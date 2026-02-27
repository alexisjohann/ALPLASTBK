# Feel Switzerland Behavior Model (MOD-FSW-001)
## Journey Transition Model (JTM) v1.0

**Session:** EBF-S-2026-02-12-FIN-002
**Datum:** 2026-02-12
**Modus:** STANDARD
**Modell-ID:** MOD-FSW-001
**Kunde:** UBS AG (Key4 / Feel Switzerland)
**Erstellt von:** FehrAdvice & Partners AG

---

## Executive Summary

Das **Feel Switzerland Journey Transition Model (JTM)** ist ein 6-dimensionales Verhaltensmodell fuer das UBS Key4 Kulturprogramm «Feel Switzerland». Es formalisiert, wie Bankkunden verschiedener Segmente durch eine 7-phasige Journey navigieren — von der ersten Awareness ueber den Eligibility Gate bis zur Advocacy.

**Kernbefund:** Das Programm hat ein **Crowding-Out Problem**. Rabatt-zentrierte Kommunikation (u_FIN) untergaebt systematisch den Social- (u_SOC) und Belonging-Wert (u_BEL) des Programms. Ein Shift zu Experience-First Kommunikation kann die End-to-End Conversion um **+15-25%** steigern — bei gleichzeitiger Reduktion des Rabatt-Budgets um **-54%**.

**3 Quick Wins (CHF 0 Zusatzkosten):**
1. Gate Reward-Framing → +25-40% Gate-Passage-Rate
2. FOMO/Scarcity-Messaging → +8-18% Decision-Phase CR
3. Preis aus Email auf Landingpage verschieben → +10-15% Click-Rate

**14 testbare Vorhersagen** machen das Modell empirisch falsifizierbar.

---

## 1. Einleitung und Fragestellung

### Mandat

UBS bietet ueber das Key4-Programm exklusiven Zugang zu Schweizer Kulturerlebnissen (ZFF, Art Basel, Lucerne Festival, etc.). Die zentrale Frage:

> **Wie laesst sich das Engagement verschiedener Kundensegmente mit dem «Feel Switzerland» Kulturprogramm verhaltens-oekonomisch modellieren, um Conversion, Advocacy und Kundenbindung zu optimieren?**

### Warum ein Verhaltensmodell?

Traditionelle CRM-Ansaetze behandeln Kunden als rationale Agenten. Das EBF-Framework zeigt: Kulturkonsum ist intrinsisch motiviert — Rabatte koennen die intrinsische Motivation **zerstoeren** (Crowding-Out, Gneezy & Rustichini 2000). Ein Verhaltensmodell identifiziert die **richtigen Hebel** fuer jedes Segment und jede Journey-Phase.

---

## 2. Kontextanalyse (Step 1+3)

### 2.1 Dual-Kontext: Markt + Kunden

**Marktkontext (Ψ_Markt):**

| Dimension | Code | Wert | Beschreibung |
|-----------|------|------|-------------|
| Kulturelle Dichte | Ψ_K* | 0.85 | Schweiz: Hoehere Kulturaffinitaet als DACH-Durchschnitt |
| Wettbewerb | Ψ_COMP | 0.35 | CS/Swisscard/ZKB bieten aehnliche Programme |
| Saisonalitaet | Ψ_T* | 0.70-1.30 | Starke saisonale Schwankungen (Art Basel Jun, ZFF Sep) |
| Digital/Physisch | Ψ_F* | 0.65 | Hybride Journey (Digital Awareness → Physisch Event) |

**Kundenkontext (Ψ_Kunde):**

| Dimension | Code | Wert | Beschreibung |
|-----------|------|------|-------------|
| Institutionell | Ψ_I | 0.75 | UBS-Rahmen: Eligibility, Compliance, Regulierung |
| Sozial | Ψ_S* | 0.60-0.90 | Social Signaling variiert stark nach Segment |
| Kognitiv | Ψ_C | 0.70 | Entscheidung unter Zeitdruck (Event-Deadlines) |
| Oekonomisch | Ψ_E* | 0.80 | Affluent-Segment: Preis ist NICHT der Haupttreiber |

### 2.2 Erweiterungen (K1+K2+K3)

- **K1: Ψ_EMO (Emotionaler Kontext):** FOMO, Anticipation, Social Buzz als Amplifier
- **K2: Ψ_COMP (Wettbewerb):** Dynamischer Wettbewerbsdruck erhoeht Transitions-Schwellen
- **K3: Ψ_T* (Saisonalitaet):** Event-Kalender als Multiplikator (Art Basel +30%, ZFF +25%)

---

## 3. Modellspezifikation (Step 2+4+5)

### 3.1 Scope: Journey-Zentrierter Prozess

```
AWARENESS → INTEREST → [GATE] → EVALUATION → DECISION → ACTION → ADVOCACY
                         ↑
                    Nur Adult Prospect
                    (Fairness-sensitiv!)
```

**7 Phasen, 4 Segmente, 6 Utility-Dimensionen, 3 Gleichungen.**

### 3.2 Segmente (SUB-1 bis SUB-4)

| Segment | Beschreibung | Gate | Primaertreiber |
|---------|-------------|------|----------------|
| **SUB-1: Super Rich** | UHNW, UBS Top-Tier | Kein Gate | U_IDN, U_ACC, U_BEL |
| **SUB-2: Adult Qualified** | WM-Kunden, Key4-berechtigt | Kein Gate | U_EXP, U_BEL, U_SOC |
| **SUB-3: Adult Prospect** | Noch nicht qualifiziert | **GATE** (Fairness!) | U_FIN im Gate, sonst U_EXP |
| **SUB-4: Youth** | Digital Natives, Nachwuchs | Kein Gate | U_EXP, U_SOC, U_ACC |

### 3.3 Der 6D Utility-Vektor (V1: +Belonging)

| Symbol | Dimension | Beschreibung | Constraint |
|--------|-----------|-------------|------------|
| U_IDN | Identity | «Ich bin ein Kulturmensch» | - |
| U_BEL | Belonging | «Ich gehoere zur UBS-Welt» | NEU (V1) |
| U_EXP | Experience | «Das Erlebnis bereichert mich» | - |
| U_SOC | Social | «Andere sehen, dass ich dabei war» | - |
| U_ACC | Access | «Ich komme rein, andere nicht» | - |
| U_FIN | Financial | «Es kostet weniger» | **CONSTRAINED** — nur Hygiene! |

### 3.4 Asymmetrische γ-Matrix (V2)

Leserichtung: γ(Zeile → Spalte) = «Wie stark beeinflusst ZEILE die Wirkung von SPALTE?»

| γ(→) | U_IDN | U_BEL | U_EXP | U_SOC | U_ACC | U_FIN |
|------|-------|-------|-------|-------|-------|-------|
| U_IDN | · | +0.45 | +0.40 | +0.30 | +0.25 | -0.25 |
| U_BEL | +0.35 | · | +0.30 | +0.50 | +0.40 | -0.20 |
| U_EXP | +0.30 | +0.25 | · | +0.45 | +0.50 | -0.15 |
| U_SOC | +0.25 | +0.40 | +0.35 | · | +0.30 | -0.50 |
| U_ACC | +0.20 | +0.35 | +0.55 | +0.25 | · | +0.20 |
| U_FIN | -0.30 | -0.35 | -0.10 | -0.40 | +0.15 | · |

**Zentrale Asymmetrien:**
- γ(SOC→FIN) = -0.50 vs γ(FIN→SOC) = -0.40 → Social leidet MEHR unter Rabatt
- γ(BEL→SOC) = +0.50 vs γ(SOC→BEL) = +0.40 → Community verstaerkt Signaling staerker
- γ(ACC→EXP) = +0.55 vs γ(EXP→ACC) = +0.50 → Access ist kausal fuer Experience

### 3.5 Dynamische Gewichte nach Journey-Phase (V3)

| Phase | U_IDN | U_BEL | U_EXP | U_SOC | U_ACC | U_FIN | Dominant |
|-------|-------|-------|-------|-------|-------|-------|----------|
| AWARENESS | 0.10 | 0.10 | 0.40 | 0.15 | 0.20 | 0.05 | EXP+ACC |
| INTEREST | 0.25 | 0.20 | 0.25 | 0.15 | 0.10 | 0.05 | IDN+BEL |
| GATE | 0.10 | 0.10 | 0.10 | 0.05 | 0.30 | 0.35 | ACC+FIN |
| EVALUATION | 0.20 | 0.15 | 0.30 | 0.10 | 0.20 | 0.05 | EXP+ACC |
| DECISION | 0.20 | 0.15 | 0.20 | 0.10 | 0.15 | 0.20 | Balanciert |
| ACTION | 0.10 | 0.10 | 0.15 | 0.10 | 0.45 | 0.10 | ACC |
| ADVOCACY | 0.25 | 0.30 | 0.15 | 0.25 | 0.05 | 0.00 | BEL+IDN |

**Insight:** U_FIN ist nur in 2 von 7 Phasen relevant (29%). Rabatt-Kommunikation adressiert weniger als ein Drittel der Journey.

---

## 4. Funktionale Form: Journey Transition Model (JTM)

### Gleichung 1: Phase-Utility

```
U_φ(s, Ψ, t) = Σᵢ wᵢ(φ,s) · uᵢ · Ψ_mod(i) · Ψ_T*(t) · [1 + εᵢ(Ψ_EMO)]
              + Σᵢ<ⱼ [γ(i→j)·uᵢ + γ(j→i)·uⱼ] · √(uᵢ·uⱼ)
              − φ_crowd(φ) · 𝟙(u_FIN > θ_crowd) · u_FIN · Σₖ≠FIN |γ(FIN→k)|·uₖ
```

**Term 1:** Gewichtete Basis-Utilities mit Kontext, Saisonalitaet und Emotion
**Term 2:** Asymmetrische Komplementaritaeten (Synergien und Crowding-Out)
**Term 3:** Crowding-Out Penalty (aktiviert wenn FIN > 40% der Gesamt-Utility)

### Gleichung 2: Phase-Transition

```
P(φ → φ+1 | s, Ψ) = σ(α_s · U_φ(s,Ψ,t) − τ_φ(s) · [1 + Ψ_COMP])
```

**Spezialfall Eligibility Gate (Adult Prospect):**
```
P(INT→EVAL | prospect) = σ(α · U_GATE − τ_GATE · [1+Ψ_COMP]) × F(Ψ_I, α_FS, β_FS)

F(Ψ_I, α_FS, β_FS) = 1 − α_FS · max(0, c_perceived − c_reference)
                      + β_FS · max(0, b_perceived − b_reference)
```

### Gleichung 3: Advocacy Feedback Loop

```
Ψ_S*(t+1) = Ψ_S*(t) + ρ · Σₛ P(ADV|s) · N_s · quality_signal(s)
```

**Quality Signal:** Super Rich (1.0) > Adult Qual (0.8) > Adult Prosp (0.6) > Youth (0.3)

### Erweiterungen (F1+F2+F3)

- **F1 Saisonalitaet:** Ψ_T*(t) = sinusoidale Basislinie + Event-Boosts (Art Basel +0.30, ZFF +0.25)
- **F2 Wettbewerb:** τ × (1 + Ψ_COMP) — hoehere Schwellen bei aktivem Wettbewerb
- **F3 Emotionale Amplifier:** ε_FOMO (0.40), ε_ANTIC (0.25), ε_BUZZ (0.30) — verstaerken U_ACC, U_EXP, U_SOC

---

## 5. Parametrisierung (Step 6)

### Strategie: Hybrid Bayesian (LLMMC Prior + UBS-Daten)

| Tier | Parameter | Anzahl | Unsicherheit |
|------|-----------|--------|--------------|
| **1 Literatur** | γ-Matrix, Fairness, Crowding-Out | ~45 | Low |
| **2 LLMMC** | ε-Amplifier, Ψ_mod, quality_signal | ~50 | Medium |
| **3 Empirisch** | τ-Schwellen, w-Gewichte, Ψ_T*, Ψ_COMP | ~60 | Variabel |
| **Total** | | **~155** | |

### Top 10 Parameter fuer Prioritaets-Kalibrierung

| Rang | Parameter | Prior | Impact (Δ CR) |
|------|-----------|-------|---------------|
| #1 | τ_GATE(prospect) | 0.65 ± 0.15 | ±18% |
| #2 | γ(FIN→SOC) | -0.50 ± 0.15 | ±12% |
| #3 | θ_crowd | 0.40 ± 0.10 | ±11% |
| #4 | w_EXP(AWARENESS) | 0.40 ± 0.10 | ±9% |
| #5 | α_FS | 0.85 ± 0.20 | ±8% |
| #6 | ε_FOMO | 0.40 ± 0.15 | ±7% |
| #7 | ρ (Diffusion) | 0.05 ± 0.02 | ±6% |
| #8 | Ψ_T*(Jun) | 1.30 ± 0.15 | ±5% |
| #9 | γ(BEL→SOC) | +0.50 ± 0.12 | ±5% |
| #10 | w_FIN(GATE) | 0.35 ± 0.10 | ±4% |

### Minimale UBS-Daten fuer Version 2.0

| Prioritaet | Daten | Kalibriert |
|-----------|-------|------------|
| **A (MUSS)** | D1: Conversion Funnel (7×4 Tabelle) | τ, α |
| **A (MUSS)** | D2: Gate-Passage-Daten | τ_GATE, α_FS |
| **A (MUSS)** | D3: Post-Event NPS/CSAT | w-Gewichte |
| B (SOLL) | D4: Monatliche Buchungen | Ψ_T* |
| B (SOLL) | D5: Referral/Advocacy Daten | ρ |
| C (KANN) | D7: Conjoint Experiment | w, γ simultan |

---

## 6. Testbare Vorhersagen (Step 7)

### 14 Vorhersagen in 3 Typen

#### Point Predictions (PP)

| ID | Vorhersage | Konfidenz |
|----|-----------|-----------|
| PP-1 | Experience-First erhoeht E2E Conversion um +15-25% | MEDIUM |
| PP-2 | Reward Frame am Gate: +25-40% Passage-Rate | HIGH |
| PP-3 | FIN > 40% Kommunikation: U_SOC sinkt um -35% | HIGH |
| PP-4 | Event-Monate (Jun/Sep) +25-35% vs ruhige Monate | MEDIUM |

#### Interval Predictions (IP, Version 2.0+)

| ID | Vorhersage | 68% CI |
|----|-----------|--------|
| IP-1 | Advocacy: Super Rich 0.35, Youth 0.08 | [0.22-0.48], [0.02-0.14] |
| IP-2 | Flywheel: Ψ_S* +0.12 nach 12 Monaten | [0.08, 0.15] |
| IP-3 | FOMO erhoeht Decision-CR um +8-18% | [0.08, 0.18] |

#### Comparative Predictions (CP, sofort testbar)

| ID | Vorhersage | Falsifiziert wenn |
|----|-----------|-------------------|
| CP-1 | CR: SuperRich > AdultQual > AdultProsp > Youth | Youth > AdultQual |
| CP-2 | CR(EXP Frame) > CR(Discount Frame) in ≥5/7 Phasen | Discount ≥3 Phasen |
| CP-3 | Advocacy(mit Community) > ohne × 1.3 | Differenz < 10% |
| CP-4 | Advocacy-Impact: SuperRich/Youth > 2.5 | Ratio < 1.5 |
| CP-5 | CR: Jun > Dez > Feb | Feb > Jun |
| CP-6 | Gate: Reward Frame > Barrier Frame × 1.25 | Differenz < 10% |
| CP-7 | ε_FOMO: AdultQual > SuperRich | SuperRich > AdultQual |

**Kritischster Test:** CP-2 — wenn Discount in ≥3 Phasen gewinnt, fundamentale Modellrevision noetig.

---

## 7. A/B-Test Designs

### Test 1: Gate Framing (CP-6) — Hoechste Prioritaet

- **Control:** Barrier Frame — «Um Key4 Benefits zu nutzen, muessen folgende Voraussetzungen erfuellt sein...»
- **Treatment:** Reward Frame — «Als geschaetzter UBS-Kunde haben Sie sich Zugang verdient. Ihr Profil zeigt: [✓]. Naechster Schritt: [1 Aktion]»
- **n:** ~800 Adult Prospects (400 pro Arm)
- **Laufzeit:** 6-8 Wochen
- **Kosten:** ~CHF 0 (nur Textaenderung)

### Test 2: Experience vs Discount (CP-2) — Kernhypothese

- **Control:** Discount-First — «30% Rabatt auf ZFF-Tickets»
- **Treatment A:** Experience-First — «Exklusiver Filmabend mit Regisseur:in am ZFF»
- **Treatment B:** Belonging-First — «Als Teil des UBS Kulturkreises: Ihr ZFF-Erlebnis»
- **n:** ~8'400 (2'800 pro Arm, stratifiziert nach Segment)
- **Laufzeit:** 2-3 Monate
- **Kosten:** ~CHF 40k

---

## 8. ROI-Vorhersage

### 12-Monats-Vergleich (20'000 Key4-Kunden)

| Metrik | Status Quo | Experience-First | Delta |
|--------|-----------|-----------------|-------|
| Aktive Nutzer | 1'600 | 2'200 | **+37%** |
| Advocacy/Empfehlungen | 160 | 484 | **+203%** |
| Gesamtkosten | CHF 422k | CHF 448k | +6% |
| Cost per Active User | CHF 264 | CHF 204 | **-23%** |
| Rabatt-Budget | CHF 192k | CHF 88k | **-54%** |

### 3-Jahres-Kumulativ (Flywheel-Effekt)

| Jahr | Status Quo (kumulativ) | EXP-First (kumulativ) | Delta |
|------|----------------------|----------------------|-------|
| 1 | 1'600 | 2'200 | +600 |
| 2 | 3'200 | 4'600 | +1'400 |
| 3 | 4'800 | 7'350 | **+2'550 (+53%)** |

**Flywheel-Mechanismus:** Advocacy erzeugt Social Proof → mehr Awareness → mehr Nutzer → mehr Advocacy → ...

---

## 9. Implementierungs-Roadmap

| Phase | Zeitraum | Aktionen | Erwarteter Effekt |
|-------|----------|----------|-------------------|
| **1 Quick Wins** | Monat 0-3 | Gate Framing, FOMO, EXP-first Emails | +25-40% Gate-CR, CHF 0 |
| **2 Komm.-Shift** | Monat 3-12 | 3-Arm A/B-Test, Rabatt-Reduktion | +15-25% E2E CR |
| **3 Community** | Monat 6-18 | UBS Kulturkreis, Top-Down Seeding | Advocacy +120% |
| **4 Optimierung** | Monat 18-36 | Modell v3.0, saisonale Optimierung | Flywheel selbsttragend |

**Erster messbarer ROI:** Monat 2 (Gate Framing A/B-Test)
**Kernhypothese bestaetigt/falsifiziert:** Monat 5 (CP-2 A/B-Test)
**Flywheel sichtbar:** Monat 12-15 (organisches Wachstum)

---

## 10. Modell-Versionen

| Version | Basis | Parameter-Quelle | Validierung |
|---------|-------|-------------------|-------------|
| **v1.0** (aktuell) | LLMMC | Tier 1+2 | Face + Comparative + Stress |
| v2.0 (Monat 6) | +UBS CRM | +Tier 3 (D1-D3) | +Holdout Validation |
| v3.0 (Monat 18) | +Temporal | +Tier 3 (D4-D6) | +Temporal Prediction |
| v4.0 (Monat 36) | +Conjoint | +Tier 3 (D7-D8) | Full Calibration |

---

## Anhang: Theoretische Fundierung

| Theorie | ID | Beitrag zum Modell |
|---------|----|--------------------|
| Identity Economics | MS-IB-001 | U_IDN, Identitaets-Utility |
| Social Identity | MS-IB-006 | U_BEL, Gruppenzugehoerigkeit |
| Prospect Theory | MS-RD-001 | U_FIN, Loss Aversion am Gate |
| Inequity Aversion | MS-SP-001 | F(·), Fairness-Funktion |
| Mental Accounting | MS-RD-005 | U_EXP, Experience Framing |
| Social Proof | MS-IF-008 | Ψ_S*, Advocacy Feedback |
| Crowding-Out | PAR-COMP-002 | γ(FIN→SOC), γ(FIN→BEL) |
| Reactance + Scarcity | PAR-COMP-NEW | γ(ACC→EXP), ε_FOMO |

---

*Modell: MOD-FSW-001 v1.0 | Session: EBF-S-2026-02-12-FIN-002 | FehrAdvice & Partners AG*
