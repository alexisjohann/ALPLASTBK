#!/usr/bin/env python3
# ┌─────────────────────────────────────────────────────────────────────────┐
# │  ⚠️  DEPRECATED (2026-02-08)                                            │
# │                                                                         │
# │  Phase 4: Case-Paper Linker via 10C (uses old paper-sources.yaml)      │
# │  Kept for reference only.                                              │
# │                                                                         │
# │  SSOT: data/paper-references/PAP-*.yaml + bibliography/bcm_master.bib │
# │  Neue Papers: /integrate-paper Workflow                                │
# └─────────────────────────────────────────────────────────────────────────┘
"""
Phase 4: Bidirectional Case-to-Paper Linking via 10C Coordinates
Strategy: Match cases to papers using domain + dimension + context matching
"""

import yaml
from pathlib import Path
from collections import defaultdict

# Load databases
paper_path = Path("data/paper-sources.yaml")
case_path = Path("data/case-registry.yaml")

with open(paper_path, 'r') as f:
    paper_data = yaml.safe_load(f)

with open(case_path, 'r') as f:
    case_data = yaml.safe_load(f)

papers = paper_data['sources']
cases = case_data['cases']

print("=" * 80)
print("PHASE 4: CASE-TO-PAPER LINKING")
print("=" * 80)
print("")

# Create paper index by ID
papers_by_id = {p['id']: p for p in papers}

# Matching function
def score_match(paper, case):
    """
    Score match between paper and case using 10C coordinates
    Scoring:
      - Domain match: +30 points
      - Dimension match: +25 points
      - Context/Psi match: +25 points
      - Gamma alignment: +20 points
    Total max: 100 points
    """
    score = 0
    details = []

    # Extract paper 10C
    paper_coords = paper.get('9c_coordinates', [{}])[0]
    paper_domain = paper_coords.get('domain')
    paper_dimension = paper_coords.get('primary_dimension')
    paper_psi = paper_coords.get('psi_dominant')
    paper_gamma = paper_coords.get('gamma', 0.5)

    # Extract case 10C
    case_9c = case.get('10C', {})
    case_domains = case.get('domain', [])
    if not isinstance(case_domains, list):
        case_domains = [case_domains] if case_domains else []

    case_dimensions = case_9c.get('WHAT', {}).get('dimensions', [])
    case_psi = case_9c.get('WHEN', {}).get('psi_dominant')

    # 1. Domain matching
    if paper_domain and paper_domain in case_domains:
        score += 30
        details.append('domain')

    # 2. Dimension matching
    if paper_dimension and paper_dimension in case_dimensions:
        score += 25
        details.append('dimension')

    # 3. Context/Psi matching
    if paper_psi and case_psi and paper_psi == case_psi:
        score += 25
        details.append('context')

    # 4. Gamma alignment (complementarity exists)
    if paper_gamma > 0.3:  # Papers with meaningful complementarity
        case_gamma = case_9c.get('HOW', {}).get('gamma_avg', 0.5)
        if abs(paper_gamma - case_gamma) < 0.4:  # Similar complementarity levels
            score += 10
            details.append('gamma')

    return score, details

# Link papers to cases
paper_to_cases = defaultdict(list)
case_to_papers = defaultdict(list)
matched_pairs = 0
total_potential = len(cases) * len(papers)

print(f"Analyzing {len(cases)} cases × {len(papers)} papers...")
print(f"Total potential matches: {total_potential:,}")
print("")

# Find high-quality matches (score >= 50)
high_quality_matches = []

for case_id, case in cases.items():
    for paper in papers:
        score, details = score_match(paper, case)

        if score >= 50:  # High-quality match threshold
            high_quality_matches.append({
                'case_id': case_id,
                'paper_id': paper['id'],
                'score': score,
                'details': details
            })
            paper_to_cases[paper['id']].append(case_id)
            case_to_papers[case_id].append(paper['id'])
            matched_pairs += 1

print(f"High-quality matches (score >= 50): {len(high_quality_matches)}")
print("")

# Statistics
papers_with_links = sum(1 for p in papers if p['id'] in paper_to_cases)
cases_with_links = sum(1 for c in cases if c in case_to_papers)

print("LINKING STATISTICS")
print("-" * 80)
print(f"Papers with links: {papers_with_links} of {len(papers)} ({100*papers_with_links/len(papers):.1f}%)")
print(f"Cases with links: {cases_with_links} of {len(cases)} ({100*cases_with_links/len(cases):.1f}%)")
print(f"Total bidirectional links: {len(high_quality_matches)}")
print("")

# Add links to databases
for match in high_quality_matches:
    paper = papers_by_id[match['paper_id']]
    case = cases[match['case_id']]

    # Add case reference to paper
    if 'linked_cases' not in paper:
        paper['linked_cases'] = []
    if match['case_id'] not in paper['linked_cases']:
        paper['linked_cases'].append(match['case_id'])
    paper['case_count'] = len(paper['linked_cases'])

    # Add paper reference to case
    if 'source_paper' not in case or case['source_paper'] is None:
        case['source_paper'] = match['paper_id']
    elif isinstance(case['source_paper'], str):
        # Keep first match
        pass

# Save updated databases
with open(paper_path, 'w') as f:
    yaml.dump(paper_data, f, default_flow_style=False, sort_keys=False)

with open(case_path, 'w') as f:
    yaml.dump(case_data, f, default_flow_style=False, sort_keys=False)

print("=" * 80)
print("✅ PHASE 4: CASE-TO-PAPER LINKING COMPLETE")
print("=" * 80)
print(f"Created {len(high_quality_matches)} bidirectional links")
print(f"Papers: {papers_with_links}/{len(papers)} now linked to cases")
print(f"Cases: {cases_with_links}/{len(cases)} now linked to papers")
print("")
print("Linking quality distribution:")
score_dist = defaultdict(int)
for match in high_quality_matches:
    score_dist[match['score']] += 1

for score in sorted(score_dist.keys(), reverse=True):
    print(f"  Score {score}: {score_dist[score]} links")

print("")
print("Next: Validation and statistics generation")
