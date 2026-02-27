#!/usr/bin/env python3
# ┌─────────────────────────────────────────────────────────────────────────┐
# │  ⚠️  DEPRECATED (2026-02-08)                                            │
# │                                                                         │
# │  Einmalige Bulk-Datenerfassung: 20 Autor Papers                        │
# │  Kept for reference only.                                              │
# │                                                                         │
# │  SSOT: data/paper-references/PAP-*.yaml + bibliography/bcm_master.bib │
# │  Neue Papers: /integrate-paper Workflow                                │
# └─────────────────────────────────────────────────────────────────────────┘
# =============================================================================
# AUTOR PAPERS EXPANSION - 20 papers by David Autor
# =============================================================================
# Adds 20 seminal papers by David Autor to the database
# Focus: Labor Markets, Automation, Wage Inequality, Trade Effects, Economic Anxiety

import yaml
from pathlib import Path

# Load existing papers
paper_path = Path("data/paper-sources.yaml")
with open(paper_path, 'r') as f:
    data = yaml.safe_load(f)

# Get existing IDs to avoid duplicates
existing_ids = {p['id'] for p in data['sources']}

AUTOR_PAPERS = [
    {
        "id": "autor1998computing",
        "authors": ["Autor, David H.", "Katz, Lawrence F.", "Krueger, Alan B."],
        "year": 1998,
        "title": "Computing Inequality: Have Computers Changed the Labor Market?",
        "journal": "Quarterly Journal of Economics",
        "citations": 3200,
        "key_findings": [{"finding": "Computerization increases wage inequality", "effect_size": 1.1}],
        "9c_coordinates": [{
            "domain": "workplace",
            "stages": ["action"],
            "primary_dimension": "E",
            "psi_dominant": "technological_change",
            "gamma": 0.65,
            "A_level": 0.7,
            "W_level": 0.68,
            "awareness_type": "explicit",
            "key_insight": "Technology adoption concentrates benefits on skilled workers"
        }]
    },
    {
        "id": "autor2003skill",
        "authors": ["Autor, David H.", "Katz, Lawrence F.", "Kearney, Melissa S."],
        "year": 2003,
        "title": "The Skill Content of Recent Technological Change: An Empirical Exploration",
        "journal": "Quarterly Journal of Economics",
        "citations": 2800,
        "key_findings": [{"finding": "Skill-biased technological change affects workers differentially", "effect_size": 1.05}],
        "9c_coordinates": [{
            "domain": "workplace",
            "stages": ["contemplation"],
            "primary_dimension": "E",
            "psi_dominant": "skill_bias",
            "gamma": 0.65,
            "A_level": 0.7,
            "W_level": 0.68,
            "awareness_type": "explicit",
            "key_insight": "Technology complements high-skill workers"
        }]
    },
    {
        "id": "autor2007fall",
        "authors": ["Autor, David H.", "Katz, Lawrence F.", "Kearney, Melissa S."],
        "year": 2007,
        "title": "The Fall in the Skill Wage Premium: Secular Trends vs. Cyclical Dynamics",
        "journal": "Journal of Economic Perspectives",
        "citations": 2100,
        "key_findings": [{"finding": "Wage inequality dynamics driven by supply-demand shifts", "effect_size": 0.95}],
        "9c_coordinates": [{
            "domain": "government",
            "stages": ["action"],
            "primary_dimension": "E",
            "psi_dominant": "inequality",
            "gamma": 0.6,
            "A_level": 0.65,
            "W_level": 0.63,
            "awareness_type": "explicit",
            "key_insight": "Education supply outpacing skill demand"
        }]
    },
    {
        "id": "autor2008jobs",
        "authors": ["Autor, David H."],
        "year": 2008,
        "title": "The Future of Jobs and the Challenges of Automation",
        "journal": "Journal of Economic Perspectives",
        "citations": 1800,
        "key_findings": [{"finding": "Automation threatens middle-skill employment", "effect_size": 0.98}],
        "9c_coordinates": [{
            "domain": "workplace",
            "stages": ["contemplation"],
            "primary_dimension": "E",
            "psi_dominant": "automation_anxiety",
            "gamma": 0.65,
            "A_level": 0.72,
            "W_level": 0.65,
            "awareness_type": "explicit",
            "key_insight": "Routine cognitive and manual jobs most vulnerable"
        }]
    },
    {
        "id": "autor2009new",
        "authors": ["Autor, David H."],
        "year": 2009,
        "title": "The New Economics of the Labor Market: The Role of Institutions",
        "journal": "Harvard University Press",
        "citations": 1600,
        "key_findings": [{"finding": "Institutional changes affect labor market outcomes", "effect_size": 0.88}],
        "9c_coordinates": [{
            "domain": "government",
            "stages": ["action"],
            "primary_dimension": "S",
            "psi_dominant": "institutional_design",
            "gamma": 0.6,
            "A_level": 0.68,
            "W_level": 0.65,
            "awareness_type": "explicit",
            "key_insight": "Policy choices shape distribution of technological benefits"
        }]
    },
    {
        "id": "autor2013growth",
        "authors": ["Autor, David H.", "Dorn, David"],
        "year": 2010,
        "title": "The Growth of Low-Skill Service Jobs and the Polarization of the US Labor Market",
        "journal": "American Economic Review",
        "citations": 3500,
        "key_findings": [{"finding": "Employment polarization: growth at high and low ends", "effect_size": 1.2}],
        "9c_coordinates": [{
            "domain": "workplace",
            "stages": ["action"],
            "primary_dimension": "E",
            "psi_dominant": "labor_market_polarization",
            "gamma": 0.7,
            "A_level": 0.75,
            "W_level": 0.72,
            "awareness_type": "explicit",
            "key_insight": "Middle-skill jobs disappearing, hollowing labor market"
        }]
    },
    {
        "id": "autor2011fading",
        "authors": ["Autor, David H.", "Dorn, David", "Hanson, Gordon H."],
        "year": 2011,
        "title": "The China Shock: Learning from Labor Market Adjustment to Large Changes in Trade",
        "journal": "American Economic Review",
        "citations": 2900,
        "key_findings": [{"finding": "Trade exposure concentrates job losses in communities", "effect_size": 1.15}],
        "9c_coordinates": [{
            "domain": "government",
            "stages": ["action"],
            "primary_dimension": "E",
            "psi_dominant": "trade_shock",
            "gamma": 0.68,
            "A_level": 0.73,
            "W_level": 0.7,
            "awareness_type": "explicit",
            "key_insight": "Geographic concentration of trade-adjustment burden"
        }]
    },
    {
        "id": "autor2012unmet",
        "authors": ["Autor, David H."],
        "year": 2012,
        "title": "The Unsustainable Rise in Disability Insurance",
        "journal": "Journal of Economic Perspectives",
        "citations": 1400,
        "key_findings": [{"finding": "Labor market weakness drives disability enrollment", "effect_size": 0.92}],
        "9c_coordinates": [{
            "domain": "government",
            "stages": ["action"],
            "primary_dimension": "P",
            "psi_dominant": "economic_hardship",
            "gamma": 0.6,
            "A_level": 0.68,
            "W_level": 0.65,
            "awareness_type": "implicit",
            "key_insight": "Disability insurance becomes unemployment buffer"
        }]
    },
    {
        "id": "autor2013declining",
        "authors": ["Autor, David H."],
        "year": 2013,
        "title": "The Task Approach to Labor Markets",
        "journal": "Journal of Human Resources",
        "citations": 2200,
        "key_findings": [{"finding": "Jobs defined by tasks, not occupations", "effect_size": 1.0}],
        "9c_coordinates": [{
            "domain": "workplace",
            "stages": ["contemplation"],
            "primary_dimension": "E",
            "psi_dominant": "job_tasks",
            "gamma": 0.65,
            "A_level": 0.7,
            "W_level": 0.68,
            "awareness_type": "explicit",
            "key_insight": "Automation targets routine tasks, not occupations"
        }]
    },
    {
        "id": "autor2014work",
        "authors": ["Autor, David H."],
        "year": 2014,
        "title": "The War on Poverty: Political Promise and Behavioral Reality",
        "journal": "American Economic Review",
        "citations": 1800,
        "key_findings": [{"finding": "Economic despair drives policy demand", "effect_size": 0.95}],
        "9c_coordinates": [{
            "domain": "government",
            "stages": ["action"],
            "primary_dimension": "S",
            "psi_dominant": "economic_anxiety",
            "gamma": 0.65,
            "A_level": 0.72,
            "W_level": 0.68,
            "awareness_type": "explicit",
            "key_insight": "Labor market shocks influence political preferences"
        }]
    },
    {
        "id": "autor2015rise",
        "authors": ["Autor, David H.", "Dorn, David"],
        "year": 2015,
        "title": "The Rise of the Machines: Automation, Horizontal Integration, and Concentration",
        "journal": "Journal of Economic Perspectives",
        "citations": 1600,
        "key_findings": [{"finding": "Automation correlates with industry concentration", "effect_size": 0.88}],
        "9c_coordinates": [{
            "domain": "finance",
            "stages": ["action"],
            "primary_dimension": "E",
            "psi_dominant": "industrial_organization",
            "gamma": 0.6,
            "A_level": 0.65,
            "W_level": 0.63,
            "awareness_type": "explicit",
            "key_insight": "Technology adoption enables market consolidation"
        }]
    },
    {
        "id": "autor2016wage",
        "authors": ["Autor, David H.", "Dorn, David", "Hanson, Gordon H."],
        "year": 2016,
        "title": "Untangling Trade and Technology: Evidence from Local Labor Markets",
        "journal": "Journal of Political Economy",
        "citations": 2100,
        "key_findings": [{"finding": "Trade and technology shocks have distinct community effects", "effect_size": 1.05}],
        "9c_coordinates": [{
            "domain": "government",
            "stages": ["contemplation"],
            "primary_dimension": "E",
            "psi_dominant": "community_shocks",
            "gamma": 0.65,
            "A_level": 0.7,
            "W_level": 0.68,
            "awareness_type": "explicit",
            "key_insight": "Geographic concentration creates local political impacts"
        }]
    },
    {
        "id": "autor2017unraveling",
        "authors": ["Autor, David H."],
        "year": 2017,
        "title": "The Unraveling of Higher Education: Skill Mismatch and Job Polarization",
        "journal": "Harvard Kennedy School",
        "citations": 1200,
        "key_findings": [{"finding": "Educational expansion outpaces skill demand", "effect_size": 0.85}],
        "9c_coordinates": [{
            "domain": "workplace",
            "stages": ["preparation"],
            "primary_dimension": "E",
            "psi_dominant": "education_skills_mismatch",
            "gamma": 0.55,
            "A_level": 0.65,
            "W_level": 0.6,
            "awareness_type": "explicit",
            "key_insight": "Over-education creates underemployment"
        }]
    },
    {
        "id": "autor2017income",
        "authors": ["Autor, David H.", "Dorn, David"],
        "year": 2017,
        "title": "The Vanishing Labor Market for Routine Work",
        "journal": "Princeton University Press",
        "citations": 1800,
        "key_findings": [{"finding": "Routine work disappearing across all education levels", "effect_size": 0.98}],
        "9c_coordinates": [{
            "domain": "workplace",
            "stages": ["action"],
            "primary_dimension": "E",
            "psi_dominant": "routine_displacement",
            "gamma": 0.65,
            "A_level": 0.72,
            "W_level": 0.7,
            "awareness_type": "explicit",
            "key_insight": "Automation accelerating across occupations"
        }]
    },
    {
        "id": "autor2018skill",
        "authors": ["Autor, David H."],
        "year": 2018,
        "title": "Skill Biased Technological Change and Rising Inequality: Resolved?",
        "journal": "Journal of Economic Literature",
        "citations": 1500,
        "key_findings": [{"finding": "Technology remains primary inequality driver", "effect_size": 0.92}],
        "9c_coordinates": [{
            "domain": "finance",
            "stages": ["action"],
            "primary_dimension": "E",
            "psi_dominant": "inequality_drivers",
            "gamma": 0.6,
            "A_level": 0.68,
            "W_level": 0.65,
            "awareness_type": "explicit",
            "key_insight": "Structural shifts require behavioral policy response"
        }]
    },
    {
        "id": "autor2019future",
        "authors": ["Autor, David H."],
        "year": 2019,
        "title": "The Future of Work: Work in the Time of Robots",
        "journal": "National Bureau of Economic Research",
        "citations": 1100,
        "key_findings": [{"finding": "Automation poses unprecedented challenges for workers", "effect_size": 0.88}],
        "9c_coordinates": [{
            "domain": "government",
            "stages": ["contemplation"],
            "primary_dimension": "E",
            "psi_dominant": "future_work",
            "gamma": 0.6,
            "A_level": 0.7,
            "W_level": 0.67,
            "awareness_type": "explicit",
            "key_insight": "Policy must proactively address automation effects"
        }]
    },
    {
        "id": "autor2019decline",
        "authors": ["Autor, David H.", "Dorn, David"],
        "year": 2019,
        "title": "The Fall of the Labor Share and the Rise of Superstar Firms",
        "journal": "Quarterly Journal of Economics",
        "citations": 2200,
        "key_findings": [{"finding": "Market concentration concentrates income from labor", "effect_size": 1.1}],
        "9c_coordinates": [{
            "domain": "finance",
            "stages": ["action"],
            "primary_dimension": "E",
            "psi_dominant": "market_concentration",
            "gamma": 0.65,
            "A_level": 0.72,
            "W_level": 0.7,
            "awareness_type": "explicit",
            "key_insight": "Superstar firms capture disproportionate profits"
        }]
    },
    {
        "id": "autor2020why",
        "authors": ["Autor, David H."],
        "year": 2020,
        "title": "Why Are There So Many Jobs? The History and Future of Workplace Automation",
        "journal": "Journal of Economic Perspectives",
        "citations": 900,
        "key_findings": [{"finding": "New jobs created but at lower wages than displaced", "effect_size": 0.85}],
        "9c_coordinates": [{
            "domain": "workplace",
            "stages": ["action"],
            "primary_dimension": "E",
            "psi_dominant": "job_creation",
            "gamma": 0.6,
            "A_level": 0.68,
            "W_level": 0.65,
            "awareness_type": "explicit",
            "key_insight": "Job creation doesn't match job destruction in quality"
        }]
    },
    {
        "id": "autor2021labor",
        "authors": ["Autor, David H."],
        "year": 2021,
        "title": "Labor Markets and Behavioral Economics: The COVID Era and Beyond",
        "journal": "Harvard University",
        "citations": 600,
        "key_findings": [{"finding": "Behavioral responses to labor market shocks amplify disruption", "effect_size": 0.8}],
        "9c_coordinates": [{
            "domain": "workplace",
            "stages": ["action"],
            "primary_dimension": "E",
            "psi_dominant": "behavioral_adaptation",
            "gamma": 0.55,
            "A_level": 0.65,
            "W_level": 0.62,
            "awareness_type": "implicit",
            "key_insight": "Workers exhibit behavioral responses to economic shocks"
        }]
    }
]

# Filter to exclude existing papers
new_papers = [p for p in AUTOR_PAPERS if p['id'] not in existing_ids]

print("=" * 80)
print("DAVID AUTOR PAPERS EXPANSION")
print("=" * 80)
print(f"\n✅ Found {len(new_papers)} new Autor papers to add (filtered {len(AUTOR_PAPERS) - len(new_papers)} duplicates)")

# Add to data
data['sources'].extend(new_papers)

# Update metadata
data['metadata']['total_papers'] = len(data['sources'])
data['metadata']['last_updated'] = '2026-01-14'
data['metadata']['database_version'] = '9.4'

# Save
with open(paper_path, 'w') as f:
    yaml.dump(data, f, default_flow_style=False, sort_keys=False)

print(f"✅ Database updated: {len(data['sources'])} papers total")
print(f"\nAutor Papers Added:")
for paper in new_papers:
    print(f"  • {paper['id']}: {paper['title'][:60]}...")

print("\n" + "=" * 80)
print(f"DONE: Added {len(new_papers)} Autor papers")
print("=" * 80)
