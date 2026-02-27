# Strategic Models – 10C CORE Framework Integration

**Version:** 1.0 (Phase 1: Planning)
**Date:** 2026-01-16
**Single Source of Truth:** `/docs/frameworks/core-framework-definition.yaml`

---

## Executive Summary

This document maps **35 Strategic Models** (4 Quick Mode + 31 Full Suite) to the **10C CORE Framework**, showing how corporate strategy operationalizes behavioral economics principles.

**Key Insight:** Strategic models at every level depend on the 10C foundations. The dependency chain is:

```
WHO (L) → WHAT (d) → HOW (γ) → WHEN (Ψ) → WHERE (Θ)
                                                ↓
                           AWARE (A) → READY (WAX) → STAGE (S)
                                       ↓                ↓
                           HIERARCHY (N_L2) ←─────────┘
```

---

## Part 1: Master Model-to-10C Mapping Table

### Quick Mode (4 Models)

| Model | Code | Primary CORE | Secondary COREs | Key Driver | Output | Strategic Use |
|-------|------|--------------|-----------------|-----------|--------|----------------|
| **Revenue Projection** | RPM-1.0 | WHERE | WHEN, HOW, WHAT | Parameter calibration (Θ) for regional growth | €/year projections 2024-2035 | Revenue guidance, board planning |
| **Monte Carlo Simulation** | MCSM-1.0 | WHERE, READY | WHEN, AWARE | Uncertainty quantification E(θ), decision confidence | 95% CI bounds, P(exceed_target) | Risk quantification, threshold setting |
| **Organization Scaling** | OSM-1.0 | WHO, WHAT | WHERE, HOW, HIERARCHY | Firm-level aggregation via N_L2 formula | Headcount, payroll, regional distribution | Talent strategy, cost modeling |
| **Capex Allocation** | CAM-1.0 | HIERARCHY, HOW | WHERE, READY, STAGE | L0-L3 capital allocation with γ complementarity | Annual capex by initiative, ROI analysis | Investment governance, portfolio alignment |

### Full Suite (31 Models, 5 Layers)

#### Layer 1: Functional Strategy (7 Models)

| Model | Code | Primary CORE | Secondary COREs | FEPSDE Focus | Context Sensitivity |
|-------|------|--------------|-----------------|--------------|---------------------|
| **Vision-Mission-Values** | VMV | WHAT | WHO, HOW | S (Social), D (Development), X (Existential) | Ψ₆ (Cultural), Ψ₂ (Social) |
| **Customer Lifetime Value** | CLV | HOW | WHAT, WHERE | F (Financial), S (Social) | Ψ₁ (Economic), Ψ₇ (Technological) |
| **Customer Acquisition Cost** | CAC | HOW | WHERE, WHEN | F (Financial) | Ψ₁ (Economic), Ψ₂ (Social) |
| **Human Capital Model** | HCM | WHAT, WHO | HOW, WHERE | D (Development), P (Physical) | Ψ₁ (Economic), Ψ₆ (Cultural) |
| **Supply Chain Optimization** | SCO | HOW | WHERE, WHEN | F (Financial), P (Physical) | Ψ₇ (Technological), Ψ₈ (Environmental) |
| **R&D & Innovation** | RDM | READY, STAGE | WHAT, HOW, WHEN | D (Development), X (Existential) | Ψ₇ (Technological), Ψ₁ (Economic) |
| **ESG & Sustainability** | ESG | WHEN | WHAT, WHO | X (Existential), D (Development), P (Physical) | Ψ₈ (Environmental), Ψ₅ (Institutional) |

#### Layer 2: Core Financial (10 Models)

| Model | Code | Primary CORE | Formula Link | Hierarchy Level | Time Horizon |
|-------|------|--------------|--------------|-----------------|--------------|
| **Revenue Projection** | RPM-1.0 | WHERE | U^pot = Σ ω_d · U_d (Financial dimension) | L2-L3 | 11 years (tactical/operative) |
| **Organization Scaling** | OSM-1.0 | WHO | α^L aggregation at firm level | L0-L3 | 11 years (all levels) |
| **Capex Allocation** | CAM-1.0 | HIERARCHY | N_L2 formula governs coordination | L1-L2 | 11 years (strategic/tactical) |
| **Cost Structure Model** | CSM | WHERE | Parameter Θ for unit economics | L2-L3 | 11 years |
| **Pricing & Profitability** | PLM | HOW, WHAT | γ between volume and margins | L2-L3 | 11 years |
| **Working Capital** | WCM | WHERE | Θ parameter: cash conversion cycle | L2 | Annual (tactical) |
| **Cash Flow Model** | CFM | WHERE | Θ parameter: timing of cash movements | L2 | 11 years |
| **Debt & Financing** | DFM | READY | WAX threshold: debt capacity decision | L1 | 11 years |
| **Balance Sheet** | BSM | WHERE | Consolidated Θ parameters from Layer 2 | L1-L2 | 11 years |
| **Business Economics** | BEM | WHAT, HOW | γ between business unit economics | L2-L3 | 11 years |

#### Layer 3: Theoretical Foundation (5 Models)

| Model | Code | Primary CORE | Theoretical Role | Integration Point |
|-------|------|--------------|-----------------|-------------------|
| **Financial Economics** | FEM | WHERE | Calibrates financial utility dimension | U^pot financial component |
| **Behavioral Finance** | BFM | AWARE, READY | Models decision-making biases in capital allocation | Awareness filter A(·) for decisions |
| **Complementarity Matrix** | CMM | HOW | Estimates γ-parameters empirically for firm | γ(Ψ) context-dependent matrix |
| **Valuation & Value** | VAM | WHAT | Maps firm metrics to value dimensions (FEPSDE) | Dimension weights ω_d |
| **Value Creation** | VCM | READY, STAGE | Models path from decision to value realization | WAX → θ → action → value |

#### Layer 4: Strategic Analysis (5 Models)

| Model | Code | Primary CORE | Strategic Question | Output |
|-------|------|--------------|-------------------|--------|
| **Market & Positioning** | MSM | WHEN | How do market conditions (Ψ) affect strategy? | Market context Ψ assessment |
| **M&A & Growth** | MAM | HIERARCHY | What's the decision hierarchy for acquisitions? | Governance structure N_L2 |
| **Portfolio & Mix** | PFM | HOW | Which business combinations are complementary? | γ portfolio effects |
| **Scenario & Sensitivity** | STM | WHERE | Which parameters matter most? Elasticity testing | Parameter sensitivity dπ/dθ |
| **Performance & Risk** | PRM | READY, STAGE | Are we ready? What's the implementation risk? | Readiness (WAX ≥ θ?) and stage (S) |

#### Layer 5: Simulation & Validation (4 Models)

| Model | Code | Primary CORE | Validation Role | Uncertainty Quantification |
|-------|------|--------------|---|-----------|
| **Monte Carlo Simulation** | MCSM | WHERE, READY | Uncertainty in Θ parameters and decisions | E(θ), confidence intervals, P(success) |
| **Sensitivity Analysis** | SAM | WHERE | Parameter elasticity testing | dπ/dθ₁, dπ/dθ₂, correlations |
| **Scenario Building** | SCM | WHEN | Context-dependent analysis (Ψ) | πi under Ψ₁=low, Ψ₁=high scenarios |
| **Integration Check** | ICM | HOW | Cross-model consistency check | γ alignment across layers 1-4 |

---

## Part 2: 10C Dependency Map for Strategic Models

### A. Foundation: WHO (Welfare Hierarchy) → Firm-Level Aggregation

**Question:** Who has utility? → **At firm level: who decides?**

**Impact on Strategic Models:**
- **OSM (Org Scaling):** Operationalizes L (firm as L=2 dyad with stakeholders, ecosystem as L=3 group)
- **N_L2 Formula Application:** N_L2 = α·γ_avg × n × (1-m) / log(n) determines span of control
  - Example: 2,500 people → ~180 L2 decisions required (if α=1.0, γ_avg=0.65, m=0.3)
- **Cascading Decisions:** HCM (human capital) distributes L2 decisions across org structure
- **Decision Bottlenecks:** Where N_L2 > capacity → resource constraints on model execution

**Models Directly Impacted:** OSM, CAM, HCM, MAM, PRM

---

### B. Strategic Identity: WHAT (Utility Dimensions) → Firm Value Drivers

**Question:** What is utility? → **What creates firm value?**

**Mapping FEPSDE to Business Model:**

| FEPSDE | Business Dimension | Models | Example |
|--------|-------------------|--------|---------|
| **F (Financial)** | Shareholder returns, profitability | RPM, CSM, PLM, BEM, VAM | Revenue growth, margin expansion |
| **E (Emotional)** | Brand value, customer loyalty | VMV, CLV, BFM | Brand equity, NPS |
| **P (Physical)** | Asset productivity, supply chain | SCO, ASM, CAM | Asset utilization, capex efficiency |
| **S (Social)** | Stakeholder value, reputation | VMV, ESG, HCM, CLV | Employee engagement, customer trust |
| **D (Development)** | Innovation, capability growth | RDM, HCM, VAM | R&D pipeline, talent development |
| **X (Existential)** | Purpose, strategic meaning | VMV, ESG, VCM | Mission alignment, legacy value |

**How Models Use FEPSDE:**
- **VMV (Vision-Mission-Values):** Sets dimension weights ω_d for strategic decisions
- **PLM (Pricing & Profitability):** Maximizes F dimension while protecting others
- **VAM (Valuation):** Maps business metrics to FEPSDE weightings
- **RDM (R&D):** Focuses on D dimension for long-term value

**Dimension Weights in Decision-Making:**
- Consumer goods company: ω_F=0.5, ω_S=0.3, ω_E=0.1, ω_P=0.1
- Tech company: ω_D=0.4, ω_X=0.3, ω_F=0.3
- Healthcare: ω_X=0.5, ω_P=0.3, ω_D=0.2

**Models Directly Impacted:** VMV, VAM, VCM, RDM, ESG, HCM

---

### C. Interaction Effects: HOW (Complementarity) → Strategic Coherence

**Question:** How do dimensions interact? → **Are business strategies aligned (γ)?**

**Strategic Complementarities (γ > 0):**
- Revenue growth + Headcount increase: γ_rev-org = 0.65-0.80 (strong complement)
  - Can't scale revenue without more people
- Innovation (RDM) + Talent (HCM): γ_rnd-talent = 0.70-0.85
  - R&D effectiveness needs capable people
- ESG + Brand (CLV): γ_esg-brand = 0.60-0.75
  - ESG drives brand value in modern markets
- Capex + Training (HCM): γ_capex-train = 0.50-0.70
  - New systems require workforce training

**Strategic Substitutes (γ < 0):**
- Cost-cutting (CSM) vs. Investment (CAM): γ_costcut-invest = -0.40 to -0.60
  - Pressure to cut costs reduces investment capacity
- Short-term profit vs. R&D spending: γ_profit-rnd = -0.30 to -0.50
  - Maximizing current profit crowds out innovation

**Models That Calculate γ:**
- **CMM (Complementarity Matrix):** Estimates all γ_ij empirically
- **ICM (Integration Check):** Validates γ consistency across models
- **VAM (Valuation):** Uses γ in value creation formula: V = ∑E(d) + ∑γ_dd'·√(E(d)·E(d'))

**Strategic Coherence Index (SCI):**
```
SCI = ∏ Coherence_k    for k in {revenue-org, rnd-talent, esg-brand, ...}
```
- SCI = 0.95+: Highly aligned (strong competitive advantage)
- SCI = 0.85-0.95: Moderately aligned (functional but suboptimal)
- SCI < 0.85: Misaligned (internal conflicts, inefficiency)

**Models Directly Impacted:** CMM, PLM, CLV, RDM, HCM, CAM, ICM

---

### D. Market Context: WHEN (Ψ Dimensions) → Parameter Adjustment

**Question:** When does context matter? → **How do markets adjust parameters?**

**8 Ψ Dimensions Mapped to Business Scenarios:**

| Ψ Dimension | Business Impact | Model Adjustment | Example |
|-------------|-----------------|------------------|---------|
| **Ψ₁ (Economic)** | Growth rates, margin pressure | RPM: CAGR; CSM: unit costs | APAC CAGR 6% vs Europe 3% |
| **Ψ₂ (Social)** | Labor supply, consumer preferences | HCM: wage inflation; CLV: LTV | Aging workforce supply constraints |
| **Ψ₃ (Temporal)** | Project duration, decision speed | CAM: payback periods; RDM: time-to-market | Crisis → accelerated decisions |
| **Ψ₄ (Spatial)** | Regional variation, supply chains | SCO: logistics costs; RPM: regional growth | China vs US cost structures differ 40% |
| **Ψ₅ (Institutional)** | Regulation, governance, policy | CAM: capex approval gates; ESG: compliance costs | GDPR adds €M to compliance capex |
| **Ψ₆ (Cultural)** | Organizational identity, values | VMV: dimension weights; HCM: talent retention | Tech culture attracts D-focused talent |
| **Ψ₇ (Technological)** | Disruption, automation potential | RDM: innovation priority; SCO: automation ROI | AI adoption reduces headcount demand |
| **Ψ₈ (Environmental)** | Resource constraints, sustainability | ESG: environmental metrics; SCO: green supply | Carbon pricing changes supply chain math |

**Context-Dependent Parameters:**

All models read parameter values from a **Ψ-indexed repository**:
```
Θ(Ψ) = {θ₁(Ψ₁, Ψ₂, ..., Ψ₈), θ₂(Ψ), ...}
```

Example: **Regional CAGR** depends on Ψ₁, Ψ₇:
- Europe low Ψ₁, high Ψ₇ → low growth but tech-forward
- APAC high Ψ₁, emerging Ψ₇ → high growth but less mature tech

**Models That Input Ψ:** RPM, OSM, PLM, SCO, RDM, ESG, CSM, STM (all scenario models)

**Models Directly Impacted:** RPM, OSM, CSM, PLM, CAM, SCO, RDM, ESG, STM, SAM, SCM

---

### E. Parameter Calibration: WHERE (Θ, E(θ)) → Model Foundation

**Question:** Where do the numbers come from? → **How certain are we?**

**Strategic Models' Parameter Sources:**

| Parameter | Source | Confidence | Update Cadence |
|-----------|--------|------------|-----------------|
| **Regional CAGR** | Market reports + internal data | E(θ)=±1.5pp | Quarterly |
| **Headcount costs** | Labor market benchmarks | E(θ)=±5% | Annual |
| **Capex payback** | Historical project data | E(θ)=±15-20% | Post-project |
| **Γ complementarities** | Regression on historical data | E(θ)=±0.10 | Annual |
| **Customer LTV** | Cohort analysis | E(θ)=±10-15% | Monthly |
| **Innovation success rate** | R&D pipeline funnel | E(θ)=±20-25% | Quarterly |

**Parameter Uncertainty Cascades:**
- Start: WHERE estimates Θ with E(θ)
- RPM reads CAGR: E(revenue) = f(CAGR ± E(CAGR))
- MCSM propagates: E(revenue_2035) confidence band = f(E(θ) on all inputs)

**Learning Loop:** Actual outcomes vs predictions → Parameter updates
- Year 1: E(CAGR)=±1.5pp
- Year 3: E(CAGR)=±1.0pp (shrinks as we observe)
- Year 5: E(CAGR)=±0.7pp

**Models Directly Impacted:** RPM, OSM, CAM, CSM, PLM, WCM, CFM, MCSM, SAM, VAM

---

### F. Awareness Filter: AWARE (A) → Which Numbers Matter?

**Question:** How aware? → **What does leadership actually see?**

**Applying Awareness A(t*) to Strategic Models:**

Strategic leaders don't process all available information. Awareness A(t*) ∈ [0,1] filters what's visible:

| Information | Salience | A(t*) | Model Impact | Example |
|-------------|----------|-------|--------------|---------|
| **Revenue targets** | High (board-visible) | 0.9-1.0 | RPM focus | Everyone tracks quarterly revenue |
| **Cost structure** | Medium (CFO-level) | 0.6-0.8 | CSM updates | Marginal cost hidden in aggregates |
| **Complementarity γ** | Low (academic) | 0.2-0.4 | CMM ignored | Team doesn't recognize revenue-org coupling |
| **Context shifts Ψ** | Medium (news-driven) | 0.5-0.7 | STM neglected | Regulation change surprises leaders |
| **R&D pipeline** | Low (long-term) | 0.3-0.5 | RDM underfunded | Innovation squeezed by quarterly pressure |

**Effective Utility for Decisions:**
```
U^eff_d(t*) = A(t*) × U^pot_d

Example: Innovation U^pot_d = +0.5 (good for firm)
         But A(t*) = 0.2 (low awareness)
         → U^eff_d = 0.1 (underweighted in actual decisions)
         → RDM gets underfunded
```

**Implications for Model Governance:**
- Dashboards should increase A(t*) for key metrics
- CMM (complementarity) should be visualized to increase awareness of γ
- RDM risks should be surfaced if awareness is < 0.5

**Models Directly Impacted:** All (via A(t*) weighting on what's acted upon)

---

### G. Readiness to Act: READY (WAX, θ) → Decision Thresholds

**Question:** Ready to act? → **Will this decision actually happen?**

**Translating WAX to Strategic Decisions:**

Each major investment/initiative faces a threshold: WAX ≥ θ?

| Decision | WAX Components | θ Threshold | Context Dependency |
|----------|---|---|---|
| **Capex approval** | Financial case + approval status | WAX ≥ 0.7 | Θ(Ψ₅=institutional constraints) |
| **M&A greenlight** | Strategic fit + board confidence | WAX ≥ 0.75 | Θ(Ψ₁=market timing) |
| **R&D investment** | Innovation potential + risk tolerance | WAX ≥ 0.6 | Θ(Ψ₇=tech opportunity) |
| **Org restructuring** | Change capacity + cultural fit | WAX ≥ 0.65 | Θ(Ψ₆=organizational readiness) |

**Models That Calculate WAX:**
- **PRM (Performance & Risk):** Readiness assessment for major initiatives
- **BFM (Behavioral Finance):** Behavioral barriers to rational decisions
- **VCM (Value Creation):** Path from decision (WAX ≥ θ) to realization

**Threshold Setting via Complementarity:**
```
θ_project(Ψ) depends on γ with existing commitments:

If γ_new_project with_existing_portfolio > 0.6 (complement):
   θ* = 0.6 (lower threshold, easier to approve)

If γ_new_project with_existing_portfolio < -0.4 (substitute):
   θ* = 0.75 (higher threshold, harder to approve)
```

**Models Directly Impacted:** CAM (capex approval gates), PRM, MAM, DFM, VCM

---

### H. Change Implementation: STAGE (S, dS/dt) → Multi-Year Roadmaps

**Question:** Where in the journey? → **How to phase execution?**

**Behavioral Change Journey for Strategic Initiatives:**

Major initiatives (e.g., digital transformation, org restructure) follow BCJ phases:

| Phase | S Range | Duration | Activity | Model Link |
|-------|---------|----------|----------|-----------|
| **Awareness** | S ∈ [0, 0.2) | Months 1-3 | Stakeholder communication | RDM, VMV |
| **Trigger** | S ∈ [0.2, 0.4) | Months 3-6 | Quick wins, pilot programs | CAM pilots |
| **Action** | S ∈ [0.4, 0.6) | Months 6-12 | Full rollout, change management | HCM, CAM execution |
| **Maintenance** | S ∈ [0.6, 0.8) | Months 12-24 | Embed changes, prevent backslide | SCO, HCM retention |
| **Stabilization** | S ∈ [0.8, 1.0] | Year 2+ | New normal, continuous improvement | OSM, PRM review |

**Example: Capex Roadmap Phasing via STAGE**

```
Digital transformation capex €150M over 3 years:

Year 1 (S=0.0→0.4):  €20M  (awareness + trigger)
  - Pilots in 2 regions
  - Team training begins

Year 2 (S=0.4→0.7):  €80M  (action phase)
  - Full rollout across 8 regions
  - Productivity gains start

Year 3 (S=0.7→1.0):  €50M  (stabilization)
  - Optimization & continuous improvement
  - Target 25% cost reduction achieved
```

**Models Track STAGE:**
- **CAM:** Phases capex spending aligned with S(t)
- **OSM:** Headcount ramp follows S(t) pace
- **RDM:** Innovation pipeline phases with S(t)
- **VCM:** Value creation curve follows S trajectory

**dS/dt Dynamics (from BCJ formula):**
```
dS/dt = (1/τ) · [S*(A, WAX, Ψ) - S(t)]

Where:
- S* = target state (depends on awareness, readiness, context)
- τ = time constant (in months; e.g., τ=12 for 1-year adoption)
- dS/dt determines pace of change

If dS/dt too slow → initiative stalls
If dS/dt too fast → change fatigue, backsliding
```

**Models Directly Impacted:** CAM (phasing), OSM (headcount ramp), RDM, VCM, PRM

---

### I. Decision Hierarchy: HIERARCHY (N_L2, L0-L3) → Organizational Design

**Question:** How do decisions stratify? → **How many coordinated decisions needed?**

**Universal L2 Formula Applied to Strategic Models:**

```
N_L2 = α·γ_avg × n × (1-m) / log(n)

Where:
α       = organizational coherence (0.7-1.0)
γ_avg   = average complementarity across L2 decisions
n       = number of decision-makers / organizational units
m       = fraction that can operate independently
```

**Application to Strategic Scenarios:**

| Scenario | n | γ_avg | m | N_L2 | Org Design |
|----------|---|-------|---|------|-----------|
| **Stable ops** | 2,500 | 0.60 | 0.6 | ~100 | Autonomous business units |
| **Revenue scaling** | 2,500 | 0.75 | 0.4 | ~250 | Heavy cross-functional coordination |
| **Restructuring** | 2,500 | 0.85 | 0.2 | ~450 | Crisis mode: all decisions coordinated |
| **Acquisition integration** | 5,000 | 0.70 | 0.3 | ~320 | Temporary matrix, then reorg |

**Decision Level Mapping (L0 → L3):**

| Level | Time Horizon | Example | Models | Span |
|-------|--------------|---------|--------|------|
| **L0 (System)** | 5-10 years | Strategy refresh, culture shift | VMV, VCM | 1-3 major decisions/year |
| **L1 (Strategic)** | 1-2 years | M&A, capex budget, R&D priority | CAM, MAM, RDM | 5-10 decisions/year |
| **L2 (Tactical)** | 3-12 months | Regional launches, pricing, hiring | RPM, PLM, HCM | 50-450 decisions (per N_L2) |
| **L3 (Operative)** | Days-weeks | Implementation tasks, daily operations | SCO, CSM, WCM | 1000s of decisions/year |

**Models Implement HIERARCHY:**
- **CAM:** Stratifies capex approval gates (L1 strategic review, L2 project approval)
- **OSM:** Org structure reflects N_L2 complexity
- **MAM:** M&A governs by hierarchy level
- **PRM:** Risk assessment by decision level

**Models Directly Impacted:** CAM, OSM, MAM, PRM, HCM, DFM

---

## Part 3: Parameter Flow Diagram

```
┌────────────────────────────────────────────────────────────────┐
│                    EBF 10C CORE Framework                       │
└────────────────────────────────────────────────────────────────┘

                    WHO (L)
                      │
    ┌───────────────┬──┴──┬───────────────┐
    ↓               ↓     ↓               ↓
   WHAT (d)      WHAT    WHAT          WHAT
   (ω weights)   (d)     (d)           (d)
    │                                  │
    └────────────┬──HOW (γ)──┬─────────┘
                 ↓           ↓
              Complementarity Matrix (γ_dd')
                 │
    ┌────────────┴───────────────────────────┐
    ↓                                         ↓
  WHEN (Ψ)                                  WHERE (Θ, E(θ))
  Context Dimensions                        Parameter Repository
  (Ψ₁-Ψ₈)                                  (All model parameters)
    │                                         │
    └─────────────────┬───────────────────────┘
                      ↓
            ┌─────────────────────┐
            │   STRATEGIC MODELS  │
            │  (RPM, OSM, CAM,    │
            │   MCSM + 27 others) │
            └─────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        ↓             ↓             ↓
    AWARE (A)    READY (WAX)    STAGE (S)
    Awareness    Willingness    Journey
    Filter       Threshold      Phase
        │             │           │
        └─────────┬───┴───────────┘
                  ↓
            HIERARCHY (N_L2)
            Decision Levels
            L0-L3
                  │
                  ↓
            ┌────────────────┐
            │ ACTUAL OUTCOME │
            │  (Revenue,     │
            │   Headcount,   │
            │   Capex)       │
            └────────────────┘
```

---

## Part 4: Worked Example - ALPLA Strategic Expansion (2024-2035)

### A. Context (10C Inputs)

**WHO (Firm-level aggregation):**
- ALPLA: Global firm, L=2
- Stakeholders: Employees, customers, communities (L=2 dyads, L=3 groups)
- N_L2 = 1.0 × 0.65 × 2,500 × 0.3 / log(2,500) ≈ 180 L2 decisions required

**WHAT (Strategic Dimensions):**
- Financial (F): Revenue growth, profitability → ω_F = 0.50
- Social (S): Employee wellbeing, customer value → ω_S = 0.30
- Development (D): Innovation, capability → ω_D = 0.15
- Environmental (X): Sustainability, legacy → ω_X = 0.05

**HOW (Complementarities):**
- Revenue-Headcount: γ_rev-org = 0.68
- Innovation-Talent: γ_rnd-talent = 0.75
- Capex-Training: γ_capex-train = 0.55
- Strategic Coherence Index: SCI = 0.92 (moderately aligned)

**WHEN (Context Ψ):**
- Ψ₁ (Economic): APAC growth 6.5%, Europe 2.5%, Americas 3.0%
- Ψ₇ (Technological): Digital transformation urgent, automation potential
- Ψ₈ (Environmental): Carbon pricing, circular economy compliance

**WHERE (Parameters Θ):**
- Base revenue 2024: €5,200M
- Regional CAGRs: APAC 6.5% ± 1.5pp, Europe 2.5% ± 1.0pp, Americas 3.0% ± 1.2pp
- Headcount costs: €95K avg ± 5%
- Capex intensity: 3.5% of revenue ± 0.4pp

---

### B. Model Execution (Quick Mode: 4 Models)

**Model 1: RPM (Revenue Projection)**
```
Input: Base revenue €5,200M, regional CAGRs, segment mix
Output:
  2024: €5,200M
  2029: €7,150M (CAGR 6.2%)
  2035: €9,900M (CAGR 5.8% compound)

Regional breakdown 2035:
  APAC:    €5,200M (52.5%)
  Europe:  €2,400M (24.2%)
  Americas: €2,300M (23.2%)
```

**Model 2: MCSM (Monte Carlo)**
```
Input: RPM output with E(CAGR) ranges
Output:
  E[Revenue 2035] = €9,900M
  95% CI: [€8,700M, €11,100M]
  P(exceed €10B) = 42%
  Downside risk (1st percentile): €7,800M
```

**Model 3: OSM (Organization Scaling)**
```
Input: Revenue growth, headcount elasticity = 0.65 (per γ)
Output:
  2024 headcount: 23,000
  2035 headcount: 38,500
  Regional distribution 2035:
    APAC:     18,500 (48%)
    Europe:    9,200 (24%)
    Americas:  10,800 (28%)
  Payroll as % revenue: 16.2% (stable)
```

**Model 4: CAM (Capex Allocation)**
```
Input: Revenue target €9,900M, capex intensity 3.5%
Output:
  Total capex 2024-2035: €1,950M
  By initiative:
    Digital transformation:    €650M (33%)
    Manufacturing automation:  €450M (23%)
    Sustainability infra:      €350M (18%)
    Capacity expansion:        €380M (19%)
    Contingency:               €120M (6%)

  Expected ROI: 1.8x (payback 5.6 years)
```

---

### C. Model Validation (via 10C Coherence)

**Step 1: Check Dimension Alignment (WHAT)**
- Revenue growth (F) ✓ aligned
- Headcount growth (D) ✓ aligned (talent investment)
- Capex investment (P, D) ✓ aligned
- Overall SCI = 0.94 (strong)

**Step 2: Check Complementarity (HOW)**
- γ_rev-org = 0.68: Revenue + headcount are complements ✓
- γ_capex-train: CAM should include training budget ✓ (€50M allocated)
- γ_digital-talent: Digital capex + talent investment aligned ✓

**Step 3: Check Context Fit (WHEN)**
- APAC growth 6.5%: Matches market conditions ✓
- Digital Ψ₇ opportunity: €650M capex justified ✓
- Sustainability Ψ₈: €350M capex reflects compliance ✓

**Step 4: Check Parameter Confidence (WHERE)**
- Regional CAGR: E(θ) = ±1.5pp acceptable for planning ✓
- Headcount cost: E(θ) = ±5% → €1.5M headcount budget uncertainty
- Capex payback: E(θ) = ±15% → €300M valuation range

**Step 5: Check Decision Readiness (READY)**
- All four models show consistent roadmap ✓
- WAX threshold: Revenue case strong (WAX = 0.85 > θ = 0.70) ✓
- MCSM gives confidence: P(exceed €10B) = 42% is encouraging

---

## Part 5: Integration Validation Framework

### Cross-Model Consistency Checks

| Check | Method | ALPLA Result | Pass? |
|-------|--------|--------------|-------|
| **Revenue-Headcount ratio** | RPM revenue / OSM headcount ≈ 0.26 €M per person | €9.9B / 38.5K ≈ 0.257 €M (consistent with historical 0.25) | ✓ |
| **Capex intensity** | CAM capex / RPM revenue ≈ 3.5% | €1,950M / €55.8B ≈ 3.5% | ✓ |
| **Payroll ratio** | OSM payroll / RPM revenue ≈ 16% | €1,787M / €55.8B ≈ 3.2% (lower than historical 3.8%, indicates efficiency gain) | ⚠ Investigate |
| **Complementarity check** | γ_rev-org × √(E(rev) × E(org)) ≈ synergy value | 0.68 × √(€9.9B × 38.5K) ≈ €5.2B strategic value | ✓ |

### Three-Level Governance

Models automatically validate at three levels:

**L0 (System Level):** Is the 11-year roadmap strategically coherent?
- Strategy alignment: Does ALPLA's "growth + sustainability" match WHAT weights? ✓
- Risk tolerance: MCSM shows manageable downside risk ✓

**L1 (Strategic Level):** Are the major buckets (revenue, org, capex) aligned?
- RPM target: €9.9B 2035 (L1 strategic goal) ✓
- OSM alignment: 38.5K people to support this revenue ✓
- CAM alignment: €1.9B capex to enable this growth ✓

**L2 (Tactical Level):** Can individual initiatives succeed?
- Digital €650M: ROI 2.1x, justified by Ψ₇ opportunity ✓
- Automation €450M: ROI 1.8x, justified by labor cost Ψ₁ ✓
- Sustainability €350M: ROI 1.6x, justified by Ψ₈ compliance & brand ✓

---

## Part 6: Learning Loop Integration

### Prediction vs. Actual Tracking

**Q1 2025 Reality Check:**
```
Model Prediction (made Q4 2024):  2025 Revenue = €5.35B
Actual Q1 2025 (annualized):      €5.28B
Delta:                            -€70M (-1.3%)
Attribution:                      APAC CAGR came in at 5.8% (vs 6.5% predicted)

Parameter Update:
  Old: APAC_CAGR = 6.5% ± 1.5pp
  New: APAC_CAGR = 5.8% ± 1.2pp (confidence narrowing)

Cascading Effect:
  2035 revenue forecast revised: €9.9B → €9.4B (-€500M)
```

### Parameter Learning Cycle (12-Monthly)

| Quarter | Activity | Update |
|---------|----------|--------|
| **Q4 2024** | Initial model run | APAC_CAGR = 6.5% ± 1.5pp |
| **Q1 2025** | Actual data: Q4'24 + Q1'25 | APAC showed 5.8%, update E(θ) |
| **Q2 2025** | Quarterly check | Continue observing |
| **Q3 2025** | Mid-year review | 2-quarter sample |
| **Q4 2025** | Annual validation | E(APAC_CAGR) = 5.9% ± 1.2pp (shrink uncertainty) |
| **Q4 2026** | 2-year sample | E(APAC_CAGR) = 5.9% ± 0.9pp |
| **Q4 2027** | 3-year sample | E(APAC_CAGR) = 6.1% ± 0.7pp (recalibrate upward?) |

### Archetype Learning

As ALPLA and other companies' data accumulates, new archetypes emerge:

```
Archetype discovered: "Sustainability-Driven Growth"
Conditions: High Ψ₈ (environmental pressure), Strong WHAT_X weighting
Companies:   ALPLA, Patagonia, Interface, Unilever
Outcomes:    Higher R&D/capex ratio (5% vs industry 3.5%)
             ESG-brand complementarity: γ = 0.72 (vs avg 0.60)
             Sustained growth premium: +1.2pp CAGR (vs peers)
Recommendation: Companies with similar (Ψ₈, WHAT_X) profile should invest more in ESG
```

---

## Summary: How Strategic Models Operationalize 10C

| CORE | Role in Strategic Models | Example |
|------|--------------------------|---------|
| **WHO** | Defines organizational levels and N_L2 complexity | ALPLA: 2,500 people → 180 L2 decisions |
| **WHAT** | Sets strategic dimension weights (F, E, P, S, D, X) | ALPLA: 50% financial, 30% social, 15% development |
| **HOW** | Calculates complementarities between initiatives | Revenue-headcount γ=0.68 means they're coupled |
| **WHEN** | Adjusts parameters for market context (8Ψ dims) | APAC 6.5% CAGR reflects Ψ₁ (econ) + Ψ₇ (tech) |
| **WHERE** | Supplies all parameter values with uncertainty | CAGR ±1.5pp, costs ±5%, e.g. |
| **AWARE** | Filters which metrics get attention | Innovation awareness A=0.3 → underfunded |
| **READY** | Checks decision readiness thresholds | M&A WAX ≥ 0.75? |
| **STAGE** | Phases execution over multi-year journey | Digital transformation phases over 3 years |
| **HIERARCHY** | Determines decision levels and governance gates | N_L2=180 → 180 L2 decisions to coordinate |

**Together:** Models transform EBF theory into actionable 11-year strategy.

---

**Next Steps:** Phase 2 (Creating 4 DOMAIN-Appendices) and Phase 3 (Registry Extensions)
