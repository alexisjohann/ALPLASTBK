#!/usr/bin/env python3
"""
EBF Bibliography Search Tool

Searches the bcm_master.bib and other bibliography files for relevant papers.
Supports keyword search, author search, and tag search.

Usage:
    python scripts/search_bibliography.py "mental accounting"
    python scripts/search_bibliography.py --author "Thaler"
    python scripts/search_bibliography.py --tag "CORE-WHERE"
    python scripts/search_bibliography.py --year 2020-2025
    python scripts/search_bibliography.py --parameter "lambda"
    python scripts/search_bibliography.py --all "loss aversion"  # Search everywhere

Reference: docs/workflows/evidence-integration-pipeline.md (Stufe 2: Literaturrecherche)
"""

import sys
import re
import argparse
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass


@dataclass
class BibEntry:
    """A single bibliography entry."""
    key: str
    entry_type: str
    title: str
    author: str
    year: str
    journal: Optional[str]
    evidence_tier: Optional[str]
    use_for: Optional[str]
    parameter: Optional[str]
    raw: str


def parse_bib_file(filepath: Path) -> List[BibEntry]:
    """Parse a .bib file and extract entries."""
    entries = []

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        print(f"Warning: Could not read {filepath}: {e}", file=sys.stderr)
        return entries

    # Split by @ entries
    pattern = r'@(\w+)\{([^,]+),([^@]*)'
    matches = re.findall(pattern, content, re.DOTALL)

    for entry_type, key, body in matches:
        # Extract fields
        title = extract_field(body, 'title') or ""
        author = extract_field(body, 'author') or ""
        year = extract_field(body, 'year') or ""
        journal = extract_field(body, 'journal')
        evidence_tier = extract_field(body, 'evidence_tier')
        use_for = extract_field(body, 'use_for')
        parameter = extract_field(body, 'parameter')

        entries.append(BibEntry(
            key=key.strip(),
            entry_type=entry_type.lower(),
            title=title,
            author=author,
            year=year,
            journal=journal,
            evidence_tier=evidence_tier,
            use_for=use_for,
            parameter=parameter,
            raw=body
        ))

    return entries


def extract_field(body: str, field: str) -> Optional[str]:
    """Extract a field value from bib entry body."""
    # Match field = {value} or field = "value" or field = value
    patterns = [
        rf'{field}\s*=\s*\{{([^}}]*)\}}',
        rf'{field}\s*=\s*"([^"]*)"',
        rf'{field}\s*=\s*(\d+)'
    ]

    for pattern in patterns:
        match = re.search(pattern, body, re.IGNORECASE)
        if match:
            return match.group(1).strip()

    return None


def search_entries(entries: List[BibEntry],
                   keyword: Optional[str] = None,
                   author: Optional[str] = None,
                   year_range: Optional[Tuple[int, int]] = None,
                   tag: Optional[str] = None,
                   parameter: Optional[str] = None,
                   search_all: bool = False) -> List[BibEntry]:
    """Search entries based on criteria."""
    results = []

    for entry in entries:
        matches = True

        # Keyword search (title, or all fields if search_all)
        if keyword:
            keyword_lower = keyword.lower()
            if search_all:
                searchable = f"{entry.title} {entry.author} {entry.journal or ''} {entry.raw}".lower()
            else:
                searchable = entry.title.lower()

            if keyword_lower not in searchable:
                matches = False

        # Author search
        if author and matches:
            if author.lower() not in entry.author.lower():
                matches = False

        # Year range search
        if year_range and matches:
            try:
                entry_year = int(entry.year)
                if not (year_range[0] <= entry_year <= year_range[1]):
                    matches = False
            except ValueError:
                matches = False

        # Tag search (use_for field)
        if tag and matches:
            if not entry.use_for or tag.lower() not in entry.use_for.lower():
                matches = False

        # Parameter search
        if parameter and matches:
            if not entry.parameter or parameter.lower() not in entry.parameter.lower():
                matches = False

        if matches:
            results.append(entry)

    return results


def format_entry(entry: BibEntry, verbose: bool = False) -> str:
    """Format an entry for display."""
    lines = []

    # Citation key and basic info
    tier_badge = f"[Tier {entry.evidence_tier}]" if entry.evidence_tier else ""
    lines.append(f"\033[1m{entry.key}\033[0m {tier_badge}")
    lines.append(f"  {entry.author} ({entry.year})")
    lines.append(f"  \033[3m{entry.title}\033[0m")

    if entry.journal:
        lines.append(f"  {entry.journal}")

    if verbose:
        if entry.use_for:
            lines.append(f"  \033[94mTags:\033[0m {entry.use_for}")
        if entry.parameter:
            lines.append(f"  \033[92mParams:\033[0m {entry.parameter}")

    return "\n".join(lines)


def format_for_eip(entries: List[BibEntry]) -> str:
    """Format entries for EIP documentation."""
    lines = ["```yaml", "pro_evidence:"]

    for entry in entries:
        lines.append(f"  - paper: \"{entry.key}\"")
        lines.append(f"    finding: \"[TODO: Summarize finding]\"")
        lines.append(f"    relevance: \"[TODO: Explain relevance]\"")
        strength = "high" if entry.evidence_tier == "1" else "medium" if entry.evidence_tier == "2" else "low"
        lines.append(f"    strength: \"{strength}\"")
        lines.append("")

    lines.append("```")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="EBF Bibliography Search Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    %(prog)s "mental accounting"           # Search titles
    %(prog)s --all "loss aversion"         # Search everywhere
    %(prog)s --author "Thaler"             # Find by author
    %(prog)s --tag "CORE-WHERE"            # Find by EBF tag
    %(prog)s --parameter "lambda"          # Find papers with parameter
    %(prog)s --year 2015-2025              # Filter by year range
    %(prog)s --eip "framing"               # Format for EIP documentation
        """
    )

    parser.add_argument(
        "query",
        nargs="?",
        help="Keyword to search in titles"
    )
    parser.add_argument(
        "--all", "-a",
        dest="search_all",
        metavar="QUERY",
        help="Search all fields (title, author, abstract, etc.)"
    )
    parser.add_argument(
        "--author",
        help="Filter by author name"
    )
    parser.add_argument(
        "--year",
        help="Filter by year range (e.g., 2015-2025 or 2020)"
    )
    parser.add_argument(
        "--tag",
        help="Filter by EBF tag (use_for field)"
    )
    parser.add_argument(
        "--parameter", "-p",
        help="Filter by parameter name"
    )
    parser.add_argument(
        "--eip",
        metavar="QUERY",
        help="Search and format output for EIP documentation"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed entry information"
    )
    parser.add_argument(
        "--limit", "-n",
        type=int,
        default=20,
        help="Maximum number of results (default: 20)"
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show bibliography statistics"
    )

    args = parser.parse_args()

    # Find bibliography files
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    bib_dir = project_root / "bibliography"

    bib_files = list(bib_dir.glob("*.bib"))

    if not bib_files:
        print("Error: No .bib files found in bibliography/", file=sys.stderr)
        return 1

    # Parse all bibliography files
    all_entries = []
    for bib_file in bib_files:
        entries = parse_bib_file(bib_file)
        all_entries.extend(entries)

    print(f"\n\033[1mEBF Bibliography Search\033[0m")
    print(f"Loaded {len(all_entries)} entries from {len(bib_files)} files")
    print("=" * 60)

    # Show stats if requested
    if args.stats:
        show_stats(all_entries)
        return 0

    # Determine search query
    keyword = args.query
    search_all = False

    if args.search_all:
        keyword = args.search_all
        search_all = True

    if args.eip:
        keyword = args.eip
        search_all = True

    # Parse year range
    year_range = None
    if args.year:
        if "-" in args.year:
            start, end = args.year.split("-")
            year_range = (int(start), int(end))
        else:
            year_range = (int(args.year), int(args.year))

    # Search
    results = search_entries(
        all_entries,
        keyword=keyword,
        author=args.author,
        year_range=year_range,
        tag=args.tag,
        parameter=args.parameter,
        search_all=search_all
    )

    # Sort by year (newest first)
    results.sort(key=lambda e: e.year if e.year else "0", reverse=True)

    # Limit results
    total_results = len(results)
    results = results[:args.limit]

    if not results:
        print("\nNo matching entries found.")
        print("\nSearch tips:")
        print("  - Use --all to search all fields, not just titles")
        print("  - Try broader keywords")
        print("  - Use --author for author-specific search")
        return 0

    print(f"\nFound {total_results} entries (showing {len(results)}):\n")

    # Format output
    if args.eip:
        print("\n\033[1mEIP Documentation Format:\033[0m\n")
        print(format_for_eip(results))
        print("\n\033[1mDetailed Entries:\033[0m\n")

    for entry in results:
        print(format_entry(entry, args.verbose))
        print()

    if total_results > args.limit:
        print(f"... and {total_results - args.limit} more. Use --limit to show more.")

    return 0


def show_stats(entries: List[BibEntry]):
    """Show bibliography statistics."""
    print("\n\033[1mBibliography Statistics:\033[0m\n")

    # Count by type
    types = {}
    for e in entries:
        types[e.entry_type] = types.get(e.entry_type, 0) + 1

    print("Entry types:")
    for t, count in sorted(types.items(), key=lambda x: -x[1]):
        print(f"  {t}: {count}")

    # Count by evidence tier
    tiers = {"1": 0, "2": 0, "3": 0, None: 0}
    for e in entries:
        tier = e.evidence_tier if e.evidence_tier in tiers else None
        tiers[tier] = tiers.get(tier, 0) + 1

    print("\nEvidence tiers:")
    for tier, count in sorted(tiers.items(), key=lambda x: str(x[0])):
        label = f"Tier {tier}" if tier else "Unclassified"
        print(f"  {label}: {count}")

    # Count entries with parameters
    with_params = sum(1 for e in entries if e.parameter)
    print(f"\nEntries with parameters: {with_params}")

    # Year distribution
    years = {}
    for e in entries:
        try:
            decade = (int(e.year) // 10) * 10
            years[decade] = years.get(decade, 0) + 1
        except:
            pass

    print("\nEntries by decade:")
    for decade, count in sorted(years.items()):
        print(f"  {decade}s: {count}")

    # Top authors
    authors = {}
    for e in entries:
        for author in re.split(r'\s+and\s+', e.author):
            # Extract last name
            parts = author.strip().split(',')
            if parts:
                name = parts[0].strip()
                if name:
                    authors[name] = authors.get(name, 0) + 1

    print("\nTop authors:")
    for author, count in sorted(authors.items(), key=lambda x: -x[1])[:15]:
        print(f"  {author}: {count}")


if __name__ == "__main__":
    sys.exit(main())
