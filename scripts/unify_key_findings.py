#!/usr/bin/env python3
"""
TL-063: Unify key_findings field names across paper-references.

Converts:
  key_findings (dict) → key_findings_structured (list)
  key_findings (list) → key_findings_structured (list)

For papers with BOTH key_findings AND key_findings_structured:
  → Remove key_findings (keep key_findings_structured as canonical)

Does NOT touch summary.key_findings (different semantic: narrative string).

Usage:
  python scripts/unify_key_findings.py --dry-run          # Analysis only
  python scripts/unify_key_findings.py --batch 1           # Convert 1 paper
  python scripts/unify_key_findings.py --batch 10          # Convert 10 papers
  python scripts/unify_key_findings.py --all               # Convert all
"""

import argparse
import glob
import sys

import yaml


def load_yaml(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def save_yaml(path, data):
    """Save YAML preserving readability."""
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True,
                  sort_keys=False, width=120)


def analyze_paper(path):
    """Analyze a paper's key_findings fields. Returns action needed."""
    data = load_yaml(path)
    if data is None:
        return None, None

    has_kf = 'key_findings' in data
    has_kfs = 'key_findings_structured' in data

    if not has_kf:
        return 'skip', data

    kf = data['key_findings']

    if has_kfs:
        # Both exist → remove key_findings (keep key_findings_structured)
        return 'remove_kf', data
    elif isinstance(kf, dict):
        # Dict → convert to list-of-one
        return 'dict_to_list', data
    elif isinstance(kf, list):
        # List → rename to key_findings_structured
        return 'rename_list', data
    else:
        # String or other → skip (unexpected)
        return 'skip_unexpected', data


def convert_paper(path, data, action):
    """Apply the conversion and save."""
    if action == 'remove_kf':
        del data['key_findings']
    elif action == 'dict_to_list':
        kf = data.pop('key_findings')
        data['key_findings_structured'] = [kf]
    elif action == 'rename_list':
        kf = data.pop('key_findings')
        data['key_findings_structured'] = kf
    else:
        return False

    save_yaml(path, data)
    return True


def main():
    parser = argparse.ArgumentParser(description='Unify key_findings field names')
    parser.add_argument('--dry-run', action='store_true', help='Analysis only, no changes')
    parser.add_argument('--batch', type=int, help='Convert N papers')
    parser.add_argument('--all', action='store_true', help='Convert all papers')
    args = parser.parse_args()

    papers = sorted(glob.glob('data/paper-references/PAP-*.yaml'))
    print(f"Scanning {len(papers)} papers...")

    actions = {'skip': 0, 'remove_kf': 0, 'dict_to_list': 0, 'rename_list': 0,
               'skip_unexpected': 0, 'error': 0}
    to_convert = []

    for path in papers:
        try:
            action, data = analyze_paper(path)
            if action is None:
                actions['error'] += 1
                continue
            actions[action] = actions.get(action, 0) + 1
            if action in ('remove_kf', 'dict_to_list', 'rename_list'):
                to_convert.append((path, data, action))
        except Exception as e:
            print(f"  ERROR: {path}: {e}")
            actions['error'] += 1

    print(f"\n=== Analysis ===")
    print(f"  skip (no key_findings):     {actions['skip']}")
    print(f"  remove_kf (both exist):     {actions['remove_kf']}")
    print(f"  dict_to_list (dict → list): {actions['dict_to_list']}")
    print(f"  rename_list (list rename):  {actions['rename_list']}")
    print(f"  skip_unexpected:            {actions['skip_unexpected']}")
    print(f"  errors:                     {actions['error']}")
    print(f"  TOTAL to convert:           {len(to_convert)}")

    if args.dry_run or (not args.batch and not args.all):
        print("\nDry run. Use --batch N or --all to apply.")
        # Show examples
        for action_type in ('remove_kf', 'dict_to_list', 'rename_list'):
            examples = [p for p, _, a in to_convert if a == action_type][:3]
            if examples:
                print(f"\n  Examples ({action_type}):")
                for e in examples:
                    print(f"    {e}")
        return

    # Apply conversions
    limit = args.batch if args.batch else len(to_convert)
    converted = 0

    for path, data, action in to_convert[:limit]:
        try:
            if convert_paper(path, data, action):
                converted += 1
                print(f"  ✓ {action}: {path.split('/')[-1]}")
        except Exception as e:
            print(f"  ✗ ERROR {path}: {e}")

    print(f"\n=== Result ===")
    print(f"  Converted: {converted}/{limit}")


if __name__ == '__main__':
    main()
