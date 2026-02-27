#!/usr/bin/env python3
"""
Production Calibration for d/SMD Scale
=======================================

Scale-local calibration for Cohen's d and SMD effect sizes.
Based on calibration_d_v1.json (n=5 Tier-1/2 anchors).

Usage:
    from calibrate_d_smd import calibrate_d_smd

    result = calibrate_d_smd(theta_llm=0.65, eu_llm=0.08)
    print(result)

Or from CLI:
    python calibrate_d_smd.py --theta 0.65 --eu 0.08

Author: EBF Framework
Date: 2025-01-13
Version: calibration_d_v1
"""

import json
import argparse
from pathlib import Path
from dataclasses import dataclass
from typing import Tuple
import math


# Calibration parameters from calibration_d_v1.json
CALIBRATION_A = 0.03
CALIBRATION_B = 0.79
SIGMA_MODEL = 0.06


@dataclass
class CalibratedEstimate:
    """Result of d/SMD calibration."""
    theta_raw: float
    theta_calibrated: float
    sigma_calibrated: float
    ci_95: Tuple[float, float]
    tier: int
    tier_note: str
    scale: str

    def __repr__(self) -> str:
        return (
            f"CalibratedEstimate(\n"
            f"  θ_raw = {self.theta_raw:.3f}\n"
            f"  θ_cal = {self.theta_calibrated:.3f} ± {self.sigma_calibrated:.3f}\n"
            f"  95% CI: [{self.ci_95[0]:.3f}, {self.ci_95[1]:.3f}]\n"
            f"  Tier: {self.tier} ({self.tier_note})\n"
            f")"
        )

    def to_dict(self) -> dict:
        return {
            "estimate": round(self.theta_calibrated, 4),
            "se": round(self.sigma_calibrated, 4),
            "ci_95": [round(self.ci_95[0], 4), round(self.ci_95[1], 4)],
            "tier": self.tier,
            "tier_note": self.tier_note,
            "scale": self.scale,
            "raw_llm": round(self.theta_raw, 4),
            "calibration": "d_v1"
        }


def calibrate_d_smd(
    theta_llm: float,
    eu_llm: float,
    a: float = CALIBRATION_A,
    b: float = CALIBRATION_B,
    sigma_model: float = SIGMA_MODEL
) -> CalibratedEstimate:
    """
    Calibrate a d/SMD-based LLMMC estimate.

    Applies the production calibration:
        θ_true ≈ 0.03 + 0.79 × θ_llm

    Args:
        theta_llm: Raw LLMMC estimate (0-1 scale)
        eu_llm: Elicitation uncertainty from LLMMC
        a: Intercept (default: 0.03)
        b: Slope (default: 0.79)
        sigma_model: Model misspecification (default: 0.06)

    Returns:
        CalibratedEstimate with calibrated values and uncertainty

    Note:
        Only valid for d/SMD-based parameters!
        For pp-based parameters, use separate workflow (pending calibration).
    """
    # Level calibration (CAL-2)
    theta_cal = max(0.0, min(1.0, a + b * theta_llm))

    # Uncertainty calibration (CAL-3)
    sigma_cal = math.sqrt((b * eu_llm) ** 2 + sigma_model ** 2)

    # 95% CI
    ci_lower = max(0.0, theta_cal - 1.96 * sigma_cal)
    ci_upper = min(1.0, theta_cal + 1.96 * sigma_cal)

    return CalibratedEstimate(
        theta_raw=theta_llm,
        theta_calibrated=theta_cal,
        sigma_calibrated=sigma_cal,
        ci_95=(ci_lower, ci_upper),
        tier=3,
        tier_note="calibrated on Tier-1/2 anchors (n=5, d/SMD scale)",
        scale="d/SMD"
    )


def load_calibration_params() -> dict:
    """Load calibration parameters from JSON file."""
    path = Path(__file__).parent.parent / "data" / "calibration" / "calibration_d_v1.json"
    with open(path, 'r') as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(
        description="Calibrate d/SMD-based LLMMC estimates",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python calibrate_d_smd.py --theta 0.65 --eu 0.08
    python calibrate_d_smd.py --theta 0.45 --eu 0.10 --json

Note: Only valid for d/SMD scale. Not applicable to pp-based parameters.
        """
    )

    parser.add_argument("--theta", type=float, required=True,
                        help="Raw LLMMC estimate (θ_llm)")
    parser.add_argument("--eu", type=float, required=True,
                        help="Elicitation uncertainty (EU_llm)")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON")
    parser.add_argument("--show-params", action="store_true",
                        help="Show calibration parameters")

    args = parser.parse_args()

    if args.show_params:
        params = load_calibration_params()
        print(json.dumps(params, indent=2))
        return

    result = calibrate_d_smd(args.theta, args.eu)

    if args.json:
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print("\n" + "=" * 50)
        print("d/SMD Calibration (calibration_d_v1)")
        print("=" * 50)
        print(f"\nInput:")
        print(f"  θ_llm = {args.theta:.3f}")
        print(f"  EU_llm = {args.eu:.3f}")
        print(f"\nCalibration formula:")
        print(f"  θ_cal = {CALIBRATION_A:.2f} + {CALIBRATION_B:.2f} × θ_llm")
        print(f"\nResult:")
        print(result)
        print("=" * 50)


if __name__ == "__main__":
    main()
