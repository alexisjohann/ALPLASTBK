# Phase 5: Intervention Registry Architecture

**Status**: Foundation Phase | **Date**: January 14, 2026
**Purpose**: Theory-driven intervention design with prediction-outcome feedback loop

---

## 📋 Overview

Phase 5 transforms the EBF from a **static knowledge base** (Phases 1-4) into a **dynamic learning system** by:

1. **Designing interventions** rooted in behavioral theory (linked papers)
2. **Predicting outcomes** using complementarity mathematics
3. **Measuring results** against predictions
4. **Extracting learnings** for continuous improvement

---

## 🏗️ Architecture Layers

```
┌─────────────────────────────────────────────────────────────────┐
│ LAYER 5: LEARNING LOOP                                          │
│ (Learnings → Parameter Updates → Better Predictions)            │
├─────────────────────────────────────────────────────────────────┤
│ LAYER 4: OUTCOME MEASUREMENT                                    │
│ (Actual KPI Results, Attribution Analysis)                      │
├─────────────────────────────────────────────────────────────────┤
│ LAYER 3: INTERVENTION EXECUTION                                 │
│ (Deploy Nudges, Incentives, Information, Social)                │
├─────────────────────────────────────────────────────────────────┤
│ LAYER 2: PREDICTION SYSTEM                                      │
│ (E(P) = Σ E_i + Σ γ_ij · √(E_i · E_j))                          │
├─────────────────────────────────────────────────────────────────┤
│ LAYER 1: INTERVENTION DESIGN                                    │
│ (Papers → 9C Context → Intervention Mix)                        │
├─────────────────────────────────────────────────────────────────┤
│ FOUNDATION: Papers + Cases + 9C Linking (Phases 1-4)            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Workflow: From Theory to Learning

### Stage 1: Problem Definition
```
Input: Business/Policy Challenge
  ├─ Domain: finance, health, workplace, government, nonprofit, energy
  ├─ Target behavior: e.g., "retirement savings", "medication adherence"
  ├─ Target population: e.g., "Low-income earners", "Shift workers"
  ├─ Current status: Baseline behavior + journey phase
  └─ Success metric: What constitutes success?
```

### Stage 2: Intervention Design (NEW - Phase 5)
```
Process: Theory-Driven Design
  │
  ├─ Step 1: Find linked cases
  │  ├─ Query case-registry for similar scenarios
  │  ├─ Filter by domain + journey phase + population
  │  └─ Load 2-3 similar projects
  │
  ├─ Step 2: Identify applicable papers
  │  ├─ Get papers linked to selected cases
  │  ├─ Filter by mechanism relevance (9C match)
  │  └─ Suggest 5-10 foundational papers
  │
  ├─ Step 3: Design intervention mix
  │  ├─ 6 intervention types available:
  │  │  ├─ Nudge (default, framing, choice architecture)
  │  │  ├─ Incentive (monetary, social, status)
  │  │  ├─ Information (personalized, comparative, visualized)
  │  │  ├─ Commitment (pre-commitment, public, habit-based)
  │  │  ├─ Social (norm, peer influence, reciprocity)
  │  │  └─ Environmental (context, design, accessibility)
  │  │
  │  ├─ For each intervention:
  │  │  ├─ Specify target segment
  │  │  ├─ Set intensity & duration
  │  │  └─ Estimate E_i from literature or pilot
  │  │
  │  └─ Estimate complementarity matrix (γ_ij)
  │     ├─ Synergy: γ > 0 (interactions amplify effect)
  │     ├─ Neutral: γ ≈ 0 (independent effects)
  │     └─ Interference: γ < 0 (interactions reduce effect)
  │
  └─ Step 4: Calculate portfolio effect
     ├─ Formula: E(P) = Σ E_i + Σ γ_ij · √(E_i · E_j)
     ├─ Confidence intervals: CI_lower to CI_upper
     └─ Output: Predicted KPI improvements
```

### Stage 3: Prediction
```
Output: Quantified Predictions
  ├─ Portfolio Effect: E(P) with confidence intervals
  ├─ Individual KPIs:
  │  ├─ Baseline value
  │  ├─ Predicted value
  │  ├─ Expected delta (absolute)
  │  ├─ Expected delta (%)
  │  └─ Confidence level
  └─ Risk factors: What could go wrong?
```

### Stage 4: Execution
```
Phase: Real-World Implementation
  ├─ Deploy intervention mix
  ├─ Monitor compliance
  ├─ Track early indicators
  └─ Collect process data
```

### Stage 5: Measurement & Analysis (NEW - Phase 5)
```
Process: Outcome Measurement
  │
  ├─ Collect actual KPI results
  ├─ Compare to predictions
  ├─ Analyze deviations
  │  ├─ Overall: Did portfolio effect materialize?
  │  ├─ By intervention: Which components worked?
  │  ├─ By segment: Who responded best?
  │  └─ Root causes: Why did we miss/exceed?
  │
  └─ Output: Deviation analysis report
```

### Stage 6: Learning Extraction (NEW - Phase 5)
```
Process: Continuous Improvement
  │
  ├─ Identify what worked
  │  └─ Generalizable patterns?
  │
  ├─ Identify what didn't work
  │  └─ Avoidable mistakes?
  │
  ├─ Update parameters
  │  ├─ E_i estimates (more accurate next time)
  │  ├─ γ_ij values (complementarity stronger/weaker than expected?)
  │  └─ Confidence levels (did we overestimate certainty?)
  │
  ├─ Generate recommendations
  │  ├─ Design improvements
  │  ├─ Timing adjustments
  │  ├─ Targeting refinements
  │  └─ Measurement enhancements
  │
  └─ Feed back to BBB (Parameter Repository)
```

---

## 🗂️ Core Data Files

### 1. intervention-registry.yaml
```yaml
projects:
  PRJ-XXX:
    meta:
      - name, client, domain, status
    context:
      - target_behavior, journey_phase, segments
    intervention_mix:
      - 1-6 interventions with E_i estimates
    complementarity_matrix:
      - γ_ij values between intervention pairs
    predictions:
      - portfolio_effect (E(P) with CI)
      - kpis (baseline, predicted, confidence)
    results:
      - measurement_date, actual KPIs
    deviation_analysis:
      - predicted vs actual, root causes
    learnings:
      - what_worked, what_didnt, parameter_updates
```

### 2. BBB Parameter Repository (Appendix)
```
Parameter Source of Truth:
├─ E_i by intervention type
├─ γ_ij by intervention pair
├─ Confidence by data source
└─ Updates from real-world outcomes
```

### 3. Linked Data Inputs
```
Phase 4 Output:
├─ paper-sources.yaml (521 papers)
├─ case-registry.yaml (846 cases)
├─ linked_cases field (24,237 links)
└─ source_paper field (bidirectional)
```

---

## 🔧 Phase 5 Scripts

### Script 1: intervention_design.py
**Purpose**: Interactive intervention design from linked papers
**Input**: Problem specification (domain, behavior, population, phase)
**Process**:
1. Find similar cases from case-registry
2. Get linked papers for those cases
3. Extract mechanisms from papers
4. Build intervention mix with E_i estimates
5. Calculate complementarity matrix
6. Compute portfolio effect

**Output**: Complete intervention design stored in registry
**Key Functions**:
- `find_similar_cases()` - Query case-registry by 9C match
- `get_relevant_papers()` - Get papers linked to cases
- `design_intervention_mix()` - Build intervention portfolio
- `estimate_complementarity()` - Calculate γ_ij matrix
- `predict_portfolio_effect()` - Compute E(P) with CI
- `register_project()` - Save to intervention-registry

### Script 2: intervention_analyzer.py
**Purpose**: Deviation analysis (predicted vs actual)
**Input**: Completed project with results
**Process**:
1. Load predictions and actual results
2. Calculate overall deviation
3. Analyze by intervention (which components worked?)
4. Analyze by segment (who responded?)
5. Identify root causes
6. Calculate learnings

**Output**: Comprehensive deviation analysis report
**Key Functions**:
- `analyze_overall_deviation()` - E(P) predicted vs actual
- `analyze_by_intervention()` - Individual component performance
- `analyze_by_segment()` - Differential response rates
- `identify_root_causes()` - Why did we deviate?
- `generate_report()` - Structured analysis output

### Script 3: learnings_extractor.py
**Purpose**: Extract learnings and update parameters
**Input**: Deviation analysis
**Process**:
1. Identify patterns across projects
2. Update E_i estimates based on evidence
3. Update γ_ij values from observed interactions
4. Increase/decrease confidence based on accuracy
5. Extract generalizable insights
6. Generate improvement recommendations

**Output**: Parameter updates + recommendations
**Key Functions**:
- `extract_what_worked()` - Identify successes
- `extract_what_didnt()` - Identify failures
- `update_parameters()` - E_i, γ_ij, confidence adjustments
- `generate_recommendations()` - Improvement suggestions
- `propagate_updates()` - Update BBB appendix

---

## 📊 Example Workflow: Finance Domain

### Problem
```
Client: Bank XYZ
Challenge: Increase retirement account enrollment among employees
Current enrollment: 28%
Target: 50%+
Population: Mostly 25-40 year-old mid-level staff
```

### Step 1: Design
```
Script: python3 scripts/intervention_design.py
Input:
  ├─ Domain: finance
  ├─ Behavior: retirement savings
  ├─ Population: mid-career workers
  ├─ Phase: contemplation
  └─ Target: +22 percentage points
```

### Step 2: Similar Cases
```
Script output: Find PRJ-001 (Opt-Out Implementation)
├─ Domain match: ✓ Finance
├─ Behavior match: ✓ Retirement
├─ Population match: ✓ Employees
└─ Result: +25 points (baseline 34% → 59%)
```

### Step 3: Linked Papers
```
Papers from PRJ-001:
├─ Thaler & Benartzi (2004) - Save More Tomorrow
├─ Madrian & Shea (2001) - Power of Default
├─ Cialdini (2006) - Social Influence
└─ ... 235 other papers from "Finance" domain case
```

### Step 4: Design Mix
```
Selected interventions:
├─ I1: Automatic enrollment (nudge)
│  └─ E_i: 0.35 (from Madrian & Shea literature)
├─ I2: Personalized projection (information)
│  └─ E_i: 0.08 (from pilot data)
├─ I3: Social norm messaging (social)
│  └─ E_i: 0.05 (from Cialdini)
└─ I4: Peer commitment program (commitment)
    └─ E_i: 0.07 (estimated from theory)
```

### Step 5: Complementarity
```
Matrix analysis:
├─ γ(I1, I2) = 0.3 (synergy: default + info improves informed choice)
├─ γ(I1, I3) = 0.2 (synergy: norm legitimizes default)
├─ γ(I1, I4) = 0.15 (synergy: commitment reinforces default)
├─ γ(I2, I3) = 0.1 (weak: info + norm are somewhat redundant)
├─ γ(I2, I4) = 0.25 (synergy: info + commitment strengthen each other)
└─ γ(I3, I4) = 0.15 (synergy: norm + commitment together stronger)
```

### Step 6: Prediction
```
E(P) = 0.35 + 0.08 + 0.05 + 0.07          [individual effects]
     + 0.3·√(0.35·0.08)                    [I1-I2 interaction]
     + 0.2·√(0.35·0.05)                    [I1-I3 interaction]
     + 0.15·√(0.35·0.07)                   [I1-I4 interaction]
     + 0.1·√(0.08·0.05)                    [I2-I3 interaction]
     + 0.25·√(0.08·0.07)                   [I2-I4 interaction]
     + 0.15·√(0.05·0.07)                   [I3-I4 interaction]

   = 0.55 + 0.062 + 0.033 + 0.027 + 0.008 + 0.013 + 0.005
   = 0.697

Confidence: 0.70 (moderate-high, based on literature + pilot)
CI: [0.55, 0.84]

Predicted enrollment: 28% + 69.7% of remaining 72% = 28% + 50% = 78%
```

### Step 7: Execute & Measure
```
Timeline: 3-month deployment
├─ Month 0: Auto-enrollment + opt-out option
├─ Month 1: Personalized statements + social messaging
├─ Month 2: Peer commitment challenges
└─ Month 3: Measurement & analysis
```

### Step 8: Results
```
Measurement date: Month 3
├─ Predicted enrollment: 78%
├─ Actual enrollment: 82%
├─ Delta: +4 percentage points (overestimate risk avoided)
└─ Confidence gained: Prediction was within 5%
```

### Step 9: Deviation Analysis
```
Good surprises:
├─ I1 (auto-enrollment): 38% actual vs 35% predicted (+3%)
│  └─ Reason: New employee cohort more responsive than expected
├─ I2-I4 interactions: Stronger than anticipated
│  └─ Reason: Peer groups amplified each other
└─ Overall: Portfolio effect stronger than expected

Lessons learned:
├─ E_i for auto-enrollment: 0.35 → 0.38 (update parameter)
├─ γ (multi-intervention): 0.18 average → 0.22 (update matrix)
├─ Confidence levels: We were well-calibrated (keep at 0.70)
└─ Recommendation: Increase peer-based interventions in similar contexts
```

---

## 🔄 Learning Loop Integration

```
Phase 1-4: Static Knowledge
├─ Papers (521)
├─ 9C Annotations (100%)
├─ Cases (846)
└─ Links (24,237)

Phase 5: Dynamic Learning
├─ Design interventions from papers
├─ Predict outcomes (E(P), confidence)
├─ Execute with clients
├─ Measure results
├─ Compare to predictions
├─ Extract learnings
├─ Update parameters (E_i, γ_ij, confidence)
└─ LOOP: Next design uses better parameters

Feedback targets:
├─ BBB Parameter Repository (Appendix)
│  └─ Update E_i values for each intervention
│  └─ Update γ_ij values for each pair
│  └─ Update confidence by source (literature/pilot/real-world)
│
├─ Intervention Registry (Meta-learning)
│  └─ Track what designs work in which contexts
│  └─ Segment-specific insights
│  └─ Domain-specific patterns
│
└─ Case Registry (Enrich with outcomes)
    └─ Link intervention results to cases
    └─ Enable similarity search on outcomes
```

---

## 📈 Success Metrics for Phase 5

| Metric | Target | Why It Matters |
|--------|--------|----------------|
| Prediction accuracy | ±20% average deviation | Calibration test |
| Parameter stability | σ < 15% across projects | Converging to true values |
| Confidence calibration | Confidence = actual accuracy | Well-calibrated predictions |
| Learning extraction | ≥5 generalizable insights per project | Cumulative improvement |
| Parameter updates | ≥3 updated per completed project | Dynamic refinement |
| Reuse rate | ≥70% designs reuse prior learnings | Leverage knowledge |

---

## 🚀 Phase 5 Timeline

**Stage 1: Foundation (This Week)**
- ✅ Create intervention_design.py
- ✅ Create intervention_analyzer.py
- ✅ Create learnings_extractor.py
- ✅ Document Phase 5 architecture

**Stage 2: Integration (Next Week)**
- Link scripts to case/paper registries
- Create interactive workflow
- Build parameter management system
- Create deviation analysis templates

**Stage 3: Pilot Projects (Week 3-4)**
- Run 2-3 pilot projects through full cycle
- Validate prediction system
- Calibrate confidence levels
- Extract first batch of learnings

**Stage 4: Scale (Month 2+)**
- Deploy to multiple domains
- Accumulate projects
- Continuous parameter refinement
- Build meta-learnings

---

## 🔗 Integration with Prior Phases

```
Phase 1-2: Papers + 9C Annotation
    ↓
Phase 3: DOI/URL Access (enables literature retrieval)
    ↓
Phase 4: Paper-Case Linking (enables design-by-analogy)
    ↓
Phase 5: Intervention Design + Learning Loop (applies theory to practice)
    ↓
Phase 6: Long-term Tracking (measures impact over years)
```

---

## 📝 Next Steps

1. **Create intervention_design.py** - Interactive design tool
2. **Create intervention_analyzer.py** - Deviation analysis
3. **Create learnings_extractor.py** - Parameter updates
4. **Build workflow documentation** - Step-by-step guides
5. **Create Phase 5 starter template** - For new projects
6. **Generate integration roadmap** - Connect to case/paper systems

---

*Phase 5 Foundation | January 14, 2026*
*Framework: 4/6 phases complete → 5/6 in progress*

