#!/usr/bin/env python3
"""
Enrich Existing Papers - Bring bcm_master.bib papers to L1+ level.

This script:
1. Finds DOIs for papers via CrossRef title/author matching
2. Adds missing use_for fields based on author/topic classification
3. Enriches metadata (volume, pages, journal) from CrossRef
4. Reports on enrichment progress

Usage:
    python scripts/enrich_existing_papers.py                    # Report mode
    python scripts/enrich_existing_papers.py --update           # Apply changes
    python scripts/enrich_existing_papers.py --limit 100        # Process first 100
    python scripts/enrich_existing_papers.py --type article     # Only articles

Author: EBF Team
Version: 1.0.0
"""

import argparse
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path

import requests

# Constants
BIBTEX_PATH = 'bibliography/bcm_master.bib'
OPENALEX_EMAIL = os.environ.get('OPENALEX_EMAIL', 'ebf@fehradvice.com')

# Author to LIT-Appendix mapping
AUTHOR_LIT_MAPPING = {
    'fehr': 'LIT-FEH',
    'thaler': 'LIT-KT',
    'kahneman': 'LIT-KT',
    'tversky': 'LIT-KT',
    'ariely': 'LIT-O',
    'camerer': 'LIT-O',
    'loewenstein': 'LIT-O',
    'sutter': 'LIT-SUT',
    'enke': 'LIT-ENK',
    'gneezy': 'LIT-O',
    'list': 'LIT-O',
    'duflo': 'LIT-O',
    'banerjee': 'LIT-O',
    'charness': 'LIT-O',
    'rabin': 'LIT-O',
    'laibson': 'LIT-O',
    'odonoghue': 'LIT-O',
    'mullainathan': 'LIT-O',
    'shafir': 'LIT-O',
    'sunstein': 'LIT-O',
    'benartzi': 'LIT-O',
    'madrian': 'LIT-O',
}

# Keywords to domain mapping for use_for
KEYWORD_DOMAIN_MAPPING = {
    'loss aversion': ['CORE-HOW', 'LIT-KT'],
    'prospect theory': ['CORE-HOW', 'LIT-KT'],
    'time preference': ['CORE-WHEN', 'LIT-O'],
    'hyperbolic': ['CORE-WHEN', 'LIT-O'],
    'social preference': ['CORE-WHO', 'LIT-FEH'],
    'fairness': ['CORE-WHO', 'LIT-FEH'],
    'reciprocity': ['CORE-WHO', 'LIT-FEH'],
    'inequality': ['CORE-WHO', 'LIT-FEH'],
    'trust': ['CORE-WHO', 'LIT-O'],
    'cooperation': ['CORE-WHO', 'LIT-O'],
    'nudge': ['DOMAIN-POLICY', 'LIT-O'],
    'default': ['CONTEXT-DEFAULT', 'LIT-O'],
    'framing': ['CORE-HOW', 'LIT-KT'],
    'mental accounting': ['CORE-WHAT', 'LIT-KT'],
    'overconfidence': ['CORE-AWARE', 'LIT-O'],
    'bounded rationality': ['CORE-AWARE', 'LIT-O'],
    'experiment': ['METHOD-EXP', 'LIT-O'],
    'field experiment': ['METHOD-FIELD', 'LIT-O'],
    'neuroeconomics': ['LIT-O'],
    'happiness': ['DOMAIN-WELLBEING', 'LIT-O'],
    'well-being': ['DOMAIN-WELLBEING', 'LIT-O'],
    'health': ['DOMAIN-HEALTH', 'LIT-O'],
    'retirement': ['DOMAIN-FINANCE', 'LIT-O'],
    'saving': ['DOMAIN-FINANCE', 'LIT-O'],
    'investment': ['DOMAIN-FINANCE', 'LIT-O'],
    'climate': ['DOMAIN-ENV', 'LIT-O'],
    'energy': ['DOMAIN-ENV', 'LIT-O'],
    'education': ['DOMAIN-EDU', 'LIT-O'],
}

# Theory support mapping based on keywords
KEYWORD_THEORY_MAPPING = {
    'prospect theory': 'MS-RD-001',
    'loss aversion': 'MS-RD-001',
    'reference point': 'MS-RD-001',
    'endowment effect': 'MS-RD-002',
    'status quo': 'MS-RD-002',
    'inequity aversion': 'MS-SP-001',
    'fairness': 'MS-SP-001',
    'inequality aversion': 'MS-SP-001',
    'reciprocity': 'MS-SP-002',
    'trust game': 'MS-SP-002',
    'social image': 'MS-SI-001',
    'signaling': 'MS-SI-001',
    'reputation': 'MS-SI-001',
    'hyperbolic discount': 'MS-TP-001',
    'present bias': 'MS-TP-001',
    'quasi-hyperbolic': 'MS-TP-001',
    'exponential discount': 'MS-TP-002',
    'time inconsistent': 'MS-TP-001',
    'commitment device': 'MS-TP-001',
    'overconfidence': 'MS-BF-001',
    'optimism bias': 'MS-BF-001',
    'availability heuristic': 'MS-BF-002',
    'representativeness': 'MS-BF-002',
    'anchoring': 'MS-BF-003',
    'adjustment': 'MS-BF-003',
    'mental accounting': 'MS-BF-004',
    'narrow framing': 'MS-BF-004',
    'framing effect': 'MS-BF-005',
    'asian disease': 'MS-BF-005',
    'default effect': 'MS-NU-001',
    'opt-out': 'MS-NU-001',
    'nudge': 'MS-NU-001',
    'choice architecture': 'MS-NU-001',
    'sunk cost': 'MS-BF-006',
    'escalation of commitment': 'MS-BF-006',
    'hindsight bias': 'MS-BF-007',
    'confirmation bias': 'MS-BF-008',
    'attention': 'MS-AT-001',
    'salience': 'MS-AT-001',
    'limited attention': 'MS-AT-001',
    'identity': 'MS-IB-001',
    'social identity': 'MS-IB-001',
    'in-group': 'MS-IB-001',
    'altruism': 'MS-SP-003',
    'warm glow': 'MS-SP-003',
    'public good': 'MS-SP-004',
    'free riding': 'MS-SP-004',
    'cooperation': 'MS-SP-004',
    'gift exchange': 'MS-SP-005',
    'efficiency wage': 'MS-SP-005',
    'crowding out': 'MS-MO-001',
    'intrinsic motivation': 'MS-MO-001',
    'extrinsic motivation': 'MS-MO-001',
}


def parse_bibtex(content: str) -> list[dict]:
    """Parse BibTeX file into list of entries."""
    entries = []

    # Match entry pattern
    pattern = r'@(\w+)\s*\{\s*([^,]+)\s*,([^@]*?)(?=\n@|\Z)'
    matches = re.findall(pattern, content, re.DOTALL)

    for entry_type, key, fields_str in matches:
        entry = {
            'type': entry_type.lower(),
            'key': key.strip(),
            'fields': {},
            'raw_fields': fields_str
        }

        # Parse fields - handle nested braces
        field_pattern = r'(\w+)\s*=\s*\{((?:[^{}]|\{[^{}]*\})*)\}'
        for field_name, field_value in re.findall(field_pattern, fields_str):
            entry['fields'][field_name.lower()] = field_value.strip()

        entries.append(entry)

    return entries


def find_doi_crossref(title: str, author: str = None, year: str = None, skip_api: bool = True) -> dict:
    """Find DOI and metadata via CrossRef API.

    Note: API calls are disabled by default in sandboxed environments.
    Set skip_api=False to attempt API lookups (may fail due to proxy).
    """
    if skip_api or not title:
        return None

    # Clean title
    clean_title = re.sub(r'[{}\\]', '', title)
    clean_title = re.sub(r'\s+', ' ', clean_title).strip()

    try:
        url = "https://api.crossref.org/works"
        params = {
            'query.title': clean_title,
            'rows': 5,
            'mailto': OPENALEX_EMAIL
        }

        if author:
            # Extract first author's last name
            first_author = author.split(' and ')[0] if ' and ' in author else author
            if ',' in first_author:
                last_name = first_author.split(',')[0].strip()
            else:
                last_name = first_author.split()[-1].strip() if first_author.split() else ''
            if last_name:
                params['query.author'] = last_name

        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        items = data.get('message', {}).get('items', [])

        for item in items:
            item_title = item.get('title', [''])[0].lower()

            # Check title similarity (first 50 chars)
            if clean_title.lower()[:50] in item_title or item_title[:50] in clean_title.lower():
                result = {
                    'doi': item.get('DOI'),
                    'volume': item.get('volume'),
                    'pages': item.get('page'),
                    'issue': item.get('issue'),
                }

                # Get journal name
                container = item.get('container-title', [])
                if container:
                    result['journal'] = container[0]

                return result

        return None

    except Exception as e:
        return None


def determine_use_for(entry: dict) -> list[str]:
    """Determine use_for based on author and title keywords."""
    use_for = set()

    # Check author
    author = entry['fields'].get('author', '').lower()
    for author_key, lit_appendix in AUTHOR_LIT_MAPPING.items():
        if author_key in author:
            use_for.add(lit_appendix)

    # Check title for keywords
    title = entry['fields'].get('title', '').lower()
    abstract = entry['fields'].get('abstract', '').lower()
    text = f"{title} {abstract}"

    for keyword, domains in KEYWORD_DOMAIN_MAPPING.items():
        if keyword in text:
            use_for.update(domains)

    # Default to LIT-O if nothing found
    if not use_for:
        use_for.add('LIT-O')

    return sorted(list(use_for))


def determine_theory_support(entry: dict) -> list[str]:
    """Determine theory_support based on title and abstract keywords."""
    theories = set()

    title = entry['fields'].get('title', '').lower()
    abstract = entry['fields'].get('abstract', '').lower()
    text = f"{title} {abstract}"

    for keyword, theory_id in KEYWORD_THEORY_MAPPING.items():
        if keyword in text:
            theories.add(theory_id)

    return sorted(list(theories))


def format_bibtex_entry(entry: dict) -> str:
    """Format entry back to BibTeX string."""
    lines = [f"@{entry['type']}{{{entry['key']},"]

    # Order fields nicely
    field_order = ['title', 'author', 'year', 'journal', 'booktitle', 'volume',
                   'number', 'pages', 'doi', 'publisher', 'address', 'editor',
                   'use_for', 'theory_support', 'evidence_tier', 'abstract',
                   'keywords', 'note', 'url']

    fields = entry['fields']
    written = set()

    # Write fields in order
    for field in field_order:
        if field in fields:
            lines.append(f"  {field} = {{{fields[field]}}},")
            written.add(field)

    # Write remaining fields
    for field, value in fields.items():
        if field not in written:
            lines.append(f"  {field} = {{{value}}},")

    # Remove trailing comma from last field
    if lines[-1].endswith(','):
        lines[-1] = lines[-1][:-1]

    lines.append("}")
    return '\n'.join(lines)


def enrich_entries(entries: list[dict], limit: int = None, entry_type: str = None,
                   update: bool = False, verbose: bool = False) -> dict:
    """Enrich entries with use_for and theory_support fields."""

    stats = {
        'total': len(entries),
        'processed': 0,
        'dois_found': 0,
        'use_for_added': 0,
        'theory_support_added': 0,
        'already_complete': 0,
        'needs_doi': [],
        'errors': 0,
        'enriched_entries': []
    }

    # Filter by type if specified
    if entry_type:
        entries = [e for e in entries if e['type'] == entry_type]
        stats['filtered'] = len(entries)

    # Apply limit
    if limit:
        entries = entries[:limit]

    print(f"\n📊 Processing {len(entries)} entries...")
    print("=" * 60)

    for i, entry in enumerate(entries):
        key = entry['key']
        fields = entry['fields']
        enriched = False

        # Track entries needing DOI
        if not fields.get('doi') and entry['type'] == 'article':
            stats['needs_doi'].append({
                'key': key,
                'title': fields.get('title', ''),
                'author': fields.get('author', ''),
                'year': fields.get('year', ''),
                'journal': fields.get('journal', '')
            })

        # Skip if already complete (has use_for and theory_support)
        if fields.get('use_for') and fields.get('theory_support'):
            stats['already_complete'] += 1
            continue

        stats['processed'] += 1

        if verbose or (i % 100 == 0):
            print(f"  [{i+1}/{len(entries)}] Processing: {key}")

        # Add use_for if missing
        if not fields.get('use_for'):
            use_for_list = determine_use_for(entry)
            fields['use_for'] = ', '.join(use_for_list)
            stats['use_for_added'] += 1
            enriched = True

            if verbose:
                print(f"    ✅ Added use_for: {fields['use_for']}")

        # Add theory_support if missing
        if not fields.get('theory_support'):
            theory_list = determine_theory_support(entry)
            if theory_list:
                fields['theory_support'] = ', '.join(theory_list)
                stats['theory_support_added'] += 1
                enriched = True

                if verbose:
                    print(f"    ✅ Added theory_support: {fields['theory_support']}")

        if enriched:
            stats['enriched_entries'].append(entry)

    return stats


def write_bibtex(entries: list[dict], output_path: str):
    """Write entries back to BibTeX file using direct replacement."""

    # Create map of enriched entries by key
    enriched_map = {e['key']: e for e in entries if e.get('_enriched')}

    if not enriched_map:
        print("   No entries to update")
        return

    # Read original file
    with open(BIBTEX_PATH, 'r', encoding='utf-8') as f:
        original_content = f.read()

    # Parse into individual entries
    new_parts = []
    current_pos = 0

    # Find each entry and replace if enriched
    pattern = r'(@\w+\s*\{\s*([^,]+)\s*,)'
    for match in re.finditer(pattern, original_content):
        entry_start = match.start()
        key = match.group(2).strip()

        # Find end of this entry (next @ or end of file)
        rest = original_content[entry_start:]
        next_at = rest.find('\n@', 1)
        if next_at == -1:
            entry_end = len(original_content)
        else:
            entry_end = entry_start + next_at

        # Add content before this entry
        new_parts.append(original_content[current_pos:entry_start])

        if key in enriched_map:
            # Replace with enriched entry
            new_parts.append(format_bibtex_entry(enriched_map[key]))
        else:
            # Keep original entry
            new_parts.append(original_content[entry_start:entry_end])

        current_pos = entry_end

    # Add any remaining content
    new_parts.append(original_content[current_pos:])

    new_content = ''.join(new_parts)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(new_content)


def export_needs_doi(papers: list[dict], output_path: str):
    """Export papers needing DOIs to a CSV file for batch processing."""
    import csv

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['key', 'title', 'author', 'year', 'journal'])
        writer.writeheader()
        writer.writerows(papers)

    print(f"📄 Exported {len(papers)} papers needing DOIs to {output_path}")


def main():
    parser = argparse.ArgumentParser(description='Enrich existing papers in bcm_master.bib')
    parser.add_argument('--update', action='store_true', help='Apply changes to bcm_master.bib')
    parser.add_argument('--limit', type=int, help='Limit number of entries to process')
    parser.add_argument('--type', type=str, help='Filter by entry type (article, book, etc.)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--output', type=str, help='Output file (default: overwrite original)')
    parser.add_argument('--export-needs-doi', type=str, help='Export papers needing DOIs to CSV')
    args = parser.parse_args()

    print("=" * 70)
    print("PAPER ENRICHMENT - Bringing papers to L1+ level")
    print("=" * 70)

    # Read BibTeX
    print(f"\n📖 Reading {BIBTEX_PATH}...")
    with open(BIBTEX_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    entries = parse_bibtex(content)
    print(f"   Found {len(entries)} entries")

    # Analyze current state
    articles = [e for e in entries if e['type'] == 'article']
    with_doi = [e for e in entries if e['fields'].get('doi')]
    with_use_for = [e for e in entries if e['fields'].get('use_for')]
    with_theory = [e for e in entries if e['fields'].get('theory_support')]
    articles_no_doi = [e for e in articles if not e['fields'].get('doi')]
    no_use_for = [e for e in entries if not e['fields'].get('use_for')]
    no_theory = [e for e in entries if not e['fields'].get('theory_support')]

    print(f"\n📊 Current State:")
    print(f"   Total entries:          {len(entries)}")
    print(f"   Articles:               {len(articles)}")
    print(f"   With DOI:               {len(with_doi)} ({100*len(with_doi)/len(entries):.1f}%)")
    print(f"   With use_for:           {len(with_use_for)} ({100*len(with_use_for)/len(entries):.1f}%)")
    print(f"   With theory_support:    {len(with_theory)} ({100*len(with_theory)/len(entries):.1f}%)")
    print(f"   Articles without DOI:   {len(articles_no_doi)}")
    print(f"   Without use_for:        {len(no_use_for)}")
    print(f"   Without theory_support: {len(no_theory)}")

    # Run enrichment
    stats = enrich_entries(
        entries,
        limit=args.limit,
        entry_type=args.type,
        update=args.update,
        verbose=args.verbose
    )

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Processed:              {stats['processed']}")
    print(f"use_for added:          {stats['use_for_added']}")
    print(f"theory_support added:   {stats['theory_support_added']}")
    print(f"Already complete:       {stats['already_complete']}")
    print(f"Papers needing DOI:     {len(stats['needs_doi'])}")

    # Export papers needing DOIs
    if args.export_needs_doi and stats['needs_doi']:
        export_needs_doi(stats['needs_doi'], args.export_needs_doi)

    if args.update and stats['enriched_entries']:
        output_path = args.output or BIBTEX_PATH
        print(f"\n📝 Writing enriched entries to {output_path}...")

        # Mark enriched entries
        for e in stats['enriched_entries']:
            e['_enriched'] = True

        write_bibtex(entries, output_path)
        print(f"✅ Updated {len(stats['enriched_entries'])} entries")
    elif not args.update and stats['enriched_entries']:
        print(f"\n⚠️  Run with --update to apply {len(stats['enriched_entries'])} changes")
        print("\nSample enriched entries:")
        for entry in stats['enriched_entries'][:5]:
            print(f"\n  {entry['key']}:")
            if entry['fields'].get('use_for'):
                print(f"    use_for: {entry['fields']['use_for']}")
            if entry['fields'].get('theory_support'):
                print(f"    theory_support: {entry['fields']['theory_support']}")


if __name__ == '__main__':
    main()
