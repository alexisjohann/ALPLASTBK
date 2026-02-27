#!/usr/bin/env python3
"""
Split a full JEP issue PDF (extracted as Markdown) into individual papers.
Matches papers against existing BibTeX entries or creates new ones.

Usage:
    python scripts/split_jep_issue.py data/paper-texts/PAP-jep-gdrive-1.md
"""

import re
import sys
from datetime import datetime
from pathlib import Path

TEXTS_DIR = Path("data/paper-texts")


def parse_toc(lines: list[str]) -> list[dict]:
    """Parse the Table of Contents to extract paper metadata."""
    papers = []
    toc_started = False

    for i, line in enumerate(lines):
        if "Contents" in line and "Volume 40" in lines[i+1] if i+1 < len(lines) else False:
            toc_started = True
            continue
        if not toc_started:
            # Check for Volume line on same line
            if "Contents" in line:
                toc_started = True
                continue
            continue

        # TOC ends at "Statement of Purpose" or similar
        if "Statement of Purpose" in line:
            break
        if "Advisory Board" in line:
            break

    return papers


def find_paper_boundaries(text: str) -> list[dict]:
    """Find paper boundaries using the JEP header pattern."""
    pattern = r"Journal of Economic Perspectives—Volume (\d+), Number (\d+)—(\w+ \d{4})—Pages (\d+)–(\d+)"

    papers = []
    for m in re.finditer(pattern, text):
        papers.append({
            "volume": int(m.group(1)),
            "number": int(m.group(2)),
            "season_year": m.group(3),
            "page_start": int(m.group(4)),
            "page_end": int(m.group(5)),
            "char_start": m.start(),
            "char_end": m.end(),
        })

    return papers


def extract_paper_text(full_text: str, start: int, next_start: int | None) -> str:
    """Extract paper text between boundaries."""
    if next_start:
        text = full_text[start:next_start]
    else:
        text = full_text[start:]
    return text.strip()


def guess_title_and_authors(paper_text: str, toc_entries: list[dict], page_start: int) -> tuple[str, str]:
    """Try to identify title and authors from paper text and TOC."""
    # Match by page number against TOC
    for entry in toc_entries:
        if entry.get("page_start") == page_start:
            return entry.get("title", ""), entry.get("authors", "")
    return "", ""


def clean_paper_text(text: str) -> str:
    """Clean up PDF extraction artifacts."""
    # Remove the JEP header line
    text = re.sub(
        r"Journal of Economic Perspectives—Volume \d+, Number \d+—\w+ \d{4}—Pages \d+–\d+\n?",
        "", text, count=1
    )
    # Fix split drop-cap (e.g., "F\nertility" -> "Fertility")
    text = re.sub(r"^([A-Z])\n(\w)", r"\1\2", text)
    # Remove duplicate lines from PDF extraction
    lines = text.split("\n")
    cleaned = []
    for i, line in enumerate(lines):
        if i > 0 and line.strip() == lines[i-1].strip() and len(line.strip()) > 20:
            continue  # skip duplicate
        cleaned.append(line)
    return "\n".join(cleaned)


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/split_jep_issue.py <fulltext.md>")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"ERROR: {input_path} not found")
        sys.exit(1)

    print(f"Reading: {input_path}")
    full_text = input_path.read_text(encoding="utf-8")
    lines = full_text.split("\n")

    # Known TOC from JEP Vol 40, No 1, Winter 2026
    # (Hardcoded because PDF TOC parsing is fragile)
    toc = [
        {"title": "The Likelihood of Persistently Low Global Fertility",
         "authors": "Michael Geruso, Dean Spears",
         "page_start": 3, "page_end": 26},
        {"title": "How Much Would Continued Low Fertility Affect the US Standard of Living?",
         "authors": "David N. Weil",
         "page_start": 27, "page_end": 46},
        {"title": "Family Institutions and the Global Fertility Transition",
         "authors": "Paula E. Gobbi, Anne Hannusch, Pauline Rossi",
         "page_start": 47, "page_end": 70},
        {"title": "Global Labor Mobility between Shrinking and Growing Labor Forces",
         "authors": "Lant Pritchett",
         "page_start": 71, "page_end": 92},
        {"title": "Labor Market Power: From Micro Evidence to Macro Consequences",
         "authors": "David Berger, Kyle Herkenhoff, Simon Mongey",
         "page_start": 93, "page_end": 114},
        {"title": "Antitrust Enforcement in Labor Markets",
         "authors": "Elena Prager",
         "page_start": 115, "page_end": 138},
        {"title": "The Economics of Noncompete Clauses",
         "authors": "Evan Starr",
         "page_start": 139, "page_end": 166},
        {"title": "Occupational Licensing in the United States",
         "authors": "Janna E. Johnson",
         "page_start": 167, "page_end": 190},
        {"title": "Asian Immigration to the United States in Historical Perspective",
         "authors": "Hannah M. Postel",
         "page_start": 191, "page_end": 214},
        {"title": "From Asia, with Skills",
         "authors": "Gaurav Khanna",
         "page_start": 215, "page_end": 240},
        {"title": "Recommendations for Further Reading",
         "authors": "Timothy Taylor",
         "page_start": 241, "page_end": 248},
    ]

    # Find paper boundaries
    boundaries = find_paper_boundaries(full_text)
    print(f"Found {len(boundaries)} paper boundaries")

    if len(boundaries) != len(toc):
        print(f"WARNING: {len(boundaries)} boundaries but {len(toc)} TOC entries")

    # Match boundaries to TOC entries by page numbers
    TEXTS_DIR.mkdir(parents=True, exist_ok=True)
    results = []

    for i, boundary in enumerate(boundaries):
        # Find matching TOC entry
        toc_entry = None
        for t in toc:
            if t["page_start"] == boundary["page_start"]:
                toc_entry = t
                break

        if not toc_entry:
            print(f"  WARNING: No TOC match for pages {boundary['page_start']}–{boundary['page_end']}")
            toc_entry = {
                "title": f"Unknown Paper (Pages {boundary['page_start']}–{boundary['page_end']})",
                "authors": "",
                "page_start": boundary["page_start"],
                "page_end": boundary["page_end"],
            }

        # Extract text
        next_start = boundaries[i+1]["char_start"] if i+1 < len(boundaries) else None
        raw_text = extract_paper_text(full_text, boundary["char_start"], next_start)
        paper_text = clean_paper_text(raw_text)
        word_count = len(paper_text.split())

        # Generate key from first author's last name
        first_author = toc_entry["authors"].split(",")[0].strip()
        last_name = first_author.split()[-1].lower() if first_author else "unknown"
        # Create a short title word
        title_words = [w.lower() for w in toc_entry["title"].split()
                       if w.lower() not in {"the", "of", "in", "and", "a", "to", "from", "with", "how", "much", "would", "between"}]
        short_title = title_words[0] if title_words else "paper"
        key = f"{last_name}2026{short_title}"

        # Determine content level
        if word_count >= 5000:
            level = "L3"
        elif word_count >= 1000:
            level = "L2"
        else:
            level = "L1"

        # Save individual paper
        out_path = TEXTS_DIR / f"PAP-{key}.md"

        header = f"""---
# Full text extracted from JEP Vol 40 No 1 (Winter 2026)
# Source: Google Drive PDF → PyMuPDF extraction → split
# DOI: (pending - to be fetched via CrossRef)
# Fetched: {datetime.now().strftime('%Y-%m-%d %H:%M')}
# Word count: {word_count}
# Content level: {level}
# Pages: {boundary['page_start']}–{boundary['page_end']}
---

# {toc_entry['title']}

**Authors:** {toc_entry['authors']}

**Journal:** Journal of Economic Perspectives, Vol. 40, No. 1, Winter 2026, pp. {boundary['page_start']}–{boundary['page_end']}

"""

        out_path.write_text(header + paper_text, encoding="utf-8")

        print(f"  [{i+1}/{len(boundaries)}] {key}: {toc_entry['title'][:60]}...")
        print(f"           {word_count:,} words, {level}, saved to {out_path.name}")

        results.append({
            "key": key,
            "title": toc_entry["title"],
            "authors": toc_entry["authors"],
            "pages": f"{boundary['page_start']}–{boundary['page_end']}",
            "word_count": word_count,
            "content_level": level,
            "file": out_path.name,
        })

    # Generate BibTeX entries
    bib_entries = []
    for r in results:
        first_author = r["authors"].split(",")[0].strip().split()[-1].lower()
        title_word = [w.lower() for w in r["title"].split()
                      if w.lower() not in {"the", "of", "in", "and", "a", "to", "from", "with", "how", "much", "would", "between"}][0]
        bib_key = f"{first_author}2026{title_word}"
        pages = r["pages"]

        bib = f"""@article{{{bib_key},
  title = {{{r['title']}}},
  author = {{{r['authors']}}},
  year = {{2026}},
  journal = {{Journal of Economic Perspectives}},
  volume = {{40}},
  number = {{1}},
  pages = {{{pages}}},
  use_for = {{LIT-O}},
  evidence_tier = {{1}},
}}
"""
        bib_entries.append(bib)

    # Save BibTeX
    bib_path = Path("data/jep_vol40_no1_bibtex.bib")
    bib_path.write_text("\n".join(bib_entries), encoding="utf-8")
    print(f"\nBibTeX entries saved to: {bib_path}")

    # Summary
    print(f"\n{'='*60}")
    print(f"  SUMMARY")
    print(f"{'='*60}")
    print(f"  Papers split:    {len(results)}")
    print(f"  L3 (full text):  {sum(1 for r in results if r['content_level'] == 'L3')}")
    print(f"  L2 (partial):    {sum(1 for r in results if r['content_level'] == 'L2')}")
    print(f"  Total words:     {sum(r['word_count'] for r in results):,}")
    print(f"  BibTeX entries:  {len(bib_entries)}")
    print(f"{'='*60}")

    for r in results:
        print(f"  {r['content_level']} | {r['word_count']:>6,}w | {r['title'][:55]}")


if __name__ == "__main__":
    main()
