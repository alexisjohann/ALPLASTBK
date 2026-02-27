# Phase 6.5 Week 3: Integration with Phase 6 Stakeholder Simulation

**Status:** PLANNING
**Date:** 2026-01-16
**Branch:** claude/connect-strategic-models-ebf-av1cT

---

## Overview

Phase 6.5 Week 3 integrates **Job Design Analysis** (Phase 6.5) with **Stakeholder Behavior Simulation** (Phase 6) to create a unified framework for HR hiring decisions that accounts for job complexity, automation risk, and engagement.

**Scope:**
1. Update Phase 6 HR decision function to use job design metrics
2. Add 3-5 additional job profiles (expand beyond ALPLA)
3. Create integration tests
4. Build scenario analysis for job design changes

---

## Integration Architecture

### Current State (Phase 6 Only)
```
Phase 6 HR Decision:
  P(HR approves hiring) = f(revenue_forecast, capability, other_factors)
  = sigmoid(0.5 + 0.8×revenue + 0.7×capability + ...)
  = 84% baseline
```

### Integrated State (Phase 6 + 6.5)
```
Phase 6 HR Decision with Job Design:
  P(HR approves hiring) = f(revenue, capability, JOB_DESIGN_FACTORS)

  JOB_DESIGN_FACTORS:
    • Complexity adjustment: ±2pp based on complexity (< 2.5 → -2, > 3.5 → +1)
    • Engagement adjustment: ±1pp based on engagement (< 5 → -1, > 7 → +0.5)
    • Automation risk adjustment: ±1pp based on automation (> 70% → -1, < 30% → +0.5)
    • Wage fairness adjustment: ±0.5pp (underpaid → -0.5, overpaid → +0.25)

  = sigmoid(0.5 + 0.8×revenue + 0.7×capability + 0.4×job_design_score + ...)
```

### Data Flow
```
┌─────────────────────────────────────────────────────────┐
│ Job Design Evaluation (Phase 6.5)                       │
│  • Complexity Score (0-5)                               │
│  • Automation Risk (0-100%)                             │
│  • Engagement Score (0-10)                              │
│  • Fair Wage Range                                      │
│  • Retention Impact                                     │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│ Integration Layer                                       │
│  • Transform metrics to 10C adjustments                  │
│  • Calculate combined job design score                  │
│  • Map to HR decision probability                       │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│ Phase 6 HR Decision (Updated)                           │
│  • Base probability: 84%                                │
│  • Job design adjustment: -2 to +2pp                    │
│  • Final probability: 82-86%                            │
└─────────────────────────────────────────────────────────┘
```

---

## Week 3 Tasks

### Task 1: Update HR Decision Function

**File:** `scripts/stakeholder_simulation/stakeholder_simulator.py`

**Current Function:**
```python
@staticmethod
def hr_hiring_decision(adjustments: NineCAdjustments) -> Tuple[float, Dict]:
    """HR hiring decision based on Phase 6 factors"""
    # Currently uses only 10C adjustments
    logit = (0.5 +
             1.25 * adjustments.WHERE_confidence +
             0.80 * (1 - adjustments.WHEN_context_risk) + ...)
    probability = DecisionFunctions._sigmoid(logit)
    return probability, drivers
```

**Updated Function (to add):**
```python
@staticmethod
def hr_hiring_with_job_design(adjustments: NineCAdjustments,
                              job_metrics: Dict = None) -> Tuple[float, Dict]:
    """HR hiring decision incorporating job design factors"""

    # Base 10C calculation
    base_logit = 0.5 + 1.25 * adjustments.WHERE_confidence + ...
    base_probability = DecisionFunctions._sigmoid(base_logit)

    # Job design adjustments (if provided)
    job_adjustment = 0
    if job_metrics:
        complexity = job_metrics.get('complexity_score', 2.5)
        automation = job_metrics.get('automation_risk', 50)
        engagement = job_metrics.get('engagement_score', 5)
        wage_fair = job_metrics.get('fairness_assessment', 'FAIR')

        # Complexity adjustment
        if complexity < 2.5:
            job_adjustment -= 0.02  # Low complexity → boredom risk
        elif complexity > 3.5:
            job_adjustment += 0.01  # Good complexity

        # Engagement adjustment
        if engagement < 5:
            job_adjustment -= 0.01
        elif engagement > 7:
            job_adjustment += 0.005

        # Automation adjustment
        if automation > 70:
            job_adjustment -= 0.01
        elif automation < 30:
            job_adjustment += 0.005

        # Wage fairness adjustment
        if wage_fair == "UNDERPAID":
            job_adjustment -= 0.005
        elif wage_fair == "OVERPAID":
            job_adjustment += 0.0025

    # Apply adjustment
    adjusted_probability = base_probability + job_adjustment
    adjusted_probability = max(0.5, min(0.95, adjusted_probability))

    return adjusted_probability, {
        'base_probability': base_probability,
        'job_design_adjustment': job_adjustment,
        'adjusted_probability': adjusted_probability,
        'complexity_score': complexity if job_metrics else None,
        'automation_risk': automation if job_metrics else None,
    }
```

**Steps:**
1. Add new function `hr_hiring_with_job_design()` to DecisionFunctions class
2. Update stakeholder_simulator.py to accept optional job_metrics parameter
3. Update simulate_stakeholder_cli.py to pass job metrics when available
4. Create integration tests

---

### Task 2: Expand Job Library

**Current State:** 1 profile (ALPLA Machine Operator)

**Planned Additions (Week 3):**

#### 2.1: Data Scientist Role
- **Company:** Tech company (generic)
- **Location:** Remote
- **Wage:** €35-45/hr
- **Tasks (6):**
  1. Data exploration & cleaning (25%)
  2. Statistical analysis (20%)
  3. Model development (20%)
  4. Dashboard/visualization (10%)
  5. Stakeholder presentations (15%)
  6. Tool & framework management (10%)
- **Expected Results:**
  - Complexity: 4.5/5 (HIGHLY_COMPLEX)
  - Automation Risk: 25% (LOW - cognitive, non-routine)
  - Engagement: 8.5/10 (EXCELLENT)

#### 2.2: Regional P&L Manager
- **Company:** Manufacturing
- **Location:** Regional office
- **Wage:** €60-75/hr
- **Tasks (7):**
  1. Budget planning & management (15%)
  2. Team leadership (20%)
  3. Strategic planning (15%)
  4. Financial analysis (20%)
  5. Supply chain oversight (15%)
  6. Personnel decisions (10%)
  7. External relations (5%)
- **Expected Results:**
  - Complexity: 4.8/5 (HIGHLY_COMPLEX)
  - Automation Risk: 10% (VERY LOW)
  - Engagement: 9.0/10 (EXCELLENT)

#### 2.3: Customer Service Representative
- **Company:** Service center
- **Location:** On-site
- **Wage:** €14-16/hr
- **Tasks (5):**
  1. Customer interaction (40%)
  2. Issue resolution (30%)
  3. Documentation (20%)
  4. Escalation management (5%)
  5. Process improvement (5%)
- **Expected Results:**
  - Complexity: 2.5/5 (SIMPLE-ROUTINE)
  - Automation Risk: 35% (MODERATE)
  - Engagement: 6.0/10 (GOOD)

#### 2.4: Software Engineer
- **Company:** Tech company
- **Location:** Remote
- **Wage:** €50-70/hr
- **Tasks (6):**
  1. Code development (40%)
  2. Code review & testing (20%)
  3. Architecture design (15%)
  4. Technical documentation (15%)
  5. Debugging & optimization (5%)
  6. Mentoring (5%)
- **Expected Results:**
  - Complexity: 4.7/5 (HIGHLY_COMPLEX)
  - Automation Risk: 15% (LOW)
  - Engagement: 8.8/10 (EXCELLENT)

#### 2.5: Manufacturing Line Manager
- **Company:** Manufacturing (ALPLA-like)
- **Location:** Production floor
- **Wage:** €22-28/hr
- **Tasks (7):**
  1. Team coordination (25%)
  2. Quality control (15%)
  3. Production scheduling (20%)
  4. Safety & compliance (15%)
  5. Equipment maintenance oversight (10%)
  6. Personnel management (10%)
  7. Continuous improvement (5%)
- **Expected Results:**
  - Complexity: 3.5/5 (ROUTINE_COGNITIVE + NON-ROUTINE)
  - Automation Risk: 30% (MODERATE)
  - Engagement: 7.5/10 (GOOD-EXCELLENT)

**Implementation:**
1. Create job profiles in `scripts/evaluate_job.py` JOB_LIBRARY
2. Define task details for each role
3. Test all 5 profiles
4. Create comparative analysis

---

### Task 3: Integration Testing

**Test Suite:**

#### Test 3.1: HR Decision with Job Metrics
```python
def test_hr_hiring_with_job_design():
    """Test HR decision function with job design metrics"""

    # Setup
    adjustments = NineCAdjustments(...)
    job_metrics_alpla = {
        'complexity_score': 2.12,
        'automation_risk': 59.6,
        'engagement_score': 5.7,
        'fairness_assessment': 'FAIR'
    }

    # Execute
    prob_without = simulator.hr_hiring_decision(adjustments)  # 84%
    prob_with = simulator.hr_hiring_with_job_design(adjustments, job_metrics_alpla)  # 82%

    # Verify
    assert prob_without > prob_with  # Low complexity should reduce approval
    assert abs(prob_with - 0.82) < 0.02  # Should be ~82%
```

#### Test 3.2: Comparative Job Analysis
```python
def test_job_design_comparisons():
    """Compare job designs across roles"""

    jobs = [
        ("ALPLA", "Machine Operator"),       # 2.12/5, 59.6%, 5.7/10
        ("TechCorp", "Data Scientist"),      # 4.5/5, 25%, 8.5/10
        ("ManufCorp", "P&L Manager"),        # 4.8/5, 10%, 9.0/10
        ("ServiceCorp", "Customer Service"), # 2.5/5, 35%, 6.0/10
        ("TechCorp", "Software Engineer"),   # 4.7/5, 15%, 8.8/10
    ]

    # Analyze all jobs
    for company, job in jobs:
        analysis = analyzer.generate_report()

        # Verify expected ranges
        assert analysis['complexity_analysis']['overall_complexity_score'] > 0
        assert 0 <= analysis['automation_risk']['overall_automation_risk_pct'] <= 100
        assert 0 <= analysis['engagement_analysis']['overall_engagement_score'] <= 10
```

#### Test 3.3: HR Decision Across Job Types
```python
def test_hr_hiring_probability_by_job_type():
    """HR approval probability varies by job design"""

    adjustments = NineCAdjustments(...)

    # High-complexity job should get better HR approval
    data_scientist_metrics = {'complexity_score': 4.5, 'automation_risk': 25, ...}
    prob_ds = simulator.hr_hiring_with_job_design(adjustments, data_scientist_metrics)

    # Low-complexity job should get worse HR approval
    machine_op_metrics = {'complexity_score': 2.12, 'automation_risk': 59.6, ...}
    prob_mo = simulator.hr_hiring_with_job_design(adjustments, machine_op_metrics)

    # Verify difference
    assert prob_ds > prob_mo
```

#### Test 3.4: Scenario Analysis
```python
def test_job_design_scenario_impact():
    """What if we improve job complexity?"""

    # Current state
    current = JobAnalyzer(current_job_profile)
    current_report = current.generate_report()

    # Improved state (complexity 2.12 → 3.5)
    improved_job = modify_job_profile(increase_complexity_to=3.5)
    improved = JobAnalyzer(improved_job)
    improved_report = improved.generate_report()

    # Verify improvement
    assert improved_report['complexity'] > current_report['complexity']
    assert improved_report['engagement'] > current_report['engagement']

    # Check HR impact
    current_hr_prob = simulator.hr_hiring_with_job_design(..., current_report)
    improved_hr_prob = simulator.hr_hiring_with_job_design(..., improved_report)

    assert improved_hr_prob > current_hr_prob
```

---

### Task 4: Scenario Analysis

**Scenarios to Create:**

#### Scenario 4.1: Upskilling
- **Question:** What if we train ALPLA operators to 3.5 complexity?
- **Changes:** Add advanced troubleshooting (15% time), reduce routine manual
- **Expected Impact:** Engagement 5.7 → 7.5, HR approval 82% → 84%

#### Scenario 4.2: Partial Automation
- **Question:** What if we automate the 95% automation risk tasks?
- **Changes:** Remove Task 1a (feed material), adjust time allocation
- **Expected Impact:** Automation risk 59.6% → 35%, retention improves

#### Scenario 4.3: Wage Adjustment
- **Question:** What if we increase ALPLA operator wage to €15/hr?
- **Changes:** Current wage €13 → €15
- **Expected Impact:** Fairness improves, HR approval +0.5pp

#### Scenario 4.4: Job Expansion (Horizontal)
- **Question:** Add new responsibilities (cross-training, mentoring)?
- **Changes:** Add mentoring (5%), quality review (5%), reduce routine
- **Expected Impact:** Variety increases, engagement improves

#### Scenario 4.5: Integrated Improvement Plan
- **Question:** Combined: upskill + wage adjust + cross-training?
- **Changes:** All of above
- **Expected Impact:** Comprehensive job redesign, HR approval ~87%

**Implementation:**
1. Create scenario functions in job_analyzer.py
2. Add scenario library (scenarios_job_design.py)
3. Create scenario comparison CLI
4. Generate visual comparisons (before/after)

---

## Implementation Sequence

### Phase 3a: HR Decision Update (2-3 hours)
1. Add `hr_hiring_with_job_design()` function
2. Update simulator to accept job_metrics
3. Update CLI to pass job metrics
4. Create integration tests (4 tests above)

### Phase 3b: Job Library Expansion (3-4 hours)
1. Create Data Scientist profile (30 min)
2. Create P&L Manager profile (30 min)
3. Create Customer Service profile (30 min)
4. Create Software Engineer profile (30 min)
5. Create Manufacturing Line Manager profile (30 min)
6. Test all 5 profiles (30 min)
7. Create comparative analysis (30 min)

### Phase 3c: Scenario Analysis (2-3 hours)
1. Create scenario functions (1 hour)
2. Create scenario library (30 min)
3. Create scenario CLI (30 min)
4. Test all 5 scenarios (1 hour)

### Phase 3d: Integration Testing (1-2 hours)
1. Write comprehensive test suite
2. Test HR decisions across all job types
3. Test scenario impacts
4. Validate data integrity

### Phase 3e: Documentation (1-2 hours)
1. Update README for new job profiles
2. Document scenario analysis
3. Create Week 3 completion summary
4. Update project status

**Total Estimated Time:** 9-14 hours
**Deliverables:** 8-10 files, 1,200-1,500 lines of code

---

## Success Criteria

- ✓ HR decision function updated and tested
- ✓ 5 job profiles added (Data Scientist, P&L Manager, Customer Service, Engineer, Line Manager)
- ✓ All job profiles analyzed and documented
- ✓ 5 scenarios created and tested
- ✓ Integration tests passing (100%)
- ✓ Comparative analysis working
- ✓ HR approval probability varies by job design
- ✓ Code committed and pushed
- ✓ Week 3 completion summary created

---

## Deliverables Summary

### Code Files
1. `scripts/stakeholder_simulation/stakeholder_simulator.py` (Updated)
2. `scripts/job_analysis/job_analyzer.py` (Updated with scenarios)
3. `scripts/evaluate_job.py` (Updated with 5 profiles)
4. `scripts/scenarios_job_design.py` (New - scenario library)
5. `scripts/job_design_scenario_cli.py` (New - scenario CLI)

### Test Files
1. `tests/test_job_design_integration.py` (New - 4+ tests)

### Documentation
1. `docs/PHASE-6.5-WEEK-3-INTEGRATION-SUMMARY.md` (New)
2. `docs/JOB-DESIGN-PROFILES.md` (New - all 5 profiles)
3. `docs/JOB-DESIGN-SCENARIOS.md` (New - scenario analysis)

---

## Next Phase (Week 4+)

After Week 3 Integration is complete:
- Extended profile library (10+ job types)
- Sensitivity analysis: Which parameters drive outcomes most?
- Historical validation: Compare model predictions with actual outcomes
- Phase 7 foundation: Strategic recommendations engine

---

**Estimated Completion:** End of session (3-4 hours of work)
**Status:** Ready to begin Phase 3a
