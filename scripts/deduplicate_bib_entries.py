#!/usr/bin/env python3
"""
Deduplicate BIB entries by title.

For each group of duplicate titles:
1. Choose the "best" entry (most fields, has PAP- prefix, has DOI)
2. Remove duplicate entries from BIB
3. Update references in YAML/TEX/MD files
4. Handle PAP-*.yaml files (rename/merge)

Usage:
  python scripts/deduplicate_bib_entries.py --analyze          # Show duplicates
  python scripts/deduplicate_bib_entries.py --batch N          # Process N groups
  python scripts/deduplicate_bib_entries.py --batch N --apply  # Actually apply changes
"""

import re
import os
import sys
import glob
import argparse
from collections import defaultdict


BIB_FILE = "bibliography/bcm_master.bib"
PAPER_REFS_DIR = "data/paper-references"
SKIP_TITLE = "Title to be added"  # Placeholder entries handled separately


def parse_bib(content):
    """Parse BIB file into dict of key -> (entry_text, fields_dict)."""
    entries = {}
    for match in re.finditer(
        r'^(@\w+\{([^,]+),\s*\n)(.*?)(^\})',
        content, re.MULTILINE | re.DOTALL
    ):
        header = match.group(1)
        key = match.group(2).strip()
        body = match.group(3)
        closing = match.group(4)
        full_text = match.group(0)

        fields = {}
        for fm in re.finditer(r'^\s+(\w+)\s*=\s*\{([^}]*)\}', body, re.MULTILINE):
            fields[fm.group(1)] = fm.group(2).strip()

        entries[key] = {
            'full_text': full_text,
            'fields': fields,
            'header': header,
            'body': body,
        }
    return entries


def find_duplicates(entries):
    """Find groups of entries with the same normalized title."""
    norm_to_keys = defaultdict(list)
    for key, data in entries.items():
        title = data['fields'].get('title', '')
        if title == SKIP_TITLE or not title:
            continue
        normalized = re.sub(r'[^\w\s]', '', title.lower())
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        if normalized:
            norm_to_keys[normalized].append(key)

    return {norm: keys for norm, keys in norm_to_keys.items()
            if len(keys) > 1}


def score_entry(key, data):
    """Score an entry for quality. Higher = better."""
    fields = data['fields']
    score = 0

    # PAP- prefix preferred (SSOT naming)
    if key.startswith('PAP-'):
        score += 10

    # DOI is valuable
    if fields.get('doi'):
        score += 5

    # More fields = more complete
    score += len(fields)

    # Journal/publisher
    if fields.get('journal') or fields.get('publisher'):
        score += 3

    # Volume/pages = more complete
    if fields.get('volume'):
        score += 1
    if fields.get('pages'):
        score += 1

    # ebf_reference_count > 0 means it's referenced
    ref_count = fields.get('ebf_reference_count', '0')
    try:
        if int(ref_count) > 0:
            score += 2
    except ValueError:
        pass

    return score


def choose_best(keys, entries):
    """Choose the best entry from a group of duplicates."""
    scored = [(score_entry(k, entries[k]), k) for k in keys]
    scored.sort(reverse=True)
    return scored[0][1], [k for _, k in scored[1:]]


def find_references(key, search_dirs=None):
    """Find all files that reference a BIB key."""
    if search_dirs is None:
        search_dirs = ['.']

    refs = []
    patterns = ['*.yaml', '*.yml', '*.tex', '*.md', '*.py']

    for sdir in search_dirs:
        for pattern in patterns:
            for filepath in glob.glob(os.path.join(sdir, '**', pattern), recursive=True):
                if '.git' in filepath:
                    continue
                if filepath == BIB_FILE:
                    continue
                try:
                    with open(filepath, 'r', errors='replace') as f:
                        content = f.read()
                    if key in content:
                        refs.append(filepath)
                except (IOError, UnicodeDecodeError):
                    pass
    return refs


def apply_dedup_group(best_key, remove_keys, entries, bib_content, dry_run=True):
    """Apply deduplication for one group."""
    changes = []

    # 1. Find all references to remove_keys
    for old_key in remove_keys:
        ref_files = find_references(old_key)
        for filepath in ref_files:
            if not dry_run:
                with open(filepath, 'r', errors='replace') as f:
                    content = f.read()
                new_content = content.replace(old_key, best_key)
                if new_content != content:
                    with open(filepath, 'w') as f:
                        f.write(new_content)
                    changes.append(f"  UPDATED: {filepath} ({old_key} -> {best_key})")
            else:
                changes.append(f"  WOULD UPDATE: {filepath} ({old_key} -> {best_key})")

    # 2. Remove old BIB entries
    for old_key in remove_keys:
        old_entry = entries[old_key]['full_text']
        if old_entry in bib_content:
            if not dry_run:
                bib_content = bib_content.replace(old_entry + '\n\n', '')
                bib_content = bib_content.replace(old_entry + '\n', '')
                bib_content = bib_content.replace(old_entry, '')
            changes.append(f"  {'REMOVED' if not dry_run else 'WOULD REMOVE'} BIB: {old_key}")

    # 3. Handle PAP-*.yaml files
    for old_key in remove_keys:
        pap_key = old_key if old_key.startswith('PAP-') else f'PAP-{old_key}'
        yaml_path = os.path.join(PAPER_REFS_DIR, f'{pap_key}.yaml')
        if os.path.exists(yaml_path):
            best_pap = best_key if best_key.startswith('PAP-') else f'PAP-{best_key}'
            best_yaml = os.path.join(PAPER_REFS_DIR, f'{best_pap}.yaml')
            if yaml_path != best_yaml:
                if not dry_run:
                    # Don't delete — just note it for manual review
                    pass
                changes.append(f"  {'NOTE' if not dry_run else 'WOULD NOTE'}: {yaml_path} is duplicate of {best_yaml}")

    return bib_content, changes


def main():
    parser = argparse.ArgumentParser(description='Deduplicate BIB entries')
    parser.add_argument('--analyze', action='store_true', help='Show duplicate analysis')
    parser.add_argument('--batch', type=int, default=0, help='Process N groups')
    parser.add_argument('--apply', action='store_true', help='Actually apply changes')
    parser.add_argument('--group', type=int, help='Process specific group number')
    args = parser.parse_args()

    with open(BIB_FILE, 'r') as f:
        bib_content = f.read()

    entries = parse_bib(bib_content)
    duplicates = find_duplicates(entries)

    if args.analyze or (not args.batch and not args.group):
        print(f"Total BIB entries: {len(entries)}")
        print(f"Duplicate groups (excl. placeholders): {len(duplicates)}")
        total_removable = sum(len(keys) - 1 for keys in duplicates.values())
        print(f"Entries to remove: {total_removable}")
        print()

        for i, (norm, keys) in enumerate(sorted(duplicates.items()), 1):
            best = choose_best(keys, entries)[0]
            title = entries[keys[0]]['fields'].get('title', '?')[:70]
            print(f"Group {i}: {title}")
            for k in keys:
                marker = " ★" if k == best else "  "
                fields_count = len(entries[k]['fields'])
                has_doi = "DOI" if entries[k]['fields'].get('doi') else "   "
                print(f"  {marker} {k} ({fields_count} fields, {has_doi})")
        return

    # Process groups
    groups = sorted(duplicates.items())
    if args.group:
        groups = [groups[args.group - 1]]
    elif args.batch:
        groups = groups[:args.batch]

    dry_run = not args.apply
    mode = "DRY RUN" if dry_run else "APPLYING"
    print(f"=== {mode}: Processing {len(groups)} groups ===\n")

    total_removed = 0
    for i, (norm, keys) in enumerate(groups, 1):
        best_key, remove_keys = choose_best(keys, entries)
        title = entries[keys[0]]['fields'].get('title', '?')[:70]
        print(f"Group {i}: {title}")
        print(f"  KEEP: {best_key} (score: {score_entry(best_key, entries[best_key])})")
        for k in remove_keys:
            print(f"  REMOVE: {k} (score: {score_entry(k, entries[k])})")

        bib_content, changes = apply_dedup_group(
            best_key, remove_keys, entries, bib_content, dry_run=dry_run
        )
        for c in changes:
            print(c)
        total_removed += len(remove_keys)
        print()

    if not dry_run:
        # Clean up multiple blank lines
        bib_content = re.sub(r'\n{3,}', '\n\n', bib_content)
        with open(BIB_FILE, 'w') as f:
            f.write(bib_content)
        print(f"\n=== APPLIED: Removed {total_removed} duplicate entries ===")
    else:
        print(f"\n=== DRY RUN: Would remove {total_removed} entries ===")
        print(f"Run with --apply to execute changes")


if __name__ == '__main__':
    main()
