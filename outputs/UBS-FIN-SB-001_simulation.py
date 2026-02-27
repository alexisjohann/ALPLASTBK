#!/usr/bin/env python3
"""
UBS Customer Savings Behavior Model Simulator
Model ID: UBS-FIN-SB-001
Purpose: Simulate monthly customer savings based on 9C EBF framework
"""

import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import Dict, Tuple
import matplotlib.pyplot as plt

# ============================================================================
# MODEL PARAMETERS (from GGG Configurator + BBB Parameter Repository)
# ============================================================================

@dataclass
class ModelParameters:
    """Parameters for UBS savings behavior model"""

    # Baseline
    beta_0: float = 850.0  # CHF baseline

    # Utility dimension weights
    beta_F: float = 0.25  # Financial
    beta_E: float = 0.15  # Emotional
    beta_P: float = 0.18  # Practical
    beta_S: float = 0.08  # Social
    beta_D: float = 0.12  # Deliberative

    # Context effects
    gamma_tau: float = 180.0      # Trust effect (CHF)
    gamma_delta: float = 120.0    # Digital adoption effect
    gamma_rho: float = -50.0      # Risk aversion drag
    gamma_sigma: float = 95.0     # Income stability boost

    # Habit formation
    lambda_habit: float = 0.62    # Stickiness factor

    # Error term
    sigma_noise: float = 80.0     # Standard deviation of random shock


@dataclass
class ContextFactors:
    """Context variables (Ψ) for a customer"""
    tau: float        # Trust (0-1)
    delta: float      # Digital adoption (0-1)
    rho: float        # Risk aversion (0-1)
    sigma: float      # Income stability (0-1)

    def as_dict(self) -> Dict:
        return {
            'trust': self.tau,
            'digital': self.delta,
            'risk_aversion': self.rho,
            'income_stability': self.sigma
        }


@dataclass
class UtilityDimensions:
    """Utility components (C) for a customer"""
    F: float  # Financial (0-1)
    E: float  # Emotional (0-1)
    P: float  # Practical (0-1)
    S: float  # Social (0-1)
    D: float  # Deliberative (0-1)

    def weighted_sum(self, params: ModelParameters) -> float:
        """Calculate weighted sum of utilities"""
        return (params.beta_F * self.F +
                params.beta_E * self.E +
                params.beta_P * self.P +
                params.beta_S * self.S +
                params.beta_D * self.D)


class SavingsBehaviorModel:
    """
    Customer Savings Behavior Model
    Implements: S_t = β₀ + Σ(β_i * C_i) + Σ(γ_ψ * Ψ) + λ * S_{t-1} + ε_t
    """

    def __init__(self, params: ModelParameters = None):
        self.params = params or ModelParameters()
        self.history = []

    def predict_single(self,
                      utility: UtilityDimensions,
                      context: ContextFactors,
                      lagged_savings: float = 0.0,
                      add_noise: bool = True) -> float:
        """
        Predict monthly savings for a customer

        Args:
            utility: Customer utility dimensions
            context: Customer context factors
            lagged_savings: Previous month's savings (for habit term)
            add_noise: Whether to add random shock

        Returns:
            Predicted monthly savings (CHF)
        """

        # Utility component
        utility_effect = utility.weighted_sum(self.params)

        # Context component
        context_effect = (
            self.params.gamma_tau * context.tau +
            self.params.gamma_delta * context.delta +
            self.params.gamma_rho * (1 - context.rho) +  # Inverted: high risk = low savings
            self.params.gamma_sigma * context.sigma
        )

        # Habit component
        habit_effect = self.params.lambda_habit * lagged_savings

        # Random shock
        noise = np.random.normal(0, self.params.sigma_noise) if add_noise else 0

        # Combine
        savings = (self.params.beta_0 +
                   utility_effect +
                   context_effect +
                   habit_effect +
                   noise)

        return max(0, savings)  # Non-negative

    def simulate_timeseries(self,
                           utility: UtilityDimensions,
                           context: ContextFactors,
                           periods: int = 12,
                           initial_savings: float = 0.0) -> np.ndarray:
        """
        Simulate savings over time (with habit formation)

        Args:
            utility: Fixed utility for entire period
            context: Fixed context for entire period
            periods: Number of months to simulate
            initial_savings: Starting savings amount

        Returns:
            Array of monthly savings predictions
        """

        savings_path = np.zeros(periods)
        lagged = initial_savings

        for t in range(periods):
            savings_t = self.predict_single(utility, context,
                                           lagged_savings=lagged,
                                           add_noise=True)
            savings_path[t] = savings_t
            lagged = savings_t

        return savings_path

    def intervention_effect(self,
                           baseline_utility: UtilityDimensions,
                           baseline_context: ContextFactors,
                           intervention: str) -> Tuple[float, float]:
        """
        Estimate effect of an intervention

        Args:
            baseline_utility: Customer utility baseline
            baseline_context: Customer context baseline
            intervention: Type of intervention

        Returns:
            (baseline_savings, intervention_savings)
        """

        baseline = self.predict_single(baseline_utility, baseline_context, add_noise=False)

        if intervention == "increase_trust":
            context_int = ContextFactors(
                tau=min(1.0, baseline_context.tau + 0.20),
                delta=baseline_context.delta,
                rho=baseline_context.rho,
                sigma=baseline_context.sigma
            )

        elif intervention == "increase_digital":
            context_int = ContextFactors(
                tau=baseline_context.tau,
                delta=min(1.0, baseline_context.delta + 0.20),
                rho=baseline_context.rho,
                sigma=baseline_context.sigma
            )

        elif intervention == "increase_income_stability":
            context_int = ContextFactors(
                tau=baseline_context.tau,
                delta=baseline_context.delta,
                rho=baseline_context.rho,
                sigma=min(1.0, baseline_context.sigma + 0.20)
            )

        elif intervention == "increase_deliberation":
            utility_int = UtilityDimensions(
                F=baseline_utility.F,
                E=baseline_utility.E,
                P=baseline_utility.P,
                S=baseline_utility.S,
                D=min(1.0, baseline_utility.D + 0.25)
            )
            intervention_savings = self.predict_single(utility_int, baseline_context, add_noise=False)
            return (baseline, intervention_savings)

        else:
            raise ValueError(f"Unknown intervention: {intervention}")

        intervention_savings = self.predict_single(baseline_utility, context_int, add_noise=False)
        return (baseline, intervention_savings)


# ============================================================================
# CUSTOMER SEGMENTS
# ============================================================================

class CustomerSegments:
    """Predefined customer segments for analysis"""

    @staticmethod
    def digital_native_high_earner():
        """Segment A: High potential saver"""
        utility = UtilityDimensions(F=0.9, E=0.8, P=0.9, S=0.7, D=0.8)
        context = ContextFactors(tau=0.85, delta=0.90, rho=0.60, sigma=0.85)
        return utility, context, "Digital-Native High-Earner"

    @staticmethod
    def traditional_conservative():
        """Segment B: Lower potential, needs trust building"""
        utility = UtilityDimensions(F=0.6, E=0.5, P=0.5, S=0.4, D=0.6)
        context = ContextFactors(tau=0.70, delta=0.35, rho=0.80, sigma=0.60)
        return utility, context, "Traditional Conservative"

    @staticmethod
    def young_professional():
        """Segment C: Growth potential"""
        utility = UtilityDimensions(F=0.7, E=0.7, P=0.8, S=0.6, D=0.7)
        context = ContextFactors(tau=0.75, delta=0.80, rho=0.65, sigma=0.65)
        return utility, context, "Young Professional"

    @staticmethod
    def baseline_average():
        """Average customer (from model specification)"""
        utility = UtilityDimensions(F=0.70, E=0.60, P=0.60, S=0.40, D=0.50)
        context = ContextFactors(tau=0.72, delta=0.65, rho=0.68, sigma=0.70)
        return utility, context, "Average Customer"


# ============================================================================
# ANALYSIS FUNCTIONS
# ============================================================================

def analyze_interventions(model: SavingsBehaviorModel,
                         utility: UtilityDimensions,
                         context: ContextFactors):
    """Analyze impact of different interventions"""

    interventions = [
        "increase_trust",
        "increase_digital",
        "increase_income_stability",
        "increase_deliberation"
    ]

    results = []
    for intervention in interventions:
        baseline, intervention_savings = model.intervention_effect(utility, context, intervention)
        effect = intervention_savings - baseline
        pct_change = (effect / baseline) * 100 if baseline > 0 else 0

        results.append({
            'Intervention': intervention.replace('_', ' ').title(),
            'Baseline (CHF)': baseline,
            'With Intervention (CHF)': intervention_savings,
            'Effect (CHF)': effect,
            'Effect (%)': pct_change
        })

    return pd.DataFrame(results)


def main():
    """Main demonstration"""

    print("=" * 80)
    print("UBS CUSTOMER SAVINGS BEHAVIOR MODEL SIMULATOR")
    print("Model ID: UBS-FIN-SB-001")
    print("=" * 80)

    # Initialize model
    model = SavingsBehaviorModel()

    # ========================================================================
    # 1. Baseline Prediction
    # ========================================================================
    print("\n1. BASELINE PREDICTION")
    print("-" * 80)

    utility_avg, context_avg, label_avg = CustomerSegments.baseline_average()
    baseline_pred = model.predict_single(utility_avg, context_avg, add_noise=False)

    print(f"{label_avg}:")
    print(f"  Predicted monthly savings: CHF {baseline_pred:.0f}")
    print(f"  Context: Trust={context_avg.tau}, Digital={context_avg.delta}, "
          f"Risk={context_avg.rho}, Income={context_avg.sigma}")

    # ========================================================================
    # 2. Segment Analysis
    # ========================================================================
    print("\n2. SEGMENT ANALYSIS")
    print("-" * 80)

    segments = [
        CustomerSegments.digital_native_high_earner(),
        CustomerSegments.traditional_conservative(),
        CustomerSegments.young_professional()
    ]

    segment_results = []
    for utility, context, label in segments:
        pred = model.predict_single(utility, context, add_noise=False)
        segment_results.append({
            'Segment': label,
            'Monthly Savings (CHF)': pred,
            'Trust': context.tau,
            'Digital': context.delta,
            'Income Stability': context.sigma
        })

    df_segments = pd.DataFrame(segment_results)
    print(df_segments.to_string(index=False))

    # ========================================================================
    # 3. Intervention Analysis
    # ========================================================================
    print("\n3. INTERVENTION ANALYSIS (on Average Customer)")
    print("-" * 80)

    df_interventions = analyze_interventions(model, utility_avg, context_avg)
    print(df_interventions.to_string(index=False))

    # ========================================================================
    # 4. Time Series Simulation
    # ========================================================================
    print("\n4. TIME SERIES SIMULATION (12 months, with habit formation)")
    print("-" * 80)

    np.random.seed(42)  # For reproducibility
    savings_path = model.simulate_timeseries(utility_avg, context_avg, periods=12)

    print(f"Month 1-3 avg: CHF {savings_path[:3].mean():.0f}")
    print(f"Month 10-12 avg: CHF {savings_path[-3:].mean():.0f}")
    print(f"Trend: {'Increasing' if savings_path[-1] > savings_path[0] else 'Decreasing'}")

    # ========================================================================
    # 5. Comparison: With vs Without Habit
    # ========================================================================
    print("\n5. HABIT FORMATION EFFECT")
    print("-" * 80)

    # With habit
    model_with_habit = SavingsBehaviorModel(ModelParameters(lambda_habit=0.62))
    path_with_habit = model_with_habit.simulate_timeseries(utility_avg, context_avg, periods=24)

    # Without habit
    model_no_habit = SavingsBehaviorModel(ModelParameters(lambda_habit=0.0))
    path_no_habit = model_no_habit.simulate_timeseries(utility_avg, context_avg, periods=24)

    print(f"With habit - Month 24 savings: CHF {path_with_habit[-1]:.0f}")
    print(f"No habit - Month 24 savings: CHF {path_no_habit[-1]:.0f}")
    print(f"Habit contribution: CHF {path_with_habit[-1] - path_no_habit[-1]:.0f}")

    # ========================================================================
    # 6. Monte Carlo Uncertainty Analysis
    # ========================================================================
    print("\n6. MONTE CARLO UNCERTAINTY (1000 simulations)")
    print("-" * 80)

    np.random.seed(42)
    simulations = 1000
    predictions = []

    for _ in range(simulations):
        pred = model.predict_single(utility_avg, context_avg, add_noise=True)
        predictions.append(pred)

    predictions = np.array(predictions)
    ci_lower = np.percentile(predictions, 5)
    ci_upper = np.percentile(predictions, 95)

    print(f"Mean prediction: CHF {predictions.mean():.0f}")
    print(f"90% Confidence Interval: CHF {ci_lower:.0f} - CHF {ci_upper:.0f}")
    print(f"Std Dev: CHF {predictions.std():.0f}")

    print("\n" + "=" * 80)
    print("END OF SIMULATION")
    print("=" * 80)


if __name__ == "__main__":
    main()
