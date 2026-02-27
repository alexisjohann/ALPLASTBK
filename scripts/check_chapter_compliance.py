#!/usr/bin/env python3
"""
EBF Chapter Template Compliance Checker v1.0
=============================================

Prüft Kapitel auf Einhaltung des Templates (chapters/00_chapter_template.tex)
MIT KAPITELTYP-SPEZIFISCHEN ANFORDERUNGEN

DIE 3 KAPITELTYPEN:
- TYPE A: CORE Chapters (5, 9, 10, 11, 12, 13) - CORE Connection Box PFLICHT
- TYPE B: Foundation Chapters (1-4, 6-8) - Standard-Struktur
- TYPE C: Application Chapters (14-19) - Multiple Worked Examples PFLICHT

KAPITELSTRUKTUR (alle Typen):
- HEADER: Metadata, Navigation Box, Appendix References Box
- OPENING: Opening paragraph, Intuition Box, Central Question, Chapter Overview
- CORE CONTENT: Subsections with labels, Definition/Intuition environments
- WORKED EXAMPLES: At least one concrete example
- CLOSING: Summary, Formal Details, What Comes Next, Reading Path Box
"""

import re
import sys
import os

# =============================================================================
# KAPITELTYP-DEFINITIONEN
# =============================================================================

CHAPTER_CONFIG = {
    'A': {
        'name': 'CORE Chapter',
        'description': 'Has dedicated CORE appendix - requires CORE Connection Box',
        'weights': {'header': 0.15, 'opening': 0.20, 'content': 0.30, 'examples': 0.15, 'closing': 0.20},
        'required': ['core_connection_box', '10c_integration', 'intuition_box', 'worked_example', 'reading_path'],
        'optional': [],
        'chapters': [5, 9, 10, 11, 12, 13]
    },
    'B': {
        'name': 'Foundation Chapter',
        'description': 'Builds conceptual groundwork - standard structure',
        'weights': {'header': 0.15, 'opening': 0.25, 'content': 0.30, 'examples': 0.10, 'closing': 0.20},
        'required': ['intuition_box', 'central_question', 'chapter_overview', 'reading_path'],
        'optional': ['core_connection_box', '10c_integration'],  # Not required for Type B
        'chapters': [1, 2, 3, 4, 6, 7, 8]
    },
    'C': {
        'name': 'Application Chapter',
        'description': 'Applies framework to practice - multiple examples required',
        'weights': {'header': 0.10, 'opening': 0.15, 'content': 0.25, 'examples': 0.30, 'closing': 0.20},
        'required': ['multiple_examples', 'policy_implications', 'reading_path'],
        'optional': ['core_connection_box', '10c_integration'],
        'chapters': [14, 15, 16, 17, 18, 19]
    }
}

# Mapping von Kapitelnummern zu Typen
CHAPTER_TO_TYPE = {}
for type_code, config in CHAPTER_CONFIG.items():
    for ch_num in config['chapters']:
        CHAPTER_TO_TYPE[ch_num] = type_code

DEFAULT_WEIGHTS = {'header': 0.15, 'opening': 0.20, 'content': 0.30, 'examples': 0.15, 'closing': 0.20}


def detect_chapter_type(content: str, filename: str) -> tuple[str, dict, int]:
    """Erkennt den Kapiteltyp aus Inhalt oder Dateiname."""

    # Extrahiere Kapitelnummer aus Dateiname (z.B. "01" aus "01_introduction.tex")
    basename = os.path.basename(filename)
    match = re.match(r'^(\d+)_', basename)
    chapter_num = int(match.group(1)) if match else None

    # Suche in Inhalt nach Chapter Type Tag
    type_match = re.search(r'Chapter Type:\s*([ABC])\s*\(', content, re.IGNORECASE)
    if type_match:
        type_code = type_match.group(1).upper()
        if type_code in CHAPTER_CONFIG:
            return type_code, CHAPTER_CONFIG[type_code], chapter_num

    # Fallback: Bestimme Typ aus Kapitelnummer
    if chapter_num and chapter_num in CHAPTER_TO_TYPE:
        type_code = CHAPTER_TO_TYPE[chapter_num]
        return type_code, CHAPTER_CONFIG[type_code], chapter_num

    # Default: Type B (Foundation)
    return 'B', CHAPTER_CONFIG['B'], chapter_num


def check_compliance(content: str, chapter_name: str) -> dict:
    """Prüft Template-Compliance mit kapiteltyp-spezifischen Anforderungen."""

    # Kapiteltyp erkennen
    type_code, type_config, chapter_num = detect_chapter_type(content, chapter_name)
    weights = type_config['weights']

    results = {
        'chapter': chapter_name,
        'chapter_num': chapter_num,
        'type_code': type_code,
        'type_name': type_config['name'],
        'type_description': type_config['description'],
        'weights': weights,
        'required_fields': type_config['required'],
        'optional_fields': type_config['optional'],
        'header': {},
        'opening': {},
        'content': {},
        'examples': {},
        'closing': {},
        'scores': {},
        'total': 0
    }

    # ==========================================================================
    # HEADER
    # ==========================================================================
    h = results['header']

    # Metadata block: Multiple patterns accepted
    # - "% CHAPTER N:" or "% Chapter N:" (uppercase or mixed case)
    # - "% Chapter 4x:" (with letter suffix)
    # - "HEADER BLOCK" section header
    # - Lines of === or --- followed by chapter info
    h['metadata_block'] = bool(
        re.search(r'%\s*CHAPTER\s+\d+[a-z]?:', content, re.IGNORECASE) or
        re.search(r'HEADER BLOCK', content) or
        re.search(r'%[-=]+\s*\n%\s*Document:', content)
    )
    h['version'] = bool(re.search(r'%\s*Version:\s*\d+\.\d+', content))
    h['purpose'] = bool(re.search(r'%\s*Purpose:', content))
    h['appendix_refs'] = bool(re.search(r'%\s*(Primary|Secondary) Appendix', content))
    h['prerequisites'] = bool(re.search(r'%\s*Prerequisites:', content))
    h['leads_to'] = bool(re.search(r'%\s*Leads to:', content))
    h['chapter_type_declared'] = bool(re.search(r'%\s*Chapter Type:\s*[ABC]', content))
    h['appendix_references_box'] = bool(re.search(r'Appendix References for This Chapter|colframe=orange', content))

    h_score = sum(h.values()) / len(h) * 100
    results['scores']['header'] = h_score

    # ==========================================================================
    # OPENING
    # ==========================================================================
    o = results['opening']

    o['quick_reference_box'] = bool(re.search(r'Begriffe in diesem Kapitel|Quick Reference', content, re.IGNORECASE))
    o['intuition_box'] = bool(re.search(r'Why.*?Matters|Intuition|Anna|Thomas', content, re.IGNORECASE))
    o['central_question'] = bool(re.search(r'Central Question|Foundational Question', content, re.IGNORECASE))
    o['chapter_overview'] = bool(re.search(r'Chapter Overview|proceeds as follows', content, re.IGNORECASE))
    o['core_connection_box'] = bool(re.search(r'10C CORE Connection|CORE Connection', content))

    # Kategorie-spezifische Score-Berechnung
    o_items = []
    for key, val in o.items():
        if key in type_config['optional']:
            if val:
                o_items.append(1)
        else:
            o_items.append(1 if val else 0)

    o_score = (sum(o_items) / len(o_items) * 100) if o_items else 0
    results['scores']['opening'] = o_score

    # ==========================================================================
    # CONTENT
    # ==========================================================================
    c = results['content']

    c['section_labels'] = bool(re.search(r'\\label\{sec:', content))
    c['multiple_subsections'] = len(re.findall(r'\\subsection\{', content)) >= 3
    c['equations'] = bool(re.search(r'\\begin\{equation\}', content))
    c['tables'] = bool(re.search(r'\\begin\{table\}|\\begin\{tabular\}', content))
    c['cross_references'] = bool(re.search(r'\\ref\{sec:|See (Chapter|Section|Appendix)', content))
    c['10c_integration'] = bool(re.search(r'10C.*?Integration|CORE.*?relates|Pipeline', content, re.IGNORECASE))

    # Kategorie-spezifische Score-Berechnung
    c_items = []
    for key, val in c.items():
        if key in type_config['optional']:
            if val:
                c_items.append(1)
        else:
            c_items.append(1 if val else 0)

    c_score = (sum(c_items) / len(c_items) * 100) if c_items else 0
    results['scores']['content'] = c_score

    # ==========================================================================
    # EXAMPLES
    # ==========================================================================
    e = results['examples']

    worked_examples = re.findall(r'Worked Example|Example \d+:|Anna|Thomas|Step \d+:', content, re.IGNORECASE)
    e['worked_example'] = len(worked_examples) >= 1
    e['multiple_examples'] = len(worked_examples) >= 2
    e['named_characters'] = bool(re.search(r'Anna|Thomas|Maria|Peter', content))
    e['numbers'] = bool(re.search(r'\d+%|\$\d+|=\s*\d+\.\d+', content))

    # Kategorie-spezifische Score-Berechnung
    e_items = []
    for key, val in e.items():
        if key in type_config['optional']:
            if val:
                e_items.append(1)
        elif key == 'multiple_examples' and type_code != 'C':
            # Only required for Type C
            if val:
                e_items.append(1)
        else:
            e_items.append(1 if val else 0)

    e_score = (sum(e_items) / len(e_items) * 100) if e_items else 0
    results['scores']['examples'] = e_score

    # ==========================================================================
    # CLOSING
    # ==========================================================================
    cl = results['closing']

    # Summary: section/subsection or tcolorbox with Summary in title
    cl['summary'] = bool(re.search(r'\\(sub)?section\{Summary|title=.*Summary|Key Points', content))
    cl['enumerated_points'] = bool(re.search(r'This chapter has established:|\\begin\{enumerate\}.*?\\textbf\{|Key Results:', content, re.DOTALL))
    cl['formal_details'] = bool(re.search(r'Formal Details|complete formal treatment|formal treatment appears', content, re.IGNORECASE))
    cl['what_comes_next'] = bool(re.search(r'What Comes Next|Chapter.*?introduces|Transition:', content))
    cl['reading_path'] = bool(re.search(r'Reading Path|colframe=green', content))
    cl['policy_implications'] = bool(re.search(r'Policy Implications|Practical Implications|Application', content, re.IGNORECASE))

    # Kategorie-spezifische Score-Berechnung
    cl_items = []
    for key, val in cl.items():
        if key in type_config['optional']:
            if val:
                cl_items.append(1)
        elif key == 'policy_implications' and type_code != 'C':
            # Only required for Type C
            if val:
                cl_items.append(1)
        else:
            cl_items.append(1 if val else 0)

    cl_score = (sum(cl_items) / len(cl_items) * 100) if cl_items else 0
    results['scores']['closing'] = cl_score

    # ==========================================================================
    # GESAMTSCORE BERECHNUNG (mit kapiteltyp-spezifischen Gewichten)
    # ==========================================================================

    weighted_score = (
        h_score * weights['header'] +
        o_score * weights['opening'] +
        c_score * weights['content'] +
        e_score * weights['examples'] +
        cl_score * weights['closing']
    )

    # PENALTY für fehlende kritische Elemente
    penalty = 0

    if 'intuition_box' in type_config['required'] and not o['intuition_box']:
        penalty += 10

    if 'reading_path' in type_config['required'] and not cl['reading_path']:
        penalty += 10

    if type_code == 'A' and not o['core_connection_box']:
        penalty += 15  # CORE chapters MUST have CORE Connection Box

    if type_code == 'C' and not e['multiple_examples']:
        penalty += 10  # Application chapters need multiple examples

    # Bonus für erfüllte Required-Felder
    all_fields = {**h, **o, **c, **e, **cl}
    required_met = sum(1 for r in type_config['required'] if r in all_fields and all_fields.get(r, False))
    required_total = len([r for r in type_config['required'] if r in all_fields])

    results['required_compliance'] = f"{required_met}/{required_total}"
    results['penalty'] = penalty
    results['weighted_score'] = weighted_score
    results['total'] = max(0, weighted_score - penalty)

    return results


def print_report(results: dict):
    """Druckt einen formatierten Report mit Kapiteltyp-Info."""

    weights = results['weights']

    print(f"\n{'='*70}")
    print(f"CHAPTER TEMPLATE COMPLIANCE REPORT: {results['chapter']}")
    print(f"{'='*70}")

    # Kapiteltyp-Info
    print(f"\n📖 KAPITELTYP: {results['type_code']} ({results['type_name']})")
    print(f"   {results['type_description']}")
    print(f"   Gewichte: H={weights['header']:.0%} O={weights['opening']:.0%} C={weights['content']:.0%} E={weights['examples']:.0%} CL={weights['closing']:.0%}")
    if results['required_fields']:
        print(f"   Required: {', '.join(results['required_fields'])}")
    if results['optional_fields']:
        print(f"   Optional: {', '.join(results['optional_fields'])}")

    # Header
    print(f"\n📋 HEADER ({weights['header']:.0%}): {results['scores']['header']:.0f}%")
    for key, val in results['header'].items():
        status = "✅" if val else "❌"
        req_mark = " ★" if key in results['required_fields'] else ""
        opt_mark = " (optional)" if key in results['optional_fields'] else ""
        print(f"   {status} {key.replace('_', ' ').title()}{req_mark}{opt_mark}")

    # Opening
    print(f"\n🎯 OPENING ({weights['opening']:.0%}): {results['scores']['opening']:.0f}%")
    for key, val in results['opening'].items():
        status = "✅" if val else "❌"
        req_mark = " ★" if key in results['required_fields'] else ""
        opt_mark = " (optional)" if key in results['optional_fields'] else ""
        print(f"   {status} {key.replace('_', ' ').title()}{req_mark}{opt_mark}")

    # Content
    print(f"\n📚 CONTENT ({weights['content']:.0%}): {results['scores']['content']:.0f}%")
    for key, val in results['content'].items():
        status = "✅" if val else "❌"
        req_mark = " ★" if key in results['required_fields'] else ""
        opt_mark = " (optional)" if key in results['optional_fields'] else ""
        print(f"   {status} {key.replace('_', ' ').title()}{req_mark}{opt_mark}")

    # Examples
    print(f"\n🔧 EXAMPLES ({weights['examples']:.0%}): {results['scores']['examples']:.0f}%")
    for key, val in results['examples'].items():
        status = "✅" if val else "❌"
        req_mark = " ★" if key in results['required_fields'] else ""
        opt_mark = " (optional)" if key in results['optional_fields'] else ""
        print(f"   {status} {key.replace('_', ' ').title()}{req_mark}{opt_mark}")

    # Closing
    print(f"\n📖 CLOSING ({weights['closing']:.0%}): {results['scores']['closing']:.0f}%")
    for key, val in results['closing'].items():
        status = "✅" if val else "❌"
        req_mark = " ★" if key in results['required_fields'] else ""
        opt_mark = " (optional)" if key in results['optional_fields'] else ""
        print(f"   {status} {key.replace('_', ' ').title()}{req_mark}{opt_mark}")

    # Gesamtscore
    print(f"\n{'─'*70}")
    print(f"   Required Fields:  {results['required_compliance']}")
    print(f"   Weighted Score:   {results['weighted_score']:.1f}%")
    if results['penalty'] > 0:
        print(f"   Penalty:         -{results['penalty']}% (missing critical elements)")
    print(f"   ═══════════════════════════════════════")
    print(f"   TOTAL SCORE:      {results['total']:.1f}%")
    print(f"{'─'*70}")

    # Bewertung
    if results['total'] >= 95:
        grade = "🏆 EXCELLENT"
    elif results['total'] >= 85:
        grade = "✅ GOOD"
    elif results['total'] >= 70:
        grade = "⚠️  ACCEPTABLE"
    elif results['total'] >= 50:
        grade = "⚠️  NEEDS WORK"
    else:
        grade = "❌ NON-COMPLIANT"

    print(f"   GRADE: {grade}")
    print(f"{'='*70}\n")


def print_chapter_types():
    """Druckt Übersicht aller Kapiteltypen."""
    print(f"\n{'='*70}")
    print("EBF CHAPTER TYPES")
    print(f"{'='*70}\n")

    for type_code, config in CHAPTER_CONFIG.items():
        w = config['weights']
        print(f"📁 TYPE {type_code}: {config['name']}")
        print(f"   {config['description']}")
        print(f"   Chapters: {', '.join(str(c) for c in config['chapters'])}")
        print(f"   Gewichte: H={w['header']:.0%} O={w['opening']:.0%} C={w['content']:.0%} E={w['examples']:.0%} CL={w['closing']:.0%}")
        print(f"   Required: {', '.join(config['required']) or 'Standard'}")
        print(f"   Optional: {', '.join(config['optional']) or '-'}")
        print()

    print("\nSTRUCTURE CHECKLIST (all chapters):")
    print("""
   HEADER:
   [ ] Metadata block (version, purpose, appendices, prerequisites)
   [ ] Chapter Type declaration
   [ ] Appendix References Box

   OPENING:
   [ ] Quick Reference Box
   [ ] Intuition Box (with named characters: Anna, Thomas)
   [ ] Central Question Box
   [ ] Chapter Overview (with section references)
   [ ] CORE Connection Box (TYPE A only)

   CONTENT:
   [ ] Section labels (\\label{sec:...})
   [ ] Multiple subsections (≥3)
   [ ] Equations and tables
   [ ] Cross-references
   [ ] 10C Integration (TYPE A only)

   EXAMPLES:
   [ ] At least one worked example
   [ ] Named characters
   [ ] Concrete numbers
   [ ] Multiple examples (TYPE C only)

   CLOSING:
   [ ] Summary with enumerated points
   [ ] Formal Details paragraph
   [ ] What Comes Next paragraph
   [ ] Reading Path Box
   [ ] Policy Implications (TYPE C only)
""")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == '--types':
            print_chapter_types()
        else:
            with open(sys.argv[1], 'r') as f:
                content = f.read()
            results = check_compliance(content, sys.argv[1])
            print_report(results)
    else:
        print("Usage: python check_chapter_compliance.py <chapter.tex>")
        print("       python check_chapter_compliance.py --types")
