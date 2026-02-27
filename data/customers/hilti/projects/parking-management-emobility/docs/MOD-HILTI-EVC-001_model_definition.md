# MOD-HILTI-EVC-001: Hilti EV Charging Repark Model

**Model ID:** MOD-HILTI-EVC-001
**Version:** 1.0
**Created:** 2026-02-20
**Session:** EBF-S-2026-02-20-ORG-001
**Project:** PRJ-HILTI-001 (Parking Management E-Mobility)
**Client:** Hilti AG, HQ Schaan
**Status:** Theoretical (Pre-Survey) — Awaiting Bayesian Update via Survey

---

## 1. Gestaltungsanlass

Hilti HQ hat **100 Ladestationen** fuer **~400 potenzielle Nutzer** (Ratio 1:4). Aktuell ist das Laden gratis, was dazu fuehrt, dass Stationen den ganzen Tag blockiert werden. Es wird ein faires Pricing-Modell gesucht, das:

1. **Mitarbeiterakzeptanz** maximiert
2. **Blockierzeit** der Ladeinfrastruktur minimiert
3. **Positive Employer Perception** aufrechterhaelt

### Kernproblem: Tragedy of the Commons

- Preis = 0 → kein Signal zum Freiraeumen → Dauerblockierung
- Klassisches Commons Dilemma (Hardin 1968, Ostrom 1990)
- Loesung muss Preis-Signal + Soziale Norm + Infrastruktur kombinieren

---

## 2. Scope Definition

| Aspekt | Definition |
|--------|-----------|
| **Typ** | Continuous — taegliche Entscheidung |
| **Verhalten** | «Umparken nach Ladeschluss oder stehen lassen» |
| **Y(t)** | Binaer: 1 = umgeparkt, 0 = stehen gelassen |
| **Zeitachse** | Taeglich, mit Habit-Persistenz (λ = 0.40) |
| **Population** | ~400 EV-Fahrer am Hilti HQ Schaan |

---

## 3. Kontext-Spezifikation (Ψ)

### MACRO (Liechtenstein/DACH)

| Dimension | Label | Wert |
|-----------|-------|------|
| Ψ_K | DACH-Arbeitskultur | Fairness-orientiert, regelrespektierend |
| Ψ_I | Gratis-Default | Status Quo = kostenlos laden |
| Ψ_E | Einkommensniveau | Hoch (Hilti-Gehaelter) |

### MESO (Hilti AG)

| Dimension | Label | Wert |
|-----------|-------|------|
| Ψ_S_corp | Corporate Identity | Stark, nachhaltigkeitsorientiert (SBTi) |
| Ψ_M | Ladeinfrastruktur | AC 11kW (Mehrheit) + DC Schnelllader |
| Ψ_T_shift | Schichtarbeit | Teils Schichtbetrieb (Plant Schaan) |

### MICRO (Situation)

| Dimension | Label | Wert |
|-----------|-------|------|
| Ψ_F | Parkplatz-Distanz | Variable Distanzen, 5-15 Min Umpark-Aufwand |
| Ψ_C | Kognitive Last | Mittags-Rush, Meeting-Druck |
| Ψ_A_notif | Notification | Noch nicht implementiert (Gate-Variable) |
| Ψ_S_peer | Peer-Beobachtbarkeit | Kollegiale Sichtbarkeit im Parkhaus |

### Moderatoren (5 Stueck)

| Moderator | Wert | Wirkung |
|-----------|------|---------|
| Community-Survey-Effekt | +0.15 | Partizipation reduziert Reaktanz |
| Workplace-Kontext | +0.10 | Taegliche Sichtbarkeit staerkt Normen |
| Gratis→Paid Transition | -0.08 | Entitlement-Effekt (Endowment) |
| DACH Fairness-Norm | +0.12 | Kulturelle Fairness-Orientierung |
| High-Income | +0.09 | Geringere Preis-Elastizitaet |

---

## 4. Variablen und Komplementaritaet

### Utility-Dimensionen

| Symbol | Name | β | Unsicherheit | Quelle |
|--------|------|---|-------------|--------|
| C.F | Financial Cost | 0.60 | ±0.12 | LLMMC + WTP-Survey |
| C.P | Practical Cost | segment-spezifisch | ±0.15 | LLMMC + Hilti-Kontext |
| C.S | Social Norm | 0.35 | ±0.08 | LLMMC + Survey |
| C.X | Corporate Identity | 0.25 | ±0.10 | LLMMC |

### Segment-spezifische Aufwandskosten β_P(s)

| Segment | β_P | Begruendung |
|---------|-----|------------|
| S1: BEV Daily | 0.55 | Jeden Tag, Routine unterbrechen |
| S2: BEV Occasional | 0.40 | 2-3x/Woche, flexibler |
| S3: PHEV Micro | 0.25 | Kleine Ladungen, geringer Aufwand |
| S4: Shift Workers | 0.75 | Schicht-Unterbrechung, hohe Kosten |

### Gate-Variable

| Symbol | Name | Distribution | Ohne Notif. | Mit Notif. |
|--------|------|-------------|-------------|------------|
| A | Awareness | Beta(3,2) | 0.30 | 0.85 |

### Komplementaritaet (γ-Matrix)

| Paar | γ | Mechanismus | Quelle |
|------|---|------------|--------|
| C.F × C.S | **-0.30** [-0.45, -0.15] | Crowding-Out: Preis zerstoert Norm | PAR-COMP-002 (adj.) |
| C.S × C.X | **+0.20** [+0.10, +0.30] | Norm verstaerkt Corporate Identity | LLMMC |
| Infra × Compliance | **+0.70** [+0.50, +0.85] | Mehr Stationen verstaerken Signal | MOD-AWE-SG-MOB-001 |

---

## 5. Funktionale Form

### Gated Logistic mit Habit und Segment-Interaktion

```
P(repark_t | s, v) = 1 / (1 + exp(-ΔU_t))

ΔU_t = A · [β_F·p(v) + β_S·σ + β_X·ι + γ_FS·p·σ + γ_SX·σ·ι]
        - β_P(s)·τ(s)
        + λ·Y_{t-1}
        + ε
```

### Erweiterungen

| Extension | Formel | Zweck |
|-----------|--------|-------|
| F1: Logistic | σ(ΔU) = 1/(1+exp(-ΔU)) | Bounded [0,1] Wahrscheinlichkeitsraum |
| F2: Habit | + λ·Y_{t-1} | Verhaltenstraegheit, Konvergenz ~5 Wochen |
| F3: Segment | β_P(s)·τ(s) | Segment-spezifische Aufwandskosten |

### Dynamik

```
P_ss = lim_{t→∞} P(repark_t)

Konvergenz: τ_half ≈ 1.2 Wochen (λ=0.40)
95% Steady State: ~5 Wochen
```

---

## 6. Parameter-Vektor (vollstaendig)

| Parameter | Wert | Range | Tier | Quelle |
|-----------|------|-------|------|--------|
| β_F | 0.60 | [0.40, 0.80] | 2 (LLMMC) | Prior; Update via WTP-Frage |
| β_P(S1) | 0.55 | [0.40, 0.70] | 2 (LLMMC) | Hilti-Kontext: taegliche Pendler |
| β_P(S2) | 0.40 | [0.25, 0.55] | 2 (LLMMC) | Gelegentliche Nutzer |
| β_P(S3) | 0.25 | [0.15, 0.38] | 2 (LLMMC) | PHEV, geringer Aufwand |
| β_P(S4) | 0.75 | [0.55, 0.90] | 2 (LLMMC) | Schichtarbeiter, hoch |
| β_S | 0.35 | [0.20, 0.50] | 2 (LLMMC) | Survey-Diagnostik DIAG-3 |
| β_X | 0.25 | [0.12, 0.38] | 2 (LLMMC) | Survey-Diagnostik DIAG-4 |
| γ_FS | -0.30 | [-0.45, -0.15] | 1→2 | PAR-COMP-002 adj. |
| γ_SX | +0.20 | [+0.10, +0.30] | 2 (LLMMC) | Prior |
| γ_IC | +0.70 | [+0.50, +0.85] | 2→3 | MOD-AWE-SG-MOB-001 |
| λ | 0.40 | [0.25, 0.55] | 2 (LLMMC) | Habit-Literatur |
| A (ohne Notif.) | 0.30 | [0.15, 0.45] | 2 (LLMMC) | Gate-Variable |
| A (mit Notif.) | 0.85 | [0.70, 0.95] | 2 (LLMMC) | Gate-Variable |

**Provenance-Regel:** Alle Parameter sind Tier-2 LLMMC Priors. Bayesian Update geplant via Survey (Phase 1) und Pilot (Phase 2).

---

## 7. Predictions

### 7.1 Prediction Matrix: P(repark) nach Variante × Segment

|           | V1:Mengen | V2:Flat | V3:PPU | V4:Zeit | V5:Ausbau |
|-----------|-----------|---------|--------|---------|-----------|
| S1 BEV daily | 0.25 [.15,.35] | 0.10 [.05,.18] | 0.55 [.40,.68] | 0.40 [.28,.52] | 0.70 [.58,.80] |
| S2 BEV occ. | 0.35 [.22,.48] | 0.15 [.08,.25] | 0.45 [.30,.58] | 0.50 [.35,.62] | 0.65 [.52,.75] |
| S3 PHEV | 0.60 [.45,.72] | 0.05 [.02,.12] | 0.70 [.55,.82] | 0.55 [.40,.68] | 0.80 [.68,.88] |
| S4 Schicht | 0.10 [.04,.18] | 0.05 [.02,.10] | 0.20 [.10,.32] | 0.15 [.08,.25] | 0.55 [.40,.68] |
| **Gewichtet** | **0.30** | **0.09** | **0.48** | **0.40** | **0.68** |

### 7.2 Ranking (Comparative)

```
V5:Ausbau > V3:PPU > V4:Zeit > V1:Mengen >> V2:Flat
P(dieses Ranking korrekt) = 0.75 [0.60, 0.85]
```

### 7.3 Paarvergleiche

| Paar | P | Konfidenz |
|------|---|----------|
| V5 > V2 | 0.99 | Praktisch sicher |
| V5 > V3 | 0.81 | Sicher |
| V3 > V4 | 0.65 | Unsicher |
| V4 > V1 | 0.68 | Unsicher |

### 7.4 Gate-Effekt (Awareness)

- **Ohne Notification:** Alle P(repark) ÷3
- **Mit Notification:** +25pp Umpark-Rate [+15pp, +35pp]
- **Empfehlung:** Notification ist VORAUSSETZUNG fuer jede Variante

### 7.5 Crowding-Out (Gneezy-Effekt)

V2 (5 CHF Flat) liegt unter dem Gneezy-Threshold (~8-10 CHF):
- Status Quo (gratis, soziale Norm aktiv): P ≈ 0.15
- V2 (5 CHF, soziale Norm zerstoert): P ≈ 0.09 [-6pp]
- «A Fine is a Price» — 5 CHF legitimiert Blockieren

### 7.6 Habit-Dynamik

| Woche | P(repark) | % Steady State |
|-------|-----------|---------------|
| 1 | 0.25 | 52% |
| 2 | 0.35 | 73% |
| 4 | 0.45 | 94% |
| 8 | 0.48 | 100% |

### 7.7 Monte Carlo (1'000 Draws)

| Variante | 5%ile | Median | 95%ile |
|----------|-------|--------|--------|
| V1 | 0.12 | 0.30 | 0.50 |
| V2 | 0.02 | 0.09 | 0.22 |
| V3 | 0.28 | 0.48 | 0.68 |
| V4 | 0.20 | 0.40 | 0.60 |
| V5 | 0.45 | 0.68 | 0.85 |

**Variance Decomposition:**
- A (Awareness): 38%
- γ_FS (Crowding-Out): 24%
- β_P (Aufwand): 19%
- β_F (Preis): 12%
- Rest: 7%

### 7.8 Szenarien

| Szenario | Bedingungen | V5 P(repark) |
|----------|-------------|-------------|
| Best | A=0.90, γ=-0.15, σ=0.70 | 0.82 |
| Base | A=0.65, γ=-0.30, σ=0.50 | 0.68 |
| Worst | A=0.25, γ=-0.50, σ=0.20 | 0.42 |

**Key Insight:** Worst Case V5 (0.42) > Base Case V2 (0.09) → V5 ist robust.

---

## 8. Bayesian Update Plan

### Phase 1: Survey → Posterior

| Parameter | Survey-Frage | Update-Regel |
|-----------|-------------|-------------|
| A (Aware) | «Wissen Sie, wie lange Ihr Auto nach dem Laden steht?» | A_post = %_correct |
| β_F (WTP) | «Ab welchem Betrag wuerden Sie umparken?» | β_F_post = f(WTP) |
| γ_FS (C-O) | «Finden Sie [Variante] fair?» | %fair→ γ_FS adjustment |
| τ (Aufwand) | «Wie aufwaendig waere Umparken?» | τ_post per Segment |

### Phase 2: Pilot (Monat 1-2)

- 20 von 100 Stationen
- Messe: Blockierzeit, Umpark-Rate, Beschwerden
- Bayesian Update #2

### Phase 3: Rollout (Monat 3+)

- Alle 100 Stationen

### Phase 4: Review (Monat 6)

- KPI-1: Akzeptanz > 70%
- KPI-2: Blockierzeit ↓ 40%
- KPI-3: Employer Perception positiv

---

## 9. Entscheidungsbaum nach Survey

```
Survey-Ergebnis
    │
    ├── A > 0.50
    │   ├── γ_FS > -0.25   → V3 oder V5
    │   ├── γ_FS ∈ [-0.40,-0.25] → V5 bevorzugt
    │   └── γ_FS < -0.40   → NUR V5
    │
    └── A < 0.50
        └── ERST Notification-System aufbauen
            └── Dann erneut messen
```

---

## 10. Cross-References

| Typ | Referenz |
|-----|---------|
| Cross-Validation | MOD-AWE-SG-MOB-001 (Kt. St. Gallen Mobilitaet) |
| Parameter | PAR-COMP-002 (Crowding-Out γ = -0.68 generic) |
| Literature | Gneezy & Rustichini (2000), Frey & Jegen (2001) |
| Project | PRJ-HILTI-001 |
| Email Correspondence | ev_charging_email_correspondence.md |
| Mobility Strategy | mobility_strategy_project_overview.md |
| EEE Workflow | Appendix EEE (METHOD-DESIGN) |
| Awareness Theory | Appendix AU (CORE-AWARE) |
| Complementarity | Appendix B (CORE-HOW) |

---

*Generated via EEE Workflow (/design-model --mode standard), Steps 1-9*
*Session: EBF-S-2026-02-20-ORG-001*
*FehrAdvice & Partners AG*
