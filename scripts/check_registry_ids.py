#!/usr/bin/env python3
"""
Registry ID Collision Prevention System
========================================

Prevents ID collisions across all EBF registries by:
1. Checking for duplicate IDs within each registry
2. Suggesting next available ID for new entries
3. Integrating with pre-commit hook to block collisions

REGISTRIES COVERED:
- theory-catalog.yaml: CAT-XX, MS-XX-XXX
- case-registry.yaml: CAS-XXX
- parameter-registry.yaml: PAR-XX-XXX
- bcm_master.bib: PAP-xxxxx (BibTeX keys)
- paper-references/: PAP-xxxxx.yaml

USAGE:
  python scripts/check_registry_ids.py --check          # Check all for duplicates
  python scripts/check_registry_ids.py --next CAT      # Get next CAT-XX
  python scripts/check_registry_ids.py --next CAS      # Get next CAS-XXX
  python scripts/check_registry_ids.py --next MS-CM    # Get next MS-CM-XXX
  python scripts/check_registry_ids.py --next PAR-CM   # Get next PAR-CM-XXX
  python scripts/check_registry_ids.py --validate ID   # Check if ID is available

Author: EBF Framework
Version: 1.0
"""

import argparse
import re
import sys
import yaml
from pathlib import Path
from collections import defaultdict

# Repository root
REPO_ROOT = Path(__file__).parent.parent

# Registry file paths
REGISTRIES = {
    'theory-catalog': REPO_ROOT / 'data' / 'theory-catalog.yaml',
    'case-registry': REPO_ROOT / 'data' / 'case-registry.yaml',
    'parameter-registry': REPO_ROOT / 'data' / 'parameter-registry.yaml',
    'bcm_master': REPO_ROOT / 'bibliography' / 'bcm_master.bib',
    'paper-references': REPO_ROOT / 'data' / 'paper-references',
}

# ID patterns for each type
ID_PATTERNS = {
    'CAT': r'CAT-(\d+)',
    'MS': r'MS-([A-Z]{2,4})-(\d{3})',
    'CAS': r'CAS-(\d+)',
    'PAR': r'PAR-([A-Z]{2,4})-(\d{3})',
    'PAP': r'PAP-([a-z]+\d{4}[a-z]*)',
}


def extract_cat_ids(filepath: Path) -> list:
    """Extract all CAT-XX IDs from theory-catalog.yaml."""
    ids = []
    try:
        content = filepath.read_text()
        matches = re.findall(r'id:\s*CAT-(\d+)', content)
        ids = [int(m) for m in matches]
    except Exception as e:
        print(f"Error reading {filepath}: {e}", file=sys.stderr)
    return ids


def extract_ms_ids(filepath: Path) -> dict:
    """Extract all MS-XX-XXX IDs from theory-catalog.yaml."""
    ids = defaultdict(list)
    try:
        content = filepath.read_text()
        matches = re.findall(r'id:\s*MS-([A-Z]{2,4})-(\d{3})', content)
        for prefix, num in matches:
            ids[prefix].append(int(num))
    except Exception as e:
        print(f"Error reading {filepath}: {e}", file=sys.stderr)
    return ids


def extract_cas_ids(filepath: Path) -> list:
    """Extract all CAS-XXX IDs from case-registry.yaml."""
    ids = []
    try:
        content = filepath.read_text()
        # Match both CAS-XXX: and CAS-XX-XXX formats
        matches = re.findall(r'CAS-(\d+):', content)
        ids = [int(m) for m in matches]
        # Also match CAS-XX-XXX format like CAS-AI-001
        alpha_matches = re.findall(r'CAS-([A-Z]+)-(\d+):', content)
        # These are separate - store them differently if needed
    except Exception as e:
        print(f"Error reading {filepath}: {e}", file=sys.stderr)
    return ids


def extract_par_ids(filepath: Path) -> dict:
    """Extract all PAR-XX-XXX IDs from parameter-registry.yaml."""
    ids = defaultdict(list)
    try:
        content = filepath.read_text()
        matches = re.findall(r'id:\s*PAR-([A-Z]{2,4})-(\d{3})', content)
        for prefix, num in matches:
            ids[prefix].append(int(num))
    except Exception as e:
        print(f"Error reading {filepath}: {e}", file=sys.stderr)
    return ids


def extract_pap_ids(bib_path: Path, yaml_dir: Path) -> set:
    """Extract all PAP-xxxxx IDs from BibTeX and paper-references/."""
    ids = set()

    # From BibTeX
    try:
        content = bib_path.read_text()
        matches = re.findall(r'@\w+\{(PAP-[a-z0-9]+)', content, re.IGNORECASE)
        ids.update(m.lower() for m in matches)
    except Exception as e:
        print(f"Error reading {bib_path}: {e}", file=sys.stderr)

    # From paper-references/
    if yaml_dir.exists():
        for f in yaml_dir.glob('PAP-*.yaml'):
            ids.add(f.stem.lower())

    return ids


def get_next_id(id_type: str, prefix: str = None) -> str:
    """Get next available ID for a given type."""

    if id_type == 'CAT':
        ids = extract_cat_ids(REGISTRIES['theory-catalog'])
        next_num = max(ids) + 1 if ids else 1
        return f"CAT-{next_num}"

    elif id_type == 'MS':
        if not prefix:
            print("Error: MS requires a prefix (e.g., MS-CM, MS-AI)", file=sys.stderr)
            sys.exit(1)
        all_ms = extract_ms_ids(REGISTRIES['theory-catalog'])
        ids = all_ms.get(prefix, [])
        next_num = max(ids) + 1 if ids else 1
        return f"MS-{prefix}-{next_num:03d}"

    elif id_type == 'CAS':
        ids = extract_cas_ids(REGISTRIES['case-registry'])
        next_num = max(ids) + 1 if ids else 1
        return f"CAS-{next_num}"

    elif id_type == 'PAR':
        if not prefix:
            print("Error: PAR requires a prefix (e.g., PAR-CM, PAR-BEH)", file=sys.stderr)
            sys.exit(1)
        all_par = extract_par_ids(REGISTRIES['parameter-registry'])
        ids = all_par.get(prefix, [])
        next_num = max(ids) + 1 if ids else 1
        return f"PAR-{prefix}-{next_num:03d}"

    else:
        print(f"Unknown ID type: {id_type}", file=sys.stderr)
        sys.exit(1)


def check_duplicates() -> dict:
    """Check all registries for duplicate IDs."""
    duplicates = {}

    # CAT duplicates
    cat_ids = extract_cat_ids(REGISTRIES['theory-catalog'])
    cat_dups = [x for x in set(cat_ids) if cat_ids.count(x) > 1]
    if cat_dups:
        duplicates['CAT'] = [f"CAT-{d}" for d in cat_dups]

    # MS duplicates (per prefix)
    ms_ids = extract_ms_ids(REGISTRIES['theory-catalog'])
    for prefix, nums in ms_ids.items():
        dups = [x for x in set(nums) if nums.count(x) > 1]
        if dups:
            duplicates[f'MS-{prefix}'] = [f"MS-{prefix}-{d:03d}" for d in dups]

    # CAS duplicates
    cas_ids = extract_cas_ids(REGISTRIES['case-registry'])
    cas_dups = [x for x in set(cas_ids) if cas_ids.count(x) > 1]
    if cas_dups:
        duplicates['CAS'] = [f"CAS-{d}" for d in cas_dups]

    # PAR duplicates (per prefix)
    par_ids = extract_par_ids(REGISTRIES['parameter-registry'])
    for prefix, nums in par_ids.items():
        dups = [x for x in set(nums) if nums.count(x) > 1]
        if dups:
            duplicates[f'PAR-{prefix}'] = [f"PAR-{prefix}-{d:03d}" for d in dups]

    return duplicates


def validate_id(id_str: str) -> bool:
    """Check if an ID is available (not already used)."""
    id_upper = id_str.upper()

    if id_upper.startswith('CAT-'):
        num = int(id_upper.replace('CAT-', ''))
        existing = extract_cat_ids(REGISTRIES['theory-catalog'])
        return num not in existing

    elif id_upper.startswith('MS-'):
        match = re.match(r'MS-([A-Z]+)-(\d+)', id_upper)
        if match:
            prefix, num = match.groups()
            existing = extract_ms_ids(REGISTRIES['theory-catalog'])
            return int(num) not in existing.get(prefix, [])

    elif id_upper.startswith('CAS-'):
        # Handle both CAS-XXX and CAS-XX-XXX
        match = re.match(r'CAS-(\d+)', id_upper)
        if match:
            num = int(match.group(1))
            existing = extract_cas_ids(REGISTRIES['case-registry'])
            return num not in existing
        return True  # Alpha-prefixed CAS IDs (like CAS-AI-001) need different handling

    elif id_upper.startswith('PAR-'):
        match = re.match(r'PAR-([A-Z]+)-(\d+)', id_upper)
        if match:
            prefix, num = match.groups()
            existing = extract_par_ids(REGISTRIES['parameter-registry'])
            return int(num) not in existing.get(prefix, [])

    elif id_str.lower().startswith('pap-'):
        existing = extract_pap_ids(REGISTRIES['bcm_master'], REGISTRIES['paper-references'])
        return id_str.lower() not in existing

    return True


def show_status():
    """Show current ID status for all registries."""
    print("=" * 70)
    print("EBF REGISTRY ID STATUS")
    print("=" * 70)

    # CAT status
    cat_ids = extract_cat_ids(REGISTRIES['theory-catalog'])
    print(f"\n📁 THEORY CATALOG (theory-catalog.yaml)")
    print(f"   CAT-XX: {len(cat_ids)} categories, highest = CAT-{max(cat_ids) if cat_ids else 0}")
    print(f"   → Next available: CAT-{max(cat_ids)+1 if cat_ids else 1}")

    # MS status
    ms_ids = extract_ms_ids(REGISTRIES['theory-catalog'])
    total_ms = sum(len(v) for v in ms_ids.values())
    print(f"   MS-XX-XXX: {total_ms} theories across {len(ms_ids)} prefixes")
    for prefix in sorted(ms_ids.keys()):
        nums = ms_ids[prefix]
        print(f"      MS-{prefix}: {len(nums)} theories, next = MS-{prefix}-{max(nums)+1:03d}")

    # CAS status
    cas_ids = extract_cas_ids(REGISTRIES['case-registry'])
    print(f"\n📁 CASE REGISTRY (case-registry.yaml)")
    print(f"   CAS-XXX: {len(cas_ids)} cases, highest = CAS-{max(cas_ids) if cas_ids else 0}")
    print(f"   → Next available: CAS-{max(cas_ids)+1 if cas_ids else 1}")

    # PAR status
    par_ids = extract_par_ids(REGISTRIES['parameter-registry'])
    total_par = sum(len(v) for v in par_ids.values())
    print(f"\n📁 PARAMETER REGISTRY (parameter-registry.yaml)")
    print(f"   PAR-XX-XXX: {total_par} parameters across {len(par_ids)} prefixes")
    for prefix in sorted(par_ids.keys()):
        nums = par_ids[prefix]
        print(f"      PAR-{prefix}: {len(nums)} params, next = PAR-{prefix}-{max(nums)+1:03d}")

    # PAP status
    pap_ids = extract_pap_ids(REGISTRIES['bcm_master'], REGISTRIES['paper-references'])
    print(f"\n📁 PAPER REFERENCES (bcm_master.bib + paper-references/)")
    print(f"   PAP-xxxxx: {len(pap_ids)} unique paper IDs")

    # Check duplicates
    print("\n" + "=" * 70)
    print("DUPLICATE CHECK")
    print("=" * 70)
    dups = check_duplicates()
    if dups:
        print("❌ DUPLICATES FOUND:")
        for id_type, dup_list in dups.items():
            print(f"   {id_type}: {', '.join(dup_list)}")
    else:
        print("✅ No duplicates found across all registries")

    print()


def main():
    parser = argparse.ArgumentParser(description='EBF Registry ID Management')
    parser.add_argument('--check', action='store_true', help='Check all registries for duplicates')
    parser.add_argument('--next', metavar='TYPE', help='Get next available ID (CAT, CAS, MS-XX, PAR-XX)')
    parser.add_argument('--validate', metavar='ID', help='Check if ID is available')
    parser.add_argument('--status', action='store_true', help='Show full status of all registries')
    parser.add_argument('--json', action='store_true', help='Output in JSON format')

    args = parser.parse_args()

    if args.status or (not args.check and not args.next and not args.validate):
        show_status()
        return 0

    if args.check:
        dups = check_duplicates()
        if dups:
            print("❌ DUPLICATES FOUND:", file=sys.stderr)
            for id_type, dup_list in dups.items():
                print(f"   {id_type}: {', '.join(dup_list)}", file=sys.stderr)
            return 1
        else:
            print("✅ No duplicates found")
            return 0

    if args.next:
        id_type = args.next.upper()
        prefix = None

        # Handle prefixed types like MS-CM, PAR-BEH
        if '-' in id_type and not id_type.startswith('MS-') and not id_type.startswith('PAR-'):
            pass  # It's already the full prefix
        elif id_type.startswith('MS-'):
            prefix = id_type[3:]  # Extract CM from MS-CM
            id_type = 'MS'
        elif id_type.startswith('PAR-'):
            prefix = id_type[4:]  # Extract BEH from PAR-BEH
            id_type = 'PAR'

        next_id = get_next_id(id_type, prefix)
        print(next_id)
        return 0

    if args.validate:
        available = validate_id(args.validate)
        if available:
            print(f"✅ {args.validate} is AVAILABLE")
            return 0
        else:
            print(f"❌ {args.validate} is ALREADY IN USE")
            return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
