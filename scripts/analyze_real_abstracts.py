#!/usr/bin/env python3
"""
SWSM Real Abstract Analyzer - Compare measured style to LLMMC priors
====================================================================

Analyzes real paper abstracts and compares measured style vectors
against the LLMMC-derived priors in the SWSM model.

Session: EBF-S-2026-01-29-SWSM-001
"""

import json
import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from stylometry_analyzer import StylometryAnalyzer, AUTHOR_PRIORS, DIMENSIONS

def load_abstracts(json_path: str) -> dict:
    """Load abstracts from JSON file."""
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def analyze_abstract(analyzer: StylometryAnalyzer, text: str) -> dict:
    """Analyze a single abstract and return dimension scores."""
    vec = analyzer.analyze_text(text)
    return {
        'D1_formality': vec.D1_formality,
        'D2_evidence': vec.D2_evidence,
        'D3_narrativity': vec.D3_narrativity,
        'D4_hedging': vec.D4_hedging,
        'D5_policy': vec.D5_policy,
        'D6_syntax': vec.D6_syntax,
        'D7_collaboration': vec.D7_collaboration,
        'D8_humor': vec.D8_humor,
        'D9_interdisciplinary': vec.D9_interdisciplinary,
        'D10_temporal': vec.D10_temporal
    }

def compare_to_prior(measured: dict, author: str) -> dict:
    """Compare measured values to LLMMC priors."""
    if author not in AUTHOR_PRIORS:
        return None

    prior = AUTHOR_PRIORS[author]['priors']
    comparison = {}

    dim_map = {
        'D1_formality': 'D1',
        'D2_evidence': 'D2',
        'D3_narrativity': 'D3',
        'D4_hedging': 'D4',
        'D5_policy': 'D5',
        'D6_syntax': 'D6',
        'D7_collaboration': 'D7',
        'D8_humor': 'D8',
        'D9_interdisciplinary': 'D9',
        'D10_temporal': 'D10'
    }

    for dim_full, dim_short in dim_map.items():
        prior_mean, prior_std = prior[dim_short]
        measured_val = measured[dim_full]
        diff = measured_val - prior_mean
        z_score = diff / prior_std if prior_std > 0 else 0

        comparison[dim_short] = {
            'prior_mean': prior_mean,
            'prior_std': prior_std,
            'measured': measured_val,
            'diff': diff,
            'z_score': z_score,
            'within_1sd': abs(z_score) <= 1.0,
            'within_2sd': abs(z_score) <= 2.0
        }

    return comparison

def main():
    print("=" * 80)
    print("SWSM REAL ABSTRACT ANALYSIS")
    print("Comparing measured style vectors to LLMMC priors")
    print("=" * 80)

    # Load abstracts
    abstracts_path = Path(__file__).parent.parent / 'data' / 'swsm-abstracts.json'
    data = load_abstracts(abstracts_path)

    print(f"\nLoaded {data['metadata']['total_abstracts']} abstracts")
    print(f"Source: {data['metadata']['source']}")
    print()

    # Initialize analyzer
    analyzer = StylometryAnalyzer()

    # Results storage
    all_results = {}

    # Dimension labels
    dim_labels = ['D1:Form', 'D2:Evid', 'D3:Narr', 'D4:Hedg', 'D5:Poli',
                  'D6:Synt', 'D7:Coll', 'D8:Hum', 'D9:Intd', 'D10:Temp']

    # Print header
    print("-" * 80)
    print(f"{'Author':<12} {'Paper':<35} {'Words':>6}")
    print("-" * 80)

    for author, papers in data['abstracts'].items():
        if not papers:
            continue

        for paper in papers:
            title = paper['title'][:32] + "..." if len(paper['title']) > 35 else paper['title']
            print(f"{author:<12} {title:<35} {paper['abstract_words']:>6}")

    print("\n" + "=" * 80)
    print("STYLE VECTOR ANALYSIS (Measured vs Prior)")
    print("=" * 80)

    # Analyze each author
    for author in data['abstracts'].keys():
        papers = data['abstracts'][author]
        if not papers:
            continue

        print(f"\n{'─' * 80}")
        print(f"  {author.upper()} - {AUTHOR_PRIORS.get(author, {}).get('full_name', author)}")
        print(f"  Cluster: {AUTHOR_PRIORS.get(author, {}).get('cluster', 'Unknown')}")
        print(f"{'─' * 80}")

        # Analyze abstract
        abstract_text = papers[0]['abstract']
        measured = analyze_abstract(analyzer, abstract_text)
        comparison = compare_to_prior(measured, author)

        if comparison is None:
            print(f"  No prior data for {author}")
            continue

        all_results[author] = {
            'measured': measured,
            'comparison': comparison
        }

        # Print comparison table
        print(f"\n  {'Dim':<8} {'Prior':>8} {'±σ':>6} {'Measured':>10} {'Diff':>8} {'Z':>6} {'Status':<12}")
        print(f"  {'-' * 66}")

        within_1sd_count = 0
        within_2sd_count = 0

        for i, (dim, vals) in enumerate(comparison.items()):
            status = ""
            if vals['within_1sd']:
                status = "✓ OK"
                within_1sd_count += 1
            elif vals['within_2sd']:
                status = "~ acceptable"
                within_2sd_count += 1
            else:
                status = "✗ DIVERGENT"

            print(f"  {dim_labels[i]:<8} {vals['prior_mean']:>8.2f} {vals['prior_std']:>6.2f} "
                  f"{vals['measured']:>10.2f} {vals['diff']:>+8.2f} {vals['z_score']:>+6.2f} {status:<12}")

        # Summary
        print(f"\n  Summary: {within_1sd_count}/10 within 1σ, {within_1sd_count + within_2sd_count}/10 within 2σ")

        if within_1sd_count >= 7:
            print(f"  Assessment: ✓ GOOD FIT - Prior matches measured style well")
        elif within_1sd_count + within_2sd_count >= 7:
            print(f"  Assessment: ~ ACCEPTABLE - Minor calibration needed")
        else:
            print(f"  Assessment: ✗ NEEDS CALIBRATION - Prior should be updated")

    # Overall summary
    print("\n" + "=" * 80)
    print("OVERALL CALIBRATION SUMMARY")
    print("=" * 80)

    total_within_1sd = 0
    total_dims = 0

    for author, results in all_results.items():
        comp = results['comparison']
        author_within_1sd = sum(1 for v in comp.values() if v['within_1sd'])
        total_within_1sd += author_within_1sd
        total_dims += 10

        pct = author_within_1sd / 10 * 100
        bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
        print(f"  {author:<15} {bar} {author_within_1sd:>2}/10 ({pct:.0f}%)")

    if total_dims > 0:
        overall_pct = total_within_1sd / total_dims * 100
        print(f"\n  Overall: {total_within_1sd}/{total_dims} dimensions within 1σ ({overall_pct:.1f}%)")

        if overall_pct >= 70:
            print(f"\n  ✓ MODEL VALIDATION PASSED - LLMMC priors are well-calibrated")
        elif overall_pct >= 50:
            print(f"\n  ~ MODEL NEEDS TUNING - Some priors should be adjusted")
        else:
            print(f"\n  ✗ MODEL NEEDS RECALIBRATION - Priors diverge from measured values")

    print("\n" + "=" * 80)

    # Save results
    output_path = Path(__file__).parent.parent / 'data' / 'swsm-calibration-results.json'
    output_data = {
        'metadata': {
            'analyzed_at': '2026-01-29',
            'n_authors': len(all_results),
            'n_abstracts': sum(len(data['abstracts'].get(a, [])) for a in all_results.keys())
        },
        'results': {}
    }

    for author, results in all_results.items():
        output_data['results'][author] = {
            'measured': results['measured'],
            'comparison': {k: {
                'prior_mean': v['prior_mean'],
                'measured': v['measured'],
                'diff': v['diff'],
                'z_score': v['z_score']
            } for k, v in results['comparison'].items()}
        }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2)

    print(f"Results saved to {output_path}")

if __name__ == '__main__':
    main()
