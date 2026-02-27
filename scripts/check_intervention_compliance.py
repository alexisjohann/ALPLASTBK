#!/usr/bin/env python3
"""
EBF Intervention Compliance Checker

Validates interventions against the 20-Field Schema (Chapter 17).
Ensures all interventions follow EBF standards and meet quality thresholds.

Usage:
    python scripts/check_intervention_compliance.py <intervention_file.yaml>
    python scripts/check_intervention_compliance.py --portfolio <portfolio_file.yaml>
    python scripts/check_intervention_compliance.py --all data/interventions/
    python scripts/check_intervention_compliance.py --template  # Show template

Reference: templates/intervention-schema.yaml, Chapter 17
"""

import sys
import yaml
import argparse
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
# REFERENCE DATA FROM CHAPTER 17
# =============================================================================

# 10C Intervention Dimensions (emergent continuous space, NOT discrete types)
# Legacy T1-T8 notation is DEPRECATED - use I_AWARE, I_WHO, etc.
VALID_TYPES = [
    "I_AWARE",      # Information/Awareness (formerly T1)
    "I_AWARE_k",    # Feedback (formerly T2)
    "I_WHEN",       # Choice Architecture/Context (formerly T3)
    "I_WHEN_t",     # Temporal/Timing (formerly T4)
    "I_WHO",        # Identity/Self-concept (formerly T5)
    "I_WHO_o",      # Social/Norms (formerly T6)
    "I_WHAT_F",     # Financial (formerly T7)
    "I_HOW"         # Commitment/Pre-commitment (formerly T8)
]

TYPE_TARGETS = {
    "I_AWARE": "A(·)",
    "I_AWARE_k": "κ_AWX",
    "I_WHEN": "κ_KON",
    "I_WHEN_t": "κ_JNY",
    "I_WHO": "W_base",
    "I_WHO_o": "u_S",
    "I_WHAT_F": "u_F",
    "I_HOW": "γ_ij"
}

TYPE_NAMES = {
    "I_AWARE": "Awareness",
    "I_AWARE_k": "Feedback",
    "I_WHEN": "Contextual",
    "I_WHEN_t": "Temporal",
    "I_WHO": "Identity",
    "I_WHO_o": "Social",
    "I_WHAT_F": "Financial",
    "I_HOW": "Commitment"
}

VALID_PHASES = ["awareness", "triggered", "action", "maintenance", "stable"]

VALID_TARGETS = ["IND", "IDN", "COL"]

VALID_FEPSDE = ["F", "E", "P", "S", "D", "X"]

VALID_SCOPES = ["instant", "operative", "tactical", "strategic", "systemic"]

VALID_DECISION_LEVELS = ["L0", "L1", "L1+", "L2", "L3"]

VALID_SEGMENTS = [
    "present_biased", "social_oriented", "autonomy_seeking",
    "loss_averse", "sophisticates", "naifs"
]

VALID_FRAMINGS = ["positive", "negative", "social", "neutral"]

VALID_AUTONOMY_LEVELS = ["voluntary", "default", "mandate", "prohibition"]

VALID_PATH_FUNCTIONS = ["door_opener", "escalator", "amplifier", "stabilizer"]

# Phase-Type Affinity Matrix (Chapter 18)
PHASE_TYPE_AFFINITY = {
    "T1": {"awareness": 0.9, "triggered": 0.6, "action": 0.3, "maintenance": 0.2, "stable": 0.1},
    "T2": {"awareness": 0.3, "triggered": 0.5, "action": 0.9, "maintenance": 0.8, "stable": 0.4},
    "T3": {"awareness": 0.2, "triggered": 0.8, "action": 0.9, "maintenance": 0.5, "stable": 0.3},
    "T4": {"awareness": 0.4, "triggered": 0.9, "action": 0.6, "maintenance": 0.3, "stable": 0.2},
    "T5": {"awareness": 0.2, "triggered": 0.3, "action": 0.4, "maintenance": 0.7, "stable": 0.9},
    "T6": {"awareness": 0.8, "triggered": 0.7, "action": 0.5, "maintenance": 0.6, "stable": 0.4},
    "T7": {"awareness": 0.2, "triggered": 0.5, "action": 0.9, "maintenance": 0.4, "stable": 0.2},
    "T8": {"awareness": 0.3, "triggered": 0.8, "action": 0.7, "maintenance": 0.5, "stable": 0.3},
}

# Known Crowding-Out Conflicts (Chapter 20)
KNOWN_CONFLICTS = {
    ("T6", "T7"): {"gamma": -0.2, "desc": "Social norms undermined by financial incentives"},
    ("T7", "T8"): {"gamma": -0.3, "desc": "Commitment undermined by external rewards"},
}

# Scope-Level Compatibility
SCOPE_LEVEL_COMPAT = {
    "instant": ["L0"],
    "operative": ["L0", "L1"],
    "tactical": ["L1", "L1+"],
    "strategic": ["L1+", "L2"],
    "systemic": ["L2", "L3"],
}


# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def validate_intervention(data: Dict, depth: str = "hybrid") -> List[ValidationResult]:
    """
    Validate an intervention against the 20-Field Schema.

    Args:
        data: Intervention data dictionary
        depth: Application depth - "light", "hybrid", or "profound"

    Returns:
        List of ValidationResult objects
    """
    results = []

    # Define required fields per depth
    light_fields = ["F1_title", "F2_intervention_type", "F4_target_structure",
                    "F5_fepsde_dimension", "F6_journey_phase"]
    hybrid_fields = light_fields + ["F7_framing", "F8_autonomy", "F9_target_segment",
                                     "F10_complementarity", "F11_side_effects", "F12_temporal_scope"]
    profound_fields = hybrid_fields + ["F13_evaluation", "F14_path_function", "F15_repetition",
                                        "F16_responsibility", "F17_evidence", "F19_description", "F20_status"]

    required_fields = {
        "light": light_fields,
        "hybrid": hybrid_fields,
        "profound": profound_fields
    }.get(depth, hybrid_fields)

    # Check required fields exist
    for field in required_fields:
        if field not in data:
            results.append(ValidationResult(
                field=field,
                severity=ValidationSeverity.ERROR,
                message=f"Required field '{field}' is missing",
                suggestion=f"Add '{field}' to the intervention specification"
            ))

    # Validate F2: Intervention Type
    results.extend(_validate_f2_type(data))

    # Validate F4: Target Structure
    results.extend(_validate_f4_target(data))

    # Validate F5: FEPSDE Dimension
    results.extend(_validate_f5_fepsde(data))

    # Validate F6: Journey Phase
    results.extend(_validate_f6_phase(data))

    # Validate F8: Autonomy (for hybrid/profound)
    if depth in ["hybrid", "profound"] and "F8_autonomy" in data:
        results.extend(_validate_f8_autonomy(data))

    # Validate F9: Target Segment (for hybrid/profound)
    if depth in ["hybrid", "profound"] and "F9_target_segment" in data:
        results.extend(_validate_f9_segment(data))

    # Validate F10: Complementarity (for hybrid/profound)
    if depth in ["hybrid", "profound"] and "F10_complementarity" in data:
        results.extend(_validate_f10_complementarity(data))

    # Validate F12: Temporal Scope (for hybrid/profound)
    if depth in ["hybrid", "profound"] and "F12_temporal_scope" in data:
        results.extend(_validate_f12_scope(data))

    # Cross-field validations
    results.extend(_validate_phase_type_affinity(data))
    results.extend(_validate_crowding_out(data))

    return results


def _validate_f2_type(data: Dict) -> List[ValidationResult]:
    """Validate F2: Intervention Type"""
    results = []
    f2 = data.get("F2_intervention_type", {})

    code = f2.get("code")
    if code not in VALID_TYPES:
        results.append(ValidationResult(
            field="F2_intervention_type.code",
            severity=ValidationSeverity.ERROR,
            message=f"Invalid intervention type '{code}'",
            suggestion=f"Must be one of: {', '.join(VALID_TYPES)}"
        ))
    else:
        # Check target component consistency
        expected_target = TYPE_TARGETS.get(code)
        actual_target = f2.get("target_component")
        if actual_target and actual_target != expected_target:
            results.append(ValidationResult(
                field="F2_intervention_type.target_component",
                severity=ValidationSeverity.ERROR,
                message=f"Target component '{actual_target}' doesn't match type {code}",
                suggestion=f"For {code}, target should be '{expected_target}'"
            ))

    return results


def _validate_f4_target(data: Dict) -> List[ValidationResult]:
    """Validate F4: Target Structure"""
    results = []
    f4 = data.get("F4_target_structure", {})

    level = f4.get("level")
    if level and level not in VALID_TARGETS:
        results.append(ValidationResult(
            field="F4_target_structure.level",
            severity=ValidationSeverity.ERROR,
            message=f"Invalid target level '{level}'",
            suggestion=f"Must be one of: {', '.join(VALID_TARGETS)}"
        ))

    return results


def _validate_f5_fepsde(data: Dict) -> List[ValidationResult]:
    """Validate F5: FEPSDE Dimension"""
    results = []
    f5 = data.get("F5_fepsde_dimension", {})

    primary = f5.get("primary")
    if primary and primary not in VALID_FEPSDE:
        results.append(ValidationResult(
            field="F5_fepsde_dimension.primary",
            severity=ValidationSeverity.ERROR,
            message=f"Invalid FEPSDE dimension '{primary}'",
            suggestion=f"Must be one of: {', '.join(VALID_FEPSDE)}"
        ))

    # Check weights sum to ~1 if provided
    weights = f5.get("weights", {})
    if weights:
        total = sum(weights.values())
        if total > 0 and abs(total - 1.0) > 0.05:
            results.append(ValidationResult(
                field="F5_fepsde_dimension.weights",
                severity=ValidationSeverity.WARNING,
                message=f"FEPSDE weights sum to {total:.2f}, expected ~1.0",
                suggestion="Normalize weights to sum to 1.0"
            ))

    return results


def _validate_f6_phase(data: Dict) -> List[ValidationResult]:
    """Validate F6: Journey Phase"""
    results = []
    f6 = data.get("F6_journey_phase", {})

    optimal = f6.get("optimal_phases", [])
    for phase in optimal:
        if phase not in VALID_PHASES:
            results.append(ValidationResult(
                field="F6_journey_phase.optimal_phases",
                severity=ValidationSeverity.ERROR,
                message=f"Invalid phase '{phase}'",
                suggestion=f"Must be one of: {', '.join(VALID_PHASES)}"
            ))

    # Check phase affinity has at least one high value
    affinity = f6.get("phase_affinity", {})
    if affinity:
        max_affinity = max(affinity.values()) if affinity.values() else 0
        if max_affinity < 0.5:
            results.append(ValidationResult(
                field="F6_journey_phase.phase_affinity",
                severity=ValidationSeverity.WARNING,
                message=f"No phase has affinity > 0.5 (max: {max_affinity:.2f})",
                suggestion="At least one phase should have α > 0.5"
            ))

    return results


def _validate_f8_autonomy(data: Dict) -> List[ValidationResult]:
    """Validate F8: Autonomy Level"""
    results = []
    f8 = data.get("F8_autonomy", {})

    level = f8.get("level")
    if level and level not in VALID_AUTONOMY_LEVELS:
        results.append(ValidationResult(
            field="F8_autonomy.level",
            severity=ValidationSeverity.ERROR,
            message=f"Invalid autonomy level '{level}'",
            suggestion=f"Must be one of: {', '.join(VALID_AUTONOMY_LEVELS)}"
        ))

    # Check reactance handling
    reactance = f8.get("reactance_risk")
    cue_required = f8.get("autonomy_cue_required", False)
    if reactance == "high" and not cue_required:
        results.append(ValidationResult(
            field="F8_autonomy",
            severity=ValidationSeverity.ERROR,
            message="High reactance risk but autonomy cue not required",
            suggestion="Set autonomy_cue_required=true for high reactance interventions"
        ))

    return results


def _validate_f9_segment(data: Dict) -> List[ValidationResult]:
    """Validate F9: Target Segment"""
    results = []
    f9 = data.get("F9_target_segment", {})

    multipliers = f9.get("segment_multipliers", {})
    warnings_list = f9.get("warnings", [])

    # Check for negative multipliers without warnings
    for segment, sigma in multipliers.items():
        if segment not in VALID_SEGMENTS:
            results.append(ValidationResult(
                field="F9_target_segment.segment_multipliers",
                severity=ValidationSeverity.WARNING,
                message=f"Unknown segment '{segment}'",
                suggestion=f"Known segments: {', '.join(VALID_SEGMENTS)}"
            ))

        if sigma < 0 and segment not in str(warnings_list):
            results.append(ValidationResult(
                field="F9_target_segment",
                severity=ValidationSeverity.ERROR,
                message=f"Segment '{segment}' has σ={sigma} < 0 (BACKFIRE RISK) but not in warnings",
                suggestion=f"Add '{segment}' to warnings list with mitigation strategy"
            ))

    return results


def _validate_f10_complementarity(data: Dict) -> List[ValidationResult]:
    """Validate F10: Complementarity"""
    results = []
    f10 = data.get("F10_complementarity", {})

    conflicts = f10.get("conflicts", [])
    synergies = f10.get("synergies", [])

    # Check gamma values are in valid range
    for item in conflicts + synergies:
        gamma = item.get("gamma", 0)
        if abs(gamma) > 1:
            results.append(ValidationResult(
                field="F10_complementarity",
                severity=ValidationSeverity.ERROR,
                message=f"Gamma value {gamma} out of range [-1, 1]",
                suggestion="Gamma must be between -1 and 1"
            ))

    return results


def _validate_f12_scope(data: Dict) -> List[ValidationResult]:
    """Validate F12: Temporal Scope"""
    results = []
    f12 = data.get("F12_temporal_scope", {})

    scope = f12.get("scope")
    if scope and scope not in VALID_SCOPES:
        results.append(ValidationResult(
            field="F12_temporal_scope.scope",
            severity=ValidationSeverity.ERROR,
            message=f"Invalid temporal scope '{scope}'",
            suggestion=f"Must be one of: {', '.join(VALID_SCOPES)}"
        ))

    # Check scope-level compatibility
    level = f12.get("decision_level")
    if scope and level:
        valid_levels = SCOPE_LEVEL_COMPAT.get(scope, [])
        if level not in valid_levels:
            results.append(ValidationResult(
                field="F12_temporal_scope",
                severity=ValidationSeverity.WARNING,
                message=f"Scope '{scope}' typically requires level {valid_levels}, not {level}",
                suggestion=f"Consider using decision level: {', '.join(valid_levels)}"
            ))

    return results


def _validate_phase_type_affinity(data: Dict) -> List[ValidationResult]:
    """Cross-validate phase selection against type affinity"""
    results = []

    f2 = data.get("F2_intervention_type", {})
    f6 = data.get("F6_journey_phase", {})

    type_code = f2.get("code")
    optimal_phases = f6.get("optimal_phases", [])

    if type_code and type_code in PHASE_TYPE_AFFINITY:
        affinity = PHASE_TYPE_AFFINITY[type_code]
        for phase in optimal_phases:
            if phase in affinity:
                alpha = affinity[phase]
                if alpha < 0.5:
                    results.append(ValidationResult(
                        field="F6_journey_phase.optimal_phases",
                        severity=ValidationSeverity.WARNING,
                        message=f"Phase '{phase}' has low affinity (α={alpha}) for type {type_code}",
                        suggestion=f"Consider phases with higher affinity for {type_code}: " +
                                   ", ".join([p for p, a in affinity.items() if a >= 0.7])
                    ))

    return results


def _validate_crowding_out(data: Dict) -> List[ValidationResult]:
    """Check for crowding-out risks in portfolio context"""
    results = []

    f2 = data.get("F2_intervention_type", {})
    f10 = data.get("F10_complementarity", {})

    type_code = f2.get("code")
    crowding_warnings = f10.get("crowding_out_warnings", [])

    # Check if this type has known conflicts that should be documented
    for (t1, t2), conflict_info in KNOWN_CONFLICTS.items():
        if type_code in (t1, t2):
            # Check if this conflict is documented
            conflict_mentioned = any(
                t1 in str(w) and t2 in str(w)
                for w in crowding_warnings
            )
            if not conflict_mentioned:
                results.append(ValidationResult(
                    field="F10_complementarity.crowding_out_warnings",
                    severity=ValidationSeverity.INFO,
                    message=f"Type {type_code} has known conflict with {t2 if type_code == t1 else t1}",
                    suggestion=f"Document: {conflict_info['desc']} (γ={conflict_info['gamma']})"
                ))

    return results


# =============================================================================
# PORTFOLIO VALIDATION
# =============================================================================

def validate_portfolio(interventions: List[Dict]) -> List[ValidationResult]:
    """
    Validate a portfolio of interventions for coherence.

    Checks:
    - C1: No negative complementarity
    - C2: Journey coverage
    - C3: Segment coverage
    - C4: Context consistency
    """
    results = []
    types_in_portfolio = []
    phases_covered = set()
    segments_covered = set()

    # Collect types and coverage
    for i, intv in enumerate(interventions):
        f2 = intv.get("F2_intervention_type", {})
        type_code = f2.get("code")
        if type_code:
            types_in_portfolio.append(type_code)

        f6 = intv.get("F6_journey_phase", {})
        phases_covered.update(f6.get("optimal_phases", []))

        f9 = intv.get("F9_target_segment", {})
        segments_covered.update(f9.get("optimal_segments", []))

    # C1: Check for conflicting pairs
    for i, t1 in enumerate(types_in_portfolio):
        for t2 in types_in_portfolio[i+1:]:
            pair = tuple(sorted([t1, t2]))
            if pair in KNOWN_CONFLICTS:
                conflict = KNOWN_CONFLICTS[pair]
                results.append(ValidationResult(
                    field="portfolio",
                    severity=ValidationSeverity.ERROR,
                    message=f"Portfolio contains conflicting types {t1} and {t2}",
                    suggestion=f"CROWDING-OUT RISK: {conflict['desc']} (γ={conflict['gamma']})"
                ))

    # C2: Journey coverage
    missing_phases = set(VALID_PHASES) - phases_covered
    if missing_phases:
        results.append(ValidationResult(
            field="portfolio.journey_coverage",
            severity=ValidationSeverity.WARNING,
            message=f"Portfolio doesn't cover phases: {', '.join(missing_phases)}",
            suggestion="Consider adding interventions for missing phases"
        ))

    # C3: Segment coverage (informational)
    if segments_covered:
        results.append(ValidationResult(
            field="portfolio.segment_coverage",
            severity=ValidationSeverity.INFO,
            message=f"Portfolio targets segments: {', '.join(segments_covered)}",
            suggestion=None
        ))

    return results


# =============================================================================
# SCORING
# =============================================================================

def calculate_score(results: List[ValidationResult]) -> Tuple[float, str]:
    """
    Calculate compliance score from validation results.

    Returns:
        Tuple of (score percentage, grade)
    """
    errors = sum(1 for r in results if r.severity == ValidationSeverity.ERROR)
    warnings = sum(1 for r in results if r.severity == ValidationSeverity.WARNING)

    # Scoring: Start at 100, -10 per error, -3 per warning
    score = max(0, 100 - (errors * 10) - (warnings * 3))

    if score >= 85:
        grade = "PASS"
    elif score >= 70:
        grade = "MARGINAL"
    else:
        grade = "FAIL"

    return score, grade


# =============================================================================
# OUTPUT FORMATTING
# =============================================================================

def format_results(results: List[ValidationResult], score: float, grade: str) -> str:
    """Format validation results for console output"""
    lines = []

    # Header
    lines.append("=" * 70)
    lines.append("EBF INTERVENTION COMPLIANCE CHECK")
    lines.append("=" * 70)
    lines.append("")

    # Score
    score_color = "✅" if grade == "PASS" else "⚠️" if grade == "MARGINAL" else "❌"
    lines.append(f"Score: {score:.0f}% {score_color} {grade}")
    lines.append("")

    # Count by severity
    errors = [r for r in results if r.severity == ValidationSeverity.ERROR]
    warnings = [r for r in results if r.severity == ValidationSeverity.WARNING]
    infos = [r for r in results if r.severity == ValidationSeverity.INFO]

    lines.append(f"Errors: {len(errors)} | Warnings: {len(warnings)} | Info: {len(infos)}")
    lines.append("-" * 70)

    # Errors first
    if errors:
        lines.append("")
        lines.append("❌ ERRORS (must fix):")
        for r in errors:
            lines.append(f"  [{r.field}]")
            lines.append(f"    {r.message}")
            if r.suggestion:
                lines.append(f"    → {r.suggestion}")

    # Warnings
    if warnings:
        lines.append("")
        lines.append("⚠️ WARNINGS (should fix):")
        for r in warnings:
            lines.append(f"  [{r.field}]")
            lines.append(f"    {r.message}")
            if r.suggestion:
                lines.append(f"    → {r.suggestion}")

    # Info
    if infos:
        lines.append("")
        lines.append("ℹ️ INFO:")
        for r in infos:
            lines.append(f"  [{r.field}]")
            lines.append(f"    {r.message}")
            if r.suggestion:
                lines.append(f"    → {r.suggestion}")

    lines.append("")
    lines.append("=" * 70)

    return "\n".join(lines)


def print_template():
    """Print a minimal intervention template"""
    template = """
# EBF Intervention Template (20-Field Schema)
# Reference: Chapter 17, templates/intervention-schema.yaml

F1_title:
  id: "INT-XXX-001"
  name: "Your Intervention Title"

F2_intervention_type:
  code: "T1"  # T1-T8: Awareness/Feedback/Contextual/Temporal/Identity/Social/Financial/Commitment
  name: "Awareness"
  target_component: "A(·)"

F4_target_structure:
  level: "IND"  # IND (Individual), IDN (Dyadic), COL (Collective)

F5_fepsde_dimension:
  primary: "F"  # F/E/P/S/D/X

F6_journey_phase:
  optimal_phases: ["awareness"]  # awareness, triggered, action, maintenance, stable
  phase_affinity:
    awareness: 0.9
    triggered: 0.6
    action: 0.3
    maintenance: 0.2
    stable: 0.1

# === HYBRID MODE (add for standard design) ===

F7_framing:
  frame_type: "positive"  # positive, negative, social, neutral

F8_autonomy:
  level: "voluntary"  # voluntary, default, mandate, prohibition
  reactance_risk: "low"  # low, medium, high
  autonomy_cue_required: false

F9_target_segment:
  optimal_segments: ["social_oriented"]
  segment_multipliers:
    present_biased: 1.0
    social_oriented: 1.2
    autonomy_seeking: 1.0
    loss_averse: 1.0
  warnings: []

F10_complementarity:
  synergies: []
  conflicts: []
  crowding_out_warnings:
    - "T6+T7: γ=-0.2 if combining social and financial"

F11_side_effects:
  risk_level: "low"
  positive_spillovers: []
  negative_spillovers: []

F12_temporal_scope:
  scope: "tactical"  # instant, operative, tactical, strategic, systemic
  duration_weeks: 12
  decision_level: "L1"  # L0, L1, L1+, L2, L3
"""
    print(template)


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="EBF Intervention Compliance Checker (Chapter 17)"
    )
    parser.add_argument("file", nargs="?", help="Intervention YAML file to validate")
    parser.add_argument("--portfolio", help="Validate a portfolio of interventions")
    parser.add_argument("--all", help="Validate all interventions in directory")
    parser.add_argument("--depth", choices=["light", "hybrid", "profound"],
                        default="hybrid", help="Validation depth")
    parser.add_argument("--template", action="store_true", help="Print intervention template")

    args = parser.parse_args()

    if args.template:
        print_template()
        return 0

    if not args.file and not args.portfolio and not args.all:
        parser.print_help()
        return 1

    if args.file:
        path = Path(args.file)
        if not path.exists():
            print(f"Error: File not found: {args.file}")
            return 1

        with open(path) as f:
            data = yaml.safe_load(f)

        results = validate_intervention(data, args.depth)
        score, grade = calculate_score(results)
        print(format_results(results, score, grade))

        return 0 if grade == "PASS" else 1

    if args.portfolio:
        path = Path(args.portfolio)
        if not path.exists():
            print(f"Error: File not found: {args.portfolio}")
            return 1

        with open(path) as f:
            data = yaml.safe_load(f)

        interventions = data.get("interventions", [data])

        # Validate each intervention
        all_results = []
        for i, intv in enumerate(interventions):
            print(f"\n--- Intervention {i+1} ---")
            results = validate_intervention(intv, args.depth)
            all_results.extend(results)
            score, grade = calculate_score(results)
            print(format_results(results, score, grade))

        # Portfolio-level validation
        print("\n--- Portfolio Analysis ---")
        portfolio_results = validate_portfolio(interventions)
        all_results.extend(portfolio_results)

        for r in portfolio_results:
            icon = {"ERROR": "❌", "WARNING": "⚠️", "INFO": "ℹ️"}[r.severity.value]
            print(f"{icon} {r.message}")
            if r.suggestion:
                print(f"   → {r.suggestion}")

        return 0

    if args.all:
        directory = Path(args.all)
        if not directory.is_dir():
            print(f"Error: Not a directory: {args.all}")
            return 1

        yaml_files = list(directory.glob("*.yaml")) + list(directory.glob("*.yml"))

        total_score = 0
        for path in yaml_files:
            print(f"\n{'='*70}")
            print(f"File: {path.name}")

            with open(path) as f:
                data = yaml.safe_load(f)

            results = validate_intervention(data, args.depth)
            score, grade = calculate_score(results)
            total_score += score
            print(format_results(results, score, grade))

        if yaml_files:
            avg_score = total_score / len(yaml_files)
            print(f"\n{'='*70}")
            print(f"Average Score: {avg_score:.1f}%")

        return 0


if __name__ == "__main__":
    sys.exit(main())
