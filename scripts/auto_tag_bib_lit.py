#!/usr/bin/env python3
"""
auto_tag_bib_lit.py - Automatically add LIT-* tags to BibTeX entries based on author

This script applies the EBF rule:
  - Author has ≥5 papers → gets LIT-R tag (e.g., LIT-THALER)
  - Author has <5 papers → gets LIT-OTHER tag

Usage:
    python scripts/auto_tag_bib_lit.py                    # Report only (dry run)
    python scripts/auto_tag_bib_lit.py --update           # Actually update BibTeX
    python scripts/auto_tag_bib_lit.py --author THALER    # Check specific author
    python scripts/auto_tag_bib_lit.py --threshold 10     # Custom threshold

Author: Claude Code
Version: 1.0 (January 2026)
"""

import re
import sys
import argparse
from pathlib import Path
from collections import Counter, defaultdict
from typing import Dict, List, Tuple, Set, Optional
from dataclasses import dataclass

# =============================================================================
# Author Name Aliases
# =============================================================================
# Maps variant spellings to canonical LIT-Appendix names

AUTHOR_ALIASES = {
    # Kahneman/Tversky -> LIT-KT (file: KTH_kahneman_tversky.tex)
    'KAHNEMAN': 'KT',
    'TVERSKY': 'KT',

    # Benabou variants -> BENABOU (file: RB_LIT-BENABOU_*)
    'BÉNABOU': 'BENABOU',
    'BENABOU': 'BENABOU',

    # Gächter variants -> GAECHTER (file: GCR_LIT-GAECHTER_*)
    'GÄCHTER': 'GAECHTER',
    'GACHTER': 'GAECHTER',
    'GAECHTER': 'GAECHTER',

    # Van den Steen -> VANDENSTEEN (file: EV_LIT-VANDENSTEEN_*)
    'STEEN': 'VANDENSTEEN',
    'VAN DEN STEEN': 'VANDENSTEEN',

    # Fischbacher -> FISCHBACHER (file: FI_LIT-FISCHBACHER_*)
    'FISCHBACHER': 'FISCHBACHER',

    # Ambühl variants
    'AMBÜHL': 'AMBUHL',
    'AMBUHL': 'AMBUHL',

    # Others with special handling
    'JR.': None,  # Skip "Jr." as author
    'III': None,  # Skip roman numerals
    'II': None,
}

# Explicit mapping from canonical name to LIT-Appendix file pattern
# Used when file naming doesn't follow LIT-* convention
EXPLICIT_LIT_FILES = {
    'KT': 'KTH_kahneman_tversky.tex',  # Kahneman/Tversky
}

# =============================================================================
# Data Structures
# =============================================================================

@dataclass
class BibEntry:
    """A BibTeX entry with position info for editing."""
    key: str
    start_pos: int
    end_pos: int
    raw_text: str
    author: Optional[str]
    has_use_for: bool
    existing_lit_tags: List[str]


# =============================================================================
# BibTeX Parsing
# =============================================================================

def parse_bibtex_entries(content: str) -> List[BibEntry]:
    """Parse BibTeX file and extract entries with position info."""
    entries = []

    # Match complete BibTeX entries
    entry_pattern = r'@(\w+)\{([^,]+),(.*?)\n\}'

    for match in re.finditer(r'@\w+\{[^,]+,.*?\n\}', content, re.DOTALL):
        raw = match.group(0)
        start = match.start()
        end = match.end()

        # Extract key
        key_match = re.match(r'@\w+\{([^,]+),', raw)
        if not key_match:
            continue
        key = key_match.group(1).strip()

        # Extract author
        author_match = re.search(r'author\s*=\s*[{"]([^}"]+)[}"]', raw, re.IGNORECASE)
        author = author_match.group(1) if author_match else None

        # Check if use_for exists
        has_use_for = bool(re.search(r'use_for\s*=', raw, re.IGNORECASE))

        # Extract existing LIT tags
        lit_tags = []
        use_for_match = re.search(r'use_for\s*=\s*\{([^}]+)\}', raw, re.IGNORECASE)
        if use_for_match:
            tags = use_for_match.group(1)
            lit_tags = [t.strip() for t in re.findall(r'LIT-\w+', tags, re.IGNORECASE)]

        entries.append(BibEntry(
            key=key,
            start_pos=start,
            end_pos=end,
            raw_text=raw,
            author=author,
            has_use_for=has_use_for,
            existing_lit_tags=lit_tags
        ))

    return entries


def get_primary_author(author_str: str) -> Optional[str]:
    """Extract primary author's last name."""
    if not author_str:
        return None

    # Take first author
    first_author = author_str.split(' and ')[0].strip()

    # Handle "LastName, FirstName" format
    if ',' in first_author:
        last_name = first_author.split(',')[0].strip()
    else:
        # Handle "FirstName LastName" format
        parts = first_author.split()
        last_name = parts[-1].strip() if parts else None

    return last_name.upper() if last_name else None


def get_canonical_lit_name(author: str) -> Optional[str]:
    """Get canonical LIT-Appendix name for an author."""
    if not author:
        return None

    author_upper = author.upper()

    # Check aliases
    if author_upper in AUTHOR_ALIASES:
        canonical = AUTHOR_ALIASES[author_upper]
        if canonical is None:
            return None  # Skip this author
        return canonical

    return author_upper


# =============================================================================
# LIT-Appendix Discovery
# =============================================================================

def discover_existing_lits(appendices_dir: Path) -> Set[str]:
    """Find all existing LIT-Appendix names."""
    existing = set()

    # 1. Find standard LIT-* files
    for filepath in appendices_dir.glob('*LIT*.tex'):
        # Extract LIT name from filename
        match = re.search(r'LIT-([A-Z]+)', filepath.stem, re.IGNORECASE)
        if match:
            existing.add(match.group(1).upper())

    # 2. Add explicit mappings (for non-standard filenames like KTH_kahneman_tversky.tex)
    for canonical_name, filename in EXPLICIT_LIT_FILES.items():
        filepath = appendices_dir / filename
        if filepath.exists():
            existing.add(canonical_name.upper())

    return existing


# =============================================================================
# Main Logic
# =============================================================================

def analyze_bibliography(
    bib_path: Path,
    appendices_dir: Path,
    threshold: int = 5
) -> Tuple[Dict[str, List[BibEntry]], Dict[str, int], Set[str]]:
    """
    Analyze bibliography and determine which entries need LIT tags.

    Returns:
        - entries_by_author: Dict mapping canonical author name to their entries
        - author_counts: Dict with paper counts per author
        - existing_lits: Set of existing LIT-Appendix names
    """
    content = bib_path.read_text(encoding='utf-8')
    entries = parse_bibtex_entries(content)

    # Group by author
    entries_by_author = defaultdict(list)
    for entry in entries:
        primary = get_primary_author(entry.author)
        canonical = get_canonical_lit_name(primary)
        if canonical:
            entries_by_author[canonical].append(entry)

    # Count papers per author
    author_counts = {author: len(entries) for author, entries in entries_by_author.items()}

    # Get existing LITs
    existing_lits = discover_existing_lits(appendices_dir)

    return entries_by_author, author_counts, existing_lits


def add_lit_tag_to_entry(entry: BibEntry, lit_name: str) -> str:
    """Add or update LIT tag in a BibTeX entry."""
    raw = entry.raw_text
    new_tag = f"LIT-{lit_name}"

    if entry.has_use_for:
        # Update existing use_for field
        if new_tag.upper() in [t.upper() for t in entry.existing_lit_tags]:
            return raw  # Already has this tag

        # Add to existing use_for
        def add_tag(match):
            existing = match.group(1)
            return f'use_for = {{{new_tag}, {existing}}}'

        raw = re.sub(r'use_for\s*=\s*\{([^}]+)\}', add_tag, raw, count=1, flags=re.IGNORECASE)
    else:
        # Add new use_for field after author line
        author_match = re.search(r'(author\s*=\s*[{"][^}"]+[}"],?\s*\n)', raw, re.IGNORECASE)
        if author_match:
            insert_pos = author_match.end()
            indent = '  '
            new_field = f'{indent}use_for = {{{new_tag}}},\n'
            raw = raw[:insert_pos] + new_field + raw[insert_pos:]

    return raw


def update_bibliography(
    bib_path: Path,
    entries_by_author: Dict[str, List[BibEntry]],
    author_counts: Dict[str, int],
    existing_lits: Set[str],
    threshold: int = 5,
    dry_run: bool = True
) -> Tuple[int, int, List[str]]:
    """
    Update BibTeX file with LIT tags.

    Returns:
        - tagged_count: Number of entries that were/would be tagged
        - skipped_count: Number of entries skipped (already tagged)
        - warnings: List of warning messages
    """
    content = bib_path.read_text(encoding='utf-8')

    tagged_count = 0
    skipped_count = 0
    warnings = []

    # Process authors with enough papers
    updates = []  # List of (old_text, new_text) pairs

    for author, entries in entries_by_author.items():
        count = author_counts[author]

        if count < threshold:
            continue  # Below threshold, skip

        # Determine LIT name
        if author in existing_lits:
            lit_name = author
        else:
            # Author qualifies but no LIT exists
            warnings.append(f"⚠️  {author} has {count} papers but no LIT-{author} appendix exists!")
            lit_name = author  # Tag anyway for future

        # Process each entry
        for entry in entries:
            if f"LIT-{lit_name}".upper() in [t.upper() for t in entry.existing_lit_tags]:
                skipped_count += 1
                continue

            new_text = add_lit_tag_to_entry(entry, lit_name)
            if new_text != entry.raw_text:
                updates.append((entry.raw_text, new_text))
                tagged_count += 1

    # Apply updates
    if not dry_run and updates:
        for old_text, new_text in updates:
            content = content.replace(old_text, new_text, 1)
        bib_path.write_text(content, encoding='utf-8')

    return tagged_count, skipped_count, warnings


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Auto-tag BibTeX entries with LIT-* based on author',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python scripts/auto_tag_bib_lit.py                    # Report only
    python scripts/auto_tag_bib_lit.py --update           # Update BibTeX
    python scripts/auto_tag_bib_lit.py --author THALER    # Check specific author
    python scripts/auto_tag_bib_lit.py --threshold 10     # Higher threshold
        """
    )
    parser.add_argument('--update', action='store_true',
                        help='Actually update the BibTeX file')
    parser.add_argument('--author', type=str,
                        help='Check specific author only')
    parser.add_argument('--threshold', type=int, default=5,
                        help='Minimum papers for LIT-R (default: 5)')
    parser.add_argument('--bib', type=str, default='bibliography/bcm_master.bib',
                        help='Path to BibTeX file')
    parser.add_argument('--appendices', type=str, default='appendices',
                        help='Path to appendices directory')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Show detailed output')

    args = parser.parse_args()

    # Resolve paths
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    bib_path = repo_root / args.bib
    appendices_dir = repo_root / args.appendices

    print("=" * 70)
    print("Auto-Tag BibTeX → LIT-Appendix")
    print("=" * 70)
    print(f"Threshold: ≥{args.threshold} papers for LIT-R")
    print()

    # Analyze
    entries_by_author, author_counts, existing_lits = analyze_bibliography(
        bib_path, appendices_dir, args.threshold
    )

    # Filter by specific author if requested
    if args.author:
        author = args.author.upper()
        canonical = get_canonical_lit_name(author)
        if canonical and canonical in entries_by_author:
            entries_by_author = {canonical: entries_by_author[canonical]}
            author_counts = {canonical: author_counts[canonical]}
        else:
            print(f"❌ Author '{args.author}' not found")
            return 1

    # Show statistics
    qualifying = [(a, c) for a, c in author_counts.items() if c >= args.threshold]
    print(f"📊 Statistics:")
    print(f"   Total authors: {len(author_counts)}")
    print(f"   Qualifying (≥{args.threshold} papers): {len(qualifying)}")
    print(f"   Existing LIT-Appendices: {len(existing_lits)}")
    print()

    # Update
    tagged, skipped, warnings = update_bibliography(
        bib_path, entries_by_author, author_counts, existing_lits,
        threshold=args.threshold,
        dry_run=not args.update
    )

    # Report
    print("=" * 70)
    print("Results")
    print("=" * 70)
    print(f"   Entries to tag:     {tagged}")
    print(f"   Already tagged:     {skipped}")
    print()

    if warnings:
        print("⚠️  Warnings:")
        for w in warnings[:10]:
            print(f"   {w}")
        if len(warnings) > 10:
            print(f"   ... and {len(warnings) - 10} more")
        print()

    if tagged > 0 and not args.update:
        print("💡 To apply changes, run with --update flag:")
        print(f"   python scripts/auto_tag_bib_lit.py --update")
    elif args.update and tagged > 0:
        print(f"✅ Updated {tagged} entries in {bib_path.name}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
