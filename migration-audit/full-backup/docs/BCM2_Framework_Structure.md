# EBF: Behavioral Change Model - Framework Structure

## Overview

The Behavioral Change Model 2.0 (EBF) provides a comprehensive theoretical and practical framework for understanding and facilitating behavioral change. It integrates insights from behavioral economics, psychology, and decision science into a unified, actionable model.

---

## Part I: THEORETICAL FOUNDATIONS (Chapters 1-9)

*[Existing chapters from Complementarity-Context Framework]*

| Chapter | Title | Content |
|---------|-------|---------|
| 1-9 | Complementarity-Context Framework | Coherence (K), Context (Ψ), 8 Ψ-Dimensions, Γ-Matrix |

---

## Part II: THE BEHAVIORAL CHANGE MODEL (Chapters 10-14)

### Chapter 10: UTILITY - The Multi-Dimensional Welfare Function

**Core Question:** *What COULD generate utility?*

#### 10.1 The Three Utility Categories

| Category | Symbol | Question | Theoretical Source |
|----------|--------|----------|-------------------|
| Individual Utility | INU | "What do I want for MYSELF?" | Classical Economics |
| Collective Utility | KNU | "What do I want for US?" | Fehr & Schmidt, Behavioral Econ |
| Identity Utility | IDN | "Who AM I?" | Akerlof & Kranton |

#### 10.2 The Six FEPSDE Dimensions

| Dimension | Symbol | Content |
|-----------|--------|---------|
| Financial | F | Income, wealth, economic security |
| Emotional | E | Wellbeing, satisfaction, meaning |
| Physical | P | Health, energy, longevity |
| Social | S | Relationships, belonging, trust |
| Digital | D | Connectivity, access, data rights |
| Ecological | Eco | Environment, sustainability |

#### 10.3 The 144-Component Structure

```
144 = 3 (INU/KNU/IDN) × 6 (FEPSDE) × 4 (Time) × 2 (Gain/Pain)
    + 4 (Identity sub-components)
    = 148 Total Components
```

#### 10.4 Uniform Calculation Logic (for ALL components)

Each component has:
- **Reference Point** $r^i_d$ (category-specific)
- **Gains** $G^i_{d,t} = \max(0, x_d - r^i_d)$
- **Pains** $P^i_{d,t} = \max(0, r^i_d - x_d)$
- **Loss Aversion** $\lambda^i_d > 1$
- **Time Discounting** $\delta^i_d \in (0,1)$

**Universal Formula:**
$$U^i_{d,t} = \delta^{i,t}_d \cdot [G^i_{d,t} - \lambda^i_d \cdot P^i_{d,t}]$$

#### 10.5 Reference Point Formation

| Category | Reference Point Type | Formation |
|----------|---------------------|-----------|
| INU | Status quo / Expectation | Past experience, social comparison |
| KNU | Group norm / Fairness | Group standard, equitable distribution |
| IDN | Self-concept / "Should be" | Identity standard, role expectations |

#### 10.6 Inter-Category Complementarities

$$Q = \sum_i \omega_i \cdot U^i + \sum_{i \neq j} \gamma_{ij} \cdot U^i \cdot U^j$$

| Complementarity | Sign | Example |
|-----------------|------|---------|
| γ_{INU,KNU} | +/- | Team bonus (+) vs. Free-riding (-) |
| γ_{INU,IDN} | +/- | Success confirms identity (+) vs. "Selling out" (-) |
| γ_{KNU,IDN} | +/- | Group identity (+) vs. Conformity pressure (-) |

#### 10.7 Context Modulation (Γ-Matrix)

All parameters modulated by context Ψ:
$$\gamma_{dj}: \text{How } \Psi_j \text{ affects } U_d$$

---

### Chapter 11: AWARENESS - The Decision Filter

**Core Question:** *What does the person THINK about in the decision moment?*

#### 11.1 The Awareness Function

$$AWA = (a_{INU}, a_{KNU}, a_{IDN}) \quad \text{where } a_i \in [0,1]$$

| Parameter | Meaning |
|-----------|---------|
| $a_{INU} = 1$ | Individual consequences are salient |
| $a_{KNU} = 1$ | Collective consequences are salient |
| $a_{IDN} = 1$ | Identity implications are salient |
| $a_i = 0$ | This category is "not seen" |

#### 11.2 The Distinction: ω vs. a

| Parameter | Symbol | Meaning | Timescale | Source |
|-----------|--------|---------|-----------|--------|
| Weight | $\omega_i$ | How important IS this to me? | Stable (Trait) | Personality, values, culture |
| Awareness | $a_i$ | Am I THINKING about it NOW? | Situational (State) | Context, framing, nudge |

#### 11.3 Determinants of AWA

| Factor | Effect on $a_{INU}$ | Effect on $a_{KNU}$ | Effect on $a_{IDN}$ |
|--------|---------------------|---------------------|---------------------|
| Time pressure | ↑↑ | ↓ | ↓ |
| Social observation | ~ | ↑ | ↑↑ |
| "For you" framing | ↑↑ | ↓ | ~ |
| "For all of us" framing | ↓ | ↑↑ | ~ |
| Identity prime | ~ | ~ | ↑↑ |
| Cognitive load | ↑ (default) | ↓ | ↓ |
| Deliberation time | ~ | ↑ | ↑ |

#### 11.4 AWA and System 1/2

| System | Typical AWA Profile | Behavior |
|--------|---------------------|----------|
| System 1 (fast) | $a_{INU}$ high, others low | Self-interested, impulsive |
| System 2 (slow) | All $a_i$ can be high | Reflective, value-consistent |

#### 11.5 Nudges as AWA Manipulation

Nudges work primarily by changing $a_i$, not $\omega_i$!

---

### Chapter 12: WILLINGNESS - The Change Potential

**Core Question:** *Is the person READY to change?*

#### 12.1 The Willingness Equation

$$\boxed{WTC = \sum_{i \in \{INU,KNU,IDN\}} a_i \cdot \omega_i \cdot \Delta U^i}$$

Where:
- $a_i$ = Awareness (from Ch. 11)
- $\omega_i$ = Weight (stable preference)
- $\Delta U^i = U^i_{new} - U^i_{old}$ = Utility difference

#### 12.2 The Threshold

$$WTC > \theta \Rightarrow \text{Change likely}$$

Where $\theta$ = switching costs, inertia, habit strength

#### 12.3 The Three Levers for Behavioral Change

```
WTC = Σ a_i · ω_i · ΔU^i
      ↑     ↑      ↑
      │     │      │
      │     │      └── DESIGN: Better alternative (ΔU↑)
      │     │
      │     └────────── EDUCATE: Change values (ω change, long-term)
      │
      └──────────────── NUDGE: Activate awareness (a↑, short-term)
```

| Lever | Changes | Timescale | Example |
|-------|---------|-----------|---------|
| Nudge | $a_i$ | Seconds-minutes | Eco-label activates $a_{KNU}$ |
| Educate | $\omega_i$ | Months-years | Education increases $\omega_{KNU}$ |
| Design | $\Delta U^i$ | Immediate | Better product, higher wage |

---

### Chapter 13: JOURNEY - The Change Process

**Core Question:** *How does change UNFOLD over time?*

#### 13.1 The Journey Phases

```
PRE-CONTEMPLATION → CONTEMPLATION → PREPARATION → ACTION → MAINTENANCE → INTEGRATION
     (A ≈ 0)           (A > 0)        (WTC > 0)    (Δx > 0)  (Δx stable)  (new IDN)
                                                       ↑
                                                       └── RELAPSE (back to earlier phase)
```

#### 13.2 Phase Characteristics

| Phase | U | A | WTC | Characteristic |
|-------|---|---|-----|----------------|
| Pre-Contemplation | Not calculated | $a_i ≈ 0$ | Undefined | "No problem" |
| Contemplation | Being explored | $a_i$ rising | $WTC ≈ 0$ | "Maybe I should..." |
| Preparation | Clear | $a_i$ high | $WTC > 0$ | "I will..." |
| Action | $\Delta U$ realized | $a_i$ very high | $WTC >> θ$ | "I'm doing it" |
| Maintenance | New status quo | $a_i$ normalizing | $WTC_{back} < 0$ | "I'm staying with it" |
| Integration | $U^{IDN}$ adapted | Automatic | No longer relevant | "This is who I am now" |

#### 13.3 The Key: Identity Transformation

**Journey is only complete when IDN adapts!**

Without IDN shift → Relapse risk remains high

#### 13.4 Intervention Timing by Phase

| Phase | Correct Intervention | Wrong Intervention |
|-------|---------------------|---------------------|
| Pre-Contemplation | Increase awareness | Demand action (creates reactance) |
| Contemplation | Explore ambivalence | Push too fast |
| Preparation | Concrete plans, commitment | Keep discussing |
| Action | Support, quick wins | Leave alone |
| Maintenance | Relapse prevention | Assume it's "done" |
| Integration | Confirm new identity | Trigger old identity |

---

### Chapter 14: SEGMENTS - Behavioral Change Types

**Core Question:** *WHO are the people? What types exist?*

#### 14.1 Base Segments (by ω-Profile)

| Segment | $\omega_{INU}$ | $\omega_{KNU}$ | $\omega_{IDN}$ | Characteristic |
|---------|----------------|----------------|----------------|----------------|
| Individualist | HIGH | low | low | "What's in it for ME?" |
| Collectivist | low | HIGH | low | "What's in it for US?" |
| Identitarian | low | low | HIGH | "Does this fit ME?" |
| Balanced | medium | medium | medium | Context-dependent |

#### 14.2 Segment × Journey Matrix

```
                    JOURNEY PHASE
            Pre-Cont  Cont  Prep  Action  Maint  Integr
          ┌─────────────────────────────────────────────┐
Individualist │   I-PC   I-C   I-P    I-A    I-M    I-I    │
          │                                             │
Collectivist  │   K-PC   K-C   K-P    K-A    K-M    K-I    │
          │                                             │
Identitarian  │  ID-PC  ID-C  ID-P   ID-A   ID-M   ID-I   │
          │                                             │
Balanced      │   B-PC   B-C   B-P    B-A    B-M    B-I    │
          └─────────────────────────────────────────────┘
                    = 24 Base Segments
```

#### 14.3 Context-Dependent Segment Distribution

| Context | Individualist | Collectivist | Identitarian |
|---------|---------------|--------------|--------------|
| Economic boom | 40% | 20% | 15% |
| Crisis/threat | 20% | 40% | 25% |
| Culture war | 25% | 20% | **45%** |
| Normal state | 30% | 25% | 20% |

#### 14.4 Intervention Strategy by Segment

| Segment | Effective | Ineffective |
|---------|-----------|-------------|
| Individualist | Show ROI, personal benefit | Moral appeal, group pressure |
| Collectivist | Group commitment, social norm | Individual incentive alone |
| Identitarian | Identity bridge, "people like you" | Only financial incentives |
| Balanced | Flexible, context-dependent | One-size-fits-all |

---

## Part III: SYNTHESIS (Chapters 15-16)

### Chapter 15: WEC - Effective Willingness

**Core Question:** *How do journey and segment scale willingness?*

#### 15.1 The WEC Function

$$\boxed{WEC = (WAX - \theta) \cdot \alpha_{BCJ} \cdot \beta_{BCS}}$$

| Component | Meaning |
|-----------|---------|
| $WAX$ | Willingness to act (Ch. 12) |
| $\theta$ | Behavioral threshold |
| $\alpha_{BCJ}$ | Journey-stage multiplier (Ch. 13) |
| $\beta_{BCS}$ | Segment multiplier (Ch. 14) |

#### 15.2 Integration Chain

```
Context (Ψ) → Utility (U) → Awareness (A) → Willingness (WAX, θ)
                           ↓
                  Journey (BCJ) × Segment (BCS)
                           ↓
                    Effective Willingness (WEC)
```

---

### Chapter 16: PROBABILITY - Effective Output

**Core Question:** *How likely is behavioral change?*

#### 16.1 The Output Equation

$$\boxed{P_{eff} = \sigma(WEC)}$$

#### 16.2 Interpretation

| Range | Bedeutung | Implikation |
|-------|-----------|-------------|
| $P_{eff} \approx 0$ | Praktisch unmöglich | Interventionen zu früh/zu schwach |
| $P_{eff} \approx 0.5$ | Schwellenbereich | Timing und Segment-Fit entscheidend |
| $P_{eff} \rightarrow 1$ | Hohe Wahrscheinlichkeit | Skalierung möglich |

---

### Chapter 17: EFFECTIVENESS - Probability of Change

**Core Question:** *How LIKELY is behavioral change?*

#### 17.1 The Outcome Equation

$$\boxed{P(\Delta B | t) = WTC \times S_{match} \times J_{trans} \times (1 - R)}$$

| Factor | Symbol | Meaning | Range |
|--------|--------|---------|-------|
| Willingness | $WTC$ | Change readiness | [-1, +1] |
| Segment Match | $S_{match}$ | Intervention fits segment? | [0, 1] |
| Journey Transition | $J_{trans}$ | Phase transition probability | [0, 1] |
| Relapse Risk | $R$ | Relapse probability | [0, 1] |

#### 17.2 The Effectiveness Matrix

**P(ΔB) by Segment × Phase × Intervention:**

| Segment | Phase | Nudge (a↑) | Educate (ω↑) | Design (ΔU↑) |
|---------|-------|------------|--------------|--------------|
| Individualist | Preparation | 0.35 | 0.20 | **0.55** |
| Collectivist | Contemplation | **0.40** | 0.25 | 0.15 |
| Identitarian | Preparation | 0.15 | **0.40** | 0.20 |

#### 17.3 Population-Level Outcomes

$$P(\Delta B)_{pop} = \sum_k P(Segment_k) \cdot P(\Delta B | Segment_k)$$

---

## Part V: COUNTERFACTUAL ANALYSIS (Chapter 18)

### Chapter 18: BASELINES - What Happens Without Intervention?

**Core Question:** *What is the REFERENCE for evaluating interventions?*

#### 18.1 The Four Baselines

| Baseline | Name | Intervention | Result | Cost |
|----------|------|--------------|--------|------|
| **B0** | STATUS QUO | — | $\Psi_0$ | — |
| **B1** | DRIFT | None | $\Psi_1 < \Psi_0$ | 0 (but loss!) |
| **B2** | MAINTAIN | System maintenance | $\Psi_2 \approx \Psi_0$ | Maintenance cost |
| **B3+** | GROWTH | Improvement | $\Psi_3 > \Psi_0$ | Maint. + Growth cost |

#### 18.2 Visualization

```
    U
    ↑
    │                                    ○ B4 (Transformation)
  0.85│                                ●
    │                                /
    │                              /
  0.75│                        ●───○ B3 (Growth)
    │                      /
    │                    /
  0.60│──●─────────────●─────────────── B2 (Maintain)
    │   ○ B0          │
    │    \            │
  0.50│     \         │
    │       \        │
    │         \     │
  0.40│           ●─────────────────── B1 (Drift)
    │
    └────────────────────────────────→ Time
         t=0        t=5
```

#### 18.3 The Central Insight

$$\boxed{\text{Status quo} \neq \text{Do nothing}}$$

**Maintaining status quo COSTS!**

#### 18.4 The Value Equations

$$\text{Maintenance Value} = (U_{B2} - U_{B1}) - \text{Maintenance Cost}$$

$$\text{Growth Value} = (U_{B3} - U_{B2}) - \text{Growth Cost}$$

$$\text{Total Intervention Value} = (U_{B3} - U_{B1}) - \text{Total Cost}$$

#### 18.5 Sequential vs. Leapfrog

| Situation | Strategy |
|-----------|----------|
| Stable system, light erosion | B1 → B2 → B3 (sequential) |
| Obsolete system | B1 → B3 direct (leapfrog) |
| Burning platform | B1 → B4 direct (transform) |

**Decision Rule:** Skip B2 when direct jump to B3 has higher ROI than sequential path.

---

## Part VI: PRACTICE (Chapter 19)

### Chapter 19: INTERVENTION TOOLKIT

**Core Question:** *What can we DO?*

#### 19.1 The Three Levers (Recap)

| Lever | Changes | Mechanism |
|-------|---------|-----------|
| **Nudge** | $a_i$ | Activate awareness |
| **Educate** | $\omega_i$ | Change values/weights |
| **Design** | $\Delta U$ | Improve options |

#### 19.2 Interventions by Baseline Level

| Level | Intervention Type | Goal |
|-------|-------------------|------|
| B2 (Maintain) | System maintenance | Prevent erosion |
| B3 (Growth) | Improvement | Incremental gains |
| B4 (Transform) | Transformation | Fundamental change |

#### 19.3 Interventions by Segment

| Segment | Primary Lever | Approach |
|---------|---------------|----------|
| Individualist | Design (ΔU) | Show personal ROI |
| Collectivist | Nudge (a) + Design | Group commitment |
| Identitarian | Educate (ω) | Identity bridge |

#### 19.4 Interventions by Journey Phase

| Phase | Primary Intervention |
|-------|---------------------|
| Pre-Contemplation | Awareness activation |
| Contemplation | Ambivalence exploration |
| Preparation | Commitment devices |
| Action | Support & quick wins |
| Maintenance | Relapse prevention |
| Integration | Identity confirmation |

#### 19.5 The Intervention Matrix

$$\text{Optimal Intervention} = f(\text{Segment}, \text{Phase}, \text{Baseline}, \text{Context})$$

#### 19.6 Intervention Catalog

*[Detailed catalog of specific techniques, evidence base, application examples]*

---

## Summary: The Complete EBF Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  CONTEXT (Ψ) ─────────────────────────────────────────────────────┐ │
│       │                                                           │ │
│       ▼                                                           │ │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐                         │ │
│  │ UTILITY │ → │AWARENESS│ → │WILLING- │                         │ │
│  │   (U)   │   │   (A)   │   │NESS(WTC)│                         │ │
│  │ Ch. 10  │   │ Ch. 11  │   │ Ch. 12  │                         │ │
│  └─────────┘   └─────────┘   └────┬────┘                         │ │
│                                   │                               │ │
│                                   ▼                               │ │
│                    ┌─────────┐   ┌─────────┐                     │ │
│                    │ JOURNEY │ ← │SEGMENTS │                     │ │
│                    │ Ch. 13  │   │ Ch. 14  │                     │ │
│                    └────┬────┘   └─────────┘                     │ │
│                         │                                         │ │
│                         ▼                                         │ │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐          │ │
│  │   WEC   │   │ P(EFF)  │   │ POLICY  │   │ LIMITS  │          │ │
│  │ Ch. 15  │   │ Ch. 16  │   │ Ch. 17  │   │ Ch. 18  │          │ │
│  └─────────┘   └─────────┘   └─────────┘   └─────────┘          │ │
│                                                                   │ │
│                         │                                         │ │
│                         ▼                                         │ │
│              ┌─────────────────────┐                             │ │
│              │ CONCLUSION & OUTLOOK │ ←──────────────────────────┘ │
│              │       Ch. 19         │     (Context feeds back)     │
│              └─────────────────────┘                               │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Key Equations Summary

| Component | Equation |
|-----------|----------|
| Utility | $U^i_{d,t} = \delta^{i,t}_d \cdot [G^i_{d,t} - \lambda^i_d \cdot P^i_{d,t}]$ |
| Total Welfare | $Q = \sum_i \omega_i \cdot U^i + \sum_{i \neq j} \gamma_{ij} \cdot U^i \cdot U^j$ |
| Effective Decision | $Q^{eff} = \sum_i a_i \cdot \omega_i \cdot U^i$ |
| Willingness | $WTC = \sum_i a_i \cdot \omega_i \cdot \Delta U^i$ |
| Effectiveness | $P(\Delta B) = WTC \times S_{match} \times J_{trans} \times (1-R)$ |
| Intervention Value | $Value = (U^{intervention} - U^{baseline1}) - Cost$ |

---

## Document Information

- **Version:** 1.0
- **Date:** January 2025
- **Framework:** EBF (Behavioral Change Model)
- **Part of:** Complementarity-Context Framework
- **Repository:** FehrAdvice-Partners-AG/complementarity-context-framework
