#!/usr/bin/env python3
"""
SPÖ Delivery Completeness Validator
====================================

Validates that all strategic questions (ANF) in the ANFRAGEN_REGISTER
have complete deliverable sets.

Standard Deliverables per ANF (PFLICHT):
  1. REPORT   - Strategiereport (reports/)
  2. WORDING  - Kommunikationsbriefing (reports/)
  3. INTERVIEW - ZIB2/Medien-Simulation (reports/)
  4. WAEHLERBEFRAGUNG - LLMMC Wählersimulation (simulations/)

Usage:
    python scripts/validate_spo_deliveries.py              # Full validation
    python scripts/validate_spo_deliveries.py --verbose     # Detailed output
    python scripts/validate_spo_deliveries.py --strict      # Exit code 1 if incomplete
    python scripts/validate_spo_deliveries.py --anf ANF-2026-02-04-001  # Single ANF

Author: FehrAdvice & Partners AG
Date: 2026-02-05
Version: 1.0
"""

import os
import sys
import yaml
import argparse
from pathlib import Path
from typing import Dict, List, Optional

# Base paths
BASE_PATH = Path(__file__).parent.parent / "data" / "customers" / "spo"
REGISTER_PATH = BASE_PATH / "database" / "ANFRAGEN_REGISTER.yaml"

# Standard deliverable types (PFLICHT for every ANF)
REQUIRED_DELIVERABLES = {
    "report": {
        "label": "REPORT",
        "description": "Strategiereport",
        "expected_prefix": "REPORT_",
        "expected_dir": "reports",
    },
    "wording": {
        "label": "WORDING",
        "description": "Kommunikationsbriefing",
        "expected_prefix": "WORDING_",
        "expected_dir": "reports",
    },
    "interview": {
        "label": "INTERVIEW",
        "description": "ZIB2/Medien-Simulation",
        "expected_prefix": "INTERVIEW_",
        "expected_dir": "reports",
    },
    "waehlerbefragung": {
        "label": "WÄHLERBEFRAGUNG",
        "description": "LLMMC Wählersimulation",
        "expected_prefix": "WAEHLERBEFRAGUNG_",
        "expected_dir": "simulations",
    },
}


def load_register() -> List[dict]:
    """Load the ANFRAGEN_REGISTER (may contain multiple YAML documents)."""
    with open(REGISTER_PATH, "r", encoding="utf-8") as f:
        for doc in yaml.safe_load_all(f):
            if doc and "anfragen" in doc:
                return doc.get("anfragen", [])
    return []


def check_file_exists(pfad: str, dateiname: str) -> bool:
    """Check if a deliverable file actually exists on disk."""
    file_path = BASE_PATH / pfad / dateiname
    return file_path.exists()


def validate_anf(anf: dict, verbose: bool = False) -> dict:
    """Validate a single ANF entry for delivery completeness.

    Returns:
        {
            "id": str,
            "status": str,
            "thema": str,
            "complete": bool,
            "missing_register": list,   # Missing in YAML outputs
            "missing_files": list,      # In register but file missing
            "present": list,            # Complete deliverables
            "score": str,               # e.g. "3/4"
        }
    """
    anf_id = anf.get("id", "UNKNOWN")
    anf_status = anf.get("status", "unbekannt")
    anf_thema = anf.get("thema", "")
    outputs = anf.get("outputs", {})

    result = {
        "id": anf_id,
        "status": anf_status,
        "thema": anf_thema,
        "complete": True,
        "missing_register": [],
        "missing_files": [],
        "present": [],
    }

    for key, spec in REQUIRED_DELIVERABLES.items():
        if key not in outputs or outputs[key] is None:
            result["missing_register"].append(spec["label"])
            result["complete"] = False
        else:
            entry = outputs[key]
            dateiname = entry.get("dateiname", "")
            pfad = entry.get("pfad", spec["expected_dir"] + "/")
            entry_status = entry.get("status", "")

            if not dateiname:
                result["missing_register"].append(spec["label"])
                result["complete"] = False
            elif not check_file_exists(pfad, dateiname):
                result["missing_files"].append(
                    f"{spec['label']} ({dateiname})"
                )
                result["complete"] = False
            else:
                result["present"].append(spec["label"])

    total = len(REQUIRED_DELIVERABLES)
    present_count = len(result["present"])
    result["score"] = f"{present_count}/{total}"

    return result


def print_result(result: dict, verbose: bool = False):
    """Print validation result for one ANF."""
    anf_id = result["id"]
    score = result["score"]
    status_icon = "✅" if result["complete"] else "❌"

    print(f"  {status_icon} {anf_id} [{score}] — {result['thema']}")

    if not result["complete"] or verbose:
        if result["missing_register"]:
            for m in result["missing_register"]:
                print(f"      ❌ {m} — fehlt im Register")
        if result["missing_files"]:
            for m in result["missing_files"]:
                print(f"      ❌ {m} — Datei nicht gefunden")
        if verbose and result["present"]:
            for p in result["present"]:
                print(f"      ✅ {p}")


def main():
    parser = argparse.ArgumentParser(
        description="Validate SPÖ delivery completeness"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Show all details"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with code 1 if any abgeschlossen ANF is incomplete",
    )
    parser.add_argument(
        "--anf", type=str, help="Validate a specific ANF ID only"
    )
    parser.add_argument(
        "--pre-commit",
        action="store_true",
        help="Pre-commit mode: only check abgeschlossen ANFs, strict",
    )
    args = parser.parse_args()

    if not REGISTER_PATH.exists():
        print("ERROR: ANFRAGEN_REGISTER.yaml not found")
        sys.exit(1)

    anfragen = load_register()

    if not anfragen:
        print("WARNING: No ANF entries found in register")
        sys.exit(0)

    # Filter
    if args.anf:
        anfragen = [a for a in anfragen if a.get("id") == args.anf]
        if not anfragen:
            print(f"ERROR: ANF {args.anf} not found")
            sys.exit(1)

    print()
    print("=" * 70)
    print("  SPÖ DELIVERY COMPLETENESS CHECK")
    print(
        f"  Standard: {len(REQUIRED_DELIVERABLES)} Pflicht-Deliverables pro ANF"
    )
    print(
        f"  ({', '.join(s['label'] for s in REQUIRED_DELIVERABLES.values())})"
    )
    print("=" * 70)
    print()

    results = []
    for anf in anfragen:
        if isinstance(anf, dict) and anf.get("id"):
            result = validate_anf(anf, verbose=args.verbose)
            results.append(result)
            print_result(result, verbose=args.verbose)

    print()
    print("-" * 70)

    # Summary
    total = len(results)
    complete = sum(1 for r in results if r["complete"])
    incomplete = total - complete

    # Check abgeschlossen but incomplete (the critical case)
    abgeschlossen_incomplete = [
        r
        for r in results
        if r["status"] == "abgeschlossen" and not r["complete"]
    ]

    print(f"  GESAMT:       {total} ANF-Einträge")
    print(f"  VOLLSTÄNDIG:  {complete}/{total}")

    if abgeschlossen_incomplete:
        print()
        print("  ⚠️  KRITISCH: Abgeschlossene ANFs mit fehlenden Deliverables:")
        for r in abgeschlossen_incomplete:
            missing = r["missing_register"] + [
                m.split(" (")[0] for m in r["missing_files"]
            ]
            print(f"      {r['id']}: fehlt {', '.join(missing)}")
    elif incomplete > 0:
        print(
            f"  IN ARBEIT:    {incomplete} (noch nicht abgeschlossen — OK)"
        )
    else:
        print()
        print("  ✅ Alle abgeschlossenen ANFs haben vollständige Deliverables.")

    print()
    print("=" * 70)
    print()

    # Exit code
    if args.strict or args.pre_commit:
        if abgeschlossen_incomplete:
            sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
