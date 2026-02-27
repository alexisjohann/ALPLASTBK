#!/usr/bin/env python3
"""
Query the Innosuisse Learning Database
======================================

Usage:
    python scripts/query_learnings.py --tag latex
    python scripts/query_learnings.py --category DOC
    python scripts/query_learnings.py --severity high
    python scripts/query_learnings.py --error-type CONSISTENCY
    python scripts/query_learnings.py --search "version"
    python scripts/query_learnings.py --all
    python scripts/query_learnings.py --stats

Error Types:
    CONSISTENCY      - Mehrere Stellen müssen synchron aktualisiert werden
    CLASSIFICATION   - Unterscheidung/Kategorisierung von Inhaltstypen fehlt
    VERIFICATION     - Vollständigkeit wurde behauptet, nicht bewiesen
    OUTPUT_FORMAT    - Falsches Lieferformat für den Anwendungsfall
    DOMAIN_KNOWLEDGE - Kritisches domänenspezifisches Wissen fehlte
    TOOL_SEQUENCE    - Workflow-Schritte in falscher Reihenfolge
    CHECKLIST        - Systematische Prüfung wurde nicht durchgeführt
    ASSUMPTION       - Falsche Annahme über Kontext/Anforderungen

"""

import argparse
import yaml
from pathlib import Path
from typing import List, Dict, Any

LEARNING_DB_PATH = Path(__file__).parent.parent / "data" / "innosuisse-learning-database.yaml"


def load_database() -> Dict[str, Any]:
    """Load the learning database."""
    with open(LEARNING_DB_PATH, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def format_learning(learning: Dict[str, Any]) -> str:
    """Format a single learning for display."""
    output = []
    output.append(f"\n{'='*70}")
    output.append(f"ID: {learning['id']} | {learning['date']} | [{learning['category']}]")
    output.append(f"{'='*70}")
    output.append(f"\n📌 {learning['title']}")
    output.append(f"   Severity: {learning['severity'].upper()}")
    output.append(f"   Error Type: {learning.get('error_type', 'N/A')}")
    output.append(f"   Tags: {', '.join(learning.get('tags', []))}")

    output.append(f"\n❌ PROBLEM:")
    for line in learning['problem'].strip().split('\n'):
        output.append(f"   {line}")

    if 'concrete_example' in learning:
        output.append(f"\n📍 KONKRETES BEISPIEL:")
        for line in learning['concrete_example'].strip().split('\n'):
            output.append(f"   {line}")

    output.append(f"\n✅ LEARNING:")
    for line in learning['learning'].strip().split('\n'):
        output.append(f"   {line}")

    if 'checklist' in learning:
        output.append(f"\n📋 CHECKLISTE:")
        for item in learning['checklist']:
            output.append(f"   ☐ {item}")

    if 'prevention' in learning:
        output.append(f"\n🛡️ PRÄVENTION:")
        for line in learning['prevention'].strip().split('\n'):
            output.append(f"   {line}")

    return '\n'.join(output)


def query_by_tag(learnings: List[Dict], tag: str) -> List[Dict]:
    """Filter learnings by tag."""
    return [l for l in learnings if tag.lower() in [t.lower() for t in l.get('tags', [])]]


def query_by_category(learnings: List[Dict], category: str) -> List[Dict]:
    """Filter learnings by category."""
    return [l for l in learnings if l['category'].upper() == category.upper()]


def query_by_severity(learnings: List[Dict], severity: str) -> List[Dict]:
    """Filter learnings by severity."""
    return [l for l in learnings if l['severity'].lower() == severity.lower()]


def query_by_error_type(learnings: List[Dict], error_type: str) -> List[Dict]:
    """Filter learnings by error type."""
    return [l for l in learnings if l.get('error_type', '').upper() == error_type.upper()]


def query_by_search(learnings: List[Dict], search: str) -> List[Dict]:
    """Search learnings by text."""
    results = []
    search = search.lower()
    for l in learnings:
        searchable = f"{l['title']} {l['problem']} {l['learning']} {' '.join(l.get('tags', []))}"
        if search in searchable.lower():
            results.append(l)
    return results


def print_stats(db: Dict[str, Any]) -> None:
    """Print statistics about the learning database."""
    learnings = db.get('learnings', [])
    categories = db.get('categories', {})

    print("\n" + "="*70)
    print("INNOSUISSE LEARNING DATABASE - STATISTIKEN")
    print("="*70)

    print(f"\n📊 Gesamt: {len(learnings)} Learnings")

    print("\n📁 Nach Kategorie:")
    cat_counts = {}
    for l in learnings:
        cat = l['category']
        cat_counts[cat] = cat_counts.get(cat, 0) + 1
    for cat, name in categories.items():
        count = cat_counts.get(cat, 0)
        print(f"   {cat}: {count} ({name})")

    print("\n⚠️ Nach Severity:")
    sev_counts = {}
    for l in learnings:
        sev = l['severity']
        sev_counts[sev] = sev_counts.get(sev, 0) + 1
    for sev in ['critical', 'high', 'medium', 'low']:
        count = sev_counts.get(sev, 0)
        emoji = {'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '🟢'}[sev]
        print(f"   {emoji} {sev}: {count}")

    print("\n🔍 Nach Error Type:")
    error_type_counts = {}
    for l in learnings:
        et = l.get('error_type', 'UNKNOWN')
        error_type_counts[et] = error_type_counts.get(et, 0) + 1
    for et, count in sorted(error_type_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"   {et}: {count}")

    print("\n🏷️ Häufigste Tags:")
    tag_counts = {}
    for l in learnings:
        for tag in l.get('tags', []):
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
    sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    for tag, count in sorted_tags:
        print(f"   {tag}: {count}")

    print()


def main():
    parser = argparse.ArgumentParser(description='Query the Innosuisse Learning Database')
    parser.add_argument('--tag', '-t', help='Filter by tag')
    parser.add_argument('--category', '-c', help='Filter by category (DOC, PROC, TECH, COMM, QA, MEET)')
    parser.add_argument('--severity', '-s', help='Filter by severity (low, medium, high, critical)')
    parser.add_argument('--error-type', '-e', help='Filter by error type (CONSISTENCY, CLASSIFICATION, VERIFICATION, OUTPUT_FORMAT, DOMAIN_KNOWLEDGE, TOOL_SEQUENCE, CHECKLIST, ASSUMPTION)')
    parser.add_argument('--search', '-q', help='Search in title, problem, learning')
    parser.add_argument('--all', '-a', action='store_true', help='Show all learnings')
    parser.add_argument('--stats', action='store_true', help='Show statistics')
    parser.add_argument('--id', help='Show specific learning by ID')

    args = parser.parse_args()

    db = load_database()
    learnings = db.get('learnings', [])

    if args.stats:
        print_stats(db)
        return

    results = learnings

    if args.id:
        results = [l for l in learnings if l['id'] == args.id]
    elif args.tag:
        results = query_by_tag(learnings, args.tag)
    elif args.category:
        results = query_by_category(learnings, args.category)
    elif args.severity:
        results = query_by_severity(learnings, args.severity)
    elif args.error_type:
        results = query_by_error_type(learnings, args.error_type)
    elif args.search:
        results = query_by_search(learnings, args.search)
    elif not args.all:
        parser.print_help()
        return

    if results:
        print(f"\n🔍 {len(results)} Learning(s) gefunden:")
        for learning in results:
            print(format_learning(learning))
    else:
        print("\n❌ Keine Learnings gefunden.")


if __name__ == '__main__':
    main()
