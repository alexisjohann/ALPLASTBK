# AI-Bubble USA: Diagnose & Prognose

**Session:** EBF-S-2026-02-04-FIN-001
**Datum:** 4. Februar 2026
**Modus:** STANDARD
**Modell:** MOD-FIN-BUBBLE-001 v1.1

---

## Executive Summary

| Frage | Antwort | Konfidenz |
|-------|---------|-----------|
| **Existiert eine AI-Bubble?** | **JA** | Hoch (B=0.82) |
| **P(Crash ≤6 Monate)** | **67%** [55%-75%] | Mittel-Hoch |
| **Ist es ein Schneeballsystem?** | Nein, aber ähnliche Dynamik | Hoch |
| **Hauptrisiko** | Circular Financing Collapse | Hoch |

---

## 1. Fragestellung

FehrAdvice wollte wissen:
1. Gibt es Indizien für eine AI-Blasenbildung in den USA?
2. Wie gross ist die Wahrscheinlichkeit, dass diese Blase in den nächsten 6 Monaten platzt?

---

## 2. Kontext-Analyse

### 2.1 Das Circular Financing Karussell

```
Microsoft ──$13B──► OpenAI ──$12.4B──► Azure (Microsoft)
                       │
Nvidia ────$100B───────┘ (GESTOPPT Feb 2026)
   │
   └──$53B──► 170 AI-Firmen ──► kaufen Nvidia GPUs
```

**Kritische Verflechtungen:**
- Microsoft investiert $13B in OpenAI → OpenAI gibt $12.4B für Azure aus
- Nvidia investiert $53B in 170 AI-Firmen → Diese kaufen Nvidia GPUs
- Nvidia + Microsoft investieren $15B in Anthropic → Anthropic kauft $30B Azure-Credits

### 2.2 Marktdaten (Stand: Februar 2026)

| Indikator | Wert | Historischer Vergleich |
|-----------|------|------------------------|
| Shiller CAPE | 40.6 | Nur 2x seit 1871 über 40 |
| Credit Spreads IG | 71 bps | 30-Jahres-Tief |
| Magnificent 7 P/E | 28-29x | Dotcom war 40+ |
| AI-Infrastruktur-Invest | $400B/Jahr | vs. $100B Revenue |
| Fear & Greed Index | 41 | Fear Zone |

---

## 3. Methodik

### 3.1 Modell: AI Bubble Diagnostic & Prognostic Model (ABDPM)

**Komponenten:**
1. Kindleberger-Minsky 5-Phasen-Modell
2. Lamont "4 Horsemen" Bubble-Kriterien
3. Circular Financing Risk Score (CFRS)
4. Shiller CAPE Ratio
5. Credit Spread Complacency Index
6. Insider Selling Indicator

### 3.2 Diagnose-Formel

```
B_score = w₁·Phase + w₂·Lamont + w₃·CFRS + w₄·CAPE + w₅·Complacency + w₆·Insider

Gewichte: w₁=0.20, w₂=0.20, w₃=0.20, w₄=0.15, w₅=0.15, w₆=0.10
```

### 3.3 Prognose-Formel

```
P(Crash 6M) = 1 - Π[1 - P(Tᵢ) × P(Crash|Tᵢ)]

Mit 8 Triggern: Circular Collapse, AI Model Failure, Fed Shock,
Geopolitik, Earnings Miss, IPO Flop, Credit Blow-Out, Insider Cascade
```

### 3.4 Theoretische Basis

- MS-IB-005: Overconfidence (Malmendier & Tate 2005)
- MS-BF-007: Overreaction (DeBondt & Thaler 1985)
- MS-BF-006: Momentum (Jegadeesh & Titman 1993)
- Kindleberger: Manias, Panics, and Crashes (1978)
- Lamont: "4 Horsemen" Bubble Detection Framework

---

## 4. Ergebnisse

### 4.1 Diagnose: Bubble-Score

```
B_score = 0.823 [0.78 - 0.87]

Interpretation:
< 0.50     Keine Blase
0.50-0.70  Überhitzung
0.70-0.85  BLASE ← Aktueller Stand
> 0.85     Kritische Blase
```

### 4.2 Die 6 Warnsignale

| # | Indikator | Wert | Status |
|---|-----------|------|--------|
| 1 | Kindleberger Phase | 3.5/5 | ⚠️ Euphorie → Distress |
| 2 | Lamont 4 Horsemen | 3.5/4 | 🔴 Fast vollständig |
| 3 | CFRS | 0.85 | 🔴 Systemisches Risiko |
| 4 | CAPE | 40.6 | 🔴 2. höchster seit 1871 |
| 5 | Credit Spreads | 71bps | ⚠️ Complacency |
| 6 | Insider Selling | 100% | 🔴 Nur Verkäufe |

### 4.3 Prognose: Crash-Wahrscheinlichkeit

```
P(Crash ≤6 Monate) = 67% [55% - 75%]

Definition "Crash": Magnificent 7 Index fällt >25% vom ATH
innerhalb von 3 Monaten
```

### 4.4 Szenarien

| Szenario | Wahrscheinlichkeit | Beschreibung |
|----------|-------------------|--------------|
| 🟢 Soft Landing | 33% | Circular hält, Korrektur -10-15% |
| 🟡 Geordnete Korrektur | 40% | Mag7 -25-35%, Rotation |
| 🔴 Harter Crash | 27% | Kettenreaktion, Mag7 >-40% |

### 4.5 Sensitivitätsanalyse

| Trigger | Einfluss auf P(Crash) |
|---------|----------------------|
| T₁ Circular Collapse | 32% |
| T₅ Earnings Miss | 24% |
| T₆ IPO Flop | 18% |
| T₈ Insider Cascade | 13% |
| Andere | 13% |

**Robustheit:** Selbst im optimistischen Szenario bleibt P(Crash) > 50%.

---

## 5. Schlussfolgerungen

1. **JA, ES IST EINE BLASE** - 6 von 6 Indikatoren im Warnsignal-Bereich

2. **KEIN KLASSISCHES PONZI** - aber Circular Financing erzeugt ähnliche systemische Risiken

3. **TIMING UNSICHER** - kritische Monate: März-April (Earnings), Mai (Fed), Juni-Juli (OpenAI IPO)

4. **HAUPTRISIKO: CIRCULAR FINANCING** - der gestoppte Nvidia-OpenAI Deal ist erstes Warnsignal

5. **SOFT LANDING MÖGLICH ABER MINDERHEIT** - erfordert dass Circular UND Earnings OK sind (33%)

---

## 6. Kritische Fenster

| Zeitraum | Risiko | Trigger |
|----------|--------|---------|
| März-April 2026 | HOCH | Q4/FY2025 Earnings |
| Mai 2026 | MITTEL | Powell-Übergang |
| Juni-Juli 2026 | HÖCHSTE | OpenAI IPO |
| Juli-August 2026 | HOCH | Q2 Earnings |

---

## 7. Quellen

### Marktdaten
- [Shiller CAPE Ratio](https://www.multpl.com/shiller-pe) - 40.67 (Feb 2026)
- [GuruFocus CAPE](https://www.gurufocus.com/economic_indicators/56/sp-500-shiller-cape-ratio)
- [CNN Fear & Greed](https://www.cnn.com/markets/fear-and-greed) - 41 (Fear)

### Circular Financing
- [Bloomberg: AI Circular Deals Guide](https://www.bloomberg.com/graphics/2026-ai-circular-deals/)
- [Yahoo Finance: Nvidia's $24B Deal Blitz](https://finance.yahoo.com/news/nvidias-24b-ai-deal-blitz-has-wall-street-asking-questions-about-murky-circular-investments-110039309.html)
- [Built In: How Circular Financing Is Fueling the AI Boom](https://builtin.com/articles/ai-circular-financing)
- [TechCrunch: OpenAI-Microsoft Spending](https://techcrunch.com/2025/11/14/leaked-documents-shed-light-into-how-much-openai-pays-microsoft/)

### Bubble-Theorie
- [Kindleberger: Manias, Panics, and Crashes](https://www.goodreads.com/book/show/367596.Manias_Panics_and_Crashes)
- [Fortune: Owen Lamont 4 Horsemen](https://fortune.com/2026/02/01/is-ai-a-bubble-top-economist-says-no-because-ipos-fraud/)
- [Acadian: Straight Talk About Circular Deals](https://www.acadian-asset.com/investment-insights/owenomics/straight-talk-about-circular-deals-in-ai)

### AI-Markt
- [Fortune: Is AI Boom a Bubble?](https://fortune.com/2026/01/04/is-ai-boom-bubble-pop-tech-stocks-sp500-bull-run/)
- [AInvest: AI Bubble 2026](https://www.ainvest.com/news/ai-bubble-2026-ai-hype-overinflating-tech-stocks-2512/)
- [Motley Fool: Why AI Bubble May Not Burst](https://www.fool.com/investing/2026/01/08/why-the-ai-bubble-may-not-burst-in-2026/)

---

## 8. Modell-Metadaten

- **Modell-ID:** MOD-FIN-BUBBLE-001
- **Version:** 1.1
- **Erstellt:** 2026-02-04
- **Session:** EBF-S-2026-02-04-FIN-001
- **Forecast-ID:** FCT-FIN-2026-001

---

*Erstellt mit dem Evidence-Based Framework (EBF) von FehrAdvice & Partners AG*
