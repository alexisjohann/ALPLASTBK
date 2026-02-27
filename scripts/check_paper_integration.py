#!/usr/bin/env python3
"""Check paper database integration quality (Dimension 2).

Measures how well papers are integrated into the EBF ecosystem:
- use_for: Links to LIT-XX, DOMAIN-XX, CORE-XX appendices
- theory_support: Links to MS-XX-XXX theories
- evidence_tier: Quality classification (1=Gold, 2=Silver, 3=Bronze)
- parameter: Extracted behavioral economics parameters
"""

import re
from pathlib import Path
from collections import defaultdict


def check_bibtex_integration():
    """Check integration fields in bcm_master.bib."""
    bib_path = Path("bibliography/bcm_master.bib")

    if not bib_path.exists():
        print("ERROR: bcm_master.bib not found")
        return None

    with open(bib_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Count total entries
    entries = re.findall(r'@\w+\{([^,]+),', content)
    total = len(entries)

    # Count integration fields
    use_for = len(re.findall(r'use_for\s*=', content))
    theory_support = len(re.findall(r'theory_support\s*=', content))
    evidence_tier = len(re.findall(r'evidence_tier\s*=', content))
    parameter = len(re.findall(r'parameter\s*=', content))

    # Extract use_for values to see distribution
    use_for_values = re.findall(r'use_for\s*=\s*\{([^}]+)\}', content)
    use_for_types = defaultdict(int)
    for val in use_for_values:
        for item in val.split(','):
            item = item.strip()
            if item.startswith('LIT-'):
                use_for_types['LIT'] += 1
            elif item.startswith('DOMAIN-'):
                use_for_types['DOMAIN'] += 1
            elif item.startswith('CORE-'):
                use_for_types['CORE'] += 1
            elif item.startswith('METHOD-'):
                use_for_types['METHOD'] += 1
            elif item.startswith('FORMAL-'):
                use_for_types['FORMAL'] += 1
            elif item.startswith('PREDICT-'):
                use_for_types['PREDICT'] += 1
            elif item.startswith('REF-'):
                use_for_types['REF'] += 1
            elif item.startswith('CONTEXT-'):
                use_for_types['CONTEXT'] += 1

    # Extract theory_support values
    theory_values = re.findall(r'theory_support\s*=\s*\{([^}]+)\}', content)
    theory_types = defaultdict(int)
    for val in theory_values:
        for item in val.split(','):
            item = item.strip()
            if item.startswith('MS-'):
                category = item.split('-')[1] if '-' in item else 'OTHER'
                theory_types[category] += 1

    return {
        'total': total,
        'use_for': use_for,
        'theory_support': theory_support,
        'evidence_tier': evidence_tier,
        'parameter': parameter,
        'use_for_types': dict(use_for_types),
        'theory_types': dict(theory_types)
    }


def check_yaml_integration():
    """Check integration in paper YAML files."""
    paper_dir = Path("data/paper-references")

    stats = {
        'total': 0,
        'with_case_links': 0,
        'with_model_links': 0,
        'with_intervention_links': 0
    }

    for yaml_file in paper_dir.glob("PAP-*.yaml"):
        stats['total'] += 1

        with open(yaml_file, 'r', encoding='utf-8') as f:
            content = f.read()

        if 'case_links:' in content or 'CAS-' in content:
            stats['with_case_links'] += 1
        if 'model_links:' in content or 'MOD-' in content:
            stats['with_model_links'] += 1
        if 'intervention_links:' in content or 'INT-' in content:
            stats['with_intervention_links'] += 1

    return stats


def print_bar(pct, width=20):
    """Print a progress bar."""
    filled = int(pct / 100 * width)
    bar = '█' * filled + '░' * (width - filled)
    return bar


def main():
    print("=" * 70)
    print("PAPER DATABASE INTEGRATION QUALITY (Dimension 2)")
    print("=" * 70)
    print()

    # BibTeX integration
    bib_stats = check_bibtex_integration()
    if bib_stats:
        total = bib_stats['total']

        print("BIBTEX INTEGRATION FIELDS:")
        print(f"  Total papers in bcm_master.bib: {total}")
        print()

        # Calculate percentages
        use_for_pct = bib_stats['use_for'] / total * 100
        theory_pct = bib_stats['theory_support'] / total * 100
        tier_pct = bib_stats['evidence_tier'] / total * 100
        param_pct = bib_stats['parameter'] / total * 100

        print(f"  use_for:        {print_bar(use_for_pct)} {use_for_pct:5.1f}% ({bib_stats['use_for']}/{total})")
        print(f"  theory_support: {print_bar(theory_pct)} {theory_pct:5.1f}% ({bib_stats['theory_support']}/{total})")
        print(f"  evidence_tier:  {print_bar(tier_pct)} {tier_pct:5.1f}% ({bib_stats['evidence_tier']}/{total})")
        print(f"  parameter:      {print_bar(param_pct)} {param_pct:5.1f}% ({bib_stats['parameter']}/{total})")
        print()

        # use_for distribution
        if bib_stats['use_for_types']:
            print("  use_for DISTRIBUTION:")
            for cat, count in sorted(bib_stats['use_for_types'].items(), key=lambda x: -x[1]):
                print(f"    {cat:12} → {count} papers")
            print()

        # theory_support distribution
        if bib_stats['theory_types']:
            print("  theory_support CATEGORIES:")
            for cat, count in sorted(bib_stats['theory_types'].items(), key=lambda x: -x[1])[:10]:
                print(f"    MS-{cat:8} → {count} papers")
            print()

    # YAML integration
    yaml_stats = check_yaml_integration()
    print("YAML CROSS-LINKS:")
    print(f"  Total YAML files: {yaml_stats['total']}")

    case_pct = yaml_stats['with_case_links'] / yaml_stats['total'] * 100
    model_pct = yaml_stats['with_model_links'] / yaml_stats['total'] * 100
    int_pct = yaml_stats['with_intervention_links'] / yaml_stats['total'] * 100

    print(f"  case_links:       {print_bar(case_pct)} {case_pct:5.1f}% ({yaml_stats['with_case_links']}/{yaml_stats['total']})")
    print(f"  model_links:      {print_bar(model_pct)} {model_pct:5.1f}% ({yaml_stats['with_model_links']}/{yaml_stats['total']})")
    print(f"  intervention:     {print_bar(int_pct)} {int_pct:5.1f}% ({yaml_stats['with_intervention_links']}/{yaml_stats['total']})")
    print()

    # Combined quality score
    print("=" * 70)
    print("INTEGRATION QUALITY SUMMARY:")
    print("=" * 70)

    # Weight: use_for most important, then theory, then tier
    if bib_stats:
        weighted_score = (
            use_for_pct * 0.40 +     # 40% weight
            theory_pct * 0.30 +       # 30% weight
            tier_pct * 0.20 +         # 20% weight
            param_pct * 0.10          # 10% weight
        )

        print(f"""
  ┌─────────────────────────────────────────────────────────────┐
  │  DIMENSION 2: INTEGRATION SCORE                             │
  │                                                             │
  │  use_for (40%):        {use_for_pct:5.1f}% → {use_for_pct * 0.4:5.1f} pts        │
  │  theory_support (30%): {theory_pct:5.1f}% → {theory_pct * 0.3:5.1f} pts        │
  │  evidence_tier (20%):  {tier_pct:5.1f}% → {tier_pct * 0.2:5.1f} pts        │
  │  parameter (10%):      {param_pct:5.1f}% → {param_pct * 0.1:5.1f} pts        │
  │  ─────────────────────────────────────────────────────────  │
  │  TOTAL INTEGRATION SCORE: {weighted_score:5.1f} / 100                  │
  └─────────────────────────────────────────────────────────────┘
        """)

        if weighted_score < 30:
            print("  STATUS: ❌ KRITISCH - Integration stark vernachlässigt")
        elif weighted_score < 50:
            print("  STATUS: ⚠️  WARNUNG - Integration unvollständig")
        elif weighted_score < 70:
            print("  STATUS: 📊 AKZEPTABEL - Integration im Aufbau")
        else:
            print("  STATUS: ✅ GUT - Integration funktioniert")

    print()


if __name__ == "__main__":
    main()
