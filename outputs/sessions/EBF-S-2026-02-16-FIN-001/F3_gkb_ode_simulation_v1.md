# GKB001 ODE Simulation: Digital Transformation & Customer Deepening Behavior Dynamics

> **Session:** EBF-S-2026-02-16-FIN-001
> **Modell:** GKB001-ODE-v1.0
> **Datum:** 2026-02-16
> **Provenance:** Layer 1 (susceptibility = 0.0)
> **Methode:** Euler-Integration, dt=0.1, 12 Monate

---

## Projekt-Kontext

| Merkmal | Wert |
|---------|------|
| **Kunde** | Graubuendner Kantonalbank (GKB) |
| **CEO** | Daniel Fust (seit 2019) |
| **Bankpraesident** | Peter Fanconi (seit 2014) |
| **Groesse** | ~1'000 MA, 45 Filialen, CHF 76.1 Mrd. Geschaeftsvolumen |
| **Rating** | AA (S&P), Staatsgarantie |
| **Strategie** | Hybrid (Digital + Personal): «Ihre Verbundenheit. Unsere Kompetenz.» |
| **Kernmarkt** | Graubuenden: 45% Hypothekarmarktanteil, Tourismusfinanzierung |
| **Herausforderungen** | Zinsabhaengigkeit (67.5%), Margendruck, Neobanken, Digitalisierung |
| **Kontextfaktoren** | 350 (CVA + Strategy Context) |
| **Literaturquellen** | 10 |

---

## Parameter-Uebersicht

### Utility-Wachstumsraten (alpha)

| Dimension | Symbol | Wert | Prior | Adjustment | Interpretation |
|-----------|--------|------|-------|------------|----------------|
| Financial | alpha_F | **0.08** | 0.06 | +0.02 | Kommissionsgeschaeft-Diversifikation + Gioia-Oekosystem |
| Emotional | alpha_E | **0.16** | 0.14 | +0.02 | 156 Jahre Tradition, Buendner Identitaet, Stolz=0.85 |
| Physical | alpha_P | **0.05** | 0.05 | +0.00 | Moderate Digitalisierung, Automation=0.55, Cloud=0.45 |
| Social | alpha_S | **0.12** | 0.10 | +0.02 | Clan-Kultur, 12J Tenure, Zusammenarbeit=0.75 |
| Development | alpha_D | **0.11** | 0.10 | +0.01 | Dig.Kompetenz=0.65, Innovationskultur=0.55 |
| Existential | alpha_X | **0.09** | 0.06 | +0.03 | Kantonalbank-Mandat, Regionalentwicklung, 156 Jahre |

### Utility-Zerfallsraten (delta)

| Dimension | Symbol | Wert | Interpretation |
|-----------|--------|------|----------------|
| Financial | delta_F | 0.04 | Staatsgarantie puffert Rueckschlaege |
| Emotional | delta_E | 0.09 | Identitaetsbasiert — langsamer als reine Emotion |
| Physical | delta_P | 0.03 | Digitale Banking-Workflows persistent |
| Social | delta_S | 0.05 | Geringe Fluktuation (6%) stabilisiert |
| Development | delta_D | 0.04 | Regelmaessige Kundeninteraktionen erhalten Skills |
| Existential | delta_X | 0.02 | Kantonalbank-Mandat tief institutionell |

### Komplementaritaeten (gamma)

| Paar | Symbol | Wert | Interpretation |
|------|--------|------|----------------|
| Social x Existential | gamma_SX | **+0.30** | Buendner Teamkultur verstaerkt Kantonalbank-Mission |
| Development x Existential | gamma_DX | **+0.25** | Lernen staerkt Modernisierungsvision |
| Financial x Social | gamma_FS | **-0.10** | Schwaecher als RMS/Zindel — Staatsgarantie puffert |
| Social x Development | gamma_SD | **+0.20** | Peer-Lernen in Filialen moderat |
| Financial x Physical | gamma_FP | **+0.20** | Effizienzgewinne direkt sichtbar im CIR |
| Emotional x Development | gamma_ED | **+0.20** | Stolz treibt Weiterbildungsbereitschaft |

### Kontext-Elastizitaeten (psi)

| Dimension | Symbol | Wert | GKB-spezifisch |
|-----------|--------|------|----------------|
| Institutional | psi_I | 0.90 | Kantonalbank-Mandat, FINMA, Staatsgarantie |
| Social | psi_S | 0.85 | Clan-Kultur, CEO als Sponsor |
| Cognitive | psi_C | **0.70** | Weniger Stress als Newsroom, aber Compliance + Transformation |
| Cultural | psi_K | **1.05** | **HOECHSTE**: Buendner Identitaet, 156J, 75% lokale MA |
| Economic | psi_E | 0.80 | Stabil (CHF 528M), aber Zinsabhaengigkeit 67.5% |
| Temporal | psi_T | 0.75 | Weniger Zeitdruck als RMS, aber Konkurrenz waechst |
| Material | psi_M | 0.75 | Avaloq/Finnova, Gioia-Produkte, aber AI/ML=0.35 |
| Physical | psi_F | 0.70 | 45 Filialen — physisch bleibt wichtig in Graubuenden |

**Mittlere Elastizitaet:** 0.813 (niedrigste der 3 Cases)

### Anfangsbedingungen

| Variable | Symbol | Wert | Interpretation |
|----------|--------|------|----------------|
| Total Utility | U_0 | 0.18 | Moderate Motivation — Strategie existiert, Dringlichkeit fehlt |
| Adoption | A_0 | **0.10** | Fruehphase — Gioia, etwas Digital, aber meist traditionell |
| Resistance | R_0 | **0.60** | Moderat-hoch — 156J Tradition, Hierarchie, 12J Tenure |
| Habit | H_0 | 0.05 | Wenige digitale Gewohnheiten etabliert |
| Momentum | M_0 | 0.08 | Etwas Schwung von Gioia + Best Recruiter |
| Decision Cap. | D_0 | 0.25 | Moderat — partizipativ aber hierarchisch |

---

## Simulationsergebnis (12 Monate)

### Monatliche Trajektorie

| Mo. | U | A | R | H | M | D | Readiness | Phase |
|-----|-------|-------|-------|-------|-------|-------|-----------|-------|
| 0 | 0.180 | 0.100 | 0.600 | 0.050 | 0.080 | 0.250 | 0.170 | Kick-off |
| 1 | 0.485 | 0.101 | 0.600 | 0.053 | 0.078 | 0.273 | 0.174 | Kick-off |
| 2 | 0.796 | 0.105 | 0.599 | 0.057 | 0.077 | 0.297 | 0.179 | Kick-off |
| 3 | 1.000 | 0.113 | 0.598 | 0.060 | 0.077 | 0.319 | 0.186 | Kick-off |
| 4 | 1.000 | 0.123 | 0.597 | 0.064 | 0.078 | 0.339 | 0.193 | Kick-off |
| 5 | 1.000 | 0.135 | 0.595 | 0.068 | 0.080 | 0.358 | 0.201 | Kick-off |
| 6 | 1.000 | 0.148 | 0.594 | 0.073 | 0.082 | 0.376 | 0.209 | Kick-off |
| 7 | 1.000 | 0.163 | 0.592 | 0.078 | 0.084 | 0.392 | 0.218 | Kick-off |
| 8 | 1.000 | 0.180 | 0.591 | 0.084 | 0.086 | 0.407 | 0.227 | Kick-off |
| 9 | 1.000 | 0.199 | 0.589 | 0.090 | 0.089 | 0.421 | 0.237 | Kick-off |
| 10 | 1.000 | 0.220 | 0.587 | 0.097 | 0.093 | 0.434 | 0.247 | Kick-off |
| 11 | 1.000 | 0.244 | 0.586 | 0.104 | 0.097 | 0.446 | 0.258 | Umsetzung |
| **12** | **1.000** | **0.269** | **0.584** | **0.113** | **0.102** | **0.457** | **0.270** | **Umsetzung** |

### Schluesselmetriken

| Metrik | Start | Ende (12 Mo.) | Veraenderung |
|--------|-------|---------------|--------------|
| **Adoption** | 10.0% | **26.9%** | +16.9pp |
| **Resistance** | 60.0% | **58.4%** | -1.6pp |
| **Decision Capability** | 25.0% | **45.7%** | +20.7pp |
| **Readiness** | 17.0% | **27.0%** | +10.0pp |
| **Momentum** (max) | 8.0% | **10.2%** | +2.2pp (Peak) |
| **Habit** | 5.0% | **11.3%** | +6.3pp |

### Phasen-Prognose

| Phase | Schwellenwert | Prognose | Status |
|-------|---------------|----------|--------|
| Foundation → Implementation | theta_1 = 0.25 | **Monat 10.3** | Readiness_10 = 0.247, Uebergang Mo. 10-11 |
| Implementation → Scaling | theta_2 = 0.55 | **~Monat 26** (Extrapolation) | Readiness_12 = 0.270, Trend +0.83pp/Mo. |
| Scaling → Full Integration | theta_3 = 0.80 | **~Monat 40+** | Nur mit beschleunigter Widerstandsreduktion |

---

## Counterfactual-Analyse (Interventions-Wirkung)

### Einzelinterventionen

| Intervention | Ohne: Adoption | Delta | Primaer-Wirkung |
|-------------|---------------|-------|-----------------|
| INT-GKB-001: Unternehmer-Kontostruktur | 26.8% | -0.1pp | alpha_F ×0.7, alpha_S ×0.8 |
| INT-GKB-002: Zweitwohnungsbesitzer | 27.0% | -0.0pp | alpha_F ×0.6, mu_momentum ×0.8 |
| **INT-GKB-003: Plattform Cross-Selling** | **20.3%** | **-6.7pp** | **beta_adoption ×0.7, alpha_S ×0.7** |
| INT-GKB-004: Lebensmitte-Check | 26.7% | -0.3pp | alpha_D ×0.7, alpha_F/E ×0.8 |

### Alle 4 Interventionen zusammen

| Metrik | Baseline | Ohne alle 4 | Delta |
|--------|----------|-------------|-------|
| **Adoption** | 26.9% | 20.0% | **-7.0pp** |
| Resistance | 58.4% | 58.5% | +0.1pp |
| Decision Cap. | 45.7% | 45.7% | ±0.0pp |

**Erkenntnis:** INT-GKB-003 (Plattform-Kunden Cross-Selling) ist die WIRKSAMSTE Intervention — sie treibt 96% des gesamten Adoptions-Deltas. Grund: Sie wirkt direkt auf beta_adoption (Adoptionsrate), den primaeren Treiber in der Kick-off-Phase.

---

## 3-Wege-Vergleich: Zindel vs. RMS vs. GKB

### 12-Monats-Ergebnisse

| Aspekt | Zindel (Bau) | RMS (Medien) | GKB (Banking) |
|--------|-------------|-------------|---------------|
| **Adoption_12** | 32.1% | **47.5%** | 26.9% |
| **Resistance_12** | 56.7% | **52.9%** | 58.4% |
| **Decision_12** | 47.8% | 45.7% | 45.7% |
| **Readiness_12** | 28.4% | **37.4%** | 27.0% |
| **Momentum_max** | 0.107 | **0.193** | 0.102 |
| **Phasenuebergang** | Mo. 10.3 | **Ab Start** | Mo. 10.3 |
| **Mittl. Elastizitaet** | 0.863 | 0.856 | **0.813** |

### Dynamik-Profile

| Treiber | Zindel | RMS | GKB | Interpretation |
|---------|--------|-----|-----|----------------|
| beta_adoption | 0.50 | 0.40 | **0.30** | GKB langsamstes Tempo — konservative Bankkultur |
| rho_resistance | 0.04 | **0.03** | **0.025** | GKB langsamste Widerstandsreduktion |
| gamma_FS (Crowding-Out) | -0.15 | **-0.20** | -0.10 | GKB geringstes Risiko — Staatsgarantie |
| gamma_SX (Social×Purpose) | **0.35** | 0.25 | 0.30 | Zindel staerkste Kopplung (Familienunternehmen) |
| r_setback | 0.15 | **0.20** | 0.12 | GKB am wenigsten setback-sensitiv |
| mu_momentum | 0.08 | **0.10** | 0.07 | GKB baut Momentum am langsamsten auf |

### Branchen-Charakteristik

```
                    GESCHWINDIGKEIT
                         ↑
                         |
              RMS ●      |
              (Medien)   |
                         |
         Zindel ●        |
         (Bau)           |
                         |
                    GKB ●|
                (Banking)|
    ─────────────────────┼──────────────────→ STABILITAET
                         |
```

| Eigenschaft | Zindel | RMS | GKB |
|-------------|--------|-----|-----|
| **Geschwindigkeit** | Mittel | Hoch | Niedrig |
| **Stabilitaet** | Mittel | Niedrig | **Hoch** |
| **Crowding-Out Risiko** | Mittel | **Hoch** | Niedrig |
| **Kulturelle Verankerung** | Stark (Familie) | Mittel (Berufung) | **Sehr stark** (Institution) |
| **Zeithorizont** | 9 Monate | 12-24 Monate | **18-36 Monate** |

---

## Interpretation

### Staerken der GKB-Dynamik

1. **Geringestes Crowding-Out Risiko:** gamma_FS = -0.10 (vs. Zindel -0.15, RMS -0.20). Die Staatsgarantie und die stabile Ertragslage bedeuten, dass finanzielle Massnahmen die Teamkultur WENIGER bedrohen. GKB kann Spar- und Transformationsmassnahmen PARALLELER durchfuehren als die anderen beiden.

2. **Tiefste Setback-Sensitivitaet:** r = 0.12 (vs. Zindel 0.15, RMS 0.20). Rueckschlaege werden in der konservativen Bankkultur ruhiger verarbeitet. Kein 24h-News-Cycle wie bei RMS.

3. **Staerkste existenzielle Verankerung:** delta_X = 0.02 (niedrigster Zerfall). Das Kantonalbank-Mandat ist tief institutionell verankert und nahezu erosionsresistent. Purpose muss nicht kuenstlich erzeugt werden — er ist im Gesetz verankert.

4. **Hoechste Fuehrungsstabilitaet:** CEO seit 2019, Praesident seit 2014, GL-Stabilitaet=0.85. Dies gibt der Transformation ein stabiles Fundament, auch wenn der Prozess langsamer ist.

### Risiken und Engpaesse

1. **Langsamste Adoptionsrate:** beta = 0.30 (vs. Zindel 0.50, RMS 0.40). Die konservative Bankkultur (Hierarchie=0.65, Agile=0.45, Tradition=0.80) bremst Adoption. **Implikation:** Braucht spezifische Beschleuniger — z.B. «Lighthouse-Filialen» die als Vorbild wirken.

2. **Langsamste Widerstandsreduktion:** rho = 0.025 (niedrigste aller 3 Cases). 156 Jahre Tradition und 12 Jahre durchschnittliche Betriebszugehoerigkeit erzeugen starke Pfadabhaengigkeit. **Implikation:** Widerstand kann NICHT durch Top-Down-Druck reduziert werden — braucht Bottom-Up-Champions in den Filialen.

3. **Niedrigste Tech-Reife:** AI/ML = 0.35, psi_M = 0.75 (niedrigste). Waehrend RMS 40 produktive KI-Use-Cases hat, steckt GKB noch in fruehen KI-Phasen. **Implikation:** Tech-Investitionen muessen PRIORISIERT werden — nicht «alles gleichzeitig».

4. **Kognitive Last unterschaetzt:** psi_C = 0.70 wirkt moderat, aber Banking-Compliance + FINMA + Digitalisierung + Kundenberatung gleichzeitig ergibt kumulative kognitive Belastung. **Implikation:** Transformationsteams von Tagesgeschaeft partiell entlasten.

### GKB-spezifische Empfehlungen (aus Simulation abgeleitet)

1. **INT-GKB-003 priorisieren:** Die Plattform-Kunden Cross-Selling Intervention ist mit -6.7pp Adoptions-Impact die wirksamste. Sie wirkt direkt auf die Adoptionsrate und sollte als ERSTES gestartet werden.

2. **Lighthouse-Filialen einrichten:** 3-5 Filialen als «Digital-First»-Vorbilder transformieren. Der soziale Beweis (psi_S = 0.85) in einer Clan-Kultur ist der staerkste Uebertragungs-Mechanismus.

3. **Buendner Identitaet als Change-Narrativ nutzen:** psi_K = 1.05 (hoechste Elastizitaet). «Die GKB modernisiert WEIL sie buendnerisch ist, nicht OBWOHL.» Die 156-jaehrige Innovationsgeschichte (Strom-Finanzierung, Tourismus-Aufbau) als Praezedenz framen.

4. **Langfristigen Horizont akzeptieren:** GKB ist ein «Slow Transformation»-Fall. 18-36 Monate bis substantielle Ergebnisse, ABER die Ergebnisse sind nachhaltiger (geringere Friction, geringerer Zerfall). Den Bankrat entsprechend erwarten lassen.

---

## Counterfactual-Zusammenfassung fuer Board

```
┌─────────────────────────────────────────────────────────────────────────┐
│  WAS PASSIERT OHNE DIE 4 INTERVENTIONEN?                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  MIT Interventionen:                                                    │
│  Adoption 26.9% │ Readiness 27.0% │ Phasenuebergang Mo. 10.3           │
│                                                                         │
│  OHNE Interventionen:                                                   │
│  Adoption 20.0% │ Readiness ~21%  │ Phasenuebergang Mo. ~16+           │
│                                                                         │
│  DELTA:                                                                 │
│  -7.0pp Adoption │ ~-6pp Readiness │ +6 Monate Verzoegerung            │
│                                                                         │
│  WIRKSAMSTE INTERVENTION:                                               │
│  INT-GKB-003 (Plattform Cross-Selling) = 96% des Gesamteffekts         │
│                                                                         │
│  EMPFEHLUNG: Mit INT-GKB-003 im Q2 starten, INT-GKB-004 im Q3         │
│  nachlegen, INT-GKB-001/002 parallel ab Q3.                            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

> **Reproduktion:** `python scripts/ode_simulator.py --customer gkb --project GKB001 --months 12`
> **Counterfactual:** `python scripts/ode_simulator.py --customer gkb --project GKB001 --months 12 --counterfactual INT-GKB-001 INT-GKB-002 INT-GKB-003 INT-GKB-004`
> **Parameter-SSOT:** `data/customers/gkb/kontextvektoren/GKB001_ODE_parameters.yaml`
> **Tests:** 35/35 bestanden (`python -m pytest tests/test_ode_simulator.py`)
> **Provenance:** Layer 1, susceptibility = 0.0
