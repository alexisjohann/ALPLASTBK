#!/usr/bin/env python3
"""
Sync theory_support from BibTeX → Paper-YAMLs.

Reads theory_support from bcm_master.bib and writes/updates
the ebf_integration.theory_support field in Paper-YAML files.

Usage:
    python scripts/sync_bib_theory_to_yaml.py [--dry-run] [--limit N]
"""

import re
import os
import sys
import glob

BIB_PATH = os.path.join(os.path.dirname(__file__), '..', 'bibliography', 'bcm_master.bib')
YAML_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'paper-references')


def parse_bib_theory_support(bib_path):
    """Extract (key, theory_list) from all BibTeX entries with theory_support."""
    with open(bib_path, 'r', encoding='utf-8') as f:
        content = f.read()

    entries = {}
    entry_pattern = re.compile(r'@\w+\{(\S+?),\s*\n(.*?)(?=\n@|\Z)', re.DOTALL)
    for m in entry_pattern.finditer(content):
        key = m.group(1)
        body = m.group(2)
        ts_match = re.search(r'theory_support\s*=\s*\{([^}]*)\}', body)
        if ts_match:
            raw = ts_match.group(1).strip()
            if raw:
                tags = [t.strip() for t in raw.split(',') if t.strip()]
                entries[key] = tags
    return entries


def read_yaml_text(path):
    """Read YAML file as text."""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def get_yaml_theory_support(text):
    """Extract current theory_support from YAML text."""
    # Match theory_support as a list
    match = re.search(r'theory_support:\s*\n((?:\s+-\s+\S+\n?)*)', text)
    if match:
        items = re.findall(r'-\s+(\S+)', match.group(1))
        return set(items)

    # Match theory_support as a single string
    match = re.search(r'theory_support:\s+(.+)', text)
    if match:
        val = match.group(1).strip()
        if val and val != 'null' and val != '~':
            # Could be comma-separated or single
            return set(t.strip().strip("'\"") for t in val.split(',') if t.strip())

    return set()


def add_theory_support_to_yaml(text, theories):
    """Add theory_support field to YAML under ebf_integration."""
    theories_sorted = sorted(theories)

    # Check if theory_support already exists
    if re.search(r'theory_support:', text):
        # Replace existing
        # Find the theory_support section and replace
        # Handle list format
        match = re.search(r'(  theory_support:\s*\n(?:\s+-\s+\S+\n?)*)', text)
        if match:
            new_section = '  theory_support:\n' + \
                         ''.join(f'  - {t}\n' for t in theories_sorted)
            return text[:match.start()] + new_section + text[match.end():]

        # Handle single-value format
        match = re.search(r'(  theory_support:\s+.+\n)', text)
        if match:
            new_section = '  theory_support:\n' + \
                         ''.join(f'  - {t}\n' for t in theories_sorted)
            return text[:match.start()] + new_section + text[match.end():]

    # theory_support doesn't exist — add after use_for section or after ebf_integration
    # Try to find end of use_for list
    use_for_end = None
    for m in re.finditer(r'  use_for:\s*\n((?:\s+-\s+.+\n)*)', text):
        use_for_end = m.end()

    if use_for_end:
        new_section = '  theory_support:\n' + \
                     ''.join(f'  - {t}\n' for t in theories_sorted)
        return text[:use_for_end] + new_section + text[use_for_end:]

    # Try after ebf_integration line
    match = re.search(r'(ebf_integration:\s*\n)', text)
    if match:
        insert_pos = match.end()
        new_section = '  theory_support:\n' + \
                     ''.join(f'  - {t}\n' for t in theories_sorted)
        return text[:insert_pos] + new_section + text[insert_pos:]

    return None  # Can't find insertion point


def main():
    dry_run = '--dry-run' in sys.argv
    limit = None
    for i, arg in enumerate(sys.argv):
        if arg == '--limit' and i + 1 < len(sys.argv):
            limit = int(sys.argv[i + 1])

    print("Parsing BibTeX theory_support fields...")
    bib_theories = parse_bib_theory_support(BIB_PATH)
    print(f"  Found {len(bib_theories)} entries with theory_support\n")

    yaml_files = sorted(glob.glob(os.path.join(YAML_DIR, 'PAP-*.yaml')))
    print(f"Found {len(yaml_files)} YAML files\n")

    stats = {'checked': 0, 'updated': 0, 'already_sync': 0,
             'no_bib': 0, 'no_ebf': 0, 'errors': 0}

    updates = []

    for yf in yaml_files:
        fname = os.path.basename(yf)
        bib_key = fname.replace('PAP-', '').replace('.yaml', '')

        if bib_key not in bib_theories:
            stats['no_bib'] += 1
            continue

        text = read_yaml_text(yf)

        if 'ebf_integration' not in text:
            stats['no_ebf'] += 1
            continue

        stats['checked'] += 1

        bib_tags = set(bib_theories[bib_key])
        yaml_tags = get_yaml_theory_support(text)

        missing = bib_tags - yaml_tags
        if not missing:
            stats['already_sync'] += 1
            continue

        # All BibTeX theories should be in YAML
        all_theories = yaml_tags | bib_tags
        updates.append((yf, bib_key, all_theories, len(missing)))

        if limit and len(updates) >= limit:
            break

    print(f"{'='*60}")
    print(f"  BibTeX → YAML theory_support: {len(updates)} files need updates")
    print(f"{'='*60}\n")

    for yf, bib_key, theories, n_missing in updates:
        icon = '🔍' if dry_run else '✅'
        theories_str = ', '.join(sorted(theories))
        print(f"  {icon} {bib_key}: +{n_missing} → [{theories_str}]")

        if not dry_run:
            text = read_yaml_text(yf)
            new_text = add_theory_support_to_yaml(text, theories)
            if new_text:
                with open(yf, 'w', encoding='utf-8') as f:
                    f.write(new_text)
                stats['updated'] += 1
            else:
                print(f"     ⚠️  Could not update")
                stats['errors'] += 1
        else:
            stats['updated'] += 1

    print(f"\n{'='*60}")
    print(f"  SUMMARY")
    print(f"{'='*60}")
    print(f"  Checked:        {stats['checked']}")
    print(f"  Already in sync:{stats['already_sync']}")
    print(f"  Updated:        {stats['updated']}")
    print(f"  No BibTeX match:{stats['no_bib']}")
    print(f"  No ebf_integr.: {stats['no_ebf']}")
    print(f"  Errors:         {stats['errors']}")

    if dry_run:
        print(f"\n  🔍 DRY RUN — no changes written")


if __name__ == '__main__':
    main()
