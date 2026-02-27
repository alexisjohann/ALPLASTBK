#!/usr/bin/env python3
"""
recompute_quality_scores.py - Fix q_C, q_I, q_total, confidence_multiplier
==========================================================================

Targeted fix: Recomputes quality scores based on EXISTING content_level and
integration_level values (does NOT recompute those levels themselves).

This fixes inconsistencies caused by level changes without corresponding
quality score updates.

Mappings (from Appendix BM, Definition 4):
  q_C = C_numeric / 3  → L0=0.0, L1=0.333, L2=0.667, L3=1.0
  q_I = I_numeric / 5  → I0=0.0, I1=0.2, I2=0.4, I3=0.6, I4=0.8, I5=1.0
  q_total = round((q_C + q_I) / 2, 3)
  confidence_multiplier: L0=0.6, L1=0.8, L2=0.95, L3=1.0

Usage:
    python scripts/recompute_quality_scores.py --stats
    python scripts/recompute_quality_scores.py --dry-run
    python scripts/recompute_quality_scores.py
"""

import os
import re
import sys
import argparse
from pathlib import Path

PAPER_DIR = Path('data/paper-references')

Q_C_MAP = {'L0': 0.0, 'L1': 0.333, 'L2': 0.667, 'L3': 1.0}
Q_I_MAP = {'I0': 0.0, 'I1': 0.2, 'I2': 0.4, 'I3': 0.6, 'I4': 0.8, 'I5': 1.0}
CM_MAP = {'L0': 0.6, 'L1': 0.8, 'L2': 0.95, 'L3': 1.0}


def get_field(text, section_pattern, field_pattern):
    """Extract a field value from within a YAML section using regex."""
    # Find the section
    sec_match = re.search(section_pattern, text)
    if not sec_match:
        return None
    # Find the field within the section's indented block
    start = sec_match.start()
    # Search from section start to end of its indented block
    remaining = text[start:]
    field_match = re.search(field_pattern, remaining, re.MULTILINE)
    if field_match:
        return field_match.group(1).strip().strip("'\"")
    return None


def extract_prior_score_fields(text):
    """Extract content_level, integration_level, q_C, q_I, q_total, confidence_multiplier from prior_score section."""
    ps_match = re.search(r'^prior_score:\s*$', text, re.MULTILINE)
    if not ps_match:
        return None

    # Get the prior_score block (everything indented under prior_score:)
    start = ps_match.end()
    lines = text[start:].split('\n')
    ps_block = []
    for line in lines:
        if line and not line[0].isspace() and line.strip():
            break
        ps_block.append(line)
    ps_text = '\n'.join(ps_block)

    result = {}

    # Content level
    m = re.search(r'content_level:\s*(\S+)', ps_text)
    result['content_level'] = m.group(1).strip("'\"") if m else None

    # Integration level
    m = re.search(r'integration_level:\s*(\S+)', ps_text)
    result['integration_level'] = m.group(1).strip("'\"") if m else None

    # confidence_multiplier
    m = re.search(r'confidence_multiplier:\s*(\S+)', ps_text)
    result['confidence_multiplier'] = float(m.group(1)) if m else None

    # quality_score fields
    m = re.search(r'q_C:\s*(\S+)', ps_text)
    result['q_C'] = float(m.group(1)) if m else None

    m = re.search(r'q_I:\s*(\S+)', ps_text)
    result['q_I'] = float(m.group(1)) if m else None

    m = re.search(r'q_total:\s*(\S+)', ps_text)
    result['q_total'] = float(m.group(1)) if m else None

    # prior_score (the numeric value)
    m = re.search(r'^\s+prior_score:\s*(\S+)', ps_text, re.MULTILINE)
    result['prior_score'] = float(m.group(1)) if m else None

    # pi_normalized
    m = re.search(r'pi_normalized:\s*(\S+)', ps_text)
    result['pi_normalized'] = float(m.group(1)) if m else None

    # classification
    m = re.search(r'classification:\s*(\S+)', ps_text)
    result['classification'] = m.group(1).strip("'\"") if m else None

    # evidence_quality
    m = re.search(r'evidence_quality:\s*(\S+)', ps_text)
    result['evidence_quality'] = float(m.group(1)) if m else None

    # computed_date
    m = re.search(r'computed_date:\s*(\S+)', ps_text)
    result['computed_date'] = m.group(1).strip("'\"") if m else None

    return result


def fix_quality_scores(text, fields, correct_q_C, correct_q_I, correct_q_total, correct_cm):
    """Fix quality score fields in the prior_score section using text replacement."""
    changed = False

    # Fix q_C
    if fields['q_C'] is not None and abs(fields['q_C'] - correct_q_C) > 0.001:
        old = f"q_C: {fields['q_C']}"
        new = f"q_C: {correct_q_C}"
        if old in text:
            text = text.replace(old, new, 1)
            changed = True

    # Fix q_I
    if fields['q_I'] is not None and abs(fields['q_I'] - correct_q_I) > 0.001:
        old = f"q_I: {fields['q_I']}"
        new = f"q_I: {correct_q_I}"
        if old in text:
            text = text.replace(old, new, 1)
            changed = True

    # Fix q_total
    if fields['q_total'] is not None and abs(fields['q_total'] - correct_q_total) > 0.001:
        old = f"q_total: {fields['q_total']}"
        new = f"q_total: {correct_q_total}"
        if old in text:
            text = text.replace(old, new, 1)
            changed = True

    # Fix confidence_multiplier
    if fields['confidence_multiplier'] is not None and abs(fields['confidence_multiplier'] - correct_cm) > 0.001:
        old = f"confidence_multiplier: {fields['confidence_multiplier']}"
        new = f"confidence_multiplier: {correct_cm}"
        if old in text:
            text = text.replace(old, new, 1)
            changed = True

    return text, changed


def main():
    parser = argparse.ArgumentParser(description='Recompute quality scores for Paper-YAMLs')
    parser.add_argument('--stats', action='store_true', help='Show statistics only')
    parser.add_argument('--dry-run', action='store_true', help='Show changes without writing')
    parser.add_argument('--limit', type=int, default=0, help='Limit changes to N files')
    args = parser.parse_args()

    files = sorted(PAPER_DIR.glob('PAP-*.yaml'))
    print(f"Scanning {len(files)} Paper-YAMLs...\n")

    # Statistics
    total = 0
    no_prior_score = 0
    old_schema = 0
    inconsistent_qC = 0
    inconsistent_qI = 0
    inconsistent_qT = 0
    inconsistent_cm = 0
    changes_needed = 0
    changes_made = 0

    # Track specific mismatches
    qC_mismatches = []
    cm_mismatches = []

    for f in files:
        total += 1
        text = f.read_text()

        fields = extract_prior_score_fields(text)
        if fields is None:
            no_prior_score += 1
            continue

        cl = fields.get('content_level')
        il = fields.get('integration_level')

        if cl is None or il is None:
            old_schema += 1
            continue

        # Compute correct values
        correct_q_C = Q_C_MAP.get(cl, 0.0)
        correct_q_I = Q_I_MAP.get(il, 0.0)
        correct_q_total = round((correct_q_C + correct_q_I) / 2, 3)
        correct_cm = CM_MAP.get(cl, 0.6)

        # Check inconsistencies
        needs_fix = False

        if fields['q_C'] is not None and abs(fields['q_C'] - correct_q_C) > 0.001:
            inconsistent_qC += 1
            qC_mismatches.append((f.name, cl, fields['q_C'], correct_q_C))
            needs_fix = True

        if fields['q_I'] is not None and abs(fields['q_I'] - correct_q_I) > 0.001:
            inconsistent_qI += 1
            needs_fix = True

        if fields['q_total'] is not None and abs(fields['q_total'] - correct_q_total) > 0.001:
            inconsistent_qT += 1
            needs_fix = True

        if fields['confidence_multiplier'] is not None and abs(fields['confidence_multiplier'] - correct_cm) > 0.001:
            inconsistent_cm += 1
            cm_mismatches.append((f.name, cl, fields['confidence_multiplier'], correct_cm))
            needs_fix = True

        if needs_fix:
            changes_needed += 1

        if args.stats:
            continue

        if not needs_fix:
            continue

        if args.limit and changes_made >= args.limit:
            continue

        new_text, changed = fix_quality_scores(text, fields, correct_q_C, correct_q_I, correct_q_total, correct_cm)

        if changed:
            if args.dry_run:
                fixes = []
                if abs((fields['q_C'] or 0) - correct_q_C) > 0.001:
                    fixes.append(f"q_C:{fields['q_C']}→{correct_q_C}")
                if abs((fields['q_I'] or 0) - correct_q_I) > 0.001:
                    fixes.append(f"q_I:{fields['q_I']}→{correct_q_I}")
                if abs((fields['q_total'] or 0) - correct_q_total) > 0.001:
                    fixes.append(f"q_total:{fields['q_total']}→{correct_q_total}")
                if abs((fields['confidence_multiplier'] or 0) - correct_cm) > 0.001:
                    fixes.append(f"cm:{fields['confidence_multiplier']}→{correct_cm}")
                print(f"  🔍 {f.name}: {', '.join(fixes)}")
            else:
                f.write_text(new_text)
                fixes = []
                if abs((fields['q_C'] or 0) - correct_q_C) > 0.001:
                    fixes.append(f"q_C→{correct_q_C}")
                if abs((fields['confidence_multiplier'] or 0) - correct_cm) > 0.001:
                    fixes.append(f"cm→{correct_cm}")
                print(f"  ✅ {f.name}: {', '.join(fixes)}")
            changes_made += 1

    # Print summary
    print(f"\n{'='*60}")
    print(f"  QUALITY SCORE ANALYSIS")
    print(f"{'='*60}\n")
    print(f"  Total papers:          {total}")
    print(f"  No prior_score:        {no_prior_score}")
    print(f"  Old schema:            {old_schema}")
    print(f"")
    print(f"  INCONSISTENCIES:")
    print(f"    q_C wrong:           {inconsistent_qC}")
    print(f"    q_I wrong:           {inconsistent_qI}")
    print(f"    q_total wrong:       {inconsistent_qT}")
    print(f"    confidence_mult:     {inconsistent_cm}")
    print(f"    TOTAL files:         {changes_needed}")
    print(f"")
    if not args.stats:
        print(f"  Changes made:          {changes_made}")
        if args.dry_run:
            print(f"\n  🔍 DRY RUN — no changes written")

    # Show sample mismatches if stats mode
    if args.stats and qC_mismatches:
        print(f"\n  Sample q_C mismatches (first 10):")
        for name, cl, old_qC, new_qC in qC_mismatches[:10]:
            print(f"    {name}: {cl} has q_C={old_qC} (should be {new_qC})")

    if args.stats and cm_mismatches:
        print(f"\n  Sample confidence_multiplier mismatches (first 10):")
        for name, cl, old_cm, new_cm in cm_mismatches[:10]:
            print(f"    {name}: {cl} has cm={old_cm} (should be {new_cm})")


if __name__ == '__main__':
    main()
