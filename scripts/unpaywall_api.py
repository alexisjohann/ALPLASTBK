#!/usr/bin/env python3
"""
Unpaywall API Client - Find Open Access versions of papers.

Features:
- Find legal OA versions for any DOI
- Check OA status (gold, green, hybrid, bronze)
- Get direct PDF links
- Batch processing for BibTeX

Usage:
    python scripts/unpaywall_api.py --doi "10.1257/aer.91.5.1369"
    python scripts/unpaywall_api.py --batch bibliography/bcm_master.bib
    python scripts/unpaywall_api.py --doi "10.1257/aer.91.5.1369" --download

API: Unpaywall (kostenlos, Email erforderlich)
Docs: https://unpaywall.org/products/api

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
from typing import Optional, List
from urllib.parse import quote

import requests
import yaml

UNPAYWALL_BASE_URL = "https://api.unpaywall.org/v2"
EMAIL = "research@fehradvice.com"


class UnpaywallClient:
    """Client for Unpaywall API."""

    def __init__(self, email: str = EMAIL):
        self.base_url = UNPAYWALL_BASE_URL
        self.email = email
        self.session = requests.Session()

    def get_paper(self, doi: str) -> dict:
        """Get OA information for a DOI."""
        # Clean DOI
        doi = self._clean_doi(doi)

        url = f"{self.base_url}/{quote(doi, safe='')}"
        params = {'email': self.email}

        try:
            response = self.session.get(url, params=params, timeout=30)

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return {'error': 'not_found', 'doi': doi}
            else:
                return {'error': response.status_code, 'doi': doi}

        except Exception as e:
            return {'error': str(e), 'doi': doi}

    def _clean_doi(self, doi: str) -> str:
        """Clean DOI format."""
        doi = doi.strip()
        if doi.startswith('https://doi.org/'):
            doi = doi[16:]
        elif doi.startswith('http://doi.org/'):
            doi = doi[15:]
        elif doi.startswith('doi:'):
            doi = doi[4:]
        return doi

    def is_open_access(self, doi: str) -> bool:
        """Check if a paper is available OA."""
        result = self.get_paper(doi)
        return result.get('is_oa', False)

    def get_pdf_url(self, doi: str) -> Optional[str]:
        """Get best PDF URL for a paper."""
        result = self.get_paper(doi)
        best = result.get('best_oa_location', {})
        if best:
            return best.get('url_for_pdf') or best.get('url')
        return None


def extract_oa_info(data: dict) -> dict:
    """Extract OA information from Unpaywall response."""
    if 'error' in data:
        return {
            'doi': data.get('doi'),
            'is_oa': False,
            'error': data.get('error'),
        }

    best_location = data.get('best_oa_location') or {}

    # Get all OA locations
    oa_locations = []
    for loc in data.get('oa_locations', []):
        oa_locations.append({
            'url': loc.get('url'),
            'url_for_pdf': loc.get('url_for_pdf'),
            'host_type': loc.get('host_type'),  # publisher, repository
            'license': loc.get('license'),
            'version': loc.get('version'),  # publishedVersion, acceptedVersion
        })

    return {
        'doi': data.get('doi'),
        'title': data.get('title'),
        'is_oa': data.get('is_oa', False),
        'oa_status': data.get('oa_status'),  # gold, green, hybrid, bronze, closed
        'journal': data.get('journal_name'),
        'publisher': data.get('publisher'),
        'year': data.get('year'),
        'best_oa_url': best_location.get('url'),
        'best_pdf_url': best_location.get('url_for_pdf'),
        'best_host': best_location.get('host_type'),
        'best_license': best_location.get('license'),
        'best_version': best_location.get('version'),
        'oa_locations': oa_locations,
    }


def format_oa_info(info: dict) -> str:
    """Format OA info for display."""
    lines = []

    if info.get('error'):
        lines.append(f"  ❌ DOI: {info.get('doi')}")
        lines.append(f"      Error: {info.get('error')}")
        return '\n'.join(lines)

    # Status emoji
    status = info.get('oa_status', 'closed')
    status_emoji = {
        'gold': '🥇',
        'hybrid': '🥈',
        'green': '🥉',
        'bronze': '🟤',
        'closed': '🔒',
    }.get(status, '❓')

    lines.append(f"  {status_emoji} {info.get('title', 'Unknown')[:60]}...")
    lines.append(f"      DOI: {info.get('doi')}")
    lines.append(f"      OA Status: {status.upper()}")

    if info.get('is_oa'):
        lines.append(f"      ✅ Open Access: Yes")
        if info.get('best_pdf_url'):
            lines.append(f"      📄 PDF: {info['best_pdf_url']}")
        elif info.get('best_oa_url'):
            lines.append(f"      🔗 URL: {info['best_oa_url']}")
        if info.get('best_license'):
            lines.append(f"      📜 License: {info['best_license']}")
        if info.get('best_version'):
            lines.append(f"      📋 Version: {info['best_version']}")
    else:
        lines.append(f"      ❌ Open Access: No")

    return '\n'.join(lines)


def process_bibtex(filepath: str, client: UnpaywallClient, limit: int = 100) -> dict:
    """Process BibTeX file and find OA versions."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract DOIs
    dois = re.findall(r'doi\s*=\s*[{"]([^}"]+)[}"]', content, re.IGNORECASE)

    results = {
        'total': len(dois),
        'processed': 0,
        'open_access': 0,
        'closed': 0,
        'errors': 0,
        'papers': [],
    }

    print(f"Found {len(dois)} DOIs in {filepath}")
    print(f"Processing {min(limit, len(dois))} papers...\n")

    for i, doi in enumerate(dois[:limit]):
        if (i + 1) % 10 == 0:
            print(f"  Progress: {i + 1}/{min(limit, len(dois))}")

        data = client.get_paper(doi)
        info = extract_oa_info(data)
        results['papers'].append(info)

        if info.get('error'):
            results['errors'] += 1
        elif info.get('is_oa'):
            results['open_access'] += 1
        else:
            results['closed'] += 1

        results['processed'] += 1

        # Rate limiting
        time.sleep(0.1)

    return results


def generate_report(results: dict) -> str:
    """Generate OA report."""
    lines = []
    lines.append("=" * 70)
    lines.append("  UNPAYWALL OPEN ACCESS REPORT")
    lines.append(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("=" * 70)

    total = results['processed']
    oa = results['open_access']
    closed = results['closed']

    lines.append(f"\n  Summary:")
    lines.append(f"    Total processed: {total}")
    lines.append(f"    Open Access: {oa} ({100*oa/total:.1f}%)" if total > 0 else "    Open Access: 0")
    lines.append(f"    Closed: {closed} ({100*closed/total:.1f}%)" if total > 0 else "    Closed: 0")
    lines.append(f"    Errors: {results['errors']}")

    # OA breakdown by status
    status_counts = {}
    for paper in results['papers']:
        status = paper.get('oa_status', 'unknown')
        status_counts[status] = status_counts.get(status, 0) + 1

    lines.append(f"\n  OA Status Breakdown:")
    for status, count in sorted(status_counts.items(), key=lambda x: -x[1]):
        emoji = {'gold': '🥇', 'hybrid': '🥈', 'green': '🥉', 'bronze': '🟤', 'closed': '🔒'}.get(status, '❓')
        lines.append(f"    {emoji} {status}: {count}")

    # List OA papers with PDFs
    oa_papers = [p for p in results['papers'] if p.get('is_oa') and p.get('best_pdf_url')]
    if oa_papers:
        lines.append(f"\n  Papers with PDF available ({len(oa_papers)}):")
        lines.append("-" * 70)
        for paper in oa_papers[:20]:
            title = paper.get('title', 'Unknown')[:50]
            lines.append(f"    • {title}...")
            lines.append(f"      {paper.get('best_pdf_url')}")

    lines.append("\n" + "=" * 70)

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Unpaywall API Client - Find Open Access versions'
    )

    # Lookup modes
    parser.add_argument('--doi', '-d', help='Check single DOI')
    parser.add_argument('--batch', '-b', help='Process BibTeX file')

    # Options
    parser.add_argument('--json', '-j', action='store_true', help='Output as JSON')
    parser.add_argument('--pdf-only', '-p', action='store_true', help='Only show papers with PDF')
    parser.add_argument('--download', '-D', action='store_true', help='Download PDF (single DOI)')
    parser.add_argument('--limit', '-n', type=int, default=100, help='Limit for batch processing')
    parser.add_argument('--output', '-o', help='Output file for report')

    args = parser.parse_args()

    if not any([args.doi, args.batch]):
        parser.print_help()
        print("\n\nExamples:")
        print('  python scripts/unpaywall_api.py --doi "10.1257/aer.91.5.1369"')
        print('  python scripts/unpaywall_api.py --batch bibliography/bcm_master.bib')
        print('  python scripts/unpaywall_api.py --batch bibliography/bcm_master.bib --pdf-only')
        sys.exit(1)

    client = UnpaywallClient()

    # Single DOI
    if args.doi:
        data = client.get_paper(args.doi)
        info = extract_oa_info(data)

        if args.json:
            print(json.dumps(info, indent=2, default=str))
        else:
            print("=" * 70)
            print(format_oa_info(info))
            print("=" * 70)

        if args.download and info.get('best_pdf_url'):
            print(f"\nDownloading PDF...")
            # Download PDF
            try:
                response = requests.get(info['best_pdf_url'], timeout=60)
                if response.status_code == 200:
                    filename = f"{args.doi.replace('/', '_')}.pdf"
                    with open(filename, 'wb') as f:
                        f.write(response.content)
                    print(f"✅ Saved to: {filename}")
                else:
                    print(f"❌ Download failed: {response.status_code}")
            except Exception as e:
                print(f"❌ Download error: {e}")

    # Batch processing
    elif args.batch:
        if not os.path.exists(args.batch):
            print(f"Error: File not found: {args.batch}")
            sys.exit(1)

        results = process_bibtex(args.batch, client, args.limit)

        if args.json:
            print(json.dumps(results, indent=2, default=str))
        else:
            report = generate_report(results)
            print(report)

            if args.output:
                with open(args.output, 'w') as f:
                    f.write(report)
                print(f"\n✅ Report saved to: {args.output}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
