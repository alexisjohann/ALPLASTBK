# Phase 6: Operational Workflow Guide

**Long-Term Outcome Tracking in Practice**

Detailed step-by-step instructions for implementing Phase 6.

---

## Phase 6 Workflow Overview

```
MONTH 0-6: Project Implementation (Phase 5)
│
└─→ MONTH 6: Phase 5 Results (initial measurement & learnings)
   │
   └─→ MONTH 6.5: Phase 6 STARTS
      ├─ Schedule 3M, 6M, 12M, 24M follow-ups
      │
      └─→ MONTH 9: 3M Measurement
         ├─ Detect early decay
         ├─ Check for unexpected attrition
         │
         └─→ MONTH 12: 6M Measurement (GOLD STANDARD)
            ├─ Highest quality data
            ├─ Check booster thresholds
            ├─ Fit decay model
            │
            └─→ MONTH 18: 12M Measurement (SUSTAINABILITY VERDICT)
               ├─ Calculate sustainability score
               ├─ Trigger boosters if needed
               ├─ Extract learnings
               │
               └─→ MONTH 30: 24M Measurement (OPTIONAL)
                  └─ Long-term maintenance assessment
```

---

## Workflow Steps

### Step 1: Schedule Follow-Ups (Month 6, ~1 hour)

**When**: Immediately after Phase 5 results are documented

**Command**:
```bash
/phase6-manage schedule PRJ-001
```

**What Happens**:
- System creates schedule with dates
- Sends notifications for upcoming measurements
- Sets up reminders for coordinators

**Checklist**:
- [ ] Phase 5 results finalized
- [ ] Project end date documented
- [ ] Schedule confirmed (use defaults or custom)
- [ ] Measurement team identified

**Output to Review**:
```json
{
  "measurement_points": [
    {
      "timepoint": "3M",
      "scheduled_date": "2026-03-30",
      "priority": "high",
      "status": "pending"
    },
    ...
  ]
}
```

**Questions to Answer**:
- Who will coordinate measurement collection?
- What's the contact process for participants?
- How will you manage non-response?

---

### Step 2a: Record 3-Month Measurement (Month 9, ~2 hours)

**When**: 3 months post-intervention end date

**Prepare Data**:
1. Conduct survey or pull administrative data
2. Format as JSON:
```json
{
  "participation_rate": 0.88,
  "satisfaction_score": 7.8,
  "behavior_frequency": 4.2
}
```

**Command**:
```bash
/phase6-manage record PRJ-001 3M --file survey_3m.json

# OR interactive entry
/phase6-manage record PRJ-001 3M --interactive
```

**What Happens**:
- System records measurement
- Calculates attrition rate
- Flags unexpected attrition
- Updates registry

**Checklist**:
- [ ] Data collected and quality-checked
- [ ] Sample size documented
- [ ] Missing data handled (imputation or reported)
- [ ] Attrition rate calculated

**Questions to Answer**:
- What sample size was achieved? (Compare to expected 80%)
- Any systematic differences between responders/non-responders?
- Were there measurement issues?

**Expected Patterns**:
- Attrition: ~20% (normal)
- Effect retention: Usually 85-95% (some decay expected)
- Satisfaction: Usually stable or slightly improved

**Red Flags** (investigate):
- Attrition > 30% (selection bias risk)
- Effect < 70% of initial (rapid decay starting)
- Satisfaction dropped (dissatisfaction emerging)

---

### Step 2b: Record 6-Month Measurement (Month 12, ~1 hour)

**When**: 6 months post-intervention end date

**Why 6M is Special**:
- Usually achieves 100% sample (administrative data)
- Best data quality
- Clear picture of mid-term sustainability
- Enough data to fit decay model

**Prepare Data**:
```json
{
  "participation_rate": 0.85,
  "usage_frequency": 3.8
}
```

**Command**:
```bash
/phase6-manage record PRJ-001 6M --file admin_6m.json
```

**What Happens**:
- System fits decay model (exponential by default)
- Estimates decay rate (ρ)
- Calculates sustainability trajectory

**Checklist**:
- [ ] Administrative data verified and complete
- [ ] No missing records (100% sample ideally)
- [ ] Data quality checks passed
- [ ] Decay model fit confirmed

**Expected Patterns**:
- Attrition: ~0% (administrative data)
- Effect retention: 75-90% is typical
- Decay model R² > 0.80

**Critical Decision Point**:
- Is effect decaying slowly (sustainable)?
- Or rapidly (booster needed)?

---

### Step 3: Analyze Decay (Month 12, ~30 minutes)

**When**: After 6M measurement recorded

**Command**:
```bash
/phase6-manage analyze PRJ-001
```

**Output**:
```json
{
  "fitted_parameters": {
    "rho": 0.0823,        # Monthly decay rate
    "E_0": 0.5700,        # Initial effect
    "t_half": 8.4         # Months to 50% effect
  },
  "model_fit": {
    "R_squared": 0.923,
    "model_quality": "good"
  },
  "predictions": {
    "3M": 0.5418,
    "6M": 0.5163,
    "12M": 0.4697,
    "24M": 0.3862
  }
}
```

**How to Interpret**:

| Decay Rate (ρ) | Interpretation | Action |
|---|---|---|
| ρ < 0.05 | Very sustainable (slow decay) | No booster likely needed |
| 0.05-0.10 | Sustainable with minor fade | Booster at 12M consider |
| 0.10-0.15 | Moderate decay | Booster at 6M+12M needed |
| ρ > 0.15 | Rapid decay | Design review required |

**Model Quality**:
- R² > 0.90: Excellent fit
- R² > 0.80: Good fit
- R² > 0.70: Acceptable
- R² < 0.70: Weak fit (investigate)

**Next Steps**:
1. If R² < 0.80: Check data quality, consider linear model
2. If ρ > 0.12: Plan booster interventions
3. If ρ < 0.05: Schedule light check-in at 12M

---

### Step 4: Check Booster Thresholds (Month 12, ~15 minutes)

**When**: After decay model fitted (Step 3)

**Command**:
```bash
/phase6-manage check-decay PRJ-001
```

**What It Does**:
- Evaluates if effect has dropped below trigger thresholds
- Determines booster type and urgency
- Updates registry if booster needed

**Thresholds**:
- Effect < 80% of initial → Reminder booster (light)
- Effect < 60% of initial → Re-engagement booster (medium)
- Effect < 40% of initial → Structural intervention (heavy)

**Output**:
```json
{
  "timepoint": "6M",
  "effect_retention_pct": 0.74,
  "trigger_booster": true,
  "booster_type": "reminder",
  "urgency": "medium",
  "recommendation": "Schedule light reminder intervention for 12M"
}
```

**Decision Tree**:

```
Is effect_retention > 80%?
├─ YES → No booster needed (yet)
│       └─ Continue to 12M measurement
└─ NO → Check urgency
        ├─ retention > 60%? → Light reminder booster
        ├─ retention > 40%? → Medium re-engagement booster
        └─ retention < 40%? → Critical: design review needed
```

---

### Step 5: Calculate Sustainability Score (Month 18, ~15 minutes)

**When**: After 12M measurement recorded

**Command**:
```bash
/phase6-manage score PRJ-001
```

**What It Does**:
- Formula: S = (E₁₂M / E₀) × √(1 - attrition)
- Classifies sustainability level
- Recommends maintenance strategy

**Output**:
```json
{
  "sustainability_score": 0.756,
  "effect_retention": 0.823,
  "attrition_adjustment": 0.918,
  "classification": "Moderately sustainable",
  "recommended_action": "Booster at 12M recommended",
  "priority": "medium"
}
```

**Sustainability Classification**:

| Score | Classification | Meaning | Action |
|---|---|---|---|
| ≥ 0.80 | Highly sustainable | Effect stable long-term | Maintenance check annually |
| 0.60-0.79 | Moderately sustainable | Minor fade expected | Booster at 12M |
| 0.40-0.59 | Moderate decay | Noticeable fade | Boosters at 6M+12M |
| < 0.40 | Rapid decay | Fast reversion | Redesign or continuous support |

**The Story of Your Score**:
- **0.823 effect retention**: 82% of initial effect remains
- **0.918 attrition adjustment**: Only modest impact from sample loss
- **0.756 final score**: Moderately sustainable

**Interpretation**: "Behavior is holding up reasonably well at 12M, but showing some fade. A light booster will likely maintain it at 0.85+ for another 12 months."

---

### Step 6: Execute Booster Intervention (Month 18-19, if needed)

**When**: If sustainability score recommends boosters

**Booster Types by Urgency**:

**Option 1: Light Reminder (if S ≥ 0.65)**
- Goal: Reactivate attention, reset defaults
- Example: "It's been a year! How's your {behavior} going?"
- Effort: 1-2 hours for communication
- Cost: Low
- Expected effect: +0.05 recovery

**Option 2: Medium Re-Engagement (if 0.40 ≤ S < 0.65)**
- Goal: Rebuild motivation, refresh benefits
- Example: Updated communication with new social proof
- Effort: 4-6 hours including design
- Cost: Medium
- Expected effect: +0.08 recovery

**Option 3: Heavy Structural (if S < 0.40)**
- Goal: Redesign intervention for sustainability
- Example: Strengthen defaults, enhance complementarities
- Effort: 20-40 hours (new design cycle)
- Cost: High
- Expected effect: New baseline

**Execution Steps**:
1. Identify which interventions degraded most (from Phase 5 results)
2. Design booster based on type chosen above
3. Implement at 12M mark
4. Document results

---

### Step 7: Record 12-Month Booster Results (Month 21, ~2 hours)

**When**: 3 months after booster intervention

**Command**:
```bash
/phase6-manage record PRJ-001 12M-post-booster --file booster_results.json
```

**Measure**:
- Did booster work? (Effect recovered?)
- Which participants responded? (segment analysis)
- Cost-benefit of booster? (benefit vs effort)

**Output**:
```json
{
  "effect_pre_booster": 0.48,
  "effect_post_booster": 0.56,
  "recovery_pct": 0.17,
  "booster_effectiveness": "moderate",
  "recommendation": "Light re-engagement every 12M maintains behavior"
}
```

---

### Step 8: Extract Learnings (Month 21, ~1 hour)

**When**: After complete 12M+ cycle with booster results

**Commands**:
```bash
# Get sustainability patterns
/phase6-manage patterns --domain [YOUR_DOMAIN]

# Get decay parameters
/phase6-manage analyze PRJ-001 --export-parameters

# Get maintenance strategy
/phase6-manage maintenance PRJ-001

# Generate full report
/phase6-manage report PRJ-001 --format html
```

**Learnings to Extract**:

1. **Decay Patterns**:
   - "Defaults decay slower (ρ=0.03) than reminders (ρ=0.15)"
   - "DACH context: values persist longer than US literature suggests"

2. **Booster Effectiveness**:
   - "Reminder boosters: 65% effective in this domain"
   - "Re-engagement boosters: better for rational-calculative segment"

3. **Segment Insights**:
   - "Present-biased segment: sustains defaults very well"
   - "Rational-calculative: fades quickly without social reinforcement"

4. **Parameter Updates**:
   ```
   Old: ρ[nudge-default, general] = 0.05
   New: ρ[nudge-default, DACH, finance] = 0.03
   Basis: n=3 projects, 12M+ tracking
   ```

---

### Step 9: Optional - 24-Month Extended Tracking (Month 30)

**When**: 24 months post-intervention (optional, lower priority)

**Command**:
```bash
/phase6-manage record PRJ-001 24M --file extended_results.json
```

**Purpose**:
- Very long-term sustainability assessment
- Identify if behavior becomes "habit" (automatic)
- Test effect permanence vs booster dependency

**Expected**:
- High attrition (40-60%, normal at 24M)
- Effect usually stabilizes (not further decay)
- Good candidates for annual check-ins

---

## Phase 6 Timeline & Coordination

### Coordinating Multiple Projects

```
Project Timeline:
PRJ-001: |---IMPL (0-6M)---|----3M-----|----6M-----|-----12M-----|-----24M-----|
PRJ-002:                   |---IMPL----|----3M-----|----6M-----|-----12M-----|
PRJ-003:                                 |---IMPL----|----3M-----|----6M-----|
```

**Recommended Rhythm**:
- **Monthly**: `/phase6-manage pending` (track upcoming measurements)
- **Quarterly**: `/phase6-manage patterns` (extract emerging patterns)
- **Bi-annually**: `/phase6-manage meta-analysis` (cross-project synthesis)

---

## Quality Assurance

### Measurement Quality Checklist

At **each measurement**, verify:

- [ ] **Sample composition**: n ≥ 30, describe characteristics
- [ ] **Response rate**: Report actual % (and vs expected)
- [ ] **Data completeness**: Any missing values? How handled?
- [ ] **Measurement validity**: Used validated scales? Describe method
- [ ] **Timing**: Exactly at scheduled timepoint? Document any delays
- [ ] **Attrition patterns**: Compare completers vs non-completers

### Data Quality Issues & Remedies

| Issue | Action |
|---|---|
| Attrition > 50% | Use weighted analysis, note selection bias risk |
| Missing data > 10% | Use multiple imputation, document method |
| Low survey response | Use administrative data as supplement |
| Conflicting reports | Investigate source, document discrepancy |
| Measurement changed | Note in report, consider sub-group analysis |

---

## Integration with Next Project Design

### Using Phase 6 Learnings in Phase 5 (New Projects)

```
Phase 6 Output:
├─ Decay rates (ρ) by intervention type & domain
├─ Booster effectiveness data
├─ Sustainability patterns
└─ Segment-specific insights

↓

Phase 5 Input (Next Project):
├─ Design interventions with decay-aware E_i values
├─ Include decay rates in Parameter Repository (BBB)
├─ Select interventions with proven sustainability (S ≥ 0.75)
└─ Tailor to segments with historical data
```

**Example: Designing Health Project Based on Phase 6 Learnings**

```
From Phase 6: "Nudge-default (ρ=0.03) + Social (ρ=0.06) sustains well
               Gamification (ρ=0.18) fades rapidly"

New Project Design:
├─ Use default + social combination
├─ Avoid gamification or limit to initial 3 months
├─ Plan booster at 12M (from historical data)
└─ Design with S ≥ 0.75 target (achievable)
```

---

## Troubleshooting

### Problem: Can't reach participants at 12M

**Solution Options**:
1. Use administrative data as proxy (if available)
2. Use last-observed-carried-forward (LOCF) - conservative estimate
3. Switch to shorter booster cycle (6M instead of 12M)
4. Document as "non-response" and weight results

### Problem: Effect decayed faster than expected (ρ > 0.15)

**Diagnostic Steps**:
1. Check intervention fidelity: Did it stay in place?
2. Environmental change: Did something change that removed trigger?
3. Habituation: Did salience fade despite intervention?
4. Measurement error: Check data quality

**Remedies**:
1. Increase booster frequency (6M instead of 12M)
2. Redesign intervention for structural embedding
3. Add social reinforcement component
4. Consider if behavior was only context-dependent

### Problem: Attrition > 50% at 12M

**Diagnostic**:
- Is attrition random or systematic?
- Check: Did specific segments drop out? (e.g., job changes, mobility)

**Analysis**:
- Use weighted estimators
- Compare completer vs non-completer baseline behavior
- Report findings with caveats

**Document**:
- "Attrition rate: 52% (n=187 → n=90)"
- "Likely due to natural job transitions in organization"
- "Results weighted by inverse probability of response"

---

## Real Example: PRJ-001 Timeline

### Month 6: Phase 5 Results (Initial)
```
→ Predicted: 52% | Actual: 57% (underestimate by 5pp)
→ Recommendation: Monitor long-term sustainability
```

### Month 6.5: Schedule Follow-Ups
```bash
/phase6-manage schedule PRJ-001
```
**Result**: 3M/6M/12M/24M scheduled

### Month 9: 3M Measurement
```bash
/phase6-manage record PRJ-001 3M --file survey_3m.json
```
- Sample: 250/312 (80%) ✓ Expected attrition
- Effect: 0.54 vs predicted 0.54 ✓ On track
- Satisfaction: 7.8/10 ✓ Maintained

### Month 12: 6M Measurement
```bash
/phase6-manage record PRJ-001 6M --file admin_6m.json
/phase6-manage analyze PRJ-001
```
- Sample: 312/312 (100%) ✓ Administrative data complete
- Effect: 0.52 vs predicted 0.52 ✓ Excellent
- Decay model: ρ = 0.0823 (good fit, R² = 0.923)

### Month 12.5: Check Decay Threshold
```bash
/phase6-manage check-decay PRJ-001
```
- Effect retention: 91% (> 80%) ✓ No booster trigger yet

### Month 18: 12M Measurement
```bash
/phase6-manage record PRJ-001 12M --file survey_12m.json
/phase6-manage score PRJ-001
```
- Sample: 187/312 (60%) ✓ Expected attrition
- Effect: 0.48 vs predicted 0.47 ✓ Prediction accurate
- Sustainability score: 0.756 → "Moderately sustainable"

### Month 18.5: Extract Learnings
```bash
/phase6-manage report PRJ-001 --format html
/phase6-manage patterns --domain finance
```

**Key Learnings**:
- "Defaults in DACH maintain 91% effect at 6M"
- "ρ = 0.08 for this financial service domain"
- "Annual light reminder maintains behavior"

---

## FAQ

**Q: Do I need to measure all four timepoints?**
A: Minimum 6M (required for decay model). 12M is strongly recommended for sustainability verdict. 3M and 24M are optional.

**Q: What if participants have moved/left?**
A: Document attrition by type. Use administrative data if available. Weight analysis if attrition > 40%.

**Q: How do I use these learnings in next project?**
A: Share with design team. Incorporate decay rates into parameter estimation. Use booster schedule as baseline.

**Q: What's the cost of Phase 6?**
A: Varies by domain. Typical: 10-30 hours over 24 months (mostly measurement collection). Booster cost: 5-20 hours if needed.

**Q: Can I skip 6M measurement?**
A: Not recommended. 6M is usually only time you get 100% administrative data. 6M-12M gap risks missing decay pattern.

---

**Next:** See `.claude/commands/phase6-manage.md` for CLI reference
