# /replicate-customer Skill
## Replicate Customer Model from Template (Complete in 4-6 Hours)

**Purpose:** Fast-track customer setup by cloning & adapting from ALPLA template

**Time Estimate:** 4-6 hours (vs. 2+ weeks of independent analysis)

---

## Usage

```
/replicate-customer <source_company> <new_company> [fast_track]

Examples:
  /replicate-customer ALPLA "Company XYZ"
  /replicate-customer ALPLA "TechCorp" fast
  /replicate-customer ALPLA "ManufactureCo" detailed
```

---

## What Gets Replicated

### Source: ALPLA Template (Production-Tested)
The ALPLA database is the "golden template" containing:
- ✓ 7 complete YAML database files
- ✓ 4 validated strategic models
- ✓ 3-phase implementation roadmap
- ✓ 25 KPI metrics
- ✓ 7 strategic dependencies
- ✓ 10 worked examples
- ✓ Board-ready presentation

### Replication Scope
**What gets copied (and adapted):**
- ✓ File structure & templates
- ✓ Model registry references
- ✓ Scenario frameworks
- ✓ Roadmap phase structure
- ✓ KPI definitions & governance
- ✓ Dependency mapping methodology

**What you must customize:**
- ⚠️ Company-specific parameters (revenue, growth rates, costs)
- ⚠️ Regional focus & market dynamics
- ⚠️ Business segments & competitive positioning
- ⚠️ Organizational structure & headcount mix
- ⚠️ Strategic priorities & phasing

---

## Workflow

### Phase 1: Source Analysis (30 min)

**Step 1.1: Analyze Target Company**
```
Questions to answer:
1. Industry/Business Model?
   ❍ Manufacturing (like ALPLA)
   ❍ Services
   ❍ Technology
   ❍ Other

2. Company Size?
   - Revenue €[X]M (ALPLA: €4,900M)
   - Headcount [X]K (ALPLA: 24.3K)
   - Geographic reach [X] countries

3. Growth Stage?
   - Mature/stable (like ALPLA)
   - Growth mode
   - Turnaround

4. Strategic Priority?
   - Geographic expansion
   - Digital transformation
   - Organic growth
   - Sustainability

5. Planning Horizon?
   - 11 years (like ALPLA) or different?
```

**Step 1.2: Assess Fit with ALPLA Template**
```
Compatibility Matrix:

Fit Dimension        | ALPLA Template | Your Company | Fit Score
-------------------|----------------|---|----------
Business Model      | Manufacturing  | ? | ?
Geographic Multi    | 5 regions      | ? | ?
Org Complexity      | 24K employees  | ? | ?
Growth Stage        | Mature/growth  | ? | ?
Capex Requirements  | Yes (high)     | ? | ?
Multi-segment       | Yes (4 segments)| ? | ?

Overall Template Fit: [LOW/MEDIUM/HIGH]
  LOW (< 40%): Limited reuse, start from scratch
  MEDIUM (40-70%): Selective reuse, customize heavily
  HIGH (70%+): Strong template fit, light customization
```

**Output: Fit Assessment Report**
```
✓ TEMPLATE FIT ASSESSMENT

Company: TechCorp
Size: €2.5B revenue, 8K employees (vs ALPLA €4.9B, 24.3K)
Growth: 8% CAGR targeted (vs ALPLA 6.9%)
Model Fit: MEDIUM-HIGH (72%)

Recommendations:
  ✓ Use ALPLA template as baseline
  ⚠️ Customize for smaller headcount
  ⚠️ Adjust segment mix (5 segments instead of 4)
  ✓ Keep 3-phase roadmap structure
  ⚠️ Reduce capex scope (-30% from ALPLA)

Estimated Replication Time: 5 hours
```

---

### Phase 2: Directory & File Setup (15 min)

**Step 2.1: Create Customer Directory**
```bash
source_dir = data/customers/ALPLA/
target_dir = data/customers/TechCorp/

mkdir -p target_dir
```

**Step 2.2: Copy Files from ALPLA**
```bash
Copy from data/customers/ALPLA/ to data/customers/TechCorp/:

✓ alpla_profile.yaml
  → techcorp_profile.yaml (update company data)

✓ alpla_assumptions.yaml
  → techcorp_assumptions.yaml (update market parameters)

✓ alpla_scenarios.yaml
  → techcorp_scenarios.yaml (template for scenarios)

✓ alpla_roadmap.yaml
  → techcorp_roadmap.yaml (adjust phases & milestones)

✓ alpla_kpis.yaml
  → techcorp_kpis.yaml (keep framework, adjust targets)

✓ alpla_dependencies.yaml
  → techcorp_dependencies.yaml (keep structure, adjust roles)

✓ alpla_models_registry_link.md
  → techcorp_models_registry_link.md (reference only)
```

---

### Phase 3: Profile Customization (1-2 hours)

**Step 3.1: Update Company Profile**

Edit `techcorp_profile.yaml`:
```yaml
customer:
  name: "TechCorp"  # ← Changed from ALPLA
  full_name: "TechCorp AG"  # ← New
  business_type: "SaaS / Cloud Services"  # ← Changed from Manufacturing

  # Update these sections:
  financial_2024:
    revenue_eur_m: 2500  # ← Changed from 4900
    estimated_ebitda_eur_m: 375  # ← Recalculate (15% vs 10%)
    estimated_ebitda_margin_percent: 15  # ← 10% for ALPLA

  geographic_presence:
    countries: 12  # ← Changed from 46
    regions:
      - name: "Europe"
        countries: 5
        revenue_eur_m: 1250
        revenue_percent: 50
      - name: "North America"
        countries: 3
        revenue_eur_m: 625
        revenue_percent: 25
      - name: "Asia-Pacific"
        countries: 4
        revenue_eur_m: 500
        revenue_percent: 20
      # Removed AMET (not relevant for TechCorp)

  organization:
    total_employees: 8000  # ← Changed from 24,350
    breakdown_by_function: [UPDATE]
    breakdown_by_region: [UPDATE]
```

**Step 3.2: Validate Profile Completeness**
```
✓ Company name & type
✓ Financial baseline (revenue, margin)
✓ Regions (≥2, ≤10 realistic for replication)
✓ Headcount & cost structure
✓ Business segments
✓ Competitive positioning
```

---

### Phase 4: Assumptions Customization (2-3 hours) ⚠️ CRITICAL

**Step 4.1: Update Regional Growth Rates**

This is THE most important step. Get market research for:
```yaml
strategic_assumptions:
  regional_growth_rates:

    europe:
      cagr: 6.0  # ← UPDATE: Based on EU SaaS growth (+/- ALPLA 2.5%)
      revenue_2024_eur_m: 1250
      rationale: "Mature European cloud market, 6% growth"

    apac:
      cagr: 12.0  # ← UPDATE: High-growth Asian tech markets
      revenue_2024_eur_m: 500
      rationale: "India, Japan AI/ML adoption driving growth"

    north_america:
      cagr: 8.5  # ← UPDATE: Strong US cloud adoption
      revenue_2024_eur_m: 625
      rationale: "Leadership position in North America"
```

**Research Sources for CAGRs:**
- Gartner/IDC industry forecasts
- Competitor annual reports
- Analyst coverage
- Management guidance
- Historical growth (if available)

**Step 4.2: Update Organizational Costs**

```yaml
headcount_costs_by_region:
  europe:
    avg_cost_per_employee_eur_k: 85  # ← SaaS pays more than manufacturing
    rationale: "Tech talent premium"

  north_america:
    avg_cost_per_employee_eur_k: 150  # ← US tech salaries very high
    rationale: "San Francisco/Seattle salary market"

  apac:
    avg_cost_per_employee_eur_k: 55  # ← Lower cost but premium for tech
    rationale: "India tech hubs"

  # Adjust function-specific costs (IT salaries higher in SaaS)
  it_digital:
    base_avg_cost_eur_k: 120  # ← vs 85K in manufacturing
    escalation_percent_per_year: 6.0  # ← vs 5% (tighter market)
```

**Step 4.3: Update Capex Assumptions**

```yaml
capex_framework:
  total_capex_11_years_eur_m: 250  # ← vs 550M for ALPLA (5x smaller)
  annual_average_capex_eur_m: 23  # ← vs 50M

  distribution_by_initiative:
    # SaaS priorities differ from manufacturing
    cloud_infrastructure:
      total_eur_m: 60  # ← NEW for SaaS (not in ALPLA)
    data_analytics:
      total_eur_m: 40  # ← Higher priority than manufacturing
    ai_ml_development:
      total_eur_m: 50  # ← NEW for SaaS
    geographic_expansion:
      total_eur_m: 50  # ← Similar to ALPLA
    # Remove or reduce: recycling, manufacturing capacity
```

**Validation Checklist:**
```
✓ Regional CAGRs source-backed
✓ Headcount costs benchmarked
✓ Capex allocation realistic (% of revenue)
✓ Segment mix reflects business model
✓ Payroll % revenue typical for industry
```

---

### Phase 5: Scenario Setup (30 min)

**Step 5.1: Define 3 Base Scenarios**

Edit `techcorp_scenarios.yaml`:
```yaml
scenarios:

  conservative:
    scenario_name: "Conservative Path"
    regional_cagr_adjustments: "All regions -2pp"
    # Auto-calculated by models based on reduced CAGRs

  base_case:
    scenario_name: "Base Case"
    regional_cagr_adjustments: "None (use assumptions CAGRs)"
    # Primary scenario for board recommendation

  optimistic:
    scenario_name: "Optimistic Path"
    regional_cagr_adjustments: "All regions +2pp"
    # Upside case with favorable execution
```

---

### Phase 6: Model Execution (30 min)

**Step 6.1: Run All Models**
```bash
/apply-models TechCorp
```

**Output:**
```
✅ ALL MODELS EXECUTED - TechCorp

Revenue: €2.5B (2024) → €5.2B (2035), 7.2% CAGR
Headcount: 8.0K → 12.5K (+56%)
Capex: €250M total (€23M/year)
Monte Carlo: 95% confidence in base case

Models Generated:
  ✓ revenue_projection_2024_2035.csv
  ✓ monte_carlo_distribution.csv
  ✓ headcount_projection_2024_2035.csv
  ✓ payroll_projection_2024_2035.csv
  ✓ capex_roadmap_2024_2035.csv
```

---

### Phase 7: Validation & QA (1 hour)

**Step 7.1: Sanity Checks**
```
Validation Checklist:

Revenue:
  ☐ 2035 revenue > 2024? YES ✓
  ☐ CAGR between -5% and 20%? [X]% ✓
  ☐ Growth aligns with market forecasts? YES ✓

Headcount:
  ☐ 2035 headcount > 2024? YES ✓
  ☐ Growth reasonable for business? [X]% ✓
  ☐ Payroll % revenue typical? [Y]% ✓

Capex:
  ☐ Annual capex < revenue? YES ✓
  ☐ ROI positive? [X]% ✓
  ☐ Payback < 7 years? YES ✓

Monte Carlo:
  ☐ 95% CI symmetric around median? YES ✓
  ☐ Probability base case = ~50%? [X]% ✓
```

**Step 7.2: Benchmark vs. Peers**
```
Compare outputs to:
  - Industry benchmarks (growth rates, margins)
  - Competitor financials
  - Analyst forecasts

Example:
  TechCorp 7.2% CAGR vs SaaS industry avg 8.5%
  → Reasonable (slightly below peer, conservative)
```

---

### Phase 8: Final Assembly (30 min)

**Step 8.1: Roadmap & KPIs**

Update `techcorp_roadmap.yaml` with:
- Phase timelines (keep 3-phase structure, adjust if needed)
- Key milestones (cloud migration, geographic expansion, etc.)
- Decision gates (board checkpoints)

Update `techcorp_kpis.yaml` with:
- KPI targets (adjusted for 2035 revenue, headcount)
- Tracking cadence (monthly, quarterly)
- Variance thresholds (±3% warning, ±5% critical)

**Step 8.2: Generate Board Presentation**
```bash
/board-presentation TechCorp pdf
```

**Output:**
```
✅ Board presentation generated
File: data/customers/techcorp/board_presentation_20260115.pdf

10 slides ready for board meeting:
  ✓ Executive summary (€2.5B → €5.2B)
  ✓ 3 scenarios (Conservative, Base, Optimistic)
  ✓ Monte Carlo confidence
  ✓ Regional drivers
  ✓ Org scaling
  ✓ Capex & ROI
  ✓ 3-phase roadmap
  ✓ Sensitivity analysis
  ✓ Competitive position
  ✓ Board recommendation
```

---

### Phase 9: Commit & Documentation (30 min)

**Step 9.1: Create Documentation**
```
Create techcorp_REPLICATION_LOG.md:
  - What was changed from ALPLA template
  - Why (market research, business model)
  - Data sources used
  - QA validation results
```

**Step 9.2: Commit to Git**
```bash
git add data/customers/techcorp/
git commit -m "feat(Customer): Replicate TechCorp from ALPLA template

- Base revenue: €2.5B (vs €4.9B ALPLA)
- Regional CAGRs: 6-12% (vs 2.5-8.5% ALPLA)
- Headcount: 8K → 12.5K (vs 24.3K → 38.5K ALPLA)
- Capex: €250M (vs €550M ALPLA)
- Models: All 4 executed, validated vs industry benchmarks
- Output: Board-ready presentation (10 slides)

Replication time: 5.5 hours (vs 2+ weeks independent)
"
```

---

## Time Breakdown

| Phase | Task | Time |
|-------|------|------|
| 1 | Source analysis & fit assessment | 0.5h |
| 2 | Directory & file setup | 0.25h |
| 3 | Profile customization | 1.5h |
| 4 | Assumptions customization ⚠️ CRITICAL | 2.5h |
| 5 | Scenario setup | 0.5h |
| 6 | Model execution | 0.5h |
| 7 | Validation & QA | 1.0h |
| 8 | Final assembly | 0.5h |
| 9 | Commit & documentation | 0.5h |
| **TOTAL** | | **7.75h** |

**Typical Replication:** 4-6 hours (if similar business model)
**Challenging Replication:** 8-10 hours (if different industry)

---

## FAQ

**Q: Can I replicate from other customers (not ALPLA)?**
A: Yes, use any completed customer as source
   ALPLA recommended as "golden template"

**Q: What if my company is very different from ALPLA?**
A: Still beneficial for framework/structure
   But more customization needed (assumptions especially)
   Fit score < 40% → consider starting fresh

**Q: How do I know if replication is worth it?**
A: If fit score > 50% → replication saves time
   If fit score < 40% → start from scratch

**Q: Can I update the template later?**
A: Yes, models recalculate automatically
   Run /apply-models again with updated parameters

---

## Success Criteria

✅ Replication successful if:
- [ ] Fit assessment completed
- [ ] Profile & assumptions customized
- [ ] All 4 models executed without errors
- [ ] Validation checklist passed
- [ ] Board presentation generated
- [ ] Committed to git with documentation
- [ ] Time: < 8 hours (vs 2+ weeks)

---

**Skill Status:** ACTIVE
**Last Updated:** 2026-01-15
**Version:** 1.0.0
