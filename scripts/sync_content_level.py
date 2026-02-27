#!/usr/bin/env python3
"""
Synchronize Content Level Between Fields
=========================================

Ensures content_level is consistent between:
- prior_score.content_level (authoritative - based on actual content analysis)
- full_text.content_level (should mirror prior_score.content_level)

Per Appendix BM Definition 2:
  L0: Metadata only (no abstract)
  L1: Abstract available (>2000 chars combined content)
  L2: Methodology + Findings (>6000 chars)
  L3: Full text (>50000 chars)

Usage:
    python scripts/sync_content_level.py --report    # Report only
    python scripts/sync_content_level.py --update    # Apply fixes
"""

import argparse
import yaml
from pathlib import Path
from datetime import datetime


def load_yaml(filepath: Path) -> dict:
    """Load YAML file safely."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return {}


def save_yaml(filepath: Path, data: dict) -> bool:
    """Save YAML with proper formatting."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        return True
    except Exception as e:
        print(f"Error saving {filepath}: {e}")
        return False


def sync_content_level(paper_dir: Path, dry_run: bool = True) -> dict:
    """
    Synchronize content_level from prior_score to full_text.

    Returns:
        Dict with statistics
    """
    stats = {
        'total': 0,
        'synced': 0,
        'already_consistent': 0,
        'missing_prior': 0,
        'missing_fulltext': 0,
        'errors': 0
    }

    for filepath in sorted(paper_dir.glob('PAP-*.yaml')):
        stats['total'] += 1

        data = load_yaml(filepath)
        if not data:
            stats['errors'] += 1
            continue

        # Get content levels from both locations
        prior_score = data.get('prior_score', {})
        full_text = data.get('full_text', {})

        ps_level = prior_score.get('content_level')
        ft_level = full_text.get('content_level')

        # Check if prior_score has content_level
        if not ps_level:
            stats['missing_prior'] += 1
            continue

        # Check if full_text section exists
        if 'full_text' not in data:
            stats['missing_fulltext'] += 1
            continue

        # Check if already consistent
        if ps_level == ft_level:
            stats['already_consistent'] += 1
            continue

        # Sync: copy from prior_score to full_text
        if not dry_run:
            data['full_text']['content_level'] = ps_level
            if save_yaml(filepath, data):
                stats['synced'] += 1
            else:
                stats['errors'] += 1
        else:
            stats['synced'] += 1

    return stats


def main():
    parser = argparse.ArgumentParser(
        description='Synchronize content_level between prior_score and full_text'
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
        '--paper-dir',
        type=Path,
        default=Path('data/paper-references'),
        help='Directory with paper YAMLs'
    )

    args = parser.parse_args()
    dry_run = not args.update

    print("=" * 70)
    print("SYNC CONTENT LEVEL BETWEEN FIELDS")
    print("=" * 70)
    print(f"Paper dir: {args.paper_dir}")
    print(f"Mode: {'DRY RUN' if dry_run else 'UPDATE'}")
    print()

    stats = sync_content_level(args.paper_dir, dry_run=dry_run)

    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total files:          {stats['total']}")
    print(f"Synced/Would sync:    {stats['synced']}")
    print(f"Already consistent:   {stats['already_consistent']}")
    print(f"Missing prior_score:  {stats['missing_prior']}")
    print(f"Missing full_text:    {stats['missing_fulltext']}")
    print(f"Errors:               {stats['errors']}")

    if dry_run and stats['synced'] > 0:
        print()
        print("⚠️  DRY RUN - No changes made.")
        print(f"   To apply: python scripts/sync_content_level.py --update")


if __name__ == '__main__':
    main()
