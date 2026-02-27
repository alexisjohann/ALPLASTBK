#!/usr/bin/env python3
"""
SPÖ Document Synchronization Validator
======================================

Validates that all SPÖ documents are synchronized with the SSOT (kernaussagen{}).

Based on Learning L-SPO-001 and Validation Rules V-SPO-001, V-SPO-002.

Usage:
    python scripts/validate_spo_sync.py                    # Full validation
    python scripts/validate_spo_sync.py --emrk             # Only EMRK documents
    python scripts/validate_spo_sync.py --check-framing    # Check for old framing
    python scripts/validate_spo_sync.py --verbose          # Detailed output

Author: FehrAdvice & Partners AG
Date: 2026-02-03
Version: 1.0
"""

import os
import re
import sys
import yaml
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

# Base path
BASE_PATH = Path(__file__).parent.parent / "data" / "customers" / "spo"


class SyncStatus(Enum):
    """Document synchronization status."""
    SYNCED = "✅ SYNCED"
    OUTDATED = "❌ OUTDATED"
    WARNING = "⚠️ WARNING"
    UNKNOWN = "❓ UNKNOWN"
    ARCHIVED = "📦 ARCHIVED"


@dataclass
class ValidationResult:
    """Result of validating a single document."""
    path: str
    status: SyncStatus
    issues: List[str]
    has_old_framing: bool
    has_new_framing: bool
    has_archive_header: bool


class SPOSyncValidator:
    """Validates SPÖ document synchronization with SSOT."""

    # Old framing patterns (should NOT appear in current docs)
    OLD_FRAMING_PATTERNS = [
        r'14\.?156\s*(Abschiebungen)?',
        r'50\s*%?\s*(Straftäter|davon\s+Straftäter)',
        r'50\s+Prozent\s+(davon\s+)?Straftäter',
        r'Höchststand.*Abschiebungen',
    ]

    # New framing patterns (SHOULD appear in current EMRK docs)
    NEW_FRAMING_PATTERNS = [
        r'95\s*%?\s*(EMRK-konform|aller\s+Rückführungen)',
        r'336\s*(Duldungskarten)?',
        r'3\.?591\s*(in\s+Schubhaft)?',
        r'Ordnung\s+statt\s+Spalten',
    ]

    # Archive header patterns
    ARCHIVE_PATTERNS = [
        r'⚠️\s*\*?\*?ARCHIV',
        r'NICHT\s+MEHR\s+VERWENDEN',
        r'\[ARCHIV\]',
        r'VERALTET',
    ]

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.kernaussagen = self._load_kernaussagen()
        self.ssot_architecture = self._load_ssot_architecture()

    def _load_kernaussagen(self) -> Dict:
        """Load kernaussagen from ANFRAGEN_REGISTER.yaml."""
        register_path = BASE_PATH / "database" / "ANFRAGEN_REGISTER.yaml"
        try:
            with open(register_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                # Extract kernaussagen for each anfrage
                kernaussagen = {}
                for anfrage in data.get('anfragen', []):
                    anfrage_id = anfrage.get('id', 'unknown')
                    kernaussagen[anfrage_id] = anfrage.get('kernaussagen', {})
                return kernaussagen
        except Exception as e:
            print(f"Error loading ANFRAGEN_REGISTER.yaml: {e}")
            return {}

    def _load_ssot_architecture(self) -> Dict:
        """Load SSOT architecture definition."""
        ssot_path = BASE_PATH / "database" / "SSOT_ARCHITEKTUR_spo_mandate.yaml"
        try:
            with open(ssot_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading SSOT_ARCHITEKTUR: {e}")
            return {}

    def _check_patterns(self, content: str, patterns: List[str]) -> List[str]:
        """Check if any patterns match in content."""
        matches = []
        for pattern in patterns:
            found = re.findall(pattern, content, re.IGNORECASE)
            if found:
                matches.extend(found if isinstance(found[0], str) else [str(f) for f in found])
        return matches

    def validate_document(self, file_path: Path) -> ValidationResult:
        """Validate a single document."""
        rel_path = str(file_path.relative_to(BASE_PATH))

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return ValidationResult(
                path=rel_path,
                status=SyncStatus.UNKNOWN,
                issues=[f"Could not read file: {e}"],
                has_old_framing=False,
                has_new_framing=False,
                has_archive_header=False
            )

        # Check for patterns
        old_framing_matches = self._check_patterns(content, self.OLD_FRAMING_PATTERNS)
        new_framing_matches = self._check_patterns(content, self.NEW_FRAMING_PATTERNS)
        archive_matches = self._check_patterns(content, self.ARCHIVE_PATTERNS)

        has_old_framing = len(old_framing_matches) > 0
        has_new_framing = len(new_framing_matches) > 0
        has_archive_header = len(archive_matches) > 0

        issues = []

        # Determine status
        if has_archive_header:
            status = SyncStatus.ARCHIVED
            if has_old_framing and not has_new_framing:
                # Archived with old framing is expected
                pass
            elif has_old_framing and has_new_framing:
                issues.append("Archive doc has mixed framing")
        elif has_old_framing and not has_new_framing:
            status = SyncStatus.OUTDATED
            issues.append(f"Contains old framing: {old_framing_matches[:3]}")
            issues.append("Missing ARCHIV header!")
        elif has_old_framing and has_new_framing:
            status = SyncStatus.WARNING
            issues.append(f"Mixed framing detected: old={old_framing_matches[:2]}, new={new_framing_matches[:2]}")
        elif has_new_framing:
            status = SyncStatus.SYNCED
        else:
            # No framing detected - might be a non-EMRK doc
            status = SyncStatus.UNKNOWN
            issues.append("No EMRK framing detected (may be non-EMRK document)")

        return ValidationResult(
            path=rel_path,
            status=status,
            issues=issues,
            has_old_framing=has_old_framing,
            has_new_framing=has_new_framing,
            has_archive_header=has_archive_header
        )

    def validate_all_documents(self, filter_emrk: bool = False) -> List[ValidationResult]:
        """Validate all SPÖ documents."""
        results = []

        # Get all markdown and yaml files
        for ext in ['*.md', '*.yaml']:
            for file_path in BASE_PATH.rglob(ext):
                # Skip database meta files
                if file_path.name in ['SSOT_ARCHITEKTUR_spo_mandate.yaml',
                                       'LEARNINGS_spo_mandate.yaml',
                                       'ANFRAGEN_REGISTER.yaml']:
                    continue

                # Skip context files
                if 'spo_context_' in file_path.name:
                    continue

                # Skip templates
                if '/templates/' in str(file_path):
                    continue

                # If filtering for EMRK, only check EMRK-related files
                if filter_emrk:
                    emrk_keywords = ['emrk', 'migration', 'abschieb', 'duldung', 'ordnung']
                    if not any(kw in file_path.name.lower() for kw in emrk_keywords):
                        continue

                result = self.validate_document(file_path)
                results.append(result)

        return results

    def print_report(self, results: List[ValidationResult]) -> Tuple[int, int, int]:
        """Print validation report and return (passed, warnings, failed) counts."""

        # Group by status
        by_status = {}
        for result in results:
            status = result.status
            if status not in by_status:
                by_status[status] = []
            by_status[status].append(result)

        print("\n" + "=" * 70)
        print("SPÖ DOCUMENT SYNCHRONIZATION REPORT")
        print("=" * 70)
        print(f"\nSSot: ANFRAGEN_REGISTER.yaml → kernaussagen{{}}")
        print(f"Based on: L-SPO-001, V-SPO-001, V-SPO-002\n")

        # Summary
        print("SUMMARY")
        print("-" * 40)
        for status in SyncStatus:
            count = len(by_status.get(status, []))
            if count > 0:
                print(f"  {status.value}: {count}")
        print()

        # Details by status
        for status in [SyncStatus.OUTDATED, SyncStatus.WARNING, SyncStatus.SYNCED,
                       SyncStatus.ARCHIVED, SyncStatus.UNKNOWN]:
            docs = by_status.get(status, [])
            if not docs:
                continue

            print(f"\n{status.value} ({len(docs)} documents)")
            print("-" * 40)

            for result in docs:
                print(f"  • {result.path}")
                if self.verbose and result.issues:
                    for issue in result.issues:
                        print(f"    └─ {issue}")

        # Return counts
        passed = len(by_status.get(SyncStatus.SYNCED, []))
        warnings = len(by_status.get(SyncStatus.WARNING, [])) + len(by_status.get(SyncStatus.UNKNOWN, []))
        failed = len(by_status.get(SyncStatus.OUTDATED, []))

        # Final verdict
        print("\n" + "=" * 70)
        if failed > 0:
            print(f"❌ VALIDATION FAILED: {failed} documents need ARCHIV header or update")
            return_code = 1
        elif warnings > 0:
            print(f"⚠️ VALIDATION PASSED WITH WARNINGS: {warnings} documents need review")
            return_code = 0
        else:
            print(f"✅ VALIDATION PASSED: All {passed} documents are synchronized")
            return_code = 0
        print("=" * 70 + "\n")

        return passed, warnings, failed


def main():
    parser = argparse.ArgumentParser(
        description="Validate SPÖ document synchronization with SSOT"
    )
    parser.add_argument(
        '--emrk', '-e',
        action='store_true',
        help='Only validate EMRK-related documents'
    )
    parser.add_argument(
        '--check-framing', '-c',
        action='store_true',
        help='Focus on framing check (old vs new)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed output'
    )
    parser.add_argument(
        '--file', '-f',
        type=str,
        help='Validate a specific file'
    )

    args = parser.parse_args()

    validator = SPOSyncValidator(verbose=args.verbose)

    if args.file:
        # Validate single file
        file_path = Path(args.file)
        if not file_path.is_absolute():
            file_path = BASE_PATH / file_path
        result = validator.validate_document(file_path)
        print(f"\n{result.status.value}: {result.path}")
        for issue in result.issues:
            print(f"  └─ {issue}")
        sys.exit(0 if result.status in [SyncStatus.SYNCED, SyncStatus.ARCHIVED] else 1)

    # Validate all documents
    results = validator.validate_all_documents(filter_emrk=args.emrk)
    passed, warnings, failed = validator.print_report(results)

    # Exit with appropriate code
    sys.exit(1 if failed > 0 else 0)


if __name__ == "__main__":
    main()
