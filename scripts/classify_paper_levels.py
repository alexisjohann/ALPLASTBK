#!/usr/bin/env python3
"""
Paper Level Classification Script
==================================
Classifies all papers in bcm_master.bib according to the 2D system:
- Content Level (0-3): How much raw content we have
- Integration Level (1-5): How deeply integrated into EBF

Based on Appendix BM (METHOD-PAPERINT)
"""

import os
import re
import yaml
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

# Paths
BASE_DIR = Path(__file__).parent.parent
BIB_FILE = BASE_DIR / "bibliography" / "bcm_master.bib"
PAPER_REFS_DIR = BASE_DIR / "data" / "paper-references"
PAPER_TEXTS_DIR = BASE_DIR / "data" / "paper-texts"
CASE_REGISTRY = BASE_DIR / "data" / "case-registry.yaml"
THEORY_CATALOG = BASE_DIR / "data" / "theory-catalog.yaml"
CHAPTERS_DIR = BASE_DIR / "chapters"
APPENDICES_DIR = BASE_DIR / "appendices"
OUTPUT_FILE = BASE_DIR / "data" / "paper-level-classification.yaml"


def parse_bibtex():
    """Parse BibTeX file and extract all papers with their fields."""
    papers = {}

    with open(BIB_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Match entries
    entries = re.findall(r'@(\w+)\{([^,]+),([^@]*)', content, re.DOTALL)

    for entry_type, key, fields in entries:
        paper = {
            'key': key.strip(),
            'type': entry_type,
            'fields': {}
        }

        # Extract relevant fields
        for field_name in ['abstract', 'theory_support', 'parameter', 'use_for',
                          'evidence_tier', 'doi', 'title', 'author', 'year']:
            match = re.search(rf'{field_name}\s*=\s*[{{"](.*?)[}}"]', fields, re.I | re.DOTALL)
            if match:
                paper['fields'][field_name] = match.group(1).strip()

        papers[key.strip()] = paper

    return papers


def get_paper_yaml_content(key):
    """Get content details from paper YAML file."""
    # Handle keys that already have PAP- prefix
    if key.startswith('PAP-'):
        yaml_path = PAPER_REFS_DIR / f"{key}.yaml"
    else:
        yaml_path = PAPER_REFS_DIR / f"PAP-{key}.yaml"
    if not yaml_path.exists():
        return {'size': 0, 'has_template': False, 'content_fields': []}

    try:
        with open(yaml_path, 'r', encoding='utf-8') as f:
            content = f.read()
            data = yaml.safe_load(content)

        if not data:
            return {'size': len(content), 'has_template': False, 'content_fields': []}

        # Check for content template fields (not just reference tracking)
        content_fields = []
        template_fields = [
            'authors', 'publication', 'evidence', 'simulation', 'experiment',
            'key_findings', 'ebf_integration', 'cross_references', 'quotable',
            'figure_results', 'related_papers', 'methodology', 'parameters_extracted'
        ]

        for field in template_fields:
            if field in data and data[field]:
                content_fields.append(field)

        # Check for content_level field explicitly set
        explicit_level = data.get('content_level')

        return {
            'size': len(content),
            'has_template': len(content_fields) >= 3,  # At least 3 template fields
            'content_fields': content_fields,
            'explicit_level': explicit_level,
            'integration_level': data.get('Integration Level') or data.get('integration_level')
        }
    except Exception as e:
        return {'size': 0, 'has_template': False, 'content_fields': [], 'error': str(e)}


def get_paper_fulltext_size(key):
    """Get full text size in characters."""
    # Handle keys that already have PAP- prefix
    if key.startswith('PAP-'):
        txt_path = PAPER_TEXTS_DIR / f"{key}.md"
    else:
        txt_path = PAPER_TEXTS_DIR / f"PAP-{key}.md"
    if txt_path.exists():
        with open(txt_path, 'r', encoding='utf-8') as f:
            return len(f.read())
    return 0


def get_cases_citing_paper(key):
    """Check if paper is cited in case registry."""
    if not CASE_REGISTRY.exists():
        return []

    with open(CASE_REGISTRY, 'r', encoding='utf-8') as f:
        content = f.read()

    # Simple check for paper key in case registry
    if key in content:
        return [key]  # Simplified - could extract actual case IDs
    return []


def get_theories_citing_paper(key):
    """Check if paper is cited in theory catalog."""
    if not THEORY_CATALOG.exists():
        return []

    with open(THEORY_CATALOG, 'r', encoding='utf-8') as f:
        content = f.read()

    if key in content:
        return [key]
    return []


def check_chapter_citations(key):
    """Check if paper is cited in any chapter."""
    chapters_citing = []

    for tex_file in CHAPTERS_DIR.glob("*.tex"):
        with open(tex_file, 'r', encoding='utf-8') as f:
            content = f.read()
        if key in content:
            chapters_citing.append(tex_file.stem)

    return chapters_citing


def check_appendix_citations(key):
    """Check if paper is cited in any appendix."""
    appendices_citing = []

    for tex_file in APPENDICES_DIR.glob("*.tex"):
        with open(tex_file, 'r', encoding='utf-8') as f:
            content = f.read()
        if key in content:
            appendices_citing.append(tex_file.stem)

    return appendices_citing


def classify_content_level(paper, yaml_info, fulltext_size):
    """
    Classify Content Level (0-3):
    0 = BibTeX only (no abstract, no template)
    1 = Basic template - has abstract OR basic YAML with few fields
    2 = Full template - has YAML with many content fields (authors, evidence, findings, etc.)
    3 = Full text (>50k chars in paper-texts/)
    """
    # Check for explicit level in YAML
    if yaml_info.get('explicit_level'):
        explicit = yaml_info['explicit_level']
        if explicit == '100%' or explicit == 3:
            return 3 if fulltext_size > 0 else 2
        elif explicit == '75%' or explicit == 2:
            return 2
        elif explicit == '50%' or explicit == 1:
            return 1

    # Level 3: Full text > 50k chars (or any full text)
    if fulltext_size > 50000:
        return 3

    # Level 2: Full template (many content fields)
    if yaml_info.get('has_template') and len(yaml_info.get('content_fields', [])) >= 5:
        return 2

    # Level 1: Basic template (has abstract OR some template fields)
    if paper['fields'].get('abstract') or yaml_info.get('has_template'):
        return 1

    # Level 0: BibTeX only (reference tracking YAML doesn't count)
    return 0


def classify_integration_level(paper, in_cases, in_theories, in_chapters, in_appendices):
    """
    Classify Integration Level (1-5):
    1 = MINIMAL (BibTeX only)
    2 = STANDARD (has theory_support OR parameter)
    3 = CASE (in Case Registry)
    4 = THEORY (in Theory Catalog)
    5 = FULL (cited in BOTH appendices AND chapters)
    """
    has_theory_support = bool(paper['fields'].get('theory_support'))
    has_parameter = bool(paper['fields'].get('parameter'))

    # Level 5: Cited in BOTH chapters AND appendices
    if in_chapters and in_appendices:
        return 5

    # Level 4: In Theory Catalog
    if in_theories:
        return 4

    # Level 3: In Case Registry
    if in_cases:
        return 3

    # Level 2: Has EBF fields
    if has_theory_support or has_parameter:
        return 2

    # Level 1: Minimal
    return 1


def main():
    print("=" * 70)
    print("PAPER LEVEL CLASSIFICATION")
    print("Based on Appendix BM (METHOD-PAPERINT)")
    print("=" * 70)
    print()

    # Parse all papers
    print("Parsing bibliography...")
    papers = parse_bibtex()
    print(f"Found {len(papers)} papers")
    print()

    # Classification results
    results = {
        'metadata': {
            'generated': datetime.now().isoformat(),
            'total_papers': len(papers),
            'methodology': 'Appendix BM (METHOD-PAPERINT)',
            'dimensions': {
                'content_level': {
                    '0': 'BibTeX only (no abstract)',
                    '1': 'Basic template (~2k chars, has abstract)',
                    '2': 'Full template (~6k chars, has YAML)',
                    '3': 'Full text (>50k chars)'
                },
                'integration_level': {
                    '1': 'MINIMAL (BibTeX only)',
                    '2': 'STANDARD (has theory_support OR parameter)',
                    '3': 'CASE (in Case Registry)',
                    '4': 'THEORY (in Theory Catalog)',
                    '5': 'FULL (cited in BOTH appendices AND chapters)'
                }
            }
        },
        'statistics': {
            'content_levels': {0: 0, 1: 0, 2: 0, 3: 0},
            'integration_levels': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
            'matrix': {}  # Content x Integration matrix
        },
        'papers': {}
    }

    # Initialize matrix
    for c in range(4):
        for i in range(1, 6):
            results['statistics']['matrix'][f"C{c}_I{i}"] = 0

    # Classify each paper
    print("Classifying papers...")
    for idx, (key, paper) in enumerate(papers.items()):
        if (idx + 1) % 500 == 0:
            print(f"  Processed {idx + 1}/{len(papers)}...")

        # Get content information
        yaml_info = get_paper_yaml_content(key)
        fulltext_size = get_paper_fulltext_size(key)

        # Get integration information
        in_cases = get_cases_citing_paper(key)
        in_theories = get_theories_citing_paper(key)
        in_chapters = check_chapter_citations(key)
        in_appendices = check_appendix_citations(key)

        # Classify
        content_level = classify_content_level(paper, yaml_info, fulltext_size)
        integration_level = classify_integration_level(
            paper, in_cases, in_theories, in_chapters, in_appendices
        )

        # Store result
        results['papers'][key] = {
            'content_level': content_level,
            'integration_level': integration_level,
            'content_details': {
                'has_abstract': bool(paper['fields'].get('abstract')),
                'yaml_size': yaml_info.get('size', 0),
                'yaml_has_template': yaml_info.get('has_template', False),
                'yaml_content_fields': yaml_info.get('content_fields', []),
                'fulltext_size': fulltext_size
            },
            'integration_details': {
                'has_theory_support': bool(paper['fields'].get('theory_support')),
                'has_parameter': bool(paper['fields'].get('parameter')),
                'in_cases': len(in_cases) > 0,
                'in_theories': len(in_theories) > 0,
                'in_chapters': in_chapters,
                'in_appendices': in_appendices[:5] if len(in_appendices) > 5 else in_appendices
            }
        }

        # Update statistics
        results['statistics']['content_levels'][content_level] += 1
        results['statistics']['integration_levels'][integration_level] += 1
        results['statistics']['matrix'][f"C{content_level}_I{integration_level}"] += 1

    # Save results
    print()
    print("Saving classification...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        yaml.dump(results, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    print(f"Saved to: {OUTPUT_FILE}")
    print()

    # Print summary
    print("=" * 70)
    print("CLASSIFICATION SUMMARY")
    print("=" * 70)
    print()

    print("CONTENT LEVELS:")
    for level, count in results['statistics']['content_levels'].items():
        pct = count / len(papers) * 100
        bar = "█" * int(pct / 2)
        print(f"  Level {level}: {count:>5} ({pct:>5.1f}%) {bar}")

    print()
    print("INTEGRATION LEVELS:")
    for level, count in results['statistics']['integration_levels'].items():
        pct = count / len(papers) * 100
        bar = "█" * int(pct / 2)
        print(f"  Level {level}: {count:>5} ({pct:>5.1f}%) {bar}")

    print()
    print("2D MATRIX (Content x Integration):")
    print()
    print("         | Int-1  | Int-2  | Int-3  | Int-4  | Int-5  |")
    print("-" * 60)
    for c in range(4):
        row = f"Cont-{c}  |"
        for i in range(1, 6):
            count = results['statistics']['matrix'][f"C{c}_I{i}"]
            row += f" {count:>5} |"
        print(row)
    print("-" * 60)

    # Identify upgrade priorities
    print()
    print("=" * 70)
    print("UPGRADE PRIORITIES")
    print("=" * 70)
    print()

    # Papers that need Content upgrade (have integration but no content)
    high_int_low_cont = [k for k, v in results['papers'].items()
                         if v['integration_level'] >= 3 and v['content_level'] == 0]
    print(f"High Integration (3+), No Content (0): {len(high_int_low_cont)} papers")
    print("  → Priority: Add abstracts via OpenAlex/SerpApi")

    # Papers that need Integration upgrade (have content but not integrated)
    high_cont_low_int = [k for k, v in results['papers'].items()
                         if v['content_level'] >= 2 and v['integration_level'] == 1]
    print(f"High Content (2+), Minimal Integration (1): {len(high_cont_low_int)} papers")
    print("  → Priority: Add theory_support, parameter fields")

    # Near Level 5 (in appendices but not chapters)
    near_level_5 = [k for k, v in results['papers'].items()
                    if v['integration_level'] == 4 or
                    (v['integration_details']['in_appendices'] and not v['integration_details']['in_chapters'])]
    print(f"Near Level 5 (in appendices, not chapters): {len(near_level_5)} papers")
    print("  → Priority: Add chapter citations")

    print()
    print("Done!")


if __name__ == '__main__':
    main()
