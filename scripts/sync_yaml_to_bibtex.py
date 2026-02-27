#!/usr/bin/env python3
"""
⚠️ DEPRECATED (2026-02-08): paper-sources.yaml is no longer SSOT.
SSOT is now: data/paper-references/PAP-*.yaml + bibliography/bcm_master.bib
Use scripts/check_paper_consistency.py for consistency checks.

Synchronize paper-sources.yaml to bcm_master.bib

Generates BibTeX entries for all papers in the YAML database
that are not yet in the BibTeX file.
"""

import yaml
import re
from pathlib import Path
from datetime import datetime

def load_yaml_papers(yaml_path: str) -> dict:
    """Load papers from YAML database."""
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return {paper['id']: paper for paper in data.get('sources', [])}

def load_existing_bibtex_ids(bib_path: str) -> set:
    """Extract existing BibTeX entry IDs."""
    ids = set()
    with open(bib_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Match @type{id, patterns
    for match in re.finditer(r'@\w+\{([^,]+),', content):
        ids.add(match.group(1).strip())
    return ids

def escape_bibtex(text: str) -> str:
    """Escape special characters for BibTeX."""
    if not text:
        return ''
    # Escape special characters
    text = text.replace('&', r'\&')
    text = text.replace('%', r'\%')
    text = text.replace('$', r'\$')
    text = text.replace('#', r'\#')
    text = text.replace('_', r'\_')
    return text

def format_authors(authors: list) -> str:
    """Format author list for BibTeX."""
    if not authors:
        return 'Unknown'
    return ' and '.join(authors)

def generate_bibtex_entry(paper_id: str, paper: dict) -> str:
    """Generate a BibTeX entry from YAML paper data."""
    paper_type = paper.get('type', 'article')

    # Map YAML types to BibTeX types
    type_mapping = {
        'journal_article': 'article',
        'book': 'book',
        'book_chapter': 'incollection',
        'working_paper': 'techreport',
        'conference': 'inproceedings',
        'report': 'techreport',
    }
    bib_type = type_mapping.get(paper_type, 'article')

    # Build entry
    lines = [f"@{bib_type}{{{paper_id},"]

    # Required fields
    title = escape_bibtex(paper.get('title', 'Unknown Title'))
    lines.append(f"  title={{{title}}},")

    authors = format_authors(paper.get('authors', []))
    lines.append(f"  author={{{authors}}},")

    year = paper.get('year', 'n.d.')
    lines.append(f"  year={{{year}}},")

    # Optional fields
    if paper.get('journal'):
        journal = escape_bibtex(paper['journal'])
        lines.append(f"  journal={{{journal}}},")

    if paper.get('volume'):
        lines.append(f"  volume={{{paper['volume']}}},")

    if paper.get('issue'):
        lines.append(f"  number={{{paper['issue']}}},")

    if paper.get('pages'):
        lines.append(f"  pages={{{paper['pages']}}},")

    if paper.get('doi'):
        lines.append(f"  doi={{{paper['doi']}}},")

    if paper.get('url'):
        lines.append(f"  url={{{paper['url']}}},")

    if paper.get('publisher'):
        publisher = escape_bibtex(paper['publisher'])
        lines.append(f"  publisher={{{publisher}}},")

    # Add evidence metadata as comments
    if paper.get('9c_coordinates'):
        coord = paper['9c_coordinates'][0] if isinstance(paper['9c_coordinates'], list) else paper['9c_coordinates']
        if isinstance(coord, dict):
            domain = coord.get('domain', '')
            stage = coord.get('stages', [''])[0] if isinstance(coord.get('stages'), list) else coord.get('stages', '')
            lines.append(f"  % 10C: domain={domain}, stage={stage}")

    if paper.get('key_findings'):
        finding = paper['key_findings'][0] if isinstance(paper['key_findings'], list) else paper['key_findings']
        if isinstance(finding, dict) and finding.get('effect_size'):
            lines.append(f"  % effect_size = {finding['effect_size']}")

    lines.append("}")

    return '\n'.join(lines)

def main():
    base_path = Path(__file__).parent.parent
    yaml_path = base_path / 'data' / 'paper-sources.yaml'
    bib_path = base_path / 'bibliography' / 'bcm_master.bib'

    print("=== YAML to BibTeX Sync ===\n")

    # Load data
    print("Loading YAML database...")
    yaml_papers = load_yaml_papers(yaml_path)
    print(f"  Found {len(yaml_papers)} papers in YAML\n")

    print("Loading existing BibTeX entries...")
    existing_ids = load_existing_bibtex_ids(bib_path)
    print(f"  Found {len(existing_ids)} existing entries\n")

    # Find missing papers
    missing_ids = set(yaml_papers.keys()) - existing_ids
    print(f"Missing papers to add: {len(missing_ids)}\n")

    if not missing_ids:
        print("No new papers to add. Database is synchronized!")
        return

    # Generate new entries
    print("Generating BibTeX entries...")
    new_entries = []

    # Group by first author for organization
    by_author = {}
    for paper_id in sorted(missing_ids):
        paper = yaml_papers[paper_id]
        first_author = paper.get('authors', ['Unknown'])[0].split(',')[0].lower()
        if first_author not in by_author:
            by_author[first_author] = []
        by_author[first_author].append((paper_id, paper))

    # Generate entries grouped by author
    for author in sorted(by_author.keys()):
        new_entries.append(f"\n% === {author.upper()} ===")
        for paper_id, paper in by_author[author]:
            entry = generate_bibtex_entry(paper_id, paper)
            new_entries.append(entry)

    # Append to BibTeX file
    print(f"Appending {len(missing_ids)} new entries to bcm_master.bib...")

    with open(bib_path, 'a', encoding='utf-8') as f:
        f.write(f"\n\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        f.write(f"\n% AUTO-GENERATED FROM paper-sources.yaml")
        f.write(f"\n% Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        f.write(f"\n% Papers added: {len(missing_ids)}")
        f.write(f"\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")
        f.write('\n'.join(new_entries))

    print(f"\nDone! Added {len(missing_ids)} new BibTeX entries.")
    print(f"Total entries now: {len(existing_ids) + len(missing_ids)}")

if __name__ == '__main__':
    main()
