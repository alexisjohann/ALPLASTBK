#!/usr/bin/env python3
"""
validate_bibtex_key_format.py - Enforce canonical BibTeX key format

SSOT: docs/standards/bibtex-key-convention.md

Canonical format: {nachname}{jahr}{kurzwort}
Regex: ^[a-z]+\d{4}[a-z]+$

Rules:
  R1: All lowercase ASCII (no accents, no uppercase)
  R2: No separators (no _, -, spaces)
  R3: Lastname = first author, letters only
  R4: Year = exactly 4 digits
  R5: Kurzwort = 1 meaningful word from title (MANDATORY)
  R6: Disambiguation via longer/different kurzwort
  R7: Skip stop words when selecting kurzwort

Usage:
    python scripts/validate_bibtex_key_format.py --all              # Check all keys
    python scripts/validate_bibtex_key_format.py --errors-only      # Only show violations
    python scripts/validate_bibtex_key_format.py --suggest          # Suggest fixes for violations
    python scripts/validate_bibtex_key_format.py --check KEY        # Check single key
    python scripts/validate_bibtex_key_format.py --stats            # Summary statistics
    python scripts/validate_bibtex_key_format.py --pre-commit       # Pre-commit mode (exit 1 on new violations)
"""

import re
import sys
import argparse
import unicodedata
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# SSOT import: all key generation logic lives in bibtex_key_generator.py
from bibtex_key_generator import (
    CANONICAL_PATTERN, STOP_WORDS, normalize_to_ascii, extract_kurzwort,
    extract_first_author_lastname, generate_canonical_key, is_canonical,
)

PROJECT_ROOT = Path(__file__).parent.parent
BIBTEX_PATH = PROJECT_ROOT / "bibliography" / "bcm_master.bib"
YAML_DIR = PROJECT_ROOT / "data" / "paper-references"

# Violation categories
VIOLATIONS = {
    'has_underscore': 'Contains underscores',
    'has_uppercase': 'Contains uppercase letters',
    'no_kurzwort': 'Missing kurzwort (only name+year)',
    'non_ascii': 'Contains non-ASCII characters',
    'has_hyphen': 'Contains hyphens',
    'numeric_suffix': 'Ends with numeric suffix instead of kurzwort',
    'other': 'Other format violation',
}


# normalize_to_ascii() and extract_kurzwort() imported from bibtex_key_generator.py (SSOT)


def classify_violation(key: str) -> Optional[str]:
    """Classify what kind of violation a key has."""
    if CANONICAL_PATTERN.match(key):
        return None  # No violation

    if '_' in key:
        return 'has_underscore'
    if key != key.lower():
        return 'has_uppercase'
    if re.match(r'^[a-z]+\d{4}$', key):
        return 'no_kurzwort'
    if not all(ord(c) < 128 for c in key):
        return 'non_ascii'
    if '-' in key:
        return 'has_hyphen'
    if re.match(r'^[a-z]+\d{4}[a-z]*\d+$', key):
        return 'numeric_suffix'

    return 'other'


def parse_bibtex_entries(bib_path: Path) -> Dict[str, Dict]:
    """Parse BibTeX file, return {key: {title, author, year, ...}}."""
    with open(bib_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    entries = {}
    entry_pattern = r'@(\w+)\{([^,]+),([^@]*?)(?=\n@|\Z)'

    for entry_type, key, fields_str in re.findall(entry_pattern, content, re.DOTALL):
        key = key.strip()
        fields = {'_type': entry_type.lower()}

        field_pattern = r'(\w+)\s*=\s*(?:\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}|(\d+))'
        for match in re.finditer(field_pattern, fields_str):
            fname = match.group(1).lower()
            fval = match.group(2) if match.group(2) is not None else match.group(3)
            fields[fname] = fval

        entries[key] = fields

    return entries


def suggest_canonical_key(key: str, entry: Dict) -> str:
    """Suggest a canonical key for a non-conforming entry.

    Uses generate_canonical_key() from bibtex_key_generator.py (SSOT).
    Falls back to key-based heuristics when entry metadata is missing.
    """
    title = entry.get('title', '')
    author = entry.get('author', '')
    year = entry.get('year', '')

    # If we have author metadata, use the canonical generator directly
    if author:
        if not year:
            m = re.search(r'(\d{4})', key)
            year = m.group(1) if m else '0000'
        result = generate_canonical_key(author, year, title)
        # If title was missing, try to salvage kurzwort from existing key
        if not title:
            m = re.search(r'\d{4}([a-z]+)', key.lower().replace('_', ''))
            if m:
                lastname = extract_first_author_lastname(author)
                result = f"{lastname}{year}{m.group(1)}"
        return result

    # Fallback: extract from key when no metadata available
    m = re.match(r'([a-zA-Z_]+?)[\d_]', key)
    lastname = m.group(1).replace('_', '').lower() if m else key[:6]
    lastname = normalize_to_ascii(lastname)
    lastname = re.sub(r'[^a-z]', '', lastname)

    if not year:
        m = re.search(r'(\d{4})', key)
        year = m.group(1) if m else '0000'

    kurzwort = extract_kurzwort(title)
    if not kurzwort:
        m = re.search(r'\d{4}([a-z]+)', key.lower().replace('_', ''))
        kurzwort = m.group(1) if m else 'unknown'

    return f"{lastname}{year}{kurzwort}"


def check_all_keys(bib_path: Path, errors_only: bool = False, suggest: bool = False) -> Tuple[int, int, Dict]:
    """Check all BibTeX keys for format compliance."""
    entries = parse_bibtex_entries(bib_path)

    violations_by_type = {}
    total = 0
    conforming = 0
    violations_list = []

    for key, entry in sorted(entries.items()):
        total += 1
        violation = classify_violation(key)

        if violation is None:
            conforming += 1
            if not errors_only:
                pass  # Don't print conforming keys
        else:
            violations_by_type.setdefault(violation, []).append(key)
            suggestion = suggest_canonical_key(key, entry) if suggest else None
            violations_list.append((key, violation, suggestion))

    return total, conforming, violations_by_type, violations_list


def print_stats(total: int, conforming: int, violations_by_type: Dict):
    """Print summary statistics."""
    print("=" * 70)
    print("  BIBTEX KEY FORMAT VALIDATION")
    print("  SSOT: docs/standards/bibtex-key-convention.md")
    print("=" * 70)
    print(f"\n  Total keys:     {total}")
    print(f"  Conforming:     {conforming} ({conforming/total*100:.1f}%)")
    print(f"  Non-conforming: {total - conforming} ({(total-conforming)/total*100:.1f}%)")

    if violations_by_type:
        print(f"\n  {'Violation':<25s} {'Count':>6s}  Description")
        print(f"  {'-'*25} {'-'*6}  {'-'*30}")
        for vtype in sorted(violations_by_type, key=lambda x: -len(violations_by_type[x])):
            count = len(violations_by_type[vtype])
            desc = VIOLATIONS.get(vtype, vtype)
            print(f"  {vtype:<25s} {count:>6d}  {desc}")


def main():
    parser = argparse.ArgumentParser(description='Validate BibTeX key format')
    parser.add_argument('--all', action='store_true', help='Check all keys')
    parser.add_argument('--errors-only', action='store_true', help='Only show violations')
    parser.add_argument('--suggest', action='store_true', help='Suggest canonical keys')
    parser.add_argument('--check', type=str, help='Check a single key')
    parser.add_argument('--stats', action='store_true', help='Show statistics only')
    parser.add_argument('--pre-commit', action='store_true', help='Pre-commit mode')
    parser.add_argument('--bib', type=str, default=str(BIBTEX_PATH), help='BibTeX file path')

    args = parser.parse_args()
    bib_path = Path(args.bib)

    if not bib_path.exists():
        print(f"ERROR: BibTeX file not found: {bib_path}")
        sys.exit(1)

    if args.check:
        violation = classify_violation(args.check)
        if violation:
            print(f"  ❌ {args.check}: {VIOLATIONS.get(violation, violation)}")
            entries = parse_bibtex_entries(bib_path)
            if args.check in entries:
                suggestion = suggest_canonical_key(args.check, entries[args.check])
                print(f"  → Suggested: {suggestion}")
            sys.exit(1)
        else:
            print(f"  ✅ {args.check}: Canonical format")
            sys.exit(0)

    if args.pre_commit:
        # Check only NEW or MODIFIED keys (via git diff)
        import subprocess
        try:
            result = subprocess.run(
                ['git', 'diff', '--cached', '--', str(bib_path)],
                capture_output=True, text=True, cwd=str(PROJECT_ROOT)
            )
            diff = result.stdout
        except Exception:
            diff = ''

        # Extract added keys from diff
        new_keys = re.findall(r'^\+@\w+\{([^,]+),', diff, re.MULTILINE)

        if not new_keys:
            sys.exit(0)  # No new keys

        violations = []
        for key in new_keys:
            key = key.strip()
            v = classify_violation(key)
            if v:
                violations.append((key, v))

        if violations:
            print("\n" + "=" * 70)
            print("  ⚠️  NEW BIBTEX KEYS VIOLATE CANONICAL FORMAT")
            print("  SSOT: docs/standards/bibtex-key-convention.md")
            print("=" * 70)
            for key, vtype in violations:
                print(f"  ❌ {key}: {VIOLATIONS.get(vtype, vtype)}")

            entries = parse_bibtex_entries(bib_path)
            print("\n  Suggestions:")
            for key, vtype in violations:
                if key in entries:
                    suggestion = suggest_canonical_key(key, entries[key])
                    print(f"  → {key} → {suggestion}")

            print(f"\n  Format: {{nachname}}{{jahr}}{{kurzwort}}")
            print(f"  Regex:  ^[a-z]+\\d{{4}}[a-z]+$")
            print(f"\n  ❌ COMMIT BLOCKED. Fix key format before committing.")
            print(f"  Use: python scripts/validate_bibtex_key_format.py --suggest KEY")
            print()
            sys.exit(1)

        sys.exit(0)

    # Default: --all or --stats
    total, conforming, violations_by_type, violations_list = check_all_keys(
        bib_path,
        errors_only=args.errors_only,
        suggest=args.suggest
    )

    print_stats(total, conforming, violations_by_type)

    if args.suggest and violations_list:
        print(f"\n  {'Current Key':<45s} → {'Suggested Key':<45s} Violation")
        print(f"  {'-'*45} → {'-'*45} {'-'*20}")
        for key, vtype, suggestion in violations_list:
            if suggestion:
                marker = " ⚠️" if suggestion == key else ""
                print(f"  {key:<45s} → {suggestion:<45s} {vtype}{marker}")

    if not args.suggest and violations_by_type and not args.stats:
        print(f"\n  Run with --suggest to see recommended fixes.")

    print()


if __name__ == '__main__':
    main()
