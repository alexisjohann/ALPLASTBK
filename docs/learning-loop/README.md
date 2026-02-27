# Learning Loop: Prediction → Execution → Measurement → Learning

**Version:** 1.1 (Phase 4 + v54 EIP Integration)
**Date:** 2026-01-20
**Status:** ACTIVE (EIP + Intervention Design Integrated) ✅

---

## Overview

The Learning Loop closes the gap between strategic model predictions and observed outcomes, enabling continuous parameter refinement and archetype discovery.

```
PREDICTION PHASE (T=0)
├── Run /apply-models CompanyX
├── Generate E(RPM), E(OSM), E(CAM), E(MCSM)
└── Store predictions in intervention-registry.yaml

         ↓ (T=1 to T=11, quarterly)

EXECUTION PHASE
├── Quarterly tracking: actual_revenue, actual_headcount, actual_capex
├── Monitor Ψ (context) for changes
└── Update intervention-registry.yaml with actuals

         ↓ (Every 4 quarters)

MEASUREMENT PHASE
├── Run quarterly_review.py
├── Calculate ΔP = Actual - Predicted
├── Decompose ΔP into:
│   ├── Parameter error (θ wrong)
│   ├── Context shock (Ψ changed)
│   └── Model error (functional form)
└── Archive analysis for archetype learning

         ↓ (Immediate)

PARAMETER UPDATE PHASE
├── Run parameter_update_pipeline.py
├── Apply Bayesian shrinkage: E(θ)_new = E(θ)_old × (1 - n/(n+k))
├── Update model_registry.yaml with new E(θ)
└── Confidence intervals shrink as n increases

         ↓ (After 3+ projects)

ARCHETYPE DISCOVERY PHASE
├── Run archetype_discovery.py
├── Cluster projects with similar (Ψ, WHAT, HOW, γ)
├── Formalize clusters as archetypes in FFF registry
└── Use archetypes to seed parameters for new customers
```

---

## Phase 4 Implementation: 4 Core Scripts

### 1. **quarterly_review.py** - Deviation Analysis

**Purpose:** Close prediction-to-execution gap

**Input:**
- Prediction from previous quarter (JSON)
- Actuals from current quarter (YAML)
- Context snapshot (Ψ dimensions)

**Output:**
- Deviation analysis: ΔP = Actual - Predicted
- Attribution decomposition (parameter vs context vs model error)
- Quarterly report (JSON)

**Example:**
```bash
# Called by: /intervention-manage close ALPLA_PROJECT --actuals Q1-2025

Review.load_prediction()              # E(RPM) = €5.35B
Review.load_actuals()                 # Actual = €5.28B
Review.analyze_deviations()           # ΔP = -€70M (-1.3%)

# Attribution:
# - APAC CAGR came in at 5.8% (vs 6.5% predicted)
# - Impact on revenue: €267M (from sensitivity analysis)
# - Root cause: Ψ_economic = 0.75 (was 0.80)
# - Conclusion: CONTEXT_SHOCK (not parameter error)
```

**Key Equations:**
```
ΔP = Actual - Predicted                          # Deviation
MAPE = |ΔP| / Predicted                          # Relative error
Attribution = f(ΔCAGR, Δheadcount_cost, ΔΨ)     # Decomposition
```

---

### 2. **parameter_update_pipeline.py** - Bayesian E(θ) Learning

**Purpose:** Update parameter uncertainty as we observe more data

**Input:**
- Historical observations for each parameter
- Prior mean and uncertainty from model_registry.yaml
- Prior strength (default: 4 quarters)

**Output:**
- Updated E(θ) for all parameters
- Shrinkage factors (how much confidence improved)
- Learning report (JSON)
- Updated model_registry.yaml

**Example:**
```bash
# Called by: quarterly_review.py after deviation analysis

Pipeline.load_parameter_metadata()     # E(APAC_CAGR) = ±1.5pp
Pipeline.load_historical_observations()  # [5.8%, 6.2%, 6.1%] (3 quarters)
Pipeline.bayesian_shrinkage()          # Apply E(θ)_new formula

# Result:
# - Old: APAC_CAGR = 8.5% ± 1.5pp
# - New: APAC_CAGR = 6.1% ± 1.0pp    (mean shifted, uncertainty shrunk)
# - Shrinkage factor: 30%              (3 quarters / (3 + 4 prior))
# - Confidence improvement: 33%        (from 86.5% to 90%)
```

**Key Formula (Bayesian Shrinkage):**
```
λ = n / (n + k)                            # Shrinkage weight
μ_new = λ × μ_observed + (1-λ) × μ_prior  # Updated mean
E(θ)_new = E(θ)_prior × (1 - 0.2 × λ)     # Uncertainty shrinkage
```

---

### 3. **archetype_discovery.py** - Pattern Learning Across Projects

**Purpose:** Discover and formalize recurring patterns

**Input:**
- All completed projects (intervention-registry.yaml)
- Context vectors: (Ψ, WHAT, HOW, γ) for each
- Performance metrics (CAGR, elasticity, ROI)

**Output:**
- Discovered archetypes (clusters of similar projects)
- Archetype recommendations for new customers
- FFF archetype registry (YAML)

**Example:**
```bash
# After 3+ completed projects

Discovery.load_completed_projects()    # [ALPLA, TechCo1, TechCo2, ...]
Discovery.extract_context_vector()     # (Ψ, WHAT, HOW) for each
Discovery.cluster_projects()           # Similarity threshold = 0.75

# Discovered Archetype: FFF-TECH-APAC
# Companies: TechCo1, TechCo2, TechCo3
# Characteristics:
#   - Ψ_tech = 0.9, Ψ_econ = 0.8
#   - WHAT: ω_D=0.4, ω_X=0.3 (Innovation + Purpose)
#   - γ_avg = 0.72 (high synergy)
# Observed Outcomes:
#   - CAGR: 7.2% (vs 6.0% baseline)
#   - Headcount elasticity: 0.75 (vs 0.65 baseline)
#   - Capex intensity: 4.2% (vs 3.5%)
# Recommendations:
#   ✓ Allocate 5%+ capex to digital transformation
#   ✓ Invest in R&D + talent development
#   ✓ Coordinate revenue-headcount-capex (high γ)

# → Use FFF-TECH-APAC to seed next tech company in APAC
# → Start with E(θ) = ±0.8pp (vs standard ±1.5pp)
# → Faster convergence, more accurate forecasts
```

**Key Clustering Metric:**
```
Similarity(Project1, Project2) = 1 / (1 + Euclidean_Distance)
# Clusters if similarity ≥ 0.75
# Archetype confirmed with n ≥ 3 projects
# Confidence = 0.6 + 0.1 × n_projects
```

---

## Integration with Strategic Models

### Workflow: Full Quarterly Cycle

```
START OF QUARTER (Q1 2025):
  1. /apply-models ALPLA
     → Generates predictions: E(RPM), E(OSM), E(CAM)
     → Stores in: intervention-registry.yaml[ALPLA_2025].predictions

  2. Company executes quarterly: revenue €5.28B, headcount 27.5K, capex €14.2M

END OF QUARTER:
  3. /intervention-manage close ALPLA_2025 --actual-q1
     → Calls quarterly_review.py
     → Analyzes ΔP = Actual - Predicted
     → Decompose: CONTEXT_SHOCK (Ψ changed), PARAMETER_ERROR (θ drift)

  4. quarterly_review.py automatically calls parameter_update_pipeline.py
     → Loads historical observations (4 quarters accumulated)
     → Bayesian shrinkage: E(APAC_CAGR) ±1.5pp → ±1.2pp
     → Updates model_registry.yaml

  5. After 3+ completed projects:
     → archetype_discovery.py runs automatically
     → Clusters similar projects
     → Creates FFF-TECH-APAC archetype
     → Next tech company in APAC gets better priors

NEXT QUARTER (Q2 2025):
  6. /apply-models NewTechCoAPAC --with-archetype FFF-TECH-APAC
     → Loads archetype seeding for better E(θ)
     → Faster convergence, more accurate confidence bands
```

---

## Data Files

### Input Files

**intervention-registry.yaml**
```yaml
projects:
  ALPLA_2024_2035:
    status: "EXECUTING"
    company_name: "ALPLA"
    predictions:
      rpm:
        annual_revenue_eur_m: 5.35
        cagr_actual: 8.5
      osm:
        headcount: 25000
        avg_cost: 95000
      cam:
        annual_capex_eur_m: 50
    execution_results:
      q1_2025:
        actual_revenue_eur_m: 5.28
        actual_headcount: 27500
        actual_capex_eur_m: 14.2
```

**model_registry.yaml** (enhanced)
```yaml
models:
  rpm_1_0:
    parameter_uncertainty:
      regional_cagr:
        value_range: "2.5% - 8.5%"
        epistemic_status_e_theta: "±1.5pp"
        update_history:
          - date: "2026-01-16"
            old_e_theta: "±1.5pp"
            new_e_theta: "±1.2pp"
            reason: "convergence"
```

### Output Files

**quarterly_review_Q1-2025.json**
```json
{
  "quarter": "Q1-2025",
  "company": "ALPLA",
  "analysis": {
    "rpm": {
      "predicted": 5.35,
      "actual": 5.28,
      "delta_p": -0.07,
      "attribution": {
        "primary_cause": "CONTEXT_SHOCK",
        "cagr_drift_pp": -0.7,
        "cagr_attribution_impact": "-€237M"
      }
    }
  },
  "parameter_updates": {
    "rpm": {
      "action": "UPDATE_PARAMETERS",
      "recommended_e_theta_shrinkage": "±1.2pp"
    }
  }
}
```

**archetype_registry.yaml**
```yaml
archetypes:
  FFF-TECH-APAC:
    name: "Tech Companies in APAC - Archetype"
    companies: ["TechCo1", "TechCo2", "TechCo3"]
    characteristics:
      context_profile:
        psi_economic: "0.80"
        psi_technological: "0.90"
    observed_outcomes:
      cagr_observed: "7.2%"
      headcount_elasticity: "0.75"
      revenue_forecast_accuracy: "98.7%"
    confidence: 0.82
    created_date: "2026-01-16"
```

---

## Integration Points

### With 10C Framework

- **WHERE (BBB):** Parameter updates directly modify BBB registry
- **WHEN (V):** Context tracking (Ψ) enables attribution analysis
- **HOW (B):** Complementarity (γ) monitored through outcome correlations
- **HIERARCHY (HI):** Quarterly reviews stratified by decision level

### With Skills

- **`/apply-models`:** Loads current E(θ) from registry
- **`/board-presentation`:** Includes "Prediction Track Record" slide
- **`/intervention-manage`:** Close command triggers learning loop

---

## Success Metrics

### Quarterly Review
- ✅ Deviation analysis: |ΔP| < 10% (acceptable tolerance)
- ✅ Attribution clarity: >80% of ΔP explained
- ✅ Trend detection: Regime changes caught within 2 quarters

### Parameter Updates
- ✅ E(θ) shrinkage: 5-10% per quarter observed
- ✅ Convergence: E(θ) → 50% of initial uncertainty by year 2
- ✅ Stability: Parameter estimates vary <3% between quarters (post-Q4)

### Archetype Discovery
- ✅ Cluster purity: Similarity ≥ 0.75 within clusters
- ✅ Archetype confidence: ≥80% after 3 projects
- ✅ Seeding impact: New customers converge 30% faster with archetype

---

## Next Steps

1. **Integrate with `/interval-manage` skill**
   - `/intervention-manage close PROJECT` triggers quarterly_review.py

2. **Add archetype seeding to `/new-customer`**
   - `/new-customer Company --archetype FFF-TECH-APAC` uses better priors

3. **Implement parameter push-back**
   - Updated E(θ) automatically affects /apply-models output

4. **Create quarterly reporting dashboard**
   - Aggregates prediction accuracy across all customers

---

## References

- **10C Framework:** `/docs/frameworks/core-framework-definition.yaml`
- **Strategic Models Mapping:** `/docs/frameworks/strategic-models-9c-mapping.md`
- **Model Registry:** `/data/models/registry/model_registry.yaml`
- **Scripts:** `/scripts/models/quarterly_review.py`, `parameter_update_pipeline.py`, `archetype_discovery.py`
