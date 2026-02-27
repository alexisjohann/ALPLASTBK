# UBS Travel-eSIM — Finales Survey-Instrument

> **Evidenzbasiert aus 11 Pre-Analysen:** A1-A3, B1-B3, G1-G4
> **Datum:** 2026-02-25 | **Version:** 1.0
> **Hypothesen:** H_E01–H_E10 (siehe G4)
> **Stichprobe:** n = 200 (Single Group + Moderatoren + Pilot/Final-Vignette)

---

## Executive Summary

Dieses Survey-Instrument misst die Akzeptanz eines UBS-gebrandeten eSIM-Services für Reisende. Das Design integriert zwei theoretische Säulen:

1. **UTAUT2** (B2): Venkatesh 2012 — Price Value, Habit, PE, FC als Haupttreiber
2. **Brand Extension Theory** (B3): Voelckner & Sattler 2006 — Fit, Brand Conviction, Marketing Support

**Erwartetes Modell:** UTAUT2 + Brand Extension Fit, R² = 0.55–0.65

**Kritischste Erkenntnis:** Brand Extension Fit (BFS = 0.405) liegt UNTER dem Schweizer Schwellenwert (0.47, angepasst für analytisches Denken nach Monga & John 2010). Aktive Fit-Verbesserung durch «Travel Banking Ecosystem»-Framing kann BFS auf 0.57 steigern (B3).

**Pilot-Einschränkung:** Die Pilotphase nutzt eine SEPARATE LANDING PAGE beim Drittanbieter (nicht in-App). Dies eliminiert den Habit-Effekt (β = 0.26 → 0.00) und reduziert die Adoptionsrate um ~25%. Pilotergebnisse × 1.33 = geschätzte finale Adoption.

---

## Design-Überblick

**Typ:** Korrelationsstudie mit Within-Subjects-Vignette (Pilot vs. Final)

Im Gegensatz zum Mortgage-Survey (2x2 Experiment) ist der eSIM-Survey korrelational aufgebaut, da:
- Kein natürliches experimentelles Manipulations-Szenario (anders als AI Disclosure)
- Hauptinteresse liegt auf Treiber-Ranking und Fit-Bewertung
- Pilot-vs-Final-Vergleich als Within-Subjects-Vignette integriert

**Moderatoren:**
- Alter (H_C03: linearer Rückgang)
- Sprachregion (H_E10: DE-CH analytischer, FR-CH holistischer)
- UBS-App-Nutzung (H_E02: Habit-Moderator)
- Reisehäufigkeit (H_E01: Need Intensity)

---

## Block F: Reiseverhalten und Kontext (2 Fragen)

### Q_E01 — Reisehäufigkeit

**Fragetext:**
> **DE:** Wie oft reisen Sie pro Jahr ausserhalb der «Roam-like-home»-Zone (EU/EWR)?
> **EN:** How often do you travel outside the 'Roam-like-home' zone per year?

**Format:** Single Choice
**Antwortoptionen:**
1. Nie
2. 1× pro Jahr
3. 2–3× pro Jahr
4. 4+ Mal pro Jahr

**Theoretische Begründung:**
Segmentierungsvariable und Need-Intensity-Moderator. A1-eSIM definiert die Zielgruppe als «Swiss retail customers traveling 1–2x/year outside Roam-like-home zones». B2 zeigt: Price Value (β = 0.28) ist der stärkste Prädiktor — und Price Value steigt mit Reisehäufigkeit (mehr Reisen = mehr Roaming-Kosten = höherer Sparanreiz).

**Analyse:** Segmentierung + Moderator für H_E01. «Nie»-Antworten werden in separater Subgruppe analysiert (Non-User-Perspektive).

**Erwartete Verteilung:** Nie: 25%, 1×: 35%, 2–3×: 30%, 4+: 10%

---

### Q_E02 — Aktuelle Lösung (Status Quo)

**Fragetext:**
> **DE:** Wie lösen Sie heute Ihr Daten-/Roaming-Problem im Ausland?
> **EN:** How do you currently solve your data/roaming problem abroad?

**Format:** Multiple Choice (Mehrfachantworten möglich)
**Antwortoptionen:**
1. Roaming meines Mobilfunkanbieters
2. Lokale SIM-Karte kaufen
3. eSIM-Anbieter (z.B. Airalo, Holafly)
4. WiFi suchen
5. Verzichte auf mobile Daten
6. Andere

**Theoretische Begründung:**
Misst den Status Quo und identifiziert die kompetitive Ausgangslage. B2 zeigt: Habit (β = 0.26) ist der zweitstärkste Prädiktor — wer bereits eSIM nutzt (Option 3), hat niedrigere Wechselbarrieren. G3 Competitor Context zeigt:
- Airalo: 20M+ Nutzer, Marktführer, ab CHF 4.50/GB
- Holafly: Unlimited-Modell, 4.6★ Trustpilot
- Saily: VPN-Bundle, NordVPN-Ökosystem

Option 1 (Roaming) identifiziert die grösste Zielgruppe: Hohe Pain Points, keine Wechselerfahrung → höchstes Potenzial für UBS-eSIM.
Option 4+5 identifiziert Extremnutzer: Verzicht auf Daten = höchste Schmerzgrenze → höchste PV-Sensitivität.

**Analyse:** Wettbewerbs-Baseline. Kreuztabelle mit BI (Q_E09) für Switching-Analyse.

**Erwartete Verteilung:** Roaming: 55%, WiFi: 30%, Lokale SIM: 10%, eSIM: 8%, Verzicht: 15%, Andere: 5%

---

## Block G: Brand Fit und Vertrauen (3 Fragen)

### Q_E03 — Perceived Brand Extension Fit (Kritischste Frage)

**Fragetext:**
> **DE:** Es passt gut, dass UBS einen eSIM-Reisedatenservice anbietet.
> **EN:** It is a good fit for UBS to offer an eSIM travel data service.

**Format:** 7-Punkt-Likert
**Anker:** 1 = Stimme überhaupt nicht zu — 7 = Stimme voll und ganz zu

**Theoretische Begründung:**
**DIE entscheidende Frage des gesamten eSIM-Surveys.** Voelckner & Sattler (2006) zeigen: Fit ist der stärkste Prädiktor für Brand Extension Success (Meta-β = 0.41). B3 berechnet den aktuellen BFS = 0.405 (MODERAT), was auf der 7-Punkt-Skala einem Mittelwert von ~3.8–4.2 entspricht.

**Schweizer Kontext (B3/G2):** Monga & John (2010) zeigen, dass analytische Denker (Deutsch-Schweizer) Fit STRENGER bewerten. Der adjustierte Schwellenwert ist BFS ≥ 0.47 (≈ M ≥ 4.3 auf 7-Punkt-Skala). Der aktuelle Basis-BFS liegt darunter.

**Interpretation der Ergebnisse:**
- M < 3.5 → **Fundamentales Akzeptanzproblem.** Bank → eSIM wird als unpassend empfunden. Strategische Neupositionierung nötig.
- M = 3.5–4.5 → **Fit-Verbesserungsstrategie erforderlich.** B3 empfiehlt 3-Säulen-Ansatz: Travel-Ökosystem-Framing (+0.08), Funktionaler Nutzen-Fokus (+0.05), Testimonials (+0.03). Gesamtpotenzial: BFS 0.405 → 0.57.
- M > 4.5 → **Grünes Licht.** Fit wird akzeptiert. Vollgas bei Launch.

**Analyse:** Primärer Prädiktor für H_E04. SEM-Pfad Fit → BI. Auch: Multi-Group-Analyse nach Sprachregion (H_E10).

**Erwarteter Mittelwert:** M = 3.8–4.5 (Risikozone — unter Schweizer Schwellenwert)

---

### Q_E04 — Brand Conviction (Kompetenz-Transfer)

**Fragetext:**
> **DE:** Ich kann mir vorstellen, dass UBS einen guten Reise-Datenservice liefern kann.
> **EN:** I can imagine that UBS can deliver a good travel data service.

**Format:** 7-Punkt-Likert
**Anker:** 1 = Stimme überhaupt nicht zu — 7 = Stimme voll und ganz zu

**Theoretische Begründung:**
Brand Conviction ist der zweitstärkste Prädiktor (Voelckner & Sattler 2006: Meta-β = 0.36). Er misst, ob Konsumenten UBS die KOMPETENZ zutrauen, einen Telco-Service zu liefern. Im Gegensatz zu Fit (Q_E03), das die KATEGORIE-Passung misst, misst Conviction die FÄHIGKEITS-Wahrnehmung.

B3 zeigt: UBS hat einen hohen Conviction-Score (0.75) aufgrund der globalen Präsenz (60+ Länder) und der Tech-Investitionen. Broniarczyk & Alba (1994): Spezifische Brand Associations sind wichtiger als generelle Einstellung — UBS-Assoziationen (global, premium, tech-affin) transferieren teilweise auf Travel-eSIM.

**Analyse:** SEM-Pfad für Brand Conviction → BI. Diskriminante Validität zu Q_E03 (Fit) prüfen.

**Erwarteter Mittelwert:** M = 4.0–4.8 (moderat — UBS-Kompetenz in Banking anerkannt, Telco unsicher)

---

### Q_E05 — Data Trust (Datenvertrauen)

**Fragetext:**
> **DE:** Wie sehr vertrauen Sie UBS, Ihre persönlichen Reise-Daten sicher zu verwalten?
> **EN:** How much do you trust UBS to securely manage your personal travel data?

**Format:** 7-Punkt-Likert
**Anker:** 1 = Vertraue überhaupt nicht — 7 = Vertraue voll und ganz

**Theoretische Begründung:**
Trust ist ein signifikanter Prädiktor für beide Produkte (H_C01). Für eSIM ist der Effekt schwächer als für Mortgage (β_esim = 0.22 vs. β_mortgage = 0.38), da eSIM ein Low-Stakes-Produkt ist. Aber: Reise-Daten beinhalten Standort-Tracking, was Privacy-Bedenken triggert.

G2 zeigt: 58% der Schweizer fürchten Datenmissbrauch bei KI/digitalen Services (EY 2025). Gleichzeitig ist Datensicherheit eine der stärksten UBS-Markenassoziationen (FINMA-Regulierung, Bankgeheimnis-Tradition). Dies ist einer der 7 Bank-Vorteile für eSIM (G3).

**Analyse:** SEM-Pfad Trust → BI. Erwartung: UBS-Data-Trust > eSIM-Anbieter-Trust (Airalo, Holafly haben kein vergleichbares Trust-Kapital).

**Erwarteter Mittelwert:** M = 4.5–5.5 (UBS-Markvertrauen transferiert stark für Datensicherheit)

---

## Block H: Nutzen und Preis (3 Fragen)

### Q_E06 — Willingness to Pay (Preissensitivität)

**Fragetext:**
> **DE:** Wie viel würden Sie maximal für einen Tages-Datenpass (1 GB) im Ausland bezahlen?
> **EN:** What is the maximum you would pay for a daily data pass (1 GB) abroad?

**Format:** Single Choice
**Antwortoptionen:**
1. CHF 0–2
2. CHF 2–5
3. CHF 5–8
4. CHF 8–12
5. CHF 12+
6. Keine Angabe

**Theoretische Begründung:**
Price Value ist der **stärkste Prädiktor** für eSIM-Adoption (H_E01, β = 0.28). G3 Competitor Pricing:
- Airalo: ~CHF 4.50/GB (Marktführer)
- Holafly: ~CHF 8–10/Tag unlimited
- Saily: ~CHF 3–5/GB
- Roaming (CH-Anbieter): CHF 3–15/MB (!) — Faktor 100–1000× teurer

Die Antwortverteilung zeigt die Zahlungsbereitschaft relativ zum Wettbewerb. Wenn die Mehrheit CHF 5–8 wählt, ist UBS mit einem Premium-Pricing (CHF 7–10) im akzeptablen Bereich.

**Analyse:** Preissensitivitäts-Analyse. Kreuztabelle mit Q_E09 (BI) für Price-Value-Elastizität.

**Erwartete Verteilung:** CHF 0–2: 10%, CHF 2–5: 30%, CHF 5–8: 35%, CHF 8–12: 15%, CHF 12+: 5%, k.A.: 5%

---

### Q_E07 — Performance Expectancy (In-App-Integration)

**Fragetext:**
> **DE:** Wie nützlich wäre es, Ihre Reise-Daten direkt in der UBS Mobile Banking App zu verwalten?
> **EN:** How useful would it be to manage your travel data directly in the UBS Mobile Banking app?

**Format:** 7-Punkt-Likert
**Anker:** 1 = Überhaupt nicht nützlich — 7 = Äusserst nützlich

**Theoretische Begründung:**
PE ist der drittstärkste eSIM-Prädiktor (H_E03, β = 0.22). Diese Frage ist **doppelt wichtig**, weil sie auch den Pilot-vs-Final-Unterschied validiert (H_E09). B2 zeigt:
- Pilot (Landing Page): EE-Penalty = -0.15, Habit = 0.00, Trust-Penalty = -0.10 → Modifier = 0.75
- Final (In-App): EE-Bonus = +0.10, Habit = +0.26, Trust-Bonus = +0.05 → Modifier = 1.00

Wenn Q_E07 (In-App PE) signifikant höher ausfällt als die aktuelle Pilot-Erfahrung, bestätigt dies den 1.33×-Multiplikator für finale Adoption.

**Analyse:** SEM-Pfad für H_E03. Auch: Vergleich PE_in_app vs. PE_current (aus Q_E02 abgeleitet).

**Erwarteter Mittelwert:** M = 5.0–5.5 (hoher Convenience-Wert für App-Nutzer; niedriger für Nicht-UBS-Kunden)

---

### Q_E08 — Roaming-Kosten-Motivation

**Fragetext:**
> **DE:** Wie wichtig ist Ihnen, Roaming-Kosten im Ausland zu sparen?
> **EN:** How important is it for you to save on roaming costs abroad?

**Format:** 7-Punkt-Likert
**Anker:** 1 = Überhaupt nicht wichtig — 7 = Äusserst wichtig

**Theoretische Begründung:**
Misst die Schmerzintensität des aktuellen Roaming-Problems — den «Pain Point», auf den UBS-eSIM als Lösung antwortet. B2 zeigt: PV ist der Top-1-Treiber. G2 bestätigt: Roaming-Kosten ausserhalb Roam-like-home bleiben hoch (CHF 3–15/MB bei Schweizer Anbietern). G3 zeigt: 64% der Konsumenten würden einen Premium für Bank-eSIM zahlen (YouGov 2025).

**Analyse:** Validierung des Price-Value-Konstrukts. Korrelation mit Q_E06 (WTP) erwartet: r > 0.50.

**Erwarteter Mittelwert:** M = 5.5–6.0 (hoch — Roaming-Kosten sind ein bekannter Schweizer Schmerzpunkt)

---

## Block I: Nutzungsbereitschaft und Adoption (3 Fragen)

### Q_E09 — Behavioral Intention (Primäre AV)

**Fragetext:**
> **DE:** Wie wahrscheinlich ist es, dass Sie den UBS eSIM-Service bei Ihrer nächsten Reise nutzen würden?
> **EN:** How likely would you be to use the UBS eSIM service on your next trip?

**Format:** 7-Punkt-Likert
**Anker:** 1 = Sehr unwahrscheinlich — 7 = Sehr wahrscheinlich

**Theoretische Begründung:**
**Primäre abhängige Variable.** Alle H_E-Hypothesen konvergieren hier. Das erwartete R² = 0.55–0.65 mit folgenden Prädiktoren (absteigend):
1. Price Value (β = 0.28)
2. Habit (β = 0.26, nur für In-App-Version)
3. PE (β = 0.22)
4. Brand Extension Fit (β = 0.20)
5. Facilitating Conditions (β = 0.15)

B3 zeigt: BFS Composite Score = 0.87 (SUCCESS ZONE, aber an unterer Grenze). Der Fit-Wert (Q_E03) hat hohe Hebelwirkung auf den Gesamterfolg.

**Analyse:** Primäre DV für SEM. Pfad-Analyse aller UTAUT2-Prädiktoren + Brand Extension Fit.

**Erwarteter Mittelwert:** M = 4.0–4.8 (moderat-positiv; Fit-Bedenken dämpfen ansonsten hohes Interesse)

**Pilot-vs-Final-Interpretation:**
- Pilot-Wert (mit Vignette «Landing Page»): M ≈ 3.5–4.2
- Final-Wert (mit Vignette «In-App»): M ≈ 4.5–5.5
- Differenz validiert den 1.33×-Multiplikator (H_E09)

---

### Q_E10 — Habit / App-Nutzungshäufigkeit

**Fragetext:**
> **DE:** Wie häufig nutzen Sie die UBS Mobile Banking App?
> **EN:** How frequently do you use the UBS Mobile Banking app?

**Format:** Single Choice
**Antwortoptionen:**
1. Täglich
2. Mehrmals pro Woche
3. Wöchentlich
4. Monatlich
5. Selten / Nie
6. Bin nicht UBS-Kunde/in

**Theoretische Begründung:**
Habit ist der zweitstärkste Prädiktor (H_E02, β = 0.26, UTAUT2). **Kritisch:** Der Habit-Effekt ist 0.00 für die Pilot-Phase (separate Landing Page) und 0.26 für die finale In-App-Version. Dies ist einer der drei Faktoren, die den 25%-Pilot-Discount erklären.

G2 zeigt: 65% UBS Mobile Banking Penetration. App-Nutzer mit täglicher/wöchentlicher Nutzung = Kern-Zielgruppe für eSIM-Adoption. G2 zeigt aber auch Digital Fatigue: Tägliche App-Nutzung bei 18–34-Jährigen fiel von 33% auf 9%.

**Analyse:** Moderator für H_E02 + H_E09. Zwei-Gruppen-Vergleich: Heavy Users (täglich/wöchentlich) vs. Light Users (monatlich/selten).

**Erwartete Verteilung:** Täglich: 15%, Mehrmals/Woche: 25%, Wöchentlich: 20%, Monatlich: 15%, Selten/Nie: 15%, Nicht-Kunde: 10%

---

### Q_E11 — Weiterempfehlung (NPS-Proxy)

**Fragetext:**
> **DE:** Würden Sie den UBS eSIM-Service Ihrem Reise-Umfeld weiterempfehlen?
> **EN:** Would you recommend the UBS eSIM service to your travel circle?

**Format:** 7-Punkt-Likert
**Anker:** 1 = Auf keinen Fall — 7 = Auf jeden Fall

**Theoretische Begründung:**
Word-of-Mouth ist ein sekundärer Outcome-Indikator. Venkatesh (2003): SI β = 0.18 — Peer-Empfehlung verstärkt Adoption. B3: Testimonial-Strategie kann BFS um +0.03 steigern. G3 zeigt: eSIM-Markt wächst stark über WoM (Airalo: primär über Reise-Blogger/Social Media gewachsen).

UBS-Vorteil: Reisende empfehlen in konkreten Situationen (Flughafen, Hotellobby) — der «Social Proof am Gate»-Moment.

**Analyse:** Sekundäre DV. Pfad: BI (Q_E09) → WoM (Q_E11). Auch: Vergleich mit Q_E03 (Fit) — hoher Fit → höhere WoM-Bereitschaft.

**Erwarteter Mittelwert:** M = 4.0–5.0 (moderat; abhängig von Fit-Bewertung und Nutzungserfahrung)

---

## Pilot-vs-Final Vignette (Within-Subjects)

**KRITISCH:** Nach Q_E09 werden ZWEI Szenarien präsentiert und Q_E09 wird für jedes Szenario separat beantwortet.

### Vignette A: Pilot-Szenario
> «Stellen Sie sich vor, Sie können über einen Link in der UBS App eine separate Webseite eines Reise-Datenanbieters öffnen. Dort kaufen Sie einen eSIM-Datenpass und aktivieren ihn auf Ihrem Smartphone. UBS vermittelt den Service, aber der eSIM-Anbieter ist ein Drittunternehmen.»

**Erwarteter Mittelwert:** M_pilot = 3.5–4.2

### Vignette B: Final-Szenario
> «Stellen Sie sich vor, Sie können direkt in der UBS Mobile Banking App einen eSIM-Datenpass kaufen und mit einem Klick aktivieren. Alles findet innerhalb der UBS App statt — gleicher Login, gleiche Sicherheit, alles auf einer Rechnung.»

**Erwarteter Mittelwert:** M_final = 4.5–5.5

### Erwartete Differenz
- Δ(Final – Pilot) ≈ +1.0–1.3 auf 7-Punkt-Skala
- Ratio: M_final / M_pilot ≈ 1.25–1.40
- Validiert den B2-Multiplikator von 1.33×

---

## Zusammenfassung: Fragenfluss und Timing

```
SCREENING (30 Sek.)
  └─ Zielgruppenprüfung: Smartphone-Nutzung? Reiseabsicht in nächsten 12 Monaten?

BLOCK F — Reiseverhalten (1 Min.)
  Q_E01 → Reisehäufigkeit
  Q_E02 → Aktuelle Roaming-Lösung

BLOCK G — Brand Fit & Trust (2 Min.)
  Q_E03 → Brand Extension Fit ★ KRITISCHSTE FRAGE
  Q_E04 → Brand Conviction
  Q_E05 → Data Trust

BLOCK H — Nutzen & Preis (2 Min.)
  Q_E06 → Willingness to Pay
  Q_E07 → Performance Expectancy (In-App)
  Q_E08 → Roaming-Kosten-Motivation

BLOCK I — Adoption (2 Min.)
  Q_E09 → Behavioral Intention ★ PRIMÄRE AV
  Q_E10 → UBS App-Nutzungshäufigkeit
  Q_E11 → Weiterempfehlung

PILOT/FINAL VIGNETTE (2 Min.)
  Vignette A (Pilot) → Q_E09_pilot (BI wiederholt)
  Vignette B (Final) → Q_E09_final (BI wiederholt)

DEMOGRAFIE (1 Min.)
  Alter, Geschlecht, Sprachregion (DE-CH/FR-CH/IT-CH),
  Reiseziele (Asien, USA, Afrika, etc.), UBS-Kundenbeziehung

TOTAL: ~10-12 Minuten
```

---

## Analyse-Plan (Kurzfassung)

| Hypothese | Test | Primäre Variablen | Erwarteter Effekt |
|---|---|---|---|
| H_E01 | SEM-Pfad | Price Value → BI | β = 0.28 |
| H_E02 | SEM-Pfad | Habit → BI | β = 0.26 (In-App) / 0.00 (Pilot) |
| H_E03 | SEM-Pfad | PE → BI | β = 0.22 |
| H_E04 | SEM-Pfad | Brand Ext. Fit → BI | β = 0.20 |
| H_E05 | SEM-Pfad | FC → BI | β = 0.15 |
| H_E06 | Pre/Post t-Test | Travel Frame → Fit | Δ = +0.08 |
| H_E07 | Moderation | Brand Prestige × Distance | -38% Distance Penalty |
| H_E08 | Regression | Dilution → Parent Brand | β ≈ -0.05 (n.s.) |
| H_E09 | Paired t-Test | Pilot vs. Final BI | Ratio = 0.75 |
| H_E10 | Multi-Group SEM | DE-CH vs. FR-CH: Fit → BI | β × 1.15 für DE-CH |

---

## Strategische Implikationen (aus allen Pre-Analysen)

### Go/No-Go Kriterien basierend auf Survey-Ergebnissen

| Metrik | Grünes Licht | Gelb (Anpassung nötig) | Rot (Stopp/Pivot) |
|---|---|---|---|
| Q_E03 Fit (M) | > 4.5 | 3.5–4.5 | < 3.5 |
| Q_E09 BI (M) | > 4.5 | 3.5–4.5 | < 3.5 |
| Q_E06 WTP (Modus) | CHF 5–8 | CHF 2–5 | CHF 0–2 |
| Pilot/Final Ratio | > 1.2× | 1.0–1.2× | < 1.0× |
| Q_E04 Conviction (M) | > 4.5 | 3.5–4.5 | < 3.5 |

### Prioritäre Handlungsfelder nach Survey

1. **Wenn Fit < 4.5:** Travel-Ökosystem-Framing aktivieren (B3: +0.08 BFS)
2. **Wenn BI_pilot < 3.5:** Pilotphase verlängern, UX verbessern, In-App-Integration priorisieren
3. **Wenn WTP < CHF 5:** Pricing unterbietet Wettbewerb nicht → Preisanpassung oder Bundling nötig
4. **Wenn Conviction < 4.0:** Kommunikation stärken → «UBS global travel expertise» positionieren
5. **Wenn Pilot/Final < 1.2×:** In-App-Integration bringt weniger Uplift als erwartet → Habit-Annahme überprüfen
