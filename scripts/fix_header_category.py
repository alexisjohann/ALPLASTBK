#!/usr/bin/env python3
"""
Fix Header Category
===================

Adds missing Category: and Language: declarations to appendix headers.

Usage:
    python scripts/fix_header_category.py appendices/FILE.tex
    python scripts/fix_header_category.py --all
"""

import re
import sys
from pathlib import Path


def detect_category(filepath: str, content: str) -> str:
    """Detect category from filename or content."""
    fname = Path(filepath).name.upper()

    # From filename pattern
    for cat in ['CORE', 'FORMAL', 'DOMAIN', 'CONTEXT', 'METHOD', 'PREDICT', 'LIT', 'REF']:
        if cat in fname:
            return cat

    # From chapter title
    title_match = re.search(r'\\chapter\{([^}]+)\}', content)
    if title_match:
        title = title_match.group(1).upper()
        for cat in ['CORE', 'FORMAL', 'DOMAIN', 'CONTEXT', 'METHOD', 'PREDICT', 'LIT', 'REF']:
            if cat in title:
                return cat

    # Heuristics based on content patterns
    if re.search(r'LIT-[A-Z]+|Literature', content, re.IGNORECASE):
        return 'LIT'
    if re.search(r'METHOD-|Methodology|Measurement', content, re.IGNORECASE):
        return 'METHOD'
    if re.search(r'DOMAIN-|Application', content, re.IGNORECASE):
        return 'DOMAIN'
    if re.search(r'FORMAL-|Proof|Theorem', content, re.IGNORECASE):
        return 'FORMAL'

    return 'UNKNOWN'


def detect_language(content: str) -> str:
    """Detect language from content."""
    german_words = len(re.findall(r'\b(und|der|die|das|ist|für|mit|von|zu|auf|werden|wird|nicht|sind|auch|als|ein|eine|bei|nach|oder|durch|über|wenn|dass|kann|sein|hat|aus|auf|noch|nur|mehr|aber|wie|sie|wir)\b', content, re.IGNORECASE))
    english_words = len(re.findall(r'\b(the|and|of|to|is|in|that|for|with|as|are|on|be|this|by|from|or|an|which|have|not|at|but|we|can|all|they|been|has|its|more|will|their|was|about|into|than|other|when|there|if)\b', content, re.IGNORECASE))

    return 'German' if german_words > english_words * 1.5 else 'English'


def fix_header(filepath: str) -> bool:
    """Fix header in file. Returns True if fixed."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    has_category = bool(re.search(r'% Category:', content))
    has_language = bool(re.search(r'% Language:', content))

    if has_category and has_language:
        return False  # Already OK

    category = detect_category(filepath, content)
    language = detect_language(content)

    modified = False

    # Add Category: if missing
    if not has_category:
        # Find where to insert - after % Module: or % Version:
        patterns = [
            (r'(% Module:[^\n]*\n)', r'\1% Category: ' + category + '\n'),
            (r'(% Version:[^\n]*\n)', r'\1% Category: ' + category + '\n'),
            (r'(% =+\n% APPENDIX [^\n]+\n% =+\n)', r'\1% Category: ' + category + '\n'),
        ]

        for pattern, replacement in patterns:
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content, count=1)
                modified = True
                break

        if not modified and not has_category:
            # Fallback: add at beginning after first comment block
            if content.startswith('%'):
                lines = content.split('\n')
                insert_idx = 0
                for i, line in enumerate(lines):
                    if line.strip() and not line.startswith('%'):
                        insert_idx = i
                        break
                    if line.startswith('% =') and i > 5:
                        insert_idx = i + 1
                        break
                lines.insert(insert_idx, f'% Category: {category}')
                content = '\n'.join(lines)
                modified = True

    # Add Language: if missing
    if not has_language:
        # Insert after Category: or Status:
        patterns = [
            (r'(% Category:[^\n]*\n)', r'\1% Language: ' + language + '\n'),
            (r'(% Status:[^\n]*\n)', r'\1% Language: ' + language + '\n'),
        ]

        for pattern, replacement in patterns:
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content, count=1)
                modified = True
                break

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed: {filepath} [Category: {category}, Language: {language}]")
        return True

    return False


def main():
    if '--all' in sys.argv:
        appendix_dir = Path('appendices')
        fixed = 0
        for f in sorted(appendix_dir.glob('*.tex')):
            if 'template' not in f.name.lower() and 'index' not in f.name.lower():
                if fix_header(str(f)):
                    fixed += 1
        print(f"\nTotal: {fixed} files fixed")
    else:
        for filepath in sys.argv[1:]:
            fix_header(filepath)


if __name__ == '__main__':
    main()
