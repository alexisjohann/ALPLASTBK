#!/usr/bin/env python3
"""
Add abstracts from SWSM JSON to bcm_master.bib entries.
"""

import json
import re
from pathlib import Path

# Mapping from SWSM author to BibTeX keys and paper info
PAPER_MAPPING = {
    "Sutter": {
        "key_pattern": r"sutter2013impatience",
        "title_contains": "Impatience"
    },
    "Fehr": {
        "key_pattern": r"PAP-fehr1999theory",
        "title_contains": "Fairness"
    },
    "Thaler": {
        "key_pattern": r"PAP-PAP-thaler1980towardtoward",
        "title_contains": "Consumer Choice"
    },
    "Kahneman": {
        "key_pattern": r"PAP-PAP-kahneman1979prospectprospect",
        "title_contains": "Prospect Theory"
    },
    "Camerer": {
        "key_pattern": r"PAP-PAP-camerer2004neuroeconomicsneuroeconomics",
        "title_contains": "Neuroeconomics"
    },
    "List": {
        "key_pattern": r"list2004field",
        "title_contains": "Field Experiment"
    },
    "Gneezy": {
        "key_pattern": r"PAP-gneezy2011when",
        "title_contains": "Incentive"
    },
    "Ariely": {
        "key_pattern": r"PAP-ariely2008predictably",
        "title_contains": "Predictably"
    },
    "Sunstein": {
        "key_pattern": r"PAP-sunstein2014nudge|PAP-sunstein2014nudge",
        "title_contains": "Nudge"
    },
    "Mullainathan": {
        "key_pattern": r"PAP-mullainathan2013scarcity",
        "title_contains": "Scarcity"
    },
    "Autor": {
        "key_pattern": r"autor2016china",
        "title_contains": "China"
    },
    "Shiller": {
        "key_pattern": r"shiller2000irrationalirrational",
        "title_contains": "Irrational Exuberance"
    }
}

def load_abstracts(json_path: str) -> dict:
    """Load abstracts from JSON."""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['abstracts']

def find_entry_position(bib_content: str, key_pattern: str) -> tuple:
    """Find the position of a BibTeX entry by key pattern."""
    pattern = rf'@\w+\{{({key_pattern})\s*,'
    match = re.search(pattern, bib_content, re.IGNORECASE)
    if match:
        key = match.group(1)
        start = match.start()
        # Find the closing brace
        brace_count = 0
        end = start
        for i, c in enumerate(bib_content[start:], start):
            if c == '{':
                brace_count += 1
            elif c == '}':
                brace_count -= 1
                if brace_count == 0:
                    end = i + 1
                    break
        return key, start, end
    return None, -1, -1

def add_abstract_to_entry(entry: str, abstract: str) -> str:
    """Add abstract field to a BibTeX entry if not already present."""
    if 'abstract' in entry.lower():
        print("  (abstract already exists, skipping)")
        return entry

    # Escape special LaTeX characters in abstract
    abstract_escaped = abstract.replace('&', r'\&')
    abstract_escaped = abstract_escaped.replace('%', r'\%')
    abstract_escaped = abstract_escaped.replace('$', r'\$')
    abstract_escaped = abstract_escaped.replace('#', r'\#')
    abstract_escaped = abstract_escaped.replace('_', r'\_')
    abstract_escaped = abstract_escaped.replace('{', r'\{')
    abstract_escaped = abstract_escaped.replace('}', r'\}')
    # Undo escaping for LaTeX braces we want to keep
    abstract_escaped = abstract_escaped.replace(r'\\{', r'\{')
    abstract_escaped = abstract_escaped.replace(r'\\}', r'\}')

    # Find position to insert (before last closing brace)
    last_brace = entry.rfind('}')
    if last_brace > 0:
        # Check if there's already a trailing comma
        before_brace = entry[:last_brace].rstrip()
        if not before_brace.endswith(','):
            insert_text = f',\n  abstract = {{{abstract}}}'
        else:
            insert_text = f'\n  abstract = {{{abstract}}},'

        # Insert before the last closing brace
        return entry[:last_brace] + insert_text + '\n' + entry[last_brace:]

    return entry

def main():
    # Paths
    base_path = Path(__file__).parent.parent
    abstracts_path = base_path / 'data' / 'swsm-abstracts.json'
    bib_path = base_path / 'bibliography' / 'bcm_master.bib'

    print("=" * 60)
    print("ADDING ABSTRACTS TO bcm_master.bib")
    print("=" * 60)

    # Load abstracts
    abstracts = load_abstracts(abstracts_path)
    print(f"\nLoaded {len(abstracts)} author abstracts")

    # Load bibliography
    with open(bib_path, 'r', encoding='utf-8', errors='ignore') as f:
        bib_content = f.read()

    print(f"Loaded bibliography ({len(bib_content):,} characters)")

    # Track changes
    updated_count = 0
    not_found = []

    for author, papers in abstracts.items():
        if not papers:
            continue

        paper = papers[0]  # First paper for each author
        mapping = PAPER_MAPPING.get(author)

        if not mapping:
            print(f"\n{author}: No mapping defined")
            not_found.append(author)
            continue

        print(f"\n{author}: Looking for {mapping['key_pattern']}")

        key, start, end = find_entry_position(bib_content, mapping['key_pattern'])

        if key:
            print(f"  Found: {key}")
            entry = bib_content[start:end]

            if 'abstract' in entry.lower():
                print("  (abstract already exists, skipping)")
                continue

            # Add abstract
            new_entry = add_abstract_to_entry(entry, paper['abstract'])
            bib_content = bib_content[:start] + new_entry + bib_content[end:]
            updated_count += 1
            print(f"  Added abstract ({paper['abstract_words']} words)")
        else:
            print(f"  NOT FOUND")
            not_found.append(author)

    # Save updated bibliography
    with open(bib_path, 'w', encoding='utf-8') as f:
        f.write(bib_content)

    print("\n" + "=" * 60)
    print(f"SUMMARY: Updated {updated_count} entries")
    if not_found:
        print(f"Not found: {', '.join(not_found)}")
    print("=" * 60)

if __name__ == '__main__':
    main()
