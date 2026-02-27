# The Effects of Human Resource Management Practices on Productivity

**Authors:** Casey Ichniowski, Kathryn Shaw, Giovanna Prennushi
**Year:** 1997
**Journal:** American Economic Review, Vol. 87, No. 3, pp. 291-313
**Archived Date:** 2026-02-24
**Content Level:** L2 (Comprehensive structured summary with S1-S6)

---

## Abstract

The authors investigate the productivity effects of innovative employment practices using data from a sample of thirty-six homogeneous steel production lines owned by seventeen companies. The productivity regressions demonstrate that lines using a set of innovative work practices, which include incentive pay, teams, flexible job assignments, employment security, and training, achieve substantially higher levels of productivity than do lines with the more traditional approach, which includes narrow job definitions, strict work rules, and hourly pay with close supervision. Their results are consistent with recent theoretical models which stress the importance of complementarities among work practices.

---

## 1. Introduction

Innovative human resource management (HRM) practices have become increasingly widespread in U.S. manufacturing, yet their effects on productivity remain contested. Proponents argue that bundles of practices — such as team-based production, incentive pay, training, employment security, and information sharing — create synergies that raise productivity beyond what any single practice could achieve. Skeptics counter that such practices are costly, difficult to implement, and may not survive rigorous empirical scrutiny.

The theoretical literature provides a clear hypothesis: if HRM practices are complements (in the sense of Milgrom and Roberts, 1990, 1995), then adopting them as a system should raise productivity more than adopting any subset. This complementarity hypothesis has strong theoretical foundations in the theory of supermodular functions, but empirical evidence has been limited.

### Research Questions

This paper asks three central questions:

1. Do innovative HRM practices raise productivity?
2. Is it the system of practices (adopted together) that matters, or do individual practices independently raise productivity?
3. Are the data consistent with the theoretical prediction of complementarities among HRM practices?

### Why Steel Finishing Lines?

The study focuses on steel finishing lines for a critical methodological reason: these production lines produce a highly homogeneous product (coils of sheet steel with measurable quality attributes), operate with nearly identical capital equipment across plants, and differ primarily in their HRM practices. This homogeneity dramatically reduces omitted variable bias — the "apples to oranges" problem that plagues cross-industry or cross-occupation studies.

Each steel finishing line is a continuous process production unit where raw steel is cleaned, annealed (heat-treated), and coated. The key performance metric is **uptime** — the percentage of scheduled operating time that the line is actually producing steel. Uptime is an ideal productivity measure because it is:
- Objective and continuously recorded
- Comparable across lines using identical technology
- Directly affected by worker effort, skill, and coordination
- Not confounded by product mix differences

---

## 2. Data and Methodology

### 2.1 Sample

The dataset covers **36 homogeneous steel finishing lines** across **17 companies** in the United States. Data were collected through:
- Monthly production records (uptime data) over multiple years
- Detailed surveys of HRM practices at each line
- Site visits and interviews with managers and workers

The sample was constructed to maximize homogeneity: all lines produce flat-rolled steel products, use similar capital equipment (continuous annealing and coating lines), and operate in the same industry subject to similar market conditions.

### 2.2 HRM Practice Variables

The study measures seven categories of HRM practices:

| Practice | Traditional | Innovative |
|----------|------------|------------|
| **Incentive Pay** | Hourly wages, narrow pay grades | Profit sharing, team bonuses, pay-for-knowledge |
| **Recruiting & Selection** | Minimal screening, union hiring hall | Extensive screening, aptitude tests, multiple interviews |
| **Teamwork** | Individual job assignments | Problem-solving teams, work teams |
| **Job Flexibility** | Narrow job classifications (30+) | Broad classifications (1-4), job rotation |
| **Employment Security** | Layoffs common | Employment guarantees, no-layoff pledges |
| **Training** | Minimal (< 1 day/year) | Extensive (> 40 hours/year) |
| **Communication** | Top-down only | Information sharing, regular meetings |

### 2.3 HRM System Classification

A key methodological innovation is the classification of lines into **HRM systems** rather than analyzing individual practices. The authors identify four main HRM systems:

**System 1 (Traditional):** Narrow job definitions, strict work rules, hourly pay with no contingent compensation, close supervision, minimal screening, no teams, minimal training, minimal communication. (Lines: 7)

**System 2 (Transitional Low):** Some innovative features (e.g., incentive pay or modest training) but within a mostly traditional framework. (Lines: 10)

**System 3 (Transitional High):** Multiple innovative practices but incomplete system adoption. Missing one or more key complementary practices. (Lines: 11)

**System 4 (Innovative):** Full cluster of innovative practices: incentive pay, teams, flexible jobs, employment security, extensive training, and information sharing. All practices adopted together as a coherent system. (Lines: 8)

### 2.4 Econometric Approach

The primary estimation equation is:

$$\text{Uptime}_{it} = \alpha + \beta \cdot \text{HRM}_{it} + \gamma \cdot X_{it} + \mu_i + \epsilon_{it}$$

where:
- Uptime_it is the percentage of scheduled operating time line i is running in month t
- HRM_it represents either individual practice indicators or system indicators
- X_it are controls (capital vintage, product mix, etc.)
- μ_i are line fixed effects (in fixed-effects specifications)
- ε_it is the error term

The authors estimate both OLS and fixed-effects models, and compare:
1. **Individual practice effects** (each practice entered separately)
2. **System effects** (dummy variables for HRM systems 1-4)
3. **Interaction effects** (all pairwise interactions among practices)

---

## 3. Main Results

### 3.1 System Effects on Productivity

The headline finding is stark and dramatic:

**Lines with the full innovative HRM system (System 4) have uptime that is 6.7 percentage points higher than lines with the traditional system (System 1).**

This is economically very significant: given that average uptime is approximately 88%, a 6.7 percentage point increase represents a substantial productivity gain. In dollar terms, this translates to approximately $2.2 million per year in additional output per line.

| HRM System | Uptime (%) | Difference vs. System 1 |
|------------|-----------|------------------------|
| System 1 (Traditional) | ~88.0% | — |
| System 2 (Transitional Low) | ~89.5% | +1.5 pp |
| System 3 (Transitional High) | ~92.0% | +4.0 pp |
| System 4 (Innovative) | ~94.7% | +6.7 pp |

The progression from System 1 to System 4 shows a clear pattern: productivity increases with the comprehensiveness of the innovative HRM system.

### 3.2 Individual Practice Effects: Small and Often Insignificant

When individual practices are entered separately into the regression:

- **Incentive pay alone:** Small positive effect, often statistically insignificant
- **Teams alone:** Small positive effect
- **Training alone:** Positive but small
- **Any single practice:** Coefficient much smaller than the system effect

**Key finding:** The sum of individual practice effects is much less than the system effect. This is the hallmark of complementarity — the whole is greater than the sum of the parts.

### 3.3 Interaction Effects

When pairwise interactions are included:

- Many interaction terms are positive and significant
- The joint effect of pairs of practices is greater than the sum of individual effects
- The full system effect exceeds even the sum of all individual + pairwise effects

This finding is consistent with higher-order complementarities (three-way, four-way interactions), though statistical power limits the ability to estimate these precisely.

### 3.4 Within-Line Changes

The panel nature of the data allows analysis of productivity changes when lines change their HRM systems:

- Lines that adopted innovative systems saw statistically significant productivity improvements
- Lines that partially adopted (System 2 or 3) saw smaller improvements
- **Transition time:** It takes approximately 12-18 months for the full productivity effect to materialize after system adoption

### 3.5 Robustness Checks

The results are robust to:
- Line fixed effects (controlling for unobserved time-invariant differences)
- Capital vintage controls
- Product mix controls
- Seasonal effects
- Alternative definitions of HRM systems
- Different time windows

---

## 4. Theoretical Framework: Complementarities

### 4.1 The Complementarity Hypothesis

The paper's results are interpreted through the lens of complementarity theory (Milgrom and Roberts, 1990, 1995):

**Definition:** Two practices x₁ and x₂ are complements if adopting both raises productivity more than the sum of adopting each individually:

$$f(x_1, x_2) - f(0, x_2) - f(x_1, 0) + f(0, 0) > 0$$

This condition — the supermodularity condition — predicts that:
1. Complementary practices will cluster at optima (adopted together or not at all)
2. Partial adoption will be less effective than full adoption
3. The marginal return to each practice increases in the level of the other practices

### 4.2 Why These Practices Are Complements

The paper provides intuitive economic logic for the complementarities:

**Incentive pay + Teams:** Incentive pay motivates effort, but team-based production requires cooperation. Team bonuses (rather than individual piece rates) align incentives with cooperative goals.

**Training + Flexible jobs:** Training equips workers with multiple skills; flexible job assignments allow workers to use those skills across tasks. Without flexibility, training is wasted; without training, flexibility is impossible.

**Employment security + Effort:** Workers invest in firm-specific skills and cooperative effort only if they expect to benefit from those investments. Employment security provides the necessary long time horizon.

**Communication + Problem-solving teams:** Information sharing enables teams to diagnose and solve production problems. Without information, teams cannot function; without teams, information has no channel for action.

### 4.3 The Failure of Partial Adoption

A critical implication is that partial adoption can be worse than no adoption at all. For example:
- Incentive pay without teams may encourage counterproductive individual competition
- Teams without training may produce coordination costs without skill benefits
- Employment security without incentive pay may reduce effort motivation

This explains the observation that many firms attempt single-practice innovations and see no results — they are missing the complementary practices that make the focal practice effective.

---

## 5. Implications

### 5.1 For Management Practice

1. **Systems thinking:** Firms should adopt HRM practices as coherent systems, not piecemeal
2. **All or nothing:** The returns to partial adoption are low; the returns to full adoption are high
3. **Patience required:** Full productivity effects take 12-18 months to materialize
4. **Switching costs:** Moving from traditional to innovative systems requires simultaneous change across multiple dimensions, which is organizationally difficult

### 5.2 For Economic Theory

1. **Complementarity matters empirically:** The theoretical predictions of Milgrom and Roberts are confirmed in a well-controlled setting
2. **Multiple equilibria:** Both the traditional and innovative systems are locally stable; firms can be "stuck" in either one
3. **Path dependence:** Initial conditions (union contracts, management philosophy, capital structure) determine which system a firm adopts

### 5.3 For Policy

1. **Diffusion barriers:** Even when the productivity benefits of innovative HRM are clear, adoption is slow because of complementarity-driven switching costs
2. **Training subsidies:** Subsidizing one practice (e.g., training) may be ineffective if complementary practices are not also adopted
3. **Institutional constraints:** Union contracts and regulatory requirements may prevent adoption of the full innovative system

---

## 6. Relation to Literature

### Foundational Theory
- **Milgrom and Roberts (1990):** "The Economics of Modern Manufacturing: Technology, Strategy, and Organization" — formal theory of complementarities in production
- **Milgrom and Roberts (1995):** "Complementarities and Fit: Strategy, Structure, and Organizational Change in Manufacturing" — extension to organizational practices
- **Topkis (1978):** Mathematical theory of supermodular functions

### Prior Empirical Work
- **MacDuffie (1995):** Flexible production systems in auto assembly — first large-sample evidence of HRM bundling effects
- **Huselid (1995):** High Performance Work Practices and turnover/productivity — cross-industry evidence
- **Arthur (1994):** Steel minimills — control vs. commitment HRM systems
- **Kochan et al. (1986):** Transformation of American Industrial Relations

### Subsequent Work
- **Bloom and Van Reenen (2007):** Extended HRM-productivity analysis to cross-country management practices
- **Bloom et al. (2012):** 10,000+ organizations across 20 countries, confirming the management practices-performance link
- **Bartel et al. (2007):** IT and HRM complementarities in valve manufacturing
- **Brynjolfsson and Milgrom (2010):** Comprehensive review of complementarity in organizations

---

## 7. Discussion: Why the Steel Industry?

The choice of steel finishing lines deserves special emphasis because it addresses the central identification challenge in this literature. Cross-industry studies (Huselid 1995; MacDuffie 1995) face the objection that HRM differences are confounded with industry, technology, product, and market differences. By studying a single, highly standardized production process, Ichniowski et al. hold constant virtually everything except HRM practices.

The steel finishing line setting offers:
- **Technology homogeneity:** All lines use similar continuous-process equipment
- **Product homogeneity:** All lines produce flat-rolled steel coils
- **Output measurement:** Uptime is objective, continuous, and comparable
- **Variation in HRM:** Despite technological similarity, lines differ substantially in HRM practices (due to different ownership, union contracts, and management philosophies)

This design provides arguably the cleanest empirical test of HRM complementarities available in any industry.

---

## 8. Conclusion

This study provides the strongest available evidence that HRM practices are complements — that they raise productivity when adopted as a coherent system but have limited effects individually. The 6.7 percentage point uptime difference between innovative and traditional HRM systems is both statistically robust and economically substantial.

The results validate the theoretical predictions of Milgrom and Roberts (1990, 1995): complementary practices cluster at optima, partial adoption is suboptimal, and the transition from one system to another is difficult because it requires simultaneous change across multiple dimensions.

The steel finishing line setting provides a rare combination of technological homogeneity and HRM variation that allows unusually clean causal identification. The findings have broad implications for management practice (adopt systems, not individual practices), economic theory (complementarities are empirically important), and policy (subsidizing single practices may be ineffective).

---

## References

Arthur, J. B. (1994). "Effects of Human Resource Systems on Manufacturing Performance and Turnover." Academy of Management Journal, 37(3), 670-687.

Bartel, A. P., Ichniowski, C., and Shaw, K. (2007). "How Does Information Technology Affect Productivity? Plant-Level Comparisons of Product Innovation, Process Improvement, and Worker Skills." Quarterly Journal of Economics, 122(4), 1721-1758.

Bloom, N. and Van Reenen, J. (2007). "Measuring and Explaining Management Practices Across Firms and Countries." Quarterly Journal of Economics, 122(4), 1351-1408.

Bloom, N., Genakos, C., Sadun, R., and Van Reenen, J. (2012). "Management Practices Across Firms and Countries." Academy of Management Perspectives, 26(1), 12-33.

Brynjolfsson, E. and Milgrom, P. (2010). "Complementarity in Organizations." In Gibbons, R. and Roberts, J. (eds.), The Handbook of Organizational Economics.

Huselid, M. A. (1995). "The Impact of Human Resource Management Practices on Turnover, Productivity, and Corporate Financial Performance." Academy of Management Journal, 38(3), 635-672.

Kochan, T. A., Katz, H. C., and McKersie, R. B. (1986). The Transformation of American Industrial Relations. Basic Books.

MacDuffie, J. P. (1995). "Human Resource Bundles and Manufacturing Performance: Organizational Logic and Flexible Production Systems in the World Auto Industry." Industrial and Labor Relations Review, 48(2), 197-221.

Milgrom, P. and Roberts, J. (1990). "The Economics of Modern Manufacturing: Technology, Strategy, and Organization." American Economic Review, 80(3), 511-528.

Milgrom, P. and Roberts, J. (1995). "Complementarities and Fit: Strategy, Structure, and Organizational Change in Manufacturing." Journal of Accounting and Economics, 19(2-3), 179-208.

Topkis, D. M. (1978). "Minimizing a Submodular Function on a Lattice." Operations Research, 26(2), 305-321.
