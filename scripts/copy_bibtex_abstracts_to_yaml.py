#!/usr/bin/env python3
"""
Copy BibTeX Abstracts to Paper Reference YAMLs
==============================================

Copies abstracts from bcm_master.bib to data/paper-references/*.yaml
This is a LOCAL operation - no external API calls required.

Per Appendix BM Definition 2:
- Papers with abstract go from L0 to L1
- Updates prior_score accordingly

Usage:
    python scripts/copy_bibtex_abstracts_to_yaml.py --report    # Report only
    python scripts/copy_bibtex_abstracts_to_yaml.py --update    # Apply changes
"""

import argparse
import re
import yaml
from pathlib import Path
from datetime import date
from typing import Dict, Optional, Tuple


def parse_bibtex_abstracts(bib_path: Path) -> Dict[str, Dict]:
    """Extract abstracts from BibTeX file."""
    abstracts = {}

    with open(bib_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Split into entries
    entries = re.split(r'\n@', content)

    for entry in entries:
        if not entry.strip():
            continue

        # Add back @ if removed
        if not entry.startswith('@'):
            entry = '@' + entry

        # Extract key
        key_match = re.search(r'@\w+\{([^,]+),', entry)
        if not key_match:
            continue
        key = key_match.group(1).strip()

        # Extract abstract - handle multi-line and various brace styles
        abstract_match = re.search(
            r'abstract\s*=\s*[{"](.+?)[}"](?=\s*,?\s*(?:\w+\s*=|$|\}))',
            entry,
            re.IGNORECASE | re.DOTALL
        )

        if abstract_match:
            abstract = abstract_match.group(1).strip()
            # Clean up LaTeX formatting
            abstract = re.sub(r'\{|\}', '', abstract)
            abstract = re.sub(r'\s+', ' ', abstract)
            abstract = abstract.strip()

            if len(abstract) > 50:  # Minimum length for meaningful abstract
                abstracts[key] = {
                    'abstract': abstract,
                    'char_count': len(abstract)
                }

    return abstracts


def load_yaml(filepath: Path) -> Optional[Dict]:
    """Load YAML file safely."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None


def save_yaml(filepath: Path, data: Dict) -> bool:
    """Save YAML with proper formatting."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        return True
    except Exception as e:
        print(f"Error saving {filepath}: {e}")
        return False


def update_yaml_with_abstract(yaml_path: Path, abstract_data: Dict, dry_run: bool = True) -> Tuple[bool, str]:
    """
    Update YAML file with abstract from BibTeX.

    Returns:
        Tuple of (updated, message)
    """
    data = load_yaml(yaml_path)
    if data is None:
        return False, "Failed to load YAML"

    # Check if already has abstract
    existing_abstract = data.get('abstract', '')
    if existing_abstract and len(str(existing_abstract)) > 50:
        return False, "Already has abstract"

    # Add abstract
    abstract = abstract_data['abstract']

    # Insert abstract after doi or publication_type
    ordered = {}
    insert_done = False

    for key, value in data.items():
        ordered[key] = value
        if key in ('doi', 'publication_type') and not insert_done:
            ordered['abstract'] = abstract
            ordered['abstract_source'] = 'bibtex'
            ordered['abstract_fetched'] = str(date.today())
            insert_done = True

    # If not inserted yet, add at end
    if not insert_done:
        ordered['abstract'] = abstract
        ordered['abstract_source'] = 'bibtex'
        ordered['abstract_fetched'] = str(date.today())

    if not dry_run:
        if save_yaml(yaml_path, ordered):
            return True, f"Added {len(abstract)} chars"
        else:
            return False, "Save failed"

    return True, f"Would add {len(abstract)} chars"


def main():
    parser = argparse.ArgumentParser(
        description='Copy BibTeX abstracts to paper reference YAMLs'
    )
    parser.add_argument(
        '--report',
        action='store_true',
        help='Report only (dry run)'
    )
    parser.add_argument(
        '--update',
        action='store_true',
        help='Actually update YAML files'
    )
    parser.add_argument(
        '--bib-file',
        type=Path,
        default=Path('bibliography/bcm_master.bib'),
        help='Path to BibTeX file'
    )
    parser.add_argument(
        '--paper-dir',
        type=Path,
        default=Path('data/paper-references'),
        help='Directory with paper YAMLs'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show details'
    )

    args = parser.parse_args()
    dry_run = not args.update

    print("=" * 70)
    print("COPY BIBTEX ABSTRACTS TO YAML")
    print("=" * 70)
    print(f"BibTeX: {args.bib_file}")
    print(f"Paper dir: {args.paper_dir}")
    print(f"Mode: {'DRY RUN' if dry_run else 'UPDATE'}")
    print()

    # Parse BibTeX
    print("Parsing BibTeX...")
    abstracts = parse_bibtex_abstracts(args.bib_file)
    print(f"Found {len(abstracts)} papers with abstracts in BibTeX")
    print()

    # Process each
    stats = {
        'processed': 0,
        'updated': 0,
        'already_has': 0,
        'no_yaml': 0,
        'errors': 0
    }

    for key, abstract_data in abstracts.items():
        yaml_path = args.paper_dir / f"PAP-{key}.yaml"

        if not yaml_path.exists():
            stats['no_yaml'] += 1
            if args.verbose:
                print(f"  {key}: No YAML file")
            continue

        stats['processed'] += 1
        updated, message = update_yaml_with_abstract(yaml_path, abstract_data, dry_run)

        if "Already has" in message:
            stats['already_has'] += 1
        elif updated:
            stats['updated'] += 1
            if args.verbose or not dry_run:
                print(f"  {key}: {message}")
        else:
            stats['errors'] += 1
            if args.verbose:
                print(f"  {key}: ERROR - {message}")

    # Summary
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"BibTeX abstracts:     {len(abstracts)}")
    print(f"YAMLs processed:      {stats['processed']}")
    print(f"Updated/Would update: {stats['updated']}")
    print(f"Already has abstract: {stats['already_has']}")
    print(f"No YAML file:         {stats['no_yaml']}")
    print(f"Errors:               {stats['errors']}")

    if dry_run and stats['updated'] > 0:
        print()
        print("⚠️  DRY RUN - No changes made.")
        print(f"   To apply: python scripts/copy_bibtex_abstracts_to_yaml.py --update")


if __name__ == '__main__':
    main()
