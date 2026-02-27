#!/usr/bin/env python3
"""
Test researcher homepage URLs from the priority list.

Checks if department/personal pages are reachable and contain PDF links.
Run locally or via GitHub Actions (not from Claude Code sandbox).

Usage:
  python scripts/test_researcher_urls.py                  # Test all
  python scripts/test_researcher_urls.py --sample 10      # Random 10
  python scripts/test_researcher_urls.py --researcher fehr # Specific
"""

import argparse
import json
import random
import re
import sys
import urllib.request
import urllib.error
from collections import defaultdict


def fetch_url(url: str, timeout: int = 15) -> tuple[int, str]:
    """Fetch URL and return (status_code, body_text)."""
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (research-bot; fehradvice.com)"},
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return resp.status, body
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:
        return 0, str(e)


def check_page(url: str) -> dict:
    """Check a URL for publication list and PDF links."""
    status, body = fetch_url(url)
    body_lower = body.lower()

    has_pdfs = bool(re.findall(r'href="[^"]*\.pdf"', body_lower))
    pdf_count = len(re.findall(r'\.pdf', body_lower))
    has_pub_list = any(
        kw in body_lower
        for kw in [
            "publications",
            "research papers",
            "working papers",
            "selected papers",
            "journal articles",
            "published papers",
            "peer-reviewed",
        ]
    )

    return {
        "url": url,
        "status": status,
        "ok": 200 <= status < 400,
        "has_pub_list": has_pub_list,
        "has_pdf_links": has_pdfs,
        "pdf_mentions": pdf_count,
        "page_size_kb": round(len(body) / 1024, 1),
    }


def main():
    parser = argparse.ArgumentParser(description="Test researcher homepage URLs")
    parser.add_argument("--sample", type=int, help="Test random N papers")
    parser.add_argument("--researcher", type=str, help="Test specific researcher slug")
    parser.add_argument(
        "--input",
        type=str,
        default="data/paper-upload-priority-top100.json",
        help="Input JSON file",
    )
    args = parser.parse_args()

    with open(args.input) as f:
        data = json.load(f)

    papers = [p for p in data["papers"] if p.get("researcher")]

    if args.researcher:
        papers = [
            p
            for p in papers
            if args.researcher.lower() in p["researcher"]["name"].lower()
            or args.researcher.lower() in p["bibtex_key"].lower()
        ]

    if args.sample:
        random.seed(42)
        papers = random.sample(papers, min(args.sample, len(papers)))

    # Deduplicate URLs (same researcher appears multiple times)
    seen_urls = set()
    urls_to_test = []
    for p in papers:
        r = p["researcher"]
        dept = r.get("department")
        pers = r.get("personal")
        if dept and dept["url"] not in seen_urls:
            seen_urls.add(dept["url"])
            urls_to_test.append(
                {
                    "researcher": r["name"],
                    "tier": "DEPT",
                    "institution": dept.get("institution", ""),
                    "url": dept["url"],
                    "site_pattern": dept.get("site_pattern", ""),
                }
            )
        if pers and pers["url"] not in seen_urls:
            seen_urls.add(pers["url"])
            urls_to_test.append(
                {
                    "researcher": r["name"],
                    "tier": "PERSONAL",
                    "institution": "",
                    "url": pers["url"],
                    "site_pattern": pers.get("site_pattern", ""),
                }
            )

    print(f"Testing {len(urls_to_test)} unique URLs from {len(papers)} papers...")
    print("=" * 90)

    results = []
    ok_count = 0
    pdf_count = 0

    for entry in urls_to_test:
        result = check_page(entry["url"])
        result["researcher"] = entry["researcher"]
        result["tier"] = entry["tier"]
        result["institution"] = entry["institution"]
        results.append(result)

        status_icon = "OK" if result["ok"] else f"FAIL({result['status']})"
        pub_icon = "PUB" if result["has_pub_list"] else "   "
        pdf_icon = f"PDF({result['pdf_mentions']})" if result["has_pdf_links"] else "no-pdf"
        size = f"{result['page_size_kb']}kb"

        print(
            f"  [{entry['tier']:8}] {status_icon:>10}  {pub_icon}  {pdf_icon:>8}  "
            f"{size:>8}  {entry['researcher'][:20]:<20}  {entry['url'][:50]}"
        )

        if result["ok"]:
            ok_count += 1
        if result["has_pdf_links"]:
            pdf_count += 1

    print("=" * 90)
    print(f"\nSUMMARY:")
    print(f"  Tested:    {len(results)} URLs")
    print(f"  Reachable: {ok_count}/{len(results)} ({100*ok_count//max(len(results),1)}%)")
    print(f"  Has PDFs:  {pdf_count}/{len(results)} ({100*pdf_count//max(len(results),1)}%)")

    # Group by tier
    for tier in ["DEPT", "PERSONAL"]:
        tier_results = [r for r in results if r["tier"] == tier]
        if tier_results:
            tier_ok = sum(1 for r in tier_results if r["ok"])
            tier_pdf = sum(1 for r in tier_results if r["has_pdf_links"])
            print(f"  {tier:8}: {tier_ok}/{len(tier_results)} reachable, {tier_pdf}/{len(tier_results)} with PDFs")

    # Failures
    failures = [r for r in results if not r["ok"]]
    if failures:
        print(f"\nFAILED ({len(failures)}):")
        for r in failures:
            print(f"  {r['status']:>3}  {r['researcher']:<25}  {r['url'][:60]}")

    return 0 if ok_count == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
