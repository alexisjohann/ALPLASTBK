#!/usr/bin/env python3
"""
EBF Unified Registry CLI
========================

Single entry point for ALL registry operations.
This is the RECOMMENDED way to interact with EBF registries.

USAGE:
    # Interactive mode (guided)
    python scripts/registry.py

    # Add new case (auto-ID)
    python scripts/registry.py add case --name "My Case" --domain finance,behavior

    # Add new parameter
    python scripts/registry.py add parameter --prefix BEH --name "Loss Aversion"

    # Get next available ID
    python scripts/registry.py next case
    python scripts/registry.py next theory --prefix CM

    # Check status
    python scripts/registry.py status

    # Validate all registries
    python scripts/registry.py validate

PHILOSOPHY:
    Manual YAML editing is error-prone and leads to:
    - Duplicate IDs
    - Merge conflicts
    - Inconsistent formatting

    This CLI ensures:
    - Unique IDs (auto-generated)
    - Consistent formatting
    - Automatic backups
    - Validation before write

Author: EBF Framework
Version: 1.0
"""

import sys
import argparse
import yaml
from pathlib import Path
from datetime import datetime

# Import registry manager
sys.path.insert(0, str(Path(__file__).parent))
from registry_manager import (
    CaseRegistry,
    TheoryCategoryRegistry,
    TheoryModelRegistry,
    ParameterRegistry,
    ModelRegistry,
    OutputRegistry,
    SkillRegistry,
    ForecastRegistry,
    SessionRegistry,
    InterventionRegistry,
    ResearcherRegistry,
    FormulaRegistry,
    get_registry,
    DuplicateIDError,
    InvalidIDError,
)


def cmd_status(args):
    """Show status of all registries."""
    print("=" * 70)
    print("EBF REGISTRY STATUS")
    print("=" * 70)

    registries = [
        ('Case', CaseRegistry()),
        ('Category', TheoryCategoryRegistry()),
        ('Theory', TheoryModelRegistry()),
        ('Parameter', ParameterRegistry()),
        ('Model', ModelRegistry()),
        ('Output', OutputRegistry()),
        ('Skill', SkillRegistry()),
        ('Forecast', ForecastRegistry()),
        ('Session', SessionRegistry()),
        ('Intervention', InterventionRegistry()),
        ('Researcher', ResearcherRegistry()),
        ('Formula', FormulaRegistry()),
    ]

    for name, reg in registries:
        print(f"\n📁 {name} Registry:")
        try:
            status = reg.status()
            if 'count' in status:
                print(f"   Count: {status['count']}")
                print(f"   Highest: {status['highest']}")
                print(f"   Next: {status['next_available']}")
            elif 'prefixes' in status:
                total_key = [k for k in status.keys() if k.startswith('total_')][0] if any(k.startswith('total_') for k in status.keys()) else None
                total = status.get(total_key, 0) if total_key else 0
                print(f"   Total: {total}")
                for prefix, info in list(status['prefixes'].items())[:5]:
                    print(f"     {prefix}: {info['count']} entries, next = {info['next']}")
                if len(status['prefixes']) > 5:
                    print(f"     ... and {len(status['prefixes']) - 5} more")
            elif 'domains' in status:
                total_key = [k for k in status.keys() if k.startswith('total_')][0] if any(k.startswith('total_') for k in status.keys()) else None
                total = status.get(total_key, 0) if total_key else 0
                print(f"   Total: {total}")
                for domain, info in list(status['domains'].items())[:5]:
                    if isinstance(info, dict):
                        count = info.get('count', info.get('total', 0))
                        print(f"     {domain}: {count} entries")
            elif 'total_researchers' in status:
                print(f"   Total: {status['total_researchers']}")
            elif 'next_for_today' in status:
                print(f"   Total: {status.get('total_sessions', 0)}")
                print(f"   Next today: {status['next_for_today']}")

            dups = status.get('duplicates', reg.validate_all())
            if dups:
                print(f"   ⚠️  DUPLICATES: {dups}")
            else:
                print(f"   ✅ No duplicates")
        except Exception as e:
            print(f"   Error: {e}")

    print()
    return 0


def cmd_next(args):
    """Get next available ID."""
    reg_type = args.registry
    prefix = args.prefix

    try:
        reg = get_registry(reg_type)
        next_id = reg.next_id(prefix)
        print(next_id)
        return 0
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def cmd_add(args):
    """Add new entry to registry."""
    reg_type = args.registry
    prefix = getattr(args, 'prefix', None)

    try:
        reg = get_registry(reg_type)

        # Build entry from args
        entry = {}

        if hasattr(args, 'name') and args.name:
            entry['name'] = args.name

        if hasattr(args, 'title') and args.title:
            entry['title'] = args.title

        if hasattr(args, 'domain') and args.domain:
            entry['domain'] = [d.strip() for d in args.domain.split(',')]

        if hasattr(args, 'description') and args.description:
            entry['description'] = args.description

        # Add metadata
        entry['created'] = datetime.now().strftime('%Y-%m-%d')
        entry['created_by'] = 'registry.py'

        # Add 10C placeholder for cases
        if reg_type in ['case', 'cas']:
            if '10C' not in entry:
                entry['10C'] = {
                    'WHO': {'levels': ['individual'], 'heterogeneity': 'medium'},
                    'WHAT': {'dimensions': ['F', 'E'], 'primary': 'decision'},
                    'HOW': {'gamma_avg': 0.0, 'interaction': 'additive'},
                    'WHEN': {'psi_dominant': 'context', 'temporal': 'point'},
                    'WHERE': {'source': 'empirical', 'confidence': 'medium'},
                    'AWARE': {'A_level': 0.5, 'awareness_type': 'partial'},
                    'READY': {'W_level': 0.5, 'theta': 0.5},
                    'STAGE': {'phase': 'decision', 'stability': 'stable'},
                    'HIERARCHY': {'primary_level': 'L1', 'intervention_type': 'nudge'},
                }

        # Confirm with user
        print("\nEntry to add:")
        print(yaml.dump(entry, default_flow_style=False, allow_unicode=True))

        if not args.yes:
            confirm = input("\nProceed? [y/N]: ").strip().lower()
            if confirm != 'y':
                print("Cancelled.")
                return 1

        # Add entry
        new_id = reg.add(entry, prefix=prefix)
        print(f"\n✅ Created: {new_id}")
        return 0

    except (DuplicateIDError, InvalidIDError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except NotImplementedError as e:
        print(f"Note: {e}", file=sys.stderr)
        return 1


def cmd_validate(args):
    """Validate all registries for duplicates."""
    print("Validating all registries...\n")

    all_ok = True
    all_registries = [
        ('Case', CaseRegistry),
        ('Category', TheoryCategoryRegistry),
        ('Theory', TheoryModelRegistry),
        ('Parameter', ParameterRegistry),
        ('Model', ModelRegistry),
        ('Output', OutputRegistry),
        ('Skill', SkillRegistry),
        ('Forecast', ForecastRegistry),
        ('Session', SessionRegistry),
        ('Intervention', InterventionRegistry),
        ('Researcher', ResearcherRegistry),
        ('Formula', FormulaRegistry),
    ]
    for name, cls in all_registries:
        try:
            reg = cls()
            dups = reg.validate_all()
            if dups:
                print(f"❌ {name}: DUPLICATES FOUND - {dups}")
                all_ok = False
            else:
                print(f"✅ {name}: OK")
        except Exception as e:
            print(f"⚠️  {name}: Error - {e}")

    print()
    if all_ok:
        print("All registries valid!")
        return 0
    else:
        print("Some registries have issues!")
        return 1


def cmd_interactive(args):
    """Interactive mode for adding entries."""
    print("=" * 60)
    print("EBF REGISTRY - Interactive Mode")
    print("=" * 60)
    print()

    # Choose registry
    print("Which registry?")
    print("  1. Case Registry (CAS-XXX)")
    print("  2. Category Registry (CAT-XX)")
    print("  3. Theory Registry (MS-XX-XXX)")
    print("  4. Parameter Registry (PAR-XX-XXX)")
    print("  5. Show Status")
    print("  6. Exit")
    print()

    choice = input("Choice [1-6]: ").strip()

    if choice == '1':
        return add_case_interactive()
    elif choice == '2':
        print("\nCategories require manual integration.")
        reg = TheoryCategoryRegistry()
        print(f"Next available: {reg.next_id()}")
        return 0
    elif choice == '3':
        return add_theory_interactive()
    elif choice == '4':
        return add_parameter_interactive()
    elif choice == '5':
        return cmd_status(args)
    elif choice == '6':
        return 0
    else:
        print("Invalid choice")
        return 1


def add_case_interactive():
    """Interactive case addition."""
    print("\n--- Add New Case ---\n")

    name = input("Case name: ").strip()
    if not name:
        print("Name required!")
        return 1

    domain_str = input("Domains (comma-separated, e.g., finance,behavior): ").strip()
    domains = [d.strip() for d in domain_str.split(',')] if domain_str else ['general']

    description = input("Description (optional): ").strip()

    entry = {
        'name': name,
        'domain': domains,
        'created': datetime.now().strftime('%Y-%m-%d'),
        '10C': {
            'WHO': {'levels': ['individual'], 'heterogeneity': 'medium'},
            'WHAT': {'dimensions': ['F', 'E'], 'primary': 'decision'},
            'HOW': {'gamma_avg': 0.0},
            'WHEN': {'psi_dominant': 'context'},
            'WHERE': {'source': 'empirical', 'confidence': 'medium'},
            'AWARE': {'A_level': 0.5},
            'READY': {'W_level': 0.5},
            'STAGE': {'phase': 'decision'},
            'HIERARCHY': {'primary_level': 'L1'},
        }
    }

    if description:
        entry['description'] = description

    print("\nEntry preview:")
    print(yaml.dump(entry, default_flow_style=False, allow_unicode=True))

    confirm = input("\nAdd this case? [y/N]: ").strip().lower()
    if confirm != 'y':
        print("Cancelled.")
        return 1

    reg = CaseRegistry()
    new_id = reg.add(entry)
    print(f"\n✅ Created: {new_id}")
    return 0


def add_theory_interactive():
    """Interactive theory addition."""
    print("\n--- Add New Theory ---\n")

    prefix = input("Prefix (e.g., CM, SP, RD): ").strip().upper()
    if not prefix:
        print("Prefix required!")
        return 1

    reg = TheoryModelRegistry()
    next_id = reg.next_id(prefix)
    print(f"\nNext available: {next_id}")
    print("Theories require manual integration into theory-catalog.yaml")
    print(f"Use ID: {next_id}")
    return 0


def add_parameter_interactive():
    """Interactive parameter addition."""
    print("\n--- Add New Parameter ---\n")

    prefix = input("Prefix (e.g., BEH, CM, COMP): ").strip().upper()
    if not prefix:
        print("Prefix required!")
        return 1

    reg = ParameterRegistry()
    next_id = reg.next_id(prefix)

    name = input("Parameter name: ").strip()
    symbol = input("Symbol (e.g., λ, β, γ): ").strip()
    description = input("Description: ").strip()

    entry = {
        'name': name,
        'symbol': symbol,
        'description': description,
        'domain': prefix.lower(),
        'created': datetime.now().strftime('%Y-%m-%d'),
    }

    print("\nEntry preview:")
    print(yaml.dump(entry, default_flow_style=False, allow_unicode=True))

    confirm = input("\nAdd this parameter? [y/N]: ").strip().lower()
    if confirm != 'y':
        print("Cancelled.")
        return 1

    new_id = reg.add(entry, prefix=prefix)
    print(f"\n✅ Created: {new_id}")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description='EBF Unified Registry CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Status command
    status_parser = subparsers.add_parser('status', help='Show registry status')

    # Next command
    next_parser = subparsers.add_parser('next', help='Get next available ID')
    next_parser.add_argument('registry', choices=['case', 'category', 'theory', 'parameter',
                                                   'model', 'output', 'skill', 'forecast',
                                                   'session', 'intervention', 'researcher', 'formula'])
    next_parser.add_argument('--prefix', help='Prefix for prefixed IDs (e.g., CM, BEH, PRJ)')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add new entry')
    add_parser.add_argument('registry', choices=['case', 'category', 'theory', 'parameter',
                                                  'model', 'output', 'skill', 'forecast',
                                                  'session', 'intervention', 'researcher', 'formula'])
    add_parser.add_argument('--name', help='Entry name')
    add_parser.add_argument('--title', help='Entry title')
    add_parser.add_argument('--domain', help='Domains (comma-separated)')
    add_parser.add_argument('--description', help='Description')
    add_parser.add_argument('--prefix', help='Prefix for MS/PAR')
    add_parser.add_argument('-y', '--yes', action='store_true', help='Skip confirmation')

    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate all registries')

    args = parser.parse_args()

    if args.command == 'status':
        return cmd_status(args)
    elif args.command == 'next':
        return cmd_next(args)
    elif args.command == 'add':
        return cmd_add(args)
    elif args.command == 'validate':
        return cmd_validate(args)
    else:
        # No command - interactive mode
        return cmd_interactive(args)


if __name__ == '__main__':
    sys.exit(main())
