#!/usr/bin/env python3
"""
Add Evidence Tier - Classify papers by journal quality.

Evidence Tiers:
  1 (Gold): Top-5 journals (QJE, AER, JPE, Econometrica, REStud) + Science/Nature
  2 (Silver): Top Field journals, NBER, peer-reviewed
  3 (Bronze): Working papers, preprints, other

Usage:
    python scripts/add_evidence_tier.py --dry-run
    python scripts/add_evidence_tier.py

Author: EBF Team
Version: 1.0.0
"""

import argparse
import re

BIBTEX_PATH = 'bibliography/bcm_master.bib'

# Tier 1: Top-5 Economics + Top Science
TIER_1_JOURNALS = [
    'quarterly journal of economics',
    'american economic review',
    'journal of political economy',
    'econometrica',
    'review of economic studies',
    'science',
    'nature',
    'nature human behaviour',
    'proceedings of the national academy',
    'pnas',
]

# Tier 2: Top Field Journals + Good General
TIER_2_JOURNALS = [
    'journal of finance',
    'review of financial studies',
    'journal of financial economics',
    'journal of monetary economics',
    'journal of public economics',
    'journal of labor economics',
    'journal of development economics',
    'journal of health economics',
    'journal of urban economics',
    'journal of economic theory',
    'journal of econometrics',
    'games and economic behavior',
    'experimental economics',
    'journal of economic behavior',
    'journal of behavioral',
    'management science',
    'american economic journal',
    'review of economics and statistics',
    'economic journal',
    'journal of the european economic',
    'rand journal',
    'international economic review',
    'journal of economic perspectives',
    'journal of economic literature',
    'brookings papers',
    'nber',
    'psychological science',
    'journal of personality and social psychology',
    'cognition',
    'judgment and decision making',
    'organizational behavior',
]

# Tier 3 indicators (working papers, preprints)
TIER_3_INDICATORS = [
    'working paper',
    'discussion paper',
    'ssrn',
    'arxiv',
    'preprint',
    'mimeo',
    'manuscript',
    'unpublished',
]


def determine_evidence_tier(entry_type: str, journal: str, note: str = '') -> int:
    """Determine evidence tier based on journal and entry type."""

    # Normalize
    journal_lower = (journal or '').lower()
    note_lower = (note or '').lower()

    # Check for Tier 3 indicators first
    for indicator in TIER_3_INDICATORS:
        if indicator in journal_lower or indicator in note_lower:
            return 3

    # Books and techreports default to Tier 2 unless working paper
    if entry_type in ['book', 'incollection']:
        return 2

    if entry_type == 'techreport':
        # NBER is Tier 2
        if 'nber' in journal_lower or 'national bureau' in journal_lower:
            return 2
        return 3

    # Check Tier 1 journals
    for t1_journal in TIER_1_JOURNALS:
        if t1_journal in journal_lower:
            return 1

    # Check Tier 2 journals
    for t2_journal in TIER_2_JOURNALS:
        if t2_journal in journal_lower:
            return 2

    # Default: if it has a journal, assume peer-reviewed (Tier 2)
    # Otherwise Tier 3
    if journal and len(journal) > 3:
        return 2

    return 3


def process_bibtex(dry_run: bool = False):
    """Process BibTeX file and add evidence_tier."""

    with open(BIBTEX_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    stats = {
        'entries': 0,
        'tier_1': 0,
        'tier_2': 0,
        'tier_3': 0,
        'already_has': 0,
        'added': 0
    }

    current_entry = {}
    in_entry = False
    entry_lines = []

    for line in lines:
        # Detect entry start
        entry_match = re.match(r'@(\w+)\s*\{\s*([^,]+)\s*,', line)
        if entry_match:
            # Process previous entry
            if in_entry and entry_lines:
                new_lines.extend(entry_lines)

            in_entry = True
            entry_lines = [line]
            current_entry = {
                'type': entry_match.group(1).lower(),
                'key': entry_match.group(2).strip(),
                'journal': '',
                'note': '',
                'has_tier': False
            }
            stats['entries'] += 1
            continue

        if in_entry:
            entry_lines.append(line)

            # Check for fields
            field_match = re.match(r'\s*(\w+)\s*=\s*\{(.+?)\}', line)
            if field_match:
                field_name = field_match.group(1).lower()
                field_value = field_match.group(2)

                if field_name == 'journal':
                    current_entry['journal'] = field_value
                elif field_name == 'booktitle':
                    current_entry['journal'] = field_value
                elif field_name == 'note':
                    current_entry['note'] = field_value
                elif field_name == 'evidence_tier':
                    current_entry['has_tier'] = True
                    stats['already_has'] += 1

            # Detect entry end
            if line.strip() == '}':
                if not current_entry['has_tier']:
                    tier = determine_evidence_tier(
                        current_entry['type'],
                        current_entry['journal'],
                        current_entry['note']
                    )

                    # Track stats
                    if tier == 1:
                        stats['tier_1'] += 1
                    elif tier == 2:
                        stats['tier_2'] += 1
                    else:
                        stats['tier_3'] += 1

                    # Insert before closing brace
                    entry_lines = entry_lines[:-1]
                    if entry_lines and not entry_lines[-1].rstrip().endswith(','):
                        last = entry_lines[-1].rstrip()
                        if last and last != '{':
                            entry_lines[-1] = last + ',\n'

                    entry_lines.append(f'  evidence_tier = {{{tier}}},\n')
                    entry_lines.append('}\n')
                    stats['added'] += 1

                new_lines.extend(entry_lines)
                in_entry = False
                entry_lines = []
        else:
            new_lines.append(line)

    # Handle last entry
    if in_entry and entry_lines:
        new_lines.extend(entry_lines)

    # Summary
    print(f"\n📊 Evidence Tier Classification:")
    print(f"   Total entries:    {stats['entries']}")
    print(f"   Already has tier: {stats['already_has']}")
    print(f"   Tier 1 (Gold):    {stats['tier_1']}")
    print(f"   Tier 2 (Silver):  {stats['tier_2']}")
    print(f"   Tier 3 (Bronze):  {stats['tier_3']}")
    print(f"   Total added:      {stats['added']}")

    if dry_run:
        print(f"\n⚠️  Dry run - no changes written")
    else:
        with open(BIBTEX_PATH, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f"\n✅ Updated {BIBTEX_PATH}")


def main():
    parser = argparse.ArgumentParser(description='Add evidence_tier to BibTeX')
    parser.add_argument('--dry-run', action='store_true', help='Preview without changes')
    args = parser.parse_args()

    print("=" * 60)
    print("ADD EVIDENCE TIER")
    print("=" * 60)

    process_bibtex(dry_run=args.dry_run)


if __name__ == '__main__':
    main()
