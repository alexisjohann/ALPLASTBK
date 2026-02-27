# /apply-models Skill
## Run Strategic Models on Customer Data

**Purpose:** Execute model suite - Quick Mode (4 models) or Full Mode (31 models via ISO-1.0)

**Time Estimate:** 2-5 minutes (Quick) | 5-10 minutes (Full)

---

## Usage

```
/apply-models <company_name> [--full-run] [scenarios] [output_format]

Examples:
  /apply-models Company_XYZ                    # Quick Mode: 4 models
  /apply-models Company_XYZ --full-run         # Full Mode: 31 models (ISO-1.0)
  /apply-models Company_XYZ --full-run all     # Full Mode with all scenarios
  /apply-models ALPLA base pdf                 # Quick Mode with PDF output
```

### Execution Modes

| Mode | Flag | Models | Layers | Time |
|------|------|--------|--------|------|
| **Quick** | (default) | RPM, MCSM, OSM, CAM | 2 | 2-5 min |
| **Full** | `--full-run` | 31 models | 5 | 5-10 min |

### Full Mode (ISO-1.0 v1.3) - 5 Layers

```
Layer 1: Functional Strategy (7)   → VMV, CLV, CAC, HCM, SCO, RDM, ESG
Layer 2: Core Financial (10)       → RPM, OSM, CAM, CSM, PLM, WCM, CFM, DFM, BSM, BEM
Layer 3: Theoretical Foundation (5) → FEM, BFM, CMM, VAM, VCM
Layer 4: Strategic Analysis (5)    → MSM, MAM, PFM, STM, PRM
Layer 5: Simulation & Validation (4) → MCSM, SAM, SCM, ICM
```

---

## Workflow

### Phase 1: Load Configuration (< 5 seconds)

**Step 1.1: Locate Customer Files**
```bash
config_dir = data/customers/<company_name_lowercase>/
profile_file = <config_dir>/<company_name_lowercase>_profile.yaml
assumptions_file = <config_dir>/<company_name_lowercase>_assumptions.yaml
```

**Step 1.2: Validate Files Exist**
- Check _profile.yaml exists ✓
- Check _assumptions.yaml exists ✓
- Check _scenarios.yaml exists ✓

**Step 1.3: Load YAML Configurations**
```python
import yaml
profile = yaml.safe_load(open(profile_file))
assumptions = yaml.safe_load(open(assumptions_file))
```

**Step 1.4: Validate Parameters**
- Base revenue > 0 ✓
- Regional CAGRs within [-5%, 20%] ✓
- Headcount costs positive ✓
- Capex allocation sums to 100% ✓
- Run validation rules from model registry

**Step 1.5: Report Status**
```
✓ Configuration loaded
  - Company: <company_name>
  - Base Revenue: €<amount>M
  - Regions: <region_list>
  - CAGRs: <min%> to <max%>
  - Status: Ready to execute
```

---

### Phase 2: Execute Model 1 - Revenue Projection (RPM-1.0)

**Step 2.1: Run Revenue Model**
```python
from scripts.models.revenue_projection import project_revenue, calculate_summary_metrics

df_revenue = project_revenue(assumptions)
metrics_revenue = calculate_summary_metrics(df_revenue)
```

**Step 2.2: Output**
- Annual revenue projection (2024-2035)
- Regional breakdown
- YoY growth %
- Summary metrics:
  - Base year revenue
  - 2035 target revenue
  - Absolute growth (€M)
  - Growth %
  - Blended CAGR

**Step 2.3: Validation**
- Revenue 2035 > 2024 ✓
- CAGR within [-5%, 20%] ✓
- All values positive ✓

**Example Output:**
```
Revenue Projection Model (RPM-1.0) - COMPLETE ✓
  2024 Revenue: €1,500M
  2035 Target: €2,850M
  Growth: +€1,350M (+90%)
  CAGR: 6.7%
  Status: Saved to data/customers/<company>/revenue_projection_2024_2035.csv
```

---

### Phase 3: Execute Model 2 - Monte Carlo Simulation (MCSM-1.0)

**Step 3.1: Run Monte Carlo (10,000 simulations)**
```python
from scripts.models.monte_carlo_simulation import run_monte_carlo

results_mc = run_monte_carlo(
  config=assumptions,
  revenue_df=df_revenue,
  num_simulations=10000,
  confidence_level=0.95
)
```

**Step 3.2: Output - Percentile Distribution**
```
Percentile  | 2035 Revenue (€M) | % of Base Case
------------|-------------------|---------------
1%          | 2,150             | 75%
5%          | 2,450             | 86%
25%         | 2,700             | 95%
50% (Median)| 2,850             | 100%
75%         | 3,000             | 105%
95%         | 3,200             | 112%
99%         | 3,400             | 119%
```

**Step 3.3: Output - Probability Metrics**
```
Key Metrics:
  Mean: €2,850M (Base case)
  Std Dev: €280M
  95% Confidence Interval: [€2,450M - €3,200M]
  Probability of exceeding base case: 50.0%
  Probability of exceeding Conservative (5th %ile): 95.0%
  Downside risk (below €2,400M): 5.0%
  Upside potential (above €3,200M): 5.0%
```

**Step 3.4: Validation**
- Mean ≈ base case ✓
- 95% CI symmetric ✓
- Probabilities sum to 100% ✓

**Example Output:**
```
Monte Carlo Simulation (MCSM-1.0) - COMPLETE ✓
  Simulations: 10,000
  Confidence Level: 95%
  Mean 2035 Revenue: €2,850M
  95% CI: [€2,450M - €3,200M]
  Probability Base Case Achievable: 50%
  Status: Saved to data/customers/<company>/monte_carlo_distribution.csv
```

---

### Phase 4: Execute Model 3 - Organizational Scaling (OSM-1.0)

**Step 4.1: Run Headcount Model**
```python
from scripts.models.organizational_scaling import project_headcount, calculate_payroll

result_org = project_headcount(assumptions)
df_headcount = result_org['headcount_projection']
df_payroll = result_org['payroll_projection']
```

**Step 4.2: Output - Headcount Evolution**
```
Year | Operations | Sales | IT | R&D | Other | Total  | YoY%
-----|------------|-------|----|----|-------|--------|------
2024 | 2,500      | 800   | 200| 150| 1,350 | 5,000  | —
2026 | 2,700      | 900   | 280| 180| 1,440 | 5,500  | 5.0%
2029 | 3,200      | 1,100 | 400| 220| 1,680 | 6,600  | 4.8%
2035 | 3,800      | 1,400 | 550| 280| 2,070 | 8,100  | 4.0%
```

**Step 4.3: Output - Payroll Projection**
```
Year | Headcount | Avg Cost/Employee | Annual Payroll | % of Revenue
-----|-----------|-------------------|----------------|-------------
2024 | 5,000     | €60K              | €300M          | 20.0%
2026 | 5,500     | €62K              | €341M          | 19.5%
2029 | 6,600     | €66K              | €435M          | 18.6%
2035 | 8,100     | €72K              | €583M          | 20.4%
```

**Step 4.4: Output - Regional Distribution**
```
Region        | 2024  | 2035  | Growth | Growth %
--------------|-------|-------|--------|----------
Europe        | 2,500 | 2,800 | +300   | +12%
Asia-Pacific  | 1,500 | 3,200 | +1,700 | +113%
South America | 800   | 1,200 | +400   | +50%
Other         | 200   | 900   | +700   | +350%
TOTAL         | 5,000 | 8,100 | +3,100 | +62%
```

**Example Output:**
```
Organizational Scaling Model (OSM-1.0) - COMPLETE ✓
  2024 Headcount: 5,000
  2035 Target: 8,100
  Growth: +3,100 (+62%)
  2024 Payroll: €300M (20% of revenue)
  2035 Payroll: €583M (20.4% of revenue)
  Status: Saved to data/customers/<company>/headcount_projection.csv
```

---

### Phase 5: Execute Model 4 - Capex Allocation (CAM-1.0)

**Step 5.1: Run Capex Model**
```python
from scripts.models.capex_allocation import project_capex

result_capex = project_capex(assumptions)
df_capex = result_capex['annual_capex']
roi_analysis = result_capex['roi_analysis']
```

**Step 5.2: Output - Annual Capex Roadmap**
```
Year | ERP | IoT | Data | Recycling | Geo Exp | Maintenance | Total
-----|-----|-----|------|-----------|---------|-------------|-------
2025 | €8M | €2M | €3M  | €3M       | €3M     | €60M        | €79M
2026 | €6M | €3M | €4M  | €3M       | €3M     | €62M        | €81M
2027 | €7M | €5M | €2M  | €20M      | €15M    | €45M        | €94M
2028 | €7M | €5M | €2M  | €15M      | €15M    | €46M        | €90M
2035 | €4M | €8M | €1M  | €8M       | €8M     | €20M        | €49M
-----|-----|-----|------|-----------|---------|-------------|-------
TOTAL| €35M| €25M| €15M | €60M      | €60M    | €295M       | €490M
```

**Step 5.3: Output - ROI Analysis**
```
Initiative      | Capex | Expected Benefits | ROI %  | Payback
----------------|-------|-------------------|--------|--------
ERP             | €35M  | €150M             | 328%   | 4 years
IoT             | €25M  | €80M              | 220%   | 3 years
Data Platform   | €15M  | €100M             | 567%   | 2 years
Recycling       | €60M  | €200M             | 233%   | 5 years
Geographic Exp  | €60M  | €350M             | 483%   | 6 years
Maintenance     | €295M | €100M             | 34%    | 3 years
----------------|-------|-------------------|--------|--------
TOTAL           | €490M | €980M             | 100%   | 4.5 years
```

**Example Output:**
```
Capex Allocation Model (CAM-1.0) - COMPLETE ✓
  Total 11-Year Capex: €490M
  Annual Average: €44.5M
  Expected Benefits: €980M
  Total ROI: 100% (2.0x return)
  Weighted Payback: 4.5 years
  Status: Saved to data/customers/<company>/capex_roadmap.csv
```

---

### Phase 6: Aggregate and Consolidate Results

**Step 6.1: Create Summary Dashboard**
```
EXECUTIVE SUMMARY - <Company Name>
════════════════════════════════════════════════════════════

[1] REVENUE TRAJECTORY
    2024: €1,500M
    2035: €2,850M
    Growth: +90% (+€1,350M)
    CAGR: 6.7%
    Confidence (95% CI): [€2,450M - €3,200M]

[2] ORGANIZATIONAL GROWTH
    2024 Headcount: 5,000
    2035 Headcount: 8,100
    Growth: +62% (+3,100)
    2024 Payroll: €300M (20% revenue)
    2035 Payroll: €583M (20.4% revenue)

[3] CAPITAL INVESTMENT
    Total 11-Year Capex: €490M
    Annual Average: €44.5M (3.0% of avg revenue)
    Expected Benefits: €980M
    ROI: 100%
    Payback: 4.5 years

[4] MONTE CARLO CONFIDENCE
    Base Case Probability: 50%
    Downside Risk: 5% (below €2,450M)
    Upside Potential: 5% (above €3,200M)
    ═════════════════════════════════════════════════════
```

**Step 6.2: Update Customer Database**
- Save revenue_projection_2024_2035.csv
- Save monte_carlo_distribution.csv
- Save headcount_projection_2024_2035.csv
- Save payroll_projection_2024_2035.csv
- Save capex_roadmap_2024_2035.csv
- Update _scenarios.yaml with calculated values
- Create summary_metrics.yaml

**Step 6.3: Generate Completion Report**
```
✅ ALL MODELS EXECUTED SUCCESSFULLY

Execution Time: 2m 43s
Models Run: 4/4
  ✓ RPM-1.0 (Revenue Projection)
  ✓ MCSM-1.0 (Monte Carlo Simulation)
  ✓ OSM-1.0 (Organizational Scaling)
  ✓ CAM-1.0 (Capex Allocation)

Outputs Created:
  ✓ data/customers/<company>/revenue_projection_2024_2035.csv
  ✓ data/customers/<company>/monte_carlo_distribution.csv
  ✓ data/customers/<company>/headcount_projection_2024_2035.csv
  ✓ data/customers/<company>/payroll_projection_2024_2035.csv
  ✓ data/customers/<company>/capex_roadmap_2024_2035.csv
  ✓ data/customers/<company>/summary_metrics.yaml

Next Steps:
  1. Review results: Are they reasonable?
  2. Run sensitivity analysis: /sensitivity-analysis <company> <parameter>
  3. Generate board presentation: /board-presentation <company>
  4. For detailed analysis: Check CSV files in data/customers/<company>/

Documentation: See data/models/README.md for model details
```

---

## 🎯 NEW: 10C CORE Foundation Output (Phase 5)

Starting with this release, `/apply-models` now outputs explicit 10C CORE dimension analysis showing how strategic models operationalize the EBF framework.

### 10C Foundation Section

When you run `/apply-models CompanyX`, you now see:

```
═══════════════════════════════════════════════════════════════════
10C CORE FOUNDATION ANALYSIS
═══════════════════════════════════════════════════════════════════

[1] HIERARCHY (Decision Stratification)
    N_L2 Formula: α·γ_avg × n × (1-m) / log(n)
    ├─ Parameters: n=2500 (headcount), α=1.0, γ_avg=0.65, m=0.3
    ├─ Result: N_L2 ≈ 180 coordinated L2 decisions required
    ├─ Governance Gates:
    │  ├─ L0 (System): Strategic direction (Board, 1-2 decisions/year)
    │  ├─ L1 (Strategic): Capex budget, M&A (Board+CFO, 5-10/year)
    │  ├─ L2 (Tactical): Project approval, pricing (BU Leaders, ~180/year)
    │  └─ L3 (Operative): Daily execution (Managers, 1000s/year)
    └─ Strategic Coherence Index (SCI): 0.94 (strong alignment)

[2] HOW (Complementarity Matrix)
    Revenue-Headcount: γ = 0.68 (strong complement)
    │  ├─ Insight: Revenue growth demands proportional headcount
    │  └─ Implication: RPM and OSM outputs must stay synchronized
    │
    Innovation-Talent: γ = 0.75 (high synergy)
    │  ├─ Insight: R&D requires capable workforce
    │  └─ Implication: RDM + HCM recommendations should align
    │
    Capex-Training: γ = 0.55 (moderate synergy)
    │  ├─ Insight: New systems require workforce training
    │  └─ Implication: CAM capex should include training budget
    │
    Value Creation Formula: V = Σ E(d) + Σ γ_ij·√(E(d)·E(d'))
    └─ Portfolio synergy potential: €250M (from γ interactions)

[3] WHEN (Context Snapshot - Ψ Dimensions)
    Ψ₁ Economic:       0.75 (growth market, positive outlook)
    Ψ₂ Social:         0.65 (labor market tight, wage pressure)
    Ψ₃ Temporal:       0.70 (seasonal, cyclical patterns)
    Ψ₄ Spatial:        0.85 (geographic diversity, multi-region)
    Ψ₅ Institutional:  0.60 (regulatory stable, compliance OK)
    Ψ₆ Cultural:       0.80 (innovation-friendly, change-ready)
    Ψ₇ Technological:  0.85 (digital transformation urgency)
    Ψ₈ Environmental:  0.55 (carbon pricing coming, ESG pressure)

    Impact: Parameter sensitivities adjusted for Ψ profile
    └─ Result: Regional CAGRs vary ±0.5pp based on Ψ_tech + Ψ_econ

[4] WHERE (Parameter Uncertainty & Confidence)
    Regional CAGR:
    ├─ Europe:         2.5% ± 1.0pp  [E(θ) confidence = 87%]
    ├─ APAC:           8.5% ± 1.5pp  [E(θ) confidence = 85%]
    ├─ Americas:       3.0% ± 1.2pp  [E(θ) confidence = 84%]
    └─ Blended:        6.2% ± 1.1pp  [E(θ) confidence = 85%]

    Headcount Elasticity: 0.65 ± 0.05  [E(θ) = 92% confidence]
    Capex Intensity:      3.5% ± 0.4pp [E(θ) = 88% confidence]

    Note: Confidence intervals shrink by ~5% per quarter with new observations
    └─ Learning Loop: quarterly_review.py updates E(θ) automatically

[5] WHAT (Strategic Utility Dimension Weights)
    Financial (F):     ω = 0.50  (primary driver)
    Development (D):   ω = 0.20  (capability building)
    Social (S):        ω = 0.15  (stakeholder value)
    Physical (P):      ω = 0.10  (operational excellence)
    Emotional (E):     ω = 0.03  (brand/culture)
    Existential (X):   ω = 0.02  (purpose/legacy)

    Interpretation:
    ├─ 50% weight on Financial means profit-focused strategy
    ├─ 20% on Development implies high R&D + talent investment
    └─ 15% on Social suggests stakeholder-inclusive model

[6] INTEGRATION SUMMARY
    ├─ WHO (Aggregation): Firm-level with 180 L2 decisions
    ├─ WHAT (Dimensions): Multi-objective, financial-led
    ├─ HOW (Synergies): High complementarity (γ_avg=0.65)
    ├─ WHEN (Context): Mixed conditions (Ψ_avg=0.71)
    ├─ WHERE (Certainty): Good baseline (E(θ) ~87%)
    ├─ AWARE: See monitoring → all metrics < 50% aware
    ├─ READY: Decision threshold θ=0.70 → WAX check shows 0.85 (ready)
    └─ STAGE: Transformation phase S=0.5 → mid-execution

    Next Step: /sensitivity-analysis CompanyX all --with-cores
    This shows which 10C dimensions drive each model's outputs
═══════════════════════════════════════════════════════════════════
```

### 10C Output Files

When you run `/apply-models`, three new files are created:

1. **9c_foundation_analysis.json**
   - Machine-readable 10C snapshot
   - Used by /board-presentation for "10C Foundation" slide
   - Used by archetype_discovery.py for pattern clustering

2. **model_interdependencies.yaml**
   - Shows which 10C CORE affects each model
   - Tracks data flow: RPM→OSM→CAM→MCSM
   - Links to model_registry.yaml for theoretical foundation

3. **parameter_confidence_tracking.json**
   - Historical E(θ) values
   - Shrinkage tracking (how confidence improves with data)
   - Used by parameter_update_pipeline.py for learning loop

### Integration with Learning Loop

The 10C Foundation output enables the full learning loop:

```
1. /apply-models CompanyX
   ↓ (saves predictions + 10C snapshot)

2. [Quarterly execution and actual outcomes]
   ↓

3. /intervention-manage close CompanyX_2025
   ↓ (runs quarterly_review.py)

4. quarterly_review.py
   ├─ Loads 10C snapshot from step 1
   ├─ Decomposes ΔP (Actual - Predicted) via 10C dimensions
   │  ├─ Parameter error: Which Θ was wrong?
   │  ├─ Context shock: Did Ψ change?
   │  └─ Model error: Functional form issue?
   └─ Calls parameter_update_pipeline.py (updates E(θ))

5. After 3+ projects:
   ├─ archetype_discovery.py runs automatically
   └─ Clusters similar (Ψ, WHAT, HOW, γ) profiles

6. Next customer with similar profile:
   └─ /new-customer --archetype FFF-TECH-APAC
      (starts with better E(θ), converges faster)
```

---

## Full Mode Workflow (ISO-1.0 Orchestrator)

When `--full-run` flag is used, the ISO-1.0 Integrated Strategy Orchestrator executes:

### Full Mode Execution

```python
from scripts.models.integrated_strategy_orchestrator import run_integrated_strategy

results = run_integrated_strategy(
    company_name="<company_name>",
    base_revenue=<from_assumptions>,
    industry="<from_profile>",
    full_run=True,  # 31 models
    verbose=True
)
```

### Full Mode Output

```
✅ ISO-1.0 FULL RUN COMPLETE

Execution Time: 8m 12s
Models Run: 31/31 across 5 Layers

LAYER 1: FUNCTIONAL STRATEGY (7 models)
  ✓ VMV-1.0 Vision-Mission-Values (Strategic Identity)
  ✓ CLV-1.0 Customer Lifetime Value
  ✓ CAC-1.0 Customer Acquisition Cost
  ✓ HCM-1.0 Human Capital Model
  ✓ SCO-1.0 Supply Chain Optimization
  ✓ RDM-1.0 R&D Investment Model
  ✓ ESG-1.0 ESG Scoring Model

LAYER 2: CORE FINANCIAL (10 models)
  ✓ RPM-1.0 Revenue Projection
  ✓ OSM-1.0 Organizational Scaling
  ✓ CAM-1.0 Capex Allocation
  ✓ CSM-1.0 Cost Structure Model
  ✓ PLM-1.0 Profit & Loss Model
  ✓ WCM-1.0 Working Capital Model
  ✓ CFM-1.0 Cash Flow Model
  ✓ DFM-1.0 Debt & Financing Model
  ✓ BSM-1.0 Balance Sheet Model
  ✓ BEM-1.0 Break-Even Model

LAYER 3: THEORETICAL FOUNDATION (5 models)
  ✓ FEM-1.0 Fehr Economic Model
  ✓ BFM-1.0 Behavioral Finance Model
  ✓ CMM-1.0 Capital Market Model
  ✓ VAM-1.0 Valuation Model
  ✓ VCM-1.0 Value Creation Model (EVA, ROIC)

LAYER 4: STRATEGIC ANALYSIS (5 models)
  ✓ MSM-1.0 Market Share Model
  ✓ MAM-1.0 M&A Model
  ✓ PFM-1.0 Portfolio Model
  ✓ STM-1.0 Strategic Planning Model
  ✓ PRM-1.0 Performance Review Model

LAYER 5: SIMULATION & VALIDATION (4 models)
  ✓ MCSM-1.0 Monte Carlo Simulation
  ✓ SAM-1.0 Sensitivity Analysis Model
  ✓ SCM-1.0 Scenario Model
  ✓ ICM-1.0 Integration Check Model

Summary:
  - Enterprise Value (VAM): €X.XXB
  - 2035 Revenue (RPM): €X.XXB
  - CLV/CAC Ratio: X.Xx
  - ESG Score: XX/100
  - Monte Carlo 95% CI: [€X.XB - €X.XB]
```

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Customer not found | Directory doesn't exist | Run /new-customer first |
| Missing _assumptions.yaml | File not created | Check _profile.yaml; templates may have defaults |
| Invalid CAGR values | < -5% or > 20% | Run with warning; user must validate |
| Revenue calculation failed | Negative or invalid inputs | Check regional allocations sum to 100% |
| Monte Carlo convergence failed | 10,000 simulations insufficient | Retry or use 20,000 simulations |
| ISO-1.0 layer dependency error | Missing upstream model results | Check layer execution order |

---

## Integration with Other Skills

**Prerequisites:**
- /new-customer must be run first (to create customer directory)
- Customer must have _assumptions.yaml with regional CAGRs

**Following Skills:**
- /sensitivity-analysis (test parameter changes)
- /board-presentation (generate output for board)

---

## Performance & Resources

| Metric | Quick Mode | Full Mode (ISO-1.0) |
|--------|------------|---------------------|
| Runtime | 2-5 min | 5-10 min |
| Models executed | 4 | 30 |
| CPU cores used | 2-4 | 4-8 |
| Memory peak | 500 MB - 1 GB | 1-2 GB |
| Disk usage (outputs) | 5-10 MB | 15-25 MB |

---

## Technical Details

**Quick Mode Implementation:**
- Sequential execution of 4 core models (RPM, MCSM, OSM, CAM)
- Parallel processing where possible (Monte Carlo)
- YAML input validation before each model
- DataFrame aggregation and CSV export

**Full Mode Implementation (ISO-1.0):**
- 5-layer architecture with automatic dependency resolution
- Data flows between layers: CLV→CAC, HCM→CSM, SCO→WCM, ESG→CMM, BFM→CMM→VAM
- All 31 models executed in correct order
- Comprehensive summary with cross-model insights

**Dependencies:**

Quick Mode:
- scripts/models/revenue_projection.py
- scripts/models/monte_carlo_simulation.py
- scripts/models/organizational_scaling.py
- scripts/models/capex_allocation.py

Full Mode (ISO-1.0):
- scripts/models/integrated_strategy_orchestrator.py (master orchestrator)
- All v1.0-v4.0 model files

---

**Skill Status:** ACTIVE
**Last Updated:** 2026-01-16
**Version:** 2.0.0
