# What Do People Want?

**Authors:** Daniel J. Benjamin, Kristen B. Cooper, Ori Heffetz, Miles S. Kimball, Tushar Kundu
**Working Paper:** NBER Working Paper No. 33846
**Date:** May 2025
**URL:** http://www.nber.org/papers/w33846
**Superkey:** PAP-benjamin2025want

---

## Abstract

We elicited over a million stated preference choices over 126 dimensions or "aspects" of well-being from a sample of 3,358 respondents on Amazon's Mechanical Turk (MTurk). Our surveys also collected self-reported well-being (SWB) questions about respondents' current levels of the aspects of well-being. From the stated preference data, we estimate relative log marginal utilities per point on our 0-100 response scale for each aspect. We validate these estimates by comparing them to alternative methods for estimating preferences. Our findings provide empirical evidence that both complements and challenges philosophical perspectives on human desires and values. Our results support Aristotelian notions of eudaimonia through family relationships and Maslow's emphasis on basic security needs, yet also suggest that contemporary theories of well-being may overemphasize abstract concepts such as happiness and life satisfaction, while undervaluing concrete aspects such as family well-being, financial security, and health, that respondents place the highest marginal utilities on. We document substantial heterogeneity in preferences across respondents within (but not between) demographic groups, with current SWB levels explaining a significant portion of the variation.

---

## 1. Introduction

Survey data is a fundamental input into scientific inquiry in the social sciences. This paper develops a new model of survey response behavior and suggests ways to improve the use of survey evidence.

### 1.1 Key Research Questions

1. What do people want? (age-old philosophical question)
2. How do marginal utilities vary across aspects of well-being?
3. What drives heterogeneity in preferences?
4. Can stated preferences provide valid estimates of marginal utilities?

### 1.2 Key Contributions

1. **Comprehensive Measurement:** Over 1 million tradeoff choices across 126 aspects
2. **Marginal Utility Estimation:** Hierarchical Bayesian model for relative log marginal utilities
3. **Validation:** Multiple approaches to validate stated preference estimates
4. **Supply-Demand Framework:** Interpretive framework for level-MU relationships
5. **Heterogeneity Analysis:** Within vs. between demographic group variation

---

## 2. Survey Design

### 2.1 Self-Reported Well-Being (SWB) Questions

- 0-100 integer scale (quasi-continuous)
- Endpoint labels: "Lowest level possible" to "Highest level possible"
- Past year timeframe
- Default slider at 50 (must move to confirm)

### 2.2 Tradeoff Questions

Respondents choose between two options, each showing:
- An aspect of well-being
- Direction of change (increase/decrease)
- Magnitude of change (1-8 points)
- Visual slider showing change relative to their reported level

**Key Design Feature:** Starting point for each aspect's change is precisely the level the respondent reported earlier, enabling analysis of how preferences relate to current SWB levels.

### 2.3 Sample

- **Platform:** Amazon Mechanical Turk (MTurk)
- **Collection Period:** June 13 - December 7, 2022
- **Total Respondents:** 5,970 completed Baseline
- **Quality-Controlled Sample:** 3,358 respondents
- **Main Analysis Sample:** 896 respondents (completed first 9 blocks)
- **Total Tradeoffs:** Over 1 million choices
- **Aspects Analyzed:** 126

**Sample Demographics vs. US Population:**
- More likely: college-educated, younger than 50, unemployed
- Less likely: income >$120k, Black, Hispanic/Latino

### 2.4 Aspect Selection Criteria

1. Commonly used in subjective well-being literature
2. Collected by large statistical agencies
3. Comprehensive coverage of potential concerns
4. Represent aspects people regularly trade off

---

## 3. Theoretical Framework

### 3.1 Binary Choice Model

Individual i's level of aspect j: w_ij
Utility function: u_i(w_i)

Change in utility from Δw_ij:
$$\frac{\Delta u_i}{\Delta w_{ij}} \approx M_{ij}$$

where M_ij is marginal utility (m_ij for log MU).

**Choice Rule:** Respondent chooses aspect j over j' iff:
$$m_{ij} - m_{ij'} + \ln(\Delta w_{ij}) - \ln(\Delta w_{ij'}) + e_{ijj'q} > 0$$

### 3.2 Hierarchical Model

Individual log marginal utilities drawn from:
$$m_{ij} \sim N(\mu_j, \sigma_j)$$

where:
- μ_j = population mean log MU for aspect j
- σ_j = standard deviation (varies by aspect)

**Normalization:** Average across log MU means equals 0.

**Interpretation:** M̄_j = e^{μ_j} is relative marginal utility compared to geometric mean.

### 3.3 Estimation

- **Method:** Hamiltonian Markov Chain Monte Carlo (HMC)
- **Priors:** Uninformative (μ_j ~ N(0,10), σ_j ~ Cauchy(0,2))

---

## 4. Main Results: Marginal Utility Estimates

### 4.1 Top-Ranked Aspects (Highest Marginal Utilities)

| Rank | Aspect | Relative MU | Category |
|------|--------|-------------|----------|
| 1 | Your children's health | 67.14 | Family |
| 2 | Your children being able to live happy lives | 20.74 | Family |
| 3 | You having enough money to pay for healthcare | 13.48 | Financial |
| 4 | Your spouse/partner's health | 12.89 | Family |
| 5 | You and your family having enough to eat | 12.03 | Financial |
| 6 | The happiness of your family | 9.42 | Family |
| 7 | Your ability to protect your loved ones | 8.80 | Financial |
| 8 | Your financial security | 7.87 | Financial |
| 9 | The happiness of you and your family | 7.34 | Summum Bonum |
| 10 | Your mental health | 5.53 | Health |

### 4.2 Standard SWB Measures (Surprisingly Low)

| Aspect | Relative MU | Rank |
|--------|-------------|------|
| How satisfied you are with your life | ~2.0 | Mid-range |
| How happy you feel | ~1.8 | Mid-range |
| Life ladder rating | ~1.6 | Mid-range |

**Key Finding:** Standard SWB measures have marginal utilities only ~2x average, while top family aspects are 10-67x average.

### 4.3 Bottom-Ranked Aspects (Lowest Marginal Utilities)

- Status signals (e.g., "How high your income compared to others")
- Prosocial aspects (e.g., "You feeling generous")
- Global public goods (e.g., "How much you trust the courts")

### 4.4 Grouped Analysis

**By Subjective Categories:**

| Group | Average Relative MU |
|-------|---------------------|
| Family Well-being | 8.47 |
| Summum Bonum | 5.23 |
| Financial | 4.12 |
| Health (Physical) | 3.89 |
| Health (Mental) | 3.67 |
| Relationships | 2.94 |
| Feelings | 1.82 |
| Work | 0.89 |
| Status/Prestige | 0.34 |

---

## 5. Validation

### 5.1 Direct Importance Measures

Three flags from Aspect Flagging Survey:
1. **Global importance:** "How important is this aspect to you?" (r = 0.84)
2. **Marginal importance:** "How valuable would a little bit more be?" (r = 0.87)
3. **Tradeoff-focused:** "How much would you give up?" (r = 0.93)

**Key Finding:** Correlation strengthens as questions more closely mirror tradeoff framework.

### 5.2 Psychophysical Insight

Subjective perceptions of importance are linear in LOG of marginal utilities.
- Analogous to Weber-Fechner law in psychophysics
- Importance ratings scale with log(MU), not MU itself

### 5.3 Social Desirability Analysis

- Correlation between social desirability scores and log MU: r = -0.39
- **But:** Only explains 15% of variation
- Rank correlation after correction: 0.94 (ordering largely preserved)

---

## 6. Supply vs. Demand Framework

### 6.1 Conceptual Framework

Two sources of variation in aspect levels:

**Supply-Driven (Production Constraints):**
- Different individuals have different capacity to produce aspects
- Example: Elderly have lower physical mobility due to production constraints
- **Prediction:** Negative relationship between level and MU

**Demand-Driven (Taste Differences):**
- Same constraints, different preferences
- Higher preference → sacrifice more → higher level AND higher MU
- **Prediction:** Positive relationship between level and MU

### 6.2 Empirical Validation

Flag question asked respondents: "Of people who don't care much about getting more, what fraction have each reason?"
- Low scores = "they already have plenty" (supply-driven)
- High scores = "they don't value it much" (demand-driven)

**Result:** Correlation between supply-demand score and empirical slope = 0.41

Aspects judged as supply-driven show steeper negative level-MU slopes.

---

## 7. Demographic Heterogeneity

### 7.1 Key Finding: Within > Between

**Substantial heterogeneity across individuals, but:**
- Differences are far greater WITHIN demographic groups than BETWEEN them
- Most aspects cluster along 45-degree line when comparing groups

### 7.2 Specific Group Differences

**Gender:**
- Only significant difference: Women place higher MU on "You not feeling anxious"

**Age:**
- Older respondents: Higher MU on "Your physical health"
- Minimal differences on emotional/relationship aspects

**Parents vs. Non-Parents:**
- Parents: Much higher MU on child-related aspects
- Significant differences for family-related aspects

**Political Affiliation:**
- Democrats: Higher MU on "Women being treated fairly"
- Republicans: Higher MU on "Your culture and traditions being honored"

**Race:**
- Black respondents: Higher MU on "Not being discriminated against"

### 7.3 Non-Findings

- **No systematic income differences** (contrary to luxury goods hypothesis)
- **No significant education differences**
- **Minimal gender differences** beyond anxiety

---

## 8. Discussion

### 8.1 Implications for Well-Being Measurement

1. **Life satisfaction is insufficient:** Only ~2x average MU, while top aspects are 10-67x
2. **Family dominates:** Children's health is extreme outlier (67x average)
3. **Financial security matters:** Multiple financial aspects in top 10
4. **Status concerns are low:** Extrinsic aspects consistently at bottom

### 8.2 Philosophical Implications

**Supports:**
- Aristotle's emphasis on family and virtue (eudaimonia)
- Maslow's emphasis on security needs
- Locke's emphasis on property rights
- Sen's capability approach (economic security enables freedom)

**Challenges:**
- Contemporary focus on life satisfaction
- Assumptions that happiness captures what people want

### 8.3 Policy Implications

1. Welfare measures should weight family and financial security heavily
2. Life satisfaction alone is poor proxy for well-being
3. Interventions targeting financial security may have outsized welfare effects

---

## Key Parameters for EBF

| Parameter | Value | Source |
|-----------|-------|--------|
| Sample size | 3,358 (quality-controlled) | Methods |
| Total tradeoffs | >1 million | Methods |
| Aspects analyzed | 126 | Methods |
| Top aspect MU (children's health) | 67x average | Table 2 |
| Life satisfaction MU | ~2x average | Table 2 |
| Social desirability R² | 0.15 | Section 3.4 |
| Validation correlation (tradeoff flag) | 0.93 | Figure 4 |
| Supply-demand slope correlation | 0.41 | Figure 9 |
| Within-group heterogeneity | >> between-group | Section 4.3 |

---

## EBF Integration

### 10C Dimensions

| Dimension | Relevance | Parameter Impact |
|-----------|-----------|------------------|
| **WHAT** (C) | Utility dimensions empirically quantified | 126 aspects with relative MU weights |
| **WHO** (AAA) | Heterogeneity within > between groups | σ_j varies by aspect |
| **HOW** (B) | Supply-demand framework for complementarity | Level-MU slopes vary by aspect |
| **WHERE** (BBB) | Parameter estimation via stated preferences | μ_j, σ_j for 126 aspects |
| **AWARE** (AU) | Self-knowledge affects survey response | Links to Falk et al. (2025) τ |

### Theory Support

- **MS-SP-001:** Social Preferences (prosocial aspects low MU)
- **MS-TP-001:** Time Preferences (financial security high MU)
- **MS-WB-001:** Well-Being Economics (Benjamin et al. line)
- **MS-AU-001:** Awareness (self-report limitations)

### Critical EBF Implications

1. **WHAT Dimension Weights:** The 126 aspect MU estimates provide empirical weights for utility dimensions
   - Family (F) dimension should be weighted heavily
   - Standard SWB (life satisfaction) is poor proxy

2. **WHO Heterogeneity:** Within-group variance >> between-group variance
   - Segmentation by demographics may be less useful than expected
   - Individual-level heterogeneity dominates

3. **Supply vs. Demand:** Framework for interpreting level-MU relationships
   - Supply-constrained aspects: Higher levels → lower MU
   - Demand-driven aspects: Higher levels → higher MU
   - Empirically validated via aspect flagging

4. **Validation of Stated Preferences:** r = 0.93 correlation validates tradeoff method
   - Stronger when questions mirror economic framework
   - Log-linear relationship (Weber-Fechner for MU)

5. **Life Satisfaction Limitation:** Major implication for EBF welfare measures
   - Life satisfaction captures only ~2x average aspect
   - Missing high-MU dimensions (family, financial, health)

### Cross-References

- Benjamin et al. (2014): Beyond Happiness and Satisfaction (PAP-benjamin2014beyond)
- Falk et al. (2025): Limited Self-knowledge (PAP-falk2025limited) - survey methodology
- Kahneman & Deaton (2010): High income and emotional well-being
- Maslow (1943): Hierarchy of needs

---

## Appendix: Aspect Categories (Selected)

### Family Well-Being (Top Category)
- Your children's health
- Your children being able to live happy lives
- Your spouse/partner's health
- The happiness of your family
- Your ability to protect your loved ones

### Financial Security
- You having enough money to pay for healthcare
- You and your family having enough to eat
- Your financial security
- The absence of worry in your life about money

### Health
- Your mental health
- Your physical health
- You getting enough sleep

### Standard SWB Measures
- How satisfied you are with your life
- How happy you feel
- Life ladder rating

### Status/Prestige (Bottom Category)
- How high your income is compared to others
- You being a winner in life
- You having others remember your accomplishments

---

*Archived: 2026-02-04*
*Source: NBER Working Paper 33846*
*Content Level: L3 (Full structural documentation)*
