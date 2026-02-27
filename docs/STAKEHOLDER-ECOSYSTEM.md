# Stakeholder-Ökosystem: Strategic Models & EBF Integration
## Rollen, Entscheidungen & Schnittstellen

**Version:** 1.0
**Datum:** 2026-01-16
**Kontext:** Phase 4+5 Integration (Learning Loop + Skill Enhancement)

---

## Übersicht: Wer nutzt das System und wie?

```
┌─────────────────────────────────────────────────────────────────────────┐
│  STRATEGIC DECISION LEVEL (Board, C-Suite)                            │
├─────────────────────────────────────────────────────────────────────────┤
│  • Board of Directors          ← /board-presentation (10-slide deck)   │
│  • CEO/CFO/COO                 ← Track Record + 10C Dashboard           │
│  • Strategy Committee           ← Scenario analysis + sensitivity       │
├─────────────────────────────────────────────────────────────────────────┤
│  OPERATIONAL LEVEL (Execution & Monitoring)                           │
├─────────────────────────────────────────────────────────────────────────┤
│  • Regional P&L Leaders        ← Regional CAGR tracking (APAC, SA)    │
│  • Business Unit Heads          ← Segment revenue forecasts            │
│  • Finance/Planning             ← Model maintenance + quarterly reviews │
│  • HR/Organization              ← Headcount projections                │
│  • Capex Committee              ← Capex allocation + ROI tracking      │
├─────────────────────────────────────────────────────────────────────────┤
│  ANALYTICAL LEVEL (Data & Learning)                                   │
├─────────────────────────────────────────────────────────────────────────┤
│  • Data Analytics / BI          ← quarterly_review.py automation      │
│  • FPA (Financial Planning)     ← parameter_update_pipeline.py        │
│  • Data Science                 ← archetype_discovery.py patterns     │
│  • Model Governance             ← Registry maintenance                 │
├─────────────────────────────────────────────────────────────────────────┤
│  EXTERNAL LEVEL (Reporting & Transparency)                            │
├─────────────────────────────────────────────────────────────────────────┤
│  • Investors / Analysts         ← Board presentation (public version) │
│  • Lenders / Rating Agencies    ← Financial forecasts + confidence    │
│  • Regulators                   ← Scenario analysis (stress tests)    │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 1. STRATEGISCHE ENTSCHEIDUNGSEBENE

### Board of Directors

**Rolle:** Strategie-Genehmigung, Risiko-Oversight, Budgetgenehmigung

**Was sie brauchen:**
```
/board-presentation Company pdf
├─ SLIDE 1: Executive Summary (4 key metrics at a glance)
├─ SLIDE 2: 3 Scenarios (Conservative, Base, Optimistic)
├─ SLIDE 2.5: Prediction Track Record (12+ quarters accuracy history)
│  └─ "Revenue ±2%, CAGR ±0.5pp, E(θ) shrinks 60% per year"
├─ SLIDE 3: Monte Carlo Confidence (percentile distribution)
├─ SLIDE 8: Sensitivity Analysis (CORE-tagged by WHERE/WHEN/HOW/WHAT)
│  └─ "APAC is 18.8% elastic; 60% parameter-driven, 40% context-driven"
├─ SLIDE 7: Roadmap (3-phase implementation with governance gates)
│  └─ Q4 2026 gate, Q4 2029 gate, Q4 2035 validation
└─ SLIDE 10: Board Recommendation (action items)
   └─ [ ] Approve base case, [ ] Authorize Phase 1 capex
```

**Ihre Fragen:**
- "Can we trust this forecast?" → **Track Record antwortet:** ±2% accuracy
- "What if markets change?" → **Learning Loop antwortet:** 1-quarter lag adaptation
- "How confident should we be?" → **WHERE antwortet:** E(θ) ±1.5pp shrinking
- "Where should we govern?" → **HIERARCHY antwortet:** N_L2 ≈ 180 L2 decisions
- "What could go wrong?" → **Sensitivity antwortet:** Top 6 risks with mitigation

**Entscheidungen:**
- ✓ Strategy approval (base case, conservative, optimistic)
- ✓ Capex authorization (Phase 1: €[X]M over 2 years)
- ✓ Quarterly review process establishment
- ✓ Governance gates timing (when to escalate)

**Feedback Loop:**
```
Q1: Board approves €€ capex
    ↓
Q2: Regional teams execute
    ↓
Q3: Actuals come in
    ↓
Q4: /intervention-manage close → quarterly_review.py
    ↓
Q1+1: Updated board presentation with track record
      "Forecast ±2.0%, actual showed ±1.8%" → confidence ↑
```

---

### CEO / CFO / COO (C-Suite)

**Rolle:** Strategie-Operationalisierung, Risiko-Mitigation, Stakeholder-Alignment

**Was sie brauchen:**
```
/board-presentation Company pdf --dashboard
├─ 10C CORE Foundation snapshot (WHERE/WHEN/HOW/WHAT/HIERARCHY live)
├─ Parameter confidence tracking (E(θ) history: how fast shrinking?)
├─ Risk attribution by dimension (70% WHERE, 20% WHEN, 7% HOW, 3% WHAT)
└─ Monthly governance gates (top 3 sensitivities to monitor)

Beispiel C-Suite Monitor:
┌────────────────────────────────────────────────────┐
│ Strategic Model Dashboard - Live                  │
├────────────────────────────────────────────────────┤
│ Base Case Revenue: €9.5B (CAGR 6.9%)              │
│ Confidence: E(θ) = ±0.8pp (from ±1.5pp at Q0)    │
│                                                    │
│ Top 3 Risks:                                       │
│  1. APAC_CAGR (18.8% elastic)     [WHERE]         │
│     → Monthly tracking required                    │
│  2. SA economic slowdown (12.6%)   [WHEN]         │
│     → Quarterly context monitoring                 │
│  3. Capex execution (1.8%)         [HOW + WHEN]   │
│     → Governance approval lag                      │
│                                                    │
│ Last Update: Q1 2025 actuals                      │
│ Accuracy: -1.8% vs forecast (within ±2%)          │
│ Next Gate: Q2 2025 (forecast review)              │
└────────────────────────────────────────────────────┘
```

**Ihre Verantwortungen:**
- **WHERE:** "Sind Parameter aktuell? Brauchen wir besser Daten?"
- **WHEN:** "Hat sich der Kontext geändert? Muss ich die Ψ-Dimensionen updaten?"
- **HOW:** "Sind die Teams koordiniert? Brauchen wir org Änderungen?"
- **WHAT:** "Stimmt die Portfolio-Alokation? Sollen wir rebalancieren?"
- **HIERARCHY:** "Wie viele L2-Entscheidungen koordinieren wir? Brauchen wir mehr gates?"

**Entscheidungen (monatlich):**
- ✓ Parameter Updates freigeben (wenn WHERE Signal)
- ✓ Context Anpassungen (wenn WHEN Signal)
- ✓ Org-Capability Investitionen (wenn HOW Signal)
- ✓ Portfolio-Rebalancing (wenn WHAT Signal)
- ✓ Governance-Gate Eskalation (wenn HIERARCHY überfordert)

---

### Strategy Committee

**Rolle:** Szenarien-Analyse, Konkurrenz-Vergleich, Langfrist-Planung

**Was sie brauchen:**
```
/sensitivity-analysis Company all --extended
├─ Alle Parameter auf ±2pp oder ±10% getestet
├─ CORE-tagged Elasticities (welche Dimension drives?)
├─ Composite Analysis (70% WHERE, 20% WHEN, 7% HOW, 3% WHAT)
├─ Competitive Comparison
│  └─ "We grow 6.9% CAGR, peers 1-2% → 4x advantage"
└─ 3-year rolling forecast (base case + 2 variants)

/board-presentation Company pdf --scenarios
├─ Conservative scenario (€7.2B, 4.2% CAGR)
│  └─ "If APAC under-performs, SA weakens"
├─ Base case (€9.5B, 6.9% CAGR) ← RECOMMENDED
│  └─ "Balanced execution across regions"
└─ Optimistic scenario (€11.5B, 8.0% CAGR)
   └─ "If Ψ₁ (economic) improves to 3%+, innovation accelerates"
```

**Ihre Analysen:**
- **Scenario branching:** Wie sensitiv ist jeder Scenario zu WHEN (Ψ)?
- **Competitive positioning:** Wo sind wir vs Wettbewerber in den 10C Dimensionen?
- **Strategic initiatives:** Welche Investitionen treiben HOW (γ) oder WHAT (ω)?
- **Downside risk:** Wie schnell können wir auf conservative case pivoten?

**Entscheidungen:**
- ✓ Scenario priorities (welcher Scenario ist Board baseline?)
- ✓ Initiative portfolio (welche Investments treiben Strategy forward?)
- ✓ Risk mitigation (kontingency plans für downside)

---

## 2. OPERATIONALE EBENE

### Regional P&L Leaders (APAC, Europe, SA, NA, AMET)

**Rolle:** Revenue-Execution, Regional-Strategien, Headcount-Management

**Was sie brauchen:**
```
/apply-models Company --regional
├─ Meine Region: APAC_CAGR = 8.5% ± 1.5pp (das ist MEIN target)
├─ Sensitivity: "1pp APAC CAGR miss = €267M revenue miss"
│  └─ "Das ist CRITICAL für overall strategy"
├─ Headcount: "APAC needs 2,500 → 3,200 headcount by 2035"
│  └─ "γ_rev-org=0.68 = jeder €100M revenue braucht ~X neue Leute"
└─ Quarterly tracking: "I will report APAC CAGR every month"

Mein APAC-Ziel (von Regional Board):
┌─────────────────────────────────────────────────────┐
│ APAC Revenue Forecast 2024-2035                    │
├─────────────────────────────────────────────────────┤
│ 2024: €1.2B (baseline)                             │
│ 2030: €2.1B (+75% growth)                          │
│ 2035: €2.9B (+142% total CAGR 8.5%)               │
│                                                     │
│ Success criteria:                                   │
│  • Actual CAGR ≥ 7.5% (1pp buffer)                 │
│  • Revenue variance < 5% YoY                       │
│  • Headcount scaling 1:1 with revenue growth       │
│                                                     │
│ WHERE risk: APAC parameter E(θ)=±1.5pp too wide   │
│  → Need better quarterly actuals reporting         │
│                                                     │
│ WHEN risk: Ψ₁ (economic) could deteriorate        │
│  → Monitor GDP growth quarterly                    │
│                                                     │
│ HOW risk: γ_rev-org=0.68 assumes tight coupling   │
│  → May need flexible staffing if execution slips  │
└─────────────────────────────────────────────────────┘
```

**Ihre Verantwortungen:**
- ✓ Hit APAC_CAGR target (8.5%, ±1pp buffer = 7.5-9.5%)
- ✓ Report actuals monthly (feeds quarterly_review.py)
- ✓ Manage headcount growth (must scale proportionally)
- ✓ Monitor WHEN context (GDP, market saturation, competitive moves)
- ✓ Escalate if diverging from forecast (> 5% variance)

**Entscheidungen:**
- ✓ Regional expansion/contraction (market entry timing)
- ✓ Pricing strategy (impact on CAGR elasticity)
- ✓ Talent acquisition (headcount pace vs revenue growth)
- ✓ Capex allocation (facility openings, equipment)

**Feedback Loop:**
```
Q0: Board approves APAC €1.2B baseline
    ↓
Q1: I execute strategy, report actual APAC revenue
    ↓
Q2: /intervention-manage close APAC_region --actuals Q1
    ├─ quarterly_review.py: Actual vs forecast
    ├─ If actual = 8.2% CAGR (forecast 8.5%) → attribution
    │  └─ Parameter drift? Context shock? Execution gap?
    └─ Result: Updated E(θ) for next forecast
    ↓
Q3: Board sees updated dashboard: "APAC on track, E(θ) ±1.4pp"
    ↓
Q4: Annual cycle closes with full year actual
    ↓
Next year: New forecast incorporates learnings
```

---

### Business Unit / Segment Leaders (Pharma, Beverage, Commodity, etc.)

**Rolle:** Segment-Strategie, Portfolio-Balancing, Margin-Management

**Was sie brauchen:**
```
/sensitivity-analysis Company Pharma_Revenue +10pct
├─ CORE-tagged output:
│  ├─ [WHAT: ω_D=0.20, ω_F=0.65] Pharma = 20% innovation, 65% financial
│  ├─ [WHERE: E(θ)=±2.5%] Parameter uncertainty
│  └─ [HOW: γ_pharma-capex=0.42] Capex synergy
│
├─ Elasticity: "€85M per 5% segment change (2.9%)"
│
└─ Complementarity cascade:
   ├─ Pharma ↑ → Capex needs ↑ (γ=0.42)
   │  └─ €85M volume + €12M capex offset = net €97M
   ├─ Pharma margin ↑ → Headcount flexible ↓ (γ=0.28)
   │  └─ Offset -€8M payroll on efficiency

Mein Pharma-Modell:
┌──────────────────────────────────────────────────┐
│ Pharma Segment Strategy                         │
├──────────────────────────────────────────────────┤
│ 2024: €1.5B revenue (25% of total)              │
│ 2035: €2.7B revenue (28% of total) [+80% growth]│
│                                                  │
│ Strategic Role: FINANCIAL driver                │
│  • F (financial): 65% → margin optimization     │
│  • D (innovation): 20% → some R&D investment    │
│  • S (scale): 15% → regional expansion          │
│                                                  │
│ Risk: Pharma parameter E(θ)=±2.5% is WIDE      │
│  → Market dynamics uncertain                    │
│  → Need quarterly competitive tracking          │
│                                                  │
│ Opportunity: γ_pharma-capex=0.42               │
│  → If we invest in capex, Pharma growth 50%+    │
│  → Recommended: Phase 1 pharma expansion        │
└──────────────────────────────────────────────────┘
```

**Ihre Verantwortungen:**
- ✓ Deliver WHAT utility (F/D/S/E/P/E targets)
- ✓ Monitor WHERE parameter (segment growth assumptions)
- ✓ Manage HOW complementarities (capex-volume coordination)
- ✓ Report segment actuals (feeds sensitivity reforecasting)
- ✓ Portfolio rebalancing (if market conditions change)

**Entscheidungen:**
- ✓ M&A vs organic growth (impact on WHAT weights)
- ✓ Capex investment (impact on HOW complementarity)
- ✓ Pricing / margin optimization (drives WHAT utility)
- ✓ Market exit / consolidation (portfolio rebalancing)

---

### Finance / Planning & Analysis (FP&A)

**Rolle:** Model-Governance, Quarterly Reviews, Parameter Updates

**Was sie brauchen:**
```
quarterly_review.py
├─ Automation:
│  ├─ Load Q1 actuals (revenue, headcount, capex by region/segment)
│  ├─ Compare vs Q0 forecast
│  ├─ Calculate ΔP = Actual - Predicted
│  └─ Decompose into WHERE/WHEN/HOW/WHAT attribution

parameter_update_pipeline.py
├─ Automation:
│  ├─ Load quarterly review ΔP
│  ├─ Apply Bayesian shrinkage: E(θ)_new = E(θ)_old × (1 - n/(n+k))
│  ├─ Detect regime changes (σ > 2.0)
│  └─ Update model_registry.yaml with new E(θ), history, reasons

archetype_discovery.py (quarterly after data accumulates)
├─ After 3+ completed projects:
│  ├─ Cluster similar (Ψ, WHAT, HOW, γ) profiles
│  ├─ Identify FFF archetypes
│  └─ Next new customer seeds with better priors

Monthly FP&A Tasks:
┌─────────────────────────────────────────────┐
│ Week 1: Collect monthly actuals             │
│ Week 2: Run quarterly_review.py (end of Q)  │
│ Week 3: Interpret attribution analysis      │
│ Week 4: Update parameter_update_pipeline    │
│         → E(θ) new values                    │
│         → model_registry.yaml updated        │
│                                              │
│ Monthly: Check model health                 │
│  • Are predictions staying ±2%?             │
│  • Are E(θ) values shrinking predictably?   │
│  • Do archetypes make sense?                │
└─────────────────────────────────────────────┘
```

**Ihre Verantwortungen:**
- ✓ Model maintenance (quarterly_review.py orchestration)
- ✓ Data quality (ensure actuals are accurate)
- ✓ Parameter governance (approve E(θ) updates)
- ✓ Forecast updates (re-run /apply-models after parameters change)
- ✓ Board briefing (explain attribution, next month's focus)

**Entscheidungen:**
- ✓ When to update parameters (after how much ΔP?)
- ✓ When to re-forecast (immediately after parameter update)
- ✓ Archetype assignments (which archetype is this new customer?)
- ✓ Model adjustments (if systematic bias found)

---

### HR / Organization

**Rolle:** Headcount-Planung, Talent-Management, Capability-Building

**Was sie brauchen:**
```
/apply-models Company --headcount
├─ Headcount projection: 8.1K → 10.2K (2024 → 2035)
├─ By function:
│  ├─ Engineering: 2.1K → 3.5K (+67%)
│  ├─ Sales: 1.2K → 1.8K (+50%)
│  ├─ Operations: 2.1K → 2.4K (+14%)
│  ├─ Finance: 1.0K → 1.2K (+20%)
│  └─ Admin: 1.7K → 1.3K (-24% via automation)
│
├─ HOW complementarity: γ_rev-org=0.68
│  └─ Each €100M revenue = ~68 new headcount (not 1:1)
│
├─ WHEN context: Ψ₃ (social/talent market)
│  └─ Engineering talent tight; need +20% salary to compete
│
└─ WHERE parameter: E(θ)=±0.08 on elasticity
   └─ High confidence in headcount-revenue coupling

HR Operational Plan:
┌────────────────────────────────────────────┐
│ Headcount Strategy 2024-2035               │
├────────────────────────────────────────────┤
│ Current: 8.1K (2024)                       │
│ Target: 10.2K (2035) = +2.1K net hires    │
│                                             │
│ Hiring pace:                               │
│  Years 1-2: +150/year (foundation build)  │
│  Years 3-5: +200/year (growth phase)      │
│  Years 6-11: +50/year (optimization phase)│
│                                             │
│ Critical: Engineering (γ=0.75 to innovation)
│  → Sales engineers must scale             │
│  → Product team must grow                 │
│                                             │
│ Opportunity: Automation (γ=0.35 to savings)
│  → Admin roles -24% via systems           │
│  → Finance operations -15% via RPA        │
│                                             │
│ Compensation:                              │
│  • Engineering: +20% vs market (talent)   │
│  • Sales: +10% (driven by APAC expansion) │
│  • Other: CPI + 2%                        │
│                                             │
│ Capability:                                │
│  • Quarterly /intervention-manage close   │
│    shows actual headcount vs forecast     │
│  • If slipping (hiring behind), escalate  │
└────────────────────────────────────────────┘
```

**Ihre Verantwortungen:**
- ✓ Hiring to headcount targets (by function, region)
- ✓ Talent quality management (especially APAC leadership)
- ✓ Capability building (for HOW complementarities to work)
- ✓ Compensation strategy (E(θ) on wage inflation)
- ✓ Actual headcount reporting (feeds quarterly_review.py)

**Entscheidungen:**
- ✓ Hiring pace (accelerate if APAC demand surges)
- ✓ Functional rebalancing (engineering -heavy for growth?)
- ✓ Salary investment (if talent market gets tighter)
- ✓ Automation / outsourcing (offset headcount growth in admin)

---

### Capex / Investment Committee

**Rolle:** Capital-Allocation, Projekt-Sequenzierung, ROI-Tracking

**Was sie brauchen:**
```
/apply-models Company --capex
├─ Total capex: €3.2B over 11 years (€290M/year average)
├─ Allocation:
│  ├─ ERP: €450M (€25M/year) [15-year ROI, 8% return]
│  ├─ IoT: €380M (€20M/year) [12-year ROI, 12% return]
│  ├─ Recycling: €920M (€50M/year) [8-year ROI, 18% return]
│  ├─ Geographic expansion: €680M (€100M/year) [10-year ROI, 10% return]
│  └─ Maintenance: €770M (€70M/year) [N/A, required]
│
├─ HOW sensitivity: γ_capex-revenue=0.62, γ_capex-org=0.48
│  └─ Org capacity (0.48) is BOTTLENECK
│     → Recommend: Invest in org capability FIRST
│
├─ WHEN sensitivity: Ψ₆ (institutional) = approval cycle lag
│  └─ If capex approved Q1, only 30% deployed Q1-Q2 (governance lag)
│     → Full deployment Q3-Q4
│
└─ WHERE: E(θ) on capex ROI = ±15% wide
   └─ Need better project governance data

Capex Roadmap (3 Phases):
┌────────────────────────────────────────────┐
│ Phase 1 (2025-26): €150M/year foundation   │
│  ├─ ERP pilot (€25M total)                 │
│  ├─ Recycling scale-up (€50M/year)        │
│  ├─ Thailand plant (€40M)                  │
│  └─ Regional leadership (€35M)             │
│                                             │
│ Phase 2 (2027-29): €320M/year expansion    │
│  ├─ APAC plant #2-4 (€150M/year)          │
│  ├─ PEF commercialization (€70M)          │
│  ├─ ERP 150 sites (€50M/year)             │
│  └─ IoT rollout (€50M/year)               │
│                                             │
│ Phase 3 (2030-35): €290M/year optimization │
│  ├─ Maintenance capex (€70M/year)         │
│  ├─ AMET scale-up (€80M/year)             │
│  ├─ Advanced recycling (€60M/year)        │
│  └─ Innovation (€80M/year)                │
│                                             │
│ Expected return: €5.8B NPV, 18% IRR       │
└────────────────────────────────────────────┘
```

**Ihre Verantwortungen:**
- ✓ Capex governance (approvals per phase gate)
- ✓ Project sequencing (order to maximize ROI)
- ✓ Org capacity monitoring (γ_capex-org=0.48 bottleneck)
- ✓ Execution tracking (vs forecast spend)
- ✓ ROI realization (actual benefits vs plan)

**Entscheidungen:**
- ✓ Phase gate approvals (Q4 2026, Q4 2029)
- ✓ Project prioritization (recycling > IoT > ERP?)
- ✓ Org capability investment (before or with capex?)
- ✓ Financing strategy (debt vs equity vs cash)

---

## 3. ANALYTISCHE EBENE

### Data Analytics / Business Intelligence

**Rolle:** Dashboard-Bereitstellung, Real-time Monitoring, Automatisierung

**Was sie brauchen:**
```
Live Strategic Dashboard (automated from system)
├─ Base case metrics:
│  ├─ Revenue: €2.85B (Q1 2024) vs €2.56B actual (-1.8%)
│  ├─ CAGR: 6.9% (assumption) vs 6.2% realized
│  └─ Confidence: E(θ) = ±0.8pp (from ±1.5pp Q0)
│
├─ Regional KPIs:
│  ├─ APAC: 6.2% actual vs 8.5% forecast (FLAG: -2.3pp)
│  ├─ Europe: 2.4% actual vs 2.5% forecast (✓ on track)
│  ├─ SA: 6.8% actual vs 6.5% forecast (✓ above target)
│  └─ NA: 4.5% actual vs 4.5% forecast (✓ on track)
│
├─ 10C CORE Status:
│  ├─ WHERE: E(θ) shrinking (±1.5pp → ±0.8pp) ✓ learning
│  ├─ WHEN: Ψ₁ economic dropped (2.8% → 2.1% GDP) ⚠ alert
│  ├─ HOW: γ values stable ✓ as expected
│  ├─ WHAT: Portfolio stable ✓ F=55%, D=15%
│  └─ HIERARCHY: N_L2=180 decisions ✓ managed
│
├─ Quarterly attribution (from latest quarterly_review.py):
│  ├─ WHERE error: -€20M (-40% of miss)
│  ├─ WHEN shock: -€25M (-50% of miss) ⚠ economic slowdown
│  ├─ WHAT drift: +€10M (offset) ✓ pharma outperformed
│  └─ HOW error: -€15M (-30% of miss)
│
└─ Next escalation:
   ├─ IF ΔP > ±5%: Escalate to C-Suite
   ├─ IF E(θ) not shrinking: Review data quality
   ├─ IF WHEN detected: Update context monitoring
   └─ IF archetype patterns: Seed next customer

Automated Alert System:
┌─────────────────────────────────────────┐
│ Strategic Model Alerts (Real-time)      │
├─────────────────────────────────────────┤
│ 🔴 CRITICAL (escalate immediately)     │
│  • ΔP > ±10% on revenue                │
│  • Regional variance > 8%               │
│  • E(θ) growing (wrong direction!)     │
│                                         │
│ 🟠 HIGH (review within week)           │
│  • ΔP > ±5% on revenue                │
│  • Parameter drift > σ (regime change) │
│  • Context regime change detected      │
│                                         │
│ 🟡 MEDIUM (monitor monthly)            │
│  • ΔP > ±2% on revenue                │
│  • E(θ) not shrinking as expected     │
│  • Regional variance > 3%              │
│                                         │
│ 🟢 OK (business as usual)              │
│  • ΔP within ±2%                       │
│  • E(θ) shrinking predictably          │
│  • All KPIs on track                   │
└─────────────────────────────────────────┘
```

**Ihre Verantwortungen:**
- ✓ Dashboard maintenance (monthly updates)
- ✓ Alert automation (trigger escalations)
- ✓ quarterly_review.py data ingestion
- ✓ Visualization & reporting (for board, C-Suite)
- ✓ Data quality validation (garbage in = garbage out)

---

### FPA (Financial Planning & Analysis)

**Rolle:** Model Governance, Parameter Maintenance, Quarterly Cycles

**Was sie brauchen:**
```
Model Registry Governance (model_registry.yaml)
├─ For each of 35 models:
│  ├─ Current parameters (θ values)
│  ├─ E(θ) confidence intervals
│  ├─ E(θ) update history (Q0 ±1.5pp → Q4 ±0.6pp)
│  ├─ 10C CORE mappings
│  └─ Last update date, reason, approver
│
├─ Quarterly cycle:
│  └─ /intervention-manage close Company Q1
│     ├─ quarterly_review.py generates ΔP attribution
│     ├─ FPA reviews: "Is this parameter-driven or context-driven?"
│     ├─ parameter_update_pipeline.py calculates new E(θ)
│     ├─ FPA approves: "New APAC_CAGR E(θ) = ±1.4pp approved"
│     └─ Model registry updated
│
└─ Monthly check-in:
   ├─ Are E(θ) values shrinking as expected?
   ├─ Do forecast errors match attribution theory?
   ├─ Should we adjust learning speed (k parameter)?
   └─ Any systematic biases to correct?

FPA Governance Process:
┌────────────────────────────────────────┐
│ Monthly: Data collection               │
│ ├─ Revenue by region/segment           │
│ ├─ Headcount actuals                   │
│ ├─ Capex spend tracking                │
│ └─ Context indicators (GDP, inflation) │
│                                         │
│ End of Quarter: Formal Review           │
│ ├─ quarterly_review.py runs            │
│ ├─ ΔP calculated & attributed          │
│ ├─ FPA + Data Science review           │
│ ├─ parameter_update_pipeline approved  │
│ ├─ E(θ) updated in registry            │
│ └─ /apply-models re-run with new θ     │
│                                         │
│ Next Month: Board Update                │
│ ├─ /board-presentation updated         │
│ ├─ Track record grows (Q0, Q1, Q2...)  │
│ ├─ Board sees learning curve           │
│ └─ Confidence bands narrow visibly     │
└────────────────────────────────────────┘
```

**Ihre Verantwortungen:**
- ✓ Parameter governance (approve E(θ) updates)
- ✓ Quarterly cycle orchestration
- ✓ Model quality assurance (systematic bias checks)
- ✓ Archetype assignment (which archetype is new customer?)
- ✓ Baseline forecast generation (/apply-models runs)

---

### Data Science / Advanced Analytics

**Rolle:** Pattern Recognition, Model Innovation, Archetype Discovery

**Was sie brauchen:**
```
archetype_discovery.py (quarterly after 3+ projects)
├─ After 3 completed projects:
│  ├─ Project 1: ALPLA (€2.5B, Europe-centric, mature)
│  ├─ Project 2: TechCo (€1.2B, APAC-growth, emerging)
│  └─ Project 3: ...(similar profile?)
│
├─ Cluster on (Ψ, WHAT, HOW, γ):
│  └─ FFF-MATURE-EU archetype:
│     ├─ Ψ: Low growth (2%), stable context
│     ├─ WHAT: F=70% (profit focus), D=10%
│     ├─ HOW: Low complementarities (γ_avg=0.45)
│     ├─ γ values: γ_rev-org=0.52, γ_capex-revenue=0.35
│     └─ Priors: E(θ) on revenue=±0.6pp (proven tight)
│
│  └─ FFF-GROWTH-APAC archetype:
│     ├─ Ψ: High growth (6-8%), emerging market
│     ├─ WHAT: F=55%, D=25%, S=20%
│     ├─ HOW: High complementarities (γ_avg=0.65)
│     ├─ γ values: γ_rev-org=0.68, γ_capex-revenue=0.62
│     └─ Priors: E(θ) on revenue=±0.8pp (faster convergence)
│
├─ For new customer: "Which archetype best fits?"
│  ├─ If FFF-MATURE-EU: Start with E(θ)=±0.6pp
│  ├─ If FFF-GROWTH-APAC: Start with E(θ)=±0.8pp
│  └─ Result: Forecast converges 30% faster
│
└─ Continuous learning:
   ├─ Every new project updates archetype profiles
   ├─ archetype_discovery.py re-clusters quarterly
   └─ Next new customer benefits from most recent patterns

Data Science Tasks (Quarterly):
┌──────────────────────────────────────┐
│ 1. Run archetype_discovery.py        │
│    → Which customers cluster together?│
│                                       │
│ 2. Analyze γ patterns                 │
│    → Are complementarities stable?   │
│    → Or does archetype matter?       │
│                                       │
│ 3. Context sensitivity analysis      │
│    → Which Ψ dimensions matter most? │
│    → Can we predict WHEN shocks?     │
│                                       │
│ 4. Forecast error deep-dives         │
│    → Why ±2% not ±1%?               │
│    → Is model misspecified?          │
│                                       │
│ 5. E(θ) convergence tracking         │
│    → Is Bayesian shrinkage working? │
│    → λ = n/(n+k) formula appropriate?│
└──────────────────────────────────────┘
```

**Ihre Verantwortungen:**
- ✓ Archetype discovery (quarterly clustering)
- ✓ Pattern analysis (which factors matter?)
- ✓ Model innovation (can we improve γ estimates?)
- ✓ Context prediction (can we forecast WHEN shocks?)
- ✓ Forecast quality analysis (why do we miss?)

---

## 4. EXTERNE EBENE

### Investors / Equity Analysts

**Rolle:** Valuation, Growth Narrative, Risk Assessment

**Was sie brauchen:**
```
/board-presentation Company pdf --investor-version
├─ SLIDE 1: Investment Thesis
│  ├─ Market opportunity: €12B total addressable market (TAM)
│  ├─ Our position: €9.5B base case by 2035 (strategic objectives)
│  └─ vs peers: 4-7x faster growth (ALPLA 6.9% vs peers 1-2%)
│
├─ SLIDE 2: Confidence & Track Record
│  ├─ "12+ quarters of forecast accuracy: ±2% revenue"
│  ├─ "E(θ) shrinks 60% per year via Bayesian learning"
│  └─ "Board gates align incentives (Q4 2026, Q4 2029)"
│
├─ SLIDE 3: Risk Management
│  ├─ Sensitivity analysis: "Top 3 risks identified"
│  ├─ Mitigation: "WHEN monitoring (quarterly Ψ snapshot)"
│  ├─ Governance: "Monthly tracking of APAC execution"
│  └─ Adaptive: "Learning loop updates forecast quarterly"
│
├─ SLIDE 4: Return Potential
│  ├─ Base case NPV: €[X]M at [Y]% discount rate
│  ├─ Downside case NPV: €[X-20%]M (conservative scenario)
│  ├─ Upside case NPV: €[X+30%]M (optimistic scenario)
│  └─ IRR by phase: Phase 1: [X]%, Phase 2: [Y]%, Phase 3: [Z]%
│
└─ SLIDE 5: Call to Action
   ├─ Series funding needed: €[X]M
   ├─ Uses of proceeds: Capex (€Y), WC (€Z), Buffer
   └─ Timeline: Series close Q2 2025, deployment Q3 2025

Investor FAQ (powered by 10C CORE):
├─ Q: "How confident are you in 6.9% CAGR?"
│  A: "WHERE: E(θ)=±0.8pp after 12 months (82% confident)
│     WHEN: Economic assumption 2.8% GDP (monitored monthly)
│     HOW: Org capability in place (γ_rev-org=0.68)
│     WHAT: F=55% portfolio alignment (strategic fit)"
│
├─ Q: "What's your downside?"
│  A: "Conservative: 4.2% CAGR (€7.2B by 2035)
│     Triggers: APAC economic slowdown, competitive pressure
│     Mitigation: Monthly tracking, quarterly reforecasting"
│
└─ Q: "How do you derisk over time?"
   A: "E(θ) shrinks 60%/year: €1.5B range → €0.6B range in 12 months
      Board gates reduce execution risk (Phase 1 → Phase 2 → Phase 3)
      Learning loop detects context changes within 1 quarter"
```

**Ihre Fragen (und Antworten):**
- WHERE: Parameter confidence? → Track record shows ±2% accuracy
- WHEN: External risks? → GDP sensitivity €134M per 1pp (monitored quarterly)
- HOW: Execution capability? → γ values proven across 3 projects
- WHAT: Strategic fit? → Portfolio aligned to investor thesis
- HIERARCHY: Governance? → Board gates + quarterly reviews de-risk

---

### Lenders / Credit Rating Agencies

**Rolle:** Debt Capacity, Coverage Ratios, Stress Testing

**Was sie brauchen:**
```
/sensitivity-analysis Company all --stress-test
├─ Base case: €9.5B revenue, €2.1B EBITDA, 4.5x Debt/EBITDA
│
├─ Stress scenarios (WHEN context shifts):
│  ├─ Mild: GDP -1pp → Revenue €8.8B, D/EBITDA 4.8x (manageable)
│  ├─ Moderate: GDP -2pp → Revenue €8.0B, D/EBITDA 5.2x (tight)
│  └─ Severe: GDP -3pp → Revenue €7.2B, D/EBITDA 5.7x (trigger covenant)
│
├─ Debt service coverage:
│  ├─ Year 1-5: 2.5x DSCR (comfortable)
│  ├─ Year 6-11: 2.8x DSCR (improving)
│  └─ Worst case: 1.8x DSCR (still above 1.2x covenant)
│
└─ Debt capacity analysis:
   ├─ Current debt: €[X]M
   ├─ Available capacity: €[Y]M (at 4.5x leverage covenant)
   ├─ Phase 1 capex needs: €[Z]M (within capacity)
   └─ Phase 2 capex needs: €[Z+W]M (need to refinance or reduce leverage)

Lender Dashboard:
┌─────────────────────────────────────┐
│ Credit Metrics Monitoring           │
├─────────────────────────────────────┤
│ Base case:                          │
│  • Revenue: €9.5B (CAGR 6.9%)      │
│  • EBITDA: €2.1B (22% margin)      │
│  • Debt: €[X]M (4.5x leverage)     │
│  • DSCR: 2.5x (interest coverage) │
│                                     │
│ Stress test (GDP -2pp):             │
│  • Revenue: €8.0B (CAGR 4.2%)      │
│  • EBITDA: €1.7B (21% margin)      │
│  • Debt: €[X]M (same)              │
│  • DSCR: 2.1x (still comfortable)  │
│  • D/EBITDA: 5.2x (vs 4.5x cov.)  │
│                                     │
│ Mitigation levers:                  │
│  • Capex deferral (reduce from €290M)
│  • Cost reduction (if margin pressure)
│  • Dividend suspension              │
│  • Debt refinancing (Q4 2026)      │
│                                     │
│ Quarterly monitoring:               │
│  ✓ Revenue vs forecast (±2% target)│
│  ✓ EBITDA margin (maintain 21-22%) │
│  ✓ Debt levels (track leverage)    │
│  ✓ Context (Ψ₁ economic) quarterly │
└─────────────────────────────────────┘
```

**Ihre Anforderungen:**
- WHERE: Parameter estimates conservative? → Show APAC data, E(θ)
- WHEN: Economic assumptions reasonable? → GDP 2.8% conservative vs consensus 3%
- HOW: Capex execution track record? → Phase 1 realistic with org capacity?
- HIERARCHY: Governance prevents overleveraging? → Board gates de-risk escalation
- Stress: Can you handle GDP -2pp? → DSCR still 2.1x, covenant safe

---

### Regulators (für börsennotierte Unternehmen)

**Rolle:** Financial Transparency, Segment Reporting, Risk Disclosure

**Was sie brauchen:**
```
Regulatory Filing (Annual Report, 10-K, Annual Report)
├─ Forward-looking statements (Item 1A Risk Factors):
│  ├─ "Revenue sensitive to APAC execution (18.8% elasticity)"
│  ├─ "Economic slowdown could reduce CAGR by 2-3pp"
│  ├─ "Capex execution dependent on org capability (γ=0.48)"
│  └─ "Competitive pressure in mature markets (Europe 2.5% CAGR)"
│
├─ Management discussion & analysis (MD&A):
│  ├─ "Base case strategy €9.5B by 2035"
│  ├─ "Board governance: quarterly reviews, phase gates Q4 2026/2029"
│  ├─ "Track record: 12+ quarters ±2% forecast accuracy"
│  └─ "Learning loop enables quarterly parameter updates"
│
├─ Segment information:
│  ├─ Geographic: Europe, APAC, SA, NA, AMET
│  │  └─ With CAGR forecasts & sensitivities
│  └─ Product: Pharma, Beverage, Commodity, Recycled
│     └─ With WHAT utility weights
│
└─ Basis of estimates (sensitivity tables):
   ├─ Revenue sensitivity to APAC_CAGR: €267M per 1pp
   ├─ Revenue sensitivity to GDP (Ψ₁): €134M per 1pp
   ├─ Headcount sensitivity to revenue: γ=0.68
   └─ Capex ROI by initiative (ERP 8%, Recycling 18%)

SEC/Stock Exchange Compliance:
├─ Material risks disclosed: APAC, economic slowdown
├─ Quantified sensitivities: Clear elasticity numbers
├─ Governance: Board gates + monthly execution tracking
├─ Learning loop: Quarterly updates reduce forecast error
└─ Archetype: Future customers converge faster (de-risks growth narrative)
```

**Ihre Anforderungen:**
- Materiality: Is APAC 18.8% elasticity material? → YES (€267M swing)
- Reasonableness: Are CAGR assumptions justified? → Track record ±2%, conservative
- Disclosure: Have you disclosed risks? → Risk factors + sensitivity tables
- Governance: Is there oversight? → Board gates, quarterly reviews
- Fraud prevention: Could management manipulate forecasts? → Learning loop detects systematic bias

---

## Zusammenfassung: Stakeholder Decision Matrix

| Stakeholder | Entscheidung | CORE Dimension | Tools | Häufigkeit |
|---|---|---|---|---|
| **Board** | Strategy approval | Alle (5 dimensions) | /board-presentation | Quarterly |
| **C-Suite** | Risk mitigation | WHERE, WHEN, HIERARCHY | Dashboard | Monthly |
| **Regional Leader** | Execution targets | WHERE, WHEN | Regional KPI tracking | Monthly |
| **Segment Leader** | Portfolio balance | WHAT, HOW | /sensitivity-analysis | Quarterly |
| **FP&A** | Parameter updates | WHERE | quarterly_review.py | Quarterly |
| **HR** | Headcount plan | HOW | Headcount projection | Monthly |
| **Capex Committee** | Phase gate approval | HOW, WHEN | Capex roadmap | Quarterly gates |
| **Data Analytics** | Alert automation | Alle (5) | Dashboard automation | Real-time |
| **Data Science** | Archetype discovery | WHEN, HOW, WHAT | archetype_discovery.py | Quarterly |
| **Investors** | Valuation/thesis | Alle + track record | Investor deck | On demand |
| **Lenders** | Debt capacity | WHERE, WHEN (stress) | Stress testing | Quarterly |
| **Regulators** | Risk disclosure | Alle | MD&A + sensitivity | Annual |

---

## Nächste Schritte: Stakeholder Enablement

### Dokumentation pro Stakeholder-Gruppe:
```
✅ Board Guide: /docs/BOARD-GUIDE.md (decision framework, track record narrative)
✅ FP&A Guide: /docs/FPA-GOVERNANCE.md (quarterly cycle, parameter updates)
✅ Regional Guide: /docs/REGIONAL-KPI-GUIDE.md (CAGR targets, elasticity alerts)
⏳ Investor Guide: /docs/INVESTOR-THESIS.md (growth narrative, risk management)
⏳ Lender Package: /docs/CREDIT-ANALYSIS.md (stress testing, debt capacity)
⏳ Regulator Guide: /docs/SEC-RISK-DISCLOSURE.md (materiality, governance)
```

### Training & Rollout:
- **Board workshop:** 2h (strategy, track record, governance model)
- **FP&A deep-dive:** 4h (quarterly cycle, parameter updates, archetype logic)
- **Regional kickoff:** 2h (targets, elasticity alerts, escalation process)
- **Investor relations:** 1h (pitch, risk disclosure, track record)

---

**Alle Stakeholder sind jetzt aligned zur 10C CORE Integration!**

