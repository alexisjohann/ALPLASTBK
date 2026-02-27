#!/usr/bin/env python3
"""
Validate PAR-4: Referential Integrity

Ensures every gamma_ij in model-registry.yaml has a parameter_ref to PAR-COMP-xxx
or is marked as domain_specific: true.

Usage:
    python scripts/validate_parameter_refs.py
    python scripts/validate_parameter_refs.py --fix  # Show what's missing
"""

import yaml
import sys
from pathlib import Path

def load_yaml(path: Path) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def get_par_comp_ids(param_registry: dict) -> set:
    """Extract all PAR-COMP-xxx IDs from parameter registry."""
    ids = set()
    comp_params = param_registry.get('complementarity_parameters', [])
    for param in comp_params:
        if param.get('id', '').startswith('PAR-COMP'):
            ids.add(param['id'])
    return ids

def find_gamma_without_ref(model_registry: dict) -> list:
    """Find all gamma_ij entries without parameter_ref or domain_specific."""
    violations = []

    def check_dict(d, path=""):
        if isinstance(d, dict):
            # Check if this is a gamma entry
            if 'gamma_ij' in d:
                has_ref = 'parameter_ref' in d
                is_domain_specific = d.get('domain_specific', False)

                if not has_ref and not is_domain_specific:
                    violations.append({
                        'path': path,
                        'gamma_ij': d.get('gamma_ij'),
                        'pair': d.get('pair', 'unknown'),
                        'mechanism': d.get('mechanism', '')[:50]
                    })

            # Recurse
            for k, v in d.items():
                check_dict(v, f"{path}.{k}" if path else k)
        elif isinstance(d, list):
            for i, item in enumerate(d):
                check_dict(item, f"{path}[{i}]")

    check_dict(model_registry)
    return violations

def main():
    repo_root = Path(__file__).parent.parent

    param_path = repo_root / 'data' / 'parameter-registry.yaml'
    model_path = repo_root / 'data' / 'model-registry.yaml'

    print("=" * 70)
    print("PAR-4 VALIDATION: Referential Integrity Check")
    print("=" * 70)
    print()

    # Load registries
    param_registry = load_yaml(param_path)
    model_registry = load_yaml(model_path)

    # Get available PAR-COMP IDs
    par_comp_ids = get_par_comp_ids(param_registry)
    print(f"Available PAR-COMP parameters: {len(par_comp_ids)}")
    for pid in sorted(par_comp_ids):
        print(f"  - {pid}")
    print()

    # Find violations
    violations = find_gamma_without_ref(model_registry)

    if violations:
        print(f"VIOLATIONS FOUND: {len(violations)}")
        print("-" * 70)
        for v in violations:
            print(f"  γ = {v['gamma_ij']}")
            print(f"    pair: {v['pair']}")
            print(f"    path: {v['path']}")
            print(f"    mechanism: {v['mechanism']}...")
            print()

        print("FIX: Add 'parameter_ref: PAR-COMP-xxx' or 'domain_specific: true'")
        print()
        sys.exit(1)
    else:
        print("✓ All gamma_ij entries have parameter_ref or domain_specific")
        print()

        # Summary
        total_gamma = 0
        with_ref = 0
        domain_specific = 0

        def count_gamma(d):
            nonlocal total_gamma, with_ref, domain_specific
            if isinstance(d, dict):
                if 'gamma_ij' in d:
                    total_gamma += 1
                    if 'parameter_ref' in d:
                        with_ref += 1
                    if d.get('domain_specific'):
                        domain_specific += 1
                for v in d.values():
                    count_gamma(v)
            elif isinstance(d, list):
                for item in d:
                    count_gamma(item)

        count_gamma(model_registry)

        print(f"SUMMARY:")
        print(f"  Total γ entries:     {total_gamma}")
        print(f"  With parameter_ref:  {with_ref}")
        print(f"  Domain-specific:     {domain_specific}")
        print()
        sys.exit(0)

if __name__ == '__main__':
    main()
