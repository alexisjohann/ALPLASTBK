#!/usr/bin/env python3
"""
Validate Paper YAML Schema against Appendix BM 2D Classification System.

This script validates that all paper YAML files in data/paper-references/
conform to the schema defined in Appendix BM, including:

1. Required fields (superkey, title, year, etc.)
2. Content Level validation (L0-L3 based on character_count)
3. Integration Level validation (I0-I5 based on ebf_integration fields)
4. Prior Score schema completeness (new 2D format)

References:
    - Appendix BM: Paper Database Schema & Prior Score Methodology
    - Definition 2: Content Level Thresholds
    - Definition 3: Integration Level Criteria
    - Definition 4: Quality Score Q(p)

Usage:
    python scripts/validate_paper_yaml_schema.py
    python scripts/validate_paper_yaml_schema.py --fix  # Auto-fix missing fields
    python scripts/validate_paper_yaml_schema.py --verbose  # Show all details
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
from collections import defaultdict
import yaml

# =============================================================================
# APPENDIX BM DEFINITIONS
# =============================================================================

# DEFINITION 2: Content Level Thresholds
THRESHOLD_L1 = 2000   # Minimum for L1 (abstract threshold)
THRESHOLD_L2 = 6000   # Minimum for L2 (key sections threshold)
THRESHOLD_L3 = 50000  # Minimum for L3 (full text threshold)

# DEFINITION 3: Integration Level Criteria
INTEGRATION_CRITERIA = {
    'I1': ['use_for', 'evidence_tier'],           # Classified
    'I2': ['theory_support'],                      # Theorized (MS-XX-XXX pattern)
    'I3': ['case_links'],                          # Exemplified (CAS-XXX pattern)
    'I4': ['parameter'],                           # Parameterized
    'I5': ['appendix_refs', 'chapter_refs'],       # Canonized
}

# Required top-level fields - Two schema variants exist
# Schema A (preferred): paper, superkey, title, author, year
# Schema B (minimal): bibtex_key, id, abstract
REQUIRED_FIELDS_A = ['paper', 'superkey', 'title', 'year']
REQUIRED_FIELDS_B = ['bibtex_key', 'id']  # Minimal variant

# Fields that should exist in any valid paper YAML
REQUIRED_FIELDS_ANY = ['doi']  # At least DOI should be present

# Expected prior_score fields (NEW 2D format from Appendix BM)
PRIOR_SCORE_FIELDS_NEW = [
    'prior_score',
    'classification',
    'content_level',
    'integration_level',      # NEW
    'confidence_multiplier',
    'evidence_quality',
    'quality_score',          # NEW (dict with q_C, q_I, q_total)
    'computed_date',
]

# Old format fields (for detection)
PRIOR_SCORE_FIELDS_OLD = [
    'prior_score',
    'classification',
    'content_level',
    'confidence_multiplier',
    'evidence_quality',
    'computed_date',
]


def load_yaml(filepath: Path) -> Optional[Dict]:
    """Load a YAML file safely."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        return None


def estimate_content_level_from_chars(char_count: int) -> str:
    """
    Estimate content level from character count.
    Implements Definition 2 from Appendix BM.
    """
    if char_count >= THRESHOLD_L3:
        return 'L3'
    elif char_count >= THRESHOLD_L2:
        return 'L2'
    elif char_count >= THRESHOLD_L1:
        return 'L1'
    else:
        return 'L0'


def estimate_integration_level(paper: Dict) -> Tuple[str, List[str]]:
    """
    Estimate integration level from paper data.
    Implements Definition 3 from Appendix BM.

    Returns:
        Tuple of (integration_level, list of reasons)
    """
    ebf = paper.get('ebf_integration', {})
    reasons = []

    # Check I5: Canonized (appendix_refs AND chapter_refs)
    has_appendix = bool(ebf.get('appendix_refs'))
    has_chapter = bool(ebf.get('chapter_refs'))
    if has_appendix and has_chapter:
        reasons.append('appendix_refs + chapter_refs → I5')
        return 'I5', reasons

    # Check I4: Parameterized
    has_parameter = bool(ebf.get('parameter'))
    # Also check top-level parameters
    if not has_parameter:
        has_parameter = bool(paper.get('parameters'))
    if has_parameter:
        reasons.append('parameter → I4')
        return 'I4', reasons

    # Check I3: Exemplified (case_links)
    has_case = bool(ebf.get('case_links'))
    if has_case:
        reasons.append('case_links → I3')
        return 'I3', reasons

    # Check I2: Theorized (theory_support with MS-XX-XXX pattern)
    theory_support = ebf.get('theory_support', '')
    if theory_support and re.search(r'MS-[A-Z]{2}-\d{3}', str(theory_support)):
        reasons.append(f'theory_support ({theory_support}) → I2')
        return 'I2', reasons

    # Check I1: Classified (use_for or evidence_tier)
    has_use_for = bool(ebf.get('use_for'))
    has_tier = bool(ebf.get('evidence_tier'))
    if has_use_for or has_tier:
        reasons.append('use_for/evidence_tier → I1')
        return 'I1', reasons

    # I0: Not integrated
    reasons.append('No integration markers → I0')
    return 'I0', reasons


def validate_paper_yaml(filepath: Path) -> Dict[str, Any]:
    """
    Validate a single paper YAML file.

    Returns:
        Dict with validation results
    """
    result = {
        'filepath': str(filepath),
        'filename': filepath.name,
        'valid': True,
        'errors': [],
        'warnings': [],
        'info': {},
        'schema_version': 'unknown',
        'metadata_schema': 'unknown',  # A (full) or B (minimal)
    }

    # Load YAML
    data = load_yaml(filepath)
    if data is None:
        result['valid'] = False
        result['errors'].append('Failed to parse YAML')
        return result

    # Detect metadata schema variant
    has_schema_a = all(f in data for f in ['paper', 'superkey'])
    has_schema_b = all(f in data for f in ['bibtex_key', 'id'])

    if has_schema_a:
        result['metadata_schema'] = 'A_FULL'
        # Check full required fields for Schema A
        for field in REQUIRED_FIELDS_A:
            if field not in data:
                result['warnings'].append(f'Schema A missing field: {field}')
        result['info']['superkey'] = data.get('superkey', 'UNKNOWN')
    elif has_schema_b:
        result['metadata_schema'] = 'B_MINIMAL'
        result['warnings'].append('Uses minimal Schema B (bibtex_key/id instead of paper/superkey)')
        result['info']['superkey'] = data.get('id', 'UNKNOWN')
        # Map B fields to standard names
        result['info']['bibtex_key'] = data.get('bibtex_key')
    else:
        result['metadata_schema'] = 'UNKNOWN'
        result['errors'].append('Unknown metadata schema (missing paper/superkey AND bibtex_key/id)')
        result['valid'] = False
        result['info']['superkey'] = 'UNKNOWN'

    # Check full_text section
    full_text = data.get('full_text', {})
    if full_text:
        result['info']['has_fulltext'] = full_text.get('available', False)
        result['info']['char_count'] = full_text.get('character_count', 0)
        result['info']['content_level_declared'] = full_text.get('content_level', 'L0')

        # Validate content level against character count
        char_count = full_text.get('character_count', 0)
        expected_level = estimate_content_level_from_chars(char_count)
        declared_level = full_text.get('content_level', 'L0')

        result['info']['content_level_expected'] = expected_level

        if declared_level != expected_level:
            result['warnings'].append(
                f'Content level mismatch: declared={declared_level}, '
                f'expected={expected_level} (chars={char_count})'
            )
    else:
        result['info']['has_fulltext'] = False
        result['info']['char_count'] = 0
        result['info']['content_level_declared'] = 'L0'
        result['info']['content_level_expected'] = 'L0'

    # Check ebf_integration section
    ebf = data.get('ebf_integration', {})
    if ebf:
        result['info']['has_ebf_integration'] = True
        result['info']['evidence_tier'] = ebf.get('evidence_tier')
        result['info']['use_for'] = ebf.get('use_for', [])
        result['info']['theory_support'] = ebf.get('theory_support')
        result['info']['parameter'] = ebf.get('parameter')

        # Estimate integration level
        int_level, reasons = estimate_integration_level(data)
        result['info']['integration_level_computed'] = int_level
        result['info']['integration_reasons'] = reasons
    else:
        result['info']['has_ebf_integration'] = False
        result['info']['integration_level_computed'] = 'I0'
        result['info']['integration_reasons'] = ['No ebf_integration section']

    # Check prior_score section
    prior_score = data.get('prior_score', {})
    if prior_score:
        result['info']['has_prior_score'] = True

        # Detect schema version
        has_integration_level = 'integration_level' in prior_score
        has_quality_score = 'quality_score' in prior_score

        if has_integration_level and has_quality_score:
            result['schema_version'] = 'NEW_2D'
        else:
            result['schema_version'] = 'OLD_1D'
            result['warnings'].append(
                'Prior score uses OLD schema (missing integration_level and quality_score)'
            )

        result['info']['prior_score_value'] = prior_score.get('prior_score')
        result['info']['classification'] = prior_score.get('classification')
        result['info']['content_level_prior'] = prior_score.get('content_level')
        result['info']['integration_level_prior'] = prior_score.get('integration_level')
    else:
        result['info']['has_prior_score'] = False
        result['schema_version'] = 'NONE'

    return result


def validate_all_papers(paper_dir: Path, verbose: bool = False) -> Dict[str, Any]:
    """
    Validate all paper YAML files in directory.

    Returns:
        Dict with aggregate statistics
    """
    stats = {
        'total': 0,
        'valid': 0,
        'invalid': 0,
        'schema_old': 0,
        'schema_new': 0,
        'schema_none': 0,
        'metadata_schema_a': 0,  # Full metadata schema
        'metadata_schema_b': 0,  # Minimal metadata schema
        'metadata_schema_unknown': 0,
        'content_level_mismatch': 0,
        'has_fulltext': 0,
        'has_ebf_integration': 0,
        'has_prior_score': 0,
        'content_levels': defaultdict(int),
        'integration_levels': defaultdict(int),
        'errors_by_type': defaultdict(int),
        'files_with_errors': [],
        'files_with_warnings': [],
    }

    results = []

    yaml_files = sorted(paper_dir.glob('PAP-*.yaml'))
    stats['total'] = len(yaml_files)

    for filepath in yaml_files:
        result = validate_paper_yaml(filepath)
        results.append(result)

        if result['valid']:
            stats['valid'] += 1
        else:
            stats['invalid'] += 1
            stats['files_with_errors'].append(result['filename'])

        if result['warnings']:
            stats['files_with_warnings'].append(result['filename'])

        # Schema version (prior_score format)
        if result['schema_version'] == 'OLD_1D':
            stats['schema_old'] += 1
        elif result['schema_version'] == 'NEW_2D':
            stats['schema_new'] += 1
        else:
            stats['schema_none'] += 1

        # Metadata schema (A=full vs B=minimal)
        if result.get('metadata_schema') == 'A_FULL':
            stats['metadata_schema_a'] += 1
        elif result.get('metadata_schema') == 'B_MINIMAL':
            stats['metadata_schema_b'] += 1
        else:
            stats['metadata_schema_unknown'] += 1

        # Content level
        content_level = result['info'].get('content_level_declared', 'L0')
        stats['content_levels'][content_level] += 1

        # Check for mismatch
        if result['info'].get('content_level_declared') != result['info'].get('content_level_expected'):
            stats['content_level_mismatch'] += 1

        # Integration level
        int_level = result['info'].get('integration_level_computed', 'I0')
        stats['integration_levels'][int_level] += 1

        # Flags
        if result['info'].get('has_fulltext'):
            stats['has_fulltext'] += 1
        if result['info'].get('has_ebf_integration'):
            stats['has_ebf_integration'] += 1
        if result['info'].get('has_prior_score'):
            stats['has_prior_score'] += 1

        # Errors
        for error in result['errors']:
            error_type = error.split(':')[0] if ':' in error else error
            stats['errors_by_type'][error_type] += 1

        if verbose:
            print(f"\n{'='*60}")
            print(f"File: {result['filename']}")
            print(f"  Superkey: {result['info'].get('superkey')}")
            print(f"  Valid: {result['valid']}")
            print(f"  Schema: {result['schema_version']}")
            print(f"  Content Level: {result['info'].get('content_level_declared')} "
                  f"(expected: {result['info'].get('content_level_expected')})")
            print(f"  Integration Level: {result['info'].get('integration_level_computed')}")
            if result['errors']:
                print(f"  ERRORS: {result['errors']}")
            if result['warnings']:
                print(f"  Warnings: {result['warnings']}")

    return stats, results


def print_report(stats: Dict[str, Any]):
    """Print validation report."""
    print("\n" + "="*70)
    print("PAPER YAML SCHEMA VALIDATION REPORT")
    print("Reference: Appendix BM - 2D Classification System")
    print("="*70)

    print(f"\n📊 SUMMARY")
    print(f"   Total files:        {stats['total']}")
    print(f"   Valid:              {stats['valid']} ({100*stats['valid']/max(stats['total'],1):.1f}%)")
    print(f"   Invalid:            {stats['invalid']}")

    print(f"\n📋 PRIOR SCORE SCHEMA (Appendix BM)")
    print(f"   NEW (2D format):    {stats['schema_new']} ({100*stats['schema_new']/max(stats['total'],1):.1f}%)")
    print(f"   OLD (1D format):    {stats['schema_old']} ({100*stats['schema_old']/max(stats['total'],1):.1f}%)")
    print(f"   NONE (no prior):    {stats['schema_none']} ({100*stats['schema_none']/max(stats['total'],1):.1f}%)")

    print(f"\n📝 METADATA SCHEMA")
    print(f"   Schema A (full):    {stats['metadata_schema_a']} ({100*stats['metadata_schema_a']/max(stats['total'],1):.1f}%) - paper/superkey/title/year")
    print(f"   Schema B (minimal): {stats['metadata_schema_b']} ({100*stats['metadata_schema_b']/max(stats['total'],1):.1f}%) - bibtex_key/id only")
    print(f"   Unknown:            {stats['metadata_schema_unknown']} ({100*stats['metadata_schema_unknown']/max(stats['total'],1):.1f}%)")

    print(f"\n📖 CONTENT LEVEL DISTRIBUTION (Definition 2)")
    for level in ['L0', 'L1', 'L2', 'L3']:
        count = stats['content_levels'].get(level, 0)
        bar = '█' * int(40 * count / max(stats['total'], 1))
        print(f"   {level}: {count:4d} {bar}")
    print(f"   Mismatches: {stats['content_level_mismatch']} (declared ≠ computed)")

    print(f"\n🔗 INTEGRATION LEVEL DISTRIBUTION (Definition 3)")
    for level in ['I0', 'I1', 'I2', 'I3', 'I4', 'I5']:
        count = stats['integration_levels'].get(level, 0)
        bar = '█' * int(40 * count / max(stats['total'], 1))
        print(f"   {level}: {count:4d} {bar}")

    print(f"\n📦 DATA AVAILABILITY")
    print(f"   Has full_text:        {stats['has_fulltext']} ({100*stats['has_fulltext']/max(stats['total'],1):.1f}%)")
    print(f"   Has ebf_integration:  {stats['has_ebf_integration']} ({100*stats['has_ebf_integration']/max(stats['total'],1):.1f}%)")
    print(f"   Has prior_score:      {stats['has_prior_score']} ({100*stats['has_prior_score']/max(stats['total'],1):.1f}%)")

    if stats['errors_by_type']:
        print(f"\n❌ ERRORS BY TYPE")
        for error_type, count in sorted(stats['errors_by_type'].items(), key=lambda x: -x[1]):
            print(f"   {error_type}: {count}")

    if stats['files_with_errors'][:10]:
        print(f"\n⚠️  FILES WITH ERRORS (first 10)")
        for f in stats['files_with_errors'][:10]:
            print(f"   - {f}")

    # Migration recommendation
    print(f"\n" + "="*70)
    print("📋 MIGRATION RECOMMENDATION")
    print("="*70)

    if stats['metadata_schema_b'] > 0:
        print(f"\n   1️⃣  METADATA NORMALIZATION:")
        print(f"   {stats['metadata_schema_b']} files use minimal Schema B (bibtex_key/id):")
        print(f"   → These need normalization to Schema A (paper/superkey/title/year)")
        print(f"   → Run: python scripts/normalize_paper_yaml_schema.py --batch")

    if stats['schema_old'] > 0:
        print(f"\n   2️⃣  PRIOR SCORE 2D MIGRATION:")
        print(f"   {stats['schema_old']} files need migration to NEW 2D schema:")
        print(f"   → Run: python scripts/compute_prior_scores.py --batch --update")
        print(f"   → This will add integration_level and quality_score fields")

    if stats['content_level_mismatch'] > 0:
        print(f"\n   3️⃣  CONTENT LEVEL VALIDATION:")
        print(f"   {stats['content_level_mismatch']} files have content_level mismatches:")
        print(f"   → Content level declared does not match character_count thresholds")
        print(f"   → Review Definition 2 thresholds: L1={THRESHOLD_L1}, L2={THRESHOLD_L2}, L3={THRESHOLD_L3}")

    gap = stats['total'] - stats['has_prior_score']
    if gap > 0:
        print(f"\n   4️⃣  MISSING PRIOR SCORES:")
        print(f"   {gap} files have no prior_score computed:")
        print(f"   → Run: python scripts/compute_prior_scores.py --batch")


def main():
    parser = argparse.ArgumentParser(
        description='Validate Paper YAML Schema against Appendix BM'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show details for each file'
    )
    parser.add_argument(
        '--paper-dir',
        type=Path,
        default=Path('data/paper-references'),
        help='Directory containing paper YAML files'
    )
    parser.add_argument(
        '--single',
        type=Path,
        help='Validate a single file'
    )

    args = parser.parse_args()

    if args.single:
        result = validate_paper_yaml(args.single)
        import json
        print(json.dumps(result, indent=2, default=str))
        return

    if not args.paper_dir.exists():
        print(f"Error: Directory not found: {args.paper_dir}")
        sys.exit(1)

    stats, results = validate_all_papers(args.paper_dir, verbose=args.verbose)
    print_report(stats)


if __name__ == '__main__':
    main()
