#!/usr/bin/env python3
"""
Deduplicate BibTeX entries in bcm_master.bib.

Strategy for each duplicate group:
1. Prefer entry WITH journal (published) over without (working paper)
2. Prefer entry WITH DOI over without
3. Prefer entry WITHOUT auto_imported_mpg_pure (manually curated)
4. Prefer entry with more fields (richer metadata)
5. Keep the one with the latest year (published version > working paper)

For each duplicate group, keeps exactly ONE entry and removes the rest.

Usage:
    python scripts/deduplicate_sutter_import.py --dry-run
    python scripts/deduplicate_sutter_import.py
"""

import argparse
import re
import sys
from collections import defaultdict


def parse_entries(content):
    """Parse BibTeX content into list of entry dicts."""
    entries = []
    # Match complete entries
    for m in re.finditer(r'(@\w+\{[^,]+,.*?\n\})', content, re.DOTALL):
        full_text = m.group(1)
        start = m.start()

        type_m = re.match(r'@(\w+)\{([^,]+),', full_text)
        if not type_m:
            continue

        entry_type = type_m.group(1).strip()
        key = type_m.group(2).strip()

        title_m = re.search(r'title\s*=\s*\{([^}]+)\}', full_text)
        title = title_m.group(1).strip() if title_m else ''
        title_norm = re.sub(r'[^a-z0-9\s]', '', title.lower()).strip()
        title_norm = re.sub(r'\s+', ' ', title_norm)

        doi_m = re.search(r'doi\s*=\s*\{([^}]+)\}', full_text)
        doi = doi_m.group(1).strip() if doi_m else ''

        journal_m = re.search(r'journal\s*=\s*\{([^}]+)\}', full_text)
        journal = journal_m.group(1).strip() if journal_m else ''

        year_m = re.search(r'year\s*=\s*\{(\d+)\}', full_text)
        year = int(year_m.group(1)) if year_m else 0

        is_auto = 'auto_imported_mpg_pure' in full_text
        has_abstract = 'abstract = {' in full_text

        # Count meaningful fields
        field_count = len(re.findall(r'^\s+\w+\s*=\s*\{', full_text, re.MULTILINE))

        entries.append({
            'key': key,
            'type': entry_type,
            'title': title,
            'title_norm': title_norm,
            'doi': doi,
            'journal': journal,
            'year': year,
            'is_auto': is_auto,
            'has_abstract': has_abstract,
            'field_count': field_count,
            'full_text': full_text,
            'start': start,
        })

    return entries


def score_entry(entry):
    """Score an entry - higher is better (should be kept)."""
    score = 0

    # Prefer manually curated over auto-imported
    if not entry['is_auto']:
        score += 100

    # Prefer entries with journal
    if entry['journal']:
        score += 50

    # Prefer entries with DOI
    if entry['doi']:
        score += 30

    # Prefer entries with abstract
    if entry['has_abstract']:
        score += 20

    # Prefer more fields (richer metadata)
    score += entry['field_count'] * 2

    # Prefer article over other types
    if entry['type'] == 'article':
        score += 10

    # Slightly prefer later year (published version)
    score += min(entry['year'] - 2000, 30) if entry['year'] > 2000 else 0

    return score


def main():
    parser = argparse.ArgumentParser(description="Deduplicate BibTeX entries")
    parser.add_argument("--input", default="bibliography/bcm_master.bib",
                        help="BibTeX file to deduplicate")
    parser.add_argument("--dry-run", action="store_true",
                        help="Report only, don't modify file")
    args = parser.parse_args()

    with open(args.input, 'r', encoding='utf-8') as f:
        content = f.read()

    entries = parse_entries(content)
    print(f"Total entries parsed: {len(entries)}")

    # Group by normalized title
    groups = defaultdict(list)
    for e in entries:
        if e['title_norm'] and len(e['title_norm']) > 10:
            groups[e['title_norm']].append(e)

    # Find duplicates
    dupes = {t: es for t, es in groups.items() if len(es) > 1}
    print(f"Duplicate groups: {len(dupes)}")

    if not dupes:
        print("No duplicates found.")
        return

    # Decide which to keep and which to remove
    to_remove = []
    kept_count = 0

    for title_norm, group_entries in sorted(dupes.items()):
        # Score each entry
        scored = [(score_entry(e), e) for e in group_entries]
        scored.sort(key=lambda x: -x[0])

        keep = scored[0][1]
        remove = [e for _, e in scored[1:]]

        kept_count += 1
        to_remove.extend(remove)

        if args.dry_run:
            print(f"\n  KEEP: {keep['key']} (score={scored[0][0]}, "
                  f"journal={keep['journal'][:30] if keep['journal'] else 'none'}, "
                  f"auto={keep['is_auto']})")
            for _, e in scored[1:]:
                print(f"  DROP: {e['key']} (score={score_entry(e)}, "
                      f"journal={e['journal'][:30] if e['journal'] else 'none'}, "
                      f"auto={e['is_auto']})")

    print(f"\n=== SUMMARY ===")
    print(f"Entries to KEEP: {kept_count} (best of each group)")
    print(f"Entries to REMOVE: {len(to_remove)}")
    print(f"Final count: {len(entries) - len(to_remove)}")

    # Breakdown
    auto_removed = sum(1 for e in to_remove if e['is_auto'])
    manual_removed = sum(1 for e in to_remove if not e['is_auto'])
    print(f"  Auto-imported removed: {auto_removed}")
    print(f"  Manual removed: {manual_removed}")

    if args.dry_run:
        print("\n[DRY RUN] No changes made.")
        return

    # Remove duplicates from content
    # Sort by position in file (reverse) to remove from end first
    to_remove_texts = set(e['full_text'] for e in to_remove)

    new_content = content
    removed = 0
    for entry_text in to_remove_texts:
        if entry_text in new_content:
            new_content = new_content.replace(entry_text, '', 1)
            removed += 1

    # Clean up multiple blank lines
    new_content = re.sub(r'\n{3,}', '\n\n', new_content)

    with open(args.input, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"\nRemoved {removed} duplicate entries from {args.input}")

    # Verify
    with open(args.input, 'r', encoding='utf-8') as f:
        verify_content = f.read()
    final_count = len(re.findall(r'^@\w+\{', verify_content, re.MULTILINE))
    print(f"Final entry count: {final_count}")


if __name__ == "__main__":
    main()
