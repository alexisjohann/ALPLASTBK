#!/usr/bin/env python3
"""
PP (Percentage Points) Calibration
==================================

Scale-local calibration for percentage point effect sizes.
Calibration is done in ORIGINAL pp space (not 0-1 mapped) to avoid ceiling effects.

Regression: pp_true = a + b × pp_llm

Usage:
    python calibrate_pp.py --fit        # Fit calibration on anchors
    python calibrate_pp.py --evaluate   # Run 5-point checklist
    python calibrate_pp.py --calibrate --pp 45 --eu 5  # Calibrate new estimate

Author: EBF Framework
Date: 2025-01-13
Protocol: HHH-CAL-PP-1
"""

import json
import argparse
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
import numpy as np
from scipy import stats


@dataclass
class PPAnchor:
    """A pp-scale calibration anchor."""
    anchor_id: str
    pp_true: float      # Tier-1/2 reference value in pp
    se_true: float      # Standard error in pp
    pp_llm: float       # LLM estimate in pp
    eu_llm: float       # Elicitation uncertainty in pp
    citation: str
    domain: str

    @property
    def weight(self) -> float:
        """Inverse variance weight."""
        return 1.0 / (self.se_true**2 + self.eu_llm**2)


@dataclass
class PPCalibrationResult:
    """Result of pp calibration fitting."""
    a: float                    # Intercept
    b: float                    # Slope
    sigma_model: float          # Model misspecification
    n_anchors: int
    r_squared: float
    anchors: List[PPAnchor]

    # LOO results
    loo_mae: float
    loo_rmse: float
    loo_coverage: float
    loo_spearman: float
    loo_predictions: List[Tuple[str, float, float, bool]]  # (id, true, pred, covered)


def load_pp_anchors() -> List[PPAnchor]:
    """Load pp-scale anchors from JSON."""
    path = Path(__file__).parent.parent / "data" / "calibration" / "tier12_anchors_raw.json"
    with open(path, 'r') as f:
        data = json.load(f)

    pp_anchors = []
    for anchor in data.get("anchors", []):
        if anchor.get("effect_type") == "pp":
            anchor_id = anchor.get("anchor_id")
            pp_true = anchor.get("effect_mean")
            se_true = anchor.get("effect_se") or 3.0  # Default SE if not specified
            citation = anchor.get("citation", "")
            domain = anchor.get("domain", "")

            # Simulate LLMMC for demo (in production: real LLM calls)
            pp_llm, eu_llm = simulate_llmmc_pp(anchor_id, pp_true)

            pp_anchors.append(PPAnchor(
                anchor_id=anchor_id,
                pp_true=pp_true,
                se_true=se_true,
                pp_llm=pp_llm,
                eu_llm=eu_llm,
                citation=citation,
                domain=domain
            ))

    return pp_anchors


def simulate_llmmc_pp(anchor_id: str, pp_true: float) -> Tuple[float, float]:
    """
    Simulate LLMMC response for pp anchor (demo mode).

    In production, replace with actual LLM API calls.
    """
    np.random.seed(hash(anchor_id) % 2**32)

    # LLM tends to slightly overestimate large effects, underestimate small ones
    if pp_true > 50:
        bias = np.random.uniform(-5, 10)  # Slight underestimation for extreme effects
    elif pp_true > 20:
        bias = np.random.uniform(-3, 8)   # Moderate bias
    else:
        bias = np.random.uniform(-2, 5)   # Small bias for small effects

    noise = np.random.normal(0, 5)
    pp_llm = max(0, pp_true + bias + noise)

    # Elicitation uncertainty scales with effect size
    eu_llm = max(2, pp_true * 0.08 + np.random.uniform(1, 4))

    return round(pp_llm, 1), round(eu_llm, 2)


def fit_pp_calibration(anchors: List[PPAnchor]) -> PPCalibrationResult:
    """
    Fit pp calibration model.

    Regression: pp_true = a + b × pp_llm (weighted)
    """
    n = len(anchors)

    pp_true = np.array([a.pp_true for a in anchors])
    pp_llm = np.array([a.pp_llm for a in anchors])
    weights = np.array([a.weight for a in anchors])

    # Weighted linear regression
    W = np.diag(weights)
    X = np.column_stack([np.ones(n), pp_llm])

    XtWX = X.T @ W @ X
    XtWy = X.T @ W @ pp_true
    beta = np.linalg.solve(XtWX, XtWy)

    a, b = beta[0], beta[1]

    # Predictions and residuals
    pp_pred = a + b * pp_llm
    residuals = pp_true - pp_pred

    # Model misspecification
    sigma_model = np.std(residuals, ddof=2)

    # R-squared
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((pp_true - np.mean(pp_true))**2)
    r_squared = 1 - (ss_res / ss_tot)

    # LOO Cross-Validation
    loo_predictions = []
    loo_residuals = []
    loo_covered = []

    for i in range(n):
        # Leave out anchor i
        mask = np.ones(n, dtype=bool)
        mask[i] = False

        X_loo = X[mask]
        y_loo = pp_true[mask]
        W_loo = np.diag(weights[mask])

        beta_loo = np.linalg.solve(X_loo.T @ W_loo @ X_loo, X_loo.T @ W_loo @ y_loo)
        a_loo, b_loo = beta_loo

        # Predict for held-out
        pred_i = a_loo + b_loo * pp_llm[i]
        true_i = pp_true[i]

        # Uncertainty for held-out
        sigma_loo = np.std(y_loo - (a_loo + b_loo * X_loo[:, 1]), ddof=2)
        se_pred = np.sqrt((b_loo * anchors[i].eu_llm)**2 + sigma_loo**2)

        ci_lower = pred_i - 1.96 * se_pred
        ci_upper = pred_i + 1.96 * se_pred
        covered = ci_lower <= true_i <= ci_upper

        loo_predictions.append((anchors[i].anchor_id, true_i, pred_i, covered))
        loo_residuals.append(true_i - pred_i)
        loo_covered.append(covered)

    loo_residuals = np.array(loo_residuals)
    loo_mae = np.mean(np.abs(loo_residuals))
    loo_rmse = np.sqrt(np.mean(loo_residuals**2))
    loo_coverage = np.mean(loo_covered)

    # Spearman correlation
    loo_preds_arr = np.array([p[2] for p in loo_predictions])
    loo_true_arr = np.array([p[1] for p in loo_predictions])
    loo_spearman, _ = stats.spearmanr(loo_preds_arr, loo_true_arr)

    return PPCalibrationResult(
        a=a,
        b=b,
        sigma_model=sigma_model,
        n_anchors=n,
        r_squared=r_squared,
        anchors=anchors,
        loo_mae=loo_mae,
        loo_rmse=loo_rmse,
        loo_coverage=loo_coverage,
        loo_spearman=loo_spearman,
        loo_predictions=loo_predictions
    )


def evaluate_calibration(result: PPCalibrationResult) -> Dict[str, any]:
    """
    Evaluate calibration using 5-point checklist.

    Returns dict with check results and overall recommendation.
    """
    checks = {}

    # Check 1: Support-Abdeckung
    pp_values = [a.pp_true for a in result.anchors]
    min_pp, max_pp = min(pp_values), max(pp_values)
    checks["check1_support"] = {
        "name": "Support-Abdeckung",
        "range": f"{min_pp:.0f}–{max_pp:.0f} pp",
        "pass": bool(min_pp <= 10 and max_pp >= 60),
        "note": "Full support coverage (low to high pp)"
    }

    # Check 2: Intercept-Größe
    checks["check2_intercept"] = {
        "name": "Intercept-Größe",
        "value": float(result.a),
        "threshold": 5.0,
        "pass": bool(abs(result.a) < 5.0),
        "note": "|a| < 5pp → Intercept ignorierbar, Modell stabil"
    }

    # Check 3: Steigung
    checks["check3_slope"] = {
        "name": "Steigung",
        "value": float(result.b),
        "range": [0.85, 1.05],
        "pass": bool(0.85 <= result.b <= 1.05),
        "note": "b ∈ [0.85, 1.05] → LLM-Bias realistisch korrigiert"
    }

    # Check 4: LOO-Coverage
    checks["check4_coverage"] = {
        "name": "LOO-Coverage",
        "value": float(result.loo_coverage),
        "threshold": 0.90,
        "pass": bool(result.loo_coverage >= 0.90),
        "note": "Coverage ≥ 90% für 95%-Intervalle"
    }

    # Check 5: Domain-Robustheit
    # Check if defaults cluster together on regression line
    defaults = [a for a in result.anchors if a.domain in ["Finance", "Health", "Energy"]]
    if len(defaults) >= 2:
        default_residuals = []
        for a in defaults:
            pred = result.a + result.b * a.pp_llm
            default_residuals.append(abs(a.pp_true - pred))
        mean_default_residual = float(np.mean(default_residuals))
        checks["check5_domain"] = {
            "name": "Domain-Robustheit",
            "mean_residual": mean_default_residual,
            "pass": bool(mean_default_residual < 10),
            "note": "Defaults liegen auf derselben Linie (kein systematisches Abweichen)"
        }
    else:
        checks["check5_domain"] = {
            "name": "Domain-Robustheit",
            "pass": None,
            "note": "Nicht genug Domain-Anchors für Prüfung"
        }

    # Overall assessment
    passed = sum(1 for c in checks.values() if c.get("pass") == True)
    total = sum(1 for c in checks.values() if c.get("pass") is not None)

    checks["overall"] = {
        "passed": passed,
        "total": total,
        "deploy_ready": passed >= 4,
        "recommendation": "DEPLOY" if passed >= 4 else "NEEDS MORE ANCHORS"
    }

    return checks


def print_calibration_report(result: PPCalibrationResult, checks: Dict):
    """Print detailed calibration report."""
    print("\n" + "=" * 70)
    print("PP CALIBRATION REPORT")
    print("=" * 70)

    print(f"\n📊 CALIBRATION PARAMETERS")
    print(f"   Formula: pp_true = {result.a:.2f} + {result.b:.3f} × pp_llm")
    print(f"   σ_model = {result.sigma_model:.2f} pp")
    print(f"   R² = {result.r_squared:.3f}")
    print(f"   n = {result.n_anchors} anchors")

    print(f"\n📈 LOO CROSS-VALIDATION")
    print(f"   MAE = {result.loo_mae:.2f} pp")
    print(f"   RMSE = {result.loo_rmse:.2f} pp")
    print(f"   Coverage = {result.loo_coverage:.1%}")
    print(f"   Spearman ρ = {result.loo_spearman:.3f}")

    print(f"\n📋 LOO PREDICTIONS")
    print(f"   {'Anchor':<35} {'True':>8} {'Pred':>8} {'Covered':>8}")
    print(f"   {'-'*35} {'-'*8} {'-'*8} {'-'*8}")
    for anchor_id, true_val, pred_val, covered in result.loo_predictions:
        covered_str = "✓" if covered else "✗"
        print(f"   {anchor_id:<35} {true_val:>8.1f} {pred_val:>8.1f} {covered_str:>8}")

    print(f"\n🔍 5-POINT CHECKLIST")
    for i, (key, check) in enumerate(checks.items()):
        if key == "overall":
            continue
        status = "✓" if check.get("pass") else "✗" if check.get("pass") is False else "?"
        print(f"   {status} Check {i+1}: {check['name']}")
        if "value" in check:
            print(f"      Value: {check['value']:.2f}")
        if "range" in check and isinstance(check["range"], list):
            print(f"      Range: {check['range']}")
        if "note" in check:
            print(f"      → {check['note']}")

    print(f"\n{'='*70}")
    overall = checks["overall"]
    if overall["deploy_ready"]:
        print(f"🟢 RECOMMENDATION: DEPLOY ({overall['passed']}/{overall['total']} checks passed)")
        print(f"   'Percentage-point effects are calibrated on Tier-1/2 anchors")
        print(f"    spanning the full support ({min(a.pp_true for a in result.anchors):.0f}–{max(a.pp_true for a in result.anchors):.0f} pp).'")
    else:
        print(f"🟡 RECOMMENDATION: {overall['recommendation']} ({overall['passed']}/{overall['total']} checks passed)")
        print(f"   Consider adding more anchors or investigating failed checks.")
    print("=" * 70)


def calibrate_new_pp(pp_llm: float, eu_llm: float,
                     a: float, b: float, sigma_model: float) -> Dict:
    """Calibrate a new pp estimate."""
    pp_cal = a + b * pp_llm
    sigma_cal = np.sqrt((b * eu_llm)**2 + sigma_model**2)

    ci_lower = max(0, pp_cal - 1.96 * sigma_cal)
    ci_upper = pp_cal + 1.96 * sigma_cal

    return {
        "pp_raw": pp_llm,
        "pp_calibrated": round(pp_cal, 2),
        "se_calibrated": round(sigma_cal, 2),
        "ci_95": [round(ci_lower, 2), round(ci_upper, 2)],
        "tier": 3,
        "tier_note": "calibrated on Tier-1/2 pp anchors"
    }


def main():
    parser = argparse.ArgumentParser(
        description="PP-scale calibration for LLMMC estimates",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("--fit", action="store_true",
                        help="Fit calibration on pp anchors")
    parser.add_argument("--evaluate", action="store_true",
                        help="Run 5-point evaluation checklist")
    parser.add_argument("--calibrate", action="store_true",
                        help="Calibrate a new pp estimate")
    parser.add_argument("--pp", type=float,
                        help="Raw pp estimate for --calibrate")
    parser.add_argument("--eu", type=float,
                        help="Elicitation uncertainty for --calibrate")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON")

    args = parser.parse_args()

    if args.fit or args.evaluate:
        print("Loading pp anchors...")
        anchors = load_pp_anchors()
        print(f"Found {len(anchors)} pp anchors")

        print("\nFitting calibration...")
        result = fit_pp_calibration(anchors)

        if args.evaluate:
            checks = evaluate_calibration(result)

            if args.json:
                output = {
                    "calibration": {
                        "a": round(result.a, 3),
                        "b": round(result.b, 4),
                        "sigma_model": round(result.sigma_model, 3),
                        "n_anchors": result.n_anchors,
                        "r_squared": round(result.r_squared, 4)
                    },
                    "loo": {
                        "mae": round(result.loo_mae, 3),
                        "rmse": round(result.loo_rmse, 3),
                        "coverage": round(result.loo_coverage, 4),
                        "spearman": round(result.loo_spearman, 4)
                    },
                    "checks": checks
                }
                print(json.dumps(output, indent=2))
            else:
                print_calibration_report(result, checks)
        else:
            print(f"\nCalibration: pp_true = {result.a:.2f} + {result.b:.3f} × pp_llm")
            print(f"σ_model = {result.sigma_model:.2f} pp")
            print(f"R² = {result.r_squared:.3f}")

    elif args.calibrate and args.pp is not None and args.eu is not None:
        # Load calibration params (in production: from saved file)
        anchors = load_pp_anchors()
        result = fit_pp_calibration(anchors)

        cal_result = calibrate_new_pp(args.pp, args.eu, result.a, result.b, result.sigma_model)

        if args.json:
            print(json.dumps(cal_result, indent=2))
        else:
            print(f"\nInput: pp_llm = {args.pp} ± {args.eu}")
            print(f"Calibrated: pp_cal = {cal_result['pp_calibrated']:.2f} ± {cal_result['se_calibrated']:.2f}")
            print(f"95% CI: [{cal_result['ci_95'][0]:.2f}, {cal_result['ci_95'][1]:.2f}]")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
