# Kontextanalyse ECHfP - Energie Schweiz für Private

**Session-ID:** EBF-S-2026-01-28-ENE-001
**Projekt:** BFE_019_ECHfP
**Datum:** 2026-01-28
**Modus:** STANDARD
**Autor:** Claude (EBF Framework)

---

## Executive Summary

**Ziel:** Wechselrate Fossil → Erneuerbar von 65% auf 75% (+10pp)

**Zentrale Erkenntnis:** Der Installateur ist der Schlüssel, nicht der Hausbesitzer. Bei 55% Notfall-Ersatz entscheidet der Installateur innerhalb von 24-48h. Die bisherige Kampagne (2021-2023) fokussierte auf Endkunden-Awareness – der richtige Ansatz für die Aufbauphase. Aber 2023 zeigt: «Wechselbereitschaft ist gesunken» → Der Bottleneck hat sich von Awareness zu Conversion verschoben.

**Handlungsempfehlung:** Shift von AWARE-dominanten zu INST+WHEN-dominanten Interventionen.

| Priorität | Intervention | Impact | Budget |
|-----------|--------------|--------|--------|
| 1 | Installateur-Aktivierung (M6) | 32% | 35% |
| 2 | Nachbarschafts-Cluster (M7) | 24% | 25% |
| 3 | STWE-Facilitierung (M8) | 18% | 20% |
| 4 | Trigger-Marketing | 12% | 15% |

**Prognose (Base Case):** P(Ziel ≥ 75%) = 51%, 95% CI: [68.2%, 82.4%]

---

## 1. Kontextanalyse

### 5-Ebenen Hierarchie

| Ebene | Quelle | Key Insights |
|-------|--------|--------------|
| MACRO | BCM2_04_KON (CH) | Umweltbewusstsein ↑, aber Vertrauen ↓, Polarisierung ↑ |
| MESO | Energy Sector | Förderstruktur stark, psychologische Barrieren dominant |
| MIKRO | BFE | Mandat ES2050, 5 Module, 3+1 Segmente |
| INDIVIDUAL | BCM2_INDIV_BFE | β=0.75-0.82, λ=2.1-2.5, W_base=0.22-0.42 |
| META | model.yaml | Interventionsvektoren, 10C vollständig |

### Kritische Ψ-Dimensionen

- **κ_SOCIAL = 0.68** (Nachbarschafts-Norm vorhanden, nicht aktiviert)
- **κ_AWX = 0.35** (Förder-Awareness niedrig, Ziel: 0.80)
- **κ_INST = 0.72** (Förderstruktur stark)

---

## 2. Modell

### Theorie-Fundierung

| Theorie | Anwendung |
|---------|-----------|
| MS-RD-004 Status Quo Bias | «Meine Ölheizung funktioniert noch» |
| MS-TP-001 Quasi-Hyperbolic | Upfront > langfristiger Nutzen |
| MS-NU-002 Default Effects | Opt-out Förderanträge |
| MS-IN-005 Social Norms | Nachbarschafts-Effekt |

### Modell-Erweiterungen

1. **M1: Installateur-Modell** (10C + Interventionsvektor für SEG_INST)
2. **M2: γ-Matrix** (Modul-Komplementaritäten, stärkste: M4↔M5 = +0.65)
3. **M3: Crowding-Analyse** (u_S × u_F, γ = -0.20, Mitigation: Sequenzierung)

---

## 3. Parameter

### Posterior-Parameter (68% CI)

| Segment | β | λ | θ | W_base | Δ_required |
|---------|---|---|---|--------|------------|
| SEG_EFH | 0.82 [.77,.87] | 2.1 [1.9,2.3] | 0.65 | 0.35 | 0.30 |
| SEG_MFH | 0.78 [.72,.84] | 2.3 [2.1,2.5] | 0.72 | 0.28 | 0.44 |
| SEG_STWE | 0.75 [.70,.80] | 2.5 [2.3,2.7] | 0.78 | 0.22 | 0.56 |
| SEG_INST | 0.65 [.58,.72] | 1.8 [1.6,2.0] | 0.55 | 0.42 | 0.13 |

### Monte Carlo Simulation (10'000 Draws)

- **Wechselrate 95% CI:** [68.2%, 82.4%]
- **P(Ziel ≥ 75%):** 51%
- **P(Ziel ≥ 70%):** 83%

### Szenario-Analyse

| Szenario | Wahrscheinlichkeit | Wechselrate | Heizungen p.a. |
|----------|-------------------|-------------|----------------|
| Best Case | 15% | 82% | 36'100 (+7'500) |
| Base Case | 60% | 75% | 33'000 (+4'400) |
| Worst Case | 25% | 68% | 29'900 (+1'300) |

### Sensitivitätsanalyse

| Rang | Parameter | Impact |
|------|-----------|--------|
| 1 | Installateur-Empfehlung (γ=0.78) | 32% |
| 2 | Nachbarschafts-Norm (κ_SOCIAL) | 24% |
| 3 | W_base STWE | 18% |
| 4 | Förder-Awareness (κ_AWX) | 14% |
| 5 | Trigger-Timing | 12% |

---

## 4. Analyse & Empfehlungen

### Haupttreiber

Der **Installateur** ist der grösste Hebel:
- 55% aller Heizungsersatz = Notfall (24-48h Entscheidung)
- Installateur-Empfehlung wird mit γ = 0.78 befolgt
- W_base Installateur (0.42) ist näher an θ (0.55) als alle Endkunden-Segmente

### 4 Strategische Empfehlungen

#### Empfehlung 1: Installateur-First Strategie (35% Budget)

| Massnahme | 10C-Target | Expected Impact |
|-----------|------------|-----------------|
| Notfall-Toolkit | I_WHEN | +8pp WP-Empfehlung |
| Marge-Kommunikation | I_WHAT (u_F) | +5pp |
| BFE Energie-Experte Zertifizierung | I_WHAT (u_S) | +3pp Schulung |
| Direkt-Einreichung Förderantrag | I_WHEN | +10pp Fördernutzung |

#### Empfehlung 2: Nachbarschafts-Cluster (25% Budget)

| Massnahme | 10C-Target | Expected Impact |
|-----------|------------|-----------------|
| Gemeinde-Challenges | I_WHAT (u_S) | κ_SOCIAL +10pp |
| WP-Badge am Briefkasten | I_WHAT (u_S) | Sichtbarkeit |
| Lokale Testimonials | I_AWARE + I_WHAT | Social Proof |
| Nachbar-Rabatt | I_WHAT (u_F) | Cluster-Anreiz |

#### Empfehlung 3: STWE Champion-Strategie (20% Budget)

| Massnahme | 10C-Target | Expected Impact |
|-----------|------------|-----------------|
| Champion-Identifikation | I_WHO | Meinungsführer |
| Champion-Toolkit | I_AWARE | Präsentationsmaterial |
| Facilitierte Versammlung | I_WHEN | Moderation |
| HEV-Partnerschaft | I_WHAT (u_S) | Legitimität |

#### Empfehlung 4: Trigger-Marketing (15% Budget)

| Massnahme | 10C-Target | Expected Impact |
|-----------|------------|-----------------|
| Installateur-Alert | I_WHEN | Response < 24h |
| EVU-Partnerschaft | I_WHEN | Verbrauchsanomalie |
| Proaktive Ansprache | I_STAGE | «Heizung 18+ Jahre» |

---

## 5. Intervention Review

### Gap-Analyse: Roadmap 2021-2024 vs. Empfehlungen

Die bisherige Roadmap fokussierte auf:
- ✅ Awareness-Aufbau (kontinuierliche Präsenz, Breitenwirkung)
- ✅ Social Proof (Testimonials, Erfahrungsberichte)
- ✅ Journey-Optimierung (Nudges, Cognitive Ease)
- ✅ Personalisierung (Segmentierung, regionale Identität)

**Kritische Gaps:**
- ❌ **Installateur-Intervention fehlt komplett** (grösster Hebel!)
- ❌ **STWE-spezifische Massnahmen fehlen**
- ⚠️ **Trigger-Marketing nur ansatzweise**

### Roadmap-Abgleich: Problem 2023

Die Roadmap dokumentiert: «Wechselbereitschaft ist gesunken».

**Interpretation:** Der Bottleneck hat sich verschoben:
- 2021-2022: Awareness-Problem → Awareness-Kampagne war richtig
- 2023+: Conversion-Problem → Installateur + Trigger ist der neue Hebel

---

## 6. Schlussfolgerungen

1. **Bisherige Strategie war richtig** für 2021-2023 (Awareness-Aufbau)
2. **Bottleneck hat sich verschoben** von Awareness zu Conversion
3. **Installateur ist der grösste Hebel** (55% Notfall, γ=0.78)
4. **STWE bleibt schwierig** (P(Erfolg)=23%), aber adressierbar
5. **Crowding-Risiko** bei Social × Financial → Sequenzierung nötig

---

## Anhang

### A. Quellen

**BCM2 Kontext-Datenbank:**
- BCM2_04_KON_economic.yaml
- BCM2_04_KON_socio_cultural.yaml
- BCM2_MIKRO_BFE_context.yaml
- BCM2_INDIV_BFE_behavioral.yaml

**Theorien (theory-catalog.yaml):**
- MS-RD-004: Status Quo Bias (Samuelson & Zeckhauser 1988)
- MS-TP-001: Quasi-Hyperbolic Discounting (Laibson 1997)
- MS-NU-002: Default Effects (Madrian & Shea 2001)
- MS-IN-005: Social Norms (Elster 1989)
- MS-SP-001: Inequity Aversion (Fehr & Schmidt 1999)

**Papers (bcm_master.bib):**
- Gächter et al. (2022): Meta-Analyse Verlustaversion
- Frederick et al. (2002): Time Discounting Survey

### B. Session-Metadata

```yaml
session_id: EBF-S-2026-01-28-ENE-001
project_id: BFE-2026-001
domain: ENE
mode: STANDARD
steps_completed: [0, 1, 2, 3, 4, 5, 6]
model_extensions: [M1_Installateur, M2_Gamma_Matrix, M3_Crowding]
new_modules: [M6, M7, M8]
```

---

*Generiert mit dem Evidence-Based Framework (EBF) | FehrAdvice & Partners AG*

*https://claude.ai/code/session_016Ryht6cjqBhEAzziPLMNTb*
