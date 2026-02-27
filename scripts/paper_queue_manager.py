#!/usr/bin/env python3
"""
Paper Integration Queue Manager

Verwaltet die Queue unvollständiger Paper-Integrationen und
ermöglicht automatisches Abarbeiten.

2D Classification System:
    content_level (0/1/2):     WAS wir haben
        0 = METADATA ONLY      (nur BibTeX-Referenz)
        1 = ABSTRACT           (BibTeX + Abstract + Key Findings)
        2 = FULL-TEXT          (BibTeX + Abstract + Vollständiger Paper-Text)

    integration_level (1-5):   WIE tief in EBF integriert
        1 = MINIMAL            (nur BibTeX)
        2 = STANDARD           (BibTeX + theory_support + use_for)
        3 = CASE               (+ Case Registry Eintrag)
        4 = THEORY             (+ Theory Catalog Eintrag)
        5 = FULL               (+ Appendix, alles)

Usage:
    python scripts/paper_queue_manager.py --status          # Queue-Status anzeigen
    python scripts/paper_queue_manager.py --add PAP-xxx     # Paper zur Queue hinzufügen
    python scripts/paper_queue_manager.py --next            # Nächstes Paper anzeigen
    python scripts/paper_queue_manager.py --complete PAP-xxx # Paper als fertig markieren
    python scripts/paper_queue_manager.py --list            # Alle pending Papers
    python scripts/paper_queue_manager.py --upgrade-schema  # Migrate to 2D system
"""

import os
import sys
import yaml
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
QUEUE_FILE = ROOT / "data" / "paper-integration-queue.yaml"
VALIDATE_SCRIPT = ROOT / "scripts" / "validate_paper_integration.py"
PAPERS_DIR = ROOT / "papers" / "evaluated" / "integrated"

# Content level descriptions
CONTENT_LEVELS = {
    0: "METADATA ONLY (nur BibTeX)",
    1: "ABSTRACT (BibTeX + Abstract + Key Findings)",
    2: "FULL-TEXT (komplett)"
}

# Integration level descriptions
INTEGRATION_LEVELS = {
    1: "MINIMAL (nur BibTeX)",
    2: "STANDARD (+ theory_support, use_for)",
    3: "CASE (+ Case Registry)",
    4: "THEORY (+ Theory Catalog)",
    5: "FULL (+ Appendix)"
}


def load_queue() -> dict:
    """Load queue from YAML file."""
    if not QUEUE_FILE.exists():
        return {
            "queue_version": "1.0",
            "config": {
                "papers_per_session": 1,
                "auto_complete_on_startup": True,
                "priority_order": "oldest_first"
            },
            "stats": {
                "total_queued": 0,
                "total_completed": 0
            },
            "pending": [],
            "completed": []
        }

    with open(QUEUE_FILE) as f:
        return yaml.safe_load(f) or {}


def save_queue(queue: dict):
    """Save queue to YAML file."""
    queue["last_updated"] = datetime.now().strftime("%Y-%m-%d")
    with open(QUEUE_FILE, "w") as f:
        yaml.dump(queue, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def get_missing_components(paper_id: str) -> list:
    """Get list of missing components for a paper."""
    import subprocess

    try:
        result = subprocess.run(
            ["python", str(VALIDATE_SCRIPT), paper_id],
            capture_output=True,
            text=True,
            cwd=str(ROOT)
        )

        missing = []
        in_missing = False
        for line in result.stdout.split("\n"):
            if "Missing components:" in line:
                in_missing = True
                continue
            if in_missing:
                if line.strip().startswith("-"):
                    missing.append(line.strip().lstrip("- "))
                elif line.strip() and not line.startswith(" "):
                    break

        return missing
    except Exception:
        return ["unknown"]


def get_paper_level(paper_id: str) -> int:
    """Get integration level from PIP file."""
    pip_dir = ROOT / "data" / "paper-intake"

    for pip_file in pip_dir.rglob("*.yaml"):
        if pip_file.name == "template.yaml":
            continue
        try:
            with open(pip_file) as f:
                pip = yaml.safe_load(f)
            if pip and pip.get("paper_id") == paper_id:
                return pip.get("ebf_integration", {}).get("integration_level", 1)
        except Exception:
            continue

    return 1


def check_full_text_available(paper_id: str) -> bool:
    """Check if full text file exists for a paper."""
    txt_file = PAPERS_DIR / f"{paper_id}.txt"
    return txt_file.exists()


def determine_content_level(paper_id: str) -> int:
    """
    Determine content level (0/1/2) for a paper based on actual file content.

    Returns:
        0 = METADATA ONLY (no file or just placeholder)
        1 = ABSTRACT (file has abstract and key findings)
        2 = FULL-TEXT (file has complete paper text)
    """
    txt_file = PAPERS_DIR / f"{paper_id}.txt"

    if not txt_file.exists():
        return 0

    try:
        content = txt_file.read_text(encoding='utf-8')
        content_lower = content.lower()

        # Quick checks for placeholders
        if '[abstract will be added]' in content_lower or 'placeholder' in content_lower:
            return 0

        # Check file size - very large files are likely full-text
        if len(content) > 15000:
            return 2

        # Look for ABSTRACT section with content (multiple formats)
        # Format 1: With === separators
        abstract_match = re.search(
            r'={10,}\s*\n\s*ABSTRACT\s*\n\s*={10,}\s*\n(.*?)(?:={10,}|$)',
            content,
            re.IGNORECASE | re.DOTALL
        )

        # Format 2: Simple ABSTRACT header (without separators)
        # Captures until next major section (all caps header) or file end
        if not abstract_match:
            abstract_match = re.search(
                r'^ABSTRACT\s*\n\n?(.*?)(?=\n\n[A-Z][A-Z _-]{3,}\n|\Z)',
                content,
                re.IGNORECASE | re.DOTALL | re.MULTILINE
            )

        if abstract_match:
            abstract_text = abstract_match.group(1).strip()
            # Remove empty lines and count meaningful content
            abstract_lines = [l.strip() for l in abstract_text.split('\n') if l.strip()]
            abstract_chars = len(' '.join(abstract_lines))

            # Check for KEY FINDINGS or similar section (indicates Level 1 at minimum)
            key_sections = ['KEY FINDINGS', 'KEY THEMES', 'KEY CONTRIBUTIONS',
                           'METHODOLOGICAL CONTRIBUTION', 'CONTRIBUTION',
                           'EBF RELEVANCE', 'SOURCES']
            has_key_section = any(s in content.upper() for s in key_sections)

            # Level 1: Has meaningful abstract (>100 chars of real content)
            if abstract_chars > 100 and has_key_section:
                # Check for full-text indicators (Level 2)
                full_text_sections = ['INTRODUCTION', 'LITERATURE REVIEW', 'DATA AND METHODS',
                                     'EMPIRICAL RESULTS', 'CONCLUSION', 'REFERENCES']
                section_count = sum(1 for s in full_text_sections if s in content.upper())

                if section_count >= 3 and len(content) > 8000:
                    return 2

                return 1

        # Level 0: No meaningful abstract found
        return 0

    except Exception as e:
        return 0


def get_content_level_icon(level: int) -> str:
    """Get emoji icon for content level."""
    icons = {0: "📋", 1: "📄", 2: "📚"}
    return icons.get(level, "❓")


def add_to_queue(paper_id: str, missing: list = None, priority: str = None) -> bool:
    """Add a paper to the queue with 2D classification (content_level × integration_level)."""
    queue = load_queue()

    # Check if already in queue
    for item in queue.get("pending", []):
        if item.get("paper_id") == paper_id:
            # Update missing components and content_level
            if missing:
                item["missing"] = missing
            # Always update content_level when re-checking
            item["content_level"] = determine_content_level(paper_id)
            save_queue(queue)
            return False  # Already exists

    # Get missing components if not provided
    if not missing:
        missing = get_missing_components(paper_id)

    if not missing:
        return False  # Paper is complete

    # 2D Classification
    content_level = determine_content_level(paper_id)
    integration_level = get_paper_level(paper_id)

    # Auto-set priority based on content level if not specified
    # Higher content = higher priority (we can do more with it)
    if priority is None:
        if content_level >= 1:
            priority = "high"
        else:
            priority = "normal"

    # Add to queue with 2D classification
    queue.setdefault("pending", []).append({
        "paper_id": paper_id,
        "added": datetime.now().isoformat(),
        # 2D Classification
        "content_level": content_level,        # 0/1/2: WHAT we have
        "integration_level": integration_level, # 1-5: HOW deep integrated
        # Legacy fields (for backwards compatibility)
        "level": integration_level,
        "has_full_text": content_level >= 1,
        "track": "A" if content_level >= 1 else "B",
        # Other fields
        "missing": missing,
        "priority": priority,
        "attempts": 0
    })

    queue["stats"]["total_queued"] = queue["stats"].get("total_queued", 0) + 1

    save_queue(queue)
    return True


def get_prior_score(paper_id: str) -> float:
    """Get prior score π(p) from paper YAML."""
    yaml_path = ROOT / "data" / "paper-references" / f"{paper_id}.yaml"
    if not yaml_path.exists():
        # Try with PAP- prefix
        yaml_path = ROOT / "data" / "paper-references" / f"PAP-{paper_id}.yaml"
    if not yaml_path.exists():
        return 0.0
    try:
        with open(yaml_path) as f:
            data = yaml.safe_load(f)
        ps = data.get('prior_score', {})
        if isinstance(ps, dict):
            return float(ps.get('prior_score', 0))
        return 0.0
    except Exception:
        return 0.0


def _sort_pending(pending: list, order: str):
    """Sort pending papers by the specified order."""
    priority_map = {"high": 0, "normal": 1, "low": 2}

    if order == "by_prior_score":
        # Sort by π(p) descending — highest-value papers first
        for item in pending:
            if 'cached_prior_score' not in item:
                item['cached_prior_score'] = get_prior_score(item.get('paper_id', ''))
        pending.sort(key=lambda x: -x.get('cached_prior_score', 0))
    elif order == "oldest_first":
        pending.sort(key=lambda x: (priority_map.get(x.get("priority", "normal"), 1), x.get("added", "")))
    elif order == "newest_first":
        pending.sort(key=lambda x: (priority_map.get(x.get("priority", "normal"), 1), x.get("added", "")), reverse=True)
    elif order == "by_level":
        pending.sort(key=lambda x: (priority_map.get(x.get("priority", "normal"), 1), -x.get("level", 1)))


def get_next_paper() -> dict | None:
    """Get the next paper to complete."""
    queue = load_queue()
    pending = queue.get("pending", [])

    if not pending:
        return None

    order = queue.get("config", {}).get("priority_order", "oldest_first")
    _sort_pending(pending, order)

    return pending[0] if pending else None


def mark_complete(paper_id: str) -> bool:
    """Mark a paper as complete and remove from queue."""
    queue = load_queue()

    # Find and remove from pending
    pending = queue.get("pending", [])
    for i, item in enumerate(pending):
        if item.get("paper_id") == paper_id:
            completed_item = pending.pop(i)
            completed_item["completed"] = datetime.now().isoformat()

            # Add to completed list
            queue.setdefault("completed", []).append(completed_item)
            queue["stats"]["total_completed"] = queue["stats"].get("total_completed", 0) + 1

            # Keep only last 50 completed items
            if len(queue["completed"]) > 50:
                queue["completed"] = queue["completed"][-50:]

            save_queue(queue)
            return True

    return False


def increment_attempts(paper_id: str):
    """Increment attempt counter for a paper."""
    queue = load_queue()

    for item in queue.get("pending", []):
        if item.get("paper_id") == paper_id:
            item["attempts"] = item.get("attempts", 0) + 1
            item["last_attempt"] = datetime.now().isoformat()
            save_queue(queue)
            return


def update_queue_tracks():
    """Update all pending papers with has_full_text and track fields."""
    queue = load_queue()
    updated = 0

    for item in queue.get("pending", []):
        paper_id = item.get("paper_id")
        if paper_id:
            has_full_text = check_full_text_available(paper_id)
            if item.get("has_full_text") != has_full_text:
                item["has_full_text"] = has_full_text
                item["track"] = "A" if has_full_text else "B"
                # Update priority based on full text
                if has_full_text and item.get("priority") == "normal":
                    item["priority"] = "high"
                updated += 1

    if updated > 0:
        save_queue(queue)

    return updated


def get_status() -> dict:
    """Get queue status summary."""
    queue = load_queue()
    pending = queue.get("pending", [])

    return {
        "pending_count": len(pending),
        "total_queued": queue.get("stats", {}).get("total_queued", 0),
        "total_completed": queue.get("stats", {}).get("total_completed", 0),
        "config": queue.get("config", {}),
        "next_paper": get_next_paper()
    }


def print_status():
    """Print queue status with 2D classification view."""
    status = get_status()
    queue = load_queue()
    pending = queue.get("pending", [])

    # Count by content_level (new 2D system)
    content_0 = [p for p in pending if p.get("content_level", 0) == 0]
    content_1 = [p for p in pending if p.get("content_level", 0) == 1]
    content_2 = [p for p in pending if p.get("content_level", 0) == 2]

    print("\n" + "="*70)
    print("  PAPER INTEGRATION QUEUE STATUS (2D System)")
    print("="*70)
    print(f"  Pending: {status['pending_count']} papers")
    print(f"  Total queued: {status['total_queued']}")
    print(f"  Total completed: {status['total_completed']}")

    print(f"\n  ┌─────────────────────────────────────────────────────────────┐")
    print(f"  │  2D KLASSIFIKATION: content_level × integration_level      │")
    print(f"  ├─────────────────────────────────────────────────────────────┤")
    print(f"  │  📋 Content 0 (nur Metadata):  {len(content_0):3d} papers               │")
    print(f"  │  📄 Content 1 (mit Abstract):  {len(content_1):3d} papers               │")
    print(f"  │  📚 Content 2 (Full-Text):     {len(content_2):3d} papers               │")
    print(f"  └─────────────────────────────────────────────────────────────┘")

    if status["next_paper"]:
        next_p = status["next_paper"]
        c_lvl = next_p.get("content_level", 0)
        i_lvl = next_p.get("integration_level", next_p.get("level", 1))
        c_icon = get_content_level_icon(c_lvl)
        ps = next_p.get("prior_score", next_p.get("cached_prior_score"))
        print(f"\n  ▶️  Next paper: {next_p['paper_id']}")
        if ps:
            print(f"     📊 Prior Score: π(p) = {ps:.3f}")
        print(f"     {c_icon} Content Level: {c_lvl} ({CONTENT_LEVELS.get(c_lvl, '?')})")
        print(f"     🔧 Integration Level: {i_lvl} ({INTEGRATION_LEVELS.get(i_lvl, '?')})")
        print(f"     Missing: {', '.join(next_p.get('missing', []))}")
        if c_lvl >= 1:
            print(f"     → Hat Abstract! Kann zu Integration Level 2+ aufgewertet werden")
        else:
            print(f"     → Braucht erst Abstract (Content Level 1)")
    else:
        print("\n  ✅ Queue is empty!")

    print()


def print_list():
    """Print all pending papers grouped by content level (2D system)."""
    queue = load_queue()
    pending = queue.get("pending", [])

    print("\n" + "="*70)
    print("  PENDING PAPERS (2D: Content × Integration)")
    print("="*70)

    if not pending:
        print("  ✅ No pending papers!")
    else:
        # Group by content_level (new 2D system)
        by_content = {0: [], 1: [], 2: []}
        for p in pending:
            c_lvl = p.get("content_level", 0)
            by_content[c_lvl].append(p)

        for c_lvl in [2, 1, 0]:  # Show highest content first
            papers = by_content[c_lvl]
            if papers:
                icon = get_content_level_icon(c_lvl)
                desc = CONTENT_LEVELS.get(c_lvl, "?")
                print(f"\n  {icon} CONTENT LEVEL {c_lvl}: {desc} ({len(papers)} papers)")
                print("  " + "-"*66)

                for i, item in enumerate(papers, 1):
                    i_lvl = item.get("integration_level", item.get("level", 1))
                    ps = item.get("prior_score", item.get("cached_prior_score"))
                    ps_str = f" | π={ps:.3f}" if ps else ""
                    print(f"\n     {i}. {item['paper_id']}")
                    print(f"        Content: {c_lvl} | Integration: {i_lvl}{ps_str}")
                    print(f"        Missing: {', '.join(item.get('missing', []))}")

    print()


def get_papers_to_process(count: int = 1) -> list:
    """Get N papers to process from the queue."""
    queue = load_queue()
    pending = queue.get("pending", [])

    if not pending:
        return []

    order = queue.get("config", {}).get("priority_order", "oldest_first")
    _sort_pending(pending, order)

    return pending[:count]


def populate_from_prior_scores(classifications=None):
    """
    Auto-populate queue from papers with specific prior-score classifications.

    Uses π(p) from data/paper-references/PAP-*.yaml to find papers that
    need integration work, sorted by prior score descending.
    """
    if classifications is None:
        classifications = ['MINIMAL', 'PENDING']

    papers_dir = ROOT / "data" / "paper-references"
    queue = load_queue()
    existing_ids = {p.get('paper_id') for p in queue.get('pending', [])}

    candidates = []
    for f in sorted(papers_dir.glob('PAP-*.yaml')):
        try:
            with open(f) as fh:
                data = yaml.safe_load(fh)
            ps = data.get('prior_score', {})
            if isinstance(ps, dict) and ps.get('classification') in classifications:
                score = float(ps.get('prior_score', 0))
                paper_id = f.stem
                if paper_id not in existing_ids:
                    candidates.append((score, paper_id, ps.get('classification', '?')))
        except Exception:
            continue

    # Sort by score descending
    candidates.sort(reverse=True)

    added = 0
    for score, paper_id, classification in candidates:
        priority = "high" if score >= 0.3 else "normal"
        queue.setdefault("pending", []).append({
            "paper_id": paper_id,
            "added": datetime.now().isoformat(),
            "content_level": 0,
            "integration_level": 1,
            "level": 1,
            "has_full_text": False,
            "track": "B",
            "missing": ["theory_support", "parameter", "case_registry"],
            "priority": priority,
            "prior_score": score,
            "classification": classification,
            "attempts": 0
        })
        added += 1

    if added > 0:
        queue["stats"]["total_queued"] = queue["stats"].get("total_queued", 0) + added
        # Set priority_order to by_prior_score
        queue.setdefault("config", {})["priority_order"] = "by_prior_score"
        save_queue(queue)

    return added, len(candidates)


def set_priority_order(order: str):
    """Set the queue priority order."""
    valid = ['oldest_first', 'newest_first', 'by_level', 'by_prior_score']
    if order not in valid:
        print(f"Invalid order. Valid: {', '.join(valid)}")
        return False
    queue = load_queue()
    queue.setdefault("config", {})["priority_order"] = order
    save_queue(queue)
    return True


def upgrade_to_2d_schema():
    """
    Upgrade existing queue entries to 2D schema (content_level × integration_level).

    Migrates from old track-based system to new 2D classification.
    """
    queue = load_queue()
    pending = queue.get("pending", [])
    upgraded = 0

    print("\n" + "="*70)
    print("  UPGRADING TO 2D SCHEMA")
    print("="*70)

    for item in pending:
        paper_id = item.get("paper_id")
        if paper_id:
            # Determine content_level from actual file
            new_content_level = determine_content_level(paper_id)
            old_content_level = item.get("content_level")

            # Only update if different or missing
            if old_content_level is None or old_content_level != new_content_level:
                item["content_level"] = new_content_level
                item["integration_level"] = item.get("level", 1)

                # Update legacy fields for backwards compat
                item["has_full_text"] = new_content_level >= 1
                item["track"] = "A" if new_content_level >= 1 else "B"

                # Update priority based on content
                if new_content_level >= 1 and item.get("priority") == "normal":
                    item["priority"] = "high"

                upgraded += 1
                icon = get_content_level_icon(new_content_level)
                print(f"  {icon} {paper_id}: content_level → {new_content_level}")

    # Update queue version
    queue["queue_version"] = "2.0"

    if upgraded > 0:
        save_queue(queue)
        print(f"\n  ✅ Upgraded {upgraded} papers to 2D schema")
    else:
        print(f"\n  ✅ All papers already use 2D schema")

    return upgraded


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Paper Integration Queue Manager (2D System: content_level × integration_level)"
    )
    parser.add_argument("--status", action="store_true", help="Show queue status")
    parser.add_argument("--add", metavar="PAPER_ID", help="Add paper to queue")
    parser.add_argument("--next", action="store_true", help="Show next paper to complete")
    parser.add_argument("--process", type=int, metavar="N", help="Get N papers to process")
    parser.add_argument("--complete", metavar="PAPER_ID", help="Mark paper as complete")
    parser.add_argument("--list", action="store_true", help="List all pending papers")
    parser.add_argument("--update-tracks", action="store_true", help="Update all papers with full-text availability")
    parser.add_argument("--upgrade-schema", action="store_true", help="Upgrade to 2D schema (content × integration)")
    parser.add_argument("--priority", choices=["low", "normal", "high"], help="Priority for --add")
    parser.add_argument("--populate", nargs="*", metavar="CLASS",
                        help="Populate queue from prior-score classifications (default: MINIMAL PENDING)")
    parser.add_argument("--set-order", choices=["oldest_first", "newest_first", "by_level", "by_prior_score"],
                        help="Set queue priority order")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if args.status:
        if args.json:
            import json
            print(json.dumps(get_status(), indent=2))
        else:
            print_status()

    elif args.add:
        if add_to_queue(args.add, priority=args.priority):
            print(f"✅ Added {args.add} to queue")
        else:
            missing = get_missing_components(args.add)
            if not missing:
                print(f"✅ {args.add} is already complete")
            else:
                print(f"ℹ️  {args.add} already in queue")

    elif args.next:
        next_paper = get_next_paper()
        if next_paper:
            if args.json:
                import json
                print(json.dumps(next_paper, indent=2))
            else:
                c_lvl = next_paper.get("content_level", 0)
                i_lvl = next_paper.get("integration_level", next_paper.get("level", 1))
                icon = get_content_level_icon(c_lvl)
                print(f"\n{icon} Next paper: {next_paper['paper_id']}")
                print(f"   Content Level: {c_lvl} ({CONTENT_LEVELS.get(c_lvl, '?')})")
                print(f"   Integration Level: {i_lvl} ({INTEGRATION_LEVELS.get(i_lvl, '?')})")
                print(f"   Missing: {', '.join(next_paper.get('missing', []))}")
        else:
            print("✅ Queue is empty!")

    elif args.process:
        papers = get_papers_to_process(args.process)
        if papers:
            if args.json:
                import json
                print(json.dumps(papers, indent=2))
            else:
                print(f"\n📋 {len(papers)} Papers to process:\n")
                for i, p in enumerate(papers, 1):
                    c_lvl = p.get("content_level", 0)
                    i_lvl = p.get("integration_level", p.get("level", 1))
                    icon = get_content_level_icon(c_lvl)
                    print(f"  {i}. {icon} {p['paper_id']}")
                    print(f"     Content: {c_lvl} | Integration: {i_lvl}")
                    print(f"     Missing: {', '.join(p.get('missing', []))}")
                    print()
        else:
            print("✅ Queue is empty!")

    elif args.complete:
        if mark_complete(args.complete):
            print(f"✅ Marked {args.complete} as complete")
        else:
            print(f"❌ {args.complete} not found in queue")

    elif args.list:
        if args.json:
            import json
            queue = load_queue()
            print(json.dumps(queue.get("pending", []), indent=2))
        else:
            print_list()

    elif args.update_tracks:
        updated = update_queue_tracks()
        print(f"✅ Updated {updated} papers with full-text availability")
        print_status()

    elif args.populate is not None:
        classes = args.populate if args.populate else ['MINIMAL', 'PENDING']
        added, total = populate_from_prior_scores(classes)
        print(f"✅ Added {added} papers to queue (from {total} candidates, classes: {', '.join(classes)})")
        print(f"   Queue now sorted by prior score π(p) descending")
        print_status()

    elif args.set_order:
        if set_priority_order(args.set_order):
            print(f"✅ Priority order set to: {args.set_order}")
            print_status()

    elif args.upgrade_schema:
        upgrade_to_2d_schema()
        print_status()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
