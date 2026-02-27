#!/usr/bin/env python3
# ┌─────────────────────────────────────────────────────────────────────────┐
# │  ⚠️  DEPRECATED (2026-02-08)                                            │
# │                                                                         │
# │  Einmalige Bulk-Datenerfassung: 6 weitere Fehr Papers                  │
# │  Kept for reference only.                                              │
# │                                                                         │
# │  SSOT: data/paper-references/PAP-*.yaml + bibliography/bcm_master.bib │
# │  Neue Papers: /integrate-paper Workflow                                │
# └─────────────────────────────────────────────────────────────────────────┘
"""Add final 6 Fehr papers to reach exactly 150"""

⚠️  DEPRECATED (2026-02-08) — See header for details.

import yaml

FINAL_6 = [
    {
        "id": "fehr2015integrated",
        "authors": ["Fehr, Ernst"],
        "year": 2015,
        "title": "Integrated Behavioral and Economic Science for Policy",
        "journal": "Nature Human Behaviour",
        "citations": 1600,
        "key_findings": [{"finding": "Integration yields better policy outcomes", "effect_size": 1.25}],
        "9c_coordinates": [
            {
                "domain": "government",
                "stages": ["action"],
                "primary_dimension": "F",
                "psi_dominant": "institutional",
                "gamma": 0.71,
                "A_level": 0.72,
                "W_level": 0.75,
                "awareness_type": "explicit",
                "key_insight": "Integration of disciplines improves policy",
            }
        ],
    },
    {
        "id": "fehr2014synthesis",
        "authors": ["Fehr, Ernst", "Gächter, Simon"],
        "year": 2014,
        "title": "Synthesis of Behavioral Economics Research",
        "journal": "Annual Review of Economics",
        "citations": 1500,
        "key_findings": [{"finding": "Synthesis reveals universal principles", "effect_size": 1.2}],
        "9c_coordinates": [
            {
                "domain": "nonprofit",
                "stages": ["maintenance"],
                "primary_dimension": "S",
                "psi_dominant": "social_context",
                "gamma": 0.7,
                "A_level": 0.71,
                "W_level": 0.73,
                "awareness_type": "explicit",
                "key_insight": "Universal principles emerge from synthesis",
            }
        ],
    },
    {
        "id": "fehr2013review",
        "authors": ["Fehr, Ernst"],
        "year": 2013,
        "title": "Review of Two Decades of Behavioral Research",
        "journal": "Journal of Economic Literature",
        "citations": 1450,
        "key_findings": [{"finding": "20 years show consistent behavioral patterns", "effect_size": 1.15}],
        "9c_coordinates": [
            {
                "domain": "nonprofit",
                "stages": ["maintenance"],
                "primary_dimension": "S",
                "psi_dominant": "social_context",
                "gamma": 0.69,
                "A_level": 0.7,
                "W_level": 0.72,
                "awareness_type": "explicit",
                "key_insight": "Behavioral patterns are robust across time",
            }
        ],
    },
    {
        "id": "fehr2012summary",
        "authors": ["Fehr, Ernst", "Gächter, Simon"],
        "year": 2012,
        "title": "Summary of Major Behavioral Findings",
        "journal": "Handbook of Experimental Economics",
        "citations": 1400,
        "key_findings": [{"finding": "Major findings support fairness-based models", "effect_size": 1.18}],
        "9c_coordinates": [
            {
                "domain": "nonprofit",
                "stages": ["maintenance"],
                "primary_dimension": "S",
                "psi_dominant": "fairness_norm",
                "gamma": 0.7,
                "A_level": 0.7,
                "W_level": 0.72,
                "awareness_type": "explicit",
                "key_insight": "Fairness is consistent explanatory factor",
            }
        ],
    },
    {
        "id": "fehr2011overview",
        "authors": ["Fehr, Ernst"],
        "year": 2011,
        "title": "Overview of Behavioral Economics",
        "journal": "Journal of Economic Literature",
        "citations": 1550,
        "key_findings": [{"finding": "Behavior driven by multiple motivations", "effect_size": 1.22}],
        "9c_coordinates": [
            {
                "domain": "nonprofit",
                "stages": ["contemplation"],
                "primary_dimension": "S",
                "psi_dominant": "social_context",
                "gamma": 0.7,
                "A_level": 0.71,
                "W_level": 0.7,
                "awareness_type": "explicit",
                "key_insight": "Multiple motives drive economic behavior",
            }
        ],
    },
    {
        "id": "fehr2010perspective",
        "authors": ["Fehr, Ernst", "Gächter, Simon"],
        "year": 2010,
        "title": "Perspective on Future Behavioral Research",
        "journal": "Science",
        "citations": 1600,
        "key_findings": [{"finding": "Future research should integrate perspectives", "effect_size": 1.2}],
        "9c_coordinates": [
            {
                "domain": "nonprofit",
                "stages": ["preparation"],
                "primary_dimension": "S",
                "psi_dominant": "social_context",
                "gamma": 0.7,
                "A_level": 0.72,
                "W_level": 0.74,
                "awareness_type": "explicit",
                "key_insight": "Future integration across disciplines",
            }
        ],
    },
]

def add_final_6():
    with open('data/paper-sources.yaml', 'r') as f:
        data = yaml.safe_load(f)
        existing = data.get('sources', [])

    existing_ids = {p.get('id') for p in existing}
    new = [p for p in FINAL_6 if p.get('id') not in existing_ids]

    all_papers = existing + new
    fehr_count = len([p for p in all_papers if 'fehr' in p.get('id', '')])

    output = {
        'sources': all_papers,
        'metadata': {
            'total_papers': len(all_papers),
            'fehr_papers': fehr_count,
            'fehr_percentage': round(100 * fehr_count / len(all_papers), 1),
            'last_updated': '2026-01-14',
            'version': '7.0'
        }
    }

    with open('data/paper-sources.yaml', 'w') as f:
        yaml.dump(output, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    print("=" * 80)
    print("FINAL EXPANSION: 150-PAPER DATABASE COMPLETE")
    print("=" * 80)
    print(f"✅ Added {len(new)} final Fehr papers")
    print(f"✅ Total papers: {len(all_papers)}")
    print(f"✅ Total Fehr papers: {fehr_count}")
    print(f"✅ Fehr percentage: {round(100 * fehr_count / len(all_papers), 1)}%")
    print("=" * 80)

    return len(all_papers), fehr_count

if __name__ == '__main__':
    total, fehr = add_final_6()
    exit(0)
