#!/usr/bin/env python3
"""
Generate Chapter-Appendix Tables from SSOT YAML

This script generates LaTeX tables from chapter-appendix-mapping.yaml.
It can update specific sections in 00_appendix_index.tex or generate
standalone files.

Usage:
    python scripts/generate_chapter_tables.py                    # Preview
    python scripts/generate_chapter_tables.py --update           # Update index
    python scripts/generate_chapter_tables.py --output tables.tex # Standalone

The YAML file is the Single Source of Truth (SSOT).
"""

import os
import sys
import re
import yaml
import argparse
from datetime import datetime
from collections import defaultdict


# =============================================================================
# CONFIGURATION
# =============================================================================

YAML_PATH = "docs/frameworks/chapter-appendix-mapping.yaml"
INDEX_PATH = "appendices/00_appendix_index.tex"
CHAPTER_INDEX_PATH = "chapters/00_chapter_index.tex"


# =============================================================================
# LOADERS
# =============================================================================

def load_yaml():
    """Load the YAML mapping file."""
    if not os.path.exists(YAML_PATH):
        print(f"ERROR: YAML file not found: {YAML_PATH}")
        sys.exit(1)

    with open(YAML_PATH, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


# =============================================================================
# GENERATORS
# =============================================================================

def generate_chapter_table(data):
    """Generate the main chapters table."""
    lines = []
    lines.append(r"\begin{table}[htbp]")
    lines.append(r"\centering")
    lines.append(r"\caption{EBF Main Document Chapters}")
    lines.append(r"\label{tab:main-chapters}")
    lines.append(r"\renewcommand{\arraystretch}{1.2}")
    lines.append(r"\small")
    lines.append(r"\begin{tabular}{@{}clp{6cm}@{}}")
    lines.append(r"\toprule")
    lines.append(r"\textbf{Ch.} & \textbf{Title} & \textbf{Core Content} \\")
    lines.append(r"\midrule")

    for ch in data.get('chapters', []):
        num = ch['number']
        title = ch['title']
        content = ch.get('core_content', '')
        # Escape special LaTeX characters
        content = content.replace('&', r'\&').replace('_', r'\_')
        content = content.replace('$', r'\$').replace('%', r'\%')
        lines.append(f"{num} & {title} & {content} \\\\")

    lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}")
    lines.append(r"\end{table}")

    return '\n'.join(lines)


def generate_appendix_chapter_matrix(data):
    """Generate the complete appendix-chapter mapping longtable."""
    lines = []
    lines.append(r"\begin{longtable}{@{}llll@{}}")
    lines.append(r"\caption{All Appendices: Chapter Linkages}")
    lines.append(r"\label{tab:all-chapter-mapping} \\")
    lines.append(r"\toprule")
    lines.append(r"\textbf{Code} & \textbf{Appendix Name} & \textbf{Primary Ch.} & \textbf{Secondary} \\")
    lines.append(r"\midrule")
    lines.append(r"\endfirsthead")
    lines.append(r"\multicolumn{4}{c}{\tablename\ \thetable{} -- continued} \\")
    lines.append(r"\toprule")
    lines.append(r"\textbf{Code} & \textbf{Appendix Name} & \textbf{Primary Ch.} & \textbf{Secondary} \\")
    lines.append(r"\midrule")
    lines.append(r"\endhead")
    lines.append(r"\midrule")
    lines.append(r"\multicolumn{4}{r}{Continued...} \\")
    lines.append(r"\endfoot")
    lines.append(r"\bottomrule")
    lines.append(r"\endlastfoot")
    lines.append("")

    # Group by category
    by_category = defaultdict(list)
    for app in data.get('appendices', []):
        by_category[app['category']].append(app)

    category_order = ['CORE', 'FORMAL', 'DOMAIN', 'CONTEXT', 'METHOD', 'PREDICT', 'LIT', 'REF']

    for cat in category_order:
        apps = by_category.get(cat, [])
        if not apps:
            continue

        count = len(apps)
        lines.append(rf"\multicolumn{{4}}{{@{{}}l}}{{\textit{{\textbf{{{cat} ({count})}}}}}} \\")

        for app in apps:
            code = app['code']
            name = f"{app['category']}-{app['name']}"
            primary = app.get('primary_chapter', '---')
            if primary is None:
                primary = '---'
            secondary = app.get('secondary_chapters', [])
            sec_str = ', '.join(f"Ch. {s}" for s in secondary) if secondary else '---'

            # Escape underscores
            name = name.replace('_', r'\_')

            lines.append(f"{code} & {name} & Ch. {primary} & {sec_str} \\\\")

        lines.append(r"\addlinespace")
        lines.append("")

    lines.append(r"\end{longtable}")

    return '\n'.join(lines)


def generate_category_counts(data):
    """Generate the category counts table."""
    by_category = defaultdict(int)
    for app in data.get('appendices', []):
        by_category[app['category']] += 1

    lines = []
    lines.append(r"\begin{table}[htbp]")
    lines.append(r"\centering")
    lines.append(r"\caption{Appendix Categories Overview}")
    lines.append(r"\label{tab:index-categories}")
    lines.append(r"\renewcommand{\arraystretch}{1.4}")
    lines.append(r"\begin{tabular}{@{}clcl@{}}")
    lines.append(r"\toprule")
    lines.append(r"\textbf{Prefix} & \textbf{Category} & \textbf{Count} & \textbf{Purpose} \\")
    lines.append(r"\midrule")

    category_info = {
        'CORE': ('Core Theory', 'Fundamental building blocks of EBF (10C + Hierarchy + EIT)'),
        'FORMAL': ('Formalization', 'Mathematical foundations and proofs'),
        'DOMAIN': ('Application Domains', 'Economics subfield applications'),
        'CONTEXT': ('Context Dimensions', r'The $\Psi$ framework components'),
        'METHOD': ('Methodology', 'Estimation and validation methods'),
        'PREDICT': ('Predictions', 'Falsifiable predictions and cases'),
        'LIT': ('Literature', 'Research integration by author'),
        'REF': ('Reference', 'Glossaries, examples, meta-theory'),
    }

    total = 0
    for cat in ['CORE', 'FORMAL', 'DOMAIN', 'CONTEXT', 'METHOD', 'PREDICT', 'LIT', 'REF']:
        count = by_category.get(cat, 0)
        total += count
        name, purpose = category_info.get(cat, (cat, ''))
        lines.append(rf"\textbf{{{cat}-}} & {name} & {count} & {purpose} \\")

    lines.append(r"\midrule")
    lines.append(rf"& \textbf{{Total}} & \textbf{{{total}}} & \\")
    lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}")
    lines.append(r"\end{table}")

    return '\n'.join(lines)


# =============================================================================
# CHAPTER-SPECIFIC GENERATORS
# =============================================================================

def generate_chapter_types_table(data):
    """Generate the chapter types distribution table."""
    chapters = data.get('chapters', [])

    # Count by type
    by_type = defaultdict(list)
    for ch in chapters:
        ch_type = ch.get('type', 'B')
        by_type[ch_type].append(str(ch['number']))

    lines = []
    lines.append(r"\begin{table}[htbp]")
    lines.append(r"\centering")
    lines.append(r"\caption{Chapter Types Distribution}")
    lines.append(r"\label{tab:chapter-types}")
    lines.append(r"\renewcommand{\arraystretch}{1.4}")
    lines.append(r"\begin{tabular}{@{}clcl@{}}")
    lines.append(r"\toprule")
    lines.append(r"\textbf{Type} & \textbf{Name} & \textbf{Count} & \textbf{Chapters} \\")
    lines.append(r"\midrule")

    type_names = {'A': 'CORE', 'B': 'Foundation', 'C': 'Application'}
    total = 0

    for t in ['A', 'B', 'C']:
        chs = by_type.get(t, [])
        count = len(chs)
        total += count
        name = type_names.get(t, t)
        ch_list = ', '.join(chs) if chs else '---'
        lines.append(rf"\textbf{{{t}}} & {name} & {count} & {ch_list} \\")

    lines.append(r"\midrule")
    lines.append(rf"& \textbf{{Total}} & \textbf{{{total}}} & \\")
    lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}")
    lines.append(r"\end{table}")

    return '\n'.join(lines)


def generate_core_chapters_table(data):
    """Generate the CORE chapters with their appendices table."""
    chapters = data.get('chapters', [])
    appendices = data.get('appendices', [])

    # Build appendix lookup
    app_by_code = {app['code']: app for app in appendices}

    # Find CORE chapters (type A)
    core_chapters = [ch for ch in chapters if ch.get('type') == 'A']

    # 10C question mapping
    question_map = {
        'B': ('HOW', r'$\gamma$ interactions'),
        'V': ('WHEN', r'$\Psi$ framework'),
        'C': ('WHAT', r'Dimensions $d$'),
        'AU': ('AWARE', r'$A(\cdot)$ function'),
        'AV': ('READY', r'$WAX, \theta$'),
        'AW': ('STAGE', r'Phase $\varphi$'),
    }

    lines = []
    lines.append(r"\begin{table}[htbp]")
    lines.append(r"\centering")
    lines.append(r"\caption{CORE Chapters and Their Primary Appendices}")
    lines.append(r"\label{tab:core-chapters}")
    lines.append(r"\renewcommand{\arraystretch}{1.4}")
    lines.append(r"\begin{tabular}{@{}cllll@{}}")
    lines.append(r"\toprule")
    lines.append(r"\textbf{Ch.} & \textbf{Title} & \textbf{10C Question} & \textbf{CORE Appendix} & \textbf{Defines} \\")
    lines.append(r"\midrule")

    for ch in sorted(core_chapters, key=lambda x: int(x['number']) if str(x['number']).isdigit() else 99):
        num = ch['number']
        title = ch['title']
        core_app = ch.get('core_appendix', '---')

        if core_app in question_map:
            question, defines = question_map[core_app]
            app_name = f"{core_app} (CORE-{question})"
        else:
            question = '---'
            defines = '---'
            app_name = core_app

        lines.append(f"{num} & {title} & {question} & {app_name} & {defines} \\\\")

    lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}")
    lines.append(r"\end{table}")

    return '\n'.join(lines)


def generate_chapter_list_table(data):
    """Generate the complete chapter list with types."""
    chapters = data.get('chapters', [])

    lines = []
    lines.append(r"\begin{table}[htbp]")
    lines.append(r"\centering")
    lines.append(r"\caption{EBF Main Document Chapters}")
    lines.append(r"\label{tab:main-chapters-index}")
    lines.append(r"\renewcommand{\arraystretch}{1.2}")
    lines.append(r"\small")
    lines.append(r"\begin{tabular}{@{}cclp{5cm}@{}}")
    lines.append(r"\toprule")
    lines.append(r"\textbf{Ch.} & \textbf{Type} & \textbf{Title} & \textbf{Core Content} \\")
    lines.append(r"\midrule")

    for ch in chapters:
        num = ch['number']
        ch_type = ch.get('type', 'B')
        title = ch['title']
        content = ch.get('core_content', '')
        # Escape special LaTeX characters
        content = content.replace('&', r'\&').replace('_', r'\_')
        content = content.replace('$', r'\$').replace('%', r'\%')
        lines.append(f"{num} & {ch_type} & {title} & {content} \\\\")

    lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}")
    lines.append(r"\end{table}")

    return '\n'.join(lines)


def generate_prerequisites_table(data):
    """Generate the chapter prerequisites matrix."""
    # This is a simplified static table - can be enhanced with YAML data
    lines = []
    lines.append(r"\begin{table}[htbp]")
    lines.append(r"\centering")
    lines.append(r"\caption{Chapter Prerequisites Matrix}")
    lines.append(r"\label{tab:prerequisites}")
    lines.append(r"\renewcommand{\arraystretch}{1.3}")
    lines.append(r"\small")
    lines.append(r"\begin{tabular}{@{}clll@{}}")
    lines.append(r"\toprule")
    lines.append(r"\textbf{Ch.} & \textbf{Title} & \textbf{Prerequisites} & \textbf{Recommended} \\")
    lines.append(r"\midrule")

    # Define prerequisites (could be enhanced to read from YAML)
    prereqs = [
        ("1--4", "Foundation I", "None", "---"),
        ("4x", "Calibration", "Ch. 4", "Ch. 8"),
        ("5", "Complementarity", "Ch. 1--3", "Ch. 4"),
        ("6--8", "Foundation II", "Ch. 1--5", "---"),
        ("9", "Context", "Ch. 5", "Ch. 6--8"),
        ("10", "Utility Architecture", "Ch. 5, 9", "All foundations"),
        ("11", "Awareness", "Ch. 10", "Ch. 9"),
        ("12", "Willingness", "Ch. 10, 11", "---"),
        ("13", "BCJ", "Ch. 10--12", "---"),
        ("14", "Segments", "Ch. 13", "Ch. 10"),
        ("15--16", "Synthesis", "Ch. 13, 14", "---"),
        ("17", "Interventions", "Ch. 13, 14", "Ch. 10"),
        ("18", "Journey-Integrated", "Ch. 13, 17", "---"),
        ("19", "Segment-Specific", "Ch. 14, 17", "Ch. 18"),
        ("20--21", "Portfolios", "Ch. 17--19", "---"),
        ("22--24", "Advanced Applications", "Ch. 17--21", "All previous"),
    ]

    for ch, title, prereq, rec in prereqs:
        lines.append(f"{ch} & {title} & {prereq} & {rec} \\\\")

    lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}")
    lines.append(r"\end{table}")

    return '\n'.join(lines)


def update_chapter_index_file(data):
    """Update specific sections in the chapter index file."""
    if not os.path.exists(CHAPTER_INDEX_PATH):
        print(f"ERROR: Chapter index file not found: {CHAPTER_INDEX_PATH}")
        return False

    with open(CHAPTER_INDEX_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    updated_count = 0

    # Update chapter types table
    types_table = generate_chapter_types_table(data)
    pattern_types = r"(\\begin\{table\}\[htbp\]\s*\\centering\s*\\caption\{Chapter Types Distribution\}\s*\\label\{tab:chapter-types\}.*?\\end\{table\})"
    if re.search(pattern_types, content, re.DOTALL):
        content = re.sub(pattern_types, lambda m: types_table, content, count=1, flags=re.DOTALL)
        print("  ✓ Updated: Chapter Types Distribution table")
        updated_count += 1
    else:
        print("  ⚠ WARNING: Could not find Chapter Types Distribution table to update")

    # Update CORE chapters table
    core_table = generate_core_chapters_table(data)
    pattern_core = r"(\\begin\{table\}\[htbp\]\s*\\centering\s*\\caption\{CORE Chapters and Their Primary Appendices\}\s*\\label\{tab:core-chapters\}.*?\\end\{table\})"
    if re.search(pattern_core, content, re.DOTALL):
        content = re.sub(pattern_core, lambda m: core_table, content, count=1, flags=re.DOTALL)
        print("  ✓ Updated: CORE Chapters table")
        updated_count += 1
    else:
        print("  ⚠ WARNING: Could not find CORE Chapters table to update")

    # Update main chapters list
    chapters_table = generate_chapter_list_table(data)
    pattern_chapters = r"(\\begin\{table\}\[htbp\]\s*\\centering\s*\\caption\{EBF Main Document Chapters\}\s*\\label\{tab:main-chapters-index\}.*?\\end\{table\})"
    if re.search(pattern_chapters, content, re.DOTALL):
        content = re.sub(pattern_chapters, lambda m: chapters_table, content, count=1, flags=re.DOTALL)
        print("  ✓ Updated: Main Chapters table")
        updated_count += 1
    else:
        print("  ⚠ WARNING: Could not find Main Chapters table to update")

    # Update prerequisites table
    prereqs_table = generate_prerequisites_table(data)
    pattern_prereqs = r"(\\begin\{table\}\[htbp\]\s*\\centering\s*\\caption\{Chapter Prerequisites Matrix\}\s*\\label\{tab:prerequisites\}.*?\\end\{table\})"
    if re.search(pattern_prereqs, content, re.DOTALL):
        content = re.sub(pattern_prereqs, lambda m: prereqs_table, content, count=1, flags=re.DOTALL)
        print("  ✓ Updated: Prerequisites Matrix table")
        updated_count += 1
    else:
        print("  ⚠ WARNING: Could not find Prerequisites Matrix table to update")

    # Update total counts in header
    total_chapters = len(data.get('chapters', []))
    content = re.sub(
        r'Total Chapters:\} & \d+',
        f'Total Chapters:}} & {total_chapters}',
        content
    )

    with open(CHAPTER_INDEX_PATH, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  ✓ Updated chapter count: {total_chapters}")
    print(f"Updated: {CHAPTER_INDEX_PATH}")
    return True


def generate_all_tables(data):
    """Generate all tables."""
    parts = []
    parts.append("% " + "=" * 75)
    parts.append("% AUTO-GENERATED FROM chapter-appendix-mapping.yaml")
    parts.append(f"% Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    parts.append("% DO NOT EDIT MANUALLY - Edit the YAML file instead")
    parts.append("% " + "=" * 75)
    parts.append("")
    parts.append("% --- Category Counts ---")
    parts.append(generate_category_counts(data))
    parts.append("")
    parts.append("% --- Main Chapters ---")
    parts.append(generate_chapter_table(data))
    parts.append("")
    parts.append("% --- Appendix-Chapter Matrix ---")
    parts.append(generate_appendix_chapter_matrix(data))

    return '\n'.join(parts)


# =============================================================================
# UPDATER
# =============================================================================

def update_index_file(data):
    """Update specific sections in the appendix index file."""
    if not os.path.exists(INDEX_PATH):
        print(f"ERROR: Index file not found: {INDEX_PATH}")
        return False

    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    updated_count = 0

    # Update the category counts table
    # Use label as unique identifier to avoid matching wrong tables
    category_table = generate_category_counts(data)
    pattern_cat = r"(\\begin\{table\}\[htbp\]\s*\\centering\s*\\caption\{Appendix Categories Overview\}\s*\\label\{tab:index-categories\}.*?\\end\{table\})"
    if re.search(pattern_cat, content, re.DOTALL):
        # Use lambda to avoid regex backreference issues with backslashes
        content = re.sub(pattern_cat, lambda m: category_table, content, count=1, flags=re.DOTALL)
        print("  ✓ Updated: Category Counts table")
        updated_count += 1
    else:
        print("  ⚠ WARNING: Could not find Category Counts table to update")

    # Update the main chapters table
    chapter_table = generate_chapter_table(data)
    pattern = r"(\\begin\{table\}\[htbp\]\s*\\centering\s*\\caption\{EBF Main Document Chapters\}\s*\\label\{tab:main-chapters\}.*?\\end\{table\})"
    if re.search(pattern, content, re.DOTALL):
        # Use lambda to avoid regex backreference issues with backslashes
        content = re.sub(pattern, lambda m: chapter_table, content, count=1, flags=re.DOTALL)
        print("  ✓ Updated: Main Chapters table")
        updated_count += 1
    else:
        print("  ⚠ WARNING: Could not find Main Chapters table to update")

    # Calculate actual counts from YAML
    by_category = defaultdict(int)
    for app in data.get('appendices', []):
        by_category[app['category']] += 1
    total_appendices = sum(by_category.values())
    total_chapters = len(data.get('chapters', []))

    # Update abstract and header references
    content = re.sub(
        r'supported by \d+ appendices',
        f'supported by {total_appendices} appendices',
        content
    )
    content = re.sub(
        r'All appendices \(\d+\)',
        f'All appendices ({total_appendices})',
        content
    )
    content = re.sub(
        r'All chapters \(\d+\)',
        f'All chapters ({total_chapters})',
        content
    )
    content = re.sub(
        r'Main Chapters\}\s*\(1--\d+\)',
        f'Main Chapters}} (1--{total_chapters})',
        content
    )
    content = re.sub(
        r'Appendices\}\s*\(\d+\)',
        f'Appendices}} ({total_appendices})',
        content
    )

    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  ✓ Updated counts: {total_appendices} appendices, {total_chapters} chapters")
    print(f"Updated: {INDEX_PATH}")
    return True


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description='Generate chapter tables from YAML')
    parser.add_argument('--update', action='store_true',
                        help='Update the appendix index file')
    parser.add_argument('--update-chapters', action='store_true',
                        help='Update the chapter index file')
    parser.add_argument('--update-all', action='store_true',
                        help='Update both appendix and chapter index files')
    parser.add_argument('--output', '-o', type=str,
                        help='Output to standalone file')
    args = parser.parse_args()

    data = load_yaml()

    if args.update_all:
        # Update both index files
        print("=" * 70)
        print("UPDATING ALL INDEX FILES")
        print("=" * 70)
        success1 = update_index_file(data)
        print()
        success2 = update_chapter_index_file(data)
        return 0 if (success1 and success2) else 1

    elif args.update:
        success = update_index_file(data)
        return 0 if success else 1

    elif args.update_chapters:
        success = update_chapter_index_file(data)
        return 0 if success else 1

    elif args.output:
        tables = generate_all_tables(data)
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(tables)
        print(f"Generated: {args.output}")
        return 0

    else:
        # Preview mode
        print("=" * 70)
        print("CHAPTER-APPENDIX TABLE GENERATOR")
        print("=" * 70)
        print(f"Source: {YAML_PATH}")
        print(f"Chapters: {len(data.get('chapters', []))}")
        print(f"Appendices: {len(data.get('appendices', []))}")
        print()
        print("Options:")
        print("  --update           Update appendix index file")
        print("  --update-chapters  Update chapter index file")
        print("  --update-all       Update both index files")
        print("  --output FILE      Generate standalone tables")
        print()
        print("--- Preview (Category Counts) ---")
        print(generate_category_counts(data)[:500] + "...")
        return 0


if __name__ == '__main__':
    sys.exit(main())
