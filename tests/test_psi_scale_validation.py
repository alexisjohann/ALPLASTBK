#!/usr/bin/env python3
"""
Tests for Psi-Scale Validation + Auto-Extract Pipeline
=======================================================

Verifies that:
  - validate_psi_scales correctly detects unmapped/unused labels
  - auto_extract_pipeline chains extraction + validation
  - Coverage statistics are accurate
  - Strict mode returns correct exit codes

Tests cover:
  - get_scale_labels / get_context_labels: Label extraction
  - get_context_params / get_registry_params: Parameter ID extraction
  - validate(): Full validation pipeline
  - auto_extract_pipeline.run_pipeline(): Chained extraction + validation
  - Coverage arithmetic: Correct percentages
  - Strict mode: Failure detection
"""

import sys
from pathlib import Path

# Add scripts/ to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from validate_psi_scales import (
    validate,
    get_scale_labels,
    get_context_labels,
    get_context_params,
    get_registry_params,
    load_yaml,
    PSI_SCALES_PATH,
    MEASUREMENT_CONTEXTS_PATH,
    PARAMETER_REGISTRY_PATH,
)

from auto_extract_pipeline import (
    run_extraction,
    run_validation,
    run_pipeline,
)


# ---------------------------------------------------------------------------
# get_scale_labels tests
# ---------------------------------------------------------------------------

def test_get_scale_labels_returns_dict():
    """get_scale_labels returns a dict of dimension -> set(labels)."""
    data = load_yaml(PSI_SCALES_PATH)
    if not data:
        print("  SKIP (pct-psi-scales.yaml not found)")
        return
    labels = get_scale_labels(data)
    assert isinstance(labels, dict), f"Expected dict, got {type(labels)}"
    assert len(labels) > 0, "Expected at least one dimension"


def test_get_scale_labels_has_psi_S():
    """psi_S dimension should exist in scales."""
    data = load_yaml(PSI_SCALES_PATH)
    if not data:
        print("  SKIP (pct-psi-scales.yaml not found)")
        return
    labels = get_scale_labels(data)
    assert "psi_S" in labels, f"Expected psi_S in labels, got {list(labels.keys())}"
    assert len(labels["psi_S"]) > 5, f"Expected >5 psi_S labels, got {len(labels['psi_S'])}"


def test_get_scale_labels_known_label():
    """welfare_stigma should be in psi_S."""
    data = load_yaml(PSI_SCALES_PATH)
    if not data:
        print("  SKIP (pct-psi-scales.yaml not found)")
        return
    labels = get_scale_labels(data)
    assert "welfare_stigma" in labels.get("psi_S", set()), \
        "Expected welfare_stigma in psi_S labels"


def test_get_scale_labels_eight_dimensions():
    """Should have all 8 psi dimensions."""
    data = load_yaml(PSI_SCALES_PATH)
    if not data:
        print("  SKIP (pct-psi-scales.yaml not found)")
        return
    labels = get_scale_labels(data)
    expected = {"psi_S", "psi_I", "psi_C", "psi_K", "psi_E", "psi_T", "psi_M", "psi_F"}
    actual = set(labels.keys())
    assert expected == actual, f"Expected {expected}, got {actual}"


# ---------------------------------------------------------------------------
# get_context_labels tests
# ---------------------------------------------------------------------------

def test_get_context_labels_returns_dict():
    """get_context_labels returns dict of used labels."""
    data = load_yaml(MEASUREMENT_CONTEXTS_PATH)
    if not data:
        print("  SKIP (pct-measurement-contexts.yaml not found)")
        return
    labels = get_context_labels(data)
    assert isinstance(labels, dict)


def test_get_context_labels_nonempty():
    """Should find labels in measurement contexts."""
    data = load_yaml(MEASUREMENT_CONTEXTS_PATH)
    if not data:
        print("  SKIP (pct-measurement-contexts.yaml not found)")
        return
    labels = get_context_labels(data)
    total = sum(len(v) for v in labels.values())
    assert total > 0, f"Expected >0 context labels, got {total}"


# ---------------------------------------------------------------------------
# get_context_params tests
# ---------------------------------------------------------------------------

def test_get_context_params_nonempty():
    """Should find parameter IDs in measurement contexts."""
    data = load_yaml(MEASUREMENT_CONTEXTS_PATH)
    if not data:
        print("  SKIP (pct-measurement-contexts.yaml not found)")
        return
    params = get_context_params(data)
    assert len(params) > 0, f"Expected >0 params, got {len(params)}"


def test_get_context_params_known_id():
    """PAR-BEH-016 should have measurement contexts."""
    data = load_yaml(MEASUREMENT_CONTEXTS_PATH)
    if not data:
        print("  SKIP (pct-measurement-contexts.yaml not found)")
        return
    params = get_context_params(data)
    assert "PAR-BEH-016" in params, \
        f"Expected PAR-BEH-016 in context params, got {sorted(list(params))[:10]}..."


# ---------------------------------------------------------------------------
# get_registry_params tests
# ---------------------------------------------------------------------------

def test_get_registry_params_nonempty():
    """Should find parameter IDs in registry."""
    data = load_yaml(PARAMETER_REGISTRY_PATH)
    if not data:
        print("  SKIP (parameter-registry.yaml not found)")
        return
    params = get_registry_params(data)
    assert len(params) > 50, f"Expected >50 registry params, got {len(params)}"


def test_get_registry_params_known_id():
    """PAR-BEH-016 should be in registry."""
    data = load_yaml(PARAMETER_REGISTRY_PATH)
    if not data:
        print("  SKIP (parameter-registry.yaml not found)")
        return
    params = get_registry_params(data)
    assert "PAR-BEH-016" in params


# ---------------------------------------------------------------------------
# validate() tests
# ---------------------------------------------------------------------------

def test_validate_returns_tuple():
    """validate() returns (ok: bool, report: dict)."""
    ok, report = validate()
    assert isinstance(ok, bool)
    assert isinstance(report, dict)


def test_validate_report_has_fields():
    """Report contains expected fields."""
    ok, report = validate()
    if "error" in report:
        print(f"  SKIP (validation error: {report['error']})")
        return
    expected_keys = [
        "unmapped_labels", "unused_labels", "scale_stats",
        "params_with_contexts", "params_total", "coverage_pct",
        "n_triplets",
    ]
    for key in expected_keys:
        assert key in report, f"Expected '{key}' in report, got {list(report.keys())}"


def test_validate_coverage_positive():
    """Coverage percentage should be positive."""
    ok, report = validate()
    if "error" in report:
        print(f"  SKIP (validation error: {report['error']})")
        return
    assert report["coverage_pct"] > 0, \
        f"Expected positive coverage, got {report['coverage_pct']}%"


def test_validate_coverage_not_over_100():
    """Coverage should not exceed 100%."""
    ok, report = validate()
    if "error" in report:
        print(f"  SKIP (validation error: {report['error']})")
        return
    assert report["coverage_pct"] <= 100, \
        f"Coverage exceeds 100%: {report['coverage_pct']}%"


def test_validate_triplets_positive():
    """Should have >0 triplets."""
    ok, report = validate()
    if "error" in report:
        print(f"  SKIP (validation error: {report['error']})")
        return
    assert report["n_triplets"] > 0, f"Expected >0 triplets, got {report['n_triplets']}"


def test_validate_scale_stats_all_dims():
    """Scale stats should have all 8 dimensions."""
    ok, report = validate()
    if "error" in report:
        print(f"  SKIP (validation error: {report['error']})")
        return
    stats = report.get("scale_stats", {})
    expected = {"psi_S", "psi_I", "psi_C", "psi_K", "psi_E", "psi_T", "psi_M", "psi_F"}
    actual = set(stats.keys())
    assert expected == actual, f"Expected {expected}, got {actual}"


def test_validate_params_with_contexts_leq_total():
    """Params with contexts <= total params."""
    ok, report = validate()
    if "error" in report:
        print(f"  SKIP (validation error: {report['error']})")
        return
    assert report["params_with_contexts"] <= report["params_total"], \
        f"params_with ({report['params_with_contexts']}) > total ({report['params_total']})"


def test_validate_unmapped_is_dict():
    """Unmapped labels should be a dict."""
    ok, report = validate()
    if "error" in report:
        print(f"  SKIP (validation error: {report['error']})")
        return
    unmapped = report.get("unmapped_labels", {})
    assert isinstance(unmapped, dict)
    # If all labels are mapped, ok should be True
    total_unmapped = sum(len(v) for v in unmapped.values())
    if total_unmapped == 0:
        assert ok, "Expected ok=True when no unmapped labels"
    else:
        assert not ok, f"Expected ok=False when {total_unmapped} unmapped labels"


# ---------------------------------------------------------------------------
# auto_extract_pipeline tests
# ---------------------------------------------------------------------------

def test_run_validation_returns_tuple():
    """run_validation returns (ok, report)."""
    ok, report = run_validation()
    assert isinstance(ok, bool)
    assert isinstance(report, dict)


def test_run_extraction_dry_run():
    """run_extraction in dry-run mode doesn't write files."""
    ok, stats = run_extraction(dry_run=True)
    assert isinstance(ok, bool)
    assert isinstance(stats, dict)
    if "error" in stats:
        print(f"  SKIP (extraction error: {stats['error']})")
        return
    assert stats.get("written") is False, \
        "Dry-run should not write files"


def test_run_extraction_has_stats():
    """Extraction stats contain expected fields."""
    ok, stats = run_extraction(dry_run=True)
    if "error" in stats:
        print(f"  SKIP (extraction error: {stats['error']})")
        return
    expected = [
        "existing_triplets", "new_extracted", "added_deduplicated",
        "merged_total", "coverage_before", "coverage_after",
    ]
    for key in expected:
        assert key in stats, f"Expected '{key}' in stats, got {list(stats.keys())}"


def test_run_extraction_coverage_nondecreasing():
    """Coverage after extraction >= coverage before."""
    ok, stats = run_extraction(dry_run=True)
    if "error" in stats:
        print(f"  SKIP (extraction error: {stats['error']})")
        return
    assert stats["coverage_after"] >= stats["coverage_before"], \
        f"Coverage decreased: {stats['coverage_before']} -> {stats['coverage_after']}"


def test_run_pipeline_validate_only():
    """Pipeline in validate-only mode skips extraction."""
    ok, combined = run_pipeline(validate_only=True)
    assert isinstance(ok, bool)
    assert isinstance(combined, dict)
    assert combined["extraction"] == {"skipped": True}, \
        f"Expected extraction skipped, got {combined['extraction']}"
    assert combined["validation"] is not None


def test_run_pipeline_dry_run():
    """Pipeline in dry-run mode doesn't write files."""
    ok, combined = run_pipeline(dry_run=True)
    assert isinstance(ok, bool)
    assert isinstance(combined, dict)
    ext = combined.get("extraction", {})
    if "error" not in ext:
        assert ext.get("written") is False, "Dry-run should not write"


def test_run_pipeline_has_overall_ok():
    """Pipeline result has overall_ok."""
    ok, combined = run_pipeline(validate_only=True)
    assert "overall_ok" in combined


def test_run_pipeline_validation_not_none():
    """Pipeline always includes validation results."""
    ok, combined = run_pipeline(dry_run=True)
    assert combined["validation"] is not None
    val = combined["validation"]
    if "error" not in val:
        assert "n_triplets" in val or "unmapped_labels" in val


def test_run_pipeline_consistency():
    """Pipeline validate-only result matches direct validation."""
    ok_pipeline, combined = run_pipeline(validate_only=True)
    ok_direct, report_direct = run_validation()

    # Both should agree on ok status
    val = combined.get("validation", {})
    if "error" not in val and "error" not in report_direct:
        unmapped_pipeline = val.get("unmapped_labels", {})
        unmapped_direct = report_direct.get("unmapped_labels", {})
        assert unmapped_pipeline == unmapped_direct, \
            f"Pipeline and direct validation disagree on unmapped labels"


# ---------------------------------------------------------------------------
# Integration tests
# ---------------------------------------------------------------------------

def test_all_context_labels_in_scales():
    """All labels used in measurement contexts should be in psi-scales.

    This is the core invariant that the pre-commit hook enforces.
    """
    ok, report = validate()
    if "error" in report:
        print(f"  SKIP (validation error: {report['error']})")
        return
    unmapped = report.get("unmapped_labels", {})
    total_unmapped = sum(len(v) for v in unmapped.values())
    assert total_unmapped == 0, \
        f"Found {total_unmapped} unmapped labels: {unmapped}"


def test_coverage_above_70_percent():
    """Parameter coverage should be >=70% (pre-commit gate threshold)."""
    ok, report = validate()
    if "error" in report:
        print(f"  SKIP (validation error: {report['error']})")
        return
    assert report["coverage_pct"] >= 70.0, \
        f"Coverage {report['coverage_pct']}% is below 70% pre-commit threshold"


def test_coverage_threshold_cli():
    """--coverage --threshold should exit 1 when below threshold."""
    import subprocess
    script = str(Path(__file__).resolve().parent.parent / "scripts" / "validate_psi_scales.py")
    # Threshold of 101% should always fail
    result = subprocess.run(
        [sys.executable, script, "--coverage", "--threshold", "101"],
        capture_output=True, text=True,
    )
    assert result.returncode == 1, \
        f"Expected exit 1 for impossible threshold, got {result.returncode}"
    assert "FAIL" in result.stdout, \
        f"Expected FAIL in output, got: {result.stdout}"


def test_extraction_pipeline_matches_validation():
    """Extraction stats should be consistent with validation report."""
    ok_ext, ext_stats = run_extraction(dry_run=True)
    ok_val, val_report = validate()

    if "error" in ext_stats or "error" in val_report:
        print("  SKIP (data file error)")
        return

    # Both should report same total triplets (since dry-run doesn't add)
    # Extraction merged_total >= validation n_triplets
    # (merged_total includes new_extracted which may overlap)
    assert ext_stats["merged_total"] >= val_report["n_triplets"], \
        f"Extraction merged ({ext_stats['merged_total']}) < validation triplets ({val_report['n_triplets']})"


# ---------------------------------------------------------------------------
# Run tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    tests = [
        # get_scale_labels
        test_get_scale_labels_returns_dict,
        test_get_scale_labels_has_psi_S,
        test_get_scale_labels_known_label,
        test_get_scale_labels_eight_dimensions,
        # get_context_labels
        test_get_context_labels_returns_dict,
        test_get_context_labels_nonempty,
        # get_context_params
        test_get_context_params_nonempty,
        test_get_context_params_known_id,
        # get_registry_params
        test_get_registry_params_nonempty,
        test_get_registry_params_known_id,
        # validate()
        test_validate_returns_tuple,
        test_validate_report_has_fields,
        test_validate_coverage_positive,
        test_validate_coverage_not_over_100,
        test_validate_triplets_positive,
        test_validate_scale_stats_all_dims,
        test_validate_params_with_contexts_leq_total,
        test_validate_unmapped_is_dict,
        # auto_extract_pipeline
        test_run_validation_returns_tuple,
        test_run_extraction_dry_run,
        test_run_extraction_has_stats,
        test_run_extraction_coverage_nondecreasing,
        test_run_pipeline_validate_only,
        test_run_pipeline_dry_run,
        test_run_pipeline_has_overall_ok,
        test_run_pipeline_validation_not_none,
        test_run_pipeline_consistency,
        # Integration
        test_all_context_labels_in_scales,
        test_coverage_above_70_percent,
        test_coverage_threshold_cli,
        test_extraction_pipeline_matches_validation,
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
