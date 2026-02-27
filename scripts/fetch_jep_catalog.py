#!/usr/bin/env python3
"""
Fetch complete Journal of Economic Perspectives (JEP) catalog from CrossRef.

Generates:
  1. data/journals/jep/jep-catalog.yaml          - Complete issue/volume catalog
  2. data/journals/jep/volumes/vol-XX.yaml        - Per-volume paper lists
  3. bibliography/jep_papers.bib                   - BibTeX entries for all papers
  4. data/paper-references/PAP-*.yaml              - Individual paper YAMLs (optional)

Usage:
  # Fetch all JEP papers (full run)
  python scripts/fetch_jep_catalog.py

  # Fetch specific volume(s)
  python scripts/fetch_jep_catalog.py --volumes 39

  # Fetch specific year range
  python scripts/fetch_jep_catalog.py --from-year 2020 --to-year 2025

  # Dry run (just show what would be fetched)
  python scripts/fetch_jep_catalog.py --dry-run

  # Generate BibTeX only (from existing catalog)
  python scripts/fetch_jep_catalog.py --bibtex-only

  # Generate PAP-*.yaml files (from existing catalog)
  python scripts/fetch_jep_catalog.py --yaml-only

  # Batch size control
  python scripts/fetch_jep_catalog.py --batch 50
"""

import argparse
import json
import os
import re
import sys
import time
import unicodedata
from pathlib import Path
from datetime import datetime

try:
    import requests
except ImportError:
    print("ERROR: 'requests' package required. Install with: pip install requests")
    sys.exit(1)

try:
    import yaml
except ImportError:
    print("ERROR: 'pyyaml' package required. Install with: pip install pyyaml")
    sys.exit(1)

# =============================================================================
# CONSTANTS
# =============================================================================
JEP_ISSN = "0895-3309"
CROSSREF_BASE = "https://api.crossref.org"
CROSSREF_MAILTO = "research@fehradvice.com"  # Polite pool

REPO_ROOT = Path(__file__).parent.parent
JEP_DIR = REPO_ROOT / "data" / "journals" / "jep"
VOLUMES_DIR = JEP_DIR / "volumes"
BIB_DIR = REPO_ROOT / "bibliography"
PAPER_REF_DIR = REPO_ROOT / "data" / "paper-references"

SEASON_MAP = {1: "Winter", 2: "Spring", 3: "Summer", 4: "Fall"}

# JEP-relevant EBF theory categories for auto-classification
JEP_TOPIC_KEYWORDS = {
    "behavioral": ["LIT-KT", "CORE-WHAT"],
    "experimental": ["LIT-FEH", "METHOD-LLMMC"],
    "labor": ["DOMAIN-LABOR"],
    "public": ["DOMAIN-PUBLIC"],
    "finance": ["DOMAIN-MONETARY"],
    "health": ["DOMAIN-HEALTH"],
    "development": ["DOMAIN-DEV"],
    "education": ["DOMAIN-EDU"],
    "inequality": ["DOMAIN-INEQ"],
    "trade": ["DOMAIN-TRADE"],
    "macro": ["DOMAIN-MACRO"],
    "industrial organization": ["DOMAIN-IO"],
    "game theory": ["FORMAL-GAME"],
    "mechanism design": ["FORMAL-MECH"],
    "nudge": ["CORE-WHEN", "LIT-THALER"],
    "prospect theory": ["LIT-KT", "CORE-WHAT"],
    "loss aversion": ["LIT-KT", "CORE-WHAT"],
    "fairness": ["LIT-FEH", "CORE-HOW"],
    "social preferences": ["LIT-FEH", "CORE-HOW"],
    "trust": ["LIT-FEH", "CORE-HOW"],
    "cooperation": ["LIT-FEH", "CORE-HOW"],
    "discrimination": ["DOMAIN-LABOR", "CORE-WHO"],
    "gender": ["DOMAIN-LABOR", "CORE-WHO"],
    "poverty": ["DOMAIN-DEV", "DOMAIN-PUBLIC"],
    "climate": ["DOMAIN-ENV"],
    "environment": ["DOMAIN-ENV"],
    "regulation": ["DOMAIN-PUBLIC"],
    "antitrust": ["DOMAIN-IO"],
    "auction": ["FORMAL-MECH"],
    "machine learning": ["METHOD-ML"],
    "artificial intelligence": ["METHOD-ML"],
    "randomized": ["METHOD-RCT"],
    "experiment": ["METHOD-RCT"],
    "survey": ["METHOD-SURVEY"],
    "causal": ["METHOD-CAUSAL"],
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def normalize_name(name: str) -> str:
    """Normalize author name for BibTeX key generation."""
    # Remove accents
    nfkd = unicodedata.normalize('NFKD', name)
    ascii_name = nfkd.encode('ASCII', 'ignore').decode('ASCII')
    # Keep only alpha chars, lowercase
    return re.sub(r'[^a-z]', '', ascii_name.lower())


def generate_bibtex_key(authors: list, year: int, title: str) -> str:
    """
    Generate canonical BibTeX key: {nachname}{jahr}{kurzwort}
    Following: docs/standards/bibtex-key-convention.md
    """
    if not authors:
        first_author = "unknown"
    else:
        # Get family name of first author
        first = authors[0]
        family = first.get("family", first.get("name", "unknown"))
        first_author = normalize_name(family)

    # Get first meaningful word from title (skip articles, prepositions)
    skip_words = {"the", "a", "an", "of", "in", "on", "for", "and", "to",
                  "is", "are", "was", "were", "do", "does", "how", "why",
                  "what", "when", "where", "which", "who", "can", "could",
                  "should", "would", "some", "new", "with", "from", "by",
                  "not", "has", "have", "had", "its", "it", "this", "that"}

    words = re.findall(r'[a-z]+', title.lower())
    short_word = "paper"
    for w in words:
        if w not in skip_words and len(w) > 2:
            short_word = w
            break

    return f"{first_author}{year}{short_word}"


def format_author_bibtex(authors: list) -> str:
    """Format author list for BibTeX."""
    if not authors:
        return "Unknown"
    parts = []
    for a in authors:
        family = a.get("family", "")
        given = a.get("given", "")
        if family and given:
            parts.append(f"{family}, {given}")
        elif family:
            parts.append(family)
        elif "name" in a:
            parts.append(a["name"])
    return " and ".join(parts)


def classify_paper_use_for(title: str, abstract: str = "") -> list:
    """Auto-classify paper for EBF use_for based on title/abstract keywords."""
    text = (title + " " + abstract).lower()
    use_for = set()
    for keyword, tags in JEP_TOPIC_KEYWORDS.items():
        if keyword in text:
            use_for.update(tags)
    if not use_for:
        use_for.add("LIT-O")
    return sorted(use_for)


def crossref_fetch_page(cursor: str = "*", rows: int = 100,
                        from_year: int = None, to_year: int = None,
                        sort: str = "published",
                        order: str = "asc") -> dict:
    """Fetch one page of JEP papers from CrossRef."""
    url = f"{CROSSREF_BASE}/journals/{JEP_ISSN}/works"
    params = {
        "cursor": cursor,
        "rows": rows,
        "sort": sort,
        "order": order,
        "mailto": CROSSREF_MAILTO,
    }

    filters = []
    if from_year:
        filters.append(f"from-pub-date:{from_year}-01-01")
    if to_year:
        filters.append(f"until-pub-date:{to_year}-12-31")
    if filters:
        params["filter"] = ",".join(filters)

    for attempt in range(4):
        try:
            resp = requests.get(url, params=params, timeout=30)
            if resp.status_code == 200:
                return resp.json()
            elif resp.status_code == 429:
                wait = 2 ** (attempt + 1)
                print(f"  Rate limited. Waiting {wait}s...")
                time.sleep(wait)
            else:
                print(f"  HTTP {resp.status_code}: {resp.text[:200]}")
                time.sleep(2 ** attempt)
        except requests.exceptions.RequestException as e:
            wait = 2 ** (attempt + 1)
            print(f"  Network error: {e}. Retrying in {wait}s...")
            time.sleep(wait)

    return None


def fetch_year(year: int, batch_size: int = 100) -> list:
    """Fetch all JEP papers for a single year using cursor pagination."""
    papers = []
    cursor = "*"
    page = 0

    while True:
        page += 1
        result = crossref_fetch_page(
            cursor=cursor,
            rows=batch_size,
            from_year=year,
            to_year=year
        )

        if not result:
            print(f"    ERROR: Failed to fetch page {page} for {year}. Stopping year.")
            break

        message = result.get("message", {})
        items = message.get("items", [])

        if not items:
            break

        papers.extend(items)

        next_cursor = message.get("next-cursor")
        if not next_cursor or next_cursor == cursor:
            break
        cursor = next_cursor

        time.sleep(0.3)

    return papers


def fetch_all_jep_papers(from_year=None, to_year=None, batch_size=100,
                         dry_run=False) -> list:
    """Fetch ALL JEP papers year-by-year to avoid cursor pagination limits."""
    if not from_year:
        from_year = 1987
    if not to_year:
        to_year = datetime.now().year

    all_papers = []

    print(f"\n{'='*60}")
    print(f"  Fetching JEP papers from CrossRef (YEAR-BY-YEAR)")
    print(f"  ISSN: {JEP_ISSN}")
    print(f"  Range: {from_year}-{to_year}")
    print(f"  Strategy: One API call per year (avoids cursor limits)")
    print(f"{'='*60}\n")

    for year in range(from_year, to_year + 1):
        if dry_run and year > from_year:
            print(f"  [DRY RUN] Stopping after first year.")
            break

        papers = fetch_year(year, batch_size)
        all_papers.extend(papers)
        print(f"  {year}: {len(papers):3d} papers  (total: {len(all_papers)})")

        # Be polite between years
        time.sleep(0.5)

    print(f"\n  Total fetched: {len(all_papers)} papers ({from_year}-{to_year})")
    return all_papers


# =============================================================================
# CATALOG GENERATION
# =============================================================================

def parse_paper(item: dict) -> dict:
    """Parse a CrossRef work item into our standard format."""
    # Title
    title_list = item.get("title", [])
    title = title_list[0] if title_list else "Untitled"

    # Authors
    authors_raw = item.get("author", [])
    authors = []
    for a in authors_raw:
        author = {}
        if "family" in a:
            author["family"] = a["family"]
        if "given" in a:
            author["given"] = a["given"]
        if "name" in a:
            author["name"] = a["name"]
        if "ORCID" in a:
            author["orcid"] = a["ORCID"]
        if author:
            authors.append(author)

    # Date
    published = item.get("published-print", item.get("published-online", {}))
    date_parts = published.get("date-parts", [[None]])[0]
    year = date_parts[0] if len(date_parts) > 0 else None
    month = date_parts[1] if len(date_parts) > 1 else None

    # Volume/Issue
    volume = item.get("volume")
    issue = item.get("issue")

    # DOI
    doi = item.get("DOI", "")

    # Pages
    page = item.get("page", "")

    # Abstract
    abstract = item.get("abstract", "")
    # Clean HTML from abstract
    if abstract:
        abstract = re.sub(r'<[^>]+>', '', abstract).strip()

    # Subject/keywords
    subjects = item.get("subject", [])

    # References count
    ref_count = item.get("references-count", 0)
    cited_by = item.get("is-referenced-by-count", 0)

    # Generate BibTeX key
    bib_key = generate_bibtex_key(authors, year, title)

    # Auto-classify
    use_for = classify_paper_use_for(title, abstract)

    # Season
    season = None
    if issue:
        try:
            season = SEASON_MAP.get(int(issue))
        except (ValueError, TypeError):
            pass

    return {
        "bibtex_key": bib_key,
        "title": title,
        "authors": authors,
        "year": year,
        "month": month,
        "volume": volume,
        "issue": issue,
        "season": season,
        "doi": doi,
        "pages": page,
        "abstract": abstract,
        "subjects": subjects,
        "references_count": ref_count,
        "cited_by": cited_by,
        "use_for": use_for,
        "url": f"https://doi.org/{doi}" if doi else None,
    }


def organize_by_volume(papers: list) -> dict:
    """Organize papers into volumes and issues."""
    volumes = {}
    for p in papers:
        vol = p.get("volume")
        issue = p.get("issue")
        if vol is None:
            continue
        try:
            vol_int = int(vol)
        except (ValueError, TypeError):
            continue

        if vol_int not in volumes:
            volumes[vol_int] = {"issues": {}}

        if issue is not None:
            try:
                issue_int = int(issue)
            except (ValueError, TypeError):
                issue_int = issue
            if issue_int not in volumes[vol_int]["issues"]:
                volumes[vol_int]["issues"][issue_int] = []
            volumes[vol_int]["issues"][issue_int].append(p)

    return volumes


# =============================================================================
# OUTPUT GENERATORS
# =============================================================================

def write_catalog_yaml(volumes: dict, papers: list):
    """Write the master JEP catalog YAML."""
    JEP_DIR.mkdir(parents=True, exist_ok=True)

    catalog = {
        "journal": {
            "name": "Journal of Economic Perspectives",
            "abbreviation": "JEP",
            "issn_print": "0895-3309",
            "issn_online": "1944-7965",
            "publisher": "American Economic Association",
            "frequency": "Quarterly (Winter, Spring, Summer, Fall)",
            "first_issue": "Summer 1987",
            "open_access": True,
            "url": "https://www.aeaweb.org/journals/jep",
            "editors_current": ["David Autor", "Enrico Moretti", "Andrei Shleifer"],
        },
        "statistics": {
            "total_papers": len(papers),
            "total_volumes": len(volumes),
            "total_issues": sum(len(v["issues"]) for v in volumes.values()),
            "year_range": f"1987-{max(volumes.keys()) + 1986}" if volumes else "N/A",
            "fetched_date": datetime.now().strftime("%Y-%m-%d"),
        },
        "volumes": {},
    }

    for vol_num in sorted(volumes.keys()):
        vol_data = volumes[vol_num]
        year = 1986 + vol_num  # Vol 1 = 1987
        vol_entry = {
            "year": year,
            "issues": {},
            "paper_count": sum(len(iss) for iss in vol_data["issues"].values()),
        }
        for iss_num in sorted(vol_data["issues"].keys()):
            papers_in_issue = vol_data["issues"][iss_num]
            season = SEASON_MAP.get(iss_num, f"Issue {iss_num}")
            vol_entry["issues"][iss_num] = {
                "season": season,
                "paper_count": len(papers_in_issue),
                "papers": [p["bibtex_key"] for p in papers_in_issue],
            }
        catalog["volumes"][vol_num] = vol_entry

    catalog_path = JEP_DIR / "jep-catalog.yaml"
    with open(catalog_path, "w", encoding="utf-8") as f:
        yaml.dump(catalog, f, default_flow_style=False, allow_unicode=True,
                  sort_keys=False, width=120)
    print(f"  Written: {catalog_path}")
    return catalog_path


def write_volume_yamls(volumes: dict):
    """Write per-volume YAML files with full paper details."""
    VOLUMES_DIR.mkdir(parents=True, exist_ok=True)
    paths = []

    for vol_num in sorted(volumes.keys()):
        vol_data = volumes[vol_num]
        year = 1986 + vol_num

        vol_file = {
            "volume": vol_num,
            "year": year,
            "journal": "Journal of Economic Perspectives",
            "issues": {},
        }

        for iss_num in sorted(vol_data["issues"].keys()):
            papers = vol_data["issues"][iss_num]
            season = SEASON_MAP.get(iss_num, f"Issue {iss_num}")

            issue_entry = {
                "season": season,
                "papers": [],
            }

            for p in papers:
                paper_entry = {
                    "bibtex_key": p["bibtex_key"],
                    "title": p["title"],
                    "authors": [
                        f"{a.get('given', '')} {a.get('family', a.get('name', ''))}".strip()
                        for a in p["authors"]
                    ],
                    "doi": p["doi"],
                    "pages": p["pages"],
                    "cited_by": p["cited_by"],
                    "use_for": p["use_for"],
                }
                if p.get("abstract"):
                    paper_entry["abstract"] = p["abstract"][:500]
                issue_entry["papers"].append(paper_entry)

            vol_file["issues"][iss_num] = issue_entry

        path = VOLUMES_DIR / f"vol-{vol_num:02d}.yaml"
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(vol_file, f, default_flow_style=False, allow_unicode=True,
                      sort_keys=False, width=120)
        paths.append(path)

    print(f"  Written: {len(paths)} volume files in {VOLUMES_DIR}")
    return paths


def write_bibtex(papers: list, output_path: Path = None):
    """Generate BibTeX file for all JEP papers."""
    if output_path is None:
        output_path = BIB_DIR / "jep_papers.bib"

    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Track keys for deduplication
    seen_keys = {}
    entries = []

    for p in papers:
        key = p["bibtex_key"]
        # Handle duplicate keys
        if key in seen_keys:
            seen_keys[key] += 1
            key = f"{key}{chr(96 + seen_keys[key])}"  # append b, c, d...
        else:
            seen_keys[key] = 1

        # Build entry
        lines = [f"@article{{{key},"]
        lines.append(f"  title = {{{p['title']}}},")
        lines.append(f"  author = {{{format_author_bibtex(p['authors'])}}},")
        if p["year"]:
            lines.append(f"  year = {{{p['year']}}},")
        lines.append(f"  journal = {{Journal of Economic Perspectives}},")
        if p["volume"]:
            lines.append(f"  volume = {{{p['volume']}}},")
        if p["issue"]:
            lines.append(f"  number = {{{p['issue']}}},")
        if p["pages"]:
            lines.append(f"  pages = {{{p['pages']}}},")
        if p["doi"]:
            lines.append(f"  doi = {{{p['doi']}}},")

        # EBF fields
        use_for_str = ", ".join(p["use_for"])
        lines.append(f"  use_for = {{{use_for_str}}},")
        lines.append(f"  evidence_tier = {{1}},")  # JEP is always Tier 1

        lines.append("}")
        entries.append("\n".join(lines))

    content = (
        f"% =============================================================================\n"
        f"% Journal of Economic Perspectives - Complete Catalog\n"
        f"% Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        f"% Papers: {len(entries)}\n"
        f"% Source: CrossRef API (ISSN {JEP_ISSN})\n"
        f"% =============================================================================\n\n"
        + "\n\n".join(entries)
        + "\n"
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Written: {output_path} ({len(entries)} entries)")
    return output_path


def write_paper_yamls(papers: list, limit: int = None):
    """Generate PAP-*.yaml files for papers."""
    PAPER_REF_DIR.mkdir(parents=True, exist_ok=True)
    count = 0

    for p in papers:
        if limit and count >= limit:
            break

        key = p["bibtex_key"]
        pap_id = f"PAP-{key}"
        path = PAPER_REF_DIR / f"{pap_id}.yaml"

        # Skip if already exists
        if path.exists():
            continue

        paper_yaml = {
            "paper_id": pap_id,
            "bibtex_key": key,
            "title": p["title"],
            "authors": [
                {
                    "name": f"{a.get('given', '')} {a.get('family', a.get('name', ''))}".strip(),
                    **({"orcid": a["orcid"]} if "orcid" in a else {}),
                }
                for a in p["authors"]
            ],
            "year": p["year"],
            "journal": "Journal of Economic Perspectives",
            "volume": p["volume"],
            "issue": p["issue"],
            "pages": p["pages"],
            "doi": p["doi"],
            "url": p["url"],
            "content_level": "L1",
            "integration_level": "I1",
            "evidence_tier": 1,
            "use_for": p["use_for"],
            "status": "cataloged",
            "source": "crossref_jep_fetch",
            "cataloged_date": datetime.now().strftime("%Y-%m-%d"),
        }

        if p.get("abstract"):
            paper_yaml["abstract"] = p["abstract"]
            paper_yaml["content_level"] = "L1"

        if p.get("cited_by"):
            paper_yaml["citation_count"] = p["cited_by"]

        if p.get("subjects"):
            paper_yaml["subjects"] = p["subjects"]

        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(paper_yaml, f, default_flow_style=False,
                      allow_unicode=True, sort_keys=False, width=120)
        count += 1

    print(f"  Written: {count} new PAP-*.yaml files in {PAPER_REF_DIR}")
    return count


# =============================================================================
# STATISTICS
# =============================================================================

def print_statistics(papers: list, volumes: dict):
    """Print summary statistics."""
    print(f"\n{'='*60}")
    print(f"  JEP CATALOG STATISTICS")
    print(f"{'='*60}")
    print(f"  Total papers:     {len(papers)}")
    print(f"  Total volumes:    {len(volumes)}")
    total_issues = sum(len(v['issues']) for v in volumes.values())
    print(f"  Total issues:     {total_issues}")

    # Year range
    years = [p["year"] for p in papers if p["year"]]
    if years:
        print(f"  Year range:       {min(years)}-{max(years)}")

    # Top cited
    by_citations = sorted(papers, key=lambda x: x.get("cited_by", 0), reverse=True)
    print(f"\n  Top 10 most-cited JEP papers:")
    for i, p in enumerate(by_citations[:10], 1):
        short_title = p["title"][:60] + "..." if len(p["title"]) > 60 else p["title"]
        author = p["authors"][0].get("family", "?") if p["authors"] else "?"
        print(f"    {i:2d}. [{p.get('cited_by', 0):5d}] {author} ({p['year']}): {short_title}")

    # use_for distribution
    use_for_counts = {}
    for p in papers:
        for tag in p.get("use_for", []):
            use_for_counts[tag] = use_for_counts.get(tag, 0) + 1

    print(f"\n  EBF use_for distribution (top 15):")
    for tag, count in sorted(use_for_counts.items(), key=lambda x: -x[1])[:15]:
        bar = "#" * min(count // 5, 40)
        print(f"    {tag:<20s} {count:4d} {bar}")

    print(f"{'='*60}\n")


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Fetch JEP catalog from CrossRef and generate EBF-compatible files"
    )
    parser.add_argument("--from-year", type=int, help="Start year (default: 1987)")
    parser.add_argument("--to-year", type=int, help="End year (default: current)")
    parser.add_argument("--volumes", type=int, nargs="+", help="Specific volume numbers")
    parser.add_argument("--batch", type=int, default=100, help="Papers per API page (default: 100)")
    parser.add_argument("--dry-run", action="store_true", help="Fetch only first page")
    parser.add_argument("--bibtex-only", action="store_true", help="Generate BibTeX from existing catalog")
    parser.add_argument("--yaml-only", action="store_true", help="Generate PAP-*.yaml from existing catalog")
    parser.add_argument("--no-paper-yamls", action="store_true", help="Skip PAP-*.yaml generation")
    parser.add_argument("--stats", action="store_true", help="Show statistics only")
    args = parser.parse_args()

    # Convert volume numbers to year range
    from_year = args.from_year
    to_year = args.to_year
    if args.volumes:
        from_year = min(args.volumes) + 1986
        to_year = max(args.volumes) + 1986

    # Fetch from CrossRef
    print("\n" + "=" * 60)
    print("  JEP CATALOG BUILDER")
    print("  Journal of Economic Perspectives")
    print("=" * 60)

    papers_raw = fetch_all_jep_papers(
        from_year=from_year,
        to_year=to_year,
        batch_size=args.batch,
        dry_run=args.dry_run,
    )

    if not papers_raw:
        print("\nERROR: No papers fetched. Check network/API access.")
        sys.exit(1)

    # Parse papers
    print("\nParsing papers...")
    papers = [parse_paper(item) for item in papers_raw]
    papers = [p for p in papers if p["year"]]  # Filter out items without year

    # Organize by volume
    volumes = organize_by_volume(papers)

    # Statistics
    print_statistics(papers, volumes)

    if args.stats:
        return

    # Write outputs
    print("\nGenerating output files...")

    # 1. Master catalog
    write_catalog_yaml(volumes, papers)

    # 2. Per-volume YAMLs
    write_volume_yamls(volumes)

    # 3. BibTeX
    write_bibtex(papers)

    # 4. PAP-*.yaml (optional)
    if not args.no_paper_yamls:
        write_paper_yamls(papers)

    print(f"\n{'='*60}")
    print(f"  DONE! JEP catalog generated successfully.")
    print(f"  Files in: {JEP_DIR}")
    print(f"  BibTeX:   {BIB_DIR / 'jep_papers.bib'}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
