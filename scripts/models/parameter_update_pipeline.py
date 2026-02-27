#!/usr/bin/env python3
# =============================================================================
# PARAMETER UPDATE PIPELINE: E(θ) Shrinkage & Learning
# =============================================================================
#
# Purpose: Update parameter uncertainty E(θ) based on observed outcomes
#
# Key Formula (Bayesian Shrinkage):
#    E(θ)_new = E(θ)_old × (1 - n / (n + k))
#
#    Where:
#      n     = number of quarters observed
#      k     = prior strength (default 4)
#      E(θ)  = epistemic uncertainty (confidence interval)
#
# Interpretation:
#    - Year 0 (prediction): APAC_CAGR = 8.5% ± 1.5pp  [E(θ) = ±1.5pp]
#    - Q1 observed: 5.8% (below prediction)
#    - Year 1 (after 4q): APAC_CAGR = 8.5% ± 1.2pp  [E(θ) shrinks]
#    - Year 2 (after 8q): APAC_CAGR = 7.2% ± 0.9pp  [updated mean, tighter]
#    - Year 3 (after 12q): APAC_CAGR = 7.1% ± 0.7pp  [converging to true value]
#
# Single Source of Truth:
#   - /data/models/registry/model_registry.yaml (parameter_uncertainty fields)
#   - /data/intervention-registry.yaml (actual outcomes)
#
# Version: 1.0
# Date: 2026-01-16
# Status: DRAFT

import yaml
import json
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime
import statistics
from dataclasses import dataclass


@dataclass
class ParameterUpdate:
    """Represents a single parameter update."""
    model_id: str
    parameter_name: str
    old_value: float
    old_e_theta: float  # Old uncertainty (e.g., ±1.5pp)
    old_confidence: float  # Confidence = 1 - E(θ)
    new_value: float
    new_e_theta: float  # New uncertainty
    new_confidence: float
    quarters_observed: int
    observations: List[float]  # Historical actual values
    bayesian_shrinkage_factor: float  # (1 - n/(n+k))
    update_reason: str  # "convergence", "drift_detected", "regime_change"
    recommendation: str


class ParameterUpdatePipeline:
    """
    Bayesian parameter learning pipeline.

    Workflow:
    1. Load historical observations for each parameter
    2. Calculate sample mean (new parameter estimate)
    3. Calculate sample std (new E(θ))
    4. Apply Bayesian shrinkage (fade old prior)
    5. Save updated parameters
    6. Generate learning report
    """

    def __init__(self, company_name: str):
        self.company_name = company_name.lower()
        self.data_dir = Path(__file__).parent.parent.parent / "data"
        self.registry_file = self.data_dir / "models" / "registry" / "model_registry.yaml"
        self.customer_dir = self.data_dir / "customers" / self.company_name

    def load_parameter_metadata(self) -> Dict:
        """Load parameter metadata from model registry."""

        with open(self.registry_file) as f:
            registry = yaml.safe_load(f)

        return registry["registry"]["models"]

    def load_historical_observations(self, parameter_name: str) -> List[float]:
        """
        Load historical actual observations for a parameter.

        Example: Load APAC_CAGR observations from quarterly reviews.
        """

        observations_file = self.customer_dir / f"parameter_history_{parameter_name}.json"

        if not observations_file.exists():
            return []

        with open(observations_file) as f:
            data = json.load(f)
            return data.get("observations", [])

    def bayesian_shrinkage(
        self,
        prior_mean: float,
        prior_e_theta: float,
        observations: List[float],
        prior_strength: int = 4  # Default: 4-quarter prior
    ) -> Tuple[float, float, float]:
        """
        Apply Bayesian shrinkage to update parameters.

        Formula:
            λ = n / (n + k)                    # Shrinkage weight
            μ_new = λ × μ_obs + (1-λ) × μ_prior
            σ_new = σ_prior × (1 - λ)         # Uncertainty shrinks

        Args:
            prior_mean: Prior parameter value (from registry)
            prior_e_theta: Prior uncertainty (e.g., 1.5 for ±1.5pp)
            observations: List of observed values
            prior_strength: Prior strength (quarters equivalent)

        Returns:
            (new_mean, new_e_theta, shrinkage_factor)
        """

        if not observations:
            # No observations yet - return prior
            return prior_mean, prior_e_theta, 0.0

        n = len(observations)
        obs_mean = statistics.mean(observations)
        obs_std = statistics.stdev(observations) if n > 1 else prior_e_theta

        # Shrinkage weight (increases with more observations)
        shrinkage_weight = n / (n + prior_strength)
        shrinkage_factor = 1 - shrinkage_weight

        # Updated parameter (blend of prior and observed)
        new_mean = (shrinkage_weight * obs_mean) + (shrinkage_factor * prior_mean)

        # Updated uncertainty (shrinks with more observations)
        # E(θ)_new = min(obs_std, prior_E(θ)) × shrinkage_factor
        new_e_theta = min(obs_std, prior_e_theta) * (1 - 0.2 * shrinkage_weight)

        return new_mean, new_e_theta, shrinkage_factor

    def detect_regime_change(self, observations: List[float], prior_mean: float) -> bool:
        """
        Detect if observations show systematic drift from prior.

        Logic: If last N observations consistently above/below prior → regime change.
        """

        if len(observations) < 4:
            return False

        # Compare last 4 observations to prior
        recent = observations[-4:]
        recent_mean = statistics.mean(recent)
        recent_std = statistics.stdev(recent) if len(recent) > 1 else 0

        # Regime change if recent_mean drifts >2σ from prior
        z_score = abs(recent_mean - prior_mean) / max(recent_std, prior_mean * 0.1)
        return z_score > 2.0

    def update_model_parameters(self, model_id: str) -> List[ParameterUpdate]:
        """Update parameters for a specific model."""

        updates = []
        metadata = self.load_parameter_metadata()

        if model_id not in metadata:
            return updates

        model_meta = metadata[model_id]
        param_uncertainty = model_meta.get("parameter_uncertainty", {})

        # Process each parameter in the model
        for param_name, param_info in param_uncertainty.items():
            if not isinstance(param_info, dict):
                continue

            old_e_theta = self._parse_e_theta(param_info.get("epistemic_status_e_theta", "±0.0pp"))
            old_value = self._parse_value(param_info.get("value", param_info.get("value_range", "")))

            # Load observations
            observations = self.load_historical_observations(f"{model_id}_{param_name}")

            # Apply Bayesian shrinkage
            new_value, new_e_theta, shrinkage_factor = self.bayesian_shrinkage(
                prior_mean=old_value,
                prior_e_theta=old_e_theta,
                observations=observations
            )

            # Detect regime change
            regime_change = self.detect_regime_change(observations, old_value) if observations else False

            # Determine update reason
            if regime_change:
                update_reason = "regime_change"
                recommendation = f"INVESTIGATE: Parameter {param_name} has shifted significantly ({old_value:.2f} → {new_value:.2f}). Check for market/structural changes."
            elif abs(new_value - old_value) > old_e_theta:
                update_reason = "drift_detected"
                recommendation = f"UPDATE: Parameter {param_name} shows drift. Update prior from {old_value:.2f} to {new_value:.2f}."
            else:
                update_reason = "convergence"
                recommendation = f"MONITOR: Parameter {param_name} converging. E(θ) shrinking from ±{old_e_theta:.2f}pp to ±{new_e_theta:.2f}pp."

            # Create update record
            update = ParameterUpdate(
                model_id=model_id,
                parameter_name=param_name,
                old_value=old_value,
                old_e_theta=old_e_theta,
                old_confidence=1 - old_e_theta,
                new_value=new_value,
                new_e_theta=new_e_theta,
                new_confidence=1 - new_e_theta,
                quarters_observed=len(observations),
                observations=observations,
                bayesian_shrinkage_factor=shrinkage_factor,
                update_reason=update_reason,
                recommendation=recommendation
            )

            updates.append(update)

        return updates

    def _parse_e_theta(self, e_theta_str: str) -> float:
        """Parse E(θ) from string like '±1.5pp' or '±5%'."""

        if not e_theta_str:
            return 0.0

        # Remove ± and pp/%
        clean = e_theta_str.replace("±", "").replace("pp", "").replace("%", "").strip()

        try:
            return float(clean)
        except ValueError:
            return 0.0

    def _parse_value(self, value_str: str) -> float:
        """Parse parameter value from string."""

        if not value_str:
            return 0.0

        # Handle range like "2.5% - 8.5%"
        if "-" in value_str:
            parts = value_str.split("-")
            try:
                v1 = float(parts[0].replace("%", "").replace("€", "").strip())
                v2 = float(parts[1].replace("%", "").replace("€", "").strip())
                return (v1 + v2) / 2  # Return midpoint
            except ValueError:
                return 0.0
        else:
            # Single value
            clean = value_str.replace("%", "").replace("€", "").strip()
            try:
                return float(clean)
            except ValueError:
                return 0.0

    def save_updated_registry(self, updates: List[ParameterUpdate]) -> str:
        """Save updated parameters back to registry."""

        with open(self.registry_file) as f:
            registry = yaml.safe_load(f)

        # Update registry with new E(θ) values
        for update in updates:
            if update.model_id not in registry["registry"]["models"]:
                continue

            model = registry["registry"]["models"][update.model_id]
            param_uncertainty = model.get("parameter_uncertainty", {})

            if update.parameter_name in param_uncertainty:
                param_info = param_uncertainty[update.parameter_name]

                # Update epistemic status
                param_info["epistemic_status_e_theta"] = f"±{update.new_e_theta:.2f}pp"
                param_info["last_updated"] = datetime.now().isoformat()
                param_info["update_history"] = param_info.get("update_history", [])
                param_info["update_history"].append({
                    "date": datetime.now().isoformat(),
                    "old_e_theta": f"±{update.old_e_theta:.2f}pp",
                    "new_e_theta": f"±{update.new_e_theta:.2f}pp",
                    "quarters_observed": update.quarters_observed,
                    "reason": update.update_reason
                })

        # Write back to file
        with open(self.registry_file, "w") as f:
            yaml.dump(registry, f, default_flow_style=False, sort_keys=False)

        return str(self.registry_file)

    def generate_learning_report(self, updates: List[ParameterUpdate]) -> Dict:
        """Generate comprehensive learning report."""

        report = {
            "company": self.company_name,
            "timestamp": datetime.now().isoformat(),
            "parameter_updates": {
                "total_updated": len(updates),
                "regime_changes": sum(1 for u in updates if u.update_reason == "regime_change"),
                "drift_detected": sum(1 for u in updates if u.update_reason == "drift_detected"),
                "convergence": sum(1 for u in updates if u.update_reason == "convergence"),
            },
            "updates": [
                {
                    "model": u.model_id,
                    "parameter": u.parameter_name,
                    "old": f"{u.old_value:.2f} (E(θ)=±{u.old_e_theta:.2f})",
                    "new": f"{u.new_value:.2f} (E(θ)=±{u.new_e_theta:.2f})",
                    "quarters": u.quarters_observed,
                    "reason": u.update_reason,
                    "recommendation": u.recommendation,
                    "shrinkage_factor": f"{u.bayesian_shrinkage_factor:.1%}",
                    "confidence_improvement": f"{(1-u.old_confidence) - (1-u.new_confidence):.1%}"
                }
                for u in updates
            ],
            "next_steps": [
                "Validate updated parameters with domain experts",
                "Re-run model comparisons with new E(θ)",
                "Archive learning for archetype discovery",
                "Plan next quarterly review"
            ]
        }

        return report

    def run(self, models: List[str] = None) -> Dict:
        """
        Run parameter update pipeline for all models (or specified models).

        Args:
            models: List of model IDs to update (default: all)
        """

        if models is None:
            models = ["rpm_1_0", "osm_1_0", "cam_1_0", "mcsm_1_0"]

        print(f"\n{'='*70}")
        print(f"PARAMETER UPDATE PIPELINE: {self.company_name.upper()}")
        print(f"{'='*70}\n")

        all_updates = []

        for model_id in models:
            print(f"Processing {model_id}...")
            updates = self.update_model_parameters(model_id)
            all_updates.extend(updates)

            for update in updates:
                print(f"  ✓ {update.parameter_name}: {update.recommendation[:60]}...")

        # Save updated registry
        print(f"\nSaving updated registry...")
        registry_file = self.save_updated_registry(all_updates)

        # Generate learning report
        report = self.generate_learning_report(all_updates)

        # Save report
        report_file = self.customer_dir / f"parameter_learning_report_{datetime.now().strftime('%Y-%m-%d')}.json"
        report_file.parent.mkdir(parents=True, exist_ok=True)

        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)

        print(f"\n✅ Registry updated: {registry_file}")
        print(f"✅ Report saved: {report_file}\n")

        return {
            "updates": all_updates,
            "report": report,
            "registry_file": registry_file,
            "report_file": str(report_file)
        }


def example_usage():
    """Example: Update parameters for ALPLA after Q1-2025 quarterly review."""

    pipeline = ParameterUpdatePipeline(company_name="ALPLA")
    results = pipeline.run(models=["rpm_1_0", "osm_1_0", "cam_1_0"])

    return results


if __name__ == "__main__":
    print("""
    PARAMETER UPDATE PIPELINE v1.0

    This script implements Bayesian learning:
    E(θ)_new = E(θ)_old × (1 - n / (n + k))

    Workflow:
        1. Load quarterly review deviations (ΔP)
        2. Aggregate observations for each parameter
        3. Calculate Bayesian shrinkage
        4. Detect regime changes
        5. Update E(θ) in model registry
        6. Generate learning report
        7. Archive for archetype discovery

    Called by quarterly_review.py after measurements complete.
    """)
