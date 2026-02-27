#!/usr/bin/env python3
"""
Update integration_level in Paper-YAMLs based on actual ebf_integration content.

Computes the correct integration level using the same hierarchy as
validate_paper_yaml_schema.py and updates stored values.

Hierarchy (highest priority first):
  I5: appendix_refs AND chapter_refs
  I4: parameter (in ebf_integration or parameter_registry)
  I3: case_links
  I2: theory_support matching MS-XX-NNN
  I1: use_for or evidence_tier
  I0: none of above

Usage:
    python scripts/update_integration_levels.py [--dry-run] [--limit N] [--stats]
"""

import re
import os
import sys
import glob

YAML_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'paper-references')

# Quality score mapping for integration level
Q_I_MAP = {
    'I0': 0.0,
    'I1': 0.2,
    'I2': 0.4,
    'I3': 0.6,
    'I4': 0.8,
    'I5': 1.0,
}


def compute_integration_level(text):
    """Compute integration level from YAML text content."""
    # Extract ebf_integration section
    ebf_match = re.search(r'ebf_integration:\s*\n((?:  \S.*\n|  \n)*)', text)
    if not ebf_match:
        return 'I0', 'no_ebf'

    ebf_text = ebf_match.group(1)

    # Check I5: appendix_refs AND chapter_refs
    has_appendix = bool(re.search(r'appendix_refs:', ebf_text))
    has_chapter = bool(re.search(r'chapter_refs:', ebf_text))
    if has_appendix and has_chapter:
        return 'I5', 'appendix+chapter'

    # Check I4: parameter (in ebf_integration or parameter_registry)
    has_param_ebf = bool(re.search(r'  parameter:', ebf_text))
    # Also check parameter_registry at top level
    has_param_reg = bool(re.search(r'^parameter_registry:', text, re.MULTILINE))
    # Also check top-level parameters:
    has_params_top = bool(re.search(r'^parameters:', text, re.MULTILINE))
    if has_param_ebf or has_param_reg or has_params_top:
        return 'I4', 'parameter'

    # Check I3: case_links
    has_case = bool(re.search(r'case_links:', ebf_text))
    if has_case:
        # Verify it has actual content (not just empty)
        case_match = re.search(r'case_links:\s*\n((?:\s+-\s+.+\n)*)', ebf_text)
        if case_match and case_match.group(1).strip():
            return 'I3', 'case_links'
        # Also check single-value format
        case_single = re.search(r'case_links:\s+(\S+)', ebf_text)
        if case_single and case_single.group(1) not in ('null', '~', '[]'):
            return 'I3', 'case_links'

    # Check I2: theory_support with MS-XX-NNN pattern
    ts_match = re.search(r'theory_support:', ebf_text)
    if ts_match:
        # Get the theory_support content (list or single value)
        ts_section = ebf_text[ts_match.start():]
        if re.search(r'MS-[A-Z]{2}-\d{3}', ts_section):
            return 'I2', 'theory_support'

    # Check I1: use_for or evidence_tier
    has_use_for = bool(re.search(r'use_for:', ebf_text))
    has_tier = bool(re.search(r'evidence_tier:', ebf_text))
    if has_use_for or has_tier:
        return 'I1', 'use_for/tier'

    return 'I0', 'empty_ebf'


def get_stored_level(text):
    """Get stored integration level(s) from YAML text."""
    levels = {}

    # Check top-level integration_level (new format)
    top_match = re.search(r'^integration_level:\s*(\S+)', text, re.MULTILINE)
    if top_match:
        val = top_match.group(1).strip()
        # Normalize: "2" → "I2", "I2" → "I2"
        if val.isdigit():
            val = f'I{val}'
        levels['top'] = val

    # Check prior_score.integration_level (old format)
    ps_match = re.search(r'prior_score:\s*\n((?:  \S.*\n|  \n)*)', text)
    if ps_match:
        ps_text = ps_match.group(1)
        il_match = re.search(r'integration_level:\s*(\S+)', ps_text)
        if il_match:
            val = il_match.group(1).strip()
            if val.isdigit():
                val = f'I{val}'
            levels['prior_score'] = val

    return levels


def update_integration_level(text, new_level):
    """Update integration_level in YAML text. Returns modified text and change count."""
    changes = 0
    new_text = text

    # Update top-level integration_level (new format)
    # Matches: "integration_level: 2" or "integration_level: I2" at line start
    def replace_top(m):
        old_val = m.group(1)
        if old_val.isdigit():
            return f'integration_level: {new_level.replace("I", "")}'
        return f'integration_level: {new_level}'

    new_text_2 = re.sub(r'^integration_level:\s*(\S+)', replace_top, new_text,
                         count=1, flags=re.MULTILINE)
    if new_text_2 != new_text:
        changes += 1
        new_text = new_text_2

    # Update prior_score.integration_level (old format)
    # Matches: "  integration_level: I1" (indented under prior_score)
    def replace_ps(m):
        old_val = m.group(1)
        if old_val.isdigit():
            return f'  integration_level: {new_level.replace("I", "")}'
        return f'  integration_level: {new_level}'

    new_text_2 = re.sub(r'^  integration_level:\s*(\S+)', replace_ps, new_text,
                         count=1, flags=re.MULTILINE)
    if new_text_2 != new_text:
        changes += 1
        new_text = new_text_2

    return new_text, changes


def update_quality_score(text, new_level):
    """Update q_I and q_total in quality_score if present."""
    new_q_i = Q_I_MAP.get(new_level, 0.0)

    # Find current q_I and q_C
    qi_match = re.search(r'    q_I:\s*([0-9.]+)', text)
    qc_match = re.search(r'    q_C:\s*([0-9.]+)', text)
    if not qi_match or not qc_match:
        return text, 0

    old_q_i = float(qi_match.group(1))
    if abs(old_q_i - new_q_i) < 0.001:
        return text, 0  # No change needed

    q_c = float(qc_match.group(1))
    new_q_total = round((q_c + new_q_i) / 2, 3)

    # Replace q_I
    text = re.sub(r'(    q_I:\s*)[0-9.]+', f'\\g<1>{new_q_i}', text, count=1)
    # Replace q_total
    text = re.sub(r'(    q_total:\s*)[0-9.]+', f'\\g<1>{new_q_total}', text, count=1)

    return text, 1


def main():
    dry_run = '--dry-run' in sys.argv
    stats_only = '--stats' in sys.argv
    limit = None
    for i, arg in enumerate(sys.argv):
        if arg == '--limit' and i + 1 < len(sys.argv):
            limit = int(sys.argv[i + 1])

    yaml_files = sorted(glob.glob(os.path.join(YAML_DIR, 'PAP-*.yaml')))
    print(f"Found {len(yaml_files)} Paper-YAMLs\n")

    # Compute levels and find discrepancies
    level_computed = {'I0': 0, 'I1': 0, 'I2': 0, 'I3': 0, 'I4': 0, 'I5': 0}
    level_stored = {'I0': 0, 'I1': 0, 'I2': 0, 'I3': 0, 'I4': 0, 'I5': 0}
    changes_needed = []
    errors = []

    for yf in yaml_files:
        fname = os.path.basename(yf)
        try:
            with open(yf, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            errors.append((fname, str(e)))
            continue

        computed, reason = compute_integration_level(text)
        stored = get_stored_level(text)

        level_computed[computed] = level_computed.get(computed, 0) + 1

        # Get effective stored level (prefer prior_score, fall back to top)
        stored_val = stored.get('prior_score', stored.get('top', None))
        if stored_val:
            level_stored[stored_val] = level_stored.get(stored_val, 0) + 1

        if stored_val and stored_val != computed:
            changes_needed.append((yf, fname, stored_val, computed, reason, stored))

    # Print statistics
    print(f"{'='*60}")
    print(f"  INTEGRATION LEVEL ANALYSIS")
    print(f"{'='*60}\n")

    print(f"  {'Level':<8} {'Stored':<12} {'Computed':<12} {'Delta':<10}")
    print(f"  {'-'*42}")
    total_stored = sum(level_stored.values())
    total_computed = sum(level_computed.values())
    for lvl in ['I0', 'I1', 'I2', 'I3', 'I4', 'I5']:
        s = level_stored.get(lvl, 0)
        c = level_computed.get(lvl, 0)
        delta = c - s
        delta_str = f"+{delta}" if delta > 0 else str(delta)
        print(f"  {lvl:<8} {s:<12} {c:<12} {delta_str:<10}")
    print(f"  {'-'*42}")
    print(f"  {'Total':<8} {total_stored:<12} {total_computed:<12}")
    print()

    # Transition matrix
    transitions = {}
    for _, fname, old, new, reason, _ in changes_needed:
        key = f"{old}→{new}"
        transitions[key] = transitions.get(key, 0) + 1

    print(f"  TRANSITIONS NEEDED: {len(changes_needed)}")
    for trans, count in sorted(transitions.items(), key=lambda x: -x[1]):
        print(f"    {trans}: {count}")
    print()

    if stats_only:
        return

    if not changes_needed:
        print("  All integration levels are already correct!")
        return

    # Apply changes
    if limit:
        changes_needed = changes_needed[:limit]
        print(f"  Limiting to {limit} changes\n")

    updated = 0
    qs_updated = 0
    update_errors = 0

    for yf, fname, old_level, new_level, reason, stored_locs in changes_needed:
        icon = '🔍' if dry_run else '✅'
        print(f"  {icon} {fname}: {old_level}→{new_level} ({reason})")

        if not dry_run:
            try:
                with open(yf, 'r', encoding='utf-8') as f:
                    text = f.read()

                new_text, n_changes = update_integration_level(text, new_level)

                # Also update quality_score if present
                new_text, qs_change = update_quality_score(new_text, new_level)
                if qs_change:
                    qs_updated += 1

                if n_changes > 0 or qs_change > 0:
                    with open(yf, 'w', encoding='utf-8') as f:
                        f.write(new_text)
                    updated += 1
                else:
                    print(f"     ⚠️  No field found to update")
                    update_errors += 1
            except Exception as e:
                print(f"     ❌ Error: {e}")
                update_errors += 1

    print(f"\n{'='*60}")
    print(f"  SUMMARY")
    print(f"{'='*60}")
    print(f"  Changes needed:     {len(changes_needed)}")
    print(f"  Updated:            {updated}")
    print(f"  Quality scores:     {qs_updated}")
    print(f"  Errors:             {update_errors}")
    if dry_run:
        print(f"\n  🔍 DRY RUN — no changes written")
    if errors:
        print(f"\n  Read errors: {len(errors)}")
        for fname, err in errors[:5]:
            print(f"    {fname}: {err}")


if __name__ == '__main__':
    main()
