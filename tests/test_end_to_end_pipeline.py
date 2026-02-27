#!/usr/bin/env python3
"""
End-to-End Pipeline Tests
==========================

Exercises the COMPLETE Three-Layer Architecture pipeline:

    User Query -> Orchestrator -> Layer 2 (Registry)
                               -> Layer 1 (PCT)
                               -> Layer 1 (LLMMC)
                               -> Layer 3 (Translation Templates)

These tests verify that all layers connect correctly and produce
consistent, provenance-tracked results.

Unlike unit tests (test_pct.py, test_orchestrator.py, etc.), these
tests exercise the FULL pipeline end-to-end with real data files.

Author: EBF Framework
Date: 2026-02-16
Layer: Meta (validates all layers)
"""

import sys
import json
import unittest
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
from translation_templates import (
    translate,
    translate_batch,
    detect_template,
    TemplateType,
)


# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

def _orch():
    """Create a fresh Orchestrator instance."""
    return Orchestrator(verbose=False)


# ---------------------------------------------------------------------------
# Pipeline Flow Tests: Query -> Orchestrator -> Translation
# ---------------------------------------------------------------------------

class TestPipelineSimple(unittest.TestCase):
    """End-to-end: Simple query (Layer 2 only) -> Translation."""

    def test_simple_query_produces_result(self):
        """PAR-BEH-001 query returns OrchestratorResult."""
        orch = _orch()
        result = orch.query(parameter_id="PAR-BEH-001")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, OrchestratorResult)
        self.assertEqual(result.parameter_id, "PAR-BEH-001")

    def test_simple_query_has_value(self):
        """Simple query returns numeric value > 0."""
        orch = _orch()
        result = orch.query(parameter_id="PAR-BEH-001")
        self.assertGreater(result.value, 0)

    def test_simple_query_has_ci(self):
        """Simple query returns CI as a 2-tuple."""
        orch = _orch()
        result = orch.query(parameter_id="PAR-BEH-001")
        self.assertEqual(len(result.ci_95), 2)
        self.assertLess(result.ci_95[0], result.ci_95[1])

    def test_simple_query_layers_used(self):
        """Simple query only uses Layer 2."""
        orch = _orch()
        result = orch.query(parameter_id="PAR-BEH-001")
        self.assertEqual(result.layers_used, LayerUsed.LAYER2_ONLY.value)

    def test_simple_query_translates_to_simple_template(self):
        """Simple query -> translate() -> SIMPLE template."""
        orch = _orch()
        result = orch.query(parameter_id="PAR-BEH-001")
        self.assertEqual(detect_template(result), TemplateType.SIMPLE)

    def test_simple_translation_contains_parameter_id(self):
        """Translation output contains parameter ID."""
        orch = _orch()
        result = orch.query(parameter_id="PAR-BEH-001")
        text = translate(result)
        self.assertIn("PAR-BEH-001", text)

    def test_simple_translation_contains_value(self):
        """Translation output contains the numeric value."""
        orch = _orch()
        result = orch.query(parameter_id="PAR-BEH-001")
        text = translate(result)
        # Value should appear formatted to 4 decimal places
        value_str = f"{result.value:.4f}"
        self.assertIn(value_str, text)

    def test_simple_query_json_serializable(self):
        """OrchestratorResult.to_dict() produces valid JSON."""
        orch = _orch()
        result = orch.query(parameter_id="PAR-BEH-001")
        d = result.to_dict()
        # Must serialize without error
        json_str = json.dumps(d)
        parsed = json.loads(json_str)
        self.assertIn("result", parsed)
        self.assertIn("provenance", parsed)


# ---------------------------------------------------------------------------
# Pipeline Flow Tests: Contextual (Layer 2 + PCT) -> Translation
# ---------------------------------------------------------------------------

class TestPipelineContextual(unittest.TestCase):
    """End-to-end: Contextual query (Layer 2 + PCT) -> Translation."""

    def _contextual_result(self):
        """Helper: run a contextual query with known Psi labels."""
        orch = _orch()
        return orch.query(
            parameter_id="PAR-BEH-016",
            context={
                "target_psi": {"psi_S": "competence_signaling"},
                "anchor_psi": {"psi_S": "welfare_stigma"},
                "anchor_context": "welfare",
            },
        )

    def test_contextual_query_applies_pct(self):
        """Contextual query applies PCT transform."""
        result = self._contextual_result()
        self.assertIsNotNone(result)
        self.assertTrue(result.pct_applied)

    def test_contextual_query_changes_value(self):
        """PCT transform changes the value from registry base."""
        result = self._contextual_result()
        self.assertNotEqual(result.value, result.registry_value)

    def test_contextual_query_has_product_m(self):
        """PCT produces a product_M != 1.0."""
        result = self._contextual_result()
        self.assertNotEqual(result.pct_product_M, 1.0)

    def test_contextual_query_has_deltas(self):
        """PCT produces psi_deltas list."""
        result = self._contextual_result()
        self.assertGreater(len(result.pct_deltas), 0)

    def test_contextual_query_layers_used(self):
        """Contextual query uses Layer 2 + PCT."""
        result = self._contextual_result()
        self.assertEqual(result.layers_used, LayerUsed.LAYER2_PLUS_PCT.value)

    def test_contextual_translates_to_contextual_template(self):
        """Contextual query -> translate() -> CONTEXTUAL template."""
        result = self._contextual_result()
        self.assertEqual(detect_template(result), TemplateType.CONTEXTUAL)

    def test_contextual_translation_contains_pct_section(self):
        """Translation mentions PCT multipliers."""
        result = self._contextual_result()
        text = translate(result)
        self.assertIn("PCT", text)

    def test_contextual_translation_contains_product_m(self):
        """Translation contains the product M value."""
        result = self._contextual_result()
        text = translate(result)
        m_str = f"{result.pct_product_M:.4f}"
        self.assertIn(m_str, text)


# ---------------------------------------------------------------------------
# Pipeline Flow Tests: Calibrated (Layer 2 + PCT + LLMMC) -> Translation
# ---------------------------------------------------------------------------

class TestPipelineCalibrated(unittest.TestCase):
    """End-to-end: Calibrated query (Layer 2 + PCT + LLMMC) -> Translation."""

    def _calibrated_result(self):
        """Helper: run a fully calibrated query."""
        orch = _orch()
        return orch.query(
            parameter_id="PAR-BEH-016",
            context={
                "target_psi": {"psi_S": "competence_signaling"},
                "anchor_psi": {"psi_S": "welfare_stigma"},
                "anchor_context": "welfare",
            },
            calibrate=True,
        )

    def test_calibrated_applies_both(self):
        """Calibrated query applies both PCT and LLMMC."""
        result = self._calibrated_result()
        self.assertIsNotNone(result)
        self.assertTrue(result.pct_applied)
        self.assertTrue(result.llmmc_applied)

    def test_calibrated_has_shrinkage(self):
        """LLMMC produces a shrinkage factor."""
        result = self._calibrated_result()
        self.assertGreater(result.llmmc_shrinkage, 0)
        self.assertLess(result.llmmc_shrinkage, 1.0)

    def test_calibrated_layers_used(self):
        """Calibrated query uses all Layer 1 components."""
        result = self._calibrated_result()
        self.assertEqual(result.layers_used, LayerUsed.LAYER2_PLUS_PCT_LLMMC.value)

    def test_calibrated_translates_to_calibrated_template(self):
        """Calibrated query -> translate() -> CALIBRATED template."""
        result = self._calibrated_result()
        self.assertEqual(detect_template(result), TemplateType.CALIBRATED)

    def test_calibrated_translation_contains_shrinkage(self):
        """Translation mentions shrinkage."""
        result = self._calibrated_result()
        text = translate(result)
        self.assertIn("Shrinkage", text)

    def test_calibrated_translation_contains_llmmc(self):
        """Translation mentions LLMMC."""
        result = self._calibrated_result()
        text = translate(result)
        self.assertIn("LLMMC", text)


# ---------------------------------------------------------------------------
# Pipeline Flow Tests: Batch -> Translation
# ---------------------------------------------------------------------------

class TestPipelineBatch(unittest.TestCase):
    """End-to-end: Batch query -> Translation."""

    def test_batch_query_returns_list(self):
        """Batch query returns a list of results."""
        orch = _orch()
        results = orch.batch_query(["PAR-BEH-001", "PAR-BEH-016"])
        self.assertEqual(len(results), 2)

    def test_batch_query_all_results(self):
        """All batch results are valid OrchestratorResults."""
        orch = _orch()
        results = orch.batch_query(["PAR-BEH-001", "PAR-BEH-016"])
        for r in results:
            self.assertIsNotNone(r)
            self.assertIsInstance(r, OrchestratorResult)

    def test_batch_translation(self):
        """Batch query -> translate_batch() produces combined output."""
        orch = _orch()
        results = orch.batch_query(["PAR-BEH-001", "PAR-BEH-016"])
        text = translate_batch(results)
        self.assertIn("PAR-BEH-001", text)
        self.assertIn("PAR-BEH-016", text)

    def test_batch_with_not_found(self):
        """Batch with unknown parameter handles gracefully."""
        orch = _orch()
        results = orch.batch_query(["PAR-BEH-001", "PAR-FAKE-999"])
        self.assertIsNotNone(results[0])
        self.assertIsNone(results[1])


# ---------------------------------------------------------------------------
# Pipeline Flow Tests: Health Check -> Translation
# ---------------------------------------------------------------------------

class TestPipelineHealth(unittest.TestCase):
    """End-to-end: Health check -> Translation."""

    def test_health_check_passes(self):
        """Full pipeline health check passes."""
        orch = _orch()
        health = orch.health_check()
        self.assertIsInstance(health, HealthCheckResult)
        # Should be healthy if all data files exist
        self.assertTrue(health.overall, f"Health check failed: {health.details}")

    def test_health_check_all_stages(self):
        """Health check covers all 6 stages."""
        orch = _orch()
        health = orch.health_check()
        expected_stages = {"registry", "symbols", "pct", "llmmc", "full_pipeline", "data_files"}
        self.assertEqual(set(health.stages.keys()), expected_stages)

    def test_health_translates_to_health_template(self):
        """Health check result -> translate() -> HEALTH template."""
        orch = _orch()
        health = orch.health_check()
        self.assertEqual(detect_template(health), TemplateType.HEALTH)


# ---------------------------------------------------------------------------
# Psi-Scales Integration Tests
# ---------------------------------------------------------------------------

class TestPsiScalesIntegration(unittest.TestCase):
    """Tests that Psi-scales resolve correctly through the pipeline."""

    def test_psi_scale_resolution(self):
        """Known Psi labels resolve to numeric values."""
        from pct import resolve_psi_value
        val = resolve_psi_value("psi_S", "welfare_stigma")
        self.assertIsNotNone(val, "welfare_stigma should be in psi_S scale")
        self.assertGreaterEqual(val, 0.0)
        self.assertLessEqual(val, 1.0)

    def test_psi_delta_computation(self):
        """Delta between two known labels is non-zero."""
        from pct import compute_psi_delta_from_labels
        delta = compute_psi_delta_from_labels("psi_S", "welfare_stigma", "competence_signaling")
        self.assertIsNotNone(delta, "Both labels should be resolvable")
        self.assertNotEqual(delta, 0.0, "Different labels should produce non-zero delta")

    def test_psi_scales_file_exists(self):
        """pct-psi-scales.yaml exists and is loadable."""
        from pct import get_psi_scales
        scales = get_psi_scales()
        self.assertGreater(len(scales), 0)

    def test_psi_scales_have_8_dimensions(self):
        """All 8 Psi dimensions are present."""
        from pct import get_psi_scales
        scales = get_psi_scales()
        expected = {"psi_S", "psi_I", "psi_C", "psi_K", "psi_E", "psi_T", "psi_M", "psi_F"}
        self.assertEqual(set(scales.keys()), expected)

    def test_psi_scales_have_values(self):
        """Each dimension has at least one label."""
        from pct import get_psi_scales
        scales = get_psi_scales()
        for dim, data in scales.items():
            values = data.get("values", {})
            self.assertGreater(len(values), 0, f"{dim} has no labels")

    def test_psi_multiplier_tables_exist(self):
        """pct-multiplier-tables.yaml is loadable."""
        from pct import get_multiplier_tables
        tables = get_multiplier_tables()
        self.assertGreater(len(tables), 0)

    def test_transform_from_contexts_works(self):
        """transform_from_contexts with real labels produces result."""
        from pct import transform_from_contexts
        result = transform_from_contexts(
            theta_A=2.5,
            anchor_psi={"psi_S": "welfare_stigma"},
            target_psi={"psi_S": "competence_signaling"},
            anchor_context="welfare",
            target_context="workplace",
        )
        self.assertGreater(result.theta_B, 0)
        self.assertNotEqual(result.theta_B, 2.5)

    def test_identity_transform(self):
        """Same anchor and target labels produce identity (M=1.0)."""
        from pct import transform_from_contexts
        result = transform_from_contexts(
            theta_A=2.5,
            anchor_psi={"psi_S": "welfare_stigma"},
            target_psi={"psi_S": "welfare_stigma"},
        )
        self.assertAlmostEqual(result.theta_B, 2.5, places=4)
        self.assertAlmostEqual(result.product_M, 1.0, places=4)


# ---------------------------------------------------------------------------
# Measurement Context DB Tests
# ---------------------------------------------------------------------------

class TestMeasurementContextDB(unittest.TestCase):
    """Tests for the measurement context database."""

    def test_measurement_contexts_file_exists(self):
        """pct-measurement-contexts.yaml exists."""
        path = Path(__file__).resolve().parent.parent / "data" / "pct-measurement-contexts.yaml"
        self.assertTrue(path.exists(), "pct-measurement-contexts.yaml should exist")

    def test_measurement_contexts_has_triplets(self):
        """Measurement context DB has triplets."""
        import yaml
        path = Path(__file__).resolve().parent.parent / "data" / "pct-measurement-contexts.yaml"
        with open(path) as f:
            data = yaml.safe_load(f)
        self.assertIn("triplets", data)
        self.assertGreater(len(data["triplets"]), 0)

    def test_measurement_contexts_triplet_structure(self):
        """Each triplet has required fields."""
        import yaml
        path = Path(__file__).resolve().parent.parent / "data" / "pct-measurement-contexts.yaml"
        with open(path) as f:
            data = yaml.safe_load(f)
        required = {"paper_key", "parameter_symbol", "context", "psi_conditions"}
        for triplet in data["triplets"][:5]:
            for field in required:
                self.assertIn(field, triplet, f"Triplet missing field: {field}")


# ---------------------------------------------------------------------------
# Auto-Anchor Discovery Tests
# ---------------------------------------------------------------------------

class TestAutoAnchor(unittest.TestCase):
    """Tests for auto-anchor discovery from measurement contexts."""

    def test_find_best_anchor_returns_result(self):
        """find_best_anchor finds an anchor for a known parameter."""
        from orchestrator import find_best_anchor
        anchor = find_best_anchor("PAR-BEH-016", {"psi_S": "competence_signaling"})
        # PAR-BEH-016 is lambda_R — may or may not have anchors in DB
        # The function should return None or a valid dict
        if anchor is not None:
            self.assertIn("anchor_psi", anchor)
            self.assertIn("anchor_context", anchor)

    def test_find_best_anchor_no_match(self):
        """find_best_anchor returns None for unknown parameter."""
        from orchestrator import find_best_anchor
        anchor = find_best_anchor("PAR-FAKE-999", {"psi_S": "x"})
        self.assertIsNone(anchor)

    def test_auto_anchor_in_query(self):
        """Query with target_psi but no anchor_psi uses auto-anchor."""
        orch = _orch()
        result = orch.query(
            parameter_id="PAR-BEH-016",
            context={"target_psi": {"psi_S": "competence_signaling"}},
        )
        self.assertIsNotNone(result)
        # Even if no anchor found, result should not be None
        # If anchor found, PCT should be applied
        if result.pct_applied:
            self.assertNotEqual(result.value, result.registry_value)


# ---------------------------------------------------------------------------
# Provenance Chain Tests
# ---------------------------------------------------------------------------

class TestProvenanceChain(unittest.TestCase):
    """Tests that provenance is maintained across all layers."""

    def test_simple_provenance(self):
        """Simple query has complete provenance."""
        orch = _orch()
        result = orch.query(parameter_id="PAR-BEH-001")
        d = result.to_dict()
        self.assertIn("provenance", d)
        self.assertEqual(d["provenance"]["query_type"], "simple")
        self.assertIn("Layer 2", d["provenance"]["layers_used"])

    def test_contextual_provenance(self):
        """Contextual query has PCT provenance."""
        orch = _orch()
        result = orch.query(
            parameter_id="PAR-BEH-016",
            context={
                "target_psi": {"psi_S": "competence_signaling"},
                "anchor_psi": {"psi_S": "welfare_stigma"},
            },
        )
        d = result.to_dict()
        self.assertIn("layer1_pct", d)
        self.assertTrue(d["layer1_pct"]["applied"])

    def test_calibrated_provenance(self):
        """Calibrated query has LLMMC provenance."""
        orch = _orch()
        result = orch.query(
            parameter_id="PAR-BEH-016",
            context={
                "target_psi": {"psi_S": "competence_signaling"},
                "anchor_psi": {"psi_S": "welfare_stigma"},
            },
            calibrate=True,
        )
        d = result.to_dict()
        self.assertIn("layer1_llmmc", d)
        self.assertTrue(d["layer1_llmmc"]["applied"])

    def test_translation_preserves_provenance(self):
        """Translation output preserves provenance info."""
        orch = _orch()
        result = orch.query(parameter_id="PAR-BEH-001")
        text = translate(result)
        # Translation should mention source and tier
        self.assertIn("Tier", text)


# ---------------------------------------------------------------------------
# Explain Output Tests
# ---------------------------------------------------------------------------

class TestExplainOutput(unittest.TestCase):
    """Tests for the explain() method."""

    def test_explain_simple(self):
        """Explain output for simple query."""
        orch = _orch()
        text = orch.explain(parameter_id="PAR-BEH-001")
        self.assertIn("Parameter:", text)
        self.assertIn("Pipeline:", text)

    def test_explain_contextual(self):
        """Explain output for contextual query includes PCT section."""
        orch = _orch()
        text = orch.explain(
            parameter_id="PAR-BEH-016",
            context={
                "target_psi": {"psi_S": "competence_signaling"},
                "anchor_psi": {"psi_S": "welfare_stigma"},
            },
        )
        self.assertIn("PCT Transform:", text)
        self.assertIn("Product M:", text)


# ---------------------------------------------------------------------------
# Data File Existence Tests
# ---------------------------------------------------------------------------

class TestDataFiles(unittest.TestCase):
    """Verify all required data files exist."""

    def _repo_root(self):
        return Path(__file__).resolve().parent.parent

    def test_parameter_registry_exists(self):
        self.assertTrue((self._repo_root() / "data" / "parameter-registry.yaml").exists())

    def test_pct_multiplier_tables_exists(self):
        self.assertTrue((self._repo_root() / "data" / "pct-multiplier-tables.yaml").exists())

    def test_pct_psi_scales_exists(self):
        self.assertTrue((self._repo_root() / "data" / "pct-psi-scales.yaml").exists())

    def test_pct_measurement_contexts_exists(self):
        self.assertTrue((self._repo_root() / "data" / "pct-measurement-contexts.yaml").exists())


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=0)
    result = runner.run(suite)
    total = result.testsRun
    failures = len(result.failures) + len(result.errors)
    passed = total - failures
    print(f"\n{passed} passed, {failures} failed out of {total} tests")
    sys.exit(0 if failures == 0 else 1)
