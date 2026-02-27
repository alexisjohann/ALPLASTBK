#!/usr/bin/env python3
"""
Branch Freshness Checker - Prevents merge conflicts by detecting divergence from main.

Usage:
    python scripts/check_branch_freshness.py              # Check current branch
    python scripts/check_branch_freshness.py --auto-rebase # Auto-rebase if possible
    python scripts/check_branch_freshness.py --status      # Show divergence summary
    python scripts/check_branch_freshness.py --file-conflicts  # Show potential file conflicts

Returns exit code 1 if branch has potential merge conflicts with main.
"""

import subprocess
import sys
import os


def run_git(args: list[str]) -> tuple[int, str]:
    """Run a git command and return (exit_code, output)."""
    result = subprocess.run(
        ["git"] + args,
        capture_output=True,
        text=True,
        cwd=os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd()),
    )
    return result.returncode, result.stdout.strip()


def get_current_branch() -> str:
    _, branch = run_git(["rev-parse", "--abbrev-ref", "HEAD"])
    return branch


def get_merge_base(branch: str, target: str = "origin/main") -> str:
    _, base = run_git(["merge-base", branch, target])
    return base


def get_commits_behind(target: str = "origin/main") -> int:
    _, output = run_git(["rev-list", "--count", f"HEAD..{target}"])
    try:
        return int(output)
    except ValueError:
        return 0


def get_commits_ahead(target: str = "origin/main") -> int:
    _, output = run_git(["rev-list", "--count", f"{target}..HEAD"])
    try:
        return int(output)
    except ValueError:
        return 0


def get_changed_files_on_branch(target: str = "origin/main") -> list[str]:
    """Get files changed on current branch since diverging from target."""
    _, output = run_git(["diff", "--name-only", f"{target}...HEAD"])
    return [f for f in output.split("\n") if f]


def get_changed_files_on_main(target: str = "origin/main") -> list[str]:
    """Get files changed on main since branch diverged."""
    merge_base = get_merge_base("HEAD", target)
    if not merge_base:
        return []
    _, output = run_git(["diff", "--name-only", merge_base, target])
    return [f for f in output.split("\n") if f]


def find_conflict_candidates() -> list[str]:
    """Find files modified on both the branch and main (potential conflicts)."""
    branch_files = set(get_changed_files_on_branch())
    main_files = set(get_changed_files_on_main())
    return sorted(branch_files & main_files)


def can_fast_forward(target: str = "origin/main") -> bool:
    """Check if branch can be fast-forwarded (no divergence)."""
    code, _ = run_git(["merge-base", "--is-ancestor", "HEAD", target])
    return code == 0


def try_auto_rebase(target: str = "origin/main") -> bool:
    """Attempt to rebase current branch onto target."""
    conflicts = find_conflict_candidates()
    if conflicts:
        print(f"Cannot auto-rebase: {len(conflicts)} files have potential conflicts:")
        for f in conflicts:
            print(f"  - {f}")
        return False

    print(f"Attempting rebase onto {target}...")
    code, output = run_git(["rebase", target])
    if code != 0:
        print(f"Rebase failed: {output}")
        run_git(["rebase", "--abort"])
        return False

    print("Rebase successful!")
    return True


def print_status():
    """Print a summary of branch divergence."""
    branch = get_current_branch()

    # Fetch latest main
    run_git(["fetch", "origin", "main"])

    behind = get_commits_behind()
    ahead = get_commits_ahead()
    conflicts = find_conflict_candidates()

    print(f"┌{'─' * 69}┐")
    print(f"│  BRANCH FRESHNESS CHECK{' ' * 46}│")
    print(f"├{'─' * 69}┤")
    print(f"│  Branch:     {branch:<55}│")
    print(f"│  Ahead:      {ahead} commits{' ' * (48 - len(str(ahead)))}│")
    print(f"│  Behind:     {behind} commits{' ' * (48 - len(str(behind)))}│")
    print(f"│  Conflicts:  {len(conflicts)} potential file conflicts{' ' * (31 - len(str(len(conflicts))))}│")

    if behind == 0:
        print(f"│{' ' * 69}│")
        print(f"│  {'STATUS: UP TO DATE':<67}│")
    elif len(conflicts) == 0:
        print(f"│{' ' * 69}│")
        print(f"│  {'STATUS: BEHIND but no file conflicts (safe to rebase)':<67}│")
    else:
        print(f"│{' ' * 69}│")
        print(f"│  {'STATUS: MERGE CONFLICTS LIKELY':<67}│")
        print(f"│{' ' * 69}│")
        print(f"│  {'Files modified on BOTH branch and main:':<67}│")
        for f in conflicts[:10]:
            line = f"│    - {f}"
            print(f"{line:<70}│")
        if len(conflicts) > 10:
            line = f"│    ... and {len(conflicts) - 10} more"
            print(f"{line:<70}│")

    print(f"│{' ' * 69}│")

    if behind > 0:
        print(f"│  {'RECOMMENDATION:':<67}│")
        if len(conflicts) == 0:
            print(f"│  {'  git fetch origin main && git rebase origin/main':<67}│")
        else:
            print(f"│  {'  git fetch origin main && git merge origin/main':<67}│")
            print(f"│  {'  Then resolve conflicts manually':<67}│")

    print(f"└{'─' * 69}┘")

    return behind, conflicts


def main():
    args = sys.argv[1:]

    if "--status" in args:
        behind, conflicts = print_status()
        sys.exit(1 if conflicts else 0)

    if "--auto-rebase" in args:
        run_git(["fetch", "origin", "main"])
        behind = get_commits_behind()
        if behind == 0:
            print("Branch is up to date with main.")
            sys.exit(0)
        if try_auto_rebase():
            sys.exit(0)
        else:
            print("Auto-rebase failed. Manual intervention needed.")
            sys.exit(1)

    if "--file-conflicts" in args:
        run_git(["fetch", "origin", "main"])
        conflicts = find_conflict_candidates()
        if conflicts:
            print(f"Potential conflict files ({len(conflicts)}):")
            for f in conflicts:
                print(f"  {f}")
            sys.exit(1)
        else:
            print("No potential file conflicts detected.")
            sys.exit(0)

    # Default: check and warn
    run_git(["fetch", "origin", "main"])
    behind = get_commits_behind()
    conflicts = find_conflict_candidates()

    if behind == 0:
        sys.exit(0)

    if conflicts:
        print(f"WARNING: Branch is {behind} commits behind main with {len(conflicts)} potential file conflicts:")
        for f in conflicts[:5]:
            print(f"  - {f}")
        if len(conflicts) > 5:
            print(f"  ... and {len(conflicts) - 5} more")
        print()
        print("Run: python scripts/check_branch_freshness.py --status")
        print("Fix: git fetch origin main && git merge origin/main")
        sys.exit(1)
    else:
        print(f"INFO: Branch is {behind} commits behind main (no file conflicts).")
        print("Recommended: git fetch origin main && git rebase origin/main")
        sys.exit(0)


if __name__ == "__main__":
    main()
