# Markowitz Portfolio Construction at Seventy

**Authors:** Stephen Boyd, Kasper Johansson, Ronald Kahn, Philipp Schiele, Thomas Schmelzer
**Date:** January 5, 2024
**Paper-ID:** PAP-boyd2024markowitz70
**Archived:** 2026-02-03

---

## Abstract

More than seventy years ago Harry Markowitz formulated portfolio construction as an optimization problem that trades off expected return and risk, defined as the standard deviation of the portfolio returns. Since then the method has been extended to include many practical constraints and objective terms, such as transaction cost or leverage limits. Despite several criticisms of Markowitz's method, for example its sensitivity to poor forecasts of the return statistics, it has become the dominant quantitative method for portfolio construction in practice. In this article we describe an extension of Markowitz's method that addresses many practical effects and gracefully handles the uncertainty inherent in return statistics forecasting. Like Markowitz's original formulation, the extension is also a convex optimization problem, which can be solved with high reliability and speed.

---

## Contents

1. Introduction
   1.1 The original Markowitz idea
   1.2 Alleged deficiencies
   1.3 Robust optimization and regularization
   1.4 Convex optimization
   1.5 Previous work
   1.6 This paper

2. Portfolio holdings and trades
   2.1 Portfolio weights
   2.2 Holding constraints and costs
   2.3 Trades
   2.4 Trading constraints and costs

3. Return and risk forecasts
   3.1 Return
   3.2 Probabilistic asset return model
   3.3 Factor model
   3.4 Return and risk forecasts
   3.5 Making return and risk forecasts robust

4. Convex optimization formulation
   4.1 Markowitz problem
   4.2 Softening constraints
   4.3 Nonconvex constraints and objectives
   4.4 Back-testing and parameter tuning

5. Numerical experiments
   5.1 Data and back-tests
   5.2 Taming Markowitz
   5.3 Markowitz++
   5.4 Parameter tuning
   5.5 Annual performance
   5.6 Scaling

6. Conclusions

---

## 1. Introduction

Harry Markowitz's 1952 paper Portfolio Selection was a true breakthrough in our understanding of and approach to investing. Before Markowitz there was (almost) no mathematical approach to investing. As a 25-year-old graduate student, Markowitz founded modern portfolio theory, and methods inspired by him would become the most widely used portfolio construction practices over the next 70 years (and counting).

### 1.1 The original Markowitz idea

Markowitz identified two steps in the portfolio selection process:
1. Form beliefs about expected returns (μ) and covariances (Σ)
2. Optimize portfolio based on these quantities

The E-V rule states that an investor desires to achieve maximum expected return while keeping variance below a given threshold:

```
maximize μᵀw
subject to wᵀΣw ≤ (σᵗᵃʳ)²
         1ᵀw = 1
```

Alternative formulation (risk-adjusted return):

```
maximize μᵀw - γwᵀΣw
subject to 1ᵀw = 1
```

where γ is the risk-aversion parameter.

### 1.2 Alleged deficiencies

**Criticism 1: Sensitive to data errors**
- Well documented sensitivity to input data
- Inverse covariance appears in analytical solutions
- Can be addressed using regularization and robust optimization

**Criticism 2: Risk symmetry assumption**
- Variance treats above-mean returns same as below-mean
- In practice, with appropriate parameters, this is not a problem

**Criticism 3: Expected utility maximization**
- Quadratic utility not always increasing
- Actually does maximize expected utility for exponential utility with Gaussian returns

**Criticism 4: Only first two moments**
- Mean-variance ignores skewness, kurtosis
- Empirically, higher moments don't improve performance

**Criticism 5: Greedy (single-period) method**
- Markowitz is myopic, not stochastic control
- But: single-period methods perform nearly as well as full stochastic control

### 1.3 Robust optimization and regularization

**Key insight:** Modify optimization to handle parameter uncertainty

Methods:
- **Robust optimization:** Optimize for worst-case parameter values
- **Regularization:** Add penalty terms to prevent extreme solutions
- Long-only constraint acts as regularization
- Black-Litterman regularizes toward market implied return
- Shrinkage for covariance estimation

### 1.4 Convex optimization

Modern advances:
- Cone programs generalize linear programming
- Reliable solvers: MOSEK, GUROBI, ECOS, Clarabel, SCS
- Domain-specific languages: CVXPY, CVX, Convex.jl

---

## 2. Portfolio Holdings and Trades

### 2.1 Portfolio weights

- Asset weights: w = (w₁, ..., wₙ) ∈ ℝⁿ
- Cash weight: c
- Budget constraint: 1ᵀw + c = 1
- Leverage: L = ||w||₁

### 2.2 Holding constraints and costs

**Weight limits:** wᵐⁱⁿ ≤ w ≤ wᵐᵃˣ

**Leverage limit:** L ≤ Lᵗᵃʳ

**Holding cost:**
```
φʰᵒˡᵈ(w,c) = (κˢʰᵒʳᵗ)ᵀ(-w)₊ + κᵇᵒʳʳᵒʷ(-c)₊
```

### 2.3 Trades

Trade vector: z = w - wᵖʳᵉ
Turnover: T = ½||z||₁

### 2.4 Trading constraints and costs

**Trade limits:** zᵐⁱⁿ ≤ z ≤ zᵐᵃˣ
**Turnover limit:** T ≤ Tᵗᵃʳ

**Trading cost (with market impact):**
```
φᵗʳᵃᵈᵉ(z) = (κˢᵖʳᵉᵃᵈ)ᵀ|z| + (κⁱᵐᵖᵃᶜᵗ)ᵀ|z|^(3/2)
```

---

## 3. Return and Risk Forecasts

### 3.2 Probabilistic asset return model

Model: r ~ (μ, Σ)

Expected return: R̄ = μᵀw + rʳᶠc
Risk (std dev): σ = √(wᵀΣw)

### 3.3 Factor model

```
r = Ff + ε
```

Where:
- F ∈ ℝⁿˣᵏ: factor loading matrix
- f ∈ ℝᵏ: factor returns
- ε ∈ ℝⁿ: idiosyncratic return

Covariance: Σ = FΣᶠFᵀ + D (low rank + diagonal)

**Computational advantage:** O(nk²) instead of O(n³)

### 3.5 Making forecasts robust

**Robust return forecast:**
```
Rʷᶜ = R̄ - ρᵀ|w|
```

Where ρ is the uncertainty radius for each asset return.

**Robust covariance forecast:**
```
(σʷᶜ)² = σ² + ϱ(Σ Σᵢᵢ^(1/2)|wᵢ|)²
```

Where ϱ ∈ [0,1) defines uncertainty level.

---

## 4. Convex Optimization Formulation

### 4.1 The Markowitz++ Problem

```
maximize  Rʷᶜ - γʰᵒˡᵈφʰᵒˡᵈ(w) - γᵗʳᵃᵈᵉφᵗʳᵃᵈᵉ(z)

subject to  1ᵀw + c = 1, z = w - wᵖʳᵉ
            wᵐⁱⁿ ≤ w ≤ wᵐᵃˣ, L ≤ Lᵗᵃʳ
            cᵐⁱⁿ ≤ c ≤ cᵐᵃˣ
            zᵐⁱⁿ ≤ z ≤ zᵐᵃˣ, T ≤ Tᵗᵃʳ
            σʷᶜ ≤ σᵗᵃʳ
```

### 4.2 Softening constraints

Replace hard constraints with penalties:
```
γ(f - fᵐᵃˣ)₊
```

**Benefits:**
- Always feasible (z=0 is always valid)
- Avoids excessive trading to satisfy marginal violations
- Handles infeasibility gracefully

### 4.4 Back-testing and parameter tuning

**Parameter search:** Cyclic method
- Increase/decrease each parameter by ~20%
- Keep if performance improves
- Continue until no improvement

---

## 5. Numerical Experiments

### Key Results (Table 1)

| Method | Return | Volatility | Sharpe | Turnover | Leverage | Drawdown |
|--------|--------|------------|--------|----------|----------|----------|
| Equal weight | 14.1% | 20.1% | 0.66 | 1.2 | 1.0 | 50.5% |
| Basic Markowitz | 3.7% | 14.5% | 0.19 | 1145.2 | 9.3 | 78.9% |
| Weight-limited | 20.2% | 11.5% | 1.69 | 638.4 | 5.1 | 30.0% |
| Leverage-limited | 22.9% | 11.9% | 1.86 | 383.6 | 1.6 | 14.9% |
| Turnover-limited | 19.0% | 11.8% | 1.54 | 26.1 | 6.5 | 25.0% |
| Robust | 15.7% | 9.0% | 1.64 | 458.8 | 3.2 | 24.7% |
| **Markowitz++** | **38.6%** | **8.7%** | **4.32** | **28.0** | **1.8** | **7.0%** |
| **Tuned Markowitz++** | **41.8%** | **8.8%** | **4.65** | **38.6** | **1.6** | **6.4%** |

### Key finding:
Adding just ONE reasonable constraint dramatically improves performance.
All constraints together (Markowitz++) gives best results.

### 5.6 Scaling

| Assets n | Factors k | Solve time (s) |
|----------|-----------|----------------|
| 100 | 10 | 0.01 |
| 500 | 20 | 0.07 |
| 2,000 | 100 | 0.22 |
| 10,000 | 100 | 0.89 |
| 50,000 | 500 | 17.77 |

Empirical scaling: O(n^0.79 × k^1.72) ≈ O(nk²)

---

## 6. Conclusions

> "It was Markowitz's great insight to formulate the choice of an investment portfolio as an optimization problem that trades off multiple objectives."

Key contributions:
1. Markowitz's core idea remains valid after 70 years
2. Modern convex optimization makes extensions practical
3. Regularization/robustification addresses sensitivity criticisms
4. Back-testing enables parameter tuning
5. Problems with 50,000+ assets solvable in seconds

> "The more complex Markowitz++ optimization problem simply realizes his original idea of an optimization-based portfolio construction method that takes multiple objectives into account."

---

## Software

Reference implementation: https://github.com/cvxgrp/markowitz-reference
Production implementation: https://github.com/cvxgrp/cvxmarkowitz

---

## EBF Relevance

This paper directly supports the SPÖ intervention portfolio methodology:

| Boyd et al. Concept | SPÖ Application |
|---------------------|-----------------|
| μ (expected return) | Expected voter impact (pp) |
| σ (risk/volatility) | Variance across segments |
| Constraints (weight, leverage, turnover) | Budget, timing, segment constraints |
| Robust optimization (uncertainty in μ, Σ) | LLMMC estimation uncertainty |
| Soft constraints | Flexible priority handling |
| Factor model | Clustering interventions by correlation |
| Back-testing | A/B testing, historical campaign analysis |

Key insight for SPÖ: **"Adding just one reasonable constraint dramatically improves performance"** - justifies our multi-constraint portfolio approach.

---

*Full text archived for EBF Framework reference*
*Content Level: L3 (complete)*
