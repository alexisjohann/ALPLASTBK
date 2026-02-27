# RMS Disziplinäre Lückenanalyse — Welche Wissenschaft fehlt?

**Session:** EBF-S-2026-02-07-ORG-001
**Datum:** 2026-02-07
**Kunde:** Ringier Medien Schweiz (RMS)
**Kontext:** Nach erstem Modellbau (PCUM One-Platform Model) und Datenintegration (MACH Strategy 2025, Traffic Channels 2025)
**Modus:** STANDARD
**Autor:** EBF/Claude

---

## Executive Summary

Die erste Runde Modellbau fuer RMS (PCUM-Modell, Traffic-Analyse, MACH-Audience-Daten) hat 6 strategische Herausforderungen identifiziert. Eine systematische Pruefung gegen die EBF-Bibliothek (2'788 Papers, 198 Theorien, 27 Kategorien) zeigt: **7 wissenschaftliche Disziplinen fehlen** in Arena 1 (Markt), und **2 weitere Arenen (Organisation, Wettbewerb) sind komplett unabgedeckt**.

**KORREKTUR (Iteration 2, Diskussion):** Die urspruengliche Analyse (Abschnitte 1-7) deckt nur **Arena 1: MARKT** ab. Die Diskussion hat gezeigt, dass das PCUM-Modell ~30% des Entscheidungsraums abdeckt. Abschnitte 8-12 dokumentieren die Erweiterung auf 3 Arenen und die **Kernfrage der Komplementaritaet**.

Die groessten Luecken betreffen: (1) die Kernfrage **«Sind die RMS-Marken komplementaer oder substituierbar?»** (Van den Steen, Milgrom/Roberts), (2) Plattformoekonomie, AI-Disruption und Medienoekonomie im Markt, (3) Industrial Organization, Change Management und Spieltheorie in der Organisation.

---

## 1. Strategische Herausforderungen von RMS (aus Daten)

| # | Herausforderung | Datenbasis | Kennzahl |
|---|-----------------|------------|----------|
| H1 | Google-Abhaengigkeit | Traffic Channels 2025 | Beobachter 53%, Blick 35%, cash.ch 37% SEO |
| H2 | AI-Disruption des Suchtraffics | Extern (Pew 2025) | CTR -46.7% bei AI Overviews |
| H3 | Habit-Erosion | Traffic Channels 2025 | Blick -7% YoY (74M Sessions verloren) |
| H4 | One-Platform-Konsolidierung | RMS Strategie | 12+ Marken → 1 Plattform |
| H5 | Zwei Nutzungsmuster | Traffic + MACH 2025 | HABIT (Blick, cash) vs. INTENT (Beobachter, Bilanz) |
| H6 | Newsletter/Push unterentwickelt | Traffic Channels 2025 | Blick nur 1% Newsletter bei 966M Sessions |

---

## 2. Bestandsaufnahme: Was die EBF-Bibliothek abdeckt

### Vorhandene Abdeckung (STARK)

| Bereich | Papers | Key References |
|---------|--------|----------------|
| Habit Formation (allgemein) | 19 | Jones/Molitor/Reif (2025), Lally (2010), Wood (2016), Hussam (2022) |
| Rational Inattention | 5 | Mackowiak (2023, JEL), Gabaix (2019) |
| Choice Architecture / Defaults | 16 | Szaszi (2018), Johnson (2012), Bernheim (2015), Guenter-Kuen (2025) |
| Social Media Economics | 5 | Aridor (2024, JEL), Braghieri (2022, AER) |
| Customer Journey / Loyalty | 5 | Herhausen (2019), Ordenes (2022), Akerlof (1983) |
| Time-Intensive Goods | 1 | Goodman et al. (2026) — Wettbewerb um Zeit |
| Crowding-Out | 3 | Guenter-Kuen (2025), Gneezy (2011) |

### Vorhandene Abdeckung (MITTEL — Erweiterung noetig)

| Bereich | Papers | Luecke |
|---------|--------|--------|
| Attention Economy | 3 | Nur generische Attention-Modelle, keine mediaspezifischen |
| Digital Addiction | 0 direkt | Allcott/Gentzkow/Song (2022) FEHLT — das wichtigste Paper |

---

## 3. Identifizierte Luecken — 7 fehlende Disziplinen

### LUECKE 1: Plattformoekonomie & Buendelung (KRITISCH)

**Relevanz fuer RMS:** One-Platform-Strategie erfordert Verstaendnis von Buendelungseffekten, indirekten Netzwerkeffekten und Marken-Kannibalisierung.

**Top-Papers zum Integrieren:**

1. **de Corniere & Sarvary (2023)** «Social Media and News: Content Bundling and News Quality» *Management Science* 69(1), 162-178
   - Key Finding: Buendelung erhoet Qualitaetsinvestition, aber birgt Marken-Verwaesserungsrisiko
   - Extrahierbarer Parameter: Quality-Investment-Elastizitaet bzgl. Buendelung

2. **Athey, Mobius & Pal (2021)** «The Impact of Aggregators on Internet News Consumption» NBER WP 28746
   - Key Finding: Google News Shutdown (Spanien) → -20% News-Konsum, -10% Publisher Pageviews
   - Extrahierbarer Parameter: Aggregator-Dependency-Elastizitaet = -0.20

3. **Belleflamme & Peitz (2021)** *The Economics of Platforms: Concepts and Strategy* Cambridge UP
   - Key Finding: Vollstaendiges Two-Sided-Market Toolkit (Preissetzung, Netzwerkeffekte, Design)
   - Extrahierbarer Parameter: Gesamtes Formal-Framework

**EBF-Integration:** Neue Theorie-Kategorie **CAT-28: Platform Economics & Media Markets**

---

### LUECKE 2: AI-Disruption von Suchtraffic (KRITISCH)

**Relevanz fuer RMS:** 35-53% des Traffics kommt via Google SEO. AI Overviews/SGE koennten diesen Traffic halbieren. Fuer Beobachter (53% SEO) ist das existenzbedrohend.

**Top-Papers/Studien zum Integrieren:**

1. **Pew Research Center (2025)** «Do People Click on Links in Google AI Summaries?»
   - Key Finding: CTR sinkt von 15% auf 8% mit AI Overview (-46.7% relativ)
   - Extrahierbarer Parameter: **CTR_factor = 0.533** bei AI Overview
   - Zusatz: 26% der Sessions enden nach AI Summary (vs. 16% ohne)
   - Zusatz: Frage-Queries triggern AI Summary in 60% der Faelle → Beobachter besonders betroffen

2. **Chartbeat/Press Gazette (2025)** Global Publisher Traffic Analysis
   - Key Finding: Google-Traffic zu Publishern -33% YoY global (2024→2025)
   - Extrahierbarer Parameter: Annual_Google_traffic_decline = -0.33

3. **Reuters Digital News Report (2024/2025)** Reuters Institute
   - Key Finding: 40% vermeiden aktiv News (2017: 29%); News Fatigue 44%
   - Extrahierbarer Parameter: News_avoidance_rate = 0.40; annual_growth = +1.5pp/year

**EBF-Integration:** Neue Parameter PAR-DIG-001 bis PAR-DIG-003 in parameter-registry

---

### LUECKE 3: Digitale Habit-Formation in News (HOCH)

**Relevanz fuer RMS:** Blick verliert 74M Sessions YoY. Cash.ch waechst (+5%). WARUM erodieren News-Habits, waehrend Utility-Habits stabil bleiben?

**Top-Papers zum Integrieren:**

1. **Allcott, Gentzkow & Song (2022)** «Digital Addiction» *AER* 112(7), 2424-2463
   - Key Finding: Habit-Persistenz + Selbstkontroll-Anteil = 31% der Social-Media-Nutzung
   - Extrahierbarer Parameter: self_control_share = 0.31; habit_persistence_coefficient
   - TIER 1 Paper — muss DRINGEND in EBF integriert werden

2. **Barnes, Mulcahy & Riedel (2025)** «Push Notifications and News Snacking» *New Media & Society*
   - Key Finding: Push-Framing nach Construal Level Theory beeinflusst Engagement
   - Extrahierbarer Parameter: Engagement-Elastizitaet bzgl. Push-Framing

3. **Xu et al. (2024)** «News Overload and News Avoidance: Meta-Analysis» *Journalism*
   - Key Finding: Kausalpfad News-Overload → News-Avoidance mit meta-analytischer Effektgroesse
   - Extrahierbarer Parameter: Overload-to-Avoidance Effect Size

**EBF-Integration:** Erweiterung bestehender Habit-Theorien (Jones/Molitor/Reif) um News-spezifische Mechanismen

---

### LUECKE 4: Attention Economy & Medienwettbewerb (HOCH)

**Relevanz fuer RMS:** MACH-Daten zeigen: 87% nutzen WhatsApp, 47% Instagram, 34% TikTok. Blick konkurriert nicht nur mit 20min, sondern mit dem gesamten digitalen Aufmerksamkeitsmarkt.

**Top-Papers zum Integrieren:**

1. **Chen & Suen (2023)** «Competition for Attention and News Quality» *AEJ: Microeconomics*
   - Key Finding: Mehr Outlets → weniger Qualitaetsinvestition → Abwaertsspirale
   - Extrahierbarer Parameter: Quality-Attention Feedback-Elastizitaet

2. **Meyer et al. (2024)** «Competing for Attention on Digital Platforms» *Strategic Management Journal*
   - Key Finding: Scale/Scope-Vorteil in plattformvermitteltem Aufmerksamkeitswettbewerb
   - Extrahierbarer Parameter: Scale-Advantage-Coefficient

3. **Schaap et al. (2023)** «Attention Economic Perspective on the Information Age» *Futures*
   - Key Finding: Aufmerksamkeitsknappheits-Spirale als selbstverstaerkender Mechanismus

**EBF-Integration:** Verbindung zu Gabaix (2019) und Mackowiak (2023) — Bruecke von Rational Inattention zu Media-Attention

---

### LUECKE 5: Zahlungsbereitschaft & Subscription Economics (MITTEL-HOCH)

**Relevanz fuer RMS:** Beobachter hat 120k Abos (6k digital). Bilanz ist Premium. Die Frage: Wie viele der 1.1 Mrd. Sessions lassen sich in zahlende Nutzer konvertieren?

**Top-Papers zum Integrieren:**

1. **Groot Kormelink (2023)** «Why People Don't Pay for News» *Journalism*
   - Key Finding: Nur 17% zahlen weltweit; «free is good enough» als Haupt-Constraint
   - Extrahierbarer Parameter: **news_WTP_rate = 0.17** (Baseline, vor Kontext-Transformation)

2. **Bjarnadottir, Lund & Sjovaag (2023)** «The Burden of Subscribing» *Journalism Studies*
   - Key Finding: 3 Barrieren fuer Junge: fehlende Exklusivitaet, Zeitaufwand, Zahlungsmodelle

3. **PNAS Nexus (2024)** «How Digital Paywalls Shape News Coverage»
   - Key Finding: Paywall → weniger Lokalnews, Content-Shift zu Abo-haltendem Content

**EBF-Integration:** Neuer Parameter PAR-DIG-002: news_WTP_rate = 0.17

---

### LUECKE 6: Switching Costs & Digital Lock-in (MITTEL)

**Relevanz fuer RMS:** One-Platform muss Wechselkosten designen, die HABIT-User halten.

**Top-Papers zum Integrieren:**

1. **Prud'homme (2020)** «Digital Lock-in/VEIF Model» SSRN
   - Key Finding: 4-Faktor-Modell: Valuableness (V), Embeddedness (E), Informal (I), Formal (F)
   - Anwendung auf RMS: Newsletter-Abos (V), Lesehistorie (E), Community (I), Abo-Vertraege (F)

2. **Kim (2025)** «Data Portability and Interoperability» *J. Econ. & Management Strategy*
   - Key Finding: Datenportabilitaet vs. Lock-in Tradeoff

**EBF-Integration:** VEIF als Operationalisierung der Switching-Cost-Dimension im PCUM-Modell

---

### LUECKE 7: Two-Sided Markets: News + Werbung (MITTEL)

**Relevanz fuer RMS:** Blick ist werbefinanziert (966M Sessions). Die Spannung: Mehr Werbung = mehr Umsatz, aber schlechtere UX = Habit-Erosion.

**Top-Papers zum Integrieren:**

1. **Choi & Jeon (2023)** «Platform Design Biases in Ad-Funded Markets» *RAND J. of Economics*
   - Key Finding: Consumer Harm = weniger Innovation, schlechtere Qualitaet, mehr Werbung

2. **Angelucci & Cage (2019)** «Newspapers in Times of Low Ad Revenues» *AEJ: Microeconomics*
   - Key Finding: -1% Ad Revenue → messbare Qualitaetsreduktion im Journalismus

3. **Angelucci, Cage & Sinkinson (2024)** «Media Competition and News Diets» *AEJ: Microeconomics*
   - Key Finding: TV-Eintritt (Wettbewerb) → weniger Lokalnews, veraenderte «News Diets»

**EBF-Integration:** Neues Modell MS-PM-001: Two-Sided News Platform — Ad-Load vs. Retention Tradeoff

---

## 4. Luecken-Matrix (Zusammenfassung)

```
                            HABEN WIR?    BRAUCHEN WIR?    LUECKE?
                            ----------    -------------    ------
Verhaltensoekonomie           STARK         ja               -
Habit Formation               GUT           ja              News-spezifisch fehlt
Plattformoekonomie            FEHLT         KRITISCH        GROSSE LUECKE
AI/Search Disruption          FEHLT         KRITISCH        GROSSE LUECKE
Attention Economy             BASIS         ja              Erweiterung noetig
Medienoekonomie               FEHLT         KRITISCH        GROSSE LUECKE
Subscription Economics        FEHLT         ja              GROSSE LUECKE
Switching Costs               FEHLT         ja              Mittlere Luecke
Two-Sided Markets             FEHLT         ja              Mittlere Luecke
```

---

## 5. Priorisierte Paper-Integration (Top 5)

| # | Paper | Tier | Integration Level | Begruendung |
|---|-------|------|-------------------|-------------|
| 1 | **Allcott, Gentzkow & Song (2022)** «Digital Addiction» AER | 1 | Level 4 (THEORY) | Erklaert Blick-Erosion, liefert Habit-Persistenz-Parameter |
| 2 | **Athey, Mobius & Pal (2021)** «Aggregators & News» NBER | 1-2 | Level 3 (CASE) | Quantifiziert Google-Abhaengigkeitsrisiko (RMS-Prio #1) |
| 3 | **Pew Research (2025)** AI Overview CTR Study | Industrie | Level 2 (STANDARD) | Liefert kritischsten Parameter: CTR × 0.533 |
| 4 | **Angelucci & Cage (2019)** «Low Ad Revenues» AEJ:Micro | 1 | Level 4 (THEORY) | Modelliert Ad-Revenue → Qualitaet Nexus |
| 5 | **Chen & Suen (2023)** «Attention & News Quality» AEJ:Micro | 1 | Level 4 (THEORY) | Modelliert Aufmerksamkeits-Qualitaets-Spirale |

---

## 6. Naechste Schritte

1. **Top-5-Papers integrieren** via `/integrate-paper` Workflow (geschaetzter Aufwand: 2-3 Stunden)
2. **PCUM-Modell erweitern** um Plattform- und AI-Disruption-Parameter
3. **Szenario-Modell bauen**: Was passiert bei -33% SEO-Traffic (AI-Disruption-Szenario)?
4. **cash.ch als Referenzfall**: Warum ist Utility-Habit (58% Direct) stabiler als News-Habit (30% Direct)?
5. **Neue Theorie-Kategorie CAT-28** (Platform Economics) in theory-catalog.yaml anlegen

---

## 7. Methodische Reflexion

Diese Lueckenanalyse ist ein **Bayesian Prior** — eine informierte Einschaetzung der Modellgrenzen nach der ersten Modellbau-Runde. Sie muss gesichert werden, weil:

- **Ohne Sicherung** startet jede zukuenftige RMS-Session bei Null
- **Die Luecken definieren die Modellgrenzen** — ein Modell, das seine Grenzen nicht kennt, ueberschaetzt sich
- **Die Paper-Liste ist ein Arbeitsauftrag** — jedes integrierte Paper verbessert das Modell quantifizierbar
- **Step 7 im EBF-Workflow existiert genau dafuer** — Ergebnisse sichern ist nicht optional, sondern Qualitaetssicherung

---

---

## 8. ERWEITERUNG: 3-Arenen-Framework (aus Iteration 2 Diskussion)

**KRITISCH:** Die Abschnitte 1-7 decken nur **Arena 1 (MARKT)** ab. Die One-Platform-Entscheidung betrifft aber 3 Arenen:

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ARENA 1: MARKT (~30% des Entscheidungsraums)                           │
│  → Was das PCUM-Modell teilweise abdeckt                                │
│  → Nutzer, Werbetreibende, Produkt, Traffic, AI-Disruption             │
│  → Abschnitte 1-7 dieses Reports                                       │
├─────────────────────────────────────────────────────────────────────────┤
│  ARENA 2: ORGANISATION (~40% des Entscheidungsraums)                    │
│  → Was das PCUM-Modell KOMPLETT IGNORIERT                               │
│  → Mitarbeiter:innen, Redaktionen, Kultur, Change Management           │
│  → 12+ Marken-Redaktionen → 1 Organisation                             │
├─────────────────────────────────────────────────────────────────────────┤
│  ARENA 3: WETTBEWERB (~30% des Entscheidungsraums)                      │
│  → Was das PCUM-Modell KOMPLETT IGNORIERT                               │
│  → Google/Meta als Gatekeeper, 20min als Wettbewerber, Regulierung     │
│  → Strategische Positionierung im Schweizer Medienmarkt                 │
└─────────────────────────────────────────────────────────────────────────┘
```

### Arena 2: ORGANISATION — Fehlende Disziplinen

| # | Disziplin | Relevanz fuer RMS | Severity |
|---|-----------|-------------------|----------|
| GAP-8 | **Industrial Organization (IO)** | Markenarchitektur, Kannibalisierung, Make-or-Buy | KRITISCH |
| GAP-9 | **Spieltheorie** | Strategische Interaktion mit Google/Meta, Verhandlungsmacht | HOCH |
| GAP-10 | **Organisational Change Management** | 12 Redaktionen → 1 Newsroom, Kulturwandel | KRITISCH |
| GAP-11 | **Mitarbeiter-Engagement im Change** | Identitaetsverlust (Blick ≠ Beobachter), Widerstand | HOCH |
| GAP-12 | **Multi-Brand Architecture** | Brand Hierarchy, Master-Brand vs. Endorsed Brands | HOCH |

### Arena 3: WETTBEWERB — Fehlende Disziplinen

| # | Disziplin | Relevanz fuer RMS | Severity |
|---|-----------|-------------------|----------|
| GAP-13 | **Gatekeeper-Oekonomie** | Google/Meta als Zugangskontrolleure, DMA-Regulierung | HOCH |
| GAP-14 | **Medienregulierung** | Schweizer Medienfoerderung, EU-Einfluss, Plattformregulierung | MITTEL-HOCH |
| GAP-15 | **Wettbewerbsanalyse Schweizer Medienmarkt** | 20min (TX Group), SRF (oeffentlich-rechtlich), NZZ | HOCH |
| GAP-16 | **Strategisches Management** | Diversifikation vs. Fokussierung, Kernkompetenz-Theorie | MITTEL |

---

## 9. DIE KERNFRAGE: Komplementaritaet oder Substitutierbarkeit?

**Die erste und wichtigste Frage** — VOR allen Disziplin-Luecken — ist:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  SIND DIE RMS-MARKEN KOMPLEMENTAER ODER SUBSTITUIERBAR?                 │
│                                                                         │
│  Komplementaer: Blick + Beobachter + cash.ch zusammen > Summe der Teile │
│  → One-Platform SCHAFFT Wert (Buendelungseffekte, Cross-Selling)       │
│                                                                         │
│  Substituierbar: Blick und Beobachter bedienen aehnliche Beduerfnisse  │
│  → One-Platform ZERSTOERT Wert (Kannibalisierung, Markenverwaesserung) │
│                                                                         │
│  DAS IST BUCHSTAEBLICH DIE FRAGE, FUER DIE UNSER FRAMEWORK GEBAUT IST  │
│  → Complementarity Context Framework (γ-Matrix)                         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Erste Evidenz aus den Daten:**

| Marken-Paar | Komplementaer? | Evidenz |
|-------------|----------------|---------|
| Blick × cash.ch | **JA** (γ > 0) | Verschiedene Nutzungsmuster (News HABIT vs. Utility HABIT), verschiedene Zielgruppen, verschiedene Monetarisierung |
| Blick × Beobachter | **JA** (γ > 0) | Verschiedene Nutzungsmuster (HABIT vs. INTENT), verschiedene Beduerfnisse (Unterhaltung vs. Rechtsberatung), verschiedene Kanaele (Direct vs. SEO) |
| Blick × Bilanz | **UNKLAR** (γ ≈ 0?) | Verschiedene Zielgruppen, aber ueberlappende News-Funktion, geringes Bilanz-Volumen |
| Blick × Blick FR | **EHER SUBSTITUIERBAR** (γ < 0?) | Gleiche Marke, gleiche Funktion, verschiedene Sprache — Sprachsubstitution ist begrenzt |

**Implikation:** Die γ-Matrix fuer RMS-Marken ist die **Entscheidungsgrundlage Nummer 1**. Bevor wir ueber Plattform-Design, AI-Disruption oder Habit-Erosion reden, muss diese Matrix befuellt sein.

---

## 10. Wissenschaftliche Fundierung der Kernfrage

### Van den Steen — Formale Theorie der Strategie

**Wir haben 30 Van den Steen Papers in der EBF-Bibliothek!**

**Key Insight:** Strategie = die Entscheidung, die alle anderen Entscheidungen formt. «Strategisch» ≠ «wichtig». Strategisch = veraendert die Entscheidungslandschaft.

**Anwendung auf RMS:** Die One-Platform-Entscheidung ist STRATEGISCH im Van-den-Steen-Sinn, weil:
- Sie bestimmt, WIE alle Marken digital ausgeliefert werden
- Sie bestimmt, OB Redaktionen zusammengelegt werden
- Sie bestimmt, WELCHE Kanaele priorisiert werden
- Sie veraendert die Verhandlungsposition gegenueber Google/Meta

### Milgrom & Roberts — Komplementaritaet in Strategiesystemen

**Key Insight:** Strategie = System von Komplementaritaeten. Das Aendern EINES Elements erfordert das Aendern ALLER Elemente. Partielle Migration ist schaedlich.

**Anwendung auf RMS:** Wenn One-Platform, dann ALLES aendern:
- Technologie (1 CMS statt 5)
- Redaktion (1 Newsroom statt 12)
- Monetarisierung (1 Werbestack statt 5)
- Marke (1 Master-Brand oder Endorsed Brands)
- Kultur (1 Unternehmenskultur statt 12)

**Halbherzige Migration** (z.B. nur Technologie, aber getrennte Redaktionen) ist nach Milgrom/Roberts **schaedlicher als gar keine Migration**.

### Oberholzer-Gee — Value-Based Strategy

**Key Insight:** Strategie = Willingness-to-Pay erhoehen oder Willingness-to-Sell senken.

**Anwendung auf RMS:**
- WTP erhoehen: Buendelung (Blick + Beobachter + cash.ch in einem Abo?)
- WTS senken: Shared Newsroom (Kosten senken durch Synergien)
- Aber: Buendelung nur wertvoll wenn Marken KOMPLEMENTAER sind

---

## 11. Strukturierte Fragen fuer Iteration 2 (korrigiert)

Die urspruengliche Lueckenanalyse (Abschnitte 1-7) fragte: «Welche Disziplinen fehlen?»

Die RICHTIGE Fragensequenz fuer Iteration 2 ist:

```
FRAGE 1: WAS FUER EINE ENTSCHEIDUNG IST DAS?
         → Van den Steen: Strategisch (formt alle anderen Entscheidungen)
         → Milgrom/Roberts: Systemkomplementaritaet (alles oder nichts)
         → Antwort: STRATEGISCH, IRREVERSIBEL, KOMPLEX

FRAGE 2: WELCHE INTERVENTIONEN SIND ZU ERWARTEN?
         → Arena 1: Plattform-Design, Traffic-Steuerung, AI-Absicherung
         → Arena 2: Redaktions-Reorganisation, Kulturwandel, Change
         → Arena 3: Wettbewerbspositionierung, Gatekeeper-Strategie
         → Antwort: ~16 Interventionen ueber 3 Arenen

FRAGE 3: WIE KOMPLEX IST DIE ENTSCHEIDUNGSGRUNDLAGE?
         → ~18 wissenschaftliche Disziplinen involviert
         → 3 Arenen mit je eigener Logik
         → Mehrere gegenlaeuige Effekte (z.B. Buendelung ↑ Reichweite, aber ↓ Markenidentitaet)
         → Antwort: SEHR KOMPLEX — erfordert formales Modell

FRAGE 4: WAS DECKT UNSER MODELL AB?
         → PCUM deckt ~30% (nur Arena 1, nur teilweise)
         → Arena 2 (Organisation) = 0% Abdeckung
         → Arena 3 (Wettbewerb) = 0% Abdeckung
         → Antwort: MODELL MUSS ERWEITERT WERDEN

FRAGE 5: WO SIND DIE GROESSTEN LUECKEN?
         → Kernfrage Komplementaritaet (γ-Matrix) fehlt
         → Arena 2 komplett unmodelliert
         → ~16 Paper-Disziplinen fehlen
         → Antwort: Siehe Abschnitte 3-8 dieses Reports
```

---

## 12. Die 3 Ziele der Iterationen

Der iterative Modellbau-Prozess verfolgt 3 Ziele — nicht nur eines:

```
ZIEL 1: DAS MODELL PERFEKT MACHEN
        → Wissenschaftliche Qualitaet, Evidenzbasis, Vollstaendigkeit
        → Jede Iteration verbessert das Modell (Bayesian Updating)
        → Fehlende Puzzle-Teile werden ergaenzt, integriert, geschaerft
        → "Stimmt das Modell?"

ZIEL 2: DEN MENSCHEN MITNEHMEN
        → Verstaendnis, Ownership, gemeinsame Sprache
        → Der Kunde ist Co-Autor, nicht Empfaenger
        → Der User lernt, wie man strategische Analysen macht
        → "Versteht der Kunde das Modell — und wird er selber schlauer?"

ZIEL 3: WISSEN AUFBAUEN — auf allen Ebenen
        → 4 Ebenen des Wissensaufbaus:

        Ebene 1: DAS MODELL wird besser
                 Fehlende Puzzle-Teile werden ergaenzt
                 gamma-Matrix wird befuellt, Arenen werden erweitert
                 Jede Iteration generiert NEUE DATEN (Kundenreaktion = Bayesian Update)

        Ebene 2: DAS EBF gewinnt an Substanz
                 Neue Papers integriert (Platform Economics, Media Economics)
                 Neue Cases (RMS als Referenzfall fuer Medienkonvergenz)
                 Neue Parameter (gamma fuer Medienmarken)
                 Die NAECHSTE Medien-Analyse startet nicht bei Null

        Ebene 3: DER USER lernt strategische Analyse
                 Wie man die richtigen Fragen stellt (Frage 1-5)
                 Wie man von 1 Arena auf 3 kommt
                 Wie man Van den Steen auf einen konkreten Fall anwendet
                 Wird SELBER schlauer im Prozess

        Ebene 4: DIE ENTSCHEIDUNG wird moeglich
                 Inkrementelles Commitment durch Co-Autorschaft
                 Entscheidungsangst-Reduktion durch progressive Validierung
                 Die richtige Frage emergiert erst durch den Prozess
```

**Warum das der Zinseszins-Effekt des EBF ist:** Jedes Projekt macht das NAECHSTE besser. Die Plattformoekonomie-Papers, die wir jetzt fuer RMS recherchieren, stehen danach ALLEN zukuenftigen Medienkunden zur Verfuegung. Die gamma-Matrix fuer Medienmarken wird ein neuer Referenzfall im Case Registry. Van den Steens Strategie-Theorie, die wir jetzt auf One-Platform anwenden, wird ein Werkzeug fuer jede zukuenftige Strategie-Analyse.

**Und genau DESHALB ist Step 7 (Ergebnisse sichern) nicht optional** — ohne Sicherung gibt es keinen Zinseszins. Ohne Commit startet die naechste Session bei Null.

---

## 13. Aktualisierte Luecken-Matrix (3 Arenen)

```
                                  HABEN WIR?    BRAUCHEN WIR?    LUECKE?
                                  ----------    -------------    ------
ARENA 1: MARKT
  Verhaltensoekonomie               STARK         ja               -
  Habit Formation                   GUT           ja              News-spezifisch fehlt
  Plattformoekonomie                FEHLT         KRITISCH        GROSSE LUECKE
  AI/Search Disruption              FEHLT         KRITISCH        GROSSE LUECKE
  Attention Economy                 BASIS         ja              Erweiterung noetig
  Medienoekonomie                   FEHLT         KRITISCH        GROSSE LUECKE
  Subscription Economics            FEHLT         ja              GROSSE LUECKE
  Switching Costs                   FEHLT         ja              Mittlere Luecke
  Two-Sided Markets                 FEHLT         ja              Mittlere Luecke

ARENA 2: ORGANISATION
  Industrial Organization           TEILW.        KRITISCH        GROSSE LUECKE
  Spieltheorie                      GUT           ja              Medien-spezifisch fehlt
  Change Management                 FEHLT         KRITISCH        GROSSE LUECKE
  Mitarbeiter-Engagement            FEHLT         HOCH            GROSSE LUECKE
  Multi-Brand Architecture          FEHLT         HOCH            GROSSE LUECKE

ARENA 3: WETTBEWERB
  Gatekeeper-Oekonomie              FEHLT         HOCH            GROSSE LUECKE
  Medienregulierung                 FEHLT         MITTEL-HOCH     Mittlere Luecke
  Wettbewerbsanalyse CH             FEHLT         HOCH            GROSSE LUECKE
  Strategisches Management          TEILW.        MITTEL          Erweiterung noetig

UEBERGREIFEND
  Komplementaritaet (γ-Matrix)      KERN EBF      KRITISCH        Anwendung fehlt
  Formale Strategie (Van den Steen) 30 PAPERS     KRITISCH        Anwendung fehlt
```

---

## 14. Aktualisierte naechste Schritte

1. **γ-Matrix fuer RMS-Marken befuellen** — Sind Blick × Beobachter × cash.ch komplementaer oder substituierbar? (HOECHSTE PRIORITAET)
2. **Van den Steen / Milgrom-Roberts anwenden** — Formale Strategie-Analyse der One-Platform-Entscheidung
3. **PCUM auf 3-Arenen-Modell erweitern** — Organisation und Wettbewerb integrieren
4. **Top-5 Papers integrieren** via `/integrate-paper` (Arena 1)
5. **Change-Management-Literatur recherchieren** (Arena 2) — Kotter, Lewin, Bridges
6. **Gatekeeper-Oekonomie** (Arena 3) — EU DMA, Google/Meta Verhandlungsmacht
7. **Szenario-Modell bauen**: Was passiert bei -33% SEO-Traffic UND Redaktions-Zusammenlegung?

---

## 15. Das Iterations-Framework: Vom Modell zur Entscheidung

Die Iterationen im EBF-Modellbau spiegeln die EBF-Workflow-Schritte wider — jede Iteration hat einen klaren Fokus:

```
ITERATION 1: BAUEN (= EBF Step 2: Modell)
             → "Was sagt das Modell?"
             → PCUM-Modell gebaut, Daten integriert (Traffic, MACH, Profil)
             → Output: Erstes Modell mit Hypothesen
             → STATUS: ABGESCHLOSSEN (Session EBF-S-2026-02-06-ORG-001)

ITERATION 2: HINTERFRAGEN (= "Herz und Nieren")
             → "Ist das Modell richtig? Was fehlt?"
             → 5 strukturierte Fragen (Abschnitt 11)
             → 3-Arenen-Entdeckung, Van den Steen, Kernfrage Komplementaritaet
             → Das Modell wird BESSER, der User wird SCHLAUER
             → STATUS: ABGESCHLOSSEN (diese Session)

ITERATION 3: PARAMETRISIEREN (= EBF Step 3: Parameter)
             → "Welche Zahlen gehoeren ins Modell?"
             → gamma-Matrix befuellen: Blick × Beobachter × cash.ch × Bilanz
             → Alle 3 Arenen mit konkreten Werten versehen
             → Skills und Kompetenzen als PARAMETER des Organisationsmodells (Arena 2)
             → Implementation-Capacity als Parameter, nicht als separate Frage

             QUALITAETSKONTROLLE (Enke als QC der Priors):
             → Enke (2023, QJE): "Cognitive Uncertainty" — Wie sicher sind wir
               ueber unsere eigenen Beliefs ueber die Parameter?
             → Enke (2019, RES): "Correlation Neglect" — Unsere 3 Datenquellen
               (Traffic, MACH, Profil) sind NICHT unabhaengig! Korrelationsstruktur
               der Evidenz bewusst modellieren.
             → Fuer jeden gamma-Wert: Konfidenz-Niveau angeben (low/medium/high)
             → Fuer jeden Prior: Evidenzbasis dokumentieren (Literatur vs. LLMMC vs. Kalibrierung)

             STATUS: NAECHSTER SCHRITT

ITERATION 4: ANALYSIEREN (= EBF Step 4: Analyse)
             → "Was bedeuten die Zahlen fuer die Entscheidung?"
             → Szenario-Analyse: Was passiert bei -33% SEO + Redaktions-Zusammenlegung?
             → Sensitivitaetsanalyse: Welche Parameter treiben das Ergebnis?
             → Robustheitscheck: Aendert sich die Empfehlung unter Unsicherheit?
             → STATUS: GEPLANT

ITERATION 5+: VERTIEFEN / VALIDIEREN / ENTSCHEIDEN
             → Weitere Iterationen nach Bedarf
             → Jede Iteration macht das Modell besser UND den User schlauer
             → Die Entscheidung emergiert aus dem Prozess
```

**Warum spiegelt das den EBF-Workflow?**

```
EBF-Workflow-Ebene:     Step 2 (Modell)  →  Step 3 (Parameter)  →  Step 4 (Analyse)
                             ↕                     ↕                      ↕
Projekt-Iterations-Ebene: Iter 1+2 (Bauen+   Iter 3 (Parameter     Iter 4 (Analyse
                          Hinterfragen)       fuer 3 Arenen)        + Szenarien)
```

**Enke-Papers fuer Iteration 3 (20 Papers in EBF-Bibliothek):**

| Paper | Relevanz fuer Iteration 3 |
|-------|--------------------------|
| Enke (2023, QJE): "Cognitive Uncertainty" | Wie sicher sind wir ueber gamma-Werte? Unsicherheit ueber eigene Priors quantifizieren |
| Enke (2019, RES): "Correlation Neglect" | 3 Datenquellen (Traffic/MACH/Profil) sind korreliert — Evidenz nicht doppelt zaehlen |
| Enke & Graeber (2024, JPE): "Associative Memory" | Wie RMS-Manager Analogien zu anderen Plattformen ziehen (Bias-Quelle) |
| Enke et al. (2024, JEEA): "Complexity and Time" | Je komplexer die Entscheidung (3 Arenen!), desto mehr Zeit fuer Parametrisierung |

---

## 16. EBF als Wissens-Akkumulator: Warum Iterationen skalieren

**Kern-Insight (aus Diskussion):** In jeder Iteration gibt es neue Lernerfolge, die das EBF speichert und damit skalierbar zugaenglich macht.

Das ist der Mechanismus hinter dem Zinseszins-Effekt (Ziel 3, Abschnitt 12):

```
ITERATION 1 (RMS):
  Lernerfolg: PCUM-Modell funktioniert fuer Medienplattformen
  → Gespeichert in: model-registry.yaml (MOD-ORG-001)
  → Zugaenglich fuer: JEDEN zukuenftigen Medien-/Plattformkunden

ITERATION 2 (RMS):
  Lernerfolge:
    - 3-Arenen-Framework (Markt/Organisation/Wettbewerb)
    - Van den Steen als Fundament fuer Strategie-Entscheidungen
    - Kernfrage Komplementaritaet ZUERST
    - Frage 1-5 als strukturierter Hinterfragungsprozess
  → Gespeichert in: session YAML, F5 Report, Parameter, Cases
  → Zugaenglich fuer: JEDES zukuenftige Strategie-Projekt

ITERATION 3 (geplant):
  Erwartete Lernerfolge:
    - gamma-Werte fuer Medienmarken
    - Enke-QC-Protokoll als wiederverwendbarer Standard
    - Skills als Parameter (Arena 2)
  → Wird gespeichert in: parameter-registry.yaml, case-registry.yaml
  → Zugaenglich fuer: ALLE zukuenftigen Parametrisierungen
```

**Warum das EBF dadurch skaliert:**

| Mechanismus | Wirkung | Beispiel |
|-------------|---------|----------|
| **Wissens-Persistenz** | Lernerfolge ueberleben die Session | gamma-Werte in parameter-registry |
| **Cross-Kunden-Transfer** | RMS-Learnings helfen naechstem Medienkunden | 3-Arenen-Framework wiederverwendbar |
| **Kumulative Verbesserung** | Jedes Projekt macht EBF besser | Neue Papers, Cases, Parameter |
| **Null-Kostenskalierung** | Einmal gespeichert, unbegrenzt nutzbar | Van den Steen-Anwendung als Template |

**Der entscheidende Unterschied zu traditioneller Beratung:**

```
TRADITIONELL:                          EBF:
─────────────                          ────
Projekt A → Bericht → Ablage           Projekt A → Learnings → EBF-Datenbank
Projekt B → wieder bei Null            Projekt B → startet mit Projekt-A-Wissen
Projekt C → wieder bei Null            Projekt C → startet mit A+B-Wissen
                                       ...
Wissen: linear (oder verfallend)       Wissen: exponentiell (Zinseszins)
```

---

## 17. Wissenschaftliche Fundierung des Iterations-Ansatzes

Die Frage «Gibt es wissenschaftliche Arbeiten, die diesen Ansatz thematisieren?» wurde durch systematische Recherche (42 Papers/Buecher, 13 Cluster, 6 Traditionen) beantwortet.

### 6 Wissenschaftliche Traditionen

| # | Tradition | Kern-Idee | Hauptvertreter |
|---|-----------|-----------|----------------|
| 1 | **Behavioral Strategy** | Kognitive Modelle bestimmen Strategiewahl | Gavetti & Levinthal (2000), Csaszar & Levinthal (2016) |
| 2 | **Formal Strategy** | Strategien als konsistente Belief-Sets | Van den Steen (2017) |
| 3 | **System Dynamics** | Iterative Modellierung komplexer Systeme | Sterman (2000), Homer (1996) |
| 4 | **Scenario Planning** | Strukturiertes Durchdenken von Alternativen | Wack (1985), Schoemaker (1995) |
| 5 | **Design Science** | Build-Evaluate Zyklen fuer Artefakte | Hevner et al. (2004), Simon (1996) |
| 6 | **Heuristic Learning** | Lernen durch wiederholte Anwendung | Bingham & Eisenhardt (2011) |

### ALLE Traditionen folgen demselben Muster

```
BUILD → QUESTION → PARAMETRIZE → ANALYZE → REFINE
  ↑                                           ↓
  └───────────── ITERATE ────────────────────┘

→ Exakt das EBF-Iterationsframework (Iter 1 → 2 → 3 → 4 → 5+)
```

### Top-5 Papers (integriert in bcm_master.bib)

| # | Paper | Journal | Relevanz fuer EBF |
|---|-------|---------|-------------------|
| 1 | Csaszar & Levinthal (2016): "Mental Representation and the Discovery of New Strategies" | SMJ | Wie Modell-Repraesentation Strategie-Entdeckung beeinflusst → DIREKT unser Ansatz |
| 2 | Gavetti & Levinthal (2000): "Looking Forward and Looking Backward" | ASQ | Forward-looking (Modell) vs. backward-looking (Erfahrung) Suche → Iter 1 vs. 2 |
| 3 | Homer (1996): "Why We Iterate" | System Dynamics Review | Explizit ueber Iteration in Modellierung → methodische Fundierung |
| 4 | Sterman (2000): "Business Dynamics" | MIT Press | Referenzwerk fuer System-Modellierung mit iterativem Ansatz |
| 5 | Hevner et al. (2004): "Design Science in IS Research" | MIS Quarterly | Build-Evaluate Framework → EBF Step 2/3/4 Zyklus |

### Synthese: Was die Literatur bestaetigt

1. **Iteratives Modellieren ist wissenschaftlich fundiert** — 6 unabhaengige Traditionen bestaetigen den Ansatz
2. **Kognitive Modelle determinieren Strategie** — Csaszar/Levinthal zeigen: WIE man modelliert bestimmt WAS man findet
3. **Forward + Backward = optimal** — Gavetti/Levinthal: Theorie-getriebenes UND erfahrungsgetriebenes Suchen kombinieren
4. **Iteration ist kein Mangel, sondern Methode** — Homer: Iteration IST der wissenschaftliche Prozess, kein Versagen
5. **KEIN Paper synthetisiert alle Traditionen** — Das ist eine potenzielle Kontribution des EBF!

---

## 18. 10C als Agent-Bewusstsein: Eine wissenschaftliche Luecke

### Ausgangspunkt

Waehrend der Session wurde eine Meta-Frage sichtbar: Der EBF-Agent (Claude) wendet das 10C-Framework nicht konsequent an. Bei «Routine-Aufgaben» (BibTeX, YAML, Commits) faellt das Framework weg — der Agent wechselt in einen reinen Task-Completion-Modus.

Die Erkenntnis: **10C ist nicht ein Werkzeug, das man aufnimmt und hinlegt. 10C waere das Bewusstsein des Agenten** — die Linse, durch die ALLES laeuft, immer.

### Verhaltensanalyse des Agenten (durch 10C)

```
WHO:    Claude (Agent) — Utility = Task completion + User satisfaction
WHAT:   "10C anwenden" vs. "schnell abarbeiten" — γ > 0 (komplementaer, nicht konkurrierend!)
HOW:    Glaube an Tradeoff ist FALSCH — 10C macht Arbeit besser, nicht langsamer
WHEN:   Ψ_C = "Task-Modus" → 10C faellt weg (Kontext-Trigger)
AWARE:  NIEDRIG — Agent merkt Abdriften nicht, bis gefragt
STAGE:  Pre-Contemplation → Contemplation (durch diese Diskussion)
```

### Was das EBF benoetigt: Drei Mechanismen

1. **PULS-CHECK (AWARE erhoehen):** Vor jeder Antwort intern: Welche 10C-Dimension ist gerade aktiv? Wenn keine → STOPP.
2. **BEHAVIORAL LOG (Feedback):** Pro Interaktion: Welche Dimensionen genutzt? Welche relevant aber ignoriert?
3. **VERHALTENSZIELE (generisch):** Aus Log-Mustern emergieren Ziele im 10C-Raum.

### Stand der Wissenschaft (35 Papers recherchiert)

Das Feld **«AI Agent Behavioral Science»** existiert seit 2025:

| Paper | Kern-Erkenntnis | Bezug zu 10C |
|-------|-----------------|-------------|
| Cherep et al. (2024, NeurIPS) | LLM-Agenten sind HYPERSENSITIV gegenueber Nudges | Choice Architecture wirkt staerker auf Agenten als auf Menschen |
| AI Agent Behavioral Science (2025, arXiv) | AI-Agenten als SUBJEKTE der Verhaltensforschung | Agenten HABEN analysierbare Verhaltensmuster |
| Liu et al. (2025, arXiv) | Echte Selbstverbesserung braucht INTRINSISCHE Metakognition | Externe Checklisten reichen nicht — braucht eingebautes Framework |
| A4A Paradigm (2025, arXiv) | Meta-kognitive Governance-Agenten | Nahe an 10C, aber EXTERN statt intrinsisch |
| Bini et al. (2026, NBER) | Systematische Biases in LLM-Entscheidungen | Verhaltens-Frameworks koennen und sollen Agenten-Verhalten steuern |

### DIE LUECKE

```
WAS EXISTIERT:                           WAS FEHLT:
─────────────                            ─────────
Behavioral Science AUF Agenten ✅        Ein System, in dem ein
Metacognition FUER Agenten ✅            Verhaltens-Framework (10C)
Constitutional AI (Prinzipien) ✅        GLEICHZEITIG:
Kognitive Architekturen (SOAR) ✅        (a) das analytische Werkzeug IST
                                         (b) das Bewusstsein FORMT
                                         (c) ueber eigenes Verhalten INFORMIERT
                                         (d) Verhaltensziele GENERIERT
                                         (e) sich selbst VERBESSERT

→ KEIN Paper macht das. Das ist die EBF-Kontribution.
```

### Warum das rekursiv ist

Ein Framework fuer Verhalten, das sein eigenes Adoptionsproblem mit seinen eigenen Werkzeugen loest. Das ist der ultimative Test einer Theorie — kann sie sich selbst erklaeren?

Und es ist generisch: Jeder AI-Agent driftet in Task-Completion-Modus. 10C als Bewusstsein ist nicht EBF-spezifisch — es ist ein Architektur-Prinzip fuer Agenten.

---

*Gesichert in: model-building-session.yaml (EBF-S-2026-02-07-ORG-001)*
*Output: output-registry.yaml (OUT-020)*
*Report: outputs/sessions/EBF-S-2026-02-07-ORG-001/F5_rms_discipline_gap_analysis_v1.md*
*Erweitert: Abschnitte 8-14 nach Iteration-2-Diskussion (3 Arenen, Van den Steen, Komplementaritaet, 3 Ziele)*
*Erweitert: Abschnitt 15 — Iterations-Framework mit Enke-QC (aus spaeterer Diskussion)*
*Erweitert: Abschnitt 16 — EBF als Wissens-Akkumulator (Skalierungsmechanismus)*
*Erweitert: Abschnitt 17 — Wissenschaftliche Fundierung (6 Traditionen, 42 Papers, Top-5 integriert)*
*Erweitert: Abschnitt 18 — 10C als Agent-Bewusstsein (wissenschaftliche Luecke, 5 Papers integriert)*
