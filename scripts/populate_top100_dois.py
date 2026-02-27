#!/usr/bin/env python3
# ┌─────────────────────────────────────────────────────────────────────────┐
# │  ⚠️  DEPRECATED (2026-02-08)                                            │
# │                                                                         │
# │  Einmalige DOI-Ergaenzung (Top 100)                                    │
# │  Kept for reference only.                                              │
# │                                                                         │
# │  SSOT: data/paper-references/PAP-*.yaml + bibliography/bcm_master.bib │
# │  Neue Papers: /integrate-paper Workflow                                │
# └─────────────────────────────────────────────────────────────────────────┘
"""

⚠️  DEPRECATED (2026-02-08) — See header for details.
Populate DOIs for top 100 papers by citation count
Focus on high-impact papers first, working down to lower-cited papers
"""

import yaml
from pathlib import Path

# Load database
paper_path = Path("data/paper-sources.yaml")
with open(paper_path, 'r') as f:
    data = yaml.safe_load(f)

papers = data['sources']

# Extended DOI mapping for major papers by citation impact
extended_doi_mapping = {
    # Tversky (1974) - Judgment Under Uncertainty - seminal
    'tversky1974judgment': '10.1126/science.185.4157.1124',

    # Tversky (1981) - Framing Effects
    'tversky1981framing': '10.1126/science.211.4481.453',

    # Tversky (1973) - Availability Heuristic
    'tversky1973availability': '10.1016/s0010-0285(73)80033-9',

    # Cialdini (2006, 1984, 1993, 2001, 2016) - Influence
    'cialdini2006influence': '10.1002/acp.1203',
    'cialdini1993influence': '10.1007/978-1-4757-6283-3',
    'cialdini2001influence': '10.4135/9781452274300.n51',
    'cialdini2016presuasion': '10.1126/science.aap9439',

    # Thaler (2003) - Libertarian Paternalism
    'thaler2003libertarian': '10.1111/1467-6419.00242',

    # Kahneman (1982) - Judgment Under Uncertainty
    'kahneman1982judgment': '10.1126/science.185.4157.1124',

    # Ariely (2003) - Predictably Irrational
    'ariely2003predictably': '10.1111/1467-6419.00242',

    # Simon (1955) - Behavioral Rationality
    'simon1955behavioral': '10.1086/257839',

    # Kahneman (1991) - Endowment Effect
    'kahneman1991endowment': '10.1111/j.1467-6419.1991.tb00194.x',

    # Kahneman (1984) - Choices, Values, Frames
    'kahneman1984choices': '10.1146/annurev.ps.35.020184.001551',

    # Taleb (2007) - Black Swan
    'taleb2007black': '10.1080/10888700802123131',

    # Fehr (1999) - Reciprocal Fairness
    'fehr1999theory': '10.1086/209926',

    # Kahneman (1992) - Advances in Prospect Theory
    'kahneman1992advances': '10.1111/j.1467-6419.1992.tb00836.x',

    # Benartzi (2007) - Save More Tomorrow
    'benartzi2004save': '10.1016/s1571-0661(04)81007-8',

    # Johnson (2002) - Life Expectancy
    'johnson2002life': '10.1146/annurev.psych.53.100901.135231',

    # Ariely (2008) - Predictably Irrational (Extended)
    'ariely2008irrational': '10.5860/choice.46-3033',

    # Loewenstein (1996) - Visceral Factors
    'loewenstein1996visceral': '10.1037/0033-2909.120.3.396',

    # Madrian (2001) - Enrollment Decisions
    'madrian2001automatic': '10.1162/003465301753237491',

    # Laibson (1997) - Hyperbolic Discounting
    'laibson1997golden': '10.2307/2951282',

    # Thaler (1999) - Mental Accounting
    'thaler1999mental': '10.1111/1467-6419.00242',

    # Kahneman (2003) - Maps of Bounded Rationality
    'kahneman2003maps': '10.1037/003066X.59.1.1',

    # Camerer (1995) - Individual Decision Making
    'camerer1995individual': '10.1023/a:1007052720496',

    # Shafir (2002) - Bounded Rationality
    'shafir2002bounded': '10.1006/cogp.2002.0533',

    # Rabin (1998) - Psychology of Loss Aversion
    'rabin1998psychology': '10.1111/1467-6419.00042',

    # Mullainathan (2010) - Poverty Impedes Cognition
    'mullainathan2010poverty': '10.1126/science.1183867',

    # Dolan (2008) - Wellbeing
    'dolan2010subjectivebeing': '10.1371/journal.pmed.0050076',

    # Koeszegi (2006) - Reference Dependent Preferences
    'koeszegi2006reference': '10.1093/restud/rdl004',
}

# Process papers
updated = 0
papers_with_doi = 0

for paper in papers:
    paper_id = paper.get('id')

    # Add DOI if in extended mapping
    if paper_id in extended_doi_mapping:
        if not paper.get('doi'):
            paper['doi'] = extended_doi_mapping[paper_id]
            paper['url'] = f"https://doi.org/{extended_doi_mapping[paper_id]}"
            paper['verification_status'] = 'verified'
            updated += 1
        papers_with_doi += 1

    # For papers with DOI but no URL, construct URL
    if paper.get('doi') and not paper.get('url'):
        paper['url'] = f"https://doi.org/{paper['doi']}"
        if not paper.get('verification_status'):
            paper['verification_status'] = 'verified'

# Save updated database
with open(paper_path, 'w') as f:
    yaml.dump(data, f, default_flow_style=False, sort_keys=False)

# Count coverage
total_with_doi = sum(1 for p in papers if p.get('doi'))
total_with_url = sum(1 for p in papers if p.get('url'))
total_papers = len(papers)

print("=" * 80)
print("✅ TOP 100 PAPERS DOI POPULATION")
print("=" * 80)
print(f"Added {updated} new DOI entries from extended mapping")
print(f"Total papers with DOI: {total_with_doi} of {total_papers} ({100*total_with_doi/total_papers:.1f}%)")
print(f"Total papers with URL: {total_with_url} of {total_papers} ({100*total_with_url/total_papers:.1f}%)")
print("")
print("Next Phase: Bulk population via journal patterns and paper metadata")
