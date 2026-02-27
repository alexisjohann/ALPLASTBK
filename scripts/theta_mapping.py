#!/usr/bin/env python3
"""
Theta Mapping: d/SMD und pp → 0-1 Skala
========================================

Piecewise linear Mapping mit MC-Unsicherheitspropagation.

Mapping-Knots (Version 1):
- d/SMD: 0.0→0.00, 0.2→0.30, 0.5→0.60, 0.8→0.90, 1.2→0.97
- pp:    0→0.00, 5→0.30, 15→0.50, 30→0.70, 60→0.90, 90→0.97

Pipeline:
  LLM → Kalibration → Mapping → θ ∈ [0,1]

Usage:
    from theta_mapping import build_alpha_theta, map_d_to_theta, map_pp_to_theta

    # Einzelner Parameter
    theta, eu = mc_map_d(llm_d=0.70, eu_llm=0.12)

    # Kompletter α-Vektor
    alpha_specs = [
        {"type": "d", "llm_hat": 0.70, "eu_llm": 0.12},
        {"type": "pp", "llm_hat": 25.0, "eu_llm": 6.0},
    ]
    alpha_hat, alpha_eu = build_alpha_theta(alpha_specs)

Author: EBF Framework
Date: 2025-01-13
Version: mapping_v1
"""

import numpy as np
import json
import argparse
from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional
from pathlib import Path


# =============================================================================
# MAPPING KNOTS (VERSION 1) - AUDITABLE
# =============================================================================

MAPPING_VERSION = "v1"

# d/SMD → θ ∈ [0,1]
D_TO_THETA_KNOTS = [
    (0.0, 0.00),   # unwirksam
    (0.2, 0.30),   # klein
    (0.5, 0.60),   # moderat-stark
    (0.8, 0.90),   # sehr stark
    (1.2, 0.97),   # Sättigung
]

# pp → θ ∈ [0,1]
PP_TO_THETA_KNOTS = [
    (0.0,  0.00),
    (5.0,  0.30),
    (15.0, 0.50),
    (30.0, 0.70),
    (60.0, 0.90),
    (90.0, 0.97),
]


# =============================================================================
# CALIBRATION FUNCTIONS (from validated fits)
# =============================================================================

# d/SMD calibration: θ_true = 0.03 + 0.79 × θ_llm
CALIBRATION_D_A = 0.03
CALIBRATION_D_B = 0.79
CALIBRATION_D_SIGMA = 0.06

# pp calibration: pp_true = -0.48 + 1.007 × pp_llm
CALIBRATION_PP_A = -0.48
CALIBRATION_PP_B = 1.007
CALIBRATION_PP_SIGMA = 3.54


def calibrate_d(llm_d: float) -> float:
    """Calibrate d/SMD estimate from LLMMC."""
    return CALIBRATION_D_A + CALIBRATION_D_B * llm_d


def calibrate_pp(llm_pp: float) -> float:
    """Calibrate pp estimate from LLMMC."""
    result = CALIBRATION_PP_A + CALIBRATION_PP_B * llm_pp
    return max(0.0, result)  # Clip at 0 (no negative effects)


def calibrate_d_with_uncertainty(llm_d: float, eu_llm: float) -> Tuple[float, float]:
    """Calibrate d with propagated uncertainty."""
    mean = calibrate_d(llm_d)
    se = np.sqrt((CALIBRATION_D_B * eu_llm)**2 + CALIBRATION_D_SIGMA**2)
    return mean, se


def calibrate_pp_with_uncertainty(llm_pp: float, eu_llm: float) -> Tuple[float, float]:
    """Calibrate pp with propagated uncertainty."""
    mean = calibrate_pp(llm_pp)
    se = np.sqrt((CALIBRATION_PP_B * eu_llm)**2 + CALIBRATION_PP_SIGMA**2)
    return mean, se


# =============================================================================
# PIECEWISE LINEAR MAPPING
# =============================================================================

def piecewise_map(x: np.ndarray, knots: List[Tuple[float, float]]) -> np.ndarray:
    """
    Piecewise linear mapping using specified knots.

    Args:
        x: Input values (can be array)
        knots: List of (x_knot, y_knot) tuples, strictly increasing in x

    Returns:
        Mapped values, clamped to knot range
    """
    xs = np.array([k[0] for k in knots], dtype=float)
    ys = np.array([k[1] for k in knots], dtype=float)

    x = np.asarray(x, dtype=float)
    x_clamped = np.clip(x, xs[0], xs[-1])

    return np.interp(x_clamped, xs, ys)


def map_d_to_theta(d: float) -> float:
    """Map d/SMD to θ ∈ [0,1]."""
    result = piecewise_map(np.array([d]), D_TO_THETA_KNOTS)
    return float(result[0])


def map_pp_to_theta(pp: float) -> float:
    """Map pp to θ ∈ [0,1]."""
    result = piecewise_map(np.array([pp]), PP_TO_THETA_KNOTS)
    return float(result[0])


def map_d_array_to_theta(d_array: np.ndarray) -> np.ndarray:
    """Map array of d values to θ."""
    return piecewise_map(d_array, D_TO_THETA_KNOTS)


def map_pp_array_to_theta(pp_array: np.ndarray) -> np.ndarray:
    """Map array of pp values to θ."""
    return piecewise_map(pp_array, PP_TO_THETA_KNOTS)


# =============================================================================
# MONTE CARLO UNCERTAINTY PROPAGATION
# =============================================================================

def mc_map(
    mean: float,
    se: float,
    mapper_func,
    n: int = 20000,
    seed: int = 0
) -> Tuple[float, float]:
    """
    Monte Carlo propagation through nonlinear mapping.

    Args:
        mean: Point estimate in original scale
        se: Standard error in original scale
        mapper_func: Mapping function (e.g., map_d_array_to_theta)
        n: Number of MC draws
        seed: Random seed

    Returns:
        (theta_hat, EU_theta) on 0-1 scale
    """
    rng = np.random.default_rng(seed)
    draws = rng.normal(mean, se, size=n)
    theta_draws = mapper_func(draws)

    return float(theta_draws.mean()), float(theta_draws.std(ddof=1))


def mc_map_d(
    llm_d: float,
    eu_llm: float,
    n: int = 20000,
    seed: int = 0
) -> Tuple[float, float]:
    """
    Full pipeline: LLM d estimate → calibrated θ with uncertainty.

    Pipeline: llm_d → calibrate_d → map_d_to_theta → (θ_hat, EU_θ)
    """
    # Calibrate
    true_mean, true_se = calibrate_d_with_uncertainty(llm_d, eu_llm)

    # MC propagation through mapping
    return mc_map(true_mean, true_se, map_d_array_to_theta, n=n, seed=seed)


def mc_map_pp(
    llm_pp: float,
    eu_llm: float,
    n: int = 20000,
    seed: int = 0
) -> Tuple[float, float]:
    """
    Full pipeline: LLM pp estimate → calibrated θ with uncertainty.

    Pipeline: llm_pp → calibrate_pp → map_pp_to_theta → (θ_hat, EU_θ)
    """
    # Calibrate
    true_mean, true_se = calibrate_pp_with_uncertainty(llm_pp, eu_llm)

    # MC propagation through mapping
    return mc_map(true_mean, true_se, map_pp_array_to_theta, n=n, seed=seed)


# =============================================================================
# BUILD ALPHA VECTOR
# =============================================================================

@dataclass
class AlphaSpec:
    """Specification for a single α parameter."""
    type: str           # "d" or "pp"
    llm_hat: float      # LLM point estimate
    eu_llm: float       # LLM elicitation uncertainty
    name: Optional[str] = None

    def to_dict(self) -> Dict:
        return {
            "type": self.type,
            "llm_hat": self.llm_hat,
            "eu_llm": self.eu_llm,
            "name": self.name
        }


def build_alpha_theta(
    alpha_specs: List[Dict],
    n_mc: int = 20000
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Build α vector on 0-1 scale from LLM estimates.

    Args:
        alpha_specs: List of dicts with keys: type, llm_hat, eu_llm
                    type is "d" or "pp"
        n_mc: Monte Carlo samples for uncertainty propagation

    Returns:
        (alpha_hat_theta, alpha_eu_theta) as numpy arrays

    Example:
        specs = [
            {"type": "d", "llm_hat": 0.70, "eu_llm": 0.12},
            {"type": "pp", "llm_hat": 25.0, "eu_llm": 6.0},
        ]
        alpha_hat, alpha_eu = build_alpha_theta(specs)
    """
    hats, eus = [], []

    for i, sp in enumerate(alpha_specs):
        if sp["type"] == "d":
            theta_hat, theta_eu = mc_map_d(
                sp["llm_hat"],
                sp["eu_llm"],
                n=n_mc,
                seed=100+i
            )
        elif sp["type"] == "pp":
            theta_hat, theta_eu = mc_map_pp(
                sp["llm_hat"],
                sp["eu_llm"],
                n=n_mc,
                seed=200+i
            )
        else:
            raise ValueError(f"type must be 'd' or 'pp', got: {sp['type']}")

        hats.append(theta_hat)
        eus.append(theta_eu)

    return np.array(hats), np.array(eus)


# =============================================================================
# REPORTING
# =============================================================================

def print_mapping_report(alpha_specs: List[Dict], alpha_hat: np.ndarray, alpha_eu: np.ndarray):
    """Print formatted mapping report."""
    print("\n" + "=" * 70)
    print("THETA MAPPING REPORT")
    print(f"Version: {MAPPING_VERSION}")
    print("=" * 70)

    print(f"\n{'#':<3} {'Type':<4} {'LLM_hat':>10} {'EU_llm':>10} {'θ_hat':>10} {'EU_θ':>10}")
    print("-" * 70)

    for i, (sp, h, e) in enumerate(zip(alpha_specs, alpha_hat, alpha_eu)):
        name = sp.get("name", f"α_{i+1}")
        print(f"{i+1:<3} {sp['type']:<4} {sp['llm_hat']:>10.3f} {sp['eu_llm']:>10.3f} {h:>10.3f} {e:>10.3f}")

    print("-" * 70)
    print(f"{'Σ':<3} {'':<4} {'':<10} {'':<10} {alpha_hat.sum():>10.3f} {np.sqrt((alpha_eu**2).sum()):>10.3f}")

    print(f"\n📋 MAPPING KNOTS")
    print(f"   d/SMD: {D_TO_THETA_KNOTS}")
    print(f"   pp:    {PP_TO_THETA_KNOTS}")

    print(f"\n📐 CALIBRATION")
    print(f"   d/SMD: θ_true = {CALIBRATION_D_A} + {CALIBRATION_D_B} × θ_llm (σ={CALIBRATION_D_SIGMA})")
    print(f"   pp:    pp_true = {CALIBRATION_PP_A} + {CALIBRATION_PP_B} × pp_llm (σ={CALIBRATION_PP_SIGMA})")
    print("=" * 70)


def get_mapping_config() -> Dict:
    """Get mapping configuration for audit trail."""
    return {
        "version": MAPPING_VERSION,
        "d_to_theta_knots": D_TO_THETA_KNOTS,
        "pp_to_theta_knots": PP_TO_THETA_KNOTS,
        "calibration": {
            "d": {
                "a": CALIBRATION_D_A,
                "b": CALIBRATION_D_B,
                "sigma": CALIBRATION_D_SIGMA
            },
            "pp": {
                "a": CALIBRATION_PP_A,
                "b": CALIBRATION_PP_B,
                "sigma": CALIBRATION_PP_SIGMA
            }
        }
    }


# =============================================================================
# CLI
# =============================================================================

def demo():
    """Run mapping demo."""
    print("\n" + "=" * 70)
    print("THETA MAPPING DEMO")
    print("=" * 70)

    # Example: 6 mixed parameters
    alpha_specs = [
        {"type": "d",  "llm_hat": 0.70, "eu_llm": 0.12, "name": "α_Awareness"},
        {"type": "d",  "llm_hat": 0.55, "eu_llm": 0.10, "name": "α_Willingness"},
        {"type": "pp", "llm_hat": 25.0, "eu_llm": 6.0,  "name": "α_Default"},
        {"type": "d",  "llm_hat": 0.80, "eu_llm": 0.10, "name": "α_Trigger"},
        {"type": "pp", "llm_hat": 10.0, "eu_llm": 5.0,  "name": "α_Reminder"},
        {"type": "d",  "llm_hat": 0.60, "eu_llm": 0.11, "name": "α_Action"},
    ]

    print("\n📋 INPUT: LLM Estimates (gemischt d und pp)")
    for sp in alpha_specs:
        print(f"   {sp.get('name', '?')}: {sp['type']} = {sp['llm_hat']} ± {sp['eu_llm']}")

    # Build alpha vector
    alpha_hat, alpha_eu = build_alpha_theta(alpha_specs)

    # Report
    print_mapping_report(alpha_specs, alpha_hat, alpha_eu)

    # Show for R-Score integration
    print("\n📊 FÜR R-SCORE")
    print(f"   alpha_hat = {np.round(alpha_hat, 3).tolist()}")
    print(f"   alpha_eu  = {np.round(alpha_eu, 3).tolist()}")

    return alpha_hat, alpha_eu


def main():
    parser = argparse.ArgumentParser(
        description="Theta Mapping: d/SMD und pp → 0-1 Skala",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Pipeline: LLM → Kalibration → Piecewise Mapping → θ ∈ [0,1]

Beispiel:
  python theta_mapping.py --demo
  python theta_mapping.py --d 0.70 --eu 0.12
  python theta_mapping.py --pp 25.0 --eu 6.0
        """
    )

    parser.add_argument("--demo", action="store_true",
                        help="Run demo with example parameters")
    parser.add_argument("--d", type=float,
                        help="d/SMD LLM estimate")
    parser.add_argument("--pp", type=float,
                        help="pp LLM estimate")
    parser.add_argument("--eu", type=float,
                        help="Elicitation uncertainty")
    parser.add_argument("--config", action="store_true",
                        help="Show mapping configuration (audit trail)")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON")

    args = parser.parse_args()

    if args.demo:
        demo()
    elif args.config:
        config = get_mapping_config()
        print(json.dumps(config, indent=2))
    elif args.d is not None and args.eu is not None:
        theta_hat, theta_eu = mc_map_d(args.d, args.eu)
        if args.json:
            print(json.dumps({
                "input": {"type": "d", "llm_hat": args.d, "eu_llm": args.eu},
                "output": {"theta_hat": round(theta_hat, 4), "theta_eu": round(theta_eu, 4)}
            }, indent=2))
        else:
            print(f"\nInput: d_llm = {args.d} ± {args.eu}")
            print(f"Calibrated: d_true = {calibrate_d(args.d):.3f}")
            print(f"Mapped: θ = {theta_hat:.3f} ± {theta_eu:.3f}")
    elif args.pp is not None and args.eu is not None:
        theta_hat, theta_eu = mc_map_pp(args.pp, args.eu)
        if args.json:
            print(json.dumps({
                "input": {"type": "pp", "llm_hat": args.pp, "eu_llm": args.eu},
                "output": {"theta_hat": round(theta_hat, 4), "theta_eu": round(theta_eu, 4)}
            }, indent=2))
        else:
            print(f"\nInput: pp_llm = {args.pp} ± {args.eu}")
            print(f"Calibrated: pp_true = {calibrate_pp(args.pp):.3f}")
            print(f"Mapped: θ = {theta_hat:.3f} ± {theta_eu:.3f}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
