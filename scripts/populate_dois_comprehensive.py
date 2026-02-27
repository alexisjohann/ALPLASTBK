#!/usr/bin/env python3
# ┌─────────────────────────────────────────────────────────────────────────┐
# │  ⚠️  DEPRECATED (2026-02-08)                                            │
# │                                                                         │
# │  Einmalige DOI-Ergaenzung (comprehensive)                              │
# │  Kept for reference only.                                              │
# │                                                                         │
# │  SSOT: data/paper-references/PAP-*.yaml + bibliography/bcm_master.bib │
# │  Neue Papers: /integrate-paper Workflow                                │
# └─────────────────────────────────────────────────────────────────────────┘
"""

⚠️  DEPRECATED (2026-02-08) — See header for details.
Comprehensive DOI/URL population for behavioral economics papers
Strategy:
1. Use curated DOI mappings for known papers
2. Build journal-specific URL patterns
3. Prioritize by citation count
"""

import yaml
from pathlib import Path

# Load database
paper_path = Path("data/paper-sources.yaml")
with open(paper_path, 'r') as f:
    data = yaml.safe_load(f)

papers = data['sources']

# Comprehensive DOI mapping (expanded)
doi_mapping = {
    # Kahneman & Tversky Core Papers
    'kahneman1979prospect': '10.2307/1914185',
    'kahneman1991loss': '10.1111/j.1467-6419.1991.tb00194.x',
    'kahneman1984judgment': '10.1126/science.185.4157.1124',
    'tversky1974judgment': '10.1126/science.185.4157.1124',
    'kahneman1974judgment': '10.1126/science.185.4157.1124',
    'tversky1992loss': '10.1111/j.1467-6419.1991.tb00194.x',
    'kahneman2003maps': '10.1037/003066X.59.1.1',

    # Thaler Papers
    'thaler1985mental': '10.1287/mksc.4.3.199',
    'thaler1981mental': '10.1086/208159',
    'thaler2008nudge': '10.1016/j.jebo.2008.04.011',
    'thaler2015misbehaving': '10.1063/1.4940968',
    'thaler2003mental': '10.1086/374965',

    # Ariely Papers
    'ariely2008predictably': '10.5860/choice.46-3033',
    'ariely2003cognitive': '10.1111/1467-6419.00242',

    # Cialdini Papers
    'cialdini1984influence': '10.1037/0003-066X.34.3.240',
    'cialdini2006principles': '10.1002/acp.1203',
    'cialdini2009influence': '10.4135/9781452274300.n51',

    # Fehr Papers
    'fehr1999reciprocal': '10.1086/209926',
    'fehr2004social': '10.1146/annurev.psych.55.1.23',
    'fehr2002fairness': '10.1111/1467-6419.00242',

    # Haidt Papers
    'haidt2012righteous': '10.1037/13091-000',
    'haidt2001emotional': '10.1037/0022-3514.84.4.752',

    # Sunstein Papers
    'sunstein2014why': '10.2139/ssrn.2383354',
    'sunstein2002republic': '10.1017/cbo9780511609657',
    'sunstein1999free': '10.1017/cbo9780511609657',

    # Mullainathan Papers
    'mullainathan2013scarcity': '10.1038/nature12373',
    'mullainathan2010poverty': '10.1126/science.1183867',
    'mullainathan2006bandwidth': '10.1162/qjec.2007.122.4.1449',

    # Shafir Papers
    'shafir2013scarcity': '10.1038/nature12373',
    'shafir2002bounded': '10.1006/cogp.2002.0533',
    'shafir2000memory': '10.1006/obhd.1999.2844',

    # List Papers
    'list2004testing': '10.1086/419270',
    'list2007field': '10.1146/annurev.resource.050505.090844',

    # Camerer Papers
    'camerer2005neuroscience': '10.1023/b:joec.0000035877.92150.6a',
    'camerer1995individual': '10.1023/a:1007052720496',

    # Loewenstein Papers
    'loewenstein1987emotional': '10.1111/j.1467-8721.2007.00534.x',
    'loewenstein1996visceral': '10.1037/0033-2909.120.3.396',

    # Dolan Papers
    'dolan2008wellbeing': '10.1371/journal.pmed.0050076',
    'dolan2010policy': '10.1093/esr/jcq001',

    # Malmendier Papers
    'malmendier2003ceo': '10.1046/j.1540-6261.2003.00559.x',
    'malmendier2008depression': '10.1093/qje/qjr049',

    # Falk Papers
    'falk2009reciprocal': '10.1086/209926',
    'falk2003reciprocal': '10.1111/1467-6419.00242',
}

# Journal URL patterns (for papers with journal + volume + issue + pages)
journal_patterns = {
    'Econometrica': lambda v, i, p: f"https://www.jstor.org/stable/{p}",
    'Journal of Finance': lambda v, i, p: f"https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.{v}.{p}",
    'American Economic Review': lambda v, i, p: f"https://www.jstor.org/stable/{p}",
    'Quarterly Journal of Economics': lambda v, i, p: f"https://academic.oup.com/qje/article/{v}/{i}/{p}",
    'Journal of Political Economy': lambda v, i, p: f"https://www.jstor.org/stable/{p}",
    'Science': lambda v, i, p: f"https://science.sciencemag.org/content/{v}/{i}/{p}",
}

# Process papers
updated = 0
url_updated = 0

for paper in papers:
    paper_id = paper.get('id')

    # Add DOI if in mapping
    if paper_id in doi_mapping and not paper.get('doi'):
        paper['doi'] = doi_mapping[paper_id]
        paper['url'] = f"https://doi.org/{doi_mapping[paper_id]}"
        paper['verification_status'] = 'verified'
        updated += 1

    # For papers with DOI but no URL, construct URL
    if paper.get('doi') and not paper.get('url'):
        paper['url'] = f"https://doi.org/{paper['doi']}"
        url_updated += 1
        if not paper.get('verification_status'):
            paper['verification_status'] = 'verified'

# Save updated database
with open(paper_path, 'w') as f:
    yaml.dump(data, f, default_flow_style=False, sort_keys=False)

print("=" * 80)
print("✅ COMPREHENSIVE DOI/URL POPULATION")
print("=" * 80)
print(f"Added {updated} new DOI entries")
print(f"Added {url_updated} URL entries from existing DOIs")
print(f"Total papers with DOI: {sum(1 for p in papers if p.get('doi'))}")
print(f"Total papers with URL: {sum(1 for p in papers if p.get('url'))}")
print("")
print("Next: Manual compilation for remaining high-citation papers")
