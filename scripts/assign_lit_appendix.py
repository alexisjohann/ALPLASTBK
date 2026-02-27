#!/usr/bin/env python3
"""
EBF LIT-Appendix Assignment Tool

Automatically assigns new papers to the correct LIT-Appendix based on the
unified LIT taxonomy (LIT-R, LIT-D, LIT-M, LIT-O).

Usage:
    python scripts/assign_lit_appendix.py --author "Thaler" --title "Mental Accounting"
    python scripts/assign_lit_appendix.py --interactive
    python scripts/assign_lit_appendix.py --bibtex paper.bib
    python scripts/assign_lit_appendix.py --check-author "Grant"
    python scripts/assign_lit_appendix.py --list-appendices

Reference: docs/frameworks/appendix-category-definitions.md (LIT-Matching-Regeln)
"""

import sys
import re
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class PaperInfo:
    """Information about a paper to be classified."""
    author: str
    title: str
    year: Optional[str] = None
    keywords: Optional[List[str]] = None
    journal: Optional[str] = None
    abstract: Optional[str] = None


@dataclass
class LITAssignment:
    """Result of LIT assignment."""
    appendix_code: str
    appendix_name: str
    category: str  # LIT-R, LIT-M, LIT-O
    confidence: str  # high, medium, low
    reasoning: str
    cluster: Optional[str] = None  # For OT assignments


# =============================================================================
# KNOWN LIT-APPENDICES (from appendix-category-definitions.md)
# =============================================================================

# Researcher-based LIT appendices (LIT-R)
LIT_R_APPENDICES = {
    "fehr": {"code": "K", "name": "LIT-FEHR", "aliases": ["ernst fehr", "fehr"]},
    "thaler": {"code": "THL", "name": "LIT-THALER", "aliases": ["richard thaler", "thaler"]},
    "kahneman": {"code": "U", "name": "LIT-KT", "aliases": ["daniel kahneman", "kahneman", "tversky"]},
    "tversky": {"code": "U", "name": "LIT-KT", "aliases": ["amos tversky", "tversky"]},
    "gneezy": {"code": "GN", "name": "LIT-GNEEZY", "aliases": ["uri gneezy", "gneezy"]},
    "ariely": {"code": "AR", "name": "LIT-ARIELY", "aliases": ["dan ariely", "ariely"]},
    "sunstein": {"code": "SUN", "name": "LIT-SUNSTEIN", "aliases": ["cass sunstein", "sunstein"]},
    "loewenstein": {"code": "LO", "name": "LIT-LOEWENSTEIN", "aliases": ["george loewenstein", "loewenstein"]},
    "camerer": {"code": "CAM", "name": "LIT-CAMERER", "aliases": ["colin camerer", "camerer"]},
    "shleifer": {"code": "M", "name": "LIT-SHLEIFER", "aliases": ["andrei shleifer", "shleifer"]},
    "heckman": {"code": "N", "name": "LIT-HECKMAN", "aliases": ["james heckman", "heckman"]},
    "autor": {"code": "O", "name": "LIT-AUTOR", "aliases": ["david autor", "autor"]},
    "duflo": {"code": "P", "name": "LIT-DUFLO", "aliases": ["esther duflo", "duflo"]},
    "bloom": {"code": "Q", "name": "LIT-BLOOM", "aliases": ["nick bloom", "bloom"]},
    "falk": {"code": "FK", "name": "LIT-FALK", "aliases": ["armin falk", "falk"]},
    "gächter": {"code": "GA", "name": "LIT-GAECHTER", "aliases": ["simon gächter", "gaechter", "gachter"]},
    "list": {"code": "LST", "name": "LIT-LIST", "aliases": ["john list", "list"]},
    "malmendier": {"code": "MAL", "name": "LIT-MALMENDIER", "aliases": ["ulrike malmendier", "malmendier"]},
    "mullainathan": {"code": "MUL", "name": "LIT-MULLAINATHAN", "aliases": ["sendhil mullainathan", "mullainathan"]},
    "shafir": {"code": "SHF", "name": "LIT-SHAFIR", "aliases": ["eldar shafir", "shafir"]},
    "becker": {"code": "BK", "name": "LIT-BECKER", "aliases": ["gary becker", "becker"]},
    "akerlof": {"code": "AK", "name": "LIT-AKERLOF", "aliases": ["george akerlof", "akerlof"]},
    "rabin": {"code": "RB", "name": "LIT-RABIN", "aliases": ["matthew rabin", "rabin"]},
    "laibson": {"code": "LB", "name": "LIT-LAIBSON", "aliases": ["david laibson", "laibson"]},
    "tirole": {"code": "TR", "name": "LIT-TIROLE", "aliases": ["jean tirole", "tirole"]},
    "benartzi": {"code": "BN", "name": "LIT-BENARTZI", "aliases": ["shlomo benartzi", "benartzi"]},
    "cialdini": {"code": "CI", "name": "LIT-CIALDINI", "aliases": ["robert cialdini", "cialdini"]},
    "schwartz": {"code": "SW", "name": "LIT-SCHWARTZ", "aliases": ["barry schwartz", "schwartz"]},
}

# Thematic/Meta LIT appendices (LIT-M)
LIT_M_APPENDICES = {
    "meta": {"code": "AX", "name": "LIT-META", "keywords": ["metascience", "meta-analysis", "replication", "methodology"]},
    "paradigms": {"code": "AY", "name": "LIT-PARADIGMS", "keywords": ["paradigm", "interdisciplinary", "theory comparison"]},
    "history": {"code": "XV", "name": "LIT-HISTORY", "keywords": ["history", "historical", "origins", "development"]},
    "critique": {"code": "XVI", "name": "LIT-CRITIQUE", "keywords": ["critique", "criticism", "rebuttal", "limitations"]},
    "thermodynamics": {"code": "XVII", "name": "LIT-THERMODYNAMICS", "keywords": ["thermodynamics", "physics", "entropy", "energy"]},
    "learning": {"code": "XIX", "name": "LIT-LEARNING", "keywords": ["learning", "belief updating", "experience goods", "bayesian"]},
}

# Thematic clusters for OT (LIT-OTHER)
OT_CLUSTERS = {
    "choice_architecture": {
        "keywords": ["choice architecture", "menu design", "option overload", "default"],
        "examples": ["Iyengar & Lepper (2000)", "Johnson & Goldstein (2003)"]
    },
    "cognitive_psychology": {
        "keywords": ["cognitive", "attention", "memory", "capacity", "working memory"],
        "examples": ["Miller (1956)", "Baddeley (1992)"]
    },
    "prosocial_motivation": {
        "keywords": ["prosocial", "altruism", "meaning", "purpose", "intrinsic motivation"],
        "examples": ["Grant (2008)", "Deci & Ryan (1985)"]
    },
    "organizational_psychology": {
        "keywords": ["organizational", "commitment", "culture", "job satisfaction"],
        "examples": ["Meyer & Allen (1991)", "Hackman & Oldham (1976)"]
    },
    "market_morality": {
        "keywords": ["market", "morality", "ethics", "commodification"],
        "examples": ["Falk & Szech (2013)", "Sandel (2012)"]
    },
    "social_norms": {
        "keywords": ["social norms", "descriptive norms", "injunctive norms", "peer effects"],
        "examples": ["Cialdini (2007)", "Bicchieri (2006)"]
    },
    "time_preferences": {
        "keywords": ["time preference", "discounting", "patience", "present bias"],
        "examples": ["Frederick et al. (2002)", "Strotz (1956)"]
    },
    "risk_preferences": {
        "keywords": ["risk preference", "risk aversion", "uncertainty", "ambiguity"],
        "examples": ["Ellsberg (1961)", "Holt & Laury (2002)"]
    },
}


# =============================================================================
# ASSIGNMENT LOGIC
# =============================================================================

def extract_primary_author(author_string: str) -> str:
    """Extract primary author's last name from author string."""
    # Handle "Last, First" format
    if "," in author_string:
        return author_string.split(",")[0].strip().lower()
    # Handle "First Last and Second Author" format
    parts = author_string.split(" and ")[0].strip().split()
    if parts:
        return parts[-1].lower()
    return author_string.lower()


def check_lit_r_match(author: str) -> Optional[Dict]:
    """Check if author matches an existing LIT-R appendix."""
    author_lower = author.lower()

    for key, data in LIT_R_APPENDICES.items():
        for alias in data["aliases"]:
            if alias in author_lower or author_lower in alias:
                return {
                    "code": data["code"],
                    "name": data["name"],
                    "matched_author": key
                }
    return None


def check_lit_m_match(paper: PaperInfo) -> Optional[Dict]:
    """Check if paper matches a thematic LIT-M appendix."""
    searchable = f"{paper.title} {' '.join(paper.keywords or [])} {paper.abstract or ''}".lower()

    # Check for historical papers (>50 years old)
    if paper.year:
        try:
            year = int(paper.year)
            if year < 1975:  # More than ~50 years old
                return {
                    "code": "XV",
                    "name": "LIT-HISTORY",
                    "category": "history",
                    "reason": f"Paper from {year} (>50 years old)"
                }
        except ValueError:
            pass

    # Check keyword matches
    for category, data in LIT_M_APPENDICES.items():
        matches = sum(1 for kw in data["keywords"] if kw in searchable)
        if matches >= 2:  # At least 2 keyword matches
            return {
                "code": data["code"],
                "name": data["name"],
                "category": category,
                "reason": f"Matched {matches} keywords for {category}"
            }

    return None


def determine_ot_cluster(paper: PaperInfo) -> str:
    """Determine the thematic cluster for OT assignment."""
    searchable = f"{paper.title} {' '.join(paper.keywords or [])} {paper.abstract or ''}".lower()

    best_cluster = "general"
    best_score = 0

    for cluster, data in OT_CLUSTERS.items():
        score = sum(1 for kw in data["keywords"] if kw in searchable)
        if score > best_score:
            best_score = score
            best_cluster = cluster

    return best_cluster


def count_author_papers_in_bib(author: str, bib_path: Path) -> int:
    """Count how many papers by this author are in the bibliography."""
    try:
        with open(bib_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read().lower()
    except Exception:
        return 0

    author_lower = author.lower()
    # Count occurrences in author fields
    pattern = rf'author\s*=\s*\{{[^}}]*{re.escape(author_lower)}[^}}]*\}}'
    matches = re.findall(pattern, content, re.IGNORECASE)
    return len(matches)


def assign_lit_appendix(paper: PaperInfo, bib_path: Optional[Path] = None) -> LITAssignment:
    """
    Assign a paper to the appropriate LIT-Appendix.

    Follows the decision tree from appendix-category-definitions.md:
    SCHRITT 0: Methodical/Historical/Critical? → LIT-M
    SCHRITT 1: Existing author-LIT? → LIT-R
    SCHRITT 2: Extension of existing author? → LIT-R
    SCHRITT 3: Author meets threshold? → New LIT-R
    SCHRITT 4: → OT with cluster
    """

    primary_author = extract_primary_author(paper.author)

    # SCHRITT 0: Check for LIT-M (methodical/historical/critical)
    lit_m_match = check_lit_m_match(paper)
    if lit_m_match:
        return LITAssignment(
            appendix_code=lit_m_match["code"],
            appendix_name=lit_m_match["name"],
            category="LIT-M",
            confidence="high",
            reasoning=f"SCHRITT 0: {lit_m_match['reason']}"
        )

    # SCHRITT 1: Check for existing author-LIT
    lit_r_match = check_lit_r_match(paper.author)
    if lit_r_match:
        return LITAssignment(
            appendix_code=lit_r_match["code"],
            appendix_name=lit_r_match["name"],
            category="LIT-R",
            confidence="high",
            reasoning=f"SCHRITT 1: Author '{lit_r_match['matched_author']}' has dedicated LIT-Appendix"
        )

    # SCHRITT 2: Check for extension of existing author (simplified)
    # Look for citations to known authors in title/keywords
    for key, data in LIT_R_APPENDICES.items():
        for alias in data["aliases"]:
            if alias in paper.title.lower():
                return LITAssignment(
                    appendix_code=data["code"],
                    appendix_name=data["name"],
                    category="LIT-R",
                    confidence="medium",
                    reasoning=f"SCHRITT 2: Paper extends '{key}' research (mentioned in title)"
                )

    # SCHRITT 3: Check if author meets threshold for new LIT
    if bib_path and bib_path.exists():
        paper_count = count_author_papers_in_bib(primary_author, bib_path)
        if paper_count >= 5:
            return LITAssignment(
                appendix_code="NEW",
                appendix_name=f"LIT-{primary_author.upper()}",
                category="LIT-R (NEW)",
                confidence="medium",
                reasoning=f"SCHRITT 3: Author '{primary_author}' has {paper_count} papers in bibliography (≥5 threshold)"
            )

    # SCHRITT 4: Assign to OT with cluster
    cluster = determine_ot_cluster(paper)
    return LITAssignment(
        appendix_code="OT",
        appendix_name="LIT-OTHER",
        category="LIT-O",
        confidence="high" if cluster != "general" else "low",
        reasoning=f"SCHRITT 4: No dedicated LIT-Appendix; assigned to OT",
        cluster=cluster
    )


def generate_bibtex_entry(paper: PaperInfo, assignment: LITAssignment) -> str:
    """Generate a BibTeX entry with EBF tags."""
    key = f"{extract_primary_author(paper.author)}{paper.year or 'YYYY'}"

    entry = f"""@article{{{key},
  author = {{{paper.author}}},
  title = {{{paper.title}}},
  year = {{{paper.year or 'YYYY'}}},
  journal = {{{paper.journal or 'JOURNAL'}}},
  % === EBF INTEGRATION ===
  ebf_lit_appendix = {{{assignment.appendix_name}}},
  ebf_lit_category = {{{assignment.category}}},
  ebf_cluster = {{{assignment.cluster or 'N/A'}}},
  ebf_integration_date = {{2026-01-19}},
  ebf_integration_confidence = {{{assignment.confidence}}},
}}"""
    return entry


def interactive_mode():
    """Run interactive paper classification."""
    print("\n" + "=" * 60)
    print("EBF LIT-Appendix Assignment Tool (Interactive Mode)")
    print("=" * 60)

    author = input("\nAuthor(s): ").strip()
    title = input("Title: ").strip()
    year = input("Year (optional): ").strip() or None
    keywords = input("Keywords (comma-separated, optional): ").strip()
    keywords = [k.strip() for k in keywords.split(",")] if keywords else None

    paper = PaperInfo(
        author=author,
        title=title,
        year=year,
        keywords=keywords
    )

    # Find bibliography
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    bib_path = project_root / "bibliography" / "bcm_master.bib"

    assignment = assign_lit_appendix(paper, bib_path)

    print("\n" + "-" * 60)
    print("ASSIGNMENT RESULT")
    print("-" * 60)
    print(f"\n  Appendix Code: \033[1m{assignment.appendix_code}\033[0m")
    print(f"  Appendix Name: \033[1m{assignment.appendix_name}\033[0m")
    print(f"  Category: {assignment.category}")
    print(f"  Confidence: {assignment.confidence}")
    print(f"  Reasoning: {assignment.reasoning}")
    if assignment.cluster:
        print(f"  OT Cluster: {assignment.cluster}")

    print("\n" + "-" * 60)
    print("BIBTEX ENTRY (for bcm_master.bib)")
    print("-" * 60)
    print(generate_bibtex_entry(paper, assignment))

    return assignment


def check_author(author_name: str):
    """Check if an author has or qualifies for a dedicated LIT-Appendix."""
    print(f"\n\033[1mChecking author: {author_name}\033[0m\n")

    # Check existing LIT-R
    lit_r_match = check_lit_r_match(author_name)
    if lit_r_match:
        print(f"  ✅ Author has dedicated LIT-Appendix:")
        print(f"     Code: {lit_r_match['code']}")
        print(f"     Name: {lit_r_match['name']}")
        return

    # Check paper count
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    bib_path = project_root / "bibliography" / "bcm_master.bib"

    if bib_path.exists():
        count = count_author_papers_in_bib(author_name, bib_path)
        print(f"  📊 Papers in bcm_master.bib: {count}")

        if count >= 5:
            print(f"  ✅ Author meets threshold (≥5) for dedicated LIT-Appendix")
            print(f"     Suggested name: LIT-{author_name.upper()}")
        elif count >= 3:
            print(f"  ⚠️  Author approaching threshold ({count}/5)")
            print(f"     Consider creating LIT-{author_name.upper()} soon")
        else:
            print(f"  ❌ Author does not meet threshold for dedicated LIT-Appendix")
            print(f"     Papers will go to LIT-OTHER (OT)")
    else:
        print(f"  ⚠️  Could not find bcm_master.bib")


def list_appendices():
    """List all known LIT-Appendices."""
    print("\n" + "=" * 70)
    print("EBF LIT-Appendices Overview")
    print("=" * 70)

    print("\n\033[1mLIT-R (Researcher-based):\033[0m\n")
    print(f"{'Code':<8} {'Name':<20} {'Primary Author':<25}")
    print("-" * 55)
    for key, data in sorted(LIT_R_APPENDICES.items(), key=lambda x: x[1]["code"]):
        print(f"{data['code']:<8} {data['name']:<20} {key.title():<25}")

    print(f"\n\033[1mLIT-M (Meta/Thematic):\033[0m\n")
    print(f"{'Code':<8} {'Name':<25} {'Keywords':<35}")
    print("-" * 70)
    for key, data in sorted(LIT_M_APPENDICES.items(), key=lambda x: x[1]["code"]):
        kw = ", ".join(data["keywords"][:3])
        print(f"{data['code']:<8} {data['name']:<25} {kw:<35}")

    print(f"\n\033[1mLIT-O Clusters (for OT):\033[0m\n")
    print(f"{'Cluster':<25} {'Example Paper':<40}")
    print("-" * 65)
    for cluster, data in OT_CLUSTERS.items():
        example = data["examples"][0] if data["examples"] else "N/A"
        print(f"{cluster:<25} {example:<40}")

    print("\n" + "=" * 70)
    print(f"Total: {len(LIT_R_APPENDICES)} LIT-R + {len(LIT_M_APPENDICES)} LIT-M + 1 LIT-O")
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="EBF LIT-Appendix Assignment Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    %(prog)s --author "Thaler" --title "Mental Accounting Matters"
    %(prog)s --interactive
    %(prog)s --check-author "Grant"
    %(prog)s --list-appendices
        """
    )

    parser.add_argument("--author", "-a", help="Paper author(s)")
    parser.add_argument("--title", "-t", help="Paper title")
    parser.add_argument("--year", "-y", help="Publication year")
    parser.add_argument("--keywords", "-k", help="Keywords (comma-separated)")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode")
    parser.add_argument("--check-author", help="Check if author qualifies for dedicated LIT")
    parser.add_argument("--list-appendices", "-l", action="store_true", help="List all LIT-Appendices")
    parser.add_argument("--generate-bibtex", "-b", action="store_true", help="Generate BibTeX entry")

    args = parser.parse_args()

    if args.list_appendices:
        list_appendices()
        return 0

    if args.check_author:
        check_author(args.check_author)
        return 0

    if args.interactive:
        interactive_mode()
        return 0

    if args.author and args.title:
        paper = PaperInfo(
            author=args.author,
            title=args.title,
            year=args.year,
            keywords=args.keywords.split(",") if args.keywords else None
        )

        script_dir = Path(__file__).parent
        project_root = script_dir.parent
        bib_path = project_root / "bibliography" / "bcm_master.bib"

        assignment = assign_lit_appendix(paper, bib_path)

        print(f"\n\033[1mLIT Assignment for: {paper.title}\033[0m")
        print("-" * 60)
        print(f"  Appendix: \033[1m{assignment.appendix_name}\033[0m ({assignment.appendix_code})")
        print(f"  Category: {assignment.category}")
        print(f"  Confidence: {assignment.confidence}")
        print(f"  Reasoning: {assignment.reasoning}")
        if assignment.cluster:
            print(f"  OT Cluster: {assignment.cluster}")

        if args.generate_bibtex:
            print("\n" + "-" * 60)
            print("BibTeX Entry:")
            print(generate_bibtex_entry(paper, assignment))

        return 0

    # Default: show help
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
