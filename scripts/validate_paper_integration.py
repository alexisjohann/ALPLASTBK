#!/usr/bin/env python3
"""
Validate Paper Integration Completeness

Prüft ob alle Dateien für ein integriertes Paper vorhanden sind
basierend auf dem Integration Level.

Usage:
    python scripts/validate_paper_integration.py PAP-berger2025debunking
    python scripts/validate_paper_integration.py --all
    python scripts/validate_paper_integration.py --recent 7  # letzte 7 Tage
"""

import os
import sys
import yaml
import re
from datetime import datetime, timedelta
from pathlib import Path
from glob import glob

# Pfade
ROOT = Path(__file__).parent.parent
PIP_DIR = ROOT / "data" / "paper-intake"
PAPER_REF_DIR = ROOT / "data" / "paper-references"
FULL_TEXT_DIR = ROOT / "papers" / "evaluated" / "integrated"
BIB_FILE = ROOT / "bibliography" / "bcm_master.bib"
CASE_REGISTRY = ROOT / "data" / "case-registry.yaml"
THEORY_CATALOG = ROOT / "data" / "theory-catalog.yaml"

# Required files per level
LEVEL_REQUIREMENTS = {
    1: ["pip", "bibtex"],
    2: ["pip", "bibtex", "paper_ref", "full_text"],
    3: ["pip", "bibtex", "paper_ref", "full_text", "case"],
    4: ["pip", "bibtex", "paper_ref", "full_text", "case", "theory"],
    5: ["pip", "bibtex", "paper_ref", "full_text", "case", "theory", "appendix"],
}

# BibTeX EBF-Felder
REQUIRED_BIB_FIELDS = [
    "evidence_tier",
    "integration_level",
    "pip_id",
    "use_for",
    "theory_support",
]

OPTIONAL_BIB_FIELDS = [
    "parameter",
    "identification",
    "external_validity",
    "session_ref",
    "notes",
]


def find_pip_for_paper(paper_id: str) -> dict | None:
    """Find PIP file for a paper ID."""
    for pip_file in PIP_DIR.rglob("*.yaml"):
        if pip_file.name == "template.yaml":
            continue
        try:
            with open(pip_file) as f:
                pip = yaml.safe_load(f)
            if pip and pip.get("paper_id") == paper_id:
                pip["_file"] = str(pip_file)
                return pip
        except Exception:
            continue
    return None


def check_bibtex_entry(paper_id: str) -> dict:
    """Check if BibTeX entry exists with required fields."""
    result = {
        "exists": False,
        "has_required_fields": False,
        "missing_fields": [],
        "has_optional_fields": [],
    }

    # Extract key from paper_id (PAP-berger2025debunking -> berger2025debunking)
    bib_key = paper_id.replace("PAP-", "")

    try:
        with open(BIB_FILE) as f:
            content = f.read()

        # Find the entry
        pattern = rf"@\w+\{{{bib_key},"
        if re.search(pattern, content):
            result["exists"] = True

            # Extract entry content
            start = content.find(f"@")
            start = content.find(f"{{{bib_key},")
            if start != -1:
                # Find matching closing brace
                depth = 1
                end = start + len(f"{{{bib_key},")
                while depth > 0 and end < len(content):
                    if content[end] == "{":
                        depth += 1
                    elif content[end] == "}":
                        depth -= 1
                    end += 1

                entry = content[start:end]

                # Check required fields
                missing = []
                for field in REQUIRED_BIB_FIELDS:
                    if f"{field} =" not in entry and f"{field}=" not in entry:
                        missing.append(field)

                result["missing_fields"] = missing
                result["has_required_fields"] = len(missing) == 0

                # Check optional fields
                for field in OPTIONAL_BIB_FIELDS:
                    if f"{field} =" in entry or f"{field}=" in entry:
                        result["has_optional_fields"].append(field)
    except Exception as e:
        result["error"] = str(e)

    return result


def check_paper_reference(paper_id: str) -> bool:
    """Check if paper reference YAML exists."""
    ref_file = PAPER_REF_DIR / f"{paper_id}.yaml"
    return ref_file.exists()


def check_full_text(paper_id: str) -> bool:
    """Check if full text file exists."""
    txt_file = FULL_TEXT_DIR / f"{paper_id}.txt"
    return txt_file.exists()


def check_case_registry(paper_id: str) -> bool:
    """Check if case exists in case registry."""
    try:
        with open(CASE_REGISTRY) as f:
            content = f.read()
        return f'source_paper: "{paper_id}"' in content or f"source_paper: '{paper_id}'" in content
    except Exception:
        return False


def check_theory_catalog(paper_id: str) -> bool:
    """Check if theory exists in theory catalog."""
    try:
        with open(THEORY_CATALOG) as f:
            content = f.read()
        return f'source_paper: "{paper_id}"' in content or f"source_paper: '{paper_id}'" in content
    except Exception:
        return False


def validate_paper(paper_id: str) -> dict:
    """Validate complete paper integration."""
    result = {
        "paper_id": paper_id,
        "pip": None,
        "level": None,
        "checks": {},
        "score": 0,
        "max_score": 0,
        "missing": [],
        "complete": False,
    }

    # Find PIP
    pip = find_pip_for_paper(paper_id)
    if not pip:
        result["checks"]["pip"] = {"status": "missing", "message": "PIP file not found"}
        result["missing"].append("PIP file")
        return result

    result["pip"] = pip.get("_file")
    result["level"] = pip.get("ebf_integration", {}).get("integration_level", 1)

    # Get requirements for this level
    requirements = LEVEL_REQUIREMENTS.get(result["level"], LEVEL_REQUIREMENTS[1])
    result["max_score"] = len(requirements)

    # Check each requirement
    for req in requirements:
        if req == "pip":
            result["checks"]["pip"] = {"status": "ok", "file": pip.get("_file")}
            result["score"] += 1

        elif req == "bibtex":
            bib_result = check_bibtex_entry(paper_id)
            if bib_result["exists"] and bib_result["has_required_fields"]:
                result["checks"]["bibtex"] = {"status": "ok", "fields": "complete"}
                result["score"] += 1
            elif bib_result["exists"]:
                result["checks"]["bibtex"] = {
                    "status": "incomplete",
                    "missing_fields": bib_result["missing_fields"]
                }
                result["missing"].append(f"BibTeX fields: {', '.join(bib_result['missing_fields'])}")
            else:
                result["checks"]["bibtex"] = {"status": "missing"}
                result["missing"].append("BibTeX entry")

        elif req == "paper_ref":
            if check_paper_reference(paper_id):
                result["checks"]["paper_ref"] = {"status": "ok"}
                result["score"] += 1
            else:
                result["checks"]["paper_ref"] = {"status": "missing"}
                result["missing"].append("Paper reference YAML")

        elif req == "full_text":
            if check_full_text(paper_id):
                result["checks"]["full_text"] = {"status": "ok"}
                result["score"] += 1
            else:
                result["checks"]["full_text"] = {"status": "missing"}
                result["missing"].append("Full text file")

        elif req == "case":
            if check_case_registry(paper_id):
                result["checks"]["case"] = {"status": "ok"}
                result["score"] += 1
            else:
                result["checks"]["case"] = {"status": "missing"}
                result["missing"].append("Case registry entry")

        elif req == "theory":
            if check_theory_catalog(paper_id):
                result["checks"]["theory"] = {"status": "ok"}
                result["score"] += 1
            else:
                result["checks"]["theory"] = {"status": "missing"}
                result["missing"].append("Theory catalog entry")

        elif req == "appendix":
            # For now, just check if mentioned in PIP
            appendix_links = pip.get("cross_references", {}).get("appendix_links", [])
            if appendix_links:
                result["checks"]["appendix"] = {"status": "ok", "links": len(appendix_links)}
                result["score"] += 1
            else:
                result["checks"]["appendix"] = {"status": "missing"}
                result["missing"].append("Appendix links")

    result["complete"] = result["score"] == result["max_score"]
    return result


def get_recent_pips(days: int = 7) -> list:
    """Get PIPs from the last N days."""
    cutoff = datetime.now() - timedelta(days=days)
    recent = []

    for pip_file in PIP_DIR.rglob("*.yaml"):
        if pip_file.name == "template.yaml":
            continue
        try:
            mtime = datetime.fromtimestamp(pip_file.stat().st_mtime)
            if mtime > cutoff:
                with open(pip_file) as f:
                    pip = yaml.safe_load(f)
                if pip and pip.get("paper_id"):
                    recent.append(pip["paper_id"])
        except Exception:
            continue

    return recent


def print_result(result: dict):
    """Print validation result."""
    paper_id = result["paper_id"]
    level = result["level"]
    score = result["score"]
    max_score = result["max_score"]
    complete = result["complete"]

    status = "✅ COMPLETE" if complete else "❌ INCOMPLETE"
    pct = (score / max_score * 100) if max_score > 0 else 0

    print(f"\n{'='*70}")
    print(f"  {paper_id}")
    print(f"{'='*70}")
    print(f"  Level: {level}")
    print(f"  Score: {score}/{max_score} ({pct:.0f}%)")
    print(f"  Status: {status}")

    if result.get("checks"):
        print(f"\n  Checks:")
        for check, info in result["checks"].items():
            status_icon = "✅" if info.get("status") == "ok" else "❌"
            print(f"    {status_icon} {check}: {info.get('status', 'unknown')}")
            if info.get("missing_fields"):
                print(f"       Missing: {', '.join(info['missing_fields'])}")

    if result.get("missing"):
        print(f"\n  ⚠️  Missing components:")
        for m in result["missing"]:
            print(f"    - {m}")

    print()


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Validate paper integration completeness")
    parser.add_argument("paper_id", nargs="?", help="Paper ID to validate (e.g., PAP-berger2025debunking)")
    parser.add_argument("--all", action="store_true", help="Validate all papers")
    parser.add_argument("--recent", type=int, metavar="DAYS", help="Validate papers from last N days")
    parser.add_argument("--incomplete-only", action="store_true", help="Only show incomplete papers")
    parser.add_argument("--summary", action="store_true", help="Show summary statistics")

    args = parser.parse_args()

    papers = []

    if args.paper_id:
        papers = [args.paper_id]
    elif args.recent:
        papers = get_recent_pips(args.recent)
        print(f"Found {len(papers)} papers from the last {args.recent} days")
    elif args.all:
        # Get all paper IDs from paper-references
        for ref_file in PAPER_REF_DIR.glob("PAP-*.yaml"):
            papers.append(ref_file.stem)
        print(f"Found {len(papers)} papers")
    else:
        parser.print_help()
        return

    results = []
    for paper_id in papers:
        result = validate_paper(paper_id)
        results.append(result)

        if args.incomplete_only and result["complete"]:
            continue

        if not args.summary:
            print_result(result)

    # Summary
    if args.summary or len(papers) > 1:
        complete = sum(1 for r in results if r["complete"])
        incomplete = len(results) - complete

        print(f"\n{'='*70}")
        print(f"  SUMMARY")
        print(f"{'='*70}")
        print(f"  Total papers: {len(results)}")
        print(f"  Complete: {complete} ✅")
        print(f"  Incomplete: {incomplete} ❌")

        if incomplete > 0:
            print(f"\n  Incomplete papers:")
            for r in results:
                if not r["complete"]:
                    print(f"    - {r['paper_id']} (Level {r['level']}, {r['score']}/{r['max_score']})")

        print()

        # Exit with error if any incomplete
        if incomplete > 0 and not args.incomplete_only:
            sys.exit(1)


if __name__ == "__main__":
    main()
