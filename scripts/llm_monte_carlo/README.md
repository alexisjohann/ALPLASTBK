# LLM Monte Carlo Estimation for Ψ-FEPSDE Coefficients

## Overview

This script implements the LLM-MC (Large Language Model Monte Carlo) methodology for extracting probabilistic knowledge from language models with uncertainty quantification.

**Paper Reference**: Appendix AN of "Complementarity and Context: A Unified Framework for Economic Rationality"

## The Problem

Standard LLM knowledge extraction produces **point estimates** without uncertainty:
```
1 Query → 1 Estimate → No confidence bounds
```

This script produces **distributional estimates**:
```
N Queries × M Variations → Distribution → μ, σ, CI₉₅
```

## Installation

```bash
pip install anthropic
```

## Usage

### Basic Usage
```bash
python llm_monte_carlo.py --api-key YOUR_ANTHROPIC_KEY --iterations 100
```

### Full Options
```bash
python llm_monte_carlo.py \
    --api-key YOUR_KEY \
    --iterations 100 \
    --output my_results.csv \
    --coefficients top12
```

### Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `--api-key` | required | Your Anthropic API key |
| `--iterations` | 100 | Iterations per coefficient |
| `--output` | llm_mc_results.csv | Output filename |
| `--coefficients` | top12 | Which set: `top12` or `all48` |

## Methodology

### Three Variation Dimensions

1. **Prompt Variation**: 5 semantically equivalent prompt templates
   - `direct`: Straightforward parameter request
   - `comparative`: Compare high vs. low Ψ populations
   - `scenario`: Concrete decision scenarios
   - `theoretical`: Theory-based reasoning
   - `calibration`: Explicit anchoring

2. **Temperature Variation**: τ ∈ {0.3, 0.5, 0.7, 0.9}

3. **Random Sampling**: Each iteration randomly samples template × temperature

### Variance Decomposition

The total variance decomposes into:

```
Var(γ̂) = Var_template + Var_temperature + Var_residual
```

This tells us **where** uncertainty comes from.

## Output Files

### Summary CSV (`*_summary.csv`)
```csv
coefficient,psi_dim,fepsde_dim,baseline,mean,std,ci_lower,ci_upper,n_valid
γ(Ψ_S→S),Ψ_S,S,0.85,0.823,0.089,0.651,0.978,97
...
```

### Full JSON (`*_full.json`)
```json
{
  "timestamp": "2026-01-04T...",
  "n_coefficients": 12,
  "results": [
    {
      "coefficient": "γ(Ψ_S→S)",
      "mean": 0.823,
      "std": 0.089,
      "ci_lower": 0.651,
      "ci_upper": 0.978,
      "template_means": {"direct": 0.81, "comparative": 0.85, ...},
      "temperature_means": {0.3: 0.79, 0.5: 0.82, ...},
      "all_estimates": [0.78, 0.85, 0.81, ...]
    }
  ]
}
```

## The 12 Priority Coefficients

| Rank | Coefficient | Interpretation |
|------|-------------|----------------|
| 1 | γ(Ψ_S→S) | Social capital → Social utility weight |
| 2 | γ(Ψ_E→F) | Economic development → Financial weight |
| 3 | γ(Ψ_K→D) | Information transparency → Digital weight |
| 4 | γ(Ψ_I→F) | Institutional quality → Financial weight |
| 5 | γ(Ψ_M→F) | Market scope → Financial weight |
| 6 | γ(Ψ_C→D) | Cognitive capacity → Digital weight |
| 7 | γ(Ψ_T→F) | Temporal stability → Financial weight |
| 8 | γ(Ψ_T→Eco) | Temporal stability → Ecological weight |
| 9 | γ(Ψ_F→F) | Factor flexibility → Financial weight |
| 10 | γ(Ψ_C→F) | Cognitive capacity → Financial weight |
| 11 | γ(Ψ_I→Eco) | Institutional quality → Ecological weight |
| 12 | γ(Ψ_T→E) | Temporal stability → Emotional weight |

## Validation Architecture

### Level 1: Internal Consistency
- Do symmetric prompts yield symmetric estimates?
- Is transitivity preserved?
- Do signs match theoretical predictions?

### Level 2: Convergence Diagnostics
- Does increasing N reduce SE?
- Is the distribution unimodal or multimodal?

### Level 3: Cross-Validation
- Compare prompt template means
- Compare temperature means
- Flag high-variance coefficients

## Cost Estimation

| Iterations | API Calls | Estimated Cost* |
|------------|-----------|-----------------|
| 30 per coef | 360 | ~$0.50 |
| 100 per coef | 1,200 | ~$1.50 |
| 1000 per coef | 12,000 | ~$15.00 |

*Using Claude Sonnet, approximate pricing

## Citation

If you use this methodology, please cite:

```bibtex
@article{fehr2026complementarity,
  title={Complementarity and Context: A Unified Framework for Economic Rationality},
  author={Fehr, Gerhard and others},
  journal={Working Paper},
  year={2026},
  note={Appendix AN: LLM Monte Carlo Methodology}
}
```

## License

MIT License - FehrAdvice & Partners AG / University of Zurich
