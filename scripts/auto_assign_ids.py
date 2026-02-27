#!/usr/bin/env python3
"""
Auto-Assign Registry IDs
========================

Automatically replaces `id: AUTO` placeholders with real IDs.

USAGE:
    # Preview what would change (dry-run)
    python scripts/auto_assign_ids.py

    # Actually apply changes
    python scripts/auto_assign_ids.py --apply

    # Process specific file
    python scripts/auto_assign_ids.py --file data/case-registry.yaml --apply

WORKFLOW:
    1. User adds entry with `id: AUTO`
    2. Run this script (or pre-commit runs it automatically)
    3. AUTO is replaced with next available ID (e.g., CAS-910)

SUPPORTED PATTERNS:
    - id: AUTO           → CAS-910 (in case-registry.yaml)
    - id: AUTO-CM        → MS-CM-003 (in theory-catalog.yaml)
    - id: AUTO-BEH       → PAR-BEH-018 (in parameter-registry.yaml)
    - id: CAT-AUTO       → CAT-26 (in theory-catalog.yaml)

Author: EBF Framework
Version: 1.0
"""

import re
import sys
import argparse
from pathlib import Path
from typing import List, Tuple, Optional

# Import registry manager
sys.path.insert(0, str(Path(__file__).parent))
from registry_manager import (
    CaseRegistry,
    TheoryCategoryRegistry,
    TheoryModelRegistry,
    ParameterRegistry,
    REPO_ROOT
)


# Registry files to scan
REGISTRY_FILES = {
    'case-registry.yaml': CaseRegistry,
    'theory-catalog.yaml': {
        'CAT': TheoryCategoryRegistry,
        'MS': TheoryModelRegistry,
    },
    'parameter-registry.yaml': ParameterRegistry,
}


def find_auto_ids(content: str, filename: str) -> List[Tuple[str, str, int, str]]:
    """
    Find all AUTO ID placeholders in content.

    Returns: List of (original_match, id_type, line_number, prefix)
    """
    results = []
    lines = content.split('\n')

    for line_num, line in enumerate(lines, 1):
        # Pattern: id: AUTO or id: AUTO-PREFIX or id: TYPE-AUTO

        # CAS-AUTO or id: AUTO (in case-registry)
        if 'case-registry' in filename:
            if re.search(r'id:\s*AUTO\b', line, re.IGNORECASE):
                results.append((line, 'CAS', line_num, None))

        # CAT-AUTO or id: CAT-AUTO
        if 'theory-catalog' in filename:
            match = re.search(r'id:\s*CAT-AUTO\b', line, re.IGNORECASE)
            if match:
                results.append((line, 'CAT', line_num, None))

            # MS-XX-AUTO or id: AUTO-XX (for theories)
            match = re.search(r'id:\s*(?:MS-)?AUTO-([A-Z]{2,4})\b', line, re.IGNORECASE)
            if match:
                prefix = match.group(1).upper()
                results.append((line, 'MS', line_num, prefix))

        # PAR-XX-AUTO or id: AUTO-XX (for parameters)
        if 'parameter-registry' in filename:
            match = re.search(r'id:\s*(?:PAR-)?AUTO-([A-Z]{2,4})\b', line, re.IGNORECASE)
            if match:
                prefix = match.group(1).upper()
                results.append((line, 'PAR', line_num, prefix))
            elif re.search(r'id:\s*AUTO\b', line, re.IGNORECASE):
                # AUTO without prefix - need to infer from context
                results.append((line, 'PAR', line_num, 'UNKNOWN'))

    return results


def replace_auto_ids(filepath: Path, dry_run: bool = True) -> List[str]:
    """
    Replace AUTO IDs with real IDs in a file.

    Returns: List of changes made
    """
    if not filepath.exists():
        return []

    content = filepath.read_text()
    filename = filepath.name
    changes = []

    auto_ids = find_auto_ids(content, filename)

    if not auto_ids:
        return []

    # Group by type to get sequential IDs
    new_content = content

    for original_line, id_type, line_num, prefix in auto_ids:
        # Get next available ID
        if id_type == 'CAS':
            registry = CaseRegistry()
            new_id = registry.next_id()
            pattern = r'id:\s*AUTO\b'
            replacement = f'id: {new_id}'

        elif id_type == 'CAT':
            registry = TheoryCategoryRegistry()
            new_id = registry.next_id()
            pattern = r'id:\s*CAT-AUTO\b'
            replacement = f'id: {new_id}'

        elif id_type == 'MS':
            if prefix and prefix != 'UNKNOWN':
                registry = TheoryModelRegistry()
                new_id = registry.next_id(prefix)
                pattern = rf'id:\s*(?:MS-)?AUTO-{prefix}\b'
                replacement = f'id: {new_id}'
            else:
                changes.append(f"  Line {line_num}: MS requires prefix (use AUTO-CM, AUTO-SP, etc.)")
                continue

        elif id_type == 'PAR':
            if prefix and prefix != 'UNKNOWN':
                registry = ParameterRegistry()
                new_id = registry.next_id(prefix)
                pattern = rf'id:\s*(?:PAR-)?AUTO-{prefix}\b'
                replacement = f'id: {new_id}'
            else:
                changes.append(f"  Line {line_num}: PAR requires prefix (use AUTO-BEH, AUTO-CM, etc.)")
                continue

        # Apply replacement
        new_line = re.sub(pattern, replacement, original_line, flags=re.IGNORECASE)
        new_content = new_content.replace(original_line, new_line, 1)
        changes.append(f"  Line {line_num}: {id_type}-AUTO → {new_id}")

    # Write if not dry run
    if not dry_run and changes:
        filepath.write_text(new_content)

    return changes


def scan_all_registries(dry_run: bool = True) -> dict:
    """Scan all registry files for AUTO IDs."""
    results = {}

    for filename in REGISTRY_FILES.keys():
        filepath = REPO_ROOT / 'data' / filename
        if filepath.exists():
            changes = replace_auto_ids(filepath, dry_run)
            if changes:
                results[filename] = changes

    return results


def main():
    parser = argparse.ArgumentParser(
        description='Auto-assign registry IDs (replaces AUTO placeholders)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Preview changes (dry-run)
  python scripts/auto_assign_ids.py

  # Apply changes
  python scripts/auto_assign_ids.py --apply

  # Process specific file
  python scripts/auto_assign_ids.py --file data/case-registry.yaml --apply

Supported AUTO patterns:
  - id: AUTO           → CAS-XXX (in case-registry.yaml)
  - id: CAT-AUTO       → CAT-XX (in theory-catalog.yaml)
  - id: AUTO-CM        → MS-CM-XXX (in theory-catalog.yaml)
  - id: AUTO-BEH       → PAR-BEH-XXX (in parameter-registry.yaml)
        """
    )

    parser.add_argument('--apply', action='store_true',
                        help='Actually apply changes (default is dry-run)')
    parser.add_argument('--file', type=Path,
                        help='Process specific file only')
    parser.add_argument('--quiet', action='store_true',
                        help='Only output if changes found')

    args = parser.parse_args()
    dry_run = not args.apply

    if args.file:
        # Process single file
        if not args.file.exists():
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            return 1

        changes = replace_auto_ids(args.file, dry_run)
        if changes:
            mode = "Would assign" if dry_run else "Assigned"
            print(f"{args.file.name}:")
            for change in changes:
                print(change)
            if dry_run:
                print(f"\nRun with --apply to make changes")
        elif not args.quiet:
            print(f"No AUTO IDs found in {args.file.name}")
    else:
        # Scan all registries
        results = scan_all_registries(dry_run)

        if results:
            mode = "DRY-RUN (preview)" if dry_run else "APPLIED"
            print(f"=== AUTO ID Assignment ({mode}) ===\n")

            for filename, changes in results.items():
                print(f"{filename}:")
                for change in changes:
                    print(change)
                print()

            if dry_run:
                print("Run with --apply to make changes")
            else:
                print("✅ All AUTO IDs assigned")
        elif not args.quiet:
            print("✅ No AUTO IDs found in any registry")

    return 0


if __name__ == '__main__':
    sys.exit(main())
