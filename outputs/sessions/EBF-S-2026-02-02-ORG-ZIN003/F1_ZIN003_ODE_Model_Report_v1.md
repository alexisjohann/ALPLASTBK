# ZIN003 Kreislaufwirtschaft - Behavioral Dynamics Model

**Session:** EBF-S-2026-02-02-ORG-ZIN003
**Kunde:** Zindel United
**Projekt:** ZIN003 - Kreislaufwirtschaft Verhaltensänderung
**CVA-Stufe:** VERTIEFT (983 Kontextfaktoren)
**Model ID:** MOD-ZIN-001
**Version:** 1.0
**Erstellt:** 2026-02-02

---

## Executive Summary

Dieses Dokument beschreibt das vollständige verhaltensökonomische Modell für das ZIN003 Kreislaufwirtschaft-Projekt bei Zindel United. Das Modell basiert auf:

- **983 Kontextfaktoren** aus 7 VERTIEFT-Level Kontextvektoren
- **40 Parameter** via LLMMC + Bayesian Update kalibriert
- **5-Variablen ODE-System** für Prozessdynamik
- **6 FEPSDE Utility-Dimensionen** mit Komplementaritäten
- **4 Szenarien** mit quantitativen Vorhersagen

**Kern-Erkenntnis:** Das Modell identifiziert einen kritischen **CROWDING-OUT Effekt** (γ_FS = -0.15): Finanzielle Anreize dürfen **ERST ab Monat 6** eingesetzt werden, sonst gefährden sie die sozialen Dynamiken.

---

## 1. Modell-Architektur

### 1.1 Funktionale Form: ODE-System

Das Modell verwendet ein gekoppeltes System gewöhnlicher Differentialgleichungen (ODE) mit 5 Zustandsvariablen:

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ZUSTANDSVARIABLEN                                                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  U(t)  Total Utility        │ Aggregierte Nutzen-Wahrnehmung            │
│  A(t)  Adoption             │ Anteil mit neuem Verhalten (S-Kurve)      │
│  R(t)  Resistance           │ Widerstand gegen Veränderung              │
│  H(t)  Habit Strength       │ Automatisierungsgrad                      │
│  M(t)  Momentum             │ Organisationale Dynamik                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Gleichungssystem

```
dU/dt = Σ_d α_d · (1 + I + γ_boost) · (1 - R) · (1 + H) - Σ_d δ_d · U_d

dA/dt = β · (U + I_total) · A · (1 - A) · (1 - 0.3·R) · (1 + M)

dR/dt = -ρ · evidence · R + r · setback · (1 - R)

dH/dt = η · A · (1 + I_D · 0.5) · (1 - H)

dM/dt = μ · success · (1 - M) - friction · M
```

---

## 2. FEPSDE Utility-Dimensionen

### 2.1 Parameter-Übersicht

| Dimension | Symbol | α (Growth) | δ (Decay) | Kontext-Adjustment |
|-----------|--------|------------|-----------|---------------------|
| **Financial** | U_F | 0.10 | 0.03 | +0.02 (ROI 6.2% in CH CE) |
| **Emotional** | U_E | 0.15 | 0.08 | +0.03 (Familienunternehmen) |
| **Physical** | U_P | 0.04 | 0.02 | -0.01 (Baubranche = physisch) |
| **Social** | U_S | 0.15 | 0.06 | +0.05 (9-köpfiges Kernteam) |
| **Development** | U_D | 0.10 | 0.04 | +0.02 (Innovationskultur) |
| **Existential** | U_X | 0.10 | 0.02 | +0.04 (8. Generation) |

### 2.2 Zindel-spezifische Erkenntnisse

**Stärken (hohe Growth Rates):**
- **Social (α_S = 0.15):** Starke Teamkultur, 9-köpfiges Kernteam
- **Emotional (α_E = 0.15):** Familienunternehmen, hohe Identifikation
- **Existential (α_X = 0.10):** 8. Generation, «Zukunft bauen» Narrativ

**Herausforderungen:**
- **Physical (α_P = 0.04):** Baubranche ist physisch anspruchsvoll, neue Prozesse erfordern zunächst mehr Aufwand

---

## 3. Komplementaritäts-Matrix

### 3.1 Positive Verstärkungen

| Paar | γ_ij | Interpretation |
|------|------|----------------|
| **Social × Existential** | +0.35 | Team-Erleben verstärkt Sinn-Erleben |
| **Development × Existential** | +0.40 | Lernen verstärkt Purpose |
| **Emotional × Development** | +0.30 | Positive Emotionen fördern Lernbereitschaft |
| **Social × Development** | +0.25 | Team-Lernen verstärkt sich gegenseitig |
| **Financial × Physical** | +0.20 | Kostenersparnis motiviert Aufwandsreduktion |

### 3.2 KRITISCHE WARNUNG: Crowding-Out

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ⚠️  CROWDING-OUT EFFEKT                                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  γ(Financial, Social) = -0.15                                           │
│                                                                         │
│  → Zu starker Geld-Fokus UNTERGRÄBT soziale Dynamiken!                 │
│  → Finanzielle Anreize ERST AB MONAT 6 einsetzen!                      │
│  → Quelle: Frey & Jegen (2001), Motivation Crowding Theory             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Prozess-Parameter

### 4.1 Adoption Dynamics

| Parameter | Wert | 95% CI | Interpretation |
|-----------|------|--------|----------------|
| **β_adoption** | 0.50 | [0.35, 0.65] | Moderate-schnelle Adoption (CEO-Sponsorship) |
| **ρ_resistance_decay** | 0.04 | [0.02, 0.06] | Widerstand baut langsam ab |
| **r_setback_sensitivity** | 0.15 | [0.10, 0.20] | Sensitivität für Rückschläge |
| **η_habit_formation** | 0.015/Tag | [0.01, 0.02] | 66 Tage zur Gewohnheit (Lally et al.) |
| **μ_momentum** | 0.08 | [0.05, 0.11] | Momentum baut bei Erfolgen auf |
| **friction** | 0.05 | [0.03, 0.07] | Natürlicher Momentum-Decay |

### 4.2 Phase Thresholds

| Phase | Threshold | Erwarteter Zeitpunkt |
|-------|-----------|----------------------|
| **Kick-off → Umsetzung** | Readiness > 0.25 | Ende Monat 2 (März 2026) |
| **Umsetzung → Stabilisierung** | Readiness > 0.55 | Ende Monat 5 (Juli 2026) |
| **Stabilisierung → Transfer** | Readiness > 0.80 | Ende Monat 7 (September 2026) |

---

## 5. Kontext-Elastizitäten (Ψ-Amplifikation)

| Ψ-Dimension | Elastizität | Zindel-spezifisch |
|-------------|-------------|-------------------|
| **Ψ_S (Social)** | 1.20 | Teamkultur sehr stark |
| **Ψ_K (Cultural)** | 1.10 | 8. Generation, starke Werte |
| **Ψ_T (Temporal)** | 0.90 | - |
| **Ψ_M (Material)** | 0.85 | TABREC, Logbau Infrastruktur |
| **Ψ_I (Institutional)** | 0.80 | - |
| **Ψ_F (Physical)** | 0.75 | Baustelle |
| **Ψ_E (Economic)** | 0.70 | - |
| **Ψ_C (Cognitive)** | 0.60 | Kognitive Last reduziert Effektivität |

---

## 6. Szenarien & Vorhersagen

### 6.1 Szenario-Übersicht

```
┌─────────────────────────────────────────────────────────────────────────┐
│  SZENARIO-PROGNOSEN                                                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  🟢 Szenario 1: "Der Beweis ist da"     P = 50-60%                     │
│     → Adoption: 100% | Stage: 4 (Transfer) | Alle Erfolge treten ein   │
│                                                                         │
│  🟡 Szenario 2: "Fast geschafft"        P = 25-30%                     │
│     → Adoption: 99.5% | Stage: 4 (Transfer) | Kleinere Rückschläge     │
│                                                                         │
│  🟠 Szenario 3: "Technisch ok"          P = 10-15%                     │
│     → Adoption: 52.3% | Stage: 2 (Umsetzung) | Kein Momentum           │
│                                                                         │
│  🔴 Szenario 4: "Kein Nutzen"           P = 5-10%                      │
│     → Adoption: 21.6% | Stage: 1 (Kick-off) | Starke Widerstände       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 6.2 Frühindikatoren

**Monat 2:**
- [ ] CU-Piloten starten → Signal: Readiness > 0.25
- [ ] Erste Quick Wins dokumentiert → Signal: Momentum steigt

**Monat 3:**
- [ ] Team-Engagement in Retrospektiven → Signal: Adoption > 0.15
- [ ] Widerstand sinkt sichtbar → Signal: Resistance < 0.5

**Monat 5:**
- [ ] ≥2 Piloten zeigen messbaren Nutzen → Signal: Adoption > 0.40
- [ ] Routine erkennbar → Signal: Habit > 0.3

---

## 7. Optimale Interventions-Sequenz

### 7.1 Zeitplan

```
┌─────────────────────────────────────────────────────────────────────────┐
│  INTERVENTIONS-TIMING                                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  MONAT 1-2:  Social (I_S = 0.3) + Development (I_D = 0.3)              │
│              → Teambuilding, Training, Workshops                        │
│              → KEINE finanziellen Anreize!                              │
│                                                                         │
│  MONAT 3-5:  Social erhöhen (I_S = 0.4) + Development reduzieren       │
│              → Peer Recognition, Success Stories                        │
│              → Training wird weniger intensiv                           │
│                                                                         │
│  MONAT 6+:   Financial einführen (I_F = 0.1) + Social reduzieren       │
│              → Jetzt sind Boni/Incentives erlaubt                       │
│              → Social-Basis ist gefestigt                               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 7.2 Begründung

1. **Monate 1-2:** Social und Development zuerst, weil:
   - γ(S,X) = +0.35 und γ(D,X) = +0.40 sind die stärksten Verstärker
   - Familienunternehmen-Identität wird aktiviert
   - Team-Kohäsion wird aufgebaut

2. **Monat 6+:** Financial erst später, weil:
   - γ(F,S) = -0.15 würde frühe Social-Gains zerstören
   - Nach 6 Monaten ist Habit bereits bei H > 0.3 (automatisiert)
   - Intrinsische Motivation ist gefestigt

---

## 8. KPI-Mapping

| Modell-Variable | KPI | Messmethode |
|-----------------|-----|-------------|
| **Adoption** | % Mitarbeiter mit regelmässiger CU-Praxis | Beobachtung, Tracking |
| **Resistance** | «Wie skeptisch bist du?» (invertiert) | Umfrage (1-5 Skala) |
| **Habit** | Automatisierungsgrad (ohne Reminder) | Verhaltens-Audit |
| **Momentum** | # positive Stories im Intranet/Monat | Content-Analyse |
| **Stage** | Phase gemäss Projektplan | Meilenstein-Tracking |

---

## 9. Theoretische Basis

### 9.1 Primäre Theorien

| Theory ID | Name | Autoren | Relevanz |
|-----------|------|---------|----------|
| MS-SP-001 | Inequity Aversion | Fehr, Schmidt (1999) | Teamdynamik, faire Verteilung |
| MS-IN-005 | Motivation Crowding | Frey, Jegen (2001) | **CROWDING-OUT Warnung** |
| MS-NU-002 | Habit Formation | Lally et al. (2010) | 66 Tage zur Automatisierung |

### 9.2 Sekundäre Theorien

| Theory ID | Name | Autoren | Relevanz |
|-----------|------|---------|----------|
| MS-IB-001 | Identity Economics | Akerlof, Kranton (2000) | Familienunternehmen-Identität |
| MS-IF-001 | Diffusion of Innovations | Rogers (2003) | S-Curve Adoption |
| MS-SP-004 | Self-Determination Theory | Deci, Ryan (2000) | Intrinsische Motivation |

---

## 10. Datenquellen

### 10.1 Kontextvektoren (983 Faktoren)

| Datei | Faktoren | Beschreibung |
|-------|----------|--------------|
| CV_ZIN003_01_unternehmen.yaml | 150 | Zindel United Profil |
| CV_ZIN003_02_branchen_ch.yaml | 150 | Schweizer Baubranche |
| CV_ZIN003_03_kreislaufwirtschaft.yaml | 183 | Circular Economy Studien |
| CV_ZIN003_04_branchen_global.yaml | 160 | Globale Baubranche |
| CV_ZIN003_05_wettbewerber_ch.yaml | 120 | CH Wettbewerber |
| CV_ZIN003_06_wettbewerber_global.yaml | 100 | Globale Wettbewerber |
| CV_ZIN003_07_graubuenden_regional.yaml | 120 | Regionales Profil GR |

### 10.2 Parameter-Datei

- **ZIN003_ODE_parameters.yaml** - Vollständige Parameter mit Priors, Posteriors, CIs

---

## 11. Nächste Schritte

1. **Interventions-Design** via `/design-intervention`
   - 20-Field Schema für jede geplante Massnahme
   - Crowding-Out Checks einbauen

2. **Monitoring Dashboard** erstellen
   - KPI-Tracking gemäss Mapping
   - Frühindikatoren-Ampel

3. **Monte Carlo Simulation** (optional)
   - 10'000 Draws für Konfidenzintervalle
   - Sensitivitätsanalyse

4. **Review nach Monat 3**
   - Parameter-Update mit realen Daten
   - Modell-Rekalibrierung falls nötig

---

## Anhang A: Model Registry Eintrag

```yaml
id: MOD-ZIN-001
name: Kreislaufwirtschaft Behavior Dynamics ODE Model
version: '1.0'
created: '2026-02-02'
customer: Zindel United
project: ZIN003
context_factors_used: 983
cva_level: VERTIEFT
functional_form:
  type: ode_system
  state_variables: [U, A, R, H, M]
validation:
  status: initial
  simulation_runs: 4
```

---

## Anhang B: Session-Details

| Feld | Wert |
|------|------|
| Session-ID | EBF-S-2026-02-02-ORG-ZIN003 |
| Modus | STANDARD |
| Entry Point | HYBRID (Theory informiert, Praxis führt) |
| Scope | PROCESS (Verhaltensänderung über Zeit) |
| Kontext (Ψ) | VOLLSTÄNDIG (8 Dimensionen) |
| Utility | VOLLSTÄNDIG (6 FEPSDE) |
| Funktionale Form | ODE System |
| Parameter-Methode | LLMMC + Bayesian Update |

---

*Generiert durch EBF Framework | Version 1.22 | Session EBF-S-2026-02-02-ORG-ZIN003*

*https://claude.ai/code/session_01YJpceUwc7Nbq6AmmcxjqXu*
