#!/usr/bin/env python3
# ┌─────────────────────────────────────────────────────────────────────────┐
# │  ⚠️  DEPRECATED (2026-02-08)                                            │
# │                                                                         │
# │  Einmalige Migration paper-sources.yaml zu PAP-*.yaml (TL-001)         │
# │  Kept for reference only.                                              │
# │                                                                         │
# │  SSOT: data/paper-references/PAP-*.yaml + bibliography/bcm_master.bib │
# │  Neue Papers: /integrate-paper Workflow                                │
# └─────────────────────────────────────────────────────────────────────────┘
"""

⚠️  DEPRECATED (2026-02-08) — See header for details.
Migrate unique data from paper-sources.yaml → paper-references/PAP-*.yaml

Adds fields that only exist in paper-sources.yaml:
  - citations (int)
  - status (seminal/foundational/cited/etc)
  - key_findings (structured findings with effect_sizes)
  - behavioral_mapping (migrated from 9c_coordinates → 10C)
  - linked_cases (CAS-XXX references)

Usage:
  python scripts/migrate_paper_sources.py --dry-run              # Show what would change
  python scripts/migrate_paper_sources.py --batch 1              # 1 paper (prototype)
  python scripts/migrate_paper_sources.py --batch 10             # 10 papers
  python scripts/migrate_paper_sources.py --batch 100            # 100 papers
  python scripts/migrate_paper_sources.py --all                  # All papers
  python scripts/migrate_paper_sources.py --paper PAP-PAP-kahneman1979prospectprospect  # Specific paper
"""

import argparse
import os
import re
import sys
import yaml


SOURCES_FILE = "data/paper-sources.yaml"
REFERENCES_DIR = "data/paper-references"


def load_paper_sources_entries():
    """Parse paper-sources.yaml entries without full YAML parse (file has errors)."""
    entries = {}
    with open(SOURCES_FILE, 'r') as f:
        content = f.read()

    # Find all entry starts
    pattern = re.compile(r'^- id: (.+)$', re.MULTILINE)
    matches = list(pattern.finditer(content))

    for i, match in enumerate(matches):
        paper_id = match.group(1).strip()
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        entry_text = content[start:end]

        try:
            parsed = yaml.safe_load(entry_text)
            if isinstance(parsed, list) and len(parsed) == 1:
                entries[paper_id] = parsed[0]
        except yaml.YAMLError:
            # Skip unparseable entries
            pass

    return entries


def load_paper_reference(paper_id):
    """Load a single paper-reference YAML."""
    path = os.path.join(REFERENCES_DIR, f"{paper_id}.yaml")
    if not os.path.exists(path):
        return None, path
    with open(path, 'r') as f:
        return yaml.safe_load(f), path


def migrate_entry(source_entry, ref_data):
    """Merge unique fields from source into reference. Returns (updated_data, changes_list)."""
    changes = []
    updated = dict(ref_data)

    # 1. citations
    if 'citations' in source_entry and 'citations' not in ref_data:
        updated['citations'] = source_entry['citations']
        changes.append(f"+ citations: {source_entry['citations']}")

    # 2. status
    if 'status' in source_entry and 'status' not in ref_data:
        updated['status'] = source_entry['status']
        changes.append(f"+ status: {source_entry['status']}")

    # 3. key_findings (structured)
    if 'key_findings' in source_entry and isinstance(source_entry['key_findings'], list):
        if 'key_findings_structured' not in ref_data:
            updated['key_findings_structured'] = source_entry['key_findings']
            changes.append(f"+ key_findings_structured: {len(source_entry['key_findings'])} findings")

    # 4. behavioral_mapping (from 9c_coordinates)
    if '9c_coordinates' in source_entry and 'behavioral_mapping' not in ref_data:
        coords = source_entry['9c_coordinates']
        if isinstance(coords, list) and len(coords) > 0:
            updated['behavioral_mapping'] = {
                'source': '9c_coordinates (migrated from paper-sources.yaml)',
                'dimensions': coords
            }
            changes.append(f"+ behavioral_mapping: {len(coords)} dimensions")

    # 5. linked_cases
    if 'linked_cases' in source_entry and isinstance(source_entry['linked_cases'], list):
        if 'linked_cases' not in ref_data:
            updated['linked_cases'] = source_entry['linked_cases']
            changes.append(f"+ linked_cases: {len(source_entry['linked_cases'])} cases")

    return updated, changes


def write_paper_reference(path, data):
    """Write updated YAML back to file."""
    with open(path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False, width=120)


def main():
    parser = argparse.ArgumentParser(description="Migrate paper-sources.yaml → paper-references/")
    parser.add_argument('--dry-run', action='store_true', help="Show changes without writing")
    parser.add_argument('--batch', type=int, default=0, help="Process N papers")
    parser.add_argument('--all', action='store_true', help="Process all papers")
    parser.add_argument('--paper', type=str, help="Process specific paper ID (e.g. PAP-PAP-kahneman1979prospectprospect)")
    args = parser.parse_args()

    print("Loading paper-sources.yaml...")
    sources = load_paper_sources_entries()
    print(f"  Parsed: {len(sources)} entries")

    # Determine which papers to process
    if args.paper:
        paper_ids = [args.paper]
    elif args.all:
        paper_ids = list(sources.keys())
    elif args.batch > 0:
        paper_ids = list(sources.keys())[:args.batch]
    else:
        print("Specify --batch N, --all, or --paper PAP-xxx")
        sys.exit(1)

    # Process
    migrated = 0
    skipped = 0
    no_ref = 0
    errors = 0

    for paper_id in paper_ids:
        source_entry = sources.get(paper_id)
        if not source_entry:
            continue

        # Normalize ID: add PAP- prefix if missing
        ref_id = paper_id if paper_id.startswith('PAP-') else f"PAP-{paper_id}"
        ref_data, ref_path = load_paper_reference(ref_id)

        if ref_data is None:
            no_ref += 1
            continue

        try:
            updated, changes = migrate_entry(source_entry, ref_data)
        except Exception as e:
            errors += 1
            print(f"  ERROR {paper_id}: {e}")
            continue

        if not changes:
            skipped += 1
            continue

        migrated += 1
        print(f"\n  {paper_id}:")
        for c in changes:
            print(f"    {c}")

        if not args.dry_run:
            write_paper_reference(ref_path, updated)

    # Summary
    print(f"\n{'DRY RUN - ' if args.dry_run else ''}SUMMARY:")
    print(f"  Processed:  {len(paper_ids)}")
    print(f"  Migrated:   {migrated}")
    print(f"  Skipped:    {skipped} (no new data)")
    print(f"  No ref:     {no_ref} (no matching paper-reference)")
    print(f"  Errors:     {errors}")


if __name__ == '__main__':
    main()
