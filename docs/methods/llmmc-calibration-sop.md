# LLMMC Calibration Set: Standard Operating Procedure

> **Version:** 1.0
> **Protocol:** HHH-UNMAPPED_CAL-1
> **Date:** 2025-01-13

---

## 1. Zieldefinition

### Was wird kalibriert?

Wir kalibrieren **nicht "die Welt"**, sondern unsere **Parameter-Skala**.

| Komponente | Beschreibung |
|------------|--------------|
| **Output** | Normierte Wirksamkeitsskala θ ∈ [0,1] |
| **Anchor** | Effekte aus realer Evidenz (RCT, Meta-Analyse) |
| **Ziel** | LLM-Schätzungen so transformieren, dass sie im Mittel zu Tier-1/2 Werten passen |

> **Kritisch:** Ein Kalibrations-Set ist nur so gut wie das Mapping auf die 0–1 Skala.

---

## 2. Parameter-Inventar

Bevor Anchors gesucht werden, definiere die Parameter-Taxonomie:

### Dimensionen

| Dimension | Beispielwerte |
|-----------|---------------|
| **Interventions-Typ** | Default, Reminder, Feedback, Incentive, Commitment, Social Norm, Friction Removal, Planning Prompt |
| **Phase** | Awareness, Contemplation, Trigger, Action, Maintenance, Stabilization |
| **Kontext** | DACH Health, Finance, Energy, HR, Digital, Mobility |
| **Outcome-Art** | Uptake, Compliance, Persistenz, Klinisch, Kosten, Verhalten |

### Ergebnis

Eine Taxonomie-Matrix, nach der Anchors systematisch gesucht werden.

---

## 3. Auswahlprinzip für Anchors

### Mindestanforderungen pro Anchor

Jeder Anchor j muss enthalten:

| # | Anforderung | Beispiel |
|---|-------------|----------|
| 1 | Intervention + Outcome klar | "Opt-out Default für 401k Enrollment" |
| 2 | Effektgröße | d = 0.82, OR = 2.5, 41 pp |
| 3 | Unsicherheit | SE = 0.04, CI [0.35, 0.49] |
| 4 | Population/Kontext | "US Employees, large firm" |
| 5 | Qualität (Tier) | Tier 1 (RCT), Tier 2 (Meta) |

### Umfang

| Level | Anzahl Anchors | Eignung |
|-------|----------------|---------|
| **Pilot** | 10–15 | Erste Kalibrierung, schnell |
| **Stabil** | 25–40 | Robuste Produktion |
| **Sehr gut** | 60+ | Breite Domain-Abdeckung |

### Diversität (entscheidend!)

Das Set muss die **gesamte Skala** abdecken:

| Bereich | θ-Werte | Beispiel-Interventionen |
|---------|---------|-------------------------|
| **Low** | 0.10–0.30 | Reine Information, schwache Awareness |
| **Mid** | 0.40–0.60 | Incentives, Reminders, Commitment |
| **High** | 0.70–0.90 | Defaults, starke Friction Removal |

> **Fehler vermeiden:** Nicht nur "Defaults & Social Norms" – das verzerrt die Kalibrierung!

---

## 4. Quellen für Tier-1/2 Evidenz

### Primärquellen

| Quelle | Tier | Charakteristik |
|--------|------|----------------|
| **Meta-Analysen** | 2 | Robust, aggregiert, mit Heterogenität |
| **Systematic Reviews** | 2 | PRISMA-konform, qualitätsgeprüft |
| **RCTs (N > 1000)** | 1 | Harte Evidenz, aber kontextspezifisch |
| **Große Feldexperimente** | 1 | Real-world, aber oft single-context |

### Schlüssel-Repositories

```
Behavioral Economics:
├── JPAL/IPA Evaluation Database
├── Nudge Unit Reports (BIT, ideas42)
├── Cochrane/Campbell Collaboration
└── AEA RCT Registry

Meta-Analysen:
├── Hummel & Maedche (2019) - Nudging
├── Mertens et al. (2022) - Defaults
├── DellaVigna & Linos (2022) - Nudge Units
├── Cadario & Chandon (2020) - Food
└── Jachimowicz et al. (2019) - Commitment
```

### Praxisregel

> Lieber **wenige sehr saubere Anchors** als viele wackelige.

---

## 5. Skalen-Mapping (kritisch!)

### Das Problem

Studien berichten verschiedene Effektmaße:
- Cohen's d
- Odds Ratio (OR)
- Percentage Points (pp)
- Percent Change (%)
- Risk Ratio (RR)

### Die Lösung: Einheitliches Mapping

#### Option A: Piecewise Linear (empfohlen für Start)

```
d ≈ 0.0  →  θ = 0.00
d ≈ 0.2  →  θ = 0.30
d ≈ 0.5  →  θ = 0.60
d ≈ 0.8  →  θ = 0.90
d ≥ 1.0  →  θ = 1.00

Linear interpolieren zwischen Stützpunkten.
```

#### Option B: Logistische Transformation (glatt)

```
θ = 1 / (1 + exp(-k × d))

k so wählen, dass d = 0.8 bei θ ≈ 0.90 liegt
→ k ≈ 2.75
```

#### Mapping-Tabelle für verschiedene Effektmaße

| Effektmaß | Formel | Beispiel |
|-----------|--------|----------|
| **Cohen's d** | θ = min(1, d/1.0) | d=0.5 → θ=0.50 |
| **Percentage Points** | θ = min(1, pp/50) | 40pp → θ=0.80 |
| **Percent Change** | θ = min(1, %/30) | 15% → θ=0.50 |
| **Odds Ratio** | θ = min(1, \|log(OR)\|/1.0) | OR=2.0 → θ=0.69 |
| **Risk Ratio** | θ = min(1, \|log(RR)\|/0.8) | RR=1.5 → θ=0.51 |

### Unsicherheits-Mapping

Für SE/CI auf θ-Skala:

**Option 1: Delta-Methode**
```
se_theta = |dθ/dEffect| × se_effect
```

**Option 2: Simulation (robuster)**
```python
samples = np.random.normal(effect_mean, effect_se, 10000)
theta_samples = [map_to_theta(s) for s in samples]
se_theta = np.std(theta_samples)
```

> **Dokumentationspflicht:** Das Mapping MUSS als Teil der Methode dokumentiert werden!

---

## 6. Datenstruktur

### Anchor-Schema

Jeder Anchor j enthält:

```yaml
# A. Identität
anchor_id: "default_401k_madrian"
intervention_type: "Default"
domain: "Finance"
phase: "Trigger"
outcome_type: "Uptake"

# B. Evidenz (True Prior)
effect_metric_type: "percentage_points"
effect_metric_value: 41
effect_se: 3.2
effect_ci_95: [34.7, 47.3]
sample_size: 6000
tier: 1
source: "Madrian & Shea (2001), QJE"
source_url: "https://doi.org/..."

# C. Gemappt auf θ-Skala
theta_true: 0.82
se_true: 0.064
mapping_method: "pp/50"

# D. LLMMC Output
theta_llm: 0.91
eu_llm: 0.05
llm_model: "gemini-1.5-pro"
llm_date: "2025-01-13"
prompt_version: "v2"
```

---

## 7. Schritt-für-Schritt Vorgehen

### Schritt 1: Anchor-Shortlist (1–2h)

1. Liste 20–30 Kandidatenstudien (Titel + Links)
2. Priorisiere nach:
   - Tier (1 > 2)
   - Relevanz für eure Domain
   - Abdeckung der θ-Skala (low/mid/high)
3. Wähle 10–15 für Pilot

**Output:** `anchor_candidates.csv`

### Schritt 2: Extraction (2–6h)

Für jeden Anchor:

```
☐ Effektgröße extrahieren
☐ Unsicherheit extrahieren (CI/SE)
☐ Sample Size notieren
☐ Kontext dokumentieren
☐ Tier bestimmen (1 oder 2)
☐ Qualitäts-Check (Randomisierung? Attrition? Intent-to-treat?)
```

**Output:** `anchors_raw.csv`

### Schritt 3: Mapping (1–2h)

```python
for anchor in anchors_raw:
    # Effekt → θ
    anchor['theta_true'] = map_effect_to_theta(
        anchor['effect_metric_type'],
        anchor['effect_metric_value']
    )

    # SE → se_theta (via Simulation)
    anchor['se_true'] = map_uncertainty(
        anchor['effect_metric_value'],
        anchor['effect_se'],
        anchor['effect_metric_type']
    )
```

**Output:** `anchors_mapped.csv`

### Schritt 4: LLMMC-Schätzungen (1–2h)

Für jeden Anchor exakt denselben LLMMC-Prompt verwenden:

```python
for anchor in anchors_mapped:
    llmmc_result = run_llmmc(
        intervention_type=anchor['intervention_type'],
        domain=anchor['domain'],
        phase=anchor['phase'],
        outcome=anchor['outcome_type']
    )
    anchor['theta_llm'] = llmmc_result['mean']
    anchor['eu_llm'] = llmmc_result['se']
```

**Output:** `anchors_complete.csv`

### Schritt 5: Fit & Validierung (30min)

```python
from llmmc_calibration import LLMMCCalibrator

calibrator = LLMMCCalibrator()
for anchor in anchors_complete:
    calibrator.add_anchor(...)

calibrator.fit()
loo = calibrator.loo_cross_validation()

print(f"MAE: {loo.mae:.3f}")
print(f"Coverage: {loo.coverage_95:.1%}")
print(f"Spearman ρ: {loo.spearman_rho:.2f}")
```

**Akzeptanzkriterien:**
- MAE < 0.12
- RMSE < 0.15
- Coverage ∈ [0.85, 0.98]
- Spearman ρ > 0.70

### Schritt 6: Freeze & Dokumentation

```python
calibration_v1 = {
    "version": "1.0",
    "date": "2025-01-13",
    "n_anchors": 16,
    "params": {
        "a": calibrator.a,
        "b": calibrator.b,
        "sigma_model": calibrator.sigma_model,
        "tau": calibrator.tau
    },
    "validation": {
        "mae": loo.mae,
        "rmse": loo.rmse,
        "coverage_95": loo.coverage_95,
        "spearman_rho": loo.spearman_rho
    },
    "mapping": "piecewise_linear_v1"
}

# Speichern
with open('data/calibration_v1.json', 'w') as f:
    json.dump(calibration_v1, f, indent=2)
```

---

## 8. Spezialfall: γ-Kalibrierung

Für Interaktionseffekte γ:

### Anforderungen

- Studien mit 2×2 Design (A, B, A+B, Control)
- Multi-arm RCTs
- Factorial Designs

### Vorgehen

1. Sammle 6–10 Interaktions-Anchors
2. Kalibriere primär Δ_int (stabiler):
   ```
   Δ_int = d_AB - d_A - d_B
   ```
3. γ nur sekundär normalisieren:
   ```
   γ = Δ_int / sqrt(d_A × d_B)
   ```

### Typische Quellen

- Benartzi & Thaler (2013): Default + Escalation
- Schultz et al. (2007): Descriptive + Injunctive Norms
- Multi-component interventions in health behavior

---

## 9. Pilot-Kalibrations-Set: Empfohlene Struktur

| Bereich | Anzahl | Beispiel-Typen |
|---------|--------|----------------|
| **High (0.7–0.9)** | 4 | Defaults, starke Friction Removal |
| **Mid (0.4–0.6)** | 4 | Incentives, Commitment, Reminders |
| **Low (0.1–0.3)** | 4 | Information-only, schwache Awareness |
| **Domain-Match** | 4 | DACH-spezifisch (eure Hauptdomain) |
| **Total** | 16 | |

---

## 10. Ergebnis: Was ihr danach habt

Nach abgeschlossener Kalibrierung könnt ihr sagen:

> "Tier-3 LLMMC estimates are calibrated on Tier-1/2 anchors (n=16).
> Typical absolute error: MAE = 0.07.
> 95% confidence bands achieve 93% coverage under LOO.
> Uncertainty is propagated via Monte Carlo under explicit assumptions."

Das ist **wissenschaftlich sauber** und **praktisch belastbar**.

---

## Checkliste: Kalibrations-Set komplett

```
☐ Zieldefinition dokumentiert
☐ Parameter-Taxonomie erstellt
☐ Anchor-Shortlist (20-30 Kandidaten)
☐ 10-16 Anchors extrahiert
  ☐ Low-Bereich abgedeckt (3-4)
  ☐ Mid-Bereich abgedeckt (4-5)
  ☐ High-Bereich abgedeckt (3-4)
☐ Mapping-Methode dokumentiert
☐ Unsicherheits-Mapping dokumentiert
☐ LLMMC für alle Anchors durchgeführt
☐ Kalibrierung gefittet (a, b, σ_model, τ)
☐ LOO-Validierung bestanden
  ☐ MAE < 0.12
  ☐ Coverage ∈ [0.85, 0.98]
  ☐ Spearman ρ > 0.70
☐ Version eingefroren und gespeichert
☐ Dokumentation vollständig
```

---

*Protocol: HHH-UNMAPPED_CAL-1 | Version: 1.0 | Date: 2025-01-13*
