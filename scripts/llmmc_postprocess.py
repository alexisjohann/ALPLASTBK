#!/usr/bin/env python3
"""
LLMMC Post-Processing Pipeline (E4–E5 + Reporting).

Reads E1-E3 elicitation results from data/llmmc-draws/, applies:
  E4: Calibration (WLS against Tier-1/2 anchors, bias correction, shrinkage)
  E5: Validation (LLP-1 reproducibility, LLP-2 calibration quality, LLP-3 bounded)

Then generates a Markdown report with:
  - Parameter table (all 17 behavioral parameters)
  - Calibration diagnostics (anchor quality, LOO-CV)
  - LLP compliance summary
  - Uncertainty decomposition per parameter

Usage:
    # Process all elicitation results in data/llmmc-draws/
    python scripts/llmmc_postprocess.py

    # Process specific file
    python scripts/llmmc_postprocess.py --input data/llmmc-draws/LLMMC_PAR-BEH-001_*.yaml

    # Generate report only (no recalibration)
    python scripts/llmmc_postprocess.py --report-only

    # Custom output directory
    python scripts/llmmc_postprocess.py --output-dir outputs/llmmc-reports/

Architecture (Three-Layer compliant):
  Layer 1: This script (formal computation — E4 calibration, E5 validation)
  Layer 2: YAML input/output (parameter store)
  Layer 3: Markdown report (human-readable translation)

Author: EBF Framework
Date: 2026-02-16
Protocol: E4-CAL, E5-VAL, LLP-1/2/3, AN-DIAG
"""

import argparse
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed. Run: pip install pyyaml")
    sys.exit(1)

# Add scripts/ to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from llmmc_calibration import (
    LLMMCCalibrator,
    CalibrationResult,
    LOOResult,
    UncertaintyDecomposition,
    AnchorDiagnostic,
    create_example_calibration_set,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
DRAWS_DIR = REPO_ROOT / "data" / "llmmc-draws"
REPORT_DIR = REPO_ROOT / "outputs" / "llmmc-reports"
PARAMETER_REGISTRY = REPO_ROOT / "data" / "parameter-registry.yaml"


# ──────────────────────────────────────────────────────────────────────
# Data Structures
# ──────────────────────────────────────────────────────────────────────

@dataclass
class ParameterResult:
    """Complete result for one parameter through E1-E5."""
    param_id: str
    symbol: str
    name: str
    # E3 (from elicitation file)
    theta_llm: float
    sigma_elicit: float
    cv: float
    n_valid: int
    n_draws: int
    draws: List[float]
    ci_90_llm: Tuple[float, float]
    # E4 (calibration)
    theta_calibrated: float
    theta_final: float
    sigma_final: float
    ci_95: Tuple[float, float]
    shrinkage_factor: float
    uncertainty: Optional[UncertaintyDecomposition] = None
    # E5 (validation)
    literature_value: Optional[float] = None
    literature_deviation: Optional[float] = None
    lit_in_ci: Optional[bool] = None
    # LLP checks
    llp1_pass: bool = False  # CV < 0.5
    llp2_pass: bool = False  # R² > 0.3 (global, not per-param)
    llp3_pass: bool = False  # σ bounded
    # Metadata
    model: str = "gpt-4o"
    temperature: float = 0.8
    timestamp: str = ""
    source_file: str = ""


@dataclass
class PipelineReport:
    """Complete pipeline report across all parameters."""
    parameters: List[ParameterResult]
    # Global calibration
    n_anchors: int = 0
    cal_a: float = 0.0
    cal_b: float = 0.0
    r_squared: float = 0.0
    sigma_model: float = 0.0
    # LOO-CV (LLP-2)
    loo_mae: float = 0.0
    loo_rmse: float = 0.0
    loo_coverage: float = 0.0
    loo_spearman: float = 0.0
    loo_acceptable: bool = False
    # Anchor diagnostics
    n_flagged_anchors: int = 0
    flagged_anchors: List[Dict] = field(default_factory=list)
    # Summary
    n_params_total: int = 0
    n_params_llp_pass: int = 0
    timestamp: str = ""


# ──────────────────────────────────────────────────────────────────────
# E4: Calibration
# ──────────────────────────────────────────────────────────────────────

def build_calibrator() -> LLMMCCalibrator:
    """Build and fit the LLMMC calibrator with all available anchors."""
    cal = LLMMCCalibrator(min_anchors=10, use_isotonic=False)

    # Add literature-based anchors
    anchors = create_example_calibration_set()
    cal.add_anchors_from_dict(anchors)

    # Add PCT-derived anchors from measurement contexts
    n_pct = cal.add_pct_anchors()

    # Fit
    cal.fit()

    return cal


def compute_r_squared(cal: LLMMCCalibrator) -> float:
    """Compute R² for the calibration fit."""
    theta_t12 = np.array([a.theta_t12 for a in cal.anchors])
    theta_llm = np.array([a.theta_llm for a in cal.anchors])
    theta_pred = cal.a + cal.b * theta_llm
    ss_res = np.sum((theta_t12 - theta_pred) ** 2)
    ss_tot = np.sum((theta_t12 - np.mean(theta_t12)) ** 2)
    return 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0


# ──────────────────────────────────────────────────────────────────────
# Load Elicitation Results
# ──────────────────────────────────────────────────────────────────────

def load_elicitation_files(draws_dir: Path) -> List[Dict]:
    """Load all LLMMC_*.yaml files from the draws directory."""
    files = sorted(draws_dir.glob("LLMMC_PAR-*.yaml"))
    results = []
    for f in files:
        with open(f) as fh:
            data = yaml.safe_load(fh)
        if data and "llmmc_elicitation" in data:
            data["_source_file"] = str(f)
            results.append(data)
    return results


def load_literature_values() -> Dict[str, float]:
    """Load literature reference values from parameter registry."""
    if not PARAMETER_REGISTRY.exists():
        return {}

    with open(PARAMETER_REGISTRY) as f:
        registry = yaml.safe_load(f)

    lit_values = {}
    for category in registry:
        if category == "metadata":
            continue
        params = registry[category]
        if not isinstance(params, list):
            continue
        for p in params:
            pid = p.get("id", "")
            values = p.get("values", {})
            lit = values.get("literature", {})
            if lit.get("mean") is not None:
                lit_values[pid] = lit["mean"]

    return lit_values


# ──────────────────────────────────────────────────────────────────────
# E5: Validation + LLP Checks
# ──────────────────────────────────────────────────────────────────────

def process_parameter(
    elicit_data: Dict,
    cal: LLMMCCalibrator,
    r_squared: float,
    lit_values: Dict[str, float],
) -> ParameterResult:
    """Process one parameter through E4-E5."""
    e = elicit_data["llmmc_elicitation"]
    param_id = e["parameter_id"]

    # E4: Calibrate
    cal_result = cal.calibrate(
        theta_llm=e["theta_llm"],
        eu_llm=e["sigma_elicit"],
    )

    # E5: Literature comparison
    lit_val = lit_values.get(param_id)
    lit_dev = None
    lit_in_ci = None
    if lit_val is not None and lit_val != 0:
        lit_dev = (cal_result.theta_final - lit_val) / abs(lit_val)
        lit_in_ci = cal_result.ci_95[0] <= lit_val <= cal_result.ci_95[1]

    # LLP checks
    cv = e.get("cv", float("inf"))
    llp1 = cv < 0.5                     # Reproducibility
    llp2 = r_squared > 0.3              # Calibration quality (global)
    sigma_ratio = cal_result.sigma_final / abs(cal_result.theta_final) \
        if cal_result.theta_final != 0 else float("inf")
    llp3 = sigma_ratio < 1.0            # Bounded uncertainty

    return ParameterResult(
        param_id=param_id,
        symbol=e.get("parameter_symbol", ""),
        name=e.get("parameter_name", ""),
        theta_llm=e["theta_llm"],
        sigma_elicit=e["sigma_elicit"],
        cv=cv,
        n_valid=e.get("n_valid", e.get("n_draws", 0)),
        n_draws=e.get("n_draws", 0),
        draws=e.get("draws", []),
        ci_90_llm=tuple(e.get("ci_90", [0, 0])),
        theta_calibrated=cal_result.theta_calibrated,
        theta_final=cal_result.theta_final,
        sigma_final=cal_result.sigma_final,
        ci_95=cal_result.ci_95,
        shrinkage_factor=cal_result.shrinkage_factor,
        uncertainty=cal_result.uncertainty,
        literature_value=lit_val,
        literature_deviation=lit_dev,
        lit_in_ci=lit_in_ci,
        llp1_pass=llp1,
        llp2_pass=llp2,
        llp3_pass=llp3,
        model=e.get("model", "gpt-4o"),
        temperature=e.get("temperature", 0.8),
        timestamp=e.get("timestamp", ""),
        source_file=elicit_data.get("_source_file", ""),
    )


# ──────────────────────────────────────────────────────────────────────
# Reporting
# ──────────────────────────────────────────────────────────────────────

def generate_report(report: PipelineReport) -> str:
    """Generate Markdown report for the complete LLMMC pipeline run."""
    ts = report.timestamp or datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    n = report.n_params_total
    n_pass = report.n_params_llp_pass

    lines = [
        f"# LLMMC Pipeline Report",
        f"",
        f"**Generated:** {ts}",
        f"**Parameters:** {n} elicited, {n_pass} LLP-compliant ({n_pass}/{n})",
        f"**Protocol:** E1→E2→E3→E4→E5 (Appendix AN v2.0)",
        f"",
        f"---",
        f"",
        f"## 1. Calibration Summary (E4)",
        f"",
        f"| Property | Value |",
        f"|----------|-------|",
        f"| Anchors (n) | {report.n_anchors} |",
        f"| Level calibration | θ_cal = {report.cal_a:.4f} + {report.cal_b:.4f} × θ_LLM |",
        f"| R² | {report.r_squared:.4f} |",
        f"| σ_model | {report.sigma_model:.4f} |",
        f"| Flagged anchors | {report.n_flagged_anchors} |",
        f"",
    ]

    # Flagged anchors detail
    if report.flagged_anchors:
        lines.extend([
            f"### Flagged Anchors (AN-DIAG)",
            f"",
            f"| Anchor | Cook's D | Leverage | |stud. resid| | Reasons |",
            f"|--------|----------|----------|--------------|---------—|",
        ])
        for fa in report.flagged_anchors:
            lines.append(
                f"| {fa['name'][:30]} | {fa['cooks_d']:.3f} | "
                f"{fa['leverage']:.3f} | {abs(fa['studentized_residual']):.2f} | "
                f"{'; '.join(fa.get('flag_reasons', []))} |"
            )
        lines.append("")

    # LOO-CV
    lines.extend([
        f"## 2. Cross-Validation (LLP-2, HHH-CAL-1)",
        f"",
        f"| Metric | Value | Threshold | Status |",
        f"|--------|-------|-----------|--------|",
        f"| MAE | {report.loo_mae:.4f} | < 0.12 | {'PASS' if report.loo_mae < 0.12 else 'FAIL'} |",
        f"| RMSE | {report.loo_rmse:.4f} | < 0.15 | {'PASS' if report.loo_rmse < 0.15 else 'FAIL'} |",
        f"| Coverage (95%) | {report.loo_coverage:.1%} | [85%, 98%] | {'PASS' if 0.85 <= report.loo_coverage <= 0.98 else 'FAIL'} |",
        f"| Spearman ρ | {report.loo_spearman:.4f} | > 0.70 | {'PASS' if report.loo_spearman > 0.70 else 'FAIL'} |",
        f"| **Overall LLP-2** | | | **{'PASS' if report.loo_acceptable else 'FAIL'}** |",
        f"",
    ])

    # Parameter table
    lines.extend([
        f"## 3. Parameter Results (E3→E4→E5)",
        f"",
        f"| ID | Symbol | θ_LLM | σ_elicit | θ_final | σ_final | 95% CI | Lit | Dev | LLP |",
        f"|-------|--------|-------|----------|---------|---------|--------|------|------|-----|",
    ])

    for p in report.parameters:
        lit_str = f"{p.literature_value:.3f}" if p.literature_value is not None else "—"
        dev_str = f"{p.literature_deviation:+.1%}" if p.literature_deviation is not None else "—"
        llp_all = p.llp1_pass and p.llp2_pass and p.llp3_pass
        llp_str = "YES" if llp_all else "NO"
        ci_str = f"[{p.ci_95[0]:.3f}, {p.ci_95[1]:.3f}]"
        lines.append(
            f"| {p.param_id} | {p.symbol} | {p.theta_llm:.4f} | "
            f"{p.sigma_elicit:.4f} | {p.theta_final:.4f} | "
            f"{p.sigma_final:.4f} | {ci_str} | {lit_str} | {dev_str} | {llp_str} |"
        )

    lines.append("")

    # LLP detail per parameter
    lines.extend([
        f"## 4. LLP Compliance Detail",
        f"",
        f"| ID | LLP-1 (CV<0.5) | LLP-2 (R²>0.3) | LLP-3 (σ bounded) | All |",
        f"|-------|-----------------|-----------------|--------------------|----|",
    ])

    for p in report.parameters:
        all_pass = p.llp1_pass and p.llp2_pass and p.llp3_pass
        lines.append(
            f"| {p.param_id} | "
            f"{'PASS' if p.llp1_pass else 'FAIL'} (CV={p.cv:.3f}) | "
            f"{'PASS' if p.llp2_pass else 'FAIL'} | "
            f"{'PASS' if p.llp3_pass else 'FAIL'} | "
            f"{'YES' if all_pass else 'NO'} |"
        )

    lines.append("")

    # Uncertainty decomposition
    has_uncertainty = any(p.uncertainty is not None for p in report.parameters)
    if has_uncertainty:
        lines.extend([
            f"## 5. Uncertainty Decomposition (AN-A5)",
            f"",
            f"| ID | σ_elicit | σ_calib | σ_model | σ_context | σ_total | Dominant |",
            f"|-------|----------|---------|---------|-----------|---------|----------|",
        ])
        for p in report.parameters:
            if p.uncertainty:
                u = p.uncertainty
                lines.append(
                    f"| {p.param_id} | {u.sigma_elicit:.4f} | "
                    f"{u.sigma_calib:.4f} | {u.sigma_model:.4f} | "
                    f"{u.sigma_context:.4f} | {u.sigma_total:.4f} | "
                    f"{u.dominant_source()} |"
                )
        lines.append("")

    # Literature comparison
    params_with_lit = [p for p in report.parameters if p.literature_value is not None]
    if params_with_lit:
        n_in_ci = sum(1 for p in params_with_lit if p.lit_in_ci)
        lines.extend([
            f"## 6. Literature Comparison (E5)",
            f"",
            f"**Literature in 95% CI:** {n_in_ci}/{len(params_with_lit)} "
            f"({n_in_ci/len(params_with_lit):.0%})",
            f"",
            f"| ID | θ_final | Lit value | Deviation | In CI |",
            f"|-------|---------|-----------|-----------|-------|",
        ])
        for p in params_with_lit:
            lines.append(
                f"| {p.param_id} | {p.theta_final:.4f} | "
                f"{p.literature_value:.4f} | {p.literature_deviation:+.1%} | "
                f"{'YES' if p.lit_in_ci else 'NO'} |"
            )
        lines.append("")

    # Summary box
    lines.extend([
        f"---",
        f"",
        f"## Summary",
        f"",
        f"```",
        f"Pipeline:     E1 -> E2 -> E3 -> E4 -> E5",
        f"Parameters:   {n} elicited",
        f"LLP-pass:     {n_pass}/{n} ({n_pass/n:.0%})" if n > 0 else f"LLP-pass:     0/0",
        f"Calibration:  R² = {report.r_squared:.4f}, n_anchors = {report.n_anchors}",
        f"LOO-CV:       MAE = {report.loo_mae:.4f}, ρ = {report.loo_spearman:.4f}",
        f"LLP-2:        {'PASS' if report.loo_acceptable else 'FAIL'}",
        f"```",
        f"",
    ])

    return "\n".join(lines)


def save_calibrated_yaml(report: PipelineReport, output_dir: Path) -> Path:
    """Save calibrated results as YAML for downstream consumption."""
    output_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = output_dir / f"LLMMC_calibrated_{ts}.yaml"

    data = {
        "llmmc_calibrated": {
            "timestamp": report.timestamp,
            "calibration": {
                "n_anchors": report.n_anchors,
                "a": round(report.cal_a, 6),
                "b": round(report.cal_b, 6),
                "r_squared": round(report.r_squared, 6),
                "sigma_model": round(report.sigma_model, 6),
            },
            "loo_cv": {
                "mae": round(report.loo_mae, 6),
                "rmse": round(report.loo_rmse, 6),
                "coverage_95": round(report.loo_coverage, 4),
                "spearman_rho": round(report.loo_spearman, 6),
                "acceptable": report.loo_acceptable,
            },
            "parameters": [],
        },
        "pipeline_status": {
            "e1_prompt": "completed",
            "e2_draws": "completed",
            "e3_aggregation": "completed",
            "e4_calibration": "completed",
            "e5_validation": "completed",
        },
    }

    for p in report.parameters:
        entry = {
            "id": p.param_id,
            "symbol": p.symbol,
            "name": p.name,
            "e3_theta_llm": round(p.theta_llm, 6),
            "e3_sigma_elicit": round(p.sigma_elicit, 6),
            "e3_cv": round(p.cv, 6),
            "e3_n_valid": p.n_valid,
            "e4_theta_calibrated": round(p.theta_calibrated, 6),
            "e4_theta_final": round(p.theta_final, 6),
            "e4_sigma_final": round(p.sigma_final, 6),
            "e4_ci_95": [round(p.ci_95[0], 6), round(p.ci_95[1], 6)],
            "e4_shrinkage": round(p.shrinkage_factor, 6),
            "llp1_pass": p.llp1_pass,
            "llp2_pass": p.llp2_pass,
            "llp3_pass": p.llp3_pass,
            "llp_all_pass": p.llp1_pass and p.llp2_pass and p.llp3_pass,
        }
        if p.literature_value is not None:
            entry["literature_value"] = p.literature_value
            entry["literature_deviation"] = round(p.literature_deviation, 6)
            entry["literature_in_ci"] = p.lit_in_ci
        if p.uncertainty:
            entry["uncertainty"] = p.uncertainty.to_dict()
        data["llmmc_calibrated"]["parameters"].append(entry)

    with open(path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True,
                  sort_keys=False)

    return path


# ──────────────────────────────────────────────────────────────────────
# Main Pipeline
# ──────────────────────────────────────────────────────────────────────

def run_pipeline(
    draws_dir: Path = DRAWS_DIR,
    output_dir: Path = REPORT_DIR,
    specific_file: Optional[str] = None,
) -> PipelineReport:
    """Run the complete E4-E5 pipeline on all elicitation results."""
    print("=" * 65)
    print("  LLMMC Post-Processing Pipeline (E4-E5)")
    print("=" * 65)

    # Load elicitation files
    if specific_file:
        files_to_load = [Path(specific_file)]
        elicit_results = []
        for f in files_to_load:
            with open(f) as fh:
                data = yaml.safe_load(fh)
            if data and "llmmc_elicitation" in data:
                data["_source_file"] = str(f)
                elicit_results.append(data)
    else:
        elicit_results = load_elicitation_files(draws_dir)

    if not elicit_results:
        print(f"\n  No elicitation results found in {draws_dir}")
        print(f"  Run the elicitation first: python scripts/llmmc_elicitation.py --all-behavioral")
        print(f"  Or use --synthetic for testing: python scripts/llmmc_elicitation.py --all-behavioral --synthetic")
        return PipelineReport(parameters=[], timestamp=datetime.now(timezone.utc).isoformat())

    print(f"\n  Found {len(elicit_results)} elicitation result(s)")

    # E4: Build calibrator
    print(f"\n── E4: Building Calibrator ──")
    cal = build_calibrator()
    r_sq = compute_r_squared(cal)
    params = cal.get_calibration_params()
    print(f"  Anchors:   {params['n_anchors']}")
    print(f"  Level cal: θ_cal = {params['a']:.4f} + {params['b']:.4f} × θ_LLM")
    print(f"  R²:        {r_sq:.4f}")
    print(f"  σ_model:   {params['sigma_model']:.4f}")

    # LOO-CV
    print(f"\n── E4: LOO Cross-Validation ──")
    loo = cal.loo_cross_validation()
    print(f"  MAE:       {loo.mae:.4f} {'PASS' if loo.mae < 0.12 else 'FAIL'}")
    print(f"  RMSE:      {loo.rmse:.4f} {'PASS' if loo.rmse < 0.15 else 'FAIL'}")
    print(f"  Coverage:  {loo.coverage_95:.1%} {'PASS' if 0.85 <= loo.coverage_95 <= 0.98 else 'FAIL'}")
    print(f"  Spearman:  {loo.spearman_rho:.4f} {'PASS' if loo.spearman_rho > 0.70 else 'FAIL'}")
    print(f"  Overall:   {'ACCEPTABLE' if loo.is_acceptable() else 'NOT ACCEPTABLE'}")

    # Anchor diagnostics
    diags = cal.diagnose_anchors()
    flagged = [d for d in diags if d.flagged]
    if flagged:
        print(f"\n  Flagged anchors: {len(flagged)}")
        for d in flagged:
            print(f"    WARNING: {d.name} ({', '.join(d.flag_reasons)})")

    # Load literature values
    lit_values = load_literature_values()
    print(f"\n  Literature references loaded: {len(lit_values)}")

    # E5: Process each parameter
    print(f"\n── E5: Processing Parameters ──")
    param_results = []
    for elicit_data in elicit_results:
        try:
            result = process_parameter(elicit_data, cal, r_sq, lit_values)
            all_pass = result.llp1_pass and result.llp2_pass and result.llp3_pass
            status = "LLP-PASS" if all_pass else "LLP-FAIL"
            print(f"  {result.param_id}: θ={result.theta_final:.4f} ± {result.sigma_final:.4f} [{status}]")
            param_results.append(result)
        except Exception as e:
            pid = elicit_data.get("llmmc_elicitation", {}).get("parameter_id", "?")
            print(f"  {pid}: ERROR — {e}")

    # Build report
    n_pass = sum(1 for p in param_results
                 if p.llp1_pass and p.llp2_pass and p.llp3_pass)

    report = PipelineReport(
        parameters=param_results,
        n_anchors=params["n_anchors"],
        cal_a=params["a"],
        cal_b=params["b"],
        r_squared=r_sq,
        sigma_model=params["sigma_model"],
        loo_mae=loo.mae,
        loo_rmse=loo.rmse,
        loo_coverage=loo.coverage_95,
        loo_spearman=loo.spearman_rho,
        loo_acceptable=loo.is_acceptable(),
        n_flagged_anchors=len(flagged),
        flagged_anchors=[d.to_dict() for d in flagged],
        n_params_total=len(param_results),
        n_params_llp_pass=n_pass,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )

    # Generate outputs
    output_dir.mkdir(parents=True, exist_ok=True)

    # Markdown report
    md_content = generate_report(report)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    md_path = output_dir / f"LLMMC_report_{ts}.md"
    with open(md_path, "w") as f:
        f.write(md_content)
    print(f"\n  Report saved: {md_path}")

    # Calibrated YAML
    yaml_path = save_calibrated_yaml(report, output_dir)
    print(f"  YAML saved:   {yaml_path}")

    # Summary
    print(f"\n{'=' * 65}")
    print(f"  PIPELINE COMPLETE")
    print(f"  Parameters:  {len(param_results)} processed")
    print(f"  LLP-pass:    {n_pass}/{len(param_results)}")
    print(f"  LOO-CV:      {'ACCEPTABLE' if loo.is_acceptable() else 'NOT ACCEPTABLE'}")
    print(f"  Report:      {md_path}")
    print(f"{'=' * 65}\n")

    return report


# ──────────────────────────────────────────────────────────────────────
# Synthetic Test Mode
# ──────────────────────────────────────────────────────────────────────

def run_synthetic_e2e(output_dir: Path = REPORT_DIR) -> PipelineReport:
    """Run complete E1→E5 pipeline with synthetic data for testing."""
    from llmmc_elicitation import (
        load_parameter_from_registry,
        generate_synthetic_draws,
        aggregate_draws,
        save_result,
        ParameterSpec,
    )

    print("=" * 65)
    print("  LLMMC SYNTHETIC E2E TEST (E1→E5)")
    print("=" * 65)

    # Generate synthetic elicitation for all behavioral params
    registry_path = PARAMETER_REGISTRY
    with open(registry_path) as f:
        registry = yaml.safe_load(f)

    params = registry.get("behavioral_parameters", [])
    print(f"\n  Generating synthetic draws for {len(params)} parameters...")

    draws_dir = DRAWS_DIR
    draws_dir.mkdir(parents=True, exist_ok=True)

    for p in params:
        try:
            param = load_parameter_from_registry(p["id"])
            draws = generate_synthetic_draws(param, n_draws=15, temperature=0.8)
            result = aggregate_draws(draws, param, "synthetic-gpt-4o", 0.8)
            save_result(result, draws_dir)
            print(f"  {p['id']}: θ={result.theta_llm:.4f} (synthetic)")
        except Exception as e:
            print(f"  {p['id']}: SKIP — {e}")

    # Now run the full pipeline on synthetic data
    print()
    return run_pipeline(draws_dir=draws_dir, output_dir=output_dir)


def main():
    parser = argparse.ArgumentParser(
        description="LLMMC Post-Processing Pipeline (E4-E5 + Reporting)"
    )
    parser.add_argument("--input", type=str,
                        help="Specific elicitation YAML to process")
    parser.add_argument("--output-dir", type=str, default=str(REPORT_DIR),
                        help=f"Output directory (default: {REPORT_DIR})")
    parser.add_argument("--draws-dir", type=str, default=str(DRAWS_DIR),
                        help=f"Draws directory (default: {DRAWS_DIR})")
    parser.add_argument("--synthetic-e2e", action="store_true",
                        help="Run synthetic E1→E5 test (no API needed)")
    parser.add_argument("--report-only", action="store_true",
                        help="Generate report from existing calibrated YAML")

    args = parser.parse_args()
    output_dir = Path(args.output_dir)

    if args.synthetic_e2e:
        run_synthetic_e2e(output_dir)
    else:
        run_pipeline(
            draws_dir=Path(args.draws_dir),
            output_dir=output_dir,
            specific_file=args.input,
        )


if __name__ == "__main__":
    main()
