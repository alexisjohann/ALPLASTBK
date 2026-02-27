#!/usr/bin/env python3
"""
Fetch abstracts for ALL papers with DOIs in bcm_master.bib
==========================================================

Uses CrossRef API with polite pool (mailto header) for best results.
Falls back to OpenAlex if CrossRef fails.

Usage:
    python fetch_all_abstracts.py --dry-run          # Show what would be fetched
    python fetch_all_abstracts.py --limit 50         # Fetch first 50
    python fetch_all_abstracts.py --all              # Fetch all (slow!)
    python fetch_all_abstracts.py --continue         # Continue from last run
"""

import re
import json
import time
import argparse
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from datetime import datetime

# API Configuration
CROSSREF_API = "https://api.crossref.org/works/"
OPENALEX_API = "https://api.openalex.org/works/doi:"
USER_AGENT = "SWSM-AbstractFetcher/1.0 (mailto:research@fehradvice.com; https://github.com/FehrAdvice)"
RATE_LIMIT_DELAY = 1.0  # seconds between requests (polite crawling)

# Paths
BASE_PATH = Path(__file__).parent.parent
BIB_PATH = BASE_PATH / "bibliography" / "bcm_master.bib"
PROGRESS_PATH = BASE_PATH / "data" / "abstract-fetch-progress.json"
ABSTRACTS_PATH = BASE_PATH / "data" / "fetched-abstracts.json"


def parse_bibtex_entries(bib_path: str) -> List[Dict]:
    """Parse BibTeX file and extract entries with DOIs but no abstracts."""
    entries = []

    with open(bib_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Split into entries
    entry_pattern = r'@(\w+)\{([^,]+),([^@]*?)(?=\n@|\Z)'
    matches = re.findall(entry_pattern, content, re.DOTALL)

    for entry_type, key, fields in matches:
        # Extract DOI
        doi_match = re.search(r'doi\s*=\s*[\{"]([^}"]+)[\}"]', fields, re.IGNORECASE)
        if not doi_match:
            continue

        # Check if abstract already exists
        has_abstract = bool(re.search(r'abstract\s*=\s*[\{"]', fields, re.IGNORECASE))
        if has_abstract:
            continue

        # Extract title for reference
        title_match = re.search(r'title\s*=\s*[\{"]([^}"]+)[\}"]', fields)
        title = title_match.group(1) if title_match else "Unknown"

        # Extract author
        author_match = re.search(r'author\s*=\s*[\{"]([^}"]+)[\}"]', fields)
        author = author_match.group(1) if author_match else "Unknown"

        doi = doi_match.group(1).strip()
        # Clean DOI
        if doi.startswith('http'):
            doi = doi.split('doi.org/')[-1]

        entries.append({
            'key': key.strip(),
            'type': entry_type,
            'doi': doi,
            'title': title[:80],
            'author': author.split(',')[0] if author else "Unknown"
        })

    return entries


def fetch_abstract_crossref(doi: str) -> Optional[str]:
    """Fetch abstract from CrossRef API."""
    url = f"{CROSSREF_API}{doi}"

    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', USER_AGENT)

        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))

            if 'message' in data and 'abstract' in data['message']:
                abstract = data['message']['abstract']
                # Clean HTML tags
                abstract = re.sub(r'<[^>]+>', '', abstract)
                # Clean JATS tags
                abstract = re.sub(r'<jats:[^>]+>', '', abstract)
                abstract = re.sub(r'</jats:[^>]+>', '', abstract)
                return abstract.strip()

    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        elif e.code == 403:
            print(f"    [CrossRef blocked - trying OpenAlex]")
            return None
    except Exception as e:
        pass

    return None


def fetch_abstract_openalex(doi: str) -> Optional[str]:
    """Fetch abstract from OpenAlex API."""
    url = f"{OPENALEX_API}{doi}"

    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', USER_AGENT)

        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))

            # OpenAlex uses 'abstract_inverted_index' - need to reconstruct
            if 'abstract_inverted_index' in data and data['abstract_inverted_index']:
                inv_index = data['abstract_inverted_index']
                # Reconstruct abstract from inverted index
                words = {}
                for word, positions in inv_index.items():
                    for pos in positions:
                        words[pos] = word

                if words:
                    abstract = ' '.join(words[i] for i in sorted(words.keys()))
                    return abstract

    except Exception as e:
        pass

    return None


def fetch_abstract(doi: str) -> Tuple[Optional[str], str]:
    """Try to fetch abstract from multiple sources."""
    # Try CrossRef first
    abstract = fetch_abstract_crossref(doi)
    if abstract:
        return abstract, "CrossRef"

    # Try OpenAlex as fallback
    abstract = fetch_abstract_openalex(doi)
    if abstract:
        return abstract, "OpenAlex"

    return None, "NotFound"


def escape_latex(text: str) -> str:
    """Escape special LaTeX characters."""
    # Order matters - do backslash first
    replacements = [
        ('\\', '\\textbackslash{}'),
        ('&', '\\&'),
        ('%', '\\%'),
        ('$', '\\$'),
        ('#', '\\#'),
        ('_', '\\_'),
        ('{', '\\{'),
        ('}', '\\}'),
        ('~', '\\textasciitilde{}'),
        ('^', '\\textasciicircum{}'),
    ]

    for old, new in replacements:
        text = text.replace(old, new)

    # Undo double escaping
    text = text.replace('\\\\&', '\\&')
    text = text.replace('\\\\%', '\\%')

    return text


def add_abstract_to_bib(bib_content: str, key: str, abstract: str) -> str:
    """Add abstract field to a specific BibTeX entry."""
    # Find the entry
    pattern = rf'(@\w+\{{{re.escape(key)}\s*,.*?)(\n@|\Z)'
    match = re.search(pattern, bib_content, re.DOTALL)

    if not match:
        return bib_content

    entry = match.group(1)

    # Check if already has abstract
    if 'abstract' in entry.lower():
        return bib_content

    # Find last closing brace of entry
    # We need to count braces to find the real end
    brace_count = 0
    entry_end = -1
    for i, c in enumerate(entry):
        if c == '{':
            brace_count += 1
        elif c == '}':
            brace_count -= 1
            if brace_count == 0:
                entry_end = i

    if entry_end > 0:
        # Insert abstract before final }
        abstract_escaped = escape_latex(abstract)
        new_entry = entry[:entry_end] + f',\n  abstract = {{{abstract_escaped}}}\n' + entry[entry_end:]
        bib_content = bib_content.replace(entry, new_entry)

    return bib_content


def load_progress() -> Dict:
    """Load progress from previous run."""
    if PROGRESS_PATH.exists():
        with open(PROGRESS_PATH, 'r') as f:
            return json.load(f)
    return {'completed': [], 'failed': [], 'last_run': None}


def save_progress(progress: Dict):
    """Save progress for continuation."""
    progress['last_run'] = datetime.now().isoformat()
    with open(PROGRESS_PATH, 'w') as f:
        json.dump(progress, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description='Fetch abstracts for all papers with DOIs')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be fetched')
    parser.add_argument('--limit', type=int, default=0, help='Limit number of papers to fetch')
    parser.add_argument('--all', action='store_true', help='Fetch all papers')
    parser.add_argument('--continue', dest='cont', action='store_true', help='Continue from last run')
    parser.add_argument('--delay', type=float, default=RATE_LIMIT_DELAY, help='Delay between requests')

    args = parser.parse_args()

    print("=" * 70)
    print("ABSTRACT FETCHER - bcm_master.bib")
    print("=" * 70)

    # Parse bibliography
    print(f"\nParsing {BIB_PATH}...")
    entries = parse_bibtex_entries(BIB_PATH)
    print(f"Found {len(entries)} papers with DOI but no abstract")

    # Load progress
    progress = load_progress() if args.cont else {'completed': [], 'failed': [], 'last_run': None}

    # Filter already processed
    if args.cont:
        entries = [e for e in entries if e['key'] not in progress['completed']
                   and e['key'] not in progress['failed']]
        print(f"After filtering completed: {len(entries)} remaining")

    # Apply limit
    if args.limit > 0:
        entries = entries[:args.limit]
        print(f"Limited to first {args.limit} entries")
    elif not args.all and not args.dry_run:
        print("\nUse --all to fetch all, --limit N for subset, or --dry-run to preview")
        entries = entries[:10]
        print(f"Defaulting to first 10 entries as demo")

    if args.dry_run:
        print("\n--- DRY RUN ---")
        for i, entry in enumerate(entries[:20], 1):
            print(f"{i:4}. {entry['key'][:30]:<30} DOI: {entry['doi'][:40]}")
        if len(entries) > 20:
            print(f"... and {len(entries) - 20} more")
        return

    # Load bibliography content
    with open(BIB_PATH, 'r', encoding='utf-8', errors='ignore') as f:
        bib_content = f.read()

    # Fetch abstracts
    print(f"\nFetching abstracts (delay: {args.delay}s between requests)...")
    print("-" * 70)

    fetched = 0
    failed = 0

    for i, entry in enumerate(entries, 1):
        print(f"[{i}/{len(entries)}] {entry['author'][:20]:<20} {entry['title'][:40]}...")

        abstract, source = fetch_abstract(entry['doi'])

        if abstract:
            # Add to bibliography
            bib_content = add_abstract_to_bib(bib_content, entry['key'], abstract)
            progress['completed'].append(entry['key'])
            fetched += 1
            print(f"    ✓ {source}: {len(abstract.split())} words")
        else:
            progress['failed'].append(entry['key'])
            failed += 1
            print(f"    ✗ No abstract found")

        # Rate limiting
        if i < len(entries):
            time.sleep(args.delay)

        # Save progress every 10 entries
        if i % 10 == 0:
            save_progress(progress)
            # Also save bibliography incrementally
            with open(BIB_PATH, 'w', encoding='utf-8') as f:
                f.write(bib_content)
            print(f"    [Progress saved: {fetched} fetched, {failed} failed]")

    # Final save
    save_progress(progress)
    with open(BIB_PATH, 'w', encoding='utf-8') as f:
        f.write(bib_content)

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Fetched:  {fetched}")
    print(f"Failed:   {failed}")
    print(f"Total:    {fetched + failed}")
    print(f"Success:  {fetched/(fetched+failed)*100:.1f}%" if fetched+failed > 0 else "N/A")
    print(f"\nProgress saved to: {PROGRESS_PATH}")
    print(f"Bibliography updated: {BIB_PATH}")


if __name__ == '__main__':
    main()
