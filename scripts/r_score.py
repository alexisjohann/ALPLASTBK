#!/usr/bin/env python3
"""
R-Score: Relevanz-/Priorisierungs-Score
=======================================

Berechnet den R-Score für Interventions-Design:

    R(a,K) = Σαᵢ + γ·‖a‖·‖K‖

Komponenten:
- αᵢ: kalibrierte Parameter (Fit/Match), mit Unsicherheit (EU)
- γ: kalibrierte Komplementarität/Interaktion, mit Unsicherheit
- ‖a‖, ‖K‖: exogen definierte Normen (Design-/Kontext-"Größe"), fix

WICHTIG: R ist ein Relevanz-/Priorisierungs-Score, kein kausaler Effekt.

Usage:
    python r_score.py --demo
    python r_score.py --alpha 0.62,0.58,0.71 --alpha-eu 0.08,0.07,0.06 \
                      --gamma 0.18 --gamma-eu 0.10 \
                      --norm-a 2.15 --norm-k 2.45

Author: EBF Framework
Date: 2025-01-13
Protocol: HHH-R-SCORE-1
"""

import numpy as np
import json
import argparse
from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict
from pathlib import Path


@dataclass
class RScoreResult:
    """Result of R-Score Monte Carlo calculation."""
    R_mean: float
    R_median: float
    R_std: float
    R_ci95: Tuple[float, float]
    R_ci80: Tuple[float, float]

    # Decision metrics
    prob_gt_threshold: Dict[float, float]  # P(R > T) for various thresholds

    # Components
    alpha_contribution: float  # E[Σαᵢ]
    gamma_contribution: float  # E[γ·‖a‖·‖K‖]

    # Metadata
    n_samples: int
    n_alpha: int
    norm_a: float
    norm_k: float

    def to_dict(self) -> Dict:
        return {
            "R_mean": round(self.R_mean, 4),
            "R_median": round(self.R_median, 4),
            "R_std": round(self.R_std, 4),
            "R_ci95": [round(self.R_ci95[0], 4), round(self.R_ci95[1], 4)],
            "R_ci80": [round(self.R_ci80[0], 4), round(self.R_ci80[1], 4)],
            "prob_gt_threshold": {str(k): round(v, 4) for k, v in self.prob_gt_threshold.items()},
            "components": {
                "alpha_contribution": round(self.alpha_contribution, 4),
                "gamma_contribution": round(self.gamma_contribution, 4)
            },
            "metadata": {
                "n_samples": self.n_samples,
                "n_alpha": self.n_alpha,
                "norm_a": self.norm_a,
                "norm_k": self.norm_k
            }
        }

    def decision(self, threshold: float = 6.0) -> str:
        """
        Generate GO/NO-GO/PILOT decision.

        Rules:
        - P(R > T) < 5%  → NO-GO
        - P(R > T) 5-25% → PILOT
        - P(R > T) > 25% → GO
        """
        prob = self.prob_gt_threshold.get(threshold, 0)

        if prob < 0.05:
            return "NO-GO"
        elif prob < 0.25:
            return "PILOT"
        else:
            return "GO"


def r_score_mc(
    alpha_hat: np.ndarray,
    alpha_eu: np.ndarray,
    gamma_hat: float,
    gamma_eu: float,
    norm_a: float,
    norm_k: float,
    n: int = 10000,
    seed: int = 42,
    thresholds: List[float] = None
) -> RScoreResult:
    """
    Monte-Carlo R-Score calculation.

    R(a,K) = Σαᵢ + γ·‖a‖·‖K‖

    Args:
        alpha_hat: Array of calibrated α parameters (point estimates)
        alpha_eu: Array of α elicitation uncertainties
        gamma_hat: Calibrated γ (complementarity) point estimate
        gamma_eu: γ elicitation uncertainty
        norm_a: Design norm ‖a‖ (fixed by design)
        norm_k: Context norm ‖K‖ (fixed by context)
        n: Number of Monte Carlo samples
        seed: Random seed for reproducibility
        thresholds: List of thresholds for P(R > T) calculation

    Returns:
        RScoreResult with full uncertainty quantification
    """
    if thresholds is None:
        thresholds = [3.0, 4.0, 5.0, 6.0, 7.0, 8.0]

    rng = np.random.default_rng(seed)

    # Draw from parameter distributions
    alpha_draws = rng.normal(alpha_hat, alpha_eu, size=(n, len(alpha_hat)))
    gamma_draws = rng.normal(gamma_hat, gamma_eu, size=n)

    # Compute R for each draw
    alpha_sum = alpha_draws.sum(axis=1)
    gamma_term = gamma_draws * norm_a * norm_k
    R = alpha_sum + gamma_term

    # Compute statistics
    R_mean = float(R.mean())
    R_median = float(np.median(R))
    R_std = float(R.std())
    R_ci95 = (float(np.percentile(R, 2.5)), float(np.percentile(R, 97.5)))
    R_ci80 = (float(np.percentile(R, 10)), float(np.percentile(R, 90)))

    # Threshold probabilities
    prob_gt_threshold = {t: float((R > t).mean()) for t in thresholds}

    # Component contributions
    alpha_contribution = float(alpha_sum.mean())
    gamma_contribution = float(gamma_term.mean())

    return RScoreResult(
        R_mean=R_mean,
        R_median=R_median,
        R_std=R_std,
        R_ci95=R_ci95,
        R_ci80=R_ci80,
        prob_gt_threshold=prob_gt_threshold,
        alpha_contribution=alpha_contribution,
        gamma_contribution=gamma_contribution,
        n_samples=n,
        n_alpha=len(alpha_hat),
        norm_a=norm_a,
        norm_k=norm_k
    )


def calibrate_alpha_for_rscore(
    theta_llm: float,
    eu_llm: float,
    scale: str = "d"
) -> Tuple[float, float]:
    """
    Calibrate a single α parameter using scale-specific calibration.

    Args:
        theta_llm: Raw LLMMC estimate
        eu_llm: Elicitation uncertainty
        scale: "d" for d/SMD, "pp" for percentage points

    Returns:
        (alpha_calibrated, alpha_eu_calibrated)
    """
    if scale == "d":
        # d/SMD calibration: θ_true = 0.03 + 0.79 × θ_llm
        a, b, sigma_model = 0.03, 0.79, 0.06
    elif scale == "pp":
        # pp calibration: pp_true = -0.48 + 1.007 × pp_llm
        # For 0-1 scale, apply pp/50 mapping
        a, b, sigma_model = -0.48/50, 1.007, 3.54/50
    else:
        raise ValueError(f"Unknown scale: {scale}")

    alpha_cal = max(0, min(1, a + b * theta_llm))
    alpha_eu = np.sqrt((b * eu_llm)**2 + sigma_model**2)

    return alpha_cal, alpha_eu


def print_rscore_report(result: RScoreResult, threshold: float = 6.0):
    """Print formatted R-Score report."""
    decision = result.decision(threshold)
    decision_emoji = {"GO": "🟢", "PILOT": "🟡", "NO-GO": "🔴"}[decision]

    print("\n" + "=" * 60)
    print("R-SCORE REPORT")
    print("=" * 60)

    print(f"\n📊 R-SCORE DISTRIBUTION")
    print(f"   E[R] = {result.R_mean:.3f}")
    print(f"   Median = {result.R_median:.3f}")
    print(f"   Std = {result.R_std:.3f}")
    print(f"   80% CI: [{result.R_ci80[0]:.3f}, {result.R_ci80[1]:.3f}]")
    print(f"   95% CI: [{result.R_ci95[0]:.3f}, {result.R_ci95[1]:.3f}]")

    print(f"\n📈 KOMPONENTEN")
    print(f"   Σαᵢ = {result.alpha_contribution:.3f} ({result.n_alpha} Parameter)")
    print(f"   γ·‖a‖·‖K‖ = {result.gamma_contribution:.3f}")
    print(f"   ‖a‖ = {result.norm_a:.2f}, ‖K‖ = {result.norm_k:.2f}")

    print(f"\n🎯 SCHWELLEN-WAHRSCHEINLICHKEITEN")
    for t, p in sorted(result.prob_gt_threshold.items()):
        marker = " ← Entscheidungs-Schwelle" if t == threshold else ""
        print(f"   P(R > {t:.1f}) = {p:.1%}{marker}")

    print(f"\n{'='*60}")
    print(f"{decision_emoji} ENTSCHEIDUNG: {decision}")
    print(f"   (basierend auf P(R > {threshold}) = {result.prob_gt_threshold[threshold]:.1%})")
    print(f"\n   Regel:")
    print(f"   • P < 5%    → NO-GO")
    print(f"   • 5-25%     → PILOT")
    print(f"   • > 25%     → GO")
    print("=" * 60)


def demo():
    """Run R-Score demo with example parameters."""
    print("\n" + "=" * 60)
    print("R-SCORE DEMO")
    print("=" * 60)

    print("\n📋 BEISPIEL-PARAMETER (kalibriert)")

    # Example: 6 intervention components (calibrated)
    alpha_hat = np.array([0.62, 0.58, 0.71, 0.65, 0.60, 0.67])
    alpha_eu = np.array([0.08, 0.07, 0.06, 0.07, 0.09, 0.08])

    # Complementarity (calibrated)
    gamma_hat = 0.18
    gamma_eu = 0.10

    # Design and context norms (fixed)
    norm_a = 2.15
    norm_k = 2.45

    print(f"\n   α = {alpha_hat}")
    print(f"   EU(α) = {alpha_eu}")
    print(f"   γ = {gamma_hat} ± {gamma_eu}")
    print(f"   ‖a‖ = {norm_a}, ‖K‖ = {norm_k}")

    # Calculate R-Score
    result = r_score_mc(
        alpha_hat, alpha_eu,
        gamma_hat, gamma_eu,
        norm_a, norm_k,
        n=50000
    )

    # Print report
    print_rscore_report(result, threshold=6.0)

    # JSON output
    print("\n📄 JSON OUTPUT")
    print(json.dumps(result.to_dict(), indent=2))

    return result


def main():
    parser = argparse.ArgumentParser(
        description="R-Score: Relevanz-/Priorisierungs-Score",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Formel: R(a,K) = Σαᵢ + γ·‖a‖·‖K‖

Entscheidungsregel (bei Schwelle T):
  P(R > T) < 5%   → NO-GO
  P(R > T) 5-25%  → PILOT
  P(R > T) > 25%  → GO

Beispiel:
  python r_score.py --demo
  python r_score.py --alpha 0.62,0.58,0.71 --alpha-eu 0.08,0.07,0.06 \\
                    --gamma 0.18 --gamma-eu 0.10 \\
                    --norm-a 2.15 --norm-k 2.45 --threshold 6.0
        """
    )

    parser.add_argument("--demo", action="store_true",
                        help="Run demo with example parameters")
    parser.add_argument("--alpha", type=str,
                        help="Comma-separated α values")
    parser.add_argument("--alpha-eu", type=str,
                        help="Comma-separated α uncertainties")
    parser.add_argument("--gamma", type=float,
                        help="γ (complementarity) value")
    parser.add_argument("--gamma-eu", type=float,
                        help="γ uncertainty")
    parser.add_argument("--norm-a", type=float, default=1.0,
                        help="Design norm ‖a‖")
    parser.add_argument("--norm-k", type=float, default=1.0,
                        help="Context norm ‖K‖")
    parser.add_argument("--threshold", type=float, default=6.0,
                        help="Decision threshold T")
    parser.add_argument("--n-samples", type=int, default=10000,
                        help="Monte Carlo samples")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON only")

    args = parser.parse_args()

    if args.demo:
        demo()
    elif args.alpha and args.gamma is not None:
        alpha_hat = np.array([float(x) for x in args.alpha.split(",")])
        alpha_eu = np.array([float(x) for x in args.alpha_eu.split(",")]) if args.alpha_eu else np.ones_like(alpha_hat) * 0.1

        result = r_score_mc(
            alpha_hat, alpha_eu,
            args.gamma, args.gamma_eu or 0.1,
            args.norm_a, args.norm_k,
            n=args.n_samples
        )

        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            print_rscore_report(result, args.threshold)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
