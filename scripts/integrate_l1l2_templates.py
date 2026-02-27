#!/usr/bin/env python3
"""
Integrate L1/L2 Templates into YAML SSOT
=========================================

Migrates structured summaries from papers/evaluated/integrated/*.txt
into data/paper-references/PAP-{key}.yaml files.

Part of the SSOT Architecture migration.

IMPLEMENTS (from Appendix BM):
- Definition 2: Content Level Function C(p) → {L0, L1, L2, L3}
- Definition 2a: L1/L2 Template Structure T_C
- Definition 2b: Confidence Multiplier ρ(C) → [0.6, 1.0]
- Axiom TPL-1: Template Equivalence
- Axiom TPL-2: Template Purpose
"""

import os
import re
import yaml
from pathlib import Path
from typing import Dict, Optional, List, Tuple, Set
from datetime import datetime

# =============================================================================
# PATHS (SSOT Architecture)
# =============================================================================
TEMPLATES_DIR = Path("papers/evaluated/integrated")
YAML_DIR = Path("data/paper-references")
PAPER_TEXTS_DIR = Path("data/paper-texts")

# =============================================================================
# DEFINITION 2: Content Level Thresholds (from Appendix BM)
# =============================================================================
# L0 < L1 < L2 < L3  ⟺  0 < 2000 < 6000 < 50000 chars
THRESHOLD_L1 = 2000   # Abstract threshold
THRESHOLD_L2 = 6000   # Key sections threshold
THRESHOLD_L3 = 50000  # Full text threshold

# =============================================================================
# DEFINITION 2b: Confidence Multiplier ρ(C)
# =============================================================================
CONFIDENCE_MULTIPLIER = {
    'L0': 0.60,  # Metadata only (40% uncertainty discount)
    'L1': 0.80,  # + Abstract/Template (20% discount)
    'L2': 0.95,  # + Key sections/Template (5% discount)
    'L3': 1.00,  # Full text (no discount)
}

# =============================================================================
# DEFINITION 2a: Template Schema T_C
# =============================================================================
TEMPLATE_SECTIONS = {
    'ABSTRACT',       # Extended summary
    'KEY_FINDINGS',   # Numbered list of empirical results
    'EBF_RELEVANCE',  # 10C dimensions, theory_support, parameters
    'SOURCES',        # URLs, BibTeX keys
}


def parse_template(content: str) -> Dict:
    """
    Parse L1/L2 template into structured sections.

    Implements Definition 2a: Template Schema T_C = (ABSTRACT, KEY_FINDINGS, EBF_RELEVANCE, SOURCES)
    """
    sections = {}

    # Extract paper key from first line
    key_match = re.search(r'^=+\s*\n(PAP-\S+)\s*\n=+', content, re.MULTILINE)
    if key_match:
        sections['paper_key'] = key_match.group(1)

    # Extract metadata (Title, Authors, Year, Journal, DOI)
    title_match = re.search(r'^Title:\s*(.+)$', content, re.MULTILINE)
    if title_match:
        sections['title'] = title_match.group(1).strip()

    authors_match = re.search(r'^Authors?:\s*(.+)$', content, re.MULTILINE)
    if authors_match:
        sections['authors'] = authors_match.group(1).strip()

    year_match = re.search(r'^Year:\s*(\d{4})', content, re.MULTILINE)
    if year_match:
        sections['year'] = year_match.group(1)

    journal_match = re.search(r'^Journal:\s*(.+)$', content, re.MULTILINE)
    if journal_match:
        sections['journal'] = journal_match.group(1).strip()

    doi_match = re.search(r'^DOI:\s*(\S+)', content, re.MULTILINE)
    if doi_match:
        sections['doi'] = doi_match.group(1).strip()

    # Extract ABSTRACT section
    abstract_match = re.search(
        r'=+\s*\nABSTRACT\s*\n=+\s*\n(.*?)(?:=+\s*\n|$)',
        content, re.DOTALL | re.IGNORECASE
    )
    if abstract_match:
        sections['abstract'] = abstract_match.group(1).strip()

    # Extract KEY FINDINGS section
    findings_match = re.search(
        r'=+\s*\nKEY FINDINGS\s*\n=+\s*\n(.*?)(?:=+\s*\n|$)',
        content, re.DOTALL | re.IGNORECASE
    )
    if findings_match:
        sections['key_findings'] = findings_match.group(1).strip()

    # Extract EBF RELEVANCE section
    relevance_match = re.search(
        r'=+\s*\nEBF RELEVANCE\s*\n=+\s*\n(.*?)(?:=+\s*\n|$)',
        content, re.DOTALL | re.IGNORECASE
    )
    if relevance_match:
        sections['ebf_relevance'] = relevance_match.group(1).strip()

    # Extract SOURCES section
    sources_match = re.search(
        r'=+\s*\nSOURCES?\s*\n=+\s*\n(.*?)$',
        content, re.DOTALL | re.IGNORECASE
    )
    if sources_match:
        sections['sources'] = sources_match.group(1).strip()

    return sections


def determine_content_level(char_count: int, has_abstract: bool = False,
                            has_findings: bool = False) -> Tuple[str, float]:
    """
    Determine content level and confidence multiplier from character count and field presence.

    Implements Definition 2 from Appendix BM:

    C(p) = {
        L0  if φ_C(p) ⊆ {title, author, year, journal, doi}
        L1  if abstract ∈ φ_C(p) ∧ |p|_C < 6000
        L2  if {methodology, findings} ⊆ φ_C(p) ∧ |p|_C < 50000
        L3  if full_text ∈ φ_C(p) ∧ |p|_C ≥ 50000
    }

    Args:
        char_count: Total character count of content
        has_abstract: Whether ABSTRACT section is present
        has_findings: Whether KEY_FINDINGS section is present

    Returns:
        Tuple of (content_level, confidence_multiplier)
    """
    # Definition 2: Content Level Function
    if char_count >= THRESHOLD_L3:
        level = 'L3'
    elif char_count >= THRESHOLD_L2 and has_findings:
        level = 'L2'
    elif char_count >= THRESHOLD_L1 and has_abstract:
        level = 'L1'
    else:
        level = 'L0'

    # Definition 2b: Confidence Multiplier
    rho = CONFIDENCE_MULTIPLIER[level]

    return level, rho


def load_yaml_safe(yaml_path: Path) -> Optional[Dict]:
    """Load YAML file with fallback for problematic files."""
    try:
        with open(yaml_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except yaml.YAMLError:
        # Fallback: try with errors='replace'
        try:
            with open(yaml_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
                # Clean up common issues
                content = content.replace('\t', '  ')
                return yaml.safe_load(content)
        except:
            return None
    except Exception:
        return None


def update_yaml_with_summary(yaml_path: Path, template_sections: Dict, template_char_count: int) -> bool:
    """Update YAML file with summary from template."""
    data = load_yaml_safe(yaml_path)
    if not data:
        return False

    # Create summary section
    summary = {
        'abstract_extended': template_sections.get('abstract', ''),
        'key_findings': template_sections.get('key_findings', ''),
        'ebf_relevance': template_sections.get('ebf_relevance', ''),
        'sources': template_sections.get('sources', ''),
        'template_source': f"papers/evaluated/integrated/{template_sections.get('paper_key', 'unknown')}.txt",
        'migrated_date': datetime.now().strftime('%Y-%m-%d')
    }

    # Only add non-empty fields
    summary = {k: v for k, v in summary.items() if v}

    # Update data
    data['summary'] = summary

    # Check if we already have full_text
    existing_full_text = data.get('full_text', {})
    existing_available = existing_full_text.get('available', False)
    existing_char_count = existing_full_text.get('character_count', 0)

    # If no full_text yet, the template becomes the main content
    # Update content_level based on combined content (Axiom TPL-1: Template Equivalence)
    total_chars = max(existing_char_count or 0, template_char_count)
    has_abstract = bool(template_sections.get('abstract'))
    has_findings = bool(template_sections.get('key_findings'))
    new_level, new_multiplier = determine_content_level(
        total_chars, has_abstract=has_abstract, has_findings=has_findings
    )

    # Update full_text section if it was L0/L1
    if not existing_available or existing_full_text.get('content_level', 'L0') in ['L0', 'L1']:
        if 'full_text' not in data:
            data['full_text'] = {}
        # Keep available=false if no actual fulltext, but note the template content
        if not existing_available:
            data['full_text']['template_available'] = True
            data['full_text']['template_char_count'] = template_char_count
        data['full_text']['content_level'] = new_level

    # Update prior_score confidence multiplier
    if 'prior_score' in data:
        old_multiplier = data['prior_score'].get('confidence_multiplier', 0.6)
        if new_multiplier > old_multiplier:
            data['prior_score']['confidence_multiplier'] = new_multiplier
            data['prior_score']['content_level'] = new_level
            # Recalculate prior_score with new multiplier
            old_score = data['prior_score'].get('prior_score', 0)
            if old_score and old_multiplier:
                # Adjust score proportionally
                base_score = old_score / old_multiplier
                new_score = round(base_score * new_multiplier, 4)
                data['prior_score']['prior_score'] = new_score
                # Update classification
                if new_score >= 0.7:
                    data['prior_score']['classification'] = 'FULL'
                elif new_score >= 0.5:
                    data['prior_score']['classification'] = 'STANDARD'
                elif new_score >= 0.3:
                    data['prior_score']['classification'] = 'MINIMAL'
                else:
                    data['prior_score']['classification'] = 'REJECT'

    # Write back
    try:
        with open(yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False, width=100)
        return True
    except Exception as e:
        print(f"  Error writing {yaml_path}: {e}")
        return False


def main():
    """Main integration function."""
    print("=" * 70)
    print("L1/L2 Template Integration into YAML SSOT")
    print("=" * 70)

    # Find all template files
    template_files = list(TEMPLATES_DIR.glob("*.txt"))
    print(f"\nFound {len(template_files)} template files")

    stats = {
        'processed': 0,
        'updated': 0,
        'yaml_not_found': 0,
        'parse_failed': 0,
        'update_failed': 0
    }

    for template_path in sorted(template_files):
        # Extract paper key from filename
        paper_key = template_path.stem  # e.g., PAP-kahneman1979prospect

        # Find corresponding YAML
        yaml_path = YAML_DIR / f"{paper_key}.yaml"

        if not yaml_path.exists():
            # Try without PAP- prefix
            if paper_key.startswith('PAP-'):
                alt_key = paper_key[4:]
                yaml_path = YAML_DIR / f"PAP-{alt_key}.yaml"

        if not yaml_path.exists():
            stats['yaml_not_found'] += 1
            continue

        # Read template
        try:
            with open(template_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
                char_count = len(content)
        except Exception as e:
            print(f"  Error reading {template_path}: {e}")
            stats['parse_failed'] += 1
            continue

        # Parse template
        sections = parse_template(content)
        if not sections.get('abstract') and not sections.get('key_findings'):
            stats['parse_failed'] += 1
            continue

        sections['paper_key'] = paper_key

        # Update YAML
        if update_yaml_with_summary(yaml_path, sections, char_count):
            stats['updated'] += 1
        else:
            stats['update_failed'] += 1

        stats['processed'] += 1

        # Progress indicator
        if stats['processed'] % 50 == 0:
            print(f"  Processed {stats['processed']} templates...")

    # Summary
    print("\n" + "=" * 70)
    print("INTEGRATION COMPLETE")
    print("=" * 70)
    print(f"Templates processed:   {stats['processed']}")
    print(f"YAMLs updated:         {stats['updated']}")
    print(f"YAML not found:        {stats['yaml_not_found']}")
    print(f"Parse failed:          {stats['parse_failed']}")
    print(f"Update failed:         {stats['update_failed']}")

    return stats


if __name__ == "__main__":
    main()
