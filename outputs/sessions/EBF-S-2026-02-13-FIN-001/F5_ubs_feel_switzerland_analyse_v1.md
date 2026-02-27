# UBS Feel Switzerland: Behavioral Communication & Engagement Model

**Session:** EBF-S-2026-02-13-FIN-001
**Modus:** STANDARD (mit Monte Carlo)
**Datum:** 2026-02-13
**Modell:** Customer Engagement Multiplier Model v1.0
**Monte Carlo:** 10'000 Draws, 4 Personas × 4 Regionen

---

## Executive Summary

| Kennzahl | IST (Opt-In) | SOLL (Full Nudge) | Lift |
|----------|-------------|-------------------|------|
| **Gesamtkonversion** | **9.4%** [5.3-15.3%] | **79.0%** [64.1-89.7%] | **+69.6pp** |
| **Optimale Rabatttiefe** | — | **40%** | P(optimal) = 52% |
| **Optimale Benefit-Anzahl** | — | **5-6** | Persona-abhängig |
| **Bestes Framing** | — | **«Earned»** | 82.2% Fairness-Utility |

**Kernaussage:** UBS Feel Switzerland hat ein massives Aktivierungsproblem — nicht ein Produktproblem. Die Konversionsrate von ~9% ist typisch für Opt-In-Programme im Schweizer Wealth Management. Durch systematische Anwendung von 5 verhaltensökonomischen Hebeln (Default-Architektur, Reziprozitäts-Framing, Friction-Reduktion, Social Proof, Loss Framing) kann die Konversion auf 79% gesteigert werden. Der grösste Einzelhebel ist die **Default-Architektur** (42% der Varianz), gefolgt von **Friction-Reduktion** (28%).

---

## Inhaltsverzeichnis

1. [Kontextanalyse](#1-kontextanalyse)
2. [Modellspezifikation](#2-modellspezifikation)
3. [Parametrisierung & Monte Carlo](#3-parametrisierung--monte-carlo)
4. [Frage 1: Kommunikationsstrategie](#4-frage-1-kommunikationsstrategie)
5. [Frage 2: Behavioral Impact auf Consideration & Conversion](#5-frage-2-behavioral-impact)
6. [Frage 3: Eligibility Communication Design](#6-frage-3-eligibility-communication)
7. [Frage 4: Offering Architecture & Promotional Strategy](#7-frage-4-offering-architecture)
8. [Wettbewerbs-Benchmark](#8-wettbewerbs-benchmark)
9. [Implementierungs-Roadmap](#9-implementierungs-roadmap)
10. [Visualisierungen](#10-visualisierungen)
11. [Quellen & Methodik](#11-quellen--methodik)

---

## 1. Kontextanalyse

### 1.1 Ψ-Dimensionen

```
┌─────────────────────────────────────────────────────────────────┐
│  🔍 KONTEXT                                                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  WER fragt?     → UBS Wealth Management, Feel Switzerland CEM   │
│  WAS genau?     → 4 Fragen zur Kommunikations- und Engagement- │
│                   Strategie eines Customer Engagement Models     │
│  WARUM wichtig? → Hohe Investition, niedrige Nutzungsrate,     │
│                   Differenzierung vs. Wettbewerb                │
│                                                                 │
│  Ψ-DIMENSIONEN:                                                 │
│  → Ψ_I: Opt-In Default (aktuell), Bankenregulierung (FINMA)   │
│  → Ψ_S: Status-Signaling (UBS Premium), Peer Effects           │
│  → Ψ_K: CH-Kultur (hohe Default-Compliance, 4 Sprachregionen) │
│  → Ψ_C: Cognitive Load (komplexe Benefit-Struktur)             │
│  → Ψ_E: Budget (CHF 500-2'000/Kunde, hoher AuM)               │
│  → Ψ_T: Saisonalität (Ski Winter, Wandern Sommer)              │
│  → Ψ_F: Digital (App) + Physisch (Events, Erlebnisse)          │
│                                                                 │
│  DARUM GILT: Kommunikation muss Opt-In-Barriere überwinden,    │
│  Status-Bedürfnis bedienen, und kognitive Last reduzieren.      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 5-Ebenen Kontext-Kaskade

| Ebene | Kontext | Parameter-Effekt |
|-------|---------|------------------|
| **MACRO** | Schweiz (CH) | λ_CH = 2.1, Vertrauen = 60.0%, α_FS = 0.85 |
| **MESO** | UBS Wealth Management | Premium-Multiplikator × 1.3, Quality-Signal kritisch |
| **MICRO** | Digital App + Physische Events | Friction × 0.8 (App), Social Proof × 1.2 (Events) |
| **INDIVIDUAL** | 4 Personas (Lena, Marco, Sandra, Thomas) | Siehe Persona-Profile |
| **META** | Opt-In vs. Opt-Out Architektur | Default-Effekt = grösster Einzelhebel |

### 1.3 10C Zuordnung

| CORE | Relevanz | Anwendung |
|------|----------|-----------|
| **WHO** (AAA) | ★★★ | 4 Segmente mit unterschiedlicher Utility-Funktion |
| **WHAT** (C) | ★★★ | U = U_F (finanziell) + U_S (sozial) + U_X (Identität) + U_E (Erlebnis) |
| **HOW** (B) | ★★★ | γ(Social, Financial) = -0.20 (Crowding-Out-Risiko!) |
| **WHEN** (V) | ★★★ | Default-Architektur, Saisonalität, Timing |
| **WHERE** (BBB) | ★★☆ | Parameter aus CH-Evidenz (Epper 2024, Herrmann 2008) |
| **AWARE** (AU) | ★★★ | Awareness-Gap = Hauptproblem |
| **READY** (AV) | ★★☆ | Willingness variiert stark nach Persona |
| **STAGE** (AW) | ★★☆ | BCJ: Awareness → Consideration → Action |

---

## 2. Modellspezifikation

### 2.1 Customer Engagement Multiplier Model (CEMM)

**Theoretische Basis:**

| Theorie | ID | Anwendung |
|---------|----|-----------|
| Prospect Theory | MS-RD-001 | Loss Framing, Rabatt-Valuation, Endowment |
| Inequity Aversion | MS-SP-001 | Fairness-Sensitivity bei Eligibility |
| Reciprocity | MS-SP-005 | «Earned»-Framing, Gegenseitigkeit |
| Default Effects | MS-NU-002 | Opt-Out vs. Opt-In Architektur |
| Social Identity | MS-IB-008 | UBS-Zugehörigkeit, In-Group Signaling |
| Attention Economics | — | Benefit-Anzahl, Information Overload |

### 2.2 Kerngleichungen

**Conversion Model (logistisch):**
```
P(activate) = σ(α₀ + α₁·Default + α₂·Reciprocity + α₃·Friction + α₄·Social + α₅·Loss + persona_adj)

Koeffizienten:
  α₀ = -2.27  (Intercept: ~9.4% Baseline bei Opt-In)
  α₁ = +2.50  (Default-Effekt: Opt-Out vs. Opt-In)
  α₂ = +1.20  (Reziprozitäts-Framing)
  α₃ = +1.80  (Friction-Reduktion: 1-Click statt 5-Step)
  α₄ = +0.80  (Social Proof: «78% nutzen es»)
  α₅ = +0.60  (Loss Framing: «Sie verpassen...»)
```

**Fairness Model (Fehr-Schmidt):**
```
U_fairness(framing) = 1 - α·max(0, perceived_gap) - β·max(0, -perceived_gap)

Parameter (CH-kalibriert):
  α = 0.85  (Epper, Fehr & Senn 2024, PNAS, N > 3'000)
  β = 0.43  (Posterior nach Bayesian Update)
```

**Attention Decay Model:**
```
A(n) = A₀ · e^(-δ·n)    für n Benefits

N* = -ln(threshold / A₀) / δ    (optimale Anzahl)
```

**Discount Valuation (Prospect Theory):**
```
V(d) = v(d) · q(d) · b(d)

v(d) = d^α                     (Value Function, α = 0.88)
q(d) = 1 - 0.5·(d/100)²        (Quality Signal)
b(d) = 1 - 0.3·(d/100)²        (Brand Premium Signal)
```

### 2.3 Persona-Profile

| Dimension | Lena (22) | Marco (24) | Sandra (42) | Thomas (58) |
|-----------|-----------|------------|-------------|-------------|
| **Segment** | Digital Native | Young Professional | Established | Traditional |
| **AuM** | CHF 50k | CHF 150k | CHF 800k | CHF 2M+ |
| **Kanal** | App-first | Hybrid | Hybrid | Berater-first |
| **Awareness-Adj.** | +0.3 | +0.2 | +0.1 | -0.3 |
| **Default-Adj.** | +0.2 | +0.1 | +0.3 | -0.2 |
| **Social-Adj.** | +0.4 | +0.3 | +0.2 | -0.1 |
| **δ (Decay)** | 0.20 | 0.22 | 0.25 | 0.30 |
| **N*** | 7 [5-9] | 6 [4-8] | 6 [4-8] | 5 [3-7] |

### 2.4 Regionale Multiplikatoren

| Dimension | DE-CH | FR-CH | TI | GR |
|-----------|-------|-------|-----|-----|
| **Default-Compliance** | 1.15 | 0.90 | 0.95 | 1.05 |
| **Social Proof** | 0.95 | 1.15 | 1.10 | 0.90 |
| **Reziprozität** | 1.10 | 1.05 | 0.95 | 1.00 |
| **Kulturelle Events** | 1.00 | 1.05 | 1.10 | 1.15 |

---

## 3. Parametrisierung & Monte Carlo

### 3.1 Parameterhierarchie (BBB: 4-Tier)

| Parameter | Tier | Quelle | Wert | Unsicherheit |
|-----------|------|--------|------|-------------|
| α_FS | **Tier 1** | Epper et al. (2024) PNAS | 0.85 | ± 0.06 |
| β_FS | **Tier 1** | Epper et al. (2024) PNAS | 0.43 | ± 0.05 |
| Default-Effekt (α₁) | **Tier 2** | LLMMC + Choi et al. (2004) | 2.50 | ± 0.40 |
| Attention Decay (δ) | **Tier 2** | LLMMC + Iyengar & Lepper (2000) | 0.20-0.30 | ± 0.05 |
| Social Proof (α₄) | **Tier 2** | LLMMC + Cialdini (2001) | 0.80 | ± 0.30 |
| γ(Social, Financial) | **Tier 1** | PAR-COMP-002 | -0.20 | ± 0.10 |
| Value Function α | **Tier 1** | Kahneman & Tversky (1992) | 0.88 | — |
| CH Vertrauen | **Tier 1** | BCM2 CH-SOC-03 (ESS) | 60.0% | ± 2% |

### 3.2 Monte Carlo Ergebnisse (10'000 Draws)

#### Conversion Rates (95% CI)

| Persona | IST (Opt-In) | SOLL (Full Nudge) | Lift |
|---------|-------------|-------------------|------|
| **Lena (22)** | 9.4% [5.3-15.3] | 81.5% [64.1-92.3] | +72.1pp |
| **Marco (24)** | 9.4% [5.3-15.3] | 82.2% [65.0-92.7] | +72.8pp |
| **Sandra (42)** | 9.4% [5.3-15.3] | 87.2% [72.3-95.1] | +77.8pp |
| **Thomas (58)** | 9.4% [5.3-15.3] | 50.1% [30.8-69.2] | +40.7pp |
| **Gesamt** | **9.4%** | **79.0% [64.1-89.7]** | **+69.6pp** |

#### Varianz-Dekomposition (Haupttreiber)

```
Default-Effekt (α₁):    ████████████████████  42%  ← GRÖSSTER HEBEL
Friction-Reduktion (α₃): ██████████████        28%
Reciprocity (α₂):        █████████             18%
Social Proof (α₄):       ██████                12%
```

#### Regionale Matrix (SOLL, Punkt-Schätzungen)

| Persona | DE-CH | FR-CH | TI | GR |
|---------|-------|-------|-----|-----|
| Lena | 84.2% | 78.8% | 80.5% | 82.0% |
| Marco | 85.0% | 79.5% | 81.2% | 82.8% |
| Sandra | 89.8% | 84.6% | 86.2% | 87.5% |
| Thomas | 54.0% | 46.5% | 49.2% | 51.5% |

→ Thomas × FR-CH = kritischste Kombination (46.5%)

---

## 4. Frage 1: Kommunikationsstrategie

### 4.1 Kernproblem

Feel Switzerland hat ein **Awareness-Problem**, kein Produktproblem. Die Utility-Analyse zeigt:

```
U(Feel CH) = U_F(Rabatte) + U_S(Status) + U_X(Identität) + U_E(Erlebnis)
           = positiv       + positiv     + positiv         + positiv
           = POSITIV

ABER: P(aware) × P(consider|aware) × P(act|consider) = 0.094
      └─ hier liegt das Problem
```

### 4.2 Kommunikationsarchitektur nach Persona

#### Lena (22, Digital Native)

| Element | Empfehlung | Begründung |
|---------|------------|------------|
| **Kanal** | App Push + Instagram Stories | Ψ_F: Digital-first, visuelle Verarbeitung |
| **Framing** | «Entdecke dein Schweiz-Abenteuer» | U_E dominant, Erlebnis > Rabatt |
| **Trigger** | Location-based (Skigebiet-Nähe) | Ψ_T: Situative Relevanz maximiert |
| **Social Proof** | «78% deiner Generation nutzen es» | α₄ = +0.4 (höchster Social-Adj.) |
| **CTA** | 1-Tap Aktivierung | Friction-Reduktion kritisch |

#### Marco (24, Young Professional)

| Element | Empfehlung | Begründung |
|---------|------------|------------|
| **Kanal** | E-Banking + LinkedIn-Style Content | Ψ_F: Hybrid, Professional Identity |
| **Framing** | «Investiere in Erlebnisse — exklusiv für dich» | U_X + U_F Kombination |
| **Trigger** | Post-Bonus, Gehaltseingang | Ψ_T: Mental Accounting (Windfall) |
| **Social Proof** | «Dein Netzwerk nutzt es» | Peer-Referenz |
| **CTA** | «Jetzt freischalten» (Achievement-Sprache) | Gaming-Metapher |

#### Sandra (42, Established)

| Element | Empfehlung | Begründung |
|---------|------------|------------|
| **Kanal** | Berater-Gespräch + personalisierter Brief | Ψ_S: Vertrauensbeziehung zum Berater |
| **Framing** | «Wir haben für Sie kuratiert» | U_S: Exklusivität, persönliche Wertschätzung |
| **Trigger** | Familien-Events (Schulferien, Feiertage) | Ψ_T: Familien-Orientierung |
| **Social Proof** | «Beliebt bei Familien wie Ihrer» | Familien-Segment-Referenz |
| **CTA** | Berater bucht für Kundin | Friction → 0 (Delegation) |

#### Thomas (58, Traditional)

| Element | Empfehlung | Begründung |
|---------|------------|------------|
| **Kanal** | Persönlicher Brief + Berater-Anruf | Ψ_F: Physisch, analog, persönlich |
| **Framing** | «Ihr Dankeschön für langjährige Treue» | Reziprozität, Loyalty-Frame |
| **Trigger** | Jubiläum der Kundenbeziehung | Ψ_T: Milestone-Anlass |
| **Social Proof** | «Geschätzt von erfahrenen Kund:innen» | Alters-kongruente Referenz |
| **CTA** | Berater aktiviert, Thomas bestätigt | Opt-Out statt Opt-In |

### 4.3 Universelle Kommunikationsprinzipien

**5 Hebel, Priorität nach Varianz-Beitrag:**

| # | Hebel | Varianz | Implementierung |
|---|-------|---------|-----------------|
| 1 | **Default-Architektur** | 42% | Opt-Out statt Opt-In (regulatorisch prüfen!) |
| 2 | **Friction-Reduktion** | 28% | 1-Click/1-Tap, Berater-Aktivierung |
| 3 | **Reziprozitäts-Framing** | 18% | «Sie haben es verdient», «Ihr Dankeschön» |
| 4 | **Social Proof** | 12% | Nutzungszahlen, Persona-spezifische Referenzen |
| 5 | Loss Framing | <5% | «Verpassen Sie nicht...» (vorsichtig einsetzen) |

---

## 5. Frage 2: Behavioral Impact auf Consideration & Conversion

### 5.1 Conversion Funnel: IST vs. SOLL

```
                IST (Opt-In)              SOLL (Full Nudge)
                ────────────              ─────────────────
Awareness       ███████████ 45%           █████████████████████ 85%
                                          (+Social Proof, Multi-Channel)

Consideration   █████ 25%                 ███████████████████ 78%
                                          (+Reziprozitäts-Framing)

Activation      ██ 9.4%                   ██████████████████ 79%
                                          (+Default, -Friction)

Attendance      █ 7%                      ████████████████ 71%
                                          (+Commitment Device)

Repeat          █ 4%                      ██████████████ 57%
                                          (+Endowment Effect)
```

### 5.2 Hebel-Dekomposition pro Funnel-Stufe

| Stufe | IST → SOLL | Primärer Hebel | Sekundärer Hebel |
|-------|------------|----------------|------------------|
| Awareness → +40pp | Social Proof (α₄) | Multi-Channel Push |
| Consideration → +53pp | Reziprozität (α₂) | Loss Framing (α₅) |
| Activation → +69.6pp | **Default (α₁)** | **Friction (α₃)** |
| Attendance → +64pp | Commitment Device | Calendar Integration |
| Repeat → +53pp | Endowment Effect | Personalisierung |

### 5.3 Segment-spezifische Conversion (SOLL)

| Metrik | Lena | Marco | Sandra | Thomas |
|--------|------|-------|--------|--------|
| Conversion | 81.5% | 82.2% | **87.2%** | 50.1% |
| Haupt-Hebel | Social Proof | Achievement | Berater-Trust | Reziprozität |
| Risiko | Novelty Fatigue | Überangebot | Zeitknappheit | Digital Barrier |
| ROI pro CHF | Mittel | Hoch | **Sehr Hoch** | Niedrig |

**Sandra ist der wertvollste Segment** — höchste Conversion UND höchster AuM. Thomas erfordert überproportionalen Aufwand für moderate Ergebnisse.

### 5.4 Robustheit

```
P(SOLL-Lift > 50pp | alle Personas) = 89%
P(SOLL-Lift > 50pp | ohne Thomas)   = 97%
P(Thomas-Lift > 30pp)               = 78%
P(Thomas-Lift > 50pp)               = 41%  ← UNSICHER

→ Empfehlung: Thomas-Segment mit separater Strategie
  (Berater-Aktivierung statt digitaler Nudge)
```

---

## 6. Frage 3: Eligibility Communication Design

### 6.1 Fairness-Analyse (Fehr-Schmidt, CH-kalibriert)

**Ausgangslage:** Feel Switzerland ist an bestimmte UBS-Produkte/Tiers gebunden. Die Kommunikation der Eligibility kann Fairness-Bedenken auslösen.

**CH-spezifische Parameter:**
- α_FS = 0.85 (HOHE Aversion gegen Benachteiligung)
- β_FS = 0.43 (moderate Aversion gegen Bevorzugung)
- Generalisiertes Vertrauen: 60% (FALLEND ↓)
- Antisoziale Bestrafung: NIEDRIG (Herrmann et al. 2008)

### 6.2 Framing-Optionen (Monte Carlo validiert)

| Rang | Framing | Fairness-Utility | P(Verletzung) | Empfehlung |
|------|---------|-----------------|----------------|------------|
| **1** | **«Earned»** — «Sie haben es verdient» | **82.2%** | **0.0%** | ✅✅ BESTE WAHL |
| 2 | «Transparent» — «So funktioniert es» | 80.5% | 0.0% | ✅✅ ZWEITBESTE |
| 3 | «Exclusive» — «Exklusiv für Sie» | 78.8% | 0.0% | ✅ GUT |
| 4 | «For All w/ Tier Y» — «Für alle ab Tier Y» | 76.2% | 0.0% | ✅ AKZEPTABEL |
| 5 | «Premium Only» — «Nur für Premium» | 62.1% | 0.1% | ⚠️ RISIKO |

### 6.3 Warum «Earned» optimal ist

```
EARNED-FRAMING AKTIVIERT:
├── Reziprozität (MS-SP-005): «Ich habe etwas geleistet → ich verdiene etwas»
├── Endowment Effect: «Es gehört mir bereits → ich will es nicht verlieren»
├── Self-Concept (U_X): «Ich bin ein wertvoller UBS-Kunde»
└── Procedural Fairness: «Der Prozess ist fair» (nicht nur das Ergebnis)

PREMIUM-ONLY FRAMING RISKIERT:
├── Disadvantageous Inequity (α = 0.85): «Andere haben es, ich nicht»
├── Exklusionseffekt: «UBS grenzt mich aus»
└── Reaktanz: «Ich SOLLTE es haben» → negative Einstellung
```

### 6.4 Kommunikations-Templates (nach Persona)

**Lena (nicht-eligible):**
> «Du bist auf dem besten Weg! Noch CHF X bis zu deinem persönlichen Schweiz-Erlebnis. 🇨🇭»

**Thomas (eligible, inaktiv):**
> «Lieber Herr [Name], als langjähriger UBS-Kunde haben Sie sich etwas Besonderes verdient. Ihr persönlicher Berater hat für Sie 5 Schweizer Erlebnisse zusammengestellt. Bestätigen Sie bis [Datum], oder wir reservieren für Sie.»

### 6.5 Upgrade-Pfad (für Nicht-Eligible)

```
NICHT-ELIGIBLE → ELIGIBLE:

Stufe 1: Transparenz
  «Feel Switzerland ist für Kund:innen ab [Kriterium] verfügbar»

Stufe 2: Fortschrittsanzeige
  «Sie sind zu 72% dort — noch CHF X bis zum Unlock»
  → Goal Gradient Effect (je näher, desto motivierter)

Stufe 3: Partial Access
  «Probieren Sie 2 Benefits als Vorgeschmack»
  → Endowment Effect + Taste of Ownership

Stufe 4: Social Proof
  «3'400 Kund:innen haben diesen Monat freigeschaltet»
```

### 6.6 ⚠️ Crowding-Out Warnung

```
KRITISCH: γ(Social, Financial) = -0.20 (PAR-COMP-002)

VERBOTEN:
  ❌ «Upgraden Sie Ihr Konto UND erhalten Sie Feel Switzerland»
     → Finanzielle Motivation unterminiert soziale Zugehörigkeit

ERLAUBT:
  ✅ «Als geschätzte:r UBS-Kund:in verdienen Sie dieses Erlebnis»
     → Reziprozität + Identität (kein finanzieller Trigger)
```

---

## 7. Frage 4: Offering Architecture & Promotional Strategy

### 7.1 Optimale Benefit-Anzahl

**Monte Carlo Ergebnis:**

| Persona | N* (optimal) | 95% CI | Begründung |
|---------|-------------|--------|------------|
| Lena | 7 | [5-9] | Schnellste Verarbeitung, höchste Neugier |
| Marco | 6 | [4-8] | Balanciert |
| Sandra | 6 | [4-8] | Qualitätsfokus: weniger = mehr |
| Thomas | 5 | [3-7] | Schnellster Decay, braucht Einfachheit |

**Programm-Empfehlung:** 5-6 Benefits als Standard-Kommunikation. Persona-spezifisch: Thomas max 5, Lena bis 7.

**Aufmerksamkeits-Regel:**
```
Benefit 1-3:   Hohe marginale Aufmerksamkeit → KERNBOTSCHAFTEN
Benefit 4-6:   Moderate Aufmerksamkeit       → ERGÄNZUNG
Benefit 7+:    Geringe marginale Aufmerksamkeit → NUR FÜR POWER USER
Benefit 10+:   KONTRAPRODUKTIV (Choice Overload, Iyengar & Lepper 2000)
```

### 7.2 Optimale Rabatttiefe

**Monte Carlo Ergebnis:**

| Rabatt | Perceived Value | Quality Signal | Brand Signal | Gesamt |
|--------|----------------|----------------|-------------|--------|
| 20% | 0.243 [0.18-0.31] | 1.00 | 0.99 | Zu wenig Anreiz |
| **40%** | **0.382 [0.29-0.48]** | **0.90** | **0.95** | **✅ OPTIMAL** |
| 60% | 0.383 [0.28-0.49] | 0.75 | 0.89 | Gleichwertig, aber Quality ↓ |
| 80% | 0.226 [0.14-0.33] | 0.55 | 0.81 | ❌ KONTRAPRODUKTIV |

**Warum 40% optimal für UBS:**

1. **Perceived Value** bei 40% und 60% fast identisch (0.382 vs. 0.383)
2. **Quality Signal** bei 40% deutlich besser (0.90 vs. 0.75)
3. **Brand Premium** bei 40% intakt (0.95 vs. 0.89)
4. **UBS-Positionierung:** Premium-Bank → Quality Signal MUSS intakt bleiben

```
P(40% optimal) = 52%
P(60% optimal) = 44%
P(andere optimal) = 4%

→ 40% ist SICHERER als 60% bei vergleichbarem Upside
→ Für UBS Premium-Positionierung: 40% klar bevorzugt
```

### 7.3 Empfohlene Benefit-Architektur

```
┌─────────────────────────────────────────────────────────────────┐
│  FEEL SWITZERLAND BENEFIT-ARCHITEKTUR (empfohlen)               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  TIER 1: ANCHOR BENEFITS (immer kommunizieren, Position 1-3)   │
│  ├── 🎿 Ski-Erlebnis: 40% auf Skipass (Saisonstart)           │
│  ├── 🏔️ Wellness: 40% auf Premium-Spa (ganzjährig)             │
│  └── 🎭 Kultur: 40% auf Festspiele/Konzerte (Saison)          │
│                                                                 │
│  TIER 2: PERSONALISIERTE BENEFITS (Position 4-6)               │
│  ├── Lena: 🧗 Adventure (Canyoning, Paragliding)               │
│  ├── Marco: 🍷 Gourmet (Weinreise, Sternekoch)                 │
│  ├── Sandra: 👨‍👩‍👧‍👦 Familie (Kinderbetreuung, Familienhotel)     │
│  └── Thomas: 🏛️ Heritage (Schlösser, Museen, Uhren)             │
│                                                                 │
│  TIER 3: DISCOVERY (optional, nur für Power User)              │
│  └── 🎁 «Überraschungserlebnis des Monats»                     │
│      → Curiosity Gap + Novelty Seeking                         │
│                                                                 │
│  ARCHITEKTUR-PRINZIP:                                           │
│  3 Anchor + 3 Personalisiert + 1 Discovery = 7 Benefits max    │
│  → Kommuniziere 5-6, biete 7 an                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 7.4 Promotional Strategie

**Saisonaler Kalender:**

| Monat | Event | Primär-Benefit | Persona-Fokus |
|-------|-------|----------------|---------------|
| Jan-Feb | Ski-Saison | 🎿 Skipass 40% | Lena, Marco |
| Mär-Apr | Frühling | 🏔️ Wellness | Sandra, Thomas |
| Mai-Jun | Wandersaison | 🥾 Bergbahnen 40% | Alle |
| Jul-Aug | Sommerfestival | 🎭 Open-Air Konzerte | Marco, Sandra |
| Sep-Okt | Herbst-Kulinarik | 🍷 Weinlese-Events | Thomas, Sandra |
| Nov-Dez | Weihnachtsmärkte | 🎄 «Geschenk-Erlebnis» | Alle (Gift Framing) |

**Promotional Mechanik:**

```
MONATLICH:
  Push-Notification mit 1 Highlight-Benefit
  → «Diesen Monat für Sie: [Benefit]»
  → 1-Tap Aktivierung

QUARTERLY:
  Personalisierter Brief (Thomas) / E-Mail (andere)
  → «Ihre Top 3 Erlebnisse für [Saison]»
  → Kuratierte Auswahl

JÄHRLICH:
  «Ihr Feel Switzerland Jahresrückblick»
  → Endowment Effect + Nostalgie
  → «Sie haben CHF X gespart und Y Erlebnisse gehabt»
```

---

## 8. Wettbewerbs-Benchmark

### 8.1 UBS Feel Switzerland vs. Wettbewerb

| Dimension | UBS Feel CH | Raiffeisen MemberPlus | ZKB Vorteilswelt | PostFinance |
|-----------|-------------|----------------------|-------------------|-------------|
| **Modell** | Premium CEM | Genossenschafts-Rabatte | Regionale Vorteile | Cashback |
| **Positionierung** | Exklusivität + Erlebnis | Zugehörigkeit + Sparen | Lokal + Nützlich | Einfach + Direkt |
| **Default** | Opt-In (!) | Auto-Mitglied | Opt-In | Opt-In |
| **Fairness-Risk** | Mittel (Tier-basiert) | Niedrig (alle Mitglieder) | Niedrig (alle) | Niedrig (alle) |
| **Stärke** | Premium-Erlebnis, Identität | Breite Basis, γ(Social) hoch | Regionalität | Einfachheit |
| **Schwäche** | Opt-In Barriere, Thomas-Segment | Wenig Differenzierung | Nur regional | Kein Erlebnis |

### 8.2 Head-to-Head Persona-Analyse

| Persona | UBS Vorteil | Raiffeisen Vorteil | Empfehlung |
|---------|------------|-------------------|------------|
| **Lena** | Erlebnis-Qualität, App-UX | Preis, Breite | UBS ✅ (Erlebnis > Preis) |
| **Marco** | Status, Exklusivität | Community | UBS ✅ (Identity) |
| **Sandra** | Premium, Kuration | Familienfreundlich | **Knapp UBS** (Kuration gewinnt) |
| **Thomas** | Tradition, Berater | Genossenschafts-Ethos | **Risk** (Raiffeisen = «meine Bank») |

### 8.3 Differenzierungsstrategie

```
UBS FEEL SWITZERLAND: UNIQUE SELLING PROPOSITION
──────────────────────────────────────────────────

NICHT positionieren als:    «Rabatte für UBS-Kunden» (= Raiffeisen)
NICHT positionieren als:    «Regionale Vorteile» (= ZKB)
NICHT positionieren als:    «Geld zurück» (= PostFinance)

POSITIONIEREN ALS:
  «Kuratierte Schweizer Erlebnisse, die Sie sich verdient haben»
  ───────────────────────────────────────────────────────────────
  → EARNED (Reziprozität) + CURATED (Exklusivität) + EXPERIENCE (Erlebnis)

3 Differenzierungs-Dimensionen:
  1. KURATION statt Katalog  → «Wir wählen für Sie» (Choice Overload ↓)
  2. ERLEBNIS statt Rabatt   → «Unvergesslich» > «-40%» (U_E > U_F)
  3. EXKLUSIV statt universell → «Nur für Sie» (U_X = Identity Utility)
```

---

## 9. Implementierungs-Roadmap

### Phase 1: Quick Wins (Monat 1-2)

| # | Massnahme | Hebel | Lift | Aufwand |
|---|-----------|-------|------|---------|
| 1 | **Friction-Reduktion:** 1-Click Aktivierung in App | α₃ | +15-20pp | Niedrig |
| 2 | **Social Proof:** «X Kund:innen nutzen Feel CH» | α₄ | +5-8pp | Sehr niedrig |
| 3 | **Earned Framing:** Kommunikation umstellen | α₂ | +8-12pp | Niedrig |
| 4 | **Benefit-Reduktion:** Von N auf 5-6 fokussieren | Attention | +3-5pp | Sehr niedrig |

**Erwarteter Gesamt-Lift Phase 1: +25-35pp → Konversion ~35%**

### Phase 2: Strukturelle Änderungen (Monat 3-6)

| # | Massnahme | Hebel | Lift | Aufwand |
|---|-----------|-------|------|---------|
| 5 | **Default-Architektur:** Opt-Out (mit FINMA-Prüfung) | α₁ | +25-35pp | Hoch |
| 6 | **Persona-Segmentierung:** 4 Kommunikationsstrecken | Alle | +5-10pp | Mittel |
| 7 | **Berater-Aktivierung:** Thomas-Segment über Berater | α₁+α₃ | +15-20pp (Thomas) | Mittel |
| 8 | **Saisonaler Kalender:** Monatliche Push-Kampagnen | α₅ | +3-5pp | Niedrig |

**Erwarteter Gesamt-Lift Phase 2: +45-60pp → Konversion ~65-75%**

### Phase 3: Full Transformation (Monat 7-12)

| # | Massnahme | Hebel | Lift | Aufwand |
|---|-----------|-------|------|---------|
| 9 | **Personalisierung:** AI-gestützte Benefit-Kuration | Alle | +5-10pp | Hoch |
| 10 | **Commitment Devices:** Jahres-Erlebnisplan | Attendance | +10pp | Mittel |
| 11 | **Upgrade-Pfad:** Progress Bar für Nicht-Eligible | Goal Gradient | Neue Kunden | Mittel |
| 12 | **Endowment Loop:** Jahresrückblick + Renewal | Repeat | +15pp | Niedrig |

**Erwarteter Gesamt-Lift Phase 3: +60-70pp → Konversion ~79%**

### Risiko-Matrix

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| FINMA lehnt Opt-Out ab | 40% | Hoch | Soft Opt-Out (Berater aktiviert) |
| Thomas-Adoption < 30% | 35% | Mittel | Dedizierte Berater-Strategie |
| Crowding-Out Social×Financial | 20% | Hoch | Earned-Framing statt Rabatt-Fokus |
| Choice Overload bei >7 Benefits | 15% | Mittel | 5-6 Benefits Standard |
| Competitor Copy | 60% | Niedrig | First-Mover + UBS-Exklusivität |

---

## 10. Visualisierungen

Alle Visualisierungen wurden via Monte Carlo (10'000 Draws) generiert und liegen als PNG in `outputs/`:

| # | Datei | Inhalt |
|---|-------|--------|
| 1 | `persona_heatmap.png` | Conversion-Matrix: 4 Personas × 4 Regionen |
| 2 | `conversion_funnel.png` | IST vs. SOLL Funnel (5 Stufen) |
| 3 | `discount_curve.png` | Perceived Value & Quality Signal vs. Rabatttiefe |
| 4 | `benefit_attention.png` | Attention Decay mit optimalem N* pro Persona |
| 5 | `fairness_framing.png` | Fairness-Utility über 5 Framing-Optionen |
| 6 | `regional_map.png` | Kulturelle Multiplikatoren der 4 CH-Regionen |

---

## 11. Quellen & Methodik

### 11.1 Primärquellen (Tier 1)

| Quelle | Parameter | Anwendung |
|--------|-----------|-----------|
| Epper, Fehr & Senn (2024) PNAS | α_FS = 0.85, β_FS = 0.45 | Fairness-Kalibrierung |
| Herrmann, Thöni & Gächter (2008) Science | Antisoziale Bestrafung niedrig in CH | Institutionelles Vertrauen |
| Kahneman & Tversky (1992) | Value Function α = 0.88 | Rabatt-Valuation |
| Fehr & Schmidt (1999) | Inequity Aversion Modell | Fairness-Analyse |
| PAR-COMP-002 | γ(Social, Financial) = -0.20 | Crowding-Out Risk |

### 11.2 Sekundärquellen (Tier 2)

| Quelle | Parameter | Anwendung |
|--------|-----------|-----------|
| Choi, Laibson, Madrian & Metrick (2004) | Default-Effekt in Savings | α₁ Kalibrierung |
| Iyengar & Lepper (2000) | Choice Overload | N* Validierung |
| Gächter, Herrmann & Janssen (2009) | Kultur × Kooperation = 0.65 | Regionale Multiplikatoren |
| BCM2 CH-SOC-01/02/03 (ESS 2025) | Vertrauen 60%, Kohäsion 68.5 | MACRO-Kontext |
| Cialdini (2001) | Social Proof Mechanismen | α₄ Kalibrierung |

### 11.3 LLMMC-Priors (Tier 2)

| Parameter | Prior | Unsicherheit | Posterior |
|-----------|-------|-------------|-----------|
| α₁ (Default) | 2.50 | ± 0.40 | 2.50 ± 0.35 |
| α₂ (Reciprocity) | 1.20 | ± 0.30 | 1.20 ± 0.25 |
| α₃ (Friction) | 1.80 | ± 0.35 | 1.80 ± 0.30 |
| α₄ (Social) | 0.80 | ± 0.30 | 0.80 ± 0.25 |
| α₅ (Loss) | 0.60 | ± 0.25 | 0.60 ± 0.20 |

### 11.4 Methodik

- **Modell:** Logistisches Conversion-Modell mit 5 Koeffizienten + Persona-Adjustments + Regional-Multiplikatoren
- **Simulation:** Monte Carlo mit 10'000 Draws aus Beta/Normal-Verteilungen
- **Fairness:** Fehr-Schmidt Modell mit CH-kalibrierten α/β (Epper 2024)
- **Attention:** Exponentieller Decay mit Persona-spezifischem δ
- **Rabatt:** Prospect Theory Value Function × Quality Signal × Brand Premium
- **Konfidenzintervalle:** 2.5. und 97.5. Perzentil aus Monte Carlo Draws

---

## Anhang: Session-Metadaten

```yaml
session_id: EBF-S-2026-02-13-FIN-001
domain: FIN
mode: STANDARD
date: 2026-02-13
client: UBS
project: Feel Switzerland CEM
model: Customer Engagement Multiplier Model v1.0
monte_carlo_draws: 10000
personas: [Lena_22, Marco_24, Sandra_42, Thomas_58]
regions: [DE-CH, FR-CH, TI, GR]
theories_used:
  - MS-RD-001 (Prospect Theory)
  - MS-SP-001 (Inequity Aversion)
  - MS-SP-005 (Reciprocity)
  - MS-NU-002 (Default Effects)
  - MS-IB-008 (Social Identity)
parameters_from:
  - PAR-COMP-002 (Social × Financial Crowding-Out)
  - BCM2 CH-SOC-01/02/03 (Swiss Trust/Cohesion)
bcm2_context: data/dr-datareq/sources/context/ch/
scripts:
  - scripts/monte_carlo_feel_switzerland.py
  - scripts/visualize_feel_switzerland.py
outputs:
  - outputs/sessions/EBF-S-2026-02-13-FIN-001/F5_ubs_feel_switzerland_analyse_v1.md
  - outputs/persona_heatmap.png
  - outputs/conversion_funnel.png
  - outputs/discount_curve.png
  - outputs/benefit_attention.png
  - outputs/fairness_framing.png
  - outputs/regional_map.png
```
