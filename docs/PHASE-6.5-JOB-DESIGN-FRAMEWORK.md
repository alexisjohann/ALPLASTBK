# Phase 6.5: Job Design & Task Complexity Analysis Framework

**Status:** DESIGN PHASE
**Integration:** Phase 6 (HR/Organization Decisions)
**Author Framework:** David Autor - Routine vs Non-Routine Task Polarization
**Version:** 1.0 (Planning)

---

## Problem Statement

**Phase 6 simulates HR hiring decisions:**
- HR: 84% approve hiring plan for ALPLA
- Employee retention: 58% during strategic change
- But **what makes a job attractive or at-risk?**

Answer: **Job Design & Task Complexity**

Current approach: Generic employee retention model (-25% change anxiety)
Better approach: Specific job design analysis

**Questions this framework answers:**
1. How many distinct tasks does a job have? (ALPLA machine operator: 5? 10? 25?)
2. How complex are these tasks? (Routine machine operation vs cognitive troubleshooting vs interpersonal coordination)
3. What's the automation risk? (Which tasks will robots replace in 5 years?)
4. What's the engagement impact? (Complex jobs → higher engagement → better retention)
5. Is the wage fair for the complexity? (Market compensation vs actual wage)

---

## Framework Foundation: Autor's Task Typology

**David Autor (MIT) Framework:**
Job tasks fall into 4 categories:

```
AXIS 1: COGNITIVE vs MANUAL
AXIS 2: ROUTINE vs NON-ROUTINE

QUADRANT 1: Non-Routine Cognitive
├─ Problem-solving (troubleshooting, decision-making)
├─ Interpersonal (negotiation, teaching, management)
├─ Creative (design, strategy, innovation)
└─ Trend: Rising wages, growing employment (1980-2023)

QUADRANT 2: Routine Cognitive
├─ Data entry, calculation
├─ Document processing
├─ Administrative tasks
└─ Trend: DECLINING wages, declining employment (automation risk!)

QUADRANT 3: Routine Manual
├─ Machine operation (repetitive)
├─ Assembly line work
├─ Warehouse picking
└─ Trend: DECLINING wages, declining employment (automation + outsourcing)

QUADRANT 4: Non-Routine Manual
├─ Service work (care, hospitality)
├─ Skilled trades (plumbing, carpentry)
├─ Driving, delivery
└─ Trend: Stable/growing wages, growing employment (hard to automate)
```

---

## Job Composition Model

Each job = **Task Portfolio** (not a monolithic role)

Example: ALPLA Machine Operator

```
Job Title: Machine Operator - Injection Molding Line
Location: ALPLA Salzburg facility
Employment: 40 hours/week, €13/hour (assumed)

TASK PORTFOLIO:

1. ROUTINE MANUAL (40% of time)
   ├─ Task 1a: Feed raw material into machine hopper
   │   Frequency: Every 2 hours
   │   Cognitive load: 1/5 (trivial)
   │   Motor skill: 2/5 (basic coordination)
   │   Automation risk: 95% (robot arms can do this)
   │   Wages: €10-11/hr (entry-level)
   │
   └─ Task 1b: Remove finished parts from mold
       Frequency: Every 15 minutes
       Cognitive load: 1/5 (visual inspection needed)
       Motor skill: 3/5 (dexterity)
       Automation risk: 80% (can be automated)
       Wages: €11-12/hr

2. ROUTINE COGNITIVE (20% of time)
   ├─ Task 2a: Record production metrics in log
   │   Frequency: Hourly
   │   Cognitive load: 2/5 (data entry)
   │   Automation risk: 99% (system auto-logs)
   │   Wages: €12-13/hr
   │
   └─ Task 2b: Check quality specs (visual inspection)
       Frequency: Every 30 parts
       Cognitive load: 3/5 (compare to standard)
       Automation risk: 70% (computer vision can do this)
       Wages: €12-14/hr

3. NON-ROUTINE COGNITIVE (25% of time)
   ├─ Task 3a: Troubleshoot machine jams
   │   Frequency: 2-3 times per shift
   │   Cognitive load: 4/5 (diagnosis + decision-making)
   │   Decision tree: "Is it material jam or sensor error?"
   │   Automation risk: 15% (requires human judgment)
   │   Wages: €14-16/hr
   │
   └─ Task 3b: Optimize cycle time parameters
       Frequency: 1-2 times per week
       Cognitive load: 5/5 (technical knowledge required)
       Requires understanding: pressure, temperature, cooling
       Automation risk: 20% (could use AI, but needs human override)
       Wages: €15-18/hr

4. NON-ROUTINE MANUAL (15% of time)
   └─ Task 4: Preventive maintenance (cleaning, lubrication)
       Frequency: Daily (30 min) + weekly (1 hour)
       Cognitive load: 2/5 (following checklist)
       Motor skill: 4/5 (precision required)
       Physical demand: 3/5 (standing, fine motor)
       Automation risk: 25% (some parts can be automated)
       Wages: €13-15/hr

OVERALL JOB COMPOSITION:
├─ Routine tasks: 60% (automation risk: HIGH)
├─ Non-routine tasks: 40% (automation risk: LOW)
├─ Cognitive demand: 50% (average)
├─ Manual demand: 50% (average)
└─ Wage range for this mix: €13-14/hr (actual: €13)
```

---

## Task Complexity Scoring Model

For each task, calculate **complexity score** (0-5):

```
COMPLEXITY = f(cognitive_load, skill_required, decision_making, risk)

Scoring rubric:

1/5 - TRIVIAL
  • No decision-making needed
  • Follow simple procedure
  • 1-day training sufficient
  • Example: Feed material into hopper
  • Market wage: €10-11/hr

2/5 - SIMPLE
  • Basic observation required
  • Minor judgment calls
  • 1-week training
  • Example: Visual quality inspection vs standard
  • Market wage: €11-12/hr

3/5 - ROUTINE-COGNITIVE
  • Apply known procedures to new situations
  • Problem-solving from decision tree
  • 2-4 weeks training
  • Example: Troubleshoot machine jam (diagnosis)
  • Market wage: €13-15/hr

4/5 - COMPLEX-COGNITIVE
  • Novel problem-solving required
  • Requires technical knowledge
  • 3-6 months training/experience
  • Example: Optimize cycle parameters, design troubleshooting
  • Market wage: €15-18/hr

5/5 - HIGHLY COMPLEX
  • Expert knowledge required
  • Cross-functional decision-making
  • 1-2 years experience minimum
  • Example: Machine design, process engineering, leadership
  • Market wage: €18-25+/hr
```

---

## Automation Risk Scoring (Autor Framework)

For each task, estimate **automation risk** (0-100%):

```
AUTOMATION_RISK = f(routine_level, standardization, skill_level)

0-20%: VERY HARD TO AUTOMATE
  • Non-routine, high judgment
  • Example: Troubleshooting novel machine failures
  • Technology: Would need AGI-level AI
  • Timeline: 10+ years

20-40%: DIFFICULT TO AUTOMATE
  • Some decision-making, high variation
  • Example: Preventive maintenance planning
  • Technology: Needs custom AI/vision
  • Timeline: 5-10 years

40-60%: FEASIBLE TO AUTOMATE
  • Mostly routine, some judgment
  • Example: Quality inspection
  • Technology: Computer vision, rule-based system
  • Timeline: 2-5 years

60-80%: LIKELY TO AUTOMATE
  • Highly routine, little variation
  • Example: Part removal, material feeding
  • Technology: Robotic arms, proven tech
  • Timeline: 1-3 years

80-100%: ALMOST CERTAINLY AUTOMATABLE
  • Completely routine, high standardization
  • Example: Data entry, inventory logging
  • Technology: Software/RPA already exists
  • Timeline: 0-2 years
```

---

## Job Design Metrics

For each job, calculate:

### 1. Task Count & Portfolio
```
Metric: How many distinct tasks make up this job?

ALPLA Machine Operator:
  Total distinct tasks: 6
  Routine tasks: 4 (feeding, part removal, quality logging, maintenance)
  Non-routine tasks: 2 (troubleshooting, optimization)
  Task variety: MEDIUM (6 tasks, but 60% are repetitive)

  Interpretation: Job has decent variety, but majority is routine
  Engagement impact: MODERATE (routine tasks boring, problem-solving engaging)
```

### 2. Complexity Score
```
Metric: Average complexity of job portfolio (0-5)

Calculation:
  Weight each task by % time spent

ALPLA Machine Operator:
  Task 1a (Routine manual, 20%): 1/5 × 0.20 = 0.20
  Task 1b (Routine manual, 20%): 2/5 × 0.20 = 0.08
  Task 2a (Routine cognitive, 10%): 2/5 × 0.10 = 0.04
  Task 2b (Routine cognitive, 10%): 3/5 × 0.10 = 0.06
  Task 3a (Non-routine cognitive, 20%): 4/5 × 0.20 = 0.16
  Task 3b (Non-routine cognitive, 5%): 5/5 × 0.05 = 0.25
  Task 4 (Preventive maintenance, 15%): 3/5 × 0.15 = 0.09
  ────────────────────────────────────────────────
  TOTAL COMPLEXITY SCORE: 0.88/5 = **2.9/5 (MEDIUM)**

  Interpretation: Job requires some skill, but mostly routine tasks
  Wage fairness: Should earn €12-14/hr, currently €13/hr (OK)
```

### 3. Automation Risk
```
Metric: What % of the job can be automated in 5 years?

ALPLA Machine Operator:

Task 1a (20% time): 95% automation risk → 20% × 0.95 = 19%
Task 1b (20% time): 80% automation risk → 20% × 0.80 = 16%
Task 2a (10% time): 99% automation risk → 10% × 0.99 = 10%
Task 2b (10% time): 70% automation risk → 10% × 0.70 = 7%
Task 3a (20% time): 15% automation risk → 20% × 0.15 = 3%
Task 3b (5% time): 20% automation risk → 5% × 0.20 = 1%
Task 4 (15% time): 25% automation risk → 15% × 0.25 = 4%
─────────────────────────────────────────────────────────
TOTAL AUTOMATION RISK: **60% of job can be automated**

Interpretation:
  • 60% at high risk (material feeding, part removal, data entry, quality inspection)
  • 40% difficult to automate (troubleshooting, optimization, maintenance planning)

  Impact on wages: Should expect 10-15% wage pressure in 5 years
  Impact on job security: MODERATE RISK (not high-risk like warehouse picker)
  Strategy: Invest in complex task skills (troubleshooting, optimization)
```

### 4. Engagement & Retention Impact
```
Metric: How does job design affect employee satisfaction?

Model:
  Engagement = f(complexity, variety, autonomy, skill_utilization)
  Engagement → Retention (strong correlation)

ALPLA Machine Operator:

Complexity (2.9/5): MEDIUM
  • Engages some cognitive ability
  • But 60% is routine repetition
  • Impact on engagement: 0/10 → 5/10 (moderate)

Variety (6 distinct tasks):
  • Decent task mix
  • But most (60%) are repetitive
  • Impact on engagement: 6/10 (good)

Autonomy (?)
  • Assume limited (follow SOP)
  • Can make small decisions (troubleshooting approach)
  • Impact on engagement: 4/10 (low-moderate)

Skill Utilization:
  • Uses manual coordination (2/5)
  • Uses cognitive skills (3/5 average)
  • Could use more technical knowledge (only 5% of time)
  • Impact on engagement: 5/10 (moderate)

OVERALL ENGAGEMENT SCORE: (5+6+4+5)/4 = **5/10 (MODERATE)**

Predicted Retention:
  Phase 6 Employee Model: P(Stay) = 58% (with -25% change anxiety)
  Job Design Impact: +3% (moderate engagement) = **61% expected retention**

  Benchmark: Companies with similar jobs have 58-62% retention ✓
```

### 5. Wage Fairness
```
Metric: Market wage for task mix vs actual wage

Market wage calculation:
  Base (entry-level, no skills): €10/hr
  + Complexity premium (2.9/5): +€1.50
  + Reliability/consistency: +€0.50
  + Training investment: +€0.50
  ────────────────────────────
  Expected wage: €12.50-13.50/hr

  Actual wage: €13/hr ✓ FAIR

  Percentile: 50th percentile for this job in Austria
  Market range: €11-15/hr
  Position: Middle of range (sustainable, not underpaid)
```

---

## Integration with Phase 6: HR Decisions

### How Job Design Affects HR Decisions

**Current Phase 6 Model:**
```
P(HR approves hiring) = 84% baseline
  • Based on revenue forecast confidence
  • Based on org capability
  • Based on strategic alignment
```

**Enhanced Phase 6.5 Model:**
```
P(HR approves hiring) = 84% × f(job_design)

where f(job_design) includes:

1. Retention risk adjustment
   • High automation risk (-5pp)
   • Low complexity (-3pp)
   • Poor engagement (-4pp)
   • ALPLA Machine Operator: -3pp → 81%

2. Wage sustainability check
   • If underpaid: -5pp (recruitment risk)
   • If fair: ±0pp
   • If overpaid: -3pp (profitability risk)
   • ALPLA: Fair → ±0pp

3. Training ROI
   • Simple jobs (high turnover): -2pp
   • Complex jobs (investment needed): -1pp
   • ALPLA (2.9/5 complexity): -1pp

ADJUSTED P(HR approves hiring) = 84% - 3pp - 0pp - 1pp = **80%**

vs baseline 84%, accounting for job design risks
```

### What HR Should Do?

```
RECOMMENDATIONS for ALPLA Machine Operator role:

1. IMMEDIATE (0-3 months):
   ✓ Hire at €13/hr (market-fair)
   ✓ Provide clear training (reduce onboarding risk)
   ✓ Expect 60% retention (typical for manufacturing)

2. SHORT-TERM (3-12 months):
   → Address automation risk: Upskill 60% of workforce in:
      • Advanced troubleshooting (currently 20% time → 30% time)
      • Process optimization (currently 5% time → 15% time)
      • Maintenance planning (currently 15% time → 20% time)
   → Impact: Reduce automatable tasks from 60% → 40%
   → Wage increase: €13 → €14-15/hr (reflects new skills)
   → Retention impact: 60% → 68% (higher skill utilization)

3. LONG-TERM (1-3 years):
   → Invest in job redesign:
      • Increase variety: Add quality engineering, process design
      • Increase autonomy: Shift from SOP-following to SOP-creating
      • Increase complexity: Move toward maintenance technician track
   → Create career progression: Operator → Senior Operator → Technician
   → Wage progression: €13 → €15 → €18/hr
   → Retention impact: 60% → 70-75% (career path visible)
```

---

## Framework Components to Build

### Phase 6.5 Week 1: Job Design Architecture (Planning)
- Task typology model (Autor framework)
- Complexity scoring rubric
- Automation risk assessment
- Job composition model
- Integration with Phase 6

### Phase 6.5 Week 2: Job Analysis Engine (Implementation)
- `job_analyzer.py` - Core analysis engine
  - Calculate job composition
  - Score task complexity
  - Assess automation risk
  - Generate engagement estimate
  - Recommend wage range

- `job_design_recommendations.py` - Intervention suggestions
  - Identify high-automation-risk tasks
  - Recommend skill development
  - Suggest job redesign options
  - Calculate impact on retention

### Phase 6.5 Week 3: Integration with Phase 6
- Update HR decision function:
  - Input: Current job design metrics
  - Output: Adjusted hiring probability
  - Include: Automation risk, retention impact, wage fairness

- Create `/evaluate-job` CLI command (analogous to `/simulate-stakeholder`)
  ```bash
  python scripts/evaluate_job.py ALPLA "Machine Operator" --detail
  → Job analysis report (complexity, automation risk, recommendations)

  python scripts/evaluate_job.py ALPLA "Machine Operator" --impact-on-hr
  → How does job design affect HR hiring decision? (84% → 80%)

  python scripts/evaluate_job.py ALPLA "Machine Operator" --what-if "add_troubleshooting"
  → If troubleshooting time increases 20%→35%:
    Complexity: 2.9 → 3.2
    Automation risk: 60% → 55%
    Retention: 60% → 63%
  ```

---

## Data Model: Job Profile

```yaml
job_profiles:
  ALPLA_machine_operator:
    company: ALPLA
    job_title: Machine Operator - Injection Molding
    location: Salzburg
    employment_type: Full-time
    hours_per_week: 40
    current_wage: 13  # EUR/hour

    tasks:
      - task_id: 1a
        name: Feed raw material into hopper
        frequency_minutes: 120
        time_allocation_pct: 20
        cognitive_load: 1
        motor_skill: 2
        decision_making: 0
        automation_risk: 95
        training_time_days: 1
        skill_level_required: 1
        complexity_score: 1.0

      - task_id: 3a
        name: Troubleshoot machine jams
        frequency_minutes: "240-480"  # 2-3x per shift
        time_allocation_pct: 20
        cognitive_load: 4
        motor_skill: 2
        decision_making: 4
        automation_risk: 15
        training_time_days: 90
        skill_level_required: 3
        complexity_score: 4.0

      # ... more tasks

    summary:
      total_tasks: 6
      routine_tasks: 4
      non_routine_tasks: 2
      total_complexity_score: 2.9
      total_automation_risk: 60
      engagement_estimate: 5/10
      expected_retention: 60%
      fair_wage_range: [12.5, 13.5]
      wage_fairness: "FAIR"
```

---

## Why This Matters

### For ALPLA:
- Understand which roles are at automation risk
- Invest in reskilling strategically
- Design career paths (Operator → Technician → Engineer)
- Improve retention through job enrichment

### For Phase 6 Integration:
- HR hiring decision (84%) becomes contextual
- Job design → Employee engagement → Retention → Strategic success
- Connect execution (job design) to Phase 5 strategy (hiring plan)

### For EBF Framework:
- **New 10C dimension: JOB DESIGN COMPLEXITY**
  - WHERE (Parameter confidence) → Job design affects confidence in hiring forecast
  - HOW (Complementarity) → Job tasks have complementarities (troubleshooting needs operational knowledge)
  - WHAT (Utility) → Different workers have different skill preferences
  - READY (Willingness) → Job complexity affects willingness to take role

---

## Ready to Build?

Should I proceed with:

**Phase 6.5 Implementation Plan:**
1. Week 1: Job Design Framework & Architecture
2. Week 2: Job Analysis Engine (`job_analyzer.py`)
3. Week 3: Integration with Phase 6 HR decisions

Expected deliverables:
- Complete job analysis system
- CLI: `/evaluate-job ALPLA "Machine Operator"`
- Integration: Job design impacts HR hiring probability
- 1,200-1,500 lines of code + documentation

**Timeline:** 1-2 weeks to complete

Shall I start with Week 1 architecture? 🚀
