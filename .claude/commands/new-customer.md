# /new-customer Skill
## Create New Strategic Customer Database

**Purpose:** Rapidly set up a new strategic customer in the model library (30 seconds)

**Time Estimate:** < 30 seconds

---

## Usage

```
/new-customer <company_name> <base_revenue_eur_m> <regions> [--template <industry>]

Examples:
  /new-customer "Company XYZ" 1500 "Europe,APAC,South America"
  /new-customer "TechCorp" 2500 "North America,Europe,APAC" --template manufacturing
  /new-customer "RetailCo" 800 "Europe" --template retail
  /new-customer "BankAG" 5000 "Europe,APAC" --template financial_services
```

### Available Templates

| Template | File | Industry | Key Characteristics |
|----------|------|----------|---------------------|
| `manufacturing` | manufacturing.yaml | B2B Manufacturing | High capex, global ops, 5% CAGR |
| `retail` | retail.yaml | Retail/E-Commerce | Low margin, inventory, 6% CAGR |
| `financial_services` | financial_services.yaml | Banking/Finance | Regulated, IT-heavy, 4% CAGR |

Templates provide pre-configured defaults for:
- Financial benchmarks (margins, growth, capex intensity)
- Organizational structure (headcount distribution)
- Regional growth patterns
- Model parameters (CLV, CAC, Monte Carlo, Valuation)
- ESG defaults
- Risk profiles

---

## Workflow

### Step 1: Validate Inputs
- Company name: non-empty string ✓
- Base revenue: positive integer/float (€M) ✓
- Regions: valid comma-separated list ✓
- Template (optional): valid industry template ✓

### Step 1b: Load Template (if --template specified)
```python
# Load industry template
template_path = f"data/templates/industries/{template}.yaml"
if template:
    with open(template_path) as f:
        industry_defaults = yaml.safe_load(f)
    # Extract defaults:
    # - financial_benchmarks (CAGR, margins, capex)
    # - organizational_benchmarks (headcount distribution)
    # - regional_defaults (growth rates by region)
    # - model_parameters (CLV, CAC, Monte Carlo, Valuation)
```

### Step 2: Create Directory Structure
```bash
mkdir -p data/customers/<company_name_lowercase>/
```

### Step 3: Generate Company Profile
Create `<company_name_lowercase>_profile.yaml` with:
- Company metadata (name, base revenue, regions, business model)
- Financial baseline (2024)
- Geographic footprint template
- Organization template (placeholder)

**Template Content:**
```yaml
customer:
  name: "<company_name>"
  base_revenue_2024_eur_m: <base_revenue>
  regions: [<comma_separated_regions>]
  business_model: "B2B Manufacturing / Service Provider"

  geographic_presence:
    countries: "TBD (to be updated)"
    regions: []  # Populated from input

  organization:
    total_employees: "TBD"

  metadata:
    database_version: "1.0.0"
    created_date: "2026-01-15"
    status: "INITIALIZED"
```

### Step 4: Generate Assumptions Template
Create `<company_name_lowercase>_assumptions.yaml` with:
- Regional growth rates (from template or ALPLA defaults)
- Organizational cost assumptions (from template)
- Capex framework (from template or placeholder)
- Business segment mix

**Without Template (defaults):**
```yaml
strategic_assumptions:
  regional_growth_rates:
    [REGION]:
      cagr: 4.0  # Default: 4% (placeholder - user must update)
      revenue_2024_eur_m: <calculated from allocation>
      rationale: "PLACEHOLDER - Update with market research"
```

**With Template (e.g., --template manufacturing):**
```yaml
strategic_assumptions:
  industry: "manufacturing"
  template_version: "1.0.0"

  financial_benchmarks:
    revenue_growth_rate: 0.05      # From template
    ebitda_margin: 0.10            # From template
    gross_margin: 0.30             # From template
    capex_to_revenue: 0.05         # From template

  regional_growth_rates:
    Europe:
      cagr: 3.0                    # From template regional_defaults
      revenue_share: 0.45
    APAC:
      cagr: 8.0                    # From template (higher growth)
      revenue_share: 0.25

  organizational:
    revenue_per_employee: 200000   # From template
    payroll_cost_per_fte: 60000    # From template
    headcount_distribution:        # From template
      operations: 0.45
      sales_service: 0.12
      it: 0.03
      # ...

  model_parameters:
    clv:
      avg_customer_lifetime_years: 8    # From template
      retention_rate: 0.90
    monte_carlo:
      revenue_volatility: 0.08          # From template
      cost_volatility: 0.05
    valuation:
      wacc: 0.08                        # From template
      ev_ebitda_multiple: 8.0
```

### Step 5: Generate Scenario Template
Create `<company_name_lowercase>_scenarios.yaml` with:
- Conservative scenario (CAGR -1.5pp)
- Base case scenario (user inputs)
- Optimistic scenario (CAGR +1.5pp)

**Example:**
```yaml
scenarios:
  conservative:
    scenario_name: "Conservative Path"
    regional_cagr_adjustments: "All regions -1.5pp"
    status: "CALCULATED (run /apply-models to populate)"

  base_case:
    scenario_name: "Base Case"
    status: "AWAITING PARAMETER INPUT"

  optimistic:
    scenario_name: "Optimistic Path"
    regional_cagr_adjustments: "All regions +1.5pp"
    status: "CALCULATED (run /apply-models to populate)"
```

### Step 6: Initialize Other Database Files
Create (empty/template) placeholders for:
- `<company_name_lowercase>_roadmap.yaml`
- `<company_name_lowercase>_kpis.yaml`
- `<company_name_lowercase>_dependencies.yaml`

### Step 7: Confirmation Output

**Without Template:**
```
✅ NEW CUSTOMER INITIALIZED

Company: <company_name>
Base Revenue (2024): €<base_revenue>M
Regions: <region_list>
Template: None (using defaults)

Files Created:
  ✓ data/customers/<company_lowercase>/
  ✓ <company_lowercase>_profile.yaml
  ✓ <company_lowercase>_assumptions.yaml
  ✓ <company_lowercase>_scenarios.yaml
  ✓ <company_lowercase>_roadmap.yaml (placeholder)
  ✓ <company_lowercase>_kpis.yaml (placeholder)
  ✓ <company_lowercase>_dependencies.yaml (placeholder)

Next Steps:
  1. ⚠️ Edit assumptions: Provide regional CAGRs, headcount cost, capex parameters
  2. Run models: /apply-models <company_name>
  3. Run sensitivity: /sensitivity-analysis <company_name> <parameter> <change>
  4. Generate board presentation: /board-presentation <company_name>
```

**With Template:**
```
✅ NEW CUSTOMER INITIALIZED

Company: <company_name>
Base Revenue (2024): €<base_revenue>M
Regions: <region_list>
Template: manufacturing (v1.0.0)

Pre-Configured Parameters:
  ✓ Revenue CAGR: 5.0%
  ✓ EBITDA Margin: 10.0%
  ✓ Capex/Revenue: 5.0%
  ✓ WACC: 8.0%
  ✓ Regional growth rates: Europe 3%, APAC 8%, Americas 5%

Files Created:
  ✓ data/customers/<company_lowercase>/
  ✓ <company_lowercase>_profile.yaml
  ✓ <company_lowercase>_assumptions.yaml (template-populated)
  ✓ <company_lowercase>_scenarios.yaml
  ✓ <company_lowercase>_roadmap.yaml (placeholder)
  ✓ <company_lowercase>_kpis.yaml (placeholder)
  ✓ <company_lowercase>_dependencies.yaml (placeholder)

Next Steps:
  1. ✅ Assumptions pre-filled (review and adjust if needed)
  2. Run models: /apply-models <company_name> --full-run
  3. Run sensitivity: /sensitivity-analysis <company_name> all
  4. Generate board presentation: /board-presentation <company_name>
```

Documentation: See data/customers/README.md for detailed parameter specs

---

## Template Reference Values

For template population, use these reference values from ALPLA:

| Metric | ALPLA | Typical Range | Note |
|--------|-------|---------------|------|
| Base Revenue (2024) | €4.9B | €500M - €50B | User input |
| Regional CAGR | 2.5%-8.5% | -5% to +20% | Must be customized |
| Headcount Cost | €35-85K | €30-100K | By function & region |
| Capex % Revenue | ~1% | 0.5%-3% | By industry |
| Payroll % Revenue | ~27% | 20%-35% | By industry |

---

## Input Validation Rules

| Rule | Check | Action if Fail |
|------|-------|---|
| Company name not empty | len(name) > 0 | REJECT with error |
| Revenue > 0 | revenue > 0 | REJECT with error |
| Regions valid | each region in [Europe, APAC, SA, NA, AMET, ...] | WARN + suggest alternatives |
| Revenue in realistic range | €100M - €100B | WARN (proceed with confirmation) |

---

## Error Handling

```
ERROR: Company name already exists
  → data/customers/<company_name_lowercase>/ already exists
  → Suggest: /new-customer "Company XYZ v2" or manually delete first

ERROR: Invalid revenue value
  → Revenue must be positive number
  → Example: /new-customer "CompanyX" 2500 "Europe,APAC"

ERROR: Invalid region
  → Region '<region>' not in valid list
  → Valid regions: Europe, Asia-Pacific, South America, North America, AMET
  → Example: /new-customer "CompanyX" 2500 "Europe,APAC"

ERROR: Invalid template
  → Template '<template>' not found
  → Valid templates: manufacturing, retail, financial_services
  → Template files located in: data/templates/industries/
  → Example: /new-customer "CompanyX" 2500 "Europe" --template manufacturing
```

---

## Output Files Summary

After execution, customer directory contains:

| File | Purpose | Status | Next Action |
|------|---------|--------|-------------|
| _profile.yaml | Company metadata | Template populated | Edit with actual company info |
| _assumptions.yaml | Model parameters | Placeholders | **MUST UPDATE** before models |
| _scenarios.yaml | Scenario definitions | Template | Auto-calculated by /apply-models |
| _roadmap.yaml | Implementation plan | Empty template | Populate after models run |
| _kpis.yaml | Tracking metrics | Empty template | Populate after models run |
| _dependencies.yaml | Cross-functional map | Empty template | Populate after analysis |

---

## Integration with Other Skills

**After /new-customer:**
```
1. Edit _assumptions.yaml manually (provide actual CAGRs, costs, etc.)
2. Run: /apply-models <company_name>
   → Calculates revenue, headcount, capex, Monte Carlo
3. Run: /sensitivity-analysis <company_name> <parameter> <change>
   → Tests impact of changes
4. Run: /board-presentation <company_name>
   → Generates board-ready output
```

---

## Technical Details

**Implementation:**
- Creates directories with mkdir -p
- Generates YAML files using Python/Jinja2 templating
- Validates all inputs before file creation
- Atomic operation (all or nothing)

**Performance:**
- Runtime: < 1 second
- Disk usage: ~100 KB per customer

**Dependencies:**
- /apply-models (to populate scenarios and models)
- /sensitivity-analysis (for what-if analysis)
- /board-presentation (for output generation)

---

## FAQ

**Q: Can I create multiple customers?**
A: Yes, unlimited. Each gets separate directory in data/customers/

**Q: What if I make a mistake in company name?**
A: You can manually delete the directory and run /new-customer again
OR create with corrected name and ignore old one

**Q: Can I import existing customer data?**
A: Yes, manually place YAML files in the directory and run /apply-models

**Q: What if my company has 10+ regions?**
A: Supported via comma-separated list. Consolidate into 5-6 main regions for analysis

---

## Success Criteria

✅ Skill execution successful if:
- [ ] Customer directory created in data/customers/
- [ ] All 6 YAML files present and valid
- [ ] Files contain template structure (not errors)
- [ ] User can proceed to /apply-models without edits (will use templates)
- [ ] Confirmation message shows file locations

---

**Skill Status:** ACTIVE
**Last Updated:** 2026-01-16
**Version:** 2.0.0

## Changelog

**v2.0.0 (2026-01-16):**
- Added `--template` flag for industry-specific defaults
- Templates available: manufacturing, retail, financial_services
- Pre-populates assumptions with industry benchmarks
- Regional growth rates auto-configured from template
