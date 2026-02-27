# PAP-fehr_2026_gtwh - Full Text Archive

**Paper:** The General Theory of Welfare Hierarchies
**Authors:** Gerhard Fehr and Andrea Fehr
**Institution:** FehrAdvice & Partners AG, Zurich
**Publication:** Working Paper, January 2026
**Archived Date:** 2026-02-04
**Content Level:** L3 (Full structural characteristics S1-S6 available)

---

## Abstract

The economic analysis of welfare has long struggled with the "aggregation problem": how to coherently combine individual utilities into meaningful measures of collective well-being without arbitrary assumptions. This paper introduces the General Theory of Welfare Hierarchies (GTWH), a framework that resolves this challenge through a fundamentally different approach. Rather than externally imposing levels of analysis, GTWH derives them endogenously from two behavioral primitives: shared identity (IDN) and collective utility interdependence (KNU). The result is a recursive, self-similar utility structure where the same mathematical form applies at every level—from individual to household to community to society—differing only in scale parameters. This paper presents the theoretical foundations, derives key propositions about inter-level dynamics, and discusses empirical implications.

---

## 1. Introduction: The Aggregation Problem

### 1.1 The Classical Challenge

Welfare economics has long faced a fundamental challenge: How do we move from individual utilities to collective welfare? Arrow's Impossibility Theorem (1951) demonstrated that no aggregation rule can satisfy seemingly minimal requirements of rationality and fairness. Subsequent work has proposed various solutions—social welfare functions, cost-benefit analysis, Pareto efficiency—but none fully resolves the underlying tension.

The problem is not merely technical. It reflects a deeper conceptual issue: the assumption that "levels" of analysis (individual, household, firm, community, nation) are externally given rather than emergent properties of social organization.

### 1.2 A New Approach

This paper proposes a fundamentally different approach. Rather than asking "How should we aggregate utilities?", we ask: "What behavioral mechanisms create coherent welfare levels in the first place?"

Our answer draws on two well-documented behavioral phenomena:

1. **Shared Identity (IDN)**: People's utility functions incorporate identity-based utility from group membership (Akerlof & Kranton, 2000, 2010)

2. **Collective Utility Interdependence (KNU)**: People care about others' utility, creating feedback loops that generate emergent collective properties (Fehr & Schmidt, 1999; Bolton & Ockenfels, 2000)

When IDN and KNU jointly operate, welfare "levels" emerge endogenously. A household is not just a collection of individuals—it is a level where shared identity and utility interdependence create genuinely new welfare dynamics.

---

## 2. The Model: GTWH Foundations

### 2.1 Level Definition

**Definition 1 (Welfare Level):** A welfare level L_n exists if and only if:
1. Members share sufficient identity: IDN(i,j) > τ_IDN for all i,j ∈ L_n
2. Utility interdependence exceeds threshold: KNU(i,j) > τ_KNU for all i,j ∈ L_n

where τ_IDN and τ_KNU are empirically determined thresholds.

**Proposition 1 (Endogenous Levels):** Under Definition 1, levels emerge from behavioral data rather than being externally imposed. The number of levels N_L is an empirical outcome, not an assumption.

### 2.2 The Recursive Utility Structure

**Definition 2 (Level-n Utility):** For level n, the utility function takes the form:

$$U^{(n)} = \sum_{d \in D} w_d^{(n)} \cdot u_d^{(n)} + \sum_{j \neq i} \alpha_{ij}^{(n)} \cdot U_j^{(n)} + \sum_{m \neq n} \gamma_{nm} \cdot U^{(m)}$$

where:
- $u_d^{(n)}$ = utility from dimension d at level n
- $w_d^{(n)}$ = weight on dimension d at level n
- $\alpha_{ij}^{(n)}$ = within-level social preference parameter
- $\gamma_{nm}$ = cross-level complementarity coefficient

**Theorem 1 (Self-Similarity):** The utility function at every level has the same mathematical form, differing only in scale parameters. This self-similarity is not assumed but derived from the behavioral mechanisms generating levels.

### 2.3 The Cross-Level Complementarity Matrix

**Definition 3 (Cross-Level Complementarity Matrix):** The matrix Γ_cross captures how utility at one level affects utility at another:

$$\Gamma_{cross} = \begin{pmatrix}
\gamma_{11} & \gamma_{12} & \cdots & \gamma_{1N} \\
\gamma_{21} & \gamma_{22} & \cdots & \gamma_{2N} \\
\vdots & \vdots & \ddots & \vdots \\
\gamma_{N1} & \gamma_{N2} & \cdots & \gamma_{NN}
\end{pmatrix}$$

**Proposition 2 (Symmetry Breaking):** In general, Γ_cross is not symmetric: $\gamma_{nm} \neq \gamma_{mn}$. The effect of household welfare on individual utility may differ from the effect of individual utility on household welfare.

---

## 3. Inter-Level Dynamics

### 3.1 Three Types of Dynamics

GTWH identifies three fundamental inter-level dynamics:

**Definition 4 (Upward Dynamics):** Individual-level changes affecting higher-level welfare:
$$\frac{\partial U^{(n+1)}}{\partial U_i^{(n)}} = \gamma_{n,n+1} + \sum_j \alpha_{ij}^{(n+1)} \cdot \frac{\partial U_j^{(n+1)}}{\partial U_i^{(n)}}$$

**Definition 5 (Downward Dynamics):** Higher-level changes affecting individual welfare:
$$\frac{\partial U_i^{(n)}}{\partial U^{(n+1)}} = \gamma_{n+1,n} + IDN(i, L_{n+1}) \cdot \beta_{identity}$$

**Definition 6 (Horizontal Dynamics):** Cross-level effects at the same hierarchical depth:
$$\frac{\partial U^{(n)}_A}{\partial U^{(n)}_B} = \gamma_{n,n}^{AB} \cdot KNU(A,B)$$

### 3.2 The Level Salience Function

**Definition 7 (Level Salience):** The salience of level n in context ψ:
$$S^{(n)}(\psi) = f(IDN^{(n)}, KNU^{(n)}, \psi)$$

**Proposition 3 (Context-Dependent Salience):** Level salience varies with context. In family contexts, household-level utility dominates; in professional contexts, firm-level utility may dominate; in civic contexts, community or national-level utility may be salient.

---

## 4. Resolving the Aggregation Problem

### 4.1 Why GTWH Avoids Arrow's Impossibility

Arrow's theorem assumes that social choice must aggregate independently given individual preferences. GTWH sidesteps this by recognizing that:

1. **Preferences are not independent**: IDN creates correlated preferences within levels
2. **Levels are not external**: They emerge from behavioral mechanisms
3. **Aggregation is not mechanical**: It reflects real psychological processes

**Theorem 2 (Coherent Aggregation):** Under GTWH, welfare aggregation is coherent because levels are defined by the very mechanisms (IDN, KNU) that make aggregation meaningful.

### 4.2 The GTWH Solution

Instead of:
- Individual utilities → [Aggregation Rule] → Social Welfare

GTWH proposes:
- Individual utilities + IDN + KNU → [Emergence] → Level-specific Utilities → [Natural Composition] → Multi-Level Welfare

---

## 5. Empirical Implications

### 5.1 Testable Predictions

**Prediction 1 (Level Number):** The number of welfare levels N_L is finite and empirically determinable from IDN and KNU data.

**Prediction 2 (Asymmetric Spillovers):** Upward and downward dynamics have different magnitudes: γ_{n,n+1} ≠ γ_{n+1,n}.

**Prediction 3 (Context Dependence):** Level salience varies systematically with context variables ψ.

**Prediction 4 (Complementarity Patterns):** The cross-level complementarity matrix Γ_cross has predictable structure based on IDN and KNU distributions.

### 5.2 Parameter Estimation

Key parameters can be estimated from:
- Survey data on identity strength (IDN)
- Experimental games measuring social preferences (KNU)
- Panel data on welfare outcomes at different levels
- Context variation studies for salience function

---

## 6. Discussion

### 6.1 Relation to Existing Frameworks

GTWH builds on and extends several literatures:

**Identity Economics (Akerlof & Kranton):** GTWH formalizes how identity creates welfare levels, not just utility components.

**Social Preferences (Fehr & Schmidt, Bolton & Ockenfels):** GTWH shows how social preferences generate inter-level dynamics, not just within-level effects.

**Complementarity Theory (Milgrom & Roberts, Brynjolfsson & Milgrom):** GTWH extends complementarity to cross-level interactions.

### 6.2 Policy Implications

GTWH has important implications for policy:

1. **Level-Appropriate Interventions:** Policies should target the appropriate welfare level based on IDN and KNU structure.

2. **Cross-Level Spillovers:** Policy effects at one level will spill over to other levels via Γ_cross.

3. **Context Sensitivity:** The same policy may have different effects in different contexts due to level salience variation.

---

## 7. Conclusion

The General Theory of Welfare Hierarchies resolves the aggregation problem by recognizing that welfare levels are not externally imposed but emerge from behavioral mechanisms. When people share identity and care about each other's utility, coherent welfare levels naturally arise. The recursive, self-similar structure of utility functions across levels provides a unified framework for multi-level welfare analysis.

---

## Appendix A: Addressing Objections

### A.1 "Isn't this just traditional welfare economics with extra steps?"

No. Traditional welfare economics takes levels as given and asks how to aggregate. GTWH derives levels endogenously and shows that aggregation follows naturally from the mechanisms creating levels.

### A.2 "How do you measure IDN and KNU?"

IDN can be measured through:
- Survey instruments (identity scales, group attachment measures)
- Behavioral experiments (identity salience manipulations)
- Neural measures (in-group/out-group processing)

KNU can be measured through:
- Dictator and ultimatum games
- Public goods experiments
- Revealed preference from consumption data

### A.3 "What about heterogeneity within levels?"

GTWH allows for heterogeneity through the distribution of IDN and KNU within levels. The level thresholds τ_IDN and τ_KNU define boundaries, but there is variation within.

### A.4 "Is the self-similarity assumption realistic?"

Self-similarity is not assumed but derived. It emerges because the same behavioral mechanisms (IDN, KNU) operate at every level. Empirical departures from self-similarity would indicate additional mechanisms not captured by GTWH.

### A.5 "How many levels are there in practice?"

This is an empirical question. Based on typical IDN and KNU patterns, we expect 4-6 levels in most societies:
- Individual (L0)
- Household/Family (L1)
- Community/Organization (L2)
- Region/Sector (L3)
- Nation/Society (L4)

### A.6 "What about international welfare?"

GTWH can accommodate international levels if IDN and KNU exceed thresholds across national boundaries. Global identity movements and international institutions may create supra-national welfare levels.

### A.7 "How does this relate to behavioral economics?"

GTWH is fundamentally behavioral: it builds on documented biases and preferences rather than assuming rational maximization. The emergence of levels from IDN and KNU is a behavioral phenomenon.

### A.8 "Can GTWH be falsified?"

Yes. Specific predictions include:
- Finite number of levels
- Asymmetric spillovers
- Context-dependent salience
- Predictable Γ_cross structure

Any of these could be falsified by data.

### A.9 "What about welfare comparisons across levels?"

GTWH provides a natural metric for cross-level comparison: the contribution of each level to total welfare, weighted by level salience. This avoids arbitrary comparisons by grounding them in behavioral mechanisms.

### A.10 "How does GTWH handle conflicts between levels?"

Conflicts arise when Γ_cross contains negative elements or when level salience shifts create trade-offs. GTWH characterizes these conflicts precisely rather than resolving them normatively.

---

## EBF Integration Notes

### Foundational Relevance for EBF Framework

This paper is **FOUNDATIONAL** for the EBF Framework. It formalizes the WHO dimension (Appendix AAA) by deriving welfare levels endogenously.

### 10C Connection

| 10C | Relevance | Connection |
|-----|-----------|------------|
| **WHO (AAA)** | Primary | Defines welfare levels L0-L4 |
| **HIERARCHY** | Strong | Inter-level dynamics formalized |
| **HOW (B)** | Strong | Γ_cross = cross-level complementarity |
| **WHEN (V)** | Moderate | Level salience S(n)(ψ) depends on context |
| **WHAT (C)** | Moderate | Utility dimensions d at each level |

### Key Parameters for EBF

- **IDN**: Shared identity threshold for level formation
- **KNU**: Collective utility interdependence threshold
- **τ_IDN, τ_KNU**: Threshold parameters for level definition
- **γ_nm**: Cross-level complementarity coefficients
- **S^(n)(ψ)**: Level salience function
- **α_ij^(n)**: Within-level social preference parameters
- **N_L**: Endogenous number of levels

### Theory Catalog Mapping

This paper **defines the foundation** for:
- MS-WH-001: General Theory of Welfare Hierarchies
- Extends MS-IB-001 (Identity Economics)
- Extends MS-SP-001 (Social Preferences)
- Integrates with MS-CO-002 (Complementarity Theory)

### Citation

This paper should be cited whenever the EBF Framework uses:
- Welfare hierarchy levels (L0-L4)
- Cross-level complementarity (Γ_cross)
- Level salience function S(n)(ψ)
- IDN/KNU thresholds for level definition
