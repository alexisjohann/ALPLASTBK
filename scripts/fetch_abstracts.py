#!/usr/bin/env python3
"""
SWSM Abstract Fetcher - Fetch abstracts via CrossRef API
=========================================================

Extracts DOIs from bibliography and fetches abstracts for style analysis.

Usage:
    python fetch_abstracts.py --author Sutter --limit 10
    python fetch_abstracts.py --all-authors --limit 5
    python fetch_abstracts.py --analyze
"""

import re
import json
import time
import argparse
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from collections import defaultdict

# Authors we're interested in
TARGET_AUTHORS = [
    'Fehr', 'Camerer', 'List', 'Sutter', 'Gneezy',
    'Thaler', 'Ariely', 'Kahneman', 'Sunstein', 'Mullainathan',
    'Autor', 'Shiller'
]

CROSSREF_API = "https://api.crossref.org/works/"
USER_AGENT = "SWSM-StyleAnalyzer/1.0 (mailto:research@fehradvice.com)"


def parse_bibtex(bib_path: str) -> List[Dict]:
    """Parse BibTeX file and extract entries with DOIs."""
    entries = []

    with open(bib_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Split into entries
    entry_pattern = r'@(\w+)\{([^,]+),([^@]*)'
    matches = re.findall(entry_pattern, content, re.DOTALL)

    for entry_type, key, fields in matches:
        entry = {
            'type': entry_type,
            'key': key.strip(),
            'doi': None,
            'title': None,
            'author': None,
            'year': None
        }

        # Extract fields
        doi_match = re.search(r'doi\s*=\s*\{([^}]+)\}', fields, re.IGNORECASE)
        if doi_match:
            entry['doi'] = doi_match.group(1).strip()

        title_match = re.search(r'title\s*=\s*\{([^}]+)\}', fields)
        if title_match:
            entry['title'] = title_match.group(1).strip()

        author_match = re.search(r'author\s*=\s*\{([^}]+)\}', fields)
        if author_match:
            entry['author'] = author_match.group(1).strip()

        year_match = re.search(r'year\s*=\s*\{?(\d{4})\}?', fields)
        if year_match:
            entry['year'] = year_match.group(1)

        entries.append(entry)

    return entries


def get_entries_by_author(entries: List[Dict], author: str) -> List[Dict]:
    """Filter entries by author name."""
    return [e for e in entries if e['author'] and author.lower() in e['author'].lower()]


def fetch_abstract_crossref(doi: str) -> Optional[str]:
    """Fetch abstract from CrossRef API."""
    if not doi:
        return None

    # Clean DOI
    doi = doi.strip()
    if doi.startswith('http'):
        doi = doi.split('doi.org/')[-1]

    url = f"{CROSSREF_API}{doi}"

    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', USER_AGENT)

        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))

            if 'message' in data and 'abstract' in data['message']:
                abstract = data['message']['abstract']
                # Clean HTML tags
                abstract = re.sub(r'<[^>]+>', '', abstract)
                return abstract.strip()

    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None  # DOI not found
        print(f"  HTTP Error {e.code} for {doi}")
    except urllib.error.URLError as e:
        print(f"  URL Error for {doi}: {e.reason}")
    except Exception as e:
        print(f"  Error for {doi}: {e}")

    return None


def fetch_abstracts_for_author(entries: List[Dict], author: str,
                                limit: int = 10, delay: float = 0.5) -> List[Dict]:
    """Fetch abstracts for papers by a specific author."""
    author_entries = get_entries_by_author(entries, author)

    # Filter to those with DOIs
    with_doi = [e for e in author_entries if e['doi']]

    print(f"\n{author}: {len(author_entries)} papers, {len(with_doi)} with DOI")

    results = []
    fetched = 0

    for entry in with_doi[:limit]:
        print(f"  Fetching: {entry['title'][:50]}...")

        abstract = fetch_abstract_crossref(entry['doi'])

        if abstract:
            entry['abstract'] = abstract
            entry['abstract_words'] = len(abstract.split())
            results.append(entry)
            fetched += 1
            print(f"    ✓ Got {entry['abstract_words']} words")
        else:
            print(f"    ✗ No abstract available")

        time.sleep(delay)  # Rate limiting

    print(f"  → Fetched {fetched}/{min(limit, len(with_doi))} abstracts")
    return results


def save_abstracts(abstracts: Dict[str, List[Dict]], output_path: str):
    """Save fetched abstracts to JSON."""
    # Convert to serializable format
    output = {
        'metadata': {
            'total_abstracts': sum(len(v) for v in abstracts.values()),
            'authors': list(abstracts.keys()),
            'fetched_at': time.strftime('%Y-%m-%d %H:%M:%S')
        },
        'abstracts': abstracts
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\nSaved to {output_path}")


def analyze_abstracts(abstracts_path: str):
    """Analyze fetched abstracts with stylometry."""
    # Import the analyzer
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from stylometry_analyzer import StylometryAnalyzer, AUTHOR_PRIORS

    with open(abstracts_path, 'r') as f:
        data = json.load(f)

    analyzer = StylometryAnalyzer()

    print("\n" + "=" * 70)
    print("ABSTRACT STYLE ANALYSIS")
    print("=" * 70)

    for author, papers in data['abstracts'].items():
        if not papers:
            continue

        print(f"\n{author} ({len(papers)} abstracts)")
        print("-" * 50)

        vectors = []
        for paper in papers:
            if 'abstract' in paper:
                vec = analyzer.analyze_text(paper['abstract'])
                vectors.append(vec.to_array())

        if vectors:
            import numpy as np
            mean_vec = np.mean(vectors, axis=0)
            std_vec = np.std(vectors, axis=0)

            # Compare to prior
            if author in AUTHOR_PRIORS:
                prior = AUTHOR_PRIORS[author]['priors']
                prior_vec = [prior[f'D{i}'][0] for i in range(1, 11)]

                print(f"{'Dim':<6} {'Prior':>8} {'Measured':>10} {'Diff':>8}")
                print("-" * 35)

                dims = ['D1:Form', 'D2:Evid', 'D3:Narr', 'D4:Hedg', 'D5:Poli',
                       'D6:Synt', 'D7:Coll', 'D8:Hum', 'D9:Int', 'D10:Tmp']

                for i, dim in enumerate(dims):
                    diff = mean_vec[i] - prior_vec[i]
                    marker = "!" if abs(diff) > 0.2 else ""
                    print(f"{dim:<6} {prior_vec[i]:>8.2f} {mean_vec[i]:>10.2f} {diff:>+8.2f} {marker}")


def main():
    parser = argparse.ArgumentParser(description='Fetch abstracts for SWSM analysis')
    parser.add_argument('--bib', default='bibliography/bcm_master.bib',
                       help='Path to bibliography file')
    parser.add_argument('--author', type=str, help='Specific author to fetch')
    parser.add_argument('--all-authors', action='store_true', help='Fetch for all target authors')
    parser.add_argument('--limit', type=int, default=10, help='Max abstracts per author')
    parser.add_argument('--output', default='data/swsm-abstracts.json', help='Output file')
    parser.add_argument('--analyze', action='store_true', help='Analyze existing abstracts')
    parser.add_argument('--delay', type=float, default=0.5, help='Delay between API calls')

    args = parser.parse_args()

    if args.analyze:
        analyze_abstracts(args.output)
        return

    print("=" * 60)
    print("SWSM ABSTRACT FETCHER")
    print("=" * 60)

    # Parse bibliography
    print(f"\nParsing {args.bib}...")
    entries = parse_bibtex(args.bib)
    print(f"Found {len(entries)} entries, {sum(1 for e in entries if e['doi'])} with DOI")

    # Determine which authors to fetch
    if args.author:
        authors = [args.author]
    elif args.all_authors:
        authors = TARGET_AUTHORS
    else:
        print("\nSpecify --author NAME or --all-authors")
        return

    # Fetch abstracts
    all_abstracts = {}

    for author in authors:
        abstracts = fetch_abstracts_for_author(
            entries, author,
            limit=args.limit,
            delay=args.delay
        )
        all_abstracts[author] = abstracts

    # Save results
    save_abstracts(all_abstracts, args.output)

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    total = 0
    for author, abstracts in all_abstracts.items():
        if abstracts:
            avg_words = sum(a['abstract_words'] for a in abstracts) / len(abstracts)
            print(f"{author:<15} {len(abstracts):>3} abstracts, avg {avg_words:.0f} words")
            total += len(abstracts)

    print(f"\nTotal: {total} abstracts fetched")
    print(f"Run with --analyze to perform style analysis")


if __name__ == '__main__':
    main()
