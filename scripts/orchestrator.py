#!/usr/bin/env python3
"""
EBF Three-Layer Orchestrator
=============================

Formal orchestrator connecting the three EBF layers:

    Layer 1 (Python)  — Formal Computation (susceptibility=0.0)
    Layer 2 (YAML)    — Parameter Store    (susceptibility=0.3)
    Layer 3 (LLM)     — Translation        (susceptibility=0.8)

The orchestrator ensures that:
  1. Every numeric value comes from Layer 1 or Layer 2 (never from LLM memory)
  2. PCT transformations are applied automatically when context differs
  3. LLMMC calibration is applied when needed
  4. Full provenance chain is maintained

Architecture:
    User Query
        |
        v
    QueryRouter  -->  classify(query) -> QueryType
        |
        v
    Orchestrator -->  route to appropriate pipeline
        |
    +---+---+---+
    |       |       |
    v       v       v
  Layer2  Layer1  Layer1
  (Load)  (PCT)   (LLMMC)
        |
        v
    OrchestratorResult (full provenance)

Usage:
    from orchestrator import Orchestrator
    orch = Orchestrator()

    # Simple lookup (Layer 2 only)
    result = orch.query("PAR-BEH-001")

    # Context-aware lookup (Layer 2 + Layer 1 PCT)
    result = orch.query("PAR-BEH-016", context={
        "target_psi": {"psi_S": "competence_signaling"},
        "anchor_psi": {"psi_S": "welfare_stigma"},
        "anchor_context": "welfare",
    })

    # Full pipeline (Layer 2 + Layer 1 PCT + Layer 1 LLMMC)
    result = orch.query("PAR-BEH-016", context={...}, calibrate=True)

    # Batch query
    results = orch.batch_query(["PAR-BEH-001", "PAR-BEH-016"])

    # CLI
    python orchestrator.py --id PAR-BEH-001
    python orchestrator.py --id PAR-BEH-016 --context welfare --calibrate
    python orchestrator.py --batch PAR-BEH-001,PAR-BEH-016
    python orchestrator.py --health

Author: EBF Framework
Date: 2026-02-15
Layer: Meta (connects Layer 1, 2, 3)
SSOT: data/knowledge/canonical/three-layer-architecture.yaml
"""

import sys
import json
import time
import argparse
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any

# Add scripts/ to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

REPO_ROOT = Path(__file__).resolve().parent.parent
MEASUREMENT_CONTEXTS_PATH = REPO_ROOT / "data" / "pct-measurement-contexts.yaml"


# ---------------------------------------------------------------------------
# Auto-anchor discovery from measurement context DB
# ---------------------------------------------------------------------------

def _load_measurement_contexts(measurement_contexts_path: Path = None) -> list:
    """Load triplets from measurement contexts YAML."""
    try:
        import yaml
    except ImportError:
        return []

    path = measurement_contexts_path or MEASUREMENT_CONTEXTS_PATH
    if not path.exists():
        return []

    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return data.get("triplets", [])


def _compute_psi_distance(
    anchor_psi: Dict[str, str],
    target_psi: Dict[str, str],
) -> float:
    """
    Compute Euclidean distance between two Psi-condition vectors
    using pct-psi-scales.yaml for numeric resolution.

    Returns distance in [0, sqrt(8)] where 0 = identical, higher = more different.
    Returns 999.0 if no dimensions can be resolved.
    """
    try:
        from pct import resolve_psi_value
    except ImportError:
        return 999.0

    sum_sq = 0.0
    n_resolved = 0

    all_dims = set(anchor_psi.keys()) | set(target_psi.keys())
    for dim in all_dims:
        a_label = anchor_psi.get(dim, "")
        t_label = target_psi.get(dim, "")

        if a_label and t_label:
            a_val = resolve_psi_value(dim, a_label)
            t_val = resolve_psi_value(dim, t_label)
            if a_val is not None and t_val is not None:
                sum_sq += (t_val - a_val) ** 2
                n_resolved += 1
        elif a_label and not t_label:
            # Anchor has dimension, target doesn't — moderate penalty
            sum_sq += 0.1
            n_resolved += 1
        elif t_label and not a_label:
            # Target has dimension, anchor doesn't — moderate penalty
            sum_sq += 0.1
            n_resolved += 1

    if n_resolved == 0:
        return 999.0

    return sum_sq ** 0.5


# Study type preference (lower = better)
_STUDY_TYPE_RANK = {
    "field_data": 0,
    "field_experiment": 0,
    "natural_experiment": 1,
    "lab_experiment": 2,
    "survey_data": 3,
    "survey": 3,
    "meta_analysis": 1,
    "administrative_data": 1,
    "historical_analysis": 4,
    "theoretical_framework": 5,
    "theoretical": 5,
}


def find_best_anchor(
    parameter_id: str,
    target_psi: Dict[str, str],
    measurement_contexts_path: Path = None,
    top_k: int = 1,
) -> Optional[Dict]:
    """
    Find the best anchor context from the measurement context database.

    Scoring uses three criteria (weighted):
      1. Psi-distance (via pct-psi-scales.yaml): smaller = better (weight 0.5)
      2. Has numeric theta_A: strong bonus (weight 0.3)
      3. Study type rank: field > lab > theoretical (weight 0.2)

    Args:
        parameter_id: EBF parameter ID (e.g. "PAR-BEH-016")
        target_psi: Target Psi conditions dict
        measurement_contexts_path: Override path for testing
        top_k: Return this many ranked candidates (default 1)

    Returns:
        If top_k == 1: Dict with best anchor, or None
        If top_k > 1: List of ranked anchor dicts
    """
    triplets = _load_measurement_contexts(measurement_contexts_path)
    if not triplets:
        return None if top_k == 1 else []

    # Filter triplets matching the parameter_id or symbol
    candidates = [
        t for t in triplets
        if t.get("parameter_id") == parameter_id
    ]

    if not candidates:
        return None if top_k == 1 else []

    scored = []
    for c in candidates:
        psi = c.get("psi_conditions", {})
        if not psi:
            continue

        # Criterion 1: Psi-distance (lower = better, normalized to [0, 1])
        dist = _compute_psi_distance(psi, target_psi)
        dist_score = min(dist / 3.0, 1.0)  # normalize: 3.0 = max expected

        # Criterion 2: Has numeric theta_A (0 = yes, 1 = no)
        val_str = str(c.get("value_estimate", ""))
        has_numeric = 0.0
        theta_A = None
        try:
            theta_A = float(val_str)
            has_numeric = 0.0
        except (ValueError, TypeError):
            has_numeric = 1.0

        # Criterion 3: Study type rank (normalized to [0, 1])
        study = c.get("study_type", "theoretical")
        rank = _STUDY_TYPE_RANK.get(study, 5)
        study_score = rank / 5.0

        # Combined score (lower = better)
        combined = 0.5 * dist_score + 0.3 * has_numeric + 0.2 * study_score

        scored.append((combined, dist, c, theta_A))

    if not scored:
        return None if top_k == 1 else []

    # Sort by combined score (ascending = best first)
    scored.sort(key=lambda x: x[0])

    def _make_result(score_tuple):
        combined, dist, triplet, theta_val = score_tuple
        psi = triplet.get("psi_conditions", {})
        ctx = triplet.get("context", "measurement_context")
        source = triplet.get("paper_key", "")

        result = {
            "anchor_psi": psi,
            "anchor_context": f"{ctx} ({source})" if source else ctx,
            "score": round(combined, 4),
            "psi_distance": round(dist, 4),
            "study_type": triplet.get("study_type", ""),
            "paper_key": source,
        }
        if theta_val is not None:
            result["theta_A"] = theta_val
        return result

    if top_k == 1:
        return _make_result(scored[0])
    else:
        return [_make_result(s) for s in scored[:top_k]]


# ---------------------------------------------------------------------------
# Query classification
# ---------------------------------------------------------------------------

class QueryType(Enum):
    """Classification of parameter queries by pipeline depth."""
    SIMPLE = "simple"               # Layer 2 only (registry lookup)
    CONTEXTUAL = "contextual"       # Layer 2 + Layer 1 PCT
    CALIBRATED = "calibrated"       # Layer 2 + Layer 1 PCT + Layer 1 LLMMC
    BATCH = "batch"                 # Multiple parameters
    HEALTH = "health"               # Pipeline health check


class LayerUsed(Enum):
    """Which layers were activated during processing."""
    LAYER2_ONLY = "Layer 2 only (Registry)"
    LAYER2_PLUS_PCT = "Layer 2 + Layer 1 (PCT)"
    LAYER2_PLUS_PCT_LLMMC = "Layer 2 + Layer 1 (PCT + LLMMC)"


# ---------------------------------------------------------------------------
# Result dataclass
# ---------------------------------------------------------------------------

@dataclass
class OrchestratorResult:
    """Complete result with provenance chain from all layers."""
    # Core result
    parameter_id: str
    symbol: str
    name: str
    value: float
    ci_95: tuple = (0.0, 0.0)

    # Provenance
    query_type: str = "simple"
    layers_used: str = "Layer 2 only (Registry)"
    pipeline_steps: List[str] = field(default_factory=list)
    tier: int = 2
    tier_note: str = ""
    source: str = ""

    # Layer 2 (Registry)
    registry_value: float = 0.0
    registry_source: str = ""

    # Layer 1 (PCT)
    pct_applied: bool = False
    pct_product_M: float = 1.0
    pct_anchor_context: str = ""
    pct_target_context: str = ""
    pct_deltas: List[Dict] = field(default_factory=list)

    # Layer 1 (LLMMC)
    llmmc_applied: bool = False
    llmmc_shrinkage: float = 1.0

    # Timing
    elapsed_ms: float = 0.0

    def to_dict(self) -> Dict:
        """Full JSON-serializable output with provenance."""
        d = {
            "result": {
                "parameter_id": self.parameter_id,
                "symbol": self.symbol,
                "name": self.name,
                "value": round(self.value, 4),
                "ci_95": [round(self.ci_95[0], 4), round(self.ci_95[1], 4)],
                "tier": self.tier,
                "tier_note": self.tier_note,
            },
            "provenance": {
                "query_type": self.query_type,
                "layers_used": self.layers_used,
                "pipeline_steps": self.pipeline_steps,
                "elapsed_ms": round(self.elapsed_ms, 1),
            },
            "layer2_registry": {
                "value": round(self.registry_value, 4),
                "source": self.registry_source,
            },
        }
        if self.pct_applied:
            d["layer1_pct"] = {
                "applied": True,
                "product_M": round(self.pct_product_M, 4),
                "anchor_context": self.pct_anchor_context,
                "target_context": self.pct_target_context,
                "deltas": self.pct_deltas,
            }
        if self.llmmc_applied:
            d["layer1_llmmc"] = {
                "applied": True,
                "shrinkage": round(self.llmmc_shrinkage, 4),
            }
        return d

    def summary(self) -> str:
        """Human-readable one-line summary."""
        parts = [f"{self.parameter_id} ({self.symbol})"]
        parts.append(f"= {self.value:.4f}")
        parts.append(f"[{self.ci_95[0]:.4f}, {self.ci_95[1]:.4f}]")
        if self.pct_applied:
            parts.append(f"PCT(M={self.pct_product_M:.3f})")
        if self.llmmc_applied:
            parts.append(f"LLMMC(s={self.llmmc_shrinkage:.3f})")
        parts.append(f"Tier {self.tier}")
        return " | ".join(parts)


# ---------------------------------------------------------------------------
# Health check result
# ---------------------------------------------------------------------------

@dataclass
class HealthCheckResult:
    """Result of pipeline health check."""
    overall: bool = True
    stages: Dict[str, bool] = field(default_factory=dict)
    details: Dict[str, str] = field(default_factory=dict)
    elapsed_ms: float = 0.0

    def to_dict(self) -> Dict:
        return {
            "healthy": self.overall,
            "stages": self.stages,
            "details": self.details,
            "elapsed_ms": round(self.elapsed_ms, 1),
        }


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------

class Orchestrator:
    """
    EBF Three-Layer Orchestrator.

    Connects Layer 1 (formal computation) with Layer 2 (parameter store)
    and ensures Layer 3 (LLM) never supplies numeric values.

    Principle: Compute, Don't Hallucinate.
    """

    def __init__(self, verbose: bool = False):
        self._verbose = verbose
        self._calibrator = None
        self._calibrator_fitted = False

    def _log(self, msg: str):
        if self._verbose:
            print(f"  [orchestrator] {msg}")

    # -------------------------------------------------------------------
    # Query classification
    # -------------------------------------------------------------------

    def classify(
        self,
        parameter_id: str = None,
        symbol: str = None,
        context: Dict = None,
        calibrate: bool = False,
    ) -> QueryType:
        """Classify a query to determine which pipeline to use."""
        if calibrate and context:
            return QueryType.CALIBRATED
        if context and (context.get("target_psi") or context.get("anchor_psi")):
            return QueryType.CONTEXTUAL
        return QueryType.SIMPLE

    # -------------------------------------------------------------------
    # Main query entry point
    # -------------------------------------------------------------------

    def query(
        self,
        parameter_id: str = None,
        symbol: str = None,
        context: Dict = None,
        calibrate: bool = False,
    ) -> Optional[OrchestratorResult]:
        """
        Universal parameter query.

        Args:
            parameter_id: Registry ID (e.g. "PAR-BEH-001")
            symbol: Parameter symbol (e.g. "lambda_R")
            context: Context specification dict:
                {
                    "target_psi": {"psi_S": "label", ...},
                    "anchor_psi": {"psi_S": "label", ...},
                    "anchor_context": "welfare",
                    "domain": "finance",
                }
            calibrate: Whether to apply LLMMC calibration

        Returns:
            OrchestratorResult with full provenance, or None
        """
        t_start = time.monotonic()
        ctx = context or {}

        query_type = self.classify(parameter_id, symbol, ctx, calibrate)
        self._log(f"Query type: {query_type.value}")

        steps = []

        # -----------------------------------------------------------
        # Step 1: Layer 2 — Load from registry
        # -----------------------------------------------------------
        steps.append("Layer 2: Registry lookup")
        self._log("Step 1: Loading from parameter-registry.yaml")

        from parameter_api import get_parameter, _find_parameter
        base = get_parameter(
            parameter_id=parameter_id,
            symbol=symbol,
            domain=ctx.get("domain"),
        )
        if base is None:
            self._log(f"Parameter not found: {parameter_id or symbol}")
            return None

        result = OrchestratorResult(
            parameter_id=base.parameter_id,
            symbol=base.symbol,
            name=base.name,
            value=base.value,
            ci_95=base.ci_95,
            registry_value=base.value,
            registry_source=base.source,
            source=base.source,
            tier=base.tier,
            tier_note=base.tier_note,
        )

        self._log(f"Registry: {base.parameter_id} = {base.value:.4f}")

        # -----------------------------------------------------------
        # Step 2: Layer 1 — PCT transform (if context provided)
        # -----------------------------------------------------------
        target_psi = ctx.get("target_psi")
        anchor_psi = ctx.get("anchor_psi")
        anchor_context = ctx.get("anchor_context", "literature")

        if target_psi and anchor_psi:
            steps.append("Layer 1: PCT transform")
            self._log("Step 2: Applying PCT transform")

            try:
                from pct import transform_from_contexts
                pct_result = transform_from_contexts(
                    theta_A=base.value,
                    anchor_psi=anchor_psi,
                    target_psi=target_psi,
                    anchor_context=anchor_context,
                    target_context=ctx.get("target_context", "target"),
                    parameter_id=base.parameter_id,
                    parameter_symbol=base.symbol,
                )

                result.value = pct_result.theta_B
                result.pct_applied = True
                result.pct_product_M = pct_result.product_M
                result.pct_anchor_context = pct_result.anchor_context
                result.pct_target_context = pct_result.target_context
                result.pct_deltas = [
                    {
                        "dimension": d.dimension,
                        "delta": round(d.delta, 4),
                        "multiplier": round(d.multiplier, 4),
                        "anchor": d.anchor_label,
                        "target": d.target_label,
                    }
                    for d in pct_result.psi_deltas
                ]

                # Adjust CI proportionally
                ratio = pct_result.product_M
                mid = result.value
                half_width = (base.ci_95[1] - base.ci_95[0]) / 2.0 * abs(ratio)
                result.ci_95 = (mid - half_width, mid + half_width)

                result.tier = 2
                result.tier_note = f"PCT-transformed (M={pct_result.product_M:.4f})"
                self._log(f"PCT: {base.value:.4f} -> {result.value:.4f} (M={pct_result.product_M:.4f})")

            except ImportError:
                self._log("PCT module not available")
                result.tier_note += " (PCT unavailable)"
            except Exception as e:
                self._log(f"PCT error: {e}")
                result.tier_note += f" (PCT error: {e})"

        elif target_psi and not anchor_psi:
            # Auto-anchor discovery: search measurement context DB
            steps.append("Layer 1: Auto-anchor discovery")
            self._log("Step 2: Searching measurement context DB for best anchor")

            anchor_info = find_best_anchor(result.parameter_id, target_psi)

            if anchor_info:
                auto_anchor_psi = anchor_info["anchor_psi"]
                auto_anchor_context = anchor_info.get("anchor_context", "auto-discovered")
                self._log(f"Auto-anchor found: {auto_anchor_context} with {auto_anchor_psi}")

                steps.append("Layer 1: PCT transform (auto-anchor)")

                try:
                    from pct import transform_from_contexts
                    pct_result = transform_from_contexts(
                        theta_A=base.value,
                        anchor_psi=auto_anchor_psi,
                        target_psi=target_psi,
                        anchor_context=auto_anchor_context,
                        target_context=ctx.get("target_context", "target"),
                        parameter_id=base.parameter_id,
                        parameter_symbol=base.symbol,
                    )

                    result.value = pct_result.theta_B
                    result.pct_applied = True
                    result.pct_product_M = pct_result.product_M
                    result.pct_anchor_context = pct_result.anchor_context
                    result.pct_target_context = pct_result.target_context
                    result.pct_deltas = [
                        {
                            "dimension": d.dimension,
                            "delta": round(d.delta, 4),
                            "multiplier": round(d.multiplier, 4),
                            "anchor": d.anchor_label,
                            "target": d.target_label,
                        }
                        for d in pct_result.psi_deltas
                    ]

                    ratio = pct_result.product_M
                    mid = result.value
                    half_width = (base.ci_95[1] - base.ci_95[0]) / 2.0 * abs(ratio)
                    result.ci_95 = (mid - half_width, mid + half_width)

                    result.tier = 2
                    result.tier_note = f"PCT-transformed via auto-anchor (M={pct_result.product_M:.4f})"
                    self._log(f"PCT (auto): {base.value:.4f} -> {result.value:.4f}")

                except ImportError:
                    self._log("PCT module not available")
                    result.tier_note += " (PCT unavailable)"
                except Exception as e:
                    self._log(f"PCT error: {e}")
                    result.tier_note += f" (PCT error: {e})"
            else:
                steps.append("Layer 1: PCT skipped (no anchor found)")
                result.tier_note += " (no anchor in measurement context DB; provide anchor_psi)"
                self._log("No auto-anchor found for parameter")

        # -----------------------------------------------------------
        # Step 3: Layer 1 — LLMMC calibration (if requested)
        # -----------------------------------------------------------
        if calibrate and result.pct_applied:
            steps.append("Layer 1: LLMMC calibration")
            self._log("Step 3: Applying LLMMC calibration")

            try:
                cal = self._get_calibrator()
                from pct import PCTResult

                mock_pct = PCTResult(
                    theta_A=result.registry_value,
                    theta_B=result.value,
                    product_M=result.pct_product_M,
                    psi_deltas=[],
                    anchor_context=result.pct_anchor_context,
                    target_context=result.pct_target_context,
                    parameter_id=result.parameter_id,
                    parameter_symbol=result.symbol,
                )

                cal_result = cal.calibrate_with_pct(mock_pct, eu_pct=0.10)
                result.value = cal_result.theta_final
                result.ci_95 = cal_result.ci_95
                result.llmmc_applied = True
                result.llmmc_shrinkage = cal_result.shrinkage_factor
                result.tier_note = cal_result.tier_note
                self._log(f"LLMMC: -> {result.value:.4f} (shrinkage={cal_result.shrinkage_factor:.4f})")

            except ImportError:
                self._log("LLMMC module not available")
                result.tier_note += " (LLMMC unavailable)"
            except Exception as e:
                self._log(f"LLMMC error: {e}")
                result.tier_note += f" (LLMMC error: {e})"

        elif calibrate and not result.pct_applied:
            steps.append("Layer 1: LLMMC skipped (no PCT applied)")
            self._log("LLMMC skipped: PCT must be applied first")

        # -----------------------------------------------------------
        # Finalize
        # -----------------------------------------------------------
        result.query_type = query_type.value
        result.pipeline_steps = steps

        if result.llmmc_applied:
            result.layers_used = LayerUsed.LAYER2_PLUS_PCT_LLMMC.value
        elif result.pct_applied:
            result.layers_used = LayerUsed.LAYER2_PLUS_PCT.value
        else:
            result.layers_used = LayerUsed.LAYER2_ONLY.value

        result.elapsed_ms = (time.monotonic() - t_start) * 1000
        return result

    # -------------------------------------------------------------------
    # Batch query
    # -------------------------------------------------------------------

    def batch_query(
        self,
        parameter_ids: List[str],
        context: Dict = None,
        calibrate: bool = False,
    ) -> List[Optional[OrchestratorResult]]:
        """
        Query multiple parameters with the same context.

        Args:
            parameter_ids: List of parameter IDs
            context: Shared context (applied to all)
            calibrate: Whether to calibrate all

        Returns:
            List of results (None for not-found)
        """
        return [
            self.query(parameter_id=pid, context=context, calibrate=calibrate)
            for pid in parameter_ids
        ]

    # -------------------------------------------------------------------
    # Health check
    # -------------------------------------------------------------------

    def health_check(self) -> HealthCheckResult:
        """Run pipeline health check using the smoke test."""
        t_start = time.monotonic()
        result = HealthCheckResult()

        # Stage 1: Registry
        try:
            from parameter_api import _find_all_parameters
            params = _find_all_parameters()
            n = len(params)
            result.stages["registry"] = n > 0
            result.details["registry"] = f"{n} parameters loaded"
        except Exception as e:
            result.stages["registry"] = False
            result.details["registry"] = str(e)
            result.overall = False

        # Stage 2: Symbol resolution
        try:
            from parameter_api import _find_parameter
            p = _find_parameter(symbol="lambda_R")
            result.stages["symbols"] = p is not None
            result.details["symbols"] = f"Resolved to {p['id']}" if p else "FAILED"
        except Exception as e:
            result.stages["symbols"] = False
            result.details["symbols"] = str(e)
            result.overall = False

        # Stage 3: PCT
        try:
            from pct import demo_benabou
            r = demo_benabou()
            ok = 1.5 < r.theta_B < 3.0
            result.stages["pct"] = ok
            result.details["pct"] = f"theta_B={r.theta_B:.3f}, M={r.product_M:.3f}"
        except Exception as e:
            result.stages["pct"] = False
            result.details["pct"] = str(e)
            result.overall = False

        # Stage 4: LLMMC
        try:
            cal = self._get_calibrator()
            cal_result = cal.calibrate(theta_llm=0.60, eu_llm=0.10)
            ok = cal_result.theta_final > 0
            result.stages["llmmc"] = ok
            result.details["llmmc"] = f"theta_final={cal_result.theta_final:.3f}"
        except Exception as e:
            result.stages["llmmc"] = False
            result.details["llmmc"] = str(e)
            result.overall = False

        # Stage 5: Full pipeline
        try:
            r = self.query(
                parameter_id="PAR-BEH-016",
                context={
                    "target_psi": {"psi_S": "competence_signaling"},
                    "anchor_psi": {"psi_S": "welfare_stigma"},
                    "anchor_context": "welfare",
                },
                calibrate=True,
            )
            ok = r is not None and r.pct_applied and r.llmmc_applied and r.value > 0
            result.stages["full_pipeline"] = ok
            result.details["full_pipeline"] = r.summary() if r else "FAILED"
        except Exception as e:
            result.stages["full_pipeline"] = False
            result.details["full_pipeline"] = str(e)
            result.overall = False

        # Stage 6: Data files
        data_files = {
            "parameter-registry.yaml": REPO_ROOT / "data" / "parameter-registry.yaml",
            "pct-multiplier-tables.yaml": REPO_ROOT / "data" / "pct-multiplier-tables.yaml",
            "pct-psi-scales.yaml": REPO_ROOT / "data" / "pct-psi-scales.yaml",
            "pct-measurement-contexts.yaml": REPO_ROOT / "data" / "pct-measurement-contexts.yaml",
        }
        all_exist = True
        missing = []
        for name, path in data_files.items():
            if not path.exists():
                all_exist = False
                missing.append(name)
        result.stages["data_files"] = all_exist
        result.details["data_files"] = "All present" if all_exist else f"Missing: {', '.join(missing)}"
        if not all_exist:
            result.overall = False

        result.elapsed_ms = (time.monotonic() - t_start) * 1000
        return result

    # -------------------------------------------------------------------
    # Calibrator management
    # -------------------------------------------------------------------

    def _get_calibrator(self):
        """Get or create a fitted LLMMC calibrator."""
        if self._calibrator_fitted:
            return self._calibrator

        from llmmc_calibration import LLMMCCalibrator, create_example_calibration_set

        self._calibrator = LLMMCCalibrator(min_anchors=5)
        self._calibrator.add_anchors_from_dict(create_example_calibration_set())
        self._calibrator.add_pct_anchors()
        self._calibrator.fit()
        self._calibrator_fitted = True

        return self._calibrator

    # -------------------------------------------------------------------
    # Natural language query resolution
    # -------------------------------------------------------------------

    def resolve_nl_query(self, query: str) -> List[Dict]:
        """
        Resolve a natural language query to matching parameters.

        Uses a multi-strategy approach:
          1. Direct ID/symbol match (e.g. "PAR-BEH-001" or "lambda_R")
          2. Keyword index (common behavioral economics terms)
          3. Fuzzy name matching (words from query against parameter names)

        Args:
            query: Natural language query string

        Returns:
            List of match dicts: [{parameter_id, symbol, name, score, match_reason}]
            Sorted by relevance score (descending).
        """
        from parameter_api import _find_all_parameters, _find_parameter

        query_lower = query.lower().strip()
        words = set(query_lower.replace(",", " ").replace("?", " ").replace("!", " ").split())
        matches = []
        seen_ids = set()

        # Strategy 1: Direct ID match
        for w in words:
            w_upper = w.upper()
            if w_upper.startswith("PAR-"):
                p = _find_parameter(parameter_id=w_upper)
                if p and p["id"] not in seen_ids:
                    matches.append({
                        "parameter_id": p["id"],
                        "symbol": p.get("symbol", ""),
                        "name": p.get("name", ""),
                        "score": 1.0,
                        "match_reason": f"Direct ID match: {w_upper}",
                    })
                    seen_ids.add(p["id"])

        # Strategy 2: Direct symbol match
        for w in words:
            p = _find_parameter(symbol=w)
            if p and p["id"] not in seen_ids:
                matches.append({
                    "parameter_id": p["id"],
                    "symbol": p.get("symbol", ""),
                    "name": p.get("name", ""),
                    "score": 0.95,
                    "match_reason": f"Symbol match: {w}",
                })
                seen_ids.add(p["id"])

        # Strategy 3: Keyword index
        keyword_hits = self._match_keywords(words)
        for pid, reason, score in keyword_hits:
            if pid not in seen_ids:
                p = _find_parameter(parameter_id=pid)
                if p:
                    matches.append({
                        "parameter_id": pid,
                        "symbol": p.get("symbol", ""),
                        "name": p.get("name", ""),
                        "score": score,
                        "match_reason": reason,
                    })
                    seen_ids.add(pid)

        # Strategy 4: Fuzzy name matching
        all_params = _find_all_parameters()
        for p in all_params:
            pid = p.get("id", "")
            if pid in seen_ids:
                continue
            name_lower = p.get("name", "").lower()
            name_words = set(name_lower.replace("-", " ").replace("_", " ").split())

            # Count overlapping meaningful words (skip short/common words)
            skip = {"the", "a", "an", "of", "in", "on", "at", "to", "for", "is",
                    "and", "or", "by", "from", "with", "how", "what", "when",
                    "where", "who", "why", "does", "do", "can", "much", "my", "i"}
            meaningful_query = words - skip
            overlap = meaningful_query & name_words
            if len(overlap) >= 1 and len(meaningful_query) > 0:
                score = len(overlap) / max(len(meaningful_query), len(name_words)) * 0.8
                matches.append({
                    "parameter_id": pid,
                    "symbol": p.get("symbol", ""),
                    "name": p.get("name", ""),
                    "score": round(score, 3),
                    "match_reason": f"Name match: {', '.join(sorted(overlap))}",
                })
                seen_ids.add(pid)

        matches.sort(key=lambda m: m["score"], reverse=True)
        return matches

    @staticmethod
    def _match_keywords(words: set) -> List[tuple]:
        """
        Match query words against a keyword index.

        Returns list of (parameter_id, reason, score) tuples.
        """
        # Keyword -> (parameter_id, score)
        # Keywords are grouped: if ANY word in a group matches, it triggers
        _KEYWORD_MAP = {
            # Loss aversion
            ("loss", "aversion", "verlustaversion", "losses"): ("PAR-BEH-001", 0.9),
            # Crowding out
            ("crowding", "crowd", "intrinsic", "extrinsic"): ("PAR-BEH-002", 0.85),
            # Present bias / discounting
            ("present", "bias", "hyperbolic", "discounting", "impatience",
             "patience", "geduld", "zeitpraeferenz"): ("PAR-BEH-003", 0.85),
            # Inequity aversion (alpha)
            ("inequity", "inequality", "fairness", "unfairness",
             "disadvantageous", "ungleichheit"): ("PAR-BEH-012", 0.85),
            # Inequity aversion (beta)
            ("advantageous", "guilt", "schuld"): ("PAR-BEH-013", 0.8),
            # Identity
            ("identity", "identitaet", "self", "selbst",
             "prescription"): ("PAR-BEH-009", 0.8),
            # Image concern
            ("image", "reputation", "signaling", "visibility",
             "ruf"): ("PAR-BEH-014", 0.85),
            # Social exclusion
            ("exclusion", "ostracism", "ausschluss",
             "belonging"): ("PAR-BEH-011", 0.85),
            # Rejection sensitivity
            ("rejection", "stigma", "ablehnung", "welfare",
             "sozialhilfe"): ("PAR-BEH-016", 0.85),
            # Network / segregation
            ("network", "segregation", "homophily",
             "netzwerk"): ("PAR-BEH-015", 0.8),
            # Trust
            ("trust", "vertrauen", "institutional"): ("PAR-CTX-002", 0.85),
            # Taboo / finance
            ("taboo", "tabu", "finance", "money", "geld",
             "finanzen"): ("PAR-CTX-001", 0.8),
            # Privacy
            ("privacy", "datenschutz", "private"): ("PAR-CTX-003", 0.8),
            # Addiction
            ("addiction", "sucht", "smoking", "rauchen"): ("PAR-BEH-004", 0.85),
            # Time / shadow price
            ("shadow", "time", "zeit", "opportunity"): ("PAR-TA-001", 0.8),
            # Complementarity
            ("complementarity", "komplementaritaet", "interaction",
             "synergy"): ("PAR-COMP-001", 0.8),
        }

        results = []
        for keyword_group, (pid, score) in _KEYWORD_MAP.items():
            overlap = words & set(keyword_group)
            if overlap:
                bonus = min(len(overlap) * 0.02, 0.08)  # slight bonus for multiple matches
                results.append((
                    pid,
                    f"Keyword match: {', '.join(sorted(overlap))}",
                    round(score + bonus, 3),
                ))

        return results

    # -------------------------------------------------------------------
    # Convenience: List available parameters
    # -------------------------------------------------------------------

    def list_parameters(self, domain: str = None) -> List[Dict]:
        """List all available parameters, optionally filtered by domain."""
        from parameter_api import list_parameters
        return list_parameters(domain)

    # -------------------------------------------------------------------
    # Convenience: explain query
    # -------------------------------------------------------------------

    def explain(
        self,
        parameter_id: str = None,
        symbol: str = None,
        context: Dict = None,
        calibrate: bool = False,
    ) -> str:
        """
        Generate a human-readable explanation of a parameter query.

        This is what Layer 3 (LLM) should use: the orchestrator computes
        the numbers, then Layer 3 translates them into natural language.
        """
        result = self.query(parameter_id, symbol, context, calibrate)
        if result is None:
            return f"Parameter {parameter_id or symbol} not found in registry."

        lines = []
        lines.append(f"Parameter: {result.name} ({result.symbol})")
        lines.append(f"  ID: {result.parameter_id}")
        lines.append(f"  Value: {result.value:.4f}")
        lines.append(f"  95% CI: [{result.ci_95[0]:.4f}, {result.ci_95[1]:.4f}]")
        lines.append(f"  Tier: {result.tier} ({result.tier_note})")
        lines.append("")
        lines.append("Pipeline:")
        for i, step in enumerate(result.pipeline_steps, 1):
            lines.append(f"  {i}. {step}")

        if result.pct_applied:
            lines.append("")
            lines.append("PCT Transform:")
            lines.append(f"  Registry value: {result.registry_value:.4f}")
            lines.append(f"  Product M: {result.pct_product_M:.4f}")
            lines.append(f"  Transformed: {result.registry_value:.4f} x {result.pct_product_M:.4f} = {result.registry_value * result.pct_product_M:.4f}")
            lines.append(f"  Context: {result.pct_anchor_context} -> {result.pct_target_context}")
            if result.pct_deltas:
                lines.append("  Dimensions:")
                for d in result.pct_deltas:
                    lines.append(f"    {d['dimension']}: {d['anchor']} -> {d['target']} (M={d['multiplier']:.3f})")

        if result.llmmc_applied:
            lines.append("")
            lines.append("LLMMC Calibration:")
            lines.append(f"  Shrinkage factor: {result.llmmc_shrinkage:.4f}")
            lines.append(f"  Final value: {result.value:.4f}")

        lines.append("")
        lines.append(f"Layers used: {result.layers_used}")
        lines.append(f"Elapsed: {result.elapsed_ms:.1f}ms")

        return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="EBF Three-Layer Orchestrator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Simple registry lookup
  python orchestrator.py --id PAR-BEH-001

  # PCT transform
  python orchestrator.py --id PAR-BEH-016 \\
      --target-psi psi_S=competence_signaling,psi_I=professional_hierarchy \\
      --anchor-psi psi_S=welfare_stigma,psi_I=bureaucratic_application \\
      --anchor-context welfare

  # Full pipeline (Registry -> PCT -> LLMMC)
  python orchestrator.py --id PAR-BEH-016 \\
      --target-psi psi_S=competence_signaling \\
      --anchor-psi psi_S=welfare_stigma \\
      --anchor-context welfare --calibrate

  # Batch query
  python orchestrator.py --batch PAR-BEH-001,PAR-BEH-016

  # Health check
  python orchestrator.py --health

  # Human-readable explanation
  python orchestrator.py --id PAR-BEH-016 \\
      --target-psi psi_S=competence_signaling \\
      --anchor-psi psi_S=welfare_stigma \\
      --anchor-context welfare --explain

  # Formatted markdown output (Layer 3 translation)
  python orchestrator.py --id PAR-BEH-001 --translate
  python orchestrator.py --id PAR-BEH-016 \\
      --target-psi psi_S=competence_signaling \\
      --calibrate --translate

  # Auto-anchor discovery (only target_psi needed)
  python orchestrator.py --id PAR-BEH-016 \\
      --target-psi psi_S=competence_signaling

  # Natural language query
  python orchestrator.py --query "loss aversion"
  python orchestrator.py --query "How strong is present bias?"
  python orchestrator.py --query "rejection stigma welfare" --calibrate

Pipeline: Layer 2 (Registry) -> Layer 1 (PCT) -> Layer 1 (LLMMC)
Principle: Compute, Don't Hallucinate
        """
    )

    parser.add_argument("--id", type=str, help="Parameter ID (e.g. PAR-BEH-001)")
    parser.add_argument("--symbol", type=str, help="Parameter symbol (e.g. lambda_R)")
    parser.add_argument("--query", type=str,
                        help="Natural language query (e.g. 'loss aversion at work')")
    parser.add_argument("--domain", type=str, help="Domain filter (e.g. finance)")
    parser.add_argument("--target-psi", type=str,
                        help="Target Psi: psi_S=label,psi_I=label")
    parser.add_argument("--anchor-psi", type=str,
                        help="Anchor Psi: psi_S=label,psi_I=label")
    parser.add_argument("--anchor-context", type=str,
                        help="Anchor context name (e.g. welfare)")
    parser.add_argument("--calibrate", action="store_true",
                        help="Apply LLMMC calibration")
    parser.add_argument("--batch", type=str,
                        help="Comma-separated parameter IDs")
    parser.add_argument("--list", action="store_true",
                        help="List available parameters")
    parser.add_argument("--health", action="store_true",
                        help="Run pipeline health check")
    parser.add_argument("--explain", action="store_true",
                        help="Human-readable explanation")
    parser.add_argument("--translate", action="store_true",
                        help="Formatted markdown output via Layer 3 translation templates")
    parser.add_argument("--json", action="store_true",
                        help="JSON output only")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Verbose logging")

    args = parser.parse_args()
    orch = Orchestrator(verbose=args.verbose)

    # Health check
    if args.health:
        result = orch.health_check()
        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        elif args.translate:
            from translation_templates import render_health
            print(render_health(result))
        else:
            print()
            print("EBF Three-Layer Pipeline Health Check")
            print("=" * 55)
            for stage, ok in result.stages.items():
                status = "PASS" if ok else "FAIL"
                detail = result.details.get(stage, "")
                print(f"  {status:4s}  {stage:25s} {detail}")
            print(f"\n  {'HEALTHY' if result.overall else 'UNHEALTHY'} ({result.elapsed_ms:.0f}ms)")
            print()
        sys.exit(0 if result.overall else 1)

    # List parameters
    if args.list:
        params = orch.list_parameters(args.domain)
        if args.json:
            print(json.dumps(params, indent=2))
        else:
            print(f"\nAvailable Parameters ({len(params)}):")
            print(f"{'ID':20s} {'Symbol':15s} {'Name':40s} {'Domains'}")
            print("-" * 95)
            for p in params:
                print(f"{p['id']:20s} {p['symbol']:15s} {p['name']:40s} {', '.join(p['domains'])}")
            print()
        return

    # Batch query
    if args.batch:
        ids = [x.strip() for x in args.batch.split(",")]
        ctx = _parse_context(args)
        results = orch.batch_query(ids, context=ctx, calibrate=args.calibrate)
        if args.json:
            output = [r.to_dict() if r else None for r in results]
            print(json.dumps(output, indent=2))
        elif args.translate:
            from translation_templates import translate_batch
            found = [r for r in results if r is not None]
            not_found = [i for i, r in zip(ids, results) if r is None]
            print(translate_batch(found, not_found=not_found if not_found else None))
        else:
            print()
            print("Batch Query Results")
            print("=" * 80)
            for r in results:
                if r:
                    print(f"  {r.summary()}")
                else:
                    print("  [not found]")
            print()
        return

    # Natural language query
    if args.query:
        matches = orch.resolve_nl_query(args.query)
        if not matches:
            print(f"\nNo parameters found matching: \"{args.query}\"")
            print("Try: --list to see all available parameters")
            sys.exit(1)

        ctx = _parse_context(args)

        if args.json:
            if len(matches) == 1 or ctx:
                # Single best match → full query
                best = matches[0]
                result = orch.query(
                    parameter_id=best["parameter_id"],
                    context=ctx,
                    calibrate=args.calibrate,
                )
                if result:
                    output = result.to_dict()
                    output["nl_match"] = best
                    print(json.dumps(output, indent=2))
                else:
                    print(json.dumps({"error": "Parameter not found", "match": best}, indent=2))
            else:
                print(json.dumps({"matches": matches}, indent=2))
            return

        # Print matches
        print()
        print(f"  Query: \"{args.query}\"")
        print(f"  Matches: {len(matches)}")
        print()

        if len(matches) == 1 or ctx or args.calibrate:
            # Auto-select best match and run full pipeline
            best = matches[0]
            print(f"  Best match: {best['parameter_id']} ({best['symbol']})")
            print(f"  Reason:     {best['match_reason']}")
            print()

            result = orch.query(
                parameter_id=best["parameter_id"],
                context=ctx,
                calibrate=args.calibrate,
            )
            if result:
                if args.explain:
                    explanation = orch.explain(
                        parameter_id=best["parameter_id"],
                        context=ctx,
                        calibrate=args.calibrate,
                    )
                    print(explanation)
                elif args.translate:
                    from translation_templates import translate
                    print(translate(result))
                else:
                    _print_result(result)
        else:
            # Multiple matches — show ranked list
            print(f"  {'#':3s} {'Score':6s} {'ID':20s} {'Symbol':15s} {'Name':35s} {'Reason'}")
            print("  " + "-" * 100)
            for i, m in enumerate(matches[:10], 1):
                print(f"  {i:3d} {m['score']:5.2f}  {m['parameter_id']:20s} "
                      f"{m['symbol']:15s} {m['name'][:35]:35s} {m['match_reason']}")
            if len(matches) > 10:
                print(f"  ... and {len(matches) - 10} more")
            print()
            print("  Tip: Use --query \"...\" --id <ID> to select a specific match")
            print("       or add --target-psi/--calibrate to auto-select the best match")
            print()
        return

    # Single query
    if not args.id and not args.symbol:
        parser.print_help()
        return

    ctx = _parse_context(args)

    if args.explain:
        if args.translate:
            # Use Layer 3 template for explain mode
            result = orch.query(
                parameter_id=args.id,
                symbol=args.symbol,
                context=ctx,
                calibrate=args.calibrate,
            )
            if result:
                from translation_templates import render_explain
                print(render_explain(result))
            else:
                print(f"Parameter not found: {args.id or args.symbol}")
                sys.exit(1)
        else:
            explanation = orch.explain(
                parameter_id=args.id,
                symbol=args.symbol,
                context=ctx,
                calibrate=args.calibrate,
            )
            print()
            print(explanation)
        return

    result = orch.query(
        parameter_id=args.id,
        symbol=args.symbol,
        context=ctx,
        calibrate=args.calibrate,
    )

    if result is None:
        print(f"Parameter not found: {args.id or args.symbol}")
        sys.exit(1)

    if args.json:
        print(json.dumps(result.to_dict(), indent=2))
    elif args.translate:
        from translation_templates import translate
        print(translate(result))
    else:
        _print_result(result)


def _parse_context(args) -> Optional[Dict]:
    """Parse CLI context arguments into a context dict."""
    ctx = {}

    if args.target_psi:
        ctx["target_psi"] = {}
        for pair in args.target_psi.split(","):
            k, v = pair.split("=", 1)
            ctx["target_psi"][k.strip()] = v.strip()

    if args.anchor_psi:
        ctx["anchor_psi"] = {}
        for pair in args.anchor_psi.split(","):
            k, v = pair.split("=", 1)
            ctx["anchor_psi"][k.strip()] = v.strip()

    if args.anchor_context:
        ctx["anchor_context"] = args.anchor_context

    if args.domain:
        ctx["domain"] = args.domain

    return ctx if ctx else None


def _print_result(result: OrchestratorResult):
    """Pretty-print an orchestrator result."""
    print()
    print("=" * 65)
    print("  EBF ORCHESTRATOR RESULT")
    print("=" * 65)
    print()
    print(f"  Parameter:  {result.parameter_id} ({result.symbol})")
    print(f"  Name:       {result.name}")
    print(f"  Value:      {result.value:.4f}")
    print(f"  95% CI:     [{result.ci_95[0]:.4f}, {result.ci_95[1]:.4f}]")
    print(f"  Tier:       {result.tier} ({result.tier_note})")
    print()
    print("  Pipeline:")
    for i, step in enumerate(result.pipeline_steps, 1):
        print(f"    {i}. {step}")

    if result.pct_applied:
        print()
        print("  PCT Transform:")
        print(f"    Registry:   {result.registry_value:.4f}")
        print(f"    Product M:  {result.pct_product_M:.4f}")
        print(f"    Anchor:     {result.pct_anchor_context}")
        print(f"    Target:     {result.pct_target_context}")
        if result.pct_deltas:
            for d in result.pct_deltas:
                print(f"    {d['dimension']:8s} {d['anchor']:30s} -> {d['target']:30s} M={d['multiplier']:.3f}")

    if result.llmmc_applied:
        print()
        print("  LLMMC Calibration:")
        print(f"    Shrinkage:  {result.llmmc_shrinkage:.4f}")

    print()
    print(f"  Layers:  {result.layers_used}")
    print(f"  Elapsed: {result.elapsed_ms:.1f}ms")
    print()


if __name__ == "__main__":
    main()
