# Capturing the Complexity of Human Strategic Decision-Making with Machine Learning

**Authors:** Jian-Qiao Zhu, Joshua C. Peterson, Benjamin Enke, Thomas L. Griffiths
**Affiliations:** Princeton University, Boston University, Harvard University & NBER
**Paper-ID:** PAP-zhu2024complexity
**Article Type:** Experimental + Machine Learning
**Archived:** 2026-02-04

---

## Abstract

Understanding how people behave in strategic settings–where they make decisions based on their expectations about the behavior of others–is a long-standing problem in the behavioral sciences. We conduct the largest study to date of strategic decision-making in the context of initial play in two-player matrix games, analyzing over 90,000 human decisions across more than 2,400 procedurally generated games that span a much wider space than previous datasets. We show that a deep neural network trained on these data predicts people's choices better than leading theories of strategic behavior, indicating that there is systematic variation that is not explained by those theories. We then modify the network to produce a new, interpretable behavioral model, revealing what the original network learned about people: their ability to optimally respond and their capacity to reason about others are dependent on the complexity of individual games. This context-dependence is critical in explaining deviations from the rational Nash equilibrium, response times, and uncertainty in strategic decisions. More broadly, our results demonstrate how machine learning can be applied beyond prediction to further help generate novel explanations of complex human behavior.

**Keywords:** Behavioral Game Theory, Large Scale Experiment, Machine Learning, Behavioral Economics, Complexity

---

## 1. Introduction

Strategic decision-making is essential when people's outcomes depend on both their own and other people's actions. As a consequence, it is an important topic in various disciplines within the social sciences, including economics, psychology, political science, and artificial intelligence, as well as cultural and biological evolution.

The most widely studied type of game in the social sciences is the class of 2×2 matrix games, which have been found to illuminate behavior in contexts including:
- Human cooperation and the evolution of morality
- Price setting and production decisions by firms
- The coordination of investment decisions
- The positioning of political candidates

### The Nash Equilibrium Problem

The rational model of strategic decisions – the Nash equilibrium – is based on two key assumptions:
1. Mutual consistency in beliefs about opponents' strategies
2. Mutual rationality in best responding to those beliefs

However, research has shown that human players often violate both of these assumptions. This has prompted the development of **behavioral game theory**, which has identified various extensions and refinements that produce a closer match to human decisions.

### The Dataset Gap

Despite a proliferation of behavioral models, evaluating their performance has relied on relatively small datasets based on a select group of games. Our study addresses this with:
- **2,416 procedurally generated games** (17-fold increase over largest prior meta-analysis)
- **93,460 human decisions**
- Dense sampling of the game space

---

## 2. Methods

### 2.1 Game Generation Algorithm

We employed Robinson and Goforth's topology for 2×2 games, which is constructed using ordinal order graphs of payoffs. Each player has 12 unique order graphs, resulting in 12×12 = 144 possible game types.

**Generated dataset:**
- 1,208 base games × 2 player perspectives = 2,416 game instances
- Payoffs as integers in range [1, 50]
- All games have at least one pure-strategy Nash equilibrium

### 2.2 Participants

- **N = 4,900** recruited via Prolific Academic
- **N = 4,673** completed the experiment
- Ages 18-86 (median = 37)
- 20 games per participant
- Compensation: $2.00 base + up to $0.50 bonus

### 2.3 Procedure

- No feedback between games
- Random rematching after each game
- Observed behaviors interpreted as **initial game play strategies**
- Row/column permutations randomized

---

## 3. Models

### 3.1 Context-Invariant Models

Models with parameters that remain constant across different games:

**Nash Equilibrium:** Pure-strategy Nash equilibrium (PSNE) predictions

**Level-k Model:** Players at level k assume opponents are at level k-1
- Level-0: Random play
- Level-1: Best response to random
- Level-k: Best response to level-(k-1)

**Quantal Response Equilibrium (QRE):** Players respond to expected payoffs probabilistically:

$$p(A) = \frac{1}{1 + e^{-\eta_{self}[EU(A) - EU(B)]}}$$

Where η_self governs the player's noisiness (inverse temperature).

**Level-k Quantal Response:** Combines level-k thinking with noisy responding

**Level-k QR + Belief Noise:** Allows η_self ≠ η^s_other (different beliefs about opponent's noisiness)

### 3.2 Context-Dependent Models

Models where parameters vary based on game characteristics:

**Multilayer Perceptron (MLP):** Direct prediction of choice probabilities from game matrix
- 3 hidden layers, 300 neurons each
- Serves as upper bound benchmark

**Neural Quantal Response:** η_self = f_MLP(game matrix)

**Neural Belief Noise:** η^s_other = f_MLP(game matrix)

**Full Neural Model:** All parameters (k distribution, η_self, η^s_other) predicted by neural networks

---

## 4. Results

### 4.1 Model Completeness

Completeness measures how well a model approximates the neural network upper bound from a starting point of random play.

| Model | Completeness |
|-------|-------------|
| Random | 0% (lower bound) |
| Nash Equilibrium | 24% |
| L1 + QR + Risk | 82% |
| **L2 + Neural QR + Neural Belief** | **96%** |
| **Full Neural Model** | **97%** |
| MLP | 100% (upper bound) |

**Key Finding:** Context-dependent models (with neural network components) substantially outperform context-invariant models.

### 4.2 What Drives Context-Dependence?

The neural network learns that:
1. **η_self varies by game** - Players are more noisy in some games than others
2. **η^s_other varies by game** - Beliefs about opponent noisiness are context-dependent
3. **η_self has larger effect** - Own response optimization varies more than beliefs about others

### 4.3 Behavioral Attenuation

When splitting games by median estimated η_self:
- **Low noisiness games:** Strong link between EU difference and choice frequency
- **High noisiness games:** Compressed link (attenuation)

---

## 5. Complexity Index

### 5.1 Development

Using LASSO regression on game features predicting η_self from the Level-2 Neural QR + Neural Belief Noise model:

| Game Feature | Effect on -η_self |
|--------------|------------------|
| Nash Equilibrium Payoff Dominance | **-0.80** (reduces complexity) |
| Inequality in Payouts | **+0.85** (increases complexity) |
| Payoff Variance (self) | +0.40 |
| Levels of Iterative Rationality | +0.38 |
| Max Payout (self) | +0.30 |
| Excess Dissimilarity (self) | +0.28 |

### 5.2 Validation (Main Experiment)

**Complexity-Response Time Correlation:**
- Pearson's r = 0.21, p < .01
- Higher complexity → longer deliberation

### 5.3 Validation (Preregistered Follow-up)

**N = 1,008 participants, 500 new games**

| Measure | Correlation with Complexity |
|---------|---------------------------|
| Response Time | r = 0.23, p < .01 |
| Cognitive Uncertainty | r = 0.24, p < .01 |

**Key Finding:** Complexity index predicts both behavioral (RT) and subjective (uncertainty) measures out-of-sample.

---

## 6. Discussion

### 6.1 Main Contributions

1. **Context-dependence matters:** Behavioral parameters are not fixed but vary with game complexity
2. **Interpretable complexity index:** Based on objective game features, generalizable
3. **ML for theory generation:** Neural networks reveal patterns, then translated to interpretable models

### 6.2 Features That Drive Complexity

**Reduce Complexity (Easier Games):**
- Dominant solvability
- Nash equilibrium payoff dominance
- Pure motives (coordination or zero-sum)

**Increase Complexity (Harder Games):**
- Excess dissimilarity (tradeoff difficulty)
- Multiple equilibria
- Iterative reasoning requirements
- Payoff inequality/asymmetry

### 6.3 Implications

The results illustrate that:
- Players' ability to optimally respond depends on game complexity
- Players' capacity to reason about others depends on game complexity
- Both effects are captured by context-dependent η parameters

---

## Key Parameters Extracted (EBF Integration)

| Parameter | Value | Source |
|-----------|-------|--------|
| Total Decisions | 93,460 | Dataset |
| Total Games | 2,416 | Dataset |
| Total Participants | 4,900 | Dataset |
| Nash Completeness | 24% | Model comparison |
| Best Context-Invariant | 82% | L1+QR+Risk |
| Best Context-Dependent | 97% | Full Neural |
| Complexity-RT (main) | r = 0.21 | Validation |
| Complexity-RT (followup) | r = 0.23 | Validation |
| Complexity-Uncertainty | r = 0.24 | Validation |
| Payoff Dominance → η | -0.80 | LASSO |
| Inequality → η | +0.85 | LASSO |
| Dissimilarity → η | +0.28 | LASSO |
| Iterative Rationality → η | +0.38 | LASSO |

---

## EBF Framework Relevance

### Context-Dependence (Ψ) Validation

This paper provides **direct experimental evidence** that behavioral parameters vary with context:

```
CONTEXT-INVARIANT MODELS:        CONTEXT-DEPENDENT MODELS:
────────────────────────         ────────────────────────
η_self = constant                η_self = f(game complexity)
η_other = constant               η_other = f(game complexity)

Max Completeness: 82%            Max Completeness: 97%

Missing: 18% of variation        Missing: Only 3% of variation
```

**EBF Implication:** The Ψ framework's assumption that context modulates behavioral parameters is empirically validated.

### Complexity as Moderator

The complexity index maps directly to EBF's context dimensions:

| Complexity Feature | EBF Dimension |
|--------------------|---------------|
| Payoff Dominance | Ψ_I (Institutional) |
| Iterative Rationality | Ψ_C (Cognitive Load) |
| Inequality | Ψ_S (Social/Fairness) |
| Dissimilarity | Ψ_C (Trade-off Difficulty) |

### ML + Behavioral Economics

The methodology demonstrates:
1. Use ML to discover unexplained variation
2. Identify which parameters are context-dependent
3. Extract interpretable features
4. Build new theoretical model

This parallels the LLMMC approach in EBF.

---

## References

Baker et al. (2017). Nature Human Behaviour.
Camerer (2011). Behavioral game theory. Princeton.
Crawford et al. (2013). Journal of Economic Literature.
Enke & Graeber (2023). Quarterly Journal of Economics.
Enke & Shubatt (2023). NBER Working Paper.
Fehr & Schmidt (1999). Quarterly Journal of Economics.
Fudenberg & Liang (2019). American Economic Review.
McKelvey & Palfrey (1995). Games and Economic Behavior.
Peterson et al. (2021). Science.
Robinson & Goforth (2005). The topology of 2x2 games.
Wright & Leyton-Brown (2017). Games and Economic Behavior.

---

*Full text archived for EBF Framework reference*
*Content Level: L3 (complete with supplementary information)*
*Evidence Tier: 2 (Large-scale experiment, strong methodology)*
*Supported by: NOMIS Foundation*
