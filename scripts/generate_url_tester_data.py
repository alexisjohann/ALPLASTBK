#!/usr/bin/env python3
"""
Generate inline JavaScript data for the researcher URL tester HTML tool.

Reads paper-upload-priority-top100.json, deduplicates researcher URLs,
and outputs a `const URL_DATA = [...]` JavaScript block.

Usage:
  python scripts/generate_url_tester_data.py              # JS block to stdout
  python scripts/generate_url_tester_data.py --json       # Raw JSON to stdout
  python scripts/generate_url_tester_data.py --stats      # Summary stats
"""

import argparse
import json
import sys
from collections import defaultdict


def extract_urls(papers: list) -> list[dict]:
    """Extract and deduplicate researcher URLs from papers."""
    seen_urls: set[str] = set()
    entries: list[dict] = []
    url_papers: dict[str, list[str]] = defaultdict(list)

    for p in papers:
        r = p.get("researcher")
        if not r:
            continue

        name = r["name"]
        dept = r.get("department")
        pers = r.get("personal")
        bkey = p["bibtex_key"]

        if dept and dept["url"] not in seen_urls:
            seen_urls.add(dept["url"])
            entries.append({
                "researcher": name,
                "institution": dept.get("institution", ""),
                "type": "DEPT",
                "sitePattern": dept.get("site_pattern", ""),
                "url": dept["url"],
                "searchHint": dept.get("search_hint", ""),
                "papers": [],
            })
        if dept:
            url_papers[dept["url"]].append(bkey)

        if pers and pers["url"] not in seen_urls:
            seen_urls.add(pers["url"])
            entries.append({
                "researcher": name,
                "institution": "",
                "type": "PERSONAL",
                "sitePattern": pers.get("site_pattern", ""),
                "url": pers["url"],
                "searchHint": pers.get("search_hint", ""),
                "papers": [],
            })
        if pers:
            url_papers[pers["url"]].append(bkey)

    # Assign papers and IDs
    for i, entry in enumerate(entries, 1):
        entry["id"] = i
        entry["papers"] = url_papers.get(entry["url"], [])
        entry["paperCount"] = len(entry["papers"])

    return entries


def main():
    parser = argparse.ArgumentParser(description="Generate URL tester data")
    parser.add_argument("--input", default="data/paper-upload-priority-top100.json")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    parser.add_argument("--stats", action="store_true", help="Show summary stats")
    args = parser.parse_args()

    with open(args.input) as f:
        data = json.load(f)

    entries = extract_urls(data["papers"])

    if args.stats:
        dept = [e for e in entries if e["type"] == "DEPT"]
        pers = [e for e in entries if e["type"] == "PERSONAL"]
        total_papers = sum(e["paperCount"] for e in entries)
        print(f"Total unique URLs:  {len(entries)}")
        print(f"  Department:       {len(dept)}")
        print(f"  Personal:         {len(pers)}")
        print(f"Papers covered:     {total_papers}")
        print(f"Unique institutions: {len(set(e['institution'] for e in dept if e['institution']))}")
        return

    if args.json:
        json.dump(entries, sys.stdout, indent=2, ensure_ascii=False)
        print()
        return

    # Output as JavaScript const
    print("const URL_DATA = " + json.dumps(entries, indent=2, ensure_ascii=False) + ";")


if __name__ == "__main__":
    main()
