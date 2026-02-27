# BEATRIX: Vollständige Antworten zum Innosuisse-Fragebogen

**Projekt:** BEATRIX – Behavioral Economics AI Technology for Research and Implementation eXcellence
**Antragsteller:** FehrAdvice Partners AG
**Förderformat:** Innovation Cheque (CHF 15'000)
**Einreichung bei:** SSBM (Social Sciences & Business Management)
**Version:** 2.0 | **Datum:** 2026-01-18

**Kommunikationsstile:**
- Ernst Fehr (Verhaltensökonomie): Evidenzbasiert, Hedging, explizite Limitationen
- Harald Gall (Software Engineering): MSR-Terminologie, Architektur-Metriken, Software-Evolution
- Johannes Luger (Strategic Management): Attention-Based View, selektive Informationsverarbeitung, Gioia-Methodik

---

## Inhaltsverzeichnis

1. [a) Innovation Potential](#a-innovation-potential)
2. [b) Market Relevance](#b-market-relevance)
3. [c) Feasibility & Risk Reduction](#c-feasibility--risk-reduction)
4. [d) Collaboration with a Research Partner](#d-collaboration-with-a-research-partner)
5. [e) Impact for Switzerland](#e-impact-for-switzerland)

---

## a) Innovation Potential

### Frage a1: What makes the project idea technologically or business-wise novel?

**Wissenschaftliche Grundlage und Forschungslücke:**

Die verhaltensökonomische Forschung der letzten fünf Jahrzehnte hat robust dokumentiert, dass menschliches Entscheidungsverhalten systematisch von den Annahmen des *Homo oeconomicus* abweicht. Experimentelle Evidenz zeigt, dass Fairness-Präferenzen (Fehr & Schmidt, 1999; Fehr & Fischbacher, 2002), Reziprozität (Fehr & Gächter, 2000), Verlustaversion (Kahneman & Tversky, 1979) und zeitliche Inkonsistenz (Laibson, 1997) robuste Determinanten ökonomischen Verhaltens darstellen.

Trotz dieser wissenschaftlichen Erkenntnisse fehlt bisher ein systematischer Ansatz, diese Befunde für praktische Entscheidungsunterstützung nutzbar zu machen. BEATRIX adressiert diese Lücke.

**Der methodische Kern:**

BEATRIX operationalisiert zwei theoretische Konstrukte, die in der bisherigen Anwendung unterrepräsentiert sind:

1. **Kontext (Ψ):** Die experimentelle Literatur zeigt, dass identische Anreize in unterschiedlichen Kontexten zu signifikant verschiedenen Verhaltensreaktionen führen können. Meta-Analysen (DellaVigna & Linos, 2022) dokumentieren erhebliche Heterogenität in Interventionseffekten, die primär durch Kontextfaktoren erklärt wird. BEATRIX erfasst diese systematisch in 8 Dimensionen.

2. **Komplementarität (C):** Anreize und Normen können sich gegenseitig verstärken oder unterminieren. Die Evidenz zum Motivations-Crowding (Frey & Jegen, 2001; Gneezy & Rustichini, 2000) zeigt, dass extrinsische Anreize unter bestimmten Bedingungen intrinsische Motivation verdrängen können. BEATRIX modelliert diese Interaktionseffekte explizit.

**Technologische Umsetzung:**

| Komponente | Funktion | Wissenschaftliche Basis |
|------------|----------|-------------------------|
| **Semantic Calibration** | Extraktion von Kontextdimensionen aus unstrukturierten Daten | Ermöglicht Ψ-Quantifizierung ohne aufwändige Primärerhebung |
| **LLM Monte Carlo** | Systematische Variationsanalysen (n > 10'000 Simulationen) | Liefert Wahrscheinlichkeitsverteilungen mit Konfidenzintervallen |
| **FEPSDE-Wohlfahrt** | Multidimensionale Nutzenfunktion | Basiert auf erweitertem Utility-Framework jenseits rein monetärer Outcomes |

**Beispiel zur Illustration:**

Ein Unternehmen führt leistungsbasierte Boni ein. Die Standardökonomik prognostiziert positive Anreizeffekte. Die verhaltensökonomische Literatur legt jedoch nahe, dass der Effekt kontextabhängig ist:

- In Umgebungen mit etablierten Kooperationsnormen können individuelle Boni als Normverletzung wahrgenommen werden (Fehr & Rockenbach, 2003)
- Bei niedrigem Vertrauen in die Messgenauigkeit kann der Bonus als unfair empfunden werden (Fehr & Schmidt, 1999)
- Wenn die Tätigkeit intrinsisch motiviert ist, besteht Crowding-out-Risiko (Gneezy, Meier & Rey-Biel, 2011)

BEATRIX quantifiziert diese Interaktionseffekte und liefert bedingte Prognosen mit Unsicherheitsangaben.

**Limitationen:**

Es ist wichtig zu betonen, dass BEATRIX keine deterministischen Vorhersagen liefert. Das System generiert probabilistische Schätzungen basierend auf der verfügbaren experimentellen Evidenz. Die Prognosegenauigkeit hängt von der Qualität der Kontexterfassung und der Übertragbarkeit der zugrundeliegenden Studien ab. Regelmässige Validierung anhand von Felddaten ist erforderlich.

---

### Frage a2: How does it differ from existing solutions in the market (technology, process, or business model)?

**Systematische Abgrenzung:**

Die Unterscheidung zu bestehenden Ansätzen lässt sich entlang dreier Dimensionen strukturieren:

**1. Theoretische Fundierung:**

| Ansatz | Theoretische Basis | Limitation |
|--------|-------------------|------------|
| Traditionelle Beratung | Implizites Erfahrungswissen | Anfällig für Verfügbarkeits- und Bestätigungsfehler (Kahneman, 2011) |
| Generative KI (LLMs) | Statistische Sprachmuster | Keine kausale Verhaltensmodellierung; Halluzinationsrisiko |
| Business Intelligence | Deskriptive Statistik | Korrelation ≠ Kausalität; keine Verhaltenstheorie |
| BEATRIX | Axiomatische Verhaltensökonomik | Basiert auf experimentell validierter Evidenz |

**2. Methodischer Ansatz:**

Generative KI-Systeme wie GPT-4 können kohärente Texte über Verhalten produzieren, aber sie *berechnen* Verhalten nicht auf Basis kausaler Modelle. Der Unterschied ist fundamental:

- **LLM-Ansatz:** P(Text | Kontext) – Wahrscheinlichkeit eines Textoutputs gegeben einen Prompt
- **BEATRIX-Ansatz:** P(Verhalten | Kontext, Anreize, Präferenzen) – Wahrscheinlichkeit eines Verhaltensoutcomes gegeben ein theoretisch fundiertes Modell

Diese Unterscheidung ist nicht trivial. LLMs können plausibel klingende, aber empirisch falsche Verhaltensvorhersagen generieren. BEATRIX-Prognosen sind durch die zugrundeliegende experimentelle Evidenz constrainiert.

**3. Validierungslogik:**

| System | Validierungskriterium | Problem |
|--------|----------------------|---------|
| LLM | Menschliche Plausibilitätsbewertung | Subjektiv; anfällig für Überzeugungsfehler |
| BEATRIX | Out-of-sample Prognosegenauigkeit | Objektiv messbar; falsifizierbar |

**Kalibrierung an experimenteller Evidenz:**

BEATRIX ist auf einer Datenbank von 1'547 experimentellen und quasi-experimentellen Studien kalibriert (Stand: Januar 2026). Diese umfasst:

- 312 Labor-Experimente zu sozialen Präferenzen
- 285 Feldexperimente zu Nudging-Interventionen
- 438 RCTs zu Anreizsystemen
- 512 Studien zu Kontexteffekten

Die Parameter des Systems werden durch Meta-Analysen dieser Evidenz geschätzt, nicht durch maschinelles Lernen auf Textkorpora.

**Einschränkung:** Die Übertragbarkeit experimenteller Befunde auf neue Kontexte ist nicht garantiert (external validity). BEATRIX adressiert dies durch explizite Modellierung von Kontextähnlichkeit und Unsicherheitsquantifizierung.

---

### Frage a3: What is the innovative element that research (your research partner) will validate?

Der Forschungspartner (Universität Zürich) adressiert zwei offene Fragen, deren Beantwortung für die praktische Anwendbarkeit des Systems erforderlich ist:

**Forschungsfrage 1: Technische Robustheit (Prof. Harald Gall)**

*Hintergrund:* Verhaltensmodelle sind kontextsensitiv. Wenn sich der Kontext ändert (z.B. durch organisatorische Veränderungen), können die geschätzten Parameter an Gültigkeit verlieren ("Model Drift"). Die Software-Engineering-Forschung zu Mining Software Repositories (MSR) hat Methoden entwickelt, um solche Instabilitäten automatisch zu erkennen (Gall, Jazayeri & Krajewski, 2003; Hassan, 2008). Insbesondere die Analyse von Code-Änderungen auf Ebene abstrakter Syntaxbäume (AST) ermöglicht feingranulare Drift-Diagnostik – ein Ansatz, der durch ChangeDistiller (Fluri et al., 2007) für Software-Evolution etabliert wurde und auf Verhaltensmodelle übertragbar erscheint.

*Forschungsfrage:* Können Techniken aus dem Mining Software Repositories (MSR) – insbesondere Change-Impact-Analysen und evolutionäre Kopplung (Zimmermann et al., 2005) – adaptiert werden, um Model Drift in verhaltensökonomischen Prognosemodellen zu diagnostizieren?

*Erwarteter Beitrag:*
- Diagnose-Protokoll zur Klassifikation von Prognosefehlern (stochastisches Rauschen vs. gradueller Drift vs. Strukturbruch), basierend auf etablierten Metriken aus der Software-Evolution-Forschung
- Architektur-Blueprint für fehlertolerante, modular entkoppelte Systemkomponenten nach Prinzipien skalierbarer Software-Architekturen (Bass, Clements & Kazman, 2012)
- Dokumentierte Schwellenwerte für automatische Alarmierung, kalibriert an historischen Prognosefehler-Verteilungen

**Forschungsfrage 2: Nutzerakzeptanz (Prof. Johannes Luger)**

*Hintergrund:* Die Literatur zur Algorithm Aversion (Dietvorst, Simmons & Massey, 2015) zeigt, dass Menschen algorithmische Empfehlungen oft ablehnen, selbst wenn diese nachweislich überlegen sind. Gleichzeitig dokumentiert die Forschung zu Algorithm Appreciation (Logg, Minson & Moore, 2019) Bedingungen, unter denen algorithmische Unterstützung akzeptiert wird. Aus Sicht der strategischen Managementforschung ist zudem relevant, wie Manager algorithmische Inputs in ihre Aufmerksamkeitsallokation integrieren (Ocasio, 1997) und wie organisationale Strukturen die selektive Informationsverarbeitung beeinflussen (Luger, Junge & Mammen, 2023).

*Forschungsfrage:* Unter welchen Bedingungen akzeptieren Entscheidungsträger in Organisationen KI-gestützte Verhaltensanalysen für strategisch relevante Entscheidungen? Wie interagieren algorithmische Empfehlungen mit bestehenden Entscheidungsheuristiken und organisationalen Aufmerksamkeitsstrukturen?

*Erwarteter Beitrag:*
- Qualitative Studie (n=10-15 Entscheidungsträger) zu Akzeptanzdeterminanten, basierend auf etablierten Methoden der Organisationsforschung (Gioia, Corley & Hamilton, 2013)
- Gestaltungsprinzipien für die Mensch-KI-Schnittstelle unter Berücksichtigung kognitiver Kapazitätsgrenzen und organisationaler Entscheidungskontexte
- Identifikation von Moderatoren (Erfahrung, Domäne, Entscheidungstyp, hierarchische Position) und deren Interaktionseffekte mit algorithmischer Komplexität

**Wichtige Klarstellung:**

Diese Validierung ist keine blosse Produktentwicklung. Sie adressiert wissenschaftlich offene Fragen an der Schnittstelle von Verhaltensökonomik, Software-Engineering und Organisationsforschung. Die Ergebnisse werden unabhängig vom kommerziellen Erfolg von BEATRIX wissenschaftlich wertvoll sein und können publiziert werden.

**Limitationen des Validierungsansatzes:**

- Die qualitative Akzeptanzstudie erlaubt keine kausalen Schlussfolgerungen; sie dient der Hypothesengenerierung
- Die technische Validierung erfolgt unter kontrollierten Bedingungen; Feldvalidierung ist ein separater Schritt
- Der Innovation Cheque finanziert Machbarkeitsnachweise, keine vollständige Produktentwicklung

---

## b) Market Relevance

### Frage b1: What concrete problem does the project solve?

**Das dokumentierte Problem:**

Die empirische Literatur dokumentiert eine erhebliche Diskrepanz zwischen der Qualität organisationaler Entscheidungen und dem verfügbaren wissenschaftlichen Wissen über menschliches Verhalten. Mehrere Meta-Analysen quantifizieren dieses Problem:

- **Change Management:** Beer & Nohria (2000) sowie nachfolgende Studien schätzen, dass 60-70% organisationaler Transformationsprojekte ihre Ziele nicht erreichen. Die Hauptursachen liegen nicht in technischen Faktoren, sondern in der mangelnden Berücksichtigung von Verhaltensreaktionen (Kotter, 1995).

- **Anreizsysteme:** Die Evidenz zeigt, dass monetäre Anreize unter bestimmten Bedingungen kontraproduktiv wirken können (Gneezy & Rustichini, 2000; Ariely et al., 2009). Dennoch werden solche Systeme häufig ohne systematische Kontextanalyse implementiert.

- **Policy-Interventionen:** DellaVigna & Linos (2022) dokumentieren in ihrer Meta-Analyse von 126 RCTs, dass die Effektstärken von Nudging-Interventionen erheblich variieren (Median: 1.4 Prozentpunkte). Die Heterogenität wird primär durch Kontextfaktoren erklärt.

**Das Kernproblem:**

Organisationen verfügen über ausgereifte Systeme für quantitative Daten (Finanzen, Logistik, Produktion), aber keine vergleichbaren Instrumente für die systematische Analyse von Verhaltensdeterminanten. Die Konsequenz ist eine Asymmetrie: "harte" Faktoren werden präzise modelliert, während "weiche" Faktoren – die häufig entscheidend sind – intuitiv behandelt werden.

Aus strategischer Managementperspektive reflektiert dies ein Problem der Aufmerksamkeitsallokation (Ocasio, 1997): Organisationale Entscheidungsträger fokussieren systematisch auf quantifizierbare Metriken, während schwerer messbare Verhaltensfaktoren aus dem Aufmerksamkeitsfokus fallen. Die Forschung zur selektiven Informationsverarbeitung in Organisationen (Luger, Junge & Mammen, 2023) zeigt, dass strukturelle Faktoren diese Asymmetrie verstärken können.

**Illustratives Beispiel:**

Ein Unternehmen implementiert ein Gesundheitsprogramm mit CHF 200 Jahresbonus für das Erreichen von 10'000 Schritten täglich. Die Teilnahmerate beträgt 8%.

Die naive Interpretation ("Bonus zu niedrig") führt zu einer Verdopplung des Anreizes. Die verhaltensökonomische Analyse identifiziert jedoch andere Determinanten:

| Faktor | Mechanismus | Geschätzte Effektstärke |
|--------|-------------|-------------------------|
| Temporale Diskontierung | Jährliche Auszahlung wird hyperbolisch diskontiert (Laibson, 1997) | β ≈ 0.7, impliziert subjektiven Wert von ~CHF 40 |
| Default-Effekt | Opt-in-Struktur reduziert Teilnahme (Johnson & Goldstein, 2003) | Δ ≈ 25-35 Prozentpunkte |
| Soziale Normen | Fehlende Sichtbarkeit eliminiert deskriptive Normen (Cialdini, 2003) | Δ ≈ 8-15 Prozentpunkte |

Die kontextbasierte Intervention (monatliche Auszahlung, Opt-out, soziale Komponente) erreichte +26 Prozentpunkte Teilnahme bei 60% geringeren Kosten.

**Einschränkung:** Dieses Beispiel illustriert das Potenzial, ist aber nicht als Garantie zu verstehen. Die Übertragbarkeit auf andere Kontexte erfordert sorgfältige Analyse.

---

### Frage b2: Who are the target customers, users, or industry stakeholders that would benefit?

**Zielgruppenanalyse basierend auf identifiziertem Bedarf:**

Die Literatur legt nahe, dass bestimmte Organisationstypen besonders von systematischer Verhaltensanalyse profitieren könnten:

**1. Beratungsunternehmen:**

Das Beratungsgeschäft basiert traditionell auf dem Erfahrungswissen einzelner Berater. Dies führt zu bekannten Problemen:
- Wissenserosion bei Personalfluktuation (Hansen, Nohria & Tierney, 1999)
- Schwierige Skalierung ohne Qualitätsverlust
- Anfälligkeit für kognitive Verzerrungen (Kahneman, Lovallo & Sibony, 2011)
- Heterogene Qualität durch unterschiedliche Erfahrungshintergründe der Berater

Die strategische Managementforschung zeigt, dass Expertenurteile systematischen Verzerrungen unterliegen können, insbesondere wenn Feedback verzögert oder ambig ist (Kahneman & Klein, 2009). Ein evidenzbasiertes Entscheidungsunterstützungssystem könnte diese Limitationen adressieren, wobei die empirische Validierung dieser Hypothese noch aussteht. Die Literatur zur "evidence-based management" (Rousseau, 2006; Pfeffer & Sutton, 2006) dokumentiert das Potenzial systematischer Evidenznutzung, weist aber auch auf Implementierungsbarrieren hin.

**2. Öffentliche Institutionen:**

Die Behavioral Insights-Bewegung (Thaler & Sunstein, 2008; OECD, 2017) hat gezeigt, dass evidenzbasierte Policy-Gestaltung zu besseren Outcomes führen kann. Allerdings zeigt die Meta-Analyse von DellaVigna & Linos (2022), dass Effekte kontextabhängig sind. Ein System zur systematischen Kontextanalyse könnte die Übertragbarkeit verbessern.

**3. Unternehmen mit Transformationsbedarf:**

Organisationale Veränderungen scheitern häufig an der mangelnden Berücksichtigung von Mitarbeiterreaktionen. Die Literatur zu "employee voice" (Hirschman, 1970) und organisationaler Gerechtigkeit (Colquitt et al., 2001) dokumentiert die Bedeutung prozeduraler und distributiver Fairness.

**Pilotierte Anwendungen (vorläufige Ergebnisse):**

| Organisation | Anwendung | Vorläufiges Ergebnis | Limitation |
|--------------|-----------|----------------------|------------|
| Verkehrsunternehmen | Kohärenz-Analyse (Strategie vs. Kultur) | Identifikation von Diskrepanzen in 3 von 8 Abteilungen | Keine Kontrollgruppe |
| Bundesamt | Vergleich: Subvention vs. Nudging | Prognose: Nudging 40% effektiver in urbanen Kontexten | Noch nicht feldvalidiert |
| Finanzinstitut | Kampagnentest mit simulierten Profilen | Reduktion der Testvarianten um 70% | Externe Validität unklar |

**Wichtige Einschränkung:** Diese Pilotanwendungen sind explorativer Natur. Systematische Wirksamkeitsnachweise erfordern kontrollierte Studien, die Teil der geplanten Forschungsagenda sind.

---

### Frage b3: What is the size and attractiveness of the potential market?

**Markteinschätzung:**

Eine präzise Marktquantifizierung ist mit erheblicher Unsicherheit behaftet. Die folgenden Schätzungen basieren auf Branchenberichten und sollten als Grössenordnungen verstanden werden:

| Segment | Geschätztes Volumen | Quelle | Konfidenz |
|---------|---------------------|--------|-----------|
| Management Consulting (global) | USD 300-350 Mrd. | IBISWorld, 2024 | Mittel |
| Management Consulting (Schweiz) | CHF 3-4 Mrd. | Schätzung basierend auf BIP-Anteil | Niedrig |
| People Analytics | USD 3-4 Mrd. | Deloitte, 2023 | Mittel |
| Behavioral Policy Consulting | Nicht separat erfasst | – | Sehr niedrig |

**Relevanter Teilmarkt:**

Nicht der gesamte Beratungsmarkt ist adressierbar. BEATRIX ist relevant für Projekte, bei denen Verhaltensänderungen eine zentrale Rolle spielen. Eine konservative Schätzung dieses Segments liegt bei 10-20% des Gesamtmarktes, was für die Schweiz einem Volumen von CHF 300-800 Mio. entspräche.

**Annahmen zur Marktattraktivität:**

Die folgenden Hypothesen zur Marktattraktivität sind plausibel, aber empirisch nicht validiert:

1. *Zahlungsbereitschaft:* Beratungskunden zahlen für Outcomes, nicht für Technologie. Dies legt nahe, dass der Wert von BEATRIX an den erzielten Ergebnissen gemessen wird.

2. *Differenzierung:* Ein evidenzbasierter Ansatz könnte Differenzierung ermöglichen, sofern die Prognosequalität nachweisbar ist.

3. *Skalierbarkeit:* Software-basierte Systeme haben theoretisch niedrige Marginalkosten, wobei die Kalibrierung für neue Kontexte Aufwand erfordert.

**Wettbewerbsposition:**

FehrAdvice verfügt über spezifische Assets:
- Wissenschaftliche Nähe zur verhaltensökonomischen Forschung (Prof. Ernst Fehr)
- Datenbank mit ca. 1'500 codierten experimentellen Studien
- Etablierte Kundenbeziehungen im DACH-Raum

Ob diese Assets in einen nachhaltigen Wettbewerbsvorteil übersetzbar sind, hängt von der erfolgreichen Validierung und Skalierung ab.

---

### Frage b4: What impact can be expected (efficiency gains, cost savings, sustainability improvements)?

**Methodik der Impact-Schätzung:**

Die folgenden Schätzungen basieren auf:
- Vergleich von Pilotprojekten mit historischen Benchmarks
- Extrapolation aus der wissenschaftlichen Literatur
- Experteneinschätzungen

Es handelt sich um Hypothesen, nicht um validierte Kausaleffekte. Die Schätzungen sind mit erheblicher Unsicherheit behaftet.

**Geschätzte Effizienzgewinne für Beratungsprozesse:**

| Dimension | Baseline (geschätzt) | Mit BEATRIX (Hypothese) | Unsicherheit |
|-----------|----------------------|-------------------------|--------------|
| Diagnosezeit | 4-6 Wochen | 1-2 Wochen | ±50% |
| Prognosegenauigkeit | Nicht systematisch erfasst | 65-80% (Pilotdaten) | ±15pp |
| Wissensretention | ~20% (Branchenschätzung) | 70-90% (durch Codifizierung) | ±20pp |

**Erwartete Kundenoutcomes:**

Die Literatur zu evidenzbasiertem Management (Pfeffer & Sutton, 2006; Rousseau, 2006) legt nahe, dass systematische Nutzung wissenschaftlicher Erkenntnisse die Entscheidungsqualität verbessern kann. Quantitative Schätzungen sind jedoch schwierig:

| Outcome | Literatur-Benchmark | BEATRIX-Hypothese | Evidenzqualität |
|---------|---------------------|-------------------|-----------------|
| Change-Projekt-Erfolgsrate | 30-40% (Beer & Nohria, 2000) | 50-70% | Niedrig (keine RCTs) |
| Nudging-Effektstärke | Median 1.4pp (DellaVigna & Linos) | 3-8pp durch bessere Kontextanpassung | Mittel (Pilotdaten) |
| Anreiz-ROI | Stark variabel | Verbesserung durch Crowding-Vermeidung | Niedrig (theoretisch) |

**Volkswirtschaftliche Perspektive:**

Eine präzise volkswirtschaftliche Impact-Schätzung ist nicht seriös möglich. Qualitativ lässt sich argumentieren:

- Bessere organisationale Entscheidungen reduzieren Ressourcenverschwendung
- Evidenzbasierte Policy-Gestaltung kann Steuergelder effizienter einsetzen
- Vermeidung von Motivations-Crowding erhält intrinsische Motivation

Diese Effekte sind theoretisch plausibel, aber nicht quantifizierbar.

**Kritische Einschränkungen:**

1. *Keine Kontrollgruppen:* Die bisherigen Pilotprojekte erlauben keine kausale Attribution.
2. *Selbstselektion:* Kunden, die BEATRIX nutzen, unterscheiden sich möglicherweise systematisch von anderen.
3. *Hawthorne-Effekt:* Verbesserungen könnten teilweise auf erhöhte Aufmerksamkeit zurückgehen, nicht auf das System.

Die im Innovation Cheque geplante Forschung adressiert einige dieser Limitationen durch systematischere Validierung.

---

## c) Feasibility & Risk Reduction

### Frage c1: What aspect of feasibility (technical, scientific, regulatory) needs to be tested?

**Identifikation der offenen Machbarkeitsfragen:**

Die Entwicklung eines evidenzbasierten Entscheidungsunterstützungssystems wie BEATRIX wirft Machbarkeitsfragen auf mehreren Ebenen auf. Diese lassen sich nach dem Technology Readiness Level (TRL) Framework systematisieren:

**1. Technische Machbarkeit (Primärfokus):**

Die zentrale technische Herausforderung betrifft die Stabilität von Verhaltensmodellen unter dynamischen Bedingungen. Die Software-Engineering-Forschung zu "concept drift" und Software-Evolution (Gama et al., 2014; Webb et al., 2016; Lehman, 1980) dokumentiert, dass Modelle an Prognosegenauigkeit verlieren können, wenn sich die zugrundeliegenden Datenverteilungen ändern. Diese Erkenntnisse aus dem Mining Software Repositories (MSR) – einem Forschungsfeld, das Prof. Gall massgeblich mitgeprägt hat (Gall, Jazayeri & Krajewski, 2003) – sind auf Verhaltensmodelle übertragbar.

| Offene Frage | Relevanz | Forschungsansatz |
|--------------|----------|------------------|
| Model Drift | Kontextänderungen (z.B. Reorganisationen) können geschätzte Parameter invalidieren | Diagnostische Algorithmen zur Drift-Erkennung basierend auf Change-Impact-Analysen (Zimmermann et al., 2005) |
| Skalierbarkeit | Pilotprojekte sind nicht automatisch auf industriellen Einsatz übertragbar | Architektur-Assessment nach Prinzipien modularer, lose gekoppelter Systeme (Bass, Clements & Kazman, 2012) |
| Interoperabilität | Integration in bestehende IT-Landschaften erfordert standardisierte Schnittstellen | API-Design und Kompatibilitätstests mit etablierten Software-Engineering-Metriken |

**2. Wissenschaftliche Machbarkeit:**

Die theoretische Fundierung basiert auf etablierter verhaltensökonomischer Forschung (Kahneman & Tversky, 1979; Fehr & Schmidt, 1999; Thaler & Sunstein, 2008). Allerdings ist die Übertragbarkeit experimenteller Befunde auf neue Kontexte (external validity) eine offene Frage (Levitt & List, 2007; Al-Ubaydli & List, 2015).

| Aspekt | Status | Einschränkung |
|--------|--------|---------------|
| Theoretische Basis | Etabliert | Keine eigene Theorieentwicklung, Anwendung existierender Modelle |
| Parametrisierung | In Arbeit | Basiert auf Literatur-Meta-Analysen, nicht auf eigenen Experimenten |
| Prognosevalidierung | Vorläufig | Pilotdaten (n=20+) ohne Kontrollgruppen |

**3. Nutzerakzeptanz:**

Die Literatur zur Algorithm Aversion (Dietvorst et al., 2015) und Algorithm Appreciation (Logg et al., 2019) zeigt, dass die Akzeptanz algorithmischer Empfehlungen von verschiedenen Moderatoren abhängt. Für BEATRIX ist unklar, unter welchen Bedingungen Entscheidungsträger bereit sind, KI-gestützte Verhaltensanalysen in ihre Entscheidungsprozesse zu integrieren.

**Regulatorische Aspekte:**

Derzeit sind keine spezifischen regulatorischen Hürden identifiziert. Das System verarbeitet keine personenbezogenen Daten im Sinne des DSG/DSGVO, da es auf aggregierten Verhaltensparametern aus publizierten Studien basiert. Diese Einschätzung sollte jedoch rechtlich validiert werden.

---

### Frage c2: What is the proof-of-concept or prototype that can realistically be achieved with CHF 15'000?

**Scope-Definition:**

Der Innovation Cheque (CHF 15'000) finanziert eine begrenzte Vorstudie. Es ist wichtig, realistische Erwartungen zu formulieren:

**Was mit CHF 15'000 erreichbar ist:**

| Deliverable | Beschreibung | Methodischer Ansatz |
|-------------|--------------|---------------------|
| **Architektur-Assessment** | Dokumentierte Analyse der bestehenden BEATRIX-Architektur hinsichtlich Skalierbarkeit | Review durch Prof. Gall basierend auf Software-Engineering-Prinzipien |
| **Drift-Diagnose-Konzept** | Konzeptuelle Spezifikation eines Protokolls zur Model-Drift-Erkennung | Literaturbasiert (Gama et al., 2014) + Adaption für Verhaltensmodelle |
| **Akzeptanz-Exploration** | Qualitative Studie (n=10-15) zu Nutzerakzeptanz | Semi-strukturierte Interviews nach etablierten Methoden (Gioia et al., 2013) |
| **Interface-Mockup** | Low-fidelity Prototyp der Mensch-KI-Schnittstelle | Iteratives Design mit Nutzerfeedback |

**Was mit CHF 15'000 NICHT erreichbar ist:**

- Vollständige Produktentwicklung
- Randomisierte kontrollierte Studien zur Wirksamkeit
- Umfassende Feldvalidierung
- Markteinführung

**Einordnung nach Technology Readiness Level:**

| Dimension | Aktuell | Nach Innovation Cheque | Limitation |
|-----------|---------|------------------------|------------|
| Technische Reife | TRL 4 (Laborvalidierung) | TRL 5-6 (Validierung in relevanter Umgebung) | TRL-Sprünge erfordern typischerweise mehr Ressourcen |
| Marktvalidierung | Hypothesen | Erste qualitative Daten | Keine quantitative Validierung |

**Wichtige Klarstellung:**

Die genannten TRL-Ziele sind ambitioniert für das verfügbare Budget. Der Innovation Cheque ermöglicht eine fundierte Einschätzung der Machbarkeit, nicht deren vollständigen Nachweis. Die Ergebnisse dienen primär der Entscheidung über Folgeinvestitionen.

---

### Frage c3: How exactly will the research partner's work reduce these risks?

**Systematische Risikoreduktion:**

Die Zusammenarbeit mit der Universität Zürich adressiert spezifische Risiken durch wissenschaftlich fundierte Methoden:

**Risiko 1: Model Drift (Prof. Harald Gall)**

*Problemstellung:* Verhaltensmodelle sind kontextsensitiv. Wenn sich organisationale oder gesellschaftliche Rahmenbedingungen ändern, können geschätzte Parameter an Gültigkeit verlieren. Die Software-Engineering-Forschung zu concept drift (Gama et al., 2014) und Software-Evolution (Lehman, 1980) hat dieses Problem dokumentiert. Insbesondere die Arbeiten zu Mining Software Repositories (MSR) zeigen, dass evolutionäre Kopplung und Change-Impact-Analysen frühzeitige Warnsignale liefern können (Zimmermann et al., 2005).

*Forschungsansatz:* Prof. Galls Expertise in Software Evolution und MSR (Gall, Jazayeri & Krajewski, 2003; Hassan, 2008) ermöglicht die Adaption etablierter Methoden – insbesondere ChangeDistiller-basierte AST-Differenzierung (Fluri et al., 2007) – für die automatische Erkennung von Verhaltensmodell-Instabilitäten. Der Ansatz verbindet Code-Metriken mit Prognose-Residuenanalyse.

*Erwarteter Output:*
- Klassifikationsschema für Prognosefehler (stochastisches Rauschen vs. gradueller Drift vs. abrupter Strukturbruch), basierend auf etablierten Software-Evolution-Metriken
- Schwellenwerte für automatische Alarmierung, kalibriert an historischen Fehlerverteilungen
- Empfehlungen für manuelle Review-Trigger mit definierten Eskalationspfaden

*Limitation:* Das Konzept wird spezifiziert, aber nicht vollständig implementiert oder empirisch validiert. Die Übertragbarkeit von Software-Metriken auf Verhaltensmodelle ist eine offene Forschungsfrage.

**Risiko 2: Architektur-Skalierbarkeit (Prof. Harald Gall)**

*Problemstellung:* Pilotprojekte mit wenigen Nutzern sind nicht automatisch auf industriellen Einsatz übertragbar. Die Software-Engineering-Literatur dokumentiert, dass Skalierungsprobleme sich häufig erst unter Last manifestieren und dass frühe Architekturentscheidungen langfristige Konsequenzen haben (Bass, Clements & Kazman, 2012).

*Forschungsansatz:* Systematisches Architektur-Review basierend auf etablierten Prinzipien der Software-Architektur: modulare Dekomposition, Fehlertoleranz durch Redundanz, lose Kopplung für unabhängige Skalierung einzelner Komponenten. Der Assessment-Ansatz nutzt Metriken aus der Software-Qualitätsforschung (Chidamber & Kemerer, 1994; Hassan, 2008).

*Erwarteter Output:*
- Dokumentierte Stärken und Schwächen der aktuellen Architektur nach etablierten Qualitätsattributen (Performanz, Wartbarkeit, Erweiterbarkeit)
- Priorisierte Empfehlungen für Refactoring basierend auf technischer Schuld-Analyse
- Blueprint für skalierbare, modular entkoppelte Komponenten

*Limitation:* Assessment, keine Implementierung. Die Umsetzung erfordert dedizierte Entwicklungsressourcen ausserhalb des Innovation Cheque.

**Risiko 3: Nutzerakzeptanz (Prof. Johannes Luger)**

*Problemstellung:* Die Literatur dokumentiert, dass Menschen algorithmische Empfehlungen unter bestimmten Bedingungen ablehnen, selbst wenn diese nachweislich überlegen sind (Dietvorst et al., 2015). Aus strategischer Managementperspektive ist dies ein Problem der Aufmerksamkeitsallokation und Informationsverarbeitung: Manager müssen algorithmische Outputs in ihre bestehenden Entscheidungsheuristiken integrieren (Ocasio, 1997). Die Forschung zeigt, dass organisationale Strukturen diese Integration moderieren (Luger, Junge & Mammen, 2023).

*Forschungsansatz:* Qualitative Studie basierend auf etablierten Methoden der Organisationsforschung (semi-strukturierte Interviews, thematische Analyse nach Gioia, Corley & Hamilton, 2013). Der Fokus liegt auf der Rekonstruktion von Sensemaking-Prozessen bei der Integration algorithmischer Verhaltensanalysen in strategische Entscheidungen. Dies knüpft an Lugers Forschung zur Rolle metaphorischer Kommunikation in Managementkontexten an (König et al., 2018).

*Erwarteter Output:*
- Identifikation von Akzeptanzdeterminanten entlang der Dimensionen: kognitive Kapazität, organisationale Rolle, Entscheidungsdomäne, vorherige Erfahrung mit algorithmischen Tools
- Gestaltungsempfehlungen für die Mensch-KI-Schnittstelle unter Berücksichtigung von Aufmerksamkeitsstrukturen und Informationsverarbeitungslimitationen
- Hypothesen für quantitative Folgestudien, formuliert als testbare Moderationseffekte

*Limitation:* Qualitative Exploration erlaubt keine kausalen Schlussfolgerungen; Ergebnisse dienen der Hypothesengenerierung, nicht dem Hypothesentest.

**Zusammenfassende Einschätzung:**

Die Forschungspartnerschaft reduziert Risiken durch systematische Analyse, nicht durch deren vollständige Eliminierung. Die Ergebnisse ermöglichen eine fundierte Go/No-Go-Entscheidung für Folgeinvestitionen.

---

### Frage c4: What would be the next steps if feasibility is proven?

**Bedingte Folgeschritte:**

Die nächsten Schritte hängen von den Ergebnissen des Innovation Cheque ab. Es werden drei Szenarien unterschieden:

**Szenario A: Positive Machbarkeitssignale**

Wenn die Vorstudie positive Ergebnisse liefert (Architektur skalierbar, Drift managebar, Akzeptanz vorhanden), wäre der logische nächste Schritt ein umfassenderes Innosuisse-Innovationsprojekt:

| Phase | Fokus | Geschätzter Aufwand | Unsicherheit |
|-------|-------|---------------------|--------------|
| Hauptprojekt (2026-2028) | Vollentwicklung und Feldvalidierung | CHF 500k-2M | Hoch (abhängig von Vorstudie) |
| Pilotierung (2028) | Kontrollierte Anwendung mit Lead Customers | CHF 200-500k | Mittel |
| Skalierung (2029+) | Kommerzielle Verbreitung | Marktabhängig | Sehr hoch |

**Szenario B: Gemischte Ergebnisse**

Wenn einzelne Aspekte positiv, andere negativ bewertet werden, wäre ein fokussiertes Nachfolgeprojekt sinnvoll, das spezifische Schwachstellen adressiert.

**Szenario C: Negative Machbarkeitssignale**

Wenn die Vorstudie fundamentale Probleme identifiziert (z.B. Architektur nicht skalierbar, Akzeptanz gering), wäre eine Neuausrichtung oder Einstellung des Projekts die rationale Konsequenz. Auch dieses Ergebnis wäre wissenschaftlich wertvoll.

**Forschungsagenda (unabhängig vom Szenario):**

Die Ergebnisse der Vorstudie können unabhängig vom kommerziellen Ausgang wissenschaftlich publiziert werden:

- Technische Erkenntnisse zu Model Drift in Verhaltensmodellen
- Empirische Befunde zur Akzeptanz von KI-gestützter Verhaltensanalyse
- Methodische Beiträge zur Architektur-Bewertung

**Kritische Einschränkung:**

Die genannte Roadmap ist hypothetisch und setzt positive Machbarkeitsergebnisse voraus. Zeitrahmen und Budgets sind Schätzungen mit hoher Unsicherheit. Die tatsächliche Entwicklung hängt von Faktoren ab, die zum jetzigen Zeitpunkt nicht vollständig antizipierbar sind (technische Herausforderungen, Marktentwicklung, Finanzierungsverfügbarkeit).

---

## d) Collaboration with a Research Partner

### Frage d1: What scientific expertise is required that we don't have in-house?

**Analyse der internen Kompetenzen:**

FehrAdvice verfügt über spezifische Stärken in der Anwendung verhaltensökonomischer Erkenntnisse:

| Bereich | Beschreibung | Einschränkung |
|---------|--------------|---------------|
| Verhaltensökonomie | Beratung durch Prof. Ernst Fehr; Anwendungserfahrung | Keine eigene Grundlagenforschung |
| Beratungsmethodik | Praktische Erfahrung aus ca. 20 Jahren | Nicht akademisch validiert |
| Literaturdatenbank | Ca. 1'500 codierte Studien | Sekundäranalyse, keine Primärforschung |
| Pilotprojekte | Ca. 20 durchgeführte Anwendungen | Ohne Kontrollgruppen |

**Identifizierte Kompetenzlücken:**

Die Literatur zu erfolgreichen Forschungskooperationen (Perkmann et al., 2013; Bruneel, D'Este & Salter, 2010) betont die Bedeutung komplementärer Kompetenzen. Für BEATRIX wurden folgende Lücken identifiziert:

| Kompetenz | Begründung des Bedarfs | Relevante Literatur | Adressiert durch |
|-----------|------------------------|---------------------|------------------|
| **Software Evolution & MSR** | Verhaltensmodelle erfordern kontinuierliche Anpassung; Mining Software Repositories bietet Methoden zur Drift-Erkennung | Gama et al. (2014); Lehman (1980); Gall, Jazayeri & Krajewski (2003) | Prof. Gall |
| **Architektur-Design** | Skalierbare Systeme erfordern spezifisches Know-how in modularer Architektur und Qualitätsmetriken | Bass, Clements & Kazman (2012); Chidamber & Kemerer (1994) | Prof. Gall |
| **Strategic Decision Making** | Integration algorithmischer Outputs in organisationale Entscheidungsprozesse | Ocasio (1997); Luger, Junge & Mammen (2023) | Prof. Luger |
| **Human-AI Interaction** | Die Akzeptanz algorithmischer Empfehlungen ist ein nicht-triviales Problem der Aufmerksamkeitsallokation | Dietvorst et al. (2015); Logg et al. (2019) | Prof. Luger |
| **Qualitative Organisationsforschung** | Wissenschaftliche Exploration erfordert methodische Rigorosität | Gioia, Corley & Hamilton (2013) | Prof. Luger |

Diese Kompetenzen sind in einem Beratungsunternehmen typischerweise nicht vorhanden und erfordern akademische Expertise. Die Kombination von Software-Engineering (Gall) und strategischem Management (Luger) adressiert sowohl technische als auch organisationale Machbarkeitsfragen.

---

### Frage d2: Why is the chosen research partner the most suitable for this project?

**Begründung der Partnerwahl:**

Die Auswahl der Universität Zürich basiert auf einer systematischen Bewertung der Passgenauigkeit zwischen Projektanforderungen und verfügbarer Expertise:

**Prof. Harald Gall (Institut für Informatik, Dekan der Wirtschaftswissenschaftlichen Fakultät):**

Prof. Gall ist international anerkannter Experte für Software Evolution und Mining Software Repositories (MSR). Seine Forschung hat das Feld der automatisierten Software-Analyse massgeblich geprägt (>20'000 Zitationen). Der Forschungsschwerpunkt ist direkt relevant für die technischen Herausforderungen von BEATRIX:

| Relevantes Forschungsgebiet | Bezug zu BEATRIX | Ausgewählte Publikationen |
|----------------------------|------------------|---------------------------|
| Mining Software Repositories | Adaption von MSR-Techniken für Verhaltensmodell-Drift-Erkennung | Gall, Jazayeri & Krajewski (2003); Hassan (2008) |
| Software Evolution | Model Drift entspricht konzeptuell dem Phänomen der Software-Alterung (Lehman's Laws) | Lehman (1980); Gall et al. (2009) |
| Change-Impact-Analyse | ChangeDistiller-Methodik zur feingranularen Änderungserkennung auf AST-Ebene | Fluri et al. (2007); Zimmermann et al. (2005) |
| Software-Qualitätsmetriken | Systematische Architektur-Bewertung nach etablierten Qualitätsattributen | Chidamber & Kemerer (1994); Hassan (2008) |

**Prof. Johannes Luger (Institut für Betriebswirtschaft, Evidence-Based Strategic Management):**

Prof. Luger forscht an der Schnittstelle von strategischem Management, Entscheidungsfindung und Organisationstheorie. Seine Arbeiten zur selektiven Informationsverarbeitung in Organisationen sind direkt relevant für die Akzeptanzfrage:

| Relevantes Forschungsgebiet | Bezug zu BEATRIX | Ausgewählte Publikationen |
|----------------------------|------------------|---------------------------|
| Selective Information Processing | Wie Manager algorithmische Outputs in Entscheidungen integrieren | Luger, Junge & Mammen (2023) |
| Attention-Based View | Aufmerksamkeitsallokation bei konkurrierenden Informationsquellen | Ocasio (1997); König et al. (2018) |
| Strategic Decision Making | Nutzung von Entscheidungsunterstützungssystemen in C-Level-Kontexten | Luger & Raisch (2021) |
| Qualitative Organisationsforschung | Rigorose Exploration nach Gioia-Methodologie | Gioia, Corley & Hamilton (2013) |

**Alternative Optionen:**

Die ETH Zürich und EPFL verfügen über exzellente Informatik-Fakultäten. Die UZH wurde aus folgenden Gründen bevorzugt:

| Kriterium | UZH | ETH/EPFL |
|-----------|-----|----------|
| Kombination Informatik + BWL | ✓ Beide Fakultäten | Primär technisch |
| Verhaltensökonomie-Tradition | ✓ Fehr-Schule | Weniger ausgeprägt |
| Passgenauigkeit zu SSBM-Einreichung | ✓ Hoch | Niedriger |

**Einschränkung:** Diese Bewertung basiert auf öffentlich verfügbaren Informationen über Forschungsprofile. Die tatsächliche Passgenauigkeit wird sich in der Zusammenarbeit erweisen.

---

### Frage d3: What is the specific contribution of the research partner (methods, tools, facilities, know-how)?

**Spezifische Beiträge der Forschungspartner:**

Die Literatur zu University-Industry Collaboration (Cohen, Nelson & Walsh, 2002; Perkmann & Walsh, 2007) identifiziert verschiedene Transfermechanismen. Für dieses Projekt sind folgende relevant:

**Arbeitspaket 1: Architektur-Assessment & Drift-Diagnostik (Prof. Harald Gall)**

| Beitrag | Beschreibung | Erwarteter Output | Limitation |
|---------|--------------|-------------------|------------|
| MSR-Methodentransfer | Adaption von Mining Software Repositories-Techniken (Change-Impact-Analyse, evolutionäre Kopplung) für Verhaltensmodelle | Konzeptuelle Spezifikation eines Drift-Diagnose-Protokolls | Übertragbarkeit auf Verhaltensmodelle ist Forschungsfrage |
| Architektur-Review | Systematische Bewertung nach Software-Qualitätsattributen (Performanz, Wartbarkeit, Skalierbarkeit) | Dokumentierte Stärken-Schwächen-Analyse mit priorisierten Refactoring-Empfehlungen | Assessment, keine Implementierung |
| ChangeDistiller-Adaption | Konzeptuelle Übertragung der AST-basierten Änderungserkennung auf Modellparameter | Blueprint für automatisierte Modellüberwachung | Keine vollständige Implementierung |

Geschätzter Aufwand: ca. CHF 8'000 (entspricht ca. 40-50 Forschungsstunden)

**Arbeitspaket 2: Akzeptanz-Exploration (Prof. Johannes Luger)**

| Beitrag | Beschreibung | Erwarteter Output | Limitation |
|---------|--------------|-------------------|------------|
| Qualitative Methodenkompetenz | Semi-strukturierte Interviews und Gioia-Methodologie (Gioia, Corley & Hamilton, 2013) | Theoriegeleiteter Interviewleitfaden und Analyseschema | Keine quantitative Validierung |
| Attention-Based Framing | Analyse der Aufmerksamkeitsallokation bei algorithmischen vs. intuitiven Inputs (Ocasio, 1997) | Konzeptuelles Modell der Informationsintegration in Managemententscheidungen | Explorative Hypothesen, nicht kausal testbar |
| Netzwerkzugang | Zugang zu C-Level-Entscheidungsträgern über akademische und Praxisnetzwerke | 10-15 qualitative Interviews mit Senior Managern | Selbstselektion der Teilnehmer möglich |
| Sensemaking-Analyse | Rekonstruktion von Interpretationsprozessen bei algorithmischen Empfehlungen | Vorläufiges Akzeptanzmodell mit identifizierten Moderatoren | Hypothesengenerierend, nicht -testend |

Geschätzter Aufwand: ca. CHF 7'000 (entspricht ca. 35-45 Forschungsstunden)

**Wichtige Klarstellung zum Budget:**

CHF 15'000 ermöglicht eine begrenzte Vorstudie. Die genannten Beiträge sind realistisch für dieses Budget, aber keine umfassende Forschung. Die Outputs sind:
- Konzeptuelle Grundlagen, keine fertigen Lösungen
- Erste explorative Daten, keine validierten Ergebnisse
- Empfehlungen, keine Implementierungen

---

### Frage d4: How will this collaboration strengthen the company's innovation capacity?

**Hypothesen zur Kapazitätsstärkung:**

Die Literatur zu Absorptive Capacity (Cohen & Levinthal, 1990; Zahra & George, 2002) legt nahe, dass Unternehmen von Forschungskooperationen profitieren können, wenn sie über die Fähigkeit verfügen, externes Wissen zu integrieren.

Für FehrAdvice werden folgende Effekte hypothetisiert:

| Dimension | Erwarteter Effekt | Unsicherheit | Evidenzbasis |
|-----------|-------------------|--------------|--------------|
| Technisches Know-how | Transfer von Software-Engineering-Methoden | Mittel | Hängt von Integrationsfähigkeit ab |
| Methodisches Repertoire | Erweiterung um qualitative Forschungsmethoden | Mittel | Erfordert interne Anpassung |
| Wissenschaftliche Legitimität | Potenzielle Co-Publikationen | Hoch | Abhängig von Ergebnisqualität |
| Netzwerkeffekte | Zugang zu akademischer Community | Mittel | Langfristige Entwicklung |

**Potenzielle Transfermechanismen:**

1. *Wissenstransfer:* UZH-Methoden werden dokumentiert und können in FehrAdvice-Praxis übernommen werden – sofern interne Kapazität zur Integration vorhanden ist

2. *Talentpipeline:* Kontakt zu UZH-Absolventen könnte Rekrutierung erleichtern – allerdings ist dies für ein Beratungsunternehmen nicht der primäre Kanal

3. *Publikationen:* Co-Autorenschaft wäre möglich, setzt aber publikationswürdige Ergebnisse voraus

4. *Folgeprojekte:* Erfolgreiche Zusammenarbeit könnte Basis für weitere Projekte sein

**Kritische Einschränkung:**

Diese Effekte sind nicht garantiert. Die Literatur zeigt, dass University-Industry Collaborations häufig an Transferbarrieren scheitern (Bruneel et al., 2010). Der Erfolg hängt von der Qualität der Zusammenarbeit, der Ergebnisse und der internen Integrationsfähigkeit ab.

---

### Frage d5: Could this collaboration lead to a longer-term partnership or a follow-up Innosuisse project?

**Bedingte Aussagen zu Folgeprojekten:**

Die Frage nach langfristiger Partnerschaft lässt sich zum jetzigen Zeitpunkt nicht definitiv beantworten. Folgende Szenarien sind denkbar:

**Szenario A: Positive Ergebnisse**

Wenn die Vorstudie positive Signale liefert, wäre ein Folgeprojekt plausibel:

| Mögliches Projekt | Voraussetzung | Geschätzter Aufwand | Unsicherheit |
|-------------------|---------------|---------------------|--------------|
| Hauptprojekt | Architektur als skalierbar bewertet | CHF 500k-2M | Hoch |
| Feldvalidierung | Akzeptanz in Vorstudie positiv | CHF 200-500k | Hoch |
| Erweiterung auf Policy | Interesse öffentlicher Institutionen | Unklar | Sehr hoch |

**Szenario B: Gemischte Ergebnisse**

Bei gemischten Ergebnissen wäre eine fokussierte Fortsetzung denkbar, die spezifische Schwachstellen adressiert.

**Szenario C: Negative Ergebnisse**

Bei negativen Ergebnissen (Architektur nicht skalierbar, Akzeptanz gering) wäre eine Fortsetzung nicht sinnvoll. Auch dieses Ergebnis wäre wissenschaftlich wertvoll und könnte publiziert werden.

**Faktoren für langfristige Partnerschaft:**

Die Literatur identifiziert folgende Erfolgsfaktoren für nachhaltige University-Industry Partnerships (Perkmann et al., 2013):

| Faktor | Status im Projekt | Einschätzung |
|--------|-------------------|--------------|
| Komplementäre Kompetenzen | Vorhanden | Positiv |
| Klare Zieldefinition | Definiert | Positiv |
| Realistische Erwartungen | In Entwicklung | Neutral |
| Persönliche Beziehungen | Zu entwickeln | Offen |
| Institutionelle Unterstützung | Vorhanden (Innosuisse) | Positiv |

**Ehrliche Einschätzung:**

Eine langfristige Partnerschaft ist möglich, aber nicht garantiert. Sie hängt von:
- Der Qualität der Ergebnisse der Vorstudie
- Der Entwicklung persönlicher Arbeitsbeziehungen
- Der Verfügbarkeit von Folgefinanzierung
- Dem strategischen Interesse beider Partner

Es wäre unseriös, zum jetzigen Zeitpunkt eine langfristige Partnerschaft zu versprechen. Der Innovation Cheque dient auch der Exploration, ob eine solche Partnerschaft sinnvoll und realistisch ist.

---

## e) Impact for Switzerland

### Frage e1: How does the project strengthen Swiss industry competitiveness (know-how, jobs, IP in Switzerland)?

**Evidenzbasierte Einschätzung zur Wettbewerbsfähigkeit:**

Die Frage nach nationalem Wettbewerbsvorteil erfordert zunächst eine kritische Einordnung: Die Innovationsforschung zeigt, dass nationale Kompetenzcluster historisch gewachsen sind und nicht deterministisch geplant werden können (Porter, 1990; Feldman & Kogler, 2010). Dennoch lassen sich plausible Mechanismen identifizieren, durch die das Projekt zur Schweizer Wettbewerbsfähigkeit beitragen könnte.

**1. Know-how-Aufbau – Evidenz und Limitationen:**

| Dimension | Hypothese | Evidenzbasis | Limitation |
|-----------|-----------|--------------|------------|
| Methodische Kompetenz | Kombination von Verhaltensökonomie + AI könnte Nische schaffen | Schweiz hat starke verhaltensökonomische Tradition (Fehr & Gächter, 2000; Fehr & Schmidt, 1999) | Andere Standorte (UK, USA) entwickeln parallele Ansätze |
| Humankapital | Ausbildungseffekte durch University-Industry-Spillovers | Perkmann et al. (2013): Evidenz für Humankapital-Transfer | Effektgrössen variieren stark nach Branche |
| Absorptive Capacity | Stärkung der Fähigkeit, externes Wissen zu nutzen | Cohen & Levinthal (1990): Absorptive Capacity als Wettbewerbsfaktor | Messung schwierig, kausale Attribution problematisch |

**2. Beschäftigung – Ehrliche Einschätzung:**

Prognosen zu Beschäftigungseffekten sind mit erheblicher Unsicherheit behaftet. Die Literatur zu Spin-offs und neuen Technologiefeldern zeigt hohe Varianz (Shane, 2004):

| Szenario | Annahme | Geschätzte Stellen (Schweiz, 5 Jahre) | Konfidenz |
|----------|---------|---------------------------------------|-----------|
| Optimistisch | Hohe Marktakzeptanz, starke Skalierung | 30-50 | Niedrig |
| Realistisch | Moderate Adoption, Nischenmarkt | 10-20 | Mittel |
| Konservativ | Langsame Diffusion, Wettbewerbsdruck | 3-8 | Mittel |

**Wichtige Limitation:** Diese Schätzungen basieren auf Analogien zu anderen Technologie-Beratungsfeldern und sind spekulativ.

**3. Intellectual Property – Differenzierte Betrachtung:**

| IP-Element | Status | Schützbarkeit | Limitation |
|------------|--------|---------------|------------|
| BCM-Framework | FehrAdvice-Eigentum | Know-how-Schutz möglich | Konzepte schwer patentierbar |
| BEATRIX-Architektur | In Entwicklung | Unklar | Software-Patente in CH begrenzt |
| Datenbank verhaltensökonomischer Experimente | Vorhanden | Trade Secret | Replikation durch andere möglich |

**Kritische Einordnung zum internationalen Vergleich:**

Ein "Schweizer Vorteil" lässt sich zum jetzigen Zeitpunkt nicht belegen. Was gesagt werden kann:
- Die Schweiz verfügt über starke Forschung in Verhaltensökonomie
- Die Kombination mit AI-Anwendung ist international noch im Frühstadium
- First-Mover-Advantages in Wissensfeldern sind empirisch umstritten (Lieberman & Montgomery, 1988)

**Fazit e1:** Das Projekt könnte zur Schweizer Wettbewerbsfähigkeit beitragen, aber kausale Effekte sind schwer isolierbar. Eine Vorstudie kann hier nur Potentiale erkunden, nicht beweisen.

---

### Frage e2: How does it support SME-university collaboration and knowledge transfer?

**Forschungsstand zu University-Industry Collaboration:**

Die Literatur zu University-Industry Linkages (UIL) identifiziert mehrere Mechanismen des Wissenstransfers, deren Wirksamkeit jedoch kontextabhängig ist (Perkmann & Walsh, 2007; D'Este & Patel, 2007):

| Transfer-Kanal | Evidenz | Typische Effektgrösse | Konditionen für Erfolg |
|----------------|---------|----------------------|------------------------|
| Gemeinsame Forschung | Moderat positiv | Variabel, oft klein | Komplementäre Expertise, klare IP-Regelung |
| Informelle Kontakte | Oft unterschätzt | Schwer messbar | Geographische Nähe, persönliche Beziehungen |
| Mobilität von Personal | Stark positiv | r = 0.2-0.4 | Anreizkompatible Karrierepfade |
| Beratung | Moderat | Fallabhängig | Klare Problemdefinition |

**Geplante Wissenstransfer-Mechanismen im Projekt:**

| Richtung | Mechanismus | Erwarteter Nutzen | Limitation |
|----------|-------------|-------------------|------------|
| Gall → FehrAdvice | MSR-Methoden (Change-Impact-Analyse, Software-Qualitätsmetriken) für Verhaltensmodell-Monitoring | Wissenschaftlich fundierte Architekturentscheidungen; systematische Drift-Erkennung | Transfer taciten Wissens schwierig; Adaption auf neue Domäne erforderlich |
| Luger → FehrAdvice | Methodisches Know-how zu qualitativer Organisationsforschung (Gioia-Methodik) | Rigorose Exploration von Nutzerakzeptanz; evidenzbasierte Interface-Gestaltung | Quantitative Validierung bleibt Folgeprojekt |
| FehrAdvice → Gall | Reale Verhaltensmodelle als Testfall für Software-Evolution-Konzepte | Empirische Relevanz für MSR-Forschung in neuer Anwendungsdomäne | Proprietäre Modelldetails möglicherweise eingeschränkt teilbar |
| FehrAdvice → Luger | Zugang zu Praxiskontexten für Akzeptanzforschung | Empirisch fundierte Forschung zu Human-AI-Interaction in strategischen Entscheidungen | Selbstselektion der Interviewpartner

**Erfolgsfaktoren nach der Literatur:**

Perkmann et al. (2013) identifizieren in ihrer Meta-Analyse folgende Erfolgsfaktoren für UIL:

| Faktor | Bedeutung | Status im Projekt | Ehrliche Einschätzung |
|--------|-----------|-------------------|----------------------|
| Vorherige Zusammenarbeit | Sehr hoch | Begrenzt (informelle Kontakte zu UZH) | Noch zu entwickeln |
| Komplementäre Ressourcen | Hoch | Vorhanden (Theorie vs. Praxis) | Positiv |
| Klare Governance | Hoch | Wird mit Vorstudie etabliert | Offen |
| Organisationale Unterstützung | Mittel | Innosuisse als Katalysator | Positiv |

**Kritische Einordnung:**

Die Literatur warnt vor überzogenen Erwartungen an UIL (Bozeman et al., 2013):
- Nicht alle Kooperationen führen zu messbarem Transfer
- KMU haben oft begrenzte Absorptive Capacity für akademisches Wissen
- Erfolgsmessung ist methodisch schwierig

**Fazit e2:** Das Projekt entspricht strukturell einem typischen UIL-Format. Ob es zu effektivem Wissenstransfer führt, kann erst ex post beurteilt werden.

---

### Frage e3: What are the potential societal or economic benefits for Switzerland if successful?

**Methodische Vorbemerkung zur Nutzenschätzung:**

Die Quantifizierung gesellschaftlicher und volkswirtschaftlicher Effekte von Forschungsprojekten ist methodisch problematisch (Salter & Martin, 2001). Die folgenden Überlegungen sind daher als spekulative Szenarien zu verstehen, nicht als Prognosen.

**Potentielle Anwendungsfelder – Evidenzbasierte Einschätzung:**

| Bereich | Theoretischer Mechanismus | Evidenzbasis | Effektgrössen-Schätzung | Konfidenz |
|---------|---------------------------|--------------|------------------------|-----------|
| Organisationale Entscheidungen | Debiasing durch strukturierte Prozesse | Kahneman et al. (2011): Noise-Reduktion möglich | 10-30% Varianzreduktion (unter Laborbedingungen) | Mittel |
| Change Management | Verhaltensbasierte Barrierenanalyse | Beer & Nohria (2000): 70% Scheitern bestätigt; Interventionseffekte unklar | Spekulativ | Niedrig |
| Public Policy | Nudging als Ergänzung zu Anreizen | Sunstein (2014); DellaVigna & Linos (2022): Effekte oft kleiner als im Labor | d = 0.05-0.15 in Feldstudien | Mittel |
| Prävention (Gesundheit) | Verhaltensvorhersage für Targeting | Volpp et al. (2011): Positive Ergebnisse bei finanziellen Anreizen | Heterogen, kontextabhängig | Mittel |

**Wichtige Limitationen bei gesellschaftlichen Nutzenbehauptungen:**

1. **Attribution:** Selbst bei positiven Outcomes ist der kausale Beitrag eines einzelnen Projekts schwer isolierbar

2. **Skalierung:** Laboreffekte übertragen sich oft nicht 1:1 in die Praxis (DellaVigna & Linos, 2022 zeigen: Feldeffekte typischerweise 60-90% kleiner als RCT-Effekte)

3. **Kontextabhängigkeit:** Verhaltensinterventionen wirken heterogen – was in einem Kontext funktioniert, kann in einem anderen scheitern (Allcott, 2015)

4. **Unintendierte Effekte:** Behavioral Interventions können negative Nebeneffekte haben (Gneezy & Rustichini, 2000: Crowding-out intrinsischer Motivation)

**Illustratives Beispiel: Energieeffizienz (mit Einschränkungen)**

Die Literatur zu Behavioral Interventions bei Energieverbrauch zeigt:

| Studie | Intervention | Effekt | Limitation |
|--------|--------------|--------|------------|
| Allcott (2011) | Social Comparison (Opower) | 2% Reduktion | Decay über Zeit |
| Schultz et al. (2007) | Normative Messaging | 5-10% (kurzfristig) | Heterogene Effekte |
| Delmas et al. (2013) | Meta-Analyse | Mean d = 0.07 | Publication Bias möglich |

**Schlussfolgerung:** Verhaltensbasierte Energieinterventionen zeigen moderate, aber nicht transformative Effekte. Eine Reduktion von Subventionsbedarf um Faktor 10 (wie manchmal behauptet) ist durch die Literatur nicht gedeckt.

**Realistische Einschätzung des Projektbeitrags:**

| Zeithorizont | Wahrscheinlicher Beitrag | Unsicherheit |
|--------------|--------------------------|--------------|
| Kurzfristig (Vorstudie) | Methodenentwicklung, Pilotvalidierung | Gering |
| Mittelfristig (3-5 Jahre) | Anwendung in begrenztem Kontext (Beratungsprojekte) | Mittel |
| Langfristig (10+ Jahre) | Potentieller Beitrag zu breiterem Methodenrepertoire | Sehr hoch |

**Fazit e3:** Gesellschaftlicher Nutzen ist plausibel, aber nicht quantifizierbar. Überzogene Nutzenbehauptungen würden den Standards wissenschaftlicher Redlichkeit widersprechen.

---

### Frage e4: Could the project help position Switzerland as a leader in this innovation area?

**Kritische Analyse zur "Führerschaft":**

Die Frage nach nationaler Führerschaft in einem Innovationsfeld erfordert eine nüchterne Betrachtung. Die Cluster-Theorie (Porter, 1990) und die Innovationsökonomie (Feldman, 2000) zeigen, dass Führerschaft:
- Historisch gewachsen ist (nicht planbar)
- Von kritischer Masse abhängt
- Pfadabhängig und schwer zu replizieren ist

**Bestandsaufnahme der Schweizer Position:**

| Dimension | Objektiver Status | Evidenz | Internationale Einordnung |
|-----------|-------------------|---------|---------------------------|
| Verhaltensökonomische Forschung | Stark | Fehr & Schmidt (1999) >10,000 Zitationen; UZH in Top-Rankings | Top 5 weltweit |
| AI/ML Forschung | Stark | ETH, EPFL international kompetitiv | Top 10 weltweit |
| Kombination Behavioral + AI | Emergent | Wenige Akteure bisher | Unklar, Feld im Entstehen |
| Industrielle Anwendung | Begrenzt | FehrAdvice als Einzelakteur | Keine kritische Masse |

**Internationale Landschaft – Differenzierte Betrachtung:**

| Standort | Stärken | Relative Position | Schweizer Differenzierung |
|----------|---------|-------------------|---------------------------|
| UK | Behavioral Insights Team, akademische Tradition | Stark in Policy | Schweiz stärker in Grundlagenforschung |
| USA | Tech-Giganten, Ressourcen, Talentpool | Dominant in AI | Schweiz fokussierter auf Verhaltensökonomie |
| Deutschland | Industrieforschung, Fraunhofer | Stark in angewandter Forschung | Schweiz agiler, aber kleiner |
| Singapur | Government-Support, Behavioral Economics | Aufstrebend | Ähnliche Nischenstrategie |

**Realistische Einschätzung:**

Die Schweiz hat Voraussetzungen für eine **Nischenposition** (nicht "globale Führerschaft"):

| Szenario | Wahrscheinlichkeit | Konditionen |
|----------|-------------------|-------------|
| Nischenführer im deutschsprachigen Raum | Mittel-Hoch | Erfolgreiche Skalierung, Folgeprojekte |
| Beitrag zu internationalem Forschungsnetzwerk | Hoch | Akademische Kooperationen, Publikationen |
| Globaler Marktführer | Niedrig | Würde massive Investitionen und kritische Masse erfordern |

**Limitationen der Führerschafts-Hypothese:**

1. **Ein Projekt macht keine Führerschaft:** Der Innovation Cheque finanziert eine Vorstudie – der Abstand zu echter Marktführerschaft ist erheblich

2. **Internationale Konkurrenz:** Andere Standorte (insb. USA, UK) haben mehr Ressourcen und Talentpools

3. **Kommerzialisierungsrisiko:** Akademische Exzellenz überträgt sich nicht automatisch in Marktführerschaft

4. **Messbarkeit:** "Führerschaft" ist ein unscharfer Begriff – nach welcher Metrik?

**Was das Projekt realistisch beitragen kann:**

- Exploration der Machbarkeit eines spezifischen Ansatzes
- Aufbau einer Arbeitsbeziehung zwischen Industrie und Akademie
- Publikationen, die zur Schweizer Sichtbarkeit im Feld beitragen
- Grundlage für grössere Folgeprojekte (falls positiv)

**Fazit e4:** Das Projekt kann einen bescheidenen Beitrag zur Schweizer Positionierung leisten. Die Behauptung einer "globalen Führerschaft" wäre zum jetzigen Zeitpunkt jedoch unbegründet und würde den Standards wissenschaftlicher Bescheidenheit widersprechen.

---

## Zusammenfassung

Dieses Dokument beantwortet alle 20 Fragen des Innosuisse-Fragebogens (Dr. Daniel Fasnacht) für das Projekt BEATRIX:

| Rubrik | Fragen | Status |
|--------|--------|--------|
| a) Innovation Potential | 3 Fragen | ✓ Vollständig beantwortet |
| b) Market Relevance | 4 Fragen | ✓ Vollständig beantwortet |
| c) Feasibility & Risk Reduction | 4 Fragen | ✓ Vollständig beantwortet |
| d) Collaboration with Research Partner | 5 Fragen | ✓ Vollständig beantwortet |
| e) Impact for Switzerland | 4 Fragen | ✓ Vollständig beantwortet |

**Nächster Schritt:** Übertragung in das Innolink-Portal.

---

*Dokument erstellt: 2026-01-18 | Version 2.0 | Für Innosuisse Innovation Cheque Antrag BEATRIX*

**Änderungshistorie:**
- v1.0 (2026-01-18): Initiale Version im Ernst-Fehr-Stil
- v2.0 (2026-01-18): Ergänzung um domänenspezifische Terminologie für Prof. Harald Gall (Software Engineering/MSR) und Prof. Johannes Luger (Strategic Management/Attention-Based View)
