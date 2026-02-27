#!/usr/bin/env python3
"""
Fetch Researcher Papers from MPG.PuRe (Max Planck Publication Repository)
=========================================================================
Fetches all publications for a researcher from pure.mpg.de REST API,
deduplicates against existing bcm_master.bib, and outputs new entries.

Usage:
    python scripts/fetch_mpg_pure_papers.py --person-id persons206813 --name "Sutter"
    python scripts/fetch_mpg_pure_papers.py --orcid 0000-0002-6143-8406 --name "Sutter"
    python scripts/fetch_mpg_pure_papers.py --estimate-time 500

API Docs: https://colab.mpdl.mpg.de/mediawiki/PubMan_REST_API_Documentation

Rate Limits & Time Estimation:
    MPG PuRe:   No documented limit. We use 0.5s between pages (25 items/page).
    OpenAlex:   ~10 req/sec polite pool (with mailto: header). We use 0.12s delay.
    Formula:    T = ceil(N/25) * 0.5 + N_doi * 0.12 + 60s overhead
    Example:    500 papers ≈ 20*0.5 + 350*0.12 + 60 = 112s ≈ 2 min
    Registry:   data/api-registry.yaml (API-BIB-002, API-BIB-005)
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: requests not installed. Run: pip install requests")
    sys.exit(1)

PURE_BASE = "https://pure.mpg.de/rest"
BIB_PATH = "bibliography/bcm_master.bib"
REGISTRY_PATH = "data/researcher-registry.yaml"


def search_pure_by_person(person_id: str, size: int = 50) -> list:
    """Search PuRe by person identifier (e.g., persons206813).

    PuRe uses CoNE (Control of Named Entities) identifiers.
    The full path format is: /persons/resource/persons206813
    We accept both short ('persons206813') and full path formats.
    """
    url = f"{PURE_BASE}/items/search"

    # Normalize person_id to full CoNE path
    if not person_id.startswith("/"):
        person_id_full = f"/persons/resource/{person_id}"
    else:
        person_id_full = person_id

    # Try multiple identifier formats (PuRe is inconsistent)
    id_variants = [person_id_full, person_id, person_id.replace("persons", "")]

    query = {
        "query": {
            "bool": {
                "should": [
                    {
                        "term": {
                            "metadata.creators.person.identifier.id": {
                                "value": variant
                            }
                        }
                    }
                    for variant in id_variants
                ],
                "minimum_should_match": 1
            }
        }
    }

    print(f"  Query variants: {id_variants}")

    all_records = []
    offset = 0
    scroll_id = None

    while True:
        if offset == 0:
            resp = requests.post(url, json=query, params={"format": "json", "size": size})
        else:
            # Use scroll for subsequent pages
            resp = requests.get(
                f"{PURE_BASE}/items/search",
                params={"format": "json", "size": size, "scrollId": scroll_id}
            )

        if resp.status_code != 200:
            print(f"  API returned {resp.status_code}: {resp.text[:200]}")
            break

        data = resp.json()

        # Handle different response structures
        if isinstance(data, dict):
            records = data.get("records", data.get("list", []))
            total = data.get("numberOfRecords", data.get("total", 0))
            scroll_id = data.get("scrollId")
        elif isinstance(data, list):
            records = data
            total = len(records)
            scroll_id = None
        else:
            break

        if not records:
            break

        all_records.extend(records)
        print(f"  Fetched {len(all_records)}/{total} records...")

        if len(all_records) >= total or not scroll_id:
            break

        time.sleep(0.5)  # Be polite

    return all_records


def search_pure_by_orcid(orcid: str, size: int = 50) -> list:
    """Search PuRe by ORCID.

    Tries multiple ORCID formats since PuRe stores them inconsistently:
    - Plain: 0000-0002-6143-8406
    - URL: https://orcid.org/0000-0002-6143-8406
    - http variant
    """
    url = f"{PURE_BASE}/items/search"

    # Try multiple ORCID formats
    orcid_clean = orcid.replace("https://orcid.org/", "").replace("http://orcid.org/", "")
    orcid_variants = [
        orcid_clean,
        f"https://orcid.org/{orcid_clean}",
        f"http://orcid.org/{orcid_clean}",
    ]

    query = {
        "query": {
            "bool": {
                "should": [
                    {
                        "term": {
                            "metadata.creators.person.identifier.id": {
                                "value": variant
                            }
                        }
                    }
                    for variant in orcid_variants
                ],
                "minimum_should_match": 1
            }
        }
    }

    print(f"  ORCID variants: {orcid_variants}")

    all_records = []
    offset = 0
    scroll_id = None

    while True:
        if offset == 0:
            resp = requests.post(url, json=query, params={"format": "json", "size": size})
        else:
            resp = requests.get(url, params={"format": "json", "scrollId": scroll_id})

        if resp.status_code != 200:
            print(f"  API returned {resp.status_code}, trying name-based search...")
            break

        data = resp.json()

        if isinstance(data, dict):
            records = data.get("records", data.get("list", []))
            total = data.get("numberOfRecords", data.get("total", 0))
            scroll_id = data.get("scrollId")
        elif isinstance(data, list):
            records = data
            total = len(records)
            scroll_id = None
        else:
            break

        if not records:
            break

        all_records.extend(records)
        print(f"  Fetched {len(all_records)}/{total} records...")

        if len(all_records) >= total or not scroll_id:
            break

        time.sleep(0.5)

    return all_records


def fetch_abstract_openalex(doi: str) -> str:
    """Fetch abstract for a single paper from OpenAlex by DOI."""
    if not doi:
        return ""
    try:
        import urllib.request
        import urllib.parse
        encoded = urllib.parse.quote(doi, safe="")
        url = f"https://api.openalex.org/works/doi:{encoded}?select=abstract_inverted_index"
        req = urllib.request.Request(url)
        req.add_header("User-Agent", "EBF-Framework/1.0 (mailto:research@fehradvice.com)")
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        inv_idx = data.get("abstract_inverted_index")
        if not inv_idx:
            return ""
        # Reconstruct text from inverted index
        word_pos = []
        for word, positions in inv_idx.items():
            for pos in positions:
                word_pos.append((pos, word))
        word_pos.sort()
        return " ".join(w for _, w in word_pos)
    except Exception:
        return ""


def search_openalex_fallback(orcid: str, name: str, first_name: str = "") -> list:
    """Fallback: Fetch from OpenAlex API (free, no key needed).

    Uses ORCID as strict primary filter. Name search is only used
    if ORCID fails, and results are filtered by first_name.
    """
    print(f"\n  Trying OpenAlex fallback for ORCID {orcid}...")

    headers = {"User-Agent": "mailto:research@fehradvice.com"}
    author = None

    # Step 1a: Find author by ORCID (strict — preferred)
    for orcid_format in [f"https://orcid.org/{orcid}", orcid]:
        url = f"https://api.openalex.org/authors/orcid:{orcid_format}"
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            author = resp.json()
            print(f"  ORCID match: {author.get('display_name')}")
            break

    # Step 1b: Only if ORCID fails, try name search with verification
    if not author:
        print(f"  ORCID lookup failed. Trying name search for '{name}'...")
        url = f"https://api.openalex.org/authors?search={name}"
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            print(f"  OpenAlex author search failed: {resp.status_code}")
            return []
        results = resp.json().get("results", [])
        if not results:
            print(f"  No author found for '{name}'")
            return []

        # Filter by first name if provided
        if first_name:
            for r in results:
                display = r.get("display_name", "")
                if first_name.lower() in display.lower() and name.lower() in display.lower():
                    author = r
                    print(f"  Name match: {display}")
                    break
        if not author:
            author = results[0]
            print(f"  WARNING: Using first result: {author.get('display_name')} (verify manually!)")

    author_id = author.get("id", "").split("/")[-1]
    works_count = author.get("works_count", 0)
    display_name = author.get("display_name", "")
    print(f"  Found: {display_name} ({author_id}), {works_count} works")

    # Verify the author matches expectations
    if name.lower() not in display_name.lower():
        print(f"  ERROR: Author '{display_name}' doesn't match '{name}'. Aborting.")
        return []

    # Step 2: Fetch all works
    all_works = []
    page = 1
    per_page = 200

    while True:
        works_url = (
            f"https://api.openalex.org/works"
            f"?filter=authorships.author.id:{author_id}"
            f"&per-page={per_page}&page={page}"
            f"&select=id,title,publication_year,doi,type,"
            f"authorships,primary_location,cited_by_count"
        )

        resp = requests.get(works_url, headers=headers)
        if resp.status_code != 200:
            print(f"  Works fetch failed at page {page}: {resp.status_code}")
            break

        data = resp.json()
        works = data.get("results", [])

        if not works:
            break

        all_works.extend(works)
        print(f"  Fetched {len(all_works)}/{works_count} works...")

        if len(all_works) >= works_count:
            break

        page += 1
        time.sleep(0.3)

    return all_works


def extract_from_pure_record(record: dict) -> dict:
    """Extract paper metadata from a PuRe JSON record."""
    meta = record.get("metadata", record.get("data", record))

    # Try different field structures
    title = (
        meta.get("title", "")
        or meta.get("metadata", {}).get("title", "")
        or ""
    )

    creators = meta.get("creators", meta.get("metadata", {}).get("creators", []))
    authors = []
    for c in creators:
        person = c.get("person", {})
        family = person.get("familyName", "")
        given = person.get("givenName", "")
        if family:
            authors.append(f"{family}, {given}")

    year = str(
        meta.get("datePublishedInPrint", "")
        or meta.get("datePublishedOnline", "")
        or meta.get("dateCreated", "")
    )[:4]

    # Source (journal)
    sources = meta.get("sources", meta.get("metadata", {}).get("sources", []))
    journal = ""
    if sources and isinstance(sources, list):
        journal = sources[0].get("title", "") if isinstance(sources[0], dict) else str(sources[0])

    # DOI
    identifiers = meta.get("identifiers", meta.get("metadata", {}).get("identifiers", []))
    doi = ""
    for ident in identifiers:
        if isinstance(ident, dict) and ident.get("type") == "DOI":
            doi = ident.get("id", "")

    return {
        "title": title,
        "authors": authors,
        "year": year,
        "journal": journal,
        "doi": doi,
        "source": "pure.mpg.de",
    }


def extract_from_openalex(work: dict) -> dict:
    """Extract paper metadata from an OpenAlex work."""
    title = work.get("title", "")

    authors = []
    for authorship in work.get("authorships", []):
        name = authorship.get("author", {}).get("display_name", "")
        if name:
            parts = name.split()
            if len(parts) >= 2:
                authors.append(f"{parts[-1]}, {' '.join(parts[:-1])}")
            else:
                authors.append(name)

    year = str(work.get("publication_year", ""))

    journal = ""
    loc = work.get("primary_location", {})
    if loc and loc.get("source"):
        journal = loc["source"].get("display_name", "")

    doi = (work.get("doi") or "").replace("https://doi.org/", "")

    return {
        "title": title,
        "authors": authors,
        "year": year,
        "journal": journal,
        "doi": doi,
        "cited_by_count": work.get("cited_by_count", 0),
        "source": "openalex.org",
    }


def generate_bibtex_key(paper: dict, target_name: str) -> str:
    """Generate a BibTeX key: nachnamejahrkurzwort."""
    # Find target author's last name
    last_name = target_name.lower()
    for a in paper.get("authors", []):
        if target_name.lower() in a.lower():
            last_name = a.split(",")[0].strip().lower()
            break

    year = paper.get("year", "0000")[:4]

    # Short word from title
    title = paper.get("title", "unknown")
    stop_words = {"the", "a", "an", "of", "in", "on", "for", "and", "to", "with", "is", "are", "do", "does", "how", "why", "what", "when", "where"}
    words = re.findall(r'[a-z]+', title.lower())
    short = "unknown"
    for w in words:
        if w not in stop_words and len(w) > 2:
            short = w
            break

    # Clean special characters
    last_name = re.sub(r'[^a-z]', '', last_name)

    return f"{last_name}{year}{short}"


def load_existing_keys(bib_path: str) -> set:
    """Load existing BibTeX keys from bcm_master.bib."""
    keys = set()
    if not os.path.exists(bib_path):
        return keys

    with open(bib_path, 'r', encoding='utf-8') as f:
        for line in f:
            m = re.match(r'@\w+\{(\w+),', line)
            if m:
                keys.add(m.group(1))
    return keys


def load_existing_titles(bib_path: str) -> set:
    """Load existing titles (lowercase) for dedup."""
    titles = set()
    if not os.path.exists(bib_path):
        return titles

    with open(bib_path, 'r', encoding='utf-8') as f:
        for line in f:
            m = re.match(r'\s*title\s*=\s*\{(.+?)\}', line, re.IGNORECASE)
            if m:
                titles.add(m.group(1).lower().strip().rstrip(','))
    return titles


def paper_to_bibtex(paper: dict, key: str, researcher_lit: str) -> str:
    """Convert paper dict to BibTeX entry."""
    authors_str = " and ".join(paper.get("authors", ["Unknown"]))
    title = paper.get("title", "Unknown")
    journal = paper.get("journal", "")
    year = paper.get("year", "")
    doi = paper.get("doi", "")

    entry_type = "article" if journal else "misc"

    lines = [
        f"@{entry_type}{{{key},",
        f"  title = {{{title}}},",
        f"  author = {{{authors_str}}},",
        f"  year = {{{year}}},",
    ]

    if journal:
        lines.append(f"  journal = {{{journal}}},")
    if doi:
        lines.append(f"  doi = {{{doi}}},")

    # Abstract (fetched from OpenAlex during import)
    abstract = paper.get("abstract", "")
    if abstract:
        # Sanitize for BibTeX
        abstract = abstract.replace("{", "\\{").replace("}", "\\}")
        abstract = abstract.replace("&", "\\&").replace("%", "\\%")
        abstract = abstract.replace("$", "\\$").replace("#", "\\#")
        abstract = abstract.replace("_", "\\_")
        abstract = re.sub(r'\s+', ' ', abstract).strip()
        lines.append(f"  abstract = {{{abstract}}},")

    # EBF fields
    lines.append(f"  % === EVIDENCE CLASSIFICATION ===")
    lines.append(f"  evidence_tier = {{2}},")
    lines.append(f"  use_for = {{LIT-{researcher_lit}}},")
    lines.append(f"  identification = {{auto_imported_mpg_pure}},")
    lines.append(f"  external_validity = {{pending_review}}")
    lines.append(f"}}")

    return "\n".join(lines)


##############################################################################
# EXPERIMENTAL MODE: Geometric Scaling (1 → 10 → 100 → all)
##############################################################################
# Principle: Never process everything at once. Scale geometrically and
# validate quality at each stage. Stop early if quality drops.
# See: CLAUDE.md → "Experiment-First Coding (Anti-Tilt Prinzip)"
##############################################################################

DEFAULT_STAGES = [1, 10, 100, 0]  # 0 = all remaining


def compute_quality_metrics(papers: list) -> dict:
    """Compute quality metrics for a batch of papers."""
    n = max(len(papers), 1)
    with_doi = sum(1 for p in papers if p.get("doi"))
    with_journal = sum(1 for p in papers if p.get("journal"))
    with_abstract = sum(1 for p in papers if p.get("abstract"))
    with_year = sum(1 for p in papers if p.get("year"))

    return {
        "total": len(papers),
        "with_doi": with_doi,
        "with_doi_pct": with_doi / n * 100,
        "with_journal": with_journal,
        "with_journal_pct": with_journal / n * 100,
        "with_abstract": with_abstract,
        "with_abstract_pct": with_abstract / n * 100,
        "with_year": with_year,
        "content_level": "L1" if with_abstract > n * 0.5 else "L0",
    }


def print_stage_report(stage_num: int, stage_size: int, metrics: dict,
                       elapsed: float, problems: list):
    """Print quality report for one experimental stage."""
    w = 56  # inner width

    def row(text):
        text = text[:w]
        print(f"  │  {text}{' ' * (w - len(text))}│")

    print()
    print(f"  ┌{'─' * (w + 2)}┐")
    row(f"STAGE {stage_num}: {metrics['total']} papers ({elapsed:.1f}s)")
    print(f"  ├{'─' * (w + 2)}┤")
    row(f"DOI:        {metrics['with_doi']:>4}/{metrics['total']}"
        f"  ({metrics['with_doi_pct']:>5.1f}%)")
    row(f"Journal:    {metrics['with_journal']:>4}/{metrics['total']}"
        f"  ({metrics['with_journal_pct']:>5.1f}%)")
    row(f"Abstract:   {metrics['with_abstract']:>4}/{metrics['total']}"
        f"  ({metrics['with_abstract_pct']:>5.1f}%)")
    row(f"Content:    {metrics['content_level']}")

    if problems:
        print(f"  ├{'─' * (w + 2)}┤")
        for p in problems:
            row(f"⚠ {p}")

    print(f"  └{'─' * (w + 2)}┘")


def check_quality_gates(metrics: dict, prev_metrics: dict = None) -> list:
    """Check quality gates. Return list of problems (empty = OK)."""
    problems = []

    # Gate 1: DOI coverage should be > 30%
    if metrics["total"] >= 5 and metrics["with_doi_pct"] < 30:
        problems.append(f"LOW DOI: {metrics['with_doi_pct']:.0f}% (expect >30%)")

    # Gate 2: If we had abstracts before, coverage shouldn't drop > 20pp
    if prev_metrics and prev_metrics["with_abstract_pct"] > 0:
        drop = prev_metrics["with_abstract_pct"] - metrics["with_abstract_pct"]
        if drop > 20:
            problems.append(
                f"ABSTRACT DROP: {prev_metrics['with_abstract_pct']:.0f}%"
                f" → {metrics['with_abstract_pct']:.0f}% (-{drop:.0f}pp)")

    # Gate 3: Papers should have years
    if metrics["total"] >= 5 and metrics["with_year"] < metrics["total"] * 0.5:
        problems.append(f"MISSING YEARS: {metrics['total'] - metrics['with_year']} papers without year")

    return problems


def run_experimental_stages(papers: list, stages: list, args,
                            existing_keys: set, existing_titles: list,
                            source: str) -> tuple:
    """Run pipeline in geometric stages with quality gates.

    Returns (all_bibtex_entries, all_new_papers, stage_reports).
    """
    all_entries = []
    all_new_papers = []
    stage_reports = []
    prev_metrics = None
    used_keys = set(existing_keys)
    processed = 0
    stopped_early = False

    print(f"\n{'=' * 60}")
    print(f"  EXPERIMENTAL MODE: {len(stages)} stages")
    print(f"  Stages: {' → '.join(str(s) if s > 0 else 'ALL' for s in stages)}")
    print(f"  Total available: {len(papers)} papers")
    print(f"{'=' * 60}")

    for stage_idx, stage_size in enumerate(stages):
        stage_num = stage_idx + 1

        # Determine batch for this stage
        if stage_size == 0:
            # "all" = everything remaining
            batch = papers[processed:]
            stage_label = f"ALL ({len(batch)})"
        else:
            # Take next N papers (cumulative)
            end = min(processed + stage_size, len(papers))
            batch = papers[processed:end]
            stage_label = str(stage_size)

        if not batch:
            print(f"\n  Stage {stage_num}: No papers remaining. Done.")
            break

        print(f"\n  Stage {stage_num}: Processing {len(batch)} papers"
              f" (of {len(papers)} total)...")

        t_start = time.time()

        # Process this batch: dedup + abstract fetch + BibTeX generation
        stage_new = []
        stage_entries = []

        for paper in batch:
            title = paper.get("title", "")
            if not title:
                continue

            # Check against existing
            title_clean = re.sub(r'[^a-z0-9 ]', '', title.lower()).strip()
            is_dup = False
            for existing in existing_titles:
                existing_clean = re.sub(r'[^a-z0-9 ]', '', existing.lower()).strip()
                if title_clean == existing_clean:
                    is_dup = True
                    break
                if len(title_clean) > 20 and title_clean[:40] == existing_clean[:40]:
                    is_dup = True
                    break
            if is_dup:
                continue

            # Also check against papers we've already added in previous stages
            already_added = False
            for prev in all_new_papers:
                prev_clean = re.sub(r'[^a-z0-9 ]', '', prev.get("title", "").lower()).strip()
                if title_clean == prev_clean:
                    already_added = True
                    break
            if already_added:
                continue

            # Fetch abstract if missing
            if paper.get("doi") and not paper.get("abstract"):
                abstract = fetch_abstract_openalex(paper["doi"])
                if abstract:
                    paper["abstract"] = abstract
                time.sleep(0.12)

            stage_new.append(paper)

            # Generate BibTeX
            key = generate_bibtex_key(paper, args.name)
            base_key = key
            counter = 1
            while key in used_keys:
                key = f"{base_key}{chr(96 + counter)}"
                counter += 1
            used_keys.add(key)

            entry = paper_to_bibtex(paper, key, args.lit)
            stage_entries.append(entry)

        elapsed = time.time() - t_start

        # Quality metrics for this stage's NEW papers
        metrics = compute_quality_metrics(stage_new)

        # Check quality gates
        problems = check_quality_gates(metrics, prev_metrics)

        # Print stage report
        print_stage_report(stage_num, len(batch), metrics, elapsed, problems)

        # Record
        stage_reports.append({
            "stage": stage_num,
            "batch_size": len(batch),
            "new_papers": len(stage_new),
            "metrics": metrics,
            "problems": problems,
            "elapsed_s": elapsed,
        })

        all_entries.extend(stage_entries)
        all_new_papers.extend(stage_new)
        processed += len(batch)
        prev_metrics = metrics

        # Quality gate: STOP if critical problems and not last stage
        critical = [p for p in problems if "LOW DOI" in p or "DROP" in p]
        if critical and stage_size != 0:
            print(f"\n  ⚠ QUALITY GATE: Stopping after stage {stage_num}.")
            print(f"    Problems: {'; '.join(critical)}")
            print(f"    Fix issues before running next stage.")
            print(f"    Use --batch {processed + stage_size} to continue.")
            stopped_early = True
            break

    # Final summary
    print(f"\n{'=' * 60}")
    print(f"  EXPERIMENTAL SUMMARY")
    print(f"{'=' * 60}")
    print(f"  Stages completed:  {len(stage_reports)}"
          f"{'  (STOPPED EARLY)' if stopped_early else ''}")
    print(f"  Papers processed:  {processed}/{len(papers)}")
    print(f"  New papers:        {len(all_new_papers)}")
    total_time = sum(r["elapsed_s"] for r in stage_reports)
    print(f"  Total time:        {total_time:.1f}s")
    if all_new_papers:
        final = compute_quality_metrics(all_new_papers)
        print(f"  Final DOI:         {final['with_doi_pct']:.0f}%")
        print(f"  Final abstract:    {final['with_abstract_pct']:.0f}%")
        print(f"  Content level:     {final['content_level']}")
    print(f"{'=' * 60}")

    return all_entries, all_new_papers, stage_reports


def estimate_pipeline_time(n_papers: int):
    """Estimate total pipeline runtime for N papers.

    Rate limits (from data/api-registry.yaml):
        MPG PuRe (API-BIB-005): No documented limit. We use 0.5s/page (25 items/page).
        OpenAlex (API-BIB-002): ~10 req/sec polite pool. We use 0.12s/request.

    Formula:
        T_total = T_pagination + T_abstracts + T_overhead
        T_pagination = ceil(N / 25) * 0.5s
        T_abstracts  = N_with_doi * 0.12s  (assume ~70% have DOIs)
        T_overhead   = 60s (setup, dedup, BibTeX generation, commit)
    """
    import math

    pages = math.ceil(n_papers / 25)
    n_with_doi = int(n_papers * 0.70)  # ~70% have DOIs
    t_pagination = pages * 0.5
    t_abstracts = n_with_doi * 0.12
    t_overhead = 60
    t_total = t_pagination + t_abstracts + t_overhead

    print(f"{'=' * 60}")
    print(f"  TIME ESTIMATION: {n_papers} papers")
    print(f"{'=' * 60}")
    print()
    print(f"  Rate Limits:")
    print(f"    MPG PuRe:   0.5s/page (25 items/page) — no documented limit")
    print(f"    OpenAlex:   0.12s/request (~8 req/s, polite pool with mailto:)")
    print()
    print(f"  Components:")
    print(f"    Pagination:    {pages:>4} pages × 0.5s  = {t_pagination:>6.1f}s")
    print(f"    Abstracts:     {n_with_doi:>4} DOIs × 0.12s = {t_abstracts:>6.1f}s")
    print(f"    Overhead:      setup + dedup + write   = {t_overhead:>6.1f}s")
    print(f"    {'─' * 46}")
    print(f"    Total:                                 = {t_total:>6.1f}s")
    print()
    minutes = t_total / 60
    if minutes < 1:
        print(f"  Estimated time: ~{t_total:.0f} seconds")
    else:
        print(f"  Estimated time: ~{minutes:.1f} minutes")
    print()
    print(f"  Notes:")
    print(f"    - Abstract fetch assumes ~70% of papers have DOIs")
    print(f"    - OpenAlex 429 (rate limit) adds ~2-8s per occurrence")
    print(f"    - Self-dedup typically removes ~30% of fetched papers")
    print(f"    - Measured: 531 Sutter papers took ~9 min total (2026-02-18)")
    print()
    print(f"  Registry: data/api-registry.yaml (API-BIB-002, API-BIB-005)")
    print(f"{'=' * 60}")


def main():
    parser = argparse.ArgumentParser(description="Fetch papers from MPG.PuRe")
    parser.add_argument("--person-id", default="persons206813",
                        help="PuRe person ID (default: persons206813 = Sutter)")
    parser.add_argument("--orcid", default="0000-0002-6143-8406",
                        help="ORCID (default: Sutter)")
    parser.add_argument("--name", default="Sutter",
                        help="Researcher last name for key generation")
    parser.add_argument("--first-name", default="Matthias",
                        help="Researcher first name for author verification")
    parser.add_argument("--lit", default="SUT",
                        help="LIT-Appendix code (default: SUT)")
    parser.add_argument("--output", default="new_papers_bibtex.bib",
                        help="Output file for new BibTeX entries")
    parser.add_argument("--dry-run", action="store_true",
                        help="Don't write files, just report")
    parser.add_argument("--append-to-bib", action="store_true",
                        help="Append new entries directly to bcm_master.bib")
    parser.add_argument("--experimental", action="store_true",
                        help="Run in experimental mode: 1 → 10 → 100 → all with quality gates")
    parser.add_argument("--stages", type=str, default=None,
                        help="Custom stages (comma-separated, 0=all). Default: 1,10,100,0")
    parser.add_argument("--estimate-time", type=int, metavar="N",
                        help="Estimate runtime for N papers and exit")
    args = parser.parse_args()

    # Time estimation mode
    if args.estimate_time is not None:
        estimate_pipeline_time(args.estimate_time)
        return

    print(f"=" * 60)
    print(f"MPG.PuRe Paper Fetcher")
    print(f"=" * 60)
    print(f"Researcher: {args.name}")
    print(f"Person ID:  {args.person_id}")
    print(f"ORCID:      {args.orcid}")
    print(f"LIT:        LIT-{args.lit}")
    print()

    # Step 1: Load existing papers
    print("Step 1: Loading existing bibliography...")
    existing_keys = load_existing_keys(BIB_PATH)
    existing_titles = load_existing_titles(BIB_PATH)
    print(f"  Found {len(existing_keys)} existing BibTeX keys")
    print(f"  Found {len(existing_titles)} existing titles")

    # Step 2: Try PuRe API
    print(f"\nStep 2: Fetching from MPG.PuRe (person: {args.person_id})...")
    records = search_pure_by_person(args.person_id)

    papers = []
    source = "pure.mpg.de"

    if records:
        print(f"  Got {len(records)} records from PuRe")
        for r in records:
            paper = extract_from_pure_record(r)
            if paper.get("title"):
                papers.append(paper)
    else:
        # Step 2b: Try ORCID-based search
        print(f"\n  PuRe person-id search returned 0. Trying ORCID...")
        records = search_pure_by_orcid(args.orcid)

        if records:
            print(f"  Got {len(records)} records from PuRe (ORCID)")
            for r in records:
                paper = extract_from_pure_record(r)
                if paper.get("title"):
                    papers.append(paper)

    if not papers:
        # Step 2c: OpenAlex fallback
        print(f"\n  PuRe returned 0 results. Trying OpenAlex fallback...")
        works = search_openalex_fallback(args.orcid, args.name, args.first_name)
        source = "openalex.org"

        if works:
            for w in works:
                paper = extract_from_openalex(w)
                if paper.get("title"):
                    papers.append(paper)

    if not papers:
        print("\n  ERROR: No papers found from any source.")
        sys.exit(1)

    print(f"\n  Total papers fetched: {len(papers)} (source: {source})")

    rejected = 0  # Track author filter rejections
    self_dupes = 0  # Track self-duplicates

    # Parse custom stages if provided
    if args.stages:
        stages = [int(s.strip()) for s in args.stages.split(",")]
    else:
        stages = list(DEFAULT_STAGES)

    # Step 2d: Post-fetch author verification
    # Only keep papers where the target researcher is actually a (co-)author
    if source == "openalex.org":
        verified_papers = []
        name_lower = args.name.lower()
        for paper in papers:
            authors_str = " ".join(paper.get("authors", [])).lower()
            if name_lower in authors_str:
                verified_papers.append(paper)
        rejected = len(papers) - len(verified_papers)  # noqa: used in summary
        if rejected > 0:
            print(f"  Author filter: kept {len(verified_papers)}, rejected {rejected} (wrong {args.name})")
        papers = verified_papers

    # Step 2e: Self-deduplication (LEARNING: OpenAlex returns Working Paper +
    # Journal + Preprint versions of the same paper → 31% duplicates in Sutter import)
    print(f"\nStep 2e: Self-deduplication (removing WP/preprint duplicates)...")
    seen_titles = {}  # normalized_title -> best paper
    for paper in papers:
        title = paper.get("title", "")
        if not title:
            continue
        title_norm = re.sub(r'[^a-z0-9 ]', '', title.lower()).strip()
        title_norm = re.sub(r'\s+', ' ', title_norm)

        if title_norm in seen_titles:
            existing = seen_titles[title_norm]
            # Keep the one with: journal > no journal, DOI > no DOI, later year
            new_score = (
                (10 if paper.get("journal") else 0) +
                (5 if paper.get("doi") else 0) +
                (int(paper.get("year", "0")[:4]) if paper.get("year") else 0)
            )
            old_score = (
                (10 if existing.get("journal") else 0) +
                (5 if existing.get("doi") else 0) +
                (int(existing.get("year", "0")[:4]) if existing.get("year") else 0)
            )
            if new_score > old_score:
                seen_titles[title_norm] = paper
        else:
            seen_titles[title_norm] = paper

    self_dupes = len(papers) - len(seen_titles)
    if self_dupes > 0:
        print(f"  Removed {self_dupes} self-duplicates (WP/preprint versions)")
        print(f"  Kept {len(seen_titles)} unique papers")
    papers = list(seen_titles.values())

    # =========================================================================
    # EXPERIMENTAL MODE: Route through staged pipeline
    # =========================================================================
    if args.experimental:
        bibtex_entries, new_papers, stage_reports = run_experimental_stages(
            papers=papers,
            stages=stages,
            args=args,
            existing_keys=existing_keys,
            existing_titles=existing_titles,
            source=source,
        )

        if not new_papers:
            print("\n  No new papers to add.")
            with open(args.output, 'w') as f:
                f.write(f"% No new papers found for {args.name}\n")
            summary = {
                "researcher": args.name, "source": source,
                "mode": "experimental", "new_papers": 0,
                "stages": [{"stage": r["stage"], "new": r["new_papers"]}
                           for r in stage_reports],
            }
            with open("fetch_summary.json", "w") as f:
                json.dump(summary, f, indent=2)
            return

        # Write output (same as traditional mode)
        if not args.dry_run:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(f"%==============================================================================\n")
                f.write(f"% AUTO-IMPORTED: {args.name} papers from {source}\n")
                f.write(f"% Date: {time.strftime('%Y-%m-%d')}\n")
                f.write(f"% Mode: EXPERIMENTAL ({len(stage_reports)} stages)\n")
                f.write(f"% Total new: {len(bibtex_entries)}\n")
                f.write(f"%==============================================================================\n\n")
                for entry in bibtex_entries:
                    f.write(entry + "\n\n")
            print(f"\n  Written to: {args.output}")

            if args.append_to_bib:
                with open(BIB_PATH, 'a', encoding='utf-8') as f:
                    f.write(f"\n%==============================================================================\n")
                    f.write(f"% AUTO-IMPORTED: {args.name} papers from {source}\n")
                    f.write(f"% Date: {time.strftime('%Y-%m-%d')}\n")
                    f.write(f"%==============================================================================\n\n")
                    for entry in bibtex_entries:
                        f.write(entry + "\n\n")
                print(f"  Appended to: {BIB_PATH}")
        else:
            print(f"\n  DRY RUN - Would write {len(bibtex_entries)} entries")
            for entry in bibtex_entries[:3]:
                print(f"\n{entry}")
            if len(bibtex_entries) > 3:
                print(f"\n  ... and {len(bibtex_entries) - 3} more")

        # Summary with stage data
        final_metrics = compute_quality_metrics(new_papers)
        summary = {
            "researcher": args.name,
            "source": source,
            "mode": "experimental",
            "total_fetched_raw": len(papers) + self_dupes,
            "self_duplicates_removed": self_dupes,
            "new_papers": len(new_papers),
            "stages_completed": len(stage_reports),
            "stages": [
                {
                    "stage": r["stage"],
                    "batch": r["batch_size"],
                    "new": r["new_papers"],
                    "doi_pct": f"{r['metrics']['with_doi_pct']:.0f}%",
                    "abstract_pct": f"{r['metrics']['with_abstract_pct']:.0f}%",
                    "time_s": f"{r['elapsed_s']:.1f}",
                    "problems": r["problems"],
                }
                for r in stage_reports
            ],
            "quality_metrics": {
                "with_doi_pct": f"{final_metrics['with_doi_pct']:.0f}%",
                "with_journal_pct": f"{final_metrics['with_journal_pct']:.0f}%",
                "with_abstract_pct": f"{final_metrics['with_abstract_pct']:.0f}%",
                "content_level": final_metrics["content_level"],
            },
        }
        with open("fetch_summary.json", "w") as f:
            json.dump(summary, f, indent=2)

        return

    # =========================================================================
    # TRADITIONAL MODE: Process all at once (original behavior)
    # =========================================================================

    # Step 3: Deduplicate against existing bibliography
    print(f"\nStep 3: Deduplicating against existing bib...")
    new_papers = []
    skipped_existing = 0
    skipped_no_title = 0

    for paper in papers:
        title = paper.get("title", "")
        if not title:
            skipped_no_title += 1
            continue

        # Check title similarity (lowercase, strip punctuation)
        title_clean = re.sub(r'[^a-z0-9 ]', '', title.lower()).strip()
        is_dup = False

        for existing in existing_titles:
            existing_clean = re.sub(r'[^a-z0-9 ]', '', existing.lower()).strip()
            if title_clean == existing_clean:
                is_dup = True
                break
            # Also check substring match (>80% overlap)
            if len(title_clean) > 20 and title_clean[:40] == existing_clean[:40]:
                is_dup = True
                break

        if is_dup:
            skipped_existing += 1
        else:
            new_papers.append(paper)

    print(f"  Already in bib:  {skipped_existing}")
    print(f"  No title:        {skipped_no_title}")
    print(f"  NEW papers:      {len(new_papers)}")

    if not new_papers:
        print("\n  No new papers to add.")
        # Write empty output for GitHub Action
        with open(args.output, 'w') as f:
            f.write(f"% No new papers found for {args.name}\n")

        # Write summary
        summary = {
            "researcher": args.name,
            "source": source,
            "mode": "traditional",
            "total_fetched": len(papers),
            "already_existing": skipped_existing,
            "new_papers": 0,
        }
        with open("fetch_summary.json", "w") as f:
            json.dump(summary, f, indent=2)

        return

    # Step 4: Fetch abstracts + Generate BibTeX
    # LEARNING: Fetch abstracts in the same pass to avoid separate workflow run
    print(f"\nStep 4: Fetching abstracts & generating BibTeX entries...")
    bibtex_entries = []
    used_keys = set(existing_keys)
    abstracts_found = 0
    abstracts_failed = 0

    for i, paper in enumerate(new_papers):
        key = generate_bibtex_key(paper, args.name)

        # Ensure unique key
        base_key = key
        counter = 1
        while key in used_keys:
            key = f"{base_key}{chr(96 + counter)}"  # a, b, c, ...
            counter += 1

        used_keys.add(key)

        # Fetch abstract if DOI available
        if paper.get("doi") and not paper.get("abstract"):
            abstract = fetch_abstract_openalex(paper["doi"])
            if abstract:
                paper["abstract"] = abstract
                abstracts_found += 1
            else:
                abstracts_failed += 1
            time.sleep(0.12)  # Rate limit: ~8 req/s

        if (i + 1) % 50 == 0:
            print(f"  [{i+1}/{len(new_papers)}] Abstracts: {abstracts_found} found, {abstracts_failed} missing")

        entry = paper_to_bibtex(paper, key, args.lit)
        bibtex_entries.append(entry)

    print(f"  Abstracts found: {abstracts_found}/{len(new_papers)}")
    print(f"  Abstract coverage: {abstracts_found/max(len(new_papers),1)*100:.0f}%")

    # Step 5: Write output
    if args.dry_run:
        print(f"\n  DRY RUN - Would write {len(bibtex_entries)} entries")
        for entry in bibtex_entries[:5]:
            print(f"\n{entry}")
        if len(bibtex_entries) > 5:
            print(f"\n  ... and {len(bibtex_entries) - 5} more")
    else:
        # Write new entries to output file
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(f"%==============================================================================\n")
            f.write(f"% AUTO-IMPORTED: {args.name} papers from {source}\n")
            f.write(f"% Date: {time.strftime('%Y-%m-%d')}\n")
            f.write(f"% Total new: {len(bibtex_entries)}\n")
            f.write(f"%==============================================================================\n\n")

            for entry in bibtex_entries:
                f.write(entry + "\n\n")

        print(f"  Written to: {args.output}")

        # Optionally append to bcm_master.bib
        if args.append_to_bib:
            with open(BIB_PATH, 'a', encoding='utf-8') as f:
                f.write(f"\n%==============================================================================\n")
                f.write(f"% AUTO-IMPORTED: {args.name} papers from {source}\n")
                f.write(f"% Date: {time.strftime('%Y-%m-%d')}\n")
                f.write(f"%==============================================================================\n\n")

                for entry in bibtex_entries:
                    f.write(entry + "\n\n")

            print(f"  Appended to: {BIB_PATH}")

    # Write summary JSON with quality metrics
    with_doi = sum(1 for p in new_papers if p.get("doi"))
    with_journal = sum(1 for p in new_papers if p.get("journal"))
    with_abstract = sum(1 for p in new_papers if p.get("abstract"))

    summary = {
        "researcher": args.name,
        "source": source,
        "mode": "traditional",
        "total_fetched_raw": len(papers) + self_dupes + skipped_existing,
        "author_filter_rejected": rejected if source == "openalex.org" else 0,
        "self_duplicates_removed": self_dupes,
        "already_existing": skipped_existing,
        "new_papers": len(new_papers),
        "quality_metrics": {
            "with_doi": with_doi,
            "with_doi_pct": f"{with_doi/max(len(new_papers),1)*100:.0f}%",
            "with_journal": with_journal,
            "with_journal_pct": f"{with_journal/max(len(new_papers),1)*100:.0f}%",
            "with_abstract": with_abstract,
            "with_abstract_pct": f"{with_abstract/max(len(new_papers),1)*100:.0f}%",
            "content_level": "L1" if with_abstract > len(new_papers) * 0.5 else "L0",
        },
        "new_keys": [generate_bibtex_key(p, args.name) for p in new_papers[:20]],
        "sample_titles": [p.get("title", "")[:80] for p in new_papers[:10]],
    }
    with open("fetch_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\n{'=' * 60}")
    print(f"IMPORT QUALITY REPORT")
    print(f"{'=' * 60}")
    print(f"  Researcher:        {args.name}")
    print(f"  Source:             {source}")
    print(f"  Raw fetched:       {summary['total_fetched_raw']}")
    if source == "openalex.org":
        print(f"  Wrong author:      -{summary['author_filter_rejected']}")
    print(f"  Self-duplicates:   -{self_dupes}")
    print(f"  Already in bib:    -{skipped_existing}")
    print(f"  ─────────────────────────")
    print(f"  NEW papers:        {len(new_papers)}")
    print(f"")
    print(f"  QUALITY:")
    print(f"    With DOI:        {with_doi}/{len(new_papers)} ({summary['quality_metrics']['with_doi_pct']})")
    print(f"    With journal:    {with_journal}/{len(new_papers)} ({summary['quality_metrics']['with_journal_pct']})")
    print(f"    With abstract:   {with_abstract}/{len(new_papers)} ({summary['quality_metrics']['with_abstract_pct']})")
    print(f"    Content level:   {summary['quality_metrics']['content_level']}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
