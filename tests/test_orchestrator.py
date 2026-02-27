#!/usr/bin/env python3
"""
Tests for EBF Three-Layer Orchestrator
========================================

Verifies the orchestrator connecting all three TLA layers:
  Layer 1 (Python) — Formal Computation
  Layer 2 (YAML)   — Parameter Store
  Layer 3 (LLM)    — Translation (NOT tested here — formal only)

Tests cover:
  - Query classification
  - Simple queries (Layer 2 only)
  - Contextual queries (Layer 2 + PCT)
  - Calibrated queries (Layer 2 + PCT + LLMMC)
  - Batch queries
  - Health check
  - Explain output
  - JSON serialization
  - Error handling
"""

import sys
import json
from pathlib import Path

# Add scripts/ to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from orchestrator import (
    Orchestrator,
    OrchestratorResult,
    HealthCheckResult,
    QueryType,
    LayerUsed,
)


# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

def _orch():
    """Create a fresh Orchestrator instance."""
    return Orchestrator(verbose=False)


# ---------------------------------------------------------------------------
# Query classification tests
# ---------------------------------------------------------------------------

def test_classify_simple():
    """No context → SIMPLE."""
    orch = _orch()
    qt = orch.classify(parameter_id="PAR-BEH-001")
    assert qt == QueryType.SIMPLE


def test_classify_contextual():
    """Context with psi → CONTEXTUAL."""
    orch = _orch()
    qt = orch.classify(
        parameter_id="PAR-BEH-016",
        context={"target_psi": {"psi_S": "x"}, "anchor_psi": {"psi_S": "y"}},
    )
    assert qt == QueryType.CONTEXTUAL


def test_classify_calibrated():
    """Context + calibrate → CALIBRATED."""
    orch = _orch()
    qt = orch.classify(
        parameter_id="PAR-BEH-016",
        context={"target_psi": {"psi_S": "x"}, "anchor_psi": {"psi_S": "y"}},
        calibrate=True,
    )
    assert qt == QueryType.CALIBRATED


def test_classify_empty_context():
    """Empty context dict → SIMPLE."""
    orch = _orch()
    qt = orch.classify(parameter_id="PAR-BEH-001", context={})
    assert qt == QueryType.SIMPLE


# ---------------------------------------------------------------------------
# Simple query tests (Layer 2 only)
# ---------------------------------------------------------------------------

def test_simple_query_by_id():
    """Simple query returns OrchestratorResult."""
    orch = _orch()
    result = orch.query(parameter_id="PAR-BEH-001")
    assert result is not None
    assert isinstance(result, OrchestratorResult)
    assert result.parameter_id == "PAR-BEH-001"
    assert result.value > 0


def test_simple_query_by_symbol():
    """Query by symbol resolves correctly."""
    orch = _orch()
    result = orch.query(symbol="lambda_R")
    assert result is not None
    assert result.parameter_id == "PAR-BEH-016"
    assert result.symbol == "λ_R"


def test_simple_query_layers_used():
    """Simple query uses Layer 2 only."""
    orch = _orch()
    result = orch.query(parameter_id="PAR-BEH-001")
    assert result is not None
    assert result.layers_used == LayerUsed.LAYER2_ONLY.value
    assert result.pct_applied is False
    assert result.llmmc_applied is False


def test_simple_query_pipeline_steps():
    """Simple query has only registry step."""
    orch = _orch()
    result = orch.query(parameter_id="PAR-BEH-001")
    assert result is not None
    assert len(result.pipeline_steps) == 1
    assert "Registry" in result.pipeline_steps[0]


def test_simple_query_ci():
    """CI bounds bracket the value."""
    orch = _orch()
    result = orch.query(parameter_id="PAR-BEH-001")
    assert result is not None
    assert result.ci_95[0] <= result.value <= result.ci_95[1]


def test_simple_query_not_found():
    """Non-existent parameter returns None."""
    orch = _orch()
    result = orch.query(parameter_id="PAR-FAKE-999")
    assert result is None


def test_simple_query_timing():
    """Query records elapsed time."""
    orch = _orch()
    result = orch.query(parameter_id="PAR-BEH-001")
    assert result is not None
    assert result.elapsed_ms > 0


# ---------------------------------------------------------------------------
# Contextual query tests (Layer 2 + PCT)
# ---------------------------------------------------------------------------

def test_contextual_query():
    """Contextual query applies PCT."""
    orch = _orch()
    result = orch.query(
        parameter_id="PAR-BEH-016",
        context={
            "target_psi": {"psi_S": "competence_signaling"},
            "anchor_psi": {"psi_S": "welfare_stigma"},
            "anchor_context": "welfare",
        },
    )
    assert result is not None
    assert result.pct_applied is True
    assert result.pct_product_M != 1.0


def test_contextual_query_value_changes():
    """PCT transform changes the value from registry."""
    orch = _orch()
    result = orch.query(
        parameter_id="PAR-BEH-016",
        context={
            "target_psi": {"psi_S": "competence_signaling"},
            "anchor_psi": {"psi_S": "welfare_stigma"},
            "anchor_context": "welfare",
        },
    )
    assert result is not None
    assert result.value != result.registry_value
    # Stigma decrease → lower value
    assert result.value < result.registry_value


def test_contextual_query_layers_used():
    """Contextual query uses Layer 2 + PCT."""
    orch = _orch()
    result = orch.query(
        parameter_id="PAR-BEH-016",
        context={
            "target_psi": {"psi_S": "competence_signaling"},
            "anchor_psi": {"psi_S": "welfare_stigma"},
            "anchor_context": "welfare",
        },
    )
    assert result is not None
    assert result.layers_used == LayerUsed.LAYER2_PLUS_PCT.value


def test_contextual_query_pipeline_steps():
    """Contextual query has registry + PCT steps."""
    orch = _orch()
    result = orch.query(
        parameter_id="PAR-BEH-016",
        context={
            "target_psi": {"psi_S": "competence_signaling"},
            "anchor_psi": {"psi_S": "welfare_stigma"},
            "anchor_context": "welfare",
        },
    )
    assert result is not None
    assert len(result.pipeline_steps) == 2
    assert "PCT" in result.pipeline_steps[1]


def test_contextual_query_provenance():
    """PCT provenance is recorded."""
    orch = _orch()
    result = orch.query(
        parameter_id="PAR-BEH-016",
        context={
            "target_psi": {"psi_S": "competence_signaling"},
            "anchor_psi": {"psi_S": "welfare_stigma"},
            "anchor_context": "welfare",
        },
    )
    assert result is not None
    assert result.pct_anchor_context == "welfare"
    assert result.pct_target_context == "target"
    assert len(result.pct_deltas) > 0


def test_contextual_query_target_without_anchor():
    """target_psi without anchor_psi triggers auto-anchor discovery."""
    orch = _orch()
    result = orch.query(
        parameter_id="PAR-BEH-016",
        context={"target_psi": {"psi_S": "competence_signaling"}},
    )
    assert result is not None
    # PAR-BEH-016 has measurement contexts → auto-anchor should be found
    assert result.pct_applied is True
    assert "auto-anchor" in result.tier_note


# ---------------------------------------------------------------------------
# Calibrated query tests (Layer 2 + PCT + LLMMC)
# ---------------------------------------------------------------------------

def test_calibrated_query():
    """Full pipeline applies PCT and LLMMC."""
    orch = _orch()
    result = orch.query(
        parameter_id="PAR-BEH-016",
        context={
            "target_psi": {"psi_S": "competence_signaling"},
            "anchor_psi": {"psi_S": "welfare_stigma"},
            "anchor_context": "welfare",
        },
        calibrate=True,
    )
    assert result is not None
    assert result.pct_applied is True
    assert result.llmmc_applied is True
    assert result.llmmc_shrinkage < 1.0


def test_calibrated_query_layers_used():
    """Calibrated query uses all layers."""
    orch = _orch()
    result = orch.query(
        parameter_id="PAR-BEH-016",
        context={
            "target_psi": {"psi_S": "competence_signaling"},
            "anchor_psi": {"psi_S": "welfare_stigma"},
            "anchor_context": "welfare",
        },
        calibrate=True,
    )
    assert result is not None
    assert result.layers_used == LayerUsed.LAYER2_PLUS_PCT_LLMMC.value


def test_calibrated_query_pipeline_steps():
    """Calibrated query has 3 steps."""
    orch = _orch()
    result = orch.query(
        parameter_id="PAR-BEH-016",
        context={
            "target_psi": {"psi_S": "competence_signaling"},
            "anchor_psi": {"psi_S": "welfare_stigma"},
            "anchor_context": "welfare",
        },
        calibrate=True,
    )
    assert result is not None
    assert len(result.pipeline_steps) == 3
    assert "LLMMC" in result.pipeline_steps[2]


def test_calibrated_without_context():
    """Calibrate without context skips LLMMC."""
    orch = _orch()
    result = orch.query(
        parameter_id="PAR-BEH-001",
        calibrate=True,
    )
    assert result is not None
    assert result.llmmc_applied is False


# ---------------------------------------------------------------------------
# Batch query tests
# ---------------------------------------------------------------------------

def test_batch_query():
    """Batch query returns list of results."""
    orch = _orch()
    results = orch.batch_query(["PAR-BEH-001", "PAR-BEH-016"])
    assert len(results) == 2
    assert all(r is not None for r in results)


def test_batch_query_with_invalid():
    """Batch query handles not-found gracefully."""
    orch = _orch()
    results = orch.batch_query(["PAR-BEH-001", "PAR-FAKE-999"])
    assert len(results) == 2
    assert results[0] is not None
    assert results[1] is None


def test_batch_query_with_context():
    """Batch query applies shared context."""
    orch = _orch()
    results = orch.batch_query(
        ["PAR-BEH-016"],
        context={
            "target_psi": {"psi_S": "competence_signaling"},
            "anchor_psi": {"psi_S": "welfare_stigma"},
            "anchor_context": "welfare",
        },
    )
    assert len(results) == 1
    assert results[0] is not None
    assert results[0].pct_applied is True


# ---------------------------------------------------------------------------
# Health check tests
# ---------------------------------------------------------------------------

def test_health_check():
    """Health check passes."""
    orch = _orch()
    result = orch.health_check()
    assert isinstance(result, HealthCheckResult)
    assert result.overall is True


def test_health_check_stages():
    """Health check has all 6 stages."""
    orch = _orch()
    result = orch.health_check()
    expected_stages = {"registry", "symbols", "pct", "llmmc", "full_pipeline", "data_files"}
    assert set(result.stages.keys()) == expected_stages


def test_health_check_all_pass():
    """All health check stages pass."""
    orch = _orch()
    result = orch.health_check()
    for stage, ok in result.stages.items():
        assert ok, f"Health check stage '{stage}' failed: {result.details.get(stage)}"


def test_health_check_timing():
    """Health check records timing."""
    orch = _orch()
    result = orch.health_check()
    assert result.elapsed_ms > 0


def test_health_check_to_dict():
    """Health check serializes to dict."""
    orch = _orch()
    result = orch.health_check()
    d = result.to_dict()
    assert "healthy" in d
    assert "stages" in d
    assert "details" in d
    assert d["healthy"] is True


# ---------------------------------------------------------------------------
# Explain tests
# ---------------------------------------------------------------------------

def test_explain_simple():
    """Explain produces readable text."""
    orch = _orch()
    text = orch.explain(parameter_id="PAR-BEH-001")
    assert "Loss Aversion" in text
    assert "PAR-BEH-001" in text
    assert "Pipeline" in text


def test_explain_with_pct():
    """Explain includes PCT details."""
    orch = _orch()
    text = orch.explain(
        parameter_id="PAR-BEH-016",
        context={
            "target_psi": {"psi_S": "competence_signaling"},
            "anchor_psi": {"psi_S": "welfare_stigma"},
            "anchor_context": "welfare",
        },
    )
    assert "PCT Transform" in text
    assert "Product M" in text


def test_explain_not_found():
    """Explain handles not-found."""
    orch = _orch()
    text = orch.explain(parameter_id="PAR-FAKE-999")
    assert "not found" in text


# ---------------------------------------------------------------------------
# Serialization tests
# ---------------------------------------------------------------------------

def test_to_dict_simple():
    """Simple result serializes."""
    orch = _orch()
    result = orch.query(parameter_id="PAR-BEH-001")
    assert result is not None
    d = result.to_dict()
    assert "result" in d
    assert "provenance" in d
    assert "layer2_registry" in d
    assert d["result"]["parameter_id"] == "PAR-BEH-001"


def test_to_dict_with_pct():
    """PCT result includes layer1_pct."""
    orch = _orch()
    result = orch.query(
        parameter_id="PAR-BEH-016",
        context={
            "target_psi": {"psi_S": "competence_signaling"},
            "anchor_psi": {"psi_S": "welfare_stigma"},
            "anchor_context": "welfare",
        },
    )
    assert result is not None
    d = result.to_dict()
    assert "layer1_pct" in d
    assert d["layer1_pct"]["applied"] is True


def test_to_dict_full_pipeline():
    """Full pipeline result includes both layer1 sections."""
    orch = _orch()
    result = orch.query(
        parameter_id="PAR-BEH-016",
        context={
            "target_psi": {"psi_S": "competence_signaling"},
            "anchor_psi": {"psi_S": "welfare_stigma"},
            "anchor_context": "welfare",
        },
        calibrate=True,
    )
    assert result is not None
    d = result.to_dict()
    assert "layer1_pct" in d
    assert "layer1_llmmc" in d


def test_json_serializable():
    """Full result is JSON-serializable."""
    orch = _orch()
    result = orch.query(
        parameter_id="PAR-BEH-016",
        context={
            "target_psi": {"psi_S": "competence_signaling"},
            "anchor_psi": {"psi_S": "welfare_stigma"},
            "anchor_context": "welfare",
        },
        calibrate=True,
    )
    assert result is not None
    json_str = json.dumps(result.to_dict())
    parsed = json.loads(json_str)
    assert parsed["result"]["parameter_id"] == "PAR-BEH-016"
    assert parsed["layer1_pct"]["applied"] is True
    assert parsed["layer1_llmmc"]["applied"] is True


def test_summary():
    """Summary produces one-line summary."""
    orch = _orch()
    result = orch.query(parameter_id="PAR-BEH-001")
    assert result is not None
    s = result.summary()
    assert "PAR-BEH-001" in s
    assert "λ" in s


# ---------------------------------------------------------------------------
# List parameters tests
# ---------------------------------------------------------------------------

def test_list_parameters():
    """List returns parameters."""
    orch = _orch()
    params = orch.list_parameters()
    assert len(params) > 0
    assert "id" in params[0]


def test_list_parameters_filter():
    """List filters by domain."""
    orch = _orch()
    params = orch.list_parameters(domain="FIN")
    assert len(params) > 0
    for p in params:
        assert "FIN" in [d.upper() for d in p["domains"]]


# ---------------------------------------------------------------------------
# Calibrator caching tests
# ---------------------------------------------------------------------------

def test_calibrator_caching():
    """Calibrator is reused across queries."""
    orch = _orch()
    ctx = {
        "target_psi": {"psi_S": "competence_signaling"},
        "anchor_psi": {"psi_S": "welfare_stigma"},
        "anchor_context": "welfare",
    }
    r1 = orch.query(parameter_id="PAR-BEH-016", context=ctx, calibrate=True)
    assert orch._calibrator_fitted is True

    r2 = orch.query(parameter_id="PAR-BEH-016", context=ctx, calibrate=True)
    assert r1.value == r2.value  # Same calibrator → same result


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    tests = [
        # Classification
        test_classify_simple,
        test_classify_contextual,
        test_classify_calibrated,
        test_classify_empty_context,
        # Simple queries
        test_simple_query_by_id,
        test_simple_query_by_symbol,
        test_simple_query_layers_used,
        test_simple_query_pipeline_steps,
        test_simple_query_ci,
        test_simple_query_not_found,
        test_simple_query_timing,
        # Contextual queries
        test_contextual_query,
        test_contextual_query_value_changes,
        test_contextual_query_layers_used,
        test_contextual_query_pipeline_steps,
        test_contextual_query_provenance,
        test_contextual_query_target_without_anchor,
        # Calibrated queries
        test_calibrated_query,
        test_calibrated_query_layers_used,
        test_calibrated_query_pipeline_steps,
        test_calibrated_without_context,
        # Batch
        test_batch_query,
        test_batch_query_with_invalid,
        test_batch_query_with_context,
        # Health check
        test_health_check,
        test_health_check_stages,
        test_health_check_all_pass,
        test_health_check_timing,
        test_health_check_to_dict,
        # Explain
        test_explain_simple,
        test_explain_with_pct,
        test_explain_not_found,
        # Serialization
        test_to_dict_simple,
        test_to_dict_with_pct,
        test_to_dict_full_pipeline,
        test_json_serializable,
        test_summary,
        # List
        test_list_parameters,
        test_list_parameters_filter,
        # Caching
        test_calibrator_caching,
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
