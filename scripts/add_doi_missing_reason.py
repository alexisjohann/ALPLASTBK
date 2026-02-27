#!/usr/bin/env python3
"""Add doi_missing_reason field to papers with null DOIs.

Schema:
- doi: "10.1234/..." → DOI exists, no reason needed
- doi: null + doi_missing_reason: "book_no_doi" → Book without DOI
- doi: null + doi_missing_reason: "chapter_no_doi" → Book chapter without DOI
- doi: null + doi_missing_reason: "working_paper" → Working paper without DOI
- doi: null + doi_missing_reason: "pre_doi_era" → Published before DOI system (~2000)
- doi: null + doi_missing_reason: "not_found" → DOI should exist but couldn't be found

Valid reasons:
- book_no_doi: Books typically don't have DOIs (use ISBN instead)
- chapter_no_doi: Book chapters typically don't have DOIs
- working_paper: Working papers/preprints often lack DOIs
- pre_doi_era: Published before widespread DOI adoption (~2000)
- not_found: DOI should exist but API lookup failed
"""

import os
import re
from pathlib import Path
from collections import defaultdict


# Valid doi_missing_reason values
VALID_REASONS = [
    "book_no_doi",
    "chapter_no_doi",
    "working_paper",
    "pre_doi_era",
    "not_found"
]


def get_publication_type(content):
    """Extract publication_type from YAML content."""
    match = re.search(r'publication_type:\s*(\S+)', content)
    return match.group(1) if match else None


def get_year(content):
    """Extract year from YAML content."""
    match = re.search(r'year:\s*["\']?(\d{4})["\']?', content)
    return int(match.group(1)) if match else None


def has_null_doi(content):
    """Check if DOI is null or "null"."""
    # Match doi: null, doi: "null", doi: 'null'
    return bool(re.search(r'doi:\s*(?:null|"null"|\'null\')\s*$', content, re.MULTILINE))


def has_doi_missing_reason(content):
    """Check if doi_missing_reason already exists."""
    return 'doi_missing_reason:' in content


def determine_reason(pub_type, year):
    """Determine the appropriate doi_missing_reason based on publication type and year."""
    if pub_type == 'book':
        return 'book_no_doi'
    elif pub_type == 'book_chapter':
        return 'chapter_no_doi'
    elif pub_type == 'working_paper':
        return 'working_paper'
    elif year and year < 2000:
        return 'pre_doi_era'
    else:
        # Journal articles and other types from 2000+ should have DOIs
        return 'not_found'


def add_doi_missing_reason(filepath, reason):
    """Add doi_missing_reason field after doi line."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the doi line and add reason after it
    # Match: doi: null or doi: "null"
    pattern = r'(doi:\s*(?:null|"null"|\'null\'))\n'
    replacement = f'\\1\ndoi_missing_reason: {reason}\n'

    new_content = re.sub(pattern, replacement, content)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False


def main():
    paper_dir = Path("data/paper-references")

    stats = defaultdict(int)
    updated = []
    skipped = []

    for yaml_file in sorted(paper_dir.glob("PAP-*.yaml")):
        with open(yaml_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Skip if DOI exists (not null)
        if not has_null_doi(content):
            stats['has_doi'] += 1
            continue

        # Skip if already has doi_missing_reason
        if has_doi_missing_reason(content):
            stats['already_has_reason'] += 1
            continue

        # Determine reason
        pub_type = get_publication_type(content)
        year = get_year(content)
        reason = determine_reason(pub_type, year)

        # Add reason
        if add_doi_missing_reason(yaml_file, reason):
            updated.append((yaml_file.name, pub_type, year, reason))
            stats[f'reason_{reason}'] += 1
            stats['updated'] += 1
        else:
            skipped.append(yaml_file.name)
            stats['skipped'] += 1

    # Print summary
    print("=" * 70)
    print("DOI MISSING REASON IMPLEMENTATION")
    print("=" * 70)
    print()
    print("STATISTICS:")
    print(f"  Papers with DOI:           {stats['has_doi']}")
    print(f"  Already had reason:        {stats['already_has_reason']}")
    print(f"  Updated with reason:       {stats['updated']}")
    print(f"  Skipped (no match):        {stats['skipped']}")
    print()
    print("REASONS ASSIGNED:")
    print(f"  book_no_doi:               {stats['reason_book_no_doi']}")
    print(f"  chapter_no_doi:            {stats['reason_chapter_no_doi']}")
    print(f"  working_paper:             {stats['reason_working_paper']}")
    print(f"  pre_doi_era:               {stats['reason_pre_doi_era']}")
    print(f"  not_found:                 {stats['reason_not_found']}")
    print()

    if updated:
        print(f"UPDATED FILES ({len(updated)}):")
        for name, pub_type, year, reason in updated[:20]:
            print(f"  {name}: {pub_type} ({year}) → {reason}")
        if len(updated) > 20:
            print(f"  ... and {len(updated) - 20} more")

    if skipped:
        print(f"\nSKIPPED FILES ({len(skipped)}):")
        for name in skipped[:10]:
            print(f"  {name}")
        if len(skipped) > 10:
            print(f"  ... and {len(skipped) - 10} more")

    print()
    print("=" * 70)
    print(f"TOTAL: {stats['updated']} papers updated with doi_missing_reason")
    print("=" * 70)


if __name__ == "__main__":
    main()
