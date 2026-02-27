# Briefing Intervista: Stichprobendesign ECHfP Nullmessung 2026

**Projekt:** BFE Wirkungsmessung «ECHfP – EnergieSchweiz für Private»
**Auftraggeber:** Bundesamt für Energie (BFE) via FehrAdvice & Partners AG
**Datum:** 2026-02-17
**Version:** 2.0 (aktualisiert nach Feedback BFE/CRK/Intervista)
**Kontakt FehrAdvice:** Lucas Amherd (lucas.amherd@fehradvice.com)
**Kontakt BFE:** Abinaya Sivarajah (abinaya.sivarajah@bfe.admin.ch)
**Kontakt CRK:** Oliver Wimmer (oliver.wimmer@cr-k.ch)
**Erhebungsart:** Online-Befragung via Intervista-Panel, 3 Wellen pro Jahr (2026)

---

## 1. Überblick

ECHfP (EnergieSchweiz für Private) ist das Nachfolge-Programm von «erneuerbar heizen» (2021–2025) unter der Dachmarke EnergieSchweiz. Die Nullmessung 2026 erfasst den Ist-Zustand **vor** dem Kampagnenstart, damit spätere Wellen (W2, W3) die Wirkung messen können.

Der Fragebogen besteht aus einem **gemeinsamen Screening-/Intro-Block** und **5 thematischen Modulen**. Jede befragte Person beantwortet genau **1 Modul** (plus den gemeinsamen Block und den Segmentierungsteil).

Die 5 Module decken das gesamte Spektrum der energetischen Gebäudemodernisierung ab: Gesamtmodernisierung (M1), Gebäudehülle (M2), Heizungsersatz (M3), PV/Solarenergie (M4) und E-Mobilität (M5). Während «erneuerbar heizen» primär den Heizungsersatz adressierte, umfasst ECHfP alle relevanten Massnahmen.

**Wichtig:** Die Befragung dient der **Erhebung des Ist-Zustands** und darf nicht selbst als Intervention wirken (keine persuasiven Formulierungen, kein Framing).

```
Quota (Alter/Geschlecht/PLZ) → Screening → Modulzuteilung → 1 Modul → Segmentierung → Demo
```

---

## 2. Gesamtzielgruppe (Screening)

| Kriterium | Definition | Screening-Item |
|-----------|-----------|----------------|
| **Alter** | 25–79 Jahre | Q_ALTER |
| **Geschlecht** | Männlich / Weiblich / Divers | Q_GESCHLECHT |
| **Eigentum** | Wohneigentümer:in (Haus oder STWE), keine Mieter:innen | INTRO1 = 2 oder 3 |
| **Gebäudealter** | Je nach Modul (s. Punkt 3); Screenout bei «weiss nicht» | INTRO2 ≠ 99 |
| **Sprache** | DE / FR / IT | Via Panel + Q_PLZ |

**Screenout-Kriterien:**
- Mieter:innen (INTRO1 = 1) → Screenout
- Gebäudealter «weiss nicht» → Screenout
- Alter < 25 oder > 79 → Screenout

---

## 3. Modulspezifische Zielgruppen

Jede Person, die das Screening besteht, qualifiziert sich für **1 oder mehrere** Module. Die Zuteilung erfolgt nach dem unter Punkt 5 beschriebenen Mechanismus.

### M1 Gesamtmodernisierung

| | |
|---|---|
| **Zielgruppe** | Wohneigentümer:innen mit Gebäude **≥ 5 Jahre** |
| **Filter** | INTRO1 ∈ {2, 3} UND INTRO2 > 1 |
| **BFE-Anforderung (Abi)** | «Analog zum Screening, an Wohneigentümer\*innen gerichtet, deren Immobilien älter als 5 Jahre sind. Eigentümer\*innen mit Gebäude älter als 1900 müssen Teil der Stichprobe sein.» |
| **Hinweis** | Breiteste Zielgruppe — fast alle gescreenten Personen qualifizieren sich |
| **INTRO2-Kategorien** | Vor 1960 / 1960–1979 / 1980–1999 / 2000–2015 / 2016–2021 / Nach 2021 |

### M2 Gebäudehülle

| | |
|---|---|
| **Zielgruppe** | Wohneigentümer:innen mit Gebäude **≥ 25 Jahre** UND Gebäudehülle **nicht** energetisch saniert |
| **Filter** | INTRO2 > 2 UND INTRO6 = 2 (Nein) |
| **BFE-Anforderung (Abi)** | «Nur bei Eigentümer\*innen mit älteren Immobilien sinnvoll, bei welchen die Gebäudehülle noch nicht energetisch saniert ist.» |

### M3 Heizungsersatz (Kernmodul)

| | |
|---|---|
| **Zielgruppe** | Wohneigentümer:innen mit Gebäude **≥ 25 Jahre** UND fossile Heizung (Öl, Gas, Elektro-Direkt) |
| **Filter** | INTRO2 > 2 UND INTRO7 = 2 (Nein, nicht erneuerbar) |
| **BFE-Anforderung (Abi)** | «Gezielt an Wohneigentümer\*innen älterer Immobilien, die ältere fossile Heizsysteme haben. Dabei insb. die ‹Boost-Zielgruppe› von ‹erneuerbar heizen› berücksichtigen.» |
| **Boost-ZG (CRK/Oliver)** | Siehe Punkt 6 — Fossile Heizung, Gebäude ≥ 25 J., gezieltes Screening |
| **Kernmodul** | M3 ist das strategische Kernmodul von ECHfP (55% aller Heizungsersetzungen sind Notfälle mit 2–4 Wochen Entscheidungs-Window) |

### M4 PV / Solarenergie

| | |
|---|---|
| **Zielgruppe** | Wohneigentümer:innen **ohne** PV-Anlage (alle Gebäudealter, inkl. Neubauten) |
| **Filter** | INTRO8 = 2 (Nein, keine PV) |
| **BFE-Anforderung (Abi)** | «Alle Wohneigentümer\*innen, die bislang keine PV-Anlage installiert haben. Auch Eigentümerschaft von Neubauten mitberücksichtigen.» |
| **Hinweis** | Kein Gebäudealter-Filter → auch Neubauten eligible |

### M5 E-Mobilität

| | |
|---|---|
| **Zielgruppe** | Wohneigentümer:innen **mit** E-Auto ODER konkreter Kaufabsicht UND eigenem Parkplatz |
| **Filter** | INTRO5a = 1 (hat E-Auto) ODER INTRO10a = 1 (plant E-Auto-Kauf) |
| **BFE-Anforderung (Abi)** | «Wohneigentümerschaft mit Auto / bestehendem Interesse am Kauf eines Autos und eigenem Parkplatz ohne Ladestation. Auch Neubauten. Es ist nicht unsere Absicht, die Leute weg von ÖV oder anderen Transportmitteln zu Auto zu bewegen.» |
| **Hinweis** | Engste Zielgruppe (~10–15% der Eigentümer:innen). Parkplatz-Frage ggf. als Zusatzfilter. |

---

## 4. Quotierung

### Interlocked Quota auf Gesamtstichproben-Ebene

| Dimension | Kategorien | Quelle |
|-----------|-----------|--------|
| **Geschlecht** | Männlich / Weiblich | BFS Strukturerhebung (Wohneigentümer:innen) |
| **Alter** | 25–39 / 40–59 / 60–79 | BFS Strukturerhebung (Wohneigentümer:innen) |
| **Sprachregion** | DE-CH / FR-CH / IT-CH | BFS (via Q_PLZ → Sprachregion) |

→ **18 Quotenzellen** (2 × 3 × 3), Verteilung gemäss BFS-Daten für Wohneigentümer:innen.

### BFS-Referenzverteilung (indikativ, bitte mit aktuellen BFS-Daten abgleichen)

**Sprachregion (Wohneigentümer:innen):**

| Region | Anteil (ca.) | Ziel-n (Säule 1) |
|--------|-------------|-------------------|
| DE-CH | 72% | 864 |
| FR-CH | 23% | 276 |
| IT-CH | 5% | 60 |
| **Total** | **100%** | **1'200** |

**Alter × Geschlecht (Wohneigentümer:innen):**

| | Männlich | Weiblich | Total |
|---|---------|---------|-------|
| 25–39 | ~12% | ~10% | ~22% |
| 40–59 | ~22% | ~19% | ~41% |
| 60–79 | ~21% | ~16% | ~37% |
| **Total** | **~55%** | **~45%** | **100%** |

⚠️ Exakte Werte bitte aus BFS Strukturerhebung 2024 (oder aktuellste verfügbare Daten) für die Population «Wohneigentümer:innen 25–79 Jahre» entnehmen.

### Keine Quotierung nach

- Gebäudetyp (EFH/MFH/STWE) — wird als Analysevariable erhoben (INTRO3)
- Gebäudealter — wird durch Modulfilter gesteuert
- Kanton — via Sprachregion implizit abgedeckt
- Attitudinales Segment — wird ex post zugewiesen (Segmentierungs-Items SEG_A1–SEG_C3)

### Quota-Items im Fragebogen (am Anfang, VOR Screening)

Gemäss Intervista-Empfehlung müssen die Quota-Items **vor INTRO3** stehen:

1. **Q_ALTER:** Alter in Jahren (oder Geburtsjahr)
2. **Q_GESCHLECHT:** Männlich / Weiblich / Divers
3. **Q_PLZ:** Postleitzahl → Ableitung Sprachregion + Kanton

---

## 5. Modulzuteilung

### Mechanismus: Disproportionale quotierte Zuteilung

Nicht rein zufällig, sondern mit **Mindest-n pro Modul** gesteuert:

```
Person besteht Screening
    │
    ▼
System prüft: Für welche Module ist Person eligible?
    │
    ▼
System prüft: Welches Modul braucht noch Befragte?
    │
    ▼
Zuteilung zu dem Modul mit dem grössten Bedarf
(unter den Modulen, für die Person eligible ist)
```

### Schichtungsvariablen für Monaden

Modulzuteilung geschichtet nach: **Region (DE-CH / FR-CH / IT-CH) × Gebäudetyp (EFH / MFH / STWE)**

### Ziel-n pro Modul (Mindestquoten, Säule 1)

| Modul | Ziel-n (Minimum) |
|-------|-----------------|
| M1 Gesamtmodernisierung | 300 |
| M2 Gebäudehülle | 250 |
| M3 Heizungsersatz | 250 |
| M4 PV / Solarenergie | 300 |
| M5 E-Mobilität | 100 |
| **Total Säule 1** | **1'200** |

### Priorisierung bei Modulzuteilung

1. Module mit dem grössten Delta (Ziel-n minus Ist-n) werden bevorzugt
2. Sobald ein Modul seine Mindestquote erreicht hat, werden neue Eligible bevorzugt zu unterbesetzten Modulen zugeteilt
3. M5 hat strukturell wenig Eligible (~12%), deshalb wird bei M5-Eligibles M5 priorisiert

---

## 6. Stichprobengrösse

### Säule 1: Gesamtstichprobe (über Panel)

**n = 1'200 pro Welle**, quotiert nach Geschlecht × Alter × Sprachregion, mit disproportionaler Modulzuteilung (s. Punkt 5).

### Säule 2: Boost M3 Heizungsersatz

| | |
|---|---|
| **Zusätzliches n** | 250 |
| **Zielgruppe** | Wohneigentümer:innen mit Gebäude ≥ 25 J. UND fossiler Heizung (Öl/Gas/Elektro-Direkt) — die Kernzielgruppe des Heizungsersatz-Moduls |
| **Rekrutierung** | Gezieltes Screening via Panel: Pre-Screening-Frage zu Heizungsart |
| **Begründung** | M3 (Heizungsersatz) ist das Kernmodul von ECHfP. Ohne Boost nur n ≈ 250 → ±6.2 PP (zu ungenau für Trendmessung zwischen Wellen). Mit Boost n = 500 → ±4.4 PP |

### Säule 3: Boost M5 E-Mobilität

| | |
|---|---|
| **Zusätzliches n** | 200 |
| **Zielgruppe** | Wohneigentümer:innen mit E-Auto ODER konkreter Kaufabsicht UND eigenem Parkplatz |
| **Rekrutierung** | Gezieltes Screening via Panel: Pre-Screening-Frage zu Autobesitz/E-Auto |
| **Begründung** | Natürliche Eligibility nur ~12% → ohne Boost n < 100 (nicht auswertbar als eigenständiges Modul) |

### Ergebnis pro Modul und Welle

| Modul | Säule 1 | Boost | **Total n** | **Stichprobenfehler (±PP, 95% KI)** |
|-------|---------|-------|-------------|--------------------------------------|
| M1 Gesamtmodernisierung | 300 | — | **300** | ±5.7 |
| M2 Gebäudehülle | 250 | — | **250** | ±6.2 |
| M3 Heizungsersatz | 250 | +250 | **500** | ±4.4 |
| M4 PV / Solarenergie | 300 | — | **300** | ±5.7 |
| M5 E-Mobilität | 100 | +200 | **300** | ±5.7 |
| **Total pro Welle** | **1'200** | **+450** | **1'650** | **±2.4** (Gesamt) |

### Signifikanz-Berechnung (Zwischenwellen-Vergleich)

Für den Nachweis statistisch signifikanter Veränderungen zwischen zwei Wellen (z.B. W1 → W2):

| Modul | n pro Welle | Detektierbarer Effekt (Δ, 80% Power, α=0.05) |
|-------|-------------|-----------------------------------------------|
| M1 | 300 | ±8.1 PP |
| M2 | 250 | ±8.9 PP |
| M3 | 500 | ±6.3 PP |
| M4 | 300 | ±8.1 PP |
| M5 | 300 | ±8.1 PP |
| Gesamt | 1'650 | ±3.5 PP |

→ **Interpretation:** Bei M3 (n=500) können Veränderungen ab ~6 PP zwischen Wellen als signifikant nachgewiesen werden. Bei kleineren Modulen (n=250–300) sind ~8–9 PP nötig.

### Über 3 Wellen kumuliert

| Modul | n kumuliert | SE kumuliert |
|-------|-----------|-------------|
| M3 Heizungsersatz | 1'500 | ±2.5 PP |
| M1/M4 (je 300) | 900 | ±3.3 PP |
| M2 Gebäudehülle | 750 | ±3.6 PP |
| M5 E-Mobilität | 900 | ±3.3 PP |
| **Gesamt** | **4'950** | **±1.4 PP** |

---

## 7. Gewichtung

| Schritt | Beschreibung |
|---------|-------------|
| **1. Design-Gewichte** | Korrektur für disproportionale Modulzuteilung: Überrepräsentierte Module erhalten Gewicht < 1, unterrepräsentierte > 1 |
| **2. Rim-Weighting (Raking)** | Iterative proportionale Anpassung (IPF) an BFS-Randverteilungen für Wohneigentümer:innen 25–79 Jahre: **Geschlecht × Alter × Sprachregion** |
| **3. Gewichte-Cap** | Maximal 3.0 (begrenzt Varianzinflation, Design Effect ≤ 1.5 angestrebt) |
| **4. Boost-Gewichtung** | Boost-Befragte (M3, M5) werden **separat gewichtet** und nur für modulspezifische Aussagen verwendet — nicht in Gesamtauswertung einbezogen |

### Gewichtungsformel

```
w_final(i) = w_design(i) × w_rim(i)

wobei:
  w_design(i)  = N_eligible_modul(i) / n_modul(i)  [korrigiert Überquotierung]
  w_rim(i)     = IPF-Gewicht an BFS-Ränder (Alter × Geschlecht × Sprachregion)

Trimming: max(w_final) ≤ 3.0
```

---

## 8. Attitudinale Segmentierung (ex post)

Die Befragten werden ex post anhand der Segmentierungs-Items (SEG_A1–SEG_C3) einem von vier attitudinalen Segmenten zugewiesen. Die Segmentierung basiert auf dem ECHfP-Marketingkonzept 1.0.

### 4 Dimensionen (je 1–5 Likert)

| Dimension | Items | Beschreibung |
|-----------|-------|-------------|
| **Orientierung** | SEG_A1, SEG_A2, SEG_A3 | Orientierungsfähigkeit in Bezug auf energetische Modernisierung |
| **Rationalität** | SEG_B1, SEG_B2, SEG_B3 | Analytisch-rationale Entscheidungsfindung |
| **Werte** | SEG_C1, SEG_C2, SEG_C3 | Werte-Orientierung (Umwelt, Nachhaltigkeit) |
| **Misstrauen** | abgeleitet aus T7, W5 | Misstrauen gegenüber Informationen/Institutionen |

### Zuordnungslogik (vereinfacht)

| Segment | Bedingung | Anteil (erwartet) |
|---------|-----------|-------------------|
| **Die Überzeugten** | Orientierung ≥ 4 UND Rationalität ≤ 2 UND Werte ≥ 4 UND Misstrauen ≤ 3 | ~23% |
| **Die Ratlose** | Orientierung ≤ 2 UND Werte ≥ 4 UND Misstrauen ≤ 3 | ~42% |
| **Die Skeptiker** | Rationalität ≥ 4 UND Misstrauen ≥ 4 | ~20% |
| **Die Verhinderer** | Orientierung ≤ 2 UND Werte ≤ 2 UND Misstrauen ≥ 4 | ~15% |

→ Default (wenn keine Regel greift): «Ratlose»

**Hinweis:** Die Segmentierung wird **nicht** zur Quotierung verwendet. Sie dient der Auswertung und ermöglicht segment-spezifische Aussagen (z.B. «Awareness bei Ratlosen ist 35% vs. 68% bei Überzeugten»).

---

## 9. Fragebogen-Struktur (Übersicht)

| Block | Items | Dauer (ca.) | Für wen |
|-------|-------|-------------|---------|
| Quota (Q_ALTER, Q_GESCHLECHT, Q_PLZ) | 3 | 1 min | Alle |
| Screening (INTRO1–INTRO13) | 13 | 3 min | Alle (mit Screenout) |
| Modulzuteilung | System | — | Alle |
| Awareness (A1–A5) | 5 | 2 min | Modul-spezifisch |
| Willingness (W1–W6) | 6 | 2 min | Modul-spezifisch |
| Impact (I1–I2) | 2 | 1 min | Modul-spezifisch |
| Trust (T0–T7) | 8 | 3 min | Modul-spezifisch |
| Zusatzfragen (Z1–Z4) | 4 | 3 min | Modul-spezifisch |
| Segmentierung (SEG_A1–SEG_C3) | 9 | 2 min | Alle |
| **Total** | **~50** | **~17 min** | |

---

## 10. Variante MINIMAL (falls Budget nur für Säule 1)

Falls die Boosts nicht möglich sind:

| Modul | n | SE (±PP) | Einschränkung |
|-------|---|----------|---------------|
| M1 | 300 | ±5.7 | OK |
| M2 | 250 | ±6.2 | Grenzwertig |
| M3 | 250 | ±6.2 | Für Kernmodul zu ungenau |
| M4 | 300 | ±5.7 | OK |
| M5 | 100 | ±9.8 | Nur deskriptiv auswertbar |
| **Total** | **1'200** | **±2.8** | |

⚠️ **Risiko:** M3 ohne Boost kann Veränderungen < 6 PP zwischen Wellen nicht detektieren. M5 ist ohne Boost nicht für eigenständige signifikante Aussagen nutzbar.

---

## 11. Offene Fragen an Intervista

1. **Disproportionale Modulzuteilung:** Ist die quotierte Modulzuteilung (Punkt 5) technisch umsetzbar in eurem System? Oder gibt es eine bevorzugte Alternative?
2. **Boost-Rekrutierung:** Wie aufwändig ist das gezielte Screening für M3 (fossile Heizung) und M5 (E-Auto + Parkplatz)? Können Pre-Screening-Fragen im Panel-Profil hinterlegt werden?
3. **Kosten Boost:** Was kosten die zusätzlichen n = 450 (250 M3 + 200 M5) pro Welle?
4. **IT-Oversampling:** Soll das Tessin überquotiert werden für sprachregionspezifische Aussagen? Falls ja: Welches n empfehlt ihr für IT?
5. **Feldzeit:** Geschätzte Feldzeit für n = 1'650 bei 3 Wellen pro Jahr?
6. **Pretest:** Wir planen einen Pretest mit n = 10–20. Ist das im regulären Prozess enthalten?
7. **BFS-Quotenmatrix:** Können wir die exakten BFS-Randverteilungen für Wohneigentümer:innen 25–79 J. gemeinsam abstimmen?

---

## 12. Nächste Schritte

| # | Aufgabe | Wer | Bis wann |
|---|---------|-----|----------|
| 1 | Rückmeldung zu Machbarkeit disproportionale Zuteilung | Intervista | [Datum] |
| 2 | Offerte Boost M3 + M5 | Intervista | [Datum] |
| 3 | BFS-Quotenmatrix (18 Zellen) abstimmen | FehrAdvice + Intervista | [Datum] |
| 4 | Fragebogen-Übergabe (finale Version v4) | FehrAdvice | [Datum] |
| 5 | Programmierung + Pretest | Intervista | [Datum] |
| 6 | Feldstart Welle 1 | Intervista | [Datum] |

---

*Erstellt von FehrAdvice & Partners AG im Rahmen des BFE-Projekts ECHfP 2026.*
*Version 2.0 — aktualisiert nach Feedback-Runde BFE (Abi), CRK (Oliver), Intervista (Sib)*
