# /literature-analysis — Systematische Literaturanalyse (SLA)

## Übersicht

Ausführbarer Workflow für systematische Literaturanalysen.
**NICHT für einzelne Papers** (→ /integrate-paper), sondern: «Was weiss die Wissenschaft zu Thema X?»

**MUSS bei JEDER systematischen Literaturanalyse verwendet werden** - nicht optional!

## Der 14-Schritt SLA-Workflow (PFLICHT)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  14-SCHRITT SYSTEMATIC LITERATURE ANALYSIS (SLA)                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  SCHRITT 1:  SLA-ID GENERIEREN     → SLA-YYYY-MM-DD-TOPIC-NNN          │
│  SCHRITT 2:  MODUS WÄHLEN          → RAPID / STANDARD / SYSTEMATIC     │
│  SCHRITT 3:  FORSCHUNGSFRAGE        → PICO oder SPIDER Format          │
│  SCHRITT 4:  KRITERIEN DEFINIEREN   → Inklusion + Exklusion VOR Suche  │
│  SCHRITT 5:  PROTOKOLL SPEICHERN    → data/literature-analyses/SLA.yaml │
│  SCHRITT 6:  INTERNE SUCHE          → bcm_master.bib + theory-catalog  │
│  SCHRITT 7:  EXTERNE SUCHE          → WebSearch + Scholar              │
│  SCHRITT 8:  SCREENING (5-Score)    → Jedes Paper bewerten + filtern   │
│  SCHRITT 9:  KODIERUNG (9-Dim)      → Strukturierte Extraktion         │
│  SCHRITT 10: SYNTHESE               → Evidenz-Tabelle + PRO/CONTRA     │
│  SCHRITT 11: GAP-ANALYSE            → Empirisch + Theoretisch + Method │
│  SCHRITT 12: REPORT SCHREIBEN       → outputs/literature-analyses/     │
│  SCHRITT 13: EBF-INTEGRATION        → Papers + Parameter + Cases       │
│  SCHRITT 14: COMMIT + PUSH          → Alle Dateien auf GitHub          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Verwendung

```bash
/literature-analysis                              # Interaktiv (empfohlen)
/literature-analysis "NIMBY Kompensation"          # Mit Thema
/literature-analysis --mode rapid                  # Rapid Mode (15-30 min)
/literature-analysis --mode standard               # Standard Mode [DEFAULT]
/literature-analysis --mode systematic             # PRISMA-konform (4+ Std)
/literature-analysis --resume SLA-2026-02-11-NIMBY-001  # Fortsetzen
```

## Automatische Trigger

Claude erkennt automatisch SLA-Anfragen und startet den Workflow:

| Trigger | Beispiel |
|---------|----------|
| "Was weiss die Wissenschaft über..." | "Was weiss die Wissenschaft über NIMBY?" |
| "Was sagt die Literatur zu..." | "Was sagt die Literatur zu Crowding-Out?" |
| "Systematische Analyse zu..." | "Systematische Analyse zu Infrastruktur-Akzeptanz" |
| "Literaturüberblick" / "Literature Review" | "Erstelle einen Literaturüberblick zu X" |
| "Forschungsstand" / "State of the Art" | "Wie ist der Forschungsstand zu Y?" |
| "Was zeigt die Evidenz..." | "Was zeigt die Evidenz zu Default-Effekten?" |
| "Gibt es Studien zu..." | "Gibt es Studien zu Kompensation bei Infrastruktur?" |

**DANN:**
```
Claude: "Ich erkenne eine Literaturanalyse-Anfrage. Starte /literature-analysis..."
→ Schritt 1: SLA-ID generieren
→ Schritt 2-14: Durchführen
```

---

## Schritt-für-Schritt Details

### Schritt 1: SLA-ID GENERIEREN

```
ID-FORMAT: SLA-{YYYY}-{MM}-{DD}-{TOPIC}-{SEQ}

TOPIC aus Thema ableiten (max 12 Zeichen, Grossbuchstaben):
  "NIMBY Kompensation"           → NIMBY
  "Default-Effekte Vorsorge"     → DEFAULTS
  "Infrastruktur-Akzeptanz"      → INFRASTRUKTUR
  "Loss Aversion Banking"        → LOSSAVERSION

SEQ: 001, 002, ... (fortlaufend pro Tag+Topic)

Beispiel: SLA-2026-02-11-NIMBY-001
```

### Schritt 2: MODUS WÄHLEN

```
┌─────────────────────────────────────────────────────────────────────────┐
│  MODUS                                                                  │
│                                                                         │
│  ⚡ RAPID      15-30 min, 10-20 Papers                                  │
│     Quellen: Nur bcm_master.bib + 1 WebSearch                          │
│     Screening: Titel-basiert (3 Scores)                                │
│     Output: Markdown 3-pager                                           │
│                                                                         │
│  🎯 STANDARD   1-2 Std, 20-50 Papers  ← [DEFAULT]                      │
│     Quellen: bcm_master.bib + theory-catalog + WebSearch + Snowballing │
│     Screening: Titel+Abstract (5 Scores)                               │
│     Output: Markdown/LaTeX 10-pager                                    │
│                                                                         │
│  🔬 SYSTEMATIC  4+ Std, 50-200 Papers                                   │
│     Quellen: Alle + Scopus/WoS (via User)                              │
│     Screening: Titel+Abstract+Volltext (5 Scores)                      │
│     Output: LaTeX/PDF 30-pager, PRISMA-konform                         │
│                                                                         │
│  → Enter = STANDARD                                                     │
└─────────────────────────────────────────────────────────────────────────┘
```

**Modus-abhängige Schritte:**

| Schritt | RAPID | STANDARD | SYSTEMATIC |
|---------|-------|----------|------------|
| 3 Forschungsfrage | 1 Frage, informal | PICO/SPIDER | PICO + Subfragen |
| 4 Kriterien | 3 Kriterien | 5-8 Kriterien | Vollständiges Set |
| 6 Interne Suche | bcm_master.bib | + theory-catalog + cases | + alle Registries |
| 7 Externe Suche | 1 WebSearch | 3-5 WebSearches + Snowball | + User liefert Scopus/WoS |
| 8 Screening | Titel (3 Scores) | Titel+Abstract (5 Scores) | + Volltext |
| 9 Kodierung | 4 Dimensionen | 9 Dimensionen | 9 Dim + Kodebuch |
| 12 Report | 3-pager MD | 10-pager MD/LaTeX | 30-pager LaTeX/PDF |

### Schritt 3: FORSCHUNGSFRAGE DEFINIEREN

Claude generiert automatisch aus dem Thema. User bestätigt.

**Für empirische Fragen → PICO Format:**

```yaml
research_question:
  format: "PICO"
  population: ""      # Wer? (z.B. "Schweizer Stimmbürger:innen")
  intervention: ""    # Was? (z.B. "Finanzielle Kompensation für Infrastruktur")
  comparison: ""      # Verglichen mit? (z.B. "Keine Kompensation")
  outcome: ""         # Ergebnis? (z.B. "Akzeptanzrate")
  primary: ""         # Vollständige Frage als Satz
  secondary: []       # 1-3 Subfragen
```

**Für explorative Fragen → SPIDER Format:**

```yaml
research_question:
  format: "SPIDER"
  sample: ""           # Wer/Was?
  phenomenon: ""       # Welches Phänomen?
  design: ""           # Studiendesign?
  evaluation: ""       # Was messen?
  research_type: ""    # Forschungstyp?
  primary: ""          # Vollständige Frage als Satz
  secondary: []
```

**Claude zeigt dem User die vorgefüllte Frage:**

```
┌─────────────────────────────────────────────────────────────────────────┐
│  📋 FORSCHUNGSFRAGE (PICO):                                             │
│                                                                         │
│  P: Schweizer Stimmbürger:innen                                        │
│  I: Finanzielle Kompensation für Infrastrukturprojekte                 │
│  C: Keine Kompensation / Prozessuale Fairness                          │
│  O: Akzeptanzrate, Zustimmung in Volksabstimmung                       │
│                                                                         │
│  → "Wie beeinflusst finanzielle Kompensation die lokale Akzeptanz     │
│     von Infrastrukturprojekten in der Schweiz?"                        │
│                                                                         │
│  Subfragen:                                                             │
│  1. Welche Kompensationsformen vermeiden Crowding-Out?                 │
│  2. Wie interagiert Status Quo Bias mit Infrastruktur-Framing?         │
│                                                                         │
│  [Enter] = OK | [e] = Editieren                                        │
└─────────────────────────────────────────────────────────────────────────┘
```

### Schritt 4: INKLUSIONS-/EXKLUSIONSKRITERIEN

**KRITISCH: Müssen VOR der Suche definiert werden!**

Claude generiert automatisch basierend auf Forschungsfrage:

```yaml
inclusion_criteria:
  population: ""          # Wer?
  intervention: ""        # Was?
  outcome: ""             # Welches Ergebnis?
  study_design: []        # Welche Designs? [RCT, quasi-experiment, survey-experiment, ...]
  time_range: "1990-2026" # Zeitraum
  languages: ["en", "de"] # Sprachen
  evidence_tier: [1, 2]   # Nur Tier 1+2 (RAPID: auch Tier 3)

exclusion_criteria:       # Nummeriert für Referenz im Exklusions-Log
  EX-1: "Rein theoretisch ohne empirische Daten"
  EX-2: "Studien mit n < 50"
  EX-3: "Keine klare Identifikationsstrategie"
  EX-4: "Nicht-demokratischer Kontext"
  EX-5: "Keine Peer-Review (ausser NBER/CEPR WP)"
```

**Claude zeigt dem User die vorgefüllten Kriterien:**

```
┌─────────────────────────────────────────────────────────────────────────┐
│  📋 INKLUSIONS-/EXKLUSIONSKRITERIEN:                                    │
│                                                                         │
│  INKLUSION:                                                             │
│  ✅ Empirisch, demokratischer Kontext, 1990-2026                       │
│  ✅ Tier 1-2, EN/DE, n ≥ 50                                            │
│                                                                         │
│  EXKLUSION:                                                             │
│  EX-1: Rein theoretisch                                                │
│  EX-2: n < 50                                                          │
│  EX-3: Keine Identifikation                                            │
│  EX-4: Nicht-demokratisch                                              │
│  EX-5: Keine Peer-Review (ausser NBER)                                 │
│                                                                         │
│  [Enter] = OK | [e] = Editieren | [+] = Kriterium hinzufügen          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Schritt 5: PROTOKOLL-YAML SPEICHERN

Claude erstellt automatisch:

```
Datei: data/literature-analyses/SLA-{ID}.yaml
```

```yaml
# ============================================================================
# SYSTEMATIC LITERATURE ANALYSIS PROTOCOL
# ID: SLA-YYYY-MM-DD-TOPIC-NNN
# ============================================================================

protocol:
  id: "SLA-YYYY-MM-DD-TOPIC-NNN"
  title: ""
  mode: "STANDARD"  # RAPID | STANDARD | SYSTEMATIC
  date_started: "YYYY-MM-DD"
  date_completed: null
  status: "in_progress"  # in_progress | completed | paused

  research_question:
    format: "PICO"  # PICO | SPIDER
    primary: ""
    secondary: []
    pico:  # oder spider
      population: ""
      intervention: ""
      comparison: ""
      outcome: ""

  inclusion_criteria:
    population: ""
    intervention: ""
    outcome: ""
    study_design: []
    time_range: ""
    languages: []
    evidence_tier: []

  exclusion_criteria:
    EX-1: ""
    EX-2: ""
    EX-3: ""

search_results:
  total_identified: 0     # N₀
  by_source:
    bcm_master_bib: 0
    theory_catalog: 0
    case_registry: 0
    web_search: 0
    snowballing: 0
  duplicates_removed: 0
  unique_candidates: 0    # N₀ - Duplikate

screening:
  screened: 0
  excluded_title_abstract: 0
  excluded_fulltext: 0
  included: 0             # N₁
  papers: []              # Liste: siehe Schritt 8

coding: []                # Liste: siehe Schritt 9

synthesis:
  evidence_table: []      # siehe Schritt 10
  pro_contra: {}          # siehe Schritt 10
  confidence: ""
  parameter_aggregation: []

gaps:
  empirical: []
  theoretical: []
  methodological: []
  contextual: []

integration:
  new_papers_added: 0
  new_parameters: []
  new_cases: []
  new_theories: []
  bcm2_updates: []

output:
  report_path: ""
  output_registry_id: ""
```

### Schritt 6: INTERNE SUCHE (IMMER ZUERST!)

Claude führt systematisch aus:

```bash
# 6.1 bcm_master.bib durchsuchen (PFLICHT)
python scripts/search_bibliography.py --eip "[Query 1 aus Forschungsfrage]"
python scripts/search_bibliography.py --eip "[Query 2]"
python scripts/search_bibliography.py --eip "[Query 3]"
python scripts/search_bibliography.py --author "[Schlüsselautor]" --parameter "[Parameter]"

# 6.2 Theory Catalog durchsuchen (STANDARD + SYSTEMATIC)
python scripts/theory_papers.py --match-10c "[10C-Dimensionen aus Frage]"
python scripts/theory_papers.py --category [CAT-XX]
python scripts/theory_papers.py --restriction "[Schlüsselrestriktion]"

# 6.3 Case Registry durchsuchen (STANDARD + SYSTEMATIC)
# Grep in data/case-registry.yaml nach Schlüsselbegriffen
```

**Output pro Quelle:** Liste von Paper-IDs + BibTeX-Keys

Claude dokumentiert in Protokoll-YAML:
```yaml
search_results:
  by_source:
    bcm_master_bib: 34    # ← aus Script-Output
    theory_catalog: 8
    case_registry: 5
```

### Schritt 7: EXTERNE SUCHE

**RAPID:** 1 WebSearch pro Subfrage
**STANDARD:** 3-5 WebSearches + Snowballing Top-10
**SYSTEMATIC:** + User liefert Scopus/WoS-Export

```bash
# 7.1 WebSearch (STANDARD + SYSTEMATIC)
WebSearch: "[Keywords] behavioral economics [Outcome] site:scholar.google.com"
WebSearch: "[Keywords] [Intervention] [Population] NBER working paper"
WebSearch: "[Keywords] meta-analysis systematic review"

# 7.2 Snowballing (STANDARD + SYSTEMATIC)
# Für die Top-10 meistzitierten Papers aus Schritt 6:
# → Backward: Referenzlisten durchgehen
# → Forward: Wer zitiert diese Papers? (via Google Scholar)
```

Claude dokumentiert und zeigt:

```
┌─────────────────────────────────────────────────────────────────────────┐
│  📊 SUCHERGEBNISSE (Schritt 6-7):                                       │
│                                                                         │
│  QUELLE              GEFUNDEN                                           │
│  bcm_master.bib        34 Papers                                        │
│  Theory Catalog         8 verlinkte Theorien                            │
│  Case Registry          5 Cases                                         │
│  WebSearch             25 Papers                                        │
│  Snowballing            5 Papers                                        │
│  ─────────────────────────────                                          │
│  TOTAL (N₀):           77                                               │
│  Duplikate:           -12                                               │
│  KANDIDATEN:           65                                               │
│                                                                         │
│  Weiter zum Screening → [Enter]                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Schritt 8: SCREENING (5-Kriterien-Score)

**KRITISCH: Jedes Paper wird SYSTEMATISCH bewertet, nicht ad-hoc!**

#### 8.1 Screening-Score berechnen (5 Kriterien)

Für jedes Kandidaten-Paper 5 Scores (0-2) vergeben:

| Kriterium | Code | 0 = Nein | 1 = Teilweise | 2 = Ja |
|-----------|------|----------|---------------|--------|
| **Relevanz** | REL | Thema passt nicht | Teilrelevant | Kernrelevant |
| **Methodik** | MET | Keine Identifikation | Schwache ID | RCT/IV/DiD/RDD |
| **Evidenz-Tier** | TIR | Tier 3 | Tier 2 | Tier 1 |
| **Kontext-Match** | CTX | Anderer Kontext | Ähnlicher Kontext | Exakter Kontext |
| **Aktualität** | AKT | Vor 2000 | 2000-2015 | 2015-2026 |

**TOTAL: 0-10 Punkte**

#### 8.2 Screening-Entscheidung

```
Score ≥ 6                            → INCLUDE
Score 4-5 + (REL = 2 ODER MET = 2)  → INCLUDE (mit Vorbehalt)
Score 4-5 ohne REL=2/MET=2          → EXCLUDE (dokumentieren)
Score ≤ 3                            → EXCLUDE (dokumentieren)
```

#### 8.3 Screening-Dokumentation (PFLICHT)

Für JEDES Paper in Protokoll-YAML:

```yaml
screening:
  papers:
    - paper_id: "PAP-frey1997costofprice"
      title: "Not In My Backyard"
      scores: {REL: 2, MET: 1, TIR: 2, CTX: 2, AKT: 0}
      total: 7
      decision: "INCLUDE"
      reason: "Core NIMBY study, Swiss context, replicated"

    - paper_id: "NEW-smith2020generic"
      title: "Generic Infrastructure Study"
      scores: {REL: 1, MET: 0, TIR: 1, CTX: 0, AKT: 2}
      total: 4
      decision: "EXCLUDE"
      reason: "EX-3: Keine Identifikationsstrategie, anderer Kontext"
```

#### 8.4 PRISMA-Flow dokumentieren (STANDARD + SYSTEMATIC)

```
Identifiziert: N₀ = 77
- Duplikate: -12
Gescreent: 65
- Exkludiert (Score ≤ 5): -40  (mit Gründen im Log)
Volltext-Prüfung: 25           (nur STANDARD + SYSTEMATIC)
- Exkludiert Volltext: -3      (mit Gründen)
────────────────────
INKLUDIERT: N₁ = 22
```

Claude zeigt:

```
┌─────────────────────────────────────────────────────────────────────────┐
│  📊 SCREENING-ERGEBNIS:                                                 │
│                                                                         │
│  N₀ = 77 identifiziert → N₁ = 22 inkludiert                            │
│                                                                         │
│  EVIDENCE TIER der inkludierten Papers:                                 │
│    Tier 1 (Gold):    8 Papers                                          │
│    Tier 2 (Silver): 11 Papers                                          │
│    Tier 3 (Bronze):  3 Papers                                          │
│                                                                         │
│  TOP-5 (höchster Score):                                                │
│  1. Frey 1997 (Score 9) — NIMBY Crowding-Out                          │
│  2. Duranton/Turner 2011 (Score 8) — Induced Demand                    │
│  3. ...                                                                 │
│                                                                         │
│  Weiter zur Kodierung → [Enter]                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Schritt 9: KODIERUNG (9-Dimensionen-Schema)

**JEDES inkludierte Paper wird nach 9 Dimensionen kodiert.**

```yaml
coding:
  - paper_id: "PAP-frey1997costofprice"
    # 9 KODIERUNGS-DIMENSIONEN:
    DIR: -1                    # Effektrichtung: +1 / 0 / -1
    ES: "-0.51"                # Effektstärke (quantifiziert)
    MEC: "motivation_crowding_out"  # Mechanismus
    MOD:                       # Moderatoren (Ψ-Dimensionen)
      - "Ψ_S: community_size"
      - "Ψ_K: civic_duty_culture"
    CTX: "Switzerland, nuclear waste siting, 1993"  # Kontext
    ID: "survey_experiment"    # Identifikation (RCT/IV/DiD/...)
    PAR:                       # EBF-Parameter-Referenzen
      - "PAR-INF-001"
      - "PAR-COMP-002"
    PC: "PRO"                  # PRO/CONTRA zur Hypothese
    REP: "conceptual_replications"  # Replikationsstatus
```

**RAPID-Modus: Nur 4 Dimensionen (DIR, ES, MEC, PC)**
**STANDARD-Modus: Alle 9 Dimensionen**
**SYSTEMATIC-Modus: 9 Dimensionen + Kodebuch + Abweichungsprotokoll**

**Kodierungs-Regeln:**

| Dimension | Werte | Hinweis |
|-----------|-------|---------|
| DIR | +1, 0, -1 | Richtung des Haupteffekts |
| ES | Numerisch | Elastizität, pp, Koeffizient, OR, Cohens d |
| MEC | String | crowding_out, induced_demand, status_quo_bias, framing, ... |
| MOD | Liste | Ψ-Dimensionen die den Effekt moderieren |
| CTX | String | Land, Branche, Zeitraum, Sample |
| ID | Enum | RCT, IV, DiD, RDD, matching, survey_experiment, correlation |
| PAR | Liste | PAR-xxx-xxx IDs (bestehende oder neue) |
| PC | Enum | PRO, CONTRA, NEUTRAL |
| REP | Enum | replicated, partial, failed, none, conceptual |

### Schritt 10: SYNTHESE

Claude erstellt automatisch aus den kodierten Daten:

#### 10.1 Evidenz-Synthese-Tabelle

```yaml
synthesis:
  evidence_table:
    - finding: "Kompensation → ↓ Akzeptanz"
      direction: "NEGATIV"
      effect_size: "γ = -0.51"
      tier_1_papers: 1
      tier_2_papers: 3
      confidence: "HOCH"
      mechanism: "Motivation Crowding-Out"
      replication: "Konzeptuell repliziert in 5+ Domains"

    - finding: "Strassenausbau → kein Netto-Effekt auf Stau"
      direction: "NULL"
      effect_size: "ε = 1.0"
      tier_1_papers: 1
      tier_2_papers: 2
      confidence: "HOCH"
      mechanism: "Induced Demand"
      replication: "International repliziert"
```

#### 10.2 PRO/CONTRA Bilanz (PFLICHT)

```yaml
synthesis:
  pro_contra:
    hypothesis: "[Haupthypothese aus Forschungsfrage]"

    pro:
      count: 0            # Anzahl PRO-Papers
      tier_1: 0           # Davon Tier 1
      key_findings: []    # Stichworte
      strongest_paper: "" # BibTeX-Key des stärksten PRO-Papers

    contra:
      count: 0
      tier_1: 0
      key_findings: []
      strongest_paper: ""

    weighted_verdict: ""  # PRO überwiegt / CONTRA überwiegt / Gemischt
    confidence: ""        # HOCH / MITTEL / NIEDRIG
    context_dependency: "" # Wann gilt PRO, wann CONTRA?
```

**VERBOTEN:**
```
❌ Nur PRO-Evidenz sammeln (Confirmation Bias)
❌ CONTRA nicht aktiv suchen
❌ Papers zählen statt wiegen (Tier 1 > 3× Tier 3)
```

**GEWICHTUNG:**
```
Tier 1 Paper = 3 Stimmen
Tier 2 Paper = 2 Stimmen
Tier 3 Paper = 1 Stimme
Repliziert   = × 1.5
```

#### 10.3 Parameter-Aggregation

```yaml
synthesis:
  parameter_aggregation:
    - parameter_id: "PAR-INF-001"
      symbol: "γ_crowd"
      papers_count: 4
      range: [-0.68, -0.35]
      weighted_mean: -0.51
      confidence: "HIGH"
      note: "Konsistent über Studien"

    - parameter_id: "NEW"
      symbol: "Δ_frame"
      papers_count: 0
      range: [8, 20]
      weighted_mean: 14
      confidence: "LOW — LLMMC Prior"
      note: "GAP: Kein direktes Experiment"
```

### Schritt 11: GAP-ANALYSE

Claude identifiziert systematisch:

```yaml
gaps:
  empirical:
    - gap: ""
      importance: "HIGH"     # HIGH / MEDIUM / LOW
      researchable: true     # Kann erforscht werden?
      suggested_design: ""   # RCT, natürliches Experiment, etc.

  theoretical:
    - gap: ""
      importance: ""
      connects_to: ""        # Welche EBF-Theorie betroffen?

  methodological:
    - gap: ""
      importance: ""

  contextual:
    - gap: ""
      missing_context: ""    # Welches Land/Branche/Setting fehlt?
```

### Schritt 12: REPORT SCHREIBEN

Claude generiert den Report automatisch:

**Speicherort:**
```
outputs/literature-analyses/SLA-{ID}/
├── SLA-{ID}_report_v1.md          # Report
├── SLA-{ID}_evidence_table.yaml   # Kodierungstabelle
├── SLA-{ID}_prisma.md             # PRISMA-Diagramm (STANDARD+)
└── SLA-{ID}_protocol.yaml         # Symlink/Kopie des Protokolls
```

**Report-Struktur (10 Sektionen):**

```markdown
# [Titel der Literaturanalyse]

## 1. Executive Summary
- Forschungsfrage
- Methodik: N₀ → N₁
- 3-5 Schlüsselbefunde
- Konfidenz-Bewertung

## 2. Einleitung & Forschungsfrage
- PICO/SPIDER
- EBF-Kontext
- Warum relevant?

## 3. Methodik
- Suchstrategie (Quellen, Queries)
- Inklusion-/Exklusionskriterien
- Screening-Verfahren (5-Score)
- Kodebuch (9 Dimensionen)

## 4. PRISMA-Flow (bei STANDARD+)
- Identifiziert → Gescreent → Geprüft → Inkludiert

## 5. Ergebnisse
- Deskriptive Statistik (N₁ nach Tier, Jahr, Methodik)
- Evidenz-Synthese-Tabelle
- Narrativ nach Mechanismen

## 6. PRO/CONTRA Bilanz
- Gewichtete Evidenz
- Konfidenz pro Befund

## 7. Gap-Analyse
- Empirische Lücken
- Theoretische Lücken
- Kontextuelle Lücken

## 8. EBF-Integration
- Neue/aktualisierte Parameter
- Neue Cases
- Cross-References

## 9. Schlussfolgerungen
- Antwort auf Forschungsfrage
- Implikationen für Praxis
- Forschungsbedarf

## Anhang
- A: Vollständige Kodierungstabelle
- B: Exklusions-Log
- C: Bibliographie
```

**RAPID:** Sektionen 1, 5, 6, 9 (3-pager)
**STANDARD:** Alle Sektionen (10-pager)
**SYSTEMATIC:** Alle Sektionen + detaillierter Anhang (30-pager)

**Report in output-registry.yaml registrieren:**

```yaml
# data/output-registry.yaml - Neuer Eintrag
- id: "EBF-OUT-SLA-NNN"
  type: "literature_analysis"
  sla_id: "SLA-YYYY-MM-DD-TOPIC-NNN"
  title: ""
  path: "outputs/literature-analyses/SLA-{ID}/"
  format: "markdown"  # oder "latex"
  date: "YYYY-MM-DD"
  papers_analyzed: 0  # N₁
```

### Schritt 13: EBF-INTEGRATION

Für jedes neue Paper (nicht bereits in bcm_master.bib):

```bash
# 13.1 Papers integrieren
# Für jedes neue Paper aus der externen Suche:
# → /integrate-paper --doi <DOI> (automatisch Level bestimmen)
# ODER bei vielen Papers: Batch-BibTeX-Eintrag erstellen

# 13.2 Parameter aktualisieren
# Neue Parameter aus parameter_aggregation → data/parameter-registry.yaml
# Bestehende Parameter: Werte updaten wenn bessere Evidenz

# 13.3 Cases hinzufügen (wenn neue Cases identifiziert)
# → /case-manage add

# 13.4 BCM2-Kontextdaten (wenn neue Faktoren gefunden)
# → Neuen Faktor in passendem BCM2_04_KON_*.yaml

# 13.5 Cross-References
# → Relevante Appendices verlinken
# → theory-catalog.yaml updaten wenn neue theory_support
```

### Schritt 14: COMMIT + PUSH

```bash
# Alle SLA-Dateien committen
git add data/literature-analyses/SLA-*.yaml \
        outputs/literature-analyses/SLA-*/ \
        data/output-registry.yaml \
        bibliography/bcm_master.bib \
        data/parameter-registry.yaml \
        data/case-registry.yaml

git commit -m "feat(SLA): [Titel] (SLA-{ID})

Systematic Literature Analysis:
- Mode: [RAPID|STANDARD|SYSTEMATIC]
- Papers: N₀=[X] identified → N₁=[Y] included
- Key finding: [1-Satz Zusammenfassung]
- New parameters: [PAR-xxx] / New cases: [CAS-xxx]
- Gaps identified: [Anzahl]

https://claude.ai/code/session_xxx"

git push -u origin <branch>
```

---

## Validierung (PFLICHT vor Schritt 14)

**Manuelle Checkliste (Claude prüft alle Punkte):**

```
PHASE 0-5 (Protokoll → Suche → Screening):
☐ Forschungsfrage SMART (PICO/SPIDER)?
☐ Kriterien VOR Suche definiert?
☐ ≥3 Quellen durchsucht?
☐ Interne Quellen ZUERST?
☐ Jede Exklusion begründet (EX-Code)?
☐ Screening-Score für jedes Paper?

PHASE 3-4 (Kodierung → Synthese):
☐ Alle N₁ Papers nach 9 Dimensionen kodiert?
☐ Evidenz-Synthese-Tabelle vollständig?
☐ PRO + CONTRA BEIDE dokumentiert?
☐ CONTRA aktiv gesucht (nicht nur PRO)?
☐ Konfidenz für jeden Befund bewertet?
☐ Gap-Analyse durchgeführt?

PHASE 5-6 (Report → Integration):
☐ Report in output-registry.yaml registriert?
☐ Neue Papers via /integrate-paper integriert?
☐ Neue Parameter in parameter-registry.yaml?
☐ Protokoll-YAML vollständig (status: completed)?
☐ Git commit + push?
```

---

## PFLICHT-Regeln

**JEDE Literaturanalyse MUSS durch den 14-Schritt Workflow.**

**VERBOTEN:**
```
❌ "Hier sind 10 relevante Papers" ohne Suchprotokoll
❌ Ad-hoc Paper-Liste ohne Screening-Scores
❌ Nur PRO-Evidenz (Confirmation Bias)
❌ Exklusion ohne EX-Code Begründung
❌ Google als EINZIGE Quelle (intern zuerst!)
❌ Effektstärken ignorieren (nur narrative Zusammenfassung)
❌ Gap-Analyse weglassen
❌ Papers finden aber nicht in EBF integrieren (Phase 6!)
❌ Report ohne output-registry.yaml Registrierung
```

**ERLAUBT / ERFORDERLICH:**
```
✅ IMMER /literature-analysis bei Themenfrage
✅ IMMER Protokoll-YAML VOR der Suche
✅ IMMER 5-Score Screening für jedes Paper
✅ IMMER PRO + CONTRA aktiv suchen
✅ IMMER Screening-Entscheidungen dokumentieren
✅ IMMER Gap-Analyse (empirisch + theoretisch)
✅ IMMER neue Papers ins EBF integrieren
✅ IMMER am Ende committen und pushen
```

---

## Unterschied zu verwandten Skills

| Skill | Fokus | Input | Output |
|-------|-------|-------|--------|
| **`/literature-analysis`** | **Thema** analysieren (N Papers) | Forschungsfrage | Synthese-Report + EBF-Integration |
| `/integrate-paper` | **Einzelnes Paper** ins EBF | Paper (DOI/Titel) | BibTeX + YAML + Cases |
| `/add-paper` | **Paper aufnehmen** (schnell) | DOI | PIP-Datei + BibTeX |
| `/paper-search` | **Papers finden** | Keywords | Kandidatenliste |
| `/upgrade-paper` | **Content Level** erhöhen | Paper-ID | L1→L2→L3 |

---

## Workflow-SSOT

> Vollständige Dokumentation: `docs/workflows/literature-analysis-workflow.md`
> Protokoll-Template: `data/literature-analyses/template.yaml`
> Report-Template: `templates/sla-report-template.md`
