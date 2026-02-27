#!/usr/bin/env python3
"""
EBF Intervention Registry Query & Analysis Tool

Query projects, analyze deviations, extract learnings, and update parameters.

Usage:
    python query_interventions.py PRJ-001              # Get specific project
    python query_interventions.py --domain health      # Filter by domain
    python query_interventions.py --status completed   # Filter by status
    python query_interventions.py --deviation          # Deviation analysis
    python query_interventions.py --learnings          # Extract all learnings
    python query_interventions.py --parameters         # Show parameter updates
    python query_interventions.py --accuracy           # Prediction accuracy stats

Author: EBF Team
Version: 1.0
"""

import argparse
import yaml
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import statistics


def load_registry(path: str = None) -> Dict:
    """Load the intervention registry YAML file."""
    if path is None:
        script_dir = Path(__file__).parent.parent
        path = script_dir / "data" / "intervention-registry.yaml"

    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def get_project(registry: Dict, project_id: str) -> Optional[Dict]:
    """Get a specific project by ID."""
    projects = registry.get('projects', {})
    return projects.get(project_id)


def filter_by_domain(projects: Dict, domain: str) -> Dict:
    """Filter projects by domain."""
    results = {}
    for pid, proj in projects.items():
        if proj.get('meta', {}).get('domain', '').lower() == domain.lower():
            results[pid] = proj
    return results


def filter_by_status(projects: Dict, status: str) -> Dict:
    """Filter projects by status."""
    results = {}
    for pid, proj in projects.items():
        if proj.get('meta', {}).get('status', '').lower() == status.lower():
            results[pid] = proj
    return results


def calculate_deviation_stats(projects: Dict) -> Dict:
    """Calculate deviation statistics across all projects."""
    deviations = []
    by_intervention_type = {}

    for pid, proj in projects.items():
        if proj.get('meta', {}).get('status') != 'completed':
            continue

        dev = proj.get('deviation_analysis', {}).get('overall', {})
        if dev.get('delta_pct') is not None:
            deviations.append({
                'project': pid,
                'predicted': dev.get('predicted_E_P'),
                'actual': dev.get('actual_E_P'),
                'delta': dev.get('delta'),
                'delta_pct': dev.get('delta_pct'),
                'direction': dev.get('direction')
            })

        # By intervention
        for idev in proj.get('deviation_analysis', {}).get('by_intervention', []):
            itype = None
            for i in proj.get('intervention_mix', []):
                if i['id'] == idev['id']:
                    itype = i.get('type', 'unknown')
                    break
            if itype:
                if itype not in by_intervention_type:
                    by_intervention_type[itype] = []
                by_intervention_type[itype].append({
                    'project': pid,
                    'intervention': idev['id'],
                    'predicted': idev.get('predicted'),
                    'actual': idev.get('actual'),
                    'delta': idev.get('delta')
                })

    return {
        'overall': deviations,
        'by_type': by_intervention_type,
        'summary': {
            'n_projects': len(deviations),
            'mean_delta_pct': statistics.mean([d['delta_pct'] for d in deviations]) if deviations else 0,
            'overestimates': len([d for d in deviations if d['direction'] == 'overestimate']),
            'underestimates': len([d for d in deviations if d['direction'] == 'underestimate']),
            'accurate': len([d for d in deviations if d['direction'] == 'accurate'])
        }
    }


def extract_all_learnings(registry: Dict) -> Dict:
    """Extract all learnings from completed projects."""
    projects = registry.get('projects', {})
    learnings = {
        'what_worked': [],
        'what_didnt': [],
        'parameter_updates': [],
        'recommendations': []
    }

    for pid, proj in projects.items():
        if proj.get('meta', {}).get('status') != 'completed':
            continue

        proj_learnings = proj.get('learnings', {})

        for item in proj_learnings.get('what_worked', []):
            item['project'] = pid
            learnings['what_worked'].append(item)

        for item in proj_learnings.get('what_didnt', []):
            item['project'] = pid
            learnings['what_didnt'].append(item)

        for item in proj_learnings.get('parameter_updates', []):
            item['project'] = pid
            learnings['parameter_updates'].append(item)

        for item in proj_learnings.get('recommendations', []):
            item['project'] = pid
            learnings['recommendations'].append(item)

    return learnings


def format_project_summary(pid: str, proj: Dict) -> str:
    """Format a brief project summary."""
    meta = proj.get('meta', {})
    name = meta.get('name', 'Unknown')
    domain = meta.get('domain', 'n/a')
    status = meta.get('status', 'n/a')

    dev = proj.get('deviation_analysis', {}).get('overall', {})
    delta_pct = dev.get('delta_pct', 'n/a')
    direction = dev.get('direction', 'n/a')

    return f"{pid}: {name}\n   Domain: {domain} | Status: {status} | Δ: {delta_pct}% ({direction})"


def format_project_full(pid: str, proj: Dict) -> str:
    """Format a full project display."""
    lines = []
    lines.append("=" * 70)
    lines.append(f"  {pid}: {proj.get('meta', {}).get('name', 'Unknown')}")
    lines.append("=" * 70)

    # Meta
    meta = proj.get('meta', {})
    lines.append(f"\nMETA:")
    lines.append(f"  Client: {meta.get('client')}")
    lines.append(f"  Domain: {meta.get('domain')}")
    lines.append(f"  Period: {meta.get('start_date')} → {meta.get('end_date')}")
    lines.append(f"  Status: {meta.get('status')}")

    # Context
    ctx = proj.get('context', {})
    lines.append(f"\nCONTEXT:")
    lines.append(f"  Target: {ctx.get('target_behavior')}")
    lines.append(f"  Population: {ctx.get('target_population')} (n={ctx.get('sample_size')})")
    lines.append(f"  Baseline: {ctx.get('baseline_behavior')}")
    lines.append(f"  Journey Phase: {ctx.get('journey_phase')}")
    lines.append(f"  Segments:")
    for seg in ctx.get('segments', []):
        lines.append(f"    - {seg['name']}: {seg['proportion']*100:.0f}% (σ={seg['sigma']})")

    # Intervention Mix
    lines.append(f"\nINTERVENTION MIX:")
    for i in proj.get('intervention_mix', []):
        lines.append(f"  {i['id']}: {i['type']}/{i['subtype']}")
        lines.append(f"      {i['description'][:60]}...")
        ec = i.get('expected_contribution', {})
        lines.append(f"      E_i={ec.get('E_i')} (conf={ec.get('confidence')}, src={ec.get('source')})")

    # Complementarity Matrix
    lines.append(f"\nCOMPLEMENTARITY MATRIX:")
    for pair in proj.get('complementarity_matrix', []):
        lines.append(f"  {pair['pair']}: γ={pair['gamma_ij']} ({pair['interaction']})")

    # Predictions
    pred = proj.get('predictions', {})
    pe = pred.get('portfolio_effect', {})
    lines.append(f"\nPREDICTIONS:")
    lines.append(f"  Portfolio Effect: E(P) = {pe.get('E_P')} [{pe.get('CI_lower')}, {pe.get('CI_upper')}]")
    lines.append(f"  KPIs:")
    for kpi in pred.get('kpis', []):
        lines.append(f"    - {kpi['name']}: {kpi.get('baseline')} → {kpi.get('predicted_value')} (Δ={kpi.get('predicted_delta_pct')}%)")

    # Results
    res = proj.get('results', {})
    if res:
        lines.append(f"\nRESULTS (measured {res.get('measurement_date')}):")
        for kpi in res.get('kpis', []):
            lines.append(f"    - {kpi['name']}: {kpi.get('actual_value')} (Δ={kpi.get('actual_delta_pct')}%)")

    # Deviation Analysis
    dev = proj.get('deviation_analysis', {})
    if dev:
        ov = dev.get('overall', {})
        lines.append(f"\nDEVIATION ANALYSIS:")
        lines.append(f"  Overall: Predicted={ov.get('predicted_E_P')} vs Actual={ov.get('actual_E_P')}")
        lines.append(f"           Δ={ov.get('delta')} ({ov.get('delta_pct')}%) → {ov.get('direction')}")

        lines.append(f"\n  By Intervention:")
        for idev in dev.get('by_intervention', []):
            lines.append(f"    {idev['id']}: {idev.get('predicted')} → {idev.get('actual')} (Δ={idev.get('delta')})")
            for cause in idev.get('likely_causes', [])[:2]:
                lines.append(f"        → {cause[:60]}")

        lines.append(f"\n  Root Causes:")
        for rc in dev.get('root_causes', []):
            lines.append(f"    [{rc.get('confidence')}] {rc.get('cause')}")

    # Learnings
    learn = proj.get('learnings', {})
    if learn:
        lines.append(f"\nLEARNINGS:")
        lines.append(f"  What Worked:")
        for item in learn.get('what_worked', []):
            lines.append(f"    ✓ {item.get('intervention')}: {item.get('insight')[:50]}...")

        lines.append(f"  What Didn't:")
        for item in learn.get('what_didnt', []):
            lines.append(f"    ✗ {item.get('intervention')}: {item.get('insight')[:50]}...")

        lines.append(f"\n  Parameter Updates:")
        for pu in learn.get('parameter_updates', []):
            lines.append(f"    • {pu.get('parameter')}: {pu.get('old_value')} → {pu.get('new_value')}")

        lines.append(f"\n  Recommendations:")
        for rec in learn.get('recommendations', []):
            lines.append(f"    [{rec.get('priority')}] [{rec.get('category')}] {rec.get('recommendation')[:50]}...")

    lines.append("")
    return "\n".join(lines)


def format_deviation_report(stats: Dict) -> str:
    """Format deviation analysis report."""
    lines = []
    lines.append("=" * 70)
    lines.append("  DEVIATION ANALYSIS REPORT")
    lines.append("=" * 70)

    summary = stats['summary']
    lines.append(f"\nSUMMARY:")
    lines.append(f"  Projects Analyzed: {summary['n_projects']}")
    lines.append(f"  Mean Deviation: {summary['mean_delta_pct']:.1f}%")
    lines.append(f"  Overestimates: {summary['overestimates']}")
    lines.append(f"  Underestimates: {summary['underestimates']}")
    lines.append(f"  Accurate: {summary['accurate']}")

    lines.append(f"\nBY PROJECT:")
    for dev in stats['overall']:
        direction_symbol = "↑" if dev['direction'] == 'underestimate' else "↓" if dev['direction'] == 'overestimate' else "="
        lines.append(f"  {dev['project']}: {dev['predicted']:.3f} → {dev['actual']:.3f} ({dev['delta_pct']:+.1f}% {direction_symbol})")

    lines.append(f"\nBY INTERVENTION TYPE:")
    for itype, data in stats['by_type'].items():
        if data:
            mean_delta = statistics.mean([d['delta'] for d in data if d['delta'] is not None])
            lines.append(f"  {itype}: mean Δ = {mean_delta:+.3f} (n={len(data)})")

    lines.append("")
    return "\n".join(lines)


def format_learnings_report(learnings: Dict) -> str:
    """Format learnings extraction report."""
    lines = []
    lines.append("=" * 70)
    lines.append("  AGGREGATED LEARNINGS")
    lines.append("=" * 70)

    lines.append(f"\n✓ WHAT WORKED ({len(learnings['what_worked'])} items):")
    for item in learnings['what_worked']:
        gen = "★" if item.get('generalizable') else ""
        lines.append(f"  {gen} [{item['project']}] {item.get('intervention')}: {item.get('insight')}")

    lines.append(f"\n✗ WHAT DIDN'T WORK ({len(learnings['what_didnt'])} items):")
    for item in learnings['what_didnt']:
        avoid = "⚠" if item.get('avoidable') else ""
        lines.append(f"  {avoid} [{item['project']}] {item.get('intervention')}: {item.get('insight')}")

    lines.append(f"\n📊 PARAMETER UPDATES ({len(learnings['parameter_updates'])} items):")
    for item in learnings['parameter_updates']:
        lines.append(f"  [{item['project']}] {item.get('parameter')}")
        lines.append(f"      {item.get('old_value')} → {item.get('new_value')} (basis: {item.get('basis')})")

    lines.append(f"\n💡 RECOMMENDATIONS ({len(learnings['recommendations'])} items):")
    # Group by priority
    high = [r for r in learnings['recommendations'] if r.get('priority') == 'high']
    medium = [r for r in learnings['recommendations'] if r.get('priority') == 'medium']
    low = [r for r in learnings['recommendations'] if r.get('priority') == 'low']

    if high:
        lines.append(f"\n  HIGH PRIORITY:")
        for rec in high:
            lines.append(f"    [{rec.get('category')}] {rec.get('recommendation')}")

    if medium:
        lines.append(f"\n  MEDIUM PRIORITY:")
        for rec in medium:
            lines.append(f"    [{rec.get('category')}] {rec.get('recommendation')}")

    if low:
        lines.append(f"\n  LOW PRIORITY:")
        for rec in low:
            lines.append(f"    [{rec.get('category')}] {rec.get('recommendation')}")

    lines.append("")
    return "\n".join(lines)


def format_parameters_report(registry: Dict) -> str:
    """Format parameter updates report."""
    lines = []
    lines.append("=" * 70)
    lines.append("  PARAMETER UPDATE TRACKER")
    lines.append("=" * 70)

    agg = registry.get('aggregated_learnings', {})

    lines.append(f"\nDACH CONTEXT ADJUSTMENTS:")
    for adj in agg.get('parameter_adjustments', {}).get('DACH_context', []):
        lines.append(f"\n  {adj['parameter']}:")
        lines.append(f"    Literature: {adj['literature_value']}")
        lines.append(f"    Observed:   {adj['observed_DACH']}")
        lines.append(f"    Adjustment: ×{adj['adjustment_factor']}")
        lines.append(f"    Confidence: {adj['confidence']} (n={adj['n_projects']})")

    lines.append(f"\nDESIGN PRINCIPLES DERIVED:")
    for prin in agg.get('design_principles', []):
        lines.append(f"\n  • {prin['principle']}")
        lines.append(f"    Source: {prin['source']}")
        lines.append(f"    Evidence: {prin['evidence']}")

    lines.append(f"\nSEGMENT INSIGHTS:")
    for seg in agg.get('segment_insights', []):
        lines.append(f"\n  {seg['segment']}:")
        lines.append(f"    {seg['insight']}")
        lines.append(f"    σ: literature={seg['literature_sigma']} → observed={seg['observed_sigma']}")

    lines.append("")
    return "\n".join(lines)


def print_stats(registry: Dict):
    """Print registry statistics."""
    projects = registry.get('projects', {})
    metadata = registry.get('metadata', {})

    print("\n" + "=" * 50)
    print("  EBF INTERVENTION REGISTRY STATISTICS")
    print("=" * 50)
    print(f"\nTotal Projects: {len(projects)}")
    print(f"Version: {metadata.get('version', 'unknown')}")

    print("\nStatus Distribution:")
    for status, count in metadata.get('status_distribution', {}).items():
        print(f"  • {status}: {count}")

    print("\nDomains Covered:")
    for domain in metadata.get('domains_covered', []):
        count = len(filter_by_domain(projects, domain))
        print(f"  • {domain}: {count}")

    print("\nIntervention Types Used:")
    for itype in metadata.get('intervention_types_used', []):
        print(f"  • {itype}")

    acc = metadata.get('average_prediction_accuracy', {})
    print(f"\nPrediction Accuracy:")
    print(f"  Mean Deviation: {acc.get('mean_delta_pct')}%")
    print(f"  Range: {acc.get('range')}")

    print(f"\nLearnings Generated:")
    print(f"  Key Learnings: {metadata.get('key_learnings_count')}")
    print(f"  Parameter Updates: {metadata.get('parameter_updates_count')}")
    print(f"  Recommendations: {metadata.get('recommendations_count')}")

    print()


def main():
    parser = argparse.ArgumentParser(
        description='Query and analyze the EBF Intervention Registry',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s PRJ-001                    # Get specific project
  %(prog)s --domain health            # Filter by domain
  %(prog)s --status completed         # Filter by status
  %(prog)s --deviation                # Deviation analysis
  %(prog)s --learnings                # Extract all learnings
  %(prog)s --parameters               # Show parameter updates
  %(prog)s --list-all                 # List all projects
  %(prog)s --stats                    # Show statistics
        """
    )

    parser.add_argument('project_id', nargs='?', help='Specific project ID')
    parser.add_argument('--domain', '-d', help='Filter by domain')
    parser.add_argument('--status', '-s', help='Filter by status')
    parser.add_argument('--deviation', action='store_true', help='Deviation analysis')
    parser.add_argument('--learnings', action='store_true', help='Extract learnings')
    parser.add_argument('--parameters', action='store_true', help='Parameter updates')
    parser.add_argument('--accuracy', action='store_true', help='Prediction accuracy')
    parser.add_argument('--list-all', '-l', action='store_true', help='List all projects')
    parser.add_argument('--stats', action='store_true', help='Show statistics')
    parser.add_argument('--brief', '-b', action='store_true', help='Brief format')
    parser.add_argument('--registry', '-r', help='Path to registry file')

    args = parser.parse_args()

    try:
        registry = load_registry(args.registry)
    except FileNotFoundError:
        print("Error: Intervention registry not found.")
        sys.exit(1)

    projects = registry.get('projects', {})

    # Specific project
    if args.project_id:
        proj = get_project(registry, args.project_id.upper())
        if proj:
            print(format_project_full(args.project_id.upper(), proj))
        else:
            print(f"Project {args.project_id} not found.")
            sys.exit(1)
        return

    # Stats
    if args.stats:
        print_stats(registry)
        return

    # Deviation analysis
    if args.deviation or args.accuracy:
        stats = calculate_deviation_stats(projects)
        print(format_deviation_report(stats))
        return

    # Learnings
    if args.learnings:
        learnings = extract_all_learnings(registry)
        print(format_learnings_report(learnings))
        return

    # Parameters
    if args.parameters:
        print(format_parameters_report(registry))
        return

    # Filters
    results = projects.copy()

    if args.domain:
        results = filter_by_domain(results, args.domain)

    if args.status:
        results = filter_by_status(results, args.status)

    # List
    if args.list_all or results != projects:
        print(f"\n{'='*60}")
        print(f"  PROJECTS ({len(results)} found)")
        print(f"{'='*60}\n")
        for pid, proj in results.items():
            if args.brief:
                print(format_project_summary(pid, proj))
            else:
                print(format_project_full(pid, proj))
        return

    # Default: show stats
    print_stats(registry)


if __name__ == '__main__':
    main()
