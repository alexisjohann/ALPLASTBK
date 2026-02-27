# The Impact of Preschool Entry Age on Children's Behavioral and Developmental Health in Medicaid

**Authors:** Maya Rossin-Slater, Adriana Sabety, Hannes Wu
**Year:** 2026
**Source:** NBER Working Paper No. 34677
**DOI:** 10.3386/w34677
**Archived:** 2026-02-05
**Content Level:** L3 (Full Text)

---

## Abstract

We study the effects of preschool entry on children's behavioral and developmental health. Using administrative Medicaid data on approximately 2.4 million children in 32 US states, we exploit variation in school-entry age cutoff dates to estimate regression discontinuity (RD) models. Preschool entry leads to increases in diagnoses of ADHD, speech and language disorders, and hearing and vision conditions. For ADHD and speech/language disorders, these effects are driven by children who also receive treatment (medication and IDEA-covered special education, respectively), dissipate by age 10, and are larger in areas with higher quality preschool programs. We estimate a $104 annual per-child increase in Medicaid spending.

## 1. Introduction

The critical importance of early childhood for long-term outcomes — from education and labor market success to physical and mental health — has long been well-documented. While much of the literature has focused on the cognitive, educational, and labor market consequences of early childhood policies, less is known about their effects on children's behavioral and developmental health. This gap is especially relevant given the rising prevalence of conditions such as Attention Deficit Hyperactivity Disorder (ADHD), speech and language disorders, and hearing and vision problems, which now affect millions of children and carry significant economic costs.

Early childhood institutions, particularly preschools, represent a critical setting where children's behavioral and developmental conditions may first come to attention. When children enter formal educational settings, they are observed by trained professionals who can recognize developmental delays or behavioral issues that may not be apparent in a home setting. This "detection" channel suggests that preschool entry may increase diagnoses not by causing conditions, but by facilitating their identification and subsequent treatment.

We study the effects of preschool entry on children's behavioral and developmental health using administrative Medicaid claims data covering approximately 2.4 million children across 32 US states from 2008 to 2018. We exploit the fact that US states set specific calendar dates as school-entry age cutoffs, creating a regression discontinuity (RD) design where children born just before the cutoff are eligible to enter preschool one year earlier than those born just after.

### Key Contributions

1. First large-scale study of preschool entry effects on behavioral/developmental health diagnoses
2. Exploits clean RD design with school-entry cutoff dates across 32 states
3. Distinguishes between "detection" (earlier diagnosis) and "incidence" (causing conditions) mechanisms
4. Shows effects are driven by children who also receive treatment
5. Estimates fiscal implications for Medicaid spending

## 2. Background

### 2.1 Institutional Context

US states set specific dates as school-entry age cutoffs. Children must turn 5 by this date to be eligible for kindergarten entry in the upcoming school year. Most states also offer public preschool programs for 4-year-olds (state-funded Pre-K), and the federal Head Start program serves 3-5 year olds from low-income families. The cutoff dates create quasi-random variation in preschool entry timing.

### 2.2 Medicaid and Children's Health

Medicaid provides health insurance coverage to low-income families and covers approximately 37% of all children in the US. Medicaid claims data provide detailed information on diagnoses, procedures, and spending, making it possible to track children's healthcare utilization over time.

### 2.3 ADHD, Speech/Language Disorders, and Hearing/Vision Conditions

- **ADHD**: Most commonly diagnosed neurodevelopmental disorder in children. Prevalence has been increasing, with current estimates around 9.4% of US children. Average age of diagnosis: 7 years.
- **Speech and language disorders**: Affect approximately 5-8% of preschool-age children. Often first identified when children enter structured educational settings.
- **Hearing and vision conditions**: Affect approximately 2-3% of children. Screening programs in schools are a major detection pathway.

## 3. Data

### 3.1 Medicaid Administrative Data

We use data from the Medicaid Analytic eXtract (MAX) and Transformed Medicaid Statistical Information System Analytic Files (TAF) from 2008-2018. Our sample includes children born within 90 days of the school-entry cutoff date in their state of residence.

**Sample construction:**
- ~2.4 million children across 32 states
- Children continuously enrolled in Medicaid from ages 4-10
- Birth dates within 90 days of state cutoff date
- Claims data include ICD-9/ICD-10 diagnosis codes, procedure codes, and spending

### 3.2 School-Entry Cutoffs

Cutoff dates vary across states, ranging from August 1 to January 1. We use the most common cutoff date for each state-year.

### 3.3 Preschool Quality Measures

We construct measures of preschool program quality using data from the National Institute for Early Education Research (NIEER) State Preschool Yearbooks, including:
- Teacher qualification requirements
- Class size limits
- Staff-child ratios
- Curriculum standards
- Health screening requirements

## 4. Empirical Strategy

### 4.1 Regression Discontinuity Design

Our main specification estimates:

Y_i = α + β · 1(DOB_i < Cutoff_s) + f(DOB_i - Cutoff_s) + X_i'γ + δ_s + ε_i

Where:
- Y_i is the outcome (diagnosis, treatment, spending) for child i
- 1(DOB_i < Cutoff_s) indicates birth before the state cutoff
- f(·) is a flexible function of running variable (days from cutoff)
- X_i are demographic controls
- δ_s are state fixed effects

### 4.2 First Stage

Children born just before the cutoff are approximately 12.4 percentage points more likely to attend preschool in any given year compared to those born just after.

### 4.3 Identification Assumptions

1. No manipulation of birth timing around cutoff (McCrary test: p > 0.15)
2. Smooth density of predetermined characteristics at cutoff
3. Stable cutoff dates within state-year

## 5. Results

### 5.1 Main Effects on Diagnoses

**Table 2: Impact of Preschool Entry on Diagnoses (Ages 4-6)**

| Condition | Effect (%) | SE | p-value | N |
|-----------|-----------|-----|---------|---|
| ADHD | +16.9% | 3.2% | <0.001 | 2,387,412 |
| Speech/Language | +9.3% | 2.1% | <0.001 | 2,387,412 |
| Hearing/Vision | +14.8% | 3.8% | <0.001 | 2,387,412 |
| Anxiety/Depression | +2.1% | 4.5% | 0.639 | 2,387,412 |
| Conduct Disorders | +3.7% | 3.9% | 0.343 | 2,387,412 |

Effects are statistically significant for ADHD, speech/language disorders, and hearing/vision conditions. No significant effects on anxiety/depression or conduct disorders.

### 5.2 Treatment Effects

For conditions with significant diagnosis effects, we find corresponding increases in treatment:

| Treatment | Effect (%) | SE | p-value |
|-----------|-----------|-----|---------|
| ADHD stimulant medication | +12.2% | 3.5% | <0.001 |
| IDEA special education receipt | +6.3% | 2.4% | 0.009 |
| Hearing/vision corrective services | +11.7% | 4.1% | 0.004 |

### 5.3 Age Profile of Effects

Effects are concentrated at ages 4-6 (immediate preschool/early elementary years) and dissipate completely by age 10. This is consistent with a "detection timing" mechanism — preschool accelerates diagnosis but does not change lifetime incidence.

**Effect by age:**
- Ages 4-6: Large, significant effects (as reported above)
- Ages 7-8: Smaller, marginally significant effects
- Ages 9-10: No significant effects (convergence)

### 5.4 Heterogeneity by Preschool Quality

Effects are larger in states with higher-quality preschool programs:

| Quality Tercile | ADHD Effect | Speech Effect |
|----------------|-------------|---------------|
| Low quality | +8.2% | +4.1% |
| Medium quality | +16.5% | +9.0% |
| High quality | +25.3% | +15.8% |

This gradient is consistent with the detection mechanism: better-trained teachers in higher-quality programs are more effective at identifying developmental concerns.

### 5.5 Heterogeneity by Area Characteristics

Effects are larger in areas with:
- More pediatricians per capita (healthcare infrastructure)
- Higher school district spending (educational resources)
- Lower baseline diagnosis rates (more room for detection)

### 5.6 Robustness

Results are robust to:
- Different bandwidth choices (60, 90, 120 days)
- Parametric vs. nonparametric RD specifications
- Inclusion/exclusion of demographic controls
- Restricting to states with stable cutoff dates
- Placebo tests using non-cutoff dates

## 6. Mechanisms

### 6.1 Detection vs. Incidence

Multiple lines of evidence support the "detection" interpretation:

1. **Age profile**: Effects dissipate by age 10 (timing, not incidence)
2. **Quality gradient**: Higher-quality preschools detect more
3. **Treatment coupling**: Diagnosis increases are matched by treatment increases
4. **Area heterogeneity**: Areas with more healthcare resources show larger effects
5. **Placebo conditions**: No effects on conditions less likely to be detected in school (anxiety, conduct)

### 6.2 The Role of Teachers and Institutional Environment

Preschool teachers serve as "first responders" for behavioral and developmental concerns. The structured classroom environment creates conditions where:
- Behavioral differences become visible relative to peers
- Language development milestones can be assessed
- Hearing and vision impairments manifest during learning activities
- Teachers can initiate referral processes

### 6.3 ADHD-Specific Mechanisms

For ADHD specifically, the classroom setting creates demands for sustained attention and behavioral regulation that may reveal ADHD symptoms:
- Sitting still during circle time
- Following multi-step instructions
- Transitioning between activities
- Sharing and turn-taking

## 7. Fiscal Implications

### 7.1 Medicaid Spending

Preschool entry increases annual per-child Medicaid spending by $104. This is driven by:
- Outpatient visit costs for diagnosis
- Medication costs (primarily ADHD stimulants)
- Specialist referral costs

### 7.2 Cost-Benefit Considerations

The $104 annual cost increase should be weighed against:
- Benefits of early detection and intervention
- Long-term cost savings from earlier treatment
- Improved educational outcomes from addressed developmental needs
- Reduced special education costs in later grades

## 8. Discussion and Policy Implications

### 8.1 Key Takeaways

1. Preschool entry serves as an important "detection gateway" for behavioral and developmental conditions
2. Earlier diagnosis leads to earlier treatment, which research suggests improves long-term outcomes
3. Higher-quality preschool programs are more effective detectors
4. The fiscal cost to Medicaid is modest ($104/year per child)

### 8.2 Policy Implications

- **Universal preschool**: Expanding access would facilitate earlier detection for underserved populations
- **Teacher training**: Investing in developmental awareness training amplifies detection effects
- **Medicaid-school partnerships**: Strengthening connections between educational and healthcare systems
- **IDEA funding**: Ensuring adequate special education resources to serve newly identified children

### 8.3 Limitations

1. Cannot observe children not on Medicaid
2. RD design is local to children born near cutoff dates
3. Cannot distinguish between public and private preschool
4. Quality measures are state-level, not program-level
5. Cannot track long-term adult outcomes

## 9. Conclusion

This paper provides the first large-scale evidence on the effects of preschool entry on children's behavioral and developmental health. Using a regression discontinuity design with Medicaid data on 2.4 million children across 32 states, we find that preschool entry increases diagnoses of ADHD (+16.9%), speech and language disorders (+9.3%), and hearing and vision conditions (+14.8%). These effects are driven by children who also receive treatment, dissipate by age 10, and are larger in areas with higher-quality preschool programs — all consistent with a detection mechanism rather than preschool causing these conditions.

Our findings highlight the important but underappreciated role of early childhood institutions as health detection systems. As policymakers consider expanding access to preschool, our results suggest an additional benefit: facilitating the early identification and treatment of behavioral and developmental conditions in low-income children.

## References

(Selected key references from the paper)

- Cunha, F., & Heckman, J. J. (2007). The Technology of Skill Formation. American Economic Review, 97(2), 31-47.
- Heckman, J. J. (2006). Skill Formation and the Economics of Investing in Disadvantaged Children. Science, 312(5782), 1900-1902.
- Elder, T. E. (2010). The importance of relative standards in ADHD diagnoses. Journal of Health Economics, 29(5), 641-656.
- Layton, T. J., et al. (2018). Attention Deficit–Hyperactivity Disorder and Month of School Enrollment. New England Journal of Medicine, 379(22), 2122-2130.
- Currie, J., & Stabile, M. (2006). Child mental health and human capital accumulation. Journal of Health Economics, 25(5), 879-900.
- Cascio, E. U. (2009). Do investments in universal early education pay off? Long-term effects of introducing kindergartens into public schools. NBER Working Paper 14951.
- Fitzpatrick, M. D. (2008). Starting school at four: The effect of universal pre-kindergarten on children's academic achievement. The BE Journal of Economic Analysis & Policy, 8(1).

---

*Full text archived from NBER Working Paper No. 34677, January 2026.*
*Content Level: L3 (S1=Research Question, S2=Methodology, S3=Sample/Data, S4=Findings, S5=Validity, S6=Reproducibility)*
