# Continuous Time and Communication in a Public-goods Experiment

**Authors:** Ryan Oprea, Gary Charness, Dan Friedman
**Date:** December 20, 2013
**Paper-ID:** PAP-oprea2013continuous
**Article Type:** Experimental Economics
**Archived:** 2026-02-04

---

## Abstract

We conduct public-goods experiments in continuous time with free-form chat, and compare to sequential discrete-time versions with and without communication. With continuous time and communication, groups typically coordinate at or near full efficiency despite challenging parameters (MPCR = 0.3). In discrete time, communication has a much smaller impact on average, and actually increases instability. Limited (pre-programmed) communication has no significant effect. Our results suggest that continuous time and rich communication are complements in enabling sustained cooperation.

---

## 1. Introduction

### The Cooperation Puzzle

A pervasive puzzle in social science concerns the maintenance of cooperation. When self-interested agents interact, theory predicts defection in one-shot games and unraveling in finitely repeated games. Yet empirical evidence shows sustained cooperation in many settings.

### Two Potential Explanations

1. **Social Preferences:** Agents may have utility functions that include others' payoffs
2. **Coordination:** Agents may desire to cooperate but face coordination problems

### Research Questions

This paper investigates whether continuous time and communication can enable sustained cooperation in public goods games with challenging parameters (MPCR = 0.3), and whether these factors are **complements**.

---

## 2. Experimental Design

### 2.1 Basic Setup

- **Subjects:** N = 128 (8 sessions × 16 subjects)
- **Location:** University of California laboratories
- **Design:** 2 × 2 between-subjects (Time Structure × Communication)
- **Game:** Linear public goods game (VCM)
- **MPCR:** 0.3 (challenging: dominant strategy is zero contribution)

### 2.2 Treatment Conditions

| Treatment | Time Structure | Communication | N |
|-----------|---------------|---------------|---|
| **DN** | Discrete | No Communication | 32 |
| **CN** | Continuous | No Communication | 32 |
| **DC** | Discrete | Full Communication (chat) | 32 |
| **CC** | Continuous | Full Communication (chat) | 32 |

### 2.3 Time Structures

**Discrete Time:**
- Sequential rounds
- Decisions made simultaneously at start of each round
- Feedback at end of each round
- Standard VCM protocol

**Continuous Time:**
- Real-time decisions
- Contributions can be adjusted at any moment
- Payoffs flow continuously
- Instantaneous feedback

### 2.4 Communication Protocols

**No Communication:**
- No interaction between subjects
- Standard anonymity

**Full Communication:**
- Free-form text chat
- Unrestricted messages
- Real-time in continuous time treatment

**Limited Communication (additional treatment):**
- Pre-programmed messages only
- Selected from menu of options

---

## 3. Results

### 3.1 Main Results Summary (Table 1)

| Treatment | Mean Contribution | Median | Rate at Maximum | Total Variation |
|-----------|------------------|--------|-----------------|-----------------|
| DN (Discrete, No Comm) | 32.6% | Low | 8% | Moderate |
| CN (Continuous, No Comm) | 38.9% | Low | 15% | Moderate |
| DC (Discrete, Comm) | 43.9% | Moderate | 21% | **Highest** |
| CC (Continuous, Comm) | **91.5%** | **100%** | **69%** | Low |

### Result 1: Continuous Time Alone Has Marginal Effect

> Without communication, continuous time improves cooperation only marginally (38.9% vs 32.6%).

**Interpretation:** Time structure alone is insufficient. Agents may wish to cooperate but cannot coordinate without communication.

### Result 2: Continuous Time + Communication = Superadditive

> With communication, continuous time leads to dramatically higher cooperation (91.5% vs 43.9% in discrete).

**Key Finding:** The interaction effect is **superadditive**:
- Expected if additive: 32.6% + (38.9%-32.6%) + (43.9%-32.6%) = 50.2%
- Observed: 91.5%
- **Superadditivity:** +41.3 percentage points above additive prediction

This is strong evidence for **complementarity**: γ(Time, Communication) > 0.

### Result 3: Communication Effects Differ by Time Structure

**In Discrete Time:**
- Communication increases mean contribution
- But also increases **instability** (highest total variation)
- Coordination attempts fail due to inability to respond quickly

**In Continuous Time:**
- Communication enables stable high cooperation
- Lowest variation among communication treatments
- Agents can respond immediately to coordinate

> "Communication increases stability in continuous time but decreases it in discrete time."

### Result 4: Limited Communication is Ineffective

> Pre-programmed messages have no significant effect compared to no communication.

**Interpretation:** Rich, free-form communication is essential. Limited signals are insufficient for the coordination required to sustain cooperation.

---

## 4. Mechanism Analysis

### 4.1 The Coordination Mechanism

The results support a **coordination explanation** rather than pure social preferences:

1. **If pure social preferences:** Communication shouldn't matter much (preferences already exist)
2. **If coordination:** Communication should enable coordination on efficient equilibria

The data strongly support the coordination mechanism:
- Communication has dramatic effect
- Effect is amplified in continuous time (where coordination is possible)
- Limited communication (insufficient for coordination) is ineffective

### 4.2 Why Complementarity?

**Continuous Time enables:**
- Rapid response to others' actions
- Real-time coordination
- Quick punishment of defection
- Immediate reward for cooperation

**Communication enables:**
- Expression of cooperative intentions
- Coordination on strategies
- Building of expectations
- Detection of defectors

**Together:**
- Agents can communicate intentions AND act on them immediately
- Creates self-enforcing cooperative equilibrium
- Neither alone is sufficient

---

## 5. Discussion

### 5.1 Implications for Theory

1. **Coordination vs. Preferences:** Results suggest coordination problems are primary barrier to cooperation
2. **Context Matters:** Time structure (Ψ_T) is crucial context variable
3. **Complementarity:** Interventions can be complements with superadditive effects

### 5.2 Policy Implications

For designing institutions that promote cooperation:

1. **Enable real-time interaction** (continuous time structure)
2. **Enable rich communication** (not just signals or votes)
3. **Recognize complementarity** - both together are essential

### 5.3 Limitations

- Laboratory setting (external validity questions)
- Specific MPCR and group size
- Anonymous subjects (vs. real relationships)

---

## Key Parameters Extracted (EBF Integration)

| Parameter | Symbol | Value | Treatment | Source |
|-----------|--------|-------|-----------|--------|
| Mean Contribution (DN) | μ_DN | 32.6% | Discrete, No Comm | Table 1 |
| Mean Contribution (CN) | μ_CN | 38.9% | Continuous, No Comm | Table 1 |
| Mean Contribution (DC) | μ_DC | 43.9% | Discrete, Comm | Table 1 |
| Mean Contribution (CC) | μ_CC | 91.5% | Continuous, Comm | Table 1 |
| Max Rate (DN) | r_DN | 8% | Discrete, No Comm | Table 1 |
| Max Rate (CN) | r_CN | 15% | Continuous, No Comm | Table 1 |
| Max Rate (DC) | r_DC | 21% | Discrete, Comm | Table 1 |
| Max Rate (CC) | r_CC | 69% | Continuous, Comm | Table 1 |
| Median (CC) | med_CC | 100% | Continuous, Comm | Table 1 |
| MPCR | α | 0.3 | All | Design |
| Superadditivity | Δ_super | +41.3pp | CC vs additive | Derived |

---

## EBF Framework Relevance

### Complementarity Evidence

```
                WITHOUT COMMUNICATION      WITH COMMUNICATION
                ─────────────────────      ──────────────────
DISCRETE        32.6%                      43.9%        (+11.3pp)
                    │                          │
                    │ +6.3pp                   │ +47.6pp  ← SUPERADDITIVE!
                    ▼                          ▼
CONTINUOUS      38.9%                      91.5%
```

**Complementarity Matrix Entry:**
```
γ(Time_Continuous, Communication_Rich) = STRONG POSITIVE

Evidence: 91.5% > 38.9% + 43.9% - 32.6% = 50.2%
Superadditivity: +41.3 percentage points
```

### 10C Mapping

| EBF Dimension | Oprea et al. Finding |
|---------------|---------------------|
| WHEN (Ψ_T) | Time structure is key context variable |
| HOW (γ) | Continuous × Communication = Complements |
| AWARE | Communication increases awareness of intentions |
| READY | Continuous time enables rapid response |

### SPÖ Application

| Finding | SPÖ Implication |
|---------|-----------------|
| Continuous > Discrete | Sustained engagement > periodic campaigns |
| Rich > Limited communication | Town halls, Q&A > slogans, flyers |
| Complementarity | Combined approach essential |
| Stability with both | Long-term support stabilization |

---

## Key References

### Public Goods Experiments
- Isaac & Walker (1988). Group size effects in public goods provision
- Ledyard (1995). Public goods: A survey of experimental research

### Communication in Games
- Charness & Dufwenberg (2006). Promises and partnership
- Bochet et al. (2006). Communication and punishment in VCM

### Continuous Time Games
- Friedman & Oprea (2012). A continuous dilemma
- Bigoni et al. (2015). Time horizon and cooperation in continuous time

---

*Full text archived for EBF Framework reference*
*Content Level: L3 (complete)*
*Evidence Tier: 2 (Experimental design, working paper / JEBO-level)*
*Original: Working Paper, University of California, December 2013*
