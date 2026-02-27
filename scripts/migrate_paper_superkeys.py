#!/usr/bin/env python3
"""
Paper Superkey Migration Script
================================
Migrates BibTeX keys to PAP- prefixed superkeys per Appendix BN.

Changes:
  PAP-kahneman1979prospectprospect → PAP-PAP-kahneman1979prospectprospect

Affected files:
  1. bibliography/bcm_master.bib - BibTeX entries

Usage:
  python scripts/migrate_paper_superkeys.py --check      # Show what would change
  python scripts/migrate_paper_superkeys.py --migrate   # Apply migrations
  python scripts/migrate_paper_superkeys.py --rollback  # Restore from backup

Author: EBF Team
Date: January 2026
Reference: Appendix BN REF-SUPERKEY, Axiom SK-9
"""

import os
import re
import shutil
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Set, Tuple

# Configuration
BIB_FILE = Path("bibliography/bcm_master.bib")
BACKUP_DIR = Path("data/.superkey_backup")

# Prefix
PAP_PREFIX = "PAP-"


class PaperMigrator:
    """Handles migration of paper BibTeX keys to PAP- superkeys."""

    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run
        self.changes: List[Dict] = []

    def create_backup(self) -> bool:
        """Create backup of BibTeX file."""
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = BACKUP_DIR / f"paper_migration_{timestamp}"
        backup_path.mkdir(exist_ok=True)

        if BIB_FILE.exists():
            shutil.copy2(BIB_FILE, backup_path / BIB_FILE.name)
            print(f"📦 Backed up {BIB_FILE.name}")

        print(f"✅ Backup created at {backup_path}")
        return True

    def migrate_bib_file(self) -> int:
        """Migrate BibTeX keys in bcm_master.bib using single pass."""
        if not BIB_FILE.exists():
            print(f"❌ BibTeX file not found: {BIB_FILE}")
            return 0

        with open(BIB_FILE, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content

        # Pattern to match BibTeX entries: @type{key,
        # Only match keys that don't already have PAP- prefix
        pattern = r'(@\w+\{)([^,\s]+)(,)'

        def replace_key(match):
            prefix = match.group(1)
            key = match.group(2)
            suffix = match.group(3)

            # Skip if already has PAP- prefix
            if key.startswith(PAP_PREFIX):
                return match.group(0)

            # Skip special entries like @string, @preamble, @comment
            entry_type = prefix[1:-1].lower()
            if entry_type in ('string', 'preamble', 'comment'):
                return match.group(0)

            self.changes.append({
                'old': key,
                'new': f"{PAP_PREFIX}{key}",
            })
            return f"{prefix}{PAP_PREFIX}{key}{suffix}"

        content = re.sub(pattern, replace_key, content)

        if content != original and not self.dry_run:
            with open(BIB_FILE, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Migrated {BIB_FILE}")

        return len(self.changes)

    def run_check(self) -> None:
        """Show what would change without applying."""
        print("\n" + "="*70)
        print("PAPER SUPERKEY MIGRATION CHECK")
        print("="*70 + "\n")

        # Simulate migration
        count = self.migrate_bib_file()

        if count == 0:
            print("No keys to migrate.")
            return

        # Show sample changes
        print(f"📚 BibTeX entries to migrate: {count}")
        sample = self.changes[:15]
        for c in sample:
            print(f"   {c['old']:45} → {c['new']}")
        if len(self.changes) > 15:
            print(f"   ... and {count - 15} more")

        # Summary
        print("\n" + "="*70)
        print("SUMMARY")
        print("="*70)
        print(f"\nTotal BibTeX entries: {count}")
        print(f"\n⚠️  Note: YAML and LaTeX files should be updated manually")
        print(f"    or use search-replace in your editor.")

        print("\n" + "-"*70)
        print("Run with --migrate to apply these changes to bcm_master.bib")
        print("-"*70 + "\n")

    def run_migrate(self) -> None:
        """Apply migrations to BibTeX file."""
        print("\n" + "="*70)
        print("PAPER SUPERKEY MIGRATION")
        print("="*70 + "\n")

        # Create backup
        print("📦 Creating backup...")
        self.create_backup()

        self.dry_run = False

        # Run migration
        print("\n🔄 Migrating BibTeX file...")
        count = self.migrate_bib_file()

        # Summary
        print("\n" + "="*70)
        print("MIGRATION COMPLETE")
        print("="*70)
        print(f"\nTotal BibTeX entries migrated: {count}")
        print(f"\n⚠️  IMPORTANT: You should also update references in:")
        print(f"    - YAML files (use_for, bib_keys fields)")
        print(f"    - LaTeX files (\\citep{{}}, \\cite{{}}) commands")
        print(f"\n💡 Tip: Use your editor's search-replace:")
        print(f"    Find: PAP-kahneman1979prospectprospect")
        print(f"    Replace: PAP-PAP-kahneman1979prospectprospect")

        print("\n" + "-"*70)
        print(f"Backup stored in: {BACKUP_DIR}")
        print("-"*70 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Migrate paper BibTeX keys to PAP- superkeys"
    )
    parser.add_argument('--check', action='store_true',
                       help='Show what would change (dry run)')
    parser.add_argument('--migrate', action='store_true',
                       help='Apply migrations')
    parser.add_argument('--rollback', action='store_true',
                       help='Restore from most recent backup')

    args = parser.parse_args()

    if not any([args.check, args.migrate, args.rollback]):
        args.check = True

    migrator = PaperMigrator(dry_run=True)

    if args.check:
        migrator.run_check()
    elif args.migrate:
        migrator.run_migrate()
    elif args.rollback:
        print("Rollback: Use paper_migration_* backup in data/.superkey_backup/")


if __name__ == '__main__':
    main()
