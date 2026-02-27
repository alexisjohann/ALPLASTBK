#!/usr/bin/env python3
"""
Upgrade parameters to Tier 1 that already have literature_sources.

EXPERIMENTAL MODE: Run with --batch N to control how many at once.

Usage:
  python scripts/upgrade_parameters_tier1.py --dry-run          # Show what would change
  python scripts/upgrade_parameters_tier1.py --batch 1          # Upgrade 1 (test)
  python scripts/upgrade_parameters_tier1.py --batch 10         # Upgrade 10
  python scripts/upgrade_parameters_tier1.py --batch all        # Upgrade all
"""

import yaml
import sys
import argparse
from datetime import datetime
from copy import deepcopy


def load_registry(path='data/parameter-registry.yaml'):
    with open(path, 'r') as f:
        return yaml.safe_load(f)


def save_registry(data, path='data/parameter-registry.yaml'):
    with open(path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, width=120, sort_keys=False)


def find_upgradeable(data):
    """Find parameters that have literature_sources but tier != 1."""
    upgradeable = []

    for section_key, section_val in data.items():
        if not isinstance(section_val, list):
            continue
        if not section_val or not isinstance(section_val[0], dict):
            continue
        if 'id' not in section_val[0]:
            continue

        for i, param in enumerate(section_val):
            tier = param.get('parameter_tier')
            has_lit = bool(param.get('literature_sources'))

            if has_lit and tier != 1:
                upgradeable.append({
                    'section': section_key,
                    'index': i,
                    'id': param.get('id', 'UNKNOWN'),
                    'name': param.get('name', param.get('symbol', 'UNKNOWN')),
                    'current_tier': tier,
                    'lit_count': len(param.get('literature_sources', [])),
                })

    return upgradeable


def upgrade_params(data, upgradeable, batch_size):
    """Upgrade specified parameters to Tier 1."""
    if batch_size == 'all':
        to_upgrade = upgradeable
    else:
        to_upgrade = upgradeable[:int(batch_size)]

    upgraded = []
    for item in to_upgrade:
        section = data[item['section']]
        param = section[item['index']]

        old_tier = param.get('parameter_tier', 'MISSING')
        param['parameter_tier'] = 1

        # Also set last_updated if not present
        if 'last_updated' not in param:
            param['last_updated'] = datetime.now().strftime('%Y-%m-%d')

        upgraded.append({
            'id': item['id'],
            'name': item['name'],
            'section': item['section'],
            'old_tier': old_tier,
            'lit_count': item['lit_count'],
        })

    return upgraded


def main():
    parser = argparse.ArgumentParser(description='Upgrade parameters with literature to Tier 1')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be upgraded')
    parser.add_argument('--batch', type=str, default='1', help='Number to upgrade (or "all")')
    parser.add_argument('--section', type=str, default=None, help='Only upgrade specific section')
    args = parser.parse_args()

    data = load_registry()
    upgradeable = find_upgradeable(data)

    if args.section:
        upgradeable = [u for u in upgradeable if u['section'] == args.section]

    print(f"Found {len(upgradeable)} parameters with literature but tier != 1")
    print()

    if args.dry_run:
        print("DRY RUN — would upgrade:")
        for i, u in enumerate(upgradeable):
            tier_str = f"Tier {u['current_tier']}" if u['current_tier'] else "NO TIER"
            print(f"  {i+1:3d}. {u['id']:20s} [{u['section']:30s}] {tier_str:10s} → Tier 1  ({u['lit_count']} sources)")
        print(f"\nTotal: {len(upgradeable)} parameters")
        return

    # Upgrade
    upgraded = upgrade_params(data, upgradeable, args.batch)

    if not upgraded:
        print("Nothing to upgrade.")
        return

    # Update metadata
    if 'metadata' in data:
        data['metadata']['last_updated'] = datetime.now().strftime('%Y-%m-%d')
        old_version = data['metadata'].get('version', '1.22')
        # Increment patch version
        parts = str(old_version).split('.')
        if len(parts) >= 2:
            parts[-1] = str(int(parts[-1]) + 1)
            data['metadata']['version'] = '.'.join(parts)

    save_registry(data)

    print(f"Upgraded {len(upgraded)} parameters to Tier 1:")
    for u in upgraded:
        tier_str = f"Tier {u['old_tier']}" if u['old_tier'] else "NO TIER"
        print(f"  ✅ {u['id']:20s} [{u['section']:30s}] {tier_str:10s} → Tier 1  ({u['lit_count']} lit sources)")

    print(f"\nTotal upgraded: {len(upgraded)}")
    remaining = len(upgradeable) - len(upgraded)
    if remaining > 0:
        print(f"Remaining: {remaining} (run with --batch {remaining} or --batch all)")


if __name__ == '__main__':
    main()
