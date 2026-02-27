#!/usr/bin/env python3
"""
get_next_lead_id.py - Atomare LEAD-ID Vergabe

Gibt die nächste freie LEAD-ID zurück und incrementiert den Tracker.
Wird von /lead-add und /meeting aufgerufen.

Usage:
    python scripts/get_next_lead_id.py              # Gibt LEAD-058 zurück, incrementiert auf 59
    python scripts/get_next_lead_id.py --peek       # Zeigt nur nächste ID (ohne Increment)
    python scripts/get_next_lead_id.py --validate   # Prüft Konsistenz
"""

import sys
import re
from pathlib import Path

# Pfad zur Lead-Datenbank
LEAD_DB = Path(__file__).parent.parent / "data" / "sales" / "lead-database.yaml"


def read_yaml_simple(filepath: Path) -> str:
    """Liest YAML als Text (ohne Parser für Atomarität)."""
    return filepath.read_text(encoding="utf-8")


def write_yaml_simple(filepath: Path, content: str) -> None:
    """Schreibt YAML als Text."""
    filepath.write_text(content, encoding="utf-8")


def get_next_lead_id(peek_only: bool = False) -> str:
    """
    Holt die nächste LEAD-ID und incrementiert den Tracker.

    Args:
        peek_only: Wenn True, wird nur gelesen ohne zu incrementieren

    Returns:
        LEAD-ID im Format "LEAD-NNN"
    """
    content = read_yaml_simple(LEAD_DB)

    # Finde next_lead_id in metadata
    match = re.search(r'next_lead_id:\s*(\d+)', content)
    if not match:
        print("ERROR: next_lead_id nicht in metadata gefunden!", file=sys.stderr)
        sys.exit(1)

    current_id = int(match.group(1))
    lead_id = f"LEAD-{current_id:03d}"

    if not peek_only:
        # Incrementiere next_lead_id
        new_id = current_id + 1
        new_content = re.sub(
            r'(next_lead_id:\s*)\d+',
            f'\\g<1>{new_id}',
            content
        )
        write_yaml_simple(LEAD_DB, new_content)
        print(f"✅ next_lead_id: {current_id} → {new_id}", file=sys.stderr)

    return lead_id


def validate_consistency() -> bool:
    """Prüft ob next_lead_id > alle existierenden IDs."""
    content = read_yaml_simple(LEAD_DB)

    # Finde next_lead_id
    match = re.search(r'next_lead_id:\s*(\d+)', content)
    if not match:
        print("ERROR: next_lead_id nicht gefunden!", file=sys.stderr)
        return False
    next_id = int(match.group(1))

    # Finde alle existierenden LEAD-IDs
    existing_ids = [int(m) for m in re.findall(r'^  - id: LEAD-(\d+)', content, re.MULTILINE)]

    if not existing_ids:
        print(f"✅ Keine existierenden Leads, next_lead_id={next_id}", file=sys.stderr)
        return True

    highest_id = max(existing_ids)

    # Prüfe auf Duplikate
    if len(existing_ids) != len(set(existing_ids)):
        from collections import Counter
        duplicates = [id for id, count in Counter(existing_ids).items() if count > 1]
        print(f"❌ DUPLIKATE gefunden: {['LEAD-' + str(d).zfill(3) for d in duplicates]}", file=sys.stderr)
        return False

    if next_id <= highest_id:
        print(f"❌ next_lead_id ({next_id}) <= höchste ID ({highest_id})", file=sys.stderr)
        print(f"   FIX: Setze next_lead_id auf {highest_id + 1}", file=sys.stderr)
        return False

    print(f"✅ Konsistent: next_lead_id={next_id}, höchste existierende ID={highest_id}", file=sys.stderr)
    print(f"   {len(existing_ids)} Leads in Datenbank", file=sys.stderr)
    return True


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "--peek":
            lead_id = get_next_lead_id(peek_only=True)
            print(lead_id)
        elif sys.argv[1] == "--validate":
            success = validate_consistency()
            sys.exit(0 if success else 1)
        elif sys.argv[1] in ["-h", "--help"]:
            print(__doc__)
        else:
            print(f"Unbekannte Option: {sys.argv[1]}", file=sys.stderr)
            print("Optionen: --peek, --validate, --help", file=sys.stderr)
            sys.exit(1)
    else:
        # Standard: ID holen und incrementieren
        lead_id = get_next_lead_id(peek_only=False)
        print(lead_id)


if __name__ == "__main__":
    main()
