# HMWM Sensitivity Analysis Results

**Model:** HMWM v3.3
**Simulations:** 10,000
**Date:** 2026-01-29

---

## 1. Confidence Intervals (95% CI)

| Outcome | Mean | 95% CI | Interpretation |
|---------|------|--------|----------------|
| `delta_U_total` | 0.0827 | [0.0111, 0.1910] | Overall welfare effect of migration |
| `delta_U_perceived` | 0.0495 | [0.0054, 0.1368] | Perceived welfare effect (with narrative distortion) |
| `perception_gap` | 0.0332 | [0.0026, 0.1024] | Gap between reality and perception |
| `fiscal_per_migrant` | 16489.8572 | [15000.0000, 19661.2835] | Net fiscal impact per migrant (CHF) |
| `welfare_cut_cost` | -12074.3923 | [-19936.5494, -5000.0000] | Cost of welfare cuts (CHF, negative = loss) |
| `years_to_adjustment` | 4.4667 | [2.4485, 10.0000] | Years for full labor market adjustment |

---

## 2. Parameter Sensitivity (Variance Contribution)

### 2.1 Drivers of Total Welfare Effect (ΔU_total)

| Rank | Parameter | Sensitivity | Direction | Source |
|------|-----------|-------------|-----------|--------|
| 1 | `beta_language` | 0.036 | positive | Foged 2024 (RDD) |
| 2 | `gamma_wage_high` | 0.007 | positive | Beerli 2021 |
| 3 | `beta_early_intervention` | 0.006 | positive | Dahlberg 2024 (RCT) |
| 4 | `gamma_wage_low` | 0.004 | positive | Caiumi & Peri 2024 (+1.7% to +2.6%) |
| 5 | `gamma_complementarity` | 0.004 | positive | Caiumi & Peri 2024 (σ=14) |

**Total variance explained:** 5.7%

### 2.2 Drivers of Perception Gap

| Rank | Parameter | Sensitivity | Direction |
|------|-----------|-------------|-----------|
| 1 | `beta_narrative` | 0.177 | negative |
| 2 | `beta_language` | 0.027 | positive |
| 3 | `gamma_wage_high` | 0.005 | positive |
| 4 | `beta_early_intervention` | 0.004 | positive |
| 5 | `gamma_wage_low` | 0.003 | positive |

---

## 3. Key Findings

### 3.1 Robustness Check

✅ **Migration effect is POSITIVE** in >97.5% of simulations

- Mean effect: 0.0827
- 95% CI: [0.0111, 0.1910]

### 3.2 Main Driver

**`beta_language`** explains 3.6% of outcome variance
- Description: Language training employment effect
- Source: Foged 2024 (RDD)

---

## 4. Policy Implications

Based on sensitivity analysis:

1. **Most leverage:** Focus on parameters with highest sensitivity
2. **Robust conclusions:** Findings hold across parameter uncertainty
3. **Key uncertainties:** Where more research is needed

