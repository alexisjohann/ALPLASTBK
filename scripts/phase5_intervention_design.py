#!/usr/bin/env python3
# ┌─────────────────────────────────────────────────────────────────────────┐
# │  ⚠️  DEPRECATED (2026-02-08)                                            │
# │                                                                         │
# │  Phase 5: Intervention Design (uses old paper-sources.yaml format)     │
# │  Kept for reference only.                                              │
# │                                                                         │
# │  SSOT: data/paper-references/PAP-*.yaml + bibliography/bcm_master.bib │
# │  Neue Papers: /integrate-paper Workflow                                │
# └─────────────────────────────────────────────────────────────────────────┘
"""
Phase 5: Theory-Driven Intervention Design from Linked Papers and Cases

Strategy: Use 10C linking to design evidence-based interventions
Input: Problem specification (domain, behavior, population, phase)
Output: Complete intervention project with predictions
"""

import yaml
from pathlib import Path
from collections import defaultdict
import json
from datetime import datetime

# Load databases
paper_path = Path("data/paper-sources.yaml")
case_path = Path("data/case-registry.yaml")
intervention_path = Path("data/intervention-registry.yaml")

with open(paper_path, 'r') as f:
    paper_data = yaml.safe_load(f)
with open(case_path, 'r') as f:
    case_data = yaml.safe_load(f)
with open(intervention_path, 'r') as f:
    intervention_data = yaml.safe_load(f)

papers = paper_data['sources']
cases = case_data['cases']
projects = intervention_data.get('projects', {})

# Create paper index
papers_by_id = {p['id']: p for p in papers}

print("=" * 80)
print("PHASE 5: THEORY-DRIVEN INTERVENTION DESIGN")
print("=" * 80)
print()

def find_similar_cases(domain, target_behavior=None, target_phase=None, limit=5):
    """
    Find similar cases in registry based on 10C matching
    """
    matches = []

    for case_id, case in cases.items():
        case_domain = case.get('domain', [])
        if not isinstance(case_domain, list):
            case_domain = [case_domain] if case_domain else []

        # Domain match
        if domain not in case_domain:
            continue

        # Phase match (if specified)
        case_phase = case.get('10C', {}).get('WHEN', {}).get('phase')
        if target_phase and case_phase != target_phase:
            continue

        # Calculate relevance score
        score = 0
        if domain in case_domain:
            score += 1

        case_9c = case.get('10C', {})
        if case_9c.get('WHAT', {}).get('dimensions'):
            score += 0.5

        matches.append({
            'case_id': case_id,
            'domain': case_domain,
            'score': score
        })

    # Sort by score and return top matches
    matches = sorted(matches, key=lambda x: x['score'], reverse=True)[:limit]
    return matches

def get_papers_for_case(case_id, limit=15):
    """
    Get papers linked to a specific case
    """
    if case_id not in cases:
        return []

    case = cases[case_id]
    linked_paper_ids = case.get('linked_cases', [])
    if not linked_paper_ids:
        linked_paper_ids = []

    # Actually, linked_cases is case-oriented. Let me get papers that link to this case
    linked_papers = []
    for paper in papers:
        if case_id in paper.get('linked_cases', []):
            linked_papers.append({
                'id': paper['id'],
                'authors': paper.get('authors', ['Unknown'])[0] if paper.get('authors') else 'Unknown',
                'year': paper.get('year'),
                'title': paper.get('title', 'Untitled'),
                'citations': paper.get('citations', 0),
                '9c_coordinates': paper.get('9c_coordinates', [{}])[0]
            })

    # Sort by citations
    linked_papers = sorted(linked_papers, key=lambda x: x['citations'], reverse=True)[:limit]
    return linked_papers

def extract_mechanisms_from_papers(papers_list):
    """
    Extract behavioral mechanisms from papers via 10C coordinates
    """
    mechanisms = defaultdict(list)

    for paper in papers_list:
        coords = paper.get('9c_coordinates', {})

        # WHAT dimension suggests intervention type
        dimension = coords.get('primary_dimension')
        if dimension:
            mechanisms[dimension].append({
                'paper_id': paper['id'],
                'mechanism': dimension,
                'author': paper['authors'][0] if paper.get('authors') else 'Unknown'
            })

        # Psi dimension suggests context/timing
        psi = coords.get('psi_dominant')
        if psi:
            mechanisms[f"context_{psi}"].append({
                'paper_id': paper['id'],
                'context': psi,
                'author': paper['authors'][0] if paper.get('authors') else 'Unknown'
            })

    return dict(mechanisms)

def estimate_intervention_effects(domain, mechanisms):
    """
    Estimate E_i (expected contribution) for interventions
    Based on domain and mechanisms
    """
    # Literature-based parameter repository (simplified BBB subset)
    default_effects = {
        'S': {'nudge': 0.30, 'social': 0.08, 'information': 0.05},
        'E': {'information': 0.15, 'incentive': 0.35, 'social': 0.10},
        'F': {'incentive': 0.40, 'commitment': 0.25, 'social': 0.15},
        'D': {'information': 0.20, 'nudge': 0.10, 'environmental': 0.12},
        'P': {'commitment': 0.35, 'social': 0.20, 'information': 0.10},
        'C': {'commitment': 0.30, 'social': 0.25, 'information': 0.08}
    }

    # Domain-specific adjustments
    domain_effects = {
        'finance': 0.25,
        'health': 0.20,
        'workplace': 0.30,
        'government': 0.15,
        'nonprofit': 0.22,
        'energy': 0.18
    }

    effects = {}
    for dimension, papers in mechanisms.items():
        if dimension.startswith('context_'):
            continue

        base_effect = default_effects.get(dimension, {}).get('nudge', 0.10)
        domain_multiplier = domain_effects.get(domain, 0.20)
        effects[dimension] = min(0.45, base_effect * (1 + domain_multiplier / 100))

    return effects

def calculate_complementarity_matrix(interventions):
    """
    Estimate γ_ij (complementarity) between intervention pairs
    """
    # Simplified: nearby interventions have synergy
    gamma_matrix = {}

    intervention_ids = [iv['id'] for iv in interventions]

    for i, id_i in enumerate(intervention_ids):
        for j, id_j in enumerate(intervention_ids):
            if i >= j:
                continue

            # Default synergy
            gamma = 0.15

            # Specific synergies
            iv_i = interventions[i]
            iv_j = interventions[j]

            type_i = iv_i.get('type', '')
            type_j = iv_j.get('type', '')

            # nudge + information synergy is strong
            if (type_i == 'nudge' and type_j == 'information') or \
               (type_i == 'information' and type_j == 'nudge'):
                gamma = 0.35

            # incentive + commitment synergy is strong
            elif (type_i == 'incentive' and type_j == 'commitment') or \
                 (type_i == 'commitment' and type_j == 'incentive'):
                gamma = 0.30

            # social + information synergy is moderate
            elif (type_i == 'social' and type_j == 'information') or \
                 (type_i == 'information' and type_j == 'social'):
                gamma = 0.20

            # Same type may have weak/negative interaction
            elif type_i == type_j:
                gamma = 0.08

            key = tuple(sorted([id_i, id_j]))
            gamma_matrix[key] = gamma

    return gamma_matrix

def calculate_portfolio_effect(interventions, gamma_matrix):
    """
    Calculate portfolio effect E(P) using complementarity formula
    E(P) = Σ E_i + Σ γ_ij · √(E_i · E_j)
    """
    # Sum of individual effects
    sum_E_i = sum(iv.get('expected_contribution', {}).get('E_i', 0) for iv in interventions)

    # Sum of interaction effects
    sum_interactions = 0
    intervention_ids = [iv['id'] for iv in interventions]

    for (id_i, id_j), gamma in gamma_matrix.items():
        iv_i = next(iv for iv in interventions if iv['id'] == id_i)
        iv_j = next(iv for iv in interventions if iv['id'] == id_j)

        E_i = iv_i.get('expected_contribution', {}).get('E_i', 0)
        E_j = iv_j.get('expected_contribution', {}).get('E_j', 0)

        interaction = gamma * (E_i * E_j) ** 0.5
        sum_interactions += interaction

    E_P = sum_E_i + sum_interactions

    # Add confidence-weighted uncertainty
    avg_confidence = sum(iv.get('expected_contribution', {}).get('confidence', 0.7)
                        for iv in interventions) / len(interventions)

    CI_width = E_P * (1 - avg_confidence) * 0.5

    return {
        'E_P': min(0.95, E_P),  # Cap at 95% effect
        'CI_lower': max(0, E_P - CI_width),
        'CI_upper': min(1.0, E_P + CI_width),
        'confidence': avg_confidence
    }

def create_project(
    project_id,
    name,
    domain,
    target_behavior,
    baseline_behavior,
    journey_phase,
    similar_cases,
    interventions,
    complementarity,
    portfolio_effect
):
    """
    Create a new intervention project and save to registry
    """
    project = {
        'meta': {
            'name': name,
            'domain': domain,
            'status': 'planning',
            'created_date': datetime.now().strftime('%Y-%m-%d'),
            'based_on_cases': [case['case_id'] for case in similar_cases]
        },
        'context': {
            'target_behavior': target_behavior,
            'baseline_behavior': baseline_behavior,
            'journey_phase': journey_phase,
            'sample_size': 'to_be_determined',
            'segments': [
                {'name': 'segment_1', 'proportion': 0.33, 'sigma': 1.5},
                {'name': 'segment_2', 'proportion': 0.33, 'sigma': 1.2},
                {'name': 'segment_3', 'proportion': 0.34, 'sigma': 1.0}
            ]
        },
        'intervention_mix': interventions,
        'complementarity_matrix': [
            {
                'pair': list(pair),
                'gamma_ij': gamma,
                'interaction': 'synergy' if gamma > 0.15 else ('neutral' if gamma < -0.05 else 'synergy'),
                'mechanism': f'Complementarity between {pair[0]} and {pair[1]}'
            }
            for pair, gamma in complementarity.items()
        ],
        'predictions': {
            'portfolio_effect': portfolio_effect,
            'kpis': [
                {
                    'name': 'Primary behavior change',
                    'baseline': baseline_behavior,
                    'predicted_value': baseline_behavior + portfolio_effect['E_P'] * (1 - baseline_behavior),
                    'predicted_delta': portfolio_effect['E_P'] * (1 - baseline_behavior),
                    'predicted_delta_pct': round(100 * portfolio_effect['E_P'], 1),
                    'confidence': round(portfolio_effect['confidence'], 2)
                }
            ]
        }
    }

    return project

# MAIN WORKFLOW
print("1. Finding similar cases (to learn from)...")
similar = find_similar_cases('finance', target_phase='contemplation', limit=3)
print(f"   Found {len(similar)} similar cases in finance domain")
for case in similar:
    print(f"   - {case['case_id']}")

print()
print("2. Extracting linked papers...")
all_papers = []
for case in similar:
    papers_for_case = get_papers_for_case(case['case_id'], limit=5)
    all_papers.extend(papers_for_case)
    print(f"   - {case['case_id']}: {len(papers_for_case)} linked papers")

print(f"   Total unique papers: {len(set(p['id'] for p in all_papers))}")

print()
print("3. Extracting behavioral mechanisms from papers...")
mechanisms = extract_mechanisms_from_papers(all_papers)
print(f"   Found {len(mechanisms)} distinct mechanisms")
for mechanism, papers in list(mechanisms.items())[:5]:
    print(f"   - {mechanism}: {len(papers)} papers")

print()
print("4. Estimating intervention effects (E_i)...")
effects = estimate_intervention_effects('finance', mechanisms)

# Build sample interventions
sample_interventions = []
intervention_types = [
    ('I1', 'nudge', 'default', 'Automatic enrollment'),
    ('I2', 'information', 'personalized', 'Personalized retirement projection'),
    ('I3', 'social', 'descriptive_norm', 'Social norm messaging'),
]

for int_id, int_type, subtype, desc in intervention_types:
    base_effect = effects.get('S', 0.20) if int_type == 'nudge' else \
                 effects.get('E', 0.15) if int_type == 'information' else \
                 effects.get('E', 0.08)

    sample_interventions.append({
        'id': int_id,
        'type': int_type,
        'subtype': subtype,
        'description': desc,
        'timing': 'contemplation',
        'target_segment': 'all',
        'parameters': {
            'intensity': 0.7,
            'duration': '3 months',
            'frequency': 'ongoing'
        },
        'expected_contribution': {
            'E_i': round(base_effect, 2),
            'confidence': 0.70,
            'source': 'literature'
        }
    })

print(f"   Sample interventions:")
for iv in sample_interventions:
    E_i = iv['expected_contribution']['E_i']
    print(f"   - {iv['id']}: {iv['description']} (E_i={E_i})")

print()
print("5. Calculating complementarity matrix...")
gamma_matrix = calculate_complementarity_matrix(sample_interventions)
print(f"   Complementarity pairs:")
for (id_i, id_j), gamma in gamma_matrix.items():
    interaction = 'synergy' if gamma > 0.15 else 'neutral' if gamma > 0 else 'interference'
    print(f"   - {id_i} × {id_j}: γ = {gamma:.2f} ({interaction})")

print()
print("6. Computing portfolio effect...")
portfolio = calculate_portfolio_effect(sample_interventions, gamma_matrix)
print(f"   E(P) = {portfolio['E_P']:.3f}")
print(f"   CI: [{portfolio['CI_lower']:.3f}, {portfolio['CI_upper']:.3f}]")
print(f"   Confidence: {portfolio['confidence']:.1%}")

print()
print("7. Creating sample project...")

# Generate next project ID
existing_ids = [int(pid.replace('PRJ-', '')) for pid in projects.keys() if pid.startswith('PRJ-')]
next_id = max(existing_ids) + 1 if existing_ids else 1
project_id = f"PRJ-{next_id:03d}"

sample_project = create_project(
    project_id=project_id,
    name="Finance Retirement Enrollment Optimization",
    domain='finance',
    target_behavior='Retirement account enrollment',
    baseline_behavior=0.28,
    journey_phase='contemplation',
    similar_cases=similar,
    interventions=sample_interventions,
    complementarity=gamma_matrix,
    portfolio_effect=portfolio
)

# Add to registry (in-memory only, not persisted)
projects[project_id] = sample_project

print(f"   Created: {project_id}")
print(f"   Name: {sample_project['meta']['name']}")
print(f"   Status: {sample_project['meta']['status']}")

print()
print("=" * 80)
print("✅ PHASE 5 INTERVENTION DESIGN: COMPLETE")
print("=" * 80)
print()
print("SUMMARY")
print("-" * 80)
print(f"Created intervention design {project_id}")
print(f"Based on {len(similar)} similar cases from case-registry")
print(f"Reviewed {len(all_papers)} papers linked to similar cases")
print(f"Designed {len(sample_interventions)} interventions")
print(f"Expected portfolio effect: {portfolio['E_P']:.1%}")
print(f"Confidence interval: {portfolio['CI_lower']:.1%} - {portfolio['CI_upper']:.1%}")
print()
print("Next steps:")
print("  1. Refine segments and target population")
print("  2. Set timeline and implementation details")
print("  3. Deploy interventions")
print("  4. Measure outcomes (Phase 5 - Analyzer)")
print("  5. Extract learnings (Phase 5 - Extractor)")

