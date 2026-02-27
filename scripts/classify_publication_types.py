#!/usr/bin/env python3
"""
Classify publication_type for all papers based on BibTeX entry types.

Maps BibTeX @types to YAML publication_type values:
  @article      → journal_article
  @book         → book
  @techreport   → working_paper
  @incollection → book_chapter
  @inproceedings → conference_paper
  @phdthesis    → dissertation
  @mastersthesis → dissertation
  @unpublished  → working_paper
  @misc         → report

SSOT for publication_type enum: data/paper-sources.schema.yaml (line 62-64)
"""

import re
import sys
from pathlib import Path

BIB_FILE = Path("bibliography/bcm_master.bib")
YAML_DIR = Path("data/paper-references")

# Mapping from BibTeX @type to YAML publication_type
BIBTEX_TO_YAML = {
    "article": "journal_article",
    "book": "book",
    "techreport": "working_paper",
    "incollection": "book_chapter",
    "inproceedings": "conference_paper",
    "conference": "conference_paper",
    "phdthesis": "dissertation",
    "mastersthesis": "dissertation",
    "unpublished": "working_paper",
    "misc": "report",
    "manual": "report",
    "booklet": "report",
}


def parse_bibtex_types():
    """Parse BibTeX file and extract entry types for each key."""
    types = {}

    with open(BIB_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Match @type{key, patterns
    pattern = r'@(\w+)\s*\{\s*([^,\s]+)\s*,'
    for match in re.finditer(pattern, content):
        entry_type = match.group(1).lower()
        key = match.group(2)

        # Store with original key
        types[key] = entry_type

        # Also store normalized versions for matching
        # Remove PAP- prefix and lowercase
        key_norm = key.replace('PAP-', '').lower()
        types[key_norm] = entry_type

        # Also store with PAP- prefix lowercase
        types[f"PAP-{key_norm}"] = entry_type

    return types


def normalize_key(key):
    """Normalize a key for matching."""
    return key.replace('PAP-', '').lower()


def get_papers_without_type():
    """Find YAML files without publication_type."""
    papers = []

    for yaml_file in YAML_DIR.glob("PAP-*.yaml"):
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check if publication_type already exists
            if 'publication_type:' not in content:
                # Extract the paper key (filename minus PAP- and .yaml)
                key = yaml_file.stem.replace('PAP-', '')
                papers.append({
                    'file': yaml_file,
                    'key': key
                })
        except Exception as e:
            print(f"Error reading {yaml_file}: {e}")

    return papers


def add_publication_type(yaml_file, pub_type):
    """Add publication_type to YAML file."""
    try:
        with open(yaml_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find a good insertion point (after year or doi)
        lines = content.split('\n')
        new_lines = []
        inserted = False

        for i, line in enumerate(lines):
            new_lines.append(line)

            # Insert after year, doi, or abstract_source line
            if not inserted and (
                line.startswith('year:') or
                line.startswith('doi:') or
                line.startswith('abstract_source:')
            ):
                # Check if next line is not already publication_type
                if i + 1 < len(lines) and not lines[i + 1].startswith('publication_type:'):
                    new_lines.append(f'publication_type: {pub_type}')
                    inserted = True

        # If not inserted yet, add before migration_status
        if not inserted:
            final_lines = []
            for line in new_lines:
                if line.startswith('migration_status:') and not inserted:
                    final_lines.append(f'publication_type: {pub_type}')
                    inserted = True
                final_lines.append(line)
            new_lines = final_lines

        # Write back
        with open(yaml_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))

        return True
    except Exception as e:
        print(f"Error updating {yaml_file}: {e}")
        return False


def main():
    print("=" * 60)
    print("PUBLICATION TYPE CLASSIFIER")
    print("=" * 60)
    print(f"\nBibTeX source: {BIB_FILE}")
    print(f"YAML directory: {YAML_DIR}")
    print(f"\nMapping (SSOT: data/paper-sources.schema.yaml):")
    for bib, yaml in sorted(BIBTEX_TO_YAML.items()):
        print(f"  @{bib:15} → {yaml}")

    # Parse BibTeX types
    print("\n" + "-" * 60)
    print("Parsing BibTeX file...")
    bib_types = parse_bibtex_types()
    print(f"Found {len(bib_types)} entries in BibTeX")

    # Count BibTeX types
    type_counts = {}
    for entry_type in bib_types.values():
        type_counts[entry_type] = type_counts.get(entry_type, 0) + 1
    print("\nBibTeX type distribution:")
    for t, c in sorted(type_counts.items(), key=lambda x: -x[1]):
        yaml_type = BIBTEX_TO_YAML.get(t, "UNKNOWN")
        print(f"  @{t:15}: {c:4} → {yaml_type}")

    # Get papers without publication_type
    print("\n" + "-" * 60)
    print("Finding YAML files without publication_type...")
    papers = get_papers_without_type()
    print(f"Found {len(papers)} papers without publication_type")

    if not papers:
        print("\nAll papers already have publication_type! Nothing to do.")
        return

    # Classify papers
    print("\n" + "-" * 60)
    print("Classifying papers...")

    stats = {
        'updated': 0,
        'not_in_bib': 0,
        'unknown_type': 0,
        'errors': 0
    }
    type_updates = {}

    for paper in papers:
        key = paper['key']
        yaml_file = paper['file']

        # Try multiple key formats
        key_norm = normalize_key(key)
        bib_type = None

        for try_key in [key, key_norm, f"PAP-{key_norm}", key.lower()]:
            if try_key in bib_types:
                bib_type = bib_types[try_key]
                break

        if bib_type is None:
            stats['not_in_bib'] += 1
            continue

        if bib_type not in BIBTEX_TO_YAML:
            print(f"  Unknown BibTeX type @{bib_type} for {key}")
            stats['unknown_type'] += 1
            continue

        pub_type = BIBTEX_TO_YAML[bib_type]

        if add_publication_type(yaml_file, pub_type):
            stats['updated'] += 1
            type_updates[pub_type] = type_updates.get(pub_type, 0) + 1
        else:
            stats['errors'] += 1

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"\nUpdated:           {stats['updated']}")
    print(f"Not in BibTeX:     {stats['not_in_bib']}")
    print(f"Unknown BibTeX type: {stats['unknown_type']}")
    print(f"Errors:            {stats['errors']}")

    if type_updates:
        print("\nUpdates by publication_type:")
        for pub_type, count in sorted(type_updates.items(), key=lambda x: -x[1]):
            print(f"  {pub_type:20}: {count}")

    print("\n✓ Classification complete!")


if __name__ == "__main__":
    main()
