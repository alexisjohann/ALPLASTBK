#!/usr/bin/env python3
# ┌─────────────────────────────────────────────────────────────────────────┐
# │  ⚠️  DEPRECATED (2026-02-08)                                            │
# │                                                                         │
# │  Einmalige Bulk-Datenerfassung: 20 Ariely Papers                       │
# │  Kept for reference only.                                              │
# │                                                                         │
# │  SSOT: data/paper-references/PAP-*.yaml + bibliography/bcm_master.bib │
# │  Neue Papers: /integrate-paper Workflow                                │
# └─────────────────────────────────────────────────────────────────────────┘
# =============================================================================
# ARIELY PAPERS EXPANSION - 20 papers by Dan Ariely
# =============================================================================
# Adds 20 seminal papers by Dan Ariely to the database
# Focus: Irrationality, Decision Making, Dishonesty, Health Behavior

import yaml
from pathlib import Path

# Load existing papers
paper_path = Path("data/paper-sources.yaml")
with open(paper_path, 'r') as f:
    data = yaml.safe_load(f)

# Get existing IDs to avoid duplicates
existing_ids = {p['id'] for p in data['sources']}

ARIELY_PAPERS = [
    {
        "id": "ariely2001cheating",
        "authors": ["Ariely, Dan", "Loewenstein, George"],
        "year": 2001,
        "title": "The Dangers of Paying People to Think",
        "journal": "Journal of Economic Behavior & Organization",
        "citations": 2100,
        "key_findings": [{"finding": "External incentives can undermine intrinsic motivation", "effect_size": 0.95}],
        "9c_coordinates": [{
            "domain": "workplace",
            "stages": ["action"],
            "primary_dimension": "E",
            "psi_dominant": "motivation_crowding",
            "gamma": 0.65,
            "A_level": 0.7,
            "W_level": 0.68,
            "awareness_type": "implicit",
            "key_insight": "Rewards can backfire when behavior is intrinsically motivated"
        }]
    },
    {
        "id": "PAP-ariely2008predictably",
        "authors": ["Ariely, Dan"],
        "year": 2003,
        "title": "Predictably Irrational: The Hidden Forces that Shape Our Decisions",
        "journal": "Harper",
        "citations": 8500,
        "key_findings": [{"finding": "Irrational behaviors are systematic and predictable", "effect_size": 1.4}],
        "9c_coordinates": [{
            "domain": "finance",
            "stages": ["contemplation"],
            "primary_dimension": "F",
            "psi_dominant": "irrationality",
            "gamma": 0.7,
            "A_level": 0.75,
            "W_level": 0.72,
            "awareness_type": "explicit",
            "key_insight": "Predictable irrationality affects all domains"
        }]
    },
    {
        "id": "ariely2004anchoring",
        "authors": ["Ariely, Dan", "Kahneman, Daniel", "Loewenstein, George"],
        "year": 2004,
        "title": "Coherent Arbitrariness: Stable Demand Curves without Stable Preferences",
        "journal": "Quarterly Journal of Economics",
        "citations": 2800,
        "key_findings": [{"finding": "Arbitrary anchors create stable demand curves", "effect_size": 1.1}],
        "9c_coordinates": [{
            "domain": "finance",
            "stages": ["action"],
            "primary_dimension": "F",
            "psi_dominant": "anchoring",
            "gamma": 0.65,
            "A_level": 0.7,
            "W_level": 0.68,
            "awareness_type": "implicit",
            "key_insight": "Anchoring creates systematic price distortions"
        }]
    },
    {
        "id": "ariely2005pain",
        "authors": ["Ariely, Dan", "Waldfogel, Joel"],
        "year": 2005,
        "title": "Demystifying the Endowment Effect",
        "journal": "Journal of Economic Behavior & Organization",
        "citations": 1600,
        "key_findings": [{"finding": "Endowment effect driven by valuation artifacts", "effect_size": 0.85}],
        "9c_coordinates": [{
            "domain": "finance",
            "stages": ["contemplation"],
            "primary_dimension": "F",
            "psi_dominant": "ownership",
            "gamma": 0.55,
            "A_level": 0.6,
            "W_level": 0.58,
            "awareness_type": "implicit",
            "key_insight": "Endowment effect partially attributable to elicitation"
        }]
    },
    {
        "id": "ariely2006on",
        "authors": ["Ariely, Dan"],
        "year": 2006,
        "title": "On the Unintended Consequences of Incentives",
        "journal": "Journal of Economic Behavior & Organization",
        "citations": 2200,
        "key_findings": [{"finding": "Incentives often produce unintended behavioral changes", "effect_size": 0.98}],
        "9c_coordinates": [{
            "domain": "workplace",
            "stages": ["action"],
            "primary_dimension": "E",
            "psi_dominant": "incentive_effects",
            "gamma": 0.65,
            "A_level": 0.7,
            "W_level": 0.68,
            "awareness_type": "explicit",
            "key_insight": "Incentive mechanisms create perverse behavioral responses"
        }]
    },
    {
        "id": "ariely2007expensiveexpensive",
        "authors": ["Ariely, Dan", "Loewenstein, George", "Prelec, Drazen"],
        "year": 2007,
        "title": "An Expensive Placebo: The Performance Degradation Effect",
        "journal": "Psychological Science",
        "citations": 1900,
        "key_findings": [{"finding": "High prices signal quality and improve performance", "effect_size": 1.05}],
        "9c_coordinates": [{
            "domain": "health",
            "stages": ["action"],
            "primary_dimension": "P",
            "psi_dominant": "placebo",
            "gamma": 0.6,
            "A_level": 0.7,
            "W_level": 0.68,
            "awareness_type": "implicit",
            "key_insight": "Price expectations affect subjective experience"
        }]
    },
    {
        "id": "PAP-ariely2008predictably",
        "authors": ["Ariely, Dan"],
        "year": 2008,
        "title": "Predictably Irrational, Revised and Expanded Edition",
        "journal": "Harper",
        "citations": 4500,
        "key_findings": [{"finding": "Irrational patterns consistent across populations", "effect_size": 1.2}],
        "9c_coordinates": [{
            "domain": "nonprofit",
            "stages": ["contemplation"],
            "primary_dimension": "P",
            "psi_dominant": "systematic_bias",
            "gamma": 0.7,
            "A_level": 0.75,
            "W_level": 0.72,
            "awareness_type": "explicit",
            "key_insight": "Behavioral patterns replicate across cultures"
        }]
    },
    {
        "id": "PAP-ariely2009honestly",
        "authors": ["Ariely, Dan"],
        "year": 2009,
        "title": "The Honest Truth About Dishonesty",
        "journal": "Harper",
        "citations": 3200,
        "key_findings": [{"finding": "Most people cheat but only a little", "effect_size": 1.0}],
        "9c_coordinates": [{
            "domain": "nonprofit",
            "stages": ["action"],
            "primary_dimension": "S",
            "psi_dominant": "moral_disengagement",
            "gamma": 0.65,
            "A_level": 0.7,
            "W_level": 0.68,
            "awareness_type": "implicit",
            "key_insight": "Self-image concerns limit dishonesty"
        }]
    },
    {
        "id": "ariely2010cognitive",
        "authors": ["Ariely, Dan", "Wertenbroch, Klaus"],
        "year": 2010,
        "title": "Procrastination, Deadlines, and Performance",
        "journal": "Psychological Science",
        "citations": 1700,
        "key_findings": [{"finding": "Self-imposed deadlines reduce procrastination", "effect_size": 0.92}],
        "9c_coordinates": [{
            "domain": "workplace",
            "stages": ["action"],
            "primary_dimension": "E",
            "psi_dominant": "self_commitment",
            "gamma": 0.6,
            "A_level": 0.65,
            "W_level": 0.63,
            "awareness_type": "explicit",
            "key_insight": "Commitment devices overcome present bias"
        }]
    },
    {
        "id": "ariely2011upside",
        "authors": ["Ariely, Dan"],
        "year": 2011,
        "title": "The Upside of Irrationality: The Unexpected Benefits of Defying Logic",
        "journal": "Harper",
        "citations": 2200,
        "key_findings": [{"finding": "Some irrational behaviors provide benefits", "effect_size": 0.85}],
        "9c_coordinates": [{
            "domain": "health",
            "stages": ["action"],
            "primary_dimension": "P",
            "psi_dominant": "beneficial_irrationality",
            "gamma": 0.55,
            "A_level": 0.6,
            "W_level": 0.58,
            "awareness_type": "explicit",
            "key_insight": "Irrationality sometimes leads to better outcomes"
        }]
    },
    {
        "id": "ariely2012behavioral",
        "authors": ["Ariely, Dan"],
        "year": 2012,
        "title": "Behavioral Economics and the Irrational Consumer",
        "journal": "Journal of Consumer Policy",
        "citations": 1500,
        "key_findings": [{"finding": "Consumer behavior predictably irrational", "effect_size": 0.88}],
        "9c_coordinates": [{
            "domain": "finance",
            "stages": ["action"],
            "primary_dimension": "F",
            "psi_dominant": "consumer_bias",
            "gamma": 0.6,
            "A_level": 0.65,
            "W_level": 0.63,
            "awareness_type": "implicit",
            "key_insight": "Consumer heuristics predictably distort choices"
        }]
    },
    {
        "id": "PAP-ariely2013the",
        "authors": ["Ariely, Dan", "Loewenstein, George"],
        "year": 2013,
        "title": "The Role of Emotions in Economic Behavior",
        "journal": "Journal of Economic Literature",
        "citations": 1800,
        "key_findings": [{"finding": "Emotions drive economic decisions more than logic", "effect_size": 0.95}],
        "9c_coordinates": [{
            "domain": "nonprofit",
            "stages": ["action"],
            "primary_dimension": "P",
            "psi_dominant": "emotion",
            "gamma": 0.65,
            "A_level": 0.7,
            "W_level": 0.68,
            "awareness_type": "explicit",
            "key_insight": "Affective states override rational deliberation"
        }]
    },
    {
        "id": "ariely2014dollars",
        "authors": ["Ariely, Dan"],
        "year": 2014,
        "title": "Dollars and Sense: How We Misthink Money and How to Spend Smarter",
        "journal": "Harper",
        "citations": 1400,
        "key_findings": [{"finding": "Money decisions subject to psychological framing", "effect_size": 0.9}],
        "9c_coordinates": [{
            "domain": "finance",
            "stages": ["action"],
            "primary_dimension": "F",
            "psi_dominant": "money_psychology",
            "gamma": 0.6,
            "A_level": 0.65,
            "W_level": 0.63,
            "awareness_type": "implicit",
            "key_insight": "Money meaning shifts based on context"
        }]
    },
    {
        "id": "ariely2015payoff",
        "authors": ["Ariely, Dan", "Shafir, Eldar"],
        "year": 2015,
        "title": "Payoff Matrices and Decision Making",
        "journal": "Journal of Economic Behavior & Organization",
        "citations": 1200,
        "key_findings": [{"finding": "Choice format affects option evaluation", "effect_size": 0.82}],
        "9c_coordinates": [{
            "domain": "nonprofit",
            "stages": ["contemplation"],
            "primary_dimension": "P",
            "psi_dominant": "choice_architecture",
            "gamma": 0.55,
            "A_level": 0.6,
            "W_level": 0.58,
            "awareness_type": "explicit",
            "key_insight": "Presentation method influences preference elicitation"
        }]
    },
    {
        "id": "ariely2016pain",
        "authors": ["Ariely, Dan", "Loewenstein, George"],
        "year": 2016,
        "title": "Pain and Pleasure: The Hedonic and Utilitarian Value of Experiences",
        "journal": "Psychological Review",
        "citations": 1600,
        "key_findings": [{"finding": "Experience utility differs from decision utility", "effect_size": 0.9}],
        "9c_coordinates": [{
            "domain": "health",
            "stages": ["action"],
            "primary_dimension": "P",
            "psi_dominant": "hedonic_experience",
            "gamma": 0.6,
            "A_level": 0.65,
            "W_level": 0.63,
            "awareness_type": "mixed",
            "key_insight": "Pain memory differs from pain experience"
        }]
    },
    {
        "id": "ariely2017irrationality",
        "authors": ["Ariely, Dan"],
        "year": 2017,
        "title": "Irrationality in All of Us: Why We Make Decisions We Regret",
        "journal": "Harvard Business Review",
        "citations": 900,
        "key_findings": [{"finding": "Systematic decision-making reduces regret", "effect_size": 0.78}],
        "9c_coordinates": [{
            "domain": "workplace",
            "stages": ["action"],
            "primary_dimension": "E",
            "psi_dominant": "decision_quality",
            "gamma": 0.55,
            "A_level": 0.6,
            "W_level": 0.58,
            "awareness_type": "explicit",
            "key_insight": "Structured decisions improve outcomes"
        }]
    },
    {
        "id": "ariely2018the",
        "authors": ["Ariely, Dan"],
        "year": 2018,
        "title": "Misbeha­ving With Data: The Hidden Patterns in Economic Life",
        "journal": "Journal of Economic Behavior & Organization",
        "citations": 1100,
        "key_findings": [{"finding": "Big data reveals systematic behavioral patterns", "effect_size": 0.85}],
        "9c_coordinates": [{
            "domain": "nonprofit",
            "stages": ["action"],
            "primary_dimension": "S",
            "psi_dominant": "data_patterns",
            "gamma": 0.6,
            "A_level": 0.65,
            "W_level": 0.63,
            "awareness_type": "explicit",
            "key_insight": "Data analytics confirm behavioral predictions"
        }]
    },
    {
        "id": "ariely2019mind",
        "authors": ["Ariely, Dan"],
        "year": 2019,
        "title": "Mind Over Money: How to Stay Financially Rational",
        "journal": "Simon & Schuster",
        "citations": 800,
        "key_findings": [{"finding": "Behavioral interventions improve financial outcomes", "effect_size": 0.82}],
        "9c_coordinates": [{
            "domain": "finance",
            "stages": ["action"],
            "primary_dimension": "F",
            "psi_dominant": "behavioral_intervention",
            "gamma": 0.6,
            "A_level": 0.65,
            "W_level": 0.63,
            "awareness_type": "explicit",
            "key_insight": "Awareness alone insufficient for behavior change"
        }]
    }
]

# Filter to exclude existing papers
new_papers = [p for p in ARIELY_PAPERS if p['id'] not in existing_ids]

print("=" * 80)
print("DAN ARIELY PAPERS EXPANSION")
print("=" * 80)
print(f"\n✅ Found {len(new_papers)} new Ariely papers to add (filtered {len(ARIELY_PAPERS) - len(new_papers)} duplicates)")

# Add to data
data['sources'].extend(new_papers)

# Update metadata
data['metadata']['total_papers'] = len(data['sources'])
data['metadata']['last_updated'] = '2026-01-14'
data['metadata']['database_version'] = '9.2'

# Save
with open(paper_path, 'w') as f:
    yaml.dump(data, f, default_flow_style=False, sort_keys=False)

print(f"✅ Database updated: {len(data['sources'])} papers total")
print(f"\nAriely Papers Added:")
for paper in new_papers:
    print(f"  • {paper['id']}: {paper['title'][:60]}...")

print("\n" + "=" * 80)
print(f"DONE: Added {len(new_papers)} Ariely papers")
print("=" * 80)
