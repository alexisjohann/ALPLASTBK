#!/usr/bin/env python3
"""
Match Papers to Appendices via OpenAlex API.

This script:
1. Reads researcher profiles from researcher-registry.yaml
2. Uses OpenAlex API to find all papers by author (via ORCID or name)
3. Matches papers in bcm_master.bib to researchers
4. Updates use_for field with correct LIT-appendix

Usage:
    python scripts/match_papers_to_appendices.py --dry-run
    python scripts/match_papers_to_appendices.py --update
    python scripts/match_papers_to_appendices.py --researcher RES-FEHR-E

APIs Used:
    - OpenAlex (free, no key required): https://api.openalex.org

Author: EBF Team
Version: 1.0.0
"""

import argparse
import json
import re
import time
from pathlib import Path

import requests
import yaml

# Paths
REGISTRY_PATH = Path('data/researcher-registry.yaml')
BIBTEX_PATH = Path('bibliography/bcm_master.bib')

# OpenAlex API (free, polite pool with email)
OPENALEX_BASE = 'https://api.openalex.org'
OPENALEX_EMAIL = 'research@fehradvice.com'

# Researcher ID to LIT-Appendix mapping
RESEARCHER_LIT_MAP = {
    'RES-FEHR-E': 'LIT-FEH',
    'RES-SUTTER-M': 'LIT-SUT',
    'RES-ENKE-B': 'LIT-ENK',
    'RES-THALER-R': 'LIT-KT',
    'RES-KAHNEMAN-D': 'LIT-KT',
}


def load_registry() -> dict:
    """Load researcher registry."""
    with open(REGISTRY_PATH, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def load_bibtex_entries() -> list[dict]:
    """Parse BibTeX file into list of entries."""
    with open(BIBTEX_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    entries = []
    # Match each entry
    pattern = r'@(\w+)\s*\{\s*([^,]+)\s*,'
    current_pos = 0

    for match in re.finditer(pattern, content):
        entry_start = match.start()

        # Find end of entry
        rest = content[entry_start:]
        brace_count = 0
        entry_end = entry_start

        for i, char in enumerate(rest):
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    entry_end = entry_start + i + 1
                    break

        entry_text = content[entry_start:entry_end]

        # Extract fields
        entry = {
            'type': match.group(1).lower(),
            'key': match.group(2).strip(),
            'text': entry_text,
            'fields': {}
        }

        # Parse fields
        field_pattern = r'\s*(\w+)\s*=\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}'
        for field_match in re.finditer(field_pattern, entry_text):
            field_name = field_match.group(1).lower()
            field_value = field_match.group(2)
            entry['fields'][field_name] = field_value

        entries.append(entry)

    return entries


def fetch_openalex_author(orcid: str = None, name: str = None) -> dict:
    """Fetch author from OpenAlex by ORCID or name."""
    if orcid:
        url = f"{OPENALEX_BASE}/authors/https://orcid.org/{orcid}"
    elif name:
        url = f"{OPENALEX_BASE}/authors"
        params = {'search': name, 'mailto': OPENALEX_EMAIL}
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        if data.get('results'):
            return data['results'][0]
        return None
    else:
        return None

    params = {'mailto': OPENALEX_EMAIL}
    response = requests.get(url, params=params, timeout=30)

    if response.status_code == 404:
        return None

    response.raise_for_status()
    return response.json()


def fetch_author_works(author_id: str, max_works: int = 500) -> list[dict]:
    """Fetch all works by an author from OpenAlex."""
    works = []
    page = 1
    per_page = 100

    while len(works) < max_works:
        url = f"{OPENALEX_BASE}/works"
        params = {
            'filter': f'author.id:{author_id}',
            'per-page': per_page,
            'page': page,
            'mailto': OPENALEX_EMAIL
        }

        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        results = data.get('results', [])
        if not results:
            break

        works.extend(results)
        page += 1
        time.sleep(0.2)  # Rate limiting

        if len(results) < per_page:
            break

    return works[:max_works]


def normalize_title(title: str) -> str:
    """Normalize title for matching."""
    if not title:
        return ''
    # Remove LaTeX commands, braces, punctuation
    title = re.sub(r'\\[a-zA-Z]+\{[^}]*\}', '', title)
    title = re.sub(r'[{}\\]', '', title)
    title = re.sub(r'[^\w\s]', '', title.lower())
    title = ' '.join(title.split())
    return title[:50]  # First 50 chars for matching


def match_works_to_bibtex(works: list[dict], entries: list[dict]) -> list[tuple]:
    """Match OpenAlex works to BibTeX entries."""
    matches = []

    # Create lookup map for BibTeX entries
    bibtex_titles = {}
    bibtex_dois = {}

    for entry in entries:
        # By title
        title = entry['fields'].get('title', '')
        norm_title = normalize_title(title)
        if norm_title:
            bibtex_titles[norm_title] = entry

        # By DOI
        doi = entry['fields'].get('doi', '').lower().strip()
        if doi:
            # Normalize DOI
            doi = doi.replace('https://doi.org/', '').replace('http://doi.org/', '')
            bibtex_dois[doi] = entry

    # Match each work
    for work in works:
        matched_entry = None

        # Try DOI match first
        work_doi = work.get('doi', '')
        if work_doi:
            work_doi = work_doi.replace('https://doi.org/', '').lower()
            if work_doi in bibtex_dois:
                matched_entry = bibtex_dois[work_doi]

        # Try title match
        if not matched_entry:
            work_title = work.get('title', '')
            norm_work_title = normalize_title(work_title)
            if norm_work_title and norm_work_title in bibtex_titles:
                matched_entry = bibtex_titles[norm_work_title]

        if matched_entry:
            matches.append((work, matched_entry))

    return matches


def update_use_for(entry: dict, lit_appendix: str) -> bool:
    """Update use_for field to include LIT-appendix."""
    current_use_for = entry['fields'].get('use_for', '')

    # Parse current use_for
    if current_use_for:
        current_values = [v.strip() for v in current_use_for.split(',')]
    else:
        current_values = []

    # Check if already has this LIT
    if lit_appendix in current_values:
        return False

    # Add LIT-appendix
    current_values.append(lit_appendix)
    entry['fields']['use_for'] = ', '.join(sorted(set(current_values)))
    return True


def update_bibtex_file(entries: list[dict], updated_keys: set):
    """Update BibTeX file with modified entries."""
    with open(BIBTEX_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    current_entry = None
    in_entry = False
    entry_lines = []

    for line in lines:
        # Detect entry start
        entry_match = re.match(r'@(\w+)\s*\{\s*([^,]+)\s*,', line)
        if entry_match:
            # Process previous entry if exists
            if in_entry and entry_lines:
                new_lines.extend(entry_lines)

            in_entry = True
            entry_lines = [line]
            current_entry = entry_match.group(2).strip()
            continue

        if in_entry:
            entry_lines.append(line)

            # Detect entry end
            if line.strip() == '}':
                # Check if this entry needs updating
                if current_entry in updated_keys:
                    # Find the entry data
                    entry_data = next((e for e in entries if e['key'] == current_entry), None)
                    if entry_data:
                        # Check if use_for line exists
                        has_use_for = any('use_for' in l for l in entry_lines)
                        new_use_for = entry_data['fields'].get('use_for', '')

                        if not has_use_for and new_use_for:
                            # Insert use_for before closing brace
                            entry_lines = entry_lines[:-1]
                            # Ensure comma on previous line
                            if entry_lines and not entry_lines[-1].rstrip().endswith(','):
                                last = entry_lines[-1].rstrip()
                                if last and last != '{':
                                    entry_lines[-1] = last + ',\n'
                            entry_lines.append(f'  use_for = {{{new_use_for}}},\n')
                            entry_lines.append('}\n')
                        elif has_use_for and new_use_for:
                            # Update existing use_for
                            for i, l in enumerate(entry_lines):
                                if 'use_for' in l:
                                    entry_lines[i] = f'  use_for = {{{new_use_for}}},\n'
                                    break

                new_lines.extend(entry_lines)
                in_entry = False
                entry_lines = []
        else:
            new_lines.append(line)

    # Handle last entry
    if in_entry and entry_lines:
        new_lines.extend(entry_lines)

    with open(BIBTEX_PATH, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)


def process_researcher(researcher: dict, entries: list[dict], dry_run: bool = True) -> dict:
    """Process one researcher and match their papers."""
    rid = researcher.get('id') or researcher.get('superkey')
    name = researcher.get('basic_info', {}).get('full_name', 'Unknown')
    orcid = researcher.get('metrics', {}).get('orcid')
    lit_appendix = RESEARCHER_LIT_MAP.get(rid, 'LIT-O')

    print(f"\n{'='*60}")
    print(f"Processing: {name} ({rid})")
    print(f"  ORCID: {orcid}")
    print(f"  LIT-Appendix: {lit_appendix}")
    print('='*60)

    stats = {
        'researcher': rid,
        'name': name,
        'works_found': 0,
        'matches': 0,
        'updated': 0,
        'already_linked': 0
    }

    # Fetch author from OpenAlex
    print(f"  Fetching author from OpenAlex...")
    author = fetch_openalex_author(orcid=orcid, name=name)

    if not author:
        print(f"  ⚠️ Author not found in OpenAlex")
        return stats

    author_id = author.get('id', '').replace('https://openalex.org/', '')
    print(f"  OpenAlex ID: {author_id}")
    print(f"  Works count: {author.get('works_count', 0)}")

    # Fetch works
    print(f"  Fetching works...")
    works = fetch_author_works(author_id)
    stats['works_found'] = len(works)
    print(f"  Found {len(works)} works")

    # Match to BibTeX
    print(f"  Matching to BibTeX entries...")
    matches = match_works_to_bibtex(works, entries)
    stats['matches'] = len(matches)
    print(f"  Matched {len(matches)} papers")

    # Update use_for
    updated_entries = []
    for work, entry in matches:
        if update_use_for(entry, lit_appendix):
            updated_entries.append(entry)
            stats['updated'] += 1
            if not dry_run:
                print(f"    ✅ {entry['key']} → +{lit_appendix}")
        else:
            stats['already_linked'] += 1

    print(f"\n  Summary:")
    print(f"    Works in OpenAlex:  {stats['works_found']}")
    print(f"    Matched in BibTeX:  {stats['matches']}")
    print(f"    Newly linked:       {stats['updated']}")
    print(f"    Already linked:     {stats['already_linked']}")

    return stats


def main():
    parser = argparse.ArgumentParser(description='Match papers to appendices via OpenAlex')
    parser.add_argument('--dry-run', action='store_true', help='Preview without changes')
    parser.add_argument('--update', action='store_true', help='Apply changes to bcm_master.bib')
    parser.add_argument('--researcher', type=str, help='Process specific researcher ID')
    args = parser.parse_args()

    print("=" * 70)
    print("PAPER-APPENDIX MATCHING via OpenAlex API")
    print("=" * 70)

    # Load data
    registry = load_registry()
    entries = load_bibtex_entries()
    print(f"\n📖 Loaded {len(entries)} BibTeX entries")

    # Get researchers
    researchers = registry.get('researchers', [])
    if args.researcher:
        researchers = [r for r in researchers if
                      r.get('id') == args.researcher or
                      r.get('superkey') == args.researcher]
        if not researchers:
            print(f"❌ Researcher {args.researcher} not found")
            return

    print(f"📚 Processing {len(researchers)} researcher(s)")

    # Process each researcher
    all_stats = []
    updated_keys = set()

    for researcher in researchers:
        try:
            stats = process_researcher(researcher, entries, dry_run=not args.update)
            all_stats.append(stats)

            # Collect updated keys
            if args.update:
                for entry in entries:
                    if entry['fields'].get('_updated'):
                        updated_keys.add(entry['key'])

        except Exception as e:
            print(f"  ❌ Error: {e}")
            continue

        time.sleep(1)  # Rate limiting between researchers

    # Summary
    print("\n" + "=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)

    total_matches = sum(s['matches'] for s in all_stats)
    total_updated = sum(s['updated'] for s in all_stats)
    total_already = sum(s['already_linked'] for s in all_stats)

    print(f"Researchers processed: {len(all_stats)}")
    print(f"Total matches found:   {total_matches}")
    print(f"Newly linked:          {total_updated}")
    print(f"Already linked:        {total_already}")

    if args.update and total_updated > 0:
        print(f"\n📝 Updating {BIBTEX_PATH}...")
        update_bibtex_file(entries, updated_keys)
        print(f"✅ Updated {total_updated} entries")
    elif not args.update and total_updated > 0:
        print(f"\n⚠️ Run with --update to apply {total_updated} changes")


if __name__ == '__main__':
    main()
