# Phase 6: Stakeholder Behavior Simulation

**Status:** Planning & Design
**Start Date:** 2026-01-16
**Objective:** Predict stakeholder decisions (buy/leave/advocate/partner) using 10C CORE framework + behavioral economics

---

## Vision

Transform strategic models from **internal forecasting tool** to **stakeholder influence system**:

```
Current (Phase 5):  ALPLA Model → Board sees €15B forecast
                                   "Should we approve €150M capex?"

Phase 6:           ALPLA Model → Board behavior simulation
                   + 12 Stakeholder models
                   + Awareness/Readiness mapping
                   + Change Journey tracking

                   Output: "82% board approval likelihood IF:"
                           "- Regional leaders briefed (AU) ✓"
                           "- CAGR confidence >80% (WHERE) ✓"
                           "- Phase gates clear (HIERARCHY) ✓"
```

---

## Architecture: 12 Stakeholder Models with 10C Profiles

### Layer 1: Stakeholder Taxonomy

| Tier | Stakeholder Type | Decision | Primary Metric | 10C Focus |
|------|------------------|----------|----------------|----------|
| **Strategic** | Board of Directors | Strategy Approval | Capex Authorization | HIERARCHY, WHERE, HOW |
| | C-Suite | Risk Mitigation | Board Recommendation | WHERE, WHEN |
| **Operational** | Regional P&L Leaders | Regional Expansion | CAGR Target Hit | WHERE, WHAT, HOW |
| | Business Unit Heads | Segment Strategy | Portfolio Rebalancing | WHAT, WHERE |
| | FP&A Team | Parameter Governance | Parameter Updates | WHERE, WHEN |
| **Analytical** | HR/Organization | Headcount Pace | Hiring Plan Approval | HOW, WHAT |
| | Capex Committee | Phase Gates | Project Sequencing | HIERARCHY, WHEN |
| | Data Analytics | Monitoring | Dashboard Alerts | WHERE, WHEN |
| | Data Science | Innovation | Archetype Discovery | HOW, WHERE |
| **External** | Customers | Purchase Decisions | Buying Probability | WHAT, WHERE |
| | Suppliers | Partnership | Long-term Commitment | HOW, WHEN |
| | Competitors | Market Response | Defensive Actions | WHEN, WHERE |

### Layer 2: Decision Types by Stakeholder

```
INTERNAL STAKEHOLDERS:
├─ Board: Approve strategy? (Yes/No/Conditional) → Capex release
├─ C-Suite: Escalate/Mitigate risk? → Monthly governance gate
├─ Regional Leaders: Hit CAGR? → Regional investment authorization
├─ Business Unit: Rebalance portfolio? → Budget reallocation
├─ FP&A: Accept parameter update? → Model governance approval
├─ HR: Approve hiring plan? → Headcount commitment
├─ Capex Committee: Gate Phase 1→2? → €150M release
├─ Analytics: Increase monitoring? → Alert threshold adjustment
└─ Data Science: Deploy archetype? → New customer seeding

EXTERNAL STAKEHOLDERS:
├─ Customers: Buy product? → Purchase decision
├─ Suppliers: Commit partnership? → Volume commitment
└─ Competitors: Respond to moves? → Competitive reaction
```

### Layer 3: 10C Profiles for Each Stakeholder

**Example: Board of Directors**

| 10C Dimension | Parameter | Formula | Behavioral Input |
|--------------|-----------|---------|------------------|
| **WHO** | Welfare Level L | Board = L3 (strategic) | Top-level utility |
| **WHAT** | Utility Weights (ω_d) | F=0.70, D=0.15, S=0.10, E=0.05 | Financial + social responsibility |
| **HOW** | Complementarities (γ) | γ_capex-revenue=0.62, γ_org-capability=0.48 | Phasing + coordination |
| **WHEN** | Context Sensitivity (Ψ) | Ψ₁(Econ), Ψ₆(Inst), Ψ₈(Regulatory) | Market + governance risk |
| **WHERE** | Parameter Uncertainty (E(θ)) | E(θ) budget = ±€5M, E(θ) CAGR = ±0.8pp | Data quality for approval |
| **AWARE** | Awareness (AU) | Fully briefed? (0-100%) | Understanding of strategy |
| **READY** | Willingness (AV, θ) | Can commit? (Capability score) | Vote likelihood |
| **STAGE** | Change Journey (φ) | Awareness → Consideration → Decision | Where in BCJ? |
| **HIERARCHY** | Decision Stratification (N_L2) | Requires alignment with: L1 (CEO), L2 (CFO/CRO) | Approval dependencies |

---

## Phase 6 Implementation Roadmap

### Phase 6a: Framework & Models (Week 1-2)

**Deliverables:**
1. **stakeholder-behavior-framework.md** (800+ lines)
   - 12 stakeholder models with 10C profiles
   - Decision functions for each (logit models)
   - Awareness/Readiness mapping (AU/AV framework)
   - Change Journey templates (8 stages)
   - Red flags & escalation rules

2. **Data Structure: Stakeholder Models Registry**
   ```yaml
   data/stakeholder-models/
   ├── board_model.yaml
   ├── regional_pl_model.yaml
   ├── customer_model.yaml
   ├── supplier_model.yaml
   ├── employee_model.yaml
   ├── competitor_model.yaml
   ├── fpa_model.yaml
   ├── capex_committee_model.yaml
   ├── investor_model.yaml
   ├── lender_model.yaml
   ├── regulator_model.yaml
   └── media_model.yaml
   ```

3. **Stakeholder Profiles Database**
   ```
   data/stakeholders/
   ├── <customer_name>/
   │   ├── board_profile.json
   │   ├── customer_segments_profiles.json
   │   ├── employee_cohorts_profiles.json
   │   ├── supplier_partnerships_profiles.json
   │   └── competitor_responses_profiles.json
   ```

### Phase 6b: Simulation Skills (Week 2-3)

**New Skill: `/simulate-stakeholder`**

Usage:
```bash
# Single stakeholder simulation
/simulate-stakeholder ALPLA board strategy_approval
/simulate-stakeholder ALPLA customer purchase_decision
/simulate-stakeholder ALPLA employee retention

# Full stakeholder matrix
/simulate-stakeholder ALPLA all
/simulate-stakeholder ALPLA --detailed

# Scenario: what-if analysis
/simulate-stakeholder ALPLA --scenario "price_increase_10pct"
/simulate-stakeholder ALPLA --scenario "capex_delay_6months"
```

**Output for Each Simulation:**
```json
{
  "stakeholder_type": "board",
  "decision": "strategy_approval",
  "approval_probability": 0.82,
  "confidence_level": "HIGH",
  "key_drivers": {
    "WHERE": "CAGR confidence ±0.8pp (82% confident) ✓",
    "WHEN": "GDP assumption 2.8% (quarterly monitoring) ✓",
    "HOW": "Org capability proven (γ_rev-org=0.68) ✓",
    "WHAT": "Portfolio alignment F=70% (strategic fit) ✓"
  },
  "awareness_readiness": {
    "awareness_score": 95,
    "readiness_score": 87,
    "journey_stage": "decision"
  },
  "change_journey": {
    "stage": 3,  // Decision
    "progress": 87,
    "timeline_to_action": "1-2 weeks"
  },
  "red_flags": [],
  "conditions_for_approval": [
    "HIERARCHY: Board gate at right timing ✓",
    "WHERE: Parameter confidence >80% ✓"
  ],
  "risk_mitigation": [
    "Monthly capex tracking (HOW bottleneck)",
    "Quarterly GDP monitoring (WHEN risk)",
    "Board updates (HIERARCHY 180 L2 decisions)"
  ]
}
```

### Phase 6c: Behavior Models (Week 3-4)

**12 Specific Models with Decision Functions**

#### 1. **Board of Directors**
- Decision: Strategy Approval (Capex Release)
- Function: P(Approve) = f(WHERE confidence, WHEN economic risk, HOW org capability, HIERARCHY gates)
- Threshold: ≥75% approval probability needed
- Timeline: 2-week board meeting cycle

#### 2. **C-Suite (CEO/CFO)**
- Decision: Risk Mitigation Actions
- Function: P(Escalate) = f(ΔP forecast miss, E(θ) shrinkage rate, WHEN context shocks)
- Threshold: Monthly governance gates if P > 60%

#### 3. **Regional P&L Leaders**
- Decision: Hit CAGR Target
- Function: P(Hit Target) = f(WHERE CAGR confidence, HOW complementarity with HQ initiatives, WHAT regional utility)
- Monthly tracking: ΔP vs forecast; escalate if > ±5%

#### 4. **Business Unit Heads**
- Decision: Portfolio Rebalancing
- Function: P(Rebalance) = f(WHAT segment utility weights, WHERE segment parameter uncertainty)
- Quarterly decision at model governance meeting

#### 5. **FP&A Team**
- Decision: Accept Parameter Update
- Function: P(Accept) = f(WHERE shrinkage magnitude, WHEN regime change detection)
- Rule: Accept if shrinkage >15% AND confidence level increases

#### 6. **HR/Organization**
- Decision: Approve Hiring Plan
- Function: P(Approve) = f(HOW complementarity γ_rev-org, revenue forecast confidence, payroll elasticity)
- Quarterly: Aligned with revenue forecast cycle

#### 7. **Capex Committee**
- Decision: Phase Gate (Go/No-Go)
- Function: P(Go) = f(HIERARCHY execution risk, WHEN capex governance lag Ψ₆, HOW org implementation capacity)
- Gates: Q4 2026 (Phase 1→2), Q4 2029 (Phase 2→3)

#### 8. **Data Analytics/BI**
- Decision: Increase Monitoring
- Function: P(Increase) = f(WHERE parameter drift, WHEN context shocks, risk volatility)
- Triggered: If E(θ) growing OR ΔP > ±5%

#### 9. **Data Science**
- Decision: Deploy Archetype
- Function: P(Deploy) = f(3+ projects completed, archetype homogeneity > 0.8, speed-up potential > 20%)
- Timeline: Month 9-12 of program

#### 10. **Customers**
- Decision: Purchase/Renew
- Function: P(Buy) = f(WHAT customer priorities matched, WHERE confidence in benefit, HOW integration ease)
- Behavioral: Loss aversion, reference point (current supplier), switching costs

#### 11. **Suppliers**
- Decision: Long-term Partnership Commitment
- Function: P(Commit) = f(HOW volume synergy, WHEN demand stability Ψ, WHERE revenue predictability)
- Timeline: 3-5 year contracts

#### 12. **Competitors**
- Decision: Market Response (Match/Undercut/Innovate)
- Function: P(Response) = f(WHEN market move speed Ψ₇, WHERE competitive intelligence E(θ_comp), HOW capability to respond)
- Speed: 1-6 month response lag

---

## Decision Functions: Detailed Examples

### Example 1: Board Approval Decision

```
P(Board Approves | Strategy) = f(
    WHERE_confidence × w1 +
    WHEN_economic_risk × w2 +
    HOW_org_capability × w3 +
    HIERARCHY_clarity × w4 +
    AWARE_briefing × w5 +
    READY_vote_likelihood × w6
)

Weights (learned from similar strategic approvals):
  w1 (WHERE) = 0.25
  w2 (WHEN) = 0.20
  w3 (HOW) = 0.20
  w4 (HIERARCHY) = 0.15
  w5 (AWARE) = 0.10
  w6 (READY) = 0.10

ALPLA Case:
  WHERE_confidence = 0.82 (CAGR ±0.8pp) ✓
  WHEN_risk = 0.25 (GDP 2.8%, conservative) ✓
  HOW_capability = 0.85 (γ_rev-org=0.68, proven) ✓
  HIERARCHY_clarity = 0.90 (Phase gates defined) ✓
  AWARE_briefing = 0.95 (Full board briefing done) ✓
  READY_vote = 0.88 (Internal poll shows 8/10 votes)

P(Approve) = 0.82×0.25 + 0.75×0.20 + 0.85×0.20 + 0.90×0.15 + 0.95×0.10 + 0.88×0.10
          = 0.205 + 0.150 + 0.170 + 0.135 + 0.095 + 0.088
          = 0.843 (84.3% approval probability)

Interpretation:
  ✓ HIGH confidence for board approval
  ✓ Go ahead with presentation
  ✓ Monitor: WHEN (economic assumption) most fragile
```

### Example 2: Customer Purchase Decision

```
P(Customer Buys | Offer) = f(
    WHAT_match × w1 +
    WHERE_confidence × w2 +
    HOW_integration_ease × w3 +
    AWARE_solution_knowledge × w4 +
    READY_decision_authority × w5 -
    loss_aversion_penalty × w6
)

Behavioral Adjustments:
  - Loss aversion: -30% penalty if switching from current supplier
  - Reference point: Current supplier = status quo baseline
  - Sunk costs: Already invested in current solution
  - Status quo bias: Switching must show >20% improvement

Example: Pharma customer considering supplier switch
  WHAT_match = 0.75 (solution meets 75% of requirements)
  WHERE_confidence = 0.70 (Product reliability proven ±15%)
  HOW_integration_ease = 0.65 (Integration complex, 6-month effort)
  AWARE_solution = 0.80 (CTO well briefed)
  READY_authority = 0.60 (Requires CFO sign-off)
  loss_aversion = -0.30 (Switching penalty)

P(Buy) = 0.75×0.30 + 0.70×0.25 + 0.65×0.20 + 0.80×0.15 + 0.60×0.10 - 0.30
       = 0.225 + 0.175 + 0.130 + 0.120 + 0.060 - 0.30
       = 0.410 (41% purchase probability)

Interpretation:
  ⚠ MODERATE-LOW purchase probability
  → Actions:
    1. Reduce loss aversion: Offer 6-month trial (reversible)
    2. Improve WHAT match: Customize solution for Pharma workflow
    3. Enhance WHERE confidence: Case studies, references
    4. Ease HOW integration: Provide integration team (reduce 6m→3m)
```

---

## Awareness & Readiness Mapping (AU/AV Framework)

### Awareness Levels (AU: 0-100%)

```
0-20%:   Unaware
         "Have they even heard of the strategy?"
         → Action: Marketing/communication campaign

20-50%:  Partially Aware
         "Do they understand the basics?"
         → Action: Education/training

50-80%:  Well Informed
         "Do they grasp implications?"
         → Action: Engagement/feedback

80-100%: Fully Briefed
         "Ready to make decisions?"
         → Ready to move to Readiness assessment
```

### Readiness Levels (AV: Capability θ_read × Willingness θ_will)

```
Readiness = θ_capability × θ_willingness

θ_capability: Can they act?
  - Resources available? (budget, time, people)
  - Skills present? (technical, organizational)
  - Authority present? (decision rights)
  - E.g., Board = 0.90 (full resources), Regional Leader = 0.75 (some constraints)

θ_willingness: Do they want to?
  - Aligned with incentives? (bonus structure, career advancement)
  - Risk averse? (loss aversion, status quo bias)
  - Social preferences? (fairness, reciprocity)
  - E.g., Board = 0.85 (reputation at stake), Employee = 0.60 (change anxiety)

Examples:
  Board:        θ_cap=0.90 × θ_will=0.85 = 0.765 (77% ready)
  Customer:     θ_cap=0.60 × θ_will=0.70 = 0.420 (42% ready)
  Employee:     θ_cap=0.70 × θ_will=0.55 = 0.385 (39% ready)
```

---

## Change Journey Mapping (8 Stages)

```
STAGE 1: AWARENESS (Status Quo Mental Model)
├─ Question: Do they know change is coming?
├─ Stakeholder Action: "Have heard of strategy, but unclear implications"
├─ Decision Gate: AU ≥ 20% (basic awareness)
└─ Timeline: 1-2 weeks before communication

STAGE 2: UNDERSTANDING (Learn About Change)
├─ Question: Do they grasp the what/why/how?
├─ Stakeholder Action: "Attended briefing, read materials"
├─ Decision Gate: AU ≥ 50% (understands implications)
├─ Blockers: Complexity, jargon, competing information
└─ Timeline: 2-4 weeks (ongoing learning)

STAGE 3: CONSIDERATION (Evaluate Options)
├─ Question: Does this align with my interests/utility?
├─ Stakeholder Action: "Comparing: current state vs proposed change"
├─ Decision Gate: WHAT alignment ≥ 0.65 (strategic fit)
├─ Blockers: Loss aversion, switching costs, risk perception
└─ Timeline: 1-2 weeks (internal evaluation)

STAGE 4: ACCEPTANCE (Reduce Psychological Resistance)
├─ Question: Can I mentally accept this as inevitable/beneficial?
├─ Stakeholder Action: "Acknowledged change is necessary, reduced anxiety"
├─ Decision Gate: Psychological resistance < 30%
├─ Blockers: Status quo bias, sunk cost fallacy, identity threat
└─ Timeline: 2-4 weeks (emotional adjustment)

STAGE 5: DECISION (Make Commitment)
├─ Question: Will I commit to support/implementation?
├─ Stakeholder Action: "Voted yes, signed agreement, budgeted resources"
├─ Decision Gate: READY (θ_cap × θ_will) ≥ 0.65
├─ Blockers: Authority gaps, competing priorities, incentive misalignment
└─ Timeline: 1-2 weeks (formal decision)

STAGE 6: PREPARATION (Get Ready to Act)
├─ Question: Do I have resources/skills/authority to execute?
├─ Stakeholder Action: "Assembled team, secured budget, trained staff"
├─ Decision Gate: θ_capability ≥ 0.70
├─ Blockers: Resource constraints, skill gaps, competing demands
└─ Timeline: 2-8 weeks (pre-launch)

STAGE 7: ACTION (Implement Change)
├─ Question: Am I actively executing the plan?
├─ Stakeholder Action: "Day 1 execution: new process, new decisions, new behaviors"
├─ Decision Gate: Execution compliance ≥ 85%
├─ Blockers: Old habits, system friction, unclear processes
└─ Timeline: First 30-90 days (critical execution window)

STAGE 8: LOYALTY (Sustained Adoption)
├─ Question: Am I continuing to support the change AND advocating to others?
├─ Stakeholder Action: "Routine adoption, speaking positively about change"
├─ Decision Gate: Net Promoter Score (NPS) ≥ 7/10
├─ Indicators: Continued use, positive word-of-mouth, feedback on improvements
└─ Timeline: 6+ months (embedded in culture)
```

---

## Integration with Existing Systems

### Connection to Phase 4+5 Models

```
ALPLA Strategic Model (Phase 5)
    ├─ /apply-models ALPLA
    │   ├─ Revenue forecast: €2.85B (CAGR 6.9%)
    │   ├─ Confidence: E(θ) = ±0.8pp, 82% confident
    │   └─ Decision stratification: N_L2 ≈ 180 coordinated decisions
    │
    └─ Phase 6 Simulation: Who will approve/execute this?
        ├─ Board simulation: 84% approval prob (depends on briefing ✓)
        ├─ Regional leaders simulation: 78% hit CAGR (depends on incentives)
        ├─ Customer simulation: 65% buy-in (depends on WHAT match)
        └─ Employee simulation: 62% retention during execution
```

### Connection to Quarterly Learning Loop

```
Quarterly Review Cycle:
    Q1: Collect actuals
        └─ /intervention-manage close ALPLA --actuals Q1
            └─ quarterly_review.py outputs ΔP = -€50M

    Q1→Q2: Stakeholder trust re-evaluation
            └─ /simulate-stakeholder ALPLA board --updated
               → Awareness impact: Did board see miss?
               → Readiness impact: Did confidence drop?
               → Changed approval prob: 84% → 72%?

    Q2: Parameter update
        └─ parameter_update_pipeline.py shrinks E(θ) ±0.8pp → ±0.6pp
            └─ /simulate-stakeholder ALPLA --updated
               → WHERE confidence improves
               → Board approval prob: 72% → 79%

    Q3: Re-engage stakeholders
        └─ /simulate-stakeholder ALPLA customer --with-track-record
           → Now can show learning: 12 quarters ±2% accuracy
           → Customer purchase prob: 65% → 82%
```

---

## Success Metrics for Phase 6

| Metric | Target | Rationale |
|--------|--------|-----------|
| **Board Approval Prediction Accuracy** | ±15pp | Predict actual votes within ±15 percentage points |
| **Customer Purchase Probability** | ±20pp | Ranking customer likelihood correctly |
| **Employee Retention Prediction** | ±25pp | Anticipate retention/attrition before it happens |
| **Change Journey Stage Accuracy** | ±1 stage | Identify actual vs predicted BCJ stage |
| **Awareness & Readiness Correlation** | r > 0.7 | AU/AV scores correlate with actual decisions |
| **Scenario Planner Sensitivity** | δP/δX within 10% | Sensitivity to changes matches real responses |

---

## Phase 6 Timeline

| Week | Deliverable | Dependencies |
|------|-------------|--------------|
| **W1** | Stakeholder models & 10C profiles (8 docs, 1,200 lines) | Phase 5 complete |
| **W2** | /simulate-stakeholder skill core logic + Board/Customer models | Framework done |
| **W3** | All 12 stakeholder models + behavior matrix | Skills logic done |
| **W4** | Change Journey mapping + scenario planner + integration | All models done |
| **W5** | Documentation (800+ lines) + examples + Phase 6 summary | All systems done |

---

## Next: Detailed Stakeholder Model Designs

Ready to start? I recommend this sequence:

1. **Week 1:** Design all 12 stakeholder profiles (10C mapping for each)
2. **Week 2:** Build core simulation skill with decision functions
3. **Week 3:** Full behavior matrix (probability heatmaps)
4. **Week 4:** Change Journey + Scenario Planner
5. **Week 5:** Documentation + Integration + Launch

Should I proceed with creating the 12 detailed stakeholder models and the /simulate-stakeholder skill?

---

**Branch:** `claude/connect-strategic-models-ebf-av1cT`
**Status:** Ready for Phase 6 Implementation
