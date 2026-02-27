#!/usr/bin/env python3
"""
Formula Compliance Checker: Exclusion Principle (EXC-1 to EXC-5)

This script validates that all aggregation formulas in the EBF framework
comply with the Exclusion Principle (Appendix FRM, Axioms EXC-1 to EXC-5).

EXC-5 defines the ONLY acceptable justifications for multiplicative formulas:
  V1: Veto-Logic (f=0 → Y=0)
  V2: Reversal-Logic (f<0 → sign flip)
  S1: Percentage-Scaling (f centered around 1)
  S2: Bounded-Output (inside sigmoid/logit)
  P1: Dimensional-Necessity (units require ×)
  P2: Conditional-Probability (P(A∩B) = P(A)·P(B|A))
  G1: Binary-Gate (f ∈ {0,1})
  C1: Capacity-Constraint (exhaustible capacity)
  E1: Empirically-Validated (p<0.05)
  T1: Theoretically-Derived (axiom → multiplicative)

Usage:
    python scripts/check_formula_compliance.py                    # Full report
    python scripts/check_formula_compliance.py --summary          # Summary only
    python scripts/check_formula_compliance.py --id K*-Ch20       # Check specific formula
    python scripts/check_formula_compliance.py --status pending   # Filter by status
    python scripts/check_formula_compliance.py --detect           # Detect new multiplicative formulas
    python scripts/check_formula_compliance.py --pre-commit       # Pre-commit mode (exit 1 if issues)

Reference: Appendix FRM, Axioms EXC-1 to EXC-5
"""

import yaml
import argparse
import sys
import re
from pathlib import Path
from typing import Dict, List, Optional
import glob

# ANSI colors for terminal output
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def load_formula_registry(registry_path: str = "data/formula-registry.yaml") -> Dict:
    """Load the formula registry YAML file."""
    with open(registry_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

# EXC-5 Whitelist: Only these justification codes are acceptable
EXC5_WHITELIST = {'V1', 'V2', 'S1', 'S2', 'P1', 'P2', 'G1', 'C1', 'E1', 'T1'}

def check_formula_compliance(formula: Dict) -> Dict:
    """
    Check a single formula for EXC compliance.

    Returns a dict with:
        - compliant: bool
        - issues: list of issues found
        - recommendations: list of recommendations
    """
    result = {
        'compliant': True,
        'issues': [],
        'recommendations': []
    }

    formulation = formula.get('formulation', 'unknown')
    status = formula.get('status', 'unknown')
    factors = formula.get('factors', [])
    justification = formula.get('justification', '')
    justification_code = formula.get('justification_code', None)

    # EXC-1: Additive is default (no issues for additive formulas)
    if formulation == 'additive':
        return result

    # EXC-5: Check if formula has valid justification code from whitelist
    if formulation in ('multiplicative', 'hybrid'):
        # If status is 'compliant' AND has valid EXC-5 justification code → accept
        if status == 'compliant' and justification_code in EXC5_WHITELIST:
            return result

        # If has valid justification code but status not updated → just info
        if justification_code in EXC5_WHITELIST:
            result['issues'].append(f"Has valid EXC-5 code ({justification_code}) but status is '{status}'")
            return result

        # Legacy check: analyze factors for veto_logic (for formulas without EXC-5 codes)
        veto_count = 0
        non_veto_count = 0
        unknown_count = 0

        for factor in factors:
            veto = factor.get('veto_logic', 'unknown')
            if veto == True:
                veto_count += 1
            elif veto == False or veto == 'reversal':  # 'reversal' counts as analyzed
                non_veto_count += 1
            else:
                unknown_count += 1

        # EXC-4: Documentation requirement
        if unknown_count > 0:
            result['compliant'] = False
            result['issues'].append(f"EXC-4 violation: {unknown_count} factors lack veto_logic analysis")
            result['recommendations'].append("Add justification_code (V1-T1) per EXC-5 whitelist")

        # No EXC-5 justification code → needs review
        if justification_code is None:
            result['compliant'] = False
            result['issues'].append("Missing justification_code - needs EXC-5 whitelist code (V1-T1)")
            result['recommendations'].append("Add justification_code from: V1, V2, S1, S2, P1, P2, G1, C1, E1, T1")

    # Check status
    if status == 'needs_revision':
        result['compliant'] = False
        result['issues'].append(f"Status is 'needs_revision': {justification}")
    elif status == 'pending_review':
        result['compliant'] = False
        result['issues'].append(f"Status is 'pending_review': Needs EXC-5 justification code")

    return result

def detect_multiplicative_formulas(tex_files: List[str]) -> List[Dict]:
    """
    Detect potential multiplicative formulas in LaTeX files.
    Looks for patterns like: Y = X · a · b · c or Y = X \cdot a \cdot b
    """
    detected = []

    # Patterns for multiplicative formulas
    patterns = [
        r'=\s*\w+\s*\\cdot\s*\w+\s*\\cdot',  # Y = X \cdot a \cdot b
        r'=\s*\w+\s*·\s*\w+\s*·',              # Y = X · a · b (unicode)
        r'\\prod',                              # \prod (explicit product)
        r'=\s*\w+\s*\^\s*\w+\s*\\times',       # Y = X^n \times
    ]

    for tex_file in tex_files:
        try:
            with open(tex_file, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')

                for i, line in enumerate(lines):
                    for pattern in patterns:
                        if re.search(pattern, line):
                            # Check if this line is in an equation environment
                            if any(env in line for env in ['equation', 'align', 'boxed']):
                                detected.append({
                                    'file': tex_file,
                                    'line': i + 1,
                                    'content': line.strip()[:100],
                                    'pattern': pattern
                                })
        except Exception as e:
            print(f"Warning: Could not read {tex_file}: {e}")

    return detected

def print_formula_report(formula: Dict, check_result: Dict) -> None:
    """Print a formatted report for a single formula."""
    status_colors = {
        'compliant': Colors.GREEN,
        'pending_review': Colors.YELLOW,
        'needs_revision': Colors.RED
    }

    status = formula.get('status', 'unknown')
    color = status_colors.get(status, Colors.RESET)

    print(f"\n{Colors.BOLD}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}Formula: {formula['id']}{Colors.RESET}")
    print(f"Name: {formula['name']}")
    print(f"Location: {formula['location']}")
    print(f"Formulation: {formula['formulation']}")
    print(f"Status: {color}{status}{Colors.RESET}")

    if formula.get('formula_latex'):
        print(f"Formula: {formula['formula_latex'][:80]}...")

    if check_result['issues']:
        print(f"\n{Colors.RED}Issues:{Colors.RESET}")
        for issue in check_result['issues']:
            print(f"  ❌ {issue}")

    if check_result['recommendations']:
        print(f"\n{Colors.YELLOW}Recommendations:{Colors.RESET}")
        for rec in check_result['recommendations']:
            print(f"  💡 {rec}")

    if check_result['compliant'] and not check_result['issues']:
        print(f"\n{Colors.GREEN}✅ Compliant with Exclusion Principle (EXC-1 to EXC-4){Colors.RESET}")

def print_summary(registry: Dict, results: Dict[str, Dict]) -> None:
    """Print a summary of all formula compliance checks."""
    summary = registry.get('summary', {})

    compliant_count = sum(1 for r in results.values() if r['compliant'] and not r['issues'])
    warning_count = sum(1 for r in results.values() if r['compliant'] and r['issues'])
    error_count = sum(1 for r in results.values() if not r['compliant'])

    print(f"\n{Colors.BOLD}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}EXCLUSION PRINCIPLE COMPLIANCE SUMMARY{Colors.RESET}")
    print(f"Reference: Appendix FRM, Axioms EXC-1 to EXC-4")
    print(f"{'='*70}")

    print(f"\n{Colors.GREEN}✅ Compliant:      {compliant_count}{Colors.RESET}")
    print(f"{Colors.YELLOW}⚠️  Warnings:       {warning_count}{Colors.RESET}")
    print(f"{Colors.RED}❌ Needs revision: {error_count}{Colors.RESET}")
    print(f"\nTotal formulas: {len(results)}")

    # List formulas by status
    if error_count > 0:
        print(f"\n{Colors.RED}Formulas needing revision:{Colors.RESET}")
        for formula_id, result in results.items():
            if not result['compliant']:
                print(f"  - {formula_id}")

    if warning_count > 0:
        print(f"\n{Colors.YELLOW}Formulas with warnings:{Colors.RESET}")
        for formula_id, result in results.items():
            if result['compliant'] and result['issues']:
                print(f"  - {formula_id}")

def main():
    parser = argparse.ArgumentParser(description='Check formula compliance with Exclusion Principle')
    parser.add_argument('--summary', action='store_true', help='Show summary only')
    parser.add_argument('--id', type=str, help='Check specific formula by ID')
    parser.add_argument('--status', type=str, choices=['compliant', 'pending_review', 'needs_revision'],
                        help='Filter by status')
    parser.add_argument('--detect', action='store_true', help='Detect new multiplicative formulas in tex files')
    parser.add_argument('--pre-commit', action='store_true', help='Pre-commit mode (exit 1 if issues)')
    parser.add_argument('--registry', type=str, default='data/formula-registry.yaml',
                        help='Path to formula registry YAML')

    args = parser.parse_args()

    # Detect mode: scan tex files for multiplicative formulas
    if args.detect:
        print(f"{Colors.BOLD}Scanning for multiplicative formulas...{Colors.RESET}")
        tex_files = glob.glob('chapters/*.tex') + glob.glob('appendices/*.tex')
        detected = detect_multiplicative_formulas(tex_files)

        if detected:
            print(f"\n{Colors.YELLOW}Found {len(detected)} potential multiplicative formulas:{Colors.RESET}")
            for d in detected[:20]:  # Limit output
                print(f"  {d['file']}:{d['line']}: {d['content'][:60]}...")
            if len(detected) > 20:
                print(f"  ... and {len(detected) - 20} more")
            print(f"\n{Colors.CYAN}Review these and add to formula-registry.yaml if not already tracked.{Colors.RESET}")
        else:
            print(f"{Colors.GREEN}No new multiplicative formulas detected.{Colors.RESET}")
        return

    # Load registry
    try:
        registry = load_formula_registry(args.registry)
    except FileNotFoundError:
        print(f"{Colors.RED}Error: Registry file not found: {args.registry}{Colors.RESET}")
        sys.exit(1)

    formulas = registry.get('formulas', [])

    # Filter by ID if specified
    if args.id:
        formulas = [f for f in formulas if f['id'] == args.id]
        if not formulas:
            print(f"{Colors.RED}Error: Formula '{args.id}' not found in registry{Colors.RESET}")
            sys.exit(1)

    # Filter by status if specified
    if args.status:
        formulas = [f for f in formulas if f.get('status') == args.status]

    # Check all formulas
    results = {}
    for formula in formulas:
        result = check_formula_compliance(formula)
        results[formula['id']] = result

        if not args.summary:
            print_formula_report(formula, result)

    # Print summary
    print_summary(registry, results)

    # Pre-commit mode: exit with error if issues
    if args.pre_commit:
        error_count = sum(1 for r in results.values() if not r['compliant'])
        if error_count > 0:
            print(f"\n{Colors.RED}❌ Pre-commit check failed: {error_count} formulas need revision{Colors.RESET}")
            print(f"Run 'python scripts/check_formula_compliance.py' for details")
            sys.exit(1)
        else:
            print(f"\n{Colors.GREEN}✅ Pre-commit check passed{Colors.RESET}")

if __name__ == '__main__':
    main()
