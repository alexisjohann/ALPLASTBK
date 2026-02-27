#!/usr/bin/env python3
"""
Fetch Paper Full Text / Abstract Automatically

Verwendet APIs um Full-Text oder Abstracts für Papers zu holen:
- CrossRef API (DOI → Abstract)
- Semantic Scholar API (Title → Abstract + Open Access PDF)
- OpenAlex API (Title → Abstract)

Usage:
    python scripts/fetch_paper_fulltext.py PAP-xxx           # Ein Paper
    python scripts/fetch_paper_fulltext.py --queue           # Alle Track B Papers
    python scripts/fetch_paper_fulltext.py --queue --limit 5 # Nur 5 Papers
"""

import os
import sys
import yaml
import json
import time
import re
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from urllib.parse import quote

ROOT = Path(__file__).parent.parent
QUEUE_FILE = ROOT / "data" / "paper-integration-queue.yaml"
FULL_TEXT_DIR = ROOT / "papers" / "evaluated" / "integrated"
BIB_FILE = ROOT / "bibliography" / "bcm_master.bib"
PIP_DIR = ROOT / "data" / "paper-intake"

# API Endpoints
CROSSREF_API = "https://api.crossref.org/works/"
SEMANTIC_SCHOLAR_API = "https://api.semanticscholar.org/graph/v1/paper/search"
OPENALEX_API = "https://api.openalex.org/works"

# Rate limiting
API_DELAY = 1.0  # seconds between API calls


def load_queue():
    """Load queue from YAML file."""
    if not QUEUE_FILE.exists():
        return {"pending": []}
    with open(QUEUE_FILE) as f:
        return yaml.safe_load(f) or {"pending": []}


def save_queue(queue):
    """Save queue to YAML file."""
    from datetime import datetime
    queue["last_updated"] = datetime.now().strftime("%Y-%m-%d")
    with open(QUEUE_FILE, "w") as f:
        yaml.dump(queue, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def get_paper_info_from_bib(paper_id: str) -> dict:
    """Extract paper info from BibTeX entry."""
    bib_key = paper_id.replace("PAP-", "")
    info = {"key": bib_key, "title": None, "doi": None, "authors": None, "year": None}

    try:
        with open(BIB_FILE) as f:
            content = f.read()

        # Find the entry
        pattern = rf"@\w+\{{{bib_key},"
        match = re.search(pattern, content)
        if not match:
            return info

        # Extract entry content
        start = match.start()
        depth = 0
        end = start
        for i, char in enumerate(content[start:], start):
            if char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break

        entry = content[start:end]

        # Extract fields
        title_match = re.search(r'title\s*=\s*\{([^}]+)\}', entry, re.IGNORECASE)
        if title_match:
            info["title"] = title_match.group(1).strip()

        doi_match = re.search(r'doi\s*=\s*\{([^}]+)\}', entry, re.IGNORECASE)
        if doi_match:
            info["doi"] = doi_match.group(1).strip()

        author_match = re.search(r'author\s*=\s*\{([^}]+)\}', entry, re.IGNORECASE)
        if author_match:
            info["authors"] = author_match.group(1).strip()

        year_match = re.search(r'year\s*=\s*\{?(\d{4})\}?', entry, re.IGNORECASE)
        if year_match:
            info["year"] = year_match.group(1)

    except Exception as e:
        print(f"  Error reading BibTeX: {e}")

    return info


def get_paper_info_from_pip(paper_id: str) -> dict:
    """Extract paper info from PIP file."""
    info = {"title": None, "doi": None, "authors": None, "year": None}

    for pip_file in PIP_DIR.rglob("*.yaml"):
        if pip_file.name == "template.yaml":
            continue
        try:
            with open(pip_file) as f:
                pip = yaml.safe_load(f)
            if pip and pip.get("paper_id") == paper_id:
                ident = pip.get("identification", {})
                info["title"] = ident.get("title")
                info["doi"] = ident.get("doi")
                info["authors"] = ", ".join(ident.get("authors", []))
                info["year"] = ident.get("year")
                return info
        except Exception:
            continue

    return info


def fetch_from_crossref(doi: str) -> dict:
    """Fetch paper data from CrossRef API."""
    result = {"abstract": None, "title": None, "source": "crossref"}

    if not doi:
        return result

    try:
        url = f"{CROSSREF_API}{quote(doi, safe='')}"
        req = Request(url, headers={"User-Agent": "EBF-Framework/1.0 (mailto:research@fehradvice.com)"})

        with urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())

        message = data.get("message", {})

        if message.get("abstract"):
            # Clean abstract (remove HTML tags)
            abstract = re.sub(r'<[^>]+>', '', message["abstract"])
            result["abstract"] = abstract.strip()

        if message.get("title"):
            result["title"] = message["title"][0] if isinstance(message["title"], list) else message["title"]

    except HTTPError as e:
        if e.code != 404:
            print(f"    CrossRef HTTP error: {e.code}")
    except Exception as e:
        print(f"    CrossRef error: {e}")

    return result


def fetch_from_semantic_scholar(title: str, authors: str = None) -> dict:
    """Fetch paper data from Semantic Scholar API."""
    result = {"abstract": None, "pdf_url": None, "source": "semantic_scholar"}

    if not title:
        return result

    try:
        # Search by title
        query = quote(title[:200])  # Limit query length
        url = f"{SEMANTIC_SCHOLAR_API}?query={query}&fields=abstract,openAccessPdf,title&limit=3"
        req = Request(url, headers={"User-Agent": "EBF-Framework/1.0"})

        with urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())

        papers = data.get("data", [])

        # Find best match
        for paper in papers:
            paper_title = paper.get("title", "").lower()
            if title.lower()[:50] in paper_title or paper_title in title.lower():
                if paper.get("abstract"):
                    result["abstract"] = paper["abstract"]
                if paper.get("openAccessPdf", {}).get("url"):
                    result["pdf_url"] = paper["openAccessPdf"]["url"]
                break

    except HTTPError as e:
        if e.code != 404:
            print(f"    Semantic Scholar HTTP error: {e.code}")
    except Exception as e:
        print(f"    Semantic Scholar error: {e}")

    return result


def fetch_from_openalex(title: str, doi: str = None) -> dict:
    """Fetch paper data from OpenAlex API."""
    result = {"abstract": None, "source": "openalex"}

    try:
        if doi:
            url = f"{OPENALEX_API}/https://doi.org/{quote(doi, safe='')}"
        elif title:
            url = f"{OPENALEX_API}?filter=title.search:{quote(title[:100])}&per_page=3"
        else:
            return result

        req = Request(url, headers={"User-Agent": "EBF-Framework/1.0 (mailto:research@fehradvice.com)"})

        with urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())

        # Handle direct DOI lookup vs search
        if doi:
            work = data
        else:
            works = data.get("results", [])
            if not works:
                return result
            # Find best match
            work = works[0]
            for w in works:
                if title.lower()[:30] in w.get("title", "").lower():
                    work = w
                    break

        # OpenAlex returns abstract as inverted index - reconstruct
        abstract_inv = work.get("abstract_inverted_index", {})
        if abstract_inv:
            # Reconstruct abstract from inverted index
            words = []
            for word, positions in abstract_inv.items():
                for pos in positions:
                    words.append((pos, word))
            words.sort()
            result["abstract"] = " ".join(w[1] for w in words)

    except HTTPError as e:
        if e.code != 404:
            print(f"    OpenAlex HTTP error: {e.code}")
    except Exception as e:
        print(f"    OpenAlex error: {e}")

    return result


def create_full_text_file(paper_id: str, info: dict, abstract: str, source: str) -> bool:
    """Create a full text file with abstract."""
    FULL_TEXT_DIR.mkdir(parents=True, exist_ok=True)

    txt_file = FULL_TEXT_DIR / f"{paper_id}.txt"

    content = f"""================================================================================
{info.get('title', paper_id)}
================================================================================

Authors: {info.get('authors', 'Unknown')}
Year: {info.get('year', 'Unknown')}
DOI: {info.get('doi', 'Not available')}

Source: Auto-fetched from {source}

================================================================================
ABSTRACT
================================================================================

{abstract}

================================================================================
EBF INTEGRATION NOTES
================================================================================

This file was automatically generated from the paper abstract.
Full text integration pending.

Key Findings:
- [To be extracted from full paper]

EBF Relevance:
- CORE Dimensions: [To be determined]
- Theory Support: [To be determined]
- Parameters: [To be determined]

================================================================================
"""

    try:
        with open(txt_file, "w") as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"  Error writing file: {e}")
        return False


def fetch_paper_fulltext(paper_id: str, verbose: bool = True) -> dict:
    """Fetch full text or abstract for a paper."""
    result = {
        "paper_id": paper_id,
        "success": False,
        "source": None,
        "abstract": None,
        "file_created": False
    }

    if verbose:
        print(f"\n📄 Processing: {paper_id}")

    # Get paper info
    info = get_paper_info_from_bib(paper_id)
    if not info.get("title"):
        pip_info = get_paper_info_from_pip(paper_id)
        info.update({k: v for k, v in pip_info.items() if v})

    if verbose:
        title = info.get('title') or 'Unknown'
        print(f"   Title: {title[:60]}...")
        print(f"   DOI: {info.get('doi') or 'Not found'}")

    abstract = None
    source = None

    # Try APIs in order of reliability

    # 1. CrossRef (if DOI available)
    if info.get("doi"):
        if verbose:
            print("   → Trying CrossRef API...")
        time.sleep(API_DELAY)
        cr_result = fetch_from_crossref(info["doi"])
        if cr_result.get("abstract"):
            abstract = cr_result["abstract"]
            source = "CrossRef"
            if verbose:
                print(f"   ✅ Found abstract via CrossRef ({len(abstract)} chars)")

    # 2. Semantic Scholar (if no abstract yet)
    if not abstract and info.get("title"):
        if verbose:
            print("   → Trying Semantic Scholar API...")
        time.sleep(API_DELAY)
        ss_result = fetch_from_semantic_scholar(info.get("title", ""), info.get("authors"))
        if ss_result.get("abstract"):
            abstract = ss_result["abstract"]
            source = "Semantic Scholar"
            if verbose:
                print(f"   ✅ Found abstract via Semantic Scholar ({len(abstract)} chars)")
        if ss_result.get("pdf_url"):
            if verbose:
                print(f"   📎 Open Access PDF available: {ss_result['pdf_url'][:50]}...")

    # 3. OpenAlex (if no abstract yet)
    if not abstract:
        if verbose:
            print("   → Trying OpenAlex API...")
        time.sleep(API_DELAY)
        oa_result = fetch_from_openalex(info.get("title"), info.get("doi"))
        if oa_result.get("abstract"):
            abstract = oa_result["abstract"]
            source = "OpenAlex"
            if verbose:
                print(f"   ✅ Found abstract via OpenAlex ({len(abstract)} chars)")

    # Create file if abstract found
    if abstract and len(abstract) > 100:  # Minimum meaningful abstract
        result["abstract"] = abstract
        result["source"] = source
        result["success"] = True

        if create_full_text_file(paper_id, info, abstract, source):
            result["file_created"] = True
            if verbose:
                print(f"   📝 Created: papers/evaluated/integrated/{paper_id}.txt")
    else:
        if verbose:
            print("   ❌ No abstract found via APIs")

    return result


def process_queue(limit: int = None, verbose: bool = True):
    """Process Track B papers from queue."""
    queue = load_queue()
    pending = queue.get("pending", [])

    # Filter to Track B only
    track_b = [p for p in pending if not p.get("has_full_text") and p.get("track") != "A"]

    if not track_b:
        print("✅ No Track B papers to process!")
        return

    if limit:
        track_b = track_b[:limit]

    print(f"\n{'='*70}")
    print(f"  FETCHING ABSTRACTS FOR {len(track_b)} TRACK B PAPERS")
    print(f"{'='*70}")

    success_count = 0

    for paper in track_b:
        paper_id = paper.get("paper_id")
        if not paper_id:
            continue

        result = fetch_paper_fulltext(paper_id, verbose)

        if result["file_created"]:
            success_count += 1

            # Update queue - move to Track A
            for item in queue.get("pending", []):
                if item.get("paper_id") == paper_id:
                    item["has_full_text"] = True
                    item["track"] = "A"
                    item["priority"] = "high"
                    item["abstract_source"] = result["source"]
                    break

    # Save updated queue
    save_queue(queue)

    print(f"\n{'='*70}")
    print(f"  SUMMARY")
    print(f"{'='*70}")
    print(f"  Processed: {len(track_b)} papers")
    print(f"  Abstracts found: {success_count}")
    print(f"  Moved to Track A: {success_count}")
    print(f"  Still Track B: {len(track_b) - success_count}")
    print()


def create_template_from_bibtex(paper_id: str, verbose: bool = True) -> bool:
    """Create a template full-text file from BibTeX info (without API fetch)."""
    info = get_paper_info_from_bib(paper_id)

    if not info.get("title"):
        pip_info = get_paper_info_from_pip(paper_id)
        info.update({k: v for k, v in pip_info.items() if v})

    if not info.get("title"):
        if verbose:
            print(f"  ❌ No title found for {paper_id}")
        return False

    FULL_TEXT_DIR.mkdir(parents=True, exist_ok=True)
    txt_file = FULL_TEXT_DIR / f"{paper_id}.txt"

    content = f"""================================================================================
{info.get('title', paper_id)}
================================================================================

Authors: {info.get('authors', 'Unknown')}
Year: {info.get('year', 'Unknown')}
DOI: {info.get('doi', 'Not available')}

Source: Template generated from BibTeX entry

================================================================================
ABSTRACT
================================================================================

[Abstract to be added - please paste from paper or fetch via DOI: {info.get('doi', 'N/A')}]

================================================================================
KEY FINDINGS
================================================================================

- [Finding 1]
- [Finding 2]
- [Finding 3]

================================================================================
METHODOLOGY
================================================================================

- Study Design: [RCT / Lab Experiment / Field Experiment / Survey / etc.]
- Sample: [N = ?, Population]
- Identification: [Strategy]

================================================================================
EBF INTEGRATION NOTES
================================================================================

CORE Dimensions:
- [To be determined]

Theory Support:
- [MS-XX-XXX codes]

Parameters:
- [Parameter estimates with SEs]

================================================================================
"""

    try:
        with open(txt_file, "w") as f:
            f.write(content)
        if verbose:
            print(f"  ✅ Created template: {txt_file.name}")
        return True
    except Exception as e:
        if verbose:
            print(f"  ❌ Error: {e}")
        return False


def process_queue_templates(limit: int = None, verbose: bool = True):
    """Create templates for Track B papers that have BibTeX entries."""
    queue = load_queue()
    pending = queue.get("pending", [])

    # Filter: Track B papers that have BibTeX info
    track_b = [p for p in pending if not p.get("has_full_text") and p.get("track") != "A"]

    if not track_b:
        print("✅ No Track B papers to process!")
        return

    if limit:
        track_b = track_b[:limit]

    print(f"\n{'='*70}")
    print(f"  CREATING TEMPLATES FOR {len(track_b)} TRACK B PAPERS")
    print(f"{'='*70}")

    success_count = 0

    for paper in track_b:
        paper_id = paper.get("paper_id")
        if not paper_id:
            continue

        if verbose:
            print(f"\n📄 {paper_id}")

        if create_template_from_bibtex(paper_id, verbose):
            success_count += 1

            # Update queue
            for item in queue.get("pending", []):
                if item.get("paper_id") == paper_id:
                    item["has_full_text"] = True
                    item["track"] = "A"
                    item["priority"] = "high"
                    item["template_created"] = True
                    break

    save_queue(queue)

    print(f"\n{'='*70}")
    print(f"  SUMMARY")
    print(f"{'='*70}")
    print(f"  Processed: {len(track_b)} papers")
    print(f"  Templates created: {success_count}")
    print(f"  Moved to Track A: {success_count}")
    print()


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Fetch Paper Full Text / Abstract")
    parser.add_argument("paper_id", nargs="?", help="Paper ID (e.g., PAP-xxx)")
    parser.add_argument("--queue", action="store_true", help="Process all Track B papers from queue")
    parser.add_argument("--templates", action="store_true", help="Create templates for papers with BibTeX (no API)")
    parser.add_argument("--limit", type=int, help="Limit number of papers to process")
    parser.add_argument("--quiet", action="store_true", help="Less verbose output")

    args = parser.parse_args()

    if args.templates:
        process_queue_templates(limit=args.limit, verbose=not args.quiet)
    elif args.queue:
        process_queue(limit=args.limit, verbose=not args.quiet)
    elif args.paper_id:
        result = fetch_paper_fulltext(args.paper_id, verbose=not args.quiet)
        if result["success"]:
            print(f"\n✅ Successfully fetched abstract for {args.paper_id}")
        else:
            print(f"\n❌ Could not fetch abstract for {args.paper_id}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
