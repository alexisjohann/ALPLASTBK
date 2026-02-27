#!/usr/bin/env python3
"""
Fix content_level fields in Paper-YAMLs.

Two issues addressed:
1. Malformed full_text.content_level values (e.g., "L1L0L1" instead of "L1")
2. Wrong prior_score.content_level (L0 when should be L1 based on actual content)

For full_text.content_level: syncs to match prior_score.content_level
For prior_score.content_level: recomputes based on structural Definition 2

Usage:
    python scripts/fix_content_level_fields.py --stats
    python scripts/fix_content_level_fields.py --dry-run
    python scripts/fix_content_level_fields.py --limit 1
    python scripts/fix_content_level_fields.py          # Fix all
"""

import re
import os
import sys
import glob
import argparse
from collections import Counter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAPER_DIR = os.path.join(BASE_DIR, 'data', 'paper-references')
TEXT_DIR = os.path.join(BASE_DIR, 'data', 'paper-texts')


def get_correct_content_level(text):
    """Determine correct content level from YAML text content using Definition 2."""
    # Extract paper key for full-text check
    m = re.search(r'^paper:\s*"?([^"\n]+)"?', text, re.MULTILINE)
    paper_key = m.group(1).strip() if m else ''

    # L3: Full text file exists and is genuine (>5000 words)
    text_path = os.path.join(TEXT_DIR, f"PAP-{paper_key}.md")
    if os.path.exists(text_path):
        with open(text_path, 'r', encoding='utf-8') as f:
            word_count = len(f.read().split())
        if word_count > 5000:
            return 'L3', f'full text {word_count} words'

    # L2: Has structural_characteristics
    if 'structural_characteristics:' in text:
        return 'L2', 'structural_characteristics'

    # L2: Has >=3 findings + abstract
    findings = re.findall(r'^\s+- finding:', text, re.MULTILINE)
    has_abstract = _has_substantial_abstract(text)
    if len(findings) >= 3 and has_abstract:
        return 'L2', f'{len(findings)} findings + abstract'

    # L2: Has full text file but short (summary/extract)
    if os.path.exists(text_path):
        return 'L2', 'summary in paper-texts'

    # L1: Has substantial abstract
    if has_abstract:
        return 'L1', 'abstract >50 chars'

    # L1: Has theory_support (list, bracket, or comma-separated single-line)
    if re.search(r'theory_support:\s*\n\s+-\s+\S', text) or \
       re.search(r'theory_support:\s*\[.+\]', text) or \
       re.search(r'theory_support:\s+MS-[A-Z]{2}-\d{3}', text):
        return 'L1', 'theory_support'

    # L1: Has key_findings with at least 1 finding (with or without leading whitespace)
    if len(findings) >= 1 or re.search(r'^- finding:', text, re.MULTILINE):
        return 'L1', f'{len(findings)} finding(s)'

    # L1: Has populated behavioral_mapping
    bm = re.search(r'behavioral_mapping:\s*\n((?:\s{4,}.+\n)*)', text, re.MULTILINE)
    if bm and len(bm.group(1).strip()) > 20:
        return 'L1', 'behavioral_mapping'

    # L0: Truly metadata only
    # Note: use_for alone does NOT qualify for L1 (it's just a routing tag)
    return 'L0', 'metadata only'


def _has_substantial_abstract(text):
    """Check if paper has a substantial abstract (>50 chars)."""
    # Top-level multiline abstract
    m = re.search(r'^abstract:\s+(.+(?:\n  .+)*)', text, re.MULTILINE)
    if m:
        val = m.group(1).strip()
        if val and val != 'null' and val != '~' and len(val) > 50:
            return True

    # Indented block scalar abstract (covers both abstract: and abstract_extended:)
    m = re.search(r'^\s+abstract(?:_extended)?:\s*[|>]-?\s*\n((?:\s{4,}.+\n)*)', text, re.MULTILINE)
    if m and len(m.group(1).strip()) > 50:
        return True

    # Indented quoted abstract
    m = re.search(r'^\s+abstract(?:_extended)?:\s*"([^"]*)"', text, re.MULTILINE)
    if m and len(m.group(1).strip()) > 50:
        return True

    # Indented single-line or multiline flow abstract/abstract_extended
    m = re.search(r'^\s+abstract(?:_extended)?:\s+(.+)$', text, re.MULTILINE)
    if m:
        val = m.group(1).strip().strip('"').strip("'")
        if val and val not in ('null', '~') and len(val) > 50:
            return True

    # Block scalar abstract_extended with continuation lines
    m = re.search(r'^\s+abstract_extended:\s*[\'"](.+?)(?:\n\n|\n\S)', text, re.MULTILINE | re.DOTALL)
    if m and len(m.group(1).strip()) > 50:
        return True

    return False


def get_prior_score_content_level(text):
    """Extract content_level from prior_score section."""
    m = re.search(r'prior_score:.*?content_level:\s*(\S+)', text, re.DOTALL)
    if m:
        return m.group(1).strip().strip('"')
    return None


def get_full_text_content_level(text):
    """Extract content_level from full_text section."""
    m = re.search(r'full_text:.*?content_level:\s*(\S+)', text, re.DOTALL)
    if m:
        return m.group(1).strip().strip('"')
    return None


def is_malformed(level):
    """Check if content_level value is malformed (concatenated)."""
    if not level:
        return False
    return len(level) > 2  # Valid: L0, L1, L2, L3


def fix_full_text_content_level(text, correct_level):
    """Fix malformed full_text.content_level using text replacement."""
    # Find the full_text block and its content_level line
    # Pattern: "  content_level: <value>" within full_text block
    ft_match = re.search(r'(full_text:\s*\n(?:  \S.*\n|  \n)*?  content_level:\s*)(\S+)', text)
    if not ft_match:
        return text, False

    old_val = ft_match.group(2)
    if old_val == correct_level:
        return text, False

    new_text = text[:ft_match.start(2)] + correct_level + text[ft_match.end(2):]
    return new_text, True


def fix_prior_score_content_level(text, correct_level):
    """Fix prior_score.content_level if wrong."""
    ps_match = re.search(r'(prior_score:\s*\n(?:  \S.*\n|  \n)*?  content_level:\s*)(\S+)', text)
    if not ps_match:
        return text, False

    old_val = ps_match.group(2)
    if old_val == correct_level:
        return text, False

    new_text = text[:ps_match.start(2)] + correct_level + text[ps_match.end(2):]
    return new_text, True


def fix_confidence_multiplier(text, new_level):
    """Update confidence_multiplier to match new content level."""
    cm_map = {'L0': '0.6', 'L1': '0.8', 'L2': '0.95', 'L3': '1.0'}
    expected = cm_map.get(new_level)
    if not expected:
        return text, False

    cm_match = re.search(r'(prior_score:.*?confidence_multiplier:\s*)([0-9.]+)', text, re.DOTALL)
    if not cm_match:
        return text, False

    old_val = cm_match.group(2)
    if old_val == expected:
        return text, False

    new_text = text[:cm_match.start(2)] + expected + text[cm_match.end(2):]
    return new_text, True


def main():
    parser = argparse.ArgumentParser(description='Fix content_level fields')
    parser.add_argument('--stats', action='store_true', help='Show statistics only')
    parser.add_argument('--dry-run', action='store_true', help='Show what would change')
    parser.add_argument('--limit', type=int, default=0, help='Limit changes (0=all)')
    args = parser.parse_args()

    yaml_files = sorted(glob.glob(os.path.join(PAPER_DIR, 'PAP-*.yaml')))
    print(f"Scanning {len(yaml_files)} Paper-YAMLs...\n")

    # Analyze
    ft_malformed = Counter()  # full_text.content_level malformed values
    ps_changes = Counter()     # prior_score.content_level corrections
    ps_current = Counter()
    ps_correct = Counter()
    changes = []

    for yf in yaml_files:
        fname = os.path.basename(yf)
        with open(yf, 'r', encoding='utf-8') as f:
            text = f.read()

        ft_level = get_full_text_content_level(text)
        ps_level = get_prior_score_content_level(text)
        correct_level, reason = get_correct_content_level(text)

        if ps_level:
            ps_current[ps_level] += 1
        ps_correct[correct_level] += 1

        # Check for issues
        ft_needs_fix = ft_level and is_malformed(ft_level)
        ft_needs_sync = ft_level and ft_level != correct_level and not is_malformed(ft_level)
        ps_needs_fix = ps_level and ps_level != correct_level

        if ft_needs_fix:
            ft_malformed[ft_level] += 1

        if ft_needs_fix or ft_needs_sync or ps_needs_fix:
            changes.append({
                'file': yf,
                'fname': fname,
                'ft_old': ft_level,
                'ps_old': ps_level,
                'correct': correct_level,
                'reason': reason,
                'ft_malformed': ft_needs_fix,
                'ft_sync': ft_needs_sync,
                'ps_fix': ps_needs_fix,
            })

    # Statistics
    print(f"{'='*60}")
    print(f"  CONTENT LEVEL ANALYSIS")
    print(f"{'='*60}\n")

    print(f"  {'Level':<8} {'Current(PS)':<14} {'Correct':<12} {'Delta':<10}")
    print(f"  {'-'*44}")
    for lvl in ['L0', 'L1', 'L2', 'L3']:
        cur = ps_current.get(lvl, 0)
        cor = ps_correct.get(lvl, 0)
        delta = cor - cur
        delta_str = f"+{delta}" if delta > 0 else str(delta)
        marker = " <--" if delta != 0 else ""
        print(f"  {lvl:<8} {cur:<14} {cor:<12} {delta_str:<10}{marker}")

    print(f"\n  MALFORMED full_text.content_level values:")
    for val, count in ft_malformed.most_common():
        print(f"    {val}: {count}")
    print(f"    TOTAL: {sum(ft_malformed.values())}")

    n_ft_malformed = sum(1 for c in changes if c['ft_malformed'])
    n_ft_sync = sum(1 for c in changes if c['ft_sync'])
    n_ps_fix = sum(1 for c in changes if c['ps_fix'])

    print(f"\n  CHANGES NEEDED:")
    print(f"    full_text.content_level malformed: {n_ft_malformed}")
    print(f"    full_text.content_level out of sync: {n_ft_sync}")
    print(f"    prior_score.content_level wrong: {n_ps_fix}")
    print(f"    TOTAL files to modify: {len(changes)}")

    if args.stats:
        return

    if not changes:
        print("\n  All content levels are correct!")
        return

    # Apply changes
    if args.limit:
        changes = changes[:args.limit]
        print(f"\n  Limiting to {args.limit} changes")

    updated = 0
    for c in changes:
        with open(c['file'], 'r', encoding='utf-8') as f:
            text = f.read()

        modified = False
        parts = []

        # Fix full_text.content_level
        if c['ft_malformed'] or c['ft_sync']:
            text, changed = fix_full_text_content_level(text, c['correct'])
            if changed:
                modified = True
                parts.append(f"ft:{c['ft_old']}→{c['correct']}")

        # Fix prior_score.content_level
        if c['ps_fix']:
            text, changed = fix_prior_score_content_level(text, c['correct'])
            if changed:
                modified = True
                parts.append(f"ps:{c['ps_old']}→{c['correct']}")

            # Also fix confidence_multiplier
            text, changed = fix_confidence_multiplier(text, c['correct'])
            if changed:
                parts.append("cm")

        icon = '🔍' if args.dry_run else '✅'
        desc = ', '.join(parts) if parts else 'no change'
        print(f"  {icon} {c['fname']}: {desc} ({c['reason']})")

        if modified and not args.dry_run:
            with open(c['file'], 'w', encoding='utf-8') as f:
                f.write(text)
            updated += 1

    print(f"\n{'='*60}")
    print(f"  SUMMARY")
    print(f"{'='*60}")
    print(f"  Files analyzed:  {len(yaml_files)}")
    print(f"  Changes needed:  {len(changes)}")
    print(f"  Updated:         {updated}")
    if args.dry_run:
        print(f"\n  🔍 DRY RUN — no changes written")


if __name__ == '__main__':
    main()
