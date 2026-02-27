#!/usr/bin/env python3
"""
Cross-file validation for data/skill-levels/ directory.

Checks:
1. WEF ID consistency: simplified IDs in wef-to-onet-mapping resolve via
   id_crosswalk to valid official IDs in wef-taxonomy-official.yaml
2. ESCO→WEF name resolution: wef_official_id fields in esco-to-wef-mapping
   resolve to valid entries in wef-taxonomy-official.yaml
3. Kaufland role completeness: all 7 roles present across all files that
   reference roles (kaufland-role-profiles, bartram-factors, dach-transferability)
4. Cross-reference file paths: all file refs in cross_references blocks exist
5. O*NET ability keys: loadings in wef-to-onet-mapping reference valid
   abilities from onet-abilities.yaml
6. README line count accuracy: reported vs actual line counts

Usage:
    python scripts/validate_skill_levels.py
    python scripts/validate_skill_levels.py --check wef_ids
    python scripts/validate_skill_levels.py --check roles
    python scripts/validate_skill_levels.py --check onet
    python scripts/validate_skill_levels.py --check xrefs
    python scripts/validate_skill_levels.py --check readme
    python scripts/validate_skill_levels.py --check all
"""

import sys
import os
import re
import yaml
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
SKILL_DIR = BASE / "data" / "skill-levels"

# ─── Helpers ────────────────────────────────────────────────────────────────

def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def line_count(path):
    with open(path, "r", encoding="utf-8") as f:
        return sum(1 for _ in f)

def collect_official_ids(taxonomy):
    """Recursively collect all WEF IDs from the official taxonomy."""
    ids = set()
    if isinstance(taxonomy, dict):
        if "id" in taxonomy and isinstance(taxonomy["id"], str) and taxonomy["id"].startswith("WEF-"):
            ids.add(taxonomy["id"])
        for v in taxonomy.values():
            ids |= collect_official_ids(v)
    elif isinstance(taxonomy, list):
        for item in taxonomy:
            ids |= collect_official_ids(item)
    return ids

def collect_onet_keys(onet_data):
    """Collect all O*NET ability keys from onet-abilities.yaml.

    Structure: categories.<category>.abilities.<ability_key> (dict of dicts)
    """
    keys = set()
    categories = onet_data.get("categories", {}) if isinstance(onet_data, dict) else {}
    for category_key in ["cognitive", "psychomotor", "physical", "sensory"]:
        category = categories.get(category_key, {})
        if isinstance(category, dict):
            abilities = category.get("abilities", {})
            if isinstance(abilities, dict):
                keys.update(abilities.keys())
    return keys


# ─── Check 1: WEF ID Consistency ───────────────────────────────────────────

def check_wef_ids():
    """Verify all simplified WEF IDs in wef-to-onet-mapping resolve to valid official IDs."""
    print("\n=== CHECK 1: WEF ID Consistency ===")
    errors = []

    taxonomy = load_yaml(SKILL_DIR / "wef-taxonomy-official.yaml")
    official_ids = collect_official_ids(taxonomy)

    mapping = load_yaml(SKILL_DIR / "wef-to-onet-mapping.yaml")

    # Check id_crosswalk entries
    crosswalk = mapping.get("id_crosswalk", {})
    if not crosswalk:
        errors.append("MISSING: id_crosswalk section in wef-to-onet-mapping.yaml")
    else:
        for simplified_id, entry in crosswalk.items():
            ref_ids = entry.get("official_ids", [])
            for ref_id in ref_ids:
                if ref_id not in official_ids:
                    errors.append(f"BROKEN: {simplified_id} → {ref_id} not in official taxonomy")

    # Check inline wef_official_id on skill entries
    skills = mapping.get("skills", {})
    for skill_key, skill in skills.items():
        if not isinstance(skill, dict):
            continue
        official_id = skill.get("wef_official_id")
        official_ids_list = skill.get("wef_official_ids", [])
        refs = ([official_id] if official_id else []) + official_ids_list
        if not refs:
            errors.append(f"MISSING: {skill_key} has no wef_official_id(s)")
        for ref_id in refs:
            if ref_id not in official_ids:
                errors.append(f"BROKEN: {skill_key} → {ref_id} not in official taxonomy")

    if errors:
        for e in errors:
            print(f"  ❌ {e}")
    else:
        print(f"  ✅ All {len(crosswalk)} crosswalk entries resolve correctly")
        print(f"  ✅ All {len(skills)} skill entries have valid wef_official_id(s)")
    return errors


# ─── Check 2: ESCO→WEF Name Resolution ─────────────────────────────────────

def check_esco_wef_names():
    """Verify wef_official_id fields in esco-to-wef-mapping resolve to valid IDs."""
    print("\n=== CHECK 2: ESCO→WEF Name Resolution ===")
    errors = []

    taxonomy = load_yaml(SKILL_DIR / "wef-taxonomy-official.yaml")
    official_ids = collect_official_ids(taxonomy)

    esco = load_yaml(SKILL_DIR / "esco-to-wef-mapping.yaml")
    mappings = esco.get("mappings", {})

    total_entries = 0
    entries_with_id = 0

    for cluster_key, cluster in mappings.items():
        if not isinstance(cluster, dict):
            continue
        wef_mappings = cluster.get("wef_mappings", [])
        for wef_map in wef_mappings:
            if not isinstance(wef_map, dict):
                continue
            total_entries += 1
            official_id = wef_map.get("wef_official_id")
            official_ids_list = wef_map.get("wef_official_ids", [])
            refs = ([official_id] if official_id else []) + official_ids_list
            if refs:
                entries_with_id += 1
            for ref_id in refs:
                if ref_id not in official_ids:
                    errors.append(f"BROKEN: {cluster_key} → wef_official_id {ref_id} not in taxonomy")

    coverage = entries_with_id / total_entries * 100 if total_entries else 0

    if errors:
        for e in errors:
            print(f"  ❌ {e}")
    print(f"  ℹ️  {entries_with_id}/{total_entries} ESCO→WEF entries have wef_official_id ({coverage:.0f}%)")
    if not errors:
        print(f"  ✅ All referenced IDs are valid")
    return errors


# ─── Check 3: Kaufland Role Completeness ───────────────────────────────────

def check_roles():
    """Verify all 7 Kaufland roles are present in all role-referencing files."""
    print("\n=== CHECK 3: Kaufland Role Completeness ===")
    errors = []

    # Expected roles from kaufland-role-profiles.yaml
    # Structure: roles.<role_key> (dict of dicts), each with id: "ROLE-K-XXX"
    kauf = load_yaml(SKILL_DIR / "kaufland-role-profiles.yaml")
    roles_data = kauf.get("roles", {})
    expected_roles = set()
    kauf_role_keys = set()

    if isinstance(roles_data, dict):
        for role_key, role_val in roles_data.items():
            kauf_role_keys.add(role_key)
            if isinstance(role_val, dict) and "id" in role_val:
                expected_roles.add(role_val["id"])

    print(f"  ℹ️  Expected roles: {len(expected_roles)} ({', '.join(sorted(expected_roles))})")

    # Check bartram-factors.yaml role_profiles.roles
    # Structure: role_profiles.roles.<english_key> (dict of dicts)
    bartram = load_yaml(SKILL_DIR / "bartram-factors.yaml")
    bartram_roles = set()
    role_profiles = bartram.get("role_profiles", {})
    if isinstance(role_profiles, dict):
        roles_section = role_profiles.get("roles", {})
        if isinstance(roles_section, dict):
            bartram_roles = set(roles_section.keys())

    # Check dach-transferability.yaml kaufland_role_eqf_mapping.roles
    # Structure: kaufland_role_eqf_mapping.roles is a list of dicts with role_ref
    dach = load_yaml(SKILL_DIR / "dach-transferability.yaml")
    dach_roles = set()
    eqf_mapping = dach.get("kaufland_role_eqf_mapping", {})
    role_list = []
    if isinstance(eqf_mapping, dict):
        role_list = eqf_mapping.get("roles", [])
    elif isinstance(eqf_mapping, list):
        role_list = eqf_mapping
    for entry in role_list:
        if isinstance(entry, dict) and "role_ref" in entry:
            dach_roles.add(entry["role_ref"])

    missing_dach = expected_roles - dach_roles
    if missing_dach:
        errors.append(f"dach-transferability.yaml missing roles: {missing_dach}")
    else:
        print(f"  ✅ dach-transferability.yaml: all {len(expected_roles)} roles present")

    # Check bartram role_profiles count (bartram uses English keys, kaufland uses German)
    if len(bartram_roles) < len(kauf_role_keys):
        errors.append(f"bartram-factors.yaml role_profiles has {len(bartram_roles)} roles, expected {len(kauf_role_keys)}")
    else:
        print(f"  ✅ bartram-factors.yaml: {len(bartram_roles)} role profiles present")

    if errors:
        for e in errors:
            print(f"  ❌ {e}")
    return errors


# ─── Check 4: Cross-Reference File Paths ──────────────────────────────────

def check_xrefs():
    """Verify all file paths in cross_references blocks exist."""
    print("\n=== CHECK 4: Cross-Reference File Paths ===")
    errors = []
    checked = 0

    for yaml_file in sorted(SKILL_DIR.glob("*.yaml")):
        data = load_yaml(yaml_file)
        if not isinstance(data, dict):
            continue

        # Check metadata-level cross_references
        xrefs = {}
        metadata = data.get("metadata", {})
        if isinstance(metadata, dict):
            for key in ["cross_references", "scale_ref", "wef_ref", "dqr_ref",
                        "nqr_ch_ref", "nqr_at_ref", "dach_transferability_ref",
                        "kaufland_roles_ref"]:
                val = metadata.get(key)
                if isinstance(val, str) and val.startswith("data/"):
                    xrefs[key] = val
                elif isinstance(val, dict):
                    for subkey, subval in val.items():
                        if isinstance(subval, str) and subval.startswith("data/"):
                            xrefs[f"{key}.{subkey}"] = subval

        # Also check top-level refs
        for key in ["cross_references"]:
            val = data.get(key)
            if isinstance(val, dict):
                for subkey, subval in val.items():
                    if isinstance(subval, str) and subval.startswith("data/"):
                        xrefs[f"{key}.{subkey}"] = subval

        for ref_key, ref_path in xrefs.items():
            checked += 1
            full_path = BASE / ref_path
            if not full_path.exists():
                errors.append(f"{yaml_file.name}:{ref_key} → {ref_path} NOT FOUND")

    if errors:
        for e in errors:
            print(f"  ❌ {e}")
    else:
        print(f"  ✅ All {checked} cross-reference file paths exist")
    return errors


# ─── Check 5: O*NET Ability Keys ──────────────────────────────────────────

def check_onet():
    """Verify O*NET ability keys in wef-to-onet-mapping match onet-abilities.yaml."""
    print("\n=== CHECK 5: O*NET Ability Key Consistency ===")
    errors = []

    onet = load_yaml(SKILL_DIR / "onet-abilities.yaml")
    valid_keys = collect_onet_keys(onet)

    mapping = load_yaml(SKILL_DIR / "wef-to-onet-mapping.yaml")
    skills = mapping.get("skills", {})

    referenced_keys = set()
    for skill_key, skill in skills.items():
        if not isinstance(skill, dict):
            continue
        loadings = skill.get("onet_loadings", {})
        if isinstance(loadings, dict):
            for ability_key in loadings:
                referenced_keys.add(ability_key)
                if valid_keys and ability_key not in valid_keys:
                    errors.append(f"{skill_key}: O*NET key '{ability_key}' not in onet-abilities.yaml")

    if not valid_keys:
        print(f"  ⚠️  Could not extract O*NET keys (schema may differ) — {len(referenced_keys)} unique keys referenced")
    elif errors:
        for e in errors:
            print(f"  ❌ {e}")
    else:
        print(f"  ✅ All {len(referenced_keys)} referenced O*NET ability keys are valid")
    return errors


# ─── Check 6: README Line Count Accuracy ──────────────────────────────────

def check_readme():
    """Verify README line counts match actual file sizes."""
    print("\n=== CHECK 6: README Line Count Accuracy ===")
    errors = []
    warnings = []

    readme_path = SKILL_DIR / "README.md"
    if not readme_path.exists():
        errors.append("README.md not found")
        print(f"  ❌ {errors[0]}")
        return errors

    readme_text = readme_path.read_text(encoding="utf-8")

    # Extract line counts from README table: | `filename.yaml` | NNN | Tier | Description |
    # Line count is in the second column (after filename)
    pattern = r'\|\s*`([^`]+\.yaml)`\s*\|\s*~?(\d+)\s*\|'
    matches = re.findall(pattern, readme_text)

    for filename, stated_count in matches:
        stated = int(stated_count)
        file_path = SKILL_DIR / filename
        if not file_path.exists():
            errors.append(f"{filename}: file not found")
            continue
        actual = line_count(file_path)
        delta = abs(actual - stated)
        pct = delta / stated * 100 if stated else 0

        # Tilde-prefixed counts get 15% tolerance, exact counts get 5%
        is_approx = f"~{stated}" in readme_text
        threshold = 15 if is_approx else 5

        if pct > threshold:
            errors.append(f"{filename}: README says {stated}, actual {actual} ({pct:.0f}% off)")
        elif delta > 5:
            warnings.append(f"{filename}: README says {'~' if is_approx else ''}{stated}, actual {actual} (within tolerance)")

    for w in warnings:
        print(f"  ⚠️  {w}")
    if errors:
        for e in errors:
            print(f"  ❌ {e}")
    else:
        print(f"  ✅ All {len(matches)} file line counts within tolerance")
    return errors


# ─── Main ──────────────────────────────────────────────────────────────────

def main():
    check = "all"
    if len(sys.argv) > 2 and sys.argv[1] == "--check":
        check = sys.argv[2]

    print("=" * 70)
    print("SKILL-LEVELS CROSS-FILE VALIDATION")
    print(f"Directory: {SKILL_DIR}")
    print("=" * 70)

    all_errors = []

    checks = {
        "wef_ids": check_wef_ids,
        "esco": check_esco_wef_names,
        "roles": check_roles,
        "xrefs": check_xrefs,
        "onet": check_onet,
        "readme": check_readme,
    }

    if check == "all":
        for name, fn in checks.items():
            all_errors.extend(fn())
    elif check in checks:
        all_errors.extend(checks[check]())
    else:
        print(f"Unknown check: {check}")
        print(f"Available: {', '.join(checks.keys())}, all")
        sys.exit(1)

    print("\n" + "=" * 70)
    if all_errors:
        print(f"RESULT: {len(all_errors)} error(s) found")
        sys.exit(1)
    else:
        print("RESULT: All checks passed ✅")
        sys.exit(0)


if __name__ == "__main__":
    main()
