# The Economic Approach to Personality, Character and Virtue

**Authors:** James J. Heckman, Tomas Galaty, Haihan Tian

**Source:** NBER Working Paper No. 31258, May 2023

**DOI:** 10.3386/w31258

**JEL Codes:** I24, J13, J24

---

## Abstract

This paper develops an economic approach to personality, character and virtue. We integrate personality psychology and virtue ethics into economics with a common framework. Psychological traits are actions, not immutable given endowments. Personality is shaped by evolution, social environment, and own choices. We examine the role of preferences and situations in generating measured behavior, and the efforts that people exert to meet situational demands. We formally develop the concept of character as the set of settled dispositions to reliably respond across a wide variety of situations. We model the emergence of a good person—the person of character—who acts through choice on commitment to virtue. We distinguish traits from preferences and compare and contrast psychological and economic perspectives on personality. Our analysis examines efforts and situations as factors shaping measured behaviors. It provides a foundation for empirically examining the distinction between traits and preferences. We enrich this framework with models of self-control and habituation. We survey empirical evidence supporting our analysis.

---

## I. Introduction

### The Challenge

Psychology and economics approach personality differently:
- **Psychology:** Traits are stable, heritable characteristics
- **Economics:** Preferences are stable, revealed through choices

This paper bridges these perspectives with a unified framework where:
1. Traits are actions (behaviors), not immutable endowments
2. Preferences and traits are conceptually distinct
3. Character emerges through choice and commitment to virtue

### Key Insight

**Traits are actions, not endowments.** What psychologists measure as "traits" are observed behaviors that emerge from the interaction of:
- Preferences (ψ) - what the person values
- Traits (θ) - stable behavioral dispositions
- Effort (e) - exertion to meet demands
- Situation (h) - external circumstances

### Paper Objectives

1. Integrate personality psychology into economics
2. Formalize virtue ethics in economic terms
3. Distinguish traits from preferences operationally
4. Model character development through self-control and habituation
5. Survey empirical evidence on malleability of character

---

## II. The Basic Framework

### Utility and Behavior

**Utility function:**
```
U = U(a, ψ, θ, h)
```

Where:
- a = action chosen
- ψ = preferences (valuation weights)
- θ = traits (stable dispositions)
- h = situation (external context)

**Measured behavior:**
```
B = f(θ, e, h)
```

Where:
- B = observed behavior (what psychologists measure)
- θ = traits
- e = effort exerted
- h = situation

### The Distinction: Preferences vs. Traits

| Concept | Definition | Stability | Observable |
|---------|------------|-----------|------------|
| **Preferences (ψ)** | What person values | Very stable | Through choices |
| **Traits (θ)** | Behavioral dispositions | Stable but malleable | Through behavior |
| **Effort (e)** | Exertion to meet demands | Variable | Through performance |

**Key point:** Preferences determine WHAT you want; traits determine HOW you typically behave.

### Traits as Actions

Traditional view: Traits are fixed endowments (genetic, innate)

Economic view: Traits are produced behaviors:
```
θ_{t+1} = g(θ_t, e_t, h_t)
```

Traits evolve based on:
- Prior trait level
- Effort invested in development
- Situations encountered

**Implication:** Personality is malleable through investment and effort.

---

## III. Character and Virtue

### Defining Character

**Character** = the set of settled dispositions to reliably respond across a wide variety of situations.

Formally:
```
Character: θ such that Var(B | h) is small for all h in H
```

A person of character produces consistent behaviors regardless of situation.

### The Virtue Framework

**Virtue** = commitment to an ideal through active choice.

Drawing on Aristotle's Nicomachean Ethics:
- Virtue is a mean between extremes (golden mean)
- Virtue requires practice (habituation)
- Virtue is about flourishing (eudaimonia)

### The Ideal Point Model

**Utility over traits:**
```
U(θ) = -|θ - σ*|
```

Where:
- σ* = ideal trait level (the golden mean)
- Utility decreases with distance from ideal

**The Golden Mean:**
```
σ* = argmax U(σ) where U''(σ) < 0

Deficiency < σ* < Excess
```

Examples:
| Virtue | Deficiency | Mean (σ*) | Excess |
|--------|------------|-----------|--------|
| Courage | Cowardice | Courage | Recklessness |
| Generosity | Stinginess | Generosity | Prodigality |
| Temperance | Insensibility | Temperance | Self-indulgence |

---

## IV. Self-Control Model

### The Problem of Temptation

Even with commitment to virtue, temptation can lead to deviation:
```
a_temptation ≠ a_virtuous
```

### The Self-Control Resource

**Self-control stock (S_t):**
- Depletable resource
- Required to resist temptation
- Can be developed through practice

**The constraint:**
```
a* = argmax U(a) subject to S_t ≥ c(a, a_temptation)
```

Where:
- c() = cost of resisting temptation
- a* = optimal action
- S_t = available self-control

### Self-Control Dynamics

```
S_{t+1} = (1 - δ_S)S_t + ι(rest_t) + investment_t
```

Where:
- δ_S = depreciation of self-control
- ι() = restoration from rest
- investment = active development

**Key insight:** Self-control is a muscle that:
- Gets fatigued with use
- Recovers with rest
- Grows stronger with training

---

## V. Habituation Model

### Aristotle's Insight

"We become just by doing just acts, temperate by doing temperate acts, brave by doing brave acts." (Nicomachean Ethics)

### Formal Model

**Habituation stock (K_t):**
```
K_{t+1} = (1 - δ_K)K_t + h(a_t)
```

Where:
- K_t = accumulated practice/habit
- δ_K = depreciation rate
- h() = habituation function
- a_t = action taken

**Effect on behavior:**
```
Cost(virtuous action) = c(a) / (1 + K_t)
```

Higher habituation → lower cost of virtuous action → more likely to act virtuously

### The Habit Formation Process

1. **Early stage:** Virtuous action requires effort, self-control
2. **Practice:** Repeated action builds habituation stock
3. **Late stage:** Virtuous action becomes natural, effortless

**This is character formation:** Converting effortful virtue into habitual virtue.

---

## VI. Effort and Situations

### The Role of Effort

Measured behavior is not just traits:
```
B = f(θ, e, h)
```

People exert effort to:
- Meet situational demands
- Signal traits they value
- Achieve goals

### Effort Depends on Stakes

```
e* = argmax [V(B) - c(e)]
```

Where:
- V(B) = value of behavior outcome
- c(e) = cost of effort

**High stakes → High effort → Behavior may not reflect true traits**

### The Situation-Trait Interaction

**Strong situations:** Constrain behavior, reduce trait expression
- Example: Job interview (everyone acts professional)

**Weak situations:** Allow trait expression
- Example: Unstructured free time

**Implication for measurement:** Context matters enormously for what "traits" you observe.

---

## VII. Distinguishing Traits from Preferences

### The Identification Problem

Both traits and preferences affect behavior. How to distinguish?

### Three Approaches

**1. Variation in Stakes**
- High stakes: Effort dominates, behavior may differ from traits
- Low stakes: Traits dominate, behavior reveals traits

**2. Variation in Situations**
- Same person, different situations
- Consistent behavior across situations → stable traits

**3. Longitudinal Analysis**
- Track changes over time
- Preferences more stable than traits
- Interventions affect traits but not preferences

### The Key Test

If an intervention changes behavior:
- **Trait change:** Behavior changes in many situations
- **Preference change:** Choice patterns change systematically

---

## VIII. Empirical Evidence on Malleability

### Early Childhood Interventions

**Perry Preschool Program:**
- Intensive preschool for disadvantaged children
- Long-term effects on:
  - Crime reduction
  - Education completion
  - Employment
  - Earnings
- Mechanism: Character skills, not IQ

**Jamaica Study:**
- Psychosocial stimulation for stunted children
- 20-year follow-up shows:
  - 25% increase in earnings
  - Effects operate through personality

**ABC Program:**
- Abecedarian early education
- Long-term health and economic benefits
- Character skills mediate effects

**China REACH:**
- Home-visiting program in rural China
- Weekly skill assessments
- Dynamic complementarity in skill formation

### Key Findings Across Studies

| Finding | Evidence |
|---------|----------|
| Character is malleable | All four programs |
| Early investment matters | Critical period effects |
| Effects are long-lasting | 20+ year follow-ups |
| Mechanism is character | IQ effects fade, character persists |
| Returns are high | 7-10% annual return on investment |

### The Fadeout Puzzle Resolved

**Traditional view:** Early intervention effects "fade out" (disappear over time)

**New interpretation (Heckman et al., 2026):**
- Measured skills change qualitatively with age
- "Fadeout" reflects skill emergence, not effect loss
- Character skills persist even when IQ effects fade

---

## IX. Implications for Economics

### For Human Capital Theory

1. **Extend skill formation:** Include character alongside cognition
2. **Recognize malleability:** Traits can be developed through investment
3. **Value character:** Character skills predict life success

### For Behavioral Economics

1. **Self-control as resource:** Incorporate S_t into models
2. **Habituation matters:** Include K_t for repeated behaviors
3. **Context dependence:** Model situation-trait interactions

### For Intervention Design

1. **Target character:** Focus on self-control, conscientiousness
2. **Build habits:** Design for repeated virtuous action
3. **Start early:** Exploit critical periods
4. **Maintain effort:** Character requires ongoing practice

---

## X. Connection to Philosophy

### Aristotelian Virtue Ethics

This paper provides economic formalization of Aristotle's insights:

| Aristotle | Economic Formalization |
|-----------|----------------------|
| Virtue as mean | Ideal point model σ* |
| Practice makes perfect | Habituation K_t |
| Akrasia (weakness of will) | Self-control constraint S_t |
| Eudaimonia (flourishing) | Lifetime utility maximization |
| Phronesis (practical wisdom) | Optimal effort allocation |

### The Good Person

Economics can now formally model "the good person":
- Has stable character (consistent θ across h)
- Commits to virtue (chooses σ*)
- Exercises self-control (maintains S_t)
- Practices habituation (builds K_t)
- Achieves flourishing (maximizes U)

---

## XI. Summary

### Main Contributions

1. **Traits as actions:** Personality is produced, not given
2. **Character formalized:** Stable dispositions across situations
3. **Virtue economics:** Golden mean in utility framework
4. **Self-control model:** S_t as depletable resource
5. **Habituation model:** K_t from repeated practice
6. **Evidence integration:** Perry/Jamaica/ABC/China REACH

### Key Equations

| Model | Equation |
|-------|----------|
| Utility | U(a, ψ, θ, h) |
| Behavior | B = f(θ, e, h) |
| Trait evolution | θ_{t+1} = g(θ_t, e_t, h_t) |
| Ideal point | U(θ) = -\|θ - σ*\| |
| Self-control | S_{t+1} = (1-δ_S)S_t + ι(rest) |
| Habituation | K_{t+1} = (1-δ_K)K_t + h(a_t) |

### Practical Implications

- Character CAN be developed through intervention
- Early childhood is critical period
- Self-control and habituation are key mechanisms
- Returns to character investment are high

---

## Key Parameters for EBF

| Parameter | Symbol | Description | Notes |
|-----------|--------|-------------|-------|
| Preferences | ψ | What person values | Very stable |
| Traits | θ | Behavioral dispositions | Malleable |
| Effort | e | Exertion to meet demands | Variable |
| Situation | h | External context | Varies |
| Self-control | S_t | Stock of willpower | Depletable |
| Habituation | K_t | Stock of practice | Cumulative |
| Ideal point | σ* | Golden mean target | Virtue target |
| Depreciation (S) | δ_S | Self-control decay | ~0.1-0.2/period |
| Depreciation (K) | δ_K | Habit decay | ~0.02-0.05/period |
| Complementarity | γ | Effort-trait interaction | Positive |

---

## References

- Almlund et al. (2011). Personality psychology and economics.
- Aristotle. Nicomachean Ethics.
- Becker (1965). A theory of the allocation of time.
- Borghans et al. (2008). The economics and psychology of personality traits.
- Cunha & Heckman (2007). The technology of skill formation.
- Heckman (2006). Skill formation and the economics of investing in disadvantaged children.
- Heckman et al. (2026). Measuring the growth of skills.

---

*Archived: 2026-02-05 | Content Level: L3 | Integration Level: 4 (THEORY)*
