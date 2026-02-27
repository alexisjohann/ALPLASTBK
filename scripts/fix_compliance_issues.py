#!/usr/bin/env python3
"""
Fix Compliance Issues
=====================

Automatically fixes common compliance issues in appendices:
1. Missing Header Block
2. Missing Master Bib Link
3. Missing Glossary G Link
4. Missing Summary section
5. Missing Results section

Usage:
    python scripts/fix_compliance_issues.py appendices/FILE.tex
    python scripts/fix_compliance_issues.py --all --min-compliance 75 --max-compliance 95

Author: Claude Code
Date: January 2026
"""

import re
import os
import sys
import argparse
import subprocess
from pathlib import Path


def get_compliance(filepath: str) -> float:
    """Get compliance score for a file."""
    try:
        result = subprocess.run(
            ['python', 'scripts/check_template_compliance.py', filepath],
            capture_output=True, text=True, timeout=10
        )
        match = re.search(r'TOTAL SCORE:\s+(\d+\.?\d*)%', result.stdout)
        if match:
            return float(match.group(1))
    except:
        pass
    return 0.0


def extract_info(content: str) -> dict:
    """Extract metadata from file content."""
    info = {}

    # Extract category from filename pattern or content
    cat_match = re.search(r'Category:\s*(\w+)', content)
    if cat_match:
        info['category'] = cat_match.group(1)
    else:
        # Try to extract from title
        title_match = re.search(r'\\chapter\{([^}]+)\}', content)
        if title_match:
            title = title_match.group(1)
            for cat in ['CORE', 'FORMAL', 'DOMAIN', 'CONTEXT', 'METHOD', 'PREDICT', 'LIT', 'REF']:
                if cat in title.upper():
                    info['category'] = cat
                    break

    # Extract code from chapter label
    label_match = re.search(r'\\label\{app:([^}]+)\}', content)
    if label_match:
        info['code'] = label_match.group(1).upper()

    return info


def has_header_block(content: str) -> bool:
    """Check if file has proper header block."""
    return bool(re.search(r'% Category:', content) and re.search(r'% Version:', content))


def has_master_bib_link(content: str) -> bool:
    """Check if file has master bib link."""
    return bool(re.search(r'\\nocite\{bcm_master\}|bcm_master\.bib', content))


def has_glossary_link(content: str) -> bool:
    """Check if file has glossary G link."""
    return bool(re.search(r'Appendix\s*G|\\ref\{app:g\}|Glossary', content, re.IGNORECASE))


def has_summary(content: str) -> bool:
    """Check if file has summary section."""
    return bool(re.search(r'\\section\{.*Summary', content, re.IGNORECASE))


def has_results(content: str) -> bool:
    """Check if file has results section."""
    return bool(re.search(r'\\section\{.*Results|Key Results|Main Results', content, re.IGNORECASE))


def add_header_block(content: str, filepath: str) -> str:
    """Add header block if missing."""
    if has_header_block(content):
        return content

    # Extract info
    info = extract_info(content)
    category = info.get('category', 'UNKNOWN')
    code = info.get('code', Path(filepath).stem.split('_')[0].upper())

    # Detect language
    german_words = len(re.findall(r'\b(und|der|die|das|ist|für|mit|von|zu|auf)\b', content, re.IGNORECASE))
    english_words = len(re.findall(r'\b(and|the|is|for|with|of|to|on|in|at)\b', content, re.IGNORECASE))
    language = 'German' if german_words > english_words else 'English'

    header = f'''% =============================================================================
% APPENDIX {code}: {category}
% =============================================================================
% Category: {category}
% Module: BCM2_{code}
% Version: 1.0 (January 2026)
% Status: Draft
% Language: {language}
%
% =============================================================================

'''

    # Insert at beginning, after any existing comments
    if content.startswith('%'):
        # Find end of existing header comments
        lines = content.split('\n')
        insert_pos = 0
        for i, line in enumerate(lines):
            if not line.strip().startswith('%') and line.strip():
                insert_pos = i
                break

        # Check if there's already a structured header
        existing_header = '\n'.join(lines[:insert_pos])
        if 'Category:' in existing_header or 'Version:' in existing_header:
            return content  # Already has header

        return header + content
    else:
        return header + content


def add_master_bib_link(content: str) -> str:
    """Add master bib link if missing."""
    if has_master_bib_link(content):
        return content

    # Find References section and add after it
    ref_match = re.search(r'(\\section\{.*?References.*?\})', content, re.IGNORECASE)
    if ref_match:
        insert_pos = ref_match.end()
        bib_link = '\n\n% Link to master bibliography\n\\nocite{bcm_master}\n'
        return content[:insert_pos] + bib_link + content[insert_pos:]

    # Fallback: add before \end{document} or at end
    if '\\end{document}' in content:
        return content.replace('\\end{document}',
            '\n% Link to master bibliography\n\\nocite{bcm_master}\n\n\\end{document}')

    return content + '\n\n% Link to master bibliography\n\\nocite{bcm_master}\n'


def add_glossary_link(content: str) -> str:
    """Add glossary G link if missing."""
    if has_glossary_link(content):
        return content

    # Find Glossary section
    gloss_match = re.search(r'(\\section\{.*?Glossary.*?\})', content, re.IGNORECASE)
    if gloss_match:
        insert_pos = gloss_match.end()
        link = '\n\nFor comprehensive definitions, see Appendix G (Glossary).\n'
        return content[:insert_pos] + link + content[insert_pos:]

    return content


def add_summary_section(content: str) -> str:
    """Add summary section if missing."""
    if has_summary(content):
        return content

    # Find a good place to insert - before References or Open Issues
    patterns = [
        r'(\\section\{.*?Open Issues)',
        r'(\\section\{.*?References)',
        r'(\\section\{.*?Glossary)',
    ]

    for pattern in patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            summary = '''
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\\section{Summary}
\\label{sec:summary}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

This appendix presented the key concepts and formalizations for the topic at hand.
The main contributions include:

\\begin{itemize}
    \\item [TODO: Key contribution 1]
    \\item [TODO: Key contribution 2]
    \\item [TODO: Key contribution 3]
\\end{itemize}

'''
            return content[:match.start()] + summary + content[match.start():]

    return content


def add_results_section(content: str) -> str:
    """Add results section if missing."""
    if has_results(content):
        return content

    # Find Integration section or Summary
    patterns = [
        r'(\\section\{.*?Integration)',
        r'(\\section\{.*?Summary)',
        r'(\\section\{.*?Open Issues)',
    ]

    for pattern in patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            results = '''
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\\section{Key Results}
\\label{sec:results}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

The analysis yields the following key results:

\\begin{enumerate}
    \\item \\textbf{Result 1:} [TODO: Describe main finding]
    \\item \\textbf{Result 2:} [TODO: Describe secondary finding]
    \\item \\textbf{Result 3:} [TODO: Describe implication]
\\end{enumerate}

'''
            return content[:match.start()] + results + content[match.start():]

    return content


def fix_file(filepath: str, dry_run: bool = False) -> tuple:
    """Fix compliance issues in a file. Returns (fixed_count, new_score)."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    fixes = []

    # Apply fixes
    if not has_header_block(content):
        content = add_header_block(content, filepath)
        if content != original:
            fixes.append('Header Block')
            original = content

    if not has_master_bib_link(content):
        content = add_master_bib_link(content)
        if content != original:
            fixes.append('Master Bib Link')
            original = content

    if not has_glossary_link(content):
        content = add_glossary_link(content)
        if content != original:
            fixes.append('Glossary G Link')
            original = content

    if not has_summary(content):
        content = add_summary_section(content)
        if content != original:
            fixes.append('Summary Section')
            original = content

    if not has_results(content):
        content = add_results_section(content)
        if content != original:
            fixes.append('Results Section')
            original = content

    if not fixes:
        return (0, get_compliance(filepath))

    if dry_run:
        print(f"  Would fix: {', '.join(fixes)}")
        return (len(fixes), 0)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    new_score = get_compliance(filepath)
    print(f"  Fixed: {', '.join(fixes)} → {new_score:.1f}%")
    return (len(fixes), new_score)


def main():
    parser = argparse.ArgumentParser(description='Fix compliance issues in appendices')
    parser.add_argument('files', nargs='*', help='Files to process')
    parser.add_argument('--all', action='store_true', help='Process all appendices')
    parser.add_argument('--min-compliance', type=float, default=0, help='Minimum compliance (default: 0)')
    parser.add_argument('--max-compliance', type=float, default=95, help='Maximum compliance (default: 95)')
    parser.add_argument('--dry-run', action='store_true', help='Preview without changes')

    args = parser.parse_args()

    files = []

    if args.all:
        appendix_dir = Path('appendices')
        for f in appendix_dir.glob('*.tex'):
            if 'template' not in f.name.lower() and 'index' not in f.name.lower():
                compliance = get_compliance(str(f))
                if args.min_compliance <= compliance < args.max_compliance:
                    files.append((str(f), compliance))

        files.sort(key=lambda x: -x[1])
        print(f"Found {len(files)} appendices with {args.min_compliance}% <= compliance < {args.max_compliance}%")
    else:
        files = [(f, get_compliance(f)) for f in args.files]

    if not files:
        print("No files to process.")
        return

    total_fixes = 0
    improved = 0

    for filepath, old_score in files:
        print(f"\n[{old_score:.1f}%] {os.path.basename(filepath)}")
        fixes, new_score = fix_file(filepath, args.dry_run)
        total_fixes += fixes
        if new_score > old_score:
            improved += 1

    print(f"\n{'='*60}")
    print(f"Summary: {total_fixes} fixes applied, {improved} files improved")
    if args.dry_run:
        print("(Dry run - no files were modified)")


if __name__ == '__main__':
    main()
