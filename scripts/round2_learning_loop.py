#!/usr/bin/env python3
"""
Round 2 Learning Loop: Iterative Paper Extraction with Active Learning.

Instead of extracting all 2,593 papers at once, this script implements
an iterative learning loop:

  Batch 1: 20 papers (stratified) → Extract → Measure → Learn
  Batch 2: 30 papers (adapted)    → Extract → Measure → Learn
  Batch 3: 50 papers (optimized)  → Extract → Measure → Learn
  Batch 4: 100 papers (scaled)    → Extract → Measure → Learn
  BULK:    Rest with optimized pipeline

Each iteration:
  1. Selects papers strategically (stratified by tier, methodology, fame)
  2. Extracts E1-E6 elements (simulated locally, real via LLM API)
  3. Measures quality against ground truth and cross-validation
  4. Identifies systematic errors and prompt improvements
  5. Updates B-I-K regression model (growing N from 10 → 60 → 110 → 210)
  6. Logs timing, accuracy, and error patterns

Usage:
    python scripts/round2_learning_loop.py --plan              # Show iteration plan
    python scripts/round2_learning_loop.py --select-batch 1    # Select papers for batch N
    python scripts/round2_learning_loop.py --evaluate-batch 1  # Evaluate batch results
    python scripts/round2_learning_loop.py --update-model      # Refit B-I-K regression
    python scripts/round2_learning_loop.py --status            # Show learning progress
    python scripts/round2_learning_loop.py --dashboard         # Full dashboard
    python scripts/round2_learning_loop.py --improve-proxies   # Apply newly discovered proxies
    python scripts/round2_learning_loop.py --hypotheses 1      # Show pre-batch hypotheses for batch N
    python scripts/round2_learning_loop.py --verdict 1         # Evaluate hypotheses against results
"""

import os
import sys
import yaml
import re
import json
import argparse
import math
import time
from collections import Counter, defaultdict
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════

PAPER_REFS_DIR = "data/paper-references"
PAPER_TEXTS_DIR = "data/paper-texts"
BIBTEX_PATH = "bibliography/bcm_master.bib"
CALIBRATION_DIR = "data/paper-calibration"
LEARNING_LOG_PATH = "data/paper-calibration/learning-log.yaml"
TRIAGE_RESULTS_PATH = "data/paper-calibration/triage-results.yaml"

# Batch configuration (papers per iteration)
BATCH_SIZES = [20, 30, 50, 100]  # Total: 200 papers before bulk

# E1-E6 EBF extraction elements
E_ELEMENTS = {
    "E1": "Parameter (θ) — behavioral economics parameters with values",
    "E2": "Context (Ψ) — measurement context and conditions",
    "E3": "Theory (MS) — theory catalog mapping",
    "E4": "Complementarity (γ) — interaction effects between dimensions",
    "E5": "Validity (τ) — internal/external validity assessment",
    "E6": "Case (CAS) — case registry integration",
}

# Stratification dimensions for batch selection
STRATA = {
    "tier": ["PROXY_PLUS_WEB", "PROXY_PLUS_LLMMC", "FULLTEXT_NEEDED"],
    "method": ["experiment", "survey", "theory", "meta-analysis", "field", "other"],
    "fame": ["high", "medium", "low"],  # Based on B-dimension
    "has_fulltext": [True, False],
}

# ═══════════════════════════════════════════════════════════════════
# PROXY IMPROVEMENTS (from metadata analysis)
# ═══════════════════════════════════════════════════════════════════

# Title keywords → methodology type mapping
TITLE_METHOD_KEYWORDS = {
    "experiment": ["experiment", "experimental", "lab experiment", "laboratory"],
    "field": ["field experiment", "field study", "natural experiment", "rct", "randomized"],
    "survey": ["survey", "questionnaire", "panel data", "cross-section"],
    "theory": ["theory", "theoretical", "model", "framework", "axiom"],
    "meta-analysis": ["meta-analysis", "meta analysis", "systematic review", "review"],
    "quasi": ["quasi-experiment", "difference-in-difference", "regression discontinuity",
              "instrumental variable", "did", "iv"],
}

# DOI prefix → journal mapping for evidence tier refinement
DOI_JOURNAL_MAP = {
    "10.1257": {"name": "AEA (AER, AEJ, JEL, JEP)", "tier": 1, "fame_boost": 0.2},
    "10.1086": {"name": "UChicago (JPE, JLE)", "tier": 1, "fame_boost": 0.15},
    "10.1093": {"name": "Oxford (QJE, REStud, JEEA)", "tier": 1, "fame_boost": 0.15},
    "10.1111": {"name": "Wiley (Econometrica, JMCB)", "tier": 1, "fame_boost": 0.1},
    "10.3982": {"name": "Econometrica", "tier": 1, "fame_boost": 0.2},
    "10.2307": {"name": "JSTOR (mixed)", "tier": 2, "fame_boost": 0.05},
    "10.1016": {"name": "Elsevier (JDE, GEB, JHE)", "tier": 2, "fame_boost": 0.05},
    "10.1007": {"name": "Springer (JEBO, ExpEcon)", "tier": 2, "fame_boost": 0.05},
    "10.3386": {"name": "NBER Working Papers", "tier": 2, "fame_boost": 0.1},
    "10.2139": {"name": "SSRN", "tier": 3, "fame_boost": 0.0},
}

# Abstract method signal words
ABSTRACT_METHOD_SIGNALS = [
    "randomized", "experiment", "treatment group", "control group",
    "rct", "survey", "panel", "cross-section", "instrumental variable",
    "regression discontinuity", "difference-in-difference", "lab",
    "field study", "meta-analysis", "n =", "participants", "subjects",
    "between-subject", "within-subject", "incentivized",
]


def load_paper_yamls():
    """Load all paper YAML files."""
    papers = {}
    for fname in sorted(os.listdir(PAPER_REFS_DIR)):
        if not fname.endswith(".yaml"):
            continue
        try:
            with open(os.path.join(PAPER_REFS_DIR, fname)) as f:
                data = yaml.safe_load(f)
            if data:
                key = fname.replace(".yaml", "")
                papers[key] = data
        except Exception:
            pass
    return papers


def load_triage_results():
    """Load existing triage results. Converts list format to dict for fast lookup."""
    if os.path.exists(TRIAGE_RESULTS_PATH):
        with open(TRIAGE_RESULTS_PATH) as f:
            data = yaml.safe_load(f) or {}
        # Convert papers list to dict keyed by paper_key
        if isinstance(data.get("papers"), list):
            papers_dict = {}
            for p in data["papers"]:
                key = p.get("paper_key", "")
                if key:
                    papers_dict[f"PAP-{key}" if not key.startswith("PAP-") else key] = {
                        "B": p.get("B", 0.3),
                        "I": p.get("I", 0.4),
                        "K": p.get("K", 0.0),
                        "A_proxy": p.get("A_proxy", 0.2),
                        "tier": p.get("triage_tier", "PROXY_PLUS_LLMMC"),
                        "has_fulltext": p.get("has_fulltext", False),
                    }
            data["papers"] = papers_dict
        return data
    return {"papers": {}}


def load_learning_log():
    """Load learning log from previous iterations."""
    if os.path.exists(LEARNING_LOG_PATH):
        with open(LEARNING_LOG_PATH) as f:
            return yaml.safe_load(f) or {"iterations": [], "metrics": {}}
    return {"iterations": [], "metrics": {}, "model_updates": [], "proxy_improvements": []}


def save_learning_log(log):
    """Save learning log."""
    os.makedirs(os.path.dirname(LEARNING_LOG_PATH), exist_ok=True)
    with open(LEARNING_LOG_PATH, "w") as f:
        yaml.dump(log, f, default_flow_style=False, allow_unicode=True, width=120)


# ═══════════════════════════════════════════════════════════════════
# IMPROVED PROXY COMPUTATION
# ═══════════════════════════════════════════════════════════════════

def extract_method_from_title(title):
    """Extract methodology type from paper title."""
    if not title:
        return "other"
    title_lower = title.lower()
    for method, keywords in TITLE_METHOD_KEYWORDS.items():
        for kw in keywords:
            if kw in title_lower:
                return method
    return "other"


def extract_journal_from_doi(doi):
    """Extract journal info from DOI prefix."""
    if not doi:
        return None
    doi_str = str(doi)
    for prefix, info in DOI_JOURNAL_MAP.items():
        if doi_str.startswith(prefix):
            return info
    return None


def count_abstract_method_signals(abstract):
    """Count methodology signal words in abstract."""
    if not abstract:
        return 0
    abstract_lower = str(abstract).lower()
    count = 0
    for signal in ABSTRACT_METHOD_SIGNALS:
        if signal in abstract_lower:
            count += 1
    return count


def compute_ebf_reference_count(paper_key, all_papers):
    """Count how many other papers reference this paper in their YAMLs."""
    count = 0
    clean_key = paper_key.replace("PAP-", "")
    for other_key, other_data in all_papers.items():
        if other_key == paper_key:
            continue
        yaml_str = str(other_data)
        if clean_key in yaml_str:
            count += 1
    return count


def has_structural_characteristics(paper_data):
    """Check if paper has structural_characteristics field."""
    return bool(paper_data.get("structural_characteristics"))


def improved_B(paper_data, base_B, doi_info=None, ebf_ref_count=0):
    """Improve B-dimension with new proxies."""
    boost = 0.0

    # DOI-based journal fame boost
    if doi_info:
        boost += doi_info.get("fame_boost", 0.0) * 0.3

    # EBF reference count boost (papers cited >5 times are more important)
    if ebf_ref_count > 5:
        boost += min(0.1, (ebf_ref_count - 5) * 0.02)

    # use_for count >= 4 indicates centrality
    use_for = paper_data.get("ebf_integration", {}).get("use_for", [])
    if isinstance(use_for, list) and len(use_for) >= 4:
        boost += 0.05

    return min(1.0, base_B + boost)


def improved_I(paper_data, base_I, method_type="other", abstract_signals=0):
    """Improve I-dimension with new proxies."""
    boost = 0.0

    # Method type from title
    method_boosts = {
        "experiment": 0.08, "field": 0.10, "quasi": 0.06,
        "survey": 0.04, "meta-analysis": 0.05,
        "theory": -0.05, "other": 0.0,
    }
    boost += method_boosts.get(method_type, 0.0)

    # Abstract method signals (more signals → more standardized methodology)
    if abstract_signals >= 3:
        boost += 0.06
    elif abstract_signals >= 1:
        boost += 0.03

    return max(0.0, min(1.0, base_I + boost))


def improved_K(paper_data, base_K):
    """Improve K-dimension with new proxies."""
    boost = 0.0

    # structural_characteristics present → complex paper
    if has_structural_characteristics(paper_data):
        boost += 0.25

    # Full text available → we invested in it → likely complex/important
    ft = paper_data.get("full_text", {})
    if isinstance(ft, dict) and ft.get("available"):
        boost += 0.10

    # Has CORE in use_for → structurally important
    use_for = paper_data.get("ebf_integration", {}).get("use_for", [])
    if isinstance(use_for, list):
        core_count = sum(1 for u in use_for if str(u).startswith("CORE"))
        if core_count > 0:
            boost += 0.10 * min(core_count, 3)

    return max(0.0, min(1.0, base_K + boost))


# ═══════════════════════════════════════════════════════════════════
# BATCH SELECTION (Stratified Sampling)
# ═══════════════════════════════════════════════════════════════════

def classify_paper_for_stratification(paper_key, paper_data, triage):
    """Classify a paper across all stratification dimensions."""
    info = triage.get("papers", {}).get(paper_key, {})

    # Tier
    tier = info.get("tier", "PROXY_PLUS_LLMMC")

    # Method from title
    title = paper_data.get("title", "")
    method = extract_method_from_title(title)

    # Fame from B-dimension
    b_val = info.get("B", 0.3)
    if b_val >= 0.6:
        fame = "high"
    elif b_val >= 0.35:
        fame = "medium"
    else:
        fame = "low"

    # Full text
    ft = paper_data.get("full_text", {})
    has_ft = isinstance(ft, dict) and ft.get("available", False)
    # Also check if file exists on disk
    if not has_ft:
        ft_path = os.path.join(PAPER_TEXTS_DIR, f"{paper_key}.md")
        has_ft = os.path.exists(ft_path)

    return {
        "tier": tier,
        "method": method,
        "fame": fame,
        "has_fulltext": has_ft,
        "B": b_val,
        "I": info.get("I", 0.4),
        "K": info.get("K", 0.0),
        "A_proxy": info.get("A_proxy", 0.2),
    }


def select_batch(batch_num, papers, triage, learning_log):
    """
    Select papers for a batch using stratified sampling.

    Batch 1: Maximize diversity (cover all strata)
    Batch 2: Focus on error-prone areas from Batch 1
    Batch 3: Fill gaps and test edge cases
    Batch 4: Scale test with optimized pipeline
    """
    if batch_num < 1 or batch_num > len(BATCH_SIZES):
        print(f"Error: batch_num must be 1-{len(BATCH_SIZES)}")
        return []

    batch_size = BATCH_SIZES[batch_num - 1]

    # Get already-processed papers
    processed = set()
    for iteration in learning_log.get("iterations", []):
        processed.update(iteration.get("papers", []))

    # Classify all unprocessed papers
    candidates = {}
    for key, data in papers.items():
        if key in processed:
            continue
        candidates[key] = classify_paper_for_stratification(key, data, triage)

    if not candidates:
        print("No unprocessed papers remaining.")
        return []

    selected = []

    if batch_num == 1:
        # Batch 1: Maximum diversity — stratified across tier × method × fame
        selected = _select_stratified(candidates, batch_size)
    elif batch_num == 2:
        # Batch 2: Focus on error-prone areas from Batch 1
        error_patterns = _get_error_patterns(learning_log)
        selected = _select_error_focused(candidates, batch_size, error_patterns)
    elif batch_num == 3:
        # Batch 3: Fill gaps — underrepresented strata + edge cases
        covered = _get_covered_strata(learning_log)
        selected = _select_gap_filling(candidates, batch_size, covered)
    else:
        # Batch 4: Random sample for scale test
        import random
        keys = list(candidates.keys())
        random.seed(42 + batch_num)
        selected = random.sample(keys, min(batch_size, len(keys)))

    return selected


def _select_stratified(candidates, n):
    """Select n papers with maximum diversity across strata."""
    # Build stratum buckets: tier × fame
    buckets = defaultdict(list)
    for key, info in candidates.items():
        stratum = f"{info['tier']}_{info['fame']}"
        buckets[stratum].append((key, info))

    selected = []
    # Round-robin across strata
    bucket_keys = sorted(buckets.keys())
    idx = 0
    while len(selected) < n and bucket_keys:
        bucket = bucket_keys[idx % len(bucket_keys)]
        if buckets[bucket]:
            # Pick paper closest to stratum center
            paper_key, _ = buckets[bucket].pop(0)
            selected.append(paper_key)
        else:
            bucket_keys.remove(bucket)
        idx += 1

    # If we need more, add papers with fulltext (high learning value)
    if len(selected) < n:
        remaining = [(k, v) for k, v in candidates.items() if k not in selected]
        ft_papers = [(k, v) for k, v in remaining if v["has_fulltext"]]
        for k, _ in ft_papers[:n - len(selected)]:
            selected.append(k)

    # Still need more? Add randomly
    if len(selected) < n:
        import random
        random.seed(42)
        remaining_keys = [k for k in candidates if k not in selected]
        random.shuffle(remaining_keys)
        selected.extend(remaining_keys[:n - len(selected)])

    return selected[:n]


def _get_error_patterns(learning_log):
    """Extract error patterns from previous iterations."""
    patterns = {
        "high_error_tiers": Counter(),
        "high_error_methods": Counter(),
        "high_error_fame": Counter(),
        "systematic_biases": [],
    }

    for iteration in learning_log.get("iterations", []):
        for error in iteration.get("errors", []):
            if error.get("tier"):
                patterns["high_error_tiers"][error["tier"]] += 1
            if error.get("method"):
                patterns["high_error_methods"][error["method"]] += 1
            if error.get("fame"):
                patterns["high_error_fame"][error["fame"]] += 1

        for bias in iteration.get("systematic_biases", []):
            patterns["systematic_biases"].append(bias)

    return patterns


def _select_error_focused(candidates, n, error_patterns):
    """Select papers that match error-prone patterns."""
    scored = []
    for key, info in candidates.items():
        score = 0
        # Boost papers matching error-prone strata
        score += error_patterns["high_error_tiers"].get(info["tier"], 0) * 3
        score += error_patterns["high_error_methods"].get(info["method"], 0) * 2
        score += error_patterns["high_error_fame"].get(info["fame"], 0) * 2
        # Boost fulltext papers (can verify extraction)
        if info["has_fulltext"]:
            score += 5
        scored.append((score, key))

    scored.sort(reverse=True)
    return [key for _, key in scored[:n]]


def _get_covered_strata(learning_log):
    """Get strata already covered by previous batches."""
    covered = Counter()
    for iteration in learning_log.get("iterations", []):
        for strat in iteration.get("strata_covered", []):
            covered[strat] += 1
    return covered


def _select_gap_filling(candidates, n, covered):
    """Select papers from underrepresented strata."""
    scored = []
    for key, info in candidates.items():
        stratum = f"{info['tier']}_{info['method']}_{info['fame']}"
        # Inverse coverage = priority
        score = 1.0 / (1 + covered.get(stratum, 0))
        # Boost edge cases (very high or very low A_proxy)
        if info["A_proxy"] > 0.33 or info["A_proxy"] < 0.17:
            score += 2
        scored.append((score, key))

    scored.sort(reverse=True)
    return [key for _, key in scored[:n]]


# ═══════════════════════════════════════════════════════════════════
# BATCH EVALUATION
# ═══════════════════════════════════════════════════════════════════

def evaluate_batch(batch_num, learning_log, papers, triage):
    """
    Evaluate a completed batch. Reads extraction results and computes metrics.

    Expected result format in learning-log.yaml:
    iterations:
      - batch: 1
        papers: [PAP-xxx, PAP-yyy, ...]
        results:
          PAP-xxx:
            E1_accuracy: 0.7  # Parameter extraction accuracy
            E2_accuracy: 0.8  # Context accuracy
            E3_accuracy: 0.9  # Theory mapping accuracy
            E4_accuracy: 0.5  # Complementarity accuracy
            E5_accuracy: 0.0  # Validity (expected low)
            E6_accuracy: 0.3  # Case integration accuracy
            time_seconds: 45  # Time for this paper
            tokens_used: 3200 # API tokens consumed
            error_type: null  # or "substitution", "hallucination", etc.
    """
    if batch_num > len(learning_log.get("iterations", [])):
        print(f"Batch {batch_num} not yet in learning log.")
        print(f"Current iterations: {len(learning_log.get('iterations', []))}")
        print()
        print("To add batch results, edit data/paper-calibration/learning-log.yaml")
        print("and add results for each paper in the batch.")
        return

    iteration = learning_log["iterations"][batch_num - 1]
    results = iteration.get("results", {})

    if not results:
        print(f"No results found for batch {batch_num}.")
        print("Add results to learning-log.yaml first.")
        return

    # Compute metrics
    metrics = {
        "batch": batch_num,
        "n_papers": len(results),
        "E_accuracy": {},
        "timing": {},
        "error_distribution": Counter(),
        "tier_accuracy": defaultdict(list),
    }

    e_scores = defaultdict(list)
    times = []
    tokens = []

    for paper_key, result in results.items():
        for e in ["E1", "E2", "E3", "E4", "E5", "E6"]:
            acc_key = f"{e}_accuracy"
            if acc_key in result and result[acc_key] is not None:
                e_scores[e].append(result[acc_key])

        if "time_seconds" in result:
            times.append(result["time_seconds"])
        if "tokens_used" in result:
            tokens.append(result["tokens_used"])
        if result.get("error_type"):
            metrics["error_distribution"][result["error_type"]] += 1

        # Group by tier
        paper_triage = triage.get("papers", {}).get(paper_key, {})
        tier = paper_triage.get("tier", "unknown")
        mean_acc = sum(result.get(f"{e}_accuracy", 0) or 0 for e in ["E1", "E2", "E3", "E4"]) / 4
        metrics["tier_accuracy"][tier].append(mean_acc)

    # Aggregate E-accuracy
    for e, scores in e_scores.items():
        if scores:
            metrics["E_accuracy"][e] = {
                "mean": round(sum(scores) / len(scores), 3),
                "min": round(min(scores), 3),
                "max": round(max(scores), 3),
                "n": len(scores),
            }

    # Timing
    if times:
        metrics["timing"] = {
            "mean_seconds": round(sum(times) / len(times), 1),
            "total_seconds": round(sum(times), 1),
            "min_seconds": round(min(times), 1),
            "max_seconds": round(max(times), 1),
        }

    if tokens:
        metrics["timing"]["mean_tokens"] = round(sum(tokens) / len(tokens))
        metrics["timing"]["total_tokens"] = sum(tokens)

    # Tier accuracy
    tier_summary = {}
    for tier, accs in metrics["tier_accuracy"].items():
        tier_summary[tier] = {
            "mean_accuracy": round(sum(accs) / len(accs), 3),
            "n": len(accs),
        }
    metrics["tier_accuracy"] = tier_summary

    # Print report
    _print_evaluation_report(metrics, batch_num)

    return metrics


def _print_evaluation_report(metrics, batch_num):
    """Print formatted evaluation report."""
    print(f"\n{'='*70}")
    print(f"  BATCH {batch_num} EVALUATION REPORT")
    print(f"  Papers: {metrics['n_papers']}")
    print(f"{'='*70}")

    # E1-E6 accuracy
    print(f"\n  E1-E6 Extraction Accuracy:")
    print(f"  {'Element':<8} {'Mean':>6} {'Min':>6} {'Max':>6} {'N':>4}")
    print(f"  {'-'*30}")
    for e in ["E1", "E2", "E3", "E4", "E5", "E6"]:
        if e in metrics["E_accuracy"]:
            d = metrics["E_accuracy"][e]
            bar = "█" * int(d["mean"] * 20) + "░" * (20 - int(d["mean"] * 20))
            print(f"  {e:<8} {d['mean']:>5.2f} {d['min']:>6.2f} {d['max']:>6.2f} {d['n']:>4}  {bar}")

    # Timing
    if metrics["timing"]:
        t = metrics["timing"]
        print(f"\n  Timing:")
        print(f"  Mean: {t.get('mean_seconds', 0):.1f}s/paper")
        print(f"  Total: {t.get('total_seconds', 0):.0f}s ({t.get('total_seconds', 0)/60:.1f}min)")
        if "mean_tokens" in t:
            print(f"  Tokens: {t['mean_tokens']}/paper (total: {t['total_tokens']:,})")
            cost_per_1k = 0.003  # Sonnet estimate
            print(f"  Est. cost: ${t['total_tokens'] * cost_per_1k / 1000:.2f}")

    # Tier accuracy
    if metrics["tier_accuracy"]:
        print(f"\n  Accuracy by Triage Tier:")
        for tier, d in sorted(metrics["tier_accuracy"].items()):
            print(f"  {tier:<25} {d['mean_accuracy']:.3f} (n={d['n']})")

    # Error distribution
    if metrics["error_distribution"]:
        print(f"\n  Error Types:")
        for error_type, count in metrics["error_distribution"].most_common():
            print(f"  {error_type:<25} {count}")

    print(f"\n{'='*70}")


# ═══════════════════════════════════════════════════════════════════
# MODEL UPDATE (Refit B-I-K regression)
# ═══════════════════════════════════════════════════════════════════

def update_model(learning_log, triage):
    """
    Refit B-I-K regression with expanded ground truth.

    After each batch, papers with E1-E6 results become new ground truth.
    This grows the regression N from 10 (initial) to 10 + sum(batch_sizes).
    """
    # Collect all ground truth points
    ground_truth = []

    # Original 10 calibration papers
    gt_files = Path(CALIBRATION_DIR).glob("GT-PAP-*.yaml")
    for gt_file in gt_files:
        try:
            with open(gt_file) as f:
                gt_data = yaml.safe_load(f)
            if gt_data and "scores" in gt_data:
                scores = gt_data["scores"]
                # Calculate actual accuracy as mean of S1-S6
                s_vals = []
                for s in ["S1", "S2", "S3", "S4", "S5", "S6"]:
                    if s in scores:
                        s_vals.append(scores[s].get("value", 0))
                if s_vals:
                    a_actual = sum(s_vals) / len(s_vals)
                    paper_key = gt_file.stem.replace("GT-", "")
                    ground_truth.append({
                        "paper": paper_key,
                        "A_actual": round(a_actual, 3),
                        "source": "calibration",
                    })
        except Exception:
            pass

    # Papers from learning iterations
    for iteration in learning_log.get("iterations", []):
        for paper_key, result in iteration.get("results", {}).items():
            # Convert E1-E6 accuracy to A_actual
            e_vals = []
            for e in ["E1", "E2", "E3", "E4", "E5", "E6"]:
                acc = result.get(f"{e}_accuracy")
                if acc is not None:
                    e_vals.append(acc)
            if e_vals:
                a_actual = sum(e_vals) / len(e_vals)
                ground_truth.append({
                    "paper": paper_key,
                    "A_actual": round(a_actual, 3),
                    "source": f"batch_{iteration.get('batch', '?')}",
                })

    # Get B, I, K for each ground truth paper
    triage_papers = triage.get("papers", {})
    regression_data = []
    for gt in ground_truth:
        paper_info = triage_papers.get(gt["paper"], {})
        if paper_info:
            regression_data.append({
                "paper": gt["paper"],
                "B": paper_info.get("B", 0.3),
                "I": paper_info.get("I", 0.4),
                "K": paper_info.get("K", 0.0),
                "A_actual": gt["A_actual"],
                "A_predicted": paper_info.get("A_proxy", 0.2),
                "source": gt["source"],
            })

    if len(regression_data) < 4:
        print(f"Too few data points ({len(regression_data)}) for regression update.")
        return

    # Simple OLS regression: A = a + b1*B + b2*I + b3*K
    # Using normal equations (no numpy dependency)
    n = len(regression_data)
    sum_B = sum(d["B"] for d in regression_data)
    sum_I = sum(d["I"] for d in regression_data)
    sum_K = sum(d["K"] for d in regression_data)
    sum_A = sum(d["A_actual"] for d in regression_data)
    sum_BB = sum(d["B"] ** 2 for d in regression_data)
    sum_II = sum(d["I"] ** 2 for d in regression_data)
    sum_KK = sum(d["K"] ** 2 for d in regression_data)
    sum_AB = sum(d["A_actual"] * d["B"] for d in regression_data)
    sum_AI = sum(d["A_actual"] * d["I"] for d in regression_data)
    sum_AK = sum(d["A_actual"] * d["K"] for d in regression_data)
    sum_BI = sum(d["B"] * d["I"] for d in regression_data)
    sum_BK = sum(d["B"] * d["K"] for d in regression_data)
    sum_IK = sum(d["I"] * d["K"] for d in regression_data)

    # Solve 4x4 system using Cramer's rule (simplified)
    # For now, use iterative gradient descent (simpler than matrix inversion)
    # Start with current coefficients
    a, b1, b2, b3 = 0.095, 0.197, 0.152, -0.182
    lr = 0.01
    for _ in range(10000):
        grad_a = grad_b1 = grad_b2 = grad_b3 = 0
        for d in regression_data:
            pred = a + b1 * d["B"] + b2 * d["I"] + b3 * d["K"]
            error = pred - d["A_actual"]
            grad_a += error
            grad_b1 += error * d["B"]
            grad_b2 += error * d["I"]
            grad_b3 += error * d["K"]
        a -= lr * grad_a / n
        b1 -= lr * grad_b1 / n
        b2 -= lr * grad_b2 / n
        b3 -= lr * grad_b3 / n

    # Compute R² and RMSE
    ss_res = 0
    ss_tot = 0
    mean_A = sum_A / n
    for d in regression_data:
        pred = a + b1 * d["B"] + b2 * d["I"] + b3 * d["K"]
        ss_res += (d["A_actual"] - pred) ** 2
        ss_tot += (d["A_actual"] - mean_A) ** 2

    r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    rmse = math.sqrt(ss_res / n)

    # Print results
    print(f"\n{'='*70}")
    print(f"  B-I-K REGRESSION UPDATE")
    print(f"  Ground truth: N={n} (10 calibration + {n-10} from batches)")
    print(f"{'='*70}")
    print(f"\n  OLD: A = 0.095 + 0.197·B + 0.152·I - 0.182·K  (N=10)")
    print(f"  NEW: A = {a:.3f} + {b1:.3f}·B + {b2:.3f}·I + {b3:.3f}·K  (N={n})")
    print(f"\n  R² = {r_squared:.3f}")
    print(f"  RMSE = {rmse:.4f}")
    print(f"\n  Data points:")
    print(f"  {'Paper':<35} {'B':>5} {'I':>5} {'K':>5} {'A_act':>6} {'A_pred':>7} {'Err':>6} {'Source'}")
    print(f"  {'-'*85}")
    for d in sorted(regression_data, key=lambda x: -x["A_actual"]):
        pred = a + b1 * d["B"] + b2 * d["I"] + b3 * d["K"]
        err = pred - d["A_actual"]
        print(f"  {d['paper']:<35} {d['B']:>5.2f} {d['I']:>5.2f} {d['K']:>5.2f} "
              f"{d['A_actual']:>6.3f} {pred:>7.3f} {err:>+6.3f} {d['source']}")

    # Save update to learning log
    update = {
        "n": n,
        "coefficients": {
            "intercept": round(a, 4),
            "B": round(b1, 4),
            "I": round(b2, 4),
            "K": round(b3, 4),
        },
        "r_squared": round(r_squared, 4),
        "rmse": round(rmse, 4),
    }

    return update


# ═══════════════════════════════════════════════════════════════════
# PROXY IMPROVEMENT APPLICATION
# ═══════════════════════════════════════════════════════════════════

def improve_proxies(papers, triage):
    """
    Apply newly discovered proxies to improve B, I, K scores.
    Shows delta from original scores.
    """
    triage_papers = triage.get("papers", {})

    improvements = {
        "B_improved": 0,
        "I_improved": 0,
        "K_improved": 0,
        "tier_changes": Counter(),
        "examples": [],
    }

    old_tiers = Counter()
    new_tiers = Counter()
    total = 0

    for paper_key, paper_data in papers.items():
        if paper_key not in triage_papers:
            continue

        old = triage_papers[paper_key]
        old_B = old.get("B", 0.3)
        old_I = old.get("I", 0.4)
        old_K = old.get("K", 0.0)
        old_A = old.get("A_proxy", 0.2)
        old_tier = old.get("tier", "PROXY_PLUS_LLMMC")

        # Apply improvements
        doi_info = extract_journal_from_doi(paper_data.get("doi"))
        method = extract_method_from_title(paper_data.get("title", ""))
        abstract_signals = count_abstract_method_signals(paper_data.get("abstract", ""))

        new_B = improved_B(paper_data, old_B, doi_info)
        new_I = improved_I(paper_data, old_I, method, abstract_signals)
        new_K = improved_K(paper_data, old_K)

        # Recompute A_proxy
        new_A = 0.095 + 0.197 * new_B + 0.152 * new_I - 0.182 * new_K

        # Determine new tier
        if new_A >= 0.45:
            new_tier = "PROXY_OK"
        elif new_A >= 0.30:
            new_tier = "PROXY_PLUS_WEB"
        elif new_A >= 0.20:
            new_tier = "PROXY_PLUS_LLMMC"
        else:
            new_tier = "FULLTEXT_NEEDED"

        old_tiers[old_tier] += 1
        new_tiers[new_tier] += 1
        total += 1

        if abs(new_B - old_B) > 0.01:
            improvements["B_improved"] += 1
        if abs(new_I - old_I) > 0.01:
            improvements["I_improved"] += 1
        if abs(new_K - old_K) > 0.01:
            improvements["K_improved"] += 1

        if old_tier != new_tier:
            improvements["tier_changes"][f"{old_tier} → {new_tier}"] += 1
            if len(improvements["examples"]) < 10:
                improvements["examples"].append({
                    "paper": paper_key,
                    "old_tier": old_tier,
                    "new_tier": new_tier,
                    "old_A": round(old_A, 3),
                    "new_A": round(new_A, 3),
                    "delta_B": round(new_B - old_B, 3),
                    "delta_I": round(new_I - old_I, 3),
                    "delta_K": round(new_K - old_K, 3),
                })

    # Print report
    print(f"\n{'='*70}")
    print(f"  PROXY IMPROVEMENT ANALYSIS")
    print(f"  Papers analyzed: {total}")
    print(f"{'='*70}")

    print(f"\n  Dimension Improvements:")
    print(f"  B improved: {improvements['B_improved']} papers ({improvements['B_improved']/total*100:.1f}%)")
    print(f"  I improved: {improvements['I_improved']} papers ({improvements['I_improved']/total*100:.1f}%)")
    print(f"  K improved: {improvements['K_improved']} papers ({improvements['K_improved']/total*100:.1f}%)")

    print(f"\n  Triage Distribution Change:")
    print(f"  {'Tier':<25} {'OLD':>6} {'NEW':>6} {'Δ':>6}")
    print(f"  {'-'*45}")
    for tier in ["PROXY_OK", "PROXY_PLUS_WEB", "PROXY_PLUS_LLMMC", "FULLTEXT_NEEDED"]:
        old_n = old_tiers.get(tier, 0)
        new_n = new_tiers.get(tier, 0)
        delta = new_n - old_n
        sign = "+" if delta > 0 else ""
        print(f"  {tier:<25} {old_n:>6} {new_n:>6} {sign}{delta:>5}")

    if improvements["tier_changes"]:
        print(f"\n  Tier Transitions:")
        for transition, count in improvements["tier_changes"].most_common():
            print(f"  {transition:<45} {count}")

    if improvements["examples"]:
        print(f"\n  Example Changes (first 10):")
        print(f"  {'Paper':<35} {'Old→New Tier':<40} {'ΔA':>6} {'ΔB':>6} {'ΔI':>6} {'ΔK':>6}")
        print(f"  {'-'*100}")
        for ex in improvements["examples"]:
            print(f"  {ex['paper']:<35} {ex['old_tier']+'→'+ex['new_tier']:<40} "
                  f"{ex['new_A']-ex['old_A']:>+5.3f} {ex['delta_B']:>+5.3f} "
                  f"{ex['delta_I']:>+5.3f} {ex['delta_K']:>+5.3f}")

    return improvements


# ═══════════════════════════════════════════════════════════════════
# HYPOTHESIS FRAMEWORK (Pre/Post Batch Comparison)
# ═══════════════════════════════════════════════════════════════════

# Hypothesis status symbols
H_SYMBOLS = {
    "pending": "⏳",
    "confirmed": "✅",
    "falsified": "❌",
    "inconclusive": "⚠️",
}

# Category colors/labels
H_CATEGORIES = {
    "accuracy": "ACCURACY",
    "bias": "BIAS VERIFICATION",
    "model": "MODEL STABILITY",
    "triage": "TRIAGE VALIDATION",
    "timing": "COST & TIMING",
    "proxy": "PROXY VALIDATION",
    "discovery": "DISCOVERY",
}


def show_hypotheses(batch_num, learning_log):
    """Display pre-batch hypotheses for a given batch."""
    iterations = learning_log.get("iterations", [])
    if batch_num > len(iterations):
        print(f"Batch {batch_num} not found in learning log.")
        return

    iteration = iterations[batch_num - 1]
    hypotheses = iteration.get("hypotheses", [])

    if not hypotheses:
        print(f"\n  No hypotheses defined for Batch {batch_num}.")
        print(f"  Add hypotheses to learning-log.yaml under iterations[{batch_num-1}].hypotheses")
        return

    print(f"\n{'='*80}")
    print(f"  PRE-BATCH HYPOTHESES: Batch {batch_num} ({len(hypotheses)} hypotheses)")
    print(f"  Formulated BEFORE extraction — to be compared with actual results")
    print(f"{'='*80}")

    # Group by category
    by_category = defaultdict(list)
    for h in hypotheses:
        by_category[h.get("category", "other")].append(h)

    # Summary counts
    counts = Counter(h.get("status", "pending") for h in hypotheses)
    print(f"\n  Status: {counts.get('pending', 0)} pending | "
          f"{counts.get('confirmed', 0)} confirmed | "
          f"{counts.get('falsified', 0)} falsified | "
          f"{counts.get('inconclusive', 0)} inconclusive")

    for cat_key in ["accuracy", "bias", "model", "triage", "timing", "proxy", "discovery"]:
        if cat_key not in by_category:
            continue
        cat_hyps = by_category[cat_key]
        cat_label = H_CATEGORIES.get(cat_key, cat_key.upper())

        print(f"\n  ── {cat_label} {'─'*(60 - len(cat_label))}")
        for h in cat_hyps:
            status_sym = H_SYMBOLS.get(h.get("status", "pending"), "?")
            hid = h.get("id", "?")
            pred = h.get("prediction", "?")
            conf = h.get("confidence", "?")

            print(f"\n  {status_sym} {hid}: {pred}")
            print(f"     Metric:    {h.get('metric', '?')}")

            # Show threshold based on direction
            direction = h.get("direction", "")
            if direction == "between":
                print(f"     Threshold: {h.get('threshold_low', '?')} <= value <= {h.get('threshold_high', '?')}")
            else:
                print(f"     Threshold: value {direction} {h.get('threshold', '?')}")

            print(f"     Confidence: {conf}")

            # Show actual value and verdict if available
            actual = h.get("actual_value")
            verdict = h.get("verdict")
            if actual is not None:
                print(f"     Actual:    {actual}")
            if verdict:
                print(f"     Verdict:   {verdict}")

    print(f"\n{'='*80}")


def evaluate_hypotheses(batch_num, learning_log, triage):
    """
    Evaluate hypotheses against batch results.

    Reads results from the batch, computes actual values for each
    hypothesis metric, and determines verdict (confirmed/falsified/inconclusive).
    """
    iterations = learning_log.get("iterations", [])
    if batch_num > len(iterations):
        print(f"Batch {batch_num} not found in learning log.")
        return None

    iteration = iterations[batch_num - 1]
    hypotheses = iteration.get("hypotheses", [])
    results = iteration.get("results", {})

    if not hypotheses:
        print(f"No hypotheses defined for Batch {batch_num}.")
        return None

    if not results:
        print(f"No results yet for Batch {batch_num}.")
        print(f"Add results to learning-log.yaml first, then run --verdict {batch_num}.")
        return None

    # Pre-compute aggregates needed for hypothesis evaluation
    triage_papers = triage.get("papers", {})

    # E-scores by tier
    tier_e_scores = defaultdict(lambda: defaultdict(list))
    # E-scores by fame
    fame_e_scores = defaultdict(lambda: defaultdict(list))
    # Overall E-scores
    all_e_scores = defaultdict(list)
    # Error counts
    error_counts = Counter()
    # Timing
    all_times = []
    all_tokens = []

    for paper_key, result in results.items():
        paper_triage = triage_papers.get(paper_key, {})
        tier = paper_triage.get("tier", "unknown")
        b_val = paper_triage.get("B", 0.3)
        fame = "high" if b_val >= 0.6 else ("medium" if b_val >= 0.35 else "low")

        for e in ["E1", "E2", "E3", "E4", "E5", "E6"]:
            acc = result.get(f"{e}_accuracy")
            if acc is not None:
                tier_e_scores[tier][e].append(acc)
                fame_e_scores[fame][e].append(acc)
                all_e_scores[e].append(acc)

        if result.get("error_type"):
            error_counts[result["error_type"]] += 1

        if "time_seconds" in result:
            all_times.append(result["time_seconds"])
        if "tokens_used" in result:
            all_tokens.append(result["tokens_used"])

    # Helper: mean of E1-E4 for a set of scores
    def mean_e14(e_dict):
        vals = []
        for e in ["E1", "E2", "E3", "E4"]:
            if e in e_dict and e_dict[e]:
                vals.extend(e_dict[e])
        return sum(vals) / len(vals) if vals else None

    def mean_list(lst):
        return sum(lst) / len(lst) if lst else None

    # Evaluate each hypothesis
    verdicts = []
    for h in hypotheses:
        hid = h.get("id", "?")
        direction = h.get("direction", "")
        actual = None
        verdict = None

        # Dispatch based on hypothesis ID pattern
        if hid.startswith("H1a"):  # PROXY_PLUS_WEB E1-E4 accuracy
            actual = mean_e14(tier_e_scores.get("PROXY_PLUS_WEB", {}))

        elif hid.startswith("H1b"):  # PROXY_PLUS_LLMMC E1-E4 accuracy
            actual = mean_e14(tier_e_scores.get("PROXY_PLUS_LLMMC", {}))

        elif hid.startswith("H1c"):  # FULLTEXT_NEEDED E1-E4 accuracy
            actual = mean_e14(tier_e_scores.get("FULLTEXT_NEEDED", {}))

        elif hid.startswith("H2a"):  # E1 overall accuracy
            actual = mean_list(all_e_scores.get("E1", []))

        elif hid.startswith("H2b"):  # E5 and E6 accuracy
            e5_mean = mean_list(all_e_scores.get("E5", []))
            e6_mean = mean_list(all_e_scores.get("E6", []))
            actual = max(e5_mean or 0, e6_mean or 0)  # Worst case (highest)

        elif hid.startswith("H2c"):  # E3 accuracy
            actual = mean_list(all_e_scores.get("E3", []))

        elif hid.startswith("H3a"):  # Fame ratio
            high_mean = mean_e14(fame_e_scores.get("high", {}))
            low_mean = mean_e14(fame_e_scores.get("low", {}))
            if high_mean is not None and low_mean is not None and low_mean > 0:
                actual = round(high_mean / low_mean, 2)

        elif hid.startswith("H3b"):  # Substitution count
            actual = error_counts.get("substitution", 0)

        elif hid.startswith("H3c"):  # E4 rank among E1-E4
            e_means = {}
            for e in ["E1", "E2", "E3", "E4"]:
                m = mean_list(all_e_scores.get(e, []))
                if m is not None:
                    e_means[e] = m
            if e_means:
                sorted_es = sorted(e_means.items(), key=lambda x: x[1])
                e4_rank = next((i+1 for i, (e, _) in enumerate(sorted_es) if e == "E4"), None)
                actual = e4_rank  # Rank 1 = lowest

        elif hid.startswith("H4a"):  # B-coefficient
            # Would need model refit — check model_updates
            updates = learning_log.get("model_updates", [])
            if updates:
                latest = updates[-1]
                actual = latest.get("coefficients", {}).get("B")

        elif hid.startswith("H4b"):  # K-coefficient
            updates = learning_log.get("model_updates", [])
            if updates:
                latest = updates[-1]
                actual = latest.get("coefficients", {}).get("K")

        elif hid.startswith("H4c"):  # R-squared
            updates = learning_log.get("model_updates", [])
            if updates:
                actual = updates[-1].get("r_squared")

        elif hid.startswith("H4d"):  # RMSE
            updates = learning_log.get("model_updates", [])
            if updates:
                actual = updates[-1].get("rmse")

        elif hid.startswith("H5"):  # Triage tier correctness
            # Check if tier ordering matches accuracy ordering
            correct = 0
            total = 0
            for paper_key, result in results.items():
                paper_triage = triage_papers.get(paper_key, {})
                tier = paper_triage.get("tier", "")
                e14 = sum(result.get(f"{e}_accuracy", 0) or 0 for e in ["E1", "E2", "E3", "E4"]) / 4
                # Tier predicts: WEB > LLMMC > FULLTEXT
                if tier == "PROXY_PLUS_WEB" and e14 >= 0.30:
                    correct += 1
                elif tier == "PROXY_PLUS_LLMMC" and 0.15 <= e14 < 0.40:
                    correct += 1
                elif tier == "FULLTEXT_NEEDED" and e14 < 0.25:
                    correct += 1
                total += 1
            if total > 0:
                actual = round(correct / total, 2)

        elif hid.startswith("H6a"):  # Mean time
            actual = round(mean_list(all_times), 1) if all_times else None

        elif hid.startswith("H6b"):  # Total cost
            if all_tokens:
                actual = round(sum(all_tokens) * 0.003 / 1000, 2)

        elif hid.startswith("H7a"):  # Title-keyword accuracy
            # This needs manual annotation — set to None if not available
            actual = None  # Requires manual check after extraction

        elif hid.startswith("H7b"):  # structural_characteristics complexity
            actual = None  # Requires manual check after extraction

        elif hid.startswith("H8a"):  # New biases count
            new_biases = iteration.get("systematic_biases", [])
            known_ids = {f"BIAS-0{i}" for i in range(1, 9)}
            new_count = sum(1 for b in new_biases if b.get("id", "") not in known_ids)
            actual = new_count

        elif hid.startswith("H8b"):  # Psi-dimension specificity
            actual = None  # Requires manual check after extraction

        # Determine verdict
        if actual is not None:
            actual = round(actual, 3) if isinstance(actual, float) else actual
            h["actual_value"] = actual

            if direction == ">=":
                threshold = h.get("threshold", 0)
                verdict = "confirmed" if actual >= threshold else "falsified"
            elif direction == "<=":
                threshold = h.get("threshold", 0)
                verdict = "confirmed" if actual <= threshold else "falsified"
            elif direction == "<":
                threshold = h.get("threshold", 0)
                verdict = "confirmed" if actual < threshold else "falsified"
            elif direction == ">":
                threshold = h.get("threshold", 0)
                verdict = "confirmed" if actual > threshold else "falsified"
            elif direction == "==":
                threshold = h.get("threshold", 0)
                # For rank comparisons: E4 rank 1 = lowest, which is what we predict
                verdict = "confirmed" if actual == 1 else "falsified"  # Rank 1 = lowest
            elif direction == "between":
                low = h.get("threshold_low", 0)
                high = h.get("threshold_high", 1)
                verdict = "confirmed" if low <= actual <= high else "falsified"
        else:
            verdict = "inconclusive"

        h["verdict"] = verdict
        h["status"] = verdict
        verdicts.append({"id": hid, "actual": actual, "verdict": verdict})

    # Print verdict report
    print(f"\n{'='*80}")
    print(f"  HYPOTHESIS VERDICT REPORT: Batch {batch_num}")
    print(f"{'='*80}")

    confirmed = sum(1 for v in verdicts if v["verdict"] == "confirmed")
    falsified = sum(1 for v in verdicts if v["verdict"] == "falsified")
    inconclusive = sum(1 for v in verdicts if v["verdict"] == "inconclusive")

    print(f"\n  SUMMARY: {confirmed} confirmed | {falsified} falsified | {inconclusive} inconclusive")
    print(f"  Confirmation rate: {confirmed}/{confirmed+falsified} = "
          f"{confirmed/(confirmed+falsified)*100:.0f}%" if (confirmed+falsified) > 0 else "")

    print(f"\n  {'ID':<12} {'Verdict':<14} {'Predicted':>12} {'Actual':>12} {'Category':<15}")
    print(f"  {'-'*70}")

    for h in hypotheses:
        hid = h.get("id", "?")
        status_sym = H_SYMBOLS.get(h.get("status", "pending"), "?")
        actual = h.get("actual_value", "—")
        cat = h.get("category", "?")

        # Format threshold as "predicted"
        direction = h.get("direction", "")
        if direction == "between":
            predicted = f"[{h.get('threshold_low', '?')}, {h.get('threshold_high', '?')}]"
        else:
            predicted = f"{direction} {h.get('threshold', '?')}"

        actual_str = f"{actual}" if actual is not None else "—"
        print(f"  {hid:<12} {status_sym} {h.get('status', '?'):<10} {predicted:>12} {actual_str:>12} {cat:<15}")

    # Highlight falsified hypotheses (most informative)
    falsified_hyps = [h for h in hypotheses if h.get("status") == "falsified"]
    if falsified_hyps:
        print(f"\n  {'─'*70}")
        print(f"  FALSIFIED HYPOTHESES (highest learning value):")
        for h in falsified_hyps:
            print(f"\n  ❌ {h.get('id', '?')}: {h.get('prediction', '?')}")
            print(f"     Expected: {h.get('direction', '')} {h.get('threshold', h.get('threshold_low', '?'))}")
            print(f"     Actual:   {h.get('actual_value', '—')}")
            print(f"     Implication: {h.get('falsification', '—')}")

    # Highlight surprises (inconclusive)
    inconclusive_hyps = [h for h in hypotheses if h.get("status") == "inconclusive"]
    if inconclusive_hyps:
        print(f"\n  {'─'*70}")
        print(f"  INCONCLUSIVE ({len(inconclusive_hyps)} — require manual evaluation):")
        for h in inconclusive_hyps:
            print(f"  ⚠️  {h.get('id', '?')}: {h.get('prediction', '?')}")

    print(f"\n{'='*80}")

    return verdicts


# ═══════════════════════════════════════════════════════════════════
# DASHBOARD & STATUS
# ═══════════════════════════════════════════════════════════════════

def show_plan():
    """Show the learning iteration plan."""
    print(f"\n{'='*70}")
    print(f"  ROUND 2: LEARNING ITERATION PLAN")
    print(f"{'='*70}")

    total_papers = sum(BATCH_SIZES)
    print(f"""
  Strategy: Process {total_papers} papers in {len(BATCH_SIZES)} iterations before bulk.
  Each iteration: Select → Extract → Measure → Learn → Improve

  ┌─────────────────────────────────────────────────────────────────┐
  │  Batch 1: {BATCH_SIZES[0]:>3} papers (STRATIFIED)                             │
  │  ├── Goal: Maximum diversity across tiers/methods/fame           │
  │  ├── Selection: Stratified sampling (tier × method × fame)       │
  │  ├── Metrics: E1-E6 accuracy, timing, error types               │
  │  └── Learning: Identify systematic biases, adjust prompts        │
  │                                                                   │
  │  Batch 2: {BATCH_SIZES[1]:>3} papers (ERROR-FOCUSED)                           │
  │  ├── Goal: Improve weakest areas from Batch 1                    │
  │  ├── Selection: Oversample error-prone strata                    │
  │  ├── Metrics: Compare with Batch 1 (improvement?)               │
  │  └── Learning: Refit B-I-K regression (N=10→60)                  │
  │                                                                   │
  │  Batch 3: {BATCH_SIZES[2]:>3} papers (GAP-FILLING)                             │
  │  ├── Goal: Cover underrepresented strata + edge cases            │
  │  ├── Selection: Inverse coverage weighting                       │
  │  ├── Metrics: K-dimension now meaningful (chicken-egg solved)    │
  │  └── Learning: Update thresholds, refit model (N=110)            │
  │                                                                   │
  │  Batch 4: {BATCH_SIZES[3]:>3} papers (SCALE TEST)                              │
  │  ├── Goal: Test optimized pipeline at scale                      │
  │  ├── Selection: Random sample                                    │
  │  ├── Metrics: Time/paper, cost/paper, accuracy stability         │
  │  └── Learning: Final model + cost estimate for bulk              │
  │                                                                   │
  │  BULK: ~{2593-total_papers} remaining papers                                │
  │  ├── Optimized prompt from 4 iterations                          │
  │  ├── Updated B-I-K model (N=210)                                 │
  │  ├── Tier-specific extraction strategy                           │
  │  └── Estimated: {(2593-total_papers)*3/3600:.1f}h at 10× parallel                      │
  └─────────────────────────────────────────────────────────────────┘

  Metriken pro Iteration:
  ├── E1-E6 Accuracy (per element, per tier, per method)
  ├── Time/Paper (seconds, tokens)
  ├── Error distribution (substitution, hallucination, omission, etc.)
  ├── Triage correctness (was tier prediction right?)
  ├── Prompt efficiency (tokens/accurate-extraction)
  └── B-I-K model fit (R², RMSE as N grows)

  Expected outcomes:
  ├── Batch 1→2: E1-E4 accuracy +10-15% from prompt improvements
  ├── Batch 2→3: K-dimension becomes meaningful (from 0→varied)
  ├── Batch 3→4: Triage thresholds optimized (RMSE: 0.103→~0.07)
  └── Bulk: Stable pipeline with known accuracy per tier
""")


def show_status(learning_log, papers, triage):
    """Show current learning progress."""
    iterations = learning_log.get("iterations", [])
    n_completed = len(iterations)
    n_papers_done = sum(len(it.get("papers", [])) for it in iterations)

    print(f"\n{'='*70}")
    print(f"  LEARNING LOOP STATUS")
    print(f"{'='*70}")
    print(f"\n  Iterations completed: {n_completed}/{len(BATCH_SIZES)}")
    print(f"  Papers processed:     {n_papers_done}/{sum(BATCH_SIZES)}")
    print(f"  Papers remaining:     {sum(BATCH_SIZES) - n_papers_done}")

    if n_completed == 0:
        print(f"\n  Next step: Select batch 1 papers")
        print(f"    python scripts/round2_learning_loop.py --select-batch 1")
        return

    # Show per-iteration summary
    print(f"\n  {'Batch':<8} {'N':>4} {'E1-E4 Acc':>10} {'Time/Paper':>12} {'Errors':>8}")
    print(f"  {'-'*46}")
    for it in iterations:
        results = it.get("results", {})
        if results:
            # Mean E1-E4 accuracy
            accs = []
            times = []
            errors = 0
            for r in results.values():
                e_vals = [r.get(f"{e}_accuracy", 0) or 0 for e in ["E1", "E2", "E3", "E4"]]
                accs.append(sum(e_vals) / 4)
                if "time_seconds" in r:
                    times.append(r["time_seconds"])
                if r.get("error_type"):
                    errors += 1

            mean_acc = sum(accs) / len(accs) if accs else 0
            mean_time = sum(times) / len(times) if times else 0
            print(f"  {it.get('batch', '?'):<8} {len(results):>4} {mean_acc:>9.3f} "
                  f"{mean_time:>10.1f}s {errors:>8}")
        else:
            print(f"  {it.get('batch', '?'):<8} {len(it.get('papers', [])):>4} {'(pending)':>10}")

    # Current model
    model_updates = learning_log.get("model_updates", [])
    if model_updates:
        latest = model_updates[-1]
        c = latest.get("coefficients", {})
        print(f"\n  Current Model (N={latest.get('n', 10)}):")
        print(f"  A = {c.get('intercept', 0.095):.3f} + {c.get('B', 0.197):.3f}·B "
              f"+ {c.get('I', 0.152):.3f}·I + {c.get('K', -0.182):.3f}·K")
        print(f"  R² = {latest.get('r_squared', 0.774):.3f}, RMSE = {latest.get('rmse', 0.103):.4f}")

    # Next step
    if n_completed < len(BATCH_SIZES):
        next_batch = n_completed + 1
        has_results = (n_completed > 0 and
                       bool(iterations[-1].get("results")))
        if has_results or n_completed == 0:
            print(f"\n  Next step: Select batch {next_batch} papers")
            print(f"    python scripts/round2_learning_loop.py --select-batch {next_batch}")
        else:
            print(f"\n  Next step: Add results for batch {n_completed}")
            print(f"    Edit data/paper-calibration/learning-log.yaml")
            print(f"    Then: python scripts/round2_learning_loop.py --evaluate-batch {n_completed}")


def show_dashboard(learning_log, papers, triage):
    """Full dashboard combining plan, status, and improvements."""
    show_status(learning_log, papers, triage)
    print()
    show_plan()


# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="Round 2 Learning Loop")
    parser.add_argument("--plan", action="store_true", help="Show iteration plan")
    parser.add_argument("--select-batch", type=int, metavar="N",
                        help="Select papers for batch N (1-4)")
    parser.add_argument("--evaluate-batch", type=int, metavar="N",
                        help="Evaluate completed batch N")
    parser.add_argument("--update-model", action="store_true",
                        help="Refit B-I-K regression with new data")
    parser.add_argument("--status", action="store_true",
                        help="Show learning progress")
    parser.add_argument("--dashboard", action="store_true",
                        help="Full dashboard")
    parser.add_argument("--improve-proxies", action="store_true",
                        help="Apply newly discovered proxies")
    parser.add_argument("--hypotheses", type=int, metavar="N",
                        help="Show pre-batch hypotheses for batch N")
    parser.add_argument("--verdict", type=int, metavar="N",
                        help="Evaluate hypotheses against batch N results")
    parser.add_argument("--save", action="store_true",
                        help="Save results to learning-log.yaml")

    args = parser.parse_args()

    if not any([args.plan, args.select_batch, args.evaluate_batch,
                args.update_model, args.status, args.dashboard,
                args.improve_proxies, args.hypotheses, args.verdict]):
        args.dashboard = True

    # Load data
    papers = load_paper_yamls()
    triage = load_triage_results()
    learning_log = load_learning_log()

    if args.plan:
        show_plan()

    elif args.select_batch is not None:
        selected = select_batch(args.select_batch, papers, triage, learning_log)
        if selected:
            print(f"\n{'='*70}")
            print(f"  BATCH {args.select_batch} SELECTION ({len(selected)} papers)")
            print(f"{'='*70}")

            # Show selected papers with their strata
            print(f"\n  {'#':<4} {'Paper':<40} {'Tier':<20} {'B':>5} {'I':>5} {'K':>5} {'Method':<12} {'FT'}")
            print(f"  {'-'*100}")
            for i, key in enumerate(selected, 1):
                info = classify_paper_for_stratification(key, papers.get(key, {}), triage)
                ft_mark = "✓" if info["has_fulltext"] else ""
                print(f"  {i:<4} {key:<40} {info['tier']:<20} {info['B']:>5.2f} "
                      f"{info['I']:>5.2f} {info['K']:>5.2f} {info['method']:<12} {ft_mark}")

            # Strata coverage
            strata_counts = Counter()
            for key in selected:
                info = classify_paper_for_stratification(key, papers.get(key, {}), triage)
                strata_counts[f"{info['tier']}_{info['fame']}"] += 1

            print(f"\n  Strata Coverage:")
            for stratum, count in sorted(strata_counts.items()):
                bar = "█" * count
                print(f"  {stratum:<35} {count:>3} {bar}")

            # Save selection to learning log
            if args.save:
                iteration = {
                    "batch": args.select_batch,
                    "batch_size": len(selected),
                    "papers": selected,
                    "selected_at": time.strftime("%Y-%m-%d %H:%M"),
                    "strata_covered": list(strata_counts.keys()),
                    "results": {},  # To be filled after extraction
                    "errors": [],
                    "systematic_biases": [],
                    "learnings": [],
                }
                # Ensure we have enough iterations in the list
                while len(learning_log["iterations"]) < args.select_batch:
                    learning_log["iterations"].append({})
                learning_log["iterations"][args.select_batch - 1] = iteration
                save_learning_log(learning_log)
                print(f"\n  ✓ Saved to {LEARNING_LOG_PATH}")
                print(f"  Next: Extract E1-E6 for these papers, then run --evaluate-batch {args.select_batch}")

    elif args.evaluate_batch is not None:
        evaluate_batch(args.evaluate_batch, learning_log, papers, triage)

    elif args.update_model:
        update = update_model(learning_log, triage)
        if update and args.save:
            learning_log.setdefault("model_updates", []).append(update)
            save_learning_log(learning_log)
            print(f"\n  ✓ Model update saved to {LEARNING_LOG_PATH}")

    elif args.improve_proxies:
        improve_proxies(papers, triage)

    elif args.hypotheses is not None:
        show_hypotheses(args.hypotheses, learning_log)

    elif args.verdict is not None:
        verdicts = evaluate_hypotheses(args.verdict, learning_log, triage)
        if verdicts and args.save:
            save_learning_log(learning_log)
            print(f"\n  ✓ Verdict results saved to {LEARNING_LOG_PATH}")

    elif args.status:
        show_status(learning_log, papers, triage)

    elif args.dashboard:
        show_dashboard(learning_log, papers, triage)


if __name__ == "__main__":
    main()
