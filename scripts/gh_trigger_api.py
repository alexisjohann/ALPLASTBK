#!/usr/bin/env python3
"""
GitHub Actions API Trigger — Zero-Sandbox-API Architecture
===========================================================
Triggers GitHub Actions workflows from the sandbox via `gh workflow run`.
NO external API calls leave this sandbox. All API work runs on GH runners.

Usage:
    # Fetch Sutter papers (default)
    python scripts/gh_trigger_api.py fetch-papers

    # Fetch with experimental mode
    python scripts/gh_trigger_api.py fetch-papers --experimental

    # Fetch for a different researcher
    python scripts/gh_trigger_api.py fetch-papers --name Fehr --person-id persons12345 --orcid 0000-0001-...

    # Enrich abstracts
    python scripts/gh_trigger_api.py enrich-abstracts

    # Enrich with experimental mode
    python scripts/gh_trigger_api.py enrich-abstracts --experimental

    # Dry run (any command)
    python scripts/gh_trigger_api.py fetch-papers --dry-run

    # Check status of last run
    python scripts/gh_trigger_api.py status fetch-papers

    # View logs of last run
    python scripts/gh_trigger_api.py logs fetch-papers

    # Full pipeline: fetch + enrich
    python scripts/gh_trigger_api.py pipeline --name Sutter

Architecture:
    ┌─────────────────────────────────────────────────────────┐
    │  SANDBOX (Claude Code)                                   │
    │  ┌─────────────────────────────────────────────────────┐ │
    │  │  gh_trigger_api.py                                  │ │
    │  │  ├── gh workflow run fetch-mpg-papers.yml ...       │ │
    │  │  ├── gh run list --workflow=...                     │ │
    │  │  ├── gh run view <id> --log                        │ │
    │  │  └── git pull (to get committed results)            │ │
    │  └─────────────────────────────────────────────────────┘ │
    │                    │ gh CLI only                          │
    └────────────────────┼─────────────────────────────────────┘
                         │
    ┌────────────────────┼─────────────────────────────────────┐
    │  GITHUB ACTIONS    │                                      │
    │  ├── PuRe API      ← fetch_mpg_pure_papers.py            │
    │  ├── OpenAlex API  ← enrich_papers_abstracts.py          │
    │  ├── CrossRef API  ← doi-lookup workflows                │
    │  └── Commit + Push ← results back to branch              │
    └──────────────────────────────────────────────────────────┘

API Registry: data/api-registry.yaml
"""

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path


# The sandbox proxy makes git remotes unrecognizable to gh CLI.
# Always pass --repo explicitly so gh knows which repository to target.
REPO = "FehrAdvice-Partners-AG/complementarity-context-framework"


def ensure_gh_token():
    """Auto-load GH_TOKEN from .claude/.gh_token if not set."""
    if os.environ.get("GH_TOKEN"):
        return
    # Search upward from script location for .claude/.gh_token
    script_dir = Path(__file__).resolve().parent
    for candidate in [script_dir.parent, Path.cwd()]:
        token_file = candidate / ".claude" / ".gh_token"
        if token_file.exists():
            token = token_file.read_text().strip()
            if token:
                os.environ["GH_TOKEN"] = token
                return
    print("WARNING: GH_TOKEN not set and .claude/.gh_token not found.", file=sys.stderr)
    print("  Run: gh auth login --with-token", file=sys.stderr)


def run_gh(args: list, capture=True, check=True) -> subprocess.CompletedProcess:
    """Run gh CLI command with retry on network errors.

    Automatically injects --repo flag because the sandbox proxy
    makes local git remotes unrecognizable to gh CLI.
    """
    # Inject --repo if not already present
    if "--repo" not in args and "-R" not in args:
        args = args[:1] + ["--repo", REPO] + args[1:]
    cmd = ["gh"] + args
    max_retries = 4
    for attempt in range(max_retries):
        try:
            result = subprocess.run(
                cmd,
                capture_output=capture,
                text=True,
                check=check,
                timeout=60,
            )
            return result
        except subprocess.CalledProcessError as e:
            # Don't retry on auth/permission errors
            if "403" in str(e.stderr) or "401" in str(e.stderr):
                raise
            if attempt < max_retries - 1:
                wait = 2 ** (attempt + 1)
                print(f"  Network error, retrying in {wait}s... ({e})")
                time.sleep(wait)
            else:
                raise
        except subprocess.TimeoutExpired:
            if attempt < max_retries - 1:
                wait = 2 ** (attempt + 1)
                print(f"  Timeout, retrying in {wait}s...")
                time.sleep(wait)
            else:
                raise


def get_current_branch() -> str:
    """Get the current git branch name."""
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True, text=True, check=True,
    )
    return result.stdout.strip()


def trigger_fetch_papers(args):
    """Trigger the fetch-mpg-papers workflow."""
    branch = get_current_branch()
    print(f"{'=' * 60}")
    print(f"  TRIGGER: Fetch Papers from MPG.PuRe / OpenAlex")
    print(f"{'=' * 60}")
    print(f"  Branch:      {branch}")
    print(f"  Researcher:  {args.name}")
    print(f"  Person ID:   {args.person_id}")
    print(f"  ORCID:       {args.orcid}")
    print(f"  LIT:         LIT-{args.lit}")
    print(f"  Mode:        {'experimental' if args.experimental else 'traditional'}")
    print(f"  Dry run:     {args.dry_run}")
    print()

    gh_args = [
        "workflow", "run", "fetch-mpg-papers.yml",
        "--ref", branch,
        "-f", f"researcher_name={args.name}",
        "-f", f"person_id={args.person_id}",
        "-f", f"lit_appendix={args.lit}",
        "-f", f"dry_run={'true' if args.dry_run else 'false'}",
        "-f", f"mode={'experimental' if args.experimental else 'traditional'}",
    ]

    if args.orcid:
        gh_args.extend(["-f", f"orcid={args.orcid}"])

    if args.first_name:
        gh_args.extend(["-f", f"researcher_first_name={args.first_name}"])

    if args.experimental and args.stages:
        gh_args.extend(["-f", f"stages={args.stages}"])

    print("  Running: gh " + " ".join(gh_args[2:]))
    run_gh(gh_args)
    print("\n  Workflow triggered. Check status with:")
    print(f"    python scripts/gh_trigger_api.py status fetch-papers")
    print(f"    python scripts/gh_trigger_api.py logs fetch-papers")


def trigger_enrich_abstracts(args):
    """Trigger the enrich-paper-abstracts workflow."""
    branch = get_current_branch()
    print(f"{'=' * 60}")
    print(f"  TRIGGER: Enrich Papers with Abstracts (OpenAlex)")
    print(f"{'=' * 60}")
    print(f"  Branch:      {branch}")
    print(f"  Input:       {args.input_file}")
    print(f"  Batch:       {args.batch}")
    print(f"  Mode:        {'experimental' if args.experimental else 'traditional'}")
    print(f"  Update bib:  {args.update_master}")
    print(f"  Dry run:     {args.dry_run}")
    print()

    gh_args = [
        "workflow", "run", "enrich-paper-abstracts.yml",
        "--ref", branch,
        "-f", f"input_file={args.input_file}",
        "-f", f"batch_size={args.batch}",
        "-f", f"update_master={'true' if args.update_master else 'false'}",
        "-f", f"dry_run={'true' if args.dry_run else 'false'}",
        "-f", f"mode={'experimental' if args.experimental else 'traditional'}",
    ]

    if args.experimental and args.stages:
        gh_args.extend(["-f", f"stages={args.stages}"])

    print("  Running: gh " + " ".join(gh_args[2:]))
    run_gh(gh_args)
    print("\n  Workflow triggered. Check status with:")
    print(f"    python scripts/gh_trigger_api.py status enrich-abstracts")


def trigger_fetch_fulltext(args):
    """Trigger the fetch-fulltext task via academic-api-sync workflow.

    Uses the registered academic-api-sync.yml workflow with task=fetch-fulltext.
    The branch version of the workflow includes the fetch-fulltext task.
    """
    branch = get_current_branch()
    print(f"{'=' * 60}")
    print(f"  TRIGGER: Fetch Full Texts (L2 → L3 Upgrade)")
    print(f"{'=' * 60}")
    print(f"  Branch:      {branch}")
    print(f"  Author:      {args.author}")
    print(f"  Batch:       {args.batch}")
    print(f"  Dry run:     {args.dry_run}")
    print()

    gh_args = [
        "workflow", "run", "academic-api-sync.yml",
        "--ref", branch,
        "-f", "api=unpaywall",
        "-f", "task=fetch-fulltext",
        "-f", f"limit={args.batch}",
        "-f", f"author_filter={args.author}",
        "-f", f"dry_run={'true' if args.dry_run else 'false'}",
        "-f", f"target_branch={branch}",
    ]

    print("  Running: gh " + " ".join(gh_args[2:]))
    run_gh(gh_args)
    print("\n  ✓ Workflow triggered. Check status with:")
    print(f"    python scripts/gh_trigger_api.py status fetch-fulltext")
    print(f"    python scripts/gh_trigger_api.py wait fetch-fulltext")


def trigger_fetch_mpg_fulltext(args):
    """Trigger the fetch-mpg-fulltext task via academic-api-sync workflow.

    Downloads PDFs from MPG PuRe (institutional repository) for L2→L3 upgrade.
    MPG PuRe hosts author-uploaded PDFs that publishers often block (HTTP 403).

    Special: --inspect item_XXXX inspects a single item (file details, storage, download test).
    """
    branch = get_current_branch()
    inspect_mode = bool(getattr(args, "inspect", ""))
    find_internal_mode = bool(getattr(args, "find_internal", False))
    fetch_internal_mode = bool(getattr(args, "fetch_internal", False))

    print(f"{'=' * 60}")
    if inspect_mode:
        print(f"  INSPECT: Single PuRe Item {args.inspect}")
    elif find_internal_mode:
        print(f"  FIND-INTERNAL: Scan all items for INTERNAL_MANAGED files")
    elif fetch_internal_mode:
        print(f"  FETCH-INTERNAL: Download PDFs from INTERNAL_MANAGED items")
    else:
        print(f"  TRIGGER: Fetch Full Texts from MPG PuRe (L2 → L3)")
    print(f"{'=' * 60}")
    print(f"  Branch:      {branch}")

    if inspect_mode:
        print(f"  Item ID:     {args.inspect}")
        limit_val = args.inspect
    elif find_internal_mode:
        print(f"  Person ID:   {args.person_id}")
        print(f"  Author:      {args.name}")
        limit_val = "find-internal"
    elif fetch_internal_mode:
        print(f"  Person ID:   {args.person_id}")
        print(f"  Author:      {args.name}")
        print(f"  Batch:       {args.batch}")
        print(f"  Dry run:     {args.dry_run}")
        limit_val = "fetch-internal"
    else:
        print(f"  Person ID:   {args.person_id}")
        print(f"  Author:      {args.name}")
        print(f"  Batch:       {args.batch}")
        print(f"  Dry run:     {args.dry_run}")
        limit_val = args.batch

    print()

    gh_args = [
        "workflow", "run", "academic-api-sync.yml",
        "--ref", branch,
        "-f", "api=unpaywall",
        "-f", "task=fetch-mpg-fulltext",
        "-f", f"limit={limit_val}",
        "-f", f"author_filter={args.name}",
        "-f", f"person_id={args.person_id}",
        "-f", f"dry_run={'true' if args.dry_run else 'false'}",
        "-f", f"target_branch={branch}",
    ]

    print("  Running: gh " + " ".join(gh_args[2:]))
    run_gh(gh_args)
    print("\n  ✓ Workflow triggered. Check status with:")
    print(f"    python scripts/gh_trigger_api.py status fetch-mpg-fulltext")
    print(f"    python scripts/gh_trigger_api.py wait fetch-mpg-fulltext")


def show_status(args):
    """Show status of recent workflow runs."""
    workflow_map = {
        "fetch-papers": "fetch-mpg-papers.yml",
        "fetch-fulltext": "academic-api-sync.yml",
        "fetch-mpg-fulltext": "academic-api-sync.yml",
        "enrich-abstracts": "enrich-paper-abstracts.yml",
        "abstract-enrichment": "abstract-enrichment.yml",
        "academic-sync": "academic-api-sync.yml",
        "doi-lookup": "doi-lookup.yml",
        "doi-batch": "doi-lookup-batch.yml",
    }

    workflow = workflow_map.get(args.workflow_name, args.workflow_name)

    print(f"{'=' * 60}")
    print(f"  STATUS: {workflow}")
    print(f"{'=' * 60}")

    result = run_gh([
        "run", "list",
        "--workflow", workflow,
        "--limit", "5",
    ])
    print(result.stdout)


def show_logs(args):
    """Show logs of the most recent workflow run."""
    workflow_map = {
        "fetch-papers": "fetch-mpg-papers.yml",
        "fetch-fulltext": "academic-api-sync.yml",
        "fetch-mpg-fulltext": "academic-api-sync.yml",
        "enrich-abstracts": "enrich-paper-abstracts.yml",
        "abstract-enrichment": "abstract-enrichment.yml",
        "academic-sync": "academic-api-sync.yml",
    }

    workflow = workflow_map.get(args.workflow_name, args.workflow_name)

    # Get the most recent run ID
    result = run_gh([
        "run", "list",
        "--workflow", workflow,
        "--limit", "1",
        "--json", "databaseId,status,conclusion",
    ])

    runs = json.loads(result.stdout)
    if not runs:
        print(f"  No runs found for {workflow}")
        return

    run_id = runs[0]["databaseId"]
    status = runs[0]["status"]
    conclusion = runs[0].get("conclusion", "")

    print(f"  Run ID:     {run_id}")
    print(f"  Status:     {status}")
    if conclusion:
        print(f"  Conclusion: {conclusion}")
    print()

    if status == "completed":
        # Show logs
        log_result = run_gh(["run", "view", str(run_id), "--log"], check=False)
        if log_result.returncode == 0:
            # Show last 100 lines
            lines = log_result.stdout.strip().split("\n")
            if len(lines) > 100:
                print(f"  ... ({len(lines) - 100} lines omitted)")
                for line in lines[-100:]:
                    print(f"  {line}")
            else:
                for line in lines:
                    print(f"  {line}")
        else:
            print(f"  Could not fetch logs: {log_result.stderr}")
    else:
        print(f"  Run is still {status}. Logs available after completion.")
        print(f"  Watch live: gh run watch {run_id}")


def trigger_pipeline(args):
    """Trigger full pipeline: fetch papers, then enrich abstracts."""
    branch = get_current_branch()
    print(f"{'=' * 60}")
    print(f"  PIPELINE: Fetch + Enrich for {args.name}")
    print(f"{'=' * 60}")
    print(f"  Branch: {branch}")
    print(f"  Step 1: Fetch papers (PuRe → OpenAlex fallback)")
    print(f"  Step 2: Enrich abstracts (OpenAlex)")
    print(f"  Mode:   {'experimental' if args.experimental else 'traditional'}")
    print()

    # Step 1: Trigger fetch
    print("  Step 1: Triggering paper fetch...")
    fetch_args = [
        "workflow", "run", "fetch-mpg-papers.yml",
        "--ref", branch,
        "-f", f"researcher_name={args.name}",
        "-f", f"person_id={args.person_id}",
        "-f", f"lit_appendix={args.lit}",
        "-f", f"dry_run={'true' if args.dry_run else 'false'}",
        "-f", f"mode={'experimental' if args.experimental else 'traditional'}",
    ]
    if args.orcid:
        fetch_args.extend(["-f", f"orcid={args.orcid}"])
    if args.first_name:
        fetch_args.extend(["-f", f"researcher_first_name={args.first_name}"])

    run_gh(fetch_args)
    print("  Fetch workflow triggered.")
    print()
    print("  NEXT STEPS (manual — GitHub Actions don't chain):")
    print(f"    1. Wait for fetch to complete:")
    print(f"       python scripts/gh_trigger_api.py status fetch-papers")
    print(f"    2. Pull results:")
    print(f"       git pull origin {branch}")
    print(f"    3. Trigger enrichment:")
    print(f"       python scripts/gh_trigger_api.py enrich-abstracts")
    print(f"    4. Wait + pull:")
    print(f"       python scripts/gh_trigger_api.py status enrich-abstracts")
    print(f"       git pull origin {branch}")


def wait_for_run(args):
    """Wait for a workflow run to complete, polling every 15s."""
    workflow_map = {
        "fetch-papers": "fetch-mpg-papers.yml",
        "fetch-fulltext": "academic-api-sync.yml",
        "fetch-mpg-fulltext": "academic-api-sync.yml",
        "enrich-abstracts": "enrich-paper-abstracts.yml",
    }

    workflow = workflow_map.get(args.workflow_name, args.workflow_name)

    print(f"  Waiting for {workflow} to complete...")

    # Get most recent run
    result = run_gh([
        "run", "list",
        "--workflow", workflow,
        "--limit", "1",
        "--json", "databaseId,status,conclusion",
    ])
    runs = json.loads(result.stdout)
    if not runs:
        print(f"  No runs found for {workflow}")
        return

    run_id = runs[0]["databaseId"]
    print(f"  Run ID: {run_id}")

    while True:
        result = run_gh([
            "run", "view", str(run_id),
            "--json", "status,conclusion",
        ])
        data = json.loads(result.stdout)
        status = data.get("status", "unknown")
        conclusion = data.get("conclusion", "")

        if status == "completed":
            print(f"\n  Completed: {conclusion}")
            if conclusion == "success":
                print(f"  Pull results: git pull origin {get_current_branch()}")
            else:
                print(f"  Check logs: python scripts/gh_trigger_api.py logs {args.workflow_name}")
            return
        elif status in ("queued", "in_progress"):
            print(f"  [{time.strftime('%H:%M:%S')}] Status: {status}...", end="\r")
            time.sleep(15)
        else:
            print(f"\n  Unexpected status: {status}")
            return


def main():
    parser = argparse.ArgumentParser(
        description="Trigger GitHub Actions API workflows from sandbox",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Fetch Sutter papers:           %(prog)s fetch-papers
  Fetch experimental:            %(prog)s fetch-papers --experimental
  Enrich abstracts:              %(prog)s enrich-abstracts
  Full pipeline:                 %(prog)s pipeline --name Sutter
  Check status:                  %(prog)s status fetch-papers
  View logs:                     %(prog)s logs fetch-papers
  Wait for completion:           %(prog)s wait fetch-papers

Architecture: Zero external API calls from sandbox.
All API work runs on GitHub Actions runners.
""",
    )

    sub = parser.add_subparsers(dest="command", help="Command to run")

    # --- fetch-papers ---
    fetch = sub.add_parser("fetch-papers", help="Fetch papers from PuRe/OpenAlex")
    fetch.add_argument("--name", default="Sutter", help="Researcher last name")
    fetch.add_argument("--first-name", default="Matthias", help="First name")
    fetch.add_argument("--person-id", default="persons206813", help="PuRe person ID")
    fetch.add_argument("--orcid", default="0000-0002-6143-8406", help="ORCID")
    fetch.add_argument("--lit", default="SUT", help="LIT-Appendix code")
    fetch.add_argument("--experimental", action="store_true", help="Experimental mode")
    fetch.add_argument("--stages", default="1,10,100,0", help="Custom stages")
    fetch.add_argument("--dry-run", action="store_true", help="Dry run")

    # --- enrich-abstracts ---
    enrich = sub.add_parser("enrich-abstracts", help="Enrich papers with abstracts")
    enrich.add_argument("--input-file", default="new_papers_bibtex.bib", help="Input file")
    enrich.add_argument("--batch", default="0", help="Batch size (0=all)")
    enrich.add_argument("--update-master", action="store_true", default=True,
                         help="Update bcm_master.bib")
    enrich.add_argument("--experimental", action="store_true", help="Experimental mode")
    enrich.add_argument("--stages", default="1,10,100,0", help="Custom stages")
    enrich.add_argument("--dry-run", action="store_true", help="Dry run")

    # --- fetch-fulltext ---
    ft = sub.add_parser("fetch-fulltext", help="Fetch OA full texts (L2→L3)")
    ft.add_argument("--author", default="sutter", help="Author filter")
    ft.add_argument("--batch", default="5", help="Batch size")
    ft.add_argument("--dry-run", action="store_true", help="Dry run (check OA only)")

    # --- fetch-mpg-fulltext ---
    mpg = sub.add_parser("fetch-mpg-fulltext", help="Fetch full texts from MPG PuRe (L2→L3)")
    mpg.add_argument("--name", default="sutter", help="Author filter name")
    mpg.add_argument("--person-id", default="persons206813", help="PuRe person ID")
    mpg.add_argument("--batch", default="50", help="Batch size")
    mpg.add_argument("--inspect", default="", help="Inspect single item (e.g., item_3674646)")
    mpg.add_argument("--find-internal", action="store_true", help="Scan all items for INTERNAL_MANAGED files")
    mpg.add_argument("--fetch-internal", action="store_true", help="Download PDFs from INTERNAL_MANAGED items found by --find-internal")
    mpg.add_argument("--dry-run", action="store_true", help="Dry run")

    # --- pipeline ---
    pipe = sub.add_parser("pipeline", help="Full pipeline: fetch + enrich")
    pipe.add_argument("--name", default="Sutter", help="Researcher last name")
    pipe.add_argument("--first-name", default="Matthias", help="First name")
    pipe.add_argument("--person-id", default="persons206813", help="PuRe person ID")
    pipe.add_argument("--orcid", default="0000-0002-6143-8406", help="ORCID")
    pipe.add_argument("--lit", default="SUT", help="LIT-Appendix code")
    pipe.add_argument("--experimental", action="store_true", help="Experimental mode")
    pipe.add_argument("--dry-run", action="store_true", help="Dry run")

    # --- status ---
    status = sub.add_parser("status", help="Show workflow run status")
    status.add_argument("workflow_name", help="Workflow name (fetch-papers, enrich-abstracts, ...)")

    # --- logs ---
    logs = sub.add_parser("logs", help="Show logs of last run")
    logs.add_argument("workflow_name", help="Workflow name")

    # --- wait ---
    wait = sub.add_parser("wait", help="Wait for workflow to complete")
    wait.add_argument("workflow_name", help="Workflow name")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        print("\nAvailable workflows:")
        print("  fetch-papers       Fetch researcher papers (PuRe → OpenAlex)")
        print("  fetch-fulltext     Fetch OA full texts via Unpaywall (L2 → L3)")
        print("  fetch-mpg-fulltext Fetch full texts from MPG PuRe (L2 → L3)")
        print("  enrich-abstracts   Enrich papers with abstracts (OpenAlex)")
        print("  pipeline           Full pipeline: fetch + enrich")
        print("  status <workflow>  Show recent run status")
        print("  logs <workflow>    Show logs of last run")
        print("  wait <workflow>    Wait for completion (polls every 15s)")
        sys.exit(0)

    commands = {
        "fetch-papers": trigger_fetch_papers,
        "fetch-fulltext": trigger_fetch_fulltext,
        "fetch-mpg-fulltext": trigger_fetch_mpg_fulltext,
        "enrich-abstracts": trigger_enrich_abstracts,
        "pipeline": trigger_pipeline,
        "status": show_status,
        "logs": show_logs,
        "wait": wait_for_run,
    }

    # Auto-load GH token before any command
    ensure_gh_token()

    handler = commands.get(args.command)
    if handler:
        handler(args)
    else:
        print(f"Unknown command: {args.command}")
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
