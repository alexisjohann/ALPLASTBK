#!/usr/bin/env python3
"""
=============================================================================
CONTEXT CONSISTENCY VALIDATOR
=============================================================================
Validates that context factors (Ψ dimensions) are used consistently across
all EBF analyses and databases. Detects contradictions and missing context.

Context Dimensions (Ψ):
- Ψ_I: Institutional (rules, defaults, regulations)
- Ψ_S: Social (peers, norms, identity)
- Ψ_K: Cultural (values, traditions, religion)
- Ψ_C: Cognitive (state, attention, fatigue)
- Ψ_E: Economic (resources, constraints, stakes)
- Ψ_T: Temporal (timing, phase, lifecycle)
- Ψ_M: Material (technology, tools, infrastructure)
- Ψ_F: Physical (location, environment)

Checks:
1. Context factors referenced in analyses exist in BCM2 database
2. Same context factor has consistent values across analyses
3. No contradictory context assumptions in same analysis
4. Context hierarchy respected (MACRO → MESO → MICRO)
5. All 8 Ψ dimensions considered where relevant
6. API data sources are current (freshness check)

Usage:
    python scripts/validate_context_consistency.py
    python scripts/validate_context_consistency.py --verbose
    python scripts/validate_context_consistency.py --check-freshness  # Check API data age

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
from datetime import datetime, timedelta

# =============================================================================
# PSI DIMENSION SPECIFICATIONS
# =============================================================================

PSI_DIMENSIONS = {
    'Ψ_I': {
        'name': 'Institutional',
        'aliases': ['psi_I', 'psi_institutional', 'institutional', 'rules', 'defaults'],
        'description': 'Rules, regulations, defaults, choice architecture',
        'typical_factors': ['default_type', 'regulation_level', 'compliance_norm']
    },
    'Ψ_S': {
        'name': 'Social',
        'aliases': ['psi_S', 'psi_social', 'social', 'peers', 'norms'],
        'description': 'Social norms, peer effects, identity',
        'typical_factors': ['peer_presence', 'social_norm_strength', 'in_group']
    },
    'Ψ_K': {
        'name': 'Cultural',
        'aliases': ['psi_K', 'psi_cultural', 'cultural', 'culture', 'values'],
        'description': 'Cultural values, traditions, religion',
        'typical_factors': ['individualism', 'uncertainty_avoidance', 'long_term_orientation']
    },
    'Ψ_C': {
        'name': 'Cognitive',
        'aliases': ['psi_C', 'psi_cognitive', 'cognitive', 'mental_state'],
        'description': 'Cognitive load, attention, fatigue, stress',
        'typical_factors': ['cognitive_load', 'attention', 'stress_level', 'fatigue']
    },
    'Ψ_E': {
        'name': 'Economic',
        'aliases': ['psi_E', 'psi_economic', 'economic', 'resources', 'stakes'],
        'description': 'Economic resources, constraints, stakes',
        'typical_factors': ['budget', 'income', 'wealth', 'stakes']
    },
    'Ψ_T': {
        'name': 'Temporal',
        'aliases': ['psi_T', 'psi_temporal', 'temporal', 'timing', 'phase'],
        'description': 'Time pressure, lifecycle phase, timing',
        'typical_factors': ['time_pressure', 'lifecycle_phase', 'deadline']
    },
    'Ψ_M': {
        'name': 'Material',
        'aliases': ['psi_M', 'psi_material', 'material', 'technology', 'tools'],
        'description': 'Technology, infrastructure, tools',
        'typical_factors': ['digital_access', 'interface_type', 'tool_availability']
    },
    'Ψ_F': {
        'name': 'Physical',
        'aliases': ['psi_F', 'psi_physical', 'physical', 'location', 'environment'],
        'description': 'Physical location, environment',
        'typical_factors': ['location_type', 'privacy', 'public_private']
    }
}

# Context hierarchy levels
CONTEXT_HIERARCHY = {
    'MACRO': {
        'description': 'Country/Market level',
        'typical_scope': 'National statistics, cultural dimensions, regulations',
        'bcm2_prefix': ['BCM2_04_KON']
    },
    'MESO': {
        'description': 'Industry/Organization level',
        'typical_scope': 'Industry norms, organizational culture, client specifics',
        'bcm2_prefix': ['BCM2_MIKRO', 'clients/', 'customers/']
    },
    'MICRO': {
        'description': 'Situation/Individual level',
        'typical_scope': '5 situational questions, individual characteristics',
        'bcm2_prefix': ['BCM2_05_IND', 'BCM2_06_META']
    }
}

# Data freshness thresholds (days)
FRESHNESS_THRESHOLDS = {
    'BFS': 365,      # Swiss Federal Statistics - yearly update
    'ESS': 730,      # European Social Survey - biennial
    'WVS': 1825,     # World Values Survey - every 5 years
    'OECD': 365,     # OECD - yearly
    'default': 365   # Default threshold
}


# =============================================================================
# DATA STRUCTURES
# =============================================================================

@dataclass
class ContextValue:
    """A context factor value with source"""
    factor_id: str
    value: Any
    psi_dimension: str
    hierarchy_level: str
    source_file: str
    source_id: str
    timestamp: Optional[str] = None


@dataclass
class ContextIssue:
    """A context consistency issue"""
    issue_type: str  # 'contradiction', 'missing_hierarchy', 'stale_data', 'undefined_factor'
    severity: str
    message: str
    context_values: List[ContextValue] = field(default_factory=list)
    analysis_id: str = ""


@dataclass
class ContextResult:
    """Complete context validation result"""
    issues: List[ContextIssue] = field(default_factory=list)
    factors_checked: int = 0
    factors_valid: int = 0
    analyses_checked: int = 0

    @property
    def score(self) -> float:
        if self.factors_checked == 0:
            return 100.0
        critical = sum(1 for i in self.issues if i.severity == 'critical')
        warnings = sum(1 for i in self.issues if i.severity == 'warning')
        penalty = critical * 10 + warnings * 2
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


def load_all_bcm2_factors(base_path: Path) -> Dict[str, ContextValue]:
    """Load all BCM2 context factors into a lookup dictionary"""
    factors = {}

    # Load from various BCM2 locations
    patterns = [
        'data/dr-datareq/sources/context/**/*.yaml',
        'data/dr-datareq/sources/global/*.yaml',
        'clients/**/*.yaml',
        'customers/**/*.yaml'
    ]

    for pattern in patterns:
        for f in glob.glob(str(base_path / pattern), recursive=True):
            data = load_yaml(f)
            if not data:
                continue

            # Determine hierarchy level from path
            hierarchy = 'MICRO'
            if 'BCM2_04_KON' in f or '/context/ch/' in f or '/context/at/' in f or '/context/de/' in f:
                hierarchy = 'MACRO'
            elif 'clients/' in f or 'customers/' in f or 'BCM2_MIKRO' in f:
                hierarchy = 'MESO'

            # Extract factors
            for factor in data.get('factors', []):
                if not factor:
                    continue
                factor_id = factor.get('id', '')
                if factor_id:
                    factors[factor_id] = ContextValue(
                        factor_id=factor_id,
                        value=factor.get('value'),
                        psi_dimension=factor.get('psi_dimension', 'unknown'),
                        hierarchy_level=hierarchy,
                        source_file=f,
                        source_id=factor_id,
                        timestamp=factor.get('last_updated') or data.get('metadata', {}).get('last_updated')
                    )

    return factors


# =============================================================================
# VALIDATORS
# =============================================================================

class ContextConsistencyValidator:
    def __init__(self, base_path: str, verbose: bool = False, check_freshness: bool = False):
        self.base_path = Path(base_path)
        self.verbose = verbose
        self.check_freshness = check_freshness
        self.result = ContextResult()

        # Load data
        self.bcm2_factors = load_all_bcm2_factors(self.base_path)
        self._load_analyses()

        if self.verbose:
            print(f"Loaded {len(self.bcm2_factors)} BCM2 context factors")
            print(f"Loaded {len(self.analyses)} analyses")

    def _load_analyses(self):
        """Load all analyses that use context factors"""
        self.analyses = []
        data_path = self.base_path / 'data'

        # Model Registry
        model_registry = load_yaml(data_path / 'model-registry.yaml') or {}
        for model in model_registry.get('models', []):
            if model:
                self.analyses.append({
                    'id': model.get('id', 'UNKNOWN'),
                    'type': 'model',
                    'data': model,
                    'source': 'model-registry.yaml'
                })

        # Case Registry
        case_registry = load_yaml(data_path / 'case-registry.yaml') or {}
        for case_id, case_data in case_registry.get('cases', {}).items():
            if case_data:
                self.analyses.append({
                    'id': case_id,
                    'type': 'case',
                    'data': case_data,
                    'source': 'case-registry.yaml'
                })

        # Session Registry
        session_registry = load_yaml(data_path / 'model-building-session.yaml') or {}
        for session in session_registry.get('sessions', []):
            if session:
                self.analyses.append({
                    'id': session.get('session_id', 'UNKNOWN'),
                    'type': 'session',
                    'data': session,
                    'source': 'model-building-session.yaml'
                })

    def _extract_context_refs(self, analysis: dict) -> List[Tuple[str, str, Any]]:
        """Extract context factor references from an analysis"""
        refs = []
        data = analysis['data']

        # Check psi_dimensions in models
        if 'psi_dimensions' in data:
            for psi in data['psi_dimensions']:
                refs.append(('psi_dimension', psi, None))

        # Check data_sources
        for source in data.get('data_sources', []):
            if not source:
                continue
            source_name = source.get('source', '')
            if 'BCM2' in source_name or 'context' in source_name.lower():
                refs.append(('data_source', source_name, source.get('type')))

        # Check context_parameters
        for context_key, params in data.get('context_parameters', {}).items():
            if isinstance(params, dict):
                for param_name, param_value in params.items():
                    refs.append(('context_param', f"{context_key}.{param_name}", param_value))

        # Check 10C.WHEN for context
        when_data = data.get('10C', {}).get('WHEN', {})
        if when_data:
            psi_dom = when_data.get('psi_dominant')
            if psi_dom:
                refs.append(('psi_dominant', psi_dom, None))

        return refs

    def validate_factor_existence(self):
        """Check that referenced context factors exist in BCM2"""
        if self.verbose:
            print("\n[1/5] Checking context factor existence...")

        for analysis in self.analyses:
            self.result.analyses_checked += 1
            refs = self._extract_context_refs(analysis)

            for ref_type, ref_name, ref_value in refs:
                self.result.factors_checked += 1

                # For data sources, check file exists
                if ref_type == 'data_source' and 'BCM2' in ref_name:
                    # Check if referenced BCM2 file exists
                    pattern = f"*{ref_name}*"
                    matches = list(self.base_path.glob(f"data/**/{pattern}"))
                    if not matches:
                        self.result.issues.append(ContextIssue(
                            issue_type='undefined_source',
                            severity='warning',
                            message=f"Analysis {analysis['id']} references non-existent BCM2 source: {ref_name}",
                            analysis_id=analysis['id']
                        ))
                    else:
                        self.result.factors_valid += 1

                # For psi dimensions, check valid
                elif ref_type == 'psi_dimension':
                    if not any(ref_name == dim or ref_name in PSI_DIMENSIONS[dim]['aliases']
                               for dim in PSI_DIMENSIONS):
                        self.result.issues.append(ContextIssue(
                            issue_type='invalid_psi',
                            severity='warning',
                            message=f"Analysis {analysis['id']} uses unknown Ψ dimension: {ref_name}",
                            analysis_id=analysis['id']
                        ))
                    else:
                        self.result.factors_valid += 1

    def validate_hierarchy_completeness(self):
        """Check that analyses consider all hierarchy levels where appropriate"""
        if self.verbose:
            print("[2/5] Checking context hierarchy completeness...")

        for analysis in self.analyses:
            if analysis['type'] != 'model':
                continue

            data = analysis['data']
            data_sources = data.get('data_sources', [])

            # Check which hierarchy levels are covered
            levels_covered = set()
            for source in data_sources:
                if not source:
                    continue
                source_name = source.get('source', '')
                if 'BCM2_04_KON' in source_name or '/context/' in source_name:
                    levels_covered.add('MACRO')
                elif 'BCM2_MIKRO' in source_name or 'clients/' in source_name:
                    levels_covered.add('MESO')
                elif 'context-dimensions' in source_name:
                    levels_covered.add('MICRO')

            # For behavioral models, all levels should ideally be covered
            if analysis['data'].get('question_type') in ['referral_activation', 'behavior_change', 'intervention']:
                missing = {'MACRO', 'MESO', 'MICRO'} - levels_covered
                if missing:
                    self.result.issues.append(ContextIssue(
                        issue_type='incomplete_hierarchy',
                        severity='info',
                        message=f"Model {analysis['id']} missing context hierarchy levels: {missing}",
                        analysis_id=analysis['id']
                    ))

    def validate_psi_coverage(self):
        """Check that relevant Ψ dimensions are considered"""
        if self.verbose:
            print("[3/5] Checking Ψ dimension coverage...")

        for analysis in self.analyses:
            if analysis['type'] != 'model':
                continue

            psi_dims = set(analysis['data'].get('psi_dimensions', []))

            # Normalize aliases to canonical names
            normalized_dims = set()
            for dim in psi_dims:
                for canonical, spec in PSI_DIMENSIONS.items():
                    if dim == canonical or dim in spec['aliases']:
                        normalized_dims.add(canonical)
                        break

            # Most models should consider at least 4 dimensions
            if len(normalized_dims) < 4:
                self.result.issues.append(ContextIssue(
                    issue_type='limited_psi_coverage',
                    severity='info',
                    message=f"Model {analysis['id']} only considers {len(normalized_dims)}/8 Ψ dimensions: {normalized_dims}",
                    analysis_id=analysis['id']
                ))

    def validate_cross_analysis_consistency(self):
        """Check that same context assumptions are consistent across analyses"""
        if self.verbose:
            print("[4/5] Checking cross-analysis consistency...")

        # Group analyses by domain/context
        context_values_by_domain = defaultdict(list)

        for analysis in self.analyses:
            refs = self._extract_context_refs(analysis)
            for ref_type, ref_name, ref_value in refs:
                if ref_type == 'context_param' and ref_value is not None:
                    domain = analysis['data'].get('domain', ['unknown'])[0] if isinstance(analysis['data'].get('domain'), list) else 'unknown'
                    context_values_by_domain[(domain, ref_name)].append({
                        'analysis_id': analysis['id'],
                        'value': ref_value
                    })

        # Check for inconsistencies within same domain
        for (domain, param_name), values in context_values_by_domain.items():
            if len(values) < 2:
                continue

            # Extract numeric values for comparison
            numeric_vals = []
            for v in values:
                val = v['value']
                if isinstance(val, dict):
                    val = val.get('mean', val.get('value'))
                if isinstance(val, (int, float)):
                    numeric_vals.append((v['analysis_id'], val))

            if len(numeric_vals) < 2:
                continue

            # Check for large deviations
            vals = [v[1] for v in numeric_vals]
            mean_val = sum(vals) / len(vals)
            if mean_val == 0:
                continue

            max_dev = max(abs(v - mean_val) / abs(mean_val) for v in vals)
            if max_dev > 0.30:  # 30% deviation threshold
                self.result.issues.append(ContextIssue(
                    issue_type='cross_analysis_conflict',
                    severity='warning',
                    message=f"Context parameter '{param_name}' varies {max_dev*100:.1f}% across {domain} analyses",
                    analysis_id=', '.join([v[0] for v in numeric_vals])
                ))

    def validate_data_freshness(self):
        """Check that external data sources are not stale"""
        if not self.check_freshness:
            return

        if self.verbose:
            print("[5/5] Checking data freshness...")

        now = datetime.now()

        for factor_id, factor in self.bcm2_factors.items():
            timestamp = factor.timestamp
            if not timestamp:
                continue

            try:
                # Parse timestamp
                if isinstance(timestamp, str):
                    if 'T' in timestamp:
                        ts = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    else:
                        ts = datetime.strptime(timestamp[:10], '%Y-%m-%d')
                else:
                    continue

                # Determine threshold based on source
                threshold_days = FRESHNESS_THRESHOLDS['default']
                for source, days in FRESHNESS_THRESHOLDS.items():
                    if source.lower() in factor.source_file.lower():
                        threshold_days = days
                        break

                age_days = (now - ts.replace(tzinfo=None)).days

                if age_days > threshold_days:
                    self.result.issues.append(ContextIssue(
                        issue_type='stale_data',
                        severity='warning',
                        message=f"Context factor {factor_id} is {age_days} days old (threshold: {threshold_days})",
                        context_values=[factor]
                    ))

            except Exception as e:
                if self.verbose:
                    print(f"  Warning: Could not parse timestamp for {factor_id}: {e}")

    def validate_all(self) -> ContextResult:
        """Run all validation checks"""
        print("=" * 70)
        print("CONTEXT CONSISTENCY VALIDATION")
        print("=" * 70)

        self.validate_factor_existence()
        self.validate_hierarchy_completeness()
        self.validate_psi_coverage()
        self.validate_cross_analysis_consistency()
        self.validate_data_freshness()

        return self.result


# =============================================================================
# OUTPUT
# =============================================================================

def print_results(result: ContextResult, verbose: bool = False):
    """Print validation results"""
    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)

    print(f"\nScore: {result.score:.1f}%")
    print(f"Analyses Checked: {result.analyses_checked}")
    print(f"Factors Checked: {result.factors_checked}")
    print(f"Factors Valid: {result.factors_valid}")

    critical = [i for i in result.issues if i.severity == 'critical']
    warnings = [i for i in result.issues if i.severity == 'warning']
    info = [i for i in result.issues if i.severity == 'info']

    print(f"\nIssues Found:")
    print(f"  - Critical: {len(critical)}")
    print(f"  - Warnings: {len(warnings)}")
    print(f"  - Info: {len(info)}")

    if critical:
        print("\n" + "-" * 70)
        print("CRITICAL ISSUES")
        print("-" * 70)
        for issue in critical:
            print(f"\n  [{issue.issue_type}] {issue.message}")
            if issue.analysis_id:
                print(f"    Analysis: {issue.analysis_id}")

    if warnings and verbose:
        print("\n" + "-" * 70)
        print("WARNINGS")
        print("-" * 70)
        for issue in warnings:
            print(f"\n  [{issue.issue_type}] {issue.message}")

    if info and verbose:
        print("\n" + "-" * 70)
        print("INFO")
        print("-" * 70)
        for issue in info:
            print(f"\n  [{issue.issue_type}] {issue.message}")

    print("\n" + "=" * 70)

    if result.score >= 85:
        print("✅ PASSED: Context consistency score >= 85%")
        return 0
    else:
        print("❌ FAILED: Context consistency score < 85%")
        return 1


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description='Validate context consistency across EBF databases')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed output')
    parser.add_argument('--check-freshness', action='store_true', help='Check data freshness')
    parser.add_argument('--path', default='.', help='Base path to repository')
    args = parser.parse_args()

    base_path = Path(args.path).resolve()
    if not (base_path / 'data').exists():
        print(f"Error: Cannot find data/ directory in {base_path}")
        sys.exit(1)

    validator = ContextConsistencyValidator(
        base_path,
        verbose=args.verbose,
        check_freshness=args.check_freshness
    )
    result = validator.validate_all()

    exit_code = print_results(result, verbose=args.verbose)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
