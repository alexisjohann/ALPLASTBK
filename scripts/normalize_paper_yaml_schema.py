#!/usr/bin/env python3
"""
Normalize Paper YAML Schema to conform to Appendix BM standards.

This script normalizes all paper YAML files to use Schema A (full metadata):
- paper: bibtex_key without PAP- prefix
- superkey: PAP-{bibtex_key}
- title: Extracted from BibTeX or DOI lookup
- year: Extracted from BibTeX or DOI lookup
- author/authors: Extracted from BibTeX

Migration paths:
- Schema B (bibtex_key/id) → Schema A (paper/superkey/title/year)
- Schema C (doi only) → Schema A via DOI lookup or BibTeX matching

References:
    - Appendix BM: Paper Database Schema & Prior Score Methodology
    - SSOT: data/paper-references/PAP-{key}.yaml

Usage:
    python scripts/normalize_paper_yaml_schema.py --report  # Report only
    python scripts/normalize_paper_yaml_schema.py --batch   # Normalize all
    python scripts/normalize_paper_yaml_schema.py --single PAP-xyz.yaml
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
from collections import defaultdict
import yaml

def load_yaml(filepath: Path) -> Optional[Dict]:
    """Load a YAML file safely."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None


def save_yaml(filepath: Path, data: Dict) -> bool:
    """Save YAML file with proper formatting."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        return True
    except Exception as e:
        print(f"Error saving {filepath}: {e}")
        return False


def load_bibtex_db_simple(bib_path: Path) -> Dict[str, Dict]:
    """
    Load BibTeX database using simple regex parsing.
    No external dependencies required.
    """
    bibtex_db = {}

    try:
        with open(bib_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Split by @ entries
        entries = re.split(r'\n@', content)

        for entry in entries:
            if not entry.strip():
                continue

            # Add back the @ if split removed it
            if not entry.startswith('@'):
                entry = '@' + entry

            # Extract entry key
            key_match = re.search(r'@\w+\{([^,]+),', entry)
            if not key_match:
                continue

            key = key_match.group(1).strip()
            entry_dict = {'ID': key}

            # Extract title
            title_match = re.search(r'title\s*=\s*[{"](.+?)[}"]', entry, re.IGNORECASE | re.DOTALL)
            if title_match:
                title = title_match.group(1).strip()
                # Clean up braces and newlines
                title = re.sub(r'\{|\}', '', title)
                title = re.sub(r'\s+', ' ', title)
                entry_dict['title'] = title

            # Extract year
            year_match = re.search(r'year\s*=\s*[{"]?(\d{4})[}"]?', entry, re.IGNORECASE)
            if year_match:
                entry_dict['year'] = year_match.group(1)

            # Extract author
            author_match = re.search(r'author\s*=\s*[{"](.+?)[}"]', entry, re.IGNORECASE | re.DOTALL)
            if author_match:
                author = author_match.group(1).strip()
                author = re.sub(r'\s+', ' ', author)
                entry_dict['author'] = author

            bibtex_db[key] = entry_dict

    except Exception as e:
        print(f"Error loading BibTeX: {e}")

    return bibtex_db


def extract_key_from_filename(filename: str) -> str:
    """Extract paper key from filename like PAP-xyz.yaml."""
    match = re.match(r'PAP-(.+)\.yaml$', filename)
    if match:
        return match.group(1)
    return filename.replace('.yaml', '').replace('PAP-', '')


def detect_schema(data: Dict) -> str:
    """Detect which schema variant the file uses."""
    has_paper = 'paper' in data
    has_superkey = 'superkey' in data
    has_bibtex_key = 'bibtex_key' in data
    has_id = 'id' in data
    has_doi = 'doi' in data

    if has_paper and has_superkey:
        return 'A_FULL'
    elif has_bibtex_key or has_id:
        return 'B_MINIMAL'
    elif has_doi:
        return 'C_DOI_ONLY'
    else:
        return 'UNKNOWN'


def normalize_to_schema_a(filepath: Path, data: Dict, bibtex_db: Dict) -> Tuple[Dict, List[str]]:
    """
    Normalize file data to Schema A format.

    Returns:
        Tuple of (normalized_data, list of changes made)
    """
    changes = []
    normalized = dict(data)  # Copy

    # Extract key from filename
    filename = filepath.name
    key_from_filename = extract_key_from_filename(filename)

    # Determine paper key
    paper_key = None
    if 'paper' in data:
        paper_key = data['paper']
    elif 'bibtex_key' in data:
        paper_key = data['bibtex_key']
        changes.append(f"paper: {paper_key} (from bibtex_key)")
    elif 'id' in data:
        # id is usually PAP-xxx, extract xxx
        id_val = data['id']
        paper_key = id_val.replace('PAP-', '') if id_val.startswith('PAP-') else id_val
        changes.append(f"paper: {paper_key} (from id)")
    else:
        paper_key = key_from_filename
        changes.append(f"paper: {paper_key} (from filename)")

    # Set paper field
    if 'paper' not in normalized:
        normalized['paper'] = paper_key

    # Set superkey
    superkey = f"PAP-{paper_key}"
    if 'superkey' not in normalized:
        normalized['superkey'] = superkey
        changes.append(f"superkey: {superkey}")

    # Try to get title and year from BibTeX
    bib_entry = bibtex_db.get(paper_key, {})

    # Title
    if 'title' not in normalized:
        if 'title' in bib_entry:
            normalized['title'] = bib_entry['title'].strip('{}')
            changes.append(f"title: from BibTeX")
        else:
            normalized['title'] = f"[Title for {paper_key}]"
            changes.append(f"title: PLACEHOLDER (needs manual entry)")

    # Year
    if 'year' not in normalized:
        if 'year' in bib_entry:
            normalized['year'] = str(bib_entry['year'])
            changes.append(f"year: {normalized['year']} (from BibTeX)")
        else:
            # Try to extract from key (e.g., fehr1999theory -> 1999)
            year_match = re.search(r'(\d{4})', paper_key)
            if year_match:
                normalized['year'] = year_match.group(1)
                changes.append(f"year: {normalized['year']} (from key)")
            else:
                normalized['year'] = 'UNKNOWN'
                changes.append(f"year: UNKNOWN (needs manual entry)")

    # Author
    if 'author' not in normalized and 'authors' not in normalized:
        if 'author' in bib_entry:
            normalized['author'] = bib_entry['author']
            changes.append(f"author: from BibTeX")

    # Clean up old fields
    if 'bibtex_key' in normalized and normalized.get('paper') == normalized.get('bibtex_key'):
        # Keep bibtex_key for reference but it's redundant now
        pass

    if 'id' in normalized and normalized.get('superkey') == normalized.get('id'):
        # id is now redundant with superkey
        del normalized['id']
        changes.append("Removed redundant 'id' field")

    # Reorder fields for consistency
    ordered = {}
    field_order = [
        'paper', 'superkey', 'title', 'author', 'authors', 'year',
        'doi', 'publication_type', 'journal', 'volume', 'pages',
        'abstract', 'abstract_source', 'abstract_fetched',
        'url', 'reference_count',
        'full_text', 'ebf_integration', 'prior_score',
        'migration_status', 'ssot_migration_date', 'summary'
    ]

    # Add fields in order
    for field in field_order:
        if field in normalized:
            ordered[field] = normalized[field]

    # Add any remaining fields
    for field in normalized:
        if field not in ordered:
            ordered[field] = normalized[field]

    return ordered, changes


def process_file(filepath: Path, bibtex_db: Dict, dry_run: bool = True) -> Dict[str, Any]:
    """
    Process a single file for normalization.

    Returns:
        Dict with processing results
    """
    result = {
        'filepath': str(filepath),
        'filename': filepath.name,
        'schema_before': 'unknown',
        'schema_after': 'A_FULL',
        'changes': [],
        'success': False,
        'error': None,
    }

    data = load_yaml(filepath)
    if data is None:
        result['error'] = 'Failed to load YAML'
        return result

    result['schema_before'] = detect_schema(data)

    if result['schema_before'] == 'A_FULL':
        result['changes'].append('Already Schema A - no changes needed')
        result['success'] = True
        return result

    # Normalize
    normalized, changes = normalize_to_schema_a(filepath, data, bibtex_db)
    result['changes'] = changes

    if not dry_run:
        if save_yaml(filepath, normalized):
            result['success'] = True
        else:
            result['error'] = 'Failed to save normalized YAML'
    else:
        result['success'] = True
        result['changes'].append('(dry run - no changes written)')

    return result


def main():
    parser = argparse.ArgumentParser(
        description='Normalize Paper YAML Schema to Appendix BM standards'
    )
    parser.add_argument(
        '--report',
        action='store_true',
        help='Report only (dry run)'
    )
    parser.add_argument(
        '--batch',
        action='store_true',
        help='Process all files'
    )
    parser.add_argument(
        '--single',
        type=Path,
        help='Process a single file'
    )
    parser.add_argument(
        '--paper-dir',
        type=Path,
        default=Path('data/paper-references'),
        help='Directory containing paper YAML files'
    )
    parser.add_argument(
        '--bib-file',
        type=Path,
        default=Path('bibliography/bcm_master.bib'),
        help='Path to BibTeX file'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show details for each file'
    )

    args = parser.parse_args()

    # Load BibTeX database (using simple regex parser)
    bibtex_db = {}
    if args.bib_file.exists():
        print(f"Loading BibTeX from {args.bib_file}...")
        bibtex_db = load_bibtex_db_simple(args.bib_file)
        print(f"Loaded {len(bibtex_db)} entries")
    else:
        print(f"Warning: BibTeX file not found at {args.bib_file}")

    dry_run = args.report or not args.batch

    if args.single:
        result = process_file(args.single, bibtex_db, dry_run=dry_run)
        print(f"\nFile: {result['filename']}")
        print(f"  Schema before: {result['schema_before']}")
        print(f"  Changes: {result['changes']}")
        print(f"  Success: {result['success']}")
        if result['error']:
            print(f"  Error: {result['error']}")
        return

    # Process all files
    yaml_files = sorted(args.paper_dir.glob('PAP-*.yaml'))

    stats = {
        'total': len(yaml_files),
        'already_a': 0,
        'normalized': 0,
        'failed': 0,
        'schema_counts': defaultdict(int),
    }

    print(f"\nProcessing {stats['total']} files...")
    print(f"Mode: {'DRY RUN (report only)' if dry_run else 'BATCH UPDATE'}")
    print("-" * 60)

    for filepath in yaml_files:
        result = process_file(filepath, bibtex_db, dry_run=dry_run)

        stats['schema_counts'][result['schema_before']] += 1

        if result['schema_before'] == 'A_FULL':
            stats['already_a'] += 1
        elif result['success']:
            stats['normalized'] += 1
        else:
            stats['failed'] += 1

        if args.verbose or not result['success']:
            print(f"\n{result['filename']}:")
            print(f"  {result['schema_before']} → A_FULL")
            for change in result['changes']:
                print(f"    - {change}")
            if result['error']:
                print(f"  ERROR: {result['error']}")

    # Summary
    print("\n" + "=" * 60)
    print("NORMALIZATION SUMMARY")
    print("=" * 60)
    print(f"\nTotal files:     {stats['total']}")
    print(f"Already Schema A: {stats['already_a']}")
    print(f"Would normalize: {stats['normalized']}")
    print(f"Failed:          {stats['failed']}")

    print(f"\nSchema distribution before:")
    for schema, count in sorted(stats['schema_counts'].items()):
        print(f"  {schema}: {count}")

    if dry_run and stats['normalized'] > 0:
        print(f"\n⚠️  This was a DRY RUN. To apply changes, run:")
        print(f"   python scripts/normalize_paper_yaml_schema.py --batch")


if __name__ == '__main__':
    main()
