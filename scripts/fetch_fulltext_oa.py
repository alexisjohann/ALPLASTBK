#!/usr/bin/env python3
"""
Full-Text Fetch for Open Access Papers (L2 → L3 Upgrade)
=========================================================

Fetches full-text content for papers with DOIs using:
1. Unpaywall API → finds Open Access PDF/HTML URLs
2. PDF extraction via pdftotext (poppler-utils)
3. HTML extraction via direct fetch + cleanup

Stores results in:
- data/paper-texts/PAP-{key}.md     (full text as markdown)
- data/paper-references/PAP-{key}.yaml  (updated content_level)

Usage:
    python scripts/fetch_fulltext_oa.py --batch 5 --dry-run
    python scripts/fetch_fulltext_oa.py --batch 50
    python scripts/fetch_fulltext_oa.py --author sutter --batch 10
    python scripts/fetch_fulltext_oa.py --key sutter2007bargaining

Requirements (GitHub Actions runner):
    pip install requests pyyaml
    apt-get install poppler-utils  # for pdftotext
"""

import argparse
import glob
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path

import requests
import yaml

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
PAPERS_DIR = Path("data/paper-references")
TEXTS_DIR = Path("data/paper-texts")
UNPAYWALL_EMAIL = "research@fehradvice.com"  # Required by Unpaywall API
USER_AGENT = "EBF-Framework/1.0 (mailto:research@fehradvice.com)"

# L3 Requirements
MIN_WORDS_ARTICLE = 10000
MIN_WORDS_SHORT = 5000

# Rate limiting
REQUEST_DELAY = 1.0  # seconds between API calls

# Stats
stats = {
    "processed": 0,
    "oa_found": 0,
    "pdf_fetched": 0,
    "html_fetched": 0,
    "l3_upgraded": 0,
    "l2_partial": 0,
    "skipped_no_oa": 0,
    "skipped_no_doi": 0,
    "errors": 0,
}

# Per-paper result tracking for detailed log
paper_results = []


# ---------------------------------------------------------------------------
# Unpaywall API
# ---------------------------------------------------------------------------
def check_unpaywall(doi: str) -> dict | None:
    """Check Unpaywall for Open Access availability."""
    url = f"https://api.unpaywall.org/v2/{doi}?email={UNPAYWALL_EMAIL}"
    try:
        resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=15)
        if resp.status_code == 200:
            return resp.json()
        elif resp.status_code == 404:
            return None
        else:
            print(f"    Unpaywall HTTP {resp.status_code}")
            return None
    except Exception as e:
        print(f"    Unpaywall error: {e}")
        return None


def get_all_oa_urls(unpaywall_data: dict) -> list[tuple[str, str, str]]:
    """Extract ALL Open Access URLs from Unpaywall response, ranked by accessibility.

    Returns list of (url, type, host_type) tuples.
    Priority: repository PDF > repository HTML > publisher PDF > publisher HTML.
    Repositories are more permissive for automated downloads than publishers.
    """
    if not unpaywall_data or not unpaywall_data.get("is_oa"):
        return []

    urls = []  # (url, type, host_type, priority)
    seen = set()

    for loc in unpaywall_data.get("oa_locations", []):
        host_type = loc.get("host_type", "unknown")
        # Repositories get priority 0, publishers get priority 1
        host_priority = 0 if host_type == "repository" else 1

        pdf_url = loc.get("url_for_pdf")
        if pdf_url and pdf_url not in seen:
            seen.add(pdf_url)
            urls.append((pdf_url, "pdf", host_type, host_priority))

        page_url = loc.get("url_for_landing_page") or loc.get("url")
        if page_url and page_url not in seen:
            seen.add(page_url)
            urls.append((page_url, "html", host_type, host_priority + 0.5))

    # Sort by priority: repo PDF (0) > repo HTML (0.5) > pub PDF (1) > pub HTML (1.5)
    urls.sort(key=lambda x: x[3])

    return [(u, t, h) for u, t, h, _ in urls]


def get_best_oa_url(unpaywall_data: dict) -> tuple[str | None, str]:
    """Extract best Open Access URL (backward-compatible wrapper).

    Returns (url, type) where type is 'pdf' or 'html'.
    """
    urls = get_all_oa_urls(unpaywall_data)
    if urls:
        return urls[0][0], urls[0][1]
    return None, ""


# ---------------------------------------------------------------------------
# PDF Download & Extraction
# ---------------------------------------------------------------------------
def url_looks_like_pdf(url: str) -> bool:
    """Check if a URL looks like it points to a PDF file."""
    url_lower = url.lower().split("?")[0]  # Remove query params
    return url_lower.endswith(".pdf") or "/pdf/" in url_lower or "pdfdirect" in url_lower


def download_pdf(url: str, output_path: str) -> tuple[bool, str]:
    """Download a PDF file. Returns (success, detail_msg)."""
    try:
        resp = requests.get(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "application/pdf,*/*",
            },
            timeout=60,
            stream=True,
            allow_redirects=True,
        )
        content_type = resp.headers.get("content-type", "unknown")
        if resp.status_code == 200 and len(resp.content) > 1000:
            # Verify it's actually a PDF
            if resp.content[:5] == b"%PDF-" or b"%PDF-" in resp.content[:100]:
                with open(output_path, "wb") as f:
                    f.write(resp.content)
                return True, f"OK ({len(resp.content)} bytes)"
            else:
                msg = f"Not a PDF (content-type={content_type}, first_bytes={resp.content[:20]})"
                print(f"    {msg}")
                return False, msg
        else:
            msg = f"HTTP {resp.status_code}, size={len(resp.content)}, type={content_type}"
            print(f"    Download failed: {msg}")
            return False, msg
    except Exception as e:
        msg = f"Exception: {e}"
        print(f"    Download error: {msg}")
        return False, msg


def extract_text_from_pdf(pdf_path: str) -> str | None:
    """Extract text from PDF using pdftotext."""
    try:
        result = subprocess.run(
            ["pdftotext", "-layout", "-enc", "UTF-8", pdf_path, "-"],
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
        else:
            print(f"    pdftotext failed: {result.stderr[:200]}")
            return None
    except FileNotFoundError:
        print("    ERROR: pdftotext not found. Install poppler-utils.")
        return None
    except Exception as e:
        print(f"    pdftotext error: {e}")
        return None


# ---------------------------------------------------------------------------
# HTML Fetch & Extraction
# ---------------------------------------------------------------------------
def fetch_html_text(url: str) -> str | None:
    """Fetch HTML page and extract text content."""
    try:
        resp = requests.get(
            url,
            headers={"User-Agent": USER_AGENT},
            timeout=30,
            allow_redirects=True,
        )
        if resp.status_code != 200:
            return None

        html = resp.text

        # Simple HTML-to-text: remove tags, decode entities
        text = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.I)
        text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL | re.I)
        text = re.sub(r"<nav[^>]*>.*?</nav>", "", text, flags=re.DOTALL | re.I)
        text = re.sub(r"<header[^>]*>.*?</header>", "", text, flags=re.DOTALL | re.I)
        text = re.sub(r"<footer[^>]*>.*?</footer>", "", text, flags=re.DOTALL | re.I)
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"&nbsp;", " ", text)
        text = re.sub(r"&amp;", "&", text)
        text = re.sub(r"&lt;", "<", text)
        text = re.sub(r"&gt;", ">", text)
        text = re.sub(r"&#\d+;", " ", text)
        text = re.sub(r"\s+", " ", text)

        return text.strip() if len(text.strip()) > 500 else None
    except Exception as e:
        print(f"    HTML fetch error: {e}")
        return None


# ---------------------------------------------------------------------------
# Text Cleanup & Validation
# ---------------------------------------------------------------------------
def cleanup_text(text: str) -> str:
    """Clean up extracted text for markdown storage."""
    # Remove excessive whitespace but preserve paragraph breaks
    lines = text.split("\n")
    cleaned = []
    prev_empty = False

    for line in lines:
        line = line.rstrip()
        if not line:
            if not prev_empty:
                cleaned.append("")
                prev_empty = True
        else:
            cleaned.append(line)
            prev_empty = False

    return "\n".join(cleaned).strip()


def count_words(text: str) -> int:
    """Count words in text."""
    return len(text.split())


def has_references_section(text: str) -> bool:
    """Check if text contains a references section."""
    patterns = [
        r"\bReferences\b",
        r"\bBibliography\b",
        r"\bLiterature\b",
        r"\bWorks Cited\b",
        r"\bREFERENCES\b",
    ]
    return any(re.search(p, text) for p in patterns)


def validate_l3(text: str) -> tuple[bool, str, dict]:
    """Validate if text meets L3 requirements (R1-R4).

    Returns (is_l3, reason, details).
    """
    word_count = count_words(text)
    has_refs = has_references_section(text)

    details = {
        "word_count": word_count,
        "has_references": has_refs,
        "r1_sections": word_count > 2000,  # Proxy: if >2k words, likely has sections
        "r3_length": word_count >= MIN_WORDS_SHORT,
    }

    if word_count >= MIN_WORDS_SHORT and has_refs:
        return True, "L3", details
    elif word_count >= 2000:
        return False, f"L2+ ({word_count} words, refs={'yes' if has_refs else 'no'})", details
    else:
        return False, f"Too short ({word_count} words)", details


# ---------------------------------------------------------------------------
# Paper Processing
# ---------------------------------------------------------------------------
def load_paper_yaml(key: str) -> dict | None:
    """Load paper YAML file."""
    path = PAPERS_DIR / f"PAP-{key}.yaml"
    if not path.exists():
        return None
    with open(path) as f:
        return yaml.safe_load(f)


def save_paper_yaml(key: str, data: dict):
    """Save paper YAML file."""
    path = PAPERS_DIR / f"PAP-{key}.yaml"
    with open(path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, width=120)


def save_fulltext(key: str, text: str, metadata: dict):
    """Save full text as markdown."""
    TEXTS_DIR.mkdir(parents=True, exist_ok=True)
    path = TEXTS_DIR / f"PAP-{key}.md"

    # Header with metadata
    header = f"""---
paper_id: PAP-{key}
doi: {metadata.get('doi', 'unknown')}
source: {metadata.get('source', 'unknown')}
fetch_date: {datetime.now().strftime('%Y-%m-%d')}
word_count: {count_words(text)}
has_references: {has_references_section(text)}
---

"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(header + text)

    return path


def process_paper(key: str, data: dict, dry_run: bool = False) -> str:
    """Process a single paper: fetch full text, validate, store.

    Returns status string.
    """
    doi = (data.get("doi") or "").strip()
    if not doi:
        stats["skipped_no_doi"] += 1
        return "SKIP (no DOI)"

    print(f"  DOI: {doi}")

    # Step 1: Check Unpaywall
    time.sleep(REQUEST_DELAY)
    unpaywall = check_unpaywall(doi)

    if not unpaywall or not unpaywall.get("is_oa"):
        stats["skipped_no_oa"] += 1
        oa_status = "closed" if unpaywall else "not_found"
        return f"SKIP (not Open Access: {oa_status})"

    # Step 2: Get ALL OA URLs, ranked by accessibility (repos first)
    all_urls = get_all_oa_urls(unpaywall)
    if not all_urls:
        stats["skipped_no_oa"] += 1
        return "SKIP (no usable OA URL)"

    oa_url, oa_type = all_urls[0][0], all_urls[0][1]
    print(f"  OA URLs: {len(all_urls)} available (best: {oa_type} from {all_urls[0][2]})")
    stats["oa_found"] += 1

    if dry_run:
        hosts = [f"{t}@{h}" for _, t, h in all_urls]
        return f"DRY-RUN: OA available ({', '.join(hosts[:3])})"

    # Step 3: Try ALL OA URLs in priority order (repos before publishers)
    text = None
    fetch_error = None
    tried_urls = []

    for url, url_type, host_type in all_urls:
        # Heuristic: if classified as html but URL looks like PDF, try PDF first
        effective_type = url_type
        if url_type == "html" and url_looks_like_pdf(url):
            effective_type = "pdf"

        print(f"    Trying {effective_type} from {host_type}: {url[:80]}...")

        if effective_type == "pdf":
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
                tmp_path = tmp.name
            try:
                ok, detail = download_pdf(url, tmp_path)
                if ok:
                    stats["pdf_fetched"] += 1
                    text = extract_text_from_pdf(tmp_path)
                    if text:
                        oa_url, oa_type = url, "pdf"
                        break
                    else:
                        tried_urls.append(f"pdftotext empty ({host_type})")
                else:
                    tried_urls.append(f"{detail} ({host_type})")
            finally:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)

        if text is None and (url_type == "html" or effective_type != url_type):
            text = fetch_html_text(url)
            if text:
                stats["html_fetched"] += 1
                oa_url, oa_type = url, "html"
                break
            else:
                tried_urls.append(f"HTML empty ({host_type})")

    if not text:
        fetch_error = f"All {len(all_urls)} URLs failed: {'; '.join(tried_urls[:5])}"

    if not text:
        stats["errors"] += 1
        error_msg = fetch_error or "Could not extract text (unknown reason)"
        paper_results.append({
            "key": key, "doi": doi, "status": "ERROR",
            "oa_url": oa_url, "oa_type": oa_type,
            "error": error_msg,
        })
        return f"ERROR: {error_msg}"

    # Step 4: Clean up
    text = cleanup_text(text)

    # Step 5: Validate L3
    is_l3, level_str, details = validate_l3(text)

    # Step 6: Save
    metadata = {
        "doi": doi,
        "source": f"unpaywall_{oa_type}",
        "oa_url": oa_url,
        "host_type": unpaywall.get("best_oa_location", {}).get("host_type", "unknown"),
    }

    text_path = save_fulltext(key, text, metadata)

    # Step 7: Update YAML
    new_level = "L3" if is_l3 else "L2"

    if "full_text" not in data:
        data["full_text"] = {}

    data["full_text"]["available"] = True
    data["full_text"]["path"] = str(text_path)
    data["full_text"]["content_level"] = new_level
    data["full_text"]["format"] = "markdown"
    data["full_text"]["archived_date"] = datetime.now().strftime("%Y-%m-%d")
    data["full_text"]["word_count"] = details["word_count"]
    data["full_text"]["has_references"] = details["has_references"]
    data["full_text"]["source"] = f"unpaywall_{oa_type}"

    if is_l3:
        data["l3_upgrade_date"] = datetime.now().strftime("%Y-%m-%d")
        data["l3_upgrade_method"] = "unpaywall_fulltext_fetch_v1"

    save_paper_yaml(key, data)

    if is_l3:
        stats["l3_upgraded"] += 1
        paper_results.append({
            "key": key, "doi": doi, "status": "L3",
            "word_count": details["word_count"],
            "has_references": details["has_references"],
            "oa_type": oa_type,
        })
        return f"L3 ✓ ({details['word_count']} words, refs={'yes' if details['has_references'] else 'no'})"
    else:
        stats["l2_partial"] += 1
        paper_results.append({
            "key": key, "doi": doi, "status": "L2+",
            "word_count": details["word_count"],
            "has_references": details["has_references"],
            "oa_type": oa_type,
            "reason": level_str,
        })
        return f"L2+ ({details['word_count']} words, refs={'yes' if details['has_references'] else 'no'}) — {level_str}"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def get_l2_papers(author_filter: str | None = None) -> list[tuple[str, dict]]:
    """Get all L2 papers with DOIs."""
    papers = []

    pattern = f"PAP-{author_filter}*.yaml" if author_filter else "PAP-*.yaml"

    for path in sorted(PAPERS_DIR.glob(pattern)):
        with open(path) as f:
            data = yaml.safe_load(f)

        if not data:
            continue

        # Check if L2
        cl = data.get("full_text", {}).get("content_level", "")
        if cl != "L2":
            continue

        # Already has full text?
        if data.get("full_text", {}).get("available") and data.get("full_text", {}).get("word_count", 0) > 0:
            continue

        key = data.get("bibtex_key") or path.stem.replace("PAP-", "")
        has_doi = bool((data.get("doi") or "").strip())
        papers.append((key, data, has_doi))

    # Sort: papers with DOI first, then alphabetically
    papers.sort(key=lambda x: (not x[2], x[0]))

    return [(k, d) for k, d, _ in papers]


def main():
    parser = argparse.ArgumentParser(description="Fetch full texts for L2 papers (Open Access)")
    parser.add_argument("--batch", type=int, default=5, help="Number of papers to process")
    parser.add_argument("--dry-run", action="store_true", help="Check OA availability without downloading")
    parser.add_argument("--author", type=str, default=None, help="Filter by author (e.g., 'sutter')")
    parser.add_argument("--key", type=str, default=None, help="Process a specific paper key")
    parser.add_argument("--list-oa", action="store_true", help="Just list OA availability stats")
    args = parser.parse_args()

    print("=" * 70)
    print("FULL-TEXT FETCH (L2 → L3 UPGRADE)")
    print("=" * 70)
    print(f"Batch size: {args.batch}")
    print(f"Dry run: {args.dry_run}")
    print(f"Author filter: {args.author or 'none'}")
    print()

    # Get papers
    if args.key:
        data = load_paper_yaml(args.key)
        if not data:
            print(f"Paper not found: {args.key}")
            return
        papers = [(args.key, data)]
    else:
        papers = get_l2_papers(args.author)

    print(f"L2 papers eligible: {len(papers)}")

    if args.batch > 0:
        papers = papers[: args.batch]

    print(f"Processing: {len(papers)}")
    print("-" * 70)

    for i, (key, data) in enumerate(papers, 1):
        stats["processed"] += 1
        print(f"\n[{i}/{len(papers)}] PAP-{key}")

        result = process_paper(key, data, dry_run=args.dry_run)
        print(f"  → {result}")

    # Summary
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Processed:       {stats['processed']}")
    print(f"OA found:        {stats['oa_found']}")
    print(f"PDFs fetched:    {stats['pdf_fetched']}")
    print(f"HTMLs fetched:   {stats['html_fetched']}")
    print(f"L3 upgraded:     {stats['l3_upgraded']}")
    print(f"L2+ (partial):   {stats['l2_partial']}")
    print(f"Skipped (no OA): {stats['skipped_no_oa']}")
    print(f"Skipped (no DOI):{stats['skipped_no_doi']}")
    print(f"Errors:          {stats['errors']}")

    if args.dry_run:
        print("\n[DRY RUN] No files were modified")

    # Write summary as artifact
    summary_path = Path("data/fulltext-fetch-log.yaml")
    summary = {
        "run_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "batch_size": args.batch,
        "dry_run": args.dry_run,
        "author_filter": args.author,
        "stats": dict(stats),
    }
    if paper_results:
        summary["paper_details"] = paper_results
    with open(summary_path, "w") as f:
        yaml.dump(summary, f, default_flow_style=False, allow_unicode=True)


if __name__ == "__main__":
    main()
