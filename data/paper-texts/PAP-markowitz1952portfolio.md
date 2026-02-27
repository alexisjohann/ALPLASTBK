# Portfolio Selection

**Author:** Harry Markowitz
**Date:** March 1952
**Journal:** The Journal of Finance, Vol. VII, No. 1, pp. 77-91
**Paper-ID:** PAP-markowitz1952portfolio
**Archived:** 2026-02-03

---

## Abstract

The process of selecting a portfolio may be divided into two stages. The first stage starts with observation and experience and ends with beliefs about the future performances of available securities. The second stage starts with the relevant beliefs about future performances and ends with the choice of portfolio. This paper is concerned with the second stage.

---

## The E-V Rule

The E-V maxim states that the investor would (or should) want to select one of those portfolios which give rise to the (E,V) combinations indicated as efficient in Figure 1, i.e., those with minimum V for given E or more and maximum E for given V or less.

**Key Insight:**
> "Diversification cannot eliminate all variance... the portfolio with maximum expected return is not necessarily the one with minimum variance."

---

## Mathematical Formulation

### Expected Return

Let:
- R_i = anticipated return from security i
- X_i = percentage of portfolio invested in security i

Expected return of portfolio:
```
E = Σᵢ Xᵢ Rᵢ
```

### Variance of Return

Let:
- σᵢⱼ = covariance between returns of securities i and j
- σᵢᵢ = σᵢ² = variance of security i

Variance of portfolio:
```
V = Σᵢ Σⱼ σᵢⱼ Xᵢ Xⱼ
```

### Constraints

```
Σᵢ Xᵢ = 1        (Budget constraint)
Xᵢ ≥ 0           (No short selling)
```

---

## The Efficient Frontier

The set of (E, V) pairs from which the investor can choose is called the **attainable set**. The subset of this set which is **efficient** consists of:
- Portfolios with minimum V for given E or more
- Portfolios with maximum E for given V or less

**Geometric Interpretation:**
The efficient set forms a curve (the "efficient frontier") in E-V space, connecting the minimum variance portfolio to the maximum return portfolio.

---

## Diversification

**Key Finding:**
> "Diversification is both observed and sensible; a rule of behavior which does not imply the superiority of diversification must be rejected both as a hypothesis and as a maxim."

### Why Diversification Works

If we invest equal amounts (1/N) in N securities:

```
V = (1/N)² Σᵢ Σⱼ σᵢⱼ
  = (1/N) × (average variance) + ((N-1)/N) × (average covariance)
```

As N → ∞:
```
V → average covariance
```

**Implication:** Portfolio variance cannot be reduced below the average covariance, no matter how many securities are held.

---

## The Law of Large Numbers Not Applicable

**Critical Insight:**
> "The law of large numbers will not be valid for portfolio diversification when correlation coefficients are generally positive."

This is because financial assets are generally positively correlated (market risk), so the standard actuarial principle of risk pooling does not fully apply.

---

## Expected Returns vs. Anticipated Returns

Markowitz distinguishes between:
- **Anticipated Returns:** Subjective beliefs about future returns
- **Expected Returns:** Probability-weighted average of possible outcomes

The E-V rule works with anticipated returns, acknowledging that:
> "We, or our statistician, may be able to make use of a wealth of information about the historical behavior of securities. We cannot... make use of beliefs which are as definite as these."

---

## Three-Security Example

For illustration, consider 3 securities with:
- Expected returns: μ₁ = 0.058, μ₂ = 0.080, μ₃ = 0.162
- Variances: σ₁² = 0.0146, σ₂² = 0.0293, σ₃² = 0.1225
- Covariances: σ₁₂ = 0.0187, σ₁₃ = 0.0145, σ₂₃ = 0.0104

The efficient frontier in this case connects:
- Minimum variance portfolio (X₁=0.56, X₂=0.44, X₃=0)
- Maximum return portfolio (X₁=0, X₂=0, X₃=1)

---

## Computational Method

The problem of finding efficient portfolios can be solved through:

1. **Parametric Quadratic Programming:**
   ```
   minimize V = X'ΣX
   subject to E = μ'X ≥ E₀
              1'X = 1
              X ≥ 0
   ```

2. **Critical Line Algorithm:**
   Markowitz developed a method to trace the entire efficient frontier by identifying "corner portfolios" where the set of securities held changes.

---

## Key Parameters Extracted

| Parameter | Symbol | Value/Formula | Source |
|-----------|--------|---------------|--------|
| Portfolio Expected Return | E | Σᵢ Xᵢ μᵢ | Eq. (1) |
| Portfolio Variance | V | Σᵢ Σⱼ Xᵢ Xⱼ σᵢⱼ | Eq. (2) |
| Diversification Limit | V_min | Average covariance as N→∞ | Section V |
| Efficient Criterion | E-V | Min V for given E, Max E for given V | Definition |

---

## Implications for Behavioral Economics

The E-V framework has profound implications:

1. **Bounded Rationality:** Computing efficient portfolios requires knowing all μᵢ and σᵢⱼ - an enormous information burden

2. **Loss Aversion Connection:** Variance captures both upside and downside - later work (Prospect Theory) would distinguish these

3. **Systematic vs. Idiosyncratic Risk:** Diversification only eliminates idiosyncratic risk; market-wide (systematic) risk persists

---

## EBF Relevance

This foundational paper establishes principles directly applicable to intervention portfolio design:

| Markowitz Concept | EBF Application |
|-------------------|-----------------|
| Expected Return E | Expected intervention impact (pp) |
| Variance V | Variance of impact across segments |
| Efficient Frontier | Optimal intervention portfolios |
| Diversification | Combining uncorrelated interventions |
| Covariance σᵢⱼ | Complementarity γᵢⱼ between interventions |
| Budget Constraint | Resource allocation constraint |

**Key Insight for SPÖ:**
> The E-V rule shows that "putting all eggs in one basket" (single intervention) is suboptimal unless that intervention dominates all others in both expected return AND variance.

---

## Historical Significance

- **1952:** Paper published in Journal of Finance
- **1959:** Book-length treatment in "Portfolio Selection: Efficient Diversification of Investments"
- **1990:** Nobel Prize in Economics (shared with Merton Miller and William Sharpe)

> "It was Markowitz's great insight to formulate the choice of an investment portfolio as an optimization problem that trades off multiple objectives."
> — Boyd et al. (2024)

---

*Full text archived for EBF Framework reference*
*Content Level: L3 (complete)*
*Original: The Journal of Finance, Vol. VII, No. 1, March 1952*
