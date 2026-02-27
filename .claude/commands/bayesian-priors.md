# /bayesian-priors - Bayesian Prior Generation from Paper Robustness

Generiere Bayesian Priors für 10C Parameter (γ, A, W, Ψ) gewichtet nach Paper Robustness Scores.

Dies ist der **standardisierte Workflow** zur Generierung von prior distributions für Modelltraining (Appendix METHOD-PRIORS).

## Verwendung

```
/bayesian-priors                    # Generiere Priors mit Standard-Settings
/bayesian-priors --force            # Regeneriere (auch wenn bereits vorhanden)
/bayesian-priors --threshold 75     # Benutzerdef. Robustness-Schwelle (default: 70%)
/bayesian-priors --output <dir>     # Output-Verzeichnis angeben
```

---

## Was der Workflow macht

```
┌─────────────────────────────────────────────────────────────┐
│  BAYESIAN PRIOR GENERATION                                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Load Paper Robustness Metrics                           │
│     → Laden aller 11 Papers mit Robustness-Scores            │
│     → Clarity (Effektgröße) + Uncertainty (LLMMC)            │
│                                                             │
│  2. Weight by Robustness                                    │
│     → >85%: weight = 1.0 (full weight)                       │
│     → 70-85%: weight = scaled (0.3 to 1.0)                   │
│     → <70%: weight = 0.0 (excluded from priors)              │
│                                                             │
│  3. Domain-Stage Aggregation                                │
│     → Gruppiere Papers nach Domain × BCJ Stage              │
│     → Weighted averaging: μ = Σ(value_i × w_i) / Σ(w_i)      │
│     → Uncertainty scaling: σ = base_σ × (1 + robustness_adj) │
│                                                             │
│  4. Generate Prior Distributions                            │
│     → γ (Complementarity) ~ N(μ_γ, σ_γ)                      │
│     → A (Awareness) ~ N(μ_A, σ_A)                            │
│     → W (Willingness) ~ N(μ_W, σ_W)                          │
│     → Ψ (Context) ~ Categorical distribution                 │
│                                                             │
│  5. Output Generation                                       │
│     → Markdown: Human-readable with 95% confidence intervals │
│     → YAML: Machine-ready for model initialization           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Weighting Strategy

Die Robustness-Scores kommen aus:

**Clarity Score (40% Gewicht):**
- Effect Size Classification: Clear (>1.0), Ambiguous (0.5-1.0), Weak (<0.5)
- Citation count adjustment: Häufig zitiert = höhere Klarheit

**Confidence Level (60% Gewicht):**
- Parameter uncertainty quantification (LLMMC approach)
- Publication adjustment für Sample Size & Replication

**Final Weighting:**

| Robustness | Gewicht | Interpretation |
|------------|---------|-----------------|
| >85% | 1.0 | Full weight - highly robust |
| 80-85% | 0.9 | Strong weight |
| 75-80% | 0.7 | Moderate weight |
| 70-75% | 0.5 | Partial weight |
| <70% | 0.0 | Excluded - insufficient robustness |

---

## Example Output

### High-Robustness Priors (>85%)

**Finance × Contemplation**
- Papers: kahneman1979prospect (100%)
- γ ∼ N(0.50, 0.063) → 95% CI: [0.377, 0.623]
- A ∼ N(0.60, 0.084) → 95% CI: [0.435, 0.765]
- W ∼ N(0.50, 0.076) → 95% CI: [0.351, 0.649]
- Ψ: framing (100%)

**Finance × Preparation**
- Papers: thaler1985mental (87%)
- γ ∼ N(0.40, 0.122) → 95% CI: [0.161, 0.639]
- A ∼ N(0.50, 0.164) → 95% CI: [0.179, 0.821]
- W ∼ N(0.60, 0.147) → 95% CI: [0.312, 0.888]
- Ψ: cognitive_framing (100%)

---

## Inputs & Prerequisites

**Erforderliche Dateien:**
- `data/paper-sources.yaml` - 11 Papers mit Pre-Extracted 10C Coordinates
- `scripts/validate_paper_robustness.py` - Robustness Metrics Calculator

**Paper-Quellen (11 total):**
- kahneman1979prospect (Prospect Theory) - 100% robust ✅
- thaler1985mental (Mental Accounting) - 87% robust ✅
- thaler2015choice (Choice Architecture) - 77% caution ⚠️
- fehr1998reciprocity (Reciprocity) - 73% caution ⚠️
- cialdini2006influence (Influence) - 74% caution ⚠️
- johnson2003thepower (Defaults) - 69% replication ❌
- madrian2001power (401k Defaults) - 60% replication ❌
- dellavigna2009paying (Gym Membership) - 60% replication ❌
- kube2012efficiency (Workplace Reciprocity) - 66% replication ❌
- hoff2011whither (Identity Effects) - 62% replication ❌
- allcott2011social (Social Norms) - 47% replication ❌

---

## Output Formats

### Markdown Report

**Datei:** `outputs/bayesian-priors/YYYY-MM-DD_priors.md`

```markdown
# Bayesian Priors Report - 2026-01-14

## Executive Summary
- Total Domain-Stage Combinations: 4
- Average Robustness: 84.3%
- Parameters: γ, A, W, Ψ

## Priors by Domain-Stage

### Finance - Contemplation
**Robustness**: 100% | **Papers**: 1

**γ (Complementarity)**
- Mean: 0.500
- σ: 0.063
- 95% CI: [0.377, 0.623]

**Contributing Papers**: kahneman1979prospect
```

### YAML Format

**Datei:** `outputs/bayesian-priors/bayesian_priors.yaml`

```yaml
bayesian_priors:
  finance:contemplation:
    domain: finance
    stage: contemplation
    robustness: 100.0
    n_papers: 1
    gamma:
      mean: 0.5
      std: 0.063
      lower: 0.0
      upper: 1.0
    A_level:
      mean: 0.6
      std: 0.084
      lower: 0.0
      upper: 1.0
    W_level:
      mean: 0.5
      std: 0.076
      lower: 0.0
      upper: 1.0
    psi_dominant:
      framing: 1.0
    contributing_papers:
      - kahneman1979prospect
```

---

## Integration with Model Training

Die YAML-Datei kann direkt für Bayesian Model Initialization verwendet werden:

```python
import yaml

with open('outputs/bayesian-priors/bayesian_priors.yaml', 'r') as f:
    priors = yaml.safe_load(f)

# Use for domain-stage specific prior initialization
for domain_stage, prior in priors['bayesian_priors'].items():
    gamma_mean = prior['gamma']['mean']
    gamma_std = prior['gamma']['std']
    # Initialize model with priors
```

---

## Implementation Details

| Datei | Zweck |
|-------|-------|
| `scripts/generate_bayesian_priors.py` | End-to-End Prior Generation |
| `scripts/validate_paper_robustness.py` | Robustness Metrics Calculation |
| `data/paper-sources.yaml` | Paper Database with 10C Coordinates |

**Script Flow:**
1. Load paper-sources.yaml (11 papers)
2. Calculate clarity score from effect sizes
3. Quantify parameter uncertainty (LLMMC)
4. Weight each paper by robustness_score
5. Aggregate by domain-stage combinations
6. Generate Markdown + YAML outputs

---

## Quality Metrics

**Coverage Analysis:**
- 4 Domain-Stage combinations with sufficient robustness
- 2 papers >85% robustness (full weight)
- 3 papers 70-85% robustness (partial weight)
- 6 papers <70% robustness (excluded)

**Parameter Distributions:**
- γ (Complementarity): Weighted by paper effect sizes on behavioral interactions
- A (Awareness): Clarity of barriers in each domain-stage
- W (Willingness): Action readiness given context
- Ψ (Context): Categorical distribution of dominant context types

---

## Fehlerbehandlung

Wenn Script fehlschlägt:

```bash
# Check dependencies
python -c "import scipy, numpy, yaml; print('OK')"

# Validate paper-sources.yaml format
python -c "import yaml; yaml.safe_load(open('data/paper-sources.yaml'))"

# Run with verbose logging
python scripts/generate_bayesian_priors.py --verbose
```

---

## Referenzen

- **Appendix METHOD-PRIORS:** Bayesian Prior Theory & Implementation
- **Appendix METHOD-ROBUSTNESS:** Paper Robustness Validation Framework
- **Papers:** data/paper-sources.yaml (11 seminal behavioral econ papers)
- **Validierung:** scripts/validate_paper_robustness.py

---

## Beispiel Workflow

```bash
# 1. Generate Bayesian priors
/bayesian-priors

# 2. Check outputs
cat outputs/bayesian-priors/2026-01-14_priors.md

# 3. Use in model training
python -c "
import yaml
with open('outputs/bayesian-priors/bayesian_priors.yaml') as f:
    priors = yaml.safe_load(f)
print('Loaded', len(priors['bayesian_priors']), 'domain-stage prior combinations')
"
```

---

**Version:** 1.0 | **Status:** Produktiv | **Letzte Ausführung:** 2026-01-14
