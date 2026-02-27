# /intervention - EBF Intervention Registry

Abfrage und Analyse von Interventions-Projekten mit Predictions, Ergebnissen und Learnings.

## Projekt-Abfragen

```bash
/intervention PRJ-001                 # Spezifisches Projekt
/intervention --domain health         # Nach Domain filtern
/intervention --status completed      # Nach Status filtern
/intervention --list                  # Alle Projekte
```

## Analysen

```bash
/intervention --deviation             # Abweichungsanalyse (Prediction vs. Actual)
/intervention --accuracy              # Prediction-Genauigkeit
/intervention --learnings             # Alle Learnings extrahieren
/intervention --parameters            # Parameter-Updates anzeigen
/intervention --stats                 # Statistiken
```

## Projekt-Struktur

Jedes Projekt enthält:

### 1. Meta & Context
- Client, Domain, Zeitraum, Status
- Zielverhalten, Population, Sample Size
- Baseline, Journey Phase, Segments

### 2. Intervention Mix
```yaml
- id: "I1"
  type: nudge
  subtype: default
  expected_contribution:
    E_i: 0.35           # Erwarteter Einzelbeitrag
    confidence: 0.85    # Konfidenz
    source: literature  # Quelle (literature/pilot/expert)
```

### 3. Komplementaritäts-Matrix
```yaml
- pair: ["I1", "I2"]
  gamma_ij: 0.3         # Synergy (+) oder Interference (-)
  interaction: synergy
  mechanism: "Warum verstärken sich I1 und I2?"
```

### 4. Predictions
```yaml
portfolio_effect:
  E_P: 0.52             # E(P) = Σ E_i + Σ γ_ij · √(E_i · E_j)
  CI_lower: 0.42
  CI_upper: 0.62
kpis:
  - name: "Teilnahmequote"
    baseline: 0.34
    predicted_value: 0.86
```

### 5. Results
```yaml
kpis:
  - name: "Teilnahmequote"
    actual_value: 0.91
    actual_delta: 0.57
```

### 6. Deviation Analysis
```yaml
overall:
  predicted_E_P: 0.52
  actual_E_P: 0.57
  delta_pct: 9.6
  direction: underestimate

by_intervention:
  - id: "I1"
    predicted: 0.35
    actual: 0.42
    likely_causes: [...]

root_causes:
  - cause: "Default-Effekt in DACH stärker als US-Literatur"
    confidence: medium
```

### 7. Learnings
```yaml
what_worked:
  - intervention: "I1"
    insight: "Opt-Out Default übertrifft Erwartungen in DACH"
    generalizable: true

parameter_updates:
  - parameter: "E_i für Default (DACH)"
    old_value: 0.35
    new_value: 0.42

recommendations:
  - category: design
    recommendation: "Rentenrechner vereinfachen"
    priority: high
```

## Neues Projekt anlegen

In `data/intervention-registry.yaml` eintragen:

```yaml
PRJ-XXX:
  meta:
    name: "Projektname"
    client: "Anonymisiert"
    domain: finance|health|energy|...
    start_date: "YYYY-MM-DD"
    end_date: "YYYY-MM-DD"
    status: planning|active|completed|analyzed

  context:
    target_behavior: "Was soll geändert werden?"
    # ...

  intervention_mix:
    - id: "I1"
      # ...

  predictions:
    # ...

  # Nach Abschluss:
  results:
    # ...
  deviation_analysis:
    # ...
  learnings:
    # ...
```

## Integration mit EBF

1. **Vor dem Projekt:** Case Registry (`/case`) für ähnliche Fälle konsultieren
2. **Design:** Intervention Mix mit EEE Workflow (`/design-model`)
3. **Prediction:** Portfolio-Formel aus Kapitel 20 anwenden
4. **Nach dem Projekt:** Ergebnisse und Learnings dokumentieren
5. **Parameter-Update:** Angepasste Werte in BBB (Parameter Repository) einpflegen

## Referenzen

- **Registry:** `data/intervention-registry.yaml`
- **Script:** `scripts/query_interventions.py`
- **Kapitel 20:** Intervention Portfolios
- **Appendix BBB:** Parameter Repository
