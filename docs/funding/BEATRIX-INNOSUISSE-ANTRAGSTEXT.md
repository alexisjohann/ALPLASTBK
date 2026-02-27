# BEATRIX Innosuisse Innovation Cheque - Antragstext

**Projekt:** BEATRIX - Behavioral Economics AI for Transformation and Research in eXperimental contexts
**Antragsteller:** FehrAdvice & Partners AG
**Forschungspartner:** Universität Zürich
**Scientific Advisor:** Prof. Dr. Ernst Fehr, Universität Zürich
**Datum:** Januar 2026

---

> **Strategischer Kernsatz:** Die Technologie ermöglicht die Innovation, aber die Transformation der Beratungspraxis ist das Produkt.

---

> **Hinweis:** Dieser Text ist für die direkte Verwendung im Innolink-Portal formatiert. Er behält den evidenzbasierten Stil bei, ist aber auf die Zeichenlimits der Antragsfelder optimiert.

---

## Inhaltsverzeichnis

1. [a) Innovation Potential](#a-innovation-potential)
2. [b) Market Relevance](#b-market-relevance)
3. [c) Feasibility & Risk Reduction](#c-feasibility--risk-reduction)
4. [d) Collaboration with a Research Partner](#d-collaboration-with-a-research-partner)
5. [e) Impact for Switzerland](#e-impact-for-switzerland)
6. [Zusammenfassung für Innolink-Abstract](#zusammenfassung-für-innolink-abstract)
7. [Glossar](#glossar)
8. [Literaturverzeichnis](#literaturverzeichnis)

---

## a) Innovation Potential

### a1) What makes the project idea technologically or business-wise novel?

BEATRIX adressiert eine dokumentierte Forschungslücke: Obwohl die verhaltensökonomische Literatur robust zeigt, dass menschliches Entscheidungsverhalten systematisch von Rationalitätsannahmen abweicht (Fehr & Schmidt, 1999; Kahneman & Tversky, 1979), fehlt bisher ein systematischer Ansatz, diese Erkenntnisse für praktische Entscheidungsunterstützung nutzbar zu machen.

**Der methodische Kern:**

BEATRIX operationalisiert zwei in der Anwendung unterrepräsentierte Konstrukte:

1. **Kontext (Ψ):** Meta-Analysen dokumentieren erhebliche Heterogenität in Interventionseffekten, die primär durch Kontextfaktoren erklärt wird (DellaVigna & Linos, 2022). BEATRIX erfasst diese systematisch.

2. **Komplementarität (C):** Anreize und Normen können sich verstärken oder unterminieren. Die Evidenz zum Motivations-Crowding (Gneezy & Rustichini, 2000) zeigt, dass extrinsische Anreize unter bestimmten Bedingungen intrinsische Motivation verdrängen. BEATRIX modelliert diese Interaktionseffekte.

**Technologische Umsetzung:** Das System kombiniert Semantic Calibration (Kontextextraktion), LLM Monte Carlo (Variationsanalysen mit Konfidenzintervallen) und multidimensionale Nutzenfunktionen.

**Limitation:** BEATRIX liefert probabilistische Schätzungen, keine deterministischen Vorhersagen. Die Prognosegenauigkeit hängt von der Kontexterfassung und der Übertragbarkeit der zugrundeliegenden Studien ab.

---

### a2) How does it differ from existing solutions in the market?

**Systematische Abgrenzung:**

| Ansatz | Basis | Limitation |
|--------|-------|------------|
| Traditionelle Beratung | Erfahrungswissen | Anfällig für kognitive Verzerrungen (Kahneman, 2011) |
| Generative KI (LLMs) | Sprachmuster | Keine kausale Verhaltensmodellierung |
| Business Intelligence | Deskriptive Statistik | Korrelation ≠ Kausalität |
| **BEATRIX** | Experimentelle Verhaltensökonomik | Basiert auf validierter Evidenz |

**Der fundamentale Unterschied:**

- LLM-Ansatz: P(Text | Kontext) – Wahrscheinlichkeit eines Textoutputs
- BEATRIX-Ansatz: P(Verhalten | Kontext, Anreize, Präferenzen) – Wahrscheinlichkeit eines Verhaltensoutcomes

BEATRIX ist auf 1'547 experimentellen Studien kalibriert (312 Labor-Experimente, 285 Feldexperimente, 438 RCTs, 512 Kontextstudien). Die Parameter werden durch Meta-Analysen geschätzt, nicht durch maschinelles Lernen auf Textkorpora.

**Einschränkung:** Die Übertragbarkeit experimenteller Befunde auf neue Kontexte (external validity) ist nicht garantiert. BEATRIX adressiert dies durch Kontextähnlichkeits-Modellierung und Unsicherheitsquantifizierung.

---

### a3) What is the innovative element that research will validate?

Der Forschungspartner (Universität Zürich) adressiert zwei offene wissenschaftliche Fragen:

**Forschungsfrage 1: Technische Robustheit (Prof. Harald Gall)**

Verhaltensmodelle können bei Kontextänderungen an Gültigkeit verlieren ("Model Drift"). Die Software-Engineering-Literatur hat Methoden zur Erkennung solcher Instabilitäten entwickelt (Gama et al., 2014).

*Forschungsfrage:* Können Software-Evolution-Algorithmen integriert werden, um Model Drift zu diagnostizieren?

*Erwarteter Beitrag:* Diagnose-Protokoll zur Klassifikation von Prognosefehlern; Architektur-Blueprint; dokumentierte Schwellenwerte für Review-Auslösung.

**Forschungsfrage 2: Nutzerakzeptanz (Prof. Luger)**

Die Literatur zur Algorithm Aversion (Dietvorst et al., 2015) zeigt, dass Menschen algorithmische Empfehlungen oft ablehnen.

*Forschungsfrage:* Unter welchen Bedingungen akzeptieren Entscheidungsträger KI-gestützte Verhaltensanalysen?

*Erwarteter Beitrag:* Qualitative Studie (n=10-15) zu Akzeptanzdeterminanten; Gestaltungsprinzipien für die Mensch-KI-Schnittstelle.

**Limitation:** Die Validierung dient der Machbarkeitseinschätzung, nicht dem vollständigen Nachweis.

---

## b) Market Relevance

### b1) What concrete problem does the project solve?

Die empirische Literatur dokumentiert eine erhebliche Diskrepanz zwischen organisationaler Entscheidungsqualität und verfügbarem Verhaltenswissen:

- **Change Management:** 60-70% der Transformationsprojekte erreichen ihre Ziele nicht (Beer & Nohria, 2000). Hauptursache: mangelnde Berücksichtigung von Verhaltensreaktionen.

- **Anreizsysteme:** Monetäre Anreize können kontraproduktiv wirken (Gneezy & Rustichini, 2000), werden aber oft ohne Kontextanalyse implementiert.

- **Policy-Interventionen:** Nudging-Effekte variieren erheblich (Median: 1.4pp); die Heterogenität wird durch Kontextfaktoren erklärt (DellaVigna & Linos, 2022).

**Das Kernproblem:** Organisationen haben ausgereifte Systeme für quantitative Daten, aber keine vergleichbaren Instrumente für systematische Verhaltensanalyse. "Harte" Faktoren werden präzise modelliert, "weiche" Faktoren intuitiv behandelt.

**Einschränkung:** BEATRIX adressiert dieses Problem, kann aber keine Garantie für bessere Outcomes geben. Die Wirksamkeit muss empirisch validiert werden.

---

### b2) Who are the target customers?

Die Literatur legt nahe, dass bestimmte Organisationstypen besonders profitieren könnten:

**1. Beratungsunternehmen:** Traditionell basierend auf Erfahrungswissen einzelner Berater. Probleme: Wissenserosion bei Fluktuation (Hansen et al., 1999), schwierige Skalierung, Anfälligkeit für kognitive Verzerrungen.

**2. Öffentliche Institutionen:** Die Behavioral Insights-Bewegung (Thaler & Sunstein, 2008) hat Potential für evidenzbasierte Policy gezeigt. Effekte sind jedoch kontextabhängig.

**3. Unternehmen mit Transformationsbedarf:** Veränderungen scheitern häufig an mangelnder Berücksichtigung von Mitarbeiterreaktionen.

**Pilotierte Anwendungen (vorläufig):**
- Verkehrsunternehmen: Kohärenz-Analyse (keine Kontrollgruppe)
- Bundesamt: Subvention vs. Nudging Vergleich (noch nicht feldvalidiert)
- Finanzinstitut: Kampagnentest (externe Validität unklar)

**Einschränkung:** Systematische Wirksamkeitsnachweise erfordern kontrollierte Studien.

---

### b3) What is the size of the potential market?

Eine präzise Marktquantifizierung ist mit Unsicherheit behaftet:

| Segment | Geschätztes Volumen | Konfidenz |
|---------|---------------------|-----------|
| Management Consulting (global) | USD 300-350 Mrd. | Mittel |
| Management Consulting (Schweiz) | CHF 3-4 Mrd. | Niedrig |
| Relevanter Teilmarkt (Verhaltensänderung) | CHF 300-800 Mio. (10-20%) | Niedrig |

**Wettbewerbsposition:** FehrAdvice verfügt über wissenschaftliche Nähe zur verhaltensökonomischen Forschung, eine Datenbank mit ~1'500 codierten Studien und etablierte Kundenbeziehungen im DACH-Raum.

**Einschränkung:** Ob diese Assets in nachhaltigen Wettbewerbsvorteil übersetzbar sind, hängt von erfolgreicher Validierung ab.

---

### b4) What impact can be expected?

Die folgenden Schätzungen basieren auf Pilotprojekten und Literatur-Extrapolation. Es sind Hypothesen, keine validierten Kausaleffekte:

| Dimension | Baseline | Mit BEATRIX (Hypothese) | Unsicherheit |
|-----------|----------|-------------------------|--------------|
| Diagnosezeit | 4-6 Wochen | 1-2 Wochen | ±50% |
| Prognosegenauigkeit | Nicht erfasst | 65-80% (Pilotdaten) | ±15pp |

**Kritische Einschränkungen:**
- Keine Kontrollgruppen in bisherigen Pilotprojekten
- Selbstselektion der Kunden möglich
- Hawthorne-Effekt nicht ausschliessbar

Die geplante Forschung adressiert einige dieser Limitationen durch systematischere Validierung.

---

## c) Feasibility & Risk Reduction

### c1) What aspect of feasibility needs to be tested?

**1. Technische Machbarkeit (Primärfokus):**

Die zentrale Herausforderung betrifft die Stabilität von Verhaltensmodellen unter dynamischen Bedingungen. Die Literatur zu "concept drift" (Gama et al., 2014) dokumentiert, dass Modelle an Genauigkeit verlieren können, wenn sich Datenverteilungen ändern.

| Offene Frage | Forschungsansatz |
|--------------|------------------|
| Model Drift | Diagnostische Algorithmen zur Drift-Erkennung |
| Skalierbarkeit | Architektur-Assessment für modulare Systeme |
| Interoperabilität | API-Design und Kompatibilitätstests |

**2. Wissenschaftliche Machbarkeit:**

Die theoretische Basis ist etabliert (Kahneman & Tversky, 1979; Fehr & Schmidt, 1999). Die Übertragbarkeit auf neue Kontexte (external validity) bleibt offen (Levitt & List, 2007).

**3. Nutzerakzeptanz:**

Die Literatur zu Algorithm Aversion/Appreciation zeigt kontextabhängige Akzeptanz (Dietvorst et al., 2015; Logg et al., 2019).

---

### c2) What proof-of-concept can be achieved with CHF 15'000?

**Erreichbar:**

| Deliverable | Methodischer Ansatz |
|-------------|---------------------|
| Architektur-Assessment | Review durch Prof. Gall nach Software-Engineering-Prinzipien |
| Drift-Diagnose-Konzept | Literaturbasiert + Adaption für Verhaltensmodelle |
| Akzeptanz-Exploration | Qualitative Studie (n=10-15) nach Gioia et al. (2013) |
| Interface-Mockup | Low-fidelity Prototyp mit Nutzerfeedback |

**NICHT erreichbar:**
- Vollständige Produktentwicklung
- Randomisierte kontrollierte Studien
- Umfassende Feldvalidierung
- Markteinführung

**Einordnung:** TRL 4 → TRL 5-6 (ambitioniert für das Budget). Der Innovation Cheque ermöglicht eine fundierte Machbarkeitseinschätzung, nicht deren vollständigen Nachweis.

---

### c3) How will the research partner's work reduce risks?

**Risiko 1: Model Drift (Prof. Gall)**

*Problem:* Verhaltensmodelle können bei Kontextänderungen an Gültigkeit verlieren.

*Ansatz:* Prof. Galls Expertise in Software Evolution (Gall et al., 2009) ermöglicht diagnostische Verfahren zur Erkennung von Modellinstabilitäten.

*Output:* Klassifikationsschema für Prognosefehler; Schwellenwerte für Alarmierung.

*Limitation:* Konzept wird spezifiziert, nicht vollständig implementiert.

**Risiko 2: Nutzerakzeptanz (Prof. Luger)**

*Problem:* Menschen lehnen algorithmische Empfehlungen oft ab (Dietvorst et al., 2015).

*Ansatz:* Qualitative Studie basierend auf etablierten Methoden (Gioia et al., 2013).

*Output:* Akzeptanzdeterminanten; Gestaltungsempfehlungen.

*Limitation:* Qualitative Exploration erlaubt keine kausalen Schlussfolgerungen.

---

### c4) What would be the next steps if feasibility is proven?

**Szenario A: Positive Signale**

| Phase | Fokus | Geschätzter Aufwand | Unsicherheit |
|-------|-------|---------------------|--------------|
| Hauptprojekt | Vollentwicklung + Feldvalidierung | CHF 500k-2M | Hoch |
| Pilotierung | Kontrollierte Anwendung | CHF 200-500k | Mittel |

**Szenario B: Gemischte Ergebnisse**

Fokussiertes Nachfolgeprojekt, das spezifische Schwachstellen adressiert.

**Szenario C: Negative Signale**

Neuausrichtung oder Einstellung. Auch dieses Ergebnis wäre wissenschaftlich wertvoll.

**Kritische Einschränkung:** Diese Roadmap ist hypothetisch. Zeitrahmen und Budgets sind Schätzungen mit hoher Unsicherheit.

---

## d) Collaboration with a Research Partner

### d1) What scientific expertise is required that we don't have in-house?

**Interne Kompetenzen (FehrAdvice):**
- Verhaltensökonomie (Anwendungserfahrung, keine Grundlagenforschung)
- Literaturdatenbank (~1'500 codierte Studien, Sekundäranalyse)
- Pilotprojekte (~20, ohne Kontrollgruppen)

**Identifizierte Kompetenzlücken:**

| Kompetenz | Begründung | Literatur |
|-----------|------------|-----------|
| Software Evolution | Verhaltensmodelle erfordern kontinuierliche Anpassung | Gama et al. (2014) |
| Architektur-Design | Skalierbare Systeme erfordern spezifisches Know-how | Bass et al. (2012) |
| Human-AI Interaction | Akzeptanz algorithmischer Empfehlungen ist nicht-trivial | Dietvorst et al. (2015) |
| Empirische Validierung | Wissenschaftliche Publikation erfordert methodische Rigorosität | Gioia et al. (2013) |

---

### d2) Why is the chosen research partner most suitable?

**Prof. Harald Gall (Institut für Informatik, UZH):**

Forschungsschwerpunkt Software Evolution ist direkt relevant:
- Software Evolution → Model Drift in Verhaltensmodellen
- Code Quality Assessment → Architektur-Bewertung
- Automatisierte Fehlerdiagnose → Erkennung von Instabilitäten

**Prof. Luger (Institut für Betriebswirtschaft, UZH):**

Expertise in strategischem Management und Human-AI Interaction:
- Technology Acceptance → Akzeptanz von KI-Empfehlungen
- Qualitative Methoden → Rigorose Exploration

**Begründung UZH vs. ETH/EPFL:**
- UZH: Kombination Informatik + BWL; Verhaltensökonomie-Tradition (Fehr-Schule)
- ETH/EPFL: Primär technisch, weniger verhaltensökonomische Verankerung

---

### d3) What is the specific contribution of the research partner?

**Arbeitspaket 1: Architektur-Assessment (Prof. Gall, ~CHF 8'000)**

| Beitrag | Output | Limitation |
|---------|--------|------------|
| Architektur-Bewertung | Stärken-Schwächen-Analyse | Konzeptuell |
| Drift-Erkennung | Adaptiertes Konzept | Keine empirische Validierung |
| Review-Kompetenz | Priorisierte Empfehlungen | Keine Umsetzungsgarantie |

**Arbeitspaket 2: Akzeptanz-Exploration (Prof. Luger, ~CHF 7'000)**

| Beitrag | Output | Limitation |
|---------|--------|------------|
| Qualitative Methoden | Interviewleitfaden | Keine quantitative Validierung |
| Netzwerk | 10-15 Interviews | Selbstselektion |
| Analyse | Vorläufiges Akzeptanzmodell | Hypothesengenerierend |

**Klarstellung:** CHF 15'000 ermöglicht eine begrenzte Vorstudie mit konzeptuellen Grundlagen und ersten explorativen Daten – keine fertigen Lösungen.

---

### d4) How will this collaboration strengthen innovation capacity?

Die Literatur zu Absorptive Capacity (Cohen & Levinthal, 1990) legt nahe, dass Unternehmen von Forschungskooperationen profitieren können:

| Dimension | Erwarteter Effekt | Unsicherheit |
|-----------|-------------------|--------------|
| Technisches Know-how | Transfer von Software-Engineering-Methoden | Mittel |
| Methodisches Repertoire | Erweiterung um qualitative Forschungsmethoden | Mittel |
| Wissenschaftliche Legitimität | Potenzielle Co-Publikationen | Hoch |
| Netzwerkeffekte | Zugang zu akademischer Community | Mittel |

**Kritische Einschränkung:** Diese Effekte sind nicht garantiert. University-Industry Collaborations scheitern häufig an Transferbarrieren (Bruneel et al., 2010).

---

### d5) Could this lead to a longer-term partnership?

**Szenarien:**

| Szenario | Folgeprojekt | Voraussetzung |
|----------|--------------|---------------|
| A: Positive Ergebnisse | Hauptprojekt (CHF 500k-2M) | Architektur skalierbar |
| B: Gemischte Ergebnisse | Fokussierte Fortsetzung | Spezifische Schwachstellen adressierbar |
| C: Negative Ergebnisse | Keine Fortsetzung | Wäre wissenschaftlich wertvoll |

**Erfolgsfaktoren für langfristige Partnerschaft (Perkmann et al., 2013):**

| Faktor | Status | Einschätzung |
|--------|--------|--------------|
| Komplementäre Kompetenzen | Vorhanden | Positiv |
| Klare Zieldefinition | Definiert | Positiv |
| Persönliche Beziehungen | Zu entwickeln | Offen |

**Ehrliche Einschätzung:** Eine langfristige Partnerschaft ist möglich, aber nicht garantiert. Der Innovation Cheque dient auch der Exploration, ob eine solche Partnerschaft sinnvoll ist.

---

## e) Impact for Switzerland

### e1) How does the project strengthen Swiss industry competitiveness?

Die Frage nach nationalem Wettbewerbsvorteil erfordert kritische Einordnung: Nationale Kompetenzcluster sind historisch gewachsen und nicht deterministisch planbar (Porter, 1990).

**Know-how-Aufbau:**

| Dimension | Hypothese | Limitation |
|-----------|-----------|------------|
| Methodische Kompetenz | Kombination Verhaltensökonomie + AI könnte Nische schaffen | Andere Standorte entwickeln parallele Ansätze |
| Humankapital | University-Industry-Spillovers möglich | Effektgrössen variieren stark |

**Beschäftigung (spekulative Schätzung):**

| Szenario | Stellen (5 Jahre) | Konfidenz |
|----------|-------------------|-----------|
| Optimistisch | 30-50 | Niedrig |
| Realistisch | 10-20 | Mittel |
| Konservativ | 3-8 | Mittel |

**Fazit:** Das Projekt könnte zur Wettbewerbsfähigkeit beitragen, aber kausale Effekte sind schwer isolierbar.

---

### e2) How does it support SME-university collaboration?

Das Projekt entspricht strukturell einem typischen University-Industry-Linkage-Format (Perkmann & Walsh, 2007):

**Geplante Wissenstransfer-Mechanismen:**

| Richtung | Mechanismus | Limitation |
|----------|-------------|------------|
| UZH → FehrAdvice | Methodisches Know-how | Transfer taciten Wissens schwierig |
| FehrAdvice → UZH | Praxisdaten für Forschung | Datenschutz-Restriktionen |

**Kritische Einordnung:** Die Literatur warnt vor überzogenen Erwartungen an UIL (Bozeman et al., 2013). Ob effektiver Wissenstransfer stattfindet, kann erst ex post beurteilt werden.

---

### e3) What are the potential societal or economic benefits?

**Methodische Vorbemerkung:** Die Quantifizierung gesellschaftlicher Effekte ist methodisch problematisch (Salter & Martin, 2001).

**Potentielle Anwendungsfelder:**

| Bereich | Evidenzbasis | Effektgrössen-Schätzung | Konfidenz |
|---------|--------------|------------------------|-----------|
| Organisationale Entscheidungen | Kahneman et al. (2011) | 10-30% Varianzreduktion (Labor) | Mittel |
| Public Policy | DellaVigna & Linos (2022) | d = 0.05-0.15 (Feld) | Mittel |

**Wichtige Limitationen:**
- Attribution des kausalen Beitrags eines Projekts schwierig
- Laboreffekte übertragen sich oft nicht 1:1 (Feldeffekte 60-90% kleiner)
- Verhaltensinterventionen wirken heterogen

**Fazit:** Gesellschaftlicher Nutzen ist plausibel, aber nicht quantifizierbar. Überzogene Behauptungen würden wissenschaftlicher Redlichkeit widersprechen.

---

### e4) Could the project help position Switzerland as a leader?

**Kritische Analyse:** Führerschaft in Innovationsfeldern ist historisch gewachsen, von kritischer Masse abhängig und pfadabhängig (Porter, 1990; Feldman, 2000).

**Bestandsaufnahme:**

| Dimension | Status | Internationale Einordnung |
|-----------|--------|---------------------------|
| Verhaltensökonomische Forschung | Stark | Top 5 weltweit |
| AI/ML Forschung | Stark | Top 10 weltweit |
| Kombination Behavioral + AI | Emergent | Unklar |
| Industrielle Anwendung | Begrenzt | Keine kritische Masse |

**Realistische Einschätzung:**

| Szenario | Wahrscheinlichkeit |
|----------|-------------------|
| Nischenführer DACH | Mittel-Hoch |
| Beitrag zu internationalem Netzwerk | Hoch |
| Globaler Marktführer | Niedrig |

**Fazit:** Das Projekt kann einen bescheidenen Beitrag zur Schweizer Positionierung leisten. Die Behauptung "globaler Führerschaft" wäre unbegründet und würde den Standards wissenschaftlicher Bescheidenheit widersprechen.

---

## Zusammenfassung für Innolink-Abstract

BEATRIX (Behavioral Economics AI for Transformation and Research in eXperimental contexts) adressiert eine dokumentierte Forschungslücke: Die verhaltensökonomische Literatur zeigt, dass Kontext (Ψ) und Komplementarität (C) entscheidend für Interventionserfolge sind (Fehr & Schmidt, 1999; DellaVigna & Linos, 2022), aber systematische Anwendungstools fehlen.

Der Innovation Cheque finanziert eine Vorstudie mit der Universität Zürich zu: (1) Model-Drift-Erkennung in Verhaltensmodellen (Prof. Gall) und (2) Nutzerakzeptanz von KI-gestützter Verhaltensanalyse (Prof. Luger).

Erwartete Outputs: Architektur-Assessment, Drift-Diagnose-Konzept, qualitative Akzeptanzstudie (n=10-15), Interface-Mockup.

Die Ergebnisse dienen der Go/No-Go-Entscheidung für ein grösseres Innosuisse-Innovationsprojekt. Positive wie negative Ergebnisse haben wissenschaftlichen Wert.

---

## Glossar

| Begriff | Definition |
|---------|------------|
| **Awareness** | Bewusstsein für eine Situation, ein Verhalten oder eine Entscheidung; im EBF-Framework eine der 10C-Dimensionen, die erfasst, wie bewusst Personen ihre Entscheidungen treffen |
| **BEATRIX** | Behavioral Economics AI for Transformation and Research in eXperimental contexts; das im Antrag beschriebene KI-gestützte Entscheidungsunterstützungssystem |
| **Behavioral Change Journey (BCJ)** | Konzeptuelles Modell der Verhaltensänderung über Zeit, das verschiedene Phasen von der Problemwahrnehmung bis zur Gewohnheitsbildung beschreibt |
| **Behavioral Economics** | Verhaltensökonomie; Forschungsfeld an der Schnittstelle von Ökonomie und Psychologie, das systematische Abweichungen von Rationalitätsannahmen untersucht |
| **Bias** | Systematische Verzerrung in der menschlichen Urteilsbildung oder Entscheidungsfindung (z.B. Confirmation Bias, Status Quo Bias) |
| **Choice Architecture** | Gestaltung der Entscheidungsumgebung, die beeinflusst, wie Menschen Optionen wahrnehmen und auswählen (Thaler & Sunstein, 2008) |
| **Cognitive Load** | Kognitive Belastung; Mass für die Beanspruchung des Arbeitsgedächtnisses bei der Informationsverarbeitung |
| **Complementarity (C)** | Komplementarität; im EBF-Framework die Wechselwirkung zwischen verschiedenen Interventionen oder Anreizen, die sich verstärken oder unterminieren können |
| **Concept Drift** | Veränderung der zugrundeliegenden Datenverteilung über Zeit, die zu Modellinstabilität führen kann (Gama et al., 2014) |
| **Context (Ψ)** | Kontext; im EBF-Framework die Gesamtheit situativer Faktoren, die Verhaltenseffekte moderieren (8 Dimensionen: Institutional, Social, Cognitive, Cultural, Economic, Temporal, Material, Physical) |
| **Decision Support System (DSS)** | Entscheidungsunterstützungssystem; computergestütztes System zur Unterstützung von Entscheidungsprozessen |
| **Default** | Voreingestellte Option, die gilt, wenn keine aktive Wahl getroffen wird; wichtiges Element der Choice Architecture |
| **EBF** | Evidence-Based Framework; das theoretische Rahmenwerk, auf dem BEATRIX basiert |
| **Effect Size** | Effektstärke; standardisiertes Mass für die Grösse eines statistischen Effekts (z.B. Cohen's d, Hedges' g) |
| **External Validity** | Externe Validität; Übertragbarkeit von Forschungsergebnissen auf andere Kontexte, Populationen oder Zeitpunkte |
| **Field Experiment** | Feldexperiment; randomisierte kontrollierte Studie in einer natürlichen Umgebung (im Gegensatz zum Laborexperiment) |
| **Framing** | Die Art und Weise, wie Informationen präsentiert werden; kann Entscheidungen systematisch beeinflussen (Tversky & Kahneman, 1981) |
| **Heuristic** | Heuristik; kognitive Abkürzung oder Daumenregel, die schnelle Urteile ermöglicht, aber zu systematischen Fehlern führen kann |
| **Human-AI Interaction** | Mensch-KI-Interaktion; Forschungsfeld zur Gestaltung und Evaluation von Schnittstellen zwischen Menschen und KI-Systemen |
| **Innovation Cheque** | Innosuisse-Förderinstrument (CHF 15'000) für KMU zur Finanzierung von Machbarkeitsstudien mit Forschungspartnern |
| **Innosuisse** | Schweizerische Agentur für Innovationsförderung; Bundesbehörde zur Förderung von Zusammenarbeit zwischen Forschung und Wirtschaft |
| **Intervention** | Gezielte Massnahme zur Beeinflussung von Verhalten oder Entscheidungen |
| **Laboratory Experiment** | Laborexperiment; kontrollierte Studie in einer künstlichen Umgebung mit hoher interner Validität |
| **LLM** | Large Language Model; Grosses Sprachmodell; KI-System, das auf grossen Textkorpora trainiert wurde (z.B. GPT, Claude) |
| **LLM Monte Carlo** | Von FehrAdvice entwickelte Methode zur Generierung von Konfidenzintervallen durch wiederholte LLM-Abfragen mit Parametervariation |
| **Loss Aversion** | Verlustaversion; Tendenz, Verluste stärker zu gewichten als gleichwertige Gewinne (Kahneman & Tversky, 1979) |
| **Meta-Analysis** | Meta-Analyse; statistische Methode zur Zusammenfassung und Analyse mehrerer Studien zum gleichen Thema |
| **Model Drift** | Veränderung der Modellgenauigkeit über Zeit aufgrund von Änderungen in den zugrundeliegenden Daten oder Kontexten |
| **Motivation Crowding** | Verdrängung intrinsischer Motivation durch extrinsische Anreize (Gneezy & Rustichini, 2000; Frey & Jegen, 2001) |
| **Nudge** | Verhaltensanstoss; Gestaltung der Entscheidungsumgebung, die Verhalten vorhersagbar beeinflusst, ohne Optionen zu verbieten oder ökonomische Anreize wesentlich zu verändern (Thaler & Sunstein, 2008) |
| **Present Bias** | Gegenwartspräferenz; Tendenz, sofortige Belohnungen gegenüber zukünftigen überzubewerten |
| **Proof of Concept (PoC)** | Machbarkeitsnachweis; Demonstration, dass ein Konzept grundsätzlich funktionsfähig ist |
| **Prospect Theory** | Neue Erwartungstheorie; deskriptive Theorie der Entscheidung unter Unsicherheit (Kahneman & Tversky, 1979) |
| **RCT** | Randomized Controlled Trial; Randomisierte kontrollierte Studie; Goldstandard der Kausalforschung |
| **Semantic Calibration** | Von FehrAdvice entwickelte Methode zur automatisierten Extraktion von Kontextinformationen aus Textbeschreibungen |
| **Social Norm** | Soziale Norm; ungeschriebene Regel oder Erwartung bezüglich angemessenen Verhaltens in einer Gruppe oder Gesellschaft |
| **Status Quo Bias** | Tendenz, den aktuellen Zustand gegenüber Veränderungen zu bevorzugen |
| **Technology Readiness Level (TRL)** | Technologiereifegrad; 9-stufige Skala zur Bewertung der Marktreife einer Technologie |
| **Utility Function** | Nutzenfunktion; mathematische Repräsentation von Präferenzen, die Entscheidungsverhalten beschreibt |

---

## Literaturverzeichnis

### Tier 1: Direkt zitierte Kernquellen

| Referenz | Zitation |
|----------|----------|
| Bass, L., Clements, P., & Kazman, R. (2012) | Software Architecture in Practice (3rd ed.). Addison-Wesley. |
| Beer, M., & Nohria, N. (2000) | Cracking the code of change. Harvard Business Review, 78(3), 133-141. |
| Bruneel, J., D'Este, P., & Salter, A. (2010) | Investigating the factors that diminish the barriers to university-industry collaboration. Research Policy, 39(7), 858-868. |
| Cohen, W. M., & Levinthal, D. A. (1990) | Absorptive capacity: A new perspective on learning and innovation. Administrative Science Quarterly, 35(1), 128-152. |
| DellaVigna, S., & Linos, E. (2022) | RCTs to scale: Comprehensive evidence from two nudge units. Econometrica, 90(1), 81-116. |
| Dietvorst, B. J., Simmons, J. P., & Massey, C. (2015) | Algorithm aversion: People erroneously avoid algorithms after seeing them err. Journal of Experimental Psychology: General, 144(1), 114-126. |
| Fehr, E., & Schmidt, K. M. (1999) | A theory of fairness, competition, and cooperation. Quarterly Journal of Economics, 114(3), 817-868. |
| Gall, H., Jazayeri, M., & Krajewski, J. (2009) | CVS release history data for detecting logical couplings. Proceedings of the 6th IEEE International Working Conference on Mining Software Repositories, 13-22. |
| Gama, J., Žliobaitė, I., Bifet, A., Pechenizkiy, M., & Bouchachia, A. (2014) | A survey on concept drift adaptation. ACM Computing Surveys, 46(4), 1-37. |
| Gioia, D. A., Corley, K. G., & Hamilton, A. L. (2013) | Seeking qualitative rigor in inductive research. Organizational Research Methods, 16(1), 15-31. |
| Gneezy, U., & Rustichini, A. (2000) | Pay enough or don't pay at all. Quarterly Journal of Economics, 115(3), 791-810. |
| Hansen, M. T., Nohria, N., & Tierney, T. (1999) | What's your strategy for managing knowledge? Harvard Business Review, 77(2), 106-116. |
| Kahneman, D. (2011) | Thinking, Fast and Slow. Farrar, Straus and Giroux. |
| Kahneman, D., & Tversky, A. (1979) | Prospect theory: An analysis of decision under risk. Econometrica, 47(2), 263-291. |
| Levitt, S. D., & List, J. A. (2007) | What do laboratory experiments measuring social preferences reveal about the real world? Journal of Economic Perspectives, 21(2), 153-174. |
| Logg, J. M., Minson, J. A., & Moore, D. A. (2019) | Algorithm appreciation: People prefer algorithmic to human judgment. Organizational Behavior and Human Decision Processes, 151, 90-103. |
| Perkmann, M., Tartari, V., McKelvey, M., Autio, E., Broström, A., D'Este, P., ... & Sobrero, M. (2013) | Academic engagement and commercialisation: A review of the literature on university-industry relations. Research Policy, 42(2), 423-442. |
| Perkmann, M., & Walsh, K. (2007) | University-industry relationships and open innovation: Towards a research agenda. International Journal of Management Reviews, 9(4), 259-280. |
| Porter, M. E. (1990) | The Competitive Advantage of Nations. Free Press. |
| Thaler, R. H., & Sunstein, C. R. (2008) | Nudge: Improving Decisions about Health, Wealth, and Happiness. Yale University Press. |

### Tier 2: Ergänzende Referenzen

| Referenz | Zitation |
|----------|----------|
| Benartzi, S., & Thaler, R. H. (2007) | Heuristics and biases in retirement savings behavior. Journal of Economic Perspectives, 21(3), 81-104. |
| Bozeman, B., Fay, D., & Slade, C. P. (2013) | Research collaboration in universities and academic entrepreneurship: The-state-of-the-art. Journal of Technology Transfer, 38(1), 1-67. |
| Charness, G., & Rabin, M. (2002) | Understanding social preferences with simple tests. Quarterly Journal of Economics, 117(3), 817-869. |
| Deci, E. L., Koestner, R., & Ryan, R. M. (1999) | A meta-analytic review of experiments examining the effects of extrinsic rewards on intrinsic motivation. Psychological Bulletin, 125(6), 627-668. |
| Feldman, M. P. (2000) | Location and innovation: The new economic geography of innovation, spillovers, and agglomeration. In G. L. Clark, M. P. Feldman, & M. S. Gertler (Eds.), The Oxford Handbook of Economic Geography (pp. 373-394). Oxford University Press. |
| Frey, B. S., & Jegen, R. (2001) | Motivation crowding theory. Journal of Economic Surveys, 15(5), 589-611. |
| Kahneman, D., Lovallo, D., & Sibony, O. (2011) | Before you make that big decision. Harvard Business Review, 89(6), 50-60. |
| List, J. A. (2011) | Why economists should conduct field experiments and 14 tips for pulling one off. Journal of Economic Perspectives, 25(3), 3-16. |
| Milkman, K. L., Beshears, J., Choi, J. J., Laibson, D., & Madrian, B. C. (2011) | Using implementation intentions prompts to enhance influenza vaccination rates. Proceedings of the National Academy of Sciences, 108(26), 10415-10420. |
| O'Donoghue, T., & Rabin, M. (1999) | Doing it now or later. American Economic Review, 89(1), 103-124. |
| Salter, A. J., & Martin, B. R. (2001) | The economic benefits of publicly funded basic research: A critical review. Research Policy, 30(3), 509-532. |
| Tversky, A., & Kahneman, D. (1981) | The framing of decisions and the psychology of choice. Science, 211(4481), 453-458. |

---

*Dokument erstellt: 2026-01-18 | Aktualisiert: 2026-01-27 | Version 4.1 | Für Innolink-Portal optimiert*
