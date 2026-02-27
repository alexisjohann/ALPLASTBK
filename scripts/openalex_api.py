#!/usr/bin/env python3
"""
OpenAlex API Client - Access 250M+ scientific publications.

Features:
- Paper search by DOI, title, keywords
- Author profiles with disambiguation
- Institution data
- Concept/topic tagging
- Citation networks
- Related works

Usage:
    python scripts/openalex_api.py --doi "10.1257/aer.91.5.1369"
    python scripts/openalex_api.py --author "Ernst Fehr"
    python scripts/openalex_api.py --author-id "A5006065034"
    python scripts/openalex_api.py --query "behavioral economics"
    python scripts/openalex_api.py --institution "University of Zurich"
    python scripts/openalex_api.py --related "W2140827718"

API: OpenAlex (kostenlos, kein API-Key erforderlich)
Docs: https://docs.openalex.org/

Author: EBF Team
Version: 1.0.0
"""

import argparse
import json
import re
import sys
import time
from datetime import datetime
from typing import Optional, List
from urllib.parse import quote

import requests

OPENALEX_BASE_URL = "https://api.openalex.org"
USER_AGENT = "EBF-Framework/1.0 (mailto:research@fehradvice.com)"


class OpenAlexClient:
    """Client for OpenAlex API."""

    def __init__(self, email: str = None):
        self.base_url = OPENALEX_BASE_URL
        self.session = requests.Session()
        # Polite pool with email
        self.params = {}
        if email:
            self.params['mailto'] = email
        else:
            self.params['mailto'] = 'research@fehradvice.com'

    def _request(self, endpoint: str, params: dict = None) -> dict:
        """Make API request."""
        url = f"{self.base_url}{endpoint}"
        all_params = {**self.params, **(params or {})}

        try:
            response = self.session.get(url, params=all_params, timeout=30)

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return {'error': 'not_found'}
            else:
                print(f"API Error: {response.status_code}")
                return {'error': response.status_code}

        except Exception as e:
            print(f"Request error: {e}")
            return {'error': str(e)}

    # =========================================================================
    # WORKS (Papers)
    # =========================================================================

    def get_work(self, work_id: str) -> dict:
        """Get a single work by OpenAlex ID or DOI."""
        if work_id.startswith('10.'):
            work_id = f"https://doi.org/{work_id}"
        return self._request(f"/works/{quote(work_id, safe='')}")

    def search_works(self, query: str, filters: dict = None,
                     per_page: int = 25, page: int = 1) -> dict:
        """Search for works."""
        params = {
            'search': query,
            'per_page': per_page,
            'page': page,
        }

        if filters:
            filter_parts = []
            for key, value in filters.items():
                filter_parts.append(f"{key}:{value}")
            params['filter'] = ','.join(filter_parts)

        return self._request('/works', params)

    def get_works_by_author(self, author_id: str, per_page: int = 50) -> dict:
        """Get all works by an author."""
        # Clean author ID
        if not author_id.startswith('A'):
            author_id = f"A{author_id}"

        params = {
            'filter': f'author.id:{author_id}',
            'per_page': per_page,
            'sort': 'publication_date:desc',
        }
        return self._request('/works', params)

    def get_related_works(self, work_id: str, per_page: int = 10) -> list:
        """Get related works for a paper."""
        work = self.get_work(work_id)
        if 'related_works' in work:
            related_ids = work['related_works'][:per_page]
            # Fetch details for each
            related = []
            for rid in related_ids:
                related.append(self.get_work(rid))
                time.sleep(0.1)  # Rate limiting
            return related
        return []

    def get_citations(self, work_id: str, per_page: int = 25) -> dict:
        """Get works that cite this paper."""
        params = {
            'filter': f'cites:{work_id}',
            'per_page': per_page,
            'sort': 'cited_by_count:desc',
        }
        return self._request('/works', params)

    def get_references(self, work_id: str) -> list:
        """Get references from a paper."""
        work = self.get_work(work_id)
        if 'referenced_works' in work:
            return work['referenced_works']
        return []

    # =========================================================================
    # AUTHORS
    # =========================================================================

    def get_author(self, author_id: str) -> dict:
        """Get author by OpenAlex ID."""
        if not author_id.startswith('A'):
            author_id = f"A{author_id}"
        return self._request(f"/authors/{author_id}")

    def search_authors(self, query: str, per_page: int = 10) -> dict:
        """Search for authors by name."""
        params = {
            'search': query,
            'per_page': per_page,
        }
        return self._request('/authors', params)

    def get_author_by_orcid(self, orcid: str) -> dict:
        """Get author by ORCID."""
        if not orcid.startswith('https://orcid.org/'):
            orcid = f"https://orcid.org/{orcid}"
        return self._request(f"/authors/{quote(orcid, safe='')}")

    # =========================================================================
    # INSTITUTIONS
    # =========================================================================

    def get_institution(self, institution_id: str) -> dict:
        """Get institution by OpenAlex ID."""
        if not institution_id.startswith('I'):
            institution_id = f"I{institution_id}"
        return self._request(f"/institutions/{institution_id}")

    def search_institutions(self, query: str, per_page: int = 10) -> dict:
        """Search for institutions."""
        params = {
            'search': query,
            'per_page': per_page,
        }
        return self._request('/institutions', params)

    # =========================================================================
    # CONCEPTS (Topics)
    # =========================================================================

    def get_concept(self, concept_id: str) -> dict:
        """Get concept by OpenAlex ID."""
        if not concept_id.startswith('C'):
            concept_id = f"C{concept_id}"
        return self._request(f"/concepts/{concept_id}")

    def search_concepts(self, query: str, per_page: int = 10) -> dict:
        """Search for concepts."""
        params = {
            'search': query,
            'per_page': per_page,
        }
        return self._request('/concepts', params)

    def get_works_by_concept(self, concept_id: str, per_page: int = 25) -> dict:
        """Get works tagged with a concept."""
        params = {
            'filter': f'concepts.id:{concept_id}',
            'per_page': per_page,
            'sort': 'cited_by_count:desc',
        }
        return self._request('/works', params)


def extract_work_metadata(work: dict) -> dict:
    """Extract clean metadata from OpenAlex work."""
    if not work or 'id' not in work:
        return {}

    # Extract authors
    authors = []
    for authorship in work.get('authorships', []):
        author = authorship.get('author', {})
        name = author.get('display_name')
        if name:
            authors.append({
                'name': name,
                'id': author.get('id', '').replace('https://openalex.org/', ''),
                'orcid': author.get('orcid'),
            })

    # Extract concepts
    concepts = []
    for concept in work.get('concepts', []):
        if concept.get('score', 0) > 0.3:  # Only high-confidence concepts
            concepts.append({
                'name': concept.get('display_name'),
                'id': concept.get('id', '').replace('https://openalex.org/', ''),
                'score': concept.get('score'),
            })

    return {
        'id': work.get('id', '').replace('https://openalex.org/', ''),
        'doi': work.get('doi', '').replace('https://doi.org/', '') if work.get('doi') else None,
        'title': work.get('title'),
        'authors': authors,
        'publication_year': work.get('publication_year'),
        'publication_date': work.get('publication_date'),
        'journal': work.get('primary_location', {}).get('source', {}).get('display_name') if work.get('primary_location') else None,
        'type': work.get('type'),
        'open_access': work.get('open_access', {}).get('is_oa'),
        'oa_url': work.get('open_access', {}).get('oa_url'),
        'cited_by_count': work.get('cited_by_count', 0),
        'concepts': concepts,
        'abstract': work.get('abstract_inverted_index'),  # Needs reconstruction
        'referenced_works_count': len(work.get('referenced_works', [])),
        'related_works_count': len(work.get('related_works', [])),
    }


def extract_author_metadata(author: dict) -> dict:
    """Extract clean metadata from OpenAlex author."""
    if not author or 'id' not in author:
        return {}

    # Get affiliations
    affiliations = []
    for aff in author.get('affiliations', []):
        inst = aff.get('institution', {})
        affiliations.append({
            'name': inst.get('display_name'),
            'id': inst.get('id', '').replace('https://openalex.org/', ''),
            'country': inst.get('country_code'),
            'years': aff.get('years', []),
        })

    return {
        'id': author.get('id', '').replace('https://openalex.org/', ''),
        'orcid': author.get('orcid'),
        'name': author.get('display_name'),
        'works_count': author.get('works_count', 0),
        'cited_by_count': author.get('cited_by_count', 0),
        'h_index': author.get('summary_stats', {}).get('h_index'),
        'i10_index': author.get('summary_stats', {}).get('i10_index'),
        'affiliations': affiliations,
        'last_known_institution': author.get('last_known_institution', {}).get('display_name'),
        'concepts': [c.get('display_name') for c in author.get('x_concepts', [])[:10]],
    }


def format_work(work: dict, index: int = None, verbose: bool = False) -> str:
    """Format a work for display."""
    metadata = extract_work_metadata(work)
    if not metadata:
        return "  (Invalid work)"

    lines = []
    prefix = f"  {index}. " if index else "  "

    lines.append(f"{prefix}{metadata.get('title', 'Unknown Title')}")

    if metadata.get('authors'):
        authors_str = ', '.join(a['name'] for a in metadata['authors'][:3])
        if len(metadata['authors']) > 3:
            authors_str += ' et al.'
        lines.append(f"      Authors: {authors_str}")

    if metadata.get('journal'):
        journal_info = f"{metadata['journal']} ({metadata.get('publication_year', '?')})"
        lines.append(f"      Journal: {journal_info}")

    if metadata.get('doi'):
        lines.append(f"      DOI: {metadata['doi']}")

    lines.append(f"      OpenAlex: {metadata.get('id')}")
    lines.append(f"      Citations: {metadata.get('cited_by_count', 0)}")

    if metadata.get('open_access'):
        lines.append(f"      Open Access: ✅ {metadata.get('oa_url', '')}")

    if verbose and metadata.get('concepts'):
        concepts_str = ', '.join(c['name'] for c in metadata['concepts'][:5])
        lines.append(f"      Concepts: {concepts_str}")

    return '\n'.join(lines)


def format_author(author: dict, verbose: bool = False) -> str:
    """Format an author for display."""
    metadata = extract_author_metadata(author)
    if not metadata:
        return "  (Invalid author)"

    lines = []
    lines.append(f"  {metadata.get('name', 'Unknown')}")
    lines.append(f"      OpenAlex ID: {metadata.get('id')}")

    if metadata.get('orcid'):
        lines.append(f"      ORCID: {metadata['orcid']}")

    if metadata.get('last_known_institution'):
        lines.append(f"      Institution: {metadata['last_known_institution']}")

    lines.append(f"      Works: {metadata.get('works_count', 0)}")
    lines.append(f"      Citations: {metadata.get('cited_by_count', 0)}")

    if metadata.get('h_index'):
        lines.append(f"      h-index: {metadata['h_index']}")

    if verbose and metadata.get('concepts'):
        lines.append(f"      Research Areas: {', '.join(metadata['concepts'][:5])}")

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='OpenAlex API Client - Access 250M+ scientific publications'
    )

    # Search modes
    parser.add_argument('--doi', '-d', help='Look up work by DOI')
    parser.add_argument('--work', '-w', help='Look up work by OpenAlex ID')
    parser.add_argument('--author', '-a', help='Search for author by name')
    parser.add_argument('--author-id', '-A', help='Get author by OpenAlex ID')
    parser.add_argument('--orcid', '-O', help='Get author by ORCID')
    parser.add_argument('--query', '-q', help='Search works by query')
    parser.add_argument('--institution', '-i', help='Search institutions')
    parser.add_argument('--concept', '-c', help='Search concepts/topics')
    parser.add_argument('--related', '-R', help='Get related works for a paper')
    parser.add_argument('--citations', '-C', help='Get papers citing this work')

    # Options
    parser.add_argument('--json', '-j', action='store_true', help='Output as JSON')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--rows', '-n', type=int, default=10, help='Number of results')

    args = parser.parse_args()

    if not any([args.doi, args.work, args.author, args.author_id, args.orcid,
                args.query, args.institution, args.concept, args.related, args.citations]):
        parser.print_help()
        print("\n\nExamples:")
        print('  python scripts/openalex_api.py --doi "10.1257/aer.91.5.1369"')
        print('  python scripts/openalex_api.py --author "Ernst Fehr"')
        print('  python scripts/openalex_api.py --orcid "0000-0002-1193-4689"')
        print('  python scripts/openalex_api.py --query "behavioral economics" --rows 20')
        print('  python scripts/openalex_api.py --related "W2140827718"')
        sys.exit(1)

    client = OpenAlexClient()

    # DOI lookup
    if args.doi:
        work = client.get_work(args.doi)
        if args.json:
            print(json.dumps(work, indent=2, default=str))
        else:
            print("=" * 70)
            print(format_work(work, verbose=args.verbose))
            print("=" * 70)

    # Work by ID
    elif args.work:
        work = client.get_work(args.work)
        if args.json:
            print(json.dumps(work, indent=2, default=str))
        else:
            print("=" * 70)
            print(format_work(work, verbose=args.verbose))
            print("=" * 70)

    # Author search
    elif args.author:
        result = client.search_authors(args.author, args.rows)
        authors = result.get('results', [])

        if args.json:
            print(json.dumps(authors, indent=2, default=str))
        else:
            print("=" * 70)
            print(f"  OPENALEX: Authors matching '{args.author}'")
            print(f"  Found: {result.get('meta', {}).get('count', 0)} total")
            print("=" * 70)

            for author in authors:
                print(format_author(author, args.verbose))
                print()

    # Author by ID
    elif args.author_id:
        author = client.get_author(args.author_id)
        if args.json:
            print(json.dumps(author, indent=2, default=str))
        else:
            print("=" * 70)
            print(format_author(author, args.verbose))

            # Also get recent works
            works = client.get_works_by_author(args.author_id, 10)
            if works.get('results'):
                print("\n  Recent Works:")
                print("-" * 70)
                for i, work in enumerate(works['results'][:5], 1):
                    print(format_work(work, i))
                    print()
            print("=" * 70)

    # Author by ORCID
    elif args.orcid:
        author = client.get_author_by_orcid(args.orcid)
        if args.json:
            print(json.dumps(author, indent=2, default=str))
        else:
            print("=" * 70)
            print(format_author(author, args.verbose))
            print("=" * 70)

    # Query search
    elif args.query:
        result = client.search_works(args.query, per_page=args.rows)
        works = result.get('results', [])

        if args.json:
            print(json.dumps(works, indent=2, default=str))
        else:
            print("=" * 70)
            print(f"  OPENALEX: Search for '{args.query}'")
            print(f"  Found: {result.get('meta', {}).get('count', 0)} total")
            print("=" * 70)

            for i, work in enumerate(works, 1):
                print(format_work(work, i, args.verbose))
                print()

    # Institution search
    elif args.institution:
        result = client.search_institutions(args.institution, args.rows)
        institutions = result.get('results', [])

        if args.json:
            print(json.dumps(institutions, indent=2, default=str))
        else:
            print("=" * 70)
            print(f"  OPENALEX: Institutions matching '{args.institution}'")
            print("=" * 70)

            for inst in institutions:
                print(f"  {inst.get('display_name')}")
                print(f"      ID: {inst.get('id', '').replace('https://openalex.org/', '')}")
                print(f"      Country: {inst.get('country_code')}")
                print(f"      Works: {inst.get('works_count', 0)}")
                print(f"      Citations: {inst.get('cited_by_count', 0)}")
                print()

    # Concept search
    elif args.concept:
        result = client.search_concepts(args.concept, args.rows)
        concepts = result.get('results', [])

        if args.json:
            print(json.dumps(concepts, indent=2, default=str))
        else:
            print("=" * 70)
            print(f"  OPENALEX: Concepts matching '{args.concept}'")
            print("=" * 70)

            for concept in concepts:
                print(f"  {concept.get('display_name')}")
                print(f"      ID: {concept.get('id', '').replace('https://openalex.org/', '')}")
                print(f"      Level: {concept.get('level')}")
                print(f"      Works: {concept.get('works_count', 0)}")
                print()

    # Related works
    elif args.related:
        related = client.get_related_works(args.related, args.rows)

        if args.json:
            print(json.dumps(related, indent=2, default=str))
        else:
            print("=" * 70)
            print(f"  OPENALEX: Related works for {args.related}")
            print("=" * 70)

            for i, work in enumerate(related, 1):
                print(format_work(work, i, args.verbose))
                print()

    # Citations
    elif args.citations:
        result = client.get_citations(args.citations, args.rows)
        works = result.get('results', [])

        if args.json:
            print(json.dumps(works, indent=2, default=str))
        else:
            print("=" * 70)
            print(f"  OPENALEX: Papers citing {args.citations}")
            print(f"  Found: {result.get('meta', {}).get('count', 0)} total")
            print("=" * 70)

            for i, work in enumerate(works, 1):
                print(format_work(work, i, args.verbose))
                print()

    return 0


if __name__ == '__main__':
    sys.exit(main())
