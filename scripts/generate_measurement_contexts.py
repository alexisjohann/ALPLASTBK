#!/usr/bin/env python3
"""
Generate Measurement Contexts from Parameter Registry
======================================================

Extracts measurement_contexts triplets from parameter-registry.yaml
by mapping domain_specific values and literature_sources to PCT-compatible
(parameter, context, psi_conditions) triplets.

This script reads existing parameter data and generates new measurement
contexts that enable PCT transformation for parameters that currently
lack contexts.

Usage:
    python generate_measurement_contexts.py               # Generate + merge
    python generate_measurement_contexts.py --dry-run     # Preview only
    python generate_measurement_contexts.py --stats       # Statistics

Layer: 1 (Formal Computation)
"""

import sys
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from collections import defaultdict
from datetime import date

REPO_ROOT = Path(__file__).resolve().parent.parent
PARAM_REGISTRY_PATH = REPO_ROOT / "data" / "parameter-registry.yaml"
EXISTING_CONTEXTS_PATH = REPO_ROOT / "data" / "pct-measurement-contexts.yaml"
PSI_SCALES_PATH = REPO_ROOT / "data" / "pct-psi-scales.yaml"
OUTPUT_PATH = REPO_ROOT / "data" / "pct-measurement-contexts.yaml"


def load_yaml(path: Path) -> Optional[Dict]:
    """Load a YAML file."""
    try:
        import yaml
    except ImportError:
        print("ERROR: PyYAML required")
        sys.exit(1)
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_yaml(data: Dict, path: Path) -> None:
    """Save data to YAML."""
    import yaml
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True,
                  sort_keys=False, width=120)


# Domain → Psi-condition mappings based on EBF context theory
DOMAIN_PSI_MAP = {
    # Finance domains
    "finance": {
        "psi_I": "market_regulatory_environment",
        "psi_E": "moderate_stakes_auction",
        "psi_M": "automated_digital_system",
    },
    "finance_retirement": {
        "psi_I": "optout_default",
        "psi_E": "high_stakes_car_purchase",
        "psi_T": "long_term_habit_accumulation",
    },
    "finance_savings": {
        "psi_I": "optout_default",
        "psi_E": "moderate_stakes_auction",
    },
    "finance_referral": {
        "psi_S": "ongoing_relationship",
        "psi_E": "moderate_stakes_auction",
    },
    "finance_insurance": {
        "psi_I": "market_regulatory_environment",
        "psi_E": "high_stakes_car_purchase",
        "psi_S": "customer_segment_dependent",
    },
    # Career domains
    "career": {
        "psi_S": "reputation_at_stake",
        "psi_E": "high_stakes_car_purchase",
        "psi_I": "competitive_labor_market",
    },
    "career_negotiation": {
        "psi_S": "reputation_at_stake",
        "psi_C": "performance_evaluation",
    },
    # Health domains
    "health": {
        "psi_E": "high_stakes_car_purchase",
        "psi_S": "illness_stigma",
        "psi_I": "medical_gatekeeping",
        "psi_F": "hospital_clinical",
    },
    "health_screening": {
        "psi_C": "information_avoidance",
        "psi_S": "illness_stigma",
        "psi_I": "medical_gatekeeping",
        "psi_F": "hospital_clinical",
        "psi_M": "paper_form_analog",
    },
    "health_exercise": {
        "psi_T": "repeated_practice_over_time",
        "psi_S": "social_observation",
        "psi_F": "public_outdoor",
    },
    "health_diet": {
        "psi_T": "repeated_practice_over_time",
        "psi_C": "ego_depletion_context",
    },
    "health_addiction": {
        "psi_C": "ego_depletion_context",
        "psi_T": "long_term_habit_accumulation",
        "psi_I": "medical_gatekeeping",
        "psi_F": "hospital_clinical",
    },
    # Education domains
    "education": {
        "psi_I": "university_systems",
        "psi_S": "structured_classroom_peers_teachers",
        "psi_T": "early_childhood_investment",
        "psi_F": "classroom_educational",
    },
    "education_cheating": {
        "psi_I": "university_systems",
        "psi_S": "social_observation",
        "psi_C": "performance_evaluation",
        "psi_F": "classroom_educational",
    },
    # Energy / Environmental
    "energy": {
        "psi_I": "market_regulatory_environment",
        "psi_S": "social_observation",
        "psi_K": "industry_norms",
        "psi_M": "automated_digital_system",
        "psi_F": "home_private",
    },
    "environment": {
        "psi_S": "social_observation",
        "psi_K": "industry_norms",
        "psi_F": "home_private",
    },
    # Consumer domains
    "consumer": {
        "psi_I": "purchasing_context",
        "psi_E": "low_stakes_grocery",
        "psi_F": "retail_store",
        "psi_M": "online_survey_platform",
    },
    "retail": {
        "psi_I": "german_retail_context",
        "psi_E": "low_stakes_grocery",
        "psi_F": "retail_store",
        "psi_M": "online_survey_platform",
    },
    # Labor domains
    "labor": {
        "psi_I": "competitive_labor_market",
        "psi_S": "professional_hierarchy",
    },
    "workplace_safety": {
        "psi_I": "company_context",
        "psi_S": "professional_hierarchy",
        "psi_F": "office_workplace",
    },
    # Welfare
    "welfare": {
        "psi_S": "welfare_stigma",
        "psi_I": "bureaucratic_application",
        "psi_F": "office_workplace",
        "psi_M": "paper_form_analog",
    },
    "welfare_takeup": {
        "psi_S": "welfare_stigma",
        "psi_I": "bureaucratic_application",
        "psi_E": "low_income_group",
        "psi_F": "office_workplace",
        "psi_M": "paper_form_analog",
    },
    # Prosocial
    "prosocial": {
        "psi_S": "social_observation",
        "psi_K": "reciprocity_expectation",
    },
    "charitable_giving": {
        "psi_S": "offering_signals_generosity",
        "psi_K": "reciprocity_expectation",
    },
    # DACH
    "dach_adjusted": {
        "psi_K": "german_consumer_expectations",
        "psi_I": "market_regulatory_environment",
    },
    # Political domains
    "political": {
        "psi_I": "democratic_with_labor_rights",
        "psi_S": "elite_dominated_discourse",
    },
    "political_austria": {
        "psi_I": "democratic_with_labor_rights",
        "psi_K": "german_consumer_expectations",
    },
    "political_switzerland": {
        "psi_I": "democratic_with_labor_rights",
        "psi_K": "german_consumer_expectations",
    },
    # Healthcare domains
    "healthcare": {
        "psi_I": "medical_gatekeeping",
        "psi_E": "high_stakes_car_purchase",
        "psi_S": "illness_stigma",
        "psi_F": "hospital_clinical",
    },
    "healthcare_germany": {
        "psi_I": "medical_gatekeeping",
        "psi_E": "high_stakes_car_purchase",
        "psi_K": "german_consumer_expectations",
        "psi_F": "hospital_clinical",
    },
    # Crisis management
    "crisis_management": {
        "psi_T": "timing_of_response",
        "psi_S": "public_social_media",
        "psi_C": "high_arousal_emotional",
    },
    # Customer experience / journey
    "customer_journey": {
        "psi_I": "company_context",
        "psi_T": "customer_journey_phase",
        "psi_M": "multi_channel_platform",
    },
    "customer_experience": {
        "psi_I": "company_context",
        "psi_S": "customer_segment_dependent",
        "psi_M": "multi_channel_platform",
    },
    # Real estate
    "real_estate": {
        "psi_I": "market_regulatory_environment",
        "psi_E": "high_stakes_car_purchase",
        "psi_F": "office_workplace",
    },
    "real_estate_switzerland": {
        "psi_I": "market_regulatory_environment",
        "psi_E": "high_stakes_car_purchase",
        "psi_K": "german_consumer_expectations",
        "psi_F": "office_workplace",
    },
    # Executive decision making
    "executive": {
        "psi_I": "company_context",
        "psi_S": "professional_hierarchy",
        "psi_E": "high_stakes_car_purchase",
        "psi_F": "office_workplace",
    },
    # Moral reasoning
    "moral_reasoning": {
        "psi_C": "warm_glow_active",
        "psi_S": "social_observation",
    },
    # Laboratory context
    "laboratory": {
        "psi_I": "research_ethics_protocol",
        "psi_C": "performance_evaluation",
        "psi_F": "laboratory_setting",
        "psi_M": "ztree_otree_vs_custom",
    },
    # Skill formation
    "skill_formation": {
        "psi_T": "early_childhood_investment",
        "psi_I": "structured_program_environment",
    },
    # Voting / conclave
    "voting": {
        "psi_I": "democratic_with_labor_rights",
        "psi_S": "elite_dominated_discourse",
    },
    "conclave": {
        "psi_I": "Universi_Dominici_Gregis",
        "psi_K": "Universi_Dominici_Gregis",
        "psi_F": "Sistine_Chapel",
    },
    # Time allocation
    "time_allocation": {
        "psi_T": "repeated_practice_over_time",
        "psi_E": "moderate_stakes_auction",
    },
    # Complementarity (structural interaction parameters)
    "complementarity": {
        "psi_I": "academic_methodology",
    },
    # Country-specific contexts
    "switzerland": {
        "psi_K": "german_consumer_expectations",
        "psi_I": "market_regulatory_environment",
    },
    "austria": {
        "psi_K": "german_consumer_expectations",
        "psi_I": "democratic_with_labor_rights",
    },
    "germany": {
        "psi_K": "german_consumer_expectations",
        "psi_I": "market_regulatory_environment",
    },
}


# Fallback: map parameter ID prefix to domain for parameters
# whose value keys don't match DOMAIN_PSI_MAP directly
PREFIX_DOMAIN_MAP = {
    "PAR-HLT": "healthcare_germany",
    "PAR-PP": "political_austria",
    "PAR-SF": "skill_formation",
    "PAR-VTM": "voting",
    "PAR-RE": "real_estate_switzerland",
    "PAR-CJ": "customer_journey",
    "PAR-CX": "customer_experience",
    "PAR-CM": "crisis_management",
    "PAR-EXE": "executive",
    "PAR-MR": "moral_reasoning",
    "PAR-ADV": "finance",
    "PAR-CON": "consumer",
    "PAR-CTX": "dach_adjusted",
    "PAR-TA": "time_allocation",
    "PAR-POL": "political_switzerland",
    "PAR-EC": "political",
    "PAR-COMP": "complementarity",
}


def extract_param_contexts(param: Dict) -> List[Dict]:
    """Extract measurement contexts from a single parameter entry."""
    pid = param.get("id", "")
    symbol = param.get("symbol", "")
    name = param.get("name", "")
    values = param.get("values", {})
    sources = param.get("literature_sources", [])

    contexts = []

    # 1. Extract from domain_specific values
    domain_specific = values.get("domain_specific", {})
    for domain, domain_vals in domain_specific.items():
        if not isinstance(domain_vals, dict):
            continue

        mean_val = domain_vals.get("mean", domain_vals.get("value", ""))
        ci = domain_vals.get("ci_68", domain_vals.get("ci_95", []))

        # Map domain to psi conditions
        psi_conditions = DOMAIN_PSI_MAP.get(domain, {})
        if not psi_conditions:
            # Try partial match
            for mapped_domain, psi in DOMAIN_PSI_MAP.items():
                if mapped_domain in domain or domain in mapped_domain:
                    psi_conditions = psi
                    break

        if not psi_conditions:
            continue

        value_str = str(mean_val) if mean_val else ""
        if ci:
            value_str += f" CI:{ci}"

        contexts.append({
            "paper_key": "parameter_registry",
            "paper_file": "parameter-registry.yaml",
            "parameter_symbol": symbol,
            "parameter_id": pid,
            "parameter_name": name,
            "context": f"{domain}_context",
            "value_estimate": value_str,
            "psi_conditions": dict(psi_conditions),
            "source_in_paper": f"parameter-registry.yaml domain_specific.{domain}",
            "study_type": "registry_derived",
            "countries": ["DACH"] if "dach" in domain.lower() else [],
            "n": None,
        })

    # 2. Extract DACH-adjusted as separate context
    dach = values.get("dach_adjusted", {})
    if dach and isinstance(dach, dict):
        mean_val = dach.get("mean", dach.get("value", ""))
        ci = dach.get("ci_68", [])
        note = dach.get("note", "")

        value_str = str(mean_val) if mean_val else ""
        if ci:
            value_str += f" CI:{ci}"

        psi_conditions = dict(DOMAIN_PSI_MAP.get("dach_adjusted", {}))

        contexts.append({
            "paper_key": "parameter_registry",
            "paper_file": "parameter-registry.yaml",
            "parameter_symbol": symbol,
            "parameter_id": pid,
            "parameter_name": name,
            "context": "dach_adjusted",
            "value_estimate": value_str,
            "psi_conditions": psi_conditions,
            "source_in_paper": f"parameter-registry.yaml dach_adjusted ({note})",
            "study_type": "registry_derived",
            "countries": ["CH", "AT", "DE"],
            "n": None,
        })

    # 3. Extract literature baseline
    lit = values.get("literature", values.get("literature_value", {}))
    if isinstance(lit, dict):
        mean_val = lit.get("mean", lit.get("value", ""))
        if mean_val:
            # Literature baseline = minimal psi context (lab setting)
            contexts.append({
                "paper_key": sources[0]["key"] if sources else "parameter_registry",
                "paper_file": "parameter-registry.yaml",
                "parameter_symbol": symbol,
                "parameter_id": pid,
                "parameter_name": name,
                "context": "literature_baseline",
                "value_estimate": str(mean_val),
                "psi_conditions": {},  # Baseline = no specific context
                "source_in_paper": f"parameter-registry.yaml literature ({lit.get('note', '')})",
                "study_type": "literature_meta",
                "countries": [],
                "n": None,
            })

    # 4. Extract from non-standard value keys (e.g., "laboratory", "calibrated",
    #    "individual_MW", "austria_2024", country names, etc.)
    standard_keys = {"domain_specific", "dach_adjusted", "literature", "literature_value",
                     "note", "unit", "range", "ci_68", "ci_95"}
    prefix = pid.rsplit("-", 1)[0] if "-" in pid else pid  # e.g. PAR-HLT from PAR-HLT-001
    prefix_domain = PREFIX_DOMAIN_MAP.get(prefix, "")

    for vkey, vdata in values.items():
        if vkey in standard_keys:
            continue

        # Try direct match of value key to DOMAIN_PSI_MAP
        psi_conditions = DOMAIN_PSI_MAP.get(vkey, {})

        # If not found, try partial match
        if not psi_conditions:
            for mapped_domain, psi in DOMAIN_PSI_MAP.items():
                if mapped_domain in vkey or vkey in mapped_domain:
                    psi_conditions = psi
                    break

        # Fall back to PREFIX_DOMAIN_MAP
        if not psi_conditions and prefix_domain:
            psi_conditions = DOMAIN_PSI_MAP.get(prefix_domain, {})

        if not psi_conditions:
            continue

        # Extract value
        if isinstance(vdata, dict):
            mean_val = vdata.get("mean", vdata.get("value", ""))
            ci = vdata.get("ci_68", vdata.get("ci_95", []))
            value_str = str(mean_val) if mean_val else ""
            if ci:
                value_str += f" CI:{ci}"
        elif vdata is not None:
            value_str = str(vdata)
        else:
            value_str = ""

        context_name = f"{vkey}_context"
        # Avoid duplicate with already-extracted domain_specific sub-contexts
        dup_key = (pid, context_name)
        already = any((c.get("parameter_id"), c.get("context")) == dup_key for c in contexts)
        if already:
            continue

        contexts.append({
            "paper_key": "parameter_registry",
            "paper_file": "parameter-registry.yaml",
            "parameter_symbol": symbol,
            "parameter_id": pid,
            "parameter_name": name,
            "context": context_name,
            "value_estimate": value_str,
            "psi_conditions": dict(psi_conditions),
            "source_in_paper": f"parameter-registry.yaml values.{vkey}",
            "study_type": "registry_derived",
            "countries": [],
            "n": None,
        })

    # 5. If no contexts extracted at all, try PREFIX_DOMAIN_MAP fallback
    if not contexts and prefix_domain:
        psi_conditions = DOMAIN_PSI_MAP.get(prefix_domain, {})
        if psi_conditions:
            contexts.append({
                "paper_key": "parameter_registry",
                "paper_file": "parameter-registry.yaml",
                "parameter_symbol": symbol,
                "parameter_id": pid,
                "parameter_name": name,
                "context": f"{prefix_domain}_context",
                "value_estimate": "",
                "psi_conditions": dict(psi_conditions),
                "source_in_paper": f"parameter-registry.yaml (prefix fallback {prefix})",
                "study_type": "registry_inferred",
                "countries": [],
                "n": None,
            })

    return contexts


def extract_all_param_contexts(registry_data: Dict) -> List[Dict]:
    """Extract measurement contexts from all parameters."""
    all_contexts = []

    for key, val in registry_data.items():
        if not key.endswith("_parameters") or not isinstance(val, list):
            continue
        for param in val:
            contexts = extract_param_contexts(param)
            all_contexts.extend(contexts)

    return all_contexts


def merge_contexts(existing: List[Dict], new: List[Dict]) -> List[Dict]:
    """Merge new contexts with existing, avoiding duplicates."""
    # Build key for existing
    existing_keys = set()
    for t in existing:
        key = (t.get("parameter_id", ""), t.get("context", ""))
        existing_keys.add(key)

    merged = list(existing)
    added = 0
    for t in new:
        key = (t.get("parameter_id", ""), t.get("context", ""))
        if key not in existing_keys:
            merged.append(t)
            existing_keys.add(key)
            added += 1

    return merged, added


def check_new_labels(contexts: List[Dict], scales_data: Dict) -> Dict[str, List[str]]:
    """Check if new contexts introduce unmapped psi labels."""
    scale_labels = {}
    for dim, dim_data in scales_data.get("scales", {}).items():
        scale_labels[dim] = set(dim_data.get("values", {}).keys())

    unmapped = defaultdict(list)
    for ctx in contexts:
        for dim, label in ctx.get("psi_conditions", {}).items():
            if label and dim in scale_labels and label not in scale_labels[dim]:
                if label not in unmapped[dim]:
                    unmapped[dim].append(label)

    return dict(unmapped)


def main():
    parser = argparse.ArgumentParser(
        description="Generate measurement contexts from parameter-registry.yaml",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_measurement_contexts.py              # Generate + merge
  python generate_measurement_contexts.py --dry-run    # Preview only
  python generate_measurement_contexts.py --stats      # Statistics

Layer: 1 (Formal Computation)
        """
    )

    parser.add_argument("--dry-run", action="store_true",
                        help="Preview without writing")
    parser.add_argument("--stats", action="store_true",
                        help="Show statistics only")

    args = parser.parse_args()

    # Load data
    registry = load_yaml(PARAM_REGISTRY_PATH)
    existing_data = load_yaml(EXISTING_CONTEXTS_PATH)
    scales = load_yaml(PSI_SCALES_PATH)

    if not registry:
        print(f"ERROR: {PARAM_REGISTRY_PATH} not found")
        sys.exit(1)

    existing_triplets = existing_data.get("triplets", []) if existing_data else []

    # Extract new contexts
    new_contexts = extract_all_param_contexts(registry)

    # Check for unmapped labels
    if scales:
        unmapped = check_new_labels(new_contexts, scales)
        if unmapped:
            total = sum(len(v) for v in unmapped.values())
            print(f"\nWARNING: {total} new labels not in psi-scales.yaml:")
            for dim, labels in sorted(unmapped.items()):
                for label in labels:
                    print(f"  {dim}: {label}")
            print()

    # Merge
    merged, added = merge_contexts(existing_triplets, new_contexts)

    # Stats
    existing_params = set(t.get("parameter_id") for t in existing_triplets if t.get("parameter_id"))
    new_params = set(t.get("parameter_id") for t in new_contexts if t.get("parameter_id"))
    merged_params = set(t.get("parameter_id") for t in merged if t.get("parameter_id"))

    print("=" * 60)
    print("  MEASUREMENT CONTEXT GENERATION")
    print("=" * 60)
    print(f"\n  Existing triplets:     {len(existing_triplets)}")
    print(f"  Existing parameters:   {len(existing_params)}")
    print(f"  New triplets found:    {len(new_contexts)}")
    print(f"  New parameters:        {len(new_params)}")
    print(f"  Added (deduplicated):  {added}")
    print(f"  Merged total:          {len(merged)}")
    print(f"  Merged parameters:     {len(merged_params)}")

    # Coverage
    total_params = 0
    for key, val in registry.items():
        if key.endswith("_parameters") and isinstance(val, list):
            total_params += len([p for p in val if p.get("id")])

    coverage_before = len(existing_params) / total_params * 100 if total_params else 0
    coverage_after = len(merged_params) / total_params * 100 if total_params else 0

    print(f"\n  Coverage BEFORE:       {len(existing_params)}/{total_params} ({coverage_before:.1f}%)")
    print(f"  Coverage AFTER:        {len(merged_params)}/{total_params} ({coverage_after:.1f}%)")

    bar_before = int(coverage_before / 100 * 40)
    bar_after = int(coverage_after / 100 * 40)
    print(f"  Before: [{'#' * bar_before}{'.' * (40 - bar_before)}] {coverage_before:.0f}%")
    print(f"  After:  [{'#' * bar_after}{'.' * (40 - bar_after)}] {coverage_after:.0f}%")

    if args.stats:
        # Show which params gained contexts
        gained = new_params - existing_params
        if gained:
            print(f"\n  New parameters with contexts ({len(gained)}):")
            for p in sorted(gained):
                print(f"    {p}")
        sys.exit(0)

    if args.dry_run:
        print(f"\n  DRY RUN: Would add {added} triplets to {OUTPUT_PATH}")
        sys.exit(0)

    # Write merged output
    output = {
        "version": "0.2",
        "generated": str(date.today()),
        "source": "data/paper-references/PAP-*.yaml + data/parameter-registry.yaml",
        "description": "Extracted measurement_contexts triplets for PCT",
        "n_papers": len(set(t["paper_key"] for t in merged)),
        "n_triplets": len(merged),
        "n_parameters": len(merged_params),
        "triplets": merged,
    }

    save_yaml(output, OUTPUT_PATH)
    print(f"\n  Written to: {OUTPUT_PATH}")
    print()


if __name__ == "__main__":
    main()
