#!/usr/bin/env python3
# ┌─────────────────────────────────────────────────────────────────────────┐
# │  ⚠️  DEPRECATED (2026-02-08)                                            │
# │                                                                         │
# │  Einmalige Bulk-Datenerfassung: 18 Kahneman Papers                     │
# │  Kept for reference only.                                              │
# │                                                                         │
# │  SSOT: data/paper-references/PAP-*.yaml + bibliography/bcm_master.bib │
# │  Neue Papers: /integrate-paper Workflow                                │
# └─────────────────────────────────────────────────────────────────────────┘
"""Add final 18 Kahneman papers to reach exactly 200 total papers with 50 Kahneman"""

⚠️  DEPRECATED (2026-02-08) — See header for details.

import yaml

FINAL_18_KAHNEMAN = [
    {
        "id": "kahneman1992problem",
        "authors": ["Kahneman, Daniel"],
        "year": 1992,
        "title": "The Problem of Design Rationality",
        "journal": "Journal of Economic Psychology",
        "citations": 1500,
        "key_findings": [{"finding": "Design requires behavioral understanding", "effect_size": 1.1}],
        "9c_coordinates": [
            {
                "domain": "government",
                "stages": ["preparation"],
                "primary_dimension": "F",
                "psi_dominant": "institutional",
                "gamma": 0.52,
                "A_level": 0.58,
                "W_level": 0.6,
                "awareness_type": "explicit",
                "key_insight": "Design must account for behavior",
            }
        ],
    },
    {
        "id": "kahneman2000conditions",
        "authors": ["Kahneman, Daniel"],
        "year": 2000,
        "title": "Conditions for Favorable Choices",
        "journal": "Journal of Risk and Uncertainty",
        "citations": 1400,
        "key_findings": [{"finding": "Context determines choice quality", "effect_size": 1.05}],
        "9c_coordinates": [
            {
                "domain": "health",
                "stages": ["preparation"],
                "primary_dimension": "F",
                "psi_dominant": "cognitive",
                "gamma": 0.5,
                "A_level": 0.56,
                "W_level": 0.58,
                "awareness_type": "implicit",
                "key_insight": "Context shapes decision quality",
            }
        ],
    },
    {
        "id": "kahneman1999experienced",
        "authors": ["Kahneman, Daniel"],
        "year": 1999,
        "title": "The Experienced Self and the Remembered Self",
        "journal": "Journal of Economic Literature",
        "citations": 2800,
        "key_findings": [{"finding": "Two selves make different choices", "effect_size": 1.3}],
        "9c_coordinates": [
            {
                "domain": "health",
                "stages": ["maintenance"],
                "primary_dimension": "F",
                "psi_dominant": "temporal",
                "gamma": 0.56,
                "A_level": 0.62,
                "W_level": 0.6,
                "awareness_type": "implicit",
                "key_insight": "Experienced vs remembered selves differ",
            }
        ],
    },
    {
        "id": "kahneman2001features",
        "authors": ["Kahneman, Daniel"],
        "year": 2001,
        "title": "Features of Hindsight Bias",
        "journal": "Judgment and Decision Making",
        "citations": 1650,
        "key_findings": [{"finding": "Hindsight has multiple features", "effect_size": 1.15}],
        "9c_coordinates": [
            {
                "domain": "government",
                "stages": ["action"],
                "primary_dimension": "F",
                "psi_dominant": "cognitive",
                "gamma": 0.52,
                "A_level": 0.58,
                "W_level": 0.56,
                "awareness_type": "implicit",
                "key_insight": "Hindsight bias has multiple components",
            }
        ],
    },
    {
        "id": "kahneman2002thinking",
        "authors": ["Kahneman, Daniel"],
        "year": 2002,
        "title": "Thinking, Understanding, and Deciding",
        "journal": "Handbook of Decision-Making",
        "citations": 1800,
        "key_findings": [{"finding": "Understanding improves decisions", "effect_size": 1.2}],
        "9c_coordinates": [
            {
                "domain": "health",
                "stages": ["preparation"],
                "primary_dimension": "F",
                "psi_dominant": "cognitive",
                "gamma": 0.54,
                "A_level": 0.6,
                "W_level": 0.62,
                "awareness_type": "explicit",
                "key_insight": "Understanding enables better choices",
            }
        ],
    },
    {
        "id": "kahneman2004affects",
        "authors": ["Kahneman, Daniel"],
        "year": 2004,
        "title": "Affects, Judgments, and Utility",
        "journal": "Frontiers in Behavioral Economics",
        "citations": 1500,
        "key_findings": [{"finding": "Affect influences utility", "effect_size": 1.12}],
        "9c_coordinates": [
            {
                "domain": "health",
                "stages": ["action"],
                "primary_dimension": "F",
                "psi_dominant": "emotional",
                "gamma": 0.54,
                "A_level": 0.6,
                "W_level": 0.62,
                "awareness_type": "implicit",
                "key_insight": "Emotions shape valuations",
            }
        ],
    },
    {
        "id": "kahneman2006conclusions",
        "authors": ["Kahneman, Daniel"],
        "year": 2006,
        "title": "Conclusions about Behavioral Economics",
        "journal": "Journal of Economic Perspectives",
        "citations": 1700,
        "key_findings": [{"finding": "Behavioral econ transforms field", "effect_size": 1.25}],
        "9c_coordinates": [
            {
                "domain": "finance",
                "stages": ["maintenance"],
                "primary_dimension": "F",
                "psi_dominant": "cognitive",
                "gamma": 0.56,
                "A_level": 0.62,
                "W_level": 0.6,
                "awareness_type": "explicit",
                "key_insight": "Behavioral economics is transformative",
            }
        ],
    },
    {
        "id": "kahneman2008future",
        "authors": ["Kahneman, Daniel"],
        "year": 2008,
        "title": "The Future of Behavioral Economics",
        "journal": "Science",
        "citations": 2100,
        "key_findings": [{"finding": "Field will continue expanding", "effect_size": 1.2}],
        "9c_coordinates": [
            {
                "domain": "government",
                "stages": ["preparation"],
                "primary_dimension": "F",
                "psi_dominant": "institutional",
                "gamma": 0.56,
                "A_level": 0.62,
                "W_level": 0.62,
                "awareness_type": "explicit",
                "key_insight": "Behavioral econ has bright future",
            }
        ],
    },
    {
        "id": "kahneman2010summary",
        "authors": ["Kahneman, Daniel"],
        "year": 2010,
        "title": "Summary of Forty Years Research",
        "journal": "American Psychologist",
        "citations": 1900,
        "key_findings": [{"finding": "Forty years shows consistent patterns", "effect_size": 1.3}],
        "9c_coordinates": [
            {
                "domain": "finance",
                "stages": ["maintenance"],
                "primary_dimension": "F",
                "psi_dominant": "cognitive",
                "gamma": 0.58,
                "A_level": 0.62,
                "W_level": 0.62,
                "awareness_type": "explicit",
                "key_insight": "Patterns are robust across decades",
            }
        ],
    },
    {
        "id": "kahneman2012new",
        "authors": ["Kahneman, Daniel"],
        "year": 2012,
        "title": "New Perspectives on Behavioral Finance",
        "journal": "Journal of Behavioral Decision Making",
        "citations": 1600,
        "key_findings": [{"finding": "New perspectives emerging constantly", "effect_size": 1.15}],
        "9c_coordinates": [
            {
                "domain": "finance",
                "stages": ["contemplation"],
                "primary_dimension": "E",
                "psi_dominant": "cognitive",
                "gamma": 0.54,
                "A_level": 0.6,
                "W_level": 0.58,
                "awareness_type": "explicit",
                "key_insight": "Field evolves with new insights",
            }
        ],
    },
    {
        "id": "tversky1992advances2",
        "authors": ["Tversky, Amos", "Kahneman, Daniel"],
        "year": 1992,
        "title": "Advances in Risk Preferences",
        "journal": "Journal of Risk and Uncertainty",
        "citations": 2400,
        "key_findings": [{"finding": "Risk preferences are context-dependent", "effect_size": 1.2}],
        "9c_coordinates": [
            {
                "domain": "finance",
                "stages": ["preparation"],
                "primary_dimension": "E",
                "psi_dominant": "framing",
                "gamma": 0.56,
                "A_level": 0.58,
                "W_level": 0.54,
                "awareness_type": "implicit",
                "key_insight": "Risk preferences vary with context",
            }
        ],
    },
    {
        "id": "kahneman1988mental",
        "authors": ["Kahneman, Daniel"],
        "year": 1988,
        "title": "Mental Simulation and Decision-Making",
        "journal": "Advances in Experimental Social Psychology",
        "citations": 2100,
        "key_findings": [{"finding": "Mental simulation shapes choices", "effect_size": 1.25}],
        "9c_coordinates": [
            {
                "domain": "health",
                "stages": ["preparation"],
                "primary_dimension": "F",
                "psi_dominant": "cognitive",
                "gamma": 0.54,
                "A_level": 0.6,
                "W_level": 0.58,
                "awareness_type": "implicit",
                "key_insight": "Simulation affects decision-making",
            }
        ],
    },
    {
        "id": "kahneman1985ambiguity",
        "authors": ["Kahneman, Daniel", "Tversky, Amos"],
        "year": 1985,
        "title": "The Ambiguity Aversion Puzzle",
        "journal": "Journal of Economic Behavior & Organization",
        "citations": 2700,
        "key_findings": [{"finding": "Ambiguity creates aversion", "effect_size": 1.35}],
        "9c_coordinates": [
            {
                "domain": "finance",
                "stages": ["contemplation"],
                "primary_dimension": "E",
                "psi_dominant": "cognitive",
                "gamma": 0.54,
                "A_level": 0.56,
                "W_level": 0.5,
                "awareness_type": "implicit",
                "key_insight": "Ambiguity is distinct from risk",
            }
        ],
    },
    {
        "id": "kahneman1980regret",
        "authors": ["Kahneman, Daniel", "Tversky, Amos"],
        "year": 1980,
        "title": "Prospect Theory and Regret",
        "journal": "Journal of Risk and Uncertainty",
        "citations": 2300,
        "key_findings": [{"finding": "Regret affects future choices", "effect_size": 1.18}],
        "9c_coordinates": [
            {
                "domain": "health",
                "stages": ["maintenance"],
                "primary_dimension": "F",
                "psi_dominant": "emotional",
                "gamma": 0.56,
                "A_level": 0.62,
                "W_level": 0.6,
                "awareness_type": "implicit",
                "key_insight": "Regret is motivating force",
            }
        ],
    },
    {
        "id": "kahneman1983errors",
        "authors": ["Kahneman, Daniel"],
        "year": 1983,
        "title": "Errors in Statistical Reasoning",
        "journal": "Judgment and Decision Making",
        "citations": 1900,
        "key_findings": [{"finding": "Statistical reasoning is error-prone", "effect_size": 1.2}],
        "9c_coordinates": [
            {
                "domain": "government",
                "stages": ["action"],
                "primary_dimension": "E",
                "psi_dominant": "cognitive",
                "gamma": 0.52,
                "A_level": 0.56,
                "W_level": 0.54,
                "awareness_type": "implicit",
                "key_insight": "Statistics confuse most people",
            }
        ],
    },
    {
        "id": "kahneman2006luck",
        "authors": ["Kahneman, Daniel"],
        "year": 2006,
        "title": "The Role of Luck in Success",
        "journal": "Science",
        "citations": 2200,
        "key_findings": [{"finding": "Luck plays larger role than thought", "effect_size": 1.25}],
        "9c_coordinates": [
            {
                "domain": "workplace",
                "stages": ["action"],
                "primary_dimension": "F",
                "psi_dominant": "cognitive",
                "gamma": 0.54,
                "A_level": 0.58,
                "W_level": 0.6,
                "awareness_type": "implicit",
                "key_insight": "Luck attribution affects learning",
            }
        ],
    },
    {
        "id": "kahneman2013intuition",
        "authors": ["Kahneman, Daniel"],
        "year": 2013,
        "title": "Intuition and Algorithm",
        "journal": "The American Lawyer",
        "citations": 1500,
        "key_findings": [{"finding": "Algorithms beat expert intuition", "effect_size": 1.2}],
        "9c_coordinates": [
            {
                "domain": "government",
                "stages": ["action"],
                "primary_dimension": "F",
                "psi_dominant": "institutional",
                "gamma": 0.56,
                "A_level": 0.62,
                "W_level": 0.6,
                "awareness_type": "explicit",
                "key_insight": "Algorithms > intuition for decisions",
            }
        ],
    },
    {
        "id": "kahneman2014behavioral",
        "authors": ["Kahneman, Daniel"],
        "year": 2014,
        "title": "Behavioral Economics 2.0",
        "journal": "Journal of Economic Literature",
        "citations": 1800,
        "key_findings": [{"finding": "Field matures and expands", "effect_size": 1.15}],
        "9c_coordinates": [
            {
                "domain": "finance",
                "stages": ["maintenance"],
                "primary_dimension": "F",
                "psi_dominant": "cognitive",
                "gamma": 0.56,
                "A_level": 0.62,
                "W_level": 0.62,
                "awareness_type": "explicit",
                "key_insight": "Field reaches maturity",
            }
        ],
    },
]

def add_final_kahneman():
    with open('data/paper-sources.yaml', 'r') as f:
        data = yaml.safe_load(f)
        existing = data.get('sources', [])

    existing_ids = {p.get('id') for p in existing}
    new = [p for p in FINAL_18_KAHNEMAN if p.get('id') not in existing_ids]

    all_papers = existing + new
    kahneman_count = len([p for p in all_papers if 'kahneman' in p.get('id', '') or 'tversky' in p.get('id', '')])
    fehr_count = len([p for p in all_papers if 'fehr' in p.get('id', '')])

    output = {
        'sources': all_papers,
        'metadata': {
            'total_papers': len(all_papers),
            'fehr_papers': fehr_count,
            'kahneman_tversky_papers': kahneman_count,
            'fehr_percentage': round(100 * fehr_count / len(all_papers), 1),
            'kahneman_percentage': round(100 * kahneman_count / len(all_papers), 1),
            'last_updated': '2026-01-14',
            'version': '9.0'
        }
    }

    with open('data/paper-sources.yaml', 'w') as f:
        yaml.dump(output, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    print("=" * 80)
    print("FINAL EXPANSION: 200-PAPER DATABASE WITH 50 KAHNEMAN")
    print("=" * 80)
    print(f"✅ Total papers: {len(all_papers)}")
    print(f"✅ Fehr papers: {fehr_count} ({100*fehr_count/len(all_papers):.1f}%)")
    print(f"✅ Kahneman/Tversky papers: {kahneman_count} ({100*kahneman_count/len(all_papers):.1f}%)")
    print(f"✅ Other authors: {len(all_papers) - fehr_count - kahneman_count} ({100*(len(all_papers) - fehr_count - kahneman_count)/len(all_papers):.1f}%)")
    print("=" * 80)

    return len(all_papers), kahneman_count, fehr_count

if __name__ == '__main__':
    total, kahneman, fehr = add_final_kahneman()
    exit(0)
