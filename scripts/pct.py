#!/usr/bin/env python3
"""
Parameter Context Transformation (PCT) Module
==============================================

Implements the full EBF equation:

    theta_B = theta_A * prod_i M(delta_psi_i) * prod_j N(delta_10C_j)

where:
    theta_A     = Parameter value in anchor context (from paper measurement_context)
    theta_B     = Parameter value in target context (prediction)
    delta_psi_i = Psi_i(target) - Psi_i(anchor)  [context difference]
    M(.)        = Psi-multiplier (from pct-multiplier-tables.yaml)

Theory:  docs/workflows/level5-paper-integration-workflow.md (Lines 309-891)
Data:    data/pct-multiplier-tables.yaml (reference ranges)
Schema:  data/paper-references/PAP-*.yaml (measurement_contexts)

Usage:
    python pct.py --demo
    python pct.py --theta 2.5 --multipliers 0.85,0.95,1.10
    python pct.py --theta 2.5 --deltas psi_S=-0.3,psi_I=-0.1,psi_C=0.2

Author: EBF Framework
Date: 2026-02-15
Protocol: PCT-TRANSFORM-1
Layer: 1 (Formal Computation)
"""

import json
import argparse
import math
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
from pathlib import Path


# ---------------------------------------------------------------------------
# Data path
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent
MULTIPLIER_TABLES_PATH = REPO_ROOT / "data" / "pct-multiplier-tables.yaml"
PSI_SCALES_PATH = REPO_ROOT / "data" / "pct-psi-scales.yaml"
TEN_C_TABLES_PATH = REPO_ROOT / "data" / "pct-10c-multiplier-tables.yaml"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class AnchorContext:
    """Anchor context from a paper measurement."""
    theta: float                          # theta_A (parameter value)
    psi: Dict[str, str]                   # Psi-conditions, e.g. {"psi_S": "welfare_stigma"}
    source_paper: str = ""                # BibTeX key
    context_name: str = ""                # e.g. "welfare_takeup"
    study_type: str = ""                  # field_data / lab_experiment / theoretical
    countries: List[str] = field(default_factory=list)


@dataclass
class PsiDelta:
    """A single Psi-dimension difference."""
    dimension: str          # e.g. "psi_S"
    delta: float            # signed difference (target - anchor)
    multiplier: float       # M(delta_psi)
    anchor_label: str = ""  # e.g. "welfare_stigma"
    target_label: str = ""  # e.g. "competence_signaling"


@dataclass
class TenCDelta:
    """A single 10C dimension difference."""
    dimension: str          # e.g. "WHO", "WHAT", "HOW"
    delta: float            # signed difference (target - anchor)
    multiplier: float       # N(delta_10C)
    anchor_value: float = 0.0
    target_value: float = 0.0


@dataclass
class PCTResult:
    """Result of a PCT transformation."""
    theta_A: float                     # Anchor value
    theta_B: float                     # Transformed value
    product_M: float                   # product of all Psi-multipliers
    psi_deltas: List[PsiDelta]         # per-dimension details
    anchor_context: str = ""           # anchor context name
    target_context: str = ""           # target context name
    parameter_id: str = ""             # e.g. "PAR-BEH-016"
    parameter_symbol: str = ""         # e.g. "lambda_R"
    # 10C multipliers (full equation: theta_B = theta_A * prod_M * prod_N)
    product_N: float = 1.0             # product of 10C multipliers
    ten_c_deltas: List[TenCDelta] = field(default_factory=list)

    def to_dict(self) -> Dict:
        """Export to JSON-serializable dict."""
        d = {
            "theta_A": round(self.theta_A, 4),
            "theta_B": round(self.theta_B, 4),
            "product_M": round(self.product_M, 4),
            "psi_deltas": [
                {
                    "dimension": pd.dimension,
                    "delta": round(pd.delta, 4),
                    "multiplier": round(pd.multiplier, 4),
                    "anchor_label": pd.anchor_label,
                    "target_label": pd.target_label,
                }
                for pd in self.psi_deltas
            ],
            "anchor_context": self.anchor_context,
            "target_context": self.target_context,
            "parameter_id": self.parameter_id,
            "parameter_symbol": self.parameter_symbol,
        }
        if self.ten_c_deltas:
            d["product_N"] = round(self.product_N, 4)
            d["ten_c_deltas"] = [
                {
                    "dimension": tc.dimension,
                    "delta": round(tc.delta, 4),
                    "multiplier": round(tc.multiplier, 4),
                }
                for tc in self.ten_c_deltas
            ]
        return d


# ---------------------------------------------------------------------------
# Multiplier table loading
# ---------------------------------------------------------------------------

def _load_multiplier_tables() -> Dict:
    """Load pct-multiplier-tables.yaml and return the multipliers dict."""
    try:
        import yaml
    except ImportError:
        # Fallback: return hardcoded reference table
        return _hardcoded_multiplier_table()

    if not MULTIPLIER_TABLES_PATH.exists():
        return _hardcoded_multiplier_table()

    with open(MULTIPLIER_TABLES_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return data.get("multipliers", {})


def _hardcoded_multiplier_table() -> Dict:
    """
    Fallback multiplier table from documentation (L510-522).

    Used when YAML is not available. Values are midpoints of reference ranges.
    """
    return {
        "psi_S": {
            "directions": {
                "stigma_decrease": {"default": 0.85, "range": [0.80, 0.90], "delta_sign": "negative"},
                "stigma_increase": {"default": 1.15, "range": [1.10, 1.25], "delta_sign": "positive"},
            }
        },
        "psi_I": {
            "directions": {
                "formality_decrease": {"default": 0.95, "range": [0.90, 0.98], "delta_sign": "negative"},
                "formality_increase": {"default": 1.08, "range": [1.02, 1.15], "delta_sign": "positive"},
            }
        },
        "psi_C": {
            "directions": {
                "load_increase": {"default": 1.10, "range": [1.05, 1.20], "delta_sign": "positive"},
                "load_decrease": {"default": 0.90, "range": [0.85, 0.95], "delta_sign": "negative"},
            }
        },
        "psi_K": {
            "directions": {
                "norm_shift": {"default": 1.00, "range": [0.70, 1.40], "delta_sign": "variable"},
            }
        },
        "psi_E": {
            "directions": {
                "scarcity_increase": {"default": 1.15, "range": [1.05, 1.30], "delta_sign": "negative"},
                "scarcity_decrease": {"default": 0.90, "range": [0.80, 0.95], "delta_sign": "positive"},
            }
        },
        "psi_T": {
            "directions": {
                "urgency_increase": {"default": 1.12, "range": [1.05, 1.25], "delta_sign": "positive"},
                "urgency_decrease": {"default": 0.90, "range": [0.85, 0.95], "delta_sign": "negative"},
            }
        },
        "psi_M": {
            "directions": {
                "digital_to_physical": {"default": 1.15, "range": [1.10, 1.30], "delta_sign": "positive"},
                "physical_to_digital": {"default": 0.85, "range": [0.75, 0.90], "delta_sign": "negative"},
            }
        },
        "psi_F": {
            "directions": {
                "public_to_private": {"default": 0.90, "range": [0.85, 0.95], "delta_sign": "negative"},
                "private_to_public": {"default": 1.10, "range": [1.05, 1.20], "delta_sign": "positive"},
            }
        },
    }


# Cache loaded tables
_MULTIPLIER_CACHE = None


def get_multiplier_tables() -> Dict:
    """Get multiplier tables (cached)."""
    global _MULTIPLIER_CACHE
    if _MULTIPLIER_CACHE is None:
        _MULTIPLIER_CACHE = _load_multiplier_tables()
    return _MULTIPLIER_CACHE


def get_default_multiplier(dimension: str, delta: float) -> float:
    """
    Get the default multiplier M(delta_psi) for a dimension and signed delta.

    Uses the reference ranges from pct-multiplier-tables.yaml.
    For a given delta direction, returns the default multiplier.
    For intermediate deltas, interpolates linearly between 1.0 and the default.

    Args:
        dimension: Psi dimension key, e.g. "psi_S"
        delta: Signed delta value (target - anchor), typically in [-1, +1]

    Returns:
        M(delta_psi): multiplier value
    """
    tables = get_multiplier_tables()

    if dimension not in tables:
        # Unknown dimension: identity multiplier
        return 1.0

    dim_data = tables[dimension]
    directions = dim_data.get("directions", {})

    if not directions:
        return 1.0

    # Find the matching direction based on delta sign
    if delta == 0.0:
        return 1.0

    # For each direction, check if it matches the delta sign
    best_match = None
    for _name, dir_data in directions.items():
        sign = dir_data.get("delta_sign", "variable")
        if sign == "negative" and delta < 0:
            best_match = dir_data
            break
        elif sign == "positive" and delta > 0:
            best_match = dir_data
            break
        elif sign == "variable":
            best_match = dir_data
            # Don't break — prefer a more specific match

    if best_match is None:
        return 1.0

    default_m = best_match.get("default", 1.0)
    example_delta = best_match.get("example_delta")

    # If we have an example delta, interpolate proportionally
    if example_delta and example_delta != 0:
        # Scale: at example_delta, M = default_m; at 0, M = 1.0
        # Linear interpolation: M = 1.0 + (default_m - 1.0) * (delta / example_delta)
        ratio = delta / example_delta
        # Clamp ratio to avoid extreme extrapolation
        ratio = max(-2.0, min(2.0, ratio))
        m = 1.0 + (default_m - 1.0) * ratio
    else:
        # No example delta: use default directly
        m = default_m

    # Safety bounds: multipliers should be positive and reasonable
    m = max(0.5, min(2.0, m))
    return m


# ---------------------------------------------------------------------------
# Psi-scales loading (categorical labels → numeric values)
# ---------------------------------------------------------------------------

_PSI_SCALES_CACHE = None


def _load_psi_scales() -> Dict:
    """Load pct-psi-scales.yaml and return the scales dict."""
    try:
        import yaml
    except ImportError:
        return {}

    if not PSI_SCALES_PATH.exists():
        return {}

    with open(PSI_SCALES_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return data.get("scales", {})


def get_psi_scales() -> Dict:
    """Get Psi-scales (cached)."""
    global _PSI_SCALES_CACHE
    if _PSI_SCALES_CACHE is None:
        _PSI_SCALES_CACHE = _load_psi_scales()
    return _PSI_SCALES_CACHE


def resolve_psi_value(dimension: str, label: str) -> Optional[float]:
    """
    Resolve a categorical Psi label to a numeric value.

    Args:
        dimension: Psi dimension, e.g. "psi_S" or "Ψ_S"
        label: Categorical label, e.g. "welfare_stigma"

    Returns:
        Numeric value in [0, 1], or None if not found
    """
    # Normalize dimension key: Ψ_S → psi_S
    dim_key = dimension.replace("Ψ", "psi")

    scales = get_psi_scales()
    if dim_key not in scales:
        return None

    values = scales[dim_key].get("values", {})
    return values.get(label)


def compute_psi_delta_from_labels(
    dimension: str,
    anchor_label: str,
    target_label: str,
) -> Optional[float]:
    """
    Compute delta_psi from categorical labels using pct-psi-scales.yaml.

    Args:
        dimension: Psi dimension, e.g. "psi_S"
        anchor_label: Label in anchor context, e.g. "welfare_stigma"
        target_label: Label in target context, e.g. "competence_signaling"

    Returns:
        delta = scale[target] - scale[anchor], or None if labels not found
    """
    val_a = resolve_psi_value(dimension, anchor_label)
    val_b = resolve_psi_value(dimension, target_label)

    if val_a is None or val_b is None:
        return None

    return val_b - val_a


# ---------------------------------------------------------------------------
# 10C multiplier tables loading  (N(delta_10C) = 1.0 + slope * delta)
# ---------------------------------------------------------------------------

_TEN_C_CACHE = None


def _load_10c_tables() -> Dict:
    """Load pct-10c-multiplier-tables.yaml and return the multipliers dict."""
    try:
        import yaml
    except ImportError:
        return _hardcoded_10c_table()

    if not TEN_C_TABLES_PATH.exists():
        return _hardcoded_10c_table()

    with open(TEN_C_TABLES_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return data.get("multipliers", {})


def _hardcoded_10c_table() -> Dict:
    """Fallback 10C table with reference-range slopes."""
    return {
        "WHO":       {"slope": 0.15, "range": [0.85, 1.20], "default": 1.0},
        "WHAT":      {"slope": 0.10, "range": [0.90, 1.15], "default": 1.0},
        "HOW":       {"slope": 0.20, "range": [0.80, 1.25], "default": 1.0},
        "WHEN":      {"slope": 0.10, "range": [0.90, 1.15], "default": 1.0},
        "WHERE":     {"slope": 0.08, "range": [0.92, 1.10], "default": 1.0},
        "AWARE":     {"slope": 0.12, "range": [0.88, 1.15], "default": 1.0},
        "READY":     {"slope": 0.15, "range": [0.85, 1.20], "default": 1.0},
        "STAGE":     {"slope": 0.10, "range": [0.90, 1.15], "default": 1.0},
        "HIERARCHY": {"slope": 0.08, "range": [0.92, 1.10], "default": 1.0},
    }


def get_10c_tables() -> Dict:
    """Get 10C multiplier tables (cached)."""
    global _TEN_C_CACHE
    if _TEN_C_CACHE is None:
        _TEN_C_CACHE = _load_10c_tables()
    return _TEN_C_CACHE


def get_10c_multiplier(dimension: str, delta: float) -> float:
    """
    Get the 10C multiplier N(delta_10C) for a dimension and signed delta.

    Formula: N = 1.0 + slope * delta
    Clamped to the dimension's range.

    Args:
        dimension: 10C dimension key (e.g. "WHO", "WHAT", "HOW")
        delta: Signed difference (target - anchor), typically in [-1, +1]

    Returns:
        N(delta_10C): multiplier value
    """
    tables = get_10c_tables()
    dim_key = dimension.upper()

    if dim_key not in tables:
        return 1.0

    dim_data = tables[dim_key]
    slope = dim_data.get("slope", 0.0)
    rng = dim_data.get("range", [0.5, 2.0])

    n = 1.0 + slope * delta

    # Clamp to reference range
    n = max(rng[0], min(rng[1], n))
    return n


def compute_10c_deltas(ten_c_deltas_raw: Dict[str, float]) -> List[TenCDelta]:
    """
    Compute 10C multipliers from a dict of signed deltas.

    Args:
        ten_c_deltas_raw: Dict of {dimension: delta}, e.g. {"WHO": -0.5, "WHAT": 0.3}

    Returns:
        List of TenCDelta objects with computed multipliers
    """
    result = []
    for dim, delta in ten_c_deltas_raw.items():
        n = get_10c_multiplier(dim, delta)
        result.append(TenCDelta(
            dimension=dim.upper(),
            delta=delta,
            multiplier=n,
        ))
    return result


# ---------------------------------------------------------------------------
# Context-based transformation (categorical labels → deltas → multipliers)
# ---------------------------------------------------------------------------

def transform_from_contexts(
    theta_A: float,
    anchor_psi: Dict[str, str],
    target_psi: Dict[str, str],
    anchor_context: str = "",
    target_context: str = "",
    parameter_id: str = "",
    parameter_symbol: str = "",
    ten_c_deltas: Dict[str, float] = None,
) -> PCTResult:
    """
    Transform theta_A using categorical Psi-condition labels.

    Resolves labels → numeric values → deltas → multipliers automatically.
    Optionally applies 10C multipliers as well.

    Args:
        theta_A: Parameter value in anchor context
        anchor_psi: Dict of {dimension: label} for anchor, e.g. {"psi_S": "welfare_stigma"}
        target_psi: Dict of {dimension: label} for target, e.g. {"psi_S": "competence_signaling"}
        anchor_context: Name of anchor context (metadata)
        target_context: Name of target context (metadata)
        parameter_id: EBF parameter ID
        parameter_symbol: EBF symbol
        ten_c_deltas: Optional dict of 10C deltas, e.g. {"WHO": -0.5, "WHAT": 0.3}

    Returns:
        PCTResult (dimensions without valid labels are skipped with warning)
    """
    # Collect all dimensions mentioned in either context
    all_dims = set()
    for d in anchor_psi:
        all_dims.add(d.replace("Ψ", "psi"))
    for d in target_psi:
        all_dims.add(d.replace("Ψ", "psi"))

    psi_deltas = []
    for dim in sorted(all_dims):
        # Normalize dimension keys
        anchor_key = dim.replace("psi", "Ψ") if dim.replace("psi", "Ψ") in anchor_psi else dim
        target_key = dim.replace("psi", "Ψ") if dim.replace("psi", "Ψ") in target_psi else dim

        anchor_label = anchor_psi.get(anchor_key, anchor_psi.get(dim, ""))
        target_label = target_psi.get(target_key, target_psi.get(dim, ""))

        if not anchor_label and not target_label:
            continue

        # Compute delta from labels
        delta = compute_psi_delta_from_labels(dim, anchor_label, target_label)

        if delta is not None:
            m = get_default_multiplier(dim, delta)
            psi_deltas.append(PsiDelta(
                dimension=dim,
                delta=delta,
                multiplier=m,
                anchor_label=anchor_label,
                target_label=target_label,
            ))
        elif anchor_label and target_label:
            # Labels exist but not in scales — use default multiplier
            psi_deltas.append(PsiDelta(
                dimension=dim,
                delta=0.0,
                multiplier=1.0,
                anchor_label=anchor_label + " (unmapped)",
                target_label=target_label + " (unmapped)",
            ))

    # Compute 10C multipliers if provided
    tc_deltas_list = []
    if ten_c_deltas:
        tc_deltas_list = compute_10c_deltas(ten_c_deltas)

    result = transform(theta_A, psi_deltas, tc_deltas_list)
    result.anchor_context = anchor_context
    result.target_context = target_context
    result.parameter_id = parameter_id
    result.parameter_symbol = parameter_symbol
    return result


# ---------------------------------------------------------------------------
# Core transformation
# ---------------------------------------------------------------------------

def transform(
    theta_A: float,
    psi_deltas: List[PsiDelta],
    ten_c_deltas: List[TenCDelta] = None,
) -> PCTResult:
    """
    Core PCT transformation.

    Computes: theta_B = theta_A * prod_i M(delta_psi_i) * prod_j N(delta_10C_j)

    Args:
        theta_A: Parameter value in anchor context
        psi_deltas: List of PsiDelta objects (dimension + delta + multiplier)
        ten_c_deltas: Optional list of TenCDelta objects for 10C multipliers

    Returns:
        PCTResult with theta_B and full transformation details
    """
    product_M = 1.0
    for pd in psi_deltas:
        product_M *= pd.multiplier

    product_N = 1.0
    tc_list = ten_c_deltas or []
    for tc in tc_list:
        product_N *= tc.multiplier

    theta_B = theta_A * product_M * product_N

    return PCTResult(
        theta_A=theta_A,
        theta_B=theta_B,
        product_M=product_M,
        psi_deltas=psi_deltas,
        product_N=product_N,
        ten_c_deltas=tc_list,
    )


def transform_with_deltas(
    theta_A: float,
    deltas: Dict[str, float],
    anchor_context: str = "",
    target_context: str = "",
    parameter_id: str = "",
    parameter_symbol: str = "",
    ten_c_deltas: Dict[str, float] = None,
) -> PCTResult:
    """
    Transform theta_A using named Psi-dimension deltas.

    Automatically looks up multipliers from the reference table.

    Args:
        theta_A: Parameter value in anchor context
        deltas: Dict of {dimension: delta}, e.g. {"psi_S": -0.3, "psi_I": -0.1}
        anchor_context: Name of anchor context (for metadata)
        target_context: Name of target context (for metadata)
        parameter_id: EBF parameter ID (e.g. "PAR-BEH-016")
        parameter_symbol: EBF symbol (e.g. "lambda_R")
        ten_c_deltas: Optional dict of 10C deltas, e.g. {"WHO": -0.5}

    Returns:
        PCTResult
    """
    psi_deltas = []
    for dim, delta in deltas.items():
        m = get_default_multiplier(dim, delta)
        psi_deltas.append(PsiDelta(
            dimension=dim,
            delta=delta,
            multiplier=m,
        ))

    tc_list = compute_10c_deltas(ten_c_deltas) if ten_c_deltas else []

    result = transform(theta_A, psi_deltas, tc_list)
    result.anchor_context = anchor_context
    result.target_context = target_context
    result.parameter_id = parameter_id
    result.parameter_symbol = parameter_symbol
    return result


def transform_with_multipliers(
    theta_A: float,
    multipliers: List[float],
    labels: Optional[List[str]] = None,
) -> PCTResult:
    """
    Transform theta_A using explicit multipliers (no table lookup).

    Args:
        theta_A: Parameter value in anchor context
        multipliers: List of M(delta_psi) values
        labels: Optional dimension labels

    Returns:
        PCTResult
    """
    if labels is None:
        labels = [f"M_{i+1}" for i in range(len(multipliers))]

    psi_deltas = [
        PsiDelta(dimension=label, delta=0.0, multiplier=m)
        for label, m in zip(labels, multipliers)
    ]
    return transform(theta_A, psi_deltas)


# ---------------------------------------------------------------------------
# Demo: Worked Example from Documentation
# ---------------------------------------------------------------------------

def demo_benabou() -> PCTResult:
    """
    Worked Example: lambda_R from welfare (2.5) to workplace (2.22).

    Source: docs/workflows/level5-paper-integration-workflow.md Lines 456-508
    Data:   data/paper-references/PAP-benabou2022hurts.yaml Lines 124-154

    Anchor: welfare_takeup
        theta_A = 2.5 (lambda_R)
        Psi_S = welfare_stigma (HIGH)
        Psi_I = bureaucratic_application
        Psi_K = self_reliance_norm

    Target: workplace_help
        Psi_S = competence_signaling (MODERATE)
        Psi_I = professional_hierarchy
        Psi_C = performance_evaluation (NEW factor)

    Transformation:
        delta_psi_S = -0.3 (stigma decreases)   -> M = 0.85
        delta_psi_I = -0.1 (less formal)         -> M = 0.95
        delta_psi_C = +0.2 (evaluation pressure) -> M = 1.10

        theta_B = 2.5 * 0.85 * 0.95 * 1.10 = 2.22
        Measured: 1.8 (23% deviation)
    """
    psi_deltas = [
        PsiDelta(
            dimension="psi_S",
            delta=-0.3,
            multiplier=0.85,
            anchor_label="welfare_stigma",
            target_label="competence_signaling",
        ),
        PsiDelta(
            dimension="psi_I",
            delta=-0.1,
            multiplier=0.95,
            anchor_label="bureaucratic_application",
            target_label="professional_hierarchy",
        ),
        PsiDelta(
            dimension="psi_C",
            delta=0.2,
            multiplier=1.10,
            anchor_label="(none)",
            target_label="performance_evaluation",
        ),
    ]

    result = transform(2.5, psi_deltas)
    result.anchor_context = "welfare_takeup"
    result.target_context = "workplace_help"
    result.parameter_id = "PAR-BEH-016"
    result.parameter_symbol = "lambda_R"
    return result


# ---------------------------------------------------------------------------
# Report printing
# ---------------------------------------------------------------------------

def print_pct_report(result: PCTResult) -> None:
    """Print a formatted PCT transformation report."""
    print()
    print("=" * 60)
    print("PCT TRANSFORMATION REPORT")
    print("=" * 60)

    if result.parameter_symbol:
        print(f"\n   Parameter: {result.parameter_symbol}", end="")
        if result.parameter_id:
            print(f" ({result.parameter_id})")
        else:
            print()

    if result.anchor_context:
        print(f"   Anchor:    {result.anchor_context}")
    if result.target_context:
        print(f"   Target:    {result.target_context}")

    print(f"\n   theta_A = {result.theta_A:.4f}")
    print()

    # Multiplier breakdown
    print("   Psi-Multipliers:")
    print("   " + "-" * 50)
    for pd in result.psi_deltas:
        direction = "+" if pd.delta >= 0 else ""
        label_info = ""
        if pd.anchor_label and pd.target_label:
            label_info = f"  ({pd.anchor_label} -> {pd.target_label})"
        print(f"   {pd.dimension:8s}  delta={direction}{pd.delta:.2f}  "
              f"M={pd.multiplier:.4f}{label_info}")
    print("   " + "-" * 50)
    print(f"   Product:  {result.product_M:.4f}")

    # 10C multipliers (if present)
    if result.ten_c_deltas:
        print()
        print("   10C-Multipliers:")
        print("   " + "-" * 50)
        for tc in result.ten_c_deltas:
            direction = "+" if tc.delta >= 0 else ""
            print(f"   {tc.dimension:12s}  delta={direction}{tc.delta:.2f}  "
                  f"N={tc.multiplier:.4f}")
        print("   " + "-" * 50)
        print(f"   Product N: {result.product_N:.4f}")

    # Final calculation
    if result.ten_c_deltas:
        print(f"\n   theta_B = theta_A * Product_M * Product_N")
        print(f"          = {result.theta_A:.4f} * {result.product_M:.4f} * {result.product_N:.4f}")
        print(f"          = {result.theta_B:.4f}")
    else:
        print(f"\n   theta_B = theta_A * Product_M")
        print(f"          = {result.theta_A:.4f} * {result.product_M:.4f}")
        print(f"          = {result.theta_B:.4f}")

    print()
    print("   Equation: theta_B = theta_A * prod_i M(delta_psi_i) * prod_j N(delta_10C_j)")
    print("   Source:   docs/workflows/level5-paper-integration-workflow.md")
    print("   Layer:    1 (Formal Computation)")
    print()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def demo():
    """Run the Benabou worked example demo."""
    print("\n" + "=" * 60)
    print("PCT DEMO: Benabou (2022) lambda_R Transformation")
    print("=" * 60)

    print("\n   Source Paper: PAP-benabou2022hurts")
    print("   Anchor: welfare_takeup (lambda_R = 2.5)")
    print("   Target: workplace_help")
    print()
    print("   Psi-Differences:")
    print("   Psi_S: welfare_stigma -> competence_signaling  (delta = -0.3)")
    print("   Psi_I: bureaucratic   -> professional          (delta = -0.1)")
    print("   Psi_C: (none)         -> performance_eval      (delta = +0.2)")

    result = demo_benabou()
    print_pct_report(result)

    # Compare with measured value
    measured = 1.8
    deviation = abs(result.theta_B - measured) / measured * 100
    print(f"   Comparison with measured value:")
    print(f"   PCT estimate: {result.theta_B:.2f}")
    print(f"   Measured:     {measured:.2f}")
    print(f"   Deviation:    {deviation:.0f}%")
    print(f"   -> Further Psi-factors may explain remaining gap")

    print(f"\n   JSON:")
    print(json.dumps(result.to_dict(), indent=2))

    return result


def main():
    parser = argparse.ArgumentParser(
        description="PCT: Parameter Context Transformation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Equation: theta_B = theta_A * prod_i M(delta_psi_i) * prod_j N(delta_10C_j)

The central EBF transformation: parameters are NOT constants,
they are functions of context theta = f(Psi, 10C).

Examples:
  python pct.py --demo
  python pct.py --theta 2.5 --multipliers 0.85,0.95,1.10
  python pct.py --theta 2.5 --deltas psi_S=-0.3,psi_I=-0.1,psi_C=0.2
  python pct.py --theta 2.5 --deltas psi_S=-0.3 --ten-c WHO=-0.5,READY=0.3
  python pct.py --theta 2.5 --anchor-psi psi_S=welfare_stigma,psi_I=bureaucratic_application \\
                             --target-psi psi_S=competence_signaling,psi_I=professional_hierarchy \\
                             --ten-c WHO=-0.5,WHAT=0.2

Theory:  docs/workflows/level5-paper-integration-workflow.md
Data:    data/pct-multiplier-tables.yaml, data/pct-10c-multiplier-tables.yaml
Scales:  data/pct-psi-scales.yaml
Layer:   1 (Formal Computation)
        """
    )

    parser.add_argument("--demo", action="store_true",
                        help="Run Benabou worked example demo")
    parser.add_argument("--theta", type=float,
                        help="Anchor parameter value theta_A")
    parser.add_argument("--multipliers", type=str,
                        help="Comma-separated multipliers M1,M2,...")
    parser.add_argument("--deltas", type=str,
                        help="Named deltas: psi_S=-0.3,psi_I=-0.1,psi_C=0.2")
    parser.add_argument("--anchor-psi", type=str,
                        help="Anchor labels: psi_S=welfare_stigma,psi_I=bureaucratic_application")
    parser.add_argument("--target-psi", type=str,
                        help="Target labels: psi_S=competence_signaling,psi_I=professional_hierarchy")
    parser.add_argument("--ten-c", type=str,
                        help="10C deltas: WHO=-0.5,WHAT=0.2,READY=0.3")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON only")

    args = parser.parse_args()

    # Parse 10C deltas if provided
    ten_c = None
    if args.ten_c:
        ten_c = {}
        for pair in args.ten_c.split(","):
            key, val = pair.split("=")
            ten_c[key.strip()] = float(val.strip())

    if args.demo:
        demo()
    elif args.theta is not None and args.anchor_psi and args.target_psi:
        # Context-based mode: resolve labels → deltas → multipliers
        anchor_psi = {}
        for pair in args.anchor_psi.split(","):
            key, val = pair.split("=", 1)
            anchor_psi[key.strip()] = val.strip()
        target_psi = {}
        for pair in args.target_psi.split(","):
            key, val = pair.split("=", 1)
            target_psi[key.strip()] = val.strip()
        result = transform_from_contexts(args.theta, anchor_psi, target_psi,
                                         ten_c_deltas=ten_c)
        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            print_pct_report(result)
    elif args.theta is not None and args.multipliers:
        # Explicit multipliers mode
        mults = [float(x) for x in args.multipliers.split(",")]
        result = transform_with_multipliers(args.theta, mults)
        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            print_pct_report(result)
    elif args.theta is not None and args.deltas:
        # Named deltas mode (auto-lookup from tables)
        deltas = {}
        for pair in args.deltas.split(","):
            key, val = pair.split("=")
            deltas[key.strip()] = float(val.strip())
        result = transform_with_deltas(args.theta, deltas, ten_c_deltas=ten_c)
        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            print_pct_report(result)
    elif args.theta is not None and ten_c:
        # 10C-only mode (no psi deltas, only 10C)
        tc_list = compute_10c_deltas(ten_c)
        result = transform(args.theta, [], tc_list)
        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            print_pct_report(result)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
