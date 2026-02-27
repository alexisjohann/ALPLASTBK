#!/usr/bin/env python3
"""
Tests for Universal Parameter-Lookup API
==========================================

Verifies the orchestrator connecting Layer 2 (YAML registry)
with Layer 1 (formal computation via PCT + LLMMC).

Tests cover:
  - get_parameter: Registry-only lookup
  - lookup_parameter: Full pipeline (Registry → PCT → LLMMC)
  - list_parameters: Listing and filtering
  - Symbol resolution: Greek letter normalization
"""

import sys
from pathlib import Path

# Add scripts/ to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from parameter_api import (
    get_parameter,
    lookup_parameter,
    list_parameters,
    ParameterValue,
    _find_parameter,
    _find_all_parameters,
)


# ---------------------------------------------------------------------------
# Registry loading tests
# ---------------------------------------------------------------------------

def test_find_all_parameters():
    """Registry loads with >0 parameters."""
    params = _find_all_parameters()
    assert len(params) > 0, f"Expected >0 parameters, got {len(params)}"


def test_find_parameter_by_id():
    """Find parameter by ID."""
    p = _find_parameter(parameter_id="PAR-BEH-001")
    assert p is not None
    assert p["id"] == "PAR-BEH-001"


def test_find_parameter_by_symbol():
    """Find parameter by Greek symbol."""
    p = _find_parameter(symbol="λ_R")
    assert p is not None
    assert p["id"] == "PAR-BEH-016"


def test_find_parameter_by_ascii_symbol():
    """Find parameter by ASCII-normalized symbol."""
    p = _find_parameter(symbol="lambda_R")
    assert p is not None
    assert p["id"] == "PAR-BEH-016"


def test_find_parameter_not_found():
    """Non-existent parameter returns None."""
    p = _find_parameter(parameter_id="PAR-NONEXIST-999")
    assert p is None


# ---------------------------------------------------------------------------
# get_parameter tests (Layer 2 only)
# ---------------------------------------------------------------------------

def test_get_parameter_basic():
    """get_parameter returns ParameterValue."""
    result = get_parameter(parameter_id="PAR-BEH-001")
    assert result is not None
    assert isinstance(result, ParameterValue)
    assert result.parameter_id == "PAR-BEH-001"
    assert result.value > 0


def test_get_parameter_loss_aversion():
    """Loss aversion should be ~2.0-2.5."""
    result = get_parameter(parameter_id="PAR-BEH-001")
    assert result is not None
    assert 1.5 < result.value < 3.5, f"Expected λ ∈ [1.5, 3.5], got {result.value}"


def test_get_parameter_by_symbol():
    """get_parameter with symbol lookup."""
    result = get_parameter(symbol="lambda_R")
    assert result is not None
    assert result.parameter_id == "PAR-BEH-016"
    assert result.value > 0


def test_get_parameter_ci():
    """CI bounds bracket the value."""
    result = get_parameter(parameter_id="PAR-BEH-001")
    assert result is not None
    assert result.ci_95[0] <= result.value <= result.ci_95[1]


def test_get_parameter_not_found():
    """Non-existent parameter returns None."""
    result = get_parameter(parameter_id="PAR-FAKE-999")
    assert result is None


def test_get_parameter_to_dict():
    """to_dict produces JSON-serializable output."""
    result = get_parameter(parameter_id="PAR-BEH-001")
    assert result is not None
    d = result.to_dict()
    assert "parameter_id" in d
    assert "value" in d
    assert "ci_95" in d

    import json
    json_str = json.dumps(d)
    assert len(json_str) > 0


# ---------------------------------------------------------------------------
# lookup_parameter tests (Full pipeline)
# ---------------------------------------------------------------------------

def test_lookup_basic():
    """lookup_parameter without PCT is same as get_parameter."""
    result = lookup_parameter(parameter_id="PAR-BEH-001")
    assert result is not None
    assert result.pct_applied is False
    assert result.llmmc_applied is False


def test_lookup_with_pct():
    """lookup_parameter with PCT transform changes value."""
    base = get_parameter(parameter_id="PAR-BEH-016")
    assert base is not None

    transformed = lookup_parameter(
        parameter_id="PAR-BEH-016",
        target_psi={"psi_S": "competence_signaling", "psi_I": "professional_hierarchy"},
        anchor_psi={"psi_S": "welfare_stigma", "psi_I": "bureaucratic_application"},
        anchor_context="welfare",
    )
    assert transformed is not None
    assert transformed.pct_applied is True
    assert transformed.pct_product_M != 1.0
    # Stigma decrease → multiplier < 1 → value should decrease
    assert transformed.value < base.value, \
        f"PCT with stigma decrease should lower value: {transformed.value} < {base.value}"


def test_lookup_with_pct_provenance():
    """PCT provenance is recorded."""
    result = lookup_parameter(
        parameter_id="PAR-BEH-016",
        target_psi={"psi_S": "competence_signaling"},
        anchor_psi={"psi_S": "welfare_stigma"},
        anchor_context="welfare",
    )
    assert result is not None
    assert result.pct_applied is True
    assert result.pct_anchor_context == "welfare"
    assert result.pct_target_context == "target"
    assert 0.5 < result.pct_product_M < 1.5


def test_lookup_with_pct_and_llmmc():
    """Full pipeline: Registry → PCT → LLMMC."""
    result = lookup_parameter(
        parameter_id="PAR-BEH-016",
        target_psi={"psi_S": "competence_signaling", "psi_I": "professional_hierarchy"},
        anchor_psi={"psi_S": "welfare_stigma", "psi_I": "bureaucratic_application"},
        anchor_context="welfare",
        calibrate=True,
    )
    assert result is not None
    assert result.pct_applied is True
    assert result.llmmc_applied is True
    assert result.llmmc_shrinkage < 1.0, "Shrinkage should be < 1.0"
    assert result.value > 0


def test_lookup_pct_without_anchor_psi():
    """target_psi without anchor_psi adds note but doesn't crash."""
    result = lookup_parameter(
        parameter_id="PAR-BEH-016",
        target_psi={"psi_S": "competence_signaling"},
    )
    assert result is not None
    assert "anchor_psi" in result.tier_note


def test_lookup_to_dict_with_pct():
    """to_dict includes PCT section when applied."""
    result = lookup_parameter(
        parameter_id="PAR-BEH-016",
        target_psi={"psi_S": "competence_signaling"},
        anchor_psi={"psi_S": "welfare_stigma"},
        anchor_context="welfare",
    )
    assert result is not None
    d = result.to_dict()
    assert "pct" in d
    assert d["pct"]["applied"] is True


# ---------------------------------------------------------------------------
# list_parameters tests
# ---------------------------------------------------------------------------

def test_list_all():
    """list_parameters returns all parameters."""
    params = list_parameters()
    assert len(params) > 0
    for p in params:
        assert "id" in p
        assert "symbol" in p
        assert "name" in p
        assert "domains" in p


def test_list_filter_domain():
    """list_parameters filters by domain."""
    fin_params = list_parameters(domain="FIN")
    assert len(fin_params) > 0
    for p in fin_params:
        assert "FIN" in [d.upper() for d in p["domains"]]


def test_list_filter_domain_case_insensitive():
    """Domain filter is case-insensitive."""
    fin1 = list_parameters(domain="FIN")
    fin2 = list_parameters(domain="fin")
    assert len(fin1) == len(fin2)


def test_list_filter_nonexistent_domain():
    """Non-existent domain returns empty list."""
    params = list_parameters(domain="NONEXISTENT_DOMAIN")
    assert len(params) == 0


# ---------------------------------------------------------------------------
# Run tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    tests = [
        # Registry loading
        test_find_all_parameters,
        test_find_parameter_by_id,
        test_find_parameter_by_symbol,
        test_find_parameter_by_ascii_symbol,
        test_find_parameter_not_found,
        # get_parameter
        test_get_parameter_basic,
        test_get_parameter_loss_aversion,
        test_get_parameter_by_symbol,
        test_get_parameter_ci,
        test_get_parameter_not_found,
        test_get_parameter_to_dict,
        # lookup_parameter
        test_lookup_basic,
        test_lookup_with_pct,
        test_lookup_with_pct_provenance,
        test_lookup_with_pct_and_llmmc,
        test_lookup_pct_without_anchor_psi,
        test_lookup_to_dict_with_pct,
        # list_parameters
        test_list_all,
        test_list_filter_domain,
        test_list_filter_domain_case_insensitive,
        test_list_filter_nonexistent_domain,
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
