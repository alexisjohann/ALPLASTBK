#!/usr/bin/env python3
"""
Generate prioritized paper upload list for frontend consumption.

Reads all Paper-YAMLs, computes priority scores, and exports
the top N papers that would benefit most from full-text upload.

Priority formula:
  IL_weight(I5=500..I1=50) + CL_boost(L2=80,L1=20) + DOI(15)
  + cases(5/case, max 100) + prior_score * 50

Output: JSON + CSV in data/paper-upload-priority-top{N}.{json,csv}

Usage:
  python scripts/generate_upload_priorities.py              # Top 100
  python scripts/generate_upload_priorities.py --top 200    # Top 200
  python scripts/generate_upload_priorities.py --json-only  # Only JSON
  python scripts/generate_upload_priorities.py --webhook URL # POST to frontend
"""

import argparse
import csv
import json
import os
import sys
import urllib.request
from collections import Counter
from datetime import datetime, timezone

import yaml


# --- Priority weights ---
IL_WEIGHT = {"I5": 500, "I4": 400, "I3": 300, "I2": 150, "I1": 50, "I0": 0}
CL_BOOST = {"L2": 80, "L1": 20, "L0": 0}
DOI_BOOST = 15
CASE_WEIGHT = 5
CASE_MAX = 100
PRIOR_MULTIPLIER = 50

# --- Researcher PDF sources (2-tier: department first, personal second) ---
#
# SEARCH HIERARCHY:
#   Stufe 0: Department/Institution page (university maintains, very stable)
#   Stufe 1: Personal homepage (researcher maintains, has most PDFs)
#   Stufe 2: Unpaywall, Semantic Scholar, etc.
#
# Both tiers provide:
#   - url: direct link to publications page
#   - site_pattern: for filetype:pdf site:X search queries
#
RESEARCHER_HOMEPAGES = {
    "fehr": {
        "name": "Ernst Fehr",
        "department": {
            "url": "https://www.econ.uzh.ch/en/people/faculty/fehr/publications.html",
            "site_pattern": "econ.uzh.ch",
            "institution": "University of Zurich",
        },
    },
    "kahneman": {
        "name": "Daniel Kahneman",
        "department": {
            "url": "https://scholar.princeton.edu/kahneman/publications",
            "site_pattern": "princeton.edu",
            "institution": "Princeton University",
        },
    },
    "thaler": {
        "name": "Richard Thaler",
        "department": {
            "url": "https://faculty.chicagobooth.edu/richard-thaler/research",
            "site_pattern": "chicagobooth.edu",
            "institution": "Chicago Booth",
        },
    },
    "camerer": {
        "name": "Colin Camerer",
        "department": {
            "url": "https://www.hss.caltech.edu/content/colin-f-camerer",
            "site_pattern": "caltech.edu",
            "institution": "Caltech",
        },
    },
    "ariely": {
        "name": "Dan Ariely",
        "department": {
            "url": "https://faculty.fuqua.duke.edu/~dandan/",
            "site_pattern": "duke.edu",
            "institution": "Duke University",
        },
        "personal": {
            "url": "https://danariely.com/resources/academic-papers/",
            "site_pattern": "danariely.com",
        },
    },
    "malmendier": {
        "name": "Ulrike Malmendier",
        "department": {
            "url": "https://eml.berkeley.edu/~ulrike/research.html",
            "site_pattern": "berkeley.edu",
            "institution": "UC Berkeley",
        },
    },
    "sutter": {
        "name": "Matthias Sutter",
        "department": {
            "url": "https://www.coll.mpg.de/matthias-sutter",
            "site_pattern": "mpg.de",
            "institution": "Max Planck Institute Bonn",
        },
    },
    "heckman": {
        "name": "James Heckman",
        "department": {
            "url": "https://www.chicagobooth.edu/faculty/directory/h/james-j-heckman",
            "site_pattern": "uchicago.edu",
            "institution": "University of Chicago",
        },
        "personal": {
            "url": "https://heckmanequation.org/resource-library/",
            "site_pattern": "heckmanequation.org",
        },
    },
    "benabou": {
        "name": "Roland Bénabou",
        "department": {
            "url": "https://www.princeton.edu/~rbenabou/papers.html",
            "site_pattern": "princeton.edu",
            "institution": "Princeton University",
        },
    },
    "dellavigna": {
        "name": "Stefano DellaVigna",
        "department": {
            "url": "https://eml.berkeley.edu/~sdellavi/research.html",
            "site_pattern": "berkeley.edu",
            "institution": "UC Berkeley",
        },
    },
    "rabin": {
        "name": "Matthew Rabin",
        "department": {
            "url": "https://scholar.harvard.edu/rabin/publications",
            "site_pattern": "harvard.edu",
            "institution": "Harvard University",
        },
    },
    "prelec": {
        "name": "Drazen Prelec",
        "department": {
            "url": "https://mitsloan.mit.edu/faculty/directory/drazen-prelec",
            "site_pattern": "mit.edu",
            "institution": "MIT Sloan",
        },
    },
    "bolton": {
        "name": "Gary Bolton",
        "department": {
            "url": "https://www.mccombs.utexas.edu/faculty/gary-bolton",
            "site_pattern": "utexas.edu",
            "institution": "UT Austin",
        },
    },
    "henrich": {
        "name": "Joseph Henrich",
        "department": {
            "url": "https://henrich.fas.harvard.edu/publications",
            "site_pattern": "harvard.edu",
            "institution": "Harvard University",
        },
    },
    "cosmides": {
        "name": "Leda Cosmides",
        "department": {
            "url": "https://www.psych.ucsb.edu/people/faculty/cosmides",
            "site_pattern": "ucsb.edu",
            "institution": "UC Santa Barbara",
        },
    },
    "becker": {
        "name": "Gary Becker",
        "department": {
            "url": "https://www.chicagobooth.edu/faculty/directory/b/gary-s-becker",
            "site_pattern": "chicagobooth.edu",
            "institution": "Chicago Booth (archive)",
        },
    },
    "tversky": {
        "name": "Amos Tversky",
        "department": {
            "url": "https://psychology.stanford.edu/",
            "site_pattern": "stanford.edu",
            "institution": "Stanford University (archive)",
        },
    },
    "falk": {
        "name": "Armin Falk",
        "department": {
            "url": "https://www.briq-institute.org/people/armin-falk",
            "site_pattern": "briq-institute.org",
            "institution": "briq Institute Bonn",
        },
    },
    "gneezy": {
        "name": "Uri Gneezy",
        "department": {
            "url": "https://rady.ucsd.edu/faculty/directory/gneezy/",
            "site_pattern": "ucsd.edu",
            "institution": "UCSD Rady",
        },
    },
    "loewenstein": {
        "name": "George Loewenstein",
        "department": {
            "url": "https://www.cmu.edu/dietrich/sds/people/faculty/george-loewenstein.html",
            "site_pattern": "cmu.edu",
            "institution": "Carnegie Mellon",
        },
    },
    "tirole": {
        "name": "Jean Tirole",
        "department": {
            "url": "https://www.tse-fr.eu/people/jean-tirole",
            "site_pattern": "tse-fr.eu",
            "institution": "Toulouse School of Economics",
        },
    },
    "balafoutas": {
        "name": "Loukas Balafoutas",
        "department": {
            "url": "https://www.uibk.ac.at/economics/personal/balafoutas/",
            "site_pattern": "uibk.ac.at",
            "institution": "University of Innsbruck",
        },
    },
    "madrian": {
        "name": "Brigitte Madrian",
        "department": {
            "url": "https://scholar.harvard.edu/madrian/publications",
            "site_pattern": "harvard.edu",
            "institution": "Harvard Kennedy School",
        },
    },
    "rossinslater": {
        "name": "Maya Rossin-Slater",
        "department": {
            "url": "https://profiles.stanford.edu/maya-rossin-slater",
            "site_pattern": "stanford.edu",
            "institution": "Stanford University",
        },
    },
    "puntoni": {
        "name": "Stefano Puntoni",
        "department": {
            "url": "https://www.wharton.upenn.edu/faculty/platform/profile/stefano-puntoni/",
            "site_pattern": "upenn.edu",
            "institution": "Wharton, UPenn",
        },
    },
    "simon": {
        "name": "Herbert Simon",
        "department": {
            "url": "https://www.cs.cmu.edu/~simon/",
            "site_pattern": "cmu.edu",
            "institution": "Carnegie Mellon (archive)",
        },
    },
    "roth": {
        "name": "Alvin Roth",
        "department": {
            "url": "https://web.stanford.edu/~alroth/papers.html",
            "site_pattern": "stanford.edu",
            "institution": "Stanford University",
        },
    },
    "allcott": {
        "name": "Hunt Allcott",
        "department": {
            "url": "https://www.microsoft.com/en-us/research/people/hallcott/",
            "site_pattern": "microsoft.com",
            "institution": "Microsoft Research",
        },
        "personal": {
            "url": "https://huntallcott.com/research/",
            "site_pattern": "huntallcott.com",
        },
    },
    "schultz": {
        "name": "P. Wesley Schultz",
        "department": {
            "url": "https://schultzlab.sites.claremont.edu/publications/",
            "site_pattern": "claremont.edu",
            "institution": "Claremont Graduate University",
        },
    },
    "braghieri": {
        "name": "Luca Braghieri",
        "department": {
            "url": "https://www.bocconi.eu/",
            "site_pattern": "bocconi.eu",
            "institution": "Bocconi University",
        },
        "personal": {
            "url": "https://www.lucabraghieri.com/research",
            "site_pattern": "lucabraghieri.com",
        },
    },
    "mertens": {
        "name": "Stephanie Mertens",
        "department": {
            "url": "https://www.econ.uzh.ch/",
            "site_pattern": "uzh.ch",
            "institution": "University of Zurich",
        },
        "personal": {
            "url": "https://www.stephaniemertens.com/research",
            "site_pattern": "stephaniemertens.com",
        },
    },
    "zellweger": {
        "name": "Thomas Zellweger",
        "department": {
            "url": "https://www.unisg.ch/en/personenverzeichnis/thomas-zellweger",
            "site_pattern": "unisg.ch",
            "institution": "University of St. Gallen",
        },
    },
    "enke": {
        "name": "Benjamin Enke",
        "department": {
            "url": "https://scholar.harvard.edu/benke/home",
            "site_pattern": "harvard.edu",
            "institution": "Harvard University",
        },
        "personal": {
            "url": "https://benjamin-enke.com/",
            "site_pattern": "benjamin-enke.com",
        },
    },
}


def match_researcher(first_author: str, bibtex_key: str) -> dict | None:
    """Match a paper to a known researcher homepage.

    Uses bibtex_key prefix as primary match (most reliable since keys follow
    the convention {surname}{year}{word}), with fallback to author name matching.
    """
    # Try bibtex_key prefix first (most reliable: "fehr1999theory" → "fehr")
    key_lower = bibtex_key.lower()
    for slug, info in RESEARCHER_HOMEPAGES.items():
        if key_lower.startswith(slug):
            return info

    # Fallback: match on first_author field (handles dict-format and strings)
    author_lower = str(first_author).lower()
    for slug, info in RESEARCHER_HOMEPAGES.items():
        surname = info["name"].split()[-1].lower()
        if surname in author_lower or slug in author_lower:
            return info

    return None


def load_paper(path: str) -> dict | None:
    """Load a single paper YAML and extract priority-relevant fields."""
    try:
        with open(path) as f:
            data = yaml.safe_load(f)
        if not data:
            return None

        key = os.path.basename(path).replace("PAP-", "").replace(".yaml", "")
        ft = data.get("full_text") or {}
        ps = data.get("prior_score") or {}
        ebf = data.get("ebf_integration") or {}

        # Content Level: full_text > prior_score > top-level
        cl = str(ft.get("content_level") or ps.get("content_level") or data.get("content_level") or "L1")
        if cl not in ("L0", "L1", "L2", "L3"):
            cl = "L1"
        if cl == "L3":
            return None  # Already has full text

        # Integration Level: prior_score > top-level
        il = str(ps.get("integration_level") or data.get("integration_level") or "I1")
        if il not in ("I0", "I1", "I2", "I3", "I4", "I5"):
            il = "I1"

        # Prior score
        score = float(ps.get("pi_normalized") or ps.get("prior_score") or 0)

        # Metadata
        title = str(data.get("title") or "")
        authors = data.get("authors") or data.get("author") or []
        if isinstance(authors, list):
            first_author = str(authors[0]) if authors else ""
        else:
            first_author = str(authors)
        year = str(data.get("year") or "")
        doi = str(data.get("doi") or "")
        journal = str(data.get("journal") or "")

        # Full text status
        has_ft = os.path.exists(f"data/paper-texts/PAP-{key}.md")

        # Linked cases
        linked_cases = data.get("linked_cases") or []
        case_count = len(linked_cases) if isinstance(linked_cases, list) else 0

        # Theory support
        theory_support = ebf.get("theory_support") or ""
        has_theory = bool(theory_support)

        # Use_for
        use_for = ebf.get("use_for") or []
        if isinstance(use_for, str):
            use_for = [use_for]

        # Priority score
        priority = (
            IL_WEIGHT.get(il, 0)
            + CL_BOOST.get(cl, 0)
            + (DOI_BOOST if doi else 0)
            + min(case_count * CASE_WEIGHT, CASE_MAX)
            + score * PRIOR_MULTIPLIER
        )

        # Researcher pages (Stufe 0: department, Stufe 1: personal)
        researcher = match_researcher(first_author, key)
        researcher_info = None
        if researcher:
            dept = researcher.get("department", {})
            pers = researcher.get("personal")
            researcher_info = {
                "name": researcher["name"],
                "department": {
                    "url": dept.get("url", ""),
                    "site_pattern": dept.get("site_pattern", ""),
                    "institution": dept.get("institution", ""),
                    "search_hint": f'{title[:60]} filetype:pdf site:{dept.get("site_pattern", "")}',
                } if dept else None,
                "personal": {
                    "url": pers["url"],
                    "site_pattern": pers["site_pattern"],
                    "search_hint": f'{title[:60]} filetype:pdf site:{pers["site_pattern"]}',
                } if pers else None,
            }

        # Auto-resolvable PDF URLs for backend auto-fetch
        fetch_urls = []
        if doi:
            fetch_urls.append(f"https://api.unpaywall.org/v2/{doi}?email=research@fehradvice.com")
            # NBER working papers have predictable PDF URLs
            if "10.3386/" in doi:
                nber_id = doi.split("10.3386/")[1]
                fetch_urls.append(f"https://www.nber.org/system/files/working_papers/{nber_id}/{nber_id}.pdf")
            fetch_urls.append(f"https://doi.org/{doi}")

        return {
            "rank": 0,
            "paper_id": f"PAP-{key}",
            "bibtex_key": key,
            "title": title[:150],
            "first_author": first_author[:40],
            "year": year,
            "doi": doi,
            "journal": journal[:80],
            "content_level": cl,
            "integration_level": il,
            "prior_score": round(score, 4),
            "has_full_text": has_ft,
            "linked_cases": case_count,
            "researcher": researcher_info,
            "fetch_urls": fetch_urls,
            "has_theory_support": has_theory,
            "use_for_count": len(use_for),
            "priority_score": round(priority, 1),
            "upload_action": "",
        }
    except Exception:
        return None


def compute_upload_action(paper: dict) -> str:
    """Determine what action is needed for this paper."""
    actions = []
    if not paper["doi"]:
        actions.append("FIND_DOI")
    if paper["has_full_text"]:
        actions.append("UPGRADE_TO_L3")
    else:
        actions.append("UPLOAD_FULLTEXT")
    return ";".join(actions)


def generate_priorities(top_n: int = 100) -> dict:
    """Generate the full priority list."""
    paper_dir = "data/paper-references"
    papers = []

    for f in sorted(os.listdir(paper_dir)):
        if not f.startswith("PAP-") or not f.endswith(".yaml"):
            continue
        result = load_paper(os.path.join(paper_dir, f))
        if result:
            papers.append(result)

    # Sort by priority descending
    papers.sort(key=lambda x: x["priority_score"], reverse=True)
    top = papers[:top_n]

    # Add rank and upload action
    for i, p in enumerate(top):
        p["rank"] = i + 1
        p["upload_action"] = compute_upload_action(p)

    # Stats
    il_dist = dict(sorted(Counter(p["integration_level"] for p in top).items()))
    cl_dist = dict(sorted(Counter(p["content_level"] for p in top).items()))
    with_researcher = sum(1 for p in top if p.get("researcher"))

    return {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "version": "3.0",
        "description": f"Top {top_n} papers prioritized for full-text upload",
        "priority_formula": "IL(I5=500..I1=50) + CL(L2=80,L1=20) + DOI(15) + cases(5/ea,max100) + prior*50",
        "total_eligible": len(papers),
        "total_in_list": len(top),
        "stats": {
            "integration_levels": il_dist,
            "content_levels": cl_dist,
            "with_doi": sum(1 for p in top if p["doi"]),
            "without_doi": sum(1 for p in top if not p["doi"]),
            "has_full_text_already": sum(1 for p in top if p["has_full_text"]),
            "needs_upload": sum(1 for p in top if not p["has_full_text"]),
            "with_researcher_homepage": with_researcher,
            "avg_linked_cases": round(sum(p["linked_cases"] for p in top) / max(len(top), 1), 1),
        },
        "papers": top,
    }


def export_json(data: dict, path: str) -> None:
    """Export as JSON."""
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def export_csv(data: dict, path: str) -> None:
    """Export as CSV."""
    fields = [
        "rank", "paper_id", "bibtex_key", "title", "first_author", "year",
        "doi", "journal", "content_level", "integration_level", "prior_score",
        "has_full_text", "linked_cases", "has_theory_support", "use_for_count",
        "priority_score", "upload_action", "researcher", "fetch_urls",
    ]
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data["papers"])


def send_webhook(url: str, data: dict) -> bool:
    """POST the priority list to a webhook URL."""
    # Send only summary + paper list (not full metadata)
    payload = {
        "event": "priority_list_updated",
        "generated": data["generated"],
        "total": data["total_in_list"],
        "stats": data["stats"],
        "papers": [
            {
                "rank": p["rank"],
                "paper_id": p["paper_id"],
                "doi": p["doi"],
                "title": p["title"],
                "first_author": p["first_author"],
                "year": p["year"],
                "priority_score": p["priority_score"],
                "upload_action": p["upload_action"],
                "researcher": p.get("researcher"),
                "fetch_urls": p.get("fetch_urls", []),
            }
            for p in data["papers"]
        ],
    }

    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            print(f"  Webhook response: {resp.status}")
            return resp.status < 400
    except Exception as e:
        print(f"  Webhook failed: {e}", file=sys.stderr)
        return False


def print_summary(data: dict) -> None:
    """Print human-readable summary."""
    stats = data["stats"]
    papers = data["papers"]

    print("=" * 72)
    print(f"  TOP {data['total_in_list']} PAPERS FOR FULL-TEXT UPLOAD")
    print(f"  Generated: {data['generated']} | Eligible: {data['total_eligible']}")
    print("=" * 72)
    print()
    print(f"  Integration Levels: {stats['integration_levels']}")
    print(f"  Content Levels:     {stats['content_levels']}")
    print(f"  With DOI:           {stats['with_doi']} / {data['total_in_list']}")
    print(f"  Researcher page:   {stats['with_researcher_homepage']} / {data['total_in_list']}")
    print(f"  Needs upload:       {stats['needs_upload']} / {data['total_in_list']}")
    print(f"  Avg linked cases:   {stats['avg_linked_cases']}")
    print()

    # Show by tier
    for label, ils in [
        ("TIER 1: Case-Integrated (I3+)", ("I3", "I4", "I5")),
        ("TIER 2: Theory-Supported (I2)", ("I2",)),
        ("TIER 3: Basic (I1)", ("I1",)),
    ]:
        tier = [p for p in papers if p["integration_level"] in ils]
        if not tier:
            continue
        print(f"  --- {label}: {len(tier)} papers ---")
        for p in tier[:8]:
            doi_s = p["doi"][:40] if p["doi"] else "NO DOI"
            ft = "FT" if p["has_full_text"] else "  "
            print(
                f"  #{p['rank']:3} [{p['integration_level']}/{p['content_level']}] "
                f"{ft} C:{p['linked_cases']:>3}  "
                f"{p['bibtex_key'][:35]:<35}  {doi_s}"
            )
        if len(tier) > 8:
            print(f"       ... +{len(tier) - 8} more")
        print()


def main():
    parser = argparse.ArgumentParser(description="Generate prioritized paper upload list")
    parser.add_argument("--top", type=int, default=100, help="Number of papers (default: 100)")
    parser.add_argument("--json-only", action="store_true", help="Only export JSON")
    parser.add_argument("--webhook", type=str, help="POST results to this URL")
    parser.add_argument("--quiet", action="store_true", help="No console output")
    parser.add_argument("--output-dir", type=str, default="data", help="Output directory")
    args = parser.parse_args()

    data = generate_priorities(args.top)

    if not args.quiet:
        print_summary(data)

    # Export JSON
    json_path = os.path.join(args.output_dir, f"paper-upload-priority-top{args.top}.json")
    export_json(data, json_path)
    if not args.quiet:
        print(f"  JSON → {json_path}")

    # Export CSV
    if not args.json_only:
        csv_path = os.path.join(args.output_dir, f"paper-upload-priority-top{args.top}.csv")
        export_csv(data, csv_path)
        if not args.quiet:
            print(f"  CSV  → {csv_path}")

    # Webhook
    if args.webhook:
        if not args.quiet:
            print(f"\n  Sending webhook to {args.webhook}...")
        ok = send_webhook(args.webhook, data)
        if not args.quiet:
            print(f"  Webhook: {'✅ OK' if ok else '❌ FAILED'}")
        if not ok:
            sys.exit(1)


if __name__ == "__main__":
    main()
