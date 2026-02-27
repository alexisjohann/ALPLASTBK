#!/usr/bin/env python3
"""Generate BibTeX entries for papers that have YAML but no BibTeX entry.

Reads paper metadata from YAML and full-text .md files, generates
BibTeX entries with EBF fields, and appends to bcm_master.bib.

Usage:
    python scripts/generate_bibtex_from_yaml.py                   # dry-run
    python scripts/generate_bibtex_from_yaml.py --execute          # append to bib
    python scripts/generate_bibtex_from_yaml.py --key berger2026labor  # single
"""

import argparse
import os
import re
import sys

BIB_FILE = "bibliography/bcm_master.bib"
REFS_DIR = "data/paper-references"
TEXTS_DIR = "data/paper-texts"

# Papers to process with their full author strings
PAPERS = {
    'berger2026labor': {
        'authors': 'Berger, David and Herkenhoff, Kyle and Mongey, Simon',
        'pages': '93--114',
    },
    'geruso2026likelihood': {
        'authors': 'Geruso, Michael and Spears, Dean',
        'pages': '3--26',
    },
    'gobbi2026family': {
        'authors': 'Gobbi, Paula E. and Hannusch, Anne and Rossi, Pauline',
        'pages': '47--70',
    },
    'johnson2026occupational': {
        'authors': 'Johnson, Janna E.',
        'pages': '167--190',
    },
    'khanna2026asia': {
        'authors': 'Khanna, Gaurav',
        'pages': '215--240',
    },
    'postel2026asian': {
        'authors': 'Postel, Hannah M.',
        'pages': '191--214',
    },
    'prager2026antitrust': {
        'authors': 'Prager, Elena',
        'pages': '115--138',
    },
    'pritchett2026global': {
        'authors': 'Pritchett, Lant',
        'pages': '71--92',
    },
    'starr2026economics': {
        'authors': 'Starr, Evan',
        'pages': '139--166',
    },
    'taylor2026recommendations': {
        'authors': 'Taylor, Timothy',
        'pages': '241--248',
    },
    'weil2026continued': {
        'authors': 'Weil, David N.',
        'pages': '27--46',
    },
}


def get_title(key):
    """Get title from YAML file."""
    yaml_path = os.path.join(REFS_DIR, f"PAP-{key}.yaml")
    with open(yaml_path, 'r') as f:
        for line in f:
            if line.startswith('title:'):
                title = line.replace('title:', '').strip().strip("'\"")
                return title
    return key


def already_in_bib(key):
    """Check if key already exists in bib file."""
    with open(BIB_FILE, 'r') as f:
        content = f.read()
    return f'{{{key},' in content


def generate_entry(key, meta):
    """Generate BibTeX entry string."""
    title = get_title(key)

    entry = f"""
@article{{{key},
  author = {{{meta['authors']}}},
  title = {{{{{title}}}}},
  journal = {{Journal of Economic Perspectives}},
  year = {{2026}},
  volume = {{40}},
  number = {{1}},
  pages = {{{meta['pages']}}},
  doi = {{}},
  evidence_tier = {{1}},
  use_for = {{LIT-O}},
  theory_support = {{}},
  parameter = {{}},
  identification = {{}},
  external_validity = {{}},
  session_ref = {{}},
  notes = {{JEP Winter 2026 symposium paper. Full text available in data/paper-texts/PAP-{key}.md.}},
}}"""
    return entry


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--execute', action='store_true')
    parser.add_argument('--key', type=str)
    args = parser.parse_args()

    papers = PAPERS
    if args.key:
        if args.key not in papers:
            print(f"ERROR: {args.key} not in paper list")
            sys.exit(1)
        papers = {args.key: papers[args.key]}

    entries = []
    for key, meta in papers.items():
        if already_in_bib(key):
            print(f"  SKIP {key}: already in bib")
            continue
        entry = generate_entry(key, meta)
        entries.append(entry)
        if args.execute:
            print(f"  ADD {key}")
        else:
            print(f"  [DRY-RUN] Would add {key}")

    if entries:
        if args.execute:
            with open(BIB_FILE, 'a') as f:
                f.write('\n% === JEP Vol 40, No 1, Winter 2026 ===\n')
                for entry in entries:
                    f.write(entry)
                    f.write('\n')
            print(f"\nAppended {len(entries)} entries to {BIB_FILE}")
        else:
            print(f"\nWould append {len(entries)} entries. Use --execute.")
            print("\nSample entry:")
            print(entries[0])


if __name__ == '__main__':
    main()
