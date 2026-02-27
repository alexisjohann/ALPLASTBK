#!/usr/bin/env python3
"""
Execute full appendix code migration
Purpose: Migrate all 120 appendices and update all 1,573+ references
"""

import json
import re
import shutil
from pathlib import Path
from collections import defaultdict
from datetime import datetime

class FullMigrationExecutor:
    def __init__(self):
        self.repo_root = Path("/home/user/complementarity-context-framework")
        self.appendices_dir = self.repo_root / "appendices"
        self.chapters_dir = self.repo_root / "chapters"
        self.docs_dir = self.repo_root / "docs"
        self.audit_dir = self.repo_root / "migration-audit"

        # Load registry
        registry_file = self.audit_dir / "appendix-registry.json"
        with open(registry_file, 'r') as f:
            self.registry = json.load(f)

        # Build mapping
        self.old_to_new = {}
        for entry in self.registry:
            old_code = entry["old_code"]
            new_code = entry["new_code"]
            if old_code not in self.old_to_new:
                self.old_to_new[old_code] = {}
            self.old_to_new[old_code][entry["old_filename"]] = new_code

        self.stats = {
            "files_renamed": 0,
            "files_failed": 0,
            "references_updated": 0,
            "references_failed": 0,
        }

    def phase_1_backup(self):
        """Phase 1: Create backup of all files"""
        print("\n" + "=" * 80)
        print("PHASE 1: CREATE BACKUPS")
        print("=" * 80)

        backup_dirs = {
            "appendices": self.audit_dir / "full-backup/appendices",
            "chapters": self.audit_dir / "full-backup/chapters",
            "docs": self.audit_dir / "full-backup/docs",
        }

        for key, backup_path in backup_dirs.items():
            backup_path.mkdir(parents=True, exist_ok=True)

            if key == "appendices":
                source_dir = self.appendices_dir
            elif key == "chapters":
                source_dir = self.chapters_dir
            elif key == "docs":
                source_dir = self.docs_dir

            count = 0
            for filepath in source_dir.glob("*.tex") if key != "docs" else source_dir.glob("**/*.md"):
                if key == "appendices" and filepath.name.startswith("00_"):
                    continue
                shutil.copy2(filepath, backup_path / filepath.name)
                count += 1

            print(f"✅ Backed up {count} files to {key}")

        print(f"\n✅ All backups created")
        return True

    def phase_2_rename_files(self):
        """Phase 2: Rename all appendix files"""
        print("\n" + "=" * 80)
        print("PHASE 2: RENAME APPENDIX FILES")
        print("=" * 80)

        for entry in self.registry:
            old_filename = entry["old_filename"]
            new_filename = entry["new_filename"]

            old_path = self.appendices_dir / old_filename
            new_path = self.appendices_dir / new_filename

            if not old_path.exists():
                print(f"⚠️  Skipped (not found): {old_filename}")
                continue

            try:
                old_path.rename(new_path)
                self.stats["files_renamed"] += 1
                if self.stats["files_renamed"] % 20 == 0:
                    print(f"  Renamed {self.stats['files_renamed']} files...")
            except Exception as e:
                print(f"❌ Failed to rename {old_filename}: {e}")
                self.stats["files_failed"] += 1

        print(f"\n✅ Renamed {self.stats['files_renamed']} files")
        return True

    def phase_3_update_references(self):
        """Phase 3: Update all references"""
        print("\n" + "=" * 80)
        print("PHASE 3: UPDATE REFERENCES")
        print("=" * 80)

        # Search and update in all files
        search_dirs = [
            (self.chapters_dir, "chapters"),
            (self.appendices_dir, "appendices"),
            (self.docs_dir, "docs"),
        ]

        for search_dir, dir_type in search_dirs:
            if not search_dir.exists():
                continue

            if dir_type == "docs":
                file_pattern = "**/*.md"
            else:
                file_pattern = "*.tex"

            for filepath in search_dir.glob(file_pattern):
                self.update_file_references(filepath)

        print(f"\n✅ Updated {self.stats['references_updated']} references")
        return True

    def update_file_references(self, filepath):
        """Update references in a single file"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            original_content = content

            # Update text references: "Appendix X" → "Appendix NEW"
            for old_code, new_code in self.old_to_new.items():
                # Only use first mapping (they should all be same for each file)
                if isinstance(new_code, dict):
                    new_code = list(new_code.values())[0] if new_code else old_code

                # Pattern: "Appendix X" where X is the old code
                pattern = rf"Appendix\s+{re.escape(old_code)}\b"
                if re.search(pattern, content):
                    content = re.sub(pattern, f"Appendix {new_code}", content)
                    self.stats["references_updated"] += len(re.findall(pattern, original_content))

                # LaTeX refs: "\ref{app:X}" → "\ref{app:NEW}"
                pattern = rf"\\ref{{app:{re.escape(old_code)}\}}"
                if re.search(pattern, content):
                    content = re.sub(pattern, f"\\ref{{app:{new_code}}}", content)

                # Axiom/Theorem refs: "X-1" → "NEW-1"
                pattern = rf"\b{re.escape(old_code)}-(\d+)\b"
                if re.search(pattern, content):
                    content = re.sub(pattern, f"{new_code}-\\1", content)

            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)

        except Exception as e:
            print(f"⚠️  Error updating {filepath}: {e}")
            self.stats["references_failed"] += 1

    def phase_4_validate(self):
        """Phase 4: Validate migration"""
        print("\n" + "=" * 80)
        print("PHASE 4: VALIDATE MIGRATION")
        print("=" * 80)

        # Check old codes are gone
        old_code_patterns = set(entry["old_code"] for entry in self.registry)
        remaining_old = []

        for old_code in old_code_patterns:
            files = list(self.appendices_dir.glob(f"{old_code}_*.tex"))
            if files:
                remaining_old.extend(files)

        if remaining_old:
            print(f"\n🔴 Old codes still exist: {len(remaining_old)} files")
            for f in remaining_old[:5]:
                print(f"   {f.name}")
            return False
        else:
            print(f"✅ All old codes removed")

        # Check new codes exist
        new_code_count = {}
        for new_code in set(entry["new_code"] for entry in self.registry):
            count = len(list(self.appendices_dir.glob(f"{new_code}_*.tex")))
            if count > 0:
                new_code_count[new_code] = count

        print(f"✅ {len(new_code_count)} new codes present")

        return True

    def phase_5_report(self):
        """Phase 5: Generate report"""
        print("\n" + "=" * 80)
        print("PHASE 5: MIGRATION REPORT")
        print("=" * 80)

        report = {
            "timestamp": datetime.now().isoformat(),
            "statistics": self.stats,
            "summary": {
                "total_appendices": len(self.registry),
                "files_renamed": self.stats["files_renamed"],
                "references_updated": self.stats["references_updated"],
            }
        }

        report_file = self.audit_dir / "migration-report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n📊 Migration Statistics:")
        print(f"   Total appendices: {report['summary']['total_appendices']}")
        print(f"   Files renamed: {report['summary']['files_renamed']}")
        print(f"   References updated: {report['summary']['references_updated']}")
        print(f"\n✅ Report saved: {report_file}")

        return True

    def run_full_migration(self):
        """Execute full migration"""
        print("\n\n" + "=" * 80)
        print("FULL APPENDIX CODE MIGRATION")
        print("=" * 80)
        print(f"Start time: {datetime.now().isoformat()}")

        phases = [
            ("Backup", self.phase_1_backup),
            ("Rename Files", self.phase_2_rename_files),
            ("Update References", self.phase_3_update_references),
            ("Validate", self.phase_4_validate),
            ("Report", self.phase_5_report),
        ]

        results = {}
        for phase_name, phase_func in phases:
            try:
                result = phase_func()
                results[phase_name] = "✅ PASS" if result else "🔴 FAIL"
            except Exception as e:
                print(f"\n🔴 Phase {phase_name} failed: {e}")
                results[phase_name] = "🔴 FAIL"

        # Summary
        print("\n\n" + "=" * 80)
        print("MIGRATION SUMMARY")
        print("=" * 80)

        for phase, result in results.items():
            print(f"{phase:20s}: {result}")

        all_pass = all(v == "✅ PASS" for v in results.values())

        print("\n" + "=" * 80)
        if all_pass:
            print("✅ MIGRATION COMPLETE - ALL PHASES PASSED")
        else:
            print("🔴 MIGRATION INCOMPLETE - SOME PHASES FAILED")
        print("=" * 80)

        return all_pass

def main():
    executor = FullMigrationExecutor()
    success = executor.run_full_migration()
    return 0 if success else 1

if __name__ == '__main__':
    exit(main())
