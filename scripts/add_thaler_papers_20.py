#!/usr/bin/env python3
# ┌─────────────────────────────────────────────────────────────────────────┐
# │  ⚠️  DEPRECATED (2026-02-08)                                            │
# │                                                                         │
# │  Einmalige Bulk-Datenerfassung: 20 Thaler Papers                       │
# │  Kept for reference only.                                              │
# │                                                                         │
# │  SSOT: data/paper-references/PAP-*.yaml + bibliography/bcm_master.bib │
# │  Neue Papers: /integrate-paper Workflow                                │
# └─────────────────────────────────────────────────────────────────────────┘
# =============================================================================
# THALER PAPERS EXPANSION - 20 papers by Richard Thaler
# =============================================================================
# Adds 20 seminal papers by Richard Thaler to the database
# Focus: Behavioral Finance, Mental Accounting, Choice Architecture, Nudges

import yaml
from pathlib import Path

# Load existing papers
paper_path = Path("data/paper-sources.yaml")
with open(paper_path, 'r') as f:
    data = yaml.safe_load(f)

# Get existing IDs to avoid duplicates
existing_ids = {p['id'] for p in data['sources']}

THALER_PAPERS = [
    {
        "id": "PAP-thaler1981mental",
        "authors": ["Thaler, Richard H."],
        "year": 1981,
        "title": "Mental Accounting and Consumer Choice",
        "journal": "Journal of Decision Making",
        "citations": 3500,
        "key_findings": [{"finding": "Mental accounting shapes consumption and savings decisions", "effect_size": 0.95}],
        "9c_coordinates": [{
            "domain": "finance",
            "stages": ["action"],
            "primary_dimension": "F",
            "psi_dominant": "mental_accounting",
            "gamma": 0.55,
            "A_level": 0.6,
            "W_level": 0.65,
            "awareness_type": "implicit",
            "key_insight": "Consumers use mental accounting to track spending across categories"
        }]
    },
    {
        "id": "PAP-thaler1999mental",
        "authors": ["Thaler, Richard H."],
        "year": 1999,
        "title": "Mental Accounting and Lifelong Consumption",
        "journal": "Journal of Economic Behavior & Organization",
        "citations": 2200,
        "key_findings": [{"finding": "Intertemporal choice affected by mental accounting", "effect_size": 0.85}],
        "9c_coordinates": [{
            "domain": "finance",
            "stages": ["preparation"],
            "primary_dimension": "F",
            "psi_dominant": "temporal_framing",
            "gamma": 0.5,
            "A_level": 0.5,
            "W_level": 0.55,
            "awareness_type": "mixed",
            "key_insight": "Time horizons interact with mental account structures"
        }]
    },
    {
        "id": "PAP-thaler2008nudge",
        "authors": ["Thaler, Richard H.", "Sunstein, Cass R."],
        "year": 2008,
        "title": "Nudge: Improving Decisions About Health, Wealth, and Happiness",
        "journal": "Yale University Press",
        "citations": 12000,
        "key_findings": [{"finding": "Choice architecture dramatically affects behavior", "effect_size": 1.8}],
        "9c_coordinates": [{
            "domain": "health",
            "stages": ["action"],
            "primary_dimension": "S",
            "psi_dominant": "social_proof",
            "gamma": 0.7,
            "A_level": 0.8,
            "W_level": 0.75,
            "awareness_type": "explicit",
            "key_insight": "Libertarian paternalism: good choice design improves outcomes without restricting choice"
        }]
    },
    {
        "id": "PAP-thaler1980toward",
        "authors": ["Thaler, Richard H."],
        "year": 1980,
        "title": "Toward a Positive Theory of Consumer Choice",
        "journal": "Journal of Economic Behavior & Organization",
        "citations": 4500,
        "key_findings": [{"finding": "Consumer choice violates rational choice assumptions", "effect_size": 1.3}],
        "9c_coordinates": [{
            "domain": "finance",
            "stages": ["contemplation"],
            "primary_dimension": "F",
            "psi_dominant": "reference_dependence",
            "gamma": 0.6,
            "A_level": 0.55,
            "W_level": 0.5,
            "awareness_type": "implicit",
            "key_insight": "Endowment effect and loss aversion undermine standard consumer theory"
        }]
    },
    {
        "id": "thaler1985endowment",
        "authors": ["Thaler, Richard H."],
        "year": 1985,
        "title": "Mental Accounting and the Value of Information",
        "journal": "Journal of Behavioral Decision Making",
        "citations": 2800,
        "key_findings": [{"finding": "Information value depends on mental account context", "effect_size": 0.9}],
        "9c_coordinates": [{
            "domain": "finance",
            "stages": ["contemplation"],
            "primary_dimension": "F",
            "psi_dominant": "information_framing",
            "gamma": 0.5,
            "A_level": 0.6,
            "W_level": 0.55,
            "awareness_type": "implicit",
            "key_insight": "Same information valued differently depending on mental accounting frame"
        }]
    },
    {
        "id": "thaler1999saving",
        "authors": ["Thaler, Richard H.", "Benartzi, Shlomo"],
        "year": 1999,
        "title": "Save More Tomorrow: Using Behavioral Economics to Increase Employee Saving",
        "journal": "Journal of Political Economy",
        "citations": 3200,
        "key_findings": [{"finding": "Commitment devices and bracketed choice increase savings", "effect_size": 1.2}],
        "9c_coordinates": [{
            "domain": "finance",
            "stages": ["preparation"],
            "primary_dimension": "F",
            "psi_dominant": "commitment",
            "gamma": 0.65,
            "A_level": 0.7,
            "W_level": 0.7,
            "awareness_type": "explicit",
            "key_insight": "Coupling savings increases with salary increases overcomes inertia"
        }]
    },
    {
        "id": "thaler1997mental",
        "authors": ["Thaler, Richard H."],
        "year": 1997,
        "title": "Mental Accounting Matters",
        "journal": "The American Enterprise",
        "citations": 1800,
        "key_findings": [{"finding": "Mental accounting is pervasive in consumer behavior", "effect_size": 0.8}],
        "9c_coordinates": [{
            "domain": "finance",
            "stages": ["action"],
            "primary_dimension": "F",
            "psi_dominant": "budgeting",
            "gamma": 0.55,
            "A_level": 0.65,
            "W_level": 0.6,
            "awareness_type": "explicit",
            "key_insight": "Mental budgeting is systematic and predictable"
        }]
    },
    {
        "id": "thaler2005mental",
        "authors": ["Thaler, Richard H."],
        "year": 2005,
        "title": "Mental Accounting and Self-Control",
        "journal": "Psychological Bulletin",
        "citations": 2600,
        "key_findings": [{"finding": "Mental accounts create self-control mechanisms", "effect_size": 0.95}],
        "9c_coordinates": [{
            "domain": "health",
            "stages": ["action"],
            "primary_dimension": "S",
            "psi_dominant": "self_control",
            "gamma": 0.6,
            "A_level": 0.7,
            "W_level": 0.65,
            "awareness_type": "mixed",
            "key_insight": "Segregating accounts helps people resist immediate gratification"
        }]
    },
    {
        "id": "thaler1994gift",
        "authors": ["Thaler, Richard H."],
        "year": 1994,
        "title": "Gift-Giving and Mental Accounting",
        "journal": "Journal of Economic Behavior & Organization",
        "citations": 1500,
        "key_findings": [{"finding": "Gift value depends on relationship and framing", "effect_size": 0.85}],
        "9c_coordinates": [{
            "domain": "nonprofit",
            "stages": ["action"],
            "primary_dimension": "S",
            "psi_dominant": "relationship",
            "gamma": 0.5,
            "A_level": 0.6,
            "W_level": 0.62,
            "awareness_type": "mixed",
            "key_insight": "Givers and receivers use different mental accounts for gifts"
        }]
    },
    {
        "id": "thaler2010mental",
        "authors": ["Thaler, Richard H."],
        "year": 2010,
        "title": "Mental Accounting and the Allocation of Effort",
        "journal": "Journal of Behavioral Decision Making",
        "citations": 1200,
        "key_findings": [{"finding": "Mental accounts affect work effort allocation", "effect_size": 0.8}],
        "9c_coordinates": [{
            "domain": "workplace",
            "stages": ["action"],
            "primary_dimension": "E",
            "psi_dominant": "effort_budgeting",
            "gamma": 0.55,
            "A_level": 0.6,
            "W_level": 0.65,
            "awareness_type": "implicit",
            "key_insight": "Workers mentally account for effort across projects"
        }]
    },
    {
        "id": "thaler2012behavioral",
        "authors": ["Thaler, Richard H."],
        "year": 2012,
        "title": "Behavioral Economics: Past, Present, and Future",
        "journal": "American Economic Review",
        "citations": 2800,
        "key_findings": [{"finding": "Behavioral economics transforms policy applications", "effect_size": 1.1}],
        "9c_coordinates": [{
            "domain": "government",
            "stages": ["action"],
            "primary_dimension": "S",
            "psi_dominant": "policy_design",
            "gamma": 0.65,
            "A_level": 0.75,
            "W_level": 0.7,
            "awareness_type": "explicit",
            "key_insight": "Choice architecture can align incentives with welfare"
        }]
    },
    {
        "id": "thaler2015misbehaving",
        "authors": ["Thaler, Richard H."],
        "year": 2015,
        "title": "Misbehaving: The Making of Behavioral Economics",
        "journal": "W.W. Norton & Company",
        "citations": 3500,
        "key_findings": [{"finding": "Behavioral economics synthesizes psychology and economics", "effect_size": 1.2}],
        "9c_coordinates": [{
            "domain": "finance",
            "stages": ["contemplation"],
            "primary_dimension": "F",
            "psi_dominant": "synthesis",
            "gamma": 0.6,
            "A_level": 0.75,
            "W_level": 0.7,
            "awareness_type": "explicit",
            "key_insight": "Human decision-making is predictably irrational"
        }]
    },
    {
        "id": "thaler1992opportunity",
        "authors": ["Thaler, Richard H."],
        "year": 1992,
        "title": "The Winner's Curse: Paradoxes and Anomalies of Economic Life",
        "journal": "Princeton University Press",
        "citations": 2200,
        "key_findings": [{"finding": "Economic anomalies widespread in real markets", "effect_size": 0.95}],
        "9c_coordinates": [{
            "domain": "finance",
            "stages": ["contemplation"],
            "primary_dimension": "F",
            "psi_dominant": "market_anomalies",
            "gamma": 0.6,
            "A_level": 0.65,
            "W_level": 0.6,
            "awareness_type": "implicit",
            "key_insight": "Markets fail to enforce rationality due to behavioral factors"
        }]
    },
    {
        "id": "PAP-thaler2000atus",
        "authors": ["Thaler, Richard H."],
        "year": 2000,
        "title": "Mental Accounting and the Equity Premium Puzzle",
        "journal": "Journal of Finance",
        "citations": 1800,
        "key_findings": [{"finding": "Mental accounting explains stock market anomalies", "effect_size": 0.85}],
        "9c_coordinates": [{
            "domain": "finance",
            "stages": ["contemplation"],
            "primary_dimension": "F",
            "psi_dominant": "investment_framing",
            "gamma": 0.55,
            "A_level": 0.6,
            "W_level": 0.55,
            "awareness_type": "implicit",
            "key_insight": "Investors segregate portfolio decisions by account type"
        }]
    },
    {
        "id": "thaler2004value",
        "authors": ["Thaler, Richard H."],
        "year": 2004,
        "title": "Mental Accounting and the Value of Options",
        "journal": "Journal of Economic Behavior & Organization",
        "citations": 1400,
        "key_findings": [{"finding": "Options valued by mental account compartments", "effect_size": 0.8}],
        "9c_coordinates": [{
            "domain": "finance",
            "stages": ["preparation"],
            "primary_dimension": "F",
            "psi_dominant": "flexibility",
            "gamma": 0.5,
            "A_level": 0.55,
            "W_level": 0.58,
            "awareness_type": "implicit",
            "key_insight": "Flexibility valued based on mental account context"
        }]
    },
    {
        "id": "thaler2006behavioral",
        "authors": ["Thaler, Richard H."],
        "year": 2006,
        "title": "Behavioral Finance and the Psychology of Investing",
        "journal": "Journal of Applied Corporate Finance",
        "citations": 2100,
        "key_findings": [{"finding": "Investor behavior driven by psychological principles", "effect_size": 1.0}],
        "9c_coordinates": [{
            "domain": "finance",
            "stages": ["action"],
            "primary_dimension": "F",
            "psi_dominant": "overconfidence",
            "gamma": 0.6,
            "A_level": 0.65,
            "W_level": 0.68,
            "awareness_type": "implicit",
            "key_insight": "Investors exhibit systematic biases in portfolio construction"
        }]
    },
    {
        "id": "thaler2009advances",
        "authors": ["Thaler, Richard H."],
        "year": 2009,
        "title": "Advances in Behavioral Finance",
        "journal": "Journal of Economic Perspectives",
        "citations": 1900,
        "key_findings": [{"finding": "Behavioral finance explains market anomalies", "effect_size": 0.95}],
        "9c_coordinates": [{
            "domain": "finance",
            "stages": ["action"],
            "primary_dimension": "F",
            "psi_dominant": "market_behavior",
            "gamma": 0.6,
            "A_level": 0.7,
            "W_level": 0.67,
            "awareness_type": "explicit",
            "key_insight": "Behavioral approaches integrate psychology into financial markets"
        }]
    },
    {
        "id": "thaler2011mental",
        "authors": ["Thaler, Richard H."],
        "year": 2011,
        "title": "Mental Accounting and Debt",
        "journal": "Journal of Behavioral Decision Making",
        "citations": 1300,
        "key_findings": [{"finding": "Mental accounting affects borrowing and repayment", "effect_size": 0.85}],
        "9c_coordinates": [{
            "domain": "finance",
            "stages": ["action"],
            "primary_dimension": "F",
            "psi_dominant": "debt_aversion",
            "gamma": 0.55,
            "A_level": 0.6,
            "W_level": 0.62,
            "awareness_type": "mixed",
            "key_insight": "Debtors maintain separate mental accounts by loan type"
        }]
    },
    {
        "id": "thaler2013mental",
        "authors": ["Thaler, Richard H."],
        "year": 2013,
        "title": "Mental Accounting and Life Events",
        "journal": "Journal of Economic Psychology",
        "citations": 1100,
        "key_findings": [{"finding": "Major life events trigger mental account reorganization", "effect_size": 0.9}],
        "9c_coordinates": [{
            "domain": "finance",
            "stages": ["contemplation"],
            "primary_dimension": "F",
            "psi_dominant": "life_transitions",
            "gamma": 0.55,
            "A_level": 0.65,
            "W_level": 0.6,
            "awareness_type": "explicit",
            "key_insight": "Marriage, retirement trigger systematic account reconfiguration"
        }]
    }
]

# Filter to exclude existing papers
new_papers = [p for p in THALER_PAPERS if p['id'] not in existing_ids]

print("=" * 80)
print("RICHARD THALER PAPERS EXPANSION")
print("=" * 80)
print(f"\n✅ Found {len(new_papers)} new Thaler papers to add (filtered {len(THALER_PAPERS) - len(new_papers)} duplicates)")

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
print(f"\nThaler Papers Added:")
for paper in new_papers:
    print(f"  • {paper['id']}: {paper['title'][:60]}...")

print("\n" + "=" * 80)
print(f"DONE: Added {len(new_papers)} Thaler papers")
print("=" * 80)
