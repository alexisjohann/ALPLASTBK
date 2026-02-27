#!/usr/bin/env python3
"""
Researcher Paper Scraper — Downloads PDFs from researcher publication pages.

PRIMARY SOURCE: data/researcher-registry.yaml
  - Full researchers (researchers[].scraping.paper_urls)
  - Scraping targets (scraping_targets[].paper_urls)

FALLBACK: data/researcher-scraper-config.json (legacy, will be removed)

Downloads new PDFs to data/researcher-papers/<Lastname_Firstname>/.
Skips already downloaded files.

Usage:
    python scripts/scrape_researcher_papers.py
    python scripts/scrape_researcher_papers.py --dry-run
    python scripts/scrape_researcher_papers.py --only Fehr_Ernst

Environment variables (for GitHub Actions):
    ONLY_RESEARCHER  — Only scrape this folder (e.g. "Fehr_Ernst")
    DRY_RUN          — "true" to only list PDFs without downloading
"""

import json
import os
import re
import sys
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote

try:
    import yaml
except ImportError:
    yaml = None

import requests
from bs4 import BeautifulSoup

REGISTRY_PATH = Path("data/researcher-registry.yaml")
LEGACY_CONFIG_PATH = Path("data/researcher-scraper-config.json")
OUTPUT_DIR = Path("data/researcher-papers")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; EBF-ResearchScraper/3.0)"
}

MIN_SIZE_KB = 10  # Skip files smaller than this (likely error pages)


def load_targets_from_registry():
    """Load scraping targets from researcher-registry.yaml (SSOT)."""
    if not REGISTRY_PATH.exists():
        print("  WARNING: researcher-registry.yaml not found")
        return []

    if yaml is None:
        print("  WARNING: PyYAML not installed, cannot read registry")
        return []

    with open(REGISTRY_PATH) as f:
        data = yaml.safe_load(f)

    targets = []

    # 1. Full researchers with scraping.paper_urls
    for r in data.get("researchers", []):
        scraping = r.get("scraping", {})
        if not scraping.get("enabled", False):
            continue

        paper_urls = scraping.get("paper_urls", [])
        if not paper_urls:
            continue

        name = r.get("basic_info", {}).get("full_name", "")
        rid = r.get("id", "")

        # Generate folder name: "Fehr_Ernst" from "Ernst Fehr"
        parts = name.split()
        if len(parts) >= 2:
            folder = f"{parts[-1]}_{parts[0]}"
        else:
            folder = name.replace(" ", "_")

        for pu in paper_urls:
            targets.append({
                "name": name,
                "url": pu["url"],
                "folder": folder,
                "registry_id": rid,
                "url_type": pu.get("type", "unknown"),
            })

    # 2. Scraping targets (lightweight entries)
    for st in data.get("scraping_targets", []):
        paper_urls = st.get("paper_urls", [])
        if not paper_urls:
            continue

        name = st.get("name", "")
        rid = st.get("id", "")

        # Generate folder name
        parts = name.split()
        if len(parts) >= 2:
            # Handle "Richard H. Thaler" → "Thaler_Richard"
            first = parts[0]
            last = parts[-1]
            folder = f"{last}_{first}"
        else:
            folder = name.replace(" ", "_")

        for pu in paper_urls:
            targets.append({
                "name": name,
                "url": pu["url"],
                "folder": folder,
                "registry_id": rid,
                "url_type": pu.get("type", "unknown"),
            })

    return targets


def load_targets_from_json():
    """Load from legacy JSON config (fallback)."""
    if not LEGACY_CONFIG_PATH.exists():
        return []

    with open(LEGACY_CONFIG_PATH) as f:
        config = json.load(f)

    targets = []
    for r in config.get("researchers", []):
        targets.append({
            "name": r["name"],
            "url": r["url"],
            "folder": r["folder"],
            "registry_id": r.get("registry_id", ""),
            "url_type": "legacy",
        })

    return targets


def load_all_targets():
    """Load targets from registry (primary) + JSON (fallback). Deduplicate."""
    registry_targets = load_targets_from_registry()
    json_targets = load_targets_from_json()

    # Use registry as primary, add JSON entries only if not already covered
    seen_urls = {t["url"] for t in registry_targets}
    seen_folders = {t["folder"] for t in registry_targets}

    for jt in json_targets:
        if jt["url"] not in seen_urls and jt["folder"] not in seen_folders:
            jt["url_type"] = "legacy_json"
            registry_targets.append(jt)

    return registry_targets


def find_pdf_links(url):
    """Fetch a page and extract all PDF links."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30, allow_redirects=True)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"  ERROR fetching {url}: {e}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    links = []
    seen = set()

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if not href.lower().endswith(".pdf") and ".pdf" not in href.lower():
            continue

        full_url = urljoin(url, href)

        if full_url in seen:
            continue
        seen.add(full_url)

        # Extract filename from URL
        path = urlparse(full_url).path
        filename = unquote(path.split("/")[-1].split("?")[0])
        if not filename.lower().endswith(".pdf"):
            filename += ".pdf"

        # Clean filename
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)

        links.append({"url": full_url, "filename": filename})

    return links


def download_pdf(url, dest_path):
    """Download a PDF file. Returns True if successful."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=60, stream=True)
        resp.raise_for_status()

        content = resp.content
        size_kb = len(content) / 1024

        if size_kb < MIN_SIZE_KB:
            print(f"  SKIP (too small, {size_kb:.0f} KB): {dest_path.name}")
            return False

        dest_path.write_bytes(content)
        print(f"  OK: {dest_path.name} ({size_kb:.0f} KB)")
        return True

    except requests.RequestException as e:
        print(f"  ERROR downloading {url}: {e}")
        return False


def scrape_url(target, dry_run=False):
    """Scrape one URL for PDF links."""
    name = target["name"]
    url = target["url"]
    folder = target["folder"]
    url_type = target.get("url_type", "unknown")

    print(f"\n  {name} [{url_type}]")
    print(f"  {url}")

    pdf_links = find_pdf_links(url)
    print(f"  Found: {len(pdf_links)} PDF links")

    if not pdf_links:
        return 0

    # Output directory
    out_dir = OUTPUT_DIR / folder
    out_dir.mkdir(parents=True, exist_ok=True)

    # Check existing files
    existing = {f.name for f in out_dir.iterdir() if f.is_file()}

    new_count = 0
    skipped = 0

    for link in pdf_links:
        if link["filename"] in existing:
            skipped += 1
            continue

        if dry_run:
            print(f"  [DRY RUN] Would download: {link['filename']}")
            new_count += 1
            continue

        dest = out_dir / link["filename"]
        if download_pdf(link["url"], dest):
            new_count += 1
            time.sleep(2)  # Be polite

    if new_count > 0 or skipped > 0:
        print(f"  → New: {new_count}, Already had: {skipped}")

    return new_count


def main():
    only = os.environ.get("ONLY_RESEARCHER", "").strip()
    dry_run = os.environ.get("DRY_RUN", "false").lower() == "true"

    # CLI args override env vars
    if "--dry-run" in sys.argv:
        dry_run = True
    for arg in sys.argv[1:]:
        if arg.startswith("--only"):
            idx = sys.argv.index(arg)
            if idx + 1 < len(sys.argv):
                only = sys.argv[idx + 1]

    targets = load_all_targets()

    if only:
        targets = [t for t in targets if t["folder"] == only]
        if not targets:
            print(f"ERROR: No researcher with folder '{only}' found.")
            sys.exit(1)

    # Group by researcher (folder)
    by_folder = {}
    for t in targets:
        by_folder.setdefault(t["folder"], []).append(t)

    print(f"Researcher Paper Scraper v3.0")
    print(f"Source: researcher-registry.yaml (SSOT)")
    print(f"Researchers: {len(by_folder)}")
    print(f"URLs to scrape: {len(targets)}")
    if dry_run:
        print(f"MODE: DRY RUN (no downloads)")

    total_new = 0
    errors = 0

    for folder, folder_targets in sorted(by_folder.items()):
        name = folder_targets[0]["name"]
        rid = folder_targets[0].get("registry_id", "")
        print(f"\n{'=' * 60}")
        print(f"  {name} ({rid})")
        print(f"  → {folder}/  ({len(folder_targets)} URLs)")
        print(f"{'=' * 60}")

        for t in folder_targets:
            try:
                total_new += scrape_url(t, dry_run=dry_run)
            except Exception as e:
                print(f"  ERROR with {t['url']}: {e}")
                errors += 1

    print(f"\n{'=' * 60}")
    print(f"  TOTAL: {total_new} new papers, {errors} errors")
    print(f"  Researchers: {len(by_folder)}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
