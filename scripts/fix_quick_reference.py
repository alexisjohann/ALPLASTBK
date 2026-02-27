#!/usr/bin/env python3
"""
Fix Quick Reference Box to include Appendix: or Category: marker.
Also adds Master Bib Link and Glossary G Link where missing.
"""

import re
import sys
from pathlib import Path
import subprocess


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


def extract_appendix_code(filepath: str, content: str) -> str:
    """Extract appendix code from filename or content."""
    # From filename
    fname = Path(filepath).stem
    parts = fname.split('_')
    if parts:
        code = parts[0].upper()
        if len(code) <= 3 and code.isalpha():
            return code

    # From label
    match = re.search(r'\\label\{app:([^}]+)\}', content)
    if match:
        return match.group(1).upper()

    return "?"


def extract_category(content: str) -> str:
    """Extract category from content."""
    match = re.search(r'% Category:\s*(\w+)', content)
    if match:
        cat = match.group(1).upper()
        if cat.endswith('-'):
            cat = cat[:-1]
        return cat
    return "UNKNOWN"


def fix_quick_reference(filepath: str) -> bool:
    """Fix Quick Reference box to include Appendix: marker."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    modified = False
    code = extract_appendix_code(filepath, content)
    category = extract_category(content)

    # Check if Quick Reference box already has Appendix: or Category:
    qr_match = re.search(r'(\\begin\{tcolorbox\}[^\]]*title=Quick Reference[^\]]*\])(.*?)(\\end\{tcolorbox\})',
                         content, re.DOTALL | re.IGNORECASE)

    if qr_match:
        qr_content = qr_match.group(2)
        if 'Appendix:' not in qr_content and 'Category:' not in qr_content:
            # Add Appendix marker at the beginning of the tcolorbox content
            new_qr_content = f'\n\\textbf{{Appendix:}} {code} ({category})\n' + qr_content
            content = content[:qr_match.start(2)] + new_qr_content + content[qr_match.end(2):]
            modified = True
            print(f"  + Added Appendix marker to Quick Reference")

    # Also try alternative Quick Reference pattern
    qr_match2 = re.search(r'(\\begin\{tcolorbox\}[^\]]*\[colback=.*?title=Quick Reference[^\]]*\])(.*?)(\\end\{tcolorbox\})',
                          content, re.DOTALL | re.IGNORECASE)

    if qr_match2 and not modified:
        qr_content = qr_match2.group(2)
        if 'Appendix:' not in qr_content and 'Category:' not in qr_content:
            new_qr_content = f'\n\\textbf{{Appendix:}} {code} ({category})\n' + qr_content
            content = content[:qr_match2.start(2)] + new_qr_content + content[qr_match2.end(2):]
            modified = True
            print(f"  + Added Appendix marker to Quick Reference")

    # Add Master Bib Link if missing
    if not re.search(r'\\nocite\{bcm_master\}', content):
        # Find References section or end
        ref_match = re.search(r'(\\section\{.*?References.*?\})', content, re.IGNORECASE)
        if ref_match:
            insert_pos = ref_match.end()
            content = content[:insert_pos] + '\n\n\\nocite{bcm_master}\n' + content[insert_pos:]
            modified = True
            print(f"  + Added Master Bib Link")
        elif '\\end{document}' in content:
            content = content.replace('\\end{document}',
                '\n% Link to master bibliography\n\\nocite{bcm_master}\n\n\\end{document}')
            modified = True
            print(f"  + Added Master Bib Link")

    # Add Glossary G Link if missing and has Glossary section
    if re.search(r'\\section\{.*?Glossary', content, re.IGNORECASE):
        if not re.search(r'Appendix\s*G|\\ref\{app:g\}|Glossary.*master|comprehensive', content, re.IGNORECASE):
            # Add link after Glossary section header
            content = re.sub(
                r'(\\section\{.*?Glossary.*?\})',
                r'\1\n\nFor comprehensive definitions, see Appendix G (Master Glossary).\n',
                content,
                count=1,
                flags=re.IGNORECASE
            )
            modified = True
            print(f"  + Added Glossary G Link")

    # Add References section if missing
    if not re.search(r'\\section\{.*?References', content, re.IGNORECASE):
        # Find Open Issues or end
        patterns = [
            r'(\\section\{.*?Open Issues)',
            r'(% =+\n% END)',
            r'(\\end\{document\})',
        ]
        for pattern in patterns:
            match = re.search(pattern, content)
            if match:
                refs_section = '''
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\\section{References}
\\label{sec:references}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

See master bibliography (\\texttt{bcm\\_master.bib}) for complete citations.

\\nocite{bcm_master}

'''
                content = content[:match.start()] + refs_section + content[match.start():]
                modified = True
                print(f"  + Added References Section")
                break

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    return modified


def main():
    if '--all' in sys.argv:
        appendix_dir = Path('appendices')
        fixed = 0
        for f in sorted(appendix_dir.glob('*.tex')):
            if 'template' not in f.name.lower() and 'index' not in f.name.lower():
                score = get_compliance(str(f))
                if score < 95:
                    print(f"\n[{score:.1f}%] {f.name}")
                    if fix_quick_reference(str(f)):
                        fixed += 1
                        new_score = get_compliance(str(f))
                        print(f"  → {new_score:.1f}%")
        print(f"\nTotal: {fixed} files fixed")
    else:
        for filepath in sys.argv[1:]:
            print(f"Fixing: {filepath}")
            fix_quick_reference(filepath)


if __name__ == '__main__':
    main()
