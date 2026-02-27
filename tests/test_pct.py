#!/usr/bin/env python3
"""
Tests for PCT (Parameter Context Transformation) Module
========================================================

Verifies the core equation: theta_B = theta_A * prod_i M(delta_psi_i)

Reference: docs/workflows/level5-paper-integration-workflow.md Lines 456-508
"""

import sys
from pathlib import Path

# Add scripts/ to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from pct import (
    AnchorContext,
    PsiDelta,
    TenCDelta,
    PCTResult,
    transform,
    transform_with_deltas,
    transform_with_multipliers,
    transform_from_contexts,
    demo_benabou,
    get_default_multiplier,
    resolve_psi_value,
    compute_psi_delta_from_labels,
    get_psi_scales,
    get_10c_multiplier,
    get_10c_tables,
    compute_10c_deltas,
)


# ---------------------------------------------------------------------------
# Core equation tests
# ---------------------------------------------------------------------------

def test_benabou_worked_example():
    """
    Worked Example from documentation (L456-508):
    lambda_R: welfare(2.5) -> workplace(2.22)

    M(psi_S=-0.3) = 0.85
    M(psi_I=-0.1) = 0.95
    M(psi_C=+0.2) = 1.10

    theta_B = 2.5 * 0.85 * 0.95 * 1.10 = 2.220625
    """
    result = demo_benabou()

    expected = 2.5 * 0.85 * 0.95 * 1.10  # = 2.220625
    assert abs(result.theta_B - expected) < 0.001, \
        f"Expected theta_B={expected:.4f}, got {result.theta_B:.4f}"
    assert abs(result.theta_A - 2.5) < 0.001
    assert result.parameter_symbol == "lambda_R"
    assert result.parameter_id == "PAR-BEH-016"
    assert result.anchor_context == "welfare_takeup"
    assert result.target_context == "workplace_help"
    assert len(result.psi_deltas) == 3


def test_identity_transformation():
    """Same context (no deltas) -> theta_B = theta_A."""
    result = transform(2.5, [])
    assert result.theta_B == result.theta_A
    assert result.product_M == 1.0


def test_single_multiplier():
    """Single Psi-dimension -> theta_B = theta_A * M."""
    pd = PsiDelta(dimension="psi_S", delta=-0.3, multiplier=0.85)
    result = transform(2.5, [pd])
    assert abs(result.theta_B - 2.5 * 0.85) < 0.001
    assert abs(result.product_M - 0.85) < 0.001


def test_product_of_multipliers():
    """Multiple multipliers -> product is multiplicative."""
    pds = [
        PsiDelta(dimension="psi_S", delta=-0.3, multiplier=0.85),
        PsiDelta(dimension="psi_I", delta=-0.1, multiplier=0.95),
    ]
    result = transform(2.0, pds)
    expected = 2.0 * 0.85 * 0.95
    assert abs(result.theta_B - expected) < 0.001
    assert abs(result.product_M - 0.85 * 0.95) < 0.001


def test_multiplier_above_one():
    """Multiplier > 1 increases theta."""
    pd = PsiDelta(dimension="psi_C", delta=0.2, multiplier=1.10)
    result = transform(2.0, [pd])
    assert result.theta_B > result.theta_A


def test_multiplier_below_one():
    """Multiplier < 1 decreases theta."""
    pd = PsiDelta(dimension="psi_S", delta=-0.3, multiplier=0.85)
    result = transform(2.0, [pd])
    assert result.theta_B < result.theta_A


# ---------------------------------------------------------------------------
# Transform with explicit multipliers
# ---------------------------------------------------------------------------

def test_transform_with_multipliers():
    """Explicit multipliers mode."""
    result = transform_with_multipliers(2.5, [0.85, 0.95, 1.10])
    expected = 2.5 * 0.85 * 0.95 * 1.10
    assert abs(result.theta_B - expected) < 0.001


def test_transform_with_multipliers_labels():
    """Explicit multipliers with custom labels."""
    result = transform_with_multipliers(
        2.5,
        [0.85, 0.95],
        labels=["psi_S", "psi_I"],
    )
    assert result.psi_deltas[0].dimension == "psi_S"
    assert result.psi_deltas[1].dimension == "psi_I"


# ---------------------------------------------------------------------------
# Transform with named deltas (table lookup)
# ---------------------------------------------------------------------------

def test_transform_with_deltas_basic():
    """Named deltas with table lookup."""
    result = transform_with_deltas(2.5, {"psi_S": -0.3})
    # Should produce a multiplier < 1 (stigma decrease)
    assert result.theta_B < 2.5
    assert len(result.psi_deltas) == 1
    assert result.psi_deltas[0].dimension == "psi_S"


def test_transform_with_deltas_metadata():
    """Metadata propagation."""
    result = transform_with_deltas(
        2.5,
        {"psi_S": -0.3},
        anchor_context="welfare",
        target_context="workplace",
        parameter_id="PAR-BEH-016",
        parameter_symbol="lambda_R",
    )
    assert result.anchor_context == "welfare"
    assert result.target_context == "workplace"
    assert result.parameter_id == "PAR-BEH-016"
    assert result.parameter_symbol == "lambda_R"


def test_transform_with_zero_delta():
    """Zero delta -> multiplier = 1.0."""
    result = transform_with_deltas(2.5, {"psi_S": 0.0})
    assert abs(result.theta_B - 2.5) < 0.001


def test_transform_with_unknown_dimension():
    """Unknown dimension -> multiplier = 1.0 (identity)."""
    result = transform_with_deltas(2.5, {"psi_UNKNOWN": 0.5})
    assert abs(result.theta_B - 2.5) < 0.001


# ---------------------------------------------------------------------------
# Multiplier table tests
# ---------------------------------------------------------------------------

def test_multiplier_stigma_decrease():
    """psi_S negative delta -> M < 1."""
    m = get_default_multiplier("psi_S", -0.3)
    assert 0.5 < m < 1.0, f"Expected M < 1 for stigma decrease, got {m}"


def test_multiplier_stigma_increase():
    """psi_S positive delta -> M > 1."""
    m = get_default_multiplier("psi_S", 0.3)
    assert m > 1.0, f"Expected M > 1 for stigma increase, got {m}"


def test_multiplier_zero_delta():
    """Zero delta -> M = 1.0."""
    m = get_default_multiplier("psi_S", 0.0)
    assert m == 1.0


def test_multiplier_bounds():
    """All multipliers should be within [0.5, 2.0]."""
    dims = ["psi_S", "psi_I", "psi_C", "psi_K", "psi_E", "psi_T", "psi_M", "psi_F"]
    for dim in dims:
        for delta in [-0.5, -0.3, -0.1, 0.1, 0.3, 0.5]:
            m = get_default_multiplier(dim, delta)
            assert 0.5 <= m <= 2.0, \
                f"M({dim}, {delta}) = {m} out of bounds [0.5, 2.0]"


def test_multiplier_monotonicity_psi_S():
    """Larger negative delta -> smaller multiplier for stigma."""
    m_small = get_default_multiplier("psi_S", -0.1)
    m_large = get_default_multiplier("psi_S", -0.5)
    assert m_large <= m_small, \
        f"Expected monotonic: M(-0.5)={m_large} <= M(-0.1)={m_small}"


# ---------------------------------------------------------------------------
# Serialization tests
# ---------------------------------------------------------------------------

def test_to_dict():
    """PCTResult serializes correctly."""
    result = demo_benabou()
    d = result.to_dict()

    assert "theta_A" in d
    assert "theta_B" in d
    assert "product_M" in d
    assert "psi_deltas" in d
    assert len(d["psi_deltas"]) == 3
    assert d["parameter_symbol"] == "lambda_R"

    # Check all values are JSON-serializable (no numpy, no dataclass)
    import json
    json_str = json.dumps(d)
    assert len(json_str) > 0


def test_to_dict_roundtrip():
    """Serialized values match computed values."""
    result = demo_benabou()
    d = result.to_dict()

    assert abs(d["theta_A"] - 2.5) < 0.001
    expected_b = 2.5 * 0.85 * 0.95 * 1.10
    assert abs(d["theta_B"] - expected_b) < 0.01


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_theta_zero():
    """theta_A = 0 -> theta_B = 0 regardless of multipliers."""
    pd = PsiDelta(dimension="psi_S", delta=-0.3, multiplier=0.85)
    result = transform(0.0, [pd])
    assert result.theta_B == 0.0


def test_many_multipliers():
    """Many multipliers compound correctly."""
    n = 10
    pds = [PsiDelta(dimension=f"dim_{i}", delta=0.1, multiplier=1.05)
           for i in range(n)]
    result = transform(1.0, pds)
    expected = 1.05 ** n
    assert abs(result.theta_B - expected) < 0.001


# ---------------------------------------------------------------------------
# Psi-scales tests (categorical label → numeric value → delta)
# ---------------------------------------------------------------------------

def test_psi_scales_loaded():
    """Psi-scales YAML loads and has expected dimensions."""
    scales = get_psi_scales()
    assert len(scales) >= 8, f"Expected >= 8 dimensions, got {len(scales)}"
    for dim in ["psi_S", "psi_I", "psi_C", "psi_K", "psi_E", "psi_T", "psi_M", "psi_F"]:
        assert dim in scales, f"Missing dimension {dim}"


def test_resolve_psi_value_known():
    """Known label resolves to a value in [0, 1]."""
    val = resolve_psi_value("psi_S", "welfare_stigma")
    assert val is not None, "welfare_stigma should be in psi_S"
    assert 0.0 <= val <= 1.0, f"Expected [0,1], got {val}"


def test_resolve_psi_value_unknown():
    """Unknown label returns None."""
    val = resolve_psi_value("psi_S", "nonexistent_label_xyz")
    assert val is None


def test_resolve_psi_value_unknown_dimension():
    """Unknown dimension returns None."""
    val = resolve_psi_value("psi_UNKNOWN", "welfare_stigma")
    assert val is None


def test_compute_delta_from_labels():
    """Delta from welfare_stigma → competence_signaling is negative."""
    delta = compute_psi_delta_from_labels("psi_S", "welfare_stigma", "competence_signaling")
    assert delta is not None
    assert delta < 0, f"Expected negative delta (stigma decrease), got {delta}"


def test_compute_delta_same_label():
    """Same label → delta = 0."""
    delta = compute_psi_delta_from_labels("psi_S", "welfare_stigma", "welfare_stigma")
    assert delta is not None
    assert delta == 0.0


def test_compute_delta_unmapped_label():
    """Unmapped label → None."""
    delta = compute_psi_delta_from_labels("psi_S", "welfare_stigma", "nonexistent_xyz")
    assert delta is None


def test_transform_from_contexts_basic():
    """Transform using categorical Psi labels."""
    result = transform_from_contexts(
        2.5,
        anchor_psi={"psi_S": "welfare_stigma", "psi_I": "bureaucratic_application"},
        target_psi={"psi_S": "competence_signaling", "psi_I": "professional_hierarchy"},
        anchor_context="welfare",
        target_context="workplace",
    )
    # Stigma decreases → theta_B should be < theta_A
    assert result.theta_B < 2.5, f"Expected theta_B < 2.5, got {result.theta_B}"
    assert len(result.psi_deltas) >= 2
    assert result.anchor_context == "welfare"
    assert result.target_context == "workplace"


def test_transform_from_contexts_labels_preserved():
    """Anchor and target labels are preserved in PsiDelta."""
    result = transform_from_contexts(
        2.5,
        anchor_psi={"psi_S": "welfare_stigma"},
        target_psi={"psi_S": "competence_signaling"},
    )
    assert len(result.psi_deltas) == 1
    pd = result.psi_deltas[0]
    assert pd.anchor_label == "welfare_stigma"
    assert pd.target_label == "competence_signaling"
    assert pd.dimension == "psi_S"


def test_transform_from_contexts_unmapped_labels():
    """Unmapped labels produce identity multiplier with (unmapped) marker."""
    result = transform_from_contexts(
        2.5,
        anchor_psi={"psi_S": "unknown_label_a"},
        target_psi={"psi_S": "unknown_label_b"},
    )
    assert len(result.psi_deltas) == 1
    pd = result.psi_deltas[0]
    assert pd.multiplier == 1.0
    assert "(unmapped)" in pd.anchor_label


def test_psi_scale_welfare_stigma_high():
    """welfare_stigma should be high on the social scale (> 0.7)."""
    val = resolve_psi_value("psi_S", "welfare_stigma")
    assert val is not None and val > 0.7, \
        f"welfare_stigma should be high (>0.7), got {val}"


def test_psi_scale_competence_signaling_moderate():
    """competence_signaling should be moderate on the social scale."""
    val = resolve_psi_value("psi_S", "competence_signaling")
    assert val is not None and 0.3 < val < 0.7, \
        f"competence_signaling should be moderate, got {val}"


# ---------------------------------------------------------------------------
# 10C multiplier tests
# ---------------------------------------------------------------------------

def test_10c_tables_loaded():
    """10C tables load with 9 expected dimensions."""
    tables = get_10c_tables()
    assert len(tables) >= 9, f"Expected >= 9 10C dimensions, got {len(tables)}"
    for dim in ["WHO", "WHAT", "HOW", "WHEN", "WHERE", "AWARE", "READY", "STAGE", "HIERARCHY"]:
        assert dim in tables, f"Missing 10C dimension {dim}"


def test_10c_multiplier_zero_delta():
    """Zero delta -> N = 1.0."""
    n = get_10c_multiplier("WHO", 0.0)
    assert n == 1.0


def test_10c_multiplier_positive_delta():
    """Positive delta -> N > 1.0 (for positive slope)."""
    n = get_10c_multiplier("WHO", 0.5)
    assert n > 1.0, f"Expected N > 1.0 for positive delta, got {n}"


def test_10c_multiplier_negative_delta():
    """Negative delta -> N < 1.0 (for positive slope)."""
    n = get_10c_multiplier("WHO", -0.5)
    assert n < 1.0, f"Expected N < 1.0 for negative delta, got {n}"


def test_10c_multiplier_unknown_dimension():
    """Unknown 10C dimension -> N = 1.0."""
    n = get_10c_multiplier("NONEXISTENT", 0.5)
    assert n == 1.0


def test_10c_multiplier_bounds():
    """All 10C multipliers should be within their declared ranges."""
    tables = get_10c_tables()
    for dim, data in tables.items():
        rng = data.get("range", [0.5, 2.0])
        for delta in [-1.0, -0.5, -0.2, 0.2, 0.5, 1.0]:
            n = get_10c_multiplier(dim, delta)
            assert rng[0] <= n <= rng[1], \
                f"N({dim}, {delta}) = {n} out of range {rng}"


def test_10c_multiplier_formula():
    """N = 1.0 + slope * delta (before clamping)."""
    tables = get_10c_tables()
    # Test with a small delta that won't trigger clamping
    dim = "WHO"
    slope = tables[dim]["slope"]
    delta = 0.1
    expected = 1.0 + slope * delta
    actual = get_10c_multiplier(dim, delta)
    assert abs(actual - expected) < 0.001, \
        f"Expected N={expected:.4f}, got {actual:.4f}"


def test_compute_10c_deltas_basic():
    """compute_10c_deltas returns correct list."""
    raw = {"WHO": -0.5, "WHAT": 0.3}
    result = compute_10c_deltas(raw)
    assert len(result) == 2
    dims = {tc.dimension for tc in result}
    assert "WHO" in dims
    assert "WHAT" in dims
    for tc in result:
        if tc.dimension == "WHO":
            assert tc.delta == -0.5
            assert tc.multiplier < 1.0


def test_transform_with_10c_only():
    """Transform with 10C multipliers only (no psi deltas)."""
    tc = [TenCDelta(dimension="WHO", delta=-0.5, multiplier=0.925)]
    result = transform(2.0, [], tc)
    expected = 2.0 * 0.925
    assert abs(result.theta_B - expected) < 0.001
    assert abs(result.product_N - 0.925) < 0.001
    assert result.product_M == 1.0


def test_transform_with_psi_and_10c():
    """Full equation: theta_B = theta_A * product_M * product_N."""
    pd = PsiDelta(dimension="psi_S", delta=-0.3, multiplier=0.85)
    tc = TenCDelta(dimension="WHO", delta=-0.5, multiplier=0.925)
    result = transform(2.0, [pd], [tc])
    expected = 2.0 * 0.85 * 0.925
    assert abs(result.theta_B - expected) < 0.001
    assert abs(result.product_M - 0.85) < 0.001
    assert abs(result.product_N - 0.925) < 0.001


def test_transform_with_deltas_and_10c():
    """transform_with_deltas passes 10C through correctly."""
    result = transform_with_deltas(
        2.5,
        {"psi_S": -0.3},
        ten_c_deltas={"WHO": -0.5},
    )
    assert result.theta_B < 2.5
    assert len(result.ten_c_deltas) == 1
    assert result.ten_c_deltas[0].dimension == "WHO"
    assert result.product_N < 1.0


def test_transform_from_contexts_with_10c():
    """transform_from_contexts passes 10C through correctly."""
    result = transform_from_contexts(
        2.5,
        anchor_psi={"psi_S": "welfare_stigma"},
        target_psi={"psi_S": "competence_signaling"},
        ten_c_deltas={"WHO": -0.5, "READY": 0.3},
    )
    assert len(result.ten_c_deltas) == 2
    assert result.product_N != 1.0


def test_to_dict_with_10c():
    """Serialization includes 10C fields when present."""
    pd = PsiDelta(dimension="psi_S", delta=-0.3, multiplier=0.85)
    tc = TenCDelta(dimension="WHO", delta=-0.5, multiplier=0.925)
    result = transform(2.0, [pd], [tc])
    d = result.to_dict()
    assert "product_N" in d
    assert "ten_c_deltas" in d
    assert len(d["ten_c_deltas"]) == 1
    assert d["ten_c_deltas"][0]["dimension"] == "WHO"

    import json
    json_str = json.dumps(d)
    assert len(json_str) > 0


def test_to_dict_without_10c():
    """Serialization omits 10C fields when no 10C deltas."""
    result = demo_benabou()
    d = result.to_dict()
    assert "product_N" not in d
    assert "ten_c_deltas" not in d


# ---------------------------------------------------------------------------
# Run tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    tests = [
        # Core equation
        test_benabou_worked_example,
        test_identity_transformation,
        test_single_multiplier,
        test_product_of_multipliers,
        test_multiplier_above_one,
        test_multiplier_below_one,
        # Explicit multipliers
        test_transform_with_multipliers,
        test_transform_with_multipliers_labels,
        # Named deltas
        test_transform_with_deltas_basic,
        test_transform_with_deltas_metadata,
        test_transform_with_zero_delta,
        test_transform_with_unknown_dimension,
        # Multiplier tables
        test_multiplier_stigma_decrease,
        test_multiplier_stigma_increase,
        test_multiplier_zero_delta,
        test_multiplier_bounds,
        test_multiplier_monotonicity_psi_S,
        # Serialization
        test_to_dict,
        test_to_dict_roundtrip,
        # Edge cases
        test_theta_zero,
        test_many_multipliers,
        # Psi-scales (categorical labels)
        test_psi_scales_loaded,
        test_resolve_psi_value_known,
        test_resolve_psi_value_unknown,
        test_resolve_psi_value_unknown_dimension,
        test_compute_delta_from_labels,
        test_compute_delta_same_label,
        test_compute_delta_unmapped_label,
        test_transform_from_contexts_basic,
        test_transform_from_contexts_labels_preserved,
        test_transform_from_contexts_unmapped_labels,
        test_psi_scale_welfare_stigma_high,
        test_psi_scale_competence_signaling_moderate,
        # 10C multipliers
        test_10c_tables_loaded,
        test_10c_multiplier_zero_delta,
        test_10c_multiplier_positive_delta,
        test_10c_multiplier_negative_delta,
        test_10c_multiplier_unknown_dimension,
        test_10c_multiplier_bounds,
        test_10c_multiplier_formula,
        test_compute_10c_deltas_basic,
        test_transform_with_10c_only,
        test_transform_with_psi_and_10c,
        test_transform_with_deltas_and_10c,
        test_transform_from_contexts_with_10c,
        test_to_dict_with_10c,
        test_to_dict_without_10c,
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
