#!/usr/bin/env python3
"""
Add Scope Box to Appendices
============================

Automatically generates and inserts Appendix Scope Box based on content analysis.

Usage:
    python scripts/add_scope_box.py appendices/FILE.tex           # Single file
    python scripts/add_scope_box.py --all --min-compliance 90     # All with >=90%
    python scripts/add_scope_box.py --dry-run appendices/FILE.tex # Preview only

Author: Claude Code
Date: January 2026
"""

import re
import os
import sys
import argparse
import subprocess
from pathlib import Path


def extract_title(content: str) -> str:
    """Extract appendix title from \\chapter{} command."""
    match = re.search(r'\\chapter\{([^}]+)\}', content)
    if match:
        return match.group(1).strip()
    return "Unknown Title"


def extract_abstract(content: str) -> str:
    """Extract abstract text."""
    match = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', content, re.DOTALL)
    if match:
        text = match.group(1).strip()
        # Clean LaTeX commands
        text = re.sub(r'\\[a-zA-Z]+\{([^}]*)\}', r'\1', text)
        text = re.sub(r'\\[a-zA-Z]+', '', text)
        return text[:200] + "..." if len(text) > 200 else text
    return ""


def extract_fundamental_question(content: str) -> str:
    """Extract the fundamental question from tcolorbox or section."""
    # Try tcolorbox first
    match = re.search(r'title=.*?Fundamental Question.*?\](.*?)\\end\{tcolorbox\}', content, re.DOTALL)
    if match:
        text = match.group(1).strip()
        # Extract textbf content
        bf_match = re.search(r'\\textbf\{([^}]+)\}', text)
        if bf_match:
            return bf_match.group(1).strip()
    return ""


def extract_sections(content: str) -> list:
    """Extract section titles for In-Scope."""
    sections = []
    for match in re.finditer(r'\\section\{([^}]+)\}', content):
        title = match.group(1).strip()
        # Skip standard sections
        if not any(skip in title.lower() for skip in
                   ['summary', 'glossary', 'reference', 'open issue', 'foundation', 'objection']):
            sections.append(title)
    return sections[:5]  # Max 5


def extract_cross_references(content: str) -> list:
    """Extract cross-references for Out-of-Scope."""
    refs = []
    # Look for "See Appendix X" or "Appendix X (NAME)"
    for match in re.finditer(r'Appendix\s+([A-Z]{1,3})\s*\(([^)]+)\)', content):
        code = match.group(1)
        name = match.group(2)
        refs.append((code, name))

    # Also check Cross-References line
    cr_match = re.search(r'Cross-References?[:\s]+([^\n]+)', content, re.IGNORECASE)
    if cr_match:
        for match in re.finditer(r'([A-Z]{1,3})\s*\(([^)]+)\)', cr_match.group(1)):
            code = match.group(1)
            name = match.group(2)
            if (code, name) not in refs:
                refs.append((code, name))

    return refs[:5]  # Max 5


def extract_deliverables(content: str) -> list:
    """Extract deliverables from tables, equations, and axioms."""
    deliverables = []

    # Count tables
    tables = len(re.findall(r'\\begin\{table', content))
    if tables > 0:
        deliverables.append(f"{tables} Table(s)")

    # Count equations
    equations = len(re.findall(r'\\begin\{equation', content))
    if equations > 0:
        deliverables.append(f"{equations} Equation(s)")

    # Count axioms
    axioms = len(re.findall(r'Axiom\s+[A-Z]+-\d+', content))
    if axioms > 0:
        deliverables.append(f"{axioms} Axiom(s)")

    # Check for worked example
    if re.search(r'Worked Example|Example:', content, re.IGNORECASE):
        deliverables.append("Worked Example(s)")

    return deliverables if deliverables else ["[TODO: Add deliverables]"]


def generate_scope_box(content: str, filepath: str) -> str:
    """Generate Scope Box LaTeX code based on content analysis."""

    title = extract_title(content)
    abstract = extract_abstract(content)
    fundamental = extract_fundamental_question(content)
    sections = extract_sections(content)
    cross_refs = extract_cross_references(content)
    deliverables = extract_deliverables(content)

    # Determine Ziel
    if fundamental:
        ziel = fundamental
    elif abstract:
        ziel = abstract.split('.')[0] + "."
    else:
        ziel = f"[TODO: Define objective for {title}]"

    # Build In-Scope items
    if sections:
        in_scope_items = "\n".join([f"    \\item {s}" for s in sections])
    else:
        in_scope_items = "    \\item [TODO: Define in-scope topics]"

    # Build Out-of-Scope items
    if cross_refs:
        out_scope_items = "\n".join([
            f"    \\item {name} $\\rightarrow$ Appendix {code}"
            for code, name in cross_refs
        ])
    else:
        out_scope_items = "    \\item [TODO: Define delegations to other appendices]"

    # Build Deliverables items
    deliv_items = "\n".join([f"    \\item {d}" for d in deliverables])

    scope_box = f'''% -----------------------------------------------------------------------------
% APPENDIX SCOPE BOX
% -----------------------------------------------------------------------------

\\begin{{tcolorbox}}[
    colback=orange!5!white,
    colframe=orange!75!black,
    title={{\\textbf{{Appendix Scope: Ziel / In-Scope / Out-of-Scope / Constraints}}}},
    fonttitle=\\bfseries
]

\\textbf{{Ziel (Objective):}}
\\begin{{itemize}}[nosep]
    \\item {ziel}
\\end{{itemize}}

\\textbf{{In-Scope:}}
\\begin{{itemize}}[nosep]
{in_scope_items}
\\end{{itemize}}

\\textbf{{Out-of-Scope (delegiert an andere Appendices):}}
\\begin{{itemize}}[nosep]
{out_scope_items}
\\end{{itemize}}

\\textbf{{Constraints (Anwendungsgrenzen):}}
\\begin{{itemize}}[nosep]
    \\item [TODO: Define when this appendix does NOT apply]
    \\item [TODO: Define required prerequisites]
    \\item [TODO: Define known limitations]
\\end{{itemize}}

\\textbf{{Lieferobjekte (Deliverables):}}
\\begin{{itemize}}[nosep]
{deliv_items}
\\end{{itemize}}

\\end{{tcolorbox}}

'''
    return scope_box


def has_scope_box(content: str) -> bool:
    """Check if content already has a Scope Box."""
    return bool(re.search(r'Appendix Scope:', content))


def insert_scope_box(content: str, scope_box: str) -> str:
    """Insert Scope Box after Quick Reference Box."""

    # Find the end of Quick Reference tcolorbox
    # Pattern: \end{tcolorbox} followed by whitespace and then PART 2 or section
    pattern = r'(\\textbf\{Cross-References[:\}][^\n]*\n\\end\{tcolorbox\})'

    match = re.search(pattern, content)
    if match:
        insert_pos = match.end()
        new_content = content[:insert_pos] + "\n\n" + scope_box + content[insert_pos:]
        return new_content

    # Fallback: Insert before PART 2: CORE CONTENT
    pattern2 = r'(% =+\n%\s+PART 2: CORE CONTENT)'
    match2 = re.search(pattern2, content)
    if match2:
        insert_pos = match2.start()
        new_content = content[:insert_pos] + scope_box + "\n" + content[insert_pos:]
        return new_content

    # Last fallback: Insert before first \section
    pattern3 = r'(\\section\{)'
    match3 = re.search(pattern3, content)
    if match3:
        insert_pos = match3.start()
        new_content = content[:insert_pos] + scope_box + "\n" + content[insert_pos:]
        return new_content

    return content  # No change if no insertion point found


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


def process_file(filepath: str, dry_run: bool = False) -> bool:
    """Process a single file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if has_scope_box(content):
        print(f"  ⏭️  Already has Scope Box: {filepath}")
        return False

    scope_box = generate_scope_box(content, filepath)
    new_content = insert_scope_box(content, scope_box)

    if new_content == content:
        print(f"  ⚠️  Could not find insertion point: {filepath}")
        return False

    if dry_run:
        print(f"  🔍 Would add Scope Box to: {filepath}")
        print(f"      Preview (first 200 chars of scope box):")
        print(f"      {scope_box[:200]}...")
        return True

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"  ✅ Added Scope Box: {filepath}")
    return True


def main():
    parser = argparse.ArgumentParser(description='Add Scope Box to appendices')
    parser.add_argument('files', nargs='*', help='Files to process')
    parser.add_argument('--all', action='store_true', help='Process all appendices')
    parser.add_argument('--min-compliance', type=float, default=90,
                        help='Minimum compliance score (default: 90)')
    parser.add_argument('--dry-run', action='store_true', help='Preview without changes')

    args = parser.parse_args()

    files = []

    if args.all:
        appendix_dir = Path('appendices')
        for f in appendix_dir.glob('*.tex'):
            if 'template' not in f.name.lower() and 'index' not in f.name.lower():
                compliance = get_compliance(str(f))
                if compliance >= args.min_compliance:
                    files.append((str(f), compliance))

        files.sort(key=lambda x: -x[1])  # Sort by compliance descending
        print(f"Found {len(files)} appendices with compliance >= {args.min_compliance}%")
    else:
        files = [(f, 0) for f in args.files]

    if not files:
        print("No files to process.")
        return

    processed = 0
    skipped = 0

    for filepath, compliance in files:
        if args.all:
            print(f"\n[{compliance:.1f}%] {os.path.basename(filepath)}")

        if process_file(filepath, args.dry_run):
            processed += 1
        else:
            skipped += 1

    print(f"\n{'='*60}")
    print(f"Summary: {processed} processed, {skipped} skipped")
    if args.dry_run:
        print("(Dry run - no files were modified)")


if __name__ == '__main__':
    main()
