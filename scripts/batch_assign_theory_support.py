#!/usr/bin/env python3
"""
Batch-assign theory_support to BibTeX entries missing it.

Three-stage matching:
  Stage 1: Keyword matching on title/abstract/keywords fields
  Stage 2: use_for DOMAIN tag → Theory defaults
  Stage 3: LIT-Author tag → Author's primary theory (conservative)

Usage:
    python scripts/batch_assign_theory_support.py --dry-run [--limit N]
    python scripts/batch_assign_theory_support.py [--limit N]
    python scripts/batch_assign_theory_support.py --stats
"""

import re
import sys
import os

BIB_PATH = os.path.join(os.path.dirname(__file__), '..', 'bibliography', 'bcm_master.bib')

# ─────────────────────────────────────────────────────────────────────
# STAGE 1: Keyword → Theory mapping (title/abstract/keywords matching)
# Extended from enrich_existing_papers.py KEYWORD_THEORY_MAPPING
# ─────────────────────────────────────────────────────────────────────

KEYWORD_THEORY_MAP = {
    # ── Reference Dependence (CAT-03) ──
    'prospect theory': 'MS-RD-001',
    'loss aversion': 'MS-RD-001',
    'reference point': 'MS-RD-001',
    'reference dependent': 'MS-RD-001',
    'probability weighting': 'MS-RD-001',
    'endowment effect': 'MS-RD-002',
    'status quo bias': 'MS-RD-002',
    'willingness to pay': 'MS-RD-002',
    'willingness to accept': 'MS-RD-002',
    'mental accounting': 'MS-RD-007',
    'narrow framing': 'MS-RD-007',
    'fungibility': 'MS-RD-007',
    'hedonic editing': 'MS-RD-007',

    # ── Social Preferences (CAT-02) ──
    'inequity aversion': 'MS-SP-001',
    'inequality aversion': 'MS-SP-001',
    'fairness concern': 'MS-SP-001',
    'fair allocation': 'MS-SP-001',
    'distributional preference': 'MS-SP-001',
    'reciprocity': 'MS-SP-002',
    'trust game': 'MS-SP-002',
    'conditional cooperation': 'MS-SP-002',
    'gift exchange': 'MS-SP-002',
    'altruism': 'MS-SP-003',
    'warm glow': 'MS-SP-004',
    'public good': 'MS-SP-004',
    'free rid': 'MS-SP-004',
    'cooperation': 'MS-SP-004',
    'voluntary contribution': 'MS-SP-004',
    'charitable giving': 'MS-SP-004',
    'social norm': 'MS-SP-004',
    'social preference': 'MS-SP-004',
    'prosocial': 'MS-SP-004',
    'ultimatum game': 'MS-SP-001',
    'dictator game': 'MS-SP-003',
    'punishment': 'MS-SP-009',
    'strong reciprocity': 'MS-SP-009',
    'third-party punishment': 'MS-SP-009',

    # ── Identity & Beliefs (CAT-05) ──
    'identity': 'MS-IB-001',
    'social identity': 'MS-IB-001',
    'in-group': 'MS-IB-001',
    'out-group': 'MS-IB-001',
    'self-image': 'MS-IB-001',
    'motivated belief': 'MS-MO-003',
    'motivated reasoning': 'MS-MO-003',
    'self-deception': 'MS-MO-003',
    'wishful thinking': 'MS-MO-003',
    'overconfidence': 'MS-IB-002',
    'optimism bias': 'MS-IB-002',
    'belief updating': 'MS-IB-003',

    # ── Time Preferences (CAT-04) ──
    'hyperbolic discount': 'MS-TP-001',
    'present bias': 'MS-TP-001',
    'quasi-hyperbolic': 'MS-TP-001',
    'time inconsisten': 'MS-TP-001',
    'commitment device': 'MS-TP-001',
    'procrastinat': 'MS-TP-001',
    'self-control': 'MS-TP-003',
    'temptation': 'MS-TP-003',
    'willpower': 'MS-TP-003',
    'patience': 'MS-TP-001',
    'impatien': 'MS-TP-001',
    'delay discount': 'MS-TP-001',
    'exponential discount': 'MS-TP-002',
    'intertemporal choice': 'MS-TP-001',

    # ── Nudge & Choice Architecture (CAT-10) ──
    'nudg': 'MS-NU-001',
    'libertarian paternalism': 'MS-NU-001',
    'choice architect': 'MS-NU-001',
    'default effect': 'MS-NU-002',
    'opt-out': 'MS-NU-002',
    'opt-in': 'MS-NU-002',
    'automatic enrollment': 'MS-NU-002',
    'active choice': 'MS-NU-002',
    'simplif': 'MS-NU-003',
    'disclosure': 'MS-NU-004',

    # ── Behavioral Finance (CAT-09) ──
    'limits to arbitrage': 'MS-BF-001',
    'anomal': 'MS-BF-001',
    'equity premium': 'MS-BF-004',
    'myopic loss aversion': 'MS-BF-004',
    'disposition effect': 'MS-BF-005',
    'sunk cost': 'MS-BF-006',
    'escalation of commitment': 'MS-BF-006',
    'hindsight bias': 'MS-BF-007',
    'confirmation bias': 'MS-BF-008',
    'bubble': 'MS-BF-001',
    'market efficiency': 'MS-CL-002',
    'asset pricing': 'MS-CL-003',

    # ── Heuristics & Biases ──
    'availability heuristic': 'MS-RD-001',
    'representativeness': 'MS-RD-001',
    'anchoring': 'MS-RD-001',
    'framing effect': 'MS-RD-001',
    'heuristic': 'MS-RD-001',
    'bounded rationality': 'MS-RD-001',

    # ── Neuroeconomics (CAT-11) ──
    'dual-system': 'MS-NE-001',
    'system 1': 'MS-NE-001',
    'system 2': 'MS-NE-001',
    'thinking, fast': 'MS-NE-001',
    'visceral': 'MS-NE-003',
    'hot-cold': 'MS-NE-003',
    'empathy gap': 'MS-NE-003',
    'neuroeconom': 'MS-NE-001',

    # ── Institutions (CAT-06) ──
    'institution': 'MS-IN-001',
    'transaction cost': 'MS-IN-002',
    'property right': 'MS-IN-003',
    'contract theory': 'MS-IN-004',
    'principal-agent': 'MS-IN-004',
    'moral hazard': 'MS-IF-003',
    'adverse selection': 'MS-IF-002',
    'asymmetric information': 'MS-IF-001',
    'signaling': 'MS-IF-001',
    'screening': 'MS-IF-002',

    # ── Strategic Interaction (CAT-08) ──
    'game theory': 'MS-SI-001',
    'nash equilibrium': 'MS-SI-001',
    'auction': 'MS-SI-002',
    'mechanism design': 'MS-SI-003',
    'bargaining': 'MS-SI-004',
    'coordination game': 'MS-SI-005',
    'beauty contest': 'MS-SI-006',

    # ── Wellbeing (CAT-12) ──
    'subjective well-being': 'MS-WB-001',
    'life satisfaction': 'MS-WB-001',
    'happiness': 'MS-WB-001',
    'easterlin': 'MS-WB-001',
    'hedonic treadmill': 'MS-WB-002',
    'hedonic adaptation': 'MS-WB-002',

    # ── Labor & Migration (CAT-20) ──
    'immigra': 'MS-LM-001',
    'emigra': 'MS-LM-001',
    'migrant': 'MS-LM-001',
    'refugee': 'MS-LM-001',
    'asylum': 'MS-LM-001',
    'minimum wage': 'MS-LM-002',
    'monopsony': 'MS-LM-002',
    'labor market': 'MS-LM-002',
    'labour market': 'MS-LM-002',
    'place-based polic': 'MS-LM-001',
    'spatial equilibrium': 'MS-LM-001',

    # ── Skill Formation (CAT-19) ──
    'skill formation': 'MS-SF-001',
    'human capital': 'MS-SF-001',
    'early childhood': 'MS-SF-001',
    'returns to education': 'MS-SF-001',
    'complementarity of investment': 'MS-SF-002',
    'dynamic complementarity': 'MS-SF-002',

    # ── Causal Inference (CAT-14) ──
    'causal inference': 'MS-HTE-001',
    'heterogeneous treatment': 'MS-HTE-001',
    'instrumental variable': 'MS-HTE-001',
    'regression discontinuity': 'MS-HTE-001',
    'difference-in-difference': 'MS-HTE-001',
    'natural experiment': 'MS-HTE-001',
    'randomized control': 'MS-HTE-001',

    # ── Motivation (CAT-11/05) ──
    'intrinsic motivation': 'MS-MO-001',
    'extrinsic motivation': 'MS-MO-001',
    'crowding out': 'MS-MO-001',
    'crowding-out': 'MS-MO-001',
    'overjustification': 'MS-MO-001',
    'self-determination': 'MS-MO-002',
    'autonomy': 'MS-MO-002',

    # ── Political Psychology (CAT-21) ──
    'populis': 'MS-PP-001',
    'right-wing authoritarian': 'MS-PP-002',
    'social dominance': 'MS-PP-003',
    'political polariz': 'MS-PP-004',
    'voting behavior': 'MS-PP-001',
    'voter turnout': 'MS-PP-001',
    'political economy': 'MS-PP-001',

    # ── Development & Poverty (CAT-13) ──
    'poverty trap': 'MS-DV-001',
    'scarcity': 'MS-DV-002',
    'cash transfer': 'MS-DV-003',
    'microfinance': 'MS-DV-004',
    'developing countr': 'MS-DV-001',

    # ── Extended: Information Economics ──
    'imperfect information': 'MS-IF-001',
    'incomplete market': 'MS-IF-001',
    'incomplete information': 'MS-IF-001',
    'credit ration': 'MS-IF-001',
    'insurance market': 'MS-IF-002',
    'information asymmetr': 'MS-IF-001',

    # ── Extended: Labor Economics ──
    'wage': 'MS-LM-002',
    'unemployment': 'MS-LM-002',
    'job search': 'MS-LM-002',
    'labor supply': 'MS-LM-002',
    'labour supply': 'MS-LM-002',
    'employment': 'MS-LM-002',
    'worker': 'MS-LM-002',
    'occupat': 'MS-LM-002',
    'gender gap': 'MS-LM-002',
    'gender pay': 'MS-LM-002',
    'glass ceiling': 'MS-LM-002',
    'workforce': 'MS-LM-002',
    'hiring': 'MS-LM-002',
    'discrimination': 'MS-LM-002',

    # ── Extended: Risk & Uncertainty ──
    'risk aversion': 'MS-RD-001',
    'risk preference': 'MS-RD-001',
    'uncertainty': 'MS-RD-001',
    'ambiguity aversion': 'MS-RD-001',
    'expected utility': 'MS-CL-001',
    'consumer choice': 'MS-RD-001',

    # ── Extended: Organizations & Strategy ──
    'organizational': 'MS-IN-001',
    'market design': 'MS-SI-003',
    'matching market': 'MS-SI-003',
    'kidney exchange': 'MS-SI-003',
    'school choice': 'MS-SI-003',
    'market failure': 'MS-IN-001',
    'regulation': 'MS-IN-001',
    'redistribution': 'MS-SP-001',
    'tax compliance': 'MS-NU-001',
    'compliance': 'MS-NU-001',

    # ── Extended: Behavioral Change ──
    'habit': 'MS-TP-003',
    'addiction': 'MS-TP-004',
    'saving': 'MS-TP-001',
    'retirement': 'MS-TP-001',
    'pension': 'MS-TP-001',
    'health behavior': 'MS-WB-001',
    'obesity': 'MS-WB-001',
    'energy conservation': 'MS-NU-001',
    'organ donat': 'MS-NU-002',

    # ── Extended: Entrepreneurship ──
    'entrepreneur': 'MS-ENT-001',
    'startup': 'MS-ENT-001',
}

# ─────────────────────────────────────────────────────────────────────
# STAGE 2: use_for tag → Theory defaults (domain-level assignment)
# Only applied when Stage 1 finds nothing
# ─────────────────────────────────────────────────────────────────────

USE_FOR_THEORY_MAP = {
    'DOMAIN-MIGRATION': ['MS-LM-001'],
    'DOMAIN-LABOR': ['MS-LM-002'],
    'DOMAIN-POLITICAL': ['MS-PP-001'],
    'DOMAIN-HEALTH': ['MS-WB-001'],
    'DOMAIN-MONETARY': ['MS-BF-001'],
    'DOMAIN-FINANCE': ['MS-BF-001'],
    'DOMAIN-EDUCATION': ['MS-SF-001'],
    'DOMAIN-DEVELOPMENT': ['MS-DV-001'],
    'DOMAIN-INTEGRATION': ['MS-LM-001'],
    'DOMAIN-PLATFORM': ['MS-NU-001'],
}

# ─────────────────────────────────────────────────────────────────────
# STAGE 3: LIT-Author tag → Author's primary theory (conservative)
# Only applied when Stage 1 AND Stage 2 find nothing
# Maps each author's LIT-appendix to their SINGLE most representative theory
# ─────────────────────────────────────────────────────────────────────

LIT_AUTHOR_THEORY_MAP = {
    'LIT-FEH': 'MS-SP-004',         # Fehr → Social Preferences (general)
    'LIT-FEHR': 'MS-SP-004',        # Fehr → Social Preferences (general)
    'LIT-KT': 'MS-RD-001',          # Kahneman-Tversky → Prospect Theory
    'LIT-MALMENDIER': 'MS-IB-002',  # Malmendier → Overconfidence/Experience
    'LIT-LIST': 'MS-SP-004',        # List → Field Experiments/Social Pref
    'LIT-FALK': 'MS-SP-002',        # Falk → Reciprocity
    'LIT-BENABOU': 'MS-MO-003',     # Bénabou → Motivated Beliefs
    'LIT-CARD': 'MS-LM-002',        # Card → Labor Economics
    'LIT-AGHION': 'MS-IN-001',      # Aghion → Institutions/Innovation
    'LIT-GOLDIN': 'MS-LM-002',      # Goldin → Labor/Gender
    'LIT-BECKER': 'MS-SF-001',      # Becker → Human Capital
    'LIT-CAMERER': 'MS-SI-006',     # Camerer → Behavioral Game Theory
    'LIT-SCHELLING': 'MS-SI-005',   # Schelling → Coordination/Focal Points
    'LIT-AKERLOF': 'MS-IB-001',     # Akerlof → Identity Economics
    'LIT-SHAFIR': 'MS-DV-002',      # Shafir → Scarcity
    'LIT-VANDENSTEEN': 'MS-SI-001', # Van den Steen → Strategic Interaction
    'LIT-AUTOR': 'MS-LM-002',       # Autor → Labor/Technology
    'LIT-MULLAINATHAN': 'MS-DV-002',# Mullainathan → Scarcity
    'LIT-ARIELY': 'MS-RD-001',      # Ariely → Behavioral Anomalies
    'LIT-SUNSTEIN': 'MS-NU-001',    # Sunstein → Nudge
    'LIT-LOEWENSTEIN': 'MS-NE-003', # Loewenstein → Visceral/Emotions
    'LIT-BLINDER': 'MS-BF-001',     # Blinder → Central Banking/Finance
    'LIT-ENK': 'MS-LM-001',         # ENK → Migration/Integration
}


def parse_entries(bib_path):
    """Parse all BibTeX entries with their fields."""
    with open(bib_path, 'r', encoding='utf-8') as f:
        content = f.read()

    entries = []
    pattern = re.compile(r'@(\w+)\{(\S+?),\s*\n(.*?)(?=\n@|\Z)', re.DOTALL)

    for m in pattern.finditer(content):
        entry_type = m.group(1)
        key = m.group(2)
        body = m.group(3)

        # Extract fields
        fields = {}
        for fm in re.finditer(r'(\w+)\s*=\s*\{((?:[^{}]|\{[^{}]*\})*)\}', body):
            fields[fm.group(1).lower()] = fm.group(2).strip()

        entries.append({
            'key': key,
            'type': entry_type,
            'fields': fields,
            'start': m.start(),
            'end': m.end(),
        })

    return entries, content


def match_theories_for_entry(entry):
    """Match theories based on title, abstract, keywords, and use_for."""
    fields = entry['fields']
    theories = set()
    match_sources = []

    # Build search text from title + abstract + keywords
    search_text = ' '.join([
        fields.get('title', ''),
        fields.get('abstract', ''),
        fields.get('keywords', ''),
    ]).lower()

    # Stage 1: Keyword matching
    for keyword, theory_id in KEYWORD_THEORY_MAP.items():
        if keyword in search_text:
            theories.add(theory_id)
            match_sources.append(('keyword', keyword, theory_id))

    # Stage 2: use_for DOMAIN tag matching (fallback if Stage 1 found nothing)
    if not theories:
        use_for = fields.get('use_for', '')
        for tag, theory_ids in USE_FOR_THEORY_MAP.items():
            if tag in use_for:
                for tid in theory_ids:
                    theories.add(tid)
                    match_sources.append(('domain', tag, tid))

    # Stage 3: LIT-Author tag matching (last resort)
    if not theories:
        use_for = fields.get('use_for', '')
        for lit_tag, theory_id in LIT_AUTHOR_THEORY_MAP.items():
            if lit_tag in use_for:
                theories.add(theory_id)
                match_sources.append(('lit', lit_tag, theory_id))
                break  # Only use first matching LIT tag

    return sorted(theories), match_sources


def add_theory_support(content, bib_key, theories):
    """Add or update theory_support field in a BibTeX entry."""
    # Find the entry
    pattern = re.compile(
        r'(@\w+\{' + re.escape(bib_key) + r',.*?(?=\n@|\Z))',
        re.DOTALL
    )
    match = pattern.search(content)
    if not match:
        return content, False

    entry = match.group(0)
    theory_str = ', '.join(theories)

    # Check if theory_support field already exists
    ts_pattern = re.compile(r'(theory_support\s*=\s*\{)([^}]*?)(\})')
    ts_match = ts_pattern.search(entry)

    if ts_match:
        # Field exists but is empty - fill it
        existing = ts_match.group(2).strip()
        if existing:
            return content, False  # Already has content, skip
        new_entry = entry[:ts_match.start()] + \
                    ts_match.group(1) + theory_str + ts_match.group(3) + \
                    entry[ts_match.end():]
    else:
        # Field doesn't exist - add after use_for or evidence_tier
        # Try to find use_for line to insert after
        uf_match = re.search(r'(use_for\s*=\s*\{[^}]*\},?\s*\n)', entry)
        if uf_match:
            insert_pos = uf_match.end()
            indent = '  '
            new_entry = entry[:insert_pos] + \
                        f'{indent}theory_support = {{{theory_str}}},\n' + \
                        entry[insert_pos:]
        else:
            # Try after evidence_tier
            et_match = re.search(r'(evidence_tier\s*=\s*\{[^}]*\},?\s*\n)', entry)
            if et_match:
                insert_pos = et_match.end()
                indent = '  '
                new_entry = entry[:insert_pos] + \
                            f'{indent}theory_support = {{{theory_str}}},\n' + \
                            entry[insert_pos:]
            else:
                return content, False  # Can't find insertion point

    content = content[:match.start()] + new_entry + content[match.end():]
    return content, True


def main():
    dry_run = '--dry-run' in sys.argv
    stats_only = '--stats' in sys.argv
    limit = None
    for i, arg in enumerate(sys.argv):
        if arg == '--limit' and i + 1 < len(sys.argv):
            limit = int(sys.argv[i + 1])

    entries, content = parse_entries(BIB_PATH)
    print(f"Parsed {len(entries)} BibTeX entries\n")

    # Identify candidates (no theory_support or empty theory_support)
    candidates = []
    already_have = 0
    for e in entries:
        ts = e['fields'].get('theory_support', '').strip()
        if ts:
            already_have += 1
        else:
            candidates.append(e)

    print(f"Already have theory_support: {already_have}")
    print(f"Candidates for assignment:   {len(candidates)}")

    # Match theories for all candidates
    matches = []
    no_match = 0
    stage1_count = 0
    stage2_count = 0
    stage3_count = 0

    for e in candidates:
        theories, sources = match_theories_for_entry(e)
        if theories:
            src_type = sources[0][0] if sources else '?'
            if src_type == 'keyword':
                stage1_count += 1
            elif src_type == 'domain':
                stage2_count += 1
            elif src_type == 'lit':
                stage3_count += 1
            matches.append((e, theories, sources))
        else:
            no_match += 1

    print(f"\nMatched via keywords (Stage 1):  {stage1_count}")
    print(f"Matched via DOMAIN  (Stage 2):   {stage2_count}")
    print(f"Matched via LIT-Author (Stage 3): {stage3_count}")
    print(f"No match found:                  {no_match}")
    print(f"Total to assign:                 {len(matches)}")

    if stats_only:
        # Show theory distribution
        theory_counts = {}
        for _, theories, _ in matches:
            for t in theories:
                theory_counts[t] = theory_counts.get(t, 0) + 1
        print(f"\n{'='*60}")
        print(f"  THEORY DISTRIBUTION (new assignments)")
        print(f"{'='*60}")
        for t, c in sorted(theory_counts.items(), key=lambda x: -x[1])[:30]:
            print(f"  {t}: {c}")
        return

    if limit:
        matches = matches[:limit]
        print(f"\nLimited to {limit} entries")

    # Apply assignments
    print(f"\n{'='*60}")
    print(f"  {'DRY RUN' if dry_run else 'APPLYING'}: {len(matches)} assignments")
    print(f"{'='*60}\n")

    stats = {'assigned': 0, 'failed': 0, 'theories_added': 0}

    for e, theories, sources in matches:
        key = e['key']
        theory_str = ', '.join(theories)
        src_type = sources[0][0] if sources else '?'
        stage = {'keyword': 'KW', 'domain': 'DM', 'lit': 'LT'}.get(src_type, '??')
        icon = '🔍' if dry_run else '✅'

        # Show first keyword match
        first_match = sources[0][1] if sources else '?'
        print(f"  {icon} [{stage}] {key}: {theory_str}  (via '{first_match}')")

        if not dry_run:
            content, changed = add_theory_support(content, key, theories)
            if changed:
                stats['assigned'] += 1
                stats['theories_added'] += len(theories)
            else:
                print(f"     ⚠️  Could not update entry")
                stats['failed'] += 1
        else:
            stats['assigned'] += 1
            stats['theories_added'] += len(theories)

    if not dry_run and stats['assigned'] > 0:
        with open(BIB_PATH, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\n  ✅ Written to {BIB_PATH}")

    print(f"\n{'='*60}")
    print(f"  SUMMARY")
    print(f"{'='*60}")
    print(f"  Entries assigned:  {stats['assigned']}")
    print(f"  Theories added:    {stats['theories_added']}")
    print(f"  Failed:            {stats['failed']}")
    print(f"  Previously had:    {already_have}")
    print(f"  New total:         {already_have + stats['assigned']}")
    print(f"  No match (skip):   {no_match}")

    if dry_run:
        print(f"\n  🔍 DRY RUN — no changes written")


if __name__ == '__main__':
    main()
