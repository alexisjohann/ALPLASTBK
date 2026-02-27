#!/usr/bin/env python3
"""
ALPLA Churn Intervention Model (ACIM)
=====================================

Bayesian model for predicting and updating churn reduction effects
from HR interventions in ALPLA US plants.

EBF Version: 10C
Model Registry: FFF-ALPLA-CHURN-001

Usage:
    model = ALPLAChurnModel()
    prediction = model.predict("US-006", ["INT1", "INT2", "INT6"])
    model.update(field_data)
    posterior = model.predict_posterior("US-006", ["INT1", "INT2", "INT6"])
"""

import numpy as np
from scipy import stats
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
from pathlib import Path
import yaml
import json

# =============================================================================
# PRIOR SPECIFICATIONS
# =============================================================================

@dataclass
class Prior:
    """Single prior distribution specification."""
    distribution: str
    params: Dict
    mean: float
    sd: float
    source: str
    confidence: str  # high, medium, low

    def sample(self, n: int = 1) -> np.ndarray:
        """Draw samples from prior distribution."""
        if self.distribution == "Normal":
            return np.random.normal(self.params["mu"], self.params["sigma"], n)
        elif self.distribution == "Beta":
            return np.random.beta(self.params["a"], self.params["b"], n)
        elif self.distribution == "Gamma":
            return np.random.gamma(self.params["shape"], self.params["scale"], n)
        elif self.distribution == "InvGamma":
            return 1 / np.random.gamma(self.params["a"], 1/self.params["b"], n)
        else:
            raise ValueError(f"Unknown distribution: {self.distribution}")


class PriorSpecification:
    """
    Complete prior specification for ALPLA Churn Model.

    Sources:
    - Meta-analyses and literature (strong priors)
    - LLMMC estimates (moderate priors)
    - Domain experts (informative priors)
    """

    def __init__(self):
        self._init_intervention_effects()
        self._init_dimension_weights()
        self._init_interactions()
        self._init_context_modifiers()
        self._init_baseline()
        self._init_time_constants()

    def _init_intervention_effects(self):
        """Prior distributions for intervention effects (δ)."""
        self.delta = {
            "INT1": Prior(
                distribution="Normal",
                params={"mu": 6.5, "sigma": 2.0},
                mean=6.5, sd=2.0,
                source="Hackman & Oldham (1976); Job Design Meta-Analysis",
                confidence="medium"
            ),
            "INT2": Prior(
                distribution="Normal",
                params={"mu": 5.0, "sigma": 1.8},
                mean=5.0, sd=1.8,
                source="Internal Mobility Literature; Heckman Skill Formation",
                confidence="medium"
            ),
            "INT3": Prior(
                distribution="Normal",
                params={"mu": 4.0, "sigma": 1.5},
                mean=4.0, sd=1.5,
                source="Compensation & Turnover Studies",
                confidence="high"
            ),
            "INT4": Prior(
                distribution="Normal",
                params={"mu": 3.0, "sigma": 1.2},
                mean=3.0, sd=1.2,
                source="Work Stress Literature",
                confidence="medium"
            ),
            "INT5": Prior(
                distribution="Normal",
                params={"mu": 4.0, "sigma": 1.5},
                mean=4.0, sd=1.5,
                source="Self-Determination Theory; Autonomy Studies",
                confidence="medium"
            ),
            "INT6": Prior(
                distribution="Normal",
                params={"mu": 2.0, "sigma": 1.0},
                mean=2.0, sd=1.0,
                source="Ariely Recognition Studies; Engagement Literature",
                confidence="high"
            ),
            "INT7": Prior(
                distribution="Normal",
                params={"mu": 3.0, "sigma": 1.5},
                mean=3.0, sd=1.5,
                source="Onboarding Meta-Analysis",
                confidence="medium"
            ),
            "INT8": Prior(
                distribution="Normal",
                params={"mu": 3.0, "sigma": 1.5},
                mean=3.0, sd=1.5,
                source="Team Dynamics Literature",
                confidence="low"
            ),
        }

    def _init_dimension_weights(self):
        """Prior distributions for FEPSDE dimension weights (ω)."""
        self.omega = {
            "F": Prior("Beta", {"a": 5, "b": 15}, 0.25, 0.09, "Wage-Turnover Meta", "high"),
            "E": Prior("Beta", {"a": 3, "b": 17}, 0.15, 0.08, "Recognition Literature", "medium"),
            "P": Prior("Beta", {"a": 2, "b": 18}, 0.10, 0.07, "Ergonomics Studies", "medium"),
            "S": Prior("Beta", {"a": 3, "b": 17}, 0.15, 0.08, "Team Cohesion Lit", "medium"),
            "D": Prior("Beta", {"a": 5, "b": 15}, 0.25, 0.09, "Career Development Meta", "high"),
            "X": Prior("Beta", {"a": 2, "b": 18}, 0.10, 0.07, "Job Security Studies", "low"),
        }

    def _init_interactions(self):
        """Prior distributions for intervention interactions (γ)."""
        self.gamma = {
            ("INT1", "INT2"): Prior("Normal", {"mu": 0.35, "sigma": 0.15}, 0.35, 0.15, "Theory", "medium"),
            ("INT2", "INT3"): Prior("Normal", {"mu": 0.40, "sigma": 0.15}, 0.40, 0.15, "Theory", "medium"),
            ("INT5", "INT6"): Prior("Normal", {"mu": 0.25, "sigma": 0.12}, 0.25, 0.12, "Theory", "medium"),
            ("INT1", "INT7"): Prior("Normal", {"mu": 0.20, "sigma": 0.10}, 0.20, 0.10, "Theory", "low"),
            ("INT3", "INT8"): Prior("Normal", {"mu": -0.45, "sigma": 0.15}, -0.45, 0.15, "Theory", "medium"),
            ("INT5", "INT8"): Prior("Normal", {"mu": -0.30, "sigma": 0.12}, -0.30, 0.12, "Theory", "low"),
        }

    def _init_context_modifiers(self):
        """Prior distributions for context modifiers (κ)."""
        self.kappa = {
            "unemployment": Prior("Normal", {"mu": 0.15, "sigma": 0.08}, 0.15, 0.08, "LLMMC", "medium"),
            "wage_competition": Prior("Normal", {"mu": 0.20, "sigma": 0.10}, 0.20, 0.10, "LLMMC", "medium"),
            "plant_size": Prior("Normal", {"mu": 0.10, "sigma": 0.05}, 0.10, 0.05, "LLMMC", "medium"),
            "tenure": Prior("Normal", {"mu": 0.18, "sigma": 0.08}, 0.18, 0.08, "LLMMC", "medium"),
            "buyin": Prior("Normal", {"mu": 0.25, "sigma": 0.10}, 0.25, 0.10, "LLMMC", "high"),
        }

    def _init_baseline(self):
        """Prior distributions for baseline parameters."""
        self.baseline = {
            "churn_intercept": Prior("Normal", {"mu": 22, "sigma": 5}, 22, 5, "ALPLA data", "high"),
            "theta": Prior("Normal", {"mu": 0.5, "sigma": 0.15}, 0.5, 0.15, "Theory", "medium"),
            "beta": Prior("Gamma", {"shape": 3, "scale": 1}, 3, 1.7, "Theory", "low"),
            "sigma_obs": Prior("InvGamma", {"a": 3, "b": 2}, 1.0, 0.5, "Measurement", "medium"),
        }

    def _init_time_constants(self):
        """Prior distributions for time constants (τ in weeks)."""
        self.tau = {
            "INT1": Prior("Gamma", {"shape": 8, "scale": 1}, 8, 2.8, "Theory", "medium"),
            "INT2": Prior("Gamma", {"shape": 16, "scale": 1}, 16, 4.0, "Theory", "medium"),
            "INT3": Prior("Gamma", {"shape": 24, "scale": 1}, 24, 4.9, "Theory", "medium"),
            "INT4": Prior("Gamma", {"shape": 10, "scale": 1}, 10, 3.2, "Theory", "medium"),
            "INT5": Prior("Gamma", {"shape": 12, "scale": 1}, 12, 3.5, "Theory", "medium"),
            "INT6": Prior("Gamma", {"shape": 4, "scale": 1}, 4, 2.0, "Theory", "high"),
            "INT7": Prior("Gamma", {"shape": 6, "scale": 1}, 6, 2.4, "Theory", "medium"),
            "INT8": Prior("Gamma", {"shape": 12, "scale": 1}, 12, 3.5, "Theory", "low"),
        }


# =============================================================================
# PREDICTION RESULTS
# =============================================================================

@dataclass
class PredictionResult:
    """Container for model predictions with uncertainty."""
    plant_id: str
    interventions: List[str]

    # Point estimates
    mean: float
    median: float

    # Uncertainty
    sd: float
    ci_50: Tuple[float, float]
    ci_80: Tuple[float, float]
    ci_95: Tuple[float, float]

    # Full distribution
    samples: np.ndarray = field(repr=False)

    # Components
    direct_effect: float = 0.0
    synergy_effect: float = 0.0
    fit_modifier: float = 1.0
    awareness_modifier: float = 0.8

    def __repr__(self):
        return (
            f"PredictionResult(plant={self.plant_id}, "
            f"mean={self.mean:.1f}pp, "
            f"95%CI=[{self.ci_95[0]:.1f}, {self.ci_95[1]:.1f}])"
        )

    def summary(self) -> str:
        """Generate human-readable summary."""
        return f"""
╔══════════════════════════════════════════════════════════════╗
║  CHURN REDUCTION PREDICTION                                   ║
╠══════════════════════════════════════════════════════════════╣
║  Plant: {self.plant_id:<52} ║
║  Interventions: {', '.join(self.interventions):<44} ║
╠══════════════════════════════════════════════════════════════╣
║  Expected Reduction: {self.mean:>6.1f} pp  (SD: {self.sd:.1f})              ║
║  Median:             {self.median:>6.1f} pp                              ║
╠══════════════════════════════════════════════════════════════╣
║  Credible Intervals:                                          ║
║    50% CI: [{self.ci_50[0]:>5.1f}, {self.ci_50[1]:>5.1f}] pp                           ║
║    80% CI: [{self.ci_80[0]:>5.1f}, {self.ci_80[1]:>5.1f}] pp                           ║
║    95% CI: [{self.ci_95[0]:>5.1f}, {self.ci_95[1]:>5.1f}] pp                           ║
╠══════════════════════════════════════════════════════════════╣
║  Effect Decomposition:                                        ║
║    Direct Effect:   {self.direct_effect:>6.1f} pp                            ║
║    Synergy Effect:  {self.synergy_effect:>6.1f} pp                            ║
║    Fit Modifier:    {self.fit_modifier:>6.2f}x                              ║
║    Awareness:       {self.awareness_modifier:>6.2f}x                              ║
╚══════════════════════════════════════════════════════════════╝
"""


# =============================================================================
# MAIN MODEL CLASS
# =============================================================================

class ALPLAChurnModel:
    """
    Bayesian Churn Intervention Model for ALPLA.

    This model:
    1. Predicts churn reduction from interventions (a priori)
    2. Updates predictions with field experiment data (posterior)
    3. Enables scenario testing and sensitivity analysis

    Based on EBF 10C Framework equations:
    - Stage 1: U^pot = Σ ω_d · U_d + Σ γ · U_d · U_d'
    - Stage 2: U^eff = A · U^pot
    - Stage 3: P(Stay) = σ(β · (U^eff - θ))
    - Stage 4: ΔChurn = Σ δ_j · I_j · Fit · A · (1 + Σ γ_jj' · I_j')
    """

    def __init__(self, config_path: Optional[str] = None):
        """Initialize model with priors."""
        self.priors = PriorSpecification()
        self.posteriors = None  # Will be set after update()
        self._load_plant_data()
        self._load_ifi_data()

    def _load_plant_data(self):
        """Load plant context data."""
        self.plant_data = {}
        data_dir = Path(__file__).parent.parent / "data"

        # Try to load PCI estimates
        pci_file = data_dir / "alpla-pci-estimates.csv"
        if pci_file.exists():
            import csv
            with open(pci_file, "r") as f:
                lines = [l for l in f if l.strip() and not l.startswith('#')]
                reader = csv.DictReader(lines)
                for row in reader:
                    self.plant_data[row['plant_id']] = {
                        'name': row['plant_name'],
                        'type': row['plant_type'],
                        'employees': int(row['S2_employees']),
                        'churn_baseline': float(row['P1_total']),
                    }

    def _load_ifi_data(self):
        """Load Intervention Fit Index data."""
        self.ifi_data = {}
        data_dir = Path(__file__).parent.parent / "data"

        ifi_file = data_dir / "alpla-intervention-fit-index.yaml"
        if ifi_file.exists():
            with open(ifi_file, "r") as f:
                data = yaml.safe_load(f)
                if data and 'plant_ifi_scores' in data:
                    for plant in data['plant_ifi_scores']:
                        plant_id = plant['plant_id']
                        self.ifi_data[plant_id] = {
                            'I1': plant.get('I1_rotation_fit', 50) / 100,
                            'I2': plant.get('I2_career_fit', 50) / 100,
                            'I3': plant.get('I3_skill_pay_fit', 50) / 100,
                            'I4': plant.get('I4_workload_fit', 50) / 100,
                            'I5': plant.get('I5_autonomy_fit', 50) / 100,
                            'cluster': plant.get('assigned_cluster', 'E'),
                        }

    def get_fit_modifier(self, plant_id: str, intervention: str) -> float:
        """
        Get intervention fit modifier for a plant.

        Fit modifier ranges from 0.5 (poor fit) to 1.5 (excellent fit).
        Based on IFI scores from alpla-intervention-fit-index.yaml.
        """
        if plant_id not in self.ifi_data:
            return 1.0  # Default: neutral fit

        ifi = self.ifi_data[plant_id]

        # Map intervention to IFI dimension
        ifi_map = {
            "INT1": "I1",  # Rotation
            "INT2": "I2",  # Career
            "INT3": "I3",  # Skill Pay
            "INT4": "I4",  # Workload
            "INT5": "I5",  # Autonomy
            "INT6": None,  # Recognition - universal, no fit needed
            "INT7": None,  # Onboarding - universal
            "INT8": None,  # Team - depends on cohesion score
        }

        ifi_key = ifi_map.get(intervention)
        if ifi_key and ifi_key in ifi:
            # Convert IFI score (0-1) to fit modifier (0.5-1.5)
            return 0.5 + ifi[ifi_key]

        return 1.0  # Default for universal interventions

    def get_synergy_multiplier(self, interventions: List[str]) -> float:
        """
        Calculate synergy multiplier for intervention combination.

        Returns multiplicative factor based on γ interactions.
        """
        if len(interventions) <= 1:
            return 1.0

        synergy = 0.0
        for i, int1 in enumerate(interventions):
            for int2 in interventions[i+1:]:
                # Check both orderings
                key = (int1, int2)
                if key in self.priors.gamma:
                    synergy += self.priors.gamma[key].mean
                key_rev = (int2, int1)
                if key_rev in self.priors.gamma:
                    synergy += self.priors.gamma[key_rev].mean

        return 1.0 + synergy

    def predict(
        self,
        plant_id: str,
        interventions: List[str],
        awareness: float = 0.80,
        n_simulations: int = 10000,
        use_posterior: bool = False
    ) -> PredictionResult:
        """
        Predict churn reduction for a plant with given interventions.

        Args:
            plant_id: Plant identifier (e.g., "US-006")
            interventions: List of intervention codes (e.g., ["INT1", "INT2", "INT6"])
            awareness: Implementation quality factor (0.3 to 1.0)
            n_simulations: Number of Monte Carlo samples
            use_posterior: Use posterior if available, else prior

        Returns:
            PredictionResult with point estimates and uncertainty
        """
        # Get parameter source (posterior if available and requested)
        params = self.posteriors if (use_posterior and self.posteriors) else self.priors

        # Monte Carlo simulation
        samples = np.zeros(n_simulations)

        for i in range(n_simulations):
            # Sample intervention effects
            total_effect = 0.0
            for intervention in interventions:
                if intervention in params.delta:
                    delta = params.delta[intervention].sample(1)[0]
                    fit = self.get_fit_modifier(plant_id, intervention)
                    total_effect += delta * fit

            # Apply synergy
            synergy = self._sample_synergy(interventions, params)
            total_effect *= synergy

            # Apply awareness
            total_effect *= awareness

            # Apply diminishing returns (soft cap at ~15pp)
            total_effect = 20 * (1 - np.exp(-total_effect / 20))

            samples[i] = total_effect

        # Calculate statistics
        mean = np.mean(samples)
        median = np.median(samples)
        sd = np.std(samples)

        ci_50 = (np.percentile(samples, 25), np.percentile(samples, 75))
        ci_80 = (np.percentile(samples, 10), np.percentile(samples, 90))
        ci_95 = (np.percentile(samples, 2.5), np.percentile(samples, 97.5))

        # Calculate component breakdown (using means)
        direct = sum(params.delta[i].mean * self.get_fit_modifier(plant_id, i)
                     for i in interventions if i in params.delta)
        synergy_mult = self.get_synergy_multiplier(interventions)

        return PredictionResult(
            plant_id=plant_id,
            interventions=interventions,
            mean=mean,
            median=median,
            sd=sd,
            ci_50=ci_50,
            ci_80=ci_80,
            ci_95=ci_95,
            samples=samples,
            direct_effect=direct,
            synergy_effect=direct * (synergy_mult - 1),
            fit_modifier=np.mean([self.get_fit_modifier(plant_id, i) for i in interventions]),
            awareness_modifier=awareness
        )

    def _sample_synergy(self, interventions: List[str], params) -> float:
        """Sample synergy multiplier from prior/posterior."""
        if len(interventions) <= 1:
            return 1.0

        synergy = 0.0
        for i, int1 in enumerate(interventions):
            for int2 in interventions[i+1:]:
                key = (int1, int2)
                if key in params.gamma:
                    synergy += params.gamma[key].sample(1)[0]
                key_rev = (int2, int1)
                if key_rev in params.gamma:
                    synergy += params.gamma[key_rev].sample(1)[0]

        return max(0.5, 1.0 + synergy)  # Floor at 0.5x

    def predict_all_plants(
        self,
        interventions: Dict[str, List[str]],
        awareness: float = 0.80
    ) -> Dict[str, PredictionResult]:
        """
        Predict churn reduction for all plants.

        Args:
            interventions: Dict mapping plant_id to intervention list
            awareness: Implementation quality factor

        Returns:
            Dict of PredictionResults keyed by plant_id
        """
        results = {}
        for plant_id, ints in interventions.items():
            results[plant_id] = self.predict(plant_id, ints, awareness)
        return results

    def update(self, field_data: Dict) -> None:
        """
        Update model with field experiment data using Bayesian updating.

        Args:
            field_data: Dictionary with observed results
                {
                    "plant_id": {
                        "interventions": ["INT1", ...],
                        "churn_baseline": 28.0,
                        "churn_observed": 18.0,
                        "duration_weeks": 52,
                        "implementation_quality": 0.85
                    },
                    ...
                }
        """
        # Initialize posteriors as copy of priors
        self.posteriors = PriorSpecification()

        # Extract observations
        observations = []
        for plant_id, data in field_data.items():
            observed_reduction = data["churn_baseline"] - data["churn_observed"]
            interventions = data["interventions"]
            quality = data.get("implementation_quality", 0.8)

            observations.append({
                "plant_id": plant_id,
                "reduction": observed_reduction,
                "interventions": interventions,
                "quality": quality
            })

        # Simple conjugate normal update for each intervention
        # (In practice, use full MCMC for joint estimation)
        for intervention in ["INT1", "INT2", "INT3", "INT4", "INT5", "INT6", "INT7", "INT8"]:
            relevant_obs = [
                obs for obs in observations
                if intervention in obs["interventions"]
            ]

            if not relevant_obs:
                continue

            # Get prior parameters
            prior_mu = self.priors.delta[intervention].mean
            prior_sigma = self.priors.delta[intervention].sd

            # Simple normal conjugate update
            # (Assumes each observation contributes equally)
            n = len(relevant_obs)
            obs_sigma = 3.0  # Assumed observation error

            # Posterior precision
            post_precision = 1/prior_sigma**2 + n/obs_sigma**2
            post_sigma = np.sqrt(1/post_precision)

            # Estimate effect for this intervention from observations
            # (Simplified: assumes single intervention or equal attribution)
            estimated_effects = []
            for obs in relevant_obs:
                n_ints = len(obs["interventions"])
                # Attribute equal share of reduction to each intervention
                estimated_effects.append(obs["reduction"] / n_ints / obs["quality"])

            obs_mean = np.mean(estimated_effects) if estimated_effects else prior_mu

            # Posterior mean
            post_mu = post_sigma**2 * (prior_mu/prior_sigma**2 + n*obs_mean/obs_sigma**2)

            # Update posterior
            self.posteriors.delta[intervention] = Prior(
                distribution="Normal",
                params={"mu": post_mu, "sigma": post_sigma},
                mean=post_mu,
                sd=post_sigma,
                source=f"Posterior (n={n} plants)",
                confidence="high" if n >= 3 else "medium"
            )

        print(f"Model updated with data from {len(field_data)} plants")

    def scenario_analysis(
        self,
        plant_id: str,
        interventions: List[str],
        scenarios: Optional[Dict] = None
    ) -> Dict[str, PredictionResult]:
        """
        Run scenario analysis with different assumptions.

        Args:
            plant_id: Plant identifier
            interventions: List of interventions
            scenarios: Optional custom scenarios, else use defaults

        Returns:
            Dict of PredictionResults for each scenario
        """
        if scenarios is None:
            scenarios = {
                "optimistic": {"awareness": 0.95, "fit_boost": 1.2},
                "base": {"awareness": 0.80, "fit_boost": 1.0},
                "conservative": {"awareness": 0.60, "fit_boost": 0.8},
            }

        results = {}
        for name, params in scenarios.items():
            # Temporarily adjust fit modifiers
            original_ifi = self.ifi_data.get(plant_id, {}).copy()
            if plant_id in self.ifi_data:
                for key in self.ifi_data[plant_id]:
                    if key != 'cluster':
                        self.ifi_data[plant_id][key] *= params.get("fit_boost", 1.0)

            results[name] = self.predict(
                plant_id,
                interventions,
                awareness=params["awareness"]
            )

            # Restore original
            if plant_id in self.ifi_data:
                self.ifi_data[plant_id] = original_ifi

        return results

    def sensitivity_analysis(
        self,
        plant_id: str,
        interventions: List[str],
        parameter: str,
        range_pct: float = 20.0
    ) -> Dict:
        """
        One-at-a-time sensitivity analysis for a parameter.

        Args:
            plant_id: Plant identifier
            interventions: List of interventions
            parameter: Parameter name (e.g., "delta_INT1", "awareness")
            range_pct: Percent variation from baseline

        Returns:
            Dict with low, base, high predictions and elasticity
        """
        base = self.predict(plant_id, interventions)

        # This is a simplified version - full implementation would
        # modify the prior and re-run
        results = {
            "base": base.mean,
            "parameter": parameter,
            "range_pct": range_pct,
        }

        # Estimate elasticity (simplified)
        if parameter == "awareness":
            low = self.predict(plant_id, interventions, awareness=0.64)  # -20%
            high = self.predict(plant_id, interventions, awareness=0.96)  # +20%
            results["low"] = low.mean
            results["high"] = high.mean
            results["elasticity"] = (high.mean - low.mean) / (0.4 * base.mean) if base.mean > 0 else 0

        return results

    def get_optimal_bundle(
        self,
        plant_id: str,
        max_interventions: int = 3,
        budget_constraint: Optional[str] = None
    ) -> Tuple[List[str], PredictionResult]:
        """
        Find optimal intervention bundle for a plant.

        Args:
            plant_id: Plant identifier
            max_interventions: Maximum number of interventions
            budget_constraint: "low", "medium", "high", or None

        Returns:
            Tuple of (optimal interventions, prediction)
        """
        from itertools import combinations

        # Define intervention costs
        costs = {
            "INT1": "low", "INT2": "medium", "INT3": "high", "INT4": "medium",
            "INT5": "low", "INT6": "low", "INT7": "low", "INT8": "medium"
        }

        cost_order = {"low": 1, "medium": 2, "high": 3}
        budget_limit = cost_order.get(budget_constraint, 10) if budget_constraint else 10

        all_interventions = list(self.priors.delta.keys())
        best_bundle = None
        best_prediction = None
        best_mean = -np.inf

        # Try all combinations up to max_interventions
        for n in range(1, max_interventions + 1):
            for combo in combinations(all_interventions, n):
                combo_list = list(combo)

                # Check budget constraint
                total_cost = sum(cost_order.get(costs.get(i, "medium"), 2) for i in combo_list)
                if total_cost > budget_limit * n:
                    continue

                # Predict
                pred = self.predict(plant_id, combo_list, n_simulations=1000)

                if pred.mean > best_mean:
                    best_mean = pred.mean
                    best_bundle = combo_list
                    best_prediction = pred

        return best_bundle, best_prediction

    def generate_preregistration(self) -> str:
        """
        Generate pre-registration document with a priori predictions.

        Returns:
            Markdown-formatted pre-registration text
        """
        text = """
# ALPLA Churn Intervention Study - Pre-Registration

## Model Specification
- Model: ALPLA Churn Intervention Model (ACIM) v1.0
- Framework: EBF 10C
- Registry: FFF-ALPLA-CHURN-001

## Prior Distributions

### Intervention Effects (δ)
"""
        for int_name, prior in self.priors.delta.items():
            text += f"- {int_name}: N({prior.mean:.1f}, {prior.sd:.1f}²) pp reduction\n"

        text += """
### Key Interactions (γ)
"""
        for (i1, i2), prior in self.priors.gamma.items():
            sign = "+" if prior.mean > 0 else ""
            text += f"- {i1} × {i2}: {sign}{prior.mean:.2f}\n"

        text += """
## A Priori Predictions

| Plant | Bundle | Expected ΔChurn | 95% CI |
|-------|--------|-----------------|--------|
"""
        # Add predictions for key plants
        bundles = {
            "US-006": ["INT1", "INT2", "INT6"],
            "US-001": ["INT5", "INT2", "INT6"],
            "US-015": ["INT2", "INT3", "INT6"],
        }

        for plant_id, ints in bundles.items():
            pred = self.predict(plant_id, ints, n_simulations=5000)
            text += f"| {plant_id} | {'+'.join(ints)} | {pred.mean:.1f}pp | [{pred.ci_95[0]:.1f}, {pred.ci_95[1]:.1f}] |\n"

        text += """
## Analysis Plan
1. Primary outcome: Difference-in-Differences of churn rates
2. Bayesian model update with observed data
3. Posterior predictive checks for model validation

---
*Generated by ALPLA Churn Model v1.0*
"""
        return text


# =============================================================================
# SIMULATION FUNCTIONS
# =============================================================================

def simulate_experiment(
    model: ALPLAChurnModel,
    treatment_plants: Dict[str, List[str]],
    control_plants: List[str],
    true_effects: Optional[Dict[str, float]] = None,
    duration_weeks: int = 52
) -> Dict:
    """
    Simulate a field experiment to test model validity.

    Args:
        model: ALPLAChurnModel instance
        treatment_plants: Dict mapping plant_id to interventions
        control_plants: List of control plant_ids
        true_effects: Optional dict of "true" intervention effects (for simulation)
        duration_weeks: Experiment duration

    Returns:
        Simulated experiment results
    """
    np.random.seed(42)  # For reproducibility

    # Default "true" effects (ground truth for simulation)
    if true_effects is None:
        true_effects = {
            "INT1": 7.0, "INT2": 5.5, "INT3": 4.5, "INT4": 3.5,
            "INT5": 4.5, "INT6": 2.5, "INT7": 3.5, "INT8": 3.0
        }

    results = {"treatment": {}, "control": {}}

    # Simulate treatment plants
    for plant_id, interventions in treatment_plants.items():
        baseline = model.plant_data.get(plant_id, {}).get("churn_baseline", 25.0)

        # Calculate "true" reduction
        true_reduction = sum(true_effects.get(i, 3.0) for i in interventions)
        # Add synergy
        true_reduction *= model.get_synergy_multiplier(interventions)
        # Add fit modifier
        fit = np.mean([model.get_fit_modifier(plant_id, i) for i in interventions])
        true_reduction *= fit
        # Add implementation quality (random)
        quality = np.random.uniform(0.7, 0.95)
        true_reduction *= quality
        # Add noise
        noise = np.random.normal(0, 2)
        observed = max(5, baseline - true_reduction + noise)

        results["treatment"][plant_id] = {
            "interventions": interventions,
            "churn_baseline": baseline,
            "churn_observed": observed,
            "true_reduction": baseline - observed,
            "implementation_quality": quality,
            "duration_weeks": duration_weeks
        }

    # Simulate control plants
    for plant_id in control_plants:
        baseline = model.plant_data.get(plant_id, {}).get("churn_baseline", 25.0)
        # Control only gets INT6 (recognition)
        true_reduction = true_effects.get("INT6", 2.0) * 0.8
        noise = np.random.normal(0, 2)
        observed = max(5, baseline - true_reduction + noise)

        results["control"][plant_id] = {
            "interventions": ["INT6"],
            "churn_baseline": baseline,
            "churn_observed": observed,
            "true_reduction": baseline - observed,
            "implementation_quality": 0.8,
            "duration_weeks": duration_weeks
        }

    # Calculate DiD estimate
    treatment_effect = np.mean([r["true_reduction"] for r in results["treatment"].values()])
    control_effect = np.mean([r["true_reduction"] for r in results["control"].values()])
    results["did_estimate"] = treatment_effect - control_effect

    return results


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    # Demo usage
    print("=" * 60)
    print("ALPLA Churn Intervention Model - Demo")
    print("=" * 60)

    # Initialize model
    model = ALPLAChurnModel()

    # Example prediction
    plant = "US-006"
    bundle = ["INT1", "INT2", "INT6"]

    print(f"\nPredicting churn reduction for {plant} with {bundle}...")
    prediction = model.predict(plant, bundle)
    print(prediction.summary())

    # Scenario analysis
    print("\nScenario Analysis:")
    scenarios = model.scenario_analysis(plant, bundle)
    for name, pred in scenarios.items():
        print(f"  {name:>12}: {pred.mean:.1f}pp [{pred.ci_95[0]:.1f}, {pred.ci_95[1]:.1f}]")

    # Optimal bundle
    print(f"\nFinding optimal bundle for {plant}...")
    optimal, opt_pred = model.get_optimal_bundle(plant, max_interventions=3)
    print(f"  Optimal: {optimal}")
    print(f"  Expected: {opt_pred.mean:.1f}pp reduction")

    print("\n" + "=" * 60)
    print("Model ready for field experiment!")
    print("=" * 60)
