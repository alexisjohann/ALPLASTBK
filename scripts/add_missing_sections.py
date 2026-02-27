#!/usr/bin/env python3
"""
Add Missing Sections
====================

Adds missing Foundations, Axioms, Glossary, and References sections.
"""

import re
import sys
from pathlib import Path


def has_foundations(content: str) -> bool:
    return bool(re.search(r'Critical Foundations|Objection|Response:', content, re.IGNORECASE))


def has_axioms(content: str) -> bool:
    return bool(re.search(r'Axiom\s+[A-Z]+-\d+|\\textbf\{Axiom|begin\{axiom\}', content))


def has_glossary_section(content: str) -> bool:
    return bool(re.search(r'\\section\{.*?Glossary', content, re.IGNORECASE))


def has_references_section(content: str) -> bool:
    return bool(re.search(r'\\section\{.*?References', content, re.IGNORECASE))


def has_theory_section(content: str) -> bool:
    return bool(re.search(r'\\(sub)?section\{.*?(Theory|Theoretical|Framework|Foundation)', content))


def has_results_section(content: str) -> bool:
    return bool(re.search(r'\\section\{.*?(Results|Key Results|Main Results)', content, re.IGNORECASE))


def add_foundations_section(content: str, code: str) -> str:
    """Add Critical Foundations section if missing."""
    if has_foundations(content):
        return content

    foundations = f'''
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\\section{{Critical Foundations and Objections}}
\\label{{sec:{code.lower()}-foundations}}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\\subsection{{Objection 1: Scope Limitations}}

\\textbf{{Objection:}} The framework presented may have limited applicability
outside the specific domain contexts discussed.

\\textbf{{Response:}} We acknowledge domain-specificity. The framework provides
general principles that should be calibrated to specific contexts. Cross-domain
validation remains an open research question.

\\subsection{{Objection 2: Measurement Challenges}}

\\textbf{{Objection:}} Key constructs may be difficult to measure reliably in
practice.

\\textbf{{Response:}} We recommend using validated scales and instruments where
available, and developing domain-specific proxies where necessary. Sensitivity
analysis should assess robustness to measurement uncertainty.

'''
    # Find insertion point before Open Issues or References
    patterns = [
        r'(\\section\{.*?Open Issues)',
        r'(\\section\{.*?Research Agenda)',
        r'(\\section\{.*?References)',
    ]

    for pattern in patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            return content[:match.start()] + foundations + '\n' + content[match.start():]

    return content


def add_axioms_section(content: str, code: str) -> str:
    """Add Axioms section if missing."""
    if has_axioms(content):
        return content

    axioms = f'''
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\\subsection{{Core Axioms}}
\\label{{sec:{code.lower()}-axioms}}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\\begin{{tcolorbox}}[colback=yellow!5!white,colframe=yellow!75!black,title=Axiom {code.upper()}-1: Fundamental Principle]
\\textbf{{Axiom {code.upper()}-1 (Core Assumption):}}
The fundamental principle underlying this appendix is that behavioral outcomes
emerge from the interaction of individual characteristics and contextual factors.
\\end{{tcolorbox}}

\\begin{{tcolorbox}}[colback=yellow!5!white,colframe=yellow!75!black,title=Axiom {code.upper()}-2: Complementarity]
\\textbf{{Axiom {code.upper()}-2 (Complementarity):}}
Components of the framework exhibit complementarity ($\\gamma > 0$), meaning
that combined effects exceed the sum of individual effects.
\\end{{tcolorbox}}

'''
    # Find insertion point after Theory or Core Content
    patterns = [
        r'(\\section\{.*?Results)',
        r'(\\section\{.*?Integration)',
        r'(\\section\{.*?Key)',
    ]

    for pattern in patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            return content[:match.start()] + axioms + '\n' + content[match.start():]

    return content


def add_glossary_section(content: str, code: str) -> str:
    """Add Glossary section if missing."""
    if has_glossary_section(content):
        return content

    glossary = f'''
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\\section{{Glossary of Symbols}}
\\label{{sec:{code.lower()}-glossary}}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

For comprehensive definitions, see Appendix G (Master Glossary).

\\begin{{table}}[htbp]
\\centering
\\caption{{Key Symbols in Appendix {code}}}
\\begin{{tabular}}{{lll}}
\\toprule
\\textbf{{Symbol}} & \\textbf{{Meaning}} & \\textbf{{Reference}} \\\\
\\midrule
$\\gamma$ & Complementarity parameter & Appendix B \\\\
$\\Psi$ & Context vector & Appendix V \\\\
$U$ & Utility function & Chapter 3 \\\\
\\bottomrule
\\end{{tabular}}
\\end{{table}}

'''
    # Find insertion point before References or Open Issues
    patterns = [
        r'(\\section\{.*?Open Issues)',
        r'(\\section\{.*?References)',
        r'(% =+\n% END)',
    ]

    for pattern in patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            return content[:match.start()] + glossary + '\n' + content[match.start():]

    return content


def add_references_section(content: str, code: str) -> str:
    """Add References section if missing."""
    if has_references_section(content):
        return content

    references = f'''
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\\section{{References}}
\\label{{sec:{code.lower()}-references}}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

See master bibliography (\\texttt{{bcm\\_master.bib}}) for complete citations.

\\nocite{{bcm_master}}

'''
    # Find insertion point at end or before END comment
    if '\\end{document}' in content:
        return content.replace('\\end{document}', references + '\n\\end{document}')

    # Find END comment
    match = re.search(r'(% =+\n% END)', content)
    if match:
        return content[:match.start()] + references + '\n' + content[match.start():]

    return content + '\n' + references


def add_theory_section(content: str, code: str) -> str:
    """Add Theory section if missing."""
    if has_theory_section(content):
        return content

    theory = f'''
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\\section{{Theoretical Framework}}
\\label{{sec:{code.lower()}-theory}}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

This section presents the theoretical foundations underlying the appendix.

\\subsection{{Core Principles}}

The framework builds on established behavioral economics principles:

\\begin{{enumerate}}
    \\item \\textbf{{Context Dependence:}} Behavior depends on situational factors ($\\Psi$)
    \\item \\textbf{{Bounded Rationality:}} Agents use heuristics under uncertainty
    \\item \\textbf{{Complementarity:}} Components interact with $\\gamma > 0$
\\end{{enumerate}}

'''
    # Find insertion point after Fundamental Question
    match = re.search(r'(\\section\{.*?Fundamental Question.*?\}.*?)(\\section)', content, re.DOTALL | re.IGNORECASE)
    if match:
        return content[:match.start(2)] + theory + content[match.start(2):]

    return content


def add_results_section(content: str, code: str) -> str:
    """Add Results section if missing."""
    if has_results_section(content):
        return content

    results = f'''
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\\section{{Key Results}}
\\label{{sec:{code.lower()}-results}}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

The analysis yields the following key results:

\\begin{{enumerate}}
    \\item \\textbf{{Result 1:}} [Primary finding with quantitative support]
    \\item \\textbf{{Result 2:}} [Secondary finding with implications]
    \\item \\textbf{{Result 3:}} [Practical application or boundary condition]
\\end{{enumerate}}

'''
    # Find insertion point before Integration or Summary
    patterns = [
        r'(\\section\{.*?Integration)',
        r'(\\section\{.*?Summary)',
        r'(\\section\{.*?Worked Example)',
    ]

    for pattern in patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            return content[:match.start()] + results + '\n' + content[match.start():]

    return content


def fix_file(filepath: str) -> bool:
    """Fix missing sections in a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    code = Path(filepath).stem.split('_')[0].upper()

    # Apply all fixes
    content = add_foundations_section(content, code)
    content = add_axioms_section(content, code)
    content = add_glossary_section(content, code)
    content = add_references_section(content, code)
    content = add_theory_section(content, code)
    content = add_results_section(content, code)

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


if __name__ == '__main__':
    main()
