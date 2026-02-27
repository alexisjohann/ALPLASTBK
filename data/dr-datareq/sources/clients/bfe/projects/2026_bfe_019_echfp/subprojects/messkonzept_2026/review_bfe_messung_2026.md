# Review: BFE Messung 2026 — EnergieSchweiz für Private (ECHfP)

**Datum:** 2026-02-17
**Reviewer:** Claude (FehrAdvice EBF Framework)
**Branch:** claude/review-bfe-measurement-2026-GDRJs
**Geprüfte Dateien:** 14 YAML/MD-Dateien, ~9'000 Zeilen
**Programm:** ECHfP = «EnergieSchweiz für Private» (Nachfolger der Kampagne «erneuerbar heizen» 2021–2025)

---

## 1. Executive Summary

Das BFE-Messung-2026-Projekt vollzieht einen **Paradigmenwechsel** in der Wirkungsmessung des Programms **«EnergieSchweiz für Private» (ECHfP)**: Weg von reinem KPI-Tracking (Reichweite, Klicks, Conversion Rates), hin zur **verhaltensökonomischen Parameterextraktion** via Evidence-Based Framework (EBF). ECHfP ist der Nachfolger der Kampagne «erneuerbar heizen» (2021–2025), die primär den Heizungsersatz adressierte. ECHfP umfasst neu 5 Module: Gesamtmodernisierung, Gebäudehülle, Heizungsersatz, PV/Solarenergie und E-Mobilität — das gesamte Spektrum der energetischen Gebäudemodernisierung. Die Wirkung wird über das **Behavioral Impact System (BIS)** gemessen, das Awareness, Willingness, Impact und Trust zu einem Gesamtscore aggregiert.

### Kernbefunde

| Aspekt | Status | Bewertung |
|--------|--------|-----------|
| Paradigmenwechsel KPI → BCM | Konzipiert, dokumentiert | Exzellent |
| 10C-Abdeckung | 3/10 → 8/10 geplant | Stark |
| Behavioral Constructs | 2/6 → 6/6 geplant | Stark |
| Fragebogen v4 → v5 | 15 neue Fragen, +5-7 Min. | Durchführbar |
| Review-Kommentar-Management | 82 Kommentare systematisch bearbeitet | Professionell |
| Panel-Design | Konzipiert, noch nicht implementiert | Kritisch für Validierung |
| Installer-Tracking | Als Gap identifiziert, nicht operationalisiert | Kritische Lücke |
| STWE-Spezifik | 3 neue Fragen (F2B.1-3) | Angemessen |
| Literaturmapping | 28 Items → 47 Papers | Solide |

### Primäres Outcome-Ziel

Fossil → Erneuerbar Heizungsersatz-Rate von **65% → 75%** (+10 Prozentpunkte, +4'400 Heizungen/Jahr)

---

## 2. Architektur-Überblick

### 2.1 Drei-Schichten-Architektur

```
┌─────────────────────────────────────────────────────────────────┐
│  SCHICHT 1: Legacy Messkonzept «erneuerbar heizen» (2021-2025)  │
│  Matomo + GSC + Google Ads → Reichweite/Engagement/Konversion   │
│  KPI-Hierarchie: Besuche → Interaktionen → Impulsberatung      │
│  Limitation: Nur Heizungsersatz, keine kausale Attribution      │
└─────────────────────────────────────────────────────────────────┘
                              ↓ informiert
┌─────────────────────────────────────────────────────────────────┐
│  SCHICHT 2: ECHfP Behavioral Impact Cockpit (2026)              │
│  BIS: Awareness (25%) + Willingness (25%)                       │
│       + Impact (30%) + Trust (20%) = Behavioral Impact Score     │
│  Datenquelle: Intervista n=1'200/Welle, 3x/Jahr                │
│  Neu: 5 Module, BCJ-Phasen, Segment-Profile, BCM-Parameter     │
└─────────────────────────────────────────────────────────────────┘
                              ↓ parametrisiert
┌─────────────────────────────────────────────────────────────────┐
│  SCHICHT 3: EBF 10C Verhaltensmodell (model.yaml)              │
│  Segment-spezifische Parameter: β, λ, θ, W_base, u_FEPSDE     │
│  Intervention Vectors: →I ∈ [0,1]^9                             │
│  Portfolio-Optimierung mit 6 Constraints (C1-C6)                │
│  Predictions: Testbare Vorhersagen pro Segment                  │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Segment-Architektur

| Segment | β (Present Bias) | λ (Loss Aversion) | θ (Activation) | W_base | Hauptbarriere |
|---------|-------------------|---------------------|-----------------|--------|---------------|
| **SEG_EFH** | 0.82 | 2.1 | 0.65 | 0.35 | Kosten-Unsicherheit |
| **SEG_MFH** | 0.78 | 2.3 | 0.72 | 0.28 | Entscheidungskomplexität |
| **SEG_STWE** | 0.75 | 2.5 | 0.78 | 0.22 | Governance-Blockade |

### 2.3 Behavioral Customer Journey (BCJ)

```
unaware → aware → considering → intending → acting → maintaining
  φ=0      φ=1      φ=2          φ=3        φ=4       φ=5
```

Schlüsselübergänge:
- **φ=0→1** (unaware→aware): Kampagnen-Effekt, Information
- **φ=2→3** (considering→intending): Installer-Kontakt, Trigger-Events
- **φ=3→4** (intending→acting): **Intention-Behavior Gap** (Sheeran 2002: 28%)

---

## 3. Der Paradigmenwechsel: KPI-Score → BCM-Parameter

### 3.1 Was sich ändert

| Dimension | Bisherig (v4) | Neu (v5/EBF) |
|-----------|---------------|---------------|
| **Auswertungslogik** | Items → Score (0-100) | Items → Parameter (β, λ, σ, θ) |
| **Awareness** | A = Σ(A_items) / max | A_exposure, A_salience, A_personal_relevance |
| **Willingness** | W = Σ(W_items) / max | u_F, u_S, u_X, θ_inv, τ, σ_d |
| **Trust** | T = Σ(T_items) / max | Ψ_trust (5 Subdimensionen) |
| **Segmentierung** | Einstellungsbasiert | Verhaltensparametrisch (β, λ, θ) |

### 3.2 Warum das wichtig ist

Der bisherige Ansatz lieferte **deskriptive Scores**: «Awareness = 52 von 100». Der neue Ansatz liefert **kausale Parameter**: «β = 0.82 bedeutet, dass EFH-Eigentümer:innen zukünftige Einsparungen um 18% abdiskontieren.» Damit werden Interventionen **gezielt designbar**:

- β niedrig → Present-Bias-Intervention (Sofort-Rabatt statt Langfrist-ROI)
- λ hoch → Loss-Frame statt Gain-Frame
- σ_d niedrig → Soziale Normen aktivieren
- θ hoch → Trigger-Events nutzen (Heizungsausfall, Renovation)

### 3.3 Zentrale Erkenntnis

> «Der Fragebogen bleibt zu 99% identisch. Die wesentliche Änderung ist ein PARADIGMENWECHSEL in der Auswertung.» — fragebogen_parameter_analyse.yaml

Dieselben Items bedienen **beides**: KPI-Scores (für BFE-Reporting) UND BCM-Parameter (für Interventions-Design). Die 14 empfohlenen Änderungen sind minimal: 9× nur Mapping-Anpassung (Level A), 4× leichtes Reframing (Level B), 1× neues Item (Level C).

---

## 4. Fragebogen v5 — Analyse

### 4.1 Neue Items in v5

| Item | Konstrukt | BCM-Parameter | Typ |
|------|-----------|---------------|-----|
| F2.10 | Soziale Normen | σ_peer | Deskriptiv |
| F2.11 | Installer-Einfluss | ι_installer | Vertrauensquelle |
| F2.12 | BCJ-Stage | φ | Selbstverortung |
| F2B.1-3 | STWE-Governance | Entscheidungsstruktur | Institutionell |
| F3.10 | Present Bias | β | Incentive-Choice |
| F3.11 | Trigger-Events | θ | Aktivierungsschwelle |
| F4.3.12 | Status Quo Bias | — | Beharrungstendenz |
| F4.9 | Loss Aversion | λ | Gain-Loss-Framing |
| F10.1 | Panel-Einwilligung | — | Longitudinal |

### 4.2 Methodische Stärken

1. **MaxDiff-Design** (14 Choice Sets, 4 Items, 10 Attribute): Direkte Schätzung der FEPSDE-Utility-Gewichte (u_F, u_E, u_P, u_S, u_X)
2. **BCJ-Staging** (F2.12): Explizite Phasen-Verortung statt impliziter Ableitung
3. **Present-Bias-Proxy** (F3.10): Incentive-Choice-Experiment (jetzt vs. später) — valider als Selbsteinschätzung
4. **Loss-Aversion-Proxy** (F4.9): Gain-Loss-Framing-Vergleich — methodisch sauber
5. **Panel-Einwilligung** (F10.1): Ermöglicht Intention-Behavior-Gap-Messung

### 4.3 Identifizierte Schwächen

| Schwäche | Schweregrad | Erläuterung |
|----------|-------------|-------------|
| **HOW-Dimension fehlt** | Hoch | Keine γ-Messung (Komplementarität/Bundling: Heizung + PV + Dämmung) |
| **WHERE-Dimension indirekt** | Mittel | Keine explizite Parameter-Validierung |
| **Befragungszeit +5-7 Min.** | Mittel | 23-28 Min. vs. 18-22 Min. — Abbruchrisiko |
| **β-Proxy vereinfacht** | Niedrig | Incentive-Choice misst Tendenz, nicht exakten β-Wert |
| **Social Desirability** | Mittel | Keine Kontrolle für soziale Erwünschtheit bei Umweltfragen |

### 4.4 10C-Abdeckung nach v5

| 10C-Dimension | v4 Status | v5 Status | Abdeckungsgrad |
|---------------|-----------|-----------|----------------|
| WHO (AAA) | Teilweise | Gut | ★★★☆ |
| WHAT (C) | MaxDiff vorhanden | MaxDiff + FEPSDE | ★★★★ |
| **HOW (B)** | **Fehlt** | **Fehlt** | **★☆☆☆** |
| WHEN (V) | Fehlt | Trigger-Events, β | ★★★☆ |
| WHERE (BBB) | Fehlt | Indirekt | ★★☆☆ |
| AWARE (AU) | Kampagnenbekanntheit | + Salienz + Wissen | ★★★★ |
| READY (AV) | 2/5-Jahres-Absicht | + θ + BCJ-Stage | ★★★★ |
| STAGE (AW) | Implizit | Explizit (F2.12) | ★★★★ |
| HIERARCHY (HI) | Fehlt | STWE teilweise | ★★☆☆ |
| EIT (IE) | — | — | N/A |

---

## 5. Review-Kommentar-Management

### 5.1 Systematische Bearbeitung

82 Kommentare von intervista und BFE wurden in 5 Kategorien bearbeitet:

| Kategorie | Anzahl | Strategie |
|-----------|--------|-----------|
| AKZEPTIEREN | 19 | Vollständig übernommen |
| VERTEIDIGEN | 14 | Mit Literatur begründet |
| KOMPROMISS | 11 | Angepasste Lösung |
| BFE-Filter | 16 | An Auftraggeber delegiert |
| Redaktionell | 22 | Direkt umgesetzt |

### 5.2 Zentraler Streitpunkt: Stories/Priming

**Intervista-Position:** «Ein Fragebogen ist kein Instrument zur Verhaltensänderung.»

**FehrAdvice-Position:** Kontextualisierung verbessert Konstruktvalidität (Schwarz 1999, Tourangeau 2000).

**Kompromiss-Lösung:**
- Typ 1 «Gespräch» → Neutralisierte Kontextualisierung (ohne emotionale Sprache)
- Typ 2 «Haus-Gang» → Gekürzte Situationsbeschreibung
- Typ 3 «Internet-Suche» → Direkter Übergang (kein Narrativ)
- Segmentierungs-Story → Komplett entfernt

### 5.3 Strategische Erkenntnis

Die Response-Strategie dokumentiert eine wichtige methodische Übereinstimmung: Sowohl intervista als auch EBF haben dasselbe Ziel — **saubere Baseline-Messung des Status Quo**. Der Unterschied liegt in der **Tiefe**, nicht in der Intention. EBF-Items messen den aktuellen Zustand (Diagnose), nicht eine gewünschte Verhaltensänderung (Therapie).

---

## 6. Legacy-Daten (2021-2025): Was wir wissen

### 6.1 Ergebnisse 2024

| Metrik | Wert | Trend |
|--------|------|-------|
| Impulsberatung CR | 9.84% | ↑ von 7.07% |
| EFH-Impulsberatung | — | +23% |
| MFH-Impulsberatung | — | **-43%** |
| KMU-Impulsberatung | — | +100% |
| QR-Code-Zugriffe | 799 | +115% |
| Organischer Traffic | — | -26% (aber Q4: +70%) |
| Kampagnen-Anteil | 52% | Dominant |

### 6.2 Kanal-Qualität

| Kanal | Anteil | Qualität | Stärke |
|-------|--------|----------|--------|
| Kampagnen (Paid) | 52% | Unterdurchschnittlich | Volumen |
| Suchmaschinen (SEO) | 20% | Sehr hoch | 26% Heizkostenrechner-CR |
| Direkte Zugriffe | 15% | Hoch | Höchste Kontakt-CR |
| Verweisende Webseiten | 10% | Sehr hoch | Längste Aufenthaltszeit |
| Soziale Netzwerke | 3% | Gering | Geringste Aufenthaltszeit |

### 6.3 SEO-Trends

Stark steigende Suchanfragen:
- «Wie lange dürfen Elektroheizungen noch betrieben werden?»
- «Wann werden Elektroheizungen verboten?»
- «Wie lange sind Elektroboiler noch erlaubt?»

→ **Content-Lücke**: Diese Fragen werden nicht ausreichend beantwortet.

---

## 7. Kritische Gaps und Empfehlungen

### 7.1 Kritische Lücken

#### Gap 1: Installer-Tracking (KRITISCH)

**Problem:** 55% aller Heizungsersetzungen sind **Notfallersetzungen**. Der Installateur ist der zentrale Entscheidungsbeeinflusser — aber weder im Legacy-Messkonzept noch im Fragebogen v5 systematisch erfasst.

**Empfehlung:** Dediziertes Installer-Modul entwickeln:
- Installer als Informationsquelle (F2.11 ist ein Anfang)
- Installer-Empfehlungsverhalten messen
- Vertrauensmetrik Installateur vs. Online-Information

#### Gap 2: HOW-Dimension / Komplementarität (HOCH)

**Problem:** Die HOW-Dimension (Komplementarität γ) ist die **einzige 10C-Dimension ohne jede Messung** in v5. Keine Daten zu Bundling-Präferenzen (Heizung + PV + Dämmung zusammen vs. einzeln).

**Empfehlung:** Mindestens 1-2 Items zu Bundling/Paketlösungen hinzufügen. Relevant für Portfolio-Optimierung der Interventionen.

#### Gap 3: Intention-Behavior Gap (HOCH)

**Problem:** Panel-Design ist konzipiert (F10.1 Einwilligung), aber die operative Umsetzung (12-Monats-Follow-up, Rücklaufquoten-Management, Matching) ist nicht dokumentiert.

**Empfehlung:** Operatives Panel-Protokoll entwickeln:
- Wave-2-Fragebogen definieren
- Attrition-Management planen (Sheeran 2002: 28% Gap erwartet)
- Matching-Strategie für Intention-vs.-Action

#### Gap 4: MFH-Rückgang (HOCH)

**Problem:** MFH-Impulsberatungen -43% in 2024 — stärkster Rückgang aller Segmente. Ursache unklar (komplexere Entscheidungsstruktur? Längere Zyklen? Principal-Agent-Problem?).

**Empfehlung:** Qualitative Vertiefung MFH/STWE:
- STWE-Items (F2B.1-3) sind guter Anfang
- Zusätzlich: MFH-Vermieter:innen-Perspektive erfassen
- Principal-Agent-Dynamik (Vermieter:in investiert, Mieter:in profitiert) modellieren

### 7.2 Mittlere Lücken

| Gap | Beschreibung | Empfehlung |
|-----|-------------|------------|
| **Social Desirability** | Keine Kontrolle bei Umweltfragen | Marlowe-Crowne Kurzskala (3 Items) |
| **Generationen-Übergang** | 65+ ohne Nachfolgeplanung | Lifecycle-Trigger-Item hinzufügen |
| **Westschweiz-Modell** | Überprop. Traffic aus FR/VS/NE | Systematische Replikation in andere Kantone |
| **Tessin-CTR** | Hohe Impressionen, fast keine Klicks | IT-Content-Audit und -Optimierung |
| **Blog-Performance** | Wenig Traffic, wenig Conversions | SEO-Optimierung oder Einstellung |

### 7.3 Stärken (zur Absicherung)

| Stärke | Bewertung |
|--------|-----------|
| MaxDiff für FEPSDE-Utility | State-of-the-Art, direkte Parameterschätzung |
| BCJ-Stage als explizites Item | Ermöglicht gezielte Phasen-Interventionen |
| A-W-I-T als KPI-Framework | Verständlich für BFE, kompatibel mit BCM |
| 47 Papers in Literaturmapping | Solide wissenschaftliche Fundierung |
| 3-Level-Change-Klassifikation | Minimale Fragebogenänderung, maximaler Erkenntnisgewinn |
| Response-Strategie | Professionelles Stakeholder-Management mit intervista |
| model.yaml (1'206 Zeilen) | Vollständiges 10C-Modell mit Predictions |

---

## 8. Bewertung der EBF-Konformität

### 8.1 10C-Compliance-Score

| Dimension | Coverage | Score | Kommentar |
|-----------|----------|-------|-----------|
| WHO (AAA) | Screening + Segmente | 7/10 | Installer fehlt als Stakeholder |
| WHAT (C) | MaxDiff + FEPSDE | 8/10 | Solide Utility-Dekomposition |
| **HOW (B)** | **Nicht gemessen** | **2/10** | **Kritische Lücke** |
| WHEN (V) | β, Trigger-Events | 7/10 | Saisonalität nur indirekt |
| WHERE (BBB) | Literaturwerte | 5/10 | Keine eigene Validierung |
| AWARE (AU) | Dual Recall + Salienz | 8/10 | Gut abgedeckt |
| READY (AV) | BCJ + θ | 8/10 | Stark durch v5-Erweiterung |
| STAGE (AW) | Explizites BCJ-Item | 8/10 | Guter Fortschritt |
| HIERARCHY (HI) | STWE teilweise | 5/10 | MFH-Entscheidungsebenen fehlen |
| EIT (IE) | Intervention-Vectors | 6/10 | Konzipiert, nicht validiert |

**Gesamt: 6.4/10** — Starker Fortschritt gegenüber 3/10 (Legacy), aber HOW und HIERARCHY bleiben Lücken.

### 8.2 Behavioral Construct Coverage

| Konstrukt | v4 | v5 | Methode |
|-----------|----|----|---------|
| Loss Aversion (λ) | ❌ | ✅ | Gain-Loss-Framing (F4.9) |
| Present Bias (β) | ❌ | ✅ | Incentive-Choice (F3.10) |
| Social Norms (σ) | ❌ | ✅ | Deskriptive Norm (F2.10) |
| Status Quo Bias | ❌ | ✅ | Beharrungstendenz (F4.3.12) |
| Default Effects | ❌ | Indirekt | Via Opt-in/Opt-out Framing |
| Mental Accounting | Grob | Verbessert | MaxDiff + Kostenwahrnehmung |

**6/6 Konstrukte gemessen** (vs. 2/6 in v4) — Ziel erreicht, wobei Default Effects nur indirekt abgedeckt sind.

---

## 9. Projektrisiken

| # | Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|---|--------|---------------------|--------|------------|
| R1 | Befragungszeit-Überschreitung (>28 Min.) | Mittel | Hoch | Modulare Kürzung vorbereiten |
| R2 | Panel-Attrition Wave 2 | Hoch | Hoch | Incentive-Strategie, Überbefragung |
| R3 | intervista lehnt EBF-Items ab | Niedrig | Hoch | V4-Justification-Dokument ist vorbereitet |
| R4 | BFE versteht BCM-Parameter nicht | Mittel | Mittel | Dual-Reporting: A-W-I-T Scores + BCM |
| R5 | MFH-Rückgang setzt sich fort | Hoch | Mittel | Qualitative Vertiefung Q1/2026 |
| R6 | Installer-Daten fehlen langfristig | Hoch | Hoch | Installer-Survey als separates Workpackage |

---

## 10. Zielgruppe, Quotierung & Gewichtung, Stichprobengrösse

### 10.1 Zielgruppe

**Gesamtzielgruppe (Screening):**
Wohneigentümer:innen in der Schweiz (Alter 25–79), die ein Haus oder eine Eigentumswohnung besitzen (INTRO1 = 2 oder 3). Mieter:innen werden ausgescreent. Befragte, die das Gebäudealter nicht kennen (INTRO2 = 99), werden ausgescreent.

**Modulspezifische Zielgruppen (nach MODUL_ZUWEISUNG V3):**

| Modul | Zielgruppe | Filter (INTRO-Block) | Geschätzte Eligibility |
|-------|-----------|----------------------|------------------------|
| **M1 Gesamtmodernisierung** | Eigentümer:innen mit Gebäude ≥ 5 Jahre | INTRO2 > 1 | ~90–95% |
| **M2 Gebäudehülle** | Eigentümer:innen mit Gebäude ≥ 25 Jahre, Hülle **nicht** saniert | INTRO2 > 2 UND INTRO6 = 2 | ~30–35% |
| **M3 Heizungsersatz** | Eigentümer:innen mit Gebäude ≥ 25 Jahre, Heizung **nicht** erneuerbar | INTRO2 > 2 UND INTRO7 = 2 | ~30–40% |
| **M4 PV/Solarenergie** | Eigentümer:innen **ohne** PV-Anlage (inkl. Neubauten) | INTRO8 = 2 | ~82–88% |
| **M5 E-Mobilität** | Eigentümer:innen **mit** E-Auto ODER Kaufabsicht E-Auto | INTRO5a = 1 ODER INTRO10a = 1 | ~10–15% |

**Hinweise zu den Eligibility-Schätzungen:**
- M1 + M4 haben sehr breite Zielgruppen (fast alle gescreenten Personen)
- M2 + M3 haben moderate Zielgruppen (nur ältere, nicht sanierte Gebäude)
- M5 hat eine sehr enge Zielgruppe (E-Auto-Penetration CH aktuell ~6–8% Neuzulassungen, Bestand ~3–4%; mit Kaufabsicht ~10–15%)
- Mehrfach-Eligibility: Die meisten Befragten qualifizieren sich für 2–4 Module gleichzeitig (typisch: M1 + M4 + ggf. M2/M3)
- Die Kernzielgruppe der Vorgängerkampagne «erneuerbar heizen» (ältere fossile Heizsysteme) deckt sich mit M3

### 10.2 Quotierung und Gewichtung

**Quotierung auf Gesamtstichproben-Ebene (interlocked):**
- **Geschlecht** × **Alter** (25–39 / 40–59 / 60–79) × **Sprachregion** (DE / FR / IT)
- Verteilung gemäss BFS Strukturerhebung (Wohneigentümer:innen)
- Quota-Items im Fragebogen: Q_ALTER, Q_GESCHLECHT, Q_PLZ (an den Anfang verschoben, vgl. V3 Änderung S6)
- Gebäudetyp (EFH/MFH) ist **keine Quotierungsvariable**, sondern nur Analysevariable (INTRO3)

**Modulzuteilung:**
- **Disproportionale Modulzuteilung** mit Mindest-n pro Modul (nicht rein zufällig)
- Stichprobenanbieter (Intervista) steuert über Modul-Quoten: Sobald ein Modul sein Ziel-n erreicht hat, werden neue Befragte bevorzugt anderen Modulen zugewiesen

**Gewichtung (Post-Stratification):**
- Rim-Weighting (iterative proportional fitting) nach Geschlecht × Alter × Sprachregion auf Gesamtstichproben-Ebene
- Gewichte cappen bei max. 3.0 (um Varianzinflation zu begrenzen)
- **IT-Oversampling optional:** Tessin kann überquotiert werden (wie im alten Design), um Sprachregion-spezifische Aussagen zu ermöglichen

### 10.3 Stichprobengrösse

**Formel für den maximalen Stichprobenfehler (95% KI, worst case p=0.5):**

```
SE = 1.96 × √(0.25 / n) = 0.98 / √n
```

| n | SE (±PP) | Bewertung |
|---|----------|-----------|
| 1'500 | ±2.5 PP | Sehr gut |
| 1'200 | ±2.8 PP | Gut |
| 1'000 | ±3.1 PP | Gut |
| 500 | ±4.4 PP | Akzeptabel |
| 400 | ±4.9 PP | Akzeptabel |
| 300 | ±5.7 PP | Grenzwertig |
| 250 | ±6.2 PP | Grenzwertig |
| 200 | ±6.9 PP | Schwach |
| 100 | ±9.8 PP | Ungenügend |

#### Problem: Reine Zufallszuteilung reicht nicht

Bei reiner Gleichverteilung auf 5 Module (n=1'200 / 5 = 240) wäre der SE ±6.3 PP — zu hoch für belastbare Modulaussagen. Zudem qualifizieren sich nicht alle Befragten für alle Module, was zu **stark ungleichen natürlichen Modulgrössen** führt:

**Geschätzte natürliche Verteilung bei n=1'200 und reiner Zufallszuteilung:**

| Modul | Geschätztes n | SE (±PP) | Problem? |
|-------|--------------|----------|----------|
| M1 Gesamtmodernisierung | ~400–480 | ±4.5–4.9 PP | OK |
| M2 Gebäudehülle | ~120–160 | ±7.7–9.0 PP | **Zu hoch** |
| M3 Heizungsersatz | ~130–170 | ±7.5–8.6 PP | **Zu hoch** |
| M4 PV/Solarenergie | ~350–420 | ±4.8–5.2 PP | OK |
| M5 E-Mobilität | ~40–70 | ±11.7–15.5 PP | **Viel zu hoch** |

**Erklärung:** M1 und M4 haben breite Eligibility und «konkurrieren» um dieselben Befragten. M2/M3 haben engere Filter. M5 hat extrem wenig Eligible (~12%), und diese qualifizieren sich meistens auch für M1/M4, was den M5-Anteil weiter verdünnt.

#### Empfehlung: 3-Säulen Stichprobendesign

```
┌─────────────────────────────────────────────────────────────────────────┐
│  SÄULE 1: GESAMTSTICHPROBE (n=1'200 pro Welle)                         │
│  ──────────────────────────────────────────────                         │
│  Rekrutierung: Intervista Online-Panel, BFS-quotiert                    │
│  Modulzuteilung: DISPROPORTIONAL QUOTIERT (nicht rein zufällig!)        │
│                                                                         │
│  Ziel-n pro Modul (Mindestquoten):                                      │
│    M1 Gesamtmodernisierung:  n = 300  (±5.7 PP)                        │
│    M2 Gebäudehülle:          n = 250  (±6.2 PP)                        │
│    M3 Heizungsersatz:        n = 250  (±6.2 PP)                        │
│    M4 PV/Solarenergie:       n = 300  (±5.7 PP)                        │
│    M5 E-Mobilität:           n = 100  (±9.8 PP) → ungenügend allein    │
│  Total:                      n = 1'200                                  │
│                                                                         │
│  Mechanismus: Sobald ein Modul seine Mindestquote erreicht hat,         │
│  werden neue Befragte bevorzugt anderen Modulen zugewiesen.             │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│  SÄULE 2: BOOST M3 HEIZUNGSERSATZ (n=250)                              │
│  ──────────────────────────────────────────                              │
│  Zielgruppe: Wohneigentümer:innen mit Gebäude ≥ 25 J. UND             │
│              fossiler Heizung (Öl/Gas) — Kernzielgruppe des            │
│              Heizungsersatz-Moduls (M3)                                 │
│  Rekrutierung: Gezieltes Screening via Panel ODER                       │
│                Adress-Sampling via Kantone/GEAK-Register                │
│  Begründung: M3 (Heizungsersatz) ist das KERNMODUL von ECHfP;          │
│              höchste Präzision nötig für Wirkungsmessung                │
│                                                                         │
│  → M3 Total: 250 (Säule 1) + 250 (Boost) = 500  →  ±4.4 PP           │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│  SÄULE 3: BOOST M5 E-MOBILITÄT (n=200)                                 │
│  ──────────────────────────────────────────                              │
│  Zielgruppe: Wohneigentümer:innen mit E-Auto ODER konkreter            │
│              Kaufabsicht E-Auto + eigenem Parkplatz                     │
│  Rekrutierung: Gezieltes Screening via Panel (Pre-Screening-Frage      │
│                zum Autobesitz) ODER Kooperation TCS/E-Mobilitäts-       │
│                Verbände                                                 │
│  Begründung: Natürliche Eligibility zu gering (~12%) für               │
│              aussagekräftige Modulergebnisse                            │
│                                                                         │
│  → M5 Total: 100 (Säule 1) + 200 (Boost) = 300  →  ±5.7 PP           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

#### Ergebnis: Stichprobengrösse pro Modul und Welle

| Modul | Säule 1 (Gesamt) | Boost | **Total n** | **SE (±PP)** | Bewertung |
|-------|-----------------|-------|-------------|-------------|-----------|
| M1 Gesamtmodernisierung | 300 | — | **300** | ±5.7 PP | Akzeptabel |
| M2 Gebäudehülle | 250 | — | **250** | ±6.2 PP | Akzeptabel |
| M3 Heizungsersatz | 250 | +250 | **500** | ±4.4 PP | Gut |
| M4 PV/Solarenergie | 300 | — | **300** | ±5.7 PP | Akzeptabel |
| M5 E-Mobilität | 100 | +200 | **300** | ±5.7 PP | Akzeptabel |
| **Total pro Welle** | **1'200** | **+450** | **1'650** | ±2.4 PP | Sehr gut |

**Über 3 Wellen (kumuliert, falls stabile Parameter):**

| Modul | n kumuliert (3 Wellen) | SE kumuliert | Ermöglicht |
|-------|------------------------|-------------|------------|
| M1 | 900 | ±3.3 PP | Subgruppenanalysen (EFH/MFH, Alter) |
| M2 | 750 | ±3.6 PP | Subgruppenanalysen |
| M3 | 1'500 | ±2.5 PP | Detaillierte Segmentierung, Trendanalyse |
| M4 | 900 | ±3.3 PP | Subgruppenanalysen |
| M5 | 900 | ±3.3 PP | Subgruppenanalysen |
| **Total** | **4'950** | ±1.4 PP | Alle Analysen |

#### Variante MINIMAL (ohne Boost)

Falls Budget nur für Säule 1 reicht:

| Modul | n (Säule 1) | SE (±PP) | Bewertung |
|-------|-------------|----------|-----------|
| M1 | 300 | ±5.7 PP | Akzeptabel |
| M2 | 250 | ±6.2 PP | Grenzwertig |
| M3 | 250 | ±6.2 PP | Grenzwertig (für Kernmodul zu hoch!) |
| M4 | 300 | ±5.7 PP | Akzeptabel |
| M5 | 100 | ±9.8 PP | **Ungenügend** |
| **Total** | **1'200** | ±2.8 PP | — |

⚠️ **Risiko Variante MINIMAL:** M3 (Kernmodul) hat keinen Boost → ±6.2 PP ist für die Kampagnenwirkungsmessung zu hoch, um statistisch signifikante Veränderungen von 5–10 PP zwischen Wellen zu detektieren. M5 ist mit n=100 nicht für eigenständige Aussagen nutzbar.

#### Entscheidungsmatrix

| Variante | Total n/Welle | Kosten-Faktor | M3 SE | M5 SE | Empfehlung |
|----------|--------------|---------------|-------|-------|------------|
| **OPTIMAL** | 1'650 | 1.0× | ±4.4 PP | ±5.7 PP | **Empfohlen** |
| **STANDARD** (nur M3-Boost) | 1'450 | 0.88× | ±4.4 PP | ±9.8 PP | M5 nur deskriptiv |
| **MINIMAL** (kein Boost) | 1'200 | 0.73× | ±6.2 PP | ±9.8 PP | Nur Gesamtaussagen |

### 10.4 Methodische Hinweise

**Disproportionale Zuteilung vs. Zufallszuteilung:**
- Der V3-Fragebogen sieht «Zufällige Modulausspielung» vor (MODUL_ZUWEISUNG)
- Für repräsentative Modulaussagen muss diese auf **quotierte Zuteilung** umgestellt werden
- Intervista kann dies über Modul-Quoten steuern: Sobald M1 sein Ziel-n erreicht hat, werden M1-eligible Befragte automatisch zu M2/M3/M4 umgeleitet
- Dies erfordert Absprache mit Intervista bei der Feldplanung (AP4.2)

**Gewichtung bei disproportionaler Zuteilung:**
- Befragte in überrepräsentierten Modulen erhalten Design-Gewichte < 1
- Befragte in unterrepräsentierten Modulen erhalten Design-Gewichte > 1
- Die Gesamtstichprobe bleibt über Rim-Weighting repräsentativ
- Boost-Befragte werden separat gewichtet und nur für Modul-Aussagen verwendet

**Power-Analyse für Trendmessung (Welle-zu-Welle):**
- Um einen Unterschied von Δ = 5 PP (z.B. Awareness-Anstieg) mit 80% Power zu detektieren: Minimum n ≈ 400 pro Modul pro Welle
- M3 mit Boost (n=500) kann Δ ≥ 4.5 PP detektieren ✓
- M1/M4 (n=300) können Δ ≥ 5.7 PP detektieren — grenzwertig
- M2 (n=250) kann Δ ≥ 6.2 PP detektieren — nur grössere Effekte
- M5 ohne Boost (n=100) kann Δ ≥ 10 PP detektieren — nur für deskriptive Zwecke
- Kumuliert über 3 Wellen deutlich besser (s. Tabelle oben)

---

## 11. Zusammenfassung und nächste Schritte

### Gesamtbewertung

Das ECHfP-Wirkungsmessungs-Projekt 2026 ist **architektonisch solid** und **methodisch ambitioniert**. Der Paradigmenwechsel von KPI-Score-Berechnung zu BCM-Parameter-Extraktion — eingebettet in das Behavioral Impact System (BIS) — ist der richtige Schritt und wird durch die bestehende Fragebogenstruktur ermöglicht, ohne diese grundlegend zu verändern. Die Erweiterung von der reinen Heizungsersatz-Kampagne «erneuerbar heizen» zum umfassenden 5-Modul-Programm ECHfP erfordert eine entsprechend differenzierte Stichproben- und Auswertungsarchitektur.

Die grössten Risiken liegen in der **operativen Umsetzung** (Panel-Design, Befragungszeit) und in **strukturellen Lücken** (HOW-Dimension, Installer-Tracking, MFH-Vertiefung).

### Empfohlene Prioritäten

1. **Sofort:** HOW-Dimension mit 1-2 Bundling-Items schliessen
2. **Kurzfristig:** Panel-Protokoll operationalisieren (Wave-2-Design, Attrition-Management)
3. **Mittelfristig:** Installer-Survey als eigenständiges Workpackage planen
4. **Laufend:** MFH/STWE-Segment vertiefen, Tessin-CTR optimieren

### Offene Fragen für Klärung

1. Ist ein Installer-Survey im Budget/Scope des aktuellen Auftrags?
2. Wie wird das Dual-Reporting (A-W-I-T + BCM) technisch umgesetzt?
3. Welche Incentive-Strategie ist für Panel-Wave-2 vorgesehen?
4. Soll die HOW-Dimension in v5 ergänzt oder für v6 geplant werden?

---

*Erstellt im Rahmen der EBF-Qualitätssicherung. SSOT für dieses Review: `messkonzept_2026/review_bfe_messung_2026.md`*
