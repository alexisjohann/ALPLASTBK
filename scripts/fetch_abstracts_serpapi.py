#!/usr/bin/env python3
"""
Fetch abstracts using SerpApi (Google Scholar)
==============================================

Usage:
    SERPAPI_KEY=your_key python scripts/fetch_abstracts_serpapi.py --limit 100
    SERPAPI_KEY=your_key python scripts/fetch_abstracts_serpapi.py --all

Or provide key as argument:
    python scripts/fetch_abstracts_serpapi.py --key YOUR_KEY --limit 100
"""

import os
import re
import sys
import json
import time
import argparse
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path
from datetime import datetime

# Paths
BASE_PATH = Path(__file__).parent.parent
YAML_DIR = BASE_PATH / "data" / "paper-references"

def get_papers_needing_abstracts():
    """Get list of papers that need abstracts."""
    papers = []

    for yaml_file in sorted(YAML_DIR.glob("PAP-*.yaml")):
        with open(yaml_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Skip if already has real abstract
        if re.search(r'^abstract:\s*"[^"]{50,}', content, re.MULTILINE):
            continue
        if re.search(r"^abstract:\s*'[^']{50,}", content, re.MULTILINE):
            continue

        # Extract fields
        title_match = re.search(r'^title:\s*["\'](.+?)["\']', content, re.MULTILINE)
        author_match = re.search(r'^author:\s*["\'](.+?)["\']', content, re.MULTILINE)
        year_match = re.search(r'^year:\s*["\']?(\d+)', content, re.MULTILINE)
        doi_match = re.search(r'^doi:\s*["\'](.+?)["\']', content, re.MULTILINE)

        if title_match:
            papers.append({
                'file': yaml_file,
                'title': title_match.group(1),
                'author': author_match.group(1) if author_match else "",
                'year': year_match.group(1) if year_match else "",
                'doi': doi_match.group(1) if doi_match else None
            })

    return papers


def fetch_from_serpapi(title, author, api_key):
    """Fetch abstract from Google Scholar via SerpApi."""
    try:
        # Build search query
        first_author = author.split(' and ')[0].split(',')[0].strip() if author else ""
        query = f"{first_author} {title}".strip()[:200]

        params = {
            "engine": "google_scholar",
            "q": query,
            "api_key": api_key,
            "num": 1
        }

        url = "https://serpapi.com/search?" + urllib.parse.urlencode(params)

        req = urllib.request.Request(url, headers={
            "User-Agent": "EBF-Research/1.0"
        })

        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode('utf-8'))

        results = data.get('organic_results', [])
        if results:
            snippet = results[0].get('snippet', '')
            if len(snippet) > 50:
                return snippet

        return None

    except urllib.error.HTTPError as e:
        if e.code == 401:
            print("    ERROR: Invalid API key")
            return None
        raise
    except Exception as e:
        print(f"    Error: {e}")
        return None


def update_yaml_with_abstract(yaml_file, abstract):
    """Update YAML file with abstract."""
    with open(yaml_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Clean abstract
    abstract = abstract.replace('"', "'").replace('\n', ' ').strip()

    # Update or add abstract
    if 'abstract: null' in content:
        content = content.replace('abstract: null', f'abstract: "{abstract}"')
    elif 'abstract:' not in content:
        # Add after doi line
        content = re.sub(
            r'(doi:[^\n]+\n)',
            r'\1abstract: "' + abstract + '"\nabstract_source: serpapi\n',
            content
        )
    else:
        # Replace existing empty abstract
        content = re.sub(
            r'abstract:\s*["\']?\s*["\']?',
            f'abstract: "{abstract}"',
            content
        )

    # Add source if not present
    if 'abstract_source' not in content:
        content = content.replace(
            f'abstract: "{abstract}"',
            f'abstract: "{abstract}"\nabstract_source: serpapi'
        )

    with open(yaml_file, 'w', encoding='utf-8') as f:
        f.write(content)


def main():
    parser = argparse.ArgumentParser(description='Fetch abstracts via SerpApi')
    parser.add_argument('--key', help='SerpApi API key')
    parser.add_argument('--limit', type=int, default=100, help='Max papers to process')
    parser.add_argument('--all', action='store_true', help='Process all papers')
    parser.add_argument('--dry-run', action='store_true', help='Dry run (no changes)')
    args = parser.parse_args()

    # Get API key
    api_key = args.key or os.environ.get('SERPAPI_KEY') or os.environ.get('SERPAPI')
    if not api_key:
        print("ERROR: No API key provided.")
        print("Usage: SERPAPI_KEY=xxx python scripts/fetch_abstracts_serpapi.py")
        print("   or: python scripts/fetch_abstracts_serpapi.py --key YOUR_KEY")
        sys.exit(1)

    print("=" * 60)
    print("SERPAPI ABSTRACT FETCHER")
    print("=" * 60)

    # Get papers
    papers = get_papers_needing_abstracts()
    print(f"Papers needing abstracts: {len(papers)}")

    if not args.all and args.limit:
        papers = papers[:args.limit]

    print(f"Processing: {len(papers)}")
    print("-" * 60)

    # Statistics
    found = 0
    not_found = 0
    errors = 0

    for i, paper in enumerate(papers):
        print(f"\n[{i+1}/{len(papers)}] {paper['author']} ({paper['year']})")
        print(f"  Title: {paper['title'][:60]}...")

        abstract = fetch_from_serpapi(paper['title'], paper['author'], api_key)

        if abstract:
            print(f"  ✓ Found: {len(abstract)} chars")
            if not args.dry_run:
                update_yaml_with_abstract(paper['file'], abstract)
                print(f"  → Saved to {paper['file'].name}")
            found += 1
        else:
            print(f"  ✗ Not found")
            not_found += 1

        # Rate limiting (SerpApi allows 100/month on free tier)
        time.sleep(0.5)

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Processed:  {found + not_found}")
    print(f"Found:      {found}")
    print(f"Not found:  {not_found}")
    print(f"Success:    {found/(found+not_found)*100:.1f}%" if (found+not_found) > 0 else "N/A")

    if args.dry_run:
        print("\n[DRY RUN] No files were modified")


if __name__ == '__main__':
    main()
