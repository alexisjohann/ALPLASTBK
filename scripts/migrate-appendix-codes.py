#!/usr/bin/env python3
"""
Appendix Code Migration Script
Purpose: Systematically rename all appendix codes from 1-3 letter to unique 3-letter codes
Strategy: Map old codes → new codes, update all references, create audit trail

Usage:
    python scripts/migrate-appendix-codes.py --scan           # Scan for all references
    python scripts/migrate-appendix-codes.py --validate       # Validate mapping
    python scripts/migrate-appendix-codes.py --migrate        # Execute migration (with backup)
    python scripts/migrate-appendix-codes.py --audit          # Generate audit report
"""

import os
import re
import json
import yaml
import shutil
from pathlib import Path
from collections import defaultdict
from datetime import datetime

class AppendixMigrator:
    def __init__(self, repo_root="/home/user/complementarity-context-framework"):
        self.repo_root = Path(repo_root)
        self.appendices_dir = self.repo_root / "appendices"
        self.docs_dir = self.repo_root / "docs"
        self.models_dir = self.repo_root / "models"
        self.mapping_file = self.docs_dir / "frameworks" / "code-mapping.yaml"
        self.audit_dir = self.repo_root / "migration-audit"
        self.audit_dir.mkdir(exist_ok=True)
        self.backup_dir = self.audit_dir / "backups"
        self.backup_dir.mkdir(exist_ok=True)

        self.mapping = self._load_mapping()
        self.old_to_new = self._build_reverse_mapping()
        self.references = defaultdict(list)

    def _load_mapping(self):
        """Load mapping from YAML file"""
        with open(self.mapping_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Find where YAML actually starts (look for "core:" or first key)
        yaml_start_idx = 0
        for i, line in enumerate(lines):
            if line.strip() and not line.strip().startswith(('**', '#', '---')):
                # Found first non-markdown line
                yaml_start_idx = i
                break

        yaml_content = ''.join(lines[yaml_start_idx:])
        return yaml.safe_load(yaml_content) or {}

    def _build_reverse_mapping(self):
        """Build old_code -> new_code mapping"""
        mapping = {}
        for category in ['core', 'formal', 'domain', 'context', 'method', 'predict', 'lit', 'ref']:
            if category in self.mapping:
                for old_code, new_code in self.mapping[category].items():
                    mapping[old_code] = new_code
        return mapping

    def scan_references(self):
        """Scan all files for appendix references"""
        print("🔍 Scanning for all appendix references...")

        patterns = [
            r'Appendix\s+([A-Z]{1,3})\b',           # "Appendix AA", "Appendix ABC"
            r'\\ref{app:([a-z0-9\-]+)}',            # LaTeX ref tags
            r'\\label{app:([a-z0-9\-]+)}',          # LaTeX label tags
            r'appendix{([A-Z]{1,3})}',              # appendix{AA}
        ]

        file_patterns = ['**/*.tex', '**/*.md', '**/*.yaml']
        search_dirs = [self.appendices_dir, self.docs_dir, self.models_dir]

        for search_dir in search_dirs:
            if not search_dir.exists():
                continue

            for file_pattern in file_patterns:
                for filepath in search_dir.glob(file_pattern):
                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()

                        for pattern in patterns:
                            for match in re.finditer(pattern, content):
                                code = match.group(1)
                                # Only track known codes
                                if code in self.old_to_new or len(code) <= 3:
                                    line_num = content[:match.start()].count('\n') + 1
                                    self.references[code].append({
                                        'file': str(filepath.relative_to(self.repo_root)),
                                        'line': line_num,
                                        'context': content[max(0, match.start()-50):match.end()+50]
                                    })
                    except Exception as e:
                        print(f"  ⚠️  Error reading {filepath}: {e}")

        # Save reference map
        ref_report = {
            'timestamp': datetime.now().isoformat(),
            'total_references': sum(len(v) for v in self.references.values()),
            'codes_found': len(self.references),
            'references': dict(self.references)
        }

        report_file = self.audit_dir / "reference-scan-report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(ref_report, f, indent=2, default=str)

        print(f"✅ Found {ref_report['total_references']} references across {ref_report['codes_found']} codes")
        print(f"📄 Report saved: {report_file}")

        return ref_report

    def validate_mapping(self):
        """Validate mapping consistency"""
        print("🔍 Validating code mapping...")

        # Check for duplicate new codes
        new_codes = list(self.old_to_new.values())
        duplicates = [code for code in set(new_codes) if new_codes.count(code) > 1]

        if duplicates:
            print(f"❌ ERROR: Duplicate new codes: {duplicates}")
            return False

        # Check for unmapped old codes
        all_old_codes = set()
        for category in ['core', 'formal', 'domain', 'context', 'method', 'predict', 'lit', 'ref']:
            if category in self.mapping:
                all_old_codes.update(self.mapping[category].keys())

        print(f"✅ Mapping validation:")
        print(f"   - Total codes: {len(all_old_codes)}")
        print(f"   - Unique new codes: {len(set(new_codes))}")
        print(f"   - No duplicates: {len(duplicates) == 0}")

        return len(duplicates) == 0

    def list_files_to_rename(self):
        """List all appendix files that will be renamed"""
        print("\n📋 Files to be renamed:")

        files_by_old_code = defaultdict(list)

        for filepath in self.appendices_dir.glob("*.tex"):
            filename = filepath.name
            # Extract code (first part before underscore or .tex)
            match = re.match(r'^([A-Z]{1,3})[_.]', filename)
            if match:
                code = match.group(1)
                if code in self.old_to_new:
                    new_code = self.old_to_new[code]
                    new_filename = filename.replace(f"{code}_", f"{new_code}_", 1).replace(f"{code}.", f"{new_code}.", 1)
                    files_by_old_code[code].append({
                        'old': filename,
                        'new': new_filename,
                        'path': filepath
                    })

        total_files = sum(len(v) for v in files_by_old_code.values())
        print(f"Total files to rename: {total_files}\n")

        for code in sorted(files_by_old_code.keys()):
            for item in files_by_old_code[code]:
                new_code = self.old_to_new[code]
                print(f"  {code} → {new_code}")
                print(f"    {item['old']} → {item['new']}")

        return files_by_old_code

    def create_migration_plan(self):
        """Create detailed migration plan document"""
        print("\n📋 Creating migration plan...")

        plan = {
            'timestamp': datetime.now().isoformat(),
            'status': 'DRAFT',
            'total_steps': 5,
            'steps': [
                {
                    'phase': 1,
                    'title': 'Backup Original Files',
                    'description': 'Create complete backup of appendices/ docs/ models/ directories',
                    'status': 'pending'
                },
                {
                    'phase': 2,
                    'title': 'Rename Appendix Files',
                    'description': 'Rename all appendix .tex files from old codes to new 3-letter codes',
                    'status': 'pending'
                },
                {
                    'phase': 3,
                    'title': 'Update Internal References',
                    'description': 'Update all "Appendix X" references in .tex and .md files',
                    'status': 'pending'
                },
                {
                    'phase': 4,
                    'title': 'Update Index',
                    'description': 'Update appendices/00_appendix_index.tex with new codes',
                    'status': 'pending'
                },
                {
                    'phase': 5,
                    'title': 'Verify & Validate',
                    'description': 'Run compliance checks and verify all references',
                    'status': 'pending'
                }
            ]
        }

        plan_file = self.audit_dir / "migration-plan.json"
        with open(plan_file, 'w', encoding='utf-8') as f:
            json.dump(plan, f, indent=2)

        print(f"✅ Migration plan created: {plan_file}")
        return plan

    def print_summary(self):
        """Print summary of what will be migrated"""
        print("\n" + "="*80)
        print("APPENDIX CODE MIGRATION SUMMARY")
        print("="*80)

        total_old_codes = len(set(self.old_to_new.keys()))
        total_new_codes = len(set(self.old_to_new.values()))

        print(f"\n📊 Statistics:")
        print(f"  - Old codes to migrate: {total_old_codes}")
        print(f"  - New unique codes: {total_new_codes}")
        print(f"  - Total references to update: {sum(len(v) for v in self.references.values())}")
        print(f"  - Appendix files: ~{len(list(self.appendices_dir.glob('*.tex')))}")
        print(f"  - Documentation files: ~{len(list(self.docs_dir.glob('**/*.md')))}")

        print(f"\n🎯 Next Steps:")
        print(f"  1. Review code-migration-mapping.yaml")
        print(f"  2. Run: python scripts/migrate-appendix-codes.py --validate")
        print(f"  3. Run: python scripts/migrate-appendix-codes.py --list-files")
        print(f"  4. Run: python scripts/migrate-appendix-codes.py --migrate")
        print(f"  5. Run: python scripts/migrate-appendix-codes.py --audit")
        print(f"\n📁 Audit trail directory: {self.audit_dir}")
        print("="*80 + "\n")

def main():
    import sys

    migrator = AppendixMigrator()

    if not migrator.validate_mapping():
        print("❌ Mapping validation failed!")
        return 1

    if len(sys.argv) < 2 or sys.argv[1] == '--scan':
        migrator.scan_references()
    elif sys.argv[1] == '--validate':
        migrator.validate_mapping()
    elif sys.argv[1] == '--list-files':
        migrator.list_files_to_rename()
    elif sys.argv[1] == '--plan':
        migrator.create_migration_plan()
    elif sys.argv[1] == '--summary':
        migrator.print_summary()
    else:
        print("Usage: python migrate-appendix-codes.py [--scan|--validate|--list-files|--plan|--summary]")
        return 1

    return 0

if __name__ == '__main__':
    exit(main())
