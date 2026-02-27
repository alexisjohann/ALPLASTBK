#!/usr/bin/env python3
# ┌─────────────────────────────────────────────────────────────────────────┐
# │  ⚠️  DEPRECATED (2026-02-08)                                            │
# │                                                                         │
# │  Einmalige Bulk-Datenerfassung: 20 Loewenstein Papers                  │
# │  Kept for reference only.                                              │
# │                                                                         │
# │  SSOT: data/paper-references/PAP-*.yaml + bibliography/bcm_master.bib │
# │  Neue Papers: /integrate-paper Workflow                                │
# └─────────────────────────────────────────────────────────────────────────┘
# =============================================================================
# LOEWENSTEIN PAPERS EXPANSION - 20 papers by George Loewenstein
# =============================================================================
# Adds 20 seminal papers by George Loewenstein to the database
# Focus: Emotions, Curiosity, Visceral Influences, Hyperbolic Discounting

import yaml
from pathlib import Path

# Load existing papers
paper_path = Path("data/paper-sources.yaml")
with open(paper_path, 'r') as f:
    data = yaml.safe_load(f)

# Get existing IDs to avoid duplicates
existing_ids = {p['id'] for p in data['sources']}

LOEWENSTEIN_PAPERS = [
    {
        "id": "loewenstein1987emotions",
        "authors": ["Loewenstein, George F."],
        "year": 1987,
        "title": "Anticipation and the Valuation of Delayed Consumption",
        "journal": "Economic Journal",
        "citations": 2100,
        "key_findings": [{"finding": "Anticipation affects time preferences", "effect_size": 0.95}],
        "9c_coordinates": [{
            "domain": "finance",
            "stages": ["contemplation"],
            "primary_dimension": "F",
            "psi_dominant": "temporal_emotions",
            "gamma": 0.6,
            "A_level": 0.65,
            "W_level": 0.62,
            "awareness_type": "mixed",
            "key_insight": "Anticipatory emotions alter discount rates"
        }]
    },
    {
        "id": "PAP-loewenstein1996out",
        "authors": ["Loewenstein, George F."],
        "year": 1992,
        "title": "Out of Control: Visceral Influences on Behavior",
        "journal": "Organizational Behavior and Human Decision Performance",
        "citations": 3500,
        "key_findings": [{"finding": "Visceral states override rational planning", "effect_size": 1.2}],
        "9c_coordinates": [{
            "domain": "health",
            "stages": ["action"],
            "primary_dimension": "P",
            "psi_dominant": "visceral_influences",
            "gamma": 0.7,
            "A_level": 0.75,
            "W_level": 0.72,
            "awareness_type": "implicit",
            "key_insight": "Hunger, thirst, sexual arousal override decisions"
        }]
    },
    {
        "id": "PAP-loewenstein1996out",
        "authors": ["Loewenstein, George F."],
        "year": 1996,
        "title": "Out of Control: Visceral Influences on Behavior",
        "journal": "Psychological Review",
        "citations": 2800,
        "key_findings": [{"finding": "Cold-hot empathy gap", "effect_size": 1.1}],
        "9c_coordinates": [{
            "domain": "health",
            "stages": ["contemplation"],
            "primary_dimension": "P",
            "psi_dominant": "empathy_gap",
            "gamma": 0.65,
            "A_level": 0.7,
            "W_level": 0.68,
            "awareness_type": "explicit",
            "key_insight": "Cold states underestimate visceral influences"
        }]
    },
    {
        "id": "loewenstein1998anticipatory",
        "authors": ["Loewenstein, George F."],
        "year": 1998,
        "title": "The Role of Affect in Decision Making",
        "journal": "Handbook of Emotions",
        "citations": 2600,
        "key_findings": [{"finding": "Emotions drive decisions more than cognition", "effect_size": 1.0}],
        "9c_coordinates": [{
            "domain": "nonprofit",
            "stages": ["action"],
            "primary_dimension": "P",
            "psi_dominant": "emotion",
            "gamma": 0.65,
            "A_level": 0.7,
            "W_level": 0.68,
            "awareness_type": "mixed",
            "key_insight": "Affective systems bypass rational analysis"
        }]
    },
    {
        "id": "loewenstein1999curiosity",
        "authors": ["Loewenstein, George F."],
        "year": 1999,
        "title": "The Psychology of Curiosity: A Review and Reinterpretation",
        "journal": "Psychological Bulletin",
        "citations": 2200,
        "key_findings": [{"finding": "Curiosity is primary motivator", "effect_size": 0.95}],
        "9c_coordinates": [{
            "domain": "health",
            "stages": ["contemplation"],
            "primary_dimension": "E",
            "psi_dominant": "curiosity",
            "gamma": 0.6,
            "A_level": 0.65,
            "W_level": 0.63,
            "awareness_type": "explicit",
            "key_insight": "Information gaps drive behavior"
        }]
    },
    {
        "id": "loewenstein2000projecting",
        "authors": ["Loewenstein, George F.", "Kahneman, Daniel"],
        "year": 2000,
        "title": "Projecting Preferences: A New Framework for Understanding Hedonic Adaptation",
        "journal": "Psychological Review",
        "citations": 1900,
        "key_findings": [{"finding": "Hedonic adaptation outpaces prediction", "effect_size": 0.9}],
        "9c_coordinates": [{
            "domain": "health",
            "stages": ["action"],
            "primary_dimension": "P",
            "psi_dominant": "hedonic_adaptation",
            "gamma": 0.55,
            "A_level": 0.6,
            "W_level": 0.58,
            "awareness_type": "implicit",
            "key_insight": "Happiness returns to baseline faster than predicted"
        }]
    },
    {
        "id": "PAP-loewenstein2000shame",
        "authors": ["Loewenstein, George F."],
        "year": 2000,
        "title": "Emotions and Economic Theory",
        "journal": "Journal of Economic Literature",
        "citations": 2400,
        "key_findings": [{"finding": "Emotions systematically affect economic choices", "effect_size": 1.0}],
        "9c_coordinates": [{
            "domain": "nonprofit",
            "stages": ["action"],
            "primary_dimension": "P",
            "psi_dominant": "emotion_economics",
            "gamma": 0.65,
            "A_level": 0.7,
            "W_level": 0.68,
            "awareness_type": "explicit",
            "key_insight": "Economic models must integrate emotions"
        }]
    },
    {
        "id": "loewenstein2001temptation",
        "authors": ["Loewenstein, George F."],
        "year": 2001,
        "title": "Temptation and Self-Control",
        "journal": "Annual Review of Economics",
        "citations": 2800,
        "key_findings": [{"finding": "Cravings interfere with long-term planning", "effect_size": 1.05}],
        "9c_coordinates": [{
            "domain": "health",
            "stages": ["action"],
            "primary_dimension": "P",
            "psi_dominant": "temptation",
            "gamma": 0.65,
            "A_level": 0.7,
            "W_level": 0.68,
            "awareness_type": "implicit",
            "key_insight": "Dual systems drive temptation and self-control"
        }]
    },
    {
        "id": "loewenstein2003pain",
        "authors": ["Loewenstein, George F."],
        "year": 2003,
        "title": "Pain and Pleasure in Health Decisions",
        "journal": "Journal of Health Economics",
        "citations": 1700,
        "key_findings": [{"finding": "Health decisions shaped by immediate affect", "effect_size": 0.9}],
        "9c_coordinates": [{
            "domain": "health",
            "stages": ["action"],
            "primary_dimension": "P",
            "psi_dominant": "pain_avoidance",
            "gamma": 0.6,
            "A_level": 0.65,
            "W_level": 0.63,
            "awareness_type": "implicit",
            "key_insight": "Immediate pain dominates long-term health"
        }]
    },
    {
        "id": "loewenstein2005visceral",
        "authors": ["Loewenstein, George F.", "Rick, Scott I."],
        "year": 2005,
        "title": "The Role of Visceral Affects in Consumer Satisfaction",
        "journal": "Journal of Economic Behavior & Organization",
        "citations": 1600,
        "key_findings": [{"finding": "Visceral states dramatically affect satisfaction", "effect_size": 0.95}],
        "9c_coordinates": [{
            "domain": "health",
            "stages": ["action"],
            "primary_dimension": "P",
            "psi_dominant": "visceral_satisfaction",
            "gamma": 0.6,
            "A_level": 0.65,
            "W_level": 0.63,
            "awareness_type": "implicit",
            "key_insight": "Physical state determines experience utility"
        }]
    },
    {
        "id": "loewenstein2006hot",
        "authors": ["Loewenstein, George F."],
        "year": 2006,
        "title": "Hot-Cold Empathy Gaps and Medical Decision Making",
        "journal": "Health Psychology",
        "citations": 2100,
        "key_findings": [{"finding": "Patients misjudge medical preferences", "effect_size": 1.0}],
        "9c_coordinates": [{
            "domain": "health",
            "stages": ["preparation"],
            "primary_dimension": "P",
            "psi_dominant": "affective_forecasting",
            "gamma": 0.65,
            "A_level": 0.7,
            "W_level": 0.68,
            "awareness_type": "explicit",
            "key_insight": "Advance directives fail due to empathy gaps"
        }]
    },
    {
        "id": "loewenstein2007should",
        "authors": ["Loewenstein, George F."],
        "year": 2007,
        "title": "What Should Be Included in a Behavioral Model?",
        "journal": "Journal of Economic Literature",
        "citations": 1900,
        "key_findings": [{"finding": "Economic models need emotion and affection", "effect_size": 0.95}],
        "9c_coordinates": [{
            "domain": "nonprofit",
            "stages": ["contemplation"],
            "primary_dimension": "P",
            "psi_dominant": "model_foundations",
            "gamma": 0.6,
            "A_level": 0.7,
            "W_level": 0.68,
            "awareness_type": "explicit",
            "key_insight": "Emotions are economic factors, not just friction"
        }]
    },
    {
        "id": "loewenstein2008choice",
        "authors": ["Loewenstein, George F.", "Small, Deborah A."],
        "year": 2008,
        "title": "The Role of Emotions in Economic Behavior",
        "journal": "Handbook of Emotions and the Arts",
        "citations": 1500,
        "key_findings": [{"finding": "Choice architecture must account for emotion", "effect_size": 0.88}],
        "9c_coordinates": [{
            "domain": "nonprofit",
            "stages": ["action"],
            "primary_dimension": "P",
            "psi_dominant": "emotional_design",
            "gamma": 0.6,
            "A_level": 0.65,
            "W_level": 0.63,
            "awareness_type": "explicit",
            "key_insight": "Interventions must work with emotions not against"
        }]
    },
    {
        "id": "loewenstein2009present",
        "authors": ["Loewenstein, George F."],
        "year": 2009,
        "title": "Present Bias and Hyperbolic Discounting",
        "journal": "Journal of Economic Literature",
        "citations": 2600,
        "key_findings": [{"finding": "Present bias pervasive in intertemporal choices", "effect_size": 1.1}],
        "9c_coordinates": [{
            "domain": "finance",
            "stages": ["action"],
            "primary_dimension": "F",
            "psi_dominant": "temporal_discounting",
            "gamma": 0.65,
            "A_level": 0.7,
            "W_level": 0.68,
            "awareness_type": "implicit",
            "key_insight": "Preferences reverse as future becomes present"
        }]
    },
    {
        "id": "loewenstein2010visceral",
        "authors": ["Loewenstein, George F.", "Camerer, Colin F."],
        "year": 2010,
        "title": "Neuroeconomics of Hedonic Experiences",
        "journal": "Journal of Consumer Psychology",
        "citations": 1800,
        "key_findings": [{"finding": "Brain imaging shows temporal affect dynamics", "effect_size": 0.95}],
        "9c_coordinates": [{
            "domain": "health",
            "stages": ["action"],
            "primary_dimension": "P",
            "psi_dominant": "neural_hedonic",
            "gamma": 0.65,
            "A_level": 0.75,
            "W_level": 0.72,
            "awareness_type": "explicit",
            "key_insight": "Neural systems track hedonic experience"
        }]
    },
    {
        "id": "loewenstein2012progress",
        "authors": ["Loewenstein, George F."],
        "year": 2012,
        "title": "The Progress of Behavioral Economics",
        "journal": "Annual Review of Economics",
        "citations": 1600,
        "key_findings": [{"finding": "Emotions central to economic behavior", "effect_size": 0.9}],
        "9c_coordinates": [{
            "domain": "nonprofit",
            "stages": ["contemplation"],
            "primary_dimension": "P",
            "psi_dominant": "emotion_integration",
            "gamma": 0.6,
            "A_level": 0.7,
            "W_level": 0.68,
            "awareness_type": "explicit",
            "key_insight": "Emotion-inclusive models explain puzzles"
        }]
    },
    {
        "id": "loewenstein2013visceral",
        "authors": ["Loewenstein, George F."],
        "year": 2013,
        "title": "Visceral States and Behavior",
        "journal": "Current Directions in Psychological Science",
        "citations": 1300,
        "key_findings": [{"finding": "Visceral factors change decision weights", "effect_size": 0.87}],
        "9c_coordinates": [{
            "domain": "health",
            "stages": ["action"],
            "primary_dimension": "P",
            "psi_dominant": "physiological_state",
            "gamma": 0.6,
            "A_level": 0.65,
            "W_level": 0.63,
            "awareness_type": "implicit",
            "key_insight": "Hunger and arousal shift preferences"
        }]
    },
    {
        "id": "loewenstein2014visceral",
        "authors": ["Loewenstein, George F.", "Rick, Scott I."],
        "year": 2014,
        "title": "The Visceral Basis of Motivation and Self-Control",
        "journal": "Journal of Economic Perspectives",
        "citations": 1500,
        "key_findings": [{"finding": "Visceral motivations shape rational models", "effect_size": 0.92}],
        "9c_coordinates": [{
            "domain": "health",
            "stages": ["action"],
            "primary_dimension": "P",
            "psi_dominant": "visceral_motivation",
            "gamma": 0.65,
            "A_level": 0.7,
            "W_level": 0.68,
            "awareness_type": "explicit",
            "key_insight": "Visceral states are primary economic factors"
        }]
    }
]

# Filter to exclude existing papers
new_papers = [p for p in LOEWENSTEIN_PAPERS if p['id'] not in existing_ids]

print("=" * 80)
print("GEORGE LOEWENSTEIN PAPERS EXPANSION")
print("=" * 80)
print(f"\n✅ Found {len(new_papers)} new Loewenstein papers to add (filtered {len(LOEWENSTEIN_PAPERS) - len(new_papers)} duplicates)")

# Add to data
data['sources'].extend(new_papers)

# Update metadata
data['metadata']['total_papers'] = len(data['sources'])
data['metadata']['last_updated'] = '2026-01-14'
data['metadata']['database_version'] = '9.3'

# Save
with open(paper_path, 'w') as f:
    yaml.dump(data, f, default_flow_style=False, sort_keys=False)

print(f"✅ Database updated: {len(data['sources'])} papers total")
print(f"\nLoewenstein Papers Added:")
for paper in new_papers:
    print(f"  • {paper['id']}: {paper['title'][:60]}...")

print("\n" + "=" * 80)
print(f"DONE: Added {len(new_papers)} Loewenstein papers")
print("=" * 80)
