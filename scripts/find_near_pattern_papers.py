#!/usr/bin/env python3
"""
Find Near-PATTERN Papers
========================
Identifies papers that could use PATTERN strategy if one more field was filled.

Usage:
    python scripts/find_near_pattern_papers.py
"""

import sys
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent))
from doi_strategy import (
    load_journal_database,
    parse_bibtex,
    find_journal,
    find_era,
    normalize_journal_name
)


def main():
    print("Loading journal database...")
    journal_db = load_journal_database()

    print("Loading bibliography...")
    papers = parse_bibtex()
    papers_without_doi = [p for p in papers if not p.get('doi') and p.get('type') == 'article']

    print(f"  {len(papers_without_doi)} journal articles without DOI")

    # Analyze each paper
    near_pattern = defaultdict(list)  # missing_field -> list of papers

    for paper in papers_without_doi:
        journal = find_journal(paper.get('journal', ''), journal_db)
        if not journal:
            continue

        year_str = paper.get('year', '')
        year = int(year_str) if year_str.isdigit() else None
        if not year:
            continue

        era = find_era(journal, year)
        if not era or not era.get('predictable', False):
            continue

        # This journal-era is predictable - check what fields are missing
        required = era.get('requires', [])
        missing = []

        for field in required:
            if field == 'pages' and not paper.get('pages'):
                missing.append('pages')
            elif field == 'volume' and not paper.get('volume'):
                missing.append('volume')
            elif field in ['issue', 'number'] and not paper.get('number'):
                missing.append('number')

        if len(missing) == 1:
            near_pattern[missing[0]].append({
                'key': paper['key'],
                'journal': journal.get('name', ''),
                'year': year,
                'title': paper.get('title', '')[:50],
                'missing': missing[0],
                'has_volume': bool(paper.get('volume')),
                'has_pages': bool(paper.get('pages')),
                'has_number': bool(paper.get('number'))
            })

    # Report
    print("\n" + "=" * 70)
    print("NEAR-PATTERN PAPERS (missing only 1 field)")
    print("=" * 70)

    total = sum(len(v) for v in near_pattern.values())
    print(f"\nTotal: {total} papers could use PATTERN with 1 field")

    for field, papers_list in sorted(near_pattern.items(), key=lambda x: -len(x[1])):
        print(f"\n{'─' * 70}")
        print(f"Missing '{field}': {len(papers_list)} papers")
        print(f"{'─' * 70}")

        # Group by journal
        by_journal = defaultdict(list)
        for p in papers_list:
            by_journal[p['journal']].append(p)

        for jname, jpapers in sorted(by_journal.items(), key=lambda x: -len(x[1]))[:10]:
            print(f"\n  {jname} ({len(jpapers)} papers):")
            for p in jpapers[:5]:
                vol = f"v{p.get('volume', '?')}" if p['has_volume'] else "no-vol"
                pg = f"p{p.get('pages', '?')}" if p['has_pages'] else "no-pg"
                print(f"    {p['key']:<35} {p['year']} {vol:>6} {pg:>8}")
            if len(jpapers) > 5:
                print(f"    ... and {len(jpapers) - 5} more")

    # Summary
    print("\n" + "=" * 70)
    print("PRIORITY RECOMMENDATION")
    print("=" * 70)

    if 'pages' in near_pattern:
        print(f"\n1. Add 'pages' field to {len(near_pattern['pages'])} papers")
        print("   → Highest impact: enables PATTERN for most papers")

    if 'volume' in near_pattern:
        print(f"\n2. Add 'volume' field to {len(near_pattern['volume'])} papers")

    if 'number' in near_pattern:
        print(f"\n3. Add 'number' field to {len(near_pattern['number'])} papers")


if __name__ == '__main__':
    main()
