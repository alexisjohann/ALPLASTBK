#!/usr/bin/env python3
"""
Tests for Layer 3 Translation Templates
=========================================

Verifies that structured templates correctly translate
OrchestratorResult objects into provenance-tracked markdown.
"""

import sys
import unittest
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

# Add scripts/ to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from translation_templates import (
    translate,
    translate_batch,
    detect_template,
    render_simple,
    render_contextual,
    render_calibrated,
    render_health,
    render_explain,
    TemplateType,
    _format_layers,
    _format_multiplier_table,
    _provenance_note,
)


# ---------------------------------------------------------------------------
# Mock dataclasses (lightweight stand-ins for OrchestratorResult)
# ---------------------------------------------------------------------------

@dataclass
class MockResult:
    parameter_id: str = "PAR-BEH-001"
    value: float = 2.35
    ci_95: Tuple[float, float] = (1.8, 3.1)
    layers_used: List[str] = field(default_factory=lambda: ["layer2"])
    name: str = "Loss Aversion Coefficient"
    symbol: str = "lambda"
    source: str = "kahneman1979prospect"
    tier: int = 1
    pct_applied: bool = False
    pct_product_M: Optional[float] = None
    pct_multipliers: Optional[dict] = None
    llmmc_applied: bool = False
    llmmc_shrinkage: Optional[float] = None
    llmmc_n_anchors: int = 0


@dataclass
class MockHealthResult:
    """Mock health result using list-based stages format."""
    status: str = "HEALTHY"
    passed: int = 6
    failed: int = 0
    stages: List[dict] = field(default_factory=lambda: [
        {"name": "Registry", "status": "PASS", "detail": "140 params"},
        {"name": "Symbols", "status": "PASS", "detail": "OK"},
        {"name": "PCT", "status": "PASS", "detail": "OK"},
        {"name": "LLMMC", "status": "PASS", "detail": "OK"},
        {"name": "Integration", "status": "PASS", "detail": "OK"},
        {"name": "API", "status": "PASS", "detail": "OK"},
    ])


@dataclass
class MockRealHealthResult:
    """Mock health result matching real HealthCheckResult format (dict-based)."""
    overall: bool = True
    stages: dict = field(default_factory=lambda: {
        "registry": True, "symbols": True, "pct": True,
        "llmmc": True, "full_pipeline": True, "data_files": True,
    })
    details: dict = field(default_factory=lambda: {
        "registry": "140 parameters loaded",
        "symbols": "OK",
        "pct": "OK",
        "llmmc": "OK",
        "full_pipeline": "OK",
        "data_files": "All present",
    })
    elapsed_ms: float = 50.0


# ---------------------------------------------------------------------------
# Tests: Template Detection
# ---------------------------------------------------------------------------

class TestTemplateDetection(unittest.TestCase):

    def test_detect_simple(self):
        r = MockResult()
        self.assertEqual(detect_template(r), TemplateType.SIMPLE)

    def test_detect_contextual(self):
        r = MockResult(pct_applied=True, pct_product_M=0.85)
        self.assertEqual(detect_template(r), TemplateType.CONTEXTUAL)

    def test_detect_calibrated(self):
        r = MockResult(pct_applied=True, llmmc_applied=True, llmmc_shrinkage=0.1)
        self.assertEqual(detect_template(r), TemplateType.CALIBRATED)

    def test_detect_health(self):
        h = MockHealthResult()
        self.assertEqual(detect_template(h), TemplateType.HEALTH)

    def test_detect_real_health(self):
        h = MockRealHealthResult()
        self.assertEqual(detect_template(h), TemplateType.HEALTH)


# ---------------------------------------------------------------------------
# Tests: Simple Template
# ---------------------------------------------------------------------------

class TestSimpleTemplate(unittest.TestCase):

    def test_contains_parameter_id(self):
        r = MockResult()
        text = render_simple(r)
        self.assertIn("PAR-BEH-001", text)

    def test_contains_value(self):
        r = MockResult()
        text = render_simple(r)
        self.assertIn("2.3500", text)

    def test_contains_ci(self):
        r = MockResult()
        text = render_simple(r)
        self.assertIn("1.8000", text)
        self.assertIn("3.1000", text)

    def test_contains_source(self):
        r = MockResult()
        text = render_simple(r)
        self.assertIn("kahneman1979prospect", text)

    def test_contains_layer_info(self):
        r = MockResult()
        text = render_simple(r)
        self.assertIn("Layer 2", text)

    def test_contains_provenance(self):
        r = MockResult()
        text = render_simple(r)
        self.assertIn("Tier", text)


# ---------------------------------------------------------------------------
# Tests: Contextual Template
# ---------------------------------------------------------------------------

class TestContextualTemplate(unittest.TestCase):

    def test_contains_pct_section(self):
        r = MockResult(
            value=1.53, pct_applied=True, pct_product_M=0.765,
            pct_multipliers={"Psi_S": 0.85, "Psi_I": 0.90},
            layers_used=["layer2", "layer1_pct"],
        )
        text = render_contextual(r)
        self.assertIn("PCT Multiplikatoren", text)
        self.assertIn("Psi_S", text)
        self.assertIn("0.8500", text)

    def test_contains_product_M(self):
        r = MockResult(
            value=1.53, pct_applied=True, pct_product_M=0.765,
            layers_used=["layer2", "layer1_pct"],
        )
        text = render_contextual(r)
        self.assertIn("0.7650", text)

    def test_contains_tla_compliance(self):
        r = MockResult(
            value=1.53, pct_applied=True, pct_product_M=0.765,
            layers_used=["layer2", "layer1_pct"],
        )
        text = render_contextual(r)
        self.assertIn("Three-Layer Compliance", text)
        self.assertIn("Kein Wert aus LLM-Gedaechtnis", text)

    def test_multiplier_direction_labels(self):
        r = MockResult(
            value=1.53, pct_applied=True, pct_product_M=0.765,
            pct_multipliers={"Psi_S": 0.85, "Psi_K": 1.15, "Psi_I": 1.0},
            layers_used=["layer2", "layer1_pct"],
        )
        text = render_contextual(r)
        self.assertIn("daempfend", text)
        self.assertIn("erhoehend", text)
        self.assertIn("neutral", text)


# ---------------------------------------------------------------------------
# Tests: Calibrated Template
# ---------------------------------------------------------------------------

class TestCalibratedTemplate(unittest.TestCase):

    def test_contains_shrinkage(self):
        r = MockResult(
            value=1.485, pct_applied=True, pct_product_M=0.765,
            llmmc_applied=True, llmmc_shrinkage=0.127,
            layers_used=["layer2", "layer1_pct", "layer1_llmmc"],
        )
        text = render_calibrated(r)
        self.assertIn("0.1270", text)
        self.assertIn("Shrinkage", text)

    def test_contains_tier_2_5(self):
        r = MockResult(
            value=1.485, pct_applied=True, pct_product_M=0.765,
            llmmc_applied=True, llmmc_shrinkage=0.127,
            layers_used=["layer2", "layer1_pct", "layer1_llmmc"],
        )
        text = render_calibrated(r)
        self.assertIn("2.5", text)
        self.assertIn("PCT-informed calibration", text)

    def test_contains_llmmc_section(self):
        r = MockResult(
            value=1.485, pct_applied=True, pct_product_M=0.765,
            llmmc_applied=True, llmmc_shrinkage=0.127,
            layers_used=["layer2", "layer1_pct", "layer1_llmmc"],
        )
        text = render_calibrated(r)
        self.assertIn("LLMMC Kalibrierung", text)
        self.assertIn("Bayesian", text)

    def test_confidence_high_shrinkage(self):
        r = MockResult(
            value=1.485, pct_applied=True, pct_product_M=0.765,
            llmmc_applied=True, llmmc_shrinkage=0.05,
            layers_used=["layer2", "layer1_pct", "layer1_llmmc"],
        )
        text = render_calibrated(r)
        self.assertIn("Hoch", text)

    def test_confidence_low_shrinkage(self):
        r = MockResult(
            value=1.485, pct_applied=True, pct_product_M=0.765,
            llmmc_applied=True, llmmc_shrinkage=0.5,
            layers_used=["layer2", "layer1_pct", "layer1_llmmc"],
        )
        text = render_calibrated(r)
        self.assertIn("Niedrig", text)


# ---------------------------------------------------------------------------
# Tests: Batch Template
# ---------------------------------------------------------------------------

class TestBatchTemplate(unittest.TestCase):

    def test_batch_shows_all_results(self):
        results = [
            MockResult(parameter_id="PAR-BEH-001", value=2.35),
            MockResult(parameter_id="PAR-BEH-016", value=1.53),
        ]
        text = translate_batch(results)
        self.assertIn("PAR-BEH-001", text)
        self.assertIn("PAR-BEH-016", text)

    def test_batch_shows_not_found(self):
        results = [MockResult(parameter_id="PAR-BEH-001", value=2.35)]
        text = translate_batch(results, not_found=["PAR-FAKE-999"])
        self.assertIn("PAR-FAKE-999", text)
        self.assertIn("Nicht gefunden", text)

    def test_batch_count(self):
        results = [MockResult(), MockResult()]
        text = translate_batch(results, not_found=["X"])
        self.assertIn("3 Parameter", text)


# ---------------------------------------------------------------------------
# Tests: Health Template
# ---------------------------------------------------------------------------

class TestHealthTemplate(unittest.TestCase):

    def test_healthy_status(self):
        h = MockHealthResult()
        text = render_health(h)
        self.assertIn("HEALTHY", text)
        self.assertIn("6/6", text)

    def test_unhealthy_shows_failures(self):
        h = MockHealthResult(
            status="UNHEALTHY", passed=4, failed=2,
            stages=[
                {"name": "Registry", "status": "PASS", "detail": "OK"},
                {"name": "Symbols", "status": "PASS", "detail": "OK"},
                {"name": "PCT", "status": "FAIL", "error": "Module not found"},
                {"name": "LLMMC", "status": "PASS", "detail": "OK"},
                {"name": "Integration", "status": "FAIL", "error": "Broken"},
                {"name": "API", "status": "PASS", "detail": "OK"},
            ]
        )
        text = render_health(h)
        self.assertIn("UNHEALTHY", text)
        self.assertIn("Module not found", text)
        self.assertIn("4/6", text)

    def test_real_health_format_healthy(self):
        h = MockRealHealthResult()
        text = render_health(h)
        self.assertIn("HEALTHY", text)
        self.assertIn("6/6", text)
        self.assertIn("registry", text)

    def test_real_health_format_unhealthy(self):
        h = MockRealHealthResult(
            overall=False,
            stages={"registry": True, "symbols": True, "pct": False, "llmmc": True, "full_pipeline": False, "data_files": True},
            details={"registry": "OK", "symbols": "OK", "pct": "Import error", "llmmc": "OK", "full_pipeline": "Broken", "data_files": "OK"},
        )
        text = render_health(h)
        self.assertIn("UNHEALTHY", text)
        self.assertIn("Import error", text)
        self.assertIn("4/6", text)


# ---------------------------------------------------------------------------
# Tests: Explain Template
# ---------------------------------------------------------------------------

class TestExplainTemplate(unittest.TestCase):

    def test_explain_contains_description(self):
        r = MockResult()
        text = render_explain(r)
        self.assertIn("Loss Aversion Coefficient", text)
        self.assertIn("Parameter-Registry", text)

    def test_explain_with_custom_text(self):
        r = MockResult()
        text = render_explain(r, explanation_text="Custom explanation here.")
        self.assertIn("Custom explanation here", text)

    def test_explain_contains_compliance_note(self):
        r = MockResult()
        text = render_explain(r)
        self.assertIn("Three-Layer Compliance", text)


# ---------------------------------------------------------------------------
# Tests: translate() auto-detection
# ---------------------------------------------------------------------------

class TestTranslateAutoDetect(unittest.TestCase):

    def test_auto_simple(self):
        r = MockResult()
        text = translate(r)
        self.assertIn("PAR-BEH-001", text)
        self.assertNotIn("PCT Multiplikatoren", text)

    def test_auto_contextual(self):
        r = MockResult(
            value=1.53, pct_applied=True, pct_product_M=0.765,
            layers_used=["layer2", "layer1_pct"],
        )
        text = translate(r)
        self.assertIn("Kontext-Transformation", text)

    def test_auto_calibrated(self):
        r = MockResult(
            value=1.485, pct_applied=True, pct_product_M=0.765,
            llmmc_applied=True, llmmc_shrinkage=0.127,
            layers_used=["layer2", "layer1_pct", "layer1_llmmc"],
        )
        text = translate(r)
        self.assertIn("Kalibrierte Transformation", text)

    def test_template_override(self):
        r = MockResult()
        text = translate(r, template=TemplateType.EXPLAIN)
        self.assertIn("Three-Layer Compliance", text)
        self.assertIn("Parameter-Registry", text)


# ---------------------------------------------------------------------------
# Tests: Helper Functions
# ---------------------------------------------------------------------------

class TestHelpers(unittest.TestCase):

    def test_format_layers(self):
        result = _format_layers(["layer2", "layer1_pct"])
        self.assertIn("Layer 2", result)
        self.assertIn("PCT", result)

    def test_format_multiplier_table_empty(self):
        result = _format_multiplier_table({})
        self.assertIn("Keine Multiplikatoren", result)

    def test_format_multiplier_table_values(self):
        result = _format_multiplier_table({"Psi_S": 0.85})
        self.assertIn("Psi_S", result)
        self.assertIn("0.8500", result)
        self.assertIn("daempfend", result)

    def test_provenance_note_with_source(self):
        r = MockResult(source="test_paper_2024")
        result = _provenance_note(r)
        self.assertIn("test_paper_2024", result)


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Custom runner for summary
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=0)
    result = runner.run(suite)
    total = result.testsRun
    failures = len(result.failures) + len(result.errors)
    passed = total - failures
    print(f"\n{passed} passed, {failures} failed out of {total} tests")
    sys.exit(0 if failures == 0 else 1)
