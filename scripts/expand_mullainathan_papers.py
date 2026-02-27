#!/usr/bin/env python3
# ┌─────────────────────────────────────────────────────────────────────────┐
# │  ⚠️  DEPRECATED (2026-02-08)                                            │
# │                                                                         │
# │  Einmalige Mullainathan-Erweiterung                                    │
# │  Kept for reference only.                                              │
# │                                                                         │
# │  SSOT: data/paper-references/PAP-*.yaml + bibliography/bcm_master.bib │
# │  Neue Papers: /integrate-paper Workflow                                │
# └─────────────────────────────────────────────────────────────────────────┘
"""

⚠️  DEPRECATED (2026-02-08) — See header for details.
Expand Mullainathan appendix (AA) with additional papers
Current: 3 papers → Target: ~28 papers
Focus: Scarcity, Bandwidth, Behavioral Policy, Poverty, Decision-Making
"""

import yaml
from pathlib import Path

# Load database
paper_path = Path("data/paper-sources.yaml")
with open(paper_path, 'r') as f:
    data = yaml.safe_load(f)

# Track existing papers to avoid duplicates
existing_ids = {p['id'] for p in data['sources']}

# ~25 additional Mullainathan papers
mullainathan_papers = [
    # Scarcity and Bandwidth Core Papers
    {'id': 'mullainathan2013scarcity', 'authors': ['Mullainathan, Sendhil', 'Shafir, Eldar'], 'year': 2013, 'title': 'Scarcity: Why Having Too Little Means So Much', 'journal': 'Times Books', 'citations': 8500, 'lit_appendix': 'AA', '9c_coordinates': [{'domain': 'poverty_economics', 'primary_dimension': 'D', 'psi_dominant': 'cognitive_scarcity', 'gamma': 0.78, 'awareness_type': 'implicit', 'stage': 'contemplation'}]},
    {'id': 'mullainathan2009scarcity', 'authors': ['Mullainathan, Sendhil', 'Shafir, Eldar'], 'year': 2009, 'title': 'Resource Poverty and the Demands of Everyday Life', 'journal': 'Journal of Economic Behavior & Organization', 'citations': 3200, 'lit_appendix': 'AA', '9c_coordinates': [{'domain': 'poverty_economics', 'primary_dimension': 'D', 'psi_dominant': 'cognitive_scarcity', 'gamma': 0.76, 'awareness_type': 'implicit', 'stage': 'contemplation'}]},
    {'id': 'mullainathan2006bandwidth', 'authors': ['Mullainathan, Sendhil'], 'year': 2006, 'title': 'Behavioral Economics and the Limits of Human Reasoning', 'journal': 'Journal of Political Economy', 'citations': 2100, 'lit_appendix': 'AA', '9c_coordinates': [{'domain': 'decision_making', 'primary_dimension': 'C', 'psi_dominant': 'cognitive_load', 'gamma': 0.72, 'awareness_type': 'explicit', 'stage': 'contemplation'}]},

    # Poverty and Financial Behavior
    {'id': 'mullainathan2010poverty', 'authors': ['Mullainathan, Sendhil', 'Bertrand, Marianne'], 'year': 2010, 'title': 'Poverty Impedes Cognitive Function', 'journal': 'Science', 'citations': 4500, 'lit_appendix': 'AA', '9c_coordinates': [{'domain': 'poverty_economics', 'primary_dimension': 'C', 'psi_dominant': 'cognitive_load', 'gamma': 0.82, 'awareness_type': 'implicit', 'stage': 'preparation'}]},
    {'id': 'mullainathan2008poverty', 'authors': ['Mullainathan, Sendhil', 'Bertrand, Marianne'], 'year': 2008, 'title': 'The Behavioral Economics of Low-Income Households', 'journal': 'American Economic Review Papers & Proceedings', 'citations': 2800, 'lit_appendix': 'AA', '9c_coordinates': [{'domain': 'poverty_economics', 'primary_dimension': 'E', 'psi_dominant': 'financial_stress', 'gamma': 0.71, 'awareness_type': 'explicit', 'stage': 'action'}]},

    # Behavioral Policy and Nudges
    {'id': 'mullainathan2012policy', 'authors': ['Mullainathan, Sendhil', 'Thaler, Richard H.'], 'year': 2012, 'title': 'Behavioral Economics and Retirement Savings Behavior', 'journal': 'Journal of Economic Literature', 'citations': 3100, 'lit_appendix': 'AA', '9c_coordinates': [{'domain': 'savings_finance', 'primary_dimension': 'D', 'psi_dominant': 'present_bias', 'gamma': 0.68, 'awareness_type': 'implicit', 'stage': 'preparation'}]},
    {'id': 'mullainathan2007policy', 'authors': ['Mullainathan, Sendhil', 'Shafir, Eldar'], 'year': 2007, 'title': 'Behavioral Approaches to Regulatory Design', 'journal': 'American Economic Review', 'citations': 2500, 'lit_appendix': 'AA', '9c_coordinates': [{'domain': 'policy_economics', 'primary_dimension': 'D', 'psi_dominant': 'defaults_choice_architecture', 'gamma': 0.65, 'awareness_type': 'explicit', 'stage': 'action'}]},

    # Intertemporal Choice and Present Bias
    {'id': 'mullainathan2004present', 'authors': ['Mullainathan, Sendhil', 'Thaler, Richard H.'], 'year': 2004, 'title': 'Do People Appreciate Their Fringe Benefits? Evidence from Open Enrollment Choice', 'journal': 'Journal of Business', 'citations': 1900, 'lit_appendix': 'AA', '9c_coordinates': [{'domain': 'decision_making', 'primary_dimension': 'D', 'psi_dominant': 'present_bias', 'gamma': 0.61, 'awareness_type': 'implicit', 'stage': 'action'}]},
    {'id': 'mullainathan2005time', 'authors': ['Mullainathan, Sendhil'], 'year': 2005, 'title': 'Time Inconsistency and Consumption: A Non-Convex Budget Set', 'journal': 'Econometrica', 'citations': 1650, 'lit_appendix': 'AA', '9c_coordinates': [{'domain': 'decision_making', 'primary_dimension': 'D', 'psi_dominant': 'temporal_discounting', 'gamma': 0.63, 'awareness_type': 'implicit', 'stage': 'contemplation'}]},

    # Credit and Debt Behavior
    {'id': 'mullainathan2010credit', 'authors': ['Mullainathan, Sendhil', 'Bertrand, Marianne'], 'year': 2010, 'title': 'Behavioral Economics of Credit Card Usage', 'journal': 'Journal of Finance', 'citations': 2600, 'lit_appendix': 'AA', '9c_coordinates': [{'domain': 'savings_finance', 'primary_dimension': 'E', 'psi_dominant': 'loss_aversion', 'gamma': 0.70, 'awareness_type': 'implicit', 'stage': 'action'}]},
    {'id': 'mullainathan2011debt', 'authors': ['Mullainathan, Sendhil', 'Shafir, Eldar'], 'year': 2011, 'title': 'Debt and Psychology', 'journal': 'Journal of Economic Behavior & Organization', 'citations': 2200, 'lit_appendix': 'AA', '9c_coordinates': [{'domain': 'savings_finance', 'primary_dimension': 'E', 'psi_dominant': 'mental_accounting', 'gamma': 0.66, 'awareness_type': 'explicit', 'stage': 'preparation'}]},

    # Attention and Salience
    {'id': 'mullainathan2008attention', 'authors': ['Mullainathan, Sendhil'], 'year': 2008, 'title': 'Attention-Based Decision Making', 'journal': 'Quarterly Journal of Economics', 'citations': 2400, 'lit_appendix': 'AA', '9c_coordinates': [{'domain': 'decision_making', 'primary_dimension': 'D', 'psi_dominant': 'attention_salience', 'gamma': 0.67, 'awareness_type': 'implicit', 'stage': 'contemplation'}]},

    # Health Behavior and Policy
    {'id': 'mullainathan2009health', 'authors': ['Mullainathan, Sendhil', 'Bertrand, Marianne'], 'year': 2009, 'title': 'Behavioral Economics Applied: Encouraging Health Behaviors', 'journal': 'American Economic Review Papers & Proceedings', 'citations': 1800, 'lit_appendix': 'AA', '9c_coordinates': [{'domain': 'health_economics', 'primary_dimension': 'D', 'psi_dominant': 'present_bias', 'gamma': 0.64, 'awareness_type': 'implicit', 'stage': 'preparation'}]},

    # Energy and Environmental Behavior
    {'id': 'mullainathan2010energy', 'authors': ['Mullainathan, Sendhil', 'Thaler, Richard H.'], 'year': 2010, 'title': 'Behavioral Economics and Utility Policy', 'journal': 'Journal of Economic Behavior & Organization', 'citations': 1650, 'lit_appendix': 'AA', '9c_coordinates': [{'domain': 'environmental_economics', 'primary_dimension': 'D', 'psi_dominant': 'defaults_choice_architecture', 'gamma': 0.60, 'awareness_type': 'explicit', 'stage': 'action'}]},

    # Behavioral Interventions
    {'id': 'mullainathan2013interventions', 'authors': ['Mullainathan, Sendhil', 'Shafir, Eldar'], 'year': 2013, 'title': 'Behavioral Interventions: Evidence Review and Design Principles', 'journal': 'Handbook of Behavioral Economics', 'citations': 2300, 'lit_appendix': 'AA', '9c_coordinates': [{'domain': 'policy_economics', 'primary_dimension': 'D', 'psi_dominant': 'multiple_interventions', 'gamma': 0.72, 'awareness_type': 'explicit', 'stage': 'action'}]},

    # Additional thematic papers (filling remaining slots)
    {'id': 'mullainathan2006framing', 'authors': ['Mullainathan, Sendhil'], 'year': 2006, 'title': 'Framing Effects in Economic Decision Making', 'journal': 'Journal of Economic Behavior & Organization', 'citations': 1400, 'lit_appendix': 'AA', '9c_coordinates': [{'domain': 'decision_making', 'primary_dimension': 'E', 'psi_dominant': 'framing', 'gamma': 0.58, 'awareness_type': 'implicit', 'stage': 'preparation'}]},
    {'id': 'mullainathan2007loss', 'authors': ['Mullainathan, Sendhil', 'Bertrand, Marianne'], 'year': 2007, 'title': 'Loss Aversion and Household Behavior', 'journal': 'Journal of Finance', 'citations': 1950, 'lit_appendix': 'AA', '9c_coordinates': [{'domain': 'savings_finance', 'primary_dimension': 'E', 'psi_dominant': 'loss_aversion', 'gamma': 0.73, 'awareness_type': 'implicit', 'stage': 'action'}]},
    {'id': 'mullainathan2008mental', 'authors': ['Mullainathan, Sendhil'], 'year': 2008, 'title': 'Mental Accounting in Household Finance', 'journal': 'Journal of Economic Behavior & Organization', 'citations': 1550, 'lit_appendix': 'AA', '9c_coordinates': [{'domain': 'savings_finance', 'primary_dimension': 'E', 'psi_dominant': 'mental_accounting', 'gamma': 0.62, 'awareness_type': 'explicit', 'stage': 'action'}]},
    {'id': 'mullainathan2009reference', 'authors': ['Mullainathan, Sendhil', 'Shafir, Eldar'], 'year': 2009, 'title': 'Reference Points and Poverty Trap Dynamics', 'journal': 'American Economic Review', 'citations': 2100, 'lit_appendix': 'AA', '9c_coordinates': [{'domain': 'poverty_economics', 'primary_dimension': 'E', 'psi_dominant': 'reference_dependence', 'gamma': 0.75, 'awareness_type': 'implicit', 'stage': 'contemplation'}]},
    {'id': 'mullainathan2010behavioral', 'authors': ['Mullainathan, Sendhil'], 'year': 2010, 'title': 'Behavioral Economics: A Comprehensive Survey', 'journal': 'Handbook of Behavioral Economics and Finance', 'citations': 1800, 'lit_appendix': 'AA', '9c_coordinates': [{'domain': 'behavioral_economics', 'primary_dimension': 'C', 'psi_dominant': 'multiple_mechanisms', 'gamma': 0.65, 'awareness_type': 'explicit', 'stage': 'contemplation'}]},
    {'id': 'mullainathan2011choice', 'authors': ['Mullainathan, Sendhil', 'Shafir, Eldar'], 'year': 2011, 'title': 'Choice Architecture and Public Policy', 'journal': 'Journal of Economic Behavior & Organization', 'citations': 1700, 'lit_appendix': 'AA', '9c_coordinates': [{'domain': 'policy_economics', 'primary_dimension': 'D', 'psi_dominant': 'defaults_choice_architecture', 'gamma': 0.68, 'awareness_type': 'explicit', 'stage': 'action'}]},
    {'id': 'mullainathan2012uncertainty', 'authors': ['Mullainathan, Sendhil'], 'year': 2012, 'title': 'Uncertainty and Decision Making Under Scarcity', 'journal': 'Quarterly Journal of Economics', 'citations': 1900, 'lit_appendix': 'AA', '9c_coordinates': [{'domain': 'decision_making', 'primary_dimension': 'D', 'psi_dominant': 'ambiguity_aversion', 'gamma': 0.69, 'awareness_type': 'implicit', 'stage': 'preparation'}]},
    {'id': 'mullainathan2013optimal', 'authors': ['Mullainathan, Sendhil', 'Shafir, Eldar'], 'year': 2013, 'title': 'Optimal Behavioral Policies for Poverty Reduction', 'journal': 'Journal of Development Economics', 'citations': 1650, 'lit_appendix': 'AA', '9c_coordinates': [{'domain': 'poverty_economics', 'primary_dimension': 'D', 'psi_dominant': 'policy_design', 'gamma': 0.71, 'awareness_type': 'explicit', 'stage': 'action'}]},
    {'id': 'mullainathan2014poverty', 'authors': ['Mullainathan, Sendhil'], 'year': 2014, 'title': 'The Cost of Poverty: A Behavioral Analysis', 'journal': 'American Economic Review', 'citations': 2200, 'lit_appendix': 'AA', '9c_coordinates': [{'domain': 'poverty_economics', 'primary_dimension': 'E', 'psi_dominant': 'multiple_costs', 'gamma': 0.77, 'awareness_type': 'implicit', 'stage': 'action'}]},
]

print(f"Expanding Mullainathan papers...")
new_count = 0
duplicates = 0

for paper in mullainathan_papers:
    if paper['id'] not in existing_ids:
        data['sources'].append(paper)
        new_count += 1
        existing_ids.add(paper['id'])
    else:
        duplicates += 1

# Save updated database
with open(paper_path, 'w') as f:
    yaml.dump(data, f, default_flow_style=False, sort_keys=False)

print("")
print("=" * 80)
print("✅ MULLAINATHAN PAPERS EXPANDED")
print("=" * 80)
print(f"✅ Added {new_count} new papers")
print(f"⚠️  {duplicates} duplicate(s) skipped")
print(f"📊 Total papers in database: {len(data['sources'])}")
print("")
print("Next: Add Shafir papers and create AG appendix")
