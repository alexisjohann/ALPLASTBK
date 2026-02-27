#!/usr/bin/env python3
"""
Monte Carlo Simulation: UBS Feel Switzerland Communication Effectiveness Model
================================================================================

Simulates conversion probability, fairness perception, attention decay,
and discount optimization across 4 personas x 4 regions with 10,000 draws.

Models:
  - Conversion: Logistic model with default, reciprocity, friction, social proof
  - Fairness: Fehr-Schmidt inequity aversion with framing modifiers
  - Attention: Exponential decay for optimal benefit count N*
  - Discount: Prospect Theory value function with quality/brand signals

Author: EBF Framework / FehrAdvice & Partners AG
Date: 2026-02-13
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Tuple
import sys

# ============================================================================
# Configuration
# ============================================================================

N_DRAWS = 10_000
SEED = 42
CI_LEVEL = 0.95

# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class Persona:
    name: str
    age: int
    # Multipliers on base parameters (1.0 = no adjustment)
    adj_default: float = 1.0
    adj_reciprocity: float = 1.0
    adj_friction_inv: float = 1.0
    adj_social_proof: float = 1.0
    social_proof_offset: float = 0.0  # additive offset (for Thomas reactance)
    eta_mult: float = 1.0  # attention decay persona modifier
    description: str = ""

@dataclass
class Region:
    name: str
    code: str
    R_default: float = 1.0
    R_financial: float = 1.0
    R_social: float = 1.0

# ============================================================================
# Define Personas
# ============================================================================

PERSONAS = [
    Persona(
        name="Lena", age=22,
        adj_default=0.9, adj_social_proof=1.3,
        eta_mult=0.85,  # digital native, slightly less decay
        description="Digital native, social-proof responsive"
    ),
    Persona(
        name="Marco", age=24,
        # balanced, no adjustments
        eta_mult=0.95,
        description="Balanced young professional"
    ),
    Persona(
        name="Sandra", age=42,
        adj_reciprocity=1.4, adj_default=1.1,
        eta_mult=1.05,
        description="Reciprocity-driven, default-compliant"
    ),
    Persona(
        name="Thomas", age=58,
        adj_default=0.7, adj_friction_inv=0.6,
        adj_social_proof=-0.3,  # used as multiplier replacement
        social_proof_offset=-0.3,  # reactance: social proof becomes negative
        eta_mult=1.20,  # faster attention decay
        description="Low trust, friction-sensitive, reactance to social proof"
    ),
]

REGIONS = [
    Region("Deutschschweiz", "DE-CH", R_default=1.15, R_financial=1.25, R_social=1.00),
    Region("Romandie",       "FR-CH", R_default=0.95, R_financial=1.00, R_social=1.15),
    Region("Ticino",         "TI",    R_default=1.05, R_financial=0.90, R_social=1.25),
    Region("Graubuenden",    "GR",    R_default=1.10, R_financial=1.10, R_social=0.90),
]

FRAMING_MODIFIERS = {
    "exclusive":     0.85,
    "earned":        0.70,
    "transparent":   0.75,
    "premium_only":  1.40,
}

DISCOUNT_LEVELS = [0.20, 0.40, 0.60, 0.80]
QUALITY_SIGNALS = {0.20: 1.00, 0.40: 0.90, 0.60: 0.75, 0.80: 0.55}
BRAND_FIT      = {0.20: 1.00, 0.40: 0.95, 0.60: 0.80, 0.80: 0.50}


# ============================================================================
# Simulation Engine
# ============================================================================

def sigmoid(x: np.ndarray) -> np.ndarray:
    """Numerically stable sigmoid."""
    return np.where(x >= 0, 1 / (1 + np.exp(-x)), np.exp(x) / (1 + np.exp(x)))


def draw_base_parameters(rng: np.random.Generator, n: int) -> Dict[str, np.ndarray]:
    """Draw base conversion model parameters from prior distributions."""
    return {
        "alpha_0": rng.normal(-2.30, 0.30, n),   # intercept
        "alpha_1": rng.normal(1.95, 0.25, n),     # default effect
        "alpha_2": rng.normal(0.55, 0.15, n),     # reciprocity
        "alpha_3": rng.normal(0.90, 0.20, n),     # friction_inv
        "alpha_4": rng.normal(0.50, 0.12, n),     # social proof
        "alpha_FS": rng.normal(0.85, 0.10, n),    # Fehr-Schmidt alpha (disadvantageous)
        "beta_FS": rng.normal(0.40, 0.08, n),     # Fehr-Schmidt beta (advantageous)
        "eta": rng.normal(0.20, 0.04, n),         # attention decay
        "alpha_PT": rng.normal(0.88, 0.05, n),    # prospect theory curvature
    }


def apply_persona_adjustments(
    params: Dict[str, np.ndarray], persona: Persona
) -> Dict[str, np.ndarray]:
    """Apply persona-specific parameter adjustments."""
    p = {k: v.copy() for k, v in params.items()}

    p["alpha_1"] *= persona.adj_default
    p["alpha_2"] *= persona.adj_reciprocity
    p["alpha_3"] *= persona.adj_friction_inv

    # Thomas special case: social proof becomes negative (reactance)
    if persona.social_proof_offset != 0.0:
        # Replace: alpha_4 * adj becomes alpha_4 * adj + offset
        # For Thomas: adj_social_proof = -0.3 means we use offset
        p["alpha_4"] = p["alpha_4"] * abs(persona.adj_social_proof) + persona.social_proof_offset
    else:
        p["alpha_4"] *= persona.adj_social_proof

    p["eta"] *= persona.eta_mult

    return p


def apply_region_multipliers(
    params: Dict[str, np.ndarray], region: Region
) -> Dict[str, np.ndarray]:
    """Apply regional multipliers to relevant parameters."""
    p = {k: v.copy() for k, v in params.items()}
    p["alpha_1"] *= region.R_default
    p["alpha_2"] *= region.R_financial  # reciprocity ~ financial incentive sensitivity
    p["alpha_4"] *= region.R_social
    return p


def compute_conversion_ist(params: Dict[str, np.ndarray]) -> np.ndarray:
    """IST scenario: opt-in, no nudge, no social proof, standard friction."""
    logit = params["alpha_0"]  # only intercept, no nudge effects
    return sigmoid(logit)


def compute_conversion_soll(params: Dict[str, np.ndarray]) -> np.ndarray:
    """SOLL scenario: opt-out default + reciprocity nudge + reduced friction + social proof."""
    logit = (
        params["alpha_0"]
        + params["alpha_1"]  # default (opt-out)
        + params["alpha_2"]  # reciprocity nudge
        + params["alpha_3"]  # friction reduction
        + params["alpha_4"]  # social proof
    )
    return sigmoid(logit)


def compute_fairness(
    params: Dict[str, np.ndarray], framing: str, modifier: float
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Fehr-Schmidt fairness utility.

    U_Fairness = 1 - alpha_FS * max(perceived_inequity, 0)
                   - beta_FS * max(-perceived_inequity, 0)

    Framing reduces perceived inequity.
    Base perceived inequity: benefit_ratio - fair_share = 0.3 (arbitrary reference)
    """
    base_inequity = 0.30  # perceived inequity without framing
    perceived = base_inequity * modifier  # framing reduces perception

    alpha_fs = params["alpha_FS"]
    beta_fs = params["beta_FS"]

    # Disadvantageous inequity (others get more)
    u_fair = 1.0 - alpha_fs * np.maximum(perceived, 0) - beta_fs * np.maximum(-perceived, 0)
    u_fair = np.clip(u_fair, 0, 1)

    # Fairness violation = U_Fairness < 0.5 threshold
    violation = (u_fair < 0.50).astype(float)

    return u_fair, violation


def compute_optimal_n(params: Dict[str, np.ndarray]) -> np.ndarray:
    """
    Attention decay model: A(N) = exp(-eta * N)
    Marginal value of Nth benefit: V_N ~ exp(-eta * (N-1))
    Optimal N*: where marginal attention > threshold (0.3)

    N* = floor(-ln(threshold) / eta)
    """
    eta = np.clip(params["eta"], 0.01, None)  # avoid division by zero
    threshold = 0.30
    n_star = np.floor(-np.log(threshold) / eta)
    n_star = np.clip(n_star, 1, 20)  # reasonable bounds
    return n_star


def compute_discount_value(
    params: Dict[str, np.ndarray], discount_pct: float
) -> np.ndarray:
    """
    Prospect Theory value function for discount perception.

    V(d) = d^alpha_PT * quality_signal(d) * brand_fit(d)

    Returns perceived value (higher = better).
    """
    alpha_pt = np.clip(params["alpha_PT"], 0.1, 1.0)
    v = np.power(discount_pct, alpha_pt)
    q = QUALITY_SIGNALS[discount_pct]
    b = BRAND_FIT[discount_pct]
    return v * q * b


def ci_95(arr: np.ndarray) -> Tuple[float, float, float]:
    """Return (mean, lower_2.5%, upper_97.5%)."""
    m = np.mean(arr)
    lo = np.percentile(arr, 2.5)
    hi = np.percentile(arr, 97.5)
    return m, lo, hi


# ============================================================================
# Output Formatting
# ============================================================================

def print_separator(char="=", width=90):
    print(char * width)

def print_header(title: str, width=90):
    print()
    print_separator("=", width)
    print(f"  {title}")
    print_separator("=", width)


def format_pct(val: float) -> str:
    return f"{val*100:.1f}%"

def format_ci(mean: float, lo: float, hi: float, pct=True) -> str:
    if pct:
        return f"{mean*100:5.1f}%  [{lo*100:5.1f}%, {hi*100:5.1f}%]"
    else:
        return f"{mean:6.2f}  [{lo:6.2f}, {hi:6.2f}]"


# ============================================================================
# Main Simulation
# ============================================================================

def main():
    rng = np.random.default_rng(SEED)
    base_params = draw_base_parameters(rng, N_DRAWS)

    # Storage for results
    results_conversion = {}      # (persona, region) -> (ist_ci, soll_ci, lift_ci)
    results_conversion_agg = {}  # persona -> aggregated across regions
    results_n_star = {}          # persona -> ci
    results_discount = {}        # persona -> {discount_pct: value_ci}
    results_fairness = {}        # framing -> (u_fair_ci, violation_prob_ci)
    results_region_matrix = {}   # (persona, region) -> soll conversion

    # ------------------------------------------------------------------
    # 1. CONVERSION MODEL: Per-persona (aggregated) and per-persona x region
    # ------------------------------------------------------------------
    print_header("UBS FEEL SWITZERLAND - MONTE CARLO SIMULATION")
    print(f"  Draws: {N_DRAWS:,}")
    print(f"  Seed:  {SEED}")
    print(f"  CI:    {CI_LEVEL*100:.0f}%")
    print()

    for persona in PERSONAS:
        p_params = apply_persona_adjustments(base_params, persona)

        # Aggregated (no region)
        ist = compute_conversion_ist(p_params)
        soll = compute_conversion_soll(p_params)
        lift = soll - ist

        results_conversion_agg[persona.name] = {
            "ist": ci_95(ist),
            "soll": ci_95(soll),
            "lift": ci_95(lift),
        }

        # Per region
        for region in REGIONS:
            rp = apply_region_multipliers(p_params, region)
            ist_r = compute_conversion_ist(rp)
            soll_r = compute_conversion_soll(rp)
            lift_r = soll_r - ist_r

            results_conversion[(persona.name, region.code)] = {
                "ist": ci_95(ist_r),
                "soll": ci_95(soll_r),
                "lift": ci_95(lift_r),
            }
            results_region_matrix[(persona.name, region.code)] = ci_95(soll_r)

    # ------------------------------------------------------------------
    # 2. OPTIMAL N* (attention decay)
    # ------------------------------------------------------------------
    for persona in PERSONAS:
        p_params = apply_persona_adjustments(base_params, persona)
        n_star = compute_optimal_n(p_params)
        results_n_star[persona.name] = ci_95(n_star)

    # ------------------------------------------------------------------
    # 3. DISCOUNT OPTIMIZATION
    # ------------------------------------------------------------------
    for persona in PERSONAS:
        p_params = apply_persona_adjustments(base_params, persona)
        results_discount[persona.name] = {}
        for d in DISCOUNT_LEVELS:
            v = compute_discount_value(p_params, d)
            results_discount[persona.name][d] = ci_95(v)

    # ------------------------------------------------------------------
    # 4. FAIRNESS MODEL (across all personas pooled)
    # ------------------------------------------------------------------
    for framing, modifier in FRAMING_MODIFIERS.items():
        all_u_fair = []
        all_violation = []
        for persona in PERSONAS:
            p_params = apply_persona_adjustments(base_params, persona)
            u_fair, violation = compute_fairness(p_params, framing, modifier)
            all_u_fair.append(u_fair)
            all_violation.append(violation)
        pooled_u = np.concatenate(all_u_fair)
        pooled_v = np.concatenate(all_violation)
        results_fairness[framing] = {
            "u_fair": ci_95(pooled_u),
            "violation_prob": ci_95(pooled_v),
        }

    # ------------------------------------------------------------------
    # 5. OVERALL PROGRAM EFFECTIVENESS
    # ------------------------------------------------------------------
    # Weighted average conversion uplift (equal persona weights, population-weighted regions)
    region_weights = {"DE-CH": 0.63, "FR-CH": 0.23, "TI": 0.08, "GR": 0.06}
    overall_lifts = []
    for persona in PERSONAS:
        persona_lift = 0.0
        for region in REGIONS:
            w = region_weights[region.code]
            lift_mean = results_conversion[(persona.name, region.code)]["lift"][0]
            persona_lift += w * lift_mean
        overall_lifts.append(persona_lift)
    overall_mean_lift = np.mean(overall_lifts)

    # Full MC for overall
    all_soll_draws = []
    all_ist_draws = []
    for persona in PERSONAS:
        p_params = apply_persona_adjustments(base_params, persona)
        for region in REGIONS:
            w = region_weights[region.code]
            rp = apply_region_multipliers(p_params, region)
            ist_r = compute_conversion_ist(rp)
            soll_r = compute_conversion_soll(rp)
            all_ist_draws.append(ist_r * w / len(PERSONAS))
            all_soll_draws.append(soll_r * w / len(PERSONAS))

    overall_ist = np.sum(all_ist_draws, axis=0)
    overall_soll = np.sum(all_soll_draws, axis=0)
    overall_lift_mc = overall_soll - overall_ist

    # ====================================================================
    # OUTPUT
    # ====================================================================

    # --- Table 1: Conversion Rates per Persona (aggregated) ---
    print_header("TABLE 1: CONVERSION RATES PER PERSONA (Aggregated)")
    print(f"  {'Persona':<12} {'Age':>4}  {'IST (Opt-In)':>28}  {'SOLL (Opt-Out+Nudge)':>28}  {'Lift':>28}")
    print_separator("-")
    for persona in PERSONAS:
        r = results_conversion_agg[persona.name]
        ist_str = format_ci(*r["ist"])
        soll_str = format_ci(*r["soll"])
        lift_str = format_ci(*r["lift"])
        print(f"  {persona.name:<12} {persona.age:>4}  {ist_str:>28}  {soll_str:>28}  {lift_str:>28}")
    print()

    # --- Table 2: Persona x Region Matrix (SOLL conversion) ---
    print_header("TABLE 2: PERSONA x REGION MATRIX - SOLL Conversion P(Convert)")
    header = f"  {'Persona':<12}"
    for region in REGIONS:
        header += f"  {region.code:>20}"
    print(header)
    print_separator("-")
    for persona in PERSONAS:
        row = f"  {persona.name:<12}"
        for region in REGIONS:
            m, lo, hi = results_region_matrix[(persona.name, region.code)]
            row += f"  {m*100:5.1f}% [{lo*100:4.1f}-{hi*100:4.1f}]"
        print(row)
    print()

    # --- Table 2b: Persona x Region Lift ---
    print_header("TABLE 2b: PERSONA x REGION MATRIX - Conversion Lift (SOLL - IST)")
    header = f"  {'Persona':<12}"
    for region in REGIONS:
        header += f"  {region.code:>20}"
    print(header)
    print_separator("-")
    for persona in PERSONAS:
        row = f"  {persona.name:<12}"
        for region in REGIONS:
            m, lo, hi = results_conversion[(persona.name, region.code)]["lift"]
            row += f"  {m*100:5.1f}pp [{lo*100:4.1f}-{hi*100:4.1f}]"
        print(row)
    print()

    # --- Table 3: Optimal N* per Persona ---
    print_header("TABLE 3: OPTIMAL NUMBER OF BENEFITS N* PER PERSONA")
    print(f"  {'Persona':<12} {'Age':>4}  {'N* (Mean)':>10}  {'95% CI':>18}  {'Description'}")
    print_separator("-")
    for persona in PERSONAS:
        m, lo, hi = results_n_star[persona.name]
        print(f"  {persona.name:<12} {persona.age:>4}  {m:>10.1f}  [{lo:>6.1f}, {hi:>6.1f}]   {persona.description}")
    print()

    # --- Table 4: Optimal Discount Depth ---
    print_header("TABLE 4: PERCEIVED DISCOUNT VALUE BY DEPTH (Prospect Theory)")
    print(f"  {'Persona':<12}", end="")
    for d in DISCOUNT_LEVELS:
        print(f"  {d*100:.0f}% discount{'':<8}", end="")
    print("  Optimal")
    print_separator("-")
    for persona in PERSONAS:
        row = f"  {persona.name:<12}"
        best_d = None
        best_v = -1
        for d in DISCOUNT_LEVELS:
            m, lo, hi = results_discount[persona.name][d]
            row += f"  {m:.3f} [{lo:.2f}-{hi:.2f}]"
            if m > best_v:
                best_v = m
                best_d = d
        row += f"    {best_d*100:.0f}%"
        print(row)
    print()
    print("  Note: Value = d^alpha_PT * quality_signal(d) * brand_fit(d)")
    print("  Higher value = better perceived deal accounting for quality/brand concerns")
    print()

    # --- Table 5: Fairness Violation Probability by Framing ---
    print_header("TABLE 5: FAIRNESS PERCEPTION BY FRAMING STRATEGY (Fehr-Schmidt)")
    print(f"  {'Framing':<16} {'Modifier':>8}  {'U_Fairness':>28}  {'P(Violation)':>28}")
    print_separator("-")
    for framing, modifier in FRAMING_MODIFIERS.items():
        r = results_fairness[framing]
        u_str = format_ci(*r["u_fair"])
        v_str = format_ci(*r["violation_prob"])
        print(f"  {framing:<16} {modifier:>8.2f}  {u_str:>28}  {v_str:>28}")
    print()
    print("  Violation threshold: U_Fairness < 0.50")
    print("  Lower modifier = more effective framing at reducing perceived inequity")
    print()

    # --- Table 5b: Fairness by Persona x Framing ---
    print_header("TABLE 5b: FAIRNESS VIOLATION P(U<0.5) BY PERSONA x FRAMING")
    header = f"  {'Persona':<12}"
    for framing in FRAMING_MODIFIERS:
        header += f"  {framing:>14}"
    print(header)
    print_separator("-")
    for persona in PERSONAS:
        p_params = apply_persona_adjustments(base_params, persona)
        row = f"  {persona.name:<12}"
        for framing, modifier in FRAMING_MODIFIERS.items():
            u_fair, violation = compute_fairness(p_params, framing, modifier)
            v_mean = np.mean(violation)
            row += f"  {v_mean*100:>12.1f}%"
        print(row)
    print()

    # --- Table 6: Overall Program Effectiveness ---
    print_header("TABLE 6: OVERALL PROGRAM EFFECTIVENESS ESTIMATE")
    print()
    print(f"  Region weights: DE-CH={region_weights['DE-CH']:.0%}, "
          f"FR-CH={region_weights['FR-CH']:.0%}, "
          f"TI={region_weights['TI']:.0%}, "
          f"GR={region_weights['GR']:.0%}")
    print()

    ist_ci = ci_95(overall_ist)
    soll_ci = ci_95(overall_soll)
    lift_ci = ci_95(overall_lift_mc)
    rel_lift = ci_95(overall_lift_mc / np.clip(overall_ist, 0.001, None))

    print(f"  {'Metric':<35} {'Mean':>8}  {'95% CI':>22}")
    print_separator("-", 70)
    print(f"  {'IST Conversion (weighted avg)':<35} {format_pct(ist_ci[0]):>8}  [{format_pct(ist_ci[1]):>6}, {format_pct(ist_ci[2]):>6}]")
    print(f"  {'SOLL Conversion (weighted avg)':<35} {format_pct(soll_ci[0]):>8}  [{format_pct(soll_ci[1]):>6}, {format_pct(soll_ci[2]):>6}]")
    print(f"  {'Absolute Lift (pp)':<35} {lift_ci[0]*100:>7.1f}pp  [{lift_ci[1]*100:>5.1f}pp, {lift_ci[2]*100:>5.1f}pp]")
    print(f"  {'Relative Lift':<35} {rel_lift[0]*100:>7.0f}%   [{rel_lift[1]*100:>5.0f}%, {rel_lift[2]*100:>5.0f}%]")
    print()

    # Best framing
    best_framing = min(results_fairness, key=lambda f: results_fairness[f]["violation_prob"][0])
    best_viol = results_fairness[best_framing]["violation_prob"][0]

    # Best discount (averaged across personas)
    discount_avg = {}
    for d in DISCOUNT_LEVELS:
        vals = [results_discount[p.name][d][0] for p in PERSONAS]
        discount_avg[d] = np.mean(vals)
    best_discount = max(discount_avg, key=discount_avg.get)

    # Average N*
    avg_n = np.mean([results_n_star[p.name][0] for p in PERSONAS])

    print_header("SUMMARY: KEY RECOMMENDATIONS")
    print()
    print(f"  1. DEFAULT ARCHITECTURE")
    print(f"     Switch from Opt-In to Opt-Out + Nudge Bundle")
    print(f"     Expected lift: {lift_ci[0]*100:.1f}pp [{lift_ci[1]*100:.1f}-{lift_ci[2]*100:.1f}pp]")
    print(f"     Relative improvement: ~{rel_lift[0]*100:.0f}%")
    print()
    print(f"  2. OPTIMAL FRAMING")
    print(f"     Best framing strategy: '{best_framing}'")
    print(f"     Fairness violation probability: {best_viol*100:.1f}%")
    print(f"     Recommendation: Frame benefits as 'earned' through loyalty")
    print()
    print(f"  3. OPTIMAL BENEFIT COUNT")
    print(f"     Average optimal N*: {avg_n:.1f} benefits")
    for persona in PERSONAS:
        m, lo, hi = results_n_star[persona.name]
        print(f"       {persona.name:<10}: N* = {m:.0f} [{lo:.0f}-{hi:.0f}]")
    print()
    print(f"  4. OPTIMAL DISCOUNT DEPTH")
    print(f"     Best perceived-value discount: {best_discount*100:.0f}%")
    print(f"     (Balances value perception with quality signal and brand fit)")
    for d in DISCOUNT_LEVELS:
        marker = " <-- optimal" if d == best_discount else ""
        print(f"       {d*100:3.0f}%: avg value = {discount_avg[d]:.3f}{marker}")
    print()
    print(f"  5. REGIONAL PRIORITIES")
    # Find best and worst region per persona
    for persona in PERSONAS:
        lifts = {}
        for region in REGIONS:
            lifts[region.code] = results_conversion[(persona.name, region.code)]["lift"][0]
        best_r = max(lifts, key=lifts.get)
        worst_r = min(lifts, key=lifts.get)
        print(f"       {persona.name:<10}: Best = {best_r} ({lifts[best_r]*100:+.1f}pp), "
              f"Weakest = {worst_r} ({lifts[worst_r]*100:+.1f}pp)")
    print()

    # --- Technical Details ---
    print_header("TECHNICAL DETAILS")
    print()
    print("  Parameter Distributions (Priors):")
    print("  ------------------------------------")
    print("  alpha_0 (intercept)   ~ N(-2.30, 0.30)")
    print("  alpha_1 (default)     ~ N( 1.95, 0.25)")
    print("  alpha_2 (reciprocity) ~ N( 0.55, 0.15)")
    print("  alpha_3 (friction)    ~ N( 0.90, 0.20)")
    print("  alpha_4 (social)      ~ N( 0.50, 0.12)")
    print("  alpha_FS              ~ N( 0.85, 0.10)")
    print("  beta_FS               ~ N( 0.40, 0.08)")
    print("  eta (decay)           ~ N( 0.20, 0.04)")
    print("  alpha_PT              ~ N( 0.88, 0.05)")
    print()
    print("  Conversion Model: P = sigmoid(alpha_0 + alpha_1*D + alpha_2*R + alpha_3*F + alpha_4*S)")
    print("  Fairness Model:   U = 1 - alpha_FS * max(inequity*modifier, 0) - beta_FS * max(-inequity*modifier, 0)")
    print("  Attention Model:  N* = floor(-ln(0.3) / eta)")
    print("  Discount Model:   V(d) = d^alpha_PT * quality(d) * brand(d)")
    print()
    print_separator("=")
    print("  Simulation complete.")
    print_separator("=")


if __name__ == "__main__":
    main()
