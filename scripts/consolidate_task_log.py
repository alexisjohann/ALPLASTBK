#!/usr/bin/env python3
"""Consolidate task-log.yaml: Merge dual-schema into single entries list.

TL-074: YAML-Schema Konsolidierung
EXPERIMENTAL: 1 → 10 → all

Problem:
  task-log.yaml has tasks split across two top-level keys:
  - entries: 16 tasks (TL-001 to TL-017)
  - learnings: 6 TLL entries (correct) + 49 TL tasks (wrong location)

Solution:
  1. Move all TL-xxx from learnings → entries
  2. Keep TLL-xxx in learnings
  3. Sort entries by TL-number
  4. Update metrics
  5. Preserve all data (no field renaming)

Usage:
  python scripts/consolidate_task_log.py --dry-run          # Preview changes
  python scripts/consolidate_task_log.py --dry-run --count 1 # Preview 1 task
  python scripts/consolidate_task_log.py --dry-run --count 10 # Preview 10
  python scripts/consolidate_task_log.py --execute            # Apply changes
"""

import argparse
import copy
import re
import sys
from pathlib import Path

import yaml


TASK_LOG = Path(__file__).parent.parent / "data" / "task-log.yaml"
BACKUP_PATH = TASK_LOG.with_suffix(".yaml.bak")


def load_yaml():
    """Load task-log.yaml preserving structure."""
    with open(TASK_LOG) as f:
        return yaml.safe_load(f)


def extract_tl_number(task):
    """Get numeric sort key from task_id like TL-073 or TL-066.5."""
    tid = task.get("task_id", "")
    m = re.match(r"TL-(\d+(?:\.\d+)?)", tid)
    if m:
        return float(m.group(1))
    return 9999


def analyze(data, max_count=None):
    """Analyze the dual-schema problem and return migration plan."""
    entries = list(data.get("entries", []) or [])
    learnings = list(data.get("learnings", []) or [])

    # Separate TL tasks from TLL learning entries
    tl_in_learnings = []
    tll_entries = []
    for item in learnings:
        if isinstance(item, dict):
            tid = item.get("task_id", "")
            iid = item.get("id", "")
            if tid.startswith("TL-"):
                tl_in_learnings.append(item)
            elif iid.startswith("TLL-"):
                tll_entries.append(item)
            else:
                tll_entries.append(item)  # Unknown → keep in learnings

    # Limit for EXPERIMENTAL phasing
    if max_count is not None:
        tl_to_move = tl_in_learnings[:max_count]
        tl_remaining = tl_in_learnings[max_count:]
    else:
        tl_to_move = tl_in_learnings
        tl_remaining = []

    return {
        "entries_count": len(entries),
        "tl_in_learnings_count": len(tl_in_learnings),
        "tll_count": len(tll_entries),
        "to_move_count": len(tl_to_move),
        "remaining_count": len(tl_remaining),
        "entries": entries,
        "tl_to_move": tl_to_move,
        "tl_remaining": tl_remaining,
        "tll_entries": tll_entries,
    }


def compute_metrics(all_entries):
    """Recompute metrics from all entries."""
    total = len(all_entries)
    by_type = {"quick_win": 0, "medium": 0, "large": 0}
    by_mode = {"TRADITIONAL": 0, "EXPERIMENTAL": 0}
    by_status = {"success": 0, "partial": 0, "tilt": 0, "in_progress": 0}
    durations = {"quick_win": [], "medium": [], "large": []}
    rec_total = 0
    rec_accepted = 0
    rec_overridden = 0

    for t in all_entries:
        # Type / tier
        ttype = t.get("task_type") or t.get("type", "")
        rec = t.get("recommendation", {})
        tier = ""
        if isinstance(rec, dict):
            tier = rec.get("tier", "")
        task_tier = tier or ttype
        if task_tier in by_type:
            by_type[task_tier] += 1

        # Coding mode
        cm = t.get("coding_mode", {})
        if isinstance(cm, dict):
            mode = cm.get("decision") or cm.get("mode", "")
            if mode in by_mode:
                by_mode[mode] += 1

        # Status
        outcome = t.get("outcome", {})
        if isinstance(outcome, dict):
            status = outcome.get("status", "")
        else:
            status = str(outcome) if outcome else ""
        if status in by_status:
            by_status[status] += 1

        # Timing
        timing = t.get("timing", {})
        if isinstance(timing, dict):
            dur = timing.get("duration_min") or timing.get("duration_total_min")
            if dur and task_tier in durations:
                durations[task_tier].append(dur)

        # Recommendation tracking
        if isinstance(rec, dict):
            if rec.get("default") is not None or rec.get("tier"):
                rec_total += 1
                ad = rec.get("accepted_default")
                if ad is True:
                    rec_accepted += 1
                elif ad is False:
                    rec_overridden += 1

    avg_durations = {}
    for k, v in durations.items():
        if v:
            avg_durations[k] = round(sum(v) / len(v), 1)

    return {
        "total_tasks": total,
        "by_type": by_type,
        "by_coding_mode": by_mode,
        "by_status": by_status,
        "recommendation": {
            "total_with_default": rec_total,
            "default_accepted": rec_accepted,
            "default_overridden": rec_overridden,
            "acceptance_rate": round(rec_accepted / rec_total, 2) if rec_total > 0 else 0,
        },
        "timing": {
            "avg_duration_min": avg_durations,
        },
    }


def build_consolidated(data, analysis):
    """Build the consolidated YAML structure."""
    # Merge entries + moved tasks, sort by TL number
    all_entries = list(analysis["entries"]) + list(analysis["tl_to_move"])
    all_entries.sort(key=extract_tl_number)

    # Rebuild learnings (TLL only + any remaining TL tasks)
    new_learnings = list(analysis["tll_entries"]) + list(analysis["tl_remaining"])

    # Compute fresh metrics
    metrics = compute_metrics(all_entries)

    return {
        "entries": all_entries,
        "metrics": metrics,
        "rules": data.get("rules", []),
        "learnings": new_learnings,
    }


def write_yaml(consolidated):
    """Write consolidated YAML with proper formatting."""
    # Backup first
    import shutil
    shutil.copy2(TASK_LOG, BACKUP_PATH)
    print(f"  Backup: {BACKUP_PATH}")

    # Write header + YAML
    header = """# Unified Task Log
# Konsolidiert: coding-mode-log.yaml + recommendation-log.yaml
# SSOT für alle Tasks, Empfehlungen und Outcomes
#
# SCHEMA-KONSOLIDIERUNG (TL-074, 2026-02-12):
#   Alle 65 Tasks sind jetzt unter 'entries' (vorher: 16 in entries + 49 in learnings)
#   TLL-Einträge bleiben unter 'learnings'
#
# DREI LERNSCHLEIFEN:
#   1. Default-Kalibrierung: Akzeptanzrate → richtige Stufe empfehlen
#   2. Coding-Mode-Kalibrierung: TRADITIONAL/EXPERIMENTAL → richtige Methode wählen
#   3. Outcome/EBF-Impact: Hat die Aktion das EBF weitergebracht?

"""

    with open(TASK_LOG, "w") as f:
        f.write(header)

        # Write entries
        f.write("entries:\n\n")
        for entry in consolidated["entries"]:
            f.write(yaml.dump([entry], default_flow_style=False, allow_unicode=True, width=120, sort_keys=False))
            f.write("\n")

        # Write metrics section
        f.write("# " + "=" * 60 + "\n")
        f.write("# METRIKEN (auto-generiert bei Konsolidierung)\n")
        f.write("# " + "=" * 60 + "\n\n")
        f.write(yaml.dump({"metrics": consolidated["metrics"]}, default_flow_style=False, allow_unicode=True, sort_keys=False))
        f.write("\n")

        # Write rules section
        f.write("# " + "=" * 60 + "\n")
        f.write("# CODING-MODE ALGORITHMUS (Referenz)\n")
        f.write("# " + "=" * 60 + "\n")
        f.write("# SSOT: data/coding-mode-algorithm.yaml\n\n")
        f.write(yaml.dump({"rules": consolidated["rules"]}, default_flow_style=False, allow_unicode=True, sort_keys=False))
        f.write("\n")

        # Write learnings section
        f.write("# " + "=" * 60 + "\n")
        f.write("# LEARNINGS (nach jedem Override oder bemerkenswertem Outcome)\n")
        f.write("# " + "=" * 60 + "\n\n")
        if consolidated["learnings"]:
            f.write(yaml.dump({"learnings": consolidated["learnings"]}, default_flow_style=False, allow_unicode=True, width=120, sort_keys=False))
        else:
            f.write("learnings: []\n")
        f.write("\n")

        # Deprecated notice
        f.write("# " + "=" * 60 + "\n")
        f.write("# DEPRECATED QUELLEN (Daten sind hier konsolidiert)\n")
        f.write("# " + "=" * 60 + "\n")
        f.write("# data/coding-mode-log.yaml → Einträge migriert als TL-001\n")
        f.write("# data/recommendation-log.yaml → Einträge migriert als TL-002, TL-003, TL-004\n")
        f.write("# Beide Dateien bleiben als Referenz, task-log.yaml ist SSOT\n")

    print(f"  Written: {TASK_LOG}")


def main():
    parser = argparse.ArgumentParser(description="Consolidate task-log.yaml dual-schema")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    parser.add_argument("--execute", action="store_true", help="Apply consolidation")
    parser.add_argument("--count", type=int, default=None, help="Limit tasks to move (EXPERIMENTAL phasing)")
    args = parser.parse_args()

    if not args.dry_run and not args.execute:
        print("Usage: specify --dry-run or --execute")
        sys.exit(1)

    print("Loading task-log.yaml...")
    data = load_yaml()

    print("Analyzing structure...")
    analysis = analyze(data, max_count=args.count)

    print(f"\n{'=' * 60}")
    print(f"CONSOLIDATION PLAN")
    print(f"{'=' * 60}")
    print(f"  entries (current):     {analysis['entries_count']} tasks")
    print(f"  TL in learnings:       {analysis['tl_in_learnings_count']} tasks (WRONG location)")
    print(f"  TLL in learnings:      {analysis['tll_count']} entries (CORRECT location)")
    print(f"  ---")
    print(f"  To move → entries:     {analysis['to_move_count']} tasks")
    print(f"  Remaining in learnings:{analysis['remaining_count']} tasks")
    print(f"  ---")
    print(f"  entries (after):       {analysis['entries_count'] + analysis['to_move_count']} tasks")
    print(f"  learnings (after):     {analysis['tll_count'] + analysis['remaining_count']} entries")

    if analysis["to_move_count"] > 0:
        print(f"\n  Tasks to move:")
        for t in analysis["tl_to_move"]:
            tid = t.get("task_id", "?")
            desc = t.get("task_description") or t.get("description", "?")
            print(f"    {tid}: {desc[:60]}")

    if args.dry_run:
        print(f"\n  DRY RUN — no changes written.")

        # Show what metrics would look like
        if args.count is None:
            consolidated = build_consolidated(data, analysis)
            m = consolidated["metrics"]
            print(f"\n  Updated metrics:")
            print(f"    total_tasks: {m['total_tasks']}")
            print(f"    by_type: {m['by_type']}")
            print(f"    by_coding_mode: {m['by_coding_mode']}")
            print(f"    by_status: {m['by_status']}")
            print(f"    acceptance_rate: {m['recommendation']['acceptance_rate']}")
        return

    if args.execute:
        print(f"\n  EXECUTING consolidation...")
        consolidated = build_consolidated(data, analysis)
        write_yaml(consolidated)

        # Verify
        print(f"\n  Verifying...")
        verify_data = load_yaml()
        v_entries = verify_data.get("entries", [])
        v_learnings = verify_data.get("learnings", [])
        tl_in_v_learnings = sum(1 for x in v_learnings if isinstance(x, dict) and x.get("task_id", "").startswith("TL-"))

        print(f"    entries: {len(v_entries)} tasks")
        print(f"    learnings: {len(v_learnings)} entries")
        print(f"    TL still in learnings: {tl_in_v_learnings}")

        if tl_in_v_learnings == 0 and args.count is None:
            print(f"\n  ✅ CONSOLIDATION COMPLETE — all TL tasks in entries")
        elif args.count is not None:
            print(f"\n  ✅ PARTIAL CONSOLIDATION — {analysis['to_move_count']} tasks moved, {analysis['remaining_count']} remaining")
        else:
            print(f"\n  ❌ VERIFICATION FAILED — TL tasks still in learnings!")
            sys.exit(1)


if __name__ == "__main__":
    main()
