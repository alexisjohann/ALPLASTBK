#!/usr/bin/env python3
"""
Post-Task Completion Checker.

Validates that completed tasks in task-log.yaml have proper outcomes,
ebf_impact, and that the workflow was followed correctly.

Usage:
    python scripts/check_task_completion.py                    # Check all
    python scripts/check_task_completion.py --last             # Check last task
    python scripts/check_task_completion.py --task TL-019      # Check specific
    python scripts/check_task_completion.py --violations       # Show violations only

Called by pre-commit hook when task-log.yaml is modified.
"""

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
TASK_LOG = ROOT / "data" / "task-log.yaml"


def load_tasks():
    """Load all tasks from entries (consolidated by TL-074)."""
    with open(TASK_LOG, "r") as f:
        data = yaml.safe_load(f)
    return list(data.get("entries", []))


def check_task(task):
    """Check a single task for completion violations. Returns list of issues."""
    issues = []
    tid = task.get("task_id", "?")

    # Only check completed tasks
    status = task.get("outcome", {}).get("status", "")
    if not status or status == "in_progress":
        return issues

    # Check outcome fields
    outcome = task.get("outcome", {})
    if not outcome.get("status"):
        issues.append(f"{tid}: Missing outcome.status")
    if not outcome.get("result"):
        issues.append(f"{tid}: Missing outcome.result")

    # Check ebf_impact (PFLICHT)
    ebf = task.get("ebf_impact", {})
    if not ebf:
        issues.append(f"{tid}: Missing ebf_impact (PFLICHT)")
    else:
        for field in ["what_improved", "measurable", "enables_next"]:
            if not ebf.get(field):
                issues.append(f"{tid}: Missing ebf_impact.{field}")

    # Check timing
    timing = task.get("timing", {})
    if not timing.get("completed"):
        issues.append(f"{tid}: Missing timing.completed")

    # Check recommendation was made (only for post-enforcement tasks TL-070+)
    try:
        num = int(tid.replace("TL-", "").replace(".", ""))
    except (ValueError, AttributeError):
        num = 0

    if num >= 70:
        rec = task.get("recommendation", {})
        if isinstance(rec, dict) and not rec.get("default") and not rec.get("tier"):
            issues.append(f"{tid}: Missing recommendation.default")

    return issues


def main():
    parser = argparse.ArgumentParser(description="Check task completion")
    parser.add_argument("--last", action="store_true", help="Check last task only")
    parser.add_argument("--task", help="Check specific task ID")
    parser.add_argument("--violations", action="store_true", help="Show violations only")
    args = parser.parse_args()

    tasks = load_tasks()

    if not tasks:
        print("  No tasks found in task-log.yaml")
        return

    if args.task:
        tasks = [t for t in tasks if t.get("task_id") == args.task]
        if not tasks:
            print(f"  Task {args.task} not found")
            sys.exit(1)
    elif args.last:
        tasks = [tasks[-1]]

    total_issues = []
    checked = 0

    for task in tasks:
        issues = check_task(task)
        if issues:
            total_issues.extend(issues)
        if task.get("outcome", {}).get("status"):
            checked += 1

    if args.violations:
        if total_issues:
            print(f"\n  VIOLATIONS ({len(total_issues)}):")
            for issue in total_issues:
                print(f"    ❌ {issue}")
        else:
            print("  No violations found ✅")
        return

    # Summary
    print(f"\n  POST-TASK COMPLETION CHECK")
    print(f"  {'─' * 50}")
    print(f"  Tasks checked:   {checked}")
    print(f"  Violations:      {len(total_issues)}")

    if total_issues:
        print(f"\n  ISSUES:")
        for issue in total_issues:
            print(f"    ❌ {issue}")
        print(f"\n  Fix these before committing!")
        sys.exit(1)
    else:
        print(f"  Status:          All OK ✅")
    print()


if __name__ == "__main__":
    main()
