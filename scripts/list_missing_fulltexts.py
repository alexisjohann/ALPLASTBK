#!/usr/bin/env python3
"""List papers that don't have full text (not L3), prioritized by importance.

Groups papers by integration level and content level to identify
the most valuable papers to obtain full texts for.

Usage:
    python scripts/list_missing_fulltexts.py                # Summary + top priorities
    python scripts/list_missing_fulltexts.py --all           # Complete list
    python scripts/list_missing_fulltexts.py --level I3      # Only I3+ papers
    python scripts/list_missing_fulltexts.py --level I4      # Only I4+ papers
    python scripts/list_missing_fulltexts.py --csv           # CSV output
"""

import os
import re
import glob
import argparse
import yaml
from pathlib import Path


PAPER_REFS_DIR = "data/paper-references"


def extract_field(content, field_name):
    """Extract a field value from YAML content using regex (fast, no full parse)."""
    # Match both top-level and nested field
    pattern = rf"^\s*{field_name}:\s*[\"']?([^\n\"'#]+)"
    match = re.search(pattern, content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return None


def extract_all_fields(filepath):
    """Extract key fields from a paper YAML file."""
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    info = {
        "key": Path(filepath).stem,
        "filepath": filepath,
    }

    # Title
    info["title"] = extract_field(content, "title") or ""

    # Authors
    authors = extract_field(content, "authors?")
    if not authors:
        authors = extract_field(content, "author")
    info["authors"] = authors or ""

    # Year
    info["year"] = extract_field(content, "year") or ""

    # Journal
    info["journal"] = extract_field(content, "journal") or ""

    # Content level - find first occurrence
    info["content_level"] = extract_field(content, "content_level") or "unknown"

    # Integration level
    info["integration_level"] = extract_field(content, "integration_level") or "unknown"

    # DOI
    info["doi"] = extract_field(content, "doi") or ""

    # Has full_text file?
    md_path = f"data/paper-texts/{info['key']}.md"
    info["has_md_file"] = os.path.exists(md_path)

    # Prior score
    prior = extract_field(content, "prior_score")
    if prior:
        try:
            info["prior_score"] = float(prior)
        except ValueError:
            info["prior_score"] = 0.0
    else:
        info["prior_score"] = 0.0

    return info


def main():
    parser = argparse.ArgumentParser(description="List papers missing full text")
    parser.add_argument("--all", action="store_true", help="Show complete list")
    parser.add_argument("--level", type=str, help="Filter by min integration level (I1-I5)")
    parser.add_argument("--csv", action="store_true", help="Output as CSV")
    parser.add_argument("--top", type=int, default=50, help="Number of top papers to show (default 50)")
    args = parser.parse_args()

    # Find all paper YAML files
    yaml_files = sorted(glob.glob(os.path.join(PAPER_REFS_DIR, "PAP-*.yaml")))
    print(f"Scanning {len(yaml_files)} paper YAML files...", flush=True)

    # Extract info for all papers
    papers = []
    for yf in yaml_files:
        info = extract_all_fields(yf)
        papers.append(info)

    # Filter: only papers NOT at L3
    not_l3 = [p for p in papers if p["content_level"] != "L3"]
    l3_papers = [p for p in papers if p["content_level"] == "L3"]

    # Integration level ordering
    il_order = {"I5": 5, "I4": 4, "I3": 3, "I2": 2, "I1": 1, "I0": 0, "unknown": -1}

    # Filter by minimum integration level if specified
    if args.level:
        min_il = il_order.get(args.level, 0)
        not_l3 = [p for p in not_l3 if il_order.get(p["integration_level"], -1) >= min_il]

    # Sort by integration level (desc), then prior_score (desc)
    not_l3.sort(key=lambda p: (-il_order.get(p["integration_level"], -1), -p["prior_score"]))

    if args.csv:
        print("key,title,authors,year,journal,content_level,integration_level,doi,has_md_file,prior_score")
        for p in not_l3:
            title = p["title"].replace('"', '""')
            authors = p["authors"].replace('"', '""')
            journal = p["journal"].replace('"', '""')
            print(f'"{p["key"]}","{title}","{authors}",{p["year"]},"{journal}",{p["content_level"]},{p["integration_level"]},{p["doi"]},{p["has_md_file"]},{p["prior_score"]:.4f}')
        return

    # Summary
    print()
    print("=" * 80)
    print("PAPERS WITHOUT FULL TEXT (not L3)")
    print("=" * 80)
    print()
    print(f"  Total papers in database:    {len(papers):>5}")
    print(f"  With full text (L3):         {len(l3_papers):>5}")
    print(f"  Without full text:           {len(not_l3):>5}")
    print()

    # Breakdown by integration level
    print("-" * 80)
    print("BY INTEGRATION LEVEL (papers without full text)")
    print("-" * 80)
    for il in ["I5", "I4", "I3", "I2", "I1", "I0", "unknown"]:
        count = sum(1 for p in not_l3 if p["integration_level"] == il)
        if count > 0:
            bar = "#" * min(count // 5, 50)
            print(f"  {il:>8}: {count:>5} papers  {bar}")
    print()

    # Breakdown by content level
    print("-" * 80)
    print("BY CONTENT LEVEL (papers without full text)")
    print("-" * 80)
    for cl in ["L2", "L1", "L0", "unknown"]:
        count = sum(1 for p in not_l3 if p["content_level"] == cl)
        if count > 0:
            bar = "#" * min(count // 10, 50)
            print(f"  {cl:>8}: {count:>5} papers  {bar}")
    print()

    # Papers with .md file but not L3 (have some text)
    has_md_not_l3 = [p for p in not_l3 if p["has_md_file"]]
    if has_md_not_l3:
        print("-" * 80)
        print(f"HAVE .md FILE BUT NOT L3: {len(has_md_not_l3)} papers (partial text available)")
        print("-" * 80)
        for p in has_md_not_l3:
            print(f"  {p['content_level']:>3} {p['integration_level']:>3}  {p['key']}")
        print()

    # Top priority: I4+ and I3 papers without full text
    high_priority = [p for p in not_l3 if il_order.get(p["integration_level"], -1) >= 3]
    if high_priority:
        print("=" * 80)
        print(f"HIGH PRIORITY (I3+): {len(high_priority)} papers without full text")
        print("=" * 80)
        for p in high_priority:
            title_short = p["title"][:55] + "..." if len(p["title"]) > 55 else p["title"]
            doi_str = f"  doi:{p['doi']}" if p["doi"] else ""
            print(f"  {p['integration_level']:>3} {p['content_level']:>3}  {p['key']:<50} {title_short}{doi_str}")
        print()

    # Show top N by prior score
    limit = len(not_l3) if args.all else args.top
    print("=" * 80)
    if args.all:
        print(f"ALL {len(not_l3)} PAPERS WITHOUT FULL TEXT (sorted by integration level, prior score)")
    else:
        print(f"TOP {min(limit, len(not_l3))} PAPERS WITHOUT FULL TEXT (sorted by integration level, prior score)")
    print("=" * 80)
    print(f"  {'IL':>3} {'CL':>3} {'Prior':>6}  {'Key':<50} {'Title'}")
    print(f"  {'---':>3} {'---':>3} {'------':>6}  {'-'*50} {'-'*30}")

    for p in not_l3[:limit]:
        title_short = p["title"][:40] + "..." if len(p["title"]) > 40 else p["title"]
        prior_str = f"{p['prior_score']:.3f}" if p["prior_score"] > 0 else "  -  "
        print(f"  {p['integration_level']:>3} {p['content_level']:>3} {prior_str:>6}  {p['key']:<50} {title_short}")

    if not args.all and len(not_l3) > limit:
        print(f"\n  ... and {len(not_l3) - limit} more. Use --all for complete list or --csv for export.")


if __name__ == "__main__":
    main()
