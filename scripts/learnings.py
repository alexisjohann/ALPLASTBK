#!/usr/bin/env python3
"""
=============================================================================
EBF LEARNINGS MANAGEMENT SYSTEM
=============================================================================
Zentrales System für maschinelles Lernen aus Fehlern über alle EBF-Domains.

SSOT: data/learnings-registry.yaml

Verwendung:
    python scripts/learnings.py list [domain]        # Learnings anzeigen
    python scripts/learnings.py add [domain]         # Neues Learning hinzufügen
    python scripts/learnings.py search <term>        # Suchen
    python scripts/learnings.py stats                # Statistiken
    python scripts/learnings.py check                # Relevante vor Arbeit prüfen

Version: 1.0
Date: January 2026
=============================================================================
"""

import argparse
import os
import re
import subprocess
import sys
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

# =============================================================================
# KONFIGURATION
# =============================================================================

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_DIR = PROJECT_ROOT / "data"

# Learnings Registry (SSOT)
LEARNINGS_REGISTRY = DATA_DIR / "learnings-registry.yaml"

# Domain-spezifische Learnings-Dateien
DOMAIN_FILES = {
    'RPT': DATA_DIR / "report-formatter-learnings.yaml",
    'INO': DATA_DIR / "innosuisse-learnings.yaml",
    'INT': DATA_DIR / "paper-integration-learnings.yaml",
    'MOD': DATA_DIR / "model-building-learnings.yaml",
    'EIP': DATA_DIR / "eip-learnings.yaml",
    'GEN': DATA_DIR / "general-learnings.yaml",
}

# Domain-Beschreibungen
DOMAIN_DESCRIPTIONS = {
    'RPT': 'Report Formatter (PDF, LaTeX, Templates)',
    'INO': 'Innosuisse / BEATRIX Projekt',
    'INT': 'Paper Integration (BibTeX, Theory Catalog)',
    'MOD': 'Model Building (10C, Interventionen)',
    'EIP': 'Evidence Integration Pipeline',
    'GEN': 'General / Other',
}

# Kategorien (übergreifend)
CATEGORIES = {
    'LATEX': 'LaTeX/PDF Generierung',
    'UNICODE': 'Unicode & Encoding',
    'WORKFLOW': 'Workflow & Prozess',
    'DATA': 'Daten & Datenbanken',
    'CONSISTENCY': 'Konsistenz-Fehler',
    'VERIFICATION': 'Verifikations-Fehler',
    'TOOL': 'Tool-Nutzung',
    'DOCS': 'Dokumentation',
    'GIT': 'Git & Versionierung',
    'OTHER': 'Sonstiges',
}


# =============================================================================
# LEARNINGS LADEN & SPEICHERN
# =============================================================================

def load_domain_learnings(domain: str) -> Dict[str, Any]:
    """Lädt Learnings für eine spezifische Domain."""
    if domain not in DOMAIN_FILES:
        return {}

    filepath = DOMAIN_FILES[domain]
    if filepath.exists():
        with open(filepath, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    return {}


def save_domain_learnings(domain: str, data: Dict[str, Any]) -> bool:
    """Speichert Learnings für eine Domain."""
    if domain not in DOMAIN_FILES:
        return False

    filepath = DOMAIN_FILES[domain]
    filepath.parent.mkdir(parents=True, exist_ok=True)

    with open(filepath, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    return True


def load_all_learnings() -> Dict[str, List[Dict]]:
    """Lädt alle Learnings aus allen Domains."""
    all_learnings = {}
    for domain in DOMAIN_FILES:
        data = load_domain_learnings(domain)
        learnings = data.get('learnings', [])
        all_learnings[domain] = learnings
    return all_learnings


def get_next_learning_id(domain: str) -> str:
    """Generiert die nächste Learning-ID für eine Domain."""
    data = load_domain_learnings(domain)
    existing_ids = [l['id'] for l in data.get('learnings', [])]

    # Finde höchste Nummer
    max_num = 0
    pattern = rf'{domain}-L-(\d+)'
    for lid in existing_ids:
        match = re.match(pattern, lid)
        if match:
            max_num = max(max_num, int(match.group(1)))

    return f"{domain}-L-{max_num + 1:03d}"


# =============================================================================
# KONTEXT-ERKENNUNG
# =============================================================================

def detect_relevant_domains() -> List[str]:
    """
    Erkennt relevante Domains basierend auf aktuellen Git-Änderungen.
    """
    try:
        result = subprocess.run(
            ['git', 'diff', '--name-only', 'HEAD'],
            capture_output=True, text=True, cwd=str(PROJECT_ROOT)
        )
        changed_files = result.stdout.strip().split('\n') if result.stdout.strip() else []

        domains = set()

        for f in changed_files:
            # Report Formatter
            if 'format_report' in f or 'templates/fehradvice' in f:
                domains.add('RPT')
            # Innosuisse
            if 'innosuisse' in f.lower() or 'beatrix' in f.lower() or 'funding/' in f:
                domains.add('INO')
            # Paper Integration
            if 'bcm_master.bib' in f or 'theory-catalog' in f or 'paper-' in f:
                domains.add('INT')
            # Model Building
            if 'model-registry' in f or 'intervention-registry' in f or 'design-model' in f:
                domains.add('MOD')
            # EIP
            if 'concept-registry' in f or 'eip' in f.lower():
                domains.add('EIP')

        return list(domains) if domains else ['GEN']

    except Exception:
        return ['GEN']


# =============================================================================
# COMMANDS
# =============================================================================

def cmd_list(domain: Optional[str] = None, verbose: bool = False,
             severity_filter: Optional[str] = None, category_filter: Optional[str] = None):
    """Zeigt Learnings an."""
    print("""
┌─────────────────────────────────────────────────────────────────────────┐
│  📚 EBF LEARNINGS DATABASE                                              │
└─────────────────────────────────────────────────────────────────────────┘
""")

    if domain:
        domains = [domain.upper()]
    else:
        domains = list(DOMAIN_FILES.keys())

    # Filter-Info anzeigen
    filters = []
    if severity_filter:
        filters.append(f"severity={severity_filter}")
    if category_filter:
        filters.append(f"category={category_filter}")
    if filters:
        print(f"Filter: {', '.join(filters)}\n")

    total = 0
    shown = 0
    for d in domains:
        data = load_domain_learnings(d)
        learnings = data.get('learnings', [])

        # Filter anwenden
        filtered = []
        for l in learnings:
            if severity_filter and l.get('severity', '').upper() != severity_filter.upper():
                continue
            if category_filter and l.get('category', '').upper() != category_filter.upper():
                continue
            filtered.append(l)

        if filtered:
            print(f"\n📁 {d}: {DOMAIN_DESCRIPTIONS.get(d, d)} ({len(filtered)}/{len(learnings)} Learnings)")
            print("-" * 70)

            for l in filtered:
                severity_icon = {'HIGH': '🔴', 'MEDIUM': '🟡', 'LOW': '🟢', 'INFO': 'ℹ️'}.get(
                    l.get('severity', 'INFO').upper(), 'ℹ️')
                title = l.get('title', '')[:50]
                print(f"  {severity_icon} {l['id']}: {title}")

                if verbose:
                    problem = l.get('problem', '').strip()[:100]
                    if problem:
                        print(f"      Problem: {problem}...")

            shown += len(filtered)
            total += len(learnings)

    print(f"\n{'=' * 70}")
    if severity_filter or category_filter:
        print(f"Gefiltert: {shown} von {total} Learnings")
    else:
        print(f"Total: {total} Learnings in {len(domains)} Domains")


def cmd_add(domain: Optional[str] = None):
    """Fügt ein neues Learning hinzu."""
    print("""
┌─────────────────────────────────────────────────────────────────────────┐
│  📝 NEUES LEARNING HINZUFÜGEN                                           │
└─────────────────────────────────────────────────────────────────────────┘
""")

    # Domain wählen
    if not domain:
        print("Verfügbare Domains:")
        for i, (key, desc) in enumerate(DOMAIN_DESCRIPTIONS.items(), 1):
            print(f"  {i}. {key}: {desc}")

        try:
            choice = input("\nDomain (Nummer oder Kürzel): ").strip()
            if choice.isdigit():
                domain = list(DOMAIN_DESCRIPTIONS.keys())[int(choice) - 1]
            else:
                domain = choice.upper()
        except (ValueError, IndexError):
            domain = 'GEN'
    else:
        domain = domain.upper()

    if domain not in DOMAIN_FILES:
        print(f"❌ Unbekannte Domain: {domain}")
        return False

    # Learning-ID generieren
    new_id = get_next_learning_id(domain)
    print(f"\nLearning ID: {new_id}")

    # Kategorie wählen
    print("\nKategorien:")
    cat_list = list(CATEGORIES.keys())
    for i, (key, desc) in enumerate(CATEGORIES.items(), 1):
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
    data = load_domain_learnings(domain)
    if 'learnings' not in data:
        data['learnings'] = []
    data['learnings'].append(new_learning)

    # Metadata aktualisieren
    if 'metadata' not in data:
        data['metadata'] = {
            'name': f"{domain} Learnings",
            'created': datetime.now().strftime('%Y-%m-%d'),
        }
    data['metadata']['last_updated'] = datetime.now().strftime('%Y-%m-%d')
    data['metadata']['total_learnings'] = len(data['learnings'])

    # Speichern
    if save_domain_learnings(domain, data):
        print(f"\n✅ Learning {new_id} hinzugefügt!")
        print(f"   Domain: {domain} ({DOMAIN_DESCRIPTIONS.get(domain, '')})")
        print(f"   Datei: {DOMAIN_FILES[domain].relative_to(PROJECT_ROOT)}")
        print(f"\n💡 Vergiss nicht: git add {DOMAIN_FILES[domain].relative_to(PROJECT_ROOT)}")
        return True
    else:
        print("❌ Fehler beim Speichern.")
        return False


def cmd_search(term: str):
    """Sucht in allen Learnings."""
    print(f"\n🔍 Suche nach: '{term}'\n")

    all_learnings = load_all_learnings()
    results = []

    term_lower = term.lower()

    for domain, learnings in all_learnings.items():
        for l in learnings:
            # Suche in allen Text-Feldern
            searchable = ' '.join([
                str(l.get('title', '')),
                str(l.get('problem', '')),
                str(l.get('solution', '')),
                str(l.get('lesson_learned', '')),
                str(l.get('id', '')),
            ]).lower()

            if term_lower in searchable:
                results.append((domain, l))

    if results:
        print(f"Gefunden: {len(results)} Learnings\n")
        for domain, l in results:
            severity_icon = {'HIGH': '🔴', 'MEDIUM': '🟡', 'LOW': '🟢', 'INFO': 'ℹ️'}.get(
                l.get('severity', 'INFO'), 'ℹ️')
            print(f"{severity_icon} [{domain}] {l['id']}: {l.get('title', '')}")
    else:
        print("Keine Learnings gefunden.")


def cmd_stats():
    """Zeigt Statistiken über alle Learnings."""
    print("""
┌─────────────────────────────────────────────────────────────────────────┐
│  📊 EBF LEARNINGS STATISTIKEN                                           │
└─────────────────────────────────────────────────────────────────────────┘
""")

    all_learnings = load_all_learnings()

    total = 0
    by_severity = {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0, 'INFO': 0}
    by_category = {}

    print("\n📁 Nach Domain:")
    print("-" * 50)
    for domain, learnings in all_learnings.items():
        count = len(learnings)
        total += count
        desc = DOMAIN_DESCRIPTIONS.get(domain, domain)
        bar = '█' * min(count, 30)
        print(f"  {domain}: {count:3d} {bar} {desc[:30]}")

        for l in learnings:
            sev = l.get('severity', 'INFO')
            by_severity[sev] = by_severity.get(sev, 0) + 1

            cat = l.get('category', 'OTHER')
            by_category[cat] = by_category.get(cat, 0) + 1

    print(f"\n  Total: {total}")

    print("\n🎯 Nach Severity:")
    print("-" * 50)
    for sev, icon in [('HIGH', '🔴'), ('MEDIUM', '🟡'), ('LOW', '🟢'), ('INFO', 'ℹ️')]:
        count = by_severity.get(sev, 0)
        bar = '█' * min(count, 30)
        print(f"  {icon} {sev:8s}: {count:3d} {bar}")

    print("\n📋 Nach Kategorie:")
    print("-" * 50)
    for cat, count in sorted(by_category.items(), key=lambda x: -x[1]):
        bar = '█' * min(count, 30)
        print(f"  {cat:15s}: {count:3d} {bar}")


def cmd_check():
    """Prüft relevante Learnings basierend auf aktuellem Kontext."""
    print("""
┌─────────────────────────────────────────────────────────────────────────┐
│  🔍 RELEVANTE LEARNINGS PRÜFEN                                          │
└─────────────────────────────────────────────────────────────────────────┘
""")

    domains = detect_relevant_domains()

    print(f"\n📂 Erkannte relevante Domains: {', '.join(domains)}")
    print("-" * 60)

    found = False
    for domain in domains:
        data = load_domain_learnings(domain)
        learnings = data.get('learnings', [])

        # Zeige HIGH und MEDIUM severity Learnings
        important = [l for l in learnings if l.get('severity') in ['HIGH', 'MEDIUM']]

        if important:
            found = True
            print(f"\n⚠️  {domain}: {len(important)} wichtige Learnings beachten:\n")

            for l in important[:5]:  # Max 5 pro Domain
                severity_icon = {'HIGH': '🔴', 'MEDIUM': '🟡'}.get(l.get('severity'), '⚠️')
                print(f"  {severity_icon} {l['id']}: {l.get('title', '')[:50]}")

                # Kurze Lösung zeigen
                solution = l.get('solution', '').strip().split('\n')[0][:60]
                if solution:
                    print(f"     → {solution}...")

    if not found:
        print("\n✅ Keine kritischen Learnings für aktuelle Arbeit gefunden.")

    print("\n💡 Details: python scripts/learnings.py list <domain>")


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='EBF Learnings Management System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Beispiele:
  %(prog)s list                    # Alle Learnings anzeigen
  %(prog)s list RPT                # Nur Report-Formatter Learnings
  %(prog)s add                     # Neues Learning hinzufügen (interaktiv)
  %(prog)s add INO                 # Neues Innosuisse Learning
  %(prog)s search "LaTeX"          # Nach Begriff suchen
  %(prog)s stats                   # Statistiken anzeigen
  %(prog)s check                   # Relevante Learnings für aktuellen Kontext

Domains:
  RPT  - Report Formatter (PDF, LaTeX, Templates)
  INO  - Innosuisse / BEATRIX Projekt
  INT  - Paper Integration (BibTeX, Theory Catalog)
  MOD  - Model Building (10C, Interventionen)
  EIP  - Evidence Integration Pipeline
  GEN  - General / Other
"""
    )

    subparsers = parser.add_subparsers(dest='command', help='Verfügbare Befehle')

    # list
    list_parser = subparsers.add_parser('list', help='Learnings anzeigen')
    list_parser.add_argument('domain', nargs='?', help='Domain-Filter (RPT, INO, INT, MOD, EIP, GEN)')
    list_parser.add_argument('-v', '--verbose', action='store_true', help='Ausführliche Ausgabe')
    list_parser.add_argument('-s', '--severity', choices=['high', 'medium', 'low', 'info'], help='Severity-Filter')
    list_parser.add_argument('-c', '--category', help='Kategorie-Filter')

    # add
    add_parser = subparsers.add_parser('add', help='Neues Learning hinzufügen')
    add_parser.add_argument('domain', nargs='?', help='Domain (RPT, INO, INT, MOD, EIP, GEN)')

    # search
    search_parser = subparsers.add_parser('search', help='In Learnings suchen')
    search_parser.add_argument('term', help='Suchbegriff')

    # stats
    subparsers.add_parser('stats', help='Statistiken anzeigen')

    # check
    subparsers.add_parser('check', help='Relevante Learnings für aktuellen Kontext')

    args = parser.parse_args()

    if args.command == 'list':
        cmd_list(args.domain, args.verbose, args.severity, args.category)
    elif args.command == 'add':
        cmd_add(args.domain)
    elif args.command == 'search':
        cmd_search(args.term)
    elif args.command == 'stats':
        cmd_stats()
    elif args.command == 'check':
        cmd_check()
    else:
        # Default: check
        cmd_check()


if __name__ == '__main__':
    main()
