# Behavioral Corporate Finance

**Authors:** Ulrike Malmendier
**Publication:** Handbook of Behavioral Economics, Volume 1, Chapter 6
**Year:** 2018
**Editors:** B. Douglas Bernheim, Stefano DellaVigna, David Laibson
**Publisher:** North-Holland/Elsevier
**Pages:** 277-379
**DOI:** 10.1016/bs.hesbe.2018.07.001

---

## Abstract

Behavioral corporate finance studies the joint effect of (i) capital market participants' deviations from rationality and (ii) corporate managers' deviations from rationality on corporate decisions and capital market outcomes. This chapter reviews research on three main themes: biased investors and how they affect managers' financing and investment decisions, biased managers and how they affect managers' financing and investment decisions when there are rational investors, and biased third parties (such as board members, auditors, analysts, or government officials) and how they affect corporate decisions.

---

## 1. Introduction

The field of behavioral corporate finance emerged from recognizing that standard corporate finance theory's predictions often diverge from empirical observations. Traditional theories assume that all market participants are fully rational—both managers making corporate decisions and investors pricing securities. Behavioral corporate finance relaxes these assumptions to study how psychological biases affect corporate decisions and market outcomes.

### 1.1 Three Perspectives Framework

The field can be organized around three perspectives:

1. **Biased Investors**: How do irrational investors affect corporate decisions when managers are rational? Managers may exploit or cater to investor biases.

2. **Biased Managers**: How do biased managers make corporate decisions when investors are rational? Overconfident CEOs may overinvest, make value-destroying acquisitions, or choose suboptimal financing.

3. **Biased Third Parties**: How do biases of board members, analysts, auditors, and regulators affect corporate outcomes?

### 1.2 Scope and Methodology

The chapter focuses on empirical evidence while presenting theoretical frameworks that guide interpretation. Key methodological contributions include:
- Development of behavioral measures (Longholder, Holder 67)
- Identification strategies for causal inference
- Survey methodology for eliciting beliefs

---

## 2. Biased Investors

### 2.1 Market Timing

The market timing hypothesis posits that rational managers exploit irrational investors by issuing equity when overvalued and repurchasing when undervalued.

**Key Evidence:**
- Baker and Wurgler (2002): External finance weighted-average market-to-book ratio has persistent negative effect on leverage
- Equity issuances cluster after positive returns and high valuations
- Long-run underperformance following IPOs and SEOs

**Theoretical Framework:**
- Myers and Majluf (1984) vs. behavioral timing
- Rational signaling vs. exploitation of mispricing

### 2.2 Catering

Managers may cater to investor preferences even when those preferences are irrational.

**Dividend Catering (Baker and Wurgler, 2004):**
- "Dividend premium" = valuation difference between dividend payers and non-payers
- Firms more likely to initiate dividends when premium is high
- Aggregate dividend policy responds to investor sentiment

**Name Changes (Cooper et al., 2001):**
- Dot-com name changes during bubble yielded 74% abnormal returns
- Reverse pattern after bubble burst

**Stock Splits (Baker et al., 2009):**
- Firms split to cater to small investors' preference for low-priced stocks
- Nominal share price reflects catering incentives

### 2.3 Investor Sentiment and Corporate Decisions

**Investment Sensitivity:**
- Polk and Sapienza (2009): Investment responds to discretionary accruals (mispricing proxy)
- Effect strongest for equity-dependent firms

**Financing Choices:**
- Henderson et al. (2006): International evidence on market timing
- Kim and Weisbach (2008): Proceeds from equity issuances often held as cash

---

## 3. Biased Managers: Overconfidence

### 3.1 Measuring Managerial Overconfidence

**The Longholder Measure:**

The Longholder measure, introduced in Malmendier and Tate (2005, 2008), identifies overconfident CEOs through their personal portfolio decisions:

- CEOs receive stock options as compensation
- Rational CEOs should exercise options early (after vesting) given underdiversification
- CEOs who hold options until expiration (or into final year) despite 67% moneyness reveal overconfidence

**Key Properties:**
- Based on revealed preferences, not survey responses
- CEO-level (not firm-level) measure
- Persistent within-CEO over time
- Predicts ex-post option exercise patterns

**Holder 67 Variant:**
- Identifies CEOs who fail to exercise options that are 67% in-the-money
- Captures portfolio under-diversification
- More conservative threshold than Longholder

**Alternative Measures:**
1. **Media-based measures**: Frequency of "confident" vs. "cautious" language in press descriptions
2. **Survey-based measures**: CFO expectations from Duke survey
3. **Earnings forecasts**: Optimistic guidance patterns

### 3.2 Overconfidence and Investment

**Theoretical Predictions:**

Overconfident managers:
- Overestimate project returns
- Believe external financing is too costly (due to perceived undervaluation)
- Overinvest when internal funds available
- Underinvest when external financing required

**Empirical Evidence (Malmendier and Tate, 2005):**

Investment-cash flow sensitivity:
- Longholder CEOs: Higher sensitivity to cash flow
- Effect concentrated in equity-dependent firms
- Not explained by information signaling

Key regression specification:
```
Investment_it = α + β1(Overconfident_it × Cash Flow_it) + β2(Cash Flow_it) + Controls + ε_it
```

Results:
- β1 significantly positive
- Overconfident CEOs invest more per dollar of cash flow
- Effect is 3-5 percentage points higher sensitivity

### 3.3 Overconfidence and Mergers & Acquisitions

**Theoretical Framework:**

Overconfident bidders:
- Overestimate synergies
- Overestimate their ability to manage target
- More likely to complete acquisitions
- More likely to overpay

**Empirical Evidence (Malmendier and Tate, 2008):**

Acquisition propensity:
- Longholder CEOs 65% more likely to make acquisitions
- Effect stronger for diversifying acquisitions
- Effect stronger when internal financing available

Market reaction:
- Announcements by Longholder CEOs: -90 basis points lower returns
- Market discounts deals by overconfident acquirers

Deal characteristics:
- More cash financing (believe equity undervalued)
- More diversifying (overestimate ability to manage unfamiliar businesses)

### 3.4 Financing Decisions

**Capital Structure:**

Overconfident managers:
- Prefer internal to external financing
- Among external sources, prefer debt to equity
- Result: Higher leverage ratios

**Pecking Order Implications:**
- Standard pecking order: Information asymmetry → internal funds preferred
- Behavioral pecking order: Overconfidence → same ordering, different mechanism

**Debt vs. Equity Choice:**
- Perceived undervaluation of equity
- Optimism about debt servicing capacity
- Evidence from financing flows around acquisitions

---

## 4. Other Managerial Biases

### 4.1 Experience Effects

**Depression Babies (Malmendier and Nagel, 2011):**

Managers' formative experiences shape risk attitudes:
- CEOs who experienced Great Depression: More conservative financing
- Vietnam-era CEOs: Different risk profiles
- 2008 crisis exposure affects subsequent decisions

**Mechanism:**
- Availability heuristic
- Overweighting personal experience
- Persistence of early-life effects

### 4.2 Miscalibration

Beyond overconfidence in mean estimates, managers may be miscalibrated:
- Confidence intervals too narrow
- Underestimate variance of outcomes
- Ben-David, Graham, and Harvey (2013): CFO forecasts systematically miscalibrated

### 4.3 Reference Points and Loss Aversion

**Acquisition Premiums:**
- Baker, Pan, and Wurgler (2012): 52-week high as reference point
- Premium relative to peak predicts deal completion
- Target shareholders anchor on historical highs

**Exercise Decisions:**
- Option exercise patterns reflect reference dependence
- Stock price path affects timing beyond rational models

---

## 5. Corporate Governance and Biased Third Parties

### 5.1 Board Composition

**Director Selection:**
- Overconfident CEOs select like-minded directors
- Confirmation bias in board composition
- Echo chamber effects

**Director Experience:**
- Directors with crisis experience: More conservative monitoring
- Network effects propagate biases

### 5.2 Analysts

**Analyst Overconfidence:**
- Overconfident analysts issue more optimistic forecasts
- Career concerns interact with biases
- Herding in analyst recommendations

**Conflicts of Interest:**
- Affiliated analyst optimism
- Investment banking relationships
- Regulatory responses (Global Settlement)

### 5.3 Auditors

**Audit Quality:**
- Familiarity breeds accommodation
- Mandatory rotation debates
- Independence vs. industry expertise trade-off

---

## 6. Networks and Social Interactions

### 6.1 Executive Networks

**Board Interlocks:**
- Behaviors spread through board connections
- Option backdating clusters in networks
- Acquisition activity propagates

**Educational Networks:**
- Business school connections
- Military backgrounds
- Regional clustering

### 6.2 Network Effects on Corporate Outcomes

**M&A Contagion:**
- Acquisition activity spreads through networks
- Peer effects in deal-making
- Information vs. behavioral channels

**Financing Decisions:**
- Capital structure mimicking
- IPO waves and peer effects

---

## 7. Quantifying the Field

### 7.1 Literature Growth

Analysis of 233 behavioral corporate papers reveals:
- Approximately 45% focus on biased investors
- Approximately 45% focus on biased managers
- Approximately 10% focus on biased third parties

### 7.2 Research Frontiers

**Emerging Areas:**
1. **Neurofinance**: Brain imaging of financial decisions
2. **Genetic studies**: Heritability of financial risk-taking
3. **Machine learning**: Text analysis for behavioral measures
4. **International evidence**: Cross-cultural variation in biases

**Methodological Advances:**
1. Improved identification strategies
2. Administrative data access
3. Field experiments in corporate settings

---

## 8. Key Findings Summary

### 8.1 Investor Biases

| Phenomenon | Key Paper | Main Finding |
|------------|-----------|--------------|
| Market timing | Baker & Wurgler (2002) | Persistent leverage effects from equity market conditions |
| Dividend catering | Baker & Wurgler (2004) | Dividend initiation responds to investor preferences |
| Sentiment effects | Polk & Sapienza (2009) | Investment responds to mispricing proxies |

### 8.2 Manager Biases

| Phenomenon | Key Paper | Main Finding |
|------------|-----------|--------------|
| Investment distortion | Malmendier & Tate (2005) | Overconfident CEOs show 3-5pp higher cash flow sensitivity |
| Acquisition excess | Malmendier & Tate (2008) | Longholder CEOs 65% more likely to acquire |
| Financing choices | Various | Overconfidence → higher leverage, less equity |

### 8.3 Third Party Effects

| Phenomenon | Key Paper | Main Finding |
|------------|-----------|--------------|
| Board composition | Various | CEO biases propagate to board selection |
| Analyst bias | Various | Career concerns interact with overconfidence |
| Network effects | Various | Behaviors spread through professional networks |

---

## 9. Methodological Contributions

### 9.1 The Longholder Measure

**Construction:**
1. Identify CEO option holdings from SEC filings
2. Track option exercise behavior over time
3. Code Longholder = 1 if CEO holds options to expiration
4. Code Holder 67 = 1 if CEO fails to exercise at 67% moneyness

**Validation:**
- Predicts out-of-sample option exercise
- Stable within-CEO over time
- Correlates with media-based measures
- Not explained by inside information

### 9.2 Identification Strategies

**Addressing Endogeneity:**
1. Within-firm variation in CEO
2. CEO fixed effects
3. Instrumental variables (e.g., inheritance shocks)
4. Natural experiments (e.g., regulatory changes)

**Distinguishing Overconfidence from:**
- Inside information
- Risk tolerance
- Career concerns
- Agency problems

---

## 10. Theoretical Frameworks

### 10.1 Value Destruction vs. Value Creation

**Value-Destroying Overconfidence:**
- Overinvestment in negative NPV projects
- Value-destroying acquisitions
- Excessive risk-taking

**Value-Enhancing Overconfidence:**
- Gervais, Heaton, and Odean (2011): Optimal contract with overconfident manager
- Overconfidence can substitute for costly incentives
- Innovation may require excessive optimism

### 10.2 Equilibrium Effects

**Market Response:**
- Rational investors price overconfidence
- Discount reflects expected value destruction
- Career market filters overconfident managers (imperfectly)

**Corporate Governance:**
- Boards may tolerate or even select for overconfidence
- Trade-off: initiative vs. excessive risk

---

## 11. Critical Assessment

### 11.1 Measurement Challenges

**Longholder Measure Limitations:**
- Requires option data (larger firms)
- Binary classification
- May capture risk tolerance or information

**Alternative Interpretations:**
- Tax timing optimization
- Signaling to employees
- Liquidity constraints

### 11.2 External Validity

**Sample Considerations:**
- Primarily U.S. large-cap firms
- Data availability constraints
- Survivorship bias

**Generalizability:**
- Private firms
- International settings
- Smaller companies

### 11.3 Welfare Implications

**Policy Relevance:**
- Should boards screen for overconfidence?
- Debiasing interventions
- Regulatory implications

---

## 12. Conclusion

Behavioral corporate finance has established that psychological biases systematically affect corporate decisions. The three-perspective framework—biased investors, biased managers, and biased third parties—provides an organizing structure for understanding these effects.

Key achievements include:
1. Development of validated measures of CEO overconfidence
2. Documentation of investment and acquisition distortions
3. Understanding of market timing and catering behaviors
4. Recognition of network and social effects

Future research directions include:
1. Improved measurement of biases
2. International and cross-cultural evidence
3. Welfare analysis and policy implications
4. Integration with machine learning methods

The field continues to grow, with behavioral considerations increasingly integrated into mainstream corporate finance research.

---

## Key Parameters and Quantifications

| Parameter | Value | Source |
|-----------|-------|--------|
| Longholder investment sensitivity premium | 3-5 percentage points | Malmendier & Tate (2005) |
| Acquisition propensity increase | 65% | Malmendier & Tate (2008) |
| Announcement return discount | -90 basis points | Malmendier & Tate (2008) |
| Papers on biased investors | ~45% | Literature review |
| Papers on biased managers | ~45% | Literature review |
| Papers on biased third parties | ~10% | Literature review |
| Dividend premium effect | Significant | Baker & Wurgler (2004) |
| Dot-com name change returns | +74% | Cooper et al. (2001) |

---

## References (Selected)

- Baker, M., & Wurgler, J. (2002). Market timing and capital structure. Journal of Finance, 57(1), 1-32.
- Baker, M., & Wurgler, J. (2004). A catering theory of dividends. Journal of Finance, 59(3), 1125-1165.
- Baker, M., Pan, X., & Wurgler, J. (2012). The effect of reference point prices on mergers and acquisitions. Journal of Financial Economics, 106(1), 49-71.
- Ben-David, I., Graham, J. R., & Harvey, C. R. (2013). Managerial miscalibration. Quarterly Journal of Economics, 128(4), 1547-1584.
- Gervais, S., Heaton, J. B., & Odean, T. (2011). Overconfidence, compensation contracts, and capital budgeting. Journal of Finance, 66(5), 1735-1777.
- Malmendier, U., & Nagel, S. (2011). Depression babies: Do macroeconomic experiences affect risk taking? Quarterly Journal of Economics, 126(1), 373-416.
- Malmendier, U., & Tate, G. (2005). CEO overconfidence and corporate investment. Journal of Finance, 60(6), 2661-2700.
- Malmendier, U., & Tate, G. (2008). Who makes acquisitions? CEO overconfidence and the market's reaction. Journal of Financial Economics, 89(1), 20-43.
- Myers, S. C., & Majluf, N. S. (1984). Corporate financing and investment decisions when firms have information that investors do not have. Journal of Financial Economics, 13(2), 187-221.
- Polk, C., & Sapienza, P. (2009). The stock market and corporate investment: A test of catering theory. Review of Financial Studies, 22(1), 187-217.

---

*Full text archived for EBF integration. Content level: L3 (complete structural characteristics S1-S6).*
