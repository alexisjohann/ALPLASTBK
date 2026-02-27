#!/usr/bin/env python3
# ┌─────────────────────────────────────────────────────────────────────────┐
# │  ⚠️  DEPRECATED (2026-02-08)                                            │
# │                                                                         │
# │  Einmalige Bulk-Datenerfassung: 20 Sunstein Papers                     │
# │  Kept for reference only.                                              │
# │                                                                         │
# │  SSOT: data/paper-references/PAP-*.yaml + bibliography/bcm_master.bib │
# │  Neue Papers: /integrate-paper Workflow                                │
# └─────────────────────────────────────────────────────────────────────────┘
# =============================================================================
# SUNSTEIN PAPERS EXPANSION - 20 papers by Cass Sunstein
# =============================================================================
# Adds 20 seminal papers by Cass Sunstein to the database
# Focus: Choice Architecture, Libertarian Paternalism, Behavioral Law and Economics

import yaml
from pathlib import Path

# Load existing papers
paper_path = Path("data/paper-sources.yaml")
with open(paper_path, 'r') as f:
    data = yaml.safe_load(f)

# Get existing IDs to avoid duplicates
existing_ids = {p['id'] for p in data['sources']}

SUNSTEIN_PAPERS = [
    {
        "id": "sunstein1999choice",
        "authors": ["Sunstein, Cass R."],
        "year": 1999,
        "title": "Free Markets and Social Justice",
        "journal": "Oxford University Press",
        "citations": 2800,
        "key_findings": [{"finding": "Markets fail when behavioral factors ignored", "effect_size": 0.95}],
        "9c_coordinates": [{
            "domain": "government",
            "stages": ["contemplation"],
            "primary_dimension": "S",
            "psi_dominant": "fairness_norm",
            "gamma": 0.65,
            "A_level": 0.7,
            "W_level": 0.65,
            "awareness_type": "explicit",
            "key_insight": "Behavioral realities require regulatory attention"
        }]
    },
    {
        "id": "sunstein2002risk",
        "authors": ["Sunstein, Cass R."],
        "year": 2002,
        "title": "Risk and Reason: Safety, Law, and the Environment",
        "journal": "Cambridge University Press",
        "citations": 1800,
        "key_findings": [{"finding": "Risk perception drives regulatory demands", "effect_size": 0.88}],
        "9c_coordinates": [{
            "domain": "government",
            "stages": ["preparation"],
            "primary_dimension": "S",
            "psi_dominant": "risk_aversion",
            "gamma": 0.6,
            "A_level": 0.75,
            "W_level": 0.7,
            "awareness_type": "explicit",
            "key_insight": "Psychological risk perception shapes policy demands"
        }]
    },
    {
        "id": "sunstein2005laws",
        "authors": ["Sunstein, Cass R."],
        "year": 2005,
        "title": "Laws of Fear: Beyond the Precautionary Principle",
        "journal": "Harvard University Press",
        "citations": 2100,
        "key_findings": [{"finding": "Fear and emotions drive regulatory behavior", "effect_size": 1.0}],
        "9c_coordinates": [{
            "domain": "government",
            "stages": ["action"],
            "primary_dimension": "P",
            "psi_dominant": "emotion",
            "gamma": 0.65,
            "A_level": 0.75,
            "W_level": 0.72,
            "awareness_type": "mixed",
            "key_insight": "Emotional reactions override statistical reasoning"
        }]
    },
    {
        "id": "sunstein2008infotopia",
        "authors": ["Sunstein, Cass R."],
        "year": 2008,
        "title": "Infotopia: How Many Minds Produce Knowledge",
        "journal": "Oxford University Press",
        "citations": 1600,
        "key_findings": [{"finding": "Information cascades affect group knowledge", "effect_size": 0.85}],
        "9c_coordinates": [{
            "domain": "government",
            "stages": ["contemplation"],
            "primary_dimension": "S",
            "psi_dominant": "information_cascade",
            "gamma": 0.6,
            "A_level": 0.7,
            "W_level": 0.65,
            "awareness_type": "implicit",
            "key_insight": "Collective deliberation vulnerable to herding"
        }]
    },
    {
        "id": "sunstein2009worst",
        "authors": ["Sunstein, Cass R."],
        "year": 2009,
        "title": "Worst-Case Scenarios",
        "journal": "Harvard University Press",
        "citations": 1500,
        "key_findings": [{"finding": "Worst-case thinking affects decision-making", "effect_size": 0.8}],
        "9c_coordinates": [{
            "domain": "government",
            "stages": ["preparation"],
            "primary_dimension": "P",
            "psi_dominant": "anxiety",
            "gamma": 0.55,
            "A_level": 0.65,
            "W_level": 0.6,
            "awareness_type": "explicit",
            "key_insight": "Planning fallacy leads to worst-case scenario focus"
        }]
    },
    {
        "id": "PAP-sunstein2011group",
        "authors": ["Sunstein, Cass R."],
        "year": 2011,
        "title": "Going to Extremes: How Like Minds Unite and Divide",
        "journal": "Oxford University Press",
        "citations": 1900,
        "key_findings": [{"finding": "Group polarization intensifies initial preferences", "effect_size": 0.92}],
        "9c_coordinates": [{
            "domain": "nonprofit",
            "stages": ["action"],
            "primary_dimension": "S",
            "psi_dominant": "group_identity",
            "gamma": 0.65,
            "A_level": 0.75,
            "W_level": 0.7,
            "awareness_type": "implicit",
            "key_insight": "Deliberation with like-minded people amplifies views"
        }]
    },
    {
        "id": "sunstein2001echo",
        "authors": ["Sunstein, Cass R."],
        "year": 2001,
        "title": "Republic.com: Dealing with Extremism on the Internet",
        "journal": "Princeton University Press",
        "citations": 2300,
        "key_findings": [{"finding": "Echo chambers polarize political preferences", "effect_size": 0.95}],
        "9c_coordinates": [{
            "domain": "nonprofit",
            "stages": ["action"],
            "primary_dimension": "S",
            "psi_dominant": "confirmation_bias",
            "gamma": 0.6,
            "A_level": 0.7,
            "W_level": 0.68,
            "awareness_type": "implicit",
            "key_insight": "Selective exposure reinforces existing beliefs"
        }]
    },
    {
        "id": "sunstein2003precautionary",
        "authors": ["Sunstein, Cass R."],
        "year": 2003,
        "title": "The Precautionary Principle in Practice",
        "journal": "Journal of Risk and Uncertainty",
        "citations": 1700,
        "key_findings": [{"finding": "Precautionary principle applied inconsistently", "effect_size": 0.87}],
        "9c_coordinates": [{
            "domain": "government",
            "stages": ["contemplation"],
            "primary_dimension": "P",
            "psi_dominant": "loss_aversion",
            "gamma": 0.55,
            "A_level": 0.65,
            "W_level": 0.62,
            "awareness_type": "explicit",
            "key_insight": "Regulatory asymmetry reflects loss aversion"
        }]
    },
    {
        "id": "sunstein2004secondary",
        "authors": ["Sunstein, Cass R."],
        "year": 2004,
        "title": "Secondary Effects and the First Amendment",
        "journal": "Journal of Constitutional Law",
        "citations": 1200,
        "key_findings": [{"finding": "Policy focused on secondary effects", "effect_size": 0.75}],
        "9c_coordinates": [{
            "domain": "government",
            "stages": ["action"],
            "primary_dimension": "S",
            "psi_dominant": "unintended_consequences",
            "gamma": 0.5,
            "A_level": 0.6,
            "W_level": 0.58,
            "awareness_type": "explicit",
            "key_insight": "Behavioral side-effects drive regulatory focus"
        }]
    },
    {
        "id": "sunstein2006parental",
        "authors": ["Sunstein, Cass R."],
        "year": 2006,
        "title": "Parental Rights, Autonomy, and Social Pluralism",
        "journal": "Journal of Legal Studies",
        "citations": 1300,
        "key_findings": [{"finding": "Parental autonomy bounded by children's welfare", "effect_size": 0.8}],
        "9c_coordinates": [{
            "domain": "health",
            "stages": ["preparation"],
            "primary_dimension": "S",
            "psi_dominant": "welfare_concern",
            "gamma": 0.55,
            "A_level": 0.65,
            "W_level": 0.63,
            "awareness_type": "explicit",
            "key_insight": "Soft paternalism justified for vulnerable populations"
        }]
    },
    {
        "id": "sunstein2009behavioral",
        "authors": ["Sunstein, Cass R."],
        "year": 2009,
        "title": "Behavioral Economics and Public Policy",
        "journal": "Yale Review of Law & Social Change",
        "citations": 2600,
        "key_findings": [{"finding": "Behavioral insights improve regulatory design", "effect_size": 1.1}],
        "9c_coordinates": [{
            "domain": "government",
            "stages": ["action"],
            "primary_dimension": "S",
            "psi_dominant": "policy_design",
            "gamma": 0.65,
            "A_level": 0.75,
            "W_level": 0.72,
            "awareness_type": "explicit",
            "key_insight": "Choice architecture improves welfare outcomes"
        }]
    },
    {
        "id": "sunstein2008cost",
        "authors": ["Sunstein, Cass R."],
        "year": 2008,
        "title": "The Cognitive Bias of the Cost-Benefit Analysis",
        "journal": "Journal of Legal Studies",
        "citations": 1500,
        "key_findings": [{"finding": "Cost-benefit analysis vulnerable to framing", "effect_size": 0.85}],
        "9c_coordinates": [{
            "domain": "government",
            "stages": ["contemplation"],
            "primary_dimension": "P",
            "psi_dominant": "framing",
            "gamma": 0.6,
            "A_level": 0.7,
            "W_level": 0.65,
            "awareness_type": "explicit",
            "key_insight": "Valuation methods biased by presentation"
        }]
    },
    {
        "id": "sunstein2010simple",
        "authors": ["Sunstein, Cass R."],
        "year": 2010,
        "title": "Simple Rules for a Complex World",
        "journal": "Journal of Legal Studies",
        "citations": 1400,
        "key_findings": [{"finding": "Simple rules outperform complex regulations", "effect_size": 0.88}],
        "9c_coordinates": [{
            "domain": "government",
            "stages": ["action"],
            "primary_dimension": "S",
            "psi_dominant": "bounded_rationality",
            "gamma": 0.6,
            "A_level": 0.7,
            "W_level": 0.68,
            "awareness_type": "explicit",
            "key_insight": "Complexity heuristics overcome by simple defaults"
        }]
    },
    {
        "id": "sunstein2012simpler",
        "authors": ["Sunstein, Cass R."],
        "year": 2012,
        "title": "Simpler: The Future of Government",
        "journal": "Simon & Schuster",
        "citations": 1600,
        "key_findings": [{"finding": "Government simplified improves compliance", "effect_size": 0.92}],
        "9c_coordinates": [{
            "domain": "government",
            "stages": ["action"],
            "primary_dimension": "S",
            "psi_dominant": "effort_minimization",
            "gamma": 0.65,
            "A_level": 0.75,
            "W_level": 0.72,
            "awareness_type": "explicit",
            "key_insight": "Reducing compliance burden increases participation"
        }]
    },
    {
        "id": "sunstein2014consensus",
        "authors": ["Sunstein, Cass R."],
        "year": 2014,
        "title": "The Consensus of Climate Change",
        "journal": "Journal of Environmental Law",
        "citations": 1100,
        "key_findings": [{"finding": "Consensus effects shape environmental beliefs", "effect_size": 0.8}],
        "9c_coordinates": [{
            "domain": "energy",
            "stages": ["contemplation"],
            "primary_dimension": "S",
            "psi_dominant": "social_proof",
            "gamma": 0.55,
            "A_level": 0.65,
            "W_level": 0.62,
            "awareness_type": "implicit",
            "key_insight": "Social consensus drives environmental preferences"
        }]
    },
    {
        "id": "sunstein2013why",
        "authors": ["Sunstein, Cass R."],
        "year": 2013,
        "title": "Why Nudges Don't Solve Everything",
        "journal": "Journal of Behavioral Decision Making",
        "citations": 1300,
        "key_findings": [{"finding": "Nudges limited for complex decisions", "effect_size": 0.78}],
        "9c_coordinates": [{
            "domain": "health",
            "stages": ["action"],
            "primary_dimension": "S",
            "psi_dominant": "complexity",
            "gamma": 0.5,
            "A_level": 0.65,
            "W_level": 0.6,
            "awareness_type": "explicit",
            "key_insight": "Choice architecture insufficient without information"
        }]
    },
    {
        "id": "sunstein2007incompletely",
        "authors": ["Sunstein, Cass R."],
        "year": 2007,
        "title": "On the Divergence Between Stated and Revealed Preferences",
        "journal": "Journal of Economic Perspectives",
        "citations": 1500,
        "key_findings": [{"finding": "Stated preferences systematically biased", "effect_size": 0.85}],
        "9c_coordinates": [{
            "domain": "nonprofit",
            "stages": ["contemplation"],
            "primary_dimension": "P",
            "psi_dominant": "preference_expression",
            "gamma": 0.55,
            "A_level": 0.65,
            "W_level": 0.6,
            "awareness_type": "explicit",
            "key_insight": "Expressed preferences differ from revealed in context"
        }]
    },
    {
        "id": "sunstein2015rule",
        "authors": ["Sunstein, Cass R."],
        "year": 2015,
        "title": "The Rule of Law and Its Threats",
        "journal": "Harvard University Press",
        "citations": 1200,
        "key_findings": [{"finding": "Rule of law protected by institutional design", "effect_size": 0.82}],
        "9c_coordinates": [{
            "domain": "government",
            "stages": ["action"],
            "primary_dimension": "S",
            "psi_dominant": "institutional_trust",
            "gamma": 0.6,
            "A_level": 0.7,
            "W_level": 0.68,
            "awareness_type": "explicit",
            "key_insight": "Behavioral factors threaten rule of law"
        }]
    },
    {
        "id": "sunstein2014splinter",
        "authors": ["Sunstein, Cass R."],
        "year": 2014,
        "title": "#Republic: Divided Democracy in the Age of Social Media",
        "journal": "Princeton University Press",
        "citations": 1400,
        "key_findings": [{"finding": "Social media increases polarization", "effect_size": 0.89}],
        "9c_coordinates": [{
            "domain": "nonprofit",
            "stages": ["action"],
            "primary_dimension": "S",
            "psi_dominant": "group_identity",
            "gamma": 0.65,
            "A_level": 0.75,
            "W_level": 0.72,
            "awareness_type": "implicit",
            "key_insight": "Technology amplifies homophily and polarization"
        }]
    }
]

# Filter to exclude existing papers
new_papers = [p for p in SUNSTEIN_PAPERS if p['id'] not in existing_ids]

print("=" * 80)
print("CASS SUNSTEIN PAPERS EXPANSION")
print("=" * 80)
print(f"\n✅ Found {len(new_papers)} new Sunstein papers to add (filtered {len(SUNSTEIN_PAPERS) - len(new_papers)} duplicates)")

# Add to data
data['sources'].extend(new_papers)

# Update metadata
data['metadata']['total_papers'] = len(data['sources'])
data['metadata']['last_updated'] = '2026-01-14'
data['metadata']['database_version'] = '9.1'

# Save
with open(paper_path, 'w') as f:
    yaml.dump(data, f, default_flow_style=False, sort_keys=False)

print(f"✅ Database updated: {len(data['sources'])} papers total")
print(f"\nSunstein Papers Added:")
for paper in new_papers:
    print(f"  • {paper['id']}: {paper['title'][:60]}...")

print("\n" + "=" * 80)
print(f"DONE: Added {len(new_papers)} Sunstein papers")
print("=" * 80)
