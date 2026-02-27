#!/usr/bin/env python3
"""
Extract Measurement Contexts from Paper-References
====================================================

Scans all data/paper-references/PAP-*.yaml files and extracts
measurement_contexts into a unified triplet database for PCT.

Output: data/pct-measurement-contexts.yaml
  - All (parameter, context, psi_conditions) triplets
  - Cross-referenced to paper keys, dimensions, study types

Usage:
    python extract_measurement_contexts.py                   # Full extraction
    python extract_measurement_contexts.py --update-scales   # Check for unmapped labels
    python extract_measurement_contexts.py --stats           # Statistics only
    python extract_measurement_contexts.py --paper PAP-benabou2022hurts
    python extract_measurement_contexts.py --dimension psi_S

Author: EBF Framework
Date: 2026-02-15
Layer: 1 (Formal Computation)
"""

import sys
import argparse
import json
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from collections import defaultdict
from datetime import date

REPO_ROOT = Path(__file__).resolve().parent.parent
PAPER_REFS_DIR = REPO_ROOT / "data" / "paper-references"
PSI_SCALES_PATH = REPO_ROOT / "data" / "pct-psi-scales.yaml"
OUTPUT_PATH = REPO_ROOT / "data" / "pct-measurement-contexts.yaml"


def load_yaml(path: Path) -> Optional[Dict]:
    """Load a YAML file, return None on failure."""
    try:
        import yaml
    except ImportError:
        print("ERROR: PyYAML required. Install with: pip install pyyaml")
        sys.exit(1)

    if not path.exists():
        return None

    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_yaml(data: Dict, path: Path) -> None:
    """Save data to YAML file."""
    import yaml

    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True,
                  sort_keys=False, width=120)


def normalize_dimension(dim: str) -> str:
    """Normalize Psi dimension key: Ψ_S → psi_S, Psi_S → psi_S."""
    return dim.replace("Ψ_", "psi_").replace("Psi_", "psi_")


def normalize_label(label: str) -> str:
    """Normalize a psi_condition label for consistent matching.

    Converts spaces, hyphens, and parenthetical notes to underscore format:
      'ages 0-5 (sensitive period)' → 'ages_0_5_sensitive_period'
      'group-based delivery' → 'group_based_delivery'
      'ego depletion context' → 'ego_depletion_context'
    """
    import re
    # Remove parentheses but keep content
    s = re.sub(r'[()]', '', label)
    # Replace hyphens and spaces with underscores
    s = re.sub(r'[-\s]+', '_', s.strip())
    # Remove trailing/leading underscores
    s = s.strip('_')
    return s


def extract_from_paper(paper_path: Path) -> List[Dict]:
    """
    Extract all measurement_contexts triplets from a single paper YAML.

    Returns a list of dicts, each representing one (parameter, context) pair.
    """
    data = load_yaml(paper_path)
    if data is None:
        return []

    # Extract paper key from filename: PAP-xxx.yaml → xxx
    paper_key = paper_path.stem
    if paper_key.startswith("PAP-"):
        paper_key = paper_key[4:]

    triplets = []

    # Look for parameter_contributions → measurement_contexts
    param_contributions = data.get("parameter_contributions", [])
    if not param_contributions:
        return []

    for param in param_contributions:
        symbol = param.get("symbol", "")
        ebf_id = param.get("ebf_id", "")
        name = param.get("name", param.get("parameter_name", ""))

        contexts = param.get("measurement_contexts", [])
        if not contexts:
            continue

        for ctx in contexts:
            if not isinstance(ctx, dict):
                continue

            # Normalize psi_conditions keys and labels
            raw_psi = ctx.get("psi_conditions", {})
            psi_conditions = {}
            if raw_psi and isinstance(raw_psi, dict):
                for dim, label in raw_psi.items():
                    norm_dim = normalize_dimension(dim)
                    if label:
                        psi_conditions[norm_dim] = normalize_label(str(label))

            triplet = {
                "paper_key": paper_key,
                "paper_file": paper_path.name,
                "parameter_symbol": symbol,
                "parameter_id": ebf_id,
                "parameter_name": name,
                "context": ctx.get("context", ""),
                "value_estimate": str(ctx.get("value_estimate", ctx.get("value", ""))),
                "psi_conditions": psi_conditions,
                "source_in_paper": ctx.get("source_in_paper", ""),
                "study_type": ctx.get("study_type", ""),
                "countries": ctx.get("countries", []),
                "n": ctx.get("n"),
            }

            # Also capture study-level field if present
            study = ctx.get("study")
            if study:
                triplet["study_reference"] = study

            triplets.append(triplet)

    return triplets


def extract_all() -> List[Dict]:
    """Extract measurement_contexts from all PAP-*.yaml files."""
    if not PAPER_REFS_DIR.exists():
        print(f"ERROR: {PAPER_REFS_DIR} not found")
        return []

    all_triplets = []
    paper_files = sorted(PAPER_REFS_DIR.glob("PAP-*.yaml"))

    for pf in paper_files:
        triplets = extract_from_paper(pf)
        all_triplets.extend(triplets)

    return all_triplets


def collect_psi_labels(triplets: List[Dict]) -> Dict[str, Set[str]]:
    """Collect all unique psi_condition labels by dimension."""
    labels_by_dim = defaultdict(set)
    for t in triplets:
        for dim, label in t.get("psi_conditions", {}).items():
            labels_by_dim[dim].add(label)
    return {k: v for k, v in sorted(labels_by_dim.items())}


def check_unmapped_labels(triplets: List[Dict]) -> Dict[str, List[str]]:
    """Check which psi_condition labels are not in pct-psi-scales.yaml."""
    scales_data = load_yaml(PSI_SCALES_PATH)
    if not scales_data:
        print("WARNING: pct-psi-scales.yaml not found, cannot check mappings")
        return {}

    scales = scales_data.get("scales", {})
    unmapped = defaultdict(list)

    labels_by_dim = collect_psi_labels(triplets)

    for dim, labels in labels_by_dim.items():
        dim_scales = scales.get(dim, {}).get("values", {})
        for label in sorted(labels):
            if label not in dim_scales:
                unmapped[dim].append(label)

    return dict(unmapped)


def print_stats(triplets: List[Dict]) -> None:
    """Print summary statistics."""
    papers = set(t["paper_key"] for t in triplets)
    params = set(t["parameter_symbol"] for t in triplets if t["parameter_symbol"])
    contexts = set(t["context"] for t in triplets if t["context"])
    study_types = set(t["study_type"] for t in triplets if t["study_type"])
    countries = set()
    for t in triplets:
        countries.update(t.get("countries", []))

    labels_by_dim = collect_psi_labels(triplets)
    total_labels = sum(len(v) for v in labels_by_dim.values())

    print()
    print("=" * 60)
    print("PCT MEASUREMENT CONTEXTS — EXTRACTION STATISTICS")
    print("=" * 60)
    print(f"\n   Papers with measurement_contexts:  {len(papers)}")
    print(f"   Total triplets (param × context):  {len(triplets)}")
    print(f"   Unique parameter symbols:          {len(params)}")
    print(f"   Unique context names:              {len(contexts)}")
    print(f"   Unique study types:                {len(study_types)}")
    print(f"   Countries covered:                 {len(countries)}")
    print(f"   Total unique Psi labels:           {total_labels}")

    print(f"\n   Psi-labels by dimension:")
    for dim, labels in sorted(labels_by_dim.items()):
        print(f"     {dim}: {len(labels)} labels")

    # Check unmapped
    unmapped = check_unmapped_labels(triplets)
    if unmapped:
        total_unmapped = sum(len(v) for v in unmapped.values())
        print(f"\n   Unmapped labels (not in psi-scales): {total_unmapped}")
        for dim, labels in sorted(unmapped.items()):
            for label in labels:
                print(f"     {dim}: {label}")
    else:
        print(f"\n   All labels mapped in psi-scales.yaml")

    # Papers breakdown
    print(f"\n   Papers:")
    for paper in sorted(papers):
        count = sum(1 for t in triplets if t["paper_key"] == paper)
        print(f"     {paper}: {count} triplets")

    print()


def build_output(triplets: List[Dict]) -> Dict:
    """Build the output YAML structure."""
    return {
        "version": "0.1",
        "generated": str(date.today()),
        "source": "data/paper-references/PAP-*.yaml",
        "description": "Extracted measurement_contexts triplets for PCT",
        "n_papers": len(set(t["paper_key"] for t in triplets)),
        "n_triplets": len(triplets),
        "n_parameters": len(set(t["parameter_symbol"] for t in triplets if t["parameter_symbol"])),
        "triplets": triplets,
    }


def filter_triplets(triplets: List[Dict], paper: str = None,
                     dimension: str = None, symbol: str = None) -> List[Dict]:
    """Filter triplets by paper, dimension, or symbol."""
    result = triplets

    if paper:
        paper_norm = paper.replace("PAP-", "").replace(".yaml", "")
        result = [t for t in result if paper_norm in t["paper_key"]]

    if dimension:
        dim_norm = normalize_dimension(dimension)
        result = [t for t in result if dim_norm in t.get("psi_conditions", {})]

    if symbol:
        result = [t for t in result if symbol.lower() in t.get("parameter_symbol", "").lower()]

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Extract measurement_contexts from PAP-*.yaml for PCT",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Scans all data/paper-references/PAP-*.yaml files and extracts
measurement_contexts into a unified triplet database.

Examples:
  python extract_measurement_contexts.py                  # Full extraction → YAML
  python extract_measurement_contexts.py --stats          # Statistics only
  python extract_measurement_contexts.py --update-scales  # Check unmapped labels
  python extract_measurement_contexts.py --paper benabou  # Filter by paper
  python extract_measurement_contexts.py --dimension psi_S --json

Layer: 1 (Formal Computation)
        """
    )

    parser.add_argument("--stats", action="store_true",
                        help="Show statistics only (no YAML output)")
    parser.add_argument("--update-scales", action="store_true",
                        help="Check for unmapped labels in psi-scales.yaml")
    parser.add_argument("--paper", type=str,
                        help="Filter by paper key (partial match)")
    parser.add_argument("--dimension", type=str,
                        help="Filter by Psi dimension (e.g. psi_S)")
    parser.add_argument("--symbol", type=str,
                        help="Filter by parameter symbol (e.g. lambda)")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON instead of YAML")
    parser.add_argument("--output", type=str,
                        help=f"Output path (default: {OUTPUT_PATH})")

    args = parser.parse_args()

    # Extract all triplets
    triplets = extract_all()

    if not triplets:
        print("No measurement_contexts found in any PAP-*.yaml file.")
        sys.exit(0)

    # Apply filters
    filtered = filter_triplets(
        triplets,
        paper=args.paper,
        dimension=args.dimension,
        symbol=args.symbol,
    )

    # Mode: update-scales
    if args.update_scales:
        unmapped = check_unmapped_labels(triplets)
        if unmapped:
            total = sum(len(v) for v in unmapped.values())
            print(f"\nUnmapped labels ({total} total):")
            print("Add these to data/pct-psi-scales.yaml:\n")
            for dim, labels in sorted(unmapped.items()):
                print(f"  {dim}:")
                for label in sorted(labels):
                    print(f"    {label}: ???  # TODO: assign value in [0, 1]")
            sys.exit(1)
        else:
            print("All psi_condition labels are mapped in psi-scales.yaml.")
            sys.exit(0)

    # Mode: stats
    if args.stats:
        print_stats(filtered)
        sys.exit(0)

    # Mode: output
    output = build_output(filtered)

    if args.json:
        print(json.dumps(output, indent=2, default=str))
    else:
        out_path = Path(args.output) if args.output else OUTPUT_PATH
        save_yaml(output, out_path)
        print(f"Extracted {len(filtered)} triplets from {output['n_papers']} papers")
        print(f"Output: {out_path}")

        # Also show stats
        print_stats(filtered)


if __name__ == "__main__":
    main()
