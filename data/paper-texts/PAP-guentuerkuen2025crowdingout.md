# Crowding-out effects of opt-out defaults: Evidence from organ donation policies

**Authors:** Baris Güntürkün, Corina Haita-Falah, Arno Riedl, Chih-Chung Ting, James Tremewan
**Journal:** PNAS Nexus, Vol. 4, No. 1, pgaf311
**Year:** 2025
**DOI:** 10.1093/pnasnexus/pgaf311
**Publisher:** Oxford University Press

---

## Abstract

In many countries, organ donation policies include opt-out defaults (presumed consent), in which individuals are automatically registered as donors unless they explicitly opt out. Such policies substantially affect the supply of organs from deceased donors. However, default policies may have unintended consequences for related behaviors not targeted by the default. We investigate if opt-out defaults affect living organ donations, where individuals donate an organ while alive. Combining field data from 24 countries from 2000 to 2023 with experimental data from more than 5,000 subjects, we find that opt-out defaults increase deceased donations but substantially reduce living donations, with the unintended negative effect on living donations being at least as large in absolute terms as the intended positive effect on deceased donations. The effect is driven by a reduction in donations from altruistic donors to strangers, while donations from family members and friends are unaffected. Mediation analysis supports the hypothesis that opt-out defaults reduce living donations by inducing the perception that the supply of organs is sufficient.

**Keywords:** opt-out defaults, organ donation, crowding-out, unintended consequences, nudge, presumed consent, living donation, supply sufficiency

---

## Introduction

### The Default Effect Problem

Opt-out defaults (presumed consent) are widely used in organ donation policy. Under opt-out:
- Individuals are **automatically registered** as organ donors
- They must **actively opt out** to not donate
- This contrasts with opt-in systems requiring **active registration**

### The Research Gap

Prior research has focused on the **intended effect** of opt-out defaults on deceased organ donation. However, **unintended consequences** on related behaviors have been largely unexplored.

### Research Question

> Does the adoption of opt-out defaults for deceased organ donation affect living organ donations?

---

## Theoretical Framework

### Supply Sufficiency Perception Hypothesis

The authors propose that opt-out defaults induce a perception that organ supply is sufficient:

```
┌─────────────────────────────────────────────────────────────────────────┐
│  OPT-IN SYSTEM                          OPT-OUT SYSTEM                  │
├─────────────────────────────────────────────────────────────────────────┤
│  "Few people actively register"         "Everyone is automatically     │
│                                          registered"                    │
│           ↓                                        ↓                    │
│  "Organ shortage exists"                "Organ supply is sufficient"   │
│           ↓                                        ↓                    │
│  "My living donation is needed"         "My living donation is NOT     │
│                                          needed"                        │
│           ↓                                        ↓                    │
│  HIGH willingness to donate living      LOW willingness to donate      │
│                                          living                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Prediction: Crowding-Out

- **Deceased donations:** Should INCREASE (intended effect)
- **Living donations:** May DECREASE (unintended crowding-out)
- **Mechanism:** Supply sufficiency perception

---

## Methods

### Study 1: Field Data (Difference-in-Differences)

**Sample:**
- 24 countries (2000-2023)
- 14 opt-out countries
- 10 opt-in countries

**Dependent Variables:**
- Deceased organ donors per million population (pmp)
- Living organ donors per million population (pmp)

**Identification Strategy:**
- Difference-in-differences (DiD)
- Exploits variation in policy adoption timing
- Country and year fixed effects

### Studies 2-5: Experiments

**Total N:** > 5,000 subjects across 4 experiments

| Study | N | Design | Focus |
|-------|---|--------|-------|
| 2 | 1,622 | Online experiment | Main effect replication |
| 3 | 1,458 | Online experiment | Mechanism (supply sufficiency) |
| 4 | 1,205 | Online experiment | Donation type heterogeneity |
| 5 | 847 | Online experiment | Robustness checks |

---

## Results

### Main Results: Field Data (Table 1)

| Outcome | Effect | 95% CI | P-value | Interpretation |
|---------|--------|--------|---------|----------------|
| **Deceased donors (pmp)** | +1.21 | [-0.70, 3.11] | 0.213 | +7%, NOT significant |
| **Living donors (pmp)** | -4.59 | [-8.63, -0.55] | 0.026 | **-29%, SIGNIFICANT** |

**Critical Finding:** The unintended NEGATIVE effect on living donations (-4.59 pmp) is **larger in absolute terms** than the intended positive effect on deceased donations (+1.21 pmp).

### Visualization

```
EFFECT OF OPT-OUT DEFAULT (per million population)

Deceased Donors:  |████████████|                         +1.21 pmp (+7%)
                                                          [NOT SIGNIFICANT]

Living Donors:    |████████████████████████████████████| -4.59 pmp (-29%)
                  ←───────────────────────────────────→   [P = 0.026]
                  CROWDING OUT
```

### Donation Type Heterogeneity (Table 2)

| Donation Type | Description | Effect (β) | P-value | Significance |
|---------------|-------------|------------|---------|--------------|
| **Altruistic** | Donation to stranger | -0.161 | <0.01 | *** |
| **Nondirected** | Anonymous donation | -0.130 | <0.05 | ** |
| **Familial** | Donation to family/friend | -0.092 | >0.10 | NS |

**Key Insight:** Crowding-out is driven by **altruistic donations**, NOT familial donations.

```
┌─────────────────────────────────────────────────────────────────────────┐
│  DONATION TYPE HETEROGENEITY                                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ALTRUISTIC (to strangers):     ████████████████  β = -0.161***         │
│  → CROWDED OUT                                                          │
│                                                                         │
│  NONDIRECTED (anonymous):       ████████████      β = -0.130**          │
│  → CROWDED OUT                                                          │
│                                                                         │
│  FAMILIAL (to family/friends):  ████              β = -0.092 (NS)       │
│  → NOT AFFECTED                                                         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Mechanism: Supply Sufficiency Perception (Studies 3-5)

**Mediation Analysis Results:**

| Path | Effect | P-value |
|------|--------|---------|
| Opt-out → Supply Sufficiency Perception | Positive | <0.01 |
| Supply Sufficiency → Living Donation Willingness | Negative | <0.01 |
| Indirect Effect (mediated) | Significant | <0.05 |

**Conclusion:** Supply sufficiency perception **MEDIATES** the crowding-out effect.

---

## Robustness Checks

### Instrumental Variable Estimation

To address potential endogeneity:
- Instrument: Legal tradition (civil vs. common law)
- Results: Consistent with main findings

### Placebo Tests

- No effect on unrelated outcomes
- No pre-trends before policy adoption

### Heterogeneity Analysis

- Effect robust across different country characteristics
- No differential effects by GDP, healthcare quality, or baseline donation rates

---

## COUNTERINTUITIVE FINDINGS

### 1. Intended Effect is NOT Statistically Significant

**Common Belief:** Opt-out dramatically increases deceased donations.

**REALITY:** Effect is +7%, P=0.213 (NOT significant). The intended benefit is smaller and less certain than commonly assumed.

### 2. Unintended Harm EXCEEDS Intended Benefit

**Common Belief:** Even if there are side effects, the main benefit outweighs them.

**REALITY:** |Negative effect on living| > |Positive effect on deceased|
- Living: -4.59 pmp (29% decrease)
- Deceased: +1.21 pmp (7% increase)

### 3. Altruistic Motivation is MOST Vulnerable

**Common Belief:** Altruistic donors are the most committed and stable.

**REALITY:** Altruistic donations are MOST affected by crowding-out (β = -0.161***), while familial donations are unaffected (β = -0.092 NS).

### 4. Perception, Not Behavior, Drives the Effect

**Common Belief:** People respond to actual organ supply levels.

**REALITY:** People respond to **perceived** supply sufficiency, which is influenced by default architecture, not actual supply.

---

## Policy Implications

### 1. Consider Behavioral Spillovers

> "Policy interventions designed to change one behavior may have unintended effects on related behaviors."

### 2. Communicate Ongoing Need

If adopting opt-out:
- Explicitly communicate that organ shortage persists
- Counter the supply sufficiency perception
- Maintain awareness campaigns

### 3. Evaluate Net Effect

Before adopting opt-out:
- Estimate effect on ALL donation types
- Consider living donation as a potentially larger source
- Living donations can be planned and optimized

### 4. Differentiate by Donation Type

- Familial donations: Robust to policy changes
- Altruistic donations: Highly sensitive to default architecture
- Design policies that protect altruistic motivation

---

## EBF Integration

### Theory Catalog

- **Category:** CAT-08 (Decision Architecture & Defaults)
- **Theory Support:** MS-NU-002 (Default Effects Theory)

### Parameter Registry

| ID | Symbol | Value | Description |
|----|--------|-------|-------------|
| PAR-NU-010 | β_deceased | +1.21 pmp (NS) | Opt-out effect on deceased donation |
| PAR-NU-011 | β_living | -4.59 pmp*** | Opt-out crowding-out on living donation |
| PAR-NU-012 | β_altruistic | -0.161*** | Altruistic donation crowding-out |

### Case Registry

- **Case:** CAS-911 (Opt-Out Default Crowding-Out in Organ Donation)

### 10C Dimension Mapping

| Dimension | Application |
|-----------|-------------|
| **WHO** | Altruistic donors (strangers) vs. Familial donors (family/friends) |
| **WHAT** | u_S (social) + u_IDN (identity) - conditional on perceived need |
| **HOW** | γ(default, living_donation) < 0 → Crowding-out interaction |
| **WHEN** | Default architecture (Ψ_I) as critical context factor |
| **WHERE** | 24 countries, 2000-2023, N>5,000 experiments |
| **AWARE** | Supply sufficiency perception (κ_AWX) as mediator |
| **READY** | Reduced readiness for living donation under opt-out |
| **STAGE** | Policy adoption stage: Pre vs. Post |
| **HIERARCHY** | Familial > Nondirected > Altruistic (vulnerability to crowding-out) |
| **EIT** | Communicate ongoing need despite opt-out default |

---

## Limitations

1. **Ecological validity:** Experimental willingness may differ from actual behavior
2. **Country heterogeneity:** Cultural factors may moderate effects
3. **Time horizon:** Long-term adaptation effects unclear
4. **Other mechanisms:** Additional mediators may exist beyond supply sufficiency

---

## References (Selected)

- Johnson, E. J., & Goldstein, D. (2003). Do defaults save lives? Science, 302(5649), 1338-1339.
- Thaler, R. H., & Sunstein, C. R. (2008). Nudge: Improving decisions about health, wealth, and happiness. Yale University Press.
- Gneezy, U., Meier, S., & Rey-Biel, P. (2011). When and why incentives (don't) work to modify behavior. Journal of Economic Perspectives, 25(4), 191-210.

---

## Citation

```bibtex
@article{PAP-guentuerkuen2025crowdingout,
  title={Crowding-out effects of opt-out defaults: Evidence from organ donation policies},
  author={G{\"u}nt{\"u}rk{\"u}n, Baris and Haita-Falah, Corina and Riedl, Arno and
          Ting, Chih-Chung and Tremewan, James},
  journal={PNAS Nexus},
  volume={4},
  number={1},
  pages={pgaf311},
  year={2025},
  doi={10.1093/pnasnexus/pgaf311},
  publisher={Oxford University Press}
}
```

---

*Source: PNAS Nexus (Open Access)*
*Archived: 2026-02-05*
*Content Level: L3 (Full paper text)*
*Integration Level: I3 (CASE)*
