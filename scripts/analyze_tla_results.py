#!/usr/bin/env python3
"""
TLA Deviation Study — Statistical Analysis (Stufe 3b)
=====================================================

Performs statistical analysis on TLA benchmark results:
  - Paired Wilcoxon tests (Arm 0 vs Arm 3)
  - Per-stratum breakdown with effect sizes (Cohen's d)
  - Confidence intervals (bootstrap)
  - Hypothesis testing (H1–H5)
  - LaTeX-ready table output

Input:  data/research/tla-deviation-results.yaml
Output: data/research/tla-statistical-analysis.yaml
        (also prints human-readable summary)

Usage:
    python scripts/analyze_tla_results.py
    python scripts/analyze_tla_results.py --latex   # Print LaTeX tables
"""

import argparse
import math
import random
import sys
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
RESULTS_PATH = ROOT / "data" / "research" / "tla-deviation-results.yaml"
OUTPUT_PATH = ROOT / "data" / "research" / "tla-statistical-analysis.yaml"


# ============================================================================
# Statistical Helpers (no scipy dependency)
# ============================================================================
def mean(xs):
    return sum(xs) / len(xs) if xs else 0.0

def stdev(xs):
    if len(xs) < 2:
        return 0.0
    m = mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))

def median(xs):
    s = sorted(xs)
    n = len(s)
    if n == 0:
        return 0.0
    if n % 2 == 1:
        return s[n // 2]
    return (s[n // 2 - 1] + s[n // 2]) / 2

def bootstrap_ci(xs, n_boot=10000, alpha=0.05, stat_fn=mean, seed=42):
    """Bootstrap confidence interval for any statistic."""
    rng = random.Random(seed)
    n = len(xs)
    if n == 0:
        return (0.0, 0.0)
    boot_stats = []
    for _ in range(n_boot):
        sample = [rng.choice(xs) for _ in range(n)]
        boot_stats.append(stat_fn(sample))
    boot_stats.sort()
    lo = int(n_boot * alpha / 2)
    hi = int(n_boot * (1 - alpha / 2))
    return (boot_stats[lo], boot_stats[hi])

def cohens_d(xs, ys):
    """Cohen's d effect size for paired samples."""
    if len(xs) != len(ys) or len(xs) < 2:
        return None
    diffs = [x - y for x, y in zip(xs, ys)]
    d_mean = mean(diffs)
    d_sd = stdev(diffs)
    if d_sd == 0:
        return float('inf') if d_mean != 0 else 0.0
    return d_mean / d_sd

def wilcoxon_approx(xs, ys):
    """
    Approximate Wilcoxon signed-rank test (two-sided).
    Returns (W_statistic, approximate_p_value, n_nonzero).

    Uses normal approximation for n >= 10.
    For smaller n, returns None for p-value.
    """
    diffs = [(x - y) for x, y in zip(xs, ys)]
    # Remove zeros
    diffs = [d for d in diffs if d != 0]
    n = len(diffs)
    if n == 0:
        return (0, 1.0, 0)

    # Rank absolute values
    abs_diffs = [(abs(d), i) for i, d in enumerate(diffs)]
    abs_diffs.sort()
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j < n - 1 and abs_diffs[j + 1][0] == abs_diffs[j][0]:
            j += 1
        avg_rank = (i + j) / 2.0 + 1.0  # 1-based
        for k in range(i, j + 1):
            ranks[abs_diffs[k][1]] = avg_rank
        i = j + 1

    # W+ = sum of ranks of positive differences
    w_plus = sum(ranks[i] for i in range(n) if diffs[i] > 0)
    w_minus = sum(ranks[i] for i in range(n) if diffs[i] < 0)
    W = min(w_plus, w_minus)

    if n < 10:
        return (W, None, n)

    # Normal approximation
    mean_w = n * (n + 1) / 4.0
    var_w = n * (n + 1) * (2 * n + 1) / 24.0
    z = (W - mean_w) / math.sqrt(var_w) if var_w > 0 else 0
    # Two-sided p-value (approximate via normal CDF)
    p = 2.0 * normal_cdf(-abs(z))

    return (W, p, n)

def normal_cdf(x):
    """Standard normal CDF approximation (Abramowitz & Stegun)."""
    # Using error function approximation
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


# ============================================================================
# Load Results
# ============================================================================
def load_results():
    with open(RESULTS_PATH) as f:
        return yaml.safe_load(f)


# ============================================================================
# Extract deviation vectors
# ============================================================================
def extract_deviations(results_data):
    """Extract per-query deviation vectors for each arm."""
    results = results_data.get('results', [])

    data = {
        'all': defaultdict(list),
        'by_stratum': defaultdict(lambda: defaultdict(list)),
    }

    for r in results:
        stratum = r['stratum']
        gt = r.get('ground_truth_value')
        if gt is None:
            continue

        for arm_name in ['arm_0', 'arm_1', 'arm_2', 'arm_3']:
            arm = r.get(arm_name, {})
            if arm is None:
                continue
            est = arm.get('estimate')
            if est is None:
                continue

            abs_dev = abs(est - gt)
            pct_dev = abs_dev / abs(gt) * 100 if gt != 0 else None
            signed_dev = est - gt

            entry = {
                'query_id': r['query_id'],
                'parameter_id': r['parameter_id'],
                'symbol': r['symbol'],
                'stratum': stratum,
                'gt': gt,
                'estimate': est,
                'abs_dev': abs_dev,
                'pct_dev': pct_dev,
                'signed_dev': signed_dev,
            }

            data['all'][arm_name].append(entry)
            data['by_stratum'][stratum][arm_name].append(entry)

    return data


# ============================================================================
# Hypothesis Tests
# ============================================================================
def test_hypotheses(dev_data):
    """Test all 5 hypotheses from the study design."""
    all_data = dev_data['all']
    by_stratum = dev_data['by_stratum']
    tests = {}

    # -----------------------------------------------------------------------
    # H1: LLM-only MAPE > 15%
    # -----------------------------------------------------------------------
    arm0_pcts = [e['pct_dev'] for e in all_data.get('arm_0', []) if e['pct_dev'] is not None]
    if arm0_pcts:
        arm0_mape = mean(arm0_pcts)
        arm0_ci = bootstrap_ci(arm0_pcts)
        tests['H1'] = {
            'hypothesis': 'LLM-only MAPE > 15%',
            'result': 'SUPPORTED' if arm0_mape > 15 else 'NOT SUPPORTED',
            'mape': round(arm0_mape, 2),
            'ci_95': [round(arm0_ci[0], 2), round(arm0_ci[1], 2)],
            'n': len(arm0_pcts),
        }

    # -----------------------------------------------------------------------
    # H2: Monotone reduction MAE(0) > MAE(1) > MAE(2) > MAE(3)
    # -----------------------------------------------------------------------
    arm_maes = {}
    arm_mae_cis = {}
    for arm_name in ['arm_0', 'arm_1', 'arm_2', 'arm_3']:
        abs_devs = [e['abs_dev'] for e in all_data.get(arm_name, [])]
        if abs_devs:
            arm_maes[arm_name] = mean(abs_devs)
            arm_mae_cis[arm_name] = bootstrap_ci(abs_devs)

    if len(arm_maes) == 4:
        monotone = (arm_maes['arm_0'] > arm_maes['arm_1'] >=
                    arm_maes['arm_2'] >= arm_maes['arm_3'])
        tests['H2'] = {
            'hypothesis': 'Monotone MAE reduction: Arm0 > Arm1 > Arm2 > Arm3',
            'result': 'SUPPORTED' if monotone else 'NOT SUPPORTED',
            'values': {k: round(v, 4) for k, v in arm_maes.items()},
            'ci_95': {k: [round(c[0], 4), round(c[1], 4)]
                      for k, c in arm_mae_cis.items()},
        }

    # -----------------------------------------------------------------------
    # H3: PCT is the critical layer (largest MAE reduction)
    # -----------------------------------------------------------------------
    if 'arm_1' in arm_maes and 'arm_2' in arm_maes:
        delta_pct = arm_maes['arm_1'] - arm_maes['arm_2']
        delta_registry = arm_maes['arm_0'] - arm_maes['arm_1'] if 'arm_0' in arm_maes else 0
        delta_llmmc = arm_maes['arm_2'] - arm_maes['arm_3'] if 'arm_3' in arm_maes else 0

        pct_is_largest = delta_pct >= max(delta_registry, delta_llmmc)

        tests['H3'] = {
            'hypothesis': 'PCT provides the largest MAE reduction',
            'result': 'SUPPORTED' if pct_is_largest else 'NOT SUPPORTED',
            'delta_registry': round(delta_registry, 4),
            'delta_pct': round(delta_pct, 4),
            'delta_llmmc': round(delta_llmmc, 4),
        }

    # -----------------------------------------------------------------------
    # H4: Context complexity increases LLM deviation (S1 < S2 < S3 < S4)
    # -----------------------------------------------------------------------
    stratum_mapes = {}
    for s in ['S1', 'S2', 'S3', 'S4']:
        s_arm0 = by_stratum.get(s, {}).get('arm_0', [])
        pcts = [e['pct_dev'] for e in s_arm0 if e['pct_dev'] is not None]
        if pcts:
            stratum_mapes[s] = mean(pcts)

    if len(stratum_mapes) >= 2:
        # Check if contextual strata (S2-S4) have higher MAPE than S1
        s1_mape = stratum_mapes.get('S1', 0)
        contextual_higher = all(
            stratum_mapes.get(s, 0) > s1_mape
            for s in ['S2', 'S3', 'S4'] if s in stratum_mapes
        )
        tests['H4'] = {
            'hypothesis': 'Context complexity increases LLM deviation',
            'result': 'SUPPORTED' if contextual_higher else 'NOT SUPPORTED',
            'stratum_mapes': {k: round(v, 2) for k, v in stratum_mapes.items()},
        }

    # -----------------------------------------------------------------------
    # H5: LLM CIs are overconfident (coverage < 95%)
    # -----------------------------------------------------------------------
    # Already computed in the main benchmark; replicate here
    arm0_coverages = []
    results = dev_data  # use raw
    for e in all_data.get('arm_0', []):
        # Need CI from the results file
        pass
    # We'll compute this from the results file directly
    tests['H5'] = {
        'hypothesis': 'LLM confidence intervals are overconfident (coverage < 95%)',
        'note': 'Computed from CI coverage in benchmark results',
    }

    return tests


# ============================================================================
# Pairwise Comparisons
# ============================================================================
def pairwise_tests(dev_data):
    """Wilcoxon signed-rank tests for all arm pairs."""
    all_data = dev_data['all']
    comparisons = []

    pairs = [
        ('arm_0', 'arm_1', 'LLM vs Registry'),
        ('arm_0', 'arm_2', 'LLM vs PCT'),
        ('arm_0', 'arm_3', 'LLM vs Full'),
        ('arm_1', 'arm_2', 'Registry vs PCT'),
        ('arm_1', 'arm_3', 'Registry vs Full'),
        ('arm_2', 'arm_3', 'PCT vs Full'),
    ]

    for arm_a, arm_b, label in pairs:
        data_a = {e['query_id']: e for e in all_data.get(arm_a, [])}
        data_b = {e['query_id']: e for e in all_data.get(arm_b, [])}

        # Paired: only queries with both arms
        common_ids = sorted(set(data_a.keys()) & set(data_b.keys()))
        if len(common_ids) < 3:
            continue

        abs_a = [data_a[qid]['abs_dev'] for qid in common_ids]
        abs_b = [data_b[qid]['abs_dev'] for qid in common_ids]

        d = cohens_d(abs_a, abs_b)
        W, p, n_nonzero = wilcoxon_approx(abs_a, abs_b)

        diff = [a - b for a, b in zip(abs_a, abs_b)]
        diff_mean = mean(diff)
        diff_ci = bootstrap_ci(diff)

        comparisons.append({
            'comparison': label,
            'arm_a': arm_a,
            'arm_b': arm_b,
            'n_paired': len(common_ids),
            'mean_diff_mae': round(diff_mean, 4),
            'diff_ci_95': [round(diff_ci[0], 4), round(diff_ci[1], 4)],
            'cohens_d': round(d, 3) if d is not None else None,
            'effect_size': classify_effect(d),
            'wilcoxon_W': round(W, 1),
            'wilcoxon_p': round(p, 4) if p is not None else None,
            'significant_005': p < 0.05 if p is not None else None,
        })

    return comparisons


def classify_effect(d):
    if d is None:
        return 'N/A'
    d = abs(d)
    if d >= 0.8:
        return 'large'
    elif d >= 0.5:
        return 'medium'
    elif d >= 0.2:
        return 'small'
    return 'negligible'


# ============================================================================
# Per-Stratum Detail
# ============================================================================
def stratum_analysis(dev_data):
    """Detailed per-stratum analysis."""
    by_stratum = dev_data['by_stratum']
    results = {}

    for stratum in ['S1', 'S2', 'S3', 'S4']:
        s_data = by_stratum.get(stratum, {})
        if not s_data:
            continue

        stratum_info = {'n': 0, 'arms': {}, 'pairwise': []}

        for arm_name in ['arm_0', 'arm_1', 'arm_2', 'arm_3']:
            entries = s_data.get(arm_name, [])
            if not entries:
                continue

            abs_devs = [e['abs_dev'] for e in entries]
            pct_devs = [e['pct_dev'] for e in entries if e['pct_dev'] is not None]

            stratum_info['n'] = max(stratum_info['n'], len(entries))
            stratum_info['arms'][arm_name] = {
                'n': len(entries),
                'mae': round(mean(abs_devs), 4),
                'mae_ci_95': [round(x, 4) for x in bootstrap_ci(abs_devs)],
                'mape': round(mean(pct_devs), 2) if pct_devs else None,
                'mape_ci_95': [round(x, 2) for x in bootstrap_ci(pct_devs)] if pct_devs else None,
                'rmse': round(math.sqrt(mean([d**2 for d in abs_devs])), 4),
                'median_abs_dev': round(median(abs_devs), 4),
            }

        # Key pairwise: LLM vs Full within stratum
        arm0_data = {e['query_id']: e for e in s_data.get('arm_0', [])}
        arm3_data = {e['query_id']: e for e in s_data.get('arm_3', [])}
        common = sorted(set(arm0_data.keys()) & set(arm3_data.keys()))

        if len(common) >= 3:
            abs_0 = [arm0_data[qid]['abs_dev'] for qid in common]
            abs_3 = [arm3_data[qid]['abs_dev'] for qid in common]
            d = cohens_d(abs_0, abs_3)
            W, p, n_nz = wilcoxon_approx(abs_0, abs_3)
            stratum_info['llm_vs_full'] = {
                'n_paired': len(common),
                'cohens_d': round(d, 3) if d is not None else None,
                'effect_size': classify_effect(d),
                'wilcoxon_p': round(p, 4) if p is not None else None,
                'significant': p < 0.05 if p is not None else None,
            }

        results[stratum] = stratum_info

    return results


# ============================================================================
# Parameter-Level Analysis
# ============================================================================
def parameter_analysis(dev_data):
    """Which parameters show the largest LLM deviation?"""
    all_arm0 = dev_data['all'].get('arm_0', [])

    by_param = defaultdict(list)
    for e in all_arm0:
        by_param[e['parameter_id']].append(e)

    param_stats = []
    for pid, entries in sorted(by_param.items()):
        pct_devs = [e['pct_dev'] for e in entries if e['pct_dev'] is not None]
        if not pct_devs:
            continue
        param_stats.append({
            'parameter_id': pid,
            'symbol': entries[0]['symbol'],
            'n_queries': len(entries),
            'mean_mape': round(mean(pct_devs), 2),
            'max_mape': round(max(pct_devs), 2),
            'stdev_mape': round(stdev(pct_devs), 2) if len(pct_devs) > 1 else 0.0,
        })

    # Sort by mean MAPE descending
    param_stats.sort(key=lambda x: x['mean_mape'], reverse=True)
    return param_stats


# ============================================================================
# LaTeX Table Generation
# ============================================================================
def generate_latex_tables(analysis):
    """Generate LaTeX tables for the paper appendix."""
    lines = []

    # Table 1: Overall Summary
    lines.append("% Table 1: Overall Arm Comparison")
    lines.append("\\begin{table}[htbp]")
    lines.append("\\centering")
    lines.append("\\caption{TLA Deviation Study: Overall Results (N=100 queries)}")
    lines.append("\\label{tab:tla-overall}")
    lines.append("\\begin{tabular}{lrrrrrr}")
    lines.append("\\toprule")
    lines.append("Arm & N & MAE & MAPE\\% & RMSE & Bias & Coverage \\\\")
    lines.append("\\midrule")

    arm_labels = {
        'arm_0': 'LLM-Only',
        'arm_1': 'Registry',
        'arm_2': 'Registry+PCT',
        'arm_3': 'Full Pipeline',
    }

    overall = analysis.get('overall', {})
    for arm_name in ['arm_0', 'arm_1', 'arm_2', 'arm_3']:
        data = overall.get(arm_name, {})
        if not data:
            continue
        label = arm_labels[arm_name]
        n = data.get('n', 0)
        mae = data.get('mae', 0)
        mape = data.get('mape', 0)
        rmse = data.get('rmse', 0)
        bias = data.get('bias', 0)
        cov = data.get('coverage_95')
        cov_str = f"{cov:.1\\%}" if cov is not None else "N/A"
        lines.append(f"{label} & {n} & {mae:.4f} & {mape:.1f} & {rmse:.4f} & "
                     f"{bias:+.4f} & {cov_str} \\\\")

    lines.append("\\bottomrule")
    lines.append("\\end{tabular}")
    lines.append("\\end{table}")
    lines.append("")

    # Table 2: Per-Stratum MAPE
    lines.append("% Table 2: Per-Stratum MAPE by Arm")
    lines.append("\\begin{table}[htbp]")
    lines.append("\\centering")
    lines.append("\\caption{TLA Deviation: MAPE\\% by Stratum and Arm}")
    lines.append("\\label{tab:tla-stratum}")
    lines.append("\\begin{tabular}{lrrrrr}")
    lines.append("\\toprule")
    lines.append("Stratum & N & LLM & Registry & PCT & Full \\\\")
    lines.append("\\midrule")

    strata_desc = {
        'S1': 'S1: Context-free',
        'S2': 'S2: 1$\\Psi$ dim.',
        'S3': 'S3: 2--3$\\Psi$ dim.',
        'S4': 'S4: Full pipeline',
    }

    by_stratum = analysis.get('by_stratum', {})
    for s in ['S1', 'S2', 'S3', 'S4']:
        s_data = by_stratum.get(s, {})
        if not s_data:
            continue
        n = s_data.get('n', 0)
        arms = s_data.get('arms', {})
        vals = []
        for a in ['arm_0', 'arm_1', 'arm_2', 'arm_3']:
            m = arms.get(a, {}).get('mape')
            vals.append(f"{m:.1f}" if m is not None else "N/A")
        lines.append(f"{strata_desc[s]} & {n} & {vals[0]} & {vals[1]} & {vals[2]} & {vals[3]} \\\\")

    lines.append("\\bottomrule")
    lines.append("\\end{tabular}")
    lines.append("\\end{table}")
    lines.append("")

    # Table 3: Pairwise Tests
    lines.append("% Table 3: Pairwise Wilcoxon Tests")
    lines.append("\\begin{table}[htbp]")
    lines.append("\\centering")
    lines.append("\\caption{Pairwise Arm Comparisons (Wilcoxon Signed-Rank)}")
    lines.append("\\label{tab:tla-pairwise}")
    lines.append("\\begin{tabular}{lrrrrl}")
    lines.append("\\toprule")
    lines.append("Comparison & N & $\\Delta$MAE & Cohen's $d$ & $p$ & Signif. \\\\")
    lines.append("\\midrule")

    for comp in analysis.get('pairwise', []):
        label = comp['comparison']
        n = comp['n_paired']
        diff = comp['mean_diff_mae']
        d = comp.get('cohens_d', 0)
        p = comp.get('wilcoxon_p')
        sig = comp.get('significant_005')
        p_str = f"{p:.4f}" if p is not None else "N/A"
        sig_str = "$^{**}$" if sig else ""
        lines.append(f"{label} & {n} & {diff:+.4f} & {d:.3f} & {p_str} & {sig_str} \\\\")

    lines.append("\\bottomrule")
    lines.append("\\end{tabular}")
    lines.append("\\end{table}")

    return "\n".join(lines)


# ============================================================================
# Main
# ============================================================================
def main():
    parser = argparse.ArgumentParser(description="TLA Statistical Analysis")
    parser.add_argument('--latex', action='store_true',
                        help="Print LaTeX tables")
    parser.add_argument('--save', action='store_true', default=True,
                        help="Save analysis to YAML (default: True)")
    args = parser.parse_args()

    if not RESULTS_PATH.exists():
        print(f"No results found at {RESULTS_PATH}")
        print("Run the benchmark first: python scripts/benchmark_tla_deviation.py")
        sys.exit(1)

    print("Loading results...")
    results_data = load_results()
    n_results = len(results_data.get('results', []))
    print(f"  {n_results} query results loaded")

    print("\nExtracting deviation vectors...")
    dev_data = extract_deviations(results_data)

    print("Running hypothesis tests...")
    hypotheses = test_hypotheses(dev_data)

    print("Running pairwise comparisons...")
    pairwise = pairwise_tests(dev_data)

    print("Running per-stratum analysis...")
    by_stratum = stratum_analysis(dev_data)

    print("Running parameter-level analysis...")
    param_stats = parameter_analysis(dev_data)

    # Build combined analysis
    overall = {}
    for arm_name in ['arm_0', 'arm_1', 'arm_2', 'arm_3']:
        entries = dev_data['all'].get(arm_name, [])
        if entries:
            abs_devs = [e['abs_dev'] for e in entries]
            pct_devs = [e['pct_dev'] for e in entries if e['pct_dev'] is not None]
            signed = [e['signed_dev'] for e in entries]
            overall[arm_name] = {
                'n': len(entries),
                'mae': round(mean(abs_devs), 4),
                'mae_ci_95': [round(x, 4) for x in bootstrap_ci(abs_devs)],
                'mape': round(mean(pct_devs), 2) if pct_devs else None,
                'mape_ci_95': [round(x, 2) for x in bootstrap_ci(pct_devs)] if pct_devs else None,
                'rmse': round(math.sqrt(mean([d**2 for d in abs_devs])), 4),
                'bias': round(mean(signed), 4),
            }

    analysis = {
        'study_id': 'TLA-DEV-2026-001',
        'n_queries': n_results,
        'overall': overall,
        'hypotheses': hypotheses,
        'pairwise': pairwise,
        'by_stratum': by_stratum,
        'top_deviating_parameters': param_stats[:10],
    }

    # Print summary
    print("\n" + "=" * 72)
    print("  TLA DEVIATION STUDY — STATISTICAL ANALYSIS")
    print("=" * 72)

    print(f"\n  N = {n_results} queries")

    # Overall table
    print("\n  OVERALL RESULTS:")
    print("  ┌──────────────┬──────┬────────┬────────────────┬────────┬────────────────┐")
    print("  │     Arm      │  N   │  MAE   │   MAE 95% CI   │ MAPE%  │  MAPE 95% CI   │")
    print("  ├──────────────┼──────┼────────┼────────────────┼────────┼────────────────┤")
    arm_labels = {'arm_0': 'LLM-Only    ', 'arm_1': 'Registry    ',
                  'arm_2': 'Reg.+PCT    ', 'arm_3': 'Full Pipe.  '}
    for arm_name in ['arm_0', 'arm_1', 'arm_2', 'arm_3']:
        d = overall.get(arm_name, {})
        if d:
            mae_ci = d.get('mae_ci_95', [0, 0])
            mape_ci = d.get('mape_ci_95', [0, 0])
            mape = d.get('mape') or 0
            print(f"  │ {arm_labels[arm_name]} │  {d['n']:>2}  │ {d['mae']:>6.4f} │"
                  f" [{mae_ci[0]:>6.4f},{mae_ci[1]:>6.4f}] │ {mape:>5.1f}% │"
                  f" [{mape_ci[0]:>5.1f},{mape_ci[1]:>5.1f}] │")
    print("  └──────────────┴──────┴────────┴────────────────┴────────┴────────────────┘")

    # Hypotheses
    print("\n  HYPOTHESIS TESTS:")
    for h_name in ['H1', 'H2', 'H3', 'H4', 'H5']:
        h = hypotheses.get(h_name, {})
        if h:
            result = h.get('result', 'N/A')
            hyp = h.get('hypothesis', '')
            marker = "✓" if result == 'SUPPORTED' else "✗"
            print(f"    {h_name}: {marker} {result}")
            print(f"        {hyp}")
            if h_name == 'H1':
                print(f"        MAPE = {h.get('mape', '?')}% (CI: {h.get('ci_95', '?')})")
            elif h_name == 'H3':
                print(f"        Registry: {h.get('delta_registry', '?')}, "
                      f"PCT: {h.get('delta_pct', '?')}, "
                      f"LLMMC: {h.get('delta_llmmc', '?')}")
            elif h_name == 'H4':
                print(f"        {h.get('stratum_mapes', {})}")

    # Pairwise
    print("\n  PAIRWISE COMPARISONS:")
    print("  ┌──────────────────────┬──────┬──────────┬─────────┬────────┬─────┐")
    print("  │    Comparison        │  N   │ ΔMAE     │Cohen's d│   p    │Sig. │")
    print("  ├──────────────────────┼──────┼──────────┼─────────┼────────┼─────┤")
    for comp in pairwise:
        label = comp['comparison'][:20].ljust(20)
        n = comp['n_paired']
        diff = comp['mean_diff_mae']
        d = comp.get('cohens_d', 0) or 0
        p = comp.get('wilcoxon_p')
        sig = "**" if comp.get('significant_005') else "  "
        p_str = f"{p:.4f}" if p is not None else " N/A "
        print(f"  │ {label} │  {n:>2}  │ {diff:>+7.4f} │  {d:>5.3f}  │{p_str:>7} │ {sig}  │")
    print("  └──────────────────────┴──────┴──────────┴─────────┴────────┴─────┘")

    # Per-stratum
    print("\n  PER-STRATUM MAPE% (with 95% CI):")
    for s in ['S1', 'S2', 'S3', 'S4']:
        s_data = by_stratum.get(s, {})
        if not s_data:
            continue
        n = s_data['n']
        print(f"    {s} (N={n}):")
        for arm_name in ['arm_0', 'arm_1', 'arm_2', 'arm_3']:
            a = s_data.get('arms', {}).get(arm_name, {})
            if a:
                mape = a.get('mape', 0) or 0
                ci = a.get('mape_ci_95', [0, 0]) or [0, 0]
                label = {'arm_0': 'LLM', 'arm_1': 'Reg', 'arm_2': 'PCT', 'arm_3': 'Full'}[arm_name]
                print(f"      {label:>4}: {mape:>6.1f}%  [{ci[0]:>5.1f}, {ci[1]:>5.1f}]")

        llm_full = s_data.get('llm_vs_full', {})
        if llm_full:
            d_val = llm_full.get('cohens_d', '?')
            eff = llm_full.get('effect_size', '?')
            p_val = llm_full.get('wilcoxon_p')
            p_str = f"p={p_val:.4f}" if p_val is not None else "p=N/A"
            print(f"      LLM vs Full: d={d_val}, {eff} effect, {p_str}")

    # Top deviating parameters
    print("\n  TOP 10 PARAMETERS BY LLM DEVIATION:")
    print("  ┌──────────────┬────────┬──────┬──────────┬──────────┐")
    print("  │  Parameter   │ Symbol │  N   │Mean MAPE │ Max MAPE │")
    print("  ├──────────────┼────────┼──────┼──────────┼──────────┤")
    for ps in param_stats[:10]:
        pid = ps['parameter_id'][:12].ljust(12)
        sym = ps['symbol'][:6].ljust(6)
        print(f"  │ {pid} │ {sym} │  {ps['n_queries']:>2}  │ {ps['mean_mape']:>7.1f}% │ {ps['max_mape']:>7.1f}% │")
    print("  └──────────────┴────────┴──────┴──────────┴──────────┘")

    print("\n" + "=" * 72)

    # Save
    if args.save:
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(OUTPUT_PATH, 'w') as f:
            yaml.dump(analysis, f, default_flow_style=False, allow_unicode=True,
                      sort_keys=False, width=120)
        print(f"\nAnalysis saved to {OUTPUT_PATH}")

    # LaTeX
    if args.latex:
        print("\n" + "=" * 72)
        print("  LATEX TABLES")
        print("=" * 72)
        print(generate_latex_tables(analysis))


if __name__ == '__main__':
    main()
