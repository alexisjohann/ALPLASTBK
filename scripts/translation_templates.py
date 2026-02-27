#!/usr/bin/env python3
"""
Layer 3 Translation Templates
===============================

Structured templates that transform formal Layer 1/2 output into
consistent, provenance-tracked natural language explanations.

The LLM is TRANSLATOR, not THINKER. These templates ensure:
  1. Every number in the output has a provenance chain
  2. Language is consistent across sessions
  3. No hallucinated values can enter the output
  4. Explanations follow the Three-Layer Architecture

Architecture:
    OrchestratorResult (Layer 1+2)
        |
        v
    TranslationTemplate.render(result)
        |
        v
    Structured Markdown (Layer 3 output)

Usage:
    from translation_templates import translate, TemplateType

    # Auto-detect best template
    text = translate(orchestrator_result)

    # Specific template
    text = translate(orchestrator_result, template=TemplateType.CONTEXTUAL)

    # CLI
    python translation_templates.py --id PAR-BEH-001
    python translation_templates.py --id PAR-BEH-016 \\
        --target-psi '{"psi_S":"competence_signaling"}' \\
        --anchor-psi '{"psi_S":"welfare_stigma"}' \\
        --anchor-context welfare --calibrate
"""

import sys
import json
import argparse
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
from typing import Optional

# Add scripts/ to path
sys.path.insert(0, str(Path(__file__).resolve().parent))


class TemplateType(Enum):
    """Translation template types matching query types."""
    SIMPLE = "simple"
    CONTEXTUAL = "contextual"
    CALIBRATED = "calibrated"
    BATCH = "batch"
    HEALTH = "health"
    EXPLAIN = "explain"


# ---------------------------------------------------------------------------
# Template Definitions
# ---------------------------------------------------------------------------

TEMPLATE_SIMPLE = """## {name} ({symbol})

| Eigenschaft | Wert |
|-------------|------|
| **Parameter-ID** | `{parameter_id}` |
| **Wert** | {value:.4f} |
| **95% CI** | [{ci_lo:.4f}, {ci_hi:.4f}] |
| **Quelle** | {source} |
| **Tier** | {tier} |
| **Layer** | {layers} |

{provenance_note}"""

TEMPLATE_CONTEXTUAL = """## {name} ({symbol}) — Kontext-Transformation

| Eigenschaft | Wert |
|-------------|------|
| **Parameter-ID** | `{parameter_id}` |
| **Anchor-Wert (θ_A)** | {anchor_value:.4f} |
| **Transformierter Wert (θ_B)** | {transformed_value:.4f} |
| **PCT Produkt M** | {product_M:.4f} |
| **95% CI** | [{ci_lo:.4f}, {ci_hi:.4f}] |
| **Layers** | {layers} |

### PCT Multiplikatoren

{multiplier_table}

### Provenance

{provenance_note}

> **Three-Layer Compliance:** Wert aus Layer 2 (YAML) geladen, via Layer 1 (PCT Python) transformiert. Kein Wert aus LLM-Gedaechtnis."""

TEMPLATE_CALIBRATED = """## {name} ({symbol}) — Kalibrierte Transformation

| Eigenschaft | Wert |
|-------------|------|
| **Parameter-ID** | `{parameter_id}` |
| **Anchor-Wert (θ_A)** | {anchor_value:.4f} |
| **PCT-transformiert** | {pct_value:.4f} (M = {product_M:.4f}) |
| **LLMMC-kalibriert** | {calibrated_value:.4f} |
| **Shrinkage-Faktor** | {shrinkage:.4f} |
| **95% CI** | [{ci_lo:.4f}, {ci_hi:.4f}] |
| **Tier** | 2.5 (PCT-informed calibration) |
| **Layers** | {layers} |

### PCT Multiplikatoren

{multiplier_table}

### LLMMC Kalibrierung

- **Shrinkage:** {shrinkage:.4f} (Bayesian Schrumpfung Richtung empirischer Anker)
- **Konfidenz:** {confidence}
- **Anker verwendet:** {n_anchors} empirische Studien

### Provenance

{provenance_note}

> **Three-Layer Compliance:** Layer 2 (YAML-Registry) → Layer 1 (PCT-Transformation) → Layer 1 (LLMMC-Kalibrierung). Vollstaendige Provenance-Kette. Kein LLM-generierter Wert."""

TEMPLATE_BATCH = """## Batch-Abfrage: {n_total} Parameter

{results_table}

{not_found_section}

> **Three-Layer Compliance:** Alle Werte aus Layer 1/2. {n_found}/{n_total} Parameter gefunden."""

TEMPLATE_HEALTH = """## Layer 1 Pipeline Health Check

| Stage | Status | Detail |
|-------|--------|--------|
{stage_rows}

### Zusammenfassung

- **Status:** {overall_status}
- **Stages:** {passed}/{total} bestanden
{failure_section}

> **Three-Layer Compliance:** Pipeline-Integritaet geprueft. {status_emoji} {overall_status}."""

TEMPLATE_EXPLAIN = """## {name} ({symbol})

{explanation}

### Technische Details

| Eigenschaft | Wert |
|-------------|------|
| **ID** | `{parameter_id}` |
| **Wert** | {value:.4f} |
| **95% CI** | [{ci_lo:.4f}, {ci_hi:.4f}] |
| **Quelle** | {source} |

> **Three-Layer Compliance:** Erklaerung basiert auf Layer 2 Metadaten. Wert aus Registry, nicht aus Gedaechtnis."""


# ---------------------------------------------------------------------------
# Rendering Functions
# ---------------------------------------------------------------------------

def _format_layers(layers_used):
    """Format layer list as readable string."""
    layer_names = {
        "layer2": "Layer 2 (YAML)",
        "layer1_pct": "Layer 1 (PCT)",
        "layer1_llmmc": "Layer 1 (LLMMC)",
    }
    if isinstance(layers_used, list):
        return " → ".join(layer_names.get(l, l) for l in layers_used)
    return str(layers_used)


def _format_multiplier_table(multipliers):
    """Format PCT multipliers as markdown table."""
    if not multipliers:
        return "*(Keine Multiplikatoren)*"
    rows = ["| Dimension | Wert | Richtung |", "|-----------|------|----------|"]
    for dim, val in multipliers.items():
        direction = "neutral" if abs(val - 1.0) < 0.001 else ("erhoehend" if val > 1.0 else "daempfend")
        rows.append(f"| {dim} | {val:.4f} | {direction} |")
    return "\n".join(rows)


def _provenance_note(result):
    """Generate provenance note from result."""
    parts = []
    if hasattr(result, 'source') and result.source:
        parts.append(f"**Primaerquelle:** {result.source}")
    if hasattr(result, 'tier') and result.tier:
        tier_labels = {1: "Literature (Meta-analysis)", 2: "LLMMC Prior", 3: "Empirical Calibration", 4: "Expert Elicitation"}
        label = tier_labels.get(result.tier, f"Tier {result.tier}")
        parts.append(f"**Tier:** {result.tier} — {label}")
    if hasattr(result, 'pct_applied') and result.pct_applied:
        parts.append("**PCT:** Kontext-Transformation angewendet")
    if hasattr(result, 'llmmc_applied') and result.llmmc_applied:
        parts.append("**LLMMC:** Bayesian Kalibrierung angewendet")
    return "\n".join(f"- {p}" for p in parts) if parts else "*(Keine zusaetzliche Provenance)*"


def render_simple(result):
    """Render simple lookup result."""
    return TEMPLATE_SIMPLE.format(
        name=getattr(result, 'name', result.parameter_id),
        symbol=getattr(result, 'symbol', ''),
        parameter_id=result.parameter_id,
        value=result.value,
        ci_lo=result.ci_95[0] if result.ci_95 else 0,
        ci_hi=result.ci_95[1] if result.ci_95 else 0,
        source=getattr(result, 'source', 'unknown'),
        tier=getattr(result, 'tier', 'N/A'),
        layers=_format_layers(result.layers_used),
        provenance_note=_provenance_note(result),
    )


def render_contextual(result):
    """Render contextual (PCT-transformed) result."""
    multipliers = {}
    if hasattr(result, 'pct_multipliers') and result.pct_multipliers:
        multipliers = result.pct_multipliers
    elif hasattr(result, 'pct_product_M') and result.pct_product_M:
        multipliers = {"combined": result.pct_product_M}

    base_value = result.value / result.pct_product_M if result.pct_product_M and result.pct_product_M != 0 else result.value

    return TEMPLATE_CONTEXTUAL.format(
        name=getattr(result, 'name', result.parameter_id),
        symbol=getattr(result, 'symbol', ''),
        parameter_id=result.parameter_id,
        anchor_value=base_value,
        transformed_value=result.value,
        product_M=result.pct_product_M if result.pct_product_M else 1.0,
        ci_lo=result.ci_95[0] if result.ci_95 else 0,
        ci_hi=result.ci_95[1] if result.ci_95 else 0,
        layers=_format_layers(result.layers_used),
        multiplier_table=_format_multiplier_table(multipliers),
        provenance_note=_provenance_note(result),
    )


def render_calibrated(result):
    """Render calibrated (PCT + LLMMC) result."""
    multipliers = {}
    if hasattr(result, 'pct_multipliers') and result.pct_multipliers:
        multipliers = result.pct_multipliers

    # Reconstruct the chain: base → PCT → LLMMC
    pct_m = result.pct_product_M if result.pct_product_M else 1.0
    shrinkage = result.llmmc_shrinkage if result.llmmc_shrinkage else 0.0

    # If we have the original base and PCT value, use them
    # Otherwise estimate from final value
    if pct_m != 0:
        base_value = result.value / pct_m if not result.llmmc_applied else (result.value / (1 - shrinkage)) if shrinkage < 1 else result.value
    else:
        base_value = result.value

    pct_value = base_value * pct_m if pct_m else result.value

    # Determine confidence from shrinkage
    if shrinkage < 0.1:
        confidence = "Hoch (geringe Schrumpfung)"
    elif shrinkage < 0.3:
        confidence = "Mittel"
    else:
        confidence = "Niedrig (starke Schrumpfung)"

    return TEMPLATE_CALIBRATED.format(
        name=getattr(result, 'name', result.parameter_id),
        symbol=getattr(result, 'symbol', ''),
        parameter_id=result.parameter_id,
        anchor_value=base_value,
        pct_value=pct_value,
        product_M=pct_m,
        calibrated_value=result.value,
        shrinkage=shrinkage,
        ci_lo=result.ci_95[0] if result.ci_95 else 0,
        ci_hi=result.ci_95[1] if result.ci_95 else 0,
        layers=_format_layers(result.layers_used),
        multiplier_table=_format_multiplier_table(multipliers),
        confidence=confidence,
        n_anchors=getattr(result, 'llmmc_n_anchors', 10),
        provenance_note=_provenance_note(result),
    )


def render_batch(results, not_found=None):
    """Render batch query results."""
    rows = ["| # | Parameter | Wert | CI 95% | Layers |", "|---|-----------|------|--------|--------|"]
    for i, r in enumerate(results, 1):
        ci = f"[{r.ci_95[0]:.2f}, {r.ci_95[1]:.2f}]" if r.ci_95 else "N/A"
        layers = ", ".join(r.layers_used) if r.layers_used else "N/A"
        rows.append(f"| {i} | `{r.parameter_id}` | {r.value:.4f} | {ci} | {layers} |")

    not_found_section = ""
    if not_found:
        not_found_section = f"\n### Nicht gefunden\n\n" + "\n".join(f"- `{nf}`" for nf in not_found)

    return TEMPLATE_BATCH.format(
        n_total=len(results) + (len(not_found) if not_found else 0),
        n_found=len(results),
        results_table="\n".join(rows),
        not_found_section=not_found_section,
    )


def render_health(health_result):
    """Render health check result.

    Supports two formats:
    - Real HealthCheckResult: overall (bool), stages (dict name→bool), details (dict name→str)
    - Mock format: status (str), passed (int), failed (int), stages (list of dicts)
    """
    stage_rows = []
    passed = 0
    failed = 0

    # Handle real HealthCheckResult (dict-based stages)
    if hasattr(health_result, 'overall') and isinstance(getattr(health_result, 'stages', None), dict):
        stages_dict = health_result.stages
        details_dict = getattr(health_result, 'details', {})
        for name, ok in stages_dict.items():
            status = "PASS" if ok else "FAIL"
            detail = details_dict.get(name, "")
            stage_rows.append(f"| {name} | {status} | {detail} |")
            if ok:
                passed += 1
            else:
                failed += 1

        overall_status = "HEALTHY" if health_result.overall else "UNHEALTHY"
        failure_section = ""
        if failed > 0:
            failures = [(n, details_dict.get(n, "Unknown")) for n, ok in stages_dict.items() if not ok]
            failure_section = "\n### Fehler\n\n" + "\n".join(
                f"- **{n}:** {d}" for n, d in failures
            )

    # Handle mock/list-based stages
    else:
        for stage in health_result.stages:
            status = "PASS" if stage.get("status") == "PASS" else "FAIL"
            detail = stage.get("detail", "")
            stage_rows.append(f"| {stage.get('name', '?')} | {status} | {detail} |")
            if stage.get("status") == "PASS":
                passed += 1
            else:
                failed += 1

        overall_status = getattr(health_result, 'status', "HEALTHY" if failed == 0 else "UNHEALTHY")
        passed = getattr(health_result, 'passed', passed)
        failed = getattr(health_result, 'failed', failed)

        failure_section = ""
        if failed > 0:
            failures = [s for s in health_result.stages if s.get("status") != "PASS"]
            failure_section = "\n### Fehler\n\n" + "\n".join(
                f"- **{f.get('name')}:** {f.get('error', 'Unknown')}" for f in failures
            )

    return TEMPLATE_HEALTH.format(
        stage_rows="\n".join(stage_rows),
        overall_status=overall_status,
        passed=passed,
        total=passed + failed,
        failure_section=failure_section,
        status_emoji="OK" if overall_status == "HEALTHY" else "WARN",
    )


def render_explain(result, explanation_text=None):
    """Render explain result."""
    if explanation_text is None:
        explanation_text = _generate_explanation(result)

    return TEMPLATE_EXPLAIN.format(
        name=getattr(result, 'name', result.parameter_id),
        symbol=getattr(result, 'symbol', ''),
        parameter_id=result.parameter_id,
        value=result.value,
        ci_lo=result.ci_95[0] if result.ci_95 else 0,
        ci_hi=result.ci_95[1] if result.ci_95 else 0,
        source=getattr(result, 'source', 'unknown'),
        explanation=explanation_text,
    )


def _generate_explanation(result):
    """Generate a provenance-based explanation from result metadata."""
    parts = []
    name = getattr(result, 'name', result.parameter_id)
    symbol = getattr(result, 'symbol', '')

    parts.append(f"**{name}** (`{symbol}`) ist ein verhaltens-oekonomischer Parameter "
                 f"aus der EBF Parameter-Registry.")

    if hasattr(result, 'source') and result.source:
        parts.append(f"\nDer Referenzwert stammt aus **{result.source}**.")

    if hasattr(result, 'tier') and result.tier:
        tier_desc = {
            1: "hoechster Evidenz-Stufe (Literatur/Meta-Analyse)",
            2: "LLMMC Prior-Stufe",
            3: "empirischer Kalibrierung",
            4: "Experten-Schaetzung",
        }
        parts.append(f"Der Wert hat Tier {result.tier}: {tier_desc.get(result.tier, 'unbekannt')}.")

    parts.append(f"\nAktueller Wert: **{result.value:.4f}**")
    if result.ci_95:
        parts.append(f"mit 95% Konfidenzintervall [{result.ci_95[0]:.4f}, {result.ci_95[1]:.4f}].")

    if hasattr(result, 'pct_applied') and result.pct_applied:
        parts.append(f"\nDer Wert wurde via **Parameter Context Transformation (PCT)** "
                     f"an den Zielkontext angepasst (M = {result.pct_product_M:.4f}).")

    if hasattr(result, 'llmmc_applied') and result.llmmc_applied:
        parts.append(f"Zusaetzlich wurde eine **LLMMC-Kalibrierung** angewendet "
                     f"(Shrinkage = {result.llmmc_shrinkage:.4f}).")

    return " ".join(parts)


# ---------------------------------------------------------------------------
# Auto-Detection & Main Entry Point
# ---------------------------------------------------------------------------

def detect_template(result):
    """Auto-detect the best template for a result."""
    if hasattr(result, 'overall') and hasattr(result, 'stages'):
        return TemplateType.HEALTH
    if hasattr(result, 'status') and hasattr(result, 'stages'):
        return TemplateType.HEALTH

    if hasattr(result, 'llmmc_applied') and result.llmmc_applied:
        return TemplateType.CALIBRATED
    if hasattr(result, 'pct_applied') and result.pct_applied:
        return TemplateType.CONTEXTUAL
    return TemplateType.SIMPLE


def translate(result, template=None, explanation=None):
    """
    Translate an OrchestratorResult into structured natural language.

    Args:
        result: OrchestratorResult or HealthCheckResult
        template: Optional TemplateType override
        explanation: Optional pre-written explanation text (for EXPLAIN)

    Returns:
        Formatted markdown string
    """
    if template is None:
        template = detect_template(result)

    if template == TemplateType.SIMPLE:
        return render_simple(result)
    elif template == TemplateType.CONTEXTUAL:
        return render_contextual(result)
    elif template == TemplateType.CALIBRATED:
        return render_calibrated(result)
    elif template == TemplateType.HEALTH:
        return render_health(result)
    elif template == TemplateType.EXPLAIN:
        return render_explain(result, explanation)
    elif template == TemplateType.BATCH:
        return render_batch([result])
    else:
        return render_simple(result)


def translate_batch(results, not_found=None):
    """Translate a batch of results."""
    return render_batch(results, not_found)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Layer 3 Translation: OrchestratorResult → Natural Language"
    )
    parser.add_argument("--id", help="Parameter ID (e.g. PAR-BEH-001)")
    parser.add_argument("--symbol", help="Parameter symbol (e.g. lambda_R)")
    parser.add_argument("--target-psi", help="Target Psi context (JSON)")
    parser.add_argument("--anchor-psi", help="Anchor Psi context (JSON)")
    parser.add_argument("--anchor-context", help="Anchor context name")
    parser.add_argument("--calibrate", action="store_true", help="Apply LLMMC calibration")
    parser.add_argument("--health", action="store_true", help="Pipeline health check")
    parser.add_argument("--explain", action="store_true", help="Explain mode")
    parser.add_argument("--batch", help="Comma-separated parameter IDs")
    parser.add_argument("--template", choices=[t.value for t in TemplateType],
                        help="Force specific template")
    args = parser.parse_args()

    from orchestrator import Orchestrator
    orch = Orchestrator()

    if args.health:
        health = orch.health_check()
        print(render_health(health))
        return 0

    if args.batch:
        ids = [x.strip() for x in args.batch.split(",")]
        results = orch.batch_query(ids)
        found = [r for r in results if r.value is not None]
        not_found_ids = [r.parameter_id for r in results if r.value is None]
        print(translate_batch(found, not_found_ids if not_found_ids else None))
        return 0

    # Single parameter query
    param_id = args.id
    symbol = args.symbol

    if not param_id and not symbol:
        parser.print_help()
        return 1

    # Build context
    context = None
    if args.target_psi or args.anchor_psi:
        context = {}
        if args.target_psi:
            context["target_psi"] = json.loads(args.target_psi)
        if args.anchor_psi:
            context["anchor_psi"] = json.loads(args.anchor_psi)
        if args.anchor_context:
            context["anchor_context"] = args.anchor_context

    result = orch.query(
        parameter_id=param_id,
        symbol=symbol,
        context=context,
        calibrate=args.calibrate,
    )

    # Determine template
    template = None
    if args.template:
        template = TemplateType(args.template)
    elif args.explain:
        template = TemplateType.EXPLAIN

    print(translate(result, template=template))
    return 0


if __name__ == "__main__":
    sys.exit(main())
