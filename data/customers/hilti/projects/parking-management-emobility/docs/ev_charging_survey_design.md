# EV Charging Survey Design — Hilti HQ (v3.1)

**Projekt:** PRJ-HILTI-001 (Parking Management E-Mobility)
**Modell:** MOD-HILTI-EVC-001 (Gated Logistic Repark Model)
**Version:** 3.1 (B3/B4/B5 Fixes nach Stakeholder-Review)
**Sprache:** Englisch
**Plattform:** Microsoft Forms
**Anonym:** Ja
**Zielgruppe:** Aktuelle EV-Fahrer am Hilti HQ Schaan (~400 Personen)
**Geschaetzte Dauer:** ~5 Minuten (12 Fragen)
**Erstellt:** 2026-02-20
**Update:** 2026-02-25

---

## Changelog v2.0 → v3.0

| Item | Aenderung | Grund |
|------|-----------|-------|
| **Alle** | 4 Antwortoptionen (statt 5) | Forced Choice — kein indifferenter Mittelwert |
| **A3** | Komplett neu: Scarcity-Erfahrung | Alte Version (Repark-Verhalten) hatte soziale Erwuenschtheit |
| **A4** | 2nd Order: «Warum haben andere umgeparkt?» | Umgeht Selbstschutz |
| **B1** | ENTFERNT | Redundant mit C2 |
| **B2** | 1st Order + unlikely/likely Skala | Direkter, ehrlicher |
| **B3** | Antwort A: «and complain» entfernt | Suggestiv |
| **B3b** | NEU: Kolleg:innen agree/complain bei Fee | Misst Akzeptanz-Erwartung |
| **B4** | Alle Pricing-Varianten (PPU, Flat, Time, Volume) | Vorher nur Fee vs. kein Fee |
| **B5** | Nur Non-Pricing: 3 Awareness-Nudges + Community | Problem ist primaer Awareness |
| **C1** | ENTFERNT | Survey zu lang |
| **C3** | ENTFERNT | Survey zu lang |
| **C4** | ENTFERNT | Survey zu lang |
| **C5** | ENTFERNT | Survey zu lang |

---

## Design-Philosophie

### Warum NICHT direkt nach Massnahmen fragen?

> Varianten V1-V5 vorstellen → «Welche akzeptierst du?» → KPIs abfragen

**Probleme:**

| # | Problem | Konsequenz |
|---|---------|------------|
| 1 | **Hypothetical Bias** | Leute koennen nicht zuverlaessig vorhersagen, wie sie auf ein nie erlebtes Preismodell reagieren |
| 2 | **Strategic Responding** | Rationale Antwort: «Ich bevorzuge das Guenstigste fuer mich» → alle waehlen Status Quo |
| 3 | **Abstraktionsproblem** | «0.15 CHF/kWh» — niemand hat eine Intuition fuer kWh-Preise als Verhaltensanreiz |
| 4 | **Framing/Reihenfolge-Effekt** | Erste Variante wird geankert, Formulierung beeinflusst Wahl |
| 5 | **Soziale Erwuenschtheit** | «Wuerden Sie umparken?» → «Ja natuerlich!» (inflationaere Akzeptanz) |

### Unser Ansatz (indirekt)

> Verhaltensparameter messen → Modell berechnet → welche Massnahme zahlt am meisten auf welchen KPI ein

```
WAS DIE LEUTE BEANTWORTEN:           WAS DAS MODELL BERECHNET:
─────────────────────────────         ────────────────────────────
Tatsaechliches Verhalten          →   Awareness-Level (A)
Was sie bei Kolleg:innen beobachten → Soziale Norm (σ)
Wie sie in konkreten Situationen  →   Aufwandskosten (τ) pro Segment
  reagiert haben
Was sie Kolleg:innen zutrauen     →   Preis-Sensitivitaet (β_F)
Welche Pricing-Variante passt     →   Varianten-Ranking
Welcher Awareness-Nudge resoniert →   Kanal-Effektivitaet

              ↓ MODELL (MOD-HILTI-EVC-001)

KPI-IMPACT PRO MASSNAHME:
─────────────────────────
V1 (Volume):  A=0.4, R=0.3, V=0.3
V3 (PPU):     A=0.6, R=0.5, V=0.5
V5 (Ausbau):  A=0.8, R=0.7, V=0.7
```

### Forced Choice Design (4 Optionen)

Alle Items haben exakt **4 Antwortoptionen**. Grund: Bei 5 Optionen waehlen ~40% die Mitte (Krosnick 1991). Mit 4 Optionen wird eine Richtungsentscheidung erzwungen — das ergibt trennschaerfere Daten fuer die KPI-Berechnung.

---

## Survey-Architektur

### Zwei Funktionen (klar getrennt)

| Funktion | Bloecke | Zweck |
|----------|---------|-------|
| **F1: Parameter-Messung** | A + B | Modell fuettern: A, σ, β_F, τ, γ_FS → Modell berechnet Massnahmen-Wirkung |
| **F2: KPI-Baseline** | C | Norm-Enforcement-Baseline → spaeter Δ messen |

### Drei methodische Saeulen

| Saeule | Fragen | Methode | Misst |
|--------|--------|---------|-------|
| **Revealed Preferences** | A1-A3 | Tatsaechliches Verhalten abfragen | Was Leute TUN |
| **Second Order Beliefs** | A4, B3, B3b | «Was glauben Sie, wie Ihre Kolleg:innen...» | Was Leute ERWARTEN |
| **First Order Preferences** | B2, B4, B5, C2 | Direkte Praeferenz (forced choice) | Was Leute WOLLEN |

### 3 Haupt-KPIs

| KPI | Name | Definition | Messbar durch |
|-----|------|-----------|---------------|
| **K1** | Akzeptanz (A-Score) | Bereitschaft, eine Veraenderung mitzutragen | B3, B3b, B4 |
| **K2** | Reziprozitaet (R-Score) | Norm-Wahrnehmung + Norm-Enforcement | A4, C2 |
| **K3** | Verhaltensaenderung (V-Score) | Wahrscheinlichkeit von tatsaechlichem Repark-Verhalten | A2, A3, B2 |

---

## Block A: Revealed Preferences — Tatsaechliches Verhalten (4 Fragen)

*Prinzip: Fragen ueber Fakten und vergangenes Verhalten. Keine Hypothesen.*

### A1. Nutzungsprofil (→ Segment-Zuordnung S1-S4)

> **How would you describe your typical charging pattern at Hilti HQ?**

- ○ I plug in every morning and usually charge to full
- ○ I charge 2-3 times per week, depending on need
- ○ I mostly do quick top-ups — small amounts here and there
- ○ My schedule varies a lot — I charge whenever I can fit it in

*→ Segment: S1 (Daily) / S2 (Occasional) / S3 (PHEV Micro) / S4 (Shift)*

**A1b.** (Nur wenn A1 = Antwort 4): **Do you work shifts at Plant Schaan?**
- ○ Yes → S4
- ○ No → S2

---

### A2. Blockierzeit — Awareness-Test (→ Parameter A)

> **Think about your last charging session. After your car was fully charged, how long did it stay connected to the station?**

- ○ I moved it within about an hour
- ○ It probably stayed 1-3 hours after charging
- ○ It stayed connected until I left for the day
- ○ I honestly have no idea when it finished charging

*→ «No idea» = direkter Awareness-Defizit-Indikator (A_low)*
*→ «Until I left» = Revealed Preference: kein Repark-Verhalten in der Baseline*
*→ Konkret («last session») statt abstrakt («typically»)*

---

### A3. Scarcity-Erfahrung (→ Demand Pressure, Problem-Severity)

> **In the past month, how often have you arrived at the charging area to find all stations occupied?**

- ○ Rarely or never
- ○ Once or twice
- ○ Several times
- ○ Almost every time I tried to charge

*→ Misst Problemdruck aus Betroffenen-Perspektive (kein Tugend-Signal)*
*→ Hohe Scarcity = staerkere Legitimation fuer Veraenderung*
*→ V-Score Input: Wer das Problem erlebt, hat hoehere Aenderungsbereitschaft*

---

### A4. Wahrgenommene Gruende fuer Umparken (→ Kanal-Effektivitaet, 2nd Order)

> **When someone at Hilti does move their car after charging is complete — what do you think is usually the main reason?**

- ○ A colleague asked them directly
- ○ They noticed all stations were full when they walked by
- ○ They got an alert from their car's app
- ○ They generally try to be considerate about shared resources

*→ 2nd Order: «Was glauben Sie, warum ANDERE umparken?» statt «Warum parken SIE um?»*
*→ Kanal-Hierarchie: Social > Salienz > Tech > Norm*
*→ R-Score Input: Anteil «colleague asked» + «considerate» = soziale Norm aktiv*

---

## Block B: Beliefs & Varianten-Praeferenz (5 Fragen)

*Prinzip: Mix aus 1st Order (direkt) und 2nd Order (Kolleg:innen) — je nach Item optimal.*

### B2. Notification-Wirkung (→ A_notification, V-Score) — 1st Order

> **If you received a push notification the moment your car was fully charged, how likely would you be to move your car within 30 minutes?**

- ○ Very unlikely
- ○ Unlikely
- ○ Likely
- ○ Very likely

*→ 1st Order: Direkte Selbsteinschaetzung (hier sinnvoll — keine Tugend-Frage)*
*→ 4-Punkt Likert ohne Mittelwert erzwingt Richtungsentscheidung*
*→ V-Score Kern-Item: Verhaltensaenderung durch Awareness-Intervention*
*→ Parameter A_notification: «Likely» + «Very likely» = A_notif_post*

---

### B3. Preis-Reaktion (→ β_F, A-Score) — 2nd Order

> **If a small fee were introduced for blocking a charging station after your car is fully charged — what share of your colleagues do you think would actually change their parking behavior?**

- ○ Almost nobody — people would just pay
- ○ Maybe 20-30% would change
- ○ About half would start moving their cars
- ○ Most people (70%+) would change their behavior

*→ Misst Preis-Elastizitaet via Peer-Projektion — KEINE WTP-Frage noetig*
*→ «Almost nobody» = niedrige β_F = Pricing allein reicht nicht*
*→ A-Score Input: implizite Akzeptanz von Pricing als Instrument*

---

### B3b. Fee-Akzeptanz bei Kolleg:innen (→ γ_FS, A-Score) — 2nd Order — NEU

> **If such a small fee were introduced — what share of your colleagues do you think would agree it's fair versus complain about it?**

- ○ Most would complain
- ○ More would complain than agree
- ○ More would agree than complain
- ○ Most would agree it's fair

*→ 2nd Order Akzeptanz-Proxy: Trennt Verhaltensreaktion (B3) von Einstellungsreaktion (B3b)*
*→ B3 hoch + B3b niedrig = Leute aendern Verhalten aber sind unzufrieden → Crowding-Out Risiko*
*→ B3 hoch + B3b hoch = Pricing ist sowohl wirksam als auch akzeptiert → V3/V4 empfohlen*
*→ A-Score Kern-Item: Akzeptanz von Pricing-Ansatz in der Population*

---

### B4. Pricing-Varianten-Praeferenz (→ Varianten-Ranking) — 1st Order

> **Four colleagues are discussing how EV charging costs should be handled at Hilti:**
>
> **Anna:** *«Pay per kilowatt-hour — you pay for what you actually use.»*
>
> **Ben:** *«A small monthly flat fee for all EV drivers — simple and predictable.»*
>
> **Clara:** *«A fee that only starts when your car is done charging but still connected — only blockers pay.»*
>
> **David:** *«A fixed number of charging days per person — for example, two days per week. Everyone gets fair access, no fees needed.»*
>
> **Who do you agree most with?**

- ○ Anna (pay per use)
- ○ Ben (monthly flat fee)
- ○ Clara (blocking fee)
- ○ David (fixed charging days, no fee)

*→ Varianten-Mapping: Anna=V3 (PPU), Ben=V2 (Flatrate), Clara=V4 (Time/Blocking), David=V1 (Quota)*
*→ 1st Order mit Charakter-Projektion: reduziert Anchoring auf erste Option*
*→ A-Score Input: Verteilung zeigt welche Pricing-Logik am meisten Rueckhalt hat*
*→ WICHTIG: Namen-Zuordnung in MS Forms randomisieren!*

---

### B5. Non-Pricing Praeferenz (→ Awareness-Kanal, Norm-Ansatz) — 1st Order

> **If Hilti were to introduce ONE non-monetary approach to improve the charging situation — which would you support most?**

- ○ A smart push notification the moment your car is fully charged
- ○ Printed reminders in office and plant areas (e.g. "Your car may be fully charged — have you moved it?")
- ○ A morning reminder email on days you're plugged in (e.g. "You're charging today — remember to move when done")
- ○ Collectively agreed charging etiquette guidelines among EV drivers

*→ 3 Awareness-Nudges + 1 Norm-Ansatz (Problem ist primaer Awareness)*
*→ Option 1: Direct Notification (Awareness — personalisiert, real-time)*
*→ Option 2: Physical Reminder (Awareness — Salienz im Arbeitsumfeld)*
*→ Option 3: Morning Reminder Email (Awareness — Pre-Commitment/Priming)*
*→ Option 4: Community Guidelines (Norm — kein Awareness-Element)*
*→ Verteilung zeigt: Welcher Awareness-Kanal resoniert am staerksten?*

---

## Block C: Norm-Assessment (1 Frage)

### C2. Norm-Enforcement (→ R-Score, σ)

> **A colleague consistently leaves their car at the charging station from 7 AM to 6 PM every day, even though it finishes charging by 10 AM. How would you describe your reaction?**

- ○ That's their right — stations are first come, first served
- ○ A bit annoying, but not my place to say anything
- ○ I think that's unfair and would wish someone addressed it
- ○ I would bring it up with them or suggest a better system

*→ Norm-Enforcement Staerke: passiv (Option 1-2) vs. aktiv (Option 3-4)*
*→ R-Score Kern-Item: Bereitschaft, Normen aktiv durchzusetzen*
*→ «Their right» = kein sozialer Druck → braucht Pricing oder Infrastruktur*
*→ «Bring it up» = starker sozialer Hebel → Norm-Interventionen wirksam*

---

## Block D: Abschluss (2 Fragen)

### D1. Segment-Validierung

> **What type of electric vehicle do you drive?**

- ○ Fully electric (BEV)
- ○ Plug-in Hybrid (PHEV)

*→ Segment S3 Validierung (PHEV + Top-up = S3)*

### D2. Offener Kommentar

> **Is there anything about the EV charging situation at Hilti HQ that we should know but haven't asked about?**

[Free text]

---

## KPI-Bildung: Survey → Index

### K1: Akzeptanz-Score (A-Score) ∈ [0, 1]

> Wie hoch ist die Bereitschaft, eine Veraenderung mitzutragen?

| Quelle | Gewicht | Berechnung |
|--------|---------|------------|
| B3 (Preis-Reaktion 2nd Order) | 0.30 | %half_or_more (Antwort 3+4) |
| B3b (Fee-Akzeptanz 2nd Order) | 0.35 | %agree (Antwort 3+4) |
| B4 (Pricing-Variante) | 0.20 | 1 - %David (David = «fixed days, no fee» = niedrigste Pricing-Akzeptanz) |
| A3 (Scarcity-Erfahrung) | 0.15 | %several_or_more (Antwort 3+4) |

```
A-Score = 0.30 × B3_change_pct + 0.35 × B3b_agree_pct
        + 0.20 × (1 - B4_david_pct) + 0.15 × A3_scarcity_pct
```

**Interpretation:**

| A-Score | Bedeutung | Empfehlung |
|---------|-----------|------------|
| > 0.65 | Hohe Akzeptanz | Pricing-Variante (V3 oder V4) direkt umsetzbar |
| 0.45 - 0.65 | Moderate Akzeptanz | Awareness-Nudge vorschalten, dann Pricing |
| < 0.45 | Niedrige Akzeptanz | NUR Non-Pricing (Awareness + Infrastruktur) |

---

### K2: Reziprozitaets-Score (R-Score) ∈ [0, 1]

> Wie stark ist Norm-Wahrnehmung und Norm-Durchsetzung?

| Quelle | Gewicht | Berechnung |
|--------|---------|------------|
| C2 (Norm-Enforcement) | 0.55 | %unfair_or_act (Antwort 3+4) |
| A4 (Soziale Gruende 2nd Order) | 0.45 | %colleague_asked + %considerate (Antwort 1+4) |

```
R-Score = 0.55 × C2_enforce_pct + 0.45 × A4_social_pct
```

**Interpretation:**

| R-Score | Bedeutung | Empfehlung |
|---------|-----------|------------|
| > 0.65 | Starke Norm | Soziale Interventionen hoch effektiv (Dashboard, Peer-Nudge) |
| 0.40 - 0.65 | Moderate Norm | Norm existiert, braucht Sichtbarmachung (B5 Options 2-3) |
| < 0.40 | Schwache Norm | Norm-Ansatz allein reicht nicht — Pricing oder Infrastruktur noetig |

---

### K3: Verhaltensaenderungs-Score (V-Score) ∈ [0, 1]

> Wie wahrscheinlich ist tatsaechliche Verhaltensaenderung?

| Quelle | Gewicht | Berechnung |
|--------|---------|------------|
| A2 (Awareness Baseline) | 0.30 | 1 - %no_idea (Antwort 4) — invertiert: hohe Awareness = hoher V-Score |
| B2 (Notification Response) | 0.40 | %likely_or_very (Antwort 3+4) |
| A3 (Scarcity-Erfahrung) | 0.30 | %several_or_more (Antwort 3+4) |

```
V-Score = 0.30 × (1 - A2_no_idea_pct) + 0.40 × B2_likely_pct
        + 0.30 × A3_scarcity_pct
```

**Interpretation:**

| V-Score | Bedeutung | Empfehlung |
|---------|-----------|------------|
| > 0.60 | Hohe Aenderungsbereitschaft | Notification allein kann genuegen |
| 0.35 - 0.60 | Moderate Bereitschaft | Notification + Pricing-Signal kombinieren |
| < 0.35 | Niedrige Bereitschaft | Strukturelle Loesung (V5 Infrastruktur) noetig |

---

## Diagnostische Kreuz-Tabellen

### Awareness vs. Willingness Diagnose

| | A2: weiss wann geladen | A2: «no idea» |
|---|---|---|
| **B2: likely/very likely** | Weiss + Will → Strukturproblem (Hassle) | Weiss nicht + Will → **Awareness-Intervention = Quick Win** |
| **B2: unlikely/very unlikely** | Weiss + Will nicht → **Willingness-Problem** | Weiss nicht + Will nicht → Doppelt-Defizit → V5 |

### Pricing-Akzeptanz Diagnose

| | B3b: agree (fair) | B3b: complain |
|---|---|---|
| **B3: wuerden Verhalten aendern** | Pricing wirkt + akzeptiert → **V3/V4 empfohlen** | Pricing wirkt aber Widerstand → **Crowding-Out Risiko** |
| **B3: wuerden NICHT aendern** | Akzeptiert aber wirkungslos → Awareness first | Weder wirksam noch akzeptiert → **NUR V5** |

---

## Parameter-Update: Survey → Modell

| Frage | Modell-Parameter | Prior | Update-Regel |
|-------|-----------------|-------|-------------|
| A2 | A (Awareness Baseline) | Beta(3,2) | %no_idea → A_low; %moved_within_hour → A_high |
| A3 | Demand Pressure | — | %scarcity = Problem-Severity |
| A4 | Kanal-Vektor | — | Ranking: Social > Salienz > Tech > Norm |
| B2 | A_notification | Beta(3,2) | %likely + %very_likely → A_notif_post |
| B3 | β_F (Preis-Sensitivitaet) | N(0.60, 0.12) | %change → β_F_post |
| B3b | γ_FS (Crowding-Out) | N(-0.30, 0.10) | %complain → γ_FS staerker negativ |
| B4 | Varianten-Ranking | — | Haeufigkeit: Anna(V3) / Ben(V2) / Clara(V4) / David(V1) |
| B5 | Awareness-Kanal | — | Haeufigkeit: Notification / Physical Reminder / Morning Email / Guidelines |
| C2 | σ (Soziale Norm) | N(0.35, 0.08) | %enforce → σ_post |

---

## Entscheidungsmatrix: KPI-Kombination → Massnahmen-Empfehlung

```
A-Score    R-Score    V-Score    →  Empfehlung
──────────────────────────────────────────────────────────
Hoch       Hoch       Hoch       →  B4-Winner (Pricing-Variante mit staerkstem Support)
Hoch       Hoch       Niedrig    →  Awareness-Nudge (B5-Winner) zuerst → dann B4-Winner
Hoch       Niedrig    Hoch       →  B4-Winner direkt — Pricing wirkt auch ohne Norm
Hoch       Niedrig    Niedrig    →  V5 (Infrastruktur) + B5-Winner
Niedrig    Hoch       x          →  B5-Winner + Community Guidelines (kein Pricing)
Niedrig    Niedrig    Hoch       →  B5-Winner allein (Awareness genuegt)
Niedrig    Niedrig    Niedrig    →  NUR V5 (rein strukturelle Loesung)
```

**B4-Winner:** Die Pricing-Variante mit den meisten Stimmen (Anna/Ben/Clara/David)
**B5-Winner:** Der Non-Pricing-Ansatz mit den meisten Stimmen

---

## Methodische Absicherung

### Gegen Hypothetical Bias
- Block A fragt NUR nach tatsaechlichem Verhalten und Erfahrungen
- Keine kWh-Preise, keine abstrakten Modelle — konkrete Erfahrungen

### Gegen Social Desirability
- A3 (Scarcity) statt «Haben Sie brav umgeparkt?»
- A4 als 2nd Order: «Warum parken ANDERE um?»
- B3/B3b als 2nd Order: «Was wuerden KOLLEG:INNEN tun/denken?»
- B4 mit Charakter-Projektion (Anna/Ben/Clara/David)

### Forced Choice (4 Optionen)
- Alle Items: 4 Optionen, kein Mittelwert
- Erzwingt Richtungsentscheidung
- Trennschaerfere Daten fuer KPI-Berechnung

### Awareness vs. Willingness Trennung
- A2 + B2 messen AWARENESS (Gate-Parameter A)
- B3 + B3b + B4 messen WILLINGNESS/AKZEPTANZ (β_F, γ_FS)
- B5 testet Awareness-KANAL (welcher Nudge wirkt?)
- Diagnostische Kreuz-Tabellen trennen die beiden Dimensionen sauber

---

## Implementation Notes for MS Forms

1. **Block-Reihenfolge beibehalten:** A (Fakten) → B (Beliefs + Praeferenzen) → C (Norm) → D (Abschluss)
2. **B4 (Anna/Ben/Clara/David):** Namen-Zuordnung zu Varianten randomisieren
3. **A1b:** Nur anzeigen wenn A1 = «schedule varies»
4. **Pflichtfelder:** A1-A4, B2-B5, B3b, C2 (D2 optional)
5. **Segment-Variable:** Automatisch aus A1 + A1b + D1 berechnen

### Einleitungstext

> *EV charging at Hilti HQ is a shared resource — with about 100 stations and 400 EV drivers, we want to develop a solution that works for everyone. This short survey (about 5 minutes) asks about your actual experience and what you observe among colleagues. Your responses are completely anonymous and will directly shape the approach we take.*

---

## Testbare Modell-Vorhersagen (aus dem Survey ableitbar)

| ID | Vorhersage | Survey-Pruefung | Wenn verletzt |
|----|-----------|----------------|--------------|
| SP-1 | A2: >40% sagen «no idea» wann Ladung fertig | A_baseline < 0.50 | Awareness-Nudge = PFLICHT vor allem anderen |
| SP-2 | B2: >60% sagen «likely/very likely» bei Notification | A_notif > 0.60 | Notification allein kann genuegen |
| SP-3 | B3b: >50% erwarten «complain» bei Fee | γ_FS < -0.25 | Pricing-Varianten = Crowding-Out Risiko |
| SP-4 | B4: Clara (Blocking Fee) hat Mehrheit | V4 > V1, V2, V3 | Blocking Fee = fairste Pricing-Logik |
| SP-5 | B5: Notification hat Mehrheit ueber Physical/Email | Direct > Physical > Pre-Commit | Personalisierter Push = praeferierter Kanal |
| SP-6 | C2: >50% finden Blockieren unfair | σ > 0.50 | Sozialer Hebel ist aktivierbar |

---

*Version 3.1 — B3/B4/B5 Fixes: Blocking-Fee Wording, Charging Days statt Volume Limit, Physical Reminders statt Dashboard/Social Email*
*Modell: MOD-HILTI-EVC-001 | Session: EBF-S-2026-02-20-ORG-001*
*FehrAdvice & Partners AG*
