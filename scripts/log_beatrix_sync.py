#!/usr/bin/env python3
"""
BEATRIX Sync Logger
====================

Schreibt Sync-Events in data/beatrix/sync-log.yaml.

Wird aufgerufen von:
  1. GitHub Action (sync-beatrix.yml) — automatisch nach Deploy
  2. Backend (server.py) — nach Seed-Reload
  3. Manuell — für Korrekturen/Nachträge

Usage:
    # Automatisch (aus GitHub Action):
    python scripts/log_beatrix_sync.py \\
        --trigger push \\
        --source github_action \\
        --commit abc1234 \\
        --message "feat: Update bcm.yaml" \\
        --branch main \\
        --files "data/knowledge/canonical/bcm.yaml,data/knowledge/canonical/ebf.yaml" \\
        --deploy-status success

    # Backend meldet Seed-Load:
    python scripts/log_beatrix_sync.py \\
        --trigger startup \\
        --source backend \\
        --deploy-status success \\
        --notes "12 seeds loaded in 3.2s"

    # Status anzeigen:
    python scripts/log_beatrix_sync.py --status

    # Letzte N Einträge:
    python scripts/log_beatrix_sync.py --tail 5

    # JSON für API:
    python scripts/log_beatrix_sync.py --status --json
"""

import os
import sys
import json
import hashlib
import argparse
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SYNC_LOG_PATH = REPO_ROOT / "data" / "beatrix" / "sync-log.yaml"
MANIFEST_PATH = REPO_ROOT / "data" / "beatrix" / "seed-manifest.yaml"


# =============================================================================
# YAML HELPERS (no PyYAML dependency)
# =============================================================================

def read_sync_log():
    """Read sync-log.yaml and return list of entries."""
    if not SYNC_LOG_PATH.exists():
        return []

    entries = []
    current_entry = {}
    current_list_key = None
    current_list_item = {}
    in_entries = False

    for line in SYNC_LOG_PATH.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()

        # Skip comments and blanks
        if not stripped or stripped.startswith("#"):
            continue

        # Detect entries section
        if stripped == "entries:":
            in_entries = True
            continue

        if not in_entries:
            continue

        # New top-level entry
        if line.startswith("  - id:"):
            if current_entry:
                entries.append(current_entry)
            current_entry = {"id": stripped.split(":", 1)[1].strip().strip('"')}
            current_list_key = None
            continue

        # Skip if no current entry
        if not current_entry:
            continue

        # Nested list item (seeds_affected, files_changed)
        if line.startswith("      - path:") and current_list_key == "seeds_affected":
            if current_list_item:
                current_entry.setdefault("seeds_affected", []).append(current_list_item)
            current_list_item = {"path": stripped.split(":", 1)[1].strip().strip('"')}
            continue

        if line.startswith("      - ") and current_list_key == "files_changed":
            val = stripped.lstrip("- ").strip().strip('"')
            current_entry.setdefault("files_changed", []).append(val)
            continue

        # Seed sub-fields
        if line.startswith("        ") and current_list_key == "seeds_affected" and current_list_item:
            if ":" in stripped:
                k, v = stripped.split(":", 1)
                current_list_item[k.strip()] = v.strip().strip('"')
            continue

        # Top-level fields
        if line.startswith("    ") and not line.startswith("      "):
            if ":" in stripped:
                k, v = stripped.split(":", 1)
                k = k.strip()
                v = v.strip().strip('"')

                # List markers
                if k in ("files_changed", "seeds_affected") and not v:
                    current_list_key = k
                    if current_list_item and current_list_key == "seeds_affected":
                        current_entry.setdefault("seeds_affected", []).append(current_list_item)
                        current_list_item = {}
                    continue

                # Nested objects (deploy, verification)
                if not v:
                    current_list_key = None
                    continue

                # Convert booleans and nulls
                if v == "true":
                    v = True
                elif v == "false":
                    v = False
                elif v == "null":
                    v = None

                current_entry[k] = v
                current_list_key = None

    # Flush last entry
    if current_list_item and current_entry:
        current_entry.setdefault("seeds_affected", []).append(current_list_item)
    if current_entry:
        entries.append(current_entry)

    return entries


def get_next_id(entries):
    """Get next SYNC-NNN id."""
    max_n = 0
    for e in entries:
        eid = e.get("id", "")
        if eid.startswith("SYNC-"):
            try:
                n = int(eid.split("-")[1])
                max_n = max(max_n, n)
            except (ValueError, IndexError):
                pass
    return f"SYNC-{max_n + 1:03d}"


def compute_file_hash(filepath):
    """SHA-256 hash of file content."""
    p = REPO_ROOT / filepath
    if not p.exists():
        return None
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_manifest_hashes():
    """Load current manifest hashes as dict {path: sha256}."""
    hashes = {}
    if not MANIFEST_PATH.exists():
        return hashes

    current_path = None
    for line in MANIFEST_PATH.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("- path:"):
            current_path = stripped.split(":", 1)[1].strip().strip('"')
        elif stripped.startswith("sha256:") and current_path:
            hashes[current_path] = stripped.split(":", 1)[1].strip().strip('"')
            current_path = None
    return hashes


def append_entry_to_log(entry):
    """Append a new entry to sync-log.yaml."""
    lines = []
    lines.append("")
    lines.append(f'  - id: "{entry["id"]}"')
    lines.append(f'    timestamp: "{entry["timestamp"]}"')
    lines.append(f'    trigger: "{entry["trigger"]}"')
    lines.append(f'    source: "{entry["source"]}"')

    if entry.get("commit_sha"):
        lines.append(f'    commit_sha: "{entry["commit_sha"]}"')
    if entry.get("commit_message"):
        lines.append(f'    commit_message: "{entry["commit_message"]}"')
    if entry.get("branch"):
        lines.append(f'    branch: "{entry["branch"]}"')

    # files_changed
    if entry.get("files_changed"):
        lines.append("    files_changed:")
        for f in entry["files_changed"]:
            lines.append(f'      - "{f}"')

    # seeds_affected
    if entry.get("seeds_affected"):
        lines.append("    seeds_affected:")
        for s in entry["seeds_affected"]:
            lines.append(f'      - path: "{s["path"]}"')
            lines.append(f'        old_hash: "{s.get("old_hash", "unknown")}"')
            lines.append(f'        new_hash: "{s.get("new_hash", "unknown")}"')
            lines.append(f'        status: "{s.get("status", "updated")}"')

    # deploy
    lines.append("    deploy:")
    lines.append(f'      triggered: {str(entry.get("deploy_triggered", True)).lower()}')
    lines.append(f'      target: "{entry.get("deploy_target", "railway")}"')
    lines.append(f'      status: "{entry.get("deploy_status", "pending")}"')
    dur = entry.get("deploy_duration_s")
    lines.append(f'      duration_s: {dur if dur else "null"}')

    # verification
    lines.append("    verification:")
    lines.append(f'      manifest_regenerated: {str(entry.get("manifest_regenerated", False)).lower()}')
    lines.append(f'      all_hashes_match: {str(entry.get("all_hashes_match", False)).lower()}')

    # notes
    if entry.get("notes"):
        lines.append(f'    notes: "{entry["notes"]}"')

    # Append to file
    content = SYNC_LOG_PATH.read_text(encoding="utf-8")
    content += "\n".join(lines) + "\n"
    SYNC_LOG_PATH.write_text(content, encoding="utf-8")

    return entry["id"]


# =============================================================================
# COMMANDS
# =============================================================================

def cmd_status(as_json=False):
    """Show sync log status."""
    entries = read_sync_log()

    if as_json:
        summary = {
            "total_syncs": len(entries),
            "last_sync": entries[-1] if entries else None,
            "by_source": {},
            "by_status": {},
        }
        for e in entries:
            src = e.get("source", "unknown")
            summary["by_source"][src] = summary["by_source"].get(src, 0) + 1
            st = e.get("deploy_status", e.get("status", "unknown"))
            summary["by_status"][st] = summary["by_status"].get(st, 0) + 1
        print(json.dumps(summary, indent=2, default=str))
        return

    print("=" * 70)
    print("  BEATRIX SYNC LOG STATUS")
    print("=" * 70)
    print(f"  Total Sync Events:  {len(entries)}")

    if entries:
        last = entries[-1]
        print(f"  Last Sync:          {last.get('id')} ({last.get('timestamp', '?')})")
        print(f"  Last Trigger:       {last.get('trigger', '?')}")
        print(f"  Last Source:        {last.get('source', '?')}")
        print(f"  Last Status:        {last.get('deploy_status', '?')}")

    # Count by source
    by_source = {}
    by_status = {}
    for e in entries:
        src = e.get("source", "unknown")
        by_source[src] = by_source.get(src, 0) + 1
        st = e.get("deploy_status", e.get("status", "unknown"))
        by_status[st] = by_status.get(st, 0) + 1

    if by_source:
        print(f"\n  By Source:")
        for src, count in sorted(by_source.items()):
            print(f"    {src:20s} {count}")

    if by_status:
        print(f"\n  By Deploy Status:")
        for st, count in sorted(by_status.items()):
            print(f"    {st:20s} {count}")

    print("=" * 70)


def cmd_tail(n=5):
    """Show last N entries."""
    entries = read_sync_log()
    recent = entries[-n:] if len(entries) >= n else entries

    for e in recent:
        status_icon = {"success": "OK", "failed": "FAIL", "skipped": "SKIP", "pending": "..."}.get(
            e.get("deploy_status", "?"), "?"
        )
        files = e.get("files_changed", [])
        file_str = f"{len(files)} file(s)" if files else "no files"
        print(f"  [{status_icon:4s}] {e.get('id', '?'):10s}  {e.get('timestamp', '?')[:19]}  "
              f"{e.get('trigger', '?'):10s}  {e.get('source', '?'):15s}  {file_str}")


def cmd_log(args):
    """Add a new sync log entry."""
    entries = read_sync_log()
    entry_id = get_next_id(entries)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Parse files
    files_changed = []
    if args.files:
        files_changed = [f.strip() for f in args.files.split(",") if f.strip()]

    # Compute seed hashes
    manifest_hashes = load_manifest_hashes()
    seeds_affected = []
    for f in files_changed:
        old_hash = manifest_hashes.get(f, "unknown")
        new_hash = compute_file_hash(f) or "unknown"
        status = "unchanged" if old_hash == new_hash else "updated"
        if old_hash == "unknown":
            status = "new"
        seeds_affected.append({
            "path": f,
            "old_hash": old_hash,
            "new_hash": new_hash,
            "status": status,
        })

    entry = {
        "id": entry_id,
        "timestamp": now,
        "trigger": args.trigger,
        "source": args.source,
        "commit_sha": args.commit or "",
        "commit_message": args.message or "",
        "branch": args.branch or "main",
        "files_changed": files_changed,
        "seeds_affected": seeds_affected,
        "deploy_triggered": args.deploy_status != "skipped",
        "deploy_target": "railway",
        "deploy_status": args.deploy_status,
        "deploy_duration_s": args.duration,
        "manifest_regenerated": args.manifest_regenerated,
        "all_hashes_match": args.hashes_match,
        "notes": args.notes or "",
    }

    written_id = append_entry_to_log(entry)
    print(f"Sync event logged: {written_id}")
    print(f"  Trigger:  {args.trigger}")
    print(f"  Source:   {args.source}")
    print(f"  Files:    {len(files_changed)}")
    print(f"  Seeds:    {len(seeds_affected)}")
    print(f"  Deploy:   {args.deploy_status}")

    return written_id


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="BEATRIX Sync Logger — Protokolliert Sync-Events"
    )

    # Mode selection
    parser.add_argument("--status", action="store_true",
                        help="Zeige Sync-Log Status")
    parser.add_argument("--tail", type=int, metavar="N",
                        help="Zeige letzte N Einträge")
    parser.add_argument("--json", action="store_true",
                        help="JSON-Ausgabe (für API)")

    # Log entry fields
    parser.add_argument("--trigger", choices=["push", "manual", "redeploy", "startup"],
                        help="Was hat den Sync ausgelöst?")
    parser.add_argument("--source", choices=["github_action", "backend", "manual"],
                        help="Wer loggt? (github_action, backend, manual)")
    parser.add_argument("--commit", type=str,
                        help="Git Commit SHA")
    parser.add_argument("--message", type=str,
                        help="Commit Message (erste Zeile)")
    parser.add_argument("--branch", type=str, default="main",
                        help="Branch (default: main)")
    parser.add_argument("--files", type=str,
                        help="Geänderte Dateien (kommagetrennt)")
    parser.add_argument("--deploy-status", choices=["success", "failed", "pending", "skipped"],
                        default="pending",
                        help="Deploy-Status")
    parser.add_argument("--duration", type=float,
                        help="Deploy-Dauer in Sekunden")
    parser.add_argument("--manifest-regenerated", action="store_true",
                        help="Wurde Manifest neu generiert?")
    parser.add_argument("--hashes-match", action="store_true",
                        help="Stimmen alle Hashes überein?")
    parser.add_argument("--notes", type=str,
                        help="Optionale Bemerkungen")

    args = parser.parse_args()

    # Dispatch
    if args.status:
        cmd_status(as_json=args.json)
    elif args.tail is not None:
        cmd_tail(args.tail)
    elif args.trigger and args.source:
        cmd_log(args)
    else:
        parser.print_help()
        print("\nBeispiele:")
        print("  python scripts/log_beatrix_sync.py --status")
        print("  python scripts/log_beatrix_sync.py --tail 5")
        print('  python scripts/log_beatrix_sync.py --trigger push --source github_action '
              '--commit abc123 --files "data/knowledge/canonical/bcm.yaml" '
              '--deploy-status success')


if __name__ == "__main__":
    main()
