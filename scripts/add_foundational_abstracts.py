#!/usr/bin/env python3
"""
Add foundational abstracts to bcm_master.bib
"""

import json
import re
from pathlib import Path

BASE_PATH = Path(__file__).parent.parent
BIB_PATH = BASE_PATH / "bibliography" / "bcm_master.bib"
ABSTRACTS_PATH = BASE_PATH / "data" / "foundational-abstracts.json"

# Mapping from abstract entry to actual BibTeX key patterns
KEY_MAPPING = {
    "PAP-tversky1974judgment": r"PAP-tversky1974judgment",
    "PAP-tversky1981framing": r"PAP-tversky1981framing",
    "PAP-tversky1991loss": r"PAP-tversky1991loss|kahneman1991loss",
    "PAP-tversky1992advances": r"PAP-tversky1992advances",
    "PAP-akerlof1970lemons": r"PAP-akerlof1970lemons",
    "PAP-akerlof2000identity": r"akerlof2000identity|akerlof2010identity",
    "PAP-laibson1997golden": r"laibson1997golden|laibson1997",
    "PAP-rabin2000risk": r"PAP-rabin2000risk|rabin2000risk|rabin2000",
    "PAP-benartzi1995myopic": r"benartzi1995myopic|benartzi1995",
    "PAP-PAP-odonoghue1999doingdoing": r"PAP-odonoghue1999doingdoing|PAP-odonoghue1999doing",
    "PAP-PAP-gaechter2002altruistic": r"PAP-gaechter2002altruistic|fehr2002",
    "PAP-dellavigna2006gym": r"PAP-dellavigna2006paying|dellavigna2006"
}

def escape_latex(text: str) -> str:
    """Escape LaTeX special characters."""
    text = text.replace('&', '\\&')
    text = text.replace('%', '\\%')
    text = text.replace('$', '\\$')
    text = text.replace('#', '\\#')
    text = text.replace('_', '\\_')
    return text

def find_entry(bib_content: str, pattern: str):
    """Find BibTeX entry by key pattern."""
    regex = rf'@\w+\{{({pattern})\s*,'
    match = re.search(regex, bib_content, re.IGNORECASE)
    if match:
        key = match.group(1)
        start = match.start()
        # Find entry end
        brace_count = 0
        for i, c in enumerate(bib_content[start:], start):
            if c == '{':
                brace_count += 1
            elif c == '}':
                brace_count -= 1
                if brace_count == 0:
                    return key, start, i + 1
    return None, -1, -1

def add_abstract(bib_content: str, key: str, start: int, end: int, abstract: str) -> str:
    """Add abstract to entry."""
    entry = bib_content[start:end]

    if 'abstract' in entry.lower():
        return bib_content  # Already has abstract

    abstract_escaped = escape_latex(abstract)

    # Find last } and insert before it
    last_brace = entry.rfind('}')
    if last_brace > 0:
        new_entry = entry[:last_brace] + f',\n  abstract = {{{abstract_escaped}}}\n' + entry[last_brace:]
        return bib_content[:start] + new_entry + bib_content[end:]

    return bib_content

def main():
    print("=" * 60)
    print("ADDING FOUNDATIONAL ABSTRACTS TO bcm_master.bib")
    print("=" * 60)

    # Load abstracts
    with open(ABSTRACTS_PATH, 'r') as f:
        data = json.load(f)

    print(f"Loaded {len(data['abstracts'])} abstracts")

    # Load bibliography
    with open(BIB_PATH, 'r', encoding='utf-8', errors='ignore') as f:
        bib_content = f.read()

    added = 0
    not_found = []

    for item in data['abstracts']:
        bib_key = item['bib_key']
        pattern = KEY_MAPPING.get(bib_key, bib_key)

        key, start, end = find_entry(bib_content, pattern)

        if key:
            old_content = bib_content
            bib_content = add_abstract(bib_content, key, start, end, item['abstract'])
            if bib_content != old_content:
                added += 1
                print(f"✓ {key}: Added ({len(item['abstract'].split())} words)")
            else:
                print(f"- {key}: Already has abstract")
        else:
            not_found.append(item['title'][:40])
            print(f"✗ {bib_key}: Not found in bibliography")

    # Save
    with open(BIB_PATH, 'w', encoding='utf-8') as f:
        f.write(bib_content)

    print("\n" + "=" * 60)
    print(f"Added: {added} abstracts")
    if not_found:
        print(f"Not found: {len(not_found)}")
        for title in not_found:
            print(f"  - {title}...")
    print("=" * 60)

if __name__ == '__main__':
    main()
