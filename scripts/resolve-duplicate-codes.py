#!/usr/bin/env python3
"""
Manually resolve duplicate codes in registry
Strategy: Assign new unique codes to duplicate entries
"""

import json
from pathlib import Path

def resolve_duplicates():
    """Resolve 7 duplicate codes"""

    registry_file = Path("/home/user/complementarity-context-framework/migration-audit/appendix-registry.json")

    with open(registry_file, 'r') as f:
        registry = json.load(f)

    print("=" * 80)
    print("RESOLVING DUPLICATE CODES")
    print("=" * 80)

    # Define manual resolutions for each duplicate
    resolutions = {
        "BHC": [
            {"filename": "AH_temporal_context.tex", "new_code": "CTM"},
            {"filename": "DOMAIN-CONSULTING_behavioral_consulting.tex", "new_code": "BHC"}
        ],
        "EQU": [
            {"filename": "BB_DOMAIN-PAPAL-APPOINTMENTS.tex", "new_code": "PAP"},
            {"filename": "BB_FORMAL-INTERVENTION-EQUILIBRIA.tex", "new_code": "EQU"}
        ],
        "FND": [
            {"filename": "X_FORMAL-FOUND_mathematical_foundations_complementarity.tex", "new_code": "FND"},
            {"filename": "X_LIT-LOEWENSTEIN_loewenstein_research.tex", "new_code": "LOE"},
            {"filename": "X_milgrom_roberts.tex", "new_code": "MIL"}
        ],
        "MCD": [
            {"filename": "AZ_PAPAL-HISTORICAL-ANALYSIS.tex", "new_code": "PAP2"},
            {"filename": "AZ_method_construct.tex", "new_code": "MCD"}
        ],
        "PAR": [
            {"filename": "AY_PAPAL-SUCCESSION-FRAMEWORK.tex", "new_code": "PAP3"},
            {"filename": "AY_paradigms.tex", "new_code": "PAR"}
        ],
        "TKT": [
            {"filename": "HHH_METHOD-TOOLKIT.tex", "new_code": "TKT"},
            {"filename": "HHH_REF-SEGMENTATION-HEURISTICS.tex", "new_code": "SEG"}
        ],
        "WHERE": [
            {"filename": "BBB_estimation_methodology.tex", "new_code": "EST"},
            {"filename": "BBB_parameter_estimation.tex", "new_code": "WHERE"}
        ],
        "VVV": [
            {"filename": "VVV_0_technology_landscape.tex", "new_code": "VVV"},
            {"filename": "VVV_1_technological_roadmap.tex", "new_code": "VVV2"},
            {"filename": "VVV_2_strategic_positioning.tex", "new_code": "VVV3"},
            {"filename": "VVV_3_product_options.tex", "new_code": "VVV4"},
            {"filename": "VVV_4_productizing_journey.tex", "new_code": "VVV5"},
            {"filename": "VVV_business_model.tex", "new_code": "VVV6"}
        ]
    }

    # Apply resolutions
    changes = 0
    for old_code, assignments in resolutions.items():
        print(f"\n📊 Resolving {old_code}:")
        for assignment in assignments:
            filename = assignment["filename"]
            new_code = assignment["new_code"]

            # Find entry in registry
            for entry in registry:
                if entry["old_filename"] == filename:
                    old_new_code = entry["new_code"]
                    entry["new_code"] = new_code
                    entry["new_filename"] = filename.replace(entry["old_code"] + "_", new_code + "_", 1)
                    print(f"   ✅ {filename}")
                    print(f"      {old_code} → {new_code}")
                    changes += 1
                    break

    # Validate
    print(f"\n" + "=" * 80)
    print("VALIDATION AFTER RESOLUTION")
    print("=" * 80)

    from collections import defaultdict
    new_codes = defaultdict(list)
    for entry in registry:
        new_codes[entry["new_code"]].append(entry)

    conflicts = {k: v for k, v in new_codes.items() if len(v) > 1}

    if conflicts:
        print(f"\n🔴 Still {len(conflicts)} conflicts:")
        for code, entries in conflicts.items():
            print(f"   {code}: {len(entries)} files")
    else:
        print(f"\n✅ NO CONFLICTS - All new codes are unique!")

    # Summary statistics
    unique_old = len(set(e["old_code"] for e in registry))
    unique_new = len(set(e["new_code"] for e in registry))

    print(f"\n📊 Summary:")
    print(f"   Total appendices: {len(registry)}")
    print(f"   Unique old codes: {unique_old}")
    print(f"   Unique new codes: {unique_new}")
    print(f"   Changes made: {changes}")

    # Save
    with open(registry_file, 'w') as f:
        json.dump(registry, f, indent=2)

    print(f"\n✅ Registry updated and saved")

    return len(conflicts) == 0

if __name__ == '__main__':
    success = resolve_duplicates()
    exit(0 if success else 1)
