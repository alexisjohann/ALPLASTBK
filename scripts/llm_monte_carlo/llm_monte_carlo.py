"""
LLM Monte Carlo Estimation for Ψ-FEPSDE Coefficients
=====================================================

This script implements the LLM-MC methodology described in Appendix AN
of "Complementarity and Context: A Unified Framework for Economic Rationality"

Author: FehrAdvice & Partners AG / University of Zurich
Date: January 2026
Version: 1.0

Usage:
    python llm_monte_carlo.py --api-key YOUR_KEY --iterations 100 --output results.csv
"""

import anthropic
import json
import random
import time
import argparse
import csv
from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
import statistics
import re


# =============================================================================
# CONFIGURATION
# =============================================================================

@dataclass
class Coefficient:
    """Represents a single Ψ-FEPSDE coefficient to estimate."""
    psi_dim: str
    psi_name: str
    fepsde_dim: str
    fepsde_name: str
    theoretical_sign: str  # "+", "-", or "?"
    baseline_estimate: float
    
    @property
    def id(self) -> str:
        return f"γ({self.psi_dim}→{self.fepsde_dim})"


# The 12 priority coefficients for Monte Carlo estimation
TOP_12_COEFFICIENTS = [
    Coefficient("Ψ_S", "Social Capital", "S", "Social", "+", 0.85),
    Coefficient("Ψ_E", "Economic Development", "F", "Financial", "+", 0.82),
    Coefficient("Ψ_K", "Information Transparency", "D", "Digital", "+", 0.75),
    Coefficient("Ψ_I", "Institutional Quality", "F", "Financial", "+", 0.72),
    Coefficient("Ψ_M", "Market Scope", "F", "Financial", "+", 0.70),
    Coefficient("Ψ_C", "Cognitive Capacity", "D", "Digital", "+", 0.68),
    Coefficient("Ψ_T", "Temporal Stability", "F", "Financial", "+", 0.65),
    Coefficient("Ψ_T", "Temporal Stability", "Eco", "Ecological", "+", 0.62),
    Coefficient("Ψ_F", "Factor Flexibility", "F", "Financial", "+", 0.58),
    Coefficient("Ψ_C", "Cognitive Capacity", "F", "Financial", "+", 0.55),
    Coefficient("Ψ_I", "Institutional Quality", "Eco", "Ecological", "+", 0.51),
    Coefficient("Ψ_T", "Temporal Stability", "E", "Emotional", "-", -0.25),
]


# =============================================================================
# PROMPT TEMPLATES
# =============================================================================

PROMPT_TEMPLATES = {
    "direct": """You are an expert in behavioral economics and the EBF framework.

Context: The Ψ-FEPSDE interaction model describes how context dimensions (Ψ) modify the weights of utility dimensions (FEPSDE) in human decision-making.

Task: Estimate the coefficient γ({psi_dim}→{fepsde_dim}) on a scale from -1.0 to +1.0.

- {psi_dim} ({psi_name}): {psi_description}
- {fepsde_dim} ({fepsde_name}): {fepsde_description}

The coefficient represents: How strongly does a HIGH value of {psi_dim} increase (+) or decrease (-) the weight of the {fepsde_name} dimension in an individual's utility function?

Provide ONLY a single number between -1.0 and +1.0. No explanation.""",

    "comparative": """In behavioral economics, context (Ψ) modifies how people weight different utility dimensions (FEPSDE).

Consider two populations:
- Population A: LOW {psi_name} ({psi_dim} = 0.2)
- Population B: HIGH {psi_name} ({psi_dim} = 0.8)

Question: How much MORE or LESS does Population B weight the {fepsde_name} dimension compared to Population A?

Express as a coefficient from -1.0 (B weights it much LESS) to +1.0 (B weights it much MORE).

Respond with ONLY a number.""",

    "scenario": """Imagine two decision-makers facing identical choices:

Person X lives in a context with LOW {psi_name}:
- {low_psi_example}

Person Y lives in a context with HIGH {psi_name}:
- {high_psi_example}

When making decisions, how much more does Person Y weight {fepsde_name} outcomes compared to Person X?

Scale: -1.0 (Y weights it much less) to +1.0 (Y weights it much more)

Answer with a single number only.""",

    "theoretical": """From the perspective of behavioral economic theory:

The context dimension {psi_dim} ({psi_name}) captures: {psi_description}

The utility dimension {fepsde_dim} ({fepsde_name}) captures: {fepsde_description}

Theoretically, what is the expected interaction coefficient γ({psi_dim}→{fepsde_dim})?

Consider:
- Does high {psi_name} enable, amplify, or constrain {fepsde_name} considerations?
- What does empirical literature suggest about this relationship?

Provide a coefficient estimate from -1.0 to +1.0.

Respond with ONLY the number.""",

    "calibration": """You are calibrating a behavioral economic model.

Parameter: γ({psi_dim}→{fepsde_dim})
Range: [-1.0, +1.0]
Meaning: Effect of {psi_name} on the utility weight of {fepsde_name}

Calibration anchors:
- γ = +1.0: Perfect positive relationship (high Ψ → high FEPSDE weight)
- γ = +0.5: Moderate positive relationship
- γ = 0.0: No systematic relationship
- γ = -0.5: Moderate negative relationship
- γ = -1.0: Perfect negative relationship

Based on behavioral economic evidence, what value should γ({psi_dim}→{fepsde_dim}) take?

Output ONLY the number."""
}


# Dimension descriptions for prompt generation
PSI_DESCRIPTIONS = {
    "Ψ_I": "Formal institutions, rule of law, contract enforcement, property rights protection",
    "Ψ_S": "Generalized trust, social norms, network density, community cohesion",
    "Ψ_C": "Cognitive skills, numeracy, financial literacy, information processing capacity",
    "Ψ_K": "Information transparency, signal quality, press freedom, market transparency",
    "Ψ_E": "Economic development, GDP per capita, market thickness, resource availability",
    "Ψ_T": "Temporal stability, policy predictability, low uncertainty, long planning horizons",
    "Ψ_M": "Market scope, trade openness, geographic reach, export diversity",
    "Ψ_F": "Factor flexibility, labor mobility, ease of hiring/firing, capital mobility"
}

FEPSDE_DESCRIPTIONS = {
    "F": "Financial outcomes: income, wealth, monetary gains and losses",
    "E": "Emotional outcomes: happiness, satisfaction, stress, anxiety",
    "P": "Physical outcomes: health, energy, bodily wellbeing",
    "S": "Social outcomes: status, relationships, reputation, belonging",
    "D": "Digital outcomes: connectivity, online presence, digital capital",
    "Eco": "Ecological outcomes: environmental impact, sustainability, nature connection"
}

LOW_PSI_EXAMPLES = {
    "Ψ_I": "Weak rule of law, unreliable contracts, corruption is common",
    "Ψ_S": "Low trust in strangers, weak community ties, social fragmentation",
    "Ψ_C": "Low financial literacy, difficulty processing complex information",
    "Ψ_K": "Opaque markets, unreliable information, high information asymmetry",
    "Ψ_E": "Low income, limited market access, resource scarcity",
    "Ψ_T": "High uncertainty, volatile policies, short planning horizons",
    "Ψ_M": "Isolated local markets, low trade, limited geographic reach",
    "Ψ_F": "Rigid labor markets, difficult to change jobs, low mobility"
}

HIGH_PSI_EXAMPLES = {
    "Ψ_I": "Strong rule of law, reliable contracts, low corruption",
    "Ψ_S": "High generalized trust, strong community bonds, dense networks",
    "Ψ_C": "High financial literacy, skilled at processing complex decisions",
    "Ψ_K": "Transparent markets, reliable information, low asymmetry",
    "Ψ_E": "High income, thick markets, abundant resources",
    "Ψ_T": "Stable environment, predictable policies, long planning horizons",
    "Ψ_M": "Global market access, high trade openness, diverse exports",
    "Ψ_F": "Flexible labor markets, easy job changes, high mobility"
}


# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def generate_prompt(coef: Coefficient, template_name: str) -> str:
    """Generate a prompt for estimating a specific coefficient."""
    template = PROMPT_TEMPLATES[template_name]
    
    return template.format(
        psi_dim=coef.psi_dim,
        psi_name=coef.psi_name,
        psi_description=PSI_DESCRIPTIONS[coef.psi_dim],
        fepsde_dim=coef.fepsde_dim,
        fepsde_name=coef.fepsde_name,
        fepsde_description=FEPSDE_DESCRIPTIONS[coef.fepsde_dim],
        low_psi_example=LOW_PSI_EXAMPLES.get(coef.psi_dim, ""),
        high_psi_example=HIGH_PSI_EXAMPLES.get(coef.psi_dim, "")
    )


def parse_coefficient(response: str) -> Optional[float]:
    """Extract a coefficient value from LLM response."""
    # Try to find a number in the response
    patterns = [
        r'^[-+]?[0-9]*\.?[0-9]+$',  # Just a number
        r'([-+]?[0-9]*\.?[0-9]+)',   # Number anywhere
    ]
    
    text = response.strip()
    
    # First try: exact match
    if re.match(patterns[0], text):
        val = float(text)
        if -1.0 <= val <= 1.0:
            return val
    
    # Second try: find any number
    matches = re.findall(patterns[1], text)
    for match in matches:
        try:
            val = float(match)
            if -1.0 <= val <= 1.0:
                return val
        except:
            continue
    
    return None


def call_claude(client: anthropic.Anthropic, prompt: str, temperature: float) -> str:
    """Make a single API call to Claude."""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=50,
        temperature=temperature,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text


def estimate_coefficient_mc(
    client: anthropic.Anthropic,
    coef: Coefficient,
    n_iterations: int = 100,
    verbose: bool = True
) -> Dict:
    """
    Run Monte Carlo estimation for a single coefficient.
    
    Returns dict with:
    - estimates: list of all estimates
    - mean, std, ci_lower, ci_upper
    - variance_decomposition
    """
    estimates = []
    metadata = []
    
    templates = list(PROMPT_TEMPLATES.keys())
    temperatures = [0.3, 0.5, 0.7, 0.9]
    
    for i in range(n_iterations):
        # Sample variation dimensions
        template = random.choice(templates)
        temp = random.choice(temperatures)
        
        # Generate and call
        prompt = generate_prompt(coef, template)
        
        try:
            response = call_claude(client, prompt, temp)
            value = parse_coefficient(response)
            
            if value is not None:
                estimates.append(value)
                metadata.append({
                    "iteration": i,
                    "template": template,
                    "temperature": temp,
                    "value": value,
                    "raw_response": response
                })
            
            if verbose and (i + 1) % 10 == 0:
                print(f"  {coef.id}: {i+1}/{n_iterations} iterations, "
                      f"current mean = {statistics.mean(estimates):.3f}")
        
        except Exception as e:
            print(f"  Error at iteration {i}: {e}")
            time.sleep(2)
        
        # Rate limiting
        time.sleep(0.5)
    
    # Compute statistics
    if len(estimates) < 5:
        return {"error": "Too few valid estimates", "n_valid": len(estimates)}
    
    mean = statistics.mean(estimates)
    std = statistics.stdev(estimates)
    sorted_est = sorted(estimates)
    n = len(sorted_est)
    ci_lower = sorted_est[int(n * 0.025)]
    ci_upper = sorted_est[int(n * 0.975)]
    
    # Variance decomposition by template
    by_template = {}
    for m in metadata:
        t = m["template"]
        if t not in by_template:
            by_template[t] = []
        by_template[t].append(m["value"])
    
    template_means = {t: statistics.mean(v) for t, v in by_template.items() if len(v) > 1}
    
    # Variance decomposition by temperature
    by_temp = {}
    for m in metadata:
        t = m["temperature"]
        if t not in by_temp:
            by_temp[t] = []
        by_temp[t].append(m["value"])
    
    temp_means = {t: statistics.mean(v) for t, v in by_temp.items() if len(v) > 1}
    
    return {
        "coefficient": coef.id,
        "psi_dim": coef.psi_dim,
        "fepsde_dim": coef.fepsde_dim,
        "n_iterations": n_iterations,
        "n_valid": len(estimates),
        "baseline": coef.baseline_estimate,
        "mean": mean,
        "std": std,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "min": min(estimates),
        "max": max(estimates),
        "template_means": template_means,
        "temperature_means": temp_means,
        "all_estimates": estimates,
        "metadata": metadata
    }


def run_full_estimation(
    api_key: str,
    coefficients: List[Coefficient],
    n_iterations: int = 100,
    output_file: str = "llm_mc_results.csv"
) -> List[Dict]:
    """Run Monte Carlo estimation for all specified coefficients."""
    
    client = anthropic.Anthropic(api_key=api_key)
    results = []
    
    print(f"\n{'='*60}")
    print(f"LLM Monte Carlo Estimation")
    print(f"{'='*60}")
    print(f"Coefficients: {len(coefficients)}")
    print(f"Iterations per coefficient: {n_iterations}")
    print(f"Total API calls: ~{len(coefficients) * n_iterations}")
    print(f"{'='*60}\n")
    
    for i, coef in enumerate(coefficients):
        print(f"\n[{i+1}/{len(coefficients)}] Estimating {coef.id}...")
        print(f"  Baseline: {coef.baseline_estimate:.2f}")
        print(f"  Expected sign: {coef.theoretical_sign}")
        
        result = estimate_coefficient_mc(
            client, coef, n_iterations, verbose=True
        )
        results.append(result)
        
        if "error" not in result:
            print(f"  Result: μ = {result['mean']:.3f}, "
                  f"σ = {result['std']:.3f}, "
                  f"95% CI = [{result['ci_lower']:.3f}, {result['ci_upper']:.3f}]")
    
    # Save results
    save_results(results, output_file)
    
    return results


def save_results(results: List[Dict], filename: str):
    """Save results to CSV and JSON."""
    
    # Summary CSV
    csv_file = filename.replace('.csv', '_summary.csv')
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'coefficient', 'psi_dim', 'fepsde_dim', 'baseline',
            'mean', 'std', 'ci_lower', 'ci_upper', 'n_valid'
        ])
        for r in results:
            if "error" not in r:
                writer.writerow([
                    r['coefficient'], r['psi_dim'], r['fepsde_dim'],
                    r['baseline'], f"{r['mean']:.4f}", f"{r['std']:.4f}",
                    f"{r['ci_lower']:.4f}", f"{r['ci_upper']:.4f}", r['n_valid']
                ])
    
    # Full JSON
    json_file = filename.replace('.csv', '_full.json')
    
    # Convert for JSON serialization
    json_results = []
    for r in results:
        jr = {k: v for k, v in r.items() if k != 'metadata'}
        jr['metadata_count'] = len(r.get('metadata', []))
        json_results.append(jr)
    
    with open(json_file, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'n_coefficients': len(results),
            'results': json_results
        }, f, indent=2)
    
    print(f"\nResults saved to:")
    print(f"  Summary: {csv_file}")
    print(f"  Full data: {json_file}")


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='LLM Monte Carlo Estimation for Ψ-FEPSDE Coefficients'
    )
    parser.add_argument(
        '--api-key', required=True,
        help='Anthropic API key'
    )
    parser.add_argument(
        '--iterations', type=int, default=100,
        help='Number of iterations per coefficient (default: 100)'
    )
    parser.add_argument(
        '--output', default='llm_mc_results.csv',
        help='Output filename (default: llm_mc_results.csv)'
    )
    parser.add_argument(
        '--coefficients', default='top12',
        choices=['top12', 'all48'],
        help='Which coefficients to estimate (default: top12)'
    )
    
    args = parser.parse_args()
    
    if args.coefficients == 'top12':
        coefficients = TOP_12_COEFFICIENTS
    else:
        # TODO: Generate all 48 coefficients
        coefficients = TOP_12_COEFFICIENTS
    
    results = run_full_estimation(
        api_key=args.api_key,
        coefficients=coefficients,
        n_iterations=args.iterations,
        output_file=args.output
    )
    
    # Print summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"{'Coefficient':<20} {'Baseline':>10} {'Mean':>10} {'Std':>10} {'95% CI':>20}")
    print("-" * 70)
    for r in results:
        if "error" not in r:
            ci = f"[{r['ci_lower']:.2f}, {r['ci_upper']:.2f}]"
            print(f"{r['coefficient']:<20} {r['baseline']:>10.2f} {r['mean']:>10.3f} "
                  f"{r['std']:>10.3f} {ci:>20}")


if __name__ == "__main__":
    main()
