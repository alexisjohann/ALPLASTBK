#!/usr/bin/env python3
"""
Phase 5: Learnings Extractor - Extract Insights & Parameter Updates

Purpose: Extract what worked/didn't work, update parameters, generate recommendations
Input: Project with deviation analysis
Output: Learnings, parameter updates, recommendations for next projects
"""

import yaml
from pathlib import Path
from collections import defaultdict

# Load intervention registry
intervention_path = Path("data/intervention-registry.yaml")

with open(intervention_path, 'r') as f:
    intervention_data = yaml.safe_load(f)

projects = intervention_data.get('projects', {})

print("=" * 80)
print("PHASE 5: LEARNINGS EXTRACTION & PARAMETER UPDATES")
print("=" * 80)
print()

def extract_what_worked(project):
    """
    Identify successful intervention components
    """
    learnings = project.get('learnings', {})
    what_worked = learnings.get('what_worked', [])

    return what_worked

def extract_what_didnt(project):
    """
    Identify unsuccessful components and causes
    """
    learnings = project.get('learnings', {})
    what_didnt = learnings.get('what_didnt', [])

    return what_didnt

def calculate_parameter_updates(project):
    """
    Generate parameter updates based on actual vs predicted performance
    """
    learnings = project.get('learnings', {})
    param_updates = learnings.get('parameter_updates', [])

    return param_updates

def extract_segment_insights(project):
    """
    Extract insights about differential segment response
    """
    deviation = project.get('deviation_analysis', {})
    by_segment = deviation.get('by_segment', [])

    insights = []

    for seg in by_segment:
        segment = seg.get('segment')
        predicted = seg.get('predicted_response', 0)
        actual = seg.get('actual_response', 0)
        delta = actual - predicted

        if delta > 0.05:  # Overperformed
            insights.append({
                'type': 'overperformance',
                'segment': segment,
                'delta': delta,
                'insight': f"{segment} responded better than expected (Δ={delta:+.1%})",
                'actionable': f"Target this segment more heavily in similar future projects"
            })
        elif delta < -0.05:  # Underperformed
            insights.append({
                'type': 'underperformance',
                'segment': segment,
                'delta': delta,
                'insight': f"{segment} responded worse than expected (Δ={delta:+.1%})",
                'actionable': f"Adjust intervention timing/design for this segment"
            })

    return insights

def generate_recommendations(project):
    """
    Generate actionable recommendations for future projects
    """
    learnings = project.get('learnings', {})
    recommendations = learnings.get('recommendations', [])

    return recommendations

def identify_generalizable_patterns(completed_projects):
    """
    Identify patterns across multiple projects for meta-learning
    """
    if not completed_projects:
        return []

    patterns = defaultdict(list)

    # Aggregate insights across projects
    for project_id, project in completed_projects:
        interventions = project.get('intervention_mix', [])
        meta = project.get('meta', {})

        for intervention in interventions:
            int_type = intervention.get('type')
            domain = meta.get('domain')

            # Get actual performance if available
            results = project.get('results', {})
            effects = results.get('intervention_effects', [])
            actual = next((e for e in effects if e.get('id') == intervention.get('id')), None)

            if actual:
                patterns[f"{int_type}_{domain}"].append({
                    'project': project_id,
                    'predicted': intervention.get('expected_contribution', {}).get('E_i', 0),
                    'actual': actual.get('observed_E_i', 0)
                })

    # Calculate aggregate statistics
    aggregated = {}
    for key, values in patterns.items():
        if values:
            avg_predicted = sum(v['predicted'] for v in values) / len(values)
            avg_actual = sum(v['actual'] for v in values) / len(values)
            delta = avg_actual - avg_predicted

            aggregated[key] = {
                'projects': len(values),
                'avg_predicted': round(avg_predicted, 3),
                'avg_actual': round(avg_actual, 3),
                'avg_delta': round(delta, 3),
                'pattern': 'consistent_overestimate' if delta < -0.05 else
                           'consistent_underestimate' if delta > 0.05 else
                           'well_calibrated'
            }

    return aggregated

def generate_learning_report(project_id):
    """
    Generate comprehensive learnings report for a project
    """
    if project_id not in projects:
        print(f"Error: Project {project_id} not found")
        return

    project = projects[project_id]

    # Check if project has learnings
    if not project.get('learnings'):
        print(f"Project {project_id} has no learnings extracted yet")
        return

    meta = project.get('meta', {})
    learnings = project.get('learnings', {})

    print(f"PROJECT: {project_id}")
    print(f"Name: {meta.get('name')}")
    print(f"Domain: {meta.get('domain')}")
    print()

    # What worked
    what_worked = extract_what_worked(project)
    if what_worked:
        print("✓ WHAT WORKED")
        print("-" * 80)
        for item in what_worked:
            print(f"  • {item.get('intervention')}")
            print(f"    {item.get('insight')}")
            if item.get('generalizable'):
                print(f"    💡 GENERALIZABLE: Can apply to other domains/segments")
        print()

    # What didn't work
    what_didnt = extract_what_didnt(project)
    if what_didnt:
        print("✗ WHAT DIDN'T WORK")
        print("-" * 80)
        for item in what_didnt:
            print(f"  • {item.get('intervention')}")
            print(f"    {item.get('insight')}")
            if item.get('avoidable'):
                print(f"    ⚠️  AVOIDABLE: Design better for next time")
        print()

    # Parameter updates
    param_updates = calculate_parameter_updates(project)
    if param_updates:
        print("📊 PARAMETER UPDATES (for BBB Repository)")
        print("-" * 80)
        for update in param_updates:
            old = update.get('old_value')
            new = update.get('new_value')
            change = ((new - old) / old * 100) if old else 0
            print(f"  • {update.get('parameter')}")
            print(f"    {old:.3f} → {new:.3f} ({change:+.1f}%)")
            print(f"    Basis: {update.get('basis')}")
        print()

    # Recommendations
    recommendations = generate_recommendations(project)
    if recommendations:
        print("💡 RECOMMENDATIONS FOR NEXT PROJECTS")
        print("-" * 80)
        for rec in recommendations:
            priority = rec.get('priority', 'medium').upper()
            print(f"  [{priority}] {rec.get('category').upper()}")
            print(f"       {rec.get('recommendation')}")
        print()

    # Segment insights
    segment_insights = extract_segment_insights(project)
    if segment_insights:
        print("👥 SEGMENT INSIGHTS")
        print("-" * 80)
        for insight in segment_insights:
            print(f"  • {insight.get('insight')}")
            print(f"    Action: {insight.get('actionable')}")
        print()

    print("=" * 80)

# MAIN: Analyze completed projects
print("COMPLETED PROJECTS WITH LEARNINGS")
print("-" * 80)

completed_projects = [
    (pid, p) for pid, p in projects.items()
    if p.get('meta', {}).get('status') == 'completed'
]

if completed_projects:
    for i, (pid, project) in enumerate(completed_projects):
        has_learnings = bool(project.get('learnings'))
        status = "✓" if has_learnings else "✗"
        print(f"{status} {pid}: {project.get('meta', {}).get('name')}")

    print()
    print("=" * 80)
    print("DETAILED LEARNING REPORTS")
    print("=" * 80)
    print()

    # Generate reports for first completed project with learnings
    with_learnings = [p for p in completed_projects if p[1].get('learnings')]
    if with_learnings:
        for project_id, _ in with_learnings[:2]:  # Show first 2
            generate_learning_report(project_id)
            print()
    else:
        print("Note: No projects have learnings extracted yet")
        print()

    # Meta-learning analysis
    print("=" * 80)
    print("META-LEARNING: PATTERNS ACROSS PROJECTS")
    print("=" * 80)
    print()

    patterns = identify_generalizable_patterns(completed_projects)

    if patterns:
        print("INTERVENTION EFFECTIVENESS BY DOMAIN")
        print("-" * 80)
        for pattern, stats in sorted(patterns.items()):
            print(f"{pattern} ({stats['projects']} projects)")
            print(f"  Predicted avg: {stats['avg_predicted']:.2f}")
            print(f"  Actual avg:    {stats['avg_actual']:.2f}")
            print(f"  Status:        {stats['pattern'].upper()}")
        print()
    else:
        print("No patterns identified yet (need more projects)")
        print()

else:
    print("No completed projects found")
    print()

print()
print("=" * 80)
print("✅ PHASE 5 LEARNINGS EXTRACTION: COMPLETE")
print("=" * 80)

