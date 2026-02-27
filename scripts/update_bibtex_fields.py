#!/usr/bin/env python3
"""
Update BibTeX Fields - Add use_for and theory_support to bcm_master.bib.

This script uses a line-by-line approach to safely add fields to entries.

Usage:
    python scripts/update_bibtex_fields.py
    python scripts/update_bibtex_fields.py --dry-run

Author: EBF Team
Version: 1.0.0
"""

import argparse
import re
from collections import defaultdict

BIBTEX_PATH = 'bibliography/bcm_master.bib'

# Author to LIT-Appendix mapping
AUTHOR_LIT_MAPPING = {
    'fehr': 'LIT-FEH',
    'thaler': 'LIT-KT',
    'kahneman': 'LIT-KT',
    'tversky': 'LIT-KT',
    'ariely': 'LIT-O',
    'camerer': 'LIT-O',
    'loewenstein': 'LIT-O',
    'sutter': 'LIT-SUT',
    'enke': 'LIT-ENK',
    'gneezy': 'LIT-O',
    'list': 'LIT-O',
    'duflo': 'LIT-O',
    'charness': 'LIT-O',
    'rabin': 'LIT-O',
    'laibson': 'LIT-O',
    'mullainathan': 'LIT-O',
    'shafir': 'LIT-O',
    'sunstein': 'LIT-O',
    'benartzi': 'LIT-O',
}

# Keywords to domain mapping
KEYWORD_DOMAIN_MAPPING = {
    'loss aversion': ['CORE-HOW', 'LIT-KT'],
    'prospect theory': ['CORE-HOW', 'LIT-KT'],
    'social preference': ['CORE-WHO', 'LIT-FEH'],
    'fairness': ['CORE-WHO', 'LIT-FEH'],
    'reciprocity': ['CORE-WHO', 'LIT-FEH'],
    'trust': ['CORE-WHO'],
    'cooperation': ['CORE-WHO'],
    'nudge': ['DOMAIN-POLICY'],
    'default': ['CONTEXT-DEFAULT'],
    'framing': ['CORE-HOW', 'LIT-KT'],
    'mental accounting': ['CORE-WHAT', 'LIT-KT'],
    'overconfidence': ['CORE-AWARE'],
    'experiment': ['METHOD-EXP'],
    'health': ['DOMAIN-HEALTH'],
    'retirement': ['DOMAIN-FINANCE'],
    'saving': ['DOMAIN-FINANCE'],
    'climate': ['DOMAIN-ENV'],
    'energy': ['DOMAIN-ENV'],
    'education': ['DOMAIN-EDU'],
}

# Theory support mapping - Expanded (100+ keywords mapped to MS-IDs)
KEYWORD_THEORY_MAPPING = {
    # Classical Economics (MS-CL)
    'general equilibrium': 'MS-CL-001',
    'expected utility': 'MS-CL-002',
    'rational expectation': 'MS-CL-003',
    'permanent income': 'MS-CL-004',
    'life-cycle': 'MS-CL-005',
    'lifecycle': 'MS-CL-005',
    'efficient market': 'MS-CL-006',
    'capm': 'MS-CL-007',
    'capital asset pricing': 'MS-CL-007',
    'ricardian': 'MS-CL-008',
    'coase theorem': 'MS-CL-009',
    'modigliani-miller': 'MS-CL-010',
    'homo economicus': 'MS-CL-011',
    'revealed preference': 'MS-CL-012',

    # Social Preferences (MS-SP)
    'inequity aversion': 'MS-SP-001',
    'fairness': 'MS-SP-001',
    'inequality aversion': 'MS-SP-001',
    'erc model': 'MS-SP-002',
    'altruism': 'MS-SP-003',
    'altruistic': 'MS-SP-003',
    'warm glow': 'MS-SP-004',
    'public good': 'MS-SP-004',
    'reciprocity': 'MS-SP-005',
    'reciprocal': 'MS-SP-005',
    'guilt aversion': 'MS-SP-006',
    'guilt': 'MS-SP-006',
    'social image': 'MS-SP-007',
    'reputation': 'MS-SP-007',
    'conditional cooperation': 'MS-SP-008',
    'strong reciprocity': 'MS-SP-009',
    'punishment': 'MS-SP-009',
    'spite': 'MS-SP-010',
    'other-regarding': 'MS-SP-011',
    'social welfare': 'MS-SP-012',
    'procedural fairness': 'MS-SP-013',
    'lying aversion': 'MS-SP-014',
    'moral wiggle room': 'MS-SP-015',
    'cooperation': 'MS-SP-016',

    # Reference-Dependent (MS-RD)
    'prospect theory': 'MS-RD-001',
    'loss aversion': 'MS-RD-001',
    'cumulative prospect': 'MS-RD-002',
    'endowment effect': 'MS-RD-003',
    'status quo bias': 'MS-RD-004',
    'mental accounting': 'MS-RD-005',
    'disposition effect': 'MS-RD-006',
    'reference-dependent': 'MS-RD-007',
    'reference dependent': 'MS-RD-007',
    'house money effect': 'MS-RD-008',
    'sunk cost': 'MS-RD-009',
    'narrow bracketing': 'MS-RD-010',

    # Time Preferences (MS-TP)
    'quasi-hyperbolic': 'MS-TP-001',
    'beta-delta': 'MS-TP-001',
    'present bias': 'MS-TP-001',
    'hyperbolic discount': 'MS-TP-002',
    'temptation': 'MS-TP-003',
    'self-control': 'MS-TP-003',
    'dual-self': 'MS-TP-004',
    'sophistication': 'MS-TP-005',
    'naivete': 'MS-TP-005',
    'projection bias': 'MS-TP-006',
    'commitment device': 'MS-TP-007',
    'pre-commitment': 'MS-TP-007',
    'procrastination': 'MS-TP-008',
    'rational addiction': 'MS-TP-009',
    'magnitude effect': 'MS-TP-010',

    # Identity & Beliefs (MS-IB)
    'identity economics': 'MS-IB-001',
    'self-image': 'MS-IB-002',
    'motivated belief': 'MS-IB-003',
    'motivated reasoning': 'MS-IB-003',
    'ego utility': 'MS-IB-004',
    'confirmation bias': 'MS-IB-005',
    'wishful thinking': 'MS-IB-006',
    'self-serving belief': 'MS-IB-007',
    'overoptimism': 'MS-IB-008',
    'optimism bias': 'MS-IB-008',
    'moral licensing': 'MS-IB-009',
    'cognitive dissonance': 'MS-IB-010',

    # Heuristics & Biases (MS-BF)
    'overconfidence': 'MS-BF-001',
    'availability heuristic': 'MS-BF-002',
    'availability bias': 'MS-BF-002',
    'anchoring': 'MS-BF-003',
    'framing effect': 'MS-BF-005',
    'framing': 'MS-BF-005',
    'representativeness': 'MS-BF-006',
    'base rate neglect': 'MS-BF-007',
    'gambler fallacy': 'MS-BF-008',
    'hot hand': 'MS-BF-009',
    'hindsight bias': 'MS-BF-010',
    'conjunction fallacy': 'MS-BF-011',
    'planning fallacy': 'MS-BF-012',

    # Nudge & Choice Architecture (MS-NU)
    'default effect': 'MS-NU-001',
    'nudge': 'MS-NU-001',
    'choice architecture': 'MS-NU-002',
    'libertarian paternalism': 'MS-NU-003',
    'simplification': 'MS-NU-004',
    'social norm': 'MS-NU-005',
    'peer effect': 'MS-NU-005',
    'feedback': 'MS-NU-006',
    'salience': 'MS-NU-007',
    'attention': 'MS-NU-007',
    'precommitment': 'MS-NU-008',
    'opt-in': 'MS-NU-009',
    'opt-out': 'MS-NU-009',

    # Motivation (MS-MO)
    'crowding out': 'MS-MO-001',
    'motivation crowding': 'MS-MO-001',
    'intrinsic motivation': 'MS-MO-002',
    'extrinsic motivation': 'MS-MO-003',
    'incentive': 'MS-MO-003',
    'self-determination': 'MS-MO-004',
    'autonomy': 'MS-MO-004',
    'signaling': 'MS-MO-005',

    # Wellbeing (MS-WB)
    'subjective well-being': 'MS-WB-001',
    'hedonic adaptation': 'MS-WB-002',
    'easterlin paradox': 'MS-WB-003',
    'aspiration': 'MS-WB-004',
    'satisfaction': 'MS-WB-005',
    'focusing illusion': 'MS-WB-006',

    # Development (MS-DV)
    'scarcity': 'MS-DV-001',
    'poverty trap': 'MS-DV-002',
    'cash transfer': 'MS-DV-005',
    'graduation program': 'MS-DV-006',

    # Causal/Econometric (MS-RCM, MS-HTE, MS-MTE)
    'potential outcome': 'MS-RCM-001',
    'causal inference': 'MS-RCM-001',
    'heterogeneous treatment': 'MS-HTE-001',
    'marginal treatment effect': 'MS-MTE-001',
    'self-selection': 'MS-MTE-002',

    # Time Allocation (MS-TA)
    'time allocation': 'MS-TA-001',
    'time use': 'MS-TA-001',
    'time-intensive': 'MS-TA-002',
    'attention economy': 'MS-TA-003',

    # Labor Markets (MS-LM)
    'place-based': 'MS-LM-001',
    'immigration': 'MS-LM-002',
    'local labor market': 'MS-LM-003',
    'temporary migration': 'MS-LM-004',
}


def determine_use_for(title: str, author: str) -> str:
    """Determine use_for value."""
    use_for = set()

    author_lower = author.lower() if author else ''
    for author_key, lit_appendix in AUTHOR_LIT_MAPPING.items():
        if author_key in author_lower:
            use_for.add(lit_appendix)

    title_lower = title.lower() if title else ''
    for keyword, domains in KEYWORD_DOMAIN_MAPPING.items():
        if keyword in title_lower:
            use_for.update(domains)

    if not use_for:
        use_for.add('LIT-O')

    return ', '.join(sorted(use_for))


def determine_theory_support(title: str) -> str:
    """Determine theory_support value."""
    theories = set()

    title_lower = title.lower() if title else ''
    for keyword, theory_id in KEYWORD_THEORY_MAPPING.items():
        if keyword in title_lower:
            theories.add(theory_id)

    return ', '.join(sorted(theories)) if theories else ''


def process_bibtex(dry_run: bool = False):
    """Process BibTeX file and add missing fields."""

    with open(BIBTEX_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    stats = {
        'use_for_added': 0,
        'theory_added': 0,
        'entries': 0
    }

    current_entry = {}
    in_entry = False
    entry_lines = []

    for i, line in enumerate(lines):
        # Detect entry start
        entry_match = re.match(r'@(\w+)\s*\{\s*([^,]+)\s*,', line)
        if entry_match:
            # Process previous entry if exists
            if in_entry and entry_lines:
                new_lines.extend(entry_lines)

            in_entry = True
            entry_lines = [line]
            current_entry = {
                'type': entry_match.group(1).lower(),
                'key': entry_match.group(2).strip(),
                'title': '',
                'author': '',
                'has_use_for': False,
                'has_theory': False
            }
            stats['entries'] += 1
            continue

        if in_entry:
            entry_lines.append(line)

            # Check for field values
            field_match = re.match(r'\s*(\w+)\s*=\s*\{(.+?)\}', line)
            if field_match:
                field_name = field_match.group(1).lower()
                field_value = field_match.group(2)

                if field_name == 'title':
                    current_entry['title'] = field_value
                elif field_name == 'author':
                    current_entry['author'] = field_value
                elif field_name == 'use_for':
                    current_entry['has_use_for'] = True
                elif field_name == 'theory_support':
                    current_entry['has_theory'] = True

            # Detect entry end (closing brace at start of line)
            if line.strip() == '}':
                # Add missing fields before closing brace
                fields_to_add = []

                if not current_entry['has_use_for']:
                    use_for = determine_use_for(current_entry['title'], current_entry['author'])
                    fields_to_add.append(f'  use_for = {{{use_for}}}')
                    stats['use_for_added'] += 1

                if not current_entry['has_theory']:
                    theory = determine_theory_support(current_entry['title'])
                    if theory:
                        fields_to_add.append(f'  theory_support = {{{theory}}}')
                        stats['theory_added'] += 1

                if fields_to_add:
                    # Insert fields before closing brace
                    entry_lines = entry_lines[:-1]  # Remove closing brace
                    # Ensure comma on last existing field
                    if entry_lines and not entry_lines[-1].rstrip().endswith(','):
                        last_line = entry_lines[-1].rstrip()
                        if last_line and last_line != '{':
                            entry_lines[-1] = last_line + ',\n'

                    for field in fields_to_add:
                        entry_lines.append(field + ',\n')
                    entry_lines.append('}\n')

                new_lines.extend(entry_lines)
                in_entry = False
                entry_lines = []
        else:
            new_lines.append(line)

    # Handle last entry if file doesn't end with newline
    if in_entry and entry_lines:
        new_lines.extend(entry_lines)

    # Summary
    print(f"\n📊 Processing Summary:")
    print(f"   Entries processed:     {stats['entries']}")
    print(f"   use_for added:         {stats['use_for_added']}")
    print(f"   theory_support added:  {stats['theory_added']}")

    if dry_run:
        print(f"\n⚠️  Dry run - no changes written")
        print(f"   Run without --dry-run to apply changes")
    else:
        with open(BIBTEX_PATH, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f"\n✅ Updated {BIBTEX_PATH}")


def main():
    parser = argparse.ArgumentParser(description='Update BibTeX fields')
    parser.add_argument('--dry-run', action='store_true', help='Show changes without applying')
    args = parser.parse_args()

    print("=" * 70)
    print("UPDATE BIBTEX FIELDS")
    print("=" * 70)

    process_bibtex(dry_run=args.dry_run)


if __name__ == '__main__':
    main()
