# What Makes a Rule Complex?

**Author:** Ryan Oprea
**Affiliation:** Department of Economics, University of California, Santa Barbara
**Journal:** American Economic Review
**Volume:** 114, Issue 1, Pages 169-203
**Year:** 2024
**DOI:** 10.1257/aer.20201874
**Paper-ID:** PAP-oprea2024complexity
**Article Type:** Experimental
**Archived:** 2026-02-04

---

## Abstract

I experimentally test what makes a rule complicated. Subjects tasked with implementing 30 rules with varying structure exhibit error rates that are: (i) increasing in states; (ii) increasing in transitions, though at a lower rate than states; (iii) lower for absorbing (compared to transient) rules; (iv) not reduced when rules can be simplified using counting; (v) reduced when rules can be simplified using counting representations; (vi) decreasing in task familiarity; and (vii) higher when subjects must reason through rules rather than physically enact them.

**Keywords:** Complexity, Bounded Rationality, Automata Theory, Rule Implementation, Procedural Costs

---

## 1. Introduction

### The Puzzle of Rule Complexity

Understanding what makes rules complex is fundamental to many areas of economics:
- Tax codes and regulations
- Contract terms
- Policy implementation
- Strategic decision-making

Yet we know little about the cognitive foundations of rule complexity. What structural features make a rule harder to follow?

### Automata Theory Approach

This paper uses finite state automata (FSMs) as a formal language for describing rules. This allows:
1. Precise characterization of rule structure
2. Decomposition into measurable components (states, transitions)
3. Comparison across rules with different structures
4. Testing specific hypotheses about complexity sources

### Main Hypotheses

Based on automata theory and behavioral economics, I test seven hypotheses:

**H1:** Complexity increases in the number of states (s-complexity)
**H2:** Complexity increases in the number of transitions (t-complexity)
**H3:** Absorbing rules are less complex than transient rules
**H4:** Subjects reduce rules to minimal representations
**H5:** Subjects can use counting (PDA) representations when available
**H6:** Familiarity reduces complexity
**H7:** Mental reasoning is more costly than physical enactment

---

## 2. Experimental Design

### 2.1 Overview

- **Subjects:** N = 275 recruited at UC Santa Barbara
- **Task:** Implement 30 different rules
- **Rules:** Vary in states (2-6) and transitions (4-12)
- **Measurement:** Error rates on rule implementation

### 2.2 Rule Structure

Rules are described as finite state automata:
- **States (s):** Memory requirements
- **Transitions (t):** Conditional responses
- **Absorption:** Whether rule has terminal states

Example: A 3-state, 6-transition rule might be:
```
State 1: If input A → Output X, stay in State 1
         If input B → Output Y, go to State 2
State 2: If input A → Output Y, go to State 3
         If input B → Output X, stay in State 2
State 3: If input A → Output X, go to State 1
         If input B → Output Y, stay in State 3
```

### 2.3 Treatments

**Main Experiment (N=180):**
- 30 rules with varying structure
- s ∈ {2, 3, 4, 5, 6}
- t ∈ {4, 6, 8, 10, 12}
- Mix of absorbing and transient rules

**Reasoning Treatment (N=45):**
- Same rules
- Must reason through mentally before responding
- Tests hypothesis 7 (reasoning vs enacting)

**Learning Treatment (N=50):**
- Mix of familiar and unfamiliar rules
- Tests hypothesis 6 (familiarity effect)

### 2.4 Procedure

1. Rule displayed as state diagram
2. Subjects receive sequence of inputs
3. Must produce correct output for each input
4. Error = incorrect output
5. Paid based on accuracy

---

## 3. Results

### 3.1 Main Results (Table 2)

| Variable | Coefficient | SE | Interpretation |
|----------|-------------|-----|----------------|
| States (s) | 0.239 | 0.026 | Each state adds ~24% to error rate |
| Transitions (t) | 0.116 | 0.028 | Each transition adds ~12% to error rate |
| Absorbing | -0.203 | 0.037 | Absorbing rules easier (~1 state equivalent) |

**Key Finding 1:** States generate larger complexity costs than transitions.

**Ratio:** States are about 2x as costly as transitions (0.239/0.116 ≈ 2.1)

**Key Finding 2:** Absorbing rules are significantly easier.

The absorption effect (-0.203) is equivalent to removing about one state from the rule.

### 3.2 Hypothesis Tests

**H1 (States → Complexity): SUPPORTED**
- Each additional state significantly increases error rates
- Effect is large and robust

**H2 (Transitions → Complexity): SUPPORTED**
- Each additional transition increases error rates
- Effect is smaller than states (~half)

**H3 (Absorption Reduces Complexity): SUPPORTED**
- Absorbing rules have significantly lower error rates
- Equivalent to removing ~1 state

**H4 (Efficient Reduction): REJECTED**
- Subjects do NOT reduce rules to minimal representations
- Even when minimal form is much simpler, they don't find it

**H5 (Counting Representations): SUPPORTED**
- When rules can use counting (PDA-like), subjects do use it
- Reduces complexity by ~2 states equivalent

**H6 (Familiarity): SUPPORTED**
- Familiar rules have significantly lower error rates
- Learning effect equivalent to ~2 states

**H7 (Reasoning vs Enacting): SUPPORTED**
- Mental reasoning more costly than physical enactment
- Adds complexity equivalent to ~1.3 states

### 3.3 Extended Model (Table 3)

| Variable | Coefficient | SE | States Equivalent |
|----------|-------------|-----|-------------------|
| States | 0.239 | 0.026 | 1.0 |
| Transitions | 0.116 | 0.028 | 0.5 |
| Absorbing | -0.203 | 0.037 | -0.85 |
| Learning | -0.479 | 0.034 | -2.0 |
| Reasoning | 0.301 | 0.037 | +1.3 |
| Countable | -0.490 | 0.046 | -2.0 |

### 3.4 Structural Estimation (Table 5)

To recover deeper parameters, I estimate a structural model where subjects:
1. Process states sequentially
2. Make errors with probability d per state
3. Learn at rate μ

**Structural Parameters:**
- Per-state cost: d = 0.043 (SE 0.006)
- Learning rate: μ = 0.047 (SE 0.011)

These structural estimates confirm the reduced-form findings.

---

## 4. Discussion

### 4.1 Why States > Transitions?

States represent memory requirements. To implement a rule with s states, subjects must:
1. Track which state they're in
2. Maintain state across inputs
3. Update state based on transitions

Transitions are conditional responses that don't require persistent memory.

### 4.2 Why Absorption Helps?

Absorbing rules have terminal states that simplify processing:
1. Once in terminal state, no need to track further
2. Reduces effective number of states
3. Provides "natural endpoints"

### 4.3 Why No Efficient Reduction?

Despite potential for simplification, subjects don't reduce rules because:
1. Finding minimal representation requires cognitive effort
2. Effort cost may exceed benefit
3. Bounded rationality in rule processing

### 4.4 Why Counting Helps?

When counting representations are available:
1. Leverages natural cognitive ability
2. Reduces state tracking to simple counting
3. Equivalent to "offloading" memory to counting system

---

## 5. Implications

### 5.1 For Policy Design

1. **Minimize states:** Policies with fewer conditions are easier to follow
2. **Use absorption:** One-time actions easier than recurring requirements
3. **Leverage counting:** "3 simple steps" easier than complex branching
4. **Allow learning:** Repeated exposure reduces perceived complexity

### 5.2 For Contract Design

1. Simple contracts with few contingencies are more likely to be followed
2. Default-based contracts (absorbing) reduce complexity
3. Counting-based contracts ("within 3 business days") easier

### 5.3 For Regulation

1. Complex regulations with many conditions generate compliance costs
2. Simplification should focus on reducing states, not transitions
3. Phase-in periods allow learning, reducing effective complexity

---

## Key Parameters Extracted (EBF Integration)

| Parameter | Value | Source | EBF Use |
|-----------|-------|--------|---------|
| State Cost | 0.239 | Table 2 | Ψ_C complexity |
| Transition Cost | 0.116 | Table 2 | Ψ_C complexity |
| Absorption Effect | -0.203 | Table 2 | Ψ_I defaults |
| Learning Effect | -0.479 | Table 3 | Ψ_T temporal |
| Reasoning Effect | 0.301 | Table 3 | Ψ_C cognitive |
| Countable Effect | -0.490 | Table 3 | Ψ_C representation |
| State/Transition Ratio | 2:1 | Derived | Intervention design |
| Structural d | 0.043 | Table 5 | LLMMC prior |
| Structural μ | 0.047 | Table 5 | Learning rate |

---

## EBF Framework Relevance

### Procedural Complexity in Ψ Framework

```
RULE COMPLEXITY DECOMPOSITION:

Total Complexity = f(states, transitions, absorption, familiarity, ...)

                    STATES        TRANSITIONS    ABSORPTION
                    ──────        ───────────    ──────────
Effect Size:        +0.239        +0.116         -0.203
Interpretation:     Memory load   Response rules  Terminal states

                    LEARNING      REASONING      COUNTABLE
                    ────────      ─────────      ─────────
Effect Size:        -0.479        +0.301         -0.490
Interpretation:     Familiarity   Mental effort  PDA representation
```

### Mapping to 10C Dimensions

| Finding | 10C Dimension | Application |
|---------|---------------|-------------|
| States > Transitions | Ψ_C (Cognitive) | Rule design |
| Absorption helps | Ψ_I (Institutional) | Default structure |
| Learning helps | Ψ_T (Temporal) | Sustained engagement |
| Reasoning costly | Ψ_C (Cognitive) | Trial periods |
| Counting helps | Ψ_C (Cognitive) | Simplification |

### SPÖ Application

| Finding | SPÖ Implication |
|---------|-----------------|
| States costly | Simple, clear policies with few conditions |
| Absorption helps | One-time actions easier than recurring |
| Learning helps | Sustained communication > one-shot |
| Reasoning costly | Experience-based campaigns effective |
| Counting helps | "3 pillars" framing reduces complexity |

---

## References

Abreu, D., and A. Rubinstein. 1988. "The Structure of Nash Equilibrium in Repeated Games with Finite Automata." Econometrica 56 (6): 1259–81.

Banks, J., and R. Sundaram. 1990. "Repeated Games, Finite Automata, and Complexity." Games and Economic Behavior 2 (2): 97–117.

Enke, B., and T. Graeber. 2023. "Cognitive Uncertainty." Quarterly Journal of Economics 138 (4): 2021–67.

Gabaix, X. 2014. "A Sparsity-Based Model of Bounded Rationality." Quarterly Journal of Economics 129 (4): 1661–710.

Kalai, E. 1990. "Bounded Rationality and Strategic Complexity in Repeated Games." In Game Theory and Applications, edited by T. Ichiishi, A. Neyman, and Y. Tauman, 131–57. San Diego: Academic Press.

Rubinstein, A. 1986. "Finite Automata Play the Repeated Prisoner's Dilemma." Journal of Economic Theory 39 (1): 83–96.

Simon, H. 1955. "A Behavioral Model of Rational Choice." Quarterly Journal of Economics 69 (1): 99–118.

---

*Full text archived for EBF Framework reference*
*Content Level: L3 (complete with methodology and structural estimation)*
*Evidence Tier: 1 (American Economic Review - Top-5 Economics Journal)*
*Original: American Economic Review, Vol. 114, No. 1, January 2024*
