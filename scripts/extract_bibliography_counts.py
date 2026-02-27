#!/usr/bin/env python3
"""
Extract Bibliography Reference Counts
======================================
Extracts the number of references listed in each paper's bibliography
and stores it as `bibliography_reference_count` in the YAML database.

This is DIFFERENT from:
  - reference_count: how many times THIS paper is referenced by others in EBF
  - ebf_reference_count: EBF-internal reference count

bibliography_reference_count = how many papers THIS paper CITES in its own bibliography.

Usage:
  python scripts/extract_bibliography_counts.py           # Report only
  python scripts/extract_bibliography_counts.py --fix     # Update YAML files
  python scripts/extract_bibliography_counts.py --verbose # Detailed output
"""

import os
import re
import sys
import yaml
import argparse
from pathlib import Path
from collections import Counter

TEXTS_DIR = Path("data/paper-texts")
YAML_DIR = Path("data/paper-references")

# Section heading patterns that indicate start of references
REF_START_PATTERNS = [
    r'^#{1,3}\s*References?\s*$',
    r'^#{1,3}\s*Bibliography\s*$',
    r'^#{1,3}\s*Works?\s+Cited\s*$',
    r'^#{1,3}\s*Literature\s*$',
    r'^#{1,3}\s*Cited\s+Works?\s*$',
    r'^#{1,3}\s*Literaturverzeichnis\s*$',
    r'^#{1,3}\s*Quellenverzeichnis\s*$',
    r'^\*\*References?\*\*\s*$',
    r'^References?\s*$',  # Plain text heading
    r'^REFERENCES?\s*$',  # All caps heading
    r'^BIBLIOGRAPHY\s*$',
]

# Patterns for notes/endnotes sections (books often use these)
NOTES_PATTERNS = [
    r'^#{1,3}\s*Notes?\s*$',
    r'^#{1,3}\s*Endnotes?\s*$',
    r'^#{1,3}\s*Footnotes?\s*$',
    r'^NOTES?\s*$',
    r'^Notes\s+to\s+Chapter',
    r'^[A-Z]?\s*Anmerkungen\s*$',  # German: "F Anmerkungen" or "Anmerkungen"
]

# Section heading patterns that indicate end of references
NEXT_SECTION_PATTERNS = [
    r'^#{1,3}\s+(?!References|Bibliography|Works|Literature|Cited|Notes|Endnotes|Chapter\s+\d)',
    r'^#{1,2}\s+(?:Appendix|Index|Acknowledgments?|About\s+the|Glossary|Abstract)',
    r'^APPENDIX',
    r'^INDEX\b',
    r'^ACKNOWLEDGMENTS',
    r'^ABOUT\s+THE',
]


def find_references_section(text):
    """Find the start of the references/bibliography section."""
    lines = text.split('\n')

    for i, line in enumerate(lines):
        stripped = line.strip()
        for pattern in REF_START_PATTERNS:
            if re.match(pattern, stripped, re.IGNORECASE):
                return i, 'references'

    # Also check for Notes sections (common in books)
    for i, line in enumerate(lines):
        stripped = line.strip()
        for pattern in NOTES_PATTERNS:
            if re.match(pattern, stripped, re.IGNORECASE):
                return i, 'notes'

    return None, None


def count_references_in_section(text, start_line):
    """Count individual reference entries from the start line."""
    lines = text.split('\n')
    ref_lines = lines[start_line + 1:]  # Skip the heading itself

    ref_count = 0
    in_references = True

    for line in ref_lines:
        stripped = line.strip()

        if not stripped:
            continue

        # Check if we've hit the next section
        for pattern in NEXT_SECTION_PATTERNS:
            if re.match(pattern, stripped, re.IGNORECASE):
                in_references = False
                break

        if not in_references:
            break

        # Skip sub-headings within notes (### Chapter 1, etc.)
        if re.match(r'^#{1,4}\s', stripped):
            continue

        # Count reference entries using multiple heuristics
        # Pattern 1: Bullet points (- Author...)
        if re.match(r'^[-•*]\s+\S', stripped):
            ref_count += 1
            continue

        # Pattern 2: Numbered references (1. Author... or [1] Author... or (1) Author...)
        if re.match(r'^(\d+[\.\)]\s|\[\d+\]\s|\(\d+\)\s)', stripped):
            ref_count += 1
            continue

        # Pattern 3: Author-year style (Lastname, F. (YYYY))
        if re.match(r'^[A-Z][a-zà-ü]+,?\s.*\(?(19|20)\d{2}', stripped):
            ref_count += 1
            continue

        # Pattern 4: Author et al style
        if re.match(r'^[A-Z][a-zà-ü]+\s+et\s+al', stripped):
            ref_count += 1
            continue

        # Pattern 5: Quoted title style ("Title" or 'Title')
        if re.match(r'^["\'"][A-Z]', stripped) and ('19' in stripped or '20' in stripped):
            ref_count += 1
            continue

        # Pattern 6: "For ... see Author" or "See Author" in notes
        if re.match(r'^(For\s|See\s)', stripped) and re.search(r'[A-Z][a-z]+,?\s', stripped):
            ref_count += 1
            continue

    return ref_count


def count_inline_citations(text):
    """Count unique inline citations for papers without a References section.

    Looks for patterns like:
    - (Author, YYYY)
    - (Author et al., YYYY)
    - Author (YYYY)
    - [N] style citations
    """
    # APA/Harvard style: (Author, YYYY) or (Author YYYY)
    apa_refs = set()
    for match in re.finditer(r'\(([A-Z][a-zà-ü]+(?:\s+(?:et\s+al\.?|and\s+[A-Z][a-zà-ü]+))?),?\s*((?:19|20)\d{2})\)', text):
        apa_refs.add(f"{match.group(1)}-{match.group(2)}")

    # Author (YYYY) style
    for match in re.finditer(r'([A-Z][a-zà-ü]+(?:\s+(?:et\s+al\.?|and\s+[A-Z][a-zà-ü]+))?)\s+\(((?:19|20)\d{2})\)', text):
        apa_refs.add(f"{match.group(1)}-{match.group(2)}")

    # Numbered citations [N] - ignore numbers > 500 (likely years or page numbers)
    numbered_refs = set()
    for match in re.finditer(r'\[(\d+)\]', text):
        num = int(match.group(1))
        if num <= 500:  # Real citation numbers are rarely > 500
            numbered_refs.add(num)

    if numbered_refs and max(numbered_refs) > len(apa_refs):
        return max(numbered_refs)  # Highest number is approximately total refs

    return len(apa_refs)


def analyze_paper(filepath):
    """Analyze a paper's full text for reference count."""
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        text = f.read()

    words = len(text.split())
    lines = text.count('\n') + 1

    # Try to find a formal References section
    ref_start, section_type = find_references_section(text)

    if ref_start is not None:
        ref_count = count_references_in_section(text, ref_start)
        method = f'section_{section_type}'
    else:
        # Fall back to counting inline citations
        ref_count = count_inline_citations(text)
        method = 'inline_citations'

    return {
        'file': filepath.name,
        'key': filepath.stem.replace('PAP-', ''),
        'words': words,
        'lines': lines,
        'ref_count': ref_count,
        'method': method,
        'has_formal_refs': ref_start is not None,
    }


def update_yaml(key, ref_count, method):
    """Update YAML file with bibliography_reference_count."""
    yaml_path = YAML_DIR / f"PAP-{key}.yaml"
    if not yaml_path.exists():
        return False

    try:
        with open(yaml_path) as f:
            data = yaml.safe_load(f)

        if not data:
            return False

        if 'full_text' not in data:
            data['full_text'] = {}

        data['full_text']['bibliography_reference_count'] = ref_count
        data['full_text']['bibliography_count_method'] = method

        with open(yaml_path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

        return True
    except Exception as e:
        print(f"  ERROR updating {yaml_path}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='Extract bibliography reference counts')
    parser.add_argument('--fix', action='store_true', help='Update YAML files with counts')
    parser.add_argument('--verbose', '-v', action='store_true', help='Detailed output')
    args = parser.parse_args()

    print("=" * 70)
    print("BIBLIOGRAPHY REFERENCE COUNT EXTRACTION")
    print("=" * 70)
    print()
    print("Field: full_text.bibliography_reference_count")
    print("  = Number of references listed in the paper's OWN bibliography")
    print("  (NOT how many times the paper is cited by others)")
    print()

    md_files = sorted(TEXTS_DIR.glob("PAP-*.md"))
    print(f"Found {len(md_files)} full-text files")
    print()

    results = []
    updated = 0

    for md_file in md_files:
        info = analyze_paper(md_file)
        results.append(info)

        if args.verbose:
            marker = "REFS" if info['has_formal_refs'] else "inln"
            print(f"  [{marker}] {info['file']:<50} {info['words']:>6}w  "
                  f"{info['ref_count']:>4} refs  ({info['method']})")

        if args.fix and info['ref_count'] > 0:
            if update_yaml(info['key'], info['ref_count'], info['method']):
                updated += 1

    # Summary
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print()

    with_refs = [r for r in results if r['ref_count'] > 0]
    without_refs = [r for r in results if r['ref_count'] == 0]
    formal_refs = [r for r in results if r['has_formal_refs']]
    inline_refs = [r for r in with_refs if not r['has_formal_refs']]

    print(f"Papers with references found:    {len(with_refs):>3} / {len(results)}")
    print(f"  - Formal References section:   {len(formal_refs):>3}")
    print(f"  - Inline citations only:       {len(inline_refs):>3}")
    print(f"Papers with no references:       {len(without_refs):>3}")
    print()

    if with_refs:
        counts = [r['ref_count'] for r in with_refs]
        print(f"Reference count statistics (papers with refs):")
        print(f"  Min:     {min(counts):>4}")
        print(f"  Max:     {max(counts):>4}")
        print(f"  Mean:    {sum(counts)/len(counts):>7.1f}")
        print(f"  Median:  {sorted(counts)[len(counts)//2]:>4}")
        print()

    # Top 15 by reference count
    top = sorted(results, key=lambda x: x['ref_count'], reverse=True)[:15]
    print("Top 15 papers by bibliography reference count:")
    print(f"  {'Paper':<50} {'Words':>6}  {'Refs':>4}  {'Method'}")
    print(f"  {'-'*50} {'-'*6}  {'-'*4}  {'-'*20}")
    for r in top:
        print(f"  {r['key']:<50} {r['words']:>6}  {r['ref_count']:>4}  {r['method']}")

    if args.fix:
        print()
        print(f"UPDATED: {updated} YAML files with bibliography_reference_count")
    elif with_refs:
        print()
        print(f"Run with --fix to update {len(with_refs)} YAML files")

    return 0


if __name__ == "__main__":
    sys.exit(main())
