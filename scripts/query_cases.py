#!/usr/bin/env python3
"""
EBF Case Registry Query Tool

Query cases by 10C dimensions, domains, tags, and other attributes.

Usage:
    python query_cases.py --who heterogeneity=high --domain health
    python query_cases.py --stage action --gamma ">0.4"
    python query_cases.py --tag nudge --segment present-biased
    python query_cases.py CASE-001
    python query_cases.py --list-all
    python query_cases.py --stats

Author: EBF Team
Version: 1.0
"""

import argparse
import yaml
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional


def load_registry(path: str = None) -> Dict:
    """Load the case registry YAML file."""
    if path is None:
        # Default path relative to script location
        script_dir = Path(__file__).parent.parent
        path = script_dir / "data" / "case-registry.yaml"

    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def get_case(registry: Dict, case_id: str) -> Optional[Dict]:
    """Get a specific case by ID."""
    cases = registry.get('cases', {})
    return cases.get(case_id)


def generate_superkey(case: Dict) -> str:
    """Generate superkey from 10C coordinates."""
    c9 = case.get('10C', {})
    domain = case.get('domain', ['unknown'])[0]
    stage = c9.get('STAGE', {}).get('phase', 'unknown') or 'structural'
    hierarchy = c9.get('HIERARCHY', {}).get('primary_level', 'unknown')

    # Intervention type from tags or infer
    tags = case.get('tags', [])
    intervention = 'unknown'
    intervention_types = ['default', 'framing', 'social_norm', 'commitment',
                         'gamification', 'environmental', 'simplification',
                         'reciprocity', 'incentive', 'information']
    for t in tags:
        if t in intervention_types:
            intervention = t
            break

    # Segment
    segments = c9.get('WHO', {}).get('segments', ['general'])
    segment = segments[0] if segments else 'general'

    # Context
    psi = c9.get('WHEN', {}).get('psi_dominant', 'unknown')

    return f"{domain}:{stage}:{hierarchy}:{intervention}:{segment}:{psi}"


def check_superkey_unique(registry: Dict, new_superkey: str, exclude_id: str = None) -> List[str]:
    """Check if superkey already exists. Returns list of matching case IDs."""
    cases = registry.get('cases', {})
    matches = []
    for case_id, case in cases.items():
        if exclude_id and case_id == exclude_id:
            continue
        existing_key = case.get('superkey', '')
        if existing_key == new_superkey:
            matches.append(case_id)
    return matches


def find_similar_superkeys(registry: Dict, superkey: str, threshold: int = 3) -> List[tuple]:
    """Find cases with similar superkeys (matching N or more components)."""
    cases = registry.get('cases', {})
    parts = superkey.split(':')
    similar = []

    for case_id, case in cases.items():
        existing_key = case.get('superkey', '')
        existing_parts = existing_key.split(':')

        # Count matching components
        matches = sum(1 for p1, p2 in zip(parts, existing_parts) if p1 == p2)

        if matches >= threshold:
            similar.append((case_id, existing_key, matches))

    return sorted(similar, key=lambda x: -x[2])  # Sort by match count desc


def filter_by_who(cases: Dict, **kwargs) -> Dict:
    """Filter cases by WHO dimension."""
    results = {}
    for case_id, case in cases.items():
        who = case.get('10C', {}).get('WHO', {})
        match = True

        if 'levels' in kwargs:
            if kwargs['levels'] not in who.get('levels', []):
                match = False
        if 'heterogeneity' in kwargs:
            if who.get('heterogeneity') != kwargs['heterogeneity']:
                match = False
        if 'segments' in kwargs:
            if kwargs['segments'] not in who.get('segments', []):
                match = False

        if match:
            results[case_id] = case
    return results


def filter_by_stage(cases: Dict, phase: str) -> Dict:
    """Filter cases by STAGE (journey phase)."""
    results = {}
    for case_id, case in cases.items():
        stage = case.get('10C', {}).get('STAGE', {})
        if stage.get('phase') == phase:
            results[case_id] = case
    return results


def filter_by_gamma(cases: Dict, operator: str, value: float) -> Dict:
    """Filter cases by gamma_avg (complementarity)."""
    results = {}
    for case_id, case in cases.items():
        how = case.get('10C', {}).get('HOW', {})
        gamma = how.get('gamma_avg', 0)

        if gamma is None:
            continue

        if operator == '>' and gamma > value:
            results[case_id] = case
        elif operator == '<' and gamma < value:
            results[case_id] = case
        elif operator == '>=' and gamma >= value:
            results[case_id] = case
        elif operator == '<=' and gamma <= value:
            results[case_id] = case
        elif operator == '=' and gamma == value:
            results[case_id] = case

    return results


def filter_by_domain(cases: Dict, domain: str) -> Dict:
    """Filter cases by domain."""
    results = {}
    for case_id, case in cases.items():
        domains = case.get('domain', [])
        if domain.lower() in [d.lower() for d in domains]:
            results[case_id] = case
    return results


def filter_by_tag(cases: Dict, tag: str) -> Dict:
    """Filter cases by tag."""
    results = {}
    for case_id, case in cases.items():
        tags = case.get('tags', [])
        if tag.lower() in [t.lower() for t in tags]:
            results[case_id] = case
    return results


def filter_by_segment(cases: Dict, segment: str) -> Dict:
    """Filter cases by segment."""
    results = {}
    for case_id, case in cases.items():
        segments = case.get('10C', {}).get('WHO', {}).get('segments', [])
        for s in segments:
            if segment.lower() in s.lower():
                results[case_id] = case
                break
    return results


def filter_by_hierarchy(cases: Dict, level: str) -> Dict:
    """Filter cases by primary hierarchy level."""
    results = {}
    for case_id, case in cases.items():
        hierarchy = case.get('10C', {}).get('HIERARCHY', {})
        if hierarchy.get('primary_level') == level:
            results[case_id] = case
    return results


def format_case_brief(case_id: str, case: Dict) -> str:
    """Format a brief one-line summary of a case."""
    name = case.get('name', 'Unknown')
    domains = ', '.join(case.get('domain', [])[:3])
    stage = case.get('10C', {}).get('STAGE', {}).get('phase', 'n/a')
    gamma = case.get('10C', {}).get('HOW', {}).get('gamma_avg', 'n/a')

    return f"{case_id}: {name}\n   Domains: {domains} | Stage: {stage} | γ: {gamma}"


def format_case_full(case_id: str, case: Dict) -> str:
    """Format a full case display."""
    lines = []
    lines.append("=" * 70)
    lines.append(f"  {case_id}: {case.get('name', 'Unknown')}")
    lines.append("=" * 70)
    lines.append("")
    superkey = case.get('superkey', 'N/A')
    lines.append(f"SUPERKEY: {superkey}")
    lines.append("")
    lines.append(f"Description: {case.get('description', 'N/A').strip()}")
    lines.append("")

    # 10C Summary
    lines.append("10C DIMENSIONS:")
    c9 = case.get('10C', {})

    who = c9.get('WHO', {})
    lines.append(f"  WHO:       levels={who.get('levels')}, heterogeneity={who.get('heterogeneity')}")

    what = c9.get('WHAT', {})
    lines.append(f"  WHAT:      dimensions={what.get('dimensions')}, primary={what.get('primary')}")

    how = c9.get('HOW', {})
    lines.append(f"  HOW:       γ_avg={how.get('gamma_avg')}, interaction={how.get('interaction')}")

    when = c9.get('WHEN', {})
    lines.append(f"  WHEN:      Ψ_dominant={when.get('psi_dominant')}, temporal={when.get('temporal')}")

    where = c9.get('WHERE', {})
    lines.append(f"  WHERE:     source={where.get('source')}, confidence={where.get('confidence')}")

    aware = c9.get('AWARE', {})
    lines.append(f"  AWARE:     A={aware.get('A_level')}, type={aware.get('awareness_type')}")

    ready = c9.get('READY', {})
    lines.append(f"  READY:     W={ready.get('W_level')}, θ={ready.get('theta')}")

    stage = c9.get('STAGE', {})
    lines.append(f"  STAGE:     phase={stage.get('phase')}, stability={stage.get('stability')}")

    hier = c9.get('HIERARCHY', {})
    lines.append(f"  HIERARCHY: level={hier.get('primary_level')}, N_L2={hier.get('N_L2')}")

    lines.append("")
    lines.append(f"INSIGHT: {case.get('insight', 'N/A').strip()}")
    lines.append("")
    lines.append(f"IMPLICATION: {case.get('implication', 'N/A').strip()}")
    lines.append("")

    # Formulas
    formulas = case.get('formulas', [])
    if formulas:
        lines.append("FORMULAS:")
        for f in formulas:
            lines.append(f"  • {f.get('name')}: {f.get('formula')}")

    lines.append("")
    lines.append(f"Domains: {', '.join(case.get('domain', []))}")
    lines.append(f"Tags: {', '.join(case.get('tags', []))}")

    refs = case.get('references', {})
    lines.append(f"Appendices: {', '.join(refs.get('appendices', []))}")
    lines.append(f"Chapters: {', '.join(map(str, refs.get('chapters', [])))}")
    lines.append(f"Related: {', '.join(refs.get('cases', []))}")

    lines.append("")

    return "\n".join(lines)


def print_stats(registry: Dict):
    """Print statistics about the case registry."""
    cases = registry.get('cases', {})
    metadata = registry.get('metadata', {})

    print("\n" + "=" * 50)
    print("  EBF CASE REGISTRY STATISTICS")
    print("=" * 50)
    print(f"\nTotal Cases: {len(cases)}")
    print(f"Version: {metadata.get('version', 'unknown')}")
    print(f"Created: {metadata.get('created', 'unknown')}")

    print("\nDomains Covered:")
    for domain in metadata.get('domains_covered', []):
        count = len(filter_by_domain(cases, domain))
        print(f"  • {domain}: {count} cases")

    print("\nIntervention Types:")
    for itype in metadata.get('intervention_types', []):
        print(f"  • {itype}")

    print("\nSegments Covered:")
    for segment in metadata.get('segments_covered', []):
        print(f"  • {segment}")

    print("\n9C Coverage:")
    coverage = metadata.get('9C_coverage', {})
    for dim, count in coverage.items():
        print(f"  • {dim}: {count}/{len(cases)}")

    print()


def main():
    parser = argparse.ArgumentParser(
        description='Query the EBF Case Registry',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s CASE-001                           # Get specific case
  %(prog)s --domain health                    # All health cases
  %(prog)s --tag nudge                        # All nudge cases
  %(prog)s --stage action                     # Cases in action phase
  %(prog)s --gamma ">0.5"                     # High complementarity
  %(prog)s --segment present-biased           # Specific segment
  %(prog)s --hierarchy L2                     # L2-level interventions
  %(prog)s --who heterogeneity=high           # High heterogeneity cases
  %(prog)s --list-all                         # List all cases
  %(prog)s --stats                            # Show statistics
        """
    )

    parser.add_argument('case_id', nargs='?', help='Specific case ID to retrieve')
    parser.add_argument('--domain', '-d', help='Filter by domain')
    parser.add_argument('--tag', '-t', help='Filter by tag')
    parser.add_argument('--stage', '-s', help='Filter by journey stage (phase)')
    parser.add_argument('--gamma', '-g', help='Filter by gamma (e.g., ">0.5", "<0.3")')
    parser.add_argument('--segment', help='Filter by behavioral segment')
    parser.add_argument('--hierarchy', '-L', help='Filter by hierarchy level (L0-L3)')
    parser.add_argument('--who', help='Filter by WHO dimension (e.g., heterogeneity=high)')
    parser.add_argument('--list-all', '-l', action='store_true', help='List all cases')
    parser.add_argument('--stats', action='store_true', help='Show registry statistics')
    parser.add_argument('--brief', '-b', action='store_true', help='Brief output format')
    parser.add_argument('--registry', '-r', help='Path to registry YAML file')
    parser.add_argument('--validate-superkeys', action='store_true', help='Validate all superkeys are unique')
    parser.add_argument('--check-superkey', help='Check if a superkey exists (e.g., "health:action:L3:...")')
    parser.add_argument('--find-similar', help='Find cases with similar superkeys')

    args = parser.parse_args()

    # Load registry
    try:
        registry = load_registry(args.registry)
    except FileNotFoundError:
        print("Error: Case registry not found. Run from repository root or specify --registry path.")
        sys.exit(1)

    cases = registry.get('cases', {})

    # Handle specific case ID
    if args.case_id:
        case = get_case(registry, args.case_id.upper())
        if case:
            print(format_case_full(args.case_id.upper(), case))
        else:
            print(f"Case {args.case_id} not found.")
            sys.exit(1)
        return

    # Handle stats
    if args.stats:
        print_stats(registry)
        return

    # Handle superkey validation
    if args.validate_superkeys:
        print("\n" + "=" * 60)
        print("  SUPERKEY VALIDATION")
        print("=" * 60)
        seen = {}
        duplicates = []
        missing = []
        for case_id, case in cases.items():
            superkey = case.get('superkey')
            if not superkey:
                missing.append(case_id)
            elif superkey in seen:
                duplicates.append((case_id, seen[superkey], superkey))
            else:
                seen[superkey] = case_id

        if missing:
            print(f"\n⚠ MISSING SUPERKEYS ({len(missing)}):")
            for cid in missing:
                print(f"  - {cid}")

        if duplicates:
            print(f"\n❌ DUPLICATE SUPERKEYS ({len(duplicates)}):")
            for cid1, cid2, key in duplicates:
                print(f"  - {cid1} == {cid2}")
                print(f"    Key: {key}")

        if not missing and not duplicates:
            print(f"\n✓ All {len(cases)} superkeys are unique and present.")

        print()
        return

    # Handle superkey check
    if args.check_superkey:
        matches = check_superkey_unique(registry, args.check_superkey)
        if matches:
            print(f"\n❌ Superkey exists in: {', '.join(matches)}")
            for cid in matches:
                print(format_case_brief(cid, cases[cid]))
        else:
            print(f"\n✓ Superkey is unique: {args.check_superkey}")
        return

    # Handle similar superkey search
    if args.find_similar:
        similar = find_similar_superkeys(registry, args.find_similar, threshold=3)
        print(f"\n{'='*60}")
        print(f"  SIMILAR SUPERKEYS (≥3 components match)")
        print(f"{'='*60}")
        print(f"\nQuery: {args.find_similar}\n")
        if similar:
            for case_id, key, match_count in similar:
                print(f"  [{match_count}/6] {case_id}")
                print(f"         {key}")
                print()
        else:
            print("  No similar cases found.")
        return

    # Handle list-all
    if args.list_all:
        print(f"\n{'='*60}")
        print(f"  ALL CASES ({len(cases)} total)")
        print(f"{'='*60}\n")
        for case_id, case in cases.items():
            print(format_case_brief(case_id, case))
            print()
        return

    # Apply filters
    results = cases.copy()

    if args.domain:
        results = filter_by_domain(results, args.domain)

    if args.tag:
        results = filter_by_tag(results, args.tag)

    if args.stage:
        results = filter_by_stage(results, args.stage)

    if args.gamma:
        # Parse operator and value
        import re
        match = re.match(r'([<>=]+)\s*([\d.]+)', args.gamma)
        if match:
            op, val = match.groups()
            results = filter_by_gamma(results, op, float(val))

    if args.segment:
        results = filter_by_segment(results, args.segment)

    if args.hierarchy:
        results = filter_by_hierarchy(results, args.hierarchy.upper())

    if args.who:
        # Parse key=value
        if '=' in args.who:
            key, value = args.who.split('=', 1)
            results = filter_by_who(results, **{key: value})

    # Output results
    if not results:
        print("No cases match the specified criteria.")
        sys.exit(0)

    print(f"\n{'='*60}")
    print(f"  MATCHING CASES ({len(results)} found)")
    print(f"{'='*60}\n")

    for case_id, case in results.items():
        if args.brief:
            print(format_case_brief(case_id, case))
        else:
            print(format_case_full(case_id, case))


if __name__ == '__main__':
    main()
