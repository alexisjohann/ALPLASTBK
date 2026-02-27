# Measuring the Growth of Skills

**Authors:** James J. Heckman, Haihan Tian, Zijian Zhang, Jin Zhou

**Source:** NBER Working Paper No. 34737, January 2026

**DOI:** 10.3386/w34737

**JEL Codes:** C18, J24

---

## Abstract

This paper discusses a fundamental problem in measuring the growth of knowledge and comparing the skills of people. New skills emerge that are not just more of the previously acquired skills. Psychometric convention forces these skills into arbitrarily constructed scales, which can severely distort measurement. To formally address this problem, we measure skills using a novel measurement scheme, estimate a stochastic learning process and reject the common scale assumption across levels for language and cognitive skills. Furthermore, we estimate dynamic complementarity without imposing arbitrary scales for skills.

---

## I. Introduction

Economists use test scores to measure learning, treating scores as cardinal and commensurable across people and ages. This practice is untenable. Test scores are at best ordinal, and different normalizations generate different rankings and treatment effects. Arbitrarily scaled scores are widely used in empirical work on child development and education.

**Key New Point:** Skills do not evolve as higher levels of a fixed set of abilities. New skills emerge with development, and they are often qualitatively different from the ones measured at earlier ages. There is no constant-unit measure of cognition or language that is valid across ages for the same people. Forcing distinct skills into a common scale distorts measures of both levels and growth.

This insight can explain key anomalies in the literature, including the apparent fadeout of early treatment effects.

**Data:** Weekly data from a large-scale home-visiting program in rural China (China REACH).

**Method:** Novel measurement scheme allowing scale-free tests of dynamic complementarity, learning, cross-complementarity, and catch-up without relying on psychometric fiat.

---

## II. The Technology of Skill Formation

The technology of skill formation is a multistage technology:

**Equation 1:**
```
K(a + 1) = f^(a)(K(a), I(a))
```

Where:
- K(a+1) = vector of skills at age a+1
- K(a) = vector of skills at age a
- I(a) = investment at age a (parenting, schools, etc.)

**Important:** K(a+1) and K(a) might be measured on a standard scale as is common in the literature, but that is not required.

### Dynamic Complementarity

Investment at age a raises the productivity (rate of learning) of later investment:

**Equation 2:**
```
∂²K(a+j+1) / ∂I(a)∂I'(a+j) > 0
```

**Critical:** This parameter does NOT require any assumption that K at different ages is measured in the same units.

---

## III. Strategy

Key to the strategy is access to repeated lessons on skills at specific levels administered to people of the same age. The outcomes (learned or not) of each sequence of identical lessons can be measured.

These measures:
- Are well-defined measures of skill comparable across otherwise identical people
- Can meaningfully measure growth within levels
- Need NOT cumulate additively across levels

Children enter the program at different ages and face a structured schedule of repeated instruction and assessments of age-specific skills.

**Examination focus:** Whether the learning rate of skills is accelerated by higher levels of skills present at the start of each stage (level) of instruction.

### Problem with Carry-Over Items

One solution is to carry over items across administrations and fix the scale on previously tested items. However, when the same item is tested on occasions separated by a year, children do better on the second occasion. There is appreciation of knowledge with the passage of time. The scale shifts upward.

---

## IV. Data

**Source:** China REACH - large scale, experimental evaluation conducted by China Development Research Foundation (CDRF).

**Intervention:** Home-visiting program cultivating multi-dimensional skill development:
- Trained home visitors (same education level as mothers)
- Weekly household visits (one hour)
- Age-specific caregiving guidance
- Weekly evaluation of knowledge

**Skills measured:** Three categories:
1. Fine motor
2. Language
3. Cognitive

**Skill ordering:** Based on difficulty levels following Palmer (1971) and Uzgiris-Hunt (1975) profiles (UHP).

### Language Skill Levels (11 UHP Levels)

| Level | Task Description |
|-------|------------------|
| 1 | Caregiver and child make sounds to interact |
| 2 | Caregiver tells child things she does in house |
| 3 | Child recognizes people's names |
| 4 | Child learns movements showing intimacy (clapping, bye-bye, thank you) |
| 5 | Looking at pictures together, child vocalizes and touches |
| 6 | Child recognizes at least one body part |
| 7 | Child identifies and/or names ordinary objects |
| 8 | Child points to named pictures, names one or more, mimics sounds |
| 9 | Child points to named pictures, names two or more, mimics sounds |
| 10 | Child points at 7+ pictures and talks about them |
| 11 | Child learns descriptive words, names objects, tells usage |

**Critical observation:** Standard psychometric practice imposes a common numerical scale across these levels. The activities at higher levels are assumed to produce knowledge that is more of the same thing measured at lower levels. **This assumption is questionable.**

### Within-Level Consistency

Within levels, the skills taught and measured are essentially identical. Example: Level 3 has five tasks all relating to "teaching the child to recognize people's names" - no hierarchy within levels.

---

## V. Results

### Learning Patterns

**Figure 1 findings:**
- Average passing rates by age within each difficulty level increase with number of lessons (consistent with learning)
- When individuals transition to higher difficulty levels, initial age-specific passing rates DECLINE at entry
- After initial declines, passing rates within levels increase as learning ensues
- Fine motor skills show at most modest learning

### Ability Group Patterns

- High ability children: highest performance across levels
- Normal ability children: second highest, catch up at later levels
- Low ability children: lowest initially, but strong evidence of catch-up at later stages

**Key finding:** The distinction between ability groups is sharp at earlier levels but gradually narrows as children progress across levels.

### Formal Test Results

Using the dynamic reinforcement learning model (Heckman and Zhou, 2026):

**Hypothesis: Common scale across levels**
- Language skills: **REJECTED**
- Cognitive skills: **REJECTED**
- Fine motor skills: **NOT REJECTED**

---

## VI. Scale-Free Test of Dynamic Complementarity

### Sample Design

In treatment sample:
- Almost all children receive lessons starting from level 6
- Heterogeneity in exposures prior to level 6 gives variability in earlier investment
- ~40% take entire curriculum
- Others enter at later stages

Two groups compared:
1. Full curriculum exposure
2. Enrolled at level 6 with no prior investment

Balance tests on baseline background variables passed.

### Results (Table 3)

**Time to First Mastery by Enrollment Cohort (Language)**

| UHP Level | Full Exposure | Enrolled at L6 | p-value | Stepdown p |
|-----------|---------------|----------------|---------|------------|
| ℓ = 7 | 2.487 | 2.518 | 0.870 | 0.864 |
| ℓ = 8 | 2.079 | 2.367 | **0.024** | 0.059 |
| ℓ = 9 | 1.496 | 1.686 | **0.017** | 0.059 |
| ℓ = 10 | 1.404 | 1.454 | 0.608 | 0.827 |
| ℓ = 11 | 1.348 | 1.698 | **0.000** | **0.000** |

**Interpretation:** At UHP Language levels 8, 9, and 11, children with full curriculum exposure require significantly fewer trials until their first success. Otherwise similar children with more early investment are learning more than those without early investment.

**Cognitive skills:** Comparable results showing dynamic complementarity.

**Fine motor skills:** No evidence of dynamic complementarity.

### Implications for Disadvantaged Children

For initially low-ability groups in both cohorts, the difference in learning rates at later levels is even more pronounced. **Disadvantaged children benefit the most** in the early stages through dynamic complementarity and reduce the gap at later stages.

---

## VII. Summary

### Main Contributions

1. **Documentation of skill emergence:** New skills emerge at different levels of nominally the same skill.

2. **Challenge to standard procedures:** Current procedures impose common scales on nominally the same skills - this is invalid for language and cognitive skills.

3. **Explanation of fadeout:** Comparing different skills over time is not meaningful. Fadeout may reflect skill emergence, not loss of treatment effects.

4. **Scale-free identification:** Lack of common scale does not prevent identifying crucial aspects of skill formation technology if meaningful scales can be found within levels.

5. **Dynamic complementarity and catch-up:** Scale-free tests identify dynamic complementarity and catch-up of the less able.

### Practical Implications

- Value-added measures assuming common scales are on shaky ground
- Careful design of future studies can avoid imposing arbitrary scales
- Within-level measurement provides valid growth assessment
- Early intervention benefits disadvantaged children most through dynamic complementarity

---

## Key Parameters for EBF

| Parameter | Domain | Value | Notes |
|-----------|--------|-------|-------|
| Dynamic complementarity (language) | Early childhood | Positive | Significant at levels 8, 9, 11 |
| Dynamic complementarity (cognitive) | Early childhood | Positive | Similar pattern to language |
| Dynamic complementarity (fine motor) | Early childhood | Null | No evidence |
| Common scale validity (language) | Measurement | Rejected | Skills emerge at each level |
| Common scale validity (cognitive) | Measurement | Rejected | Skills emerge at each level |
| Common scale validity (fine motor) | Measurement | Not rejected | May be cumulative |
| Catch-up potential (low ability) | Learning | High | Gap narrows at later levels |

---

## References

- Bailey et al. (2020). Persistence and fade-out of educational-intervention effects. *Psychological Science in the Public Interest*.
- Cunha et al. (2021). The econometrics of early childhood human capital and investments. *Annual Review of Economics*.
- Dehaene (2020). How We Learn: The New Science of Education and the Brain.
- Freyberger (2025). Normalizations and misspecification in skill formation models. *Review of Economic Studies*.
- Heckman et al. (2025). Dynamic complementarity. *AEJ: Applied Economics* (under revision).
- Heckman & Zhou (2026). The microdynamics of early childhood learning. *Journal of Political Economy* (forthcoming).
- Jacob & Rothstein (2016). The measurement of student ability in modern assessment systems. *JEP*.
- Zhou et al. (2026). The impacts of a prototypical home visiting program on child skills. *Journal of Labor Economics*.

---

*Archived: 2026-02-05 | Content Level: L3 | Integration Level: 4 (THEORY)*
