#!/usr/bin/env python3
# ┌─────────────────────────────────────────────────────────────────────────┐
# │  ⚠️  DEPRECATED (2026-02-08)                                            │
# │                                                                         │
# │  Einmaliges Extraktions-Script: Papers aus LIT-Appendices extrahiert   │
# │  und nach extracted_papers.yaml geschrieben.                           │
# │  Ziel-Datei (extracted_papers.yaml) ist DEPRECATED.                    │
# │  Kept for reference only.                                              │
# │                                                                         │
# │  SSOT: data/paper-references/PAP-*.yaml + bibliography/bcm_master.bib │
# │  Neue Papers: /integrate-paper Workflow                                │
# └─────────────────────────────────────────────────────────────────────────┘
"""
Extract papers from LIT-Appendices and generate YAML entries.

⚠️  DEPRECATED — Target file (extracted_papers.yaml) is deprecated (2026-02-08).

Supported formats (v2.0):
  1. \\item \\textbf{Author (Year).} Title. Journal.
  2. \\paragraph{Citation.} blocks
  3. \\subsubsection{Year: Title} with inline author
  4. Enumerated bibliography: \\item \\textbf{Author (Year).} ``Title'' \\textit{Journal}
  5. BibTeX citations: \\citet{key}, \\citep{key} with .bib lookup
  6. Inline bullet citations without \\textbf{}
  7. tcolorbox narrative citations

Output: YAML entries ready to merge into paper-sources.yaml
"""

import re
import os
import yaml
from pathlib import Path
from datetime import datetime
from collections import defaultdict


# =============================================================================
# BIBTEX PARSER
# =============================================================================

def load_bibtex_database(bib_paths):
    """Load and parse BibTeX files into a lookup dictionary."""
    bib_db = {}

    for bib_path in bib_paths:
        if not bib_path.exists():
            continue

        with open(bib_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Parse each BibTeX entry
        # Pattern matches @type{key, ... }
        entry_pattern = re.compile(
            r'@(\w+)\s*\{\s*([a-zA-Z0-9_]+)\s*,\s*(.*?)\n\}',
            re.DOTALL
        )

        for match in entry_pattern.finditer(content):
            entry_type = match.group(1).lower()
            key = match.group(2)
            fields_text = match.group(3)

            # Parse fields
            entry = {
                'id': key,
                'type': entry_type,
            }

            # Extract common fields
            field_pattern = re.compile(r'(\w+)\s*=\s*\{([^}]*)\}')
            for field_match in field_pattern.finditer(fields_text):
                field_name = field_match.group(1).lower()
                field_value = field_match.group(2).strip()

                if field_name == 'author':
                    entry['authors'] = parse_bibtex_authors(field_value)
                elif field_name == 'title':
                    entry['title'] = clean_latex(field_value)
                elif field_name == 'journal':
                    entry['journal'] = clean_latex(field_value)
                elif field_name == 'year':
                    try:
                        entry['year'] = int(field_value)
                    except ValueError:
                        pass
                elif field_name == 'booktitle':
                    if 'journal' not in entry:
                        entry['journal'] = clean_latex(field_value)
                elif field_name == 'publisher':
                    entry['publisher'] = clean_latex(field_value)

            bib_db[key] = entry

    return bib_db


def parse_bibtex_authors(author_str):
    """Parse BibTeX author string (Lastname, Firstname and Lastname2, Firstname2)."""
    if not author_str:
        return []

    # Split by " and "
    parts = re.split(r'\s+and\s+', author_str)
    authors = []

    for part in parts:
        part = part.strip()
        if not part:
            continue

        # Handle "Lastname, Firstname" format
        if ',' in part:
            lastname = part.split(',')[0].strip()
            authors.append(lastname)
        else:
            # "Firstname Lastname" - take last word
            words = part.split()
            if words:
                authors.append(words[-1])

    return authors


# =============================================================================
# LATEX CLEANING
# =============================================================================

def clean_latex(text):
    """Remove LaTeX commands and clean text."""
    if not text:
        return ''
    # Remove common LaTeX commands
    text = re.sub(r'\\emph\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\textbf\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\textit\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\&', '&', text)
    text = re.sub(r"``|''", '"', text)  # LaTeX quotes
    text = re.sub(r'"|"', '"', text)  # Unicode quotes
    text = re.sub(r'\\[a-zA-Z]+\{([^}]*)\}', r'\1', text)  # Other commands
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'^\s*[\-\*]\s*', '', text)  # Remove list markers
    return text.strip()


# =============================================================================
# AUTHOR PARSING
# =============================================================================

def parse_authors(author_str):
    """Parse author string into list of authors."""
    if not author_str:
        return []

    author_str = clean_latex(author_str)

    # Handle "et al."
    if 'et al' in author_str.lower():
        main_match = re.match(r'([A-Z][a-zA-Z\-\']+)', author_str)
        if main_match:
            return [f"{main_match.group(1)} et al."]
        return [author_str]

    # Split by &, \&, "and", or comma followed by capital (but not initials)
    parts = re.split(r'\s*(?:&|\\&|\band\b)\s*', author_str)

    authors = []
    for part in parts:
        part = part.strip()
        if not part:
            continue

        # Handle comma-separated multiple authors within one part
        # e.g., "Smith, J., Jones, K." -> split carefully
        subparts = re.split(r',\s*(?=[A-Z][a-z])', part)

        for subpart in subparts:
            subpart = subpart.strip()
            if not subpart:
                continue

            # Extract name (handle "Lastname, F." and "Firstname Lastname" formats)
            name_match = re.match(r'([A-Z][a-zA-Z\-\']+(?:,\s*[A-Z]\.?(?:\s*[A-Z]\.)?)?)', subpart)
            if name_match:
                name = name_match.group(1).strip()
                if name and len(name) > 1:
                    authors.append(name)

    return authors if authors else [author_str] if author_str else []


# =============================================================================
# PAPER ID GENERATION
# =============================================================================

def generate_paper_id(authors, year):
    """Generate a paper ID from authors and year."""
    if not authors:
        return f"unknown{year}"

    first_author = authors[0].lower()

    # Extract last name
    if ',' in first_author:
        last_name = first_author.split(',')[0]
    elif ' ' in first_author:
        parts = first_author.split()
        last_name = parts[0]  # Usually "Lastname, F."
    else:
        last_name = first_author

    # Clean: remove "et al", special chars
    last_name = last_name.replace('et al', '').strip()
    last_name = re.sub(r'[^a-z]', '', last_name)

    if not last_name:
        return f"unknown{year}"

    return f"{last_name}{year}"


# =============================================================================
# FORMAT PARSERS
# =============================================================================

def parse_item_textbf_entry(text):
    """
    Parse an \item \textbf{...} entry.

    Handles:
    - \item \textbf{Author (Year).} Title. Journal.
    - \item \textbf{Author (Year).} ``Title'' \textit{Journal}.
    """
    # Extract the textbf content and what follows
    match = re.match(r'\\item\s*\\textbf\{([^}]+)\}\s*(.*)', text, re.DOTALL)
    if not match:
        return None

    textbf_content = match.group(1).strip()
    rest = match.group(2).strip()

    # Extract year from textbf content
    year_match = re.search(r'\((\d{4})\)', textbf_content)
    if not year_match:
        # Try alternative: year at end without parens
        year_match = re.search(r'(\d{4})\s*$', textbf_content)
    if not year_match:
        return None

    year = int(year_match.group(1))

    # Extract authors (everything before the year)
    authors_str = textbf_content[:year_match.start()].strip()
    # Remove trailing punctuation
    authors_str = re.sub(r'[\.,;:\s]+$', '', authors_str)

    # Parse authors
    authors = parse_authors(authors_str)
    if not authors:
        return None

    # Extract title from rest
    title = None
    journal = None

    # Try LaTeX double-backtick quoted title first: ``Title''
    backtick_match = re.match(r"``([^']+)''\.?\s*(.*)", rest)
    if backtick_match:
        title = backtick_match.group(1)
        rest = backtick_match.group(2)
    else:
        # Try regular quoted title
        quote_match = re.match(r'["\']([^"\']+)["\']\.?\s*(.*)', rest)
        if quote_match:
            title = quote_match.group(1)
            rest = quote_match.group(2)
        else:
            # First sentence as title (up to period, but not abbreviations)
            sentence_match = re.match(r'([A-Z][^\.]+(?:\.[A-Z])?[^\.]*)\.\s*(.*)', rest)
            if sentence_match:
                title = sentence_match.group(1)
                rest = sentence_match.group(2)

    # Try to extract journal from rest
    if rest:
        # Look for \textit{Journal} or \emph{Journal} pattern
        journal_match = re.search(r'\\textit\{([^}]+)\}|\\emph\{([^}]+)\}', rest)
        if journal_match:
            journal = journal_match.group(1) or journal_match.group(2)

    return {
        'authors': authors,
        'year': year,
        'title': clean_latex(title) if title else None,
        'journal': clean_latex(journal) if journal else None,
    }


def parse_paragraph_citation(text):
    """
    Parse a \paragraph{Citation.} block.
    """
    text = text.strip()

    # Pattern: Author(s) (Year). "Title." Journal
    pattern = re.compile(
        r'([A-Z][a-zA-Z\-\']+(?:,\s*[A-Z][a-zA-Z\.\s]*)?(?:\s*(?:,|&|and)\s*[A-Z][a-zA-Z\-\']+(?:,\s*[A-Z][a-zA-Z\.\s]*)?)*(?:\s*et\s*al\.?)?)\s*\((\d{4})\)\.\s*[``"\']?([^"\']+?)["\'\.]?\s*(?:\\textit\{([^}]+)\}|\\emph\{([^}]+)\})?',
        re.MULTILINE
    )

    match = pattern.search(text)
    if not match:
        return None

    authors_str = match.group(1)
    year = int(match.group(2))
    title = match.group(3)
    journal = match.group(4) or match.group(5)

    authors = parse_authors(authors_str)
    if not authors:
        return None

    return {
        'authors': authors,
        'year': year,
        'title': clean_latex(title) if title else None,
        'journal': clean_latex(journal) if journal else None,
    }


def parse_inline_bullet_citation(text):
    """
    Parse inline bullet citations WITHOUT \textbf{} wrapper.

    Format: \item Author, A. (Year). Title. \textit{Journal}.
    """
    # Pattern for: Author(s) (Year). Title. \textit{Journal}
    pattern = re.compile(
        r'\\item\s+([A-Z][a-zA-Z\-\']+(?:,\s*[A-Z]\.?)?(?:\s*(?:,|&|\\&)\s*[A-Z][a-zA-Z\-\']+(?:,\s*[A-Z]\.?)?)*)\s*\((\d{4})\)\.\s*([^\\]+?)\.?\s*(?:\\textit\{([^}]+)\}|\\emph\{([^}]+)\})?',
        re.DOTALL
    )

    match = pattern.match(text)
    if not match:
        return None

    authors_str = match.group(1)
    year = int(match.group(2))
    title = match.group(3).strip()
    journal = match.group(4) or match.group(5)

    authors = parse_authors(authors_str)
    if not authors:
        return None

    return {
        'authors': authors,
        'year': year,
        'title': clean_latex(title) if title else None,
        'journal': clean_latex(journal) if journal else None,
    }


def parse_tcolorbox_citation(text):
    """
    Parse tcolorbox title citations.

    Format: \begin{tcolorbox}[...,title=Author & Author (Year)]
    """
    # Find title in tcolorbox options
    title_match = re.search(
        r'title\s*=\s*(?:Key Paper:\s*)?([A-Z][a-zA-Z\-\']+(?:\s*(?:,|&|\\&)\s*[A-Z][a-zA-Z\-\']+)*)\s*\((\d{4})\)',
        text
    )

    if not title_match:
        return None

    authors_str = title_match.group(1)
    year = int(title_match.group(2))

    authors = parse_authors(authors_str)
    if not authors:
        return None

    # Try to find title in the content
    paper_title = None
    title_line_match = re.search(r'\\textbf\{Title:\}\s*([^\n]+)', text)
    if title_line_match:
        paper_title = clean_latex(title_line_match.group(1))

    # Try to find source/journal
    journal = None
    source_match = re.search(r'\\textbf\{Source:\}\s*([^\n]+)', text)
    if source_match:
        journal = clean_latex(source_match.group(1))

    return {
        'authors': authors,
        'year': year,
        'title': paper_title,
        'journal': journal,
    }


def extract_bibtex_citations(content, bib_db):
    """
    Extract papers from \citet{key} and \citep{key} citations.
    Returns dict of papers found in bib_db.
    """
    papers = {}

    # Find all citation keys
    cite_pattern = re.compile(r'\\cite[tp]?\{([a-zA-Z0-9_,\s]+)\}')

    for match in cite_pattern.finditer(content):
        keys_str = match.group(1)
        keys = [k.strip() for k in keys_str.split(',')]

        for key in keys:
            if key in bib_db and key not in papers:
                entry = bib_db[key]
                if 'year' in entry and 'authors' in entry:
                    papers[key] = {
                        'authors': entry['authors'],
                        'year': entry['year'],
                        'title': entry.get('title'),
                        'journal': entry.get('journal'),
                        'bibtex_key': key,
                    }

    return papers


# =============================================================================
# MAIN EXTRACTION
# =============================================================================

def extract_from_file(filepath, bib_db=None):
    """Extract papers from a single LIT-Appendix file."""
    papers = {}

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    filename = os.path.basename(filepath)

    # Method 1: \item \textbf{...} blocks (original + improved)
    pattern1 = re.compile(
        r'\\item\s*\\textbf\{[^}]+\}[^\n]*(?:\n(?!\s*\\item|\s*\\end|\s*\\begin\{quote\})[^\n]*)*',
        re.MULTILINE
    )

    for match in pattern1.finditer(content):
        entry_text = match.group(0)
        parsed = parse_item_textbf_entry(entry_text)
        if parsed:
            add_paper(papers, parsed, filename, 'item_textbf')

    # Method 2: \paragraph{Citation.} blocks
    pattern2 = re.compile(
        r'\\paragraph\{Citation\.?\}\s*\n?([^\n]+(?:\n(?!\\paragraph|\\subsubsection)[^\n]*)*)',
        re.MULTILINE
    )

    for match in pattern2.finditer(content):
        citation_text = match.group(1)
        parsed = parse_paragraph_citation(citation_text)
        if parsed:
            add_paper(papers, parsed, filename, 'paragraph_citation')

    # Method 3: \subsubsection{Year: Title} with inline author
    pattern3 = re.compile(
        r'\\subsubsection\{(\d{4}):\s*([^}]+)\}.*?\\paragraph\{Citation\.?\}\s*\n?([^\n]+)',
        re.DOTALL
    )

    for match in pattern3.finditer(content):
        year = int(match.group(1))
        subsec_title = match.group(2).strip()
        citation_line = match.group(3).strip()

        # Extract author from citation line
        author_match = re.match(r'([A-Z][a-zA-Z\-\']+(?:,\s*[A-Z][a-zA-Z\.\s]*)?(?:\s*(?:,|&|and)\s*[A-Z][a-zA-Z\-\']+(?:,\s*[A-Z][a-zA-Z\.\s]*)?)*)', citation_line)
        if author_match:
            authors = parse_authors(author_match.group(1))
            # Extract journal
            journal_match = re.search(r'\\textit\{([^}]+)\}|\\emph\{([^}]+)\}', citation_line)
            journal = journal_match.group(1) or journal_match.group(2) if journal_match else None

            parsed = {
                'authors': authors,
                'year': year,
                'title': clean_latex(subsec_title),
                'journal': clean_latex(journal) if journal else None,
            }
            add_paper(papers, parsed, filename, 'subsubsection_year')

    # Method 4: Inline bullet citations without \textbf{}
    pattern4 = re.compile(
        r'\\item\s+[A-Z][a-zA-Z\-\',\s\.&\\]+\s*\(\d{4}\)\.[^\n]+',
        re.MULTILINE
    )

    for match in pattern4.finditer(content):
        entry_text = match.group(0)
        # Skip if already handled by method 1 (has \textbf)
        if '\\textbf' in entry_text:
            continue
        parsed = parse_inline_bullet_citation(entry_text)
        if parsed:
            add_paper(papers, parsed, filename, 'inline_bullet')

    # Method 5: tcolorbox citations
    pattern5 = re.compile(
        r'\\begin\{tcolorbox\}\[([^\]]*title=[^\]]+)\](.*?)\\end\{tcolorbox\}',
        re.DOTALL
    )

    for match in pattern5.finditer(content):
        tcolorbox_opts = match.group(1)
        tcolorbox_content = match.group(2)
        full_text = tcolorbox_opts + tcolorbox_content

        parsed = parse_tcolorbox_citation(full_text)
        if parsed:
            add_paper(papers, parsed, filename, 'tcolorbox')

    # Method 6: BibTeX citations (if database provided)
    if bib_db:
        bibtex_papers = extract_bibtex_citations(content, bib_db)
        for key, parsed in bibtex_papers.items():
            add_paper(papers, parsed, filename, 'bibtex_citation')

    return papers


def add_paper(papers, parsed, filename, method='unknown'):
    """Add a parsed paper to the papers dict, handling duplicates."""
    paper_id = generate_paper_id(parsed['authors'], parsed['year'])

    # Handle duplicates
    original_id = paper_id
    suffix = 0
    while paper_id in papers:
        # Check if it's actually the same paper (same year, similar authors)
        existing = papers[paper_id]
        if existing['year'] == parsed['year']:
            # Likely same paper, skip
            return
        suffix += 1
        paper_id = f"{original_id}_{chr(96+suffix)}"
        if suffix > 26:
            return

    papers[paper_id] = {
        'id': paper_id,
        'authors': parsed['authors'],
        'year': parsed['year'],
        'title': parsed.get('title'),
        'journal': parsed.get('journal'),
        'source_file': filename,
        'extraction_method': method,
    }

    # Add bibtex_key if present
    if 'bibtex_key' in parsed:
        papers[paper_id]['bibtex_key'] = parsed['bibtex_key']


def load_existing_yaml_ids(yaml_path):
    """Load existing paper IDs from YAML database."""
    ids = set()
    try:
        with open(yaml_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('- id:'):
                    paper_id = line.split(':', 1)[1].strip()
                    ids.add(paper_id)
    except Exception as e:
        print(f"Warning: Could not load existing YAML: {e}")
    return ids


def generate_yaml_entry(paper):
    """Generate a YAML entry for a paper."""
    entry = {
        'id': paper['id'],
        'authors': paper['authors'],
        'year': paper['year'],
        'title': paper.get('title') or 'Title to be added',
        'status': 'extracted',
        'type': 'journal_article',
        'extraction_source': paper.get('source_file', 'unknown'),
        'extraction_method': paper.get('extraction_method', 'unknown'),
    }

    if paper.get('journal'):
        entry['journal'] = paper['journal']

    if paper.get('bibtex_key'):
        entry['bibtex_key'] = paper['bibtex_key']

    # Placeholder 10C coordinates
    entry['9c_coordinates'] = [{
        'domain': 'to_be_classified',
        'stages': ['to_be_classified'],
        'primary_dimension': 'X',
    }]

    return entry


def main():
    base_path = Path(__file__).parent.parent
    appendices_path = base_path / 'appendices'
    yaml_path = base_path / 'data' / 'paper-sources.yaml'
    output_path = base_path / 'data' / 'extracted_papers.yaml'
    bib_path = base_path / 'bibliography' / 'bcm_master.bib'

    print("=" * 70)
    print("EXTRACT PAPERS FROM LIT-APPENDICES (v2.0)")
    print("=" * 70)
    print()
    print("Supported formats:")
    print("  1. \\item \\textbf{Author (Year).} Title. Journal.")
    print("  2. \\paragraph{Citation.} blocks")
    print("  3. \\subsubsection{Year: Title} with author")
    print("  4. \\item \\textbf{Author (Year).} ``Title'' \\textit{Journal}")
    print("  5. \\citet{key}, \\citep{key} with .bib lookup")
    print("  6. Inline bullet citations without \\textbf{}")
    print("  7. tcolorbox narrative citations")
    print()

    # Load BibTeX database
    print("Loading BibTeX database...")
    bib_paths = [bib_path]
    # Also check for other .bib files
    bib_paths.extend(base_path.glob('bibliography/*.bib'))
    bib_db = load_bibtex_database(bib_paths)
    print(f"Loaded {len(bib_db)} BibTeX entries")
    print()

    # Find all relevant files
    lit_files = set()
    for pattern in ['*LIT*.tex', '*_papers.tex', '*_research.tex']:
        lit_files.update(appendices_path.glob(pattern))
    lit_files = sorted(lit_files)

    print(f"Found {len(lit_files)} LIT-Appendix files")
    print()

    # Load existing paper IDs
    print("Loading existing paper IDs from paper-sources.yaml...")
    existing_ids = load_existing_yaml_ids(yaml_path)
    print(f"Found {len(existing_ids)} existing papers")
    print()

    # Extract papers from all files
    all_papers = {}
    papers_by_file = defaultdict(int)
    papers_by_method = defaultdict(int)

    print("Extracting papers from files...")
    for filepath in lit_files:
        papers = extract_from_file(filepath, bib_db)
        papers_by_file[filepath.name] = len(papers)

        for paper_id, paper in papers.items():
            # Use base ID for deduplication
            base_id = re.sub(r'_[a-z]$', '', paper_id)
            if base_id not in all_papers and paper_id not in all_papers:
                all_papers[paper_id] = paper
                papers_by_method[paper.get('extraction_method', 'unknown')] += 1

    print(f"\nExtracted {len(all_papers)} unique papers")
    print()

    # Show stats by method
    print("Papers by extraction method:")
    for method, count in sorted(papers_by_method.items(), key=lambda x: -x[1]):
        print(f"  {count:4d}  {method}")
    print()

    # Show stats by file
    print("Papers extracted by file (top 25):")
    for filename, count in sorted(papers_by_file.items(), key=lambda x: -x[1])[:25]:
        print(f"  {count:4d}  {filename}")
    print()

    # Filter out existing
    new_papers = {}
    for pid, p in all_papers.items():
        base_id = re.sub(r'_[a-z]$', '', pid)
        if base_id not in existing_ids and pid not in existing_ids:
            new_papers[pid] = p

    print(f"New papers (not in paper-sources.yaml): {len(new_papers)}")
    print()

    # Count papers with complete metadata
    complete_count = sum(1 for p in new_papers.values()
                        if p.get('title') and p['title'] != 'Title to be added')
    print(f"Papers with extracted titles: {complete_count}/{len(new_papers)}")
    print()

    # Generate YAML output
    print(f"Generating YAML output to {output_path}...")

    yaml_entries = []
    for paper_id in sorted(new_papers.keys()):
        entry = generate_yaml_entry(new_papers[paper_id])
        yaml_entries.append(entry)

    output_content = {
        'metadata': {
            'generated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'source': 'extract_papers_from_lit.py v2.0',
            'total_extracted': len(yaml_entries),
            'extraction_methods': dict(papers_by_method),
            'note': '10C coordinates need classification; some titles may need review',
        },
        'extracted_papers': yaml_entries,
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        yaml.dump(output_content, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    print(f"\nDone! Extracted {len(yaml_entries)} new papers.")
    print(f"Output written to: {output_path}")
    print()
    print("Next steps:")
    print("  1. Review extracted_papers.yaml")
    print("  2. Merge into paper-sources.yaml")
    print("  3. Run: python scripts/sync_yaml_to_bibtex.py")

if __name__ == '__main__':
    main()
