#!/usr/bin/env python3
"""
Validate Psi-Scale Consistency
===============================

Checks that all psi_condition labels used in measurement contexts
are defined in pct-psi-scales.yaml, and reports coverage statistics.

Can be used as:
  - CLI tool: python validate_psi_scales.py
  - Pre-commit hook: python validate_psi_scales.py --strict
  - Coverage report: python validate_psi_scales.py --report

Exit codes:
  0 = All labels mapped (or --report mode)
  1 = Unmapped labels found (--strict mode)

Layer: 2 (Parameter Store Validation)
"""

import sys
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Optional, Set, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
PSI_SCALES_PATH = REPO_ROOT / "data" / "pct-psi-scales.yaml"
MEASUREMENT_CONTEXTS_PATH = REPO_ROOT / "data" / "pct-measurement-contexts.yaml"
PARAMETER_REGISTRY_PATH = REPO_ROOT / "data" / "parameter-registry.yaml"


def load_yaml(path: Path) -> Optional[Dict]:
    """Load a YAML file."""
    try:
        import yaml
    except ImportError:
        print("ERROR: PyYAML required. Install with: pip install pyyaml")
        sys.exit(1)
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_scale_labels(scales_data: Dict) -> Dict[str, Set[str]]:
    """Extract all defined labels per dimension from psi-scales."""
    labels = {}
    for dim, dim_data in scales_data.get("scales", {}).items():
        labels[dim] = set(dim_data.get("values", {}).keys())
    return labels


def get_context_labels(contexts_data: Dict) -> Dict[str, Set[str]]:
    """Extract all labels used in measurement contexts."""
    labels = defaultdict(set)
    for triplet in contexts_data.get("triplets", []):
        for dim, label in triplet.get("psi_conditions", {}).items():
            if label:
                labels[dim].add(label)
    return dict(labels)


def get_context_params(contexts_data: Dict) -> Set[str]:
    """Get parameter IDs that have measurement contexts."""
    params = set()
    for triplet in contexts_data.get("triplets", []):
        pid = triplet.get("parameter_id")
        if pid:
            params.add(pid)
    return params


def get_registry_params(registry_data: Dict) -> Set[str]:
    """Get all parameter IDs from the registry.

    Registry structure: {behavioral_parameters: [...], contextual_parameters: [...], ...}
    Each sub-list contains dicts with 'id' field.
    """
    params = set()
    if not registry_data:
        return params
    for key, val in registry_data.items():
        if key.endswith("_parameters") and isinstance(val, list):
            for entry in val:
                pid = entry.get("id")
                if pid:
                    params.add(pid)
    return params


def validate(strict: bool = False) -> Tuple[bool, Dict]:
    """Run full validation. Returns (ok, report_data)."""
    scales_data = load_yaml(PSI_SCALES_PATH)
    contexts_data = load_yaml(MEASUREMENT_CONTEXTS_PATH)
    registry_data = load_yaml(PARAMETER_REGISTRY_PATH)

    if not scales_data:
        return False, {"error": f"Not found: {PSI_SCALES_PATH}"}
    if not contexts_data:
        return False, {"error": f"Not found: {MEASUREMENT_CONTEXTS_PATH}"}

    scale_labels = get_scale_labels(scales_data)
    context_labels = get_context_labels(contexts_data)
    context_params = get_context_params(contexts_data)
    registry_params = get_registry_params(registry_data) if registry_data else set()

    # 1. Find unmapped labels (in contexts but not in scales)
    unmapped = {}
    for dim, labels in context_labels.items():
        dim_scales = scale_labels.get(dim, set())
        missing = labels - dim_scales
        if missing:
            unmapped[dim] = sorted(missing)

    # 2. Find unused labels (in scales but not in contexts)
    unused = {}
    for dim, labels in scale_labels.items():
        dim_contexts = context_labels.get(dim, set())
        extra = labels - dim_contexts
        if extra:
            unused[dim] = sorted(extra)

    # 3. Dimension coverage
    all_dims = {"psi_S", "psi_I", "psi_C", "psi_K", "psi_E", "psi_T", "psi_M", "psi_F"}
    dims_with_scales = set(scale_labels.keys())
    dims_with_contexts = set(context_labels.keys())
    dims_missing_scales = all_dims - dims_with_scales
    dims_missing_contexts = all_dims - dims_with_contexts

    # 4. Parameter coverage
    params_with_contexts = context_params
    params_total = registry_params
    params_without_contexts = params_total - params_with_contexts
    coverage_pct = (len(params_with_contexts) / len(params_total) * 100) if params_total else 0

    # 5. Scale statistics
    scale_stats = {}
    for dim in sorted(all_dims):
        n_scale = len(scale_labels.get(dim, set()))
        n_context = len(context_labels.get(dim, set()))
        scale_stats[dim] = {"n_scale_labels": n_scale, "n_context_labels": n_context}

    report = {
        "unmapped_labels": unmapped,
        "unused_labels": unused,
        "dims_missing_scales": sorted(dims_missing_scales),
        "dims_missing_contexts": sorted(dims_missing_contexts),
        "scale_stats": scale_stats,
        "params_with_contexts": len(params_with_contexts),
        "params_total": len(params_total),
        "coverage_pct": round(coverage_pct, 1),
        "params_without_contexts": sorted(params_without_contexts)[:20],  # Show first 20
        "n_triplets": len(contexts_data.get("triplets", [])),
    }

    total_unmapped = sum(len(v) for v in unmapped.values())
    ok = total_unmapped == 0

    return ok, report


def print_report(report: Dict) -> None:
    """Print human-readable validation report."""
    if "error" in report:
        print(f"ERROR: {report['error']}")
        return

    print()
    print("=" * 65)
    print("  PSI-SCALE VALIDATION REPORT")
    print("=" * 65)

    # Dimension coverage
    print("\n  DIMENSION COVERAGE (8 Psi-Dimensions):")
    print("  " + "-" * 61)
    print(f"  {'Dimension':<12} {'Scale Labels':>14} {'Context Labels':>16} {'Status':>10}")
    print("  " + "-" * 61)
    for dim, stats in sorted(report["scale_stats"].items()):
        n_s = stats["n_scale_labels"]
        n_c = stats["n_context_labels"]
        if n_s == 0:
            status = "EMPTY"
        elif n_c == 0:
            status = "NO CTX"
        elif n_s < 5:
            status = "SPARSE"
        else:
            status = "OK"
        print(f"  {dim:<12} {n_s:>14} {n_c:>16} {status:>10}")

    if report["dims_missing_contexts"]:
        print(f"\n  Dimensions with NO measurement contexts:")
        for d in report["dims_missing_contexts"]:
            print(f"    {d}")

    # Parameter coverage
    print(f"\n  PARAMETER COVERAGE:")
    print("  " + "-" * 61)
    n_with = report["params_with_contexts"]
    n_total = report["params_total"]
    pct = report["coverage_pct"]
    n_tri = report["n_triplets"]
    print(f"  Parameters with measurement contexts:  {n_with:>4} / {n_total}")
    print(f"  Coverage:                              {pct:>5.1f}%")
    print(f"  Total triplets:                        {n_tri:>4}")

    bar_width = 40
    filled = int(pct / 100 * bar_width)
    bar = "#" * filled + "." * (bar_width - filled)
    print(f"  [{bar}] {pct:.0f}%")

    # Unmapped labels
    unmapped = report["unmapped_labels"]
    total_unmapped = sum(len(v) for v in unmapped.values())
    if unmapped:
        print(f"\n  UNMAPPED LABELS ({total_unmapped} — used in contexts but NOT in scales):")
        print("  " + "-" * 61)
        for dim, labels in sorted(unmapped.items()):
            for label in labels:
                print(f"    {dim}: {label}")
        print(f"\n  ACTION: Add these to data/pct-psi-scales.yaml")
    else:
        print(f"\n  UNMAPPED LABELS: None (all context labels are in scales)")

    # Unused labels (info only)
    unused = report["unused_labels"]
    total_unused = sum(len(v) for v in unused.values())
    if total_unused > 0:
        print(f"\n  UNUSED LABELS ({total_unused} — in scales but not used in any context):")
        print("  " + "-" * 61)
        # Just show count per dimension, not full list
        for dim, labels in sorted(unused.items()):
            print(f"    {dim}: {len(labels)} unused labels")

    # Summary
    print(f"\n  " + "=" * 61)
    if total_unmapped == 0:
        print(f"  RESULT: PASS — All labels consistent")
    else:
        print(f"  RESULT: FAIL — {total_unmapped} unmapped labels need attention")
    print(f"  " + "=" * 61)
    print()


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Validate Psi-Scale consistency between scales and measurement contexts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python validate_psi_scales.py                       # Full report
  python validate_psi_scales.py --strict              # Exit 1 if unmapped labels
  python validate_psi_scales.py --json                # JSON output
  python validate_psi_scales.py --coverage            # Parameter coverage only
  python validate_psi_scales.py --coverage --threshold 70  # Exit 1 if < 70%

Layer: 2 (Parameter Store Validation)
        """
    )

    parser.add_argument("--strict", action="store_true",
                        help="Exit with code 1 if unmapped labels found")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON")
    parser.add_argument("--coverage", action="store_true",
                        help="Show only parameter coverage statistics")
    parser.add_argument("--threshold", type=float, default=None,
                        help="Minimum coverage %% (exit 1 if below). Use with --coverage.")

    args = parser.parse_args()

    ok, report = validate()

    if args.json:
        import json
        print(json.dumps(report, indent=2, default=str))
    elif args.coverage:
        n_with = report.get("params_with_contexts", 0)
        n_total = report.get("params_total", 0)
        pct = report.get("coverage_pct", 0)
        print(f"PCT Coverage: {n_with}/{n_total} parameters ({pct}%)")
        if args.threshold is not None and pct < args.threshold:
            print(f"FAIL: {pct}% < {args.threshold}% threshold")
            sys.exit(1)
    else:
        print_report(report)

    if args.strict and not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
