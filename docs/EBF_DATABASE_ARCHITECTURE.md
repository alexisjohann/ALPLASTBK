# EBF Database Architecture: The Integrated Meta-System
## How Model, Context, and Intervention Databases Connect

**Created**: January 14, 2026
**Status**: Architecture Definition (Implementation Roadmap)
**Purpose**: Document the interconnected database system that enables systematic learning and improvement

---

## Executive Summary

The Evidence-Based Framework has **THREE INTERCONNECTED DATABASES**:

```
┌─────────────────────────────────────────────────────────────────────┐
│ MODEL DATABASE (models.registry.yaml)                               │
│ ├─ Papal Succession Framework (PSF 2.0)                             │
│ ├─ Trump Constitutional Risk                                        │
│ ├─ Xi Removal Risk                                                  │
│ └─ [Future: Corporate CEO, CCP Congress, Military]                  │
├─────────────────────────────────────────────────────────────────────┤
│ CONTEXT DATABASE (context-registry.yaml - NEW)                      │
│ ├─ Ψ = Environmental/Contextual Factors                             │
│ ├─ Economic conditions (GDP, unemployment, etc.)                    │
│ ├─ Political climate (democracy, polarization, etc.)               │
│ ├─ Institutional factors (military strength, court independence)    │
│ └─ Real-time monitoring feeds                                       │
├─────────────────────────────────────────────────────────────────────┤
│ INTERVENTION DATABASE (intervention-registry.yaml - EXISTING)       │
│ ├─ Behavioral interventions implemented                             │
│ ├─ Predicted outcomes vs. actual results                            │
│ ├─ Learning from successes and failures                             │
│ └─ Parameter updates for next iteration                             │
├─────────────────────────────────────────────────────────────────────┤
│ CASE REGISTRY (case-registry.yaml - EXISTING)                       │
│ ├─ Specific instances linking all three DBs                         │
│ ├─ "2022 Papal Conclave": Connects PSF 2.0 + Context + Outcome     │
│ └─ Historical cases for model training                              │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 1. MODEL DATABASE
**Location**: `models/models.registry.yaml`
**Owner**: Model Registry System
**Purpose**: Single source of truth for all decision models

### Contents
- **Model Metadata**: ID, version, status, category
- **Dimensions**: Λ, Ι, Π, Ν, Α (for papal) or system-specific
- **Parameters**: β coefficients, γ complementarity terms
- **Validation**: Historical accuracy, test coverage
- **Improvement Roadmap**: Phases 1-3 tasks

### Example: PSF 2.0
```yaml
model_id: PSF-2.0
version: 1.1
status: STABLE
dimensions:
  - symbol: Λ
    name: Network Centrality
    weight: 0.40
    beta_coefficient: 2.5
validation:
  accuracy: 1.00
  data_points: 12
phase_1_completed:
  - Task 1.1: Pre-1958 Historical Extension
phase_2_planned:
  - Task 2.1: Complementarity Parameters (target: RMSE 1.5)
```

### Query Examples
```python
# Get all stable models
stable_models = registry.list_models_by_status(ModelStatus.STABLE)

# Get models by category
succession_models = registry.list_models_by_category(ModelCategory.SUCCESSION)

# Get best-validated models
top_models = registry.get_best_validated_models(n=5)
```

---

## 2. CONTEXT DATABASE (NEW)
**Location**: `data/context-registry.yaml`
**Owner**: Context Management System
**Purpose**: Track environmental/contextual factors (Ψ dimensions)

### Why Separate?
- **Models** describe HOW people decide (fixed structure)
- **Context** describes WHAT they decide in (changes daily)
- **Intervention** describes WHAT WE DID (actions)

Separating enables:
- Real-time Ψ updates without touching models
- Historical context reconstruction for backtesting
- Scenario planning ("What if GDP collapsed?")

### Contents

**Global Context Dimensions** (apply to all models):
```yaml
economic:
  gdp_growth: 2.1%  # Latest quarterly
  unemployment: 3.8%
  inflation: 2.5%
  market_volatility: 15%

political:
  regime_type: democracy
  polarization_index: 7.2/10  # 0=united, 10=split
  institutional_trust: 45%
  election_cycle: mid-term

institutional:
  judicial_independence: strong
  military_autonomy: moderate
  media_freedom: free
  civil_service_quality: 7.5/10
```

**System-Specific Context** (e.g., Papal):
```yaml
vatican:
  latest_pope_age: 92  # For conclave timing
  factional_divisions: high  # Integralisten vs. Progressive
  church_crisis_topics:
    - clergy_abuse_scandals
    - declining_attendance
  international_relations: cold  # With governments
```

**System-Specific Context** (e.g., Chinese Politics):
```yaml
china:
  party_factionalism: moderate  # ~40% Xi, ~30% anti-Xi, ~30% neutral
  economic_growth: 5.2%  # Triggered? (threshold: <3%)
  taiwan_tension: elevated  # Risk of military action?
  senior_patriarch_alive: false  # Can they intervene?
  pbsc_composition:
    xi_allies: 3/7
    neutral: 2/7
    opponents: 2/7
```

### Structure

```yaml
context_registry:
  metadata:
    version: 1.0
    last_updated: 2026-01-14
    update_frequency: daily

  global_dimensions:
    economic: {...}
    political: {...}
    institutional: {...}
    technological: {...}

  model_specific_contexts:
    PSF-2.0:
      vatican_conditions: {...}
      conclave_timing: {...}

    TRUMP-COMPLIANCE:
      us_conditions: {...}
      military_alignment: {...}

    XI-REMOVAL:
      china_conditions: {...}
      pbsc_alignment: {...}

  historical_snapshots:
    "2026-01-14": {...}
    "2025-12-14": {...}
    "1922-02-01": {...}  # For backtesting PSF 2.0
```

---

## 3. INTERVENTION DATABASE (EXISTING)
**Location**: `data/intervention-registry.yaml`
**Owner**: Project Tracking System
**Purpose**: Track behavioral interventions and their outcomes

### Contents
- **Project**: What intervention was implemented?
- **Predictions**: What did the model predict would happen?
- **Results**: What actually happened?
- **Learning**: How do we update the model?
- **Parameters**: Which parameter values need refinement?

### Example: 1922 Papal Conclave (Hypothetical Intervention)

```yaml
intervention_id: INTERVENTION-UNMAPPED_PAP-1922-01
model_used: PSF-1.0  # (Pre v2.0, no γ terms)
project_name: "Support Ratti Compromise Candidacy"
timing: "February 1922"

predictions:
  predicted_winner: Ratti
  predicted_probability: 0.76
  predicted_ballots: 8
  predicted_duration_days: 1-2

implementation:
  intervention_type: "Coalition Formation Support"
  target_audience: "Progressive & Conservative cardinal factions"
  mechanism: "Facilitate back-channel communication showing Ratti acceptability"
  timing: "Ballot 10-11 (when stalemate appeared)"

results:
  actual_winner: Ratti ✓
  actual_ballots: 14
  actual_duration_days: 2
  prediction_accuracy: "CORRECT WINNER, WRONG DURATION"

learning:
  prediction_error: +6 ballots (75% overestimate)
  root_cause: "Model didn't account for factional stalemate dynamics"
  dimension_analysis:
    λ_actual: 0.72 (lower than other popes)
    π_actual: 0.48 (much weaker than threshold)
    ι_critical: 0.88 (higher than normal - bridge-builder effect)

  hypothesis: "With weak Π, candidate needs higher Ι to achieve consensus"
            "This suggests complementarity parameter γ_ΙΠ is critical"

parameter_updates:
  - parameter: "γ_ΙΠ"
    proposed_value: 0.5
    rationale: "Integration + weak Predecessor interaction explains slow coalition"
  - parameter: "γ_ΛΠ"
    proposed_value: 0.8
    rationale: "Synergy effect when both network and predecessor are strong"

next_model_version: "PSF v2.0 (Phase 2, Task 2.1)"
implementation_date: "2026 Q3-Q4"
```

---

## 4. CASE REGISTRY (EXISTING)
**Location**: `data/case-registry.yaml`
**Owner**: Case Management System
**Purpose**: Connect specific historical cases to models + context + interventions

### How It Bridges All Three Databases

```yaml
case_id: CASE-UNMAPPED_PAP-1922-01
title: "Papal Conclave 1922: Ratti's Compromise Victory"

model_reference:
  model_id: PSF-2.0
  version: 1.0  # (or 2.0 after Phase 2)
  usage: "Apply model to predict conclave outcome"
  prediction: "Ratti wins with 0.76 probability in ~8 ballots"

context_reference:
  context_date: 1922-02-01
  vatican_context:
    factional_division: high  # Integralisten vs. Progressive
    predecessor_recent_death: 8 days ago
    cardinals_voting: 53
    pope_needed: 2/3 = 36 votes

intervention_reference:
  intervention_id: INTERVENTION-UNMAPPED_PAP-1922-01
  intervention_type: "Coalition Support"
  outcome: "Ratti elected after 14 ballots (not 8)"

historical_outcome:
  pope_elected: "Achille Ratti (Pius XI)"
  ballots: 14
  duration: 2 days
  votes_for_ratti: 42

analysis:
  model_accuracy: "Winner CORRECT, Duration WRONG"
  critical_finding: "Strong integration capacity enabled compromise in factional stalemate"
  learning_point: "Need complementarity parameters (γ) for future versions"

model_update:
  triggered_by: "1922 case discrepancy"
  improvement_task: "PHASE_2_TASK_2_1"
  expected_completion: "Q3-Q4 2026"
```

---

## How They Connect: Data Flow

### Flow 1: Normal Operation (Prediction)

```
┌──────────────────┐
│  MODEL DATABASE  │  Load PSF 2.0 (Λ, Ι, Π, Ν, Α params)
└────────┬─────────┘
         │
         ↓
┌──────────────────┐
│ CONTEXT DATABASE │  Get current Vatican context (Ψ)
└────────┬─────────┘      - Factional divisions
         │                - Candidate network positions
         │                - Predecessor signals
         ↓
┌──────────────────┐
│   CASE INSTANCE  │  Input: Dimensions (Λ, Ι, Π, Ν, Α) + Context (Ψ)
└────────┬─────────┘
         │
         ↓
   [ PREDICT OUTPUT ]
       Winner probability, Duration, Confidence
```

### Flow 2: Learning Loop (Feedback)

```
┌──────────────────┐
│  PREDICTION      │  Model said: "Ratti wins in 8 ballots"
└────────┬─────────┘
         │
         ↓
┌──────────────────┐
│   ACTUAL OUTCOME │  Actually: "Ratti wins in 14 ballots"
└────────┬─────────┘
         │
         ↓
┌──────────────────┐
│  CASE REGISTRY   │  Record discrepancy
└────────┬─────────┘
         │
         ↓
┌──────────────────┐
│  LEARNING ENGINE │  Analyze: Why was duration wrong?
└────────┬─────────┘      → Weak Π + high Ι combination
         │                → Factional stalemate dynamics
         │                → Need complementarity (γ) terms
         ↓
┌──────────────────┐
│ MODEL ROADMAP    │  Trigger Task 2.1: "Add complementarity parameters"
│ UPDATE           │
└────────┬─────────┘
         │
         ↓
┌──────────────────┐
│ NEXT VERSION     │  PSF v2.0: Add 10 γ parameters
│ DEVELOPMENT      │  Target: RMSE 2.73 → 1.5
└──────────────────┘
```

### Flow 3: Intervention Planning

```
┌──────────────────┐
│  QUESTION        │  "How to help Ratti win the conclave?"
└────────┬─────────┘
         │
         ↓
┌──────────────────┐
│ MODEL DATABASE   │  Query: What increases P(Ratti)?
└────────┬─────────┘      → Higher Λ (network position)
         │                → Higher Ι (bridge-building)
         │                → Higher Π (predecessor support)
         ↓
┌──────────────────┐
│  INTERVENTION    │  Design: Which lever is actionable?
│  DESIGN          │         → Support factional bridge-building (Ι)
└────────┬─────────┘            (Can't change network history)
         │
         ↓
┌──────────────────┐
│  INTERVENTION    │  Execute: Facilitate communication between
│  IMPLEMENTATION  │          conservative & progressive cardinals
└────────┬─────────┘
         │
         ↓
┌──────────────────┐
│ INTERVENTION DB  │  Record: Predicted 0.76 P(Ratti)
│ + CASE REGISTRY  │         Actual: won (P=1.0)
└──────────────────┘
```

---

## 5. PARAMETER REPOSITORY (Appendix UNMAPPED_EST)
**Location**: `appendices/BBB_PARAMETER-REPOSITORY.tex`
**Owner**: Data Steward
**Purpose**: Centralized repository of Tier 1-3 parameter values

### How It Connects
```
┌─────────────────────────────┐
│ PARAMETER REPOSITORY (BBB)  │
├─────────────────────────────┤
│ Tier 1: Hard empirical data │  Model DB
│         (from published     │  reads these
│         studies)            │  parameters
├─────────────────────────────┤
│ Tier 2: Meta-analytical     │
│         estimates           │
├─────────────────────────────┤
│ Tier 3: Synthetic priors    │
│         (EBF defaults)      │
├─────────────────────────────┤
│ UPDATE TRIGGERS:            │
│ - Intervention results      │
│   (Intervention DB)         │
│ - New validations           │
│   (Model DB)                │
│ - Context changes           │
│   (Context DB)              │
└─────────────────────────────┘
```

---

## 6. Query Examples: Cross-Database

### Example 1: "What models apply to papal succession?"

```python
# Query MODEL DB
papal_models = registry.list_models_by_category("SUCCESSION")
# Returns: [PSF-2.0, planned CCP-SUCCESSION, planned MILITARY-SUCCESSION]

# Cross-reference to CASE REGISTRY
papal_cases = case_registry.find_cases_by_model("PSF-2.0")
# Returns: [CASE-UNMAPPED_PAP-1878-01, CASE-UNMAPPED_PAP-1903-01, ..., CASE-UNMAPPED_PAP-2025-01]

# Get context for each case
for case in papal_cases:
    context = context_registry.get_context_at_date(case.date)
    # Returns: Vatican conditions at that date
```

### Example 2: "Why did the 1922 model fail?"

```python
# Get case from CASE REGISTRY
case_1922 = case_registry.get_case("CASE-UNMAPPED_PAP-1922-01")

# Get model predictions
model_v1 = model_registry.get_model("PSF-2.0")
pred = model_v1.apply(case_1922.dimensions)
# Returns: P(Ratti) = 0.76, Ballots = 8

# Get actual outcomes
actual = case_1922.historical_outcome
# Returns: Winner = Ratti, Ballots = 14

# Analyze gap
gap = actual.ballots - pred.ballots  # +6 ballots
learning = case_1922.analysis.learning_point
# "Need complementarity parameters (γ) for factional dynamics"

# Trigger model improvement
improvement = model_registry.get_improvement("PHASE_2_TASK_2_1")
# Returns: "Complementarity Parameters - Timeline: Q3-Q4 2026"
```

### Example 3: "What if GDP collapsed in 2027?"

```python
# Scenario planning
current_context = context_registry.get_current()
scenario_context = current_context.copy()
scenario_context.economic.gdp_growth = 1.5  # Collapse

# Query: What models are sensitive to GDP?
sensitive_models = model_registry.query(
    sensitivity_to=["GDP_growth"]
)
# Returns: [TRUMP-COMPLIANCE, XI-REMOVAL, ...]

# Apply models under scenario
for model in sensitive_models:
    base_prediction = model.apply(current_context)
    scenario_prediction = model.apply(scenario_context)

    print(f"{model.id}: {base_prediction} → {scenario_prediction}")
    # Trump Compliance: 38% → 48%
    # Xi Removal Risk: 24% → 38%
```

---

## 7. Implementation Roadmap

### Immediate (Done)
- ✓ Model Database (models.registry.yaml)
- ✓ Model Schema (models.schema.yaml)
- ✓ Model Registry Manager (models_registry.py)

### Q1-Q2 2026 (Phase 1)
- [ ] Context Database (context-registry.yaml)
- [ ] Context Schema (context.schema.yaml)
- [ ] Context Manager (context_manager.py)
- [ ] Integration tests between Model DB + Context DB

### Q3-Q4 2026 (Phase 2)
- [ ] Enhanced Model DB with γ parameters
- [ ] Intervention Database improvements (better tracking)
- [ ] Learning Engine (auto-trigger improvements from case discrepancies)

### 2027+ (Phase 3)
- [ ] Parameter Repository automation (Tier 1-3 updates)
- [ ] Real-time context feeds (API integrations)
- [ ] Dashboard (query interface)
- [ ] Mobile app (decision support)

---

## Database Governance

### Roles

| Role | Responsibility |
|------|-----------------|
| **Model Steward** | Maintain Model DB; coordinate Phase 1-3 improvements |
| **Context Manager** | Real-time Ψ updates; scenario planning |
| **Intervention Lead** | Project tracking; learning extraction |
| **Case Curator** | Historical case data; cross-references |
| **Parameter Keeper** | Tier 1-3 values; update triggers |

### Update Procedures

**Model DB Update**:
1. New version created
2. Parameters tested (cross-validation)
3. Model DB updated
4. Validation re-run
5. Commit to git

**Context DB Update**:
1. Daily: Fetch latest economic/political data
2. Weekly: Assess institutional changes
3. Quarterly: Scenario review
4. Ad-hoc: Crisis event updates

**Intervention DB Update**:
1. Project launched → Create record
2. Predictions made → Store in DB
3. Outcomes observed → Record actual results
4. Gap analyzed → Extract learning
5. Parameters updated → Trigger model improvement

---

## Benefits of Integrated Architecture

✓ **Single Source of Truth**: Each piece of data lives in one place
✓ **Learning Loop**: Cases trigger model improvements automatically
✓ **Scenario Planning**: Query "what if Ψ changed?" on any model
✓ **Audit Trail**: Full history of predictions + outcomes + learnings
✓ **Generalization**: Reuse models across systems with Ψ remapping
✓ **Scalability**: Add new models without restructuring databases
✓ **Transparency**: All decisions traceable to models + context + data

---

## Next Steps

1. **Immediate**: Create Context Database schema + registry
2. **Q1 2026**: Build Context Manager (Python class)
3. **Q2 2026**: Integrate Model DB + Context DB
4. **Q3 2026**: Build Learning Engine (auto-trigger improvements)
5. **2027+**: Build dashboard + mobile interface

---

**Architecture Version**: 1.0
**Status**: Design Complete, Implementation Roadmap Ready
**Next Decision**: Start Context Database development?
