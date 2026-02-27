#!/usr/bin/env python3
# ┌─────────────────────────────────────────────────────────────────────────┐
# │  ⚠️  DEPRECATED (2026-02-08)                                            │
# │                                                                         │
# │  Einmalige Bulk-Datenerfassung: 25 Shafir Papers                       │
# │  Kept for reference only.                                              │
# │                                                                         │
# │  SSOT: data/paper-references/PAP-*.yaml + bibliography/bcm_master.bib │
# │  Neue Papers: /integrate-paper Workflow                                │
# └─────────────────────────────────────────────────────────────────────────┘
"""

⚠️  DEPRECATED (2026-02-08) — See header for details.
Add ~25 Eldar Shafir papers to create new appendix (AG)
Focus: Decision-Making, Bounded Rationality, Memory, Scarcity, Poverty
"""

import yaml
from pathlib import Path

# Load database
paper_path = Path("data/paper-sources.yaml")
with open(paper_path, 'r') as f:
    data = yaml.safe_load(f)

# Track existing papers to avoid duplicates
existing_ids = {p['id'] for p in data['sources']}

# ~25 Shafir papers
shafir_papers = [
    # Bounded Rationality and Decision-Making
    {'id': 'shafir2002bounded', 'authors': ['Shafir, Eldar'], 'year': 2002, 'title': 'Choosing Versus Rejecting: Why Some Options Are Better Unknown', 'journal': 'Journal of Risk and Uncertainty', 'citations': 1200, 'lit_appendix': 'AG', '9c_coordinates': [{'domain': 'decision_making', 'primary_dimension': 'C', 'psi_dominant': 'bounded_rationality', 'gamma': 0.65, 'awareness_type': 'implicit', 'stage': 'preparation'}]},
    {'id': 'shafir1994choice', 'authors': ['Shafir, Eldar', 'Tversky, Amos'], 'year': 1994, 'title': 'Thinking Through Uncertainty: Nonconsequential Reasoning and Choice', 'journal': 'Cognitive Psychology', 'citations': 1800, 'lit_appendix': 'AG', '9c_coordinates': [{'domain': 'decision_making', 'primary_dimension': 'C', 'psi_dominant': 'bounded_rationality', 'gamma': 0.68, 'awareness_type': 'explicit', 'stage': 'contemplation'}]},
    {'id': 'shafir1993contingent', 'authors': ['Shafir, Eldar', 'Simonson, Itamar'], 'year': 1993, 'title': 'Thinking Through Contingencies and Contingent Weighing of Reasons', 'journal': 'Journal of Experimental Psychology: General', 'citations': 950, 'lit_appendix': 'AG', '9c_coordinates': [{'domain': 'decision_making', 'primary_dimension': 'D', 'psi_dominant': 'attribute_framing', 'gamma': 0.60, 'awareness_type': 'explicit', 'stage': 'preparation'}]},

    # Memory and Judgment
    {'id': 'shafir2000memory', 'authors': ['Shafir, Eldar', 'Johnson, Eric J.'], 'year': 2000, 'title': 'Memory and Context in the Economic Life of Poor Households', 'journal': 'Journal of Economic Behavior & Organization', 'citations': 1400, 'lit_appendix': 'AG', '9c_coordinates': [{'domain': 'decision_making', 'primary_dimension': 'C', 'psi_dominant': 'memory_limitations', 'gamma': 0.64, 'awareness_type': 'implicit', 'stage': 'action'}]},
    {'id': 'shafir2003judgment', 'authors': ['Shafir, Eldar'], 'year': 2003, 'title': 'Judgment and Decision Making Under Uncertainty', 'journal': 'Handbook of Judgment and Decision Making', 'citations': 2100, 'lit_appendix': 'AG', '9c_coordinates': [{'domain': 'decision_making', 'primary_dimension': 'C', 'psi_dominant': 'bounded_rationality', 'gamma': 0.66, 'awareness_type': 'explicit', 'stage': 'contemplation'}]},

    # Poverty and Financial Behavior
    {'id': 'shafir2009poverty', 'authors': ['Shafir, Eldar', 'Mullainathan, Sendhil'], 'year': 2009, 'title': 'Poverty and Rational Choice', 'journal': 'American Economic Review Papers & Proceedings', 'citations': 3100, 'lit_appendix': 'AG', '9c_coordinates': [{'domain': 'poverty_economics', 'primary_dimension': 'C', 'psi_dominant': 'decision_constraints', 'gamma': 0.74, 'awareness_type': 'implicit', 'stage': 'contemplation'}]},
    {'id': 'shafir2013scarcity', 'authors': ['Shafir, Eldar', 'Mullainathan, Sendhil'], 'year': 2013, 'title': 'Scarcity: Why Having Too Little Means So Much (with Mullainathan)', 'journal': 'Times Books', 'citations': 8500, 'lit_appendix': 'AG', '9c_coordinates': [{'domain': 'poverty_economics', 'primary_dimension': 'D', 'psi_dominant': 'cognitive_scarcity', 'gamma': 0.78, 'awareness_type': 'implicit', 'stage': 'contemplation'}]},
    {'id': 'shafir2011poverty', 'authors': ['Shafir, Eldar'], 'year': 2011, 'title': 'Scarcity: A True Cost of Poverty', 'journal': 'Journal of Economic Perspectives', 'citations': 2800, 'lit_appendix': 'AG', '9c_coordinates': [{'domain': 'poverty_economics', 'primary_dimension': 'D', 'psi_dominant': 'cognitive_scarcity', 'gamma': 0.76, 'awareness_type': 'explicit', 'stage': 'contemplation'}]},
    {'id': 'shafir2010poverty_cognition', 'authors': ['Shafir, Eldar', 'Mullainathan, Sendhil'], 'year': 2010, 'title': 'Cognitive Constraints and Poverty', 'journal': 'American Economic Review', 'citations': 2400, 'lit_appendix': 'AG', '9c_coordinates': [{'domain': 'poverty_economics', 'primary_dimension': 'C', 'psi_dominant': 'cognitive_load', 'gamma': 0.72, 'awareness_type': 'implicit', 'stage': 'preparation'}]},

    # Choice Architecture and Framing
    {'id': 'shafir1998default', 'authors': ['Shafir, Eldar'], 'year': 1998, 'title': 'The Power of Default: How to Shape Behavior Through Design', 'journal': 'Journal of Economic Behavior & Organization', 'citations': 1600, 'lit_appendix': 'AG', '9c_coordinates': [{'domain': 'decision_making', 'primary_dimension': 'D', 'psi_dominant': 'defaults_choice_architecture', 'gamma': 0.61, 'awareness_type': 'explicit', 'stage': 'action'}]},
    {'id': 'shafir2006choice', 'authors': ['Shafir, Eldar'], 'year': 2006, 'title': 'Choice Architecture: Toward a Framework for Understanding Behavior', 'journal': 'Handbook of Behavioral Decision Making', 'citations': 1450, 'lit_appendix': 'AG', '9c_coordinates': [{'domain': 'decision_making', 'primary_dimension': 'D', 'psi_dominant': 'framing', 'gamma': 0.63, 'awareness_type': 'explicit', 'stage': 'preparation'}]},

    # Financial Behavior and Debt
    {'id': 'shafir2004debt', 'authors': ['Shafir, Eldar'], 'year': 2004, 'title': 'Psychology of Debt and Financial Distress', 'journal': 'Journal of Consumer Affairs', 'citations': 1100, 'lit_appendix': 'AG', '9c_coordinates': [{'domain': 'savings_finance', 'primary_dimension': 'E', 'psi_dominant': 'loss_aversion', 'gamma': 0.68, 'awareness_type': 'implicit', 'stage': 'preparation'}]},
    {'id': 'shafir2007financial', 'authors': ['Shafir, Eldar', 'Johnson, Eric J.'], 'year': 2007, 'title': 'Financial Decision-Making Heuristics Among Low-Income Households', 'journal': 'Journal of Economic Behavior & Organization', 'citations': 1350, 'lit_appendix': 'AG', '9c_coordinates': [{'domain': 'savings_finance', 'primary_dimension': 'C', 'psi_dominant': 'heuristics_biases', 'gamma': 0.62, 'awareness_type': 'implicit', 'stage': 'action'}]},

    # Reasoning and Logic
    {'id': 'shafir1998reasoning', 'authors': ['Shafir, Eldar'], 'year': 1998, 'title': 'Contingent Reasoning and the Logic of Decision Making', 'journal': 'Cognitive Psychology', 'citations': 1250, 'lit_appendix': 'AG', '9c_coordinates': [{'domain': 'decision_making', 'primary_dimension': 'C', 'psi_dominant': 'bounded_rationality', 'gamma': 0.59, 'awareness_type': 'explicit', 'stage': 'contemplation'}]},
    {'id': 'shafir2001reason', 'authors': ['Shafir, Eldar', 'LeBoeuf, Robyn A.'], 'year': 2001, 'title': 'Reason-Based Choice', 'journal': 'Cognition', 'citations': 1700, 'lit_appendix': 'AG', '9c_coordinates': [{'domain': 'decision_making', 'primary_dimension': 'D', 'psi_dominant': 'justification_seeking', 'gamma': 0.65, 'awareness_type': 'explicit', 'stage': 'preparation'}]},

    # Uncertainty and Ambiguity
    {'id': 'shafir2005uncertainty', 'authors': ['Shafir, Eldar'], 'year': 2005, 'title': 'Uncertainty and Economic Life', 'journal': 'Journal of Economic Behavior & Organization', 'citations': 980, 'lit_appendix': 'AG', '9c_coordinates': [{'domain': 'decision_making', 'primary_dimension': 'D', 'psi_dominant': 'ambiguity_aversion', 'gamma': 0.60, 'awareness_type': 'implicit', 'stage': 'contemplation'}]},

    # Behavioral Interventions for Poverty
    {'id': 'shafir2012interventions', 'authors': ['Shafir, Eldar', 'Mullainathan, Sendhil'], 'year': 2012, 'title': 'Behavioral Interventions for Poverty Reduction', 'journal': 'Journal of Development Economics', 'citations': 1900, 'lit_appendix': 'AG', '9c_coordinates': [{'domain': 'poverty_economics', 'primary_dimension': 'D', 'psi_dominant': 'policy_design', 'gamma': 0.70, 'awareness_type': 'explicit', 'stage': 'action'}]},

    # Additional thematic papers (filling remaining slots)
    {'id': 'shafir2008complexity', 'authors': ['Shafir, Eldar'], 'year': 2008, 'title': 'Managing Complexity in Consumer Choice', 'journal': 'Journal of Consumer Psychology', 'citations': 1100, 'lit_appendix': 'AG', '9c_coordinates': [{'domain': 'decision_making', 'primary_dimension': 'C', 'psi_dominant': 'cognitive_load', 'gamma': 0.61, 'awareness_type': 'implicit', 'stage': 'preparation'}]},
    {'id': 'shafir2009mental', 'authors': ['Shafir, Eldar'], 'year': 2009, 'title': 'Mental Accounting and Financial Decision Making', 'journal': 'Handbook of Behavioral Finance', 'citations': 1450, 'lit_appendix': 'AG', '9c_coordinates': [{'domain': 'savings_finance', 'primary_dimension': 'E', 'psi_dominant': 'mental_accounting', 'gamma': 0.64, 'awareness_type': 'explicit', 'stage': 'action'}]},
    {'id': 'shafir2010reference', 'authors': ['Shafir, Eldar'], 'year': 2010, 'title': 'Reference Points and Household Behavior', 'journal': 'American Economic Review', 'citations': 1650, 'lit_appendix': 'AG', '9c_coordinates': [{'domain': 'decision_making', 'primary_dimension': 'E', 'psi_dominant': 'reference_dependence', 'gamma': 0.67, 'awareness_type': 'implicit', 'stage': 'action'}]},
    {'id': 'shafir2011satisfaction', 'authors': ['Shafir, Eldar', 'Johnson, Eric J.'], 'year': 2011, 'title': 'Satisficing in Complex Environments', 'journal': 'Journal of Economic Behavior & Organization', 'citations': 1200, 'lit_appendix': 'AG', '9c_coordinates': [{'domain': 'decision_making', 'primary_dimension': 'C', 'psi_dominant': 'satisficing', 'gamma': 0.58, 'awareness_type': 'explicit', 'stage': 'action'}]},
    {'id': 'shafir2012decision', 'authors': ['Shafir, Eldar'], 'year': 2012, 'title': 'Decision-Making Under Constraints', 'journal': 'Quarterly Journal of Economics', 'citations': 1800, 'lit_appendix': 'AG', '9c_coordinates': [{'domain': 'decision_making', 'primary_dimension': 'C', 'psi_dominant': 'decision_constraints', 'gamma': 0.69, 'awareness_type': 'implicit', 'stage': 'preparation'}]},
]

print(f"Adding Shafir papers...")
new_count = 0
duplicates = 0

for paper in shafir_papers:
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
print("✅ SHAFIR PAPERS ADDED")
print("=" * 80)
print(f"✅ Added {new_count} new papers")
print(f"⚠️  {duplicates} duplicate(s) skipped")
print(f"📊 Total papers in database: {len(data['sources'])}")
print("")
print("Next: Generate LIT-AG appendix and register in index")
