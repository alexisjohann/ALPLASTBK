#!/usr/bin/env python3
"""
Tests for the Immune Gateway — Pre-Response Layer 1 Computation.

Tests the keyword detection that solves the "host decides" paradox:
The LLM no longer decides whether Layer 1 runs. The immune gateway
detects parameter keywords AUTONOMOUSLY and pre-computes values.
"""

import sys
import os
import subprocess
from pathlib import Path

# Add scripts/ to path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from immune_gateway import (
    detect_parameter_query,
    format_output,
    TRIGGER_THRESHOLD,
)


# ============================================================================
# Keyword Detection Tests
# ============================================================================

class TestKeywordDetection:
    """Tests for detect_parameter_query()."""

    # --- Should trigger ---

    def test_loss_aversion_english(self):
        result = detect_parameter_query("What is loss aversion?")
        assert result is not None
        assert result["triggered"] is True
        assert result["score"] >= TRIGGER_THRESHOLD

    def test_loss_aversion_german(self):
        result = detect_parameter_query("Wie stark ist Verlustaversion?")
        assert result is not None
        assert result["triggered"] is True

    def test_present_bias(self):
        result = detect_parameter_query("How strong is present bias?")
        assert result is not None
        assert any("PAR-BEH-003" == m.get("parameter_id") for m in result["matches"])

    def test_direct_parameter_id(self):
        result = detect_parameter_query("Show me PAR-BEH-001 value")
        assert result is not None
        assert result["score"] == 1.0

    def test_greek_symbol_lambda(self):
        result = detect_parameter_query("lambda_R in welfare context")
        assert result is not None
        assert result["score"] == 1.0

    def test_greek_symbol_theta(self):
        result = detect_parameter_query("What is theta_A for this parameter?")
        assert result is not None

    def test_stigma_rejection(self):
        result = detect_parameter_query("How does rejection stigma affect behavior?")
        assert result is not None
        assert any("PAR-BEH-016" == m.get("parameter_id") for m in result["matches"])

    def test_fairness_inequity(self):
        result = detect_parameter_query("Tell me about fairness and inequity aversion")
        assert result is not None

    def test_trust_institutional(self):
        result = detect_parameter_query("How does institutional trust vary?")
        assert result is not None

    def test_crowding_out(self):
        result = detect_parameter_query("Does extrinsic motivation crowd out intrinsic?")
        assert result is not None

    def test_multiple_keywords_bonus(self):
        """Multiple matching keywords should increase score."""
        single = detect_parameter_query("loss behavior")
        double = detect_parameter_query("loss aversion behavior")
        assert single is not None
        assert double is not None
        assert double["score"] >= single["score"]

    def test_question_amplifier_german(self):
        """'wie stark' should amplify the score."""
        base = detect_parameter_query("Verlustaversion im Kontext")
        amplified = detect_parameter_query("Wie stark ist Verlustaversion?")
        assert base is not None
        assert amplified is not None
        assert amplified["score"] > base["score"]

    def test_question_amplifier_english(self):
        """'how strong' should amplify the score."""
        base = detect_parameter_query("present bias in decisions")
        amplified = detect_parameter_query("How strong is present bias?")
        assert base is not None
        assert amplified is not None
        assert amplified["score"] > base["score"]

    def test_identity_parameter(self):
        result = detect_parameter_query("What role does identity play?")
        assert result is not None

    def test_network_segregation(self):
        result = detect_parameter_query("How does network segregation affect outcomes?")
        assert result is not None

    def test_complementarity(self):
        result = detect_parameter_query("Is there complementarity between these factors?")
        assert result is not None

    # --- German umlaut tests (umlaut normalization) ---

    def test_german_umlaut_intrinsische(self):
        """German 'intrinsische' should match via umlaut normalization."""
        result = detect_parameter_query("Wie können wir intrinsische Motivation schützen?")
        assert result is not None
        assert any("PAR-BEH-002" == m.get("parameter_id") for m in result["matches"])

    def test_german_umlaut_verdraengen(self):
        """German 'verdrängt' should match via ä→ae normalization."""
        result = detect_parameter_query("Verdrängt extrinsische Belohnung die Motivation?")
        assert result is not None
        assert any("PAR-BEH-002" == m.get("parameter_id") for m in result["matches"])

    def test_german_umlaut_zugehoerigkeit(self):
        """German 'Zugehörigkeit' should match via ö→oe normalization."""
        result = detect_parameter_query("Welche Rolle spielt Zugehörigkeit?")
        assert result is not None
        assert any("PAR-BEH-011" == m.get("parameter_id") for m in result["matches"])

    def test_german_umlaut_ungerecht(self):
        """German 'Ungerechtigkeit' should match for inequity."""
        result = detect_parameter_query("Ist diese Verteilung ungerecht?")
        assert result is not None

    def test_german_full_sentence_crowding(self):
        """Full German model-building question should trigger crowding-out."""
        result = detect_parameter_query(
            "Wie können wir Mitarbeiter zum Energiesparen motivieren "
            "ohne intrinsische Motivation zu verdrängen?"
        )
        assert result is not None
        assert result["score"] >= 0.9
        assert any("PAR-BEH-002" == m.get("parameter_id") for m in result["matches"])

    # --- Should NOT trigger ---

    def test_git_command_skipped(self):
        result = detect_parameter_query("git push origin main")
        assert result is None

    def test_short_confirmation_skipped(self):
        result = detect_parameter_query("ok")
        assert result is None

    def test_ja_skipped(self):
        result = detect_parameter_query("ja")
        assert result is None

    def test_technical_command_skipped(self):
        result = detect_parameter_query("erstelle eine neue Datei")
        assert result is None

    def test_implementation_request_skipped(self):
        result = detect_parameter_query("implementiere den neuen Algorithmus")
        assert result is None

    def test_weather_question_no_trigger(self):
        result = detect_parameter_query("How is the weather today?")
        assert result is None

    def test_empty_string(self):
        result = detect_parameter_query("")
        assert result is None

    def test_very_short_prompt(self):
        result = detect_parameter_query("hi there")
        assert result is None

    def test_commit_message_skipped(self):
        result = detect_parameter_query("commit this with message fix bug")
        assert result is None

    def test_delete_file_skipped(self):
        result = detect_parameter_query("delete the old test file")
        assert result is None


# ============================================================================
# Output Formatting Tests
# ============================================================================

class TestOutputFormatting:
    """Tests for format_output()."""

    def test_format_with_orchestrator_result(self):
        detection = {
            "triggered": True,
            "query": "loss aversion",
            "matches": [{"parameter_id": "PAR-BEH-001", "keywords": ["loss", "aversion"], "score": 0.95}],
            "score": 0.95,
        }
        orch_result = {
            "parameter_id": "PAR-BEH-001",
            "symbol": "lambda_R",
            "name": "Loss Aversion Coefficient",
            "registry_value": 2.25,
            "range": "[1.8, 3.0]",
            "evidence_tier": "Tier 1",
            "provenance": "Layer 2 (Registry)",
        }
        output = format_output(detection, orch_result)
        assert "IMMUNE GATEWAY" in output
        assert "PAR-BEH-001" in output
        assert "lambda_R" in output
        assert "2.25" in output
        assert "DIRECTIVE" in output
        assert "Do NOT cite from LLM memory" in output

    def test_format_without_orchestrator_result(self):
        detection = {
            "triggered": True,
            "query": "some query",
            "matches": [{"keywords": ["loss"], "score": 0.7}],
            "score": 0.7,
        }
        output = format_output(detection, None)
        assert "IMMUNE GATEWAY" in output
        assert "Orchestrator returned no result" in output
        assert "DIRECTIVE" in output

    def test_format_contains_virus_framework_reference(self):
        detection = {"triggered": True, "query": "test", "matches": [], "score": 0.8}
        output = format_output(detection, None)
        assert "host no longer decides" in output

    def test_format_with_pct_result(self):
        detection = {"triggered": True, "query": "test", "matches": [], "score": 0.8}
        orch_result = {
            "parameter_id": "PAR-BEH-016",
            "symbol": "lambda_R",
            "name": "Rejection Sensitivity",
            "registry_value": 2.5,
            "pct_result": 2.125,
            "anchor_context": "welfare",
            "provenance": "Layer 2 + Layer 1 (PCT)",
        }
        output = format_output(detection, orch_result)
        assert "PCT Transform" in output
        assert "2.125" in output
        assert "welfare" in output


# ============================================================================
# Architecture Tests (verify the paradox is resolved)
# ============================================================================

class TestArchitecturalProperties:
    """Tests verifying the architectural properties of the Immune Gateway."""

    def test_gateway_is_autonomous(self):
        """The gateway triggers WITHOUT LLM involvement."""
        # This tests that detect_parameter_query() works purely on string matching
        # No LLM call is needed — keyword detection is deterministic
        result = detect_parameter_query("What is loss aversion?")
        assert result is not None
        # The result is computed by Python (Layer 1), not by LLM (Layer 3)

    def test_gateway_is_silent_when_not_triggered(self):
        """Non-parameter prompts produce no output (no noise)."""
        result = detect_parameter_query("Tell me about the weather")
        assert result is None

    def test_skip_patterns_prevent_false_triggers(self):
        """Technical commands never trigger the gateway."""
        technical_prompts = [
            "git status",
            "commit changes",
            "fix the bug in line 42",
            "create a new file called test.py",
            "delete the old config",
            "implementiere die Funktion",
        ]
        for prompt in technical_prompts:
            result = detect_parameter_query(prompt)
            assert result is None, f"False trigger on: {prompt}"

    def test_behavioral_keywords_always_trigger(self):
        """Core behavioral economics terms always trigger the gateway."""
        behavioral_prompts = [
            "loss aversion",
            "present bias",
            "inequity aversion",
            "rejection stigma",
            "crowding out intrinsic motivation",
        ]
        for prompt in behavioral_prompts:
            result = detect_parameter_query(prompt)
            assert result is not None, f"Missed trigger on: {prompt}"

    def test_direct_references_always_trigger(self):
        """Direct parameter references always trigger with max score."""
        direct_prompts = [
            "PAR-BEH-001",
            "lambda_R value",
            "theta_A for welfare",
            "beta_ discount factor",
        ]
        for prompt in direct_prompts:
            result = detect_parameter_query(prompt)
            assert result is not None, f"Missed direct trigger on: {prompt}"
            assert result["score"] == 1.0, f"Direct trigger not max score: {prompt}"


# ============================================================================
# Self-Test (CLI)
# ============================================================================

class TestSelfTest:
    """Test the --test flag."""

    def test_self_test_runs(self):
        result = subprocess.run(
            [sys.executable, str(REPO_ROOT / "scripts" / "immune_gateway.py"), "--test"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0
        assert "Self-Test" in result.stdout
        assert "PASS" in result.stdout


# ============================================================================
# Integration with Hook
# ============================================================================

class TestHookIntegration:
    """Test that the hook script references the immune gateway correctly."""

    def test_hook_references_immune_gateway(self):
        hook_path = REPO_ROOT / ".claude" / "hooks" / "user-prompt-submit.sh"
        assert hook_path.exists()
        content = hook_path.read_text()
        assert "immune_gateway.py" in content
        assert "IMMUNE GATEWAY" in content
        assert "Wirt entscheidet" in content or "host decides" in content

    def test_hook_has_timeout(self):
        hook_path = REPO_ROOT / ".claude" / "hooks" / "user-prompt-submit.sh"
        content = hook_path.read_text()
        assert "timeout" in content


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
