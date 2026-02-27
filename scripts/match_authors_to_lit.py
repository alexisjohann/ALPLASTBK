#!/usr/bin/env python3
"""
Match Papers to LIT-Appendices by Author Name (Local).

This script matches papers in bcm_master.bib to their corresponding
LIT-appendix based on author names - NO API REQUIRED.

Usage:
    python scripts/match_authors_to_lit.py --dry-run
    python scripts/match_authors_to_lit.py --update

Author: EBF Team
Version: 1.0.0
"""

import argparse
import re
from collections import defaultdict

BIBTEX_PATH = 'bibliography/bcm_master.bib'

# Author name patterns → LIT-Appendix mapping
# Format: (pattern, LIT-code, full_name)
AUTHOR_LIT_MAPPING = [
    # Core Researchers (dedicated appendices)
    (r'\bfehr\b', 'LIT-FEH', 'Ernst Fehr'),
    (r'\bsutter\b', 'LIT-SUT', 'Matthias Sutter'),
    (r'\benke\b', 'LIT-ENK', 'Benjamin Enke'),

    # Kahneman-Tversky tradition
    (r'\bkahneman\b', 'LIT-KT', 'Daniel Kahneman'),
    (r'\btversky\b', 'LIT-KT', 'Amos Tversky'),
    (r'\bthaler\b', 'LIT-KT', 'Richard Thaler'),

    # Other notable researchers → LIT-O with tags
    (r'\bariely\b', 'LIT-O', 'Dan Ariely'),
    (r'\bcamerer\b', 'LIT-O', 'Colin Camerer'),
    (r'\bloewenstein\b', 'LIT-O', 'George Loewenstein'),
    (r'\brabin\b', 'LIT-O', 'Matthew Rabin'),
    (r'\blaibson\b', 'LIT-O', 'David Laibson'),
    (r'\bgneezy\b', 'LIT-O', 'Uri Gneezy'),
    (r'\blist\b', 'LIT-O', 'John List'),
    (r'\bduflo\b', 'LIT-O', 'Esther Duflo'),
    (r'\bbanerjee\b', 'LIT-O', 'Abhijit Banerjee'),
    (r'\bcharness\b', 'LIT-O', 'Gary Charness'),
    (r'\bmullainathan\b', 'LIT-O', 'Sendhil Mullainathan'),
    (r'\bshafir\b', 'LIT-O', 'Eldar Shafir'),
    (r'\bsunstein\b', 'LIT-O', 'Cass Sunstein'),
    (r'\bbenartzi\b', 'LIT-O', 'Shlomo Benartzi'),
    (r'\bschmidt\b', 'LIT-O', 'Klaus Schmidt'),
    (r'\bfischbacher\b', 'LIT-O', 'Urs Fischbacher'),
    (r'\bgächter\b', 'LIT-O', 'Simon Gächter'),
    (r'\bheinrich\b', 'LIT-O', 'Joseph Henrich'),
    (r'\bfalk\b', 'LIT-O', 'Armin Falk'),
]


def process_bibtex():
    """Process BibTeX and match authors to LIT-appendices."""

    with open(BIBTEX_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    stats = defaultdict(int)
    stats['total'] = 0
    stats['updated'] = 0
    stats['already_has'] = 0
    lit_counts = defaultdict(int)

    new_lines = []
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
                'author': '',
                'use_for': '',
                'has_use_for': False
            }
            stats['total'] += 1
            continue

        if in_entry:
            entry_lines.append(line)

            # Check for fields
            field_match = re.match(r'\s*(\w+)\s*=\s*\{(.+?)\}', line)
            if field_match:
                field_name = field_match.group(1).lower()
                field_value = field_match.group(2)

                if field_name == 'author':
                    current_entry['author'] = field_value
                elif field_name == 'use_for':
                    current_entry['use_for'] = field_value
                    current_entry['has_use_for'] = True

            # Detect entry end
            if line.strip() == '}':
                # Match author to LIT-appendix
                author_lower = current_entry['author'].lower()
                matched_lits = set()

                for pattern, lit_code, author_name in AUTHOR_LIT_MAPPING:
                    if re.search(pattern, author_lower, re.IGNORECASE):
                        matched_lits.add(lit_code)
                        lit_counts[lit_code] += 1

                # Update use_for if we found matches
                if matched_lits:
                    current_use_for = current_entry['use_for']
                    if current_use_for:
                        existing = set(v.strip() for v in current_use_for.split(','))
                    else:
                        existing = set()

                    # Add new LITs
                    new_lits = matched_lits - existing
                    if new_lits:
                        all_lits = existing | matched_lits
                        new_use_for = ', '.join(sorted(all_lits))

                        # Update entry_lines
                        if current_entry['has_use_for']:
                            # Replace existing use_for line
                            for i, l in enumerate(entry_lines):
                                if re.match(r'\s*use_for\s*=', l):
                                    entry_lines[i] = f'  use_for = {{{new_use_for}}},\n'
                                    break
                        else:
                            # Insert before closing brace
                            entry_lines = entry_lines[:-1]
                            if entry_lines and not entry_lines[-1].rstrip().endswith(','):
                                last = entry_lines[-1].rstrip()
                                if last and last != '{':
                                    entry_lines[-1] = last + ',\n'
                            entry_lines.append(f'  use_for = {{{new_use_for}}},\n')
                            entry_lines.append('}\n')

                        stats['updated'] += 1
                    else:
                        stats['already_has'] += 1

                new_lines.extend(entry_lines)
                in_entry = False
                entry_lines = []
        else:
            new_lines.append(line)

    # Handle last entry
    if in_entry and entry_lines:
        new_lines.extend(entry_lines)

    return new_lines, stats, lit_counts


def main():
    parser = argparse.ArgumentParser(description='Match authors to LIT-appendices')
    parser.add_argument('--dry-run', action='store_true', help='Preview without changes')
    parser.add_argument('--update', action='store_true', help='Apply changes')
    args = parser.parse_args()

    print("=" * 70)
    print("AUTHOR → LIT-APPENDIX MATCHING")
    print("=" * 70)

    new_lines, stats, lit_counts = process_bibtex()

    print(f"\n📊 Results:")
    print(f"   Total entries:     {stats['total']}")
    print(f"   Newly linked:      {stats['updated']}")
    print(f"   Already linked:    {stats['already_has']}")

    print(f"\n📚 Papers per LIT-Appendix:")
    for lit, count in sorted(lit_counts.items(), key=lambda x: -x[1]):
        print(f"   {lit}: {count}")

    if args.update and stats['updated'] > 0:
        print(f"\n📝 Updating {BIBTEX_PATH}...")
        with open(BIBTEX_PATH, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f"✅ Updated {stats['updated']} entries")
    elif not args.update:
        print(f"\n⚠️  Run with --update to apply changes")


if __name__ == '__main__':
    main()
