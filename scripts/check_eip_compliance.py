#!/usr/bin/env python3
"""
EBF Evidence Integration Pipeline (EIP) Compliance Checker

Validates that concepts have been properly processed through the EIP workflow.
Ensures all new concepts have evidence documentation (PRO/CONTRA).

Usage:
    python scripts/check_eip_compliance.py                    # Validate concept-registry.yaml
    python scripts/check_eip_compliance.py --concept CONC-2026-001  # Validate specific concept
    python scripts/check_eip_compliance.py --rejected         # Validate rejected_concepts.md
    python scripts/check_eip_compliance.py --all              # Validate everything
    python scripts/check_eip_compliance.py --stats            # Show statistics

Reference: docs/workflows/evidence-integration-pipeline.md
"""

import sys
import yaml
import argparse
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class ValidationSeverity(Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


@dataclass
class ValidationResult:
    field: str
    severity: ValidationSeverity
    message: str
    suggestion: Optional[str] = None


# =============================================================================
# EIP REFERENCE DATA
# =============================================================================

VALID_TRIGGERS = ["TR1", "TR2", "TR3", "TR4", "TR5"]

TRIGGER_DESCRIPTIONS = {
    "TR1": "Neue Terminologie eingeführt",
    "TR2": "Neuer Mechanismus beschrieben",
    "TR3": "Neue γ-Werte behauptet",
    "TR4": "Neue Formel/Gleichung entwickelt",
    "TR5": "Neue Intervention vorgeschlagen"
}

VALID_DECISIONS = ["integrate", "reject", "modify"]

VALID_EVIDENCE_STRENGTH = ["high", "medium", "low"]

VALID_THREAT_LEVELS = ["high", "medium", "low"]

VALID_CONFIDENCE_LEVELS = ["high", "medium", "low"]

# Minimum requirements for EIP compliance
MIN_PRO_EVIDENCE = 1  # At least 1 supporting paper
MIN_CONFIDENCE_FOR_INTEGRATION = "medium"  # At least medium confidence


# =============================================================================
# CONCEPT VALIDATION
# =============================================================================

def validate_concept(concept: Dict) -> Tuple[List[ValidationResult], int]:
    """Validate a single concept entry against EIP requirements."""
    results = []
    score = 100

    # Required fields
    required_fields = [
        "concept_id", "name", "description", "triggers",
        "proposed_location", "evidence", "decision", "session"
    ]

    for field in required_fields:
        if field not in concept:
            results.append(ValidationResult(
                field=field,
                severity=ValidationSeverity.ERROR,
                message=f"Required field '{field}' is missing",
                suggestion=f"Add '{field}' to the concept entry"
            ))
            score -= 15

    # Validate concept_id format
    if "concept_id" in concept:
        concept_id = concept["concept_id"]
        if not re.match(r"CONC-\d{4}-\d{3}", concept_id):
            results.append(ValidationResult(
                field="concept_id",
                severity=ValidationSeverity.ERROR,
                message=f"Invalid concept_id format: {concept_id}",
                suggestion="Use format: CONC-YYYY-NNN (e.g., CONC-2026-001)"
            ))
            score -= 10

    # Validate triggers
    if "triggers" in concept:
        triggers = concept["triggers"]
        if not triggers or len(triggers) == 0:
            results.append(ValidationResult(
                field="triggers",
                severity=ValidationSeverity.ERROR,
                message="No triggers specified",
                suggestion="Add at least one trigger (TR1-TR5)"
            ))
            score -= 10
        else:
            for trigger in triggers:
                # Check if trigger contains valid TR1-TR5
                has_valid_trigger = any(t in trigger for t in VALID_TRIGGERS)
                if not has_valid_trigger:
                    results.append(ValidationResult(
                        field="triggers",
                        severity=ValidationSeverity.WARNING,
                        message=f"Trigger may not follow TR1-TR5 format: {trigger[:50]}...",
                        suggestion="Format: 'TR1: Neue Terminologie (...)'"
                    ))
                    score -= 5

    # Validate evidence
    if "evidence" in concept:
        evidence = concept["evidence"]

        # Check PRO evidence
        if "pro" not in evidence or not evidence["pro"]:
            results.append(ValidationResult(
                field="evidence.pro",
                severity=ValidationSeverity.ERROR,
                message="No PRO evidence provided",
                suggestion="Add supporting papers from bcm_master.bib"
            ))
            score -= 15
        else:
            pro_papers = evidence["pro"]
            if len(pro_papers) < MIN_PRO_EVIDENCE:
                results.append(ValidationResult(
                    field="evidence.pro",
                    severity=ValidationSeverity.WARNING,
                    message=f"Only {len(pro_papers)} PRO papers (minimum: {MIN_PRO_EVIDENCE})",
                    suggestion="Search for additional supporting evidence"
                ))
                score -= 5

            # Validate each PRO paper
            for i, paper in enumerate(pro_papers):
                if "paper" not in paper:
                    results.append(ValidationResult(
                        field=f"evidence.pro[{i}]",
                        severity=ValidationSeverity.ERROR,
                        message="Paper citation key missing",
                        suggestion="Add 'paper' field with bibtex key"
                    ))
                    score -= 5
                if "finding" not in paper:
                    results.append(ValidationResult(
                        field=f"evidence.pro[{i}]",
                        severity=ValidationSeverity.WARNING,
                        message="Finding description missing",
                        suggestion="Add 'finding' field describing the supporting evidence"
                    ))
                    score -= 3
                if "strength" not in paper:
                    results.append(ValidationResult(
                        field=f"evidence.pro[{i}]",
                        severity=ValidationSeverity.WARNING,
                        message="Evidence strength not specified",
                        suggestion=f"Add 'strength' field ({'/'.join(VALID_EVIDENCE_STRENGTH)})"
                    ))
                    score -= 3

        # Check CONTRA evidence (should at least be documented)
        if "contra" not in evidence:
            results.append(ValidationResult(
                field="evidence.contra",
                severity=ValidationSeverity.WARNING,
                message="CONTRA evidence section missing",
                suggestion="Add 'contra' section (can be empty list with note)"
            ))
            score -= 5

        # Check summary
        if "summary" not in evidence:
            results.append(ValidationResult(
                field="evidence.summary",
                severity=ValidationSeverity.WARNING,
                message="Evidence summary missing",
                suggestion="Add 'summary' with pro_count, contra_count, confidence"
            ))
            score -= 5
        else:
            summary = evidence["summary"]
            if "confidence" not in summary:
                results.append(ValidationResult(
                    field="evidence.summary.confidence",
                    severity=ValidationSeverity.WARNING,
                    message="Confidence level not specified",
                    suggestion=f"Add 'confidence' ({'/'.join(VALID_CONFIDENCE_LEVELS)})"
                ))
                score -= 3

    # Validate decision
    if "decision" in concept:
        decision = concept["decision"]
        if decision not in VALID_DECISIONS:
            results.append(ValidationResult(
                field="decision",
                severity=ValidationSeverity.ERROR,
                message=f"Invalid decision: {decision}",
                suggestion=f"Use one of: {', '.join(VALID_DECISIONS)}"
            ))
            score -= 10

        # If integrated, check integration details
        if decision == "integrate":
            if "integration" not in concept:
                results.append(ValidationResult(
                    field="integration",
                    severity=ValidationSeverity.ERROR,
                    message="Integration details missing for 'integrate' decision",
                    suggestion="Add 'integration' section with appendix, section, chapters"
                ))
                score -= 10
            else:
                integration = concept["integration"]
                if "appendix" not in integration:
                    results.append(ValidationResult(
                        field="integration.appendix",
                        severity=ValidationSeverity.WARNING,
                        message="Target appendix not specified",
                        suggestion="Add 'appendix' field"
                    ))
                    score -= 5

    # Validate decision_rationale
    if "decision_rationale" not in concept:
        results.append(ValidationResult(
            field="decision_rationale",
            severity=ValidationSeverity.WARNING,
            message="Decision rationale missing",
            suggestion="Add 'decision_rationale' explaining why this decision was made"
        ))
        score -= 5

    # Validate session date
    if "session" in concept:
        session = concept["session"]
        if not re.match(r"\d{4}-\d{2}-\d{2}", session):
            results.append(ValidationResult(
                field="session",
                severity=ValidationSeverity.WARNING,
                message=f"Invalid date format: {session}",
                suggestion="Use format: YYYY-MM-DD"
            ))
            score -= 3

    return results, max(0, score)


def validate_registry(registry_path: Path) -> Tuple[Dict, int]:
    """Validate the entire concept registry."""
    results = {
        "concepts": [],
        "errors": [],
        "warnings": [],
        "info": []
    }
    total_score = 0

    try:
        with open(registry_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except Exception as e:
        results["errors"].append(f"Failed to load registry: {e}")
        return results, 0

    if "concepts" not in data or not data["concepts"]:
        results["warnings"].append("No concepts in registry")
        return results, 100

    concepts = data["concepts"]
    scores = []

    for concept in concepts:
        concept_id = concept.get("concept_id", "UNKNOWN")
        concept_results, score = validate_concept(concept)
        scores.append(score)

        results["concepts"].append({
            "id": concept_id,
            "name": concept.get("name", "Unknown"),
            "score": score,
            "results": concept_results
        })

        for r in concept_results:
            if r.severity == ValidationSeverity.ERROR:
                results["errors"].append(f"[{concept_id}] {r.field}: {r.message}")
            elif r.severity == ValidationSeverity.WARNING:
                results["warnings"].append(f"[{concept_id}] {r.field}: {r.message}")
            else:
                results["info"].append(f"[{concept_id}] {r.field}: {r.message}")

    total_score = sum(scores) // len(scores) if scores else 0

    # Check statistics consistency
    if "statistics" in data:
        stats = data["statistics"]
        actual_total = len(concepts)
        if stats.get("total_concepts", 0) != actual_total:
            results["warnings"].append(
                f"Statistics mismatch: total_concepts={stats.get('total_concepts')} but found {actual_total}"
            )

    return results, total_score


def validate_rejected_concepts(rejected_path: Path) -> Tuple[List[str], int]:
    """Validate rejected_concepts.md structure."""
    warnings = []
    score = 100

    try:
        with open(rejected_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return [f"Failed to read file: {e}"], 0

    # Check required sections
    required_sections = [
        "# Rejected Concepts Registry",
        "## Entscheidungsmatrix",
        "## Register der verworfenen Konzepte",
        "## Re-Evaluation Prozess"
    ]

    for section in required_sections:
        if section not in content:
            warnings.append(f"Missing section: {section}")
            score -= 10

    # Check template format
    if "rejected_concept:" not in content:
        warnings.append("No YAML template found")
        score -= 5

    return warnings, max(0, score)


def print_results(results: Dict, total_score: int, verbose: bool = False):
    """Print validation results."""
    print("\n" + "=" * 70)
    print("EBF Evidence Integration Pipeline (EIP) Compliance Report")
    print("=" * 70)

    # Overall score
    if total_score >= 85:
        status = "PASS"
        color = "\033[92m"  # Green
    elif total_score >= 70:
        status = "WARNING"
        color = "\033[93m"  # Yellow
    else:
        status = "FAIL"
        color = "\033[91m"  # Red

    print(f"\nOverall Score: {color}{total_score}% ({status})\033[0m")
    print("-" * 70)

    # Per-concept scores
    if results.get("concepts"):
        print("\nConcept Scores:")
        for concept in results["concepts"]:
            score_color = "\033[92m" if concept["score"] >= 85 else "\033[93m" if concept["score"] >= 70 else "\033[91m"
            print(f"  {concept['id']}: {score_color}{concept['score']}%\033[0m - {concept['name']}")

    # Errors
    if results.get("errors"):
        print(f"\n\033[91mERRORS ({len(results['errors'])}):\033[0m")
        for error in results["errors"]:
            print(f"  - {error}")

    # Warnings
    if results.get("warnings"):
        print(f"\n\033[93mWARNINGS ({len(results['warnings'])}):\033[0m")
        for warning in results["warnings"]:
            print(f"  - {warning}")

    # Info (only if verbose)
    if verbose and results.get("info"):
        print(f"\n\033[94mINFO ({len(results['info'])}):\033[0m")
        for info in results["info"]:
            print(f"  - {info}")

    print("\n" + "=" * 70)

    # Summary
    print("\nSummary:")
    print(f"  - Total concepts validated: {len(results.get('concepts', []))}")
    print(f"  - Errors: {len(results.get('errors', []))}")
    print(f"  - Warnings: {len(results.get('warnings', []))}")
    print(f"  - Required score for commit: >= 85%")
    print("\n" + "=" * 70)


def show_stats(registry_path: Path):
    """Show EIP statistics."""
    try:
        with open(registry_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading registry: {e}")
        return

    print("\n" + "=" * 70)
    print("EIP Statistics")
    print("=" * 70)

    if "statistics" in data:
        stats = data["statistics"]
        print(f"\n  Total concepts: {stats.get('total_concepts', 0)}")
        print(f"  Integrated: {stats.get('integrated', 0)}")
        print(f"  Rejected: {stats.get('rejected', 0)}")
        print(f"  Modified: {stats.get('modified', 0)}")
        print(f"  Last updated: {stats.get('last_updated', 'Unknown')}")

    if "concepts" in data:
        concepts = data["concepts"]

        # Count by trigger
        trigger_counts = {}
        for concept in concepts:
            for trigger in concept.get("triggers", []):
                for t in VALID_TRIGGERS:
                    if t in trigger:
                        trigger_counts[t] = trigger_counts.get(t, 0) + 1

        print("\n  Concepts by trigger:")
        for t in VALID_TRIGGERS:
            count = trigger_counts.get(t, 0)
            desc = TRIGGER_DESCRIPTIONS.get(t, "")
            print(f"    {t}: {count} ({desc})")

        # Count by decision
        decision_counts = {}
        for concept in concepts:
            decision = concept.get("decision", "unknown")
            decision_counts[decision] = decision_counts.get(decision, 0) + 1

        print("\n  Concepts by decision:")
        for decision in VALID_DECISIONS:
            count = decision_counts.get(decision, 0)
            print(f"    {decision}: {count}")

    print("\n" + "=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="EBF Evidence Integration Pipeline (EIP) Compliance Checker"
    )
    parser.add_argument(
        "--concept",
        help="Validate specific concept by ID"
    )
    parser.add_argument(
        "--rejected",
        action="store_true",
        help="Validate rejected_concepts.md"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Validate everything"
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show EIP statistics"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show verbose output"
    )

    args = parser.parse_args()

    # Paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    registry_path = project_root / "data" / "concept-registry.yaml"
    rejected_path = project_root / "quality" / "rejected_concepts.md"

    if args.stats:
        show_stats(registry_path)
        return 0

    if args.rejected or args.all:
        print("\nValidating rejected_concepts.md...")
        warnings, score = validate_rejected_concepts(rejected_path)
        if warnings:
            print(f"\n\033[93mWarnings:\033[0m")
            for w in warnings:
                print(f"  - {w}")
        print(f"\nrejected_concepts.md score: {score}%")

    if args.concept:
        # Validate specific concept
        try:
            with open(registry_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading registry: {e}")
            return 1

        concept = None
        for c in data.get("concepts", []):
            if c.get("concept_id") == args.concept:
                concept = c
                break

        if not concept:
            print(f"Concept {args.concept} not found")
            return 1

        results, score = validate_concept(concept)
        print(f"\nValidating {args.concept}...")
        for r in results:
            severity_color = {
                ValidationSeverity.ERROR: "\033[91m",
                ValidationSeverity.WARNING: "\033[93m",
                ValidationSeverity.INFO: "\033[94m"
            }
            print(f"  {severity_color[r.severity]}{r.severity.value}\033[0m: {r.field} - {r.message}")
            if r.suggestion:
                print(f"    Suggestion: {r.suggestion}")
        print(f"\nScore: {score}%")
        return 0 if score >= 85 else 1

    # Default: validate entire registry
    print(f"\nValidating {registry_path}...")
    results, total_score = validate_registry(registry_path)
    print_results(results, total_score, args.verbose)

    return 0 if total_score >= 85 else 1


if __name__ == "__main__":
    sys.exit(main())
