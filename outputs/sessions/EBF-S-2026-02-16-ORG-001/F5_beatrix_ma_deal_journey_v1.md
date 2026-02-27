# BEATRIX × M&A: Behavioral Deal Journey

**Session:** EBF-S-2026-02-16-ORG-001
**Modell:** MOD-MA-001 (M&A Behavioral Deal Journey Model v1.0)
**Datum:** 2026-02-16
**Modus:** STANDARD

---

## Executive Summary

BEATRIX ermoeglicht eine systematische verhaltensorekonomische Analyse entlang der gesamten M&A Deal Journey. Das Modell MOD-MA-001 strukturiert 7 Produkte in 6 Deal-Phasen und quantifiziert verhaltensorekonomische Risiken, die klassische Due-Diligence-Prozesse nicht erfassen. Das Flaggschiff-Produkt **Behavioral Due Diligence (BDD)** ergaenzt Financial, Legal und Tax DD um eine fuenfte Pruefungsdimension.

**Kernerkenntnis:** 70% der M&A-Misserfolge sind auf kulturelle Inkompatibilitaet zurueckzufuehren (Weber & Camerer 2003). BEATRIX quantifiziert diese Risiken ueber Psi-Distanzen, gamma-Interaktionen und kontextabhaengige Parameter (lambda, beta).

---

## 1. Deal Journey: 6 Phasen × BEATRIX

### Phase 1: Origination — Investment Thesis Validation

**M&A-Kontext:** Strategische Rationale pruefen, Target Universe definieren, Go/No-Go Entscheidung vorbereiten.

**Verhaltensorekonomische Risiken:**

| Risiko | Parameter | Quelle | Impact |
|--------|-----------|--------|--------|
| CEO Overconfidence | +65% Akquisitionsneigung | Malmendier & Tate (2008) | Zu viele/zu teure Deals |
| Empire Building | U_Identity > U_Shareholder | Akerlof & Kranton (2000) | Wertvernichtende Deals |
| Anchoring auf Synergien | Literatur-Prior: 40-60% Realisierung | KPMG (2019) | Ueberbewertung |
| Strategy Cannibalization | gamma_MA+INNOV = -0.22 | SOCM-1.0 (ALPLA) | Innovation stirbt |

**BEATRIX-Deliverables:**
1. **Overconfidence Score** des Investitionskomitees (Skala 0-1, Threshold 0.6)
2. **gamma-Matrix:** Welche bestehenden Strategien verstaerkt/zerstoert M&A?
3. **Identity Fit Score:** Ist M&A kongruent mit der Unternehmensidentitaet?
4. **Go/No-Go:** Behavioral Risk Rating (Low/Medium/High/Critical)

**Praxis-Referenz ALPLA:**
```
SOCM-1.0 Ergebnis:
  M&A Utility         = 0.615 (Rang 6 von 6 Strategieoptionen)
  Circular Economy     = 0.795 (Rang 1)
  Innovation           = 0.775 (Rang 2)

  gamma_MA+INNOV = -0.22 (staerkster negativer Effekt)
  gamma_MA+SCALE = +0.20 (einzige positive Synergie)

  Empfehlung: M&A nur als taktische Ergaenzung, nicht Kernstrategie
  Erfolgswahrscheinlichkeit: 65% (mit M&A) vs. 82% (ohne M&A)
```

---

### Phase 2: Screening — Cultural Fit Assessment

**M&A-Kontext:** Longlist → Shortlist, Indicative Offers, Teaser/NDA-Phase.

**BEATRIX-Mehrwert:** Traditionelle Screenings fokussieren auf Financials und Markt. BEATRIX ergaenzt die **verhaltensorekonomische Kompatibilitaetspruefung**.

**Methodik: Psi-Distanzmessung**

Fuer Acquirer und jedes Target werden 8 Kontextdimensionen gemessen:

```
Psi-Dimensionen (pro Unternehmen):
  Psi_I: Regeln & Governance (formell vs. informell)
  Psi_S: Soziale Struktur (hierarchisch vs. flach)
  Psi_K: Unternehmenskultur (konservativ vs. agil)
  Psi_C: Kognitive Muster (analytisch vs. intuitiv)
  Psi_E: Ressourcenallokation (zentral vs. dezentral)
  Psi_T: Zeitkultur (langfristig vs. kurzfristig)
  Psi_M: Tooling & Prozesse (standardisiert vs. ad hoc)
  Psi_F: Raeumliche Struktur (zentralisiert vs. verteilt)
```

**Distanzberechnung:**
```
d(Acquirer, Target) = sqrt( sum_i (Psi_i_Acq - Psi_i_Tgt)^2 )

Benchmarks:
  d < 0.30: Low friction (Smooth Integration expected)
  d = 0.30-0.60: Medium friction (Managed Integration required)
  d = 0.60-0.90: High friction (Intensive Integration Management)
  d > 0.90: Critical friction (Integration failure likely)
```

**BEATRIX-Deliverables:**
1. **Psi-Distanzmatrix** (Acquirer vs. 3-5 Targets, 8 Dimensionen)
2. **CVA-Schnellprofil** pro Target (30 Faktoren, 2-4h Aufwand)
3. **Stakeholder Reaction Forecast** (7-Persona Simulation pro Target)
4. **Cultural Integration Difficulty Score** (CIDS: Low/Medium/High/Critical)

---

### Phase 3: Due Diligence — Behavioral Due Diligence (BDD)

**M&A-Kontext:** Parallel zu Financial, Legal, Tax und Commercial DD.

Dies ist das **Flaggschiff-Produkt** — die groesste Differenzierung gegenueber klassischen M&A-Beratern.

#### BDD-Modul 1: Leadership Assessment

**Ziel:** Verhaltensprofilierung des Target-Managements.

| Dimension | Messung | Threshold | Risiko |
|-----------|---------|-----------|--------|
| Overconfidence | Malmendier/Tate Score | > 0.6 | Ueberschaetzte Projections |
| Risikoverhalten | SBDMS-1.0 Risk Appetite | > 0.7 | Hidden Risk Exposure |
| Identitaetskongruenz | Identity Fit Acquirer ↔ Target | < 0.4 | Post-Deal Konflikte |
| Decision Quality | SBDMS-1.0 Board Effectiveness | < 0.5 | Governance-Defizite |

**Methodik:** SBDMS-1.0 wird auf das Target-Board kalibriert. Inputs: oeffentliche Daten, Management-Praesentationen, Expert Calls.

#### BDD-Modul 2: Cultural Compatibility

**Ziel:** Quantifizierte Kulturvergleichsanalyse.

| Dimension | Acquirer | Target | Delta | Risiko |
|-----------|----------|--------|-------|--------|
| Psi_I (Governance) | 0.75 | 0.40 | 0.35 | ⚠️ Regelkonflikte |
| Psi_S (Hierarchie) | 0.60 | 0.80 | 0.20 | OK |
| Psi_K (Kultur) | 0.55 | 0.30 | 0.25 | ⚠️ Wertekonflikte |
| ... | ... | ... | ... | ... |
| **d(Gesamt)** | | | **0.52** | **Medium Friction** |

**Methodik:** CVA-Schnellprofil (30 Faktoren) oder CVA-Standard (400 Faktoren) je nach Deal-Groesse.

#### BDD-Modul 3: Organizational Resilience

**Ziel:** Veraenderungsfaehigkeit des Targets messen.

**BCJ-Assessment:** In welcher Change-Phase befindet sich die Target-Organisation?

```
BCJ-Phase-Distribution (Beispiel Target):
  UNAWARE:    15% der Organisation
  AWARE:      35% der Organisation
  WILLING:    30% der Organisation
  ACTING:     15% der Organisation
  MAINTAINING: 5% der Organisation

  Resilience Score = 0.55 (Mittel)
  → Organisation ist mehrheitlich AWARE aber noch nicht WILLING
  → Integration wird 6-12 Monate mehr brauchen als geplant
```

#### BDD-Modul 4: Complementarity Risk Map

**Ziel:** Wo zerstoert die Integration Wert?

```
gamma-Analyse (Beispiel):
  gamma(Target_R&D + Acquirer_Scale) = +0.15    Synergie
  gamma(Target_Culture + Acquirer_Process) = -0.30  RISIKO
  gamma(Target_Talent + Financial_Incentives) = -0.20  Crowding-Out
  gamma(Target_Brand + Acquirer_Brand) = +0.10    Leichte Synergie

  Kritische Interaktion: Kultur × Prozess (-0.30)
  → Standardisierung der Prozesse bedroht Target-Innovationskultur
  → Empfehlung: Geschuetzte Autonomie fuer R&D-Einheit
```

#### BDD-Modul 5: Stakeholder Impact Analysis

**Ziel:** Wie reagieren die wichtigsten Stakeholder?

**Methodik:** `/simulate-stakeholder` mit 7 Personas:

| Persona | Reaktion | Risiko | Intervention |
|---------|----------|--------|--------------|
| Target CEO | Ambivalent (Exit-Optionalitaet vs. Legacy) | Flight Risk 40% | Advisory Board + Naming |
| Target CTO | Negativ (Autonomieverlust) | Flight Risk 65% | Geschuetzte Autonomie |
| Betriebsrat | Sehr negativ (Arbeitsplatzsicherheit) | Blockade-Risiko | Standortgarantie 3 Jahre |
| Key Customers | Verunsichert (Ansprechpartner?) | Revenue Risk 15% | Persoenliche Zusicherung |
| Regulatoren | Neutral-positiv | Genehmigungsrisiko 10% | Early Engagement |
| Lieferanten | Verunsichert (Konditionen?) | Supply Risk 8% | Vertragsverlaengerung |
| Acquirer-Team | Ueberlastet (Double Duty) | Burnout Risk 30% | Dedicated Integration Team |

---

### Phase 4: Execution — Transaction Advisory (Behavioral)

**M&A-Kontext:** SPA-Verhandlung, Kaufpreisfindung, Earn-Out Design.

**Kontextabhaengige Verlustaversion des Verkaeufers:**

```
lambda_seller = f(Psi_K, Psi_S, Psi_T)

Benchmarks:
  Familienunternehmer (Gruender):        lambda = 3.5
  Familienunternehmer (2. Generation):   lambda = 2.8
  PE Exit (Fondsende):                   lambda = 1.8
  Corporate Carve-Out:                   lambda = 2.2
  Distressed Sale:                       lambda = 1.5

Implikation (Beispiel: Familienunternehmer, 2. Generation):
  Preisnachlass von 10% wird als lambda x 10% = 28% Verlust empfunden
  → Non-Monetary Bridges noetig: Naming Rights, Advisory Board, Vermaechtnis-Sicherung
```

**Earn-Out Design (Present Bias adjustiert):**

```
beta_earnout: Zeitliche Diskontierung durch Verkaeufer

  Gruender (optimistisch):     beta = 0.85  → akzeptiert Earn-Out eher
  PE (rational):               beta = 0.95  → Earn-Out fast zum Nennwert
  Manager (risikoavers):       beta = 0.70  → Earn-Out stark abgewertet

Implikation:
  Ein Earn-Out von CHF 10M in 3 Jahren wird von einem risikoaversen
  Manager als CHF 10M x 0.70^3 = CHF 3.4M wahrgenommen
  → Entweder hoehere Earn-Out Summe oder kuerzere Laufzeit
```

**BEATRIX-Deliverables:**
1. **Seller Behavioral Profile** (lambda, beta, Fairness-Praeferenzen)
2. **Behavioral Negotiation Playbook** (Anchoring, Framing, Sequencing)
3. **Non-Monetary Value Bridge Design** (Legacy, Naming, Advisory)
4. **Fairness Score** der Deal-Struktur (Fehr/Schmidt Inequity Aversion)

---

### Phase 5: Closing — Day-1 Readiness Program

**M&A-Kontext:** Signing bis Day 1 + 30 Tage.

**Prinzip: Defaults sind maechtig.**

```
Choice Architecture am Day 1:

  DEFAULTS setzen (Opt-out statt Opt-in):
  ├── Neue Org-Struktur als Default (wer NICHT zugestimmt hat, muss aktiv widersprechen)
  ├── Neue Email-Domain als Default (alte leitet automatisch um)
  ├── Neue Reporting Lines als Default
  └── Neue Benefits als Default (mit Besitzstandswahrung)

  SALIENZ steuern (was faellt zuerst auf?):
  ├── BEHALTEN: Kantine, Parkplaetze, Pausenraeume (hohe taegliche Salienz)
  ├── AENDERN:  Logo, Brand, externe Kommunikation (strategisch wichtig)
  ├── VERZOEGERN: IT-Migration, ERP-Wechsel (disruptiv, nicht sichtbar)
  └── SOFORT:   CEO-Video, Town Hall, Welcome Package (Signal der Wertschaetzung)

  FRAMING der Ankuendigung:
  ├── Deskriptive Norm: «85% der Kolleg:innen sehen Chancen in der Fusion»
  ├── NICHT: Angst-Kommunikation («Veraenderung wird hart»)
  ├── Gain Frame: «Was wir gemeinsam erreichen koennen»
  └── NICHT: Loss Frame: «Was sich alles aendern wird»
```

**BEATRIX-Deliverables:**
1. **Day-1 Choice Architecture Blueprint** (15+ Default-Entscheidungen)
2. **Announcement Framing Scripts** (CEO-Ansprache, Townhall, Email)
3. **Salienz-Priorisierung** (Was aendern / behalten / verzoegern)
4. **Retention Nudge Toolkit** (Stay-Boni, Commitment Devices)
5. **Quick Win Roadmap** (erste 30 Tage: sichtbare Verbesserungen)

---

### Phase 6: Integration — Behavioral Integration Management (BIM) + Value Creation Tracking

**M&A-Kontext:** Post-Merger Integration ueber 24-36 Monate.

**BCJ × PMI Phasen-Mapping:**

```
┌──────────────┬───────────────┬────────────────────────────────────┬───────┐
│ BCJ-Phase    │ PMI-Zeitraum  │ BEATRIX-Intervention               │ alpha │
├──────────────┼───────────────┼────────────────────────────────────┼───────┤
│ UNAWARE      │ Monat 0-1     │ Town Halls, CEO Cascades           │ 0.85  │
│              │               │ «Warum diese Fusion?» Narrativ     │       │
│ AWARE        │ Monat 1-3     │ Information Sessions, Q&A          │ 0.78  │
│              │               │ Feedback Loops, Concern Mapping    │       │
│ WILLING      │ Monat 3-6     │ Quick Wins, Joint Project Teams    │ 0.72  │
│              │               │ Cross-Pollination Events           │       │
│ ACTING       │ Monat 6-18    │ Prozessintegration, KPI Alignment  │ 0.68  │
│              │               │ Shared Services, System Migration  │       │
│ MAINTAINING  │ Monat 18-36   │ Kultur-Rituale, Annual Reviews     │ 0.75  │
│              │               │ Alumni Programs, Identity Building │       │
└──────────────┴───────────────┴────────────────────────────────────┴───────┘
```

**Monitoring-Dashboard (monatlich):**

| Metrik | Messung | Zielwert | Warnschwelle |
|--------|---------|----------|--------------|
| Psi-Distanz (Kultur) | CVA Delta | Konvergenz → 0 | Divergenz > +0.05/Monat |
| Synergy Realization | Plan vs. Ist | ≥ 60% | < 40% |
| Key Talent Attrition | Freiwillige Kuendigungen | < 10% p.a. | > 15% p.a. |
| Employee Engagement | Pulse Survey | > 65% | < 50% |
| Integration Milestones | On Track / Delayed | > 80% on track | < 60% on track |

**Value Creation Tracking (Jahre 1-5):**

```
Bayesian Synergy Tracking:
  Prior (aus BDD):       Synergien = CHF 50M p.a. [CI: 25-75M]
  Year 1 Observation:    Realisiert = CHF 18M
  Posterior Update:       Synergien = CHF 42M p.a. [CI: 28-56M]
  Brier Score Year 1:    0.12 (Unterschaetzung der Integrationskosten)

  Year 2 Observation:    Realisiert = CHF 35M (kumuliert: 53M)
  Posterior Update:       Synergien = CHF 48M p.a. [CI: 38-58M]

  → Lessons Learned: Integrationskosten Year 1 systematisch unterschaetzt
  → Parameter-Update: Integration Cost Factor +15% fuer naechsten Deal
```

---

## 2. Differenzierung: BEATRIX vs. Klassische M&A-Beratung

| Dimension | Klassisch | BEATRIX |
|-----------|-----------|---------|
| **DD-Scope** | Financial, Legal, Tax, Commercial | + Behavioral (5 Module) |
| **Kultur** | Qualitative Interviews | Quantifiziert: Psi-Distanz, 8 Dimensionen |
| **Synergien** | Top-down, oft 100% angenommen | Bayesian: Literatur-Prior 40-60%, kontextadjustiert |
| **Verhandlung** | Erfahrungsbasiert | Parameterbasiert: lambda, beta, gamma |
| **Integration** | Generische Checklisten | BCJ-phasengerecht, andere Interventionen pro Phase |
| **Monitoring** | Quartalsweise Reviews | Monatliches Psi-Tracking + Bayesian Updates |
| **Learning** | Ad hoc | Systematisch: Parameter fliessen in naechsten Deal |

---

## 3. Produktportfolio-Uebersicht

| # | Produkt | Phase | Kern-Deliverable | Dauer | Pricing |
|---|---------|-------|-------------------|-------|---------|
| 1 | **Investment Thesis Validation** | Origination | Overconfidence Score + gamma-Matrix | 1-2 Wo. | Fixed Fee |
| 2 | **Cultural Fit Assessment** | Screening | Psi-Distanzmatrix + CVA-Profil | 2-3 Wo./Target | Per Target |
| 3 | **Behavioral Due Diligence (BDD)** | Due Diligence | 5-Modul BDD Report | 4-6 Wo. | Fixed + Success |
| 4 | **Transaction Advisory (Behavioral)** | Execution | Seller Profile + Negotiation Playbook | 2-4 Wo. | Retainer + Success |
| 5 | **Day-1 Readiness Program** | Closing | Choice Architecture + Framing Scripts | 2-3 Wo. | Fixed Fee |
| 6 | **Behavioral Integration Mgmt (BIM)** | Integration | 24-Mo. Plan + Kultur-Dashboard | 24-36 Mo. | Monthly Retainer |
| 7 | **Value Creation Tracking** | Post-Integration | Synergy Tracker + Lessons Learned | 1-5 Jahre | Annual Fee |

---

## 4. Modell-Referenzen

| Modell | Anwendung in M&A |
|--------|-----------------|
| **SBDMS-1.0** | Board Decision Architecture, Overconfidence Screening |
| **SOCM-1.0** | Strategische Komplementaritaet, gamma-Matrix |
| **SDM-1.0** | 4-Phasen Organisationstransformation |
| **BCJ** | 5-Phasen Integration Journey |
| **CVA** | Kulturelle Kontextanalyse (30-400 Faktoren) |

## 5. Theorie-Basis

| Theorie | Autor | M&A-Anwendung |
|---------|-------|---------------|
| Overconfidence & Acquisitions | Malmendier & Tate (2008) | Investment Thesis Validation |
| Identity Economics | Akerlof & Kranton (2000) | Cultural Fit, Identity Conflict |
| Inequity Aversion | Fehr & Schmidt (1999) | Deal Fairness, Post-Deal Cooperation |
| Prospect Theory | Kahneman & Tversky (1979) | Seller Loss Aversion, Framing |
| Present Bias | Laibson (1997) | Earn-Out Design |
| Cultural Distance | Weber & Camerer (2003) | Psi-Distanzmessung |

## 6. gamma-Parameter (Komplementaritaeten)

| Paar | gamma | Bedeutung | M&A-Relevanz |
|------|-------|-----------|--------------|
| M&A × Innovation | -0.22 | Staerkster negativer Effekt | Target-Innovation erstes Integrationsopfer |
| M&A × Scale | +0.20 | Positive Synergie | Groessenvorteile realisierbar |
| Overconfidence × Premium | +0.35 | Hubris-Praemie | 65% mehr Akquisitionsneigung |
| Kulturdistanz × Integration | -0.45 | Cultural Friction | 70% der Misserfolge kulturbedingt |
| Social × Financial | -0.20 | Crowding-Out | Retention-Boni vs. Teamgeist |
| Fairness × Kooperation | +0.30 | Fairness-Dividende | Faire Deals → bessere Post-Deal-Kooperation |

---

*Erstellt: 2026-02-16 | Session: EBF-S-2026-02-16-ORG-001 | Modell: MOD-MA-001 v1.0*
