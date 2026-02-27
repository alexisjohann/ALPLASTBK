#!/usr/bin/env python3
"""Consolidate PAP-manual-* entries into their canonical counterparts.

For each manual-N paper:
1. Rename .md file to canonical key
2. Update canonical YAML with full_text reference
3. Remove manual-N YAML and .md

Usage:
    python scripts/consolidate_manual_papers.py          # dry-run
    python scripts/consolidate_manual_papers.py --execute # do it
"""

import argparse
import os
import re
import shutil
from datetime import date

MAPPING = {
    'manual-1': 'herd2025administrative',
    'manual-2': 'francis2025merger',
    'manual-3': 'schmidt2025did',
    'manual-4': 'shapiro2025acquisitions',
    'manual-5': 'howard2025two',
    'manual-6': 'slemrod2025tax',
    'manual-7': 'liscow2025getting',
    'manual-8': 'kaplow2025improving',
    'manual-9': 'fudenberg2025philipp',
    'manual-10': 'borusyak2025practical',
}

TEXTS_DIR = "data/paper-texts"
REFS_DIR = "data/paper-references"


def update_yaml_fulltext(yaml_path, md_path, content_level):
    """Update full_text section in canonical YAML."""
    with open(yaml_path, 'r', encoding='utf-8') as f:
        content = f.read()

    today = date.today().isoformat()

    # Check if full_text section exists
    if 'full_text:' in content:
        # Replace existing full_text block
        content = re.sub(
            r'full_text:\n(?:  .*\n)*',
            f'full_text:\n'
            f'  available: true\n'
            f'  path: "{md_path}"\n'
            f'  content_level: {content_level}\n'
            f'  template_available: false\n'
            f'  template_char_count: 0\n'
            f'  archived_date: "{today}"\n',
            content
        )
    else:
        # Append full_text section
        content += (
            f'\nfull_text:\n'
            f'  available: true\n'
            f'  path: "{md_path}"\n'
            f'  content_level: {content_level}\n'
            f'  template_available: false\n'
            f'  template_char_count: 0\n'
            f'  archived_date: "{today}"\n'
        )

    with open(yaml_path, 'w', encoding='utf-8') as f:
        f.write(content)


def get_content_level(md_path):
    """Determine content level from .md file."""
    with open(md_path, 'r', encoding='utf-8') as f:
        text = f.read()
    word_count = len(text.split())
    if word_count > 5000:
        return 'L3'
    elif word_count > 500:
        return 'L2'
    return 'L1'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()

    for manual_key, canonical_key in MAPPING.items():
        manual_md = os.path.join(TEXTS_DIR, f"PAP-{manual_key}.md")
        manual_yaml = os.path.join(REFS_DIR, f"PAP-{manual_key}.yaml")
        canonical_md = os.path.join(TEXTS_DIR, f"PAP-{canonical_key}.md")
        canonical_yaml = os.path.join(REFS_DIR, f"PAP-{canonical_key}.yaml")

        if not os.path.exists(manual_md):
            print(f"  SKIP {manual_key}: no .md file")
            continue
        if not os.path.exists(canonical_yaml):
            print(f"  SKIP {manual_key}: canonical YAML {canonical_yaml} not found")
            continue

        content_level = get_content_level(manual_md)

        if args.execute:
            # 1. Copy .md to canonical name
            shutil.copy2(manual_md, canonical_md)
            print(f"  COPY {manual_md} → {canonical_md}")

            # 2. Update canonical YAML
            update_yaml_fulltext(canonical_yaml, canonical_md, content_level)
            print(f"  UPDATE {canonical_yaml} (full_text.available=true, {content_level})")

            # 3. Remove manual files
            os.remove(manual_md)
            print(f"  DELETE {manual_md}")
            if os.path.exists(manual_yaml):
                os.remove(manual_yaml)
                print(f"  DELETE {manual_yaml}")
        else:
            print(f"  [DRY-RUN] {manual_key} → {canonical_key} ({content_level})")
            print(f"    COPY {manual_md} → {canonical_md}")
            print(f"    UPDATE {canonical_yaml}")
            if os.path.exists(manual_yaml):
                print(f"    DELETE {manual_yaml}, {manual_md}")

    if not args.execute:
        print(f"\nDry run. Use --execute to consolidate.")
    else:
        print(f"\nConsolidation complete.")


if __name__ == '__main__':
    main()
