#!/usr/bin/env python3
"""
BibTeX Enrichment - Enhance bcm_master.bib with CrossRef data.

Features:
- Add missing DOIs by title search
- Update citation counts
- Validate existing DOIs
- Fill missing metadata (volume, pages, etc.)
- Generate report of changes

Usage:
    python scripts/enrich_bibtex.py                      # Report only
    python scripts/enrich_bibtex.py --update             # Apply updates
    python scripts/enrich_bibtex.py --validate           # Validate DOIs only
    python scripts/enrich_bibtex.py --citations          # Update citation counts
    python scripts/enrich_bibtex.py --entry "fehr1999"   # Single entry

Author: EBF Team
Version: 1.0.0
"""

import argparse
import os
import re
import sys
import time
from datetime import datetime

# Add scripts to path for crossref_api import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from crossref_api import CrossRefClient, extract_metadata

BIBTEX_PATH = 'bibliography/bcm_master.bib'
BACKUP_PATH = 'bibliography/bcm_master.bib.backup'


def parse_bibtex(filepath: str) -> dict:
    """Parse BibTeX file into dictionary of entries."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    entries = {}
    # Match BibTeX entries
    pattern = r'@(\w+)\s*\{\s*([^,]+)\s*,([^@]*?)(?=\n@|\Z)'
    matches = re.findall(pattern, content, re.DOTALL)

    for entry_type, key, fields_str in matches:
        key = key.strip()
        fields = {}

        # Parse fields
        field_pattern = r'(\w+)\s*=\s*[{"](.+?)[}"](?=\s*,?\s*(?:\w+\s*=|\}))'
        field_matches = re.findall(field_pattern, fields_str, re.DOTALL)

        for field_name, field_value in field_matches:
            fields[field_name.lower()] = field_value.strip()

        entries[key] = {
            'type': entry_type.lower(),
            'key': key,
            'fields': fields,
            'raw': f"@{entry_type}{{{key},{fields_str}}}"
        }

    return entries


def get_entry_info(entry: dict) -> dict:
    """Extract key info from a BibTeX entry."""
    fields = entry.get('fields', {})
    return {
        'key': entry.get('key'),
        'title': fields.get('title', ''),
        'author': fields.get('author', ''),
        'year': fields.get('year', ''),
        'doi': fields.get('doi', ''),
        'journal': fields.get('journal', ''),
        'volume': fields.get('volume'),
        'pages': fields.get('pages'),
        'citations': fields.get('citations'),
    }


def find_doi_by_title(client: CrossRefClient, title: str, author: str = None) -> str:
    """Try to find DOI for a paper by title."""
    if not title:
        return None

    # Clean title
    clean_title = re.sub(r'[{}\\]', '', title)

    works = client.search_by_title(clean_title, rows=3)

    if not works:
        return None

    # Check first result
    for work in works:
        metadata = extract_metadata(work)
        if not metadata:
            continue

        # Compare titles (fuzzy)
        result_title = metadata.get('title', '').lower()
        search_title = clean_title.lower()

        # Simple similarity check
        if search_title[:50] in result_title or result_title[:50] in search_title:
            return metadata.get('doi')

    return None


def validate_entries(entries: dict, client: CrossRefClient) -> dict:
    """Validate DOIs in entries."""
    results = {
        'valid': [],
        'invalid': [],
        'missing': [],
    }

    for key, entry in entries.items():
        info = get_entry_info(entry)

        if info['doi']:
            if client.validate_doi(info['doi']):
                results['valid'].append(key)
            else:
                results['invalid'].append(key)
        else:
            results['missing'].append(key)

        # Rate limiting
        time.sleep(0.1)

    return results


def enrich_entry(entry: dict, client: CrossRefClient) -> dict:
    """Enrich a single entry with CrossRef data."""
    info = get_entry_info(entry)
    updates = {}

    # If no DOI, try to find one
    if not info['doi']:
        found_doi = find_doi_by_title(client, info['title'], info['author'])
        if found_doi:
            updates['doi'] = found_doi
            info['doi'] = found_doi

    # If we have a DOI, get full metadata
    if info['doi']:
        work = client.get_work(info['doi'])
        if isinstance(work, dict) and 'DOI' in work:
            metadata = extract_metadata(work)

            # Update missing fields
            if not info['volume'] and metadata.get('volume'):
                updates['volume'] = metadata['volume']

            if not info['pages'] and metadata.get('pages'):
                updates['pages'] = metadata['pages']

            # Always update citation count
            if metadata.get('citations'):
                updates['citations'] = str(metadata['citations'])

    return updates


def update_bibtex_entry(raw: str, updates: dict) -> str:
    """Apply updates to a raw BibTeX entry."""
    for field, value in updates.items():
        # Check if field exists
        pattern = rf'({field}\s*=\s*[{{"])[^}}"]+(["}}])'
        if re.search(pattern, raw, re.IGNORECASE):
            # Update existing field
            raw = re.sub(pattern, rf'\g<1>{value}\g<2>', raw, flags=re.IGNORECASE)
        else:
            # Add new field before closing brace
            raw = re.sub(r'(\s*)\}(\s*)$', rf',\n  {field} = {{{value}}}\n}}\2', raw)

    return raw


def generate_report(entries: dict, enrichment_results: dict) -> str:
    """Generate enrichment report."""
    lines = []
    lines.append("=" * 70)
    lines.append("  BIBTEX ENRICHMENT REPORT")
    lines.append(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("=" * 70)

    lines.append(f"\n  Total entries: {len(entries)}")

    # Count stats
    with_doi = sum(1 for e in entries.values() if e['fields'].get('doi'))
    without_doi = len(entries) - with_doi

    lines.append(f"  With DOI: {with_doi}")
    lines.append(f"  Without DOI: {without_doi}")

    # Enrichment stats
    if enrichment_results:
        dois_found = sum(1 for r in enrichment_results.values() if 'doi' in r)
        citations_updated = sum(1 for r in enrichment_results.values() if 'citations' in r)
        other_updates = sum(1 for r in enrichment_results.values() if any(k not in ['doi', 'citations'] for k in r))

        lines.append(f"\n  Enrichment:")
        lines.append(f"    DOIs found: {dois_found}")
        lines.append(f"    Citations updated: {citations_updated}")
        lines.append(f"    Other fields updated: {other_updates}")

        # Details
        if enrichment_results:
            lines.append(f"\n  Details:")
            for key, updates in enrichment_results.items():
                if updates:
                    lines.append(f"    {key}:")
                    for field, value in updates.items():
                        display_value = value[:50] + '...' if len(str(value)) > 50 else value
                        lines.append(f"      + {field}: {display_value}")

    lines.append("\n" + "=" * 70)

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Enrich BibTeX with CrossRef data'
    )
    parser.add_argument('--update', '-u', action='store_true',
                        help='Apply updates to BibTeX file')
    parser.add_argument('--validate', '-V', action='store_true',
                        help='Validate DOIs only')
    parser.add_argument('--citations', '-c', action='store_true',
                        help='Update citation counts only')
    parser.add_argument('--entry', '-e',
                        help='Process single entry by key')
    parser.add_argument('--find-dois', '-f', action='store_true',
                        help='Find missing DOIs')
    parser.add_argument('--limit', '-n', type=int, default=50,
                        help='Limit number of entries to process')
    parser.add_argument('--input', '-i', default=BIBTEX_PATH,
                        help='Input BibTeX file')
    parser.add_argument('--output', '-o',
                        help='Output file (default: overwrite input)')

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: BibTeX file not found: {args.input}")
        return 1

    print(f"Loading {args.input}...")
    entries = parse_bibtex(args.input)
    print(f"Loaded {len(entries)} entries")

    client = CrossRefClient()

    # Validation mode
    if args.validate:
        print("\nValidating DOIs...")
        results = validate_entries(entries, client)

        print(f"\n✅ Valid DOIs: {len(results['valid'])}")
        print(f"❌ Invalid DOIs: {len(results['invalid'])}")
        print(f"⚠️  Missing DOIs: {len(results['missing'])}")

        if results['invalid']:
            print("\nInvalid DOIs:")
            for key in results['invalid'][:10]:
                doi = entries[key]['fields'].get('doi', '')
                print(f"  {key}: {doi}")

        return 0

    # Single entry mode
    if args.entry:
        if args.entry not in entries:
            print(f"Error: Entry '{args.entry}' not found")
            return 1

        entry = entries[args.entry]
        print(f"\nProcessing: {args.entry}")
        info = get_entry_info(entry)
        print(f"  Title: {info['title'][:60]}...")
        print(f"  DOI: {info['doi'] or 'None'}")

        updates = enrich_entry(entry, client)

        if updates:
            print(f"\nUpdates found:")
            for field, value in updates.items():
                print(f"  + {field}: {value}")

            if args.update:
                print("\n(Use --update to apply)")
        else:
            print("\nNo updates needed.")

        return 0

    # Batch enrichment
    enrichment_results = {}
    entries_to_process = list(entries.items())[:args.limit]

    if args.find_dois:
        # Only entries without DOI
        entries_to_process = [
            (k, v) for k, v in entries.items()
            if not v['fields'].get('doi')
        ][:args.limit]
        print(f"\nSearching DOIs for {len(entries_to_process)} entries without DOI...")

    elif args.citations:
        # Only entries with DOI
        entries_to_process = [
            (k, v) for k, v in entries.items()
            if v['fields'].get('doi')
        ][:args.limit]
        print(f"\nUpdating citations for {len(entries_to_process)} entries...")

    else:
        print(f"\nProcessing {len(entries_to_process)} entries...")

    for i, (key, entry) in enumerate(entries_to_process):
        if (i + 1) % 10 == 0:
            print(f"  Progress: {i + 1}/{len(entries_to_process)}")

        try:
            if args.citations:
                # Only update citations
                info = get_entry_info(entry)
                if info['doi']:
                    count = client.get_citations_count(info['doi'])
                    if count:
                        enrichment_results[key] = {'citations': str(count)}
            else:
                updates = enrich_entry(entry, client)
                if updates:
                    enrichment_results[key] = updates

            # Rate limiting
            time.sleep(0.2)

        except Exception as e:
            print(f"  Error processing {key}: {e}")

    # Generate report
    report = generate_report(entries, enrichment_results)
    print(report)

    # Apply updates if requested
    if args.update and enrichment_results:
        print("\nApplying updates...")

        # Backup
        with open(args.input, 'r') as f:
            original_content = f.read()

        backup_path = args.input + '.backup'
        with open(backup_path, 'w') as f:
            f.write(original_content)
        print(f"  Backup saved to: {backup_path}")

        # Apply updates
        updated_content = original_content
        for key, updates in enrichment_results.items():
            entry = entries[key]
            old_raw = entry['raw']
            new_raw = update_bibtex_entry(old_raw, updates)
            updated_content = updated_content.replace(old_raw, new_raw)

        # Write output
        output_path = args.output or args.input
        with open(output_path, 'w') as f:
            f.write(updated_content)
        print(f"  Updated file: {output_path}")

    elif enrichment_results and not args.update:
        print("\nRun with --update to apply changes.")

    return 0


if __name__ == '__main__':
    sys.exit(main())
