# /board-presentation Skill
## Generate Board-Ready Strategic Presentation

**Purpose:** Create executive presentation from model outputs in 2 minutes

**Time Estimate:** 1-2 minutes

---

## Usage

```
/board-presentation <company_name> [format] [style]

Examples:
  /board-presentation Company_XYZ
  /board-presentation Company_XYZ pdf
  /board-presentation Company_XYZ powerpoint clean
  /board-presentation ALPLA pdf professional
  /board-presentation Company_XYZ markdown
```

---

## Supported Formats

| Format | Extension | Output | Use Case |
|--------|-----------|--------|----------|
| PDF | .pdf | Single-document presentation | Print, email, distribute |
| PowerPoint | .pptx | Editable slides | Board meetings, discussions |
| Markdown | .md | Text format | Version control, collaboration |
| HTML | .html | Web-ready | Internal portals, dashboards |
| LaTeX | .tex | Professional typeset | Academic/formal contexts |

---

## Presentation Structure (10 Slides)

### SLIDE 1: Executive Summary
**Title:** Strategic Outlook 2035 | [Company Name]

**Content:**
- Company name & logo
- Base case target (2035 revenue)
- Key metrics at a glance:
  - Current (2024) → Target (2035)
  - Revenue: €[X]B → €[Y]B (+[Z]%)
  - CAGR: [X]%
  - Headcount: [X]K → [Y]K
  - Capex: €[X]M (average per year)

**Visual:** Large call-out box with 4 key numbers

---

### SLIDE 2: 3 Strategic Scenarios
**Title:** Revenue Scenarios 2024-2035

**Content (Table):**
| Scenario | 2024 | 2035 | Growth | CAGR | Status |
|----------|------|------|--------|------|--------|
| Conservative | €X | €Y | +Z% | 4.2% | ✓ Achievable |
| **Base Case** | €X | €Y | +Z% | 6.9% | ✅ **RECOMMENDED** |
| Optimistic | €X | €Y | +Z% | 8.0% | Stretch |

**Visual:** 3-line chart showing trajectory curves

---

### SLIDE 3: Monte Carlo Confidence Metrics
**Title:** Risk Quantification (10,000 Scenarios)

**Content:**
- Percentile distribution table:
  ```
  Percentile | 2035 Revenue | Probability
  5% | €[downside] | Low probability of missing
  50% (Median) | €[base] | 50% chance
  95% | €[upside] | High confidence
  ```

- Key probability metrics:
  - Probability base case achievable: [X]%
  - Probability exceeding conservative: [X]%
  - Downside risk (5th percentile): €[X]B
  - Upside potential (95th percentile): €[X]B

**Visual:** Histogram + probability curve with percentile markers

---

### SLIDE 4: Regional Growth Drivers
**Title:** Regional Revenue Breakdown & Growth Rates

**Content (Table):**
| Region | 2024 | 2035 | CAGR | Key Driver |
|--------|------|------|------|-----------|
| Europe | € | € | 2.5% | Mature market, compliance |
| Asia-Pacific | € | € | 8.5% | Market entry, expansion |
| South America | € | € | 6.5% | Beverage strength |
| North America | € | € | 4.5% | Steady recovery |
| AMET | € | € | 8.0% | Early-mover advantage |

**Visual:** Stacked bar chart showing regional mix shift (2024 vs 2035)

---

### SLIDE 5: Organizational Scaling
**Title:** Headcount & Payroll Evolution

**Content:**
- Left side: Headcount by function (stacked bar)
  - 2024: [X]K total
  - 2035: [Y]K total (+[Z]%)

- Right side: Payroll as % of revenue
  - 2024: [X]% of revenue
  - 2035: [Y]% of revenue
  - Headcount cost escalation: +[X]% annual (blended)

**Key metrics:**
- Critical hiring needs:
  - IT/Digital: +[X] positions (highest priority)
  - APAC Leadership: +[X] positions
  - Advanced Recycling: +[X] specialists

**Visual:** Dual-axis chart (headcount stacked bar + payroll % line)

---

### SLIDE 6: Capital Allocation & ROI
**Title:** 11-Year Capex Strategy & Expected Returns

**Content (Table):**
| Initiative | Capex | Benefits | ROI | Payback |
|-----------|-------|----------|-----|---------|
| ERP | €[X]M | €[Y]M | Z% | X years |
| IoT | €[X]M | €[Y]M | Z% | X years |
| Recycling | €[X]M | €[Y]M | Z% | X years |
| Geographic | €[X]M | €[Y]M | Z% | X years |
| Maintenance | €[X]M | €[Y]M | Z% | X years |
| **TOTAL** | €[X]M | €[Y]M | Z% | X years |

**Key insight:**
- Total capex: €[X]M over 11 years (€[X]M/year average)
- Expected benefits: €[Y]M
- Total ROI: [Z]%
- Payback period: [X] years

**Visual:** Waterfall chart showing capex allocation and ROI buildup

---

### SLIDE 7: Key Execution Milestones (3-Phase Roadmap)
**Title:** Implementation Timeline 2025-2035

**Content:**
```
Phase 1: Foundation        Phase 2: Expansion         Phase 3: Optimization
(2025-2026)               (2027-2029)               (2030-2035)
├─ ERP pilot              ├─ APAC plant #2-4        ├─ AMET at scale
├─ Recycling scale-up     ├─ PEF commercialization ├─ Paboco profitability
├─ Regional leadership    ├─ 500K tonnes capacity   ├─ Advanced recycling mature
├─ Thailand plant         ├─ ERP 150 plants        ├─ ERP 95% coverage
└─ 25% recycled content   └─ Revenue €7B target    └─ Revenue €9.9B target
```

**Key decision gates marked:**
- Q4 2026: Phase 2 approval
- Q4 2029: Phase 3 approval
- Q4 2035: Strategy validation

**Visual:** Gantt-style timeline with phases, initiatives, and decision gates

---

### SLIDE 8: Sensitivity Analysis & Risk Factors
**Title:** Parameter Sensitivities & Risk Management

**Content:**
- Top 5 sensitivities (elasticity analysis):
  ```
  #1 APAC CAGR:      €267M per 1pp (18.8% elasticity) 🔴 HIGH
  #2 South America:  €180M per 1pp (12.6% elasticity) 🔴 HIGH
  #3 Europe CAGR:    €120M per 1pp (8.4% elasticity) 🟡 MEDIUM
  #4 Pharma segment: €85M per 5% (2.9% elasticity) 🟡 MEDIUM
  #5 Capex budget:   €50M per 10% (1.8% elasticity) 🟢 LOW
  ```

- Risk mitigation strategies:
  - ✓ Strong APAC program management (weekly tracking)
  - ✓ Regional leadership with execution experience
  - ✓ Phased capex approach (preserve optionality)
  - ✓ Quarterly board reviews vs assumptions

**Visual:** Spider chart or sensitivity tornado chart

---

### SLIDE 9: Competitive Positioning
**Title:** Market Position vs. Competitors (2024 → 2035)

**Content (Table):**
| Company | 2024 | 2035 (Est.) | CAGR | Competitive Position |
|---------|------|------|------|-----|
| Amcor | $13.0B | $15.5B | 1.7% | Slow growth |
| Berry Global | $13.5B | $15.0B | 1.0% | Declining |
| [Company] | €[X]B | €[Y]B | [Z]% | **4-7x faster** |

**Key advantage:**
- Vertical integration (design → recycling)
- In-house capacity (vs. outsourced)
- Sustainability leadership positioning

**Visual:** Comparison bar chart showing ALPLA growth trajectory vs peers

---

### SLIDE 10: Strategic Recommendation & Next Steps
**Title:** Board Decision & Approval

**Content:**

**RECOMMENDATION: Base Case Strategy (€X.XB target)**
- ✅ Balanced growth across regions & segments
- ✅ Achievable with disciplined €[X]M/year capex
- ✅ Positions company as circular economy leader
- ✅ Expected ROI: [X]% over 11 years

**THREE-PHASE IMPLEMENTATION:**
- **Phase 1 (2025-26):** Foundation & acceleration
  - Q1 2026: APAC regional setup complete
  - Board gate decision: Proceed to Phase 2

- **Phase 2 (2027-29):** Expansion & scaling
  - Board gate decision: Proceed to Phase 3 (Q4 2029)

- **Phase 3 (2030-35):** Optimization & maturation
  - Final target: €[X.X]B revenue, [X]% CAGR achieved

**BOARD ACTION REQUESTED:**
- [ ] Approve base case strategy (€X.XB by 2035)
- [ ] Authorize Phase 1 capex (€[X]M, 2025-2026)
- [ ] Establish quarterly review process
- [ ] Confirm regional leadership hiring authority

---

## Prediction Track Record & Learning Loop Integration (Phase 5)

**Purpose:** Demonstrate prediction accuracy and evolving confidence to board through historical track record.

### Fundamental Insight

The Learning Loop enables continuous parameter refinement, resulting in:
1. **Improved accuracy** over time as E(θ) shrinks with observations
2. **Narrowing confidence intervals** as sample size grows (Bayesian shrinkage)
3. **Attributable errors** (context shock vs. parameter drift vs. model misspecification)
4. **Velocity of learning** showing how fast confidence converges

### New Optional Slide: "Prediction Track Record" (Slide 2.5)

**When to Include:**
- ✓ **For mature projects** (3+ quarters of actual data)
- ✓ **To establish credibility** in forecast for new customers
- ✓ **For board reviews** to show disciplined learning approach
- ✓ **For risk mitigation** demonstrating adaptive strategy

**When to Exclude:**
- ✗ New customer (< 1 quarter of data)
- ✗ Board wants streamlined presentation (10 slides only)

### Track Record Content

#### Section 1: Historical Accuracy Table

Shows prediction vs. actual for 3+ quarters of past projects:

```
╔══════════════════════════════════════════════════════════════════════════╗
║ SLIDE 2.5: PREDICTION TRACK RECORD | Historical Accuracy Summary      ║
╚══════════════════════════════════════════════════════════════════════════╝

HISTORICAL PREDICTIONS vs ACTUAL OUTCOMES
(3+ Completed Projects | 12+ Quarters of Data)

Project    │ Metric       │ 2024 Q1 Pred  │ 2024 Q1 Actual │ Error   │ MAPE
           │              │ (Jan 2023)    │ (Apr 2024)     │ (ΔP)    │
─────────────┼──────────────┼───────────────┼────────────────┼─────────┼────────
ALPLA-2024  │ Revenue      │ €2.50B        │ €2.45B         │ -€50M   │ -2.0%  ✓
            │ APAC CAGR    │ 8.5%          │ 5.8%           │ -2.7pp  │ ✗ WIDE
            │ Headcount    │ 27.5K         │ 26.8K          │ -700    │ -2.5%  ✓
            │ Capex        │ €240M         │ €218M          │ -€22M   │ -9.2%  ⚠
─────────────┼──────────────┼───────────────┼────────────────┼─────────┼────────
ALPLA-2024  │ Revenue      │ €2.60B        │ €2.56B         │ -€40M   │ -1.5%  ✓
(Q2 2024)   │ APAC CAGR    │ 6.5% (updated)│ 6.2%           │ -0.3pp  │ ✓ TIGHT
            │ Headcount    │ 27.8K         │ 27.5K          │ -300    │ -1.1%  ✓
            │ Capex        │ €260M         │ €242M          │ -€18M   │ -6.9%  ✓
─────────────┼──────────────┼───────────────┼────────────────┼─────────┼────────
TechCo1     │ Revenue      │ €1.20B        │ €1.18B         │ -€20M   │ -1.7%  ✓
(3 qtrs)    │ CAGR         │ 12.0%         │ 11.5%          │ -0.5pp  │ ✓ TIGHT
            │ Headcount    │ 8.5K          │ 8.2K           │ -300    │ -3.5%  ✓
            │ Capex        │ €85M          │ €92M           │ +€7M    │ +8.2%  ⚠
─────────────┼──────────────┼───────────────┼────────────────┼─────────┼────────
OVERALL     │ Revenue MAPE │                                          │ 1.7%   ✓✓
            │ CAGR MAPE    │                                          │ 1.2pp  ✓✓
            │ Headcount    │                                          │ 2.4%   ✓
            │ Capex MAPE   │                                          │ 8.1%   ⚠
━━━━━━━━━━━━┷━━━━━━━━━━━━━┷━━━━━━━━━━━━━━━┷━━━━━━━━━━━━━━━━┷━━━━━━━━┷━━━━━━

KEY FINDINGS:
  ✓✓ EXCELLENT: Revenue predictions accurate within ±2% (18 quarters)
  ✓✓ EXCELLENT: CAGR estimates converge to ±0.5pp range
  ✓  GOOD: Headcount within ±3.5%
  ⚠  NEEDS WORK: Capex estimates wide (±9%) → need better governance data
```

#### Section 2: Confidence Interval Convergence

Shows how E(θ) shrinks over quarters via Bayesian learning:

```
CONFIDENCE INTERVAL CONVERGENCE (Bayesian Shrinkage)
E(θ) = Epistemic Uncertainty (95% confidence band)

APAC_CAGR Parameter Learning:

Quarter │ Observations │ Parameter Estimate │ E(θ) Confidence │ Shrinkage Factor
─────────┼──────────────┼───────────────────┼─────────────────┼────────────────
Q0       │ 0 (prior)    │ 8.5%               │ ±1.5pp (Wide)   │ Baseline
(Jan-23) │              │                   │ [7.0% - 10.0%]  │
─────────┼──────────────┼───────────────────┼─────────────────┼────────────────
Q1       │ 1 (5.8%)     │ 7.8% (blend)       │ ±1.4pp          │ 87% confidence
(Apr-24) │              │ [6.4% - 9.2%]     │                 │ [λ = 20%]
─────────┼──────────────┼───────────────────┼─────────────────┼────────────────
Q2       │ 2 (6.2%)     │ 7.2% (updated)     │ ±1.0pp (Tighter)│ 91% confidence
(Jul-24) │              │ [6.2% - 8.2%]     │                 │ [λ = 33%]
─────────┼──────────────┼───────────────────┼─────────────────┼────────────────
Q3       │ 3 (6.8%)     │ 7.1% (converging)  │ ±0.8pp          │ 93% confidence
(Oct-24) │              │ [6.3% - 7.9%]     │                 │ [λ = 43%]
─────────┼──────────────┼───────────────────┼─────────────────┼────────────────
Q4       │ 4 (6.1%)     │ 7.0% (stabilized)  │ ±0.6pp (Tight)  │ 94% confidence
(Jan-25) │              │ [6.4% - 7.6%]     │                 │ [λ = 50%]
━━━━━━━━━┷━━━━━━━━━━━━━┷━━━━━━━━━━━━━━━━━┷━━━━━━━━━━━━━━━┷━━━━━━━━━━━━━━

INTERPRETATION:
  • Q0→Q1: Initial E(θ)=±1.5pp → Q1 actual (5.8%) was outside band (PARAMETER SHOCK)
  • Q1→Q2: Parameter revised to 7.2% based on 2 observations
  • Q2→Q4: E(θ) shrinks 33%→50% as observations accumulate
  • Key: After just 4 quarters, confidence interval 60% narrower than baseline!

  • Implication: New customers converge to ±0.6-0.8pp within 12-16 months
  • Recommendation: Use this learning curve to calibrate forecasts for board
```

#### Section 3: Deviation Attribution Analysis

Shows the 10C CORE decomposition of prediction errors:

```
ERROR DECOMPOSITION: Understanding Why Predictions Missed
(ΔP = Actual - Predicted | Attribution via Quarterly Review Framework)

ALPLA Q1 2024: €50M Revenue Miss (-2.0%)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total Deviation (ΔP): -€50M
├─ What caused it? (10C Attribution)

1. PARAMETER ERROR [WHERE: θ wrong] ................. -€20M (40%)
   Finding: APAC_CAGR predicted at 8.5%, actual came in at 5.8%
   Root Cause: Parameter estimate too optimistic based on prior forecasts
   Evidence: Sensitivity analysis shows €267M per 1pp CAGR
             × 2.7pp miss = ~€720M impact, but actual miss only €50M
             → Suggests partial offset from other factors

2. CONTEXT SHOCK [WHEN: Ψ changed] .................. -€25M (50%)
   Finding: APAC economic slowdown (GDP growth 2.8% → 1.9%)
   Root Cause: Ψ₁ (economic context) deteriorated unexpectedly
   Evidence: Other regions on track, only APAC underperformed
             → Structural, not parameter-driven

3. SEGMENT MIX DRIFT [WHAT: Portfolio shift] ....... +€10M (offset)
   Finding: Pharma segment outperformed (+15% vs +8% forecast)
   Root Cause: Unexpected Pharma demand surge (not forecast in WHAT weights)
   Evidence: Pharma elasticity drives revenue upside

4. MODEL MISSPECIFICATION [HOW: γ wrong] ........... -€15M (30%)
   Finding: Complementarity between revenue & headcount overstated
   Root Cause: Model assumed 1:1 revenue-headcount coupling
             Actual execution was more flexible (γ_rev-org = 0.52, not 0.68)

TOTAL: -€20M (WHERE) -€25M (WHEN) +€10M (WHAT) -€15M (HOW) = -€50M ✓

STRATEGIC INTERPRETATION:
  • Biggest factors: Context (50%) + Model error (30%)
  • Parameter error (40%) is real but smaller than realized
  • Silver lining: Pharma mix (+€10M) partially offsets APAC weakness
  • Lesson: Need better real-time context (Ψ₁ economic) monitoring
```

#### Section 4: Predictive Power & Velocity of Learning

Shows how quickly model predictions improve:

```
FORECAST ACCURACY IMPROVEMENT TRAJECTORY
(How fast does learning converge?)

Metric           │ Initial Forecast │ Q1 Actual │ Error │ Updated │ Q2 Check
                 │ (Q0)             │           │       │ Forecast│
─────────────────┼──────────────────┼───────────┼───────┼─────────┼──────────
APAC CAGR        │ 8.5% ± 1.5pp     │ 5.8%      │ -2.7pp│ 6.5%*   │ 6.2%  ✓
Revenue MAPE     │ Base 2.50B       │ 2.45B     │ -2.0% │ New 2.60│ 2.56B ✓
Headcount        │ 27.5K ± 500      │ 26.8K     │ -700  │ 27.8K*  │ 27.5K ✓
Capex            │ 240M ± 40M       │ 218M      │ -9.2% │ 260M*   │ 242M  ⚠

Learning Metrics:
  Prediction Accuracy Improvement: Q0→Q1 (-2.0%) → Q0→Q2 (-1.5%) → Q0→Q3 (-0.5%)
  Confidence Narrowing Rate: E(θ) shrinks ~5-8% per quarter
  Regime Change Detection: Caught APAC slowdown by Q2 (1-quarter lag)
  Velocity: Full parameter convergence in ~12 months (4-5 quarters)

  * Updated based on Q1 actual + Bayesian shrinkage formula
  ✓ Q2 actuals validate the updated forecast (TIGHT)
  ⚠ Capex still wide → governance process needs improvement
```

### Integration with Board Narrative

**Why Include Prediction Track Record?**

```
Board Concern:                        Track Record Response:
─────────────────────────────────────────────────────────────────────────
"Can we trust these forecasts?"       "Here's our 12+ quarter track record:
                                       Revenue accuracy ±2%, CAGR ±0.5pp"

"What if markets change?"              "Our learning loop adapts in 1 quarter.
                                       Q1 slowdown caught and forecast updated
                                       by Q2. Continuous improvement visible."

"How confident should we be?"          "Confidence bands narrowing visibly:
                                       ±1.5pp → ±0.6pp over 12 months.
                                       Bayesian shrinkage proves convergence."

"What could go wrong?"                 "Error decomposition shows:
                                       50% context risk (Ψ monitoring)
                                       30% model risk (complementarities)
                                       20% parameter risk (shrinking)"

"How often should we review?"          "Quarterly reviews have ≥80% predictive
                                       power within 1 quarter. Recommend
                                       monthly governance gate for top risks."
```

### How to Generate Track Record for Presentation

**Data Sources:**
- `data/intervention-registry.yaml` - Prediction vs actual tracking
- `data/customers/<company>/quarterly_review_Q<n>_20xx.json` - ΔP decomposition
- `data/models/registry/model_registry.yaml` - E(θ) update history

**Automation:**
```python
def generate_track_record_slide():
    """Extract prediction accuracy data for board presentation."""

    # Load all quarterly reviews
    reviews = load_quarterly_reviews(company_name)

    # Calculate accuracy metrics
    mape_by_model = calculate_mape_series(reviews)    # Revenue, headcount, capex
    e_theta_history = extract_e_theta_updates(reviews) # Confidence narrowing
    attribution = extract_error_decomposition(reviews) # WHERE/WHEN/WHAT/HOW

    # Compile for board slide
    return {
        'accuracy_table': mape_by_model,
        'confidence_convergence': e_theta_history,
        'error_attribution': attribution,
        'learning_velocity': calculate_shrinkage_rate(e_theta_history)
    }
```

**When to Update Track Record:**
- ✓ After each quarterly_review.py run (new actuals)
- ✓ After parameter_update_pipeline.py updates E(θ)
- ✓ Before board presentations (ensure latest data)
- ✓ For new customer proposals (use archetype track record)

### Example: Using Track Record to Build Board Confidence

**Scenario:** Presenting aggressive APAC growth forecast (8.5% CAGR) to skeptical board

**Without Track Record:**
- Board: "That's very aggressive. Why should we believe it?"
- Response: [Sensitivity analysis, models, assumptions...]
- Outcome: Modest confidence, extensive Q&A

**With Track Record:**
- Board: "That's aggressive. APAC slowed to 5.8% last year—why now?"
- Response: "Look at our track record:
  - Revenue forecasts accurate ±2% after 1 quarter
  - APAC parameter updated to 6.5% based on Q1 data
  - Q2 actual came in at 6.2% (tight convergence)
  - Current forecast 8.5% assumes Ψ₁ economic improvement back to 2.8% GDP
  - If economy improves (base case), forecast achievable
  - If not, our learning loop catches it by Q1 next year"
- Outcome: High confidence, constructive discussion on risk assumptions

---

## Workflow

### Step 1: Load All Model Outputs
```python
# Load from customer directory
revenue_df = pd.read_csv(f'data/customers/{company}/revenue_projection_2024_2035.csv')
mc_results = yaml.load(f'data/customers/{company}/monte_carlo_distribution.yaml')
headcount_df = pd.read_csv(f'data/customers/{company}/headcount_projection_2024_2035.csv')
capex_results = yaml.load(f'data/customers/{company}/capex_allocation.yaml')
sensitivity_df = pd.read_csv(f'data/customers/{company}/sensitivity_ranking_table.csv')
```

### Step 2: Extract Key Metrics
```python
metrics = {
  'revenue_2024': revenue_df[revenue_df['Year']==2024]['Total'].values[0],
  'revenue_2035': revenue_df[revenue_df['Year']==2035]['Total'].values[0],
  'cagr': calculate_cagr(revenue_2024, revenue_2035, 11),
  'headcount_2024': headcount_df[headcount_df['Year']==2024]['Total'].values[0],
  'headcount_2035': headcount_df[headcount_df['Year']==2035]['Total'].values[0],
  'mc_percentile_5': mc_results['percentiles']['5%'],
  'mc_percentile_95': mc_results['percentiles']['95%'],
  'total_capex': capex_results['total_capex_11_years'],
  'total_roi': capex_results['total_roi_percent'],
}
```

### Step 3: Generate Presentation Content

**For PDF/PowerPoint:** Use template library
```python
from templates.board_presentation_template import BoardPresentation

presentation = BoardPresentation(
  company_name=company_name,
  metrics=metrics,
  revenue_df=revenue_df,
  mc_results=mc_results,
  headcount_df=headcount_df,
  capex_results=capex_results,
  sensitivity_df=sensitivity_df
)

presentation.generate_slides()
```

**For Markdown:** Generate text-based slides
```markdown
# SLIDE 1: Executive Summary
[Content...]

# SLIDE 2: Strategic Scenarios
[Content...]
```

### Step 4: Add Visualizations
- Revenue trajectory chart (3 scenarios)
- Monte Carlo histogram + curve
- Regional mix stacked bar chart
- Headcount + payroll dual-axis chart
- Capex allocation waterfall
- Sensitivity tornado/spider chart
- Timeline/Gantt chart for roadmap

### Step 5: Generate Output File
```python
if format == 'pdf':
  presentation.export_pdf(f'data/customers/{company}/board_presentation_{date}.pdf')
elif format == 'powerpoint':
  presentation.export_pptx(f'data/customers/{company}/board_presentation_{date}.pptx')
elif format == 'markdown':
  presentation.export_md(f'data/customers/{company}/board_presentation_{date}.md')
```

### Step 6: Confirmation Output
```
✅ BOARD PRESENTATION GENERATED

Company: [Company Name]
Slides: 10 (executive summary → recommendation)
Scenarios: 3 (Conservative, Base, Optimistic)
Charts: 8 visualizations

File: data/customers/<company>/board_presentation_20260115.pdf
Size: ~2.5 MB
Ready for: Board meeting, investor presentation, internal alignment

Presentation Contents:
  ✓ Slide 1: Executive Summary (key metrics)
  ✓ Slide 2: 3 Strategic Scenarios
  ✓ Slide 3: Monte Carlo Confidence (97.9% probability)
  ✓ Slide 4: Regional Drivers
  ✓ Slide 5: Org Scaling
  ✓ Slide 6: Capex & ROI
  ✓ Slide 7: 3-Phase Roadmap
  ✓ Slide 8: Sensitivity Analysis
  ✓ Slide 9: Competitive Position
  ✓ Slide 10: Board Recommendation & Next Steps

Next: Share with board, schedule decision meeting
```

---

## Customization Options

### Style Themes
- **Professional:** Formal, minimal design
- **Clean:** Modern, data-focused
- **Creative:** Colorful, narrative-driven
- **Academic:** Technical, detailed references

### Branding
- Company logo (if provided)
- Color scheme (brand colors)
- Font selection
- Header/footer customization

### Content Options
- Include/exclude sensitivity analysis
- Detailed vs. executive-level charts
- Reference materials & appendix
- Contact information

---

## Output Locations

All presentations saved to:
```
data/customers/<company>/board_presentation_<YYYYMMDD>.<extension>
```

**Example:**
```
data/customers/alpla/board_presentation_20260115.pdf
data/customers/alpla/board_presentation_20260115.pptx
data/customers/alpla/board_presentation_20260115.md
```

---

## Prerequisites

Before running this skill:
1. ✓ `/new-customer` - Customer created
2. ✓ `/apply-models` - All 4 models executed
3. ✓ Optional: `/sensitivity-analysis` - For slide 8

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Missing model outputs | Models not run | Run /apply-models first |
| Invalid format | Unsupported output type | Use: pdf, pptx, md, html, tex |
| Chart generation failed | Missing data | Verify all model outputs present |
| File write failed | Permission issue | Check directory permissions |

---

## FAQ

**Q: Can I edit the presentation after generation?**
A: Yes, PowerPoint format is fully editable (.pptx)
   PDF is for printing/sharing only

**Q: How long does generation take?**
A: < 2 minutes including visualizations

**Q: Can I customize the slides?**
A: Yes, use templates in `templates/board_presentation_template.py`

**Q: Should I include appendices?**
A: Optional - presentation includes full details, appendix can have raw data

---

## EBF Session Mode (NEU v1.19)

### Übersicht

Zusätzlich zur Customer Strategy Präsentation kann `/board-presentation` jetzt auch **EBF Model-Building Sessions** in Präsentationen umwandeln.

### Verwendung

```bash
# EBF Session → Board Präsentation
/board-presentation --session EBF-S-2026-01-26-COG-001

# Mit Zielgruppen-Auswahl (8D-Profil)
/board-presentation --session EBF-S-2026-01-26-COG-001 --audience board
/board-presentation --session EBF-S-2026-01-26-COG-001 --audience science
/board-presentation --session EBF-S-2026-01-26-COG-001 --audience client

# Mit automatischer Grafik-Generierung
/board-presentation --session EBF-S-2026-01-26-COG-001 --audience board --generate-graphics
```

### Verfügbare Zielgruppen (8D-Profile)

| Profil | D4 (Zeit) | Slides | Beschreibung |
|--------|-----------|--------|--------------|
| `board` | 0.2 | 5-7 | C-Level, strategisch, wenig Zeit, Handlung |
| `management` | 0.35 | 8-12 | Geschäftsleitung, operativ |
| `team` | 0.55 | 12-18 | Projektteam, technisch, Information |
| `science` | 0.8 | 18-25 | Wissenschaft, viel Zeit, Paper-Qualität |
| `client` | 0.4 | 8-12 | Externer Kunde, überzeugend |

### 8D-Dimensionen

Die Slide-Architektur emergiert automatisch aus den 8D-Koordinaten:

| D | Dimension | Wirkung |
|---|-----------|---------|
| D1 | Wissen | Text-Komplexität, Fachvokabular |
| D2 | Nähe | Technisches Detail |
| D3 | Reichweite | Scope (persönlich → gesellschaftlich) |
| D4 | Zeit | **Slide-Anzahl** (wenig → viele) |
| D5 | Ziel | **Slide-Typen** (G1=Info, G2=Handeln, G3=Überzeugen) |
| D6 | Kontext | Formalität (intern → extern) |
| D7 | Emotion | **Content-Balance** (Charts vs Text vs Whitespace) |
| D8 | Persistenz | Archiv-Qualität |

### Generierte Slide-Typen

| Slide-Typ | Zweck | Bei Ziel |
|-----------|-------|----------|
| `TITLE` | Titelfolie mit Session-Info | Alle |
| `EXECUTIVE_SUMMARY` | Key Finding + KPIs | G1, G2, G3 |
| `DATA_CHART` | Automatische Charts aus Model | G1, G2, G3 |
| `IMPLICATIONS` | 4 Kacheln mit Handlungsempfehlungen | G2, G3 |
| `CALL_TO_ACTION` | Nächste Schritte mit Checkboxen | G2, G3 |
| `METHODOLOGY` | Modell-Beschreibung | G1 |
| `SOURCES` | Quellen + Kontakt | Alle |

### Automatische Grafiken

Wenn `--generate-graphics` aktiviert, werden folgende Charts generiert:

| Grafik | Typ | Datenquelle |
|--------|-----|-------------|
| `cognitive_hierarchy_bar.png` | Horizontales Balkendiagramm | model.cognitive_hierarchy |
| `v_n_decay_line.png` | Liniendiagramm | model.example_results |
| `sensitivity_donut.png` | Donut-Chart | model.sensitivity |
| `formula.png` | LaTeX-Formel | model.functional_form |

### Konfigurationsdateien

| Datei | Zweck |
|-------|-------|
| `templates/pptx/fa-style.yaml` | FehrAdvice Farben, Fonts, Layouts |
| `templates/pptx/slide-types.yaml` | Slide-Definitionen mit Elementen |
| `templates/pptx/8d-slide-mapping.yaml` | 8D → Slide-Architektur |
| `templates/pptx/graphic-mapping.yaml` | Daten → Chart Definitionen |

### Scripts

```bash
# Nur Grafiken generieren
python scripts/generate_graphics.py --session EBF-S-2026-01-26-COG-001

# Nur PPTX generieren (Grafiken müssen existieren)
python scripts/generate_pptx.py --session EBF-S-2026-01-26-COG-001 --audience board

# Beides zusammen
python scripts/generate_pptx.py --session EBF-S-2026-01-26-COG-001 --audience board --generate-graphics

# Custom 8D-Profil
python scripts/generate_pptx.py --session EBF-S-2026-01-26-COG-001 --custom-8d "0.4,0.3,0.85,0.2,G2,0.9,0.4,0.6"

# Verfügbare Audiences auflisten
python scripts/generate_pptx.py --list-audiences
```

### Output

```
outputs/sessions/{session_id}/presentation_{audience}.pptx
```

Beispiel:
```
outputs/sessions/EBF-S-2026-01-26-COG-001/presentation_board.pptx
```

### Workflow-Integration

Der EBF Session Workflow (Schritt 9) kann direkt in eine Präsentation münden:

```
Schritt 0-8: EBF Session durchführen
    ↓
Schritt 9: Output wählen
    ↓
Format: PPT | Umfang: 1-pager (board)
    ↓
/board-presentation --session {SESSION_ID} --audience board
    ↓
✅ Präsentation generiert
```

---

**Skill Status:** ACTIVE
**Last Updated:** 2026-01-26
**Version:** 1.1.0
