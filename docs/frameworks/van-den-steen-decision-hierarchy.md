# Van den Steen Theory of Strategy: Formalizing Emergent Decision Hierarchies

**Author:** BEATRIX Research Group
**Version:** 1.0 (January 2026)
**Purpose:** Ground the emergent decision layer framework in Van den Steen's formal theory of strategy

---

## Executive Summary

Van den Steen (2017) provides a formal theory showing that **strategy is the smallest set of choices that determines all other choices through complementarity**. This insight directly explains why behavioral intervention design has emergent decision hierarchies:

1. **Meta-Level Choice:** The strategic decision (e.g., "Aggressive Growth" vs. "Maintenance")
2. **Constrained Choices:** All other intervention decisions that MUST align with the meta-choice
3. **Emergence:** The number of constrained choices (= number of decision layers) depends on:
   - The ambition level of the meta-choice
   - The complexity of the target context
   - The welfare level (Individual to Nation)

**Key Theorem (Van den Steen + Complementarity):**
$$\text{Number of Decision Layers} = f(\text{Meta-Choice Ambition}, \text{Context Complexity}, \text{Welfare Level})$$

This is NOT a fixed 4-layer hierarchy. It EMERGES from the strategic choice.

---

## Part 1: Van den Steen's Core Theory

### Definition 1.1: Strategy as Smallest Set of Choices

In Van den Steen's formal theory, **strategy is the smallest set of choices that, through complementarity, determines all other choices**.

**Mathematical Definition:**

Let $\mathcal{C} = \{c_1, c_2, ..., c_n\}$ be all choices in an organization/intervention.

A **strategy** is a subset $S \subset \mathcal{C}$ such that:

1. **Sufficiency:** For any choice $c_i \notin S$, the optimal value of $c_i$ is uniquely determined by $S$
2. **Minimality:** Removing any choice from $S$ violates Sufficiency

**Mathematically:**
$$S = \arg\min_{S' \subset \mathcal{C}} |S'| \quad \text{s.t.} \quad \forall c_i \notin S': c_i^* = \arg\max c_i \; \text{given} \; S'$$

### Definition 1.2: Why Strategy Exists (Coordination vs. Autonomy)

Van den Steen shows that a choice $c_i$ should be included in strategy if and only if the coordination benefit exceeds the autonomy cost.

**Value of Including Choice in Strategy:**
$$V_i = \underbrace{\beta_{coord}^{(i)} \cdot (1 - \text{Var}(c_i))}_{\text{coordination gain}} - \underbrace{\sum_j \gamma_{ij} \cdot |c_i - c_i^{preferred,j}|}_{\text{autonomy loss}}$$

where:
- $\beta_{coord}^{(i)}$ = how much other agents' payoffs depend on $c_i$ being coordinated
- $\text{Var}(c_i)$ = variance of $c_i$ without strategy (high variance = bad coordination)
- $\gamma_{ij}$ = complementarity strength between $c_i$ and preferences of agent $j$
- $c_i^{preferred,j}$ = what agent $j$ would choose without coordination constraint

**Decision Rule:**
$$\text{Include } c_i \text{ in Strategy} \Leftrightarrow V_i > 0$$

### Definition 1.3: Shared Beliefs = Strategy

A critical insight from Van den Steen: **Strategy is equivalent to shared beliefs** about what matters.

If all agents share beliefs about:
- Which choices are strategic (are in $S$)
- What values those choices should take

Then:
- All other choices automatically align (because they're determined by $S$)
- The organization/intervention needs minimal enforcement
- Value is maximized

---

## Part 2: Application to Behavioral Intervention Design

### Theorem 2.1: Meta-Level Strategic Choice

In intervention design, the **meta-level strategic choice** is the highest-level commitment that cascades through the entire intervention architecture.

**Examples by Context:**

| Context | Meta-Level Choice | What It Determines |
|---------|-------------------|-------------------|
| **Health (Smoking)** | "Complete Cessation vs. Harm Reduction" | All messaging, pharmacology, social support |
| **Finance** | "Aggressive Savings vs. Minimal Obligation" | Which defaults, which incentives, which nudges |
| **Sustainability** | "Transformation vs. Incremental Improvement" | Supply chain redesign, incentive structure |
| **Organization** | "Digital Disruption vs. Organizational Continuity" | Training intensity, change management depth |

### Theorem 2.2: Cascading Constraints (The Decision Hierarchy)

Once the meta-choice is fixed, **a cascade of dependent choices emerges through complementarity**.

**Mathematical Model:**

Let $m$ = meta-choice (strategy scope)
Let $D_k$ = the $k$-th level of dependent choices

**Cascade Structure:**

$$\begin{array}{lcl}
D_0: & m & \text{(Meta-choice: e.g., "Aggressive")} \\
D_1: & \{c_1, c_2, ..., c_k\} & \text{Choices that must align with } m \\
D_2: & \{c_{k+1}, ..., c_\ell\} & \text{Choices determined by } D_1 \\
D_3: & \{c_{\ell+1}, ..., c_p\} & \text{Choices determined by } D_2 \\
& \vdots & \vdots
\end{array}$$

Each level $D_i$ contains choices that:
1. Are complementary with $m$ (or with $D_{i-1}$)
2. CANNOT vary independently of the upstream choice
3. Must be coordinated for the intervention to be coherent

### Definition 2.3: What Creates a Decision Layer?

A **decision layer** exists at level $i$ if and only if there is at least one choice that:
1. Cannot be determined by any choice at level $i-1$ alone
2. Requires explicit decision-making
3. Is complementary with the strategic direction

**Formally:**

Layer $D_i$ exists $\Leftrightarrow \exists c \in D_i$ such that:

$$c^* = \arg\max c \text{ given } D_0, D_1, ..., D_{i-1} \text{ is not a unique, deterministic function}$$

In other words: **There is still discretion at this level** (not fully determined by upstream choices).

### Theorem 2.4: Number of Layers Depends on Ambition

The number of decision layers is NOT fixed. It depends on:

**Layer Count Formula:**

$$N_{layers} = 1 + \sum_{i=1}^{\infty} \mathbb{1}\left[\text{Discretion Remains at Level } D_i\right]$$

where $\mathbb{1}[·]$ is an indicator function.

**Factors Determining Number of Layers:**

| Factor | Low Value | High Value |
|--------|-----------|-----------|
| **Meta-Choice Ambition** | "Maintain status quo" (2-3 layers) | "Transform completely" (6-8+ layers) |
| **Context Complexity** | Simple binary (fewer layers) | Complex multi-stakeholder (more layers) |
| **Welfare Level** | Individual (fewer layers) | Nation/Society (more layers) |
| **Complementarity Density** | Sparse network (fewer) | Dense network (more) |

---

## Part 3: Mapping Decision Layers to Intervention Archetypes

### Table 3.1: Emergent Layers by Strategic Archetype

```
Meta-Choice Archetype:
├── HARVESTING (Exit-Oriented)
│   ├── Individual Level: 1-2 layers (e.g., "Cease all activity")
│   ├── Team Level: 2-3 layers
│   ├── Organization Level: 2-3 layers
│   └── Nation Level: 3-4 layers
│
├── MAINTENANCE (Status Quo Preservation)
│   ├── Individual Level: 2-3 layers (e.g., "Keep doing what works")
│   ├── Team Level: 3-4 layers
│   ├── Organization Level: 3-4 layers
│   └── Nation Level: 4-5 layers
│
├── BALANCED (Incremental Improvement)
│   ├── Individual Level: 3-4 layers (e.g., "Moderate improvement")
│   ├── Team Level: 4-5 layers
│   ├── Organization Level: 4-6 layers
│   └── Nation Level: 6-8 layers
│
└── AGGRESSIVE (Transformation)
    ├── Individual Level: 4-5 layers (e.g., "Complete life redesign")
    ├── Team Level: 5-6 layers
    ├── Organization Level: 6-8 layers
    └── Nation Level: 8-12+ layers
```

### Why Aggressive Has More Layers

**Intuition:** When you commit to "transformation," you have more dependent choices to make:

1. **Meta-Choice:** "Aggressive transformation"
2. **Layer 1:** Which dimensions transform? (What gets disrupted?)
3. **Layer 2:** How radical? (Scope of change in each dimension)
4. **Layer 3:** Timeline? (When does each change occur?)
5. **Layer 4:** Support structure? (What holds the system together during transformation?)
6. **Layer 5:** Communication strategy? (How do stakeholders understand the vision?)
7. **Layer 6:** Governance model? (Who decides during transition?)
8. **Layer 7:** Success metrics? (What determines success at each phase?)

**In contrast, "Maintenance" at individual level:**
1. **Meta-Choice:** "Keep current behavior"
2. **Layer 1:** What reminders/supports needed? (Habit maintenance)
3. **Layer 2:** How to handle lapses? (Exception handling)

---

## Part 4: Formal Integration with Complementarity Theory

### Theorem 4.1: Complementarity Determines Layer Boundaries

Two choices $c_i$ and $c_j$ are in the SAME layer if they are **substitutes** (not strongly complementary).
Two choices are in DIFFERENT layers if they are **complements** (strongly dependent).

**Mathematical Definition:**

Complementarity parameter:
$$\gamma_{ij} = \frac{\partial^2 V}{\partial c_i \partial c_j}$$

Layer Assignment Rule:
$$\text{Layer}(c_i) < \text{Layer}(c_j) \Leftrightarrow \exists c_k: \gamma_{ki} > \gamma_{kj}$$

In words: A choice $c_i$ comes BEFORE $c_j$ in the hierarchy if something upstream is more complementary with $c_i$.

### Theorem 4.2: Coherence Constraint

Not all combinations of layer decisions are valid. An intervention is **coherent** if:

For every layer $D_i$, the choices made are **mutually reinforcing** with all upstream choices.

**Formally:**

$$\text{Coherent}(m, D_1, D_2, ..., D_n) \Leftrightarrow \forall i, j: \gamma_{ij} \geq \gamma_{min}$$

where $\gamma_{min}$ is a context-dependent threshold of acceptable complementarity.

**Implication:** Misaligned choices cause 30-80% efficiency loss (Van den Steen, 2017).

Examples of Incoherence:
- Meta-choice: "Aggressive digital transformation"
- Layer 1: "Traditional hierarchical governance"
- **INCOHERENT** ← These choices contradict

---

## Part 5: Practitioner Framework

### Procedure 5.1: How to Determine Your Decision Layers

**Step 1: Fix the Meta-Level Choice**

Ask: "What is our fundamental strategic commitment?"

Examples:
- "Complete smoking cessation for all individuals by 2030"
- "Carbon neutral operations by 2025"
- "Industry-leading digital customer experience"

**Step 2: Identify Level 1 Choices (Directly Dependent)**

Ask: "What MUST be decided to implement the meta-choice?"

Example for "Complete smoking cessation":
- L1a: Pharmacological support (nicotine replacement? Bupropion? Varenicline?)
- L1b: Social support structure (group vs. individual?)
- L1c: Incentive structure (penalty or reward based?)
- L1d: Communication approach (fear-based? Empowerment-based?)

**Step 3: Identify Level 2 Choices (Dependent on Level 1)**

Ask: "Given Level 1 choices, what still needs deciding?"

Example: If L1a = "Varenicline only" and L1c = "Incentive-based"
- L2a: What is the financial incentive scale?
- L2b: When are incentives provided?
- L2c: Who qualifies? (How strict?)

**Step 4: Continue Until No Discretion Remains**

Ask: "At this level, are all important choices determined by upstream, or is there still discretion?"

If YES, discretion remains → Create another layer
If NO, fully determined → Stop

### Example 5.1: Smoking Cessation - Layers by Archetype

**MAINTENANCE Archetype (2-3 layers):**
```
Meta-Choice: "Reduce smoking by 20% in 2 years"
├─ Layer 1: Target population (smokers with high health risks)
├─ Layer 2: Primary intervention (Nicotine replacement patches + self-help)
└─ Layer 3: Tracking/Follow-up (quarterly check-ins)
```

**AGGRESSIVE Archetype (5-6 layers):**
```
Meta-Choice: "Achieve complete smoking cessation in target population"
├─ Layer 1: Clinical approach (Combination pharmacotherapy + intensive counseling)
├─ Layer 2: Social infrastructure (Peer support groups + family engagement)
├─ Layer 3: Incentive structure (Performance-based bonuses + penalties)
├─ Layer 4: Timeline design (When to escalate intensity)
├─ Layer 5: Communication strategy (Sustained messaging + belief alignment)
└─ Layer 6: Success metrics (Hard stops if compliance drops below X%)
```

---

## Part 6: Connection to Appendix UNMAPPED_PAP (Equilibria Framework)

### How Van den Steen + BB Create a Complete Framework

**Appendix UNMAPPED_PAP provides:**
- Equilibrium diagnostics ($\xi$, $\kappa_{crit}$)
- Drift rates ($\lambda(\kappa)$)
- Optimal intervention intensity

**Van den Steen provides:**
- Why interventions have multiple coordinated layers (not just "more of the same")
- How to design those layers for coherence
- Why misalignment kills effectiveness

**Integration:**
1. **Diagnosis (BB):** What is the current equilibrium quality?
2. **Strategy (Van den Steen):** What meta-choice are we making?
3. **Design (Van den Steen + Complementarity):** How many layers of decisions must be coordinated?
4. **Implementation (Appendix UNMAPPED_REA):** How do we ensure willingness at each layer?

---

## Part 7: Key References

**Primary Source:**
- Van den Steen, E. (2017). "A Formal Theory of Strategy." *Management Science*, 63(8), 2616–2636.
  - Core concept: Strategy as the smallest set of choices
  - Coordination vs. autonomy tradeoff
  - Why firms exist (and why organizations need strategy)

**Secondary Applications:**
- Milgrom & Roberts (1990, 1995) on complementarities and organizational architecture
- Roberts (2004) *Modern Firm* - PARC framework for coherent organizational design
- Hart & Moore (1990) on incomplete contracts and residual control

**Integration with EBF:**
- Appendix UNMAPPED_STA (BCJ-T36): Van den Steen as special case of BCJ
- Appendix UNMAPPED_HOW: Complementarity theory foundations
- Appendix UNMAPPED_PAP: Equilibrium operationalization

---

## Part 8: Open Questions for Chapter 15

1. **Quantifying Layer Count:** How do we reliably predict $N_{layers}$ for a given context?
   - Can we use complementarity density as a proxy?
   - Is there a formula relating welfare level to layer count?

2. **Layer Interdependence:** How tightly must layers be coordinated?
   - Can decisions at Layer 2 proceed before Layer 1 is finalized?
   - What is the minimum consistency threshold?

3. **Adaptive Layering:** Can layer structure change during implementation?
   - What triggers adding/removing a layer?
   - How do we manage this dynamically?

4. **Cross-Welfare Coherence:** How do decision hierarchies align across welfare levels?
   - When Nation-level strategy conflicts with Individual-level choice
   - How to maintain coherence in multi-level interventions?

---

**Version:** 1.0
**Last Updated:** January 12, 2026
**Author:** BEATRIX Research Group
