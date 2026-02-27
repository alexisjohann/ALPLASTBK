# Phase 5: Intervention Design & Learning Loop Workflow

**Status**: Foundation Phase | **Date**: January 14, 2026
**Tools**: 3 core scripts + intervention-registry.yaml + linked papers/cases

---

## 🎯 Quick Start: Complete Workflow

### Scenario: Design a Pension Enrollment Intervention

```bash
# Step 1: Design interventions from linked theory
python3 scripts/phase5_intervention_design.py

# Output: Creates PRJ-004 with:
# ├─ 3 interventions designed
# ├─ Complementarity matrix
# ├─ Portfolio effect predicted: 43%
# └─ Confidence intervals

# Step 2: Execute the intervention (real-world implementation)
# [Deploy for 3-6 months]

# Step 3: Measure outcomes
# [Collect actual KPI results]

# Step 4: Analyze deviations (predicted vs actual)
python3 scripts/phase5_intervention_analyzer.py

# Output: Comprehensive analysis
# ├─ Overall E(P) deviation
# ├─ Performance by intervention
# ├─ Performance by segment
# ├─ Root causes for deviations
# └─ Accuracy assessment

# Step 5: Extract learnings
python3 scripts/phase5_learnings_extractor.py

# Output: Continuous improvement
# ├─ What worked / What didn't
# ├─ Parameter updates (E_i, γ_ij, confidence)
# ├─ Segment-specific insights
# ├─ Actionable recommendations
# └─ Meta-learnings across projects
```

---

## 📚 Understanding the Tools

### Script 1: intervention_design.py

**Purpose**: Design evidence-based interventions from linked papers

**How it works**:
```
Input: Problem (domain, behavior, population, phase)
  ↓
Find similar cases in case-registry
  ↓
Extract papers linked to those cases
  ↓
Identify behavioral mechanisms (9C dimensions)
  ↓
Design intervention mix (nudges, incentives, etc.)
  ↓
Estimate E_i (expected contribution) from literature
  ↓
Calculate complementarity matrix (γ_ij)
  ↓
Compute portfolio effect E(P) = Σ E_i + Σ γ_ij · √(E_i · E_j)
  ↓
Output: Complete intervention project with predictions
```

**Key concepts**:
- **E_i**: Individual intervention effectiveness (0-1 scale)
- **γ_ij**: Complementarity between intervention i and j
  - γ > 0.15: Synergy (interactions amplify)
  - γ ≈ 0: Neutral (independent)
  - γ < 0: Interference (interactions reduce effect)
- **E(P)**: Portfolio effect = combined effectiveness with interactions

**Example output**:
```yaml
PRJ-004:
  intervention_mix:
    - id: I1
      type: nudge
      expected_contribution:
        E_i: 0.30      # 30% of remaining behavior change
        confidence: 0.85
        source: literature

  predictions:
    portfolio_effect:
      E_P: 0.43       # Combined 43% effect after complementarity
      CI_lower: 0.37
      CI_upper: 0.49
      confidence: 0.70
```

### Script 2: intervention_analyzer.py

**Purpose**: Compare predictions to outcomes and identify causes

**When to use**: After project completion with measurement results

**Outputs**:
1. **Overall Deviation Analysis**
   - Predicted E(P) vs Actual E(P)
   - Percentage deviation
   - Accuracy classification

2. **By Intervention Analysis**
   - Which components worked?
   - Which underperformed?
   - Attribution confidence

3. **By Segment Analysis**
   - Did all segments respond equally?
   - Which overperformed / underperformed?
   - Segment-specific patterns

4. **Root Cause Analysis**
   - Why did we miss/exceed predictions?
   - Evidence strength (high/medium/low confidence)

**Example output**:
```
PROJECT: PRJ-001
Status: completed

OVERALL DEVIATION ANALYSIS
Predicted E(P):  52.0%
Actual E(P):     86.4%
Deviation:       +34.4% (UNDERESTIMATE)
Accuracy:        >30% (larger deviation than acceptable)

BY INTERVENTION ANALYSIS
✓ I1 (nudge):           E_i 0.35 → 0.42 (+20%) [HIGH confidence]
✗ I2 (information):     E_i 0.08 → 0.06 (-25%) [MEDIUM confidence]
✗ I3 (social):          E_i 0.05 → 0.04 (-20%) [LOW confidence]
```

### Script 3: learnings_extractor.py

**Purpose**: Extract insights and update parameters for next projects

**Extracts**:
1. **What worked** (generalizable patterns)
2. **What didn't** (avoidable mistakes)
3. **Parameter updates** (E_i, γ_ij values from evidence)
4. **Recommendations** (design/timing/targeting/measurement improvements)
5. **Segment insights** (differential response rates)
6. **Meta-learnings** (patterns across projects)

**Example updates**:
```yaml
parameter_updates:
  - parameter: "E_i for Nudge (default) in finance"
    old_value: 0.35
    new_value: 0.42
    basis: "Observation from PRJ-001, n=312"

  - parameter: "γ_ij for (nudge, information) pair"
    old_value: 0.30
    new_value: 0.35
    basis: "Stronger synergy than expected in PRJ-001"

  - parameter: "confidence_level"
    old_value: 0.70
    new_value: 0.85
    basis: "Well-calibrated predictions in finance domain"
```

---

## 🔄 The Complete Learning Loop

```
Phase 5 Learning Loop:

START
  ↓
1. DESIGN (intervention_design.py)
  ├─ Input: Problem specification
  ├─ Process: Papers → 9C → Intervention mix
  └─ Output: Predicted E(P) with confidence intervals
  ↓
2. IMPLEMENT
  ├─ Deploy interventions in real-world
  ├─ Track execution fidelity
  └─ Collect compliance data
  ↓
3. MEASURE
  ├─ Collect actual KPI results
  ├─ Calculate actual E(P)
  └─ Document any deviations
  ↓
4. ANALYZE (intervention_analyzer.py)
  ├─ Compare predicted vs actual
  ├─ Identify which components worked
  ├─ Analyze segment-level differences
  └─ Root cause analysis
  ↓
5. LEARN (learnings_extractor.py)
  ├─ Extract generalizable insights
  ├─ Update parameters (E_i, γ_ij, confidence)
  ├─ Generate recommendations
  └─ Feed updates to BBB Repository
  ↓
6. ITERATE (LOOP)
  ├─ Use updated parameters in next design
  ├─ Incorporate lessons learned
  ├─ Apply recommendations
  └─ GOTO STEP 1
  ↓
CONTINUOUS IMPROVEMENT
```

---

## 📋 Typical Project Timeline

### Week 1-2: Design Phase
```
Mon: Define problem, gather requirements
Tue: Research similar cases and papers
Wed: Run intervention_design.py
Thu: Refine design with stakeholders
Fri: Finalize project specifications
```

### Week 3-12: Implementation Phase (variable)
```
Deploy interventions
Monitor compliance
Track early indicators
Collect process data
```

### Week 13: Measurement Phase
```
Collect final KPI results
Calculate actual outcomes
Prepare results for analysis
```

### Week 14: Analysis Phase
```
Mon-Tue: Run intervention_analyzer.py
Wed: Interpret deviation analysis
Thu: Stakeholder review
Fri: Prepare learnings extraction
```

### Week 15: Learning Phase
```
Mon: Run learnings_extractor.py
Tue-Wed: Extract insights
Thu: Update BBB parameters
Fri: Documentation + recommendations
```

### Week 16: Loop Back
```
Start next design cycle with updated parameters
```

---

## 💾 Data Management

### Key Files

**Intervention Registry** (primary working file):
```
data/intervention-registry.yaml
├─ projects: [PRJ-001, PRJ-002, ...]
│  ├─ meta: project metadata
│  ├─ context: problem definition
│  ├─ intervention_mix: designed interventions
│  ├─ complementarity_matrix: γ_ij values
│  ├─ predictions: E(P) and KPI predictions
│  ├─ results: actual measurements (after execution)
│  ├─ deviation_analysis: predicted vs actual
│  └─ learnings: insights and updates
└─ [Easy to version, git-track]
```

**Linked Data** (from Phases 1-4):
```
data/paper-sources.yaml (521 papers)
  ├─ linked_cases: papers point to cases
  └─ [Input for intervention_design.py]

data/case-registry.yaml (846 cases)
  ├─ source_paper: cases point to papers
  └─ [Input for finding similar cases]
```

**Parameter Repository** (BBB Appendix):
```
appendices/BBB_PARAMETER_REPOSITORY.tex
├─ E_i by intervention type
│  ├─ By domain (finance, health, workplace, etc.)
│  ├─ By population (age, income, education)
│  └─ Confidence levels (literature/pilot/real-world)
│
├─ γ_ij by intervention pair
│  ├─ Known synergies
│  ├─ Known interferences
│  └─ Domain-specific complementarities
│
└─ [Updated by learnings_extractor.py]
```

---

## 🎓 Learning: From Prediction to Knowledge

### Parameter Updates Flow

```
Project Execution
  ↓
Actual Results
  ↓
Deviation Analysis
  ↓
Root Causes Identified
  ↓
Parameter Updates Calculated
  ├─ ΔE_i = actual - predicted (for each intervention)
  ├─ Δγ_ij = observed - assumed (for each pair)
  └─ Δconfidence = accuracy of prediction
  ↓
Updates Propagate to BBB
  ├─ E_i[finance, nudge, default] ← 0.35 to 0.42
  ├─ γ[nudge, information] ← 0.30 to 0.35
  ├─ confidence[finance, literature] ← 0.70 to 0.85
  └─ [Historical tracking of all updates]
  ↓
Next Project Design
  ├─ Uses updated E_i values (more accurate)
  ├─ Uses updated γ_ij values (better complementarity)
  ├─ Uses updated confidence (better calibration)
  └─ [Predictions improve iteratively]
```

---

## 🚀 Advanced: Custom Analysis

### Add project measurement results manually:

```yaml
projects:
  PRJ-004:
    # ... design fields ...

    results:
      measurement_date: "2026-02-28"
      kpis:
        - name: "Retirement enrollment rate"
          actual_value: 0.56  # 56% actual enrollment
          actual_delta: 0.28
          actual_delta_pct: 100

      intervention_effects:
        - id: "I1"
          observed_E_i: 0.32
          attribution_confidence: 0.85
        - id: "I2"
          observed_E_i: 0.12
          attribution_confidence: 0.60
        - id: "I3"
          observed_E_i: 0.04
          attribution_confidence: 0.40

      deviation_analysis:
        overall:
          predicted_E_P: 0.43
          actual_E_P: 0.48
          delta: 0.05
          delta_pct: 11.6
          direction: "underestimate"

        by_segment:
          - segment: "segment_1"
            predicted_response: 0.40
            actual_response: 0.52
            delta: 0.12
          - segment: "segment_2"
            predicted_response: 0.50
            actual_response: 0.58
            delta: 0.08
```

Then run:
```bash
python3 scripts/phase5_intervention_analyzer.py    # Analyze deviations
python3 scripts/phase5_learnings_extractor.py      # Extract learnings
```

---

## 🔗 Integration with Framework

### Papers → Cases → Design Loop

```
Phase 1-4: Static Knowledge
├─ 521 Papers (9C-annotated)
├─ 846 Cases (9C-annotated)
└─ 24,237 Links (bidirectional)

Phase 5: Dynamic Learning
├─ Intervention Design (theory → practice)
├─ Prediction System (math-based E(P))
├─ Outcome Measurement (real-world feedback)
├─ Deviation Analysis (what happened?)
├─ Learning Extraction (what did we learn?)
└─ Parameter Updates (improve for next time)
```

### Closing the Loop

```
Project 1 (PRJ-001):
├─ Design from papers + cases
├─ Predict E(P) = 0.52
├─ Actual E(P) = 0.864
├─ Update: nudge effectiveness 0.35 → 0.42
└─ Learn: complementarity stronger than assumed

Project 2 (PRJ-002):
├─ Design using UPDATED parameters
├─ Predict E(P) = 0.48 (better estimate)
├─ Actual E(P) = 0.43
├─ Update: information effectiveness 0.08 → 0.06
└─ Learn: information less effective in health

Project 3 (PRJ-003):
├─ Design using TWICE-updated parameters
├─ Predict E(P) = 0.45 (even better estimate)
├─ Actual E(P) = 0.44
├─ Confidence improves: 70% → 85%
└─ CONVERGENCE: Parameters stabilizing
```

---

## ✅ Phase 5 Checklist

### Before Starting a New Project
- [ ] Have similar projects completed? If yes, review learnings
- [ ] Are relevant papers linked to cases? If no, run Phase 4
- [ ] What domain? Check BBB parameters for that domain
- [ ] What population? Check if segment-specific parameters exist
- [ ] What journey phase? Use matching cases for context

### During Design
- [ ] run `python3 scripts/phase5_intervention_design.py`
- [ ] Verify E_i estimates from literature/pilots
- [ ] Set realistic confidence intervals
- [ ] Get stakeholder approval on predictions
- [ ] Document assumptions (especially γ_ij values)

### During Implementation
- [ ] Track fidelity (did interventions deploy as designed?)
- [ ] Monitor early indicators (not just end-state)
- [ ] Document any deviations from plan
- [ ] Keep segment membership data clean

### During Measurement
- [ ] Use same KPI definitions as predicted
- [ ] Ensure comparable measurement periods
- [ ] Collect segment-level data (not just aggregate)
- [ ] Document measurement challenges

### During Analysis
- [ ] run `python3 scripts/phase5_intervention_analyzer.py`
- [ ] Interpret deviations (not random noise?)
- [ ] Identify root causes (stakeholder interviews?)
- [ ] Segment analysis: which groups responded?

### During Learning
- [ ] run `python3 scripts/phase5_learnings_extractor.py`
- [ ] Update BBB parameters with evidence
- [ ] Generate recommendations (actionable?)
- [ ] Share insights with team
- [ ] Plan next project incorporating learnings

---

## 🎯 Success Indicators

| Indicator | Target | What It Means |
|-----------|--------|---------------|
| Prediction accuracy | ±20% average | Well-calibrated forecasts |
| Parameter stability | σ < 15% | Converging to true values |
| Confidence calibration | Confidence = accuracy | Realistic uncertainty estimates |
| Learning extraction rate | ≥5 per project | Cumulative improvement |
| Reuse rate | ≥70% | Leveraging prior knowledge |
| Portfolio effect improvement | +15% per 5 projects | System getting smarter |

---

## 📞 Support & Troubleshooting

**Script doesn't find similar cases?**
- Check: Are your cases tagged with domains?
- Solution: Run Phase 4 linker if not already done

**Parameter values seem off?**
- Check: Are estimates from literature or real data?
- Solution: Use literature values initially, update with real projects

**Confidence intervals too wide?**
- Check: Are E_i estimates uncertain?
- Solution: Run pilots to narrow CI before full deployment

**Learnings don't match observations?**
- Check: Were predictions documented correctly?
- Solution: Review actual vs predicted side-by-side

---

## 🚀 Next: Phase 6

**Phase 6: Long-Term Outcome Tracking**
- Track behavior change over months/years
- Measure sustainability
- Detect decay in effects
- Update parameters for long-term performance
- Enable meta-analysis across time horizons

---

*Phase 5 Workflow Guide | January 14, 2026*
*For questions about specific scripts, see PHASE_5_ARCHITECTURE.md*

