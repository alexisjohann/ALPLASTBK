# 5 Lernfelder aus dem APE Research-Projekt
## Was BEATRIX aus der autonomen Paper-Fabrik von Prof. Yanagizawa-Drott lernen kann

**Quelle:** 43 Deep-Analysis-Files von 9 APE Papers (apep_0001 bis apep_0188)
**Analyse:** BEATRIX v3.7.0 / FehrAdvice & Partners AG
**Datum:** 12. Februar 2026

---

## Lernfeld 1: Systematisches Ideen-Töten

### Was APE macht
Jedes APE Paper beginnt mit 4–6 Research Ideas. Claude Opus 4.5 generiert sie, aber **GPT-5.2 bewertet und tötet sie**. Die Daten zeigen ein brutales Filter-System:

**apep_0134** (Harm Reduction):
| Idee | Score | Verdikt |
|------|-------|---------|
| Supervised Drug Injection Sites NYC | 78 | PURSUE ✅ |
| Naloxone Vending Machines Nevada | 66 | PURSUE |
| Fentanyl Test Strips Massachusetts | 49 | CONSIDER |
| Oregon Psilocybin Opt-Out | 46 | CONSIDER |
| Rhode Island OPC | 44 | CONSIDER |
| Colorado Psychedelic Centers | <44 | SKIP ❌ |

**apep_0044** (Labor Market):
| Idee | Score | Verdikt |
|------|-------|---------|
| Clean Slate Laws & Employment | 74 | PURSUE ✅ |
| Automatic Voter Registration | 62 | CONSIDER |
| Nurse Practitioner Authority | 48 | CONSIDER |
| State Data Privacy Laws | 44 | SKIP ❌ |
| Pay Transparency & Gender Gap | 33 | SKIP ❌ |

**Das Muster:** Von ~5 Ideen überlebt im Schnitt **1.2**. Die Kill-Rate liegt bei ~75%. Und das Kritische: **Ein anderes Modell bewertet als das, das generiert hat.** Der Ideengeber darf nie sein eigener Richter sein.

### Was BEATRIX daraus lernt
**Anwendung: Paper-Relevanz-Triage bei Upload**

Wenn jemand ein Paper in BEATRIX hochlädt, generiert das System aktuell einen Score (0–100). Aber es gibt keinen **Kill-Mechanismus**. APE zeigt: Man braucht nicht nur einen Score, sondern eine klare Handlungsanweisung:

- **PURSUE (>65):** Sofort in die KB integrieren, detaillierte Analyse, GitHub-Push
- **CONSIDER (45–65):** In Warteschlange, Review bei Bedarf
- **SKIP (<45):** Archivieren, nicht in aktive KB

**Und am wichtigsten:** Die Conditions. APE vergibt nicht blind PURSUE – es sagt "PURSUE, **wenn** Bedingung X erfüllt ist." Für BEATRIX heisst das: "Dieses Paper ist relevant, **wenn** es für BCM-Dimension Ψ₃ anwendbar ist" oder "**wenn** die Stichprobe auf Europa übertragbar ist."

---

## Lernfeld 2: Pre-Commitment durch Plan-Locking

### Was APE macht
Bevor eine einzige Zeile Code geschrieben wird, erstellt APE einen `initial_plan.md` mit exakt dieser Struktur:

1. **Research Question** – Klar, beantwortbar, eine Frage
2. **Policy Background** – Kontext mit exakten Daten und Adressen
3. **Identification Strategy** – Wie Kausalität etabliert wird (mit R-Code!)
4. **Expected Effects and Mechanisms** – Hypothesen VOR der Analyse
5. **Primary Specification** – Die exakte statistische Methode
6. **Data Sources** – Herkunft mit API-URLs
7. **Planned Robustness Checks** – Vorab definierte Sensitivitätsanalysen

Dann wird der Plan **LOCKED**: `LOCKED – do not modify after commit`. Git-Timestamps beweisen, dass der Plan existierte, BEVOR die Daten analysiert wurden.

**apep_0134 (initial_plan.md):** Enthält vorab spezifizierte Spillover-Ringe ("Ring 1: Treated, Ring 2: Excluded donut, Ring 3: Control"), die exakte Inference-Strategie für nur 2 behandelte Units, und sogar die geplante MSPE-Ratio für Placebo-Tests.

**apep_0074 (initial_plan.md):** Definiert vorab, wie mit concurrent gun-policy changes umgegangen wird, welche Exposure-Codierung verwendet wird, und welche Subgruppen-Analysen (Alter, Geschlecht) geplant sind.

### Was BEATRIX daraus lernt
**Anwendung: Strukturierte Analyse-Templates für FehrAdvice-Projekte**

Für jedes Beratungsprojekt, das auf empirischer Evidenz basiert, sollte BEATRIX ein Pre-Commitment-Template generieren:

1. **Fragestellung** – Was genau wollen wir wissen?
2. **Kontext-Hypothese** – Was erwarten wir aufgrund von BCM/Ψ-Dimensionen?
3. **Methode** – Wie evaluieren wir die Intervention?
4. **Vorab definierte Erfolgskriterien** – Wann gilt die Intervention als wirksam?
5. **Planned Checks** – Welche Alternativerklärungen prüfen wir?

Der Punkt ist nicht, dass FehrAdvice akademische Papers schreibt. Der Punkt ist: **Pre-Commitment verhindert retrospektives Rationalisieren.** Wenn eine Nudge-Intervention getestet wird, muss vorher festgelegt sein, was "Erfolg" bedeutet – nicht nachher.

**Konkreter BEATRIX-Feature:** `POST /api/projects/{id}/pre-commitment` – generiert ein gelocktes Analyse-Template, das auf GitHub mit Timestamp gepusht wird. Unmanipulierbar.

---

## Lernfeld 3: Adversarial Quality Control durch Disagreement

### Was APE macht
Das vielleicht eleganteste Feature von APE: **Die Reviewer sind sich nie einig.** Und das ist Absicht.

**apep_0170** (Salary Transparency):
| Reviewer | Verdict |
|----------|---------|
| Claude Code (intern) | MINOR REVISION |
| GPT-5-mini | MAJOR REVISION |
| Grok-4.1-Fast | MAJOR REVISION |
| Gemini-3-Flash | REJECT AND RESUBMIT |

**apep_0074** (Red Flag Laws):
| Reviewer | Verdict |
|----------|---------|
| Claude Code (intern) | REJECT AND RESUBMIT |
| GPT-5-mini | MAJOR REVISION |

Wenn alle Reviewer "ACCEPT" sagen, ist das Paper entweder perfekt oder die Reviewer sind zu milde. APE nutzt die **Disagreements produktiv**: Der Revision Plan priorisiert Issues nach Konsens ("alle drei Reviewer kritisieren X" = HIGH PRIORITY) vs. Einzelmeinung ("nur Gemini findet Y problematisch" = LOW PRIORITY).

**apep_0134 Revision Plan – Priorisierung:**
```
HIGH: Missing citations (alle Reviewer)
MEDIUM: Synthetic DiD discussion (Gemini)
MEDIUM: SCM Weights Table (Grok)
LOW: TWFE Limitations (nur GPT)
```

**apep_0170 Revision Plan:**
```
HIGH PRIORITY (Feasible within this revision)
MEDIUM PRIORITY (Acknowledged but requiring more data/time)
LOW PRIORITY (Future work / beyond scope)
```

### Was BEATRIX daraus lernt
**Anwendung: Multi-Perspektiven-Bewertung für FehrAdvice-Deliverables**

Statt EINEN Claude-Call zu machen, der ein Dokument analysiert, sollte BEATRIX **3 Perspektiven** generieren:

1. **Analytical Perspective** (streng methodisch): Sind die Behauptungen durch Daten gedeckt?
2. **Practical Perspective** (anwendungsorientiert): Kann der Kunde das umsetzen?
3. **Devil's Advocate** (bewusst kritisch): Was könnte schiefgehen?

Dann: Disagreement-Analyse. Wo stimmen alle 3 überein? → Hohes Vertrauen. Wo widersprechen sie sich? → Manuelles Review nötig.

**Für den BEATRIX Review-Endpoint:** Aktuell ist BEATRIX ein einzelner Reviewer. Phase 2 könnte sein: `POST /api/documents/{id}/multi-review` mit 3 unterschiedlichen System-Prompts (BCM-fokussiert, Methodik-fokussiert, Praxis-fokussiert), die unabhängig voneinander reviewen. Die Synthese wird automatisch erstellt.

---

## Lernfeld 4: Integrity-Scanning als Standard-Prozess

### Was APE macht
Jedes APE Paper wird einem automatischen Integrity Scan unterzogen – von **GPT-5.2**, das sowohl den LaTeX-Text als auch den R-Code liest und prüft, ob Text und Code konsistent sind.

**Die 6 Flag-Kategorien (mit Häufigkeit über 5 Papers):**

| Flag | Häufigkeit | Severity |
|------|------------|----------|
| HARD_CODED_RESULTS | In 4 von 5 Papers | HIGH |
| METHODOLOGY_MISMATCH | In 5 von 5 Papers | HIGH/MEDIUM |
| DATA_PROVENANCE_MISSING | In 4 von 5 Papers | MEDIUM |
| SELECTIVE_REPORTING | In 1 von 5 Papers | MEDIUM |
| SUSPICIOUS_TRANSFORMS | In 1 von 5 Papers | MEDIUM |

**Das überraschende Ergebnis:** 4 von 5 analysierten Papers werden als **SUSPICIOUS** eingestuft. Nicht weil sie betrügerisch sind, sondern weil es systematische Probleme gibt:

1. **HARD_CODED_RESULTS** ist das häufigste Problem: Tabellen und Figures im LaTeX werden manuell eingefügt statt automatisch aus dem Code generiert. Das ist bei AI-generierten Papers besonders problematisch, weil das Modell die "erwarteten" Ergebnisse in den Text schreiben kann, bevor der Code sie tatsächlich produziert.

2. **METHODOLOGY_MISMATCH** zeigt Inkonsistenzen zwischen Text-Beschreibung und Code-Implementation:
   - apep_0053: "The manuscript states AVR treatment is coded as in effect by the November CPS survey" – aber der Code macht etwas anderes
   - apep_0074: "Table 3 hard-codes sample sizes" die nicht mit dem Code-Output übereinstimmen

3. **DATA_PROVENANCE_MISSING**: Daten werden aus lokalen CSVs geladen, ohne dass der Pfad vom Fetch-Script zum Analyse-Script nachvollziehbar ist.

### Was BEATRIX daraus lernt
**Anwendung: Claim-Verification für FehrAdvice Reports**

FehrAdvice-Reports enthalten regelmässig empirische Claims: "67% der Kunden bevorzugen Option A" oder "die Intervention führte zu einer 23% Steigerung." Aktuell gibt es keinen systematischen Check, ob diese Zahlen:
- Konsistent durch das Dokument verwendet werden
- Einer nachvollziehbaren Quelle entspringen
- Mit den richtigen Einheiten/Kontexten angegeben sind

**BEATRIX Integrity Check für Reports:**
1. **Claim-Extraktion:** Alle quantitativen Aussagen automatisch identifizieren
2. **Konsistenz-Check:** Wird dieselbe Zahl überall gleich verwendet? (Abstract sagt 23%, Discussion sagt 25%?)
3. **Quellen-Check:** Ist eine Quelle angegeben? Ist sie nachvollziehbar?
4. **Kontext-Check:** Werden Effektgrössen im richtigen Kontext interpretiert? (Relative vs. absolute Risikoreduktion)

Das muss nicht perfekt sein. APE zeigt: Selbst ein imperfekter automatischer Scan findet in 80% der Fälle echte Probleme. Der Wert liegt im systematischen Prüfen, nicht in der Perfektion.

---

## Lernfeld 5: Reply-to-Reviewers als Wissens-Destillation

### Was APE macht
Der vielleicht unterschätzteste Teil des APE-Systems ist der `reply_to_reviewers_1.md`. Das ist nicht einfach eine Pflichtübung – es ist ein **Wissens-Destillations-Prozess**:

**Struktur (konsistent über alle Papers):**
1. Reviewer-Concern wird wörtlich zitiert
2. Response adressiert den Kern (nicht die Oberfläche)
3. Entweder: Änderung implementiert + wo im Paper
4. Oder: Begründung, warum nicht geändert (mit Referenz)

**apep_0134 – Beispiel für brillante Nicht-Änderung:**
> **Reviewer (GPT-5-mini):** "Report 95% confidence intervals for main SCM treatment effects"
>
> **Response:** "We report randomization inference p-values following Abadie et al. (2010), which provide valid finite-sample inference for SCM with few treated units. Conventional confidence intervals assume large-sample asymptotics inappropriate for N=2 treated neighborhoods."

Das ist keine Verteidigung – es ist eine **Lehr-Erklärung**. Der Reviewer lernt etwas. Und das Response-Dokument wird selbst zu einer wertvollen Ressource.

**apep_0074 – Ehrliches Eingestehen:**
> **Reviewer:** "Too few treated clusters (3 states)"
>
> **Response:** "Agreed. The main specification uses only Indiana (2006), California (2016), and Washington (2017)."
>
> **Reviewer:** "Need randomization inference or wild cluster bootstrap"
>
> **Response:** "Acknowledged as a limitation. Given data constraints, we cannot implement these approaches."

Bemerkenswert: Das System verteidigt nicht blind. Es gesteht echte Schwächen ein – und genau das macht die Reply glaubwürdig.

**apep_0170 Revision Plan – Triage:**
```
HIGH PRIORITY (Feasible within this revision):
  → Unweighted ACS percentiles discussion
  → Job-changer proxy limitation  
  → Top-coding discussion
  
MEDIUM PRIORITY (Acknowledged but requiring more data/time):
  → Monthly earnings data (not available in ACS)
  → Alternative wage measures

LOW PRIORITY (Future work / beyond scope):
  → Full structural model
```

### Was BEATRIX daraus lernt
**Anwendung 1: Automatische "Response to Feedback" für FehrAdvice Proposals**

Wenn ein Kunde Feedback zu einem FehrAdvice-Proposal gibt, generiert BEATRIX automatisch ein strukturiertes Response-Dokument:

- **Feedback-Punkt** → **Response** → **Änderung im Dokument (oder Begründung warum nicht)**
- Priorisierung: Was ist substanziell (HIGH) vs. kosmetisch (LOW)?
- Dokumentation: Welche Änderungen wurden wo im Dokument vorgenommen?

**Anwendung 2: Wissens-Destillation aus Kritik**

Jede kritische Frage zu einem BEATRIX-KB-Dokument wird gespeichert und beantwortet. Über Zeit entsteht ein **FAQ pro Paper**:
- "Warum ist diese Studie mit N=200 trotzdem relevant?" → Antwort mit Power-Analyse
- "Gilt das auch in Europa?" → Antwort mit Kontextfaktoren
- "Was sagt die Gegenposition?" → Antwort mit alternativen Interpretationen

Diese Q&A-Paare werden selbst zu KB-Einträgen und verbessern die RAG-Qualität.

**Anwendung 3: Peer-Review-Simulation für interne Dokumente**

Bevor ein FehrAdvice-Report zum Kunden geht:
1. BEATRIX generiert 3 simulierte Reviewer-Kritiken (methodisch, praktisch, skeptisch)
2. BEATRIX generiert einen automatischen Reply-to-Reviewers
3. Der Reply identifiziert die **echten Schwächen** des Dokuments
4. Das Team kann entscheiden, welche Schwächen vorab adressiert werden

---

## Zusammenfassung: Die 5 Lernfelder als BEATRIX-Roadmap

| # | Lernfeld | APE-Mechanismus | BEATRIX-Adaptation | Priority |
|---|----------|-----------------|---------------------|----------|
| 1 | **Ideen töten** | 4-6 Ideas → Score → Kill 75% | Paper-Triage mit PURSUE/CONSIDER/SKIP + Conditions | Phase 2 |
| 2 | **Pre-Commitment** | Locked Research Plan vor Analyse | Gelocktes Analyse-Template für Projekte | Phase 3 |
| 3 | **Adversarial QC** | 4 Reviewer widersprechen sich → Priorisierung | Multi-Perspektiven-Review (3 Prompts) | Phase 2 |
| 4 | **Integrity Scanning** | Code vs. Text Konsistenz-Check | Claim-Verification für Reports | Phase 2 |
| 5 | **Reply-to-Reviewers** | Strukturierte Wissens-Destillation aus Kritik | Feedback-Response + FAQ pro Paper + Peer-Review-Sim | Phase 3 |

### Das übergeordnete Prinzip

Alle 5 Lernfelder teilen eine Grundidee: **Qualität entsteht durch systematischen Widerspruch, nicht durch Zustimmung.** 

APE ist nicht gut, weil Claude Opus gute Papers schreibt. APE ist gut, weil GPT-5.2 schlechte Ideen tötet, 4 Reviewer unabhängig kritisieren, ein Integrity Scanner Inkonsistenzen findet, und ein Revision-Prozess die Kritik in Verbesserungen destilliert.

Für BEATRIX heisst das: Die Wissensbasis wird nicht besser, indem wir mehr Papers hochladen. Sie wird besser, indem wir jedes Paper systematisch herausfordern.
