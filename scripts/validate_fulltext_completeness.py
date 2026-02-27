#!/usr/bin/env python3
"""
Validate Full-Text Completeness
================================
Checks whether papers in data/paper-texts/ are actually complete (L3)
or structured summaries (L2). Updates content_level in YAML accordingly.

Criteria for L3 (complete):
  R1: All sections from original paper present
  R2: Has References/Bibliography section with cited works
  R3: Minimum word count (>10,000 for articles, >5,000 for short papers)
  R4: No EBF-added sections (Key Parameters, EBF Framework Relevance)

Usage:
  python scripts/validate_fulltext_completeness.py           # Report only
  python scripts/validate_fulltext_completeness.py --fix     # Fix content_levels
  python scripts/validate_fulltext_completeness.py --verbose # Detailed output
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

# EBF-specific sections that indicate a summary, not original text
EBF_MARKERS = [
    "Key Parameters Extracted",
    "EBF Framework Relevance",
    "EBF Integration",
    "Parameters Contributed",
    "Axioms Established",
    "Cross-References",
    "Content Level:",
    "Evidence Tier:",
    "Full text archived for EBF",
]

# Reference section patterns (markdown headings AND plain-text headings)
REF_PATTERNS = [
    r'^#{1,3}\s*References\s*$',
    r'^#{1,3}\s*Bibliography\s*$',
    r'^#{1,3}\s*Works Cited\s*$',
    r'^#{1,3}\s*Literature\s*$',
    r'^#{1,3}\s*Cited Works\s*$',
    r'^References Cited\s*$',
    r'^References\s*$',
    r'^Bibliography\s*$',
    r'^Works Cited\s*$',
    r'^Literature Cited\s*$',
]


def count_words(text):
    """Count words in text."""
    return len(text.split())


def count_references(text):
    """Count approximate number of references in References section."""
    refs_start = None
    for pattern in REF_PATTERNS:
        match = re.search(pattern, text, re.MULTILINE | re.IGNORECASE)
        if match:
            refs_start = match.start()
            break

    if refs_start is None:
        return 0

    refs_text = text[refs_start:]
    # Count reference entries (lines starting with - or numbered or author names)
    ref_lines = 0
    for line in refs_text.split('\n'):
        line = line.strip()
        if not line:
            continue
        # Reference patterns
        if re.match(r'^[-•]\s', line):
            ref_lines += 1
        elif re.match(r'^\d+[\.\)]\s', line):
            ref_lines += 1
        elif re.match(r'^[A-Z][a-zà-ü]+,?\s', line) and ('(' in line or '19' in line or '20' in line):
            ref_lines += 1

    return ref_lines


def has_references_section(text):
    """Check if text has a formal References section."""
    for pattern in REF_PATTERNS:
        if re.search(pattern, text, re.MULTILINE | re.IGNORECASE):
            return True
    return False


def get_yaml_bib_count(key):
    """Get bibliography_reference_count from YAML (set by extract_bibliography_counts.py).

    This captures references detected via multiple methods:
    - section_references: formal ## References heading
    - section_notes: ## Notes/Endnotes sections with citations
    - inline_citations: Author (Year) patterns in text
    """
    yaml_path = YAML_DIR / f"PAP-{key}.yaml"
    if not yaml_path.exists():
        return 0
    try:
        with open(yaml_path) as f:
            data = yaml.safe_load(f)
        if data:
            # Check top-level first (preferred location)
            top_count = data.get('bibliography_reference_count', 0) or 0
            if top_count > 0:
                return top_count
            # Fallback: check inside full_text block
            if 'full_text' in data:
                return data['full_text'].get('bibliography_reference_count', 0) or 0
        return 0
    except Exception:
        return 0


def has_ebf_markers(text):
    """Check if text contains EBF-specific sections (indicating summary)."""
    found = []
    for marker in EBF_MARKERS:
        if marker.lower() in text.lower():
            found.append(marker)
    return found


def classify_paper(filepath):
    """Classify a paper's completeness level.

    L3 criteria (ALL must be met):
      R1: Substantial content (>10K words)
      R2: Has references (formal section OR bibliography_reference_count >= 10 in YAML)
      R3: Word count threshold (>10K for full papers)
      R4: No EBF markers in text (separation of concerns)
    """
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        text = f.read()

    key = filepath.stem.replace('PAP-', '')
    words = count_words(text)
    lines = text.count('\n') + 1
    has_refs = has_references_section(text)
    ref_count = count_references(text) if has_refs else 0
    ebf_markers = has_ebf_markers(text)

    # Flexible R2: check YAML bibliography_reference_count as fallback
    # This captures refs detected via Notes, Endnotes, inline citations
    yaml_bib_count = get_yaml_bib_count(key)
    has_sufficient_refs = has_refs or yaml_bib_count >= 10

    # If we have yaml_bib_count but no formal refs section, use yaml count
    if not has_refs and yaml_bib_count > 0:
        ref_count = yaml_bib_count

    # Classification
    issues = []

    # R4: No EBF markers
    if ebf_markers:
        issues.append(f"EBF markers found: {', '.join(ebf_markers[:3])}")

    # R2: Has references (flexible - formal section OR YAML bib count)
    if not has_sufficient_refs:
        issues.append("No references detected (no section + YAML bib_count < 10)")

    # R3: Minimum word count
    if words < 5000:
        issues.append(f"Too short ({words} words, need >5000)")

    # Determine level
    if not issues:
        # All criteria met - R1 (content), R2 (refs), R3 (length), R4 (no EBF)
        if words >= 10000 and ref_count >= 10:
            level = "L3"
        elif words >= 5000:
            level = "L3"
        else:
            level = "L2"
    elif len(issues) == 1 and not has_sufficient_refs and words >= 10000:
        # Long text but no refs detected - might be a book chapter or data report
        level = "L2"
    elif words < 1000:
        level = "L1"
    else:
        level = "L2"

    return {
        'file': filepath.name,
        'key': key,
        'words': words,
        'lines': lines,
        'has_refs': has_refs,
        'ref_count': ref_count,
        'yaml_bib_count': yaml_bib_count,
        'ebf_markers': ebf_markers,
        'issues': issues,
        'level': level,
    }


def get_yaml_level(key):
    """Get current content_level from YAML."""
    yaml_path = YAML_DIR / f"PAP-{key}.yaml"
    if not yaml_path.exists():
        return None, yaml_path

    try:
        with open(yaml_path) as f:
            data = yaml.safe_load(f)
        if data and 'full_text' in data:
            return data['full_text'].get('content_level'), yaml_path
        return None, yaml_path
    except Exception:
        return None, yaml_path


def fix_yaml_level(key, new_level):
    """Update content_level in YAML."""
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

        data['full_text']['content_level'] = new_level
        data['full_text']['available'] = True
        data['full_text']['path'] = f"data/paper-texts/PAP-{key}.md"

        with open(yaml_path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

        return True
    except Exception as e:
        print(f"  ERROR updating {yaml_path}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='Validate full-text completeness')
    parser.add_argument('--fix', action='store_true', help='Fix content_levels in YAML')
    parser.add_argument('--verbose', '-v', action='store_true', help='Detailed output')
    args = parser.parse_args()

    print("=" * 70)
    print("FULL-TEXT COMPLETENESS VALIDATION")
    print("=" * 70)
    print()

    md_files = sorted(TEXTS_DIR.glob("PAP-*.md"))
    print(f"Found {len(md_files)} full-text files")
    print()

    results = []
    level_counts = Counter()
    misclassified = []
    fixed = 0

    for md_file in md_files:
        info = classify_paper(md_file)
        results.append(info)
        level_counts[info['level']] += 1

        # Check if YAML has different level
        yaml_level, yaml_path = get_yaml_level(info['key'])

        if yaml_level and yaml_level != info['level']:
            misclassified.append({
                'key': info['key'],
                'yaml_level': yaml_level,
                'actual_level': info['level'],
                'issues': info['issues'],
            })

            if args.fix:
                if fix_yaml_level(info['key'], info['level']):
                    fixed += 1
                    if args.verbose:
                        print(f"  FIXED: {info['key']} {yaml_level} -> {info['level']}")

        elif not yaml_level:
            # content_level missing entirely — set it
            if args.fix:
                if fix_yaml_level(info['key'], info['level']):
                    fixed += 1
                    if args.verbose:
                        print(f"  SET: {info['key']} -> {info['level']} (was missing)")

        if args.verbose:
            status = "OK" if not info['issues'] else "ISSUES"
            ref_info = 'REFS' if info['has_refs'] else (f"B{info['yaml_bib_count']}" if info['yaml_bib_count'] else '----')
            print(f"  [{info['level']}] {info['file']:<45} {info['words']:>6} words  "
                  f"{ref_info:<5} "
                  f"{'EBF!' if info['ebf_markers'] else '    '}  {status}")

    # Summary
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print()
    print("Content Level Distribution:")
    for level in ['L3', 'L2', 'L1']:
        count = level_counts.get(level, 0)
        pct = count / len(results) * 100 if results else 0
        bar = "#" * int(pct / 2)
        print(f"  {level}: {count:>3} ({pct:5.1f}%)  {bar}")

    print()
    print(f"Has References section: {sum(1 for r in results if r['has_refs']):>3} / {len(results)}")
    print(f"Has EBF markers:       {sum(1 for r in results if r['ebf_markers']):>3} / {len(results)}")
    print(f"Average word count:    {sum(r['words'] for r in results) / len(results):>8,.0f}")

    if misclassified:
        print()
        print(f"MISCLASSIFIED: {len(misclassified)} files have wrong content_level in YAML")
        if not args.fix:
            print("  Run with --fix to correct them")
            print()
            for m in misclassified[:10]:
                print(f"  {m['key']}: YAML says {m['yaml_level']}, should be {m['actual_level']}")
                for issue in m['issues']:
                    print(f"    -> {issue}")

    if args.fix and fixed:
        print()
        print(f"FIXED: {fixed} YAML files updated")

    # Exit code
    if misclassified and not args.fix:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
