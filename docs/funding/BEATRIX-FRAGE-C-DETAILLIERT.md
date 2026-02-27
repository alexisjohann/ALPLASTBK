# Frage c) Feasibility & Risk Reduction — Detaillierte Antwort

**Version:** 5.0 (Überarbeitet nach Qualitätsframework)
**Datum:** 2026-01-18
**Für:** Innosuisse Innovation Cheque

---

## Executive Summary

**Mit CHF 15'000 validieren wir die vier kritischen Unsicherheiten vor dem Scale-up:**

| Unsicherheit | Wer validiert | Erwartung |
|--------------|---------------|-----------|
| Technische Skalierbarkeit | Prof. Gall | GO: 60% |
| Pipeline-Robustheit | Prof. Gall | GO: 70% |
| Nutzerakzeptanz | Prof. Luger | GO: 50% |
| Organisationale Adoption | Prof. Luger | GO: 40% |

**Deliverables:** 3 Reports (Technical, Adoption, Integrated) → **GO / PILOT / NO-GO** Entscheidung

**ROI der Studie:** 267% erwarteter Wert (CHF 40k Ersparnis durch vermiedene Fehlinvestitionen)

**Bei GO:** Innosuisse Hauptprojekt (CHF 300-500k) für Produktentwicklung. Siehe **Frage d)** für Partner-Details.

---

## Die vier Unterfragen

| # | Original-Frage (Fasnacht) | Unsere Antwort-Struktur |
|---|---------------------------|-------------------------|
| c1 | What aspect of **feasibility** needs to be tested? | Abschnitt 1: Die vier Machbarkeits-Dimensionen |
| c2 | What **proof-of-concept** can be achieved with CHF 15'000? | Abschnitt 2: Konkrete Deliverables |
| c3 | How will the research partner's work **reduce risks**? | Abschnitt 3: Risiko-Reduktions-Matrix |
| c4 | What would be the **next steps** if feasibility is proven? | Abschnitt 4: Roadmap nach GO |

---

# Abschnitt 1: Welche Machbarkeitsaspekte müssen getestet werden?

## 1.1 Die vier kritischen Unsicherheiten

BEATRIX steht vor dem Scale-up. Die folgenden vier Dimensionen sind kritisch:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    BEATRIX FEASIBILITY MATRIX                               │
├───────────────────────────────────┬─────────────────────────────────────────┤
│         TECHNISCH                 │           MENSCHLICH                    │
│                                   │                                         │
│  ┌───────────────────────────┐    │    ┌───────────────────────────┐       │
│  │ D1: SKALIERBARKEIT        │    │    │ D3: NUTZERAKZEPTANZ       │       │
│  │ Kann die γ-Matrix für     │    │    │ Vertrauen Manager den     │       │
│  │ 100+ Nutzer berechnet     │    │    │ KI-gestützten             │       │
│  │ werden?                   │    │    │ Empfehlungen?             │       │
│  │                           │    │    │                           │       │
│  │ → Prof. Gall (UZH)        │    │    │ → Prof. Luger (UZH)       │       │
│  └───────────────────────────┘    │    └───────────────────────────┘       │
│                                   │                                         │
│  ┌───────────────────────────┐    │    ┌───────────────────────────┐       │
│  │ D2: REPRODUZIERBARKEIT    │    │    │ D4: CHANGE-FÄHIGKEIT      │       │
│  │ Liefert die LLMMC-        │    │    │ Können Organisationen     │       │
│  │ Pipeline konsistente      │    │    │ BEATRIX erfolgreich       │       │
│  │ Ergebnisse?               │    │    │ adoptieren?               │       │
│  │                           │    │    │                           │       │
│  │ → Prof. Gall (UZH)        │    │    │ → Prof. Luger (UZH)       │       │
│  └───────────────────────────┘    │    └───────────────────────────┘       │
│                                   │                                         │
├───────────────────────────────────┴─────────────────────────────────────────┤
│                          Validierung: CHF 15'000 / 125h                     │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 1.2 Dimension 1: Technische Skalierbarkeit

### Was ist das Problem?

Die **Komplementaritätsmatrix Γ** ist das Herzstück von BEATRIX:
- 144×144 = 20'736 potenzielle Interaktionen
- Jede Berechnung erfordert Zugriff auf 1'922 Papers
- Multiple LLM-Calls pro Parameter

### Die kritische Frage

> Kann BEATRIX 100+ gleichzeitige Nutzer bedienen, ohne dass Latenz und Kosten explodieren?

### Was wir bereits wissen

| Aspekt | Status | Evidenz |
|--------|--------|---------|
| **Single-User Performance** | ✅ Validiert | <2s Antwortzeit |
| **Kleines Team (5 User)** | ✅ Validiert | Pilotprojekte erfolgreich |
| **Enterprise-Scale (50+ User)** | ❓ Unbekannt | Keine Tests |
| **Multi-Tenant Architektur** | ❓ Konzeptionell | Nicht implementiert |

### Was Prof. Gall validiert

1. **Architektur-Review:** Ist die aktuelle Architektur skalierbar?
2. **Benchmarking:** Performance unter Last (10, 50, 100 User)
3. **Empfehlungen:** Roadmap zur Produktions-Architektur

### Erwartete Ergebnisse

| Szenario | Wahrscheinlichkeit | Konsequenz |
|----------|-------------------|------------|
| **GO:** Architektur ist skalierbar | 60% | Direkt zum Produkt-Launch |
| **PILOT:** Mit Anpassungen skalierbar | 30% | 3-6 Monate Entwicklung |
| **NO-GO:** Fundamental limitiert | 10% | Architektur-Neuaufbau nötig |

---

## 1.3 Dimension 2: Pipeline-Reproduzierbarkeit

### Was ist das Problem?

Die **LLM Monte Carlo (LLMMC)** Pipeline schätzt Parameter:
- N=100+ LLM-Durchläufe pro Parameter
- Literatur-Kontext muss korrekt eingebunden werden
- Updates müssen systematisch integriert werden

### Die kritische Frage

> Liefert die Pipeline bei wiederholter Ausführung konsistente Ergebnisse?

### Was wir bereits wissen

| Aspekt | Status | Evidenz |
|--------|--------|---------|
| **Interne Konsistenz** | ✅ Gut | Std < 0.05 bei N=100 |
| **Externe Validierung** | ✅ Gut | MAE = 0.034 vs. Literatur |
| **Reproduzierbarkeit** | ❓ Nicht systematisch getestet | Anekdotisch konsistent |
| **Update-Prozess** | ❓ Manuell | Nicht dokumentiert |

### Was Prof. Gall validiert

1. **Code-Review:** Ist die Pipeline robust implementiert?
2. **Reproduzierbarkeits-Tests:** Gleiche Inputs → gleiche Outputs?
3. **CI/CD-Empfehlungen:** Wie systematisieren?

### Erwartete Ergebnisse

| Szenario | Wahrscheinlichkeit | Konsequenz |
|----------|-------------------|------------|
| **GO:** Pipeline robust | 70% | Qualitätssiegel für Parameter |
| **PILOT:** Verbesserungen nötig | 25% | 1-2 Monate Entwicklung |
| **NO-GO:** Fundamental instabil | 5% | Methodik überdenken |

---

## 1.4 Dimension 3: Nutzerakzeptanz

### Was ist das Problem?

BEATRIX liefert KI-gestützte Empfehlungen. Aber:
- Vertrauen Manager KI-Empfehlungen?
- Wie beeinflusst der Denkstil (φ) die Akzeptanz?
- Ist die Handlungsschwelle (θ) höher oder niedriger?

### Die kritische Frage

> Setzen Manager BEATRIX-Empfehlungen tatsächlich um, oder bleiben sie skeptisch?

### Was wir bereits wissen

| Aspekt | Status | Evidenz |
|--------|--------|---------|
| **Expert-User Akzeptanz** | ✅ Hoch | FehrAdvice-Berater nutzen es |
| **C-Level Akzeptanz** | ❓ Gemischt | Anekdotisch variabel |
| **Denkstil-Einfluss (φ)** | ❓ Unbekannt | Keine systematische Studie |
| **Schwellen-Effekt (θ)** | ❓ Unbekannt | Keine Human-AI Daten |

### Was Prof. Luger validiert

1. **Nutzer-Tests:** 10-15 Führungskräfte
2. **φ-Messung:** Denkstil-Diagnose
3. **θ-Messung:** Umsetzungswahrscheinlichkeit
4. **A/B-Tests:** Verschiedene Präsentationsformate

### Erwartete Ergebnisse

| Szenario | Wahrscheinlichkeit | Konsequenz |
|----------|-------------------|------------|
| **GO:** Hohe Akzeptanz | 50% | Direkt zum Markt |
| **PILOT:** Präsentation anpassen | 40% | UX-Optimierung |
| **NO-GO:** Fundamentale Skepsis | 10% | Hybrid-Modell (Mensch + KI) |

---

## 1.5 Dimension 4: Change-Fähigkeit

### Was ist das Problem?

Selbst wenn BEATRIX akzeptiert wird, muss es in Organisationen **adoptiert** werden:
- Welche BCJ-Phase ist kritisch?
- Welche Change-Interventionen helfen?
- Wie lange dauert die Adoption?

### Die kritische Frage

> Können Organisationen BEATRIX erfolgreich in ihre Prozesse integrieren?

### Was wir bereits wissen

| Aspekt | Status | Evidenz |
|--------|--------|---------|
| **Pilot-Projekte** | ✅ Erfolgreich | 3 abgeschlossene Projekte |
| **Langfrist-Nutzung** | ❓ Unbekannt | Zu früh für Daten |
| **Change-Barrieren** | ❓ Qualitativ bekannt | Nicht systematisiert |
| **Erfolgsfaktoren** | ❓ Anekdotisch | Nicht validiert |

### Was Prof. Luger validiert

1. **BCJ-Diagnose:** In welcher Phase scheitert Adoption?
2. **Barrieren-Analyse:** Was blockiert?
3. **Enabler-Analyse:** Was hilft?
4. **Change-Strategie:** Empfehlungen für Rollout

### Erwartete Ergebnisse

| Szenario | Wahrscheinlichkeit | Konsequenz |
|----------|-------------------|------------|
| **GO:** Klarer Adoptionspfad | 40% | Rollout-Playbook |
| **PILOT:** Spezifische Barrieren | 50% | Gezielte Interventionen |
| **NO-GO:** Systemische Blockade | 10% | Produkt-Pivot nötig |

---

# Abschnitt 2: Was kann mit CHF 15'000 erreicht werden?

## 2.1 Budget-Allokation

| Arbeitspaket | Stunden | Stundensatz | Total |
|--------------|---------|-------------|-------|
| **Gall: Architektur-Analyse** | 40 | CHF 120 | CHF 4'800 |
| **Gall: Pipeline-Review** | 15 | CHF 120 | CHF 1'800 |
| **Luger: Nutzer-Tests** | 40 | CHF 120 | CHF 4'800 |
| **Luger: BCJ-Analyse** | 15 | CHF 120 | CHF 1'800 |
| **Integration & Reporting** | 15 | CHF 120 | CHF 1'800 |
| **Total** | **125** | — | **CHF 15'000** |

---

## 2.2 Konkrete Deliverables

### Deliverable 1: Technical Feasibility Report (Gall)

| Element | Beschreibung |
|---------|--------------|
| **Umfang** | 15-20 Seiten + Benchmarking-Daten |
| **Inhalt** | Architektur-Bewertung, Skalierbarkeits-Tests, Pipeline-Review |
| **Output** | GO/PILOT/NO-GO mit konkreten Empfehlungen |
| **Timeline** | 6 Wochen |

### Deliverable 2: Adoption Feasibility Report (Luger)

| Element | Beschreibung |
|---------|--------------|
| **Umfang** | 15-20 Seiten + Nutzer-Daten |
| **Inhalt** | Akzeptanz-Analyse, BCJ-Diagnose, Change-Strategie |
| **Output** | GO/PILOT/NO-GO mit Rollout-Empfehlungen |
| **Timeline** | 6 Wochen |

### Deliverable 3: Integrated Feasibility Assessment

| Element | Beschreibung |
|---------|--------------|
| **Umfang** | 5-10 Seiten Executive Summary |
| **Inhalt** | Synthese beider Reports, Gesamtbewertung |
| **Output** | GO/PILOT/NO-GO Entscheidungsgrundlage |
| **Timeline** | 2 Wochen nach Einzelreports |

---

## 2.3 Was CHF 15'000 NICHT leisten kann

| Aspekt | Was möglich ist | Was NICHT möglich ist |
|--------|-----------------|----------------------|
| **Architektur** | Bewertung & Empfehlungen | Implementierung |
| **Pipeline** | Review & Best Practices | Neuaufbau |
| **Nutzer-Tests** | 10-15 Personen | Repräsentative Studie |
| **Change** | Qualitative Analyse | Longitudinale Studie |

**Wichtig:** Das Innovation Cheque Projekt liefert die **Entscheidungsgrundlage**, nicht die **Implementierung**.

---

# Abschnitt 3: Wie reduziert die Forschung die Risiken?

## 3.1 Risiko-Matrix vor und nach Studie

### Technisches Risiko (Gall)

| Risiko | Vor Studie | Nach Studie (erwartet) |
|--------|------------|------------------------|
| **Skalierbarkeit scheitert** | Hoch (keine Daten) | Niedrig (Benchmarks) |
| **Architektur-Fehler** | Mittel (nicht reviewt) | Niedrig (Expert-Review) |
| **Pipeline instabil** | Mittel (nicht getestet) | Niedrig (Reproduzierbarkeit) |
| **Kosten explodieren** | Hoch (nicht modelliert) | Niedrig (Projektion) |

**Risiko-Reduktion:** 60-70%

### Marktrisiko (Luger)

| Risiko | Vor Studie | Nach Studie (erwartet) |
|--------|------------|------------------------|
| **Manager vertrauen nicht** | Hoch (keine Daten) | Niedrig (validiert) |
| **Denkstil-Mismatch** | Mittel (nicht untersucht) | Niedrig (φ-Profile) |
| **Adoption scheitert** | Hoch (keine Strategie) | Mittel (BCJ-Analyse) |
| **Change-Widerstand** | Hoch (nicht analysiert) | Niedrig (Barrieren bekannt) |

**Risiko-Reduktion:** 50-60%

---

## 3.2 Entscheidungsbaum nach Studie

```
                            ┌─────────────────────────────────────┐
                            │    STUDIE ABGESCHLOSSEN             │
                            │    (nach 3-6 Monaten)               │
                            └─────────────────────────────────────┘
                                           │
                    ┌──────────────────────┼──────────────────────┐
                    │                      │                      │
                    ▼                      ▼                      ▼
           ┌───────────────┐      ┌───────────────┐      ┌───────────────┐
           │     GO        │      │    PILOT      │      │    NO-GO      │
           │  (40% erw.)   │      │  (50% erw.)   │      │  (10% erw.)   │
           └───────────────┘      └───────────────┘      └───────────────┘
                    │                      │                      │
                    ▼                      ▼                      ▼
           ┌───────────────┐      ┌───────────────┐      ┌───────────────┐
           │ Direkt zum    │      │ Gezielte      │      │ Fundamental   │
           │ Scale-up      │      │ Verbesserungen│      │ überdenken    │
           │               │      │ (3-6 Monate)  │      │               │
           │ → Innosuisse  │      │ → dann GO     │      │ → Pivot oder  │
           │   Hauptprojekt│      │               │      │   Stopp       │
           └───────────────┘      └───────────────┘      └───────────────┘
```

---

## 3.3 Return on Investment der Studie

### Szenario-Analyse

| Szenario | P | Kosten ohne Studie | Kosten mit Studie | Ersparnis |
|----------|---|--------------------|--------------------|-----------|
| **GO (hätten sowieso gebaut)** | 40% | CHF 0 | CHF 15k | -CHF 15k |
| **PILOT (hätten falsch gebaut)** | 50% | CHF 100k (Rework) | CHF 15k + 50k | CHF 35k |
| **NO-GO (hätten Geld verbrannt)** | 10% | CHF 300k (Fail) | CHF 15k | CHF 285k |

**Erwartungswert der Ersparnis:**
```
E(Ersparnis) = 0.4 × (-15k) + 0.5 × 35k + 0.1 × 285k
             = -6k + 17.5k + 28.5k
             = CHF 40'000
```

**ROI der Studie:** 267% (CHF 40k Erwartungswert / CHF 15k Investment)

---

# Abschnitt 4: Was sind die nächsten Schritte nach GO?

## 4.1 Roadmap bei GO

### Phase 1: MVP Refinement (Monate 1-3)

| Aktivität | Beschreibung | Ressourcen |
|-----------|--------------|------------|
| **Architektur-Update** | Gall-Empfehlungen implementieren | 2 Entwickler |
| **UX-Optimierung** | Luger-Empfehlungen umsetzen | 1 UX Designer |
| **Dokumentation** | User Guides, API Docs | 1 Technical Writer |

### Phase 2: Pilot-Programm (Monate 4-6)

| Aktivität | Beschreibung | Ressourcen |
|-----------|--------------|------------|
| **5-10 Pilot-Kunden** | Strukturierte Tests | Sales + CS |
| **Feedback-Integration** | Iterative Verbesserung | Dev Team |
| **Pricing-Validation** | Zahlungsbereitschaft testen | Strategy |

### Phase 3: Market Launch (Monate 7-12)

| Aktivität | Beschreibung | Ressourcen |
|-----------|--------------|------------|
| **Go-to-Market** | Marketing-Kampagne | Marketing |
| **Sales-Team** | Aufbau Vertrieb | 2-3 Sales |
| **Customer Success** | Onboarding, Support | 1-2 CS |

---

## 4.2 Folge-Finanzierung

### Option A: Innosuisse Innovationsprojekt

| Aspekt | Details |
|--------|---------|
| **Typ** | Hauptprojekt mit Forschungspartner |
| **Budget** | CHF 200k-500k |
| **Dauer** | 12-24 Monate |
| **Fokus** | Produktentwicklung + Wissenschaft |
| **Wahrscheinlichkeit** | Hoch (bei GO aus Cheque-Studie) |

### Option B: Venture Capital

| Aspekt | Details |
|--------|---------|
| **Runde** | Seed (CHF 1-3M) |
| **Investoren** | Swiss VCs (Redalpine, Lakestar) |
| **Dauer** | 18-24 Monate Runway |
| **Fokus** | Skalierung |
| **Wahrscheinlichkeit** | Mittel (abhängig von Traction) |

### Option C: Corporate Partnership

| Aspekt | Details |
|--------|---------|
| **Partner** | Consulting-Firmen, HR-Tech |
| **Modell** | White-Label, Revenue Share |
| **Volumen** | CHF 100k-500k/Jahr |
| **Fokus** | Marktdurchdringung |
| **Wahrscheinlichkeit** | Mittel-Hoch |

---

## 4.3 Meilensteine nach GO

| Zeitpunkt | Meilenstein | Erfolgskriterium |
|-----------|-------------|------------------|
| **Monat 3** | MVP 2.0 ready | Gall-Empfehlungen umgesetzt |
| **Monat 6** | 10 Pilot-Kunden | NPS > 50 |
| **Monat 9** | First Revenue | ARR > CHF 100k |
| **Monat 12** | Product-Market Fit | 50+ zahlende Kunden |
| **Monat 18** | Scale-up | ARR > CHF 500k |
| **Monat 24** | Profitabilität | Break-even erreicht |

---

# Zusammenfassung: Feasibility & Risk Reduction

## Die vier Kernaussagen

### 1. Kritische Unsicherheiten identifiziert

> Vier Dimensionen müssen validiert werden: Skalierbarkeit (Gall), Reproduzierbarkeit (Gall), Nutzerakzeptanz (Luger), Change-Fähigkeit (Luger).

### 2. Realistische Deliverables

> Mit CHF 15'000 liefern wir drei Reports: Technical Feasibility (Gall), Adoption Feasibility (Luger), Integrated Assessment — als GO/PILOT/NO-GO Entscheidungsgrundlage.

### 3. Signifikante Risiko-Reduktion

> 60-70% technische Risiko-Reduktion, 50-60% Markt-Risiko-Reduktion — bei einem ROI von 267%.

### 4. Klare Next Steps

> Bei GO: 12-Monats-Roadmap zu Product-Market Fit, mit Optionen für Innosuisse Hauptprojekt, VC, oder Corporate Partnership.

---

## Feasibility auf einen Blick

| Dimension | Frage | Wer validiert | Erwartung |
|-----------|-------|---------------|-----------|
| **Skalierbarkeit** | 100+ User möglich? | Gall | GO: 60% |
| **Reproduzierbarkeit** | Pipeline robust? | Gall | GO: 70% |
| **Akzeptanz** | Manager vertrauen? | Luger | GO: 50% |
| **Adoption** | Organisationen können? | Luger | GO: 40% |
| **Gesamt** | Scale-up möglich? | Beide | GO: ~40%, PILOT: ~50% |

---

## Verweise auf andere Fragen

| Frage | Relevanter Inhalt |
|-------|-------------------|
| **a) Innovation** | Was genau validiert wird (8Ψ, γ-Matrix, LLMMC) |
| **b) Market** | Warum Validierung wichtig ist (SAM, Zielgruppen) |
| **d) Partner** | Detaillierte Arbeitspakete Gall + Luger |
| **e) Switzerland** | Langfrist-Impact bei erfolgreicher Validierung |

---

*Dokument erstellt: 2026-01-18*
*Version: 5.0 (Überarbeitet nach Qualitätsframework)*
*Änderungen v5.0: Executive Summary, Cross-References*
