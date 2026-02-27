#!/usr/bin/env python3
"""
Task Dashboard — 3 Learning Loops + Overview.

Analyzes task-log.yaml and coding-mode-algorithm.yaml to show:
  1. Default-Kalibrierung (tier acceptance rate)
  2. Coding-Mode-Kalibrierung (TRADITIONAL vs EXPERIMENTAL success)
  3. Outcome/EBF-Impact (task value tracking)

Usage:
    python scripts/task_dashboard.py                 # Full dashboard
    python scripts/task_dashboard.py --loop1          # Default calibration only
    python scripts/task_dashboard.py --loop2          # Coding mode only
    python scripts/task_dashboard.py --loop3          # Outcome/impact only
    python scripts/task_dashboard.py --violations     # Workflow violations
    python scripts/task_dashboard.py --json           # Machine-readable output
"""

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
TASK_LOG = ROOT / "data" / "task-log.yaml"
ALGORITHM = ROOT / "data" / "coding-mode-algorithm.yaml"


def load_tasks():
    """Load all tasks from entries (consolidated by TL-074)."""
    with open(TASK_LOG) as f:
        data = yaml.safe_load(f)
    return list(data.get("entries", []))


def load_algorithm():
    with open(ALGORITHM) as f:
        return yaml.safe_load(f)


# ─────────────────────────────────────────────────────────────────────────
# LOOP 1: Default-Kalibrierung (Tier Acceptance Rate)
# ─────────────────────────────────────────────────────────────────────────
def loop1_default_calibration(tasks):
    """Analyze tier recommendation acceptance rate."""
    tiers = defaultdict(lambda: {"total": 0, "accepted": 0, "rejected": 0})
    no_rec = 0

    for t in tasks:
        rec = t.get("recommendation", {})
        if not isinstance(rec, dict):
            rec = {}

        # New schema: recommendation.tier
        tier = rec.get("tier")
        accepted = rec.get("accepted_default")

        # Old schema: task_type as tier equivalent
        if tier is None:
            tier = t.get("task_type")
            if tier:
                accepted = True  # old schema had no rejection tracking

        if tier is None:
            no_rec += 1
            continue

        tiers[tier]["total"] += 1
        if accepted is True:
            tiers[tier]["accepted"] += 1
        elif accepted is False:
            tiers[tier]["rejected"] += 1

    total = sum(v["total"] for v in tiers.values())
    total_accepted = sum(v["accepted"] for v in tiers.values())

    print("\n┌─────────────────────────────────────────────────────────────┐")
    print("│  LOOP 1: DEFAULT-KALIBRIERUNG (Tier Acceptance)             │")
    print("├─────────────────────────────────────────────────────────────┤")
    print(f"│  Gesamt: {total} Tasks mit Tier-Empfehlung                        │")

    if total > 0:
        rate = total_accepted / total * 100
        print(f"│  Akzeptanzrate: {rate:.0f}% ({total_accepted}/{total})                          │")
    print("│                                                             │")

    for tier in ["quick_win", "medium", "large"]:
        d = tiers.get(tier, {"total": 0, "accepted": 0, "rejected": 0})
        if d["total"] > 0:
            rate = d["accepted"] / d["total"] * 100
            bar = "█" * int(rate / 5) + "░" * (20 - int(rate / 5))
            print(f"│  {tier:12s}  {bar}  {rate:3.0f}% ({d['accepted']}/{d['total']})   │")

    if no_rec > 0:
        print(f"│                                                             │")
        print(f"│  ⚠️  {no_rec} Tasks OHNE Tier-Empfehlung (Workflow-Verletzung) │")

    print("└─────────────────────────────────────────────────────────────┘")

    return {
        "total": total,
        "accepted": total_accepted,
        "rate": total_accepted / total if total > 0 else 0,
        "no_recommendation": no_rec,
        "by_tier": {k: v for k, v in tiers.items()},
    }


# ─────────────────────────────────────────────────────────────────────────
# LOOP 2: Coding-Mode-Kalibrierung (TRADITIONAL vs EXPERIMENTAL)
# ─────────────────────────────────────────────────────────────────────────
def loop2_coding_mode(tasks):
    """Analyze coding mode decisions and outcomes."""
    modes = defaultdict(lambda: {
        "total": 0, "success": 0, "partial": 0, "tilt": 0,
        "files": [], "durations": [], "violations": []
    })

    for t in tasks:
        cm = t.get("coding_mode", {})
        if not isinstance(cm, dict):
            cm = {}
        mode = cm.get("mode") or cm.get("decision") or "UNKNOWN"
        outcome_raw = t.get("outcome", {})
        if isinstance(outcome_raw, dict):
            outcome = outcome_raw.get("status", "unknown")
        else:
            outcome = str(outcome_raw) if outcome_raw else "unknown"

        modes[mode]["total"] += 1
        if outcome == "success":
            modes[mode]["success"] += 1
        elif outcome == "partial":
            modes[mode]["partial"] += 1
        elif outcome == "tilt":
            modes[mode]["tilt"] += 1

        features = t.get("features", {})
        if features.get("files_affected"):
            modes[mode]["files"].append(features["files_affected"])

        timing = t.get("timing", {})
        dur = timing.get("duration_total_min") or timing.get("duration_min")
        if dur:
            modes[mode]["durations"].append(dur)

        # Check for would_different_choice_be_better
        learning = t.get("learning", {})
        if isinstance(learning, dict) and learning.get("would_different_choice_be_better"):
            modes[mode]["violations"].append(t.get("task_id", "?"))

    print("\n┌─────────────────────────────────────────────────────────────┐")
    print("│  LOOP 2: CODING-MODE-KALIBRIERUNG                           │")
    print("├─────────────────────────────────────────────────────────────┤")

    for mode in ["TRADITIONAL", "EXPERIMENTAL", "UNKNOWN"]:
        d = modes.get(mode)
        if not d or d["total"] == 0:
            continue

        success_rate = d["success"] / d["total"] * 100 if d["total"] > 0 else 0
        print(f"│                                                             │")
        print(f"│  {mode}:                                            │")
        print(f"│    Tasks: {d['total']:3d}  Success: {success_rate:3.0f}%                          │")

        if d["files"]:
            files = sorted(d["files"])
            median = files[len(files) // 2]
            print(f"│    Files: {min(files)}-{max(files)} (median: {median})                       │")

        if d["durations"]:
            durs = sorted(d["durations"])
            median = durs[len(durs) // 2]
            print(f"│    Duration: {min(durs)}-{max(durs)} min (median: {median})                  │")

        if d["tilt"] > 0:
            print(f"│    ❌ TILT: {d['tilt']} Tasks                                    │")
        if d["violations"]:
            print(f"│    ⚠️  Falsche Wahl: {', '.join(d['violations'])}                │")

    # Algorithm info
    try:
        algo = load_algorithm()
        thresh = algo.get("thresholds", {})
        print(f"│                                                             │")
        print(f"│  ALGORITHMUS v{algo.get('version', '?')}:                                          │")
        print(f"│    files ≤ {thresh.get('files_affected', '?')} → TRAD                                │")
        print(f"│    lines ≤ {thresh.get('lines_estimated', '?')} → TRAD (wenn pattern bekannt)        │")
    except Exception:
        pass

    print("└─────────────────────────────────────────────────────────────┘")

    return {mode: {k: v for k, v in d.items() if k != "files" and k != "durations"}
            for mode, d in modes.items()}


# ─────────────────────────────────────────────────────────────────────────
# LOOP 3: Outcome/EBF-Impact
# ─────────────────────────────────────────────────────────────────────────
def loop3_outcome_impact(tasks):
    """Analyze task outcomes and EBF impact."""
    complete = 0
    incomplete_impact = 0
    impact_types = Counter()
    total_duration = 0
    duration_count = 0

    for t in tasks:
        outcome = t.get("outcome", {})
        if not isinstance(outcome, dict):
            outcome = {"status": str(outcome)} if outcome else {}
        if outcome.get("status") == "success":
            complete += 1

        ebf = t.get("ebf_impact", {})
        if not isinstance(ebf, dict):
            ebf = {}
        if ebf and ebf.get("what_improved"):
            # Categorize impact
            text = (ebf.get("what_improved", "") + " " + ebf.get("enables_next", "")).lower()
            if "paper" in text or "bib" in text:
                impact_types["Paper/Bibliographie"] += 1
            elif "validier" in text or "consisten" in text or "compliance" in text:
                impact_types["Validierung/Qualität"] += 1
            elif "ssot" in text or "migr" in text or "cleanup" in text:
                impact_types["Daten/SSOT"] += 1
            elif "skill" in text or "workflow" in text or "enforcement" in text:
                impact_types["Process/Workflow"] += 1
            elif "model" in text or "parameter" in text or "theory" in text:
                impact_types["Modell/Theorie"] += 1
            else:
                impact_types["Andere"] += 1
        elif outcome.get("status") == "success":
            incomplete_impact += 1

        timing = t.get("timing", {})
        dur = timing.get("duration_total_min") or timing.get("duration_min")
        if dur:
            total_duration += dur
            duration_count += 1

    print("\n┌─────────────────────────────────────────────────────────────┐")
    print("│  LOOP 3: OUTCOME / EBF-IMPACT                               │")
    print("├─────────────────────────────────────────────────────────────┤")
    print(f"│  Tasks abgeschlossen: {complete}                                     │")
    print(f"│  Davon ohne EBF-Impact: {incomplete_impact}                               │")

    if duration_count > 0:
        avg = total_duration / duration_count
        print(f"│  Gesamtzeit: {total_duration} min ({total_duration / 60:.1f}h)                          │")
        print(f"│  Durchschnitt: {avg:.0f} min/Task                                  │")

    if impact_types:
        print(f"│                                                             │")
        print(f"│  IMPACT-KATEGORIEN:                                         │")
        for cat, count in impact_types.most_common():
            bar = "█" * count
            print(f"│    {cat:25s} {bar} ({count})            │")

    print("└─────────────────────────────────────────────────────────────┘")

    return {
        "complete": complete,
        "incomplete_impact": incomplete_impact,
        "total_duration_min": total_duration,
        "impact_types": dict(impact_types),
    }


# ─────────────────────────────────────────────────────────────────────────
# Workflow Violations
# ─────────────────────────────────────────────────────────────────────────
def _get_desc(t):
    """Get description from either schema format."""
    return t.get("description") or t.get("task_description") or "?"


def _has_tier(t):
    """Check if task has a tier recommendation (either schema)."""
    rec = t.get("recommendation", {})
    if isinstance(rec, dict):
        if rec.get("tier"):
            return True
    # Old schema: task_type field serves as tier equivalent
    if t.get("task_type"):
        return True
    return False


def show_violations(tasks):
    """Show all workflow violations (only for post-system tasks TL-070+)."""
    violations = []

    for t in tasks:
        tid = t.get("task_id", "?")

        # Explicit violations
        learning = t.get("learning", {})
        if isinstance(learning, dict) and learning.get("workflow_violation"):
            violations.append({
                "task_id": tid,
                "description": _get_desc(t),
                "type": learning.get("violation_type", "?"),
                "root_cause": learning.get("root_cause", "?"),
            })

        # Missing tier recommendation (only for TL-070+ where system was active)
        try:
            num = int(tid.replace("TL-", "").replace(".", ""))
        except (ValueError, AttributeError):
            num = 0

        if num >= 70 and not _has_tier(t):
            outcome = t.get("outcome", {})
            status = outcome.get("status", "") if isinstance(outcome, dict) else ""
            if status == "success":
                if not any(v["task_id"] == tid for v in violations):
                    violations.append({
                        "task_id": tid,
                        "description": _get_desc(t),
                        "type": "MISSING_RECOMMENDATION",
                        "root_cause": "No 3-tier box shown (post-enforcement)",
                    })

    print("\n┌─────────────────────────────────────────────────────────────┐")
    print("│  WORKFLOW-VERLETZUNGEN                                       │")
    print("├─────────────────────────────────────────────────────────────┤")

    if not violations:
        print("│  ✅ Keine Verletzungen gefunden                              │")
    else:
        print(f"│  ❌ {len(violations)} Verletzung(en):                                       │")
        for v in violations:
            print(f"│                                                             │")
            print(f"│  {v['task_id']}: {v['description'][:45]}│")
            print(f"│    Typ: {v['type'][:49]}│")
            print(f"│    Ursache: {v['root_cause'][:45]}│")

    print("└─────────────────────────────────────────────────────────────┘")

    return violations


# ─────────────────────────────────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────────────────────────────────
def _get_status(t):
    """Get outcome status from either schema format."""
    outcome = t.get("outcome", {})
    if isinstance(outcome, dict):
        return outcome.get("status", "")
    return str(outcome) if outcome else ""


def show_summary(tasks):
    """Show overall summary."""
    total = len(tasks)
    success = sum(1 for t in tasks if _get_status(t) == "success")
    in_progress = sum(1 for t in tasks if _get_status(t) == "in_progress")

    print("\n╔═════════════════════════════════════════════════════════════╗")
    print("║  EBF TASK DASHBOARD                                         ║")
    print("╠═════════════════════════════════════════════════════════════╣")
    print(f"║  Tasks gesamt: {total:3d}   Erfolg: {success:3d}   Offen: {in_progress:2d}                 ║")
    print(f"║  Erfolgsrate:  {success / total * 100:.0f}%                                        ║")
    print("╚═════════════════════════════════════════════════════════════╝")


def main():
    parser = argparse.ArgumentParser(description="EBF Task Dashboard")
    parser.add_argument("--loop1", action="store_true", help="Default calibration only")
    parser.add_argument("--loop2", action="store_true", help="Coding mode only")
    parser.add_argument("--loop3", action="store_true", help="Outcome/impact only")
    parser.add_argument("--violations", action="store_true", help="Violations only")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    tasks = load_tasks()
    show_all = not any([args.loop1, args.loop2, args.loop3, args.violations])

    results = {}

    if show_all:
        show_summary(tasks)

    if show_all or args.loop1:
        results["loop1"] = loop1_default_calibration(tasks)

    if show_all or args.loop2:
        results["loop2"] = loop2_coding_mode(tasks)

    if show_all or args.loop3:
        results["loop3"] = loop3_outcome_impact(tasks)

    if show_all or args.violations:
        results["violations"] = show_violations(tasks)

    if args.json:
        # Serialize only JSON-safe parts
        safe = {}
        for k, v in results.items():
            if isinstance(v, list):
                safe[k] = v
            elif isinstance(v, dict):
                safe[k] = {str(kk): vv for kk, vv in v.items()
                           if isinstance(vv, (str, int, float, bool, type(None), dict, list))}
        print(json.dumps(safe, indent=2, default=str))


if __name__ == "__main__":
    main()
