# UBS Mortgage Custom GPT — Finales Survey-Instrument

> **Evidenzbasiert aus 11 Pre-Analysen:** A1-A3, B1-B3, G1-G4
> **Datum:** 2026-02-25 | **Version:** 1.0
> **Hypothesen:** H_M01–H_M12 (siehe G4)
> **Stichprobe:** n = 300 (2x2 Design, 75 pro Zelle)

---

## Executive Summary

Dieses Survey-Instrument misst die Akzeptanz eines KI-gestützten Hypothekar-Zinsrechners auf UBS-Kanälen. Das Design integriert drei theoretische Säulen:

1. **Algorithm Aversion/Appreciation** (B1): Dietvorst 2015/2018, Castelo 2019, Longoni 2019
2. **Trust-UTAUT2** (B2): Venkatesh 2012, Gefen 2003, Kim 2009
3. **Trust-Kaskade** (A2): 6-Schicht-Vertrauensdekomposition (tau_final = 0.142–0.285)

**Erwartetes Modell:** Trust-UTAUT2 + Algorithm Aversion, R² = 0.62–0.68

**Kritischste Design-Entscheidung:** Modifizierbarkeit der KI-Ausgabe. Dietvorst (2018) zeigt +41 Prozentpunkte Nutzung wenn Nutzer Parameter anpassen können (32% → 73%).

---

## Experimentelles Design

**Typ:** 2x2 Between-Subjects

| | **Modifizierbar** | **Fixe Ausgabe** |
|---|---|---|
| **KI offengelegt** | Zelle 1 (n=75) — Optimale Zelle | Zelle 2 (n=75) — Höchste Aversion |
| **KI nicht offengelegt** | Zelle 3 (n=75) | Zelle 4 (n=75) — Kontrollgruppe |

**Faktor 1 — KI-Offenlegung:** Variiert ob «berechnet von KI» sichtbar ist
**Faktor 2 — Modifizierbarkeit:** Variiert ob Nutzer Parameter anpassen können

**Erwartete Zellmittelwerte (Q_M06 auf 7-Punkt-Skala):**
- Zelle 1 (offengelegt + modifizierbar): M = 5.8
- Zelle 2 (offengelegt + fix): M = 3.9
- Zelle 3 (nicht offengelegt + modifizierbar): M = 5.2
- Zelle 4 (nicht offengelegt + fix): M = 4.5

**Haupteffekt Modifizierbarkeit:** Cohen's d = 0.60 (gross)
**Interaktionseffekt:** β = +0.15 (Synergie: offengelegt + modifizierbar = bestes Ergebnis)

---

## Block A: Kanal und Kontext (3 Fragen)

### Q_M01 — Kanalidentifikation

**Fragetext:**
> **DE:** Wie sind Sie auf diesen Service aufmerksam geworden?
> **EN:** How did you become aware of this service?

**Format:** Single Choice
**Antwortoptionen:**
1. UBS Website
2. UBS Mobile Banking App
3. ChatGPT Marketplace
4. Homegate / ImmoScout24
5. Social Media (Instagram, LinkedIn, etc.)
6. Empfehlung (Berater, Freunde, Familie)
7. Andere

**Theoretische Begründung:**
Ohne Kanal-Zuordnung ist die Datenanalyse wertlos. Die Ψ-Kontexte variieren um Faktor 2–3 zwischen Kanälen. Die Trust-Kaskade (A2) zeigt:
- Website: tau_final = 0.228
- Marketplace: tau_final = 0.142
- Partner (Homegate): tau_final = 0.170

Der Kanal determiniert den gesamten Vertrauenskontext und damit die Basisakzeptanz.

**Analyse:** Moderator-Variable für alle Haupteffekt-Hypothesen. Kanal-spezifische Subgruppen-Analysen.

**Erwartete Verteilung:** Website 35%, App 25%, Marketplace 15%, Partner 15%, Social 5%, Empfehlung 5%

---

### Q_M02 — Kaufphase / Segmentzuordnung

**Fragetext:**
> **DE:** Wo stehen Sie aktuell bei Ihrem Hypothekar-Vorhaben?
> **EN:** Where are you currently in your mortgage journey?

**Format:** Single Choice
**Antwortoptionen:**
1. Ich habe ein konkretes Objekt im Blick
2. Ich suche aktiv nach einer Immobilie
3. Ich informiere mich allgemein über Hypotheken
4. Ich möchte eine bestehende Hypothek refinanzieren

**Theoretische Begründung:**
A1 identifiziert 4 Segmente mit unterschiedlichen 10C-Profilen:
- **Erstkäufer** (40% TAM): AWARE = 0.20, READY_W = 0.70 — hoher Intent, tiefes Wissen
- **Refinanzierer** (30%): AWARE = 0.75, READY_W = 0.40 — hohes Wissen, moderater Intent
- **Erben** (10%): AWARE = 0.15, READY_W = 0.50 — geringstes Wissen, emotionaler Kontext
- **Informationssuchende** (20%): AWARE = 0.50, READY_W = 0.25 — kein konkreter Intent

Jedes Segment benötigt einen anderen GPT-Dialogfluss. Erstkäufer brauchen Erklärung, Refinanzierer wollen Vergleich, Informationssuchende explorieren.

**Analyse:** Segment-Zuordnung für Subgruppen-Analysen. Life Transition Multiplier = 1.5 für Segmente 1–2.

**Erwartete Verteilung:** Option 1: 20%, Option 2: 20%, Option 3: 35%, Option 4: 25%

---

### Q_M03 — Hypothekar-Wissen

**Fragetext:**
> **DE:** Wie vertraut sind Sie mit Hypothekenfinanzierung?
> **EN:** How familiar are you with mortgage financing?

**Format:** 5-Punkt-Likert
**Anker:** 1 = Gar nicht vertraut — 5 = Sehr vertraut

**Theoretische Begründung:**
Domain-Wissen moderiert Algorithm Appreciation (Logg 2019): Bei objektiven Aufgaben mit hohem eigenem Wissen steigt die KI-Wertschätzung. A1 zeigt AWARE-Werte von 0.20 (Erstkäufer) bis 0.75 (Refinanzierer). Dieses Item validiert die Selbsteinschätzung gegen die Segmentzuordnung aus Q_M02.

**Analyse:** Moderator für H_M05 (Objectivity × Aversion). Erwartete Interaktion: Knowledge × Objectivity → Aversion ↓

**Erwarteter Mittelwert:** M = 3.2 (leicht unter Mitte; viele Erstinteressierte)

---

## Block B: KI-Wahrnehmung und Algorithm Aversion (4 Fragen)

### Q_M04 — KI-Transparenz (Experimentelle Manipulation Check)

**Fragetext:**
> **DE:** Wissen Sie, dass die Zinsindikation von einem KI-System berechnet wird?
> **EN:** Are you aware that the rate indication is calculated by an AI system?

**Format:** Binär (Ja / Nein)

**Theoretische Begründung:**
Manipulation Check für Faktor 1 des 2x2-Designs. In Zellen 1–2 (offengelegt) muss >90% «Ja» antworten. In Zellen 3–4 (nicht offengelegt) erwartet man 20–40% «Ja» (manche erkennen KI trotzdem). Dietvorst (2015): Transparenz triggert Scrutiny, was nach Fehlern zu dauerhafter Aversion führt. Castelo & Ward (2019): Bei objektiven Aufgaben führt Disclosure aber zu Appreciation statt Aversion.

**Analyse:** Chi-Quadrat-Test zwischen Experimentalgruppen. Manipulation gilt als erfolgreich wenn Zelle 1/2 vs. 3/4 signifikant unterschiedlich (p < .001).

**Schweizer Kontext (G2):** 75% der Schweizer fordern AI-Labeling → Offenlegung wird wahrscheinlich regulatorisch obligatorisch. Ergebnis informiert Framing-Strategie.

---

### Q_M05 — Transparenz-Präferenz

**Fragetext:**
> **DE:** Wie wichtig ist es Ihnen zu wissen, ob ein Mensch oder eine KI antwortet?
> **EN:** How important is it for you to know whether a human or AI is responding?

**Format:** 7-Punkt-Likert
**Anker:** 1 = Überhaupt nicht wichtig — 7 = Sehr wichtig

**Theoretische Begründung:**
Misst die Grundhaltung zur KI-Transparenz. Hohe Werte (>5) korrelieren mit höherem Aversionsrisiko (Dietvorst 2015: d = 0.85). G2 zeigt den Schweizer AI-Paradox: 45% nutzen GenAI täglich, aber 58% fürchten Datenmissbrauch. Diese Ambivalenz wird hier gemessen.

**Analyse:** Prädiktor für H_M03 (Aversion → BI). Erwartung: Korrelation r = 0.45 mit Algorithm Aversion Scale.

**Erwarteter Mittelwert:** M = 5.2 (über Mitte — Schweizer schätzen Transparenz hoch)

---

### Q_M06 — KI-Nutzungsbereitschaft (Primäre AV)

**Fragetext:**
> **DE:** Würden Sie eine KI-generierte Zinsindikation als Entscheidungsgrundlage nutzen?
> **EN:** Would you use an AI-generated rate indication as a basis for your decision?

**Format:** 7-Punkt-Likert
**Anker:** 1 = Auf keinen Fall — 7 = Auf jeden Fall

**Theoretische Begründung:**
Dies ist die **primäre abhängige Variable** des Experiments. Der erwartete Mittelwert variiert nach experimenteller Bedingung:
- Mit Modifizierbarkeit: M = 5.1–5.8 (Dietvorst 2018: 73% Nutzung)
- Ohne Modifizierbarkeit: M = 3.9–4.5 (Dietvorst 2018: 32% Nutzung)

Drei Parameter bestimmen den Wert:
- alpha_aversion = 0.68 (68% zeigen Basisaversion, B1)
- beta_modification = 0.41 (Modifizierbarkeit hebt +41pp, B1)
- gamma_objectivity = 0.38 (Objektives Framing verschiebt zu Appreciation, B1)

**Analyse:** Primäre DV für 2x2 ANOVA + SEM. Testet H_M03, H_M04, H_M09, H_M10.

**Power:** f = 0.25 (mittlerer Effekt), α = .05, Power = .90 → n = 260 (65/Zelle)

**Erwarteter Mittelwert:** M = 4.1–5.1 (Gesamtstichprobe; über Mitte dank Objektvitäts-Bonus, aber unter 6 wegen High-Stakes-Penalty)

---

### Q_M07 — Modifizierbarkeits-Präferenz (Kritischste Design-Frage)

**Fragetext:**
> **DE:** Wäre es für Sie wichtig, Parameter (z.B. Risikobereitschaft, Laufzeit) selbst anpassen zu können?
> **EN:** Would it be important for you to adjust parameters (e.g., risk tolerance, term) yourself?

**Format:** 7-Punkt-Likert
**Anker:** 1 = Überhaupt nicht wichtig — 7 = Sehr wichtig

**Theoretische Begründung:**
**DER grösste einzelne Design-Hebel** im gesamten Survey. Dietvorst (2018) zeigt: Modifizierbarkeit steigert Algorithmus-Nutzung um 41 Prozentpunkte (Cohen's h = 0.85 — ein enormer Effekt). B1 zeigt, dass delta_AI in der Trust-Kaskade von 0.31 (fix) auf 0.72 (modifizierbar) springt.

Dies ist gleichzeitig der **Manipulation Check für Faktor 2** des Experiments. In Zellen 1/3 (modifizierbar) erleben Nutzer die Anpassungsmöglichkeit; in Zellen 2/4 (fix) nicht.

**Analyse:** Manipulation Check + SEM-Pfad für H_M04. Testet auch, ob Modifizierbarkeits-WUNSCH (diese Frage) mit tatsächlicher Modifizierbarkeits-NUTZUNG (experimentell) interagiert.

**Erwarteter Mittelwert:** M = 5.5–6.0 (starke Präferenz erwartet). Werte über 5.5 bestätigen, dass Modifizierbarkeit ein «Must-Have» ist.

---

## Block C: Vertrauen und Performance (4 Fragen)

### Q_M08 — Institutionelles Vertrauen (UBS)

**Fragetext:**
> **DE:** Wie sehr vertrauen Sie UBS bei der Berechnung einer Hypothekar-Zinsindikation?
> **EN:** How much do you trust UBS to calculate a mortgage rate indication?

**Format:** 7-Punkt-Likert
**Anker:** 1 = Vertraue überhaupt nicht — 7 = Vertraue voll und ganz

**Theoretische Begründung:**
Trust ist der **dominante Prädiktor** (H_M01, β = 0.38). Die Trust-Kaskade (A2) zeigt 6 multiplikative Schichten:
- tau_institutional (UBS Brand) = 0.82
- tau_data (Privacy) = 0.68
- tau_AI (Algorithm) = 0.31–0.72 (je nach Modifizierbarkeit)
- tau_output (Accuracy) = 0.78
- tau_emotional (Comfort) = 0.75
- tau_social (Reputation) = 0.85

Total: tau_final = 0.142–0.285. Dieses Item misst die erste Schicht (tau_institutional). Kim (2009) zeigt für Mobile Banking: Trust (0.38) > PU (0.31) > PEOU (0.14).

**Analyse:** SEM-Pfad für H_M01. Auch Mediator-Test: Trust → PE → BI (indirekter Pfad β = 0.34 laut Gefen 2003).

**Erwarteter Mittelwert:** M = 5.0–5.5 (UBS-Markenvertrauen ist stark, aber KI-Komponente reduziert leicht)

---

### Q_M09 — Performance Expectancy (Nützlichkeit)

**Fragetext:**
> **DE:** Wie nützlich wäre eine sofortige, indikative Zinsberechnung für Ihre Hypothekarentscheidung?
> **EN:** How useful would an immediate, indicative rate calculation be for your mortgage decision?

**Format:** 7-Punkt-Likert
**Anker:** 1 = Überhaupt nicht nützlich — 7 = Äusserst nützlich

**Theoretische Begründung:**
PE ist der zweitstärkste Prädiktor (H_M02, β = 0.32). Davis (1989) TAM zeigt PU β = 0.42–0.66, aber im Kontext eines KI-basierten Finanztools wird ein Teil des PE-Effekts durch Trust mediiert (Gefen 2003). Der bereinigte direkte Effekt ist 0.32.

Die drei Nutzen-Dimensionen:
- **Geschwindigkeit:** Sofortige Indikation vs. 2–5 Tage Wartezeit (G3: kein Konkurrent bietet Echtzeit-KI)
- **Verfügbarkeit:** 24/7 vs. Berater-Termine
- **Vergleichbarkeit:** Instant-Benchmark vs. mühsame Einzelanfragen

**Analyse:** SEM-Pfad für H_M02. Erwartet: Stärkster Effekt bei Segment «Informationssuchende» (A1: niedriger Intent, hohe Explorations-Motivation).

**Erwarteter Mittelwert:** M = 5.5–6.0 (hoch — der funktionale Nutzen ist offensichtlich)

---

### Q_M10 — Effort Expectancy (Einfachheit)

**Fragetext:**
> **DE:** Wie einfach war die Nutzung des KI-Zinsrechners?
> **EN:** How easy was it to use the AI rate calculator?

**Format:** 7-Punkt-Likert
**Anker:** 1 = Sehr schwierig — 7 = Sehr einfach

**Hinweis:** Post-Usage-Frage. Erfordert GPT-Interaktion vor Beantwortung.

**Theoretische Begründung:**
EE ist ein Hygienefaktor (H_M08, β = 0.14). Conversational UI reduziert die Eintrittsbarriere natürlicherweise (chatten statt Formular ausfüllen). Kim (2009) zeigt für Mobile Banking: EE = 0.14 — wichtig, aber nicht differenzierend.

**Analyse:** SEM-Pfad für H_M08. Erwartet: Schwächster UTAUT-Prädiktor, aber Floor-Effekt bei Problemen (Score < 4 → sofortiger Abbruch).

**Erwarteter Mittelwert:** M = 5.0–5.5 (Conversational UI ist einfacher als Formulare, aber Finanzkomplexität erhöht wahrgenommenen Aufwand)

---

### Q_M11 — Wahrgenommenes Risiko

**Fragetext:**
> **DE:** Wie riskant empfinden Sie es, eine Hypothekarentscheidung auf Basis einer KI-Indikation zu treffen?
> **EN:** How risky do you perceive it to make a mortgage decision based on an AI indication?

**Format:** 7-Punkt-Likert
**Anker:** 1 = Überhaupt nicht riskant — 7 = Sehr riskant

**Theoretische Begründung:**
Perceived Risk ist eine Barriere (β = -0.28, Pavlou 2003). Hypothekarfinanzierung ist eine der grössten finanziellen Entscheidungen im Leben — Burton (2020) zeigt, dass Algorithm Aversion bei High-Stakes-Personal-Decisions am stärksten ist. G2 bestätigt: Schweizer sind risikobewusst (Tagesgeldsparquote >15%).

**Framing-Empfehlung:** Die Frage misst das WAHRGENOMMENE Risiko. Die GPT-Ausgabe sollte als «Indikation, nicht Entscheidung» positioniert werden, um die Risikowahrnehmung zu senken. Transparente Konfidenzintervalle («±0.15% vom finalen Angebot») können helfen.

**Analyse:** Kontrollvariable in SEM. Testet, ob Risk den Trust→BI-Pfad mediiert.

**Erwarteter Mittelwert:** M = 4.5–5.0 (über Mitte — High-Stakes-Kontext)

---

## Block D: Soziales und Personalisierung (2 Fragen)

### Q_M12 — Social Influence (Beraterempfehlung)

**Fragetext:**
> **DE:** Würde die Empfehlung Ihres UBS-Beraters Ihre Bereitschaft erhöhen, den KI-Zinsrechner zu nutzen?
> **EN:** Would your UBS advisor's recommendation increase your willingness to use the AI rate calculator?

**Format:** 7-Punkt-Likert
**Anker:** 1 = Überhaupt nicht — 7 = Sehr stark

**Theoretische Begründung:**
Social Influence (H_M07, β = 0.18) wird durch Alter moderiert (Venkatesh 2003): Stärker bei 45+ (traditionelle Affluent-Kunden). Dietvorst (2018) zeigt höchstes Vertrauen in Human-AI-Kombination. Die Berater-Empfehlung ist der primäre SI-Kanal im Hypothekarkontext.

**Analyse:** SEM-Pfad für H_M07. Moderation durch Alter: Erwartung β(SI) = 0.12 für <40, β(SI) = 0.26 für 45+.

**Erwarteter Mittelwert:** M = 4.5 (moderat; Beraterempfehlung ist wichtig, aber nicht entscheidend für digital-affine Segmente)

---

### Q_M13 — Wahrgenommene Personalisierung

**Fragetext:**
> **DE:** Wie gut hat der KI-Zinsrechner Ihre persönliche Situation berücksichtigt?
> **EN:** How well did the AI rate calculator consider your personal situation?

**Format:** 7-Punkt-Likert
**Anker:** 1 = Überhaupt nicht — 7 = Vollständig

**Hinweis:** Post-Usage-Frage. Erfordert GPT-Interaktion vor Beantwortung.

**Theoretische Begründung:**
**DESIGN-KRITISCH.** Longoni (2019) zeigt einen starken indirekten Uniqueness-Neglect-Effekt von -0.83 auf Anbieter-Wahl. Im BI-Kontext (H_M06) beträgt der skalierte Effekt -0.18. Wenn Nutzer das Gefühl haben, die KI behandle sie als «Durchschnitt», sinkt die Nutzungsbereitschaft drastisch.

**Gegenstrategien (aus B1, Priorität 3):**
- Input-Faktoren (Einkommen, LTV, Kanton, Laufzeit) sichtbar in der Berechnung zeigen
- Personalisierte Kommentare: «Basierend auf Ihrem Einkommen von CHF X und LTV von Y%...»
- Vergleich mit Durchschnitt: «Ihre Indikation liegt X% unter/über dem Durchschnitt für Ihren Kanton»

**Analyse:** Mediator in H_M06. Test: Uniqueness Neglect → Personalization ↓ → BI ↓ (PROCESS Model 4).

**Erwarteter Mittelwert:** M = 3.5–4.5 (RISIKO-ZONE — GPT kann generisch wirken). Werte unter 4.0 signalisieren dringenden Handlungsbedarf im GPT-Design.

---

## Block E: Handlungsabsicht und Follow-up (2 Fragen)

### Q_M14 — Behavioral Intention / Lead Conversion

**Fragetext:**
> **DE:** Wie wahrscheinlich ist es, dass Sie nach dieser Indikation einen Beratungstermin bei UBS vereinbaren?
> **EN:** How likely are you to schedule a consultation with UBS after this indication?

**Format:** 7-Punkt-Likert
**Anker:** 1 = Sehr unwahrscheinlich — 7 = Sehr wahrscheinlich

**Theoretische Begründung:**
Sekundäre AV und direkter Conversion-Indikator. A1 Journey Model schätzt C_GPT_to_RM Konversionsrate auf 8–15%. Auf der 7-Punkt-Skala bedeutet dies: ca. 8–15% scoren 6–7 (= konvertieren).

**Analyse:** Sekundäre DV für SEM. Pfad-Analyse: Trust/PE/Aversion → BI (Q_M06) → Conversion (Q_M14).

**Erwarteter Mittelwert:** M = 3.5–4.5 (unter Mitte — nicht jeder GPT-Nutzer will sofort einen Termin)

---

### Q_M15 — Human Handoff (Direkte Conversion-CTA)

**Fragetext:**
> **DE:** Möchten Sie diese Indikation mit einem Berater besprechen?
> **EN:** Would you like to discuss this indication with an advisor?

**Format:** Single Choice mit Abstufung
**Antwortoptionen:**
1. Ja, sofort Termin vereinbaren
2. Ja, aber später
3. Nein, die Indikation reicht mir
4. Nein, ich werde einen anderen Anbieter kontaktieren

**Theoretische Begründung:**
**DAS Lead-Generierungs-Element.** B1 zeigt: AI-Human-Komplementarität (γ_ai_human = 0.35) ist die optimale Positionierung. GPT als «Schritt 1 vor dem Berater» → höchste Gesamtakzeptanz (Dietvorst 2018). G3 bestätigt: Kein Konkurrent bietet diesen nahtlosen GPT→Berater-Handoff.

Option 4 ist ein Warnsignal: Zeigt aktive Abwanderung. Wenn >10% Option 4 wählen, besteht Aversions-induzierte Churn-Gefahr.

**Analyse:** Konversionsrate = (Option 1 + Option 2) / Total. Segmentiert nach Experimentalzelle. H_M12 Test: Vergleich BI zwischen Option 1+2 (GPT+Human) vs. Option 3 (GPT-only).

**Erwartete Verteilung:** Option 1: 8%, Option 2: 15%, Option 3: 65%, Option 4: 12%

---

## Zusammenfassung: Fragenfluss und Timing

```
SCREENING (30 Sek.)
  └─ Zielgruppenprüfung: Interesse an Hypothekarfinanzierung? eSIM-fähiges Gerät?

BLOCK A — Kontext (1 Min.)
  Q_M01 → Kanal
  Q_M02 → Kaufphase
  Q_M03 → Hypothekar-Wissen

RANDOMISIERUNG in 2x2-Zelle (System)

VIGNETTE / GPT-INTERAKTION (3-5 Min.)
  └─ Szenario: «Stellen Sie sich vor, Sie besuchen [Kanal] und sehen einen
     KI-Zinsrechner [mit/ohne KI-Label], der [anpassbare/fixe] Indikationen gibt.»

BLOCK B — KI-Wahrnehmung (2 Min.)
  Q_M04 → KI-Transparenz (Manipulation Check)
  Q_M05 → Transparenz-Präferenz
  Q_M06 → KI-Nutzungsbereitschaft ★ PRIMÄRE AV
  Q_M07 → Modifizierbarkeits-Präferenz

BLOCK C — Trust & Performance (2 Min.)
  Q_M08 → Institutionelles Vertrauen
  Q_M09 → Performance Expectancy
  Q_M10 → Effort Expectancy
  Q_M11 → Wahrgenommenes Risiko

BLOCK D — Soziales (1 Min.)
  Q_M12 → Beraterempfehlung
  Q_M13 → Personalisierung ★ DESIGN-KRITISCH

BLOCK E — Intention (1 Min.)
  Q_M14 → Beratungstermin-Intention
  Q_M15 → Human Handoff CTA ★ CONVERSION

DEMOGRAFIE (1 Min.)
  Alter, Geschlecht, Region (DE-CH/FR-CH/IT-CH), Einkommen, UBS-Kundenbeziehung

TOTAL: ~12-15 Minuten
```

---

## Analyse-Plan (Kurzfassung)

| Hypothese | Test | Primäre Variablen | Erwarteter Effekt |
|---|---|---|---|
| H_M01 | SEM-Pfad | Trust → BI | β = 0.38 |
| H_M02 | SEM-Pfad | PE → BI | β = 0.32 |
| H_M03 | SEM-Pfad | Aversion → BI | β = -0.25 |
| H_M04 | ANOVA + SEM | Modifizierbarkeit → Usage | Δ = 41pp |
| H_M05 | Moderation | Objectivity × Aversion | β_int = 0.38 |
| H_M06 | Mediation | Uniqueness → Personalization → BI | β_ind = -0.18 |
| H_M07 | Mod. Regression | SI × Age → BI | β = 0.18, mod +0.08/Dekade |
| H_M08 | SEM-Pfad | EE → BI | β = 0.14 |
| H_M09 | Mixed ANOVA | Disclosure → Trust (pre/post) | d_pre = -0.12, d_post = +0.08 |
| H_M10 | 2-way ANOVA | Disclosure × Modifiability | β_int = +0.15 |
| H_M11 | One-way ANOVA | Segment → Aversion | η² > 0.06 |
| H_M12 | t-Test | GPT+Human vs. GPT-only → BI | Δ = 0.35 |
