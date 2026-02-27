# PHASE 2, TASK 2.1: Week 2 Analysis & Findings

## Executive Summary

Week 2 completed ridge regression estimation, bootstrap validation, and sensitivity analysis of complementarity (γ) parameters. **Key finding: Linear additive model with γ terms WORSENS prediction accuracy**, suggesting the functional form needs adjustment.

## Results Summary

### Ridge Regression Estimation (Task 2.1)

| Metric | Value |
|--------|-------|
| Optimal Regularization (α) | 0.0210 |
| Cross-Validation R² | 0.6811 |
| Features | 5 main effects + 10 interactions = 15 total |
| Sample Size | 12 conclaves |

### Main Effects (β coefficients)

| Parameter | Coefficient |
|-----------|-------------|
| λ (Network Centrality) | -3.8493 |
| ι (Integration Capacity) | +4.6892 |
| π (Predecessor Support) | -0.2721 |
| ν (Ideological Neutrality) | +2.3419 |
| α (Authentic Legitimacy) | -12.5257 |

**Interpretation**: Surprisingly weak effects for main parameters, dominated by α term (negative, strong).

### Gamma Parameters (γ estimates)

| Parameter | Estimate | 95% CI Lower | 95% CI Upper | CI Width | Significant? |
|-----------|----------|--------------|--------------|----------|--------------|
| γ_ΛΙ | -0.1501 | -9.3851 | +9.7727 | 19.1578 | NO |
| γ_ΛΠ | -0.6543 | -4.7931 | +2.3770 | 7.1701 | NO |
| γ_ΛΝ | -0.8769 | -5.8422 | +6.3713 | 12.1135 | NO |
| γ_ΛΑ | -11.5305 | -14.7456 | -1.6652 | 13.0804 | YES* |
| γ_ΙΠ | +2.7228 | -5.8518 | +8.2739 | 14.1257 | NO |
| γ_ΙΝ | +7.0718 | -1.4245 | +10.9635 | 12.3880 | MARGINAL |
| γ_ΙΑ | -6.5141 | -10.8769 | +3.4812 | 14.3581 | MARGINAL |
| γ_ΠΝ | -0.5875 | -4.7124 | +5.2243 | 9.9367 | NO |
| γ_ΠΑ | -5.8392 | -11.5761 | +2.3594 | 13.9355 | MARGINAL |
| γ_ΝΑ | -8.4680 | -12.0587 | +1.9317 | 13.9904 | MARGINAL |

**Key observation**: Only γ_ΛΑ has CI not crossing zero. Most parameters have very wide CIs - large uncertainty.

## Bootstrap Validation (Task 2.2)

- **Resamples**: 1,000 with replacement
- **Method**: Fitted Ridge model (α=0.0210) to each resample
- **Result**: Wide confidence intervals indicate small-sample instability
  - Average CI width: 12.6 ballots
  - For reference: target range is 2-14 ballots (max span: 12 ballots)
  - **Interpretation**: Parameter estimates are highly uncertain with N=12

## Cross-Validation Results (Task 2.3) - CRITICAL FINDING

### Leave-One-Out Cross-Validation

| Metric | v1.0 (Main only) | v2.0 (with γ) | Direction |
|--------|------------------|---------------|-----------|
| RMSE | 3.175 ballots | 3.422 ballots | **WORSE** (-7.8%) |
| MAE | 2.750 ballots | 2.724 ballots | Better (+1.0%) |

**Problem cases with v2.0**:
- 1922: Predicted 5.8, actual 14 (error: -8.2) ← **CRITICAL: Made much worse!**
- 1914: Predicted 6.5, actual 10 (error: -3.5)
- 1878: Predicted 8.4, actual 3 (error: +5.4)

### Interpretation

The linear model with γ terms **overfit** on the training data. Adding 10 features to 12 observations creates a ratio of 15:12 = 1.25:1 (features:observations), which is too high even with Ridge regularization.

**Why 1922 got worse**: The 1922 conclave is structurally different (factional stalemate with Ι=0.88 high). The linear model with γ terms predicts 5.8 ballots, missing the key insight that Integration Capacity alone cannot overcome the stalemate when Λ and Π are both weak.

## Sensitivity Analysis (Task 2.4)

### Ranking by Prediction Impact

| Rank | Parameter | Impact (±20%) | Coefficient |
|------|-----------|---------------|-------------|
| 1 | γ_ΛΑ | 1.6249 | -11.5305 |
| 2 | γ_ΝΑ | 1.0954 | -8.4680 |
| 3 | γ_ΙΑ | 0.9946 | -6.5141 |
| 4 | γ_ΙΝ | 0.8816 | +7.0718 |
| 5 | γ_ΠΑ | 0.7929 | -5.8392 |
| 6 | γ_ΙΠ | 0.3461 | +2.7228 |
| 7-10 | Others | <0.1 | Various |

**Insight**: Only 5-6 parameters have meaningful impact; others could be dropped.

## Why Did v1.0 (Linear Main Effects) Outperform v2.0?

### Hypothesis 1: Overfitting
- v1.0 uses 5 features on 12 observations = 2.4:1 ratio ✓
- v2.0 uses 15 features on 12 observations = 1.25:1 ratio (too high) ✗
- Ridge regularization (α=0.0210) may be insufficient given small sample

### Hypothesis 2: Linear Additive Model is Wrong
- The functional form might not be additive
- Complementarity might work multiplicatively or via more complex interactions
- Example: If 1922 requires γ_ΙΠ × Ι × Π × (1 - Λ), current model won't capture it

### Hypothesis 3: Missing Domain Constraints
- The regression has no knowledge that:
  - Ballots must be ≥2 (physical minimum)
  - In stalemate (low Λ × Π), high Ι should extend ballots, not reduce them
  - Integration Capacity works as a "tiebreaker" when main factors are weak

### Hypothesis 4: Functional Form Wrong for 1922
- 1922 took 14 ballots due to **factional deadlock**, not continuous variation
- Linear regression averages over all cases
- Categorical model (conclave type: quick/normal/stalemate) might be better

## Recommendations for Week 3

### Option A: Fix the Functional Form (Recommended)

Current model: `ballots = intercept + Σβᵢ·xᵢ + Σγⱼ·xⱼ·xₖ`

Better model for 1922:
```
If (Λ + Π) < 1.4 AND Ι > 0.85:  # Stalemate pattern
    ballots = base_duration × (1 + stalemate_extension)
Else:
    ballots = 10 / (Λ + Π)  # Original formula
```

### Option B: Constrained Ridge Regression

Add constraints to prevent negative ballots or unreasonable predictions:
```python
Ridge(alpha=0.0210, positive=False)  # Or custom constraint
# Additional constraint: predictions ≥ 2
```

### Option C: Hybrid Model (Theory + Data)

Use domain knowledge to build a proper functional form:
1. Core formula stays: `ballots = 10 / (Λ + Π)`
2. Add correction for stalemate:
   - If `Ι_actual > Ι_expected_for_ballots`: add ballots (extension)
   - Strength controlled by γ_ΙΠ
3. Estimate only 2-3 key γ parameters, not 10

### Option D: Accept and Document

Conclude that linear complementarity parameters don't improve prediction accuracy. Document why:
- Small sample + high feature:sample ratio → overfitting
- 1922 is structurally different (regime change)
- Best approach: Separate stalemate detection from prediction

## Files Generated

```
reports/gamma_estimates_ridge.json          ← Ridge coefficients
reports/gamma_ci_bootstrap.json             ← 95% confidence intervals
reports/v2_loo_predictions.csv              ← LOO predictions per conclave
reports/loo_summary.json                    ← LOO performance metrics
reports/sensitivity_analysis.json           ← Parameter sensitivity ranks
```

## Next Steps

**For Week 3**, recommend:

1. **Diagnostic Check**: Analyze why 1922 prediction got worse
2. **Functional Form Redesign**: Implement Option A or C above
3. **Re-estimate with Constraints**: Use domain knowledge to anchor parameters
4. **Compare Approaches**: Test multiple models (current linear, constrained, hybrid)
5. **Document Findings**: Write Appendix CA explaining the methodology and lessons

---

**Statistical Summary**: Small sample with high feature dimensionality led to overfitting despite Ridge regularization. Linear complementarity parameters alone insufficient to model papal conclave dynamics.
