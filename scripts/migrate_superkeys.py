#!/usr/bin/env python3
"""
Superkey Migration Script
=========================
Migrates all EBF registries to the unified superkey format per Appendix BN.

Phases:
  1. Customer Registry (CUS-) - DONE (created separately)
  2. Project references with customer context
  3. Model IDs (EBF-MOD- → MOD-)
  4. Case/Concept prefixes (CASE- → CAS-, CONC- → CON-)
  5. Formula keys (add FRM-)
  6. Output IDs (EBF-OUT- → OUT-)

Usage:
  python scripts/migrate_superkeys.py --check      # Show what would change
  python scripts/migrate_superkeys.py --migrate   # Apply migrations
  python scripts/migrate_superkeys.py --rollback  # Restore from backup

Author: EBF Team
Date: January 2026
Reference: Appendix BN REF-SUPERKEY
"""

import os
import sys
import re
import yaml
import shutil
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Any

# Configuration
DATA_DIR = Path("data")
BACKUP_DIR = Path("data/.superkey_backup")
CUSTOMER_REGISTRY = DATA_DIR / "customer-registry.yaml"

# Migration mappings
MIGRATIONS = {
    "model": {
        "file": DATA_DIR / "model-registry.yaml",
        "pattern": r"^EBF-MOD-(\d+)$",
        "replacement": r"MOD-\1",
        "id_field": "id",
        "list_key": "models",
        "special_cases": {
            "PSF-2.0": "MOD-PSF",
            "ESL-META-001": "MOD-ESL",
            "EBF-MOD-REF-001": "MOD-REF-001",
            "EBF-MOD-NEAR-001": "MOD-NEAR-001",
            "EBF-MOD-IDV-001": "MOD-IDV-001",
        }
    },
    "output": {
        "file": DATA_DIR / "output-registry.yaml",
        "pattern": r"^EBF-OUT-(\d+)$",
        "replacement": r"OUT-\1",
        "id_field": "id",
        "list_key": "outputs",
    },
    "case": {
        "file": DATA_DIR / "case-registry.yaml",
        "pattern": r"^CASE-(\d+)$",
        "replacement": r"CAS-\1",
        "id_field": None,  # Uses dict keys
        "list_key": "cases",
    },
    "concept": {
        "file": DATA_DIR / "concept-registry.yaml",
        "pattern": r"^CONC-(\d{4})-(\d+)$",
        "replacement": r"CON-\1-\2",
        "id_field": "concept_id",
        "list_key": "concepts",
    },
    "project": {
        "file": DATA_DIR / "intervention-registry.yaml",
        "pattern": r"^PRJ-(\d+)$",
        "replacement": None,  # Needs customer context
        "id_field": None,  # Uses dict keys
        "list_key": "projects",
    },
}

# Session reference pattern (for updating references in other files)
SESSION_PATTERN = r"EBF-S-(\d{4})-(\d{2})-(\d{2})-([A-Z]+)-(\d{3})"
SESSION_REPLACEMENT = r"EBF-S-\1-\2-\3-\4-\5"  # Keep format, just validate


class SuperkeyMigrator:
    """Handles migration of superkeys across all EBF registries."""

    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run
        self.changes: List[Dict[str, Any]] = []
        self.errors: List[str] = []
        self.customer_map: Dict[str, str] = {}

    def load_customer_registry(self) -> bool:
        """Load customer registry to map projects to customers."""
        if not CUSTOMER_REGISTRY.exists():
            self.errors.append(f"Customer registry not found: {CUSTOMER_REGISTRY}")
            return False

        with open(CUSTOMER_REGISTRY, 'r') as f:
            data = yaml.safe_load(f)

        for customer in data.get('customers', []):
            code = customer.get('code', '')
            cus_id = customer.get('id', '')
            if code and cus_id:
                self.customer_map[code.lower()] = cus_id

        print(f"✅ Loaded {len(self.customer_map)} customers from registry")
        return True

    def create_backup(self) -> bool:
        """Create backup of all registry files."""
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = BACKUP_DIR / timestamp
        backup_path.mkdir(exist_ok=True)

        for name, config in MIGRATIONS.items():
            src = config['file']
            if src.exists():
                dst = backup_path / src.name
                shutil.copy2(src, dst)
                print(f"📦 Backed up {src.name}")

        print(f"✅ Backup created at {backup_path}")
        return True

    def migrate_model_ids(self) -> int:
        """Phase 3: Migrate model IDs (EBF-MOD- → MOD-)."""
        config = MIGRATIONS['model']
        file_path = config['file']

        if not file_path.exists():
            self.errors.append(f"Model registry not found: {file_path}")
            return 0

        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)

        count = 0
        models = data.get(config['list_key'], [])

        for model in models:
            old_id = model.get(config['id_field'], '')
            new_id = None

            # Check special cases first
            if old_id in config.get('special_cases', {}):
                new_id = config['special_cases'][old_id]
            else:
                # Apply pattern
                match = re.match(config['pattern'], old_id)
                if match:
                    new_id = re.sub(config['pattern'], config['replacement'], old_id)

            if new_id and new_id != old_id:
                self.changes.append({
                    'type': 'model',
                    'old': old_id,
                    'new': new_id,
                    'file': str(file_path),
                })
                if not self.dry_run:
                    model[config['id_field']] = new_id
                count += 1

        if not self.dry_run and count > 0:
            with open(file_path, 'w') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

        return count

    def migrate_output_ids(self) -> int:
        """Phase 6: Migrate output IDs (EBF-OUT- → OUT-)."""
        config = MIGRATIONS['output']
        file_path = config['file']

        if not file_path.exists():
            self.errors.append(f"Output registry not found: {file_path}")
            return 0

        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)

        count = 0
        outputs = data.get(config['list_key'], [])

        for output in outputs:
            old_id = output.get(config['id_field'], '')
            match = re.match(config['pattern'], old_id)

            if match:
                new_id = re.sub(config['pattern'], config['replacement'], old_id)
                self.changes.append({
                    'type': 'output',
                    'old': old_id,
                    'new': new_id,
                    'file': str(file_path),
                })
                if not self.dry_run:
                    output[config['id_field']] = new_id
                count += 1

        if not self.dry_run and count > 0:
            with open(file_path, 'w') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

        return count

    def migrate_case_ids(self) -> int:
        """Phase 4a: Migrate case IDs (CASE- → CAS-)."""
        config = MIGRATIONS['case']
        file_path = config['file']

        if not file_path.exists():
            self.errors.append(f"Case registry not found: {file_path}")
            return 0

        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)

        count = 0
        cases = data.get(config['list_key'], {})

        if isinstance(cases, dict):
            new_cases = {}
            for old_id, case_data in cases.items():
                match = re.match(config['pattern'], old_id)
                if match:
                    new_id = re.sub(config['pattern'], config['replacement'], old_id)
                    self.changes.append({
                        'type': 'case',
                        'old': old_id,
                        'new': new_id,
                        'file': str(file_path),
                    })
                    new_cases[new_id if not self.dry_run else old_id] = case_data
                    count += 1
                else:
                    new_cases[old_id] = case_data

            if not self.dry_run and count > 0:
                data[config['list_key']] = new_cases
                with open(file_path, 'w') as f:
                    yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

        return count

    def migrate_concept_ids(self) -> int:
        """Phase 4b: Migrate concept IDs (CONC- → CON-)."""
        config = MIGRATIONS['concept']
        file_path = config['file']

        if not file_path.exists():
            self.errors.append(f"Concept registry not found: {file_path}")
            return 0

        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)

        count = 0
        concepts = data.get(config['list_key'], [])

        for concept in concepts:
            old_id = concept.get(config['id_field'], '')
            match = re.match(config['pattern'], old_id)

            if match:
                new_id = re.sub(config['pattern'], config['replacement'], old_id)
                self.changes.append({
                    'type': 'concept',
                    'old': old_id,
                    'new': new_id,
                    'file': str(file_path),
                })
                if not self.dry_run:
                    concept[config['id_field']] = new_id
                count += 1

        if not self.dry_run and count > 0:
            with open(file_path, 'w') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

        return count

    def migrate_project_ids(self) -> int:
        """Phase 2: Migrate project IDs to include customer context."""
        config = MIGRATIONS['project']
        file_path = config['file']

        if not file_path.exists():
            self.errors.append(f"Intervention registry not found: {file_path}")
            return 0

        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)

        count = 0
        projects = data.get(config['list_key'], {})

        # For projects, we need to infer customer from project metadata
        # Since we don't have customer info in current projects, we'll use UNKNOWN
        if isinstance(projects, dict):
            new_projects = {}
            for old_id, project_data in projects.items():
                match = re.match(config['pattern'], old_id)
                if match:
                    # Try to infer customer from project metadata
                    client = project_data.get('meta', {}).get('client', '')
                    customer_code = self._infer_customer_code(client)

                    if customer_code:
                        new_id = f"CUS-{customer_code}-{old_id}"
                    else:
                        new_id = f"CUS-UNKNOWN-{old_id}"

                    self.changes.append({
                        'type': 'project',
                        'old': old_id,
                        'new': new_id,
                        'file': str(file_path),
                        'note': f"Customer: {customer_code or 'UNKNOWN'}",
                    })
                    new_projects[new_id if not self.dry_run else old_id] = project_data
                    count += 1
                else:
                    new_projects[old_id] = project_data

            if not self.dry_run and count > 0:
                data[config['list_key']] = new_projects
                with open(file_path, 'w') as f:
                    yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

        return count

    def _infer_customer_code(self, client_name: str) -> str:
        """Try to infer customer code from client name."""
        if not client_name:
            return ""

        client_lower = client_name.lower()

        # Check against known customers
        for code, cus_id in self.customer_map.items():
            if code in client_lower:
                return code.upper()

        return ""

    def add_formula_keys(self) -> int:
        """Phase 5: Add FRM- keys to formula registry."""
        file_path = DATA_DIR / "formula-registry.yaml"

        if not file_path.exists():
            self.errors.append(f"Formula registry not found: {file_path}")
            return 0

        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)

        count = 0
        formulas = data.get('formulas', [])

        if isinstance(formulas, list):
            for i, formula in enumerate(formulas):
                if 'id' not in formula:
                    new_id = f"FRM-{str(i+1).zfill(3)}"
                    self.changes.append({
                        'type': 'formula',
                        'old': '(none)',
                        'new': new_id,
                        'file': str(file_path),
                    })
                    if not self.dry_run:
                        formula['id'] = new_id
                    count += 1

        if not self.dry_run and count > 0:
            with open(file_path, 'w') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

        return count

    def update_cross_references(self) -> int:
        """Update all cross-references in related files."""
        count = 0

        # Build old→new mapping
        mapping = {c['old']: c['new'] for c in self.changes if c['old'] != '(none)'}

        if not mapping:
            return 0

        # Files that might contain references
        ref_files = [
            DATA_DIR / "model-building-session.yaml",
            DATA_DIR / "output-registry.yaml",
            DATA_DIR / "intervention-registry.yaml",
        ]

        for file_path in ref_files:
            if not file_path.exists():
                continue

            with open(file_path, 'r') as f:
                content = f.read()

            original = content
            for old, new in mapping.items():
                if old in content:
                    content = content.replace(old, new)
                    count += 1

            if content != original and not self.dry_run:
                with open(file_path, 'w') as f:
                    f.write(content)

        return count

    def run_check(self) -> None:
        """Show what would change without applying."""
        print("\n" + "="*70)
        print("SUPERKEY MIGRATION CHECK")
        print("="*70 + "\n")

        self.load_customer_registry()

        # Run all migrations in dry-run mode
        totals = {
            'model': self.migrate_model_ids(),
            'output': self.migrate_output_ids(),
            'case': self.migrate_case_ids(),
            'concept': self.migrate_concept_ids(),
            'project': self.migrate_project_ids(),
            'formula': self.add_formula_keys(),
        }

        # Print changes by type
        for entity_type in ['model', 'output', 'case', 'concept', 'project', 'formula']:
            changes = [c for c in self.changes if c['type'] == entity_type]
            if changes:
                print(f"\n📦 {entity_type.upper()} ({len(changes)} changes):")
                print("-" * 50)
                for c in changes:
                    note = f" ({c['note']})" if 'note' in c else ""
                    print(f"  {c['old']:30} → {c['new']}{note}")

        # Summary
        print("\n" + "="*70)
        print("SUMMARY")
        print("="*70)
        total = sum(totals.values())
        print(f"\nTotal changes: {total}")
        for entity, count in totals.items():
            status = "✅" if count > 0 else "⏭️"
            print(f"  {status} {entity}: {count}")

        if self.errors:
            print(f"\n⚠️ Errors: {len(self.errors)}")
            for e in self.errors:
                print(f"  ❌ {e}")

        print("\n" + "-"*70)
        print("Run with --migrate to apply these changes")
        print("-"*70 + "\n")

    def run_migrate(self) -> None:
        """Apply all migrations."""
        print("\n" + "="*70)
        print("SUPERKEY MIGRATION")
        print("="*70 + "\n")

        # Create backup first
        print("📦 Creating backup...")
        self.create_backup()

        self.load_customer_registry()
        self.dry_run = False

        # Run all migrations
        print("\n🔄 Running migrations...")
        totals = {
            'model': self.migrate_model_ids(),
            'output': self.migrate_output_ids(),
            'case': self.migrate_case_ids(),
            'concept': self.migrate_concept_ids(),
            'project': self.migrate_project_ids(),
            'formula': self.add_formula_keys(),
        }

        # Update cross-references
        print("\n🔗 Updating cross-references...")
        ref_count = self.update_cross_references()

        # Summary
        print("\n" + "="*70)
        print("MIGRATION COMPLETE")
        print("="*70)
        total = sum(totals.values())
        print(f"\nTotal changes: {total}")
        for entity, count in totals.items():
            status = "✅" if count > 0 else "⏭️"
            print(f"  {status} {entity}: {count}")
        print(f"  🔗 cross-references: {ref_count}")

        if self.errors:
            print(f"\n⚠️ Errors: {len(self.errors)}")
            for e in self.errors:
                print(f"  ❌ {e}")

        print("\n" + "-"*70)
        print(f"Backup stored in: {BACKUP_DIR}")
        print("Run with --rollback to restore if needed")
        print("-"*70 + "\n")

    def run_rollback(self) -> None:
        """Restore from most recent backup."""
        if not BACKUP_DIR.exists():
            print("❌ No backup directory found")
            return

        # Find most recent backup
        backups = sorted(BACKUP_DIR.iterdir(), reverse=True)
        if not backups:
            print("❌ No backups found")
            return

        latest = backups[0]
        print(f"\n📦 Restoring from: {latest}")

        for backup_file in latest.iterdir():
            dst = DATA_DIR / backup_file.name
            shutil.copy2(backup_file, dst)
            print(f"  ✅ Restored {backup_file.name}")

        print("\n✅ Rollback complete")


def main():
    parser = argparse.ArgumentParser(
        description="Migrate EBF registries to unified superkey format"
    )
    parser.add_argument('--check', action='store_true',
                       help='Show what would change (dry run)')
    parser.add_argument('--migrate', action='store_true',
                       help='Apply migrations')
    parser.add_argument('--rollback', action='store_true',
                       help='Restore from most recent backup')

    args = parser.parse_args()

    if not any([args.check, args.migrate, args.rollback]):
        args.check = True  # Default to check mode

    migrator = SuperkeyMigrator(dry_run=True)

    if args.check:
        migrator.run_check()
    elif args.migrate:
        migrator.run_migrate()
    elif args.rollback:
        migrator.run_rollback()


if __name__ == '__main__':
    main()
