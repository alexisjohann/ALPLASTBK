#!/usr/bin/env python3
"""
DOI Strategy Determiner
=======================
Determines the optimal strategy for obtaining a DOI for each paper
based on journal, year, and the journal-database.yaml era information.

Usage:
    python scripts/doi_strategy.py                    # Analyze all papers without DOI
    python scripts/doi_strategy.py --key PAP-kahneman1979prospect # Check specific paper
    python scripts/doi_strategy.py --stats            # Show statistics
    python scripts/doi_strategy.py --export           # Export to CSV

Output:
    PATTERN - DOI can be generated from metadata
    LOOKUP  - DOI must be looked up via API (CrossRef, JSTOR, etc.)
"""

import re
import yaml
import argparse
from pathlib import Path
from collections import defaultdict
from typing import Optional, Tuple, Dict, List, Any

# Paths
SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
BIB_FILE = ROOT_DIR / "bibliography" / "bcm_master.bib"
JOURNAL_DB = ROOT_DIR / "data" / "journal-database.yaml"


def load_journal_database() -> Dict:
    """Load the journal database with era information."""
    with open(JOURNAL_DB, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def parse_bibtex() -> List[Dict]:
    """Parse the BibTeX file and extract paper entries."""
    with open(BIB_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    entries = []
    current_entry = {}

    for line in content.split('\n'):
        # Entry start
        match = re.match(r'^@(\w+)\{([^,]+),', line)
        if match:
            if current_entry:
                entries.append(current_entry)
            current_entry = {
                'type': match.group(1).lower(),
                'key': match.group(2)
            }
            continue

        # Field extraction
        for field in ['doi', 'journal', 'volume', 'number', 'pages', 'year', 'title', 'author', 'booktitle']:
            pattern = rf'^\s*{field}\s*=\s*[{{\"](.+?)[}}\"]'
            match = re.match(pattern, line, re.IGNORECASE)
            if match:
                current_entry[field] = match.group(1)

    # Add last entry
    if current_entry:
        entries.append(current_entry)

    return entries


def normalize_journal_name(name: str) -> str:
    """Normalize journal name for matching."""
    if not name:
        return ""
    # Take first part before comma, strip whitespace
    name = name.split(',')[0].strip()
    # Remove common variations
    name = name.replace('\\&', '&')
    name = name.replace('  ', ' ')
    return name.lower()


def find_journal(journal_name: str, journal_db: Dict) -> Optional[Dict]:
    """Find a journal in the database by name."""
    if not journal_name:
        return None

    normalized = normalize_journal_name(journal_name)

    for journal in journal_db.get('journals', []):
        # Check main name
        if normalize_journal_name(journal.get('name', '')) == normalized:
            return journal
        # Check abbreviation
        if journal.get('abbreviation', '').lower() == normalized:
            return journal
        # Partial match
        if normalized in normalize_journal_name(journal.get('name', '')):
            return journal
        if normalize_journal_name(journal.get('name', '')) in normalized:
            return journal

    return None


def find_era(journal: Dict, year: int) -> Optional[Dict]:
    """Find the applicable era for a paper based on year."""
    if not journal or not year:
        return None

    for era in journal.get('doi_eras', []):
        years = era.get('years', [0, 9999])
        if len(years) >= 2 and years[0] <= year <= years[1]:
            return era

    # Return last era if year is beyond all defined eras
    eras = journal.get('doi_eras', [])
    if eras:
        return eras[-1]

    return None


def get_doi_strategy(paper: Dict, journal_db: Dict) -> Dict:
    """
    Determine the DOI strategy for a paper.

    Returns:
        {
            'strategy': 'PATTERN' | 'LOOKUP' | 'UNKNOWN',
            'journal_found': bool,
            'journal_name': str,
            'journal_superkey': str,
            'era': str,
            'pattern': str (if PATTERN),
            'lookup_source': str (if LOOKUP),
            'predictability_rate': float,
            'reason': str
        }
    """
    result = {
        'key': paper.get('key', ''),
        'strategy': 'UNKNOWN',
        'journal_found': False,
        'journal_name': paper.get('journal', ''),
        'journal_superkey': None,
        'era': None,
        'pattern': None,
        'lookup_source': None,
        'predictability_rate': 0.0,
        'reason': ''
    }

    # Already has DOI?
    if paper.get('doi'):
        result['strategy'] = 'HAS_DOI'
        result['reason'] = f"Already has DOI: {paper['doi']}"
        return result

    # Not a journal article?
    if paper.get('type') not in ['article', 'inproceedings']:
        result['strategy'] = 'SKIP'
        result['reason'] = f"Entry type '{paper.get('type')}' - not a journal article"
        return result

    # Find journal
    journal = find_journal(paper.get('journal', ''), journal_db)
    if not journal:
        result['strategy'] = 'LOOKUP'
        result['lookup_source'] = 'CrossRef'
        result['reason'] = f"Journal not in database: {paper.get('journal', 'N/A')}"
        return result

    result['journal_found'] = True
    result['journal_name'] = journal.get('name', '')
    result['journal_superkey'] = journal.get('superkey', '')
    result['predictability_rate'] = journal.get('predictability_rate', 0.0)

    # Get year
    year_str = paper.get('year', '')
    year = int(year_str) if year_str.isdigit() else None

    if not year:
        result['strategy'] = 'LOOKUP'
        result['lookup_source'] = 'CrossRef'
        result['reason'] = "No valid year found"
        return result

    # Find applicable era
    era = find_era(journal, year)
    if not era:
        result['strategy'] = 'LOOKUP'
        result['lookup_source'] = 'CrossRef'
        result['reason'] = f"No era defined for year {year}"
        return result

    result['era'] = era.get('era', 'Unknown')

    # Check predictability
    if era.get('predictable', False):
        # Check if we have required fields
        required = era.get('requires', [])
        missing = []
        for field in required:
            if field == 'pages' and not paper.get('pages'):
                missing.append('pages')
            elif field == 'volume' and not paper.get('volume'):
                missing.append('volume')
            elif field == 'issue' and not paper.get('number'):
                missing.append('issue')
            elif field == 'number' and not paper.get('number'):
                missing.append('number')

        if missing:
            result['strategy'] = 'LOOKUP'
            result['lookup_source'] = 'CrossRef'
            result['reason'] = f"Missing required fields for pattern: {', '.join(missing)}"
        else:
            result['strategy'] = 'PATTERN'
            result['pattern'] = era.get('pattern', '')
            result['reason'] = f"Predictable pattern for {era.get('era')} era"
    else:
        result['strategy'] = 'LOOKUP'
        prefix = era.get('prefix', '')

        # Determine lookup source based on prefix
        if prefix == '10.2307':
            result['lookup_source'] = 'JSTOR'
        elif prefix == '10.1086':
            result['lookup_source'] = 'Chicago/CrossRef'
        elif prefix in ['10.1126', '10.1038']:
            result['lookup_source'] = 'Publisher/CrossRef'
        else:
            result['lookup_source'] = 'CrossRef'

        result['reason'] = f"{era.get('pattern_type', 'Unknown')} pattern in {era.get('era')} era - not predictable"

    return result


def generate_doi_from_pattern(paper: Dict, pattern: str) -> Optional[str]:
    """Generate a DOI from a pattern and paper metadata."""
    if not pattern:
        return None

    doi = pattern

    # Replace placeholders
    volume = paper.get('volume', '')
    issue = paper.get('number', '1')
    pages = paper.get('pages', '')
    year = paper.get('year', '')

    # Extract start page
    startpage = pages.split('-')[0].strip() if pages else ''

    doi = doi.replace('{volume}', volume)
    doi = doi.replace('{issue}', issue)
    doi = doi.replace('{startpage}', startpage)
    doi = doi.replace('{page}', startpage)
    doi = doi.replace('{year}', year)
    doi = doi.replace('{year_short}', year[-2:] if len(year) >= 2 else year)

    # Check if all placeholders replaced
    if '{' in doi:
        return None

    return doi


def main():
    parser = argparse.ArgumentParser(description='Determine DOI strategy for papers')
    parser.add_argument('--key', help='Check specific paper by key')
    parser.add_argument('--stats', action='store_true', help='Show statistics')
    parser.add_argument('--export', action='store_true', help='Export to CSV')
    parser.add_argument('--generate', action='store_true', help='Generate DOIs where possible')
    parser.add_argument('--limit', type=int, default=0, help='Limit number of papers to process')
    args = parser.parse_args()

    # Load data
    print("Loading journal database...")
    journal_db = load_journal_database()
    print(f"  {len(journal_db.get('journals', []))} journals loaded")

    print("Loading bibliography...")
    papers = parse_bibtex()
    print(f"  {len(papers)} papers loaded")

    # Filter to papers without DOI
    papers_without_doi = [p for p in papers if not p.get('doi')]
    print(f"  {len(papers_without_doi)} papers without DOI")

    # Single paper lookup
    if args.key:
        paper = next((p for p in papers if args.key.lower() in p.get('key', '').lower()), None)
        if not paper:
            print(f"Paper not found: {args.key}")
            return

        result = get_doi_strategy(paper, journal_db)

        print(f"\n{'='*70}")
        print(f"PAPER: {paper.get('key')}")
        print(f"{'='*70}")
        print(f"Title:   {paper.get('title', 'N/A')[:60]}...")
        print(f"Author:  {paper.get('author', 'N/A')[:60]}...")
        print(f"Journal: {paper.get('journal', 'N/A')}")
        print(f"Year:    {paper.get('year', 'N/A')}")
        print(f"Volume:  {paper.get('volume', 'N/A')}")
        print(f"Issue:   {paper.get('number', 'N/A')}")
        print(f"Pages:   {paper.get('pages', 'N/A')}")
        print(f"DOI:     {paper.get('doi', 'MISSING')}")
        print(f"\n{'─'*70}")
        print(f"STRATEGY: {result['strategy']}")
        print(f"{'─'*70}")
        print(f"Journal Found:   {result['journal_found']}")
        print(f"Journal:         {result['journal_name']}")
        print(f"SuperKey:        {result['journal_superkey']}")
        print(f"Era:             {result['era']}")
        print(f"Predict. Rate:   {result['predictability_rate']:.0%}")
        print(f"Reason:          {result['reason']}")

        if result['strategy'] == 'PATTERN':
            print(f"\nPATTERN: {result['pattern']}")
            generated = generate_doi_from_pattern(paper, result['pattern'])
            if generated:
                print(f"GENERATED DOI: {generated}")
        elif result['strategy'] == 'LOOKUP':
            print(f"\nLOOKUP SOURCE: {result['lookup_source']}")

        return

    # Process all papers
    results = []
    process_list = papers_without_doi if not args.limit else papers_without_doi[:args.limit]

    for paper in process_list:
        result = get_doi_strategy(paper, journal_db)
        result['paper'] = paper
        results.append(result)

    # Statistics
    if args.stats or not args.export:
        stats = defaultdict(int)
        by_source = defaultdict(int)
        by_journal = defaultdict(lambda: {'pattern': 0, 'lookup': 0, 'total': 0})

        for r in results:
            stats[r['strategy']] += 1
            if r['strategy'] == 'LOOKUP':
                by_source[r['lookup_source']] += 1
            if r['journal_superkey']:
                j = r['journal_superkey']
                by_journal[j]['total'] += 1
                if r['strategy'] == 'PATTERN':
                    by_journal[j]['pattern'] += 1
                else:
                    by_journal[j]['lookup'] += 1

        print(f"\n{'='*70}")
        print("DOI STRATEGY STATISTICS")
        print(f"{'='*70}")
        print(f"\nTotal papers without DOI: {len(results)}")
        print(f"\nBy Strategy:")
        for strategy, count in sorted(stats.items(), key=lambda x: -x[1]):
            pct = 100 * count / len(results) if results else 0
            print(f"  {strategy:<15} {count:>5} ({pct:>5.1f}%)")

        print(f"\nLookup Sources:")
        for source, count in sorted(by_source.items(), key=lambda x: -x[1]):
            print(f"  {source:<20} {count:>5}")

        print(f"\n{'─'*70}")
        print("Top 15 Journals by Papers Without DOI:")
        print(f"{'─'*70}")
        print(f"{'Journal':<20} {'Total':>6} {'Pattern':>8} {'Lookup':>8} {'Rate':>8}")

        sorted_journals = sorted(by_journal.items(), key=lambda x: -x[1]['total'])[:15]
        for jkey, counts in sorted_journals:
            rate = counts['pattern'] / counts['total'] if counts['total'] > 0 else 0
            print(f"{jkey:<20} {counts['total']:>6} {counts['pattern']:>8} {counts['lookup']:>8} {rate:>7.0%}")

    # Generate DOIs
    if args.generate:
        print(f"\n{'='*70}")
        print("GENERATED DOIs (PATTERN strategy)")
        print(f"{'='*70}")

        generated_count = 0
        for r in results:
            if r['strategy'] == 'PATTERN' and r['pattern']:
                paper = r['paper']
                doi = generate_doi_from_pattern(paper, r['pattern'])
                if doi:
                    generated_count += 1
                    print(f"{paper['key']:<40} {doi}")

        print(f"\n{generated_count} DOIs generated")

    # Export to CSV
    if args.export:
        import csv
        output_file = ROOT_DIR / "data" / "doi_strategy_export.csv"

        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'key', 'strategy', 'journal_found', 'journal_superkey',
                'era', 'pattern', 'lookup_source', 'predictability_rate',
                'reason', 'journal', 'year', 'volume', 'issue', 'pages'
            ])

            for r in results:
                paper = r.get('paper', {})
                writer.writerow([
                    r['key'],
                    r['strategy'],
                    r['journal_found'],
                    r['journal_superkey'],
                    r['era'],
                    r['pattern'],
                    r['lookup_source'],
                    r['predictability_rate'],
                    r['reason'],
                    paper.get('journal', ''),
                    paper.get('year', ''),
                    paper.get('volume', ''),
                    paper.get('number', ''),
                    paper.get('pages', '')
                ])

        print(f"\nExported to {output_file}")


if __name__ == '__main__':
    main()
