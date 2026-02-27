#!/usr/bin/env python3
"""
fix_doubled_kurzwort.py - Fix BibTeX keys with doubled kurzwort

Problem: 174 BibTeX entries have doubled kurzwort (e.g., kahneman1979prospectprospect)
         while YAML files have single kurzwort (PAP-kahneman1979prospect.yaml)

Solution: Rename BibTeX keys to single kurzwort + update all cross-references

Also fixes:
- PAP-PAP- double prefix in registry files
- PAP- prefix in LaTeX \cite{} commands (should be bare keys)
- PAP- prefix in theory-catalog bib_keys (should be bare keys)

Usage:
    python scripts/fix_doubled_kurzwort.py --dry-run          # Preview changes
    python scripts/fix_doubled_kurzwort.py --dry-run --limit 1  # Test 1 key
    python scripts/fix_doubled_kurzwort.py --execute           # Apply all fixes
"""

import re
import os
import sys
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
BIB_PATH = PROJECT_ROOT / "bibliography" / "bcm_master.bib"

# Files to scan for cross-references
CROSS_REF_PATTERNS = [
    "data/theory-catalog.yaml",
    "data/case-registry.yaml",
    "data/parameter-registry.yaml",
    "data/researcher-registry.yaml",
    "data/model-registry.yaml",
    "data/intervention-registry.yaml",
    "data/model-building-session.yaml",
    "data/forecast-registry.yaml",
    "data/concept-registry.yaml",
    "data/paper-level-classification.yaml",
]

CROSS_REF_GLOBS = [
    "data/paper-references/PAP-*.yaml",
    "data/paper-texts/PAP-*.md",
    "data/paper-intake/**/*.yaml",
    "data/paper-calibration/*.yaml",
    "data/customers/**/*.yaml",
    "data/dr-datareq/**/*.yaml",
    "appendices/*.tex",
    "chapters/*.tex",
]


def find_doubled_kurzwort_keys(bib_content):
    """Find all BibTeX keys with doubled kurzwort."""
    keys = re.findall(r'^@\w+\{([^,]+),', bib_content, re.MULTILINE)
    doubled = {}
    for k in keys:
        m = re.match(r'^([a-z]+)(\d{4})(.+)$', k)
        if m:
            kurzwort = m.group(3)
            for l in range(3, len(kurzwort) // 2 + 1):
                if kurzwort[:l] == kurzwort[l:2*l]:
                    correct = f"{m.group(1)}{m.group(2)}{kurzwort[:l]}"
                    doubled[k] = correct
                    break
    return doubled


def get_all_files_to_scan():
    """Get all files that might contain cross-references."""
    files = set()

    # Explicit files
    for rel_path in CROSS_REF_PATTERNS:
        p = PROJECT_ROOT / rel_path
        if p.exists():
            files.add(p)

    # Glob patterns
    for pattern in CROSS_REF_GLOBS:
        for p in PROJECT_ROOT.glob(pattern):
            if p.is_file():
                files.add(p)

    return sorted(files)


def fix_bib_keys(bib_content, rename_map, dry_run=True):
    """Rename doubled kurzwort keys in BibTeX content."""
    changes = 0
    result = bib_content

    for old_key, new_key in sorted(rename_map.items(), key=lambda x: -len(x[0])):
        # Replace the entry key definition
        pattern = re.compile(r'(@\w+\{)' + re.escape(old_key) + r'(,)')
        if pattern.search(result):
            if not dry_run:
                result = pattern.sub(r'\g<1>' + new_key + r'\2', result)
            changes += 1

    return result, changes


def fix_cross_references(file_path, rename_map, dry_run=True):
    """Fix all cross-references in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception:
        return 0

    original = content
    changes = 0

    # Sort by length (longest first) to avoid partial replacements
    for old_key, new_key in sorted(rename_map.items(), key=lambda x: -len(x[0])):
        # Replace the doubled key everywhere it appears
        if old_key in content:
            count = content.count(old_key)
            if not dry_run:
                content = content.replace(old_key, new_key)
            changes += count

    if changes > 0 and not dry_run and content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    return changes


def fix_pap_pap_prefix(files, dry_run=True):
    """Fix PAP-PAP- double prefix to PAP- in all files."""
    total_fixes = 0

    for fp in files:
        try:
            with open(fp, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
        except Exception:
            continue

        if 'PAP-PAP-' not in content:
            continue

        count = content.count('PAP-PAP-')
        if not dry_run:
            content = content.replace('PAP-PAP-', 'PAP-')
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(content)

        if count > 0:
            print(f"  PAP-PAP- fix: {fp.relative_to(PROJECT_ROOT)} ({count} occurrences)")
            total_fixes += count

    return total_fixes


def fix_pap_prefix_in_cite(files, dry_run=True):
    """Fix PAP- prefix in LaTeX \\cite commands (should be bare keys)."""
    total_fixes = 0

    for fp in files:
        if not str(fp).endswith('.tex'):
            continue

        try:
            with open(fp, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
        except Exception:
            continue

        original = content

        # Fix \cite{PAP-key}, \citep{PAP-key}, \citet{PAP-key}
        # Also handle multiple keys: \cite{PAP-key1, PAP-key2}
        def strip_pap_prefix(m):
            inner = m.group(2)
            # Strip PAP- from each key in comma-separated list
            keys = [k.strip() for k in inner.split(',')]
            fixed_keys = []
            for k in keys:
                if k.startswith('PAP-'):
                    fixed_keys.append(k[4:])  # Strip PAP-
                else:
                    fixed_keys.append(k)
            return m.group(1) + '{' + ', '.join(fixed_keys) + '}'

        pattern = re.compile(r'(\\cite[pt]*)\{([^}]*PAP-[^}]*)\}')
        content, n = pattern.subn(strip_pap_prefix, content)

        if n > 0:
            if not dry_run:
                with open(fp, 'w', encoding='utf-8') as f:
                    f.write(content)
            print(f"  PAP- in \\cite fix: {fp.relative_to(PROJECT_ROOT)} ({n} commands)")
            total_fixes += n

    return total_fixes


def fix_pap_prefix_in_bib_keys(theory_catalog_path, dry_run=True):
    """Fix PAP- prefix in theory-catalog bib_keys (should be bare keys)."""
    try:
        with open(theory_catalog_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return 0

    # Pattern: "PAP-keyname" in bib_keys arrays
    # Replace PAP- prefix in quoted bib_keys values
    pattern = re.compile(r'(bib_keys:\s*\[.*?)"PAP-([a-z]+\d{4}[a-z]+)"', re.DOTALL)

    # Actually, simpler: just replace "PAP- in bib_keys context
    # We need to be careful to only replace within bib_keys arrays
    original = content

    # Replace "PAP-xxx" with "xxx" when it appears as a bib_key value
    content = re.sub(r'"PAP-([a-z]+\d{4}[a-z]+)"', r'"\1"', content)

    changes = sum(1 for a, b in zip(original, content) if a != b) > 0
    count = original.count('"PAP-') - content.count('"PAP-')

    if count > 0:
        if not dry_run:
            with open(theory_catalog_path, 'w', encoding='utf-8') as f:
                f.write(content)
        print(f"  PAP- prefix in bib_keys: {theory_catalog_path.relative_to(PROJECT_ROOT)} ({count} fixes)")

    return count


def main():
    parser = argparse.ArgumentParser(description='Fix doubled kurzwort in BibTeX keys')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without applying')
    parser.add_argument('--execute', action='store_true', help='Apply all fixes')
    parser.add_argument('--limit', type=int, default=0, help='Limit number of keys to fix')
    parser.add_argument('--skip-doubled', action='store_true', help='Skip doubled kurzwort fix')
    parser.add_argument('--only-pap-prefix', action='store_true', help='Only fix PAP- prefix issues')

    args = parser.parse_args()

    if not args.dry_run and not args.execute:
        print("ERROR: Specify --dry-run or --execute")
        sys.exit(1)

    dry_run = args.dry_run
    mode = "DRY RUN" if dry_run else "EXECUTING"

    print(f"\n{'='*70}")
    print(f"  FIX DOUBLED KURZWORT + PAP- PREFIX ISSUES ({mode})")
    print(f"{'='*70}\n")

    # Read BibTeX
    with open(BIB_PATH, 'r', encoding='utf-8', errors='replace') as f:
        bib_content = f.read()

    # Get all files to scan
    all_files = get_all_files_to_scan()
    print(f"  Files to scan: {len(all_files)}")

    total_changes = 0

    # === PHASE 1: Fix doubled kurzwort ===
    if not args.only_pap_prefix:
        doubled = find_doubled_kurzwort_keys(bib_content)

        if args.limit > 0:
            items = list(doubled.items())[:args.limit]
            doubled = dict(items)

        print(f"\n  Phase 1: Doubled kurzwort keys to fix: {len(doubled)}")

        if doubled:
            # Fix BibTeX
            bib_content, bib_changes = fix_bib_keys(bib_content, doubled, dry_run)
            print(f"  BibTeX keys renamed: {bib_changes}")
            total_changes += bib_changes

            if not dry_run:
                with open(BIB_PATH, 'w', encoding='utf-8') as f:
                    f.write(bib_content)

            # Fix cross-references
            xref_changes = 0
            for fp in all_files:
                n = fix_cross_references(fp, doubled, dry_run)
                if n > 0:
                    print(f"  XRef fix: {fp.relative_to(PROJECT_ROOT)} ({n} replacements)")
                    xref_changes += n

            print(f"  Cross-reference fixes: {xref_changes}")
            total_changes += xref_changes

    # === PHASE 2: Fix PAP-PAP- double prefix ===
    print(f"\n  Phase 2: Fix PAP-PAP- double prefix")
    pap_pap_fixes = fix_pap_pap_prefix(all_files, dry_run)
    print(f"  PAP-PAP- fixes: {pap_pap_fixes}")
    total_changes += pap_pap_fixes

    # === PHASE 3: Fix PAP- prefix in LaTeX \cite commands ===
    print(f"\n  Phase 3: Fix PAP- prefix in LaTeX \\cite commands")
    cite_fixes = fix_pap_prefix_in_cite(all_files, dry_run)
    print(f"  LaTeX cite fixes: {cite_fixes}")
    total_changes += cite_fixes

    # === PHASE 4: Fix PAP- prefix in theory-catalog bib_keys ===
    print(f"\n  Phase 4: Fix PAP- prefix in theory-catalog bib_keys")
    tc_path = PROJECT_ROOT / "data" / "theory-catalog.yaml"
    tc_fixes = fix_pap_prefix_in_bib_keys(tc_path, dry_run)
    print(f"  Theory-catalog bib_keys fixes: {tc_fixes}")
    total_changes += tc_fixes

    # === SUMMARY ===
    print(f"\n{'='*70}")
    print(f"  TOTAL CHANGES: {total_changes}")
    if dry_run:
        print(f"  (DRY RUN - no files modified)")
        print(f"  Run with --execute to apply changes")
    else:
        print(f"  All changes applied successfully")
    print(f"{'='*70}\n")


if __name__ == '__main__':
    main()
