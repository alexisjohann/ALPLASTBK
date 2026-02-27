#!/usr/bin/env python3
"""
sync_bib_to_lit.py - Automatic BibTeX → LIT-Appendix Synchronization

This script synchronizes papers from bcm_master.bib to their corresponding
LIT-Appendices based on the `use_for` field.

Usage:
    python scripts/sync_bib_to_lit.py                    # Report only (dry run)
    python scripts/sync_bib_to_lit.py --update           # Actually update files
    python scripts/sync_bib_to_lit.py --lit LIT-BLINDER  # Sync specific LIT only
    python scripts/sync_bib_to_lit.py --verbose          # Show details

Workflow:
    1. Parse bcm_master.bib
    2. Extract `use_for` fields, filter for LIT-* tags
    3. Group papers by LIT-Appendix
    4. For each LIT-Appendix:
       - Check if paper already exists in appendix
       - If not: generate LaTeX section and insert
    5. Report changes

Author: Claude Code
Version: 1.0 (January 2026)
"""

import re
import os
import sys
import glob
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime

# =============================================================================
# Data Structures
# =============================================================================

@dataclass
class BibEntry:
    """Represents a BibTeX entry with EBF extensions."""
    key: str
    entry_type: str
    title: str
    author: str
    year: str
    journal: Optional[str] = None
    volume: Optional[str] = None
    pages: Optional[str] = None
    publisher: Optional[str] = None
    use_for: List[str] = None
    parameter: Optional[str] = None
    notes: Optional[str] = None
    evidence_tier: Optional[str] = None
    identification: Optional[str] = None
    external_validity: Optional[str] = None

    def __post_init__(self):
        if self.use_for is None:
            self.use_for = []


@dataclass
class LitAppendix:
    """Represents a LIT-Appendix file."""
    code: str
    name: str
    filepath: Path
    existing_keys: List[str]


# =============================================================================
# BibTeX Parser
# =============================================================================

def parse_bibtex(filepath: Path) -> List[BibEntry]:
    """Parse bcm_master.bib and extract entries with use_for fields."""
    entries = []

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Match BibTeX entries
    entry_pattern = r'@(\w+)\{([^,]+),\s*(.*?)\n\}'

    # Split by entries more carefully
    raw_entries = re.split(r'\n(?=@\w+\{)', content)

    for raw in raw_entries:
        if not raw.strip() or raw.strip().startswith('%'):
            continue

        # Match entry type and key
        match = re.match(r'@(\w+)\{([^,]+),', raw)
        if not match:
            continue

        entry_type = match.group(1).lower()
        key = match.group(2).strip()

        # Extract fields
        entry = BibEntry(
            key=key,
            entry_type=entry_type,
            title=extract_field(raw, 'title'),
            author=extract_field(raw, 'author'),
            year=extract_field(raw, 'year'),
            journal=extract_field(raw, 'journal'),
            volume=extract_field(raw, 'volume'),
            pages=extract_field(raw, 'pages'),
            publisher=extract_field(raw, 'publisher'),
            parameter=extract_field(raw, 'parameter'),
            notes=extract_field(raw, 'notes'),
            evidence_tier=extract_field(raw, 'evidence_tier'),
            identification=extract_field(raw, 'identification'),
            external_validity=extract_field(raw, 'external_validity'),
        )

        # Parse use_for field
        use_for_raw = extract_field(raw, 'use_for')
        if use_for_raw:
            # Parse {tag1, tag2, tag3} format
            tags = re.findall(r'[\w-]+', use_for_raw)
            entry.use_for = tags

        entries.append(entry)

    return entries


def extract_field(raw: str, field: str) -> Optional[str]:
    """Extract a field value from a BibTeX entry."""
    # Handle both field = {value} and field = "value" formats
    pattern = rf'{field}\s*=\s*[\{{"](.*?)[\}}"]\s*[,\n]'
    match = re.search(pattern, raw, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()
    return None


# =============================================================================
# LIT-Appendix Discovery
# =============================================================================

def discover_lit_appendices(appendices_dir: Path) -> Dict[str, LitAppendix]:
    """Discover all LIT-Appendix files and their existing paper keys."""
    lit_appendices = {}

    # Find all LIT-* files
    for filepath in appendices_dir.glob('*LIT*.tex'):
        # Extract LIT code from filename or content
        filename = filepath.stem

        # Try to extract LIT name (e.g., LIT-BLINDER, LIT-THALER)
        # Match the FIRST word after LIT- (the primary identifier)
        match = re.search(r'LIT-([A-Z]+)', filename, re.IGNORECASE)
        if not match:
            # Try from file content
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read(2000)
            match = re.search(r'LIT-([A-Z]+)', content, re.IGNORECASE)

        if match:
            # Use only the primary identifier (e.g., BLINDER, not BLINDER_CENTRAL_BANK)
            primary_name = match.group(1).upper()
            lit_name = f"LIT-{primary_name}"

            # Read file to find existing paper keys
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Find existing citations/keys
            existing_keys = re.findall(r'\\cite[tp]?\{([^}]+)\}', content)
            existing_keys += re.findall(r'bibitem\{([^}]+)\}', content)
            # Also find papers mentioned by key pattern (e.g., blinder2008central)
            existing_keys += re.findall(r'\b([a-z]+\d{4}[a-z]*)\b', content.lower())

            # If this LIT already exists (multiple files for same author), merge
            if lit_name in lit_appendices:
                # Keep the one with shorter filename (more canonical)
                if len(filepath.stem) < len(lit_appendices[lit_name].filepath.stem):
                    lit_appendices[lit_name].filepath = filepath
                lit_appendices[lit_name].existing_keys.extend(existing_keys)
                lit_appendices[lit_name].existing_keys = list(set(lit_appendices[lit_name].existing_keys))
            else:
                lit_appendices[lit_name] = LitAppendix(
                    code=primary_name,
                    name=lit_name,
                    filepath=filepath,
                    existing_keys=list(set(existing_keys))
                )

    return lit_appendices


# =============================================================================
# Paper → LIT Mapping
# =============================================================================

def map_papers_to_lit(entries: List[BibEntry]) -> Dict[str, List[BibEntry]]:
    """Group papers by their LIT-* tags from use_for field."""
    mapping = {}

    for entry in entries:
        for tag in entry.use_for:
            if tag.upper().startswith('LIT-'):
                lit_name = tag.upper()
                if lit_name not in mapping:
                    mapping[lit_name] = []
                mapping[lit_name].append(entry)

    return mapping


# =============================================================================
# LaTeX Generation
# =============================================================================

def generate_paper_section(entry: BibEntry) -> str:
    """Generate LaTeX section for a paper entry."""

    # Determine citation format
    if entry.entry_type == 'book':
        citation = f"{entry.author} ({entry.year}). \\textit{{{entry.title}}}. {entry.publisher or 'Publisher'}."
    else:
        journal = entry.journal or "Journal"
        vol_pages = ""
        if entry.volume:
            vol_pages = f", {entry.volume}"
        if entry.pages:
            vol_pages += f", {entry.pages}"
        citation = f"{entry.author} ({entry.year}). ``{entry.title}.'' \\textit{{{journal}}}{vol_pages}."

    # Build section
    lines = [
        f"",
        f"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%",
        f"\\subsubsection{{{entry.year}: {entry.title[:60]}{'...' if len(entry.title) > 60 else ''}}}",
        f"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%",
        f"",
        f"\\paragraph{{Citation.}}",
        f"{citation}",
        f"",
    ]

    # Add notes as Core Finding if available
    if entry.notes:
        # Clean up notes (remove newlines, extra spaces)
        notes_clean = ' '.join(entry.notes.split())
        lines.extend([
            f"\\paragraph{{Core Finding.}}",
            f"{notes_clean[:500]}{'...' if len(notes_clean) > 500 else ''}",
            f"",
        ])

    # Add parameters if available
    if entry.parameter:
        lines.extend([
            f"\\paragraph{{Key Parameters.}}",
            f"\\texttt{{{entry.parameter}}}",
            f"",
        ])

    # Add 10C Integration placeholder
    lines.extend([
        f"\\paragraph{{10C Integration.}}",
        f"\\begin{{itemize}}[nosep]",
        f"  \\item \\textbf{{Domain}}: [To be specified]",
        f"  \\item \\textbf{{use\\_for}}: {', '.join(entry.use_for)}",
        f"\\end{{itemize}}",
        f"",
    ])

    return '\n'.join(lines)


def find_insertion_point(content: str) -> int:
    """Find the best insertion point for new papers in a LIT-Appendix."""

    # Look for "Papers Integrated" section
    match = re.search(r'\\subsection\{Papers Integrated.*?\}', content)
    if match:
        # Find the next section after Papers Integrated
        next_section = re.search(r'\\subsection\{', content[match.end():])
        if next_section:
            return match.end() + next_section.start()
        # Otherwise insert before \section{Summary} or end of file
        summary = re.search(r'\\section\{Summary\}', content)
        if summary:
            return summary.start()

    # Look for "Key Insights" or "Open Research" sections
    for marker in [r'\\subsection\{Key Insights', r'\\subsection\{Open Research', r'\\section\{Summary']:
        match = re.search(marker, content)
        if match:
            return match.start()

    # Default: before \end{document} or end of file
    end_doc = re.search(r'\\end\{document\}', content)
    if end_doc:
        return end_doc.start()

    return len(content)


# =============================================================================
# Synchronization Logic
# =============================================================================

def sync_lit_appendix(
    lit: LitAppendix,
    papers: List[BibEntry],
    dry_run: bool = True,
    verbose: bool = False
) -> Tuple[int, List[str]]:
    """Synchronize papers to a LIT-Appendix."""

    added = []
    skipped = []

    # Read current content
    with open(lit.filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_sections = []

    for paper in papers:
        # Check if paper already exists
        key_lower = paper.key.lower()
        if key_lower in [k.lower() for k in lit.existing_keys]:
            skipped.append(paper.key)
            if verbose:
                print(f"  ⏭️  {paper.key} - already in {lit.name}")
            continue

        # Also check if title is mentioned
        title_words = paper.title.lower().split()[:3]
        title_check = ' '.join(title_words)
        if title_check in content.lower():
            skipped.append(paper.key)
            if verbose:
                print(f"  ⏭️  {paper.key} - title found in {lit.name}")
            continue

        # Generate section for new paper
        section = generate_paper_section(paper)
        new_sections.append(section)
        added.append(paper.key)

        if verbose:
            print(f"  ✅ {paper.key} - will be added to {lit.name}")

    # If we have new sections and not dry run, update file
    if new_sections and not dry_run:
        insertion_point = find_insertion_point(content)

        # Build insertion block
        header = f"\n% === AUTO-GENERATED ENTRIES ({datetime.now().strftime('%Y-%m-%d')}) ===\n"
        footer = f"\n% === END AUTO-GENERATED ENTRIES ===\n"

        new_content = (
            content[:insertion_point] +
            header +
            '\n'.join(new_sections) +
            footer +
            content[insertion_point:]
        )

        with open(lit.filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

    return len(added), added


# =============================================================================
# Main Entry Point
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Sync BibTeX entries to LIT-Appendices',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python scripts/sync_bib_to_lit.py                    # Report only
    python scripts/sync_bib_to_lit.py --update           # Update files
    python scripts/sync_bib_to_lit.py --lit LIT-BLINDER  # Specific LIT
    python scripts/sync_bib_to_lit.py --verbose          # Detailed output
        """
    )
    parser.add_argument('--update', action='store_true',
                        help='Actually update the LIT-Appendix files')
    parser.add_argument('--lit', type=str,
                        help='Sync only specific LIT-Appendix (e.g., LIT-BLINDER)')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Show detailed output')
    parser.add_argument('--bib', type=str, default='bibliography/bcm_master.bib',
                        help='Path to BibTeX file')
    parser.add_argument('--appendices', type=str, default='appendices',
                        help='Path to appendices directory')

    args = parser.parse_args()

    # Resolve paths
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    bib_path = repo_root / args.bib
    appendices_dir = repo_root / args.appendices

    print("=" * 70)
    print("BibTeX → LIT-Appendix Synchronization")
    print("=" * 70)
    print()

    # Parse BibTeX
    print(f"📚 Parsing {bib_path.name}...")
    entries = parse_bibtex(bib_path)
    print(f"   Found {len(entries)} total entries")

    # Map papers to LIT
    lit_mapping = map_papers_to_lit(entries)
    lit_papers_count = sum(len(papers) for papers in lit_mapping.values())
    print(f"   Found {lit_papers_count} papers with LIT-* tags")
    print()

    # Discover LIT-Appendices
    print(f"📁 Discovering LIT-Appendices in {appendices_dir.name}/...")
    lit_appendices = discover_lit_appendices(appendices_dir)
    print(f"   Found {len(lit_appendices)} LIT-Appendix files")
    print()

    # Filter if specific LIT requested
    if args.lit:
        lit_name = args.lit.upper()
        if not lit_name.startswith('LIT-'):
            lit_name = f'LIT-{lit_name}'
        if lit_name not in lit_appendices:
            print(f"❌ LIT-Appendix '{lit_name}' not found!")
            print(f"   Available: {', '.join(sorted(lit_appendices.keys()))}")
            sys.exit(1)
        lit_appendices = {lit_name: lit_appendices[lit_name]}
        lit_mapping = {k: v for k, v in lit_mapping.items() if k == lit_name}

    # Sync each LIT-Appendix
    print("🔄 Synchronization Report:")
    print("-" * 70)

    total_added = 0
    total_skipped = 0
    changes = []

    for lit_name in sorted(set(lit_mapping.keys()) | set(lit_appendices.keys())):
        papers = lit_mapping.get(lit_name, [])
        lit = lit_appendices.get(lit_name)

        if not lit:
            print(f"\n⚠️  {lit_name}: No appendix file found!")
            print(f"   Papers waiting: {len(papers)}")
            for p in papers[:5]:
                print(f"      - {p.key}")
            if len(papers) > 5:
                print(f"      ... and {len(papers) - 5} more")
            continue

        if not papers:
            if args.verbose:
                print(f"\n📄 {lit_name}: No new papers tagged")
            continue

        print(f"\n📄 {lit_name} ({lit.filepath.name})")
        print(f"   Papers tagged: {len(papers)}")
        print(f"   Existing keys: {len(lit.existing_keys)}")

        added_count, added_keys = sync_lit_appendix(
            lit, papers,
            dry_run=not args.update,
            verbose=args.verbose
        )

        total_added += added_count
        total_skipped += len(papers) - added_count

        if added_count > 0:
            changes.append((lit_name, added_keys))
            status = "WILL ADD" if not args.update else "ADDED"
            print(f"   {status}: {added_count} papers")
        else:
            print(f"   Already synced ✓")

    # Summary
    print()
    print("=" * 70)
    print("Summary")
    print("=" * 70)
    print(f"   Total papers with LIT tags: {lit_papers_count}")
    print(f"   Papers to add:              {total_added}")
    print(f"   Papers already synced:      {total_skipped}")
    print()

    if total_added > 0 and not args.update:
        print("💡 To apply changes, run with --update flag:")
        print(f"   python scripts/sync_bib_to_lit.py --update")
        print()

    if args.update and changes:
        print("✅ Files updated:")
        for lit_name, keys in changes:
            print(f"   {lit_name}: +{len(keys)} papers")
        print()
        print("📝 Don't forget to review and commit the changes!")

    return 0 if total_added == 0 or args.update else 1


if __name__ == '__main__':
    sys.exit(main())
