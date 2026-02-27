#!/usr/bin/env python3
"""
DOI Lookup Script for EBF Papers
================================
Uses CrossRef API to find DOIs for papers in bcm_master.bib

Usage:
    python scripts/lookup_paper_dois.py --analyze          # Show papers without DOI
    python scripts/lookup_paper_dois.py --lookup KEY       # Lookup single paper
    python scripts/lookup_paper_dois.py --batch N          # Lookup N papers (dry-run)
    python scripts/lookup_paper_dois.py --batch N --execute # Apply DOIs
    python scripts/lookup_paper_dois.py --priority         # Lookup high-priority papers first
"""

import re
import sys
import json
import time
import argparse
import urllib.request
import urllib.parse
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Tuple

BIB_FILE = Path("bibliography/bcm_master.bib")
CROSSREF_API = "https://api.crossref.org/works"
USER_AGENT = "EBF-Framework/1.0 (mailto:research@fehradvice.com)"

@dataclass
class PaperInfo:
    key: str
    title: str = ""
    author: str = ""
    year: str = ""
    journal: str = ""
    doi: Optional[str] = None
    reference_count: int = 0
    has_pap_prefix: bool = False

def parse_bibtex() -> Dict[str, PaperInfo]:
    """Parse BibTeX file and extract paper metadata."""
    content = BIB_FILE.read_text()
    papers = {}

    # Match each entry
    pattern = r'@\w+\{([^,]+),\s*(.*?)(?=\n@|\Z)'
    for match in re.finditer(pattern, content, re.DOTALL):
        key = match.group(1)
        entry = match.group(2)

        paper = PaperInfo(key=key)
        paper.has_pap_prefix = key.startswith('PAP-')

        # Extract fields
        title_match = re.search(r'title\s*=\s*\{([^}]+)\}', entry, re.IGNORECASE)
        if title_match:
            paper.title = title_match.group(1).strip()

        author_match = re.search(r'author\s*=\s*\{([^}]+)\}', entry, re.IGNORECASE)
        if author_match:
            paper.author = author_match.group(1).strip()

        year_match = re.search(r'year\s*=\s*\{?(\d{4})\}?', entry, re.IGNORECASE)
        if year_match:
            paper.year = year_match.group(1)

        journal_match = re.search(r'journal\s*=\s*\{([^}]+)\}', entry, re.IGNORECASE)
        if journal_match:
            paper.journal = journal_match.group(1).strip()

        doi_match = re.search(r'doi\s*=\s*\{([^}]+)\}', entry, re.IGNORECASE)
        if doi_match:
            doi_val = doi_match.group(1).strip()
            if doi_val.lower() != 'null' and doi_val:
                paper.doi = doi_val

        ref_match = re.search(r'ebf_reference_count\s*=\s*\{(\d+)\}', entry)
        if ref_match:
            paper.reference_count = int(ref_match.group(1))

        papers[key] = paper

    return papers

def crossref_lookup(title: str, author: str = "", year: str = "") -> Optional[Dict]:
    """Query CrossRef API for paper DOI."""
    # Build query
    query_parts = []
    if title:
        # Clean title
        clean_title = re.sub(r'[{}\\]', '', title)
        query_parts.append(clean_title)

    if author:
        # Extract first author's last name
        first_author = author.split(' and ')[0] if ' and ' in author else author
        last_name = first_author.split(',')[0] if ',' in first_author else first_author.split()[-1]
        query_parts.append(last_name)

    if not query_parts:
        return None

    query = ' '.join(query_parts)

    # Build URL
    params = {
        'query': query,
        'rows': 5,
        'select': 'DOI,title,author,published-print,container-title,score'
    }

    url = f"{CROSSREF_API}?{urllib.parse.urlencode(params)}"

    # Make request
    req = urllib.request.Request(url)
    req.add_header('User-Agent', USER_AGENT)

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())

            if data['status'] == 'ok' and data['message']['items']:
                items = data['message']['items']

                # Find best match
                for item in items:
                    item_title = item.get('title', [''])[0].lower() if item.get('title') else ''
                    search_title = title.lower()

                    # Check title similarity
                    if item_title and search_title:
                        # Simple word overlap check
                        item_words = set(re.findall(r'\w+', item_title))
                        search_words = set(re.findall(r'\w+', search_title))

                        if len(item_words) > 0 and len(search_words) > 0:
                            overlap = len(item_words & search_words) / max(len(item_words), len(search_words))

                            if overlap > 0.5:  # At least 50% word overlap
                                # Verify year if available
                                item_year = None
                                if 'published-print' in item and item['published-print'].get('date-parts'):
                                    item_year = str(item['published-print']['date-parts'][0][0])

                                if year and item_year and year != item_year:
                                    continue  # Year mismatch

                                return {
                                    'doi': item['DOI'],
                                    'title': item.get('title', [''])[0],
                                    'score': item.get('score', 0),
                                    'year': item_year
                                }

                # If no good match found, return top result with warning
                top = items[0]
                return {
                    'doi': top['DOI'],
                    'title': top.get('title', [''])[0],
                    'score': top.get('score', 0),
                    'confidence': 'low'
                }

    except Exception as e:
        print(f"  ⚠️ CrossRef error: {e}")
        return None

    return None

def update_bibtex_doi(key: str, doi: str) -> bool:
    """Update DOI in BibTeX entry."""
    content = BIB_FILE.read_text()

    # Find the entry
    if key.startswith('PAP-'):
        search_key = key
    else:
        search_key = key

    # Pattern to find the entry
    entry_pattern = r'(@\w+\{' + re.escape(search_key) + r',.*?)(?=\n@|\Z)'
    match = re.search(entry_pattern, content, re.DOTALL)

    if not match:
        return False

    entry = match.group(1)

    # Check if DOI field exists
    if re.search(r'doi\s*=', entry, re.IGNORECASE):
        # Update existing DOI
        new_entry = re.sub(
            r'(doi\s*=\s*\{)[^}]*(\})',
            r'\g<1>' + doi + r'\g<2>',
            entry,
            flags=re.IGNORECASE
        )
    else:
        # Add DOI field before the closing brace or before ebf_ fields
        if 'ebf_reference_count' in entry:
            new_entry = re.sub(
                r'(,\s*)(ebf_reference_count)',
                r',\n  doi = {' + doi + r'},\n  \g<2>',
                entry
            )
        else:
            # Add before closing
            new_entry = re.sub(
                r'(\s*)\}$',
                r',\n  doi = {' + doi + r'}\n}',
                entry
            )

    # Replace in content
    new_content = content.replace(entry, new_entry)
    BIB_FILE.write_text(new_content)

    return True

def analyze_papers(papers: Dict[str, PaperInfo]):
    """Show analysis of papers without DOI."""
    print("=" * 80)
    print("PAPERS WITHOUT DOI")
    print("=" * 80)
    print()

    no_doi = [p for p in papers.values() if not p.doi and not p.has_pap_prefix]
    with_doi = [p for p in papers.values() if p.doi and not p.has_pap_prefix]
    migrated = [p for p in papers.values() if p.has_pap_prefix]

    print(f"📚 Total papers: {len(papers)}")
    print(f"✅ Migrated (PAP-): {len(migrated)}")
    print(f"🔗 With DOI: {len(with_doi)}")
    print(f"❌ Need DOI: {len(no_doi)}")
    print()

    # Sort by reference count (most cited first)
    no_doi.sort(key=lambda p: -p.reference_count)

    print("📊 High-priority papers (most referenced, need DOI):")
    print()
    for p in no_doi[:20]:
        print(f"  {p.key:45} refs={p.reference_count:3}  {p.title[:40]}...")

    if len(no_doi) > 20:
        print(f"  ... and {len(no_doi) - 20} more")

    print()
    print("-" * 80)
    print("Commands:")
    print("  --lookup KEY       Lookup DOI for single paper")
    print("  --batch N          Lookup N papers (dry-run)")
    print("  --priority         Lookup high-priority papers first")
    print("-" * 80)

def lookup_single(papers: Dict[str, PaperInfo], key: str, execute: bool = False):
    """Lookup DOI for a single paper."""
    if key not in papers:
        print(f"❌ Paper not found: {key}")
        return

    paper = papers[key]

    print("=" * 80)
    print(f"DOI LOOKUP: {key}")
    print("=" * 80)
    print()
    print(f"📄 Title: {paper.title[:70]}...")
    print(f"👤 Author: {paper.author[:50]}...")
    print(f"📅 Year: {paper.year}")
    print(f"📍 References: {paper.reference_count}")
    print(f"🔗 Current DOI: {paper.doi or 'MISSING'}")
    print()

    if paper.doi:
        print("✅ Paper already has DOI")
        return

    print("🔍 Searching CrossRef...")
    result = crossref_lookup(paper.title, paper.author, paper.year)

    if result:
        print()
        print(f"📖 Found: {result['title'][:60]}...")
        print(f"🔗 DOI: {result['doi']}")
        print(f"📊 Score: {result.get('score', 'N/A')}")

        if result.get('confidence') == 'low':
            print("⚠️  Low confidence match - verify manually")

        if execute:
            print()
            print("💾 Updating BibTeX...")
            if update_bibtex_doi(key, result['doi']):
                print(f"✅ DOI added: {result['doi']}")
            else:
                print("❌ Failed to update BibTeX")
        else:
            print()
            print(f"Run with --execute to apply: --lookup {key} --execute")
    else:
        print("❌ No DOI found in CrossRef")

def batch_lookup(papers: Dict[str, PaperInfo], count: int, execute: bool = False, priority: bool = False):
    """Batch lookup DOIs for multiple papers."""
    # Filter papers without DOI
    no_doi = [p for p in papers.values() if not p.doi and not p.has_pap_prefix]

    if priority:
        # Sort by reference count (highest first)
        no_doi.sort(key=lambda p: -p.reference_count)

    to_process = no_doi[:count]

    print("=" * 80)
    print(f"BATCH DOI LOOKUP: {len(to_process)} papers")
    print("=" * 80)
    print()

    found = 0
    failed = 0
    low_confidence = 0

    for i, paper in enumerate(to_process):
        print(f"[{i+1}/{len(to_process)}] {paper.key}")
        print(f"  Title: {paper.title[:50]}...")

        result = crossref_lookup(paper.title, paper.author, paper.year)

        if result:
            found += 1
            confidence = "✅" if result.get('confidence') != 'low' else "⚠️"
            if result.get('confidence') == 'low':
                low_confidence += 1

            print(f"  {confidence} DOI: {result['doi']}")

            if execute and result.get('confidence') != 'low':
                if update_bibtex_doi(paper.key, result['doi']):
                    print(f"  💾 Saved")
                else:
                    print(f"  ❌ Save failed")
        else:
            failed += 1
            print(f"  ❌ Not found")

        # Rate limit
        time.sleep(0.5)
        print()

    print("-" * 80)
    print(f"Summary:")
    print(f"  ✅ Found: {found}")
    print(f"  ⚠️ Low confidence: {low_confidence}")
    print(f"  ❌ Not found: {failed}")

    if not execute:
        print()
        print("Run with --execute to apply DOIs")

def main():
    parser = argparse.ArgumentParser(description="DOI Lookup for EBF Papers")
    parser.add_argument('--analyze', action='store_true', help='Analyze papers without DOI')
    parser.add_argument('--lookup', type=str, help='Lookup DOI for single paper')
    parser.add_argument('--batch', type=int, help='Batch lookup N papers')
    parser.add_argument('--priority', action='store_true', help='Process high-priority papers first')
    parser.add_argument('--execute', action='store_true', help='Apply changes')

    args = parser.parse_args()

    papers = parse_bibtex()

    if args.analyze or (not args.lookup and not args.batch):
        analyze_papers(papers)
    elif args.lookup:
        lookup_single(papers, args.lookup, args.execute)
    elif args.batch:
        batch_lookup(papers, args.batch, args.execute, args.priority)

if __name__ == '__main__':
    main()
