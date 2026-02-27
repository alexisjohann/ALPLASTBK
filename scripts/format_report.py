#!/usr/bin/env python3
"""
=============================================================================
FEHRADVICE REPORT FORMATTER
=============================================================================
Automatisierte Konvertierung von Markdown-Reports in FehrAdvice-formatierte
PDF- und HTML-Dokumente.

SSOT: appendices/REF-STYLE_SG_corporate_style_guide.tex
Templates: templates/fehradvice-report.latex, templates/fehradvice-report.css

Verwendung:
    python scripts/format_report.py input.md --output output.pdf
    python scripts/format_report.py input.md --format html
    python scripts/format_report.py input.md --format pptx

Version: 1.1
Date: January 2026
=============================================================================
"""

import argparse
import os
import re
import subprocess
import sys
import tempfile
import yaml
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any


# =============================================================================
# KONFIGURATION
# =============================================================================

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
TEMPLATES_DIR = PROJECT_ROOT / "templates"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
ASSETS_DIR = PROJECT_ROOT / "assets"

# Workflow-Verzeichnis (SSOT für format-report)
WORKFLOW_DIR = PROJECT_ROOT / "workflows" / "format-report"
WORKFLOW_OUTPUTS_DIR = WORKFLOW_DIR / "outputs"

# Template-Dateien
LATEX_TEMPLATE = TEMPLATES_DIR / "fehradvice-report.latex"
CSS_TEMPLATE = TEMPLATES_DIR / "fehradvice-report.css"
HTML_TEMPLATE = TEMPLATES_DIR / "fehradvice-report.html"
COVER_TEMPLATE = TEMPLATES_DIR / "fehradvice-cover.latex"
BACK_TEMPLATE = TEMPLATES_DIR / "fehradvice-back.latex"
TOC_TEMPLATE = TEMPLATES_DIR / "fehradvice-toc.latex"
PPTX_TEMPLATE = TEMPLATES_DIR / "pptx" / "FehrAdvice-Master.pptx"
FA_STYLE = TEMPLATES_DIR / "pptx" / "fa-style.yaml"

# Learnings-Datenbank
LEARNINGS_DB = PROJECT_ROOT / "data" / "report-formatter-learnings.yaml"

# Default-Werte
DEFAULT_DOCTYPE = "Strategisches Dossier"
DEFAULT_AUTHOR = "FehrAdvice & Partners AG"

# Erforderliche Workflow-Struktur
REQUIRED_WORKFLOW_STRUCTURE = {
    'directories': [
        WORKFLOW_DIR,
        WORKFLOW_OUTPUTS_DIR,
        WORKFLOW_DIR / "docs",
    ],
    'files': [
        WORKFLOW_DIR / "README.md",
        WORKFLOW_DIR / "docs" / "workflow-guide.md",
    ],
    'templates': [
        COVER_TEMPLATE,
        BACK_TEMPLATE,
        TOC_TEMPLATE,
        LATEX_TEMPLATE,
        CSS_TEMPLATE,
        HTML_TEMPLATE,
    ]
}


# =============================================================================
# LEARNINGS INTEGRATION
# =============================================================================

def load_learnings() -> Dict[str, Any]:
    """Lädt die Learnings-Datenbank."""
    if LEARNINGS_DB.exists():
        with open(LEARNINGS_DB, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    return {}


def get_next_learning_id() -> str:
    """Generiert die nächste Learning-ID."""
    learnings = load_learnings()
    existing_ids = [l['id'] for l in learnings.get('learnings', [])]

    # Finde höchste Nummer
    max_num = 0
    for lid in existing_ids:
        match = re.match(r'RPT-L-(\d+)', lid)
        if match:
            max_num = max(max_num, int(match.group(1)))

    return f"RPT-L-{max_num + 1:03d}"


def add_learning_interactive() -> bool:
    """Fügt ein neues Learning interaktiv hinzu."""
    print("""
┌─────────────────────────────────────────────────────────────────────────┐
│  📝 NEUES LEARNING HINZUFÜGEN                                           │
└─────────────────────────────────────────────────────────────────────────┘
""")

    learnings = load_learnings()
    new_id = get_next_learning_id()

    print(f"Learning ID: {new_id}")
    print()

    # Kategorie wählen
    categories = learnings.get('categories', {})
    print("Kategorien:")
    cat_list = list(categories.keys())
    for i, (key, desc) in enumerate(categories.items(), 1):
        print(f"  {i}. {key}: {desc}")

    try:
        cat_choice = input("\nKategorie (Nummer oder Name): ").strip()
        if cat_choice.isdigit():
            category = cat_list[int(cat_choice) - 1]
        else:
            category = cat_choice.upper()
    except (ValueError, IndexError):
        category = "WORKFLOW"

    # Titel
    title = input("Titel: ").strip()
    if not title:
        print("❌ Titel ist erforderlich.")
        return False

    # Problem
    print("Problem (mehrzeilig, leere Zeile zum Beenden):")
    problem_lines = []
    while True:
        line = input()
        if not line:
            break
        problem_lines.append(line)
    problem = '\n'.join(problem_lines)

    # Lösung
    print("Lösung (mehrzeilig, leere Zeile zum Beenden):")
    solution_lines = []
    while True:
        line = input()
        if not line:
            break
        solution_lines.append(line)
    solution = '\n'.join(solution_lines)

    # Lesson Learned
    print("Lesson Learned (mehrzeilig, leere Zeile zum Beenden):")
    lesson_lines = []
    while True:
        line = input()
        if not line:
            break
        lesson_lines.append(line)
    lesson_learned = '\n'.join(lesson_lines)

    # Severity
    severity = input("Severity (HIGH/MEDIUM/LOW/INFO) [INFO]: ").strip().upper() or "INFO"

    # Neues Learning erstellen
    new_learning = {
        'id': new_id,
        'category': category,
        'title': title,
        'problem': problem + '\n' if problem else '',
        'solution': solution + '\n' if solution else '',
        'severity': severity,
        'first_encountered': datetime.now().strftime('%Y-%m-%d'),
        'lesson_learned': lesson_learned + '\n' if lesson_learned else '',
        'resolution': '',
        'recurrence_probability': '0%'
    }

    # Zur Datenbank hinzufügen
    if 'learnings' not in learnings:
        learnings['learnings'] = []
    learnings['learnings'].append(new_learning)

    # Metadata aktualisieren
    if 'metadata' in learnings:
        learnings['metadata']['last_updated'] = datetime.now().strftime('%Y-%m-%d')
        learnings['metadata']['total_learnings'] = len(learnings['learnings'])

    # Speichern
    with open(LEARNINGS_DB, 'w', encoding='utf-8') as f:
        yaml.dump(learnings, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

    print(f"\n✅ Learning {new_id} hinzugefügt!")
    print(f"   Datei: {LEARNINGS_DB.relative_to(PROJECT_ROOT)}")
    print(f"\n💡 Vergiss nicht: git add {LEARNINGS_DB.relative_to(PROJECT_ROOT)}")

    return True


def check_learning_reminder() -> None:
    """
    Prüft ob kürzlich Änderungen an Script/Templates gemacht wurden
    und erinnert an Learnings.
    """
    try:
        # Git diff prüfen (unstaged + staged)
        result = subprocess.run(
            ['git', 'diff', '--name-only', 'HEAD'],
            capture_output=True, text=True, cwd=str(PROJECT_ROOT)
        )

        changed_files = result.stdout.strip().split('\n') if result.stdout.strip() else []

        # Relevante Dateien prüfen
        relevant_patterns = [
            'scripts/format_report.py',
            'templates/fehradvice-',
            'templates/pptx/',
        ]

        relevant_changes = [f for f in changed_files
                          if any(p in f for p in relevant_patterns)]

        if relevant_changes:
            print("""
┌─────────────────────────────────────────────────────────────────────────┐
│  💡 LEARNING REMINDER                                                   │
├─────────────────────────────────────────────────────────────────────────┤
│  Du hast Änderungen an Report-Formatter Dateien gemacht:                │""")
            for f in relevant_changes[:5]:
                print(f"│    • {f:<63} │")
            print("""│                                                                         │
│  Vergiss nicht, relevante Learnings zu dokumentieren!                   │
│                                                                         │
│  → python scripts/format_report.py --add-learning                       │
└─────────────────────────────────────────────────────────────────────────┘
""")
    except Exception:
        pass  # Silently fail if git is not available


def check_dependencies() -> list:
    """Prüft ob alle Abhängigkeiten installiert sind."""
    issues = []

    # Pandoc prüfen
    try:
        subprocess.run(['pandoc', '--version'], capture_output=True, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        issues.append({
            'type': 'DEPS',
            'message': 'Pandoc nicht installiert',
            'fix': 'apt-get install pandoc',
            'learning_id': 'RPT-L-008'
        })

    # pdflatex prüfen
    try:
        subprocess.run(['pdflatex', '--version'], capture_output=True, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        issues.append({
            'type': 'DEPS',
            'message': 'pdflatex nicht installiert',
            'fix': 'apt-get install texlive-latex-extra',
            'learning_id': 'RPT-L-009'
        })

    return issues


# =============================================================================
# WORKFLOW-STRUKTUR VALIDIERUNG
# =============================================================================

def verify_workflow_structure(auto_fix: bool = False) -> dict:
    """
    Überprüft die Workflow-Verzeichnisstruktur und meldet Probleme.

    Args:
        auto_fix: Wenn True, werden fehlende Verzeichnisse automatisch erstellt

    Returns:
        Dict mit 'valid' (bool), 'issues' (list), 'fixed' (list)
    """
    result = {
        'valid': True,
        'issues': [],
        'fixed': [],
        'warnings': []
    }

    # Verzeichnisse prüfen
    for dir_path in REQUIRED_WORKFLOW_STRUCTURE['directories']:
        if not dir_path.exists():
            if auto_fix:
                dir_path.mkdir(parents=True, exist_ok=True)
                result['fixed'].append(f"Verzeichnis erstellt: {dir_path.relative_to(PROJECT_ROOT)}")
            else:
                result['valid'] = False
                result['issues'].append(f"Verzeichnis fehlt: {dir_path.relative_to(PROJECT_ROOT)}")

    # Dateien prüfen (nur Warnung, kein Fehler)
    for file_path in REQUIRED_WORKFLOW_STRUCTURE['files']:
        if not file_path.exists():
            result['warnings'].append(f"Datei fehlt: {file_path.relative_to(PROJECT_ROOT)}")

    # Templates prüfen (kritisch)
    for template_path in REQUIRED_WORKFLOW_STRUCTURE['templates']:
        if not template_path.exists():
            result['valid'] = False
            result['issues'].append(f"Template fehlt: {template_path.relative_to(PROJECT_ROOT)}")

    # .gitignore in outputs prüfen
    gitignore_path = WORKFLOW_OUTPUTS_DIR / ".gitignore"
    if WORKFLOW_OUTPUTS_DIR.exists() and not gitignore_path.exists():
        if auto_fix:
            gitignore_content = """# Generated PDF outputs - not tracked in git
*.pdf

# Temporary files
_cover_*.pdf
_content_*.pdf
_back_*.pdf
_toc_*.pdf
"""
            gitignore_path.write_text(gitignore_content)
            result['fixed'].append(f".gitignore erstellt: {gitignore_path.relative_to(PROJECT_ROOT)}")
        else:
            result['warnings'].append(f".gitignore fehlt in outputs/ - generierte PDFs werden nicht ignoriert")

    return result


def print_workflow_status():
    """Zeigt den Status der Workflow-Struktur an."""
    print("\n" + "=" * 60)
    print("📁 WORKFLOW-STRUKTUR ÜBERPRÜFUNG")
    print("=" * 60)

    result = verify_workflow_structure(auto_fix=False)

    # Verzeichnisse
    print("\n📂 Verzeichnisse:")
    for dir_path in REQUIRED_WORKFLOW_STRUCTURE['directories']:
        status = "✅" if dir_path.exists() else "❌"
        print(f"   {status} {dir_path.relative_to(PROJECT_ROOT)}")

    # Templates
    print("\n📄 Templates:")
    for template_path in REQUIRED_WORKFLOW_STRUCTURE['templates']:
        status = "✅" if template_path.exists() else "❌"
        print(f"   {status} {template_path.relative_to(PROJECT_ROOT)}")

    # Dateien
    print("\n📝 Dokumentation:")
    for file_path in REQUIRED_WORKFLOW_STRUCTURE['files']:
        status = "✅" if file_path.exists() else "⚠️"
        print(f"   {status} {file_path.relative_to(PROJECT_ROOT)}")

    # Zusammenfassung
    print("\n" + "-" * 60)
    if result['valid']:
        print("✅ Workflow-Struktur ist vollständig und korrekt.")
    else:
        print("❌ Probleme gefunden:")
        for issue in result['issues']:
            print(f"   • {issue}")

    if result['warnings']:
        print("\n⚠️ Warnungen:")
        for warning in result['warnings']:
            print(f"   • {warning}")

    print("\n💡 Tipp: Verwende --verify --fix um Probleme automatisch zu beheben.")
    print("=" * 60 + "\n")

    return result['valid']


def get_default_output_path(input_file: Path, output_format: str) -> Path:
    """
    Bestimmt den Standard-Output-Pfad im Workflow-Verzeichnis.

    Args:
        input_file: Eingabedatei
        output_format: Ausgabeformat (pdf, html, etc.)

    Returns:
        Pfad im Workflow-Outputs-Verzeichnis
    """
    ext_map = {'pdf': '.pdf', 'html': '.html', 'pptx': '.pptx', 'docx': '.docx'}
    ext = ext_map.get(output_format, '.pdf')

    # Sicherstellen dass outputs-Verzeichnis existiert
    WORKFLOW_OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

    return WORKFLOW_OUTPUTS_DIR / f"{input_file.stem}{ext}"


def validate_output_path(output_path: Path) -> tuple:
    """
    Validiert ob der Output-Pfad im empfohlenen Verzeichnis liegt.

    Args:
        output_path: Geplanter Ausgabepfad

    Returns:
        Tuple (is_recommended: bool, message: str)
    """
    # Normalisiere Pfade für Vergleich
    try:
        output_resolved = output_path.resolve()
        workflow_resolved = WORKFLOW_OUTPUTS_DIR.resolve()

        # Prüfen ob im Workflow-Outputs-Verzeichnis
        if str(output_resolved).startswith(str(workflow_resolved)):
            return (True, None)

        # Prüfen ob im allgemeinen outputs-Verzeichnis
        outputs_resolved = OUTPUTS_DIR.resolve()
        if str(output_resolved).startswith(str(outputs_resolved)):
            return (True, f"💡 Empfohlen: {WORKFLOW_OUTPUTS_DIR.relative_to(PROJECT_ROOT)}/")

        # Außerhalb der Standard-Verzeichnisse
        return (False, f"⚠️ Output außerhalb des Workflow-Verzeichnisses: {output_path}\n"
                       f"   Empfohlen: {WORKFLOW_OUTPUTS_DIR.relative_to(PROJECT_ROOT)}/")
    except Exception:
        return (True, None)  # Bei Fehlern durchlassen


def analyze_content_for_issues(content: str) -> list:
    """Analysiert den Inhalt auf bekannte Probleme."""
    issues = []

    # Emojis erkennen
    emoji_pattern = re.compile(r'[\U0001F300-\U0001F9FF]')
    if emoji_pattern.search(content):
        issues.append({
            'type': 'UNICODE',
            'message': 'Dokument enthält Emojis',
            'recommendation': 'HTML-Output empfohlen für volle Emoji-Unterstützung',
            'learning_id': 'RPT-L-004'
        })

    # Progress-Bars erkennen
    if '█' in content or '████' in content:
        issues.append({
            'type': 'TABLES',
            'message': 'Dokument enthält Progress-Bars',
            'recommendation': 'HTML-Output empfohlen für korrekte Darstellung',
            'learning_id': 'RPT-L-003'
        })

    # Unicode-Sonderzeichen erkennen
    special_chars = ['−', '–', '—', '≤', '≥', '≠', '×', '÷']
    found_chars = [c for c in special_chars if c in content]
    if found_chars:
        issues.append({
            'type': 'UNICODE',
            'message': f'Dokument enthält Unicode-Sonderzeichen: {found_chars}',
            'note': 'Werden automatisch für LaTeX konvertiert',
            'learning_id': 'RPT-L-005'
        })

    # Komplexe Tabellen erkennen (mehr als 5 Spalten oder viele Zeilen)
    table_lines = [l for l in content.split('\n') if l.startswith('|')]
    if table_lines:
        max_cols = max(l.count('|') for l in table_lines)
        if max_cols > 6:
            issues.append({
                'type': 'TABLES',
                'message': f'Dokument enthält komplexe Tabellen ({max_cols-1} Spalten)',
                'recommendation': 'HTML-Output kann komplexe Tabellen besser darstellen',
                'learning_id': 'RPT-L-003'
            })

    return issues


def get_format_recommendation(content: str, requested_format: str) -> Optional[str]:
    """Gibt eine Format-Empfehlung basierend auf dem Inhalt."""
    issues = analyze_content_for_issues(content)

    if requested_format == 'pdf' and issues:
        problematic_issues = [i for i in issues if i['type'] in ['UNICODE', 'TABLES']
                            and 'recommendation' in i]
        if problematic_issues:
            return f"""
┌─────────────────────────────────────────────────────────────────────────┐
│  💡 FORMAT-EMPFEHLUNG                                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Das Dokument enthält Elemente, die in HTML besser dargestellt werden:  │
│                                                                         │
{chr(10).join(f"│  • {i['message'][:60]:<60} │" for i in problematic_issues)}
│                                                                         │
│  Empfehlung: Verwende -f html für optimale Darstellung                  │
│              oder fahre mit -f pdf fort (Elemente werden konvertiert)   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
"""
    return None


def diagnose_error(error_message: str) -> Optional[Dict[str, str]]:
    """Diagnostiziert einen Fehler anhand der Learnings-Datenbank."""
    learnings = load_learnings()
    quick_ref = learnings.get('quick_reference', [])

    for entry in quick_ref:
        if entry['error'].lower() in error_message.lower():
            learning_id = entry['learning_id']
            # Finde das vollständige Learning
            for learning in learnings.get('learnings', []):
                if learning['id'] == learning_id:
                    return {
                        'id': learning_id,
                        'title': learning['title'],
                        'fix': entry['fix'],
                        'full_solution': learning.get('solution', ''),
                        'prevention': learning.get('prevention', '')
                    }
            return {
                'id': learning_id,
                'fix': entry['fix']
            }

    return None


def print_diagnostic(error_message: str):
    """Gibt eine hilfreiche Diagnose für einen Fehler aus."""
    diagnosis = diagnose_error(error_message)

    if diagnosis:
        print(f"""
┌─────────────────────────────────────────────────────────────────────────┐
│  🔍 BEKANNTES PROBLEM ERKANNT: {diagnosis.get('id', 'N/A'):<38} │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Problem: {diagnosis.get('title', 'Unbekannt')[:58]:<58} │
│                                                                         │
│  Lösung:  {diagnosis.get('fix', 'Siehe Learnings-DB')[:58]:<58} │
│                                                                         │
│  Details: data/report-formatter-learnings.yaml                          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
""")
    else:
        print(f"""
┌─────────────────────────────────────────────────────────────────────────┐
│  ⚠️  UNBEKANNTER FEHLER                                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Dieser Fehler ist noch nicht in der Learnings-Datenbank.               │
│                                                                         │
│  Bitte dokumentiere das Problem in:                                     │
│  data/report-formatter-learnings.yaml                                   │
│                                                                         │
│  Workaround: Versuche HTML-Output (-f html)                             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
""")


# =============================================================================
# HILFSFUNKTIONEN
# =============================================================================

def load_fa_style() -> Dict[str, Any]:
    """Lädt die FehrAdvice Style-Konfiguration."""
    if FA_STYLE.exists():
        with open(FA_STYLE, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    return {}


def extract_yaml_frontmatter(content: str) -> tuple[Dict[str, Any], str]:
    """Extrahiert YAML-Frontmatter aus Markdown."""
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            try:
                frontmatter = yaml.safe_load(parts[1])
                body = parts[2].strip()
                return frontmatter or {}, body
            except yaml.YAMLError:
                pass
    return {}, content


def apply_swiss_orthography(text: str) -> str:
    """Wendet Schweizer Orthographie-Regeln an."""
    # ß → ss
    text = text.replace('ß', 'ss')

    # Deutsche Anführungszeichen → Guillemets
    text = re.sub(r'„([^"]+)"', r'«\1»', text)
    text = re.sub(r'"([^"]+)"', r'«\1»', text)

    # Einfache Anführungszeichen → ‹ ›
    text = re.sub(r"'([^']+)'", r'‹\1›', text)

    return text


def format_numbers_swiss(text: str) -> str:
    """Formatiert Zahlen im Schweizer Format (1'000.00)."""
    # Ersetze Komma-Tausendertrennzeichen durch Apostroph
    text = re.sub(r'(\d),(\d{3})', r"\1'\2", text)
    return text


def replace_emojis_for_latex(text: str) -> str:
    """Ersetzt Emojis durch LaTeX-kompatible Alternativen."""
    emoji_replacements = {
        '✅': '[OK]',
        '❌': '[X]',
        '⚠️': '[!]',
        '✓': '[v]',
        '✗': '[x]',
        '→': '->',
        '←': '<-',
        '↑': '^',
        '↓': 'v',
        '🥇': '[1.]',
        '🥈': '[2.]',
        '🥉': '[3.]',
        '💪': '*',
        '😴': '-',
        '📊': '',
        '📋': '',
        '📁': '',
        '🔬': '',
        '📚': '',
        '⚡': '',
        '🎯': '',
        '1️⃣': '1.',
        '2️⃣': '2.',
        '3️⃣': '3.',
        '4️⃣': '4.',
        '5️⃣': '5.',
        '█': '#',  # Progress bar character
        '−': '-',  # Unicode minus
        '–': '-',  # En dash
        '—': '--', # Em dash
        '…': '...',
        '«': '"',
        '»': '"',
        '‹': "'",
        '›': "'",
        ''': "'",
        ''': "'",
        '"': '"',
        '"': '"',
        '×': 'x',
        '÷': '/',
        '≈': '~',
        '≤': '<=',
        '≥': '>=',
        '≠': '!=',
        '∈': 'in',
        '∉': 'not in',
        '∑': 'Sum',
        '∏': 'Prod',
        '√': 'sqrt',
        '∞': 'inf',
        '°': ' deg',
        '±': '+/-',
        '·': '*',
        # Box-drawing characters (for ASCII art diagrams)
        '┌': '+',
        '┐': '+',
        '└': '+',
        '┘': '+',
        '├': '+',
        '┤': '+',
        '┬': '+',
        '┴': '+',
        '┼': '+',
        '│': '|',
        '─': '-',
        '═': '=',
        '║': '|',
        '╔': '+',
        '╗': '+',
        '╚': '+',
        '╝': '+',
        # Traffic light emojis
        '🔴': '[!]',
        '🟡': '[?]',
        '🟢': '[v]',
        '🔵': '[i]',
        '⚪': '[ ]',
        # Subscript numbers
        '₀': '0',
        '₁': '1',
        '₂': '2',
        '₃': '3',
        '₄': '4',
        '₅': '5',
        '₆': '6',
        '₇': '7',
        '₈': '8',
        '₉': '9',
        # Superscript numbers
        '⁰': '^0',
        '¹': '^1',
        '²': '^2',
        '³': '^3',
        '⁴': '^4',
        '⁵': '^5',
        '⁶': '^6',
        '⁷': '^7',
        '⁸': '^8',
        '⁹': '^9',
        # Greek letters commonly used in formulas
        'α': 'alpha',
        'β': 'beta',
        'γ': 'gamma',
        'δ': 'delta',
        'σ': 'sigma',
        'Σ': 'Sigma',
        'Ψ': 'Psi',
        'λ': 'lambda',
        'π': 'pi',
        'Π': 'Pi',
        'μ': 'mu',
        'ε': 'epsilon',
        'θ': 'theta',
        'φ': 'phi',
        'ω': 'omega',
        'Ω': 'Omega',
        'ρ': 'rho',
        'τ': 'tau',
        'κ': 'kappa',
    }

    for emoji, replacement in emoji_replacements.items():
        text = text.replace(emoji, replacement)

    # Remove any remaining emoji-like characters (Unicode range)
    # This is a fallback for any emojis not in the replacement dict
    text = re.sub(r'[\U00010000-\U0010ffff]', '', text)

    return text


def preprocess_markdown(content: str, for_latex: bool = True) -> str:
    """Vorverarbeitung des Markdown-Inhalts."""
    content = apply_swiss_orthography(content)
    content = format_numbers_swiss(content)
    if for_latex:
        content = replace_emojis_for_latex(content)
    return content


def detect_session_id(content: str, filepath: Path) -> Optional[str]:
    """Erkennt die Session-ID aus Inhalt oder Dateipfad."""
    # Aus Frontmatter
    frontmatter, _ = extract_yaml_frontmatter(content)
    if 'session-id' in frontmatter:
        return frontmatter['session-id']

    # Aus Inhalt
    match = re.search(r'Session[:\s-]*([A-Z]{3}-S-\d{4}-\d{2}-\d{2}-[A-Z]+-\d+)', content)
    if match:
        return match.group(1)

    # Aus Dateipfad
    for part in filepath.parts:
        if part.startswith('EBF-S-'):
            return part

    return None


def generate_cover_page(metadata: Dict[str, Any], output_path: Path) -> Optional[Path]:
    """
    Generiert ein PDF-Cover-Page aus dem LaTeX-Template.

    Args:
        metadata: Dict mit title, subtitle, doctype, date, client, auftraggeber, mandantin, version
        output_path: Pfad für die Cover-Page PDF

    Returns:
        Pfad zur generierten Cover-PDF oder None bei Fehler
    """
    if not COVER_TEMPLATE.exists():
        print(f"⚠️ Cover-Template nicht gefunden: {COVER_TEMPLATE}")
        return None

    # LaTeX-Datei mit angepassten Parametern erstellen
    with open(COVER_TEMPLATE, 'r', encoding='utf-8') as f:
        template_content = f.read()

    # Parameter ersetzen (neues Design mit allen Feldern)
    replacements = {
        r'\\renewcommand{\\FADocType}{[^}]*}':
            f'\\\\renewcommand{{\\\\FADocType}}{{{metadata.get("doctype", "PROJEKTBRIEFING")}}}',
        r'\\renewcommand{\\FATitle}{[^}]*}':
            f'\\\\renewcommand{{\\\\FATitle}}{{{metadata.get("title", "Haupttitel")}}}',
        r'\\renewcommand{\\FASubtitle}{[^}]*}':
            f'\\\\renewcommand{{\\\\FASubtitle}}{{{metadata.get("subtitle", "")}}}',
        r'\\renewcommand{\\FASubtitleTwo}{[^}]*}':
            f'\\\\renewcommand{{\\\\FASubtitleTwo}}{{{metadata.get("subtitle2", "")}}}',
        r'\\renewcommand{\\FAClient}{[^}]*}':
            f'\\\\renewcommand{{\\\\FAClient}}{{{metadata.get("client", "")}}}',
        r'\\renewcommand{\\FAAuftraggeber}{[^}]*}':
            f'\\\\renewcommand{{\\\\FAAuftraggeber}}{{{metadata.get("auftraggeber", "")}}}',
        r'\\renewcommand{\\FAMandantin}{[^}]*}':
            f'\\\\renewcommand{{\\\\FAMandantin}}{{{metadata.get("mandantin", "")}}}',
        r'\\renewcommand{\\FADate}{[^}]*}':
            f'\\\\renewcommand{{\\\\FADate}}{{{metadata.get("date", "")}}}',
        r'\\renewcommand{\\FAVersion}{[^}]*}':
            f'\\\\renewcommand{{\\\\FAVersion}}{{{metadata.get("version", "1.0")}}}',
    }

    for pattern, replacement in replacements.items():
        template_content = re.sub(pattern, replacement, template_content)

    # Temporäre LaTeX-Datei erstellen
    with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False, encoding='utf-8') as tmp:
        tmp.write(template_content)
        tmp_tex = Path(tmp.name)

    try:
        # LaTeX kompilieren
        cmd = [
            'pdflatex',
            '-interaction=nonstopmode',
            '-output-directory', str(tmp_tex.parent),
            str(tmp_tex)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(PROJECT_ROOT))

        if result.returncode == 0:
            tmp_pdf = tmp_tex.with_suffix('.pdf')
            if tmp_pdf.exists():
                # PDF an Zielort kopieren
                import shutil
                shutil.copy(tmp_pdf, output_path)
                print(f"✅ Cover-Page erstellt: {output_path}")
                return output_path
        else:
            print(f"⚠️ Cover-Page Fehler: {result.stderr[:200] if result.stderr else 'Unbekannt'}")

    finally:
        # Temporäre Dateien aufräumen
        for ext in ['.tex', '.pdf', '.aux', '.log']:
            tmp_file = tmp_tex.with_suffix(ext)
            if tmp_file.exists():
                tmp_file.unlink()

    return None


def merge_pdfs(pdf_list: list, output_path: Path) -> bool:
    """
    Fügt mehrere PDFs zu einer Datei zusammen.

    Args:
        pdf_list: Liste von PDF-Pfaden
        output_path: Pfad für die zusammengefügte PDF

    Returns:
        True bei Erfolg
    """
    try:
        # Versuche PyPDF2
        from PyPDF2 import PdfMerger
        merger = PdfMerger()
        for pdf in pdf_list:
            if Path(pdf).exists():
                merger.append(str(pdf))
        merger.write(str(output_path))
        merger.close()
        return True
    except ImportError:
        pass

    try:
        # Fallback: pdftk
        cmd = ['pdftk'] + [str(p) for p in pdf_list] + ['cat', 'output', str(output_path)]
        result = subprocess.run(cmd, capture_output=True)
        return result.returncode == 0
    except FileNotFoundError:
        pass

    try:
        # Fallback: pdfunite (Teil von Poppler)
        cmd = ['pdfunite'] + [str(p) for p in pdf_list] + [str(output_path)]
        result = subprocess.run(cmd, capture_output=True)
        return result.returncode == 0
    except FileNotFoundError:
        pass

    print("⚠️ Kein PDF-Merge-Tool gefunden. Installiere: pip install PyPDF2")
    return False


def generate_back_page(metadata: Dict[str, Any], output_path: Path) -> Optional[Path]:
    """
    Generiert ein PDF-Back-Page aus dem LaTeX-Template.

    Args:
        metadata: Dict mit year (optional)
        output_path: Pfad für die Back-Page PDF

    Returns:
        Pfad zur generierten Back-PDF oder None bei Fehler
    """
    if not BACK_TEMPLATE.exists():
        print(f"⚠️ Back-Template nicht gefunden: {BACK_TEMPLATE}")
        return None

    # LaTeX-Datei mit angepassten Parametern erstellen
    with open(BACK_TEMPLATE, 'r', encoding='utf-8') as f:
        template_content = f.read()

    # Jahr aus Datum extrahieren oder aktuelles Jahr verwenden
    year = datetime.now().year
    if 'date' in metadata and metadata['date']:
        # Versuche Jahr aus Datum zu extrahieren
        import re
        year_match = re.search(r'20\d{2}', str(metadata['date']))
        if year_match:
            year = year_match.group(0)

    # Parameter ersetzen
    template_content = re.sub(
        r'\\renewcommand{\\FAYear}{[^}]*}',
        f'\\\\renewcommand{{\\\\FAYear}}{{{year}}}',
        template_content
    )

    # Temporäre LaTeX-Datei erstellen
    with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False, encoding='utf-8') as tmp:
        tmp.write(template_content)
        tmp_tex = Path(tmp.name)

    try:
        # LaTeX kompilieren
        cmd = [
            'pdflatex',
            '-interaction=nonstopmode',
            '-output-directory', str(tmp_tex.parent),
            str(tmp_tex)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(PROJECT_ROOT))

        if result.returncode == 0:
            tmp_pdf = tmp_tex.with_suffix('.pdf')
            if tmp_pdf.exists():
                # PDF an Zielort kopieren
                import shutil
                shutil.copy(tmp_pdf, output_path)
                print(f"✅ Back-Page erstellt: {output_path}")
                return output_path
        else:
            print(f"⚠️ Back-Page Fehler: {result.stderr[:200] if result.stderr else 'Unbekannt'}")

    finally:
        # Temporäre Dateien aufräumen
        for ext in ['.tex', '.pdf', '.aux', '.log']:
            tmp_file = tmp_tex.with_suffix(ext)
            if tmp_file.exists():
                tmp_file.unlink()

    return None


def generate_toc_page(metadata: Dict[str, Any], toc_entries: list, output_path: Path) -> Optional[Path]:
    """
    Generiert ein PDF-Inhaltsverzeichnis aus dem LaTeX-Template.

    Args:
        metadata: Dict mit project, client, page_num, total_pages
        toc_entries: Liste von Dicts mit num, title, page
        output_path: Pfad für die TOC-Page PDF

    Returns:
        Pfad zur generierten TOC-PDF oder None bei Fehler
    """
    if not TOC_TEMPLATE.exists():
        print(f"⚠️ TOC-Template nicht gefunden: {TOC_TEMPLATE}")
        return None

    # LaTeX-Datei mit angepassten Parametern erstellen
    with open(TOC_TEMPLATE, 'r', encoding='utf-8') as f:
        template_content = f.read()

    # Parameter ersetzen
    replacements = {
        r'\\renewcommand{\\FAPageNum}{[^}]*}':
            f'\\\\renewcommand{{\\\\FAPageNum}}{{{metadata.get("page_num", "4")}}}',
        r'\\renewcommand{\\FATotalPages}{[^}]*}':
            f'\\\\renewcommand{{\\\\FATotalPages}}{{{metadata.get("total_pages", "34")}}}',
        r'\\renewcommand{\\FAProject}{[^}]*}':
            f'\\\\renewcommand{{\\\\FAProject}}{{{metadata.get("project", "PROJEKT")}}}',
        r'\\renewcommand{\\FAClient}{[^}]*}':
            f'\\\\renewcommand{{\\\\FAClient}}{{{metadata.get("client", "KUNDEN NAME")}}}',
    }

    for pattern, replacement in replacements.items():
        template_content = re.sub(pattern, replacement, template_content)

    # TOC-Einträge generieren
    if toc_entries:
        toc_latex = ""
        for entry in toc_entries:
            num = entry.get('num', '')
            title = entry.get('title', '')
            page = entry.get('page', '')
            toc_latex += f"\\tocentrySimple{{{num}}}{{{title}}}{{{page}}}\n"

        # Ersetze die TOC-Einträge im Template
        # Finde den Bereich zwischen "--- TOC Einträge ---" und "\\newpage"
        toc_pattern = r'(\\color{fadarkgray}\n)(\\tocentrySimple.*?)(\\newpage)'
        template_content = re.sub(
            toc_pattern,
            f'\\1{toc_latex}\\3',
            template_content,
            flags=re.DOTALL
        )

    # Temporäre LaTeX-Datei erstellen
    with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False, encoding='utf-8') as tmp:
        tmp.write(template_content)
        tmp_tex = Path(tmp.name)

    try:
        # LaTeX kompilieren
        cmd = [
            'pdflatex',
            '-interaction=nonstopmode',
            '-output-directory', str(tmp_tex.parent),
            str(tmp_tex)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(PROJECT_ROOT))

        if result.returncode == 0:
            tmp_pdf = tmp_tex.with_suffix('.pdf')
            if tmp_pdf.exists():
                # PDF an Zielort kopieren
                import shutil
                shutil.copy(tmp_pdf, output_path)
                print(f"✅ TOC-Page erstellt: {output_path}")
                return output_path
        else:
            print(f"⚠️ TOC-Page Fehler: {result.stderr[:200] if result.stderr else 'Unbekannt'}")

    finally:
        # Temporäre Dateien aufräumen
        for ext in ['.tex', '.pdf', '.aux', '.log']:
            tmp_file = tmp_tex.with_suffix(ext)
            if tmp_file.exists():
                tmp_file.unlink()

    return None


# =============================================================================
# KONVERTIERUNGSFUNKTIONEN
# =============================================================================

def convert_to_pdf_latex(input_file: Path, output_file: Path, metadata: Dict[str, Any]) -> bool:
    """Konvertiert Markdown → PDF via Pandoc + LaTeX."""
    print(f"📄 Konvertiere {input_file.name} → PDF (LaTeX)...")

    if not LATEX_TEMPLATE.exists():
        print(f"❌ LaTeX-Template nicht gefunden: {LATEX_TEMPLATE}")
        return False

    # Pandoc-Kommando
    cmd = [
        'pandoc',
        str(input_file),
        '-o', str(output_file),
        f'--template={LATEX_TEMPLATE}',
        '--pdf-engine=pdflatex',
        '--toc',
        '-f', 'markdown-simple_tables-multiline_tables-grid_tables',  # Use pipe tables only
        '-V', f'title={metadata.get("title", "Strategisches Dossier")}',
        '-V', f'subtitle={metadata.get("subtitle", "")}',
        '-V', f'doctype={metadata.get("doctype", DEFAULT_DOCTYPE)}',
        '-V', f'date={metadata.get("date", datetime.now().strftime("%d. %B %Y"))}',
        '-V', f'session-id={metadata.get("session-id", "")}',
        '-V', 'lang=de-CH',
        '-V', 'geometry=a4paper',
    ]

    # Logo hinzufügen falls vorhanden
    logo_path = ASSETS_DIR / "logos" / "fehradvice_logo.png"
    if logo_path.exists():
        cmd.extend(['-V', f'logo={logo_path}'])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ PDF erstellt: {output_file}")
            return True
        else:
            print(f"❌ Pandoc-Fehler: {result.stderr}")
            # Diagnose aus Learnings-DB
            print_diagnostic(result.stderr)
            return False
    except FileNotFoundError:
        print("❌ Pandoc nicht installiert.")
        print_diagnostic("Pandoc nicht installiert")
        return False


def convert_to_pdf_weasyprint(input_file: Path, output_file: Path, metadata: Dict[str, Any]) -> bool:
    """Konvertiert Markdown → HTML → PDF via WeasyPrint."""
    print(f"📄 Konvertiere {input_file.name} → PDF (WeasyPrint)...")

    if not CSS_TEMPLATE.exists():
        print(f"❌ CSS-Template nicht gefunden: {CSS_TEMPLATE}")
        return False

    # Erst nach HTML konvertieren
    with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as tmp:
        tmp_html = Path(tmp.name)

    try:
        # Markdown → HTML
        cmd_html = [
            'pandoc',
            str(input_file),
            '-o', str(tmp_html),
            '-s',  # Standalone
            f'--css={CSS_TEMPLATE}',
            '-V', f'title={metadata.get("title", "Strategisches Dossier")}',
            '-V', 'lang=de-CH',
            '--metadata', f'title={metadata.get("title", "")}',
        ]

        result = subprocess.run(cmd_html, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Pandoc HTML-Fehler: {result.stderr}")
            return False

        # HTML → PDF via WeasyPrint
        try:
            from weasyprint import HTML, CSS
            html_doc = HTML(filename=str(tmp_html))
            css_doc = CSS(filename=str(CSS_TEMPLATE))
            html_doc.write_pdf(str(output_file), stylesheets=[css_doc])
            print(f"✅ PDF erstellt: {output_file}")
            return True
        except ImportError:
            print("⚠️ WeasyPrint nicht installiert. Fallback zu wkhtmltopdf...")

            # Fallback: wkhtmltopdf
            cmd_pdf = [
                'wkhtmltopdf',
                '--enable-local-file-access',
                str(tmp_html),
                str(output_file)
            ]
            result = subprocess.run(cmd_pdf, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ PDF erstellt: {output_file}")
                return True
            else:
                print(f"❌ wkhtmltopdf-Fehler: {result.stderr}")
                return False

    finally:
        if tmp_html.exists():
            tmp_html.unlink()


def convert_to_html(input_file: Path, output_file: Path, metadata: Dict[str, Any]) -> bool:
    """Konvertiert Markdown → HTML."""
    print(f"🌐 Konvertiere {input_file.name} → HTML...")

    cmd = [
        'pandoc',
        str(input_file),
        '-o', str(output_file),
        '-s',  # Standalone
        f'--css={CSS_TEMPLATE}',
        '--embed-resources',
        '--standalone',
        '-V', f'title={metadata.get("title", "Strategisches Dossier")}',
        '-V', 'lang=de-CH',
        '--metadata', f'title={metadata.get("title", "")}',
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ HTML erstellt: {output_file}")
            return True
        else:
            print(f"❌ Pandoc-Fehler: {result.stderr}")
            return False
    except FileNotFoundError:
        print("❌ Pandoc nicht installiert.")
        return False


def convert_to_pptx(input_file: Path, output_file: Path, metadata: Dict[str, Any]) -> bool:
    """Konvertiert Markdown → PowerPoint."""
    print(f"📊 Konvertiere {input_file.name} → PPTX...")

    if not PPTX_TEMPLATE.exists():
        print(f"⚠️ PPTX-Template nicht gefunden: {PPTX_TEMPLATE}")
        print("   Verwende Standard-Template...")
        reference_doc = None
    else:
        reference_doc = str(PPTX_TEMPLATE)

    cmd = [
        'pandoc',
        str(input_file),
        '-o', str(output_file),
        '-t', 'pptx',
    ]

    if reference_doc:
        cmd.extend(['--reference-doc', reference_doc])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ PPTX erstellt: {output_file}")
            return True
        else:
            print(f"❌ Pandoc-Fehler: {result.stderr}")
            return False
    except FileNotFoundError:
        print("❌ Pandoc nicht installiert.")
        return False


def convert_to_docx(input_file: Path, output_file: Path, metadata: Dict[str, Any]) -> bool:
    """Konvertiert Markdown → Word DOCX."""
    print(f"📝 Konvertiere {input_file.name} → DOCX...")

    # Reference-Doc für Styling
    reference_doc = TEMPLATES_DIR / "executive-summary-template.docx"

    cmd = [
        'pandoc',
        str(input_file),
        '-o', str(output_file),
    ]

    if reference_doc.exists():
        cmd.extend(['--reference-doc', str(reference_doc)])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ DOCX erstellt: {output_file}")
            return True
        else:
            print(f"❌ Pandoc-Fehler: {result.stderr}")
            return False
    except FileNotFoundError:
        print("❌ Pandoc nicht installiert.")
        return False


# =============================================================================
# HAUPTFUNKTION
# =============================================================================

def format_report(
    input_path: str,
    output_path: Optional[str] = None,
    output_format: str = 'pdf',
    engine: str = 'latex',
    preprocess: bool = True,
    with_cover: bool = False,
    with_back: bool = False,
    with_toc: bool = False,
    toc_entries: Optional[list] = None
) -> bool:
    """
    Hauptfunktion für Report-Formatierung.

    Args:
        input_path: Pfad zur Markdown-Eingabedatei
        output_path: Pfad zur Ausgabedatei (optional)
        output_format: Ausgabeformat (pdf, html, pptx, docx)
        engine: PDF-Engine (latex, weasyprint)
        preprocess: Schweizer Orthographie anwenden
        with_cover: Cover-Page hinzufügen (nur PDF)
        with_back: Back-Page hinzufügen (nur PDF)
        with_toc: Inhaltsverzeichnis-Page hinzufügen (nur PDF)
        toc_entries: Liste von TOC-Einträgen [{num, title, page}, ...]

    Returns:
        True bei Erfolg, False bei Fehler
    """
    input_file = Path(input_path)

    if not input_file.exists():
        print(f"❌ Eingabedatei nicht gefunden: {input_file}")
        return False

    # Inhalt lesen
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Format-Empfehlung basierend auf Inhalt
    recommendation = get_format_recommendation(content, output_format)
    if recommendation:
        print(recommendation)

    # Frontmatter extrahieren
    frontmatter, body = extract_yaml_frontmatter(content)

    # Metadata zusammenstellen
    metadata = {
        'title': frontmatter.get('title', input_file.stem.replace('_', ' ').title()),
        'subtitle': frontmatter.get('subtitle', ''),
        'doctype': frontmatter.get('doctype', DEFAULT_DOCTYPE),
        'date': frontmatter.get('date', datetime.now().strftime('%d. %B %Y')),
        'session-id': detect_session_id(content, input_file) or frontmatter.get('session-id', ''),
        'author': frontmatter.get('author', DEFAULT_AUTHOR),
    }

    # Schweizer Orthographie anwenden
    for_latex = output_format == 'pdf' and engine == 'latex'
    if preprocess:
        body = preprocess_markdown(body, for_latex=for_latex)

        # Temporäre Datei mit vorverarbeitetem Inhalt
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as tmp:
            # Frontmatter zurückschreiben
            tmp.write('---\n')
            yaml.dump(metadata, tmp, allow_unicode=True, default_flow_style=False)
            tmp.write('---\n\n')
            tmp.write(body)
            tmp_path = Path(tmp.name)

        input_file = tmp_path
    else:
        tmp_path = None

    # Output-Pfad bestimmen
    if output_path:
        output_file = Path(output_path)
        # Validiere Output-Pfad
        is_recommended, message = validate_output_path(output_file)
        if message:
            print(message)
    else:
        # Standard: Workflow-Outputs-Verzeichnis verwenden
        output_file = get_default_output_path(Path(input_path), output_format)
        print(f"📁 Output: {output_file.relative_to(PROJECT_ROOT)}")

    # Ausgabeverzeichnis erstellen
    output_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        # Konvertierung durchführen
        if output_format == 'pdf':
            # Mit Cover-Page, TOC oder Back-Page?
            if with_cover or with_back or with_toc:
                parts_info = []
                if with_cover:
                    parts_info.append("Cover")
                if with_toc:
                    parts_info.append("TOC")
                if with_back:
                    parts_info.append("Back")
                print(f"📄 Generiere mit {' + '.join(parts_info)}-Page...")

                # Temporäre Pfade
                cover_pdf = output_file.parent / f"_cover_{output_file.stem}.pdf"
                toc_pdf = output_file.parent / f"_toc_{output_file.stem}.pdf"
                content_pdf = output_file.parent / f"_content_{output_file.stem}.pdf"
                back_pdf = output_file.parent / f"_back_{output_file.stem}.pdf"

                # Cover generieren (falls gewünscht)
                cover_success = generate_cover_page(metadata, cover_pdf) if with_cover else None

                # TOC generieren (falls gewünscht)
                toc_success = None
                if with_toc:
                    toc_metadata = {
                        'project': metadata.get('project', metadata.get('doctype', 'PROJEKT')),
                        'client': metadata.get('client', 'KUNDEN NAME'),
                        'page_num': '4',
                        'total_pages': '34',
                    }
                    # Default TOC-Einträge falls nicht angegeben
                    default_toc = [
                        {'num': '', 'title': 'Executive Summary', 'page': '2'},
                        {'num': '1', 'title': 'Einleitung', 'page': '5'},
                        {'num': '2', 'title': 'Methodik', 'page': '8'},
                        {'num': '3', 'title': 'Analyse', 'page': '10'},
                        {'num': '4', 'title': 'Ergebnisse', 'page': '15'},
                        {'num': '5', 'title': 'Empfehlungen', 'page': '20'},
                        {'num': '', 'title': 'Anhang', 'page': '25'},
                    ]
                    toc_success = generate_toc_page(toc_metadata, toc_entries or default_toc, toc_pdf)

                # Content generieren
                if engine == 'weasyprint':
                    content_success = convert_to_pdf_weasyprint(input_file, content_pdf, metadata)
                else:
                    content_success = convert_to_pdf_latex(input_file, content_pdf, metadata)

                # Back-Page generieren (falls gewünscht)
                back_success = generate_back_page(metadata, back_pdf) if with_back else None

                # PDF-Liste für Merge erstellen (Reihenfolge: Cover → TOC → Content → Back)
                pdfs_to_merge = []
                if with_cover and cover_success:
                    pdfs_to_merge.append(cover_pdf)
                if with_toc and toc_success:
                    pdfs_to_merge.append(toc_pdf)
                if content_success:
                    pdfs_to_merge.append(content_pdf)
                if with_back and back_success:
                    pdfs_to_merge.append(back_pdf)

                # PDFs zusammenfügen
                if content_success and len(pdfs_to_merge) > 0:
                    if len(pdfs_to_merge) > 1:
                        if merge_pdfs(pdfs_to_merge, output_file):
                            print(f"✅ PDF mit {' + '.join(parts_info)} erstellt: {output_file}")
                            success = True
                        else:
                            # Fallback: Nur Content
                            print("⚠️ PDF-Merge fehlgeschlagen. Verwende nur Content.")
                            import shutil
                            shutil.copy(content_pdf, output_file)
                            success = True
                    else:
                        # Nur Content (Cover/TOC/Back fehlgeschlagen)
                        import shutil
                        shutil.copy(content_pdf, output_file)
                        success = True
                else:
                    success = False

                # Temporäre Dateien aufräumen
                for tmp_pdf in [cover_pdf, toc_pdf, content_pdf, back_pdf]:
                    if tmp_pdf.exists():
                        tmp_pdf.unlink()
            else:
                # Ohne Cover/Back-Page
                if engine == 'weasyprint':
                    success = convert_to_pdf_weasyprint(input_file, output_file, metadata)
                else:
                    success = convert_to_pdf_latex(input_file, output_file, metadata)
        elif output_format == 'html':
            success = convert_to_html(input_file, output_file, metadata)
        elif output_format == 'pptx':
            success = convert_to_pptx(input_file, output_file, metadata)
        elif output_format == 'docx':
            success = convert_to_docx(input_file, output_file, metadata)
        else:
            print(f"❌ Unbekanntes Format: {output_format}")
            success = False

        return success

    finally:
        # Temporäre Datei aufräumen
        if tmp_path and tmp_path.exists():
            tmp_path.unlink()


def batch_format(input_dir: str, output_format: str = 'pdf') -> int:
    """Formatiert alle Markdown-Dateien in einem Verzeichnis."""
    input_path = Path(input_dir)
    if not input_path.is_dir():
        print(f"❌ Verzeichnis nicht gefunden: {input_path}")
        return 0

    md_files = list(input_path.glob('**/*.md'))
    print(f"📂 Gefunden: {len(md_files)} Markdown-Dateien")

    success_count = 0
    for md_file in md_files:
        if format_report(str(md_file), output_format=output_format):
            success_count += 1

    print(f"\n✅ {success_count}/{len(md_files)} Dateien erfolgreich konvertiert")
    return success_count


# =============================================================================
# CLI
# =============================================================================

def show_learnings():
    """Zeigt alle Learnings aus der Datenbank."""
    learnings = load_learnings()

    print("""
┌─────────────────────────────────────────────────────────────────────────┐
│  📚 REPORT FORMATTER LEARNINGS                                          │
├─────────────────────────────────────────────────────────────────────────┤
""")

    for learning in learnings.get('learnings', []):
        severity_icon = {'HIGH': '🔴', 'MEDIUM': '🟡', 'LOW': '🟢', 'INFO': 'ℹ️'}.get(
            learning.get('severity', 'INFO'), 'ℹ️')
        print(f"│  {severity_icon} {learning['id']}: {learning['title'][:50]:<50} │")

    print("""│                                                                         │
│  Details: data/report-formatter-learnings.yaml                          │
└─────────────────────────────────────────────────────────────────────────┘
""")

    # Quick Reference
    print("\n📋 QUICK REFERENCE:\n")
    for entry in learnings.get('quick_reference', []):
        print(f"  • {entry['error'][:40]:<40} → {entry['fix']}")


def main():
    parser = argparse.ArgumentParser(
        description='FehrAdvice Report Formatter - Konvertiert Markdown zu formatierten Reports',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Beispiele:
  %(prog)s report.md                          # → workflows/format-report/outputs/report.pdf
  %(prog)s report.md -o output.pdf            # Mit explizitem Output
  %(prog)s report.md -f html                  # HTML-Output
  %(prog)s report.md -f pptx                  # PowerPoint-Output
  %(prog)s report.md -f pdf --engine weasyprint  # PDF via WeasyPrint
  %(prog)s report.md --cover                  # PDF mit FehrAdvice Cover-Page
  %(prog)s report.md --back                   # PDF mit FehrAdvice Back-Page
  %(prog)s report.md --cover --back           # Vollständiges Dokument mit Cover + Back
  %(prog)s report.md --cover --toc --back     # Mit Cover + Inhaltsverzeichnis + Back
  %(prog)s --batch sessions/                  # Alle MDs im Verzeichnis
  %(prog)s --check-deps                       # Abhängigkeiten prüfen
  %(prog)s --verify                           # Workflow-Struktur überprüfen
  %(prog)s --verify --fix                     # Struktur überprüfen und reparieren
  %(prog)s --learnings                        # Alle Learnings anzeigen
  %(prog)s --add-learning                     # Neues Learning interaktiv hinzufügen

Workflow-Struktur:
  workflows/format-report/                    # Zentrales Workflow-Verzeichnis
  workflows/format-report/outputs/            # Generierte Reports (DEFAULT)
  templates/                                  # LaTeX/CSS Templates

Templates:
  LaTeX:  templates/fehradvice-report.latex
  CSS:    templates/fehradvice-report.css
  PPTX:   templates/pptx/FehrAdvice-Master.pptx

Learnings:
  data/report-formatter-learnings.yaml        # Bekannte Probleme & Lösungen
        """
    )

    parser.add_argument('input', nargs='?', help='Eingabe-Markdown-Datei')
    parser.add_argument('-o', '--output', help='Ausgabedatei')
    parser.add_argument('-f', '--format', choices=['pdf', 'html', 'pptx', 'docx'],
                        default='pdf', help='Ausgabeformat (default: pdf)')
    parser.add_argument('--engine', choices=['latex', 'weasyprint'],
                        default='latex', help='PDF-Engine (default: latex)')
    parser.add_argument('--no-preprocess', action='store_true',
                        help='Schweizer Orthographie nicht anwenden')
    parser.add_argument('--cover', action='store_true', default=True,
                        help='Cover-Page hinzufügen (Standard: aktiviert, nur PDF/DOCX)')
    parser.add_argument('--no-cover', action='store_true',
                        help='Cover-Page NICHT hinzufügen')
    parser.add_argument('--back', action='store_true', default=True,
                        help='Back-Page hinzufügen (Standard: aktiviert, nur PDF/DOCX)')
    parser.add_argument('--no-back', action='store_true',
                        help='Back-Page NICHT hinzufügen')
    parser.add_argument('--toc', action='store_true',
                        help='Inhaltsverzeichnis-Page hinzufügen (nur PDF)')
    parser.add_argument('--toc-entries', metavar='JSON',
                        help='TOC-Einträge als JSON (optional)')
    parser.add_argument('--batch', metavar='DIR',
                        help='Batch-Konvertierung aller MDs in Verzeichnis')
    parser.add_argument('--check-deps', action='store_true',
                        help='Abhängigkeiten prüfen')
    parser.add_argument('--learnings', action='store_true',
                        help='Alle Learnings anzeigen')
    parser.add_argument('--add-learning', action='store_true',
                        help='Neues Learning interaktiv hinzufügen')
    parser.add_argument('--analyze', metavar='FILE',
                        help='Datei auf potenzielle Probleme analysieren')
    parser.add_argument('--verify', action='store_true',
                        help='Workflow-Struktur überprüfen')
    parser.add_argument('--fix', action='store_true',
                        help='Fehlende Verzeichnisse automatisch erstellen (mit --verify)')
    parser.add_argument('--version', action='version', version='%(prog)s 1.3')

    args = parser.parse_args()

    # Learnings anzeigen
    if args.learnings:
        show_learnings()
        return 0

    # Neues Learning hinzufügen
    if args.add_learning:
        success = add_learning_interactive()
        return 0 if success else 1

    # Abhängigkeiten prüfen
    if args.check_deps:
        issues = check_dependencies()
        if issues:
            print("❌ Fehlende Abhängigkeiten gefunden:\n")
            for issue in issues:
                print(f"  • {issue['message']}")
                print(f"    Fix: {issue['fix']}")
                print()
            return 1
        else:
            print("✅ Alle Abhängigkeiten sind installiert.")
            return 0

    # Workflow-Struktur überprüfen
    if args.verify:
        if args.fix:
            print("🔧 Überprüfe und repariere Workflow-Struktur...")
            result = verify_workflow_structure(auto_fix=True)
            if result['fixed']:
                print("\n✅ Folgende Korrekturen wurden durchgeführt:")
                for fix in result['fixed']:
                    print(f"   • {fix}")
            if result['issues']:
                print("\n❌ Folgende Probleme konnten nicht automatisch behoben werden:")
                for issue in result['issues']:
                    print(f"   • {issue}")
                return 1
            print("\n✅ Workflow-Struktur ist jetzt vollständig.")
            return 0
        else:
            valid = print_workflow_status()
            return 0 if valid else 1

    # Datei analysieren
    if args.analyze:
        with open(args.analyze, 'r', encoding='utf-8') as f:
            content = f.read()
        issues = analyze_content_for_issues(content)
        if issues:
            print(f"📋 Analyse von {args.analyze}:\n")
            for issue in issues:
                print(f"  • [{issue['type']}] {issue['message']}")
                if 'recommendation' in issue:
                    print(f"    → {issue['recommendation']}")
                print()
        else:
            print(f"✅ Keine bekannten Probleme in {args.analyze}")
        return 0

    # Batch-Konvertierung
    if args.batch:
        return batch_format(args.batch, args.format)

    # Einzelne Datei konvertieren
    if args.input:
        # TOC-Einträge parsen falls angegeben
        toc_entries = None
        if args.toc_entries:
            import json
            try:
                toc_entries = json.loads(args.toc_entries)
            except json.JSONDecodeError:
                print("⚠️ TOC-Einträge konnten nicht geparst werden (erwarte JSON)")

        # Cover und Back sind standardmässig aktiviert (FehrAdvice Corporate Design)
        # --no-cover und --no-back deaktivieren sie explizit
        use_cover = args.cover and not args.no_cover
        use_back = args.back and not args.no_back

        success = format_report(
            args.input,
            output_path=args.output,
            output_format=args.format,
            engine=args.engine,
            preprocess=not args.no_preprocess,
            with_cover=use_cover,
            with_back=use_back,
            with_toc=args.toc,
            toc_entries=toc_entries
        )
        return 0 if success else 1

    # Keine Argumente
    parser.print_help()

    # Learning Reminder prüfen (bei leeren Argumenten)
    check_learning_reminder()

    return 1


if __name__ == '__main__':
    sys.exit(main())
