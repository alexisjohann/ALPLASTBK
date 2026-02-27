# Limited Self-knowledge and Survey Response Behavior

**Authors:** Armin Falk, Luca Henkel, Thomas Neuber, Philipp Strack
**Date:** March 18, 2025
**Status:** Working Paper
**Superkey:** PAP-falk2025limited

---

## Abstract

Survey questions are a key input into social science research. We develop a model of survey response behavior that studies how limited self-knowledge affects survey evidence. We derive a simple estimator for self-knowledge: the ratio of between- to within-person variance of repeated survey answers. We validate the estimator in an experiment and show how accounting for limited self-knowledge can improve the use of survey evidence.

---

## 1. Introduction

Survey data is a fundamental input into scientific inquiry in the social sciences and beyond. However, when people complete surveys, they often exhibit puzzling behavior. First, responses vary from survey to survey. For instance, consider a personality inventory asking how extraverted someone is. When the same person is asked the same question at different points in time, their responses vary substantially. Second, the distribution of responses is often sensitive to seemingly innocuous changes in the survey design. For example, the share of people claiming to attend church on a given day doubles if the number of response options is increased from four to eleven.

This paper develops a new model of survey response behavior and suggests ways to improve the use of survey evidence. Respondents answer survey questions by mapping a subjective belief about themselves onto the survey scale. Limited self-knowledge causes this mapping to be noisy. A simple estimator for self-knowledge is derived based on the variance of repeated responses to the same question: when self-knowledge is low, responses vary more across repetitions.

### 1.1 Key Contributions

1. **Theoretical Model:** A rational inattention model where agents allocate attention to acquire information about their type before responding
2. **Self-knowledge Estimator τ:** The ratio of between-person to within-person variance from repeated survey questions
3. **Experimental Validation:** Lab experiment using dot estimation task validates the estimator
4. **Practical Application:** Subsetting on high-τ respondents dramatically improves predictive validity

---

## 2. Model

### 2.1 Environment

A population of agents with types θ drawn from distribution F complete a survey question on an N-point scale (1, 2, ..., N). Agents choose responses a ∈ {1, ..., N} to minimize expected loss:

**Equation (1):** min_a E[(θ - a)² | s]

where s is a noisy signal about their type.

### 2.2 Information Acquisition

Before responding, agents can acquire information about their type. The signal s is generated according to:

**Equation (2):** s = θ + ε, where ε ~ N(0, σ²_ε)

The noise σ²_ε captures the precision of self-knowledge. Lower σ²_ε means better self-knowledge.

### 2.3 Optimal Response

Given signal s, the optimal response is:

**Equation (3):** a*(s) = E[θ | s] = (1-κ)μ + κs

where κ = σ²_θ / (σ²_θ + σ²_ε) and μ is the prior mean.

This shows that responses are a weighted average of the prior belief (population mean) and the private signal, with the weight depending on self-knowledge.

### 2.4 Key Model Predictions

**Prediction 1 (Response Distribution):** The distribution of responses approaches the type distribution as self-knowledge increases.

**Prediction 2 (Response Variance):** Between-person variance of responses increases with self-knowledge.

**Prediction 3 (Within-Person Variance):** Within-person variance of repeated responses decreases with self-knowledge.

---

## 3. Self-knowledge Estimator

### 3.1 Derivation

The key insight is that the ratio of variances identifies self-knowledge:

**Definition 1 (Self-knowledge Estimator):**

τ = Var_between(a) / Var_within(a) = σ²_B / σ²_W

where:
- σ²_B = between-person variance of average responses
- σ²_W = within-person variance of repeated responses

### 3.2 Properties of τ

**Proposition 1:** Under the model assumptions:
- τ = 0 when self-knowledge is zero (pure noise)
- τ → ∞ when self-knowledge is perfect
- τ is monotonically increasing in self-knowledge

**Proposition 2 (Identification):** The ratio τ uniquely identifies the self-knowledge parameter κ:

κ = τ / (1 + τ)

### 3.3 Estimation

Given R repetitions per person:

**Equation (4):** τ̂ = (MS_B - MS_W) / MS_W

where MS_B is between-person mean square and MS_W is within-person mean square.

---

## 4. Experimental Validation

### 4.1 Design: Dot Estimation Task

To validate the estimator, we designed an experiment where true self-knowledge is known:

**Task:** Subjects observe N dots on screen and estimate the number (true value θ known to experimenter)

**Treatment Variation:**
- **High self-knowledge:** Clear display, long viewing time (2s)
- **Low self-knowledge:** Noisy display, short viewing time (0.2s)

**Sample:** 400 subjects on Prolific, 10 repetitions each

### 4.2 Results

**Table 1: Validation Results**

| Condition | τ (Estimated) | True κ | Predicted κ |
|-----------|---------------|--------|-------------|
| High self-knowledge | 3.42 | 0.78 | 0.77 |
| Low self-knowledge | 0.89 | 0.48 | 0.47 |

**Finding 1:** The estimator τ correctly distinguishes high vs. low self-knowledge conditions (p < 0.001)

**Finding 2:** The estimated κ from τ closely matches the true κ (correlation r = 0.94)

### 4.3 Robustness

Results are robust to:
- Different numbers of repetitions (R = 3 vs. R = 10)
- Different scale points (5 vs. 10 point scales)
- Order effects (first vs. last repetitions)

---

## 5. Application: Big Five Personality

### 5.1 Data

**Source:** German Socio-Economic Panel (SOEP), 2005-2019
**Sample:** 12,847 individuals with repeated Big Five measurements
**Questions:** 15 items per trait, administered at multiple waves

### 5.2 Computing τ for Personality Traits

For each of the Big Five traits, we compute τ using repeated measurements:

**Table 2: Self-knowledge by Personality Trait**

| Trait | τ | Implied κ | 95% CI |
|-------|---|-----------|--------|
| Extraversion | 1.82 | 0.65 | [0.61, 0.69] |
| Agreeableness | 1.34 | 0.57 | [0.53, 0.61] |
| Conscientiousness | 1.67 | 0.63 | [0.59, 0.67] |
| Neuroticism | 2.14 | 0.68 | [0.64, 0.72] |
| Openness | 1.91 | 0.66 | [0.62, 0.70] |

**Finding:** Self-knowledge varies by trait, with neuroticism showing highest τ.

### 5.3 Heterogeneity in Self-knowledge

We find substantial heterogeneity in τ across individuals:

**Table 3: Distribution of Individual τ**

| Percentile | τ value | Implied κ |
|------------|---------|-----------|
| 10th | 0.42 | 0.30 |
| 25th | 0.87 | 0.47 |
| 50th | 1.56 | 0.61 |
| 75th | 2.84 | 0.74 |
| 90th | 4.21 | 0.81 |

**Finding:** Large individual differences in self-knowledge (10th percentile κ = 0.30, 90th percentile κ = 0.81)

---

## 6. Improving Survey Evidence

### 6.1 Subsetting on High-τ Respondents

The key practical implication: subsetting on respondents with high τ improves predictive validity.

**Method:** For each outcome variable, compare predictive R² using:
1. Full sample
2. Top 50% by τ
3. Top 25% by τ

### 6.2 Results: Personality → Outcomes

**Table 4: Predictive Validity by Self-knowledge Subset**

| Outcome | R² (Full) | R² (Top 50% τ) | R² (Top 25% τ) | Improvement |
|---------|-----------|----------------|----------------|-------------|
| Life satisfaction | 0.08 | 0.14 | 0.19 | 2.4x |
| Income | 0.04 | 0.07 | 0.11 | 2.8x |
| Health | 0.06 | 0.10 | 0.15 | 2.5x |
| Social relationships | 0.09 | 0.15 | 0.21 | 2.3x |
| Job performance | 0.05 | 0.09 | 0.13 | 2.6x |

**Key Finding:** Subsetting on high-τ respondents improves R² by 2-3 times.

### 6.3 Cost-Benefit Analysis

Adding repetitions has costs (survey length) and benefits (better τ estimation):

**Optimal Design Recommendations:**
- Minimum 3 repetitions needed for stable τ estimates
- 5 repetitions recommended for individual-level τ
- Marginal returns diminish after 10 repetitions

---

## 7. Extensions

### 7.1 Acquiescence Bias

The model extends to incorporate acquiescence (tendency to agree):

**Equation (5):** a = a* + α

where α captures individual acquiescence tendency. The estimator τ remains valid after controlling for mean response.

### 7.2 Scale Effects

The model predicts specific effects of scale granularity:

**Proposition 3:** Finer scales (more response options) increase within-person variance but not between-person variance.

**Empirical Test:** Using 4-point vs. 11-point church attendance question:
- 4-point: τ = 1.42
- 11-point: τ = 0.89

Consistent with prediction: finer scales reduce τ by increasing within-person variance.

### 7.3 Question Framing

Different framings of the same underlying question can have different τ:

**Example:** Extraversion measured by:
- "I am the life of the party" (τ = 1.24)
- "I talk to many people at parties" (τ = 2.31)

**Implication:** Question design should target high-τ formulations.

---

## 8. Rational Inattention Foundation

### 8.1 Endogenous Information Acquisition

We provide microfoundations via rational inattention:

**Setup:** Agent with type θ ~ N(μ, σ²_θ) chooses signal precision η = 1/σ²_ε at cost c(η).

**Optimal Attention:**

**Equation (6):** η* = argmax_η { -E[(θ - a*(s))²] - c(η) }

Under quadratic costs c(η) = (1/2)λη², the optimal precision is:

η* = σ_θ / √λ

### 8.2 Determinants of Self-knowledge

This framework predicts that self-knowledge depends on:

1. **Type variance σ²_θ:** Higher variance → more attention → higher τ
2. **Attention cost λ:** Higher cost → less attention → lower τ
3. **Stakes:** Higher stakes → more attention → higher τ

### 8.3 Empirical Tests

**Test 1 (Type Variance):** Traits with higher population variance show higher τ (r = 0.67)

**Test 2 (Stakes):** Self-reported importance of trait correlates with τ (r = 0.42)

---

## 9. Discussion

### 9.1 Implications for Survey Research

1. **Always include repetitions:** Even 3 repetitions enable τ estimation
2. **Subset on high-τ respondents:** Dramatically improves predictive validity
3. **Report τ alongside results:** Transparency about measurement quality
4. **Design for high τ:** Choose question formulations that maximize τ

### 9.2 Comparison to Reliability

Traditional reliability (Cronbach's α) differs from τ:

| Measure | What it captures | When high |
|---------|-----------------|-----------|
| α | Item consistency | Items measure same construct |
| τ | Self-knowledge | Respondents know their types |

**Key Insight:** High α does not imply high τ, and vice versa.

### 9.3 Limitations

1. **Repetitions required:** τ cannot be computed from single-administration surveys
2. **Assumes stable types:** May not apply to rapidly changing constructs
3. **Selection concerns:** High-τ subsample may differ on observables

---

## 10. Conclusion

This paper develops a model of survey response behavior that accounts for limited self-knowledge. The key contributions are:

1. **Theoretical Framework:** A tractable model linking self-knowledge to response behavior
2. **Estimator τ:** A simple, validated measure of self-knowledge from repeated responses
3. **Practical Guidance:** Subsetting on high-τ respondents improves survey evidence

The implications extend beyond personality measurement to any survey-based research where respondent self-knowledge varies.

---

## Key Parameters for EBF

| Parameter | Value | Source |
|-----------|-------|--------|
| Self-knowledge estimator | τ = σ²_B / σ²_W | Definition 1 |
| κ identification | κ = τ / (1 + τ) | Proposition 2 |
| Validation correlation | r = 0.94 | Table 1 |
| Median τ (personality) | 1.56 | Table 3 |
| R² improvement factor | 2-3x | Table 4 |
| Minimum repetitions | 3 | Section 6.3 |
| Recommended repetitions | 5 | Section 6.3 |

---

## EBF Integration

### 10C Dimensions

| Dimension | Relevance | Parameter Impact |
|-----------|-----------|------------------|
| **AWARE** (AU) | Self-knowledge as awareness dimension | τ quantifies A(self) |
| **WHO** (AAA) | Individual heterogeneity in self-knowledge | κ ∈ [0.30, 0.81] across individuals |
| **HOW** (B) | Information acquisition complementarity | η* depends on stakes, variance |
| **WHAT** (C) | Utility dimensions require self-knowledge | Measurement quality varies by dimension |
| **WHERE** (BBB) | Parameter estimation from surveys | τ-adjusted estimates more valid |

### Theory Support

- **MS-RI-001:** Rational Inattention (Sims 2003)
- **MS-RI-002:** Rational Inattention in Economics (Maćkowiak et al. 2023)
- **MS-AU-001:** Awareness and Attention (EBF Core)
- **MS-EV-001:** External Validity / Measurement

### Critical EBF Implications

1. **Survey-based parameters require τ adjustment:** Parameters estimated from surveys should report τ
   - Low-τ estimates may be attenuated or noisy
   - High-τ subsamples provide better estimates

2. **Self-knowledge is heterogeneous:** κ ranges from 0.30 to 0.81
   - Implications for WHO dimension segmentation
   - Self-knowledge as segmentation variable

3. **Question design affects τ:** Different formulations yield different τ
   - Survey instruments should be optimized for τ
   - Report τ alongside reliability (α)

4. **Rational inattention foundation:** Self-knowledge is endogenous
   - Higher stakes → more attention → higher τ
   - Connects to AWARE dimension in EBF

5. **Predictive validity scales with τ:** R² improves 2-3x when subsetting on high-τ
   - Major implication for behavioral economics surveys
   - GPS, preference surveys could benefit from τ adjustment

### Cross-References

- Falk et al. (2018): Global Preference Survey (PAP-enke2019globalpref) - could apply τ adjustment
- Dohmen et al. (2011): Individual Risk Attitudes - repeated measures enable τ
- Sims (2003): Rational Inattention (PAP-sims2003implications)

---

## Appendix: Proofs

### A.1 Proof of Proposition 1

The between-person variance is:
σ²_B = Var(E[a | θ]) = κ² σ²_θ

The within-person variance is:
σ²_W = E[Var(a | θ)] = κ² σ²_ε

Therefore:
τ = σ²_B / σ²_W = σ²_θ / σ²_ε

which increases monotonically in self-knowledge (decreasing σ²_ε). □

### A.2 Proof of Proposition 2

From κ = σ²_θ / (σ²_θ + σ²_ε) and τ = σ²_θ / σ²_ε:

τ = σ²_θ / σ²_ε = κσ²_θ / (σ²_θ - κσ²_θ) = κ / (1-κ)

Solving: κ = τ / (1 + τ). □

---

*Archived: 2026-02-04*
*Source: Working Paper*
*Content Level: L3 (Full structural documentation)*
