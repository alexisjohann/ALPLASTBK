#!/usr/bin/env python3
"""
LLMMC Workflow Runner
=====================

Complete workflow for running LLMMC calibration:
1. Load Tier-1/2 anchors
2. Generate LLMMC prompts for each anchor
3. Parse LLM responses
4. Fit calibration model
5. Validate via LOO

Usage:
    python scripts/run_llmmc_workflow.py --generate-prompts
    python scripts/run_llmmc_workflow.py --parse-responses responses.json
    python scripts/run_llmmc_workflow.py --fit-calibration
    python scripts/run_llmmc_workflow.py --full-demo

Author: EBF Framework
Date: 2025-01-13
Protocol: HHH-LLMMC-1
"""

import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
import numpy as np

# Import calibrator
from llmmc_calibration import LLMMCCalibrator, CalibrationAnchor


# =============================================================================
# LLMMC Prompt Generation
# =============================================================================

LLMMC_THETA_PROMPT_TEMPLATE = """Du bist ein Experte für Verhaltensökonomie und Public Health Interventionen.

AUFGABE:
Schätze die Wirksamkeit einer Intervention auf einer Skala von 0.00 bis 1.00.

INTERVENTION:
- Typ: {intervention_type}
- Domain: {domain}
- Outcome: {outcome}
- Beschreibung: {description}

SKALA:
- 0.00 = Keine Wirkung (d ≈ 0)
- 0.30 = Kleine Wirkung (d ≈ 0.2)
- 0.50 = Mittlere Wirkung (d ≈ 0.5)
- 0.80 = Große Wirkung (d ≈ 0.8)
- 1.00 = Maximale Wirkung

WICHTIG:
- Basiere deine Schätzung auf der verfügbaren Evidenz zu diesem Interventionstyp
- Berücksichtige Meta-Analysen und große RCTs
- Gib nur eine Zahl zurück, keine Erklärung

ANTWORTFORMAT (exakt dieses JSON):
{{
  "theta": <deine Schätzung zwischen 0.00 und 1.00>,
  "confidence": <deine Konfidenz 0-100>,
  "reasoning_keywords": ["keyword1", "keyword2", "keyword3"]
}}
"""

LLMMC_4PERSPECTIVE_PROMPTS = {
    "direct": """Schätze direkt: Was ist die typische Wirksamkeit von {intervention_type} für {outcome}?
Antworte nur mit einer Zahl zwischen 0.00 und 1.00.""",

    "comparative": """Vergleiche: Ist {intervention_type} für {outcome} wirksamer oder weniger wirksam als typische Verhaltensinterventionen (Median d ≈ 0.3)?
- Viel schwächer: 0.10-0.20
- Etwas schwächer: 0.20-0.30
- Vergleichbar: 0.30-0.40
- Etwas stärker: 0.40-0.60
- Viel stärker: 0.60-0.90
Antworte nur mit einer Zahl.""",

    "theoretical": """Aus theoretischer Sicht: Welche Effektstärke würdest du für {intervention_type} bei {outcome} erwarten, basierend auf:
- Dual-Process-Theorie
- Prospect Theory
- Social Proof Mechanismen
Antworte nur mit einer Zahl zwischen 0.00 und 1.00.""",

    "calibration": """Kalibrierungs-Check: Default-Interventionen haben typischerweise θ ≈ 0.85, reine Information θ ≈ 0.15.
Wo auf dieser Skala liegt {intervention_type} für {outcome}?
Antworte nur mit einer Zahl zwischen 0.00 und 1.00."""
}


@dataclass
class LLMMCPrompt:
    """Generated prompt for LLMMC elicitation."""
    anchor_id: str
    intervention_type: str
    domain: str
    outcome: str
    phase: str
    description: str
    prompt_direct: str
    prompt_comparative: str
    prompt_theoretical: str
    prompt_calibration: str
    prompt_combined: str

    def to_dict(self) -> Dict:
        return {
            "anchor_id": self.anchor_id,
            "intervention_type": self.intervention_type,
            "domain": self.domain,
            "outcome": self.outcome,
            "phase": self.phase,
            "prompts": {
                "direct": self.prompt_direct,
                "comparative": self.prompt_comparative,
                "theoretical": self.prompt_theoretical,
                "calibration": self.prompt_calibration,
                "combined": self.prompt_combined
            }
        }


def generate_prompts_for_anchor(anchor: Dict) -> LLMMCPrompt:
    """Generate 4-perspective LLMMC prompts for an anchor."""
    intervention_type = anchor.get("intervention_type", "")
    domain = anchor.get("domain", "")
    outcome = anchor.get("outcome", "")
    phase = anchor.get("phase", "")
    description = anchor.get("effect_detail", "")
    anchor_id = anchor.get("anchor_id", "")

    # Generate perspective prompts
    prompts = {}
    for perspective, template in LLMMC_4PERSPECTIVE_PROMPTS.items():
        prompts[perspective] = template.format(
            intervention_type=intervention_type,
            outcome=outcome,
            domain=domain
        )

    # Generate combined prompt
    combined = LLMMC_THETA_PROMPT_TEMPLATE.format(
        intervention_type=intervention_type,
        domain=domain,
        outcome=outcome,
        description=description
    )

    return LLMMCPrompt(
        anchor_id=anchor_id,
        intervention_type=intervention_type,
        domain=domain,
        outcome=outcome,
        phase=phase,
        description=description,
        prompt_direct=prompts["direct"],
        prompt_comparative=prompts["comparative"],
        prompt_theoretical=prompts["theoretical"],
        prompt_calibration=prompts["calibration"],
        prompt_combined=combined
    )


# =============================================================================
# Tier-1/2 Anchor Loading
# =============================================================================

def load_tier12_anchors(path: Optional[Path] = None) -> Dict:
    """Load Tier-1/2 anchors from JSON file."""
    if path is None:
        path = Path(__file__).parent.parent / "data" / "calibration" / "tier12_anchors_raw.json"

    with open(path, 'r') as f:
        return json.load(f)


def load_pilot_set(path: Optional[Path] = None) -> Dict:
    """Load pilot calibration set."""
    if path is None:
        path = Path(__file__).parent.parent / "data" / "calibration" / "pilot_calibration_set_v1.json"

    with open(path, 'r') as f:
        return json.load(f)


# =============================================================================
# Response Parsing
# =============================================================================

@dataclass
class LLMMCResponse:
    """Parsed LLMMC response."""
    anchor_id: str
    theta_llm: float
    eu_llm: float  # Elicitation uncertainty
    n_samples: int
    perspective_means: Dict[str, float]
    consistency_score: float

    def to_dict(self) -> Dict:
        return {
            "anchor_id": self.anchor_id,
            "theta_llm": round(self.theta_llm, 4),
            "eu_llm": round(self.eu_llm, 4),
            "n_samples": self.n_samples,
            "perspective_means": {k: round(v, 4) for k, v in self.perspective_means.items()},
            "consistency_score": round(self.consistency_score, 4)
        }


def aggregate_llmmc_samples(
    samples: Dict[str, List[float]],
    anchor_id: str
) -> LLMMCResponse:
    """
    Aggregate LLMMC samples from multiple perspectives.

    Args:
        samples: Dict with keys 'direct', 'comparative', 'theoretical', 'calibration'
                 and values as lists of float samples
        anchor_id: Identifier for the anchor

    Returns:
        LLMMCResponse with aggregated statistics
    """
    all_samples = []
    perspective_means = {}

    for perspective, values in samples.items():
        if values:
            perspective_means[perspective] = float(np.mean(values))
            all_samples.extend(values)

    if not all_samples:
        raise ValueError(f"No samples for anchor {anchor_id}")

    # Global mean and SE
    theta_llm = float(np.mean(all_samples))
    eu_llm = float(np.std(all_samples) / np.sqrt(len(all_samples)))

    # Consistency score: 1 - normalized variance across perspectives
    if len(perspective_means) > 1:
        persp_values = list(perspective_means.values())
        var_between = np.var(persp_values)
        var_total = np.var(all_samples)
        consistency = 1.0 - (var_between / max(var_total, 0.001))
        consistency = max(0, min(1, consistency))
    else:
        consistency = 1.0

    return LLMMCResponse(
        anchor_id=anchor_id,
        theta_llm=theta_llm,
        eu_llm=eu_llm,
        n_samples=len(all_samples),
        perspective_means=perspective_means,
        consistency_score=consistency
    )


def parse_llm_json_response(response_text: str) -> Dict:
    """Parse JSON response from LLM."""
    # Try to extract JSON from response
    import re

    # Look for JSON block
    json_match = re.search(r'\{[^{}]*\}', response_text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass

    # Try to extract just a number
    number_match = re.search(r'0?\.\d+|\d+\.?\d*', response_text)
    if number_match:
        value = float(number_match.group())
        return {"theta": min(1.0, max(0.0, value))}

    raise ValueError(f"Could not parse response: {response_text[:100]}")


# =============================================================================
# Calibration Workflow
# =============================================================================

def run_calibration_from_anchors(
    tier12_data: Dict,
    llmmc_responses: Dict[str, LLMMCResponse]
) -> LLMMCCalibrator:
    """
    Run calibration using Tier-1/2 anchors and LLMMC responses.

    Args:
        tier12_data: Loaded tier12_anchors_raw.json data
        llmmc_responses: Dict mapping anchor_id to LLMMCResponse

    Returns:
        Fitted LLMMCCalibrator
    """
    calibrator = LLMMCCalibrator(min_anchors=8)

    mapping_results = tier12_data.get("theta_mapping_results", {})
    anchors = tier12_data.get("anchors", [])

    for anchor in anchors:
        anchor_id = anchor.get("anchor_id", "")
        citation = anchor.get("citation", "")

        # Get theta_true from mapping
        if anchor_id in mapping_results:
            theta_true = mapping_results[anchor_id].get("theta_true")
            se_true = mapping_results[anchor_id].get("se_true", 0.05)
        else:
            continue

        # Get LLMMC response
        if anchor_id not in llmmc_responses:
            print(f"  Warning: No LLMMC response for {anchor_id}, skipping")
            continue

        response = llmmc_responses[anchor_id]

        calibrator.add_anchor(
            name=anchor_id,
            theta_t12=theta_true,
            se_t12=se_true if se_true else 0.05,
            theta_llm=response.theta_llm,
            eu_llm=response.eu_llm,
            source=citation
        )

    print(f"\nAdded {len(calibrator.anchors)} anchors to calibrator")

    calibrator.fit()
    return calibrator


# =============================================================================
# Demo Mode: Simulated LLMMC
# =============================================================================

def simulate_llmmc_for_anchor(anchor: Dict, theta_true: float) -> LLMMCResponse:
    """
    Simulate LLMMC responses for demo purposes.

    In production, this would be replaced by actual LLM API calls.
    """
    # Simulate LLM bias and noise
    np.random.seed(hash(anchor.get("anchor_id", "")) % 2**32)

    bias = np.random.uniform(-0.1, 0.15)  # LLMs tend to slightly overestimate
    noise_scale = np.random.uniform(0.05, 0.12)

    # Generate samples for each perspective
    samples = {}
    for perspective in ["direct", "comparative", "theoretical", "calibration"]:
        perspective_bias = np.random.uniform(-0.05, 0.05)
        n_samples = 10
        perspective_samples = [
            np.clip(theta_true + bias + perspective_bias + np.random.normal(0, noise_scale), 0, 1)
            for _ in range(n_samples)
        ]
        samples[perspective] = perspective_samples

    return aggregate_llmmc_samples(samples, anchor.get("anchor_id", ""))


def run_full_demo():
    """Run complete demo of LLMMC calibration workflow."""
    print("=" * 70)
    print("LLMMC CALIBRATION WORKFLOW - FULL DEMO")
    print("=" * 70)

    # Step 1: Load Tier-1/2 anchors
    print("\n[Step 1] Loading Tier-1/2 anchors...")
    tier12_data = load_tier12_anchors()
    anchors = tier12_data.get("anchors", [])
    mapping_results = tier12_data.get("theta_mapping_results", {})
    print(f"  Loaded {len(anchors)} anchors")

    # Step 2: Generate prompts (for documentation)
    print("\n[Step 2] Generating LLMMC prompts...")
    prompts = []
    for anchor in anchors:
        prompt = generate_prompts_for_anchor(anchor)
        prompts.append(prompt)
        print(f"  ✓ {anchor.get('anchor_id')}")

    # Save prompts
    prompts_path = Path(__file__).parent.parent / "data" / "calibration" / "llmmc_prompts.json"
    with open(prompts_path, 'w') as f:
        json.dump([p.to_dict() for p in prompts], f, indent=2, ensure_ascii=False)
    print(f"\n  Saved prompts to: {prompts_path}")

    # Step 3: Simulate LLMMC responses (in production: call LLM API)
    print("\n[Step 3] Running LLMMC protocol (simulated for demo)...")
    llmmc_responses = {}
    for anchor in anchors:
        anchor_id = anchor.get("anchor_id")
        if anchor_id in mapping_results:
            theta_true = mapping_results[anchor_id].get("theta_true", 0.5)
            response = simulate_llmmc_for_anchor(anchor, theta_true)
            llmmc_responses[anchor_id] = response
            print(f"  {anchor_id}: θ_llm = {response.theta_llm:.3f} ± {response.eu_llm:.3f}")

    # Save responses
    responses_path = Path(__file__).parent.parent / "data" / "calibration" / "llmmc_responses_demo.json"
    with open(responses_path, 'w') as f:
        json.dump({k: v.to_dict() for k, v in llmmc_responses.items()}, f, indent=2)
    print(f"\n  Saved responses to: {responses_path}")

    # Step 4: Fit calibration
    print("\n[Step 4] Fitting calibration model...")
    calibrator = run_calibration_from_anchors(tier12_data, llmmc_responses)

    # Step 5: Show results
    print("\n" + calibrator.summary())

    # Step 6: Save calibration
    params = calibrator.get_calibration_params()
    loo = calibrator.loo_cross_validation()

    calibration_output = {
        "version": "1.0-demo",
        "date": "2025-01-13",
        "n_anchors": params["n_anchors"],
        "calibration_params": {
            "a": round(params["a"], 4),
            "b": round(params["b"], 4),
            "sigma_model": round(params["sigma_model"], 4),
            "tau": round(params["tau"], 4)
        },
        "validation": {
            "mae": round(loo.mae, 4),
            "rmse": round(loo.rmse, 4),
            "coverage_95": round(loo.coverage_95, 4),
            "spearman_rho": round(loo.spearman_rho, 4),
            "acceptable": bool(loo.is_acceptable())
        },
        "anchors_used": [a.name for a in calibrator.anchors]
    }

    cal_path = Path(__file__).parent.parent / "data" / "calibration" / "calibration_v1_demo.json"
    with open(cal_path, 'w') as f:
        json.dump(calibration_output, f, indent=2)
    print(f"\nSaved calibration to: {cal_path}")

    # Step 7: Demo calibration of new parameter
    print("\n" + "=" * 70)
    print("DEMO: Calibrating a new parameter")
    print("=" * 70)

    # Example: New parameter estimate from LLMMC
    theta_raw = 0.68
    eu_raw = 0.09

    result = calibrator.calibrate(theta_raw, eu_raw)

    print(f"\nNew parameter (uncalibrated):")
    print(f"  θ_LLM = {theta_raw:.3f} ± {eu_raw:.3f}")
    print(f"\nAfter calibration:")
    print(f"  θ_cal = {result.theta_calibrated:.3f}")
    print(f"  θ_final = {result.theta_final:.3f} ± {result.sigma_final:.3f}")
    print(f"  95% CI: [{result.ci_95[0]:.3f}, {result.ci_95[1]:.3f}]")
    print(f"  Shrinkage λ = {result.shrinkage_factor:.3f}")

    print("\n" + "=" * 70)
    print("WORKFLOW COMPLETE")
    print("=" * 70)
    print(f"""
Nächste Schritte für Produktion:
1. Ersetze simulate_llmmc_for_anchor() durch echte LLM-API-Calls
2. Führe 4-Perspektiven-Protokoll mit Temperature-Sampling durch
3. Füge weitere Tier-1/2 Anchors hinzu (Ziel: n ≥ 16)
4. Validiere gegen Hold-out-Set
5. Freeze als calibration_v1.json

Dateien erstellt:
- data/calibration/llmmc_prompts.json
- data/calibration/llmmc_responses_demo.json
- data/calibration/calibration_v1_demo.json
""")


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="LLMMC Calibration Workflow Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_llmmc_workflow.py --full-demo
  python run_llmmc_workflow.py --generate-prompts
  python run_llmmc_workflow.py --show-anchors
        """
    )

    parser.add_argument("--full-demo", action="store_true",
                        help="Run full demo with simulated LLMMC responses")
    parser.add_argument("--generate-prompts", action="store_true",
                        help="Generate LLMMC prompts for all anchors")
    parser.add_argument("--show-anchors", action="store_true",
                        help="Display all Tier-1/2 anchors with θ_true values")
    parser.add_argument("--parse-responses", type=str,
                        help="Parse LLMMC responses from JSON file")
    parser.add_argument("--fit-calibration", action="store_true",
                        help="Fit calibration from existing responses")

    args = parser.parse_args()

    if args.full_demo:
        run_full_demo()
    elif args.generate_prompts:
        print("Generating LLMMC prompts...")
        tier12_data = load_tier12_anchors()
        for anchor in tier12_data.get("anchors", []):
            prompt = generate_prompts_for_anchor(anchor)
            print(f"\n{'='*60}")
            print(f"Anchor: {prompt.anchor_id}")
            print(f"{'='*60}")
            print("\n[Combined Prompt]:")
            print(prompt.prompt_combined)
    elif args.show_anchors:
        print("Tier-1/2 Calibration Anchors")
        print("=" * 70)
        tier12_data = load_tier12_anchors()
        mapping = tier12_data.get("theta_mapping_results", {})
        for anchor in tier12_data.get("anchors", []):
            anchor_id = anchor.get("anchor_id")
            if anchor_id in mapping:
                theta = mapping[anchor_id].get("theta_true", "?")
                se = mapping[anchor_id].get("se_true", "?")
                print(f"{anchor_id}:")
                print(f"  θ_true = {theta}, SE = {se}")
                print(f"  Citation: {anchor.get('citation', '')}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
