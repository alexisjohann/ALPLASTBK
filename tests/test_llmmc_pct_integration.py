#!/usr/bin/env python3
"""
Tests for PCT-LLMMC Integration (PCT-CAL-1)
=============================================

Verifies that PCT-transformed parameters can be used as informed priors
for the LLMMC calibration pipeline.

Tests cover:
  - _parse_numeric_value: Parsing various value_estimate formats
  - add_pct_anchors: Loading measurement_contexts as calibration anchors
  - calibrate_with_pct: End-to-end PCT → LLMMC calibration
  - CalibrationResult.pct_provenance: Provenance tracking
"""

import sys
from pathlib import Path

# Add scripts/ to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from llmmc_calibration import (
    LLMMCCalibrator,
    CalibrationAnchor,
    CalibrationResult,
    _parse_numeric_value,
)
from pct import (
    PCTResult,
    PsiDelta,
    transform,
    transform_with_deltas,
    transform_from_contexts,
    demo_benabou,
)


# ---------------------------------------------------------------------------
# _parse_numeric_value tests
# ---------------------------------------------------------------------------

def test_parse_direct_float():
    """Direct float string."""
    assert _parse_numeric_value("0.57") == 0.57
    assert _parse_numeric_value("2.5") == 2.5
    assert _parse_numeric_value("-0.3") == -0.3


def test_parse_integer():
    """Integer string."""
    assert _parse_numeric_value("3") == 3.0
    assert _parse_numeric_value("0") == 0.0


def test_parse_range_midpoint():
    """Range 'lo-hi' → midpoint."""
    val = _parse_numeric_value("0.60-0.80")
    assert val is not None
    assert abs(val - 0.70) < 0.001


def test_parse_range_with_dash():
    """Range with en-dash."""
    val = _parse_numeric_value("0.20\u20130.40")  # en-dash
    assert val is not None
    assert abs(val - 0.30) < 0.001


def test_parse_percentage():
    """Percentage string."""
    val = _parse_numeric_value("-10.1%")
    assert val is not None
    assert abs(val - (-0.101)) < 0.001

    val2 = _parse_numeric_value("5%")
    assert val2 is not None
    assert abs(val2 - 0.05) < 0.001


def test_parse_embedded_approx():
    """Embedded number with ≈."""
    val = _parse_numeric_value("λ_R ≈ 2.5")
    assert val is not None
    assert abs(val - 2.5) < 0.001


def test_parse_embedded_tilde():
    """Embedded number with ~."""
    val = _parse_numeric_value("delta_S ~ 0.15 per period")
    assert val is not None
    assert abs(val - 0.15) < 0.001


def test_parse_embedded_equals():
    """Embedded number with =."""
    val = _parse_numeric_value("β = 0.82")
    assert val is not None
    assert abs(val - 0.82) < 0.001


def test_parse_qualitative_returns_none():
    """Qualitative strings return None."""
    assert _parse_numeric_value("positive (β > 0)") is None
    assert _parse_numeric_value("high persuasion") is None
    assert _parse_numeric_value("varies") is None


def test_parse_empty_returns_none():
    """Empty/blank strings return None."""
    assert _parse_numeric_value("") is None
    assert _parse_numeric_value("   ") is None
    assert _parse_numeric_value(None.__str__() if False else "") is None


# ---------------------------------------------------------------------------
# add_pct_anchors tests
# ---------------------------------------------------------------------------

def test_add_pct_anchors_loads():
    """add_pct_anchors loads from pct-measurement-contexts.yaml."""
    cal = LLMMCCalibrator(min_anchors=1)
    n = cal.add_pct_anchors()
    # Should find at least some parseable numeric values
    assert n > 0, f"Expected >0 anchors from measurement_contexts, got {n}"
    assert len(cal.anchors) == n


def test_add_pct_anchors_names():
    """Anchors get meaningful names from parameter + context."""
    cal = LLMMCCalibrator(min_anchors=1)
    cal.add_pct_anchors()
    for anchor in cal.anchors:
        assert "_" in anchor.name, f"Anchor name should be param_context, got '{anchor.name}'"
        assert anchor.source != "unknown"


def test_add_pct_anchors_bias():
    """LLM estimates have systematic overestimation bias (larger absolute value)."""
    cal = LLMMCCalibrator(min_anchors=1)
    cal.add_pct_anchors()
    for anchor in cal.anchors:
        # LLM overestimates magnitude: |theta_llm| > |theta_t12|
        assert abs(anchor.theta_llm) > abs(anchor.theta_t12), \
            f"LLM should overestimate magnitude: |{anchor.theta_llm}| > |{anchor.theta_t12}|"


def test_add_pct_anchors_missing_file():
    """Missing file returns 0 anchors with warning."""
    cal = LLMMCCalibrator(min_anchors=1)
    n = cal.add_pct_anchors(contexts_path=Path("/nonexistent/path.yaml"))
    assert n == 0


# ---------------------------------------------------------------------------
# calibrate_with_pct tests
# ---------------------------------------------------------------------------

def _fitted_calibrator() -> LLMMCCalibrator:
    """Create a calibrator fitted with example + PCT anchors."""
    cal = LLMMCCalibrator(min_anchors=5)

    # Add manual anchors to ensure enough for fitting
    examples = [
        ("Default_Action", 0.85, 0.04, 0.91, 0.05, "Madrian 2001"),
        ("Default_Trigger", 0.78, 0.05, 0.85, 0.06, "Johnson 2003"),
        ("Social_Awareness", 0.35, 0.06, 0.42, 0.09, "Allcott 2011"),
        ("Social_Action", 0.28, 0.07, 0.38, 0.10, "Schultz 2007"),
        ("Incentive_Action", 0.50, 0.08, 0.58, 0.11, "Gneezy 2011"),
        ("Incentive_Maint", 0.32, 0.09, 0.45, 0.12, "Charness 2009"),
        ("Commitment_Action", 0.65, 0.05, 0.72, 0.07, "Bryan 2010"),
        ("Loss_Frame", 0.45, 0.06, 0.55, 0.08, "Kahneman 1979"),
        ("Feedback_Action", 0.40, 0.06, 0.47, 0.08, "Kluger 1996"),
        ("Simplification", 0.60, 0.05, 0.68, 0.07, "Bettinger 2012"),
    ]
    for name, t12, se, llm, eu, src in examples:
        cal.add_anchor(name, t12, se, llm, eu, src)

    # Also add PCT anchors
    cal.add_pct_anchors()

    cal.fit()
    return cal


def test_calibrate_with_pct_basic():
    """calibrate_with_pct produces valid CalibrationResult."""
    cal = _fitted_calibrator()
    pct_result = demo_benabou()

    result = cal.calibrate_with_pct(pct_result, eu_pct=0.10)

    assert isinstance(result, CalibrationResult)
    assert result.theta_raw > 0
    assert result.theta_final > 0
    assert result.ci_95[0] < result.theta_final < result.ci_95[1]
    assert result.tier == 3


def test_calibrate_with_pct_provenance():
    """PCT provenance is tracked in CalibrationResult."""
    cal = _fitted_calibrator()
    pct_result = demo_benabou()

    result = cal.calibrate_with_pct(pct_result, eu_pct=0.10)

    assert result.pct_provenance is not None
    prov = result.pct_provenance
    assert "theta_A" in prov
    assert "theta_B_pct" in prov
    assert "product_M" in prov
    assert "anchor_context" in prov
    assert "target_context" in prov
    assert "parameter_symbol" in prov
    assert "n_psi_dimensions" in prov
    assert prov["theta_A"] == round(pct_result.theta_A, 4)
    assert prov["theta_B_pct"] == round(pct_result.theta_B, 4)


def test_calibrate_with_pct_tier_note():
    """Tier note mentions PCT-informed."""
    cal = _fitted_calibrator()
    pct_result = demo_benabou()

    result = cal.calibrate_with_pct(pct_result, eu_pct=0.10)

    assert "PCT-informed" in result.tier_note
    assert "Tier 2.5" in result.tier_note


def test_calibrate_with_pct_to_dict():
    """to_dict includes pct_provenance."""
    cal = _fitted_calibrator()
    pct_result = demo_benabou()

    result = cal.calibrate_with_pct(pct_result, eu_pct=0.10)
    d = result.to_dict()

    assert "pct_provenance" in d
    assert d["pct_provenance"]["parameter_symbol"] == "lambda_R"

    # Verify JSON-serializable
    import json
    json_str = json.dumps(d)
    assert len(json_str) > 0


def test_calibrate_with_pct_unfitted_raises():
    """Calling calibrate_with_pct before fit() raises RuntimeError."""
    cal = LLMMCCalibrator(min_anchors=1)
    pct_result = demo_benabou()

    try:
        cal.calibrate_with_pct(pct_result)
        assert False, "Should have raised RuntimeError"
    except RuntimeError:
        pass


def test_calibrate_with_pct_no_shrinkage():
    """calibrate_with_pct with apply_shrinkage=False."""
    cal = _fitted_calibrator()
    pct_result = demo_benabou()

    result = cal.calibrate_with_pct(pct_result, apply_shrinkage=False)

    assert result.shrinkage_factor == 1.0
    assert result.theta_final == result.theta_calibrated


def test_calibrate_with_pct_lower_uncertainty():
    """PCT estimates should have lower calibrated uncertainty than raw LLM."""
    cal = _fitted_calibrator()
    pct_result = demo_benabou()

    # PCT-informed: lower eu
    result_pct = cal.calibrate_with_pct(pct_result, eu_pct=0.10)

    # Raw LLM: higher eu
    result_llm = cal.calibrate(theta_llm=pct_result.theta_B, eu_llm=0.15)

    # Compare sigma_final directly (not clipped CIs, since calibrate()
    # clips to [0,1] which makes CIs artificially narrow for theta > 1)
    assert result_pct.sigma_final <= result_llm.sigma_final + 0.01, \
        f"PCT sigma ({result_pct.sigma_final:.3f}) should be <= LLM sigma ({result_llm.sigma_final:.3f})"


# ---------------------------------------------------------------------------
# End-to-end integration test
# ---------------------------------------------------------------------------

def test_end_to_end_pct_llmmc():
    """
    Full pipeline: measurement_contexts → PCT transform → LLMMC calibrate.

    Demonstrates the complete Tier 2.5 workflow:
    1. Load PCT anchors from measurement_contexts
    2. Fit calibrator on empirical + PCT anchors
    3. Transform parameter using PCT
    4. Calibrate the PCT result through LLMMC
    """
    # Step 1-2: Create fitted calibrator with PCT anchors
    cal = _fitted_calibrator()

    # Step 3: PCT transform (Benabou welfare → workplace)
    pct_result = transform_from_contexts(
        2.5,
        anchor_psi={"psi_S": "welfare_stigma", "psi_I": "bureaucratic_application"},
        target_psi={"psi_S": "competence_signaling", "psi_I": "professional_hierarchy"},
        anchor_context="welfare",
        target_context="workplace",
        parameter_symbol="lambda_R",
        parameter_id="PAR-BEH-016",
    )

    # Step 4: Calibrate through LLMMC
    result = cal.calibrate_with_pct(pct_result, eu_pct=0.10)

    # Verify the full chain
    assert result.theta_final > 0
    assert result.pct_provenance is not None
    assert result.pct_provenance["anchor_context"] == "welfare"
    assert result.pct_provenance["target_context"] == "workplace"
    assert result.pct_provenance["parameter_symbol"] == "lambda_R"
    assert result.ci_95[0] < result.ci_95[1]


# ---------------------------------------------------------------------------
# Run tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    tests = [
        # _parse_numeric_value
        test_parse_direct_float,
        test_parse_integer,
        test_parse_range_midpoint,
        test_parse_range_with_dash,
        test_parse_percentage,
        test_parse_embedded_approx,
        test_parse_embedded_tilde,
        test_parse_embedded_equals,
        test_parse_qualitative_returns_none,
        test_parse_empty_returns_none,
        # add_pct_anchors
        test_add_pct_anchors_loads,
        test_add_pct_anchors_names,
        test_add_pct_anchors_bias,
        test_add_pct_anchors_missing_file,
        # calibrate_with_pct
        test_calibrate_with_pct_basic,
        test_calibrate_with_pct_provenance,
        test_calibrate_with_pct_tier_note,
        test_calibrate_with_pct_to_dict,
        test_calibrate_with_pct_unfitted_raises,
        test_calibrate_with_pct_no_shrinkage,
        test_calibrate_with_pct_lower_uncertainty,
        # End-to-end
        test_end_to_end_pct_llmmc,
    ]

    passed = 0
    failed = 0
    errors = []

    for test in tests:
        try:
            test()
            passed += 1
            print(f"  PASS  {test.__name__}")
        except AssertionError as e:
            failed += 1
            errors.append((test.__name__, str(e)))
            print(f"  FAIL  {test.__name__}: {e}")
        except Exception as e:
            failed += 1
            errors.append((test.__name__, str(e)))
            print(f"  ERROR {test.__name__}: {e}")

    print(f"\n{'=' * 40}")
    print(f"  {passed} passed, {failed} failed, {passed + failed} total")
    if errors:
        print(f"\n  Failures:")
        for name, err in errors:
            print(f"    {name}: {err}")
    print()

    sys.exit(0 if failed == 0 else 1)
