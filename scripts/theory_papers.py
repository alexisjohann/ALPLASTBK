#!/usr/bin/env python3
"""
Theory-Papers Lookup Script
===========================

Bidirectional lookup between:
- Appendix MS Theory Catalog (data/theory-catalog.yaml)
- Master Bibliography (bibliography/bcm_master.bib)

Usage:
    # Find papers supporting a theory
    python scripts/theory_papers.py --theory MS-RD-001
    python scripts/theory_papers.py --theory "Prospect Theory"

    # Find theories a paper supports
    python scripts/theory_papers.py --paper kahneman1979prospect

    # List all theories in a category
    python scripts/theory_papers.py --category CAT-03
    python scripts/theory_papers.py --category "Reference Dependence"

    # Search theories by restriction
    python scripts/theory_papers.py --restriction "lambda > 1"

    # Show statistics
    python scripts/theory_papers.py --stats

    # Export for 10C model matching
    python scripts/theory_papers.py --match-10c "beta < 1, psi_default"

Author: EBF Team
Version: 1.0 (January 2026)
"""

import argparse
import yaml
import re
import os
from pathlib import Path
from collections import defaultdict

# Paths
SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
THEORY_CATALOG = ROOT_DIR / "data" / "theory-catalog.yaml"
BIB_FILE = ROOT_DIR / "bibliography" / "bcm_master.bib"


def load_theory_catalog():
    """Load the theory catalog YAML file."""
    with open(THEORY_CATALOG, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def parse_bibtex(bib_path):
    """Parse BibTeX file and extract entries with theory_support field."""
    entries = {}
    current_key = None
    current_entry = {}

    with open(bib_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Simple BibTeX parser
    entry_pattern = r'@(\w+)\{([^,]+),([^@]*)'
    matches = re.findall(entry_pattern, content, re.DOTALL)

    for entry_type, key, fields in matches:
        entry = {'type': entry_type, 'key': key.strip()}

        # Extract fields
        field_pattern = r'(\w+)\s*=\s*\{([^}]*)\}'
        field_matches = re.findall(field_pattern, fields)

        for field_name, field_value in field_matches:
            entry[field_name.lower()] = field_value.strip()

        entries[key.strip()] = entry

    return entries


def find_papers_for_theory(theory_id, catalog, bib_entries):
    """Find all papers that support a given theory."""
    papers = []

    # Find the theory in the catalog
    theory = None
    for cat in catalog.get('categories', []):
        for t in cat.get('theories', []):
            if t['id'] == theory_id or t['name'].lower() == theory_id.lower():
                theory = t
                break
        if theory:
            break

    if not theory:
        return None, []

    # Get papers from bib_keys
    bib_keys = theory.get('bib_keys', [])
    for key in bib_keys:
        if key in bib_entries:
            papers.append(bib_entries[key])

    # Also search for papers with theory_support field
    for key, entry in bib_entries.items():
        theory_support = entry.get('theory_support', '')
        if theory_id in theory_support or theory['name'] in theory_support:
            if entry not in papers:
                papers.append(entry)

    return theory, papers


def find_theories_for_paper(paper_key, catalog, bib_entries):
    """Find all theories that a paper supports."""
    theories = []

    paper = bib_entries.get(paper_key)
    if not paper:
        return None, []

    # Check theory_support field in paper
    theory_support = paper.get('theory_support', '')
    supported_ids = [s.strip() for s in theory_support.split(',') if s.strip()]

    # Search all theories for this paper
    for cat in catalog.get('categories', []):
        for theory in cat.get('theories', []):
            # Check if paper is in bib_keys
            if paper_key in theory.get('bib_keys', []):
                theories.append((cat, theory))
            # Check if theory_id matches
            elif theory['id'] in supported_ids:
                theories.append((cat, theory))

    return paper, theories


def list_category(category_id, catalog):
    """List all theories in a category."""
    for cat in catalog.get('categories', []):
        if cat['id'] == category_id or cat['name'].lower() == category_id.lower():
            return cat
    return None


def search_by_restriction(restriction, catalog):
    """Search theories by EBF restriction pattern."""
    results = []
    restriction_lower = restriction.lower()

    for cat in catalog.get('categories', []):
        for theory in cat.get('theories', []):
            restrictions = theory.get('ebf_restrictions', {})
            for key, value in restrictions.items():
                if restriction_lower in str(value).lower() or restriction_lower in key.lower():
                    results.append((cat, theory))
                    break

    return results


def match_10c(dimensions, catalog):
    """Match theories to 10C dimensions."""
    results = []
    dim_list = [d.strip().lower() for d in dimensions.split(',')]

    for cat in catalog.get('categories', []):
        for theory in cat.get('theories', []):
            restrictions = theory.get('ebf_restrictions', {})
            match_score = 0
            matches = []

            for dim in dim_list:
                for key, value in restrictions.items():
                    if dim in key.lower() or dim in str(value).lower():
                        match_score += 1
                        matches.append(f"{key}={value}")
                        break

            if match_score > 0:
                results.append((cat, theory, match_score, matches))

    # Sort by match score
    results.sort(key=lambda x: x[2], reverse=True)
    return results


def get_statistics(catalog, bib_entries):
    """Get statistics about the theory catalog and paper coverage."""
    stats = {
        'total_theories': 0,
        'total_categories': len(catalog.get('categories', [])),
        'theories_per_category': {},
        'papers_linked': 0,
        'papers_with_theory_support': 0,
        'theories_with_der_proof': 0,
        'restriction_distribution': defaultdict(int)
    }

    all_bib_keys = set()

    for cat in catalog.get('categories', []):
        cat_count = len(cat.get('theories', []))
        stats['theories_per_category'][cat['name']] = cat_count
        stats['total_theories'] += cat_count

        for theory in cat.get('theories', []):
            # Count linked papers
            bib_keys = theory.get('bib_keys', [])
            all_bib_keys.update(bib_keys)

            # Count DER proofs
            if theory.get('der_proof'):
                stats['theories_with_der_proof'] += 1

            # Count restrictions
            restrictions = theory.get('ebf_restrictions', {})
            for key in restrictions:
                stats['restriction_distribution'][key] += 1

    stats['papers_linked'] = len(all_bib_keys)

    # Count papers with theory_support
    for entry in bib_entries.values():
        if entry.get('theory_support'):
            stats['papers_with_theory_support'] += 1

    return stats


def format_theory(theory, cat=None, verbose=False):
    """Format a theory for display."""
    output = []
    output.append(f"  {theory['id']}: {theory['name']}")
    output.append(f"    Authors: {theory['authors']} ({theory['year']})")

    if verbose:
        output.append(f"    Category: {cat['name'] if cat else 'Unknown'}")
        output.append(f"    Validity: {theory.get('validity', 'N/A')}")

        restrictions = theory.get('ebf_restrictions', {})
        if restrictions:
            output.append("    EBF Restrictions:")
            for key, value in restrictions.items():
                output.append(f"      - {key}: {value}")

        if theory.get('der_proof'):
            output.append(f"    Formal Proof: {theory['der_proof']}")

        bib_keys = theory.get('bib_keys', [])
        if bib_keys:
            output.append(f"    Papers: {', '.join(bib_keys)}")

    return '\n'.join(output)


def format_paper(paper, verbose=False):
    """Format a paper for display."""
    output = []
    output.append(f"  [{paper['key']}]")
    output.append(f"    Title: {paper.get('title', 'N/A')}")
    output.append(f"    Author: {paper.get('author', 'N/A')}")
    output.append(f"    Year: {paper.get('year', 'N/A')}")

    if verbose:
        if paper.get('journal'):
            output.append(f"    Journal: {paper['journal']}")
        if paper.get('theory_support'):
            output.append(f"    Theory Support: {paper['theory_support']}")
        if paper.get('parameter'):
            output.append(f"    Parameters: {paper['parameter']}")

    return '\n'.join(output)


def main():
    parser = argparse.ArgumentParser(
        description='Bidirectional lookup between Theory Catalog and Bibliography',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --theory MS-RD-001          # Find papers for Prospect Theory
  %(prog)s --paper kahneman1979prospect # Find theories supported by paper
  %(prog)s --category CAT-03           # List Reference Dependence theories
  %(prog)s --restriction "lambda > 1"  # Find loss aversion theories
  %(prog)s --match-10c "beta < 1"      # Match to 10C model
  %(prog)s --stats                     # Show statistics
        """
    )

    parser.add_argument('--theory', '-t', help='Find papers for a theory (ID or name)')
    parser.add_argument('--paper', '-p', help='Find theories supported by a paper (BibTeX key)')
    parser.add_argument('--category', '-c', help='List theories in a category (ID or name)')
    parser.add_argument('--restriction', '-r', help='Search by EBF restriction pattern')
    parser.add_argument('--match-10c', '-m', help='Match theories to 10C dimensions (comma-separated)')
    parser.add_argument('--stats', '-s', action='store_true', help='Show statistics')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--json', action='store_true', help='Output as JSON')

    args = parser.parse_args()

    # Load data
    catalog = load_theory_catalog()
    bib_entries = parse_bibtex(BIB_FILE)

    if args.stats:
        stats = get_statistics(catalog, bib_entries)
        print("\n=== Theory Catalog Statistics ===\n")
        print(f"Total Theories: {stats['total_theories']}")
        print(f"Total Categories: {stats['total_categories']}")
        print(f"Papers Linked: {stats['papers_linked']}")
        print(f"Theories with DER Proofs: {stats['theories_with_der_proof']}")
        print(f"\nTheories per Category:")
        for cat, count in stats['theories_per_category'].items():
            print(f"  {cat}: {count}")
        print(f"\nRestriction Distribution:")
        for key, count in sorted(stats['restriction_distribution'].items(), key=lambda x: -x[1]):
            print(f"  {key}: {count}")
        return

    if args.theory:
        theory, papers = find_papers_for_theory(args.theory, catalog, bib_entries)
        if theory:
            print(f"\n=== Theory: {theory['name']} ===\n")
            print(format_theory(theory, verbose=True))
            print(f"\n=== Supporting Papers ({len(papers)}) ===\n")
            for paper in papers:
                print(format_paper(paper, args.verbose))
        else:
            print(f"Theory not found: {args.theory}")
        return

    if args.paper:
        paper, theories = find_theories_for_paper(args.paper, catalog, bib_entries)
        if paper:
            print(f"\n=== Paper ===\n")
            print(format_paper(paper, verbose=True))
            print(f"\n=== Supported Theories ({len(theories)}) ===\n")
            for cat, theory in theories:
                print(format_theory(theory, cat, args.verbose))
        else:
            print(f"Paper not found: {args.paper}")
        return

    if args.category:
        cat = list_category(args.category, catalog)
        if cat:
            print(f"\n=== Category: {cat['name']} ===")
            print(f"Restriction: {cat['restriction']}")
            print(f"Validity Domain: {cat['validity_domain']}")
            print(f"\nTheories ({len(cat.get('theories', []))}):\n")
            for theory in cat.get('theories', []):
                print(format_theory(theory, cat, args.verbose))
        else:
            print(f"Category not found: {args.category}")
        return

    if args.restriction:
        results = search_by_restriction(args.restriction, catalog)
        print(f"\n=== Theories with restriction '{args.restriction}' ({len(results)}) ===\n")
        for cat, theory in results:
            print(format_theory(theory, cat, args.verbose))
        return

    if args.match_10c:
        results = match_10c(args.match_10c, catalog)
        print(f"\n=== 10C Matching for '{args.match_10c}' ({len(results)} matches) ===\n")
        for cat, theory, score, matches in results[:10]:  # Top 10
            print(f"  [{score} matches] {theory['id']}: {theory['name']}")
            print(f"    Matched: {', '.join(matches)}")
            print(f"    Authors: {theory['authors']} ({theory['year']})")
            print()
        return

    # Default: show help
    parser.print_help()


if __name__ == '__main__':
    main()
