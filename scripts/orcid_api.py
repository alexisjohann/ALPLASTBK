#!/usr/bin/env python3
"""
ORCID API Client - Researcher identification and publication tracking.

Features:
- Look up researchers by ORCID
- Get complete publication list
- Employment/education history
- Automatic researcher tracking

Usage:
    python scripts/orcid_api.py --orcid "0000-0002-1193-4689"
    python scripts/orcid_api.py --search "Ernst Fehr"
    python scripts/orcid_api.py --works "0000-0002-1193-4689"

API: ORCID Public API (kostenlos, kein API-Key für öffentliche Daten)
Docs: https://info.orcid.org/documentation/api-tutorials/

Author: EBF Team
Version: 1.0.0
"""

import argparse
import json
import re
import sys
from datetime import datetime
from typing import Optional, List

import requests
import yaml

ORCID_BASE_URL = "https://pub.orcid.org/v3.0"
REGISTRY_PATH = 'data/researcher-registry.yaml'


class ORCIDClient:
    """Client for ORCID Public API."""

    def __init__(self):
        self.base_url = ORCID_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
        })

    def _request(self, endpoint: str) -> dict:
        """Make API request."""
        url = f"{self.base_url}{endpoint}"

        try:
            response = self.session.get(url, timeout=30)

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

    def get_record(self, orcid: str) -> dict:
        """Get full ORCID record."""
        orcid = self._clean_orcid(orcid)
        return self._request(f"/{orcid}/record")

    def get_person(self, orcid: str) -> dict:
        """Get person details (name, biography)."""
        orcid = self._clean_orcid(orcid)
        return self._request(f"/{orcid}/person")

    def get_works(self, orcid: str) -> dict:
        """Get all works/publications."""
        orcid = self._clean_orcid(orcid)
        return self._request(f"/{orcid}/works")

    def get_employments(self, orcid: str) -> dict:
        """Get employment history."""
        orcid = self._clean_orcid(orcid)
        return self._request(f"/{orcid}/employments")

    def get_educations(self, orcid: str) -> dict:
        """Get education history."""
        orcid = self._clean_orcid(orcid)
        return self._request(f"/{orcid}/educations")

    def search(self, query: str, rows: int = 10) -> dict:
        """Search for ORCID records."""
        # ORCID search API
        url = "https://pub.orcid.org/v3.0/search/"
        params = {
            'q': query,
            'rows': rows,
        }

        try:
            response = self.session.get(url, params=params, timeout=30)
            if response.status_code == 200:
                return response.json()
            return {'error': response.status_code}
        except Exception as e:
            return {'error': str(e)}

    def _clean_orcid(self, orcid: str) -> str:
        """Clean and validate ORCID format."""
        # Remove URL prefix if present
        if 'orcid.org/' in orcid:
            orcid = orcid.split('orcid.org/')[-1]

        # Validate format (0000-0000-0000-0000)
        orcid = orcid.strip()
        if not re.match(r'^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$', orcid):
            print(f"Warning: Invalid ORCID format: {orcid}")

        return orcid


def extract_works(works_data: dict) -> list:
    """Extract publication list from ORCID works response."""
    publications = []

    for group in works_data.get('group', []):
        work_summaries = group.get('work-summary', [])
        if not work_summaries:
            continue

        # Take the first (most complete) summary
        summary = work_summaries[0]

        # Extract external IDs
        external_ids = {}
        for ext_id in summary.get('external-ids', {}).get('external-id', []):
            id_type = ext_id.get('external-id-type')
            id_value = ext_id.get('external-id-value')
            if id_type and id_value:
                external_ids[id_type] = id_value

        # Extract publication year
        pub_date = summary.get('publication-date') or {}
        year = pub_date.get('year', {}).get('value') if pub_date else None

        publications.append({
            'title': summary.get('title', {}).get('title', {}).get('value'),
            'type': summary.get('type'),
            'year': year,
            'journal': summary.get('journal-title', {}).get('value') if summary.get('journal-title') else None,
            'doi': external_ids.get('doi'),
            'pmid': external_ids.get('pmid'),
            'external_ids': external_ids,
            'put_code': summary.get('put-code'),
        })

    # Sort by year (newest first)
    publications.sort(key=lambda x: x.get('year') or '0000', reverse=True)

    return publications


def extract_employments(emp_data: dict) -> list:
    """Extract employment history."""
    employments = []

    for group in emp_data.get('affiliation-group', []):
        summaries = group.get('summaries', [])
        for item in summaries:
            summary = item.get('employment-summary', {})

            org = summary.get('organization', {})
            start = summary.get('start-date') or {}
            end = summary.get('end-date') or {}

            employments.append({
                'organization': org.get('name'),
                'department': summary.get('department-name'),
                'role': summary.get('role-title'),
                'start_year': start.get('year', {}).get('value') if start else None,
                'end_year': end.get('year', {}).get('value') if end else None,
                'country': org.get('address', {}).get('country'),
            })

    return employments


def extract_person(person_data: dict) -> dict:
    """Extract person details."""
    name_data = person_data.get('name', {}) or {}
    bio_data = person_data.get('biography', {}) or {}

    return {
        'given_name': name_data.get('given-names', {}).get('value'),
        'family_name': name_data.get('family-name', {}).get('value'),
        'credit_name': name_data.get('credit-name', {}).get('value') if name_data.get('credit-name') else None,
        'biography': bio_data.get('content'),
    }


def format_researcher(orcid: str, person: dict, employments: list, works_count: int) -> str:
    """Format researcher info for display."""
    lines = []
    lines.append("=" * 70)

    name = person.get('credit_name') or f"{person.get('given_name', '')} {person.get('family_name', '')}".strip()
    lines.append(f"  {name}")
    lines.append(f"  ORCID: {orcid}")
    lines.append("=" * 70)

    if person.get('biography'):
        bio = person['biography'][:300] + '...' if len(person.get('biography', '')) > 300 else person.get('biography', '')
        lines.append(f"\n  Biography: {bio}")

    if employments:
        lines.append("\n  📍 Employment History:")
        lines.append("-" * 40)
        for emp in employments[:5]:
            role = emp.get('role') or 'Position'
            org = emp.get('organization') or 'Unknown'
            start = emp.get('start_year') or '?'
            end = emp.get('end_year') or 'Present'
            lines.append(f"    • {role}")
            lines.append(f"      {org} ({start} - {end})")

    lines.append(f"\n  📚 Publications: {works_count}")
    lines.append("=" * 70)

    return '\n'.join(lines)


def format_works(publications: list, limit: int = 20) -> str:
    """Format publications for display."""
    lines = []
    lines.append("\n  📄 Publications:")
    lines.append("-" * 70)

    for i, pub in enumerate(publications[:limit], 1):
        title = pub.get('title') or 'Unknown Title'
        year = pub.get('year') or '?'
        journal = pub.get('journal') or ''
        doi = pub.get('doi') or ''

        lines.append(f"\n  {i}. {title}")
        if journal:
            lines.append(f"      {journal} ({year})")
        else:
            lines.append(f"      ({year})")
        if doi:
            lines.append(f"      DOI: {doi}")

    if len(publications) > limit:
        lines.append(f"\n  ... and {len(publications) - limit} more")

    return '\n'.join(lines)


def update_researcher_registry(orcid: str, person: dict, employments: list, publications: list):
    """Update researcher registry with ORCID data."""
    if not os.path.exists(REGISTRY_PATH):
        print(f"Registry not found: {REGISTRY_PATH}")
        return

    with open(REGISTRY_PATH, 'r') as f:
        registry = yaml.safe_load(f)

    researchers = registry.get('researchers', [])

    # Find researcher by ORCID
    found = False
    for researcher in researchers:
        existing_orcid = researcher.get('orcid')
        if existing_orcid and orcid in existing_orcid:
            # Update data
            researcher['orcid'] = f"https://orcid.org/{orcid}"
            researcher['orcid_last_sync'] = datetime.now().isoformat()
            researcher['orcid_works_count'] = len(publications)

            # Add any new DOIs
            existing_dois = set()
            for paper in researcher.get('paper_bibliography', {}).get('integrated', []):
                if paper.get('doi'):
                    existing_dois.add(paper['doi'].lower())

            new_papers = []
            for pub in publications:
                if pub.get('doi') and pub['doi'].lower() not in existing_dois:
                    new_papers.append({
                        'title': pub.get('title'),
                        'year': pub.get('year'),
                        'doi': pub.get('doi'),
                        'source': 'ORCID',
                    })

            if new_papers:
                if 'paper_bibliography' not in researcher:
                    researcher['paper_bibliography'] = {}
                if 'not_integrated' not in researcher['paper_bibliography']:
                    researcher['paper_bibliography']['not_integrated'] = []
                researcher['paper_bibliography']['not_integrated'].extend(new_papers)

            found = True
            print(f"Updated {researcher.get('name')} with {len(new_papers)} new papers")
            break

    if found:
        with open(REGISTRY_PATH, 'w') as f:
            yaml.dump(registry, f, default_flow_style=False, allow_unicode=True)


def main():
    parser = argparse.ArgumentParser(
        description='ORCID API Client - Researcher identification and tracking'
    )

    # Lookup modes
    parser.add_argument('--orcid', '-o', help='Look up by ORCID')
    parser.add_argument('--search', '-s', help='Search by name')
    parser.add_argument('--works', '-w', help='Get works for ORCID')

    # Options
    parser.add_argument('--json', '-j', action='store_true', help='Output as JSON')
    parser.add_argument('--update-registry', '-u', action='store_true',
                        help='Update researcher registry with ORCID data')
    parser.add_argument('--rows', '-n', type=int, default=10, help='Number of results')

    args = parser.parse_args()

    if not any([args.orcid, args.search, args.works]):
        parser.print_help()
        print("\n\nExamples:")
        print('  python scripts/orcid_api.py --orcid "0000-0002-1193-4689"')
        print('  python scripts/orcid_api.py --search "Ernst Fehr"')
        print('  python scripts/orcid_api.py --works "0000-0002-1193-4689"')
        print('  python scripts/orcid_api.py --orcid "0000-0002-1193-4689" --update-registry')
        sys.exit(1)

    client = ORCIDClient()

    # ORCID lookup
    if args.orcid:
        orcid = client._clean_orcid(args.orcid)

        person_data = client.get_person(orcid)
        person = extract_person(person_data)

        emp_data = client.get_employments(orcid)
        employments = extract_employments(emp_data)

        works_data = client.get_works(orcid)
        publications = extract_works(works_data)

        if args.json:
            output = {
                'orcid': orcid,
                'person': person,
                'employments': employments,
                'publications': publications,
            }
            print(json.dumps(output, indent=2, default=str))
        else:
            print(format_researcher(orcid, person, employments, len(publications)))
            print(format_works(publications, 10))

        if args.update_registry:
            import os
            update_researcher_registry(orcid, person, employments, publications)

    # Search
    elif args.search:
        result = client.search(args.search, args.rows)

        if args.json:
            print(json.dumps(result, indent=2, default=str))
        else:
            print("=" * 70)
            print(f"  ORCID: Search for '{args.search}'")
            print("=" * 70)

            for item in result.get('result', []):
                record = item.get('orcid-identifier', {})
                orcid = record.get('path', '')

                # Get basic info
                person_data = client.get_person(orcid)
                person = extract_person(person_data)
                name = f"{person.get('given_name', '')} {person.get('family_name', '')}".strip()

                print(f"\n  {name}")
                print(f"      ORCID: {orcid}")
                print(f"      URL: https://orcid.org/{orcid}")

    # Works only
    elif args.works:
        orcid = client._clean_orcid(args.works)
        works_data = client.get_works(orcid)
        publications = extract_works(works_data)

        if args.json:
            print(json.dumps(publications, indent=2, default=str))
        else:
            print("=" * 70)
            print(f"  ORCID Works: {orcid}")
            print(f"  Total: {len(publications)}")
            print("=" * 70)
            print(format_works(publications, args.rows))

    return 0


if __name__ == '__main__':
    import os
    sys.exit(main())
