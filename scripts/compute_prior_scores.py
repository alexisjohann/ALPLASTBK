#!/usr/bin/env python3
"""
compute_prior_scores.py - Compute Prior Scores π(p) for Paper Database
======================================================================

Implements the formal system from Appendix BM (METHOD-PAPERINT):

CONTENT LEVEL SYSTEM (Definition 2):
- Definition 2: Content Level Function C(p) → {L0, L1, L2, L3}
- Definition 2a: L1/L2 Template Structure T_C = (ABSTRACT, KEY_FINDINGS, EBF_RELEVANCE, SOURCES)
- Definition 2b: Confidence Multiplier ρ(C) → [0.6, 1.0]
- Axiom TPL-1: Template Equivalence (L1/L2 templates ≈ full-text for prior scoring)
- Axiom TPL-2: Template Purpose (3 functions)

PRIOR SCORE SYSTEM (Definition 5-8):
- Definition 5: Prior Score π(p) = Σ wᵢ · gᵢ · sᵢ(p) · τ(p) · ρₖ
- Definition 6: Gap Vector G = (g_theory, g_param, g_case, g_LIT, g_10C, g_domain)
- Definition 7: Supply Vector S(p) = (s_theory, s_param, s_case, s_LIT, s_10C, s_domain)
- Definition 8: Weight Vector W (default: theory=0.25, param=0.25, ...)
- Definition 0b: Evidence Tier τ(p) ∈ {1.0, 0.8, 0.5}

THEOREMS:
- Theorem 2: Prior Score Algorithm (computational procedure)
- Theorem 3: Bayesian Updating with Confidence Multipliers

Usage:
    python scripts/compute_prior_scores.py --compute-gap       # Show current Gap Vector
    python scripts/compute_prior_scores.py --score PAP-xxx     # Score single paper
    python scripts/compute_prior_scores.py --batch             # Score all papers
    python scripts/compute_prior_scores.py --update-yamls      # Write scores to YAMLs
    python scripts/compute_prior_scores.py --stats             # Show score distribution

Author: EBF Team
Date: 2026-02-01
SSOT: appendices/BM_METHOD-PAPERINT_paper_integration_methodology.tex
"""

import os
import sys
import yaml
import argparse
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Tuple, Optional

# =============================================================================
# CONFIGURATION (from Appendix BM)
# =============================================================================

# =============================================================================
# DEFINITION 2: Content Level Thresholds
# =============================================================================
# C(p) = {
#     L0  if φ_C(p) ⊆ {title, author, year, journal, doi}
#     L1  if abstract ∈ φ_C(p) ∧ |p|_C < 6000
#     L2  if {methodology, findings} ⊆ φ_C(p) ∧ |p|_C < 50000
#     L3  if full_text ∈ φ_C(p) ∧ |p|_C ≥ 50000
# }
THRESHOLD_L1 = 2000   # Minimum for L1 (abstract threshold)
THRESHOLD_L2 = 6000   # Minimum for L2 (key sections threshold)
THRESHOLD_L3 = 50000  # Minimum for L3 (full text threshold)

# =============================================================================
# DEFINITION 2a: L1/L2 Template Structure T_C
# =============================================================================
# T_C = (ABSTRACT, KEY_FINDINGS, EBF_RELEVANCE, SOURCES)
# Per Axiom TPL-1: Templates are functionally equivalent to full-text for prior scoring
TEMPLATE_SECTIONS = {
    'ABSTRACT',       # Extended summary (>= original abstract)
    'KEY_FINDINGS',   # Numbered list of empirical results
    'EBF_RELEVANCE',  # 10C dimensions, theory_support, parameters
    'SOURCES',        # URLs, BibTeX keys
}

# =============================================================================
# DEFINITION 2b: Confidence Multiplier ρ(C)
# =============================================================================
# ρ: {L0, L1, L2, L3} → [0.6, 1.0]
# Reflects uncertainty discount based on available content
CONFIDENCE_MULTIPLIER = {
    'L0': 0.60,  # Metadata only (40% uncertainty discount)
    'L1': 0.80,  # + Abstract/Template (20% discount)
    'L2': 0.95,  # + Key sections/Template (5% discount)
    'L3': 1.00,  # Full text (no discount)
}

# =============================================================================
# DEFINITION 8: Default Weights W
# =============================================================================
# W = (w_theory, w_param, w_case, w_LIT, w_10C, w_domain)
# Σ wᵢ = 1.0
WEIGHTS = {
    'theory': 0.25,  # Theory Catalog contribution
    'param': 0.25,   # Parameter Registry contribution
    'case': 0.15,    # Case Registry contribution
    'LIT': 0.15,     # LIT-Appendix contribution
    '10C': 0.10,     # 10C Coverage contribution
    'domain': 0.10   # Domain Coverage contribution
}

# =============================================================================
# DEFINITION 0b: Evidence Tier τ(p)
# =============================================================================
# τ: Papers → {1.0, 0.8, 0.5}
# Reflects publication quality and methodological rigor
EVIDENCE_TIER_MULTIPLIER = {
    1: 1.0,    # Tier 1: Top-5 Journal, RCT, replicated
    2: 0.8,    # Tier 2: Peer-reviewed, solid methodology
    3: 0.5,    # Tier 3: Working paper, preprint
    None: 0.6  # Unknown tier (conservative default)
}

# Integration Decision Thresholds (Axiom MECE-4)
THRESHOLDS = {
    'high_priority': 0.7,   # Target I5
    'standard': 0.5,        # Target I3-I4
    'minimal': 0.3,         # Target I1-I2
    'reject': 0.2           # Early rejection
}

# Top-5 Journals for Tier 1
TOP5_JOURNALS = {
    'quarterly journal of economics', 'qje',
    'american economic review', 'aer',
    'econometrica',
    'journal of political economy', 'jpe',
    'review of economic studies', 'restud'
}

# High-quality journals for Tier 2
TIER2_JOURNALS = {
    'journal of finance', 'jf',
    'journal of financial economics', 'jfe',
    'review of financial studies', 'rfs',
    'management science', 'ms',
    'journal of economic behavior and organization', 'jebo',
    'journal of public economics',
    'journal of labor economics',
    'journal of monetary economics',
    'journal of economic theory',
    'games and economic behavior',
    'experimental economics',
    'journal of risk and uncertainty'
}

# LIT-Appendix author mappings
LIT_AUTHOR_MAPPING = {
    'fehr': 'LIT-FEHR',
    'thaler': 'LIT-THALER',
    'kahneman': 'LIT-KT',
    'tversky': 'LIT-KT',
    'sunstein': 'LIT-SUNSTEIN',
    'ariely': 'LIT-ARIELY',
    'camerer': 'LIT-CAMERER',
    'loewenstein': 'LIT-LOEWENSTEIN',
    'laibson': 'LIT-LAIBSON',
    'rabin': 'LIT-RABIN',
    'shleifer': 'LIT-SHLEIFER',
    'barberis': 'LIT-BARBERIS'
}

# Theory keywords for supply estimation
THEORY_KEYWORDS = {
    'prospect theory', 'loss aversion', 'reference point',
    'hyperbolic discounting', 'present bias', 'time preference',
    'social preference', 'inequity aversion', 'fairness',
    'mental accounting', 'narrow framing',
    'overconfidence', 'optimism bias',
    'anchoring', 'availability heuristic',
    'default effect', 'status quo bias',
    'nudge', 'choice architecture',
    'reciprocity', 'trust', 'cooperation'
}

# Parameter keywords
PARAMETER_KEYWORDS = {
    'lambda', 'β', 'beta', 'γ', 'gamma', 'δ', 'delta',
    'coefficient', 'parameter', 'estimate',
    'elasticity', 'marginal', 'discount rate'
}


# =============================================================================
# GAP VECTOR COMPUTATION
# =============================================================================

def compute_gap_vector(base_path: Path) -> Dict[str, float]:
    """
    Compute current Gap Vector G from EBF state.

    Returns dict with g_theory, g_param, g_case, g_LIT, g_10C, g_domain
    """
    gap = {}

    # g_theory: Theory Catalog coverage
    theory_catalog_path = base_path / 'data' / 'theory-catalog.yaml'
    try:
        if theory_catalog_path.exists():
            with open(theory_catalog_path) as f:
                theories = yaml.safe_load(f)
            # Count theories with bib_keys vs total
            total_theories = 0
            covered_theories = 0
            if theories and 'categories' in theories:
                for cat in theories['categories']:
                    if 'models' in cat:
                        for model in cat['models']:
                            total_theories += 1
                            if model.get('bib_keys'):
                                covered_theories += 1
            gap['theory'] = 1 - (covered_theories / max(total_theories, 1))
        else:
            gap['theory'] = 0.5  # Default
    except yaml.YAMLError:
        gap['theory'] = 0.5  # Default on parse error

    # g_param: Parameter Registry evidence gap
    param_registry_path = base_path / 'data' / 'parameter-registry.yaml'
    try:
        if param_registry_path.exists():
            with open(param_registry_path) as f:
                params = yaml.safe_load(f)
            total_params = len(params.get('parameters', [])) if params else 0
            params_with_evidence = sum(1 for p in params.get('parameters', [])
                                       if p.get('source') or p.get('bib_key')) if params else 0
            gap['param'] = 1 - (params_with_evidence / max(total_params, 1))
        else:
            gap['param'] = 0.6  # Default - we need parameters
    except yaml.YAMLError:
        gap['param'] = 0.6  # Default on parse error

    # g_case: Case Registry size gap (target: 1000 cases)
    case_registry_path = base_path / 'data' / 'case-registry.yaml'
    case_target = 1000
    try:
        if case_registry_path.exists():
            with open(case_registry_path) as f:
                cases = yaml.safe_load(f)
            case_count = len(cases.get('cases', [])) if cases else 0
            gap['case'] = max(0, 1 - (case_count / case_target))
        else:
            gap['case'] = 0.5
    except yaml.YAMLError:
        gap['case'] = 0.5  # Default on parse error

    # g_LIT: LIT-Appendix coverage (simplified: count papers per major author)
    bib_path = base_path / 'bibliography' / 'bcm_master.bib'
    lit_coverage = defaultdict(int)
    lit_targets = {'LIT-FEHR': 150, 'LIT-THALER': 100, 'LIT-KT': 150, 'LIT-O': 500}

    if bib_path.exists():
        with open(bib_path) as f:
            bib_content = f.read().lower()
        for author, lit in LIT_AUTHOR_MAPPING.items():
            lit_coverage[lit] += bib_content.count(author)

    # Find most under-covered LIT
    max_gap = 0
    for lit, target in lit_targets.items():
        coverage = lit_coverage.get(lit, 0)
        lit_gap = max(0, 1 - (coverage / target))
        max_gap = max(max_gap, lit_gap)
    gap['LIT'] = max_gap if max_gap > 0 else 0.3

    # g_10C: Simplified - assume moderate need
    gap['10C'] = 0.2

    # g_domain: Domain balance (simplified)
    gap['domain'] = 0.4

    return gap


# =============================================================================
# CONTENT LEVEL ESTIMATION (Definition 2)
# =============================================================================

def estimate_content_level(paper: Dict) -> Tuple[str, float]:
    """
    Estimate Content Level from paper metadata.

    Implements Definition 2 from Appendix BM:

    C(p) = {
        L0  if φ_C(p) ⊆ {title, author, year, journal, doi}
        L1  if abstract ∈ φ_C(p) ∧ |p|_C < 6000
        L2  if {methodology, findings} ⊆ φ_C(p) ∧ |p|_C < 50000
        L3  if full_text ∈ φ_C(p) ∧ |p|_C ≥ 50000
    }

    Per Axiom TPL-1 (Template Equivalence):
    L1/L2 templates in the 'summary' section are functionally
    equivalent to actual abstracts/findings for prior scoring.

    Args:
        paper: Dict with paper metadata (may include 'summary' from YAML)

    Returns:
        Tuple of (content_level, confidence_multiplier)
    """
    # Extract relevant fields
    abstract = paper.get('abstract', '') or ''
    full_text_info = paper.get('full_text', {})
    summary = paper.get('summary', {})

    # Calculate character count
    char_count = 0

    # Check for full_text (from YAML full_text section)
    if isinstance(full_text_info, dict):
        char_count = full_text_info.get('character_count', 0) or 0
        if full_text_info.get('available', False) and char_count >= THRESHOLD_L3:
            return 'L3', CONFIDENCE_MULTIPLIER['L3']
    elif isinstance(full_text_info, str):
        char_count = len(full_text_info)
        if char_count >= THRESHOLD_L3:
            return 'L3', CONFIDENCE_MULTIPLIER['L3']

    # Check for L1/L2 template content (Axiom TPL-1: Template Equivalence)
    has_abstract = bool(abstract) or bool(summary.get('abstract_extended', ''))
    has_findings = bool(summary.get('key_findings', ''))
    has_ebf_relevance = bool(summary.get('ebf_relevance', ''))

    # Calculate template char count if available
    template_chars = 0
    if summary:
        for key in ['abstract_extended', 'key_findings', 'ebf_relevance', 'sources']:
            template_chars += len(str(summary.get(key, '') or ''))
        if full_text_info and isinstance(full_text_info, dict):
            template_chars = max(template_chars, full_text_info.get('template_char_count', 0) or 0)

    # Use maximum of available content
    total_chars = max(char_count, template_chars, len(abstract))

    # Apply Definition 2 with template support
    if total_chars >= THRESHOLD_L3:
        return 'L3', CONFIDENCE_MULTIPLIER['L3']
    elif (has_findings or has_ebf_relevance) and total_chars >= THRESHOLD_L2:
        # L2: Key sections available (via template or directly)
        return 'L2', CONFIDENCE_MULTIPLIER['L2']
    elif has_abstract and total_chars >= THRESHOLD_L1:
        # L1: Abstract available (via template or directly)
        return 'L1', CONFIDENCE_MULTIPLIER['L1']
    elif has_abstract:
        # Has abstract but below L1 threshold - still counts as L1
        return 'L1', CONFIDENCE_MULTIPLIER['L1']
    else:
        # L0: Metadata only
        return 'L0', CONFIDENCE_MULTIPLIER['L0']


# =============================================================================
# SUPPLY VECTOR ESTIMATION (Definition 7)
# =============================================================================


# =============================================================================
# DEFINITION 3: Integration Level Function I(p) → {I1, I2, I3, I4, I5}
# =============================================================================
# I(p) = {
#     I1  if use_for ∈ φ_I(p) ∧ evidence_tier ∈ φ_I(p)
#     I2  if I(p) ≥ I1 ∧ theory_support ∈ φ_I(p)
#     I3  if I(p) ≥ I2 ∧ case_links ∈ φ_I(p)
#     I4  if I(p) ≥ I3 ∧ parameter ∈ φ_I(p)
#     I5  if I(p) ≥ I4 ∧ appendix_refs ∈ φ_I(p) ∧ chapter_refs ∈ φ_I(p)
# }
# Monotonicity: I1 ≺ I2 ≺ I3 ≺ I4 ≺ I5 (strict ordering by field inclusion)

INTEGRATION_LEVEL_NUMERIC = {
    'I0': 0,   # Not classified
    'I1': 1,   # Classified (use_for + evidence_tier)
    'I2': 2,   # Theorized (+ theory_support)
    'I3': 3,   # Exemplified (+ case_links)
    'I4': 4,   # Parameterized (+ parameter)
    'I5': 5,   # Canonized (+ appendix + chapter refs)
}


def estimate_integration_level(paper: Dict) -> Tuple[str, float]:
    """
    Estimate Integration Level from paper metadata.

    Implements Definition 3 from Appendix BM:

    I(p) = {
        I1  if use_for ∈ φ_I(p) ∧ evidence_tier ∈ φ_I(p)
        I2  if I(p) ≥ I1 ∧ theory_support ∈ φ_I(p)
        I3  if I(p) ≥ I2 ∧ case_links ∈ φ_I(p)
        I4  if I(p) ≥ I3 ∧ parameter ∈ φ_I(p)
        I5  if I(p) ≥ I4 ∧ appendix_refs ∈ φ_I(p) ∧ chapter_refs ∈ φ_I(p)
    }

    Per Axiom MECE-1: Integration Level is INDEPENDENT of Content Level.
    A paper can be (L0, I4) or (L3, I1) - dimensions are orthogonal.

    Args:
        paper: Dict with paper metadata

    Returns:
        Tuple of (integration_level, q_I) where q_I = I_numeric / 5
    """
    # Extract EBF-specific fields
    use_for = paper.get('use_for', '') or ''
    evidence_tier = paper.get('evidence_tier', None)
    theory_support = paper.get('theory_support', '') or ''
    case_links = paper.get('case_links', []) or []
    parameter = paper.get('parameter', '') or ''
    appendix_refs = paper.get('appendix_refs', []) or []
    chapter_refs = paper.get('chapter_refs', []) or []

    # Also check ebf_integration section (alternative location)
    ebf = paper.get('ebf_integration', {}) or {}
    if ebf:
        use_for = use_for or ebf.get('use_for', '')
        evidence_tier = evidence_tier or ebf.get('evidence_tier')
        theory_support = theory_support or ebf.get('theory_support', '')
        parameter = parameter or ebf.get('parameter', '')

    # Check each level (monotonic: must satisfy all previous levels)

    # I1: Classified (use_for + evidence_tier)
    has_use_for = bool(use_for)
    has_evidence_tier = evidence_tier is not None

    if not (has_use_for and has_evidence_tier):
        return 'I0', 0.0  # Not yet classified

    # I1 satisfied
    level = 'I1'

    # I2: Theorized (+ theory_support with MS-XX-XXX)
    has_theory = bool(theory_support) and ('ms-' in str(theory_support).lower())
    if has_theory:
        level = 'I2'
    else:
        return level, INTEGRATION_LEVEL_NUMERIC[level] / 5.0

    # I3: Exemplified (+ case_links with CAS-XXX)
    has_cases = bool(case_links) or ('cas-' in str(paper).lower())
    if has_cases:
        level = 'I3'
    else:
        return level, INTEGRATION_LEVEL_NUMERIC[level] / 5.0

    # I4: Parameterized (+ parameter with extracted values)
    has_params = bool(parameter) and any(c in str(parameter) for c in ['=', 'λ', 'β', 'γ', 'lambda', 'beta', 'alpha'])
    if has_params:
        level = 'I4'
    else:
        return level, INTEGRATION_LEVEL_NUMERIC[level] / 5.0

    # I5: Canonized (+ appendix_refs + chapter_refs)
    has_appendix = bool(appendix_refs) or ('appendix' in str(paper).lower() and '-' in str(paper))
    has_chapter = bool(chapter_refs) or ('chapter' in str(paper).lower())
    if has_appendix and has_chapter:
        level = 'I5'

    return level, INTEGRATION_LEVEL_NUMERIC[level] / 5.0


# =============================================================================
# DEFINITION 4: Quality Score Q(p) = (q_C, q_I) ∈ [0,1]²
# =============================================================================
# Q(p) = (C(p)/L3, I(p)/I5) = (q_C, q_I)
# Target state: Q* = (1, 1) ⟺ (L3, I5)

CONTENT_LEVEL_NUMERIC = {
    'L0': 0,
    'L1': 1,
    'L2': 2,
    'L3': 3,
}


def compute_quality_score(content_level: str, integration_level: str) -> Tuple[float, float]:
    """
    Compute 2D Quality Score Q(p) = (q_C, q_I).

    Implements Definition 4 from Appendix BM:
    Q(p) = (C(p)/L3, I(p)/I5) ∈ [0,1]²

    Target state: Q* = (1, 1) ⟺ (L3, I5)

    Returns:
        Tuple (q_C, q_I) where both values are in [0, 1]
    """
    q_C = CONTENT_LEVEL_NUMERIC.get(content_level, 0) / 3.0
    q_I = INTEGRATION_LEVEL_NUMERIC.get(integration_level, 0) / 5.0
    return round(q_C, 3), round(q_I, 3)


def estimate_evidence_tier(paper: Dict) -> int:
    """
    Estimate Evidence Tier τ(p) from journal or existing field.

    Implements Definition 0b from Appendix BM:

    τ(p) = {
        1.0  if p ∈ Top-5 Journal ∨ RCT ∨ replicated
        0.8  if p ∈ Peer-Reviewed ∧ solid methodology
        0.5  if p = Working Paper ∨ Preprint
    }

    Tier 1 (Gold): QJE, AER, Econometrica, JPE, REStud, RCTs
    Tier 2 (Silver): JF, JFE, RFS, MS, JEBO, other peer-reviewed
    Tier 3 (Bronze): NBER, SSRN, Working Papers, Preprints
    """
    # First check if evidence_tier is already set in metadata
    if 'evidence_tier' in paper:
        try:
            return int(paper['evidence_tier'])
        except (ValueError, TypeError):
            pass

    # Also check ebf_integration section
    ebf = paper.get('ebf_integration', {})
    if ebf and 'evidence_tier' in ebf:
        try:
            return int(ebf['evidence_tier'])
        except (ValueError, TypeError):
            pass

    journal = paper.get('journal', '').lower()

    # Check Top-5
    for j in TOP5_JOURNALS:
        if j in journal:
            return 1

    # Check Tier 2
    for j in TIER2_JOURNALS:
        if j in journal:
            return 2

    # Check for NBER, working paper indicators
    if 'nber' in journal or 'working paper' in journal.lower():
        return 3

    # Default to Tier 2 for peer-reviewed
    if journal:
        return 2

    return 3


def estimate_supply_vector(paper: Dict, base_path: Path) -> Dict[str, float]:
    """
    Estimate Supply Vector S(p) from paper metadata.

    Uses heuristics based on:
    - Title and abstract keywords
    - Author (LIT mapping)
    - Existing EBF fields (use_for, theory_support, parameter)
    - Journal quality
    """
    supply = {}

    title = paper.get('title', '') or ''
    abstract = paper.get('abstract', '') or ''
    author = paper.get('author', '') or ''
    use_for = paper.get('use_for', '') or ''
    theory_support = paper.get('theory_support', '') or ''
    param_field = paper.get('parameter', '') or ''

    title = title.lower()
    abstract = abstract.lower()
    author = author.lower()
    use_for = use_for.lower()
    theory_support = theory_support.lower()
    text = f"{title} {abstract}"

    # s_theory: Does paper extend/validate theory?
    theory_score = 0

    # High signal: existing theory_support field
    if theory_support and 'ms-' in theory_support:
        theory_score = 1.0
    else:
        # Keyword-based estimation
        for keyword in THEORY_KEYWORDS:
            if keyword in text:
                theory_score += 0.2

    supply['theory'] = min(1.0, theory_score)

    # s_param: Are parameters extractable?
    param_score = 0

    # High signal: existing parameter field
    if param_field and ('=' in param_field or 'lambda' in param_field.lower() or
                        'alpha' in param_field.lower() or 'beta' in param_field.lower()):
        param_score = 1.0
    else:
        # Keyword-based estimation
        for keyword in PARAMETER_KEYWORDS:
            if keyword in text:
                param_score += 0.15
        # Boost if methodology mentions estimation
        if 'estimat' in text or 'regress' in text or 'experiment' in text:
            param_score += 0.3

    supply['param'] = min(1.0, param_score)

    # s_case: Is there a real-world example?
    case_score = 0

    # Check use_for for case indicators
    if 'case' in use_for.lower():
        case_score = 0.8

    # Keyword-based estimation
    case_indicators = ['case study', 'field experiment', 'natural experiment',
                       'real-world', 'practical', 'application', 'policy',
                       'ultimatum', 'dictator game', 'public goods']
    case_score += sum(0.2 for ind in case_indicators if ind in text)

    supply['case'] = min(1.0, case_score)

    # s_LIT: Does paper fit an under-covered LIT?
    lit_score = 0

    # High signal: existing use_for with LIT-
    if 'lit-' in use_for:
        lit_score = 1.0
    else:
        # Author-based estimation
        for auth, lit in LIT_AUTHOR_MAPPING.items():
            if auth in author:
                lit_score = 1.0
                break

        if lit_score == 0:
            # Check if behavioral economics related
            be_keywords = ['behavioral', 'behaviour', 'nudge', 'bias', 'heuristic',
                          'cognitive', 'psychological', 'irrational']
            if any(kw in text for kw in be_keywords):
                lit_score = 0.5

    supply['LIT'] = lit_score

    # s_10C: How many 10C dimensions addressed?
    dims_covered = 0

    # Check use_for for CORE- indicators
    core_pattern = r'core-(\w+)'
    cores_in_use_for = set(re.findall(core_pattern, use_for))
    dims_covered += len(cores_in_use_for)

    # Keyword-based estimation
    dimensions = {
        'WHO': ['agent', 'consumer', 'investor', 'household', 'firm'],
        'WHAT': ['utility', 'preference', 'value', 'benefit', 'payoff'],
        'HOW': ['interaction', 'strategic', 'game', 'social', 'cooperation'],
        'WHEN': ['context', 'situation', 'environment', 'framing'],
        'WHERE': ['parameter', 'calibrat', 'estimat', 'empirical'],
        'AWARE': ['attention', 'salience', 'awareness', 'cognitive', 'limited'],
        'READY': ['intention', 'willing', 'motivation', 'ready'],
        'STAGE': ['journey', 'stage', 'phase', 'process'],
        'HIERARCHY': ['decision', 'choice', 'level', 'hierarchy'],
        'EIT': ['intervention', 'nudge', 'policy', 'design', 'mechanism']
    }
    for dim, keywords in dimensions.items():
        if any(kw in text for kw in keywords):
            dims_covered += 1

    supply['10C'] = min(1.0, dims_covered / 10.0)

    # s_domain: Domain match
    domain_score = 0.3

    # Check use_for for DOMAIN- indicators
    if 'domain-' in use_for:
        domain_score = 0.8
    elif any(kw in text for kw in ['economics', 'finance', 'behavior', 'decision',
                                    'market', 'consumer', 'investor']):
        domain_score = 0.5

    supply['domain'] = domain_score

    return supply


# =============================================================================
# PRIOR SCORE COMPUTATION
# =============================================================================

def compute_prior_score(paper: Dict, gap: Dict[str, float],
                        base_path: Path) -> Dict:
    """
    Compute Prior Score π(p) using Theorem 2 algorithm.

    Implements Definition 5 from Appendix BM:

    π(p) = Σᵢ wᵢ · gᵢ · sᵢ(p) · τ(p) · ρₖ

    Where:
    - wᵢ = Weight for dimension i (Definition 8)
    - gᵢ = Gap in dimension i (Definition 6)
    - sᵢ(p) = Supply from paper p for dimension i (Definition 7)
    - τ(p) = Evidence Tier multiplier (Definition 0b)
    - ρₖ = Confidence multiplier for Content Level k (Definition 2b)

    Returns dict with:
    - prior_score: float in [0, 1]
    - content_level: L0-L3
    - evidence_tier: 1-3
    - confidence_multiplier: ρ_k
    - supply_vector: dict
    - decision: HIGH_PRIORITY/STANDARD/MINIMAL/REJECT
    - target_integration: I1-I5
    """
    result = {}

    # Step 1: Estimate Content Level (Definition 2)
    content_level, confidence_multiplier = estimate_content_level(paper)
    result['content_level'] = content_level
    result['confidence_multiplier'] = confidence_multiplier

    # Step 1b: Estimate Integration Level (Definition 3)
    integration_level, q_I = estimate_integration_level(paper)
    result['integration_level'] = integration_level

    # Step 1c: Compute Quality Score (Definition 4)
    q_C = CONTENT_LEVEL_NUMERIC.get(content_level, 0) / 3.0
    result['quality_score'] = {
        'q_C': round(q_C, 3),
        'q_I': round(q_I, 3),
        'q_total': round((q_C + q_I) / 2, 3)  # Average as overall quality
    }

    # Step 2: Estimate Evidence Tier
    evidence_tier = estimate_evidence_tier(paper)
    result['evidence_tier'] = evidence_tier
    tau = EVIDENCE_TIER_MULTIPLIER[evidence_tier]

    # Step 3: Estimate Supply Vector
    supply = estimate_supply_vector(paper, base_path)
    result['supply_vector'] = supply

    # Step 4: Compute raw Prior Score (before confidence adjustment)
    raw_score = 0
    for dim in ['theory', 'param', 'case', 'LIT', '10C', 'domain']:
        w = WEIGHTS[dim]
        g = gap[dim]
        s = supply[dim]
        raw_score += w * g * s * tau

    result['raw_score'] = round(raw_score, 4)

    # Step 5: Apply confidence multiplier (Theorem 3, Definition 2b)
    # Per Axiom TPL-1: Templates at L1/L2 level get same ρ as direct content
    rho = result['confidence_multiplier']
    adjusted_score = raw_score * rho
    result['prior_score'] = round(adjusted_score, 4)

    # Store evidence quality for YAML output
    result['evidence_quality'] = tau

    # Step 6: Determine decision
    pi = result['prior_score']
    max_possible = raw_score  # If we had full text (ρ=1)

    if pi >= THRESHOLDS['high_priority']:
        result['decision'] = 'HIGH_PRIORITY'
        result['target_integration'] = 'I5'
    elif pi >= THRESHOLDS['standard']:
        result['decision'] = 'STANDARD'
        result['target_integration'] = 'I3-I4'
    elif pi >= THRESHOLDS['minimal']:
        result['decision'] = 'MINIMAL'
        result['target_integration'] = 'I1-I2'
    elif max_possible < THRESHOLDS['reject']:
        result['decision'] = 'REJECT'
        result['target_integration'] = None
    else:
        result['decision'] = 'PENDING'
        result['target_integration'] = 'TBD'

    result['max_possible_score'] = round(max_possible, 4)
    result['computed_at'] = datetime.now().isoformat()

    return result


# =============================================================================
# BATCH PROCESSING
# =============================================================================

def load_bibtex_entry(paper_id: str, base_path: Path) -> Dict:
    """Load paper metadata from BibTeX file."""
    bib_path = base_path / 'bibliography' / 'bcm_master.bib'
    if not bib_path.exists():
        return {}

    with open(bib_path) as f:
        content = f.read()

    # Find entry for this paper
    # Try both PAP-xxx and xxx formats
    patterns = [
        f'@article{{{paper_id},',
        f'@article{{PAP-{paper_id},',
        f'@book{{{paper_id},',
        f'@book{{PAP-{paper_id},'
    ]

    start_idx = -1
    for pattern in patterns:
        idx = content.lower().find(pattern.lower())
        if idx >= 0:
            start_idx = idx
            break

    if start_idx < 0:
        return {}

    # Extract entry (find matching closing brace)
    brace_count = 0
    end_idx = start_idx
    for i, char in enumerate(content[start_idx:]):
        if char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count == 0:
                end_idx = start_idx + i + 1
                break

    entry_text = content[start_idx:end_idx]

    # Parse fields
    paper = {}
    field_pattern = r'(\w+)\s*=\s*[{"]([^{}"\n]+)[}"]'
    for match in re.finditer(field_pattern, entry_text):
        field = match.group(1).lower()
        value = match.group(2).strip()
        paper[field] = value

    # Also try to extract evidence_tier specially
    tier_match = re.search(r'evidence_tier\s*=\s*\{(\d+)\}', entry_text)
    if tier_match:
        paper['evidence_tier'] = int(tier_match.group(1))

    return paper


def load_paper_from_yaml(yaml_path: Path) -> Dict:
    """Load paper metadata from YAML file."""
    try:
        with open(yaml_path) as f:
            paper = yaml.safe_load(f)
    except yaml.YAMLError:
        # Fallback: extract key fields manually
        with open(yaml_path) as f:
            content = f.read()

        paper = {}
        for line in content.split('\n'):
            if line.startswith('title:'):
                paper['title'] = line.split(':', 1)[1].strip().strip('"')
            elif line.startswith('author:'):
                paper['author'] = line.split(':', 1)[1].strip().strip('"')
            elif line.startswith('year:'):
                paper['year'] = line.split(':', 1)[1].strip().strip('"')
            elif line.startswith('abstract:'):
                paper['abstract'] = line.split(':', 1)[1].strip().strip('"')
            elif line.startswith('journal:'):
                paper['journal'] = line.split(':', 1)[1].strip().strip('"')
            elif line.startswith('doi:'):
                paper['doi'] = line.split(':', 1)[1].strip().strip('"')

    return paper if paper else {}


def load_paper_combined(yaml_path: Path, base_path: Path) -> Dict:
    """Load paper from YAML and BibTeX, combining both sources."""
    paper = load_paper_from_yaml(yaml_path)

    # Get paper ID
    paper_id = yaml_path.stem.replace('PAP-', '')

    # Also load from BibTeX for additional fields
    bib_data = load_bibtex_entry(paper_id, base_path)

    # Merge: YAML takes precedence, but fill in missing fields from BibTeX
    for key, value in bib_data.items():
        if key not in paper or not paper[key]:
            paper[key] = value

    return paper


def update_yaml_with_score(yaml_path: Path, score_data: Dict) -> None:
    """
    Add prior_score section to paper YAML.

    Implements the YAML schema from Appendix BM (2D Classification System):

    prior_score:
      # Prior Score (Definition 5)
      prior_score: 0.58          # π(p) = Σ wᵢ · gᵢ · sᵢ(p) · τ(p) · ρₖ
      classification: STANDARD   # Based on thresholds (Axiom MECE-4)

      # Content Level (Definition 2)
      content_level: L3          # C(p) ∈ {L0, L1, L2, L3}
      confidence_multiplier: 1.0 # ρ(C) from Definition 2b

      # Integration Level (Definition 3)
      integration_level: I2      # I(p) ∈ {I1, I2, I3, I4, I5}

      # Quality Score (Definition 4)
      quality_score:
        q_C: 1.0                 # Content quality = C(p)/L3
        q_I: 0.4                 # Integration quality = I(p)/I5
        q_total: 0.7             # Average quality

      # Evidence Tier (Definition 0b)
      evidence_quality: 1.0      # τ(p) ∈ {1.0, 0.8, 0.5}

      computed_date: "2026-02-01"
    """
    with open(yaml_path) as f:
        content = f.read()

    # Map decision to classification
    classification_map = {
        'HIGH_PRIORITY': 'FULL',
        'STANDARD': 'STANDARD',
        'MINIMAL': 'MINIMAL',
        'PENDING': 'MINIMAL',
        'REJECT': 'REJECT'
    }
    classification = classification_map.get(score_data['decision'], 'MINIMAL')

    # Get computed date (just date, not full timestamp)
    computed_date = score_data['computed_at'].split('T')[0]

    # Check if prior_score section already exists
    if 'prior_score:' in content:
        # Update existing section
        lines = content.split('\n')
        new_lines = []
        skip_until_next_section = False

        for line in lines:
            if line.startswith('prior_score:'):
                skip_until_next_section = True
                # Add new prior_score section (matching Appendix BM 2D schema)
                q_score = score_data.get('quality_score', {'q_C': 0, 'q_I': 0, 'q_total': 0})
                new_lines.append('prior_score:')
                new_lines.append(f"  prior_score: {score_data['prior_score']}")
                new_lines.append(f"  classification: {classification}")
                new_lines.append(f"  content_level: {score_data['content_level']}")
                new_lines.append(f"  integration_level: {score_data.get('integration_level', 'I0')}")
                new_lines.append(f"  confidence_multiplier: {score_data['confidence_multiplier']}")
                new_lines.append(f"  evidence_quality: {score_data.get('evidence_quality', 1.0)}")
                new_lines.append(f"  quality_score:")
                new_lines.append(f"    q_C: {q_score.get('q_C', 0)}")
                new_lines.append(f"    q_I: {q_score.get('q_I', 0)}")
                new_lines.append(f"    q_total: {q_score.get('q_total', 0)}")
                new_lines.append(f"  computed_date: '{computed_date}'")
                continue

            if skip_until_next_section:
                if line and not line.startswith(' ') and not line.startswith('\t'):
                    skip_until_next_section = False
                else:
                    continue

            new_lines.append(line)

        content = '\n'.join(new_lines)
    else:
        # Add new section at the end (matching Appendix BM 2D schema)
        q_score = score_data.get('quality_score', {'q_C': 0, 'q_I': 0, 'q_total': 0})
        prior_score_yaml = f"""
prior_score:
  prior_score: {score_data['prior_score']}
  classification: {classification}
  content_level: {score_data['content_level']}
  integration_level: {score_data.get('integration_level', 'I0')}
  confidence_multiplier: {score_data['confidence_multiplier']}
  evidence_quality: {score_data.get('evidence_quality', 1.0)}
  quality_score:
    q_C: {q_score.get('q_C', 0)}
    q_I: {q_score.get('q_I', 0)}
    q_total: {q_score.get('q_total', 0)}
  computed_date: '{computed_date}'
"""
        content = content.rstrip() + '\n' + prior_score_yaml

    with open(yaml_path, 'w') as f:
        f.write(content)


def process_all_papers(base_path: Path, update_yamls: bool = False) -> List[Dict]:
    """Process all papers and compute Prior Scores."""
    paper_refs_path = base_path / 'data' / 'paper-references'

    if not paper_refs_path.exists():
        print(f"Error: {paper_refs_path} does not exist")
        return []

    # Compute Gap Vector once
    gap = compute_gap_vector(base_path)
    print(f"\nGap Vector G:")
    for dim, val in gap.items():
        print(f"  g_{dim}: {val:.3f}")
    print()

    results = []
    yaml_files = list(paper_refs_path.glob('PAP-*.yaml'))

    print(f"Processing {len(yaml_files)} papers...")

    for i, yaml_file in enumerate(yaml_files):
        if (i + 1) % 100 == 0:
            print(f"  Processed {i + 1}/{len(yaml_files)}...")

        try:
            paper = load_paper_combined(yaml_file, base_path)
            score_data = compute_prior_score(paper, gap, base_path)
            score_data['paper_id'] = yaml_file.stem
            results.append(score_data)

            if update_yamls:
                update_yaml_with_score(yaml_file, score_data)
        except Exception as e:
            print(f"  Error processing {yaml_file.name}: {e}")

    return results


def print_statistics(results: List[Dict]) -> None:
    """Print score distribution statistics."""
    if not results:
        print("No results to analyze")
        return

    scores = [r['prior_score'] for r in results]
    decisions = defaultdict(int)
    for r in results:
        decisions[r['decision']] += 1

    print("\n" + "=" * 60)
    print("PRIOR SCORE STATISTICS")
    print("=" * 60)

    print(f"\nTotal papers: {len(results)}")
    print(f"Mean score: {sum(scores) / len(scores):.3f}")
    print(f"Min score: {min(scores):.3f}")
    print(f"Max score: {max(scores):.3f}")

    print("\nDecision Distribution:")
    for decision in ['HIGH_PRIORITY', 'STANDARD', 'MINIMAL', 'PENDING', 'REJECT']:
        count = decisions.get(decision, 0)
        pct = count / len(results) * 100
        bar = '█' * int(pct / 2)
        print(f"  {decision:15} {count:5} ({pct:5.1f}%) {bar}")

    print("\nScore Distribution:")
    ranges = [(0.0, 0.2), (0.2, 0.3), (0.3, 0.5), (0.5, 0.7), (0.7, 1.0)]
    for low, high in ranges:
        count = sum(1 for s in scores if low <= s < high)
        pct = count / len(results) * 100
        bar = '█' * int(pct / 2)
        print(f"  [{low:.1f}, {high:.1f}): {count:5} ({pct:5.1f}%) {bar}")

    print("\nTop 10 Papers by Prior Score:")
    sorted_results = sorted(results, key=lambda x: x['prior_score'], reverse=True)
    for r in sorted_results[:10]:
        print(f"  {r['prior_score']:.3f} | {r['paper_id']}")


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description='Compute Prior Scores for Paper Database')
    parser.add_argument('--compute-gap', action='store_true', help='Show current Gap Vector')
    parser.add_argument('--score', type=str, help='Score single paper (PAP-xxx)')
    parser.add_argument('--batch', action='store_true', help='Score all papers')
    parser.add_argument('--update-yamls', action='store_true', help='Write scores to YAML files')
    parser.add_argument('--stats', action='store_true', help='Show score distribution')
    parser.add_argument('--base-path', type=str, default='.', help='Base path to repository')

    args = parser.parse_args()
    base_path = Path(args.base_path).resolve()

    if args.compute_gap:
        gap = compute_gap_vector(base_path)
        print("\nCurrent Gap Vector G (EBF Needs):")
        print("=" * 40)
        for dim, val in gap.items():
            bar = '█' * int(val * 20)
            print(f"  g_{dim:8} = {val:.3f} {bar}")
        print("\nInterpretation: Higher = more need for papers in this area")
        return

    if args.score:
        paper_id = args.score
        if not paper_id.startswith('PAP-'):
            paper_id = f'PAP-{paper_id}'

        yaml_path = base_path / 'data' / 'paper-references' / f'{paper_id}.yaml'
        if not yaml_path.exists():
            print(f"Error: {yaml_path} not found")
            return

        paper = load_paper_combined(yaml_path, base_path)
        gap = compute_gap_vector(base_path)
        result = compute_prior_score(paper, gap, base_path)

        print(f"\nPrior Score for {paper_id}:")
        print("=" * 60)

        # 2D Classification (MECE-Compliant)
        print(f"\n  2D CLASSIFICATION (Appendix BM):")
        print(f"  ──────────────────────────────────")
        print(f"  Content Level     C(p) = {result['content_level']}")
        print(f"  Integration Level I(p) = {result.get('integration_level', 'I0')}")

        # Quality Score
        q = result.get('quality_score', {})
        print(f"\n  QUALITY SCORE Q(p) = ({q.get('q_C', 0):.2f}, {q.get('q_I', 0):.2f})")
        print(f"  q_total = {q.get('q_total', 0):.3f}  (Target: 1.0 = L3+I5)")

        # Prior Score Details
        print(f"\n  PRIOR SCORE π(p):")
        print(f"  ──────────────────────────────────")
        print(f"  π(p) = {result['prior_score']:.4f}")
        print(f"  Raw Score = {result['raw_score']:.4f}")
        print(f"  Evidence Tier τ = {result['evidence_tier']} (multiplier: {EVIDENCE_TIER_MULTIPLIER[result['evidence_tier']]})")
        print(f"  Confidence ρ = {result['confidence_multiplier']}")

        # Decision
        print(f"\n  DECISION (Axiom MECE-4):")
        print(f"  ──────────────────────────────────")
        print(f"  Classification = {result['decision']}")
        print(f"  Target Integration = {result['target_integration']}")

        # Supply Vector
        print(f"\n  SUPPLY VECTOR S(p):")
        print(f"  ──────────────────────────────────")
        for dim, val in result['supply_vector'].items():
            print(f"    s_{dim:8} = {val:.3f}")
        return

    if args.batch or args.update_yamls or args.stats:
        results = process_all_papers(base_path, update_yamls=args.update_yamls)

        if args.update_yamls:
            print(f"\nUpdated {len(results)} YAML files with Prior Scores")

        if args.stats or args.batch:
            print_statistics(results)
        return

    parser.print_help()


if __name__ == '__main__':
    main()
