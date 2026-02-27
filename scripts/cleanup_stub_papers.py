#!/usr/bin/env python3
# ┌─────────────────────────────────────────────────────────────────────────┐
# │  ⚠️  DEPRECATED (2026-02-08)                                            │
# │                                                                         │
# │  Einmalige Stub-Paper-Bereinigung                                      │
# │  Kept for reference only.                                              │
# │                                                                         │
# │  SSOT: data/paper-references/PAP-*.yaml + bibliography/bcm_master.bib │
# │  Neue Papers: /integrate-paper Workflow                                │
# └─────────────────────────────────────────────────────────────────────────┘
"""

⚠️  DEPRECATED (2026-02-08) — See header for details.
Batch cleanup of orphaned stub papers (Title to be added) that have proper counterparts.

This script:
1. Identifies all BibTeX stubs with "Title to be added"
2. Checks which have counterparts (same prefix + extended key)
3. Deletes: YAML files, BibTeX entries, and references in data files
"""

import re
import os
import sys
import glob

REPO = "/home/user/complementarity-context-framework"
BIB_FILE = os.path.join(REPO, "bibliography/bcm_master.bib")
YAML_DIR = os.path.join(REPO, "data/paper-references")

DATA_FILES_TO_CLEAN = [
    os.path.join(REPO, "data/paper-calibration/triage-results.yaml"),
    os.path.join(REPO, "data/paper-calibration/learning-log.yaml"),
    os.path.join(REPO, "data/paper-level-classification.yaml"),
    os.path.join(REPO, "data/paper-sources.yaml"),
    os.path.join(REPO, "data/doi_strategy_export.csv"),
]


def find_all_bib_keys(bib_content):
    """Extract all BibTeX keys."""
    return re.findall(r'@\w+\{([^,]+),', bib_content)


def find_stub_keys(bib_content):
    """Find keys with 'Title to be added'."""
    stubs = []
    entries = re.split(r'\n(?=@)', bib_content)
    for entry in entries:
        if 'Title to be added' in entry:
            m = re.match(r'@\w+\{([^,]+),', entry)
            if m:
                stubs.append(m.group(1))
    return stubs


def has_counterpart(stub_key, all_keys):
    """Check if a proper entry exists with the same prefix."""
    for key in all_keys:
        if key != stub_key and key.startswith(stub_key) and len(key) > len(stub_key):
            return True
    return False


def remove_bib_entry(bib_content, key):
    """Remove a single BibTeX entry by key."""
    pattern = rf'@\w+\{{{re.escape(key)},.*?\n\}}\n?'
    return re.sub(pattern, '', bib_content, count=1, flags=re.DOTALL)


def remove_from_triage(content, key):
    """Remove triage-results entry."""
    pattern = rf'- paper_key: {re.escape(key)}\n(?:  [^\n]+\n)*'
    return re.sub(pattern, '', content)


def remove_from_learning_log(content, key):
    """Remove from learning-log."""
    content = re.sub(rf'  - PAP-{re.escape(key)}\n', '', content)
    return content


def remove_from_classification(content, key):
    """Remove from paper-level-classification."""
    pattern = rf'  {re.escape(key)}:\n(?:    [^\n]+\n)*'
    return re.sub(pattern, '', content)


def remove_from_sources(content, key):
    """Remove from paper-sources."""
    pattern = rf'- id: {re.escape(key)}\n(?:  [^\n]+\n)*(?:\n(?:  [^\n]+\n)*)*'
    return re.sub(pattern, '', content)


def remove_from_csv(content, key):
    """Remove from CSV."""
    return re.sub(rf'{re.escape(key)},[^\n]*\n', '', content)


def main():
    dry_run = "--dry-run" in sys.argv

    with open(BIB_FILE, 'r') as f:
        bib_content = f.read()

    all_keys = find_all_bib_keys(bib_content)
    stub_keys = find_stub_keys(bib_content)

    # Filter to only those WITH counterparts
    safe_to_delete = [k for k in stub_keys if has_counterpart(k, all_keys)]
    no_counterpart = [k for k in stub_keys if not has_counterpart(k, all_keys)]

    print(f"Total stubs: {len(stub_keys)}")
    print(f"With counterpart (SAFE TO DELETE): {len(safe_to_delete)}")
    print(f"No counterpart (KEEP): {len(no_counterpart)}")
    print()

    if dry_run:
        print("=== DRY RUN - No changes made ===")
        print(f"\nWould delete {len(safe_to_delete)} stubs:")
        for k in sorted(safe_to_delete):
            counterparts = [x for x in all_keys if x != k and x.startswith(k)]
            print(f"  {k} -> counterparts: {', '.join(counterparts[:3])}")
        print(f"\nWould keep {len(no_counterpart)} stubs (no counterpart):")
        for k in sorted(no_counterpart):
            print(f"  {k}")
        return

    # === STEP 1: Delete YAML files ===
    yaml_deleted = 0
    for key in safe_to_delete:
        yaml_path = os.path.join(YAML_DIR, f"PAP-{key}.yaml")
        if os.path.exists(yaml_path):
            os.remove(yaml_path)
            yaml_deleted += 1

    print(f"[1/3] Deleted {yaml_deleted} YAML files")

    # === STEP 2: Remove BibTeX entries ===
    for key in safe_to_delete:
        bib_content = remove_bib_entry(bib_content, key)

    with open(BIB_FILE, 'w') as f:
        f.write(bib_content)

    print(f"[2/3] Removed {len(safe_to_delete)} BibTeX entries")

    # === STEP 3: Clean data files ===
    cleaners = {
        "triage-results.yaml": remove_from_triage,
        "learning-log.yaml": remove_from_learning_log,
        "paper-level-classification.yaml": remove_from_classification,
        "paper-sources.yaml": remove_from_sources,
        "doi_strategy_export.csv": remove_from_csv,
    }

    data_cleaned = 0
    for filepath in DATA_FILES_TO_CLEAN:
        basename = os.path.basename(filepath)
        if not os.path.exists(filepath):
            continue
        with open(filepath, 'r') as f:
            content = f.read()
        original_len = len(content)
        cleaner = cleaners.get(basename)
        if cleaner:
            for key in safe_to_delete:
                content = cleaner(content, key)
        if len(content) != original_len:
            with open(filepath, 'w') as f:
                f.write(content)
            data_cleaned += 1
            print(f"  Cleaned: {basename} (-{original_len - len(content)} chars)")

    print(f"[3/3] Cleaned {data_cleaned} data files")
    print(f"\n=== DONE: Removed {len(safe_to_delete)} orphaned stubs ===")


if __name__ == "__main__":
    main()
