# PAP-becker1990empirical - Full Text Archive

**Paper:** An Empirical Analysis of Cigarette Addiction
**Authors:** Gary S. Becker, Michael Grossman, Kevin M. Murphy
**Institution:** NBER Working Paper No. 3322
**Year:** 1990
**Archived Date:** 2026-02-04
**Content Level:** L3 (Full structural characteristics S1-S6 available)

---

## Abstract

We use a framework suggested by a model of rational addiction to analyze empirically the demand for cigarettes. The data consist of per capita cigarettes sales (in packs) annually by state for the period 1955 through 1985. The empirical results provide support for the implications of a rational addiction model that cross price effects are negative (consumption in different periods are complements), that long-run price responses exceed short-run responses, and that permanent price effects exceed temporary price effects. A 10 percent permanent increase in the price of cigarettes reduces current consumption by 4 percent in the short run and by 7.5 percent in the long run. In contrast, a 10 percent increase in the price for only one period decreases consumption by only 3 percent. In addition, a one period price increase of 10 percent reduces consumption in the previous period by approximately .7 percent and consumption in the subsequent period by 1.5 percent. These estimates illustrate the importance of the intertemporal linkages in cigarette demand implied by rational addictive behavior.

---

## I. Introduction and Summary

Becker and Murphy (1988) develop a theoretical model of rational addiction and outline its key empirical predictions. This paper uses that framework to analyze empirically the demand for cigarettes. The data consist of per capita cigarette sales (in packs) annually by state for the period 1955 through 1985. The empirical results indicate that smoking is addictive.

The Becker-Murphy model follows Stigler and Becker (1977), Iannaccone (1986), Ryder and Heal (1973), Boyer (1978, 1983), and Spinnewyn (1981) by considering the interaction of past and current consumption in a rational model. The main feature of these models is that past consumption of some goods influences their current consumption by affecting the marginal utility of current and future consumption.

**Key Properties of Addictive Goods:**
- Greater past consumption of harmfully addictive goods such as cigarettes stimulates current consumption
- Past consumption increases the marginal utility of current consumption more than the present value of the marginal harm from future consumption
- Past consumption is reinforcing for addictive goods

**Key Empirical Implications:**
1. Bimodal distribution of consumption
2. Quitting by cold turkey
3. Negative cross effect (complementarity) between price at one time and consumption at another
4. Larger long-run than short-run elasticities of demand
5. Larger responses to anticipated than unanticipated price changes
6. Larger responses to permanent than temporary price changes

### Main Findings

- A 10 percent permanent increase in cigarette price reduces current consumption by **4 percent in the short run** and by **7.5 percent in the long run**
- A 10 percent increase in price for only one period decreases consumption by **only 3 percent**
- A one period price increase of 10 percent:
  - Decreases consumption in the previous period by approximately **0.7 percent**
  - Decreases consumption in the subsequent period by **1.5 percent**

**Critical Result:** The results strongly reject myopic behavior and generally support the model of rational addiction.

---

## II. The Basic Model

### Utility Function

Following Boyer (1978, 1983), current period utility in period t is given by a concave utility function:

$$U(Y_t, C_t, C_{t-1}, e_t)$$

where:
- $C_t$ = quantity of cigarettes consumed in period t
- $C_{t-1}$ = quantity of cigarettes consumed in period t-1
- $Y_t$ = consumption of a composite commodity in period t
- $e_t$ = impact of unmeasured life cycle variables on utility

### Consumer's Problem

Individuals maximize the sum of lifetime utility discounted at the rate r:

$$\max \sum_{t=1}^{\infty} \beta^{t-1} U(C_t, C_{t-1}, Y_t, e_t)$$

subject to $C_0 = C^0$ (initial condition) and budget constraint:

$$\sum_{t=1}^{\infty} \beta^{t-1}(Y_t + P_t C_t) = A^0$$

where $\beta = 1/(1+r)$ and $P_t$ is the price of cigarettes in period t.

### First-Order Conditions

$$(3a) \quad U_Y(C_t, C_{t-1}, Y_t, e_t) = \lambda$$

$$(3b) \quad U_1(C_t, C_{t-1}, e_t) + \beta U_2(C_{t+1}, C_t, e_{t+1}) = \lambda P_t$$

**Key Insight:** For harmfully addictive goods like cigarettes, $U_2 < 0$, meaning current consumption reduces future utility.

### The Estimating Equation (Quadratic Utility)

With quadratic utility, the first-order conditions yield a linear difference equation:

$$(6) \quad C_t = \theta C_{t-1} + \beta\theta C_{t+1} + \theta_0 + \theta_1 P_t + \theta_2 e_t + \theta_3 e_{t+1}$$

where:

$$\theta = \frac{-(U_{12}U_{yy} - U_{1y}U_{2y})}{(U_{11}U_{yy} - U_{1y}^2) + \beta(U_{22}U_{yy} - U_{2y}^2)}$$

**Definition of Addiction:** A good is addictive if and only if $\theta > 0$ (increase in past consumption leads to increase in current consumption).

### Dynamic Properties

The dynamics are determined by the roots of:

$$\mu^2 - \frac{\mu}{\beta\theta} + \frac{1}{\beta} = 0$$

The two roots are:

$$\mu_1 = \frac{1 - (1 - 4\beta^2\theta^2)^{1/2}}{2\beta\theta}, \quad \mu_2 = \frac{1 + (1 - 4\beta^2\theta^2)^{1/2}}{2\beta\theta}$$

Both roots are positive if and only if cigarettes are addictive ($\theta > 0$).

### Price Effects

**Temporary own price effect (unanticipated):**
$$\frac{dC_t}{dP_t} = \frac{\theta_1}{\theta(\mu_2 - \mu_1)} < 0$$

**Long-run effect of permanent price change:**
$$\frac{dC_t}{dP^*} = \frac{\theta_1}{1 - \theta - \beta\theta}$$

**Key Result:** Long-run response exceeds short-run response by factor $(\mu_2 - 1)$. This exceeds one if and only if $\mu_2 > 1$, which is equivalent to $\theta > 0$ (addiction).

---

## III. A Myopic Model of Addiction

### Key Distinction from Rational Addiction

Myopic individuals fail to consider the impact of current consumption on future utility and future consumption. The first-order condition for myopic behavior:

$$(16b) \quad U_1 + U_{1y}Y_t + U_{11}C_t + U_{12}C_{t-1} + U_{1e}e_t = \lambda P_t$$

**Critical Difference:** The myopic equation is entirely backward looking. Current consumption depends only on:
- Current price
- Lagged consumption
- Marginal utility of wealth
- Current events

Current consumption is independent of both future consumption $C_{t+1}$ and future events $e_{t+1}$.

### Empirical Test

**Myopic behavior implies:** Coefficient on instrumented future consumption should be **zero**

**Rational behavior implies:** Coefficient on future consumption should have the **same sign** as coefficient on lagged consumption (sizes differ only by discount factor)

---

## IV. Data and Empirical Implementation

### Dataset

- **Coverage:** Time series of state cross sections, 1955-1985
- **Observations:** 1,516 (50 states + DC × 31 years, minus missing data)
- **Source:** Tobacco Tax Council (1986)
- **Measure:** Per capita tax-paid cigarette sales (in packs)

### Key Variables

| Variable | Mean | Std. Dev. | Description |
|----------|------|-----------|-------------|
| C | 124.8 | 31.96 | Per capita cigarette consumption (packs) |
| P | 29.6 | 3.30 | Retail price per pack (1967 cents) |
| Income | 29.30 | 8.54 | Per capita income (hundreds of 1967 dollars) |
| Tax | 6.4 | 2.90 | Excise tax (1967 cents per pack) |
| hs | 52.88 | 14.85 | % with high school education |
| divorce | 4.96 | 14.85 | % divorced women aged 25-34 |
| unemp | 5.41 | 2.30 | Unemployment rate |
| mormon | 2.70 | 10.01 | % Mormon |
| catholic | 18.94 | 13.41 | % Catholic |

### Identification Strategy

State excise taxes on cigarettes provide empirical leverage:
- Tax rates vary greatly across states at a point in time
- Tax rates vary within a given state over time
- Average tax: 6.4 cents per pack (21% of average retail price of 30 cents)
- One standard deviation difference: 6 cents (20% of average price)

### Instrumental Variables Strategy

Past and future prices are instruments for $C_{t-1}$ and $C_{t+1}$:
- Past prices directly affect past consumption
- Future prices directly affect future consumption
- Prices assumed uncorrelated with unobservables

---

## V. Empirical Results

### Table 2: OLS Results

| Variable | Model 1 | Model 2 | Model 3 | Model 4 |
|----------|---------|---------|---------|---------|
| $P_{t-1}$ | - | - | -2.073 | -1.949 |
| $P_t$ | -3.018 | -3.216 | -0.626 | -0.685 |
| $P_{t+1}$ | - | - | -0.834 | -0.809 |
| $Y_t$ | 1.530 | 1.610 | 1.620 | 1.660 |

**Implied price elasticity:** -0.71 (at mean)

**F-test that past and future prices have no effect:** F = 10.7 and 34.8 → **strongly reject non-addiction**

### Table 3: Two-Stage Least Squares Results

Testing equation: $C_t = \theta C_{t-1} + \beta\theta C_{t+1} + \theta_0 + \theta_1 P_t$

| Parameter | Model 1 | Model 2 | Model 3 | Model 4 | Model 5 |
|-----------|---------|---------|---------|---------|---------|
| $\hat{C}_{t-1}$ | 0.424 | 0.375 | 0.443 | 0.480 | - |
| $\hat{C}_{t+1}$ | 0.133 | 0.239 | 0.172 | 0.229 | 0.205 |
| $P_t$ | -1.392 | -1.229 | -1.230 | -0.981 | -1.141 |
| $Y_t$ | 0.831 | 0.753 | 0.741 | 0.607 | 0.595 |

**Key Results:**
- Past consumption positively affects current consumption ✓
- Future consumption positively affects current consumption ✓ (rejects myopia)
- Current price negatively affects current consumption ✓

### Table 4: Roots of Difference Equation

| Model | $\mu_1$ | $\mu_2$ |
|-------|---------|---------|
| 1 | 0.141 | 2.218 |
| 2 | 0.265 | 2.405 |
| 3 | 0.188 | 2.069 |
| 4 | 0.263 | 1.822 |
| 5 | 0.229 | 1.976 |

**Interpretation:** A 10% increase in current consumption increases next period's consumption by 4.2-5.5%, and a 10% increase in future consumption increases current consumption by 1.4-2.6%.

### Table 5: Price Elasticities (2SLS)

| Elasticity Type | Model 1 | Model 2 | Model 3 | Model 4 | Model 5 |
|-----------------|---------|---------|---------|---------|---------|
| Long-run (permanent) | -0.743 | -0.773 | -0.757 | -0.799 | -0.791 |
| Own price (anticipated) | -0.374 | -0.363 | -0.350 | -0.310 | -0.341 |
| Own price (unanticipated) | -0.351 | -0.323 | -0.318 | -0.266 | -0.301 |
| Future price (unantic.) | -0.050 | -0.086 | -0.060 | -0.070 | -0.069 |
| Past price (unantic.) | -0.158 | -0.134 | -0.154 | -0.146 | -0.153 |
| Short-run | -0.408 | -0.440 | -0.391 | -0.360 | -0.391 |

**KEY FINDING:**
- **Short-run elasticity: -0.4** (4% reduction from 10% price increase)
- **Long-run elasticity: -0.75** (7.5% reduction from 10% price increase)
- **Ratio: ~1.9** (long-run nearly twice short-run)

---

## VI. General Model

### Stock-Based Formulation

Utility depends on consumption $C_t$ and a "stock" of past consumption $S_t$:

$$S_{t+1} = (1 - \delta)S_t + C_t$$

where $\delta$ is the depreciation rate on the stock.

$$U_t = U(C_t, S_t)$$

### First-Order Condition

$$U_c(C_t, S_t) + \sum_{\tau=1}^{\infty} \beta^\tau (1-\delta)^\tau U_S(C_{t+\tau}, S_{t+\tau}) = \lambda P_t$$

### Estimating Equation

With quadratic utility:

$$(22) \quad C_t = \theta C_{t-1} + \beta\theta C_{t+1} + \theta_0 + \theta_1 P_{t-1} + \theta_2 P_t + \theta_3 P_{t+1}$$

**Key Difference:** Past and future prices enter in addition to current price and past/future consumption.

---

## VII. Empirical Results for General Model

### Table 6: General 2SLS Results

| Variable | Model 6 | Model 7 | Model 8 | Model 9 | Model 10 |
|----------|---------|---------|---------|---------|----------|
| $\hat{C}_{t-1}$ | 0.495 | 0.505 | 0.417 | 0.470 | 0.441 |
| $\hat{C}_{t+1}$ | 0.294 | 0.350 | 0.396 | 0.423 | 0.375 |
| $P_{t-1}$ | 0.613 | 0.758 | 0.662 | 0.890 | 0.694 |
| $P_t$ | -1.685 | -1.906 | -1.697 | -1.931 | -1.687 |
| $P_{t+1}$ | 0.569 | 0.772 | 0.628 | 0.801 | 0.590 |

**All signs conform with theoretical predictions:**
- Past and future consumption: positive ✓
- Past and future prices (controlling for C): positive ✓
- Current price: negative ✓

### Tests of Myopic vs Rational Addiction

**Myopia implies:** Zero coefficients on future consumption and future price

**F-test for both future effects = 0:**
- Model 1: F = 18.6 → **reject myopia**
- Model 2: F = 21.3 → **reject myopia**

**F-test for time-separability (all past/future effects = 0):**
- Model 1: F = 615.7 → **reject time-separability**
- Model 2: F = 799.2 → **reject time-separability**

### Table 7: Price Elasticities (General Model)

| Elasticity Type | Model 6 | Model 7 | Model 8 | Model 9 | Model 10 |
|-----------------|---------|---------|---------|---------|----------|
| Long-run | -0.565 | -0.612 | -0.515 | -0.533 | -0.517 |
| Own price (anticipated) | -0.412 | -0.462 | -0.420 | -0.468 | -0.419 |
| Own price (unanticipated) | -0.422 | -0.480 | -0.409 | -0.461 | -0.406 |
| Short-run | -0.402 | -0.444 | -0.442 | -0.478 | -0.437 |

---

## VIII. Monopoly and Addiction

### Pricing Implications

Two-period Cobb-Douglas demand:

$$q_1 = a_1 p_1^{-\varepsilon_1} p_2^{*\gamma}$$
$$q_2 = a_2 p_2^{-\varepsilon_2} q_1^\gamma$$

where $0 < \gamma < 1$ represents the addiction effect.

### Key Results

1. **Marginal revenue < Marginal cost in period 1** when $p_2 > c_2$ and consumption is addictive
   - Monopolist may lower price to get consumers "hooked"
   - Explains free cigarette distribution to college students

2. **Price rises when demand falls** if cigarette companies have monopoly power
   - 1982-1983 price increases preceded and followed federal tax increase
   - "Apparent paradox" that profits rise while smoking declines is resolved

3. **Anticipated future taxes raise current prices** under oligopoly with addiction

---

## Key Equations Summary

**Utility Function:**
$$U = U(Y_t, C_t, C_{t-1}, e_t)$$

**Estimating Equation (Simple):**
$$C_t = \theta C_{t-1} + \beta\theta C_{t+1} + \theta_0 + \theta_1 P_t$$

**Estimating Equation (General):**
$$C_t = \theta C_{t-1} + \beta\theta C_{t+1} + \theta_0 + \theta_1 P_{t-1} + \theta_2 P_t + \theta_3 P_{t+1}$$

**Long-Run Elasticity:**
$$\eta_{LR} = \frac{\theta_1}{1 - \theta - \beta\theta}$$

**Short-Run Elasticity:**
$$\eta_{SR} = \frac{\theta_1}{\theta(1 - \mu_1)}$$

---

## EBF Integration Notes

### Foundational Relevance for EBF Framework

This paper is **FOUNDATIONAL** for the EBF Framework. It provides the first major empirical validation of rational addiction theory and establishes key parameters for addiction modeling.

### 10C Connection

| 10C | Relevance | Connection |
|-----|-----------|------------|
| **WHAT (C)** | Primary | Addiction affects commodity production efficiency |
| **HOW (B)** | Strong | Intertemporal complementarity in consumption |
| **WHEN (V)** | Strong | Time preferences, discounting behavior |
| **WHERE (BBB)** | Primary | Empirical parameter estimates |
| **AWARE (AU)** | Moderate | Information about health hazards |

### Key Parameters for EBF

| Parameter | Value | Description |
|-----------|-------|-------------|
| $\theta$ | 0.4-0.5 | Addiction reinforcement parameter |
| $\eta_{SR}$ | -0.40 | Short-run price elasticity |
| $\eta_{LR}$ | -0.75 | Long-run price elasticity |
| $\eta_{LR}/\eta_{SR}$ | ~1.9 | Addiction amplification ratio |
| Cross-price (future) | -0.06 to -0.09 | Future price effect on current consumption |
| Cross-price (past) | -0.13 to -0.16 | Past price effect on current consumption |

### Theory Catalog Mapping

This paper provides **empirical validation** for:
- MS-RA-001: Rational Addiction Theory (Becker & Murphy)
- MS-CC-001: Consumption Capital Theory
- MS-HP-001: Household Production Theory (Stigler & Becker)

### Methodological Contribution

1. **Instrumental Variables for Addiction:** Using past/future prices as instruments for past/future consumption
2. **Testing Myopic vs Rational:** Future consumption coefficient distinguishes models
3. **State-level Panel Data:** 50 states × 31 years provides identification

### Citation

This paper should be cited whenever the EBF Framework uses:
- Rational addiction parameter estimates
- Short-run vs long-run elasticity comparisons
- Intertemporal complementarity in consumption
- Tests of myopic vs forward-looking behavior
- Addiction reinforcement coefficients
