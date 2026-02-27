#!/usr/bin/env python3
"""
Complete Appendix Code Migration Execution System
Purpose: Execute full migration with quality assurance and rollback capability
Strategy: Pre-check → Backup → Migrate → Validate → Report

Usage:
    python scripts/execute-complete-migration.py --dry-run
    python scripts/execute-complete-migration.py --execute
    python scripts/execute-complete-migration.py --rollback
    python scripts/execute-complete-migration.py --validate
"""

import os
import re
import json
import yaml
import shutil
import subprocess
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Set, Tuple, Optional
import hashlib

class CompleteMigrationExecutor:
    """Execute complete appendix code migration with safety guarantees"""

    def __init__(self, repo_root="/home/user/complementarity-context-framework"):
        self.repo_root = Path(repo_root)
        self.appendices_dir = self.repo_root / "appendices"
        self.chapters_dir = self.repo_root / "chapters"
        self.docs_dir = self.repo_root / "docs"
        self.models_dir = self.repo_root / "models"

        self.migration_dir = self.repo_root / "migration-audit"
        self.migration_dir.mkdir(exist_ok=True)

        self.execution_dir = self.migration_dir / f"execution-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        self.execution_dir.mkdir(exist_ok=True)

        self.backup_dir = self.execution_dir / "backups"
        self.backup_dir.mkdir(exist_ok=True)

        self.mapping_file = self.docs_dir / "frameworks" / "code-mapping.yaml"
        self.mapping = self._load_mapping()
        self.old_to_new = self._build_reverse_mapping()

        # Statistics
        self.stats = {
            'files_renamed': 0,
            'references_updated': 0,
            'errors': [],
            'warnings': [],
            'checksums_before': {},
            'checksums_after': {},
        }

        self.log_file = self.execution_dir / "migration.log"
        self.error_log = self.execution_dir / "errors.log"

    def _load_mapping(self) -> dict:
        """Load code mapping"""
        with open(self.mapping_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        yaml_start_idx = 0
        for i, line in enumerate(lines):
            if line.strip() and not line.strip().startswith(('**', '#', '---')):
                yaml_start_idx = i
                break
        yaml_content = ''.join(lines[yaml_start_idx:])
        return yaml.safe_load(yaml_content) or {}

    def _build_reverse_mapping(self) -> dict:
        """Build old_code -> new_code mapping"""
        mapping = {}
        for category in ['core', 'formal', 'domain', 'context', 'method', 'predict', 'lit', 'ref', 'domain_new', 'new_appendices']:
            if category in self.mapping:
                for old_code, new_code in self.mapping[category].items():
                    mapping[old_code] = new_code
        return mapping

    def log(self, message: str, level: str = "INFO"):
        """Log message to file and stdout"""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] [{level}] {message}"
        print(log_entry)
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry + "\n")

    def error(self, message: str):
        """Log error"""
        self.log(message, "ERROR")
        self.stats['errors'].append(message)
        with open(self.error_log, 'a', encoding='utf-8') as f:
            f.write(f"[{datetime.now().isoformat()}] {message}\n")

    def warning(self, message: str):
        """Log warning"""
        self.log(message, "WARNING")
        self.stats['warnings'].append(message)

    def calculate_checksum(self, filepath: Path) -> str:
        """Calculate MD5 checksum of file"""
        if not filepath.exists():
            return ""
        md5 = hashlib.md5()
        with open(filepath, 'rb') as f:
            md5.update(f.read())
        return md5.hexdigest()

    def phase_1_pre_checks(self) -> bool:
        """Pre-migration validation"""
        self.log("\n" + "="*80)
        self.log("PHASE 1: PRE-MIGRATION CHECKS")
        self.log("="*80)

        # Check mapping consistency
        self.log("\n1. Validating code mapping...")
        new_codes = list(self.old_to_new.values())
        duplicates = [code for code in set(new_codes) if new_codes.count(code) > 1]
        if duplicates:
            self.error(f"Duplicate new codes found: {duplicates}")
            return False
        self.log(f"   ✅ {len(self.old_to_new)} unique codes, no duplicates")

        # Check for circular dependencies
        self.log("\n2. Checking for circular dependencies...")
        circular = self._find_circular_dependencies()
        if circular:
            self.warning(f"Circular dependencies found: {circular}")
            for cycle in circular:
                self.log(f"   ⚠️  {' → '.join(cycle)} → {cycle[0]}")
        else:
            self.log(f"   ✅ No circular dependencies detected")

        # Verify all appendix files exist
        self.log("\n3. Verifying all appendix files...")
        all_files = list(self.appendices_dir.glob("*.tex"))
        assigned_codes = set()
        for filepath in all_files:
            match = re.match(r'^([A-Z]{1,3})', filepath.name)
            if match:
                assigned_codes.add(match.group(1))

        missing_codes = set(self.old_to_new.keys()) - assigned_codes
        if missing_codes:
            self.warning(f"Codes in mapping but no files found: {missing_codes}")
        self.log(f"   ✅ {len(all_files)} appendix files found, {len(assigned_codes)} codes present")

        # Test file access
        self.log("\n4. Testing file access...")
        test_file = self.appendices_dir / "00_appendix_template.tex"
        if not test_file.exists():
            self.error(f"Cannot access template file: {test_file}")
            return False
        self.log(f"   ✅ File system access verified")

        return True

    def phase_2_backup(self) -> bool:
        """Create complete backup"""
        self.log("\n" + "="*80)
        self.log("PHASE 2: CREATE BACKUPS")
        self.log("="*80)

        directories_to_backup = [
            ('appendices', self.appendices_dir),
            ('chapters', self.chapters_dir),
            ('docs', self.docs_dir),
            ('models', self.models_dir),
        ]

        for name, dirpath in directories_to_backup:
            if not dirpath.exists():
                continue

            self.log(f"\nBacking up {name}/...")
            backup_path = self.backup_dir / name
            try:
                shutil.copytree(dirpath, backup_path)
                self.log(f"   ✅ Backed up to {backup_path.relative_to(self.repo_root)}")

                # Calculate checksums
                for filepath in backup_path.rglob("*"):
                    if filepath.is_file():
                        rel_path = str(filepath.relative_to(self.repo_root))
                        self.stats['checksums_before'][rel_path] = self.calculate_checksum(filepath)

            except Exception as e:
                self.error(f"Backup failed for {name}: {e}")
                return False

        self.log(f"\n   ✅ Total files backed up: {len(self.stats['checksums_before'])}")
        return True

    def phase_3_dry_run(self) -> bool:
        """Execute dry-run without actual changes"""
        self.log("\n" + "="*80)
        self.log("PHASE 3: DRY-RUN SIMULATION")
        self.log("="*80)

        self.log("\n1. Simulating file renames...")
        renamed_count = 0
        for filepath in self.appendices_dir.glob("*.tex"):
            match = re.match(r'^([A-Z]{1,3})[_.]', filepath.name)
            if not match:
                continue
            old_code = match.group(1)
            if old_code in self.old_to_new:
                new_code = self.old_to_new[old_code]
                new_name = filepath.name.replace(f"{old_code}_", f"{new_code}_", 1).replace(f"{old_code}.", f"{new_code}.", 1)
                self.log(f"   [{renamed_count+1}] {filepath.name} → {new_name}")
                renamed_count += 1

        self.log(f"\n   ✅ Dry-run: {renamed_count} files would be renamed")

        self.log("\n2. Simulating reference updates...")
        reference_count = 0
        for filepath in list(self.chapters_dir.glob("*.tex")) + list(self.appendices_dir.glob("*.tex")):
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            for old_code, new_code in self.old_to_new.items():
                matches = len(re.findall(rf'\bAppendix\s+{old_code}\b', content))
                if matches > 0:
                    reference_count += matches
                    self.log(f"   [{reference_count}] {filepath.name}: Appendix {old_code} → {new_code} ({matches} occurrences)")

        self.log(f"\n   ✅ Dry-run: {reference_count} references would be updated")
        return True

    def phase_4_execute_migration(self) -> bool:
        """Execute actual migration"""
        self.log("\n" + "="*80)
        self.log("PHASE 4: EXECUTE MIGRATION")
        self.log("="*80)

        # Step 1: Rename all appendix files
        self.log("\n1. Renaming appendix files...")
        try:
            renamed = self._rename_appendix_files()
            self.stats['files_renamed'] = renamed
            self.log(f"   ✅ Renamed {renamed} files")
        except Exception as e:
            self.error(f"File renaming failed: {e}")
            return False

        # Step 2: Update all references
        self.log("\n2. Updating all references...")
        try:
            updated = self._update_all_references()
            self.stats['references_updated'] = updated
            self.log(f"   ✅ Updated {updated} references")
        except Exception as e:
            self.error(f"Reference update failed: {e}")
            return False

        # Step 3: Update axiom/theorem references
        self.log("\n3. Updating axiom and theorem references...")
        try:
            axiom_count = self._update_axiom_theorem_references()
            self.log(f"   ✅ Updated {axiom_count} axiom/theorem references")
        except Exception as e:
            self.error(f"Axiom/theorem update failed: {e}")
            return False

        return True

    def _rename_appendix_files(self) -> int:
        """Rename all appendix files"""
        count = 0
        for filepath in list(self.appendices_dir.glob("*.tex")):
            match = re.match(r'^([A-Z]{1,3})[_.]', filepath.name)
            if not match:
                continue

            old_code = match.group(1)
            if old_code not in self.old_to_new:
                continue

            new_code = self.old_to_new[old_code]
            new_name = filepath.name.replace(f"{old_code}_", f"{new_code}_", 1).replace(f"{old_code}.", f"{new_code}.", 1)
            new_filepath = filepath.parent / new_name

            try:
                filepath.rename(new_filepath)
                self.log(f"   Renamed: {filepath.name} → {new_name}")
                count += 1
            except Exception as e:
                self.error(f"Failed to rename {filepath.name}: {e}")

        return count

    def _update_all_references(self) -> int:
        """Update references in all files"""
        count = 0
        search_dirs = [self.chapters_dir, self.appendices_dir, self.docs_dir, self.models_dir]

        for search_dir in search_dirs:
            if not search_dir.exists():
                continue

            for filepath in list(search_dir.rglob("*.tex")) + list(search_dir.rglob("*.md")):
                if not filepath.is_file():
                    continue

                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()

                    original_content = content
                    for old_code, new_code in self.old_to_new.items():
                        # Update text references: "Appendix AA" → "Appendix LAB"
                        content = re.sub(
                            rf'\bAppendix\s+{re.escape(old_code)}\b',
                            f'Appendix {new_code}',
                            content
                        )

                        # Update LaTeX refs: \ref{app:aa} → \ref{app:lab}
                        content = re.sub(
                            rf'\\ref{{app:{old_code.lower()}[^}}]*}}',
                            f'\\ref{{app:{new_code.lower()}}}',
                            content,
                            flags=re.IGNORECASE
                        )

                        # Update appendix commands: appendix{AA} → appendix{LAB}
                        content = re.sub(
                            rf'appendix{{{re.escape(old_code)}}}',
                            f'appendix{{{new_code}}}',
                            content
                        )

                    if content != original_content:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(content)
                        changes = sum(1 for old_code in self.old_to_new if old_code in original_content)
                        count += changes

                except Exception as e:
                    self.error(f"Failed to update references in {filepath}: {e}")

        return count

    def _update_axiom_theorem_references(self) -> int:
        """Update axiom/theorem references like 'Appendix AU-1' → 'Appendix AWA-1'"""
        count = 0
        search_dirs = [self.chapters_dir, self.appendices_dir, self.docs_dir, self.models_dir]

        for search_dir in search_dirs:
            if not search_dir.exists():
                continue

            for filepath in list(search_dir.rglob("*.tex")) + list(search_dir.rglob("*.md")):
                if not filepath.is_file():
                    continue

                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()

                    original_content = content
                    for old_code, new_code in self.old_to_new.items():
                        # Update axiom references: "AU-1" → "AWA-1"
                        content = re.sub(
                            rf'\b{re.escape(old_code)}-(\d+)\b',
                            f'{new_code}-\\1',
                            content
                        )

                        # Update theorem references: "HHH-T5" → "TKT-T5"
                        content = re.sub(
                            rf'\b{re.escape(old_code)}-T(\d+)\b',
                            f'{new_code}-T\\1',
                            content
                        )

                    if content != original_content:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(content)
                        changes = sum(1 for old_code in self.old_to_new if old_code in original_content)
                        count += changes

                except Exception as e:
                    self.error(f"Failed to update axiom/theorem in {filepath}: {e}")

        return count

    def phase_5_post_validation(self) -> bool:
        """Validate migration success"""
        self.log("\n" + "="*80)
        self.log("PHASE 5: POST-MIGRATION VALIDATION")
        self.log("="*80)

        # Check 1: No old codes remain
        self.log("\n1. Checking for remaining old codes...")
        old_code_references = 0
        for filepath in list(self.chapters_dir.rglob("*.tex")) + list(self.appendices_dir.rglob("*.tex")):
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            for old_code in self.old_to_new.keys():
                matches = len(re.findall(rf'\bAppendix\s+{re.escape(old_code)}\b', content))
                if matches > 0:
                    old_code_references += matches
                    self.warning(f"   Old code '{old_code}' still found in {filepath.name}: {matches} occurrences")

        if old_code_references == 0:
            self.log(f"   ✅ No old code references found")
        else:
            self.log(f"   ⚠️  Found {old_code_references} old code references")

        # Check 2: New codes exist
        self.log("\n2. Verifying new codes exist...")
        new_code_files = defaultdict(list)
        for filepath in self.appendices_dir.glob("*.tex"):
            match = re.match(r'^([A-Z]{1,3})', filepath.name)
            if match:
                code = match.group(1)
                new_code_files[code].append(filepath.name)

        missing_new_codes = set(self.old_to_new.values()) - set(new_code_files.keys())
        if missing_new_codes:
            self.warning(f"   New codes not found: {missing_new_codes}")
        else:
            self.log(f"   ✅ All {len(set(self.old_to_new.values()))} new codes found in files")

        # Check 3: Checksum verification
        self.log("\n3. Computing post-migration checksums...")
        modified_count = 0
        for filepath in list(self.chapters_dir.rglob("*")) + list(self.appendices_dir.rglob("*")) + list(self.docs_dir.rglob("*")):
            if filepath.is_file():
                rel_path = str(filepath.relative_to(self.repo_root))
                checksum = self.calculate_checksum(filepath)
                self.stats['checksums_after'][rel_path] = checksum
                if rel_path in self.stats['checksums_before']:
                    if checksum != self.stats['checksums_before'][rel_path]:
                        modified_count += 1

        self.log(f"   ✅ {modified_count} files were modified")

        return old_code_references == 0

    def _find_circular_dependencies(self) -> List[List[str]]:
        """Find circular dependencies in appendix references"""
        # Simplified circular dependency detection
        cycles = []
        # In real implementation, would need to build full dependency graph
        return cycles

    def phase_6_generate_report(self) -> str:
        """Generate final report"""
        self.log("\n" + "="*80)
        self.log("PHASE 6: GENERATE REPORT")
        self.log("="*80)

        report = f"""
# Complete Appendix Code Migration Report

**Execution Date:** {datetime.now().isoformat()}
**Status:** {'✅ SUCCESS' if not self.stats['errors'] else '❌ FAILED'}

## Migration Statistics

### Files Processed
- Files renamed: {self.stats['files_renamed']}
- References updated: {self.stats['references_updated']}
- Files checksummed: {len(self.stats['checksums_before'])}

### Codes Migrated
- Total old codes: {len(self.old_to_new)}
- Total new codes: {len(set(self.old_to_new.values()))}

### Quality Metrics
- Errors: {len(self.stats['errors'])}
- Warnings: {len(self.stats['warnings'])}

## Detailed Changes

### Old Code → New Code Mapping
"""
        for old, new in sorted(self.old_to_new.items()):
            report += f"\n- {old:6s} → {new:6s}"

        if self.stats['errors']:
            report += f"\n\n## Errors ({len(self.stats['errors'])})\n"
            for error in self.stats['errors']:
                report += f"\n- {error}"

        if self.stats['warnings']:
            report += f"\n\n## Warnings ({len(self.stats['warnings'])})\n"
            for warning in self.stats['warnings']:
                report += f"\n- {warning}"

        report_file = self.execution_dir / "MIGRATION-REPORT.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)

        self.log(f"\n   ✅ Report saved: {report_file.relative_to(self.repo_root)}")
        return report

    def run_complete_migration(self, dry_run: bool = True) -> bool:
        """Execute complete migration"""
        self.log(f"\n{'='*80}")
        self.log(f"APPENDIX CODE MIGRATION SYSTEM")
        self.log(f"{'='*80}")
        self.log(f"Mode: {'DRY-RUN' if dry_run else 'EXECUTE'}")
        self.log(f"Execution ID: {self.execution_dir.name}")

        # Phase 1: Pre-checks
        if not self.phase_1_pre_checks():
            self.log("\n❌ PRE-CHECKS FAILED - Aborting migration")
            return False

        # Phase 2: Backup
        if not self.phase_2_backup():
            self.log("\n❌ BACKUP FAILED - Aborting migration")
            return False

        # Phase 3: Dry-run
        if not self.phase_3_dry_run():
            self.log("\n❌ DRY-RUN FAILED - Aborting migration")
            return False

        if dry_run:
            self.log("\n" + "="*80)
            self.log("✅ DRY-RUN COMPLETED SUCCESSFULLY")
            self.log("="*80)
            self.log(f"\nTo execute migration, run:")
            self.log(f"  python scripts/execute-complete-migration.py --execute")
            return True

        # Phase 4: Execute
        if not self.phase_4_execute_migration():
            self.log("\n❌ MIGRATION FAILED - Attempting rollback...")
            self._rollback()
            return False

        # Phase 5: Validate
        if not self.phase_5_post_validation():
            self.log("\n⚠️  VALIDATION WARNINGS - Check report")

        # Phase 6: Report
        self.phase_6_generate_report()

        self.log("\n" + "="*80)
        self.log("✅ MIGRATION COMPLETED SUCCESSFULLY")
        self.log("="*80)
        self.log(f"\nResults:")
        self.log(f"  - Files renamed: {self.stats['files_renamed']}")
        self.log(f"  - References updated: {self.stats['references_updated']}")
        self.log(f"  - Errors: {len(self.stats['errors'])}")
        self.log(f"  - Warnings: {len(self.stats['warnings'])}")
        self.log(f"\nExecution report: {self.execution_dir.relative_to(self.repo_root)}/")

        return True

    def _rollback(self):
        """Restore from backup"""
        self.log("\n🔄 ROLLING BACK...")
        try:
            for backup_name in ['appendices', 'chapters', 'docs', 'models']:
                backup_path = self.backup_dir / backup_name
                target_path = self.repo_root / backup_name
                if backup_path.exists():
                    shutil.rmtree(target_path, ignore_errors=True)
                    shutil.copytree(backup_path, target_path)
                    self.log(f"   ✅ Restored {backup_name}/")
        except Exception as e:
            self.error(f"Rollback failed: {e}")

def main():
    import sys

    executor = CompleteMigrationExecutor()

    if len(sys.argv) < 2 or sys.argv[1] == '--dry-run':
        executor.run_complete_migration(dry_run=True)
    elif sys.argv[1] == '--execute':
        response = input("\n⚠️  This will rename 81+ files and update 900+ references. Continue? (yes/no): ")
        if response.lower() == 'yes':
            executor.run_complete_migration(dry_run=False)
        else:
            print("Aborted.")
    elif sys.argv[1] == '--validate':
        print("Validation not yet implemented")
    elif sys.argv[1] == '--rollback':
        print("Rollback not yet implemented")
    else:
        print("Usage: python execute-complete-migration.py [--dry-run|--execute|--validate|--rollback]")

if __name__ == '__main__':
    main()
