#!/usr/bin/env python3
"""
CLI Wrapper for /simulate-stakeholder Skill
Integrates Python simulation engine with strategic models

Usage:
    python scripts/simulate_stakeholder_cli.py ALPLA board strategy_approval
    python scripts/simulate_stakeholder_cli.py ALPLA all
    python scripts/simulate_stakeholder_cli.py ALPLA customer --scenario price_increase_10pct
    python scripts/simulate_stakeholder_cli.py ALPLA all --updated

Version: 1.0.0
"""

import sys
import argparse
import json
import os
from pathlib import Path

# Add stakeholder_simulation module to path
sys.path.insert(0, str(Path(__file__).parent / "stakeholder_simulation"))

from stakeholder_simulator import (
    StakeholderSimulator,
    NineCAdjustments,
)
from scenarios import ScenarioManager
from output_formatters import OutputFormatter

# ============================================================================
# CONSTANTS
# ============================================================================

CUSTOMER_DATA_PATH = "data/customers"
STRATEGIC_MODELS_PATH = "data/models/registry/model_registry.yaml"
QUARTERLY_REVIEW_PATH = "data/quarterly_reviews"

# ============================================================================
# STAKEHOLDER-SPECIFIC 10C PROFILES (Defaults based on registry)
# ============================================================================

DEFAULT_ADJUSTMENTS = {
    "board": NineCAdjustments(
        WHERE_confidence=0.82,
        WHEN_context_risk=0.25,
        HOW_capability=0.85,
        WHAT_alignment=0.80,
        HIERARCHY_clarity=0.90,
        AWARE_briefing=0.95,
        READY_willingness=0.88,
    ),
    "c_suite": NineCAdjustments(
        WHERE_confidence=0.80,
        WHEN_context_risk=0.30,
        HOW_capability=0.85,
        WHAT_alignment=0.75,
        HIERARCHY_clarity=0.85,
        AWARE_briefing=0.90,
        READY_willingness=0.85,
    ),
    "regional_pl": NineCAdjustments(
        WHERE_confidence=0.75,
        WHEN_context_risk=0.35,
        HOW_capability=0.78,
        WHAT_alignment=0.80,
        HIERARCHY_clarity=0.70,
        AWARE_briefing=0.85,
        READY_willingness=0.80,
    ),
    "customer": NineCAdjustments(
        WHERE_confidence=0.70,
        WHEN_context_risk=0.40,
        HOW_capability=0.65,
        WHAT_alignment=0.75,
        HIERARCHY_clarity=0.60,
        AWARE_briefing=0.80,
        READY_willingness=0.60,
    ),
    "employee": NineCAdjustments(
        WHERE_confidence=0.65,
        WHEN_context_risk=0.45,
        HOW_capability=0.70,
        WHAT_alignment=0.70,
        HIERARCHY_clarity=0.60,
        AWARE_briefing=0.70,
        READY_willingness=0.55,
    ),
    "supplier": NineCAdjustments(
        WHERE_confidence=0.72,
        WHEN_context_risk=0.35,
        HOW_capability=0.75,
        WHAT_alignment=0.70,
        HIERARCHY_clarity=0.70,
        AWARE_briefing=0.85,
        READY_willingness=0.80,
    ),
    "competitor": NineCAdjustments(
        WHERE_confidence=0.60,
        WHEN_context_risk=0.50,
        HOW_capability=0.70,
        WHAT_alignment=0.65,
        HIERARCHY_clarity=0.75,
        AWARE_briefing=0.95,
        READY_willingness=0.85,
    ),
    "fpa": NineCAdjustments(
        WHERE_confidence=0.85,
        WHEN_context_risk=0.20,
        HOW_capability=0.80,
        WHAT_alignment=0.85,
        HIERARCHY_clarity=0.90,
        AWARE_briefing=0.95,
        READY_willingness=0.90,
    ),
    "hr": NineCAdjustments(
        WHERE_confidence=0.70,
        WHEN_context_risk=0.40,
        HOW_capability=0.75,
        WHAT_alignment=0.80,
        HIERARCHY_clarity=0.70,
        AWARE_briefing=0.80,
        READY_willingness=0.75,
    ),
    "capex_committee": NineCAdjustments(
        WHERE_confidence=0.80,
        WHEN_context_risk=0.30,
        HOW_capability=0.80,
        WHAT_alignment=0.75,
        HIERARCHY_clarity=0.92,
        AWARE_briefing=0.90,
        READY_willingness=0.85,
    ),
    "analytics": NineCAdjustments(
        WHERE_confidence=0.75,
        WHEN_context_risk=0.35,
        HOW_capability=0.85,
        WHAT_alignment=0.80,
        HIERARCHY_clarity=0.80,
        AWARE_briefing=0.90,
        READY_willingness=0.85,
    ),
    "data_science": NineCAdjustments(
        WHERE_confidence=0.70,
        WHEN_context_risk=0.40,
        HOW_capability=0.82,
        WHAT_alignment=0.75,
        HIERARCHY_clarity=0.65,
        AWARE_briefing=0.75,
        READY_willingness=0.72,
    ),
}

# ============================================================================
# MAIN CLI LOGIC
# ============================================================================

def load_customer_model(customer_name: str) -> dict:
    """Load strategic model for customer"""
    # Try to load from data/models/registry/model_registry.yaml
    model_path = Path(STRATEGIC_MODELS_PATH)
    if model_path.exists():
        try:
            import yaml
            with open(model_path, 'r') as f:
                registry = yaml.safe_load(f)
            # Find customer model
            for model in registry.get('models', []):
                if model.get('name', '').upper() == customer_name.upper():
                    return model
        except:
            pass

    # Return placeholder if not found
    return {
        "name": customer_name,
        "status": "mock",
        "message": f"Using default profile for {customer_name}",
    }

def load_quarterly_review(customer_name: str, quarter: str = "Q1") -> dict:
    """Load quarterly review data (ΔP attribution, E(θ) updates)"""
    review_path = Path(QUARTERLY_REVIEW_PATH) / f"{customer_name.lower()}" / f"{quarter}.yaml"
    if review_path.exists():
        try:
            import yaml
            with open(review_path, 'r') as f:
                return yaml.safe_load(f)
        except:
            pass

    return None

def adjust_9c_from_quarterly_review(adjustments: NineCAdjustments, review: dict) -> NineCAdjustments:
    """
    Update 10C adjustments based on quarterly review data

    If quarterly review shows parameter shrinkage, confidence improves:
    - E(θ) shrinks by 20% → WHERE confidence increases
    - If ΔP miss > ±5% → WHEN context risk increases
    """
    if not review:
        return adjustments

    # Apply quarterly updates
    if "parameter_shrinkage" in review:
        # Shrinkage improves confidence
        shrinkage_pct = review["parameter_shrinkage"]
        if shrinkage_pct > 0.15:  # Significant shrinkage
            adjustments.WHERE_confidence = min(1.0, adjustments.WHERE_confidence + 0.05)

    if "forecast_miss_pct" in review:
        # Large miss increases context risk
        miss = abs(review["forecast_miss_pct"])
        if miss > 0.05:
            adjustments.WHEN_context_risk = min(1.0, adjustments.WHEN_context_risk + 0.10)
        elif miss < 0.02:
            adjustments.WHEN_context_risk = max(0, adjustments.WHEN_context_risk - 0.05)

    return adjustments

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Simulate stakeholder decisions using 10C CORE framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single decision
  %(prog)s ALPLA board strategy_approval

  # Full matrix
  %(prog)s ALPLA all

  # What-if scenario
  %(prog)s ALPLA customer --scenario price_increase_10pct

  # With latest quarterly data
  %(prog)s ALPLA all --updated
        """
    )

    parser.add_argument("customer", help="Customer name (e.g., ALPLA)")
    parser.add_argument("stakeholder", nargs="?", default="all",
                        help="Stakeholder type (board|c_suite|regional_pl|customer|...|all)")
    parser.add_argument("--scenario", help="What-if scenario name")
    parser.add_argument("--updated", action="store_true", help="Use latest quarterly data")
    parser.add_argument("--detailed", action="store_true", help="Show detailed analysis")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--help-scenarios", action="store_true", help="List all scenarios")

    args = parser.parse_args()

    # Help: List scenarios
    if args.help_scenarios:
        print("\nAVAILABLE SCENARIOS:")
        print("=" * 70)
        for name, scenario in sorted(ScenarioManager.ALL_SCENARIOS.items()):
            print(f"\n{name}:")
            print(f"  {scenario.description}")
            print(f"  Category: {scenario.category.value}")
            if scenario.financial_impact:
                print(f"  Impact: {scenario.financial_impact}")
            if scenario.recommendation:
                print(f"  Recommendation: {scenario.recommendation}")
        return

    # Initialize simulator
    simulator = StakeholderSimulator()

    # Load customer model
    customer_model = load_customer_model(args.customer)

    # Get base adjustments
    if args.stakeholder == "all":
        # Simulate all stakeholders
        results = {}
        for stakeholder_type in ["board", "c_suite", "regional_pl", "fpa", "hr",
                                "capex_committee", "analytics", "data_science",
                                "customer", "supplier", "employee", "competitor"]:
            adjustments = DEFAULT_ADJUSTMENTS.get(stakeholder_type, DEFAULT_ADJUSTMENTS["board"])

            # Apply quarterly updates if requested
            if args.updated:
                quarterly = load_quarterly_review(args.customer)
                adjustments = adjust_9c_from_quarterly_review(adjustments, quarterly)

            # Apply scenario adjustments if provided
            scenario_adj = None
            if args.scenario:
                scenario = ScenarioManager.get_scenario(args.scenario)
                scenario_adj = scenario.adjustments

            result = simulator.simulate(stakeholder_type, adjustments, scenario_adj)
            results[stakeholder_type] = result

        # Output
        if args.json:
            output = {
                "customer": args.customer,
                "stakeholders": {
                    k: {
                        "probability": v.probability,
                        "confidence": v.confidence_level.value,
                        "risk_zone": v.risk_zone.value,
                    }
                    for k, v in results.items()
                }
            }
            print(json.dumps(output, indent=2))
        else:
            print(OutputFormatter.format_matrix(results))

    else:
        # Single stakeholder
        stakeholder_type = args.stakeholder.lower()

        if stakeholder_type not in DEFAULT_ADJUSTMENTS:
            print(f"Error: Unknown stakeholder type '{stakeholder_type}'")
            print(f"Available: {list(DEFAULT_ADJUSTMENTS.keys())}")
            sys.exit(1)

        adjustments = DEFAULT_ADJUSTMENTS[stakeholder_type]

        # Apply quarterly updates if requested
        if args.updated:
            quarterly = load_quarterly_review(args.customer)
            adjustments = adjust_9c_from_quarterly_review(adjustments, quarterly)

        # Apply scenario adjustments if provided
        scenario_adj = None
        if args.scenario:
            scenario = ScenarioManager.get_scenario(args.scenario)
            scenario_adj = scenario.adjustments

        result = simulator.simulate(stakeholder_type, adjustments, scenario_adj)

        # Output
        if args.json:
            print(OutputFormatter.format_json(result))
        elif args.detailed:
            print(OutputFormatter.format_detailed(result))
        else:
            print(OutputFormatter.format_summary(result))

            # If scenario, also show comparison
            if args.scenario:
                print("\n" + "=" * 70)
                baseline_result = simulator.simulate(stakeholder_type, adjustments)
                scenario_obj = ScenarioManager.get_scenario(args.scenario)
                print(OutputFormatter.format_scenario(
                    baseline_result, result,
                    args.scenario,
                    scenario_obj.description
                ))

if __name__ == "__main__":
    main()
