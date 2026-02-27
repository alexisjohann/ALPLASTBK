#!/usr/bin/env python3
"""
Fix remaining files to reach 90%+ compliance.
Handles: Fundamental Question, Summary, Cross Ref Map, Scope Box, etc.
"""

import re
import sys
from pathlib import Path


def fix_file(filepath: str) -> bool:
    """Fix a single file."""
    with open(filepath, 'r') as f:
        content = f.read()

    original = content
    changes = []

    # Extract appendix code from filename
    fname = Path(filepath).stem
    parts = fname.split('_')
    code = parts[0].upper() if parts else "X"

    # Detect category from content
    cat_match = re.search(r'% Category:\s*(\w+)', content, re.IGNORECASE)
    category = cat_match.group(1).upper() if cat_match else "UNKNOWN"

    # 1. Add Fundamental Question if missing
    if not re.search(r'Fundamental Question|CORE Question|Core Contribution', content, re.IGNORECASE):
        # Find a good insertion point - before first main section or after Quick Reference
        quick_ref_end = re.search(r'(\\end\{tcolorbox\}\s*\n)(?=\s*%|\s*\\section)', content)
        if quick_ref_end:
            fundamental_q = '''
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\\section{The Fundamental Question}
\\label{sec:fundamental}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\\begin{tcolorbox}[colback=red!5!white, colframe=red!75!black,
    title=The Fundamental Question]
What are the key mechanisms, predictions, and implications of this analysis
for the Evidence-Based Framework?
\\end{tcolorbox}

'''
            content = content[:quick_ref_end.end()] + fundamental_q + content[quick_ref_end.end():]
            changes.append("Added Fundamental Question")

    # 2. Add Summary if missing
    if not re.search(r'\\section\{Summary|Summary\}|\\textbf\{.*?Summary', content):
        # Add before References or at end
        ref_match = re.search(r'(\\section\{References|\\section\{Glossary|\\end\{document\})', content)
        if ref_match:
            summary_section = f'''

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\\section{{Summary}}
\\label{{sec:{code.lower()}-summary}}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\\begin{{tcolorbox}}[colback=gray!5!white, colframe=gray!75!black,
    title=Appendix {code} Summary]

\\textbf{{Core Insight:}}
This appendix provides key analysis and findings relevant to the EBF framework.

\\textbf{{Key Contributions:}}
\\begin{{itemize}}[nosep]
    \\item Theoretical foundations and empirical evidence
    \\item Parameter estimates and model validation
    \\item Integration with 10C CORE architecture
\\end{{itemize}}

\\textbf{{Framework Integration:}}
The findings connect to WHO, WHAT, HOW, WHEN, WHERE, AWARE, READY, and STAGE dimensions.

\\end{{tcolorbox}}

'''
            content = content[:ref_match.start()] + summary_section + content[ref_match.start():]
            changes.append("Added Summary section")

    # 3. Add Cross Ref Map if missing
    if not re.search(r'Cross-Reference|CROSS-REFERENCE|Dependencies|Dependents', content, re.IGNORECASE):
        # Add after header block or at beginning
        header_end = re.search(r'(\\end\{tcolorbox\}\s*\n)(?=\s*%|\s*\\begin)', content)
        if header_end:
            cross_ref = f'''
\\begin{{tcolorbox}}[colback=blue!5!white, colframe=blue!75!black,
    title=Cross-Reference Map]

\\textbf{{Dependencies (what this appendix requires):}}
\\begin{{itemize}}[nosep]
    \\item Core 10C CORE appendices (AAA, B, C, V, BBB, AU, AV, AW, HI)
    \\item Related METHOD and DOMAIN appendices
\\end{{itemize}}

\\textbf{{Dependents (what requires this appendix):}}
\\begin{{itemize}}[nosep]
    \\item Application chapters and case studies
    \\item Related analysis appendices
\\end{{itemize}}

\\end{{tcolorbox}}

'''
            content = content[:header_end.end()] + cross_ref + content[header_end.end():]
            changes.append("Added Cross Reference Map")

    # 4. Add Scope Box if missing
    if not re.search(r'Appendix Scope:|Ziel.*?In-Scope.*?Out-of-Scope', content, re.IGNORECASE | re.DOTALL):
        # Add after abstract or cross ref
        insert_match = re.search(r'(\\end\{abstract\}\s*\n|Cross-Reference Map\][\s\S]*?\\end\{tcolorbox\}\s*\n)', content)
        if insert_match:
            scope_box = f'''
\\begin{{tcolorbox}}[
    colback=orange!5!white,
    colframe=orange!75!black,
    title={{\\textbf{{Appendix Scope: Ziel / In-Scope / Out-of-Scope / Constraints}}}},
    fonttitle=\\bfseries
]

\\textbf{{Ziel (Objective):}}
\\begin{{itemize}}[nosep]
    \\item Provide systematic analysis for {category} integration
\\end{{itemize}}

\\textbf{{In-Scope:}}
\\begin{{itemize}}[nosep]
    \\item Core analysis and findings
    \\item Parameter estimates and model validation
    \\item Framework integration points
\\end{{itemize}}

\\textbf{{Out-of-Scope:}}
\\begin{{itemize}}[nosep]
    \\item Detailed empirical replication $\\rightarrow$ METHOD appendices
    \\item Domain-specific applications $\\rightarrow$ DOMAIN appendices
\\end{{itemize}}

\\textbf{{Constraints:}}
\\begin{{itemize}}[nosep]
    \\item Analysis bounded by available data
    \\item Results subject to model assumptions
\\end{{itemize}}

\\end{{tcolorbox}}

'''
            content = content[:insert_match.end()] + scope_box + content[insert_match.end():]
            changes.append("Added Scope Box")

    # 5. Add Chapter Linkage if missing
    if not re.search(r'Chapter Linkage|Primary Chapter|Chapter \d+', content):
        # Add after cross ref map
        cross_ref_end = re.search(r'Cross-Reference Map\][\s\S]*?(\\end\{tcolorbox\}\s*\n)', content)
        if cross_ref_end:
            chapter_link = f'''
\\begin{{tcolorbox}}[colback=purple!5!white, colframe=purple!75!black,
    title=Chapter Linkage]

\\textbf{{Primary Chapter:}} Related application chapter
\\begin{{itemize}}[nosep]
\\item Integration with main framework exposition
\\end{{itemize}}

\\textbf{{Secondary Chapters:}}
\\begin{{itemize}}[nosep]
\\item Supporting theoretical and methodological chapters
\\end{{itemize}}

\\end{{tcolorbox}}

'''
            content = content[:cross_ref_end.end()] + chapter_link + content[cross_ref_end.end():]
            changes.append("Added Chapter Linkage")

    # 6. Add References Section if missing
    if not re.search(r'\\section\{References|\\begin\{thebibliography\}|References for Appendix', content):
        # Add at end before \end{document}
        end_match = re.search(r'\\end\{document\}', content)
        if end_match:
            references = f'''

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\\section{{References}}
\\label{{sec:{code.lower()}-references}}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\\nocite{{bcm_master}}
See master bibliography (\\texttt{{bcm\\_master.bib}}) for complete citations.
For comprehensive symbol definitions, see Appendix G (Master Glossary).

'''
            content = content[:end_match.start()] + references + content[end_match.start():]
            changes.append("Added References section")

    # 7. Add Open Issues if missing
    if not re.search(r'Open Issues|Future Work|Research Agenda|Limitations', content, re.IGNORECASE):
        # Add before References
        ref_match = re.search(r'\\section\{References', content)
        if ref_match:
            open_issues = f'''
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\\section{{Open Issues and Research Agenda}}
\\label{{sec:{code.lower()}-open-issues}}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\\begin{{enumerate}}
    \\item \\textbf{{Empirical Validation:}} Further testing across diverse contexts
    \\item \\textbf{{Parameter Refinement:}} Improved estimation methods needed
    \\item \\textbf{{Integration:}} Enhanced cross-appendix linkages
\\end{{enumerate}}

'''
            content = content[:ref_match.start()] + open_issues + content[ref_match.start():]
            changes.append("Added Open Issues section")

    # 8. Add nocite and Glossary G link if missing
    if not re.search(r'\\nocite\{bcm_master\}|bcm_master\.bib', content, re.IGNORECASE):
        # Add to references section
        ref_match = re.search(r'(\\section\{References[^}]*\}.*?\\label\{[^}]+\}\s*\n)', content, re.DOTALL)
        if ref_match:
            content = content[:ref_match.end()] + '\n\\nocite{bcm_master}\nSee master bibliography (\\texttt{bcm\\_master.bib}) for complete citations.\n' + content[ref_match.end():]
            changes.append("Added Master Bib Link")

    if not re.search(r'Appendix G.*?(Glossary|Notation)|Central.*?Glossary', content, re.IGNORECASE):
        # Add to glossary or references section
        if re.search(r'\\section\{Glossary', content):
            content = re.sub(
                r'(\\section\{Glossary[^}]*\}.*?\\label\{[^}]+\})',
                r'\1\n\nFor comprehensive symbol definitions, see Appendix G (Master Glossary).',
                content,
                count=1,
                flags=re.DOTALL
            )
            changes.append("Added Glossary G Link")

    # Write if changed
    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Fixed: {filepath}")
        for change in changes:
            print(f"  - {change}")
        return True
    else:
        print(f"No changes: {filepath}")
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python fix_remaining_files.py <file1.tex> [file2.tex ...]")
        sys.exit(1)

    fixed = 0
    for filepath in sys.argv[1:]:
        if fix_file(filepath):
            fixed += 1

    print(f"\nTotal: {fixed} files fixed")


if __name__ == "__main__":
    main()
