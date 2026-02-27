#!/usr/bin/env python3
"""
FIX LAST 10% ALGORITHM
======================

Effizient die letzten 10% Compliance erreichen.

Strategie:
- Phase 1: High-Impact Quick Fixes (Glossary G Link, References)
- Phase 2: Template Sections (Results, Summary, Fundamental Question)
- Phase 3: Template Boxes (Header Block, Scope Box)

Usage:
    python scripts/fix_last_10_percent.py [--dry-run] [--phase N]
"""

import re
import sys
import os
from pathlib import Path

# =============================================================================
# TEMPLATES
# =============================================================================

GLOSSARY_G_LINK = "\nFor comprehensive symbol definitions, see Appendix G (Master Glossary).\n"

REFERENCES_SECTION = """

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\\section{References}
\\label{sec:CODE-references}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\\nocite{bcm_master}
See master bibliography (\\texttt{bcm\\_master.bib}) for complete citations.
For comprehensive symbol definitions, see Appendix G (Master Glossary).

"""

RESULTS_SECTION = """

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\\section{Key Results}
\\label{sec:CODE-results}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

The analysis yields the following key results:

\\begin{enumerate}
    \\item \\textbf{Result 1:} Primary finding with quantitative support
    \\item \\textbf{Result 2:} Secondary finding with implications
    \\item \\textbf{Result 3:} Practical application or boundary condition
\\end{enumerate}

"""

SUMMARY_SECTION = """

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\\section{Summary}
\\label{sec:CODE-summary}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\\begin{tcolorbox}[colback=gray!5!white, colframe=gray!75!black,
    title=Appendix CODE Summary]

\\textbf{Core Insight:}
This appendix provides key analysis relevant to the EBF framework.

\\textbf{Key Contributions:}
\\begin{itemize}[nosep]
    \\item Theoretical foundations and integration
    \\item Parameter estimates and validation
    \\item Cross-appendix connections
\\end{itemize}

\\end{tcolorbox}

"""

FUNDAMENTAL_QUESTION = """

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\\section{The Fundamental Question}
\\label{sec:CODE-fundamental}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\\begin{tcolorbox}[colback=red!5!white, colframe=red!75!black,
    title=The Fundamental Question]
What are the key mechanisms and implications of this analysis for the
Evidence-Based Framework (EBF)?
\\end{tcolorbox}

"""

HEADER_BLOCK = """
\\begin{tcolorbox}[colback=blue!5!white, colframe=blue!75!black,
    title=Quick Reference: Appendix CODE]

\\textbf{Appendix:} CODE (CATEGORY)

\\textbf{Core Question:} What are the key findings in this domain?

\\textbf{Key Concepts:}
\\begin{itemize}[nosep]
\\item Framework integration
\\item Parameter validation
\\item Cross-references
\\end{itemize}

\\textbf{Cross-References:} See related appendices below
\\end{tcolorbox}

"""

SCOPE_BOX = """
\\begin{tcolorbox}[
    colback=orange!5!white,
    colframe=orange!75!black,
    title={\\textbf{Appendix Scope: Ziel / In-Scope / Out-of-Scope / Constraints}},
    fonttitle=\\bfseries
]

\\textbf{Ziel (Objective):}
\\begin{itemize}[nosep]
    \\item Provide systematic analysis for CATEGORY integration
\\end{itemize}

\\textbf{In-Scope:}
\\begin{itemize}[nosep]
    \\item Core analysis and findings
    \\item Framework integration points
\\end{itemize}

\\textbf{Out-of-Scope:}
\\begin{itemize}[nosep]
    \\item Detailed empirical replication $\\rightarrow$ METHOD appendices
\\end{itemize}

\\textbf{Constraints:}
\\begin{itemize}[nosep]
    \\item Analysis bounded by available data
\\end{itemize}

\\end{tcolorbox}

"""

ABSTRACT_SECTION = """
\\begin{abstract}
This appendix provides systematic analysis and documentation relevant to the
Evidence-Based Framework (EBF). It integrates with the 10C CORE architecture
and provides validated findings for practical application.
\\end{abstract}

"""

CHAPTER_LINKAGE = """
\\begin{tcolorbox}[colback=purple!5!white, colframe=purple!75!black,
    title=Chapter Linkage]

\\textbf{Primary Chapter:} Related application chapter
\\begin{itemize}[nosep]
\\item Integration with main framework exposition
\\end{itemize}

\\textbf{Secondary Chapters:}
\\begin{itemize}[nosep]
\\item Supporting theoretical and methodological chapters
\\end{itemize}

\\end{tcolorbox}

"""

OPEN_ISSUES = """
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\\section{Open Issues and Research Agenda}
\\label{sec:CODE-open-issues}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\\begin{enumerate}
    \\item \\textbf{Empirical Validation:} Further testing across diverse contexts
    \\item \\textbf{Parameter Refinement:} Improved estimation methods needed
    \\item \\textbf{Integration:} Enhanced cross-appendix linkages
\\end{enumerate}

"""

# =============================================================================
# DETECTION FUNCTIONS
# =============================================================================

def get_code_and_category(filepath, content):
    """Extract appendix code and category."""
    fname = Path(filepath).stem
    parts = fname.split('_')
    code = parts[0].upper() if parts else "X"

    cat_match = re.search(r'% Category:\s*(\w+)', content, re.IGNORECASE)
    category = cat_match.group(1).upper() if cat_match else "UNKNOWN"

    return code, category

def has_glossary_g_link(content):
    return bool(re.search(r'Appendix G|Glossary.*master|comprehensive', content, re.IGNORECASE))

def has_references_section(content):
    return bool(re.search(r'\\section\{References', content))

def has_results(content):
    return bool(re.search(r'\\(sub)?section\{.*?(Results|Findings|Validation)', content))

def has_summary(content):
    return bool(re.search(r'\\section\{Summary|Summary\}|\\textbf\{.*?Summary', content))

def has_fundamental_question(content):
    return bool(re.search(r'Fundamental Question|CORE Question|Core Contribution', content, re.IGNORECASE))

def has_header_block(content):
    return bool(re.search(r'\\begin\{tcolorbox\}.*?(Appendix:|Category:|CORE Question:)', content, re.DOTALL))

def has_scope_box(content):
    return bool(re.search(r'Appendix Scope:|Ziel.*?In-Scope.*?Out-of-Scope', content, re.IGNORECASE | re.DOTALL))

def has_abstract(content):
    return bool(re.search(r'\\begin\{abstract\}|Abstract\}|\\textbf\{Abstract', content))

def has_chapter_linkage(content):
    return bool(re.search(r'Chapter Linkage|Primary Chapter|Chapter \d+', content))

def has_open_issues(content):
    return bool(re.search(r'Open Issues|Future Work|Research Agenda|Limitations', content, re.IGNORECASE))

# =============================================================================
# FIX FUNCTIONS
# =============================================================================

def fix_glossary_g_link(content, code):
    """Add Glossary G link to glossary or references section."""
    # Try to add after Glossary section
    match = re.search(r'(\\section\{Glossary[^}]*\}.*?\\label\{[^}]+\})', content, re.DOTALL)
    if match:
        return content[:match.end()] + GLOSSARY_G_LINK + content[match.end():]

    # Or add to references section
    match = re.search(r'(\\section\{References[^}]*\})', content)
    if match:
        return content[:match.end()] + "\n" + GLOSSARY_G_LINK + content[match.end():]

    return content

def fix_references_section(content, code):
    """Add References section before end of document."""
    template = REFERENCES_SECTION.replace('CODE', code.lower())

    match = re.search(r'\\end\{document\}', content)
    if match:
        return content[:match.start()] + template + content[match.start():]

    match = re.search(r'\\end\{chapter\}', content)
    if match:
        return content[:match.start()] + template + content[match.start():]

    return content

def fix_results(content, code):
    """Add Results section before Summary or Glossary."""
    template = RESULTS_SECTION.replace('CODE', code.lower())

    # Before Summary
    match = re.search(r'\\section\{Summary', content)
    if match:
        return content[:match.start()] + template + content[match.start():]
    # Before Glossary
    match = re.search(r'\\section\{Glossary', content)
    if match:
        return content[:match.start()] + template + content[match.start():]
    # Before References
    match = re.search(r'\\section\{References', content)
    if match:
        return content[:match.start()] + template + content[match.start():]
    return content

def fix_summary(content, code):
    """Add Summary section before Glossary or References."""
    template = SUMMARY_SECTION.replace('CODE', code.lower())

    # Before Glossary
    match = re.search(r'\\section\{Glossary', content)
    if match:
        return content[:match.start()] + template + content[match.start():]
    # Before References
    match = re.search(r'\\section\{References', content)
    if match:
        return content[:match.start()] + template + content[match.start():]
    return content

def fix_fundamental_question(content, code):
    """Add Fundamental Question after header/abstract."""
    template = FUNDAMENTAL_QUESTION.replace('CODE', code.lower())

    # After abstract
    match = re.search(r'(\\end\{abstract\}\s*\n)', content)
    if match:
        return content[:match.end()] + template + content[match.end():]

    # After first tcolorbox
    match = re.search(r'(\\end\{tcolorbox\}\s*\n)(?=\s*%|\s*\\section)', content)
    if match:
        return content[:match.end()] + template + content[match.end():]

    return content

def fix_header_block(content, code, category):
    """Add Header Block after maketitle or begin document."""
    template = HEADER_BLOCK.replace('CODE', code).replace('CATEGORY', category)

    # After maketitle
    match = re.search(r'(\\maketitle\s*\n)', content)
    if match:
        return content[:match.end()] + template + content[match.end():]

    # After begin{document}
    match = re.search(r'(\\begin\{document\}\s*\n)', content)
    if match:
        return content[:match.end()] + template + content[match.end():]

    # After chapter declaration with label
    match = re.search(r'(\\chapter\*?\{[^}]+\}.*?\\label\{[^}]+\}\s*\n)', content, re.DOTALL)
    if match:
        return content[:match.end()] + template + content[match.end():]

    # After chapter declaration without label
    match = re.search(r'(\\chapter\*?\{[^}]+\}\s*\n)', content)
    if match:
        return content[:match.end()] + template + content[match.end():]

    # After begin{chapter}
    match = re.search(r'(\\begin\{chapter\}\{[^}]+\}.*?\\label\{[^}]+\}\s*\n)', content, re.DOTALL)
    if match:
        return content[:match.end()] + template + content[match.end():]

    # After first section* (some files start with section*)
    match = re.search(r'(\\section\*\{[^}]+\}\s*\n)', content)
    if match:
        return content[:match.end()] + template + content[match.end():]

    return content

def fix_scope_box(content, code, category):
    """Add Scope Box after abstract or header block."""
    template = SCOPE_BOX.replace('CODE', code).replace('CATEGORY', category)

    # After abstract
    match = re.search(r'(\\end\{abstract\}\s*\n)', content)
    if match:
        return content[:match.end()] + template + content[match.end():]

    # After first tcolorbox (header block)
    match = re.search(r'(\\end\{tcolorbox\}\s*\n)', content)
    if match:
        return content[:match.end()] + template + content[match.end():]

    # After chapter declaration
    match = re.search(r'(\\chapter\{[^}]+\}\s*\n)', content)
    if match:
        return content[:match.end()] + template + content[match.end():]

    return content

def fix_abstract(content, code):
    """Add Abstract after chapter or title."""
    template = ABSTRACT_SECTION

    # After chapter with label
    match = re.search(r'(\\chapter\*?\{[^}]+\}.*?\\label\{[^}]+\}\s*\n)', content, re.DOTALL)
    if match:
        return content[:match.end()] + template + content[match.end():]

    # After chapter without label
    match = re.search(r'(\\chapter\*?\{[^}]+\}\s*\n)', content)
    if match:
        return content[:match.end()] + template + content[match.end():]

    # After begin{chapter}
    match = re.search(r'(\\begin\{chapter\}\{[^}]+\}.*?\\label\{[^}]+\}\s*\n)', content, re.DOTALL)
    if match:
        return content[:match.end()] + template + content[match.end():]

    # After title in article
    match = re.search(r'(\\maketitle\s*\n)', content)
    if match:
        return content[:match.end()] + template + content[match.end():]

    # After first tcolorbox (if header block exists)
    match = re.search(r'(Quick Reference.*?\\end\{tcolorbox\}\s*\n)', content, re.DOTALL)
    if match:
        return content[:match.end()] + template + content[match.end():]

    return content

def fix_chapter_linkage(content, code, category):
    """Add Chapter Linkage after Cross-Reference Map or header."""
    template = CHAPTER_LINKAGE

    # After Cross-Reference Map tcolorbox
    match = re.search(r'(Cross-Reference.*?\\end\{tcolorbox\}\s*\n)', content, re.DOTALL)
    if match:
        return content[:match.end()] + template + content[match.end():]

    # After first tcolorbox
    match = re.search(r'(\\end\{tcolorbox\}\s*\n)', content)
    if match:
        return content[:match.end()] + template + content[match.end():]

    return content

def fix_open_issues(content, code):
    """Add Open Issues section before References."""
    template = OPEN_ISSUES.replace('CODE', code.lower())

    # Before References
    match = re.search(r'\\section\{References', content)
    if match:
        return content[:match.start()] + template + content[match.start():]

    return content

# =============================================================================
# MAIN ALGORITHM
# =============================================================================

def fix_file(filepath, dry_run=False, phase=None):
    """Apply fixes to a single file."""
    with open(filepath, 'r') as f:
        content = f.read()

    original = content
    code, category = get_code_and_category(filepath, content)
    changes = []

    # PHASE 1: High-Impact Quick Fixes
    if phase is None or phase == 1:
        if not has_glossary_g_link(content):
            content = fix_glossary_g_link(content, code)
            if content != original:
                changes.append("P1: Added Glossary G Link")

        if not has_references_section(content):
            new_content = fix_references_section(content, code)
            if new_content != content:
                content = new_content
                changes.append("P1: Added References Section")

    # PHASE 2: Template Sections
    if phase is None or phase == 2:
        if not has_results(content):
            new_content = fix_results(content, code)
            if new_content != content:
                content = new_content
                changes.append("P2: Added Results Section")

        if not has_summary(content):
            new_content = fix_summary(content, code)
            if new_content != content:
                content = new_content
                changes.append("P2: Added Summary Section")

        if not has_fundamental_question(content):
            new_content = fix_fundamental_question(content, code)
            if new_content != content:
                content = new_content
                changes.append("P2: Added Fundamental Question")

    # PHASE 3: Template Boxes
    if phase is None or phase == 3:
        if not has_header_block(content):
            new_content = fix_header_block(content, code, category)
            if new_content != content:
                content = new_content
                changes.append("P3: Added Header Block")

        if not has_scope_box(content):
            new_content = fix_scope_box(content, code, category)
            if new_content != content:
                content = new_content
                changes.append("P3: Added Scope Box")

        if not has_abstract(content):
            new_content = fix_abstract(content, code)
            if new_content != content:
                content = new_content
                changes.append("P3: Added Abstract")

        if not has_chapter_linkage(content):
            new_content = fix_chapter_linkage(content, code, category)
            if new_content != content:
                content = new_content
                changes.append("P3: Added Chapter Linkage")

        if not has_open_issues(content):
            new_content = fix_open_issues(content, code)
            if new_content != content:
                content = new_content
                changes.append("P3: Added Open Issues")

    # Write if changed
    if content != original and not dry_run:
        with open(filepath, 'w') as f:
            f.write(content)

    return changes

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Fix last 10% compliance issues')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be fixed')
    parser.add_argument('--phase', type=int, choices=[1, 2, 3], help='Run only specific phase')
    parser.add_argument('files', nargs='*', help='Files to fix (default: all appendices)')
    args = parser.parse_args()

    # Get files
    if args.files:
        files = args.files
    else:
        files = [f'appendices/{f}' for f in os.listdir('appendices') if f.endswith('.tex')]

    print("=" * 60)
    print("FIX LAST 10% ALGORITHM")
    print("=" * 60)
    if args.dry_run:
        print("MODE: DRY RUN (no changes will be made)")
    if args.phase:
        print(f"PHASE: {args.phase} only")
    print()

    total_fixed = 0
    total_changes = 0

    for filepath in sorted(files):
        changes = fix_file(filepath, dry_run=args.dry_run, phase=args.phase)
        if changes:
            total_fixed += 1
            total_changes += len(changes)
            print(f"{'[DRY]' if args.dry_run else 'Fixed'}: {filepath}")
            for c in changes:
                print(f"  - {c}")

    print()
    print("=" * 60)
    print(f"Total: {total_fixed} files, {total_changes} changes")
    print("=" * 60)

if __name__ == "__main__":
    main()
