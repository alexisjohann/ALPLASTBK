# EBF Goal Decomposition Method (EBF-GDM)

> **Version:** 1.0
> **Datum:** 2026-02-09
> **Status:** ACTIVE
> **SSOT:** `docs/frameworks/ebf-gdm-methodology.md` (dieses Dokument)
> **Zielarchitektur:** `data/ebf-gdm-goals.yaml`
> **Wissenschaftliche Basis:** KAOS (van Lamsweerde 2001) + 7 EBF-Erweiterungen

---

## 1. Zweck

Das EBF-GDM ist die formale Methodik, mit der das Evidence-Based Framework (EBF) von seiner Mission über Ziele zu Arbeitspaketen und Lieferobjekten gelangt. Es stellt Nachvollziehbarkeit (Traceability) sicher: Jedes Arbeitspaket lässt sich bis zur Mission zurückverfolgen, und jedes Lieferobjekt hat messbare Akzeptanzkriterien.

---

## 2. Mission

```
EBF soll die Grundlage, der Source Code sein, um Verhalten und die
Konsequenzen von Entscheidungen auf das Verhalten so genau wie möglich
prognostizieren zu können.
```

**Zwei Prognosetypen:**
- **Typ 1 (Prognose):** Was wird passieren? (gegeben Kontext Ψ und Menschen)
- **Typ 2 (Intervention):** Was passiert, WENN wir intervenieren? (gegeben Ψ, Menschen, Intervention I)

---

## 3. Wissenschaftliche Grundlage

### 3.1 Straw-Man: KAOS (van Lamsweerde)

KAOS (Knowledge Acquisition in autOmated Specification) ist ein zielorientiertes Requirements-Engineering-Framework, das Ziele als Baumstruktur (AND/OR-Dekomposition) modelliert und formale Traceability zwischen Zielen, Anforderungen und Agenten sicherstellt.

**Kernelemente von KAOS:**
- Ziel-Dekomposition (AND/OR-Bäume)
- Obstacle Analysis (Hindernisse pro Ziel)
- Agent Responsibility (Zuweisung an Akteure)
- Formale Spezifikation (Temporal Logic)

**Quellen:**
- van Lamsweerde (2001): «Goal-Oriented Requirements Engineering: A Guided Tour»
- van Lamsweerde (2009): *Requirements Engineering: From System Goals to UML Models to Software Specifications*
- Dardenne, van Lamsweerde & Fickas (1993): «Goal-Directed Requirements Acquisition»

### 3.2 Gap-Analyse: KAOS → EBF-GDM

| Gap | KAOS-Limitation | EBF-Bedarf | Erweiterung |
|-----|-----------------|------------|-------------|
| **G1** | Keine Metriken pro Ziel | Messbare Fortschrittsindikatoren | E1: GQM/OKR-Metriken |
| **G2** | Keine IST-SOLL-Gap-Analyse | Empirischer Status pro Unterziel | E2: Ansoff-Gap |
| **G3** | Keine Lieferobjekte/Akzeptanzkriterien | Prüfbare Deliverables | E3: PRINCE2-LO |
| **G4** | Kein Feedback-Loop | 3-Level-Feedback (Parameter, Modell, Theorie) | E4: Argyris/Bateson-Feedback |
| **G5** | Keine Querschnittsanforderungen | Systemziele, die alle HZ betreffen | E5: AOP-Querschnitt |
| **G6** | Kein Rückwirkungsmechanismus auf Inputs | Interventionen verändern Kontext und Menschen | E6: Meadows/Sterman-Rückkopplung |
| **G7** | Keine empirische Validierung | Brier-Score, Kalibrierungsmetriken | E7: Tetlock/Brier-Validierung |

### 3.3 EBF-GDM = KAOS + E1–E7

```
EBF-GDM = KAOS(AND/OR, Obstacles, Agents, Traceability)
         + E1(GQM/OKR Metrics)
         + E2(Ansoff Gap Analysis)
         + E3(PRINCE2 Deliverables)
         + E4(Argyris/Bateson 3-Level Feedback)
         + E5(AOP Cross-Cutting Concerns)
         + E6(Meadows/Sterman Input Feedback)
         + E7(Tetlock/Brier Empirical Validation)
```

---

## 4. Die 7 EBF-GDM Erweiterungen

### E1: GQM/OKR-Metriken (Basili et al. 1994, Doerr 2018)

**Regel:** Jedes Ziel hat mindestens einen Key Result (KR) mit messbarem Indikator.

```yaml
# Beispiel
hz1:
  name: "Menschen verstehen"
  key_results:
    - kr: "≥50 Papers mit Individual-Level Parametern integriert"
      metric: "count(PAR-IND-*)"
      current: 12
      target: 50
```

**Quellen:**
- Basili, Caldiera & Rombach (1994): «The Goal Question Metric Approach»
- Kaplan & Norton (1992): «The Balanced Scorecard»
- Doerr (2018): *Measure What Matters*

### E2: Ansoff-Gap-Analyse (Ansoff 1965)

**Regel:** Für jedes Unterziel wird der empirische IST-Status erhoben (✅ erreicht / ⚠️ teilweise / 🔴 offen) und die Gap dokumentiert.

```yaml
# Beispiel
uz1_1:
  name: "Psychologische Typen"
  ist: "12 Typen in BCM2_05_IND"
  soll: "Vollständiges 48-Parameter-Profil mit Literatur-Verankerung"
  gap: "36 Parameter fehlen oder haben nur LLMMC-Prior"
  status: "teilweise"  # ⚠️
```

**Quellen:**
- Ansoff (1965): *Corporate Strategy*
- Mintzberg (1994): *The Rise and Fall of Strategic Planning*

### E3: PRINCE2-Lieferobjekte (OGC 2017)

**Regel:** Jedes Arbeitspaket hat mindestens ein Lieferobjekt (LO) mit Akzeptanzkriterien.

```yaml
# Beispiel
ap_1_1:
  name: "Individual-Parameter-Erweiterung"
  deliverables:
    - lo: "BCM2_05_IND mit 48 Parametern"
      acceptance: "Alle Parameter haben PAR-IND-* Referenz + Tier 1/2 Quelle"
      format: "YAML"
```

**Quellen:**
- OGC (2017): *Managing Successful Projects with PRINCE2*, 6th Ed.
- Haugan (2002): *Effective Work Breakdown Structures*
- PMI (2021): *PMBOK Guide*, 7th Ed.

### E4: Argyris/Bateson 3-Level-Feedback

**Regel:** Validierungsergebnisse fliessen auf 3 Ebenen zurück:

| Level | Was wird angepasst | Trigger | Analog |
|-------|-------------------|---------|--------|
| **L1** | Parameter-Werte (θ) | Brier-Score-Abweichung > Schwelle | Argyris Single-Loop |
| **L2** | Modell-Struktur (Variablen, Funktionalform) | Systematischer Bias über multiple Prognosen | Argyris Double-Loop |
| **L3** | Theorie/Axiome | Fundamentale Prognose-Fehler, neue Evidenz widerspricht Axiom | Bateson Learning III |

```
Prognose → Realität → Δ
  ↓
  L1: |Δ| < ε₁ → Bayesian Update auf θ
  L2: |Δ| > ε₁ ∧ systematisch → Modell-Revision
  L3: Axiom-Widerspruch → Theory-Revision
```

**Quellen:**
- Argyris (1977): «Double Loop Learning in Organizations»
- Argyris & Schön (1978): *Organizational Learning*
- Bateson (1972): *Steps to an Ecology of Mind*

### E5: AOP-Querschnittsanforderungen (Kiczales et al. 1997)

**Regel:** Systemziele (SZ1–SZ7) sind Querschnittsanforderungen, die ALLE Inhaltsziele betreffen. Jedes Arbeitspaket wird gegen alle SZ geprüft.

```
SZ1 (Modularität)     × AP_1_1, AP_1_2, ..., AP_6_4
SZ2 (Konsistenz)      × AP_1_1, AP_1_2, ..., AP_6_4
...
SZ7 (Nutzbarkeit)     × AP_1_1, AP_1_2, ..., AP_6_4
```

**Quelle:**
- Kiczales et al. (1997): «Aspect-Oriented Programming»

### E6: Meadows/Sterman Input-Rückkopplung

**Regel:** Interventionen (HZ6) verändern die Inputs Kontext (Ψ) und Menschen, was neue Prognosen erfordert.

```
Intervention I → ΔΨ (Kontext verändert sich)
              → ΔMensch (Menschen verändern sich)
              → Neue Prognose nötig (Typ 1 + Typ 2)
```

**Beispiel:** Eine Nudge-Intervention verändert den Default (Ψ_I). Nach der Intervention ist der «neue Normal-Kontext» ein anderer. Alle Prognosen, die auf dem alten Ψ_I basieren, müssen aktualisiert werden.

**Quellen:**
- Meadows (2008): *Thinking in Systems: A Primer*
- Sterman (2000): *Business Dynamics: Systems Thinking and Modeling for a Complex World*

### E7: Tetlock/Brier Empirische Validierung

**Regel:** Prognosen werden mit dem Brier-Score kalibriert. Kalibrierungsmetriken fliessen in E4-Feedback ein.

```
Brier Score = (1/N) × Σ (p_i - o_i)²

Wobei:
  p_i = Prognostizierte Wahrscheinlichkeit
  o_i = Tatsächliches Ergebnis (0 oder 1)
```

**Ziel-Kalibrierung:**
- «70%-Prognosen» sollen in ~70% der Fälle eintreten
- Overconfidence (systematisch zu hohe p) → L1-Feedback
- Systematischer Bias → L2-Feedback

**Quellen:**
- Tetlock & Gardner (2015): *Superforecasting: The Art and Science of Prediction*
- Brier (1950): «Verification of Forecasts Expressed in Terms of Probability»

---

## 5. Die 7 GDM-Regeln

### R1: Traceability (← KAOS + Gotel & Finkelstein 1994)

> Jeder Knoten im Zielbaum hat eine eindeutige ID und einen expliziten Elternknoten.

```
MISSION → HZ-n → UZ-n-m → AP-n-m-k → LO-n-m-k-j
```

**ID-Schema:**
| Ebene | Format | Beispiel |
|-------|--------|----------|
| Mission | `MISSION` | MISSION |
| Hauptziel | `HZ-{n}` | HZ-1, HZ-2 |
| Unterziel | `UZ-{n}-{m}` | UZ-1-1, UZ-3-2 |
| Arbeitspaket | `AP-{n}-{m}-{k}` | AP-1-1-1 |
| Lieferobjekt | `LO-{n}-{m}-{k}-{j}` | UNMAPPED_LO-1-1-1-1 |

**Quellen:**
- Gotel & Finkelstein (1994): «An Analysis of the Requirements Traceability Problem»
- Ramesh & Jarke (2001): «Toward Reference Models for Requirements Traceability»

### R2: Meilenstein-Regel (← PRINCE2)

> Jedes Hauptziel hat mindestens einen Meilenstein mit Datum und Prüfkriterium.

### R3: Gap-Regel (← E2 Ansoff)

> Jedes Unterziel hat einen dokumentierten IST-Status und eine Gap-Beschreibung.

### R4: Arbeitspaket-Regel (← PMI/PRINCE2)

> Arbeitspakete werden aus Gaps gebündelt. Ein AP adressiert genau eine Gap oder eine logisch zusammenhängende Gruppe von Gaps.

### R5: Lieferobjekt-Regel (← E3 PRINCE2)

> Jedes AP hat mindestens ein Lieferobjekt mit Akzeptanzkriterien. Ein LO ist «fertig» wenn alle Akzeptanzkriterien erfüllt sind.

### R6: Vollständigkeits-Regel (← INCOSE/NASA SE)

> Der Zielbaum ist vollständig wenn: (a) jede Gap mindestens einem AP zugeordnet ist, (b) jedes AP mindestens ein LO hat, (c) jedes SZ auf jedes AP geprüft wurde.

**Quellen:**
- INCOSE (2015): *Systems Engineering Handbook*, 4th Ed.
- NASA (2017): *Systems Engineering Handbook*

### R7: Querschnitt-Regel (← E5 AOP)

> Systemziele (SZ) werden als Prüfmatrix auf ALLE Arbeitspakete angewendet. Konflikte werden dokumentiert und aufgelöst.

---

## 6. Zielarchitektur

### 6.1 Übersicht: Zirkulärer Flow

```
            ┌──────────────────────────────────────┐
            │                                      │
            ▼                                      │
   ┌─────────────┐     ┌─────────────┐            │
   │  HZ1        │     │  HZ2        │            │
   │  MENSCHEN   │     │  KONTEXT    │            │
   │  (Input 1)  │     │  (Input 2)  │            │
   └──────┬──────┘     └──────┬──────┘            │
          │                   │                    │
          └─────────┬─────────┘                    │
                    ▼                              │
            ┌─────────────┐                        │
            │  HZ3        │                        │
            │  MODELL &   │                        │
            │  EVIDENZ    │                        │
            └──────┬──────┘                        │
                   ▼                               │
            ┌─────────────┐                        │
            │  HZ4        │                        │
            │  PROGNOSE   │                        │ Rückkopplung
            └──────┬──────┘                        │ (E6: ΔΨ, ΔMensch)
                   ▼                               │
            ┌─────────────┐                        │
            │  HZ5        │                        │
            │  VALIDIERUNG│──── L1/L2/L3 ──┐      │
            │  & LERNEN   │                │      │
            └──────┬──────┘                │      │
                   ▼                       ▼      │
            ┌─────────────┐         ┌──────────┐  │
            │  HZ6        │         │ Feedback │  │
            │ INTERVENTION│────────►│ auf HZ3  │  │
            │ & RÜCKKOPPL.│         └──────────┘  │
            └──────┬──────┘                        │
                   │                               │
                   └───────────────────────────────┘
```

**OUTPUT (emergiert aus HZ1–HZ6):**
- 10C Workflow (der operative Prozess)
- Prognosen (Typ 1 + Typ 2)
- Interventionsempfehlungen
- Kalibrierte Parameter

### 6.2 Sechs Inhaltsziele (HZ1–HZ6)

| ID | Name | Unterziele | Status |
|----|------|-----------|--------|
| **HZ1** | Menschen verstehen | UZ-1-1 bis UZ-1-4 | 1✅ 1⚠️ 2🔴 |
| **HZ2** | Kontext modellieren | UZ-2-1 bis UZ-2-4 | 1✅ 2⚠️ 1🔴 |
| **HZ3** | Modell & Evidenz | UZ-3-1 bis UZ-3-4 | 1✅ 2⚠️ 1🔴 |
| **HZ4** | Prognose | UZ-4-1 bis UZ-4-4 | 0✅ 1⚠️ 3🔴 |
| **HZ5** | Validierung & Lernen | UZ-5-1 bis UZ-5-3 | 1✅ 1⚠️ 1🔴 |
| **HZ6** | Intervention & Rückkopplung | UZ-6-1 bis UZ-6-4 | 1✅ 1⚠️ 2🔴 |

**Vollständige Zielarchitektur:** `data/ebf-gdm-goals.yaml`

### 6.3 Sieben Systemziele (SZ1–SZ7)

| ID | Name | Prüfkriterium |
|----|------|---------------|
| **SZ1** | Modularität | Jede Komponente ist unabhängig testbar |
| **SZ2** | Formale Konsistenz | Keine Widersprüche zwischen Axiomen, Modellen, Parametern |
| **SZ3** | Empirische Verankerung | Jeder Parameter hat PAR-*-* Referenz mit Tier 1/2 Quelle |
| **SZ4** | Ausführbarkeit | Jedes Modell ist als Python-Script lauffähig |
| **SZ5** | Lernfähigkeit | 3-Level-Feedback implementiert (E4) |
| **SZ6** | Skalierbarkeit | Neue Domänen/Kontexte/Menschen hinzufügbar ohne Refactoring |
| **SZ7** | Nutzbarkeit | Consultant kann Modell in <30 min anwenden |

---

## 7. Nächste Schritte (nach Methodik-Dokumentation)

Die Methodik ist das WIE. Die nächsten Schritte wenden sie an:

1. **E1 anwenden:** Key Results für alle 23 UZ definieren (Metriken + Targets)
2. **E2 anwenden:** Empirischen IST-Status für alle 23 UZ erheben
3. **R4 anwenden:** Gaps zu Arbeitspaketen bündeln
4. **R5 anwenden:** Lieferobjekte mit Akzeptanzkriterien pro AP
5. **R7 anwenden:** SZ-Querschnittsprüfung für alle AP
6. **R6 anwenden:** Vollständigkeitsprüfung

---

## 8. Quellenverzeichnis

### KAOS & Requirements Engineering
- van Lamsweerde, A. (2001). Goal-Oriented Requirements Engineering: A Guided Tour. *Proceedings of RE'01*, pp. 249–262.
- van Lamsweerde, A. (2009). *Requirements Engineering: From System Goals to UML Models to Software Specifications.* Wiley.
- Dardenne, A., van Lamsweerde, A., & Fickas, S. (1993). Goal-Directed Requirements Acquisition. *Science of Computer Programming*, 20(1-2), 3–50.
- Yu, E. (1997). Towards Modelling and Reasoning Support for Early-Phase Requirements Engineering. *Proceedings of RE'97*, pp. 226–235.

### Metriken & Balanced Scorecard
- Basili, V., Caldiera, G., & Rombach, H.D. (1994). The Goal Question Metric Approach. In *Encyclopedia of Software Engineering*. Wiley.
- Kaplan, R.S. & Norton, D.P. (1992). The Balanced Scorecard — Measures That Drive Performance. *Harvard Business Review*, 70(1), 71–79.
- Kaplan, R.S. & Norton, D.P. (2004). *Strategy Maps: Converting Intangible Assets into Tangible Outcomes.* Harvard Business School Press.
- Doerr, J. (2018). *Measure What Matters: How Google, Bono, and the Gates Foundation Rock the World with OKRs.* Portfolio/Penguin.

### Projektmanagement & Work Breakdown
- PMI (2021). *A Guide to the Project Management Body of Knowledge (PMBOK Guide)*, 7th Ed. Project Management Institute.
- OGC (2017). *Managing Successful Projects with PRINCE2*, 6th Ed. TSO.
- Haugan, G.T. (2002). *Effective Work Breakdown Structures.* Management Concepts.

### Traceability
- Gotel, O. & Finkelstein, A. (1994). An Analysis of the Requirements Traceability Problem. *Proceedings of RE'94*, pp. 94–101.
- Ramesh, B. & Jarke, M. (2001). Toward Reference Models for Requirements Traceability. *IEEE Transactions on Software Engineering*, 27(1), 58–93.

### Systems Engineering
- INCOSE (2015). *Systems Engineering Handbook*, 4th Ed. Wiley.
- NASA (2017). *NASA Systems Engineering Handbook*, Rev. 2. NASA/SP-2016-6105.

### Strategische Planung
- Ansoff, H.I. (1965). *Corporate Strategy: An Analytic Approach to Business Policy for Growth and Expansion.* McGraw-Hill.
- Mintzberg, H. (1994). *The Rise and Fall of Strategic Planning.* Free Press.
- Akao, Y. (1991). *Hoshin Kanri: Policy Deployment for Successful TQM.* Productivity Press.

### Feedback & Lerntheorie
- Argyris, C. (1977). Double Loop Learning in Organizations. *Harvard Business Review*, 55(5), 115–125.
- Argyris, C. & Schön, D.A. (1978). *Organizational Learning: A Theory of Action Perspective.* Addison-Wesley.
- Bateson, G. (1972). *Steps to an Ecology of Mind.* University of Chicago Press.

### Systemdynamik & Rückkopplung
- Meadows, D.H. (2008). *Thinking in Systems: A Primer.* Chelsea Green Publishing.
- Sterman, J.D. (2000). *Business Dynamics: Systems Thinking and Modeling for a Complex World.* McGraw-Hill.

### Aspect-Oriented Programming
- Kiczales, G. et al. (1997). Aspect-Oriented Programming. *Proceedings of ECOOP'97*, LNCS 1241, pp. 220–242.

### Prognose & Kalibrierung
- Tetlock, P.E. & Gardner, D. (2015). *Superforecasting: The Art and Science of Prediction.* Crown.
- Brier, G.W. (1950). Verification of Forecasts Expressed in Terms of Probability. *Monthly Weather Review*, 78(1), 1–3.
