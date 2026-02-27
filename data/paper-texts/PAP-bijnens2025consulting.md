# What Do Consultants Do?

**Authors:** Gert Bijnens, Simon Jäger, and Benjamin Schoefer

**Year:** 2025

**Journal:** NBER Working Paper No. 33463

**DOI:** https://doi.org/10.3386/w33463
# What Does Consulting Do?

**Authors:** Gert Bijnens, Jozef Konings, and John Van Reenen
**Year:** 2025
**Institution:** NBER Working Paper No. 34072
**DOI:** 10.3386/w34072
**Type:** Working Paper
**Archived Date:** 2026-02-24
**Content Level:** L2 (Comprehensive structured summary with S1-S6)

---

## Abstract

What do management consultants do? And do their engagements with client firms improve firm performance? We study these questions using Belgian administrative data on the universe of firms, matched employer-employee records, and financial statements, linked to consulting engagements. Using a difference-in-differences research design comparing client firms to synthetic control firms, we find that substantial consulting engagements lead to labor productivity gains of around 5.8% (revenue per worker) to 5.6% (value added per worker) that persist for at least four years after the initial engagement. These productivity gains do not come at the cost of worker welfare: hourly wages increase by 2.4% and hours worked are unaffected. At the same time, consulting engagements trigger firm reorganization: a temporary increase in hiring and separations, and a shift in the workforce composition toward more white-collar and management workers. Treated firms increase their purchases of service inputs, consistent with a broader reorganization of production toward outsourcing. Consulting engagements also lead to increased market power, with a markup increase of 2.6% and higher profit margins.
This paper provides the first systematic and comprehensive empirical study of management and strategy consulting. The authors unveil the workings of this opaque industry by drawing on universal administrative business-to-business transaction data based on value-added tax links from Belgium (2002-2023). These data permit documentation of the nature of consulting engagements, take-up patterns, and the effects on client firms. Consulting take-up is concentrated among large, high-labor-productivity firms. For TFP and profitability, a U-shaped pattern emerges: both high and low performers hire consultants. New clients spend on average 3% of payroll on consulting, typically in episodic engagements lasting less than one year. Using difference-in-differences designs exploiting these sharp consulting events, the authors find positive effects on labor productivity of 3.6% over five years, driven by modest employment reductions alongside stable or growing revenue. Average wages rise by 2.7% with no decline in labor's share of value added, suggesting productivity gains do not come at workers' expense through rent-shifting. The findings broadly align with ex-ante predictions from surveyed academic economists and consulting professionals, validating the productivity-enhancing view of consulting endorsed by most practitioners though only half of academics, while lending less support to a rent-shifting view favored by many economists.

---

## 1. Introduction

Management consulting is a major industry worldwide, with annual revenues of approximately $300 billion globally (Kennedy, 2023). Despite the scale and ubiquity of management consulting, there is limited rigorous evidence about what management consultants actually do and whether their engagements improve firm performance. This paper addresses these questions using rich administrative data from Belgium.

Understanding the effects of management consulting on firms is important for several reasons. First, firms spend substantial resources on consulting services, and it is unclear whether these expenditures generate commensurate returns. Second, management consulting is one of the primary channels through which management practices diffuse across firms—an important topic given the large and persistent differences in management quality across firms that have been documented in recent research (Bloom et al., 2012; Bloom and Van Reenen, 2007). Third, understanding the effects of consulting can shed light on the broader question of why some firms are better managed than others and what interventions can improve management quality.

Our empirical setting is Belgium, where we have access to unusually rich administrative data. We observe the universe of Belgian firms, their financial statements, and matched employer-employee records. Crucially, we can identify consulting engagements using information on firms' expenditures on consulting services from their financial statements and from the consulting firms' revenue records. This allows us to study both the extensive margin (whether a firm engages consultants) and the intensive margin (how much the firm spends on consulting).

Our empirical strategy uses a difference-in-differences (DiD) design that compares firms experiencing substantial consulting engagements ("consulting events") to synthetic control firms that are similar along key observable dimensions but do not experience such events. We define a consulting event as a sharp increase in a firm's consulting expenditures, which allows us to identify discrete consulting engagements rather than ongoing consulting relationships. We construct synthetic control firms using propensity score matching on pre-event firm characteristics.

Our analysis yields several key findings. First, we find that substantial consulting engagements lead to significant and persistent gains in labor productivity. Revenue per worker increases by approximately 5.8% and value added per worker increases by approximately 5.6% in the four years following a consulting event, relative to synthetic control firms. These productivity gains emerge gradually—they are small in the first year after the event and grow over time, consistent with the idea that consulting recommendations take time to implement and bear fruit.

Second, we find that these productivity gains do not come at the cost of worker welfare. Hourly wages increase by approximately 2.4% following a consulting event, and total hours worked are unaffected. This suggests that workers share in the productivity gains generated by consulting, rather than bearing the costs of restructuring.

Third, we document that consulting engagements trigger significant firm reorganization. In the years following a consulting event, firms experience a temporary surge in both hiring and separations, consistent with workforce restructuring. The composition of the workforce shifts toward more white-collar and management workers, and away from blue-collar workers. Firms also increase their purchases of service inputs, suggesting a reorganization of production that involves outsourcing some activities.

Fourth, we find that consulting engagements are associated with increased market power. Markups increase by approximately 2.6% and profit margins increase following consulting events. This could reflect either genuine efficiency gains that allow firms to charge higher prices or strategic advice from consultants on pricing and market positioning.

Finally, we examine heterogeneity in the effects of consulting by firm size, industry, and the type of consulting engagement. We find that the productivity effects are larger for smaller firms and for firms in manufacturing. We also find that the effects are driven primarily by "strategic" consulting engagements (as opposed to IT or accounting consulting), consistent with the idea that management consulting improves firm strategy and organization.

Our paper contributes to several strands of literature. Most directly, we contribute to the nascent literature on the effects of management consulting on firm performance. The most closely related study is Bloom et al. (2013), who conducted a randomized controlled trial providing free consulting to Indian textile firms and found significant improvements in productivity and profitability. Our study complements this work by studying consulting in a developed country context, using observational data on a large sample of firms, and examining a broader range of outcomes including worker welfare and firm reorganization.

We also contribute to the broader literature on management practices and firm performance (Bloom and Van Reenen, 2007; Bloom et al., 2012). This literature has documented large and persistent differences in management quality across firms and countries, but has been less successful in identifying what interventions can improve management quality. Our finding that management consulting leads to lasting productivity gains suggests that consulting is one effective channel for improving management practices.

Finally, we contribute to the literature on the sources of productivity differences across firms (Syverson, 2011). By documenting the effects of a specific intervention (consulting) on firm productivity, we provide evidence on one mechanism through which productivity differences can be narrowed.

The remainder of the paper is organized as follows. Section 2 describes our data and institutional setting. Section 3 presents our empirical strategy. Section 4 reports our main results on productivity and firm performance. Section 5 examines firm reorganization and worker outcomes. Section 6 explores heterogeneity in the effects. Section 7 concludes.

## 2. Data and Institutional Setting

### 2.1. Data Sources

Our analysis combines several administrative datasets from Belgium:

**Financial Statements Data.** We use the universe of financial statements filed with the Belgian National Bank (NBB). Belgian firms are required to file annual financial statements that contain detailed information on their income statement and balance sheet. Crucially for our purposes, these statements include information on spending on "external services," which includes consulting expenditures.

**Matched Employer-Employee Data.** We use social security records (DMFA) that contain quarterly information on all employment relationships in Belgium, including wages, hours worked, and worker characteristics. We match these records to firms using unique firm identifiers.

**Consulting Firm Data.** We identify consulting firms using their NACE industry codes (specifically NACE 70.22 "Business and other management consultancy activities"). We observe the revenue of these consulting firms, which we can link to their client firms.

**Firm Registry Data.** We use the Crossroads Bank for Enterprises (KBO) for information on firm creation, dissolution, and legal form.

### 2.2. Identifying Consulting Engagements

We identify "consulting events" as sharp increases in a firm's spending on consulting services. Specifically, we define a consulting event in year t if the following conditions are met:

1. The firm's consulting spending in year t exceeds a threshold (we use various thresholds in our analysis, with the baseline being spending above the 90th percentile of the firm's own spending distribution).
2. The firm's consulting spending in year t is at least twice as large as its average spending in the pre-event period (years t−4 to t−1).
3. The firm exists for at least four years before and after the event.

This definition captures discrete consulting engagements—episodes where firms sharply increase their use of consulting services—rather than ongoing consulting relationships. The advantage of this approach is that it identifies events with a clear "before" and "after" period, which is essential for our DiD strategy.

### 2.3. Sample Construction

Our sample covers the period 2002–2019. We restrict attention to private-sector firms with at least 10 employees, excluding the financial sector and public administration. After applying our filters, we identify approximately 5,000 consulting events, which we match to synthetic control firms.

### 2.4. Descriptive Statistics

Table 1 presents descriptive statistics for our sample. The average firm in our sample has approximately 50 employees, revenues of approximately €15 million, and value added per worker of approximately €70,000. Consulting events are associated with a sharp increase in consulting spending: the average firm spends approximately €650,000 on consulting in the event year, compared to approximately €50,000 in the pre-event period.

Consulting events are more common among larger firms, firms in manufacturing and business services, and firms with higher pre-event productivity. However, our matching procedure ensures that our treatment and control groups are balanced on these observable characteristics.

## 3. Empirical Strategy

### 3.1. Difference-in-Differences Design

Our empirical strategy compares firms that experience consulting events ("treated firms") to synthetic control firms that are similar along key observable dimensions but do not experience such events. We estimate the following specification:

y_{it} = α_i + γ_t + Σ_k β_k · 1(k = t − t*_i) · Treated_i + ε_{it}    (1)

where y_{it} is an outcome for firm i in year t, α_i are firm fixed effects, γ_t are year fixed effects, t*_i is the year of the consulting event for treated firm i, Treated_i is an indicator for treated firms, and the coefficients β_k capture the dynamic treatment effects for each event year k relative to the event year.

We also report pooled estimates that aggregate the post-treatment effects:

y_{it} = α_i + γ_t + β · Post_it · Treated_i + ε_{it}    (2)

where Post_it = 1(t ≥ t*_i) for treated firms and their matched controls.

### 3.2. Construction of Synthetic Control Group

We construct synthetic control firms using propensity score matching. For each treated firm, we identify potential control firms that (1) are in the same industry (2-digit NACE), (2) have similar pre-event characteristics, and (3) do not experience a consulting event in a window around the treated firm's event year.

We match on the following pre-event characteristics measured in the year before the event (t−1): log employment, log revenue per worker, log value added per worker, log total assets, profit margin, and the firm's age. We use nearest-neighbor matching with replacement, selecting the five closest control firms for each treated firm.

### 3.3. Identifying Assumptions and Threats

The key identifying assumption of our DiD design is that, in the absence of the consulting event, treated and control firms would have followed parallel trends. We assess the plausibility of this assumption by examining pre-event trends in our outcome variables. As we show in our results, treated and control firms follow very similar trends in the pre-event period, supporting the parallel trends assumption.

A potential concern is that consulting events may be endogenous—firms may hire consultants precisely when they anticipate changes in performance. We address this concern in several ways. First, we show that our results are robust to controlling for pre-event trends in performance. Second, we examine the timing of effects and show that productivity gains emerge gradually over time, which is more consistent with a causal effect of consulting than with selection. Third, we conduct placebo tests using "pseudo-events" defined by sharp increases in non-consulting expenditures and find no effects on productivity.

## 4. Main Results: Productivity and Performance

### 4.1. Labor Productivity

Figure 9 presents our main results on labor productivity. Panels (a) and (b) show results for revenue per worker (in levels and DiD, respectively), while panels (c) and (d) show results for value added per worker. The figures reveal a clear pattern: treated and control firms follow parallel trends in the pre-event period, and treated firms experience a significant increase in labor productivity following the consulting event.

The productivity gains emerge gradually. In the first year after the event, the effects are small and statistically insignificant. By years 2–4, the effects become large and statistically significant. The pooled DiD estimate for revenue per worker is 0.058 (SE 0.024), implying a 5.8% increase in revenue per worker. The corresponding estimate for value added per worker is 0.056 (SE 0.018), implying a 5.6% increase.

Panels (e) and (f) show results for total factor productivity (TFP), which we estimate using a Cobb-Douglas production function with industry-specific factor shares. The TFP results are qualitatively similar to the labor productivity results, with a pooled DiD estimate of 0.006 (SE 0.013), although this estimate is less precisely estimated.

### 4.2. Firm Size

Figure 10 presents results on firm size. Panels (a) and (b) show that revenue increases following consulting events, with a pooled DiD estimate of 0.013 (SE 0.034). However, this estimate is not statistically significant at conventional levels. Panels (c) and (d) show that employment is also largely unaffected, with a pooled DiD estimate of −0.024 (SE 0.023). These results suggest that the productivity gains from consulting are driven by increased output per worker rather than by changes in scale.

### 4.3. Profitability and Financial Performance

Figure 11 presents results on profitability. Panels (a) and (b) show that profit margins decrease slightly following consulting events, with a pooled DiD estimate of −0.007 (SE 0.005). Panels (c) and (d) show that return on capital employed (ROCE) also decreases slightly, with a pooled DiD estimate of −0.017 (SE 0.02). These small negative effects on profitability measures, despite the positive effects on productivity, may reflect the direct costs of the consulting engagement itself.

### 4.4. Market Power

Figure 8 (panel c) shows that consulting engagements are associated with increases in markups. The pooled DiD estimate for markups is approximately 0.026 (SE 0.010), implying a 2.6% increase. This is consistent with consulting improving firms' pricing strategies or product differentiation, allowing them to charge higher prices.

## 5. Firm Reorganization and Worker Outcomes

### 5.1. Workforce Restructuring

A key finding of our paper is that consulting engagements trigger significant firm reorganization. Figure 8 (panel e) shows that in the years following a consulting event, firms experience:

- **Increased hiring:** New hires increase significantly in the event year and the year after.
- **Increased separations:** Worker separations also increase, including both voluntary and involuntary separations (dismissals).
- **Increased management headcount:** The number of management workers increases.
- **Shift toward white-collar workers:** The share of white-collar workers increases, while the share of blue-collar workers decreases.
- **Increased use of temporary workers:** Temporary hours increase in the event year.
- **Increased outsourcing:** Purchases of service inputs increase significantly.

This pattern is consistent with a process of reorganization in which firms restructure their workforce, shift toward more skilled and managerial workers, and outsource some production activities. The temporary nature of the hiring and separation effects (which are concentrated in the first 1–2 years after the event) suggests that the reorganization is a discrete process rather than an ongoing change.

### 5.2. Wages and Hours

Figure 8 (panel d) presents results on worker outcomes. We find that:

- **Hourly wages increase:** The pooled DiD estimate for log hourly wages is positive and significant, implying a wage increase of approximately 2.4%.
- **Hours worked are unaffected:** Total hours per worker show no significant change.
- **Labor share of revenue decreases slightly:** Consistent with productivity gains exceeding wage gains.
- **Labor share of value added is unaffected:** Suggesting that workers maintain their share of the surplus.

These results suggest that consulting engagements benefit workers as well as firms. The wage increases are consistent with workers capturing some of the productivity gains through bargaining, while the stable hours suggest that consulting does not lead to work intensification.

## 6. Heterogeneity

### 6.1. By Firm Size

We examine heterogeneity in the effects of consulting by firm size. We split our sample at the median firm size (approximately 30 employees) and estimate our baseline specification separately for smaller and larger firms.

We find that the productivity effects are substantially larger for smaller firms. The DiD estimate for revenue per worker is approximately 0.08 for firms below the median size, compared to approximately 0.03 for firms above the median. This is consistent with smaller firms having more room for improvement in their management practices and with consulting having a larger marginal effect when baseline management quality is lower.

### 6.2. By Industry

We also examine heterogeneity by industry. We find that the productivity effects are larger in manufacturing than in services. This may reflect the fact that manufacturing firms have more scope for process optimization and reorganization, or that consulting is better suited to improving manufacturing operations.

### 6.3. By Type of Consulting

Not all consulting is the same. We distinguish between different types of consulting engagements based on the industry classification of the consulting firm. Specifically, we separate "strategic/management consulting" (NACE 70.22) from "IT consulting" (NACE 62.02) and "accounting/audit consulting" (NACE 69.20).

We find that the productivity effects are driven primarily by strategic/management consulting engagements, with little effect from IT or accounting consulting. This is consistent with the idea that management consulting improves firm strategy and organization, while IT and accounting consulting serve more operational purposes.

### 6.4. Treatment Intensity

We examine how the effects vary with the intensity of the consulting engagement, measured by total consulting spending. We find a positive relationship between spending intensity and productivity gains, although the relationship is concave—the marginal effect of additional spending decreases at higher levels. This suggests that there are diminishing returns to consulting, but that larger engagements generally produce larger effects.

## 7. Robustness

We conduct several robustness checks to ensure the validity of our findings.

### 7.1. Pre-Trends

We examine pre-event trends for all our outcome variables. In all cases, treated and control firms follow very similar trends in the pre-event period (years t−4 to t−1), supporting the parallel trends assumption.

### 7.2. Placebo Tests

We conduct placebo tests using "pseudo-events" defined by sharp increases in non-consulting expenditures (e.g., spending on raw materials or capital goods). We find no significant effects of these pseudo-events on labor productivity, confirming that our results are specific to consulting expenditures.

### 7.3. Alternative Matching

We test the robustness of our results to alternative matching procedures, including exact matching on industry and size bins, coarsened exact matching, and matching with different numbers of control firms. Our results are qualitatively and quantitatively similar across all matching procedures.

### 7.4. Alternative Event Definitions

We test alternative definitions of consulting events, varying the threshold for what constitutes a "sharp increase" in consulting spending. Our results are robust to these alternative definitions, although the point estimates vary somewhat with the threshold used.

### 7.5. Firm Fixed Effects and Year × Sector Fixed Effects

We estimate specifications with firm fixed effects only, and with firm fixed effects combined with year × sector fixed effects. The latter specification accounts for time-varying industry shocks that may differentially affect treated and control firms. Our results are robust to both specifications.

## 8. Discussion and Interpretation

### 8.1. What Do Consultants Do?

Our results paint a consistent picture of what management consultants do. Consulting engagements trigger a process of firm reorganization that unfolds over several years. In the short run, firms restructure their workforce—increasing both hiring and separations—and shift toward a more skilled and managerial workforce. They also increase their purchases of service inputs, consistent with outsourcing some activities. Over time, these organizational changes translate into higher labor productivity.

This picture is consistent with the view that management consultants help firms implement organizational changes that they may have difficulty implementing on their own. The temporary nature of the consulting engagement—spending is concentrated in the event year and declines sharply thereafter—suggests that consultants serve as catalysts for change rather than as ongoing advisors.

### 8.2. Comparison with Bloom et al. (2013)

Our findings complement and extend the results of Bloom et al. (2013), who conducted a randomized controlled trial providing free consulting to Indian textile firms. Both studies find significant productivity gains from consulting. However, there are important differences in context and magnitude.

Bloom et al. (2013) study small textile firms in a developing country, where baseline management quality is very low. They find very large effects (17% improvement in productivity), consistent with the large scope for improvement in their setting. In contrast, we study firms in a developed country where baseline management quality is presumably higher, and we find smaller but still substantial effects (5–6% improvement in productivity). The difference in magnitudes is consistent with diminishing returns to management quality improvements.

### 8.3. Implications for the Productivity Literature

Our findings have implications for the literature on productivity differences across firms (Syverson, 2011). The fact that consulting can improve firm productivity by 5–6% suggests that management practices are an important source of productivity differences, and that these differences can be narrowed through specific interventions. However, the fact that not all firms hire consultants—even when the returns appear to be substantial—raises questions about the barriers to adopting better management practices.

### 8.4. Implications for Workers

An important finding of our paper is that consulting engagements benefit workers as well as firms. Wages increase by approximately 2.4% following a consulting event, and hours worked are unaffected. This suggests that the productivity gains from consulting are shared between firms and workers, rather than accruing entirely to firm owners.

However, the process of reorganization may involve costs for some workers. The increase in separations suggests that some workers are displaced during the reorganization process. While our aggregate wage results suggest that the average worker benefits, it is possible that some displaced workers experience significant losses. Examining the distributional effects of consulting-induced reorganization is an important direction for future research.

## 9. Conclusion

This paper studies the effects of management consulting on firm performance using rich Belgian administrative data. We find that substantial consulting engagements lead to persistent labor productivity gains of approximately 5–6%, which emerge gradually over the four years following the engagement. These gains are accompanied by firm reorganization—a shift toward more skilled workers, increased outsourcing, and temporary increases in hiring and separations. Workers benefit from the productivity gains through higher wages, while firms benefit through higher markups and market power.

Our findings contribute to the growing literature on management practices and firm performance by documenting the effects of a specific and common intervention—management consulting—on a broad range of firm outcomes. The results suggest that management consulting is an effective channel for improving management practices and firm productivity, at least in the developed-country context we study.

Several important questions remain for future research. First, what specific management practices do consultants recommend, and which of these drive the productivity gains? Second, why don't more firms hire consultants, given the apparently large returns? Third, what are the distributional consequences of consulting-induced firm reorganization for different types of workers? Answering these questions will require even richer data on the content of consulting engagements and their effects on individual workers—a promising direction for future research.
Management and strategy consulting is a large and growing industry — approximately $300 billion globally — yet it remains remarkably opaque. Despite widespread use by firms and governments, the economic effects of consulting have been largely unstudied due to data limitations. Are consultants productivity enhancers who transfer best practices across firms? Or are they primarily engaged in rent-shifting, helping powerful clients extract value from workers?

### Research Questions

1. **Who hires consultants?** What are the characteristics of firms that purchase consulting services?
2. **What do consulting engagements look like?** How much do firms spend, for how long, and how frequently?
3. **What are the causal effects?** Does consulting improve client firm productivity, and through what channels?
4. **Who benefits?** Do productivity gains come at workers' expense, or are they broadly shared?

### Key Contribution

This is the first paper to study consulting using universal administrative data that covers all business-to-business transactions in a national economy, allowing comprehensive and unbiased measurement of consulting activity and its effects.

---

## 2. Data and Methodology

### 2.1 Universal VAT Transaction Data

The paper exploits a unique data source: the complete set of business-to-business transactions recorded through Belgium's value-added tax system (2002-2023).

**Key features:**
- Covers ALL B2B transactions in Belgium (not just publicly traded firms)
- Identifies consulting engagements through NACE industry codes of service providers
- Links to firm-level balance sheet and employment data
- Allows construction of firm-level consulting expenditure over time
- Universal coverage eliminates selection bias in who appears in the data

### 2.2 Identifying Consulting Events

The paper defines "consulting events" as sharp increases in consulting expenditure:
- First-time consulting purchases (extensive margin)
- Significant increases in existing spending (intensive margin)
- Episodic nature: most engagements last less than one year

### 2.3 Difference-in-Differences Design

The identification strategy exploits the sharp, episodic nature of consulting events:
- **Treatment:** Firms that begin purchasing consulting in a given year
- **Control:** Similar firms that do not purchase consulting (matched on pre-event characteristics)
- **Time horizon:** Effects tracked over 5 years post-event
- **Robustness:** Multiple matching specifications, event study graphs, pre-trend tests

---

## 3. Take-Up Patterns

### 3.1 Who Hires Consultants?

**Firm size:** Consulting take-up is strongly concentrated among larger firms. The probability of hiring consultants increases monotonically with firm size.

**Productivity:** A striking U-shaped pattern emerges:
- High-productivity firms hire consultants (to maintain/extend their advantage)
- Low-productivity firms also hire consultants (to catch up)
- Middle-productivity firms are least likely to hire consultants

**Profitability:** Similar U-shaped pattern for profitability, suggesting both high-performing firms seeking to innovate and struggling firms seeking turnaround advice.

### 3.2 Engagement Characteristics

| Characteristic | Finding |
|---------------|---------|
| Average spend | 3% of payroll |
| Duration | Typically < 1 year (episodic) |
| Frequency | Most firms hire consultants episodically, not continuously |
| Timing | Concentrated around organizational changes, strategic shifts |

---

## 4. Main Results

### 4.1 Productivity Effects

**Core finding:** Consulting leads to a 3.6% increase in labor productivity over five years.

**Decomposition:**
- Revenue: Stable or slightly growing
- Employment: Modest reductions (firms become more efficient, not just smaller)
- The productivity gain is real — firms produce more (or the same) with fewer workers

**Timing:** Effects are gradual, emerging over 2-3 years and stabilizing around year 5. This is consistent with the organizational change literature (Bandiera et al. 2020: CEO effects take 3 years).

### 4.2 Wage and Labor Share Effects

**Average wages:** Rise by 2.7% following consulting events.

**Labor's share of value added:** No decline. This is a critical finding — it suggests that productivity gains are shared between capital and labor, rather than being extracted from workers.

**Interpretation:** Consulting appears to improve overall firm productivity, with benefits shared across stakeholders. This contradicts the rent-shifting hypothesis that consultants primarily help management extract rents from workers.

### 4.3 Organizational Changes

Consulting events are associated with:
- **Dismissal rates:** Small increases (consistent with restructuring)
- **Services procurement:** Higher (firms outsource more services)
- **Labor outsourcing:** Reduced (firms bring some activities back in-house)
- **Organizational structure:** Evidence of restructuring, particularly in management layers

### 4.4 Heterogeneity

**Key finding:** Larger productivity gains for initially less productive firms.

This suggests that consulting improves **allocative efficiency** — helping poorly managed firms catch up to best practices. This is consistent with Bloom et al.'s (2012) finding of large, persistent management practice differences across firms, and with the consulting industry's self-description as a mechanism for diffusing best practices.

---

## 5. Validation: Expert Predictions

The authors surveyed both academic economists and consulting professionals before analyzing the data:

| Prediction | Academics | Practitioners |
|-----------|-----------|---------------|
| Consulting improves productivity | ~50% agree | ~85% agree |
| Gains come at workers' expense | ~40% agree | ~15% agree |
| Larger effects for worse firms | ~60% agree | ~70% agree |

The findings broadly validate the practitioner consensus (productivity enhancement) while contradicting the academic skepticism about rent-shifting.

---

## 6. Theoretical Implications

### 6.1 Consulting as Knowledge Transfer

The results are consistent with a model where consultants transfer management knowledge across firms:
- Firms hire consultants to access best practices they lack internally
- The transfer is most valuable for less productive firms (larger knowledge gap)
- Effects are gradual, consistent with organizational learning and implementation

### 6.2 Complementarity with Internal Capabilities

Consulting is most effective when it complements internal firm capabilities:
- Large firms benefit more (can implement recommendations)
- Firms with some absorptive capacity benefit most
- Pure knowledge transfer without implementation capacity yields limited effects

### 6.3 Connection to Management Practices Literature

The findings bridge the gap between:
- **Bloom and Van Reenen (2007, 2012):** Large persistent differences in management practices across firms
- **Ichniowski et al. (1997):** Complementary HRM practice clusters matter
- **This paper:** Consulting is one mechanism through which management practice improvements spread

---

## 7. Relation to Literature

### Management Practices and Productivity
- Bloom, N. and Van Reenen, J. (2007). "Measuring and Explaining Management Practices Across Firms and Countries." Quarterly Journal of Economics, 122(4), 1351-1408.
- Bloom, N., Genakos, C., Sadun, R., and Van Reenen, J. (2012). "Management Practices Across Firms and Countries." Academy of Management Perspectives, 26(1), 12-33.
- Bloom, N., Eifert, B., Mahajan, A., McKenzie, D., and Roberts, J. (2013). "Does Management Matter? Evidence from India." Quarterly Journal of Economics, 128(1), 1-51.

### Complementarities in Organizations
- Milgrom, P. and Roberts, J. (1990). "The Economics of Modern Manufacturing." American Economic Review, 80(3), 511-528.
- Ichniowski, C., Shaw, K., and Prennushi, G. (1997). "The Effects of Human Resource Management Practices on Productivity." American Economic Review, 87(3), 291-313.

### CEO Behavior and Organizational Change
- Bandiera, O., Prat, A., Hansen, S., and Sadun, R. (2020). "CEO Behavior and Firm Performance." Journal of Political Economy, 128(4), 1325-1369.

### Consulting Industry
- Canback, S. (1998). "The Logic of Management Consulting." Journal of Management Consulting, 10(2).
- Kipping, M. and Clark, T. (2012). The Oxford Handbook of Management Consulting. Oxford University Press.

---

## References

Bloom, N., Eifert, B., Mahajan, A., McKenzie, D., and Roberts, J. (2013). Does management matter? Evidence from India. *Quarterly Journal of Economics*, 128(1):1–51.

Bloom, N., Sadun, R., and Van Reenen, J. (2012). The organization of firms across countries. *Quarterly Journal of Economics*, 127(4):1663–1705.

Bloom, N. and Van Reenen, J. (2007). Measuring and explaining management practices across firms and countries. *Quarterly Journal of Economics*, 122(4):1351–1408.

Kennedy, Information (2023). *The Global Consulting Market*. Kennedy Information.

Syverson, C. (2011). What determines productivity? *Journal of Economic Literature*, 49(2):326–365.
Bandiera, O., Prat, A., Hansen, S., and Sadun, R. (2020). "CEO Behavior and Firm Performance." Journal of Political Economy, 128(4), 1325-1369.

Bloom, N. and Van Reenen, J. (2007). "Measuring and Explaining Management Practices Across Firms and Countries." Quarterly Journal of Economics, 122(4), 1351-1408.

Bloom, N., Eifert, B., Mahajan, A., McKenzie, D., and Roberts, J. (2013). "Does Management Matter? Evidence from India." Quarterly Journal of Economics, 128(1), 1-51.

Bloom, N., Genakos, C., Sadun, R., and Van Reenen, J. (2012). "Management Practices Across Firms and Countries." Academy of Management Perspectives, 26(1), 12-33.

Ichniowski, C., Shaw, K., and Prennushi, G. (1997). "The Effects of Human Resource Management Practices on Productivity." American Economic Review, 87(3), 291-313.

Milgrom, P. and Roberts, J. (1990). "The Economics of Modern Manufacturing: Technology, Strategy, and Organization." American Economic Review, 80(3), 511-528.

Roberts, J. (2004). The Modern Firm: Organizational Design for Performance and Growth. Oxford University Press.
