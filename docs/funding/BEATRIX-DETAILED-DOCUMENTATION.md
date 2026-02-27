# BEATRIX: Detaillierte Dokumentation

**Version:** 1.0 | **Datum:** 2026-01-18 | **Status:** Für Innosuisse-Antrag

---

## Inhaltsverzeichnis

1. [Frage 1: Was ist BEATRIX?](#frage-1-was-ist-beatrix)
2. [Frage 2: Wie setzen wir BEATRIX in der Beratung ein?](#frage-2-wie-setzen-wir-beatrix-in-der-beratung-ein)
3. [Frage 3: Wie lief die Beratung VOR BEATRIX?](#frage-3-wie-lief-die-beratung-vor-beatrix)
4. [Frage 4: Wohin möchten wir BEATRIX weiterentwickeln?](#frage-4-wohin-möchten-wir-beatrix-weiterentwickeln)
5. [Appendix: Kontext (Ψ) erklärt](#appendix-kontext-ψ-erklärt)
6. [Appendix: Framework vs. Model](#appendix-framework-vs-model)
7. [Appendix: 20 KPIs im Vergleich](#appendix-20-kpis-im-vergleich)

---

## Frage 1: Was ist BEATRIX?

### Definition

BEATRIX ist ein **General Decision Support System (GDSS)**, das die axiomatische Strenge der Verhaltensökonomik mit der Skalierbarkeit moderner Künstlicher Intelligenz verbindet.

| Aspekt | Beschreibung |
|--------|--------------|
| **Entwickler** | FehrAdvice & Partners AG unter Einbeziehung von Prof. Ernst Fehr |
| **Kern-Transformation** | Von erfahrungsbasiertem Handwerk zu datengetriebener Ingenieurswissenschaft |
| **Unterschied zu GPT** | Generative KI erzeugt Texte auf Basis statistischer Wahrscheinlichkeiten; BEATRIX **berechnet menschliches Verhalten** auf Basis evidenzbasierter Zusammenhänge |
| **Innosuisse-Ziel** | Prototyp → industriell skalierbare, fehlertolerante Software-Architektur |

### Das Kernproblem: Die Lücke zwischen Daten und Verhalten

Entscheidungsträger verfügen über:
- ✓ Exzellente Daten zu **messbaren Faktoren** (Finanzen, Logistik, Technik)
- ✗ Wenig systematische Grundlagen für **weiche Faktoren** (Kultur, Vertrauen, Normen, Identität)

**Grenzen herkömmlicher Ansätze:**

| Ansatz | Limitation |
|--------|------------|
| **Traditionelle Beratung** | Basiert auf Intuition, nicht skalierbar, anfällig für kognitive Verzerrungen |
| **Standard-KI (LLMs)** | Kann über Strategie schreiben, aber nicht präzise Verhalten vorhersagen |

**BEATRIX-Lösung:** Nicht Text simulieren, sondern eine **axiomatische Verhaltensmatrix** berechnen.

---

### Die theoretische Basis: Das Complementarity-Context Framework

#### Was ist Komplementarität?

**Beispiel:** Ein Unternehmen führt leistungsbasiertes Bonussystem ein.

| Dimension | Problem wenn ignoriert |
|-----------|----------------------|
| Kultur | In kooperativer Kultur kann individueller Bonus Konkurrenz erzeugen |
| Vertrauen | Bei niedrigem Führungsvertrauen wird Bonus als Kontrolle wahrgenommen |
| Motivation | Intrinsische Motivation kann durch extrinsische verdrängt werden |

**Das Zusammenspiel dieser Faktoren (Komplementarität)** kann zum gegenteiligen Effekt führen. BEATRIX berücksichtigt mathematisch nachvollziehbar die gleichzeitigen Wirkungen.

#### Was ist Kontext (Ψ)?

Kontext ist alles, was die Entscheidung beeinflusst, **ohne dass sich die Präferenzen ändern**.

**Die 8 Ψ-Dimensionen:**

| Dimension | Erfasst | Beispiel |
|-----------|---------|----------|
| **Physisch** | Ort, Temperatur, Lärm | Büro vs. Home Office |
| **Sozial** | Wer beobachtet, wer urteilt | Allein vs. mit Vorgesetztem |
| **Zeitlich** | Zeitdruck, Zeitpunkt | Morgens vs. abends |
| **Kulturell** | Normen, Erwartungen | Schweiz vs. Japan |
| **Institutionell** | Regeln, Defaults, Strukturen | Opt-in vs. Opt-out |
| **Informationell** | Was ist bekannt, was präsent | Nach vs. vor einer Nachricht |
| **Emotional** | Stimmung, Stress, Energie | Entspannt vs. gestresst |
| **Ressourcenbezogen** | Zeit, Geld, Aufmerksamkeit | Reich vs. knapp |

**Die Kern-Formel:**

```
Effektive Nutzenstiftung = Potenzielle Nutzenstiftung × Kontext-Faktor

U_eff = U_pot × f(Ψ)
```

---

### Die technologische Umsetzung (UZH-Beitrag)

#### Layer A: Semantic Calibration Engine

- Extrahiert aus unstrukturierten Kundendaten (Berichte, Intranet, Umfragen) die relevanten Kontextdimensionen
- Gleicht mit Datenbank experimenteller Effekte ab
- **Herausforderung:** System muss Kontextänderungen (z.B. Fusion) erkennen und Verhaltensmatrix anpassen

#### Layer B: LLM Monte Carlo

- LLMs nicht als Antwort-Generatoren, sondern für **systematische Variationsanalysen**
- Tausende Mikro-Simulationen mit leicht variierten Parametern
- **Output:** Wahrscheinlichkeitsverteilung statt Einzelantwort
  - "Mit 85% Wahrscheinlichkeit führt Massnahme A zu Steigerung, ±3% Konfidenzintervall"

#### Layer C: FEPSDE Welfare-Berechnung

Multidimensionale Wohlfahrtsfunktion:

| Dimension | Beschreibung |
|-----------|--------------|
| **F** Financial | Geld, Einkommen, wirtschaftliche Sicherheit |
| **E** Emotional | Wohlbefinden, Zufriedenheit, Sinn |
| **P** Physical | Gesundheit, Energie, Langlebigkeit |
| **S** Social | Beziehungen, Zugehörigkeit, Status |
| **D** Digital | Konnektivität, Zugang, digitale Teilhabe |
| **E** Ecological | Umweltqualität, Nachhaltigkeit |

---

## Frage 2: Wie setzen wir BEATRIX in der Beratung ein?

### Die Policy Analysis Pipeline

BEATRIX ersetzt episodisches Projektgeschäft durch **kontinuierliche, datengetriebene Systempartnerschaft**.

#### Modul A: Automated Coherence Audit (Diagnose)

| Vorher | Mit BEATRIX |
|--------|-------------|
| Wochenlange Interviews, Fokusgruppen, manuelle Auswertungen | System an Kundendatenströme angeschlossen |
| Kostenintensiv, langsam, subjektiv | NLP extrahiert Kulturdimensionen automatisch |

**Kundenbeispiel: Südostbahn (SOB)**
- Messung der Strategic Coherence (Strategie vs. Kultur)
- Output: Quantitative Heatmap mit Kohärenz-Index
- "In Abteilung Wartung liegt K bei nur 0.35 → passive Widerstand erwartet"

#### Modul B: Ex-Ante Simulation ("The Wind Tunnel")

Statt Best-Practice-Empfehlungen: **Wirkung vor Implementierung simulieren**.

**Kundenbeispiel: Bundesamt für Energie (BFE)**
- Szenario A: Subventionen für Wärmepumpen
- Szenario B: Nudging durch soziale Vergleiche
- BEATRIX prognostiziert: "Szenario B in städtischen Kantonen 40% effektiver bei 10% der Kosten"

#### Modul C: Behavioral Pricing & Marketing

**Kundenbeispiel: Schweizer Bank**
- 20 Kampagnenvarianten an Silicon Samples (simulierte Kundenprofile) testen
- Nur Top-3 mit hoher Konversionswahrscheinlichkeit werden real ausgerollt

**Kundenbeispiel: Retailbanking Pricing**
- BEATRIX berechnet Fairness-Wahrnehmung
- Zeigt psychologische Schmerzgrenze für Preiserhöhungen

#### Modul D: Strategic Resilience & Monitoring

**Kundenbeispiel: Bauunternehmen**
- Simulation: "Was passiert mit Polier-Motivation bei Kurzarbeit?"
- BEATRIX identifiziert Coherence Traps (kurzfristige Massnahmen zerstören langfristige Werte)

---

## Frage 3: Wie lief die Beratung VOR BEATRIX?

### Phase 1: VOR BEATRIX – Das "Guru-Modell"

| Aspekt | Status Quo Ante |
|--------|-----------------|
| **Wissensbasis** | Implizites Wissen (tacit knowledge) |
| **Prozess** | Jedes Mandat bei Null, manuelle Interviews/Workshops |
| **Qualität** | Abhängig von Seniorität und Intuition des Partners |
| **Limit** | Nicht skalierbar, hoher Wissensverlustrisk |
| **Zeitverteilung** | 60-70% Datenerhebung, 30% strategische Lösung |

### Phase 2: MIT BEATRIX – Das "Plattform-Modell"

**Transformation:** Wissen wird zu explizitem Code (codified knowledge)

#### A. Effizienzsteigerung: +45%

| Metrik | Vorher | Nachher |
|--------|--------|---------|
| Kultur-Diagnose | 4 Wochen | 3 Tage |
| Beraterzeit für High-Value-Tasks | 30% | 80% |

#### B. Qualitätssteigerung: +50%

| Aspekt | Vorher | Nachher |
|--------|--------|---------|
| Empfehlungsbasis | Plausible Meinung | Simulation |
| Aussage | "Das könnte schwierig werden" | "Scheiterwahrscheinlichkeit 65% ±5%" |

#### C. Geschäftsmodell-Veränderung

- Von Zeit-gegen-Geld zu **Asset-Based Consulting**
- Wissen in Komplementaritäts-Matrix konserviert
- Junior-Berater + BEATRIX = Partner-Qualität

### Zusammenfassung: Das Delta

| Dimension | VOR BEATRIX | MIT BEATRIX |
|-----------|-------------|-------------|
| Basis | Intuition & Erfahrung | Daten & Kalibrierung |
| Analyse | Rückblickend (Post-Mortem) | Vorausschauend (Simulation) |
| Skalierung | Linear (Personal) | Software-gestützt |
| Output | Powerpoint-Konzepte | Validierte Szenarien |
| Effizienz | Benchmark (100%) | **+45% Produktivität** |
| Qualität | Subjektiv variierend | **+50% Prognosegüte** |

---

## Frage 4: Wohin möchten wir BEATRIX weiterentwickeln?

### Vision: From Tool to Living System

| Heute | Projektende | Übermorgen |
|-------|-------------|------------|
| Werkzeug für Berater (Expert-in-the-Loop) | Plattform für evidenzbasierte Entscheidungen | Selbstlernendes Ökosystem |

### 1. Self-Reinforcement Learning

**Herausforderung:** Ökonomische Modelle veralten bei Weltkontext-Änderungen.

**Lösung:** Automatisiertes Diagnose-Protokoll bei Prediction Errors:

| Error-Typ | Reaktion |
|-----------|----------|
| **Type I** (Rauschen) | Ignorieren |
| **Type II** (Parameter Drift) | System schlägt Koeffizienten-Update vor |
| **Type III** (Strukturbruch) | System erkennt neue Dimension, alarmiert Forscher |

**Impact:** BEATRIX wird nicht veralten, sondern kontinuierlich präziser.

### 2. Silicon Samples & Digital Twins

**Herausforderung:** Für Policy-Massnahmen muss Heterogenität ganzer Gesellschaften abgebildet werden.

**Lösung:** Digitale Zwillinge realer Gruppen (z.B. "Schweizer Wohnbevölkerung")
- Tausende LLM-Instanzen mit individuellen Kontextprofilen
- Test von Emergent Behavior (Herdenverhalten, Polarisierung)

**Validierung:** Prof. Luger prüft, ob digitale Zwillinge sich wie echte Menschen verhalten.

### 3. Natural Language Policy Interfaces

**Herausforderung:** 432 Dimensionen (10C × 8Ψ × 6 FEPSDE) sind für Nicht-Experten nicht handhabbar.

**Lösung:** Semantic Translation Layer
- Input: "Was passiert, wenn wir die Preise erhöhen?"
- Output: "Churn-Risiko steigt um 12% bei Segment B"

**Impact:** Verhaltensökonomik wird demokratisiert – auch KMUs, Gemeinden, Vereine erhalten Zugang.

### 4. Skalierung der Kalibrierungs-Basis

- Aktuell: ~1.500 codierte Experimente
- Ziel: 5.000+ Studien
- Methode: Crawler extrahieren automatisch experimentelle Designs aus wissenschaftlichen Papers

---

## Appendix: Kontext (Ψ) erklärt

### Das Praxis-Beispiel: SwissHealth Fitness-App

**Ausgangslage:**
- CHF 200 Jahresbonus für 10'000 Schritte/Tag
- App funktioniert technisch einwandfrei
- Nur 8% Nutzung

**Naive Analyse:** CHF 200 > CHF 0 → Bonus erhöhen auf CHF 400
**Ergebnis:** Nutzung steigt von 8% auf 9% (+1%)

**Kontext-Analyse (8Ψ):**

| Ψ-Dimension | Problem | Impact |
|-------------|---------|--------|
| Zeitlich | Bonus kommt am Jahresende (Present Bias) | **82%** |
| Institutionell | Opt-in Default verhindert passive Teilnahme | **71%** |
| Sozial | Keine soziale Komponente | **58%** |
| Emotional | "Überwachungs"-Wahrnehmung | 45% |
| Informationell | Kein Feedback während des Tages | 38% |
| Bonus-Höhe | CHF 200 vs. 400 | nur **12%** |

**Berechnung:**
```
U_eff = 200 × 0.04 = CHF 8 (gefühlter Wert)
```

Der Bonus fühlt sich an wie CHF 8, nicht CHF 200. **Das Problem ist der Kontext, nicht der Bonus.**

### Vergleich: Ohne vs. Mit BEATRIX

| Aspekt | OHNE BEATRIX | MIT BEATRIX |
|--------|--------------|-------------|
| Zeit | 7-8 Monate | 10 Wochen |
| Kosten | CHF 230k + CHF 1.8M | CHF 100k + CHF 50k |
| Diagnose | "Bonus zu niedrig" (falsch) | "Ψ_temporal = 82%" (korrekt) |
| Empfehlung | Bonus erhöhen | Wöchentliche Micro-Rewards |
| Ergebnis | +1% Nutzung | **+26% Nutzung** |
| ROI | Negativ | **+1'200%** |

---

## Appendix: Framework vs. Model

### Definition

| | Framework | Model |
|-|-----------|-------|
| **Zweck** | Denken organisieren | Vorhersagen machen |
| **Aussage** | "So sollte man über X nachdenken" | "X führt zu Y" |
| **Falsifizierbar?** | Nein (Meta-Ebene) | Ja (durch Daten) |
| **Bei Misserfolg** | Integriert als Information | Wird verworfen |
| **Analogie** | Kochbuch-Struktur | Einzelnes Rezept |

### Die Küchen-Analogie

**Framework = Kochbuch-Struktur:**
- Jedes Rezept hat Zutaten, Zubereitung, Garzeit, Serviervorschlag
- Sagt nicht WAS du kochst, sondern WIE man über Kochen nachdenkt

**Model = Spezifisches Rezept:**
- 400g Spaghetti + 150g Guanciale + 4 Eigelb + 100g Pecorino → 12 Min kochen → 4 Portionen
- Macht spezifische, testbare Vorhersage

### SwissHealth: Model-Denken vs. Framework-Denken

**OHNE Framework:**
1. Hypothese: "CHF 200 Bonus → +15% Nutzung"
2. Test: Nur +1% → Model falsifiziert
3. Neues Model: "CHF 400 Bonus" → wieder +1%
4. Schlussfolgerung: "Finanzielle Anreize funktionieren nicht"

**MIT Framework:**
1. Framework: U_eff = U_pot × f(Ψ)
2. Diagnose: Ψ_temporal = 82% Impact (Hauptbarriere)
3. Generiertes Model: "Wöchentliche CHF 4 statt jährliche CHF 200"
4. Test: +12% → Erfolg; wenn nicht → nächste Ψ-Dimension prüfen

**Erfolgswahrscheinlichkeit:**
- Model-only: ~30% (ein Schuss)
- Framework: ~83% (fünf informierte Versuche)

---

## Appendix: 20 KPIs im Vergleich

### 10 KPIs für Beratungsunternehmen

| # | KPI | Klassisch | EBF | Δ |
|---|-----|-----------|-----|---|
| 1 | Revenue per Consultant | CHF 400k | CHF 650k | **+63%** |
| 2 | Project Margin | 35% | 52% | **+17pp** |
| 3 | Utilization Rate | 65% | 78% | **+13pp** |
| 4 | Client Retention | 40% | 72% | **+32pp** |
| 5 | Time to Diagnosis | 4-6 Wochen | 3-5 Tage | **-85%** |
| 6 | Knowledge Retention | 20% | 85% | **+65pp** |
| 7 | Junior Effectiveness | 30% von Senior | 75% von Senior | **+45pp** |
| 8 | Proposal Win Rate | 25% | 45% | **+20pp** |
| 9 | Scalability | 4 Proj./Partner | 12 Proj./Partner | **3×** |
| 10 | IP Value | Gering (Commodity) | Hoch (Proprietär) | **∞** |

### 10 KPIs für Kundennutzen

| # | KPI | Klassisch | EBF | Δ |
|---|-----|-----------|-----|---|
| 1 | ROI der Empfehlung | 150% | 450% | **3×** |
| 2 | Implementierungserfolg | 30% | 75% | **+45pp** |
| 3 | Time to Results | 12-18 Monate | 3-6 Monate | **-70%** |
| 4 | Prognose-Genauigkeit | N/A | 73% | **∞** |
| 5 | Actionability | 40% | 85% | **+45pp** |
| 6 | Wissenstransfer | 15% | 60% | **+45pp** |
| 7 | Nachhaltigkeit (2 Jahre) | 25% | 65% | **+40pp** |
| 8 | Risikoreduktion | Gering | Hoch | **Qual.** |
| 9 | Cost per Outcome | CHF 50k/% | CHF 8k/% | **-84%** |
| 10 | Capability Building | 10% | 55% | **+45pp** |

### Die ultimative Einsicht

| Klassische Beratung | EBF + BEATRIX |
|---------------------|---------------|
| Geschäftsmodell: Verkaufe **ZEIT** kluger Menschen | Geschäftsmodell: Verkaufe **ERGEBNISSE** eines Systems |
| Problem: Zeit ist endlich, Klugheit nicht skalierbar | Vorteil: System ist skalierbar, lernt, wird besser |
| Ergebnis: Hohe Kosten, variable Qualität | Ergebnis: Niedrigere Kosten, konsistente Qualität |

**Der Unterschied ist wie zwischen HANDWERK und INDUSTRIALISIERUNG.**

---

*Dokument erstellt: 2026-01-18 | Für Innosuisse-Antrag BEATRIX*
