# APPENDIX: Medien-Datenbank Österreich

## Systematisches Media Monitoring für politische Kommunikation

**Projekt:** SPÖ Strategische Kommunikation
**Version:** 1.0
**Datum:** 4. Februar 2026
**Referenz:** DB-SPO-MEDIEN-001
**SSOT:** `data/customers/spo/database/MEDIEN_DATENBANK.yaml`

---

## 1. EXECUTIVE SUMMARY

Die Medien-Datenbank ist ein strukturiertes System zur:
- **Prognose** von Medienreaktionen vor SPÖ-Kommunikation
- **Erfassung** tatsächlicher Reaktionen (automatisiert, Volltext)
- **Validierung** der Prognose-Genauigkeit (Brier Score)
- **Akkumulation** von Learnings für zukünftige Prognosen

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  PROGNOSE              →    EREIGNIS    →    VALIDIERUNG               │
│  (vor Kommunikation)        (SPÖ agiert)     (Medien reagieren)        │
│                                                                         │
│  ┌─────────────────┐       ┌──────────┐      ┌─────────────────┐       │
│  │ P(neg) = 65%    │  ──►  │ Inflation│  ──► │ Krone: negativ  │       │
│  │ P(neu) = 25%    │       │ 2% Meldung│     │ Standard: pos.  │       │
│  │ P(pos) = 10%    │       └──────────┘      │ ORF: neutral    │       │
│  └─────────────────┘                         └─────────────────┘       │
│         │                                            │                  │
│         │                                            │                  │
│         └────────────────►  BRIER SCORE  ◄───────────┘                 │
│                             (Genauigkeit)                               │
│                                  │                                      │
│                                  ▼                                      │
│                         ┌─────────────────┐                            │
│                         │    LEARNINGS    │                            │
│                         │ (für nächstes   │                            │
│                         │  Thema nutzen)  │                            │
│                         └─────────────────┘                            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. THEORETISCHE GRUNDLAGE

### 2.1 Warum Medienreaktionen prognostizierbar sind

Medien sind keine neutralen Informationsvermittler, sondern **Organisationen mit Geschäftsmodellen**. Diese Geschäftsmodelle erzeugen systematische, vorhersagbare Reaktionsmuster.

#### Die Boulevard-Gleichung

```
Aufmerksamkeit = f(Negativität × Emotionalität × Personalisierung)
```

**Verhaltensökonomische Basis:**

| Bias | Mechanismus | Implikation für Prognose |
|------|-------------|--------------------------|
| **Negativity Bias** | Negatives wird 3-5× stärker wahrgenommen als Positives | Boulevard wird IMMER negativen Winkel finden |
| **Loss Aversion (λ ≈ 2.25)** | Verluste wiegen schwerer als Gewinne | "Trotzdem teuer" > "Endlich besser" |
| **Availability Heuristic** | Leicht abrufbare Beispiele dominieren | Supermarkt-Preis > Statistik Austria |
| **Peak-End Rule** | Spitzen und Ende bleiben im Gedächtnis | Inflationshoch 2022 bleibt präsent |
| **Fundamental Attribution Error** | Situationen werden Personen zugeschrieben | Regierung schuld an Schlechtem, nicht an Gutem |

### 2.2 Die 6 Reframing-Strategien (RF-1 bis RF-6)

Wenn Boulevard über Regierungserfolge berichten "muss", wendet er systematisch eine oder mehrere dieser Strategien an:

```
┌─────────────────────────────────────────────────────────────────────────┐
│  REFRAMING-STRATEGIEN BEI REGIERUNGSERFOLGEN                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  RF-1: TROTZDEM-FRAME                     Häufigkeit: ████████████ 85%  │
│  "2% Inflation – aber IM SUPERMARKT..."                                 │
│  Mechanismus: Erfolg anerkennen, dann relativieren                      │
│                                                                         │
│  RF-2: ZU-SPÄT-FRAME                      Häufigkeit: ████████░░░ 65%  │
│  "JETZT erst? Nach 2 Jahren Leiden!"                                    │
│  Mechanismus: Timing kritisieren statt Ergebnis                         │
│                                                                         │
│  RF-3: NICHT-IHR-VERDIENST-FRAME          Häufigkeit: ██████░░░░░ 50%  │
│  "Globale Entwicklung, nicht Regierung"                                 │
│  Mechanismus: Attribution auf externe Faktoren                          │
│                                                                         │
│  RF-4: ABLENKUNGSMANÖVER-FRAME            Häufigkeit: █████░░░░░░ 40%  │
│  "Inflation sinkt – aber MIGRATION explodiert!"                         │
│  Mechanismus: Anderes negatives Thema hochziehen                        │
│                                                                         │
│  RF-5: WER-ZAHLT-FRAME                    Häufigkeit: ████░░░░░░░ 35%  │
│  "Inflation runter – aber SCHULDEN explodieren!"                        │
│  Mechanismus: Versteckte Kosten suchen                                  │
│                                                                         │
│  RF-6: ELITE-VS-VOLK-FRAME                Häufigkeit: ███████░░░░ 60%  │
│  "SIE feiern sich – WIR leiden weiter"                                  │
│  Mechanismus: Erfolg als Elite-Projekt framen                           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.3 Strategische Konsequenz

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  ❌ NICHT TUN:                                                          │
│     Boulevard überzeugen wollen                                         │
│     → Strukturell unmöglich (Geschäftsmodell)                           │
│                                                                         │
│  ✅ STATTDESSEN:                                                        │
│     Boulevard als WETTER behandeln, nicht als Gegner                    │
│     → Prognose erstellen, darauf vorbereiten, nicht bekämpfen           │
│                                                                         │
│  🎯 FOKUS:                                                              │
│     Eigene Kanäle + Qualitätsmedien für Swing-Voters                    │
│     → Dort ist Überzeugung möglich                                      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. DATENBANK-ARCHITEKTUR

### 3.1 Drei-Säulen-Struktur

```
MEDIEN_DATENBANK.yaml
│
├── TEIL 1: STATISCHE MEDIENPROFILE
│   └── 16 österreichische Medien mit:
│       • Reichweite (Print + Online)
│       • Politische Einordnung (1-10 Skala)
│       • Eigentümerstruktur
│       • Schlüssel-Journalisten
│       • Reaktionsmuster (historisch)
│       • SPÖ-Relevanz
│
├── TEIL 2: DYNAMISCHES THEMEN-TRACKING
│   └── Pro Thema:
│       • Kontext (Anlass, Bedeutung, Positionen)
│       • Integrierte Analysen (5 pro Thema)
│       • Prognosen pro Medium
│       • Tatsächliche Reaktionen (Volltext)
│       • Auswertung (Brier Score, Learnings)
│
└── TEIL 3: AGGREGIERTE LEARNINGS
    └── Erkenntnisse aus abgeschlossenen Trackings:
        • Allgemeine Muster
        • Medium-spezifisch
        • Themen-spezifisch
```

### 3.2 Medien-Profil Schema

Jedes Medium wird mit folgenden Attributen erfasst:

```yaml
- id: MED-AT-001
  name: "Kronen Zeitung"
  kurzname: "Krone"
  typ: "Boulevard"
  format: "Print + Online"

  reichweite:
    print_taeglich: 1800000
    online_unique_user: 4500000
    reichweite_prozent: 38.0
    trend: "stabil"

  politische_einordnung:
    spektrum: "rechtspopulistisch-opportunistisch"
    skala: 6  # 1=links, 5=mitte, 10=rechts
    stabilitaet: "volatil"
    historisch:
      - periode: "2017-2019"
        tendenz: "FPÖ-freundlich"
      - periode: "2025-heute"
        tendenz: "Regierungs-skeptisch"

  eigentuemerstruktur:
    eigentuemer: "Mediaprint (Funke/Dichand)"
    einfluss_politik: "hoch"

  charakteristika:
    storytelling_stil: "emotional, personalisiert, vereinfachend"
    bevorzugte_frames:
      - "Elite vs. Volk"
      - "Der kleine Mann"
      - "Trotzdem-Relativierung"
    trigger_themen:
      - "Migration"
      - "Teuerung"
      - "Pensionen"

  reaktionsmuster:
    bei_regierungserfolgen: "Relativierung, Trotzdem-Frame"
    bei_regierungsfehlern: "Maximale Empörung, Personalisierung"

  spoe_relevanz:
    wichtigkeit: "kritisch"
    erreichbare_segmente:
      - "Ältere Arbeiter"
      - "Pensionisten"
    risiko: "Narrativ-Setzung gegen SPÖ-Erfolge"
    chance: "Hohe Reichweite bei SPÖ-Kernzielgruppen"
```

### 3.3 Erfasste Medien (16)

| ID | Medium | Typ | Reichweite | Einordnung | SPÖ-Relevanz |
|----|--------|-----|------------|------------|--------------|
| MED-AT-001 | Kronen Zeitung | Boulevard | 38% | 6 (rechtspop.) | kritisch |
| MED-AT-002 | oe24/Österreich | Boulevard | 15% | 7 (rechts) | kritisch |
| MED-AT-003 | Heute | Boulevard | 12% | 5.5 (mitte-rechts) | hoch |
| MED-AT-004 | Der Standard | Qualität | 8% | 3.5 (mitte-links) | hoch |
| MED-AT-005 | Die Presse | Qualität | 5% | 6.5 (konservativ) | mittel |
| MED-AT-006 | Kurier | Qualität | 6% | 5 (mitte) | mittel |
| MED-AT-007 | News | Magazin | 3% | 5 (mitte) | mittel |
| MED-AT-008 | ORF | TV/Online | 45% | 5 (neutral) | sehr hoch |
| MED-AT-009 | Servus TV | TV | 8% | 7 (rechts) | hoch |
| MED-AT-010 | exxpress | Online | 2% | 8 (rechts) | niedrig |
| MED-AT-011 | kontrast.at | Online | 1% | 2 (links) | eigen |
| MED-AT-012 | Kleine Zeitung | Regional | 5% | 6 (konservativ) | mittel |
| MED-AT-013 | Salzburger Nachr. | Regional | 2% | 6 (konservativ) | niedrig |
| MED-AT-014 | Tiroler Tagesz. | Regional | 2% | 6.5 (konservativ) | niedrig |
| MED-AT-015 | OÖ Nachrichten | Regional | 3% | 6 (konservativ) | mittel |
| MED-AT-016 | Vorarlb. Nachr. | Regional | 1% | 5.5 (liberal-kons.) | niedrig |

---

## 4. PROGNOSE-METHODIK

### 4.1 Prognose-Schema

Für jedes Medium wird eine strukturierte Prognose erstellt:

```yaml
prognose:
  medium_id: MED-AT-001  # Krone
  prognose_datum: "2026-02-04"

  erwartetes_framing:
    primaer: "Trotzdem teuer"
    sekundaer: "Elite vs. Volk"
    headline_varianten:
      - "2% Inflation – aber IM SUPERMARKT zahlen wir DRAUF!"
      - "Regierung feiert – Pensionistin Hermi (74) weint beim Einkauf"

  erwartete_argumente:
    - "Kumulative Teuerung seit 2022"
    - "Einzelschicksale mit Fotos"
    - "Gefühlte vs. gemessene Inflation"

  erwartetes_timing: "Sofort + Follow-up-Serie"

  prognose_wahrscheinlichkeiten:
    negativ: 85
    neutral: 10
    positiv: 5

  konfidenz: "hoch"  # absolut/sehr_hoch/hoch/mittel/niedrig
```

### 4.2 Prognose-Kalibrierung

Die Wahrscheinlichkeiten werden basierend auf:

1. **Historisches Reaktionsmuster** des Mediums
2. **Themen-Affinität** (Wirtschaft, Migration, etc.)
3. **Aktuelle politische Konstellation**
4. **Eigentümer-/Redaktionslinie**
5. **Timing** (Wochentag, andere News-Konkurrenz)

### 4.3 Konfidenz-Skala

| Konfidenz | Definition | Wann verwenden |
|-----------|------------|----------------|
| absolut | 100% sicher | Medium hat feste ideologische Linie (exxpress) |
| sehr_hoch | 90%+ | Klares historisches Muster |
| hoch | 75-90% | Gutes Verständnis, geringe Varianz |
| mittel | 50-75% | Unsicherheiten vorhanden |
| niedrig | <50% | Neues Medium oder unvorhersehbares Verhalten |

---

## 5. AUTOMATISIERTE ERFASSUNG

### 5.1 Volltext-Erfassungs-Schema

Nach dem Ereignis werden tatsächliche Reaktionen automatisch erfasst:

```yaml
tatsaechliche_reaktion:
  # Basis-Identifikation
  datum: "2026-02-05T08:30:00"
  artikel_url: "https://www.krone.at/3312345"

  # Inhalt (automatisch extrahiert)
  headline: "2% Inflation – aber IM SUPERMARKT..."
  lead: "Statistik jubelt, Bürger leiden"
  volltext: |
    [Kompletter Artikeltext - automatisch via Scraping]
  word_count: 487

  # Metadaten
  autoren: ["Klaus Herrmann"]
  zitierte_personen: ["FPÖ-Sprecher X", "Pensionistin Hermi"]

  # Analyse
  framing: "Trotzdem"  # RF-1
  tonalitaet: "negativ"
  sentiment_score: -0.72  # -1.0 bis +1.0

  # Automatisierung
  auto_fetch:
    timestamp: "2026-02-05T09:00:00"
    methode: "RSS"
    erfolgreich: true
```

### 5.2 RSS/Scraping-Konfiguration

```yaml
automatisierung:
  medien_urls:
    MED-AT-001:  # Krone
      rss: "https://www.krone.at/rss"
      scrape_pattern: "article.story-content"
    MED-AT-002:  # oe24
      rss: "https://www.oe24.at/rss"
      scrape_pattern: "div.article-body"
    MED-AT-004:  # Standard
      rss: "https://www.derstandard.at/rss"
      scrape_pattern: "div.article-body"

  trigger_keywords:
    - "Inflation"
    - "Teuerung"
    - "Babler"
    - "SPÖ"

  fetch_intervall_minuten: 30
  speicher_volltext: true
  max_artikel_pro_medium: 5
```

### 5.3 Automatische Sentiment-Analyse

Der Sentiment-Score wird berechnet aus:
- Wort-Level Sentiment (positive/negative Wörter)
- Satz-Level Kontext
- Headline-Gewichtung (2×)
- Zitat-Attribution (wer sagt was)

```
sentiment_score ∈ [-1.0, +1.0]

-1.0 ────────── 0 ────────── +1.0
  │              │              │
  │              │              │
"vernichtend"  "neutral"    "positiv"
```

---

## 6. VALIDIERUNG & LEARNINGS

### 6.1 Brier Score

Der Brier Score misst die Prognose-Genauigkeit:

```
Brier Score = (Prognose - Ergebnis)²

Beispiel:
- Prognose: P(negativ) = 0.85
- Ergebnis: negativ (= 1)
- Brier Score = (0.85 - 1)² = 0.0225 ✓ (gut)

Interpretation:
- Brier = 0.00: Perfekte Prognose
- Brier < 0.10: Sehr gut
- Brier < 0.25: Akzeptabel
- Brier > 0.25: Verbesserungsbedarf
```

### 6.2 Auswertungs-Schema

```yaml
auswertung:
  prognose_korrekt: true
  abweichung_beschreibung: "Headline exakt wie prognostiziert"
  brier_score: 0.0225
  learning: |
    Krone verwendet bei Wirtschaftsthemen IMMER den Trotzdem-Frame.
    Personalisierung (Pensionistin) war wie erwartet.
    RF-6 (Elite vs. Volk) weniger prominent als erwartet.
```

### 6.3 Learning-Aggregation

Nach jedem abgeschlossenen Tracking werden Learnings kategorisiert:

```yaml
learnings:
  allgemeine_muster:
    - learning_id: LRN-001
      beschreibung: "Boulevard verwendet bei JEDEM Erfolgsthema mindestens einen RF-Frame"
      konfidenz: "sehr hoch"
      basiert_auf: ["TRK-2026-02-04-001"]

  medium_spezifisch:
    MED-AT-001:  # Krone
      - "RF-1 (Trotzdem) ist Default-Frame"
      - "Personalisierung IMMER mit Foto"
      - "Timing: Sofort + 3-Tage-Follow-up-Serie"

  themen_spezifisch:
    wirtschaft:
      - "Gefühlte vs. gemessene Inflation ist Standard-Argument"
      - "Supermarkt-Beispiele haben höchste Resonanz"
```

---

## 7. WORKFLOW: NEUES THEMA TRACKEN

### 7.1 Schritt-für-Schritt

```
┌─────────────────────────────────────────────────────────────────────────┐
│  WORKFLOW: Neues Thema in Medien-Datenbank                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  SCHRITT 1: THEMA ANLEGEN                                               │
│  ─────────────────────────────────────────────────────────────────────  │
│  • Neue ID vergeben: TRK-YYYY-MM-DD-NNN                                 │
│  • Kontext dokumentieren (Anlass, Bedeutung, Positionen)                │
│  • Mit ANFRAGEN_REGISTER verknüpfen                                     │
│                                                                         │
│  SCHRITT 2: ANALYSEN ERSTELLEN                                          │
│  ─────────────────────────────────────────────────────────────────────  │
│  • Wording (3-Ebenen-Argumentation)                                     │
│  • Interview-Simulation (falls TV-relevant)                             │
│  • Wählerbefragung (LLMMC Simulation)                                   │
│  • Boulevard-Analyse (6 RF-Frames)                                      │
│  • Medienprognosen (alle relevanten Medien)                             │
│                                                                         │
│  SCHRITT 3: PROGNOSEN ERFASSEN                                          │
│  ─────────────────────────────────────────────────────────────────────  │
│  • Pro Medium: Framing, Argumente, Timing, P(neg/neu/pos)               │
│  • Konfidenz angeben                                                    │
│  • Headline-Varianten formulieren                                       │
│                                                                         │
│  SCHRITT 4: EREIGNIS ABWARTEN                                           │
│  ─────────────────────────────────────────────────────────────────────  │
│  • SPÖ-Kommunikation erfolgt                                            │
│  • Automatisches Monitoring aktiviert (RSS, Scraping)                   │
│                                                                         │
│  SCHRITT 5: REAKTIONEN ERFASSEN (AUTOMATISIERT)                         │
│  ─────────────────────────────────────────────────────────────────────  │
│  • Volltext automatisch extrahieren                                     │
│  • Sentiment-Score berechnen                                            │
│  • Framing identifizieren                                               │
│                                                                         │
│  SCHRITT 6: VALIDIERUNG                                                 │
│  ─────────────────────────────────────────────────────────────────────  │
│  • Prognose vs. Realität vergleichen                                    │
│  • Brier Score berechnen                                                │
│  • Learnings dokumentieren                                              │
│                                                                         │
│  SCHRITT 7: LEARNINGS AGGREGIEREN                                       │
│  ─────────────────────────────────────────────────────────────────────  │
│  • Allgemeine Muster aktualisieren                                      │
│  • Medium-spezifische Erkenntnisse ergänzen                             │
│  • Themen-spezifische Learnings hinzufügen                              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 7.2 Checkliste

```
NEUES THEMA - CHECKLISTE

☐ TRK-ID vergeben
☐ Kontext dokumentiert (Anlass, Bedeutung, Positionen)
☐ ANF-Referenz verknüpft
☐ Wording erstellt (ANA-XXX-001)
☐ Interview-Simulation erstellt (falls relevant) (ANA-XXX-002)
☐ Wählerbefragung simuliert (ANA-XXX-003)
☐ Boulevard-Analyse erstellt (ANA-XXX-004)
☐ Medienprognosen erstellt (ANA-XXX-005)
☐ Alle relevanten Medien mit Prognosen versehen
☐ Automatisierung konfiguriert (Keywords, RSS)
☐ Commit + Push

NACH EREIGNIS:

☐ Reaktionen automatisch erfasst
☐ Volltext gespeichert
☐ Sentiment analysiert
☐ Framing identifiziert
☐ Brier Score berechnet
☐ Learnings dokumentiert
☐ Aggregierte Learnings aktualisiert
☐ Tracking als "abgeschlossen" markiert
```

---

## 8. INTEGRATION MIT ANDEREN SYSTEMEN

### 8.1 Verknüpfung mit ANFRAGEN_REGISTER

Jedes Tracking referenziert eine strategische Anfrage:

```yaml
# In MEDIEN_DATENBANK.yaml:
themen_tracking:
  - id: TRK-2026-02-04-001
    anfrage_referenz: "ANF-2026-02-04-001"  # ← Verknüpfung

# In ANFRAGEN_REGISTER.yaml:
datenbanken:
  - id: "DB-SPO-MEDIEN-001"
    verknuepfte_anfragen:
      - anfrage_id: "ANF-2026-02-04-001"
```

### 8.2 Verknüpfung mit Wählersimulationen

Die Wählerbefragung (ANA-XXX-003) liefert Segment-Reaktionen, die mit Medien-Reichweiten korreliert werden können:

```
Segment-Medien-Matrix:

                    Krone    Standard    ORF
Kern-SPÖ            ███░░    █████       ████░
Enttäuschte Mitte   ████░    ███░░       █████
FPÖ-Affine          █████    █░░░░       ███░░
Junge Städter       █░░░░    █████       ██░░░
```

### 8.3 Verknüpfung mit Strategiebriefing

Die 3-Ebenen-Argumentation aus dem Wording füttert die Medien-spezifische Ansprache:

| Medium-Typ | Primär-Level | Sekundär-Level |
|------------|--------------|----------------|
| Boulevard | L1 (Fakten) | L2 (Werte) |
| Qualität | L3 (Bedeutung) | L1 (Fakten) |
| TV | L2 (Werte) | L1 (Fakten) |
| Eigene Kanäle | Alle drei | - |

---

## 9. METRIKEN & KPIs

### 9.1 Prognose-Qualität

| Metrik | Berechnung | Zielwert |
|--------|------------|----------|
| Durchschnittlicher Brier Score | Σ Brier / n | < 0.15 |
| Tonalitäts-Trefferquote | Korrekte Tonalität / n | > 80% |
| Framing-Trefferquote | Korrekter Haupt-Frame / n | > 70% |
| Timing-Genauigkeit | Korrekte Timing-Prognose / n | > 75% |

### 9.2 Tracking-Vollständigkeit

| Metrik | Berechnung | Zielwert |
|--------|------------|----------|
| Erfassungsrate | Erfasste Artikel / Erwartete Artikel | > 90% |
| Volltext-Rate | Artikel mit Volltext / Erfasste Artikel | > 95% |
| Sentiment-Rate | Artikel mit Sentiment / Erfasste Artikel | 100% |

### 9.3 Learning-Akkumulation

| Metrik | Berechnung | Zielwert |
|--------|------------|----------|
| Learnings pro Tracking | Dokumentierte Learnings / Trackings | > 3 |
| Medium-Coverage | Medien mit Learnings / Alle Medien | > 80% |
| Themen-Coverage | Themen mit Learnings / Alle Themen | 100% |

---

## 10. ANHANG

### A. Tonalitäts-Definitionen

| Tonalität | Definition | Beispiel-Indikatoren |
|-----------|------------|---------------------|
| **negativ** | Kritisch, ablehnend, relativierend, Angriff | "aber", "trotzdem", "zu spät", "versagt" |
| **neutral** | Faktisch, beide Seiten, ausgewogen | "laut Statistik", "Experten sagen", "einerseits...andererseits" |
| **positiv** | Wohlwollend, Erfolg anerkennend, konstruktiv | "Erfolg", "wirkt", "Verbesserung", "Maßnahmen greifen" |

### B. Framing-Kategorien

| Code | Frame | Trigger-Wörter |
|------|-------|----------------|
| RF-1 | Trotzdem | "aber", "trotzdem", "dennoch", "obwohl" |
| RF-2 | Zu spät | "endlich", "nach Jahren", "zu spät", "längst überfällig" |
| RF-3 | Nicht ihr Verdienst | "Basiseffekt", "global", "extern", "Zufall" |
| RF-4 | Ablenkung | "derweil", "aber [anderes Thema]", "währenddessen" |
| RF-5 | Wer zahlt | "Schulden", "Steuerzahler", "Kosten", "wer zahlt" |
| RF-6 | Elite vs. Volk | "sie feiern", "wir zahlen", "Elite", "Politiker" |

### C. Medium-Spezifische Erwartungen

| Medium | Standard-Frame | Typisches Timing | Personalisierung |
|--------|----------------|------------------|------------------|
| Krone | RF-1 + RF-6 | Sofort + 3-Tage-Serie | Immer (mit Foto) |
| oe24 | RF-2 + FPÖ-Zitate | Sofort + Live-Ticker | Oft |
| Heute | RF-1 + RF-4 | Sofort | Manchmal |
| Standard | Differenziert | +1 Tag | Selten |
| Presse | RF-3 | +1 Tag | Nie |
| ORF | Neutral | Sofort | Nie |

---

**Erstellt:** FehrAdvice Strategieteam
**Letzte Aktualisierung:** 4. Februar 2026
**SSOT:** `data/customers/spo/database/MEDIEN_DATENBANK.yaml`
**Version:** 1.0

---

*Dieses Dokument ist Teil der strategischen Dokumentation für das SPÖ-Mandat und wird bei signifikanten Änderungen an der Medien-Datenbank aktualisiert.*
