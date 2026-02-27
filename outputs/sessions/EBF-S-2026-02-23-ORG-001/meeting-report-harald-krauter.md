# Meeting-Report: Harald Kräuter & Astrid Zöchling (ORF)

**Datum:** 2026-02-23
**Ort:** [TBD]
**Teilnehmer FA:** Gerhard Fehr
**Teilnehmer ORF:** Harald Kräuter [Position TBD], Astrid Zöchling [Position TBD, erwähnt/anwesend]
**Meeting-ID:** MTG-2026-02-23-001
**Session-ID:** EBF-S-2026-02-23-ORG-001
**Status:** ✅ MEETING DURCHGEFÜHRT

---

## 1. Gesprächspartner

| Feld | Details |
|------|---------|
| **Name** | Harald Kräuter |
| **Organisation** | Österreichischer Rundfunk (ORF) |
| **Position** | [TBD] |
| **Person-ID** | PER-EXT-023 |
| **Weitere Beteiligte** | Astrid Zöchling (PER-EXT-024) — Value Stream Implementierung IT ↔ Nutzer |

---

## 2. Kontext

Der ORF hat in den letzten 24 Monaten hohe Investitionen in zahlreiche IT-Tools getätigt:
- Automatische Urlaubsabfrage
- Planungs-Tools
- AI-Tools (diverse)
- Weitere interne Workflow-Tools

Die **technologische Implementierung** ist erfolgreich abgeschlossen. Die grösste Herausforderung ist jedoch, dass diese Tools noch nicht im erforderlichen Ausmass genutzt werden, um die hohen Investitionen zu rechtfertigen. Es gibt einen «Leader-Anteil» von Early Adopters, aber die flächendeckende Nutzung fehlt.

**Astrid Zöchling** hat Value Streams zwischen den Nutzern und der IT implementiert, die sicherstellen sollen, dass die IT nur das realisiert, was der Nutzer wirklich braucht. Die Kernfrage dabei: **Weiss der Nutzer, was er braucht?**

**Verhaltensökonomische Einordnung:** Dies ist kein IT-Problem, sondern ein **Verhaltensproblem** — klassischer Technology Adoption Gap mit bekannten behavioral barriers (Status Quo Bias, Present Bias, Default Effect, Social Proof Gap).

---

## 3. Besprochene Themen

### Thema 1: IT Tool Adoption Gap — Diagnose

| Aspekt | Details |
|--------|---------|
| **Status** | ✅ Ausführlich besprochen |
| **EBF-Relevanz** | Hoch — 6 Verhaltensbarrieren identifiziert |

**6 identifizierte Barrieren (gewichtet nach Impact):**

| # | Barriere | Impact | Mechanismus |
|---|----------|--------|-------------|
| 1 | Status Quo Bias | 85% | "Mein alter Weg funktioniert ja" |
| 2 | Present Bias (β ≈ 0.65) | 72% | Lernkosten JETZT, Nutzen in 3 Wochen |
| 3 | Default Effect | 68% | Alter Workflow ist immer noch der Default |
| 4 | Social Proof Gap | 62% | Early Adopters sind unsichtbar |
| 5 | Identity Threat | 48% | "Ich bin Journalist, kein IT-Mensch" |
| 6 | Hassle Factor | 38% | Neues Login, andere Oberfläche |

**Adoption Curve Position:** Der ORF befindet sich am «Chasm» (Geoffrey Moore) — der Sprung von ~16% Early Adopters auf 50%+ Early Majority steht aus.

---

### Thema 2: Interventions-Baukasten «Einfach Näher»

| Aspekt | Details |
|--------|---------|
| **Status** | ✅ Vollständig entwickelt |
| **EBF-Relevanz** | Sehr hoch — bidirektionales Behavioral Design |

**Kernprinzip:** Bidirektionale Bewegung — IT bewegt sich Richtung Menschen UND Menschen bewegen sich Richtung IT-Tools.

#### Die 3 Brücken

| Brücke | Prinzip | Verhaltens-Mechanismus |
|--------|---------|----------------------|
| **BRÜCKE 1: SICHTBAR MACHEN** | Awareness + Feedback | Descriptive Norms, Loss Aversion |
| **BRÜCKE 2: EINFACH MACHEN** | Friction Reduction | Default Effect, Hassle Factor |
| **BRÜCKE 3: GEMEINSAM MACHEN** | Social Proof | Peer Effects, In-Group Motivation |

#### Interventionen pro Brücke

**BRÜCKE 1 — SICHTBAR MACHEN:**
- **S-1:** Nutzen zeigen, nicht Features (IT-Seite)
- **S-2:** Live-Dashboard «ORF Digital Puls» (IT-Seite)
- **S-3:** «Mein erster Erfolg» — 90-Sekunden Soforterlebnis (Menschen-Seite)
- **S-4:** Persönlicher Zeit-Tracker mit Feedback (Menschen-Seite)

**BRÜCKE 2 — EINFACH MACHEN:**
- **E-1:** Dreiklick-Test — jede Kernfunktion in ≤3 Klicks (IT-Seite)
- **E-2:** Alte Wege abschalten — 3-Phasen Sanfter Zwang (IT-Seite)
- **E-3:** Workflow-First Design + Workflow Shadowing (IT-Seite)
- **E-4:** «Ein Tool pro Monat» — sequentielles Onboarding (Menschen-Seite)

**BRÜCKE 3 — GEMEINSAM MACHEN:**
- **G-1:** «Sprechstunde» statt Helpdesk — IT sitzt in der Abteilung (IT-Seite)
- **G-2:** Peer Champions — «Digital-Kolleg:innen» pro Abteilung (Menschen-Seite)
- **G-3:** «Vorher/Nachher» — 60-Sekunden Erfolgsgeschichten-Videos (Menschen-Seite)
- **G-4:** Team-Challenges (nicht individuell!) — Abteilungswettbewerb (Menschen-Seite)

#### 5 Sofort-Interventionen (priorisiert)

| ID | Intervention | Impact | Zeitrahmen |
|----|-------------|--------|------------|
| **I-1** | Default umkehren (alte Systeme abschalten) | SEHR HOCH | Woche 1-2 |
| **I-2** | Peer Champions pro Abteilung | HOCH | Woche 2-4 |
| **I-3** | Sichtbarkeit schaffen (Dashboard) | MITTEL-HOCH | Woche 1 |
| **I-4** | Micro-Onboarding statt Schulung | MITTEL | Woche 2-3 |
| **I-5** | Führungskräfte als Signal | MITTEL | Sofort |

#### Fahrplan

| Zeitraum | Massnahmen | Erwartete Adoption |
|----------|-----------|-------------------|
| Woche 1-2 | Dashboard, Dreiklick-Audit, Champions identifizieren, Deadline kommunizieren | 35% |
| Woche 3-4 | Tool 1 Rollout (90s-Onboarding), IT-Sprechstunde, Erfolgsgeschichten | 35% |
| Woche 5-8 | Phase 2 (Hinweis alter Weg), Team-Challenge, Workflow Shadowing | 55% |
| Woche 9-12 | Phase 3 (alter Weg AUS), Tool 2 Rollout, Champion-Netzwerk etabliert | 75% |
| Monat 4+ | Tool 3 (AI), Continuous Feedback, Self-sustaining Community | 90% |

#### KPIs

| KPI | Ziel W4 | Ziel W8 | Ziel W12 |
|-----|---------|---------|----------|
| Adoption Rate (aktive User) | 35% | 55% | 75% |
| Regelmässige Nutzung (≥3×/Wo) | 20% | 40% | 60% |
| «Alter Weg»-Nutzung | 70% | 30% | <10% |
| Zufriedenheits-Score (1-10) | 5.5 | 7.0 | 7.5 |
| Gesparte Stunden/Woche (org.) | 200h | 600h | 1'200h |

---

### Thema 3: Value Streams verhaltensökonomisch aufrüsten

| Aspekt | Details |
|--------|---------|
| **Status** | ✅ Ausführlich besprochen |
| **Bezug** | Astrid Zöchlings Value Stream Implementierung |

**Kernproblem:** Value Streams setzen voraus, dass der Nutzer weiss, was er braucht. 4 wissenschaftlich dokumentierte Gründe, warum das nicht funktioniert:

| # | Phänomen | Quelle | Konsequenz |
|---|----------|--------|------------|
| 1 | Preference Construction | Slovic & Lichtenstein | Präferenzen werden im Moment konstruiert, nicht abgerufen |
| 2 | Status Quo Anchoring | Kahneman & Tversky | Nutzer können nur inkrementelle Verbesserungen vorstellen |
| 3 | Empathy Gap | Loewenstein | Im Workshop (kalt) kann man Bedürfnisse unter Stress (heiss) nicht vorhersagen |
| 4 | Say-Do Gap | — | Was Menschen sagen ≠ was sie nutzen |

**4 Fixes für den Value Stream:**

| Fix | Prinzip | Konkret |
|-----|---------|---------|
| **FIX 1: BEOBACHTE statt FRAGE** | Workflow Shadowing (4h/Abteilung) | IT beobachtet echtes Arbeitsverhalten statt Anforderungen abzufragen |
| **FIX 2: ZEIGE statt BESCHREIBE** | Klickbarer Prototyp vor Code | Recognition > Recall — Nutzer kann erkennen, nicht generieren |
| **FIX 3: TESTE statt SPEZIFIZIERE** | 5-Personen-Test (Nielsen) | 5 echte Nutzer:innen finden 85% aller Probleme |
| **FIX 4: SCHLIESSE den Feedback Loop** | Adoption als Erfolgskriterium | Nicht "Feature delivered" sondern "Adoption ≥70%" |

**Zentrale Erkenntnis:**
> Der Nutzer kann nicht sagen, was er will. Aber er kann sofort sagen: «Das ist es» oder «Das ist es nicht.» → Weg vom GENERIEREN zum AUSWÄHLEN.

**Neues Erfolgskriterium für Value Streams:**
- ALT: Erfolg = Feature delivered on time
- NEU: Erfolg = Adoption Rate ≥ 70% nach 30 Tagen

---

### Thema 4: SRG-Halbierungsinitiative (Exkurs)

| Aspekt | Details |
|--------|---------|
| **Status** | Kurz präsentiert |
| **Referenz** | FCT-POL-2026-001 |

EBF-Prognose für die Abstimmung vom 8. März 2026:
- **NEIN: 52.1%** [95% CI: 43.5-60.7%]
- **P(NEIN gewinnt) = 62.4%**
- 2. SRG-Trendumfrage (gfs.bern) erwartet am 25. Februar
- Relevanz für ORF: Signalwirkung bei möglicher Annahme für europäische öffentlich-rechtliche Sender

---

## 4. Kernerkenntnisse

1. **Das ORF-Problem ist KEIN IT-Problem, sondern ein Verhaltensproblem.** Die Technologie funktioniert — das Verhalten hat sich nicht geändert.

2. **Der grösste Einzelhebel ist das Abschalten alter Wege.** Solange der alte Workflow existiert, ist er der Weg des geringsten Widerstands (Default Effect).

3. **Das Programm muss bidirektional sein.** Nur Nutzer zu nudgen reicht nicht — IT muss sich ebenfalls bewegen (Workflow-First Design, Dreiklick-Test).

4. **Value Streams brauchen eine verhaltensökonomische Schicht.** Die Annahme «der Nutzer weiss was er braucht» ist empirisch falsch. Lösung: Prototypen zeigen statt Anforderungen abfragen.

5. **Programm «Einfach Näher» mit 3 Brücken ist intuitiv, messbar und sofort umsetzbar.** SICHTBAR — EINFACH — GEMEINSAM.

---

## 5. Verknüpfte EBF-Analysen

| Session-ID | Thema | Präsentiert |
|-----------|-------|-------------|
| EBF-S-2026-02-23-ORG-001 | ORF IT Tool Adoption & «Einfach Näher» Program | ✅ |
| EBF-S-2026-01-30-POL-003 | SRG-Halbierungsinitiative Forecast | ✅ (Kurzversion) |

---

## 6. Follow-up Aktionen

| # | Aktion | Typ | Deadline | Owner | Status |
|---|--------|-----|----------|-------|--------|
| FU-ORF-001 | Meeting-Report und «Einfach Näher» Programm-Dokument zusenden | Dokument | 28.02.2026 | GF | 🔴 Offen |
| FU-ORF-002 | Segment-Analyse vertiefen (welche MA-Gruppen brauchen welche Intervention) | Analyse | 07.03.2026 | FA | ⏳ Offen |
| FU-ORF-003 | Offerte/Proposal für «Einfach Näher» Implementierung erstellen | Offerte | 14.03.2026 | FA | ⏳ Offen |
| FU-ORF-004 | Folgetermin mit Harald Kräuter + Astrid Zöchling vereinbaren | Meeting | 07.03.2026 | GF | 🔴 Offen |

---

## 7. Meeting-Notizen

### Gesprächsqualität: ⭐⭐⭐ Sehr gut

Tiefgehende, inhaltlich reiche Diskussion über drei Kernthemenblöcke. Harald Kräuter beschreibt die Herausforderung präzise: «Die technologische Implementierung ist erfolgreich erfolgt — die grösste Herausforderung ist jedoch, dass diese Tools noch nicht in dem Ausmass verwendet werden, dass die hohen Investitionen gerechtfertigt sind.»

### Zentrale Zitate / Beobachtungen

- **Zur Ausgangslage:** «In den letzten 24 Monaten wurden hohe Investitionen in zahlreiche IT-Tools getätigt [...] neue mögliche Workflows sind nicht implementiert, und die Tools werden daher unterbenutzt.»

- **Zu Astrid Zöchlings Value Streams:** «Die Frage ist — weiss der Nutzer, was er braucht? Und wie stellt man sicher, dass dies End-to-End so kommunizierbar ist, dass der Nutzer auch klar weiss und sieht, was er bestellt?»

- **Zum gewünschten Programm:** «Am Ende sollte ein generelles Programm entstehen, dass die IT näher an die Menschen, und die Menschen näher an die Usage der IT-Tools bringt, und dieses Programm ist einfach und intuitiv verständlich, komplexitätsreduzierend, aber sehr durchdacht, um das Verhalten der User, aber auch der IT in die richtige Richtung zu nudgen.»

### Verhaltensökonomische Modelle angewendet

| Modell/Theorie | Anwendung |
|----------------|-----------|
| Rogers Diffusion of Innovation | Adoption Curve Position (Chasm) |
| Geoffrey Moore Crossing the Chasm | Sprung von 16% → 50% |
| Kahneman & Tversky Status Quo Bias | Barriere #1: "Alter Weg funktioniert" |
| Loewenstein Hot-Cold Empathy Gap | Value Stream Problem: Workshop ≠ Realität |
| Slovic Preference Construction | Nutzer konstruiert Bedürfnisse, hat sie nicht |
| Nielsen 5-User Rule | Prototyp-Testing mit 5 Personen = 85% der Probleme |
| Thaler & Sunstein Default Effect | Grösster Hebel: Alten Weg abschalten |

---

## 8. Strategische Optionen

| Option | Beschreibung | Aufwand | Impact |
|--------|-------------|---------|--------|
| **A: Quick Win** | Sofort-Interventionen I-1 bis I-5 (Woche 1-4), internes ORF-Team setzt um | Gering (Beratung) | Mittel-Hoch |
| **B: Begleitetes Programm** | FehrAdvice begleitet «Einfach Näher» über 12 Wochen mit Behavioral Design | Mittel (Projekt) | Hoch |
| **C: Vollständige Transformation** | Programm + Value Stream Redesign + Segment-Analyse + KPI-System | Hoch (Mandat) | Sehr Hoch |

---

*Erstellt: 2026-02-23 | Meeting-ID: MTG-2026-02-23-001 | Session-ID: EBF-S-2026-02-23-ORG-001*
*Template: TPL-MTG-001 (Vollständig) | Version: 1.0*
