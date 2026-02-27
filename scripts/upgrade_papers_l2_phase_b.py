#!/usr/bin/env python3
"""
Paper L1→L2 Phase B: Multi-Source Upgrade

Goes beyond abstract-parsing (Phase A) by mining 5 additional data sources
already present in the YAML files:

  B1: EBF Metadata Mining  - identification/parameter/external_validity fields
  B2: Summary Mining       - key_findings, abstract_extended, ebf_relevance
  B3: Title Keywords       - methodology cues in paper titles
  B4: Journal Inference    - top journals imply empirical methodology
  B5: Author-Method Inference - prolific authors' typical methodology

Each approach can independently set S2/S3/S4 flags. If S1+S2+S3+S4 all
detected across ANY combination of approaches → upgrade to L2.

Usage:
  python scripts/upgrade_papers_l2_phase_b.py --dry-run           # Analyze only
  python scripts/upgrade_papers_l2_phase_b.py --dry-run --batch 1 # 1 paper
  python scripts/upgrade_papers_l2_phase_b.py --dry-run --batch 10
  python scripts/upgrade_papers_l2_phase_b.py --apply             # Apply all
  python scripts/upgrade_papers_l2_phase_b.py --stats             # Summary only
"""

import os
import re
import yaml
import sys
from pathlib import Path
from datetime import date

PAPER_DIR = Path("data/paper-references")
BIB_FILE = Path("bibliography/bcm_master.bib")
TODAY = date.today().isoformat()

# =============================================================================
# B1: EBF METADATA MINING
# =============================================================================
# These keywords in ebf_integration.identification imply S2 (methodology)
IDENTIFICATION_S2_KEYWORDS = [
    'RCT', 'randomized', 'experiment', 'field_experiment', 'lab_experiment',
    'natural_experiment', 'quasi_experiment', 'DiD', 'difference_in_difference',
    'regression_discontinuity', 'RDD', 'instrumental_variable', 'IV',
    'panel', 'cross_section', 'time_series', 'survey', 'meta_analysis',
    'empirical', 'regression', 'estimation', 'OLS', '2SLS', 'GMM',
    'event_study', 'propensity_score', 'fixed_effects', 'calibration',
    'simulation', 'structural_estimation', 'bounds', 'Bayesian',
    'rerandomization', 'longitudinal', 'repeated_cross_section',
    'audit_study', 'correspondence_study', 'conjoint',
]

# Keywords in identification that also imply S3 (sample/data present)
IDENTIFICATION_S3_KEYWORDS = [
    'RCT', 'randomized', 'field_experiment', 'lab_experiment',
    'natural_experiment', 'DiD', 'regression_discontinuity', 'RDD',
    'panel', 'cross_section', 'survey', 'meta_analysis',
    'empirical', 'event_study', 'longitudinal', 'audit_study',
    'correspondence_study', 'conjoint', 'rerandomization',
    'N_very_large', 'N_large', 'N_medium',
]

# Keywords in identification that imply theoretical-only (NOT S3)
THEORETICAL_KEYWORDS = [
    'theoretical', 'conceptual', 'behavioral_model', 'review',
    'normative', 'axiomatic', 'proof', 'philosophical',
]


def mine_ebf_metadata(data):
    """B1: Extract S2/S3/S4 signals from ebf_integration fields."""
    ebf = data.get('ebf_integration', {})
    if not ebf:
        return {}, []

    signals = {}
    sources = []

    # --- identification → S2 + possibly S3 ---
    ident = ebf.get('identification', '')
    if ident and isinstance(ident, str):
        ident_lower = ident.lower().replace('-', '_').replace(' ', '_')

        # Check if theoretical
        is_theoretical = any(kw.lower() in ident_lower for kw in THEORETICAL_KEYWORDS)

        # S2: methodology detected?
        for kw in IDENTIFICATION_S2_KEYWORDS:
            if kw.lower().replace('-', '_') in ident_lower:
                signals['S2'] = True
                sources.append(f'B1:identification={kw}')
                break

        # S3: data/sample implied?
        if not is_theoretical:
            for kw in IDENTIFICATION_S3_KEYWORDS:
                if kw.lower().replace('-', '_') in ident_lower:
                    signals['S3'] = True
                    sources.append(f'B1:identification→S3={kw}')
                    break

        # Check for N= patterns in identification
        if re.search(r'N\s*[=_]\s*\d', ident):
            signals['S3'] = True
            sources.append('B1:identification→N=')

    # --- external_validity → S3 ---
    ext_val = ebf.get('external_validity', '')
    if ext_val and isinstance(ext_val, str):
        # Countries/regions imply data exists
        geo_patterns = [
            r'\b(?:US|USA|UK|EU|OECD|China|India|Germany|Switzerland|Austria|'
            r'Denmark|Sweden|Norway|Finland|Netherlands|France|Italy|Spain|'
            r'Japan|Korea|Israel|Brazil|Mexico|Canada|Australia|Africa)\b',
            r'\bcausal\b', r'\breplicated\b', r'\bcross[_-]?country\b',
            r'\b\d+\s*countries\b',
        ]
        for pat in geo_patterns:
            if re.search(pat, ext_val, re.IGNORECASE):
                signals['S3'] = True
                sources.append(f'B1:external_validity→S3')
                break

    # --- parameter → S4 ---
    param = ebf.get('parameter', '')
    if param and isinstance(param, str):
        # Any named parameters with values imply findings
        if re.search(r'[=≈~]\s*[-+]?\d', param):
            signals['S4'] = True
            sources.append('B1:parameter→S4(numeric)')
        elif len(param) > 10:
            # Even named parameters without values suggest empirical findings
            signals['S4'] = True
            sources.append('B1:parameter→S4(named)')

    return signals, sources


# =============================================================================
# B2: SUMMARY SECTION MINING
# =============================================================================

def mine_summary(data):
    """B2: Extract S2/S3/S4 from summary sections."""
    summary = data.get('summary', {})
    if not summary:
        return {}, []

    signals = {}
    sources = []

    # key_findings → S4
    kf = summary.get('key_findings', '')
    if kf and isinstance(kf, str) and len(kf) > 50:
        signals['S4'] = True
        sources.append('B2:summary.key_findings')

    # key_findings_structured → S4
    kfs = data.get('key_findings_structured', [])
    if kfs and isinstance(kfs, list) and len(kfs) > 0:
        signals['S4'] = True
        sources.append('B2:key_findings_structured')

    # abstract_extended → mine for S2/S3/S4 using Phase A keywords
    ext = summary.get('abstract_extended', '')
    if ext and isinstance(ext, str) and len(ext) > 100:
        sys.path.insert(0, str(Path(__file__).parent))
        from upgrade_papers_l2 import METHODOLOGY_KEYWORDS, SAMPLE_DATA_KEYWORDS, FINDINGS_KEYWORDS, detect_keywords
        s2_found, _ = detect_keywords(ext, METHODOLOGY_KEYWORDS)
        s3_found, _ = detect_keywords(ext, SAMPLE_DATA_KEYWORDS)
        s4_found, _ = detect_keywords(ext, FINDINGS_KEYWORDS)
        if s2_found:
            signals['S2'] = True
            sources.append('B2:abstract_extended→S2')
        if s3_found:
            signals['S3'] = True
            sources.append('B2:abstract_extended→S3')
        if s4_found:
            signals['S4'] = True
            sources.append('B2:abstract_extended→S4')

    # ebf_relevance → can imply methodology
    rel = summary.get('ebf_relevance', '')
    if rel and isinstance(rel, str):
        if re.search(r'(?:RCT|experiment|panel|survey|empirical|field)', rel, re.IGNORECASE):
            signals['S2'] = True
            sources.append('B2:ebf_relevance→S2')

    return signals, sources


# =============================================================================
# B3: TITLE KEYWORD EXTRACTION
# =============================================================================

TITLE_S2_PATTERNS = [
    # Explicit methodology in title
    (r'\b(?:field|lab(?:oratory)?|natural|quasi[- ]?)\s*experiment', 'experiment'),
    (r'\brandomized\s+(?:controlled\s+)?trial\b', 'RCT'),
    (r'\bRCT\b', 'RCT'),
    (r'\bempirical\s+(?:analysis|evidence|study|investigation)\b', 'empirical'),
    (r'\bmeta[- ]analysis\b', 'meta-analysis'),
    (r'\bsystematic\s+review\b', 'systematic_review'),
    (r'\bevent\s+study\b', 'event_study'),
    (r'\bregression\s+discontinuity\b', 'RDD'),
    (r'\bdifference[- ]in[- ]difference', 'DiD'),
    (r'\binstrumental\s+variable\b', 'IV'),
    (r'\bpanel\s+(?:data|analysis|study)\b', 'panel'),
    (r'\bcross[- ](?:country|cultural|section)', 'cross_section'),
    (r'\blongitudinal\b', 'longitudinal'),
    (r'\bsurvey\s+(?:evidence|data|of)\b', 'survey'),
    (r'\baudit\s+study\b', 'audit_study'),
    (r'\bcorrespondence\s+(?:study|test)\b', 'correspondence_study'),
]

TITLE_S2_S3_PATTERNS = [
    # Patterns that imply BOTH methodology AND data
    (r'\bevidence\s+from\s+(?:a\s+)?(?:natural|field|randomized|large)', 'evidence_from'),
    (r'\bevidence\s+from\s+(?:the\s+)?(?:\w+\s+){0,2}(?:experiment|survey|panel|data)', 'evidence_from'),
    (r'\busing\s+(?:\w+\s+)?(?:data|panel|survey|experiment)', 'using_data'),
    (r'\banalysis\s+of\s+(?:\w+\s+){0,3}(?:data|panel|survey|records)', 'analysis_of_data'),
    (r'\bfrom\s+(?:\d+|a)\s+(?:countries|firms|households|schools|states)', 'from_N_units'),
    (r'\b(?:in|across)\s+\d+\s+(?:countries|firms|states|regions)', 'across_N'),
]


def mine_title(data):
    """B3: Extract S2/S3 signals from paper title."""
    title = data.get('title', '')
    if not title:
        return {}, []

    signals = {}
    sources = []

    for pat, label in TITLE_S2_PATTERNS:
        if re.search(pat, title, re.IGNORECASE):
            signals['S2'] = True
            sources.append(f'B3:title→S2({label})')
            break

    for pat, label in TITLE_S2_S3_PATTERNS:
        if re.search(pat, title, re.IGNORECASE):
            signals['S2'] = True
            signals['S3'] = True
            sources.append(f'B3:title→S2+S3({label})')
            break

    return signals, sources


# =============================================================================
# B4: JOURNAL-BASED INFERENCE
# =============================================================================

# Journals where papers are overwhelmingly empirical (>90% have S2+S3+S4)
EMPIRICAL_JOURNALS = {
    # Top-5 Economics
    'American Economic Review': {'S2': True, 'S3': True},
    'Quarterly Journal of Economics': {'S2': True, 'S3': True},
    'Journal of Political Economy': {'S2': True, 'S3': True},
    'Econometrica': {'S2': True},  # Some are pure theory
    'Review of Economic Studies': {'S2': True, 'S3': True},
    # Strong empirical journals
    'Review of Economics and Statistics': {'S2': True, 'S3': True, 'S4': True},
    'Journal of Labor Economics': {'S2': True, 'S3': True, 'S4': True},
    'Journal of Human Resources': {'S2': True, 'S3': True, 'S4': True},
    'Journal of Public Economics': {'S2': True, 'S3': True},
    'Journal of Development Economics': {'S2': True, 'S3': True},
    'Journal of Health Economics': {'S2': True, 'S3': True},
    'American Economic Journal: Applied Economics': {'S2': True, 'S3': True, 'S4': True},
    'American Economic Journal: Economic Policy': {'S2': True, 'S3': True, 'S4': True},
    'Journal of the European Economic Association': {'S2': True, 'S3': True},
    # Behavioral/Experimental
    'Experimental Economics': {'S2': True, 'S3': True, 'S4': True},
    'Journal of Economic Behavior \\& Organization': {'S2': True, 'S3': True},
    'Journal of Economic Behavior and Organization': {'S2': True, 'S3': True},
    'Journal of Behavioral and Experimental Economics': {'S2': True, 'S3': True, 'S4': True},
    # Finance
    'Journal of Finance': {'S2': True, 'S3': True},
    'Journal of Financial Economics': {'S2': True, 'S3': True},
    'Review of Financial Studies': {'S2': True, 'S3': True},
    # Management/Psychology
    'Management Science': {'S2': True, 'S3': True},
    'Psychological Science': {'S2': True, 'S3': True, 'S4': True},
    'Journal of Personality and Social Psychology': {'S2': True, 'S3': True, 'S4': True},
    # Science/Nature (mostly empirical)
    'Science': {'S2': True, 'S3': True},
    'Nature': {'S2': True, 'S3': True},
    'Nature Human Behaviour': {'S2': True, 'S3': True, 'S4': True},
    'Proceedings of the National Academy of Sciences': {'S2': True, 'S3': True},
}

# Build journal lookup cache from BibTeX
_bib_journal_cache = None


def _load_bib_journals():
    """Load journal mapping from BibTeX file (paper_key → journal name)."""
    global _bib_journal_cache
    if _bib_journal_cache is not None:
        return _bib_journal_cache

    _bib_journal_cache = {}
    if not BIB_FILE.exists():
        return _bib_journal_cache

    content = BIB_FILE.read_text(encoding='utf-8', errors='replace')
    current_key = None
    for line in content.split('\n'):
        # Match @article{key, or @inproceedings{key,
        m = re.match(r'@\w+\{(\S+?),', line)
        if m:
            current_key = m.group(1).strip()
            continue
        if current_key:
            m = re.match(r'\s*journal\s*=\s*\{(.+?)\}', line, re.IGNORECASE)
            if m:
                _bib_journal_cache[current_key] = m.group(1).strip()

    return _bib_journal_cache


def mine_journal(data):
    """B4: Infer S2/S3 from journal name."""
    paper_key = data.get('paper', '')
    if not paper_key:
        return {}, []

    journals = _load_bib_journals()
    journal = journals.get(paper_key, '')

    if not journal:
        return {}, []

    signals = {}
    sources = []

    # Exact match
    if journal in EMPIRICAL_JOURNALS:
        journal_signals = EMPIRICAL_JOURNALS[journal]
        signals.update(journal_signals)
        flags = '+'.join(journal_signals.keys())
        sources.append(f'B4:journal={journal}→{flags}')
        return signals, sources

    # Fuzzy match (handle LaTeX escaping, abbreviations)
    journal_lower = journal.lower().replace('\\&', '&').replace('\\', '')
    for ref_journal, ref_signals in EMPIRICAL_JOURNALS.items():
        ref_lower = ref_journal.lower().replace('\\&', '&').replace('\\', '')
        if ref_lower in journal_lower or journal_lower in ref_lower:
            signals.update(ref_signals)
            flags = '+'.join(ref_signals.keys())
            sources.append(f'B4:journal≈{ref_journal}→{flags}')
            return signals, sources

    return signals, sources


# Journals where a paper with a substantive abstract almost certainly has findings
# (>95% of papers in these journals are empirical with results)
STRONG_EMPIRICAL_JOURNALS = {
    'American Economic Review',
    'Quarterly Journal of Economics',
    'Journal of Political Economy',
    'Review of Economic Studies',
    'Review of Economics and Statistics',
    'Journal of Labor Economics',
    'Journal of Human Resources',
    'Journal of Public Economics',
    'Journal of Development Economics',
    'Journal of Health Economics',
    'American Economic Journal: Applied Economics',
    'American Economic Journal: Economic Policy',
    'Journal of the European Economic Association',
    'Experimental Economics',
    'Journal of Finance',
    'Journal of Financial Economics',
    'Review of Financial Studies',
    'Management Science',
    'Psychological Science',
    'Science',
    'Nature',
    'Nature Human Behaviour',
    'Proceedings of the National Academy of Sciences',
}


def mine_journal_s4(data):
    """B4b: Infer S4 for papers in strong empirical journals with abstracts.

    Rationale: Papers in AER, QJE, JPE etc. with a substantive abstract
    (>200 chars) virtually always contain empirical findings. The abstract
    likely contains findings language that Phase A's keywords missed due to
    subtle or domain-specific phrasing.
    """
    paper_key = data.get('paper', '')
    abstract = data.get('abstract', '')
    if not paper_key or not abstract or len(str(abstract)) < 150:
        return {}, []

    journals = _load_bib_journals()
    journal = journals.get(paper_key, '')
    if not journal:
        return {}, []

    # Check against strong empirical journals (exact + fuzzy)
    journal_clean = journal.lower().replace('\\&', '&').replace('\\', '')
    matched = False
    matched_name = ''
    for ref_journal in STRONG_EMPIRICAL_JOURNALS:
        ref_clean = ref_journal.lower().replace('\\&', '&').replace('\\', '')
        if ref_clean in journal_clean or journal_clean in ref_clean:
            matched = True
            matched_name = ref_journal
            break

    if not matched:
        return {}, []

    return {'S4': True}, [f'B4b:journal+abstract→S4({matched_name})']


# =============================================================================
# B5: AUTHOR-METHOD INFERENCE
# =============================================================================

# Authors known for specific methodology patterns
# Only highly prolific authors with consistent methods
AUTHOR_METHOD_MAP = {
    # Experimental economists (lab/field experiments)
    'Fehr': {'S2': True, 'S3': True},
    'Gneezy': {'S2': True, 'S3': True},
    'List': {'S2': True, 'S3': True},
    'Levitt': {'S2': True, 'S3': True},
    'DellaVigna': {'S2': True, 'S3': True},
    'Ariely': {'S2': True, 'S3': True},
    'Charness': {'S2': True, 'S3': True},
    'Camerer': {'S2': True, 'S3': True},
    # Development economists (RCTs)
    'Banerjee': {'S2': True, 'S3': True},
    'Duflo': {'S2': True, 'S3': True},
    'Kremer': {'S2': True, 'S3': True},
    # Empirical labor/public
    'Chetty': {'S2': True, 'S3': True},
    'Heckman': {'S2': True, 'S3': True},
    'Angrist': {'S2': True, 'S3': True},
    'Card': {'S2': True, 'S3': True},
    'Imbens': {'S2': True, 'S3': True},
    # Applied micro
    'Allcott': {'S2': True, 'S3': True},
    'Mullainathan': {'S2': True, 'S3': True},
    'Madrian': {'S2': True, 'S3': True},
}


def mine_author(data):
    """B5: Infer S2/S3 from author's typical methodology."""
    author = data.get('author', '')
    if not author:
        return {}, []

    signals = {}
    sources = []

    # Check first author (stored as last name)
    for name, method_signals in AUTHOR_METHOD_MAP.items():
        if name.lower() == author.lower():
            signals.update(method_signals)
            flags = '+'.join(method_signals.keys())
            sources.append(f'B5:author={name}→{flags}')
            break

    return signals, sources


# =============================================================================
# COMBINED ANALYSIS + UPGRADE
# =============================================================================

def get_content_level(data):
    """Get current content level from YAML data (handles both schemas)."""
    # Try top-level first (new format)
    cl = data.get('content_level', None)
    if cl and isinstance(cl, str) and cl.startswith('L'):
        return cl

    # Try prior_score.content_level (old format)
    ps = data.get('prior_score', {})
    if isinstance(ps, dict):
        cl = ps.get('content_level', None)
        if cl and isinstance(cl, str) and cl.startswith('L'):
            return cl

    # Try full_text.content_level
    ft = data.get('full_text', {})
    if isinstance(ft, dict):
        cl = ft.get('content_level', None)
        if cl and isinstance(cl, str):
            # Handle L1L0L1 bug
            if 'L2' in cl:
                return 'L2'
            if 'L3' in cl:
                return 'L3'
            if cl.startswith('L'):
                return 'L1'

    return 'L1'  # Default assumption


def has_structural_characteristics(data):
    """Check if paper already has structural_characteristics block."""
    return 'structural_characteristics' in data


def process_paper(filepath, dry_run=True, verbose=False):
    """Process a single paper through all Phase B approaches."""
    try:
        content = filepath.read_text(encoding='utf-8')
        data = yaml.safe_load(content)
    except Exception as e:
        return {'status': 'error', 'file': str(filepath), 'error': str(e)}

    if not data or not isinstance(data, dict):
        return {'status': 'error', 'file': str(filepath), 'error': 'empty/invalid YAML'}

    # Skip if not L1
    cl = get_content_level(data)
    if cl != 'L1':
        return {'status': 'skip', 'file': str(filepath), 'reason': f'already {cl}'}

    # Skip if already has structural characteristics with S2+S3+S4
    sc = data.get('structural_characteristics', {})
    if sc and sc.get('S2_methodology') and sc.get('S3_sample_data') and sc.get('S4_findings'):
        return {'status': 'skip', 'file': str(filepath), 'reason': 'already has S2+S3+S4'}

    # --- Phase A signals (abstract-based, may already be partial) ---
    abstract = data.get('abstract', '')
    s1 = bool(abstract and len(str(abstract)) > 20)
    if not s1:
        return {'status': 'skip', 'file': str(filepath), 'reason': 'no abstract'}

    # Collect signals from all 5 approaches
    all_signals = {'S2': False, 'S3': False, 'S4': False}
    all_sources = []

    # If existing structural_characteristics has partial S flags, carry them forward
    if sc:
        if sc.get('S2_methodology'):
            all_signals['S2'] = True
            all_sources.append('existing:S2')
        if sc.get('S3_sample_data'):
            all_signals['S3'] = True
            all_sources.append('existing:S3')
        if sc.get('S4_findings'):
            all_signals['S4'] = True
            all_sources.append('existing:S4')

    # B1: EBF Metadata Mining
    b1_signals, b1_sources = mine_ebf_metadata(data)
    for k, v in b1_signals.items():
        if v:
            all_signals[k] = True
    all_sources.extend(b1_sources)

    # B2: Summary Mining
    b2_signals, b2_sources = mine_summary(data)
    for k, v in b2_signals.items():
        if v:
            all_signals[k] = True
    all_sources.extend(b2_sources)

    # B3: Title Keywords
    b3_signals, b3_sources = mine_title(data)
    for k, v in b3_signals.items():
        if v:
            all_signals[k] = True
    all_sources.extend(b3_sources)

    # B4: Journal Inference
    b4_signals, b4_sources = mine_journal(data)
    for k, v in b4_signals.items():
        if v:
            all_signals[k] = True
    all_sources.extend(b4_sources)

    # B4b: Journal+Abstract → S4 inference (for strong empirical journals)
    b4b_signals, b4b_sources = mine_journal_s4(data)
    for k, v in b4b_signals.items():
        if v:
            all_signals[k] = True
    all_sources.extend(b4b_sources)

    # B5: Author Inference
    b5_signals, b5_sources = mine_author(data)
    for k, v in b5_signals.items():
        if v:
            all_signals[k] = True
    all_sources.extend(b5_sources)

    # --- S3 Inference (same as Phase A) ---
    s3_inferred = False
    if all_signals['S2'] and all_signals['S4'] and not all_signals['S3']:
        # If empirical methodology + findings → data must exist
        empirical_indicators = [
            'B1:identification', 'B3:title→S2(experiment', 'B3:title→S2(RCT',
            'B3:title→S2(empirical', 'B3:title→S2+S3', 'B4:journal',
            'B5:author',
        ]
        is_empirical = any(
            any(ind in src for ind in empirical_indicators)
            for src in all_sources
        )
        if is_empirical:
            all_signals['S3'] = True
            s3_inferred = True
            all_sources.append('inference:S2+S4→S3')

    s2 = all_signals['S2']
    s3 = all_signals['S3']
    s4 = all_signals['S4']
    can_upgrade = s1 and s2 and s3 and s4

    result = {
        'status': 'upgrade' if can_upgrade else 'partial',
        'file': str(filepath),
        'paper': data.get('paper', os.path.basename(filepath)),
        'S1': s1, 'S2': s2, 'S3': s3, 'S4': s4,
        'sources': all_sources,
        'missing': [],
        's3_inferred': s3_inferred,
    }

    if not s2:
        result['missing'].append('S2_methodology')
    if not s3:
        result['missing'].append('S3_sample_data')
    if not s4:
        result['missing'].append('S4_findings')

    if can_upgrade and not dry_run:
        _apply_upgrade(filepath, content, data, s1=True, s2=True, s3=True, s4=True, s5=False, s6=False)
        result['status'] = 'upgraded'

    return result


def _apply_upgrade(filepath, original_content, data, s1, s2, s3, s4, s5, s6):
    """Apply the L2 upgrade to a paper YAML file using regex replacements.
    Reuses the same approach as Phase A for consistency."""
    content = original_content

    # 1. Add structural_characteristics before full_text: block
    sc_block = (
        f"structural_characteristics:\n"
        f"  S1_research_question: {'true' if s1 else 'false'}\n"
        f"  S2_methodology: {'true' if s2 else 'false'}\n"
        f"  S3_sample_data: {'true' if s3 else 'false'}\n"
        f"  S4_findings: {'true' if s4 else 'false'}\n"
        f"  S5_validity: {'true' if s5 else 'false'}\n"
        f"  S6_reproducibility: {'true' if s6 else 'false'}\n"
    )

    if 'structural_characteristics:' not in content:
        if 'full_text:' in content:
            content = content.replace('full_text:', sc_block + 'full_text:', 1)
        elif 'ebf_integration:' in content:
            content = content.replace('ebf_integration:', sc_block + 'ebf_integration:', 1)
    else:
        # Update existing structural_characteristics
        content = re.sub(
            r'(structural_characteristics:\n(?:  \S+[^\n]*\n)*)',
            sc_block,
            content
        )

    # 2. Fix garbled content_level in full_text block (L1L0L1 → L2)
    content = re.sub(
        r'(full_text:\n(?:  [^\n]+\n)*?  content_level: )L1L0L1',
        r'\g<1>L2',
        content
    )
    content = re.sub(
        r'(full_text:\n(?:  [^\n]+\n)*?  content_level: )L1\b',
        r'\g<1>L2',
        content
    )

    # 3. Update prior_score.content_level: L1 → L2
    content = re.sub(
        r'(prior_score:\n(?:  [^\n]+\n)*?  content_level: )L1\b',
        r'\g<1>L2',
        content
    )

    # 4. Update top-level content_level if present (new format)
    content = re.sub(
        r'^(content_level: )L1\b',
        r'\g<1>L2',
        content,
        flags=re.MULTILINE
    )

    # 5. Update confidence_multiplier: 0.8 → 0.95
    content = re.sub(
        r'(prior_score:\n(?:  [^\n]+\n)*?  confidence_multiplier: )0\.8\b',
        r'\g<1>0.95',
        content
    )

    # 6. Update quality_score: q_C from 0.333 to 0.667, q_total accordingly
    content = re.sub(
        r'(  quality_score:\n    q_C: )0\.333',
        r'\g<1>0.667',
        content
    )
    content = re.sub(
        r'(    q_total: )0\.267',
        r'\g<1>0.433',
        content
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Paper L1→L2 Phase B: Multi-Source Upgrade')
    parser.add_argument('--batch', type=int, default=0, help='Process N papers (0=all)')
    parser.add_argument('--dry-run', action='store_true', default=True, help='Only analyze (default)')
    parser.add_argument('--apply', action='store_true', help='Actually apply upgrades')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed sources')
    parser.add_argument('--stats', action='store_true', help='Show summary only')
    parser.add_argument('--approach-stats', action='store_true', help='Show per-approach statistics')
    args = parser.parse_args()

    if args.apply:
        args.dry_run = False

    files = sorted(PAPER_DIR.glob('PAP-*.yaml'))
    print(f"Found {len(files)} paper YAMLs")

    if args.batch > 0:
        files = files[:args.batch]
        print(f"Processing batch of {args.batch}")

    results = {'upgrade': 0, 'partial': 0, 'skip': 0, 'error': 0, 'upgraded': 0}
    missing_counts = {'S2_methodology': 0, 'S3_sample_data': 0, 'S4_findings': 0}
    approach_counts = {'B1': 0, 'B2': 0, 'B3': 0, 'B4': 0, 'B5': 0, 'inference': 0, 'existing': 0}
    upgrade_list = []
    partial_list = []

    for f in files:
        r = process_paper(f, dry_run=args.dry_run, verbose=args.verbose)
        status = r['status']
        if status in results:
            results[status] += 1

        if status in ('upgrade', 'upgraded'):
            upgrade_list.append(r)
            # Count which approaches contributed
            for src in r.get('sources', []):
                for approach in approach_counts:
                    if src.startswith(approach):
                        approach_counts[approach] += 1
                        break

            if args.verbose and not args.stats:
                srcs = ', '.join(r.get('sources', [])[:5])
                print(f"  ✅ {r['paper']}: {srcs}")

        elif status == 'partial':
            partial_list.append(r)
            for m in r.get('missing', []):
                missing_counts[m] += 1
            # Still count approach contributions for partials
            for src in r.get('sources', []):
                for approach in approach_counts:
                    if src.startswith(approach):
                        approach_counts[approach] += 1
                        break

            if args.verbose and not args.stats:
                srcs = ', '.join(r.get('sources', [])[:3])
                print(f"  ⚠️  {r['paper']}: missing {r['missing']} (has: {srcs})")

        elif status == 'error':
            print(f"  ❌ {r['file']}: {r.get('error', '?')}")

    # Summary
    total_processed = sum(results.values())
    n_l1 = results['upgrade'] + results['partial'] + results.get('upgraded', 0)
    print(f"\n{'='*60}")
    print(f"PHASE B RESULTS ({total_processed} papers processed)")
    print(f"{'='*60}")
    if args.dry_run:
        print(f"  ✅ Can upgrade to L2:  {results['upgrade']:>5} ({results['upgrade']/max(n_l1,1)*100:.1f}% of L1)")
    else:
        print(f"  ✅ Upgraded to L2:     {results['upgraded']:>5}")
    print(f"  ⚠️  Partial (missing):  {results['partial']:>5} ({results['partial']/max(n_l1,1)*100:.1f}% of L1)")
    print(f"  ⏭️  Skipped (not L1):   {results['skip']:>5}")
    print(f"  ❌ Errors:              {results['error']:>5}")

    if results['partial'] > 0:
        print(f"\n  Still missing (after all 5 approaches):")
        for k, v in sorted(missing_counts.items(), key=lambda x: -x[1]):
            print(f"    {k}: {v} papers")

    if args.approach_stats or args.verbose:
        print(f"\n  Approach contributions (to upgradeable papers):")
        for approach, count in sorted(approach_counts.items(), key=lambda x: -x[1]):
            label = {
                'B1': 'EBF Metadata Mining',
                'B2': 'Summary Mining',
                'B3': 'Title Keywords',
                'B4': 'Journal Inference',
                'B5': 'Author Inference',
                'inference': 'S3 Inference (S2+S4→S3)',
                'existing': 'Existing S-flags',
            }.get(approach, approach)
            print(f"    {approach} ({label}): {count}")

    if not args.dry_run and results['upgraded'] > 0:
        print(f"\n  📊 {results['upgraded']} papers upgraded L1→L2 in Phase B")

    return results


if __name__ == '__main__':
    main()
