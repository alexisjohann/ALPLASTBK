#!/usr/bin/env python3
"""
Auto-Extract Pipeline: Measurement Contexts + Psi-Scale Validation
===================================================================

Chains two steps in a single command:
  1. generate_measurement_contexts.py → Extract contexts from parameter-registry
  2. validate_psi_scales.py           → Check all labels are mapped in psi-scales

This script is designed for:
  - Pre-commit hooks (--strict mode: exit 1 on unmapped labels)
  - CLI usage (--dry-run, --stats, --report)
  - CI/CD pipelines (--json for machine-readable output)

Usage:
    python auto_extract_pipeline.py                   # Extract + validate
    python auto_extract_pipeline.py --dry-run         # Preview only
    python auto_extract_pipeline.py --validate-only   # Skip extraction
    python auto_extract_pipeline.py --strict          # Exit 1 on issues
    python auto_extract_pipeline.py --json            # JSON output
    python auto_extract_pipeline.py --report          # Full report

Layer: 2 (Parameter Store Validation)
"""

import sys
import argparse
from pathlib import Path
from typing import Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"

# Add scripts/ to path for imports
sys.path.insert(0, str(SCRIPTS_DIR))


def run_extraction(dry_run: bool = False) -> Tuple[bool, Dict]:
    """
    Run measurement context extraction from parameter-registry.

    Returns (ok, stats) where stats contains extraction counts.
    """
    from generate_measurement_contexts import (
        load_yaml,
        extract_all_param_contexts,
        merge_contexts,
        check_new_labels,
        save_yaml,
    )
    from datetime import date

    PARAM_REGISTRY_PATH = REPO_ROOT / "data" / "parameter-registry.yaml"
    EXISTING_CONTEXTS_PATH = REPO_ROOT / "data" / "pct-measurement-contexts.yaml"
    PSI_SCALES_PATH = REPO_ROOT / "data" / "pct-psi-scales.yaml"
    OUTPUT_PATH = REPO_ROOT / "data" / "pct-measurement-contexts.yaml"

    registry = load_yaml(PARAM_REGISTRY_PATH)
    existing_data = load_yaml(EXISTING_CONTEXTS_PATH)
    scales = load_yaml(PSI_SCALES_PATH)

    if not registry:
        return False, {"error": f"parameter-registry.yaml not found at {PARAM_REGISTRY_PATH}"}

    existing_triplets = existing_data.get("triplets", []) if existing_data else []
    new_contexts = extract_all_param_contexts(registry)

    # Check for unmapped labels
    unmapped = {}
    if scales:
        unmapped = check_new_labels(new_contexts, scales)

    merged, added = merge_contexts(existing_triplets, new_contexts)

    # Coverage stats
    existing_params = set(t.get("parameter_id") for t in existing_triplets if t.get("parameter_id"))
    merged_params = set(t.get("parameter_id") for t in merged if t.get("parameter_id"))

    total_params = 0
    for key, val in registry.items():
        if key.endswith("_parameters") and isinstance(val, list):
            total_params += len([p for p in val if p.get("id")])

    stats = {
        "existing_triplets": len(existing_triplets),
        "new_extracted": len(new_contexts),
        "added_deduplicated": added,
        "merged_total": len(merged),
        "existing_params": len(existing_params),
        "merged_params": len(merged_params),
        "total_params": total_params,
        "coverage_before": round(len(existing_params) / total_params * 100, 1) if total_params else 0,
        "coverage_after": round(len(merged_params) / total_params * 100, 1) if total_params else 0,
        "unmapped_labels": unmapped,
    }

    if not dry_run and added > 0:
        output = {
            "version": "0.2",
            "generated": str(date.today()),
            "source": "data/paper-references/PAP-*.yaml + data/parameter-registry.yaml",
            "description": "Extracted measurement_contexts triplets for PCT",
            "n_papers": len(set(t["paper_key"] for t in merged)),
            "n_triplets": len(merged),
            "n_parameters": len(merged_params),
            "triplets": merged,
        }
        save_yaml(output, OUTPUT_PATH)
        stats["written"] = True
    else:
        stats["written"] = False

    return True, stats


def run_validation(strict: bool = False) -> Tuple[bool, Dict]:
    """
    Run psi-scale validation.

    Returns (ok, report) where ok means no unmapped labels.
    """
    from validate_psi_scales import validate
    return validate(strict=strict)


def run_pipeline(
    dry_run: bool = False,
    validate_only: bool = False,
    strict: bool = False,
) -> Tuple[bool, Dict]:
    """
    Run the complete extraction + validation pipeline.

    Returns (ok, combined_report).
    """
    combined = {
        "extraction": None,
        "validation": None,
        "overall_ok": True,
    }

    # Step 1: Extraction (unless validate-only)
    if not validate_only:
        extract_ok, extract_stats = run_extraction(dry_run=dry_run)
        combined["extraction"] = extract_stats
        if not extract_ok:
            combined["overall_ok"] = False
    else:
        combined["extraction"] = {"skipped": True}

    # Step 2: Validation
    valid_ok, valid_report = run_validation(strict=strict)
    combined["validation"] = valid_report
    if not valid_ok and strict:
        combined["overall_ok"] = False

    return combined["overall_ok"], combined


def print_pipeline_report(combined: Dict) -> None:
    """Print human-readable pipeline report."""
    print()
    print("=" * 65)
    print("  AUTO-EXTRACT PIPELINE REPORT")
    print("=" * 65)

    # Extraction section
    ext = combined.get("extraction", {})
    if ext.get("skipped"):
        print("\n  EXTRACTION: Skipped (--validate-only)")
    elif ext.get("error"):
        print(f"\n  EXTRACTION: ERROR — {ext['error']}")
    else:
        print(f"\n  EXTRACTION:")
        print(f"  " + "-" * 61)
        print(f"  Existing triplets:     {ext.get('existing_triplets', 0)}")
        print(f"  New extracted:         {ext.get('new_extracted', 0)}")
        print(f"  Added (deduplicated):  {ext.get('added_deduplicated', 0)}")
        print(f"  Merged total:          {ext.get('merged_total', 0)}")

        cov_before = ext.get("coverage_before", 0)
        cov_after = ext.get("coverage_after", 0)
        print(f"\n  Coverage: {cov_before:.1f}% -> {cov_after:.1f}%")
        bar_width = 40
        bar = "#" * int(cov_after / 100 * bar_width) + "." * (bar_width - int(cov_after / 100 * bar_width))
        print(f"  [{bar}] {cov_after:.0f}%")

        if ext.get("written"):
            print(f"\n  Written to: data/pct-measurement-contexts.yaml")
        else:
            print(f"\n  No changes written (dry-run or no new contexts)")

        unmapped = ext.get("unmapped_labels", {})
        if unmapped:
            total_unmapped = sum(len(v) for v in unmapped.values())
            print(f"\n  WARNING: {total_unmapped} unmapped labels in new contexts:")
            for dim, labels in sorted(unmapped.items()):
                for label in labels:
                    print(f"    {dim}: {label}")

    # Validation section
    val = combined.get("validation", {})
    if val.get("error"):
        print(f"\n  VALIDATION: ERROR — {val['error']}")
    else:
        unmapped = val.get("unmapped_labels", {})
        total_unmapped = sum(len(v) for v in unmapped.values())
        n_with = val.get("params_with_contexts", 0)
        n_total = val.get("params_total", 0)
        pct = val.get("coverage_pct", 0)
        n_tri = val.get("n_triplets", 0)

        print(f"\n  VALIDATION:")
        print(f"  " + "-" * 61)
        print(f"  Total triplets:        {n_tri}")
        print(f"  Parameter coverage:    {n_with}/{n_total} ({pct}%)")
        print(f"  Unmapped labels:       {total_unmapped}")

        if total_unmapped == 0:
            print(f"\n  RESULT: PASS — All labels consistent")
        else:
            print(f"\n  RESULT: FAIL — {total_unmapped} unmapped labels")
            for dim, labels in sorted(unmapped.items()):
                for label in labels:
                    print(f"    {dim}: {label}")

    # Overall
    overall = combined.get("overall_ok", False)
    print(f"\n  " + "=" * 61)
    if overall:
        print(f"  PIPELINE: PASS")
    else:
        print(f"  PIPELINE: FAIL")
    print(f"  " + "=" * 61)
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Auto-Extract Pipeline: measurement contexts + psi-scale validation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python auto_extract_pipeline.py                   # Full pipeline
  python auto_extract_pipeline.py --dry-run         # Preview only
  python auto_extract_pipeline.py --validate-only   # Skip extraction
  python auto_extract_pipeline.py --strict          # Exit 1 on issues
  python auto_extract_pipeline.py --json            # JSON output

Layer: 2 (Parameter Store Validation)
        """
    )

    parser.add_argument("--dry-run", action="store_true",
                        help="Preview extraction without writing")
    parser.add_argument("--validate-only", action="store_true",
                        help="Skip extraction, only validate")
    parser.add_argument("--strict", action="store_true",
                        help="Exit with code 1 if unmapped labels found")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON")
    parser.add_argument("--quiet", action="store_true",
                        help="Minimal output (for pre-commit hooks)")

    args = parser.parse_args()

    ok, combined = run_pipeline(
        dry_run=args.dry_run,
        validate_only=args.validate_only,
        strict=args.strict,
    )

    if args.json:
        import json
        print(json.dumps(combined, indent=2, default=str))
    elif args.quiet:
        if not ok:
            val = combined.get("validation", {})
            unmapped = val.get("unmapped_labels", {})
            total = sum(len(v) for v in unmapped.values())
            print(f"Psi-scale validation: {total} unmapped labels")
    else:
        print_pipeline_report(combined)

    if args.strict and not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
