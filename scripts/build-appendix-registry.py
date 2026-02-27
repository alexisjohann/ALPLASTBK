#!/usr/bin/env python3
"""
Build complete appendix registry from actual files
Purpose: Create definitive file-by-file mapping for migration
"""

import json
import re
from pathlib import Path
from collections import defaultdict

class AppendixRegistryBuilder:
    def __init__(self, repo_root="/home/user/complementarity-context-framework"):
        self.repo_root = Path(repo_root)
        self.appendices_dir = self.repo_root / "appendices"

        # Load code mapping
        import yaml
        mapping_file = self.repo_root / "docs/frameworks/code-mapping.yaml"
        with open(mapping_file, 'r') as f:
            lines = f.readlines()
        yaml_start = 0
        for i, line in enumerate(lines):
            if line.strip() and not line.strip().startswith(('**', '#', '---')):
                yaml_start = i
                break
        yaml_content = ''.join(lines[yaml_start:])
        self.mapping = yaml.safe_load(yaml_content) or {}

        self.registry = []

    def classify_appendix(self, filename):
        """Classify appendix based on filename and content"""

        # Priority 1: Explicit category markers in filename
        if "LIT-" in filename:
            return "lit"
        elif "DOMAIN-" in filename:
            if "PAPAL" in filename:
                return "domain_new"
            return "domain"
        elif "METHOD-" in filename:
            return "method"
        elif "FORMAL-" in filename:
            return "formal"
        elif "THEORY-" in filename:
            return "formal"  # THEORY-* usually formal
        elif "REF-" in filename:
            return "ref"
        elif "PREDICT-" in filename:
            return "predict"
        elif "CONTEXT-" in filename:
            return "context"

        # Priority 2: Content-based classification
        filepath = self.appendices_dir / filename
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Look for category markers
            if "\\documentclass{appendix_lit}" in content or "LIT-" in content:
                return "lit"
            elif "\\documentclass{appendix_domain}" in content or "DOMAIN-" in content:
                return "domain"
            elif "\\documentclass{appendix_method}" in content or "METHOD-" in content:
                return "method"
            elif "\\documentclass{appendix_formal}" in content or "FORMAL-" in content:
                return "formal"
        except:
            pass

        # Priority 3: Known patterns
        if "literature" in filename.lower() or "research" in filename.lower():
            return "lit"
        elif "labor" in filename.lower() or "matching" in filename.lower():
            return "domain"
        elif "llm" in filename.lower() or "method" in filename.lower():
            return "method"
        elif "proof" in filename.lower() or "derivation" in filename.lower():
            return "formal"

        return None  # Unknown

    def get_new_code(self, old_code, category):
        """Get new code from mapping"""
        if category in self.mapping:
            if old_code in self.mapping[category]:
                return self.mapping[category][old_code]
        return None

    def build_registry(self):
        """Build complete registry from actual files"""

        files_by_code = defaultdict(list)

        # Scan all appendix files
        for filepath in sorted(self.appendices_dir.glob("*.tex")):
            filename = filepath.name

            # Skip templates and indices
            if filename.startswith("00_"):
                continue

            # Extract old code
            old_code = None
            if "_" in filename:
                parts = filename.split("_")
                old_code = parts[0]
            elif "." in filename:
                old_code = filename.split(".")[0]

            if not old_code:
                print(f"⚠️  Could not extract code from: {filename}")
                continue

            # Classify
            category = self.classify_appendix(filename)
            if not category:
                print(f"⚠️  Could not classify: {filename}")
                category = "unknown"

            # Get new code
            new_code = self.get_new_code(old_code, category)
            if not new_code:
                print(f"⚠️  No mapping found: {old_code} in {category}")
                new_code = f"UNMAPPED_{old_code}"

            # Generate new filename
            new_filename = filename.replace(f"{old_code}_", f"{new_code}_", 1)
            new_filename = new_filename.replace(f"{old_code}.", f"{new_code}.", 1)

            entry = {
                "old_filename": filename,
                "old_code": old_code,
                "category": category,
                "new_code": new_code,
                "new_filename": new_filename,
                "file_size": filepath.stat().st_size
            }

            self.registry.append(entry)
            files_by_code[old_code].append(entry)

        return files_by_code

    def validate_registry(self):
        """Validate registry for conflicts"""

        print("\n" + "=" * 80)
        print("REGISTRY VALIDATION")
        print("=" * 80)

        # Check for duplicate new codes
        new_codes = {}
        conflicts = []

        for entry in self.registry:
            new_code = entry["new_code"]
            if new_code in new_codes:
                conflicts.append({
                    "new_code": new_code,
                    "file1": new_codes[new_code]["old_filename"],
                    "file2": entry["old_filename"]
                })
            new_codes[new_code] = entry

        if conflicts:
            print(f"\n🔴 {len(conflicts)} NEUE CODE-KONFLIKTE:")
            for conf in conflicts:
                print(f"   {conf['new_code']}: {conf['file1']} <-> {conf['file2']}")
        else:
            print(f"\n✅ KEINE NEUEN CODE-KONFLIKTE")

        # Check for unmapped codes
        unmapped = [e for e in self.registry if e["new_code"].startswith("UNMAPPED_")]
        if unmapped:
            print(f"\n🔴 {len(unmapped)} UNMAPPED CODES:")
            for entry in unmapped:
                print(f"   {entry['old_code']}: {entry['old_filename']}")
        else:
            print(f"\n✅ ALLE CODES GEMAPPT")

        return len(conflicts) == 0 and len(unmapped) == 0

    def save_registry(self, output_file=None):
        """Save registry to JSON"""
        if not output_file:
            output_file = self.repo_root / "migration-audit/appendix-registry.json"

        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w') as f:
            json.dump(self.registry, f, indent=2)

        print(f"\n✅ Registry saved: {output_file}")
        print(f"   Total appendices: {len(self.registry)}")

        return output_file

    def print_summary(self):
        """Print summary statistics"""

        print("\n" + "=" * 80)
        print("APPENDIX REGISTRY SUMMARY")
        print("=" * 80)

        categories = defaultdict(list)
        for entry in self.registry:
            categories[entry["category"]].append(entry)

        print(f"\nByCategory:")
        for cat in sorted(categories.keys()):
            entries = categories[cat]
            print(f"  {cat:15s}: {len(entries):3d} files")

        print(f"\nTotal: {len(self.registry)} appendices")

        # Show duplicates (same old_code, different categories)
        from collections import Counter
        old_codes = Counter(e["old_code"] for e in self.registry)
        duplicates = {code: count for code, count in old_codes.items() if count > 1}

        if duplicates:
            print(f"\n📊 Old codes with multiple files:")
            for code in sorted(duplicates.keys()):
                entries = [e for e in self.registry if e["old_code"] == code]
                print(f"  {code} ({duplicates[code]} files):")
                for e in entries:
                    print(f"    - {e['old_filename']} ({e['category']})")

def main():
    builder = AppendixRegistryBuilder()

    print("Building appendix registry from actual files...")
    files_by_code = builder.build_registry()

    builder.print_summary()
    valid = builder.validate_registry()
    registry_file = builder.save_registry()

    print("\n" + "=" * 80)
    if valid:
        print("✅ REGISTRY VALID - Ready for migration")
    else:
        print("🔴 REGISTRY HAS ISSUES - Review above")
    print("=" * 80)

    return 0 if valid else 1

if __name__ == '__main__':
    exit(main())
