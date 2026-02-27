#!/usr/bin/env python3
"""
LLMMC → R-Score: Vollständige End-to-End Pipeline
==================================================

Pipeline: LLM Estimates → Kalibration → Mapping → R-Score → Entscheidung

Komponenten:
1. Kalibration (calibration_d_v1, calibration_pp_v1)
2. Mapping (piecewise linear, mapping_v1)
3. R-Score (Monte Carlo mit Unsicherheitspropagation)
4. Entscheidung (NO-GO / PILOT / GO)

Usage:
    python llmmc_to_rscore.py --demo
    python llmmc_to_rscore.py --config config.json
    python llmmc_to_rscore.py --interactive

Author: EBF Framework
Date: 2025-01-13
Protocol: HHH-LLMMC-RSCORE-1
"""

import numpy as np
import json
import argparse
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
from pathlib import Path

# Import from local modules
from theta_mapping import (
    build_alpha_theta,
    get_mapping_config,
    print_mapping_report,
    MAPPING_VERSION
)
from r_score import (
    r_score_mc,
    RScoreResult,
    print_rscore_report
)


@dataclass
class PipelineConfig:
    """Configuration for the full pipeline."""
    alpha_specs: List[Dict]     # [{type, llm_hat, eu_llm, name?}, ...]
    gamma_llm: float            # LLM estimate for γ
    gamma_eu: float             # γ uncertainty
    norm_a: float               # Design norm ‖a‖
    norm_k: float               # Context norm ‖K‖
    threshold: float = 6.0      # Decision threshold T
    n_mc: int = 20000           # Monte Carlo samples

    def to_dict(self) -> Dict:
        return {
            "alpha_specs": self.alpha_specs,
            "gamma_llm": self.gamma_llm,
            "gamma_eu": self.gamma_eu,
            "norm_a": self.norm_a,
            "norm_k": self.norm_k,
            "threshold": self.threshold,
            "n_mc": self.n_mc
        }

    @classmethod
    def from_dict(cls, d: Dict) -> "PipelineConfig":
        return cls(
            alpha_specs=d["alpha_specs"],
            gamma_llm=d["gamma_llm"],
            gamma_eu=d["gamma_eu"],
            norm_a=d["norm_a"],
            norm_k=d["norm_k"],
            threshold=d.get("threshold", 6.0),
            n_mc=d.get("n_mc", 20000)
        )


@dataclass
class PipelineResult:
    """Full pipeline result."""
    # Inputs
    config: PipelineConfig

    # Mapping results
    alpha_hat_theta: np.ndarray
    alpha_eu_theta: np.ndarray

    # R-Score results
    r_score: RScoreResult

    # Decision
    decision: str
    decision_prob: float

    def to_dict(self) -> Dict:
        return {
            "config": self.config.to_dict(),
            "mapping": {
                "alpha_hat_theta": self.alpha_hat_theta.round(4).tolist(),
                "alpha_eu_theta": self.alpha_eu_theta.round(4).tolist(),
                "sum_alpha": round(float(self.alpha_hat_theta.sum()), 4),
                "version": MAPPING_VERSION
            },
            "r_score": self.r_score.to_dict(),
            "decision": {
                "result": self.decision,
                "threshold": self.config.threshold,
                "prob_gt_threshold": round(self.decision_prob, 4)
            }
        }


def run_pipeline(config: PipelineConfig) -> PipelineResult:
    """
    Run full LLMMC → R-Score pipeline.

    Steps:
    1. Build α vector on 0-1 scale (with calibration + mapping)
    2. Compute R-Score with Monte Carlo
    3. Generate decision

    Args:
        config: Pipeline configuration

    Returns:
        PipelineResult with all intermediate and final results
    """
    # Step 1: Build alpha vector
    alpha_hat, alpha_eu = build_alpha_theta(config.alpha_specs, n_mc=config.n_mc)

    # Step 2: Compute R-Score
    r_result = r_score_mc(
        alpha_hat=alpha_hat,
        alpha_eu=alpha_eu,
        gamma_hat=config.gamma_llm,
        gamma_eu=config.gamma_eu,
        norm_a=config.norm_a,
        norm_k=config.norm_k,
        n=config.n_mc,
        thresholds=[3.0, 4.0, 5.0, config.threshold, 7.0, 8.0]
    )

    # Step 3: Decision
    decision = r_result.decision(config.threshold)
    decision_prob = r_result.prob_gt_threshold.get(config.threshold, 0)

    return PipelineResult(
        config=config,
        alpha_hat_theta=alpha_hat,
        alpha_eu_theta=alpha_eu,
        r_score=r_result,
        decision=decision,
        decision_prob=decision_prob
    )


def print_full_report(result: PipelineResult):
    """Print comprehensive pipeline report."""
    config = result.config

    print("\n" + "=" * 70)
    print("LLMMC → R-SCORE PIPELINE REPORT")
    print("=" * 70)

    # Input summary
    print(f"\n📥 INPUTS")
    print(f"   n_α = {len(config.alpha_specs)} Parameter")
    print(f"   γ = {config.gamma_llm} ± {config.gamma_eu}")
    print(f"   ‖a‖ = {config.norm_a}, ‖K‖ = {config.norm_k}")
    print(f"   Schwelle T = {config.threshold}")

    # Mapping results
    print_mapping_report(config.alpha_specs, result.alpha_hat_theta, result.alpha_eu_theta)

    # R-Score results
    print_rscore_report(result.r_score, config.threshold)

    # Summary
    decision_emoji = {"GO": "🟢", "PILOT": "🟡", "NO-GO": "🔴"}[result.decision]
    print(f"\n{'='*70}")
    print(f"{decision_emoji} FINALE ENTSCHEIDUNG: {result.decision}")
    print(f"   P(R > {config.threshold}) = {result.decision_prob:.1%}")
    print("=" * 70)


def demo():
    """Run demo with example configuration."""
    print("\n" + "=" * 70)
    print("LLMMC → R-SCORE DEMO")
    print("=" * 70)

    # Example: 6 mixed parameters (typical intervention design)
    config = PipelineConfig(
        alpha_specs=[
            {"type": "d",  "llm_hat": 0.70, "eu_llm": 0.12, "name": "α_Awareness"},
            {"type": "d",  "llm_hat": 0.55, "eu_llm": 0.10, "name": "α_Willingness"},
            {"type": "pp", "llm_hat": 25.0, "eu_llm": 6.0,  "name": "α_Default"},
            {"type": "d",  "llm_hat": 0.80, "eu_llm": 0.10, "name": "α_Trigger"},
            {"type": "pp", "llm_hat": 10.0, "eu_llm": 5.0,  "name": "α_Reminder"},
            {"type": "d",  "llm_hat": 0.60, "eu_llm": 0.11, "name": "α_Action"},
        ],
        gamma_llm=0.18,
        gamma_eu=0.10,
        norm_a=2.15,
        norm_k=2.45,
        threshold=5.0,  # Lower threshold for demo
        n_mc=50000
    )

    result = run_pipeline(config)
    print_full_report(result)

    # JSON output
    print("\n📄 JSON OUTPUT")
    output = result.to_dict()
    print(json.dumps(output, indent=2))

    return result


def run_from_config_file(path: str) -> PipelineResult:
    """Run pipeline from JSON config file."""
    with open(path, 'r') as f:
        config_dict = json.load(f)

    config = PipelineConfig.from_dict(config_dict)
    result = run_pipeline(config)
    print_full_report(result)

    return result


def interactive_mode():
    """Interactive parameter entry."""
    print("\n" + "=" * 70)
    print("LLMMC → R-SCORE: INTERAKTIVER MODUS")
    print("=" * 70)

    alpha_specs = []
    print("\nGib die α-Parameter ein (leer = fertig):")

    i = 1
    while True:
        print(f"\n--- α_{i} ---")
        type_input = input("  Typ (d/pp) [leer=fertig]: ").strip().lower()
        if not type_input:
            break
        if type_input not in ["d", "pp"]:
            print("  ⚠ Typ muss 'd' oder 'pp' sein")
            continue

        try:
            llm_hat = float(input(f"  LLM Schätzung ({type_input}): "))
            eu_llm = float(input("  Elicitation Uncertainty: "))
            name = input("  Name (optional): ").strip() or f"α_{i}"

            alpha_specs.append({
                "type": type_input,
                "llm_hat": llm_hat,
                "eu_llm": eu_llm,
                "name": name
            })
            i += 1
        except ValueError:
            print("  ⚠ Ungültige Eingabe")

    if not alpha_specs:
        print("Keine Parameter eingegeben. Abbruch.")
        return

    print("\n--- γ (Komplementarität) ---")
    gamma_llm = float(input("  γ LLM Schätzung: "))
    gamma_eu = float(input("  γ Uncertainty: "))

    print("\n--- Normen ---")
    norm_a = float(input("  ‖a‖ (Design-Norm): "))
    norm_k = float(input("  ‖K‖ (Kontext-Norm): "))

    threshold = float(input("\n  Entscheidungs-Schwelle T [6.0]: ").strip() or "6.0")

    config = PipelineConfig(
        alpha_specs=alpha_specs,
        gamma_llm=gamma_llm,
        gamma_eu=gamma_eu,
        norm_a=norm_a,
        norm_k=norm_k,
        threshold=threshold
    )

    result = run_pipeline(config)
    print_full_report(result)

    # Save config
    save = input("\nKonfiguration speichern? (j/n): ").strip().lower()
    if save == "j":
        filename = input("Dateiname [config.json]: ").strip() or "config.json"
        with open(filename, 'w') as f:
            json.dump(config.to_dict(), f, indent=2)
        print(f"Gespeichert: {filename}")


def main():
    parser = argparse.ArgumentParser(
        description="LLMMC → R-Score: Vollständige Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Pipeline: LLM → Kalibration → Mapping → R-Score → Entscheidung

Beispiele:
  python llmmc_to_rscore.py --demo
  python llmmc_to_rscore.py --config intervention_config.json
  python llmmc_to_rscore.py --interactive
        """
    )

    parser.add_argument("--demo", action="store_true",
                        help="Run demo with example parameters")
    parser.add_argument("--config", type=str,
                        help="Path to JSON config file")
    parser.add_argument("--interactive", action="store_true",
                        help="Interactive parameter entry")
    parser.add_argument("--json", action="store_true",
                        help="Output JSON only (no report)")

    args = parser.parse_args()

    if args.demo:
        demo()
    elif args.config:
        run_from_config_file(args.config)
    elif args.interactive:
        interactive_mode()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
