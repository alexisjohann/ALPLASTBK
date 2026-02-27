#!/usr/bin/env python3
"""
Upgrade PAP-*.yaml files to Content Level L2.
==============================================
Extracts S1-S4 structural characteristics from abstracts using keyword
heuristics. Adds use_for, theory_support, and sets content_level: L2.

Works entirely LOCALLY — no external API calls.

Usage:
    # Stage 1: Process 1 paper (preview)
    python scripts/upgrade_papers_to_l2.py --batch 1 --dry-run

    # Stage 2: Process 10 papers
    python scripts/upgrade_papers_to_l2.py --batch 10

    # Stage 3: Process 100 papers
    python scripts/upgrade_papers_to_l2.py --batch 100

    # Stage 4: Process all
    python scripts/upgrade_papers_to_l2.py --batch 0

    # Experimental mode (geometric scaling with quality gates)
    python scripts/upgrade_papers_to_l2.py --experimental

    # Filter by author
    python scripts/upgrade_papers_to_l2.py --author sutter --batch 10
"""

import argparse
import re
import sys
import yaml
from pathlib import Path
from datetime import date

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PAPER_DIR = Path("data/paper-references")
BIB_FILE = Path("bibliography/bcm_master.bib")

# Theory keywords → MS-XX-XXX mapping
THEORY_KEYWORDS = {
    # Social Preferences
    "MS-SP-001": ["inequity aversion", "fairness", "unfair", "inequality aversion",
                   "fehr.*schmidt", "disadvantageous inequality"],
    "MS-SP-002": ["reciproc", "conditional cooperat", "reciprocal"],
    # Public Goods
    "MS-PG-001": ["public good", "free rid", "voluntary contribution",
                   "social dilemma", "cooperation game"],
    "MS-PG-002": ["punishment", "sanction", "peer punishment", "costly punishment"],
    # Prospect Theory / Risk
    "MS-RD-001": ["prospect theory", "loss aversion", "reference point",
                   "risk attitude", "kahneman.*tversky"],
    "MS-RD-002": ["risk preference", "risk taking", "gamble", "lottery",
                   "ambiguity aversion"],
    # Time Preferences
    "MS-TP-001": ["time preference", "patience", "impatien", "discount",
                   "present bias", "delay", "intertemporal"],
    # Trust
    "MS-TR-001": ["trust game", "trust", "trustworth", "betrayal"],
    # Bargaining
    "MS-BG-001": ["ultimatum", "bargain", "dictator game", "offer",
                   "proposer", "responder"],
    # Competition
    "MS-CM-001": ["tournament", "competi", "contest", "winner.*take",
                   "performance.*incentive"],
    # Gender
    "MS-GE-001": ["gender differ", "gender gap", "women", "female",
                   "sex differ", "gender"],
    # Behavioral IO
    "MS-IO-001": ["market", "auction", "bidding", "trading", "asset market"],
    # Education / Children
    "MS-ED-001": ["child", "adolescen", "school", "student", "education",
                   "cognitive", "development"],
}

# use_for domain mapping (keyword → DOMAIN/CORE)
DOMAIN_KEYWORDS = {
    "CORE-HOW": ["interaction", "mechanism", "complementar", "strategic",
                  "game theor", "incentive design"],
    "CORE-WHAT": ["utility", "preference", "well-being", "welfare",
                   "happiness", "satisfaction"],
    "CORE-WHEN": ["context", "framing", "default", "choice architect"],
    "CORE-WHO": ["heterogene", "individual differ", "type", "population"],
    "CORE-AWARE": ["information", "feedback", "awareness", "transparent",
                    "salien"],
    "DOMAIN-INSTITUTIONS": ["institution", "governance", "rule", "regulation",
                             "policy", "voting", "democracy"],
    "DOMAIN-LABOR": ["labor", "labour", "worker", "employ", "wage",
                      "workplace", "team"],
    "DOMAIN-HEALTH": ["health", "medical", "patient", "organ donat"],
    "DOMAIN-FINANCE": ["finance", "invest", "saving", "stock", "portfolio",
                        "pension", "retirement"],
    "DOMAIN-EDUCATION": ["education", "school", "student", "learn",
                          "teaching", "university"],
    "DOMAIN-ENVIRONMENT": ["environment", "climate", "energy", "emission",
                            "sustainab"],
}

# Methodology keywords for S2
METHODOLOGY_KEYWORDS = [
    "experiment", "survey", "field study", "field experiment", "lab experiment",
    "laboratory", "rct", "randomized", "randomised", "regression",
    "estimation", "empirical", "model", "simulation", "treatment",
    "control group", "between-subject", "within-subject", "panel data",
    "cross-section", "time series", "meta-analysis", "natural experiment",
    "instrumental variable", "difference-in-difference", "quasi-experiment",
    "game", "incentivized", "artefactual", "online experiment",
]

# Sample/Data keywords for S3
SAMPLE_KEYWORDS = [
    "subject", "participant", "observation", "sample", "respondent",
    "student", "children", "adolescent", "household", "firm",
    "countr", "nation", "dataset", "data set", "panel", "census",
    "n =", "n=", r"\d+ (subjects|participants|students|children)",
    "waves", "round", "period", "session",
]

# Findings keywords for S4
FINDINGS_KEYWORDS = [
    "find", "found", "result", "show", "demonstrat", "evidence",
    "effect", "significant", "increas", "decreas", "conclude",
    "impact", "reduc", "improv", "suggest", "indicat", "confirm",
    "correlat", "associat", "predict", "outperform", "robust",
]


# ---------------------------------------------------------------------------
# Extraction logic
# ---------------------------------------------------------------------------

def text_matches(text: str, keywords: list) -> bool:
    """Check if text matches any keyword (case-insensitive regex)."""
    text_lower = text.lower()
    for kw in keywords:
        if re.search(kw.lower(), text_lower):
            return True
    return False


def extract_s1(abstract: str, title: str) -> bool:
    """S1: Research Question. True if abstract exists with >50 chars."""
    return len(abstract.strip()) > 50


def extract_s2(abstract: str, title: str) -> bool:
    """S2: Methodology identifiable from abstract."""
    combined = f"{title} {abstract}"
    return text_matches(combined, METHODOLOGY_KEYWORDS)


def extract_s3(abstract: str, title: str) -> bool:
    """S3: Sample/Data mentioned."""
    combined = f"{title} {abstract}"
    return text_matches(combined, SAMPLE_KEYWORDS)


def extract_s4(abstract: str, title: str) -> bool:
    """S4: Findings reported."""
    return text_matches(abstract, FINDINGS_KEYWORDS)


def detect_theories(abstract: str, title: str) -> list:
    """Detect theory support from keywords."""
    combined = f"{title} {abstract}"
    theories = []
    for theory_id, keywords in THEORY_KEYWORDS.items():
        if text_matches(combined, keywords):
            theories.append(theory_id)
    return sorted(theories)


def detect_domains(abstract: str, title: str) -> list:
    """Detect use_for domains from keywords."""
    combined = f"{title} {abstract}"
    domains = []
    for domain, keywords in DOMAIN_KEYWORDS.items():
        if text_matches(combined, keywords):
            domains.append(domain)
    return sorted(domains)


def detect_methodology_type(abstract: str, title: str) -> str:
    """Classify methodology type."""
    combined = f"{title} {abstract}".lower()
    if any(kw in combined for kw in ["lab experiment", "laboratory"]):
        return "lab_experiment"
    if any(kw in combined for kw in ["field experiment", "natural experiment"]):
        return "field_experiment"
    if any(kw in combined for kw in ["survey", "questionnaire"]):
        return "survey"
    if any(kw in combined for kw in ["meta-analysis", "meta analysis"]):
        return "meta_analysis"
    if any(kw in combined for kw in ["regression", "panel data", "cross-section"]):
        return "econometric"
    if "experiment" in combined:
        return "experiment"
    if any(kw in combined for kw in ["theor", "model", "proof"]):
        return "theoretical"
    return "empirical"


def extract_key_findings(abstract: str) -> list:
    """Extract key findings as bullet points from abstract."""
    findings = []

    # Split on sentence boundaries
    sentences = re.split(r'(?<=[.!?])\s+', abstract)

    for sent in sentences:
        sent = sent.strip()
        if not sent or len(sent) < 20:
            continue
        # Check if sentence contains findings language
        if text_matches(sent, FINDINGS_KEYWORDS):
            # Clean up the sentence
            clean = re.sub(r'\s+', ' ', sent).strip()
            if clean and clean not in findings:
                findings.append(clean)

    return findings[:5]  # Max 5 findings


def determine_evidence_tier(data: dict) -> int:
    """Estimate evidence tier from available metadata."""
    # Check if we have journal info from the BibTeX key or doi
    doi = data.get("doi", "")
    bibtex_key = data.get("bibtex_key", data.get("id", ""))

    # Tier 1: Top journals (AER, QJE, Econometrica, JPE, REStud, Science, Nature)
    # We can't easily check journal from YAML alone, default to 2
    # Tier 2: Peer-reviewed
    if doi:
        return 2  # Has DOI = likely peer-reviewed

    # Tier 3: Working paper / preprint
    return 3


def upgrade_paper(data: dict, author_filter: str = "") -> dict:
    """Upgrade a paper YAML to L2 by extracting S1-S4 and EBF fields."""
    abstract = data.get("abstract", "")
    title = data.get("title", "")
    bibtex_key = data.get("bibtex_key", data.get("id", "").replace("PAP-", ""))

    if not abstract or len(abstract.strip()) < 30:
        return None  # Can't upgrade without abstract

    # Already has content_level L2+?
    existing_cl = None
    if "full_text" in data and isinstance(data["full_text"], dict):
        existing_cl = data["full_text"].get("content_level")
    if existing_cl in ("L2", "L3"):
        return None  # Already upgraded

    # Check structural_characteristics
    if "structural_characteristics" in data:
        sc = data["structural_characteristics"]
        if sc.get("S1_research_question") and sc.get("S4_findings"):
            return None  # Already has S1+S4 at minimum

    # --- Extract S1-S4 ---
    s1 = extract_s1(abstract, title)
    s2 = extract_s2(abstract, title)
    s3 = extract_s3(abstract, title)
    s4 = extract_s4(abstract, title)

    # Must have at least S1 + one more for L2
    if not s1:
        return None

    content_level = "L2" if (s1 and s2 and s4) else "L1"

    # --- Detect theories and domains ---
    theories = detect_theories(abstract, title)
    domains = detect_domains(abstract, title)

    # Always include LIT-SUT for Sutter papers
    lit_appendix = None
    if author_filter:
        lit_code = author_filter.upper()[:3]
        lit_appendix = f"LIT-{lit_code}"

    use_for = list(set(domains))
    if lit_appendix and lit_appendix not in use_for:
        use_for.append(lit_appendix)
    use_for = sorted(use_for)

    # --- Extract key findings ---
    key_findings = extract_key_findings(abstract)

    # --- Detect methodology ---
    methodology = detect_methodology_type(abstract, title)

    # --- Evidence tier ---
    evidence_tier = determine_evidence_tier(data)

    # --- Build upgraded data ---
    # Structural characteristics
    data["structural_characteristics"] = {
        "S1_research_question": s1,
        "S2_methodology": s2,
        "S3_sample_data": s3,
        "S4_findings": s4,
        "S5_validity": False,
        "S6_reproducibility": False,
    }

    # Full text section
    if "full_text" not in data or not isinstance(data.get("full_text"), dict):
        data["full_text"] = {
            "available": False,
            "path": None,
            "content_level": content_level,
        }
    else:
        data["full_text"]["content_level"] = content_level

    # EBF integration
    if "ebf_integration" not in data or not isinstance(data.get("ebf_integration"), dict):
        data["ebf_integration"] = {}

    ebf = data["ebf_integration"]
    if not ebf.get("use_for"):
        ebf["use_for"] = use_for
    if not ebf.get("theory_support") and theories:
        ebf["theory_support"] = ", ".join(theories)
    if not ebf.get("evidence_tier"):
        ebf["evidence_tier"] = evidence_tier
    if not ebf.get("identification"):
        ebf["identification"] = methodology
    if not ebf.get("external_validity"):
        ebf["external_validity"] = "pending_review"

    # Key findings in summary
    if key_findings and "summary" not in data:
        data["summary"] = {
            "key_findings": key_findings,
        }

    # Upgrade metadata
    data["l2_upgrade_date"] = str(date.today())
    data["l2_upgrade_method"] = "keyword_heuristic_v1"

    return data


# ---------------------------------------------------------------------------
# Main processing
# ---------------------------------------------------------------------------

def process_papers(batch: int = 0, dry_run: bool = False,
                   author: str = "", verbose: bool = False):
    """Process papers and upgrade to L2."""
    yaml_files = sorted(PAPER_DIR.glob("PAP-*.yaml"))

    if author:
        yaml_files = [f for f in yaml_files if author.lower() in f.name.lower()]

    print(f"{'=' * 60}")
    print(f"  UPGRADE PAPERS TO L2")
    print(f"{'=' * 60}")
    print(f"  Total YAML files: {len(yaml_files)}")
    print(f"  Author filter:    {author or 'none'}")
    print(f"  Batch size:       {batch or 'all'}")
    print(f"  Dry run:          {dry_run}")
    print()

    # Stats
    stats = {
        "total": len(yaml_files),
        "processed": 0,
        "upgraded": 0,
        "skipped_no_abstract": 0,
        "skipped_already_l2": 0,
        "l2_count": 0,
        "l1_count": 0,
        "theories_detected": 0,
        "domains_detected": 0,
    }

    upgraded_files = []

    for i, yaml_file in enumerate(yaml_files):
        if batch > 0 and stats["upgraded"] >= batch:
            break

        try:
            with open(yaml_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except Exception as e:
            print(f"  ERROR reading {yaml_file.name}: {e}")
            continue

        if not data:
            continue

        stats["processed"] += 1
        result = upgrade_paper(data, author)

        if result is None:
            # Check why skipped
            abstract = data.get("abstract", "")
            if not abstract or len(abstract.strip()) < 30:
                stats["skipped_no_abstract"] += 1
            else:
                stats["skipped_already_l2"] += 1
            continue

        # Count results
        cl = result.get("full_text", {}).get("content_level", "")
        if cl == "L2":
            stats["l2_count"] += 1
        else:
            stats["l1_count"] += 1

        theories = result.get("ebf_integration", {}).get("theory_support", "")
        if theories:
            stats["theories_detected"] += 1

        domains = result.get("ebf_integration", {}).get("use_for", [])
        if len(domains) > 1:  # More than just LIT-SUT
            stats["domains_detected"] += 1

        stats["upgraded"] += 1
        upgraded_files.append(yaml_file)

        if verbose or batch <= 10:
            print(f"  [{stats['upgraded']}/{batch or '?'}] {yaml_file.name}")
            print(f"    Content Level: {cl}")
            s = result.get("structural_characteristics", {})
            print(f"    S1={s.get('S1_research_question')}, "
                  f"S2={s.get('S2_methodology')}, "
                  f"S3={s.get('S3_sample_data')}, "
                  f"S4={s.get('S4_findings')}")
            if theories:
                print(f"    Theories: {theories}")
            print(f"    Use-for: {', '.join(domains)}")
            findings = result.get("summary", {}).get("key_findings", [])
            if findings:
                print(f"    Findings: {len(findings)} extracted")
            print()

        # Write back
        if not dry_run:
            with open(yaml_file, "w", encoding="utf-8") as f:
                yaml.dump(result, f, default_flow_style=False,
                          allow_unicode=True, sort_keys=False, width=120)

    # --- Summary ---
    print(f"{'=' * 60}")
    print(f"  SUMMARY")
    print(f"{'=' * 60}")
    print(f"  Processed:        {stats['processed']}")
    print(f"  Upgraded:         {stats['upgraded']}")
    print(f"    → L2:           {stats['l2_count']}")
    print(f"    → L1:           {stats['l1_count']}")
    print(f"  Skipped:")
    print(f"    No abstract:    {stats['skipped_no_abstract']}")
    print(f"    Already L2+:    {stats['skipped_already_l2']}")
    print(f"  Theories found:   {stats['theories_detected']}")
    print(f"  Domains found:    {stats['domains_detected']}")

    if dry_run:
        print(f"\n  [DRY RUN] No files were modified.")

    return stats, upgraded_files


def main():
    parser = argparse.ArgumentParser(
        description="Upgrade PAP-*.yaml files to Content Level L2",
    )
    parser.add_argument("--batch", type=int, default=0,
                        help="Number of papers to process (0=all)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview only, don't modify files")
    parser.add_argument("--author", default="",
                        help="Filter by author name in filename")
    parser.add_argument("--verbose", action="store_true",
                        help="Show details for each paper")
    parser.add_argument("--experimental", action="store_true",
                        help="Geometric scaling: 1→10→100→all with gates")

    args = parser.parse_args()

    if args.experimental:
        stages = [1, 10, 100, 0]
        for stage_batch in stages:
            label = stage_batch if stage_batch > 0 else "ALL"
            print(f"\n{'#' * 60}")
            print(f"  EXPERIMENTAL STAGE: {label}")
            print(f"{'#' * 60}\n")

            stats, files = process_papers(
                batch=stage_batch,
                dry_run=args.dry_run,
                author=args.author,
                verbose=(stage_batch <= 10),
            )

            if stage_batch > 0 and stage_batch < 100:
                print(f"\n  Quality gate: Review {stage_batch} results above.")
                print(f"  Press Enter to continue or Ctrl+C to abort.")
                try:
                    input()
                except (KeyboardInterrupt, EOFError):
                    print("\n  Aborted.")
                    sys.exit(0)
    else:
        process_papers(
            batch=args.batch,
            dry_run=args.dry_run,
            author=args.author,
            verbose=args.verbose,
        )


if __name__ == "__main__":
    main()
