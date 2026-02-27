#!/usr/bin/env python3
"""
Monte Carlo Simulation for MOD-UBS-AIMARK-001
UBS AI Marketing Transformation Model

Session: EBF-S-2026-02-12-FIN-001
Draws: 10,000
Output: 95% CIs for all key parameters, trigger crossing probabilities,
        sensitivity analysis, segment-level expected values

Usage:
    python scripts/monte_carlo_ubs_aimark.py
    python scripts/monte_carlo_ubs_aimark.py --draws 50000
    python scripts/monte_carlo_ubs_aimark.py --output yaml
"""

import argparse
import json
import sys
from datetime import datetime

import numpy as np

np.random.seed(2026)

# =============================================================================
# CONFIGURATION
# =============================================================================

N_DRAWS = 10_000

# =============================================================================
# 1. SCENARIO PROBABILITY DISTRIBUTIONS
# =============================================================================
# Dirichlet distribution ensures P(S1)+P(S2)+P(S3) = 1
# Alpha parameters calibrated to match point estimates and CIs
SCENARIO_ALPHA = {
    "S1_bigtech": 4.0,      # mean ~0.20
    "S2_hybrid": 10.0,      # mean ~0.50
    "S3_trust": 6.0,        # mean ~0.30
}

# =============================================================================
# 2. SEGMENT BEHAVIORAL PARAMETERS (mean, std)
# =============================================================================
SEGMENTS = {
    "SEG-LEGACY": {
        "size": 1_500_000,
        "tau_trust":       {"mean": 0.85, "std": 0.05, "dist": "beta"},
        "lambda_la":       {"mean": 1.80, "std": 0.20, "dist": "lognormal"},
        "beta_pb":         {"mean": 0.88, "std": 0.04, "dist": "beta"},
        "ai_adoption":     {"mean": 0.25, "std": 0.08, "dist": "beta"},
        "switching_cost":  {"mean": 0.75, "std": 0.08, "dist": "beta"},
        "fear_of_asking":  {"mean": 0.30, "std": 0.10, "dist": "beta"},
    },
    "SEG-CS-MIGRATED": {
        "size": 1_000_000,
        "tau_trust":       {"mean": 0.55, "std": 0.10, "dist": "beta"},
        "lambda_la":       {"mean": 2.20, "std": 0.30, "dist": "lognormal"},
        "beta_pb":         {"mean": 0.82, "std": 0.06, "dist": "beta"},
        "ai_adoption":     {"mean": 0.20, "std": 0.08, "dist": "beta"},
        "switching_cost":  {"mean": 0.35, "std": 0.10, "dist": "beta"},
        "fear_of_asking":  {"mean": 0.45, "std": 0.12, "dist": "beta"},
    },
    "SEG-DIGITAL": {
        "size": 800_000,
        "tau_trust":       {"mean": 0.70, "std": 0.08, "dist": "beta"},
        "lambda_la":       {"mean": 1.60, "std": 0.20, "dist": "lognormal"},
        "beta_pb":         {"mean": 0.78, "std": 0.06, "dist": "beta"},
        "ai_adoption":     {"mean": 0.55, "std": 0.10, "dist": "beta"},
        "switching_cost":  {"mean": 0.25, "std": 0.08, "dist": "beta"},
        "fear_of_asking":  {"mean": 0.15, "std": 0.06, "dist": "beta"},
    },
    "SEG-UHNW": {
        "size": 400_000,
        "tau_trust":       {"mean": 0.80, "std": 0.06, "dist": "beta"},
        "lambda_la":       {"mean": 2.10, "std": 0.25, "dist": "lognormal"},
        "beta_pb":         {"mean": 0.92, "std": 0.03, "dist": "beta"},
        "ai_adoption":     {"mean": 0.15, "std": 0.06, "dist": "beta"},
        "switching_cost":  {"mean": 0.80, "std": 0.06, "dist": "beta"},
        "fear_of_asking":  {"mean": 0.20, "std": 0.08, "dist": "beta"},
    },
}

# =============================================================================
# 3. MARKETING FUNCTION PARAMETERS (mean, std)
# =============================================================================
FUNCTIONS = {
    "F1_content":       {"ai_pot": (0.85, 0.05), "feasibility": (0.75, 0.08), "diff": (0.40, 0.10), "weight": 0.15},
    "F2_campaign":      {"ai_pot": (0.80, 0.06), "feasibility": (0.70, 0.10), "diff": (0.35, 0.10), "weight": 0.12},
    "F3_intelligence":  {"ai_pot": (0.90, 0.04), "feasibility": (0.60, 0.10), "diff": (0.65, 0.10), "weight": 0.27, "must_win": True},
    "F4_performance":   {"ai_pot": (0.85, 0.05), "feasibility": (0.80, 0.06), "diff": (0.30, 0.08), "weight": 0.13},
    "F5_discovery":     {"ai_pot": (0.95, 0.03), "feasibility": (0.35, 0.12), "diff": (0.85, 0.08), "weight": 0.30, "must_win": True},
    "F6_competitive":   {"ai_pot": (0.75, 0.08), "feasibility": (0.85, 0.06), "diff": (0.25, 0.08), "weight": 0.08},
    "F7_brand_crisis":  {"ai_pot": (0.80, 0.06), "feasibility": (0.70, 0.10), "diff": (0.50, 0.12), "weight": 0.09},
}

# =============================================================================
# 4. CROSS-MODULE COMPLEMENTARITIES (mean, std)
# =============================================================================
GAMMAS = {
    "M1_M3": {"mean": 0.45, "std": 0.10},  # AI capability × Skill readiness
    "M1_M2": {"mean": 0.35, "std": 0.08},  # AI deployment × Customer adoption
    "M2_M4": {"mean": 0.30, "std": 0.08},  # Scenarios × Strategy
    "M3_M4": {"mean": 0.25, "std": 0.07},  # Org readiness × Execution
}

# =============================================================================
# 5. EARLY WARNING TRIGGER PARAMETERS
# =============================================================================
TRIGGERS = {
    "T1_ai_query_share": {
        "current": 0.08,
        "monthly_growth_rate": {"mean": 0.03, "std": 0.015},  # 3% ± 1.5% per month
        "thresholds": {"S1": 0.25, "S2": 0.15, "S3_decline": 0.05},
    },
    "T3_client_ai_adoption": {
        "current": 0.12,
        "monthly_growth_rate": {"mean": 0.02, "std": 0.01},
        "thresholds": {"S1": 0.40, "S2": 0.25, "S3_stagnate": 0.10},
    },
    "T4_advisor_preference": {
        "current": 0.72,
        "monthly_change_rate": {"mean": -0.008, "std": 0.005},  # declining
        "thresholds": {"S1": 0.40, "S2": 0.55, "S3": 0.80},
    },
}

# =============================================================================
# 6. NO-REGRET MOVE PARAMETERS
# =============================================================================
NR_MOVES = {
    "NR1_ai_literacy": {
        "rho":  (0.95, 0.03), "V_min": (0.80, 0.06),
        "O":    (0.85, 0.05), "r":     (0.90, 0.04), "L": (0.90, 0.04),
    },
    "NR2_monitoring": {
        "rho":  (0.90, 0.04), "V_min": (0.75, 0.08),
        "O":    (0.95, 0.03), "r":     (0.85, 0.05), "L": (0.95, 0.03),
    },
    "NR3_discovery_pilot": {
        "rho":  (0.80, 0.07), "V_min": (0.60, 0.10),
        "O":    (0.90, 0.05), "r":     (0.75, 0.08), "L": (0.85, 0.06),
    },
    "NR4_intelligence": {
        "rho":  (0.85, 0.06), "V_min": (0.70, 0.08),
        "O":    (0.80, 0.06), "r":     (0.60, 0.10), "L": (0.80, 0.06),
    },
    "NR5_ethics": {
        "rho":  (0.90, 0.04), "V_min": (0.65, 0.08),
        "O":    (0.70, 0.08), "r":     (0.95, 0.03), "L": (0.60, 0.10),
    },
    "NR6_cs_trust": {
        "rho":  (0.75, 0.08), "V_min": (0.70, 0.10),
        "O":    (0.60, 0.10), "r":     (0.70, 0.08), "L": (0.75, 0.08),
    },
}

# Scenario-specific value for each segment (mean, std)
SEGMENT_SCENARIO_VALUE = {
    "SEG-LEGACY":      {"S1": (0.50, 0.12), "S2": (0.75, 0.08), "S3": (0.90, 0.05)},
    "SEG-CS-MIGRATED": {"S1": (0.30, 0.12), "S2": (0.55, 0.10), "S3": (0.70, 0.10)},
    "SEG-DIGITAL":     {"S1": (0.65, 0.10), "S2": (0.70, 0.08), "S3": (0.45, 0.12)},
    "SEG-UHNW":        {"S1": (0.60, 0.10), "S2": (0.80, 0.06), "S3": (0.92, 0.04)},
}

# Module weights per scenario
MODULE_WEIGHTS = {
    "S1": {"M1": 0.35, "M2": 0.25, "M3": 0.25, "M4": 0.15},
    "S2": {"M1": 0.25, "M2": 0.25, "M3": 0.25, "M4": 0.25},
    "S3": {"M1": 0.15, "M2": 0.20, "M3": 0.35, "M4": 0.30},
}


# =============================================================================
# HELPER: Sample from Beta given mean and std
# =============================================================================
def sample_beta(mean, std, n):
    """Sample from Beta distribution given mean and std, clamped to (0,1)."""
    mean = np.clip(mean, 0.01, 0.99)
    var = std ** 2
    max_var = mean * (1 - mean)
    if var >= max_var:
        var = max_var * 0.95
    alpha = mean * (mean * (1 - mean) / var - 1)
    beta_param = (1 - mean) * (mean * (1 - mean) / var - 1)
    alpha = max(alpha, 0.5)
    beta_param = max(beta_param, 0.5)
    return np.random.beta(alpha, beta_param, n)


def sample_lognormal(mean, std, n):
    """Sample from LogNormal given mean and std in linear space."""
    var = std ** 2
    sigma2 = np.log(1 + var / mean**2)
    mu = np.log(mean) - sigma2 / 2
    return np.random.lognormal(mu, np.sqrt(sigma2), n)


def sample_param(spec, n):
    """Sample n draws from parameter spec."""
    if spec["dist"] == "beta":
        return sample_beta(spec["mean"], spec["std"], n)
    elif spec["dist"] == "lognormal":
        return sample_lognormal(spec["mean"], spec["std"], n)
    else:
        return np.random.normal(spec["mean"], spec["std"], n)


def ci(arr, pct=95):
    """Return (mean, lo, hi) for given percentile CI."""
    lo = (100 - pct) / 2
    hi = 100 - lo
    return float(np.mean(arr)), float(np.percentile(arr, lo)), float(np.percentile(arr, hi))


def ci_str(arr, pct=95, fmt=".2f"):
    """Format CI as string."""
    m, lo, hi = ci(arr, pct)
    return f"{m:{fmt}} [{lo:{fmt}}, {hi:{fmt}}]"


# =============================================================================
# SIMULATION
# =============================================================================
def run_simulation(n_draws=N_DRAWS):
    results = {}

    # -------------------------------------------------------------------------
    # A. SCENARIO PROBABILITIES (Dirichlet)
    # -------------------------------------------------------------------------
    alphas = np.array([SCENARIO_ALPHA["S1_bigtech"],
                       SCENARIO_ALPHA["S2_hybrid"],
                       SCENARIO_ALPHA["S3_trust"]])
    scenario_draws = np.random.dirichlet(alphas, n_draws)  # (n, 3)
    p_s1 = scenario_draws[:, 0]
    p_s2 = scenario_draws[:, 1]
    p_s3 = scenario_draws[:, 2]

    results["scenario_probabilities"] = {
        "S1_bigtech":  {"mean_ci": ci_str(p_s1), "p5": f"{np.percentile(p_s1, 5):.3f}", "p95": f"{np.percentile(p_s1, 95):.3f}"},
        "S2_hybrid":   {"mean_ci": ci_str(p_s2), "p5": f"{np.percentile(p_s2, 5):.3f}", "p95": f"{np.percentile(p_s2, 95):.3f}"},
        "S3_trust":    {"mean_ci": ci_str(p_s3), "p5": f"{np.percentile(p_s3, 5):.3f}", "p95": f"{np.percentile(p_s3, 95):.3f}"},
    }

    # -------------------------------------------------------------------------
    # B. SEGMENT BEHAVIORAL PARAMETERS
    # -------------------------------------------------------------------------
    seg_params = {}
    for seg_name, seg_spec in SEGMENTS.items():
        seg_params[seg_name] = {}
        for param_name, param_spec in seg_spec.items():
            if param_name == "size":
                continue
            draws = sample_param(param_spec, n_draws)
            seg_params[seg_name][param_name] = draws

    results["segment_parameters"] = {}
    for seg_name in SEGMENTS:
        results["segment_parameters"][seg_name] = {}
        for param_name in seg_params[seg_name]:
            draws = seg_params[seg_name][param_name]
            results["segment_parameters"][seg_name][param_name] = ci_str(draws)

    # -------------------------------------------------------------------------
    # C. SEGMENT RETENTION RISK (tau × switching_cost → retention probability)
    # -------------------------------------------------------------------------
    results["segment_retention_risk"] = {}
    for seg_name in SEGMENTS:
        tau = seg_params[seg_name]["tau_trust"]
        sc = seg_params[seg_name]["switching_cost"]
        # Retention = tau * switching_cost (multiplicative: both must be high)
        retention = tau * sc
        flight_risk = 1.0 - retention
        results["segment_retention_risk"][seg_name] = {
            "retention_probability": ci_str(retention),
            "flight_risk": ci_str(flight_risk),
            "clients_at_risk_mean": int(np.mean(flight_risk) * SEGMENTS[seg_name]["size"]),
        }

    # -------------------------------------------------------------------------
    # D. MARKETING FUNCTION VALUE (Module 1)
    # -------------------------------------------------------------------------
    func_values = {}
    total_v = np.zeros(n_draws)
    for fname, fspec in FUNCTIONS.items():
        ai = sample_beta(fspec["ai_pot"][0], fspec["ai_pot"][1], n_draws)
        feas = sample_beta(fspec["feasibility"][0], fspec["feasibility"][1], n_draws)
        diff = sample_beta(fspec["diff"][0], fspec["diff"][1], n_draws)
        w = fspec["weight"]
        v = w * ai * feas * (1 + diff)
        func_values[fname] = v
        total_v += v

    results["module_1_value_chain"] = {
        "V_total": ci_str(total_v),
    }
    results["module_1_functions"] = {}
    for fname in FUNCTIONS:
        results["module_1_functions"][fname] = ci_str(func_values[fname], fmt=".3f")

    # Priority ranking stability
    rank_counts = {fn: np.zeros(len(FUNCTIONS)) for fn in FUNCTIONS}
    for i in range(n_draws):
        vals = [(fn, func_values[fn][i]) for fn in FUNCTIONS]
        vals.sort(key=lambda x: -x[1])
        for rank, (fn, _) in enumerate(vals):
            rank_counts[fn][rank] += 1
    results["module_1_ranking_stability"] = {}
    for fn in FUNCTIONS:
        modal_rank = int(np.argmax(rank_counts[fn])) + 1
        top3_pct = float(np.sum(rank_counts[fn][:3]) / n_draws * 100)
        results["module_1_ranking_stability"][fn] = {
            "modal_rank": modal_rank,
            "top3_probability": f"{top3_pct:.1f}%",
        }

    # -------------------------------------------------------------------------
    # E. SEGMENT-SCENARIO EXPECTED VALUE (Module 2)
    # -------------------------------------------------------------------------
    results["module_2_segment_scenario"] = {}
    for seg_name in SEGMENTS:
        v_s1 = sample_beta(*SEGMENT_SCENARIO_VALUE[seg_name]["S1"], n_draws)
        v_s2 = sample_beta(*SEGMENT_SCENARIO_VALUE[seg_name]["S2"], n_draws)
        v_s3 = sample_beta(*SEGMENT_SCENARIO_VALUE[seg_name]["S3"], n_draws)
        # Scenario-weighted expected value
        ev = p_s1 * v_s1 + p_s2 * v_s2 + p_s3 * v_s3
        results["module_2_segment_scenario"][seg_name] = {
            "S1_value": ci_str(v_s1),
            "S2_value": ci_str(v_s2),
            "S3_value": ci_str(v_s3),
            "expected_value_weighted": ci_str(ev),
            "worst_case_5pct": f"{np.percentile(ev, 5):.3f}",
        }

    # -------------------------------------------------------------------------
    # F. CROSS-MODULE COMPLEMENTARITIES (Module integration)
    # -------------------------------------------------------------------------
    gamma_draws = {}
    for gname, gspec in GAMMAS.items():
        gamma_draws[gname] = np.clip(np.random.normal(gspec["mean"], gspec["std"], n_draws), 0, 1)

    results["cross_module_gammas"] = {}
    for gname in GAMMAS:
        results["cross_module_gammas"][gname] = ci_str(gamma_draws[gname])

    # -------------------------------------------------------------------------
    # G. NO-REGRET MOVE SCORES (Module 4)
    # -------------------------------------------------------------------------
    results["module_4_no_regret"] = {}
    nr_scores_all = {}
    for nr_name, nr_spec in NR_MOVES.items():
        rho = sample_beta(*nr_spec["rho"], n_draws)
        v_min = sample_beta(*nr_spec["V_min"], n_draws)
        o = sample_beta(*nr_spec["O"], n_draws)
        r = sample_beta(*nr_spec["r"], n_draws)
        l = sample_beta(*nr_spec["L"], n_draws)
        # NR = rho * V_min + (1-rho) * O + r * L
        nr_score = rho * v_min + (1 - rho) * o + r * l
        nr_scores_all[nr_name] = nr_score
        results["module_4_no_regret"][nr_name] = {
            "NR_score": ci_str(nr_score),
            "P_above_0.70": f"{np.mean(nr_score > 0.70) * 100:.1f}%",
            "P_above_0.80": f"{np.mean(nr_score > 0.80) * 100:.1f}%",
        }

    # NR ranking stability
    nr_names = list(NR_MOVES.keys())
    nr_rank_1_pct = {}
    for i, name in enumerate(nr_names):
        rank_1_count = 0
        for d in range(n_draws):
            scores = [nr_scores_all[n][d] for n in nr_names]
            if scores[i] == max(scores):
                rank_1_count += 1
        nr_rank_1_pct[name] = f"{rank_1_count / n_draws * 100:.1f}%"
    results["module_4_ranking_stability"] = nr_rank_1_pct

    # -------------------------------------------------------------------------
    # H. EARLY WARNING TRIGGER CROSSING (time to threshold)
    # -------------------------------------------------------------------------
    results["early_warning_triggers"] = {}
    horizons_months = [12, 24, 36]

    for tname, tspec in TRIGGERS.items():
        current = tspec["current"]
        # Support both naming conventions
        rate_key = "monthly_growth_rate" if "monthly_growth_rate" in tspec else "monthly_change_rate"
        gr_mean = tspec[rate_key]["mean"]
        gr_std = tspec[rate_key]["std"]

        growth_rates = np.random.normal(gr_mean, gr_std, n_draws)

        trigger_results = {}
        for threshold_name, threshold_val in tspec["thresholds"].items():
            # Time to reach threshold: current + rate * t = threshold
            # t = (threshold - current) / rate
            if "decline" in threshold_name or "stagnate" in threshold_name:
                # For decline thresholds, check if value falls below
                time_to_cross = np.where(
                    growth_rates < 0,
                    (threshold_val - current) / growth_rates,
                    np.inf
                )
            else:
                # Standard: growth toward threshold
                delta = threshold_val - current
                if delta > 0:
                    time_to_cross = np.where(
                        growth_rates > 0,
                        delta / growth_rates,
                        np.inf
                    )
                else:
                    # Already past threshold
                    time_to_cross = np.zeros(n_draws)

            crossing_probs = {}
            for h in horizons_months:
                p_cross = float(np.mean(time_to_cross <= h))
                crossing_probs[f"{h}m"] = f"{p_cross * 100:.1f}%"

            median_months = float(np.median(time_to_cross[np.isfinite(time_to_cross)])) if np.any(np.isfinite(time_to_cross)) else float("inf")
            trigger_results[threshold_name] = {
                "crossing_probability": crossing_probs,
                "median_months_to_cross": f"{median_months:.1f}" if median_months < 100 else ">100",
            }

        results["early_warning_triggers"][tname] = trigger_results

    # -------------------------------------------------------------------------
    # I. SENSITIVITY ANALYSIS (Variance Decomposition)
    # -------------------------------------------------------------------------
    # Which parameters drive the most variance in total expected value?
    # Use segment-weighted expected value as target
    total_clients = sum(s["size"] for s in SEGMENTS.values())
    portfolio_ev = np.zeros(n_draws)
    for seg_name in SEGMENTS:
        w = SEGMENTS[seg_name]["size"] / total_clients
        v_s1 = sample_beta(*SEGMENT_SCENARIO_VALUE[seg_name]["S1"], n_draws)
        v_s2 = sample_beta(*SEGMENT_SCENARIO_VALUE[seg_name]["S2"], n_draws)
        v_s3 = sample_beta(*SEGMENT_SCENARIO_VALUE[seg_name]["S3"], n_draws)
        ev = p_s1 * v_s1 + p_s2 * v_s2 + p_s3 * v_s3
        portfolio_ev += w * ev

    results["portfolio_expected_value"] = ci_str(portfolio_ev)

    # Correlations with key parameters
    sensitivity = {}
    for seg_name in SEGMENTS:
        for param_name in seg_params[seg_name]:
            key = f"{seg_name}.{param_name}"
            corr = float(np.corrcoef(seg_params[seg_name][param_name], portfolio_ev)[0, 1])
            if abs(corr) > 0.05:
                sensitivity[key] = f"{corr:.3f}"

    # Add scenario probability correlations
    sensitivity["P(S1_bigtech)"] = f"{float(np.corrcoef(p_s1, portfolio_ev)[0, 1]):.3f}"
    sensitivity["P(S2_hybrid)"] = f"{float(np.corrcoef(p_s2, portfolio_ev)[0, 1]):.3f}"
    sensitivity["P(S3_trust)"] = f"{float(np.corrcoef(p_s3, portfolio_ev)[0, 1]):.3f}"

    # Sort by absolute correlation
    sensitivity_sorted = dict(sorted(sensitivity.items(), key=lambda x: -abs(float(x[1]))))
    results["sensitivity_top_drivers"] = dict(list(sensitivity_sorted.items())[:15])

    # -------------------------------------------------------------------------
    # J. DYNAMIC COMPLEMENTARITY PREMIUM (Module 3)
    # -------------------------------------------------------------------------
    # MS-SF-003: gamma_low > gamma_normal > gamma_high
    # Simulate ROI of early vs late AI training investment
    skill_gap = sample_beta(0.50, 0.10, n_draws)  # average skill gap
    early_investment = sample_beta(0.70, 0.10, n_draws)  # high early investment
    late_investment = sample_beta(0.70, 0.10, n_draws)  # same investment, but late

    # Dynamic complementarity factor: early investment boosts later returns
    dc_factor_early = 1.0 + sample_beta(0.45, 0.10, n_draws)  # 1.45x average boost
    dc_factor_late = np.ones(n_draws)  # no boost for late starters

    # ROI = (skill_improvement / investment) × dc_factor
    roi_early = (skill_gap * early_investment * dc_factor_early) / early_investment
    roi_late = (skill_gap * late_investment * dc_factor_late) / late_investment
    dc_premium = roi_early / roi_late

    results["module_3_dynamic_complementarity"] = {
        "roi_early_training": ci_str(roi_early),
        "roi_late_training": ci_str(roi_late),
        "dc_premium_ratio": ci_str(dc_premium),
        "P_early_better": f"{np.mean(roi_early > roi_late) * 100:.1f}%",
    }

    # -------------------------------------------------------------------------
    # K. INTEGRATED MODEL VALUE
    # -------------------------------------------------------------------------
    # U_total = sum(w_m * V_m) + sum(gamma_ij * sqrt(V_i * V_j))
    # Simplified: use normalized module values
    m1_v = total_v / np.max(total_v)  # normalize
    m2_v = portfolio_ev / np.max(portfolio_ev)
    m3_v = roi_early / np.max(roi_early)
    m4_v_arr = np.zeros(n_draws)
    for nr in nr_scores_all.values():
        m4_v_arr += nr
    m4_v = m4_v_arr / (len(NR_MOVES) * np.max(m4_v_arr))

    integrated_values = {}
    for scenario, weights in MODULE_WEIGHTS.items():
        u = (weights["M1"] * m1_v + weights["M2"] * m2_v +
             weights["M3"] * m3_v + weights["M4"] * m4_v)
        # Add complementarity terms
        u += gamma_draws["M1_M3"] * np.sqrt(m1_v * m3_v)
        u += gamma_draws["M1_M2"] * np.sqrt(m1_v * m2_v)
        u += gamma_draws["M2_M4"] * np.sqrt(m2_v * m4_v)
        u += gamma_draws["M3_M4"] * np.sqrt(m3_v * m4_v)
        integrated_values[scenario] = u

    results["integrated_model_value"] = {}
    for scenario in MODULE_WEIGHTS:
        results["integrated_model_value"][scenario] = ci_str(integrated_values[scenario])

    # Expected integrated value (scenario-weighted)
    u_expected = (p_s1 * integrated_values["S1"] +
                  p_s2 * integrated_values["S2"] +
                  p_s3 * integrated_values["S3"])
    results["integrated_model_value"]["expected_weighted"] = ci_str(u_expected)

    return results


# =============================================================================
# OUTPUT FORMATTING
# =============================================================================
def print_results(results):
    """Print results in structured format."""
    print("=" * 78)
    print("  MONTE CARLO SIMULATION: MOD-UBS-AIMARK-001")
    print(f"  UBS AI Marketing Transformation Model | {N_DRAWS:,} Draws")
    print(f"  Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 78)

    print("\n" + "─" * 78)
    print("  A. SCENARIO PROBABILITIES (Dirichlet Distribution)")
    print("─" * 78)
    for s, v in results["scenario_probabilities"].items():
        print(f"  {s:20s}  {v['mean_ci']:30s}  (5th: {v['p5']}, 95th: {v['p95']})")

    print("\n" + "─" * 78)
    print("  B. SEGMENT BEHAVIORAL PARAMETERS (95% CI)")
    print("─" * 78)
    for seg in results["segment_parameters"]:
        print(f"\n  {seg}:")
        for param, val in results["segment_parameters"][seg].items():
            print(f"    {param:20s}  {val}")

    print("\n" + "─" * 78)
    print("  C. SEGMENT RETENTION RISK")
    print("─" * 78)
    for seg, v in results["segment_retention_risk"].items():
        print(f"\n  {seg}:")
        print(f"    Retention probability:  {v['retention_probability']}")
        print(f"    Flight risk:            {v['flight_risk']}")
        print(f"    Clients at risk (mean): {v['clients_at_risk_mean']:,}")

    print("\n" + "─" * 78)
    print("  D. MODULE 1: MARKETING FUNCTION VALUES (95% CI)")
    print("─" * 78)
    print(f"  V_total: {results['module_1_value_chain']['V_total']}")
    print()
    for fn, val in results["module_1_functions"].items():
        stab = results["module_1_ranking_stability"][fn]
        print(f"  {fn:20s}  {val:30s}  Rank {stab['modal_rank']} ({stab['top3_probability']} in top 3)")

    print("\n" + "─" * 78)
    print("  E. MODULE 2: SEGMENT × SCENARIO EXPECTED VALUE")
    print("─" * 78)
    for seg, v in results["module_2_segment_scenario"].items():
        print(f"\n  {seg}:")
        print(f"    S1 BigTech:    {v['S1_value']}")
        print(f"    S2 Hybrid:     {v['S2_value']}")
        print(f"    S3 Trust:      {v['S3_value']}")
        print(f"    E[V] weighted: {v['expected_value_weighted']}")
        print(f"    VaR (5th pct): {v['worst_case_5pct']}")

    print("\n" + "─" * 78)
    print("  F. CROSS-MODULE COMPLEMENTARITIES")
    print("─" * 78)
    for g, val in results["cross_module_gammas"].items():
        print(f"  gamma({g}): {val}")

    print("\n" + "─" * 78)
    print("  G. MODULE 4: NO-REGRET MOVE SCORES (95% CI)")
    print("─" * 78)
    for nr, v in results["module_4_no_regret"].items():
        rank1 = results["module_4_ranking_stability"].get(nr, "?")
        print(f"  {nr:25s}  NR={v['NR_score']:30s}  P>0.80: {v['P_above_0.80']:6s}  #1: {rank1}")

    print("\n" + "─" * 78)
    print("  H. EARLY WARNING TRIGGER CROSSING PROBABILITIES")
    print("─" * 78)
    for t, thresholds in results["early_warning_triggers"].items():
        print(f"\n  {t}:")
        for threshold_name, tv in thresholds.items():
            crossing = tv["crossing_probability"]
            median = tv["median_months_to_cross"]
            print(f"    {threshold_name:20s}  12m: {crossing['12m']:6s}  24m: {crossing['24m']:6s}  36m: {crossing['36m']:6s}  Median: {median}")

    print("\n" + "─" * 78)
    print("  I. SENSITIVITY ANALYSIS (Top Drivers of Portfolio Value)")
    print("─" * 78)
    for param, corr in results["sensitivity_top_drivers"].items():
        bar = "█" * int(abs(float(corr)) * 40)
        sign = "+" if float(corr) > 0 else "-"
        print(f"  {param:35s}  r={corr:7s}  {sign}{bar}")

    print("\n" + "─" * 78)
    print("  J. MODULE 3: DYNAMIC COMPLEMENTARITY PREMIUM")
    print("─" * 78)
    dc = results["module_3_dynamic_complementarity"]
    print(f"  ROI early training (2026): {dc['roi_early_training']}")
    print(f"  ROI late training (2028):  {dc['roi_late_training']}")
    print(f"  DC premium ratio:          {dc['dc_premium_ratio']}")
    print(f"  P(early > late):           {dc['P_early_better']}")

    print("\n" + "─" * 78)
    print("  K. INTEGRATED MODEL VALUE (Scenario-Weighted)")
    print("─" * 78)
    for s, val in results["integrated_model_value"].items():
        print(f"  {s:20s}  {val}")

    print("\n" + "=" * 78)
    print("  END OF SIMULATION")
    print("=" * 78)


def results_to_yaml_block(results):
    """Convert results to a YAML-compatible string for model-registry."""
    lines = []
    lines.append("  monte_carlo_results:")
    lines.append(f"    draws: {N_DRAWS}")
    lines.append(f"    seed: 2026")
    lines.append(f"    date: '{datetime.now().strftime('%Y-%m-%d')}'")
    lines.append(f"    script: 'scripts/monte_carlo_ubs_aimark.py'")
    lines.append("")

    lines.append("    scenario_probabilities:")
    for s, v in results["scenario_probabilities"].items():
        lines.append(f"      {s}: \"{v['mean_ci']}\"")

    lines.append("")
    lines.append("    segment_retention_risk:")
    for seg, v in results["segment_retention_risk"].items():
        lines.append(f"      {seg}:")
        lines.append(f"        flight_risk: \"{v['flight_risk']}\"")
        lines.append(f"        clients_at_risk: {v['clients_at_risk_mean']}")

    lines.append("")
    lines.append("    module_1_total_value: \"{0}\"".format(results["module_1_value_chain"]["V_total"]))

    lines.append("")
    lines.append("    module_4_no_regret_scores:")
    for nr, v in results["module_4_no_regret"].items():
        lines.append(f"      {nr}: \"{v['NR_score']}\"")

    lines.append("")
    lines.append("    early_warning_24m_crossing:")
    for t, thresholds in results["early_warning_triggers"].items():
        lines.append(f"      {t}:")
        for tn, tv in thresholds.items():
            lines.append(f"        {tn}: \"{tv['crossing_probability']['24m']}\"")

    lines.append("")
    lines.append("    dynamic_complementarity_premium: \"{0}\"".format(
        results["module_3_dynamic_complementarity"]["dc_premium_ratio"]))
    lines.append("    P_early_training_better: \"{0}\"".format(
        results["module_3_dynamic_complementarity"]["P_early_better"]))

    lines.append("")
    lines.append("    integrated_expected_value: \"{0}\"".format(
        results["integrated_model_value"]["expected_weighted"]))

    lines.append("")
    lines.append("    sensitivity_top_5:")
    for i, (param, corr) in enumerate(results["sensitivity_top_drivers"].items()):
        if i >= 5:
            break
        lines.append(f"      - parameter: \"{param}\"")
        lines.append(f"        correlation: {corr}")

    return "\n".join(lines)


# =============================================================================
# MAIN
# =============================================================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Monte Carlo for MOD-UBS-AIMARK-001")
    parser.add_argument("--draws", type=int, default=N_DRAWS, help="Number of MC draws")
    parser.add_argument("--output", choices=["text", "yaml", "json"], default="text")
    args = parser.parse_args()

    N_DRAWS = args.draws
    np.random.seed(2026)

    print(f"Running Monte Carlo with {N_DRAWS:,} draws...", file=sys.stderr)
    results = run_simulation(N_DRAWS)

    if args.output == "text":
        print_results(results)
    elif args.output == "yaml":
        print(results_to_yaml_block(results))
    elif args.output == "json":
        print(json.dumps(results, indent=2))
