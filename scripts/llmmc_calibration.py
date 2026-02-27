#!/usr/bin/env python3
"""
LLMMC Calibration Module (v2.0)
================================

Implements the calibration methodology from Appendix AN (METHOD-LLMMC) and
Appendix III (Calibration Pipeline).

OPERATIONAL EPISTEMOLOGY (Appendix AN v2.0):
    An LLMMC prior is NOT "what the LLM thinks." It is the output of a validated
    measurement procedure (E1-E5) applied to a structured knowledge aggregation
    device. The legitimacy derives from the PROCEDURE, not from the DEVICE.

    The LLM is a MEASUREMENT INSTRUMENT with:
    - Known, characterizable systematic bias b(C, π)
    - Stochastic measurement error ε(τ)
    - A formal calibration procedure (CAL-1 through CAL-4)
    - Quantifiable measurement uncertainty (4-component decomposition)

Components:
- CAL-1: Calibration anchor requirements (n >= 10)
- CAL-2: Level calibration (bias & scaling via WLS)
- CAL-3: Uncertainty calibration (4-component: elicit + calib + model + context)
- CAL-4: Evidence-weighted shrinkage (decision-theoretic LINEX loss)
- HHH-CAL-1: LOO cross-validation
- PCT-CAL-1: PCT-informed priors (Tier 2.5)
- AN-DIAG: Anchor diagnostics (Cook's distance, leverage, studentized residuals)
- AN-BOUND: Bounded parameter treatment (logit/Fisher-z transforms)
- AN-HIER: Hierarchical Bayesian domain-level shrinkage

Five Operational Steps (E1-E5):
    E1: Structured Elicitation Design (parameter space, context, prompts)
    E2: Repeated Measurement (N >= 10 draws, perspective rotation, temperature schedule)
    E3: Statistical Aggregation (mean + elicitation variance)
    E4: Calibration (WLS against Tier-1/2 anchors)
    E5: Validation and Bounded Inference (bounds, shrinkage, uncertainty, LOO-CV)

Legitimate LLMMC Prior (LLP) Conditions:
    LLP-1: Reproducibility (consistent across runs)
    LLP-2: Calibration (LOO-CV: MAE < 0.12, Spearman ρ > 0.70, Coverage ∈ [0.85, 0.98])
    LLP-3: Bounded Uncertainty (σ_total computed, CI within parameter space)

Usage:
    calibrator = LLMMCCalibrator()
    calibrator.add_anchor("Default_Action", theta_t12=0.85, se_t12=0.04,
                          theta_llm=0.91, eu_llm=0.05, source="Madrian & Shea 2001")
    calibrator.fit()
    result = calibrator.calibrate(theta_llm=0.87, eu_llm=0.06)

    # PCT-informed calibration (Tier 2.5):
    from pct import transform_from_contexts
    pct_result = transform_from_contexts(2.5, anchor_psi, target_psi)
    result = calibrator.calibrate_with_pct(pct_result, eu_pct=0.10)

    # Anchor diagnostics:
    diags = calibrator.diagnose_anchors()
    for d in diags:
        if d.flagged:
            print(f"WARNING: Anchor {d.name} flagged (Cook's D={d.cooks_d:.3f})")

    # MC uncertainty propagation:
    mc_result = calibrator.mc_uncertainty_propagation(theta_llm=0.87, eu_llm=0.06)

Author: EBF Framework
Date: 2025-01-13 (v1.0), 2026-02-16 (v2.0)
Protocol: HHH-LLMMC-1, HHH-CAL-1, PCT-CAL-1, AN-DIAG, AN-BOUND, AN-HIER
"""

import re
import numpy as np
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from scipy import stats
from sklearn.isotonic import IsotonicRegression
import warnings

REPO_ROOT = Path(__file__).resolve().parent.parent
MEASUREMENT_CONTEXTS_PATH = REPO_ROOT / "data" / "pct-measurement-contexts.yaml"


# =============================================================================
# Bounded Parameter Transforms (AN-BOUND, Appendix AN §Bounded Parameter Treatment)
# =============================================================================

def logit_transform(theta, lower: float = 0.0, upper: float = 1.0):
    """Transform bounded parameter to unbounded space via logit.

    For θ ∈ [ℓ, u]: φ(θ) = log((θ - ℓ) / (u - θ))
    All calibration operations should be performed in φ-space.
    Accepts scalars or numpy arrays.
    """
    eps = 1e-10
    theta_clipped = np.clip(theta, lower + eps, upper - eps)
    result = np.log((theta_clipped - lower) / (upper - theta_clipped))
    return float(result) if np.ndim(result) == 0 else result


def inverse_logit(phi, lower: float = 0.0, upper: float = 1.0):
    """Back-transform from unbounded to bounded space.

    φ⁻¹(φ) = ℓ + (u - ℓ) / (1 + exp(-φ))
    Accepts scalars or numpy arrays.
    """
    result = lower + (upper - lower) / (1.0 + np.exp(-phi))
    return float(result) if np.ndim(result) == 0 else result


def fisher_z(r: float) -> float:
    """Fisher z-transform for correlations r ∈ (-1, 1)."""
    r_clipped = np.clip(r, -0.9999, 0.9999)
    return float(np.arctanh(r_clipped))


def inverse_fisher_z(z: float) -> float:
    """Inverse Fisher z-transform."""
    return float(np.tanh(z))


@dataclass
class UncertaintyDecomposition:
    """4-component uncertainty decomposition (Axiom AN-A5).

    σ²_total = σ²_elicit + σ²_calib + σ²_model + σ²_context

    Components:
        sigma_elicit: Elicitation variance — from N LLM draws
        sigma_calib: Calibration variance — uncertainty in a, b parameters
        sigma_model: Model misspecification — residual variance after calibration
        sigma_context: Context uncertainty — from Ψ-dimension mapping
    """
    sigma_elicit: float
    sigma_calib: float
    sigma_model: float
    sigma_context: float

    @property
    def sigma_total(self) -> float:
        """Total uncertainty (root sum of squares)."""
        return float(np.sqrt(
            self.sigma_elicit**2 + self.sigma_calib**2 +
            self.sigma_model**2 + self.sigma_context**2
        ))

    @property
    def variance_total(self) -> float:
        """Total variance."""
        return (self.sigma_elicit**2 + self.sigma_calib**2 +
                self.sigma_model**2 + self.sigma_context**2)

    def dominant_source(self) -> str:
        """Identify the dominant uncertainty source."""
        sources = {
            "elicitation": self.sigma_elicit**2,
            "calibration": self.sigma_calib**2,
            "model": self.sigma_model**2,
            "context": self.sigma_context**2,
        }
        return max(sources, key=sources.get)

    def to_dict(self) -> Dict:
        return {
            "sigma_elicit": round(self.sigma_elicit, 4),
            "sigma_calib": round(self.sigma_calib, 4),
            "sigma_model": round(self.sigma_model, 4),
            "sigma_context": round(self.sigma_context, 4),
            "sigma_total": round(self.sigma_total, 4),
            "dominant_source": self.dominant_source(),
        }


@dataclass
class AnchorDiagnostic:
    """Diagnostic for a single calibration anchor (AN-DIAG).

    Cook's distance, leverage, and studentized residuals for identifying
    influential or problematic anchor points.
    """
    name: str
    cooks_d: float
    leverage: float
    studentized_residual: float
    flagged: bool
    flag_reasons: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "cooks_d": round(self.cooks_d, 4),
            "leverage": round(self.leverage, 4),
            "studentized_residual": round(self.studentized_residual, 4),
            "flagged": self.flagged,
            "flag_reasons": self.flag_reasons,
        }


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
    theta_raw: float           # Raw LLM estimate (or PCT estimate)
    theta_calibrated: float    # After level calibration
    theta_final: float         # After shrinkage
    sigma_calibrated: float    # Calibrated uncertainty
    sigma_final: float         # Final uncertainty after shrinkage
    ci_95: Tuple[float, float] # 95% confidence interval
    shrinkage_factor: float    # Lambda (0 = full shrinkage, 1 = no shrinkage)
    tier: int = 3
    tier_note: str = ""
    pct_provenance: Optional[Dict] = None  # PCT transformation details if applicable
    uncertainty: Optional[UncertaintyDecomposition] = None  # 4-component decomposition (AN-A5)

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON export."""
        d = {
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
        if self.pct_provenance:
            d["pct_provenance"] = self.pct_provenance
        if self.uncertainty:
            d["uncertainty_decomposition"] = self.uncertainty.to_dict()
        return d


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
                 shrinkage_prior: float = 0.5,
                 linex_c1: float = 1.0,
                 linex_c2: float = 2.0,
                 linex_a: float = 1.0,
                 bounds: Optional[Tuple[float, float]] = None):
        """
        Initialize calibrator.

        Args:
            min_anchors: Minimum number of calibration anchors (CAL-1)
            use_isotonic: Use isotonic regression instead of linear
            shrinkage_prior: Prior mean for shrinkage (default: 0.5 = agnostic)
            linex_c1: LINEX loss underestimation penalty (default: 1.0)
            linex_c2: LINEX loss overestimation penalty (default: 2.0)
            linex_a: LINEX loss exponential parameter (default: 1.0)
            bounds: Parameter bounds (lower, upper) for logit transform.
                    None = unbounded (no transform).
        """
        self.min_anchors = min_anchors
        self.use_isotonic = use_isotonic
        self.shrinkage_prior = shrinkage_prior
        self.linex_c1 = linex_c1
        self.linex_c2 = linex_c2
        self.linex_a = linex_a
        self.bounds = bounds

        self.anchors: List[CalibrationAnchor] = []
        self.a: Optional[float] = None  # Intercept
        self.b: Optional[float] = None  # Slope
        self.sigma_model: Optional[float] = None  # Model misspecification
        self.sigma_calib: Optional[float] = None  # Calibration parameter uncertainty
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

        # If bounds are set, fit in transformed space (logit)
        # so calibration and fit use the same domain.
        # Filter out anchors outside bounds (they can't be logit-transformed).
        if self.bounds is not None:
            lo, hi = self.bounds
            eps = 1e-6
            mask = (theta_t12 > lo + eps) & (theta_t12 < hi - eps) \
                 & (theta_llm > lo + eps) & (theta_llm < hi - eps)
            theta_t12 = theta_t12[mask]
            theta_llm = theta_llm[mask]
            weights = weights[mask]
            n = len(theta_t12)
            if n < self.min_anchors:
                raise ValueError(
                    f"CAL-1 violation: After filtering to bounds [{lo}, {hi}], "
                    f"only {n} anchors remain (need {self.min_anchors})."
                )
            theta_t12 = logit_transform(theta_t12, lo, hi)
            theta_llm = logit_transform(theta_llm, lo, hi)

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

        # Bootstrap sigma_calib: uncertainty in calibration parameters a, b
        # This quantifies how much the calibration itself is uncertain
        n_boot = 200
        a_boots = np.zeros(n_boot)
        b_boots = np.zeros(n_boot)
        rng = np.random.default_rng(42)
        for boot_i in range(n_boot):
            idx = rng.choice(n, size=n, replace=True)
            t12_b = theta_t12[idx]
            llm_b = theta_llm[idx]
            w_b = weights[idx]
            W_b = np.diag(w_b)
            X_b = np.column_stack([np.ones(n), llm_b])
            try:
                beta_b = np.linalg.solve(X_b.T @ W_b @ X_b, X_b.T @ W_b @ t12_b)
                a_boots[boot_i] = beta_b[0]
                b_boots[boot_i] = beta_b[1]
            except np.linalg.LinAlgError:
                a_boots[boot_i] = self.a
                b_boots[boot_i] = self.b
        # sigma_calib from spread of bootstrapped predictions at mean theta_llm
        mean_llm = np.mean(theta_llm)
        pred_boots = a_boots + b_boots * mean_llm
        self.sigma_calib = float(np.std(pred_boots))

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
        Apply decision-theoretic evidence-weighted shrinkage (CAL-4, Axiom AN-A6).

        Uses LINEX asymmetric loss function:
            L(Δ) = c₁·[exp(a·Δ) - a·Δ - 1]  if Δ ≥ 0 (overestimation)
            L(Δ) = c₂·[exp(a·|Δ|) - a·|Δ| - 1]  if Δ < 0 (underestimation)

        Optimal shrinkage (Appendix AN, Result AN-R7):
            λ^opt = τ²/(τ² + σ²_total) · [1 - a·σ²_total/(2(τ² + σ²_total))]

        When c1 == c2 (symmetric), this reduces to standard James-Stein shrinkage.

        Returns:
            Tuple of (theta_final, sigma_final, lambda)
        """
        sigma_total_sq = sigma_cal**2
        tau_sq = self.tau**2

        # Base shrinkage factor (James-Stein)
        lam_base = tau_sq / (tau_sq + sigma_total_sq)

        # LINEX asymmetry correction
        # When c2 > c1 (underestimation costlier), we shrink less (preserve signal)
        # The correction term adjusts the shrinkage based on loss asymmetry
        asymmetry_ratio = self.linex_c2 / max(self.linex_c1, 1e-10)
        if abs(asymmetry_ratio - 1.0) > 0.01:
            # Apply LINEX correction: reduce shrinkage when losses are asymmetric
            correction = self.linex_a * sigma_total_sq / (2 * (tau_sq + sigma_total_sq))
            lam = lam_base * (1.0 - correction)
            # Bias correction for asymmetric loss: shift toward conservative direction
            # When c2 > c1 (underestimation costly), shift estimate upward
            bias_shift = (np.log(asymmetry_ratio) / (2 * self.linex_a)) * sigma_total_sq
        else:
            # Symmetric case: standard James-Stein
            lam = lam_base
            bias_shift = 0.0

        lam = np.clip(lam, 0.0, 1.0)

        # Shrunk estimate with LINEX bias correction
        theta_final = lam * theta_cal + (1 - lam) * self.shrinkage_prior + bias_shift

        # Shrunk uncertainty
        sigma_final = lam * sigma_cal

        return theta_final, sigma_final, lam

    def calibrate(self, theta_llm: float, eu_llm: float,
                  apply_shrinkage: bool = True,
                  sigma_context: float = 0.0) -> CalibrationResult:
        """
        Calibrate a new LLM estimate (E5: Validation and Bounded Inference).

        Implements the full pipeline: level calibration → uncertainty calibration
        → bounded transform → shrinkage → uncertainty decomposition.

        Args:
            theta_llm: Raw LLM estimate from LLMMC (output of E2-E3)
            eu_llm: Elicitation uncertainty from LLMMC (σ_elicit from E3)
            apply_shrinkage: Whether to apply shrinkage (default: True)
            sigma_context: Context uncertainty from Ψ-mapping (default: 0.0)

        Returns:
            CalibrationResult with calibrated estimate, uncertainty, and
            4-component UncertaintyDecomposition (Axiom AN-A5)

        Raises:
            RuntimeError: If calibrator not fitted
        """
        if not self._fitted:
            raise RuntimeError("Calibrator not fitted. Call fit() first.")

        # Apply bounded transform if bounds specified (AN-BOUND)
        lo_b = self.bounds[0] if self.bounds else None
        hi_b = self.bounds[1] if self.bounds else None
        if self.bounds is not None:
            theta_work = logit_transform(theta_llm, lo_b, hi_b)
            # Transform eu_llm to logit space via Delta method:
            # sigma_logit ≈ sigma_orig / (theta*(1-theta_normalized))
            theta_norm = (theta_llm - lo_b) / (hi_b - lo_b)
            theta_norm = np.clip(theta_norm, 0.01, 0.99)
            jacobian = 1.0 / (theta_norm * (1.0 - theta_norm) * (hi_b - lo_b))
            eu_logit = eu_llm * jacobian
        else:
            theta_work = theta_llm
            eu_logit = eu_llm

        # Level calibration (CAL-2) — in working space
        theta_cal = self._apply_level_calibration(theta_work)

        # Uncertainty calibration (CAL-3) — use transformed uncertainty
        sigma_cal = self._apply_uncertainty_calibration(eu_logit)

        # Shrinkage (CAL-4, Axiom AN-A6)
        if apply_shrinkage:
            theta_final_work, sigma_final_work, lam = self._apply_shrinkage(theta_cal, sigma_cal)
        else:
            theta_final_work = theta_cal
            sigma_final_work = sigma_cal
            lam = 1.0

        # Back-transform and compute CI
        if self.bounds is not None:
            # CI in logit space, then back-transform endpoints
            ci_lower_logit = theta_final_work - 1.96 * sigma_final_work
            ci_upper_logit = theta_final_work + 1.96 * sigma_final_work
            theta_final = inverse_logit(theta_final_work, lo_b, hi_b)
            theta_cal = inverse_logit(theta_cal, lo_b, hi_b)
            ci_lower = float(inverse_logit(ci_lower_logit, lo_b, hi_b))
            ci_upper = float(inverse_logit(ci_upper_logit, lo_b, hi_b))
            # Approximate SE in original space via Delta method
            theta_norm_final = (theta_final - lo_b) / (hi_b - lo_b)
            theta_norm_final = np.clip(theta_norm_final, 0.01, 0.99)
            sigma_final = sigma_final_work * theta_norm_final * (1.0 - theta_norm_final) * (hi_b - lo_b)
        else:
            theta_final = theta_final_work
            sigma_final = sigma_final_work
            ci_lower = max(0, theta_final - 1.96 * sigma_final)
            ci_upper = min(1, theta_final + 1.96 * sigma_final)

        # 4-component uncertainty decomposition (Axiom AN-A5)
        uncertainty = UncertaintyDecomposition(
            sigma_elicit=eu_llm,
            sigma_calib=self.sigma_calib if self.sigma_calib else 0.0,
            sigma_model=self.sigma_model if self.sigma_model else 0.0,
            sigma_context=sigma_context,
        )

        return CalibrationResult(
            theta_raw=theta_llm,
            theta_calibrated=theta_cal,
            theta_final=theta_final,
            sigma_calibrated=sigma_cal,
            sigma_final=sigma_final,
            ci_95=(ci_lower, ci_upper),
            shrinkage_factor=lam,
            tier=3,
            tier_note=f"calibrated on Tier-1/2 anchors (n={len(self.anchors)})",
            uncertainty=uncertainty,
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
            "sigma_calib": self.sigma_calib,
            "tau": self.tau,
            "n_anchors": len(self.anchors),
            "use_isotonic": self.use_isotonic,
            "linex_c1": self.linex_c1,
            "linex_c2": self.linex_c2,
            "linex_a": self.linex_a,
            "bounds": self.bounds,
        }

    # -----------------------------------------------------------------
    # Anchor Diagnostics (AN-DIAG)
    # -----------------------------------------------------------------

    def diagnose_anchors(self) -> List[AnchorDiagnostic]:
        """
        Compute diagnostics for all calibration anchors (AN-DIAG).

        For each anchor, computes:
        - Cook's distance: influence on calibration parameters
        - Leverage: how unusual the anchor's LLM estimate is
        - Studentized residual: how poorly the anchor fits the calibration

        Flagging criteria:
        - Cook's D > 4/n
        - |Studentized residual| > 2
        - Leverage > 2p/n (p=2 for linear model)

        Returns:
            List of AnchorDiagnostic objects, one per anchor
        """
        if not self._fitted:
            raise RuntimeError("Calibrator not fitted. Call fit() first.")

        n = len(self.anchors)
        p = 2  # intercept + slope
        theta_llm = np.array([a.theta_llm for a in self.anchors])
        theta_t12 = np.array([a.theta_t12 for a in self.anchors])
        weights = np.array([a.weight for a in self.anchors])

        # Design matrix and hat matrix
        X = np.column_stack([np.ones(n), theta_llm])
        W = np.diag(weights)
        XtWX_inv = np.linalg.inv(X.T @ W @ X)
        H = X @ XtWX_inv @ X.T @ W  # Hat matrix

        # Predictions and residuals
        theta_pred = self.a + self.b * theta_llm
        residuals = theta_t12 - theta_pred

        # MSE
        mse = np.sum(weights * residuals**2) / (n - p)

        diagnostics = []
        for i in range(n):
            h_ii = H[i, i]
            e_i = residuals[i]

            # Studentized residual
            denom = np.sqrt(max(mse * (1 - h_ii), 1e-12))
            stud_resid = e_i / denom

            # Cook's distance
            cooks_d = (stud_resid**2 * h_ii) / (p * (1 - h_ii)) if (1 - h_ii) > 1e-12 else 0.0

            # Flagging
            flag_reasons = []
            if cooks_d > 4.0 / n:
                flag_reasons.append(f"Cook's D={cooks_d:.3f} > {4.0/n:.3f}")
            if abs(stud_resid) > 2.0:
                flag_reasons.append(f"|studentized_resid|={abs(stud_resid):.2f} > 2")
            if h_ii > 2 * p / n:
                flag_reasons.append(f"leverage={h_ii:.3f} > {2*p/n:.3f}")

            diagnostics.append(AnchorDiagnostic(
                name=self.anchors[i].name,
                cooks_d=float(cooks_d),
                leverage=float(h_ii),
                studentized_residual=float(stud_resid),
                flagged=len(flag_reasons) > 0,
                flag_reasons=flag_reasons,
            ))

        return diagnostics

    # -----------------------------------------------------------------
    # MC Uncertainty Propagation (Algorithm MC-UP, Appendix AN)
    # -----------------------------------------------------------------

    def mc_uncertainty_propagation(
        self,
        theta_llm: float,
        eu_llm: float,
        sigma_context: float = 0.0,
        n_mc: int = 2000,
        seed: int = 42,
    ) -> Dict:
        """
        Monte Carlo uncertainty propagation through the full pipeline.

        Bootstrap the entire calibration → shrinkage pipeline to get
        empirical posterior distribution (Algorithm MC-UP from Appendix AN).

        Steps per MC draw:
        1. Resample anchors with replacement
        2. Refit calibration (a*, b*)
        3. Draw θ_LLM* ~ N(θ_LLM, σ_elicit²)
        4. Apply calibration with resampled params
        5. Apply shrinkage
        6. Collect θ*_final

        Args:
            theta_llm: Raw LLM estimate
            eu_llm: Elicitation uncertainty
            sigma_context: Context uncertainty
            n_mc: Number of Monte Carlo draws (default: 2000)
            seed: Random seed for reproducibility

        Returns:
            Dict with posterior_mean, posterior_sd, ci_95, posterior_draws
        """
        if not self._fitted:
            raise RuntimeError("Calibrator not fitted. Call fit() first.")

        n = len(self.anchors)
        rng = np.random.default_rng(seed)
        theta_finals = np.zeros(n_mc)

        theta_t12_arr = np.array([a.theta_t12 for a in self.anchors])
        theta_llm_arr = np.array([a.theta_llm for a in self.anchors])
        weights_arr = np.array([a.weight for a in self.anchors])

        for mc_i in range(n_mc):
            # Step 1: Resample anchors
            idx = rng.choice(n, size=n, replace=True)
            t12_b = theta_t12_arr[idx]
            llm_b = theta_llm_arr[idx]
            w_b = weights_arr[idx]

            # Step 2: Refit calibration
            try:
                W_b = np.diag(w_b)
                X_b = np.column_stack([np.ones(n), llm_b])
                beta_b = np.linalg.solve(X_b.T @ W_b @ X_b, X_b.T @ W_b @ t12_b)
                a_b, b_b = beta_b[0], beta_b[1]
                resid_b = t12_b - (a_b + b_b * llm_b)
                sigma_model_b = np.std(resid_b, ddof=2) if n > 2 else self.sigma_model
                tau_b = np.std(a_b + b_b * llm_b)
            except (np.linalg.LinAlgError, ValueError):
                a_b, b_b = self.a, self.b
                sigma_model_b = self.sigma_model
                tau_b = self.tau

            # Step 3: Draw noisy theta_llm
            theta_draw = rng.normal(theta_llm, eu_llm)

            # Step 4: Apply calibration
            theta_cal_b = a_b + b_b * theta_draw
            sigma_cal_b = np.sqrt((b_b * eu_llm)**2 + sigma_model_b**2 + sigma_context**2)

            # Step 5: Apply shrinkage
            lam_b = tau_b**2 / (tau_b**2 + sigma_cal_b**2) if (tau_b**2 + sigma_cal_b**2) > 0 else 0.5
            theta_final_b = lam_b * theta_cal_b + (1 - lam_b) * self.shrinkage_prior

            theta_finals[mc_i] = theta_final_b

        # Compute posterior statistics
        posterior_mean = float(np.mean(theta_finals))
        posterior_sd = float(np.std(theta_finals))
        ci_lower = float(np.percentile(theta_finals, 2.5))
        ci_upper = float(np.percentile(theta_finals, 97.5))

        return {
            "posterior_mean": round(posterior_mean, 4),
            "posterior_sd": round(posterior_sd, 4),
            "ci_95": [round(ci_lower, 4), round(ci_upper, 4)],
            "n_mc": n_mc,
            "posterior_draws": theta_finals.tolist(),
        }

    # -----------------------------------------------------------------
    # Hierarchical Bayesian Calibration (AN-HIER, Appendix AN)
    # -----------------------------------------------------------------

    def hierarchical_calibrate(
        self,
        domain_anchors: Dict[str, List[CalibrationAnchor]],
        theta_llm: float,
        eu_llm: float,
        target_domain: str,
        sigma_context: float = 0.0,
    ) -> CalibrationResult:
        """
        Hierarchical Bayesian calibration with domain-level shrinkage.

        Multi-level model (Appendix AN §Hierarchical Bayesian Extension):
            Level 1: θ_ij | μ_j, σ²_j ~ N(a_j + b_j·θ_LLM, σ²_j)
            Level 2: μ_j | μ_0, τ²_domain ~ N(μ_0, τ²_domain)
            Level 3: μ_0 | μ_global, τ²_global ~ N(μ_global, τ²_global)

        Domain-level empirical Bayes shrinkage pools information across
        domains while respecting domain-specific calibration patterns.

        Args:
            domain_anchors: Dict mapping domain names to lists of anchors
            theta_llm: Raw LLM estimate for target parameter
            eu_llm: Elicitation uncertainty
            target_domain: Domain for the target parameter
            sigma_context: Context uncertainty

        Returns:
            CalibrationResult with hierarchical calibration
        """
        # Step 1: Fit domain-specific calibrators
        domain_estimates = {}
        domain_sigmas = {}
        for domain, anchors in domain_anchors.items():
            if len(anchors) < 3:
                continue
            cal = LLMMCCalibrator(min_anchors=3, bounds=self.bounds)
            for a in anchors:
                cal.add_anchor(a.name, a.theta_t12, a.se_t12,
                               a.theta_llm, a.eu_llm, a.source)
            try:
                cal.fit()
                result = cal.calibrate(theta_llm, eu_llm, apply_shrinkage=False)
                domain_estimates[domain] = result.theta_calibrated
                domain_sigmas[domain] = result.sigma_calibrated
            except (ValueError, RuntimeError):
                continue

        if not domain_estimates:
            # Fallback to pooled calibration
            return self.calibrate(theta_llm, eu_llm, sigma_context=sigma_context)

        # Step 2: Compute global mean and between-domain variance
        all_ests = np.array(list(domain_estimates.values()))
        all_sigs = np.array(list(domain_sigmas.values()))
        mu_global = float(np.mean(all_ests))
        tau_domain_sq = max(float(np.var(all_ests) - np.mean(all_sigs**2)), 1e-6)

        # Step 3: Domain-level empirical Bayes shrinkage
        if target_domain in domain_estimates:
            theta_domain = domain_estimates[target_domain]
            sigma_domain = domain_sigmas[target_domain]
        else:
            # Use global estimate for unknown domain
            theta_domain = mu_global
            sigma_domain = float(np.sqrt(tau_domain_sq + np.mean(all_sigs**2)))

        # Shrink domain estimate toward global mean
        lam_hier = tau_domain_sq / (tau_domain_sq + sigma_domain**2)
        theta_hier = lam_hier * theta_domain + (1 - lam_hier) * mu_global

        # Posterior variance includes both:
        #   (a) conditional variance: lam * sigma²_domain
        #   (b) estimation uncertainty in mu_global: ~mean(sigma²) / n_domains
        # When tau_domain → 0 (full pooling), (a) → 0 but (b) > 0
        sigma_mu_global = float(np.sqrt(np.mean(all_sigs**2) / len(all_sigs)))
        sigma_hier = float(np.sqrt(
            lam_hier * sigma_domain**2
            + (1 - lam_hier)**2 * sigma_mu_global**2
        ))

        # Step 4: Apply standard shrinkage on top
        theta_final, sigma_final, lam = self._apply_shrinkage(theta_hier, sigma_hier)

        # Bounds
        lower_bound = self.bounds[0] if self.bounds else 0
        upper_bound = self.bounds[1] if self.bounds else 1
        ci_lower = max(lower_bound, theta_final - 1.96 * sigma_final)
        ci_upper = min(upper_bound, theta_final + 1.96 * sigma_final)

        uncertainty = UncertaintyDecomposition(
            sigma_elicit=eu_llm,
            sigma_calib=self.sigma_calib if self.sigma_calib else 0.0,
            sigma_model=self.sigma_model if self.sigma_model else 0.0,
            sigma_context=sigma_context,
        )

        n_domains = len(domain_estimates)
        return CalibrationResult(
            theta_raw=theta_llm,
            theta_calibrated=theta_hier,
            theta_final=theta_final,
            sigma_calibrated=sigma_hier,
            sigma_final=sigma_final,
            ci_95=(ci_lower, ci_upper),
            shrinkage_factor=lam,
            tier=3,
            tier_note=(
                f"hierarchical ({n_domains} domains, "
                f"target={target_domain}, "
                f"λ_hier={lam_hier:.2f})"
            ),
            uncertainty=uncertainty,
        )

    def summary(self) -> str:
        """Generate human-readable summary (v2.0 with AN-A5/A6 diagnostics)."""
        if not self._fitted:
            return f"LLMMCCalibrator (not fitted, {len(self.anchors)} anchors)"

        params = self.get_calibration_params()
        loo = self.loo_cross_validation()

        lines = [
            "=" * 65,
            "LLMMC Calibration Summary (v2.0)",
            "=" * 65,
            f"Anchors: n = {params['n_anchors']}",
            f"Method: {'Isotonic' if params['use_isotonic'] else 'Linear'}",
            f"Bounds: {params['bounds'] or 'unbounded'}",
            "",
            "Level Calibration (CAL-2):",
            f"  theta_cal = {params['a']:.4f} + {params['b']:.4f} * theta_LLM",
            "",
            "Uncertainty (AN-A5, 4-component):",
            f"  sigma_model = {params['sigma_model']:.4f}  (model misspecification)",
            f"  sigma_calib = {params['sigma_calib']:.4f}  (calibration parameter uncertainty)",
            "",
            "Shrinkage (CAL-4, Axiom AN-A6):",
            f"  tau = {params['tau']:.4f}",
            f"  Prior = {self.shrinkage_prior}",
            f"  LINEX: c1={params['linex_c1']}, c2={params['linex_c2']}, a={params['linex_a']}",
            f"  {'(asymmetric)' if params['linex_c1'] != params['linex_c2'] else '(symmetric)'}",
            "",
            "LOO Cross-Validation (HHH-CAL-1 / LLP-2):",
            f"  MAE = {loo.mae:.4f} {'PASS' if loo.mae < 0.12 else 'FAIL'}",
            f"  RMSE = {loo.rmse:.4f} {'PASS' if loo.rmse < 0.15 else 'FAIL'}",
            f"  Coverage_95 = {loo.coverage_95:.2%} {'PASS' if 0.85 <= loo.coverage_95 <= 0.98 else 'FAIL'}",
            f"  Spearman rho = {loo.spearman_rho:.4f} {'PASS' if loo.spearman_rho > 0.70 else 'FAIL'}",
        ]

        # Anchor diagnostics
        diags = self.diagnose_anchors()
        flagged = [d for d in diags if d.flagged]
        lines.append("")
        lines.append(f"Anchor Diagnostics (AN-DIAG): {len(flagged)}/{len(diags)} flagged")
        for d in flagged:
            lines.append(f"  WARNING: {d.name} ({', '.join(d.flag_reasons)})")

        lines.extend([
            "",
            f"LLP Status: {'LEGITIMATE' if loo.is_acceptable() else 'NOT LEGITIMATE'}",
            f"  LLP-1 (Reproducibility): bootstrap sigma_calib={params['sigma_calib']:.4f}",
            f"  LLP-2 (Calibration): {'PASS' if loo.is_acceptable() else 'FAIL'}",
            f"  LLP-3 (Bounded): {'PASS' if params['bounds'] else 'unbounded (default)'}",
            "=" * 65
        ])

        return "\n".join(lines)

    # -----------------------------------------------------------------
    # PCT Integration (PCT-CAL-1)
    # -----------------------------------------------------------------

    def add_pct_anchors(
        self,
        contexts_path: Optional[Path] = None,
        se_default: float = 0.08,
        eu_llm_default: float = 0.12,
    ) -> int:
        """
        Load measurement_contexts from extracted YAML and add as anchors.

        Only triplets with parseable numeric value_estimates are used.
        The value_estimate becomes theta_t12 (empirical Tier-1/2 reference),
        and an LLMMC-simulated prior is added as theta_llm with default
        uncertainty.

        Args:
            contexts_path: Path to pct-measurement-contexts.yaml
                           (default: data/pct-measurement-contexts.yaml)
            se_default: Default standard error for parsed values
            eu_llm_default: Default elicitation uncertainty for LLM prior

        Returns:
            Number of anchors added
        """
        try:
            import yaml
        except ImportError:
            warnings.warn("PyYAML required for PCT anchor loading")
            return 0

        path = contexts_path or MEASUREMENT_CONTEXTS_PATH
        if not path.exists():
            warnings.warn(f"PCT measurement contexts not found: {path}")
            return 0

        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        triplets = data.get("triplets", [])
        added = 0

        for t in triplets:
            val_str = str(t.get("value_estimate", ""))
            theta = _parse_numeric_value(val_str)
            if theta is None:
                continue

            name = f"{t.get('parameter_symbol', 'unknown')}_{t.get('context', 'unknown')}"
            source = t.get("paper_key", "unknown")

            # Synthetic LLMMC prior for calibration anchor pairing.
            # In production, theta_llm comes from actual LLMMC protocol (E1-E3):
            #   E1: structured prompt → E2: N≥10 draws → E3: aggregated mean.
            # Here we simulate the typical LLM bias pattern for demo/bootstrap:
            #   - LLMs overestimate magnitude by ~10-15% (Appendix AN, Table 1)
            #   - Additive bias ~0.02 (intercept shift)
            # TODO(production): Replace with actual LLMMC elicitation via E1-E3
            sign = 1.0 if theta >= 0 else -1.0
            theta_llm = theta * 1.12 + sign * 0.02

            self.add_anchor(
                name=name,
                theta_t12=theta,
                se_t12=se_default,
                theta_llm=theta_llm,
                eu_llm=eu_llm_default,
                source=source,
            )
            added += 1

        return added

    def calibrate_with_pct(
        self,
        pct_result,
        eu_pct: float = 0.10,
        apply_shrinkage: bool = True,
        sigma_context: float = 0.05,
    ) -> CalibrationResult:
        """
        Calibrate using a PCT-transformed value as informed prior (Tier 2.5).

        Instead of a raw LLM estimate, the PCT prediction theta_B serves
        as the input. This is Tier 2.5: better than pure LLM (Tier 3)
        because it uses empirical anchors + formal transformation,
        but still benefits from LLMMC bias correction.

        Args:
            pct_result: A PCTResult object from pct.transform*()
            eu_pct: Uncertainty of the PCT estimate (default 0.10,
                    lower than typical LLM eu because PCT is grounded)
            apply_shrinkage: Whether to apply shrinkage
            sigma_context: Context uncertainty from Ψ-mapping (default: 0.05,
                          lower than pure LLMMC because PCT accounts for context)

        Returns:
            CalibrationResult with PCT provenance and UncertaintyDecomposition
        """
        if not self._fitted:
            raise RuntimeError("Calibrator not fitted. Call fit() first.")

        # Use PCT prediction as the input (replacing raw LLM estimate)
        theta_pct = pct_result.theta_B

        # Apply LLMMC calibration pipeline
        theta_cal = self._apply_level_calibration(theta_pct)
        sigma_cal = self._apply_uncertainty_calibration(eu_pct)

        if apply_shrinkage:
            theta_final, sigma_final, lam = self._apply_shrinkage(theta_cal, sigma_cal)
        else:
            theta_final = theta_cal
            sigma_final = sigma_cal
            lam = 1.0

        ci_lower = theta_final - 1.96 * sigma_final
        ci_upper = theta_final + 1.96 * sigma_final

        # Build PCT provenance
        provenance = {
            "theta_A": round(pct_result.theta_A, 4),
            "theta_B_pct": round(pct_result.theta_B, 4),
            "product_M": round(pct_result.product_M, 4),
            "anchor_context": pct_result.anchor_context,
            "target_context": pct_result.target_context,
            "parameter_symbol": pct_result.parameter_symbol,
            "n_psi_dimensions": len(pct_result.psi_deltas),
        }

        # 4-component uncertainty (AN-A5)
        uncertainty = UncertaintyDecomposition(
            sigma_elicit=eu_pct,
            sigma_calib=self.sigma_calib if self.sigma_calib else 0.0,
            sigma_model=self.sigma_model if self.sigma_model else 0.0,
            sigma_context=sigma_context,
        )

        return CalibrationResult(
            theta_raw=theta_pct,
            theta_calibrated=theta_cal,
            theta_final=theta_final,
            sigma_calibrated=sigma_cal,
            sigma_final=sigma_final,
            ci_95=(ci_lower, ci_upper),
            shrinkage_factor=lam,
            tier=3,
            tier_note=(
                f"PCT-informed (Tier 2.5): anchor={pct_result.anchor_context}, "
                f"target={pct_result.target_context}, "
                f"calibrated on {len(self.anchors)} anchors"
            ),
            pct_provenance=provenance,
            uncertainty=uncertainty,
        )


def _parse_numeric_value(val_str: str) -> Optional[float]:
    """
    Parse a numeric value from a value_estimate string.

    Handles: "0.57", "2.5", "-10.1%", "λ_R ≈ 2.5", "0.60-0.80" (takes midpoint).
    Returns None for qualitative strings like "positive (β > 0)".
    """
    if not val_str or val_str.strip() == "":
        return None

    s = val_str.strip()

    # Direct float
    try:
        return float(s)
    except ValueError:
        pass

    # Range "0.60-0.80" → midpoint (but not negative numbers like "-0.3")
    range_match = re.match(r'^(\d+\.?\d*)\s*[-–]\s*(\d+\.?\d*)$', s)
    if range_match:
        lo, hi = float(range_match.group(1)), float(range_match.group(2))
        return (lo + hi) / 2.0

    # Percentage "-10.1%"
    pct_match = re.match(r'^([+-]?\d+\.?\d*)%$', s)
    if pct_match:
        return float(pct_match.group(1)) / 100.0

    # Embedded number "λ_R ≈ 2.5" or "delta_S ~ 0.15 per period"
    num_match = re.search(r'[≈~=]\s*([+-]?\d+\.?\d*)', s)
    if num_match:
        return float(num_match.group(1))

    return None


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


def demo_pct_calibration() -> None:
    """
    Full PCT → LLMMC calibration demo (Tier 2.5 pipeline).

    Demonstrates:
      1. Load empirical + PCT anchors
      2. Fit calibrator
      3. PCT transform (Benabou welfare → workplace)
      4. LLMMC calibration of the PCT result
      5. Full provenance chain
    """
    import json
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from pct import (
        demo_benabou, transform_from_contexts, print_pct_report,
    )

    print()
    print("=" * 65)
    print("  PCT → LLMMC CALIBRATION DEMO (Tier 2.5 Pipeline)")
    print("=" * 65)

    # ── Step 1: Create calibrator with empirical + PCT anchors ──────
    print("\n── Step 1: Build Calibration Set ──")
    cal = LLMMCCalibrator(min_anchors=5, use_isotonic=False)

    # Add literature-based anchors
    anchors = create_example_calibration_set()
    cal.add_anchors_from_dict(anchors)
    print(f"   Empirical anchors: {len(anchors)}")

    # Add PCT-derived anchors from measurement_contexts
    n_pct = cal.add_pct_anchors()
    print(f"   PCT anchors (from measurement_contexts): {n_pct}")
    print(f"   Total anchors: {len(cal.anchors)}")

    # ── Step 2: Fit calibrator ──────────────────────────────────────
    print("\n── Step 2: Fit Calibrator ──")
    cal.fit()
    params = cal.get_calibration_params()
    print(f"   Level calibration: θ_cal = {params['a']:.4f} + {params['b']:.4f} × θ_LLM")
    print(f"   Model uncertainty: σ_model = {params['sigma_model']:.4f}")
    print(f"   Shrinkage τ: {params['tau']:.4f}")

    # ── Step 3: PCT Transform (Benabou welfare → workplace) ────────
    print("\n── Step 3: PCT Transform ──")
    print("   Parameter: λ_R (rejection sensitivity)")
    print("   Anchor: welfare_takeup (θ_A = 2.5)")
    print("   Target: workplace_help")

    pct_result = demo_benabou()
    print(f"\n   Psi-Multipliers:")
    for pd in pct_result.psi_deltas:
        sign = "+" if pd.delta >= 0 else ""
        print(f"     {pd.dimension:8s}  Δ={sign}{pd.delta:.2f}  M={pd.multiplier:.4f}"
              f"  ({pd.anchor_label} → {pd.target_label})")
    print(f"   Product(M): {pct_result.product_M:.4f}")
    print(f"   θ_B(PCT) = {pct_result.theta_A:.4f} × {pct_result.product_M:.4f}"
          f" = {pct_result.theta_B:.4f}")

    # ── Step 4: LLMMC Calibration of PCT result ────────────────────
    print("\n── Step 4: LLMMC Calibration (Tier 2.5) ──")
    result = cal.calibrate_with_pct(pct_result, eu_pct=0.10)

    print(f"   Input (PCT):        θ_B = {result.theta_raw:.4f}")
    print(f"   After bias corr:    θ_cal = {result.theta_calibrated:.4f}")
    print(f"   After shrinkage:    θ_final = {result.theta_final:.4f} ± {result.sigma_final:.4f}")
    print(f"   95% CI:             [{result.ci_95[0]:.4f}, {result.ci_95[1]:.4f}]")
    print(f"   Shrinkage factor:   λ = {result.shrinkage_factor:.4f}")
    print(f"   Tier:               {result.tier} ({result.tier_note})")

    # ── Step 5: Comparison with raw LLM estimate ───────────────────
    print("\n── Step 5: Comparison (PCT vs Raw LLM) ──")
    result_llm = cal.calibrate(theta_llm=pct_result.theta_B, eu_llm=0.15)
    pct_width = result.ci_95[1] - result.ci_95[0]
    llm_width = result_llm.ci_95[1] - result_llm.ci_95[0]

    print(f"   {'':20s} {'PCT (Tier 2.5)':>18s} {'Raw LLM (Tier 3)':>18s}")
    print(f"   {'─' * 58}")
    print(f"   {'Input θ':20s} {result.theta_raw:>18.4f} {result_llm.theta_raw:>18.4f}")
    print(f"   {'Uncertainty':20s} {'0.10':>18s} {'0.15':>18s}")
    print(f"   {'Final θ':20s} {result.theta_final:>18.4f} {result_llm.theta_final:>18.4f}")
    print(f"   {'95% CI width':20s} {pct_width:>18.4f} {llm_width:>18.4f}")
    advantage = (1 - pct_width / llm_width) * 100 if llm_width > 0 else 0
    print(f"\n   → PCT reduces CI width by {advantage:.0f}%")

    # ── Step 6: Provenance chain ───────────────────────────────────
    print("\n── Step 6: Full Provenance Chain ──")
    d = result.to_dict()
    prov = d.get("pct_provenance", {})
    print(f"   Source paper: PAP-benabou2022hurts")
    print(f"   Parameter:    {prov.get('parameter_symbol', '')} ({pct_result.parameter_id})")
    print(f"   Anchor:       {prov.get('anchor_context', '')} (θ_A = {prov.get('theta_A', '')})")
    print(f"   Target:       {prov.get('target_context', '')} (θ_B = {prov.get('theta_B_pct', '')})")
    print(f"   Transform:    {prov.get('n_psi_dimensions', '')} Ψ-dimensions, M = {prov.get('product_M', '')}")
    print(f"   Calibration:  {len(cal.anchors)} anchors ({n_pct} from PCT)")
    print(f"   Final:        θ = {result.theta_final:.4f} [{result.ci_95[0]:.4f}, {result.ci_95[1]:.4f}]")

    print(f"\n   JSON (full):")
    print(json.dumps(d, indent=2))
    print()


if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(
        description="LLMMC Calibration — LLM Monte Carlo bias correction",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python llmmc_calibration.py                 # Standard LLMMC demo
  python llmmc_calibration.py --pct-demo      # Full PCT → LLMMC pipeline
  python llmmc_calibration.py --json          # JSON output only

Protocol: HHH-LLMMC-1, HHH-CAL-1, PCT-CAL-1
Layer: 1 (Formal Computation)
        """
    )
    parser.add_argument("--pct-demo", action="store_true",
                        help="Run PCT → LLMMC calibration demo (Tier 2.5)")
    parser.add_argument("--json", action="store_true",
                        help="JSON-only output for standard demo")
    args = parser.parse_args()

    if args.pct_demo:
        demo_pct_calibration()
        sys.exit(0)

    # Standard LLMMC demo
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

    if args.json:
        import json
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print("\nJSON output:")
        import json
        print(json.dumps(result.to_dict(), indent=2))
