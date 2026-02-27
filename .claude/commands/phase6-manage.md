# Phase 6: Long-Term Outcome Tracking & Management

**Command:** `/phase6-manage`

Manage long-term follow-up measurements, decay analysis, and sustainability assessment.

## Quick Reference

```bash
# Schedule follow-ups
/phase6-manage schedule PRJ-001                    # Schedule default 3M/6M/12M/24M measurements
/phase6-manage schedule PRJ-001 --custom file.json # Custom timepoints
/phase6-manage schedule-all --pending               # Show all pending schedules

# Record measurements
/phase6-manage record PRJ-001 3M --file kpis.json  # Record 3M measurement
/phase6-manage record PRJ-001 12M --interactive    # Interactive entry
/phase6-manage pending                             # List all pending measurements

# Decay analysis
/phase6-manage analyze PRJ-001                     # Fit exponential decay model
/phase6-manage analyze PRJ-001 --model linear      # Fit linear decay
/phase6-manage predict PRJ-001 --months 24         # Project forward to 24M
/phase6-manage score PRJ-001                       # Calculate sustainability score

# Booster decisions
/phase6-manage check-decay PRJ-001                 # Check if booster triggered
/phase6-manage boosters --needed                   # List all projects needing boosters
/phase6-manage boosters PRJ-001 --trigger          # Trigger boosters if thresholds met

# Reports & learning
/phase6-manage report PRJ-001                      # Full Phase 6 report
/phase6-manage patterns --domain health            # Sustainability patterns by domain
/phase6-manage meta-analysis                       # Cross-project synthesis
/phase6-manage maintenance PRJ-001                 # Long-term maintenance strategies

# Detailed outputs
/phase6-manage decay-curve PRJ-001 --plot          # Visualize decay trajectory
/phase6-manage learnings --all                     # Extract all learnings across projects
```

---

## Commands

### `schedule` - Create follow-up measurement plan

```bash
/phase6-manage schedule PRJ-001
```

**What it does:**
- Creates default follow-up schedule (3M, 6M, 12M, 24M)
- Calculates measurement dates based on intervention end date
- Sets up tracking plan

**Options:**
- `--custom FILE`: Load custom timepoints from JSON
- `--timepoints "3M,6M,12M,24M"`: Override default schedule

**Output:**
```json
{
  "created": "2026-01-14T10:30:00",
  "measurement_points": [
    {
      "timepoint": "3M",
      "scheduled_date": "2026-03-30",
      "measurement_type": "survey",
      "target_metrics": ["participation_rate", "satisfaction", "behavior_frequency"],
      "sample_size_pct": 0.8,
      "priority": "high",
      "status": "pending"
    },
    ...
  ]
}
```

---

### `record` - Enter measurement data

```bash
/phase6-manage record PRJ-001 3M --file kpis.json
/phase6-manage record PRJ-001 12M --interactive
```

**What it does:**
- Records actual measurement at a timepoint
- Calculates delta vs predictions
- Detects attrition issues
- Triggers decay checks

**File format (kpis.json):**
```json
{
  "participation_rate": 0.88,
  "satisfaction": 7.8,
  "behavior_frequency": 4.2
}
```

**Output:**
```json
{
  "measurement_date": "2026-03-30",
  "sample_size": 250,
  "coverage": 0.8,
  "kpis": [
    {
      "name": "participation_rate",
      "actual_value": 0.88,
      "delta_vs_prediction": 0.02
    }
  ]
}
```

---

### `pending` - List all pending measurements

```bash
/phase6-manage pending
/phase6-manage pending --overdue
```

**What it does:**
- Lists all scheduled but not completed measurements
- Shows due dates and priorities
- Highlights overdue items

**Output:**
```
Found 8 pending measurements:

  PRJ-001     3M   2026-03-30  (high)   - Pension Opt-Out...
  PRJ-002     6M   2026-04-15  (high)   - Health Choice...
  PRJ-003    12M   2026-09-30  (medium) - Smart Meter...
  ...
```

---

### `analyze` - Fit decay model to data

```bash
/phase6-manage analyze PRJ-001
/phase6-manage analyze PRJ-001 --model linear
/phase6-manage analyze --all                      # Analyze all projects
```

**What it does:**
- Fits exponential decay model: E(t) = E₀ · e^(-ρ·t)
- Estimates monthly decay rate (ρ)
- Calculates time to 50% effect (t_half)
- Provides model quality metrics (R²)

**Output:**
```json
{
  "model": "exponential",
  "formula": "E(t) = E₀ · e^(-ρ·t)",
  "fitted_parameters": {
    "rho": 0.0823,
    "E_0": 0.5700,
    "t_half": 8.4
  },
  "model_fit": {
    "R_squared": 0.923,
    "n_observations": 3,
    "model_quality": "good"
  },
  "predictions": {
    "3M": 0.5418,
    "6M": 0.5163,
    "12M": 0.4697,
    "24M": 0.3862
  }
}
```

**Interpretation:**
- **ρ = 0.0823**: Monthly decay rate ~8.2%
- **t_half = 8.4 months**: Effect down to 50% by month 8
- **R² = 0.923**: Excellent model fit
- **12M prediction = 0.47**: Effect expected to be 47% of initial at 12M

---

### `predict` - Project effect forward in time

```bash
/phase6-manage predict PRJ-001 --months 24
/phase6-manage predict PRJ-001 --months 36 --plot
```

**What it does:**
- Projects effect trajectory E(t) into future
- Shows confidence bands (±15% by default)
- Highlights booster trigger points
- Optional visualization

**Output:**
```json
{
  "project_id": "PRJ-001",
  "model": "exponential",
  "trajectory": {
    "0M": {
      "predicted_effect": 0.5700,
      "ci_lower": 0.4845,
      "ci_upper": 0.6555
    },
    "3M": {
      "predicted_effect": 0.5418,
      "ci_lower": 0.4606,
      "ci_upper": 0.6231
    },
    "6M": {
      "predicted_effect": 0.5163,
      "ci_lower": 0.4389,
      "ci_upper": 0.5938
    },
    ...
    "24M": {
      "predicted_effect": 0.3862,
      "ci_lower": 0.3283,
      "ci_upper": 0.4442
    }
  }
}
```

---

### `score` - Calculate sustainability score

```bash
/phase6-manage score PRJ-001
/phase6-manage score --all --threshold 0.70
```

**What it does:**
- Calculates: S = (E₁₂M / E₀) × (1 - attrition)^0.5
- Classifies sustainability level
- Recommends booster strategy
- Sets maintenance priority

**Formula Explanation:**
- **E₁₂M / E₀**: What % of initial effect remains at 12M?
- **(1 - attrition)^0.5**: Penalty for sample loss
- **S ≥ 0.80**: Highly sustainable (no booster)
- **0.60-0.79**: Moderately sustainable (booster at 12M)
- **0.40-0.59**: Moderate decay (booster at 6M+12M)
- **S < 0.40**: Rapid decay (design review needed)

**Output:**
```json
{
  "sustainability_score": 0.756,
  "effect_retention": 0.823,
  "attrition_adjustment": 0.918,
  "classification": "Moderately sustainable",
  "recommended_action": "Booster at 12M recommended",
  "priority": "medium"
}
```

---

### `check-decay` - Check booster thresholds

```bash
/phase6-manage check-decay PRJ-001
/phase6-manage check-decay --all --trigger-boosters
```

**What it does:**
- Evaluates: Does effect decay cross booster trigger?
- Triggers if effect drops below 80% (6M) or 60% (12M)
- Schedules booster intervention if triggered
- Updates registry

**Thresholds:**
- **Effect < 80% of initial**: Light reminder booster
- **Effect < 60% of initial**: Medium re-engagement booster
- **Effect < 40% of initial**: Heavy structural intervention

**Output:**
```json
{
  "timepoint": "6M",
  "effect_retention_pct": 0.74,
  "trigger_booster": true,
  "booster_type": "reminder",
  "urgency": "medium"
}
```

---

### `report` - Generate comprehensive Phase 6 report

```bash
/phase6-manage report PRJ-001
/phase6-manage report PRJ-001 --format html --open
/phase6-manage report --all --format pdf
```

**What it does:**
- Comprehensive report combining:
  - Measurement timeline
  - Attrition analysis
  - Decay model & fit statistics
  - Sustainability score
  - Booster recommendations
  - Parameter updates
  - Key learnings

**Output Format:**
- `--format json`: Detailed data structure
- `--format html`: Formatted report for stakeholders
- `--format pdf`: Polished document

**Report Sections:**
1. **Summary**: Key metrics at a glance
2. **Measurements**: All timepoint data
3. **Decay Analysis**: Model parameters & fit
4. **Sustainability**: Classification & maintenance needs
5. **Boosters**: When/why/how to reinforce
6. **Learnings**: Generalizable insights
7. **Recommendations**: Next steps

---

### `patterns` - Extract sustainability patterns

```bash
/phase6-manage patterns
/phase6-manage patterns --domain health
/phase6-manage patterns --domain finance,health --intervention nudge
```

**What it does:**
- Analyzes sustainability across multiple projects
- Groups by domain or intervention type
- Identifies generalizable patterns
- Updates knowledge base

**Output:**
```json
{
  "patterns_analyzed": ["nudge", "social", "information"],
  "sustainability_by_intervention": {
    "nudge": {
      "average_effect_retention_12M": 0.82,
      "assessment": "Excellent - effect sustained",
      "n_projects": 3
    },
    "social": {
      "average_effect_retention_12M": 0.71,
      "assessment": "Good - minor decay"
    }
  },
  "key_patterns": [
    {
      "pattern": "Structural interventions (defaults, choice architecture) show excellent sustainability",
      "confidence": "high",
      "generalizability": "across domains"
    }
  ]
}
```

---

### `meta-analysis` - Cross-project synthesis

```bash
/phase6-manage meta-analysis
/phase6-manage meta-analysis --domains health,finance --min-projects 3
```

**What it does:**
- Synthesizes findings from multiple projects
- Identifies repeating patterns
- Estimates generalizability
- Updates parameter repository

**Output:**
```json
{
  "n_projects": 5,
  "domains_represented": ["finance", "health", "energy", "workplace"],
  "average_sustainability_score": 0.682,
  "generalizable_patterns": [
    {
      "pattern": "Effect decay follows exponential model with ρ ≈ 0.08-0.10",
      "confidence": "high",
      "n_supporting_projects": 5
    },
    {
      "pattern": "Defaults and choice architecture show ρ < 0.05 (very sustainable)",
      "confidence": "high"
    }
  ]
}
```

---

### `maintenance` - Long-term maintenance strategies

```bash
/phase6-manage maintenance PRJ-001
```

**What it does:**
- Analyzes decay characteristics
- Recommends maintenance approach
- Specifies frequency & cost
- Segment-specific strategies

**Strategy Options:**
1. **Structural Maintenance** (ρ < 0.05)
   - Maintain choice architecture
   - Annual check-in
   - Low cost

2. **Light Reinforcement** (0.05 ≤ ρ < 0.10)
   - Annual reminder campaign
   - Celebrate participation
   - Low cost

3. **Regular Booster Cycle** (ρ ≥ 0.10)
   - Semi-annual boosters
   - Vary intervention type
   - Medium cost

---

## Use Cases

### Use Case 1: Schedule & Track a New Project's 24-Month Lifecycle

```bash
# After intervention completes (6-month deployment)
/phase6-manage schedule PRJ-NEWPROJECT

# At 3 months post-intervention
/phase6-manage record PRJ-NEWPROJECT 3M --file survey_results_3m.json

# At 6 months (usually highest quality data)
/phase6-manage record PRJ-NEWPROJECT 6M --file admin_data_6m.json

# Check if any boosters needed
/phase6-manage check-decay PRJ-NEWPROJECT

# At 12 months (key sustainability verdict)
/phase6-manage record PRJ-NEWPROJECT 12M --file survey_results_12m.json
/phase6-manage score PRJ-NEWPROJECT
/phase6-manage analyze PRJ-NEWPROJECT

# Generate comprehensive report
/phase6-manage report PRJ-NEWPROJECT --format html
```

### Use Case 2: Extract Learnings for Next Project

```bash
# Find what worked in health domain
/phase6-manage patterns --domain health

# Get generalizable meta-patterns
/phase6-manage meta-analysis --domains health

# Get specific sustainability insights
/phase6-manage maintenance PRJ-001
```

### Use Case 3: Manage Booster Interventions

```bash
# Check which projects need boosters
/phase6-manage check-decay --all

# Get booster effectiveness from past projects
/phase6-manage patterns --booster-effectiveness

# Trigger boosters if thresholds crossed
/phase6-manage check-decay --all --trigger-boosters
```

---

## Data Flow Integration

Phase 6 integrates with existing systems:

```
Phase 5: /intervention-manage close PRJ-001
    ↓
Phase 6: /phase6-manage schedule PRJ-001
    ↓ (3-6-12-24 months later)
Phase 6: /phase6-manage record PRJ-001 [3M/6M/12M/24M]
    ↓
Phase 6: /phase6-manage analyze PRJ-001
    ↓
Phase 6: /phase6-manage patterns (extract learnings)
    ↓
Back to Phase 5: /design-model --decay-aware (use learnings for next project)
```

---

## Integration with `/intervention` command

Enhanced `/intervention` command with Phase 6 data:

```bash
/intervention PRJ-001 --phase 6              # Show Phase 6 results
/intervention PRJ-001 --decay                # Show decay curves
/intervention PRJ-001 --sustainability       # Show sustainability score
/intervention PRJ-001 --long-term-learnings  # Show learnings
```

---

## FAQ

**Q: When should I schedule follow-ups?**
A: Right after project completion (Phase 5 results recorded). Default is 3M, 6M, 12M, 24M post-intervention.

**Q: What's the minimum to measure?**
A: At least 6M (required for decay estimation). 12M is preferred for sustainability verdict.

**Q: What sample size do I need?**
A: Default: 80% at 3M, 100% at 6M (administrative), 60% at 12M, 40% at 24M. Adjust based on context.

**Q: When do I trigger a booster?**
A: Automatically when effect drops below 80% at 6M or 60% at 12M. Check via `/phase6-manage check-decay`.

**Q: How do I use decay learnings in next project?**
A: Use `/phase6-manage patterns` and `/design-model --decay-aware` to incorporate decay rates into next intervention.

---

## Implementation Details

- **Language**: Python 3.8+
- **Files**:
  - `scripts/phase6_longterm_tracker.py`
  - `scripts/phase6_decay_analyzer.py`
  - `scripts/phase6_learnings_extractor.py`
- **Data Source**: `data/intervention-registry.yaml`
- **Models**: Exponential (default), Linear, Segmented decay

---

**Next:** See `docs/PHASE_6_WORKFLOW_GUIDE.md` for step-by-step operational guide.
