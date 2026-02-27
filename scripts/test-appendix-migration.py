#!/usr/bin/env python3
"""
Test appendix migration on small subset (10 files)
Purpose: Validate migration approach before full rollout
"""

import json
import re
import shutil
from pathlib import Path
from collections import defaultdict
from datetime import datetime

class SubsetMigrationTester:
    def __init__(self):
        self.repo_root = Path("/home/user/complementarity-context-framework")
        self.appendices_dir = self.repo_root / "appendices"
        self.chapters_dir = self.repo_root / "chapters"
        self.docs_dir = self.repo_root / "docs"
        self.test_dir = self.repo_root / "migration-test"
        self.test_dir.mkdir(exist_ok=True)

        # Load registry
        registry_file = self.repo_root / "migration-audit/appendix-registry.json"
        with open(registry_file, 'r') as f:
            self.registry = json.load(f)

        # Test files (no duplicates, unique mappings)
        self.test_files = {
            "A_formal_derivations.tex": "DER",
            "D_proofs.tex": "PRF",
            "E_operationalization.tex": "OPS",
            "F_worked_examples.tex": "EXM",
            "H_computational_history.tex": "HRC",
            "I_nobel_contributions.tex": "NOB",
            "L_acemoglu_papers.tex": "ACE",
            "M_shleifer_papers.tex": "SHL",
            "N_heckman_papers.tex": "HEC",
            "O_autor_papers.tex": "AUT",
        }

    def test_step_1_backup(self):
        """Step 1: Create backups of test files"""
        print("\n" + "=" * 80)
        print("STEP 1: BACKUP TEST FILES")
        print("=" * 80)

        backup_dir = self.test_dir / "backup"
        backup_dir.mkdir(exist_ok=True)

        for filename in self.test_files.keys():
            src = self.appendices_dir / filename
            if src.exists():
                dst = backup_dir / filename
                shutil.copy2(src, dst)
                size = src.stat().st_size
                print(f"✅ Backed up: {filename} ({size} bytes)")
            else:
                print(f"❌ NOT FOUND: {filename}")
                return False

        print(f"\n✅ All test files backed up to: {backup_dir}")
        return True

    def test_step_2_rename_files(self):
        """Step 2: Test file renaming"""
        print("\n" + "=" * 80)
        print("STEP 2: TEST FILE RENAMING")
        print("=" * 80)

        renames = []
        errors = []

        for old_name, new_code in self.test_files.items():
            old_path = self.appendices_dir / old_name
            # Generate new name
            new_name = old_name.replace(old_name.split("_")[0] + "_", new_code + "_", 1)
            new_path = self.appendices_dir / new_name

            if not old_path.exists():
                errors.append(f"Source not found: {old_name}")
                continue

            # Rename
            try:
                old_path.rename(new_path)
                renames.append((old_name, new_name))
                print(f"✅ Renamed: {old_name} → {new_name}")
            except Exception as e:
                errors.append(f"Failed to rename {old_name}: {e}")
                print(f"❌ Failed: {old_name}: {e}")

        if errors:
            print(f"\n🔴 {len(errors)} ERRORS:")
            for error in errors:
                print(f"   {error}")
            return False

        print(f"\n✅ All {len(renames)} files renamed successfully")
        return True

    def test_step_3_update_references(self):
        """Step 3: Find and update references to test files"""
        print("\n" + "=" * 80)
        print("STEP 3: UPDATE REFERENCES")
        print("=" * 80)

        # Map old codes to new codes
        old_to_new = {
            "A": "DER",
            "D": "PRF",
            "E": "OPS",
            "F": "EXM",
            "H": "HRC",
            "I": "NOB",
            "L": "ACE",
            "M": "SHL",
            "N": "HEC",
            "O": "AUT",
        }

        updates = defaultdict(lambda: {"chapters": [], "appendices": [], "docs": []})

        # Search in chapters
        print("\n📍 Searching in chapters...")
        for filepath in self.chapters_dir.glob("*.tex"):
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            for old_code, new_code in old_to_new.items():
                # Text references
                pattern = rf"Appendix\s+{re.escape(old_code)}\b"
                if re.search(pattern, content):
                    updates[old_code]["chapters"].append((filepath.name, "text"))
                    print(f"  Found: Appendix {old_code} in {filepath.name}")

                # LaTeX refs
                pattern = rf"\\ref{{app:{re.escape(old_code)}\}}"
                if re.search(pattern, content):
                    updates[old_code]["chapters"].append((filepath.name, "LaTeX"))
                    print(f"  Found: \\ref{{app:{old_code}}} in {filepath.name}")

        # Search in appendices
        print("\n📍 Searching in appendices...")
        for filepath in self.appendices_dir.glob("*.tex"):
            if filepath.name.startswith("00_"):
                continue

            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            for old_code, new_code in old_to_new.items():
                # Text references
                pattern = rf"Appendix\s+{re.escape(old_code)}\b"
                if re.search(pattern, content):
                    updates[old_code]["appendices"].append((filepath.name, "text"))
                    print(f"  Found: Appendix {old_code} in {filepath.name}")

                # LaTeX refs
                pattern = rf"\\ref{{app:{re.escape(old_code)}\}}"
                if re.search(pattern, content):
                    updates[old_code]["appendices"].append((filepath.name, "LaTeX"))

        # Report
        print(f"\n📊 References found:")
        total = 0
        for old_code, locations in updates.items():
            if locations["chapters"] or locations["appendices"]:
                print(f"\n  Appendix {old_code} (→ {old_to_new[old_code]}):")
                if locations["chapters"]:
                    print(f"    Chapters: {len(locations['chapters'])} files")
                    for fname, typ in locations["chapters"]:
                        print(f"      - {fname} ({typ})")
                        total += 1
                if locations["appendices"]:
                    print(f"    Appendices: {len(locations['appendices'])} files")
                    for fname, typ in locations["appendices"]:
                        print(f"      - {fname} ({typ})")
                        total += 1

        print(f"\n✅ Total references to update: {total}")
        return updates

    def test_step_4_validate_files(self):
        """Step 4: Validate that old codes are gone and new codes exist"""
        print("\n" + "=" * 80)
        print("STEP 4: VALIDATE RENAMED FILES")
        print("=" * 80)

        old_to_new = {
            "A": "DER",
            "D": "PRF",
            "E": "OPS",
            "F": "EXM",
            "H": "HRC",
            "I": "NOB",
            "L": "ACE",
            "M": "SHL",
            "N": "HEC",
            "O": "AUT",
        }

        all_valid = True

        for old_code, new_code in old_to_new.items():
            # Check old code is gone
            old_files = list(self.appendices_dir.glob(f"{old_code}_*.tex"))
            if old_files:
                print(f"❌ Old code still exists: {old_code}: {[f.name for f in old_files]}")
                all_valid = False
            else:
                print(f"✅ Old code gone: {old_code}")

            # Check new code exists
            new_files = list(self.appendices_dir.glob(f"{new_code}_*.tex"))
            if new_files:
                print(f"✅ New code exists: {new_code}: {len(new_files)} file(s)")
            else:
                print(f"❌ New code NOT found: {new_code}")
                all_valid = False

        return all_valid

    def test_step_5_restore(self):
        """Step 5: Restore from backup"""
        print("\n" + "=" * 80)
        print("STEP 5: RESTORE FROM BACKUP")
        print("=" * 80)

        backup_dir = self.test_dir / "backup"
        restored = 0

        for filename in self.test_files.keys():
            backup_path = backup_dir / filename
            target_path = self.appendices_dir / filename

            # Extract original code
            old_code = filename.split("_")[0]
            new_code = self.test_files[filename]

            # Check if file was renamed
            new_filename = filename.replace(old_code + "_", new_code + "_", 1)
            renamed_path = self.appendices_dir / new_filename

            if renamed_path.exists():
                # Restore
                renamed_path.unlink()
                shutil.copy2(backup_path, target_path)
                restored += 1
                print(f"✅ Restored: {new_filename} → {filename}")
            elif target_path.exists():
                print(f"✅ Already present: {filename}")
            else:
                print(f"⚠️  Not found: {filename}")

        print(f"\n✅ Restored {restored} files from backup")
        return True

    def run_all_tests(self):
        """Run complete test sequence"""
        print("\n\n" + "=" * 80)
        print("APPENDIX MIGRATION - SUBSET TEST")
        print("=" * 80)
        print(f"Test date: {datetime.now().isoformat()}")
        print(f"Test files: {len(self.test_files)}")

        results = {
            "backup": self.test_step_1_backup(),
            "rename": self.test_step_2_rename_files(),
            "references": self.test_step_3_update_references(),
            "validate": self.test_step_4_validate_files(),
            "restore": self.test_step_5_restore(),
        }

        # Summary
        print("\n\n" + "=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)

        for step, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{step:15s}: {status}")

        all_pass = all(results.values()) if isinstance(results["references"], dict) else False
        if results["references"] and isinstance(results["references"], dict):
            all_pass = results["backup"] and results["rename"] and results["validate"] and results["restore"]

        print("\n" + "=" * 80)
        if all_pass:
            print("✅ ALL TESTS PASSED - Ready for full migration")
        else:
            print("🔴 SOME TESTS FAILED - Review above")
        print("=" * 80)

        return all_pass

def main():
    tester = SubsetMigrationTester()
    success = tester.run_all_tests()
    return 0 if success else 1

if __name__ == '__main__':
    exit(main())
