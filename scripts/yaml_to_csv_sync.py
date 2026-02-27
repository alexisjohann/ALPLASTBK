#!/usr/bin/env python3
"""
⚠️ DEPRECATED (2026-02-08): paper-sources.yaml is no longer SSOT.
SSOT is now: data/paper-references/PAP-*.yaml + bibliography/bcm_master.bib

YAML → CSV Sync: Generate CSV from YAML master database.

WICHTIG: paper-sources.yaml ist NICHT MEHR die MASTER-Datenbank.
         Siehe data/paper-references/ für aktuelle Paper-Daten.
"""

import yaml
import csv
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
YAML_PATH = BASE_DIR / "data" / "paper-sources.yaml"
CSV_PATH = BASE_DIR / "bibliography" / "framework_paper_mapping.csv"

def yaml_to_csv_row(paper):
    """Convert YAML paper entry to CSV row."""
    # Authors
    authors = paper.get('authors', [])
    if isinstance(authors, list):
        author_str = '; '.join(str(a) for a in authors)
    else:
        author_str = str(authors)

    # 9c_coordinates → Psi_Dimension, key_insight
    coords = paper.get('9c_coordinates', [])
    if isinstance(coords, list) and coords and isinstance(coords[0], dict):
        psi_dim = coords[0].get('psi_dominant', '') or ''
        key_insight = coords[0].get('key_insight', '') or ''
    else:
        psi_dim = ''
        key_insight = ''

    # key_findings → Specific_Contribution
    findings = paper.get('key_findings', [])
    if isinstance(findings, list) and findings:
        if isinstance(findings[0], dict):
            specific = findings[0].get('finding', '') or ''
        else:
            specific = str(findings[0])
    else:
        specific = ''

    # use_for → Framework_Element
    use_for = paper.get('use_for', [])
    if isinstance(use_for, list):
        framework_elem = ','.join(str(u) for u in use_for)
    else:
        framework_elem = str(use_for) if use_for else ''

    # evidence_tier → Relevance mapping
    tier = paper.get('evidence_tier', 3)
    if tier and tier <= 2:
        relevance = 'Core'
    elif tier == 5:
        relevance = 'Methodological'
    elif tier == 4:
        relevance = 'Anecdotal'
    else:
        relevance = 'Supporting'

    return {
        'Paper_ID': paper.get('id', ''),
        'Author': author_str,
        'Year': str(paper.get('year', '')),
        'Title': paper.get('title', ''),
        'Appendix': paper.get('lit_appendix', ''),
        'Framework_Element': framework_elem,
        'Psi_Dimension': psi_dim,
        'Specific_Contribution': specific,
        'Equation_Concept': key_insight,
        'Relevance': relevance,
        'Citations_Approx': str(paper.get('citations', 0)),
        'Evidence_Tier': str(tier) if tier else '',
    }


def sync_yaml_to_csv():
    """Regenerate CSV from YAML master."""
    print(f"Loading YAML master: {YAML_PATH}")
    with open(YAML_PATH, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    sources = data.get('sources', [])
    print(f"Found {len(sources)} papers in YAML")

    # Convert all papers
    rows = []
    for paper in sources:
        row = yaml_to_csv_row(paper)
        rows.append(row)

    # Sort by Paper_ID
    rows.sort(key=lambda x: x.get('Paper_ID', ''))

    # Write CSV
    fieldnames = [
        'Paper_ID', 'Author', 'Year', 'Title', 'Appendix',
        'Framework_Element', 'Psi_Dimension', 'Specific_Contribution',
        'Equation_Concept', 'Relevance', 'Citations_Approx', 'Evidence_Tier'
    ]

    print(f"Writing CSV: {CSV_PATH}")
    with open(CSV_PATH, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✓ Synced {len(rows)} papers to CSV")

    # Verify
    tier_counts = {}
    for row in rows:
        t = row.get('Evidence_Tier', '')
        tier_counts[t] = tier_counts.get(t, 0) + 1

    print(f"\nTier distribution:")
    for t in sorted(tier_counts.keys()):
        print(f"  Tier {t}: {tier_counts[t]}")


if __name__ == '__main__':
    sync_yaml_to_csv()
