#!/usr/bin/env python3
"""
Skill Gap Analysis & Transferability Computation

Computes skill gaps between person profiles and role requirements,
role-to-role transferability (cosine similarity), and development paths.

Uses the multi-tier skill architecture:
  Kaufland Roles → WEF Skills → O*NET Abilities → Bartram Factors

SSOT: data/skill-levels/
Reference: MOD-013 (KIBSM)

Usage:
  # List all roles
  python scripts/skill_gap_analysis.py --list-roles

  # Show role profile
  python scripts/skill_gap_analysis.py --role marktleiter

  # Compute transferability between two roles
  python scripts/skill_gap_analysis.py --transferability --from kassierer --to abteilungsleiter

  # Show development path (multi-step)
  python scripts/skill_gap_analysis.py --development-path --from verkaufsberater --to bezirksleiter

  # Compute skill gap for a person vs role
  python scripts/skill_gap_analysis.py --gap --role marktleiter --person-levels '{"leadership_social_influence":4,"analytical_thinking":3}'

  # Aggregate to Bartram factors
  python scripts/skill_gap_analysis.py --bartram --role marktleiter
"""

import argparse
import json
import math
import sys
from pathlib import Path

import yaml

BASE_DIR = Path(__file__).resolve().parent.parent
SKILL_DIR = BASE_DIR / "data" / "skill-levels"


def load_yaml(filename):
    path = SKILL_DIR / filename
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_roles():
    data = load_yaml("kaufland-role-profiles.yaml")
    return data["roles"]


def load_wef_to_onet():
    data = load_yaml("wef-to-onet-mapping.yaml")
    return data["skills"]


def load_bartram():
    data = load_yaml("bartram-factors.yaml")
    return data["factors"]


def load_level_scale():
    data = load_yaml("level-scale.yaml")
    return data["scale"]


def get_role_vector(role_data):
    """Extract skill-level vector from a role profile."""
    vec = {}
    for skill_key, skill_info in role_data.get("wef_skills", {}).items():
        vec[skill_key] = skill_info["level"]
    return vec


def cosine_similarity(vec_a, vec_b):
    """Compute cosine similarity between two skill vectors."""
    all_keys = set(vec_a.keys()) | set(vec_b.keys())
    if not all_keys:
        return 0.0

    dot = sum(vec_a.get(k, 0) * vec_b.get(k, 0) for k in all_keys)
    mag_a = math.sqrt(sum(v ** 2 for v in vec_a.values()))
    mag_b = math.sqrt(sum(v ** 2 for v in vec_b.values()))

    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


def compute_gap(role_vec, person_vec):
    """Compute skill gaps: positive = person exceeds, negative = development needed."""
    gaps = {}
    for skill, required in role_vec.items():
        current = person_vec.get(skill, 0)
        gaps[skill] = {
            "required": required,
            "current": current,
            "gap": current - required,
            "priority": classify_gap(current - required),
        }
    return gaps


def classify_gap(gap):
    if gap >= 0:
        return "met"
    elif gap >= -1:
        return "low"
    elif gap >= -2:
        return "medium"
    else:
        return "critical"


def gap_timeline(gap):
    if gap >= 0:
        return "—"
    elif gap >= -1:
        return "1-3 months"
    elif gap >= -2:
        return "3-12 months"
    else:
        return "12+ months"


def aggregate_to_bartram(role_vec, wef_to_onet, bartram_factors):
    """Aggregate WEF skill levels to Bartram Great Eight factors via O*NET."""
    onet_levels = {}
    onet_counts = {}

    for skill_key, level in role_vec.items():
        mapping = wef_to_onet.get(skill_key)
        if not mapping:
            continue
        for ability, loading in mapping.get("onet_loadings", {}).items():
            weighted = level * loading
            onet_levels[ability] = onet_levels.get(ability, 0) + weighted
            onet_counts[ability] = onet_counts.get(ability, 0) + loading

    for ability in onet_levels:
        if onet_counts[ability] > 0:
            onet_levels[ability] /= onet_counts[ability]

    bartram_scores = {}
    for factor_key, factor_data in bartram_factors.items():
        primary_abilities = factor_data.get("onet_abilities_primary", [])
        scores = [onet_levels.get(a, 0) for a in primary_abilities if a in onet_levels]
        if scores:
            bartram_scores[factor_key] = {
                "name": factor_data["name"],
                "level": round(sum(scores) / len(scores), 1),
                "abilities_used": len(scores),
            }
    return bartram_scores


def find_development_path(roles, start_role, target_role):
    """Find the career path from start to target role."""
    path = [start_role]
    current = start_role
    visited = {start_role}

    while current != target_role:
        role_data = roles.get(current)
        if not role_data:
            break
        next_role = role_data.get("next_role")
        if not next_role or next_role in visited:
            break
        path.append(next_role)
        visited.add(next_role)
        current = next_role

    if current != target_role:
        return None
    return path


def print_role_profile(role_key, role_data):
    print(f"\n{'=' * 60}")
    print(f"  {role_data['name']}")
    print(f"  ID: {role_data['id']}  |  Career: {role_data['karrierestufe']}")
    print(f"  Next role: {role_data.get('next_role', '—')}")
    print(f"{'=' * 60}")
    print(f"\n  {'Skill':<45} {'Level':>5}  {'Importance':>10}")
    print(f"  {'─' * 62}")

    for skill_key, skill_info in role_data.get("wef_skills", {}).items():
        name = skill_key.replace("_", " ").title()
        level = skill_info["level"]
        importance = skill_info["importance"]
        bar = "█" * level + "░" * (7 - level)
        print(f"  {name:<45} {bar} {level}  {'★' * importance}")


def print_gap_analysis(gaps, role_name):
    print(f"\n{'=' * 70}")
    print(f"  SKILL GAP ANALYSIS: {role_name}")
    print(f"{'=' * 70}")
    print(f"\n  {'Skill':<40} {'Req':>4} {'Cur':>4} {'Gap':>4}  {'Priority':<10} {'Timeline'}")
    print(f"  {'─' * 75}")

    sorted_gaps = sorted(gaps.items(), key=lambda x: x[1]["gap"])
    for skill_key, info in sorted_gaps:
        name = skill_key.replace("_", " ").title()[:38]
        gap = info["gap"]
        priority = info["priority"]
        timeline = gap_timeline(gap)

        marker = "✅" if gap >= 0 else ("⚠️ " if gap >= -1 else "❌")
        print(
            f"  {name:<40} {info['required']:>4} {info['current']:>4} {gap:>+4}  {marker} {priority:<8} {timeline}"
        )

    total_gaps = sum(1 for g in gaps.values() if g["gap"] < 0)
    critical = sum(1 for g in gaps.values() if g["priority"] == "critical")
    print(f"\n  Summary: {total_gaps} gaps ({critical} critical) out of {len(gaps)} skills")


def print_transferability(roles, from_key, to_key):
    from_data = roles[from_key]
    to_data = roles[to_key]
    vec_a = get_role_vector(from_data)
    vec_b = get_role_vector(to_data)
    sim = cosine_similarity(vec_a, vec_b)

    print(f"\n{'=' * 60}")
    print(f"  TRANSFERABILITY: {from_data['name']}")
    print(f"              →   {to_data['name']}")
    print(f"{'=' * 60}")
    print(f"\n  Cosine Similarity: {sim:.2f}")

    if sim >= 0.85:
        print(f"  Interpretation:    HIGH — minimal retraining needed")
    elif sim >= 0.70:
        print(f"  Interpretation:    MODERATE — targeted upskilling")
    elif sim >= 0.50:
        print(f"  Interpretation:    LOW — significant development needed")
    else:
        print(f"  Interpretation:    MINIMAL — different skill profiles")

    all_skills = set(vec_a.keys()) | set(vec_b.keys())
    print(f"\n  {'Skill':<40} {'From':>5} {'To':>5} {'Delta':>6}")
    print(f"  {'─' * 58}")

    diffs = []
    for skill in sorted(all_skills):
        a_val = vec_a.get(skill, 0)
        b_val = vec_b.get(skill, 0)
        diffs.append((skill, a_val, b_val, b_val - a_val))

    diffs.sort(key=lambda x: x[3])
    for skill, a_val, b_val, delta in diffs:
        name = skill.replace("_", " ").title()[:38]
        marker = "" if delta == 0 else ("↑" if delta > 0 else "↓")
        print(f"  {name:<40} {a_val:>5} {b_val:>5} {delta:>+5} {marker}")


def print_development_path(roles, path):
    print(f"\n{'=' * 70}")
    print(f"  DEVELOPMENT PATH: {roles[path[0]]['name']} → {roles[path[-1]]['name']}")
    print(f"{'=' * 70}")

    for i in range(len(path) - 1):
        from_key = path[i]
        to_key = path[i + 1]
        from_data = roles[from_key]
        to_data = roles[to_key]
        vec_a = get_role_vector(from_data)
        vec_b = get_role_vector(to_data)
        sim = cosine_similarity(vec_a, vec_b)

        print(f"\n  Step {i + 1}: {from_data['name']} → {to_data['name']}")
        print(f"  Transferability: {sim:.2f}")

        new_skills = []
        upgrade_skills = []
        for skill, level in vec_b.items():
            from_level = vec_a.get(skill, 0)
            if from_level == 0 and level > 0:
                new_skills.append((skill, level))
            elif level > from_level:
                upgrade_skills.append((skill, from_level, level))

        if new_skills:
            print(f"  NEW skills needed:")
            for skill, level in new_skills:
                name = skill.replace("_", " ").title()
                print(f"    + {name} (Level {level})")

        if upgrade_skills:
            print(f"  UPGRADE skills:")
            for skill, from_l, to_l in sorted(upgrade_skills, key=lambda x: x[1] - x[2]):
                name = skill.replace("_", " ").title()
                print(f"    ↑ {name}: {from_l} → {to_l} (+{to_l - from_l})")


def print_bartram(bartram_scores, role_name):
    print(f"\n{'=' * 60}")
    print(f"  BARTRAM GREAT EIGHT: {role_name}")
    print(f"{'=' * 60}")
    print(f"\n  {'Factor':<35} {'Level':>6}  {'Visual'}")
    print(f"  {'─' * 55}")

    for factor_key, info in sorted(bartram_scores.items(), key=lambda x: -x[1]["level"]):
        level = info["level"]
        bar = "█" * round(level) + "░" * (7 - round(level))
        print(f"  {info['name']:<35} {level:>5.1f}  {bar}")


def main():
    parser = argparse.ArgumentParser(description="Skill Gap Analysis & Transferability")
    parser.add_argument("--list-roles", action="store_true", help="List all Kaufland roles")
    parser.add_argument("--role", type=str, help="Show role profile")
    parser.add_argument("--transferability", action="store_true", help="Compute transferability")
    parser.add_argument("--from", dest="from_role", type=str, help="Source role")
    parser.add_argument("--to", dest="to_role", type=str, help="Target role")
    parser.add_argument("--development-path", action="store_true", help="Show development path")
    parser.add_argument("--gap", action="store_true", help="Compute skill gap")
    parser.add_argument("--person-levels", type=str, help="JSON dict of person skill levels")
    parser.add_argument("--bartram", action="store_true", help="Aggregate to Bartram factors")
    parser.add_argument("--all-transfers", action="store_true", help="Show full transferability matrix")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()
    roles = load_roles()

    if args.list_roles:
        print(f"\n  {'Key':<25} {'ID':<15} {'Name':<35} {'Level'}")
        print(f"  {'─' * 80}")
        for key, data in roles.items():
            print(f"  {key:<25} {data['id']:<15} {data['name']:<35} {data['karrierestufe']}")
        return

    if args.role and not args.gap and not args.bartram:
        if args.role not in roles:
            print(f"Error: Role '{args.role}' not found. Use --list-roles.", file=sys.stderr)
            sys.exit(1)
        print_role_profile(args.role, roles[args.role])
        return

    if args.transferability:
        if not args.from_role or not args.to_role:
            print("Error: --transferability requires --from and --to", file=sys.stderr)
            sys.exit(1)
        if args.from_role not in roles or args.to_role not in roles:
            print(f"Error: Role not found. Use --list-roles.", file=sys.stderr)
            sys.exit(1)
        print_transferability(roles, args.from_role, args.to_role)
        return

    if args.development_path:
        if not args.from_role or not args.to_role:
            print("Error: --development-path requires --from and --to", file=sys.stderr)
            sys.exit(1)
        path = find_development_path(roles, args.from_role, args.to_role)
        if not path:
            print(f"Error: No career path from {args.from_role} to {args.to_role}", file=sys.stderr)
            sys.exit(1)
        print_development_path(roles, path)
        return

    if args.gap:
        if not args.role or not args.person_levels:
            print("Error: --gap requires --role and --person-levels", file=sys.stderr)
            sys.exit(1)
        if args.role not in roles:
            print(f"Error: Role '{args.role}' not found.", file=sys.stderr)
            sys.exit(1)
        person_vec = json.loads(args.person_levels)
        role_vec = get_role_vector(roles[args.role])
        gaps = compute_gap(role_vec, person_vec)

        if args.json:
            print(json.dumps(gaps, indent=2))
        else:
            print_gap_analysis(gaps, roles[args.role]["name"])
        return

    if args.bartram:
        if not args.role:
            print("Error: --bartram requires --role", file=sys.stderr)
            sys.exit(1)
        if args.role not in roles:
            print(f"Error: Role '{args.role}' not found.", file=sys.stderr)
            sys.exit(1)
        wef_to_onet = load_wef_to_onet()
        bartram_factors = load_bartram()
        role_vec = get_role_vector(roles[args.role])
        scores = aggregate_to_bartram(role_vec, wef_to_onet, bartram_factors)

        if args.json:
            print(json.dumps(scores, indent=2))
        else:
            print_bartram(scores, roles[args.role]["name"])
        return

    if args.all_transfers:
        role_keys = list(roles.keys())
        print(f"\n  TRANSFERABILITY MATRIX (Cosine Similarity)")
        print(f"  {'':>20}", end="")
        for k in role_keys:
            short = k[:8]
            print(f" {short:>8}", end="")
        print()

        for from_key in role_keys:
            short = from_key[:20]
            print(f"  {short:>20}", end="")
            vec_a = get_role_vector(roles[from_key])
            for to_key in role_keys:
                vec_b = get_role_vector(roles[to_key])
                sim = cosine_similarity(vec_a, vec_b)
                print(f" {sim:>8.2f}", end="")
            print()
        return

    parser.print_help()


if __name__ == "__main__":
    main()
