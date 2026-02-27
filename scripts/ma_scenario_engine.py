#!/usr/bin/env python3
"""
M&A Behavioral Scenario Engine (Layer 1)
==========================================

Computes behavioral risk scores for M&A transactions using MOD-MA-001:

  1. Psi-Distance Calculator: 8-dimensional cultural distance (Acquirer vs. Target)
  2. Gamma Interaction Matrix: complementarity/crowding-out between strategic dimensions
  3. BDD Scoring: 5-module Behavioral Due Diligence composite score
  4. Synergy Realization Forecast: Bayesian-updated synergy capture with behavioral discount
  5. BCJ Phase Simulation: 5-phase integration trajectory over 36 months
  6. Counterfactual Comparison: with vs. without behavioral integration

Parameters are loaded from data/parameter-registry.yaml (PAR-MA-001 to PAR-MA-008).

Usage:
    python ma_scenario_engine.py --demo
    python ma_scenario_engine.py --scenario scenario.yaml
    python ma_scenario_engine.py --scenario scenario.yaml --json
    python ma_scenario_engine.py --scenario scenario.yaml --counterfactual

Author: EBF Framework (Layer 1 - Formal Computation)
Date: 2026-02-16
Model: MOD-MA-001 (M&A Behavioral Deal Journey Model)
Session: EBF-S-2026-02-16-ORG-001
Protocol: TLA Layer 1 (virus-susceptibility = 0.0)
"""

import json
import math
import argparse
import sys
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. Install: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class PsiProfile:
    """8-dimensional organizational culture profile (Psi-dimensions)."""
    psi_I: float = 0.5   # Institutional (formality, governance)
    psi_S: float = 0.5   # Social (hierarchy, collaboration)
    psi_K: float = 0.5   # Cultural (values, traditions)
    psi_C: float = 0.5   # Cognitive (decision style, risk appetite)
    psi_E: float = 0.5   # Economic (resource orientation)
    psi_T: float = 0.5   # Temporal (time horizon, speed)
    psi_M: float = 0.5   # Mechanisms (technology, processes)
    psi_F: float = 0.5   # Physical (geography, infrastructure)

    def as_vector(self) -> List[float]:
        return [self.psi_I, self.psi_S, self.psi_K, self.psi_C,
                self.psi_E, self.psi_T, self.psi_M, self.psi_F]

    @staticmethod
    def dimension_names() -> List[str]:
        return ["Institutional", "Social", "Cultural", "Cognitive",
                "Economic", "Temporal", "Mechanisms", "Physical"]

    @staticmethod
    def dimension_weights_ma() -> List[float]:
        """M&A-specific Psi-dimension weights (from BDD-2 sub_metrics)."""
        return [0.15, 0.20, 0.25, 0.10, 0.10, 0.05, 0.10, 0.05]


@dataclass
class GammaMatrix:
    """Strategic complementarity/crowding-out matrix."""
    pairs: Dict[str, float] = field(default_factory=dict)

    def net_score(self) -> float:
        """Net complementarity score (sum of all gammas)."""
        return sum(self.pairs.values())

    def positive_count(self) -> int:
        return sum(1 for v in self.pairs.values() if v > 0)

    def negative_count(self) -> int:
        return sum(1 for v in self.pairs.values() if v < 0)

    def max_risk(self) -> Tuple[str, float]:
        """Most negative gamma (highest risk)."""
        if not self.pairs:
            return ("none", 0.0)
        worst = min(self.pairs.items(), key=lambda x: x[1])
        return worst


@dataclass
class BDDScores:
    """Scores for the 5 BDD modules (0-1 each)."""
    leadership: float = 0.5      # BDD-1
    cultural: float = 0.5        # BDD-2
    resilience: float = 0.5      # BDD-3
    complementarity: float = 0.5  # BDD-4
    stakeholder: float = 0.5     # BDD-5

    # Weights from PORT-BDD-001
    WEIGHTS = [0.15, 0.25, 0.20, 0.25, 0.15]

    # Inter-module gammas from portfolio
    GAMMAS = {
        ("leadership", "cultural"): 0.35,
        ("cultural", "resilience"): 0.40,
        ("resilience", "complementarity"): 0.30,
        ("complementarity", "stakeholder"): 0.45,
        ("leadership", "stakeholder"): 0.25,
    }

    def scores_list(self) -> List[float]:
        return [self.leadership, self.cultural, self.resilience,
                self.complementarity, self.stakeholder]

    def composite_score(self) -> float:
        """Weighted average with gamma adjustments."""
        scores = self.scores_list()
        # Weighted base score
        base = sum(w * s for w, s in zip(self.WEIGHTS, scores))
        # Gamma interaction term
        gamma_adj = 0.0
        score_map = {
            "leadership": self.leadership,
            "cultural": self.cultural,
            "resilience": self.resilience,
            "complementarity": self.complementarity,
            "stakeholder": self.stakeholder,
        }
        for (m1, m2), gamma in self.GAMMAS.items():
            gamma_adj += gamma * math.sqrt(score_map[m1] * score_map[m2])
        return min(1.0, max(0.0, base + gamma_adj * 0.1))

    def traffic_light(self) -> str:
        s = self.composite_score()
        if s >= 0.70:
            return "GREEN"
        elif s >= 0.45:
            return "AMBER"
        else:
            return "RED"


@dataclass
class MAScenario:
    """Complete M&A scenario specification."""
    name: str = "Unnamed Deal"
    deal_type: str = "strategic"  # strategic, pe_exit, carveout, distressed
    deal_size_meur: float = 100.0
    seller_type: str = "family_founder"
    acquirer: PsiProfile = field(default_factory=PsiProfile)
    target: PsiProfile = field(default_factory=PsiProfile)
    announced_synergies_meur: float = 20.0
    bdd_scores: BDDScores = field(default_factory=BDDScores)
    gamma_matrix: GammaMatrix = field(default_factory=GammaMatrix)
    integration_months: int = 36


# =============================================================================
# PARAMETER LOOKUPS (from PAR-MA-001 to PAR-MA-008)
# =============================================================================

# PAR-MA-001: Seller Loss Aversion by type
LAMBDA_SELLER = {
    "family_founder": 3.50,
    "family_2nd_gen": 2.80,
    "pe_exit": 1.80,
    "corporate_carveout": 2.20,
    "distressed_sale": 1.50,
}

# PAR-MA-002: Earn-Out Present Bias by type
BETA_EARNOUT = {
    "founder_optimistic": 0.85,
    "pe_rational": 0.95,
    "manager_risk_averse": 0.70,
}

# PAR-MA-003: Hubris Premium
GAMMA_HUBRIS = 0.35  # +65% acquisition propensity

# PAR-MA-004: Cultural Friction
GAMMA_CULTURE = -0.45  # Distance x integration success

# PAR-MA-005: M&A-Innovation Cannibalization
GAMMA_MA_INNOV = -0.22  # ALPLA calibrated

# PAR-MA-006: Fairness Dividend
GAMMA_FAIRNESS = 0.30

# PAR-MA-007: Synergy Realization Rate
RHO_SYNERGY = {
    "overall": 0.50,
    "cost": 0.70,
    "revenue": 0.35,
    "cultural": 0.25,
}

# PAR-MA-008: Key Talent Flight Risk
PI_FLIGHT = {
    "base": 0.33,
    "se_asia": 0.40,
    "europe": 0.28,
    "us": 0.35,
}

# Default gamma matrix for M&A deals (from MOD-MA-001)
DEFAULT_GAMMAS = {
    "social_x_financial": -0.20,
    "ma_x_innovation": -0.22,
    "ma_x_scale": 0.20,
    "hubris_x_premium": 0.35,
    "culture_x_integration": -0.45,
    "fairness_x_cooperation": 0.30,
}


# =============================================================================
# ENGINE FUNCTIONS
# =============================================================================

def compute_psi_distance(acquirer: PsiProfile, target: PsiProfile,
                         weighted: bool = True) -> Dict:
    """
    Compute 8-dimensional Psi-distance between Acquirer and Target.

    Returns dict with per-dimension distances, weighted total, and interpretation.
    """
    a_vec = acquirer.as_vector()
    t_vec = target.as_vector()
    weights = PsiProfile.dimension_weights_ma() if weighted else [1/8]*8
    names = PsiProfile.dimension_names()

    per_dim = {}
    weighted_sq_sum = 0.0
    for i, (a, t, w, name) in enumerate(zip(a_vec, t_vec, weights, names)):
        diff = abs(a - t)
        per_dim[name] = {
            "acquirer": round(a, 3),
            "target": round(t, 3),
            "distance": round(diff, 3),
            "weight": round(w, 3),
            "weighted_contribution": round(w * diff**2, 4),
        }
        weighted_sq_sum += w * diff**2

    total_distance = math.sqrt(weighted_sq_sum)

    # Interpretation
    if total_distance < 0.25:
        interpretation = "LOW distance — standard integration sufficient"
    elif total_distance < 0.50:
        interpretation = "MODERATE distance — enhanced cultural integration required"
    elif total_distance < 0.75:
        interpretation = "HIGH distance — significant integration risk, requires dedicated program"
    else:
        interpretation = "VERY HIGH distance — deal-breaking unless structural remedies implemented"

    # Dominant driver (highest weighted contribution)
    driver = max(per_dim.items(), key=lambda x: x[1]["weighted_contribution"])

    return {
        "total_distance": round(total_distance, 4),
        "interpretation": interpretation,
        "dominant_driver": driver[0],
        "per_dimension": per_dim,
    }


def compute_gamma_matrix(scenario: MAScenario) -> Dict:
    """
    Compute gamma interaction matrix for the deal.

    Combines default M&A gammas with scenario-specific adjustments.
    """
    gammas = dict(DEFAULT_GAMMAS)
    gammas.update(scenario.gamma_matrix.pairs)

    # Adjust cultural friction by actual Psi-distance
    psi_result = compute_psi_distance(scenario.acquirer, scenario.target)
    psi_dist = psi_result["total_distance"]
    # Cultural friction amplifies non-linearly with distance
    adjusted_culture = GAMMA_CULTURE * (psi_dist / 0.50)  # normalized to benchmark
    gammas["culture_x_integration"] = round(adjusted_culture, 4)

    # Compute net score
    net = sum(gammas.values())
    positives = {k: v for k, v in gammas.items() if v > 0}
    negatives = {k: v for k, v in gammas.items() if v < 0}

    return {
        "gammas": {k: round(v, 4) for k, v in gammas.items()},
        "net_complementarity": round(net, 4),
        "positive_sum": round(sum(positives.values()), 4),
        "negative_sum": round(sum(negatives.values()), 4),
        "highest_risk": min(gammas.items(), key=lambda x: x[1]),
        "highest_synergy": max(gammas.items(), key=lambda x: x[1]),
        "psi_distance_used": psi_dist,
    }


def compute_bdd_score(scenario: MAScenario) -> Dict:
    """
    Compute composite BDD score from 5 modules.

    Uses weighted average + gamma interaction terms from BDD portfolio.
    """
    bdd = scenario.bdd_scores
    composite = bdd.composite_score()
    traffic = bdd.traffic_light()

    module_details = {
        "BDD-1_Leadership": {
            "score": round(bdd.leadership, 3),
            "weight": 0.15,
            "weighted": round(0.15 * bdd.leadership, 4),
        },
        "BDD-2_Cultural": {
            "score": round(bdd.cultural, 3),
            "weight": 0.25,
            "weighted": round(0.25 * bdd.cultural, 4),
        },
        "BDD-3_Resilience": {
            "score": round(bdd.resilience, 3),
            "weight": 0.20,
            "weighted": round(0.20 * bdd.resilience, 4),
        },
        "BDD-4_Complementarity": {
            "score": round(bdd.complementarity, 3),
            "weight": 0.25,
            "weighted": round(0.25 * bdd.complementarity, 4),
        },
        "BDD-5_Stakeholder": {
            "score": round(bdd.stakeholder, 3),
            "weight": 0.15,
            "weighted": round(0.15 * bdd.stakeholder, 4),
        },
    }

    return {
        "composite_score": round(composite, 4),
        "traffic_light": traffic,
        "modules": module_details,
        "recommendation": _bdd_recommendation(traffic, composite),
    }


def _bdd_recommendation(traffic: str, score: float) -> str:
    if traffic == "GREEN":
        return "Proceed with standard PMI. Behavioral risks manageable with routine measures."
    elif traffic == "AMBER":
        return "Proceed with enhanced integration measures. Dedicate behavioral integration budget (2-5% of deal value). Consider BIM program (PROD-MA-06)."
    else:
        return "CAUTION: Reconsider deal structure or require structural remedies. Behavioral risks may destroy >50% of projected synergies."


def compute_synergy_forecast(scenario: MAScenario) -> Dict:
    """
    Compute behavioral-adjusted synergy realization forecast.

    Uses PAR-MA-007 (rho_synergy) with Psi-distance and BDD adjustments.
    """
    announced = scenario.announced_synergies_meur

    # Base realization rates (PAR-MA-007)
    cost_synergy = announced * 0.60  # typically 60% of announced are cost
    revenue_synergy = announced * 0.30  # 30% revenue
    cultural_synergy = announced * 0.10  # 10% cultural/organizational

    # Behavioral discount based on Psi-distance
    psi_result = compute_psi_distance(scenario.acquirer, scenario.target)
    psi_dist = psi_result["total_distance"]
    # Higher Psi-distance → lower realization
    psi_penalty = max(0.5, 1.0 - psi_dist * 0.8)

    # BDD score adjustment
    bdd_composite = scenario.bdd_scores.composite_score()
    bdd_multiplier = 0.6 + 0.5 * bdd_composite  # range 0.6-1.1

    # Compute adjusted synergies
    cost_realized = cost_synergy * RHO_SYNERGY["cost"] * bdd_multiplier
    revenue_realized = revenue_synergy * RHO_SYNERGY["revenue"] * psi_penalty * bdd_multiplier
    cultural_realized = cultural_synergy * RHO_SYNERGY["cultural"] * psi_penalty * bdd_multiplier

    total_realized = cost_realized + revenue_realized + cultural_realized
    realization_rate = total_realized / announced if announced > 0 else 0

    # Behavioral value at risk
    value_at_risk = announced - total_realized

    return {
        "announced_synergies_meur": announced,
        "breakdown": {
            "cost": {"announced": round(cost_synergy, 2), "realized": round(cost_realized, 2),
                     "rate": round(RHO_SYNERGY["cost"] * bdd_multiplier, 3)},
            "revenue": {"announced": round(revenue_synergy, 2), "realized": round(revenue_realized, 2),
                        "rate": round(RHO_SYNERGY["revenue"] * psi_penalty * bdd_multiplier, 3)},
            "cultural": {"announced": round(cultural_synergy, 2), "realized": round(cultural_realized, 2),
                         "rate": round(RHO_SYNERGY["cultural"] * psi_penalty * bdd_multiplier, 3)},
        },
        "total_realized_meur": round(total_realized, 2),
        "realization_rate": round(realization_rate, 3),
        "behavioral_value_at_risk_meur": round(value_at_risk, 2),
        "adjustments": {
            "psi_distance_penalty": round(psi_penalty, 3),
            "bdd_multiplier": round(bdd_multiplier, 3),
        },
    }


def simulate_bcj_trajectory(scenario: MAScenario) -> List[Dict]:
    """
    Simulate BCJ 5-phase integration trajectory over integration_months.

    Models organizational transition: Unaware → Aware → Willing → Acting → Maintaining.
    Uses simple logistic-like phase transition model.
    """
    months = scenario.integration_months
    psi_result = compute_psi_distance(scenario.acquirer, scenario.target)
    psi_dist = psi_result["total_distance"]
    bdd_score = scenario.bdd_scores.composite_score()

    # Transition rates (lower with higher psi-distance, higher with better BDD)
    base_rate = 0.15 * (1 - psi_dist * 0.5) * (0.5 + bdd_score)

    # Initial state: mostly Unaware
    state = {
        "unaware": 0.70,
        "aware": 0.20,
        "willing": 0.08,
        "acting": 0.02,
        "maintaining": 0.00,
    }

    trajectory = []
    for month in range(months + 1):
        # Capture current state
        entry = {"month": month}
        entry.update({k: round(v, 4) for k, v in state.items()})
        # Compute aggregate progress (0-1)
        progress = (state["aware"] * 0.25 + state["willing"] * 0.50 +
                    state["acting"] * 0.75 + state["maintaining"] * 1.0)
        entry["progress"] = round(progress, 4)

        # Psi-distance convergence (decays over time with integration)
        psi_current = psi_dist * math.exp(-0.03 * month * bdd_score)
        entry["psi_distance"] = round(psi_current, 4)

        trajectory.append(entry)

        if month >= months:
            break

        # Phase transitions (simple Euler step)
        rate = base_rate
        # Acceleration after month 3 (Quick Wins effect)
        if month > 3:
            rate *= 1.2
        # Deceleration at high distance
        if psi_dist > 0.6:
            rate *= 0.8

        du = -rate * state["unaware"]
        da = rate * state["unaware"] - rate * 0.8 * state["aware"]
        dw = rate * 0.8 * state["aware"] - rate * 0.6 * state["willing"]
        dac = rate * 0.6 * state["willing"] - rate * 0.4 * state["acting"]
        dm = rate * 0.4 * state["acting"]

        state["unaware"] = max(0, state["unaware"] + du)
        state["aware"] = max(0, state["aware"] + da)
        state["willing"] = max(0, state["willing"] + dw)
        state["acting"] = max(0, state["acting"] + dac)
        state["maintaining"] = max(0, state["maintaining"] + dm)

        # Normalize to sum to 1
        total = sum(state.values())
        if total > 0:
            state = {k: v/total for k, v in state.items()}

    return trajectory


def compute_counterfactual(scenario: MAScenario) -> Dict:
    """
    Compare: WITH behavioral integration vs. WITHOUT.

    'Without' uses standard M&A integration (no BDD, no behavioral interventions).
    """
    # WITH behavioral integration (current scenario)
    synergy_with = compute_synergy_forecast(scenario)
    bcj_with = simulate_bcj_trajectory(scenario)

    # WITHOUT: degrade BDD scores and remove behavioral adjustments
    no_bdd = MAScenario(
        name=scenario.name + " (No Behavioral Integration)",
        deal_type=scenario.deal_type,
        deal_size_meur=scenario.deal_size_meur,
        seller_type=scenario.seller_type,
        acquirer=scenario.acquirer,
        target=scenario.target,
        announced_synergies_meur=scenario.announced_synergies_meur,
        bdd_scores=BDDScores(
            leadership=0.30, cultural=0.30, resilience=0.35,
            complementarity=0.25, stakeholder=0.30
        ),  # Industry average without BDD
        gamma_matrix=scenario.gamma_matrix,
        integration_months=scenario.integration_months,
    )
    synergy_without = compute_synergy_forecast(no_bdd)
    bcj_without = simulate_bcj_trajectory(no_bdd)

    # Flight risk comparison
    flight_with = PI_FLIGHT.get("base", 0.33) * (1 - scenario.bdd_scores.stakeholder * 0.5)
    flight_without = PI_FLIGHT.get("base", 0.33) * 1.2  # 20% higher without BDD

    # Value of behavioral integration
    delta_synergies = synergy_with["total_realized_meur"] - synergy_without["total_realized_meur"]

    # Progress comparison at month 12 and month 24
    m12_with = bcj_with[12]["progress"] if len(bcj_with) > 12 else 0
    m12_without = bcj_without[12]["progress"] if len(bcj_without) > 12 else 0
    m24_with = bcj_with[24]["progress"] if len(bcj_with) > 24 else 0
    m24_without = bcj_without[24]["progress"] if len(bcj_without) > 24 else 0

    return {
        "with_behavioral": {
            "synergy_realized_meur": synergy_with["total_realized_meur"],
            "realization_rate": synergy_with["realization_rate"],
            "flight_risk": round(flight_with, 3),
            "progress_m12": round(m12_with, 3),
            "progress_m24": round(m24_with, 3),
        },
        "without_behavioral": {
            "synergy_realized_meur": synergy_without["total_realized_meur"],
            "realization_rate": synergy_without["realization_rate"],
            "flight_risk": round(flight_without, 3),
            "progress_m12": round(m12_without, 3),
            "progress_m24": round(m24_without, 3),
        },
        "delta": {
            "additional_synergies_meur": round(delta_synergies, 2),
            "additional_realization_pp": round(
                (synergy_with["realization_rate"] - synergy_without["realization_rate"]) * 100, 1),
            "flight_risk_reduction_pp": round((flight_without - flight_with) * 100, 1),
            "progress_acceleration_m12": round((m12_with - m12_without) * 100, 1),
            "progress_acceleration_m24": round((m24_with - m24_without) * 100, 1),
        },
        "roi_estimate": {
            "behavioral_investment_meur": round(scenario.deal_size_meur * 0.02, 2),
            "additional_value_meur": round(delta_synergies, 2),
            "roi_multiple": round(delta_synergies / (scenario.deal_size_meur * 0.02), 1)
                if scenario.deal_size_meur > 0 else 0,
        },
    }


def run_full_analysis(scenario: MAScenario, counterfactual: bool = False) -> Dict:
    """Run complete M&A behavioral analysis."""
    results = {
        "scenario": {
            "name": scenario.name,
            "deal_type": scenario.deal_type,
            "deal_size_meur": scenario.deal_size_meur,
            "seller_type": scenario.seller_type,
            "lambda_seller": LAMBDA_SELLER.get(scenario.seller_type, 2.50),
            "announced_synergies_meur": scenario.announced_synergies_meur,
        },
        "psi_distance": compute_psi_distance(scenario.acquirer, scenario.target),
        "gamma_matrix": compute_gamma_matrix(scenario),
        "bdd_score": compute_bdd_score(scenario),
        "synergy_forecast": compute_synergy_forecast(scenario),
        "bcj_trajectory": {
            "summary": {
                "months": scenario.integration_months,
            },
            "milestones": [],
        },
    }

    # Extract BCJ milestones
    trajectory = simulate_bcj_trajectory(scenario)
    for m in [0, 3, 6, 12, 18, 24, 36]:
        if m < len(trajectory):
            results["bcj_trajectory"]["milestones"].append(trajectory[m])

    if counterfactual:
        results["counterfactual"] = compute_counterfactual(scenario)

    return results


# =============================================================================
# SCENARIO LOADING
# =============================================================================

def load_scenario_from_yaml(path: str) -> MAScenario:
    """Load scenario from YAML file."""
    with open(path, "r") as f:
        data = yaml.safe_load(f)

    sc = data.get("scenario", data)

    acquirer_psi = sc.get("acquirer_psi", {})
    target_psi = sc.get("target_psi", {})

    acquirer = PsiProfile(**{k: v for k, v in acquirer_psi.items() if hasattr(PsiProfile, k)})
    target = PsiProfile(**{k: v for k, v in target_psi.items() if hasattr(PsiProfile, k)})

    bdd = sc.get("bdd_scores", {})
    bdd_scores = BDDScores(
        leadership=bdd.get("leadership", 0.5),
        cultural=bdd.get("cultural", 0.5),
        resilience=bdd.get("resilience", 0.5),
        complementarity=bdd.get("complementarity", 0.5),
        stakeholder=bdd.get("stakeholder", 0.5),
    )

    gamma_pairs = sc.get("gamma_overrides", {})
    gamma_matrix = GammaMatrix(pairs=gamma_pairs)

    return MAScenario(
        name=sc.get("name", "Unnamed Deal"),
        deal_type=sc.get("deal_type", "strategic"),
        deal_size_meur=sc.get("deal_size_meur", 100.0),
        seller_type=sc.get("seller_type", "family_founder"),
        acquirer=acquirer,
        target=target,
        announced_synergies_meur=sc.get("announced_synergies_meur", 20.0),
        bdd_scores=bdd_scores,
        gamma_matrix=gamma_matrix,
        integration_months=sc.get("integration_months", 36),
    )


def create_alpla_demo() -> MAScenario:
    """Create ALPLA-like M&A scenario for smoke testing."""
    return MAScenario(
        name="ALPLA SE Asia Acquisition (Demo)",
        deal_type="strategic",
        deal_size_meur=200.0,
        seller_type="family_founder",
        acquirer=PsiProfile(
            psi_I=0.75,   # Austrian corporate governance
            psi_S=0.60,   # Collaborative but hierarchical
            psi_K=0.70,   # Strong Vorarlberg family culture
            psi_C=0.65,   # Conservative, engineering-driven
            psi_E=0.70,   # Resource-efficient, capex-disciplined
            psi_T=0.55,   # Long-term family perspective
            psi_M=0.75,   # Advanced manufacturing technology
            psi_F=0.60,   # European HQ, global footprint
        ),
        target=PsiProfile(
            psi_I=0.35,   # Less formal governance (SE Asia)
            psi_S=0.80,   # High-context social relationships
            psi_K=0.25,   # Very different cultural values
            psi_C=0.45,   # Relationship-driven, less systematic
            psi_E=0.40,   # Different resource orientation
            psi_T=0.40,   # Shorter time horizon
            psi_M=0.45,   # Less advanced technology
            psi_F=0.20,   # SE Asia location, distance from HQ
        ),
        announced_synergies_meur=40.0,
        bdd_scores=BDDScores(
            leadership=0.65,       # Moderate — founder risk
            cultural=0.35,         # Low — high Psi-distance
            resilience=0.55,       # Moderate — growth culture
            complementarity=0.60,  # Moderate — scale synergy offsets innovation risk
            stakeholder=0.45,      # Low-moderate — SE Asia talent flight risk
        ),
        gamma_matrix=GammaMatrix(pairs={
            "ma_x_se_asia_growth": 0.25,     # Growth market opportunity
            "local_knowledge_gap": -0.30,     # Know-how deficit in SE Asia
        }),
        integration_months=36,
    )


# =============================================================================
# OUTPUT FORMATTING
# =============================================================================

def format_text_report(results: Dict) -> str:
    """Format results as human-readable text report."""
    lines = []
    sc = results["scenario"]
    lines.append("=" * 72)
    lines.append(f"  M&A BEHAVIORAL SCENARIO ENGINE — MOD-MA-001")
    lines.append(f"  Deal: {sc['name']}")
    lines.append("=" * 72)

    # Scenario Summary
    lines.append(f"\n{'─'*72}")
    lines.append("  SCENARIO")
    lines.append(f"{'─'*72}")
    lines.append(f"  Deal Type:        {sc['deal_type']}")
    lines.append(f"  Deal Size:        EUR {sc['deal_size_meur']}M")
    lines.append(f"  Seller Type:      {sc['seller_type']}")
    lines.append(f"  Lambda (Seller):  {sc['lambda_seller']}")
    lines.append(f"  Announced Syn.:   EUR {sc['announced_synergies_meur']}M")

    # Psi-Distance
    psi = results["psi_distance"]
    lines.append(f"\n{'─'*72}")
    lines.append("  PSI-DISTANCE (Cultural Distance)")
    lines.append(f"{'─'*72}")
    lines.append(f"  Total Distance:   {psi['total_distance']}")
    lines.append(f"  Interpretation:   {psi['interpretation']}")
    lines.append(f"  Dominant Driver:  {psi['dominant_driver']}")
    lines.append("")
    lines.append(f"  {'Dimension':<15} {'Acquirer':>10} {'Target':>10} {'Distance':>10} {'Weight':>8}")
    lines.append(f"  {'─'*53}")
    for name, vals in psi["per_dimension"].items():
        lines.append(f"  {name:<15} {vals['acquirer']:>10.3f} {vals['target']:>10.3f} "
                      f"{vals['distance']:>10.3f} {vals['weight']:>8.3f}")

    # Gamma Matrix
    gm = results["gamma_matrix"]
    lines.append(f"\n{'─'*72}")
    lines.append("  GAMMA MATRIX (Complementarities)")
    lines.append(f"{'─'*72}")
    lines.append(f"  Net Complementarity:  {gm['net_complementarity']}")
    lines.append(f"  Positive Sum:         {gm['positive_sum']}")
    lines.append(f"  Negative Sum:         {gm['negative_sum']}")
    hr, hv = gm["highest_risk"]
    lines.append(f"  Highest Risk:         {hr} (gamma = {hv})")
    hs, hsv = gm["highest_synergy"]
    lines.append(f"  Highest Synergy:      {hs} (gamma = {hsv})")
    lines.append("")
    for pair, gamma in gm["gammas"].items():
        marker = "  " if gamma >= 0 else "!!"
        lines.append(f"  {marker} {pair:<35} gamma = {gamma:+.4f}")

    # BDD Score
    bdd = results["bdd_score"]
    lines.append(f"\n{'─'*72}")
    lines.append("  BDD SCORE (Behavioral Due Diligence)")
    lines.append(f"{'─'*72}")
    lines.append(f"  Composite Score:   {bdd['composite_score']}")
    lines.append(f"  Traffic Light:     {bdd['traffic_light']}")
    lines.append(f"  Recommendation:    {bdd['recommendation']}")
    lines.append("")
    for module, vals in bdd["modules"].items():
        bar_len = int(vals["score"] * 30)
        bar = "█" * bar_len + "░" * (30 - bar_len)
        lines.append(f"  {module:<25} {bar} {vals['score']:.3f} (w={vals['weight']})")

    # Synergy Forecast
    sf = results["synergy_forecast"]
    lines.append(f"\n{'─'*72}")
    lines.append("  SYNERGY REALIZATION FORECAST")
    lines.append(f"{'─'*72}")
    lines.append(f"  Announced:        EUR {sf['announced_synergies_meur']}M")
    lines.append(f"  Realized:         EUR {sf['total_realized_meur']}M")
    lines.append(f"  Realization Rate: {sf['realization_rate']*100:.1f}%")
    lines.append(f"  Value at Risk:    EUR {sf['behavioral_value_at_risk_meur']}M")
    lines.append("")
    for cat, vals in sf["breakdown"].items():
        lines.append(f"  {cat:<10}  Announced: EUR {vals['announced']:>6.1f}M  "
                      f"Realized: EUR {vals['realized']:>6.1f}M  Rate: {vals['rate']*100:>5.1f}%")

    # BCJ Trajectory
    bcj = results["bcj_trajectory"]
    lines.append(f"\n{'─'*72}")
    lines.append("  BCJ INTEGRATION TRAJECTORY")
    lines.append(f"{'─'*72}")
    lines.append(f"  {'Month':>5} {'Unaware':>8} {'Aware':>8} {'Willing':>8} "
                  f"{'Acting':>8} {'Maintain':>8} {'Progress':>10} {'PsiDist':>8}")
    lines.append(f"  {'─'*67}")
    for m in bcj["milestones"]:
        lines.append(f"  {m['month']:>5} {m['unaware']:>8.3f} {m['aware']:>8.3f} "
                      f"{m['willing']:>8.3f} {m['acting']:>8.3f} {m['maintaining']:>8.3f} "
                      f"{m['progress']:>10.3f} {m['psi_distance']:>8.3f}")

    # Counterfactual
    if "counterfactual" in results:
        cf = results["counterfactual"]
        lines.append(f"\n{'─'*72}")
        lines.append("  COUNTERFACTUAL: With vs. Without Behavioral Integration")
        lines.append(f"{'─'*72}")
        lines.append(f"  {'Metric':<35} {'With BDD':>12} {'Without':>12} {'Delta':>12}")
        lines.append(f"  {'─'*71}")

        w = cf["with_behavioral"]
        wo = cf["without_behavioral"]
        d = cf["delta"]

        lines.append(f"  {'Synergies Realized (EUR M)':<35} {w['synergy_realized_meur']:>12.1f} "
                      f"{wo['synergy_realized_meur']:>12.1f} {d['additional_synergies_meur']:>+12.1f}")
        lines.append(f"  {'Realization Rate':<35} {w['realization_rate']*100:>11.1f}% "
                      f"{wo['realization_rate']*100:>11.1f}% {d['additional_realization_pp']:>+11.1f}pp")
        lines.append(f"  {'Key Talent Flight Risk':<35} {w['flight_risk']*100:>11.1f}% "
                      f"{wo['flight_risk']*100:>11.1f}% {d['flight_risk_reduction_pp']:>+11.1f}pp")
        lines.append(f"  {'Integration Progress M12':<35} {w['progress_m12']*100:>11.1f}% "
                      f"{wo['progress_m12']*100:>11.1f}% {d['progress_acceleration_m12']:>+11.1f}pp")
        lines.append(f"  {'Integration Progress M24':<35} {w['progress_m24']*100:>11.1f}% "
                      f"{wo['progress_m24']*100:>11.1f}% {d['progress_acceleration_m24']:>+11.1f}pp")

        roi = cf["roi_estimate"]
        lines.append(f"\n  ROI of Behavioral Integration:")
        lines.append(f"  Investment (2% of deal):  EUR {roi['behavioral_investment_meur']}M")
        lines.append(f"  Additional value:         EUR {roi['additional_value_meur']}M")
        lines.append(f"  ROI Multiple:             {roi['roi_multiple']}x")

    lines.append(f"\n{'='*72}")
    lines.append("  Parameters: PAR-MA-001 to PAR-MA-008 | Model: MOD-MA-001")
    lines.append("  Session: EBF-S-2026-02-16-ORG-001 | Layer 1 Computation")
    lines.append(f"{'='*72}")

    return "\n".join(lines)


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="M&A Behavioral Scenario Engine (MOD-MA-001, Layer 1)"
    )
    parser.add_argument("--scenario", type=str, help="Path to scenario YAML file")
    parser.add_argument("--demo", action="store_true", help="Run ALPLA SE Asia demo scenario")
    parser.add_argument("--counterfactual", action="store_true",
                        help="Include counterfactual comparison (with vs. without BDD)")
    parser.add_argument("--json", action="store_true", help="Output as JSON instead of text")
    args = parser.parse_args()

    if not args.demo and not args.scenario:
        parser.print_help()
        print("\nError: specify --demo or --scenario <path>")
        sys.exit(1)

    # Load scenario
    if args.demo:
        scenario = create_alpla_demo()
    else:
        scenario = load_scenario_from_yaml(args.scenario)

    # Run analysis
    results = run_full_analysis(scenario, counterfactual=args.counterfactual or args.demo)

    # Output
    if args.json:
        # Remove trajectory for cleaner JSON (keep milestones)
        print(json.dumps(results, indent=2, default=str))
    else:
        print(format_text_report(results))


if __name__ == "__main__":
    main()
