# EV Charging Survey Design — Hilti HQ (v2.0)

**Projekt:** PRJ-HILTI-001 (Parking Management E-Mobility)
**Modell:** MOD-HILTI-EVC-001 (Gated Logistic Repark Model)
**Version:** 2.0 (komplett ueberarbeitet)
**Sprache:** Englisch
**Plattform:** Microsoft Forms
**Anonym:** Ja
**Zielgruppe:** Aktuelle EV-Fahrer am Hilti HQ Schaan (~400 Personen)
**Geschaetzte Dauer:** ~8 Minuten (16 Fragen)
**Erstellt:** 2026-02-20

---

## Design-Philosophie: Warum NICHT direkt nach Massnahmen fragen?

### Christians Ansatz (direkt)

> Varianten V1-V5 vorstellen → «Welche akzeptierst du?» → KPIs abfragen

**Probleme:**

| # | Problem | Konsequenz |
|---|---------|------------|
| 1 | **Hypothetical Bias** | Leute koennen nicht zuverlaessig vorhersagen, wie sie auf ein nie erlebtes Preismodell reagieren |
| 2 | **Strategic Responding** | Rationale Antwort: «Ich bevorzuge das Guenstigste fuer mich» → alle waehlen Status Quo |
| 3 | **Abstraktionsproblem** | «0.15 CHF/kWh» — niemand hat eine Intuition fuer kWh-Preise als Verhaltensanreiz |
| 4 | **Framing/Reihenfolge-Effekt** | Erste Variante wird geankert, Formulierung beeinflusst Wahl |
| 5 | **Soziale Erwuenschtheit** | «Wuerden Sie umparken?» → «Ja natuerlich!» (inflationaere Akzeptanz, deflationaere Aenderung) |

### Unser Ansatz (indirekt)

> Verhaltensparameter messen → Modell berechnet → welche Massnahme zahlt am meisten auf welchen KPI ein

```
WAS DIE LEUTE BEANTWORTEN:           WAS DAS MODELL BERECHNET:
─────────────────────────────         ────────────────────────────
Tatsaechliches Verhalten          →   Awareness-Level (A)
Was sie bei Kolleg:innen beobachten → Soziale Norm (σ)
Wie sie in konkreten Situationen  →   Aufwandskosten (τ) pro Segment
  reagiert haben oder wuerden
Was sie Kolleg:innen zutrauen     →   Preis-Sensitivitaet (β_F)
Ob Preis oder Gemeinschaft        →   Crowding-Out Risiko (γ_FS)
  wichtiger ist

              ↓ MODELL (MOD-HILTI-EVC-001)

KPI-IMPACT PRO MASSNAHME:
─────────────────────────
V1 (Mengen):  A=0.4, R=0.3, V=0.3
V3 (PPU):     A=0.6, R=0.5, V=0.5
V5 (Ausbau):  A=0.8, R=0.7, V=0.7
...
```

**Kernprinzip:** Die Leute beantworten Fragen, die sie authentisch beantworten KOENNEN. Das Modell berechnet, was sie nicht beantworten KOENNEN (welche Massnahme wirkt am besten).

---

## Survey-Architektur

### Zwei Funktionen (klar getrennt)

| Funktion | Bloecke | Zweck |
|----------|---------|-------|
| **F1: Parameter-Messung** | A + B | Modell fuettern: A, σ, β_F, τ, γ_FS, ι → Modell berechnet Massnahmen-Wirkung |
| **F2: KPI-Baseline** | C | Vorher-Werte fuer Akzeptanz, Reziprozitaet, Verhaltensaenderung → spaeter Δ messen |

### Drei methodische Saeulen

| Saeule | Fragen | Methode | Misst |
|--------|--------|---------|-------|
| **Revealed Preferences** | A1-A4 | Tatsaechliches Verhalten abfragen | Was Leute TUN |
| **Second Order Beliefs** | B1-B5 | «Was glauben Sie, wie Ihre Kolleg:innen...» | Was Leute ERWARTEN |
| **Vignetten + KPI-Baseline** | C1-C5 + D1-D2 | Konkrete Szenarien + KPI-Indices | Verhaltensproxies + Baseline |

### 3 Haupt-KPIs

| KPI | Name | Definition | Messbar durch |
|-----|------|-----------|---------------|
| **K1** | Akzeptanz (A-Score) | Bereitschaft, eine Veraenderung mitzutragen | B3, B4, C3, C4 |
| **K2** | Reziprozitaet (R-Score) | Bedingte Kooperation + Norm-Enforcement | B1, C1, C2 |
| **K3** | Verhaltensaenderung (V-Score) | Wahrscheinlichkeit von tatsaechlichem Repark-Verhalten | A2, A3, B2, C5 |

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
*→ Natuerliche Sprache statt technischer Frequenz-Abfrage*

**A1b.** (Nur wenn A1 = Antwort 4): **Do you work shifts at Plant Schaan?**
- ○ Yes → S4
- ○ No → S2

---

### A2. Blockierzeit — Awareness-Test (→ Parameter A)

> **Think about your last charging session. After your car was fully charged, how long did it stay connected to the station?**

- ○ I moved it right away
- ○ About 1-2 hours
- ○ Probably 3-5 hours
- ○ It stayed until I left for the day
- ○ Honestly, I have no idea when it finished charging

*→ «No idea» = direkter Awareness-Defizit-Indikator (A_low)*
*→ «Until I left» = Revealed Preference: kein Repark-Verhalten in der Baseline*
*→ Konkret («last session») statt abstrakt («typically»)*

---

### A3. Vergangenes Repark-Verhalten (→ V-Score Baseline)

> **In the past month, have you ever moved your car from a charging spot to a regular parking spot to free up the charger?**

- ○ Yes, several times
- ○ Yes, once or twice
- ○ No, but I've thought about it
- ○ No — it honestly never occurred to me

*→ Revealed Preference Baseline fuer V-Score*
*→ «Never occurred» vs «thought about it» = Awareness-Gradient*
*→ Keine hypothetische Frage — reines Verhalten*

---

### A4. Natuerliche Ausloeser (→ Kanal-Effektivitaet)

> **If you HAVE moved your car before — what actually prompted you? If not — which of these would most likely get you to move?**

- ○ A colleague asked me personally
- ○ I saw that all stations were occupied and felt bad
- ○ I happened to check my phone/app and noticed charging was done
- ○ No specific trigger — I just try to be considerate
- ○ Honestly, nothing has made me think about it so far

*→ Kanal-Hierarchie: Social (Kollege) > Salienz (alle besetzt) > Tech (App) > Norm (Gewissen)*
*→ Mischt Revealed (hat) und niedrigschwellig Stated (wuerde)*

---

## Block B: Second Order Beliefs — Was Kolleg:innen denken und tun (5 Fragen)

*Prinzip: «Was glauben Sie, wie Ihre Kolleg:innen...» umgeht Selbstschutz und misst die wahrgenommene Norm.*

### B1. Norm-Schaetzung (→ σ, R-Score)

> **What percentage of your EV-driving colleagues do you think would agree with this statement: «A fully charged car should not block a charging station for hours — it's not fair to others who need it.»**

- ○ Less than 25% would agree
- ○ About 25-50% would agree
- ○ About 50-75% would agree
- ○ More than 75% would agree

*→ 2nd Order Belief misst σ (Soziale Norm) OHNE dass die Person sich selbst positionieren muss*
*→ Schaetzung >50% = Norm existiert, kann aktiviert werden*
*→ R-Score Input: hoher Wert = starke Reziprozitaets-Erwartung*

---

### B2. Notification-Wirkung (→ A_notification, V-Score)

> **Imagine every EV driver received a push notification the moment their car is fully charged. What percentage of your colleagues do you think would actually move their car within 30 minutes?**

- ○ Less than 20%
- ○ About 20-40%
- ○ About 40-60%
- ○ More than 60%

*→ 2nd Order umgeht «Ja, ICH wuerde natuerlich sofort...»*
*→ Misst realistische Erwartung an Notification-Effektivitaet*
*→ V-Score Input: Verhaltensaenderung durch Information allein*

---

### B3. Preis-Reaktion (→ β_F, A-Score)

> **If a small fee were introduced for electricity consumed while the car is just standing (not charging) — what share of your colleagues do you think would actually change their parking behavior?**

- ○ Almost nobody — people would just pay and complain
- ○ Maybe 20-30% would change
- ○ About half would start moving their cars
- ○ Most people (70%+) would change their behavior

*→ Misst Preis-Elastizitaet via Peer-Projektion — KEINE WTP-Frage noetig*
*→ «Almost nobody» = niedrige β_F = Pricing allein reicht nicht*
*→ A-Score Input: implizite Akzeptanz von Pricing als Instrument*

---

### B4. Preis vs. Gemeinschaft (→ γ_FS, A-Score)

> **Two colleagues are talking about the charging situation:**
>
> **Anna says:** *«The simplest solution is a small fee for blocking. Everyone pays for what they use — that's fair.»*
>
> **Thomas says:** *«I think a fee sends the wrong signal. We're all Hilti — we should sort this out as a community, not with a price tag.»*
>
> **Which perspective do you think MOST of your colleagues would agree with?**

- ○ Most would agree with Anna (fee = fair)
- ○ Slight majority would agree with Anna
- ○ Slight majority would agree with Thomas
- ○ Most would agree with Thomas (community = better)

*→ 2nd Order + Charakter-Projektion = doppelte Distanzierung*
*→ Thomas-Mehrheit = Crowding-Out Risiko (γ_FS stark negativ)*
*→ A-Score Input: Akzeptanz von Pricing-Ansatz*
*→ Entscheidend fuer: V3/V4 (Pricing) vs V5 (Infrastruktur)*

---

### B5. Loesungs-Praeferenz der Mehrheit (→ Varianten-Ranking, A-Score)

> **If Hilti were to introduce ONE approach to improve the charging situation — which one do you think would get the most support from your colleagues?**

- ○ A smart notification system that tells you when charging is done and a station is free
- ○ More charging stations so that waiting and blocking is no longer an issue
- ○ A combination: more stations, smart notifications, and a small usage-based fee
- ○ Clear community guidelines — agreed rules, no fees needed

*→ Misst Varianten-Akzeptanz via 2nd Order (nicht: «Was wollen SIE?»)*
*→ Entspricht: Notification / V5 Infra / V5 Kombi / Norm-only*
*→ A-Score: Population-Level Praeferenz*
*→ KEINE kWh-Preise, keine abstrakten Modelle — konkrete Loesungsbilder*

---

## Block C: Vignetten + KPI-Diagnostik (5 Fragen)

*Prinzip: Konkrete Szenarien fuer Revealed-Preference-Proxies. KPI-bildungsfaehige Items.*

### C1. Reziprozitaet: Bedingte Kooperation (→ R-Score Kern)

> **Imagine you find out that the majority of your EV-driving colleagues have started moving their cars once charging is complete. Would that change your own behavior?**

- ○ Definitely — I'd want to do my part too
- ○ Probably — it would feel like the right thing to do
- ○ Maybe — depends on whether it's convenient
- ○ Not really — my decision wouldn't depend on what others do

*→ Bedingte Kooperation (Fehr & Fischbacher 2004, Fischbacher et al. 2001)*
*→ «Definitely» + «Probably» = R-Score hoch → Norm-basierte Intervention wirkt*
*→ «Not really» = individualistisch → braucht strukturelle Loesung*

---

### C2. Reziprozitaet: Norm-Enforcement (→ R-Score, negative Seite)

> **A colleague consistently leaves their car at the charging station from 7 AM to 6 PM every day, even though it finishes charging by 10 AM. How would you describe your reaction?**

- ○ That's their right — stations are first come, first served
- ○ A bit annoying, but not my place to say anything
- ○ I think that's unfair and would wish someone addressed it
- ○ I would bring it up with them or suggest a better system

*→ Negative Reziprozitaet + Bestrafungsbereitschaft*
*→ «Bring it up» = hohe Norm-Enforcement → starker sozialer Hebel vorhanden*
*→ «Their right» = kein sozialer Druck → Pricing oder Infrastruktur noetig*
*→ R-Score: Bereitschaft, Normen aktiv durchzusetzen*

---

### C3. Vignette: Realistisches Umpark-Szenario (→ V-Score, τ)

> **Picture this: It's 11:30 AM. Your car finished charging at 10 AM. You have a meeting at noon. You get a message from a colleague: «Hey, any chance your car is done? I really need to charge before my client visit this afternoon.»**
>
> **What would you realistically do?**

- ○ Go move my car right away — they need it more
- ○ Reply that I'll move it right after my meeting (around 1 PM)
- ○ Feel bad but probably not make it — the timing is too tight
- ○ I probably wouldn't see the message until much later

*→ Vignette = naeher an Revealed als abstrakte Praeferenz*
*→ Konkrete Zeit, konkreter Grund, konkreter sozialer Druck*
*→ Option C/D = ehrliche «Nein»-Antworten ohne Gesichtsverlust*
*→ V-Score Input + τ (Aufwandskosten in realistischem Szenario)*

---

### C4. Akzeptanz: Gap-Wahrnehmung (→ A-Score, ι)

> **When you think about Hilti's sustainability commitments — does the current EV charging situation at HQ feel like it matches what Hilti stands for?**

- ○ Yes, it works well as it is
- ○ It's fine but could be organized better
- ○ Not really — it feels a bit unmanaged for a company like Hilti
- ○ I haven't really thought about it that way

*→ Misst Corporate Identity (ι) INDIREKT — kein «Ist Ihnen Nachhaltigkeit wichtig?»*
*→ Gap-Wahrnehmung: je groesser der Gap, desto hoeher die Veraenderungsbereitschaft*
*→ A-Score Input: «Could be better» + «Not really» = hohe Akzeptanz fuer Veraenderung*

---

### C5. Commitment-Bereitschaft (→ V-Score, Pre-Commitment)

> **If Hilti introduced a voluntary «Fair Charging Pledge» — a simple commitment to free up your station within 30 minutes of charging completion — would you sign it?**

- ○ Yes, I'd sign it
- ○ I'd seriously consider it
- ○ Probably not
- ○ No

*→ Pre-Commitment Device (Ariely & Wertenbroch 2002)*
*→ «Sign» = starker V-Score (realer als «Wuerden Sie umparken?»)*
*→ Pledge hat bindende Wirkung — Frage nach Commitment ist naeher an Revealed als Frage nach Intention*

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
| B3 (Preis-Reaktion 2nd Order) | 0.25 | %half_or_more (Antwort 3+4) |
| B4 (Anna/Thomas 2nd Order) | 0.25 | %Anna (Antwort 1+2) |
| B5 (Loesungs-Praeferenz) | 0.25 | %Kombi_or_Infra (Antwort 2+3) |
| C4 (Gap-Wahrnehmung) | 0.25 | %could_be_better + %not_really (Antwort 2+3) |

```
A-Score = 0.25 × B3_change_pct + 0.25 × B4_anna_pct
        + 0.25 × B5_kombi_infra_pct + 0.25 × C4_gap_pct
```

**Interpretation:**
| A-Score | Bedeutung | Empfehlung |
|---------|-----------|------------|
| > 0.65 | Hohe Akzeptanz | Pricing-Variante (V3) direkt umsetzbar |
| 0.45 - 0.65 | Moderate Akzeptanz | Kommunikation vorschalten, dann V3 oder V5 |
| < 0.45 | Niedrige Akzeptanz | NUR Infrastruktur (V5) ohne Pricing |

---

### K2: Reziprozitaets-Score (R-Score) ∈ [0, 1]

> Wie stark ist bedingte Kooperation und Norm-Durchsetzung?

| Quelle | Gewicht | Berechnung |
|--------|---------|------------|
| B1 (Norm-Schaetzung 2nd Order) | 0.30 | %above_50 (Antwort 3+4) |
| C1 (Bedingte Kooperation) | 0.40 | %definitely + %probably (Antwort 1+2) |
| C2 (Norm-Enforcement) | 0.30 | %unfair + %bring_it_up (Antwort 3+4) |

```
R-Score = 0.30 × B1_above50_pct + 0.40 × C1_cond_coop_pct
        + 0.30 × C2_enforce_pct
```

**Interpretation:**
| R-Score | Bedeutung | Empfehlung |
|---------|-----------|------------|
| > 0.70 | Starke Reziprozitaet | Soziale-Norm-Interventionen hoch effektiv |
| 0.45 - 0.70 | Moderate Reziprozitaet | Norm existiert, braucht Sichtbarmachung |
| < 0.45 | Schwache Reziprozitaet | Norm-Ansatz allein reicht nicht, Pricing oder Infrastruktur noetig |

---

### K3: Verhaltensaenderungs-Score (V-Score) ∈ [0, 1]

> Wie wahrscheinlich ist tatsaechliche Verhaltensaenderung?

| Quelle | Gewicht | Berechnung |
|--------|---------|------------|
| A2 (Vergangenes Repark) | 0.25 | %yes_several + %yes_once (Antwort 1+2) — Revealed |
| A3 (Natuerliche Ausloeser) | 0.15 | %colleague + %saw_occupied + %app (Antwort 1+2+3) |
| B2 (Notification 2nd Order) | 0.20 | %above_40 (Antwort 3+4) |
| C3 (Vignette Repark) | 0.20 | %move_now + %after_meeting (Antwort 1+2) |
| C5 (Pledge Commitment) | 0.20 | %sign + %consider (Antwort 1+2) |

```
V-Score = 0.25 × A2_revealed_pct + 0.15 × A3_trigger_pct
        + 0.20 × B2_notif_pct + 0.20 × C3_vignette_pct
        + 0.20 × C5_pledge_pct
```

**Interpretation:**
| V-Score | Bedeutung | Empfehlung |
|---------|-----------|------------|
| > 0.60 | Hohe Aenderungsbereitschaft | Leichter Nudge + Notification reicht |
| 0.35 - 0.60 | Moderate Bereitschaft | Nudge + Pricing-Signal kombinieren |
| < 0.35 | Widerstand oder Indifferenz | Strukturelle Loesung (V5) noetig |

---

## Parameter-Update: Survey → Modell

| Frage | Modell-Parameter | Prior | Update-Regel |
|-------|-----------------|-------|-------------|
| A2 | A (Awareness Baseline) | Beta(3,2) | %no_idea → A_low; %moved → A_high |
| A3 | V_baseline | — | %already_moved → Baseline Repark-Rate |
| A4 | Kanal-Vektor | — | Ranking: Social > Salienz > Tech > Norm |
| B1 | σ (Soziale Norm) | N(0.35, 0.08) | %above_50 → σ_post |
| B2 | A_notification | Beta(3,2) | %above_40 → A_notif_post |
| B3 | β_F (Preis-Sensitivitaet) | N(0.60, 0.12) | %change → β_F_post |
| B4 | γ_FS (Crowding-Out) | N(-0.30, 0.10) | %Thomas → γ_FS staerker negativ |
| B5 | Varianten-Ranking | — | Ranking nach Haeufigkeit |
| C1 | Reziprozitaet | — | %cond_coop → R-Faktor |
| C3 | τ (Aufwand) | LogN(-0.5, 0.3) | %move_now vs %not_make_it → τ_post |
| C4 | ι (Identity Gap) | N(0.25, 0.10) | %gap → ι_post |

---

## Entscheidungsmatrix: KPI-Kombination → Massnahmen-Empfehlung

```
A-Score    R-Score    V-Score    →  Empfehlung
──────────────────────────────────────────────────────────
Hoch       Hoch       Hoch       →  V3 (PPU) — Community traegt Pricing
Hoch       Hoch       Niedrig    →  Notification + Norm zuerst → dann V3
Hoch       Niedrig    Hoch       →  V3 oder V4 — Preis wirkt auch ohne Norm
Hoch       Niedrig    Niedrig    →  V5 (Infrastruktur, da Pricing akzeptiert aber Verhalten traege)
Niedrig    Hoch       x          →  V5 + Norm (kein hartes Pricing)
Niedrig    Niedrig    Hoch       →  Notification allein (V-Score zeigt Bereitschaft)
Niedrig    Niedrig    Niedrig    →  NUR V5 (rein strukturelle Loesung)
```

---

## Methodische Absicherung

### Gegen Hypothetical Bias
- Block A fragt NUR nach tatsaechlichem Verhalten
- C3 verwendet konkrete Vignette statt abstrakter Praeferenz
- C5 fragt nach Commitment (bindender als Intention)

### Gegen Social Desirability
- Block B verwendet durchgehend 2nd Order Beliefs («Was denken Ihre Kolleg:innen?»)
- B4 nutzt Charakter-Projektion (Anna/Thomas) + 2nd Order (doppelte Distanzierung)
- C2 bietet «Their right» als gesichtswahrende Non-Enforcement-Option

### Fuer Revealed Preference Proxies
- A2: Tatsaechliches vergangenes Verhalten (schon umgeparkt?)
- A3: Tatsaechliche Ausloeser (was hat funktioniert?)
- A4 (Awareness): Wissenstest statt Einstellungsfrage
- C3: Vignette mit konkretem Zeitdruck, sozialem Kontext, realistischen Optionen

### Fuer zuverlaessige KPI-Bildung
- Jeder KPI hat 3-5 Items aus verschiedenen Bloecken (Triangulation)
- Mischung aus Revealed (A-Block), 2nd Order (B-Block), Vignette (C-Block)
- Alle Items auf gleiche Skala normierbar (Anteil der «positiven» Antworten)
- Vorher-Nachher-Messung moeglich (gleicher Survey nach Intervention)

---

## Implementation Notes for MS Forms

1. **Block-Reihenfolge beibehalten:** A (Fakten) → B (2nd Order) → C (Szenarien) → D (Abschluss)
2. **Innerhalb Block B:** Antwortoptionen-Reihenfolge randomisieren wo moeglich
3. **B4 (Anna/Thomas):** Namen-Zuordnung randomisieren (50% sehen Anna=Fee zuerst, 50% Thomas=Fee)
4. **A1b:** Nur anzeigen wenn A1 = «schedule varies»
5. **Pflichtfelder:** A1-A4, B1-B5, C1-C5 (D2 optional)
6. **Segment-Variable:** Automatisch aus A1 + A1b + D1 berechnen

### Einleitungstext

> *EV charging at Hilti HQ is a shared resource — with about 100 stations and 400 EV drivers, we want to develop a solution that works for everyone. This short survey (about 8 minutes) asks about your actual experience and what you observe among colleagues. Your responses are completely anonymous and will directly shape the approach we take.*

---

## Testbare Modell-Vorhersagen (aus dem Survey ableitbar)

| ID | Vorhersage | Survey-Pruefung | Wenn verletzt |
|----|-----------|----------------|--------------|
| SP-1 | A2: >40% sagen «no idea» wann Ladung fertig | A < 0.50 | Notification = PFLICHT vor allem anderen |
| SP-2 | B1: >50% schaetzen Norm bei >50% | σ > 0.50 | Sozialer Hebel ist verfuegbar |
| SP-3 | B4: Thomas-Mehrheit (>50%) | γ_FS < -0.25 | Pricing-Varianten (V2, V3) = Crowding-Out Risiko |
| SP-4 | C1: >60% «definitely» oder «probably» | R-Score > 0.60 | Bedingte Kooperation funktioniert |
| SP-5 | C3: <40% wuerden sofort umparken (Vignette) | V_realistic < 0.40 | Strukturelle Loesung (V5) noetig |
| SP-6 | C5: >50% wuerden Pledge unterschreiben | Commitment > 0.50 | Pledge als Intervention-Baustein |

---

*Version 2.0 — Komplett ueberarbeitet nach Feedback: Second Order Beliefs, Revealed Preferences, KPI-Bildung*
*Modell: MOD-HILTI-EVC-001 | Session: EBF-S-2026-02-20-ORG-001*
*FehrAdvice & Partners AG*
