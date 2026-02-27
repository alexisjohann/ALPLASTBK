# Ψ-Dimension Interaction Effects: Complements and Substitutes

**Date:** 2026-01-04  
**Method:** LLM Monte Carlo (Appendix AN Protocol)  
**Test Context:** Test 2 - Management Practices → Productivity (Bloom et al. 2012)

---

## Executive Summary

This document reports LLM Monte Carlo estimates for all 28 pairwise interaction effects between the 8 Ψ-dimensions. The key finding is that **Factor Flexibility (Ψ_F) acts as a universal complement**—it amplifies the effects of nearly all other dimensions. Meanwhile, **Institutions (Ψ_I) and Social Capital (Ψ_S) are substitutes**, consistent with the "Varieties of Capitalism" literature.

---

## Methodology

For each of the 28 pairwise interactions (8×7/2):
- 10 independent estimates generated
- 4 rotating perspectives: direct, comparative, theoretical, calibration
- 4 temperature levels: τ ∈ {0.3, 0.5, 0.7, 0.9}
- Aggregation: Mean, Std, 95% CI

**Interpretation:**
- β > 0: Complementary (dimensions reinforce each other)
- β < 0: Substitutive (dimensions replace each other)
- β ≈ 0: Independent (no interaction)

---

## Complete Interaction Matrix

### Strong Complements (β > +0.10)

| Interaction | β Mean | 95% CI | Interpretation |
|-------------|--------|--------|----------------|
| **Ψ_I × Ψ_F** | **+0.140** | [+0.10, +0.18] | Institutions + Flexibility = ordered adaptability |
| **Ψ_M × Ψ_F** | **+0.116** | [+0.09, +0.14] | Global markets require adjustment capacity |
| **Ψ_K × Ψ_M** | **+0.106** | [+0.08, +0.13] | Transparency enables global trade |
| **Ψ_T × Ψ_F** | **+0.105** | [+0.08, +0.13] | Stable rules enable orderly change |
| Ψ_I × Ψ_T | +0.101 | [+0.07, +0.14] | Institutions need time to consolidate |

### Moderate Complements (β ∈ [+0.05, +0.10])

| Interaction | β Mean | 95% CI | Interpretation |
|-------------|--------|--------|----------------|
| Ψ_C × Ψ_K | +0.096 | [+0.07, +0.12] | Information requires processing capacity |
| Ψ_K × Ψ_F | +0.095 | [+0.07, +0.12] | Information enables informed adjustment |
| Ψ_E × Ψ_T | +0.086 | [+0.06, +0.11] | Development needs stable conditions |
| Ψ_T × Ψ_M | +0.086 | [+0.06, +0.11] | Stability enables long-term trade |
| Ψ_C × Ψ_F | +0.085 | [+0.06, +0.11] | Skills enable flexibility utilization |
| Ψ_I × Ψ_K | +0.076 | [+0.05, +0.10] | Transparency makes institutions effective |
| Ψ_S × Ψ_T | +0.076 | [+0.05, +0.10] | Trust requires time to build |
| Ψ_C × Ψ_M | +0.076 | [+0.05, +0.10] | Skills rewarded in larger markets |
| Ψ_E × Ψ_M | +0.076 | [+0.05, +0.10] | Developed economies benefit from trade |
| Ψ_I × Ψ_M | +0.066 | [+0.04, +0.09] | Institutions enable global contracts |
| Ψ_C × Ψ_T | +0.066 | [+0.04, +0.09] | Education requires stable planning |
| Ψ_K × Ψ_T | +0.066 | [+0.04, +0.09] | Information valuable for long-term planning |

### Weak Complements (β ∈ [+0.02, +0.05])

| Interaction | β Mean | 95% CI | Interpretation |
|-------------|--------|--------|----------------|
| Ψ_C × Ψ_E | +0.045 | [+0.02, +0.07] | Cognition more valuable in developed economies |
| Ψ_I × Ψ_C | +0.038 | [+0.02, +0.06] | Rules require understanding for compliance |
| Ψ_S × Ψ_C | +0.031 | [+0.01, +0.05] | Networks require competence to leverage |

### Neutral (β ≈ 0)

| Interaction | β Mean | 95% CI | Interpretation |
|-------------|--------|--------|----------------|
| Ψ_E × Ψ_F | +0.025 | [+0.00, +0.05] | Rich countries often have rigid labor markets |
| Ψ_S × Ψ_M | +0.007 | [−0.02, +0.04] | Local networks vs. global markets tension |

### Substitutes (β < 0)

| Interaction | β Mean | 95% CI | Interpretation |
|-------------|--------|--------|----------------|
| Ψ_S × Ψ_F | −0.035 | [−0.06, −0.01] | Networks can inhibit mobility |
| Ψ_I × Ψ_E | −0.045 | [−0.07, −0.02] | Institutions more important in poor countries |
| Ψ_S × Ψ_K | −0.045 | [−0.07, −0.02] | Networks are information channels |
| Ψ_S × Ψ_E | −0.053 | [−0.08, −0.03] | Social capital more important in poor contexts |
| Ψ_I × Ψ_S | −0.055 | [−0.08, −0.03] | Formal rules replace informal trust |
| **Ψ_K × Ψ_E** | **−0.075** | [−0.10, −0.05] | Information interventions work where info is scarce |

---

## Key Findings

### 1. Factor Flexibility (Ψ_F) as Universal Complement

Ψ_F interacts positively with nearly all other dimensions:

| Partner | Interaction β |
|---------|---------------|
| Ψ_I | +0.140 |
| Ψ_M | +0.116 |
| Ψ_T | +0.105 |
| Ψ_K | +0.095 |
| Ψ_C | +0.085 |
| Ψ_E | +0.025 |
| Ψ_S | −0.035 |

**Interpretation:** Flexibility is the "enabler"—without it, other contextual advantages cannot be leveraged. This confirms the main effect finding that Ψ_F dominates in Test 2. Good institutions, transparency, and stability all require the *capacity to act* to translate into productivity gains.

### 2. Institutions and Social Capital as Substitutes

Ψ_I × Ψ_S = −0.055

This is the core insight of the "Varieties of Capitalism" literature:
- **Liberal Market Economies** (US, UK): High Ψ_I, lower reliance on Ψ_S
- **Coordinated Market Economies** (Germany, Japan): Balance of Ψ_I and Ψ_S
- **Informal Economies** (developing countries): Low Ψ_I, high reliance on Ψ_S

Formal rules and informal trust serve similar functions—contract enforcement, coordination, dispute resolution. Countries optimize across this tradeoff based on historical path dependencies.

### 3. Information × Development is Substitutive

Ψ_K × Ψ_E = −0.075 (strongest substitution)

**Interpretation:** In developed economies, information is already abundant—the marginal value of additional transparency is low. This is consistent with:
- Test 5 finding (information interventions work when Ψ_K is low)
- Jensen (2007): Large effects in Kerala where information was genuinely scarce
- Dupas (2011): Small effects where baseline information was already high

### 4. The Stability-Flexibility Nexus

Ψ_T × Ψ_F = +0.105 (strong complement)

This is counterintuitive at first—stability and flexibility seem opposed. But the interaction is positive because:
- **Stability without flexibility:** Rigidity, inability to adapt
- **Flexibility without stability:** Chaos, no planning horizon
- **Both together:** *Orderly adaptation*—the capacity to change within predictable rules

This is the "flexicurity" model (Denmark, Netherlands): High labor market flexibility combined with strong social safety nets and stable institutional frameworks.

### 5. The Information-Cognition Synergy

Ψ_C × Ψ_K = +0.096 (strong complement)

Information is only valuable if it can be processed. This implies:
- Information interventions should target populations with adequate baseline cognitive capacity
- Education and information provision are complements, not substitutes
- "Information overload" is a real phenomenon when Ψ_K >> Ψ_C

---

## Interaction Heatmap

```
         Ψ_I    Ψ_S    Ψ_C    Ψ_K    Ψ_E    Ψ_T    Ψ_M    Ψ_F
Ψ_I       —    −0.06  +0.04  +0.08  −0.05  +0.10  +0.07  +0.14
Ψ_S    −0.06     —    +0.03  −0.05  −0.05  +0.08  +0.01  −0.04
Ψ_C    +0.04  +0.03     —    +0.10  +0.05  +0.07  +0.08  +0.09
Ψ_K    +0.08  −0.05  +0.10     —    −0.08  +0.07  +0.11  +0.10
Ψ_E    −0.05  −0.05  +0.05  −0.08     —    +0.09  +0.08  +0.03
Ψ_T    +0.10  +0.08  +0.07  +0.07  +0.09     —    +0.09  +0.11
Ψ_M    +0.07  +0.01  +0.08  +0.11  +0.08  +0.09     —    +0.12
Ψ_F    +0.14  −0.04  +0.09  +0.10  +0.03  +0.11  +0.12     —

Legend: Strong complement (>+0.10): ██  Complement (+0.05 to +0.10): ▓▓  
        Weak/Neutral (−0.05 to +0.05): ░░  Substitute (<−0.05): ▒▒
```

---

## Policy Implications

### 1. Sequencing Matters

Because Ψ_F is a universal complement, reforms should prioritize flexibility *before* or *alongside* other improvements. Investing in institutions (Ψ_I) or information (Ψ_K) without flexibility (Ψ_F) yields diminished returns.

### 2. Context-Specific Substitution

The Ψ_I × Ψ_S substitution implies:
- In high-Ψ_I contexts: Don't invest heavily in social capital programs
- In low-Ψ_I contexts: Social capital programs may be highly effective

### 3. Information Targeting

The Ψ_K × Ψ_E substitution implies:
- Information interventions: Target low-Ψ_E contexts
- In high-Ψ_E contexts: Information is not the bottleneck

### 4. The Flexicurity Model

The Ψ_T × Ψ_F complementarity supports "flexicurity" policies:
- High flexibility + high stability = optimal
- This requires strong social insurance to enable risk-taking

---

## Limitations

1. **Single test context:** Interactions estimated for Management → Productivity only; may differ for other relationships
2. **Additive interaction model:** Higher-order interactions (3-way, 4-way) not estimated
3. **LLM-MC limitations:** As documented in Appendix AN

---

## Files in This Commit

- `interaction_effects_documentation.md` - This file
- `interaction_matrix.csv` - Raw interaction coefficients
- `interaction_heatmap_data.csv` - Matrix format for visualization

---

*Cross-references: Appendix AN (LLM-MC Methodology), Appendix V (Ψ-Dimensions), Test 2 Main Effects*
