# ALPLA Directors Meeting — Behavioral Presentation Architecture

| Feld | Wert |
|------|------|
| **Session-ID** | EBF-S-2026-02-23-ORG-001 |
| **Output-ID** | OUT-045 |
| **Datum Meeting** | 27. Februar 2026 |
| **Praesentator** | Walter Ritzer (COO) |
| **Dauer** | 40 Minuten |
| **Publikum** | Fuehrungskreis der Direktoren (Jahresmeeting) |
| **Erstellt** | 2026-02-23 |

---

## Executive Summary

Dieses Dokument ist die vollstaendige Behavioral Design Architektur fuer Walters 40-Minuten-Slot im Direktoren-Jahresmeeting. Es ueberarbeitet die 3 Themen (Safety & Environment, Update Next, Quality/RECARE) mit 7 verhaltenspsychologischen Prinzipien fuer maximalen Impact, Spannung und Nachhaltige Wirkung.

**Zentrale Design-Entscheidungen:**
1. **Neue Reihenfolge:** Quality → Next → Safety (Problem → Loesung → Sinn)
2. **Attention Resets** alle 8-10 Minuten (Frage, Story, Demo)
3. **Multiplikatoren-Aktivierung** in jedem Block ("Was IHR tun koennt / Was IHR davon habt")
4. **Physisches Commitment** am Ende (Karte statt Slides)

---

## Teil 1: DIAGNOSE — Warum Standard-Praesentationen scheitern

### Das typische Jahresmeeting-Muster

```
Minute 0-5:    "Hier sind unsere KPIs..."        → Aufmerksamkeit 80%
Minute 5-15:   "Und hier noch mehr Zahlen..."    → Aufmerksamkeit 40%
Minute 15-30:  "Und ausserdem..."                → Aufmerksamkeit 20%
Minute 30-40:  "Zusammenfassung und Fragen?"     → Handys unter Tisch

ERGEBNIS: Direktoren nicken, gehen raus, vergessen 90% in 24 Stunden.
```

### Walters Ziel erfordert eine andere Architektur

- Direktoren sollen **MULTIPLIZIEREN** (in ihren Bereichen handeln)
- Direktoren sollen sich **COMMITTEN** (oeffentlich, messbar)
- Direktoren sollen **MOTIVIERT SEIN** (nicht nur informiert)

---

## Teil 2: VERHALTENS-ARCHITEKTUR

### 7 Behavioral Design Prinzipien

| # | Prinzip | Quelle | Wo eingesetzt | Erwarteter Effekt |
|---|---------|--------|---------------|-------------------|
| 1 | **Loss Frame** | Kahneman & Tversky (1979) | Opening Hook | 2.25× staerker als Gain Frame |
| 2 | **Peak-End Rule** | Kahneman (2000) | Video Min 23 + Safety Story Min 26 | Bestimmt was erinnert wird |
| 3 | **Implementation Intentions** | Gollwitzer (1999) | Commitment-Karte Min 38 | +42% Umsetzungsrate |
| 4 | **Social Proof** | Cialdini (2001) | Best Practice Werk, Handzeichen | "Wenn DIE das koennen..." |
| 5 | **Reciprocity** | Fehr & Gaechter (2000) | "Was IHR davon habt" | Fairness → Bereitschaft |
| 6 | **Identifiable Victim** | Small (2007) | Safety-Story (1 Person) | 100× staerker als Statistik |
| 7 | **Identity Appeal** | Akerlof & Kranton (2000) | "Leader nicht Direktoren" | Selbstbild aktiviert |

### Neue Reihenfolge (Narrative Arc)

**Bisherig (vermutlich):** Safety → Next → Quality

**Neu (Behavioral Design):**
1. Quality (RECARE) → **DAS PROBLEM** (Spannung aufbauen)
2. Update Next → **DIE LOESUNG** (Hoehepunkt / Peak)
3. Safety & Environment → **DER SINN** (Emotionaler Schluss / End)

**Begruendung:** Peak-End Rule — Menschen erinnern den emotionalen Hoehepunkt und das Ende. Safety am Schluss = bleibt haengen. Next in der Mitte = Peak-Moment (Video/Demo).

---

## Teil 3: DIE 40 MINUTEN IM DETAIL

### Zeit-Architektur

```
00:00-02:00   OPENING HOOK                           2 min
02:00-13:00   BLOCK 1: QUALITY (RECARE)             11 min
13:00-14:00   TRANSITION 1                           1 min
14:00-25:00   BLOCK 2: UPDATE NEXT                  11 min
25:00-26:00   TRANSITION 2                           1 min
26:00-36:00   BLOCK 3: SAFETY & ENVIRONMENT         10 min
36:00-40:00   CLOSING: ONE COMMITMENT                4 min
```

### Aufmerksamkeits-Design

```
100%│     ●                    ●                   ●
    │    / \                  / \                 / \       ●
 80%│   /   \    ●          /   \    ●          /   \     / \
    │  /     \  / \        /     \  / \        /     \   /   \
 60%│ /       \/   \      /       \/   \      /       \_/     \
    │/              \    /              \    /                  \
 40%│                \  /                \  /                    \
    │                 \/                  \/                      \
 20%│ Hook    Q      T    Next      T    Safety        Commit
    └──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──
       0  2  4  6  8 10 12 14 16 18 20 22 24 26 28 30 32 34 36 40

● = Attention Reset (Frage, Ueberraschung, Aktivierung)
```

---

### 00:00 – 02:00 | OPENING HOOK: "Die 40-Millionen-Frage"

**Slide 1:** Schwarzer Screen. Eine Zahl.

```
                        €40'000'000
```

**Walter (steht, kein Pult, freie Buehne):**

> "40 Millionen Euro. Das ist was wir als Gruppe im letzten Jahr verloren haben durch Qualitaetsprobleme, ungeplante Stillstaende und Sicherheitsvorfaelle.
>
> 40 Millionen. Das ist nicht eine Operations-Zahl. Das ist EURE Zahl. Aus euren Werken. Euren Teams.
>
> In den naechsten 40 Minuten zeige ich euch drei Dinge:
> Erstens — wo das Geld hingeht.
> Zweitens — wie wir es zurueckholen.
> Drittens — warum es um mehr als Geld geht.
>
> Und am Ende bitte ich jeden von euch um EINE Sache."

**Behavioral Mechanics:**
- Loss Frame: "verloren" statt "investiert"
- Ownership: "EURE Zahl" — nicht Walter's Problem, ALLER Problem
- Curiosity Gap: "drei Dinge" + "EINE Sache" → Was kommt da?
- Standing, kein Pult → Authority + Energy

**HINWEIS:** Die €40M ist eine Beispielzahl. Walter soll die echte Zahl verwenden (Scrap + Downtime + Safety Costs + Penalties). Wenn keine Gesamtzahl verfuegbar: Schaetzung reicht. Der Schockeffekt ist der Punkt, nicht die Praezision.

---

### 02:00 – 13:00 | BLOCK 1: QUALITY / RECARE — "Wo das Geld hingeht"

**Innere Struktur:** PROBLEM → URSACHE → LOESUNG → IHR

#### 02:00-04:00 — DAS PROBLEM (2 min)

**Slide:** "RECARE Scorecard" — Die Wahrheit in einer Tabelle

| Metrik | Ziel | IST | Gap |
|--------|------|-----|-----|
| Scrap Rate | X% | Y% | 🔴 -Z% |
| Customer Complaints | X ppm | Y ppm | 🔴 -Z |
| OEE | X% | Y% | 🟡 -Z% |
| First Pass Yield | X% | Y% | 🔴 -Z% |

**Walter:**
> "Das Rot in dieser Tabelle — das sind nicht abstrakte Zahlen. Jedes Prozent Scrap ist eine Tonne Kunststoff die ein Kunde nicht bekommt. Und jede Reklamation ist ein Kunde der beim naechsten Mal woanders anfragt."

#### 04:00-06:00 — DIE URSACHE: "Warum passiert das?" (2 min)

**Slide:** Pareto-Diagramm der Top-3 Qualitaetsprobleme

> "80% unserer Qualitaetskosten kommen aus 3 Ursachen:
> 1. [Ursache 1 — z.B. Werkzeugwechsel-Fehler]
> 2. [Ursache 2 — z.B. Prozessparameter-Drift]
> 3. [Ursache 3 — z.B. Rohstoff-Schwankungen]
>
> Das Gute: Alle drei sind LOESBAR.
> Das Schlechte: Nicht von Operations allein."
> ← BRIDGE zu "ihr seid Teil der Loesung"

#### 06:00-09:00 — DIE LOESUNG: RECARE Programm (3 min)

**Slide:** "RECARE — 3 Saeulen"

```
┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│  RE-DUCE    │   │  CARE-FUL   │   │  RE-ACT     │
│  ─────────  │   │  ─────────  │   │  ─────────  │
│  Scrap      │   │  Prozess-   │   │  Schnelle   │
│  reduzieren │   │  disziplin  │   │  Reaktion   │
│  [Massnahmen│   │  [Massnahmen│   │  [Massnahmen│
│   1, 2, 3]  │   │   1, 2, 3]  │   │   1, 2, 3]  │
└─────────────┘   └─────────────┘   └─────────────┘
```

> "Wir haben mit 4 Pilotwerken gestartet. Die Ergebnisse nach 6 Monaten: [konkrete Verbesserung zeigen]. Das funktioniert. Aber nur wenn es UEBERALL laeuft."

#### 09:00-11:00 — IHR: "Was die Gruppe braucht" (2 min)

⚡ **ATTENTION RESET:** Direkte Ansprache — Walter tritt vor, weg von Slides.

> "Jetzt zu euch. RECARE funktioniert nicht als Operations-Programm. Es funktioniert als KULTUR-Programm."

| Was IHR tun koennt | Was IHR davon habt |
|--------------------|--------------------|
| RECARE in euer Werk-Review aufnehmen (1 KPI) | -X% Scrap = €Y mehr Marge in EUREM P&L |
| Quality-Champion im Team benennen | Weniger Eskalationen die EUREN Tag ruinieren |
| Best Practice eures Werks teilen (1 Beispiel) | Sichtbarkeit in der Gruppe ("Werk X hat das geloest") |

> "Ich schicke euch nach dem Meeting eine einfache Vorlage. Ein A4-Blatt. 3 Fragen. 10 Minuten eurer Zeit. Wer mir das bis 15. Maerz zurueckschickt, dessen Werk ist im Q2-Review als Best Practice dabei."

#### 11:00-13:00 — QUICK WIN SHOWCASE (2 min)

**Slide:** "Was Werk [Name] in 3 Monaten geschafft hat"

EIN konkretes Beispiel. EINE Erfolgsgeschichte. MIT Foto des Teams. Idealerweise ein Werk eines anwesenden Direktors → Social Proof + Stolz.

---

### 13:00 – 14:00 | TRANSITION 1 (1 min)

**Walter:**
> "Qualitaet verbessern ist wichtig. Aber noch wichtiger ist: WIE wir in 3 Jahren produzieren. Denn die Welt veraendert sich schneller als unsere Maschinen."

→ Curiosity Gap fuer Block 2

---

### 14:00 – 25:00 | BLOCK 2: UPDATE NEXT — "Wie wir es zurueckholen"

**Innere Struktur:** VISION → REALITAET → ROADMAP → IHR → WOW

#### 14:00-16:00 — VISION: "Das Werk von 2028" (2 min)

**Slide:** Split Screen — HEUTE vs. 2028

| HEUTE | 2028 |
|-------|------|
| Manuelle Umruestung | Automatisch |
| Papier-Checklisten | Digital/Real-time |
| Reaktive Wartung | Predictive |
| Erfahrungswissen im Kopf | Datengestuetzt + Erfahrung |
| Lokal optimiert | Global vernetzt |

> "Das ist kein Science Fiction. Die Technologie existiert. Die Frage ist nur: Schaffen WIR den Uebergang schnell genug, bevor es unsere Wettbewerber tun?"

← Loss Frame: Wettbewerber als Bedrohung

#### 16:00-18:00 — REALITAET: "Wo stehen wir?" (2 min)

⚡ **ATTENTION RESET:** Interaktive Frage

**Slide:** Die 5 Stufen (Walters Stufe-1-bis-5 Modell)

```
┌────┬────┬────┬────┬────┐
│ S1 │ S2 │ S3 │ S4 │ S5 │
│    │    │ ██ │    │    │
│    │ ██ │ ██ │    │    │  ← "Wir sind hier"
│ ██ │ ██ │ ██ │    │    │
└────┴────┴────┴────┴────┘
Basis  Auto  Digital  AI   Full
```

**Walter:**
> "Kurze Frage an euch — ich will keine Praesentation halten, ich will wissen wo IHR steht:
> Wer von euch wuerde sein Werk auf Stufe 1-2 einschaetzen? [Haende] ... Stufe 3? ... Stufe 4?"

→ Aktivierung: Direktoren muessen NACHDENKEN statt zuhoeren
→ Live-Daten: Wie heterogen ist die Gruppe?
→ Soziale Dynamik: Niemand will als Stufe 1 dastehen

#### 18:00-21:00 — ROADMAP: "Die naechsten 18 Monate" (3 min)

**Slide:** Einfache Timeline (NICHT Gantt-Chart!)

```
Q1'26 ──── Q2'26 ──── Q3'26 ──── Q4'26 ──── Q1'27
  │           │           │           │           │
Pilot      Rollout     Standard   Optimize    Next Wave
[3 Werke]  [+8 Werke]  [Global]  [KPIs]     [Stufe 4]
```

> "3 Phasen. Pilot laeuft. Ergebnisse sind [konkret]. Rollout-Welle 2 startet in Q2 — und da kommen EURE Werke."

#### 21:00-23:00 — IHR: "Was ihr als Multiplikatoren tun koennt" (2 min)

| Was IHR tun koennt | Was IHR davon habt |
|--------------------|--------------------|
| EINEN Prozess in eurem Werk fuer Next-Pilot nominieren | Vorsprung: "Early Adopter" → mehr Ressourcen, mehr Aufmerksamkeit |
| Euren besten Techniker fuer Next-Training freistellen (2 Tage) | Euer Team entwickelt sich weiter → weniger Fluktuation |
| Erfahrungen teilen: "Was hat bei euch NICHT funktioniert?" | Ihr vermeidet Fehler die andere schon gemacht haben → spart Wochen |

#### 23:00-25:00 — WOW-MOMENT (2 min)

⚡ **PEAK MOMENT** (Peak-End Rule — hier sitzt der Hoehepunkt!)

**Slide:** Live-Demo oder Video (30 Sekunden)

Etwas ZEIGEN das die Zukunft greifbar macht:
- **Option A:** Kurzes Video einer automatisierten Umruestung
- **Option B:** Dashboard Live-Schaltung zu einem Pilot-Werk
- **Option C:** Vorher/Nachher einer konkreten Verbesserung

> "DAS ist Stufe 4. In [Pilotwerk] laeuft das seit [X Monaten]. Die Umruestzeit ist von [X] auf [Y] Minuten gefallen. Das ist keine PowerPoint-Vision. Das ist Realitaet."

→ SEHEN > HOEREN > LESEN (Emotional Peak)
→ Konkreter Beweis zerstoert Skeptik

---

### 25:00 – 26:00 | TRANSITION 2 (1 min)

**Walter (ruhiger, langsamer, Tonwechsel):**

> "Technologie und Qualitaet sind wichtig. Aber das Wichtigste in unseren Werken sind nicht die Maschinen.
>
> [Pause]
>
> Letztes Jahr hatten wir [X] Sicherheitsvorfaelle. [X] Menschen die abends nicht so nach Hause kamen wie sie morgens gekommen sind."

→ Emotionaler Tonwechsel = Aufmerksamkeits-Reset
→ Personalisierung: "Menschen", nicht "Incidents"

---

### 26:00 – 36:00 | BLOCK 3: SAFETY & ENVIRONMENT — "Warum es um mehr geht"

**Innere Struktur:** MENSCH → DATEN → SYSTEM → IHR

#### 26:00-28:00 — EIN MENSCH (2 min)

⚡ **ATTENTION RESET:** Story statt Slide

Walter erzaehlt EINE Geschichte. Echt. Persoenlich.

> "Im [Monat] ist in [Werk] etwas passiert. [Name/anonymisiert] hat [was passiert ist]. Er/Sie hat [Konsequenz]. Ich habe [ihn/sie/die Familie] besucht.
>
> Was mich dabei am meisten getroffen hat: [Ein konkretes Detail das menschlich beruehrt]"

**Regeln fuer die Story:**
- KEINE SLIDES waehrend der Story
- Walter spricht frei, langsam, mit Pausen
- Das ist der emotionalste Moment der 40 Minuten
- Nach der Story: 3 Sekunden Stille. Dann weiter.

**Falls kein realer Vorfall:** Geschichte eines Beinahe-Unfalls oder die Geschichte eines Mitarbeiters der dank Safety-Kultur einen Unfall VERHINDERT hat (positive Version).

#### 28:00-30:00 — DATEN: "Wo wir stehen" (2 min)

**Slide:** Safety Performance (einfach, klar, emotional codiert)

```
LTIR (Lost Time Injury Rate)

2024: ████████████████  X.X
2025: ████████████      X.X  ↓ [Trend]
2026: ██████████        X.X  ↓
Ziel: ████              X.X

"Jeder Balken ist ein Mensch der verletzt wurde"
```

**Plus Environment KPIs (1 Slide):**
- CO2/Tonne Produkt: Trend
- Recycling-Quote (rPET): Trend
- Energie-Effizienz: Trend

#### 30:00-33:00 — SYSTEM: "Was wir aendern" (3 min)

**Slide:** "3 Prioritaeten Safety & Environment 2026"

1. **[Prioritaet 1 — z.B. Safety Leadership Programm]**
   → Nicht nur Regeln, sondern KULTUR
   → "Safety ist nicht was wir TUN, es ist wer wir SIND"

2. **[Prioritaet 2 — z.B. Near-Miss Reporting ohne Konsequenzen]**
   → Psychologische Sicherheit: Melden = Heldentum, nicht Problem
   → Ziel: 10× mehr Near-Miss Reports = 10× weniger echte Unfaelle

3. **[Prioritaet 3 — z.B. Environment Roadmap 2028]**
   → Konkrete Reduktionsziele
   → Verbindung zu Kunden-Anforderungen (ESG = Geschaeft!)

#### 33:00-36:00 — IHR: Multiplikatoren-Rolle (3 min)

**Walter (persoenlich, direkt):**

> "Safety ist das EINZIGE Thema wo ich keine Kompromisse mache. Nicht bei Kosten. Nicht bei Zeitdruck. Nicht bei Ausreden.
>
> Und das muss von EUCH kommen. Nicht von Regeln. Eure Teams schauen auf EUCH. Wenn IHR den Helm nicht tragt, traegt ihn NIEMAND."

| Was IHR tun koennt | Was IHR davon habt |
|--------------------|--------------------|
| Safety Walk 1×/Woche (15 Min, ohne Ankuendigung) | Ihr SEHT was passiert bevor es passiert |
| Near-Miss des Monats FEIERN (nicht bestrafen!) | Meldekultur entsteht → weniger echte Unfaelle |
| EINE persoenliche Safety-Geschichte erzaehlen (im naechsten Team-Meeting) | Eure Leute spueren: "Der meint es ernst" → Glaubwuerdigkeit |

---

### 36:00 – 40:00 | CLOSING: "EINE SACHE" — Das Commitment

**DAS IST DER WICHTIGSTE TEIL DER GANZEN PRAESENTATION.**

#### 36:00-37:30 — Zusammenfuehrung (90 sek)

**Slide:** Die 3 Themen als EINE Geschichte

```
   QUALITY          →      NEXT           →     SAFETY
   Das Problem              Die Loesung         Der Sinn

   "Weniger Fehler    durch  bessere Systeme   fuer
    sichere Menschen"
```

> "Qualitaet, Innovation und Sicherheit sind nicht drei Themen. Sie sind EINS: Wir bauen Werke in denen Menschen gerne arbeiten und stolz sind auf das was sie herstellen. Das ist die ALPLA-Kultur. Und die braucht EUCH."

#### 37:30-40:00 — ONE COMMITMENT (150 sek)

⚡ **PHYSISCHES COMMITMENT** — Auf dem Tisch liegt eine Karte pro Person

**Karten-Design:**

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  MEIN BEITRAG BIS Q2 2026                               │
│                                                         │
│  QUALITY:  Ich werde ________________________________   │
│                                                         │
│  NEXT:     Ich werde ________________________________   │
│                                                         │
│  SAFETY:   Ich werde ________________________________   │
│                                                         │
│  Name: _________________  Datum: ___________            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Walter:**

> "Auf eurem Platz liegt eine Karte. Drei Zeilen. Fuer jedes Thema: EINE konkrete Sache die ihr bis Q2 macht. Nicht alles. EINE Sache pro Thema.
>
> Nehmt euch 60 Sekunden. Schreibt es auf.
>
> [60 Sekunden Stille — Walter wartet ruhig]
>
> Fertig? Diese Karte behaltet ihr. Ich brauche sie nicht. Aber IHR werdet sie finden wenn ihr im April euer Buero aufraeumt. Und dann wisst ihr: Habe ich es getan? Oder nicht?
>
> [Pause]
>
> Danke fuer eure Aufmerksamkeit. Danke fuer euren Einsatz. Und danke dass ihr nicht nur Direktoren seid, sondern Leader."

**Behavioral Mechanics:**
- Commitment Device: Aufschreiben = 42% hoehere Umsetzung (Gollwitzer 1999)
- "Ich brauche sie nicht" = Autonomie (kein Kontroll-Gefuehl)
- "April Buero aufraeumt" = Mental Time Travel + Selbst-Accountability
- "Leader nicht Direktoren" = Identity Appeal (Akerlof & Kranton)
- Physisches Artefakt: Karte ueberlebt die Praesentation (Slides nicht)

---

## Teil 4: FOLLOW-UP PLAN (nach dem Meeting)

### Woche 1 (28. Februar — 7. Maerz)

| Aktion | Timing |
|--------|--------|
| Follow-up Email mit 1-Seiter Zusammenfassung (3 Themen, 3 Asks) | 28. Februar |
| RECARE-Vorlage angehaengt (das versprochene A4-Blatt) | 28. Februar |
| Persoenliche Nachricht an 2-3 "Champions" die im Meeting aktiv waren | 3. Maerz |

### Q2 Review (April/Mai)

| Aktion | Timing |
|--------|--------|
| RECARE 1-Seiter einsammeln (wer hat bis 15.3 zurueckgeschickt?) | 15. Maerz |
| Best Practice Feature: Werk das am meisten verbessert hat | Q2-Review |
| Zurueckkommen auf Commitment-Karten: "Wer hat seine EINE Sache gemacht?" | Q2-Review |
| Next Rollout: Welche Werke haben nominiert? | Q2-Review |

---

## Teil 5: VORBEREITUNGS-CHECKLISTE

### Bis 25. Februar (2 Tage vor Meeting)

```
☐ ZAHLEN
  ☐ Gesamtkosten Quality/Safety/Downtime berechnen (fuer €-Zahl im Hook)
  ☐ RECARE Scorecard aktualisieren (IST vs. Ziel pro Metrik)
  ☐ Safety LTIR Trend (2024, 2025, YTD 2026, Ziel)
  ☐ Next Stufen-Verteilung (wieviele Werke pro Stufe?)
  ☐ Environment KPIs (CO2, rPET, Energie)

☐ GESCHICHTEN
  ☐ EINE Safety-Geschichte auswaehlen (echt, persoenlich, erzaehlbar)
  ☐ EINE Quality Best Practice (mit Foto/Werk/Person)

☐ DEMO
  ☐ Next Video/Dashboard vorbereiten (30 Sekunden, funktioniert!)
  ☐ Backup-Plan falls Technik nicht funktioniert (Screenshot)
```

### Bis 26. Februar (1 Tag vor Meeting)

```
☐ MATERIALIEN
  ☐ Commitment-Karten drucken (1 pro Teilnehmer + 5 Reserve)
  ☐ RECARE 1-Seiter Vorlage fertigstellen
  ☐ Follow-up Email vorschreiben (Versand am 28.2)
  ☐ Slides finalisieren

☐ PROBEN
  ☐ Opening Hook laut sprechen (2 Min, stehend, frei)
  ☐ Safety-Story laut sprechen (ohne Slides, 2 Min)
  ☐ Timing pruefen (40 Min exakt — Stoppuhr!)
  ☐ Uebergaenge ueben (Tonwechsel bei Transitions!)
  ☐ Commitment-Sequenz ueben ("60 Sekunden Stille" aushalten)
```

### Am Tag des Meetings (27. Februar)

```
☐ Karten auf jeden Platz legen BEVOR Teilnehmer kommen
☐ Slides auf Projektor testen
☐ Video/Demo testen
☐ Wasser bereit (40 Min Reden = trockener Hals)
☐ Stoppuhr/Timer bereit (nicht sichtbar fuer Teilnehmer)
```

---

## Teil 6: SLIDE-UEBERSICHT (14 Slides fuer 40 Minuten)

| Slide | Inhalt | Block | Dauer |
|-------|--------|-------|-------|
| 1 | Schwarzer Screen + €-Zahl | Hook | 2 min |
| 2 | RECARE Scorecard (Tabelle mit Rot/Gelb/Gruen) | Quality | 2 min |
| 3 | Pareto Top-3 Ursachen | Quality | 2 min |
| 4 | RECARE 3 Saeulen | Quality | 3 min |
| 5 | Multiplikatoren-Tabelle Quality | Quality | 2 min |
| 6 | Quick Win Showcase (Foto + Zahlen) | Quality | 2 min |
| 7 | Split Screen HEUTE vs. 2028 | Next | 2 min |
| 8 | 5-Stufen-Modell (Handzeichen-Frage) | Next | 2 min |
| 9 | Timeline Roadmap | Next | 3 min |
| 10 | Multiplikatoren-Tabelle Next | Next | 2 min |
| 11 | Video/Demo (WOW-Moment) | Next | 2 min |
| — | KEINE Slide (Story frei erzaehlt) | Safety | 2 min |
| 12 | LTIR Balkendiagramm + Environment KPIs | Safety | 2 min |
| 13 | 3 Prioritaeten Safety + Multiplikatoren-Tabelle | Safety | 6 min |
| 14 | "QUALITY → NEXT → SAFETY" als EINE Geschichte | Closing | 4 min |

**Total: 14 Slides fuer 40 Minuten = ∅ 2.9 Min/Slide → bewusst WENIG Slides!**

---

## Anhang: Wissenschaftliche Grundlagen

### Loss Aversion in Presentations
- Kahneman, D. & Tversky, A. (1979). Prospect Theory. *Econometrica*, 47(2), 263-291.
- Verluste wiegen 2-2.5× schwerer als gleichwertige Gewinne
- Anwendung: "€40M VERLOREN" statt "€40M Verbesserungspotenzial"

### Peak-End Rule
- Kahneman, D., Fredrickson, B.L., Schreiber, C.A., & Redelmeier, D.A. (1993). When More Pain Is Preferred to Less. *Psychological Science*, 4(6), 401-405.
- Menschen bewerten Erlebnisse nach dem PEAK und dem END, nicht nach der Dauer
- Anwendung: Video/Demo als Peak (Min 23), Safety-Story als End (Min 26)

### Implementation Intentions
- Gollwitzer, P.M. (1999). Implementation intentions: Strong effects of simple plans. *American Psychologist*, 54(7), 493-503.
- "Wenn X, dann Y"-Plaene erhoehen Umsetzung um 42%
- Anwendung: Commitment-Karte mit "Ich werde ___" Format

### Identifiable Victim Effect
- Small, D.A., Loewenstein, G., & Slovic, P. (2007). Sympathy and callousness. *Organizational Behavior and Human Decision Processes*, 102(2), 143-153.
- Eine einzelne identifizierbare Person loest staerkere Reaktion aus als Statistik
- Anwendung: Safety-STORY (1 Person) statt Safety-STATISTIK

### Social Proof
- Cialdini, R.B. (2001). *Influence: Science and Practice*. Allyn & Bacon.
- Menschen orientieren sich am Verhalten aehnlicher Anderer
- Anwendung: Best Practice Werk eines Peer-Direktors zeigen

### Identity Economics
- Akerlof, G.A. & Kranton, R.E. (2000). Economics and Identity. *Quarterly Journal of Economics*, 115(3), 715-753.
- Identitaet beeinflusst Entscheidungen staerker als materielle Anreize
- Anwendung: "Leader, nicht Direktoren" → Selbstbild aktiviert Handlung
