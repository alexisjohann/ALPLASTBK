#!/usr/bin/env python3
"""
Multi-Source Full-Text PDF Fetcher
===================================
Finds and downloads PDFs from multiple open-access sources.

Source Cascade (waterfall — stops at first hit):
  1. Unpaywall      (DOI → best OA location, 100k/day)
  2. OpenAlex       (DOI → 60M cached PDFs on S3)
  3. EconStor       (title search → ZBW bitstream)
  4. Semantic Scholar (DOI → openAccessPdf link)
  5. MPG PuRe       (person search → INTERNAL_MANAGED)

Design principle: "The PDF exists SOMEWHERE — find it."
Learned from Engel cross-validation: PuRe had only 2/250 papers,
but EconStor and ScienceDirect had many more.

Usage:
    # Scan DOIs from bibtex, find PDF sources
    python scripts/fetch_fulltext_multisource.py --scan --author engel

    # Fetch PDFs for papers with known DOIs
    python scripts/fetch_fulltext_multisource.py --fetch --batch 20

    # Dry run (scan only, no downloads)
    python scripts/fetch_fulltext_multisource.py --scan --author sutter --dry-run

    # Fetch for specific DOIs
    python scripts/fetch_fulltext_multisource.py --fetch --dois "10.1177/002,10.2139/ssrn"

Requirements (GitHub Actions runner):
    pip install requests pyyaml
    apt-get install poppler-utils  # for pdftotext
"""

import argparse
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
BIB_FILE = Path("bibliography/bcm_master.bib")
LOG_FILE = Path("data/multisource-fetch-log.yaml")

USER_AGENT = "EBF-Framework/1.0 (mailto:research@fehradvice.com)"
# Browser-like UA for publisher sites that block bots
BROWSER_UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
CONTACT_EMAIL = "research@fehradvice.com"
REQUEST_DELAY = 0.5  # seconds between API calls

# L3 requirements
MIN_WORDS_ARTICLE = 10000
MIN_WORDS_SHORT = 5000

# Source priority (lower = tried first)
SOURCES = [
    "unpaywall",
    "openalex",
    "econstor",
    "semantic_scholar",
    "pure_mpg",
]


# ---------------------------------------------------------------------------
# Stats
# ---------------------------------------------------------------------------
stats = {
    "total_dois": 0,
    "already_have_fulltext": 0,
    "scanned": 0,
    "pdf_found": 0,
    "pdf_downloaded": 0,
    "pdf_converted": 0,
    "l3_upgraded": 0,
    "errors": 0,
    "source_hits": {s: 0 for s in SOURCES},
    "source_misses": {s: 0 for s in SOURCES},
}

results = []


# ---------------------------------------------------------------------------
# DOI Sanitization
# ---------------------------------------------------------------------------
def sanitize_doi(doi: str) -> str:
    """Clean DOI string: strip quotes, whitespace, URL prefixes."""
    if not doi:
        return doi
    # Strip whitespace and quotes
    doi = doi.strip().strip("'\"")
    # Remove URL prefix if present
    for prefix in ["https://doi.org/", "http://doi.org/", "doi:"]:
        if doi.lower().startswith(prefix):
            doi = doi[len(prefix):]
    return doi.strip()


# Publisher domains that block bot User-Agents
PUBLISHER_DOMAINS = [
    "aeaweb.org", "jstor.org", "sciencedirect.com", "springer.com",
    "wiley.com", "tandfonline.com", "oxfordjournals.org", "nber.org",
    "cambridge.org", "uchicago.edu",
]


def is_publisher_url(url: str) -> bool:
    """Check if URL is from a publisher that blocks bot UAs."""
    return any(domain in url.lower() for domain in PUBLISHER_DOMAINS)


# ---------------------------------------------------------------------------
# Source 1: Unpaywall
# ---------------------------------------------------------------------------
def search_unpaywall(doi: str) -> dict | None:
    """Query Unpaywall for OA PDF location.

    Returns: {"pdf_url": str, "source": str, "host_type": str} or None
    """
    url = f"https://api.unpaywall.org/v2/{doi}"
    params = {"email": CONTACT_EMAIL}

    try:
        resp = requests.get(url, params=params, headers={"User-Agent": USER_AGENT},
                            timeout=15)
        if resp.status_code == 404:
            return None
        if resp.status_code != 200:
            print(f"    Unpaywall: HTTP {resp.status_code}")
            return None

        data = resp.json()

        # Try best_oa_location first
        best = data.get("best_oa_location") or {}
        pdf_url = best.get("url_for_pdf") or best.get("url")
        if pdf_url and pdf_url.endswith(".pdf"):
            return {
                "pdf_url": pdf_url,
                "source": "unpaywall",
                "host_type": best.get("host_type", "unknown"),
                "version": best.get("version", "unknown"),
                "license": best.get("license", "unknown"),
            }

        # Try all oa_locations
        for loc in data.get("oa_locations", []):
            pdf_url = loc.get("url_for_pdf") or loc.get("url")
            if pdf_url and pdf_url.endswith(".pdf"):
                return {
                    "pdf_url": pdf_url,
                    "source": "unpaywall",
                    "host_type": loc.get("host_type", "unknown"),
                    "version": loc.get("version", "unknown"),
                    "license": loc.get("license", "unknown"),
                }

        return None

    except requests.RequestException as e:
        print(f"    Unpaywall error: {e}")
        return None


# ---------------------------------------------------------------------------
# Source 2: OpenAlex
# ---------------------------------------------------------------------------
def search_openalex(doi: str) -> dict | None:
    """Query OpenAlex for PDF URL (60M cached PDFs).

    Returns: {"pdf_url": str, "source": str, ...} or None
    """
    url = f"https://api.openalex.org/works/doi:{doi}"
    params = {"mailto": CONTACT_EMAIL}

    try:
        resp = requests.get(url, params=params, headers={"User-Agent": USER_AGENT},
                            timeout=15)
        if resp.status_code == 404:
            return None
        if resp.status_code != 200:
            print(f"    OpenAlex: HTTP {resp.status_code}")
            return None

        data = resp.json()

        # Check primary_location for PDF
        primary = data.get("primary_location") or {}
        pdf_url = primary.get("pdf_url")
        if pdf_url:
            return {
                "pdf_url": pdf_url,
                "source": "openalex",
                "host_type": primary.get("source", {}).get("type", "unknown"),
                "openalex_id": data.get("id", ""),
                "has_fulltext": data.get("has_fulltext", False),
            }

        # Check best_oa_location
        best_oa = data.get("best_oa_location") or {}
        pdf_url = best_oa.get("pdf_url")
        if pdf_url:
            return {
                "pdf_url": pdf_url,
                "source": "openalex",
                "host_type": best_oa.get("source", {}).get("type", "unknown"),
                "openalex_id": data.get("id", ""),
            }

        # Check all locations
        for loc in data.get("locations", []):
            pdf_url = loc.get("pdf_url")
            if pdf_url:
                return {
                    "pdf_url": pdf_url,
                    "source": "openalex",
                    "host_type": loc.get("source", {}).get("type", "unknown"),
                    "openalex_id": data.get("id", ""),
                }

        return None

    except requests.RequestException as e:
        print(f"    OpenAlex error: {e}")
        return None


# ---------------------------------------------------------------------------
# Source 2b: OpenAlex Fulltext (NGRAMS/abstract — returns text directly)
# ---------------------------------------------------------------------------
def fetch_openalex_fulltext(doi: str) -> dict | None:
    """Try OpenAlex fulltext content API (returns text, no PDF needed).

    OpenAlex has indexed the full text of ~60M papers. When has_fulltext=True,
    we can get the text via the fulltext search or the abstract + title.
    Also returns the paper title for file naming.
    """
    url = f"https://api.openalex.org/works/doi:{doi}"
    params = {"mailto": CONTACT_EMAIL, "select": "id,title,has_fulltext,open_access,abstract_inverted_index,authorships"}

    try:
        resp = requests.get(url, params=params, headers={"User-Agent": USER_AGENT},
                            timeout=15)
        if resp.status_code != 200:
            return None

        data = resp.json()
        title = data.get("title", "")
        has_fulltext = data.get("has_fulltext", False)
        openalex_id = data.get("id", "")

        # Reconstruct abstract from inverted index
        abstract_idx = data.get("abstract_inverted_index") or {}
        if abstract_idx:
            max_pos = max(pos for positions in abstract_idx.values() for pos in positions)
            words = [""] * (max_pos + 1)
            for word, positions in abstract_idx.items():
                for pos in positions:
                    words[pos] = word
            abstract = " ".join(words)
        else:
            abstract = ""

        # Get authors
        authorships = data.get("authorships", [])
        authors = [a.get("author", {}).get("display_name", "") for a in authorships]

        if title or abstract:
            return {
                "source": "openalex_meta",
                "title": title,
                "abstract": abstract,
                "authors": authors,
                "openalex_id": openalex_id,
                "has_fulltext": has_fulltext,
            }

        return None

    except requests.RequestException as e:
        print(f"    OpenAlex fulltext error: {e}")
        return None


# ---------------------------------------------------------------------------
# Source 3: EconStor (ZBW)
# ---------------------------------------------------------------------------
def search_econstor(doi: str, title: str = "") -> dict | None:
    """Search EconStor for PDF (300k+ economics papers).

    EconStor uses DSpace. We search via the simple search API.
    Returns: {"pdf_url": str, "source": str, ...} or None
    """
    # Try DOI-based search first
    search_term = doi if doi else title
    if not search_term:
        return None

    url = "https://www.econstor.eu/rest/items/find-by-metadata-field"

    # Try searching via the OAI-PMH or simple REST
    # EconStor DSpace REST: /rest/items?query=...
    search_url = f"https://www.econstor.eu/rest/items"
    params = {"query": search_term, "limit": 5, "expand": "bitstreams"}

    try:
        resp = requests.get(search_url, params=params,
                            headers={"User-Agent": USER_AGENT},
                            timeout=15)
        if resp.status_code != 200:
            # Try alternative: search via handle resolver
            if doi:
                alt_url = f"https://www.econstor.eu/api/core/items?query={doi}"
                resp = requests.get(alt_url,
                                    headers={"User-Agent": USER_AGENT},
                                    timeout=15)
                if resp.status_code != 200:
                    return None
            else:
                return None

        data = resp.json()
        if not isinstance(data, list):
            data = data.get("_embedded", {}).get("items", []) if isinstance(data, dict) else []

        for item in data[:5]:
            # Look for PDF bitstreams
            bitstreams = item.get("bitstreams", [])
            if isinstance(bitstreams, list):
                for bs in bitstreams:
                    if bs.get("mimeType") == "application/pdf":
                        link = bs.get("retrieveLink") or bs.get("link")
                        if link:
                            if not link.startswith("http"):
                                link = f"https://www.econstor.eu{link}"
                            return {
                                "pdf_url": link,
                                "source": "econstor",
                                "handle": item.get("handle", ""),
                            }

        return None

    except requests.RequestException as e:
        print(f"    EconStor error: {e}")
        return None


# ---------------------------------------------------------------------------
# Source 4: Semantic Scholar
# ---------------------------------------------------------------------------
def search_semantic_scholar(doi: str) -> dict | None:
    """Query Semantic Scholar for OA PDF link.

    Returns: {"pdf_url": str, "source": str, ...} or None
    """
    url = f"https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}"
    params = {"fields": "openAccessPdf,title,year"}

    try:
        resp = requests.get(url, params=params,
                            headers={"User-Agent": USER_AGENT},
                            timeout=15)
        if resp.status_code == 404:
            return None
        if resp.status_code == 429:
            print("    Semantic Scholar: Rate limited, waiting 5s...")
            time.sleep(5)
            resp = requests.get(url, params=params,
                                headers={"User-Agent": USER_AGENT},
                                timeout=15)
        if resp.status_code != 200:
            print(f"    Semantic Scholar: HTTP {resp.status_code}")
            return None

        data = resp.json()
        oa_pdf = data.get("openAccessPdf") or {}
        pdf_url = oa_pdf.get("url")
        if pdf_url:
            return {
                "pdf_url": pdf_url,
                "source": "semantic_scholar",
                "s2_status": oa_pdf.get("status", "unknown"),
            }

        return None

    except requests.RequestException as e:
        print(f"    Semantic Scholar error: {e}")
        return None


# ---------------------------------------------------------------------------
# PDF Download & Conversion
# ---------------------------------------------------------------------------
def download_pdf(pdf_url: str, output_path: Path) -> bool:
    """Download a PDF file. Returns True on success.

    Uses browser-like headers for publisher sites that block bots.
    """
    try:
        # Use browser-like headers for publisher sites
        if is_publisher_url(pdf_url):
            headers = {
                "User-Agent": BROWSER_UA,
                "Accept": "application/pdf,*/*",
                "Accept-Language": "en-US,en;q=0.9",
                "Referer": pdf_url.split("/pdf/")[0] if "/pdf/" in pdf_url else pdf_url,
            }
            print(f"    Using browser headers for publisher site")
        else:
            headers = {"User-Agent": USER_AGENT}

        resp = requests.get(pdf_url, headers=headers,
                            timeout=60, stream=True, allow_redirects=True)

        if resp.status_code == 403:
            print(f"    Download blocked (403 Forbidden) — publisher blocks automated access")
            return False
        if resp.status_code != 200:
            print(f"    Download failed: HTTP {resp.status_code}")
            return False

        # Check content type
        ct = resp.headers.get("Content-Type", "")
        if "pdf" not in ct.lower() and "octet-stream" not in ct.lower():
            # Some sites return HTML login pages instead of PDFs
            if "html" in ct.lower():
                print(f"    Got HTML instead of PDF (likely paywall/login page)")
            else:
                print(f"    Not a PDF: Content-Type={ct}")
            return False

        # Write to file
        with open(output_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)

        size = output_path.stat().st_size
        if size < 1000:
            print(f"    File too small ({size} bytes), likely not a real PDF")
            output_path.unlink()
            return False

        # Additional check: PDF magic bytes
        with open(output_path, "rb") as f:
            magic = f.read(5)
        if magic != b"%PDF-":
            print(f"    File is not a valid PDF (magic bytes: {magic!r})")
            output_path.unlink()
            return False

        print(f"    Downloaded: {size:,} bytes")
        return True

    except requests.RequestException as e:
        print(f"    Download error: {e}")
        return False


def pdf_to_text(pdf_path: Path) -> str | None:
    """Convert PDF to text using pdftotext."""
    try:
        result = subprocess.run(
            ["pdftotext", "-layout", str(pdf_path), "-"],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode != 0:
            print(f"    pdftotext failed: {result.stderr[:200]}")
            return None

        text = result.stdout.strip()
        if len(text) < 100:
            print(f"    Extracted text too short ({len(text)} chars)")
            return None

        return text

    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f"    pdftotext error: {e}")
        return None


# ---------------------------------------------------------------------------
# BibTeX DOI Extraction
# ---------------------------------------------------------------------------
def extract_dois_from_bibtex(bib_path: Path, author_filter: str = "") -> list[dict]:
    """Extract DOIs and titles from bcm_master.bib.

    Returns list of {"key": str, "doi": str, "title": str, "author": str}
    """
    entries = []
    current = {}

    with open(bib_path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()

            # New entry
            if line.startswith("@") and "{" in line:
                if current.get("key"):
                    entries.append(current)
                key = line.split("{", 1)[1].rstrip(",").strip()
                current = {"key": key, "doi": "", "title": "", "author": ""}
                continue

            # Fields
            low = line.lower()
            if low.startswith("doi"):
                doi = re.search(r'=\s*\{([^}]+)\}', line)
                if doi:
                    current["doi"] = doi.group(1).strip()
            elif low.startswith("title"):
                title = re.search(r'=\s*\{(.+)\}', line)
                if title:
                    current["title"] = title.group(1).strip()
            elif low.startswith("author"):
                author = re.search(r'=\s*\{(.+)\}', line)
                if author:
                    current["author"] = author.group(1).strip()

    # Don't forget last entry
    if current.get("key"):
        entries.append(current)

    # Filter by author if requested
    if author_filter:
        af = author_filter.lower()
        entries = [e for e in entries if af in e.get("author", "").lower()]

    # Filter to entries with DOIs
    with_doi = [e for e in entries if e.get("doi")]

    print(f"  BibTeX: {len(entries)} entries" +
          (f" matching '{author_filter}'" if author_filter else "") +
          f", {len(with_doi)} with DOIs")

    return with_doi


# ---------------------------------------------------------------------------
# Paper YAML Integration
# ---------------------------------------------------------------------------
def find_paper_yaml(doi: str, bibtex_key: str = "") -> Path | None:
    """Find the PAP-*.yaml file for a DOI or bibtex key."""
    if not PAPERS_DIR.exists():
        return None

    # Try by bibtex key first
    if bibtex_key:
        yaml_path = PAPERS_DIR / f"PAP-{bibtex_key}.yaml"
        if yaml_path.exists():
            return yaml_path

    # Search by DOI in YAML files
    for yaml_file in PAPERS_DIR.glob("PAP-*.yaml"):
        try:
            with open(yaml_file, "r") as f:
                content = f.read()
                if doi and doi in content:
                    return yaml_file
        except Exception:
            continue

    return None


def check_has_fulltext(bibtex_key: str) -> bool:
    """Check if we already have full text for this paper."""
    text_path = TEXTS_DIR / f"PAP-{bibtex_key}.md"
    return text_path.exists() and text_path.stat().st_size > 1000


# ---------------------------------------------------------------------------
# Main: Scan Mode
# ---------------------------------------------------------------------------
def run_scan(entries: list[dict], dry_run: bool = False) -> list[dict]:
    """Scan DOIs across all sources to find PDF locations.

    Returns list of scan results with found PDF URLs.
    """
    print(f"\n{'=' * 60}")
    print(f"SCAN: Finding PDF sources for {len(entries)} papers")
    print(f"{'=' * 60}")

    scan_results = []

    for i, entry in enumerate(entries, 1):
        doi = sanitize_doi(entry["doi"])
        key = entry["key"]
        title = entry.get("title", "")

        print(f"\n  [{i}/{len(entries)}] {key}")
        print(f"    DOI: {doi}")
        print(f"    Title: {title[:70]}{'...' if len(title) > 70 else ''}")

        stats["scanned"] += 1

        # Skip if we already have fulltext
        if check_has_fulltext(key):
            print(f"    → Already have full text, skipping")
            stats["already_have_fulltext"] += 1
            scan_results.append({
                "key": key, "doi": doi, "status": "already_have_fulltext"
            })
            continue

        # Cascade through sources
        found = None
        for source_name in SOURCES:
            time.sleep(REQUEST_DELAY)

            if source_name == "unpaywall":
                found = search_unpaywall(doi)
            elif source_name == "openalex":
                found = search_openalex(doi)
            elif source_name == "econstor":
                found = search_econstor(doi, title)
            elif source_name == "semantic_scholar":
                found = search_semantic_scholar(doi)
            elif source_name == "pure_mpg":
                # PuRe is handled by fetch_mpg_fulltext.py separately
                continue

            if found:
                stats["source_hits"][source_name] += 1
                stats["pdf_found"] += 1
                print(f"    ✓ Found via {source_name}: {found['pdf_url'][:80]}...")
                scan_results.append({
                    "key": key,
                    "doi": doi,
                    "title": title[:100],
                    "status": "found",
                    **found,
                })
                break
            else:
                stats["source_misses"][source_name] += 1

        if not found:
            print(f"    ✗ No OA PDF found across {len(SOURCES)} sources")
            scan_results.append({
                "key": key, "doi": doi, "title": title[:100],
                "status": "not_found",
            })

    return scan_results


# ---------------------------------------------------------------------------
# Main: Fetch Mode
# ---------------------------------------------------------------------------
def run_fetch(scan_results: list[dict], batch_size: int = 50,
              dry_run: bool = False) -> list[dict]:
    """Download PDFs and convert to text.

    Takes scan results with pdf_url and downloads them.
    """
    fetchable = [r for r in scan_results if r.get("status") == "found" and r.get("pdf_url")]

    if not fetchable:
        print("\n  No PDFs to fetch.")
        return []

    print(f"\n{'=' * 60}")
    print(f"FETCH: Downloading {min(len(fetchable), batch_size)} of {len(fetchable)} PDFs")
    print(f"{'=' * 60}")

    if dry_run:
        print("  [DRY RUN] Skipping downloads.")
        return fetchable[:batch_size]

    TEXTS_DIR.mkdir(parents=True, exist_ok=True)
    fetch_results = []

    for i, item in enumerate(fetchable[:batch_size], 1):
        key = item["key"]
        doi = item["doi"]
        pdf_url = item["pdf_url"]
        source = item.get("source", "unknown")

        print(f"\n  [{i}/{min(len(fetchable), batch_size)}] {key}")
        print(f"    Source: {source}")
        print(f"    URL: {pdf_url[:80]}...")

        # Download PDF to temp file
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp_path = Path(tmp.name)

        try:
            if not download_pdf(pdf_url, tmp_path):
                # Fallback: try OpenAlex metadata (title + abstract → L1/L2)
                print(f"    → PDF download failed, trying OpenAlex metadata fallback...")
                meta = fetch_openalex_fulltext(doi)
                if meta and (meta.get("abstract") or meta.get("title")):
                    title_str = meta.get("title", "")
                    abstract_str = meta.get("abstract", "")
                    authors_str = ", ".join(meta.get("authors", []))
                    meta_text = f"# {title_str}\n\n**Authors:** {authors_str}\n\n## Abstract\n\n{abstract_str}"
                    word_count = len(meta_text.split())
                    text_path = TEXTS_DIR / f"PAP-{key}.md"
                    header = f"""---
# Full text fetched via multi-source cascade (metadata fallback)
# Source: openalex_meta
# DOI: {doi}
# Fetched: {datetime.now().strftime('%Y-%m-%d %H:%M')}
# Word count: {word_count}
# Note: PDF download failed — abstract only (L1)
---

"""
                    text_path.write_text(header + meta_text, encoding="utf-8")
                    print(f"    → Saved metadata fallback: {text_path} ({word_count} words)")
                    item["fetch_status"] = "metadata_only"
                    item["word_count"] = word_count
                    item["content_level"] = "L1"
                    item["title"] = title_str
                    fetch_results.append(item)
                    continue

                stats["errors"] += 1
                item["fetch_status"] = "download_failed"
                fetch_results.append(item)
                continue

            stats["pdf_downloaded"] += 1

            # Convert to text
            text = pdf_to_text(tmp_path)
            if not text:
                stats["errors"] += 1
                item["fetch_status"] = "conversion_failed"
                fetch_results.append(item)
                continue

            stats["pdf_converted"] += 1
            word_count = len(text.split())
            print(f"    Extracted: {word_count:,} words")

            # Save full text
            text_path = TEXTS_DIR / f"PAP-{key}.md"
            header = f"""---
# Full text fetched via multi-source cascade
# Source: {source}
# DOI: {doi}
# Fetched: {datetime.now().strftime('%Y-%m-%d %H:%M')}
# Word count: {word_count}
---

"""
            text_path.write_text(header + text, encoding="utf-8")
            print(f"    Saved: {text_path}")

            # Determine content level
            if word_count >= MIN_WORDS_ARTICLE:
                new_level = "L3"
                stats["l3_upgraded"] += 1
            elif word_count >= MIN_WORDS_SHORT:
                new_level = "L3"  # Short paper
                stats["l3_upgraded"] += 1
            else:
                new_level = "L2"  # Partial text

            # Update paper YAML if it exists
            yaml_path = find_paper_yaml(doi, key)
            if yaml_path:
                update_paper_yaml(yaml_path, text_path, new_level, source, word_count)

            item["fetch_status"] = "success"
            item["word_count"] = word_count
            item["content_level"] = new_level
            fetch_results.append(item)

        finally:
            # Clean up temp file
            if tmp_path.exists():
                tmp_path.unlink()

        time.sleep(REQUEST_DELAY)

    return fetch_results


def update_paper_yaml(yaml_path: Path, text_path: Path, level: str,
                      source: str, word_count: int):
    """Update paper YAML with full text info."""
    try:
        with open(yaml_path, "r") as f:
            data = yaml.safe_load(f) or {}

        # Update content level
        data["content_level"] = level

        # Update full_text section
        data["full_text"] = {
            "available": True,
            "path": str(text_path),
            "format": "markdown",
            "source": source,
            "word_count": word_count,
            "archived_date": datetime.now().strftime("%Y-%m-%d"),
        }

        with open(yaml_path, "w") as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True,
                      sort_keys=False, width=120)

        print(f"    Updated YAML: {yaml_path.name} → {level}")

    except Exception as e:
        print(f"    YAML update error: {e}")


# ---------------------------------------------------------------------------
# Log
# ---------------------------------------------------------------------------
def write_log(scan_results: list, fetch_results: list):
    """Write summary log."""
    log = {
        "run_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "mode": "multisource",
        "stats": stats,
        "source_cascade": SOURCES,
        "scan_summary": {
            "total": len(scan_results),
            "found": sum(1 for r in scan_results if r.get("status") == "found"),
            "not_found": sum(1 for r in scan_results if r.get("status") == "not_found"),
            "already_have": sum(1 for r in scan_results if r.get("status") == "already_have_fulltext"),
        },
        "fetch_summary": {
            "total": len(fetch_results),
            "success": sum(1 for r in fetch_results if r.get("fetch_status") == "success"),
            "failed": sum(1 for r in fetch_results
                          if r.get("fetch_status") in ("download_failed", "conversion_failed")),
        },
        "found_items": [
            {
                "key": r["key"],
                "doi": r["doi"],
                "title": r.get("title", ""),
                "source": r.get("source", ""),
                "pdf_url": r.get("pdf_url", ""),
                "word_count": r.get("word_count", 0),
                "content_level": r.get("content_level", ""),
                "fetch_status": r.get("fetch_status", "scan_only"),
            }
            for r in scan_results if r.get("status") == "found"
        ],
    }

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "w") as f:
        yaml.dump(log, f, default_flow_style=False, allow_unicode=True,
                  sort_keys=False, width=120)

    print(f"\n  Log written: {LOG_FILE}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Multi-Source Full-Text PDF Fetcher"
    )
    parser.add_argument("--scan", action="store_true",
                        help="Scan sources for PDF availability")
    parser.add_argument("--fetch", action="store_true",
                        help="Download found PDFs and convert to text")
    parser.add_argument("--author", type=str, default="",
                        help="Filter by author name in bibtex")
    parser.add_argument("--batch", type=int, default=50,
                        help="Max papers to process")
    parser.add_argument("--dry-run", action="store_true",
                        help="Scan only, no downloads")
    parser.add_argument("--dois", type=str, default="",
                        help="Comma-separated DOIs to search")
    parser.add_argument("--bib", type=str, default=str(BIB_FILE),
                        help="Path to BibTeX file")

    args = parser.parse_args()

    if not args.scan and not args.fetch:
        args.scan = True
        args.fetch = True

    print("╔" + "═" * 58 + "╗")
    print("║  MULTI-SOURCE FULL-TEXT FETCHER                          ║")
    print("║  Sources: Unpaywall → OpenAlex → EconStor → S2          ║")
    print("╚" + "═" * 58 + "╝")

    # Get DOIs to search
    if args.dois:
        # Sanitize each DOI (strip quotes, whitespace, URL prefixes)
        raw_dois = args.dois.strip().strip("'\"")
        entries = [{"key": f"manual-{i}", "doi": sanitize_doi(d), "title": ""}
                   for i, d in enumerate(raw_dois.split(","), 1)]
        # Filter out empty DOIs
        entries = [e for e in entries if e["doi"]]
    else:
        bib_path = Path(args.bib)
        if not bib_path.exists():
            print(f"  Error: BibTeX file not found: {bib_path}")
            sys.exit(1)
        entries = extract_dois_from_bibtex(bib_path, args.author)

    if not entries:
        print("  No entries to process.")
        sys.exit(0)

    stats["total_dois"] = len(entries)

    # Limit to batch size
    entries = entries[:args.batch]
    print(f"  Processing {len(entries)} entries (batch={args.batch})")

    # Phase 1: Scan
    scan_results = []
    if args.scan:
        scan_results = run_scan(entries, dry_run=args.dry_run)

    # Phase 2: Fetch
    fetch_results = []
    if args.fetch and not args.dry_run:
        fetch_results = run_fetch(scan_results, batch_size=args.batch,
                                  dry_run=args.dry_run)

    # Write log
    write_log(scan_results, fetch_results)

    # Print summary
    print(f"\n{'=' * 60}")
    print("SUMMARY")
    print(f"{'=' * 60}")
    print(f"  Papers scanned:      {stats['scanned']}")
    print(f"  Already have text:   {stats['already_have_fulltext']}")
    print(f"  PDF found:           {stats['pdf_found']}")
    print(f"  PDF downloaded:      {stats['pdf_downloaded']}")
    print(f"  Text converted:      {stats['pdf_converted']}")
    print(f"  L3 upgraded:         {stats['l3_upgraded']}")
    print(f"  Errors:              {stats['errors']}")
    print(f"\n  Source effectiveness:")
    for s in SOURCES:
        hits = stats['source_hits'][s]
        misses = stats['source_misses'][s]
        total = hits + misses
        rate = f"{hits/total:.0%}" if total > 0 else "n/a"
        print(f"    {s:20s}: {hits:>3} hits / {total:>3} tried ({rate})")

    return 0


if __name__ == "__main__":
    sys.exit(main())
