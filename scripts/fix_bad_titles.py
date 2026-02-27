#!/usr/bin/env python3
# ┌─────────────────────────────────────────────────────────────────────────┐
# │  ⚠️  DEPRECATED (2026-02-08)                                            │
# │                                                                         │
# │  Einmaliges Migrations-Script: Abgeschnittene Titel in                 │
# │  extracted_papers.yaml durch LaTeX-Quellensuche korrigiert.            │
# │  Arbeit abgeschlossen (TL-025). Kept for reference only.              │
# │                                                                         │
# │  SSOT: data/paper-references/PAP-*.yaml + bibliography/bcm_master.bib │
# │  Neue Papers: /integrate-paper Workflow                                │
# └─────────────────────────────────────────────────────────────────────────┘
"""
fix_bad_titles.py — Look up real titles for papers with bad/truncated titles
in extracted_papers.yaml by searching the original LIT-appendix LaTeX files.

⚠️  DEPRECATED — Migration complete (TL-025, 2026-02-08).

The extraction script (extract_papers_from_lit.py) truncated many titles to
single characters or placeholders. This script recovers the real titles by
searching the LaTeX source files for author+year patterns.

Usage:
    python scripts/fix_bad_titles.py --dry-run          # Preview matches
    python scripts/fix_bad_titles.py --batch 1           # Fix 1 paper
    python scripts/fix_bad_titles.py                     # Fix all
    python scripts/fix_bad_titles.py --status            # Show stats
"""

import argparse
import os
import re
import sys
import yaml
from pathlib import Path

ROOT = Path(__file__).parent.parent
EXTRACTED_PATH = ROOT / "data" / "extracted_papers.yaml"
APPENDICES_DIR = ROOT / "appendices"


def is_bad_title(title):
    """Check if a title is bad (truncated or placeholder)."""
    if not title:
        return True
    return len(title) <= 20 or "to be added" in title.lower()


def extract_surname(authors):
    """Extract first author surname from authors list."""
    if not authors:
        return None
    first = authors[0]
    surname = first.split(",")[0].strip()
    # Handle "von X" style names
    surname = surname.split(".")[-1].strip()
    return surname


def find_title_in_latex(surname, year, latex_path):
    """Search a LaTeX file for a paper citation and extract the title.

    Looks for patterns like:
    \\item Surname, ... (YEAR). TITLE. \\textit{Journal}
    \\item Surname, ... (YEAR). \\textit{TITLE}. Publisher
    \\item Surname ... (YEAR). TITLE.
    """
    if not latex_path.exists():
        return None, "file_not_found"

    with open(latex_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Normalize surname for matching (case-insensitive)
    surname_lower = surname.lower()
    year_str = str(year)

    # Strategy 1: Find \item lines with author+year
    # Pattern: \item [Author stuff] (Year). [Title].
    lines = content.split("\n")
    for i, line in enumerate(lines):
        line_lower = line.lower()

        # Check if line contains both surname and year
        if surname_lower not in line_lower:
            continue
        if year_str not in line:
            continue
        if "\\item" not in line_lower and "\\textbf{" not in line_lower:
            continue

        # Found a matching line - extract title
        # Combine with next line(s) in case of line wrapping
        combined = line
        for j in range(1, 4):
            if i + j < len(lines):
                next_line = lines[i + j].strip()
                if next_line.startswith("\\item") or next_line.startswith("\\end{"):
                    break
                combined += " " + next_line

        title = extract_title_from_citation(combined, year_str)
        if title and len(title) > 10:
            return title, "item_match"

    # Strategy 2: Search for textbf{Author} patterns
    for i, line in enumerate(lines):
        line_lower = line.lower()
        if surname_lower not in line_lower or year_str not in line:
            continue
        if "\\textbf{" not in line:
            continue

        combined = line
        for j in range(1, 4):
            if i + j < len(lines):
                next_line = lines[i + j].strip()
                if next_line.startswith("\\item") or next_line.startswith("\\end{"):
                    break
                combined += " " + next_line

        title = extract_title_from_citation(combined, year_str)
        if title and len(title) > 10:
            return title, "textbf_match"

    # Strategy 3: Broader search - any line with surname+year
    for i, line in enumerate(lines):
        line_lower = line.lower()
        if surname_lower not in line_lower or year_str not in line:
            continue

        # Skip comment lines
        if line.strip().startswith("%"):
            continue

        combined = line
        for j in range(1, 4):
            if i + j < len(lines):
                next_line = lines[i + j].strip()
                if not next_line or next_line.startswith("\\item") or next_line.startswith("\\end{"):
                    break
                combined += " " + next_line

        title = extract_title_from_citation(combined, year_str)
        if title and len(title) > 10:
            return title, "broad_match"

    return None, "not_found"


def extract_title_from_citation(text, year):
    """Extract a title from a citation text.

    Handles patterns like:
    - Author (Year). Title. \\textit{Journal}
    - Author (Year). \\textit{Title}. Publisher
    - Author (Year). Title. Publisher.
    """
    # Clean up LaTeX commands for matching
    clean = text.replace("\n", " ").strip()

    # Pattern 1: (Year). Title. \textit{
    m = re.search(
        r'\(' + year + r'[a-z]?\)\.\s*(.+?)\.\s*\\textit\{',
        clean
    )
    if m:
        title = m.group(1).strip()
        title = clean_latex(title)
        if len(title) > 5:
            return title

    # Pattern 2: (Year). \textit{Title}.
    m = re.search(
        r'\(' + year + r'[a-z]?\)\.\s*\\textit\{([^}]+)\}',
        clean
    )
    if m:
        title = m.group(1).strip()
        title = clean_latex(title)
        if len(title) > 5:
            return title

    # Pattern 3: (Year). Title.  (take until next period, at least 20 chars)
    m = re.search(
        r'\(' + year + r'[a-z]?\)\.\s*(.+?)(?:\.\s|$)',
        clean
    )
    if m:
        title = m.group(1).strip()
        title = clean_latex(title)
        if len(title) > 20:
            return title

    # Pattern 4: (Year). followed by long text (might span patterns)
    m = re.search(
        r'\(' + year + r'[a-z]?\)\.\s*(.{20,}?)(?:\.\s*(?:\\textit|In:|Retrieved|Available|doi|http)|\.\s*$)',
        clean
    )
    if m:
        title = m.group(1).strip()
        title = clean_latex(title)
        if len(title) > 10:
            return title

    # Pattern 5: Just grab everything after (Year). up to reasonable length
    m = re.search(
        r'\(' + year + r'[a-z]?\)\.\s*(.{10,})',
        clean
    )
    if m:
        raw = m.group(1).strip()
        # Take up to first sentence end
        parts = re.split(r'\.\s', raw, maxsplit=1)
        title = parts[0].strip()
        title = clean_latex(title)
        if len(title) > 10:
            return title

    return None


def clean_latex(text):
    """Remove LaTeX formatting from text."""
    text = re.sub(r'\\textit\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\textbf\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\emph\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\enquote\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\[a-zA-Z]+\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\&', '&', text)
    text = re.sub(r'---', '—', text)
    text = re.sub(r'--', '–', text)
    text = text.replace('\\', '')
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def main():
    parser = argparse.ArgumentParser(description="Fix bad titles in extracted_papers.yaml")
    parser.add_argument("--batch", type=int, help="Process N papers")
    parser.add_argument("--dry-run", action="store_true", help="Preview only")
    parser.add_argument("--status", action="store_true", help="Show statistics")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    args = parser.parse_args()

    # Load data
    with open(EXTRACTED_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    papers = data["extracted_papers"]

    # Find bad-title papers
    bad_papers = [(i, p) for i, p in enumerate(papers) if is_bad_title(p.get("title", ""))]

    if args.status:
        print(f"Total papers: {len(papers)}")
        print(f"Bad titles:   {len(bad_papers)}")
        single_char = sum(1 for _, p in bad_papers if len(p.get("title", "")) <= 3)
        placeholder = sum(1 for _, p in bad_papers if "to be added" in p.get("title", "").lower())
        short = len(bad_papers) - single_char - placeholder
        print(f"  Single char:  {single_char}")
        print(f"  Placeholder:  {placeholder}")
        print(f"  Short (<20):  {short}")
        return

    to_process = bad_papers[:args.batch] if args.batch else bad_papers

    fixed = 0
    not_found = 0
    results = []

    for idx, paper in to_process:
        pid = paper["id"]
        old_title = paper.get("title", "")
        surname = extract_surname(paper.get("authors", []))
        year = paper.get("year", "")
        source = paper.get("extraction_source", "")

        if not surname or not year or not source:
            results.append({"id": pid, "status": "skip", "reason": "missing_metadata"})
            continue

        # Find LaTeX file
        latex_path = APPENDICES_DIR / source
        if not latex_path.exists():
            # Try with .tex extension
            if not source.endswith(".tex"):
                latex_path = APPENDICES_DIR / (source + ".tex")

        new_title, match_type = find_title_in_latex(surname, year, latex_path)

        if new_title and new_title.strip() != old_title.strip():
            fixed += 1
            results.append({
                "id": pid, "status": "fixed", "match_type": match_type,
                "old": old_title, "new": new_title
            })
            if not args.dry_run:
                papers[idx]["title"] = new_title
        elif new_title and new_title.strip() == old_title.strip():
            # Title already correct, just short
            results.append({
                "id": pid, "status": "already_correct",
                "title": old_title
            })
            continue
        else:
            not_found += 1
            results.append({
                "id": pid, "status": "not_found",
                "old": old_title, "surname": surname, "year": year, "source": source
            })

    # Report
    print(f"{'[DRY RUN] ' if args.dry_run else ''}Results:")
    print(f"  Processed: {len(to_process)}")
    print(f"  Fixed:     {fixed}")
    print(f"  Not found: {not_found}")

    if args.verbose or args.dry_run:
        if any(r["status"] == "fixed" for r in results):
            print(f"\nFixed titles:")
            for r in results:
                if r["status"] == "fixed":
                    print(f"  {r['id']}: \"{r['old']}\" → \"{r['new'][:70]}\" ({r['match_type']})")

        if any(r["status"] == "not_found" for r in results):
            print(f"\nNot found:")
            for r in results:
                if r["status"] == "not_found":
                    print(f"  {r['id']}: {r['surname']} ({r['year']}) in {r['source']}")

    # Write back
    if not args.dry_run and fixed > 0:
        with open(EXTRACTED_PATH, "w", encoding="utf-8") as f:
            # Preserve the header comments
            f.write("# ┌─────────────────────────────────────────────────────────────────────────┐\n")
            f.write("# │  ⚠️  DEPRECATED (2026-02-08)                                            │\n")
            f.write("# │                                                                         │\n")
            f.write("# │  SSOT ist jetzt: data/paper-references/PAP-*.yaml + bcm_master.bib     │\n")
            f.write("# │                                                                         │\n")
            f.write("# │  Diese Datei ist ein Zwischenprodukt von extract_papers_from_lit.py.   │\n")
            f.write("# │  137 von 138 Einträgen sind NICHT im SSOT (bcm_master.bib).           │\n")
            f.write("# │  Neue Paper-Integration läuft über /integrate-paper Workflow.           │\n")
            f.write("# │                                                                         │\n")
            f.write("# │  NICHT MEHR BEARBEITEN. Bei Fragen: task-log.yaml TL-008              │\n")
            f.write("# └─────────────────────────────────────────────────────────────────────────┘\n\n")
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        print(f"\nUpdated {fixed} titles in {EXTRACTED_PATH}")


if __name__ == "__main__":
    main()
