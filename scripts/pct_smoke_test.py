#!/usr/bin/env python3
"""
PCT Pipeline Smoke Test
========================

End-to-end health check: Registry -> PCT -> LLMMC -> Parameter API.
Designed for CI/CD and pre-commit validation.

Exit codes:
  0 = all stages passed
  1 = one or more stages failed
"""

import sys
from pathlib import Path

# Add scripts/ to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

STAGES = []

def stage(name):
    """Decorator to register and run a pipeline stage."""
    def decorator(fn):
        STAGES.append((name, fn))
        return fn
    return decorator


# ---------------------------------------------------------------------------
# Stage 1: Registry loads
# ---------------------------------------------------------------------------
@stage("Registry loads parameters")
def check_registry():
    from parameter_api import _find_all_parameters
    params = _find_all_parameters()
    assert len(params) > 0, f"Expected >0 parameters, got {len(params)}"
    return f"{len(params)} parameters loaded"


# ---------------------------------------------------------------------------
# Stage 2: Symbol resolution
# ---------------------------------------------------------------------------
@stage("Symbol resolution (Greek + ASCII)")
def check_symbols():
    from parameter_api import _find_parameter
    p1 = _find_parameter(symbol="lambda_R")
    assert p1 is not None, "lambda_R not found"
    p2 = _find_parameter(symbol="\u03bb_R")  # Greek lambda
    assert p2 is not None, "Greek lambda_R not found"
    assert p1["id"] == p2["id"], f"Mismatch: {p1['id']} != {p2['id']}"
    return f"Resolved to {p1['id']}"


# ---------------------------------------------------------------------------
# Stage 3: get_parameter (Layer 2 only)
# ---------------------------------------------------------------------------
@stage("get_parameter (Layer 2)")
def check_get_parameter():
    from parameter_api import get_parameter
    result = get_parameter(parameter_id="PAR-BEH-001")
    assert result is not None, "PAR-BEH-001 not found"
    assert result.value > 0, f"Expected value > 0, got {result.value}"
    assert result.ci_95[0] <= result.value <= result.ci_95[1], "CI bounds violated"
    return f"value={result.value:.2f}, CI={result.ci_95}"


# ---------------------------------------------------------------------------
# Stage 4: PCT transform
# ---------------------------------------------------------------------------
@stage("PCT transform (Benabou demo)")
def check_pct():
    from pct import demo_benabou
    result = demo_benabou()
    assert result.theta_A == 2.5, f"Expected theta_A=2.5, got {result.theta_A}"
    assert 1.5 < result.theta_B < 3.0, f"theta_B out of range: {result.theta_B}"
    assert result.product_M != 1.0, "Product M should not be 1.0"
    return f"theta_A={result.theta_A} -> theta_B={result.theta_B:.3f} (M={result.product_M:.3f})"


# ---------------------------------------------------------------------------
# Stage 5: LLMMC calibration
# ---------------------------------------------------------------------------
@stage("LLMMC calibration")
def check_llmmc():
    from llmmc_calibration import LLMMCCalibrator
    cal = LLMMCCalibrator(min_anchors=5)
    examples = [
        ("Default_Action", 0.85, 0.04, 0.91, 0.05, "Madrian 2001"),
        ("Default_Trigger", 0.78, 0.05, 0.85, 0.06, "Johnson 2003"),
        ("Social_Awareness", 0.35, 0.06, 0.42, 0.09, "Allcott 2011"),
        ("Social_Action", 0.28, 0.07, 0.38, 0.10, "Schultz 2007"),
        ("Incentive_Action", 0.50, 0.08, 0.58, 0.11, "Gneezy 2011"),
        ("Commitment_Action", 0.65, 0.05, 0.72, 0.07, "Bryan 2010"),
        ("Loss_Frame", 0.45, 0.06, 0.55, 0.08, "Kahneman 1979"),
        ("Feedback_Action", 0.40, 0.06, 0.47, 0.08, "Kluger 1996"),
        ("Simplification", 0.60, 0.05, 0.68, 0.07, "Bettinger 2012"),
        ("Incentive_Maint", 0.32, 0.09, 0.45, 0.12, "Charness 2009"),
    ]
    for name, t12, se, llm, eu, src in examples:
        cal.add_anchor(name, t12, se, llm, eu, src)
    cal.fit()
    result = cal.calibrate(theta_llm=0.60, eu_llm=0.10)
    assert result.theta_final > 0, f"Expected theta_final > 0, got {result.theta_final}"
    assert result.ci_95[0] < result.ci_95[1], "CI should be an interval"
    return f"theta_final={result.theta_final:.3f}, shrinkage={result.shrinkage_factor:.3f}"


# ---------------------------------------------------------------------------
# Stage 6: PCT + LLMMC integration (Tier 2.5)
# ---------------------------------------------------------------------------
@stage("PCT + LLMMC integration (Tier 2.5)")
def check_pct_llmmc():
    from llmmc_calibration import LLMMCCalibrator
    from pct import demo_benabou
    cal = LLMMCCalibrator(min_anchors=5)
    examples = [
        ("Default_Action", 0.85, 0.04, 0.91, 0.05, "Madrian 2001"),
        ("Default_Trigger", 0.78, 0.05, 0.85, 0.06, "Johnson 2003"),
        ("Social_Awareness", 0.35, 0.06, 0.42, 0.09, "Allcott 2011"),
        ("Social_Action", 0.28, 0.07, 0.38, 0.10, "Schultz 2007"),
        ("Incentive_Action", 0.50, 0.08, 0.58, 0.11, "Gneezy 2011"),
        ("Commitment_Action", 0.65, 0.05, 0.72, 0.07, "Bryan 2010"),
        ("Loss_Frame", 0.45, 0.06, 0.55, 0.08, "Kahneman 1979"),
        ("Feedback_Action", 0.40, 0.06, 0.47, 0.08, "Kluger 1996"),
        ("Simplification", 0.60, 0.05, 0.68, 0.07, "Bettinger 2012"),
        ("Incentive_Maint", 0.32, 0.09, 0.45, 0.12, "Charness 2009"),
    ]
    for name, t12, se, llm, eu, src in examples:
        cal.add_anchor(name, t12, se, llm, eu, src)
    cal.add_pct_anchors()
    cal.fit()
    pct_result = demo_benabou()
    result = cal.calibrate_with_pct(pct_result, eu_pct=0.10)
    assert result.pct_provenance is not None, "PCT provenance missing"
    assert result.theta_final > 0, "theta_final should be > 0"
    return f"theta_final={result.theta_final:.3f}, pct_applied=True"


# ---------------------------------------------------------------------------
# Stage 7: Full Parameter API pipeline
# ---------------------------------------------------------------------------
@stage("Parameter API full pipeline")
def check_parameter_api():
    from parameter_api import lookup_parameter
    result = lookup_parameter(
        parameter_id="PAR-BEH-016",
        target_psi={"psi_S": "competence_signaling", "psi_I": "professional_hierarchy"},
        anchor_psi={"psi_S": "welfare_stigma", "psi_I": "bureaucratic_application"},
        anchor_context="welfare",
        calibrate=True,
    )
    assert result is not None, "lookup_parameter returned None"
    assert result.pct_applied is True, "PCT should be applied"
    assert result.llmmc_applied is True, "LLMMC should be applied"
    assert result.value > 0, f"Expected value > 0, got {result.value}"
    return f"value={result.value:.3f}, pct_M={result.pct_product_M:.3f}, shrinkage={result.llmmc_shrinkage:.3f}"


# ---------------------------------------------------------------------------
# Stage 8: JSON serialization
# ---------------------------------------------------------------------------
@stage("JSON serialization (to_dict)")
def check_serialization():
    import json
    from parameter_api import lookup_parameter
    result = lookup_parameter(
        parameter_id="PAR-BEH-016",
        target_psi={"psi_S": "competence_signaling"},
        anchor_psi={"psi_S": "welfare_stigma"},
        anchor_context="welfare",
    )
    assert result is not None
    d = result.to_dict()
    json_str = json.dumps(d)
    assert len(json_str) > 0, "JSON should not be empty"
    parsed = json.loads(json_str)
    assert parsed["pct"]["applied"] is True
    return f"JSON OK ({len(json_str)} bytes)"


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------
def main():
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    quiet = "--quiet" in sys.argv or "-q" in sys.argv

    passed = 0
    failed = 0
    errors = []

    if not quiet:
        print("PCT Pipeline Smoke Test")
        print("=" * 60)

    for name, fn in STAGES:
        try:
            detail = fn()
            passed += 1
            if not quiet:
                print(f"  PASS  {name}")
                if verbose and detail:
                    print(f"        -> {detail}")
        except AssertionError as e:
            failed += 1
            errors.append((name, str(e)))
            if not quiet:
                print(f"  FAIL  {name}: {e}")
        except Exception as e:
            failed += 1
            errors.append((name, f"{type(e).__name__}: {e}"))
            if not quiet:
                print(f"  ERROR {name}: {type(e).__name__}: {e}")

    if not quiet:
        print(f"\n{'=' * 60}")
        print(f"  {passed}/{passed + failed} stages passed")
        if errors:
            print(f"\n  Failures:")
            for name, err in errors:
                print(f"    {name}: {err}")
        print()

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
