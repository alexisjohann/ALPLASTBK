#!/usr/bin/env python3
"""
identify_cross_references.py - Cross-Reference Identification Algorithm (CRIA)

Implements the CRIA algorithm from Appendix BO (REF-ARCH) to identify
which appendices should cross-reference each other.

Usage:
    python scripts/identify_cross_references.py appendices/HI_*.tex
    python scripts/identify_cross_references.py --all --threshold 0.6
    python scripts/identify_cross_references.py --missing-only
    python scripts/identify_cross_references.py --matrix

Author: EBF Framework
Version: 1.0 (January 2026)
Reference: Appendix BO (REF-ARCH), Section 4
"""

import os
import re
import sys
import argparse
from glob import glob
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass
from pathlib import Path


# =============================================================================
# CONSTANTS (from Appendix BO)
# =============================================================================

# Weights for relevance score calculation
WEIGHTS = {
    'w1_10c': 0.40,      # 10C dimension overlap
    'w2_cat': 0.20,      # Category affinity
    'w3_term': 0.25,     # Terminology overlap
    'w4_param': 0.15,    # Parameter overlap
}

# Category Affinity Matrix (from BO Section 4.3)
# Rows and columns: CORE, FORMAL, DOMAIN, CONTEXT, METHOD, PREDICT, LIT, REF
CATEGORIES = ['CORE', 'FORMAL', 'DOMAIN', 'CONTEXT', 'METHOD', 'PREDICT', 'LIT', 'REF']

CATEGORY_AFFINITY = {
    ('CORE', 'CORE'): 0.9,    ('CORE', 'FORMAL'): 0.8,   ('CORE', 'DOMAIN'): 0.7,
    ('CORE', 'CONTEXT'): 0.8, ('CORE', 'METHOD'): 0.6,   ('CORE', 'PREDICT'): 0.7,
    ('CORE', 'LIT'): 0.8,     ('CORE', 'REF'): 0.5,

    ('FORMAL', 'FORMAL'): 0.7, ('FORMAL', 'DOMAIN'): 0.5, ('FORMAL', 'CONTEXT'): 0.6,
    ('FORMAL', 'METHOD'): 0.7, ('FORMAL', 'PREDICT'): 0.6, ('FORMAL', 'LIT'): 0.4,
    ('FORMAL', 'REF'): 0.4,

    ('DOMAIN', 'DOMAIN'): 0.6, ('DOMAIN', 'CONTEXT'): 0.7, ('DOMAIN', 'METHOD'): 0.6,
    ('DOMAIN', 'PREDICT'): 0.5, ('DOMAIN', 'LIT'): 0.5, ('DOMAIN', 'REF'): 0.4,

    ('CONTEXT', 'CONTEXT'): 0.7, ('CONTEXT', 'METHOD'): 0.6, ('CONTEXT', 'PREDICT'): 0.6,
    ('CONTEXT', 'LIT'): 0.5, ('CONTEXT', 'REF'): 0.4,

    ('METHOD', 'METHOD'): 0.6, ('METHOD', 'PREDICT'): 0.7, ('METHOD', 'LIT'): 0.5,
    ('METHOD', 'REF'): 0.6,

    ('PREDICT', 'PREDICT'): 0.5, ('PREDICT', 'LIT'): 0.4, ('PREDICT', 'REF'): 0.3,

    ('LIT', 'LIT'): 0.6, ('LIT', 'REF'): 0.5,

    ('REF', 'REF'): 0.4,
}

# 10C Dimensions
DIMENSIONS_10C = ['WHO', 'WHAT', 'HOW', 'WHEN', 'WHERE', 'AWARE', 'READY', 'STAGE', 'HIERARCHY', 'EIT']

# Category patterns in filenames
CATEGORY_PATTERNS = {
    'CORE': r'CORE-',
    'FORMAL': r'FORMAL-',
    'DOMAIN': r'DOMAIN-',
    'CONTEXT': r'CONTEXT-',
    'METHOD': r'METHOD-',
    'PREDICT': r'PREDICT-',
    'LIT': r'LIT-',
    'REF': r'REF-',
}


# =============================================================================
# DATA STRUCTURES
# =============================================================================

@dataclass
class AppendixFeatures:
    """Features extracted from an appendix for CRIA calculation."""
    code: str
    filename: str
    category: str
    dimensions_10c: Set[str]
    terms: Set[str]
    parameters: Set[str]
    existing_refs: Set[str]  # Already referenced appendices


@dataclass
class CrossRefRecommendation:
    """A cross-reference recommendation."""
    source: str
    target: str
    score: float
    level: str  # 'must', 'should', 'may'
    components: Dict[str, float]  # Individual score components
    is_missing: bool  # True if reference doesn't exist yet


# =============================================================================
# FEATURE EXTRACTION
# =============================================================================

def extract_code_from_filename(filename: str) -> str:
    """Extract appendix code from filename."""
    basename = os.path.basename(filename)
    # Pattern: CODE_CATEGORY-NAME_description.tex
    match = re.match(r'^([A-Z]+\d*|[A-Z]+)_', basename)
    if match:
        return match.group(1)
    # Fallback: first part before underscore
    return basename.split('_')[0].upper()


def extract_category(filename: str, content: str) -> str:
    """Extract category from filename or content."""
    basename = os.path.basename(filename)

    for cat, pattern in CATEGORY_PATTERNS.items():
        if re.search(pattern, basename, re.IGNORECASE):
            return cat

    # Try to find in content
    for cat, pattern in CATEGORY_PATTERNS.items():
        if re.search(pattern, content):
            return cat

    return 'UNKNOWN'


def extract_10c_dimensions(content: str) -> Set[str]:
    """Extract 10C dimensions mentioned in the appendix."""
    dimensions = set()

    # Direct dimension mentions
    dimension_patterns = {
        'WHO': r'\bWHO\b|CORE-WHO|welfare hierarchy|aggregation level',
        'WHAT': r'\bWHAT\b|CORE-WHAT|utility dimension|FEPSDE',
        'HOW': r'\bHOW\b|CORE-HOW|complementarity|interaction',
        'WHEN': r'\bWHEN\b|CORE-WHEN|context|Ψ|psi',
        'WHERE': r'\bWHERE\b|CORE-WHERE|parameter|BBB',
        'AWARE': r'\bAWARE\b|CORE-AWARE|awareness|consciousness',
        'READY': r'\bREADY\b|CORE-READY|willingness|capacity',
        'STAGE': r'\bSTAGE\b|CORE-STAGE|journey|behavioral change',
        'HIERARCHY': r'\bHIERARCHY\b|CORE-HIERARCHY|decision hierarchy|L[0-3]',
        'EIT': r'\bEIT\b|CORE-EIT|intervention|emergence',
    }

    for dim, pattern in dimension_patterns.items():
        if re.search(pattern, content, re.IGNORECASE):
            dimensions.add(dim)

    return dimensions


def extract_terms(content: str) -> Set[str]:
    """Extract key behavioral economics terms from content."""
    # Common EBF terms (subset for efficiency)
    key_terms = [
        'loss aversion', 'prospect theory', 'mental accounting',
        'hyperbolic discounting', 'present bias', 'default effect',
        'social preferences', 'reciprocity', 'fairness', 'inequity aversion',
        'bounded rationality', 'heuristics', 'nudge', 'choice architecture',
        'framing', 'anchoring', 'availability', 'representativeness',
        'overconfidence', 'status quo bias', 'endowment effect',
        'sunk cost', 'time inconsistency', 'self-control',
        'social norms', 'peer effects', 'identity', 'motivation',
        'intrinsic', 'extrinsic', 'crowding out', 'incentives',
        'utility', 'welfare', 'complementarity', 'substitutability',
    ]

    found_terms = set()
    content_lower = content.lower()

    for term in key_terms:
        if term in content_lower:
            found_terms.add(term)

    return found_terms


def extract_parameters(content: str) -> Set[str]:
    """Extract behavioral parameters mentioned in content."""
    parameters = set()

    # Common parameter patterns
    param_patterns = [
        r'\\lambda\b|\blambda\b|λ',  # Loss aversion
        r'\\beta\b|\bbeta\b|β',      # Time discounting
        r'\\gamma\b|\bgamma\b|γ',    # Complementarity
        r'\\alpha\b|\balpha\b|α',    # Risk aversion
        r'\\delta\b|\bdelta\b|δ',    # Discount factor
        r'\\sigma\b|\bsigma\b|σ',    # Social sensitivity
        r'\\kappa\b|\bkappa\b|κ',    # Context sensitivity
        r'\\tau\b|\btau\b|τ',        # Time parameters
        r'\\theta\b|\btheta\b|θ',    # Threshold
        r'\\rho\b|\brho\b|ρ',        # Correlation
    ]

    for pattern in param_patterns:
        if re.search(pattern, content):
            # Extract the Greek letter name
            match = re.search(r'\\(\w+)|([αβγδλσκτθρ])', pattern)
            if match:
                parameters.add(match.group(1) or match.group(2))

    return parameters


def extract_existing_references(content: str) -> Set[str]:
    """Extract appendix codes already referenced in the content."""
    refs = set()

    # Pattern: Appendix X, Appendix XX, Appendix XXX
    matches = re.findall(r'Appendix\s+([A-Z]{1,3}\d*)', content)
    refs.update(matches)

    # Pattern: app:code references
    matches = re.findall(r'\\ref\{app:([a-z\-]+)\}', content, re.IGNORECASE)
    refs.update(m.upper() for m in matches)

    # Pattern: CORE-XXX, METHOD-XXX, etc.
    for cat in CATEGORIES:
        matches = re.findall(rf'{cat}-([A-Z]+)', content)
        refs.update(matches)

    return refs


def extract_features(filepath: str) -> Optional[AppendixFeatures]:
    """Extract all features from an appendix file."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        print(f"Warning: Could not read {filepath}: {e}", file=sys.stderr)
        return None

    code = extract_code_from_filename(filepath)
    category = extract_category(filepath, content)
    dimensions = extract_10c_dimensions(content)
    terms = extract_terms(content)
    parameters = extract_parameters(content)
    existing_refs = extract_existing_references(content)

    return AppendixFeatures(
        code=code,
        filename=filepath,
        category=category,
        dimensions_10c=dimensions,
        terms=terms,
        parameters=parameters,
        existing_refs=existing_refs,
    )


# =============================================================================
# CRIA SCORE CALCULATION
# =============================================================================

def get_category_affinity(cat1: str, cat2: str) -> float:
    """Get category affinity score from the matrix."""
    # Matrix is symmetric
    key1 = (cat1, cat2)
    key2 = (cat2, cat1)

    if key1 in CATEGORY_AFFINITY:
        return CATEGORY_AFFINITY[key1]
    if key2 in CATEGORY_AFFINITY:
        return CATEGORY_AFFINITY[key2]

    # Default for unknown categories
    return 0.3


def jaccard_similarity(set1: Set[str], set2: Set[str]) -> float:
    """Calculate Jaccard similarity between two sets."""
    if not set1 and not set2:
        return 0.0

    intersection = len(set1 & set2)
    union = len(set1 | set2)

    return intersection / union if union > 0 else 0.0


def overlap_ratio(set1: Set[str], set2: Set[str]) -> float:
    """Calculate overlap ratio (intersection / size of set1)."""
    if not set1:
        return 0.0

    intersection = len(set1 & set2)
    return intersection / len(set1)


def calculate_relevance_score(features1: AppendixFeatures,
                              features2: AppendixFeatures) -> Tuple[float, Dict[str, float]]:
    """
    Calculate CRIA relevance score between two appendices.

    Returns: (total_score, component_scores)
    """
    # S_10C: 10C dimension overlap (Jaccard similarity)
    s_10c = jaccard_similarity(features1.dimensions_10c, features2.dimensions_10c)

    # S_cat: Category affinity
    s_cat = get_category_affinity(features1.category, features2.category)

    # S_term: Terminology overlap
    s_term = overlap_ratio(features1.terms, features2.terms)

    # S_param: Parameter overlap
    s_param = overlap_ratio(features1.parameters, features2.parameters)

    # Weighted sum
    total = (
        WEIGHTS['w1_10c'] * s_10c +
        WEIGHTS['w2_cat'] * s_cat +
        WEIGHTS['w3_term'] * s_term +
        WEIGHTS['w4_param'] * s_param
    )

    components = {
        'S_10C': s_10c,
        'S_cat': s_cat,
        'S_term': s_term,
        'S_param': s_param,
    }

    return total, components


def score_to_level(score: float) -> str:
    """Convert relevance score to recommendation level."""
    if score > 0.8:
        return 'must'
    elif score > 0.6:
        return 'should'
    elif score > 0.5:
        return 'may'
    else:
        return 'none'


# =============================================================================
# MAIN ANALYSIS FUNCTIONS
# =============================================================================

def analyze_single_appendix(filepath: str, all_features: Dict[str, AppendixFeatures],
                           threshold: float = 0.5) -> List[CrossRefRecommendation]:
    """Analyze cross-references for a single appendix."""
    features = all_features.get(extract_code_from_filename(filepath))
    if not features:
        return []

    recommendations = []

    for code, other_features in all_features.items():
        if code == features.code:
            continue

        score, components = calculate_relevance_score(features, other_features)
        level = score_to_level(score)

        if score > threshold:
            is_missing = code not in features.existing_refs

            recommendations.append(CrossRefRecommendation(
                source=features.code,
                target=code,
                score=score,
                level=level,
                components=components,
                is_missing=is_missing,
            ))

    # Sort by score descending
    recommendations.sort(key=lambda r: r.score, reverse=True)

    return recommendations


def load_all_appendices(appendix_dir: str = 'appendices') -> Dict[str, AppendixFeatures]:
    """Load features from all appendices."""
    features = {}

    pattern = os.path.join(appendix_dir, '*.tex')
    files = glob(pattern)

    for filepath in files:
        basename = os.path.basename(filepath)
        # Skip index and template files
        if basename.startswith('00_') or 'template' in basename.lower():
            continue

        f = extract_features(filepath)
        if f:
            features[f.code] = f

    return features


# =============================================================================
# OUTPUT FORMATTING
# =============================================================================

def print_recommendations(recommendations: List[CrossRefRecommendation],
                         verbose: bool = False,
                         missing_only: bool = False):
    """Print recommendations in a formatted way."""
    if missing_only:
        recommendations = [r for r in recommendations if r.is_missing]

    if not recommendations:
        print("No recommendations above threshold.")
        return

    print(f"\n{'='*70}")
    print(f"Cross-Reference Recommendations for {recommendations[0].source}")
    print(f"{'='*70}\n")

    # Group by level
    must_refs = [r for r in recommendations if r.level == 'must']
    should_refs = [r for r in recommendations if r.level == 'should']
    may_refs = [r for r in recommendations if r.level == 'may']

    if must_refs:
        print("🔴 MUST REFERENCE (R > 0.8):")
        for r in must_refs:
            status = "❌ MISSING" if r.is_missing else "✅ EXISTS"
            print(f"   {r.target:6} → R={r.score:.2f} {status}")
            if verbose:
                print(f"          S_10C={r.components['S_10C']:.2f}, "
                      f"S_cat={r.components['S_cat']:.2f}, "
                      f"S_term={r.components['S_term']:.2f}, "
                      f"S_param={r.components['S_param']:.2f}")
        print()

    if should_refs:
        print("🟡 SHOULD REFERENCE (0.6 < R ≤ 0.8):")
        for r in should_refs:
            status = "❌ MISSING" if r.is_missing else "✅ EXISTS"
            print(f"   {r.target:6} → R={r.score:.2f} {status}")
            if verbose:
                print(f"          S_10C={r.components['S_10C']:.2f}, "
                      f"S_cat={r.components['S_cat']:.2f}, "
                      f"S_term={r.components['S_term']:.2f}, "
                      f"S_param={r.components['S_param']:.2f}")
        print()

    if may_refs:
        print("🟢 MAY REFERENCE (0.5 < R ≤ 0.6):")
        for r in may_refs:
            status = "❌ MISSING" if r.is_missing else "✅ EXISTS"
            print(f"   {r.target:6} → R={r.score:.2f} {status}")
        print()

    # Summary
    total = len(recommendations)
    missing = sum(1 for r in recommendations if r.is_missing)
    print(f"{'─'*70}")
    print(f"Total: {total} recommendations | Missing: {missing} | Existing: {total-missing}")


def print_matrix(all_features: Dict[str, AppendixFeatures], threshold: float = 0.5):
    """Print a matrix of all cross-reference scores."""
    codes = sorted(all_features.keys())

    print(f"\n{'='*70}")
    print("Cross-Reference Affinity Matrix (R > {:.1f})".format(threshold))
    print(f"{'='*70}\n")

    # Header
    print("      ", end="")
    for code in codes[:15]:  # Limit for readability
        print(f"{code:>6}", end="")
    print()

    for code1 in codes[:15]:
        print(f"{code1:6}", end="")
        for code2 in codes[:15]:
            if code1 == code2:
                print("   -- ", end="")
            else:
                score, _ = calculate_relevance_score(
                    all_features[code1],
                    all_features[code2]
                )
                if score > threshold:
                    print(f" {score:.2f}", end="")
                else:
                    print("   .  ", end="")
        print()


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='CRIA: Cross-Reference Identification Algorithm',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s appendices/HI_*.tex           # Analyze single appendix
  %(prog)s --all                         # Analyze all appendices
  %(prog)s --all --missing-only          # Show only missing references
  %(prog)s --matrix                      # Show affinity matrix
  %(prog)s --all --threshold 0.6         # Custom threshold

Reference: Appendix BO (REF-ARCH), Section 4
        """
    )

    parser.add_argument('files', nargs='*', help='Appendix files to analyze')
    parser.add_argument('--all', '-a', action='store_true',
                       help='Analyze all appendices')
    parser.add_argument('--threshold', '-t', type=float, default=0.5,
                       help='Minimum score threshold (default: 0.5)')
    parser.add_argument('--missing-only', '-m', action='store_true',
                       help='Show only missing cross-references')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Show detailed score components')
    parser.add_argument('--matrix', action='store_true',
                       help='Print cross-reference matrix')
    parser.add_argument('--appendix-dir', default='appendices',
                       help='Directory containing appendices')

    args = parser.parse_args()

    # Load all appendix features
    print("Loading appendix features...", file=sys.stderr)
    all_features = load_all_appendices(args.appendix_dir)
    print(f"Loaded {len(all_features)} appendices.", file=sys.stderr)

    if args.matrix:
        print_matrix(all_features, args.threshold)
        return

    if args.all:
        # Analyze all appendices
        for code in sorted(all_features.keys()):
            filepath = all_features[code].filename
            recommendations = analyze_single_appendix(
                filepath, all_features, args.threshold
            )
            if recommendations:
                print_recommendations(
                    recommendations,
                    verbose=args.verbose,
                    missing_only=args.missing_only
                )
    elif args.files:
        # Analyze specified files
        for filepath in args.files:
            for f in glob(filepath):
                recommendations = analyze_single_appendix(
                    f, all_features, args.threshold
                )
                if recommendations:
                    print_recommendations(
                        recommendations,
                        verbose=args.verbose,
                        missing_only=args.missing_only
                    )
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
