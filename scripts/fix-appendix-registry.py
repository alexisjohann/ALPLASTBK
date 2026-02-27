#!/usr/bin/env python3
"""
Fix appendix registry by improving classification
"""

import json
import yaml
from pathlib import Path
from collections import defaultdict

def load_mapping():
    """Load code mapping from YAML"""
    mapping_file = Path("/home/user/complementarity-context-framework/docs/frameworks/code-mapping.yaml")
    with open(mapping_file, 'r') as f:
        lines = f.readlines()
    yaml_start = 0
    for i, line in enumerate(lines):
        if line.strip() and not line.strip().startswith(('**', '#', '---')):
            yaml_start = i
            break
    yaml_content = ''.join(lines[yaml_start:])
    return yaml.safe_load(yaml_content) or {}

def find_code_category(code, mapping):
    """Find which category a code belongs to"""
    for category, codes_dict in mapping.items():
        if isinstance(codes_dict, dict):
            if code in codes_dict:
                return category
    return None

def fix_registry():
    """Fix the registry by using the mapping to correct classifications"""

    mapping = load_mapping()
    registry_file = Path("/home/user/complementarity-context-framework/migration-audit/appendix-registry.json")

    with open(registry_file, 'r') as f:
        registry = json.load(f)

    print("=" * 80)
    print("FIXING APPENDIX REGISTRY")
    print("=" * 80)

    fixed_count = 0
    unmapped_codes = set()

    for entry in registry:
        old_code = entry["old_code"]

        # Try to find category from mapping
        category = find_code_category(old_code, mapping)

        if category:
            if entry["category"] == "unknown":
                print(f"\n✅ Fixed {old_code}: unknown → {category}")
                entry["category"] = category
                fixed_count += 1

            # Get correct new code
            if category in mapping and old_code in mapping[category]:
                new_code = mapping[category][old_code]
                if entry["new_code"].startswith("UNMAPPED_"):
                    print(f"   new_code: UNMAPPED_{old_code} → {new_code}")
                    entry["new_code"] = new_code
                    # Fix filename
                    entry["new_filename"] = entry["old_filename"].replace(f"{old_code}_", f"{new_code}_", 1)
                    fixed_count += 1
        else:
            unmapped_codes.add(old_code)

    print(f"\n" + "=" * 80)
    print(f"Fixed: {fixed_count} entries")
    print(f"Unmapped codes: {len(unmapped_codes)}")

    if unmapped_codes:
        print(f"\nCodes not in mapping: {sorted(unmapped_codes)}")

    # Save fixed registry
    with open(registry_file, 'w') as f:
        json.dump(registry, f, indent=2)

    print(f"\n✅ Registry updated: {registry_file}")

    return registry

if __name__ == '__main__':
    fix_registry()
