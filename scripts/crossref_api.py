#!/usr/bin/env python3
"""
CrossRef API Client - Access 150M+ scientific publication metadata.

Features:
- DOI → Full metadata lookup
- Title/Author search
- Citation counts
- Reference lists
- BibTeX generation
- Journal information

Usage:
    python scripts/crossref_api.py --doi "10.1257/aer.91.5.1369"
    python scripts/crossref_api.py --title "Risk Aversion and Incentive Effects"
    python scripts/crossref_api.py --author "Ernst Fehr"
    python scripts/crossref_api.py --doi "10.1257/aer.91.5.1369" --bibtex
    python scripts/crossref_api.py --doi "10.1257/aer.91.5.1369" --references

API: CrossRef (kostenlos, kein API-Key erforderlich)
Docs: https://api.crossref.org/swagger-ui/index.html

Author: EBF Team
Version: 1.0.0
"""

import argparse
import json
import re
import sys
import time
from datetime import datetime
from typing import Optional
from urllib.parse import quote

import requests

# Polite pool - mit Email bessere Rate Limits
CROSSREF_BASE_URL = "https://api.crossref.org"
USER_AGENT = "EBF-Framework/1.0 (mailto:research@fehradvice.com)"


class CrossRefClient:
    """Client for CrossRef API."""

    def __init__(self, email: str = None):
        self.base_url = CROSSREF_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': USER_AGENT if not email else f"EBF-Framework/1.0 (mailto:{email})"
        })

    def _request(self, endpoint: str, params: dict = None) -> dict:
        """Make API request with rate limiting."""
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.get(url, params=params, timeout=30)

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return {'status': 'not_found'}
            else:
                print(f"API Error: {response.status_code}")
                return {'status': 'error', 'code': response.status_code}

        except Exception as e:
            print(f"Request error: {e}")
            return {'status': 'error', 'message': str(e)}

    def get_work(self, doi: str) -> dict:
        """Get metadata for a DOI."""
        # Clean DOI
        doi = doi.strip()
        if doi.startswith('https://doi.org/'):
            doi = doi[16:]
        elif doi.startswith('http://doi.org/'):
            doi = doi[15:]
        elif doi.startswith('doi:'):
            doi = doi[4:]

        result = self._request(f"/works/{quote(doi, safe='')}")

        if result.get('status') == 'ok':
            return result.get('message', {})
        return result

    def search_works(self, query: str, rows: int = 20,
                     author: str = None,
                     container_title: str = None,
                     from_year: int = None) -> list:
        """Search for works by query."""
        params = {
            'query': query,
            'rows': rows,
            'sort': 'relevance',
            'order': 'desc'
        }

        if author:
            params['query.author'] = author
        if container_title:
            params['query.container-title'] = container_title
        if from_year:
            params['filter'] = f'from-pub-date:{from_year}'

        result = self._request('/works', params)

        if result.get('status') == 'ok':
            return result.get('message', {}).get('items', [])
        return []

    def search_by_author(self, author_name: str, rows: int = 50) -> list:
        """Search for all works by an author."""
        params = {
            'query.author': author_name,
            'rows': rows,
            'sort': 'published',
            'order': 'desc'
        }

        result = self._request('/works', params)

        if result.get('status') == 'ok':
            return result.get('message', {}).get('items', [])
        return []

    def search_by_title(self, title: str, rows: int = 5) -> list:
        """Search for works by exact title."""
        params = {
            'query.title': title,
            'rows': rows,
        }

        result = self._request('/works', params)

        if result.get('status') == 'ok':
            return result.get('message', {}).get('items', [])
        return []

    def get_references(self, doi: str) -> list:
        """Get references cited by a paper."""
        work = self.get_work(doi)
        if isinstance(work, dict) and 'reference' in work:
            return work.get('reference', [])
        return []

    def get_citations_count(self, doi: str) -> int:
        """Get number of citations for a DOI."""
        work = self.get_work(doi)
        if isinstance(work, dict):
            return work.get('is-referenced-by-count', 0)
        return 0

    def get_journal(self, issn: str) -> dict:
        """Get journal information by ISSN."""
        result = self._request(f"/journals/{issn}")
        if result.get('status') == 'ok':
            return result.get('message', {})
        return result

    def validate_doi(self, doi: str) -> bool:
        """Check if a DOI exists."""
        work = self.get_work(doi)
        return isinstance(work, dict) and 'DOI' in work


def extract_metadata(work: dict) -> dict:
    """Extract clean metadata from CrossRef response."""
    if not work or 'DOI' not in work:
        return {}

    # Extract authors
    authors = []
    for author in work.get('author', []):
        name_parts = []
        if author.get('given'):
            name_parts.append(author['given'])
        if author.get('family'):
            name_parts.append(author['family'])
        if name_parts:
            authors.append(' '.join(name_parts))
        elif author.get('name'):
            authors.append(author['name'])

    # Extract date
    pub_date = None
    date_parts = work.get('published-print', work.get('published-online', {}))
    if date_parts and 'date-parts' in date_parts:
        parts = date_parts['date-parts'][0]
        if len(parts) >= 1:
            pub_date = str(parts[0])
            if len(parts) >= 2:
                pub_date += f"-{parts[1]:02d}"
            if len(parts) >= 3:
                pub_date += f"-{parts[2]:02d}"

    # Extract title
    title = work.get('title', [''])[0] if work.get('title') else ''

    return {
        'doi': work.get('DOI'),
        'title': title,
        'authors': authors,
        'journal': work.get('container-title', [''])[0] if work.get('container-title') else '',
        'publisher': work.get('publisher', ''),
        'volume': work.get('volume'),
        'issue': work.get('issue'),
        'pages': work.get('page'),
        'year': date_parts.get('date-parts', [[None]])[0][0] if date_parts else None,
        'published_date': pub_date,
        'type': work.get('type'),
        'issn': work.get('ISSN', []),
        'citations': work.get('is-referenced-by-count', 0),
        'references_count': work.get('references-count', 0),
        'url': work.get('URL'),
        'abstract': work.get('abstract'),
        'subject': work.get('subject', []),
        'funder': [f.get('name') for f in work.get('funder', []) if f.get('name')],
        'license': [l.get('URL') for l in work.get('license', []) if l.get('URL')],
    }


def generate_bibtex(metadata: dict) -> str:
    """Generate BibTeX entry from metadata."""
    if not metadata.get('doi'):
        return ""

    # Determine entry type
    entry_type = 'article'
    work_type = metadata.get('type', '')
    if 'book' in work_type:
        entry_type = 'book'
    elif 'proceedings' in work_type:
        entry_type = 'inproceedings'
    elif 'report' in work_type:
        entry_type = 'techreport'

    # Generate key
    first_author = metadata['authors'][0].split()[-1].lower() if metadata.get('authors') else 'unknown'
    year = metadata.get('year', 'XXXX')
    title_word = re.sub(r'[^a-z]', '', metadata.get('title', 'untitled').split()[0].lower())[:10]
    key = f"{first_author}{year}{title_word}"

    # Build BibTeX
    lines = [f"@{entry_type}{{{key},"]

    if metadata.get('title'):
        lines.append(f'  title = {{{metadata["title"]}}},')

    if metadata.get('authors'):
        authors_str = ' and '.join(metadata['authors'])
        lines.append(f'  author = {{{authors_str}}},')

    if metadata.get('journal'):
        lines.append(f'  journal = {{{metadata["journal"]}}},')

    if metadata.get('year'):
        lines.append(f'  year = {{{metadata["year"]}}},')

    if metadata.get('volume'):
        lines.append(f'  volume = {{{metadata["volume"]}}},')

    if metadata.get('issue'):
        lines.append(f'  number = {{{metadata["issue"]}}},')

    if metadata.get('pages'):
        lines.append(f'  pages = {{{metadata["pages"]}}},')

    if metadata.get('doi'):
        lines.append(f'  doi = {{{metadata["doi"]}}},')

    if metadata.get('url'):
        lines.append(f'  url = {{{metadata["url"]}}},')

    if metadata.get('publisher'):
        lines.append(f'  publisher = {{{metadata["publisher"]}}},')

    lines.append('}')

    return '\n'.join(lines)


def format_work(work: dict, index: int = None, verbose: bool = False) -> str:
    """Format a work for display."""
    metadata = extract_metadata(work)
    if not metadata:
        return "  (Invalid metadata)"

    lines = []
    prefix = f"  {index}. " if index else "  "

    lines.append(f"{prefix}{metadata.get('title', 'Unknown Title')}")

    if metadata.get('authors'):
        authors_str = ', '.join(metadata['authors'][:3])
        if len(metadata['authors']) > 3:
            authors_str += ' et al.'
        lines.append(f"      Authors: {authors_str}")

    if metadata.get('journal'):
        journal_info = metadata['journal']
        if metadata.get('volume'):
            journal_info += f" {metadata['volume']}"
            if metadata.get('issue'):
                journal_info += f"({metadata['issue']})"
        if metadata.get('pages'):
            journal_info += f": {metadata['pages']}"
        if metadata.get('year'):
            journal_info += f" ({metadata['year']})"
        lines.append(f"      Journal: {journal_info}")

    lines.append(f"      DOI: {metadata.get('doi')}")
    lines.append(f"      Citations: {metadata.get('citations', 0)}")

    if verbose:
        if metadata.get('abstract'):
            abstract = metadata['abstract'][:200] + '...' if len(metadata.get('abstract', '')) > 200 else metadata.get('abstract', '')
            # Remove HTML tags
            abstract = re.sub(r'<[^>]+>', '', abstract)
            lines.append(f"      Abstract: {abstract}")

        if metadata.get('subject'):
            lines.append(f"      Subjects: {', '.join(metadata['subject'][:5])}")

        if metadata.get('funder'):
            lines.append(f"      Funders: {', '.join(metadata['funder'])}")

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='CrossRef API Client - Access scientific publication metadata'
    )

    # Search modes
    parser.add_argument('--doi', '-d', help='Look up by DOI')
    parser.add_argument('--title', '-t', help='Search by title')
    parser.add_argument('--author', '-a', help='Search by author name')
    parser.add_argument('--query', '-q', help='General search query')

    # Options
    parser.add_argument('--bibtex', '-b', action='store_true', help='Output as BibTeX')
    parser.add_argument('--references', '-r', action='store_true', help='Show references')
    parser.add_argument('--citations', '-c', action='store_true', help='Show citation count only')
    parser.add_argument('--validate', '-V', action='store_true', help='Validate DOI exists')
    parser.add_argument('--json', '-j', action='store_true', help='Output as JSON')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--rows', '-n', type=int, default=10, help='Number of results')

    args = parser.parse_args()

    if not any([args.doi, args.title, args.author, args.query]):
        parser.print_help()
        print("\n\nExamples:")
        print('  python scripts/crossref_api.py --doi "10.1257/aer.91.5.1369"')
        print('  python scripts/crossref_api.py --title "Prospect Theory"')
        print('  python scripts/crossref_api.py --author "Ernst Fehr" --rows 20')
        print('  python scripts/crossref_api.py --doi "10.1257/aer.91.5.1369" --bibtex')
        sys.exit(1)

    client = CrossRefClient()

    # DOI lookup
    if args.doi:
        if args.validate:
            valid = client.validate_doi(args.doi)
            print(f"DOI {args.doi}: {'✅ Valid' if valid else '❌ Not found'}")
            sys.exit(0 if valid else 1)

        if args.citations:
            count = client.get_citations_count(args.doi)
            print(f"Citations: {count}")
            sys.exit(0)

        if args.references:
            refs = client.get_references(args.doi)
            print(f"References ({len(refs)}):")
            for i, ref in enumerate(refs, 1):
                title = ref.get('article-title', ref.get('unstructured', 'Unknown'))
                doi = ref.get('DOI', 'No DOI')
                print(f"  {i}. {title[:80]}")
                print(f"      DOI: {doi}")
            sys.exit(0)

        work = client.get_work(args.doi)

        if args.json:
            print(json.dumps(work, indent=2, default=str))
        elif args.bibtex:
            metadata = extract_metadata(work)
            print(generate_bibtex(metadata))
        else:
            print("=" * 70)
            print(format_work(work, verbose=args.verbose))
            print("=" * 70)

    # Title search
    elif args.title:
        works = client.search_by_title(args.title, args.rows)

        if args.json:
            print(json.dumps(works, indent=2, default=str))
        else:
            print("=" * 70)
            print(f"  CROSSREF: Title search for '{args.title}'")
            print(f"  Found: {len(works)} result(s)")
            print("=" * 70)

            for i, work in enumerate(works, 1):
                print(format_work(work, i, args.verbose))
                print()

    # Author search
    elif args.author:
        works = client.search_by_author(args.author, args.rows)

        if args.json:
            print(json.dumps(works, indent=2, default=str))
        else:
            print("=" * 70)
            print(f"  CROSSREF: Papers by '{args.author}'")
            print(f"  Found: {len(works)} result(s)")
            print("=" * 70)

            for i, work in enumerate(works, 1):
                print(format_work(work, i, args.verbose))
                print()

    # General search
    elif args.query:
        works = client.search_works(args.query, args.rows)

        if args.json:
            print(json.dumps(works, indent=2, default=str))
        else:
            print("=" * 70)
            print(f"  CROSSREF: Search for '{args.query}'")
            print(f"  Found: {len(works)} result(s)")
            print("=" * 70)

            for i, work in enumerate(works, 1):
                print(format_work(work, i, args.verbose))
                print()

    return 0


if __name__ == '__main__':
    sys.exit(main())
