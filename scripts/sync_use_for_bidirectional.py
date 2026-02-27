#!/usr/bin/env python3
"""
Bidirectional use_for synchronization between bcm_master.bib and Paper-YAMLs.

Runs both sync directions in sequence:
1. BibTeX → YAML: Ensures YAML files have all BibTeX use_for tags
2. YAML → BibTeX: Ensures BibTeX has all YAML use_for tags

Usage:
    python scripts/sync_use_for_bidirectional.py [--dry-run] [--only-core]
    python scripts/sync_use_for_bidirectional.py --status
"""

import subprocess
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def run_sync(script_name, extra_args=None):
    """Run a sync script and capture output."""
    cmd = [sys.executable, os.path.join(SCRIPT_DIR, script_name)]
    if extra_args:
        cmd.extend(extra_args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout, result.returncode


def main():
    args = sys.argv[1:]
    dry_run = '--dry-run' in args
    status_only = '--status' in args

    if status_only:
        args = ['--dry-run']

    # Direction 1: BibTeX → YAML
    print("=" * 60)
    print("  DIRECTION 1: BibTeX → YAML")
    print("=" * 60)
    out1, _ = run_sync('sync_bib_use_for_to_yaml.py', args)

    # Extract updated count
    for line in out1.split('\n'):
        if 'Updated:' in line or 'Tags added:' in line or 'Already in sync:' in line:
            print(f"  {line.strip()}")

    # Direction 2: YAML → BibTeX
    print()
    print("=" * 60)
    print("  DIRECTION 2: YAML → BibTeX")
    print("=" * 60)
    out2, _ = run_sync('sync_yaml_use_for_to_bib.py', args)

    for line in out2.split('\n'):
        if 'Updated:' in line or 'Tags added:' in line or 'Already in sync:' in line:
            print(f"  {line.strip()}")

    # Summary
    print()
    print("=" * 60)
    if status_only:
        print("  STATUS CHECK COMPLETE")
    elif dry_run:
        print("  DRY RUN COMPLETE")
    else:
        print("  BIDIRECTIONAL SYNC COMPLETE")
    print("=" * 60)


if __name__ == '__main__':
    main()
