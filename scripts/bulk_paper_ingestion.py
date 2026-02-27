#!/usr/bin/env python3
"""
Bulk Paper Ingestion - Automate L1 paper integration for all researchers.

This script:
1. Fetches all papers for researchers via SerpAPI/ORCID/CrossRef
2. Finds DOIs via CrossRef/OpenAlex
3. Generates BibTeX entries with proper EBF fields
4. Adds to bcm_master.bib with use_for = {LIT-XXX}

Usage:
    python scripts/bulk_paper_ingestion.py                    # Report mode
    python scripts/bulk_paper_ingestion.py --update           # Apply changes
    python scripts/bulk_paper_ingestion.py --researcher RES-FEHR-E
    python scripts/bulk_paper_ingestion.py --limit 50         # Limit per researcher

Author: EBF Team
Version: 1.0.0
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path

import requests
import yaml

# Constants
REGISTRY_PATH = 'data/researcher-registry.yaml'
BIBTEX_PATH = 'bibliography/bcm_master.bib'

# API Keys from environment
SERPAPI_KEY = os.environ.get('SERPAPI_KEY')
OPENALEX_EMAIL = os.environ.get('OPENALEX_EMAIL', 'ebf@fehradvice.com')

# LIT-Appendix mapping
RESEARCHER_LIT_MAPPING = {
    'RES-FEHR-E': 'LIT-FEH',
    'RES-SUTTER-M': 'LIT-SUT',
    'RES-ENKE-B': 'LIT-ENK',
}


def load_registry() -> dict:
    """Load researcher registry."""
    with open(REGISTRY_PATH, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def load_existing_bibtex() -> set:
    """Load existing BibTeX keys to avoid duplicates."""
    keys = set()
    try:
        with open(BIBTEX_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
        # Extract all keys
        pattern = r'@\w+\s*\{\s*([^,]+)\s*,'
        keys = set(re.findall(pattern, content))
    except FileNotFoundError:
        pass
    return keys


def fetch_serpapi_papers(scholar_id: str, max_papers: int = 100) -> list[dict]:
    """Fetch papers from Google Scholar via SerpAPI."""
    if not SERPAPI_KEY:
        print("  ⚠️  SERPAPI_KEY not set, skipping SerpAPI")
        return []

    try:
        url = "https://serpapi.com/search.json"
        all_papers = []
        start = 0

        while len(all_papers) < max_papers:
            params = {
                "engine": "google_scholar_author",
                "author_id": scholar_id,
                "api_key": SERPAPI_KEY,
                "start": start,
                "num": min(100, max_papers - len(all_papers))
            }

            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            articles = data.get('articles', [])
            if not articles:
                break

            for article in articles:
                paper = {
                    'title': article.get('title', 'Unknown'),
                    'year': article.get('year'),
                    'journal': article.get('publication'),
                    'citations': article.get('cited_by', {}).get('value', 0),
                    'link': article.get('link'),
                    'authors': article.get('authors', ''),
                    'source': 'serpapi'
                }
                all_papers.append(paper)

            start += len(articles)
            if len(articles) < 100:
                break
            time.sleep(1)  # Rate limiting

        return all_papers[:max_papers]

    except Exception as e:
        print(f"  ⚠️  SerpAPI error: {e}")
        return []


def fetch_orcid_papers(orcid_id: str) -> list[dict]:
    """Fetch papers from ORCID."""
    if not orcid_id:
        return []

    try:
        # Try Atom feed first
        feed_url = f"https://orcid.org/{orcid_id}/works.atom"
        response = requests.get(feed_url, timeout=30)
        response.raise_for_status()

        import xml.etree.ElementTree as ET
        root = ET.fromstring(response.content)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}

        papers = []
        for entry in root.findall('atom:entry', ns):
            title_elem = entry.find('atom:title', ns)
            published_elem = entry.find('atom:published', ns)

            paper = {
                'title': title_elem.text if title_elem is not None else 'Unknown',
                'year': published_elem.text[:4] if published_elem is not None and published_elem.text else None,
                'doi': None,
                'source': 'orcid'
            }

            # Extract DOI from links
            for link in entry.findall('atom:link', ns):
                href = link.get('href', '')
                if 'doi.org' in href:
                    paper['doi'] = href.replace('https://doi.org/', '').replace('http://doi.org/', '')

            papers.append(paper)

        return papers

    except Exception as e:
        print(f"  ⚠️  ORCID error: {e}")
        return []


def fetch_crossref_papers(author_name: str, from_year: int = 1990) -> list[dict]:
    """Fetch papers from CrossRef."""
    try:
        base_url = "https://api.crossref.org/works"
        all_papers = []
        cursor = '*'

        while len(all_papers) < 500:  # Safety limit
            params = {
                'query.author': author_name,
                'filter': f'from-pub-date:{from_year}',
                'rows': 100,
                'cursor': cursor,
                'mailto': OPENALEX_EMAIL
            }

            response = requests.get(base_url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            items = data.get('message', {}).get('items', [])
            if not items:
                break

            for item in items:
                title_list = item.get('title', ['Unknown'])
                paper = {
                    'title': title_list[0] if title_list else 'Unknown',
                    'year': str(item.get('published', {}).get('date-parts', [[None]])[0][0]) if item.get('published') else None,
                    'doi': item.get('DOI'),
                    'journal': item.get('container-title', [''])[0] if item.get('container-title') else None,
                    'volume': item.get('volume'),
                    'pages': item.get('page'),
                    'authors': '; '.join([f"{a.get('family', '')}, {a.get('given', '')}" for a in item.get('author', [])[:5]]),
                    'source': 'crossref'
                }
                all_papers.append(paper)

            cursor = data.get('message', {}).get('next-cursor')
            if not cursor:
                break
            time.sleep(0.5)

        return all_papers

    except Exception as e:
        print(f"  ⚠️  CrossRef error: {e}")
        return []


def find_doi_for_paper(title: str, author: str = None) -> str:
    """Try to find DOI for a paper via CrossRef."""
    if not title:
        return None

    try:
        clean_title = re.sub(r'[{}\\]', '', title)

        url = "https://api.crossref.org/works"
        params = {
            'query.title': clean_title,
            'rows': 5,
            'mailto': OPENALEX_EMAIL
        }
        if author:
            params['query.author'] = author.split(',')[0]  # First author

        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        items = data.get('message', {}).get('items', [])
        if items:
            # Check title similarity
            for item in items:
                item_title = item.get('title', [''])[0].lower()
                if clean_title.lower()[:40] in item_title or item_title[:40] in clean_title.lower():
                    return item.get('DOI')

        return None

    except Exception:
        return None


def generate_bibtex_key(author: str, year: str, title: str) -> str:
    """Generate a BibTeX key."""
    # Extract first author's last name
    if ',' in author:
        last_name = author.split(',')[0].strip()
    elif ' ' in author:
        last_name = author.split()[-1].strip()
    else:
        last_name = author.strip()

    last_name = re.sub(r'[^a-zA-Z]', '', last_name).lower()
    year = str(year) if year else '0000'

    # First word of title
    title_word = re.sub(r'[^a-zA-Z]', '', title.split()[0] if title else 'unknown').lower()

    return f"{last_name}{year}{title_word}"


def generate_bibtex_entry(paper: dict, lit_appendix: str) -> str:
    """Generate a BibTeX entry for a paper."""
    key = generate_bibtex_key(
        paper.get('authors', 'Unknown'),
        paper.get('year', ''),
        paper.get('title', 'Unknown')
    )

    entry_type = 'article' if paper.get('journal') else 'misc'

    fields = []
    fields.append(f'  title = {{{paper.get("title", "Unknown")}}}')

    if paper.get('authors'):
        fields.append(f'  author = {{{paper.get("authors")}}}')

    if paper.get('year'):
        fields.append(f'  year = {{{paper.get("year")}}}')

    if paper.get('journal'):
        fields.append(f'  journal = {{{paper.get("journal")}}}')

    if paper.get('doi'):
        fields.append(f'  doi = {{{paper.get("doi")}}}')

    if paper.get('volume'):
        fields.append(f'  volume = {{{paper.get("volume")}}}')

    if paper.get('pages'):
        fields.append(f'  pages = {{{paper.get("pages")}}}')

    # EBF-specific fields
    fields.append(f'  use_for = {{{lit_appendix}}}')
    fields.append(f'  evidence_tier = {{3}}')  # Default to Bronze (working paper level)
    fields.append(f'  integration_level = {{L1}}')
    fields.append(f'  added_date = {{{datetime.now().strftime("%Y-%m-%d")}}}')
    fields.append(f'  source = {{{paper.get("source", "api")}}}')

    entry = f"@{entry_type}{{{key},\n"
    entry += ",\n".join(fields)
    entry += "\n}\n"

    return key, entry


def merge_papers(papers_list: list[list[dict]]) -> list[dict]:
    """Merge papers from multiple sources, removing duplicates."""
    seen_titles = {}
    merged = []

    for papers in papers_list:
        for paper in papers:
            title_key = paper.get('title', '').lower()[:50]

            if title_key not in seen_titles:
                seen_titles[title_key] = paper
                merged.append(paper)
            else:
                # Update with better data if available
                existing = seen_titles[title_key]
                if paper.get('doi') and not existing.get('doi'):
                    existing['doi'] = paper['doi']
                if paper.get('journal') and not existing.get('journal'):
                    existing['journal'] = paper['journal']

    return merged


def process_researcher(researcher: dict, existing_keys: set, limit: int = 100) -> tuple[list, list]:
    """Process a single researcher and return papers to add."""
    rid = researcher.get('id') or researcher.get('superkey')
    name = researcher.get('basic_info', {}).get('full_name', 'Unknown')
    scholar_id = researcher.get('google_scholar_id') or researcher.get('metrics', {}).get('google_scholar_id')
    orcid = researcher.get('orcid') or researcher.get('metrics', {}).get('orcid')
    lit_appendix = RESEARCHER_LIT_MAPPING.get(rid, 'LIT-O')

    print(f"\n📚 Processing {name} ({rid})")
    print(f"   Scholar ID: {scholar_id}")
    print(f"   ORCID: {orcid}")
    print(f"   LIT Appendix: {lit_appendix}")

    # Fetch from multiple sources
    papers_lists = []

    if scholar_id:
        print("   Fetching from SerpAPI...")
        serpapi_papers = fetch_serpapi_papers(scholar_id, max_papers=limit)
        print(f"   → {len(serpapi_papers)} papers from SerpAPI")
        papers_lists.append(serpapi_papers)

    if orcid:
        print("   Fetching from ORCID...")
        orcid_papers = fetch_orcid_papers(orcid)
        print(f"   → {len(orcid_papers)} papers from ORCID")
        papers_lists.append(orcid_papers)

    print(f"   Fetching from CrossRef ({name})...")
    crossref_papers = fetch_crossref_papers(name)
    print(f"   → {len(crossref_papers)} papers from CrossRef")
    papers_lists.append(crossref_papers)

    # Merge and deduplicate
    all_papers = merge_papers(papers_lists)
    print(f"   → {len(all_papers)} unique papers after merge")

    # Find DOIs for papers without them
    for paper in all_papers:
        if not paper.get('doi'):
            doi = find_doi_for_paper(paper.get('title'), paper.get('authors'))
            if doi:
                paper['doi'] = doi

    # Generate BibTeX entries for new papers
    new_entries = []
    skipped = []

    for paper in all_papers:
        key, entry = generate_bibtex_entry(paper, lit_appendix)

        # Check if already exists
        if key in existing_keys:
            skipped.append(paper)
            continue

        # Check for similar keys
        base_key = key
        counter = 2
        while key in existing_keys:
            key = f"{base_key}{chr(96 + counter)}"  # a, b, c...
            counter += 1

        new_entries.append({
            'key': key,
            'entry': entry,
            'paper': paper
        })
        existing_keys.add(key)

    print(f"   → {len(new_entries)} NEW papers to add")
    print(f"   → {len(skipped)} already in bibliography")

    return new_entries, skipped


def main():
    parser = argparse.ArgumentParser(description='Bulk paper ingestion for EBF')
    parser.add_argument('--update', action='store_true', help='Apply changes to bcm_master.bib')
    parser.add_argument('--researcher', type=str, help='Process specific researcher ID')
    parser.add_argument('--limit', type=int, default=100, help='Max papers per researcher')
    parser.add_argument('--output', type=str, help='Output JSON file for new papers')
    args = parser.parse_args()

    print("=" * 70)
    print("BULK PAPER INGESTION - Level 1 Integration")
    print("=" * 70)

    # Load data
    registry = load_registry()
    existing_keys = load_existing_bibtex()
    print(f"\n📖 Existing BibTeX entries: {len(existing_keys)}")

    # Get researchers
    researchers = registry.get('researchers', [])
    if args.researcher:
        researchers = [r for r in researchers if r.get('id') == args.researcher or r.get('superkey') == args.researcher]
        if not researchers:
            print(f"❌ Researcher {args.researcher} not found")
            return

    all_new_entries = []
    all_skipped = []

    for researcher in researchers:
        new_entries, skipped = process_researcher(researcher, existing_keys, args.limit)
        all_new_entries.extend(new_entries)
        all_skipped.extend(skipped)

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total NEW papers to add: {len(all_new_entries)}")
    print(f"Total already existing: {len(all_skipped)}")

    # Output JSON if requested
    if args.output:
        output_data = {
            'timestamp': datetime.now().isoformat(),
            'new_papers': [e['paper'] for e in all_new_entries],
            'count': len(all_new_entries)
        }
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        print(f"\n📄 Output written to {args.output}")

    # Apply updates if requested
    if args.update and all_new_entries:
        print(f"\n📝 Appending {len(all_new_entries)} entries to {BIBTEX_PATH}...")

        with open(BIBTEX_PATH, 'a', encoding='utf-8') as f:
            f.write(f"\n\n% ======================================================================\n")
            f.write(f"% BULK INGESTION - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write(f"% {len(all_new_entries)} papers added via bulk_paper_ingestion.py\n")
            f.write(f"% ======================================================================\n\n")

            for entry_data in all_new_entries:
                f.write(entry_data['entry'])
                f.write("\n")

        print(f"✅ Added {len(all_new_entries)} papers to bibliography")
    elif not args.update and all_new_entries:
        print("\n⚠️  Run with --update to apply changes")
        print("\nSample entries:")
        for entry_data in all_new_entries[:3]:
            print(f"\n{entry_data['entry']}")


if __name__ == '__main__':
    main()
