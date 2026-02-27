#!/usr/bin/env python3
"""
Intelligent appendix mapper using filename context
Resolves duplicate old codes by analyzing filenames and content
"""

import json
import re
from pathlib import Path
from collections import defaultdict

class IntelligentAppendixMapper:
    def __init__(self):
        self.registry_file = Path("/home/user/complementarity-context-framework/migration-audit/appendix-registry.json")

        # Load existing registry
        with open(self.registry_file, 'r') as f:
            self.registry = json.load(f)

        # Pattern-based new codes for duplicates
        self.duplicate_handlers = {
            # (old_code, category1_marker, category2_marker): (new_code1, new_code2)
            ("T", "LIT-CAMERER", "metatheory"): ("CAM", "MTA"),
            ("Y", "LIT-", "capital"): ("CIA", "CAP"),
            ("BB", "PAPAL", "EQUILIBRIA"): ("EQU", "EQU"),  # Special case: will handle
            ("X", "FORMAL-FOUND", "milgrom"): ("FND", "MIL"),
            ("AN", "llm_monte_carlo_final", None): ("LLM", "LLM"),  # Same code
            ("AZ", "PAPAL", "method_construct"): ("MCD", "MCD"),  # Same code
            ("AY", "PAPAL", "paradigms"): ("PAR", "PAR"),  # Same code
            ("AG", "LIT-AG", "complexity"): ("SHA", "CMX"),
            ("AD", "LIT-AD", "evolutionary"): ("SPC", "EVO"),
            ("S", "LIT-SUNSTEIN", "predictions"): ("SUN", "PRM"),
            ("HHH", "METHOD-TOOLKIT", "REF-SEGMENTATION"): ("TKT", "TKT"),  # Same code
            ("V", "THEORY-MEP", "psi_dimensions"): ("CTW", "WEN"),  # Special: contexts
            ("BBB", "estimation_methodology", "parameter_estimation"): ("WHERE", "WHERE"),  # Same code
        }

    def resolve_duplicate(self, old_code, entries):
        """Resolve which new code each entry should get"""

        if len(entries) == 1:
            return entries

        print(f"\n📊 Resolving {old_code} ({len(entries)} entries):")

        # Try pattern-based matching
        for (code, marker1, marker2), (new1, new2) in self.duplicate_handlers.items():
            if code != old_code:
                continue

            # Match first entry
            if marker1 and marker1.lower() in entries[0]["old_filename"].lower():
                entries[0]["new_code"] = new1
                print(f"  ✅ {entries[0]['old_filename']:50s} → {new1}")
                if len(entries) > 1:
                    entries[1]["new_code"] = new2
                    print(f"  ✅ {entries[1]['old_filename']:50s} → {new2}")
                return entries

            # Try reverse
            if marker2 and marker2.lower() in entries[0]["old_filename"].lower():
                entries[0]["new_code"] = new2
                print(f"  ✅ {entries[0]['old_filename']:50s} → {new2}")
                if len(entries) > 1:
                    entries[1]["new_code"] = new1
                    print(f"  ✅ {entries[1]['old_filename']:50s} → {new1}")
                return entries

        # Generic fallback: add suffix
        print(f"  ⚠️  Using fallback strategy (adding suffix)")
        for i, entry in enumerate(entries):
            entry["new_code"] = f"{entries[0]['new_code']}{i+1}"
            print(f"  → {entry['old_filename']:50s} → {entry['new_code']}")

        return entries

    def map_vvv_codes(self):
        """Handle 6 VVV files - they need new codes"""

        vvv_entries = [e for e in self.registry if e["old_code"] == "VVV"]

        print(f"\n📊 Handling VVV codes ({len(vvv_entries)} files):")
        print("   Files:")
        for i, entry in enumerate(vvv_entries, 1):
            print(f"     {i}. {entry['old_filename']}")

        # Assign new codes based on content
        vvv_codes = ["VVV", "VVV2", "VVV3", "VVV4", "VVV5", "VVV6"]

        for i, entry in enumerate(vvv_entries):
            if i < len(vvv_codes):
                entry["new_code"] = vvv_codes[i]
                entry["new_filename"] = entry["old_filename"].replace("VVV_", f"{vvv_codes[i]}_", 1)
                print(f"   ✅ {entry['old_filename']:50s} → {vvv_codes[i]}")

    def map_unmapped_codes(self):
        """Map remaining unmapped codes"""

        print(f"\n📊 Mapping unmapped codes:")

        unmapped_map = {
            "AM": "GCR",      # LIT-GAECHTER → LIT-COOPERATION-RECIPROCITY
            "BJ": "STC",      # FORMAL-STRATEGY-COMPARISON
            "DOMAIN-CONSULTING": "BHC",  # Already mapped in normal flow
            "EV": "EXP",      # Experimental evidence
            "LIT-META": "MSC",  # Metascience
            "LIT-THERMODYNAMICS": "THM",  # Thermodynamics
            "METHOD-TRACKING": "TRK",  # Tracking
            "QQQ": "QLY",     # Quality assessment
            "REF-APPLY": "APL",  # Apply reference
            "REF-CASES": "CAS",  # Cases reference
            "VVV1": "VVV7",    # VVV variant
        }

        for entry in self.registry:
            code = entry["old_code"]
            if code in unmapped_map:
                new_code = unmapped_map[code]
                entry["new_code"] = new_code
                entry["new_filename"] = entry["old_filename"].replace(f"{code}_", f"{new_code}_", 1)
                print(f"  ✅ {code:20s} → {new_code:10s} ({entry['old_filename']})")

    def resolve_conflicts(self):
        """Main method to resolve all conflicts"""

        print("=" * 80)
        print("INTELLIGENT APPENDIX MAPPING")
        print("=" * 80)

        # Group by old code
        by_old_code = defaultdict(list)
        for entry in self.registry:
            by_old_code[entry["old_code"]].append(entry)

        # Resolve duplicates
        duplicates = {k: v for k, v in by_old_code.items() if len(v) > 1}

        for old_code in sorted(duplicates.keys()):
            entries = duplicates[old_code]
            self.resolve_duplicate(old_code, entries)

        # Handle VVV specially
        self.map_vvv_codes()

        # Map unmapped
        self.map_unmapped_codes()

        # Save result
        with open(self.registry_file, 'w') as f:
            json.dump(self.registry, f, indent=2)

        print(f"\n✅ Updated registry saved")

        # Validate result
        self.validate_result()

    def validate_result(self):
        """Validate that all conflicts are resolved"""

        print("\n" + "=" * 80)
        print("VALIDATION AFTER MAPPING")
        print("=" * 80)

        # Check for remaining conflicts
        new_codes = defaultdict(list)
        for entry in self.registry:
            new_codes[entry["new_code"]].append(entry)

        conflicts = {k: v for k, v in new_codes.items() if len(v) > 1}
        unmapped = [e for e in self.registry if "UNMAPPED_" in e["new_code"]]

        if conflicts:
            print(f"\n🔴 {len(conflicts)} Remaining conflicts:")
            for new_code, entries in sorted(conflicts.items()):
                print(f"   {new_code}: {len(entries)} files")
        else:
            print(f"\n✅ NO CONFLICTS - All new codes are unique!")

        if unmapped:
            print(f"\n🔴 {len(unmapped)} Unmapped codes:")
            for entry in unmapped:
                print(f"   {entry['old_code']} in {entry['old_filename']}")
        else:
            print(f"\n✅ NO UNMAPPED CODES - All codes have mappings!")

        # Summary
        print(f"\n📊 Summary:")
        print(f"   Total appendices: {len(self.registry)}")
        print(f"   Unique old codes: {len(set(e['old_code'] for e in self.registry))}")
        print(f"   Unique new codes: {len(set(e['new_code'] for e in self.registry))}")

        return len(conflicts) == 0 and len(unmapped) == 0

def main():
    mapper = IntelligentAppendixMapper()
    mapper.resolve_conflicts()

if __name__ == '__main__':
    main()
