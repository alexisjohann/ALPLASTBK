#!/usr/bin/env python3
"""
Fix Content Levels in Paper Database (Definition 2: STRUCTURAL)

Content Level Definition 2 (from CLAUDE.md):
  L0: Metadata only (no S1-S6) - title, author, year but NO research question, NO classification
  L1: Research Question known (S1) - has use_for or theory_support or abstract with substance
  L2: Summary/Extract (S1-S4, no full text) - has key_findings_structured with substance
  L3: COMPLETE original text + References in data/paper-texts/

L0 Criteria (ALL must be true):
  - No abstract OR abstract is empty/trivial (<50 chars)
  - No key_findings_structured OR empty
  - No behavioral_mapping OR empty
  - No summary OR empty
  (use_for alone does NOT qualify for L1 - it's just a routing tag)

L2 Criteria (must have substantial content):
  - Has key_findings_structured with >=3 findings
  - OR has structural_characteristics block (S1-S6)
  - OR has full_text file that is a summary/extract (exists but <5000 words)

L3 Criteria:
  - Full text file exists in data/paper-texts/
  - File has >5000 words (genuine full paper)
  - All R1-R4 requirements met

Usage:
  python scripts/fix_content_levels.py --dry-run          # Show what would change
  python scripts/fix_content_levels.py --batch 1          # Fix 1 paper (test)
  python scripts/fix_content_levels.py --batch 10         # Fix 10 papers
  python scripts/fix_content_levels.py                    # Fix all
  python scripts/fix_content_levels.py --stats            # Show statistics only
  python scripts/fix_content_levels.py --orphans          # List orphaned full-text files
  python scripts/fix_content_levels.py --fix-prior-scores # Fix papers missing prior_score
"""

import os
import sys
import glob
import re
import argparse
from collections import Counter


PAPER_DIR = "data/paper-references"
TEXT_DIR = "data/paper-texts"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read_yaml_simple(filepath):
    """Read YAML file and extract key fields without pyyaml dependency."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    result = {
        'content': content,
        'filepath': filepath,
        'filename': os.path.basename(filepath),
    }

    # Extract superkey
    m = re.search(r'^superkey:\s*"?([^"\n]+)"?', content, re.MULTILINE)
    result['superkey'] = m.group(1).strip() if m else None

    # Extract paper field
    m = re.search(r'^paper:\s*"?([^"\n]+)"?', content, re.MULTILINE)
    result['paper'] = m.group(1).strip() if m else None

    # Extract current content_level from prior_score
    m = re.search(r'prior_score:.*?content_level:\s*"?(\w+)"?', content, re.DOTALL)
    result['prior_content_level'] = m.group(1).strip() if m else None

    # Extract full_text.content_level
    m = re.search(r'full_text:.*?content_level:\s*"?([^"\n]+)"?', content, re.DOTALL)
    result['full_text_content_level'] = m.group(1).strip() if m else None

    # Check for prior_score block existence
    result['has_prior_score'] = 'prior_score:' in content

    # Extract full_text.available
    m = re.search(r'full_text:.*?available:\s*(true|false)', content, re.DOTALL)
    result['full_text_available'] = m.group(1) == 'true' if m else False

    # Extract full_text.path
    m = re.search(r'full_text:.*?path:\s*"?([^"\n]+)"?', content, re.DOTALL)
    result['full_text_path'] = m.group(1).strip() if m else None

    # Check abstract - can be top-level or indented
    abstract_text = ""
    # Try top-level multiline (abstract: text\n  continuation\n  continuation)
    m = re.search(r'^abstract:\s+(.+(?:\n  .+)*)', content, re.MULTILINE)
    if m:
        abstract_text = m.group(1).strip()
    if not abstract_text:
        # Try indented multiline
        m = re.search(r'^\s+abstract:\s*[|>]-?\s*\n((?:\s{4,}.+\n)*)', content, re.MULTILINE)
        if m:
            abstract_text = m.group(1).strip()
    if not abstract_text:
        # Try indented single-line
        m = re.search(r'^\s+abstract:\s*"([^"]*)"', content, re.MULTILINE)
        if m:
            abstract_text = m.group(1).strip()
    if not abstract_text:
        m = re.search(r'^\s+abstract:\s+(.+)$', content, re.MULTILINE)
        if m:
            val = m.group(1).strip().strip('"')
            if val and val != 'null' and val != '~':
                abstract_text = val
    result['abstract'] = abstract_text
    result['has_abstract'] = len(abstract_text) > 50

    # Check key_findings_structured
    result['has_key_findings'] = 'key_findings_structured:' in content
    # Count findings (lines starting with "  - finding:")
    findings = re.findall(r'^\s+- finding:', content, re.MULTILINE)
    result['findings_count'] = len(findings)

    # Check behavioral_mapping
    result['has_behavioral_mapping'] = 'behavioral_mapping:' in content
    # Check if behavioral_mapping has actual content (not just empty)
    bm_match = re.search(r'behavioral_mapping:\s*\n((?:    .+\n)*)', content, re.MULTILINE)
    result['behavioral_mapping_populated'] = bool(bm_match and len(bm_match.group(1).strip()) > 20)

    # Check summary
    result['has_summary'] = bool(re.search(r'^\s+summary:\s*[|>]?\s*\S', content, re.MULTILINE))

    # Check use_for (can be under ebf_integration: or top-level)
    result['has_use_for'] = 'use_for:' in content
    # Check if use_for has actual entries
    use_for_entries = re.findall(r'use_for:\s*\n(\s+-\s+\S+)', content)
    result['use_for_populated'] = len(use_for_entries) > 0

    # Check theory_support
    result['has_theory_support'] = 'theory_support:' in content
    ts_match = re.search(r'theory_support:\s*\[([^\]]*)\]', content)
    if ts_match:
        result['theory_support_populated'] = len(ts_match.group(1).strip()) > 0
    else:
        result['theory_support_populated'] = bool(re.search(r'theory_support:\s*\n\s+-', content))

    # Check structural_characteristics
    result['has_structural_chars'] = 'structural_characteristics:' in content

    # Check title
    m = re.search(r'^\s+title:\s*"?([^"\n]+)"?', content, re.MULTILINE)
    result['title'] = m.group(1).strip() if m else ""

    return result


def get_full_text_word_count(paper_key):
    """Count words in a paper's full text file."""
    text_path = os.path.join(BASE_DIR, TEXT_DIR, f"PAP-{paper_key}.md")
    if not os.path.exists(text_path):
        # Try without PAP- prefix
        text_path = os.path.join(BASE_DIR, TEXT_DIR, f"{paper_key}.md")
        if not os.path.exists(text_path):
            return 0

    with open(text_path, 'r', encoding='utf-8') as f:
        text = f.read()
    return len(text.split())


def determine_content_level(paper_data):
    """Determine the correct content level based on structural Definition 2."""
    paper_key = paper_data.get('paper', '')

    # L3: Full text exists and is genuine (>5000 words)
    text_path = os.path.join(BASE_DIR, TEXT_DIR, f"PAP-{paper_key}.md")
    if os.path.exists(text_path):
        word_count = get_full_text_word_count(paper_key)
        if word_count > 5000:
            return 'L3', f"full text {word_count} words"

    # L2: Has substantial structured content (S1-S4)
    if paper_data['has_structural_chars']:
        return 'L2', "has structural_characteristics (S1-S6)"

    if paper_data['findings_count'] >= 3 and paper_data['has_abstract']:
        return 'L2', f"{paper_data['findings_count']} findings + abstract"

    # Check if full text file exists but is a summary (<5000 words)
    if os.path.exists(text_path):
        word_count = get_full_text_word_count(paper_key)
        if word_count > 0:
            return 'L2', f"summary/extract in paper-texts ({word_count} words)"

    # L1: Has research question / meaningful classification
    # use_for with actual entries means someone classified this paper = L1
    if paper_data['has_abstract']:
        return 'L1', "abstract (>50 chars)"

    if paper_data['theory_support_populated']:
        return 'L1', "theory_support populated"

    if paper_data['has_key_findings'] and paper_data['findings_count'] >= 1:
        return 'L1', f"{paper_data['findings_count']} finding(s)"

    if paper_data['has_behavioral_mapping'] and paper_data['behavioral_mapping_populated']:
        return 'L1', "behavioral_mapping populated"

    if paper_data.get('use_for_populated') and paper_data.get('title', ''):
        return 'L1', "use_for classified"

    # L0: Truly metadata only — no abstract, no classification, no findings
    return 'L0', "metadata only"


def update_content_level(paper_data, new_level, reason):
    """Update content level in YAML file."""
    content = paper_data['content']
    filepath = paper_data['filepath']

    # Update prior_score.content_level
    old_level = paper_data['prior_content_level']
    if old_level and old_level != new_level:
        # Replace in prior_score block
        content = re.sub(
            r'(prior_score:.*?content_level:\s*)"?' + re.escape(old_level) + r'"?',
            r'\g<1>' + new_level,
            content,
            count=1,
            flags=re.DOTALL
        )

    # Update full_text.content_level compound encoding
    ft_level = paper_data.get('full_text_content_level', '')
    if ft_level and len(ft_level) >= 2:
        # The compound encoding: position 1 = overall level
        new_compound = new_level + ft_level[2:] if len(ft_level) > 2 else new_level
        if ft_level != new_compound:
            content = re.sub(
                r'(full_text:.*?content_level:\s*)"?' + re.escape(ft_level) + r'"?',
                r'\g<1>' + new_compound,
                content,
                count=1,
                flags=re.DOTALL
            )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return True


def add_prior_score_block(paper_data):
    """Add a minimal prior_score block to papers that lack one."""
    content = paper_data['content']
    filepath = paper_data['filepath']

    if paper_data['has_prior_score']:
        return False

    # Determine level
    new_level, reason = determine_content_level(paper_data)

    # Add prior_score block before full_text block or at end
    prior_block = f"""
prior_score:
  composite_score: 0.0
  content_level: {new_level}
  confidence_multiplier: {"0.60" if new_level == "L0" else "0.80" if new_level == "L1" else "0.95" if new_level == "L2" else "1.00"}
  temporal_decay: 1.0
  last_calculated: "2026-02-09"
"""

    # Insert before full_text: block
    ft_pos = content.find('\nfull_text:')
    if ft_pos > 0:
        content = content[:ft_pos] + prior_block + content[ft_pos:]
    else:
        content = content.rstrip() + '\n' + prior_block

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return True


def find_orphaned_full_texts():
    """Find full-text .md files with no corresponding YAML."""
    text_dir = os.path.join(BASE_DIR, TEXT_DIR)
    if not os.path.exists(text_dir):
        return []

    orphans = []
    for md_file in sorted(glob.glob(os.path.join(text_dir, "*.md"))):
        basename = os.path.basename(md_file)
        if basename == "README.md":
            continue

        # Derive expected YAML path
        yaml_name = basename.replace('.md', '.yaml')
        if not yaml_name.startswith('PAP-'):
            yaml_name = 'PAP-' + yaml_name

        yaml_path = os.path.join(BASE_DIR, PAPER_DIR, yaml_name)
        if not os.path.exists(yaml_path):
            word_count = len(open(md_file, 'r', encoding='utf-8').read().split())
            orphans.append({
                'file': basename,
                'words': word_count,
                'path': md_file
            })

    return orphans


def main():
    parser = argparse.ArgumentParser(description='Fix content levels in paper database')
    parser.add_argument('--dry-run', action='store_true', help='Show changes without applying')
    parser.add_argument('--batch', type=int, default=0, help='Process only N papers')
    parser.add_argument('--stats', action='store_true', help='Show statistics only')
    parser.add_argument('--orphans', action='store_true', help='List orphaned full-text files')
    parser.add_argument('--fix-prior-scores', action='store_true', help='Add prior_score to papers missing it')
    parser.add_argument('--verbose', action='store_true', help='Show detailed output')
    args = parser.parse_args()

    paper_dir = os.path.join(BASE_DIR, PAPER_DIR)
    yaml_files = sorted(glob.glob(os.path.join(paper_dir, "PAP-*.yaml")))

    if args.orphans:
        orphans = find_orphaned_full_texts()
        print(f"\n{'='*60}")
        print(f"ORPHANED FULL-TEXT FILES ({len(orphans)} found)")
        print(f"{'='*60}")
        for o in orphans:
            print(f"  {o['file']:50s} {o['words']:>6d} words")
        return

    print(f"\nScanning {len(yaml_files)} paper YAML files...")

    # Analyze all papers
    level_counts_before = Counter()
    level_counts_after = Counter()
    changes = []
    missing_prior = []

    processed = 0
    for i, yaml_file in enumerate(yaml_files):
        data = read_yaml_simple(yaml_file)
        old_level = data['prior_content_level'] or 'NONE'
        level_counts_before[old_level] += 1

        if not data['has_prior_score']:
            missing_prior.append(data)

        new_level, reason = determine_content_level(data)
        level_counts_after[new_level] += 1

        if args.stats:
            continue

        if old_level != new_level:
            changes.append({
                'file': data['filename'],
                'old': old_level,
                'new': new_level,
                'reason': reason,
                'title': data['title'][:60],
                'data': data,
            })

        if args.batch > 0 and len(changes) >= args.batch:
            # Continue counting for stats but stop collecting changes
            continue

    if args.stats:
        print(f"\n{'='*60}")
        print(f"CONTENT LEVEL STATISTICS")
        print(f"{'='*60}")
        print(f"\n{'Level':<8} {'Current':>10} {'Should Be':>10} {'Delta':>8}")
        print(f"{'-'*36}")
        for level in ['L0', 'L1', 'L2', 'L3', 'NONE']:
            before = level_counts_before.get(level, 0)
            after = level_counts_after.get(level, 0)
            delta = after - before
            delta_str = f"+{delta}" if delta > 0 else str(delta)
            if delta != 0:
                print(f"{level:<8} {before:>10} {after:>10} {delta_str:>8}  ←")
            else:
                print(f"{level:<8} {before:>10} {after:>10} {delta_str:>8}")

        print(f"\nMissing prior_score block: {len(missing_prior)}")
        if missing_prior:
            for mp in missing_prior[:10]:
                print(f"  - {mp['filename']}")
            if len(missing_prior) > 10:
                print(f"  ... and {len(missing_prior) - 10} more")

        return

    # Show changes
    if not changes and not (args.fix_prior_scores and missing_prior):
        print("No changes needed.")
        return

    # Level change summary
    change_types = Counter()
    for c in changes:
        change_types[f"{c['old']}→{c['new']}"] += 1

    print(f"\n{'='*60}")
    print(f"CONTENT LEVEL CHANGES ({len(changes)} papers)")
    print(f"{'='*60}")
    for ct, count in change_types.most_common():
        print(f"  {ct}: {count}")

    if args.verbose or len(changes) <= 20:
        print(f"\nDetails:")
        for c in changes:
            print(f"  {c['file']:45s} {c['old']:>4s} → {c['new']:<4s}  ({c['reason']})")

    if args.fix_prior_scores and missing_prior:
        print(f"\nMissing prior_score: {len(missing_prior)} papers")

    if args.dry_run:
        print(f"\n[DRY RUN] No changes applied.")
        return

    # Apply changes
    applied = 0
    for c in changes:
        if update_content_level(c['data'], c['new'], c['reason']):
            applied += 1

    prior_fixed = 0
    if args.fix_prior_scores:
        for mp in missing_prior:
            if add_prior_score_block(mp):
                prior_fixed += 1

    print(f"\n{'='*60}")
    print(f"APPLIED: {applied} content level changes")
    if prior_fixed:
        print(f"APPLIED: {prior_fixed} prior_score blocks added")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
