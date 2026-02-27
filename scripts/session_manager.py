#!/usr/bin/env python3
"""
Session Manager for EBF Framework
=================================

Automatisches Session-Tracking für User-Behavior-Learning.

Features:
- Superkey-Generierung
- Session-Dokumentation
- Learning-Extraktion
- User-Identifikation

Usage:
    python scripts/session_manager.py start --domain ORG --user FA-VR-001
    python scripts/session_manager.py end
    python scripts/session_manager.py status
    python scripts/session_manager.py learn --pattern all
"""

import argparse
import yaml
import os
from datetime import datetime
from pathlib import Path
import sys

# Paths
REPO_ROOT = Path(__file__).parent.parent
SESSION_DB = REPO_ROOT / "data" / "model-building-session.yaml"
TEAM_DB = REPO_ROOT / "data" / "fehradvice" / "team.yaml"
CURRENT_SESSION = REPO_ROOT / ".claude" / "current-session.yaml"

# Domain mappings
DOMAINS = {
    "REL": "Religion",
    "FIN": "Finance",
    "HLT": "Health",
    "ENV": "Environment",
    "POL": "Policy",
    "ORG": "Organization",
    "EDU": "Education",
    "INT": "Internal",
    "OTH": "Other"
}


def load_yaml(path: Path) -> dict:
    """Load YAML file."""
    if not path.exists():
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f) or {}


def save_yaml(path: Path, data: dict):
    """Save YAML file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def get_next_sequence(domain: str) -> int:
    """Get next sequence number for today's sessions in given domain."""
    today = datetime.now().strftime("%Y-%m-%d")
    session_db = load_yaml(SESSION_DB)
    sessions = session_db.get("sessions", [])

    count = 0
    for s in sessions:
        sid = s.get("id", s.get("session_id", ""))
        if f"-{today.replace('-', '-')}-{domain}-" in sid:
            count += 1

    return count + 1


def generate_superkey(domain: str) -> str:
    """Generate session superkey."""
    today = datetime.now().strftime("%Y-%m-%d")
    seq = get_next_sequence(domain)
    return f"EBF-S-{today}-{domain}-{seq:03d}"


def lookup_user(user_id: str = None, name: str = None) -> dict:
    """Lookup user in team database."""
    team_db = load_yaml(TEAM_DB)

    # Search in all sections
    for section in ["board", "management", "team", "alumni"]:
        members = team_db.get(section, [])
        for member in members:
            if user_id and member.get("id") == user_id:
                return member
            if name:
                full_name = f"{member.get('name', {}).get('first', '')} {member.get('name', {}).get('last', '')}".strip()
                if name.lower() in full_name.lower():
                    return member

    return {}


def start_session(domain: str = "OTH", user_id: str = None, user_name: str = None) -> dict:
    """Start a new session."""
    # Generate superkey
    superkey = generate_superkey(domain)

    # Lookup user
    user = {}
    if user_id:
        user = lookup_user(user_id=user_id)
    elif user_name:
        user = lookup_user(name=user_name)

    # Create session
    session = {
        "session_id": superkey,
        "domain": domain,
        "domain_name": DOMAINS.get(domain, "Other"),
        "started": datetime.now().isoformat(),
        "status": "ACTIVE",
        "user": {
            "id": user.get("id", "UNKNOWN"),
            "name": f"{user.get('name', {}).get('first', '')} {user.get('name', {}).get('last', '')}".strip() or "Unknown User",
            "role": user.get("title", user.get("role", ""))
        },
        "narrative": [],
        "outputs_created": [],
        "learnings": []
    }

    # Save current session
    save_yaml(CURRENT_SESSION, session)

    return session


def add_narrative(step: int, user_input: str, interpretation: str = None,
                  correction: bool = False, learning: str = None):
    """Add narrative step to current session."""
    if not CURRENT_SESSION.exists():
        print("ERROR: No active session. Run 'start' first.", file=sys.stderr)
        return

    session = load_yaml(CURRENT_SESSION)

    narrative_entry = {
        "step": step,
        "timestamp": datetime.now().isoformat(),
        "user_input": user_input
    }

    if interpretation:
        narrative_entry["interpretation"] = interpretation
    if correction:
        narrative_entry["correction"] = True
    if learning:
        narrative_entry["learning"] = learning

    session["narrative"].append(narrative_entry)
    save_yaml(CURRENT_SESSION, session)


def add_output(path: str, output_type: str, description: str = None):
    """Add created output to current session."""
    if not CURRENT_SESSION.exists():
        return

    session = load_yaml(CURRENT_SESSION)
    session["outputs_created"].append({
        "path": path,
        "type": output_type,
        "description": description,
        "timestamp": datetime.now().isoformat()
    })
    save_yaml(CURRENT_SESSION, session)


def end_session() -> dict:
    """End current session and save to database."""
    if not CURRENT_SESSION.exists():
        print("ERROR: No active session.", file=sys.stderr)
        return {}

    session = load_yaml(CURRENT_SESSION)
    session["status"] = "COMPLETED"
    session["ended"] = datetime.now().isoformat()

    # Extract learnings
    learnings = extract_learnings(session)
    session["session_learnings"] = learnings

    # Load session database
    session_db = load_yaml(SESSION_DB)
    if "sessions" not in session_db:
        session_db["sessions"] = []

    # Convert to database format
    db_entry = {
        "id": session["session_id"],
        "date": session["started"][:10],
        "timestamp": session["started"],
        "domain": session["domain"],
        "mode": "OPERATIONAL",
        "user": session["user"],
        "context": {
            "session_type": "OPERATIONAL",
            "triggers_detected": []
        },
        "session_narrative": session["narrative"],
        "outputs": session["outputs_created"],
        "session_learnings": learnings,
        "status": "COMPLETED"
    }

    # Add to sessions
    session_db["sessions"].append(db_entry)

    # Update metadata
    session_db["metadata"]["total_sessions"] = len(session_db["sessions"])
    session_db["metadata"]["last_updated"] = datetime.now().strftime("%Y-%m-%d")

    # Save
    save_yaml(SESSION_DB, session_db)

    # Remove current session file
    CURRENT_SESSION.unlink()

    return session


def extract_learnings(session: dict) -> dict:
    """Extract learnings from session narrative."""
    learnings = {
        "user_behavior_patterns": [],
        "corrections_made": [],
        "recommendations_for_future": []
    }

    for entry in session.get("narrative", []):
        if entry.get("correction"):
            learnings["corrections_made"].append({
                "step": entry["step"],
                "original": entry.get("interpretation", ""),
                "corrected_by": entry["user_input"],
                "learning": entry.get("learning", "User korrigierte Interpretation")
            })

        if entry.get("learning"):
            learnings["recommendations_for_future"].append(entry["learning"])

    # Deduplicate recommendations
    learnings["recommendations_for_future"] = list(set(learnings["recommendations_for_future"]))

    return learnings


def get_status() -> dict:
    """Get current session status."""
    if not CURRENT_SESSION.exists():
        return {"status": "NO_ACTIVE_SESSION"}

    return load_yaml(CURRENT_SESSION)


def get_learnings(pattern_type: str = "all", user_id: str = None) -> list:
    """Get learnings from all sessions."""
    session_db = load_yaml(SESSION_DB)
    learnings = []

    for session in session_db.get("sessions", []):
        # Filter by user if specified
        if user_id and session.get("user", {}).get("id") != user_id:
            continue

        session_learnings = session.get("session_learnings", {})

        if pattern_type == "all" or pattern_type == "behavior":
            learnings.extend(session_learnings.get("user_behavior_patterns", []))

        if pattern_type == "all" or pattern_type == "corrections":
            learnings.extend(session_learnings.get("corrections_made", []))

        if pattern_type == "all" or pattern_type == "recommendations":
            for rec in session_learnings.get("recommendations_for_future", []):
                learnings.append({"recommendation": rec, "session": session.get("id")})

    return learnings


def autosave_session(interval_minutes: int = 30, auto_end_hour: int = 22) -> str:
    """
    Auto-save session if interval has passed since last save.
    Also ends session automatically at specified hour (default: 22:00).

    Returns:
        "saved" - if autosave performed
        "ended" - if session auto-ended
        "skipped" - if no action needed
        "no_session" - if no active session
    """
    if not CURRENT_SESSION.exists():
        return "no_session"

    session = load_yaml(CURRENT_SESSION)
    now = datetime.now()

    # Check if it's time for auto-end (22:00 or later)
    if now.hour >= auto_end_hour:
        # Check if session started today before auto-end hour
        started = datetime.fromisoformat(session["started"].replace("+01:00", "").replace("+00:00", ""))
        if started.date() == now.date() and started.hour < auto_end_hour:
            # End the session
            end_session()
            return "ended"

    # Check last save time
    last_save = session.get("last_autosave")

    if last_save:
        last_save_time = datetime.fromisoformat(last_save)
        minutes_since_save = (now - last_save_time).total_seconds() / 60

        if minutes_since_save < interval_minutes:
            return "skipped"  # Not time yet

    # Perform autosave
    session["last_autosave"] = now.isoformat()
    session["autosave_count"] = session.get("autosave_count", 0) + 1

    # Save to current session file
    save_yaml(CURRENT_SESSION, session)

    # Also save a backup snapshot to the database (without ending session)
    save_session_snapshot(session)

    return "saved"


def save_session_snapshot(session: dict):
    """Save a snapshot of current session to database without ending it."""
    session_db = load_yaml(SESSION_DB)

    # Look for existing entry with same ID
    session_id = session["session_id"]
    existing_idx = None

    for idx, s in enumerate(session_db.get("sessions", [])):
        if s.get("id") == session_id or s.get("session_id") == session_id:
            existing_idx = idx
            break

    # Create snapshot entry
    snapshot = {
        "id": session_id,
        "date": session["started"][:10],
        "timestamp": session["started"],
        "domain": session["domain"],
        "mode": "OPERATIONAL",
        "user": session["user"],
        "context": {
            "session_type": "OPERATIONAL",
            "triggers_detected": []
        },
        "session_narrative": session.get("narrative", []),
        "outputs": session.get("outputs_created", []),
        "status": "IN_PROGRESS",
        "last_autosave": session.get("last_autosave"),
        "autosave_count": session.get("autosave_count", 0)
    }

    if existing_idx is not None:
        # Update existing entry
        session_db["sessions"][existing_idx] = snapshot
    else:
        # Add new entry
        if "sessions" not in session_db:
            session_db["sessions"] = []
        session_db["sessions"].append(snapshot)

    # Update metadata
    session_db["metadata"]["last_updated"] = datetime.now().strftime("%Y-%m-%d")

    # Save
    save_yaml(SESSION_DB, session_db)


def print_session_box(session: dict):
    """Print session info box."""
    print("┌─────────────────────────────────────────────────────────────────┐")
    print("│  🚀 SESSION GESTARTET                                           │")
    print("├─────────────────────────────────────────────────────────────────┤")
    print(f"│  Superkey:  {session['session_id']:<40}     │")
    print(f"│  User:      {session['user']['name']:<40}     │")
    print(f"│  Domain:    {session['domain']} ({session['domain_name']:<30})     │")
    print(f"│  Start:     {session['started']:<40}     │")
    print("│                                                                 │")
    print("│  Diese Session wird automatisch dokumentiert.                   │")
    print("│  Auto-Save: alle 30 Minuten                                    │")
    print("│  Am Ende: /session end                                         │")
    print("└─────────────────────────────────────────────────────────────────┘")


def main():
    parser = argparse.ArgumentParser(description="EBF Session Manager")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Start command
    start_parser = subparsers.add_parser("start", help="Start new session")
    start_parser.add_argument("--domain", default="OTH", choices=list(DOMAINS.keys()))
    start_parser.add_argument("--user", help="User ID (e.g., FA-VR-001)")
    start_parser.add_argument("--name", help="User name")

    # End command
    subparsers.add_parser("end", help="End current session")

    # Status command
    subparsers.add_parser("status", help="Show session status")

    # Learn command
    learn_parser = subparsers.add_parser("learn", help="Show learnings")
    learn_parser.add_argument("--pattern", default="all",
                              choices=["all", "behavior", "corrections", "recommendations"])
    learn_parser.add_argument("--user", help="Filter by user ID")

    # Add narrative command
    narrative_parser = subparsers.add_parser("narrative", help="Add narrative entry")
    narrative_parser.add_argument("--step", type=int, required=True)
    narrative_parser.add_argument("--input", required=True)
    narrative_parser.add_argument("--interpretation")
    narrative_parser.add_argument("--correction", action="store_true")
    narrative_parser.add_argument("--learning")

    # Add output command
    output_parser = subparsers.add_parser("output", help="Add output entry")
    output_parser.add_argument("--path", required=True)
    output_parser.add_argument("--type", required=True)
    output_parser.add_argument("--description")

    # Autosave command (called by hook)
    autosave_parser = subparsers.add_parser("autosave", help="Auto-save if interval passed")
    autosave_parser.add_argument("--interval", type=int, default=30,
                                  help="Minutes between auto-saves (default: 30)")

    args = parser.parse_args()

    if args.command == "start":
        session = start_session(args.domain, args.user, args.name)
        print_session_box(session)

    elif args.command == "end":
        session = end_session()
        if session:
            print(f"✅ Session {session['session_id']} beendet und gespeichert.")
            print(f"   Learnings extrahiert: {len(session.get('session_learnings', {}).get('recommendations_for_future', []))}")

    elif args.command == "status":
        status = get_status()
        if status.get("status") == "NO_ACTIVE_SESSION":
            print("ℹ️  Keine aktive Session.")
        else:
            print(f"📍 Aktive Session: {status['session_id']}")
            print(f"   User: {status['user']['name']}")
            print(f"   Domain: {status['domain']}")
            print(f"   Narrative Steps: {len(status.get('narrative', []))}")

    elif args.command == "learn":
        learnings = get_learnings(args.pattern, args.user)
        print(f"📚 Learnings ({len(learnings)} gefunden):")
        for i, l in enumerate(learnings[:10], 1):
            if "recommendation" in l:
                print(f"   {i}. {l['recommendation']}")
            elif "learning" in l:
                print(f"   {i}. {l['learning']}")

    elif args.command == "narrative":
        add_narrative(args.step, args.input, args.interpretation,
                      args.correction, args.learning)
        print(f"✅ Narrative Step {args.step} hinzugefügt.")

    elif args.command == "output":
        add_output(args.path, args.type, args.description)
        print(f"✅ Output hinzugefügt: {args.path}")

    elif args.command == "autosave":
        result = autosave_session(args.interval)
        if result == "saved":
            session = load_yaml(CURRENT_SESSION)
            print(f"💾 Auto-Save #{session.get('autosave_count', 1)}: {session['session_id']}", file=sys.stderr)
        elif result == "ended":
            print(f"🌙 Session automatisch beendet (22:00 Uhr)", file=sys.stderr)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
