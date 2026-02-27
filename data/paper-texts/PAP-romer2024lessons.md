# Lessons from history for successful disinflation

**Authors:** Christina D. Romer & David H. Romer (University of California, Berkeley)
**Journal:** Journal of Monetary Economics 148 (2024) 103654
**DOI:** 10.1016/j.jmoneco.2024.103654
**Conference:** Spring 2024 NBER conference on "Inflation in the Covid era and beyond"
**Archived:** 2026-02-05

## Abstract

One factor that could affect whether monetary policymakers succeed in reducing inflation is the
degree to which they are committed to reducing it. We use the narrative record — particularly the
detailed minutes and transcripts of Federal Reserve policymaking meetings — to identify nine
episodes where policymakers made a deliberate decision to try to reduce inflation. We find
substantial variation in the strength of their commitment, and that stronger commitment was
associated with better disinflation outcomes. We find that the mechanism through which
commitment mattered was not mainly an expectations channel, but rather that less committed
policymakers were more likely to abandon their efforts to reduce inflation. The analysis carries a
cautionary note for the current episode: the Federal Reserve's commitment to reducing inflation
appears moderate, suggesting the possibility of premature easing.

## Methodology

### Narrative Identification
- Read all FOMC transcripts and Minutes from 1946-present
- Identified 9 deliberate disinflation attempts (not all tightening episodes — only those with stated intention to reduce inflation)
- Distinguished from routine policy adjustments or responses to financial crises

### Commitment Scaling (1-5)
- 1 = "very weak" — just a desire with little sense of determination
- 2 = "weak"
- 3 = "moderate" — determined but with caveats
- 4 = "strong"
- 5 = "very strong" — willing to accept substantial costs

### Regression Framework
- Local projection regressions: Δπ(t+h) = α + β·D(t) + controls
- Scaled dummy variables: D(t) × commitment_level
- Controls: lagged inflation, lagged unemployment rate

## The Nine Episodes

### Table 1: Deliberate Disinflation Attempts

| # | Start | Chair | Commitment | Inflation at Start |
|---|-------|-------|------------|-------------------|
| 1 | 1947:5 | Eccles | 3 (moderate) | ~20% |
| 2 | 1955:12 | Martin | 4 (strong) | ~3% |
| 3 | 1958:9 | Martin | 2 (weak) | ~3% |
| 4 | 1966:10 | Martin | 3 (moderate) | ~4% |
| 5 | 1969:1 | Martin/Burns | 3 (moderate) | ~5% |
| 6 | 1974:6 | Burns | 1 (very weak) | ~12% |
| 7 | 1978:8 | Miller | 2 (weak) | ~9% |
| 8 | 1979:10 | Volcker | 5 (very strong) | ~12% |
| 9 | 1988:3 | Greenspan | 4 (strong) | ~4% |

### Current Episode (2022)
- Start: March 2022
- Chair: Powell
- Commitment: 3 (moderate) — "determined but with significant caveats"
- Inflation at start: ~6% (core PCE)

## Key Findings

### Finding 1: Commitment Predicts Disinflation Success
- Higher commitment → larger, more sustained inflation reduction
- Regression coefficient: each 1-unit increase in commitment associated with ~1pp more disinflation after 2 years
- Relationship is roughly linear

### Finding 2: Expectations Channel Does NOT Explain the Mechanism
- Expected inflation (from Livingston Survey, SPF) does NOT respond differently to high vs. low commitment
- Table 2: No significant difference in expected inflation responses by commitment level
- "The mechanism through which commitment matters is not mainly through expectations"

### Finding 3: Premature Easing IS the Mechanism
- Less committed policymakers more likely to abandon disinflation before completion
- Table 3: Low commitment episodes end earlier (premature reversal)
- High commitment episodes (Volcker, Martin 1955, Greenspan 1988) maintained tight policy until inflation fell substantially
- Low commitment episodes (Burns 1974, Miller 1978, Martin 1958) reversed course

### Finding 4: Cautionary Note for Current Episode
- Powell Fed's commitment rated as "moderate" (3)
- Historical pattern: moderate commitment → risk of premature easing
- Key risk: if economic weakness emerges, Fed may ease before inflation is fully tamed
- "Our findings suggest that the most important thing the Federal Reserve can do is to persevere"

## Mechanisms: Expectations vs. Perseverance

### Expectations Channel (tested and REJECTED)
- Rational expectations view: credible commitment → lower inflation expectations → painless disinflation
- Evidence: expected inflation responds similarly regardless of commitment level
- "The expectations channel is not the primary mechanism"

### Perseverance Channel (tested and CONFIRMED)
- Commitment → willingness to maintain tight policy despite economic costs
- Less committed policymakers reverse course when unemployment rises
- More committed policymakers "stay the course" through economic weakness
- This is the channel through which commitment reduces inflation

## Data Sources
- FOMC Transcripts (1946-present, released with 5-year lag)
- FOMC Minutes (full historical record)
- Livingston Survey of Professional Forecasters (expected inflation)
- Survey of Professional Forecasters (SPF)
- New York Times coverage (for narrative context)
- Bureau of Labor Statistics (CPI, unemployment rate)

## References (selected)
- Ball (1994): Credible disinflation with staggered price-setting
- Clarida, Galí & Gertler (2000): Monetary policy rules and macroeconomic stability
- DeLong (1997): America's peacetime inflation — Fed narrative history
- Erceg & Levin (2003): Imperfect credibility and inflation persistence
- Friedman (1968): Role of monetary policy — AER presidential address
- Romer & Romer (1989): Does monetary policy matter? — Narrative approach
- Romer & Romer (2004): New measure of monetary shocks — AER
- Sargent (1982): Ends of four big inflations
- Sargent (1999): Conquest of American Inflation
- Volcker (1979): New operating procedures — FOMC announcement

## Note
This is a full research paper (21 pages, 3 tables, 5 figures) with formal methodology.
Narrative approach is systematic and reproducible (FOMC records are public).
Key contribution: separating expectations channel from perseverance channel.
Direct policy relevance for current Fed disinflation effort.
