# 🎯 Claude Code Skills — Vollständiger Guide

> **Alle verfügbaren Skills & Commands für das EBF Framework**

**Version 1.1** | Januar 20, 2026 | FehrAdvice & Partners AG

---

## 📋 Übersicht: Alle Skills

### **Customer Strategy Skills** (5 Skills)
Parametrische Kundenmodelle in < 15 Minuten

| Skill | Beschreibung | Zeit |
|-------|------------|------|
| `/new-customer` | Neue Customer-Datenbank erstellen | < 1 min |
| `/apply-models` | 4 Modelle ausführen (RPM, MCSM, OSM, CAM) | 2-5 min |
| `/sensitivity-analysis` | Was-Wenn-Szenarien testen | < 2 min |
| `/board-presentation` | Board-ready Deck generieren | 1-2 min |
| `/replicate-customer` | Von ALPLA-Template replizieren | 4-6 h |

### **Evidence-Based Framework Skills** (6 Skills) ✨ NEU

**Neuer Schwerpunkt: Verhaltensmodellierung & Interventionen**

| Skill | Beschreibung | Zeit | Status |
|-------|------------|------|--------|
| `/design-model` | 9-Step Verhaltensmodell designen (EEE Workflow) | 10-60 min | ✅ v54 |
| `/design-intervention` | 20-Field Interventions-Schema (EBF-konform) | 10-60 min | ✅ v54 NEU |
| `/case` | Case Registry abfragen (10C-indiziert) | instant | ✅ v54 |
| `/case-manage` | Cases finden & anlegen | 5-10 min | ✅ v54 |
| `/intervention` | Intervention Registry abfragen | instant | ✅ v54 |
| `/intervention-manage` | Projekte anlegen & abschließen | 5-10 min | ✅ v54 |

### **Documentation & Paper Skills** (2 Skills)

| Skill | Beschreibung | Zeit |
|-------|------------|------|
| `/generate-paper` | Paper aus Kapitel/Appendix generieren | 5-10 min |
| `/compile` | LaTeX → PDF kompilieren | 2-5 min |

### **Quality & Validation Skills** (3 Skills)

| Skill | Beschreibung | Zeit |
|-------|------------|------|
| `/check-compliance` | Compliance prüfen (Kapitel/Appendix) | < 1 min |
| `/validate` | Alle Validierungen ausführen | 5-10 min |
| `/r-score` | LLMMC → R-Score Pipeline | 10-30 min |

---

## 🚀 Schnellstart nach Anwendungsfall

| Skill | Beschreibung | Zeit | Ausgabe |
|-------|------------|------|---------|
| **`/new-customer`** | Neue Customer-Datenbank erstellen | < 1 min | YAML + Python-Zugang |
| **`/apply-models`** | 4 Modelle ausführen (RPM, MCSM, OSM, CAM) | 2-5 min | CSVs + Charts |
| **`/sensitivity-analysis`** | Parameter-Auswirkungen testen (Was-Wenn) | < 2 min | Sensitivitäts-Reports |
| **`/board-presentation`** | Board-ready PDF (10 Slides) generieren | 1-2 min | Professional Deck |
| **`/replicate-customer`** | Von ALPLA-Template replizieren (4-6h) | 4-6 h | Vollständiges Modell |

---

## 🚀 Integrated Workflow (Standard-Ablauf)

```
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 1: SETUP (< 1 Minute)                                    │
├─────────────────────────────────────────────────────────────────┤
│  /new-customer "CompanyName" 1500 "Europe,APAC,SA"             │
│  ↓                                                              │
│  ✓ Datenbank erstellt                                          │
│  ✓ 4 Modelle initialisiert                                     │
│  ✓ Ready für Modellausführung                                  │
└─────────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 2: ASSUMPTION TUNING (5-10 Minuten)                      │
├─────────────────────────────────────────────────────────────────┤
│  📝 Manuell anpassen:                                           │
│     - Revenue growth assumptions                               │
│     - Cost structure per market                                │
│     - Headcount productivity                                   │
│     - Capex requirements                                       │
│                                                                │
│  Dateien in: data/customers/<company>/                         │
│    - database.yaml                                             │
│    - assumptions.yaml                                          │
└─────────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 3: EXECUTION (2-5 Minuten)                               │
├─────────────────────────────────────────────────────────────────┤
│  /apply-models CompanyName                                     │
│  ↓                                                              │
│  ✓ RPM (Revenue Projection Model) ausgeführt                   │
│  ✓ MCSM (Headcount/Cost Model) ausgeführt                      │
│  ✓ OSM (Organizational Structure) ausgeführt                   │
│  ✓ CAM (Capital Allocation) ausgeführt                         │
│                                                                │
│  Outputs: outputs/<company>/                                   │
│    - revenue_projections.csv                                   │
│    - headcount_analysis.csv                                    │
│    - org_design.json                                           │
│    - capex_requirements.csv                                    │
└─────────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 4: SENSITIVITY TESTING (< 2 Minuten)                     │
├─────────────────────────────────────────────────────────────────┤
│  /sensitivity-analysis CompanyName APAC_CAGR +1.5pp            │
│  ↓                                                              │
│  ✓ Sensitivitäts-Matrix generiert                              │
│  ✓ Risiko-Profile identifiziert                                │
│  ✓ What-If-Szenarien erstellt                                  │
└─────────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 5: BOARD PRESENTATION (1-2 Minuten)                      │
├─────────────────────────────────────────────────────────────────┤
│  /board-presentation CompanyName pdf                            │
│  ↓                                                              │
│  ✓ 10-Slide Deck generiert                                     │
│  ✓ Alle KPIs visualisiert                                      │
│  ✓ Ready für Präsentation                                      │
│                                                                │
│  Slide-Struktur:                                               │
│    1. Executive Summary                                        │
│    2. Market Overview & Assumptions                            │
│    3. Revenue Projections (5y)                                 │
│    4. Revenue Mix by Market                                    │
│    5. Headcount & Productivity                                 │
│    6. Org Design (Current → Target)                            │
│    7. Capex Requirements                                       │
│    8. Sensitivities & Risks                                    │
│    9. Key Milestones                                           │
│   10. Investment Thesis                                        │
└─────────────────────────────────────────────────────────────────┘

✅ COMPLETE STRATEGIC MODEL: < 15 Minuten statt 2+ Wochen!
```

---

## 📖 Detaillierte Skill-Dokumentation

### 1️⃣ `/new-customer` — Neue Customer-Datenbank

**Was es macht:**
- Neue Customer-Datenbank mit Standardannahmen erstellen
- 4 Modellvorlagen initialisieren
- Ordnerstruktur in `data/customers/` anlegen

**Syntax:**
```bash
/new-customer "<Company Name>" <base_revenue_mln> "<Region1,Region2,Region3>"
```

**Parameter:**
| Parameter | Typ | Beispiel | Beschreibung |
|-----------|-----|---------|-------------|
| `Company Name` | String | "TechCorp" | Eindeutiger Unternehmensname |
| `base_revenue_mln` | Integer | 1500 | Basis-Revenue in Millionen EUR |
| `Regions` | CSV | "Europe,APAC,SA" | Geografische Märkte (Europe, APAC, SA, NA) |

**Beispiele:**

```bash
# Neue Tech-Company für Europa und APAC
/new-customer "TechCorp" 2500 "Europe,APAC"

# Europäische Mittelständler alle 4 Regionen
/new-customer "MediumTech" 500 "Europe,APAC,SA,NA"

# Südamerikaisches Fokus-Unternehmen
/new-customer "LatinTech" 300 "SA,Europe"
```

**Output-Struktur:**
```
data/customers/TechCorp/
├── database.yaml              ← Stammdaten
├── assumptions.yaml           ← Parametrische Annahmen
├── models/
│   ├── rpm_config.yaml        ← Revenue Projection Model
│   ├── mcsm_config.yaml       ← Headcount/Cost Model
│   ├── osm_config.yaml        ← Org Structure Model
│   └── cam_config.yaml        ← Capital Allocation Model
└── README.md                  ← Dokumentation
```

**Was du danach machen solltest:**
1. ✏️ `assumptions.yaml` anpassen (Growth rates, Margins, etc.)
2. 📊 `database.yaml` mit aktuellen Zahlen aktualisieren (optional)
3. ⚙️ Region-spezifische Parameter justieren
4. ✅ Dann: `/apply-models` aufrufen

---

### 2️⃣ `/apply-models` — Alle 4 Modelle ausführen

**Was es macht:**
- Alle 4 Modelle sequenziell ausführen
- Revenue-, Headcount-, Org- und Capex-Projektionen generieren
- Charts und Statistiken erstellen
- Alle Ausgaben in `outputs/<Company>/` speichern

**Syntax:**
```bash
/apply-models <Company> [--format csv|json|both] [--years 5|10]
```

**Parameter:**
| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|---------|-------------|
| `Company` | String | — | Unternehmensname (aus `/new-customer`) |
| `format` | Flag | both | Output-Format: csv, json, oder both |
| `years` | Flag | 5 | Projektionszeitraum (5 oder 10 Jahre) |

**Beispiele:**

```bash
# Standard: 5 Jahre, alle Formate
/apply-models TechCorp

# 10-Jahres-Projektion
/apply-models TechCorp --years 10

# Nur CSV-Output
/apply-models TechCorp --format csv

# 10 Jahre, nur JSON
/apply-models TechCorp --years 10 --format json
```

**Output-Dateien:**
```
outputs/TechCorp/
├── revenue_projections.csv    ← RPM Output
├── headcount_analysis.csv     ← MCSM Output (HC + Costs)
├── org_design.json            ← OSM Output (Struktur)
├── capex_requirements.csv     ← CAM Output (Investitionen)
├── charts/
│   ├── revenue_5y.png
│   ├── headcount_growth.png
│   ├── cost_breakdown.png
│   └── capex_profile.png
└── summary.json               ← Alle KPIs aggregiert
```

**Was die 4 Modelle machen:**

| Modell | Input | Output | Logik |
|--------|-------|--------|-------|
| **RPM** (Revenue) | Base Revenue, CAGR by market | 5y Revenue by market | Kompound growth mit Markt-Mix |
| **MCSM** (Headcount) | Revenue, Productivity, Cost/HC | HC trajectory + Total costs | Revenue-based HC allocation |
| **OSM** (Org Design) | HC levels, Departments | Org chart, Spans | Org design von ALPLA |
| **CAM** (Capex) | Revenue growth, Market size | Capex by year + ROI | Infrastructure + IT + Ops |

---

### 3️⃣ `/sensitivity-analysis` — Was-Wenn-Szenarien

**Was es macht:**
- Testet Auswirkungen von Parametervariationen
- Erstellt Sensitivitäts-Matrizen (z.B. 2D: CAGR vs. Margin)
- Identifiziert kritische Trigger-Punkte
- Generiert Risk-Profile und Szenarien

**Syntax:**
```bash
/sensitivity-analysis <Company> <Parameter> <Change> [--format report|csv|all]
```

**Parameter:**
| Parameter | Typ | Beispiel | Beschreibung |
|-----------|-----|---------|-------------|
| `Company` | String | TechCorp | Unternehmensname |
| `Parameter` | Enum | APAC_CAGR | Parameter zum Variieren (siehe unten) |
| `Change` | Float | +1.5pp | Änderung (z.B. +1.5 Prozentpunkte, -10%) |
| `format` | Flag | all | Output: report, csv, oder all |

**Verfügbare Parameter:**
```
Regional Growth (market-specific):
  - EUROPE_CAGR         (z.B. +0.5pp, -1.0pp)
  - APAC_CAGR           (z.B. +2.0pp)
  - SA_CAGR             (z.B. -1.5pp)
  - NA_CAGR             (z.B. +1.0pp)

Profitability:
  - GROSS_MARGIN        (z.B. +2pp, -1pp)
  - OPEX_RATIO          (z.B. +1pp)
  - TAX_RATE            (z.B. +2pp)

Headcount:
  - PRODUCTIVITY_GAIN   (z.B. +5%, -3%)
  - HC_COST_INFLATION   (z.B. +2pp)

Capital:
  - CAPEX_INTENSITY     (z.B. +1pp, -0.5pp)
  - CAPEX_CAPEX_ROI     (z.B. +5%, -5%)
```

**Beispiele:**

```bash
# Was passiert, wenn APAC mit +2pp stärker wächst?
/sensitivity-analysis TechCorp APAC_CAGR +2pp

# Was, wenn Gross Margin 3pp sinkt?
/sensitivity-analysis TechCorp GROSS_MARGIN -3pp

# Was, wenn Produktivität +10% steigt?
/sensitivity-analysis TechCorp PRODUCTIVITY_GAIN +10pct

# 2D-Sensitivität: APAC_CAGR × GROSS_MARGIN (Matrix)
/sensitivity-analysis TechCorp APAC_CAGR×GROSS_MARGIN "+1pp,-1pp"

# Alle Parameter durchspielen (umfassender Report)
/sensitivity-analysis TechCorp all
```

**Output:**
```
outputs/TechCorp/sensitivity/
├── APAC_CAGR_+2pp/
│   ├── revenue_delta.csv           ← Impact auf Revenue
│   ├── headcount_delta.csv         ← Impact auf HC
│   ├── margin_delta.csv            ← Impact auf Profitabilität
│   └── sensitivity_chart.png       ← Visualisierung
├── sensitivity_matrix.csv          ← 2D: Parameter × Impact
├── risk_profile.json               ← Kritische Trigger
└── scenario_comparison.pdf         ← Alle Szenarien vs. Base
```

**Interpretation der Outputs:**
- **Sensitivity_delta.csv:** Zeigt absolute Veränderungen
- **Risk_profile.json:** Listet kritische Schwellenwerte auf
- **Scenario_comparison.pdf:** Side-by-Side Vergleich aller Szenarien

---

### 4️⃣ `/board-presentation` — Präsentations-Deck generieren

**Was es macht:**
- Erstellt ein professionelles 10-Slide Deck
- Alle KPIs automatisch visualisiert
- Executive Summary + Business Case
- Ready für Board/Investor-Präsentation

**Syntax:**
```bash
/board-presentation <Company> [--format pdf|pptx|both] [--style professional|concise]
```

**Parameter:**
| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|---------|-------------|
| `Company` | String | — | Unternehmensname |
| `format` | Flag | pdf | Ausgabe: pdf, pptx, oder both |
| `style` | Flag | professional | professional = verbose, concise = compact |

**Beispiele:**

```bash
# Standard: PDF mit ausführlichen Texten
/board-presentation TechCorp

# PowerPoint für interne Bearbeitung
/board-presentation TechCorp --format pptx

# Beide Formate
/board-presentation TechCorp --format both

# Kompakte Version (1-Seite Notizen pro Slide)
/board-presentation TechCorp --style concise
```

**Slide-Struktur:**

| # | Slide | Content | Quelle |
|---|-------|---------|--------|
| 1 | **Executive Summary** | Company, Strategy, Key metrics | database.yaml |
| 2 | **Market Overview** | Regions, TAM, Assumptions | assumptions.yaml |
| 3 | **Revenue Projections** | 5-Year path, CAGR by market | RPM output |
| 4 | **Revenue Mix** | Waterfall by market, Mix shifts | RPM breakdown |
| 5 | **Headcount & Productivity** | HC trajectory, Revenue/HC | MCSM output |
| 6 | **Organizational Design** | Current vs. Target structure | OSM output |
| 7 | **Capex Requirements** | 5Y capex profile, ROI | CAM output |
| 8 | **Risks & Sensitivities** | 3 downside scenarios | sensitivity output |
| 9 | **Key Milestones** | Timeline with decision gates | assumptions.yaml |
| 10 | **Investment Thesis** | Value creation bridge, P&L impact | Summary stats |

**Output:**
```
outputs/TechCorp/presentations/
├── TechCorp_Board_Presentation_20260115.pdf
├── TechCorp_Board_Presentation_20260115.pptx
├── charts/                    ← Alle Slide-Charts separat
└── notes.txt                  ← Speaker Notes
```

---

### 5️⃣ `/replicate-customer` — Von ALPLA-Template replizieren

**Was es macht:**
- Kopiert das vollständige ALPLA-Modell (€4.9B → €9.9B)
- Passt alle Annahmen an neue Company an
- Lädt alle Models, Strategien und Organizational Design
- Takes 4-6 Stunden für komplette Replikation

**Syntax:**
```bash
/replicate-customer <Source> "<New Company>" [--mode fast|complete|custom]
```

**Parameter:**
| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|---------|-------------|
| `Source` | String | ALPLA | Template-Company (momentan: ALPLA) |
| `New Company` | String | — | Name der neuen Company |
| `mode` | Flag | complete | fast = essentials, complete = alles |

**Modi:**

| Modus | Was wird kopiert | Zeit | Use Case |
|-------|-----------------|------|----------|
| **fast** | Nur Modelle + base assumptions | 1-2h | Schneller MVP |
| **complete** | Alles inkl. Strategien + Org Design | 4-6h | Full production model |
| **custom** | Fast + ausgewählte Komponenten | 2-4h | Selective replication |

**Beispiele:**

```bash
# Komplette Replikation (alles wie ALPLA)
/replicate-customer ALPLA "NewCorp"

# Nur Modelle (schneller MVP)
/replicate-customer ALPLA "TechCorp" --mode fast

# Fast-Mode + mit Custom-Strategien
/replicate-customer ALPLA "MedTech" --mode custom
```

**Was wird repliziert (complete mode):**

| Komponente | Quelle | Wohin |
|-----------|--------|-------|
| **Models** | ALPLA/models/ | NewCorp/models/ |
| **Assumptions** | ALPLA/assumptions_€4.9B_€9.9B | NewCorp/assumptions (angepasst) |
| **Org Design** | ALPLA/org_design_€4.9B_€9.9B | NewCorp/org_design |
| **Growth Strategies** | ALPLA/strategies/ | NewCorp/strategies |
| **P&L Template** | ALPLA/financials/ | NewCorp/financials |
| **KPI Framework** | ALPLA/kpis/ | NewCorp/kpis |

**Output-Struktur:**
```
data/customers/NewCorp/
├── database.yaml              ← ALPLA base, angepasst
├── assumptions.yaml           ← ALPLA assumptions, scaled
├── models/                    ← Kopiert + Config angepasst
├── org_design/                ← Komplettes ALPLA Org Design
├── strategies/                ← 3 Growth Strategies
├── financials/                ← P&L Template + Projections
└── replication_log.txt        ← Was wurde kopiert, wann
```

**Nach Replikation:**
1. ✏️ `database.yaml` mit echten Daten anpassen
2. 🎯 `assumptions.yaml` region-spezifisch justieren
3. 📊 `/apply-models` ausführen
4. 📈 Outputs in `outputs/NewCorp/` prüfen

**Timing:**
- **Fast mode:** 30 min Setup + 30-60 min erste Model-Run = ~1-2h total
- **Complete mode:** 1h Replikation + 1h Config + 2-4h Validierung = 4-6h total

---

## 🎯 Typische Use Cases

### Use Case 1: Schnelle Opportunity Assessment (15 Min)

**Scenario:** Investor fragt: "Wie könnte TechCorp bei 40% APAC-Growth skalieren?"

**Workflow:**
```bash
# 1. Setup
/new-customer "TechCorp" 1500 "Europe,APAC"

# 2. Ausführen
/apply-models TechCorp

# 3. Sensitivität: +40% APAC?
/sensitivity-analysis TechCorp APAC_CAGR +8pp

# 4. Präsentation
/board-presentation TechCorp --style concise
```

**Total: 12-15 Minuten!**

---

### Use Case 2: Parametrische Szenarien (30 Min)

**Scenario:** Drei P&L-Szenarien für Steuerboard

**Workflow:**
```bash
# Base case
/apply-models TechCorp --years 5

# Bull case: APAC +2pp, Margin +1pp
/sensitivity-analysis TechCorp APAC_CAGR×GROSS_MARGIN "+2pp,+1pp"

# Bear case: APAC -2pp, Margin -1pp
/sensitivity-analysis TechCorp APAC_CAGR×GROSS_MARGIN "-2pp,-1pp"

# Vergleichende Präsentation
/board-presentation TechCorp --style professional
```

**Total: 25-30 Minuten!**

---

### Use Case 3: ALPLA-Template für neues Unternehmen (4-6 h)

**Scenario:** Neue Portfolio-Company soll ALPLA-Modell nutzen

**Workflow:**
```bash
# 1. Repliziere Modell (4-6 h, läuft im Hintergrund)
/replicate-customer ALPLA "PortfolioCo"

# [Während Replikation läuft: Daten sammeln]

# 2. Nach Replikation: Daten anpassen + ausführen
/apply-models PortfolioCo

# 3. Sensitivitäten
/sensitivity-analysis PortfolioCo all

# 4. Finale Präsentation
/board-presentation PortfolioCo
```

**Total: 4-6h (davon 3-5h automatisiert)**

---

## 🔧 Troubleshooting

### Problem: `/new-customer` fehlgeschlagen
```
Error: Customer "TechCorp" already exists
```
**Lösung:** Customer-Name muss eindeutig sein. Nutze einen neuen Namen oder lösche `data/customers/TechCorp/`

### Problem: `/apply-models` sehr langsam
```
Warning: Large dataset detected (10-year projection)
Processing may take 10-15 minutes...
```
**Lösung:** Nutze `--years 5` statt 10, oder starten Sie in separate Session

### Problem: `/board-presentation` hat leere Charts
```
No data found in outputs/<Company>/
```
**Lösung:** `/apply-models` muss VOR `/board-presentation` ausgeführt sein

### Problem: Sensitivitäts-Output unvollständig
```
Sensitivity incomplete: Only 3/5 parameters tested
```
**Lösung:** Nutze `--format all` und versuche erneut mit `/sensitivity-analysis <Company> all`

---

## 📊 Tipps & Best Practices

### ✅ DO

1. **Immer in dieser Reihenfolge:**
   - `/new-customer` → anpassen → `/apply-models` → `/sensitivity-analysis` → `/board-presentation`

2. **Daten vor Modellen justieren:**
   - ✏️ `database.yaml` anpassen
   - ⚙️ `assumptions.yaml` kalibrieren
   - 🔄 DANN erst `/apply-models` aufrufen

3. **Regional denken:**
   - Jeder Markt (Europe, APAC, SA, NA) hat eigene Annahmen
   - Region-spezifische CAGRs und Margins verwenden

4. **Sensitivitäten prüfen:**
   - Vor Board-Präsentation: Welche Parameter treiben >20% Varianz?
   - Diese Parameter als "key sensitivities" in Slide 8 erwähnen

### ❌ DON'T

1. **Nicht `/apply-models` ohne Daten-Check aufrufen**
   - Müll rein = Müll raus

2. **Nicht Annahmen nach Model-Run ändern**
   - Modelle werden mit Snapshot-Annahmen gebaut
   - Änderungen = neuer Model-Run erforderlich

3. **Nicht Board-Deck ohne Sensitivitäten**
   - Immer 3 Szenarien zeigen (Base, Bull, Bear)

4. **Nicht regional aggregieren**
   - Jeder Markt getrennt tracken
   - Mix-Verschiebungen sind strategisch wichtig

---

## 📞 Support & Fragen

### Dokumentation
- Detaillierte Skill-Docs: `.claude/commands/<skill>.md`
- Framework-Dokumentation: `CLAUDE.md`
- Modell-Spezifikationen: `data/models/`

### Features anfordern
- Issue auf GitHub: `FehrAdvice-Partners-AG/complementarity-context-framework`
- Skill Feature Request: `[FEATURE] /skill-name: ...`

### Bugs melden
- Issue: `[BUG] /skill-name: ...`
- Include: Company name, Parameter, Fehler-Output

---

## 📈 Beispiel: Von Setup zu Board-Deck in 15 Minuten

```bash
# Minute 0-1: Neue Company
/new-customer "FastGrowth" 2000 "Europe,APAC,SA"

# Minute 1-2: Annahmen manuell anpassen
# (Edit data/customers/FastGrowth/assumptions.yaml)

# Minute 2-7: Modelle ausführen
/apply-models FastGrowth --years 5

# Minute 7-9: Sensitivitäten testen
/sensitivity-analysis FastGrowth APAC_CAGR +3pp

# Minute 9-11: Präsentation generieren
/board-presentation FastGrowth --format pdf

# Minute 11-15: Präsentation review
# (outputs/FastGrowth/presentations/...)

✅ Ready for Board in 15 Minuten!
```

---

<div align="center">

**Viel Erfolg mit den Customer Strategy Skills! 🚀**

*Bei Fragen: Lese `.claude/commands/<skill>.md` oder frag Claude Code*

</div>

---

---

## 🆕 Neu in Version 1.1 (Januar 2026)

**EBF Framework Skills hinzugefügt:**
- ✅ `/design-model` — 9-Step EEE Workflow für Verhaltensmodelle
- ✅ `/design-intervention` — 20-Field Schema mit Compliance-Checks
- ✅ Evidence Integration Pipeline (EIP) — Automatische Literatur-Integration
- ✅ `/case` & `/case-manage` — Case Registry mit 10C-Indexierung
- ✅ `/intervention` & `/intervention-manage` — Intervention Tracking

**Updates:**
- All Skills dokumentiert
- 15+ Commands verfügbar
- v54 Features integriert
- Hybrid README Auto-Update System

---

*Letzte Aktualisierung: 2026-01-20*
*Version: 1.1 — Full EBF Skills Suite*
