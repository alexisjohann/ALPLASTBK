#!/usr/bin/env python3
"""
Sync use_for tags from bcm_master.bib → Paper-YAML files.

Compares use_for fields between BibTeX and YAML, adds missing tags
from BibTeX to YAML. Focuses on CORE-* tags but syncs all use_for entries.

Usage:
    python scripts/sync_bib_use_for_to_yaml.py [--dry-run] [--limit N] [--only-core]
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
    # Find all entries
    entry_pattern = re.compile(r'@\w+\{(\S+?),\s*\n(.*?)(?=\n@|\Z)', re.DOTALL)
    for m in entry_pattern.finditer(content):
        key = m.group(1)
        body = m.group(2)

        # Extract use_for
        uf_match = re.search(r'use_for\s*=\s*\{([^}]*)\}', body)
        if uf_match:
            tags = [t.strip() for t in uf_match.group(1).split(',') if t.strip()]
            entries[key] = set(tags)

    return entries


def load_yaml(path):
    """Load a YAML file safely."""
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def save_yaml_use_for(path, new_tags):
    """Add missing use_for tags to a YAML file by text manipulation.

    We use text manipulation instead of yaml.dump to preserve formatting,
    comments, and field order.
    """
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Find the use_for section under ebf_integration
    in_ebf = False
    use_for_start = -1
    use_for_end = -1

    for i, line in enumerate(lines):
        stripped = line.rstrip()

        if stripped.startswith('ebf_integration:'):
            in_ebf = True
            continue

        if in_ebf and stripped.strip().startswith('use_for:'):
            use_for_start = i
            # Find existing entries (lines starting with "  - " under use_for)
            j = i + 1
            while j < len(lines):
                next_line = lines[j].rstrip()
                # Check if this is a use_for list item (indented with "  - ")
                if re.match(r'^    - ', next_line) or re.match(r'^  - ', next_line):
                    j += 1
                elif next_line.strip() == '':
                    j += 1  # skip blank lines within list
                else:
                    break
            use_for_end = j
            break

        # If we hit another top-level key, reset
        if in_ebf and not line.startswith(' ') and line.strip() and not line.startswith('#'):
            in_ebf = False

    if use_for_start == -1:
        return False

    # Determine indentation by looking at existing entries
    indent = '  - '  # default
    for k in range(use_for_start + 1, use_for_end):
        m = re.match(r'^(\s+- )', lines[k])
        if m:
            indent = m.group(1)
            break

    # Add new tags before use_for_end
    insert_lines = []
    for tag in sorted(new_tags):
        insert_lines.append(f'{indent}{tag}\n')

    # Insert new lines
    lines = lines[:use_for_end] + insert_lines + lines[use_for_end:]

    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    return True


def main():
    dry_run = '--dry-run' in sys.argv
    only_core = '--only-core' in sys.argv
    limit = None
    for i, arg in enumerate(sys.argv):
        if arg == '--limit' and i + 1 < len(sys.argv):
            limit = int(sys.argv[i + 1])

    print("Parsing BibTeX use_for fields...")
    bib_entries = parse_bib_use_for(BIB_PATH)
    print(f"  Found {len(bib_entries)} entries with use_for\n")

    # Scan YAML files
    yaml_files = sorted(glob.glob(os.path.join(YAML_DIR, 'PAP-*.yaml')))
    print(f"Found {len(yaml_files)} YAML files\n")

    stats = {'checked': 0, 'updated': 0, 'missing_yaml': 0, 'missing_bib': 0,
             'already_sync': 0, 'no_use_for_yaml': 0, 'errors': 0,
             'tags_added': 0}

    updates = []

    for yf in yaml_files:
        fname = os.path.basename(yf)
        # Extract bib key from filename: PAP-{key}.yaml -> key
        bib_key = fname.replace('PAP-', '').replace('.yaml', '')

        if bib_key not in bib_entries:
            stats['missing_bib'] += 1
            continue

        bib_tags = bib_entries[bib_key]

        # Load YAML
        try:
            data = load_yaml(yf)
        except Exception as e:
            stats['errors'] += 1
            continue

        if not data or 'ebf_integration' not in data:
            stats['no_use_for_yaml'] += 1
            continue

        ebf = data.get('ebf_integration', {})
        yaml_tags = set(ebf.get('use_for', []) or [])

        # Find tags in BibTeX but not in YAML
        if only_core:
            missing = {t for t in bib_tags - yaml_tags if t.startswith('CORE-')}
        else:
            missing = bib_tags - yaml_tags

        stats['checked'] += 1

        if not missing:
            stats['already_sync'] += 1
            continue

        updates.append((yf, bib_key, missing, yaml_tags))

        if limit and len(updates) >= limit:
            break

    # Apply updates
    print(f"{'='*60}")
    print(f"  SYNC RESULTS: {len(updates)} files need updates")
    print(f"{'='*60}\n")

    for yf, bib_key, missing, yaml_tags in updates:
        missing_str = ', '.join(sorted(missing))
        print(f"  {'🔍' if dry_run else '✅'} {bib_key}: +{len(missing)} tags ({missing_str})")
        stats['tags_added'] += len(missing)

        if not dry_run:
            try:
                success = save_yaml_use_for(yf, missing)
                if success:
                    stats['updated'] += 1
                else:
                    print(f"     ⚠️  Could not find use_for section")
                    stats['errors'] += 1
            except Exception as e:
                print(f"     ❌ Error: {e}")
                stats['errors'] += 1
        else:
            stats['updated'] += 1

    print(f"\n{'='*60}")
    print(f"  SUMMARY")
    print(f"{'='*60}")
    print(f"  Checked:        {stats['checked']}")
    print(f"  Already in sync:{stats['already_sync']}")
    print(f"  Updated:        {stats['updated']}")
    print(f"  Tags added:     {stats['tags_added']}")
    print(f"  Missing in BIB: {stats['missing_bib']}")
    print(f"  No use_for:     {stats['no_use_for_yaml']}")
    print(f"  Errors:         {stats['errors']}")

    if dry_run:
        print(f"\n  🔍 DRY RUN — no changes written")
    elif stats['updated'] > 0:
        print(f"\n  ✅ {stats['updated']} YAML files updated")


if __name__ == '__main__':
    main()
