#!/usr/bin/env python3
"""
Fetch Full Texts from MPG PuRe (Max Planck Publication Repository)
===================================================================
Downloads PDFs from MPG PuRe items and converts to text for L3 upgrade.

MPG PuRe often hosts author-uploaded PDFs that are freely downloadable,
unlike publisher sites (Wiley, OUP, etc.) which return HTTP 403.

URL Pattern:
    https://pure.mpg.de/rest/items/{item_id}/component/{file_id}/content

Usage:
    python scripts/fetch_mpg_fulltext.py --person-id persons206813 --name sutter
    python scripts/fetch_mpg_fulltext.py --batch 20 --dry-run
    python scripts/fetch_mpg_fulltext.py --name sutter --batch 50

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
PURE_BASE = "https://pure.mpg.de/rest"
PAPERS_DIR = Path("data/paper-references")
TEXTS_DIR = Path("data/paper-texts")
USER_AGENT = "EBF-Framework/1.0 (mailto:research@fehradvice.com)"
REQUEST_DELAY = 0.5  # seconds between API calls

# L3 requirements
MIN_WORDS_SHORT = 5000

# Stats
stats = {
    "pure_items_found": 0,
    "items_with_files": 0,
    "matched_to_l2": 0,
    "pdfs_downloaded": 0,
    "l3_upgraded": 0,
    "l2_partial": 0,
    "errors": 0,
    "skipped_already_l3": 0,
    "skipped_no_match": 0,
}

paper_results = []


# ---------------------------------------------------------------------------
# MPG PuRe API
# ---------------------------------------------------------------------------
def search_pure_by_person(person_id: str, size: int = 100, author_name: str = "") -> list:
    """Search PuRe by person identifier (e.g., persons206813).

    Uses multiple query strategies:
    1. Person ID match (ElasticSearch term query)
    2. Creator name match (if author_name provided)
    3. Offset-based pagination for all results
    """
    url = f"{PURE_BASE}/items/search"

    if not person_id.startswith("/"):
        person_id_full = f"/persons/resource/{person_id}"
    else:
        person_id_full = person_id

    # Strategy 1: Person ID variants (covers different PuRe formats)
    id_variants = [person_id_full, person_id, person_id.replace("persons", "")]

    # Build multi-strategy query
    should_clauses = [
        {"term": {"metadata.creators.person.identifier.id": {"value": v}}}
        for v in id_variants
    ]
    # Add nested identifier match
    should_clauses.append(
        {"match": {"metadata.creators.person.identifier.id": person_id}}
    )
    # Strategy 2: Author name match (broader)
    if author_name:
        should_clauses.append(
            {"match_phrase": {"metadata.creators.person.familyName": author_name.capitalize()}}
        )
        should_clauses.append(
            {"match": {"metadata.creators.value": author_name.capitalize()}}
        )

    query = {
        "query": {
            "bool": {
                "should": should_clauses,
                "minimum_should_match": 1
            }
        }
    }

    print(f"  Querying PuRe for person: {person_id}")
    if author_name:
        print(f"  Also searching by name: {author_name}")
    print(f"  Query clauses: {len(should_clauses)}")

    all_records = []
    offset = 0
    total_reported = 0

    while True:
        params = {"format": "json", "size": size, "offset": offset}
        resp = requests.post(url, json=query, params=params)

        if resp.status_code != 200:
            print(f"  API returned {resp.status_code}: {resp.text[:200]}")
            break

        data = resp.json()

        if isinstance(data, dict):
            records = data.get("records", data.get("list", []))
            total_reported = data.get("numberOfRecords", data.get("total", 0))
        elif isinstance(data, list):
            records = data
            total_reported = len(records) if offset == 0 else total_reported
        else:
            break

        if not records:
            break

        all_records.extend(records)
        offset = len(all_records)
        print(f"  Fetched {offset}/{total_reported} PuRe items...")

        if offset >= total_reported:
            break

        time.sleep(REQUEST_DELAY)

    print(f"  Total: {len(all_records)} items (API reported: {total_reported})")
    return all_records


def search_pure_by_doi(doi: str) -> list:
    """Search PuRe by DOI identifier with post-filter for exact match.

    Uses both term and match queries to maximize recall (PuRe's identifier
    field may be analyzed text), then POST-FILTERS to verify the returned
    item's actual DOI matches exactly. This eliminates false positives from
    fuzzy ElasticSearch matching while still finding true matches.

    Returns list of verified matching records (usually 0 or 1).
    """
    url = f"{PURE_BASE}/items/search"
    doi_clean = doi.strip().lower()

    # Use both term (for keyword fields) and match (for analyzed text fields).
    # The match clause causes fuzzy results, but the post-filter below
    # verifies exact DOI match, eliminating false positives.
    query = {
        "query": {
            "bool": {
                "should": [
                    {"term": {"metadata.identifiers.id": {"value": doi}}},
                    {"term": {"metadata.identifiers.id": {"value": doi_clean}}},
                    {"match_phrase": {"metadata.identifiers.id": doi}},
                ],
                "minimum_should_match": 1,
            }
        }
    }
    try:
        resp = requests.post(url, json=query, params={"format": "json", "size": 20}, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            if isinstance(data, dict):
                records = data.get("records", data.get("list", []))
            elif isinstance(data, list):
                records = data
            else:
                return []

            # POST-FILTER: verify that returned item actually has this exact DOI.
            # This is critical because match/match_phrase queries on analyzed fields
            # can return items with similar but different DOIs (e.g., same publisher prefix).
            verified = []
            for rec in records:
                dn = rec.get("data", rec) if isinstance(rec, dict) else rec
                if not isinstance(dn, dict):
                    continue
                meta = dn.get("metadata", {})
                item_dois = set()
                for ident in (meta.get("identifiers", []) or []):
                    if isinstance(ident, dict) and ident.get("type") == "DOI":
                        item_dois.add((ident.get("id", "") or "").strip().lower())
                if doi_clean in item_dois:
                    verified.append(rec)
            return verified
    except Exception as e:
        print(f"    DOI search error for {doi}: {e}")
    return []


def search_pure_by_title(title: str, author_hint: str = "", diag: dict | None = None) -> list:
    """Search PuRe by title with optional author hint.

    Used as fallback when DOI search fails (Strategy 4). Many papers are on
    PuRe but without DOI in metadata, making DOI search miss them.

    Returns list of matching records (post-filtered by title similarity).
    If diag dict is provided, accumulates diagnostic counters into it.
    """
    url = f"{PURE_BASE}/items/search"

    # Clean title for search: remove special chars, lowercase
    clean = re.sub(r'[^\w\s]', ' ', title.lower()).strip()
    words = clean.split()
    if len(words) < 3:
        if diag is not None:
            diag["too_short"] = diag.get("too_short", 0) + 1
        return []

    # Use first ~8 significant words for query (avoid stopwords)
    stopwords = {'the', 'a', 'an', 'of', 'in', 'on', 'for', 'and', 'to', 'by', 'with', 'from', 'is', 'are', 'at'}
    sig_words = [w for w in words if w not in stopwords and len(w) > 2][:8]
    search_phrase = " ".join(sig_words)

    must_clauses = [
        {"match": {"metadata.title": {"query": search_phrase, "minimum_should_match": "60%"}}}
    ]
    # Author hint as 'should' (boost, not requirement) — PuRe's
    # metadata.creators.value format varies and a 'must' match kills
    # 97%+ of results. The post-filter on title similarity is sufficient.
    should_clauses = []
    if author_hint:
        should_clauses.append(
            {"match": {"metadata.creators.value": {"query": author_hint, "boost": 2}}}
        )

    query = {
        "query": {
            "bool": {
                "must": must_clauses,
                "should": should_clauses,
            }
        }
    }
    try:
        resp = requests.post(url, json=query, params={"format": "json", "size": 10}, timeout=30)
        if resp.status_code != 200:
            if diag is not None:
                diag["non_200"] = diag.get("non_200", 0) + 1
                if diag.get("non_200") <= 3:
                    diag.setdefault("non_200_samples", []).append(
                        {"status": resp.status_code, "body": resp.text[:200]})
            return []

        data = resp.json()
        if isinstance(data, dict):
            records = data.get("records", data.get("list", []))
        elif isinstance(data, list):
            records = data
        else:
            if diag is not None:
                diag["bad_response_type"] = diag.get("bad_response_type", 0) + 1
            return []

        if not records:
            if diag is not None:
                diag["empty_records"] = diag.get("empty_records", 0) + 1
            return []

        # Post-filter: title must be similar (>60% word overlap)
        verified = []
        title_words = set(sig_words)
        for rec in records:
            dn = rec.get("data", rec) if isinstance(rec, dict) else rec
            if not isinstance(dn, dict):
                continue
            meta = dn.get("metadata", {})
            rec_title = (meta.get("title", "") or "").lower()
            rec_clean = re.sub(r'[^\w\s]', ' ', rec_title)
            rec_words = set(w for w in rec_clean.split() if w not in stopwords and len(w) > 2)

            if not rec_words:
                continue
            overlap = len(title_words & rec_words) / max(len(title_words), 1)
            if overlap >= 0.5:
                verified.append(rec)

        if records and not verified:
            if diag is not None:
                diag["filtered_out"] = diag.get("filtered_out", 0) + 1
                if diag.get("filtered_out") <= 2:
                    # Log sample: what title was searched vs what was returned
                    sample_titles = []
                    for r in records[:3]:
                        dn2 = r.get("data", r) if isinstance(r, dict) else r
                        if isinstance(dn2, dict):
                            sample_titles.append(
                                (dn2.get("metadata", {}).get("title", "?"))[:80])
                    diag.setdefault("filtered_out_samples", []).append({
                        "searched": search_phrase[:60],
                        "returned_titles": sample_titles,
                        "records_count": len(records),
                    })
        elif verified:
            if diag is not None:
                diag["with_results"] = diag.get("with_results", 0) + 1

        return verified
    except Exception as e:
        if diag is not None:
            diag["exceptions"] = diag.get("exceptions", 0) + 1
            if diag.get("exceptions") <= 3:
                diag.setdefault("exception_samples", []).append(str(e)[:200])
        print(f"    Title search error: {e}")
    return []


def get_item_with_files(object_id: str) -> dict | None:
    """Fetch full item details from PuRe REST API.

    The search API returns stale file IDs. We need to GET the actual item
    to get the current file components with valid IDs.

    Returns the full item data_node or None on failure.
    """
    url = f"{PURE_BASE}/items/{object_id}"
    try:
        resp = requests.get(url, params={"format": "json"}, timeout=30)
        if resp.status_code == 200:
            return resp.json()
        # If versioned ID fails, try without version suffix
        # e.g., item_2463938_1 → item_2463938
        if "_" in object_id:
            base_id = object_id.rsplit("_", 1)[0]
            resp2 = requests.get(
                f"{PURE_BASE}/items/{base_id}",
                params={"format": "json"},
                timeout=30,
            )
            if resp2.status_code == 200:
                return resp2.json()
        print(f"    GET item failed: HTTP {resp.status_code}")
    except Exception as e:
        print(f"    GET item error: {e}")
    return None


def extract_files_from_item(data_node: dict, object_id: str) -> list:
    """Extract file components with download URLs from a PuRe item data node.

    Storage types:
    - INTERNAL_MANAGED: Actual PDF stored in PuRe → use REST API download
    - EXTERNAL_URL: Just a link (DOI, publisher) → follow the external URL
    - EXTERNAL_SERVICE: External service reference → skip

    For INTERNAL_MANAGED:
        1. Pubman portal: /pubman/item/{objectId}/component/{fileId}/{filename}
        2. REST API: /items/{objectId}/component/{fileId}/content

    For EXTERNAL_URL:
        1. The content/name field contains the external URL (e.g., DOI link)
    """
    # Get the correct objectId and version from the actual item data
    actual_object_id = data_node.get("objectId", object_id)
    version = data_node.get("versionNumber", "")
    if version:
        item_version_id = f"{actual_object_id}_{version}"
    else:
        item_version_id = actual_object_id

    files = data_node.get("files", []) or []
    file_components = []
    for f in (files if isinstance(files, list) else []):
        file_id = f.get("objectId", "")
        visibility = f.get("visibility", "")
        content_type = f.get("mimeType", f.get("content-type", ""))
        name = f.get("name", "")
        if not name and isinstance(f.get("metadata"), dict):
            name = f["metadata"].get("title", "")
        storage = f.get("storage", "")
        content_ref = f.get("content", "")
        size = f.get("size", 0)

        if not file_id:
            continue

        urls = []

        if storage == "INTERNAL_MANAGED":
            # Actual file stored in PuRe — use REST API
            if name and not name.startswith("http"):
                urls.append(f"https://pure.mpg.de/pubman/item/{item_version_id}/component/{file_id}/{name}")
            urls.append(f"{PURE_BASE}/items/{item_version_id}/component/{file_id}/content")
            base_obj = actual_object_id
            if base_obj != item_version_id:
                urls.append(f"{PURE_BASE}/items/{base_obj}/component/{file_id}/content")

        elif storage == "EXTERNAL_URL":
            # External URL reference — the "content" or "name" IS the URL
            external_url = content_ref or name or ""
            if external_url and external_url.startswith("http"):
                urls.append(external_url)
            # Also try DOI redirect if it looks like a DOI URL
            if "doi.org" in external_url:
                # DOI URLs redirect to publisher — might get PDF
                urls.append(external_url)

        else:
            # Unknown storage type — try REST API as fallback
            urls.append(f"{PURE_BASE}/items/{item_version_id}/component/{file_id}/content")

        if urls:
            # Deduplicate while preserving order
            seen = set()
            unique_urls = []
            for u in urls:
                if u not in seen:
                    seen.add(u)
                    unique_urls.append(u)

            file_components.append({
                "file_id": file_id,
                "visibility": visibility,
                "content_type": content_type,
                "name": name,
                "storage": storage,
                "content_ref": content_ref,
                "size": size,
                "item_version_id": item_version_id,
                "download_urls": unique_urls,
            })
    return file_components


def extract_item_info(record: dict) -> dict:
    """Extract item metadata from PuRe search record.

    PuRe REST API structure:
        record['data']['objectId']     → item ID
        record['data']['metadata']     → paper metadata (title, identifiers, dates)
        record['data']['files']        → file components (PDFs) — may be STALE!
    """
    # Navigate the nested structure: record > data > metadata
    data_node = record.get("data", record)
    meta = data_node.get("metadata", data_node)

    # Item ID and version
    object_id = data_node.get("objectId", "")
    version = data_node.get("versionNumber", "")
    if not version:
        lv = data_node.get("latestVersion", {})
        version = lv.get("versionNumber", "") if isinstance(lv, dict) else ""
    item_version_id = f"{object_id}_{version}" if version else object_id

    # Title — metadata can have nested title
    title = ""
    if isinstance(meta, dict):
        title = meta.get("title", "")

    # DOI — look in metadata.identifiers
    identifiers = []
    if isinstance(meta, dict):
        identifiers = meta.get("identifiers", []) or []
    doi = ""
    for ident in (identifiers if isinstance(identifiers, list) else []):
        if isinstance(ident, dict) and ident.get("type") == "DOI":
            doi = ident.get("id", "")

    # Year
    year = ""
    if isinstance(meta, dict):
        year = str(
            meta.get("datePublishedInPrint", "")
            or meta.get("datePublishedOnline", "")
            or meta.get("dateCreated", "")
        )[:4]

    # File components from SEARCH results (may be stale!)
    # These are used for initial filtering only.
    # For actual downloads, we re-fetch via get_item_with_files().
    files = data_node.get("files", []) or []
    has_files = bool(files)

    return {
        "item_id": item_version_id,
        "object_id": object_id,
        "title": title,
        "doi": doi.lower().strip() if doi else "",
        "year": year,
        "has_files": has_files,
        "search_file_count": len(files) if isinstance(files, list) else 0,
        # Keep search-level file info for diagnostics only
        "_search_files": files if isinstance(files, list) else [],
    }


# ---------------------------------------------------------------------------
# PDF Download & Text Extraction (shared with fetch_fulltext_oa.py)
# ---------------------------------------------------------------------------
def download_pdf(url: str, output_path: str) -> tuple[bool, str]:
    """Download a PDF file. Returns (success, detail_msg).

    Handles:
    - Direct PDF links (Content-Type: application/pdf)
    - Octet-stream that might be PDF (checks magic bytes)
    - DOI redirects (doi.org → publisher → PDF or HTML)
    - HTML responses (publisher landing pages, not PDFs)
    """
    try:
        resp = requests.get(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "application/pdf,application/octet-stream,*/*",
            },
            timeout=60,
            allow_redirects=True,
        )
        content_type = resp.headers.get("content-type", "unknown")
        final_url = resp.url  # after redirects

        if resp.status_code == 200 and len(resp.content) > 1000:
            # Check for actual PDF content (magic bytes)
            is_pdf = resp.content[:5] == b"%PDF-" or b"%PDF-" in resp.content[:100]

            if is_pdf:
                with open(output_path, "wb") as f:
                    f.write(resp.content)
                return True, f"OK ({len(resp.content)} bytes, from {final_url[:80]})"
            elif "octet-stream" in content_type and len(resp.content) > 10000:
                # Large octet-stream might still be a PDF
                with open(output_path, "wb") as f:
                    f.write(resp.content)
                return True, f"OK-octet ({len(resp.content)} bytes, type={content_type})"
            elif "html" in content_type.lower():
                return False, f"HTML page (not PDF), redirected to {final_url[:80]}"
            else:
                return False, f"Not a PDF (content-type={content_type}, size={len(resp.content)}, first bytes={resp.content[:20]})"
        elif resp.status_code == 200:
            return False, f"Too small ({len(resp.content)} bytes, type={content_type})"
        else:
            # Capture error response body for debugging
            body_preview = ""
            try:
                body_preview = resp.text[:300]
            except Exception:
                body_preview = str(resp.content[:300])
            return False, f"HTTP {resp.status_code}, size={len(resp.content)}, type={content_type}, body={body_preview}"
    except Exception as e:
        return False, f"Exception: {e}"


def extract_text_from_pdf(pdf_path: str) -> str | None:
    """Extract text from PDF using pdftotext."""
    try:
        result = subprocess.run(
            ["pdftotext", "-layout", "-enc", "UTF-8", pdf_path, "-"],
            capture_output=True,
            text=True,
            timeout=120,
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


def cleanup_text(text: str) -> str:
    """Clean up extracted text."""
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
    return len(text.split())


def has_references_section(text: str) -> bool:
    patterns = [r"\bReferences\b", r"\bBibliography\b", r"\bLiterature\b",
                r"\bWorks Cited\b", r"\bREFERENCES\b"]
    return any(re.search(p, text) for p in patterns)


def validate_l3(text: str) -> tuple[bool, str, dict]:
    word_count = count_words(text)
    has_refs = has_references_section(text)
    details = {
        "word_count": word_count,
        "has_references": has_refs,
        "r3_length": word_count >= MIN_WORDS_SHORT,
    }
    if word_count >= MIN_WORDS_SHORT and has_refs:
        return True, "L3", details
    elif word_count >= 2000:
        return False, f"L2+ ({word_count} words, refs={'yes' if has_refs else 'no'})", details
    else:
        return False, f"Too short ({word_count} words)", details


# ---------------------------------------------------------------------------
# Paper Database
# ---------------------------------------------------------------------------
def normalize_title(title: str) -> str:
    """Normalize title for fuzzy matching."""
    t = title.lower().strip()
    # Remove common punctuation
    t = re.sub(r'[^\w\s]', ' ', t)
    # Collapse whitespace
    t = re.sub(r'\s+', ' ', t).strip()
    return t


def load_bibtex_titles(bib_path: str = "bibliography/bcm_master.bib",
                       author_filter: str | None = None) -> dict[str, str]:
    """Load BibTeX titles as bibtex_key → title mapping.

    Simple parser — extracts key and title from BibTeX entries.
    """
    titles = {}
    current_key = None
    current_title = None
    in_title = False

    try:
        with open(bib_path, encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                # Detect entry start: @article{sutter2013impatience,
                if line.startswith("@") and "{" in line:
                    key_part = line.split("{", 1)[1].rstrip(",").strip()
                    if author_filter and not key_part.startswith(author_filter):
                        current_key = None
                        continue
                    current_key = key_part
                    current_title = None
                    in_title = False
                elif current_key and re.match(r'title\s*=', line.lower()):
                    # title={Some Title Here}, or title = {Some Title},
                    title_raw = line.split("=", 1)[1].strip()
                    # Remove braces and trailing comma
                    title_raw = title_raw.strip(",").strip()
                    if title_raw.startswith("{") and title_raw.endswith("}"):
                        title_raw = title_raw[1:-1]
                    # Clean LaTeX
                    title_raw = re.sub(r'[{}\\"]', '', title_raw)
                    title_raw = title_raw.strip()
                    if title_raw:
                        titles[current_key] = title_raw
    except FileNotFoundError:
        print(f"  WARNING: BibTeX file not found: {bib_path}")
    return titles


def _extract_dois_from_bibtex(bib_path: str = "bibliography/bcm_master.bib",
                              author_filter: str | None = None) -> set[str]:
    """Extract DOIs from BibTeX entries for a given author.

    This catches papers that have DOIs in BibTeX but no YAML file yet,
    or YAML files at L0/L1 without DOI fields populated.
    """
    dois = set()
    current_key = None
    current_doi = None
    in_entry = False

    try:
        with open(bib_path, encoding="utf-8", errors="replace") as f:
            for line in f:
                stripped = line.strip()
                # Entry start
                if stripped.startswith("@") and "{" in stripped:
                    key_part = stripped.split("{", 1)[1].rstrip(",").strip()
                    if author_filter and not key_part.startswith(author_filter):
                        current_key = None
                        in_entry = False
                        continue
                    current_key = key_part
                    current_doi = None
                    in_entry = True
                elif in_entry and current_key and re.match(r'doi\s*=', stripped.lower()):
                    doi_raw = stripped.split("=", 1)[1].strip()
                    doi_raw = doi_raw.strip(",").strip().strip("{}")
                    doi_raw = doi_raw.strip('"').strip()
                    if doi_raw:
                        dois.add(doi_raw.lower())
    except FileNotFoundError:
        pass
    return dois


def _build_doi_title_map(bib_path: str = "bibliography/bcm_master.bib",
                         author_filter: str | None = None) -> dict[str, str]:
    """Build DOI → title mapping from BibTeX for ALL entries matching author_filter.

    Unlike load_bibtex_titles (which returns bibtex_key → title), this returns
    doi → title. This is critical for Strategy 4 which needs titles for DOIs
    that had no PuRe hit.

    Also loads titles from YAML files (data/paper-references/) since many
    BibTeX entries have truncated titles.
    """
    doi_to_title = {}
    current_key = None
    current_title = None
    current_doi = None
    in_entry = False

    try:
        with open(bib_path, encoding="utf-8", errors="replace") as f:
            for line in f:
                stripped = line.strip()
                if stripped.startswith("@") and "{" in stripped:
                    # Save previous entry
                    if in_entry and current_doi and current_title:
                        doi_to_title[current_doi] = current_title
                    # Start new entry
                    key_part = stripped.split("{", 1)[1].rstrip(",").strip()
                    if author_filter and not key_part.startswith(author_filter):
                        current_key = None
                        in_entry = False
                        continue
                    current_key = key_part
                    current_title = None
                    current_doi = None
                    in_entry = True
                elif in_entry and current_key:
                    if re.match(r'title\s*=', stripped.lower()):
                        title_raw = stripped.split("=", 1)[1].strip()
                        title_raw = title_raw.strip(",").strip()
                        if title_raw.startswith("{") and title_raw.endswith("}"):
                            title_raw = title_raw[1:-1]
                        title_raw = re.sub(r'[{}\\"]', '', title_raw)
                        title_raw = title_raw.strip()
                        if title_raw:
                            current_title = title_raw
                    elif re.match(r'doi\s*=', stripped.lower()):
                        doi_raw = stripped.split("=", 1)[1].strip()
                        doi_raw = doi_raw.strip(",").strip().strip("{}")
                        doi_raw = doi_raw.strip('"').strip()
                        if doi_raw:
                            current_doi = doi_raw.lower()
            # Don't forget the last entry
            if in_entry and current_doi and current_title:
                doi_to_title[current_doi] = current_title
    except FileNotFoundError:
        pass

    # Also load titles from YAML files (often more complete than BibTeX)
    pattern = f"PAP-{author_filter}*.yaml" if author_filter else "PAP-*.yaml"
    for path in sorted(PAPERS_DIR.glob(pattern)):
        try:
            with open(path) as f:
                data = yaml.safe_load(f)
            if not data:
                continue
            doi = (data.get("doi") or "").strip().lower()
            title = data.get("title", "")
            if doi and title and len(title) > 10 and not title.startswith("["):
                # YAML title takes priority if it's a real title (not placeholder)
                doi_to_title[doi] = title
        except Exception:
            continue

    return doi_to_title


def get_l2_papers(author_filter: str | None = None) -> dict[str, dict]:
    """Get all L2 papers as DOI→(key, data, path) and title→(key, data, path) mapping.

    Returns a dict with both DOI keys and normalized title keys for matching.
    Loads titles from BOTH YAML metadata AND BibTeX file (bcm_master.bib).
    Also indexes BibTeX-only entries (no YAML) for title matching.
    """
    papers = {}  # doi → (key, data, path) AND title:... → (key, data, path)
    pattern = f"PAP-{author_filter}*.yaml" if author_filter else "PAP-*.yaml"

    # Load titles from BibTeX for enrichment
    bib_titles = load_bibtex_titles(author_filter=author_filter)
    print(f"  Loaded {len(bib_titles)} titles from BibTeX")

    yaml_keys = set()

    for path in sorted(PAPERS_DIR.glob(pattern)):
        with open(path) as f:
            data = yaml.safe_load(f)
        if not data:
            continue

        # Only papers that need upgrade (no full text yet, or L2)
        ft = data.get("full_text", {})
        cl = ft.get("content_level", "")
        if cl == "L3":
            continue  # already done

        # Already has substantial full text?
        if ft.get("available") and ft.get("word_count", 0) >= MIN_WORDS_SHORT:
            continue

        doi = (data.get("doi") or "").strip().lower()
        key = data.get("bibtex_key") or path.stem.replace("PAP-", "")
        yaml_keys.add(key)
        entry = (key, data, path)

        if doi:
            papers[doi] = entry

        # Title from YAML or from BibTeX
        title = data.get("title", "") or bib_titles.get(key, "")
        if title:
            papers[f"title:{normalize_title(title)}"] = entry

    # Also index BibTeX entries that DON'T have YAML files yet
    # These can be created on the fly when matched
    bib_only_count = 0
    for bib_key, title in bib_titles.items():
        if bib_key in yaml_keys:
            continue  # already indexed via YAML
        # Create a minimal entry — YAML will be created during processing
        data = {
            "bibtex_key": bib_key,
            "id": f"PAP-{bib_key}",
            "title": title,
            "_bib_only": True,  # Flag: no YAML file yet
        }
        path = PAPERS_DIR / f"PAP-{bib_key}.yaml"
        entry = (bib_key, data, path)
        norm = normalize_title(title)
        papers[f"title:{norm}"] = entry
        bib_only_count += 1

    print(f"  YAML papers indexed: {len(yaml_keys)} (upgradable)")
    print(f"  BibTeX-only papers indexed: {bib_only_count}")
    return papers


def save_paper_yaml(key: str, data: dict):
    path = PAPERS_DIR / f"PAP-{key}.yaml"
    with open(path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, width=120)


def save_fulltext(key: str, text: str, metadata: dict):
    TEXTS_DIR.mkdir(parents=True, exist_ok=True)
    path = TEXTS_DIR / f"PAP-{key}.md"
    header = f"""---
paper_id: PAP-{key}
doi: {metadata.get('doi', 'unknown')}
source: {metadata.get('source', 'mpg_pure')}
fetch_date: {datetime.now().strftime('%Y-%m-%d')}
word_count: {count_words(text)}
has_references: {has_references_section(text)}
pure_item_id: {metadata.get('item_id', 'unknown')}
---

"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(header + text)
    return path


# ---------------------------------------------------------------------------
# Main Processing
# ---------------------------------------------------------------------------
def process_item(item_info: dict, l2_papers: dict, dry_run: bool = False) -> str:
    """Process a PuRe item: match to L2 paper, download PDF, extract text."""
    doi = item_info["doi"]
    title = item_info["title"]

    # Match to L2 paper: DOI first, then title fallback
    match = None
    if doi:
        match = l2_papers.get(doi)
    if not match and title:
        title_key = f"title:{normalize_title(title)}"
        match = l2_papers.get(title_key)
    if not match:
        stats["skipped_no_match"] += 1
        return f"SKIP (no matching L2 paper for DOI={doi or 'none'}, title={title[:50]})"

    key, data, yaml_path = match
    stats["matched_to_l2"] += 1

    # Use DOI from L2 paper if PuRe item has none
    if not doi:
        doi = (data.get("doi") or "").strip().lower()

    # If BibTeX-only, create proper YAML structure
    if data.get("_bib_only"):
        data = {
            "bibtex_key": key,
            "id": f"PAP-{key}",
            "title": data.get("title", title),
            "doi": doi,
            "ebf_integration": {
                "use_for": ["LIT-SUT"],
                "evidence_tier": 3,
            },
            "full_text": {"available": False, "content_level": "L0"},
        }

    # Fetch FRESH item details from PuRe REST API
    # Search results have stale file IDs that cause HTTP 400 errors
    object_id = item_info["object_id"]
    item_id = item_info["item_id"]
    print(f"    Fetching fresh item details for {item_id}...")
    fresh_item = get_item_with_files(item_id)

    if not fresh_item:
        stats["errors"] += 1
        paper_results.append({
            "key": key, "doi": doi, "status": "ERROR",
            "item_id": item_id,
            "error": f"Failed to GET item details from REST API",
        })
        return f"ERROR: Could not fetch item {item_id} from REST API"

    # Navigate to data node (response might be the data node directly)
    fresh_data = fresh_item.get("data", fresh_item) if isinstance(fresh_item, dict) else fresh_item

    # Extract file components from fresh data
    files = extract_files_from_item(fresh_data, object_id)
    print(f"    Fresh item has {len(files)} file components")

    # Log storage types
    storage_types = [f.get("storage", "unknown") for f in files]
    for st in set(storage_types):
        count = storage_types.count(st)
        print(f"      Storage: {st} × {count}")

    if not files:
        return f"SKIP (PuRe item has no file components after fresh fetch)"

    # Separate INTERNAL_MANAGED (actual PDFs) from EXTERNAL_URL (just links)
    internal_files = [f for f in files if f.get("storage") == "INTERNAL_MANAGED"]
    external_files = [f for f in files if f.get("storage") == "EXTERNAL_URL"]
    other_files = [f for f in files if f.get("storage") not in ("INTERNAL_MANAGED", "EXTERNAL_URL")]

    # Prioritize: internal files first, then external URLs, then others
    ordered_files = internal_files + external_files + other_files

    # Filter for PDF-like files (but keep all if none match)
    pdf_files = [f for f in ordered_files if
                 "pdf" in (f.get("content_type", "") or "").lower()
                 or (f.get("name", "") or "").lower().endswith(".pdf")
                 or (f.get("visibility") in ("PUBLIC", "AUDIENCE") and f.get("storage") == "INTERNAL_MANAGED")]

    if not pdf_files:
        pdf_files = ordered_files  # Try all files if no obvious PDFs

    if internal_files:
        print(f"    → {len(internal_files)} INTERNAL files (actual PDFs in PuRe)")
    if external_files:
        print(f"    → {len(external_files)} EXTERNAL_URL files (DOI/publisher links)")
        for ef in external_files:
            print(f"      URL: {(ef.get('content_ref') or ef.get('name', ''))[:80]}")

    if dry_run:
        return f"DRY-RUN: {len(pdf_files)} files available (item {item_id})"

    # Try each file component
    text = None
    fetch_error = None

    for fc in pdf_files:
        urls = fc.get("download_urls", [])
        if not urls:
            continue

        for url in urls:
            print(f"    Trying: {url[:100]}...")

            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
                tmp_path = tmp.name
            try:
                ok, detail = download_pdf(url, tmp_path)
                if ok:
                    stats["pdfs_downloaded"] += 1
                    text = extract_text_from_pdf(tmp_path)
                    if text:
                        break
                    else:
                        fetch_error = f"pdftotext empty for {url}"
                else:
                    fetch_error = f"Download failed: {detail}"
            finally:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
            time.sleep(0.3)  # brief pause between URL attempts

        if text:
            break

    if not text:
        stats["errors"] += 1
        error_msg = fetch_error or "No text extracted from any file"
        paper_results.append({
            "key": key, "doi": doi, "status": "ERROR",
            "item_id": item_info["item_id"],
            "error": error_msg,
        })
        return f"ERROR: {error_msg}"

    # Clean up and validate
    text = cleanup_text(text)
    is_l3, level_str, details = validate_l3(text)

    # Save fulltext
    metadata = {
        "doi": doi,
        "source": "mpg_pure",
        "item_id": item_info["item_id"],
    }
    text_path = save_fulltext(key, text, metadata)

    # Update YAML
    if "full_text" not in data:
        data["full_text"] = {}

    data["full_text"]["available"] = True
    data["full_text"]["path"] = str(text_path)
    data["full_text"]["content_level"] = "L3" if is_l3 else "L2"
    data["full_text"]["format"] = "markdown"
    data["full_text"]["archived_date"] = datetime.now().strftime("%Y-%m-%d")
    data["full_text"]["word_count"] = details["word_count"]
    data["full_text"]["has_references"] = details["has_references"]
    data["full_text"]["source"] = "mpg_pure"
    data["full_text"]["pure_item_id"] = item_info["item_id"]

    if is_l3:
        data["l3_upgrade_date"] = datetime.now().strftime("%Y-%m-%d")
        data["l3_upgrade_method"] = "mpg_pure_fulltext_fetch_v1"

    save_paper_yaml(key, data)

    if is_l3:
        stats["l3_upgraded"] += 1
        paper_results.append({
            "key": key, "doi": doi, "status": "L3",
            "word_count": details["word_count"],
            "has_references": details["has_references"],
            "item_id": item_info["item_id"],
        })
        return f"L3 ✓ ({details['word_count']} words, refs={'yes' if details['has_references'] else 'no'})"
    else:
        stats["l2_partial"] += 1
        paper_results.append({
            "key": key, "doi": doi, "status": "L2+",
            "word_count": details["word_count"],
            "has_references": details["has_references"],
            "item_id": item_info["item_id"],
            "reason": level_str,
        })
        return f"L2+ ({details['word_count']} words) — {level_str}"


def inspect_item(item_id: str):
    """Inspect a single PuRe item in detail — shows all file info, storage types, URLs."""
    print("=" * 70)
    print(f"INSPECTING PuRe ITEM: {item_id}")
    print("=" * 70)

    # Fetch item
    print(f"\nFetching {item_id} via REST API...")
    item = get_item_with_files(item_id)
    if not item:
        print("ERROR: Could not fetch item")
        return

    data = item.get("data", item) if isinstance(item, dict) else item
    if not isinstance(data, dict):
        print(f"ERROR: Unexpected data type: {type(data)}")
        return

    # Basic metadata
    meta = data.get("metadata", {})
    print(f"\n--- METADATA ---")
    print(f"  objectId:      {data.get('objectId', '?')}")
    print(f"  versionNumber: {data.get('versionNumber', '?')}")
    print(f"  versionState:  {data.get('versionState', '?')}")
    print(f"  publicState:   {data.get('publicState', '?')}")
    print(f"  title:         {meta.get('title', '?')[:100]}")
    print(f"  genre:         {meta.get('genre', '?')}")

    # Creators
    creators = meta.get("creators", [])
    if creators:
        names = []
        for c in creators[:5]:
            p = c.get("person", {})
            fn = p.get("familyName", "")
            gn = p.get("givenName", "")
            names.append(f"{gn} {fn}".strip() or str(c.get("value", "?")))
        print(f"  creators:      {', '.join(names)}")

    # Identifiers
    identifiers = meta.get("identifiers", [])
    if identifiers:
        for ident in identifiers:
            print(f"  identifier:    {ident.get('type', '?')}: {ident.get('id', '?')}")

    # Dates
    for date_field in ["datePublishedInPrint", "datePublishedOnline", "dateCreated"]:
        val = meta.get(date_field, "")
        if val:
            print(f"  {date_field}: {val}")

    # Files — the key part
    files = data.get("files", []) or []
    print(f"\n--- FILES ({len(files)}) ---")

    # Write inspection results to log (single pass: print + capture)
    log_path = Path("data/mpg-fulltext-fetch-log.yaml")
    log = {
        "run_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "mode": "inspect",
        "inspected_item": item_id,
        "objectId": data.get("objectId", ""),
        "versionNumber": data.get("versionNumber", ""),
        "title": meta.get("title", "")[:200],
        "n_files": len(files),
        "files_detail": [],
        "download_tests": [],
    }

    if not files:
        print("  NO FILES FOUND")
    else:
        obj_id = data.get("objectId", "")
        ver = data.get("versionNumber", "")
        item_ver_id = f"{obj_id}_{ver}" if ver else obj_id

        for i, f in enumerate(files):
            file_id = f.get("objectId", "")
            fname = f.get("name", "")
            storage = f.get("storage", "")

            print(f"\n  File {i+1}:")
            print(f"    objectId:     {file_id}")
            print(f"    name:         {fname}")
            print(f"    storage:      {storage}")
            print(f"    visibility:   {f.get('visibility', '?')}")
            print(f"    mimeType:     {f.get('mimeType', '?')}")
            print(f"    size:         {f.get('size', '?')} bytes")
            print(f"    content:      {str(f.get('content', '?'))[:200]}")

            # Capture file details for YAML log
            log["files_detail"].append({
                "objectId": file_id,
                "name": str(fname)[:200],
                "storage": storage,
                "visibility": f.get("visibility", ""),
                "mimeType": f.get("mimeType", ""),
                "size": f.get("size", 0),
                "content": str(f.get("content", ""))[:300],
            })

            # Build download URLs
            print(f"    --- DOWNLOAD URLs ---")
            if storage == "INTERNAL_MANAGED":
                if fname and not fname.startswith("http"):
                    print(f"    [1] https://pure.mpg.de/pubman/item/{item_ver_id}/component/{file_id}/{fname}")
                print(f"    [2] {PURE_BASE}/items/{item_ver_id}/component/{file_id}/content")
                if obj_id != item_ver_id:
                    print(f"    [3] {PURE_BASE}/items/{obj_id}/component/{file_id}/content")
            elif storage == "EXTERNAL_URL":
                ext_url = f.get("content", "") or fname
                print(f"    [ext] {ext_url}")
            else:
                print(f"    [fallback] {PURE_BASE}/items/{item_ver_id}/component/{file_id}/content")

            # Try downloading INTERNAL_MANAGED + PUBLIC files (single attempt, logged)
            if storage == "INTERNAL_MANAGED" and f.get("visibility") in ("PUBLIC", "AUDIENCE"):
                print(f"    --- DOWNLOAD ATTEMPT ---")
                urls_to_try = []
                if fname and not fname.startswith("http"):
                    urls_to_try.append(f"https://pure.mpg.de/pubman/item/{item_ver_id}/component/{file_id}/{fname}")
                urls_to_try.append(f"{PURE_BASE}/items/{item_ver_id}/component/{file_id}/content")

                test_result = {"file_id": file_id, "urls_tried": [], "success": False}
                with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
                    tmp_path = tmp.name
                try:
                    for url in urls_to_try:
                        print(f"    Trying: {url[:100]}...")
                        ok, detail = download_pdf(url, tmp_path)
                        test_result["urls_tried"].append({"url": url[:200], "ok": ok, "detail": detail[:200]})
                        print(f"    Result: {detail}")
                        if ok:
                            test_result["success"] = True
                            text = extract_text_from_pdf(tmp_path)
                            if text:
                                wc = count_words(text)
                                has_refs = has_references_section(text)
                                test_result["word_count"] = wc
                                test_result["has_references"] = has_refs
                                test_result["text_preview"] = text[:300]
                                print(f"    Text extracted: {wc} words, references={'yes' if has_refs else 'no'}")
                                print(f"    First 200 chars: {text[:200]}")
                            break
                finally:
                    if os.path.exists(tmp_path):
                        os.unlink(tmp_path)
                log["download_tests"].append(test_result)

    with open(log_path, "w") as fp:
        yaml.dump(log, fp, default_flow_style=False, allow_unicode=True)
    print(f"\nInspection log written to: {log_path}")


def _check_item_for_internal(fd: dict, item_id: str) -> dict | None:
    """Check a fetched item for INTERNAL_MANAGED files that are downloadable.

    PuRe visibility values:
    - PUBLIC: Anyone can download (most common for postprints)
    - AUDIENCE: Available to registered users / institutional access
    - PRIVATE: Only owner can access

    We accept PUBLIC and AUDIENCE since both are accessible via REST API.
    The actual download will verify accessibility.

    Returns item info dict if found, None otherwise.
    """
    ALLOWED_VISIBILITY = {"PUBLIC", "AUDIENCE"}

    files = fd.get("files", []) or []
    if not files:
        return None

    has_internal = False
    for f in files:
        if (f.get("storage") == "INTERNAL_MANAGED"
                and f.get("visibility", "") in ALLOWED_VISIBILITY):
            has_internal = True
            break

    if not has_internal:
        return None

    meta = fd.get("metadata", {})
    doi = ""
    for ident in (meta.get("identifiers", []) or []):
        if isinstance(ident, dict) and ident.get("type") == "DOI":
            doi = ident.get("id", "")

    return {
        "item_id": fd.get("objectId", item_id),
        "version": fd.get("versionNumber", ""),
        "title": (meta.get("title", "") or "")[:120],
        "doi": doi,
        "files": [
            {
                "file_id": f.get("objectId", ""),
                "name": str(f.get("name", ""))[:150],
                "storage": f.get("storage", ""),
                "visibility": f.get("visibility", ""),
                "size": f.get("size", 0),
                "mimeType": f.get("mimeType", ""),
            }
            for f in files
            if (f.get("storage") == "INTERNAL_MANAGED"
                and f.get("visibility", "") in ALLOWED_VISIBILITY)
        ],
    }


def find_internal_managed(person_id: str, author_name: str):
    """Scan PuRe items for INTERNAL_MANAGED files using FOUR strategies:

    Strategy 1: Person search (covers items linked to person ID)
    Strategy 2: DOI search (covers items NOT linked but matchable by DOI)
    Strategy 3: Re-check external-only items from Strategy 1 via DOI lookup
    Strategy 4: Title search fallback for DOIs with no PuRe hit

    Strategy 4 addresses the 84% of DOIs that return zero PuRe results in
    Strategy 2. Many papers ARE on PuRe but their DOI metadata doesn't match
    exactly. Title-based search catches these (e.g. sutter2025risk).
    """
    print("=" * 70)
    print("FIND INTERNAL_MANAGED FILES (Person + DOI + Re-check + Title)")
    print("=" * 70)
    print(f"Person ID: {person_id}")
    print(f"Author: {author_name}")
    print()

    internal_items = []
    seen_object_ids = set()  # dedup across strategies
    external_only_oids = set()  # Track items classified as external-only
    external_only = 0
    no_files = 0
    errors = 0
    storage_dist = {}

    # === Strategy 1: Person search ===
    print("Strategy 1: Searching by person ID...")
    records = search_pure_by_person(person_id, author_name=author_name)
    print(f"  Found {len(records)} items via person search")

    # DEDUP: Extract unique base objectIds from search results FIRST.
    # Person search returns many versions of the same item (e.g., 420 records
    # for ~200 unique papers). Processing each unique objectId ONCE avoids
    # redundant API calls and inflated counts.
    # Keep the HIGHEST versioned ID per objectId (latest version in search).
    unique_oids = {}  # base_oid → (item_id, info)
    for record in records:
        info = extract_item_info(record)
        item_id = info["item_id"]
        obj_id = info.get("object_id", item_id)
        if obj_id not in unique_oids:
            unique_oids[obj_id] = (item_id, info)
        else:
            # Keep the record with the highest version number
            prev_id = unique_oids[obj_id][0]
            try:
                prev_ver = int(prev_id.rsplit("_", 1)[-1])
                curr_ver = int(item_id.rsplit("_", 1)[-1])
                if curr_ver > prev_ver:
                    unique_oids[obj_id] = (item_id, info)
            except (ValueError, IndexError):
                pass

    print(f"  Unique base objectIds: {len(unique_oids)} (from {len(records)} records)")

    # Track non-PUBLIC INTERNAL_MANAGED for diagnostics
    internal_non_public = 0
    visibility_dist = {}

    for i, (obj_id, (item_id, info)) in enumerate(unique_oids.items()):
        # Try BOTH base objectId and versioned ID.
        # PuRe's GET /items/{base_id} may return a non-released version with
        # restricted file visibility, while the versioned ID (from search)
        # might point to the released version with PUBLIC files.
        candidates = [obj_id]
        if item_id != obj_id:
            candidates.append(item_id)

        fd = None
        for cand_id in candidates:
            fresh = get_item_with_files(cand_id)
            if not fresh:
                continue
            fd_temp = fresh.get("data", fresh) if isinstance(fresh, dict) else fresh
            if not isinstance(fd_temp, dict):
                continue
            # Check if this version has INTERNAL_MANAGED files
            result_temp = _check_item_for_internal(fd_temp, cand_id)
            if result_temp:
                # Found INTERNAL_MANAGED! Use this version.
                fd = fd_temp
                break
            elif fd is None:
                # Keep first valid response as fallback
                fd = fd_temp

        if fd is None:
            errors += 1
            continue

        actual_oid = fd.get("objectId", obj_id)
        seen_object_ids.add(actual_oid)

        files = fd.get("files", []) or []
        if not files:
            no_files += 1
        else:
            for f in files:
                st = f.get("storage", "unknown")
                storage_dist[st] = storage_dist.get(st, 0) + 1
                # Track visibility for INTERNAL_MANAGED files
                if st == "INTERNAL_MANAGED":
                    vis = f.get("visibility", "unknown")
                    visibility_dist[vis] = visibility_dist.get(vis, 0) + 1

            result = _check_item_for_internal(fd, item_id)
            if result:
                result["source"] = "person_search"
                internal_items.append(result)
                print(f"  [{i+1}/{len(unique_oids)}] ✓ INTERNAL: {result['title'][:60]}...")
            else:
                # Check WHY it failed: are there INTERNAL_MANAGED but non-PUBLIC?
                has_im = any(f.get("storage") == "INTERNAL_MANAGED" for f in files)
                if has_im:
                    internal_non_public += 1
                    vis_list = [f.get("visibility", "?") for f in files
                                if f.get("storage") == "INTERNAL_MANAGED"]
                    print(f"  [{i+1}/{len(unique_oids)}] ⚠ INTERNAL but NOT downloadable "
                          f"({obj_id}): visibility={vis_list}")
                external_only += 1
                external_only_oids.add(actual_oid)

        if (i + 1) % 50 == 0:
            print(f"  ... scanned {i+1}/{len(unique_oids)}")
        time.sleep(0.15)

    person_items = len(records)
    internal_from_s1 = len(internal_items)
    print(f"  Strategy 1 complete: {internal_from_s1} INTERNAL_MANAGED found")
    print(f"  Strategy 1 stats: {len(unique_oids)} unique objectIds "
          f"(from {len(records)} records), "
          f"{no_files} no-files, {external_only} external-only, {errors} errors")
    if internal_non_public:
        print(f"  ⚠ {internal_non_public} items had INTERNAL_MANAGED with non-PUBLIC visibility!")
        print(f"  Visibility distribution for INTERNAL_MANAGED: {visibility_dist}")
    print()

    # === Strategy 2: DOI search (supplementary — NEW items only) ===
    print("Strategy 2: Searching by DOI from paper database...")
    l2_papers = get_l2_papers(author_filter=author_name)

    # Collect unique DOIs (from both L0/L1/L2 papers AND BibTeX-only entries)
    dois = set()
    for key, val in l2_papers.items():
        if key.startswith("title:"):
            continue  # skip title entries
        dois.add(key)  # key is the DOI

    # Also extract DOIs from BibTeX for papers without YAML
    bib_dois = _extract_dois_from_bibtex(author_filter=author_name)
    dois.update(bib_dois)

    print(f"  DOIs to search: {len(dois)} (YAML + BibTeX)")

    # DEBUG: Check if specific DOIs of interest are in the set
    debug_dois = ["10.1257/aer.20211217"]  # sutter2025risk
    for dd in debug_dois:
        if dd in dois:
            print(f"  ✓ DEBUG: DOI {dd} IS in search set")
        else:
            print(f"  ✗ DEBUG: DOI {dd} NOT in search set!")

    doi_searched = 0
    doi_found_new = 0
    doi_with_hits = 0
    doi_already_seen = 0
    doi_recheck_external = 0
    doi_no_hit = []  # Track DOIs that returned no PuRe results

    for doi in sorted(dois):
        doi_searched += 1
        if doi_searched % 20 == 0:
            print(f"  ... searched {doi_searched}/{len(dois)} DOIs "
                  f"(hits: {doi_with_hits}, new: {doi_found_new}, seen: {doi_already_seen})")

        doi_records = search_pure_by_doi(doi)
        if not doi_records:
            # Track DOIs that we expected to find but didn't
            if doi in [d.lower() for d in debug_dois]:
                print(f"  ✗ DEBUG: DOI {doi} returned NO results from PuRe!")
            doi_no_hit.append(doi)
            continue

        doi_with_hits += 1

        for rec in doi_records:
            dn = rec.get("data", rec) if isinstance(rec, dict) else rec
            oid = dn.get("objectId", "") if isinstance(dn, dict) else ""

            already_seen = oid in seen_object_ids
            already_external = oid in external_only_oids

            if already_seen and not already_external:
                # Already found with INTERNAL_MANAGED in Strategy 1 → skip
                doi_already_seen += 1
                continue

            # BUG FIX: If item was seen but classified as external_only,
            # re-check it! Strategy 1 may have fetched an old version without
            # the PDF. The DOI search might find a different/newer version.
            if already_external:
                doi_recheck_external += 1

            if not already_seen:
                seen_object_ids.add(oid)
                doi_found_new += 1

            # Fetch full item data
            fresh = get_item_with_files(oid)
            if not fresh:
                errors += 1
                continue

            fd = fresh.get("data", fresh) if isinstance(fresh, dict) else fresh
            if not isinstance(fd, dict):
                errors += 1
                continue

            files = fd.get("files", []) or []
            if not files:
                if not already_seen:
                    no_files += 1
            else:
                if not already_seen:
                    for f in files:
                        st = f.get("storage", "unknown")
                        storage_dist[st] = storage_dist.get(st, 0) + 1

                result = _check_item_for_internal(fd, oid)
                if result:
                    # Check not already found (dedup by DOI)
                    already_found = any(
                        it.get("doi", "").lower() == doi.lower()
                        for it in internal_items
                    )
                    if not already_found:
                        src = "doi_recheck" if already_external else "doi_search"
                        result["source"] = src
                        result["matched_doi"] = doi
                        internal_items.append(result)
                        if already_external:
                            external_only -= 1
                            external_only_oids.discard(oid)
                            print(f"  ✓ RECOVERED via DOI re-check [{doi}]: {result['title'][:60]}...")
                        else:
                            print(f"  ✓ NEW via DOI [{doi}]: {result['title'][:60]}...")
                elif not already_seen:
                    external_only += 1

        time.sleep(0.2)

    internal_from_s2 = len(internal_items) - internal_from_s1
    print(f"  Strategy 2 complete: {doi_searched} DOIs searched")
    print(f"    DOIs with verified hits: {doi_with_hits}")
    print(f"    Items already found (INTERNAL) in S1: {doi_already_seen}")
    print(f"    Items re-checked (were external-only in S1): {doi_recheck_external}")
    print(f"    NEW items found: {doi_found_new}")
    print(f"    NEW INTERNAL_MANAGED: {internal_from_s2}")
    print()

    # === Strategy 3: Re-check remaining external-only items ===
    # After Bug 1 fix (latest version in S1) and Bug 2 fix (S2 re-checks
    # external-only via DOI), Strategy 3 catches remaining edge cases:
    # items where PuRe DOI search fails but a direct re-GET might work.
    if external_only_oids:
        print(f"Strategy 3: Re-checking {len(external_only_oids)} remaining external-only items...")
        recheck_found = 0

        # Build objectId→DOI mapping from person search records
        oid_to_doi = {}
        for record in records:
            info = extract_item_info(record)
            if info["doi"]:
                oid_to_doi[info.get("object_id", "")] = info["doi"]

        # Also build title→DOI mapping from our papers DB for items
        # where PuRe search didn't have a DOI in metadata
        title_to_doi = {}
        for key, val in l2_papers.items():
            if key.startswith("title:"):
                k, data, path = val
                doi_val = (data.get("doi") or "").strip().lower()
                if doi_val:
                    title_to_doi[key.replace("title:", "")] = doi_val

        # Also match by title from person search records
        oid_to_title = {}
        for record in records:
            info = extract_item_info(record)
            oid = info.get("object_id", "")
            if info["title"] and oid:
                oid_to_title[oid] = normalize_title(info["title"])

        for oid in sorted(external_only_oids):
            doi = oid_to_doi.get(oid, "")
            if not doi:
                # Try to find DOI via title matching
                title = oid_to_title.get(oid, "")
                if title:
                    doi = title_to_doi.get(title, "")
            if not doi:
                continue

            # Search PuRe by DOI (might return a different version with files)
            doi_recs = search_pure_by_doi(doi)
            if not doi_recs:
                continue

            for rec in doi_recs:
                dn = rec.get("data", rec) if isinstance(rec, dict) else rec
                rec_oid = dn.get("objectId", "") if isinstance(dn, dict) else ""

                # Fetch FRESH item data
                fresh = get_item_with_files(rec_oid)
                if not fresh:
                    continue

                fd = fresh.get("data", fresh) if isinstance(fresh, dict) else fresh
                if not isinstance(fd, dict):
                    continue

                result = _check_item_for_internal(fd, rec_oid)
                if result:
                    # Check not already found
                    already = any(
                        it.get("doi", "").lower() == doi.lower()
                        for it in internal_items
                    )
                    if not already:
                        result["source"] = "recheck_strategy3"
                        result["matched_doi"] = doi
                        internal_items.append(result)
                        recheck_found += 1
                        external_only -= 1
                        print(f"  ✓ RECOVERED via re-check [{doi}]: {result['title'][:60]}...")

            time.sleep(0.2)

        print(f"  Strategy 3 complete: {recheck_found} INTERNAL_MANAGED recovered")
        print()

    # === Strategy 4: Title search fallback for DOIs with no PuRe hit ===
    # 84% of DOIs (248/293 in Run #3) return zero results from PuRe DOI search.
    # Many of these papers ARE on PuRe but without matching DOI in metadata.
    # Title search catches them. Key target: sutter2025risk (10.1257/aer.20211217).
    internal_from_s4 = 0
    s4_diag = {"doi_to_title_count": 0, "overlap_count": 0, "searchable_count": 0,
               "s4_searched": 0, "s4_found": 0, "doi_no_hit_sample": [],
               "doi_to_title_sample": [], "bib_file_exists": False, "papers_dir_exists": False}
    if doi_no_hit:
        # Build DOI→title mapping directly from BibTeX + YAML
        # Previous approach iterated l2_papers keys, but those only contain DOIs
        # from YAML files — BibTeX-only entries were indexed by title key only.
        # The new _build_doi_title_map() reads DOI+title pairs from BibTeX directly.
        s4_diag["bib_file_exists"] = Path("bibliography/bcm_master.bib").exists()
        s4_diag["papers_dir_exists"] = PAPERS_DIR.exists()
        doi_to_title = _build_doi_title_map(author_filter=author_name)
        s4_diag["doi_to_title_count"] = len(doi_to_title)
        print(f"  DOI→title mapping: {len(doi_to_title)} entries from BibTeX+YAML")

        # Debug: Show sample doi_no_hit entries and map keys
        print(f"  doi_no_hit count: {len(doi_no_hit)}")
        if doi_no_hit:
            print(f"  doi_no_hit sample: {doi_no_hit[:3]}")
        if doi_to_title:
            sample_keys = list(doi_to_title.keys())[:3]
            print(f"  doi_to_title sample keys: {sample_keys}")
        # Check specific DOI
        test_doi = "10.1257/aer.20211217"
        print(f"  DEBUG: {test_doi} in doi_no_hit? {test_doi in doi_no_hit}")
        print(f"  DEBUG: {test_doi} in doi_to_title? {test_doi in doi_to_title}")

        # Check overlap
        no_hit_set = set(doi_no_hit)
        map_set = set(doi_to_title.keys())
        overlap = no_hit_set & map_set
        s4_diag["overlap_count"] = len(overlap)
        s4_diag["doi_no_hit_sample"] = doi_no_hit[:5]
        s4_diag["doi_to_title_sample"] = list(doi_to_title.keys())[:5]
        print(f"  DEBUG: overlap(doi_no_hit, doi_to_title) = {len(overlap)}")

        searchable = [d for d in doi_no_hit if d in doi_to_title
                      and len(doi_to_title[d]) > 10]
        print(f"Strategy 4: Title search for {len(searchable)}/{len(doi_no_hit)} DOIs with no PuRe hit...")
        if searchable:
            for i, sd in enumerate(sorted(searchable)[:3]):
                print(f"  First searchable [{i}]: DOI={sd} → title={doi_to_title[sd][:60]}")

        s4_diag["searchable_count"] = len(searchable)
        search_diag = {}  # accumulate per-search diagnostics
        s4_searched = 0
        s4_found = 0
        for doi in sorted(searchable):
            title = doi_to_title[doi]
            s4_searched += 1
            if s4_searched % 20 == 0:
                print(f"  ... searched {s4_searched}/{len(searchable)} titles "
                      f"(found: {s4_found})")

            title_records = search_pure_by_title(title, author_hint=author_name, diag=search_diag)
            if not title_records:
                continue

            for rec in title_records:
                dn = rec.get("data", rec) if isinstance(rec, dict) else rec
                oid = dn.get("objectId", "") if isinstance(dn, dict) else ""

                if oid in seen_object_ids:
                    continue  # already processed

                seen_object_ids.add(oid)

                # Fetch full item data
                fresh = get_item_with_files(oid)
                if not fresh:
                    errors += 1
                    continue

                fd = fresh.get("data", fresh) if isinstance(fresh, dict) else fresh
                if not isinstance(fd, dict):
                    errors += 1
                    continue

                files = fd.get("files", []) or []
                if not files:
                    no_files += 1
                else:
                    for f in files:
                        st = f.get("storage", "unknown")
                        storage_dist[st] = storage_dist.get(st, 0) + 1

                result = _check_item_for_internal(fd, oid)
                if result:
                    # Dedup by DOI
                    already = any(
                        it.get("doi", "").lower() == doi.lower()
                        for it in internal_items
                    )
                    if not already:
                        result["source"] = "title_search"
                        result["matched_doi"] = doi
                        internal_items.append(result)
                        s4_found += 1
                        internal_from_s4 += 1
                        print(f"  ✓ NEW via title [{doi}]: {result['title'][:60]}...")
                else:
                    external_only += 1

            time.sleep(0.3)

        s4_diag["s4_searched"] = s4_searched
        s4_diag["s4_found"] = s4_found
        s4_diag["search_diagnostics"] = search_diag
        print(f"  Strategy 4 complete: {s4_searched} titles searched, {s4_found} INTERNAL_MANAGED found")
        if search_diag:
            print(f"  Search breakdown: {search_diag}")
        print()

    total_scanned = person_items + doi_found_new

    # Summary
    print("=" * 70)
    print("RESULTS")
    print("=" * 70)
    print(f"Person search items:     {person_items}")
    print(f"DOI search new items:    {doi_found_new}")
    print(f"Total unique items:      {len(seen_object_ids)}")
    internal_from_s3 = len(internal_items) - internal_from_s1 - internal_from_s2 - internal_from_s4
    print(f"  With INTERNAL_MANAGED: {len(internal_items)}")
    print(f"    from Strategy 1 (person):    {internal_from_s1}")
    print(f"    from Strategy 2 (DOI new):   {internal_from_s2}")
    print(f"    from Strategy 3 (re-check):  {internal_from_s3}")
    print(f"    from Strategy 4 (title):     {internal_from_s4}")
    print(f"  With EXTERNAL_URL only: {external_only}")
    print(f"  No files:              {no_files}")
    print(f"  Errors:                {errors}")
    print(f"\nStorage distribution:")
    for st, count in sorted(storage_dist.items()):
        print(f"  {st}: {count}")

    if internal_items:
        print(f"\n--- ITEMS WITH DOWNLOADABLE PDFs ({len(internal_items)}) ---")
        for item in internal_items:
            src = item.get("source", "?")
            print(f"\n  {item['item_id']} (v{item['version']}) [via {src}]")
            print(f"    Title: {item['title']}")
            print(f"    DOI:   {item['doi'] or '(none)'}")
            for f in item["files"]:
                print(f"    File:  {f['name'][:80]} ({f['size']} bytes, {f['mimeType']})")

    # Write log (separate file to prevent overwriting)
    log_path = Path("data/mpg-find-internal-log.yaml")
    log = {
        "run_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "mode": "find-internal",
        "person_id": person_id,
        "author_name": author_name,
        "person_search_items": person_items,
        "doi_search_dois": doi_searched,
        "doi_search_verified_hits": doi_with_hits,
        "doi_search_already_seen": doi_already_seen,
        "doi_search_recheck_external": doi_recheck_external,
        "doi_search_new_items": doi_found_new,
        "recheck_external_only": len(external_only_oids),
        "total_unique_items": len(seen_object_ids),
        "unique_person_search_oids": len(unique_oids),
        "internal_managed_count": len(internal_items),
        "internal_from_strategy1": internal_from_s1,
        "internal_from_strategy2": internal_from_s2,
        "internal_from_strategy3": internal_from_s3,
        "internal_from_strategy4": internal_from_s4,
        "internal_non_public_count": internal_non_public,
        "external_only_count": external_only,
        "no_files_count": no_files,
        "errors": errors,
        "storage_distribution": storage_dist,
        "visibility_distribution": visibility_dist,
        "doi_no_hit_count": len(doi_no_hit),
        "strategy4_diagnostics": s4_diag,
        "internal_items": internal_items,
    }
    with open(log_path, "w") as fp:
        yaml.dump(log, fp, default_flow_style=False, allow_unicode=True)
    print(f"\nLog written to: {log_path}")

    # Also write to the standard log path for fetch-internal to read
    fetch_log_path = Path("data/mpg-fulltext-fetch-log.yaml")
    log["_note"] = "Copy from find-internal for fetch-internal to read"
    with open(fetch_log_path, "w") as fp:
        yaml.dump(log, fp, default_flow_style=False, allow_unicode=True)
    print(f"Also written to: {fetch_log_path} (for --fetch-internal)")


def fetch_internal_managed(author_name: str, batch: int = 50, dry_run: bool = False):
    """Download PDFs from INTERNAL_MANAGED items found by --find-internal.

    Reads the find-internal log, matches items to L2 papers by DOI,
    downloads the PDFs, extracts text, and upgrades to L3.
    """
    # Try dedicated log first, fall back to shared log
    log_path = Path("data/mpg-find-internal-log.yaml")
    if not log_path.exists():
        log_path = Path("data/mpg-fulltext-fetch-log.yaml")
    if not log_path.exists():
        print("ERROR: No find-internal log found. Run --find-internal first.")
        return

    with open(log_path) as f:
        log = yaml.safe_load(f)

    if not log or log.get("mode") != "find-internal":
        print("ERROR: Log file is not from a find-internal run.")
        print(f"  Log mode: {log.get('mode', 'unknown') if log else 'empty'}")
        print(f"  Log path: {log_path}")
        print("  Run --find-internal first to scan for INTERNAL_MANAGED files.")
        return

    internal_items = log.get("internal_items", [])
    if not internal_items:
        print("No INTERNAL_MANAGED items found in log.")
        return

    print("=" * 70)
    print("FETCH INTERNAL_MANAGED PDFs (from find-internal results)")
    print("=" * 70)
    print(f"Items to process: {len(internal_items)}")
    print(f"Author filter: {author_name}")
    print(f"Batch: {batch}")
    print(f"Dry run: {dry_run}")
    print()

    # Load L2 papers for matching
    l2_papers = get_l2_papers(author_name)
    print()

    results = []
    processed = 0

    for item in internal_items[:batch]:
        item_id = item.get("item_id", "")
        doi = (item.get("doi") or "").strip().lower()
        title = item.get("title", "")
        files = item.get("files", [])

        processed += 1
        print(f"\n[{processed}/{min(len(internal_items), batch)}] {title[:60]}...")
        print(f"  DOI: {doi}")
        print(f"  Item: {item_id}")
        print(f"  Files: {len(files)}")

        # Match to L2 paper by DOI first, then title
        match = None
        if doi:
            match = l2_papers.get(doi)
        if not match and title:
            match = l2_papers.get(f"title:{normalize_title(title)}")

        if not match:
            print(f"  → SKIP: No matching L2 paper")
            results.append({"item_id": item_id, "doi": doi, "status": "SKIP",
                            "reason": "no_l2_match", "title": title[:80]})
            continue

        key, data, yaml_path = match
        print(f"  → Matched to: PAP-{key}")

        # Check if already L3
        ft = data.get("full_text", {})
        if ft.get("content_level") == "L3" and ft.get("word_count", 0) >= MIN_WORDS_SHORT:
            print(f"  → SKIP: Already L3 ({ft.get('word_count', 0)} words)")
            results.append({"item_id": item_id, "key": key, "doi": doi,
                            "status": "SKIP", "reason": "already_l3"})
            continue

        # If BibTeX-only, create proper YAML structure
        if data.get("_bib_only"):
            data = {
                "bibtex_key": key,
                "id": f"PAP-{key}",
                "title": data.get("title", title),
                "doi": doi,
                "ebf_integration": {"use_for": ["LIT-SUT"], "evidence_tier": 3},
                "full_text": {"available": False, "content_level": "L0"},
            }

        if dry_run:
            print(f"  → DRY-RUN: Would download {len(files)} files")
            results.append({"item_id": item_id, "key": key, "doi": doi,
                            "status": "DRY_RUN", "files": len(files)})
            continue

        # Fetch fresh item data for download
        print(f"  Fetching fresh item data...")
        fresh = get_item_with_files(item_id)
        if not fresh:
            # Try with version suffix
            version = item.get("version", "")
            if version:
                fresh = get_item_with_files(f"{item_id}_{version}")
        if not fresh:
            print(f"  → ERROR: Could not fetch item")
            results.append({"item_id": item_id, "key": key, "doi": doi,
                            "status": "ERROR", "error": "fetch_failed"})
            stats["errors"] += 1
            continue

        fresh_data = fresh.get("data", fresh) if isinstance(fresh, dict) else fresh
        file_components = extract_files_from_item(fresh_data, item_id)

        # Filter for INTERNAL_MANAGED + downloadable PDF files
        pdf_files = [fc for fc in file_components
                     if fc.get("storage") == "INTERNAL_MANAGED"
                     and fc.get("visibility") in ("PUBLIC", "AUDIENCE")]
        if not pdf_files:
            pdf_files = [fc for fc in file_components
                         if fc.get("storage") == "INTERNAL_MANAGED"]

        if not pdf_files:
            print(f"  → SKIP: No INTERNAL_MANAGED files in fresh data")
            results.append({"item_id": item_id, "key": key, "doi": doi,
                            "status": "SKIP", "reason": "no_internal_files_fresh"})
            continue

        # Try downloading
        text = None
        fetch_error = None

        for fc in pdf_files:
            urls = fc.get("download_urls", [])
            for url in urls:
                print(f"  Trying: {url[:100]}...")
                with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
                    tmp_path = tmp.name
                try:
                    ok, detail = download_pdf(url, tmp_path)
                    if ok:
                        stats["pdfs_downloaded"] += 1
                        text = extract_text_from_pdf(tmp_path)
                        if text:
                            break
                        else:
                            fetch_error = "pdftotext returned empty"
                    else:
                        fetch_error = detail
                finally:
                    if os.path.exists(tmp_path):
                        os.unlink(tmp_path)
                time.sleep(0.3)
            if text:
                break

        if not text:
            error_msg = fetch_error or "No text extracted"
            print(f"  → ERROR: {error_msg}")
            results.append({"item_id": item_id, "key": key, "doi": doi,
                            "status": "ERROR", "error": error_msg[:200]})
            stats["errors"] += 1
            continue

        # Clean and validate
        text = cleanup_text(text)
        is_l3, level_str, details = validate_l3(text)

        # Save fulltext
        metadata = {"doi": doi, "source": "mpg_pure", "item_id": item_id}
        text_path = save_fulltext(key, text, metadata)

        # Update YAML
        if "full_text" not in data:
            data["full_text"] = {}
        data["full_text"]["available"] = True
        data["full_text"]["path"] = str(text_path)
        data["full_text"]["content_level"] = "L3" if is_l3 else "L2"
        data["full_text"]["format"] = "markdown"
        data["full_text"]["archived_date"] = datetime.now().strftime("%Y-%m-%d")
        data["full_text"]["word_count"] = details["word_count"]
        data["full_text"]["has_references"] = details["has_references"]
        data["full_text"]["source"] = "mpg_pure"
        data["full_text"]["pure_item_id"] = item_id

        if is_l3:
            data["l3_upgrade_date"] = datetime.now().strftime("%Y-%m-%d")
            data["l3_upgrade_method"] = "mpg_pure_fulltext_fetch_v1"

        save_paper_yaml(key, data)

        if is_l3:
            stats["l3_upgraded"] += 1
            print(f"  → L3 ✓ ({details['word_count']} words, refs={'yes' if details['has_references'] else 'no'})")
        else:
            stats["l2_partial"] += 1
            print(f"  → L2+ ({details['word_count']} words) — {level_str}")

        results.append({
            "item_id": item_id, "key": key, "doi": doi,
            "status": "L3" if is_l3 else "L2+",
            "word_count": details["word_count"],
            "has_references": details["has_references"],
        })
        time.sleep(REQUEST_DELAY)

    # Summary
    print()
    print("=" * 70)
    print("FETCH INTERNAL SUMMARY")
    print("=" * 70)
    l3_count = sum(1 for r in results if r.get("status") == "L3")
    l2_count = sum(1 for r in results if r.get("status") == "L2+")
    skip_count = sum(1 for r in results if r.get("status") == "SKIP")
    error_count = sum(1 for r in results if r.get("status") == "ERROR")
    print(f"Processed:  {processed}")
    print(f"L3 upgraded: {l3_count}")
    print(f"L2+ partial: {l2_count}")
    print(f"Skipped:     {skip_count}")
    print(f"Errors:      {error_count}")

    # Write results log
    fetch_log = {
        "run_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "mode": "fetch-internal",
        "author_filter": author_name,
        "batch": batch,
        "dry_run": dry_run,
        "processed": processed,
        "l3_upgraded": l3_count,
        "l2_partial": l2_count,
        "skipped": skip_count,
        "errors": error_count,
        "results": results,
    }
    fetch_log_path = Path("data/mpg-fulltext-fetch-log.yaml")
    with open(fetch_log_path, "w") as fp:
        yaml.dump(fetch_log, fp, default_flow_style=False, allow_unicode=True)
    print(f"\nLog written to: {fetch_log_path}")


def main():
    parser = argparse.ArgumentParser(description="Fetch full texts from MPG PuRe")
    parser.add_argument("--person-id", default="persons206813",
                        help="PuRe person ID (default: persons206813 = Sutter)")
    parser.add_argument("--name", default="sutter",
                        help="Author filter for paper database matching")
    parser.add_argument("--batch", type=int, default=50,
                        help="Max papers to process")
    parser.add_argument("--dry-run", action="store_true",
                        help="Check availability without downloading")
    parser.add_argument("--inspect", type=str, default="",
                        help="Inspect a single PuRe item ID (e.g., item_3674646)")
    parser.add_argument("--find-internal", action="store_true",
                        help="Scan ALL PuRe items for INTERNAL_MANAGED files (bypasses L2 matching)")
    parser.add_argument("--fetch-internal", action="store_true",
                        help="Download PDFs from INTERNAL_MANAGED items found by --find-internal")
    args = parser.parse_args()

    # Special mode: inspect single item
    if args.inspect:
        inspect_item(args.inspect)
        return

    # Special mode: find all INTERNAL_MANAGED files
    if args.find_internal:
        find_internal_managed(args.person_id, args.name)
        return

    # Special mode: fetch PDFs from find-internal results
    if args.fetch_internal:
        fetch_internal_managed(args.name, args.batch, args.dry_run)
        return

    print("=" * 70)
    print("MPG PuRe FULL-TEXT FETCH (Institutional Repository)")
    print("=" * 70)
    print(f"Person ID: {args.person_id}")
    print(f"Author filter: {args.name}")
    print(f"Batch size: {args.batch}")
    print(f"Dry run: {args.dry_run}")
    print()

    # Step 1: Get L2 papers that need upgrade
    print("Step 1: Loading L2 papers from database...")
    l2_papers = get_l2_papers(args.name)
    doi_papers = {k: v for k, v in l2_papers.items() if not k.startswith("title:")}
    title_papers = {k: v for k, v in l2_papers.items() if k.startswith("title:")}
    print(f"  L2 papers with DOI: {len(doi_papers)}")
    print(f"  L2 papers with title index: {len(title_papers)}")
    print()

    # Step 2: Search MPG PuRe
    print("Step 2: Searching MPG PuRe...")
    records = search_pure_by_person(args.person_id, author_name=args.name)
    stats["pure_items_found"] = len(records)
    print(f"  Total PuRe items: {len(records)}")
    print()

    # Step 3: Extract item info and match (DOI first, then title fallback)
    print("Step 3: Matching PuRe items to L2 papers...")
    matched_items = []
    diagnostic_items = []  # for log
    doi_matched = 0
    title_matched = 0

    # Build set of L2 normalized titles for fast lookup
    l2_title_set = set(title_papers.keys())

    # Diagnostic: collect first 5 PuRe normalized titles for comparison
    pure_title_samples = []

    for record in records:
        info = extract_item_info(record)
        match_type = None

        # Try DOI match first
        if info["doi"] and info["doi"] in doi_papers:
            match_type = "doi"
            doi_matched += 1
        # Fallback: title match
        elif info["title"]:
            norm_title = normalize_title(info["title"])
            title_key = f"title:{norm_title}"
            if title_key in title_papers:
                match_type = "title"
                title_matched += 1

            # Collect sample for diagnostics
            if len(pure_title_samples) < 10:
                pure_title_samples.append(title_key)

        # Diagnostic: log first 20 items regardless of match
        if len(diagnostic_items) < 20:
            doi_in_l2 = bool(info["doi"] and info["doi"] in doi_papers) if info["doi"] else False
            search_files = info.get("_search_files", [])
            diagnostic_items.append({
                "item_id": info["item_id"],
                "doi": info["doi"] or "(none)",
                "doi_in_l2": doi_in_l2,
                "title": (info["title"] or "")[:80],
                "n_files": info.get("search_file_count", 0),
                "match_type": match_type or "(none)",
                "file_types": [f.get("mimeType", "?") for f in search_files[:3]],
                "file_visibility": [f.get("visibility", "?") for f in search_files[:3]],
            })

        if match_type:
            matched_items.append(info)
            if info.get("has_files"):
                stats["items_with_files"] += 1
            info["_match_type"] = match_type

    print(f"  Matched items total: {len(matched_items)}")
    print(f"    By DOI:   {doi_matched}")
    print(f"    By title: {title_matched}")
    print(f"  Items with files in search: {stats['items_with_files']}")
    print(f"  NOTE: PuRe search doesn't always show files; Step 3b fetches each individually")
    print()

    # Step 3b: Scan storage types across ALL matched items
    # Previous runs only sampled the first 20 (oldest items, all EXTERNAL_URL).
    # Newer items often have INTERNAL_MANAGED PDFs, so we scan ALL items.
    print(f"Step 3b: Scanning storage types across ALL {len(matched_items)} matched items...")
    storage_distribution = {}  # storage_type → count
    internal_managed_items = []  # items with actual PDFs
    items_scanned = 0
    for sample_item in matched_items:
        sample_id = sample_item["item_id"]
        fresh = get_item_with_files(sample_id)
        if fresh:
            fd = fresh.get("data", fresh) if isinstance(fresh, dict) else fresh
            if isinstance(fd, dict):
                has_internal = False
                for sf in (fd.get("files", []) or []):
                    st = sf.get("storage", "unknown")
                    storage_distribution[st] = storage_distribution.get(st, 0) + 1
                    if st == "INTERNAL_MANAGED" and sf.get("visibility") in ("PUBLIC", "AUDIENCE"):
                        has_internal = True
                if has_internal:
                    internal_managed_items.append(sample_item)
        items_scanned += 1
        if items_scanned % 50 == 0:
            print(f"  ... scanned {items_scanned}/{len(matched_items)}")
        time.sleep(0.15)
    print(f"  Storage type distribution (from {items_scanned} items):")
    for st, count in sorted(storage_distribution.items()):
        print(f"    {st}: {count} files")
    print(f"  Items with INTERNAL_MANAGED + PUBLIC files: {len(internal_managed_items)}")
    print()

    # Prioritize items with INTERNAL_MANAGED files for download
    # Put them first, then the rest (EXTERNAL_URL only)
    if internal_managed_items:
        other_items = [it for it in matched_items if it not in internal_managed_items]
        matched_items = internal_managed_items + other_items
        print(f"Reordered: {len(internal_managed_items)} INTERNAL_MANAGED items first, then {len(other_items)} others")

    # Limit batch
    if args.batch > 0:
        matched_items = matched_items[:args.batch]

    # Step 4: Process each matched item
    print(f"Step 4: Processing {len(matched_items)} items...")
    print("-" * 70)

    for i, item_info in enumerate(matched_items, 1):
        print(f"\n[{i}/{len(matched_items)}] {item_info['title'][:60]}...")
        print(f"  DOI: {item_info['doi']}")
        print(f"  PuRe: {item_info['item_id']} ({item_info.get('search_file_count', '?')} files in search)")

        result = process_item(item_info, l2_papers, dry_run=args.dry_run)
        print(f"  → {result}")

        time.sleep(REQUEST_DELAY)

    # Summary
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"PuRe items found:     {stats['pure_items_found']}")
    print(f"Items with files:     {stats['items_with_files']}")
    print(f"Matched to L2:        {stats['matched_to_l2']}")
    print(f"PDFs downloaded:      {stats['pdfs_downloaded']}")
    print(f"L3 upgraded:          {stats['l3_upgraded']}")
    print(f"L2+ (partial):        {stats['l2_partial']}")
    print(f"Errors:               {stats['errors']}")
    print(f"Skipped (no match):   {stats['skipped_no_match']}")

    # Write log
    log_path = Path("data/mpg-fulltext-fetch-log.yaml")
    log = {
        "run_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "person_id": args.person_id,
        "author_filter": args.name,
        "batch_size": args.batch,
        "dry_run": args.dry_run,
        "stats": dict(stats),
        "match_stats": {
            "doi_matched": doi_matched,
            "title_matched": title_matched,
            "l2_papers_doi": len(doi_papers),
            "l2_papers_title": len(title_papers),
        },
    }
    if storage_distribution:
        log["storage_distribution"] = storage_distribution
        log["storage_items_scanned"] = items_scanned
        log["internal_managed_count"] = len(internal_managed_items)
    if paper_results:
        log["paper_details"] = paper_results
    if diagnostic_items:
        log["diagnostic_pure_items"] = diagnostic_items
    # Sample of L2 DOIs and titles for comparison
    l2_doi_sample = sorted([k for k in doi_papers.keys()])[:20]
    log["l2_doi_sample"] = l2_doi_sample
    l2_title_sample = sorted([k for k in title_papers.keys()])[:10]
    log["l2_title_sample"] = l2_title_sample
    # PuRe normalized title samples for comparison
    log["pure_title_samples"] = pure_title_samples
    # Log raw record keys — find a record WITH files for diagnostic
    if records:
        first = records[0]
        raw_keys = list(first.keys()) if isinstance(first, dict) else [str(type(first))]
        log["raw_record_keys"] = raw_keys
        data_node = first.get("data", first) if isinstance(first, dict) else {}
        if isinstance(data_node, dict):
            log["raw_data_keys"] = list(data_node.keys())
            meta = data_node.get("metadata", {})
            if isinstance(meta, dict):
                log["raw_metadata_keys"] = list(meta.keys())[:15]
                identifiers = meta.get("identifiers", [])
                log["raw_identifiers_sample"] = identifiers[:5] if identifiers else "none"

        # Find first record with files for file structure diagnostic
        file_record = None
        for r in records:
            dn = r.get("data", r) if isinstance(r, dict) else {}
            if isinstance(dn, dict) and dn.get("files"):
                file_record = dn
                break

        if file_record:
            files = file_record.get("files", [])
            log["raw_n_files_in_data"] = len(files) if isinstance(files, list) else 0
            log["raw_file_record_objectId"] = file_record.get("objectId", "")
            log["raw_file_record_versionNumber"] = file_record.get("versionNumber", "")
            if files and isinstance(files, list) and isinstance(files[0], dict):
                log["raw_first_file_keys"] = list(files[0].keys())
                log["raw_first_file_content"] = str(files[0].get("content", ""))[:300]
                log["raw_first_file_storage"] = str(files[0].get("storage", ""))[:300]
                log["raw_first_file_name"] = str(files[0].get("name", ""))[:200]
                log["raw_first_file_objectId"] = str(files[0].get("objectId", ""))[:200]
                log["raw_first_file_visibility"] = str(files[0].get("visibility", ""))[:200]
                log["raw_first_file_size"] = files[0].get("size", 0)

            # Also try fetching fresh item to compare
            fresh_obj_id = file_record.get("objectId", "")
            if fresh_obj_id:
                fresh_v = file_record.get("versionNumber", "")
                fresh_id = f"{fresh_obj_id}_{fresh_v}" if fresh_v else fresh_obj_id
                fresh = get_item_with_files(fresh_id)
                if fresh:
                    fd = fresh.get("data", fresh) if isinstance(fresh, dict) else fresh
                    if isinstance(fd, dict):
                        fresh_files = fd.get("files", [])
                        log["fresh_item_objectId"] = fd.get("objectId", "")
                        log["fresh_item_versionNumber"] = fd.get("versionNumber", "")
                        log["fresh_item_n_files"] = len(fresh_files) if isinstance(fresh_files, list) else 0
                        if fresh_files and isinstance(fresh_files, list) and isinstance(fresh_files[0], dict):
                            log["fresh_first_file_objectId"] = fresh_files[0].get("objectId", "")
                            log["fresh_first_file_name"] = fresh_files[0].get("name", "")[:200]
                            log["fresh_first_file_visibility"] = fresh_files[0].get("visibility", "")
                            log["fresh_first_file_size"] = fresh_files[0].get("size", 0)
        else:
            log["raw_n_files_in_data"] = 0
    with open(log_path, "w") as f:
        yaml.dump(log, f, default_flow_style=False, allow_unicode=True)

    print(f"\nLog written to: {log_path}")


if __name__ == "__main__":
    main()
