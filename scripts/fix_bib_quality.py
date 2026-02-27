#!/usr/bin/env python3
# ┌─────────────────────────────────────────────────────────────────────────┐
# │  ⚠️  DEPRECATED (2026-02-08)                                            │
# │                                                                         │
# │  Einmaliges Migrations-Script: BIB-Qualität der 47 auto-importierten   │
# │  Einträge aus extracted_papers.yaml bereinigt.                         │
# │  Arbeit abgeschlossen (TL-030). Kept for reference only.              │
# │                                                                         │
# │  SSOT: data/paper-references/PAP-*.yaml + bibliography/bcm_master.bib │
# │  Neue Papers: /integrate-paper Workflow                                │
# └─────────────────────────────────────────────────────────────────────────┘
"""
fix_bib_quality.py — Fix data quality issues in bcm_master.bib
for the 47 entries auto-imported from extracted_papers.yaml.

⚠️  DEPRECATED — Migration complete (TL-030, 2026-02-08).

Fixes:
1. Convert @article → @book for 19 entries that are books (not journal articles)
2. Add missing journal names for well-known papers

Usage:
    python scripts/fix_bib_quality.py --dry-run   # Preview changes
    python scripts/fix_bib_quality.py              # Apply changes
"""

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
BIB_PATH = ROOT / "bibliography" / "bcm_master.bib"

# ──────────────────────────────────────────────────────────────
# 19 entries that should be @book, not @article
# journal field contains the book title
# ──────────────────────────────────────────────────────────────
BOOKS = {
    "bateson1972steps": "Chandler Publishing",
    "bohr1934atomic": "Cambridge University Press",
    "cuvier1812recherches": "Deterville",
    "dear2006intelligibility": "University of Chicago Press",
    "duhem1906la": "Chevalier et Rivière",
    "galison1997image": "University of Chicago Press",
    "grabisch2016set": "Springer",
    "granet1934la": "La Renaissance du Livre",
    "hacking1983representing": "Cambridge University Press",
    "jammer1974philosophy": "Wiley",
    "lakatos1978methodology": "Cambridge University Press",
    "leontief1941structure": "Harvard University Press",
    "loreau2010populations": "Princeton University Press",
    "luhmann1984soziale": "Suhrkamp",
    "murdoch1987niels": "Cambridge University Press",
    "newton1687philosophiae": "Royal Society",
    "sandel2012what": "Farrar, Straus and Giroux",
    "satz2010why": "Oxford University Press",
    "wiener1948cybernetics": "MIT Press",
}

# ──────────────────────────────────────────────────────────────
# Journal names for well-known papers (high confidence)
# ──────────────────────────────────────────────────────────────
JOURNALS = {
    "amir2005supermodularity": "Journal of Mathematical Economics",
    "arora1996testing": "RAND Journal of Economics",
    "athey2002monotone": "Econometrica",
    "bohr1928quantum": "Nature",
    "breakspear2017dynamic": "Nature Neuroscience",
    "cassiman2006search": "Management Science",
    "denrell2003vicarious": "Organization Science",
    "foucquier2015analysis": "Pharmacology and Therapeutics",
    "grabisch1999axiomatic": "International Journal of Game Theory",
    "heisenberg1927ber": "Zeitschrift f{\\\"u}r Physik",
    "leiponen2005organization": "Management Science",
    "loewe1953problem": "Science",
    "loreau2001partitioning": "American Naturalist",
    "naeem2002ecosystem": "Nature",
    "rudin2019stop": "Nature Machine Intelligence",
    "sporns2011human": "Nature Reviews Neuroscience",
}


def main():
    parser = argparse.ArgumentParser(description="Fix BIB data quality issues")
    parser.add_argument("--dry-run", action="store_true", help="Preview only")
    args = parser.parse_args()

    lines = BIB_PATH.read_text(encoding="utf-8").splitlines(keepends=True)

    books_fixed = 0
    journals_added = 0
    changes = []
    current_key = None
    output_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Detect entry start: @article{key, or @book{key,
        entry_match = re.match(r'^@(\w+)\{([^,]+),', line)
        if entry_match:
            current_key = entry_match.group(2).strip()

        # Fix 1: Convert @article → @book
        if current_key in BOOKS and re.match(r'^@article\{', line):
            line = re.sub(r'^@article\{', '@book{', line)
            books_fixed += 1
            changes.append(("book", current_key, BOOKS[current_key]))

        # Fix 1b: For books, replace journal= with publisher=
        if current_key in BOOKS and re.match(r'\s*journal\s*=\s*\{', line):
            publisher = BOOKS[current_key]
            line = re.sub(
                r'(\s*)journal(\s*=\s*)\{[^}]*\}',
                rf'\1publisher\2{{{publisher}}}',
                line
            )

        # Fix 2: Add journal after year= for articles missing it
        if current_key in JOURNALS and re.match(r'\s*year\s*=\s*\{', line):
            # Check if journal already exists in this entry
            has_journal = False
            for j in range(i + 1, min(i + 20, len(lines))):
                if re.match(r'\s*journal\s*=', lines[j]):
                    has_journal = True
                    break
                if re.match(r'^@', lines[j]):
                    break
            if not has_journal:
                journal = JOURNALS[current_key]
                # Add journal line after year line
                output_lines.append(line)
                indent = re.match(r'(\s*)', line).group(1)
                output_lines.append(f"{indent}journal = {{{journal}}},\n")
                journals_added += 1
                changes.append(("journal", current_key, journal))
                i += 1
                continue

        output_lines.append(line)
        i += 1

    # Report
    prefix = "[DRY RUN] " if args.dry_run else ""
    print(f"{prefix}Results:")
    print(f"  Books fixed (@article → @book):  {books_fixed}")
    print(f"  Journals added:                   {journals_added}")
    print(f"  Total changes:                    {books_fixed + journals_added}")

    if changes:
        print(f"\nChanges:")
        for change_type, key, value in changes:
            if change_type == "book":
                print(f"  📖 {key}: @article → @book (publisher: {value})")
            else:
                print(f"  📰 {key}: + journal = {{{value}}}")

    # Count remaining missing journals
    content = "".join(output_lines)
    remaining = []
    for m in re.finditer(r'^@article\{([^,]+),', content, re.MULTILINE):
        key = m.group(1).strip()
        # Get the entry text until next @
        start = m.start()
        next_entry = re.search(r'\n@', content[start + 1:])
        end = start + 1 + next_entry.start() if next_entry else len(content)
        entry = content[start:end]
        if "Auto-imported" in entry and "journal" not in entry.split("notes")[0]:
            remaining.append(key)

    if remaining:
        print(f"\n⚠️  Still missing journal ({len(remaining)} entries):")
        for key in remaining:
            print(f"  → {key}")
        print(f"\n  These need DOI lookup via GitHub Actions workflow.")

    # Write back
    if not args.dry_run and (books_fixed > 0 or journals_added > 0):
        BIB_PATH.write_text("".join(output_lines), encoding="utf-8")
        print(f"\n✅ Updated {BIB_PATH}")


if __name__ == "__main__":
    main()
