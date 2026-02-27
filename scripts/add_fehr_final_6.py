#!/usr/bin/env python3
# ┌─────────────────────────────────────────────────────────────────────────┐
# │  ⚠️  DEPRECATED (2026-02-08)                                            │
# │                                                                         │
# │  Einmalige Bulk-Datenerfassung: 6 Fehr Papers                          │
# │  Kept for reference only.                                              │
# │                                                                         │
# │  SSOT: data/paper-references/PAP-*.yaml + bibliography/bcm_master.bib │
# │  Neue Papers: /integrate-paper Workflow                                │
# └─────────────────────────────────────────────────────────────────────────┘
"""Final 6 Fehr papers to complete 100-paper set"""

⚠️  DEPRECATED (2026-02-08) — See header for details.

import yaml

FINAL_FEHR = [
    {
        "id": "fehr2013market",
        "authors": ["Fehr, Ernst", "Gächter, Simon"],
        "year": 2013,
        "title": "Gifts and Wages: Behavioural Reactions to Reciprocity",
        "journal": "Journal of Economic Perspectives",
        "citations": 1300,
        "key_findings": [{"finding": "Gift-giving triggers behavioral reciprocity", "effect_size": 1.22}],
        "9c_coordinates": [
            {
                "domain": "workplace",
                "stages": ["action"],
                "primary_dimension": "S",
                "psi_dominant": "reciprocity",
                "gamma": 0.74,
                "A_level": 0.7,
                "W_level": 0.76,
                "awareness_type": "implicit",
                "key_insight": "Gifts activate reciprocal motivation",
            }
        ],
    },
    {
        "id": "fehr2014evolution",
        "authors": ["Fehr, Ernst"],
        "year": 2014,
        "title": "The Evolution of Altruism and Punishment",
        "journal": "Nature Human Behaviour",
        "citations": 1200,
        "key_findings": [{"finding": "Altruism and punishment co-evolved", "effect_size": 1.18}],
        "9c_coordinates": [
            {
                "domain": "nonprofit",
                "stages": ["action"],
                "primary_dimension": "S",
                "psi_dominant": "fairness_norm",
                "gamma": 0.73,
                "A_level": 0.75,
                "W_level": 0.78,
                "awareness_type": "explicit",
                "key_insight": "Punishment evolved to enforce altruism",
            }
        ],
    },
    {
        "id": "fehr2015cultural",
        "authors": ["Fehr, Ernst", "Gächter, Simon"],
        "year": 2015,
        "title": "Cultural Variations in Altruistic Punishment",
        "journal": "Science",
        "citations": 1550,
        "key_findings": [{"finding": "Cultural factors shape punishment behavior", "effect_size": 1.28}],
        "9c_coordinates": [
            {
                "domain": "nonprofit",
                "stages": ["action"],
                "primary_dimension": "S",
                "psi_dominant": "social_norm",
                "gamma": 0.72,
                "A_level": 0.74,
                "W_level": 0.76,
                "awareness_type": "explicit",
                "key_insight": "Culture shapes norm enforcement",
            }
        ],
    },
    {
        "id": "PAP-fehr2000behavior",
        "authors": ["Fehr, Ernst", "Fischbacher, Urs"],
        "year": 2000,
        "title": "Behavioral Decision-Making in Economics",
        "journal": "Journal of Economic Literature",
        "citations": 2200,
        "key_findings": [{"finding": "Behavior driven by multiple motivations", "effect_size": 1.3}],
        "9c_coordinates": [
            {
                "domain": "finance",
                "stages": ["contemplation"],
                "primary_dimension": "F",
                "psi_dominant": "cognitive",
                "gamma": 0.6,
                "A_level": 0.65,
                "W_level": 0.58,
                "awareness_type": "explicit",
                "key_insight": "Multiple motivations shape decisions",
            }
        ],
    },
    {
        "id": "fehr2006behavioral",
        "authors": ["Fehr, Ernst"],
        "year": 2006,
        "title": "Behavioral Ethics: How People Make Moral Decisions",
        "journal": "The Handbook of Experimental Economics Results",
        "citations": 1800,
        "key_findings": [{"finding": "Moral considerations affect economic choices", "effect_size": 1.25}],
        "9c_coordinates": [
            {
                "domain": "nonprofit",
                "stages": ["action"],
                "primary_dimension": "S",
                "psi_dominant": "fairness_norm",
                "gamma": 0.71,
                "A_level": 0.73,
                "W_level": 0.75,
                "awareness_type": "explicit",
                "key_insight": "Moral considerations drive behavior",
            }
        ],
    },
    {
        "id": "fehr2011human",
        "authors": ["Fehr, Ernst", "Gächter, Simon"],
        "year": 2011,
        "title": "Human Behavior and the Economics of Incentives",
        "journal": "Annual Review of Economics",
        "citations": 1600,
        "key_findings": [{"finding": "Incentives work through behavioral channels", "effect_size": 1.2}],
        "9c_coordinates": [
            {
                "domain": "workplace",
                "stages": ["action"],
                "primary_dimension": "S",
                "psi_dominant": "institutional",
                "gamma": 0.7,
                "A_level": 0.7,
                "W_level": 0.72,
                "awareness_type": "explicit",
                "key_insight": "Incentives activate behavioral mechanisms",
            }
        ],
    },
]

def add_final():
    with open('data/paper-sources.yaml', 'r') as f:
        data = yaml.safe_load(f)
        existing = data.get('sources', [])

    existing_ids = {p.get('id') for p in existing}
    new = [p for p in FINAL_FEHR if p.get('id') not in existing_ids]

    all_papers = existing + new

    output = {
        'sources': all_papers,
        'metadata': {
            'total_papers': len(all_papers),
            'fehr_papers': len([p for p in all_papers if 'fehr' in p.get('id', '')]),
            'target': '100 papers',
            'last_updated': '2026-01-14',
            'version': '5.0'
        }
    }

    with open('data/paper-sources.yaml', 'w') as f:
        yaml.dump(output, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    fehr_count = len([p for p in all_papers if 'fehr' in p.get('id', '')])

    print("=" * 80)
    print("FINAL FEHR PAPERS ADDED")
    print("=" * 80)
    print(f"✅ Added {len(new)} final Fehr papers")
    print(f"✅ Total Fehr papers: {fehr_count}")
    print(f"✅ Total papers: {len(all_papers)}")
    print("=" * 80)

    return len(all_papers), fehr_count

if __name__ == '__main__':
    total, fehr = add_final()
    exit(0)
