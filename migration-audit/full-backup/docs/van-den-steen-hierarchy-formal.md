# Van den Steen Decision Hierarchy: Formal Specification

**Author:** BEATRIX Research Group
**Based on:** Van den Steen, E. (2017). "A Formal Theory of Strategy." Management Science, 63(8), 2616–2636.
**Version:** 1.1 (January 2026)
**Purpose:** Provide a formal, context-universal framework for understanding decision hierarchies

---

## Executive Summary

Van den Steen (2017) provides a formal theory that generates a universally applicable **4-level decision hierarchy**. This hierarchy is not context-specific (not unique to organizations vs. households vs. nations). Instead, it emerges endogenously from a single principle:

**Principle: A decision is strategic if and only if many other decisions optimally align to it.**

This creates a universal hierarchy applicable to any coordinated system:

| Level | Name | Definition | Example |
|-------|------|-----------|---------|
| **L0** | Meta-Meta-Decision | What counts as a relevant decision? (Defines decision space) | "Are we in business X?" "Market or state?" |
| **L1** | Strategic Root Decision | Few, persistent choices with high interaction density | "Cost-leadership or premium?" "Growth or stability?" |
| **L2** | Derived Strategic Decisions | Many choices that align to L1 through complementarity | "Which product lines?" "Supply chain structure?" |
| **L3** | Operative Decisions | Low interaction, low guiding effect; high specificity | "Which vendor?" "What quarterly budget?" |

**Key Insight:** Strategy = hierarchization of attention. A decision is strategic not because it is important, irreversible, or high-stakes, but because it guides other decisions.

---

## Part 1: Formal Foundations from Van den Steen

### Definition 1.1: Strategic Decision (Endogenous)

A decision $d_i$ is **strategic** relative to a set of choices $\mathcal{D} = \{d_1, ..., d_n\}$ if and only if:

$$d_i \text{ is strategic} \Leftrightarrow \exists \{d_j : j \neq i\} \text{ such that } d_j^* = \arg\max d_j \text{ given } d_i$$

**In words:** Decision $d_i$ is strategic if other decision-makers optimally condition their choices on $d_i$.

**Corollary:** This definition is reflexive and recursive:
- $d_i$ may be strategic relative to $\{d_j, d_k, ...\}$ but not relative to others
- No global "strategic" label; only relative to a context

### Definition 1.2: Hierarchy from Complementarity

Strategic decisions form a **hierarchy** when there is a partial ordering:

$$d_i \prec d_j \Leftrightarrow \text{The value of } d_i \text{ depends more strongly on } d_j \text{ than vice versa}$$

Formally: $\frac{\partial^2 V}{\partial d_i \partial d_j} > \frac{\partial^2 V}{\partial d_j \partial d_i}$ (complementarity asymmetry)

This creates a **directed acyclic graph (DAG)** of decisions, not a simple linear hierarchy.

### Definition 1.3: Strategic Scope

Van den Steen defines **strategy scope** as:

$$S = \{d_i : d_i \text{ is strategic}\}$$

The key theorem: $|S| \ll n$. Strategy is a small set; most decisions are operative.

**Why?** Because if too many decisions are strategic, they cannot all be coordinated. Humans/organizations have limited attention.

---

## Part 2: The Universal 4-Level Hierarchy

From Van den Steen's theory, a universal 4-level hierarchy emerges:

### Level 0: Meta-Meta-Decisions

**Definition:** Decisions that determine what counts as a relevant decision in the first place.

**Characteristics:**
- Scope-defining
- Often taken as given/exogenous
- Highest irreversibility (but irreversibility is not what makes them strategic)

**Examples:**

| Context | L0 Decision |
|---------|-------------|
| Organization | "Are we in business X (e.g., automotive, pharma)?" |
| Organization | "Do we operate in market economy or planned?" |
| Household | "What is our primary life goal (career, family, leisure)?" |
| Household | "Do we operate as nuclear or extended family?" |
| Nation | "Do we use market mechanisms or state planning?" |
| Nation | "What is our primary identity (nation-state, federation, empire)?" |
| Individual | "What domain are we changing (health, career, relationships)?" |
| Intervention | "What is the target behavior (smoking, exercise, savings)?" |

**Key Property:** Changing L0 is rarely attempted without external shock. Stable over years/decades.

---

### Level 1: Strategic Root Decisions

**Definition:** Few (typically 2-5), persistent choices with **high interaction density**. Other choices optimally align to them.

**Characteristics (from Van den Steen):**
- **High interaction density:** Changing one forces changes in many others
- **High persistence:** Not easily revisable (though not necessarily irreversible)
- **Coordination effect:** Value comes from alignment, not optimization of the single choice alone

**Examples:**

| Context | L1 Decision | Why Strategic? |
|---------|------------|----------------|
| Organization | "Cost-leadership vs. premium/differentiation" | Determines supply chain, R&D spending, marketing, hiring |
| Organization | "Diversified vs. focused?" | Determines governance structure, capital allocation |
| Household | "Career-primary vs. family-primary?" | Determines time allocation, location, financial priorities |
| Household | "Urban vs. rural?" | Determines commute, school choices, social network |
| Nation | "Export-driven economy vs. domestic-focused?" | Determines trade policy, currency policy, education system |
| Nation | "Tech leader vs. tech follower?" | Determines R&D investment, education priorities, regulation |
| Individual (Health) | "Intensive cessation vs. harm reduction?" | Determines pharmacology, counseling, social support structure |
| Individual (Career) | "Build expertise (deep) vs. build networks (broad)?" | Determines time allocation, projects, social investment |
| Intervention | "Aggressive transformation vs. maintenance?" | Determines resource intensity, timeline, stakeholder engagement |

**Formal Property:** If L1 has $k$ elements, then at least $k(k-1)/2$ high-order complementarity terms exist.

---

### Level 2: Derived Strategic Decisions

**Definition:** Many choices that are **strategically relational** to L1. They remain somewhat discretionary, but they must cohere with L1.

**Characteristics:**
- Dependent on L1 choices
- May have local autonomy (L2a, L2b, L2c can vary independently from each other)
- But must not contradict L1
- Number and nature vary based on L1 complexity and context

**Examples (for L1 = "Cost-Leadership"):**

| Sub-Decision | Nature | Constraints | Discretion |
|--------------|--------|-------------|-----------|
| Supply chain structure | L2a | Must minimize cost; must be reliable | Where to source (which countries)? |
| Manufacturing process | L2b | Must enable scale; must minimize defects | Automation level? |
| Workforce strategy | L2c | Must minimize labor cost; must enable flexibility | Contractor vs. employee balance? |
| Product design | L2d | Must minimize part count; maximize standardization | Which platforms? |
| Geographic footprint | L2e | Must optimize for cost/access | Which countries/regions? |

**Key Property:** $|L2| \gg |L1|$. L2 decisions are many.

---

### Level 3: Operative Decisions

**Definition:** High-specificity, low-interaction decisions. Usually made in real-time without strategic review.

**Characteristics:**
- **Fully determined** (or nearly so) by L2 choices
- **High specificity:** Context-dependent, detailed choices
- **Low guiding-effect:** Changing one rarely affects others
- **High frequency:** Made repeatedly (often daily/weekly)

**Examples:**

| Context | L3 Decision |
|---------|-------------|
| Organization | "Which specific vendor for office supplies?" |
| Organization | "What should Q3 marketing budget be?" (given L1, L2 already determine approximate level) |
| Household | "Which restaurant for dinner?" |
| Household | "What brand of toothpaste?" |
| Nation | "Interest rate adjustment (0.25\% up or down)?" (given L1, L2 already determine the broad policy) |
| Intervention | "Should incentive be \$50 or \$75?" (given L1, L2 already determine "incentive-based," just not the amount) |

**Key Property:** L3 decisions are made by local units/individuals without central strategic review.

---

## Part 3: Why This Hierarchy is Universal

Van den Steen's theory implies the hierarchy is **context-universal** because it derives from a single principle: **complementarity and coordination.**

### Proof Sketch

1. **Premise:** In any coordinated system, agents make decisions, and some decisions interact (complement).

2. **Definition:** A decision is strategic iff others align to it.

3. **Theorem:** As interaction density increases, a hierarchy emerges with strategic decisions at the root.

4. **Corollary:** This hierarchy has the same 4-level structure regardless of context because:
   - L0 always exists (what domain are we in?)
   - L1 always has small cardinality (bounded rationality)
   - L2 always has large cardinality (consequences of L1)
   - L3 always has high specificity (local implementation)

### Universal Examples

**Organization (Tech Startup):**
- L0: "Are we a software company?"
- L1: "Cheap commodity software (e.g., open-source wrapper) vs. premium AI-powered solution?"
- L2: "Type of go-to-market" "API-first vs. UI-first" "Freemium vs. enterprise"
- L3: "Which CRM tool" "What pricing per user"

**Nation (Carbon Neutrality Commitment):**
- L0: "Do we use market mechanisms or state direction?"
- L1: "Tech-driven transition (markets, innovation) vs. behavior-driven (rationing, mandates)?"
- L2: "Carbon tax / cap-and-trade vs. subsidies" "Renewable mix (solar, wind, nuclear)" "Transport: EV vs. public transit vs. walkability"
- L3: "EV tax credit: \$5k or \$10k?" "Solar panel rebate percentage"

**Household (Life Planning):**
- L0: "Are we a two-income or one-income household?"
- L1: "Career-primary vs. family-primary?"
- L2: "Childcare strategy" "Geographic location" "Education philosophy"
- L3: "Which school to choose" "Which job offer to take"

---

## Part 4: Strategic Coherence and Misalignment

### Definition 4.1: Coherence

A system is **coherent** if all L2 decisions reinforce the L1 strategic roots.

**Formally:**

$$\text{Coherent} \Leftrightarrow \forall i,j \in L2: \gamma_{ij} \geq \gamma_{min}$$

where $\gamma_{ij}$ is the complementarity between L2 decision $i$ and $j$, and $\gamma_{min}$ is a context-dependent threshold.

### Definition 4.2: Incoherence

A system exhibits **incoherence** when L2 decisions contradict or fail to reinforce each other.

**Examples of Incoherence:**

| L1 Choice | Incoherent L2 | Why Incoherent |
|-----------|--------------|----------------|
| "Cost-leadership" | "Hire only PhDs" | PhDs demand high salaries; undermines cost |
| "Aggressive transformation" | "Minimal change management" | No one understands new direction; transformation fails |
| "Career-primary" | "Have children" (without support infrastructure) | Forces constant context-switching; career and family both suffer |
| "Intensiveintervention" | "Minimal budget" | Cannot execute; design and resource misaligned |

### Consequence: Efficiency Loss

Van den Steen shows that misalignment causes **efficiency losses of 30-80%** depending on severity:

$$\text{Efficiency} = 1 - \sum_i \alpha_i \cdot |\text{Incoherence}_i|$$

where $\alpha_i$ are weights for each L2 choice.

---

## Part 5: Determining L2 Complexity (Number of Sub-Decisions)

The number of L2 sub-decisions depends on:

### Factor 1: L1 Complexity

**Simple L1** (binary choice, e.g., "Cost vs. premium"): 3-4 L2 decisions
**Complex L1** (multi-dimensional, e.g., "Aggressive transformation with 5 dimensions"): 8-12 L2 decisions

### Factor 2: Context Heterogeneity

**Homogeneous context** (single stakeholder, one site): Fewer L2 decisions needed
**Heterogeneous context** (multiple nations, multiple stakeholders, conflicting interests): More L2 decisions needed

### Factor 3: Coupling Strength

**Tightly coupled** (e.g., manufacturing line): Changes in one place immediately affect others; fewer L2 decisions (just one sequence)
**Loosely coupled** (e.g., multi-country federation): Changes can be somewhat independent; more L2 decisions

### Empirical Ranges

| Context | Typical L2 Count | Ranges |
|---------|-----------------|--------|
| Individual decision | 2-4 | Simple (2) to Complex (4+) |
| Team decision (5-20 people) | 3-6 | Simple (3) to Complex (6+) |
| Organization (100-1000 people) | 5-10 | Simple (5) to Complex (10+) |
| Multi-org (10-1000 org) | 8-15 | Simple (8) to Complex (15+) |
| Nation (millions) | 10-20+ | Complex (15+) to Very complex (20+) |

---

## Part 6: Application to Behavioral Intervention Design

### Level 0: Scope
"What behavior are we targeting?" (e.g., smoking cessation, exercise, savings)

### Level 1: Strategic Roots (2-3 typical)

**Example for smoking:**
- L1a: "Intensive pharmacological support vs. behavioral support vs. minimal intervention"
- L1b: "Cold-turkey cessation vs. gradual reduction" (if allowed by health model)

**Example for organizational transformation:**
- L1a: "Disruption-tolerant (accept chaos) vs. disruption-minimizing (maintain operations)"
- L1b: "Top-down (CEO-driven) vs. distributed (bottom-up adoption)"

### Level 2: Derived Strategic Decisions (5-10 typical)

**For smoking L1 = "Intensive pharmacological + cold-turkey":**
- L2a: "Pharmacological agent: nicotine replacement vs. bupropion vs. varenicline"
- L2b: "Counseling intensity: weekly vs. monthly vs. on-demand"
- L2c: "Social support: group vs. individual vs. family-based"
- L2d: "Incentive structure: reward-based vs. penalty-based vs. neutral"
- L2e: "Monitoring frequency: daily vs. weekly vs. monthly"
- L2f: "Quit date strategy: fixed date vs. flexible"

### Level 3: Operative Decisions

- "What is the exact dose of varenicline?"
- "Which day/time for counseling sessions?"
- "What is the incentive amount in dollars?"

---

## Part 7: Decision Hierarchy vs. Fixed Org Charts

### Common Mistake

Confusing **organizational hierarchy** (CEO > VP > Manager > Analyst) with **decision hierarchy** (L0 > L1 > L2 > L3).

### Key Difference

- **Org hierarchy:** Describes reporting lines and authority
- **Decision hierarchy (Van den Steen):** Describes which decisions guide other decisions

**Example:** In a startup, the CEO makes both L1 (strategic root) and L3 (which vendor?) decisions. In a large company, L1 is made by C-suite; L3 is made by procurement manager.

**Same hierarchy structure; different role distribution.**

---

## Part 8: Practical Decision Tree for Practitioners

### How to Classify a Decision

```
Is the decision scope-defining (what domain are we in)?
├─ YES → L0
└─ NO:
  Does it have high interaction density with many other decisions?
  ├─ YES → Is it more fundamental than most others?
  │        ├─ YES → L1 (Strategic Root)
  │        └─ NO → L2 (Derived Strategic)
  └─ NO → L3 (Operative)
```

### How to Determine L1 for Your Context

Ask:
1. What are the 2-3 choices that, if changed, would require rethinking almost everything else?
2. If we flip this choice, how many other decisions are affected?
3. Is this choice relatively stable over time (persistent)?

If all three are "many/yes," then it's likely L1.

---

## Part 9: Connection to EBF Frameworks

### How Van den Steen Fits EBF

| EBF Concept | Van den Steen Relevance |
|-------------|------------------------|
| Complementarity (Appendix B) | IS the mechanism that creates hierarchy |
| Decision layers (Ch15) | Are the L2 sub-decisions emanating from L1 roots |
| Coherence (Ch15) | Requires all L2 to reinforce L1 |
| Equilibrium (Appendix BB) | Assumes L1-L2-L3 coherence; if incoherent, equilibrium degrades |
| Willingness (Appendix AV) | More likely when decision hierarchy is coherent |

### Why This Matters

Understanding decision hierarchy prevents a common intervention failure:

**Mistake:** Designing L2 interventions (counseling, incentives, reminders) without clarifying L1 (what exactly are we trying to achieve?).

**Correct:** Start with L0-L1 clarity. L2-L3 designs emerge naturally from L1.

---

## Part 10: Open Questions

1. **Adaptive hierarchies:** Can L1 change during implementation? Under what conditions?

2. **Cross-level communication:** When L2 discovers that L1 is misaligned, how does feedback work?

3. **Quantifying complementarity:** How to measure $\gamma_{ij}$ in practice?

4. **Multi-stakeholder L1:** When different stakeholders have different L1 preferences, how to resolve?

5. **Computational hierarchy:** Can we algorithmically detect L1 from data?

---

## References

**Primary:**
- Van den Steen, E. (2017). "A Formal Theory of Strategy." Management Science, 63(8), 2616–2636.

**Secondary:**
- Milgrom, P. & Roberts, J. (1990, 1995). "Complementarities and fit: Strategy, structure, and organizational change in manufacturing." Journal of Accounting and Economics.
- Roberts, J. (2004). *The Modern Firm: Organizational Design for Performance and Growth*. Oxford University Press.
- Hart, O. & Moore, J. (1990). "Property rights and the nature of the firm." Journal of Political Economy.

---

**Version:** 1.1
**Last Updated:** January 12, 2026
**Author:** BEATRIX Research Group
