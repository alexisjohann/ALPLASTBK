#!/usr/bin/env python3
"""
UBS Choice Architecture Simulator
Interactive UI for behavioral intervention design

Model ID: UBS-FIN-SB-001
Framework: Evidence-Based Framework (EBF) - 10C Methodology
"""

import streamlit as st
import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import Dict, List, Tuple

# ============================================================================
# MODEL (from UBS-FIN-SB-001_simulation.py)
# ============================================================================

@dataclass
class ModelParameters:
    """Parameters for UBS savings behavior model"""
    beta_0: float = 850.0
    beta_F: float = 0.25
    beta_E: float = 0.15
    beta_P: float = 0.18
    beta_S: float = 0.08
    beta_D: float = 0.12
    gamma_tau: float = 180.0
    gamma_delta: float = 120.0
    gamma_rho: float = -50.0
    gamma_sigma: float = 95.0
    lambda_habit: float = 0.62
    sigma_noise: float = 80.0


@dataclass
class ContextFactors:
    """Context variables (Ψ)"""
    tau: float      # Trust
    delta: float    # Digital adoption
    rho: float      # Risk aversion
    sigma: float    # Income stability


@dataclass
class UtilityDimensions:
    """Utility components (C)"""
    F: float  # Financial
    E: float  # Emotional
    P: float  # Practical
    S: float  # Social
    D: float  # Deliberative

    def weighted_sum(self, params: ModelParameters) -> float:
        return (params.beta_F * self.F +
                params.beta_E * self.E +
                params.beta_P * self.P +
                params.beta_S * self.S +
                params.beta_D * self.D)


class SavingsBehaviorModel:
    """Customer Savings Behavior Model"""

    def __init__(self, params: ModelParameters = None):
        self.params = params or ModelParameters()

    def predict(self, utility: UtilityDimensions, context: ContextFactors,
                lagged_savings: float = 0.0, add_noise: bool = False) -> float:
        utility_effect = utility.weighted_sum(self.params)
        context_effect = (
            self.params.gamma_tau * context.tau +
            self.params.gamma_delta * context.delta +
            self.params.gamma_rho * (1 - context.rho) +
            self.params.gamma_sigma * context.sigma
        )
        habit_effect = self.params.lambda_habit * lagged_savings
        noise = np.random.normal(0, self.params.sigma_noise) if add_noise else 0
        savings = self.params.beta_0 + utility_effect + context_effect + habit_effect + noise
        return max(0, savings)

    def monte_carlo(self, utility: UtilityDimensions, context: ContextFactors,
                    n_simulations: int = 1000) -> Tuple[float, float, float]:
        predictions = [self.predict(utility, context, add_noise=True)
                       for _ in range(n_simulations)]
        return np.mean(predictions), np.percentile(predictions, 5), np.percentile(predictions, 95)


# ============================================================================
# INTERVENTIONS
# ============================================================================

INTERVENTIONS = {
    "trust_campaign": {
        "name": "Trust Campaign",
        "description": "175 Jahre Stabilität kommunizieren",
        "effect_param": "tau",
        "effect_size": 0.18,
        "expected_chf": 160,
        "cost": "Medium",
        "roi": "High"
    },
    "digital_adoption": {
        "name": "Mobile App Promotion",
        "description": "Digital-First Onboarding",
        "effect_param": "delta",
        "effect_size": 0.20,
        "expected_chf": 90,
        "cost": "Low",
        "roi": "Very High"
    },
    "auto_save": {
        "name": "Auto-Save Setup",
        "description": "Automatische Sparbeiträge",
        "effect_param": "habit",
        "effect_size": 0.13,
        "expected_chf": 120,
        "cost": "Low",
        "roi": "Very High"
    },
    "financial_education": {
        "name": "Financial Education",
        "description": "Finanzwissen-Programme",
        "effect_param": "D",
        "effect_size": 0.15,
        "expected_chf": 45,
        "cost": "Low",
        "roi": "High"
    }
}

SEGMENTS = {
    "digital_native": {
        "name": "Digital-Native High-Earner",
        "utility": UtilityDimensions(F=0.9, E=0.8, P=0.9, S=0.7, D=0.8),
        "context": ContextFactors(tau=0.85, delta=0.90, rho=0.60, sigma=0.85),
        "color": "#2ecc71"
    },
    "traditional": {
        "name": "Traditional Conservative",
        "utility": UtilityDimensions(F=0.6, E=0.5, P=0.5, S=0.4, D=0.6),
        "context": ContextFactors(tau=0.70, delta=0.35, rho=0.80, sigma=0.60),
        "color": "#e74c3c"
    },
    "young_professional": {
        "name": "Young Professional",
        "utility": UtilityDimensions(F=0.7, E=0.7, P=0.8, S=0.6, D=0.7),
        "context": ContextFactors(tau=0.75, delta=0.80, rho=0.65, sigma=0.65),
        "color": "#3498db"
    },
    "average": {
        "name": "Average Customer",
        "utility": UtilityDimensions(F=0.70, E=0.60, P=0.60, S=0.40, D=0.50),
        "context": ContextFactors(tau=0.72, delta=0.65, rho=0.68, sigma=0.70),
        "color": "#9b59b6"
    }
}


# ============================================================================
# STREAMLIT APP
# ============================================================================

def main():
    st.set_page_config(
        page_title="UBS Choice Architecture",
        page_icon="🏦",
        layout="wide"
    )

    st.title("🏦 UBS Choice Architecture Simulator")
    st.markdown("**Model:** UBS-FIN-SB-001 | **Framework:** EBF 10C Methodology")

    # Initialize model
    model = SavingsBehaviorModel()

    # ========================================================================
    # SIDEBAR: Context Inputs
    # ========================================================================
    st.sidebar.header("📊 Context (Ψ)")

    # Segment preset
    segment_choice = st.sidebar.selectbox(
        "Segment Preset",
        options=["custom"] + list(SEGMENTS.keys()),
        format_func=lambda x: "Custom" if x == "custom" else SEGMENTS[x]["name"]
    )

    if segment_choice != "custom":
        seg = SEGMENTS[segment_choice]
        default_tau = seg["context"].tau
        default_delta = seg["context"].delta
        default_rho = seg["context"].rho
        default_sigma = seg["context"].sigma
    else:
        default_tau, default_delta, default_rho, default_sigma = 0.72, 0.65, 0.68, 0.70

    st.sidebar.markdown("---")

    tau = st.sidebar.slider("Trust (τ)", 0.0, 1.0, default_tau, 0.01,
                            help="Vertrauen in UBS/Finanzsystem")
    delta = st.sidebar.slider("Digital Adoption (δ)", 0.0, 1.0, default_delta, 0.01,
                              help="Mobile Banking Nutzung")
    rho = st.sidebar.slider("Risk Aversion (ρ)", 0.0, 1.0, default_rho, 0.01,
                            help="Risikoaversion (1=sehr konservativ)")
    sigma = st.sidebar.slider("Income Stability (σ)", 0.0, 1.0, default_sigma, 0.01,
                              help="Einkommensstabilität")

    context = ContextFactors(tau=tau, delta=delta, rho=rho, sigma=sigma)

    # Use average utility dimensions
    utility = UtilityDimensions(F=0.70, E=0.60, P=0.60, S=0.40, D=0.50)

    # ========================================================================
    # MAIN: Prediction
    # ========================================================================
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("💰 Prediction")

        baseline = model.predict(utility, context)
        mean_pred, ci_lower, ci_upper = model.monte_carlo(utility, context)

        # Big metric
        st.metric(
            label="Predicted Monthly Savings",
            value=f"CHF {baseline:.0f}",
            delta=f"90% CI: {ci_lower:.0f} - {ci_upper:.0f}"
        )

        # Progress bar
        max_savings = 2000
        progress = min(baseline / max_savings, 1.0)
        st.progress(progress)
        st.caption(f"{progress*100:.0f}% of maximum potential (CHF {max_savings})")

    with col2:
        st.header("📈 Context Effects")
        effects_data = {
            "Factor": ["Trust", "Digital", "Risk", "Income"],
            "Value": [tau, delta, rho, sigma],
            "Effect (CHF)": [
                f"+{180*tau:.0f}",
                f"+{120*delta:.0f}",
                f"{-50*(1-rho):.0f}",
                f"+{95*sigma:.0f}"
            ]
        }
        st.dataframe(pd.DataFrame(effects_data), hide_index=True)

    # ========================================================================
    # INTERVENTIONS
    # ========================================================================
    st.markdown("---")
    st.header("🎯 Interventions")

    selected_interventions = []

    cols = st.columns(4)
    for i, (key, intervention) in enumerate(INTERVENTIONS.items()):
        with cols[i]:
            selected = st.checkbox(
                intervention["name"],
                help=intervention["description"]
            )
            st.caption(f"+{intervention['expected_chf']} CHF")
            st.caption(f"ROI: {intervention['roi']}")
            if selected:
                selected_interventions.append(key)

    # Calculate combined effect
    if selected_interventions:
        total_effect = sum(INTERVENTIONS[k]["expected_chf"] for k in selected_interventions)
        new_prediction = baseline + total_effect
        pct_increase = (total_effect / baseline) * 100

        st.markdown("### Combined Effect")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Baseline", f"CHF {baseline:.0f}")
        with col2:
            st.metric("With Interventions", f"CHF {new_prediction:.0f}", f"+{total_effect:.0f}")
        with col3:
            st.metric("Increase", f"+{pct_increase:.1f}%")

        # Synergy note
        if len(selected_interventions) > 1:
            st.info("💡 **Synergy Tip:** Trust + Digital zeigen γ=0.60 Komplementarität - "
                    "kombinierte Wirkung kann höher sein als Summe der Einzeleffekte!")

    # ========================================================================
    # SEGMENT COMPARISON
    # ========================================================================
    st.markdown("---")
    st.header("👥 Segment Comparison")

    segment_data = []
    for key, seg in SEGMENTS.items():
        pred = model.predict(seg["utility"], seg["context"])
        segment_data.append({
            "Segment": seg["name"],
            "Trust": seg["context"].tau,
            "Digital": seg["context"].delta,
            "Prediction (CHF)": f"{pred:.0f}"
        })

    df_segments = pd.DataFrame(segment_data)
    st.dataframe(df_segments, hide_index=True, use_container_width=True)

    # ========================================================================
    # FOOTER
    # ========================================================================
    st.markdown("---")
    st.caption("**Model:** UBS-FIN-SB-001 | **Status:** CONFIG-derived, Validation Pending | "
               "**Framework:** Evidence-Based Framework (EBF)")
    st.caption("Based on: Fehr (2010), Thaler & Sunstein (2008), Guiso et al. (2008), "
               "Kahneman (2011)")


if __name__ == "__main__":
    main()
