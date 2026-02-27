# Phase 6: Long-Term Outcome Tracking & Effect Sustainability

**Status:** Implementation Phase 1
**Created:** 2026-01-14
**Branch:** `claude/add-outcome-tracking-fmuto`

---

## Executive Summary

Phase 6 extends the Phase 5 learning loop to track behavioral outcomes beyond initial measurement (6-9 months). It enables:

1. **Effect Sustainability**: Does behavior change persist over 12+ months?
2. **Decay Modeling**: How quickly do effects fade? At what rate (ρ)?
3. **Long-Term Meta-Learning**: Patterns across time horizons (months vs years)
4. **Booster Mechanics**: When and how do interventions need reinforcement?
5. **Outcome Evolution**: How does heterogeneous response develop over time?

---

## Phase 6 Architecture

### 6.1 Data Structure Extensions

The intervention-registry schema is extended with three new top-level sections:

#### A. Follow-Up Schedule (Planning)
```yaml
follow_up_schedule:
  measurement_points:
    - timepoint: 3M    # months post-intervention
      measurement_type: survey
      target_metrics: [participation_rate, satisfaction, behavior_frequency]
      sample_size_pct: 0.8
      priority: high
    - timepoint: 6M
      measurement_type: administrative
      target_metrics: [participation_rate, usage_frequency]
      sample_size_pct: 1.0
      priority: high
    - timepoint: 12M
      measurement_type: survey
      target_metrics: [participation_rate, satisfaction, relapse_likelihood]
      sample_size_pct: 0.6
      priority: medium
    - timepoint: 24M
      measurement_type: survey
      target_metrics: [participation_rate, behavior_naturalization, recommendations]
      sample_size_pct: 0.4
      priority: low

  booster_intervention_points:
    - timepoint: 6M
      trigger_condition: "decay detected (effect < 80% of initial)"
      intervention_type: reminder
      intensity: light
    - timepoint: 12M
      trigger_condition: "decay detected (effect < 60% of initial)"
      intervention_type: re-engagement
      intensity: medium
```

#### B. Long-Term Results (Actual Measurements)
```yaml
long_term_results:
  3M:
    measurement_date: '2025-12-30'
    sample_size: 250
    coverage: 0.8
    kpis:
      - name: participation_rate
        actual_value: 0.88
        delta_vs_prediction: 0.02
        confidence: high
      - name: satisfaction_score
        actual_value: 7.8
        scale: 1-10
  6M:
    measurement_date: '2026-03-30'
    sample_size: 312
    coverage: 1.0
    kpis:
      - name: participation_rate
        actual_value: 0.85
        delta_vs_12M_prediction: -0.01
      - name: opt_out_rate
        actual_value: 0.04
  12M:
    measurement_date: '2026-09-30'
    sample_size: 187
    coverage: 0.6
    attrition: 0.4
    kpis:
      - name: participation_rate
        actual_value: 0.81
        delta_vs_prediction: -0.05
```

#### C. Decay & Persistence Analysis
```yaml
decay_analysis:
  effect_decay:
    model: exponential
    formula: "E(t) = E₀ · e^(-ρ·t)"
    fitted_parameters:
      rho: 0.08  # monthly decay rate
      E_0: 0.57  # initial effect (from results section)
      t_half: 8.7  # months until 50% of effect remains
    model_fit:
      R_squared: 0.92
      AIC: 123.4
    predictions:
      3M: 0.54
      6M: 0.52
      12M: 0.48
      24M: 0.40

  by_segment:
    present-biased:
      observed_decay: slow
      rho: 0.05
      interpretation: "Sustained behavior once adopted"
    loss-averse:
      observed_decay: medium
      rho: 0.08
      interpretation: "Moderate fade-out"
    rational-calculative:
      observed_decay: fast
      rho: 0.12
      interpretation: "Early exit after initial trial"

  by_intervention:
    I1-Default:
      decay_pattern: very_slow
      mechanism: "Structural inertia maintains behavior"
      sustainability_score: 0.92
    I2-Reminder:
      decay_pattern: fast
      mechanism: "Effect diminishes when reminder ceases"
      sustainability_score: 0.45
```

### 6.2 Measurement Framework

#### Timepoint Strategy

| Timepoint | Months | Method | Sample | Priority | Use Case |
|-----------|--------|--------|--------|----------|----------|
| **Initial** | 0 | Baseline | 100% | - | Pre-intervention snapshot |
| **Short-term** | 3 | Survey | 80% | High | Early effect persistence |
| **Mid-term** | 6 | Admin | 100% | High | Effect stabilization |
| **Long-term** | 12 | Survey | 60% | Medium | Sustainability verdict |
| **Very Long-term** | 24 | Survey | 40% | Low | Maintenance needs |

**Rationale:**
- 3M: Detect immediate decay (avoid ceiling effects)
- 6M: Peak measurement (most robust sample)
- 12M: Long-term verdict (behavior sustained?)
- 24M: Maintenance phase (booster needs?)

#### Attrition Modeling

Natural attrition expected:
- 3M: ~20% (people leave, move, life changes)
- 6M: ~0% (administrative data assumed complete)
- 12M: ~40% (survey fatigue, life transitions)
- 24M: ~60% (significant natural attrition)

Controls for selection bias:
- Compare completers vs non-completers on initial behavior
- Weight results if non-random attrition detected
- Report sample composition

### 6.3 Decay Models

#### Model 1: Exponential Decay (Default)
```
E(t) = E₀ · e^(-ρ·t)

Parameters:
- E₀ = initial effect (from Phase 5 results)
- ρ = monthly decay rate (0 = no decay, 0.2 = rapid decay)
- t = months since intervention start
- t_half = ln(2)/ρ = time to 50% effect

Interpretation:
- ρ < 0.05: Very sustainable (decay imperceptible)
- 0.05 ≤ ρ < 0.10: Sustainable with slight fade
- 0.10 ≤ ρ < 0.15: Moderate decay (booster needed at 12M)
- ρ ≥ 0.15: Rapid decay (booster needed at 6M)
```

#### Model 2: Linear Decay (When appropriate)
```
E(t) = E₀ - β·t

For interventions with constant fade rate
Use when effect follows step function (e.g., incentive removal)
```

#### Model 3: Segmented Decay
Different decay patterns per behavioral segment:
```
E(t) = E_loss_averse(t) + E_present_biased(t) + E_rational(t)

Weighted by segment proportion and heterogeneity (σᵢ)
```

### 6.4 Sustainability Metrics

#### Primary Metric: Sustainability Score (0-1)

```
S = (E_12M / E_0) · (1 - attrition_rate)^0.5

Components:
- E_12M / E_0: What % of initial effect remains?
- Attrition adjustment: Penalize high sample loss

Thresholds:
- S ≥ 0.80: Highly sustainable (no booster needed)
- 0.60 ≤ S < 0.80: Moderately sustainable (booster at 12M)
- 0.40 ≤ S < 0.60: Moderate decay (booster at 6M+12M)
- S < 0.40: Rapid decay (consider structural vs behavioral intervention)
```

#### Secondary Metrics

1. **Booster Intervention Threshold**
   - When does decay trigger booster need?
   - Based on predicted E(t) < baseline + (E₀ - baseline) × 0.8

2. **Naturalization Score**
   - Does behavior become "automatic" (low cognitive load)?
   - Measured via survey at 12M
   - Scale: 1 (still effortful) to 5 (automatic habit)

3. **Relapse Rate**
   - % who return to baseline behavior at 12M
   - Key predictor of need for maintenance phase

4. **Contagion Effect**
   - Do participants influence non-participants to adopt?
   - Secondary outcome tracking

---

## Phase 6 Implementation Components

### Component 1: Registry Schema Extension

**File:** `data/intervention-registry.yaml`

```yaml
projects:
  PRJ-001:
    meta: {...}  # existing
    context: {...}  # existing
    intervention_mix: [...]  # existing
    predictions: {...}  # existing
    results: {...}  # existing (up to 6M)
    deviation_analysis: {...}  # existing
    learnings: {...}  # existing

    # NEW: Phase 6 sections
    follow_up_schedule:
      measurement_points: [...]
      booster_intervention_points: [...]

    long_term_results:
      3M: {...}
      6M: {...}
      12M: {...}
      24M: {...}

    decay_analysis:
      effect_decay: {...}
      by_segment: {...}
      by_intervention: {...}

    long_term_learnings:
      sustainability_verdict: "..."
      decay_patterns: {...}
      booster_recommendations: [...]
      meta_learnings: [...]
```

### Component 2: Scripts

#### script: `phase6_outcomes_tracker.py`

Manages follow-up measurement scheduling and data entry:

```python
class Phase6OutcomesTracker:
    """Manage long-term outcome tracking"""

    def schedule_follow_up(project_id, measurement_points):
        """Create schedule for future measurements"""

    def record_measurement(project_id, timepoint, kpis, metadata):
        """Enter measurement data at specific timepoint"""

    def detect_attrition(project_id, timepoint, actual_sample):
        """Flag unexpected attrition patterns"""

    def check_decay_threshold(project_id, timepoint):
        """Evaluate if decay triggers booster intervention"""

    def generate_follow_up_report(project_id):
        """Summary of follow-up measurements vs predictions"""
```

#### Script: `phase6_decay_analyzer.py`

Analyzes effect persistence and models decay:

```python
class Phase6DecayAnalyzer:
    """Model and analyze effect decay over time"""

    def fit_decay_model(project_id, model_type='exponential'):
        """Fit exponential/linear/segmented decay model"""
        # Returns: ρ (decay rate), t_half, model_fit metrics

    def predict_effect_trajectory(project_id, months_ahead=24):
        """Project effect forward: E(t) = E₀ · e^(-ρ·t)"""

    def calculate_sustainability_score(project_id):
        """S = (E_12M / E_0) · (1 - attrition_rate)^0.5"""

    def identify_segment_heterogeneity(project_id):
        """Which segments sustain behavior? Which fade quickly?"""

    def estimate_booster_needs(project_id):
        """When should boosters be triggered? What type?"""

    def generate_decay_report(project_id):
        """Comprehensive report: curves, parameters, recommendations"""
```

#### Script: `phase6_learnings_extractor.py`

Extracts meta-learnings from long-term data:

```python
class Phase6LearningsExtractor:
    """Extract insights from long-term tracking data"""

    def extract_sustainability_patterns(domain=None, intervention_type=None):
        """What interventions sustain? Across domains?"""

    def update_decay_parameters(project_id):
        """Update ρ (decay rate) in parameter repository (Appendix BBB)"""

    def identify_booster_effectiveness(project_id):
        """Did booster interventions work? What worked best?"""

    def extract_behavioral_patterns(project_id, segment=None):
        """How do different segments behave over 24 months?"""

    def generate_meta_analysis(domains=None, years=None):
        """Cross-project analysis: Which effect decay patterns repeat?"""

    def recommend_maintenance_strategies(project_id):
        """Based on observed decay, what keeps behavior sustained?"""
```

### Component 3: CLI Commands

#### New Command: `/phase6-manage`

```bash
/phase6-manage schedule PRJ-001
/phase6-manage schedule-all --test-mode  # Preview all upcoming measurements

/phase6-manage record PRJ-001 3M --file measurements.json
/phase6-manage record PRJ-001 12M --interactive

/phase6-manage check-decay PRJ-001
/phase6-manage check-decay --all --trigger-boosters

/phase6-manage analyze PRJ-001
/phase6-manage analyze PRJ-001 --model exponential --plot

/phase6-manage report PRJ-001 --format html  # Full Phase 6 report
/phase6-manage cross-project-analysis --domains health,finance
```

#### Enhanced Command: `/intervention`

```bash
/intervention PRJ-001 --phase 6              # Show Phase 6 data
/intervention PRJ-001 --decay                # Decay curves
/intervention PRJ-001 --sustainability       # Sustainability score
/intervention --learnings-long-term          # Long-term patterns
/intervention --decay-analysis --by-segment
```

### Component 4: Documentation

#### Document: `docs/PHASE_6_ARCHITECTURE.md` (this file)

Complete technical specification of Phase 6.

#### Document: `docs/PHASE_6_WORKFLOW_GUIDE.md`

Operational guide with step-by-step instructions:
- How to schedule follow-ups
- How to record measurements
- How to detect decay issues
- How to trigger boosters
- How to extract learnings

#### Document: `docs/PHASE_6_CASE_STUDIES.md`

Real examples:
- PRJ-001 extending to 24M (projection)
- Hypothetical booster intervention (PRJ-002)
- Cross-project meta-analysis

---

## Phase 6 Workflow Integration

### Extended 8-Stage Learning Loop (Now 10 Stages)

```
Stage 1: Design (Problem → Similar Cases → Linked Papers → Intervention)
Stage 2: Implementation (Real-world deployment 3-6 months)
Stage 3: Measurement (Collect actual results at 6-9M)
Stage 4: Analysis (Compare predictions to reality, extract learnings)
Stage 5: Learning (Update parameters from short-term data)
Stage 6: Iterate (Next project uses updated parameters)

NEW: Stage 7: Long-Term Tracking (Schedule 3M, 6M, 12M, 24M measurements)
NEW: Stage 8: Decay Analysis (Fit models, detect sustainability)
NEW: Stage 9: Booster Mechanics (Trigger reinforcement if needed)
NEW: Stage 10: Meta-Learning (Extract long-term patterns, update BBB)
```

### Integration Points

#### A. With /case-manage

```
/case-manage find PRJ-NEW --similar-timeline
→ Find cases with similar behavior (25+ years track record)
→ Extract long-term sustainability insights
```

#### B. With /design-model

```
/design-model PRJ-NEW --long-term-sustainable
→ Design with E_i values that have 12M+ track record
→ Include decay rates (ρ) from Phase 6 analysis
→ Select interventions with S ≥ 0.75
```

#### C. With /intervention-manage

```
/intervention-manage close PRJ-001 --schedule-follow-up
→ Automatically schedules 3M, 6M, 12M follow-ups
→ Sets reminders for measurement collection
→ Alerts if decay thresholds reached
```

---

## Parameter Updates (Appendix BBB Integration)

### New Parameters Estimated in Phase 6

#### 1. Decay Rates by Intervention Type
```
ρ (rho) = monthly decay rate
ρ[nudge-default] = 0.03 ± 0.02    # Very sustainable
ρ[nudge-labeling] = 0.08 ± 0.04   # Moderate decay
ρ[reminder] = 0.15 ± 0.06         # Rapid decay when removed
ρ[incentive] = 0.18 ± 0.05        # Rapid decay (extrinsic)
ρ[social-norm] = 0.06 ± 0.04      # Sustainable if internalized
```

#### 2. Sustainability Scores by Context
```
S[nudge + social] = 0.85 ± 0.08   (High complementarity sustains)
S[incentive alone] = 0.35 ± 0.12  (Low sustainability without social)
S[DACH culture] = 0.80 ± 0.05     (Cultural internalization)
```

#### 3. Booster Intervention Effectiveness
```
boost_effectiveness[6M-reminder] = 0.65 ± 0.10
boost_effectiveness[12M-re-engagement] = 0.55 ± 0.12
boost_effectiveness[social-reminder] = 0.75 ± 0.08
```

---

## Quality Assurance

### Validation Checklist

- [ ] Follow-up schedule created for all active/completed projects
- [ ] Measurement points align with Phase 5 predictions
- [ ] Attrition models documented per project
- [ ] Decay model fitted with R² > 0.80
- [ ] Sustainability score ≥ 0.70 or booster triggers identified
- [ ] Parameter updates cross-checked with Appendix BBB
- [ ] Booster interventions scheduled if S < 0.75
- [ ] Meta-learnings extracted and documented
- [ ] Cross-project patterns identified (n ≥ 3 for generalization)

### Measurement Quality Standards

- **Sample Size**: Report actual sample, n ≥ 30 for confidence claims
- **Attrition Bias**: Weighted analysis if attrition > 40%
- **Survey Validity**: Use validated scales where possible
- **Administrative Data**: Verify data source and completeness
- **Missing Data**: Multiple imputation if > 5% missing

---

## Phase 6 Timeline

### Immediate (January 2026)
- [x] Architecture specification (this document)
- [ ] Registry schema extension
- [ ] Implementation of phase6_outcomes_tracker.py

### Short-term (Feb-Mar 2026)
- [ ] Implementation of phase6_decay_analyzer.py
- [ ] Implementation of phase6_learnings_extractor.py
- [ ] CLI commands (/phase6-manage)

### Medium-term (Apr-Jun 2026)
- [ ] Workflow guide & case studies
- [ ] Integration with /design-model (decay-aware design)
- [ ] Appendix updates (PHASE-TRACKING)

### Long-term (Jul-Dec 2026+)
- [ ] First real 12M measurement cycle completes (PRJ-001)
- [ ] Meta-learnings from multiple projects (n ≥ 5)
- [ ] Parameter updates to Appendix BBB

---

## Appendix References

### Existing Appendices Extended by Phase 6

| Appendix | Category | Extension |
|----------|----------|-----------|
| BBB | CORE-WHERE | Add ρ (decay rates) by intervention type & context |
| JJJ | METHOD-TRACKING | Add long-term tracking section |
| EEE | METHOD-DESIGN | Add decay-aware model design (Step 6) |

### New Appendices (Phase 6)

**PP1: METHOD-DECAY**
Decay modeling theory, models, fitting procedures

**PP2: DOMAIN-SUSTAINABILITY**
Sustainability by domain: health, finance, energy, workplace

**PP3: REF-PHASE6**
Quick reference for Phase 6 operations

---

## References & Theoretical Foundation

### Effect Persistence in Economics Literature

- **Thaler & Sunstein (2008)**: Default effects persist when structural (not when removed)
- **Fehr & Gächter (2000)**: Social preferences effects sustain if internalized
- **Kahneman & Tversky (1979)**: Loss aversion persistence literature
- **Cialdini et al. (2006)**: Commitment effects sustain longer than simple information

### Decay Modeling in Behavioral Change Literature

- **Kwasnicka et al. (2016)**: Meta-review of behavior change maintenance
- **Lally et al. (2009)**: Habit formation takes 66 days on average, but highly variable
- **Michie et al. (2009)**: NICE guidelines on behavior change maintenance

### Phase 6 Implementation Language

- **Rationale**: Python (Phase 5 consistency)
- **Data Format**: YAML (Phase 5 consistency)
- **Documentation**: Markdown + LaTeX (framework consistency)
- **Visualization**: Matplotlib/Plotly (decay curves, confidence bands)

---

**Next Step**: Implement registry schema extension → Scripts → CLI → Documentation

**Questions?** See `docs/PHASE_6_WORKFLOW_GUIDE.md` for operational details
