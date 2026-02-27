#!/usr/bin/env python3
"""
Paper SSOT Consistency Check

Prüft bidirektionale Konsistenz zwischen:
  - bibliography/bcm_master.bib (BibTeX)
  - data/paper-references/PAP-*.yaml (YAML SSOT)

Usage:
  python scripts/check_paper_consistency.py              # Full report
  python scripts/check_paper_consistency.py --summary     # One-line summary
  python scripts/check_paper_consistency.py --fix-missing  # Generate missing YAMLs
  python scripts/check_paper_consistency.py --exit-code    # Exit 1 if gaps > threshold
"""

import argparse
import os
import re
import sys


BIB_FILE = "bibliography/bcm_master.bib"
REFS_DIR = "data/paper-references"
GAP_THRESHOLD = 0  # For --exit-code: max allowed BIB→YAML gaps


def extract_bib_keys():
    """Extract all BibTeX keys from bcm_master.bib."""
    keys = set()
    with open(BIB_FILE, 'r') as f:
        for line in f:
            m = re.match(r'^@\w+\{([^,]+),', line)
            if m:
                key = m.group(1).strip()
                # Normalize: ensure PAP- prefix
                if not key.startswith('PAP-'):
                    key = f"PAP-{key}"
                keys.add(key)
    return keys


def extract_yaml_keys():
    """Extract all YAML keys from paper-references directory."""
    keys = set()
    for fname in os.listdir(REFS_DIR):
        if fname.startswith('PAP-') and fname.endswith('.yaml'):
            keys.add(fname.replace('.yaml', ''))
    return keys


def main():
    parser = argparse.ArgumentParser(description="Paper SSOT Consistency Check")
    parser.add_argument('--summary', action='store_true', help="One-line summary")
    parser.add_argument('--fix-missing', action='store_true', help="Show commands to fix gaps")
    parser.add_argument('--exit-code', action='store_true', help="Exit 1 if BIB→YAML gaps > threshold")
    args = parser.parse_args()

    bib_keys = extract_bib_keys()
    yaml_keys = extract_yaml_keys()

    both = bib_keys & yaml_keys
    bib_only = bib_keys - yaml_keys
    yaml_only = yaml_keys - bib_keys

    total = len(bib_keys | yaml_keys)
    consistency = len(both) / total * 100 if total > 0 else 100

    if args.summary:
        status = "OK" if len(bib_only) == 0 else "GAPS"
        print(f"[{status}] BIB: {len(bib_keys)} | YAML: {len(yaml_keys)} | Match: {len(both)} | "
              f"BIB→YAML gaps: {len(bib_only)} | YAML→BIB gaps: {len(yaml_only)} | "
              f"Consistency: {consistency:.1f}%")
        if args.exit_code and len(bib_only) > GAP_THRESHOLD:
            sys.exit(1)
        return

    # Full report
    print("=" * 60)
    print("PAPER SSOT CONSISTENCY CHECK")
    print("=" * 60)
    print()
    print(f"  BibTeX entries:      {len(bib_keys)}")
    print(f"  YAML references:     {len(yaml_keys)}")
    print(f"  Match (in both):     {len(both)}")
    print(f"  BIB without YAML:    {len(bib_only)}")
    print(f"  YAML without BIB:    {len(yaml_only)}")
    print(f"  Consistency:         {consistency:.1f}%")
    print()

    if bib_only:
        print(f"--- BIB without YAML ({len(bib_only)}) ---")
        for key in sorted(bib_only):
            print(f"  {key}")
        print()

    if yaml_only:
        print(f"--- YAML without BIB ({len(yaml_only)}) ---")
        for key in sorted(yaml_only):
            print(f"  {key}")
        print()

    if not bib_only and not yaml_only:
        print("PERFECT: 100% bidirektionale Konsistenz!")
    elif not bib_only:
        print(f"BIB→YAML: 100% (alle BibTeX-Einträge haben YAML)")
        print(f"YAML→BIB: {len(yaml_only)} orphan YAMLs (niedrige Priorität)")
    else:
        print(f"ACTION NEEDED: {len(bib_only)} BibTeX-Einträge ohne YAML")

    if args.exit_code and len(bib_only) > GAP_THRESHOLD:
        sys.exit(1)


if __name__ == '__main__':
    main()
