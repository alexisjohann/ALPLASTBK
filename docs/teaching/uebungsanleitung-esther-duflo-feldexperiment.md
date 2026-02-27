# Übungsanleitung: «Was würde Esther Duflo über dein Feld-Experiment sagen?»

**Kurs:** Feldexperimente in der Praxis
**Dozent:** Nils Handler
**Version:** 1.0 | Februar 2026

---

## 1. Einleitung und Lernziele

In dieser Übung nehmt ihr die Perspektive von **Esther Duflo** ein — Nobelpreisträgerin 2019, Professorin am MIT und Mitgründerin des Abdul Latif Jameel Poverty Action Lab (J-PAL). Duflo ist bekannt für ihren rigorosen, praxisorientierten Ansatz zu **randomisierten kontrollierten Studien (RCTs)** und evidenzbasierter Politikgestaltung.

### Was ihr in dieser Übung lernt

| Lernziel | Beschreibung |
|----------|--------------|
| **L1: Kausalität** | Zwischen Korrelation und Kausalität unterscheiden — und verstehen, warum das für Politik relevant ist |
| **L2: Experimentelles Design** | Die Kernelemente eines RCT identifizieren und kritisch bewerten |
| **L3: Messbarkeit** | Abstrakte Konzepte in messbare Outcomes übersetzen |
| **L4: Externe Validität** | Beurteilen, ob und wie Ergebnisse skalierbar und übertragbar sind |
| **L5: Ethik** | Ethische Spannungsfelder in Feldexperimenten erkennen und reflektieren |

### Wer ist Esther Duflo?

Esther Duflo (*1972, Paris) hat mit Abhijit Banerjee die experimentelle Entwicklungsökonomie grundlegend verändert. Statt grosse Theorien über Armut aufzustellen, fragt sie: **«Was funktioniert tatsächlich — und wie wissen wir das?»** Ihre Methode: Hypothesen mit Feldexperimenten testen, Ergebnisse messen, aus den Daten lernen.

Zentrale Werke:
- Banerjee, A. V., & Duflo, E. (2009). *The Experimental Approach to Development Economics.* Annual Review of Economics, 1, 151–178.
- Banerjee, A. V., & Duflo, E. (2011). *Poor Economics.* PublicAffairs.
- Duflo, E., Glennerster, R., & Kremer, M. (2007). *Using Randomization in Development Economics Research: A Toolkit.* Handbook of Development Economics, 4.

---

## 2. Die fünf Duflo-Kriterien

Esther Duflo würde euer Feld-Experiment anhand von fünf zentralen Kriterien bewerten. Jedes Kriterium ist gleichzeitig eine **Denkfrage**, die ihr auf euren eigenen Projektvorschlag anwenden sollt.

### Kriterium 1: Randomisierung und Identifikation

> *«If you want to know whether something works, you have to test it — and you have to test it right.»*
> — Esther Duflo

**Die Frage:** Wie stellt ihr sicher, dass der beobachtete Effekt **kausal** auf eure Intervention zurückzuführen ist?

| Element | Was Duflo prüfen würde | Euer Experiment |
|---------|------------------------|-----------------|
| **Randomisierung** | Werden Treatment- und Kontrollgruppe zufällig zugewiesen? | ☐ Ja / ☐ Nein — Begründung: |
| **Selektionsbias** | Gibt es systematische Unterschiede zwischen den Gruppen vor der Intervention? | ☐ Ausgeschlossen / ☐ Mögliches Risiko — Beschreibung: |
| **Confounders** | Welche Störvariablen könnten den Effekt verzerren? | Liste: |
| **Identifikationsstrategie** | Falls kein RCT: Welche alternative Strategie (DiD, IV, RDD) wird verwendet? | Strategie: |

**Typische Duflo-Rückfrage:**
«Du sagst, deine Intervention wirkt. Aber woher weisst du, dass der Effekt nicht von etwas anderem kommt? Zeig mir die Identifikationsstrategie.»

---

### Kriterium 2: Messbarkeit der Outcomes

> *«What you can't measure, you can't improve.»*

**Die Frage:** Sind eure Outcome-Variablen **konkret, messbar und relevant**?

| Prüfpunkt | Beschreibung | Euer Experiment |
|-----------|--------------|-----------------|
| **Primärer Outcome** | Was genau messt ihr? (Eine Variable, klar definiert) | Variable: |
| **Sekundäre Outcomes** | Welche zusätzlichen Effekte erwartet ihr? | Variablen: |
| **Messintervall** | Wann messt ihr? (Vorher/Nachher, Follow-up?) | Zeitpunkte: |
| **Datenquelle** | Woher kommen die Daten? (Survey, Admin-Daten, Beobachtung?) | Quelle: |
| **Operationalisierung** | Wie wird ein abstraktes Konzept (z.B. «Wohlbefinden») in eine messbare Grösse übersetzt? | Definition: |

**Typische Duflo-Rückfrage:**
«Du willst ‹Nachhaltigkeit› messen. Was genau bedeutet das? Ist es CO₂-Ausstoss pro Kopf? Recycling-Quote? Subjektives Umweltbewusstsein? Sag mir die Zahl, die sich ändern soll.»

---

### Kriterium 3: Kausalität und Theorie des Wandels

> *«You need a theory of change — but the experiment tells you if the theory is right.»*

**Die Frage:** Durch welchen **Mechanismus** soll eure Intervention wirken?

Erstellt eine **Theory of Change** (ToC) für euer Experiment:

```
┌───────────────┐     ┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│   INPUTS      │────►│  ACTIVITIES   │────►│   OUTPUTS     │────►│   OUTCOMES    │
│               │     │               │     │               │     │               │
│ Was investiert│     │ Was wird      │     │ Was wird      │     │ Was verändert │
│ ihr?          │     │ getan?        │     │ produziert?   │     │ sich?         │
└───────────────┘     └───────────────┘     └───────────────┘     └───────────────┘
                                                                         │
                                                                         ▼
                                                                  ┌───────────────┐
                                                                  │    IMPACT     │
                                                                  │               │
                                                                  │ Langfristiger │
                                                                  │ Effekt        │
                                                                  └───────────────┘
```

| Element | Beschreibung | Euer Experiment |
|---------|--------------|-----------------|
| **Kausaler Mechanismus** | Warum sollte die Intervention den Outcome verändern? | Mechanismus: |
| **Annahmen** | Welche Annahmen müssen gelten, damit der Mechanismus funktioniert? | Annahmen: |
| **Verhaltenskanal** | Über welchen Verhaltenskanal wirkt die Intervention? (Information, Anreize, Defaults, soziale Normen?) | Kanal: |
| **Alternativerklärungen** | Was könnte den Effekt sonst erklären? | Alternativen: |

**Typische Duflo-Rückfrage:**
«Du hast einen Effekt gefunden — grossartig. Aber warum? Wenn du den Mechanismus nicht verstehst, weisst du nicht, ob die Intervention anderswo auch funktioniert.»

---

### Kriterium 4: Skalierbarkeit und externe Validität

> *«The question is not just ‹does it work here?› but ‹will it work there?›»*

**Die Frage:** Können die Ergebnisse eures Experiments auf andere Kontexte **übertragen** werden?

| Dimension | Frage | Euer Experiment |
|-----------|-------|-----------------|
| **Populationstransfer** | Gilt der Effekt auch für andere Zielgruppen? | ☐ Ja / ☐ Eingeschränkt — Warum: |
| **Kontexttransfer** | Gilt der Effekt auch in anderen Ländern, Kulturen, Institutionen? | ☐ Ja / ☐ Eingeschränkt — Warum: |
| **Zeittransfer** | Ist der Effekt über Zeit stabil oder verschwindet er? | ☐ Stabil / ☐ Unklar — Begründung: |
| **Skalierung** | Was passiert, wenn die Intervention von 100 auf 100'000 Personen skaliert wird? | Herausforderungen: |
| **General Equilibrium** | Verändert die Skalierung die Rahmenbedingungen selbst? | ☐ Ja / ☐ Nein — Erklärung: |

**Typische Duflo-Rückfrage:**
«Dein Experiment funktioniert in einem Dorf in Kenia. Aber wird es auch in einem Slum in Mumbai funktionieren? Was ist anders am Kontext?»

---

### Kriterium 5: Ethik und Forschungsverantwortung

> *«We have a responsibility — to the people we study, and to the truth.»*

**Die Frage:** Ist euer Experiment **ethisch vertretbar** — und habt ihr das systematisch geprüft?

| Prüfpunkt | Beschreibung | Euer Experiment |
|-----------|--------------|-----------------|
| **Informed Consent** | Wissen die Teilnehmenden, dass sie an einem Experiment teilnehmen? | ☐ Ja / ☐ Nein — Begründung: |
| **Schaden vermeiden** | Kann die Kontrollgruppe durch Nicht-Behandlung Schaden nehmen? | ☐ Kein Schaden / ☐ Möglicher Schaden — Beschreibung: |
| **Equipoise** | Gibt es echte Unsicherheit darüber, ob die Intervention wirkt? (Wenn ihr schon wisst, dass sie wirkt, ist Randomisierung ethisch problematisch.) | ☐ Echte Unsicherheit / ☐ Problematisch |
| **Datenschutz** | Wie werden personenbezogene Daten geschützt? | Massnahmen: |
| **Nachsorge** | Was passiert nach dem Experiment? Erhalten die Kontrollgruppen die Intervention? | Plan: |
| **Ethikkommission** | Wurde das Experiment von einer Ethikkommission geprüft? | ☐ Ja / ☐ Geplant / ☐ Nicht erforderlich |

**Typische Duflo-Rückfrage:**
«Du randomisierst den Zugang zu einer Bildungsintervention. Die Kontrollgruppe bekommt nichts. Wie gehst du damit um, dass du bewusst Menschen ausschliesst?»

---

## 3. Übungsablauf

### Phase 1: Vorbereitung (individuell, vor der Sitzung)

**Aufgabe:** Lest euren eigenen Projektvorschlag noch einmal durch und beantwortet für jedes der fünf Duflo-Kriterien die Prüffragen in Abschnitt 2. Bringt eure ausgefüllte Selbstbewertung mit.

**Leseliste (Pflicht):**
- Banerjee & Duflo (2009): *The Experimental Approach to Development Economics*, Kapitel 1–3
- J-PAL Policy Briefcase eurer Wahl: [www.povertyactionlab.org/policy-insights](https://www.povertyactionlab.org/policy-insights)

**Leseliste (empfohlen):**
- Duflo, Glennerster & Kremer (2007): *Using Randomization in Development Economics Research: A Toolkit*, Abschnitt 2–4
- Angrist & Pischke (2009): *Mostly Harmless Econometrics*, Kapitel 2 (Randomisierung)

---

### Phase 2: Peer-Review «Im Geiste Duflos» (in 3er-Gruppen, 45 min)

**Schritt 1: Rollen zuweisen (5 min)**

In jeder 3er-Gruppe gibt es drei Rollen, die nach jeder Runde rotieren:

| Rolle | Aufgabe |
|-------|---------|
| **Präsentator:in** | Stellt den Projektvorschlag in 5 Minuten vor |
| **Duflo-Reviewer:in** | Gibt Feedback anhand der 5 Kriterien — streng, aber konstruktiv |
| **Protokollant:in** | Dokumentiert die wichtigsten Punkte und die Bewertung |

**Schritt 2: Präsentation (5 min pro Person)**

Der/die Präsentator:in stellt den Projektvorschlag vor. Fokus auf:
- Was ist die Forschungsfrage?
- Was ist die Intervention?
- Was ist das experimentelle Design?
- Was ist der erwartete Effekt?

**Schritt 3: Duflo-Review (10 min pro Person)**

Der/die Duflo-Reviewer:in bewertet den Vorschlag anhand des **Duflo-Scorecards** (siehe Abschnitt 4). Dabei:

- **Seid streng, aber fair.** Duflo ist bekannt dafür, Schwächen im Design direkt anzusprechen — aber immer mit dem Ziel, das Experiment besser zu machen.
- **Formuliert konkrete Verbesserungsvorschläge.** Nicht nur «Das ist ein Problem», sondern «Das könntest du so lösen: ...».
- **Stellt die Duflo-Rückfragen.** Nutzt die typischen Rückfragen aus Abschnitt 2.

**Schritt 4: Rotation**

Nach jeder Runde wechseln die Rollen. Am Ende hat jede Person einmal präsentiert, einmal reviewed und einmal protokolliert.

---

### Phase 3: Plenum und Synthese (30 min)

**Aufgabe 1: Häufigste Schwachstellen**

Jede Gruppe nennt die **zwei häufigsten Schwachstellen**, die in den Projektvorschlägen aufgefallen sind. Nils Handler sammelt diese an der Tafel.

**Aufgabe 2: Duflo-Prinzipien destillieren**

Gemeinsam erarbeiten wir aus den Erfahrungen der Peer-Reviews eine Liste von **«Duflo-Prinzipien für gute Feldexperimente»**. Diese Prinzipien gelten als Referenz für die weitere Arbeit an euren Projekten.

**Aufgabe 3: Reflexion**

Jede:r beantwortet für sich:
1. Was war die wichtigste Erkenntnis aus dem Duflo-Review meines Projekts?
2. Welche konkrete Änderung werde ich an meinem Projektvorschlag vornehmen?
3. Gibt es eine Frage, die ich nicht beantworten konnte — und wo ich Hilfe brauche?

---

## 4. Duflo-Scorecard

Nutzt diese Scorecard für das strukturierte Feedback. Jedes Kriterium wird auf einer Skala von 1–5 bewertet.

### Bewertungsskala

| Score | Bedeutung | Beschreibung |
|-------|-----------|--------------|
| **5** | Exzellent | Duflo wäre begeistert — methodisch sauber, klar begründet |
| **4** | Gut | Solide Basis, kleine Verbesserungen möglich |
| **3** | Akzeptabel | Grundidee erkennbar, aber signifikante Lücken im Design |
| **2** | Schwach | Fundamentale Probleme in der Identifikation oder Messung |
| **1** | Ungenügend | Kein erkennbares experimentelles Design oder schwere Mängel |

### Scorecard-Vorlage

```
┌─────────────────────────────────────────────────────────────────────────┐
│  DUFLO-SCORECARD                                                        │
│  Projektvorschlag: _______________________________________________      │
│  Reviewer:in: ____________________________________________________      │
│  Datum: __________________________________________________________      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  KRITERIUM 1: Randomisierung und Identifikation              ___/5      │
│  Kommentar: ________________________________________________________    │
│  ____________________________________________________________________   │
│  Verbesserungsvorschlag: ____________________________________________   │
│                                                                         │
│  KRITERIUM 2: Messbarkeit der Outcomes                       ___/5      │
│  Kommentar: ________________________________________________________    │
│  ____________________________________________________________________   │
│  Verbesserungsvorschlag: ____________________________________________   │
│                                                                         │
│  KRITERIUM 3: Kausalität und Theorie des Wandels             ___/5      │
│  Kommentar: ________________________________________________________    │
│  ____________________________________________________________________   │
│  Verbesserungsvorschlag: ____________________________________________   │
│                                                                         │
│  KRITERIUM 4: Skalierbarkeit und externe Validität           ___/5      │
│  Kommentar: ________________________________________________________    │
│  ____________________________________________________________________   │
│  Verbesserungsvorschlag: ____________________________________________   │
│                                                                         │
│  KRITERIUM 5: Ethik und Forschungsverantwortung              ___/5      │
│  Kommentar: ________________________________________________________    │
│  ____________________________________________________________________   │
│  Verbesserungsvorschlag: ____________________________________________   │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│  GESAMTSCORE:                                                ___/25     │
│                                                                         │
│  ZUSAMMENFASSUNG (2–3 Sätze):                                           │
│  ____________________________________________________________________   │
│  ____________________________________________________________________   │
│  ____________________________________________________________________   │
│                                                                         │
│  TOP-STÄRKE des Vorschlags:                                             │
│  ____________________________________________________________________   │
│                                                                         │
│  TOP-SCHWÄCHE und wie sie behoben werden kann:                          │
│  ____________________________________________________________________   │
│  ____________________________________________________________________   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Vertiefung: Verhaltensökonomische Perspektive

Esther Duflos Arbeit berührt zahlreiche verhaltensökonomische Mechanismen. Wenn ihr euer Feldexperiment designt, prüft zusätzlich diese **verhaltensökonomischen Hebel**:

### Checkliste: Verhaltensökonomische Dimensionen im Feldexperiment

| Dimension | Frage für euer Experiment | Relevante Theorie |
|-----------|--------------------------|-------------------|
| **Soziale Normen** | Nutzt eure Intervention soziale Vergleiche oder Peer-Effekte? | Fehr & Schmidt (1999): Fairness und Kooperation |
| **Default-Effekte** | Gibt es in eurem Design einen Default — und ist er bewusst gewählt? | Thaler & Sunstein (2008): Nudge |
| **Verlustaversion** | Framt eure Intervention Gewinne oder Verluste? | Kahneman & Tversky (1979): Prospect Theory |
| **Zeitinkonsistenz** | Müssen Teilnehmende jetzt handeln für zukünftigen Nutzen? Wie geht ihr mit Present Bias um? | Laibson (1997): Quasi-hyperbolic Discounting |
| **Kognitive Überlastung** | Ist die Entscheidungssituation einfach genug? Sind zu viele Optionen vorhanden? | Iyengar & Lepper (2000): Choice Overload |
| **Reziprozität** | Setzt eure Intervention auf Gegenseitigkeit? | Fehr & Gächter (2000): Cooperation and Punishment |
| **Salience** | Ist die relevante Information sichtbar und im richtigen Moment verfügbar? | Bordalo, Gennaioli & Shleifer (2012): Salience Theory |
| **Commitment Devices** | Können Teilnehmende sich vorab binden? | Bryan, Karlan & Nelson (2010): Commitment Devices |

### Anwendungsbeispiel

**Experiment:** Erhöhung der Recycling-Quote in Studierendenwohnheimen

| Dimension | Anwendung im Experiment |
|-----------|------------------------|
| Soziale Normen | Treatment: «85% deiner Nachbar:innen recyceln bereits» |
| Default | Recycling-Container direkt neben dem Abfalleimer (kein Zusatzaufwand) |
| Salience | Farbige Markierungen am Container + wöchentliche Rückmeldung |
| Commitment | Teilnehmende unterschreiben «Recycling-Pledge» am Semesterstart |

---

## 6. Häufige Fehler — und wie Duflo sie korrigieren würde

| Fehler | Warum es ein Problem ist | Duflos Korrektur |
|--------|--------------------------|------------------|
| **«Wir vergleichen Teilnehmende, die sich freiwillig gemeldet haben, mit denen, die nicht teilnehmen.»** | Selektionsbias: Freiwillige unterscheiden sich systematisch von Nicht-Freiwilligen. | «Randomisiere die Einladung zur Teilnahme, nicht die Teilnahme selbst. Dann hast du ein Intent-to-Treat Design.» |
| **«Unser Outcome ist ‹nachhaltiges Verhalten›.»** | Zu vage. Nicht messbar. | «Definiere genau eine Zahl. Zum Beispiel: kg CO₂ pro Kopf pro Monat, gemessen über Stromverbrauchsdaten.» |
| **«Wir erwarten einen grossen Effekt.»** | Ohne Power-Analyse ist die Stichprobe vermutlich zu klein. | «Wie gross muss dein Sample sein, um einen Effekt von X mit 80% Power zu entdecken? Rechne es aus.» |
| **«Wir haben kein Budget für eine Kontrollgruppe.»** | Ohne Kontrollgruppe kein kausaler Schluss. | «Dann mach ein Stepped-Wedge Design: Alle bekommen die Intervention, aber zeitlich versetzt. Die Noch-nicht-Behandelten sind deine Kontrolle.» |
| **«Wir können nicht randomisieren, weil es unfair wäre.»** | Berechtigter Einwand — aber lösbar. | «Verwende eine Waitlist-Control oder überkreuze: Gruppe A bekommt Intervention 1 zuerst, Gruppe B Intervention 2. So bekommt jede:r etwas.» |
| **«Unser Experiment hat bei 50 Personen funktioniert.»** | Geringe statistische Power, Ergebnisse möglicherweise nicht replizierbar. | «Zeig mir den Konfidenzintervall. Wenn er von –0.5 bis +1.5 geht, weisst du eigentlich nichts.» |

---

## 7. Weiterführende Ressourcen

### Pflichtlektüre
- Banerjee, A. V., & Duflo, E. (2009). The Experimental Approach to Development Economics. *Annual Review of Economics*, 1, 151–178.

### Empfohlene Lektüre
- Duflo, E., Glennerster, R., & Kremer, M. (2007). Using Randomization in Development Economics Research: A Toolkit. *Handbook of Development Economics*, 4.
- Angrist, J. D., & Pischke, J.-S. (2009). *Mostly Harmless Econometrics.* Princeton University Press. (Kapitel 2)
- Banerjee, A. V., & Duflo, E. (2011). *Poor Economics.* PublicAffairs.
- List, J. A. (2011). Why Economists Should Conduct Field Experiments and 14 Tips for Pulling One Off. *Journal of Economic Perspectives*, 25(3), 3–16.

### J-PAL Ressourcen
- J-PAL Research Resources: [www.povertyactionlab.org/research-resources](https://www.povertyactionlab.org/research-resources)
- J-PAL Policy Insights: [www.povertyactionlab.org/policy-insights](https://www.povertyactionlab.org/policy-insights)

### Verhaltensökonomische Grundlagen
- Fehr, E., & Schmidt, K. M. (1999). A Theory of Fairness, Competition, and Cooperation. *Quarterly Journal of Economics*, 114(3), 817–868.
- Kahneman, D., & Tversky, A. (1979). Prospect Theory: An Analysis of Decision under Risk. *Econometrica*, 47(2), 263–291.
- Thaler, R. H., & Sunstein, C. R. (2008). *Nudge: Improving Decisions About Health, Wealth, and Happiness.* Yale University Press.

---

## 8. Abgabe und Bewertung

### Was ihr abgebt

1. **Ausgefüllte Selbstbewertung** (Abschnitt 2, alle 5 Kriterien) — vor der Sitzung
2. **Ausgefüllte Duflo-Scorecard** (Abschnitt 4) für das Projekt, das ihr reviewed habt — nach der Sitzung
3. **Überarbeiteter Projektvorschlag** (1–2 Seiten) mit dokumentierten Änderungen basierend auf dem Feedback — innerhalb einer Woche

### Bewertungskriterien für die Überarbeitung

| Kriterium | Gewichtung | Beschreibung |
|-----------|------------|--------------|
| **Qualität der Reaktion auf Feedback** | 40% | Wurden die identifizierten Schwächen adressiert? |
| **Methodische Verbesserung** | 30% | Hat sich die Identifikationsstrategie, Messung oder das Design verbessert? |
| **Reflexionstiefe** | 20% | Zeigt die Überarbeitung ein Verständnis der zugrundeliegenden methodischen Prinzipien? |
| **Darstellung** | 10% | Ist der überarbeitete Vorschlag klar strukturiert und verständlich? |

---

## Anhang A: Kurzprofil Esther Duflo

| | |
|---|---|
| **Name** | Esther Duflo |
| **Geboren** | 1972, Paris, Frankreich |
| **Position** | Abdul Latif Jameel Professor of Poverty Alleviation and Development Economics, MIT |
| **Nobelpreis** | 2019 (gemeinsam mit Abhijit Banerjee und Michael Kremer) |
| **Beitrag** | Experimenteller Ansatz zur Armutsbekämpfung |
| **Methode** | Randomisierte kontrollierte Studien (RCTs) in Entwicklungsländern |
| **Institution** | Co-Gründerin und Co-Direktorin, J-PAL (Abdul Latif Jameel Poverty Action Lab) |
| **Kernüberzeugung** | «Fight poverty with evidence, not ideology.» |

### Duflos wichtigste methodische Prinzipien

1. **Randomisierung ist der Goldstandard** — aber nicht der einzige Weg zu kausaler Evidenz
2. **Kleine, gut designte Experimente** sind oft wertvoller als grosse, schlecht designte
3. **Mechanismen verstehen** ist wichtiger als nur Effekte messen
4. **Externe Validität** muss aktiv hergestellt werden — sie kommt nicht automatisch
5. **Ethik ist kein Hindernis**, sondern Teil guter Forschung
6. **Replikation und Transparenz** sind nicht optional

---

## Anhang B: Glossar

| Begriff | Definition |
|---------|------------|
| **RCT** | Randomized Controlled Trial — randomisierte kontrollierte Studie |
| **Treatment** | Die Intervention, die getestet wird |
| **Control** | Die Vergleichsgruppe, die keine Intervention erhält |
| **Intent-to-Treat (ITT)** | Analyse, die alle Zugewiesenen einschliesst, unabhängig davon, ob sie die Intervention tatsächlich erhalten haben |
| **Average Treatment Effect (ATE)** | Durchschnittlicher kausaler Effekt der Intervention |
| **Power** | Statistische Macht — die Wahrscheinlichkeit, einen tatsächlich vorhandenen Effekt zu entdecken |
| **Externe Validität** | Übertragbarkeit der Ergebnisse auf andere Populationen, Kontexte und Zeitpunkte |
| **Selektionsbias** | Verzerrung durch systematische Unterschiede zwischen Treatment- und Kontrollgruppe |
| **Spillover** | Effekte der Intervention, die auf die Kontrollgruppe «überschwappen» |
| **Attrition** | Ausfall von Teilnehmenden während des Experiments |
| **DiD** | Difference-in-Differences — Vergleich von Veränderungen über Zeit zwischen Treatment- und Kontrollgruppe |
| **RDD** | Regression Discontinuity Design — Nutzung eines Schwellenwerts für kausale Identifikation |
| **IV** | Instrumental Variable — Nutzung einer exogenen Variable zur kausalen Identifikation |
| **Stepped-Wedge Design** | Experimentelles Design, bei dem alle Gruppen die Intervention erhalten, aber zeitlich versetzt |
| **Equipoise** | Echter Zustand der Unsicherheit darüber, ob eine Intervention wirkt |

---

*Diese Übungsanleitung wurde für den Kurs «Feldexperimente in der Praxis» (Nils Handler) entwickelt. Version 1.0, Februar 2026.*
