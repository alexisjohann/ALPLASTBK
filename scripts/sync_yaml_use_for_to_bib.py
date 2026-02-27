#!/usr/bin/env python3
"""
Sync use_for tags from Paper-YAML → bcm_master.bib (reverse direction).

Finds tags present in YAML ebf_integration.use_for but missing from
the BibTeX use_for field, and adds them.

Usage:
    python scripts/sync_yaml_use_for_to_bib.py [--dry-run] [--limit N]
"""

import re
import os
import sys
import glob
import yaml

BIB_PATH = os.path.join(os.path.dirname(__file__), '..', 'bibliography', 'bcm_master.bib')
YAML_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'paper-references')


def parse_bib_use_for(bib_path):
    """Extract (key, use_for_set) from all BibTeX entries."""
    with open(bib_path, 'r', encoding='utf-8') as f:
        content = f.read()

    entries = {}
    entry_pattern = re.compile(r'@\w+\{(\S+?),\s*\n(.*?)(?=\n@|\Z)', re.DOTALL)
    for m in entry_pattern.finditer(content):
        key = m.group(1)
        body = m.group(2)
        uf_match = re.search(r'use_for\s*=\s*\{([^}]*)\}', body)
        if uf_match:
            tags = [t.strip() for t in uf_match.group(1).split(',') if t.strip()]
            entries[key] = set(tags)
    return entries


def add_tag_to_bib(content, bib_key, new_tags):
    """Add tags to a BibTeX entry's use_for field."""
    pattern = re.compile(
        r'(@\w+\{' + re.escape(bib_key) + r',.*?(?=\n@|\Z))',
        re.DOTALL
    )
    match = pattern.search(content)
    if not match:
        return content, False

    entry = match.group(0)
    use_for_pattern = re.compile(r'(use_for\s*=\s*\{)([^}]*?)(\})')
    uf_match = use_for_pattern.search(entry)
    if not uf_match:
        return content, False

    existing = uf_match.group(2).strip()
    additions = ', '.join(sorted(new_tags))
    if existing:
        new_val = existing + ', ' + additions
    else:
        new_val = additions

    new_entry = entry[:uf_match.start()] + \
                uf_match.group(1) + new_val + uf_match.group(3) + \
                entry[uf_match.end():]

    content = content[:match.start()] + new_entry + content[match.end():]
    return content, True


def main():
    dry_run = '--dry-run' in sys.argv
    limit = None
    for i, arg in enumerate(sys.argv):
        if arg == '--limit' and i + 1 < len(sys.argv):
            limit = int(sys.argv[i + 1])

    print("Parsing BibTeX use_for fields...")
    bib_entries = parse_bib_use_for(BIB_PATH)
    print(f"  Found {len(bib_entries)} entries with use_for\n")

    yaml_files = sorted(glob.glob(os.path.join(YAML_DIR, 'PAP-*.yaml')))
    print(f"Found {len(yaml_files)} YAML files\n")

    with open(BIB_PATH, 'r', encoding='utf-8') as f:
        bib_content = f.read()

    stats = {'checked': 0, 'updated': 0, 'tags_added': 0, 'errors': 0,
             'already_sync': 0, 'no_use_for': 0, 'missing_bib': 0}

    updates = []

    for yf in yaml_files:
        fname = os.path.basename(yf)
        bib_key = fname.replace('PAP-', '').replace('.yaml', '')

        if bib_key not in bib_entries:
            stats['missing_bib'] += 1
            continue

        try:
            with open(yf, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        except Exception:
            stats['errors'] += 1
            continue

        if not data or 'ebf_integration' not in data:
            stats['no_use_for'] += 1
            continue

        yaml_tags = set(data.get('ebf_integration', {}).get('use_for', []) or [])
        bib_tags = bib_entries[bib_key]

        # Tags in YAML but not in BibTeX
        missing_in_bib = yaml_tags - bib_tags

        stats['checked'] += 1

        if not missing_in_bib:
            stats['already_sync'] += 1
            continue

        updates.append((bib_key, missing_in_bib))
        if limit and len(updates) >= limit:
            break

    print(f"{'='*60}")
    print(f"  YAML → BibTeX: {len(updates)} entries need updates")
    print(f"{'='*60}\n")

    for bib_key, missing in updates:
        tags_str = ', '.join(sorted(missing))
        print(f"  {'🔍' if dry_run else '✅'} {bib_key}: +{len(missing)} tags ({tags_str})")
        stats['tags_added'] += len(missing)

        if not dry_run:
            bib_content, changed = add_tag_to_bib(bib_content, bib_key, missing)
            if changed:
                stats['updated'] += 1
            else:
                print(f"     ⚠️  Could not update BibTeX entry")
                stats['errors'] += 1
        else:
            stats['updated'] += 1

    if not dry_run and stats['updated'] > 0:
        with open(BIB_PATH, 'w', encoding='utf-8') as f:
            f.write(bib_content)
        print(f"\n  ✅ Written to {BIB_PATH}")

    print(f"\n{'='*60}")
    print(f"  SUMMARY")
    print(f"{'='*60}")
    print(f"  Checked:        {stats['checked']}")
    print(f"  Already in sync:{stats['already_sync']}")
    print(f"  Updated:        {stats['updated']}")
    print(f"  Tags added:     {stats['tags_added']}")
    print(f"  Missing in BIB: {stats['missing_bib']}")
    print(f"  Errors:         {stats['errors']}")

    if dry_run:
        print(f"\n  🔍 DRY RUN — no changes written")


if __name__ == '__main__':
    main()
