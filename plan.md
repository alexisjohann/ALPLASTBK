# GPM-2.0: Goalkeeper Performance Framework — Erweiterung mit wissenschaftlicher Literatur

## Ziel

GPM-1.0 zu GPM-2.0 erweitern durch:
1. Integration von 7 Schlüsselpapieren, die das Leistungsbewertungs-Paradox formal analysieren
2. Formalisierung des **Visibility Framework** (Sichtbarkeits-Paradox)
3. Formalisierung des **Counterfactual Measurement Framework** (V* = GPAR + xG_Buildup)
4. **Position Generalization** (Sichtbarkeits-Spektrum über alle Positionen)
5. Verankerung in **Holmstrom-Milgrom (1991) Multi-Task Theory**

---

## Phase 1: Paper-Integration (7 Schlüsselpapiere)

Folgende Papers in `bibliography/bcm_master.bib` und `data/paper-references/` integrieren:

| # | Paper | BibTeX Key | Level | Begründung |
|---|-------|-----------|-------|------------|
| 1 | Bar-Eli, Azar, Ritov et al. (2007) "Action Bias Among Elite Soccer Goalkeepers" JEBO | `bareli2007action` | Level 3 (CASE) | Direkte empirische Evidenz für Action Bias bei Elfmetern |
| 2 | Palacios-Huerta (2003) "Professionals Play Minimax" RES | `palacioshuerta2003minimax` | Level 2 (STANDARD) | Nash-Gleichgewicht bei Elfmetern, Rationalitäts-Evidenz |
| 3 | Holmstrom & Milgrom (1991) "Multitask Principal-Agent" JLEO | `holmstrom1991multitask` | Level 4 (THEORY) | Theoretisches Fundament für Multi-Task-Verzerrung |
| 4 | Kerr (1975) "On the Folly of Rewarding A While Hoping for B" AMJ | `kerr1975folly` | Level 2 (STANDARD) | Organisationales Fehlausrichtungs-Framework |
| 5 | Rose (1985) "Sick Individuals and Sick Populations" IJE | `rose1985sick` | Level 2 (STANDARD) | Originales Prevention Paradox |
| 6 | Chiappori, Levitt, Groseclose (2002) "Testing Mixed-Strategy" AER | `chiappori2002testing` | Level 2 (STANDARD) | Heterogene Spieler in Mixed-Strategy |
| 7 | Apesteguia & Palacios-Huerta (2010) "Psychological Pressure" AER | `apesteguia2010psychological` | Level 2 (STANDARD) | Reihenfolge-Effekt bei Elfmetern |

**Für jedes Paper:**
- BibTeX-Eintrag mit EBF-Feldern (use_for, theory_support, evidence_tier, parameter)
- PAP-*.yaml in data/paper-references/
- theory_support Verknüpfung zu existierenden Theorien

---

## Phase 2: GPM model-definition.yaml Erweiterung

### 2a. Neuer Abschnitt: `visibility_framework`

```yaml
visibility_framework:
  axiom: "GPM-VIS-1: Observable ≠ Valuable"
  description: |
    Die Sichtbarkeit einer Torhüter-Aktion ist NICHT proportional
    zu ihrem Beitrag zum Teamerfolg. Formalisierung:

    V(a) = Visibility einer Aktion a
    C(a) = Contribution einer Aktion a zum Teamerfolg

    Für Torhüter gilt systematisch:
    Corr(V, C) < 0 für präventive Aktionen
    Corr(V, C) > 0 für reaktive Aktionen

  visibility_spectrum:
    - position: "Stürmer"
      V_C_correlation: 0.85
      explanation: "Tore sind maximal sichtbar UND maximal wertvoll"
    - position: "Offensiver Mittelfeldspieler"
      V_C_correlation: 0.65
      explanation: "Assists sichtbar, aber Raumöffnung unsichtbar"
    - position: "Zentrales Mittelfeld"
      V_C_correlation: 0.35
      explanation: "Ballgewinne teilweise sichtbar, Passnetzwerk-Beitrag unsichtbar"
    - position: "Innenverteidiger"
      V_C_correlation: 0.20
      explanation: "Tackles sichtbar, aber Positionierung und Antizipation unsichtbar"
    - position: "Torhüter"
      V_C_correlation: -0.15
      explanation: "Paraden sichtbar, aber beste Leistung = nichts passiert"

  literature_anchor: "holmstrom1991multitask"
  ebf_connection: "Holmstrom-Milgrom Theorem: Bei Multi-Task mit unterschiedlicher
    Messbarkeit verzerren leistungsbasierte Anreize Effort zu messbaren Aufgaben"
```

### 2b. Neuer Abschnitt: `counterfactual_framework`

```yaml
counterfactual_framework:
  axiom: "GPM-CF-1: Leistung = Beobachtet + Verhindert"
  formula: |
    V*(GK) = V_observed(GK) + V_prevented(GK)

    wobei:
    V_observed = GPAR (Goals Prevented Above Replacement)
                = PSxG_faced - Goals_conceded

    V_prevented = xG_prevented_by_positioning + xG_prevented_by_communication
                + xG_prevented_by_space_compression

    Das Paradox: V_prevented ist der GRÖSSERE Term,
    aber V_observed ist der EINZIGE der gemessen wird.

  measurement_approaches:
    - name: "PSxG / xGOT (Post-Shot Expected Goals)"
      measures: "V_observed (teilweise)"
      limitation: "Erfasst nur Shot-Stopping, nicht Prevention"
      source: "Stats Perform 2025"
    - name: "Goals Prevented (xGP)"
      measures: "V_observed"
      limitation: "Season-to-season Varianz ±0.2/90min"
      source: "Football Innovation Hub 2024"
    - name: "Possession Value Models"
      measures: "V_prevented (teilweise)"
      limitation: "Nur Distribution, nicht Positioning/Communication"
      source: "StatsBomb 2023"
    - name: "Bayesian xGOT"
      measures: "V_observed + partielle V_prevented"
      limitation: "Datenintensiv, noch experimentell"
      source: "Frontiers 2025"
```

### 2c. Neuer Abschnitt: `position_generalization`

```yaml
position_generalization:
  axiom: "GPM-GEN-1: Das Sichtbarkeits-Paradox existiert auf allen Positionen,
    aber mit unterschiedlicher Intensität"

  measurement_paradox_by_position:
    striker:
      paradox_intensity: 0.15  # Niedrig: Tore sind sichtbar UND wertvoll
      invisible_contribution: ["Pressing auslösen", "Räume öffnen für Mitspieler", "Gegner binden"]
      dominant_metric: "Tore + Assists"
      metric_quality: 0.85  # Misst gut, was zählt

    goalkeeper:
      paradox_intensity: 0.95  # Maximal: Beste Leistung = nichts passiert
      invisible_contribution: ["Positionierung", "Kommunikation", "Raumkompression", "Spielaufbau"]
      dominant_metric: "Save Rate / Clean Sheets"
      metric_quality: 0.25  # Misst schlecht, was zählt

    centre_back:
      paradox_intensity: 0.75
      invisible_contribution: ["Laufwege schließen", "Pressing-Trigger", "Kopfball-Dominanz im Raum"]
      dominant_metric: "Tackles + Interceptions"
      metric_quality: 0.35

    defensive_midfielder:
      paradox_intensity: 0.70
      invisible_contribution: ["Passwinkel schließen", "Gegenpressing", "Übergangskontrolle"]
      dominant_metric: "Ballgewinne + Pass%"
      metric_quality: 0.40

    full_back:
      paradox_intensity: 0.50
      invisible_contribution: ["Tiefe halten", "Überzahl herstellen"]
      dominant_metric: "Flanken + Tackles"
      metric_quality: 0.50

  theoretical_anchor:
    holmstrom_milgrom: |
      Je MEHR eine Position präventive (unsichtbare) Aufgaben hat,
      desto STÄRKER verzerren metrische Bewertungssysteme das Training.

      Gradient: ∂(Verzerrung)/∂(Prävention_share) > 0

    kerr_principle: |
      Fussballclubs belohnen systematisch A (spektakuläre Paraden)
      während sie auf B hoffen (souveräne Raumkontrolle).
```

### 2d. Neuer Abschnitt: `action_bias_formalization`

```yaml
action_bias_formalization:
  axiom: "GPM-AB-1: Norm-kongruentes Handeln wird bei Misserfolg weniger bestraft"

  formal_model:
    description: |
      Bar-Eli et al. (2007): Bei Elfmetern ist SPRINGEN die soziale Norm.

      Regret(Tor | Aktion=Norm) < Regret(Tor | Aktion≠Norm)

      Obwohl: P(Gehalten | Mitte) > P(Gehalten | Sprung)

      Dies ist ein ALLGEMEINES Prinzip:
      In jeder Bewertungssituation wird norm-konformes Scheitern
      weniger bestraft als norm-abweichender Erfolg.

  application_to_training:
    description: |
      Blocken ist die "Norm" im modernen Torhütertraining
      (viral, spektakulär, häufig in Highlight-Reels).

      Fangen ist die ABWEICHUNG von dieser Norm
      (still, unsichtbar, selten in Highlights).

      → Trainer wählen Blocken, weil:
        Regret(Gegentor nach Block-Training) < Regret(Gegentor nach Fang-Training)
        OBWOHL: P(Clean Sheet | Fang-Training) > P(Clean Sheet | Block-Training)
```

### 2e. Erweiterte Predictions (PRED-GPM-005 bis PRED-GPM-008)

```yaml
predictions_v2:
  - id: PRED-GPM-005
    statement: "Positions with higher paradox_intensity show LARGER gaps between
      metric-based and contribution-based player valuations"
    testable: true
    falsification: "If goalkeeper transfer fees correlate >0.7 with actual team improvement"
    confidence: HIGH
    literature: "holmstrom1991multitask"

  - id: PRED-GPM-006
    statement: "Goalkeepers who prioritize positioning (invisible) over spectacular saves
      (visible) will have LOWER market value but HIGHER team contribution"
    testable: true
    falsification: "If spectacular-save-focused GKs consistently improve team xGA"
    confidence: MEDIUM
    literature: "bareli2007action, kerr1975folly"

  - id: PRED-GPM-007
    statement: "Introducing V* (counterfactual) metrics will REDUCE action bias in
      goalkeeper training by >20% within 2 seasons"
    testable: true
    falsification: "If V* metrics are available but training allocation unchanged"
    confidence: MEDIUM
    literature: "holmstrom1991multitask"

  - id: PRED-GPM-008
    statement: "The Prevention Paradox: Teams with the BEST goalkeepers will show
      the FEWEST spectacular saves (because positioning prevents shots)"
    testable: true
    falsification: "If top-xGA teams show more saves than average"
    confidence: HIGH
    literature: "rose1985sick"
```

---

## Phase 3: Registries aktualisieren

### 3a. Theory Catalog (2 neue Einträge)

- **MS-IF-007: Multi-Task Principal-Agent** (Holmstrom & Milgrom 1991)
  - ebf_restriction: "Observable effort ≠ valuable effort when tasks differ in measurability"
  - bib_keys: [holmstrom1991multitask]

- **MS-SP-008: Action Bias / Norm Theory** (Bar-Eli et al. 2007, Kahneman & Miller 1986)
  - ebf_restriction: "Norm-congruent failure < Norm-deviant success in perceived regret"
  - bib_keys: [bareli2007action, tversky1973availability]

### 3b. Case Registry (3 neue Cases)

- **CAS-xxx: Elfmeter Action Bias** — Bar-Eli et al. 286 Elfmeter, GK springt obwohl Mitte besser
- **CAS-xxx: Minimax bei Profis** — Palacios-Huerta 1417 Elfmeter, Nash-Gleichgewicht bestätigt
- **CAS-xxx: Brentford Goalkeeper Analytics** — Datengetriebene GK-Scouting mit xGP

### 3c. Parameter Registry (3 neue Parameter)

- **PAR-SPO-001: Action Bias Magnitude** — Effektgrösse des Action Bias bei Elfmetern
- **PAR-SPO-002: Visibility-Contribution Correlation** — Korrelation V(a) und C(a) nach Position
- **PAR-SPO-003: Prevention Paradox Intensity** — Grad des Sichtbarkeits-Paradox (0-1)

---

## Phase 4: Working Paper aktualisieren

Working Paper `outputs/medium/working-papers/WP-001_goalkeeper_performance_framework.tex` ergänzen um:

1. **Section 6: The Visibility Paradox** — Formalisierung mit Holmstrom-Milgrom Verankerung
2. **Section 7: Counterfactual Performance Measurement** — V* = V_observed + V_prevented
3. **Section 8: Position Generalization** — Spektrum von Stürmer bis Torhüter
4. **Section 9: Action Bias in Goalkeeper Training** — Bar-Eli Formalisierung
5. **References** — 7 neue Papers

---

## Phase 5: Git Workflow

1. Branch: `claude/goalkeeper-performance-framework-Kkyyl` (bereits zugewiesen)
2. Commits:
   - `feat(GPM): Add 7 key papers to bibliography (Bar-Eli, Palacios-Huerta, Holmstrom-Milgrom, Kerr, Rose, Chiappori, Apesteguia)`
   - `feat(GPM): Extend model-definition.yaml with visibility, counterfactual, generalization frameworks`
   - `feat(GPM): Add theory catalog entries MS-IF-007, MS-SP-008`
   - `feat(GPM): Add cases and parameters for action bias and visibility paradox`
   - `feat(GPM): Update working paper with new theoretical sections`
3. Push to feature branch

---

## Risiken & Mitigationen

| Risiko | Mitigation |
|--------|------------|
| Pre-commit hook blockiert wegen Compliance | Alle EBF-Felder in BibTeX ausfüllen |
| Registry-ID-Kollision | `registry_manager.py --next` für alle IDs verwenden |
| Model-definition.yaml wird zu gross | Visibility/Counterfactual als separate Sections, nicht als Verschachtelung |
| Working Paper LaTeX-Kompilierung | `/compile` nach Änderungen testen |

---

## Coding Mode: TRADITIONAL

- < 5 Dateien hauptsächlich betroffen (model-definition.yaml, bcm_master.bib, theory-catalog, case-registry, working paper)
- Bekanntes Pattern (Paper-Integration + Modell-Erweiterung)
- < 500 Zeilen pro Datei

## Geschätzte Artefakte

| Datei | Änderung |
|-------|----------|
| `bibliography/bcm_master.bib` | +7 BibTeX-Einträge |
| `data/paper-references/PAP-*.yaml` | +7 neue YAML-Dateien |
| `models/GPM-1-0-GOALKEEPER-PERFORMANCE/model-definition.yaml` | +4 neue Sections (~200 Zeilen) |
| `data/theory-catalog.yaml` | +2 Theorie-Einträge |
| `data/case-registry.yaml` | +3 Cases |
| `data/parameter-registry.yaml` | +3 Parameter |
| `outputs/medium/working-papers/WP-001_*.tex` | +4 Sections (~150 Zeilen) |