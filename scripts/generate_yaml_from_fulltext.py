#!/usr/bin/env python3
"""Generate YAML metadata for orphaned full-text papers.

Orphaned = has PAP-*.md in data/paper-texts/ but no PAP-*.yaml in data/paper-references/.
Parses the markdown header (YAML frontmatter + structured title/author/journal lines)
to create a minimal but valid paper-reference YAML.

Usage:
    python scripts/generate_yaml_from_fulltext.py                  # dry-run all
    python scripts/generate_yaml_from_fulltext.py --execute         # create YAMLs
    python scripts/generate_yaml_from_fulltext.py --key PAP-berger2026labor  # single paper
    python scripts/generate_yaml_from_fulltext.py --limit 10 --execute       # first 10
"""

import argparse
import glob
import os
import re
import sys
from datetime import date

TEXTS_DIR = "data/paper-texts"
REFS_DIR = "data/paper-references"


def find_orphaned():
    """Find full texts without corresponding YAML."""
    orphaned = []
    for md_path in sorted(glob.glob(os.path.join(TEXTS_DIR, "PAP-*.md"))):
        key = os.path.basename(md_path).replace(".md", "")
        yaml_path = os.path.join(REFS_DIR, f"{key}.yaml")
        if not os.path.exists(yaml_path):
            orphaned.append((key, md_path))
    return orphaned


def parse_frontmatter(text):
    """Extract YAML frontmatter between --- markers."""
    meta = {}
    match = re.match(r'^---\s*\n(.*?)\n---', text, re.DOTALL)
    if not match:
        return meta

    for line in match.group(1).split('\n'):
        line = line.strip()
        if line.startswith('#'):
            # Comment lines may contain useful info
            if 'DOI:' in line:
                doi_match = re.search(r'DOI:\s*(10\.\S+)', line)
                if doi_match:
                    meta['doi'] = doi_match.group(1)
            if 'Word count:' in line:
                wc_match = re.search(r'Word count:\s*(\d+)', line)
                if wc_match:
                    meta['word_count'] = int(wc_match.group(1))
            if 'Content level:' in line:
                cl_match = re.search(r'Content level:\s*(L\d)', line)
                if cl_match:
                    meta['content_level'] = cl_match.group(1)
            if 'Pages:' in line:
                meta['pages_raw'] = re.search(r'Pages:\s*(.+)', line).group(1).strip()
            if 'abstract only' in line.lower() or 'L1' in line:
                meta['content_level'] = 'L1'
            if 'Source:' in line:
                meta['source'] = re.search(r'Source:\s*(.+)', line).group(1).strip()
            if 'Fetched:' in line:
                meta['fetched'] = re.search(r'Fetched:\s*(.+)', line).group(1).strip()
    return meta


def parse_body(text):
    """Extract title, authors, journal from markdown body."""
    meta = {}

    # Remove frontmatter
    body = re.sub(r'^---.*?---\s*', '', text, flags=re.DOTALL)

    # Title: first # heading
    title_match = re.match(r'#\s+(.+)', body.strip())
    if title_match:
        meta['title'] = title_match.group(1).strip()

    # Authors: **Authors:** line
    author_match = re.search(r'\*\*Authors?:\*\*\s*(.+)', body)
    if author_match:
        meta['authors_raw'] = author_match.group(1).strip()
        # Extract first author last name
        first_author = meta['authors_raw'].split(',')[0].strip()
        # Handle "First Last" format
        parts = first_author.split()
        if len(parts) >= 2:
            meta['first_author_last'] = parts[-1].strip()
        else:
            meta['first_author_last'] = first_author

    # Journal: **Journal:** line
    journal_match = re.search(r'\*\*Journal:\*\*\s*(.+)', body)
    if journal_match:
        meta['journal_raw'] = journal_match.group(1).strip()

    # Abstract: ## Abstract section
    abstract_match = re.search(r'##\s*Abstract\s*\n\n(.+?)(?:\n\n|\n##|\Z)', body, re.DOTALL)
    if abstract_match:
        meta['abstract'] = abstract_match.group(1).strip()

    return meta


def infer_bibtex_key(pap_key):
    """Convert PAP-key to bibtex_key (remove PAP- prefix)."""
    return pap_key.replace("PAP-", "")


def determine_content_level(fm_meta, body_meta, word_count):
    """Determine content level from available info."""
    if fm_meta.get('content_level'):
        return fm_meta['content_level']
    if word_count and word_count > 5000:
        return 'L3'
    if word_count and word_count > 500:
        return 'L2'
    return 'L1'


def determine_year(bibtex_key):
    """Extract year from bibtex key like berger2026labor."""
    year_match = re.search(r'(\d{4})', bibtex_key)
    if year_match:
        return year_match.group(1)
    return str(date.today().year)


def determine_publication_type(body_meta):
    """Infer publication type from journal info."""
    journal = body_meta.get('journal_raw', '')
    if 'Journal of Economic Perspectives' in journal:
        return 'article'
    if 'Quarterly Journal' in journal or 'American Economic Review' in journal:
        return 'article'
    if 'Working Paper' in journal or 'NBER' in journal:
        return 'working_paper'
    return 'article'


def structural_characteristics(word_count, body_meta):
    """Determine S1-S6 based on available content."""
    has_abstract = bool(body_meta.get('abstract'))
    is_fulltext = word_count and word_count > 5000

    return {
        'S1_research_question': True,  # Title implies research question
        'S2_methodology': is_fulltext,
        'S3_sample_data': is_fulltext,
        'S4_findings': is_fulltext or has_abstract,
        'S5_validity': False,
        'S6_reproducibility': False,
    }


def generate_yaml(pap_key, md_path):
    """Generate YAML content for an orphaned paper."""
    with open(md_path, 'r', encoding='utf-8') as f:
        text = f.read()

    fm_meta = parse_frontmatter(text)
    body_meta = parse_body(text)
    bibtex_key = infer_bibtex_key(pap_key)
    year = determine_year(bibtex_key)
    word_count = fm_meta.get('word_count', len(text.split()))
    content_level = determine_content_level(fm_meta, body_meta, word_count)
    pub_type = determine_publication_type(body_meta)
    s_chars = structural_characteristics(word_count, body_meta)

    title = body_meta.get('title', bibtex_key)
    author = body_meta.get('first_author_last', bibtex_key.split(str(year))[0].capitalize() if year in bibtex_key else 'Unknown')
    doi = fm_meta.get('doi', '')

    # Build abstract (truncate if needed)
    abstract = body_meta.get('abstract', '')
    if not abstract and word_count and word_count < 500:
        # For short texts (abstract-only), use the body as abstract
        body = re.sub(r'^---.*?---\s*', '', text, flags=re.DOTALL)
        body = re.sub(r'#.*\n', '', body)
        body = re.sub(r'\*\*.*?\*\*\s*', '', body)
        abstract = body.strip()[:500]

    # Escape YAML special chars in strings
    def yaml_str(s):
        if not s:
            return 'null'
        s = s.replace("'", "''")
        if ':' in s or '#' in s or '\n' in s or s.startswith('{') or s.startswith('['):
            return f"'{s}'"
        return s

    def yaml_multiline(s, indent=2):
        if not s:
            return 'null'
        prefix = ' ' * indent
        lines = s.split('\n')
        return '|\n' + '\n'.join(f'{prefix}{line}' for line in lines)

    # Generate YAML
    yaml_lines = [
        f"paper: {bibtex_key}",
        f"superkey: {pap_key}",
        f"title: {yaml_str(title)}",
        f"author: {yaml_str(author)}",
        f"year: '{year}'",
        f"publication_type: {pub_type}",
        f"doi: {yaml_str(doi) if doi else 'null'}",
    ]

    # Abstract
    if abstract:
        yaml_lines.append(f"abstract: {yaml_multiline(abstract)}")
    else:
        yaml_lines.append("abstract: null")

    yaml_lines.append(f"abstract_source: fulltext_extraction")

    # URL
    yaml_lines.append("url: null")

    # References
    yaml_lines.extend([
        "reference_count: 0",
        "references: []",
    ])

    # Structural characteristics
    yaml_lines.extend([
        "structural_characteristics:",
        f"  S1_research_question: {str(s_chars['S1_research_question']).lower()}",
        f"  S2_methodology: {str(s_chars['S2_methodology']).lower()}",
        f"  S3_sample_data: {str(s_chars['S3_sample_data']).lower()}",
        f"  S4_findings: {str(s_chars['S4_findings']).lower()}",
        f"  S5_validity: {str(s_chars['S5_validity']).lower()}",
        f"  S6_reproducibility: {str(s_chars['S6_reproducibility']).lower()}",
    ])

    # Full text reference
    yaml_lines.extend([
        "full_text:",
        "  available: true",
        f"  path: \"{md_path}\"",
        f"  content_level: {content_level}",
        "  template_available: false",
        "  template_char_count: 0",
        f"  archived_date: \"{date.today().isoformat()}\"",
    ])

    # EBF integration (minimal - to be enriched later)
    yaml_lines.extend([
        "ebf_integration:",
        "  evidence_tier: 2",
        "  use_for:",
        "  - LIT-O",
        "  theory_support: null",
        "  parameter: null",
        "  identification: null",
    ])

    # Status
    yaml_lines.extend([
        "status:",
        "  integration_level: I1",
        f"  content_level: {content_level}",
        f"  created_date: \"{date.today().isoformat()}\"",
        "  created_by: generate_yaml_from_fulltext.py",
        "  needs_review: true",
    ])

    return '\n'.join(yaml_lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description="Generate YAML for orphaned full texts")
    parser.add_argument('--execute', action='store_true', help='Actually create files (default: dry-run)')
    parser.add_argument('--key', type=str, help='Process single paper key (e.g., PAP-berger2026labor)')
    parser.add_argument('--limit', type=int, help='Process only N papers')
    parser.add_argument('--skip-jep-gdrive', action='store_true', help='Skip PAP-jep-gdrive-* (full journal dumps)')
    args = parser.parse_args()

    orphaned = find_orphaned()

    if args.skip_jep_gdrive:
        orphaned = [(k, p) for k, p in orphaned if 'jep-gdrive' not in k]

    if args.key:
        orphaned = [(k, p) for k, p in orphaned if k == args.key]
        if not orphaned:
            print(f"ERROR: {args.key} not found or already has YAML")
            sys.exit(1)

    if args.limit:
        orphaned = orphaned[:args.limit]

    print(f"Found {len(orphaned)} orphaned full texts\n")

    for pap_key, md_path in orphaned:
        yaml_content = generate_yaml(pap_key, md_path)
        yaml_path = os.path.join(REFS_DIR, f"{pap_key}.yaml")

        if args.execute:
            with open(yaml_path, 'w', encoding='utf-8') as f:
                f.write(yaml_content)
            print(f"  CREATED: {yaml_path}")
        else:
            print(f"  [DRY-RUN] Would create: {yaml_path}")
            print(f"    Title: {yaml_content.split(chr(10))[2]}")
            print(f"    Year:  {yaml_content.split(chr(10))[4]}")
            print()

    if not args.execute:
        print(f"\nDry run complete. Use --execute to create {len(orphaned)} YAML files.")
    else:
        print(f"\nCreated {len(orphaned)} YAML files.")


if __name__ == '__main__':
    main()
