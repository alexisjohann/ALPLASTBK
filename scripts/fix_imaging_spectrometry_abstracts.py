#!/usr/bin/env python3
"""
Fix Imaging Spectrometry Abstract Contamination
================================================
Removes the incorrect imaging spectrometry abstract from all YAML files
where it was incorrectly inserted. Replaces with null/empty.

The contaminated abstract starts with:
"Imaging spectrometry has mainly been a research tool..."

This is NOT a real abstract for any behavioral economics paper.
"""

import os
import yaml
from pathlib import Path

YAML_DIR = Path("data/paper-references")
CONTAMINATION_MARKER = "Imaging spectrometry has mainly been a research tool"

def fix_contaminated_files():
    """Find and fix all YAML files with the wrong abstract."""
    fixed = []
    skipped = []

    for yaml_path in sorted(YAML_DIR.glob("PAP-*.yaml")):
        with open(yaml_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if CONTAMINATION_MARKER not in content:
            continue

        # Parse YAML
        try:
            data = yaml.safe_load(content)
        except yaml.YAMLError as e:
            print(f"  YAML ERROR: {yaml_path.name}: {e}")
            skipped.append(yaml_path.name)
            continue

        if not data:
            skipped.append(yaml_path.name)
            continue

        # Check if abstract is contaminated
        abstract = data.get('abstract', '')
        if not abstract or CONTAMINATION_MARKER not in str(abstract):
            # Might be in summary.abstract_extended
            summary = data.get('summary', {})
            if summary and CONTAMINATION_MARKER in str(summary.get('abstract_extended', '')):
                summary['abstract_extended'] = None
                data['summary'] = summary
            else:
                skipped.append(yaml_path.name)
                continue
        else:
            # Remove contaminated abstract
            data['abstract'] = None
            data['abstract_source'] = 'contamination_removed'
            data['abstract_fetched'] = '2026-02-07'

        # Write back
        with open(yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

        fixed.append(yaml_path.name)
        print(f"  FIXED: {yaml_path.name}")

    return fixed, skipped

def main():
    print("=" * 60)
    print("FIX IMAGING SPECTROMETRY ABSTRACT CONTAMINATION")
    print("=" * 60)
    print()

    fixed, skipped = fix_contaminated_files()

    print()
    print(f"SUMMARY:")
    print(f"  Fixed:   {len(fixed)} files")
    print(f"  Skipped: {len(skipped)} files")
    print()

    if fixed:
        print("Fixed files:")
        for f in fixed:
            print(f"  - {f}")

if __name__ == "__main__":
    main()
