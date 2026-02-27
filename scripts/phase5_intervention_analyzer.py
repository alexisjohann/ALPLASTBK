#!/usr/bin/env python3
"""
Phase 5: Intervention Analysis - Deviation Analysis & Outcome Measurement

Purpose: Compare predicted vs actual outcomes, identify root causes, extract learnings
Input: Completed project with measurement results
Output: Comprehensive deviation analysis and recommendations
"""

import yaml
from pathlib import Path
from collections import defaultdict
import math

# Load intervention registry
intervention_path = Path("data/intervention-registry.yaml")

with open(intervention_path, 'r') as f:
    intervention_data = yaml.safe_load(f)

projects = intervention_data.get('projects', {})

print("=" * 80)
print("PHASE 5: INTERVENTION ANALYSIS & DEVIATION ANALYSIS")
print("=" * 80)
print()

def analyze_overall_deviation(project):
    """
    Compare predicted portfolio effect to actual results
    """
    predictions = project.get('predictions', {})
    results = project.get('results', {})

    if not predictions or not results:
        return None

    portfolio_pred = predictions.get('portfolio_effect', {})
    E_P_predicted = portfolio_pred.get('E_P', 0)

    # Calculate actual portfolio effect from KPI results
    kpis_pred = predictions.get('kpis', [])
    kpis_actual = results.get('kpis', [])

    if not kpis_pred or not kpis_actual:
        return None

    # Match baseline and actual for first KPI
    kpi_pred = kpis_pred[0]
    kpi_actual = next((k for k in kpis_actual if k['name'] == kpi_pred['name']), None)

    if not kpi_actual:
        return None

    baseline = kpi_pred.get('baseline', 0)
    predicted_value = kpi_pred.get('predicted_value', 0)
    actual_value = kpi_actual.get('actual_value', 0)

    # Calculate actual effect
    if baseline == 0:
        return None

    E_P_actual = (actual_value - baseline) / (1 - baseline) if baseline < 1 else 0

    # Deviation analysis
    delta = E_P_actual - E_P_predicted
    delta_pct = (delta / E_P_predicted * 100) if E_P_predicted != 0 else 0

    direction = 'overestimate' if delta < 0 else 'underestimate' if delta > 0 else 'accurate'

    return {
        'E_P_predicted': round(E_P_predicted, 3),
        'E_P_actual': round(E_P_actual, 3),
        'delta': round(delta, 3),
        'delta_pct': round(delta_pct, 1),
        'direction': direction,
        'accuracy_margin': '±20%' if abs(delta_pct) <= 20 else '±30%' if abs(delta_pct) <= 30 else '>30%'
    }

def analyze_by_intervention(project):
    """
    Analyze how each intervention component performed
    """
    interventions = project.get('intervention_mix', [])
    results = project.get('results', {})

    if not interventions or not results:
        return []

    actual_effects = results.get('intervention_effects', [])

    analysis = []
    for intervention in interventions:
        int_id = intervention.get('id')
        E_i_predicted = intervention.get('expected_contribution', {}).get('E_i', 0)

        actual_effect = next((a for a in actual_effects if a.get('id') == int_id), None)
        E_i_actual = actual_effect.get('observed_E_i', 0) if actual_effect else None

        if E_i_actual is not None:
            delta = E_i_actual - E_i_predicted
            delta_pct = (delta / E_i_predicted * 100) if E_i_predicted != 0 else 0

            analysis.append({
                'id': int_id,
                'type': intervention.get('type'),
                'E_i_predicted': round(E_i_predicted, 3),
                'E_i_actual': round(E_i_actual, 3),
                'delta': round(delta, 3),
                'delta_pct': round(delta_pct, 1),
                'direction': 'better' if delta > 0 else 'worse' if delta < 0 else 'as_expected',
                'confidence': actual_effect.get('attribution_confidence', 0.5) if actual_effect else 0.5
            })

    return sorted(analysis, key=lambda x: x['delta'], reverse=True)

def analyze_by_segment(project):
    """
    Analyze differential response rates across segments
    """
    context = project.get('context', {})
    results = project.get('results', {})

    segments = context.get('segments', [])
    segment_analysis = results.get('deviation_analysis', {}).get('by_segment', [])

    analysis = []
    for seg_analysis in segment_analysis:
        segment_name = seg_analysis.get('segment')
        predicted = seg_analysis.get('predicted_response', 0)
        actual = seg_analysis.get('actual_response', 0)
        delta = actual - predicted

        # Find segment metadata
        seg_meta = next((s for s in segments if s.get('name') == segment_name), None)
        proportion = seg_meta.get('proportion', 0) if seg_meta else 0

        analysis.append({
            'segment': segment_name,
            'proportion': round(proportion, 2),
            'predicted_response': round(predicted, 3),
            'actual_response': round(actual, 3),
            'delta': round(delta, 3),
            'overperformed': delta > 0
        })

    return sorted(analysis, key=lambda x: x['delta'], reverse=True)

def identify_root_causes(project):
    """
    Extract root causes for deviations
    """
    overall = project.get('deviation_analysis', {}).get('overall', {})
    by_intervention = project.get('deviation_analysis', {}).get('by_intervention', [])

    root_causes = overall.get('root_causes', [])

    return root_causes

def generate_deviation_report(project_id):
    """
    Generate comprehensive deviation analysis
    """
    if project_id not in projects:
        print(f"Error: Project {project_id} not found")
        return

    project = projects[project_id]

    # Check if project has results
    if not project.get('results'):
        print(f"Project {project_id} has no results yet (status: {project.get('meta', {}).get('status')})")
        return

    print(f"PROJECT: {project_id}")
    print(f"Name: {project.get('meta', {}).get('name')}")
    print(f"Status: {project.get('meta', {}).get('status')}")
    print()

    # Overall analysis
    overall_analysis = analyze_overall_deviation(project)
    if overall_analysis:
        print("OVERALL DEVIATION ANALYSIS")
        print("-" * 80)
        print(f"Predicted portfolio effect (E_P):  {overall_analysis['E_P_predicted']:.1%}")
        print(f"Actual portfolio effect:          {overall_analysis['E_P_actual']:.1%}")
        print(f"Deviation:                        {overall_analysis['delta']:+.1%} ({overall_analysis['delta_pct']:+.1f}%)")
        print(f"Direction:                        {overall_analysis['direction'].upper()}")
        print(f"Accuracy:                         {overall_analysis['accuracy_margin']}")
        print()

    # By intervention analysis
    by_intervention = analyze_by_intervention(project)
    if by_intervention:
        print("BY INTERVENTION ANALYSIS")
        print("-" * 80)
        for analysis in by_intervention:
            status = "✓" if analysis['direction'] == 'better' else "✗" if analysis['direction'] == 'worse' else "="
            print(f"{status} {analysis['id']} ({analysis['type']})")
            print(f"   Predicted E_i: {analysis['E_i_predicted']:.2f}, Actual: {analysis['E_i_actual']:.2f}")
            print(f"   Delta: {analysis['delta']:+.3f} ({analysis['delta_pct']:+.1f}%)")
            print(f"   Attribution confidence: {analysis['confidence']:.0%}")
        print()

    # By segment analysis
    by_segment = analyze_by_segment(project)
    if by_segment:
        print("BY SEGMENT ANALYSIS")
        print("-" * 80)
        for analysis in by_segment:
            symbol = "↑" if analysis['overperformed'] else "↓"
            print(f"{symbol} {analysis['segment']} ({analysis['proportion']:.0%} of population)")
            print(f"   Predicted: {analysis['predicted_response']:.1%}, Actual: {analysis['actual_response']:.1%}")
            print(f"   Delta: {analysis['delta']:+.1%}")
        print()

    # Root causes
    root_causes = identify_root_causes(project)
    if root_causes:
        print("ROOT CAUSES")
        print("-" * 80)
        for cause in root_causes:
            confidence = cause.get('confidence', 'unknown')
            print(f"({confidence.upper()}) {cause.get('cause')}")
            print(f"      Evidence: {cause.get('evidence')}")
        print()

    print("=" * 80)

# MAIN: List completed projects and analyze one
print("AVAILABLE PROJECTS")
print("-" * 80)

completed_projects = [
    (pid, p) for pid, p in projects.items()
    if p.get('meta', {}).get('status') == 'completed'
]

if completed_projects:
    for i, (pid, project) in enumerate(completed_projects):
        print(f"{i+1}. {pid}: {project.get('meta', {}).get('name')}")
        measurement = project.get('results', {}).get('measurement_date', 'N/A')
        print(f"   Measurement date: {measurement}")

    print()
    print("Analyzing first completed project...")
    print()

    analyze_project_id = completed_projects[0][0]
    generate_deviation_report(analyze_project_id)
else:
    print("No completed projects with results found")
    print()
    print("Note: Projects must have:")
    print("  - status: completed")
    print("  - results section with actual KPIs")
    print("  - deviation_analysis with predicted vs actual")
    print()

print()
print("=" * 80)
print("✅ PHASE 5 INTERVENTION ANALYSIS: COMPLETE")
print("=" * 80)

