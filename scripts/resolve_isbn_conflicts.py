#!/usr/bin/env python3
"""Resolve ISBN merge conflicts by keeping the main branch version (API-fetched)."""

import os
import re
from pathlib import Path

def resolve_conflict(filepath):
    """Resolve conflict by keeping the origin/main version (API-fetched ISBN)."""
    with open(filepath, 'r') as f:
        content = f.read()

    if '<<<<<<<' not in content:
        return False

    # Pattern to match conflict markers around isbn line
    pattern = r'<<<<<<< HEAD\nisbn: ([^\n]+)\n=======\nisbn: ([^\n]+)\n>>>>>>> origin/main'

    def replace_conflict(match):
        head_isbn = match.group(1)
        main_isbn = match.group(2)
        # Keep main branch ISBN (API-fetched is more reliable)
        return f'isbn: {main_isbn}'

    new_content = re.sub(pattern, replace_conflict, content)

    if new_content != content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        return True
    return False

def main():
    paper_dir = Path('data/paper-references')
    resolved = 0

    for yaml_file in sorted(paper_dir.glob('PAP-*.yaml')):
        if resolve_conflict(yaml_file):
            print(f"Resolved: {yaml_file.name}")
            resolved += 1

    print(f"\nResolved {resolved} conflicts")

if __name__ == "__main__":
    main()
