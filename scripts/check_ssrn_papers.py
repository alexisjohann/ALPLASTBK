#!/usr/bin/env python3
"""
SSRN Paper Monitor - Check for new working papers on SSRN.

Monitors researchers for new SSRN papers using:
1. SerpAPI (Google Scholar with site:ssrn.com filter)
2. Direct SSRN author page scraping as fallback

Usage:
    python scripts/check_ssrn_papers.py                    # All researchers
    python scripts/check_ssrn_papers.py --researcher RES-FEHR-E
    python scripts/check_ssrn_papers.py --topic "behavioral economics"

API: SerpAPI (uses existing SERPAPI_KEY)

Author: EBF Team
Version: 1.0.0
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta

import requests
import yaml

SERPAPI_KEY = os.environ.get('SERPAPI_KEY')
REGISTRY_PATH = 'data/researcher-registry.yaml'


def search_ssrn_via_serpapi(query: str, num_results: int = 20) -> list:
    """Search SSRN papers via SerpAPI Google Scholar."""
    if not SERPAPI_KEY:
        print("Warning: SERPAPI_KEY not set, skipping SerpAPI search")
        return []

    params = {
        'engine': 'google_scholar',
        'q': f'site:ssrn.com {query}',
        'api_key': SERPAPI_KEY,
        'num': num_results,
        'as_ylo': datetime.now().year - 1,  # Last 2 years
    }

    try:
        response = requests.get(
            'https://serpapi.com/search',
            params=params,
            timeout=30
        )

        if response.status_code == 200:
            data = response.json()
            results = []

            for item in data.get('organic_results', []):
                # Extract SSRN ID from URL
                ssrn_id = None
                link = item.get('link', '')
                match = re.search(r'abstract[=/](\d+)', link)
                if match:
                    ssrn_id = match.group(1)

                results.append({
                    'title': item.get('title', ''),
                    'link': link,
                    'ssrn_id': ssrn_id,
                    'snippet': item.get('snippet', ''),
                    'authors': item.get('publication_info', {}).get('authors', []),
                    'year': item.get('publication_info', {}).get('summary', ''),
                })

            return results
        else:
            print(f"SerpAPI error: {response.status_code}")
            return []

    except Exception as e:
        print(f"Error searching SSRN: {e}")
        return []


def search_ssrn_direct(author_name: str) -> list:
    """Search SSRN directly via their search page."""
    # SSRN search URL
    search_url = "https://papers.ssrn.com/sol3/cf_dev/AbsByAuth.cfm"

    # Try to find author's SSRN page
    params = {
        'per_id': '',  # Would need author ID
    }

    # Alternative: Use SSRN search
    search_params = {
        'form_name': 'journalBrowse',
        'journal_id': '',
        'Network': '',
        'lim': 'false',
        'SortOrder': 'ab_approval_date',
        'output_format': 'json',
        'Terms': author_name,
    }

    try:
        response = requests.get(
            'https://papers.ssrn.com/sol3/JELJOUR_Results.cfm',
            params={'form_name': 'journalBrowse', 'Terms': author_name},
            timeout=30,
            headers={'User-Agent': 'Mozilla/5.0 (compatible; ResearchBot/1.0)'}
        )

        # Parse HTML response for paper links
        papers = []
        if response.status_code == 200:
            # Simple regex extraction of SSRN abstract links
            matches = re.findall(
                r'abstract[=/](\d+)["\'].*?>(.*?)</a>',
                response.text,
                re.IGNORECASE | re.DOTALL
            )
            for ssrn_id, title in matches[:20]:
                papers.append({
                    'ssrn_id': ssrn_id,
                    'title': re.sub(r'<[^>]+>', '', title).strip(),
                    'link': f'https://papers.ssrn.com/sol3/papers.cfm?abstract_id={ssrn_id}',
                })

        return papers

    except Exception as e:
        print(f"Error in direct SSRN search: {e}")
        return []


def get_ssrn_paper_details(ssrn_id: str) -> dict:
    """Get details for a specific SSRN paper."""
    url = f"https://papers.ssrn.com/sol3/papers.cfm?abstract_id={ssrn_id}"

    try:
        response = requests.get(
            url,
            timeout=30,
            headers={'User-Agent': 'Mozilla/5.0 (compatible; ResearchBot/1.0)'}
        )

        if response.status_code == 200:
            html = response.text

            # Extract title
            title_match = re.search(r'<meta name="citation_title" content="([^"]+)"', html)
            title = title_match.group(1) if title_match else None

            # Extract authors
            authors = re.findall(r'<meta name="citation_author" content="([^"]+)"', html)

            # Extract abstract
            abstract_match = re.search(
                r'<meta name="description" content="([^"]+)"',
                html
            )
            abstract = abstract_match.group(1) if abstract_match else None

            # Extract date
            date_match = re.search(r'<meta name="citation_publication_date" content="([^"]+)"', html)
            pub_date = date_match.group(1) if date_match else None

            # Extract keywords
            keywords = re.findall(r'<meta name="citation_keywords" content="([^"]+)"', html)

            return {
                'ssrn_id': ssrn_id,
                'title': title,
                'authors': authors,
                'abstract': abstract,
                'publication_date': pub_date,
                'keywords': keywords,
                'url': url,
            }

        return {}

    except Exception as e:
        print(f"Error fetching SSRN paper {ssrn_id}: {e}")
        return {}


def check_researcher_ssrn(researcher: dict) -> list:
    """Check SSRN for new papers from a researcher."""
    name = researcher.get('name', '')
    known_ssrn_ids = set()

    # Get known SSRN papers from registry
    for paper in researcher.get('paper_bibliography', {}).get('integrated', []):
        if 'ssrn' in paper.get('source', '').lower():
            ssrn_match = re.search(r'(\d{6,})', paper.get('url', ''))
            if ssrn_match:
                known_ssrn_ids.add(ssrn_match.group(1))

    for paper in researcher.get('paper_bibliography', {}).get('not_integrated', []):
        if 'ssrn' in paper.get('source', '').lower():
            ssrn_match = re.search(r'(\d{6,})', paper.get('url', ''))
            if ssrn_match:
                known_ssrn_ids.add(ssrn_match.group(1))

    # Search SSRN
    print(f"  Searching SSRN for: {name}")
    results = search_ssrn_via_serpapi(f'author:"{name}"')

    # Filter to new papers
    new_papers = []
    for paper in results:
        ssrn_id = paper.get('ssrn_id')
        if ssrn_id and ssrn_id not in known_ssrn_ids:
            # Get full details
            details = get_ssrn_paper_details(ssrn_id)
            if details:
                new_papers.append(details)
            else:
                new_papers.append(paper)

    return new_papers


def search_topic(topic: str, num_results: int = 30) -> list:
    """Search SSRN for papers on a topic."""
    print(f"Searching SSRN for topic: {topic}")
    results = search_ssrn_via_serpapi(topic, num_results)

    # Enrich with details
    enriched = []
    for paper in results[:10]:  # Limit to avoid rate limiting
        ssrn_id = paper.get('ssrn_id')
        if ssrn_id:
            details = get_ssrn_paper_details(ssrn_id)
            if details:
                enriched.append(details)
            else:
                enriched.append(paper)
        else:
            enriched.append(paper)

    return enriched


def format_paper(paper: dict, index: int) -> str:
    """Format a paper for display."""
    lines = []
    lines.append(f"\n  {index}. {paper.get('title', 'Unknown Title')}")

    authors = paper.get('authors', [])
    if authors:
        if isinstance(authors, list):
            authors_str = ', '.join(a.get('name', a) if isinstance(a, dict) else a for a in authors[:3])
            if len(authors) > 3:
                authors_str += ' et al.'
        else:
            authors_str = authors
        lines.append(f"     Authors: {authors_str}")

    if paper.get('publication_date'):
        lines.append(f"     Date: {paper['publication_date']}")

    if paper.get('ssrn_id'):
        lines.append(f"     SSRN ID: {paper['ssrn_id']}")
        lines.append(f"     URL: https://papers.ssrn.com/sol3/papers.cfm?abstract_id={paper['ssrn_id']}")
    elif paper.get('link'):
        lines.append(f"     URL: {paper['link']}")

    if paper.get('abstract'):
        abstract = paper['abstract'][:200] + '...' if len(paper.get('abstract', '')) > 200 else paper.get('abstract', '')
        lines.append(f"     Abstract: {abstract}")

    return '\n'.join(lines)


def save_results(results: list, output_path: str):
    """Save results to YAML file."""
    data = {
        'generated_at': datetime.now().isoformat(),
        'total_papers': len(results),
        'papers': results
    }

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

    print(f"\n✅ Saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Monitor SSRN for new working papers'
    )
    parser.add_argument(
        '--researcher', '-r',
        help='Specific researcher ID (e.g., RES-FEHR-E)'
    )
    parser.add_argument(
        '--topic', '-t',
        help='Search for papers on a topic'
    )
    parser.add_argument(
        '--save', '-s',
        action='store_true',
        help='Save results to file'
    )
    parser.add_argument(
        '--output', '-o',
        help='Output file path'
    )
    parser.add_argument(
        '--json', '-j',
        action='store_true',
        help='Output as JSON'
    )

    args = parser.parse_args()

    # Topic search mode
    if args.topic:
        results = search_topic(args.topic)

        if args.json:
            print(json.dumps(results, indent=2, default=str))
        else:
            print("=" * 70)
            print(f"  SSRN PAPERS: {args.topic}")
            print(f"  Found: {len(results)} papers")
            print("=" * 70)

            for i, paper in enumerate(results, 1):
                print(format_paper(paper, i))

        if args.save:
            safe_topic = args.topic.lower().replace(' ', '_')[:30]
            output_path = args.output or f"data/ssrn/topic-{safe_topic}.yaml"
            save_results(results, output_path)

        return 0

    # Researcher mode
    if not os.path.exists(REGISTRY_PATH):
        print(f"Error: Registry not found at {REGISTRY_PATH}")
        return 1

    with open(REGISTRY_PATH, 'r') as f:
        registry = yaml.safe_load(f)

    researchers = registry.get('researchers', [])

    if args.researcher:
        # Find specific researcher
        researcher = None
        for r in researchers:
            if r.get('id') == args.researcher or r.get('superkey') == args.researcher:
                researcher = r
                break

        if not researcher:
            print(f"Error: Researcher {args.researcher} not found")
            return 1

        researchers = [researcher]

    all_new_papers = {}
    total_new = 0

    print("=" * 70)
    print("  SSRN PAPER MONITOR")
    print(f"  Checking {len(researchers)} researcher(s)")
    print("=" * 70)

    for researcher in researchers:
        rid = researcher.get('id') or researcher.get('superkey')
        name = researcher.get('name', 'Unknown')

        new_papers = check_researcher_ssrn(researcher)

        if new_papers:
            all_new_papers[rid] = {
                'name': name,
                'papers': new_papers
            }
            total_new += len(new_papers)

            print(f"\n  📄 {name}: {len(new_papers)} new SSRN paper(s)")
            for i, paper in enumerate(new_papers, 1):
                print(format_paper(paper, i))

    print("\n" + "=" * 70)
    print(f"  TOTAL: {total_new} new paper(s) found")
    print("=" * 70)

    if args.json:
        print(json.dumps(all_new_papers, indent=2, default=str))

    if args.save and all_new_papers:
        output_path = args.output or f"data/ssrn/monitor-{datetime.now().strftime('%Y-%m-%d')}.yaml"
        save_results(all_new_papers, output_path)

    # Set output for GitHub Actions
    if os.environ.get('GITHUB_OUTPUT'):
        with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
            f.write(f"new_papers_found={'true' if total_new > 0 else 'false'}\n")
            f.write(f"total_new_papers={total_new}\n")

    return 0


if __name__ == '__main__':
    sys.exit(main())
