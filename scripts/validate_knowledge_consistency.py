#!/usr/bin/env python3
"""
Validate chat-insights against canonical SSOT entries.

Checks all chat-insight YAML files for terminology errors that contradict
the canonical knowledge base entries in data/knowledge/canonical/.

SSOT: data/knowledge/canonical/terminology-registry.yaml
      (consolidated registry of ALL canonical terms)

Usage:
    python scripts/validate_knowledge_consistency.py          # Check all
    python scripts/validate_knowledge_consistency.py --fix     # Auto-fix known errors
    python scripts/validate_knowledge_consistency.py --strict  # Exit code 1 on any error
    python scripts/validate_knowledge_consistency.py --summary # Show term counts by category
"""

import os
import sys
import re
import glob
import argparse
from pathlib import Path

# ── Repository root ──────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parent.parent
CHAT_INSIGHTS_DIR = REPO_ROOT / "data" / "knowledge" / "chat-insights"
CANONICAL_DIR = REPO_ROOT / "data" / "knowledge" / "canonical"
TERMINOLOGY_REGISTRY = CANONICAL_DIR / "terminology-registry.yaml"

# ── SSOT Rules ───────────────────────────────────────────────────────────
# These rules are derived from the terminology-registry.yaml (SSOT).
# The hardcoded list here is the VALIDATION ENGINE — it implements the
# registry's wrong_forms as regex patterns for file scanning.
#
# To add a new rule:
# 1. Add the term to terminology-registry.yaml (SSOT)
# 2. Add the corresponding regex rule below
# 3. Run: python scripts/validate_knowledge_consistency.py --summary

TERMINOLOGY_RULES = [
    # ── BCM Name (SSOT: TRM-FRM-002) ──
    {
        "id": "BCM-NAME-001",
        "registry_id": "TRM-FRM-002",
        "pattern": r"Behavioral\s+Competence\s+Model",
        "description": "Wrong BCM name: 'Behavioral Competence Model'",
        "correct": "Behavioral Change Model",
        "fix_from": "Behavioral Competence Model",
        "fix_to": "Behavioral Change Model",
        "severity": "ERROR",
        "ssot": "data/knowledge/canonical/terminology-registry.yaml",
    },
    {
        "id": "BCM-NAME-002",
        "registry_id": "TRM-FRM-002",
        "pattern": r"Behavioral\s+Context\s+Model",
        "description": "Wrong BCM name: 'Behavioral Context Model'",
        "correct": "Behavioral Change Model",
        "fix_from": "Behavioral Context Model",
        "fix_to": "Behavioral Change Model",
        "severity": "ERROR",
        "ssot": "data/knowledge/canonical/terminology-registry.yaml",
    },
    # ── FEPSDE (SSOT: TRM-FEPSDE-003, TRM-FEPSDE-005, TRM-FEPSDE-006) ──
    {
        "id": "FEPSDE-001",
        "registry_id": "TRM-FEPSDE-003",
        "pattern": r"P\s*[=:]\s*Psychological",
        "description": "Wrong FEPSDE: P = Psychological (correct: Physical)",
        "correct": "P = Physical",
        "severity": "ERROR",
        "ssot": "data/knowledge/canonical/terminology-registry.yaml",
    },
    {
        "id": "FEPSDE-002",
        "registry_id": "TRM-FEPSDE-005",
        "pattern": r"D\s*[=:]\s*Developmental",
        "description": "Wrong FEPSDE: D = Developmental (correct: Digital)",
        "correct": "D = Digital",
        "severity": "ERROR",
        "ssot": "data/knowledge/canonical/terminology-registry.yaml",
    },
    {
        "id": "FEPSDE-003",
        "registry_id": "TRM-FEPSDE-006",
        "pattern": r"E\s*[=:]\s*Environmental(?!\s+Support)",
        "description": "Wrong FEPSDE: E = Environmental (correct: Ecological)",
        "correct": "E = Ecological",
        "severity": "ERROR",
        "ssot": "data/knowledge/canonical/terminology-registry.yaml",
    },
    # ── Ψ-Dimension Names (SSOT: TRM-PSI-*) ──
    {
        "id": "PSI-NAME-001",
        "registry_id": "TRM-PSI-007",
        "pattern": r"Ψ_Co\b|Psi_Co\b|\\Psi_Co\b",
        "description": "Wrong Ψ symbol: Ψ_Co (correct: Ψ_M for Material)",
        "correct": "Ψ_M (Material)",
        "fix_from": "Ψ_Co",
        "fix_to": "Ψ_M",
        "severity": "ERROR",
        "ssot": "data/knowledge/canonical/terminology-registry.yaml",
    },
    {
        "id": "PSI-NAME-002",
        "registry_id": "TRM-PSI-003",
        "pattern": r"Ψ_Cu\b|Psi_Cu\b|\\Psi_Cu\b",
        "description": "Wrong Ψ symbol: Ψ_Cu (correct: Ψ_K for Cultural)",
        "correct": "Ψ_K (Cultural)",
        "fix_from": "Ψ_Cu",
        "fix_to": "Ψ_K",
        "severity": "ERROR",
        "ssot": "data/knowledge/canonical/terminology-registry.yaml",
    },
    {
        "id": "PSI-NAME-003",
        "registry_id": "TRM-PSI-008",
        "pattern": r"Ψ_P\b(?!\s*\()|Psi_P\b(?!\s*\()",
        "description": "Wrong Ψ symbol: Ψ_P (correct: Ψ_F for Physical)",
        "correct": "Ψ_F (Physical)",
        "fix_from": "Ψ_P",
        "fix_to": "Ψ_F",
        "severity": "ERROR",
        "ssot": "data/knowledge/canonical/terminology-registry.yaml",
    },
    {
        "id": "PSI-NAME-004",
        "registry_id": "TRM-PSI-004",
        "pattern": r"Ψ_K\s*\(Knowledge\)",
        "description": "Wrong Ψ label: Ψ_K (Knowledge) (correct: Cultural)",
        "correct": "Ψ_K (Cultural)",
        "severity": "ERROR",
        "ssot": "data/knowledge/canonical/terminology-registry.yaml",
    },
    {
        "id": "PSI-NAME-005",
        "registry_id": "TRM-PSI-005",
        "pattern": r"Ψ_E\s*\(Environmental\)",
        "description": "Wrong Ψ label: Ψ_E (Environmental) (correct: Economic)",
        "correct": "Ψ_E (Economic)",
        "severity": "ERROR",
        "ssot": "data/knowledge/canonical/terminology-registry.yaml",
    },
    {
        "id": "PSI-NAME-006",
        "registry_id": "TRM-PSI-007",
        "pattern": r"Communication\s*\(Ψ|Ψ.*Communication",
        "description": "Wrong Ψ dimension: 'Communication' (correct: Material)",
        "correct": "Material (Ψ_M)",
        "fix_from": "Communication",
        "fix_to": "Material",
        "severity": "ERROR",
        "ssot": "data/knowledge/canonical/terminology-registry.yaml",
    },
    {
        "id": "PSI-SCARF-001",
        "registry_id": "TRM-PSI-*",
        "pattern": r"Autonomy,\s*Certainty,\s*Fairness,\s*Belonging",
        "description": "SCARF model dimensions used instead of EBF Ψ-dimensions",
        "correct": "Institutional, Social, Cognitive, Cultural, Economic, Temporal, Material, Physical",
        "severity": "ERROR",
        "ssot": "data/knowledge/canonical/terminology-registry.yaml",
    },
]


def scan_file(filepath, rules):
    """Scan a single file against all rules. Returns list of violations."""
    violations = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return [{"file": str(filepath), "rule": "READ-ERROR", "message": str(e)}]

    for rule in rules:
        matches = list(re.finditer(rule["pattern"], content, re.IGNORECASE))
        for match in matches:
            # Find line number
            line_num = content[: match.start()].count("\n") + 1
            violations.append(
                {
                    "file": str(filepath),
                    "line": line_num,
                    "rule_id": rule["id"],
                    "registry_id": rule.get("registry_id", ""),
                    "severity": rule["severity"],
                    "description": rule["description"],
                    "correct": rule["correct"],
                    "ssot": rule["ssot"],
                    "matched_text": match.group(),
                    "fixable": "fix_from" in rule,
                }
            )
    return violations


def fix_file(filepath, rules):
    """Apply auto-fixes to a file. Returns number of fixes applied."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return 0

    fixes = 0
    for rule in rules:
        if "fix_from" in rule and "fix_to" in rule:
            # Direct string replace
            count = content.count(rule["fix_from"])
            if count > 0:
                content = content.replace(rule["fix_from"], rule["fix_to"])
                fixes += count
            # Also handle YAML line-continuations (text split across lines)
            pattern = re.escape(rule["fix_from"]).replace(r"\ ", r"\s+")
            for m in reversed(list(re.finditer(pattern, content, re.IGNORECASE))):
                original = m.group()
                if original != rule["fix_from"]:  # only if not already fixed above
                    replacement = rule["fix_to"]
                    # Preserve original whitespace structure
                    if "\n" in original:
                        parts = rule["fix_to"].split()
                        orig_parts = re.split(r"\s+", original)
                        ws = re.search(r"\s*\n\s*", original)
                        if ws and len(parts) >= 2:
                            replacement = parts[0] + ws.group() + " ".join(parts[1:])
                    content = content[: m.start()] + replacement + content[m.end() :]
                    fixes += 1

    if fixes > 0:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    return fixes


def scan_directory(directory, rules):
    """Scan all YAML files in directory recursively."""
    all_violations = []
    yaml_files = sorted(glob.glob(str(directory / "**" / "*.yaml"), recursive=True))

    for filepath in yaml_files:
        violations = scan_file(filepath, rules)
        all_violations.extend(violations)

    return all_violations, len(yaml_files)


def print_summary():
    """Print terminology registry summary (term counts by category)."""
    print()
    print("=" * 72)
    print("  TERMINOLOGY REGISTRY SUMMARY")
    print(f"  SSOT: {TERMINOLOGY_REGISTRY.relative_to(REPO_ROOT)}")
    print("=" * 72)

    # Count rules by category
    categories = {}
    for rule in TERMINOLOGY_RULES:
        rid = rule.get("registry_id", "UNKNOWN")
        prefix = rid.split("-")[1] if "-" in rid else "OTHER"
        categories.setdefault(prefix, []).append(rule["id"])

    print()
    print(f"  {'Category':<20} {'Rules':<8} {'Rule IDs'}")
    print(f"  {'─' * 20} {'─' * 8} {'─' * 40}")
    for cat, rules in sorted(categories.items()):
        print(f"  {cat:<20} {len(rules):<8} {', '.join(rules[:3])}{'...' if len(rules) > 3 else ''}")

    total = len(TERMINOLOGY_RULES)
    fixable = sum(1 for r in TERMINOLOGY_RULES if "fix_from" in r)
    print()
    print(f"  Total validation rules: {total}")
    print(f"  Auto-fixable rules:     {fixable}")
    print(f"  Registry file exists:   {'✅' if TERMINOLOGY_REGISTRY.exists() else '❌'}")
    print()

    # Show categories from registry file
    if TERMINOLOGY_REGISTRY.exists():
        try:
            with open(TERMINOLOGY_REGISTRY, "r", encoding="utf-8") as f:
                content = f.read()
            # Count TRM- entries
            trm_count = content.count("id: TRM-")
            print(f"  Terms in registry:      {trm_count}")
        except Exception:
            pass
    print()


def print_report(violations, total_files, fix_mode=False):
    """Print a formatted report of violations."""
    errors = [v for v in violations if v["severity"] == "ERROR"]
    warnings = [v for v in violations if v["severity"] == "WARNING"]

    print()
    print("=" * 72)
    print("  KNOWLEDGE CONSISTENCY VALIDATION REPORT")
    print(f"  SSOT: data/knowledge/canonical/terminology-registry.yaml")
    print("=" * 72)
    print(f"  Files scanned:  {total_files}")
    print(f"  Errors found:   {len(errors)}")
    print(f"  Warnings found: {len(warnings)}")
    print(f"  Auto-fixable:   {sum(1 for v in violations if v.get('fixable'))}")
    print("=" * 72)

    if not violations:
        print()
        print("  ✅ All chat-insights are consistent with canonical SSOTs.")
        print()
        return

    # Group by file
    by_file = {}
    for v in violations:
        fname = os.path.relpath(v["file"], REPO_ROOT)
        by_file.setdefault(fname, []).append(v)

    for fname, file_violations in sorted(by_file.items()):
        print()
        print(f"  📄 {fname}")
        for v in file_violations:
            fix_marker = " [FIXABLE]" if v.get("fixable") else ""
            reg_ref = f" [{v['registry_id']}]" if v.get("registry_id") else ""
            print(f"     ❌ Line {v['line']}: {v['description']}{fix_marker}{reg_ref}")
            print(f"        Correct: {v['correct']}")
            print(f"        SSOT: {v['ssot']}")

    print()
    print("-" * 72)
    if fix_mode:
        print("  Run with --fix to auto-correct fixable errors.")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Validate chat-insights against canonical SSOT entries"
    )
    parser.add_argument(
        "--fix", action="store_true", help="Auto-fix known terminology errors"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with code 1 if any errors found",
    )
    parser.add_argument(
        "--pre-commit",
        action="store_true",
        help="Pre-commit mode: only check staged files",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Show terminology registry summary",
    )
    args = parser.parse_args()

    if args.summary:
        print_summary()
        return 0

    if args.fix:
        # Fix mode: apply auto-fixes
        yaml_files = sorted(
            glob.glob(str(CHAT_INSIGHTS_DIR / "**" / "*.yaml"), recursive=True)
        )
        total_fixes = 0
        fixed_files = 0
        for filepath in yaml_files:
            fixes = fix_file(filepath, TERMINOLOGY_RULES)
            if fixes > 0:
                total_fixes += fixes
                fixed_files += 1
                print(f"  ✅ Fixed {fixes} error(s) in {os.path.relpath(filepath, REPO_ROOT)}")

        if total_fixes == 0:
            print("  ✅ No fixable errors found.")
        else:
            print(f"\n  Total: {total_fixes} fix(es) in {fixed_files} file(s).")
        return 0

    # Scan mode
    violations, total_files = scan_directory(CHAT_INSIGHTS_DIR, TERMINOLOGY_RULES)
    print_report(violations, total_files, fix_mode=not args.fix)

    if args.strict and any(v["severity"] == "ERROR" for v in violations):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
