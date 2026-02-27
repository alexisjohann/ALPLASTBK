#!/usr/bin/env python3
"""Rank I2 papers as candidates for I5 (Full Integration) upgrade.

Scans all PAP-*.yaml files in data/paper-references/ and produces
a prioritized ranking based on evidence tier, content completeness,
and existing integration components.

Usage:
    python scripts/rank_i5_candidates.py              # Top 20 candidates
    python scripts/rank_i5_candidates.py --all         # All I2 papers
    python scripts/rank_i5_candidates.py --top 50      # Top 50
    python scripts/rank_i5_candidates.py --tier 1      # Only Tier 1
    python scripts/rank_i5_candidates.py --stats       # Summary statistics
"""

import glob
import os
import re
import sys
import yaml


def extract_field(content, field_name):
    """Extract a YAML field value from raw text (fast, no full parse)."""
    pattern = rf'^\s*{field_name}:\s*(.+)$'
    match = re.search(pattern, content, re.MULTILINE)
    if match:
        val = match.group(1).strip().strip("'\"")
        return val
    return None


def has_section(content, section_name):
    """Check if a YAML section exists."""
    pattern = rf'^\s*{section_name}:'
    return bool(re.search(pattern, content, re.MULTILINE))


def parse_paper(filepath):
    """Extract key fields from a paper YAML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    basename = os.path.basename(filepath).replace('.yaml', '')

    # Integration level - check multiple locations
    int_level = None
    for field in ['integration_level']:
        val = extract_field(content, field)
        if val and val.isdigit():
            int_level = int(val)
            break

    # Also check nested status.integration_level
    if int_level is None:
        match = re.search(r'status:\s*\n\s+integration_level:\s*(\d+)', content)
        if match:
            int_level = int(match.group(1))

    # Also check ebf_integration.integration_level
    if int_level is None:
        match = re.search(r'ebf_integration:\s*\n(?:\s+\w+:.*\n)*?\s+integration_level:\s*(\d+)', content)
        if match:
            int_level = int(match.group(1))

    # Evidence tier
    ev_tier = None
    val = extract_field(content, 'evidence_tier')
    if val and val.isdigit():
        ev_tier = int(val)
    if ev_tier is None:
        match = re.search(r'ebf_integration:\s*\n(?:\s+\w+:.*\n)*?\s+evidence_tier:\s*(\d+)', content)
        if match:
            ev_tier = int(match.group(1))

    # Content level
    content_level = extract_field(content, 'content_level')
    if content_level and content_level.startswith('L'):
        content_level = content_level
    else:
        content_level = 'L1'

    # Prior score
    pi_norm = None
    val = extract_field(content, 'pi_normalized')
    if val:
        try:
            pi_norm = float(val)
        except ValueError:
            pass

    # Title
    title = extract_field(content, 'title')
    if title:
        title = title[:80]

    # Year
    year = extract_field(content, 'year')

    # Check for key I5 components
    has_params = has_section(content, 'parameter_contributions') or has_section(content, 'parameters')
    has_behavioral = has_section(content, 'behavioral_mapping') or has_section(content, '10C_mapping')
    has_findings = has_section(content, 'key_findings_structured')
    has_chapter = has_section(content, 'chapter_relevance')
    has_theory = has_section(content, 'theory_support') or has_section(content, 'theory_integration')
    has_cases = has_section(content, 'case_registry') or has_section(content, 'case_integration') or has_section(content, 'linked_cases')
    has_fulltext = 'available: true' in content and 'paper-texts' in content

    return {
        'file': basename,
        'title': title or 'Unknown',
        'year': year,
        'integration_level': int_level,
        'evidence_tier': ev_tier or 3,
        'content_level': content_level,
        'pi_normalized': pi_norm,
        'has_parameters': has_params,
        'has_behavioral_mapping': has_behavioral,
        'has_key_findings': has_findings,
        'has_chapter_relevance': has_chapter,
        'has_theory_support': has_theory,
        'has_cases': has_cases,
        'has_fulltext': has_fulltext,
    }


def calculate_readiness(paper):
    """Calculate upgrade readiness score (0-100)."""
    score = 0

    # Evidence tier (max 30 points)
    tier = paper['evidence_tier']
    if tier == 1:
        score += 30
    elif tier == 2:
        score += 20
    else:
        score += 10

    # Content level (max 15 points)
    cl = paper['content_level']
    if cl == 'L3':
        score += 15
    elif cl == 'L2':
        score += 10
    else:
        score += 5

    # Existing components (max 42 points, 7 points each)
    components = [
        'has_parameters', 'has_behavioral_mapping', 'has_key_findings',
        'has_chapter_relevance', 'has_theory_support', 'has_cases'
    ]
    for comp in components:
        if paper.get(comp):
            score += 7

    # Prior score bonus (max 13 points)
    pi = paper.get('pi_normalized')
    if pi:
        score += min(13, int(pi * 13))

    return score


def print_stats(papers):
    """Print summary statistics."""
    levels = {}
    tiers = {}
    for p in papers:
        il = p.get('integration_level', 0) or 0
        et = p.get('evidence_tier', 3) or 3
        levels[il] = levels.get(il, 0) + 1
        tiers[et] = tiers.get(et, 0) + 1

    print("\n" + "=" * 70)
    print("  PAPER DATABASE STATISTICS")
    print("=" * 70)
    print(f"\n  Total papers scanned: {len(papers)}")
    print(f"\n  Integration Level Distribution:")
    for level in sorted(levels.keys()):
        bar = "█" * (levels[level] // 10)
        name = {0: 'I0', 1: 'I1', 2: 'I2', 3: 'I3', 4: 'I4', 5: 'I5'}.get(level, f'I{level}')
        print(f"    {name}: {levels[level]:>5}  {bar}")

    print(f"\n  Evidence Tier Distribution:")
    for tier in sorted(tiers.keys()):
        bar = "█" * (tiers[tier] // 10)
        print(f"    Tier {tier}: {tiers[tier]:>5}  {bar}")

    # I2 with Tier 1
    i2_t1 = [p for p in papers if (p.get('integration_level') or 0) == 2 and p.get('evidence_tier') == 1]
    print(f"\n  I2 papers with Tier 1 evidence: {len(i2_t1)}")

    # I2 with L3 content
    i2_l3 = [p for p in papers if (p.get('integration_level') or 0) == 2 and p.get('content_level') == 'L3']
    print(f"  I2 papers with L3 full text: {len(i2_l3)}")

    # I2 with parameters
    i2_params = [p for p in papers if (p.get('integration_level') or 0) == 2 and p.get('has_parameters')]
    print(f"  I2 papers with parameters: {len(i2_params)}")

    print()


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Rank I2 papers for I5 upgrade')
    parser.add_argument('--all', action='store_true', help='Show all I2 papers')
    parser.add_argument('--top', type=int, default=20, help='Show top N candidates')
    parser.add_argument('--tier', type=int, help='Filter by evidence tier')
    parser.add_argument('--stats', action='store_true', help='Show summary statistics')
    parser.add_argument('--min-score', type=int, default=0, help='Minimum readiness score')
    args = parser.parse_args()

    # Scan all paper YAML files
    pattern = 'data/paper-references/PAP-*.yaml'
    files = glob.glob(pattern)
    if not files:
        # Try from repo root
        files = glob.glob(os.path.join(os.path.dirname(__file__), '..', pattern))

    papers = []
    for f in files:
        try:
            paper = parse_paper(f)
            papers.append(paper)
        except Exception as e:
            pass  # Skip unparseable files

    if args.stats:
        print_stats(papers)
        return

    # Filter to I2 papers only
    i2_papers = [p for p in papers if (p.get('integration_level') or 0) == 2]

    if args.tier:
        i2_papers = [p for p in i2_papers if p.get('evidence_tier') == args.tier]

    # Calculate readiness scores
    for p in i2_papers:
        p['readiness'] = calculate_readiness(p)

    if args.min_score:
        i2_papers = [p for p in i2_papers if p['readiness'] >= args.min_score]

    # Sort by readiness (descending)
    i2_papers.sort(key=lambda x: x['readiness'], reverse=True)

    if not args.all:
        i2_papers = i2_papers[:args.top]

    # Print results
    print("\n" + "=" * 100)
    print("  I5 UPGRADE CANDIDATES — Ranked by Readiness Score")
    print("=" * 100)
    print(f"\n  {'#':>3}  {'Score':>5}  {'Tier':>4}  {'CL':>3}  {'Params':>6}  {'BM':>4}  {'KF':>4}  {'CH':>4}  {'TH':>4}  {'Paper'}")
    print(f"  {'—'*3}  {'—'*5}  {'—'*4}  {'—'*3}  {'—'*6}  {'—'*4}  {'—'*4}  {'—'*4}  {'—'*4}  {'—'*50}")

    for i, p in enumerate(i2_papers, 1):
        score = p['readiness']
        tier = p.get('evidence_tier', '?')
        cl = p.get('content_level', '?')
        params = '✓' if p['has_parameters'] else '·'
        bm = '✓' if p['has_behavioral_mapping'] else '·'
        kf = '✓' if p['has_key_findings'] else '·'
        ch = '✓' if p['has_chapter_relevance'] else '·'
        th = '✓' if p['has_theory_support'] else '·'
        name = p['file'].replace('PAP-', '')
        if len(name) > 50:
            name = name[:47] + '...'

        # Color-code score
        if score >= 70:
            indicator = "★★★"
        elif score >= 50:
            indicator = "★★ "
        elif score >= 30:
            indicator = "★  "
        else:
            indicator = "   "

        print(f"  {i:>3}  {score:>5}  T{tier:<3}  {cl:>3}  {params:>6}  {bm:>4}  {kf:>4}  {ch:>4}  {th:>4}  {name}  {indicator}")

    print(f"\n  Legend: Params=parameter_contributions, BM=behavioral_mapping, KF=key_findings,")
    print(f"         CH=chapter_relevance, TH=theory_support, ★=readiness level")
    print(f"\n  Total I2 candidates shown: {len(i2_papers)}")
    print(f"  Run with --stats for full database overview")
    print()


if __name__ == '__main__':
    main()
