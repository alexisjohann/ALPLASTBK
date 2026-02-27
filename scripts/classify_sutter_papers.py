#!/usr/bin/env python3
"""
Systematic classification of Sutter papers: Add integration_level to all PAP-sutter*.yaml files.

Integration Level Rules (from CLAUDE.md):
  I0: Metadata only
  I1: use_for assigned
  I2: + theory_support
  I3: + case_registry (case_integration or linked_cases)
  I4: Dedicated Appendix
  I5: Full Framework Integration

Usage:
  python scripts/classify_sutter_papers.py --dry-run          # Show what would change
  python scripts/classify_sutter_papers.py --batch 1          # Process 1 file (test)
  python scripts/classify_sutter_papers.py --batch 10         # Process 10 files
  python scripts/classify_sutter_papers.py                    # Process all files
"""

import argparse
import glob
import os
import re
import sys
import yaml


def determine_integration_level(data):
    """Determine integration level from existing components."""
    ebf = data.get('ebf_integration', {})

    has_use_for = bool(ebf.get('use_for'))
    has_theory_support = bool(ebf.get('theory_support'))
    has_case = bool(ebf.get('case_integration') or data.get('linked_cases'))
    has_parameters = bool(data.get('parameter_contributions'))
    has_key_findings = bool(data.get('key_findings_structured'))
    has_behavioral_mapping = bool(data.get('behavioral_mapping'))
    has_full_text = bool(data.get('full_text', {}).get('available'))

    # Determine level
    if has_use_for and has_theory_support and has_case and has_parameters and has_key_findings and has_behavioral_mapping:
        return 5, 'FULL'
    if has_use_for and has_theory_support and has_case:
        return 3, 'CASE'
    if has_use_for and has_theory_support:
        return 2, 'STANDARD'
    if has_use_for:
        return 1, 'MINIMAL'
    return 0, 'METADATA'


def add_integration_level(filepath, dry_run=False):
    """Add integration_level to a YAML file if missing."""
    with open(filepath, 'r') as f:
        content = f.read()

    # Parse YAML
    data = yaml.safe_load(content)
    if not data:
        return None, "empty file"

    # Check for existing integration_level in both ebf_integration AND prior_score
    ebf = data.get('ebf_integration', {})
    existing_ebf_level = ebf.get('integration_level')
    existing_prior_level = data.get('prior_score', {}).get('integration_level')

    # Use either location
    existing_level = existing_ebf_level or existing_prior_level

    # Determine correct level
    level_num, level_name = determine_integration_level(data)

    if existing_level:
        # Parse existing level (could be "I1", "I2", etc. or just int)
        if isinstance(existing_level, str) and existing_level.startswith('I'):
            existing_num = int(existing_level[1:])
        else:
            existing_num = int(existing_level)
        if existing_num == level_num:
            return None, f"already I{level_num} (correct)"
        else:
            return None, f"already I{existing_num} (computed I{level_num}, keeping existing)"

    # Add integration_level and integration_level_name
    if dry_run:
        return level_num, f"would add I{level_num} ({level_name})"

    # Find the right place to insert: after evidence_tier line in ebf_integration
    lines = content.split('\n')
    new_lines = []
    inserted = False
    in_ebf = False

    for i, line in enumerate(lines):
        new_lines.append(line)

        # Detect ebf_integration section
        if line.strip().startswith('ebf_integration:'):
            in_ebf = True
            continue

        # Insert after evidence_tier line
        if in_ebf and not inserted:
            if line.strip().startswith('evidence_tier:'):
                new_lines.append(f'  integration_level: {level_num}')
                new_lines.append(f'  integration_level_name: {level_name}')
                inserted = True
                in_ebf = False
                continue
            # If we hit use_for before evidence_tier, insert before use_for
            if line.strip().startswith('use_for:'):
                # Insert before use_for
                new_lines.pop()  # Remove the use_for line we just added
                new_lines.append(f'  integration_level: {level_num}')
                new_lines.append(f'  integration_level_name: {level_name}')
                new_lines.append(line)  # Re-add use_for
                inserted = True
                in_ebf = False
                continue

    # If not inserted yet (no evidence_tier found), try after ebf_integration: line
    if not inserted:
        new_lines = []
        for i, line in enumerate(lines):
            new_lines.append(line)
            if line.strip().startswith('ebf_integration:'):
                new_lines.append(f'  integration_level: {level_num}')
                new_lines.append(f'  integration_level_name: {level_name}')
                inserted = True

    if not inserted:
        return None, "could not find insertion point"

    with open(filepath, 'w') as f:
        f.write('\n'.join(new_lines))

    return level_num, f"added I{level_num} ({level_name})"


def main():
    parser = argparse.ArgumentParser(description='Classify Sutter papers with integration levels')
    parser.add_argument('--dry-run', action='store_true', help='Show what would change without modifying files')
    parser.add_argument('--batch', type=int, default=0, help='Process only N files (0=all)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show details for each file')
    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pattern = os.path.join(base_dir, 'data', 'paper-references', 'PAP-sutter*.yaml')
    files = sorted(glob.glob(pattern))

    if args.batch > 0:
        files = files[:args.batch]

    print(f"{'[DRY RUN] ' if args.dry_run else ''}Processing {len(files)} Sutter paper files...")
    print()

    stats = {'I0': 0, 'I1': 0, 'I2': 0, 'I3': 0, 'I4': 0, 'I5': 0, 'skipped': 0, 'errors': 0}
    changes = []

    for filepath in files:
        fname = os.path.basename(filepath)
        try:
            level, msg = add_integration_level(filepath, dry_run=args.dry_run)
            if level is not None:
                stats[f'I{level}'] += 1
                changes.append((fname, level, msg))
                if args.verbose:
                    print(f"  {'→' if not args.dry_run else '~'} {fname}: {msg}")
            else:
                stats['skipped'] += 1
                if args.verbose:
                    print(f"  - {fname}: {msg}")
        except Exception as e:
            stats['errors'] += 1
            print(f"  ✗ {fname}: ERROR - {e}")

    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    total_changed = sum(stats[f'I{i}'] for i in range(6))
    print(f"Total files:    {len(files)}")
    print(f"Changed:        {total_changed}")
    print(f"Skipped:        {stats['skipped']}")
    print(f"Errors:         {stats['errors']}")
    print()
    print("Integration Level Distribution (changes):")
    for i in range(6):
        count = stats[f'I{i}']
        if count > 0:
            bar = '█' * count
            print(f"  I{i}: {count:3d} {bar}")
    print()

    if changes and not args.dry_run:
        print(f"Successfully classified {total_changed} papers.")
    elif changes and args.dry_run:
        print(f"Would classify {total_changed} papers. Run without --dry-run to apply.")


if __name__ == '__main__':
    main()
