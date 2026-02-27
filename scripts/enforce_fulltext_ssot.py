#!/usr/bin/env python3
"""
enforce_fulltext_ssot.py - Enforce Full-Text SSOT Location

SSOT (Single Source of Truth) for paper full-texts:
  data/paper-texts/PAP-{key}.md

This script:
1. Migrates full-texts from legacy locations to SSOT
2. Updates Paper-YAML with correct full_text paths
3. Validates that no full-texts exist outside SSOT
4. Can be run as pre-commit hook to enforce SSOT

WORKFLOW GAP FIX:
  Prevents full-texts from being stored in wrong locations.
  Ensures Paper-YAML full_text.path always points to SSOT.

Usage:
    python scripts/enforce_fulltext_ssot.py --check
    python scripts/enforce_fulltext_ssot.py --migrate
    python scripts/enforce_fulltext_ssot.py --fix-yaml

Author: EBF Framework Team
Version: 1.0.0
Date: 2026-02-05
"""

import argparse
import os
import re
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Tuple
import yaml

# Paths
REPO_ROOT = Path(__file__).parent.parent
SSOT_PATH = REPO_ROOT / "data" / "paper-texts"
PAPER_REFS_PATH = REPO_ROOT / "data" / "paper-references"

# Legacy locations to check
LEGACY_LOCATIONS = [
    REPO_ROOT / "papers" / "evaluated" / "integrated",
    REPO_ROOT / "papers" / "evaluated",
    REPO_ROOT / "papers" / "full-texts",
    REPO_ROOT / "papers",
]


def find_legacy_fulltexts() -> List[Dict]:
    """Find full-texts in legacy locations."""
    legacy_files = []

    for legacy_path in LEGACY_LOCATIONS:
        if not legacy_path.exists():
            continue

        for ext in ['*.txt', '*.md', '*.tex']:
            for file in legacy_path.glob(ext):
                # Check if it's a paper full-text (starts with PAP-)
                if file.stem.startswith('PAP-') or 'PAP-' in file.name:
                    paper_key = file.stem
                    if not paper_key.startswith('PAP-'):
                        # Try to extract PAP-key
                        match = re.search(r'(PAP-[\w]+)', file.name)
                        if match:
                            paper_key = match.group(1)

                    ssot_file = SSOT_PATH / f"{paper_key}.md"

                    legacy_files.append({
                        "legacy_path": file,
                        "paper_key": paper_key,
                        "ssot_path": ssot_file,
                        "ssot_exists": ssot_file.exists(),
                        "size": file.stat().st_size
                    })

    return legacy_files


def migrate_to_ssot(legacy_info: Dict, dry_run: bool = True) -> bool:
    """Migrate a full-text file to SSOT location."""
    legacy_path = legacy_info["legacy_path"]
    ssot_path = legacy_info["ssot_path"]

    if legacy_info["ssot_exists"]:
        # Compare sizes
        ssot_size = ssot_path.stat().st_size
        legacy_size = legacy_info["size"]

        if legacy_size > ssot_size:
            print(f"  ⚠️  SSOT exists but legacy is larger ({legacy_size} vs {ssot_size} bytes)")
            if not dry_run:
                # Backup SSOT and copy legacy
                backup_path = ssot_path.with_suffix('.md.bak')
                shutil.copy(ssot_path, backup_path)
                shutil.copy(legacy_path, ssot_path)
                print(f"  ✅ Updated SSOT from larger legacy file")
        else:
            print(f"  ✓ SSOT already exists and is larger/equal")
        return True

    # Create SSOT directory if needed
    SSOT_PATH.mkdir(parents=True, exist_ok=True)

    if dry_run:
        print(f"  [DRY RUN] Would copy: {legacy_path}")
        print(f"            To:         {ssot_path}")
        return True

    # Copy to SSOT (convert to .md)
    if legacy_path.suffix == '.txt':
        # Read and write as markdown
        with open(legacy_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Add markdown header
        paper_key = legacy_info["paper_key"]
        md_content = f"# {paper_key}\n\n{content}"

        with open(ssot_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
    else:
        shutil.copy(legacy_path, ssot_path)

    print(f"  ✅ Migrated to SSOT: {ssot_path.name}")
    return True


def fix_paper_yaml_paths() -> List[Dict]:
    """Fix Paper-YAML full_text paths to point to SSOT."""
    fixes = []

    for yaml_file in PAPER_REFS_PATH.glob("PAP-*.yaml"):
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        except Exception as e:
            print(f"  ⚠️  Error reading {yaml_file}: {e}")
            continue

        if not data:
            continue

        paper_key = yaml_file.stem
        ssot_path = SSOT_PATH / f"{paper_key}.md"
        ssot_exists = ssot_path.exists()

        # Get current full_text settings
        full_text = data.get('full_text', {})
        current_available = full_text.get('available', False)
        current_path = full_text.get('path')

        expected_path = f"data/paper-texts/{paper_key}.md"

        needs_fix = False
        fix_details = {"yaml_file": yaml_file, "paper_key": paper_key, "changes": []}

        # Check if available flag is wrong
        if ssot_exists and not current_available:
            fix_details["changes"].append({
                "field": "full_text.available",
                "old": False,
                "new": True
            })
            needs_fix = True

        if not ssot_exists and current_available:
            fix_details["changes"].append({
                "field": "full_text.available",
                "old": True,
                "new": False
            })
            needs_fix = True

        # Check if path is wrong
        if ssot_exists and current_path != expected_path:
            fix_details["changes"].append({
                "field": "full_text.path",
                "old": current_path,
                "new": expected_path
            })
            needs_fix = True

        if needs_fix:
            fixes.append(fix_details)

    return fixes


def apply_yaml_fixes(fixes: List[Dict], dry_run: bool = True) -> int:
    """Apply fixes to Paper-YAML files."""
    fixed_count = 0

    for fix in fixes:
        yaml_file = fix["yaml_file"]
        paper_key = fix["paper_key"]

        print(f"\n  📝 {paper_key}")

        with open(yaml_file, 'r', encoding='utf-8') as f:
            content = f.read()
            data = yaml.safe_load(content)

        if not data:
            continue

        # Ensure full_text section exists
        if 'full_text' not in data:
            data['full_text'] = {}

        for change in fix["changes"]:
            field = change["field"]
            new_value = change["new"]

            print(f"     {field}: {change['old']} → {new_value}")

            if field == "full_text.available":
                data['full_text']['available'] = new_value
            elif field == "full_text.path":
                data['full_text']['path'] = new_value

        if not dry_run:
            with open(yaml_file, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
            print(f"     ✅ Updated")
            fixed_count += 1
        else:
            print(f"     [DRY RUN] Would update")

    return fixed_count


def check_ssot_compliance() -> Dict:
    """Check overall SSOT compliance."""
    results = {
        "ssot_files": 0,
        "legacy_files": 0,
        "yaml_with_wrong_path": 0,
        "yaml_with_missing_flag": 0,
        "compliant": True
    }

    # Count SSOT files
    if SSOT_PATH.exists():
        results["ssot_files"] = len(list(SSOT_PATH.glob("PAP-*.md")))

    # Find legacy files
    legacy = find_legacy_fulltexts()
    results["legacy_files"] = len([l for l in legacy if not l["ssot_exists"]])

    # Check YAML files
    fixes = fix_paper_yaml_paths()
    results["yaml_with_wrong_path"] = len([f for f in fixes
        if any(c["field"] == "full_text.path" for c in f["changes"])])
    results["yaml_with_missing_flag"] = len([f for f in fixes
        if any(c["field"] == "full_text.available" for c in f["changes"])])

    results["compliant"] = (
        results["legacy_files"] == 0 and
        results["yaml_with_wrong_path"] == 0 and
        results["yaml_with_missing_flag"] == 0
    )

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Enforce Full-Text SSOT Location"
    )
    parser.add_argument("--check", action="store_true", help="Check compliance")
    parser.add_argument("--migrate", action="store_true", help="Migrate legacy files to SSOT")
    parser.add_argument("--fix-yaml", action="store_true", help="Fix Paper-YAML full_text paths")
    parser.add_argument("--dry-run", action="store_true", help="Don't make changes")
    parser.add_argument("--all", action="store_true", help="Run all fixes")

    args = parser.parse_args()

    if not any([args.check, args.migrate, args.fix_yaml, args.all]):
        args.check = True  # Default to check

    print(f"\n{'='*60}")
    print(f"  FULL-TEXT SSOT ENFORCEMENT")
    print(f"  SSOT: {SSOT_PATH}")
    print(f"{'='*60}\n")

    exit_code = 0

    if args.check or args.all:
        print("📊 Checking SSOT Compliance...\n")
        results = check_ssot_compliance()

        print(f"  SSOT Files:              {results['ssot_files']}")
        print(f"  Legacy Files (not migrated): {results['legacy_files']}")
        print(f"  YAML with wrong path:    {results['yaml_with_wrong_path']}")
        print(f"  YAML with wrong flag:    {results['yaml_with_missing_flag']}")
        print()

        if results["compliant"]:
            print("  ✅ SSOT COMPLIANT")
        else:
            print("  ❌ NOT COMPLIANT - Run with --all to fix")
            exit_code = 1
        print()

    if args.migrate or args.all:
        print("📁 Migrating Legacy Files...\n")
        legacy = find_legacy_fulltexts()

        if not legacy:
            print("  ✓ No legacy files found")
        else:
            for item in legacy:
                print(f"\n  {item['paper_key']}")
                print(f"    Legacy: {item['legacy_path']}")
                migrate_to_ssot(item, dry_run=args.dry_run)

        print()

    if args.fix_yaml or args.all:
        print("📝 Fixing Paper-YAML Paths...\n")
        fixes = fix_paper_yaml_paths()

        if not fixes:
            print("  ✓ All Paper-YAML files have correct full_text paths")
        else:
            fixed = apply_yaml_fixes(fixes, dry_run=args.dry_run)
            if not args.dry_run:
                print(f"\n  Fixed {fixed} files")

        print()

    print(f"{'='*60}\n")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
