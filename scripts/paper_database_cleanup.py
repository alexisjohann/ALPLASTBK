#!/usr/bin/env python3
"""
paper_database_cleanup.py - Comprehensive paper database cleanup

Fixes all 7 issues identified in the health check:
1. Queue: Remove/remap 321 stale entries
2. L3 overclaims: Downgrade 5 papers to L2
3. Legacy fulltext paths: Migrate 5 files to SSOT
4. Integration level: Batch-compute for all YAMLs
5. theory_support gap: Auto-link where possible
6. Deprecated references: Remove migration_source from YAMLs
7. Summary report

Usage:
    python scripts/paper_database_cleanup.py --dry-run    # Preview
    python scripts/paper_database_cleanup.py --execute    # Apply all
    python scripts/paper_database_cleanup.py --execute --phase 1  # Only phase 1
"""

import re
import os
import sys
import yaml
import glob
import shutil
import argparse
from pathlib import Path
from collections import Counter, defaultdict

PROJECT_ROOT = Path(__file__).parent.parent
BIB_PATH = PROJECT_ROOT / "bibliography" / "bcm_master.bib"
YAML_DIR = PROJECT_ROOT / "data" / "paper-references"
TEXT_DIR = PROJECT_ROOT / "data" / "paper-texts"
QUEUE_PATH = PROJECT_ROOT / "data" / "paper-integration-queue.yaml"
THEORY_PATH = PROJECT_ROOT / "data" / "theory-catalog.yaml"


def load_yaml(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def save_yaml(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True,
                  sort_keys=False, width=120)


def get_all_yaml_keys():
    keys = set()
    for f in os.listdir(YAML_DIR):
        if f.startswith('PAP-') and f.endswith('.yaml'):
            keys.add(f[4:-5])
    return keys


def get_bib_data():
    """Parse BibTeX for use_for, theory_support, evidence_tier."""
    with open(BIB_PATH, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    entries = {}
    current_key = None
    current_fields = {}

    for line in content.split('\n'):
        m = re.match(r'^@\w+\{([^,]+),', line)
        if m:
            if current_key:
                entries[current_key] = current_fields
            current_key = m.group(1)
            current_fields = {}
        elif current_key and '=' in line:
            fm = re.match(r'\s*(\w+)\s*=\s*\{(.+?)\}', line)
            if fm:
                current_fields[fm.group(1)] = fm.group(2)

    if current_key:
        entries[current_key] = current_fields

    return entries


# ═══════════════════════════════════════════════════════════════════════
# PHASE 1: Queue Cleanup
# ═══════════════════════════════════════════════════════════════════════

def phase1_queue_cleanup(dry_run=True):
    print("\n" + "=" * 70)
    print("  PHASE 1: Queue Cleanup")
    print("=" * 70)

    if not QUEUE_PATH.exists():
        print("  Queue file not found. Skipping.")
        return 0

    queue_data = load_yaml(QUEUE_PATH)

    # Queue is a dict with 'pending' key
    if isinstance(queue_data, dict):
        pending = queue_data.get('pending', [])
    elif isinstance(queue_data, list):
        pending = queue_data
        queue_data = {'pending': pending}
    else:
        print("  Queue has unexpected format. Skipping.")
        return 0

    if not pending:
        print("  Queue is empty. Skipping.")
        return 0

    yaml_keys = get_all_yaml_keys()
    valid = []
    remapped = 0
    removed = 0

    for entry in pending:
        pid = entry.get('paper_id', '')
        key = pid.replace('PAP-', '')

        # Already valid?
        if key in yaml_keys:
            valid.append(entry)
            continue

        # Try to remap: find canonical key with same author+year prefix
        m = re.match(r'^([a-z]+\d{4})', key.lower())
        if m:
            prefix = m.group(1)
            candidates = [yk for yk in yaml_keys if yk.startswith(prefix)]
            if len(candidates) == 1:
                # Unambiguous match
                new_key = candidates[0]
                entry['paper_id'] = f'PAP-{new_key}'
                entry['remapped_from'] = pid
                valid.append(entry)
                remapped += 1
                continue

        # Cannot remap — remove
        removed += 1

    print(f"  Original queue:  {len(pending)} entries")
    print(f"  Valid (kept):    {len(valid) - remapped}")
    print(f"  Remapped:        {remapped}")
    print(f"  Removed (stale): {removed}")

    if not dry_run:
        queue_data['pending'] = valid
        queue_data['stats'] = {
            'total_pending': len(valid),
            'cleaned_date': '2026-02-11',
            'removed_stale': removed,
            'remapped': remapped,
        }
        save_yaml(QUEUE_PATH, queue_data)
        print("  Queue saved.")

    return remapped + removed


# ═══════════════════════════════════════════════════════════════════════
# PHASE 2: L3 Overclaim Downgrade
# ═══════════════════════════════════════════════════════════════════════

L3_OVERCLAIMS = [
    'benabou2024ends',
    'binetti2024understanding',
    'boyd2024markowitz',
    'efferson2022superadditive',
    'markowitz1952portfolio',
]


def phase2_l3_overclaims(dry_run=True):
    print("\n" + "=" * 70)
    print("  PHASE 2: L3 Overclaim Downgrade")
    print("=" * 70)

    fixes = 0
    for key in L3_OVERCLAIMS:
        yaml_path = YAML_DIR / f'PAP-{key}.yaml'
        if not yaml_path.exists():
            print(f"  SKIP: {key} (YAML not found)")
            continue

        data = load_yaml(yaml_path)
        changed = False

        # Fix top-level content_level
        if data.get('content_level') == 'L3':
            data['content_level'] = 'L2'
            changed = True
            print(f"  FIX: {key} — top-level content_level L3 → L2")

        # Also fix in full_text section if present
        ft = data.get('full_text', {})
        if ft and ft.get('content_level') == 'L3':
            ft['content_level'] = 'L2'
            ft['content_level_note'] = 'Downgraded from L3: text <5k words (summary/extract, not full original)'
            changed = True
            print(f"  FIX: {key} — full_text.content_level L3 → L2")

        # Also fix in prior_score section if present
        ps = data.get('prior_score', {})
        if ps and ps.get('content_level') == 'L3':
            ps['content_level'] = 'L2'
            ps['confidence_multiplier'] = 0.95  # L2 = 0.95, was L3 = 1.00
            changed = True
            print(f"  FIX: {key} — prior_score.content_level L3 → L2")

        if changed:
            fixes += 1
            if not dry_run:
                save_yaml(yaml_path, data)

    print(f"  Total L3 → L2 downgrades: {fixes}")
    return fixes


# ═══════════════════════════════════════════════════════════════════════
# PHASE 3: Legacy Fulltext Path Migration
# ═══════════════════════════════════════════════════════════════════════

LEGACY_PATHS = {
    'ioannidis2005most': 'papers/evaluated/integrated/Ioanidis.txt',
    'nagel1995unraveling': 'papers/evaluated/integrated/beauty contest.txt',
    'sorensen2020capabilities': 'papers/evaluated/integrated/Organizational-20Design_Parc-Model 2023-07-13 08_35_28.txt',
    'thaler2012behavioral': 'papers/evaluated/integrated/Behavioral Economics, Past, Present, Future SSRN-id2790606.txt',
    'thaler2015choice': 'papers/evaluated/integrated/Choice Architecture SSRN-id1583509.txt',
}


def phase3_legacy_paths(dry_run=True):
    print("\n" + "=" * 70)
    print("  PHASE 3: Legacy Fulltext Path Migration")
    print("=" * 70)

    fixes = 0
    for key, legacy_path in LEGACY_PATHS.items():
        yaml_path = YAML_DIR / f'PAP-{key}.yaml'
        target_path = TEXT_DIR / f'PAP-{key}.md'
        source_path = PROJECT_ROOT / legacy_path

        if not yaml_path.exists():
            print(f"  SKIP: {key} (YAML not found)")
            continue

        data = load_yaml(yaml_path)

        # Migrate text file if source exists and target doesn't
        if source_path.exists() and not target_path.exists():
            if not dry_run:
                # Read legacy .txt, write as .md
                with open(source_path, 'r', encoding='utf-8', errors='replace') as f:
                    text = f.read()
                with open(target_path, 'w', encoding='utf-8') as f:
                    f.write(f"# {data.get('title', key)}\n\n")
                    f.write(text)
                print(f"  MIGRATED: {legacy_path} → {target_path.relative_to(PROJECT_ROOT)}")
            else:
                print(f"  WOULD MIGRATE: {legacy_path} → data/paper-texts/PAP-{key}.md")

        # Update YAML path
        ft = data.get('full_text', {})
        if ft:
            old_path = ft.get('path', '')
            new_path = f'data/paper-texts/PAP-{key}.md'
            if old_path != new_path:
                ft['path'] = new_path
                ft['format'] = 'markdown'
                fixes += 1
                print(f"  FIX: {key} — path updated to SSOT")

                if not dry_run:
                    save_yaml(yaml_path, data)

    print(f"  Total path fixes: {fixes}")
    return fixes


# ═══════════════════════════════════════════════════════════════════════
# PHASE 4: Integration Level Batch-Compute
# ═══════════════════════════════════════════════════════════════════════

def compute_integration_level(key, data, bib_entry):
    """Compute integration level based on actual components present."""
    score = 0

    # I1: use_for assigned
    use_for = bib_entry.get('use_for', '')
    if use_for and use_for.strip():
        score = max(score, 1)

    # I2: + theory_support
    theory_support = bib_entry.get('theory_support', '')
    if theory_support and theory_support.strip():
        score = max(score, 2)

    # I3: + case_registry linked
    case_links = data.get('case_integration', [])
    linked_cases = data.get('linked_cases', [])
    if case_links or linked_cases:
        score = max(score, 3)

    # I4: Has dedicated appendix reference
    chapter_rel = data.get('chapter_relevance', [])
    if chapter_rel and len(chapter_rel) > 0:
        score = max(score, 4)

    # I5: Full framework integration (all components)
    has_params = bool(data.get('parameter_contributions', []))
    has_theory = bool(data.get('theory_integration', {}))
    has_case = bool(case_links or linked_cases)
    has_chapter = bool(chapter_rel)
    ft = data.get('full_text', {})
    has_fulltext = ft.get('available', False) if ft else False
    if has_params and has_theory and has_case and has_chapter and has_fulltext:
        score = max(score, 5)

    return score


def phase4_integration_levels(dry_run=True):
    print("\n" + "=" * 70)
    print("  PHASE 4: Integration Level Batch-Compute")
    print("=" * 70)

    bib_data = get_bib_data()
    yaml_keys = get_all_yaml_keys()

    level_counts = Counter()
    updates = 0

    for key in sorted(yaml_keys):
        yaml_path = YAML_DIR / f'PAP-{key}.yaml'
        try:
            data = load_yaml(yaml_path)
        except Exception:
            continue

        if not data:
            continue

        bib_entry = bib_data.get(key, {})
        computed_level = compute_integration_level(key, data, bib_entry)
        level_str = f'I{computed_level}'
        level_counts[level_str] += 1

        # Update prior_score.integration_level if different
        ps = data.get('prior_score', {})
        if ps is None:
            ps = {}
            data['prior_score'] = ps

        current = ps.get('integration_level', None)
        if current != level_str:
            ps['integration_level'] = level_str
            updates += 1

            if not dry_run:
                save_yaml(yaml_path, data)

    print(f"  Integration Level Distribution:")
    for level in sorted(level_counts.keys()):
        print(f"    {level}: {level_counts[level]:>5} papers")
    print(f"  Updates needed: {updates}")
    return updates


# ═══════════════════════════════════════════════════════════════════════
# PHASE 5: theory_support Gap Auto-Link
# ═══════════════════════════════════════════════════════════════════════

def build_keyword_theory_map():
    """Build mapping from keywords to theory IDs from theory-catalog."""
    if not THEORY_PATH.exists():
        return {}

    try:
        tc = load_yaml(THEORY_PATH)
    except Exception:
        return {}

    keyword_map = {}
    categories = tc.get('categories', [])
    for cat in categories:
        models = cat.get('models', [])
        for model in models:
            mid = model.get('id', '')
            name = model.get('name', '').lower()
            keywords = model.get('keywords', [])
            # Add model name words as keywords
            for word in re.findall(r'[a-z]{4,}', name):
                if word not in ('with', 'from', 'that', 'this', 'when', 'where',
                                'model', 'theory', 'framework', 'approach'):
                    keyword_map.setdefault(word, set()).add(mid)
            for kw in keywords:
                if isinstance(kw, str):
                    keyword_map.setdefault(kw.lower(), set()).add(mid)

    return keyword_map


def phase5_theory_support(dry_run=True):
    print("\n" + "=" * 70)
    print("  PHASE 5: theory_support Gap Analysis")
    print("=" * 70)

    bib_data = get_bib_data()
    keyword_map = build_keyword_theory_map()

    # Count current state
    has_ts = sum(1 for v in bib_data.values()
                 if v.get('theory_support', '').strip())
    no_ts = len(bib_data) - has_ts

    print(f"  Papers with theory_support:    {has_ts}")
    print(f"  Papers without theory_support: {no_ts}")

    # Auto-link: match title keywords to theory catalog
    auto_linkable = 0
    matches = defaultdict(list)

    for key, fields in bib_data.items():
        if fields.get('theory_support', '').strip():
            continue  # Already has theory_support

        title = fields.get('title', '').lower()
        title_words = set(re.findall(r'[a-z]{4,}', title))

        found_theories = set()
        for word in title_words:
            if word in keyword_map:
                found_theories.update(keyword_map[word])

        if found_theories:
            auto_linkable += 1
            # Take top match (most specific)
            matches[key] = sorted(found_theories)[:3]

    print(f"  Auto-linkable via keywords:    {auto_linkable}")
    print(f"  Remaining unlinked:            {no_ts - auto_linkable}")

    # Show some examples
    if matches:
        examples = list(matches.items())[:5]
        print(f"\n  Sample auto-links:")
        for key, theories in examples:
            title = bib_data[key].get('title', '')[:50]
            print(f"    {key}: {title}... → {theories}")

    # NOTE: We do NOT auto-apply theory_support in BibTeX because:
    # - Keyword matching is imprecise
    # - theory_support should be reviewed by humans
    # - We just report the gap
    print(f"\n  NOTE: Auto-linking NOT applied (needs human review).")
    print(f"  Exportable list: {auto_linkable} papers could be linked.")

    return auto_linkable


# ═══════════════════════════════════════════════════════════════════════
# PHASE 6: Remove Deprecated migration_source References
# ═══════════════════════════════════════════════════════════════════════

def phase6_deprecated_refs(dry_run=True):
    print("\n" + "=" * 70)
    print("  PHASE 6: Remove Deprecated migration_source References")
    print("=" * 70)

    fixes = 0
    for fp in sorted(YAML_DIR.glob('PAP-*.yaml')):
        try:
            data = load_yaml(fp)
        except Exception:
            continue

        if not data:
            continue

        changed = False

        # Remove migration_source field
        if 'migration_source' in data:
            del data['migration_source']
            changed = True

        # Remove migration_status if it just says "ssot_migrated"
        if data.get('migration_status') == 'ssot_migrated':
            del data['migration_status']
            changed = True

        # Clean up ebf_migration_status
        ebf = data.get('ebf_integration', {})
        if ebf and ebf.get('ebf_migration_status') in ('migrated', 'pending'):
            del ebf['ebf_migration_status']
            changed = True

        if changed:
            fixes += 1
            if not dry_run:
                save_yaml(fp, data)

    print(f"  YAMLs cleaned: {fixes}")
    return fixes


# ═══════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description='Paper Database Cleanup')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes')
    parser.add_argument('--execute', action='store_true', help='Apply changes')
    parser.add_argument('--phase', type=int, default=0,
                        help='Run only specific phase (1-6), 0=all')
    args = parser.parse_args()

    if not args.dry_run and not args.execute:
        print("ERROR: Specify --dry-run or --execute")
        sys.exit(1)

    dry_run = args.dry_run
    mode = "DRY RUN" if dry_run else "EXECUTING"
    phase = args.phase

    print(f"\n{'='*70}")
    print(f"  PAPER DATABASE CLEANUP ({mode})")
    print(f"{'='*70}")

    total = 0

    if phase in (0, 1):
        total += phase1_queue_cleanup(dry_run)
    if phase in (0, 2):
        total += phase2_l3_overclaims(dry_run)
    if phase in (0, 3):
        total += phase3_legacy_paths(dry_run)
    if phase in (0, 4):
        total += phase4_integration_levels(dry_run)
    if phase in (0, 5):
        total += phase5_theory_support(dry_run)
    if phase in (0, 6):
        total += phase6_deprecated_refs(dry_run)

    print(f"\n{'='*70}")
    print(f"  TOTAL FIXES: {total}")
    if dry_run:
        print(f"  (DRY RUN — no files modified)")
    else:
        print(f"  All changes applied")
    print(f"{'='*70}\n")


if __name__ == '__main__':
    main()
