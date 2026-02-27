# /sensitivity-analysis Skill
## Test Parameter Sensitivity and Impact Analysis

**Purpose:** Quantify "what-if" scenarios in < 2 minutes

**Time Estimate:** 30 seconds - 2 minutes

---

## Usage

```
/sensitivity-analysis <company_name> <parameter> <change> [output_format]

Examples:
  /sensitivity-analysis Company_XYZ APAC_CAGR -1.5pp
  /sensitivity-analysis Company_XYZ Europe_revenue +500
  /sensitivity-analysis Company_XYZ capex_budget -10pct
  /sensitivity-analysis ALPLA headcount_cost +5pct table
  /sensitivity-analysis ALPLA all auto
```

---

## Parameter Types Supported

### Type 1: Regional CAGR Changes
```
/sensitivity-analysis <company> <REGION>_CAGR <±Npp>

Examples:
  /sensitivity-analysis CompanyX Europe_CAGR +1pp
  /sensitivity-analysis CompanyX APAC_CAGR -2pp
  /sensitivity-analysis CompanyX SA_CAGR -1.5pp

Regions: Europe, Asia-Pacific (APAC), South America (SA),
         North America (NA), Africa/Middle East (AMET)

Change Format: ±<number>pp (percentage points)
Valid Range: -5pp to +10pp (typical: ±1-2pp)
```

### Type 2: Revenue/Segment Changes
```
/sensitivity-analysis <company> <SEGMENT>_revenue <±N%>

Examples:
  /sensitivity-analysis CompanyX Pharma_revenue +10pct
  /sensitivity-analysis CompanyX Commodity_revenue -5pct

Segments: Beverage, Pharma, Industrial, Recycled_Materials

Change Format: ±<number>pct (percentage)
Valid Range: -30% to +30%
```

### Type 3: Cost Structure Changes
```
/sensitivity-analysis <company> <COST>_cost <±N%>

Examples:
  /sensitivity-analysis CompanyX headcount_cost +5pct
  /sensitivity-analysis CompanyX capex_per_unit -10pct
  /sensitivity-analysis CompanyX operational_margin +2pct

Cost Types: headcount_cost, capex_per_unit, operational_margin, ...

Change Format: ±<number>pct
Valid Range: -20% to +20%
```

### Type 4: Capex Changes
```
/sensitivity-analysis <company> capex_budget <±N%>

Examples:
  /sensitivity-analysis CompanyX capex_budget +15pct
  /sensitivity-analysis CompanyX capex_budget -20pct

Change Format: ±<number>pct
Valid Range: -50% to +50%
```

### Type 5: Bulk Analysis (All Key Parameters)
```
/sensitivity-analysis <company> all [test_depth]

Examples:
  /sensitivity-analysis CompanyX all
  /sensitivity-analysis CompanyX all standard  (±1pp or ±5%)
  /sensitivity-analysis CompanyX all extended  (±2pp or ±10%)

Tests all key parameters:
  - All regional CAGRs (±1pp standard, ±2pp extended)
  - Major segments (±5% standard, ±10% extended)
  - Headcount cost (±5% standard, ±10% extended)
  - Capex budget (±10% standard, ±20% extended)
```

---

## Workflow

### Step 1: Parse Input
- Extract company name
- Identify parameter type
- Validate parameter name against registry
- Parse change value (direction + magnitude)

**Validation:**
- Parameter exists in assumptions ✓
- Change value within valid range ✓
- Company directory exists ✓

### Step 2: Load Base Case
```python
base_config = load_yaml(f'data/customers/{company_name}/_assumptions.yaml')
base_metrics = load_yaml(f'data/customers/{company_name}/summary_metrics.yaml')
```

### Step 3: Create Alternative Scenarios

**Scenario A: Downside (Parameter decreased)**
```yaml
config_down = deepcopy(base_config)
config_down['regional_growth_rates']['apac']['cagr'] = 8.5 - 1.5  # = 7.0%
```

**Scenario B: Base Case (No change)**
```yaml
config_base = base_config  # Unchanged
```

**Scenario C: Upside (Parameter increased)**
```yaml
config_up = deepcopy(base_config)
config_up['regional_growth_rates']['apac']['cagr'] = 8.5 + 1.5  # = 10.0%
```

### Step 4: Re-Run Affected Models

**For CAGR Changes:** Re-run RPM-1.0 only
```python
df_revenue_down = project_revenue(config_down)
df_revenue_base = project_revenue(config_base)
df_revenue_up = project_revenue(config_up)

revenue_down = df_revenue_down[df_revenue_down['Year']==2035]['Total'].values[0]
revenue_base = df_revenue_base[df_revenue_base['Year']==2035]['Total'].values[0]
revenue_up = df_revenue_up[df_revenue_up['Year']==2035]['Total'].values[0]
```

**For Headcount Changes:** Re-run OSM-1.0
```python
result_down = project_headcount(config_down)
result_base = project_headcount(config_base)
result_up = project_headcount(config_up)

headcount_down = result_down['total_headcount_2035']
headcount_base = result_base['total_headcount_2035']
headcount_up = result_up['total_headcount_2035']
```

**For Capex Changes:** Re-run CAM-1.0
```python
result_down = project_capex(config_down)
result_base = project_capex(config_base)
result_up = project_capex(config_up)

capex_down = result_down['total_capex_11_years']
roi_down = result_down['total_roi_percent']
```

### Step 5: Calculate Impact

**Impact Formula:**
```
Impact (absolute) = Value_UP - Value_DOWN
Impact (%) = (Value_UP - Value_DOWN) / Value_BASE * 100

Elasticity (per 1pp or 1%):
  = Impact / (2 * Change_Magnitude)  [if change is ±N]
```

**Example Calculation:**
```
Base APAC CAGR: 8.5%
Change: -1.5pp to -0.5pp and +0.5pp to +1.5pp (range test)

Scenario Down: 8.5% - 1.5pp = 7.0%
  Revenue 2035: €2,450M

Scenario Base: 8.5%
  Revenue 2035: €2,850M

Scenario Up: 8.5% + 1.5pp = 10.0%
  Revenue 2035: €3,250M

Impact Range: €3,250M - €2,450M = €800M
Elasticity: €800M / (2 × 1.5pp) = €267M per 1pp CAGR change

Result:
  If APAC CAGR drops 1pp → Revenue drops ~€267M
  If APAC CAGR rises 1pp → Revenue rises ~€267M
```

### Step 6: Generate Sensitivity Table

**Output Table:**
```
╔════════════════════════════════════════════════════════════════╗
║ SENSITIVITY ANALYSIS: APAC_CAGR Change ±1.5pp                ║
╠════════════════════════════════════════════════════════════════╣
║ Base Assumption: APAC CAGR = 8.5%                            ║
║ Change Range: -1.5pp to +1.5pp                               ║
╠════════════════════════════════════════════════════════════════╣

Revenue Impact (2035):
  Downside (7.0% CAGR):  €2,450M (-€400M vs base, -14%)
  Base Case (8.5%):       €2,850M (baseline)
  Upside (10.0%):         €3,250M (+€400M vs base, +14%)

Elasticity: €267M per 1pp CAGR change

Headcount Impact (2035):
  Downside: 7,800 employees
  Base Case: 8,100 employees
  Upside: 8,400 employees

Payroll Impact (€M):
  Downside: €562M
  Base Case: €583M
  Upside: €605M
```

### Step 7: Identify Sensitivity Ranking

**Question: Which parameters matter most?**

Run across all key parameters and rank:
```
Parameter Sensitivity Ranking (Impact on 2035 Revenue):
═════════════════════════════════════════════════════════

Rank | Parameter          | Impact per unit | Elasticity
-----|-------------------|-----------------|----------
  1  | APAC_CAGR         | €267M per 1pp   | 18.8%
  2  | SA_CAGR           | €180M per 1pp   | 12.6%
  3  | Europe_CAGR       | €120M per 1pp   | 8.4%
  4  | Pharma_Revenue    | €85M per 5%     | 2.9%
  5  | NA_CAGR           | €75M per 1pp    | 5.2%
  6  | Capex_Budget      | €50M per 10%    | 1.8%

Key Insight: APAC CAGR has 3x more impact than Europe CAGR
             Focus board oversight on APAC execution
```

### Step 8: Generate Output Report

**Simple Output (Single Parameter):**
```
✅ SENSITIVITY ANALYSIS COMPLETE

Parameter: APAC_CAGR
Change: -1.5pp to +1.5pp

2035 REVENUE IMPACT:
  Downside: €2,450M (-14%)
  Base Case: €2,850M
  Upside: €3,250M (+14%)

Elasticity: €267M per 1pp CAGR change

Implication:
  • APAC execution is CRITICAL to strategy
  • 1% miss in APAC = €267M revenue miss in 2035
  • Recommend: Strong program management, quarterly tracking

File: data/customers/CompanyX/sensitivity_APAC_CAGR_20260115.csv
```

**Bulk Output (All Parameters):**
```
✅ SENSITIVITY ANALYSIS COMPLETE (All Parameters)

Total Parameters Tested: 12
Model Runtime: 45 seconds

TOP 5 MOST SENSITIVE PARAMETERS:
  1. APAC_CAGR: €267M per 1pp (18.8% elasticity)
  2. SA_CAGR: €180M per 1pp (12.6% elasticity)
  3. Europe_CAGR: €120M per 1pp (8.4% elasticity)
  4. Pharma_segment: €85M per 5% (2.9% elasticity)
  5. Headcount_cost: €62M per 5% (2.2% elasticity)

RECOMMENDED FOCUS AREAS:
  ⚠️ HIGH: Track APAC CAGR vs forecast (weekly)
  ⚠️ HIGH: Track SA CAGR vs forecast (weekly)
  ⚠️ MEDIUM: Track Europe CAGR vs forecast (monthly)

FILE OUTPUTS:
  ✓ data/customers/CompanyX/sensitivity_all_parameters.csv
  ✓ data/customers/CompanyX/sensitivity_ranking_table.csv
  ✓ data/customers/CompanyX/sensitivity_elasticity_chart.png

Next: /board-presentation to show risk analysis
```

---

## Output Formats

### Format 1: Table (Default)
```
╔════════════════════════════════════════╗
║ Parameter | Downside | Base | Upside  ║
╠════════════════════════════════════════╣
║ APAC_CAGR | €2,450M  | €2,850M | €3,250M ║
╚════════════════════════════════════════╝
```

### Format 2: CSV
```csv
Parameter,Unit,Downside_Value,Base_Case_Value,Upside_Value,Impact_Absolute,Impact_Percent,Elasticity
APAC_CAGR,pp,2450,2850,3250,400,14.0%,267
```

### Format 3: Chart (PNG)
Visualization showing:
- Downside/Base/Upside as bars
- Sensitivity curve (parameter vs impact)
- Elasticity annotations

---

## 10C CORE Mapping: Understanding Sensitivity Driver Dimensions (Phase 5)

**Purpose:** Identify which 10C CORE dimensions drive parameter sensitivity, enabling diagnosis and strategic response.

### Fundamental Insight

Every elasticity result maps to one or more 10C CORE dimensions:
- **WHERE (θ):** Parameter estimation uncertainty → how confident are we in the base value?
- **WHEN (Ψ):** Context sensitivity → which external factors drive the result?
- **WHAT:** Strategic utility dimension → which customer priorities are affected?
- **HOW (γ):** Complementarity → how do dependencies amplify/dampen the impact?

### Parameter-to-CORE Mapping

#### Type 1: Regional CAGR Changes → WHERE + WHEN

**CORE Dimensions:**
- **PRIMARY: WHERE** - Parameter uncertainty E(θ) on regional CAGR estimates
  - APAC_CAGR: E(θ) = ±1.5pp (±17.6% confidence width)
  - Europe_CAGR: E(θ) = ±1.2pp (±14.1%)
  - Result: Higher E(θ) → higher elasticity → need better data

- **SECONDARY: WHEN** - Context Ψ economic sensitivity
  - Ψ₁(Economic): Changes in GDP growth → alters regional CAGR assumptions
  - Ψ₂(Social): Market saturation → structural CAGR ceiling
  - Attribution: "Is sensitivity driven by parameter uncertainty or real market fragility?"

**Example Output - CORE Tagged:**
```
Parameter: APAC_CAGR -1.5pp to +1.5pp
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CORE-Driven Elasticity:
  [WHERE: ±1.5pp]      Parameter confidence interval (data quality issue)
  [WHEN: Ψ₁ Economic]   Economic cycle effects (external sensitivity)
  [WHEN: Ψ₂ Social]     Market saturation forces (structural trend)

Revenue Elasticity: €267M per 1pp CAGR change

INTERPRETATION:
  • €267M impact = Parameter uncertainty (WHERE) contributes 60%
  • €160M impact = Economic context (WHEN-Ψ₁) contributes 40%
  • Implication: If economy strengthens, APAC CAGR may exceed 8.5%
                 [WHEN-driven upside requires quarterly context tracking]
```

#### Type 2: Segment Revenue Changes → WHAT + WHERE

**CORE Dimensions:**
- **PRIMARY: WHAT** - Strategic utility dimension allocation to segment
  - Pharma segment → D(innovation), F(financial) dimensions
  - Commodity segment → F(financial) only
  - Result: Elasticity reflects strategic importance weight

- **SECONDARY: WHERE** - Parameter uncertainty in segment mix
  - Pharma growth assumptions: E(θ) = ±2.5%
  - If E(θ) is wide → elasticity is high → segment is strategically uncertain

**Example Output - CORE Tagged:**
```
Parameter: Pharma_Revenue +10% change
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CORE-Driven Elasticity:
  [WHAT: ω_D=0.20]      Pharma = 20% of strategic innovation utility
  [WHAT: ω_F=0.65]      Pharma = 65% of financial utility
  [WHERE: ±2.5%]        Pharma growth parameter uncertainty

Revenue Elasticity: €85M per 5% segment change (2.9%)

Complementarity Effects [HOW]:
  • Pharma volume ↑ → Capex intensity ↑ (γ_pharma-capex = 0.42)
    Additional impact: +€12M capex on €85M revenue lift
  • Pharma margin ↑ → Headcount elasticity ↓ (γ_pharma-org = 0.28)
    Partial offset: -€8M payroll on efficiency gains

INTERPRETATION:
  • Strategic: Pharma segment drives 30% of total revenue variability
  • Governance: Monitor via quarterly WHAT dimension framework
  • Dependency: Pharma-capex complementarity (γ=0.42) requires coordinated planning
```

#### Type 3: Headcount Cost Changes → HOW + WHERE

**CORE Dimensions:**
- **PRIMARY: HOW** - Complementarity γ between revenue and headcount
  - γ_rev-org = 0.68 (high synergy: revenue growth requires proportional hiring)
  - Result: Cost changes → cascading revenue impact via elasticity

- **SECONDARY: WHERE** - Parameter uncertainty in headcount elasticity
  - Headcount elasticity: E(θ) = ±0.08 (how tightly coupled is headcount to revenue?)
  - If E(θ) is wide → flexible staffing → lower elasticity

**Example Output - CORE Tagged:**
```
Parameter: Headcount_Cost +5% change
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CORE-Driven Elasticity:
  [HOW: γ_rev-org=0.68]  High revenue-headcount synergy (tightly coupled)
  [WHERE: E(θ)=±0.08]    Elasticity parameter confidence
  [HOW: γ_innovation-talent=0.75]  Innovation effectiveness dependent on talent

Payroll Impact: €62M per 5% cost increase (2.2% elasticity)

Complementarity Cascade [HOW-driven]:
  • Headcount quality ↑ (due to +5% spend) → Innovation capability ↑
    Additional impact: +€28M via faster product cycles (γ=0.75)
  • Headcount quality ↑ → Customer service ↑
    Additional impact: +€15M via reduced churn (γ=0.55)

Total Economic Impact: €62M direct + €43M indirect = €105M (3.7% elasticity)

INTERPRETATION:
  • HOW-driven: Complementarities amplify the direct cost impact by 70%
  • Strategic: Headcount investment is leverage point for value creation
  • Governance: Cost changes need synchronized INNOVATION & SERVICE tracking
```

#### Type 4: Capex Budget Changes → HOW + WHEN

**CORE Dimensions:**
- **PRIMARY: HOW** - Complementarity γ between capex initiatives and revenue/org
  - γ_capex-revenue = 0.62 (capex drives growth)
  - γ_capex-org = 0.48 (capex requires organizational capability to implement)
  - Result: Elasticity reflects synergy strength

- **SECONDARY: WHEN** - Context Ψ institutional (governance constraints)
  - Ψ₆(Institutional): Approval cycles, risk appetite → capex execution risk
  - Ψ₇(Technological): Tech cycle stage → ROI timing

**Example Output - CORE Tagged:**
```
Parameter: Capex_Budget +15% change
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CORE-Driven Elasticity:
  [HOW: γ_capex-revenue=0.62]    Capex-to-revenue synergy (execution risk: M)
  [HOW: γ_capex-org=0.48]        Organizational implementation capacity (bottleneck)
  [WHEN: Ψ₆ Institutional]       Governance approval cycles (6-12 month lag)
  [WHEN: Ψ₇ Technological]       Tech cycle readiness (obsolescence risk)

Direct Revenue Impact: +€50M per 10% capex
Synergy-Adjusted Impact: +€31M (accounting for γ_capex-org=0.48 organizational constraint)

Execution Risk Analysis [WHEN-Ψ₆]:
  • Q1-Q2 lag: Only 30% of capex deployed (governance approvals pending)
  • Q3-Q4 acceleration: 70% deployed (assumes org capacity)
  • Implication: €50M capex increase → only €15M impact in Year 1

ROI Timing [WHEN-Ψ₇]:
  • Digital capex: 18-month payoff (high Ψ₇)
  • Automation capex: 36-month payoff (medium Ψ₇)
  • Facility capex: 60-month payoff (low Ψ₇)

INTERPRETATION:
  • HOW-driven: Organizational capacity (γ=0.48) is the binding constraint
    → Recommendation: Invest in capability first, capex second
  • WHEN-driven: Governance lag (Ψ₆) creates execution risk
    → Recommendation: Front-load approvals; execute in Q1-Q2
  • Timeline: Expect 60% impact realization in Year 1, 100% by Year 3
```

### Composite Analysis: All Parameters Ranked by 10C Driver

**When running sensitivity analysis on ALL parameters, interpret results via CORE:**

```
Rank │ Parameter        │ Elasticity │ PRIMARY CORE │ SECONDARY     │ Action
─────┼──────────────────┼────────────┼──────────────┼───────────────┼─────────────────
  1  │ APAC_CAGR        │ 18.8%      │ WHERE (θ)    │ WHEN (Ψ₁econ) │ Improve APAC data
  2  │ SA_CAGR          │ 12.6%      │ WHERE (θ)    │ WHEN (Ψ₂soc)  │ Monitor social trends
  3  │ Europe_CAGR      │ 8.4%       │ WHERE (θ)    │ WHEN (Ψ₁econ) │ Quarterly tracking
  4  │ Pharma_segment   │ 2.9%       │ WHAT (ω_D)   │ WHERE (θ)     │ Rebalance portfolio
  5  │ Headcount_cost   │ 2.2%       │ HOW (γ)      │ WHERE (θ)     │ Invest in talent
  6  │ Capex_budget     │ 1.8%       │ HOW (γ)      │ WHEN (Ψ₆inst) │ Streamline governance
───┴──────────────────┴────────────┴──────────────┴───────────────┴──────────────────

Strategic Insight:
  • WHERE (parameter uncertainty) drives 70% of sensitivity
    → Need: Better data collection, calibration against quarterly actuals
    → Tool: quarterly_review.py decomposes ΔP into parameter vs context error

  • WHEN (context sensitivity) drives 20% of sensitivity
    → Need: Quarterly Ψ snapshot to detect context regime changes
    → Tool: intervention-manage close tracks Ψ dimensions for context shock attribution

  • HOW (complementarity) drives 7% of sensitivity
    → Need: Monitor γ values through outcome correlations
    → Tool: archetype_discovery.py learns γ from 3+ project outcomes

  • WHAT (strategic priorities) drives 3% of sensitivity
    → Need: Explicit WHAT dimension specification in customer onboarding
    → Tool: /new-customer captures ω_d weights during setup
```

### Integration with Learning Loop

**Sensitivity Analysis ↔ Quarterly Review Cycle:**

```
Q0: /apply-models CompanyX
    └─ Baseline elasticities recorded (WHERE: E(θ), HOW: γ)

Q1: Actual results come in
    └─ /intervention-manage close CompanyX --actuals Q1
       ├─ quarterly_review.py: Compare actual vs predicted
       ├─ ΔP decomposition: Identify WHERE vs WHEN vs HOW drift
       └─ If ΔP > threshold → need parameter update

Q2: /sensitivity-analysis CompanyX APAC_CAGR -1.5pp
    └─ Result includes CORE attribution:
       "€267M elasticity = 60% WHERE (parameter θ), 40% WHEN (Ψ economy)"

    └─ Cross-check with Q1 actual:
       If Q1 showed CONTEXT_SHOCK (Ψ changed):
         → Sensitivity explanation (WHEN-driven) predicts similar results
         → High confidence in forecast range

       If Q1 showed PARAMETER_ERROR (θ wrong):
         → Update E(θ) via parameter_update_pipeline.py
         → Rerun sensitivity with new WHERE confidence
         → Elasticity should shrink as E(θ) shrinks

Q3: After 3+ completed projects
    └─ archetype_discovery.py learns HOW patterns
       ├─ Clusters projects with similar γ profiles
       ├─ Infers γ values more precisely
       └─ Next customer in same archetype gets better HOW estimates
```

### Example: Complete CORE Analysis Session

**User Request:**
```
/sensitivity-analysis ALPLA APAC_CAGR -1.5pp
```

**Output (with 10C CORE Mapping):**
```
╔══════════════════════════════════════════════════════════════════════════╗
║ SENSITIVITY ANALYSIS: ALPLA | APAC_CAGR -1.5pp to +1.5pp              ║
║ 10C CORE-Tagged Analysis                                                  ║
╚══════════════════════════════════════════════════════════════════════════╝

1. PARAMETER CORE TAG [WHERE]:
   Base Assumption: APAC CAGR = 8.5%
   Uncertainty: E(θ) = ±1.5pp (typical range: 7.0% - 10.0%)
   Confidence: 1 - E(θ)/8.5% = 82% (medium-high confidence in base estimate)

   Question: How confident are we in 8.5%?
   → Check: Last quarterly_review.py output
   → ALPLA Q1-2025: Actual = 5.8%, Predicted = 8.5%, ΔP = -2.7pp
   → Finding: Parameter estimate was 2.7pp too high!
   → Implication: E(θ) should increase to ±2.0pp (not ±1.5pp)

2. REVENUE ELASTICITY [WHERE-driven]:
   Scenario Down (7.0% CAGR):   €2,450M (-€400M vs base, -14%)
   Scenario Base (8.5%):        €2,850M (baseline)
   Scenario Up (10.0%):         €3,250M (+€400M vs base, +14%)

   Elasticity: €267M per 1pp CAGR change
   Interpretation: "If APAC CAGR were 1pp lower, revenue drops €267M"

3. CONTEXT SENSITIVITY [WHEN-driven]:
   Ψ₁ (Economic): Current GDP growth = 2.1%
                  Historical range: 1.5% - 3.2%
                  Ψ₁ Sensitivity: ±0.7pp GDP → ±0.5pp APAC CAGR
                  Economic impact: €134M per 1pp GDP swing

   Ψ₂ (Social): Market maturity stage = Growth (not yet Mature)
                Risk: Saturation within 2 years if penetration > 60%
                Ψ₂ Impact: If saturation hits → CAGR drops to 4-5%

   Current Context Score: Ψ_avg = 0.73 (neutral-positive for growth)
   → Monitoring: Quarterly context update required (WHEN tracking)

4. COMPLEMENTARITY EFFECTS [HOW-driven]:
   γ_rev-org = 0.68: Revenue change → Headcount change

   If APAC CAGR increases 1.5pp → Revenue +€400M
   → Headcount grows to support revenue +€400M
   → Payroll cost increases by €24M (€400M × elasticity 6%)
   → Net income impact: €400M - €24M = €376M (offset: -6%)

5. STRATEGIC UTILITY [WHAT-driven]:
   APAC contribution to strategic dimensions:
   F (Financial): 0.55 (revenue weighted)
   D (Diversity): 0.15 (emerging market growth)
   S (Scale): 0.20 (volume opportunity)
   E/P/E: 0.10 (environmental/social/governance minimal)

   → APAC CAGR directly affects F (55% weight)
   → Less impact on D or S dimensions
   → Strategic priority: Maximize F (revenue) in APAC

6. GOVERNANCE IMPLICATIONS [HIERARCHY]:
   Decision Level: L2 (Regional P&L accountability)
   N_L2 formula: APAC requires ~45 coordinated L2 decisions
   Critical Decision: APAC growth target approval
   → Quarterly APAC CAGR tracking required (governance gate)
   → If actual < forecast: Trigger remediation at L1 level

SUMMARY TABLE:
┌─────────────────┬──────────────┬────────────┬──────────────┐
│ CORE Dimension  │ Sensitivity  │ Elasticity │ Implication  │
├─────────────────┼──────────────┼────────────┼──────────────┤
│ WHERE (θ)       │ ±1.5pp       │ €267M/1pp  │ Need better  │
│                 │ (May be too  │            │ data (Q1     │
│                 │ narrow; Q1   │            │ showed -2.7) │
│                 │ showed -2.7) │            │              │
├─────────────────┼──────────────┼────────────┼──────────────┤
│ WHEN (Ψ₁econ)   │ GDP ±0.7pp   │ €134M/1pp  │ Monitor Q1-Q2│
│                 │              │ GDP swing  │ econ outlook │
├─────────────────┼──────────────┼────────────┼──────────────┤
│ HOW (γ)         │ γ_rev-org    │ -€24M/€400 │ Revenue      │
│                 │ 0.68         │ revenue    │ growth        │
│                 │              │ (offset)   │ affordable    │
├─────────────────┼──────────────┼────────────┼──────────────┤
│ WHAT (ω_F)      │ F=55% weight │ 55% of     │ Strategic    │
│                 │              │ elasticity │ alignment:   │
│                 │              │ is F-driven│ APAC = core  │
└─────────────────┴──────────────┴────────────┴──────────────┘

FILES CREATED:
  ✓ sensitivity_APAC_CAGR_9c_analysis.json    [Machine-readable CORE tags]
  ✓ sensitivity_APAC_CAGR_elasticity.csv     [Standard output]
  ✓ sensitivity_APAC_CAGR_context_check.yaml [Ψ dimensions snapshot]

NEXT STEPS:
  1. Review Q1-2025 quarterly_review.py output (WHERE parameter drift)
  2. If ΔP decomposition = "PARAMETER_ERROR" → Update E(θ) ±2.0pp
  3. If ΔP decomposition = "CONTEXT_SHOCK" → Re-run sensitivity with new Ψ
  4. Track APAC CAGR weekly vs. quarterly forecast (governance gate)
```

**When to Use This Analysis:**

✓ **After quarterly review shows large ΔP:** Understand if it's WHERE (parameter) or WHEN (context)
✓ **During board discussions:** Show which CORE dimensions drive sensitivity → strategic focus
✓ **In risk planning:** Identify governance gates (HIERARCHY) for key parameters
✓ **For new customer setup:** Use CORE mapping to identify best comparable archetype

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Parameter not found | Typo or non-existent parameter | List valid parameters with /help |
| Invalid change value | Outside typical range | Warn but proceed; user confirms |
| Model execution failed | Bad assumptions | Validate assumptions in _assumptions.yaml |
| Company not found | Directory missing | Run /new-customer first |

---

## Integration with Other Skills

**Prerequisites:**
- /new-customer (create customer)
- /apply-models (run initial models)

**Following:**
- /board-presentation (show sensitivity analysis in board deck)

---

## FAQ

**Q: What's the difference between "elasticity" and "impact"?**
A: Impact = absolute change (€M)
   Elasticity = percentage sensitivity (% change per unit parameter change)

**Q: Can I test multiple parameters at once?**
A: Use `/sensitivity-analysis <company> all` for comprehensive scan

**Q: How do I interpret elasticity?**
A: Example: "APAC elasticity 18.8%" means
   If APAC CAGR changes 1pp, revenue changes ~18.8% (or €267M)

**Q: Should I store sensitivity results?**
A: Yes, automatically saved to data/customers/<company>/
   Use for board presentations and risk dashboards

---

**Skill Status:** ACTIVE
**Last Updated:** 2026-01-15
**Version:** 1.0.0
