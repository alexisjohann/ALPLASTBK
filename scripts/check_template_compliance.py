#!/usr/bin/env python3
"""
EBF Template Compliance Checker v2.1
=========================================

Prüft Appendices auf Einhaltung des Templates (00_appendix_template.tex)
MIT KATEGORIE-SPEZIFISCHEN ANFORDERUNGEN UND SPRACHKONSISTENZ

SPRACH-REGEL:
- Eine Sprache pro Dokument (keine Mischung)
- Default: Deutsch
- Explizite Ausnahme: "% Language: English" im Header

DIE 8 KATEGORIEN:
- CORE-   : Core Theory (AAA, B, C, V, BBB, AU, AV) - Axiome + Foundations PFLICHT
- FORMAL- : Formalization (A, D) - Beweise + Axiome PFLICHT
- DOMAIN- : Applications (AA-AG, AJ, AK, W-Z) - Worked Examples PFLICHT
- CONTEXT-: Context (AH, AI) - Ψ-Integration PFLICHT
- METHOD- : Methodology (AN, AL, E, R) - Validierung PFLICHT
- PREDICT-: Predictions (S, AO-AT) - Testbare Hypothesen PFLICHT
- LIT-    : Literature (I-Q, U) - Axiome OPTIONAL
- REF-    : Reference (F, G, H, T) - Tutorial-Format PFLICHT

KATEGORIE-SPEZIFISCHE GEWICHTUNG:
- CORE/FORMAL: Core Content 40%, Back Matter 35%
- DOMAIN/METHOD: Application 25%
- LIT: Core Content 25%, Back Matter 40%
- REF: Application 30%
"""

import re
import sys
import os

# =============================================================================
# KATEGORIE-DEFINITIONEN
# =============================================================================

CATEGORY_CONFIG = {
    'CORE': {
        'description': 'Core Theory - Beantwortet 10C Fragen',
        'weights': {'front_matter': 0.15, 'core_content': 0.40, 'application': 0.10, 'back_matter': 0.35},
        'required': ['axioms', 'foundations', 'glossary_g_link', 'master_bib_link'],
        'optional': [],
        'appendices': ['AAA', 'B', 'C', 'V', 'BBB', 'AU', 'AV', 'AW']
    },
    'FORMAL': {
        'description': 'Formalization - Mathematische Strenge',
        'weights': {'front_matter': 0.15, 'core_content': 0.45, 'application': 0.10, 'back_matter': 0.30},
        'required': ['axioms', 'theory', 'glossary_g_link', 'master_bib_link'],
        'optional': ['worked_example'],  # Beweise statt Beispiele
        'appendices': ['A', 'D']
    },
    'DOMAIN': {
        'description': 'Domain Applications - Anwendungsfelder',
        'weights': {'front_matter': 0.15, 'core_content': 0.30, 'application': 0.25, 'back_matter': 0.30},
        'required': ['worked_example', 'implications', 'integration'],
        'optional': ['axioms'],  # Anwendungen brauchen keine eigenen Axiome
        'appendices': ['AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AJ', 'AK', 'W', 'X', 'Y', 'Z', 'AW', 'AX']
    },
    'CONTEXT': {
        'description': 'Context Analysis - Ψ-Dimensionen',
        'weights': {'front_matter': 0.20, 'core_content': 0.35, 'application': 0.15, 'back_matter': 0.30},
        'required': ['integration', 'theory'],  # Muss mit V integrieren
        'optional': ['axioms'],
        'appendices': ['AH', 'AI']
    },
    'METHOD': {
        'description': 'Methodology - Messung & Validierung',
        'weights': {'front_matter': 0.15, 'core_content': 0.30, 'application': 0.25, 'back_matter': 0.30},
        'required': ['worked_example', 'results'],  # Empirische Validierung
        'optional': ['axioms'],
        'appendices': ['AN', 'AL', 'E', 'R', 'AZ']
    },
    'METHOD-SWSM': {
        'description': 'Scientific Writing Structure Model - Text Analysis & Generation',
        'weights': {'front_matter': 0.10, 'core_content': 0.35, 'application': 0.25, 'back_matter': 0.30},
        'required': [
            'axioms',           # SWSM-1 bis SWSM-20
            'worked_example',   # Fehr-Profil Extraktion + Generation
            'results',          # Empirische Validierung
            'swsm_components',  # E1-E9 alle dokumentiert
            'swsm_theta',       # θ Parameter-Schema
            'swsm_deprecation', # 8D → θ Migration
        ],
        'optional': [],
        'appendices': ['SW'],
        'swsm_specific': True  # Flag für SWSM-spezifische Checks
    },
    'PREDICT': {
        'description': 'Predictions - Testbare Vorhersagen',
        'weights': {'front_matter': 0.15, 'core_content': 0.40, 'application': 0.15, 'back_matter': 0.30},
        'required': ['results', 'implications'],  # Vorhersagen + Implikationen
        'optional': ['axioms'],
        'appendices': ['S', 'AO', 'AP', 'AQ', 'AR', 'AS', 'AT']
    },
    'LIT': {
        'description': 'Literature - Forschungsintegration',
        'weights': {'front_matter': 0.15, 'core_content': 0.25, 'application': 0.15, 'back_matter': 0.45},
        'required': ['integration', 'references_section'],  # Literatur-Fokus
        'optional': ['axioms', 'worked_example'],  # Literaturübersicht braucht keine
        'appendices': ['I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'U', 'AY']
    },
    'REF': {
        'description': 'Reference - Nachschlagewerke & Tutorials',
        'weights': {'front_matter': 0.15, 'core_content': 0.25, 'application': 0.30, 'back_matter': 0.30},
        'required': ['worked_example'],  # Tutorial-Format PFLICHT
        'optional': ['axioms', 'foundations'],  # Referenzmaterial braucht keine
        'appendices': ['F', 'G', 'H', 'T']
    }
}

# Default für unbekannte Kategorien
DEFAULT_WEIGHTS = {'front_matter': 0.20, 'core_content': 0.35, 'application': 0.15, 'back_matter': 0.30}

# =============================================================================
# SPRACHKONSISTENZ-PRÜFUNG
# =============================================================================

# Typische Wörter für Spracherkennung (außerhalb von LaTeX-Commands)
GERMAN_INDICATORS = [
    r'\bund\b', r'\boder\b', r'\bfür\b', r'\bmit\b', r'\bvon\b', r'\bzu\b',
    r'\bdas\b', r'\bdie\b', r'\bder\b', r'\bein\b', r'\beine\b', r'\beiner\b',
    r'\bist\b', r'\bsind\b', r'\bwird\b', r'\bwerden\b', r'\bwurde\b',
    r'\bkann\b', r'\bkönnen\b', r'\bsoll\b', r'\bsollen\b',
    r'\bsiehe\b', r'\bbeispiel\b', r'\babschnitt\b', r'\bkapitel\b',
    r'\bdefinition\b', r'\bgleichung\b', r'\btabelle\b', r'\babbildung\b',
    r'\bzusammenfassung\b', r'\bergebnis\b', r'\bfrage\b', r'\bantwort\b',
    r'\bwichtig\b', r'\bhier\b', r'\bdaher\b', r'\bdadurch\b', r'\bjedoch\b',
]

ENGLISH_INDICATORS = [
    r'\band\b', r'\bor\b', r'\bfor\b', r'\bwith\b', r'\bfrom\b', r'\bto\b',
    r'\bthe\b', r'\ba\b', r'\ban\b', r'\bthis\b', r'\bthat\b', r'\bthese\b',
    r'\bis\b', r'\bare\b', r'\bwas\b', r'\bwere\b', r'\bbeen\b',
    r'\bcan\b', r'\bcould\b', r'\bshould\b', r'\bwould\b', r'\bmay\b',
    r'\bsee\b', r'\bexample\b', r'\bsection\b', r'\bchapter\b',
    r'\bdefinition\b', r'\bequation\b', r'\btable\b', r'\bfigure\b',
    r'\bsummary\b', r'\bresult\b', r'\bquestion\b', r'\banswer\b',
    r'\bimportant\b', r'\bhere\b', r'\btherefore\b', r'\bhowever\b', r'\bthus\b',
]


def detect_language(content: str) -> dict:
    """
    Erkennt die Sprache des Dokuments und prüft auf Konsistenz.

    Returns:
        dict mit:
        - declared: Explizit deklarierte Sprache (oder None)
        - detected: Erkannte Hauptsprache ('de', 'en', 'mixed')
        - german_count: Anzahl deutscher Indikatoren
        - english_count: Anzahl englischer Indikatoren
        - consistent: True wenn konsistent, False wenn gemischt
        - issues: Liste von Problemen
    """
    result = {
        'declared': None,
        'detected': 'unknown',
        'german_count': 0,
        'english_count': 0,
        'consistent': True,
        'issues': []
    }

    # 1. Prüfe auf explizite Sprachdeklaration
    lang_match = re.search(r'%\s*Language:\s*(German|Deutsch|English|Englisch)', content, re.IGNORECASE)
    if lang_match:
        lang = lang_match.group(1).lower()
        result['declared'] = 'de' if lang in ['german', 'deutsch'] else 'en'

    # 2. Entferne LaTeX-Commands und Mathe für saubere Analyse
    # Behalte nur Text außerhalb von \command{...} und $...$
    clean_content = re.sub(r'\\[a-zA-Z]+\{[^}]*\}', ' ', content)
    clean_content = re.sub(r'\\[a-zA-Z]+', ' ', clean_content)
    clean_content = re.sub(r'\$[^$]+\$', ' ', clean_content)
    clean_content = re.sub(r'\\\[[^\]]+\\\]', ' ', clean_content)
    clean_content = re.sub(r'%.*$', ' ', clean_content, flags=re.MULTILINE)
    clean_content = clean_content.lower()

    # 3. Zähle Indikatoren
    for pattern in GERMAN_INDICATORS:
        result['german_count'] += len(re.findall(pattern, clean_content, re.IGNORECASE))

    for pattern in ENGLISH_INDICATORS:
        result['english_count'] += len(re.findall(pattern, clean_content, re.IGNORECASE))

    # 4. Bestimme Hauptsprache
    total = result['german_count'] + result['english_count']
    if total < 20:
        result['detected'] = 'unknown'
        result['issues'].append('Zu wenig Text für Spracherkennung')
    else:
        german_ratio = result['german_count'] / total
        english_ratio = result['english_count'] / total

        if german_ratio > 0.7:
            result['detected'] = 'de'
        elif english_ratio > 0.7:
            result['detected'] = 'en'
        else:
            result['detected'] = 'mixed'
            result['consistent'] = False
            result['issues'].append(f'Gemischte Sprache: {german_ratio:.0%} DE, {english_ratio:.0%} EN')

    # 5. Prüfe Konsistenz mit Deklaration
    if result['declared'] and result['detected'] != 'unknown':
        if result['declared'] != result['detected'] and result['detected'] != 'mixed':
            result['consistent'] = False
            result['issues'].append(f"Deklariert: {result['declared'].upper()}, Erkannt: {result['detected'].upper()}")

    # 6. Default-Regel: Deutsch erwartet wenn nicht deklariert
    if not result['declared'] and result['detected'] == 'en':
        result['issues'].append('Englisch ohne Deklaration (Default ist Deutsch)')

    return result


def detect_category(content: str, filename: str) -> tuple[str, dict]:
    """Erkennt die Kategorie aus Inhalt oder Dateiname."""

    # Extrahiere Appendix-Code aus Dateiname (z.B. "AAA" aus "AAA_aggregation_levels.tex")
    basename = os.path.basename(filename)
    match = re.match(r'^([A-Z]+)_', basename)
    appendix_code = match.group(1) if match else None

    # Suche in Inhalt nach Category-Tag
    cat_match = re.search(r'Category:\s*(CORE|FORMAL|DOMAIN|CONTEXT|METHOD|PREDICT|LIT|REF)', content, re.IGNORECASE)
    if cat_match:
        category = cat_match.group(1).upper()
        if category in CATEGORY_CONFIG:
            return category, CATEGORY_CONFIG[category]

    # Fallback: Suche nach Appendix-Code in den Kategorien
    if appendix_code:
        for cat_name, cat_config in CATEGORY_CONFIG.items():
            if appendix_code in cat_config['appendices']:
                return cat_name, cat_config

    # Default: Unbekannt
    return 'UNKNOWN', {
        'description': 'Unbekannte Kategorie',
        'weights': DEFAULT_WEIGHTS,
        'required': [],
        'optional': [],
        'appendices': []
    }


def check_swsm_specific(content: str) -> dict:
    """
    SWSM-spezifische Compliance-Checks für Appendix SW.

    Prüft:
    - Alle 9 Komponenten (E1-E9) dokumentiert
    - Alle 20 Axiome (SWSM-1 bis SWSM-20) definiert
    - θ Parameter-Schema vollständig (6 Kategorien)
    - 8D Deprecation Notice vorhanden
    - Worked Examples für Extraktion und Generation
    """
    swsm = {
        'components': {},
        'axioms': {},
        'theta': {},
        'deprecation': {},
        'examples': {},
        'score': 0
    }

    # ==========================================================================
    # E1-E9 KOMPONENTEN (9 required)
    # ==========================================================================
    components = {
        'E1': r'E1.*?Cohesion|Cohesion.*?Analyzer|E1[:\s]',
        'E2': r'E2.*?RST|RST.*?Discourse|Rhetorical Structure|E2[:\s]',
        'E3': r'E3.*?CARS|Move.*?Tagger|Swales|E3[:\s]',
        'E4': r'E4.*?Theme|Theme.*?Rheme|Information.*?Structure|E4[:\s]',
        'E5': r'E5.*?SFL|Clause.*?Annotator|Lexicogrammar|E5[:\s]',
        'E6': r'E6.*?Lexicogrammar|Profiler|E6[:\s]',
        'E7': r'E7.*?Genre|Genre.*?Classifier|E7[:\s]',
        'E8': r'E8.*?Move.*?Planner|Document.*?Planning|E8[:\s]',
        'E9': r'E9.*?Text.*?Generator|Generation|E9[:\s]',
    }

    for comp, pattern in components.items():
        swsm['components'][comp] = bool(re.search(pattern, content, re.IGNORECASE))

    comp_count = sum(swsm['components'].values())
    swsm['components']['_score'] = comp_count / 9 * 100
    swsm['components']['_count'] = f"{comp_count}/9"

    # ==========================================================================
    # SWSM AXIOME (mindestens 10 der 20 erwartet)
    # ==========================================================================
    axiom_patterns = [
        r'SWSM-1[:\s]|Stratal.*?Organization',
        r'SWSM-2[:\s]|Rank.*?Scale',
        r'SWSM-3[:\s]|Metafunction',
        r'SWSM-4[:\s]|Instantiation',
        r'SWSM-5[:\s]|Cohesion.*?Axiom',
        r'SWSM-6[:\s]|RST.*?Axiom',
        r'SWSM-7[:\s]|CARS.*?Axiom',
        r'SWSM-8[:\s]|Genre.*?Emergence',
        r'SWSM-9[:\s]|Style.*?Percolation',
        r'SWSM-10[:\s]|Parameter.*?Extraction',
        r'SWSM-11[:\s]',
        r'SWSM-12[:\s]|Domain.*?Specialization',
        r'SWSM-13[:\s]',
        r'SWSM-14[:\s]',
        r'SWSM-15[:\s]',
        r'SWSM-16[:\s]|Quantitative.*?Bounds',
        r'SWSM-17[:\s]',
        r'SWSM-18[:\s]',
        r'SWSM-19[:\s]',
        r'SWSM-20[:\s]',
    ]

    axiom_count = 0
    for i, pattern in enumerate(axiom_patterns, 1):
        found = bool(re.search(pattern, content, re.IGNORECASE))
        swsm['axioms'][f'SWSM-{i}'] = found
        if found:
            axiom_count += 1

    swsm['axioms']['_score'] = min(100, axiom_count / 10 * 100)  # 10 Axiome = 100%
    swsm['axioms']['_count'] = f"{axiom_count}/20"

    # ==========================================================================
    # θ PARAMETER-SCHEMA (6 Kategorien required)
    # ==========================================================================
    theta_patterns = {
        'theta_move': r'θ_move|theta_move|\\theta.*?move|Move.*?Parameter',
        'theta_cohesion': r'θ_cohesion|theta_cohesion|\\theta.*?cohesion|Cohesion.*?Parameter',
        'theta_rst': r'θ_rst|theta_rst|\\theta.*?rst|RST.*?Parameter',
        'theta_lexicogrammar': r'θ_lexicogrammar|theta_lexicogrammar|\\theta.*?lexicogrammar|Lexicogrammar.*?Parameter',
        'theta_info': r'θ_info|theta_info|\\theta.*?info|Information.*?Parameter',
        'theta_vocab': r'θ_vocab|theta_vocab|\\theta.*?vocab|Vocabulary.*?Parameter',
    }

    for theta, pattern in theta_patterns.items():
        swsm['theta'][theta] = bool(re.search(pattern, content, re.IGNORECASE))

    theta_count = sum(swsm['theta'].values())
    swsm['theta']['_score'] = theta_count / 6 * 100
    swsm['theta']['_count'] = f"{theta_count}/6"

    # ==========================================================================
    # 8D DEPRECATION NOTICE
    # ==========================================================================
    swsm['deprecation']['8d_mentioned'] = bool(re.search(r'8D|8-D|eight.*?dimension', content, re.IGNORECASE))
    swsm['deprecation']['deprecated'] = bool(re.search(r'deprecat|obsolete|replaced|ersetzt|veraltet', content, re.IGNORECASE))
    swsm['deprecation']['migration'] = bool(re.search(r'migration|transition|upgrade|umstellung', content, re.IGNORECASE))

    dep_count = sum(swsm['deprecation'].values())
    swsm['deprecation']['_score'] = dep_count / 3 * 100

    # ==========================================================================
    # WORKED EXAMPLES
    # ==========================================================================
    swsm['examples']['profile_extraction'] = bool(re.search(
        r'(extract|extrahier).*?(profile|profil)|Fehr.*?profile|profile.*?Fehr|Korpus.*?Analyse',
        content, re.IGNORECASE
    ))
    swsm['examples']['text_generation'] = bool(re.search(
        r'generat.*?(text|abstract)|text.*?generat|Abstract.*?generat',
        content, re.IGNORECASE
    ))
    swsm['examples']['interpolation'] = bool(re.search(
        r'interpolat|distance.*?profile|profile.*?distance|0\.\d.*?×.*?θ|blend|mix',
        content, re.IGNORECASE
    ))

    ex_count = sum(swsm['examples'].values())
    swsm['examples']['_score'] = ex_count / 3 * 100

    # ==========================================================================
    # GESAMTSCORE
    # ==========================================================================
    swsm['score'] = (
        swsm['components']['_score'] * 0.30 +
        swsm['axioms']['_score'] * 0.25 +
        swsm['theta']['_score'] * 0.20 +
        swsm['deprecation']['_score'] * 0.10 +
        swsm['examples']['_score'] * 0.15
    )

    return swsm


def print_swsm_report(swsm: dict):
    """Druckt SWSM-spezifischen Compliance-Report."""

    print(f"\n{'─'*70}")
    print("🔬 SWSM-SPEZIFISCHE COMPLIANCE")
    print(f"{'─'*70}")

    # Komponenten
    print(f"\n📦 KOMPONENTEN (E1-E9): {swsm['components']['_count']} ({swsm['components']['_score']:.0f}%)")
    for comp in ['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9']:
        status = "✅" if swsm['components'][comp] else "❌"
        print(f"   {status} {comp}")

    # Axiome
    print(f"\n📐 AXIOME (SWSM-1 bis SWSM-20): {swsm['axioms']['_count']} ({swsm['axioms']['_score']:.0f}%)")
    found = [k for k, v in swsm['axioms'].items() if v and not k.startswith('_')]
    missing = [k for k, v in swsm['axioms'].items() if not v and not k.startswith('_')]
    if found:
        print(f"   ✅ Gefunden: {', '.join(found[:10])}{'...' if len(found) > 10 else ''}")
    if missing and len(missing) <= 10:
        print(f"   ❌ Fehlt: {', '.join(missing)}")

    # θ Parameter
    print(f"\n🎛️  θ PARAMETER: {swsm['theta']['_count']} ({swsm['theta']['_score']:.0f}%)")
    for theta in ['theta_move', 'theta_cohesion', 'theta_rst', 'theta_lexicogrammar', 'theta_info', 'theta_vocab']:
        status = "✅" if swsm['theta'][theta] else "❌"
        print(f"   {status} {theta}")

    # Deprecation
    print(f"\n⚠️  8D DEPRECATION: {swsm['deprecation']['_score']:.0f}%")
    for key in ['8d_mentioned', 'deprecated', 'migration']:
        status = "✅" if swsm['deprecation'][key] else "❌"
        print(f"   {status} {key.replace('_', ' ').title()}")

    # Examples
    print(f"\n📝 WORKED EXAMPLES: {swsm['examples']['_score']:.0f}%")
    for key in ['profile_extraction', 'text_generation', 'interpolation']:
        status = "✅" if swsm['examples'][key] else "❌"
        print(f"   {status} {key.replace('_', ' ').title()}")

    # Gesamtscore
    print(f"\n{'─'*70}")
    print(f"   SWSM COMPLIANCE SCORE: {swsm['score']:.1f}%")
    print(f"{'─'*70}")


def check_compliance(content: str, appendix_name: str) -> dict:
    """Prüft Template-Compliance mit kategorie-spezifischen Anforderungen."""

    # Kategorie erkennen
    category, cat_config = detect_category(content, appendix_name)
    weights = cat_config['weights']

    # Sprache erkennen
    language = detect_language(content)

    results = {
        'appendix': appendix_name,
        'category': category,
        'category_description': cat_config['description'],
        'weights': weights,
        'required_fields': cat_config['required'],
        'optional_fields': cat_config['optional'],
        'language': language,
        'front_matter': {},
        'core_content': {},
        'application': {},
        'back_matter': {},
        'critical_links': {},
        'scores': {},
        'total': 0
    }

    # ==========================================================================
    # FRONT MATTER
    # ==========================================================================
    fm = results['front_matter']

    fm['header_block'] = bool(re.search(r'\\begin\{tcolorbox\}.*?(Appendix:|Category:|CORE Question:)', content, re.DOTALL))
    fm['cross_ref_map'] = bool(re.search(r'Cross-Reference|CROSS-REFERENCE|Dependencies|Dependents', content, re.IGNORECASE))
    fm['chapter_linkage'] = bool(re.search(r'Chapter Linkage|Primary Chapter|Chapter \d+', content))
    fm['abstract'] = bool(re.search(r'\\begin\{abstract\}|Abstract\}|\\textbf\{Abstract', content))
    fm['quick_reference'] = bool(re.search(r'Quick Reference|Jump to:|Key (Equations|Formulas|Results)', content, re.IGNORECASE))
    fm['scope_box'] = bool(re.search(r'Appendix Scope:|Ziel.*?In-Scope.*?Out-of-Scope|Constraints.*?Anwendungsgrenzen|Lieferobjekte', content, re.IGNORECASE | re.DOTALL))

    fm_score = sum(fm.values()) / len(fm) * 100
    results['scores']['front_matter'] = fm_score

    # ==========================================================================
    # CORE CONTENT
    # ==========================================================================
    cc = results['core_content']

    cc['fundamental_question'] = bool(re.search(r'Fundamental Question|CORE Question|Core Contribution', content, re.IGNORECASE))
    cc['theory'] = bool(re.search(r'\\(sub)?section\{.*?(Theory|Theoretical|Framework|Foundation)', content))
    cc['axioms'] = bool(re.search(r'\\begin\{axiom\}|Axiom.*?:|axiom\}|\\label\{ax:', content, re.IGNORECASE))
    cc['results'] = bool(re.search(r'\\(sub)?section\{.*?(Results|Findings|Validation)', content))
    cc['integration'] = bool(re.search(r'Integration|Connection to|Cross-reference|Related Appendix', content, re.IGNORECASE))

    # Kategorie-spezifische Score-Berechnung: Optional-Felder nicht negativ werten
    cc_items = []
    for key, val in cc.items():
        if key in cat_config['optional']:
            # Optional: Nur positiv werten wenn vorhanden
            if val:
                cc_items.append(1)
            # Sonst ignorieren (nicht 0 hinzufügen)
        else:
            cc_items.append(1 if val else 0)

    cc_score = (sum(cc_items) / len(cc_items) * 100) if cc_items else 0
    results['scores']['core_content'] = cc_score

    # ==========================================================================
    # APPLICATION
    # ==========================================================================
    app = results['application']

    app['worked_example'] = bool(re.search(r'Worked Example|Example:|Step \d+:|Case Study|Tutorial', content, re.IGNORECASE))
    app['implications'] = bool(re.search(r'Implications|Practical|Practice|Application', content, re.IGNORECASE))

    # Kategorie-spezifische Score-Berechnung
    app_items = []
    for key, val in app.items():
        if key in cat_config['optional']:
            if val:
                app_items.append(1)
        else:
            app_items.append(1 if val else 0)

    app_score = (sum(app_items) / len(app_items) * 100) if app_items else 100
    results['scores']['application'] = app_score

    # ==========================================================================
    # BACK MATTER
    # ==========================================================================
    bm = results['back_matter']

    bm['summary'] = bool(re.search(r'\\section\{Summary|Summary\}|\\textbf\{.*?Summary', content))
    bm['glossary_section'] = bool(re.search(r'\\section\{Glossary|Glossary of Symbols', content))
    bm['foundations'] = bool(re.search(r'Critical Foundations|Objection|Response:', content, re.IGNORECASE))
    bm['open_issues'] = bool(re.search(r'Open Issues|Future Work|Research Agenda|Limitations', content, re.IGNORECASE))
    bm['references_section'] = bool(re.search(r'\\section\{References|\\begin\{thebibliography\}|References for Appendix', content))

    # Kategorie-spezifische Score-Berechnung
    bm_items = []
    for key, val in bm.items():
        if key in cat_config['optional']:
            if val:
                bm_items.append(1)
        else:
            bm_items.append(1 if val else 0)

    bm_score = (sum(bm_items) / len(bm_items) * 100) if bm_items else 0
    results['scores']['back_matter'] = bm_score

    # ==========================================================================
    # CRITICAL LINKS
    # ==========================================================================
    cl = results['critical_links']

    cl['glossary_g_link'] = bool(re.search(r'Appendix G|Central.*?Glossary|Glossary and Notation|Master Glossary', content, re.IGNORECASE))
    cl['master_bib_link'] = bool(re.search(r'master.*?references\.bib|Master Bibliography|bcm2.*?references|\\nocite\{bcm_master\}|bcm_master\.bib', content, re.IGNORECASE))

    # ==========================================================================
    # GESAMTSCORE BERECHNUNG (mit kategorie-spezifischen Gewichten)
    # ==========================================================================

    weighted_score = (
        fm_score * weights['front_matter'] +
        cc_score * weights['core_content'] +
        app_score * weights['application'] +
        bm_score * weights['back_matter']
    )

    # PENALTY für fehlende kritische Links (nur wenn REQUIRED für Kategorie)
    penalty = 0
    if 'glossary_g_link' in cat_config['required'] and not cl['glossary_g_link']:
        penalty += 10
    elif not cl['glossary_g_link']:
        penalty += 5  # Reduzierte Penalty für nicht-required

    if 'master_bib_link' in cat_config['required'] and not cl['master_bib_link']:
        penalty += 10
    elif not cl['master_bib_link']:
        penalty += 5  # Reduzierte Penalty für nicht-required

    # PENALTY für Sprachinkonsistenz
    if not language['consistent']:
        penalty += 15  # Gemischte Sprache ist ein größeres Problem
    elif language['detected'] == 'en' and not language['declared']:
        penalty += 5   # Englisch ohne Deklaration (Default ist Deutsch)

    # Bonus für erfüllte Required-Felder (außer Links)
    all_fields = {**fm, **cc, **app, **bm}
    required_met = sum(1 for r in cat_config['required'] if r in all_fields and all_fields.get(r, False))
    required_total = len([r for r in cat_config['required'] if r in all_fields])

    results['required_compliance'] = f"{required_met}/{required_total}"
    results['penalty'] = penalty
    results['weighted_score'] = weighted_score
    results['total'] = max(0, weighted_score - penalty)

    # ==========================================================================
    # SWSM-SPEZIFISCHE CHECKS (nur für METHOD-SWSM Kategorie)
    # ==========================================================================
    if category == 'METHOD-SWSM' or (appendix_name and 'SW' in os.path.basename(appendix_name).upper()[:3]):
        swsm_results = check_swsm_specific(content)
        results['swsm'] = swsm_results

        # SWSM Score beeinflusst Gesamtscore
        # 50% Standard-Compliance + 50% SWSM-spezifisch
        results['total'] = (results['total'] * 0.5) + (swsm_results['score'] * 0.5)

    return results


def print_report(results: dict):
    """Druckt einen formatierten Report mit Kategorie-Info."""

    weights = results['weights']

    print(f"\n{'='*70}")
    print(f"TEMPLATE COMPLIANCE REPORT: {results['appendix']}")
    print(f"{'='*70}")

    # Kategorie-Info
    print(f"\n🏷️  KATEGORIE: {results['category']}")
    print(f"   {results['category_description']}")
    print(f"   Gewichte: FM={weights['front_matter']:.0%} CC={weights['core_content']:.0%} APP={weights['application']:.0%} BM={weights['back_matter']:.0%}")
    if results['required_fields']:
        print(f"   Required: {', '.join(results['required_fields'])}")
    if results['optional_fields']:
        print(f"   Optional: {', '.join(results['optional_fields'])}")

    # Front Matter
    print(f"\n📋 FRONT MATTER ({weights['front_matter']:.0%}): {results['scores']['front_matter']:.0f}%")
    for key, val in results['front_matter'].items():
        status = "✅" if val else "❌"
        opt_mark = " (optional)" if key in results['optional_fields'] else ""
        req_mark = " ★" if key in results['required_fields'] else ""
        print(f"   {status} {key.replace('_', ' ').title()}{req_mark}{opt_mark}")

    # Core Content
    print(f"\n📚 CORE CONTENT ({weights['core_content']:.0%}): {results['scores']['core_content']:.0f}%")
    for key, val in results['core_content'].items():
        status = "✅" if val else "❌"
        opt_mark = " (optional)" if key in results['optional_fields'] else ""
        req_mark = " ★" if key in results['required_fields'] else ""
        print(f"   {status} {key.replace('_', ' ').title()}{req_mark}{opt_mark}")

    # Application
    print(f"\n🔧 APPLICATION ({weights['application']:.0%}): {results['scores']['application']:.0f}%")
    for key, val in results['application'].items():
        status = "✅" if val else "❌"
        opt_mark = " (optional)" if key in results['optional_fields'] else ""
        req_mark = " ★" if key in results['required_fields'] else ""
        print(f"   {status} {key.replace('_', ' ').title()}{req_mark}{opt_mark}")

    # Back Matter
    print(f"\n📖 BACK MATTER ({weights['back_matter']:.0%}): {results['scores']['back_matter']:.0f}%")
    for key, val in results['back_matter'].items():
        status = "✅" if val else "❌"
        opt_mark = " (optional)" if key in results['optional_fields'] else ""
        req_mark = " ★" if key in results['required_fields'] else ""
        print(f"   {status} {key.replace('_', ' ').title()}{req_mark}{opt_mark}")

    # Critical Links
    print(f"\n⚠️  CRITICAL LINKS:")
    for key, val in results['critical_links'].items():
        if val:
            status = "✅"
        elif key in results['required_fields']:
            status = "❌ FEHLT (-10%)"
        else:
            status = "❌ fehlt (-5%)"
        req_mark = " ★" if key in results['required_fields'] else ""
        print(f"   {status} {key.replace('_', ' ').title()}{req_mark}")

    # Language Check
    lang = results['language']
    lang_names = {'de': 'Deutsch', 'en': 'English', 'mixed': 'GEMISCHT', 'unknown': 'Unbekannt'}
    lang_detected = lang_names.get(lang['detected'], lang['detected'])
    lang_declared = lang_names.get(lang['declared'], 'nicht deklariert') if lang['declared'] else 'nicht deklariert'

    print(f"\n🌐 SPRACHE:")
    if lang['consistent']:
        print(f"   ✅ {lang_detected} (Deklariert: {lang_declared})")
    else:
        print(f"   ❌ {lang_detected} (Deklariert: {lang_declared}) -15%")
    if lang['issues']:
        for issue in lang['issues']:
            print(f"   ⚠️  {issue}")
    print(f"   📊 Indikatoren: {lang['german_count']} DE / {lang['english_count']} EN")

    # Gesamtscore
    print(f"\n{'─'*70}")
    print(f"   Required Fields:  {results['required_compliance']}")
    print(f"   Weighted Score:   {results['weighted_score']:.1f}%")
    if results['penalty'] > 0:
        print(f"   Penalty:         -{results['penalty']}% (Links/Sprache)")
    print(f"   ═══════════════════════════════════════")
    print(f"   TOTAL SCORE:      {results['total']:.1f}%")
    print(f"{'─'*70}")

    # SWSM-spezifischer Report (falls vorhanden)
    if 'swsm' in results:
        print_swsm_report(results['swsm'])

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


def print_category_overview():
    """Druckt Übersicht aller Kategorien."""
    print(f"\n{'='*70}")
    print("EBF APPENDIX KATEGORIEN")
    print(f"{'='*70}\n")

    for cat_name, config in CATEGORY_CONFIG.items():
        w = config['weights']
        print(f"📁 {cat_name}: {config['description']}")
        print(f"   Gewichte: FM={w['front_matter']:.0%} CC={w['core_content']:.0%} APP={w['application']:.0%} BM={w['back_matter']:.0%}")
        print(f"   Required: {', '.join(config['required']) or 'Standard'}")
        print(f"   Optional: {', '.join(config['optional']) or '-'}")
        print(f"   Appendices: {', '.join(config['appendices'])}")
        print()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == '--categories':
            print_category_overview()
        else:
            with open(sys.argv[1], 'r') as f:
                content = f.read()
            results = check_compliance(content, sys.argv[1])
            print_report(results)
    else:
        print("Usage: python check_template_compliance.py <appendix.tex>")
        print("       python check_template_compliance.py --categories")
