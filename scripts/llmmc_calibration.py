#!/usr/bin/env python3
"""
LLMMC Calibration Module
========================

Implements the calibration methodology from HHH Appendix (Section: LLMMC-Kalibrierung).

Calibrates Tier-3 (LLM-based) estimates against Tier-1/2 (empirical) anchors.

Components:
- CAL-1: Calibration anchor requirements
- CAL-2: Level calibration (bias & scaling)
- CAL-3: Uncertainty calibration (coverage)
- CAL-4: Evidence-weighted shrinkage
- HHH-CAL-1: LOO cross-validation

Usage:
    calibrator = LLMMCCalibrator()
    calibrator.add_anchor("Default_Action", theta_t12=0.85, se_t12=0.04,
                          theta_llm=0.91, eu_llm=0.05, source="Madrian & Shea 2001")
    calibrator.fit()
    result = calibrator.calibrate(theta_llm=0.87, eu_llm=0.06)

Author: EBF Framework
Date: 2025-01-13
Protocol: HHH-LLMMC-1, HHH-CAL-1
"""

import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from scipy import stats
from sklearn.isotonic import IsotonicRegression
import warnings


@dataclass
class CalibrationAnchor:
    """Single calibration anchor point."""
    name: str
    theta_t12: float  # Tier-1/2 reference value
    se_t12: float     # Tier-1/2 standard error
    theta_llm: float  # LLM estimate
    eu_llm: float     # LLM elicitation uncertainty
    source: str       # Citation

    @property
    def weight(self) -> float:
        """Inverse variance weight (CAL-2)."""
        return 1.0 / (self.se_t12**2 + self.eu_llm**2)


@dataclass
class CalibrationResult:
    """Result of calibrated estimation."""
    theta_raw: float           # Raw LLM estimate
    theta_calibrated: float    # After level calibration
    theta_final: float         # After shrinkage
    sigma_calibrated: float    # Calibrated uncertainty
    sigma_final: float         # Final uncertainty after shrinkage
    ci_95: Tuple[float, float] # 95% confidence interval
    shrinkage_factor: float    # Lambda (0 = full shrinkage, 1 = no shrinkage)
    tier: int = 3
    tier_note: str = ""

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON export."""
        return {
            "estimate": round(self.theta_final, 4),
            "se": round(self.sigma_final, 4),
            "ci_95": [round(self.ci_95[0], 4), round(self.ci_95[1], 4)],
            "tier": self.tier,
            "tier_note": self.tier_note,
            "calibration_details": {
                "raw_llm": round(self.theta_raw, 4),
                "level_calibrated": round(self.theta_calibrated, 4),
                "shrinkage_factor": round(self.shrinkage_factor, 4)
            }
        }


@dataclass
class LOOResult:
    """Leave-one-out cross-validation result."""
    mae: float
    rmse: float
    coverage_95: float
    spearman_rho: float
    residuals: List[float]
    predictions: List[float]

    def is_acceptable(self) -> bool:
        """Check if calibration meets minimum standards."""
        return (self.mae < 0.12 and
                self.rmse < 0.15 and
                0.85 <= self.coverage_95 <= 0.98 and
                self.spearman_rho > 0.70)

    def is_good(self) -> bool:
        """Check if calibration meets good standards."""
        return (self.mae < 0.08 and
                self.rmse < 0.10 and
                0.90 <= self.coverage_95 <= 0.96 and
                self.spearman_rho > 0.85)


class LLMMCCalibrator:
    """
    LLMMC Calibration System.

    Implements the full calibration pipeline:
    1. Collect calibration anchors (Tier-1/2 + Tier-3 pairs)
    2. Fit level calibration (a, b parameters)
    3. Estimate sigma_model for coverage calibration
    4. Apply shrinkage for uncertain estimates
    5. Validate via LOO cross-validation

    Axioms:
    - CAL-1: Calibration anchor requirements (n >= 10)
    - CAL-2: Linear calibration transformation
    - CAL-3: Coverage calibration
    - CAL-4: Evidence-weighted shrinkage
    """

    def __init__(self,
                 min_anchors: int = 10,
                 use_isotonic: bool = False,
                 shrinkage_prior: float = 0.5):
        """
        Initialize calibrator.

        Args:
            min_anchors: Minimum number of calibration anchors (CAL-1)
            use_isotonic: Use isotonic regression instead of linear
            shrinkage_prior: Prior mean for shrinkage (default: 0.5 = agnostic)
        """
        self.min_anchors = min_anchors
        self.use_isotonic = use_isotonic
        self.shrinkage_prior = shrinkage_prior

        self.anchors: List[CalibrationAnchor] = []
        self.a: Optional[float] = None  # Intercept
        self.b: Optional[float] = None  # Slope
        self.sigma_model: Optional[float] = None  # Model misspecification
        self.tau: Optional[float] = None  # Signal variance for shrinkage
        self.isotonic_model: Optional[IsotonicRegression] = None
        self._fitted = False

    def add_anchor(self, name: str, theta_t12: float, se_t12: float,
                   theta_llm: float, eu_llm: float, source: str) -> None:
        """
        Add a calibration anchor point.

        Args:
            name: Parameter name (e.g., "alpha_Default_Action")
            theta_t12: Tier-1/2 empirical value
            se_t12: Standard error of Tier-1/2 estimate
            theta_llm: LLM estimate from LLMMC protocol
            eu_llm: Elicitation uncertainty from LLMMC
            source: Citation (e.g., "Madrian & Shea 2001")
        """
        anchor = CalibrationAnchor(
            name=name,
            theta_t12=theta_t12,
            se_t12=se_t12,
            theta_llm=theta_llm,
            eu_llm=eu_llm,
            source=source
        )
        self.anchors.append(anchor)
        self._fitted = False

    def add_anchors_from_dict(self, anchors: List[Dict]) -> None:
        """
        Add multiple anchors from list of dictionaries.

        Args:
            anchors: List of dicts with keys: name, theta_t12, se_t12,
                     theta_llm, eu_llm, source
        """
        for a in anchors:
            self.add_anchor(**a)

    def fit(self) -> None:
        """
        Fit calibration model on anchors.

        Implements:
        - CAL-2: Level calibration (weighted linear regression)
        - CAL-3: Coverage calibration (sigma_model estimation)
        - CAL-4: Shrinkage parameter (tau estimation)

        Raises:
            ValueError: If fewer than min_anchors available
        """
        n = len(self.anchors)
        if n < self.min_anchors:
            raise ValueError(
                f"CAL-1 violation: Need at least {self.min_anchors} anchors, "
                f"got {n}. Add more Tier-1/2 reference points."
            )

        # Extract arrays
        theta_t12 = np.array([a.theta_t12 for a in self.anchors])
        theta_llm = np.array([a.theta_llm for a in self.anchors])
        weights = np.array([a.weight for a in self.anchors])

        if self.use_isotonic:
            # Isotonic regression (monotonic, robust)
            self.isotonic_model = IsotonicRegression(
                y_min=0.0, y_max=1.0, out_of_bounds='clip'
            )
            self.isotonic_model.fit(theta_llm, theta_t12, sample_weight=weights)
            theta_pred = self.isotonic_model.predict(theta_llm)
            self.a = 0  # Not used for isotonic
            self.b = 1  # Not used for isotonic
        else:
            # Weighted linear regression (CAL-2)
            # theta_t12 = a + b * theta_llm
            W = np.diag(weights)
            X = np.column_stack([np.ones(n), theta_llm])

            # Weighted least squares
            XtWX = X.T @ W @ X
            XtWy = X.T @ W @ theta_t12
            beta = np.linalg.solve(XtWX, XtWy)

            self.a = beta[0]
            self.b = beta[1]

            theta_pred = self.a + self.b * theta_llm

        # Residuals for sigma_model (CAL-3)
        residuals = theta_t12 - theta_pred
        self.sigma_model = np.std(residuals, ddof=2)  # df correction for a, b

        # Signal variance for shrinkage (CAL-4)
        # Use variance of calibrated predictions
        self.tau = np.std(theta_pred)

        self._fitted = True

    def _apply_level_calibration(self, theta_llm: float) -> float:
        """Apply level calibration (CAL-2)."""
        if self.use_isotonic and self.isotonic_model is not None:
            return float(self.isotonic_model.predict([[theta_llm]])[0])
        else:
            return np.clip(self.a + self.b * theta_llm, 0, 1)

    def _apply_uncertainty_calibration(self, eu_llm: float) -> float:
        """Apply uncertainty calibration (CAL-3)."""
        b_effective = self.b if not self.use_isotonic else 1.0
        return np.sqrt((b_effective * eu_llm)**2 + self.sigma_model**2)

    def _apply_shrinkage(self, theta_cal: float, sigma_cal: float
                        ) -> Tuple[float, float, float]:
        """
        Apply evidence-weighted shrinkage (CAL-4).

        Returns:
            Tuple of (theta_final, sigma_final, lambda)
        """
        # Shrinkage factor
        lam = self.tau**2 / (self.tau**2 + sigma_cal**2)

        # Shrunk estimate
        theta_final = lam * theta_cal + (1 - lam) * self.shrinkage_prior

        # Shrunk uncertainty
        sigma_final = lam * sigma_cal

        return theta_final, sigma_final, lam

    def calibrate(self, theta_llm: float, eu_llm: float,
                  apply_shrinkage: bool = True) -> CalibrationResult:
        """
        Calibrate a new LLM estimate.

        Args:
            theta_llm: Raw LLM estimate from LLMMC
            eu_llm: Elicitation uncertainty from LLMMC
            apply_shrinkage: Whether to apply shrinkage (default: True)

        Returns:
            CalibrationResult with calibrated estimate and uncertainty

        Raises:
            RuntimeError: If calibrator not fitted
        """
        if not self._fitted:
            raise RuntimeError("Calibrator not fitted. Call fit() first.")

        # Level calibration (CAL-2)
        theta_cal = self._apply_level_calibration(theta_llm)

        # Uncertainty calibration (CAL-3)
        sigma_cal = self._apply_uncertainty_calibration(eu_llm)

        # Shrinkage (CAL-4)
        if apply_shrinkage:
            theta_final, sigma_final, lam = self._apply_shrinkage(theta_cal, sigma_cal)
        else:
            theta_final = theta_cal
            sigma_final = sigma_cal
            lam = 1.0

        # Confidence interval
        ci_lower = max(0, theta_final - 1.96 * sigma_final)
        ci_upper = min(1, theta_final + 1.96 * sigma_final)

        return CalibrationResult(
            theta_raw=theta_llm,
            theta_calibrated=theta_cal,
            theta_final=theta_final,
            sigma_calibrated=sigma_cal,
            sigma_final=sigma_final,
            ci_95=(ci_lower, ci_upper),
            shrinkage_factor=lam,
            tier=3,
            tier_note=f"calibrated on Tier-1/2 anchors (n={len(self.anchors)})"
        )

    def loo_cross_validation(self) -> LOOResult:
        """
        Perform Leave-One-Out cross-validation (HHH-CAL-1).

        Returns:
            LOOResult with MAE, RMSE, coverage, and Spearman rho
        """
        if len(self.anchors) < self.min_anchors:
            raise ValueError(f"Need at least {self.min_anchors} anchors for LOO-CV")

        n = len(self.anchors)
        predictions = []
        residuals = []
        in_ci = []
        true_values = []

        for i in range(n):
            # Leave out anchor i
            loo_anchors = [a for j, a in enumerate(self.anchors) if j != i]
            test_anchor = self.anchors[i]

            # Fit on n-1
            loo_calibrator = LLMMCCalibrator(
                min_anchors=max(3, self.min_anchors - 2),
                use_isotonic=self.use_isotonic,
                shrinkage_prior=self.shrinkage_prior
            )
            for a in loo_anchors:
                loo_calibrator.add_anchor(
                    a.name, a.theta_t12, a.se_t12,
                    a.theta_llm, a.eu_llm, a.source
                )

            try:
                loo_calibrator.fit()
            except ValueError:
                warnings.warn(f"Could not fit LOO fold {i}, skipping")
                continue

            # Predict for held-out
            result = loo_calibrator.calibrate(
                test_anchor.theta_llm,
                test_anchor.eu_llm,
                apply_shrinkage=False  # No shrinkage for fair comparison
            )

            pred = result.theta_calibrated
            true = test_anchor.theta_t12
            resid = true - pred

            predictions.append(pred)
            true_values.append(true)
            residuals.append(resid)

            # Coverage check
            in_interval = (true >= result.ci_95[0]) and (true <= result.ci_95[1])
            in_ci.append(in_interval)

        # Compute metrics
        residuals = np.array(residuals)
        predictions = np.array(predictions)
        true_values = np.array(true_values)

        mae = np.mean(np.abs(residuals))
        rmse = np.sqrt(np.mean(residuals**2))
        coverage = np.mean(in_ci)
        spearman_rho, _ = stats.spearmanr(predictions, true_values)

        return LOOResult(
            mae=mae,
            rmse=rmse,
            coverage_95=coverage,
            spearman_rho=spearman_rho,
            residuals=list(residuals),
            predictions=list(predictions)
        )

    def get_calibration_params(self) -> Dict:
        """Get fitted calibration parameters."""
        if not self._fitted:
            raise RuntimeError("Calibrator not fitted.")

        return {
            "a": self.a,
            "b": self.b,
            "sigma_model": self.sigma_model,
            "tau": self.tau,
            "n_anchors": len(self.anchors),
            "use_isotonic": self.use_isotonic
        }

    def summary(self) -> str:
        """Generate human-readable summary."""
        if not self._fitted:
            return f"LLMMCCalibrator (not fitted, {len(self.anchors)} anchors)"

        params = self.get_calibration_params()
        loo = self.loo_cross_validation()

        lines = [
            "=" * 60,
            "LLMMC Calibration Summary",
            "=" * 60,
            f"Anchors: n = {params['n_anchors']}",
            f"Method: {'Isotonic' if params['use_isotonic'] else 'Linear'}",
            "",
            "Level Calibration (CAL-2):",
            f"  θ_cal = {params['a']:.4f} + {params['b']:.4f} × θ_LLM",
            "",
            "Uncertainty Calibration (CAL-3):",
            f"  σ_model = {params['sigma_model']:.4f}",
            "",
            "Shrinkage (CAL-4):",
            f"  τ = {params['tau']:.4f}",
            f"  Prior = {self.shrinkage_prior}",
            "",
            "LOO Cross-Validation (HHH-CAL-1):",
            f"  MAE = {loo.mae:.4f} {'✓' if loo.mae < 0.12 else '✗'}",
            f"  RMSE = {loo.rmse:.4f} {'✓' if loo.rmse < 0.15 else '✗'}",
            f"  Coverage_95 = {loo.coverage_95:.2%} {'✓' if 0.85 <= loo.coverage_95 <= 0.98 else '✗'}",
            f"  Spearman ρ = {loo.spearman_rho:.4f} {'✓' if loo.spearman_rho > 0.70 else '✗'}",
            "",
            f"Overall: {'ACCEPTABLE' if loo.is_acceptable() else 'NEEDS IMPROVEMENT'}",
            f"         {'GOOD' if loo.is_good() else ''}",
            "=" * 60
        ]

        return "\n".join(lines)


# =============================================================================
# Example Usage
# =============================================================================

def create_example_calibration_set() -> List[Dict]:
    """
    Create example calibration set based on behavioral economics literature.

    These are illustrative values - in practice, extract from actual studies.
    """
    return [
        # Defaults
        {"name": "alpha_Default_Action", "theta_t12": 0.85, "se_t12": 0.04,
         "theta_llm": 0.91, "eu_llm": 0.05, "source": "Madrian & Shea 2001"},
        {"name": "alpha_Default_Trigger", "theta_t12": 0.78, "se_t12": 0.05,
         "theta_llm": 0.85, "eu_llm": 0.06, "source": "Johnson & Goldstein 2003"},

        # Social Norms
        {"name": "alpha_Social_Awareness", "theta_t12": 0.35, "se_t12": 0.06,
         "theta_llm": 0.42, "eu_llm": 0.09, "source": "Allcott 2011"},
        {"name": "alpha_Social_Action", "theta_t12": 0.28, "se_t12": 0.07,
         "theta_llm": 0.38, "eu_llm": 0.10, "source": "Schultz et al 2007"},

        # Incentives
        {"name": "alpha_Incentive_Action", "theta_t12": 0.50, "se_t12": 0.08,
         "theta_llm": 0.58, "eu_llm": 0.11, "source": "Gneezy et al 2011"},
        {"name": "alpha_Incentive_Maint", "theta_t12": 0.32, "se_t12": 0.09,
         "theta_llm": 0.45, "eu_llm": 0.12, "source": "Charness & Gneezy 2009"},

        # Commitment
        {"name": "alpha_Commit_Maint", "theta_t12": 0.45, "se_t12": 0.07,
         "theta_llm": 0.52, "eu_llm": 0.10, "source": "Royer et al 2015"},
        {"name": "alpha_Commit_Action", "theta_t12": 0.38, "se_t12": 0.08,
         "theta_llm": 0.48, "eu_llm": 0.11, "source": "Milkman et al 2014"},

        # Feedback
        {"name": "alpha_Feedback_Action", "theta_t12": 0.42, "se_t12": 0.06,
         "theta_llm": 0.55, "eu_llm": 0.08, "source": "Hummel & Maedche 2019"},
        {"name": "alpha_Feedback_Maint", "theta_t12": 0.35, "se_t12": 0.07,
         "theta_llm": 0.48, "eu_llm": 0.09, "source": "Karlan et al 2016"},

        # Framing
        {"name": "alpha_Framing_Awareness", "theta_t12": 0.25, "se_t12": 0.08,
         "theta_llm": 0.35, "eu_llm": 0.12, "source": "Tversky & Kahneman 1981"},
        {"name": "alpha_Framing_Trigger", "theta_t12": 0.30, "se_t12": 0.09,
         "theta_llm": 0.42, "eu_llm": 0.13, "source": "Levin et al 1998"},

        # Gamma (interactions)
        {"name": "gamma_Default_Escalation", "theta_t12": 0.25, "se_t12": 0.10,
         "theta_llm": 0.31, "eu_llm": 0.14, "source": "Benartzi & Thaler 2013"},
        {"name": "gamma_Feedback_Social", "theta_t12": 0.18, "se_t12": 0.09,
         "theta_llm": 0.28, "eu_llm": 0.12, "source": "Schultz et al 2007"},
        {"name": "gamma_Incentive_Feedback", "theta_t12": -0.12, "se_t12": 0.11,
         "theta_llm": -0.05, "eu_llm": 0.15, "source": "Gneezy & Rustichini 2000"},
    ]


if __name__ == "__main__":
    # Demo
    print("LLMMC Calibration Demo")
    print("=" * 60)

    # Create calibrator
    calibrator = LLMMCCalibrator(min_anchors=10, use_isotonic=False)

    # Add calibration set
    anchors = create_example_calibration_set()
    calibrator.add_anchors_from_dict(anchors)
    print(f"Added {len(anchors)} calibration anchors")

    # Fit
    calibrator.fit()
    print("\nFitted calibration model")

    # Show summary
    print("\n" + calibrator.summary())

    # Calibrate a new parameter
    print("\n" + "=" * 60)
    print("Example: Calibrating a new parameter")
    print("=" * 60)

    # Raw LLM estimate
    theta_llm = 0.72
    eu_llm = 0.08

    result = calibrator.calibrate(theta_llm, eu_llm)

    print(f"\nRaw LLM estimate: {theta_llm:.3f} ± {eu_llm:.3f}")
    print(f"After level calibration: {result.theta_calibrated:.3f}")
    print(f"After shrinkage: {result.theta_final:.3f} ± {result.sigma_final:.3f}")
    print(f"95% CI: [{result.ci_95[0]:.3f}, {result.ci_95[1]:.3f}]")
    print(f"Shrinkage factor λ: {result.shrinkage_factor:.3f}")
    print(f"\nTier: {result.tier} ({result.tier_note})")

    print("\nJSON output:")
    import json
    print(json.dumps(result.to_dict(), indent=2))
