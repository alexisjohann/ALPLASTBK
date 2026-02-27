#!/usr/bin/env python3
"""
Cleanup orphan PAP-*.yaml files (YAML without BIB entry).

Strategy:
1. For orphans WITH EBF data: merge into target YAML, then delete
2. For orphans WITHOUT EBF data: just delete

Usage:
  python scripts/cleanup_orphan_yamls.py --analyze          # Show plan
  python scripts/cleanup_orphan_yamls.py --batch N          # Process N orphans
  python scripts/cleanup_orphan_yamls.py --all              # Process all
  python scripts/cleanup_orphan_yamls.py --all --apply      # Actually apply
"""

import os
import re
import sys
import yaml
import shutil
import argparse

BIB_FILE = "bibliography/bcm_master.bib"
REFS_DIR = "data/paper-references"

# EBF fields that contain valuable data worth merging
EBF_FIELDS = [
    'key_findings_structured', 'behavioral_mapping',
    'parameter_contributions', 'citations', 'linked_cases',
    'use_for', 'theory_support', 'evidence_tier',
]

# Manual target mappings for the 8 orphans that couldn't auto-resolve
MANUAL_TARGETS = {
    'PAP-akerlof2000economics': 'PAP-akerlof2000identity',
    'PAP-becker1988': 'PAP-BeckerMurphy1988',
    'PAP-fehr1997reciprocal': 'PAP-fehr1997origins',
    'PAP-fehr2002indirect': 'PAP-fehr2002enforcement',
    'PAP-gigerenzer2007helping': 'PAP-gigerenzer2007gut',
    'PAP-kahneman1992advances': 'PAP-kahneman1992problem',
    'PAP-kahneman1992certainty': 'PAP-kahneman1992problem',
    'PAP-tversky1973psychology': 'PAP-tversky1973availability',
}


def normalize_bib_key(key):
    """Ensure PAP- prefix (same logic as check_paper_consistency.py)."""
    if not key.startswith('PAP-'):
        return f"PAP-{key}"
    return key


def normalize_title(t):
    """Normalize title for comparison."""
    t = re.sub(r'[^\w\s]', '', t.lower())
    return re.sub(r'\s+', ' ', t).strip()


def load_bib_keys():
    """Load all BIB keys as PAP-normalized set."""
    keys = set()
    with open(BIB_FILE, 'r') as f:
        for line in f:
            m = re.match(r'^@\w+\{([^,]+),', line)
            if m:
                keys.add(normalize_bib_key(m.group(1).strip()))
    return keys


def load_yaml_keys():
    """Load all YAML keys."""
    keys = set()
    for fname in os.listdir(REFS_DIR):
        if fname.startswith('PAP-') and fname.endswith('.yaml'):
            keys.add(fname.replace('.yaml', ''))
    return keys


def build_title_index():
    """Build normalized_title → PAP-key mapping from BIB."""
    index = {}
    with open(BIB_FILE, 'r') as f:
        bib_content = f.read()

    for match in re.finditer(
        r'^@\w+\{([^,]+),\s*\n(.*?)^\}',
        bib_content, re.MULTILINE | re.DOTALL
    ):
        raw = match.group(1).strip()
        body = match.group(2)
        tm = re.search(r'title\s*=\s*\{([^}]*)\}', body)
        if tm:
            title = tm.group(1).strip()
            norm = normalize_title(title)
            if norm and norm != 'title to be added':
                index[norm] = normalize_bib_key(raw)
    return index


def find_target(orphan_key, yaml_data, bib_keys, title_index):
    """Find the target PAP-key for an orphan YAML."""
    # Check manual targets first
    if orphan_key in MANUAL_TARGETS:
        return MANUAL_TARGETS[orphan_key]

    title = yaml_data.get('title', '') if yaml_data else ''

    # 1. Title match
    if title:
        norm = normalize_title(title)
        if norm and norm != 'title to be added' and norm in title_index:
            return title_index[norm]

    # 2. [Title for xxx] reference
    if title:
        ref_m = re.search(r'\[Title for ([^\]]+)\]', title)
        if ref_m:
            ref_key = ref_m.group(1).strip()
            pap_ref = normalize_bib_key(ref_key)
            if pap_ref in bib_keys:
                return pap_ref
            # Try stripping extra PAP-
            clean = ref_key.replace('PAP-', '')
            pap_clean = normalize_bib_key(clean)
            if pap_clean in bib_keys:
                return pap_clean

    return None


def merge_ebf_data(orphan_data, target_path):
    """Merge EBF fields from orphan into target YAML. Returns list of merged fields."""
    if not os.path.exists(target_path):
        return []

    try:
        with open(target_path, 'r') as f:
            target_data = yaml.safe_load(f) or {}
    except yaml.YAMLError as e:
        print(f"  WARNING: Cannot parse {target_path}: {e}")
        return []

    merged = []
    for field in EBF_FIELDS:
        if field in orphan_data and field not in target_data:
            target_data[field] = orphan_data[field]
            merged.append(field)

    if merged:
        with open(target_path, 'w') as f:
            yaml.dump(target_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    return merged


def main():
    parser = argparse.ArgumentParser(description='Cleanup orphan PAP-*.yaml files')
    parser.add_argument('--analyze', action='store_true', help='Show cleanup plan')
    parser.add_argument('--batch', type=int, default=0, help='Process N orphans')
    parser.add_argument('--all', action='store_true', help='Process all orphans')
    parser.add_argument('--apply', action='store_true', help='Actually apply changes')
    args = parser.parse_args()

    bib_keys = load_bib_keys()
    yaml_keys = load_yaml_keys()
    title_index = build_title_index()

    orphans = sorted(yaml_keys - bib_keys)
    print(f"Total orphan YAMLs: {len(orphans)}")

    # Classify orphans
    plan = []  # (orphan_key, action, target, ebf_fields)
    for orphan in orphans:
        yaml_path = os.path.join(REFS_DIR, f"{orphan}.yaml")
        try:
            with open(yaml_path, 'r') as f:
                data = yaml.safe_load(f)
        except Exception:
            plan.append((orphan, 'DELETE', None, []))
            continue

        if not data:
            plan.append((orphan, 'DELETE', None, []))
            continue

        ebf_fields = [f for f in EBF_FIELDS if f in data]
        target = find_target(orphan, data, bib_keys, title_index)

        if ebf_fields and target:
            plan.append((orphan, 'MERGE+DELETE', target, ebf_fields))
        elif ebf_fields and not target:
            plan.append((orphan, 'KEEP_REVIEW', None, ebf_fields))
        else:
            plan.append((orphan, 'DELETE', target, []))

    # Analyze
    merges = [p for p in plan if p[1] == 'MERGE+DELETE']
    deletes = [p for p in plan if p[1] == 'DELETE']
    keeps = [p for p in plan if p[1] == 'KEEP_REVIEW']

    if args.analyze or (not args.batch and not args.all):
        print(f"\n=== CLEANUP PLAN ===")
        print(f"  MERGE+DELETE (EBF data → target): {len(merges)}")
        print(f"  DELETE (no EBF data):              {len(deletes)}")
        print(f"  KEEP for review:                   {len(keeps)}")
        print()

        if merges:
            print("--- MERGE+DELETE ---")
            for orphan, action, target, fields in merges[:10]:
                print(f"  {orphan} → {target}")
                print(f"    EBF fields: {fields}")
            if len(merges) > 10:
                print(f"  ... and {len(merges) - 10} more")
            print()

        if keeps:
            print("--- KEEP for review ---")
            for orphan, action, target, fields in keeps:
                print(f"  {orphan} ({fields})")
        return

    # Process
    to_process = plan
    if args.batch:
        to_process = plan[:args.batch]

    dry_run = not args.apply
    mode = "DRY RUN" if dry_run else "APPLYING"
    print(f"\n=== {mode}: Processing {len(to_process)} orphans ===\n")

    deleted = 0
    merged = 0
    kept = 0
    merge_field_count = 0

    for orphan, action, target, ebf_fields in to_process:
        yaml_path = os.path.join(REFS_DIR, f"{orphan}.yaml")

        if action == 'KEEP_REVIEW':
            print(f"  SKIP: {orphan} (needs manual review)")
            kept += 1
            continue

        if action == 'MERGE+DELETE' and target:
            target_path = os.path.join(REFS_DIR, f"{target}.yaml")
            if not dry_run:
                # Load orphan data
                with open(yaml_path, 'r') as f:
                    orphan_data = yaml.safe_load(f) or {}
                # Merge EBF fields
                merged_fields = merge_ebf_data(orphan_data, target_path)
                if merged_fields:
                    merge_field_count += len(merged_fields)
                    print(f"  MERGED: {orphan} → {target} ({merged_fields})")
                # Delete orphan
                os.remove(yaml_path)
                print(f"  DELETED: {orphan}")
            else:
                print(f"  WOULD MERGE: {orphan} → {target} ({ebf_fields})")
                print(f"  WOULD DELETE: {orphan}")
            merged += 1

        elif action == 'DELETE':
            if not dry_run:
                os.remove(yaml_path)
                print(f"  DELETED: {orphan}")
            else:
                print(f"  WOULD DELETE: {orphan}")
            deleted += 1

    print(f"\n=== {'APPLIED' if not dry_run else 'DRY RUN'} SUMMARY ===")
    print(f"  Merged + deleted: {merged}")
    print(f"  Deleted (no EBF): {deleted}")
    print(f"  Kept for review:  {kept}")
    if not dry_run:
        print(f"  EBF fields merged: {merge_field_count}")
    else:
        print(f"\nRun with --apply to execute changes")


if __name__ == '__main__':
    main()
