#!/usr/bin/env python3
"""
Deduplicate BibTeX Entries
==========================
Removes duplicate entries, keeping the most complete version.

Usage:
    python scripts/deduplicate_bibtex.py              # Dry run
    python scripts/deduplicate_bibtex.py --apply      # Apply changes
"""

import re
import argparse
from pathlib import Path
from collections import defaultdict

SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
BIB_FILE = ROOT_DIR / "bibliography" / "bcm_master.bib"


def parse_entries(content: str) -> list:
    """Parse BibTeX file into list of entries."""
    entries = []

    # Match each entry
    pattern = r'(@\w+\{[^@]+)'
    matches = re.findall(pattern, content, re.DOTALL)

    for match in matches:
        # Extract key
        key_match = re.match(r'@\w+\{([^,]+),', match)
        if key_match:
            key = key_match.group(1).strip()
            entries.append({
                'key': key,
                'raw': match.strip(),
                'has_doi': bool(re.search(r'^\s*doi\s*=', match, re.MULTILINE | re.IGNORECASE)),
                'field_count': len(re.findall(r'^\s*\w+\s*=', match, re.MULTILINE))
            })

    return entries


def score_entry(entry: dict) -> int:
    """Score an entry - higher is better."""
    score = entry['field_count']
    if entry['has_doi']:
        score += 100  # Strongly prefer entries with DOI
    return score


def main():
    parser = argparse.ArgumentParser(description='Deduplicate BibTeX entries')
    parser.add_argument('--apply', action='store_true', help='Apply changes')
    args = parser.parse_args()

    with open(BIB_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    entries = parse_entries(content)
    print(f"Total entries found: {len(entries)}")

    # Group by key
    by_key = defaultdict(list)
    for entry in entries:
        by_key[entry['key']].append(entry)

    # Find duplicates
    duplicates = {k: v for k, v in by_key.items() if len(v) > 1}
    print(f"Duplicate keys found: {len(duplicates)}")

    if not duplicates:
        print("No duplicates to remove!")
        return

    # For each duplicate, keep the best entry
    to_remove = []
    print("\nDuplicate analysis:")
    print("-" * 70)

    for key, entries_list in sorted(duplicates.items()):
        print(f"\n{key} ({len(entries_list)} copies):")

        # Score each entry
        scored = [(score_entry(e), e) for e in entries_list]
        scored.sort(key=lambda x: -x[0])  # Highest first

        best_score, best_entry = scored[0]

        for score, entry in scored:
            marker = "KEEP" if entry == best_entry else "REMOVE"
            doi_marker = "✓DOI" if entry['has_doi'] else "no-DOI"
            print(f"  [{marker}] fields={entry['field_count']:2d} {doi_marker}")

        # Mark others for removal
        for score, entry in scored[1:]:
            to_remove.append(entry['raw'])

    print(f"\n{'-' * 70}")
    print(f"Entries to remove: {len(to_remove)}")

    if not args.apply:
        print("\n[DRY RUN] Use --apply to actually remove duplicates")
        return

    # Remove duplicates from content
    new_content = content
    removed = 0
    for raw in to_remove:
        if raw in new_content:
            new_content = new_content.replace(raw, '', 1)
            removed += 1

    # Clean up multiple blank lines
    new_content = re.sub(r'\n{3,}', '\n\n', new_content)

    # Write back
    with open(BIB_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"\n{removed} duplicate entries removed")

    # Verify
    with open(BIB_FILE, 'r', encoding='utf-8') as f:
        new_entries = parse_entries(f.read())
    print(f"Entries remaining: {len(new_entries)}")


if __name__ == '__main__':
    main()
