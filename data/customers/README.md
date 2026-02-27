# ALPLA Customer Model Database
## Single Source of Truth for Strategic Planning & Execution

**Database Version:** 1.1 (v54 Compatible)
**Last Updated:** 2026-01-20
**Maintained By:** Strategic Analysis Team
**Framework:** EBF v54 with Intervention Design & UNTCM Model

---

## Overview

This customer database serves as the **single source of truth** for all ALPLA strategic models, assumptions, scenarios, and execution roadmaps. It integrates insights from 7 comprehensive strategic documents into a queryable, auditable YAML-based system.

### Why This Database?

1. **Consolidation:** All strategic models, parameters, and assumptions in one place
2. **Auditability:** Every number, assumption, and decision is documented with source links
3. **Replicability:** Template-based structure enables application to other customers
4. **Execution Tracking:** KPIs and roadmap enable quarterly monitoring
5. **Scenario Comparison:** Real-time sensitivity analysis across Conservative/Base/Optimistic scenarios

---

## Database Structure (7 Files)

### File 1: `alpla_profile.yaml`
**Purpose:** Customer metadata and strategic context
**Owner:** Strategic Planning

**Contains:**
- Company profile (ALPLA: €4.9B revenue, 24,350 employees, 46 countries)
- Geographic footprint (200 plants across 5 regions)
- Business segments (Beverage 40%, Pharma 20%, Industrial 25%, Recycled Materials 15%)
- Competitive positioning (3rd globally, unique vertical integration advantage)
- Strategic vision 2035 (€9.9B revenue, +101% growth)

**Key Sections:**
- Corporate structure & ownership (family-owned, Austrian)
- Financial profile (2024 baseline)
- Production assets (200 plants, 13 recycling, 68 in-house)
- Organization (24,350 → 38,500 employees)
- Core competencies (vertical integration, recycling, pharma expertise)
- Certifications & partnerships (Paboco JV, PLANETA JV)

**Use Cases:**
- Customer onboarding presentations
- Competitive analysis
- Stakeholder communication

---

### File 2: `alpla_models.yaml`
**Purpose:** Registry of all validated strategic models
**Owner:** Strategic Planning

**Contains:**
- **10 strategic models** across Tier 1, 2, 3:
  - Tier 1 CORE: SOCM-1.0, OrgModel-1.0
  - Tier 2 FUNCTIONAL: DigitalStrategy-1.0, HRStrategy-1.0, SalesStrategy-1.0
  - Tier 3 TOOLS: SOCM-MonteCarlo-1.0, RevenueProjection-1.0, DashboardTool-1.0

**Each Model Entry Includes:**
- Model ID & version
- Status (VALIDATED, APPROVED, IMPLEMENTED)
- Description of strategic value
- Framework/dimensions used
- Validation approach
- Source documents (links to Markdown reports)

**Key Metrics per Model:**
- SOCM: 6 strategic options, 6 evaluation dimensions, complementarity effects (γ)
- OrgModel: 3 phases, headcount evolution 24.3K → 38.5K
- DigitalStrategy: €95M capex, ERP/IoT/Data/Cybersecurity pillars
- HRStrategy: €1.58B → €2.70B payroll, 14,150 net hires
- SalesStrategy: €5.0B incremental revenue across 5 channels

**Use Cases:**
- Model governance (what's approved, what's in development)
- Audit trail (model versions, approval dates)
- Cross-referencing models

---

### File 3: `alpla_assumptions.yaml`
**Purpose:** Parametric foundation for all models
**Owner:** CFO & Strategic Planning

**Contains 9 Assumption Sections:**

1. **Regional Growth Rates (2024-2035 CAGR %)**
   - Asia-Pacific: 8.5% (€740M → €1,600M)
   - Africa/Middle East: 8.0% (€240M → €500M)
   - South America: 6.5% (€980M → €1,700M)
   - North America: 4.5% (€740M → €1,100M)
   - Europe: 2.5% (€2,200M → €2,700M)
   - Portfolio CAGR: 6.9%

2. **Organizational Costs (by region & function)**
   - APAC: €35K/employee (lower-cost labor)
   - Europe: €65K/employee (developed market)
   - IT/Digital: €85K + 5% escalation/year (tight market)
   - Operations: €45K + 3% escalation/year

3. **Capex Framework (€550M total, €50M/year average)**
   - ERP S/4HANA: €35M (4-year payback)
   - IoT deployment: €25M (3-year payback)
   - Data platform: €15M (3-year payback)
   - Cybersecurity: €20M (risk mitigation)
   - Recycling expansion: €60M
   - Geographic expansion: €60M
   - Maintenance capex: €335M

4. **Business Segment Assumptions**
   - Beverage: 40% → 28% (€1.96B → €2.8B), 3.5% CAGR
   - Pharma: 20% → 20% (€0.98B → €2.0B), 8.5% CAGR (high growth)
   - Industrial: 25% → 21% (€1.23B → €2.1B), 5.0% CAGR
   - Recycled Materials: 15% → 20% (€0.74B → €2.0B), 12% CAGR (strategic)

5. **Pricing & Margin Strategy**
   - Annual price escalation: 2.5%
   - Sustainability premium: 5-10% on recycled content
   - Pharma premium: 4.1x vs commodity (€3.50/kg vs €0.85/kg)
   - EBITDA margin evolution: 10.2% → 12.0%

6. **Market & Competitive Assumptions**
   - Global packaging market CAGR: 3.5%
   - Circular economy market CAGR: 15% (high growth)
   - ALPLA market share: 1.1% → 1.6% (45% market share gain)
   - Competitive advantage vs peers: 4.0x (ALPLA 6.9% CAGR vs Amcor 1.7%, Berry 1.0%)

7. **Digital & Innovation Assumptions**
   - ERP coverage: 1.3% → 95% (240 plants by 2035)
   - IoT coverage: 0% → 80% (200 plants by 2035)
   - Expected digital benefits: €500M over 11 years

8. **Sustainability Assumptions**
   - EU regulatory: Plastic tax €0.80/kg (2026), 25% recycled content (2025), 35% (2030)
   - Carbon neutral by 2035 (60% reduction)
   - Advanced recycling: 350K → 700K tonnes/year

9. **Risk & Downside Assumptions**
   - Downside scenario CAGR: 4.2% (€8.7B target)
   - Upside scenario CAGR: 7.3% (€11.1B target)
   - Key risks: commodity volatility (±20%), geopolitical, tech execution

**Use Cases:**
- Sensitivity analysis (change an assumption, re-calculate revenue)
- Benchmarking (compare assumptions to other customers)
- Model audits (trace numbers back to source)

---

### File 4: `alpla_scenarios.yaml`
**Purpose:** Strategic scenario modeling and Monte Carlo analysis
**Owner:** CFO & Strategic Planning

**Contains 3 Strategic Scenarios + Monte Carlo:**

1. **Conservative Scenario (€8.7B by 2035, 5.8% CAGR)**
   - Lower capex, defensive positioning
   - Recommendation: NOT RECOMMENDED
   - Risk: Misses market opportunity
   - Probability of success: 65%

2. **Base Case Scenario (€9.9B by 2035, 6.9% CAGR) ✅ RECOMMENDED**
   - Balanced growth across regions & segments
   - Strategic portfolio: CE 40%, INNOV 20%, BIO 30%, SCALE 10%
   - Achievable with €50M/year capex
   - Probability of success: 82%
   - Recommended by board: APPROVED (2025-12-28)

3. **Optimistic Scenario (€11.1B by 2035, 8.0% CAGR)**
   - Aggressive capex, market acceleration
   - Recommendation: CONSIDER FOR DISCUSSION
   - Risk: Elevated execution risk
   - Probability of success: 65%

4. **Monte Carlo Stochastic Analysis (10,000 simulations)**
   - Base case distribution: Mean €9.9B, Std Dev €850M
   - Confidence interval: €8.7B (5th %ile) - €11.1B (95th %ile)
   - Probability exceeds conservative: 97.9%
   - Probability exceeds €10B: 45.5%
   - Key sensitivity: Asia-Pacific CAGR (±€0.4B per ±1% CAGR)

**Each Scenario Includes:**
- Financial projections (revenue, EBITDA, margins)
- Regional breakdown
- Capex investment
- Headcount evolution
- Organizational implications
- Phase milestones
- Strengths & weaknesses
- Risk factors
- Board assessment

**Use Cases:**
- Board presentations (show 3 scenarios)
- Sensitivity analysis (what if Asia-Pac CAGR drops 1%?)
- Risk management (probability of exceeding base case)
- Decision-making (Monte Carlo confidence in base case recommendation)

---

### File 5: `alpla_roadmap.yaml`
**Purpose:** 3-phase implementation plan with quarterly milestones
**Owner:** Strategic Planning Office & PMO

**Contains 3 Phases + 36 Quarterly Milestones:**

1. **Phase 1: Foundation & Acceleration (2025-2026)**
   - Duration: 24 months
   - Revenue target: €5.3B (4% CAGR)
   - Capex budget: €180M (€90M/year average)
   - Headcount target: 27,400 (+3,050 net hires)
   - Key objectives: ERP pilot, Recycling scale-up, APAC setup, Paboco series production

   **Q1-Q4 2025 Milestones:**
   - Q1: Thailand plant go-live, APAC MD onboard, ERP vendor selection
   - Q2: Thailand 100% capacity, ERP pilot design phase, Paboco series production
   - Q3: ERP build phase 50%, India pharma hub construction, 25% recycled content achieved
   - Q4: ERP UAT complete, India pharma operational, Egypt market entry

   **Q1-Q2 2026 Milestones:**
   - Q1: ERP Thailand go-live, Egypt pharma JV signed, South Africa market entry
   - Q2: ERP Germany go-live, Mexico recycling operationalized
   - Q3: ERP Mexico go-live, AMET regional structure complete
   - Q4: Phase 1 complete, board approval for Phase 2 plan

2. **Phase 2: Expansion & Scaling (2027-2029)**
   - Duration: 36 months
   - Revenue target: €7.0B (6% CAGR)
   - Capex budget: €230M (€77M/year average)
   - Headcount target: 32,500 (+5,100 net hires)
   - Key objectives: APAC footprint expansion (3-5 plants), AMET hub, recycling 500K tonnes, PEF commercialization

   **Key Milestones:**
   - Q1 2027: Vietnam construction 50%, India pharma expansion approved
   - Q2 2027: Vietnam operational, India location finalized
   - Q1 2028: South Africa recycling operational, recycling 500K tonnes
   - Q4 2029: Phase 2 complete, revenue €7.0B achieved, Phase 3 plan approved

3. **Phase 3: Optimization & Maturation (2030-2035)**
   - Duration: 60 months
   - Revenue target: €9.9B (7% CAGR)
   - Capex budget: €140M (€23M/year average)
   - Headcount target: 38,500 (+6,000 net hires)
   - Key objectives: AMET at scale, Paboco profitability, advanced recycling mature, ERP 95% coverage

   **Key Milestones:**
   - Q1 2030: Paboco profitability achieved, ERP 67% coverage
   - Q2 2034: Revenue €9.5B+ (on track)
   - Q4 2035: Phase 3 complete, revenue €9.9B achieved, CAGR 6.9% validated

**Governance Components:**
- Steering committee (monthly during active phases)
- Board oversight (quarterly)
- Decision gates (strategic go/no-go points)
- KPI dashboard (25 metrics tracked)
- Risk contingencies (3 critical cascades)

**Use Cases:**
- Project management (what milestones are due when)
- Board reporting (quarterly progress vs roadmap)
- Decision-making (gate reviews, go/no-go decisions)
- Risk management (contingency triggers)

---

### File 6: `alpla_kpis.yaml`
**Purpose:** Strategic KPI framework for execution monitoring
**Owner:** Strategic Planning Office

**Contains 6 KPI Tiers (25 Total Metrics):**

1. **Tier 1: Strategic Financial KPIs (3 metrics)**
   - Total Revenue (monthly reporting, €4.9B → €9.9B)
   - EBITDA Margin % (monthly, 10.2% → 12.0%)
   - Organic Growth % (quarterly, 3.5% → 6.5%)

2. **Tier 2: Operational KPIs (7 metrics)**
   - Total Headcount (monthly, 24,350 → 38,500)
   - Capex Investment (monthly tracking vs budget)
   - Recycling Capacity (quarterly, 350K → 700K tonnes)
   - ERP Plant Coverage (quarterly, 1.3% → 95%)
   - IoT Plant Coverage (quarterly, 0% → 80%)

3. **Tier 3: Strategic Initiative KPIs (5 metrics)**
   - Asia-Pacific Revenue (€740M → €1,600M)
   - Africa/Middle East Revenue (€240M → €500M)
   - Paboco Production Units (0 → 500M/year)
   - Recycled Materials Revenue (€735M → €1,100M)

4. **Tier 4: Capability KPIs (3 metrics)**
   - Executive Retention (target 95%)
   - Critical Role Turnover (target <10%)
   - IT/Digital Talent Hiring (target 700 over 11 years)

5. **Tier 5: Customer & Market KPIs (3 metrics)**
   - Global Market Share (1.1% → 1.6%)
   - Top 20 Account Concentration (60% → 65%)
   - Customer Retention Rate (target 95%)

6. **Tier 6: Sustainability & ESG KPIs (3 metrics)**
   - Recycled Content % (18% → 35%)
   - Carbon Reduction Index (0% → 60% by 2035)
   - Waste to Landfill (target 0% by 2030)

**Reporting Architecture:**
- Monthly executive dashboard (CEO, CFO, COO, Regional CEOs)
- Quarterly board report (all Tier 1 KPIs + strategic initiative progress)
- Monthly steering committee dashboard
- Functional scorecards (by department)

**Use Cases:**
- Monthly board reporting
- Quarterly variance analysis
- Executive dashboard
- KPI trend tracking
- Risk identification (when KPIs miss thresholds)

---

### File 7: `alpla_dependencies.yaml`
**Purpose:** Cross-functional integration map showing strategy interdependencies
**Owner:** Strategic Planning & Steering Committee

**Contains 7 Strategic Dependencies + Governance:**

1. **Digital → Sales (Supply chain visibility enables APAC expansion)**
   - ERP enables real-time inventory tracking
   - Demand forecasting improves sales effectiveness
   - Customer 360 platform enables personalization
   - Revenue impact: €150-200M by 2035

2. **HR → Digital (Talent enables transformation execution)**
   - IT specialist acquisition critical (700 people over 11 years)
   - Change management enables ERP adoption
   - Failure scenario: Lack of talent → implementation delays 6-12 months

3. **Sales → HR + Digital (Revenue funds investment)**
   - €50M annual capex funded from EBITDA growth
   - €1.3B payroll over 11 years funded from revenue
   - Virtuous cycle: Growth → Capex → Capability → More Growth

4. **Circular Economy (Cross-functional integration)**
   - Digital: Track recycled material flows, carbon accounting
   - HR: 50-100 advanced recycling specialists
   - Sales: Premium pricing on recycled materials (+5-10%)
   - Revenue at stake: €1.1B by 2035

5. **Geographic Expansion (APAC/AMET)**
   - Sales opens markets (customer pre-commitment)
   - HR builds regional leadership
   - Digital infrastructure (ERP, IoT) for operations
   - Failure cascade: If HR can't hire → market entry delayed

6. **Paboco Innovation**
   - R&D capability (50+ scientists)
   - Sales commercialization (500M units/year)
   - Digital tracking (quality, production)
   - Revenue at stake: €100-200M by 2035

7. **Advanced Recycling Scaling**
   - HR: Hire specialists (50-100 engineers)
   - Sales: Build customer base (700K tonnes demand)
   - Digital: Track quality, traceability
   - Revenue at stake: €100M EBITDA

**Critical Path Analysis:**
- Phase 1 critical path: HR recruitment → Sales customer lock-in → Ops plant ramp → Digital ERP
- If any critical activity delayed → cascade failures

**Risk Cascades (3 major):**
- Cascade 1: Sales revenue miss → Plant underutilized → Digital ROI lower
- Cascade 2: HR talent miss → APAC strategy stalls → €300M revenue at risk
- Cascade 3: Digital delays → No supply chain visibility → Operations chaos

**Use Cases:**
- Steering committee oversight (what depends on what?)
- Risk management (cascade analysis)
- Execution tracking (when one initiative fails, what else breaks?)
- Resource prioritization (which dependencies are most critical?)

---

## How to Use This Database

### 1. **For Board Presentations**
```
Step 1: Pull alpla_profile.yaml → Company overview slide
Step 2: Pull alpla_scenarios.yaml → 3 scenarios (Conservative/Base/Optimistic)
Step 3: Pull alpla_roadmap.yaml → 3-phase implementation plan
Step 4: Pull alpla_kpis.yaml → Board-level KPI dashboard
Output: Professional board presentation ready in 30 minutes
```

### 2. **For Quarterly Board Reviews**
```
Step 1: Compare actual results vs alpla_kpis.yaml targets
Step 2: Calculate variances (Warning if ±3%, Critical if ±5%)
Step 3: Check milestone status against alpla_roadmap.yaml
Step 4: Update alpla_models.yaml with any model changes
Step 5: Re-run Monte Carlo if assumptions changed (alpla_assumptions.yaml)
Output: Board-ready variance report + risk escalations
```

### 3. **For Sensitivity Analysis**
```
Step 1: Modify alpla_assumptions.yaml (e.g., APAC CAGR: 8.5% → 7.5%)
Step 2: Recalculate using alpla_scenarios.yaml logic
Step 3: Output: Revenue impact = -€0.4B by 2035
Example: "If APAC CAGR misses by 1pp, base case revenue drops to €9.5B"
```

### 4. **For Capex Prioritization**
```
Step 1: Review alpla_roadmap.yaml Phase 1 milestones
Step 2: Map to alpla_dependencies.yaml (which capex enables what?)
Step 3: Identify critical path activities
Step 4: Prioritize: Digital → HR → Sales (dependency sequence)
Output: Capex prioritization aligned with execution risks
```

### 5. **For Risk Management**
```
Step 1: Review alpla_dependencies.yaml risk cascades
Step 2: Identify triggering events (e.g., "APAC revenue <€50M")
Step 3: Define mitigation (e.g., "pre-commit customer before plant opens")
Step 4: Monitor via alpla_kpis.yaml (escalation thresholds)
Output: Proactive risk monitoring + early warning system
```

### 6. **For Execution Tracking (PMO)**
```
Step 1: Quarterly review alpla_roadmap.yaml milestones
Step 2: Update completion status (on-track, at-risk, completed)
Step 3: Compare vs alpla_kpis.yaml (KPI variance analysis)
Step 4: Escalate missed milestones via alpla_dependencies.yaml cascade analysis
Output: Project status report + risk indicators
```

### 7. **Replicating for New Customer**
```
Step 1: Copy alpla_profile.yaml → new_customer_profile.yaml (modify company data)
Step 2: Copy alpla_assumptions.yaml → new_customer_assumptions.yaml (modify market data)
Step 3: Copy alpla_scenarios.yaml → reuse logic with new assumptions
Step 4: Copy alpla_roadmap.yaml → modify phases for customer timeline
Step 5: Copy alpla_kpis.yaml → reuse KPI framework
Step 6: Copy alpla_dependencies.yaml → reuse dependency structure
Output: New customer database in 4-6 hours (vs 2+ weeks of analysis)
```

---

## Database Governance

### Maintenance & Updates
- **Review Cycle:** Quarterly (Q1, Q2, Q3, Q4)
- **Next Full Review:** 2026-04-15
- **Maintained By:** Strategic Analysis Team
- **Approval Authority:** Board of Directors

### Change Control
- All material assumption changes require CFO + CEO sign-off
- New model versions require board approval
- Quarterly scenario re-runs (Monte Carlo) with updated data
- Annual validation of all regression model coefficients

### Versioning
- **Current Version:** 1.0.0 (2026-01-15)
- **Release Notes:** See git commit history
- **Backward Compatibility:** YAML structure is stable (no breaking changes expected)

### Data Quality
- Assumption sources documented in alpla_assumptions.yaml
- Model validation dates recorded in alpla_models.yaml
- Audit trail in git history (commits with dates/authors)

---

## Related Documents

### Strategic Foundation Documents
- `outputs/ALPLA_Board_Presentation_Summary.md` - 12-slide board presentation
- `outputs/ALPLA_Organizational_Design_Model_2025-2035.md` - 60+ page org design
- `outputs/ALPLA_Digital_Technology_Strategy_2025-2035.md` - Digital roadmap
- `outputs/ALPLA_HR_Strategy_2025-2035.md` - HR strategy & talent plan
- `outputs/ALPLA_Sales_KeyAccount_Strategy_2025-2035.md` - Sales & customer strategy

### Analytical Tools
- `scripts/SOCM_Alpla_Monte_Carlo_simple.py` - 10,000 scenario simulations (400 lines)
- `scripts/alpla_2035_revenue_dashboard.py` - Streamlit interactive dashboard

### Supporting Materials
- `data/customers/README.md` - This file
- `docs/frameworks/core-framework-definition.yaml` - EBF framework definition
- `appendices/` - 56 supporting appendices (EBF framework)

---

## Quick Reference

### Revenue Targets
| Scenario | 2024 | 2026 | 2029 | 2035 | CAGR |
|----------|------|------|------|------|------|
| Conservative | €4.9B | €5.1B | €6.2B | €8.7B | 5.8% |
| **Base Case** | €4.9B | €5.3B | €7.0B | €9.9B | 6.9% |
| Optimistic | €4.9B | €5.4B | €7.5B | €11.1B | 8.0% |

### Capex Budget
| Phase | Period | Budget | Annual Average | Total Cumulative |
|-------|--------|--------|-----------------|------------------|
| Phase 1 | 2025-26 | €180M | €90M | €180M |
| Phase 2 | 2027-29 | €230M | €77M | €410M |
| Phase 3 | 2030-35 | €140M | €23M | €550M |

### Headcount Evolution
| Year | Headcount | Regional Breakdown (2035) |
|------|-----------|---------------------------|
| 2024 | 24,350 | Europe 59%, APAC 16%, SA 21%, NA 12%, AMET 3% |
| 2026 | 27,400 | |
| 2029 | 32,500 | |
| 2035 | 38,500 | Europe 37.6%, APAC 20.9%, SA 13.5%, NA 7.8%, AMET 10.4%, Global 9.8% |

### Regional Growth (2024-2035)
| Region | 2024 | 2035 | CAGR | Growth |
|--------|------|------|------|--------|
| Asia-Pacific | €740M | €1,600M | 8.5% | +116% |
| Africa/ME | €240M | €500M | 8.0% | +108% |
| South America | €980M | €1,700M | 6.5% | +73% |
| North America | €740M | €1,100M | 4.5% | +49% |
| Europe | €2,200M | €2,700M | 2.5% | +23% |
| **TOTAL** | **€4,900M** | **€9,900M** | **6.9%** | **+101%** |

---

## Contact & Support

**Questions About This Database?**
- Strategic Planning Office: strategic-team@alpla.com
- Database Maintainer: analytics@alpla.com

**Accessing the Database:**
- Location: `/home/user/complementarity-context-framework/data/customers/alpla/`
- Format: YAML (text-based, version control friendly)
- Access: Read/write to authorized users

---

**Database Status:** ✅ ACTIVE & MAINTAINED
**Last Updated:** 2026-01-15
**Version:** 1.0.0
