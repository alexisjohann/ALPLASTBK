# BEATRIX Live-Einführung — Demo-Script

**Meeting:** 19.02.2026 | Marcel Aisslinger, Rebecca Äbli, Boletin Asani
**FehrAdvice:** Manuel
**Dauer:** 40-50 Minuten
**Ziel:** Marcel zeigt seinem Team live, was BEATRIX kann

---

## Vorbereitung (vor dem Meeting)

- [ ] Laptop mit Claude Code / BEATRIX offen
- [ ] UBS-Daten geladen (passiert automatisch)
- [ ] Beamer/Screen-Share bereit
- [ ] Dieses Script als Leitfaden

---

## Einführung: «Was ist BEATRIX?» (10 min)

### Warum diese Einführung
Rebecca und Boletin kennen BEATRIX nicht. Marcel hat es beim ersten Treffen gesehen, aber sein Team braucht den Kontext. Ziel: In 10 Minuten verstehen alle, WARUM BEATRIX existiert und WAS es anders macht als andere Beratungstools.

### Einstieg (Manuel erzählt, kein Screen nötig)

> «Stellt euch vor, ihr plant eine Kampagne für eure 3.7 Millionen Kunden. Ihr habt Daten, ihr habt Erfahrung, ihr habt Bauchgefühl. Aber eine Frage bleibt: Warum funktioniert dieselbe Kampagne bei einem Segment — und bei einem anderen nicht?»

**Pause. Blickkontakt.**

> «Die Antwort ist Kontext. Dieselbe Botschaft, dasselbe Angebot, derselbe Kanal — aber ein anderer Mensch in einer anderen Situation reagiert komplett anders. Und diesen Kontext systematisch zu verstehen — dafür haben wir BEATRIX gebaut.»

### Die 3 Kernaussagen (je 2 Minuten)

**1. «BEATRIX ist kein Chatbot»**

> «BEATRIX ist kein ChatGPT, das schöne Texte schreibt. BEATRIX ist ein Analysesystem, das auf über 2'300 wissenschaftlichen Papers basiert — aufgebaut vom Team um Prof. Ernst Fehr an der Universität Zürich. Jede Zahl, jeder Parameter kommt aus der Forschung, nicht aus dem Bauchgefühl.»

Kernbotschaft: **Wissenschaft, nicht Meinung.**

**2. «Kontext ist der Multiplikator»**

> «In der klassischen Verhaltensökonomie heisst es: Menschen gewichten Verluste 2.25× stärker als Gewinne. Das ist der Durchschnitt. Aber bei euren Ex-Credit-Suisse-Kunden, die gerade die Bank gewechselt haben und verunsichert sind? Da ist der Wert 2.5×. Bei euren langjährigen UBS-Kunden? 1.8×. Derselbe psychologische Effekt — aber der Kontext verändert die Intensität. BEATRIX modelliert genau das.»

Kernbotschaft: **Keine Durchschnittswerte — eure Situation, eure Zahlen.**

**3. «Von der Analyse zur Massnahme»**

> «Die meisten Analysen enden mit ‹Hier sind die Insights›. BEATRIX geht weiter: Es modelliert eure Kundensegmente, designt konkrete Massnahmen, und simuliert die Wirkung — bevor ihr einen Franken ausgebt. Und genau das zeigen wir euch jetzt live.»

Kernbotschaft: **Nicht nur verstehen — handeln.**

### Überleitung zu Station 1

> «Genug Theorie. Lasst mich euch zeigen, was BEATRIX über UBS bereits weiss.»

**→ Laptop öffnen, BEATRIX starten.**

---

## Station 1: «Wir kennen euren Kontext» (10 min)

### Was zeigen
BEATRIX kennt UBS bereits — 350 dokumentierte Kontextfaktoren.

### Live-Aktion
Frage an BEATRIX stellen:

> «Was sind die 5 grössten Behavioral Challenges für UBS Growth Marketing im Kontext der CS-Integration?»

### Was BEATRIX zeigt
- Automatische Kontextanalyse (350 Faktoren werden referenziert)
- 8 Kontext-Dimensionen (FIN, MKT, STR, PEO, TEC, ORG, RIS, STK)
- UBS-spezifische Parameter: λ_UBS = 1.8, τ_CH = 0.85, τ_CS-Migrierte = 0.55

### Talking Points
- «Das ist kein generisches Tool — das sind EURE 350 Kontextfaktoren»
- «Jede Empfehlung basiert auf eurem spezifischen Kontext, nicht auf Durchschnittswerten»
- «Die CS-Integration verändert die Parameter: Vertrauen bei Ex-CS-Kunden ist 0.55 statt 0.85»

### Wow-Moment für das Team
Zeigen: `ubs_context_master_overview.yaml` — 350 Faktoren in 8 Dimensionen, spezifisch für UBS.

---

## Station 2: «Euer Modell existiert bereits» (10 min)

### Was zeigen
MOD-UBS-GMA-001 — das Growth Marketing Activation Modell, gebaut für Marcels Team.

### Live-Aktion
Frage an BEATRIX:

> «Zeig mir das 10C-Modell für UBS Growth Marketing — welches Segment hat das grösste Potenzial?»

### Was BEATRIX zeigt
4 Segmente mit unterschiedlichen Parametern:

| Segment | Kunden | Vertrauen (τ) | Verlust-Aversion (λ) | Aktivierungspotenzial |
|---------|--------|---------------|----------------------|----------------------|
| UBS Legacy | 1.5M | 0.85 | 1.8 | Mittel |
| **CS-Migrierte** | **1.0M** | **0.55** | **2.5** | **Höchstes** |
| Digital-Only | 800k | 0.70 | 1.6 | Hoch |
| Affluent | 400k | 0.80 | 2.1 | Mittel-Hoch |

### Talking Points
- «CS-Migrierte haben das grösste Potenzial UND das grösste Risiko»
- «λ = 2.5 heisst: Verluste wiegen 2.5× schwerer als Gewinne — deshalb funktioniert ‹Verpassen Sie nicht› besser als ‹Gewinnen Sie›»
- «Jedes Segment braucht eine andere Ansprache — BEATRIX zeigt welche»

### Interaktion mit Team
Fragen: «Rebecca, Boletin — welches Segment betreut ihr primär?»
→ Antwort nutzen für Station 3.

---

## Station 3: «Von der Analyse zur Massnahme» (10 min)

### Was zeigen
BEATRIX designt konkrete, wissenschaftlich fundierte Interventionen — keine generischen Tipps.

### Live-Aktion
Basierend auf der Antwort aus Station 2, Frage an BEATRIX:

> «Designe eine Intervention für [Segment X]: Wie aktivieren wir diese Kunden für Save & Invest?»

### Was BEATRIX zeigt
- 10C-Zieldimension (z.B. AWARE → Awareness erhöhen)
- Konkreter Interventions-Vorschlag mit 20-Field Schema
- Wissenschaftliche Fundierung (z.B. Conditional Cooperation nach Fischbacher et al. 2001)
- Erwarteter Lift (+15-25% Conversion bei Social Proof)
- Crowding-Out Warnung (wenn Social + Financial kombiniert → Risiko)

### Talking Points
- «Jede Massnahme hat eine Theorie dahinter — nicht ‹Bauchgefühl›»
- «BEATRIX warnt auch, wenn Massnahmen sich gegenseitig kannibalisieren»
- «Die 3 Behavioral Models dahinter: Conditional Cooperation, Social Image, Identity Economics»

### Konkretes Beispiel zeigen
Campaign-Architektur «Invest Like You»:
1. **Welle 1 — Social Proof** (4 Wochen): «83% der UBS-Kunden in deinem Alter haben einen Sparplan»
2. **Welle 2 — Identity** (4 Wochen): «Welcher Anlegertyp bist du?» Quiz
3. **Welle 3 — Image & Values** (laufend): Sharing-Mechanismen

---

## Station 4: «Was würden eure Kunden sagen?» (10 min)

### Was zeigen
BEATRIX simuliert Kundenreaktionen — bevor die Kampagne live geht.

### Live-Aktion

> «Simuliere: Wie reagiert ein Ex-Credit-Suisse-Kunde (45, CHF 500k Vermögen, skeptisch) auf die Social-Proof-Kampagne?»

### Was BEATRIX zeigt
- Persona-basierte Reaktionssimulation
- Barrieren-Analyse (Vertrauen τ=0.55 → «Warum sollte ich der UBS glauben?»)
- Empfohlene Anpassung (z.B. «Vertrauenssignal zuerst, dann Social Proof»)
- Vergleich: Mit vs. ohne Anpassung

### Talking Points
- «Statt 6 Wochen A/B-Test: BEATRIX simuliert die Reaktion in Sekunden»
- «Das ersetzt keinen echten Test — aber es spart die ersten 3 Iterationen»
- «Wir können jede Persona, jedes Segment, jede Kampagne durchspielen»

---

## Abschluss & Nächste Schritte (5 min)

### Zusammenfassung

> «Was ihr gesehen habt:
> 1. BEATRIX kennt UBS — 350 Kontextfaktoren, nicht generisch
> 2. Euer Modell existiert — 4 Segmente, spezifische Parameter
> 3. Wissenschaftlich fundierte Massnahmen — nicht Bauchgefühl
> 4. Simulation vor dem Launch — spart Zeit und Geld»

### Call to Action
- «Wo seht ihr den grössten Hebel für euer Team?»
- «Welches Projekt wollen wir als erstes mit BEATRIX angehen?»

### Vorbereitet als Leave-Behind
- MOD-UBS-GMA-001 (das Modell, das wir gezeigt haben)
- 3 Briefings (AI Marketing, Crypto Communication, Feel Switzerland)
- BEATRIX Extension Proposal (`2026_beatrix_extension_marketing.yaml`)

---

## Notizen für Manuel

### Dos
- BEATRIX live nutzen, nicht Slides zeigen — das Team soll die Interaktion sehen
- Rebecca und Boletin aktiv einbeziehen — sie sollen Fragen stellen
- Auf Marcels Reaktion achten — er kennt BEATRIX vom Konzept, sein Team nicht
- UBS-spezifische Daten betonen — das unterscheidet uns von jedem Berater

### Don'ts
- Nicht zu technisch werden (kein YAML zeigen, keine Formeln)
- Nicht alles auf einmal zeigen — 4 Stationen reichen
- Nicht versprechen, was BEATRIX nicht kann (kein Ersatz für echte Daten)
- Nicht über CoE XD Pilot reden, es sei denn Marcel bringt es auf — das ist ein separater Track

### Falls Fragen kommen
- **«Was kostet das?»** → Auf BEATRIX Extension Proposal verweisen, konkretes Angebot folgt
- **«Wie lange dauert das?»** → Phase 0 (Alignment): 2 Wochen, Phase 1 (Transfer): 4 Wochen
- **«Brauchen wir eigene Daten?»** → Nein für den Start — 350 Kontextfaktoren + Behavioral Models reichen. Eigene Daten verbessern die Kalibrierung
- **«Wer hat das gebaut?»** → Prof. Ernst Fehr (Universität Zürich) + FehrAdvice, basierend auf 2'300+ wissenschaftlichen Papers

---

*Erstellt: 2026-02-18 | Für Meeting: 2026-02-19*
