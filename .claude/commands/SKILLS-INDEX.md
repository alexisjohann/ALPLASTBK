# Claude Code Skills Index

Übersicht aller verfügbaren Slash-Commands für das EBF-Projekt.

## Single Source of Truth (SSOT)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  SKILL DOCUMENTATION ARCHITECTURE                                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  data/skill-registry.yaml        ← SSOT (maschinenlesbar)              │
│       ↓                                                                 │
│  .claude/commands/SKILLS-INDEX.md  ← Menschenlesbare Übersicht         │
│       ↓                                                                 │
│  .claude/commands/*.md           ← Detaillierte Skill-Dokumentation    │
│       ↓                                                                 │
│  CLAUDE.md (Slash Commands)      ← Quick Reference                     │
│       ↓                                                                 │
│  Appendix SK (REF-SKILLS)        ← EBF-Dokumentation (formal)          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**SSOT:** `data/skill-registry.yaml` (42 Skills, 8 Kategorien)

**Bei Änderungen:**
1. Zuerst `skill-registry.yaml` aktualisieren
2. Dann SKILLS-INDEX.md anpassen
3. CLAUDE.md Quick Reference aktualisieren
4. Bei neuen Skills: Appendix SK referenzieren

---

## 📊 Data Management Skills

### `/classify-papers` - Extract Papers klassifizieren ⚠️ DEPRECATED
**Klassifiziere 138 extrahierte Papers gegen paper-sources.yaml (DEPRECATED → use /integrate-paper)**

- 90 Direct Matches via Fuzzy Matching (65.2%)
- 48 Fallback Mappings via Domain (34.8%)
- 100% Coverage mit Confidence Scoring
- Version: 1.2.0

**Datei:** `.claude/commands/classify-papers.md`

---

## 📚 Literature Management Skills

### `/generate-paper` - Paper aus Kapitel/Appendix generieren
**Generiere formale Papers im Fehr/Thaler/Kahneman Style**

- Aus Kapitel-Auswahl
- Mit Style-Varianten (fehr, thaler, kahneman, sunstein)
- PDF-Kompilierung automatisch

**Datei:** `.claude/commands/generate-paper.md`

---

## 📝 Document Creation Skills

### `/new-chapter` - Neues Kapitel erstellen
**Erstelle ein neues Kapitel nach Template mit allen Compliance-Elementen**

- Automatisches Compliance-Checking (85%+ erforderlich)
- Typ-spezifisches Template (A/B/C)
- Navigation-Updates automatisch

**Datei:** `.claude/commands/new-chapter.md`

### `/new-appendix` - Neuen Appendix erstellen
**Erstelle einen neuen Appendix mit vollständiger Integration**

- 8 Kategorien (CORE, FORMAL, DOMAIN, CONTEXT, METHOD, PREDICT, LIT, REF)
- Cross-Reference Management
- Index-Updates automatisch

**Datei:** `.claude/commands/new-appendix.md`

### `/swsm` - Structured Writing Structure Model
**Text-Analyse und -Generierung mit SFL + RST + CARS**

- **Analyse**: Move-Tagging, Kohäsion, RST-Parsing, Info-Struktur
- **Generierung**: 8D → Genre → Move-Sequenz → Text
- **Qualität**: Move Coverage, Kohäsions-Score, RST-Tiefe
- 9 Engines (E1-E9), 6 Genres

**Datei:** `.claude/commands/swsm.md`

---

## ✅ Quality Assurance Skills

### `/check-compliance` - Template-Compliance prüfen
**Prüfe Kapitel- oder Appendix-Compliance gegen Template**

- Score ≥85% erforderlich für Commits
- Fehlende Elemente mit Empfehlungen
- Kapitelttyp-spezifische Checks

**Datei:** `.claude/commands/check-compliance.md`

### `/validate` - Alle Validierungen ausführen
**Führe vollständigen Validierungs-Check durch**

- 10C-Framework-Konsistenz
- Appendix-Index-Integrität
- Cross-Reference-Validierung
- Compliance-Scores

**Datei:** `.claude/commands/validate.md`

---

## 🏗️ Build & Compilation Skills

### `/compile` - LaTeX → PDF kompilieren
**Kompiliere LaTeX-Dateien zu PDF mit latexmk**

- Automatische Dependency-Auflösung
- Error-Reporting
- Draft/Final Mode

**Datei:** `.claude/commands/compile.md`

### `/convert` - Format konvertieren
**Konvertiere zwischen LaTeX, Word, Markdown mit pandoc**

- LaTeX ↔ Markdown
- LaTeX → Word/PDF
- Formatierung beibehalten

**Datei:** `.claude/commands/convert.md`

### `/build-all` - Alle Papers kompilieren
**Kompiliere alle outputs/ PDFs mit paralleler Verarbeitung**

- Batch-Processing
- Error-Summary
- Zeit-Optimierung

**Datei:** `.claude/commands/build-all.md`

---

## 🧠 Behavioral Model Skills

### `/design-model` - Verhaltensmodell designen
**Designiere ein 10C-Modell mit EEE Workflow**

- 4 Modi: SCHNELL / GEFÜHRT / TEMPLATE / CUSTOM
- 9 Steps mit 3+1 Choice Architecture
- GGG Configurator + FFF Registry
- Testbare Vorhersagen

**Datei:** `.claude/commands/design-model.md`

### `/design-intervention` - EBF-konforme Intervention erstellen (NEU)
**Erstelle Interventionen nach 20-Field Schema (Kapitel 17)**

- 3 Modi: Light (10 min) / Hybrid (30 min) / Profound (60 min)
- Interventionen als Vektoren $\vec{I} \in [0,1]^9$ im 10C-Raum
- Phase-Dimension Affinity Matrix (Chapter 18)
- Segment-Multiplier Matrix (Chapter 19)
- Crowding-Out Prüfung (Social+Financial, Financial+Commitment)
- Validierung: Score ≥ 85% erforderlich

**Datei:** `.claude/commands/design-intervention.md`

---

## 📈 Customer Strategy Skills (NEW 2026)

### `/new-customer` - Neue Customer-Datenbank erstellen
**Erstelle parametrisches Kundenmodell in < 1 Minute**

- Automatische 4-Modell-Initialisierung
- RPM, MCSM, OSM, CAM vorbereitet
- Ready für `/apply-models`

**Datei:** `.claude/commands/new-customer.md`

### `/apply-models` - Alle 4 Modelle ausführen
**Führe Revenue, Headcount, Org, Capital Modelle aus**

- 2-5 Minuten für vollständige Analyse
- CSVs + Charts in outputs/
- Monte-Carlo für Unsicherheit

**Datei:** `.claude/commands/apply-models.md`

### `/sensitivity-analysis` - Parameter-Auswirkungen testen
**Was-Wenn Analysen für Modellparameter**

- < 2 Minuten für vollständige Matrix
- Alle Parameter oder einzeln
- Report mit Tornado-Diagrammen

**Datei:** `.claude/commands/sensitivity-analysis.md`

### `/board-presentation` - Board-ready Präsentation generieren
**Generiere 10-Slide PDF für Executive Presentation**

- Executive Summary
- Key Findings & Recommendations
- Visuals + Charts
- 1-2 Minuten

**Datei:** `.claude/commands/board-presentation.md`

### `/replicate-customer` - Von Template replizieren
**Repliziere Kundenmodell von ALPLA in 4-6 Stunden**

- Schnelle Modellentwicklung
- Validated Foundation
- Ready für Anpassungen

**Datei:** `.claude/commands/replicate-customer.md`

---

## 📋 Case & Intervention Registry Skills

### `/case` - Case Registry abfragen
**Suche in 10C-indizierter Case-Datenbank**

- Nach Domain, Stage, Dimension filtern
- Case-Details mit Predictions
- Linked Papers & Learnings

**Datei:** `.claude/commands/case.md`

### `/case-manage` - Cases finden & speichern
**Manage Case Identification & Long-Term Outcomes**

- Cases für neue Projekte finden
- Results & Learnings erfassen
- Integration mit Intervention Registry

**Datei:** `.claude/commands/case-manage.md`

### `/intervention` - Intervention Registry abfragen
**Suche Project Portfolio & Learnings**

- Aktive Interventionen
- Abgeschlossene Projekte
- Deviation Analysis & Insights

**Datei:** `.claude/commands/intervention-manage.md`

### `/intervention-manage` - Projekte verwalten
**Erstelle, Update & Close Intervention Projekte**

- Mit Predictions & Results
- Learning Erfassung
- Outcomes Tracking

**Datei:** `.claude/commands/intervention-manage.md`

---

## 🔧 Utility Skills

### `/r-score` - LLMMC → R-Score Pipeline
**Berechne R-Scores aus LLM Monte Carlo Output**

- Robustness quantifizieren
- Threshold-Testing
- Report-Generierung

**Datei:** `.claude/commands/r-score.md`

### `/bayesian-priors` - Prior Generation
**Generiere Bayesian Priors aus Paper Robustness**

- Aus Literatur-Evidenz
- Hierarchische Priors
- Parameter-Distributions

**Datei:** `.claude/commands/bayesian-priors.md`

---

## 📖 How to Use Skills

### Invoking a Skill
```bash
/skill-name [arguments]
/classify-papers --dry-run
/design-model --mode schnell
/new-customer "CompanyX" 1500 "Europe,APAC"
```

### Skill Documentation
Alle Skills haben vollständige Dokumentation mit:
- ✓ Beschreibung & Kurzbeschreibung
- ✓ Verwendungs-Beispiele
- ✓ Schritt-für-Schritt Anweisungen
- ✓ Schwellenwerte & Metriken
- ✓ Troubleshooting-Tipps
- ✓ Integration mit Git

### Finding Skills
```bash
# In Claude Code Web/CLI:
/help                  # Zeigt alle verfügbaren Skills
ls .claude/commands/   # Alle .md Dateien = Skills
```

---

## 📊 Skills by Domain

### Data Preparation & Classification
- `/classify-papers` - Extract Papers klassifizieren

### Document Creation & Management
- `/new-chapter` - Neues Kapitel
- `/new-appendix` - Neuer Appendix
- `/generate-paper` - Paper generieren

### Quality & Validation
- `/check-compliance` - Compliance prüfen
- `/validate` - Vollständige Validierung

### Build & Output
- `/compile` - LaTeX → PDF
- `/convert` - Format konvertieren
- `/build-all` - Alle PDFs kompilieren

### Behavioral Modeling
- `/design-model` - EEE Workflow (9 Steps)
- `/design-intervention` - 20-Field Schema (NEU)

### Strategic Analysis (Customer Models)
- `/new-customer` - DB erstellen
- `/apply-models` - 4 Modelle laufen
- `/sensitivity-analysis` - Was-Wenn Analyse
- `/board-presentation` - 10-Slide Deck
- `/replicate-customer` - Von Template

### Registries & Learning
- `/case` - Case suchen
- `/case-manage` - Cases verwalten
- `/intervention` - Interventionen suchen
- `/intervention-manage` - Interventionen managen
- `/bfe-project` - BFE-Projekte erstellen & verwalten
- `/innosuisse` - Innosuisse/BEATRIX Workflow (NEU, AUTO-TRIGGER)

### Analysis & Metrics
- `/r-score` - Robustness Score
- `/bayesian-priors` - Prior Generation

---

## 🏢 Client Project Skills (NEW 2026)

### `/innosuisse` - Innosuisse Projekt-Workflow (BEATRIX) (NEU)
**PFLICHT-Workflow für alle BEATRIX/Innosuisse Aufgaben**

- **AUTOMATISCH AKTIVIERT** bei Trigger (docs/funding/, "BEATRIX", "Innosuisse")
- 8 Fehlertypen mit Präventions-Checkliste
- 7-Stellen Checkliste für Kernaussagen
- 3-Stellen Checkliste für Versionsnummern
- Ernst Fehr BEATRIX-Korrektur integriert
- Lerndatenbank-Integration

**Beispiele:**
```
/innosuisse                    # Workflow starten
/innosuisse check              # Lerndatenbank konsultieren
/innosuisse query --error-type CONSISTENCY
/innosuisse add                # Neues Learning hinzufügen
```

**Datei:** `.claude/commands/innosuisse.md`

### `/bfe-project` - BFE Projekte erstellen & verwalten (NEU)
**Erstelle und verwalte BFE-Interventionsprojekte mit 10C-Workflow**

- 2 Modi: SCHNELL (5 min) / VOLLSTÄNDIG (20 min)
- Automatische Kontext-Selektion aus MESO/MAKRO
- Projekt-Lifecycle: new → status → close
- Learning Loop zurück in Kontextvektoren
- Crowding-Out Prüfung integriert

**Beispiele:**
```
/bfe-project new              # Interaktiv erstellen
/bfe-project new --schnell    # Schnellmodus (5 Fragen)
/bfe-project list             # Alle Projekte anzeigen
/bfe-project status BFE-2026-001
/bfe-project close BFE-2026-001
```

**Datei:** `.claude/commands/bfe-project.md`

---

## 🔗 Quick Links

| Element | Link |
|---------|------|
| **Skills Directory** | `.claude/commands/` |
| **This File** | `.claude/commands/SKILLS-INDEX.md` |
| **README** | `.claude/commands/README.md` |
| **Project Docs** | `docs/` |
| **CLAUDE.md** | `CLAUDE.md` |

---

Version 1.3 | Januar 27, 2026 | Claude Code

**v1.3:** Added `/innosuisse` (BEATRIX PFLICHT-Workflow mit Auto-Trigger)
**v1.2:** Added `/bfe-project` (BFE Projekt-Workflow mit Learning Loop)
**v1.1:** Added `/design-intervention` (20-Field Schema, Chapters 17-20)
