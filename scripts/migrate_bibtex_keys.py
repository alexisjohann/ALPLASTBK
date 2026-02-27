#!/usr/bin/env python3
"""
migrate_bibtex_keys.py - Rename non-canonical BibTeX keys to canonical format

SSOT: docs/standards/bibtex-key-convention.md
Format: {nachname}{jahr}{kurzwort}
Regex: ^[a-z]+\d{4}[a-z]+$

This script:
1. Identifies non-canonical keys in bcm_master.bib
2. Generates canonical replacements
3. Renames keys in: BibTeX, Paper-YAML, Paper-Text, Queue
4. Updates all cross-references in: theory-catalog, case-registry, etc.

Usage:
    python scripts/migrate_bibtex_keys.py --dry-run                # Preview ALL changes
    python scripts/migrate_bibtex_keys.py --dry-run --limit 1      # Preview 1 key
    python scripts/migrate_bibtex_keys.py --dry-run --limit 10     # Preview 10 keys
    python scripts/migrate_bibtex_keys.py --execute --limit 1      # Migrate 1 key
    python scripts/migrate_bibtex_keys.py --execute --limit 10     # Migrate 10 keys
    python scripts/migrate_bibtex_keys.py --execute                # Migrate ALL keys
    python scripts/migrate_bibtex_keys.py --category underscore    # Only underscore keys
    python scripts/migrate_bibtex_keys.py --category no_kurzwort   # Only missing kurzwort
    python scripts/migrate_bibtex_keys.py --collision-check        # Check for collisions
"""

import re
import os
import sys
import argparse
import shutil
import unicodedata
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
BIBTEX_PATH = PROJECT_ROOT / "bibliography" / "bcm_master.bib"
YAML_DIR = PROJECT_ROOT / "data" / "paper-references"
TEXTS_DIR = PROJECT_ROOT / "data" / "paper-texts"
QUEUE_FILE = PROJECT_ROOT / "data" / "paper-integration-queue.yaml"

# Files that may contain BibTeX key references
CROSS_REF_FILES = [
    PROJECT_ROOT / "data" / "theory-catalog.yaml",
    PROJECT_ROOT / "data" / "case-registry.yaml",
    PROJECT_ROOT / "data" / "parameter-registry.yaml",
    PROJECT_ROOT / "data" / "researcher-registry.yaml",
    PROJECT_ROOT / "data" / "model-registry.yaml",
    PROJECT_ROOT / "data" / "model-building-session.yaml",
    PROJECT_ROOT / "data" / "intervention-registry.yaml",
    PROJECT_ROOT / "data" / "output-registry.yaml",
    PROJECT_ROOT / "data" / "concept-registry.yaml",
    PROJECT_ROOT / "data" / "forecast-registry.yaml",
]

# Directories with YAML files that may reference paper keys
CROSS_REF_DIRS = [
    PROJECT_ROOT / "data" / "paper-intake",
    PROJECT_ROOT / "data" / "customers",
]

# LaTeX directories
LATEX_DIRS = [
    PROJECT_ROOT / "appendices",
    PROJECT_ROOT / "chapters",
]

CANONICAL_PATTERN = re.compile(r'^[a-z]+\d{4}[a-z]+$')

STOP_WORDS = {
    'the', 'a', 'an', 'and', 'or', 'of', 'in', 'on', 'for', 'to', 'with',
    'from', 'by', 'as', 'at', 'about', 'into', 'toward', 'towards', 'beyond',
    'through', 'between', 'among', 'across', 'is', 'are', 'was', 'were',
    'do', 'does', 'did', 'can', 'could', 'will', 'would', 'shall', 'should',
    'may', 'might', 'how', 'what', 'when', 'where', 'why', 'who', 'which',
    'that', 'this', 'not', 'no', 'new', 'its', 'has', 'have', 'been', 'more',
    'some', 'all', 'but', 'than', 'too', 'very', 'just', 'also', 'only'
}


def normalize_ascii(text: str) -> str:
    """Convert accented chars to ASCII."""
    replacements = {
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
        'á': 'a', 'à': 'a', 'â': 'a', 'ä': 'a', 'ã': 'a',
        'ó': 'o', 'ò': 'o', 'ô': 'o', 'ö': 'o', 'õ': 'o',
        'ú': 'u', 'ù': 'u', 'û': 'u', 'ü': 'u',
        'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i',
        'ñ': 'n', 'ç': 'c', 'ß': 'ss', 'ø': 'o', 'å': 'a',
        'æ': 'ae', 'œ': 'oe', 'ð': 'd', 'þ': 'th',
    }
    result = text
    for char, replacement in replacements.items():
        result = result.replace(char, replacement)
        result = result.replace(char.upper(), replacement)
    result = unicodedata.normalize('NFKD', result)
    result = result.encode('ascii', 'ignore').decode('ascii')
    return result


def extract_kurzwort(title: str) -> str:
    """Extract first meaningful word from title."""
    if not title:
        return ''
    clean = re.sub(r'\\[a-zA-Z]+\{([^}]*)\}', r'\1', title)
    clean = re.sub(r'[{}\\$]', '', clean)
    clean = normalize_ascii(clean)
    words = re.findall(r'[a-zA-Z]+', clean)
    for word in words:
        w_lower = word.lower()
        if w_lower not in STOP_WORDS and len(w_lower) >= 3:
            return w_lower
    for word in words:
        if len(word) >= 2:
            return word.lower()
    return ''


def parse_bibtex(bib_path: Path) -> Dict[str, Dict]:
    """Parse BibTeX file into entries."""
    with open(bib_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    entries = {}
    entry_pattern = r'@(\w+)\{([^,]+),([^@]*?)(?=\n@|\Z)'
    for entry_type, key, fields_str in re.findall(entry_pattern, content, re.DOTALL):
        key = key.strip()
        fields = {'_type': entry_type.lower()}
        field_pattern = r'(\w+)\s*=\s*(?:\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}|(\d+))'
        for match in re.finditer(field_pattern, fields_str):
            fname = match.group(1).lower()
            fval = match.group(2) if match.group(2) is not None else match.group(3)
            fields[fname] = fval
        entries[key] = fields
    return entries


def classify_violation(key: str) -> Optional[str]:
    """Classify violation type."""
    if CANONICAL_PATTERN.match(key):
        return None
    if '_' in key:
        return 'has_underscore'
    if key != key.lower():
        return 'has_uppercase'
    if re.match(r'^[a-z]+\d{4}$', key):
        return 'no_kurzwort'
    if not all(ord(c) < 128 for c in key):
        return 'non_ascii'
    if '-' in key:
        return 'has_hyphen'
    if re.match(r'^[a-z]+\d{4}[a-z]*\d+$', key):
        return 'numeric_suffix'
    return 'other'


def generate_canonical_key(old_key: str, entry: Dict, existing_keys: Set[str]) -> str:
    """Generate canonical key, avoiding collisions."""
    title = entry.get('title', '')
    author = entry.get('author', '')
    year = entry.get('year', '')

    # Extract lastname
    if author:
        first_author = author.split(' and ')[0].strip()
        if ',' in first_author:
            lastname = first_author.split(',')[0].strip()
        else:
            parts = first_author.split()
            lastname = parts[-1] if parts else ''
        lastname = normalize_ascii(lastname).lower()
        lastname = re.sub(r'[^a-z]', '', lastname)
    else:
        m = re.match(r'([a-zA-Z_]+?)[\d_]', old_key)
        lastname = m.group(1).replace('_', '').lower() if m else old_key[:6]
        lastname = normalize_ascii(lastname)
        lastname = re.sub(r'[^a-z]', '', lastname)

    if not year:
        m = re.search(r'(\d{4})', old_key)
        year = m.group(1) if m else '0000'

    kurzwort = extract_kurzwort(title)
    if not kurzwort:
        # Try to salvage from old key
        m = re.search(r'\d{4}_?([a-z]+)', old_key.lower().replace('_', ' ').replace(' ', ''))
        kurzwort = m.group(1) if m else 'unknown'

    candidate = f"{lastname}{year}{kurzwort}"

    # Check collision
    if candidate in existing_keys and candidate != old_key:
        # Try longer kurzwort
        clean_title = normalize_ascii(re.sub(r'[{}\\$]', '', title))
        words = [w.lower() for w in re.findall(r'[a-zA-Z]+', clean_title)
                 if w.lower() not in STOP_WORDS and len(w) >= 3]
        if len(words) >= 2:
            candidate = f"{lastname}{year}{words[0]}{words[1]}"
        if candidate in existing_keys:
            # Add suffix
            for i in range(2, 20):
                candidate_i = f"{lastname}{year}{kurzwort}{chr(96+i)}"  # b, c, d, ...
                if candidate_i not in existing_keys:
                    candidate = candidate_i
                    break

    return candidate


def find_references_in_file(filepath: Path, old_key: str) -> List[Tuple[int, str]]:
    """Find all lines in a file containing the old key."""
    matches = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            for i, line in enumerate(f, 1):
                if old_key in line:
                    matches.append((i, line.rstrip()))
    except Exception:
        pass
    return matches


def replace_in_file(filepath: Path, old_key: str, new_key: str) -> int:
    """Replace old_key with new_key in a file. Returns number of replacements."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        count = content.count(old_key)
        if count > 0:
            new_content = content.replace(old_key, new_key)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
        return count
    except Exception as e:
        print(f"  ERROR in {filepath}: {e}")
        return 0


def rename_yaml_file(old_key: str, new_key: str, dry_run: bool) -> bool:
    """Rename PAP-{old_key}.yaml to PAP-{new_key}.yaml."""
    old_path = YAML_DIR / f"PAP-{old_key}.yaml"
    new_path = YAML_DIR / f"PAP-{new_key}.yaml"

    if not old_path.exists():
        return False

    if new_path.exists() and old_key != new_key:
        print(f"  ⚠️  COLLISION: {new_path.name} already exists!")
        return False

    if not dry_run:
        # Update internal references in the YAML file first
        replace_in_file(old_path, old_key, new_key)
        # Then rename
        old_path.rename(new_path)
    return True


def rename_text_file(old_key: str, new_key: str, dry_run: bool) -> bool:
    """Rename PAP-{old_key}.md to PAP-{new_key}.md."""
    old_path = TEXTS_DIR / f"PAP-{old_key}.md"
    new_path = TEXTS_DIR / f"PAP-{new_key}.md"

    if not old_path.exists():
        return False

    if new_path.exists() and old_key != new_key:
        print(f"  ⚠️  COLLISION: {new_path.name} already exists!")
        return False

    if not dry_run:
        old_path.rename(new_path)
    return True


def update_bibtex(old_key: str, new_key: str, dry_run: bool) -> bool:
    """Rename key in bcm_master.bib."""
    if dry_run:
        return True

    with open(BIBTEX_PATH, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    # Replace the key in the @type{key, line
    pattern = re.compile(r'(@\w+\{)' + re.escape(old_key) + r'(,)')
    new_content, count = pattern.subn(r'\g<1>' + new_key + r'\2', content)

    if count == 0:
        print(f"  ⚠️  Key {old_key} not found in BibTeX!")
        return False

    # Also replace any internal references (e.g., crossref = {old_key})
    new_content = new_content.replace(old_key, new_key)

    with open(BIBTEX_PATH, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return True


def update_cross_references(old_key: str, new_key: str, dry_run: bool) -> int:
    """Update all cross-references in YAML/LaTeX files."""
    total_replacements = 0

    # Single YAML files
    for filepath in CROSS_REF_FILES:
        if filepath.exists():
            refs = find_references_in_file(filepath, old_key)
            if refs:
                if not dry_run:
                    count = replace_in_file(filepath, old_key, new_key)
                    total_replacements += count
                else:
                    total_replacements += len(refs)

    # YAML directories
    for dirpath in CROSS_REF_DIRS:
        if dirpath.exists():
            for f in dirpath.rglob('*.yaml'):
                refs = find_references_in_file(f, old_key)
                if refs:
                    if not dry_run:
                        count = replace_in_file(f, old_key, new_key)
                        total_replacements += count
                    else:
                        total_replacements += len(refs)

    # LaTeX files
    for dirpath in LATEX_DIRS:
        if dirpath.exists():
            for f in dirpath.rglob('*.tex'):
                refs = find_references_in_file(f, old_key)
                if refs:
                    if not dry_run:
                        count = replace_in_file(f, old_key, new_key)
                        total_replacements += count
                    else:
                        total_replacements += len(refs)

    # Paper-references YAMLs (other papers may reference this one)
    for f in YAML_DIR.glob('PAP-*.yaml'):
        if f.stem != f"PAP-{old_key}":  # Skip self
            refs = find_references_in_file(f, old_key)
            if refs:
                if not dry_run:
                    count = replace_in_file(f, old_key, new_key)
                    total_replacements += count
                else:
                    total_replacements += len(refs)

    return total_replacements


def migrate_key(old_key: str, new_key: str, dry_run: bool) -> Dict:
    """Migrate a single key. Returns stats dict."""
    stats = {
        'bibtex': False,
        'yaml_renamed': False,
        'text_renamed': False,
        'cross_refs': 0,
    }

    if old_key == new_key:
        return stats

    # 1. Update BibTeX
    stats['bibtex'] = update_bibtex(old_key, new_key, dry_run)

    # 2. Rename YAML
    stats['yaml_renamed'] = rename_yaml_file(old_key, new_key, dry_run)

    # 3. Rename text file
    stats['text_renamed'] = rename_text_file(old_key, new_key, dry_run)

    # 4. Update cross-references
    stats['cross_refs'] = update_cross_references(old_key, new_key, dry_run)

    return stats


def main():
    parser = argparse.ArgumentParser(description='Migrate BibTeX keys to canonical format')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without executing')
    parser.add_argument('--execute', action='store_true', help='Execute migration')
    parser.add_argument('--limit', type=int, default=0, help='Limit number of keys to migrate (0=all)')
    parser.add_argument('--category', type=str, default='all',
                        choices=['all', 'has_underscore', 'no_kurzwort', 'has_uppercase',
                                 'non_ascii', 'has_hyphen', 'numeric_suffix', 'other'],
                        help='Only migrate keys of this category')
    parser.add_argument('--collision-check', action='store_true', help='Check for collisions only')

    args = parser.parse_args()

    if not args.dry_run and not args.execute and not args.collision_check:
        print("ERROR: Specify --dry-run, --execute, or --collision-check")
        sys.exit(1)

    dry_run = args.dry_run or args.collision_check

    # Parse BibTeX
    print(f"\nLoading BibTeX from {BIBTEX_PATH}...")
    entries = parse_bibtex(BIBTEX_PATH)
    print(f"  Found {len(entries)} entries")

    # Find non-canonical keys
    all_keys = set(entries.keys())
    migrations: List[Tuple[str, str, str]] = []  # (old, new, violation_type)

    for key in sorted(entries.keys()):
        violation = classify_violation(key)
        if violation is None:
            continue
        if args.category != 'all' and violation != args.category:
            continue

        new_key = generate_canonical_key(key, entries[key], all_keys)
        migrations.append((key, new_key, violation))
        all_keys.add(new_key)

    print(f"  Keys to migrate: {len(migrations)}")

    if args.limit > 0:
        migrations = migrations[:args.limit]
        print(f"  Limited to: {args.limit}")

    # Check for collisions
    if args.collision_check:
        collisions = [(old, new, v) for old, new, v in migrations if old == new]
        same_target = {}
        for old, new, v in migrations:
            same_target.setdefault(new, []).append(old)
        target_collisions = {k: v for k, v in same_target.items() if len(v) > 1}

        print(f"\n  Self-collisions (old==new): {len(collisions)}")
        for old, new, v in collisions[:10]:
            print(f"    {old} → {new} ({v})")

        print(f"\n  Target collisions (multiple old → same new): {len(target_collisions)}")
        for target, sources in list(target_collisions.items())[:10]:
            print(f"    → {target}: {sources}")
        return

    # Execute migrations
    print(f"\n{'='*70}")
    mode = "DRY RUN" if dry_run else "EXECUTING"
    print(f"  {mode}: Migrating {len(migrations)} keys")
    print(f"{'='*70}")

    total_stats = {'bibtex': 0, 'yaml': 0, 'text': 0, 'xrefs': 0, 'skipped': 0}

    for i, (old_key, new_key, violation) in enumerate(migrations, 1):
        if old_key == new_key:
            total_stats['skipped'] += 1
            continue

        print(f"\n  [{i}/{len(migrations)}] {old_key} → {new_key}  ({violation})")

        stats = migrate_key(old_key, new_key, dry_run)

        if stats['bibtex']:
            total_stats['bibtex'] += 1
        if stats['yaml_renamed']:
            total_stats['yaml'] += 1
        if stats['text_renamed']:
            total_stats['text'] += 1
        total_stats['xrefs'] += stats['cross_refs']

        details = []
        if stats['bibtex']:
            details.append("BIB")
        if stats['yaml_renamed']:
            details.append("YAML")
        if stats['text_renamed']:
            details.append("TXT")
        if stats['cross_refs']:
            details.append(f"XREF:{stats['cross_refs']}")
        print(f"     → {' | '.join(details) if details else 'no changes'}")

    # Summary
    print(f"\n{'='*70}")
    print(f"  SUMMARY ({mode})")
    print(f"{'='*70}")
    print(f"  BibTeX keys renamed:   {total_stats['bibtex']}")
    print(f"  YAML files renamed:    {total_stats['yaml']}")
    print(f"  Text files renamed:    {total_stats['text']}")
    print(f"  Cross-refs updated:    {total_stats['xrefs']}")
    print(f"  Skipped (no change):   {total_stats['skipped']}")

    if dry_run:
        print(f"\n  This was a DRY RUN. Use --execute to apply changes.")
    else:
        print(f"\n  ✅ Migration complete. Run validation:")
        print(f"     python scripts/validate_bibtex_key_format.py --stats")
    print()


if __name__ == '__main__':
    main()
