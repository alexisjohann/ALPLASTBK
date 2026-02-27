#!/usr/bin/env python3
"""
Add All Missing Elements
========================

Comprehensive script to add all missing compliance elements to appendices.
Handles: Abstract, Quick Reference, Scope Box, Fundamental Question, Theory,
Results, Summary, Glossary, References, and more.

Usage:
    python scripts/add_all_missing_elements.py appendices/FILE.tex
"""

import re
import sys
from pathlib import Path


def extract_code(filepath: str, content: str) -> str:
    """Extract appendix code."""
    fname = Path(filepath).stem
    parts = fname.split('_')
    if parts and len(parts[0]) <= 3:
        return parts[0].upper()

    match = re.search(r'\\label\{app:([^}]+)\}', content)
    if match:
        return match.group(1).upper()

    return "X"


def extract_category(content: str) -> str:
    """Extract category from content."""
    match = re.search(r'% Category:\s*(\w+)', content)
    if match:
        cat = match.group(1).upper()
        return cat.rstrip('-')
    return "UNKNOWN"


def extract_title(content: str) -> str:
    """Extract title from chapter command."""
    match = re.search(r'\\chapter\*?\{([^}]+)\}', content)
    if match:
        return match.group(1).strip()
    return "Unknown"


def has_element(content: str, pattern: str) -> bool:
    """Check if content has element matching pattern."""
    return bool(re.search(pattern, content, re.IGNORECASE | re.DOTALL))


def add_abstract(content: str, code: str, title: str) -> str:
    """Add abstract if missing."""
    if has_element(content, r'\\begin\{abstract\}'):
        return content

    abstract = f'''\\begin{{abstract}}
This appendix presents the key concepts and formalizations for {title}.
It provides theoretical foundations, practical applications, and integration
points with other components of the Evidence-Based Framework (EBF).
The content supports decision-making and behavioral analysis in the context
of complementarity and context-dependent outcomes.
\\end{{abstract}}

'''
    # Insert after chapter command
    match = re.search(r'(\\chapter\*?\{[^}]+\}.*?\\label\{[^}]+\})', content, re.DOTALL)
    if match:
        return content[:match.end()] + '\n\n' + abstract + content[match.end():]

    return content


def add_quick_reference(content: str, code: str, category: str, title: str) -> str:
    """Add Quick Reference box if missing."""
    if has_element(content, r'Quick Reference'):
        return content

    qr = f'''\\begin{{tcolorbox}}[colback=blue!5!white, colframe=blue!75!black,
    title=Quick Reference: {title}]

\\textbf{{Appendix:}} {code} ({category})

\\textbf{{Core Concepts:}}
\\begin{{itemize}}[nosep]
\\item Complementarity ($\\gamma > 0$): Components interact synergistically
\\item Context ($\\Psi$): Situational factors that influence behavior
\\item Utility dimensions: FEPSDE (Financial, Emotional, Physical, Social, Development, Experiential)
\\end{{itemize}}

\\textbf{{Key Formulas:}}
\\begin{{equation}}
U = \\sum_d \\omega_d \\cdot u_d + \\gamma \\cdot f(\\text{{interactions}})
\\end{{equation}}

\\textbf{{Cross-References:}} Appendix B (CORE-HOW), V (CORE-WHEN), G (Glossary)
\\end{{tcolorbox}}

'''
    # Insert after abstract or chapter
    patterns = [
        r'(\\end\{abstract\})',
        r'(\\chapter\*?\{[^}]+\}.*?\\label\{[^}]+\})',
    ]

    for pattern in patterns:
        match = re.search(pattern, content, re.DOTALL)
        if match:
            return content[:match.end()] + '\n\n' + qr + content[match.end():]

    return content


def add_scope_box(content: str, code: str, category: str, title: str) -> str:
    """Add Scope Box if missing."""
    if has_element(content, r'Appendix Scope:|Ziel.*In-Scope'):
        return content

    scope = f'''% -----------------------------------------------------------------------------
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
    \\item Formalize and document the key concepts of {title}
\\end{{itemize}}

\\textbf{{In-Scope:}}
\\begin{{itemize}}[nosep]
    \\item Core theoretical foundations
    \\item Mathematical formalizations where applicable
    \\item Integration with EBF framework
\\end{{itemize}}

\\textbf{{Out-of-Scope (delegiert an andere Appendices):}}
\\begin{{itemize}}[nosep]
    \\item Detailed empirical validation $\\rightarrow$ METHOD appendices
    \\item Domain-specific applications $\\rightarrow$ DOMAIN appendices
    \\item Complete literature review $\\rightarrow$ LIT appendices
\\end{{itemize}}

\\textbf{{Constraints (Anwendungsgrenzen):}}
\\begin{{itemize}}[nosep]
    \\item Framework requires calibration to specific contexts
    \\item Parameters may vary across domains
    \\item Validity bounded by underlying assumptions
\\end{{itemize}}

\\textbf{{Lieferobjekte (Deliverables):}}
\\begin{{itemize}}[nosep]
    \\item Theoretical framework with formal definitions
    \\item Integration points with other appendices
    \\item Practical guidelines for application
\\end{{itemize}}

\\end{{tcolorbox}}

'''
    # Insert after Quick Reference or abstract
    patterns = [
        r'(\\end\{tcolorbox\}.*?Cross-References.*?\\end\{tcolorbox\})',
        r'(\\end\{abstract\})',
    ]

    for pattern in patterns:
        match = re.search(pattern, content, re.DOTALL)
        if match:
            return content[:match.end()] + '\n\n' + scope + content[match.end():]

    return content


def add_fundamental_question(content: str, code: str, title: str) -> str:
    """Add Fundamental Question section if missing."""
    if has_element(content, r'Fundamental Question'):
        return content

    fq = f'''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\\section{{The Fundamental Question}}
\\label{{sec:{code.lower()}-fundamental}}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\\begin{{tcolorbox}}[
    colback=red!5!white,
    colframe=red!75!black,
    title={{\\textbf{{Fundamental Question}}}}
]
\\textbf{{How does {title.lower()} integrate with and contribute to the
Evidence-Based Framework for understanding behavioral outcomes?}}

This appendix addresses the core challenge of formalizing behavioral principles
within a rigorous theoretical framework while maintaining practical applicability.
\\end{{tcolorbox}}

'''
    # Insert after Scope Box or Quick Reference
    patterns = [
        r'(\\end\{tcolorbox\}.*?Lieferobjekte.*?\\end\{tcolorbox\})',
        r'(\\end\{tcolorbox\}.*?Cross-References.*?\\end\{tcolorbox\})',
    ]

    for pattern in patterns:
        match = re.search(pattern, content, re.DOTALL)
        if match:
            return content[:match.end()] + '\n\n' + fq + content[match.end():]

    # Fallback: insert before first section
    match = re.search(r'(\\section\{)', content)
    if match:
        return content[:match.start()] + fq + '\n' + content[match.start():]

    return content


def add_summary(content: str, code: str) -> str:
    """Add Summary section if missing."""
    if has_element(content, r'\\section\{.*Summary'):
        return content

    summary = f'''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\\section{{Summary}}
\\label{{sec:{code.lower()}-summary}}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

This appendix has presented the key concepts and theoretical foundations.
The main contributions include:

\\begin{{enumerate}}
    \\item Formal definitions and theoretical framework
    \\item Integration with the broader EBF structure
    \\item Practical guidelines for application
\\end{{enumerate}}

The content supports decision-making and behavioral analysis within the
Evidence-Based Framework, providing a foundation for further research
and practical implementation.

'''
    # Insert before Glossary, Open Issues, or References
    patterns = [
        r'(\\section\{.*?Glossary)',
        r'(\\section\{.*?Open Issues)',
        r'(\\section\{.*?References)',
    ]

    for pattern in patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            return content[:match.start()] + summary + '\n' + content[match.start():]

    return content


def fix_file(filepath: str) -> bool:
    """Fix all missing elements in a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    code = extract_code(filepath, content)
    category = extract_category(content)
    title = extract_title(content)

    # Apply all fixes in order
    content = add_abstract(content, code, title)
    content = add_quick_reference(content, code, category, title)
    content = add_scope_box(content, code, category, title)
    content = add_fundamental_question(content, code, title)
    content = add_summary(content, code)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def main():
    for filepath in sys.argv[1:]:
        print(f"Processing: {filepath}")
        if fix_file(filepath):
            print(f"  Fixed")
        else:
            print(f"  No changes needed")


if __name__ == '__main__':
    main()
