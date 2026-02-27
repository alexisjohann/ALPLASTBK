#!/usr/bin/env python3
"""
AEA Full-Text HTML Fetcher
===========================
Fetches full-text articles from aeaweb.org HTML pages (not PDFs).
JEP and other AEA journals are open access — HTML is freely available.

Approach:
  1. Given an issue DOI (e.g., 10.1257/jep.40.1), fetch the issue page
  2. Extract all article DOIs from the issue
  3. For each article, fetch the HTML full text
  4. Convert to clean Markdown and save to data/paper-texts/

Usage:
    # Fetch all articles from a specific issue
    python scripts/fetch_aea_fulltext.py --issue 10.1257/jep.40.1

    # Fetch specific DOIs
    python scripts/fetch_aea_fulltext.py --dois "10.1257/jep.20231394,10.1257/jep.20241415"

    # Dry run (show what would be fetched)
    python scripts/fetch_aea_fulltext.py --issue 10.1257/jep.40.1 --dry-run

Requirements (GitHub Actions runner):
    pip install requests beautifulsoup4 pyyaml
"""

import argparse
import re
import sys
import time
from datetime import datetime
from pathlib import Path

import requests
import yaml

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("ERROR: beautifulsoup4 not installed. Run: pip install beautifulsoup4")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
TEXTS_DIR = Path("data/paper-texts")
LOG_FILE = Path("data/aea-fetch-log.yaml")

# Browser-like headers (AEA blocks bot user-agents)
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

AEA_BASE = "https://www.aeaweb.org"
REQUEST_DELAY = 1.0  # seconds between requests (be polite)


# ---------------------------------------------------------------------------
# Fetch issue page → extract article DOIs
# ---------------------------------------------------------------------------
def fetch_issue_articles(issue_doi: str) -> list[dict]:
    """Fetch the full issue page and extract all article metadata.

    Args:
        issue_doi: e.g., "10.1257/jep.40.1"

    Returns:
        List of dicts with keys: doi, title, authors, url
    """
    url = f"{AEA_BASE}/full_issue.php?doi={issue_doi}"
    print(f"  Fetching issue page: {url}")

    resp = requests.get(url, headers=HEADERS, timeout=30)
    if resp.status_code != 200:
        print(f"  ERROR: HTTP {resp.status_code} for issue page")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    articles = []

    # Find all article sections
    # AEA issue pages have article listings with titles, authors, DOIs
    for article_div in soup.select("article, .article-listing, .journal-article"):
        title_el = article_div.select_one("h3 a, .title a, a.title")
        if not title_el:
            continue

        title = title_el.get_text(strip=True)
        href = title_el.get("href", "")

        # Extract DOI from href (format: /articles?id=10.1257/jep.XXXXX)
        doi = ""
        if "id=" in href:
            doi = href.split("id=")[-1]
        elif "doi/" in href:
            doi = href.split("doi/")[-1]

        # Extract authors
        author_el = article_div.select_one(".author, .authors, .contrib")
        authors = author_el.get_text(strip=True) if author_el else ""

        if doi:
            articles.append({
                "doi": doi,
                "title": title,
                "authors": authors,
                "url": f"{AEA_BASE}{href}" if href.startswith("/") else href,
            })

    # Fallback: parse links that contain article DOIs
    if not articles:
        print("  Trying fallback link parsing...")
        for link in soup.find_all("a", href=True):
            href = link["href"]
            if "/articles?id=10.1257/" in href:
                doi = href.split("id=")[-1]
                title = link.get_text(strip=True)
                if doi and title and len(title) > 10:
                    articles.append({
                        "doi": doi,
                        "title": title,
                        "authors": "",
                        "url": f"{AEA_BASE}{href}" if href.startswith("/") else href,
                    })

    # Deduplicate by DOI
    seen = set()
    unique = []
    for a in articles:
        if a["doi"] not in seen:
            seen.add(a["doi"])
            unique.append(a)

    print(f"  Found {len(unique)} articles in issue")
    return unique


# ---------------------------------------------------------------------------
# Fetch single article full text
# ---------------------------------------------------------------------------
def fetch_article_fulltext(doi: str) -> dict | None:
    """Fetch the full text of a single AEA article.

    Args:
        doi: e.g., "10.1257/jep.20231394"

    Returns:
        Dict with keys: title, authors, abstract, sections, references, word_count
        or None on failure.
    """
    url = f"{AEA_BASE}/articles?id={doi}"
    print(f"    Fetching: {url}")

    resp = requests.get(url, headers=HEADERS, timeout=30)
    if resp.status_code != 200:
        print(f"    ERROR: HTTP {resp.status_code}")
        return None

    soup = BeautifulSoup(resp.text, "html.parser")

    # --- Title ---
    title = ""
    title_el = soup.select_one("h1.title, h1.article-title, .article-header h1")
    if title_el:
        title = title_el.get_text(strip=True)
    if not title:
        title_el = soup.find("meta", {"name": "citation_title"})
        if title_el:
            title = title_el.get("content", "")

    # --- Authors ---
    authors = []
    # Try meta tags first (most reliable)
    for meta in soup.find_all("meta", {"name": "citation_author"}):
        authors.append(meta.get("content", ""))
    # Fallback to page elements
    if not authors:
        for a_el in soup.select(".author a, .contrib-group .name"):
            authors.append(a_el.get_text(strip=True))

    # --- Abstract ---
    abstract = ""
    abs_el = soup.select_one(".abstract, #abstract, section.abstract")
    if abs_el:
        abstract = abs_el.get_text(strip=True)
        # Remove "Abstract" prefix
        if abstract.lower().startswith("abstract"):
            abstract = abstract[8:].strip()

    # --- Full text body ---
    body_sections = []

    # Method 1: Look for article body / full text container
    body = soup.select_one(
        "article .article-body, .article-content, "
        "#article-body, .full-text, .article-full-text, "
        "section.article"
    )
    if body:
        body_sections = extract_sections(body)

    # Method 2: Look for all section headings + their content
    if not body_sections:
        for section in soup.select("section[id], div.section"):
            heading = section.find(["h2", "h3", "h4"])
            heading_text = heading.get_text(strip=True) if heading else ""
            paragraphs = []
            for p in section.find_all("p"):
                text = p.get_text(strip=True)
                if text:
                    paragraphs.append(text)
            if paragraphs:
                body_sections.append({
                    "heading": heading_text,
                    "text": "\n\n".join(paragraphs),
                })

    # Method 3: Just get all paragraphs from the main content area
    if not body_sections:
        main = soup.select_one("main, #content, .container")
        if main:
            paragraphs = []
            for p in main.find_all("p"):
                text = p.get_text(strip=True)
                if text and len(text) > 50:  # skip short nav/footer text
                    paragraphs.append(text)
            if paragraphs:
                body_sections.append({
                    "heading": "",
                    "text": "\n\n".join(paragraphs),
                })

    # --- References ---
    references = []
    ref_section = soup.select_one(
        "#references, .references, section.ref-list, "
        ".bibliography, .citation-list"
    )
    if ref_section:
        for ref in ref_section.find_all(["li", "p", "div"], class_=lambda c: c and ("ref" in str(c).lower() or "citation" in str(c).lower())):
            ref_text = ref.get_text(strip=True)
            if ref_text and len(ref_text) > 10:
                references.append(ref_text)
        # Fallback: all list items in references section
        if not references:
            for li in ref_section.find_all("li"):
                ref_text = li.get_text(strip=True)
                if ref_text and len(ref_text) > 10:
                    references.append(ref_text)

    # --- JEL codes ---
    jel_codes = []
    jel_el = soup.select_one(".jel-codes, .jel, .article-jel")
    if jel_el:
        jel_codes = re.findall(r"[A-Z]\d{2}", jel_el.get_text())

    # Compose full text
    full_body = "\n\n".join(
        (f"## {s['heading']}\n\n{s['text']}" if s["heading"] else s["text"])
        for s in body_sections
    )

    word_count = len(f"{title} {abstract} {full_body}".split())

    return {
        "title": title,
        "authors": authors,
        "abstract": abstract,
        "body_sections": body_sections,
        "full_body": full_body,
        "references": references,
        "jel_codes": jel_codes,
        "word_count": word_count,
        "url": url,
    }


def extract_sections(container) -> list[dict]:
    """Extract sections with headings from an HTML container."""
    sections = []
    current_heading = ""
    current_paragraphs = []

    for child in container.children:
        if not hasattr(child, "name") or child.name is None:
            continue

        if child.name in ["h2", "h3", "h4"]:
            # Save previous section
            if current_paragraphs:
                sections.append({
                    "heading": current_heading,
                    "text": "\n\n".join(current_paragraphs),
                })
            current_heading = child.get_text(strip=True)
            current_paragraphs = []
        elif child.name == "p":
            text = child.get_text(strip=True)
            if text:
                current_paragraphs.append(text)
        elif child.name in ["div", "section"]:
            # Recurse into divs
            sub_sections = extract_sections(child)
            if sub_sections:
                # Save current first
                if current_paragraphs:
                    sections.append({
                        "heading": current_heading,
                        "text": "\n\n".join(current_paragraphs),
                    })
                    current_heading = ""
                    current_paragraphs = []
                sections.extend(sub_sections)
        elif child.name in ["ul", "ol"]:
            items = []
            for li in child.find_all("li"):
                items.append(f"- {li.get_text(strip=True)}")
            if items:
                current_paragraphs.append("\n".join(items))
        elif child.name == "table":
            current_paragraphs.append(f"[Table omitted]")
        elif child.name == "figure":
            caption = child.find("figcaption")
            if caption:
                current_paragraphs.append(f"[Figure: {caption.get_text(strip=True)}]")

    # Don't forget the last section
    if current_paragraphs:
        sections.append({
            "heading": current_heading,
            "text": "\n\n".join(current_paragraphs),
        })

    return sections


# ---------------------------------------------------------------------------
# Save article as Markdown
# ---------------------------------------------------------------------------
def save_article_markdown(article: dict, doi: str, key: str) -> Path:
    """Save fetched article as Markdown file.

    Args:
        article: Result from fetch_article_fulltext()
        doi: The article DOI
        key: File key (e.g., "manual-1" or bibtex key)

    Returns:
        Path to saved file
    """
    TEXTS_DIR.mkdir(parents=True, exist_ok=True)
    text_path = TEXTS_DIR / f"PAP-{key}.md"

    lines = []
    lines.append(f"---")
    lines.append(f"# Full text fetched from AEA HTML")
    lines.append(f"# Source: aeaweb.org")
    lines.append(f"# DOI: {doi}")
    lines.append(f"# URL: {article['url']}")
    lines.append(f"# Fetched: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"# Word count: {article['word_count']}")
    lines.append(f"---")
    lines.append(f"")
    lines.append(f"# {article['title']}")
    lines.append(f"")

    if article["authors"]:
        lines.append(f"**Authors:** {', '.join(article['authors'])}")
        lines.append(f"")

    if article["jel_codes"]:
        lines.append(f"**JEL:** {', '.join(article['jel_codes'])}")
        lines.append(f"")

    if article["abstract"]:
        lines.append(f"## Abstract")
        lines.append(f"")
        lines.append(article["abstract"])
        lines.append(f"")

    if article["full_body"]:
        lines.append(article["full_body"])
        lines.append(f"")

    if article["references"]:
        lines.append(f"## References")
        lines.append(f"")
        for ref in article["references"]:
            lines.append(f"- {ref}")
        lines.append(f"")

    text_path.write_text("\n".join(lines), encoding="utf-8")
    return text_path


# ---------------------------------------------------------------------------
# Generate bibtex-style key from DOI
# ---------------------------------------------------------------------------
def doi_to_key(doi: str) -> str:
    """Generate a simple key from DOI for file naming.

    e.g., 10.1257/jep.20231394 → jep-20231394
    """
    # Take the part after the last /
    suffix = doi.split("/")[-1] if "/" in doi else doi
    # Clean for filename
    return re.sub(r"[^a-zA-Z0-9\-]", "-", suffix)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Fetch full-text articles from AEA HTML pages"
    )
    parser.add_argument("--issue", type=str, default="",
                        help="Issue DOI (e.g., 10.1257/jep.40.1)")
    parser.add_argument("--dois", type=str, default="",
                        help="Comma-separated article DOIs")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be fetched without downloading")
    parser.add_argument("--batch", type=int, default=50,
                        help="Max articles to fetch")

    args = parser.parse_args()

    print("╔" + "═" * 58 + "╗")
    print("║  AEA FULL-TEXT HTML FETCHER                               ║")
    print("║  Source: aeaweb.org (HTML, not PDF)                       ║")
    print("╚" + "═" * 58 + "╝")

    # Determine articles to fetch
    articles_to_fetch = []

    if args.issue:
        print(f"\n  Issue: {args.issue}")
        issue_articles = fetch_issue_articles(args.issue)
        for a in issue_articles:
            articles_to_fetch.append({
                "doi": a["doi"],
                "title": a["title"],
                "key": doi_to_key(a["doi"]),
            })

    if args.dois:
        raw_dois = args.dois.strip().strip("'\"")
        for i, doi in enumerate(raw_dois.split(","), 1):
            doi = doi.strip().strip("'\"")
            if doi:
                articles_to_fetch.append({
                    "doi": doi,
                    "title": "",
                    "key": doi_to_key(doi),
                })

    if not articles_to_fetch:
        print("  No articles to fetch. Use --issue or --dois.")
        sys.exit(1)

    # Limit to batch size
    articles_to_fetch = articles_to_fetch[:args.batch]
    print(f"\n  Articles to fetch: {len(articles_to_fetch)}")

    if args.dry_run:
        print("\n  [DRY RUN] Would fetch:")
        for a in articles_to_fetch:
            print(f"    - {a['doi']}: {a.get('title', '(unknown)')}")
        sys.exit(0)

    # Fetch each article
    TEXTS_DIR.mkdir(parents=True, exist_ok=True)
    results = []
    success = 0
    failed = 0

    for i, item in enumerate(articles_to_fetch, 1):
        doi = item["doi"]
        key = item["key"]

        print(f"\n  [{i}/{len(articles_to_fetch)}] {doi}")

        time.sleep(REQUEST_DELAY)

        article = fetch_article_fulltext(doi)
        if not article:
            print(f"    FAILED: Could not fetch article")
            failed += 1
            results.append({
                "key": key,
                "doi": doi,
                "status": "failed",
                "word_count": 0,
            })
            continue

        # Use title from article if we didn't have it
        if not item["title"] and article["title"]:
            item["title"] = article["title"]

        # Determine content level
        wc = article["word_count"]
        if wc >= 10000 and article["references"]:
            level = "L3"
        elif wc >= 5000:
            level = "L3"
        elif wc >= 1000:
            level = "L2"
        else:
            level = "L1"

        # Save
        saved_path = save_article_markdown(article, doi, key)
        print(f"    Saved: {saved_path} ({wc:,} words, {level})")
        print(f"    Title: {article['title'][:80]}")
        print(f"    Sections: {len(article['body_sections'])}")
        print(f"    References: {len(article['references'])}")

        success += 1
        results.append({
            "key": key,
            "doi": doi,
            "title": article["title"],
            "authors": ", ".join(article["authors"]),
            "status": "success",
            "word_count": wc,
            "content_level": level,
            "sections": len(article["body_sections"]),
            "references": len(article["references"]),
        })

    # Summary
    print(f"\n{'=' * 60}")
    print(f"  SUMMARY: {success} success, {failed} failed")
    print(f"{'=' * 60}")

    # Write log
    log = {
        "run_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source": "aeaweb.org",
        "method": "html",
        "stats": {
            "total": len(articles_to_fetch),
            "success": success,
            "failed": failed,
        },
        "results": results,
    }

    LOG_FILE.write_text(yaml.dump(log, default_flow_style=False, allow_unicode=True),
                        encoding="utf-8")
    print(f"  Log: {LOG_FILE}")


if __name__ == "__main__":
    main()
