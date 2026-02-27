#!/usr/bin/env python3
# ┌─────────────────────────────────────────────────────────────────────────┐
# │  ⚠️  DEPRECATED (2026-02-08)                                            │
# │                                                                         │
# │  Einmaliges Migrations-Script: 47 Papers aus extracted_papers.yaml     │
# │  in BIB + PAP-*.yaml integriert. Arbeit abgeschlossen (TL-028).       │
# │  Kept for reference only.                                              │
# │                                                                         │
# │  SSOT: data/paper-references/PAP-*.yaml + bibliography/bcm_master.bib │
# │  Neue Papers: /integrate-paper Workflow                                │
# └─────────────────────────────────────────────────────────────────────────┘
"""
integrate_extracted_papers.py — Batch-integrate papers from extracted_papers.yaml into SSOT.

⚠️  DEPRECATED — Migration complete (TL-028, 2026-02-08).

EXPERIMENTAL MODE: Run with --batch N to process N papers at a time.
Workflow: 1 → 10 → 100 → all

For each paper in extracted_papers.yaml that is NOT yet in bcm_master.bib:
1. Check if paper already exists under a different BIB key (author+year fuzzy match)
2. If new: create BIB entry + PAP-*.yaml (L1 minimal)
3. If duplicate: log the match

Usage:
    python scripts/integrate_extracted_papers.py --dry-run          # Preview only
    python scripts/integrate_extracted_papers.py --batch 1          # Process 1
    python scripts/integrate_extracted_papers.py --batch 10         # Process 10
    python scripts/integrate_extracted_papers.py --batch 100        # Process 100
    python scripts/integrate_extracted_papers.py                    # Process all
    python scripts/integrate_extracted_papers.py --status           # Show stats
"""

import argparse
import os
import re
import sys
import yaml
from datetime import date
from pathlib import Path
from collections import defaultdict

# Paths
ROOT = Path(__file__).parent.parent
BIB_PATH = ROOT / "bibliography" / "bcm_master.bib"
EXTRACTED_PATH = ROOT / "data" / "extracted_papers.yaml"
PAPER_REFS_DIR = ROOT / "data" / "paper-references"
TODAY = date.today().isoformat()

# LIT-appendix code → use_for mapping
LIT_MAPPING = {
    "L": "LIT-ACEMOGLU",
    "Z": "LIT-AGHION",
    "K": "LIT-FEHR",
    "GN": "LIT-GNEEZY",
    "MN": "LIT-NIEDERLE",
    "PA": "LIT-AGHION",
    "AA": "LIT-GNEEZY",
}


def load_bib_keys_and_authors(bib_path):
    """Parse BIB file to get all keys and author+year combos for duplicate detection."""
    keys = set()
    author_year = {}  # (normalized_surname, year) → bib_key

    current_key = None
    current_author = None
    current_year = None

    with open(bib_path, "r", encoding="utf-8") as f:
        for line in f:
            # Match BIB entry start
            m = re.match(r"@\w+\{([^,]+),", line)
            if m:
                # Save previous entry
                if current_key and current_author and current_year:
                    for surname in current_author:
                        author_year[(surname.lower(), current_year)] = current_key
                current_key = m.group(1).strip()
                keys.add(current_key)
                current_author = []
                current_year = None
                continue

            if current_key:
                # Match author field
                am = re.match(r"\s*author\s*=\s*\{(.+?)(?:\}|$)", line)
                if am:
                    author_str = am.group(1)
                    # Extract surnames: "Fehr, Ernst and Schmidt, Klaus" → ["fehr", "schmidt"]
                    # Also handle: "Ernst Fehr and Klaus Schmidt" → ["fehr", "schmidt"]
                    parts = re.split(r"\s+and\s+", author_str)
                    for part in parts:
                        part = part.strip()
                        if "," in part:
                            # "Lastname, Firstname" format
                            surname = part.split(",")[0].strip()
                        else:
                            # "Firstname Lastname" format — take last word
                            words = part.split()
                            surname = words[-1] if words else part
                        if surname:
                            current_author.append(surname)

                # Match year field
                ym = re.match(r"\s*year\s*=\s*\{?(\d{4})", line)
                if ym:
                    current_year = ym.group(1)

    # Save last entry
    if current_key and current_author and current_year:
        for surname in current_author:
            author_year[(surname.lower(), current_year)] = current_key

    return keys, author_year


def load_existing_yamls():
    """Get set of existing PAP-*.yaml keys."""
    existing = set()
    for f in PAPER_REFS_DIR.glob("PAP-*.yaml"):
        key = f.stem.replace("PAP-", "")
        existing.add(key)
    return existing


def normalize_id(paper_id):
    """Normalize extracted paper ID to BIB key format."""
    # Already in good format: authorYYYY or authorYYYY_suffix
    return paper_id


def find_duplicate(paper, bib_keys, author_year_map):
    """Check if paper already exists in BIB under a different key."""
    pid = paper["id"]

    # Direct match
    if pid in bib_keys:
        return pid, "exact"

    # PAP- prefixed match
    if f"PAP-{pid}" in bib_keys:
        return f"PAP-{pid}", "pap_prefix"

    # Author+year match
    if paper.get("authors"):
        first_author = paper["authors"][0]
        surname = first_author.split(",")[0].strip().split(".")[-1].strip()
        year_str = str(paper.get("year", ""))
        key = (surname.lower(), year_str)
        if key in author_year_map:
            return author_year_map[key], "author_year"

    return None, None


def generate_bib_key(paper):
    """Generate a proper BIB key from paper metadata."""
    authors = paper.get("authors", [])
    year = paper.get("year", "")

    if authors:
        first_author = authors[0]
        # Extract surname: "Acemoglu, D." → "acemoglu"
        surname = first_author.split(",")[0].strip().lower()
        # Remove non-alpha
        surname = re.sub(r"[^a-z]", "", surname)
    else:
        surname = "unknown"

    # Create short title word
    title = paper.get("title", "")
    title_words = re.findall(r"[A-Za-z]+", title)
    # Skip common words
    skip = {"the", "a", "an", "of", "in", "on", "for", "and", "to", "with", "from", "by"}
    title_word = ""
    for w in title_words:
        if w.lower() not in skip:
            title_word = w.lower()
            break

    return f"{surname}{year}{title_word}"


def make_bib_entry(paper, bib_key):
    """Generate BibTeX entry string."""
    authors = paper.get("authors", [])
    author_str = " and ".join(authors)
    year = paper.get("year", "")
    title = paper.get("title", "")
    journal = paper.get("journal", "")

    # Determine use_for from lit_appendix
    lit_code = paper.get("lit_appendix", "")
    lit_use = LIT_MAPPING.get(lit_code, "LIT-O")
    use_for = f"{{{lit_use}}}"

    lines = [
        f"@article{{{bib_key},",
        f"  title={{{title}}},",
        f"  author={{{author_str}}},",
        f"  year={{{year}}},",
    ]
    if journal:
        lines.append(f"  journal={{{journal}}},")

    lines.extend([
        f"  evidence_tier = {{3}},",
        f"  integration_level = {{1}},",
        f"  use_for = {use_for},",
        f"  theory_support = {{}},",
        f"  parameter = {{}},",
        f"  identification = {{}},",
        f"  external_validity = {{}},",
        f"  session_ref = {{}},",
        f"  notes = {{Auto-imported from extracted_papers.yaml ({paper.get('extraction_source', 'unknown')})}},",
        f"  keywords = {{}}",
        f"}}",
    ])
    return "\n".join(lines)


def make_yaml_entry(paper, bib_key):
    """Generate PAP-*.yaml content."""
    authors = paper.get("authors", [])
    author_str = " and ".join(authors)
    year = str(paper.get("year", ""))
    title = paper.get("title", "")
    lit_code = paper.get("lit_appendix", "")
    lit_use = LIT_MAPPING.get(lit_code, "LIT-O")
    extraction_source = paper.get("extraction_source", "")

    data = {
        "paper": bib_key,
        "superkey": f"PAP-{bib_key}",
        "title": title,
        "author": author_str,
        "year": year,
        "publication_type": "journal_article",
        "journal": paper.get("journal"),
        "doi": None,
        "url": None,
        "citations": None,
        "status": "published",
        "content_level": "L1",
        "integration_level": 1,
        "ebf_integration": {
            "evidence_tier": 3,
            "use_for": [lit_use],
            "theory_support": [],
        },
        "summary": {
            "abstract": f"Referenced in {extraction_source}. Full metadata pending.",
        },
        "key_findings_structured": [],
        "behavioral_mapping": {
            "dimensions": [],
        },
        "linked_cases": [],
        "full_text": {
            "available": False,
            "path": None,
        },
        "prior_score": {
            "prior_score": 0.05,
            "classification": "MINIMAL",
            "content_level": "L1",
            "integration_level": "I1",
            "confidence_multiplier": 0.60,
            "evidence_quality": 0.30,
            "computed_date": TODAY,
        },
        "ssot_migration_date": TODAY,
        "source": "extracted_papers.yaml",
        "extraction_source": extraction_source,
    }
    return yaml.dump(data, default_flow_style=False, allow_unicode=True, sort_keys=False)


def process_papers(papers, bib_keys, author_year_map, existing_yamls, batch=None, dry_run=False, skip_bad_titles=True):
    """Process papers: create BIB entries + YAML files."""
    new_bib_entries = []
    new_yamls = []
    duplicates = []
    skipped_yaml_exists = []
    skipped_bad_title = []

    to_process = papers[:batch] if batch else papers

    for paper in to_process:
        pid = paper["id"]

        # Check for duplicates
        dup_key, dup_type = find_duplicate(paper, bib_keys, author_year_map)
        if dup_key:
            duplicates.append({"id": pid, "existing_key": dup_key, "match_type": dup_type})
            continue

        # Skip papers with bad titles (single char, placeholder, etc.)
        title = paper.get("title", "")
        if skip_bad_titles and (len(title) <= 5 or "to be added" in title.lower()):
            skipped_bad_title.append({"id": pid, "title": title})
            continue

        # Generate BIB key
        bib_key = generate_bib_key(paper)

        # Avoid collision with existing keys
        base_key = bib_key
        suffix = 0
        while bib_key in bib_keys:
            suffix += 1
            bib_key = f"{base_key}_{suffix}"

        # Create BIB entry
        bib_entry = make_bib_entry(paper, bib_key)
        new_bib_entries.append({"key": bib_key, "entry": bib_entry, "paper": paper})
        bib_keys.add(bib_key)

        # Check if YAML already exists
        if bib_key in existing_yamls:
            skipped_yaml_exists.append(bib_key)
        else:
            yaml_content = make_yaml_entry(paper, bib_key)
            new_yamls.append({"key": bib_key, "content": yaml_content})

    return new_bib_entries, new_yamls, duplicates, skipped_yaml_exists, skipped_bad_title


def write_results(new_bib_entries, new_yamls, dry_run=False):
    """Write BIB entries and YAML files to disk."""
    if dry_run:
        return

    # Append BIB entries
    if new_bib_entries:
        with open(BIB_PATH, "a", encoding="utf-8") as f:
            f.write("\n")
            for entry in new_bib_entries:
                f.write(f"\n{entry['entry']}\n")

    # Write YAML files
    for yml in new_yamls:
        yaml_path = PAPER_REFS_DIR / f"PAP-{yml['key']}.yaml"
        with open(yaml_path, "w", encoding="utf-8") as f:
            f.write(yml["content"])


def show_status(papers, bib_keys, author_year_map, existing_yamls):
    """Show current integration status."""
    new = 0
    dup = 0
    for paper in papers:
        dup_key, _ = find_duplicate(paper, bib_keys, author_year_map)
        if dup_key:
            dup += 1
        else:
            new += 1

    print(f"extracted_papers.yaml: {len(papers)} papers")
    print(f"  Already in BIB (duplicates): {dup}")
    print(f"  New (need integration):      {new}")
    print(f"  Existing YAML files:         {len(existing_yamls)}")
    print(f"  BIB entries total:           {len(bib_keys)}")


def main():
    parser = argparse.ArgumentParser(description="Integrate extracted papers into SSOT")
    parser.add_argument("--batch", type=int, help="Process N papers (EXPERIMENTAL mode)")
    parser.add_argument("--dry-run", action="store_true", help="Preview only, don't write")
    parser.add_argument("--status", action="store_true", help="Show integration status")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    args = parser.parse_args()

    # Load data
    with open(EXTRACTED_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    papers = data["extracted_papers"]

    bib_keys, author_year_map = load_bib_keys_and_authors(BIB_PATH)
    existing_yamls = load_existing_yamls()

    if args.status:
        show_status(papers, bib_keys, author_year_map, existing_yamls)
        return

    # Process
    new_bib, new_yamls, duplicates, skipped, bad_titles = process_papers(
        papers, bib_keys, author_year_map, existing_yamls,
        batch=args.batch, dry_run=args.dry_run
    )

    # Report
    print(f"{'[DRY RUN] ' if args.dry_run else ''}Results:")
    print(f"  Processed:    {len(new_bib) + len(duplicates) + len(bad_titles)} papers")
    print(f"  New BIB+YAML: {len(new_bib)}")
    print(f"  Duplicates:   {len(duplicates)}")
    print(f"  Bad titles:   {len(bad_titles)}")
    if skipped:
        print(f"  YAML exists:  {len(skipped)}")

    if args.verbose or args.dry_run:
        if duplicates:
            print(f"\nDuplicates found:")
            for d in duplicates:
                print(f"  {d['id']} → {d['existing_key']} ({d['match_type']})")

        if bad_titles:
            print(f"\nSkipped (bad title):")
            for bt in bad_titles[:10]:
                print(f"  {bt['id']}: '{bt['title']}'")
            if len(bad_titles) > 10:
                print(f"  ... and {len(bad_titles) - 10} more")

        if new_bib:
            print(f"\nNew papers to add:")
            for entry in new_bib:
                p = entry["paper"]
                print(f"  {entry['key']}: {p.get('title', '?')[:70]}")

    # Write
    if not args.dry_run:
        write_results(new_bib, new_yamls)
        print(f"\nWritten: {len(new_bib)} BIB entries, {len(new_yamls)} YAML files")


if __name__ == "__main__":
    main()
