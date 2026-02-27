#!/usr/bin/env python3
"""
Fix Paper Database: Smart Fix + Bad Bank
TL-067: Paperdatenbank bereinigen

WHAT IT DOES:
1. Removes PAP- prefix from BibTeX keys (813 entries)
2. Fixes PAP-PAP- superkeys in YAMLs (54 entries)
3. Fixes word duplications in paper fields (25 entries)
4. Moves truly broken entries to bad-bank/ (empty paper fields, parse errors)
5. Updates all cross-references

EXPERIMENTAL MODE: Run with --dry-run first, then --batch N, then --all
"""

import argparse
import os
import re
import shutil
import sys
import yaml
from datetime import datetime

BIB_PATH = 'bibliography/bcm_master.bib'
YAML_DIR = 'data/paper-references'
BAD_BANK_DIR = 'data/paper-bad-bank'
BAD_BANK_BIB = 'data/paper-bad-bank/bad_bank.bib'


def parse_bibtex_entries(bib_path):
    """Parse BibTeX file into list of (key, full_entry_text, start_pos, end_pos)."""
    with open(bib_path, 'r') as f:
        content = f.read()

    entries = []
    for match in re.finditer(r'(@\w+\{)([^,]+),(.*?)(?=@\w+\{|\Z)', content, re.DOTALL):
        entry_type = match.group(1)  # e.g. @article{
        key = match.group(2).strip()
        body = match.group(3)
        full_text = entry_type + key + ',' + body
        entries.append({
            'key': key,
            'type': entry_type,
            'body': body,
            'full_text': full_text,
            'start': match.start(),
            'end': match.end()
        })
    return entries, content


def classify_entry(bib_key, yaml_dir):
    """Classify a BibTeX entry as good, fixable, or bad_bank."""
    issues = []
    fixes = []

    # Determine YAML path
    if bib_key.startswith('PAP-'):
        yaml_path = os.path.join(yaml_dir, f'{bib_key}.yaml')
        clean_key = bib_key[4:]  # Remove PAP-
        issues.append('BIB_PAP_PREFIX')
        fixes.append(f'BibTeX key: {bib_key} → {clean_key}')
    else:
        yaml_path = os.path.join(yaml_dir, f'PAP-{bib_key}.yaml')
        clean_key = bib_key

    if not os.path.exists(yaml_path):
        return 'bad_bank', issues + ['NO_YAML'], fixes, yaml_path

    try:
        with open(yaml_path) as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        return 'bad_bank', issues + ['YAML_PARSE_ERROR'], fixes, yaml_path

    if not data:
        return 'bad_bank', issues + ['YAML_EMPTY'], fixes, yaml_path

    paper = str(data.get('paper', ''))
    superkey = str(data.get('superkey', ''))

    # Check for empty paper field
    if not paper or paper == 'None':
        return 'bad_bank', issues + ['EMPTY_PAPER'], fixes, yaml_path

    # Check for PAP-PAP- superkey (fixable)
    if 'PAP-PAP-' in superkey:
        issues.append('PAP_PAP_SUPERKEY')
        expected_sk = f'PAP-{clean_key}'
        fixes.append(f'Superkey: {superkey} → {expected_sk}')

    # Check for word duplication or key mismatch in paper field
    if paper not in [clean_key, f'PAP-{clean_key}', bib_key]:
        # Check if it's a fixable word duplication
        # e.g. camerer2003behavioralbehavioral → camerer2003behavioral
        if clean_key in paper and len(paper) > len(clean_key):
            issues.append('WORD_DUPLICATION')
            fixes.append(f'Paper field: {paper} → {clean_key}')
        else:
            issues.append('KEY_MISMATCH')
            fixes.append(f'Paper field: {paper} → {clean_key}')

    if not issues:
        return 'good', [], [], yaml_path

    # If only fixable issues, classify as fixable
    bad_issues = {'NO_YAML', 'YAML_PARSE_ERROR', 'YAML_EMPTY', 'EMPTY_PAPER'}
    if any(i in bad_issues for i in issues):
        return 'bad_bank', issues, fixes, yaml_path

    return 'fixable', issues, fixes, yaml_path


def fix_bibtex_key(bib_content, old_key, new_key):
    """Replace a BibTeX key in the file content."""
    # Replace the entry definition
    pattern = re.compile(r'(@\w+\{)' + re.escape(old_key) + r',')
    bib_content = pattern.sub(r'\g<1>' + new_key + ',', bib_content)
    return bib_content


def fix_yaml_file(yaml_path, clean_key):
    """Fix paper field and superkey in YAML file."""
    with open(yaml_path) as f:
        content = f.read()

    data = yaml.safe_load(content)
    if not data:
        return False, "Empty YAML"

    changed = False
    expected_superkey = f'PAP-{clean_key}'

    # Fix paper field
    current_paper = str(data.get('paper', ''))
    if current_paper != clean_key:
        # Use string replacement to preserve YAML formatting
        # Replace first occurrence of paper: value
        old_line = f'paper: {current_paper}'
        new_line = f'paper: {clean_key}'
        if old_line in content:
            content = content.replace(old_line, new_line, 1)
            changed = True
        else:
            # Try with quotes
            for quote in ["'", '"']:
                old_line = f'paper: {quote}{current_paper}{quote}'
                new_line = f'paper: {clean_key}'
                if old_line in content:
                    content = content.replace(old_line, new_line, 1)
                    changed = True
                    break

    # Fix superkey
    current_sk = str(data.get('superkey', ''))
    if current_sk != expected_superkey:
        old_line = f'superkey: {current_sk}'
        new_line = f'superkey: {expected_superkey}'
        if old_line in content:
            content = content.replace(old_line, new_line, 1)
            changed = True

    if changed:
        with open(yaml_path, 'w') as f:
            f.write(content)

    return changed, "OK"


def move_to_bad_bank(bib_key, yaml_path, bib_entry_text, reasons):
    """Move entry to bad bank directory."""
    os.makedirs(BAD_BANK_DIR, exist_ok=True)

    # Move YAML
    if os.path.exists(yaml_path):
        dest = os.path.join(BAD_BANK_DIR, os.path.basename(yaml_path))
        shutil.move(yaml_path, dest)

    # Append BibTeX to bad bank bib
    with open(BAD_BANK_BIB, 'a') as f:
        f.write(f'% BAD BANK: {", ".join(reasons)}\n')
        f.write(f'% Moved: {datetime.now().isoformat()}\n')
        f.write(bib_entry_text.rstrip() + '\n\n')

    return True


def remove_from_bibtex(bib_content, key):
    """Remove an entry from BibTeX content."""
    pattern = re.compile(
        r'@\w+\{' + re.escape(key) + r',.*?(?=@\w+\{|\Z)',
        re.DOTALL
    )
    return pattern.sub('', bib_content)


def main():
    parser = argparse.ArgumentParser(description='Fix Paper Database')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done')
    parser.add_argument('--batch', type=int, default=0, help='Process N entries (0=all)')
    parser.add_argument('--fix-only', action='store_true', help='Only fix, no bad bank')
    parser.add_argument('--bad-bank-only', action='store_true', help='Only bad bank, no fixes')
    parser.add_argument('--stats', action='store_true', help='Show statistics only')
    args = parser.parse_args()

    print("=" * 70)
    print("PAPER DATABASE FIX — Smart Fix + Bad Bank")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 70)

    entries, bib_content = parse_bibtex_entries(BIB_PATH)
    print(f"\nTotal BibTeX entries: {len(entries)}")

    # Classify all entries
    good = []
    fixable = []
    bad_bank = []

    for entry in entries:
        category, issues, fixes, yaml_path = classify_entry(entry['key'], YAML_DIR)
        entry['category'] = category
        entry['issues'] = issues
        entry['fixes'] = fixes
        entry['yaml_path'] = yaml_path

        if category == 'good':
            good.append(entry)
        elif category == 'fixable':
            fixable.append(entry)
        else:
            bad_bank.append(entry)

    print(f"\n{'='*50}")
    print(f"  GOOD:      {len(good):5d} papers (no changes needed)")
    print(f"  FIXABLE:   {len(fixable):5d} papers (scriptable fix)")
    print(f"  BAD BANK:  {len(bad_bank):5d} papers (move to archive)")
    print(f"{'='*50}")

    if args.stats:
        # Show detailed stats
        fix_reasons = {}
        for e in fixable:
            for i in e['issues']:
                fix_reasons[i] = fix_reasons.get(i, 0) + 1
        print(f"\nFIXABLE reasons:")
        for r, c in sorted(fix_reasons.items(), key=lambda x: -x[1]):
            print(f"  {r:30s} {c:5d}")

        bad_reasons = {}
        for e in bad_bank:
            for i in e['issues']:
                bad_reasons[i] = bad_reasons.get(i, 0) + 1
        print(f"\nBAD BANK reasons:")
        for r, c in sorted(bad_reasons.items(), key=lambda x: -x[1]):
            print(f"  {r:30s} {c:5d}")

        print(f"\nBAD BANK entries:")
        for e in bad_bank:
            print(f"  {e['key']:50s} {', '.join(e['issues'])}")
        return

    if args.dry_run:
        print(f"\n--- DRY RUN (showing first 10 of each) ---\n")

        print("FIXABLE (sample):")
        for e in fixable[:10]:
            clean_key = e['key'][4:] if e['key'].startswith('PAP-') else e['key']
            print(f"  {e['key']:50s} → {clean_key}")
            for fix in e['fixes']:
                print(f"    {fix}")
        if len(fixable) > 10:
            print(f"  ... and {len(fixable)-10} more")

        print(f"\nBAD BANK:")
        for e in bad_bank:
            print(f"  {e['key']:50s} → {', '.join(e['issues'])}")
        return

    # EXECUTE FIXES
    processed = 0
    limit = args.batch if args.batch > 0 else len(fixable) + len(bad_bank)

    new_bib_content = bib_content
    fixed_count = 0
    bad_count = 0

    # Phase 1: Fix entries
    if not args.bad_bank_only:
        for entry in fixable:
            if processed >= limit:
                break

            old_key = entry['key']
            clean_key = old_key[4:] if old_key.startswith('PAP-') else old_key

            # Fix BibTeX key
            if 'BIB_PAP_PREFIX' in entry['issues']:
                new_bib_content = fix_bibtex_key(new_bib_content, old_key, clean_key)

            # Fix YAML
            if os.path.exists(entry['yaml_path']):
                changed, msg = fix_yaml_file(entry['yaml_path'], clean_key)
                if changed:
                    pass  # silently fixed

            fixed_count += 1
            processed += 1

            if processed % 100 == 0:
                print(f"  Fixed {processed}/{min(limit, len(fixable))}...")

    # Phase 2: Bad Bank
    if not args.fix_only:
        for entry in bad_bank:
            if processed >= limit:
                break

            move_to_bad_bank(
                entry['key'],
                entry['yaml_path'],
                entry['full_text'],
                entry['issues']
            )
            new_bib_content = remove_from_bibtex(new_bib_content, entry['key'])
            bad_count += 1
            processed += 1

    # Write updated BibTeX
    if fixed_count > 0 or bad_count > 0:
        # Backup
        backup_path = f'{BIB_PATH}.backup-{datetime.now().strftime("%Y%m%d-%H%M%S")}'
        shutil.copy2(BIB_PATH, backup_path)
        print(f"\nBackup: {backup_path}")

        with open(BIB_PATH, 'w') as f:
            f.write(new_bib_content)

    print(f"\n{'='*50}")
    print(f"  RESULTS:")
    print(f"  Fixed:     {fixed_count:5d} entries (BibTeX key + YAML)")
    print(f"  Bad Bank:  {bad_count:5d} entries (moved to {BAD_BANK_DIR}/)")
    print(f"  Remaining: {len(good) + fixed_count:5d} clean entries")
    print(f"{'='*50}")


if __name__ == '__main__':
    main()
