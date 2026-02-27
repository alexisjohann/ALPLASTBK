# PAP-brynjolfsson_2013_complementarity - Full Text Archive

**Paper:** Complementarity in Organizations
**Authors:** Erik Brynjolfsson and Paul Milgrom
**Publication:** Handbook of Organizational Economics, Princeton University Press, 2013
**Pages:** 11-55
**Archived Date:** 2026-02-04
**Content Level:** L3 (Full structural characteristics S1-S6 available)

---

## Abstract

Complementarity is an important concept in organizational analysis, because it offers an approach to explaining patterns of organizational practices, how they fit with particular business strategies, and why different organizations choose different patterns and strategies. The formal analysis of complementarity is based on studying the interactions among pairs of interrelated decisions. This chapter develops the mathematical theory of complementarities, presents ten key theorems, and reviews the empirical evidence on complementarities in organizations.

---

## 1. Introduction

According to the American Heritage dictionary, a synergy is "the interaction of two or more agents or forces so that their combined effect is greater than the sum of their individual effects." Complementarity, as used in this chapter, is a near synonym for "synergy," but it is set in a decisionmaking context and defined with mathematical precision.

### Definition of Complementarity

Let Δ₁ and Δ₂ be the increase in profits that would result from changing either alone, and let ΔB be the increase that results from doing both together. The two changes are (weakly) complementary if:

**ΔB ≥ Δ₁ + Δ₂**

regardless of the firm's other choices.

### The Table of Interactions

The paper introduces a prototype for portraying interactions in a system of complements:

| Practice | (1) Tech Changes | (2) Flexible Training | (3) Worker Discretion | (4) Job Protection |
|----------|------------------|----------------------|----------------------|-------------------|
| (1) Make frequent technical changes | | + | + | + |
| (2) Train workers flexibly | | | + | |
| (3) Give workers discretion | | | | + |
| (4) Protect workers' jobs | | | | |
| (*) Frequent upgrade opportunities | + | | | |

A "+" indicates complementary practices.

---

## 2. Theory

### 2.1 Mathematical Foundations

With n binary choices, the decisionmaker's payoff can be denoted by f(x), x ∈ {0,1}ⁿ. The ith and jth choices are (weakly) complementary if for all x:

$$f(1,1,x^{-ij}) - f(0,0,x^{-ij}) \geq [f(1,0,x^{-ij}) - f(0,0,x^{-ij})] + [f(0,1,x^{-ij}) - f(0,0,x^{-ij})]$$

### 2.2 Key Definitions

**Definition (Sublattice):** A set S ⊆ Rⁿ is a sublattice if:
(∀x,y)(x,y ∈ S) ⇒ (x ∨ y, x ∧ y ∈ S)

where x ∨ y is the componentwise maximum and x ∧ y is the componentwise minimum.

**Definition (Supermodular):** A function f: S → R is supermodular if:
(∀x,y ∈ S) f(x ∨ y) + f(x ∧ y) ≥ f(x) + f(y)

**Definition (Complementarities):** The decision problem has complementarities if S is a sublattice and f is supermodular.

---

## 3. Ten Theorems about Complementarities

### Theorem 1a (Topkis 1978)
Complementarity is a pairwise relationship for constraint sets. S ⊆ Rⁿ is a sublattice iff for each pair (i,j), there exist sublattices Sᵢⱼ ⊆ R² such that the constraint decomposes.

### Theorem 1b (Topkis 1978)
Complementarity is a pairwise relationship for objectives. f is supermodular iff it is supermodular in each pair of variables separately.

### Theorem 2 (Topkis 1978)
The set of optimizers is a sublattice. Optimal decisions cluster: they are adopted together or not at all.

### Theorem 3 (Milgrom & Roberts 1995)
"Coherent" searches can find and verify the optimum. More than half of the gain from moving to the optimum can be realized by optimizing over coherent changes (all increased or all decreased).

### Theorem 4 (Topkis 1978)
Comparative statics are like demand theory. If S is a sublattice and f is supermodular, the optimal solution X(θ) is isotone (nondecreasing) in the parameter θ.

### Theorem 5a & 5b (Milgrom & Shannon 1994)
Complementarity conditions are necessary for isotone comparative statics.

### Theorem 6
Limited results extend to modular systems. Even with complex within-module interactions, cross-module complementarity predictions hold.

### Theorem 7 (Milgrom & Roberts 1996)
Long-run changes are larger than short-run changes. The LeChatelier Principle applies to systems of complements.

### Theorem 8 (Milgrom et al. 1991)
Dynamical systems exhibit momentum. Once variables begin moving in a direction, they tend to continue.

### Theorem 9
Complementarities create value to simple coordination. Correlated errors are better than independent errors in systems of complements.

### Theorem 10 (Topkis 1978)
Returns to scale/scope create complementarities. Shared inputs with economies of scale make activities complementary.

---

## 4. Applications and Implications

### 4.1 Organizational Change

Why is organizational change so difficult? Complementarities provide part of the answer:

1. **Coordination Problem:** Multiple actors must coordinate on scope, time, and content of change
2. **Implicit Practices:** Culture and rules of thumb persist despite explicit changes
3. **Timing Difficulties:** Some variables take time, making synchronization difficult

### 4.2 Imitation Difficulties

Firms like Lincoln Electric, Walmart, and Toyota enjoyed sustained high performance. Despite intensive study, competitors could not replicate their success. Complementarities explain why:
- Small errors in matching practices lead to large penalties
- Subtle complementarities make imitation difficult even across plants in the same firm
- Intel's "copy-exactly" policy: replicate every element, including paint color and window orientation

### 4.3 Mergers and Acquisitions

When organizations combine, each brings explicit and implicit methods. Complementarities influence success:
- Cisco Systems employs a "director of culture" who issues "culture badges"
- Recognizes complementarity of culture to other systems

---

## 5. Empirical Evidence

### 5.1 Key Empirical Studies

**Ichniowski et al. (1997):** 36 steel finishing lines
- Practices cluster more than random chance predicts
- Clusters have significant productivity effects
- Isolated changes have little effect

**Bresnahan et al. (2002):** 300 large U.S. firms
- IT + organizational practices + human capital → skill-biased technical change
- Interaction of IT, workplace organization, and human capital predicts productivity

**Black and Lynch (2004):** ~800 establishments
- Productivity correlates with: computers, teams, profit sharing, employee voice, reengineering

### 5.2 Testing for Complementarities

**Performance Test:**
$$\Delta_p \equiv f(1,1) + f(0,0) - f(1,0) - f(0,1)$$

If Δp > 0, reject null hypothesis of no complementarities.

**Correlation Test:**
$$\Delta_c \equiv \text{correlation}(y_1, y_2)$$

Larger Δc provides evidence against null hypothesis.

### 5.3 Unobserved Heterogeneity

Key insight: Unobserved heterogeneity can bias both tests:
- Performance test may be biased downward (reject complementarities when they exist)
- Correlation test may be biased upward (find spurious complementarities)

**Mitigations:**
1. Homogeneous populations (insider econometrics)
2. Panel data with fixed effects
3. Natural experiments
4. Designed experiments

---

## 6. Conclusion

### Implications for Managers

1. **Best Practice Fallacy:** The same practice that works at Lincoln Electric may fail elsewhere
2. **Change Management:** Complementarities create both inertia and momentum
3. **Competitive Strategy:** Tightly coupled systems create entry barriers
4. **M&A Risks:** Organizational capital is fragile
5. **Leadership Role:** Multiple equilibria require coordination

### Research Agenda

1. Applications of existing theory
2. Empirical assessments (especially field experiments)
3. Extensions: learning, evolution, search in complex systems

---

## Key Equations Summary

**Supermodularity:**
$$f(x \vee y) + f(x \wedge y) \geq f(x) + f(y)$$

**Performance Test:**
$$\Delta_p = f(1,1) + f(0,0) - f(1,0) - f(0,1) > 0$$

**Production with Complements (Cobb-Douglas):**
$$\max_{x \geq 0} \lambda x_1^\alpha x_2^\beta - w \cdot x$$

The marginal return to x₁, λαx₁^(α-1)x₂^β - w₁, is increasing in x₂ if α,β > 0.

---

## EBF Integration Notes

### Foundational Relevance for EBF Framework

This paper is **foundational** for the EBF Framework. The entire complementarity concept (γ) derives from this formalization.

### 10C Connection

| 10C | Relevance | Connection |
|-----|-----------|------------|
| **HOW (B)** | Primary | γₖₗ interaction parameters = complementarity |
| **HIERARCHY** | Strong | Theorem 2: optimal decisions cluster |
| **WHEN (V)** | Moderate | Context affects which complements are valuable |
| **WHERE (BBB)** | Strong | Provides mathematical foundation for parameter estimation |

### Key Parameters for EBF

- **γₖₗ:** Interaction strength between choices k and l (directly from Definition)
- **Supermodularity condition:** f(x∨y) + f(x∧y) ≥ f(x) + f(y)
- **Performance test Δp:** Empirical measure of complementarity

### Theory Catalog Mapping

This paper **defines the foundation** for:
- MS-CO-xxx: Coordination theories
- Milgrom & Roberts (1990, 1992, 1995) extensions
- Modern manufacturing literature

### Behavioral Economics Implications

1. **Bounded Rationality:** Theorem 9 shows correlated errors are better than independent errors
2. **Organizational Inertia:** Complementarities explain resistance to change
3. **Path Dependence:** Theorem 8 (momentum) creates historical dependence
4. **Multiple Equilibria:** Systems of complements have multiple local optima

### Empirical Methodology for EBF

The paper provides the standard methodology for testing complementarities:
1. Performance regressions with interaction terms
2. Correlation/clustering analysis
3. Panel data with fixed effects
4. Natural and designed experiments

### Citation: This paper should be cited whenever the EBF Framework uses:
- Complementarity (γ) parameters
- Supermodularity conditions
- Performance vs. correlation tests
- Organizational change analysis
