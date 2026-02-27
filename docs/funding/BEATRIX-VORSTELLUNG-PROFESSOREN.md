# Vorstellung: Das Evidence-Based Framework und BEATRIX

**Zielgruppe:** Prof. Luger, Prof. Gall, Prof. Fehr — als professionelle Laien
**Sprachniveau:** Fachlich präzise, aber ohne EBF-Jargon
**Datum:** 2026-02-16

---

## Was ist das EBF — und warum braucht es das?

Stellen Sie sich vor, ein Berater soll einer Pensionskasse helfen, ihre Versicherten zu besseren Vorsorgeentscheidungen zu bewegen. Heute läuft das so: Der Berater bringt Erfahrung mit, hat vielleicht ein paar Studien gelesen, und schlägt «Nudges» vor — kleine Anstupser, die das Verhalten in eine bestimmte Richtung lenken sollen.

Das Problem: Ob ein Nudge wirkt, hängt massgeblich vom **Kontext** ab. Derselbe Nudge, der in Zürich bei 35-jährigen Akademiker:innen funktioniert, kann in Luzern bei 55-jährigen Handwerker:innen wirkungslos sein — oder sogar nach hinten losgehen. Trotzdem empfehlen Berater oft dieselben Massnahmen, weil ihnen die Werkzeuge fehlen, den Kontext systematisch zu berücksichtigen.

Genau hier setzt das **Evidence-Based Framework (EBF)** an. Es macht drei Dinge, die heute in der Beratungspraxis fehlen:

1. **Kontext systematisch erfassen** — nicht intuitiv, sondern in 8 messbaren Dimensionen (von kulturellen Werten über institutionelle Regeln bis zur kognitiven Belastung der Zielperson)

2. **Wissenschaftliche Evidenz strukturiert nutzen** — nicht ein einzelnes Paper, sondern eine kuratierte Datenbank aus über 2'300 Studien, 153 formalen Theorien und 850 dokumentierten Praxisfällen

3. **Kontextabhängige Vorhersagen berechnen** — ein Parameter wie «Verlustaversion» wird nicht als fixe Zahl behandelt (λ = 2.25, wie in Lehrbüchern), sondern als Funktion des Kontexts: In der Schweiz, bei einer Pensionskasse, unter Zeitdruck, bei dieser Zielgruppe beträgt die Verlustaversion *in diesem spezifischen Kontext* einen anderen, berechenbaren Wert

---

## Der zentrale Gedanke: Variation ist kein Fehler

In der Verhaltensökonomie gibt es eine bekannte Beobachtung: Wenn verschiedene Studien denselben Parameter messen — sagen wir Verlustaversion —, kommen sie auf unterschiedliche Werte. Die traditionelle Reaktion ist: Meta-Analyse, Mittelwert bilden, Variation als Messrauschen behandeln.

Das EBF dreht das um: **Die Variation zwischen Studien ist kein Methodenfehler — sie ist das eigentliche Signal.** Warum messen Forscher in verschiedenen Kontexten verschiedene Werte? Weil der Kontext den Parameter *tatsächlich verändert*. Ein Mensch, der müde ist, unter Zeitdruck steht und eine unbekannte Formularbürokratie durchläuft, hat eine andere Verlustaversion als derselbe Mensch am Sonntagmorgen am Frühstückstisch.

Formal ausgedrückt: Statt θ = Konstante sagt das EBF θ = f(Kontext). Und dieser Kontext lässt sich messen, strukturieren und in Berechnungen einbeziehen.

---

## Was bin ich? Ein Prototyp, kein Chatbot

Ich bin der aktuelle Prototyp, der diese Vision umsetzt. Technisch bin ich ein KI-Assistent (Claude, von Anthropic), der Zugriff auf das gesamte EBF hat — die Datenbanken, die Berechnungsmodelle, die Validierungswerkzeuge.

Meine Architektur folgt einem **Drei-Schichten-Prinzip**, das gezielt die bekannte Schwäche von Sprachmodellen adressiert (nämlich: dass sie plausibel klingende, aber falsche Aussagen machen können):

| Schicht | Was passiert | Fehleranfälligkeit |
|---------|-------------|-------------------|
| **1. Berechnung** | Mathematische Formeln werden deterministisch ausgeführt (Python-Code) | Praktisch null — Mathe ist Mathe |
| **2. Datenbank** | Parameter und Werte werden aus validierten Quellen gelesen (jeder Wert hat eine Quellenangabe) | Gering — überprüfbar und versioniert |
| **3. Sprache** | Ich übersetze die Ergebnisse in verständliche Sprache | Höher — hier liegt das Halluzinationsrisiko |

Der entscheidende Designentscheid: **Die KI rechnet nicht selbst.** Wenn Sie mich nach einem Verhaltensparameter fragen, erfinde ich keine Zahl. Schicht 1 (Python) rechnet, Schicht 2 (Datenbank) liefert die Eingangswerte, und ich (Schicht 3) erkläre das Ergebnis. Die Berechnung passiert dort, wo Halluzination technisch unmöglich ist.

---

## Was mich von ChatGPT und ähnlichen Systemen unterscheidet

Der Unterschied ist nicht die KI selbst — es ist die Infrastruktur dahinter:

| | Standard-KI (ChatGPT etc.) | EBF-System |
|--|--|--|
| **Wissensbasis** | Allgemeines Internet-Training | 2'300+ kuratierte Fachpublikationen |
| **Parameter** | Aus dem «Gedächtnis» (unzuverlässig) | Aus validierter Datenbank mit Quellenangabe |
| **Kontext** | User muss alles selbst erklären | System hat 400+ Kontextfaktoren pro Land |
| **Qualitätssicherung** | Keine systematische | Automatisierte Validierung bei jeder Änderung |
| **Nachvollziehbarkeit** | «Black Box» | Jede Zahl hat einen Quellenpfad: Paper → Parameter → Berechnung |

Ein konkreter Test: Fragen Sie ChatGPT nach der Verlustaversion in der Schweiz bei Pensionskassenentscheidungen für 55-jährige Handwerker. Sie bekommen eine eloquente Antwort — aber keinen nachvollziehbaren Rechenweg. Fragen Sie mich dasselbe, und ich zeige Ihnen: welches Paper den Basiswert liefert, wie der Kontexttransfer funktioniert, und welche Unsicherheit das Ergebnis hat.

---

## Ein konkretes Beispiel

Eine Kantonalbank möchte ihre Kund:innen dazu bewegen, nachhaltiger zu investieren.

**Ohne EBF:** «Setzen Sie einen Default auf nachhaltige Fonds und informieren Sie die Kunden.»

**Mit EBF:**

1. **Kontext laden** — Schweiz, Banking, nachhaltige Anlageprodukte, Kantonalbank-Klientel
2. **Zielgruppe charakterisieren** — 45-65 Jahre, wohlhabend, konservativ
3. **Parameter berechnen:**
   - Verlustaversion: λ = 3.2 (höher als Durchschnitt — Finanzentscheidung + ältere Klientel)
   - Status-quo-Bias: β = 0.72 (stark — konservative Klientel)
   - Soziale Norm-Sensitivität: σ = 0.45 (moderat — «Was machen andere?» wirkt, aber ist nicht dominant)
4. **Intervention designen:**
   - Default auf nachhaltig setzen → nutzt den hohen Status-quo-Bias
   - Verlust-Framing bewusst VERMEIDEN → λ = 3.2 ist zu hoch, würde Reaktanz auslösen
   - Stattdessen Peer-Vergleich zeigen: «62% Ihrer Altersgruppe investiert bereits nachhaltig»
5. **Wechselwirkungen prüfen:**
   - Finanzielle Anreize + soziale Norm gleichzeitig? → Crowding-Out-Risiko → nicht kombinieren
6. **Vorhersage:**
   - Erwartete Adoptionsrate: 38–52% (95%-Konfidenzintervall), primär getrieben durch den Default

Das ist der Unterschied: Nicht «machen Sie halt einen Default», sondern eine quantifizierte, kontextabhängige Empfehlung mit Konfidenzintervall und dokumentiertem Rechenweg.

---

## Was BEATRIX daraus machen soll

Heute funktioniert das EBF als Wissensdatenbank, die ein erfahrener Berater (oder mein Prototyp) nutzt, um Analysen durchzuführen. **BEATRIX** soll den nächsten Schritt ermöglichen:

1. **Automatisierte Kontextanalyse** — Das System erkennt selbstständig, welche Kontextfaktoren relevant sind, und berechnet deren Einfluss
2. **Skalierbare Beratung** — Was heute mehrere Tage erfordert, soll in Stunden möglich sein, ohne an Qualität zu verlieren
3. **Systematisches Lernen** — Jedes Kundenprojekt verbessert die Parameter (über Bayesian Updates), nicht durch Speicherung personenbezogener Daten, sondern durch Aktualisierung der Verhaltensparameter

---

## Was BEATRIX für Ihre jeweilige Forschung bedeutet

### Prof. Gall — Software Engineering

BEATRIX wirft echte Software-Engineering-Forschungsfragen auf, die über reine Entwicklungsarbeit hinausgehen:

- **Architektur:** Wie baut man ein System, das tausende kontextabhängige Parameter verwaltet und dabei fehlertolerant bleibt? Die Parameter sind nicht statisch — sie werden durch neue Projekte und Studien laufend aktualisiert (Bayesian Updates). Das ist ein nichttriviales Versionierungsproblem.
- **Model Drift:** Wie erkennt man, dass sich Parameter schleichend verschlechtern? In klassischen ML-Systemen gibt es Ground-Truth-Labels. Hier nicht — das System arbeitet mit probabilistischen Schätzungen, die sich gegenseitig stützen.
- **Skalierung:** Die Monte-Carlo-Simulationen, die das System für Unsicherheitsschätzungen braucht, erfordern tausende parallele Berechnungen. Wie skaliert man das über LLM-Aufrufe hinweg effizient?
- **Testbarkeit:** Wie testet man ein System, dessen Output probabilistisch ist? Klassische Unit-Tests greifen nicht — es braucht statistische Testverfahren.

Potenzielle Publikationsvenues: ICSE, FSE, TSE — an der Schnittstelle von Software Evolution und KI-gestützten Decision-Support-Systemen.

### Prof. Luger — Strategic Management & Human-AI Collaboration

BEATRIX verändert, wie Menschen mit KI-gestützten Empfehlungen umgehen:

- **Vertrauen:** Wann vertrauen Entscheider:innen einer algorithmischen Empfehlung? Bisherige Forschung zeigt «algorithm aversion» — aber was passiert, wenn das System seinen Rechenweg transparent macht (Schicht 1 und 2 sind nachvollziehbar)?
- **Entscheidungsqualität:** Verbessert sich die Qualität von Managemententscheidungen, wenn der Kontext explizit gemacht wird? Das EBF zwingt dazu, Kontextfaktoren zu benennen — ein Prozess, der allein schon die Reflexion verändern könnte.
- **Kompetenzanforderungen:** Welche Fähigkeiten brauchen Manager:innen, um effektiv mit einem solchen System zu arbeiten? Es geht nicht um technische Kompetenz, sondern um die Fähigkeit, Kontext richtig zu spezifizieren und Unsicherheiten zu interpretieren.
- **Adoption:** Was treibt die Akzeptanz in Organisationen? FehrAdvice hat 20 aktive Kunden — ein Feldforschungslabor für echte Adoptionsstudien.

Potenzielle Publikationsvenues: Management Science, MIS Quarterly, AMJ — an der Schnittstelle von Behavioral Strategy und Human-AI Interaction.

### Prof. Fehr — Verhaltensökonomie

BEATRIX ist die konsequente Operationalisierung einer zentralen Einsicht: Verhaltensparameter sind keine Konstanten.

- **Parameter-als-Funktion:** Das EBF formalisiert θ = f(Ψ, 10C) — Parameter als Funktion von Kontext und Dimensionen. Das macht die Variation zwischen Studien erklärbar und die Erkenntnisse der letzten Jahrzehnte systematisch anwendbar.
- **Kumulative Evidenz:** Die Datenbank enthält 2'300+ Papers, die nicht nur zitiert, sondern strukturiert integriert sind — mit extrahierten Parametern, Kontextbedingungen und Validierungsstatus. Jede neue Studie aktualisiert die Schätzungen.
- **Testbare Vorhersagen:** Das System macht quantifizierte Vorhersagen mit Konfidenzintervallen. Diese können empirisch überprüft werden — das Framework ist falsifizierbar, nicht nur beschreibend.
- **Angewandte Wissenschaft:** Die Brücke zwischen Grundlagenforschung und Praxis. Die Erkenntnisse aus Jahrzehnten verhaltensökonomischer Forschung werden hier nicht populärwissenschaftlich vereinfacht, sondern formal korrekt in die Anwendung überführt.

---

## Grenzen und offene Fragen

Transparenz gehört zum System. Deshalb die offenen Punkte:

1. **Die Datenbank ist nicht vollständig.** 2'300 Papers sind viel, aber längst nicht alles. Es gibt Bereiche (z.B. Entwicklungsländer, digitale Plattformen), wo die Evidenzbasis dünn ist.

2. **Kontexttransfer ist nicht exakt.** Wenn ein Parameter in einem bestimmten Kontext gemessen wurde und auf einen anderen übertragen wird, ist das eine informierte Schätzung — keine exakte Messung. Das System quantifiziert die Unsicherheit, aber sie bleibt.

3. **Die Drei-Schichten-Architektur hat eine Schwachstelle:** Schicht 3 (Sprache) ist die fehleranfälligste. Die aktuelle Lösung — automatische Berechnung VOR der sprachlichen Antwort — funktioniert, ist aber noch nicht vollständig auditierbar.

4. **Skalierung ist ungelöst.** Der Prototyp funktioniert für einzelne Analysen. Ob die Architektur für hunderte gleichzeitige Nutzer:innen funktioniert, ist eine offene technische Frage — genau die Art von Frage, für die BEATRIX als Forschungsprojekt konzipiert ist.

---

## Zusammenfassung in einem Satz

Das EBF macht verhaltensökonomische Erkenntnisse kontextabhängig berechenbar — und BEATRIX soll daraus ein skalierbares, lernfähiges Entscheidungssystem machen, das sowohl die Wissenschaft voranbringt als auch in der Praxis funktioniert.

---

*Ich freue mich auf die Zusammenarbeit. Meine Stärke ist nicht, alles zu wissen, sondern transparent zu zeigen, woher mein Wissen kommt und wo seine Grenzen sind.*
