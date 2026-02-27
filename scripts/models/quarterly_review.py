#!/usr/bin/env python3
# =============================================================================
# QUARTERLY REVIEW & PARAMETER UPDATE PIPELINE
# =============================================================================
#
# Purpose: Close the Prediction → Execution → Measurement → Learning loop
#
# Workflow:
#   1. Load prediction from previous quarter
#   2. Get actual outcomes from current quarter
#   3. Analyze deviations (ΔP = Actual - Predicted)
#   4. Decompose ΔP into sources (parameter error, context shock, model error)
#   5. Update E(θ) if |ΔP| > threshold
#   6. Generate quarterly report with insights
#   7. Archive results for archetype discovery
#
# Single Source of Truth:
#   - /docs/frameworks/strategic-models-9c-mapping.md (10C mappings)
#   - /data/models/registry/model_registry.yaml (parameter metadata + E(θ))
#   - /data/intervention-registry.yaml (project tracking)
#
# Version: 1.0
# Date: 2026-01-16
# Status: DRAFT (ready for implementation)

import yaml
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple
import statistics


class QuarterlyReview:
    """
    Closes the learning loop for strategic models.

    Key Insight: Every quarter, we observe:
      ΔP = Actual - Predicted

    This delta tells us THREE things:
      1. Parameter error (θ was wrong)
      2. Context shock (Ψ changed unexpectedly)
      3. Model error (functional form was wrong)

    We decompose ΔP to identify which, then update E(θ).
    """

    def __init__(self, company_name: str, quarter: str):
        """
        Args:
            company_name: e.g. "ALPLA"
            quarter: e.g. "Q1-2025" or "2025-Q1"
        """
        self.company_name = company_name
        self.quarter = quarter
        self.data_dir = Path(__file__).parent.parent.parent / "data"
        self.customer_dir = self.data_dir / "customers" / company_name.lower()
        self.results = {}

    def load_prediction(self) -> Dict:
        """Load the prediction made in the previous quarter."""
        prev_quarter_file = self.customer_dir / f"{self.company_name.lower()}_prediction_{self.quarter}.json"

        if not prev_quarter_file.exists():
            raise FileNotFoundError(f"No prediction found: {prev_quarter_file}")

        with open(prev_quarter_file) as f:
            return json.load(f)

    def load_actuals(self) -> Dict:
        """Load actual outcomes for this quarter."""
        actuals_file = self.customer_dir / f"{self.company_name.lower()}_actuals_{self.quarter}.yaml"

        if not actuals_file.exists():
            raise FileNotFoundError(f"No actuals found: {actuals_file}")

        with open(actuals_file) as f:
            return yaml.safe_load(f)

    def analyze_deviations(self, prediction: Dict, actuals: Dict) -> Dict:
        """
        Analyze deviations and decompose ΔP into sources.

        Formula:
            ΔP = Actual - Predicted

        Decomposition (Bayesian):
            ΔP = ΔP_parameter + ΔP_context + ΔP_model

        Attribution logic:
        - If CAGR changed in market data → ΔP_context (Ψ shock)
        - If model input parameters drifted → ΔP_parameter (θ wrong)
        - If residual remains → ΔP_model (functional form issue)
        """

        analysis = {
            "quarter": self.quarter,
            "timestamp": datetime.now().isoformat(),
            "models": {}
        }

        # Analyze each model separately
        for model_name in ["rpm", "osm", "cam"]:
            if model_name not in prediction or model_name not in actuals:
                continue

            pred = prediction[model_name]
            actual = actuals[model_name]

            # Revenue analysis (RPM)
            if model_name == "rpm":
                pred_revenue = pred.get("annual_revenue_eur_m", 0)
                actual_revenue = actual.get("annual_revenue_eur_m", 0)
                delta_p = actual_revenue - pred_revenue
                mape = abs(delta_p) / pred_revenue if pred_revenue > 0 else 0

                analysis["models"]["rpm"] = {
                    "predicted": pred_revenue,
                    "actual": actual_revenue,
                    "delta_p": delta_p,
                    "mape": f"{mape:.1%}",
                    "direction": "above" if delta_p > 0 else "below",

                    # Attribution analysis
                    "attribution": self._analyze_rpm_deviation(
                        pred, actual, delta_p
                    )
                }

            # Headcount analysis (OSM)
            elif model_name == "osm":
                pred_headcount = pred.get("headcount", 0)
                actual_headcount = actual.get("headcount", 0)
                delta_p = actual_headcount - pred_headcount
                mape = abs(delta_p) / pred_headcount if pred_headcount > 0 else 0

                analysis["models"]["osm"] = {
                    "predicted": pred_headcount,
                    "actual": actual_headcount,
                    "delta_p": delta_p,
                    "mape": f"{mape:.1%}",
                    "direction": "above" if delta_p > 0 else "below",

                    "attribution": self._analyze_osm_deviation(
                        pred, actual, delta_p
                    )
                }

            # Capex analysis (CAM)
            elif model_name == "cam":
                pred_capex = pred.get("annual_capex_eur_m", 0)
                actual_capex = actual.get("annual_capex_eur_m", 0)
                delta_p = actual_capex - pred_capex
                mape = abs(delta_p) / pred_capex if pred_capex > 0 else 0

                analysis["models"]["cam"] = {
                    "predicted": pred_capex,
                    "actual": actual_capex,
                    "delta_p": delta_p,
                    "mape": f"{mape:.1%}",
                    "direction": "above" if delta_p > 0 else "below",

                    "attribution": self._analyze_cam_deviation(
                        pred, actual, delta_p
                    )
                }

        return analysis

    def _analyze_rpm_deviation(self, pred: Dict, actual: Dict, delta_p: float) -> Dict:
        """
        Attribution for revenue deviation.

        Sources:
        - Ψ_economic shock: Market CAGR changed
        - θ_cagr wrong: Parameter estimate was off
        - θ_mix wrong: Segment mix shifted
        """

        pred_cagr = pred.get("cagr_actual", 0)
        actual_cagr = actual.get("cagr_observed", 0)
        cagr_drift = actual_cagr - pred_cagr

        attribution = {
            "primary_cause": "CONTEXT_SHOCK" if abs(cagr_drift) > 0.5 else "PARAMETER_ERROR",
            "cagr_drift_pp": f"{cagr_drift:.2f}pp",
            "cagr_attribution_impact": f"€{delta_p * (cagr_drift / max(pred_cagr, 0.01)):.0f}M",

            "segment_mix_drift": actual.get("segment_mix_actual") if "segment_mix_actual" in actual else "N/A",
            "regional_performance": {
                k: f"{v:.1%}" for k, v in actual.get("regional_cagr_observed", {}).items()
            }
        }

        return attribution

    def _analyze_osm_deviation(self, pred: Dict, actual: Dict, delta_p: float) -> Dict:
        """
        Attribution for headcount deviation.

        Sources:
        - θ_elasticity wrong: Headcount/revenue coupling was off
        - θ_cost wrong: Average cost per person changed
        - γ_rev-org misestimated: Revenue-headcount complementarity was wrong
        """

        pred_headcount = pred.get("headcount", 0)
        actual_headcount = actual.get("headcount", 0)
        pred_revenue = pred.get("revenue_reference", 0)
        actual_revenue = actual.get("revenue_reference", 0)

        # Calculate elasticity drift
        if pred_revenue > 0:
            pred_elasticity = pred_headcount / pred_revenue if pred_revenue > 0 else 0
        else:
            pred_elasticity = 0

        if actual_revenue > 0:
            actual_elasticity = actual_headcount / actual_revenue
        else:
            actual_elasticity = 0

        elasticity_drift = actual_elasticity - pred_elasticity

        attribution = {
            "primary_cause": "PARAMETER_ERROR",  # Headcount usually parameter-driven
            "elasticity_drift": f"{elasticity_drift:.3f}",
            "elasticity_attribution_impact": f"{delta_p:.0f} people",

            "avg_cost_per_person": {
                "predicted": f"€{pred.get('avg_cost', 0):.0f}K",
                "actual": f"€{actual.get('avg_cost', 0):.0f}K",
            },
            "functional_distribution": actual.get("function_distribution", {})
        }

        return attribution

    def _analyze_cam_deviation(self, pred: Dict, actual: Dict, delta_p: float) -> Dict:
        """
        Attribution for capex deviation.

        Sources:
        - θ_intensity wrong: Capex as % of revenue was off
        - γ_complementarity wrong: Initiative synergies were misestimated
        - Ψ_institutional changed: Governance constraints shifted
        """

        pred_capex = pred.get("annual_capex_eur_m", 0)
        actual_capex = actual.get("annual_capex_eur_m", 0)
        pred_revenue = pred.get("revenue_reference", 0)
        actual_revenue = actual.get("revenue_reference", 0)

        pred_intensity = (pred_capex / pred_revenue * 100) if pred_revenue > 0 else 0
        actual_intensity = (actual_capex / actual_revenue * 100) if actual_revenue > 0 else 0
        intensity_drift = actual_intensity - pred_intensity

        attribution = {
            "primary_cause": "GOVERNANCE_CONSTRAINT" if abs(delta_p) > 50 else "PARAMETER_ERROR",
            "capex_intensity_drift_pp": f"{intensity_drift:.2f}pp",
            "intensity_attribution_impact": f"€{delta_p:.0f}M",

            "initiative_breakdown": actual.get("initiative_allocation", {}),
            "delayed_initiatives": actual.get("delayed_or_cancelled", []),
            "accelerated_initiatives": actual.get("accelerated", [])
        }

        return attribution

    def calculate_parameter_updates(self, analysis: Dict) -> Dict:
        """
        Update E(θ) based on observed deviations.

        Bayesian shrinkage formula:
            E(θ)_new = f(E(θ)_old, ΔP_observed, n_quarters)

        As we observe more quarters, E(θ) shrinks (confidence increases).
        """

        updates = {}

        for model_name, model_analysis in analysis.get("models", {}).items():
            if "delta_p" not in model_analysis:
                continue

            delta_p = model_analysis["delta_p"]
            mape = float(model_analysis["mape"].rstrip("%")) / 100

            # Determine if update is needed
            # Threshold: update if |ΔP| > 5% of prediction
            if mape > 0.05:
                updates[model_name] = {
                    "observation": delta_p,
                    "mape": mape,
                    "action": "UPDATE_PARAMETERS" if mape > 0.10 else "MONITOR",
                    "recommended_e_theta_shrinkage": f"±{max(0, (0.015 - mape * 0.1)):.2%}",
                    "next_review": f"{self._get_next_quarter()}"
                }
            else:
                updates[model_name] = {
                    "observation": delta_p,
                    "mape": mape,
                    "action": "NO_UPDATE_NEEDED",
                    "rationale": "Prediction accuracy within acceptable range (±5%)"
                }

        return updates

    def _get_next_quarter(self) -> str:
        """Calculate next quarter for review."""
        # Parse quarter
        if "-" in self.quarter:
            parts = self.quarter.split("-")
            year = int(parts[1])
            q = int(parts[0][1])
        else:
            parts = self.quarter.split("-")
            year = int(parts[0])
            q = int(parts[1][1])

        # Increment quarter
        q += 1
        if q > 4:
            q = 1
            year += 1

        return f"Q{q}-{year}"

    def save_results(self, analysis: Dict, updates: Dict) -> str:
        """Save quarterly review results."""

        results = {
            "quarter": self.quarter,
            "company": self.company_name,
            "timestamp": datetime.now().isoformat(),
            "analysis": analysis,
            "parameter_updates": updates,

            # Metadata for archetype learning
            "metadata": {
                "total_delta_rpm": sum([
                    analysis["models"][m].get("delta_p", 0)
                    for m in analysis["models"] if m == "rpm"
                ]),
                "total_delta_osm": sum([
                    analysis["models"][m].get("delta_p", 0)
                    for m in analysis["models"] if m == "osm"
                ]),
                "needs_parameter_update": any(
                    u.get("action") == "UPDATE_PARAMETERS"
                    for u in updates.values()
                )
            }
        }

        # Save quarterly review
        output_file = self.customer_dir / f"quarterly_review_{self.quarter}.json"
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)

        return str(output_file)

    def run(self) -> Dict:
        """Run complete quarterly review."""

        print(f"\n{'='*70}")
        print(f"QUARTERLY REVIEW: {self.company_name} | {self.quarter}")
        print(f"{'='*70}\n")

        # Load data
        print("Loading prediction and actuals...")
        try:
            prediction = self.load_prediction()
            actuals = self.load_actuals()
        except FileNotFoundError as e:
            print(f"ERROR: {e}")
            return {}

        # Analyze deviations
        print("Analyzing deviations (ΔP = Actual - Predicted)...")
        analysis = self.analyze_deviations(prediction, actuals)

        # Calculate parameter updates
        print("Calculating parameter updates (E(θ) shrinkage)...")
        updates = self.calculate_parameter_updates(analysis)

        # Save results
        print("Saving quarterly review...")
        output_file = self.save_results(analysis, updates)

        # Print summary
        self._print_summary(analysis, updates)

        print(f"\n✅ Review saved to: {output_file}\n")

        return {"analysis": analysis, "updates": updates, "output_file": output_file}

    def _print_summary(self, analysis: Dict, updates: Dict):
        """Print human-readable summary."""

        print("\nDEVIATION ANALYSIS:")
        print("-" * 70)

        for model_name, model_data in analysis["models"].items():
            print(f"\n  {model_name.upper()}:")
            print(f"    Predicted: {model_data.get('predicted', 'N/A')}")
            print(f"    Actual:    {model_data.get('actual', 'N/A')}")
            print(f"    ΔP:        {model_data.get('delta_p', 'N/A')}")
            print(f"    MAPE:      {model_data.get('mape', 'N/A')}")
            print(f"    Direction: {model_data.get('direction', 'N/A')}")
            print(f"    Attribution: {model_data['attribution'].get('primary_cause', 'N/A')}")

        print("\n\nPARAMETER UPDATES:")
        print("-" * 70)

        for model_name, update_data in updates.items():
            print(f"\n  {model_name.upper()}: {update_data.get('action', 'N/A')}")
            if update_data.get('action') == "UPDATE_PARAMETERS":
                print(f"    New E(θ) range: {update_data.get('recommended_e_theta_shrinkage', 'N/A')}")
                print(f"    Next review: {update_data.get('next_review', 'N/A')}")
            else:
                print(f"    Rationale: {update_data.get('rationale', 'Continue monitoring')}")


def example_usage():
    """Example: Run quarterly review for ALPLA Q1-2025."""

    # Initialize review
    review = QuarterlyReview(company_name="ALPLA", quarter="Q1-2025")

    # Run review
    results = review.run()

    return results


if __name__ == "__main__":
    # This is a template - in practice, called by /intervention-manage close
    print("""
    QUARTERLY REVIEW TEMPLATE v1.0

    This script closes the Learning Loop:
    Prediction → Execution → Measurement → Parameter Update

    Usage in CLI:
        /intervention-manage close ALPLA_PROJECT \
            --actual-revenue 5.28 \
            --actual-headcount 27.5 \
            --actual-capex 14.2

    This will:
        1. Load prediction from previous quarter
        2. Compare with actuals
        3. Decompose deviations (ΔP) into sources
        4. Update E(θ) via Bayesian shrinkage
        5. Generate quarterly report
        6. Archive for archetype discovery
    """)
