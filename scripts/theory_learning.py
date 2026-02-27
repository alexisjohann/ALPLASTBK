#!/usr/bin/env python3
"""
Theory Learning Loop
====================

Enables the theory catalog to learn from:
1. Project results (intervention outcomes)
2. New papers (with theory_support field)
3. Meta-analyses (parameter range updates)
4. New theories (via EIP workflow)

Usage:
    # Learn from project result
    python scripts/theory_learning.py --project-result project_id predicted actual

    # Sync papers with theory_support to catalog
    python scripts/theory_learning.py --sync-papers

    # Update parameter range from meta-analysis
    python scripts/theory_learning.py --update-param MS-RD-001 lambda "1.8-2.5" "DellaVigna2018"

    # Add new theory (after EIP validation)
    python scripts/theory_learning.py --add-theory CAT-03 "New Theory Name" "Author" 2024

    # Show learning history
    python scripts/theory_learning.py --history

    # Show statistics
    python scripts/theory_learning.py --stats

Author: EBF Team
Version: 1.0 (January 2026)
"""

import argparse
import yaml
import re
import os
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Paths
SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
THEORY_CATALOG = ROOT_DIR / "data" / "theory-catalog.yaml"
BIB_FILE = ROOT_DIR / "bibliography" / "bcm_master.bib"
INTERVENTION_REGISTRY = ROOT_DIR / "data" / "intervention-registry.yaml"
LEARNING_LOG = ROOT_DIR / "data" / "theory-learning-log.yaml"


def load_yaml(path):
    """Load a YAML file."""
    if not path.exists():
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f) or {}


def save_yaml(data, path):
    """Save data to a YAML file."""
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def load_learning_log():
    """Load or initialize the learning log."""
    if not LEARNING_LOG.exists():
        return {
            'metadata': {
                'created': datetime.now().isoformat(),
                'last_updated': datetime.now().isoformat(),
                'total_updates': 0
            },
            'updates': []
        }
    return load_yaml(LEARNING_LOG)


def save_learning_log(log):
    """Save the learning log."""
    log['metadata']['last_updated'] = datetime.now().isoformat()
    log['metadata']['total_updates'] = len(log.get('updates', []))
    save_yaml(log, LEARNING_LOG)


def parse_bibtex_theory_support(bib_path):
    """Parse BibTeX file and extract entries with theory_support field."""
    entries = {}

    with open(bib_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Simple BibTeX parser
    entry_pattern = r'@(\w+)\{([^,]+),([^@]*)'
    matches = re.findall(entry_pattern, content, re.DOTALL)

    for entry_type, key, fields in matches:
        # Extract theory_support field
        theory_match = re.search(r'theory_support\s*=\s*\{([^}]*)\}', fields)
        if theory_match:
            theory_ids = [t.strip() for t in theory_match.group(1).split(',')]
            entries[key.strip()] = theory_ids

    return entries


def learn_from_project(project_id, predicted, actual, notes=""):
    """
    Learn from a project result by comparing prediction to actual outcome.

    If deviation > threshold, suggests parameter updates.
    """
    catalog = load_yaml(THEORY_CATALOG)
    log = load_learning_log()

    deviation = abs(float(actual) - float(predicted))
    deviation_pct = (deviation / float(predicted)) * 100 if float(predicted) != 0 else 0

    update = {
        'timestamp': datetime.now().isoformat(),
        'type': 'project_result',
        'project_id': project_id,
        'predicted': float(predicted),
        'actual': float(actual),
        'deviation': deviation,
        'deviation_pct': round(deviation_pct, 2),
        'notes': notes,
        'action_taken': None
    }

    # Determine if significant deviation
    if deviation_pct > 20:
        update['action_taken'] = 'REVIEW_RECOMMENDED'
        update['recommendation'] = f"Deviation {deviation_pct:.1f}% exceeds 20% threshold. Review parameter assumptions."
        print(f"\n⚠️  SIGNIFICANT DEVIATION DETECTED")
        print(f"   Project: {project_id}")
        print(f"   Predicted: {predicted}")
        print(f"   Actual: {actual}")
        print(f"   Deviation: {deviation_pct:.1f}%")
        print(f"\n   RECOMMENDATION: Review parameter assumptions in BBB (CORE-WHERE)")
    elif deviation_pct > 10:
        update['action_taken'] = 'LOGGED'
        update['recommendation'] = f"Moderate deviation {deviation_pct:.1f}%. Monitor for pattern."
        print(f"\n📊 Moderate deviation logged ({deviation_pct:.1f}%)")
    else:
        update['action_taken'] = 'CONFIRMED'
        update['recommendation'] = f"Prediction accurate within 10%. Model validated."
        print(f"\n✅ Prediction confirmed (deviation {deviation_pct:.1f}%)")

    log['updates'].append(update)
    save_learning_log(log)

    return update


def sync_papers_to_theories():
    """
    Sync papers with theory_support field to theory catalog bib_keys.
    """
    catalog = load_yaml(THEORY_CATALOG)
    log = load_learning_log()

    # Get all papers with theory_support
    paper_theories = parse_bibtex_theory_support(BIB_FILE)

    if not paper_theories:
        print("No papers with theory_support field found.")
        return

    updates_made = 0

    # For each paper, add to relevant theory's bib_keys
    for paper_key, theory_ids in paper_theories.items():
        for theory_id in theory_ids:
            # Find the theory in catalog
            for cat in catalog.get('categories', []):
                for theory in cat.get('theories', []):
                    if theory['id'] == theory_id:
                        # Add paper if not already in bib_keys
                        if 'bib_keys' not in theory:
                            theory['bib_keys'] = []
                        if paper_key not in theory['bib_keys']:
                            theory['bib_keys'].append(paper_key)
                            updates_made += 1
                            print(f"  Added {paper_key} → {theory_id}")

    if updates_made > 0:
        # Save updated catalog
        save_yaml(catalog, THEORY_CATALOG)

        # Log the sync
        update = {
            'timestamp': datetime.now().isoformat(),
            'type': 'paper_sync',
            'papers_synced': len(paper_theories),
            'updates_made': updates_made,
            'action_taken': 'SYNCED'
        }
        log['updates'].append(update)
        save_learning_log(log)

        print(f"\n✅ Synced {updates_made} paper-theory links")
    else:
        print("\n📊 All papers already synced")

    return updates_made


def update_parameter(theory_id, param_name, new_range, source):
    """
    Update a parameter range for a theory based on new evidence.
    """
    catalog = load_yaml(THEORY_CATALOG)
    log = load_learning_log()

    # Find the theory
    theory_found = None
    for cat in catalog.get('categories', []):
        for theory in cat.get('theories', []):
            if theory['id'] == theory_id:
                theory_found = theory
                break
        if theory_found:
            break

    if not theory_found:
        print(f"❌ Theory not found: {theory_id}")
        return None

    # Get old value
    old_value = theory_found.get('ebf_restrictions', {}).get(param_name, 'N/A')

    # Update the parameter
    if 'ebf_restrictions' not in theory_found:
        theory_found['ebf_restrictions'] = {}
    theory_found['ebf_restrictions'][param_name] = new_range

    # Add update history to theory
    if 'update_history' not in theory_found:
        theory_found['update_history'] = []
    theory_found['update_history'].append({
        'date': datetime.now().strftime('%Y-%m-%d'),
        'param': param_name,
        'old': str(old_value),
        'new': new_range,
        'source': source
    })

    # Save catalog
    save_yaml(catalog, THEORY_CATALOG)

    # Log the update
    update = {
        'timestamp': datetime.now().isoformat(),
        'type': 'parameter_update',
        'theory_id': theory_id,
        'parameter': param_name,
        'old_value': str(old_value),
        'new_value': new_range,
        'source': source,
        'action_taken': 'UPDATED'
    }
    log['updates'].append(update)
    save_learning_log(log)

    print(f"\n✅ Updated {theory_id}.{param_name}")
    print(f"   Old: {old_value}")
    print(f"   New: {new_range}")
    print(f"   Source: {source}")

    return update


def add_theory(category_id, name, authors, year, restrictions=None):
    """
    Add a new theory to the catalog (after EIP validation).
    """
    catalog = load_yaml(THEORY_CATALOG)
    log = load_learning_log()

    # Find the category
    target_cat = None
    for cat in catalog.get('categories', []):
        if cat['id'] == category_id:
            target_cat = cat
            break

    if not target_cat:
        print(f"❌ Category not found: {category_id}")
        return None

    # Generate new theory ID
    existing_ids = [t['id'] for t in target_cat.get('theories', [])]
    cat_prefix = category_id.replace('CAT-', 'MS-')

    # Map category to theory prefix
    prefix_map = {
        'CAT-01': 'MS-CL', 'CAT-02': 'MS-SP', 'CAT-03': 'MS-RD',
        'CAT-04': 'MS-TP', 'CAT-05': 'MS-IB', 'CAT-06': 'MS-IN',
        'CAT-07': 'MS-IF', 'CAT-08': 'MS-SI', 'CAT-09': 'MS-BF',
        'CAT-10': 'MS-NU', 'CAT-11': 'MS-NE', 'CAT-12': 'MS-WB',
        'CAT-13': 'MS-DV'
    }
    prefix = prefix_map.get(category_id, 'MS-XX')

    # Find next available number
    existing_nums = []
    for tid in existing_ids:
        if tid.startswith(prefix):
            try:
                num = int(tid.split('-')[-1])
                existing_nums.append(num)
            except ValueError:
                pass
    next_num = max(existing_nums, default=0) + 1
    new_id = f"{prefix}-{next_num:03d}"

    # Create new theory entry
    new_theory = {
        'id': new_id,
        'name': name,
        'authors': authors,
        'year': year,
        'ebf_restrictions': restrictions or {},
        'validity': 'To be determined',
        'bib_keys': [],
        'added_via': 'EIP',
        'added_date': datetime.now().strftime('%Y-%m-%d')
    }

    # Add to category
    if 'theories' not in target_cat:
        target_cat['theories'] = []
    target_cat['theories'].append(new_theory)

    # Update metadata
    catalog['metadata']['total_theories'] = sum(
        len(cat.get('theories', [])) for cat in catalog.get('categories', [])
    )
    catalog['metadata']['last_updated'] = datetime.now().strftime('%Y-%m-%d')

    # Save catalog
    save_yaml(catalog, THEORY_CATALOG)

    # Log the addition
    update = {
        'timestamp': datetime.now().isoformat(),
        'type': 'theory_added',
        'theory_id': new_id,
        'name': name,
        'category': category_id,
        'action_taken': 'ADDED'
    }
    log['updates'].append(update)
    save_learning_log(log)

    print(f"\n✅ Added new theory: {new_id}")
    print(f"   Name: {name}")
    print(f"   Authors: {authors} ({year})")
    print(f"   Category: {target_cat['name']}")

    return new_theory


def show_history(limit=20):
    """Show recent learning history."""
    log = load_learning_log()

    updates = log.get('updates', [])
    if not updates:
        print("\nNo learning history yet.")
        return

    print(f"\n=== Learning History (last {min(limit, len(updates))} of {len(updates)}) ===\n")

    for update in updates[-limit:]:
        timestamp = update.get('timestamp', 'Unknown')[:10]
        update_type = update.get('type', 'unknown')
        action = update.get('action_taken', 'N/A')

        if update_type == 'project_result':
            print(f"[{timestamp}] PROJECT: {update.get('project_id')} | "
                  f"Deviation: {update.get('deviation_pct')}% | Action: {action}")
        elif update_type == 'paper_sync':
            print(f"[{timestamp}] SYNC: {update.get('updates_made')} paper-theory links added")
        elif update_type == 'parameter_update':
            print(f"[{timestamp}] PARAM: {update.get('theory_id')}.{update.get('parameter')} | "
                  f"{update.get('old_value')} → {update.get('new_value')}")
        elif update_type == 'theory_added':
            print(f"[{timestamp}] NEW: {update.get('theory_id')} - {update.get('name')}")


def show_statistics():
    """Show learning statistics."""
    log = load_learning_log()
    catalog = load_yaml(THEORY_CATALOG)

    updates = log.get('updates', [])

    # Count by type
    type_counts = defaultdict(int)
    for u in updates:
        type_counts[u.get('type', 'unknown')] += 1

    # Count theories and papers
    total_theories = sum(
        len(cat.get('theories', [])) for cat in catalog.get('categories', [])
    )
    total_bib_keys = sum(
        len(t.get('bib_keys', []))
        for cat in catalog.get('categories', [])
        for t in cat.get('theories', [])
    )

    # Project result stats
    project_results = [u for u in updates if u.get('type') == 'project_result']
    if project_results:
        avg_deviation = sum(u.get('deviation_pct', 0) for u in project_results) / len(project_results)
        confirmed = sum(1 for u in project_results if u.get('action_taken') == 'CONFIRMED')
    else:
        avg_deviation = 0
        confirmed = 0

    print("\n=== Theory Learning Statistics ===\n")
    print(f"Total Theories: {total_theories}")
    print(f"Total Paper Links: {total_bib_keys}")
    print(f"Total Learning Updates: {len(updates)}")
    print(f"\nUpdates by Type:")
    for utype, count in sorted(type_counts.items()):
        print(f"  {utype}: {count}")

    if project_results:
        print(f"\nProject Results:")
        print(f"  Total: {len(project_results)}")
        print(f"  Avg Deviation: {avg_deviation:.1f}%")
        print(f"  Confirmed (within 10%): {confirmed} ({100*confirmed/len(project_results):.0f}%)")

    print(f"\nLast Updated: {log.get('metadata', {}).get('last_updated', 'Never')}")


def main():
    parser = argparse.ArgumentParser(
        description='Theory Learning Loop - Enable theory catalog to learn',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --project-result PROJ001 0.35 0.42 "Savings intervention"
  %(prog)s --sync-papers
  %(prog)s --update-param MS-RD-001 lambda "1.8-2.5" "DellaVigna2018"
  %(prog)s --add-theory CAT-03 "New Theory" "Smith" 2024
  %(prog)s --history
  %(prog)s --stats
        """
    )

    parser.add_argument('--project-result', nargs=3, metavar=('ID', 'PRED', 'ACTUAL'),
                        help='Learn from project result: ID predicted actual')
    parser.add_argument('--project-notes', default='',
                        help='Notes for project result')
    parser.add_argument('--sync-papers', action='store_true',
                        help='Sync papers with theory_support to catalog')
    parser.add_argument('--update-param', nargs=4, metavar=('THEORY', 'PARAM', 'RANGE', 'SOURCE'),
                        help='Update parameter: theory_id param_name new_range source')
    parser.add_argument('--add-theory', nargs=4, metavar=('CAT', 'NAME', 'AUTHORS', 'YEAR'),
                        help='Add new theory: category_id name authors year')
    parser.add_argument('--history', action='store_true', help='Show learning history')
    parser.add_argument('--stats', action='store_true', help='Show statistics')
    parser.add_argument('--limit', type=int, default=20, help='Limit for history display')

    args = parser.parse_args()

    if args.project_result:
        project_id, predicted, actual = args.project_result
        learn_from_project(project_id, predicted, actual, args.project_notes)
    elif args.sync_papers:
        sync_papers_to_theories()
    elif args.update_param:
        theory_id, param, new_range, source = args.update_param
        update_parameter(theory_id, param, new_range, source)
    elif args.add_theory:
        cat_id, name, authors, year = args.add_theory
        add_theory(cat_id, name, authors, int(year))
    elif args.history:
        show_history(args.limit)
    elif args.stats:
        show_statistics()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
