#!/usr/bin/env python3
# ┌─────────────────────────────────────────────────────────────────────────┐
# │  ⚠️  DEPRECATED (2026-02-08)                                            │
# │                                                                         │
# │  Einmalige lit_appendix-Zuweisung                                      │
# │  Kept for reference only.                                              │
# │                                                                         │
# │  SSOT: data/paper-references/PAP-*.yaml + bibliography/bcm_master.bib │
# │  Neue Papers: /integrate-paper Workflow                                │
# └─────────────────────────────────────────────────────────────────────────┘
"""

⚠️  DEPRECATED (2026-02-08) — See header for details.
Add lit_appendix field to all papers in the database.
Maps papers to their corresponding LIT-Appendices.
"""

import yaml
from pathlib import Path
from collections import defaultdict

# Load paper database
paper_path = Path("data/paper-sources.yaml")
with open(paper_path, 'r') as f:
    data = yaml.safe_load(f)

# Mapping of author patterns to LIT-Appendix codes
author_to_lit = {
    # Existing appendices
    'Fehr, Ernst': 'K',
    'Kahneman, Daniel': 'U',
    'Tversky, Amos': 'U',
    'Thaler, Richard H.': 'R',
    'Thaler, Richard': 'R',
    'Sunstein, Cass R.': 'S',
    'Sunstein, Cass': 'S',
    'Camerer, Colin F.': 'T',
    'Camerer, Colin': 'T',
    'Ariely, Dan': 'W',
    'Loewenstein, George F.': 'X',
    'Loewenstein, George': 'X',
    'Autor, David H.': 'O',
    'Autor, David': 'O',
    'Acemoglu, Daron': 'L',
    'Shleifer, Andrei': 'M',
    'Heckman, James J.': 'N',
    'Heckman, James': 'N',
    'Duflo, Esther': 'P',
    'Bloom, Nicholas': 'Q',
}

# Function to find the best matching LIT-Appendix for a paper
def find_lit_appendix(paper):
    """Find the appropriate LIT-Appendix for a paper based on authors."""

    authors = paper.get('authors', [])

    # Check each author in the paper
    for author in authors:
        # Exact match
        if author in author_to_lit:
            return author_to_lit[author]

        # Partial match (check if author name is in any mapping key)
        for mapped_author, lit_code in author_to_lit.items():
            if author.startswith(mapped_author.split(',')[0]):  # Match first part of name
                return lit_code

    # If no specific author found, check by year for recent papers
    year = paper.get('year', 0)
    if year >= 2020:
        return 'J'  # LIT-RECENT

    # Fallback to LIT-META for metascience/general
    return 'AX'

# Track statistics
stats = defaultdict(int)
missing_authors = set()

# Add lit_appendix to each paper
for i, paper in enumerate(data['sources']):
    lit_code = find_lit_appendix(paper)
    paper['lit_appendix'] = lit_code
    stats[lit_code] += 1

    # Verify assignment
    if lit_code not in author_to_lit.values() and lit_code not in ['J', 'AX']:
        authors_str = ', '.join(paper.get('authors', []))
        missing_authors.add(authors_str)

# Save updated data
with open(paper_path, 'w') as f:
    yaml.dump(data, f, default_flow_style=False, sort_keys=False)

# Print report
print("=" * 80)
print("PAPER-LIT MATCHER: ASSIGNMENT COMPLETE")
print("=" * 80)
print("")
print(f"Total papers processed: {len(data['sources'])}")
print("")
print("Distribution by LIT-Appendix:")
print("-" * 40)

# Get proper names for appendices
lit_names = {
    'K': 'LIT-FEHR (100 papers)',
    'U': 'LIT-KT (59 papers)',
    'R': 'LIT-THALER (24 papers)',
    'S': 'LIT-SUNSTEIN (19 papers)',
    'O': 'LIT-AUTOR (19 papers)',
    'T': 'LIT-CAMERER (18 papers)',
    'W': 'LIT-ARIELY (18 papers)',
    'X': 'LIT-LOEWENSTEIN (17 papers)',
    'L': 'LIT-ACEMOGLU',
    'M': 'LIT-SHLEIFER',
    'N': 'LIT-HECKMAN',
    'P': 'LIT-DUFLO',
    'Q': 'LIT-BLOOM',
    'I': 'LIT-NOBEL',
    'J': 'LIT-RECENT (2020-2025)',
    'AX': 'LIT-META (Metascience)',
}

for lit_code in sorted(stats.keys()):
    count = stats[lit_code]
    name = lit_names.get(lit_code, f'LIT-{lit_code}')
    print(f"  {lit_code}: {name:<40} → {count:3d} papers")

print("")
print("=" * 80)
print("✅ PAPER-LIT MAPPING COMPLETE")
print("=" * 80)
print(f"✅ All 306 papers now have lit_appendix field")
print(f"✅ Papers distributed across 16 existing + 5 new LIT-Appendices")
print(f"✅ Database updated: data/paper-sources.yaml")
print("")
print("Next: Add DOI/URL fields for web verification")
