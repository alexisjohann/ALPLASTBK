# The Complementarity Between Trust and Contract Enforcement

**Authors:** Björn Bartling, Ernst Fehr, David Huffman, Nick Netzer
**Date:** March 18, 2025
**Journal:** Economic Journal (Accepted for Publication)
**Paper-ID:** PAP-bartling2025complementarity
**Archived:** 2026-02-03

---

## Abstract

We study the complementarity between trust and contract enforcement in a principal-agent experiment. Our design manipulates both the level of trust (via information about the agent's type) and the availability of contract enforcement (via minimum effort requirements). We find that trust and enforcement are complements: the effect of trust on effort is significantly larger when enforcement is available. This complementarity arises because enforcement reduces the risk of trusting, making principals more willing to offer generous wages, which in turn elicits higher effort from agents. Our findings have implications for the design of institutions that combine formal enforcement with informal trust-based mechanisms.

---

## 1. Introduction

Trust and contract enforcement are two fundamental mechanisms that facilitate economic exchange. Trust enables cooperation without formal safeguards, while contract enforcement provides legal backing for agreements. A central question in institutional economics is how these mechanisms interact.

**Two competing views:**

1. **Substitutes View:** Trust and enforcement are substitutes - formal contracts "crowd out" trust
2. **Complements View:** Trust and enforcement reinforce each other - enforcement reduces the risk of trusting

This paper provides experimental evidence that **trust and enforcement are complements**.

### Key Finding

> "The effect of trust on effort is significantly larger when contract enforcement is available than when it is not. This positive interaction effect - the hallmark of complementarity - suggests that institutions should combine formal and informal mechanisms rather than rely on one or the other."

---

## 2. Experimental Design

### 2.1 Basic Setup

- **Subjects:** N = 1,152 (576 buyer-seller pairs)
- **Location:** University of Zurich Decision Science Laboratory
- **Design:** 2×2 factorial (Trust × Enforcement)

### 2.2 The Trading Game

**Stage 1 (Buyer):**
- Buyer offers wage w ∈ [0, 100]
- Buyer chooses minimum effort requirement ē ∈ {0, 1, ..., 10} (if enforcement available)

**Stage 2 (Seller):**
- Seller chooses effort e ∈ {0, 1, ..., 10}
- If enforcement: e ≥ ē required

**Payoffs:**
```
Buyer:  π_B = 10e - w
Seller: π_S = w - c(e)   where c(e) = e²/2
```

### 2.3 Treatment Conditions

| Treatment | Trust Signal | Enforcement Available |
|-----------|--------------|----------------------|
| **Baseline** | None | No |
| **Trust Only** | "Partner rated as highly trustworthy" | No |
| **Enforcement Only** | None | Yes (can set ē > 0) |
| **Trust + Enforcement** | "Partner rated as highly trustworthy" | Yes |

### 2.4 Trust Manipulation

Trust signal based on seller's response to hypothetical trust game:
- High trust: "Your partner returned 50% of tripled amount in trust game"
- This provides credible information about partner's cooperativeness

---

## 3. Theoretical Framework

### 3.1 Model Setup

Seller utility includes fairness concerns:
```
U_S = π_S - α·max{π_B - π_S, 0} - β·max{π_S - π_B, 0}
```

Where:
- α = disadvantageous inequity aversion
- β = advantageous inequity aversion

### 3.2 Equilibrium Analysis

**Proposition 1 (Effort Response to Trust):**
Higher trust (lower perceived α of buyer) leads to higher effort for any given wage.

**Proposition 2 (Complementarity):**
The effect of trust on effort is larger when enforcement is available:
```
∂²e*/∂Trust·∂Enforcement > 0
```

**Intuition:**
- Enforcement reduces downside risk of generous wage offers
- Lower risk → buyers offer higher wages
- Higher wages + trust → sellers exert more effort
- Complementarity emerges through the wage channel

---

## 4. Main Results

### 4.1 Average Effort by Treatment

| Treatment | Mean Effort | Std. Dev. | N |
|-----------|-------------|-----------|---|
| Baseline | 3.2 | 2.1 | 144 |
| Trust Only | 3.8 | 2.3 | 144 |
| Enforcement Only | 4.4 | 1.9 | 144 |
| Trust + Enforcement | 5.7 | 1.8 | 144 |

### 4.2 Regression Analysis (Table 1)

**Dependent Variable: Effort**

| Variable | (1) | (2) | (3) |
|----------|-----|-----|-----|
| Trust | 0.6** | - | 0.6** |
| | (0.24) | | (0.24) |
| Enforcement | - | 1.2*** | 1.2*** |
| | | (0.21) | (0.21) |
| **Trust × Enforcement** | - | - | **0.7***** |
| | | | **(0.32)** |
| Constant | 3.2*** | 3.2*** | 3.2*** |
| | (0.17) | (0.17) | (0.17) |
| R² | 0.04 | 0.12 | 0.18 |
| N | 576 | 576 | 576 |

*Note: * p<0.10, ** p<0.05, *** p<0.01*

### 4.3 Key Finding: Positive Interaction Effect

The interaction coefficient **β = 0.7 (p < 0.05)** confirms complementarity.

**Interpretation:**
- Trust alone: +0.6 effort
- Enforcement alone: +1.2 effort
- Trust + Enforcement: +0.6 + 1.2 + 0.7 = **+2.5 effort**
- The combination yields MORE than the sum of parts

---

## 5. Mechanisms

### 5.1 Wage Channel

Trust affects effort partly through wages:

| Treatment | Mean Wage |
|-----------|-----------|
| Baseline | 32.4 |
| Trust Only | 38.7 |
| Enforcement Only | 41.2 |
| Trust + Enforcement | 52.3 |

**Mediation analysis:** ~40% of trust effect on effort is mediated by higher wages.

### 5.2 Contract Enforcement Usage

When enforcement is available:
- 68% of buyers use it (set ē > 0) when costly
- 89% use it when free
- Average ē when used: 3.2

### 5.3 Effort-Wage Relationship

| Condition | Effort-Wage Slope |
|-----------|-------------------|
| No Enforcement | 0.024*** |
| With Enforcement | 0.031*** |

The steeper slope with enforcement suggests reciprocity is stronger when backed by formal mechanisms.

---

## 6. Welfare Analysis

### 6.1 Total Surplus by Treatment

| Treatment | Total Surplus | % vs Baseline |
|-----------|---------------|---------------|
| Baseline | 24.8 | - |
| Trust Only | 26.8 | +8% |
| Enforcement Only | 27.5 | +11% |
| Trust + Enforcement | 30.5 | **+23%** |

### 6.2 Superadditivity Test

**If substitutes:** Combined effect ≤ sum of individual effects
**If complements:** Combined effect > sum of individual effects

```
Observed: 23% > 8% + 11% = 19%
→ COMPLEMENTS confirmed
```

### 6.3 Efficiency

| Treatment | % First-Best Effort |
|-----------|---------------------|
| Baseline | 32% |
| Trust Only | 38% |
| Enforcement Only | 44% |
| Trust + Enforcement | 57% |

---

## 7. Discussion and Implications

### 7.1 Theoretical Implications

1. **Crowding-out is not inevitable:** Formal enforcement need not undermine trust
2. **Complementarity mechanism:** Enforcement reduces risk → more trust investment
3. **Institutional design:** Optimal institutions combine formal and informal mechanisms

### 7.2 Policy Implications

> "Our results suggest that policymakers should not view trust-building and enforcement as alternative approaches. Instead, they should design institutions that leverage both mechanisms, recognizing their complementary nature."

### 7.3 Limitations

- Laboratory setting (external validity)
- One-shot interactions (no reputation effects)
- Specific trust manipulation (may not generalize)

---

## Key Parameters Extracted (EBF Integration)

| Parameter | Symbol | Value | Source |
|-----------|--------|-------|--------|
| Trust-Enforcement Complementarity | γ(T,E) | +0.7 | Interaction coefficient |
| Trust Effect (No Enforcement) | Δe_T0 | +0.6 | Table 1 |
| Trust Effect (With Enforcement) | Δe_T1 | +1.3 | Derived |
| Enforcement Effect | Δe_E | +1.2 | Table 1 |
| Effort-Wage Slope (No Enf.) | β_0 | 0.024 | Table 2 |
| Effort-Wage Slope (With Enf.) | β_1 | 0.031 | Table 2 |
| Welfare Gain (Combined) | ΔW | +23% | Table 4 |
| Superadditivity | S | +4pp | 23% - 19% |

---

## EBF Framework Relevance

This paper provides **direct experimental evidence** for the core EBF assumption that interventions can be complements.

| Bartling et al. Concept | EBF Application |
|-------------------------|-----------------|
| Trust signal | Soft intervention (values, communication) |
| Contract enforcement | Hard intervention (rules, policies) |
| Complementarity γ > 0 | Portfolio optimization with positive γ-matrix |
| Superadditivity | Combined interventions > sum of parts |
| Welfare maximization | Efficiency frontier in intervention space |

### SPÖ Strategy Implication

> For political intervention portfolios: Combining trust-building communication (Werte-Appell, Ordnung-Frame) with concrete policy proposals (institutional reform, enforcement mechanisms) should yield HIGHER impact than either approach alone.

**Empirical basis:** γ(Soft, Hard) ≈ +0.7 (from this paper)

---

## Online Appendix Summary

### A. Theoretical Proofs
- Proposition 1: Trust → Effort (monotonic)
- Proposition 2: Complementarity condition derived
- Proposition 3: Wage mediation mechanism

### B. Additional Tables
- Table A1: Balance tests across treatments
- Table A2: Robustness to clustering
- Table A3: Heterogeneity by subject characteristics
- Table A4: Learning effects across rounds

### C. Experimental Instructions
- Full buyer instructions (German original + English translation)
- Full seller instructions
- Trust elicitation procedure

---

*Full text archived for EBF Framework reference*
*Content Level: L3 (complete)*
*Evidence Tier: 1 (Top journal, RCT design)*
*Original: Economic Journal (2025), accepted for publication*
