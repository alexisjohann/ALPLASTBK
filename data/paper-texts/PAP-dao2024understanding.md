# Understanding the international rise and fall of inflation since 2020

**Authors:** Mai Chi Dao (IMF), Pierre-Olivier Gourinchas (IMF), Daniel Leigh (IMF), Prachi Mishra (Ashoka University)
**Journal:** Journal of Monetary Economics 148 (2024) 103658
**DOI:** 10.1016/j.jmoneco.2024.103658
**Conference:** Spring 2024 NBER conference on "Inflation in the Covid era and beyond"
**Archived:** 2026-02-05

## Abstract

This paper analyzes inflation dynamics in 21 advanced and emerging market economies since
2020. We decompose inflation into core inflation as measured by the weighted median inflation
rate, and headline shocks—deviations of headline inflation from core. Headline shocks occurred
largely on account of energy price changes, although food price changes and indicators of supply
chain problems also played a role. We explain the evolution of core inflation with two factors: the
strength of macroeconomic conditions—measured by the unemployment gap, the output gap, and
the ratio of job vacancies to unemployment—and the pass-through into core inflation from past
headline shocks. We conclude that the international rise and fall of inflation since 2020 largely
reflected the direct and pass-through effects of headline shocks. Macroeconomic conditions
generally played a secondary role. In the United States, estimated price pressures from strong
macroeconomic conditions had been greater than in other economies but have eased.

## Methodology

### Inflation Decomposition
- headline inflation = core inflation + headline shocks (Eq. 1)
- Core inflation measured by WEIGHTED MEDIAN inflation rate (not traditional XFE)
- Weighted median strips out unusually large price changes in time-varying industries
- Superior to XFE during Covid era (adjusted R-squared drops from 45% to 18% with XFE)

### Headline Shock Drivers (10 candidate variables tested)
- Top 3 drivers (by R-squared):
  1. Relative energy-price inflation (dominant for 17/21 countries)
  2. Relative food-price inflation (significant in 11/21 cases)
  3. Global shipping costs (Harper charter rate, significant in 7/21 cases)
- Together explain 21%-94% of headline shock variation by country

### Phillips Curve for Core Inflation (Eq. 2)
- π = πᵉ + f(Y) + g(H) + ε
- πᵉ: longer-term survey expectations (one-for-one pass-through assumed)
- Y: macroeconomic conditions (unemployment gap, output gap, or V/U)
  - V/U used for US and Canada (Beveridge curve shift during pandemic)
  - Unemployment gap for most other economies
  - Output gap for emerging markets
- H: headline inflation shocks (12-month average, captures pass-through)
- f(.) and g(.): allow nonlinearities (quadratic/cubic functions)
- Linear specification for UK and Italy (no evidence of nonlinearities)

### Sample
- 21 economies (10 advanced + 4 emerging with full estimation, 7 additional for cross-section)
- Advanced: Canada, Euro Area, France, Germany, Italy, Japan, Spain, Sweden, UK, US
- Emerging: Brazil, Chile, India, Poland
- Period: 2020-March 2024
- Data: Haver Analytics, Fed Cleveland, Statistics Canada, IMF WEO, Consensus Economics

## Key Findings

### Finding 1: Energy Prices Dominated the Rise AND Fall
- Energy price inflation: primary driver of headline shocks in 17/21 countries
- Median headline inflation: 0.7% (Dec 2020) → 8.6% peak (Aug 2022) → 3.1% (Mar 2024)
- Energy prices rose ~44pp to peak, then largely dissipated by late 2023
- Energy + passthrough account for ~49% of inflation rise and ~62% of fall (average across 14 countries)

### Finding 2: Macroeconomic Conditions Played Secondary Role (Except US)
- Share of macro conditions in inflation rise: below 9% on average
- Long-term inflation expectations remained well anchored (median stable at 2.1%)
- Key exception: United States
  - V/U contribution to US inflation significantly larger than other economies
  - V/U captures broader price pressures beyond wage channel
  - Even controlling for wage growth, V/U remains significant
  - US contribution of V/U: 2.3pp (Mar 2024) vs. 0.9pp (Euro Area) vs. 0.5pp (UK)

### Finding 3: Cross-Country Passthrough Puzzle Resolved
- Puzzle: no cross-country correlation between energy price inflation and core inflation
- Resolution: country-specific passthrough coefficients vary enormously
- After adjusting for country-specific coefficients: R-squared jumps from ~0% to 76-79%
- Poland example: large core inflation rise fully explained by strong country-specific passthrough

### Finding 4: Energy Price Policies Mattered
- Countries with larger price-suppressing fiscal measures had smaller headline shocks
- France: 3% GDP in price-suppressing measures → relatively low energy-price contribution
- Germany: smaller measures → energy contribution nearly 3x larger than France
- Negative correlation between fiscal energy measures and energy contribution to headline shocks

### Finding 5: Nonlinearities Are Important
- Steeper Phillips curve slope when output above potential / labor markets tight
- Asymmetry: positive headline shocks → stronger core inflation impact than negative shocks
- Consistent with Ball & Mankiw (1994) menu cost theory and Benigno & Eggertsson (2023)
- Weighted median inflation critical: traditional XFE halves explanatory power

### Finding 6: US Is the Exception
- Stronger macroeconomic conditions contributed more to inflation than in other countries
- V/U contribution to 12-month US inflation in Mar 2024: still substantial (2.3pp)
- But declining: V/U contribution in Mar 2024 only 1/3 of Feb 2023 level
- Factors: expansionary fiscal stance, pandemic savings, fixed-rate mortgages buffering households

## Complementary Findings (vs. Bernanke & Blanchard 2024a)
- Both studies reach same broad conclusion: price shocks dominant, not labor market pressure
- This paper finds LARGER role for V/U in US (V/U in overall core equation, not just wages)
- This paper documents nonlinearity in V/U-inflation relationship
- Bernanke & Blanchard use linear specification

## References (selected)
- Ball, Leigh & Mishra (2022): Understanding US inflation during Covid — Brookings
- Ball & Mankiw (1994): Asymmetric price adjustment
- Benigno & Eggertsson (2023): Non-linear Phillips curve
- Bernanke & Blanchard (2024a): Post-pandemic inflation in 11 economies
- Blanchard & Wolfers (2000): Shocks and institutions in European unemployment
- Dao et al. (2023): Unconventional fiscal policy — IMF WP
- Hazell et al. (2022): Slope of Phillips curve from US states — QJE

## Note
This is a full research paper (19 pages text + extensive annexes with 8 tables, 7+ figures).
IMF Research Department paper with rigorous cross-country empirical methodology.
Data available on request. Weighted median inflation computation by IMF staff.
Key contribution: resolving cross-country passthrough puzzle via country-specific coefficients.
