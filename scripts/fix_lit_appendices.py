#!/usr/bin/env python3
"""
Fix LIT Appendices
==================

Adds missing front matter to LIT appendices that are structured as paper lists.
"""

import re
import sys
from pathlib import Path


def extract_researcher_name(content: str) -> str:
    """Extract researcher name from content."""
    # Try to find "papers by X" or "X Research"
    match = re.search(r'papers by ([A-Z][a-z]+ [A-Z][a-z]+)', content, re.IGNORECASE)
    if match:
        return match.group(1)

    match = re.search(r'([A-Z][a-z]+)\'s research', content, re.IGNORECASE)
    if match:
        return match.group(1)

    match = re.search(r'Research.*?by\s+([A-Z][a-z]+ [A-Z][a-z]+)', content, re.IGNORECASE)
    if match:
        return match.group(1)

    return "Unknown Researcher"


def extract_code(filepath: str) -> str:
    """Extract appendix code from filename."""
    fname = Path(filepath).stem
    parts = fname.split('_')
    if parts and len(parts[0]) <= 3:
        return parts[0].upper()
    return "X"


def has_chapter(content: str) -> bool:
    """Check if file has chapter command."""
    return bool(re.search(r'\\chapter\{', content))


def has_header(content: str) -> bool:
    """Check if file has proper header."""
    return bool(re.search(r'% Category:', content))


def fix_lit_appendix(filepath: str) -> bool:
    """Fix a LIT appendix by adding proper front matter."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if has_chapter(content) and has_header(content):
        return False  # Already has proper structure

    code = extract_code(filepath)
    researcher = extract_researcher_name(content)

    # Build front matter
    header = f'''% =============================================================================
% APPENDIX {code}: LIT-{researcher.upper().split()[0] if researcher != "Unknown Researcher" else "AUTHOR"}: {researcher} Research Integration
% =============================================================================
% Category: LIT
% Language: English
% Version: 1.0 (January 2026)
% Status: Draft
%
% This appendix integrates research papers by {researcher} into the EBF framework.
%
% =============================================================================

\\chapter{{LIT-{researcher.upper().split()[0] if researcher != "Unknown Researcher" else "AUTHOR"}: {researcher} Research Integration}}
\\label{{app:{code.lower()}}}

\\begin{{abstract}}
This appendix integrates the research contributions of {researcher} into the
Evidence-Based Framework. It documents key papers, core findings, and their
integration with EBF dimensions including complementarity parameters ($\\gamma$),
context factors ($\\Psi$), and utility dimensions.
\\end{{abstract}}

\\begin{{tcolorbox}}[colback=blue!5!white, colframe=blue!75!black,
    title=Quick Reference: {researcher} Research]

\\textbf{{Appendix:}} {code} (LIT)

\\textbf{{Researcher:}} {researcher}

\\textbf{{Core Themes:}}
\\begin{{itemize}}[nosep]
\\item Behavioral economics foundations
\\item Empirical evidence for EBF parameters
\\item Policy implications and interventions
\\end{{itemize}}

\\textbf{{EBF Integration:}}
\\begin{{itemize}}[nosep]
\\item Complementarity values ($\\gamma$) from experimental evidence
\\item Context effects ($\\Psi$) documented across studies
\\item Utility dimension weightings calibrated to findings
\\end{{itemize}}

\\textbf{{Cross-References:}} BBB (CORE-WHERE), K (LIT-FEHR), G (Glossary)
\\end{{tcolorbox}}

% -----------------------------------------------------------------------------
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
    \\item Integrate {researcher}'s research into EBF with parameter extraction
\\end{{itemize}}

\\textbf{{In-Scope:}}
\\begin{{itemize}}[nosep]
    \\item Paper-by-paper integration with 10C mapping
    \\item Extraction of $\\gamma$, $\\Psi$, and effect size parameters
    \\item Cross-references to related EBF components
\\end{{itemize}}

\\textbf{{Out-of-Scope (delegiert an andere Appendices):}}
\\begin{{itemize}}[nosep]
    \\item Parameter validation $\\rightarrow$ Appendix BBB (CORE-WHERE)
    \\item Formal axiomatization $\\rightarrow$ CORE appendices
    \\item Meta-analysis $\\rightarrow$ LIT-M appendices
\\end{{itemize}}

\\textbf{{Constraints (Anwendungsgrenzen):}}
\\begin{{itemize}}[nosep]
    \\item Parameters are extracted from published studies
    \\item Effect sizes may vary across replications
    \\item Context-specificity of findings applies
\\end{{itemize}}

\\textbf{{Lieferobjekte (Deliverables):}}
\\begin{{itemize}}[nosep]
    \\item Paper integration table with 10C mappings
    \\item Extracted parameters for BBB repository
    \\item Cross-reference map to related literature
\\end{{itemize}}

\\end{{tcolorbox}}

'''

    # Remove any existing fundamental question that was added
    content = re.sub(r'%+\n\\section\{The Fundamental Question\}.*?\\end\{tcolorbox\}\n+', '', content, flags=re.DOTALL)

    # Insert header at the beginning
    new_content = header + '\n' + content

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True


def main():
    for filepath in sys.argv[1:]:
        print(f"Processing: {filepath}")
        if fix_lit_appendix(filepath):
            print(f"  Fixed")
        else:
            print(f"  Already has structure")


if __name__ == '__main__':
    main()
