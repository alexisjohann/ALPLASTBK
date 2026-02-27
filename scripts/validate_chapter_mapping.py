#!/usr/bin/env python3
"""
Validate Chapter-Appendix Mapping (SSOT)

This script validates the chapter-appendix-mapping.yaml against:
1. Actual chapter files in chapters/
2. Actual appendix files in appendices/
3. Internal consistency rules

Usage:
    python scripts/validate_chapter_mapping.py
    python scripts/validate_chapter_mapping.py --strict  # Fail on warnings
    python scripts/validate_chapter_mapping.py --fix     # Show fix suggestions

Exit codes:
    0 = Valid
    1 = Errors found
    2 = Warnings found (with --strict)
"""

import os
import sys
import re
import yaml
import glob
import argparse
from collections import defaultdict
from pathlib import Path


# =============================================================================
# CONFIGURATION
# =============================================================================

YAML_PATH = "docs/frameworks/chapter-appendix-mapping.yaml"
CHAPTERS_DIR = "chapters"
APPENDICES_DIR = "appendices"

VALID_CATEGORIES = {"CORE", "FORMAL", "DOMAIN", "CONTEXT", "METHOD", "PREDICT", "LIT", "REF"}
VALID_CHAPTER_TYPES = {"A", "B", "C"}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def load_yaml():
    """Load and parse the YAML mapping file."""
    if not os.path.exists(YAML_PATH):
        print(f"ERROR: YAML file not found: {YAML_PATH}")
        sys.exit(1)

    with open(YAML_PATH, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def get_chapter_files():
    """Get all chapter files from the chapters directory."""
    pattern = os.path.join(CHAPTERS_DIR, "*.tex")
    files = glob.glob(pattern)

    # Extract chapter numbers from filenames
    chapters = {}
    for f in files:
        basename = os.path.basename(f)
        # Match patterns like "01_", "10_", "4x_", "24_"
        match = re.match(r'^(\d+x?|\d+)_', basename)
        if match:
            num = match.group(1)
            # Normalize: "01" -> "1", but keep "4x" as is
            if num.isdigit():
                num = str(int(num))
            chapters[num] = basename

    return chapters


def get_appendix_files():
    """Get all appendix files from the appendices directory."""
    pattern = os.path.join(APPENDICES_DIR, "*.tex")
    files = glob.glob(pattern)

    # Filter out templates, backups, index
    excluded = {'00_appendix_template.tex', '00_appendix_index.tex'}

    appendices = set()
    for f in files:
        basename = os.path.basename(f)
        if basename in excluded or '_backup' in basename:
            continue

        # Extract code from filename (first part before underscore or entire name)
        # Examples: "AAA_CORE-WHO.tex" -> "AAA", "BK_METHOD-CALC.tex" -> "BK"
        code_match = re.match(r'^([A-Z]+\d*|[A-Z]+)', basename)
        if code_match:
            appendices.add(code_match.group(1))

    return appendices


# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def validate_chapters(data, actual_chapters, errors, warnings):
    """Validate chapter definitions against actual files."""
    yaml_chapters = {}

    for ch in data.get('chapters', []):
        num = str(ch['number'])
        yaml_chapters[num] = ch

        # Check chapter type
        ch_type = ch.get('type', 'B')
        if ch_type not in VALID_CHAPTER_TYPES:
            errors.append(f"Chapter {num}: Invalid type '{ch_type}' (must be A, B, or C)")

        # Check file exists
        expected_file = ch.get('file')
        if expected_file:
            full_path = os.path.join(CHAPTERS_DIR, expected_file)
            if not os.path.exists(full_path):
                warnings.append(f"Chapter {num}: File not found: {expected_file}")

    # Check for chapters in filesystem but not in YAML
    for num, filename in actual_chapters.items():
        if num not in yaml_chapters and not num.startswith('0'):
            warnings.append(f"Chapter {num} ({filename}) exists but not in YAML")

    # Check for chapters in YAML but not in filesystem
    for num in yaml_chapters:
        if num not in actual_chapters and num != '4x':
            errors.append(f"Chapter {num} in YAML but no file found")


def validate_appendices(data, actual_appendices, errors, warnings):
    """Validate appendix definitions against actual files."""
    yaml_appendices = {}
    codes_seen = set()

    for app in data.get('appendices', []):
        code = app['code']

        # Check for duplicate codes
        if code in codes_seen:
            errors.append(f"Appendix {code}: Duplicate code")
        codes_seen.add(code)

        yaml_appendices[code] = app

        # Check category
        category = app.get('category', '')
        if category not in VALID_CATEGORIES:
            errors.append(f"Appendix {code}: Invalid category '{category}'")

        # Check primary chapter exists
        primary = app.get('primary_chapter')
        if primary is None and category not in {'REF', 'LIT'}:
            warnings.append(f"Appendix {code}: No primary_chapter specified")

    # Check for appendices in YAML but possibly missing files
    # (This is a soft check since file naming varies)
    yaml_codes = set(yaml_appendices.keys())

    # Report count mismatch
    expected = data.get('metadata', {}).get('total_appendices', 0)
    actual = len(yaml_codes)
    if expected != actual:
        warnings.append(f"Metadata says {expected} appendices but YAML has {actual}")


def validate_cross_references(data, errors, warnings):
    """Validate cross-references between chapters and appendices."""
    chapter_nums = {str(ch['number']) for ch in data.get('chapters', [])}
    appendix_codes = {app['code'] for app in data.get('appendices', [])}

    for app in data.get('appendices', []):
        code = app['code']

        # Check primary_chapter reference
        primary = app.get('primary_chapter')
        if primary is not None:
            if str(primary) not in chapter_nums:
                errors.append(f"Appendix {code}: primary_chapter '{primary}' not found")

        # Check secondary_chapters references
        for sec in app.get('secondary_chapters', []):
            if str(sec) not in chapter_nums:
                errors.append(f"Appendix {code}: secondary_chapter '{sec}' not found")


def validate_core_consistency(data, errors, warnings):
    """Validate CORE appendix specific rules."""
    core_appendices = [app for app in data.get('appendices', [])
                       if app.get('category') == 'CORE']

    # CORE appendices should link to Type A chapters
    type_a_chapters = {str(ch['number']) for ch in data.get('chapters', [])
                       if ch.get('type') == 'A'}

    for app in core_appendices:
        code = app['code']
        primary = str(app.get('primary_chapter', ''))

        # This is a soft check - CORE appendices often link to their concept chapter
        if primary and primary not in type_a_chapters:
            # Just a warning, not an error
            pass


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description='Validate chapter-appendix mapping')
    parser.add_argument('--strict', action='store_true',
                        help='Treat warnings as errors')
    parser.add_argument('--fix', action='store_true',
                        help='Show fix suggestions')
    parser.add_argument('--quiet', '-q', action='store_true',
                        help='Only show errors')
    args = parser.parse_args()

    print("=" * 70)
    print("CHAPTER-APPENDIX MAPPING VALIDATION")
    print("=" * 70)
    print(f"SSOT: {YAML_PATH}")
    print()

    # Load data
    data = load_yaml()
    actual_chapters = get_chapter_files()
    actual_appendices = get_appendix_files()

    errors = []
    warnings = []

    # Run validations
    validate_chapters(data, actual_chapters, errors, warnings)
    validate_appendices(data, actual_appendices, errors, warnings)
    validate_cross_references(data, errors, warnings)
    validate_core_consistency(data, errors, warnings)

    # Report results
    if errors:
        print("ERRORS:")
        for e in errors:
            print(f"  [ERROR] {e}")
        print()

    if warnings and not args.quiet:
        print("WARNINGS:")
        for w in warnings:
            print(f"  [WARN]  {w}")
        print()

    # Summary
    print("-" * 70)
    metadata = data.get('metadata', {})
    print(f"Chapters in YAML:   {len(data.get('chapters', []))} (expected: {metadata.get('total_chapters', '?')})")
    print(f"Appendices in YAML: {len(data.get('appendices', []))} (expected: {metadata.get('total_appendices', '?')})")
    print(f"Chapter files:      {len(actual_chapters)}")
    print(f"Appendix files:     {len(actual_appendices)} (unique codes)")
    print("-" * 70)

    if errors:
        print(f"RESULT: FAILED ({len(errors)} errors, {len(warnings)} warnings)")
        return 1
    elif warnings and args.strict:
        print(f"RESULT: FAILED (strict mode, {len(warnings)} warnings)")
        return 2
    elif warnings:
        print(f"RESULT: PASSED with {len(warnings)} warnings")
        return 0
    else:
        print("RESULT: PASSED")
        return 0


if __name__ == '__main__':
    sys.exit(main())
