#!/usr/bin/env python3
"""
Compute B-I-K proxy accuracy scores and triage recommendations for all papers.

B = Bekanntheit (Fame/Visibility) — how well-known is this paper?
I = Inferierbarkeit (Inferability) — how standardized/predictable is the methodology?
K = Komplexität (Complexity) — how many dimensions need extraction?

Based on calibration experiment (2026-02-07) with 10 ground truth papers:
    A_proxy = 0.095 + 0.197·B + 0.152·I - 0.182·K
    R² = 0.774, RMSE = 0.055

Since citation counts are unavailable for most papers, B is estimated from:
    - evidence_tier (journal quality)
    - integration_level (how deeply EBF uses it)
    - content_level (how much we've invested)
    - use_for count (centrality in EBF)
    - author_frequency (how many papers by same author in our BibTeX)
    - full_text availability

Usage:
    python scripts/compute_paper_triage.py                  # Full run
    python scripts/compute_paper_triage.py --stats          # Summary statistics
    python scripts/compute_paper_triage.py --paper PAP-xxx  # Single paper
    python scripts/compute_paper_triage.py --tier proxy     # Filter by triage tier
"""

import os
import sys
import yaml
import re
import argparse
from collections import Counter, defaultdict
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════

PAPER_REFS_DIR = "data/paper-references"
PAPER_TEXTS_DIR = "data/paper-texts"
BIBTEX_PATH = "bibliography/bcm_master.bib"
OUTPUT_PATH = "data/paper-calibration/triage-results.yaml"

# Regression coefficients from calibration (N=10, R²=0.774)
INTERCEPT = 0.095
COEFF_B = 0.197
COEFF_I = 0.152
COEFF_K = -0.182

# Triage thresholds (from calibration analysis)
TRIAGE_THRESHOLDS = {
    "PROXY_OK": 0.45,       # A_proxy >= 0.45 → LLM proxy sufficient for E1-E4
    "PROXY_PLUS_WEB": 0.30, # 0.30 <= A_proxy < 0.45 → proxy + WebSearch
    "FULLTEXT_NEEDED": 0.0, # A_proxy < 0.30 → full text required
}

# ═══════════════════════════════════════════════════════════════════
# B DIMENSION: Bekanntheit (Fame/Visibility)
# ═══════════════════════════════════════════════════════════════════

def compute_B(paper_data, author_freq, has_fulltext):
    """
    Estimate fame/visibility from available metadata.

    Components (all normalized to [0, 1]):
    - b1: evidence_tier (Tier 1 → 1.0, Tier 2 → 0.5, Tier 3 → 0.2)
    - b2: integration_level (I5 → 1.0, I4 → 0.8, I3 → 0.5, I2 → 0.3, I1 → 0.1)
    - b3: use_for_count (normalized: many uses → central paper)
    - b4: author_frequency (prolific author in our DB → likely famous)
    - b5: has_fulltext (we invested in getting it → important)
    - b6: content_level (L3 → 1.0, L2 → 0.6, L1 → 0.2, L0 → 0.0)

    Weights reflect correlation with actual citation counts from calibration:
    b1 (evidence_tier) gets highest weight because journal tier
    is the strongest available proxy for citations.
    """
    ebf = paper_data.get("ebf_integration", {})
    prior = paper_data.get("prior_score", {})
    ft = paper_data.get("full_text", {})

    # b1: Evidence tier → fame proxy (strongest signal)
    tier = ebf.get("evidence_tier", 3)
    if isinstance(tier, str):
        try:
            tier = int(tier)
        except (ValueError, TypeError):
            tier = 3
    b1 = {1: 1.0, 2: 0.5, 3: 0.2, 5: 0.1}.get(tier, 0.2)

    # b2: Integration level → investment proxy
    il = prior.get("integration_level", "I1")
    if isinstance(il, str):
        b2 = {"I5": 1.0, "I4": 0.8, "I3": 0.5, "I2": 0.3, "I1": 0.1}.get(il, 0.1)
    else:
        b2 = 0.1

    # b3: use_for count → centrality proxy
    use_for = ebf.get("use_for", [])
    if isinstance(use_for, list):
        n_uses = len(use_for)
    elif isinstance(use_for, str):
        n_uses = len(use_for.split(","))
    else:
        n_uses = 0
    b3 = min(1.0, n_uses / 8.0)  # 8+ uses → max centrality

    # b4: Author frequency → fame proxy
    author = paper_data.get("author", "")
    if isinstance(author, list):
        # Use first author
        author = author[0] if author else ""
    if isinstance(author, dict):
        author = author.get("family", author.get("name", ""))
    # Normalize author name
    author_key = str(author).strip().split(",")[0].split(" ")[0].lower()
    freq = author_freq.get(author_key, 0)
    b4 = min(1.0, freq / 20.0)  # 20+ papers → max fame

    # b5: Full text available → we invested
    b5 = 1.0 if (has_fulltext or ft.get("available", False)) else 0.0

    # b6: Content level
    cl = prior.get("content_level", ft.get("content_level", "L0"))
    if isinstance(cl, str):
        b6 = {"L3": 1.0, "L2": 0.6, "L1": 0.2, "L0": 0.0}.get(cl, 0.0)
    else:
        b6 = 0.0

    # Weighted combination
    # evidence_tier is strongest citation proxy (weight 0.35)
    # author_frequency is second strongest (weight 0.20)
    # integration_level reflects EBF team assessment (weight 0.15)
    B = (0.35 * b1 + 0.20 * b4 + 0.15 * b2 +
         0.12 * b3 + 0.10 * b5 + 0.08 * b6)

    return min(1.0, max(0.0, B)), {
        "b1_evidence_tier": round(b1, 2),
        "b2_integration_level": round(b2, 2),
        "b3_use_for_count": round(b3, 2),
        "b4_author_frequency": round(b4, 2),
        "b5_has_fulltext": round(b5, 2),
        "b6_content_level": round(b6, 2),
    }


# ═══════════════════════════════════════════════════════════════════
# I DIMENSION: Inferierbarkeit (Inferability)
# ═══════════════════════════════════════════════════════════════════

def compute_I(paper_data):
    """
    Estimate how well methodology can be inferred from metadata.

    Components:
    - i1: publication_type (journal_article → standardized, book → less)
    - i2: identification present (RCT, experimental → highly standardized)
    - i3: theory_support present (established methodology in EBF)
    - i4: year recency (newer → more standardized reporting)
    - i5: evidence_tier (Tier 1 → strict methodology requirements)
    """
    ebf = paper_data.get("ebf_integration", {})

    # i1: Publication type
    pub_type = paper_data.get("publication_type", "unknown")
    i1 = {"journal_article": 0.8, "conference_paper": 0.7,
           "book_chapter": 0.5, "book": 0.4, "working_paper": 0.6,
           "technical_report": 0.5}.get(str(pub_type), 0.3)

    # i2: Identification/methodology type
    ident = ebf.get("identification", "")
    if isinstance(ident, str):
        ident_lower = ident.lower()
        if any(x in ident_lower for x in ["rct", "experimental", "experiment"]):
            i2 = 1.0
        elif any(x in ident_lower for x in ["quasi", "natural_experiment", "did", "iv"]):
            i2 = 0.8
        elif any(x in ident_lower for x in ["survey", "panel", "cross_section"]):
            i2 = 0.6
        elif any(x in ident_lower for x in ["theoretical", "model", "simulation"]):
            i2 = 0.5
        elif ident:
            i2 = 0.4
        else:
            i2 = 0.2
    else:
        i2 = 0.2

    # i3: Theory support present
    ts = ebf.get("theory_support", None)
    if ts:
        if isinstance(ts, list):
            i3 = min(1.0, 0.5 + 0.1 * len(ts))
        else:
            i3 = 0.6
    else:
        i3 = 0.1

    # i4: Year recency (2010+ → 0.8, 2000+ → 0.6, 1990+ → 0.4, older → 0.2)
    year = paper_data.get("year", "2000")
    try:
        year_int = int(str(year).strip("'\""))
    except (ValueError, TypeError):
        year_int = 2000
    if year_int >= 2010:
        i4 = 0.8
    elif year_int >= 2000:
        i4 = 0.6
    elif year_int >= 1990:
        i4 = 0.5
    elif year_int >= 1980:
        i4 = 0.4
    else:
        i4 = 0.2

    # i5: Evidence tier → methodology standardization
    tier = ebf.get("evidence_tier", 3)
    if isinstance(tier, str):
        try:
            tier = int(tier)
        except (ValueError, TypeError):
            tier = 3
    i5 = {1: 0.9, 2: 0.6, 3: 0.3, 5: 0.2}.get(tier, 0.3)

    # Weighted combination
    I = (0.30 * i2 + 0.25 * i5 + 0.20 * i3 + 0.15 * i1 + 0.10 * i4)

    return min(1.0, max(0.0, I)), {
        "i1_publication_type": round(i1, 2),
        "i2_identification": round(i2, 2),
        "i3_theory_support": round(i3, 2),
        "i4_year_recency": round(i4, 2),
        "i5_evidence_tier": round(i5, 2),
    }


# ═══════════════════════════════════════════════════════════════════
# K DIMENSION: Komplexität (Complexity)
# ═══════════════════════════════════════════════════════════════════

def compute_K(paper_data):
    """
    Estimate extraction complexity.

    Components:
    - k1: parameter density (more parameters = harder)
    - k2: multi-CORE usage (spans many dimensions)
    - k3: case_integration present (rich enough for cases = complex)
    - k4: theory count (multiple theories = complex interactions)
    - k5: chapter_relevance count (many chapters = multi-faceted)
    """
    ebf = paper_data.get("ebf_integration", {})

    # k1: Parameter density
    param = ebf.get("parameter", "")
    params_list = ebf.get("parameters", [])
    if isinstance(params_list, list) and params_list:
        n_params = len(params_list)
    elif isinstance(param, str) and param:
        # Count comma-separated parameters
        n_params = len([p for p in param.split(",") if p.strip()])
    else:
        n_params = 0
    k1 = min(1.0, n_params / 10.0)  # 10+ params → max complexity

    # k2: Multi-CORE usage
    use_for = ebf.get("use_for", [])
    if isinstance(use_for, list):
        core_uses = [u for u in use_for if isinstance(u, str) and u.startswith("CORE-")]
    elif isinstance(use_for, str):
        core_uses = [u.strip() for u in use_for.split(",") if "CORE-" in u]
    else:
        core_uses = []
    k2 = min(1.0, len(core_uses) / 5.0)  # 5+ COREs → max complexity

    # k3: Case integration present
    case_int = ebf.get("case_integration", None)
    k3 = 0.7 if case_int else 0.0

    # k4: Theory count
    ts = ebf.get("theory_support", None)
    if isinstance(ts, list):
        n_theories = len(ts)
    elif isinstance(ts, str) and ts:
        n_theories = 1
    else:
        n_theories = 0
    k4 = min(1.0, n_theories / 3.0)  # 3+ theories → max

    # k5: Chapter relevance count
    ch_rel = ebf.get("chapter_relevance", [])
    if isinstance(ch_rel, list):
        n_chapters = len(ch_rel)
    else:
        n_chapters = 0
    k5 = min(1.0, n_chapters / 4.0)  # 4+ chapters → max

    # Weighted combination
    K = (0.30 * k1 + 0.25 * k2 + 0.20 * k4 + 0.15 * k3 + 0.10 * k5)

    return min(1.0, max(0.0, K)), {
        "k1_parameter_density": round(k1, 2),
        "k2_multi_core": round(k2, 2),
        "k3_case_integration": round(k3, 2),
        "k4_theory_count": round(k4, 2),
        "k5_chapter_relevance": round(k5, 2),
    }


# ═══════════════════════════════════════════════════════════════════
# TRIAGE DECISION
# ═══════════════════════════════════════════════════════════════════

def compute_triage(B, I, K):
    """
    Compute proxy accuracy and triage recommendation.

    A_proxy = 0.095 + 0.197·B + 0.152·I - 0.182·K

    Triage:
    - PROXY_OK:        A >= 0.45 → LLM proxy reliable for E1-E4
    - PROXY_PLUS_WEB:  0.30 <= A < 0.45 → need WebSearch augmentation
    - PROXY_PLUS_LLMMC: 0.20 <= A < 0.30 → need LLMMC estimation
    - FULLTEXT_NEEDED:  A < 0.20 → full text required for all fields
    """
    A = INTERCEPT + COEFF_B * B + COEFF_I * I + COEFF_K * K
    A = max(0.0, min(1.0, A))

    if A >= 0.45:
        tier = "PROXY_OK"
        strategy = "LLM proxy for E1-E4, skip E5-E6"
    elif A >= 0.30:
        tier = "PROXY_PLUS_WEB"
        strategy = "LLM + WebSearch for E1-E3, full text for E4-E6"
    elif A >= 0.20:
        tier = "PROXY_PLUS_LLMMC"
        strategy = "LLM + LLMMC estimation, prioritize for full text"
    else:
        tier = "FULLTEXT_NEEDED"
        strategy = "Full text required for all fields"

    return A, tier, strategy


# ═══════════════════════════════════════════════════════════════════
# DATA LOADING
# ═══════════════════════════════════════════════════════════════════

def count_author_frequencies(bibtex_path):
    """Count how often each author appears in the BibTeX file."""
    freq = Counter()
    if not os.path.exists(bibtex_path):
        return freq

    with open(bibtex_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if line.lower().startswith("author"):
                # Extract author names
                match = re.search(r'=\s*\{(.+?)\}', line)
                if match:
                    authors_str = match.group(1)
                    for author in re.split(r'\s+and\s+', authors_str):
                        # Get last name
                        parts = author.strip().split(",")
                        if parts:
                            last = parts[0].strip().lower()
                            if last and len(last) > 1:
                                freq[last] += 1
    return freq


def get_fulltext_papers(texts_dir):
    """Get set of paper keys that have full texts."""
    fulltext_keys = set()
    if os.path.exists(texts_dir):
        for f in os.listdir(texts_dir):
            if f.startswith("PAP-") and f.endswith(".md"):
                key = f[4:-3]  # Remove PAP- and .md
                fulltext_keys.add(key)
    return fulltext_keys


def load_paper_yaml(filepath):
    """Load a single paper YAML file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data if isinstance(data, dict) else None
    except Exception:
        return None


# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="Compute B-I-K triage for all papers")
    parser.add_argument("--stats", action="store_true", help="Show summary statistics")
    parser.add_argument("--paper", type=str, help="Show details for single paper")
    parser.add_argument("--tier", type=str, help="Filter by triage tier")
    parser.add_argument("--top", type=int, default=0, help="Show top N papers by proxy accuracy")
    parser.add_argument("--bottom", type=int, default=0, help="Show bottom N papers")
    parser.add_argument("--save", action="store_true", help="Save results to YAML")
    parser.add_argument("--calibrate", action="store_true", help="Show calibration comparison")
    parser.add_argument("--timing", action="store_true", help="Show timing per step + pipeline estimate")
    args = parser.parse_args()

    import time
    timings = {}

    # ─── Step 1: Load BibTeX author frequencies ───
    t0 = time.time()
    author_freq = count_author_frequencies(BIBTEX_PATH)
    t1 = time.time()
    timings["1_bibtex_authors"] = t1 - t0
    print(f"  [1] BibTeX authors:  {t1-t0:.2f}s ({len(author_freq)} authors)", file=sys.stderr)

    # ─── Step 2: Load full-text list ───
    fulltext_keys = get_fulltext_papers(PAPER_TEXTS_DIR)
    t2 = time.time()
    timings["2_fulltext_scan"] = t2 - t1
    print(f"  [2] Full-text scan:  {t2-t1:.2f}s ({len(fulltext_keys)} full texts)", file=sys.stderr)

    # ─── Step 3: Load all paper YAMLs ───
    results = []
    paper_dir = Path(PAPER_REFS_DIR)
    yaml_files = sorted(paper_dir.glob("PAP-*.yaml"))
    papers_loaded = 0
    papers_data = []
    for yf in yaml_files:
        data = load_paper_yaml(yf)
        if data:
            papers_data.append((yf, data))
            papers_loaded += 1
    t3 = time.time()
    timings["3_yaml_loading"] = t3 - t2
    per_yaml_ms = (t3 - t2) / max(papers_loaded, 1) * 1000
    print(f"  [3] YAML loading:    {t3-t2:.2f}s ({papers_loaded} papers, {per_yaml_ms:.1f}ms/paper)", file=sys.stderr)

    # ─── Step 4: Compute B-I-K for all papers ───
    for yf, data in papers_data:
        paper_key = data.get("paper", data.get("superkey", yf.stem))
        if isinstance(paper_key, str) and paper_key.startswith("PAP-"):
            paper_key = paper_key[4:]

        has_ft = paper_key in fulltext_keys

        B, b_details = compute_B(data, author_freq, has_ft)
        I, i_details = compute_I(data)
        K, k_details = compute_K(data)
        A, tier, strategy = compute_triage(B, I, K)

        results.append({
            "paper_key": paper_key,
            "title": data.get("title", "Unknown")[:80],
            "year": str(data.get("year", "?")),
            "B": round(B, 3),
            "I": round(I, 3),
            "K": round(K, 3),
            "A_proxy": round(A, 3),
            "triage_tier": tier,
            "strategy": strategy,
            "has_fulltext": has_ft,
            "evidence_tier": data.get("ebf_integration", {}).get("evidence_tier", "?"),
            "b_details": b_details,
            "i_details": i_details,
            "k_details": k_details,
        })

    t4 = time.time()
    timings["4_bik_computation"] = t4 - t3
    per_bik_ms = (t4 - t3) / max(len(results), 1) * 1000
    print(f"  [4] B-I-K compute:   {t4-t3:.2f}s ({len(results)} papers, {per_bik_ms:.2f}ms/paper)", file=sys.stderr)

    timings["total_local"] = t4 - t0
    print(f"  [T] TOTAL local:     {t4-t0:.2f}s", file=sys.stderr)

    results.sort(key=lambda x: x["A_proxy"], reverse=True)

    # ─── Timing report ───
    if args.timing:
        tier_counts = Counter(r["triage_tier"] for r in results)
        n_web = tier_counts.get("PROXY_PLUS_WEB", 0)
        n_llmmc = tier_counts.get("PROXY_PLUS_LLMMC", 0)
        n_ft = tier_counts.get("FULLTEXT_NEEDED", 0)
        n_ok = tier_counts.get("PROXY_OK", 0)

        # Per-step LLM extraction time estimates (seconds)
        # Based on empirical measurements with Claude Sonnet API
        T_E1E6_LLM = 3.0        # E1-E6 extraction via LLM (pure, no tools)
        T_WEBSEARCH = 5.0       # WebSearch augmentation per paper
        T_PROXY_CHAIN = 2.0     # Proxy chain inference (z-Tree, N, etc.)
        T_LLMMC = 2.0           # LLMMC parameter estimation
        T_FULLTEXT_READ = 15.0  # Reading + parsing full text
        T_FULLTEXT_EXTRACT = 5.0  # E1-E6 from full text

        print(f"\n{'='*75}")
        print(f"  PIPELINE ZEITSCHÄTZUNG")
        print(f"{'='*75}")
        print(f"\n  LOKALE SCHRITTE (bereits gemessen):")
        print(f"  {'Schritt':<35} {'Zeit':>8} {'Pro Paper':>12}")
        print(f"  {'-'*35} {'-'*8} {'-'*12}")
        print(f"  {'[1] BibTeX-Autoren extrahieren':<35} {timings['1_bibtex_authors']:>7.2f}s {'':>12}")
        print(f"  {'[2] Volltext-Liste scannen':<35} {timings['2_fulltext_scan']:>7.2f}s {'':>12}")
        print(f"  {'[3] YAML-Dateien laden':<35} {timings['3_yaml_loading']:>7.2f}s {per_yaml_ms:>9.1f}ms")
        print(f"  {'[4] B-I-K berechnen':<35} {timings['4_bik_computation']:>7.2f}s {per_bik_ms:>9.2f}ms")
        print(f"  {'TOTAL lokal':<35} {timings['total_local']:>7.2f}s {'':>12}")

        print(f"\n  LLM-EXTRAKTION (geschätzt, sequenziell):")
        print(f"  {'Schritt':<35} {'s/Paper':>8} {'Papers':>7} {'Total':>10}")
        print(f"  {'-'*35} {'-'*8} {'-'*7} {'-'*10}")

        # Round 1
        r1_total = n_web * (T_E1E6_LLM + T_WEBSEARCH + T_PROXY_CHAIN)
        print(f"  {'Runde 1: PROXY_PLUS_WEB':<35}")
        print(f"    {'E1-E6 LLM Extraktion':<33} {T_E1E6_LLM:>7.0f}s {n_web:>7} {n_web*T_E1E6_LLM/60:>8.0f}min")
        print(f"    {'+ WebSearch Augmentation':<33} {T_WEBSEARCH:>7.0f}s {n_web:>7} {n_web*T_WEBSEARCH/60:>8.0f}min")
        print(f"    {'+ Proxy Chain Inferenz':<33} {T_PROXY_CHAIN:>7.0f}s {n_web:>7} {n_web*T_PROXY_CHAIN/60:>8.0f}min")
        print(f"    {'SUBTOTAL Runde 1':<33} {T_E1E6_LLM+T_WEBSEARCH+T_PROXY_CHAIN:>7.0f}s {n_web:>7} {r1_total/60:>8.0f}min")

        # Round 2
        r2_total = n_llmmc * (T_E1E6_LLM + T_LLMMC)
        print(f"  {'Runde 2: PROXY_PLUS_LLMMC':<35}")
        print(f"    {'E1-E6 LLM Extraktion':<33} {T_E1E6_LLM:>7.0f}s {n_llmmc:>7} {n_llmmc*T_E1E6_LLM/60:>8.0f}min")
        print(f"    {'+ LLMMC Estimation':<33} {T_LLMMC:>7.0f}s {n_llmmc:>7} {n_llmmc*T_LLMMC/60:>8.0f}min")
        print(f"    {'SUBTOTAL Runde 2':<33} {T_E1E6_LLM+T_LLMMC:>7.0f}s {n_llmmc:>7} {r2_total/60:>8.0f}min")

        # Round 3
        r3_total = n_ft * (T_FULLTEXT_READ + T_FULLTEXT_EXTRACT)
        print(f"  {'Runde 3: FULLTEXT_NEEDED':<35}")
        print(f"    {'Volltext lesen + parsen':<33} {T_FULLTEXT_READ:>7.0f}s {n_ft:>7} {n_ft*T_FULLTEXT_READ/60:>8.0f}min")
        print(f"    {'E1-E6 Extraktion':<33} {T_FULLTEXT_EXTRACT:>7.0f}s {n_ft:>7} {n_ft*T_FULLTEXT_EXTRACT/60:>8.0f}min")
        print(f"    {'SUBTOTAL Runde 3':<33} {T_FULLTEXT_READ+T_FULLTEXT_EXTRACT:>7.0f}s {n_ft:>7} {r3_total/60:>8.0f}min")

        # Totals
        pipeline_total = r1_total + r2_total + r3_total
        print(f"\n  {'─'*60}")
        print(f"  {'GESAMTE PIPELINE:':<35}")
        print(f"    {'Lokal (B-I-K Triage)':<33} {'':>8} {'':>7} {timings['total_local']:>7.0f}s")
        print(f"    {'Runde 1 (LLM+Web)':<33} {'':>8} {n_web:>7} {r1_total/3600:>7.1f}h")
        print(f"    {'Runde 2 (LLM+LLMMC)':<33} {'':>8} {n_llmmc:>7} {r2_total/3600:>7.1f}h")
        print(f"    {'Runde 3 (Volltext)':<33} {'':>8} {n_ft:>7} {r3_total/3600:>7.1f}h")
        print(f"    {'TOTAL (sequenziell)':<33} {'':>8} {len(results):>7} {pipeline_total/3600:>7.1f}h")

        # Parallelization estimate
        n_parallel = 10  # 10 concurrent LLM calls
        print(f"\n    {'TOTAL (10× parallel)':<33} {'':>8} {'':>7} {pipeline_total/3600/n_parallel:>7.1f}h")
        print(f"    {'TOTAL (50× parallel)':<33} {'':>8} {'':>7} {pipeline_total/3600/50:>7.1f}h")

        # Cost estimate (rough)
        # Sonnet: ~$3/million input tokens, ~$15/million output tokens
        # Average paper extraction: ~2K input tokens, ~1K output tokens
        avg_input_tokens = 2000
        avg_output_tokens = 1000
        cost_per_paper = (avg_input_tokens * 3 + avg_output_tokens * 15) / 1_000_000
        total_cost = len(results) * cost_per_paper
        print(f"\n  KOSTENESCHÄTZUNG (Sonnet API):")
        print(f"    Pro Paper:  ~${cost_per_paper:.4f}")
        print(f"    Total:      ~${total_cost:.2f}")
        print(f"    (Runde 1+WebSearch ist teurer: ~${n_web * cost_per_paper * 2:.2f})")

        return

    # ─── Single paper query ───
    if args.paper:
        key = args.paper.replace("PAP-", "")
        matches = [r for r in results if r["paper_key"] == key]
        if not matches:
            print(f"Paper '{key}' not found.")
            return
        r = matches[0]
        print(f"\n{'='*70}")
        print(f"  PAPER: {r['paper_key']}")
        print(f"  TITLE: {r['title']}")
        print(f"  YEAR:  {r['year']}")
        print(f"{'='*70}")
        print(f"\n  B (Bekanntheit):    {r['B']:.3f}")
        for k, v in r['b_details'].items():
            print(f"    {k}: {v}")
        print(f"\n  I (Inferierbarkeit): {r['I']:.3f}")
        for k, v in r['i_details'].items():
            print(f"    {k}: {v}")
        print(f"\n  K (Komplexität):    {r['K']:.3f}")
        for k, v in r['k_details'].items():
            print(f"    {k}: {v}")
        print(f"\n  A_proxy:  {r['A_proxy']:.3f}")
        print(f"  TRIAGE:   {r['triage_tier']}")
        print(f"  STRATEGY: {r['strategy']}")
        print(f"  FULLTEXT: {'YES' if r['has_fulltext'] else 'NO'}")
        print(f"  EV.TIER:  {r['evidence_tier']}")
        return

    # ─── Calibration comparison ───
    if args.calibrate:
        cal_papers = {
            "fehr1999theory": 0.45,
            "akerlof2000identity": 0.40,
            "PAP-gaechter2008antisocial": 0.30,
            "stigler1977gustibus": 0.25,
            "kahneman2000experienced": 0.30,
            "BeckerGrossmanMurphy1994": 0.20,
            "milkman2021megastudies": 0.15,
            "brynjolfsson_2013_complementarity": 0.10,
            "herhausen2019firestorms": 0.10,
            "enke2024morality": 0.15,
        }
        print(f"\n{'='*80}")
        print(f"  CALIBRATION COMPARISON (10 ground truth papers)")
        print(f"{'='*80}")
        print(f"  {'Paper':<40} {'A_actual':>8} {'A_pred':>8} {'Error':>8} {'Tier':>20}")
        print(f"  {'-'*40} {'-'*8} {'-'*8} {'-'*8} {'-'*20}")

        total_se = 0
        n = 0
        for r in results:
            if r["paper_key"] in cal_papers:
                actual = cal_papers[r["paper_key"]]
                pred = r["A_proxy"]
                err = pred - actual
                total_se += err ** 2
                n += 1
                print(f"  {r['paper_key']:<40} {actual:>8.3f} {pred:>8.3f} {err:>+8.3f} {r['triage_tier']:>20}")

        if n > 0:
            rmse = (total_se / n) ** 0.5
            print(f"\n  RMSE: {rmse:.4f} (N={n})")
        return

    # ─── Filter by tier ───
    if args.tier:
        tier_upper = args.tier.upper()
        filtered = [r for r in results if r["triage_tier"] == tier_upper]
        if not filtered:
            # Try partial match
            filtered = [r for r in results if tier_upper in r["triage_tier"]]
        results_show = filtered
    elif args.top > 0:
        results_show = results[:args.top]
    elif args.bottom > 0:
        results_show = results[-args.bottom:]
    else:
        results_show = results

    # ─── Statistics ───
    tier_counts = Counter(r["triage_tier"] for r in results)
    ft_by_tier = defaultdict(int)
    for r in results:
        if r["has_fulltext"]:
            ft_by_tier[r["triage_tier"]] += 1

    if args.stats or not (args.tier or args.top or args.bottom):
        print(f"\n{'='*70}")
        print(f"  B-I-K TRIAGE RESULTS ({len(results)} papers)")
        print(f"{'='*70}")
        print(f"\n  DISTRIBUTION:")
        for tier in ["PROXY_OK", "PROXY_PLUS_WEB", "PROXY_PLUS_LLMMC", "FULLTEXT_NEEDED"]:
            count = tier_counts.get(tier, 0)
            ft = ft_by_tier.get(tier, 0)
            pct = 100 * count / len(results) if results else 0
            bar = "█" * int(pct / 2)
            print(f"  {tier:<20} {count:>5} ({pct:>5.1f}%) {bar}")
            if ft > 0:
                print(f"  {'':20} (already have {ft} full texts)")

        # Summary stats
        A_values = [r["A_proxy"] for r in results]
        B_values = [r["B"] for r in results]
        I_values = [r["I"] for r in results]
        K_values = [r["K"] for r in results]

        print(f"\n  DIMENSION STATISTICS:")
        print(f"  {'':15} {'Mean':>8} {'Median':>8} {'Min':>8} {'Max':>8}")
        for name, vals in [("B (Fame)", B_values), ("I (Infer)", I_values),
                           ("K (Complex)", K_values), ("A (Proxy)", A_values)]:
            sorted_v = sorted(vals)
            mean = sum(vals) / len(vals) if vals else 0
            median = sorted_v[len(sorted_v)//2] if sorted_v else 0
            print(f"  {name:<15} {mean:>8.3f} {median:>8.3f} {sorted_v[0]:>8.3f} {sorted_v[-1]:>8.3f}")

        # Full-text gap analysis
        ft_count = sum(1 for r in results if r["has_fulltext"])
        need_ft = tier_counts.get("FULLTEXT_NEEDED", 0)
        need_ft_no_ft = need_ft - ft_by_tier.get("FULLTEXT_NEEDED", 0)

        print(f"\n  FULLTEXT GAP ANALYSIS:")
        print(f"  Total papers:           {len(results)}")
        print(f"  Have full text:         {ft_count}")
        print(f"  Need full text (tier):  {need_ft}")
        print(f"  CRITICAL GAP:           {need_ft_no_ft} papers need full text but don't have it")

        # EBF-specific: PCT readiness
        pct_ready = sum(1 for r in results if r["A_proxy"] >= 0.30)
        print(f"\n  PCT READINESS (A_proxy >= 0.30):")
        print(f"  PCT-ready papers:       {pct_ready} ({100*pct_ready/len(results):.1f}%)")
        print(f"  Need more extraction:   {len(results) - pct_ready}")

    # ─── Detailed output ───
    if args.tier or args.top or args.bottom:
        print(f"\n  {'Paper':<40} {'Year':>5} {'B':>6} {'I':>6} {'K':>6} {'A':>6} {'Tier':>20} {'FT':>3}")
        print(f"  {'-'*40} {'-'*5} {'-'*6} {'-'*6} {'-'*6} {'-'*6} {'-'*20} {'-'*3}")
        for r in results_show:
            ft_mark = "YES" if r["has_fulltext"] else ""
            print(f"  {r['paper_key']:<40} {r['year']:>5} {r['B']:>6.3f} {r['I']:>6.3f} "
                  f"{r['K']:>6.3f} {r['A_proxy']:>6.3f} {r['triage_tier']:>20} {ft_mark:>3}")

    # ─── Save results ───
    if args.save:
        output = {
            "metadata": {
                "date": "2026-02-07",
                "model": "B-I-K OLS (N=10 calibration, R²=0.774)",
                "n_papers": len(results),
                "regression": {
                    "intercept": INTERCEPT,
                    "coeff_B": COEFF_B,
                    "coeff_I": COEFF_I,
                    "coeff_K": COEFF_K,
                    "R_squared": 0.774,
                    "RMSE": 0.055,
                },
            },
            "summary": {
                "tier_distribution": dict(tier_counts),
                "fulltext_by_tier": dict(ft_by_tier),
                "mean_A": round(sum(r["A_proxy"] for r in results) / len(results), 3),
                "pct_ready_count": sum(1 for r in results if r["A_proxy"] >= 0.30),
            },
            "papers": [{
                "paper_key": r["paper_key"],
                "B": r["B"],
                "I": r["I"],
                "K": r["K"],
                "A_proxy": r["A_proxy"],
                "triage_tier": r["triage_tier"],
                "has_fulltext": r["has_fulltext"],
                "evidence_tier": r["evidence_tier"],
            } for r in results],
        }

        os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
        with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
            yaml.dump(output, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        print(f"\n  Results saved to {OUTPUT_PATH}", file=sys.stderr)


if __name__ == "__main__":
    main()
