#!/usr/bin/env python3
"""
Check for new papers by researchers tracked in researcher-registry.yaml.

Uses ORCID Atom feeds and Google Scholar (via scraping fallback) to detect
new publications not yet in the registry.

Usage:
    python scripts/check_researcher_papers.py --registry data/researcher-registry.yaml
    python scripts/check_researcher_papers.py --researcher RES-FEHR-E
    python scripts/check_researcher_papers.py --output new_papers.json

Author: EBF Team
Version: 1.0.0
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

import requests
import yaml
import xml.etree.ElementTree as ET
import time

try:
    import feedparser
    HAS_FEEDPARSER = True
except ImportError:
    HAS_FEEDPARSER = False

try:
    from scholarly import scholarly
    HAS_SCHOLARLY = True
except ImportError:
    HAS_SCHOLARLY = False

# SerpAPI for Google Scholar (reliable, paid service with free tier)
SERPAPI_KEY = None  # Set via environment variable SERPAPI_KEY
import os
if os.environ.get('SERPAPI_KEY'):
    SERPAPI_KEY = os.environ.get('SERPAPI_KEY')


def load_registry(registry_path: str) -> dict:
    """Load researcher registry YAML."""
    with open(registry_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def get_orcid_papers(orcid_id: str) -> list[dict]:
    """
    Fetch papers from ORCID Atom feed.

    Args:
        orcid_id: ORCID identifier (e.g., "0000-0003-3943-9857")

    Returns:
        List of paper dicts with title, year, doi, journal
    """
    feed_url = f"https://orcid.org/{orcid_id}/works.atom"

    try:
        # Use feedparser if available, otherwise fall back to manual XML
        if HAS_FEEDPARSER:
            feed = feedparser.parse(feed_url)
            papers = []

            for entry in feed.entries:
                paper = {
                    'title': entry.get('title', 'Unknown'),
                    'year': entry.get('published', '')[:4] if entry.get('published') else None,
                    'doi': None,
                    'journal': None,
                    'source': 'orcid',
                }

                for link in entry.get('links', []):
                    if 'doi.org' in link.get('href', ''):
                        paper['doi'] = link['href'].replace('https://doi.org/', '')

                papers.append(paper)

            return papers
        else:
            # Manual XML parsing fallback
            response = requests.get(feed_url, timeout=30)
            response.raise_for_status()

            # Parse Atom XML
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
                    'journal': None,
                    'source': 'orcid',
                }

                # Extract DOI from links
                for link in entry.findall('atom:link', ns):
                    href = link.get('href', '')
                    if 'doi.org' in href:
                        paper['doi'] = href.replace('https://doi.org/', '')

                papers.append(paper)

            return papers

    except Exception as e:
        print(f"  Warning: ORCID feed error for {orcid_id}: {e}")
        return []


def get_serpapi_scholar_papers(scholar_id: str, max_papers: int = 100) -> list[dict]:
    """
    Fetch papers from Google Scholar via SerpAPI (paid but reliable).

    Requires SERPAPI_KEY environment variable.
    Free tier: 100 searches/month (sufficient for weekly checks).

    Args:
        scholar_id: Google Scholar author ID (e.g., "WoSILroAAAAJ")
        max_papers: Maximum papers to retrieve

    Returns:
        List of paper dicts
    """
    if not SERPAPI_KEY:
        return []

    try:
        url = "https://serpapi.com/search.json"
        params = {
            "engine": "google_scholar_author",
            "author_id": scholar_id,
            "api_key": SERPAPI_KEY,
            "num": min(max_papers, 100)  # Max 100 per request
        }

        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        papers = []
        for article in data.get('articles', []):
            paper = {
                'title': article.get('title', 'Unknown'),
                'year': article.get('year'),
                'doi': None,
                'journal': article.get('publication'),
                'citations': article.get('cited_by', {}).get('value', 0),
                'link': article.get('link'),
                'source': 'serpapi_scholar'
            }
            papers.append(paper)

        return papers

    except Exception as e:
        print(f"  Warning: SerpAPI error: {e}")
        return []


def get_google_scholar_papers(scholar_id: str, max_papers: int = 50) -> list[dict]:
    """
    Fetch papers from Google Scholar using scholarly library.

    Args:
        scholar_id: Google Scholar author ID (e.g., "WoSILroAAAAJ")
        max_papers: Maximum number of papers to fetch

    Returns:
        List of paper dicts
    """
    if not HAS_SCHOLARLY:
        print("  Warning: scholarly not installed. Install with: pip install scholarly")
        return []

    try:
        # Get author by ID
        author = scholarly.search_author_id(scholar_id)
        author = scholarly.fill(author, sections=['publications'])

        papers = []
        for i, pub in enumerate(author.get('publications', [])):
            if i >= max_papers:
                break

            # Fill publication details (rate limited)
            try:
                pub_filled = scholarly.fill(pub)
                time.sleep(0.5)  # Rate limiting to avoid blocks
            except Exception:
                pub_filled = pub

            bib = pub_filled.get('bib', {})
            paper = {
                'title': bib.get('title', 'Unknown'),
                'year': bib.get('pub_year'),
                'doi': None,  # Scholar doesn't provide DOI directly
                'journal': bib.get('venue') or bib.get('journal'),
                'citations': pub_filled.get('num_citations', 0),
                'source': 'google_scholar'
            }
            papers.append(paper)

        return papers

    except Exception as e:
        print(f"  Warning: Google Scholar error: {e}")
        return []


def get_crossref_papers(author_name: str, from_year: int = 2024) -> list[dict]:
    """
    Fetch recent papers from CrossRef API.

    Args:
        author_name: Author name to search (e.g., "Ernst Fehr")
        from_year: Only papers from this year onwards

    Returns:
        List of paper dicts
    """
    base_url = "https://api.crossref.org/works"
    params = {
        'query.author': author_name,
        'filter': f'from-pub-date:{from_year}',
        'rows': 100,
        'sort': 'published',
        'order': 'desc'
    }

    try:
        response = requests.get(base_url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        papers = []
        for item in data.get('message', {}).get('items', []):
            paper = {
                'title': item.get('title', ['Unknown'])[0],
                'year': str(item.get('published', {}).get('date-parts', [[None]])[0][0]),
                'doi': item.get('DOI'),
                'journal': item.get('container-title', ['Unknown'])[0] if item.get('container-title') else None,
                'source': 'crossref'
            }
            papers.append(paper)

        return papers

    except Exception as e:
        print(f"Error fetching CrossRef for {author_name}: {e}")
        return []


def get_known_papers(researcher: dict) -> set[str]:
    """
    Get set of known paper identifiers (DOIs and titles) from registry.

    Args:
        researcher: Researcher dict from registry

    Returns:
        Set of identifiers (lowercase DOIs and titles)
    """
    known = set()

    bibliography = researcher.get('paper_bibliography', {})

    # Integrated papers
    for paper in bibliography.get('integrated', []):
        if paper.get('key'):
            known.add(paper['key'].lower())
        if paper.get('bibtex_key'):
            known.add(paper['bibtex_key'].lower())
        if paper.get('title'):
            known.add(paper['title'].lower()[:50])  # First 50 chars for fuzzy match

    # Non-integrated papers
    for paper in bibliography.get('not_integrated', []):
        if paper.get('paper_id'):
            known.add(paper['paper_id'].lower())
        if paper.get('key'):
            known.add(paper['key'].lower())
        if paper.get('title'):
            known.add(paper['title'].lower()[:50])

    return known


def normalize_title(title: str) -> str:
    """Normalize title for comparison."""
    return title.lower().replace(':', '').replace('-', '').strip()[:50]


def find_new_papers(researcher: dict) -> list[dict]:
    """
    Find papers not yet in the researcher's registry entry.

    Uses multiple sources in priority order:
    1. Google Scholar (most complete, but can be blocked)
    2. ORCID (reliable, but not all authors have it)
    3. CrossRef (supplements with recent papers)

    Args:
        researcher: Researcher dict from registry

    Returns:
        List of new paper dicts
    """
    researcher_id = researcher.get('id', 'Unknown')
    known_papers = get_known_papers(researcher)

    all_papers = []

    # Try SerpAPI first (most reliable, requires API key)
    # Check both top-level and metrics for google_scholar_id
    scholar_id = researcher.get('google_scholar_id') or researcher.get('metrics', {}).get('google_scholar_id')
    if scholar_id and SERPAPI_KEY:
        serpapi_papers = get_serpapi_scholar_papers(scholar_id, max_papers=100)
        all_papers.extend(serpapi_papers)
        print(f"  SerpAPI Scholar: Found {len(serpapi_papers)} papers")
    elif scholar_id:
        # Fallback to scholarly (free but can be blocked)
        scholar_papers = get_google_scholar_papers(scholar_id, max_papers=100)
        all_papers.extend(scholar_papers)
        print(f"  Google Scholar (scholarly): Found {len(scholar_papers)} papers")

    # Try ORCID as backup
    # Check both top-level and metrics for orcid
    orcid = researcher.get('orcid') or researcher.get('metrics', {}).get('orcid')
    if orcid:
        orcid_papers = get_orcid_papers(orcid)
        all_papers.extend(orcid_papers)
        print(f"  ORCID: Found {len(orcid_papers)} papers")

    # Try CrossRef for recent papers (always check)
    # Check various name fields
    basic_info = researcher.get('basic_info', {})
    full_name = basic_info.get('full_name') or basic_info.get('name')
    if full_name:
        crossref_papers = get_crossref_papers(full_name, from_year=2024)
        all_papers.extend(crossref_papers)
        print(f"  CrossRef: Found {len(crossref_papers)} recent papers")

    # Filter out known papers
    new_papers = []
    for paper in all_papers:
        title_normalized = normalize_title(paper.get('title', ''))
        doi_normalized = paper.get('doi', '').lower() if paper.get('doi') else None

        is_known = (
            title_normalized in known_papers or
            (doi_normalized and doi_normalized in known_papers) or
            any(title_normalized in k for k in known_papers)
        )

        if not is_known:
            new_papers.append(paper)

    # Deduplicate by title
    seen_titles = set()
    unique_papers = []
    for paper in new_papers:
        title_key = normalize_title(paper.get('title', ''))
        if title_key not in seen_titles:
            seen_titles.add(title_key)
            unique_papers.append(paper)

    return unique_papers


def main():
    parser = argparse.ArgumentParser(
        description='Check for new papers by tracked researchers'
    )
    parser.add_argument(
        '--registry',
        default='data/researcher-registry.yaml',
        help='Path to researcher registry YAML'
    )
    parser.add_argument(
        '--researcher',
        default='all',
        help='Specific researcher ID or "all"'
    )
    parser.add_argument(
        '--output',
        help='Output JSON file for new papers (for GitHub Actions)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output'
    )

    args = parser.parse_args()

    # Load registry
    registry_path = Path(args.registry)
    if not registry_path.exists():
        print(f"Error: Registry not found: {registry_path}")
        sys.exit(1)

    registry = load_registry(registry_path)
    researchers_raw = registry.get('researchers', {})

    # Handle both list and dict formats
    researchers = []
    if isinstance(researchers_raw, list):
        researchers = researchers_raw
    elif isinstance(researchers_raw, dict):
        for key, value in researchers_raw.items():
            if isinstance(value, dict):
                # Dict format: RES-ENKE-B: {...}
                value['id'] = key
                researchers.append(value)
            elif isinstance(value, list):
                # Mixed: some entries are lists
                researchers.extend(value)

    if not researchers:
        print("No researchers found in registry")
        sys.exit(0)

    # Filter researchers if specific one requested
    if args.researcher != 'all':
        researchers = [r for r in researchers if r.get('id') == args.researcher]
        if not researchers:
            print(f"Researcher not found: {args.researcher}")
            sys.exit(1)

    # Check each researcher
    results = {}
    total_new = 0

    print(f"\n{'='*60}")
    print(f"RESEARCHER PAPER CHECK - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}\n")

    for researcher in researchers:
        researcher_id = researcher.get('id', 'Unknown')
        name = researcher.get('basic_info', {}).get('full_name', researcher_id)

        print(f"Checking: {name} ({researcher_id})")

        new_papers = find_new_papers(researcher)
        results[researcher_id] = new_papers
        total_new += len(new_papers)

        if new_papers:
            print(f"  ✨ NEW PAPERS FOUND: {len(new_papers)}")
            for paper in new_papers:
                print(f"     - {paper.get('title', 'Unknown')[:60]}...")
                if paper.get('doi'):
                    print(f"       DOI: {paper['doi']}")
        else:
            print(f"  ✓ No new papers detected")

        print()

    # Summary
    print(f"{'='*60}")
    print(f"SUMMARY: {total_new} new papers found across {len(researchers)} researchers")
    print(f"{'='*60}\n")

    # Output for GitHub Actions
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)

        # Set output for GitHub Actions (new syntax)
        github_output = os.environ.get('GITHUB_OUTPUT')
        if github_output:
            with open(github_output, 'a') as f:
                f.write(f"new_papers_found={'true' if total_new > 0 else 'false'}\n")
                f.write(f"new_papers_count={total_new}\n")
        else:
            # Fallback for local testing
            print(f"new_papers_found={'true' if total_new > 0 else 'false'}")
            print(f"new_papers_count={total_new}")

    # Always return 0 on success - workflow checks output variables
    return 0


if __name__ == '__main__':
    sys.exit(main())
