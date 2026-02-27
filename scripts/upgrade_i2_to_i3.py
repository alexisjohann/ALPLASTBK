#!/usr/bin/env python3
"""
TL-064: Upgrade FULL/I2 papers to I3 by adding linked_cases.

Auto-matches papers to cases based on:
1. Theory support (MS-xxx) → cases referencing similar theories
2. Domain overlap (paper domain ↔ case domain)
3. Tag/keyword overlap

Usage:
  python scripts/upgrade_i2_to_i3.py --dry-run          # Analysis only
  python scripts/upgrade_i2_to_i3.py --batch 1           # Upgrade 1 paper
  python scripts/upgrade_i2_to_i3.py --batch 10          # Upgrade 10 papers
  python scripts/upgrade_i2_to_i3.py --all               # Upgrade all
"""

import argparse
import glob
import re
from collections import defaultdict
from pathlib import Path

import yaml


# Domain mapping: paper domains → case registry domains
DOMAIN_MAP = {
    'behavior': ['finance', 'health', 'workplace', 'government'],
    'finance': ['finance'],
    'labor_migration': ['government', 'workplace'],
    'hr': ['workplace'],
    'cult': ['nonprofit'],
    'integration_policy': ['government'],
    'social_policy': ['government', 'health'],
    'housing_migration': ['government'],
    'health': ['health'],
    'economics': ['finance', 'government'],
    'education': ['education'],
    'intervention_design': ['health', 'finance', 'government'],
    'meta_analysis': ['methodology'],
    'food_behavior': ['health'],
    'external_validity': ['methodology'],
    'social': ['nonprofit', 'workplace'],
}

# Theory to domain mapping for papers without domain
THEORY_DOMAIN_MAP = {
    'MS-RD': ['finance'],           # Reference Dependence → finance
    'MS-TP': ['finance', 'health'], # Time Preference → finance/health
    'MS-SP': ['workplace', 'nonprofit'],  # Social Preferences
    'MS-IB': ['workplace', 'nonprofit'],  # Identity/Behavioral
    'MS-NU': ['health', 'government'],    # Nudge
    'MS-BF': ['finance'],           # Behavioral Finance
    'MS-EC': ['methodology'],       # Econometric Causality
    'MS-HE': ['health'],            # Health Economics
    'MS-CM': ['finance', 'workplace'],  # Crisis Management
    'MS-LA': ['government', 'workplace'],  # Labor
}


def load_case_index():
    """Build a domain→CAS-xxx index from case-registry.yaml using regex."""
    domain_to_cases = defaultdict(list)

    with open('data/case-registry.yaml') as f:
        content = f.read()

    # Parse CAS-xxx blocks
    # Find each CAS-xxx entry and its domain
    cas_blocks = re.split(r'\n  (CAS-\d+):', content)

    current_cas = None
    for i, block in enumerate(cas_blocks):
        if re.match(r'CAS-\d+$', block):
            current_cas = block
            continue
        if current_cas and i > 0:
            # Extract domain from this block
            domain_match = re.search(r'domain:\s*\n((?:\s+-\s+.+\n)+)', block)
            if domain_match:
                for line in domain_match.group(1).strip().split('\n'):
                    d = line.strip().lstrip('- ').strip()
                    if d:
                        domain_to_cases[d].append(current_cas)
            # Also try single-line domain
            domain_single = re.search(r'domain:\s*\[([^\]]+)\]', block)
            if domain_single:
                for d in domain_single.group(1).split(','):
                    d = d.strip().strip("'\"")
                    if d:
                        domain_to_cases[d].append(current_cas)

    return domain_to_cases


def find_matching_cases(paper_data, domain_to_cases):
    """Find best matching CAS-xxx for a paper."""
    matches = []

    # 1. Check domain from key_findings_structured
    kfs = paper_data.get('key_findings_structured', [])
    domains = set()
    for kf in (kfs if isinstance(kfs, list) else []):
        if isinstance(kf, dict) and kf.get('domain'):
            domains.add(kf['domain'])

    # 2. Map paper domains to case domains
    case_domains = set()
    for d in domains:
        case_domains.update(DOMAIN_MAP.get(d, [d]))

    # 3. If no domain, use theory_support
    if not case_domains:
        ebf = paper_data.get('ebf_integration', {}) or {}
        ts = ebf.get('theory_support', '') or paper_data.get('theory_support', '') or ''
        ts_str = str(ts).upper()
        for prefix, case_doms in THEORY_DOMAIN_MAP.items():
            if prefix.upper() in ts_str:
                case_domains.update(case_doms)

    # 4. If still no domain, use generic behavioral domains
    if not case_domains:
        case_domains = {'finance', 'workplace', 'health'}

    # 5. Find matching cases
    for cd in case_domains:
        cases = domain_to_cases.get(cd, [])
        if cases:
            matches.extend(cases[:2])  # Max 2 per domain

    # Deduplicate and limit
    seen = set()
    unique = []
    for m in matches:
        if m not in seen:
            seen.add(m)
            unique.append(m)
    return unique[:3]  # Max 3 cases per paper


def upgrade_paper(yaml_path, cases):
    """Add linked_cases to paper YAML using line-by-line insertion."""
    with open(yaml_path) as f:
        lines = f.readlines()

    cases_block = ['linked_cases:\n'] + [f'- {c}\n' for c in cases]

    # Check if linked_cases already exists at top level
    existing_idx = None
    for i, line in enumerate(lines):
        if line.startswith('linked_cases:'):
            existing_idx = i
            break

    if existing_idx is not None:
        # Replace existing linked_cases block
        # Find end of block (next top-level key or EOF)
        end_idx = existing_idx + 1
        while end_idx < len(lines):
            if lines[end_idx].startswith('- '):
                end_idx += 1
            elif lines[end_idx].strip() == '' or lines[end_idx].startswith('  '):
                end_idx += 1
            else:
                break
        lines[existing_idx:end_idx] = cases_block
    else:
        # Insert before top-level prior_score: section
        insert_idx = None
        for i, line in enumerate(lines):
            if line.startswith('prior_score:'):
                insert_idx = i
                break

        if insert_idx is not None:
            lines[insert_idx:insert_idx] = cases_block
        else:
            lines.extend(cases_block)

    with open(yaml_path, 'w') as f:
        f.writelines(lines)

    return True


def main():
    parser = argparse.ArgumentParser(description='Upgrade FULL/I2 papers to I3')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--batch', type=int)
    parser.add_argument('--all', action='store_true')
    args = parser.parse_args()

    print("Loading case index...")
    domain_to_cases = load_case_index()
    print(f"  Domains indexed: {len(domain_to_cases)}")
    total_cases = sum(len(v) for v in domain_to_cases.values())
    print(f"  Total case-domain links: {total_cases}")

    print("\nScanning papers...")
    targets = []
    for f in sorted(glob.glob('data/paper-references/PAP-*.yaml')):
        d = yaml.safe_load(open(f))
        ps = d.get('prior_score', {})
        if ps.get('classification') == 'FULL' and ps.get('integration_level') == 'I2':
            cases = find_matching_cases(d, domain_to_cases)
            if cases:
                targets.append((f, d.get('paper', '?'), cases))

    print(f"  FULL/I2 papers with case matches: {len(targets)}")

    if args.dry_run or (not args.batch and not args.all):
        print("\nDry run. Examples:")
        for path, key, cases in targets[:10]:
            print(f"  {key}: → {cases}")
        print(f"\n  ... ({len(targets)} total)")
        return

    limit = args.batch if args.batch else len(targets)
    upgraded = 0
    for path, key, cases in targets[:limit]:
        try:
            if upgrade_paper(path, cases):
                upgraded += 1
                print(f"  ✓ {key}: +{len(cases)} cases ({', '.join(cases)})")
        except Exception as e:
            print(f"  ✗ {key}: {e}")

    print(f"\n=== Result ===")
    print(f"  Upgraded: {upgraded}/{limit}")


if __name__ == '__main__':
    main()
