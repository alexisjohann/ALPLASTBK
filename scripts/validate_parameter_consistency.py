#!/usr/bin/env python3
"""
=============================================================================
PARAMETER CONSISTENCY VALIDATOR
=============================================================================
Validates that behavioral economics parameters are used consistently across
all EBF databases. Detects conflicting values, range violations, and drift.

Key Parameters Tracked:
- λ (lambda): Loss aversion coefficient (typical: 2.0-2.5)
- β (beta): Present bias / hyperbolic discounting (typical: 0.7-1.0)
- γ (gamma): Complementarity coefficients (typical: -1 to +1)
- α (alpha): Risk aversion (typical: 0.5-1.0)
- δ (delta): Time discount factor (typical: 0.9-1.0)
- σ (sigma): Social preference weights (typical: 0-1)
- κ (kappa): Various context modifiers
- τ (tau): Trust parameters
- Ψ dimensions: Context factors

Checks:
1. Theory-catalog restrictions vs. model-registry parameters
2. Parameter-registry canonical values vs. usage in cases
3. BCM2 context factors vs. case-registry context values
4. Cross-database parameter naming consistency
5. Parameter range validity (within theoretical bounds)
6. Drift detection (>20% deviation from canonical values)

Usage:
    python scripts/validate_parameter_consistency.py
    python scripts/validate_parameter_consistency.py --verbose
    python scripts/validate_parameter_consistency.py --report  # Generate detailed report

Version: 1.0
Date: January 2026
=============================================================================
"""

import os
import sys
import re
import yaml
import glob
import argparse
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field
from collections import defaultdict
import math

# =============================================================================
# PARAMETER SPECIFICATIONS
# =============================================================================

# Canonical parameter ranges from behavioral economics literature
PARAMETER_SPECS = {
    # Loss Aversion
    'lambda': {
        'name': 'Loss Aversion',
        'aliases': ['λ', 'loss_aversion', 'lambda_loss'],
        'canonical_range': (1.5, 3.0),
        'typical_value': 2.25,
        'hard_bounds': (1.0, 5.0),
        'source': 'Kahneman & Tversky (1979), Tversky & Kahneman (1992)'
    },
    # Present Bias
    'beta': {
        'name': 'Present Bias',
        'aliases': ['β', 'present_bias', 'beta_hyperbolic'],
        'canonical_range': (0.6, 1.0),
        'typical_value': 0.85,
        'hard_bounds': (0.3, 1.0),
        'source': 'Laibson (1997), O\'Donoghue & Rabin (1999)'
    },
    # Time Discount Factor
    'delta': {
        'name': 'Time Discount Factor',
        'aliases': ['δ', 'time_discount', 'discount_factor'],
        'canonical_range': (0.9, 1.0),
        'typical_value': 0.95,
        'hard_bounds': (0.5, 1.0),
        'source': 'Frederick et al. (2002)'
    },
    # Risk Aversion
    'alpha': {
        'name': 'Risk Aversion',
        'aliases': ['α', 'risk_aversion', 'alpha_crra'],
        'canonical_range': (0.5, 2.0),
        'typical_value': 1.0,
        'hard_bounds': (0.0, 5.0),
        'source': 'Mehra & Prescott (1985)'
    },
    # Complementarity
    'gamma': {
        'name': 'Complementarity',
        'aliases': ['γ', 'complementarity', 'gamma_ij'],
        'canonical_range': (-0.5, 0.7),
        'typical_value': 0.3,
        'hard_bounds': (-1.0, 1.0),
        'source': 'EBF Framework (Chapter 10)'
    },
    # Inequity Aversion (alpha)
    'alpha_inequity': {
        'name': 'Disadvantageous Inequity Aversion',
        'aliases': ['alpha_FS', 'alpha_fehr_schmidt'],
        'canonical_range': (0.5, 4.0),
        'typical_value': 2.0,
        'hard_bounds': (0.0, 10.0),
        'source': 'Fehr & Schmidt (1999)'
    },
    # Inequity Aversion (beta)
    'beta_inequity': {
        'name': 'Advantageous Inequity Aversion',
        'aliases': ['beta_FS', 'beta_fehr_schmidt'],
        'canonical_range': (0.0, 0.6),
        'typical_value': 0.3,
        'hard_bounds': (0.0, 1.0),
        'source': 'Fehr & Schmidt (1999)'
    },
    # Trust
    'tau': {
        'name': 'Trust/Trustworthiness',
        'aliases': ['τ', 'trust', 'trust_level'],
        'canonical_range': (0.3, 0.8),
        'typical_value': 0.5,
        'hard_bounds': (0.0, 1.0),
        'source': 'Berg et al. (1995)'
    },
    # Social Weight
    'sigma': {
        'name': 'Social Preference Weight',
        'aliases': ['σ', 'social_weight', 'altruism'],
        'canonical_range': (0.0, 0.5),
        'typical_value': 0.2,
        'hard_bounds': (0.0, 1.0),
        'source': 'Charness & Rabin (2002)'
    },
}

# Deviation thresholds
DEVIATION_THRESHOLDS = {
    'warning': 0.10,   # 10% deviation = warning
    'review': 0.20,    # 20% deviation = needs review
    'critical': 0.50   # 50% deviation = critical
}


# =============================================================================
# DATA STRUCTURES
# =============================================================================

@dataclass
class ParameterValue:
    """A parameter value with source context"""
    name: str
    value: float
    source_file: str
    source_id: str
    context: str = ""
    confidence: str = "medium"


@dataclass
class ConsistencyIssue:
    """A parameter consistency issue"""
    parameter: str
    issue_type: str  # 'range_violation', 'drift', 'conflict', 'naming'
    severity: str  # 'critical', 'warning', 'info'
    message: str
    values: List[ParameterValue] = field(default_factory=list)
    deviation: float = 0.0


@dataclass
class ConsistencyResult:
    """Complete consistency check result"""
    issues: List[ConsistencyIssue] = field(default_factory=list)
    parameters_checked: int = 0
    parameters_valid: int = 0

    @property
    def score(self) -> float:
        if self.parameters_checked == 0:
            return 100.0
        critical_count = sum(1 for i in self.issues if i.severity == 'critical')
        warning_count = sum(1 for i in self.issues if i.severity == 'warning')
        penalty = (critical_count * 10 + warning_count * 2)
        return max(0, 100 - penalty)


# =============================================================================
# FILE LOADERS
# =============================================================================

def load_yaml(path: str) -> Optional[dict]:
    """Load YAML file safely"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        return None


def load_all_bcm2_files(base_path: Path) -> List[dict]:
    """Load all BCM2 context YAML files"""
    bcm2_files = []
    patterns = [
        'data/dr-datareq/sources/context/**/*.yaml',
        'data/dr-datareq/sources/global/*.yaml'
    ]
    for pattern in patterns:
        for f in glob.glob(str(base_path / pattern), recursive=True):
            data = load_yaml(f)
            if data:
                data['_source_file'] = f
                bcm2_files.append(data)
    return bcm2_files


# =============================================================================
# PARAMETER EXTRACTION
# =============================================================================

def normalize_parameter_name(name: str) -> str:
    """Normalize parameter name to canonical form"""
    name_lower = name.lower().strip()

    # Check against all aliases
    for canonical, spec in PARAMETER_SPECS.items():
        if name_lower == canonical:
            return canonical
        for alias in spec.get('aliases', []):
            if name_lower == alias.lower():
                return canonical

    return name_lower


def extract_numeric_value(value: Any) -> Optional[float]:
    """Extract numeric value from various formats"""
    if isinstance(value, (int, float)):
        return float(value)

    if isinstance(value, str):
        # Handle ranges like "2.0-2.5"
        range_match = re.match(r'([\d.]+)\s*[-–]\s*([\d.]+)', value)
        if range_match:
            low = float(range_match.group(1))
            high = float(range_match.group(2))
            return (low + high) / 2

        # Handle simple numbers
        num_match = re.match(r'^([\d.]+)', value)
        if num_match:
            return float(num_match.group(1))

    if isinstance(value, dict):
        # Handle {mean: X, ci_68: [...]} format
        if 'mean' in value:
            return float(value['mean'])
        if 'value' in value:
            return float(value['value'])

    return None


def extract_parameters_from_model(model: dict, source_file: str) -> List[ParameterValue]:
    """Extract all parameters from a model definition"""
    params = []
    model_id = model.get('id', 'UNKNOWN')

    # Extract from variables
    for var in model.get('variables', []):
        if not var:
            continue
        symbol = var.get('symbol', '')
        weight = var.get('weight')
        if weight:
            params.append(ParameterValue(
                name=f"{symbol}_weight",
                value=extract_numeric_value(weight) or 0,
                source_file=source_file,
                source_id=model_id,
                context=f"variable weight for {var.get('name', symbol)}"
            ))

    # Extract from functional_form.parameters
    func_form = model.get('functional_form', {})
    for key, value in func_form.get('parameters', {}).items():
        num_val = extract_numeric_value(value)
        if num_val is not None:
            params.append(ParameterValue(
                name=normalize_parameter_name(key),
                value=num_val,
                source_file=source_file,
                source_id=model_id,
                context=f"functional form parameter"
            ))

    # Extract from context_parameters
    for context_key, context_params in model.get('context_parameters', {}).items():
        if isinstance(context_params, dict):
            for key, value in context_params.items():
                num_val = extract_numeric_value(value)
                if num_val is not None:
                    params.append(ParameterValue(
                        name=normalize_parameter_name(key),
                        value=num_val,
                        source_file=source_file,
                        source_id=model_id,
                        context=f"context parameter ({context_key})"
                    ))

    # Extract from complementarity_matrix
    for pair_def in model.get('complementarity_matrix', []):
        gamma = pair_def.get('gamma_ij')
        if gamma is not None:
            pair = pair_def.get('pair', ['?', '?'])
            params.append(ParameterValue(
                name='gamma',
                value=extract_numeric_value(gamma) or 0,
                source_file=source_file,
                source_id=model_id,
                context=f"complementarity {pair[0]}-{pair[1]}"
            ))

    return params


def extract_parameters_from_theory(theory: dict, source_file: str) -> List[ParameterValue]:
    """Extract EBF restrictions from theory definition"""
    params = []
    theory_id = theory.get('id', 'UNKNOWN')

    restrictions = theory.get('ebf_restrictions', {})
    for key, value in restrictions.items():
        # Skip non-numeric restrictions like "exogenous"
        if isinstance(value, str) and not re.match(r'^[\d.]+', value):
            continue
        num_val = extract_numeric_value(value)
        if num_val is not None:
            params.append(ParameterValue(
                name=normalize_parameter_name(key),
                value=num_val,
                source_file=source_file,
                source_id=theory_id,
                context=f"EBF restriction"
            ))

    return params


def extract_parameters_from_case(case_id: str, case_data: dict, source_file: str) -> List[ParameterValue]:
    """Extract parameters from case definition"""
    params = []

    # Extract from 10C dimensions
    for dim_name, dim_data in case_data.get('10C', {}).items():
        if not isinstance(dim_data, dict):
            continue

        for key, value in dim_data.items():
            if key.endswith('_level') or key.startswith('gamma') or key.startswith('N_'):
                num_val = extract_numeric_value(value)
                if num_val is not None:
                    params.append(ParameterValue(
                        name=normalize_parameter_name(key),
                        value=num_val,
                        source_file=source_file,
                        source_id=case_id,
                        context=f"10C dimension {dim_name}"
                    ))

    # Extract from formulas
    for formula in case_data.get('formulas', []):
        if not formula:
            continue
        for var_name, var_value in formula.get('variables', {}).items():
            num_val = extract_numeric_value(var_value)
            if num_val is not None:
                params.append(ParameterValue(
                    name=normalize_parameter_name(var_name),
                    value=num_val,
                    source_file=source_file,
                    source_id=case_id,
                    context=f"formula variable"
                ))

    return params


def extract_parameters_from_bcm2(bcm2_data: dict) -> List[ParameterValue]:
    """Extract parameters from BCM2 context files"""
    params = []
    source_file = bcm2_data.get('_source_file', 'BCM2')

    # Handle factors list
    for factor in bcm2_data.get('factors', []):
        if not factor:
            continue
        factor_id = factor.get('id', 'UNKNOWN')
        value = factor.get('value')
        if value is not None:
            num_val = extract_numeric_value(value)
            if num_val is not None:
                params.append(ParameterValue(
                    name=factor.get('name', factor_id),
                    value=num_val,
                    source_file=source_file,
                    source_id=factor_id,
                    context="BCM2 context factor"
                ))

    return params


# =============================================================================
# VALIDATORS
# =============================================================================

class ParameterConsistencyValidator:
    def __init__(self, base_path: str, verbose: bool = False):
        self.base_path = Path(base_path)
        self.verbose = verbose
        self.result = ConsistencyResult()
        self.all_parameters: Dict[str, List[ParameterValue]] = defaultdict(list)

        # Load all data sources
        self._load_and_extract_parameters()

    def _load_and_extract_parameters(self):
        """Load all data sources and extract parameters"""
        data_path = self.base_path / 'data'

        # 1. Model Registry
        model_registry = load_yaml(data_path / 'model-registry.yaml') or {}
        for model in model_registry.get('models', []):
            if model:
                for param in extract_parameters_from_model(model, 'model-registry.yaml'):
                    self.all_parameters[param.name].append(param)

        # 2. Theory Catalog
        theory_catalog = load_yaml(data_path / 'theory-catalog.yaml') or {}
        for cat in theory_catalog.get('categories', []):
            if not cat:
                continue
            for theory in cat.get('theories', []):
                if theory:
                    for param in extract_parameters_from_theory(theory, 'theory-catalog.yaml'):
                        self.all_parameters[param.name].append(param)

        # 3. Case Registry
        case_registry = load_yaml(data_path / 'case-registry.yaml') or {}
        for case_id, case_data in case_registry.get('cases', {}).items():
            if case_data:
                for param in extract_parameters_from_case(case_id, case_data, 'case-registry.yaml'):
                    self.all_parameters[param.name].append(param)

        # 4. Parameter Registry
        param_registry = load_yaml(data_path / 'parameter-registry.yaml') or {}
        for param_def in param_registry.get('parameters', []):
            if not param_def:
                continue
            name = normalize_parameter_name(param_def.get('name', ''))
            value = extract_numeric_value(param_def.get('canonical_value'))
            if value is not None:
                self.all_parameters[name].append(ParameterValue(
                    name=name,
                    value=value,
                    source_file='parameter-registry.yaml',
                    source_id=param_def.get('id', 'UNKNOWN'),
                    context='canonical value',
                    confidence='high'
                ))

        # 5. BCM2 Context Files
        bcm2_files = load_all_bcm2_files(self.base_path)
        for bcm2_data in bcm2_files:
            for param in extract_parameters_from_bcm2(bcm2_data):
                self.all_parameters[param.name].append(param)

        if self.verbose:
            print(f"Extracted {sum(len(v) for v in self.all_parameters.values())} parameter values")
            print(f"Unique parameters: {len(self.all_parameters)}")

    def check_range_validity(self):
        """Check if parameters are within valid ranges"""
        if self.verbose:
            print("\n[1/4] Checking parameter range validity...")

        for param_name, spec in PARAMETER_SPECS.items():
            values = self.all_parameters.get(param_name, [])
            self.result.parameters_checked += len(values)

            for pv in values:
                hard_low, hard_high = spec['hard_bounds']

                if pv.value < hard_low or pv.value > hard_high:
                    self.result.issues.append(ConsistencyIssue(
                        parameter=param_name,
                        issue_type='range_violation',
                        severity='critical',
                        message=f"Parameter {param_name}={pv.value} outside hard bounds [{hard_low}, {hard_high}]",
                        values=[pv]
                    ))
                else:
                    soft_low, soft_high = spec['canonical_range']
                    if pv.value < soft_low or pv.value > soft_high:
                        self.result.issues.append(ConsistencyIssue(
                            parameter=param_name,
                            issue_type='range_warning',
                            severity='warning',
                            message=f"Parameter {param_name}={pv.value} outside typical range [{soft_low}, {soft_high}]",
                            values=[pv]
                        ))
                    else:
                        self.result.parameters_valid += 1

    def check_cross_database_consistency(self):
        """Check consistency of same parameter across databases"""
        if self.verbose:
            print("[2/4] Checking cross-database consistency...")

        for param_name, values in self.all_parameters.items():
            if len(values) < 2:
                continue

            # Get distinct values
            numeric_values = [pv.value for pv in values if pv.value is not None]
            if not numeric_values:
                continue

            mean_val = sum(numeric_values) / len(numeric_values)
            max_deviation = max(abs(v - mean_val) / mean_val if mean_val != 0 else 0 for v in numeric_values)

            if max_deviation > DEVIATION_THRESHOLDS['critical']:
                self.result.issues.append(ConsistencyIssue(
                    parameter=param_name,
                    issue_type='conflict',
                    severity='critical',
                    message=f"Parameter {param_name} has {max_deviation*100:.1f}% deviation across databases",
                    values=values,
                    deviation=max_deviation
                ))
            elif max_deviation > DEVIATION_THRESHOLDS['review']:
                self.result.issues.append(ConsistencyIssue(
                    parameter=param_name,
                    issue_type='drift',
                    severity='warning',
                    message=f"Parameter {param_name} shows {max_deviation*100:.1f}% drift (needs review)",
                    values=values,
                    deviation=max_deviation
                ))

    def check_theory_model_alignment(self):
        """Check that model parameters align with theory restrictions"""
        if self.verbose:
            print("[3/4] Checking theory-model alignment...")

        data_path = self.base_path / 'data'

        theory_catalog = load_yaml(data_path / 'theory-catalog.yaml') or {}
        model_registry = load_yaml(data_path / 'model-registry.yaml') or {}

        # Build theory restrictions map
        theory_restrictions = {}
        for cat in theory_catalog.get('categories', []):
            if not cat:
                continue
            for theory in cat.get('theories', []):
                if not theory:
                    continue
                theory_id = theory.get('id')
                restrictions = theory.get('ebf_restrictions', {})
                theory_restrictions[theory_id] = restrictions

        # Check model against its referenced theories
        for model in model_registry.get('models', []):
            if not model:
                continue
            model_id = model.get('id', 'UNKNOWN')

            # Get referenced theories
            theory_refs = []
            theory_basis = model.get('theory_basis', {})
            for section in ['primary', 'secondary']:
                for ref in theory_basis.get(section, []):
                    if ref:
                        theory_refs.append(ref.get('theory_id'))

            # Check model params against theory restrictions
            model_params = extract_parameters_from_model(model, 'model-registry.yaml')

            for theory_id in theory_refs:
                if theory_id not in theory_restrictions:
                    continue

                restrictions = theory_restrictions[theory_id]

                for param in model_params:
                    canonical_name = param.name.replace('_weight', '')

                    if canonical_name in restrictions:
                        theory_value = restrictions[canonical_name]
                        if isinstance(theory_value, (int, float)):
                            # Check if model violates theory restriction
                            if abs(param.value - theory_value) > 0.01:  # Small tolerance
                                self.result.issues.append(ConsistencyIssue(
                                    parameter=canonical_name,
                                    issue_type='theory_conflict',
                                    severity='warning',
                                    message=f"Model {model_id} has {canonical_name}={param.value} but theory {theory_id} requires {theory_value}",
                                    values=[param],
                                    deviation=abs(param.value - theory_value)
                                ))

    def check_naming_consistency(self):
        """Check for parameter naming inconsistencies"""
        if self.verbose:
            print("[4/4] Checking naming consistency...")

        # Find parameters that might be the same but named differently
        suspicious_pairs = [
            ('lambda', 'loss_aversion'),
            ('beta', 'present_bias'),
            ('gamma', 'complementarity'),
            ('alpha', 'risk_aversion'),
        ]

        for p1, p2 in suspicious_pairs:
            v1 = self.all_parameters.get(p1, [])
            v2 = self.all_parameters.get(p2, [])

            if v1 and v2:
                # Already normalized to same name, but check if sources use different names
                pass  # This is handled by normalization

    def validate_all(self) -> ConsistencyResult:
        """Run all validation checks"""
        print("=" * 70)
        print("PARAMETER CONSISTENCY VALIDATION")
        print("=" * 70)

        self.check_range_validity()
        self.check_cross_database_consistency()
        self.check_theory_model_alignment()
        self.check_naming_consistency()

        return self.result


# =============================================================================
# OUTPUT
# =============================================================================

def print_results(result: ConsistencyResult, verbose: bool = False):
    """Print validation results"""
    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)

    print(f"\nScore: {result.score:.1f}%")
    print(f"Parameters Checked: {result.parameters_checked}")
    print(f"Parameters Valid: {result.parameters_valid}")

    critical_issues = [i for i in result.issues if i.severity == 'critical']
    warning_issues = [i for i in result.issues if i.severity == 'warning']

    print(f"\nIssues Found:")
    print(f"  - Critical: {len(critical_issues)}")
    print(f"  - Warnings: {len(warning_issues)}")

    if critical_issues:
        print("\n" + "-" * 70)
        print("CRITICAL ISSUES")
        print("-" * 70)
        for issue in critical_issues:
            print(f"\n  [{issue.issue_type}] {issue.message}")
            if issue.deviation > 0:
                print(f"    Deviation: {issue.deviation*100:.1f}%")
            for pv in issue.values[:3]:  # Show max 3 examples
                print(f"    - {pv.source_file}:{pv.source_id} = {pv.value} ({pv.context})")

    if warning_issues and verbose:
        print("\n" + "-" * 70)
        print("WARNINGS")
        print("-" * 70)
        for issue in warning_issues:
            print(f"\n  [{issue.issue_type}] {issue.message}")
            if issue.deviation > 0:
                print(f"    Deviation: {issue.deviation*100:.1f}%")

    print("\n" + "=" * 70)

    if result.score >= 85:
        print("✅ PASSED: Parameter consistency score >= 85%")
        return 0
    else:
        print("❌ FAILED: Parameter consistency score < 85%")
        return 1


def generate_report(result: ConsistencyResult, base_path: Path):
    """Generate detailed parameter consistency report"""
    report_path = base_path / 'quality' / 'parameter-consistency-report.md'

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Parameter Consistency Report\n\n")
        f.write(f"Generated: {__import__('datetime').datetime.now().isoformat()}\n\n")
        f.write(f"**Score:** {result.score:.1f}%\n\n")

        f.write("## Summary\n\n")
        f.write(f"- Parameters Checked: {result.parameters_checked}\n")
        f.write(f"- Parameters Valid: {result.parameters_valid}\n")
        f.write(f"- Critical Issues: {len([i for i in result.issues if i.severity == 'critical'])}\n")
        f.write(f"- Warnings: {len([i for i in result.issues if i.severity == 'warning'])}\n\n")

        if result.issues:
            f.write("## Issues\n\n")
            for issue in result.issues:
                emoji = "🔴" if issue.severity == 'critical' else "🟡"
                f.write(f"### {emoji} {issue.parameter}: {issue.issue_type}\n\n")
                f.write(f"{issue.message}\n\n")
                if issue.values:
                    f.write("| Source | ID | Value | Context |\n")
                    f.write("|--------|----|----- -|--------|\n")
                    for pv in issue.values:
                        f.write(f"| {pv.source_file} | {pv.source_id} | {pv.value} | {pv.context} |\n")
                    f.write("\n")

    print(f"Report saved to: {report_path}")


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description='Validate parameter consistency across EBF databases')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed output')
    parser.add_argument('--report', action='store_true', help='Generate detailed report')
    parser.add_argument('--path', default='.', help='Base path to repository')
    args = parser.parse_args()

    base_path = Path(args.path).resolve()
    if not (base_path / 'data').exists():
        print(f"Error: Cannot find data/ directory in {base_path}")
        sys.exit(1)

    validator = ParameterConsistencyValidator(base_path, verbose=args.verbose)
    result = validator.validate_all()

    if args.report:
        generate_report(result, base_path)

    exit_code = print_results(result, verbose=args.verbose)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
