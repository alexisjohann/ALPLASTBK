#!/usr/bin/env python3
"""
⚠️ DEPRECATED (2026-02-08): paper-sources.yaml is no longer SSOT.
SSOT is now: data/paper-references/PAP-*.yaml + bibliography/bcm_master.bib
Use scripts/check_paper_consistency.py for consistency checks.

Synchronize paper-sources.yaml and framework_paper_mapping.csv databases.

This script:
1. Identifies papers missing from each database
2. Generates entries for missing papers
3. Maintains consistency between both formats
"""

import csv
import yaml
import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent
YAML_PATH = BASE_DIR / "data" / "paper-sources.yaml"
CSV_PATH = BASE_DIR / "bibliography" / "framework_paper_mapping.csv"

def load_yaml_papers():
    """Load papers from paper-sources.yaml"""
    with open(YAML_PATH, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    papers = {}
    for source in data.get('sources', []):
        paper_id = source.get('id')
        if paper_id:
            papers[paper_id] = source
    return papers, data

def load_csv_papers():
    """Load papers from framework_paper_mapping.csv"""
    papers = {}
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            paper_id = row.get('Paper_ID')
            if paper_id:
                papers[paper_id] = row
    return papers

def csv_to_yaml_entry(csv_row):
    """Convert CSV row to YAML entry format"""
    # Parse author string
    authors = [a.strip() for a in csv_row.get('Author', '').split(';')]

    # Determine evidence tier based on relevance
    relevance = csv_row.get('Relevance', 'Supporting')
    if relevance == 'Core':
        tier = 2
    elif relevance == 'Supporting':
        tier = 3
    elif relevance == 'Methodological':
        tier = 5
    else:
        tier = 4

    # Map Framework_Element to use_for
    framework_elements = csv_row.get('Framework_Element', '').split(',')
    use_for = [e.strip() for e in framework_elements if e.strip()]

    # Map Psi_Dimension
    psi_dim = csv_row.get('Psi_Dimension', '')

    entry = {
        'id': csv_row.get('Paper_ID'),
        'authors': authors,
        'year': int(csv_row.get('Year', 0)) if csv_row.get('Year', '').isdigit() else None,
        'title': csv_row.get('Title', ''),
        'journal': None,  # CSV doesn't have this
        'volume': None,
        'issue': None,
        'doi': None,
        'citations': int(csv_row.get('Citations_Approx', 0)) if csv_row.get('Citations_Approx', '').isdigit() else 0,
        'status': 'published',
        'type': 'journal_article',
        'relevance': 'high' if relevance == 'Core' else 'medium',
        'evidence_tier': tier,
        'use_for': use_for if use_for else ['general'],
        'key_findings': [
            {
                'finding': csv_row.get('Specific_Contribution', 'See paper for details'),
                'domain': 'economics' if not psi_dim else psi_dim.lower().replace('psi_', ''),
                'stage': None,
                'primary_dimension': None,
                'effect_size': None
            }
        ],
        '9c_coordinates': [
            {
                'domain': 'economics',
                'stages': None,
                'primary_dimension': None,
                'psi_dominant': psi_dim if psi_dim else None,
                'gamma': None,
                'A_level': None,
                'W_level': None,
                'awareness_type': None,
                'key_insight': csv_row.get('Equation_Concept', csv_row.get('Specific_Contribution', ''))
            }
        ],
        'lit_appendix': csv_row.get('Appendix', 'general'),
        'url': None,
        'verification_status': 'pending',
        'linked_cases': []
    }
    return entry

def yaml_to_csv_row(yaml_entry):
    """Convert YAML entry to CSV row format"""
    # Join authors
    authors = '; '.join(yaml_entry.get('authors', []))

    # Get framework elements from use_for
    use_for = yaml_entry.get('use_for', [])
    framework_elements = ','.join(use_for) if use_for else ''

    # Get Psi dimension from 9c_coordinates
    coords = yaml_entry.get('9c_coordinates', [])
    if isinstance(coords, list) and len(coords) > 0 and isinstance(coords[0], dict):
        psi_dim = coords[0].get('psi_dominant', '')
        key_insight = coords[0].get('key_insight', '')
    else:
        psi_dim = ''
        key_insight = ''

    # Get specific contribution from key_findings
    findings = yaml_entry.get('key_findings', [])
    if isinstance(findings, list) and len(findings) > 0:
        if isinstance(findings[0], dict):
            specific = findings[0].get('finding', '')
        else:
            specific = str(findings[0])
    else:
        specific = str(findings) if findings else ''

    # Determine relevance
    tier = yaml_entry.get('evidence_tier', 3)
    if tier <= 2:
        relevance = 'Core'
    elif tier == 5:
        relevance = 'Methodological'
    else:
        relevance = 'Supporting'

    row = {
        'Paper_ID': yaml_entry.get('id', ''),
        'Author': authors,
        'Year': str(yaml_entry.get('year', '')),
        'Title': yaml_entry.get('title', ''),
        'Appendix': yaml_entry.get('lit_appendix', ''),
        'Framework_Element': framework_elements,
        'Psi_Dimension': psi_dim if psi_dim else '',
        'Specific_Contribution': specific,
        'Equation_Concept': key_insight,
        'Relevance': relevance,
        'Citations_Approx': str(yaml_entry.get('citations', 0))
    }
    return row

def sync_databases():
    """Main sync function"""
    print("Loading databases...")
    yaml_papers, yaml_data = load_yaml_papers()
    csv_papers = load_csv_papers()

    yaml_ids = set(yaml_papers.keys())
    csv_ids = set(csv_papers.keys())

    yaml_only = yaml_ids - csv_ids
    csv_only = csv_ids - yaml_ids
    both = yaml_ids & csv_ids

    print(f"\nCurrent state:")
    print(f"  YAML papers: {len(yaml_ids)}")
    print(f"  CSV papers: {len(csv_ids)}")
    print(f"  In both: {len(both)}")
    print(f"  YAML only: {len(yaml_only)}")
    print(f"  CSV only: {len(csv_only)}")

    # Generate new YAML entries from CSV-only papers
    print(f"\nGenerating {len(csv_only)} new YAML entries from CSV...")
    new_yaml_entries = []
    for paper_id in sorted(csv_only):
        csv_row = csv_papers[paper_id]
        yaml_entry = csv_to_yaml_entry(csv_row)
        new_yaml_entries.append(yaml_entry)

    # Generate new CSV rows from YAML-only papers
    print(f"Generating {len(yaml_only)} new CSV rows from YAML...")
    new_csv_rows = []
    for paper_id in sorted(yaml_only):
        yaml_entry = yaml_papers[paper_id]
        csv_row = yaml_to_csv_row(yaml_entry)
        new_csv_rows.append(csv_row)

    return new_yaml_entries, new_csv_rows, yaml_data, csv_papers

def write_synced_yaml(yaml_data, new_entries, output_path=None):
    """Write updated YAML with new entries"""
    if output_path is None:
        output_path = YAML_PATH

    # Add new entries to sources
    yaml_data['sources'].extend(new_entries)

    # Update metadata
    total = len(yaml_data['sources'])
    yaml_data['metadata']['total_papers'] = total
    yaml_data['metadata']['sync_status'] = 'SYNCED'
    yaml_data['metadata']['last_updated'] = '2026-01-17'
    yaml_data['metadata']['version'] = '10.0'
    yaml_data['metadata']['database_version'] = '11.0'

    with open(output_path, 'w', encoding='utf-8') as f:
        yaml.dump(yaml_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    print(f"Wrote {total} papers to {output_path}")

def write_synced_csv(existing_papers, new_rows, output_path=None):
    """Write updated CSV with new rows"""
    if output_path is None:
        output_path = CSV_PATH

    # Combine existing and new
    all_rows = list(existing_papers.values()) + new_rows

    fieldnames = ['Paper_ID', 'Author', 'Year', 'Title', 'Appendix',
                  'Framework_Element', 'Psi_Dimension', 'Specific_Contribution',
                  'Equation_Concept', 'Relevance', 'Citations_Approx']

    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for row in sorted(all_rows, key=lambda x: x.get('Paper_ID', '')):
            writer.writerow(row)

    print(f"Wrote {len(all_rows)} papers to {output_path}")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Sync paper databases')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without writing')
    parser.add_argument('--yaml-only', action='store_true', help='Only update YAML')
    parser.add_argument('--csv-only', action='store_true', help='Only update CSV')
    args = parser.parse_args()

    new_yaml, new_csv, yaml_data, csv_papers = sync_databases()

    if args.dry_run:
        print(f"\nDry run - would add:")
        print(f"  {len(new_yaml)} entries to YAML")
        print(f"  {len(new_csv)} rows to CSV")
        print("\nSample new YAML entries:")
        for entry in new_yaml[:3]:
            print(f"  - {entry['id']}: {entry['title'][:50]}...")
        print("\nSample new CSV rows:")
        for row in new_csv[:3]:
            print(f"  - {row['Paper_ID']}: {row['Title'][:50]}...")
    else:
        if not args.csv_only:
            write_synced_yaml(yaml_data, new_yaml)
        if not args.yaml_only:
            write_synced_csv(csv_papers, new_csv)
        print("\nSync complete!")
