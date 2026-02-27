# CEO Behavior and Firm Performance

**Authors:** Oriana Bandiera, Andrea Prat, Stephen Hansen, Raffaella Sadun
**Year:** 2020
**Journal:** Journal of Political Economy, Vol. 128, No. 4, pp. 1325-1369
**DOI:** 10.1086/705331
**Archived Date:** 2026-02-24
**Content Level:** L2 (Comprehensive structured summary with S1-S6)

---

## Abstract

We develop a new method to measure CEO behavior in large samples via a survey that collects high-frequency, high-dimensional diary data and a machine learning algorithm that estimates behavioral types. Applying this method to 1,114 CEOs in six countries reveals two types: "leaders," who do multifunction, high-level meetings, and "managers," who do individual meetings with core functions. Firms that hire leaders perform better, and it takes three years for a new CEO to make a difference. Structural estimates indicate that productivity differentials are due to mismatches rather than to leaders being better for all firms.

---

## 1. Introduction

What do CEOs actually do, and does it matter for firm performance? Despite the central role of CEOs in modern economies — setting strategy, allocating resources, motivating employees — remarkably little systematic evidence exists on how CEOs spend their time and whether differences in CEO behavior affect firm outcomes.

The challenge is measurement. Traditional approaches either rely on small samples (Mintzberg 1973, who observed five CEOs) or proxy behavior through observable characteristics like education, tenure, or compensation. These proxies capture who the CEO is but not what the CEO does day to day.

### Research Questions

This paper addresses three fundamental questions:

1. **Measurement:** How can we systematically measure CEO behavior across large samples and multiple countries?
2. **Typology:** Do CEOs cluster into distinct behavioral types, and if so, what are these types?
3. **Performance:** Does CEO behavioral type affect firm performance, and if so, through what mechanism?

### Contribution

The paper makes three contributions:

First, it develops a **new survey methodology** that collects time-use data from CEOs at 15-minute intervals over one full workweek, yielding high-frequency, high-dimensional behavioral data for each CEO.

Second, it applies **machine learning algorithms** (specifically, Latent Dirichlet Allocation adapted from text mining) to classify CEO behavioral patterns into distinct types, discovering a two-type taxonomy.

Third, it estimates **structural models** linking CEO type to firm productivity, distinguishing between "leaders are universally better" and "matching matters" (assignment) explanations.

---

## 2. Data and Methodology

### 2.1 CEO Time-Use Survey

The authors designed and implemented a large-scale survey of CEO time use:

**Sample:** 1,114 CEOs across six countries (Brazil, France, Germany, India, United Kingdom, United States)

**Firm selection:** Manufacturing firms with 100-5,000 employees (to ensure CEO roles are comparable)

**Data collection protocol:**
- Personal assistant of each CEO recorded the CEO's activities in 15-minute blocks for five consecutive workdays (Monday-Friday)
- Each block was coded along multiple dimensions:
  - **Activity type:** planned meeting, unplanned meeting, phone call, business meal, public event, travel, working alone
  - **Function:** production, marketing, sales, finance, HR, strategy, general management, other
  - **Number of participants:** alone, one-on-one, 2-5, 6+
  - **Whether participants are insiders or outsiders**
  - **Level of participants:** C-suite, senior management, junior staff
  - **Initiative:** planned or unplanned

**Result:** Each CEO is represented by a vector of time-allocation shares across hundreds of possible activity categories.

### 2.2 Machine Learning Classification

To identify behavioral types from the high-dimensional time-use data, the authors adapt **Latent Dirichlet Allocation (LDA)**, a topic model originally developed for text analysis:

- Each CEO is treated as a "document"
- Each 15-minute activity block is treated as a "word"
- The algorithm identifies latent "topics" (behavioral types) that best explain the observed distribution of activities across CEOs

The algorithm reveals **two dominant behavioral types:**

**Type 1: "Leaders"**
- Spend more time in **large, multi-function meetings** (cross-departmental)
- Focus on **high-level activities** (strategy, planning, C-suite interactions)
- More **planned interactions** (less reactive)
- Engage with **senior management and outside stakeholders**
- Time allocation: more strategy, marketing, general management

**Type 2: "Managers"**
- Spend more time in **one-on-one meetings** with core function heads
- Focus on **operational activities** (production, finance, HR)
- More **unplanned interactions** (reactive)
- Engage primarily with **internal staff** (fewer outsiders)
- Time allocation: more production, finance, HR

### 2.3 Behavioral Differences in Detail

| Dimension | Leaders | Managers |
|-----------|---------|----------|
| Meeting size | Larger (6+) | Smaller (1-on-1) |
| Meeting composition | Multi-function | Single function |
| Participant level | C-suite, senior | All levels |
| Activity type | Planned meetings | Mix planned/unplanned |
| Functional focus | Strategy, marketing | Production, finance |
| External engagement | Higher | Lower |
| Hours worked | Slightly more (~52h/week) | Slightly fewer (~50h/week) |

---

## 3. Main Results

### 3.1 CEO Type and Firm Performance

**Core finding:** Firms with leader-type CEOs have **higher productivity** (measured by sales per employee and value added per employee).

The estimated performance differential is substantial:

- Leader-type CEO firms have approximately **3.5% higher revenue** (controlling for firm size, industry, country)
- This effect is robust to controls for CEO characteristics (education, tenure, age)
- The effect is robust across all six countries in the sample

### 3.2 It Takes Three Years

A particularly striking finding involves CEO transitions. When a new CEO takes over:

- **Year 1:** No measurable effect on firm performance
- **Year 2:** Small, often insignificant effects
- **Year 3+:** Full performance effects materialize

This 3-year lag is consistent with the organizational economics prediction that behavioral change requires time for:
1. The CEO to understand the organization
2. New routines to be established
3. Complementary organizational changes to take effect
4. Old practices to be fully replaced

### 3.3 Matching vs. Universally Better

The most important theoretical finding concerns the mechanism:

**Are leaders simply better than managers for all firms?** Or does the right CEO type depend on the firm?

The structural estimation reveals that **matching matters:** the performance differential is driven by **mismatches** — managers in firms that would benefit from leaders, and (to a lesser extent) leaders in firms that would benefit from managers.

**Evidence for matching:**
- In firms with more complex operations (multi-product, multi-plant), leaders outperform managers by a larger margin
- In firms with simpler, more routine operations, the manager type is less disadvantageous
- The cross-country variation in leader prevalence correlates with institutional factors that affect the returns to different CEO types

### 3.4 What Drives the Leader Premium?

The paper explores channels through which leader-type CEOs raise productivity:

1. **Cross-functional coordination:** Leaders' multi-function meetings facilitate information flow across organizational silos
2. **Strategic focus:** Leaders allocate more time to forward-looking activities (strategy, marketing) vs. backward-looking activities (production monitoring)
3. **External alignment:** Leaders' greater engagement with outside stakeholders (customers, suppliers, investors) improves market positioning

---

## 4. Theoretical Framework

### 4.1 A Simple Model of CEO Time Allocation

The paper develops a structural model in which the CEO allocates a fixed time endowment across activities:

- Each activity produces "output" that depends on the CEO's type and the firm's characteristics
- The CEO's optimal allocation depends on both the CEO's comparative advantage across activities and the firm's marginal return to each activity

**Key insight:** A leader-type CEO has comparative advantage in multi-function coordination, while a manager-type CEO has comparative advantage in operational oversight. The optimal match depends on which activity has higher marginal value for the specific firm.

### 4.2 Assignment Problem

The structural model is an assignment problem: matching heterogeneous CEOs to heterogeneous firms. The equilibrium matching depends on:
- The distribution of CEO types (approximately 60% leaders, 40% managers)
- The distribution of firm needs
- The efficiency of the CEO labor market (how well firms can identify and attract the right type)

**Finding:** The CEO labor market is imperfect — observed mismatches are common and persistent, generating the productivity differentials.

---

## 5. Robustness and Extensions

### 5.1 Selection Concerns

A key concern is reverse causality: do productive firms hire leader-type CEOs, or do leader-type CEOs make firms productive?

**Addressing selection:**
- The 3-year lag finding argues against simple selection (if firms hire leaders when they are already doing well, effects should appear immediately)
- CEO transitions provide quasi-experimental variation
- Controlling for pre-CEO firm characteristics does not eliminate the leader premium
- Instrumental variable specifications using CEO labor market thickness yield similar results

### 5.2 Country Differences

| Country | Leader Share | Performance Gap |
|---------|-------------|-----------------|
| United States | 65% | +3.2% |
| United Kingdom | 62% | +3.8% |
| Germany | 58% | +2.9% |
| France | 55% | +3.5% |
| Brazil | 52% | +4.1% |
| India | 48% | +4.5% |

**Pattern:** Countries with less developed managerial labor markets (Brazil, India) show both fewer leaders and larger performance gaps from mismatches.

### 5.3 Within-CEO Variation

The methodology captures not just between-CEO differences but also within-CEO variation over the week:
- Leaders show more consistent behavior patterns
- Managers show more reactive, variable behavior
- Monday and Friday behaviors differ systematically

---

## 6. Relation to Literature

### CEO and Management Studies
- **Mintzberg (1973):** "The Nature of Managerial Work" — pioneering but small-sample observational study of 5 CEOs
- **Bertrand and Schoar (2003):** "Managing with Style" — CEO fixed effects matter for corporate policies
- **Bloom and Van Reenen (2007):** Management practices across firms and countries — parallel methodology for middle management
- **Bloom et al. (2012):** Extension to 10,000+ organizations in 20 countries
- **Kaplan et al. (2012):** CEO personality traits and VC-backed firm outcomes

### Assignment and Matching
- **Gabaix and Landier (2008):** CEO talent and firm size — assortative matching
- **Terviö (2008):** Market for talent and inequality
- **Rosen (1982):** Authority, control, and the distribution of earnings

### Organizational Economics
- **Van den Steen (2017, 2018):** Formal theory of strategy and the strategist
- **Gibbons and Roberts (2013):** Handbook of Organizational Economics
- **Lazear (2018):** Personnel economics and compensation

---

## 7. Conclusion

This paper makes three key contributions to understanding CEO behavior and its consequences:

1. **Measurement innovation:** The high-frequency diary method combined with machine learning produces the first large-scale, systematic classification of CEO behavioral types.

2. **Two types:** CEOs cluster into "leaders" (cross-functional coordinators, strategic focus) and "managers" (operational specialists, functional focus).

3. **Matching matters:** The 3.5% productivity premium for leader-type CEOs is driven by firm-CEO mismatches, not by leaders being universally superior. This implies that the CEO labor market is imperfect and that better matching could raise aggregate productivity.

The 3-year transition period for new CEOs to affect firm performance underscores the organizational complementarities at work: CEO behavior must be complemented by organizational routines, culture, and practices that take time to develop.

---

## References

Bandiera, O., Prat, A., and Sadun, R. (2013). "Managing the Family Firm: Evidence from CEOs at Work." NBER Working Paper No. 19722.

Bertrand, M. and Schoar, A. (2003). "Managing with Style: The Effect of Managers on Firm Policies." Quarterly Journal of Economics, 118(4), 1169-1208.

Bloom, N. and Van Reenen, J. (2007). "Measuring and Explaining Management Practices Across Firms and Countries." Quarterly Journal of Economics, 122(4), 1351-1408.

Bloom, N., Genakos, C., Sadun, R., and Van Reenen, J. (2012). "Management Practices Across Firms and Countries." Academy of Management Perspectives, 26(1), 12-33.

Gabaix, X. and Landier, A. (2008). "Why Has CEO Pay Increased So Much?" Quarterly Journal of Economics, 123(1), 49-100.

Gibbons, R. and Roberts, J. (2013). The Handbook of Organizational Economics. Princeton University Press.

Kaplan, S. N., Klebanov, M. M., and Sorensen, M. (2012). "Which CEO Characteristics and Abilities Matter?" Journal of Finance, 67(3), 973-1007.

Lazear, E. P. (2018). "Compensation and Incentives in the Workplace." Journal of Economic Perspectives, 32(3), 195-214.

Mintzberg, H. (1973). The Nature of Managerial Work. Harper & Row.

Rosen, S. (1982). "Authority, Control, and the Distribution of Earnings." Bell Journal of Economics, 13(2), 311-323.

Terviö, M. (2008). "The Difference That CEOs Make: An Assignment Model Approach." American Economic Review, 98(3), 642-668.

Van den Steen, E. (2017). "A Formal Theory of Strategy." Management Science, 63(8), 2616-2636.

Van den Steen, E. (2018). "Strategy and the Strategist: How It Matters Who Develops the Strategy." Management Science, 64(10), 4533-4551.

Wasserman, N. (2003). "Founder-CEO Succession and the Paradox of Entrepreneurial Success." Organization Science, 14(2), 149-172.
