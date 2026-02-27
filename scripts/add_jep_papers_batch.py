#!/usr/bin/env python3
"""
Batch-add JEP papers from a structured list.
Generates BibTeX entries and PAP-*.yaml files.

Usage:
  python scripts/add_jep_papers_batch.py --input data/journals/jep/import-batch.yaml
  python scripts/add_jep_papers_batch.py --input data/journals/jep/import-batch.yaml --dry-run
"""

import argparse
import os
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("pip install pyyaml")
    sys.exit(1)

REPO_ROOT = Path(__file__).parent.parent
BIB_FILE = REPO_ROOT / "bibliography" / "bcm_master.bib"
PAPER_REF_DIR = REPO_ROOT / "data" / "paper-references"


def generate_bibtex(paper: dict) -> str:
    """Generate a single BibTeX entry."""
    key = paper["bibtex_key"]
    authors_bib = " and ".join(paper["authors_bib"])
    pages = paper.get("pages", "").replace("-", "--")

    lines = [f"@article{{{key},"]
    lines.append(f"  title = {{{paper['title']}}},")
    lines.append(f"  author = {{{authors_bib}}},")
    lines.append(f"  year = {{{paper['year']}}},")
    lines.append(f"  journal = {{Journal of Economic Perspectives}},")
    lines.append(f"  volume = {{{paper['volume']}}},")
    lines.append(f"  number = {{{paper['issue']}}},")
    if pages:
        lines.append(f"  pages = {{{pages}}},")
    lines.append(f"  doi = {{{paper['doi']}}},")
    use_for = ", ".join(paper.get("use_for", ["LIT-O"]))
    lines.append(f"  use_for = {{{use_for}}},")
    lines.append(f"  evidence_tier = {{1}},")
    lines.append("}")
    return "\n".join(lines)


def generate_yaml(paper: dict) -> dict:
    """Generate PAP-*.yaml content."""
    key = paper["bibtex_key"]
    return {
        "paper_id": f"PAP-{key}",
        "bibtex_key": key,
        "title": paper["title"],
        "authors": [{"name": n} for n in paper["authors"]],
        "year": paper["year"],
        "journal": "Journal of Economic Perspectives",
        "volume": paper["volume"],
        "issue": paper["issue"],
        "pages": paper.get("pages", ""),
        "doi": paper["doi"],
        "url": f"https://doi.org/{paper['doi']}",
        "content_level": "L1",
        "integration_level": "I1",
        "evidence_tier": 1,
        "use_for": paper.get("use_for", ["LIT-O"]),
        "status": "cataloged",
        "source": "jep_catalog_batch",
        "cataloged_date": paper.get("cataloged_date", "2026-02-18"),
    }


def main():
    parser = argparse.ArgumentParser(description="Batch-add JEP papers")
    parser.add_argument("--input", required=True, help="YAML file with paper list")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be created")
    args = parser.parse_args()

    with open(args.input) as f:
        data = yaml.safe_load(f)

    papers = data.get("papers", [])
    print(f"Found {len(papers)} papers in {args.input}")

    bib_entries = []
    yaml_count = 0
    skipped = 0

    for p in papers:
        key = p["bibtex_key"]

        # Generate BibTeX
        bib = generate_bibtex(p)
        bib_entries.append(bib)

        # Generate YAML
        yaml_path = PAPER_REF_DIR / f"PAP-{key}.yaml"
        if yaml_path.exists():
            print(f"  SKIP (exists): {yaml_path.name}")
            skipped += 1
            continue

        yaml_content = generate_yaml(p)

        if args.dry_run:
            print(f"  WOULD CREATE: {yaml_path.name}")
            print(f"    Title: {p['title'][:60]}...")
        else:
            with open(yaml_path, "w") as f:
                yaml.dump(yaml_content, f, default_flow_style=False,
                          allow_unicode=True, sort_keys=False, width=120)
            print(f"  CREATED: {yaml_path.name}")
        yaml_count += 1

    # Append BibTeX entries
    if bib_entries and not args.dry_run:
        # Read existing bib to check for duplicates
        existing = BIB_FILE.read_text()
        new_entries = []
        for entry in bib_entries:
            key = entry.split("{")[1].split(",")[0]
            if key not in existing:
                new_entries.append(entry)
            else:
                print(f"  BIB SKIP (exists): {key}")

        if new_entries:
            with open(BIB_FILE, "a") as f:
                f.write("\n% === JEP Batch Import ===\n")
                f.write("\n".join(new_entries))
                f.write("\n")
            print(f"\n  Appended {len(new_entries)} BibTeX entries to {BIB_FILE.name}")

    print(f"\nDone: {yaml_count} YAMLs, {len(bib_entries)} BibTeX, {skipped} skipped")


if __name__ == "__main__":
    main()
