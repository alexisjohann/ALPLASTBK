# EBF Database Schemas — Vollständige Dokumentation

> **Single Source of Truth für alle 5 Datenbanken des EBF Frameworks**

**Status:** ✅ Alle 5 Schemas standardisiert und dokumentiert (Januar 18, 2026)

---

## 📋 Übersicht: Die 5 Datenbanken

Das EBF Framework nutzt **5 integrierte Datenbanken**, jede mit einem **autoritative Schema**:

| # | Datenbank | Einträge | Schema-Datei | Status |
|---|-----------|----------|--------------|--------|
| **1** | **Paper-Sources Registry** | 1,784 Papers | `data/paper-sources.schema.yaml` | ✅ v1.0 |
| **2** | **Case Registry** | 100+ Cases | `data/case-registry.schema.yaml` | ✅ v1.0 |
| **3** | **Intervention Registry** | 50+ Projects | `data/intervention-registry.schema.yaml` | ✅ v1.0 |
| **4** | **Model Registry** | 38+ Models | `models/models.schema.yaml` | ✅ v1.0 |
| **5** | **Stakeholder Models** | 2+ Companies | `data/stakeholder-models/stakeholder-models.schema.yaml` | ✅ v1.0 |

---

## 🔑 Die 5 Schemas im Detail

### 1️⃣ **Paper-Sources Registry Schema**
📁 `data/paper-sources.schema.yaml` (560 Zeilen)

**Zweck:** 1,784 wissenschaftliche Arbeiten von 1972-2026 mit vollständiger 10C-Indizierung

**Hauptentitäten:**
- `Paper`: Bibliographische Metadaten + Abstrakt + Volltext-URLs
- `KeyFinding`: Empirische Ergebnisse pro Paper
- `NineC_Coordinates`: Mapping zu 10C Framework (domain, stages, primary_dimension, gamma, A_level, W_level)
- `LitAppendixMapping`: Verknüpfung zu LIT-/REF-Appendices (A-Z)
- `LinkedCase`: Verweise zu Case Registry Einträgen
- `Validation`: Verifikationsstatus, evidence_tier (1-5), quality_score

**Kritische Constraints:**
- Alle Paper-IDs müssen eindeutig sein
- Mindestens ein 10C-Koordinat pro Paper
- Gamma ∈ [-1.0, 1.0]
- A_level, W_level ∈ [0.0, 1.0]
- High-relevance Papers sollten case_count > 0 haben

**Beispiel-Eintrag:**
```yaml
kahneman1979prospect:
  authors: [Kahneman, Daniel; Tversky, Amos]
  year: 1979
  title: "Prospect Theory: An Analysis of Decision under Risk"
  key_findings:
    - finding: "Loss aversion: λ = 2.25"
      domain: finance
      stage: contemplation
      primary_dimension: E
      effect_size: 2.25
  9c_coordinates:
    - domain: finance
      gamma: 0.5
      A_level: 0.6
      W_level: 0.5
  linked_cases: [CASE-010, CASE-012, ...]
```

---

### 2️⃣ **Case Registry Schema**
📁 `data/case-registry.schema.yaml` (850+ Zeilen)

**Zweck:** 100+ reale Anwendungsbeispiele mit vollständiger 10C-Spezifikation

**Hauptentitäten:**
- `Case`: Master-Datensatz mit Name, Beschreibung, Superkey
- `NineC_Specification`: **KOMPLETTES 10C-Mapping** für jeden Case:
  - **WHO:** Welfare levels (L0-L3) + Segments
  - **WHAT:** FEPSDE-Dimensionen + Gewichte
  - **HOW:** Komplementarität γ (inkl. γ-Matrix)
  - **WHEN:** Kontext (Ψ) - framing, social_context, scarcity, etc.
  - **WHERE:** Datenquellen + Confidence
  - **AWARE:** A_level + awareness_type
  - **READY:** W_level + θ + Barriers & Facilitators
  - **STAGE:** Behavior change phase + Stabilität
  - **HIERARCHY:** Welfare level interactions + strategic_ordering
- `Formula`: Quantitative Formalisierung (LaTeX) mit Variablendefinitionen
- `InsightAndImplication`: Insights + policy implications + transferability
- `References`: Verknüpfungen zu Appendices, Chapters, Papers, Interventions
- `SourceTracking`: Herkunft (Paper oder Project) + Verifikationsstatus

**Kritische Constraints:**
- Superkey-Format: `domain:subtype:L#:concept:context:intervention_type`
- Alle 10C Dimensionen sollten adressiert sein
- Gamma ∈ [-1.0, 1.0]
- Awareness/Willingness ∈ [0.0, 1.0]
- Formeln müssen vollständig definierte Variablen haben

**Beispiel-Eintrag:**
```yaml
CASE-001:
  name: "Internalisierte vs. Externalisierte Komplexität"
  superkey: "anthropology:structural:L2:complexity:cross-cultural:culture"
  10C:
    WHO:
      levels: [individual, society]
      heterogeneity: high
    WHAT:
      dimensions: [S, E]
      primary: cognitive_load
    HOW:
      gamma_avg: 0.6
    ...
  formula:
    - name: "L2-Formel (Westlich)"
      formula: "N_L2 = 1.0 × 0.4 × 100 × (1-0.7) / log(100) ≈ 2.6"
      variables: {alpha: 1.0, gamma_avg: 0.4, n: 100, m: 0.7}
```

---

### 3️⃣ **Intervention Registry Schema**
📁 `data/intervention-registry.schema.yaml` (900+ Zeilen)

**Zweck:** 50+ behavior change Projekte mit Predictions, Results & Learnings

**Hauptentitäten:**
- `ProjectMetadata`: Name, Client, Domain, Start/End Dates, Budget
- `Context`: Target behavior, population, baseline rate, sample size, segments
- `InterventionComponent`: Einzelne Interventionen mit:
  - Type: nudge, incentive, institutional, information, education, social
  - Subtype: default, opt_out, salience, personalized_projection, norm, etc.
  - Parameters: intensity, duration, frequency, cost
  - Expected contribution: E_i ∈ [0, 1], confidence, source, mechanism
- `ComplementarityPair`: Wechselwirkungen zwischen Interventionen:
  - γ_ij ∈ [-1.0, 1.0]
  - Interaction type: synergy, substitutable, independent, antagonistic
- `Predictions`: Erwartete Effekte:
  - Portfolio effect: E_P = Σ E_i + Σ γ_ij × √(E_i × E_j)
  - KPI-Vorhersagen mit Baselines, predicted_value, predicted_delta
- `Results`: Tatsächlich gemessene Outcomes:
  - Actual KPI values
  - Intervention effects mit attribution_confidence
  - Unintended consequences
- `DeviationAnalysis`: Prediction vs. Reality Analyse:
  - Overall delta (actual - predicted)
  - By-intervention breakdown
  - By-segment breakdown
  - Explanation of deviations
- `Learnings`: Schlüsseleinsichten:
  - what_worked + transferability
  - what_didn't_work
  - unexpected_effects
  - segment_heterogeneity
  - implementation_insights
  - **theory_updates**: Parameter-Aktualisierungen für BBB (Parameter Repository)

**Kritische Constraints:**
- Status-Workflow: planned → in_progress → completed (or paused/cancelled)
- Segment proportions MÜSSEN sich zu 1.0 summieren (±0.05)
- Intervention IDs müssen konsekutiv sein: I1, I2, I3, ...
- Completed projects MÜSSEN Results & DeviationAnalysis haben
- Portfolio-Formel: E_P = Σ E_i + Σ γ_ij × √(E_i × E_j)
- Paper-Referenzen müssen in paper-sources.yaml existieren
- Case-Referenzen müssen in case-registry.yaml existieren

**Beispiel-Eintrag:**
```yaml
PRJ-001:
  meta:
    name: "Betriebliche Altersvorsorge Opt-Out Implementation"
    client: "Mittelständisches Unternehmen (500 MA)"
    domain: finance
    start_date: '2025-03-01'
    end_date: '2025-09-30'
    status: completed

  context:
    target_behavior: "Teilnahme an bAV"
    baseline_behavior: 0.34
    sample_size: 312
    segments:
      - {name: present-biased, proportion: 0.45, sigma: 1.8}
      - {name: loss-averse, proportion: 0.30, sigma: 1.5}
      - {name: rational, proportion: 0.25, sigma: 0.8}

  intervention_mix:
    - id: I1
      type: nudge
      subtype: default
      expected_contribution: {E_i: 0.35, confidence: 0.85, source: literature}
    - id: I2
      type: information
      subtype: personalized_projection
      expected_contribution: {E_i: 0.08, confidence: 0.60, source: pilot}
    - id: I3
      type: social
      subtype: descriptive_norm
      expected_contribution: {E_i: 0.05, confidence: 0.50, source: literature}

  complementarity_matrix:
    - pair: [I1, I2]
      gamma_ij: 0.3
      interaction: synergy
      mechanism: "Default + Information verstärkt informierte Akzeptanz"

  predictions:
    portfolio_effect:
      E_P: 0.52
      CI_lower: 0.42
      CI_upper: 0.62
      formula_used: "E(P) = Σ E_i + Σ γ_ij · √(E_i · E_j)"

  results:
    measurement_date: '2025-09-30'
    kpis:
      - name: "Teilnahmequote bAV"
        actual_value: 0.91
        actual_delta: 0.57
        actual_delta_pct: 168

  deviation_analysis:
    overall:
      predicted_E_P: 0.52
      actual_E_P: 0.57
      delta: 0.05
      delta_pct: 9.6
      direction: underestimate

  learnings:
    what_worked:
      - {finding: "Default enrollment was highly effective", mechanism: "Reduced friction", transferability: high}
    theory_updates:
      parameter_updates:
        - {parameter: "lambda (loss_aversion)", old_value: 2.25, new_value: 2.15, confidence: "high"}
```

---

### 4️⃣ **Model Registry Schema**
📁 `models/models.schema.yaml` (560 Zeilen)

**Zweck:** 38+ vorkonfigurierte Modelle mit mathematischer Formalisierung, Validierung & Verbesserungsplan

**Hauptentitäten:**
- `Model`: Master record mit status (STABLE, BETA, EXPERIMENTAL, PLANNED)
- `ModelVersion`: Versionsverlauf + breaking_changes + migration_guide
- `MathematicalModel`: Formale Spezifikation:
  - model_type: LOGISTIC, LINEAR, TREE, NEURAL_NETWORK, BAYESIAN, SIMULATION
  - formula (LaTeX)
  - dimensions mit weights
  - parameters mit confidence_intervals
- `Validation`: Validierung gegen historische Daten:
  - validation_type: HISTORICAL, CROSS_VALIDATION, OUT_OF_SAMPLE, EXPERT_ASSESSMENT
  - metrics: accuracy, precision, recall, f1, calibration_error
  - test_cases: predicted vs. actual
- `Improvement`: Roadmap (PHASE_1 bis PHASE_3) mit success_criteria
- `Dimension`: Einzelne Modellvariablen mit weight, measurement_method, data_sources
- `DataPoint`: Historische Observations
- `Limitation`: Bekannte Limitationen mit fix_strategy & improvement_id

**Kritische Constraints:**
- Model IDs: Pattern `^[A-Z]+-[A-Z0-9]+(-[0-9]{4})?$`
- Status-Workflow: PLANNED → EXPERIMENTAL → BETA → STABLE (keine Rückwärtsbewegung außer zu BETA)
- Dimension-Gewichte MÜSSEN sich zu ~1.0 summieren (±0.05)
- Jedes Modell MUSS ≥1 Validierung haben
- Improvement-Timelines müssen explizit sein (kein "soon" oder "später")
- Versioning: semantic versioning (MAJOR.MINOR[.PATCH])

---

### 5️⃣ **Stakeholder Models Schema**
📁 `data/stakeholder-models/stakeholder-models.schema.yaml` (750+ Zeilen)

**Zweck:** Customer/Company-spezifische Modelle mit KPIs, Szenarien, Monte Carlo & Sensitivitätsanalysen

**Hauptentitäten:**
- `CompanyProfile`: Name, Industry, Region, Employees, Revenue, Headquarters
- `BusinessAssumptions`: Kernfinanzielle Annahmen:
  - Revenue growth (CAGR %)
  - Profitability (EBITDA margin, operating margin, net margin)
  - Capital structure (CapEx intensity, debt/EBITDA, equity return)
  - Labor costs (wage inflation, productivity, headcount growth)
  - Operational (COGS %, SGA %, R&D %)
  - Market (market share, market growth, competitive position)
- `StrategicRoadmap`: Multi-year initiatives + milestones + divestitures
- `Scenario`: Alternative Annahmen (Base Case, Best Case, Downside, Stress Test):
  - assumption_overrides
  - probability ∈ [0, 1]
  - timeline
- `OperatingModel`: Organisationsstruktur:
  - business_units mit revenue_contribution, margin, growth, headcount
  - cost_centers mit annual_cost, allocation_basis
  - shared_services mit cost_per_transaction
- `KPI_Definition`: Tracking-Metriken mit formula, source, tracking_frequency, targets
- `MonteCarloResults`: Probabilistische Simulationen (10,000+ Iterationen):
  - KPI distributions: mean, median, std_dev, p10, p90, min, max
  - correlation_matrix
  - scenario_probabilities
- `SensitivityAnalysis`: Parameter-Wichtigkeit:
  - tornado_chart mit impact ranking
  - elasticity_estimates (% change output per 1% change input)
  - critical_thresholds
- `ValueDriverAnalysis`: Was schafft Wert?
  - revenue_drivers mit contribution %
  - cost_structure
  - cash_conversion
  - return_metrics (ROIC, ROE, ROA)
- `OutputDocuments`: Generierte Reports (board_presentation, financial_model, sensitivity_reports)
- `ModelLineage`: Herkunft + seed_model + template_source + derived_from_stakeholder
- `ValidationMetadata`: QA-Status, assumptions_reviewed, stakeholder_sign_off, quality_score

**Kritische Constraints:**
- Revenue CAGR ∈ [-20%, +50%]
- EBITDA margin ∈ [-100%, +100%]
- CapEx intensity ∈ [0%, 100%]
- Scenario probabilities summieren sich zu 1.0 (±0.05)
- Monte Carlo: iterations ≥ 1,000
- Percentiles: p10 < median < p90
- Business unit revenues summieren sich zu ~100% (±5%)
- Correlation matrix symmetric + diagonal = 1.0

---

## 🔄 Beziehungen zwischen Datenbanken

```
┌─────────────────────────────────────────────────────────────────┐
│ PAPER-SOURCES (1,784)                                           │
│ ├─ linked_cases → CASE-REGISTRY                                 │
│ ├─ lit_appendix → Appendix codes (A-Z)                          │
│ └─ used_in_models → MODEL-REGISTRY                              │
└─────────────────────────────────────────────────────────────────┘
         ↓ (parameters θ)
┌─────────────────────────────────────────────────────────────────┐
│ MODEL-REGISTRY (38+ models)                                     │
│ ├─ seed_models → used by INTERVENTION-REGISTRY                  │
│ └─ used_by_stakeholders → STAKEHOLDER-MODELS                    │
└─────────────────────────────────────────────────────────────────┘
         ↓ (predictions)
┌─────────────────────────────────────────────────────────────────┐
│ INTERVENTION-REGISTRY (50+ projects)                            │
│ ├─ linked_papers → PAPER-SOURCES                                │
│ ├─ linked_cases → CASE-REGISTRY                                 │
│ ├─ model_seed → MODEL-REGISTRY                                  │
│ ├─ case_created → CASE-REGISTRY (new case from results)         │
│ └─ theory_updates → BBB (Parameter Repository)                  │
└─────────────────────────────────────────────────────────────────┘
         ↓ (learnings)
┌─────────────────────────────────────────────────────────────────┐
│ CASE-REGISTRY (100+ cases)                                      │
│ ├─ linked_papers → PAPER-SOURCES                                │
│ ├─ source_paper → PAPER-SOURCES                                 │
│ ├─ source_project → INTERVENTION-REGISTRY                       │
│ ├─ references.appendices → Appendix codes                       │
│ └─ references.chapters → Chapter numbers (1-19)                 │
└─────────────────────────────────────────────────────────────────┘
         ↓ (customer data)
┌─────────────────────────────────────────────────────────────────┐
│ STAKEHOLDER-MODELS (2+ companies)                               │
│ ├─ seed_model → MODEL-REGISTRY                                  │
│ ├─ template_source → MODEL-TEMPLATES                            │
│ └─ derived_from_stakeholder → STAKEHOLDER-MODELS (lineage)      │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📊 Schema-Vergleich: Key Statistics

| Aspekt | Paper-Sources | Case | Intervention | Model | Stakeholder |
|--------|---------------|------|--------------|-------|-------------|
| **Einträge** | 1,784 | 100+ | 50+ | 38+ | 2+ |
| **Schema-Größe** | 560 Zeilen | 850+ | 900+ | 560 | 750+ |
| **Hauptentitäten** | 6 | 6 | 8 | 8 | 12 |
| **10C-Mapping** | ✅ Ja (1 pro Paper) | ✅ Ja (vollständig) | ✅ Ja (implizit) | ⚠️ Nein | ⚠️ Nein |
| **Foreign Keys** | 3 (Papers→Cases, Papers→Appendix, Papers→Models) | 5 (Cases→Papers, Cases→Cases, Cases→Interventions, Cases→Appendix, Cases→Chapters) | 7 (Projects→Papers, Projects→Cases, Projects→Model, Projects→Case_created, Projects→Appendix) | 6 (Models→Validations, Models→DataPoints, Models→Improvements, Models→Limitations, Models→Dimensions) | 4 (Stakeholders→Model, Stakeholders→Template, Stakeholders→Stakeholder, Stakeholders→Documents) |
| **Validierungsregeln** | 10 | 10 | 11 | 10 | 10 |
| **Unique Constraints** | 3 | 2 | 2 | 2 | 2 |

---

## ✅ QA-Checklisten pro Schema

### Paper-Sources Checklist
- [ ] Alle 1,784 Paper-IDs sind eindeutig
- [ ] Alle Authors folgen 'FirstName, LastName' Format
- [ ] Alle Papers haben Domäne & 10C-Koordinaten
- [ ] Gamma ∈ [-1, 1]
- [ ] A_level, W_level ∈ [0, 1]
- [ ] High-relevance Papers haben case_count > 0
- [ ] Alle LitAppendix-Codes (A-Z) sind gültig
- [ ] Keine Duplikate

### Case Registry Checklist
- [ ] Alle 100+ Case-IDs sind eindeutig (CASE-XXX)
- [ ] Alle Cases haben Domäne & vollständige 10C-Spezifikation
- [ ] Superkey folgt Hierarchie-Format
- [ ] Gamma ∈ [-1, 1]
- [ ] A_level, W_level ∈ [0, 1]
- [ ] Formeln haben vollständig definierte Variablen
- [ ] Alle Paper-Referenzen existieren
- [ ] Alle Appendix-Referenzen sind valid

### Intervention Registry Checklist
- [ ] Alle 50+ Project-IDs sind eindeutig
- [ ] Alle Projects haben Meta, Context, Intervention_mix
- [ ] Segment-Proportionen = 1.0 (±0.05)
- [ ] Intervention IDs sind konsekutiv (I1, I2, I3, ...)
- [ ] Gamma ∈ [-1, 1]
- [ ] Confidence & attribution_confidence ∈ [0, 1]
- [ ] Completed projects haben Results & DeviationAnalysis
- [ ] Portfolio-Formel korrekt berechnet

### Model Registry Checklist
- [ ] Alle 38+ Model-IDs sind eindeutig
- [ ] Status-Workflow ist korrekt
- [ ] Dimension-Gewichte = 1.0 (±0.05)
- [ ] Jedes Modell hat ≥1 Validierung
- [ ] Improvement-Timelines sind explizit
- [ ] Versioning ist semantic
- [ ] Keine Duplikate

### Stakeholder Models Checklist
- [ ] Alle Company-IDs sind eindeutig
- [ ] Revenue CAGR ∈ [-20%, +50%]
- [ ] EBITDA margin ∈ [-100%, +100%]
- [ ] Szenario-Wahrscheinlichkeiten = 1.0 (±0.05)
- [ ] Monte Carlo: iterations ≥ 1,000
- [ ] Percentiles: p10 < p50 < p90
- [ ] Business unit revenues = 100% (±5%)

---

## 🔧 Workflow: Wie die Schemas zusammen verwendet werden

### Use Case 1: Neues Verhaltensmodell designen
```
1. /design-model → Nutzt MODEL-REGISTRY als Seed
2. Nutzt PAPER-SOURCES für Parameter (WHERE)
3. Speichert Modell in MODEL-REGISTRY
4. Erstellt neuen Eintrag mit 10C-Mapping
```

### Use Case 2: Intervention planen
```
1. /case --domain health → Suche ähnliche CASES
2. /intervention-manage new → Plan basierend auf CASES
3. Nutze PAPER-SOURCES für Literatur-Links
4. Nutze MODEL-REGISTRY für Predictions
5. Nach Durchführung: /intervention-manage close
6. Ergebnisse fließen in CASE-REGISTRY als neuer Case
```

### Use Case 3: Kundenmodell bauen
```
1. /new-customer "CompanyX" → Erstelle in STAKEHOLDER-MODELS
2. Nutze seed_model aus MODEL-REGISTRY
3. /apply-models CompanyX → Führe Monte Carlo aus
4. /sensitivity-analysis → Teste Parameter (alle aus MODEL)
5. /board-presentation → Generiere Report
```

---

## 📝 Versioning & Evolution

Alle 5 Schemas sind **Version 1.0** und dokumentieren:
- **Erstellungsdatum:** 18. Januar 2026
- **Backward Compatibility:** Ja (für zukünftige Versionen)
- **Erweiterungspfad:** Klare Dokumentation für v1.1, v2.0, etc.

**Migrations-Richtlinie:**
- Breaking changes erfordern Major Version Bump (v1.0 → v2.0)
- Neue optionale Felder erlaubt ohne Version Bump
- Alle Migrationen dokumentieren Fallback-Pfade für ältere Daten

---

## 🎯 Nächste Schritte

### Kurz (Diese Woche)
- [ ] Validierungsscripts schreiben für alle 5 Datenbanken
- [ ] YAML-Dateien auf Schema-Konformität prüfen
- [ ] Dokumentation in README.md aktualisieren

### Mittel (Diesen Monat)
- [ ] API/CLI entwickeln für direkten Zugriff auf Datenbanken
- [ ] Automatische Validierungshooks in Pre-Commit
- [ ] Dashboard für Datenbank-Überblick

### Langfristig (Dieses Quartal)
- [ ] Datenmigration zu strukturierter Datenbank (SQLite/PostgreSQL)
- [ ] REST API für programmatischen Zugriff
- [ ] Automatische Cross-Reference-Validierung zwischen Datenbanken

---

## 📚 Referenzen

Alle Schemas sind Self-Contained und dokumentieren:
- ✅ Alle erforderlichen & optionalen Felder
- ✅ Datentypen & Validierungsregeln
- ✅ Foreign-Key Constraints
- ✅ Cardinality Relationships
- ✅ QA-Checklisten
- ✅ Beispiel-Einträge
- ✅ Migrations-Pfade

**Single Source of Truth:**
```
Paper-Sources:       data/paper-sources.schema.yaml
Case Registry:       data/case-registry.schema.yaml
Intervention:        data/intervention-registry.schema.yaml
Model Registry:      models/models.schema.yaml
Stakeholder Models:  data/stakeholder-models/stakeholder-models.schema.yaml
```

---

**Dokumentation v1.0 | Erstellt: 18. Januar 2026**
