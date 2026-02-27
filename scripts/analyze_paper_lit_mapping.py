#!/usr/bin/env python3
# ┌─────────────────────────────────────────────────────────────────────────┐
# │  ⚠️  DEPRECATED (2026-02-08)                                            │
# │                                                                         │
# │  Einmalige Analyse Paper-LIT-Zuordnung                                 │
# │  Kept for reference only.                                              │
# │                                                                         │
# │  SSOT: data/paper-references/PAP-*.yaml + bibliography/bcm_master.bib │
# │  Neue Papers: /integrate-paper Workflow                                │
# └─────────────────────────────────────────────────────────────────────────┘
# =============================================================================
# PAPER-TO-LIT APPENDIX ANALYSIS
# =============================================================================
# Analyzes all 306 papers and maps them to LIT-Appendices
# Step 1: Understand current state, identify gaps, plan new appendices

import yaml
from pathlib import Path
from collections import defaultdict
import re

# Load papers
paper_path = Path("data/paper-sources.yaml")
with open(paper_path, 'r') as f:
    papers = yaml.safe_load(f)['sources']

print("=" * 80)
print("PHASE 1: PAPER-TO-LIT APPENDIX ANALYSIS")
print("=" * 80)

# Step 1: Extract all unique authors
author_counts = defaultdict(int)
author_papers = defaultdict(list)

for paper in papers:
    for author in paper.get('authors', []):
        # Extract last name
        last_name = author.split(',')[0] if ',' in author else author.split()[-1]
        author_counts[author] += 1
        author_papers[author].append({
            'id': paper['id'],
            'title': paper['title'][:60],
            'year': paper['year']
        })

# Step 2: Define existing LIT-Appendices
existing_lit = {
    'I': 'LIT-NOBEL',
    'J': 'LIT-RECENT',
    'K': 'LIT-FEHR',
    'L': 'LIT-ACEMOGLU',
    'M': 'LIT-SHLEIFER',
    'N': 'LIT-HECKMAN',
    'O': 'LIT-AUTOR',
    'P': 'LIT-DUFLO',
    'Q': 'LIT-BLOOM',
    'U': 'LIT-KT',
    'AX': 'LIT-META',
    'AY': 'LIT-PARADIGMS',
    'XV': 'LIT-HISTORY',
    'XVI': 'LIT-CRITIQUE',
    'XVII': 'LIT-THERMODYNAMICS',
    'XVIII': 'LIT-FEHR-METHOD'
}

# Step 3: Create author → LIT mapping
author_to_lit = {
    'Fehr, Ernst': ('K', 'LIT-FEHR'),
    'Kahneman, Daniel': ('U', 'LIT-KT'),
    'Tversky, Amos': ('U', 'LIT-KT'),
    'Autor, David H.': ('O', 'LIT-AUTOR'),
    'Acemoglu, Daron': ('L', 'LIT-ACEMOGLU'),
    'Shleifer, Andrei': ('M', 'LIT-SHLEIFER'),
    'Heckman, James J.': ('N', 'LIT-HECKMAN'),
    'Duflo, Esther': ('P', 'LIT-DUFLO'),
    'Bloom, Nick': ('Q', 'LIT-BLOOM'),
}

# NEW - to be created
new_lit_to_create = {
    'Thaler, Richard H.': ('R', 'LIT-THALER', 'Richard Thaler Research'),
    'Sunstein, Cass R.': ('S', 'LIT-SUNSTEIN', 'Cass Sunstein Research'),
    'Camerer, Colin F.': ('T', 'LIT-CAMERER', 'Colin Camerer Research'),
    'Ariely, Dan': ('W', 'LIT-ARIELY', 'Dan Ariely Research'),
    'Loewenstein, George F.': ('X', 'LIT-LOEWENSTEIN', 'George Loewenstein Research'),
}

# Step 4: Classify papers
classified_papers = {
    'has_lit': [],
    'needs_new_lit': [],
    'fallback_recent': [],
    'fallback_meta': [],
}

for paper in papers:
    matched = False
    paper_authors = paper.get('authors', [])
    primary_author = paper_authors[0] if paper_authors else None

    # Check if matches existing or new LIT
    for author in paper_authors:
        if author in author_to_lit:
            code, lit_name = author_to_lit[author]
            classified_papers['has_lit'].append({
                'paper_id': paper['id'],
                'author': author,
                'lit_code': code,
                'lit_name': lit_name,
                'year': paper['year']
            })
            matched = True
            break
        elif author in new_lit_to_create:
            code, lit_name, title = new_lit_to_create[author]
            classified_papers['needs_new_lit'].append({
                'paper_id': paper['id'],
                'author': author,
                'lit_code': code,
                'lit_name': lit_name,
                'lit_title': title,
                'year': paper['year']
            })
            matched = True
            break

    # Fallback logic
    if not matched:
        year = paper.get('year', 0)
        if year >= 2020:
            classified_papers['fallback_recent'].append({
                'paper_id': paper['id'],
                'author': primary_author or 'Unknown',
                'reason': 'Recent (>=2020)',
                'year': year
            })
        else:
            classified_papers['fallback_meta'].append({
                'paper_id': paper['id'],
                'author': primary_author or 'Unknown',
                'reason': 'Other',
                'year': year
            })

# Print Analysis Report
print(f"\n📊 TOTAL PAPERS: {len(papers)}")
print(f"   ✓ Has existing LIT: {len(classified_papers['has_lit'])}")
print(f"   ✓ Needs new LIT: {len(classified_papers['needs_new_lit'])}")
print(f"   ⚠ Fallback (Recent): {len(classified_papers['fallback_recent'])}")
print(f"   ⚠ Fallback (Meta): {len(classified_papers['fallback_meta'])}")

print("\n" + "=" * 80)
print("📚 EXISTING LIT-APPENDICES (16 total)")
print("=" * 80)
for code in ['I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'U', 'AX', 'AY', 'XV', 'XVI', 'XVII', 'XVIII']:
    if code in existing_lit:
        count = len([p for p in classified_papers['has_lit'] if p['lit_code'] == code])
        print(f"\n{code:4s} → {existing_lit[code]:20s} ({count} papers)")
        for p in sorted([p for p in classified_papers['has_lit'] if p['lit_code'] == code], key=lambda x: x['author'])[:3]:
            print(f"       • {p['paper_id']:20s} ({p['author']})")
        if count > 3:
            print(f"       ... +{count-3} more papers")

print("\n" + "=" * 80)
print("🆕 NEW LIT-APPENDICES TO CREATE (5 total)")
print("=" * 80)
new_authors = {}
for p in classified_papers['needs_new_lit']:
    author = p['author']
    if author not in new_authors:
        new_authors[author] = []
    new_authors[author].append(p)

for author, papers_list in sorted(new_authors.items()):
    code, lit_name, title = new_lit_to_create[author]
    print(f"\n{code:4s} → {lit_name:20s} ({len(papers_list)} papers)")
    print(f"       Title: {title}")
    for p in sorted(papers_list, key=lambda x: x['year'], reverse=True)[:3]:
        print(f"       • {p['paper_id']:20s} ({p['year']})")
    if len(papers_list) > 3:
        print(f"       ... +{len(papers_list)-3} more papers")

print("\n" + "=" * 80)
print("⚠️  FALLBACK PAPERS")
print("=" * 80)
print(f"\nFallback to LIT-RECENT (J): {len(classified_papers['fallback_recent'])}")
for p in classified_papers['fallback_recent'][:5]:
    print(f"  • {p['paper_id']:20s} ({p['author']}, {p['year']})")
if len(classified_papers['fallback_recent']) > 5:
    print(f"  ... +{len(classified_papers['fallback_recent'])-5} more")

print(f"\nFallback to LIT-META (AX): {len(classified_papers['fallback_meta'])}")
for p in classified_papers['fallback_meta'][:5]:
    print(f"  • {p['paper_id']:20s} ({p['author']}, {p['year']})")
if len(classified_papers['fallback_meta']) > 5:
    print(f"  ... +{len(classified_papers['fallback_meta'])-5} more")

# Save mapping report
mapping_report = {
    'analysis_date': '2026-01-14',
    'total_papers': len(papers),
    'existing_lit_appendices': existing_lit,
    'new_lit_appendices_to_create': {
        author: {
            'code': code,
            'name': name,
            'title': title,
            'paper_count': len([p for p in classified_papers['needs_new_lit'] if p['author'] == author])
        }
        for author, (code, name, title) in new_lit_to_create.items()
    },
    'classification': {
        'has_existing_lit': len(classified_papers['has_lit']),
        'needs_new_lit': len(classified_papers['needs_new_lit']),
        'fallback_recent': len(classified_papers['fallback_recent']),
        'fallback_meta': len(classified_papers['fallback_meta']),
    },
    'detailed_new_lit': {
        author: [
            {'paper_id': p['paper_id'], 'year': p['year']}
            for p in classified_papers['needs_new_lit']
            if p['author'] == author
        ]
        for author in new_authors.keys()
    }
}

with open('outputs/paper_lit_mapping_report.yaml', 'w') as f:
    yaml.dump(mapping_report, f, default_flow_style=False, sort_keys=False)

print("\n" + "=" * 80)
print("✅ MAPPING REPORT SAVED: outputs/paper_lit_mapping_report.yaml")
print("=" * 80)

print("\n📋 SUMMARY FOR NEXT PHASE:")
print("   1. Create 5 new LIT-Appendices (R, S, T, W, X)")
print("   2. Use codes: R=Thaler, S=Sunstein, T=Camerer, W=Ariely, X=Loewenstein")
print("   3. Register in appendix_index.tex (4 locations)")
print("   4. Run paper_lit_matcher.py to link all papers")
print("=" * 80)
