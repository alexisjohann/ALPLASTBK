#!/usr/bin/env python3
"""
EBF CORE Framework Validation Script

Validiert die Konsistenz des nC CORE Frameworks über alle Repository-Dateien.
Single Source of Truth: docs/frameworks/core-framework-definition.yaml

Usage:
    python scripts/validate_core_framework.py [--fix] [--verbose]

Options:
    --fix      Automatisch behebbare Probleme korrigieren (nur mit Bestätigung)
    --verbose  Detaillierte Ausgabe
"""

import os
import re
import sys
import yaml
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

# ============================================================================
# CONFIGURATION
# ============================================================================

SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
SSOT_FILE = REPO_ROOT / "docs" / "frameworks" / "core-framework-definition.yaml"

# Files to validate for nC consistency
FILES_TO_CHECK = [
    "README.md",
    "CLAUDE.md",
    "appendices/README.md",
    "appendices/00_appendix_index.tex",
    "docs/frameworks/appendix-category-definitions.md",
]

# Files/patterns to ignore (examples, historical assessments, etc.)
IGNORE_PATTERNS = [
    "core-framework-extension-guide.md",  # Contains examples with 10C, 10C
    "quality/assessments/",               # Historical assessments (5C, 7C snapshots)
    "quality/reports/",                   # Historical quality reports
    "migration-audit/",                   # Historical migration backups
    "outputs/",                           # Historical generated reports
]

# ============================================================================
# PAPER TERMINOLOGY ALLOWLIST
# ============================================================================
# Papers may use their own "nC" terminology that is NOT the EBF CORE framework.
# These patterns are EXEMPTED from validation to avoid false positives.
#
# Format: Each entry is a regex pattern that, if matched in a line, exempts
#         that line from the nC framework validation.
#
# IMPORTANT: Add new paper terminology here when papers use "3C", "5C", etc.
#            for their own frameworks (e.g., TCQ = Touchpoints-Context-Qualities).
# ============================================================================
PAPER_TERMINOLOGY_ALLOWLIST = [
    # TCQ Framework (Touchpoints-Context-Qualities) - 3 components
    r"TCQ\s+Framework",                    # "TCQ Framework"
    r"Touchpoints.*Context.*Qualities",    # Full name
    r"MS-CX-\d+.*\(.*Framework\)",         # Theory catalog references like "MS-CX-001 (TCQ Framework)"

    # Marketing 3C/4C/5C frameworks (common in business literature)
    r"(?:Customer|Company|Competitor|Context|Collaborator).*3C",  # Porter's 3C
    r"4C\s+(?:Marketing|Model)",           # 4C Marketing Model
    r"5C\s+(?:Analysis|Marketing)",        # 5C Analysis

    # Paper-specific frameworks (add new ones here)
    r"3C\s+(?:Model|Modell|Approach|Ansatz)",  # Generic 3C models in papers

    # Explicit "not EBF" markers
    r"nicht.*EBF",                         # German: "nicht EBF Framework"
    r"not.*EBF",                           # English: "not EBF Framework"
    r"paper's own",                        # "paper's own framework"
    r"eigene[rns]?\s+Framework",           # German: own framework
]

# Patterns to search for in each file type
# Note: These patterns are designed to find "nC CORE Framework" references,
# NOT individual CORE numbers like "CORE 7" which are valid.
PATTERNS = {
    ".md": [
        r"(\d)C\s+(?:CORE|Framework|Architektur|Architecture)",  # "10C CORE", "10C Framework"
        r"(?:die|the)\s+(\d)\s+CORE\s+(?:Fragen|questions|appendices)",  # "die 10 CORE Fragen"
        r"(\d)\s+(?:fundamental|fundamentale)\s+(?:Fragen|questions)",  # "9 fundamentale Fragen"
        r"one\s+of\s+(\d)C",  # "one of 10C"
        r"eine[rn]?\s+der\s+(\d)C",  # "eine der 10C"
    ],
    ".tex": [
        r"(\d)C\s+(?:CORE|Framework)",  # "10C CORE Framework"
        r"(\d)\s+CORE\s+[Aa]ppendices",  # "10 CORE Appendices"
        r"all\s+(?:nine|(\d))\s+CORE",  # "all nine CORE" or "all 10 CORE"
    ],
    ".yaml": [
        r"count:\s*(\d+)",
        r'version:\s*["\']?(\d+)C',
    ],
}

# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class ValidationIssue:
    """Represents a validation issue found in a file."""
    file: str
    line_number: int
    issue_type: str
    expected: str
    found: str
    context: str
    auto_fixable: bool = False


@dataclass
class CoreDefinition:
    """Represents a CORE appendix definition."""
    number: int
    code: str
    appendix_code: str
    full_name: str
    title: str
    question_de: str
    question_en: str
    output: str
    primary_symbol: str
    chapter_reference: int
    file: str
    key_concepts: List[str]


# ============================================================================
# SSOT LOADING
# ============================================================================

def load_ssot() -> Dict:
    """Load the Single Source of Truth YAML file."""
    if not SSOT_FILE.exists():
        print(f"❌ FEHLER: Single Source of Truth nicht gefunden: {SSOT_FILE}")
        print("   Bitte docs/frameworks/core-framework-definition.yaml erstellen.")
        sys.exit(1)

    with open(SSOT_FILE, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def get_core_count(ssot: Dict) -> int:
    """Get the expected CORE count from SSOT."""
    return ssot['framework']['count']


def get_cores(ssot: Dict) -> List[CoreDefinition]:
    """Get list of CORE definitions from SSOT."""
    cores = []
    for c in ssot['cores']:
        cores.append(CoreDefinition(
            number=c['number'],
            code=c['code'],
            appendix_code=c['appendix_code'],
            full_name=c['full_name'],
            title=c['title'],
            question_de=c['question_de'],
            question_en=c['question_en'],
            output=c['output'],
            primary_symbol=c['primary_symbol'],
            chapter_reference=c['chapter_reference'],
            file=c['file'],
            key_concepts=c['key_concepts'],
        ))
    return cores


# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def validate_ssot_internal(ssot: Dict) -> List[ValidationIssue]:
    """Validate internal consistency of SSOT."""
    issues = []

    expected_count = ssot['framework']['count']
    actual_count = len(ssot['cores'])

    if expected_count != actual_count:
        issues.append(ValidationIssue(
            file=str(SSOT_FILE),
            line_number=0,
            issue_type="COUNT_MISMATCH",
            expected=str(expected_count),
            found=str(actual_count),
            context=f"framework.count={expected_count} aber {actual_count} cores definiert",
        ))

    # Check sequential numbering
    numbers = [c['number'] for c in ssot['cores']]
    expected_numbers = list(range(1, expected_count + 1))
    if numbers != expected_numbers:
        issues.append(ValidationIssue(
            file=str(SSOT_FILE),
            line_number=0,
            issue_type="NUMBERING_GAP",
            expected=str(expected_numbers),
            found=str(numbers),
            context="CORE Nummerierung ist nicht sequentiell",
        ))

    # Check for duplicate codes
    codes = [c['code'] for c in ssot['cores']]
    if len(codes) != len(set(codes)):
        duplicates = [c for c in codes if codes.count(c) > 1]
        issues.append(ValidationIssue(
            file=str(SSOT_FILE),
            line_number=0,
            issue_type="DUPLICATE_CODE",
            expected="Eindeutige Codes",
            found=str(set(duplicates)),
            context="Doppelte CORE codes gefunden",
        ))

    # Check that all referenced files exist
    for core in ssot['cores']:
        file_path = REPO_ROOT / core['file']
        if not file_path.exists():
            issues.append(ValidationIssue(
                file=str(SSOT_FILE),
                line_number=0,
                issue_type="MISSING_FILE",
                expected=core['file'],
                found="(nicht gefunden)",
                context=f"CORE-{core['code']} referenziert nicht-existente Datei",
            ))

    return issues


def is_allowlisted_terminology(line: str) -> bool:
    """Check if a line contains allowlisted paper terminology.

    Papers may use their own "nC" frameworks (e.g., TCQ = 3C, Porter's 3C)
    that should NOT be flagged as wrong EBF CORE framework references.
    """
    for pattern in PAPER_TERMINOLOGY_ALLOWLIST:
        if re.search(pattern, line, re.IGNORECASE):
            return True
    return False


def find_nc_references(file_path: Path, expected_n: int) -> List[ValidationIssue]:
    """Find all nC references in a file and check if they match expected_n."""
    issues = []

    if not file_path.exists():
        return issues

    suffix = file_path.suffix
    patterns = PATTERNS.get(suffix, PATTERNS['.md'])

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"  ⚠️  Konnte {file_path} nicht lesen: {e}")
        return issues

    for line_num, line in enumerate(lines, 1):
        # Skip lines with allowlisted paper terminology (e.g., TCQ Framework, Porter's 3C)
        if is_allowlisted_terminology(line):
            continue

        for pattern in patterns:
            matches = re.finditer(pattern, line, re.IGNORECASE)
            for match in matches:
                # Handle patterns with optional groups
                group_val = match.group(1)
                if group_val is None:
                    continue  # Skip matches where the number wasn't captured
                try:
                    found_n = int(group_val)
                except ValueError:
                    continue  # Skip non-numeric captures
                if found_n != expected_n and found_n in range(1, 20):  # Plausible range
                    issues.append(ValidationIssue(
                        file=str(file_path.relative_to(REPO_ROOT)),
                        line_number=line_num,
                        issue_type="WRONG_NC_COUNT",
                        expected=f"{expected_n}C",
                        found=f"{found_n}C",
                        context=line.strip()[:80],
                        auto_fixable=True,
                    ))

    return issues


def validate_core_table_in_file(file_path: Path, cores: List[CoreDefinition]) -> List[ValidationIssue]:
    """Check if a file contains a CORE table and validate it."""
    issues = []

    if not file_path.exists():
        return issues

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return issues

    # Check for missing CORE codes in files that should list them
    expected_codes = {c.code for c in cores}

    # Simple check: does the file mention all CORE codes?
    if "CORE-" in content or "| Code |" in content:
        for core in cores:
            # Check if this CORE is mentioned
            code_patterns = [
                f"CORE-{core.code}",
                f"| {core.code} |",
                f"|{core.code}|",
                f"{core.appendix_code}.*CORE-{core.code}",
            ]
            found = any(re.search(p, content) for p in code_patterns)

            if not found and core.number == len(cores):  # Especially check latest CORE
                issues.append(ValidationIssue(
                    file=str(file_path.relative_to(REPO_ROOT)),
                    line_number=0,
                    issue_type="MISSING_CORE",
                    expected=f"CORE-{core.code} ({core.appendix_code})",
                    found="(nicht gefunden)",
                    context=f"Datei sollte CORE-{core.code} enthalten",
                ))

    return issues


def validate_appendix_category_count(file_path: Path, expected_n: int) -> List[ValidationIssue]:
    """Check if appendix-category-definitions.md has correct CORE count."""
    issues = []

    if not file_path.exists():
        return issues

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return issues

    # Look for pattern like "| 1 | `CORE-` | Core Theory | 7 |"
    pattern = r'\|\s*1\s*\|\s*`CORE-`\s*\|\s*Core Theory\s*\|\s*(\d+)\s*\|'
    match = re.search(pattern, content)

    if match:
        found_n = int(match.group(1))
        if found_n != expected_n:
            issues.append(ValidationIssue(
                file=str(file_path.relative_to(REPO_ROOT)),
                line_number=0,
                issue_type="CATEGORY_COUNT_WRONG",
                expected=str(expected_n),
                found=str(found_n),
                context=f"CORE- Kategorie zeigt {found_n} statt {expected_n}",
                auto_fixable=True,
            ))

    return issues


# ============================================================================
# MAIN VALIDATION
# ============================================================================

def run_validation(verbose: bool = False) -> Tuple[List[ValidationIssue], Dict]:
    """Run all validation checks."""
    print("=" * 70)
    print("EBF CORE Framework Validation")
    print("=" * 70)
    print()

    # Load SSOT
    print(f"📖 Lade Single Source of Truth: {SSOT_FILE.relative_to(REPO_ROOT)}")
    ssot = load_ssot()
    expected_n = get_core_count(ssot)
    cores = get_cores(ssot)

    print(f"   Framework Version: {ssot['framework']['version']}")
    print(f"   Erwartete COREs: {expected_n}")
    print()

    all_issues = []

    # 1. Validate SSOT internal consistency
    print("🔍 Prüfe SSOT interne Konsistenz...")
    ssot_issues = validate_ssot_internal(ssot)
    all_issues.extend(ssot_issues)
    if verbose:
        for issue in ssot_issues:
            print(f"   ❌ {issue.issue_type}: {issue.context}")
    print(f"   → {len(ssot_issues)} Problem(e) gefunden")
    print()

    # 2. Check main files for nC references
    print("🔍 Prüfe Haupt-Dateien auf nC Referenzen...")
    for rel_path in FILES_TO_CHECK:
        file_path = REPO_ROOT / rel_path
        if file_path.exists():
            issues = find_nc_references(file_path, expected_n)
            all_issues.extend(issues)
            if verbose and issues:
                print(f"   📄 {rel_path}: {len(issues)} Problem(e)")
                for issue in issues:
                    print(f"      L{issue.line_number}: {issue.found} → {issue.expected}")
    print(f"   → {sum(1 for i in all_issues if i.issue_type == 'WRONG_NC_COUNT')} nC Problem(e)")
    print()

    # 3. Check for missing COREs in documentation
    print("🔍 Prüfe CORE-Vollständigkeit in Dokumentation...")
    for rel_path in FILES_TO_CHECK:
        file_path = REPO_ROOT / rel_path
        issues = validate_core_table_in_file(file_path, cores)
        all_issues.extend(issues)
        if verbose and issues:
            for issue in issues:
                print(f"   ❌ {issue.file}: {issue.expected}")
    print(f"   → {sum(1 for i in all_issues if i.issue_type == 'MISSING_CORE')} fehlende COREs")
    print()

    # 4. Special check for appendix-category-definitions.md
    print("🔍 Prüfe appendix-category-definitions.md...")
    cat_file = REPO_ROOT / "docs" / "frameworks" / "appendix-category-definitions.md"
    cat_issues = validate_appendix_category_count(cat_file, expected_n)
    all_issues.extend(cat_issues)
    if verbose and cat_issues:
        for issue in cat_issues:
            print(f"   ❌ {issue.context}")
    print(f"   → {len(cat_issues)} Problem(e)")
    print()

    # 5. Search for any remaining wrong nC in entire repo
    print("🔍 Durchsuche Repository nach falschen nC Referenzen...")
    wrong_nc_count = 0
    for md_file in REPO_ROOT.rglob("*.md"):
        if ".git" in str(md_file):
            continue
        # Skip ignored patterns (examples, historical assessments)
        rel_path_str = str(md_file.relative_to(REPO_ROOT))
        if any(pattern in rel_path_str for pattern in IGNORE_PATTERNS):
            continue
        issues = find_nc_references(md_file, expected_n)
        # Filter for actual wrong counts (not already in FILES_TO_CHECK)
        new_issues = [i for i in issues if str(REPO_ROOT / i.file) != str(md_file) or
                      str(md_file.relative_to(REPO_ROOT)) not in FILES_TO_CHECK]
        if new_issues:
            wrong_nc_count += len(new_issues)
            if verbose:
                print(f"   📄 {md_file.relative_to(REPO_ROOT)}: {len(new_issues)} Problem(e)")
        all_issues.extend(issues)
    print(f"   → {wrong_nc_count} zusätzliche nC Problem(e)")

    return all_issues, ssot


def print_summary(issues: List[ValidationIssue], ssot: Dict):
    """Print validation summary."""
    print()
    print("=" * 70)
    print("ZUSAMMENFASSUNG")
    print("=" * 70)

    expected_n = ssot['framework']['count']
    cores = get_cores(ssot)

    print(f"\n📊 Framework Status: {expected_n}C")
    print(f"   Definierte COREs:")
    for core in cores:
        print(f"   {core.number}. {core.code} ({core.appendix_code}) - {core.question_de}")

    if not issues:
        print(f"\n✅ Keine Probleme gefunden! Das {expected_n}C Framework ist konsistent.")
    else:
        print(f"\n❌ {len(issues)} Problem(e) gefunden:")

        # Group by type
        by_type = {}
        for issue in issues:
            by_type.setdefault(issue.issue_type, []).append(issue)

        for issue_type, type_issues in sorted(by_type.items()):
            print(f"\n   {issue_type}: {len(type_issues)} Problem(e)")
            for issue in type_issues[:5]:  # Show max 5 per type
                print(f"   • {issue.file}:{issue.line_number}")
                print(f"     Erwartet: {issue.expected}, Gefunden: {issue.found}")
            if len(type_issues) > 5:
                print(f"   ... und {len(type_issues) - 5} weitere")

        # Count auto-fixable
        auto_fixable = sum(1 for i in issues if i.auto_fixable)
        if auto_fixable > 0:
            print(f"\n💡 {auto_fixable} Problem(e) sind automatisch behebbar.")
            print("   Führe aus: python scripts/validate_core_framework.py --fix")

    print()


# ============================================================================
# MAIN
# ============================================================================

def main():
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    fix_mode = "--fix" in sys.argv

    issues, ssot = run_validation(verbose=verbose)
    print_summary(issues, ssot)

    if fix_mode and any(i.auto_fixable for i in issues):
        print("⚠️  --fix Modus ist noch nicht implementiert.")
        print("   Bitte beheben Sie die Probleme manuell.")

    # Exit code
    sys.exit(0 if not issues else 1)


if __name__ == "__main__":
    main()
