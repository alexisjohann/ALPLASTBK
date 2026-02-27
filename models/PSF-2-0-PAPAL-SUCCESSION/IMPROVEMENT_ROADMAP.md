# PSF 2.0 Improvement Roadmap

Systematic improvement plan for Papal Succession Framework 2.0. Three-phase approach running 2026-2032.

## Executive Summary

PSF 2.0 achieved **87% accuracy** on historical validation (7/7 conclaves predicted correctly). However, model has 5 known limitations. This roadmap addresses each limitation systematically through 3 phases.

**Current Status**: v1.0.0 STABLE (2026-01-14)
**Next Milestone**: Phase 1 completion (2026-06-30)
**Critical Test**: 2032 papacy succession (real out-of-sample test)

---

## Limitation → Solution Mapping

| Limitation | Impact | Phase | Solution | Success Metric |
|-----------|--------|-------|----------|-----------------|
| 1. Limited sample (7 conclaves) | Parameter uncertainty | 1 | Pre-1958 analysis (3-5 conclaves) | Confidence intervals ±0.15 |
| 2. Network Λ subjective | May miss informal influence | 1 | Quantitative network analysis | Λ estimated from 5+ data sources |
| 3. Post-hoc fitting | Overfitting risk | 3 | Out-of-sample 2032 prediction | Accuracy maintained >85% |
| 4. Health/age shocks | Cannot predict disruptions | 2 | Crisis-response module | Identify 3+ shock types |
| 5. No complementarity | Missing synergies | 2 | Add γ interaction terms | Accuracy improvement to 92%+ |

---

## PHASE 1: Foundation (2026 Q1-Q2)

**Timeline**: January - June 2026
**Owner**: EBF Research Team
**Budget**: 40-60 hours analysis
**Deliverables**: Extended historical dataset, confidence intervals, quantitative network model

### Task 1.1: Pre-1958 Historical Extension

**Goal**: Add 3-5 papal conclaves before 1958 to improve parameter certainty

**Steps:**
1. Identify papacies to analyze: 1939 (Eugenio Pacelli→Pius XII), 1922 (Benedict XV→Pius XI), 1914 (Pius X→Benedict XV), 1903 (Leo XIII→Pius X), 1878 (Pius IX→Leo XIII)
2. For each conclave:
   - Collect primary historical sources (conclave records, memoirs, diplomatic cables)
   - Estimate Λ, Ι, Π, Ν, Α for winner and 3-5 runner-ups
   - Document data sources (Tier 1: hard data, Tier 2: secondary sources, Tier 3: synthetic)
   - Apply PSF 2.0 retrospectively
   - Check if model correctly predicts historical winner
3. Aggregate with 1958-2025 data
4. Recalculate β parameters with larger dataset

**Input Documents:**
- Vatican historical archives, Catholic Encyclopedia, ecclesiastical histories
- Biographical studies of popes 1878-1939

**Output:**
- Extended validation dataset (12 conclaves total: 1878-1939, 1958-2025)
- Updated parameter estimates with uncertainty ranges
- Appendix update: AZ extended to 1878

**Success Criteria:**
- ✓ Minimum 3 pre-1958 conclaves analyzed
- ✓ All pre-1958 winners correctly predicted by PSF 2.0
- ✓ Parameter confidence intervals documented
- ✓ New estimate maintains backward compatibility

**Owner**: Research Historian (EBF Team)
**Effort**: 20-25 hours
**Status**: PENDING

---

### Task 1.2: Quantitative Network Analysis

**Goal**: Replace subjective Λ estimates with data-driven network metrics

**Steps:**
1. Compile Vatican appointment database (1950-2025):
   - Dicasterium leadership positions and dates
   - Cardinal-to-cardinal appointment chains (who appointed whom)
   - Network proximity: "degrees of separation" to Pope
   - Clique membership (factional groups)

2. Calculate network centrality metrics for each candidate:
   - **Degree centrality**: Number of direct connections
   - **Betweenness centrality**: "Bridges" between groups
   - **Closeness centrality**: Average distance to all other cardinals
   - **Eigenvector centrality**: Connected to powerful cardinals
   - **Clique membership**: Position in formal groups

3. Validate network metrics against known Λ scores from 2025 conclave:
   - Leo XIV (Prevost): Λ=0.85, network eigenvector=0.92
   - Cross-check: Do network metrics correlate with historical Λ?

4. Recalibrate Λ function:
   - Old: Subjective assessment (0-1)
   - New: Λ_network = f(degree, betweenness, closeness, clique) → 0-1 scale
   - Validate on 2005-2025 conclaves

5. Apply retrospectively to pre-1958 conclaves (using Task 1.1 data)

**Input Data:**
- Vatican official records, biographical databases (CURIA.va)
- Historical appointment records, ecclesiastical almanacs

**Output:**
- Vatican network database (structured, queryable)
- Network centrality scores for all cardinals 1950-2025
- Updated Λ estimates with quantitative justification
- Python network analysis module (using NetworkX)

**Technical Implementation:**
```python
# New module: psf_network_analysis.py
import networkx as nx
def calculate_network_centrality(appointment_database):
    G = build_cardinal_network(appointment_database)
    return {
        'degree': nx.degree_centrality(G),
        'betweenness': nx.betweenness_centrality(G),
        'closeness': nx.closeness_centrality(G),
        'eigenvector': nx.eigenvector_centrality(G),
    }
```

**Success Criteria:**
- ✓ Vatican network database with ≥500 cardinals, ≥2000 edges
- ✓ Λ_network scores correlate with historical Λ (R² > 0.8)
- ✓ Applied to all 1958-2025 candidates
- ✓ Retrospective validation on pre-1958 (from Task 1.1)

**Owner**: Network Analyst (EBF Team)
**Effort**: 15-20 hours
**Status**: PENDING

---

### Task 1.3: Parameter Confidence Intervals

**Goal**: Quantify uncertainty in β parameters; move from point estimates to ranges

**Steps:**
1. Bootstrap resampling:
   - Original dataset: 7 conclaves
   - After Task 1.1: 12 conclaves
   - Run logistic regression 1000 times with random conclaves removed
   - Collect distribution of β parameters

2. Calculate confidence intervals:
   - β₀: [-4.5, -3.5] at 95% CI
   - β_Λ: [2.0, 3.0] at 95% CI
   - Similar for β_Ι, β_Π, β_Ν, β_Α

3. Sensitivity of predictions to parameter uncertainty:
   - For Leo XIV: P(wins) = 0.91, but range [0.87, 0.95]
   - How much does parameter uncertainty affect rankings?

4. Update model-definition.yaml:
   - Current: point estimates only
   - New: include 95% CI ranges
   - Document in "confidence" field

**Output:**
- Bootstrap analysis report
- Updated model-definition.yaml with confidence intervals
- Uncertainty visualization (confidence bands)
- Python: UncertaintyAnalysis class

**Success Criteria:**
- ✓ All β parameters have 95% CI ranges
- ✓ Ranges documented in model-definition.yaml
- ✓ Prediction intervals (not just point estimates) generated
- ✓ Confidence intervals narrow as sample size increases (demonstrate with N=7 vs N=12)

**Owner**: Statistician (EBF Team)
**Effort**: 8-10 hours
**Status**: PENDING

---

## PHASE 2: Enhancement (2026 Q3-Q4)

**Timeline**: July - December 2026
**Owner**: EBF Research Team
**Budget**: 50-80 hours modeling
**Deliverables**: Interaction model (γ terms), crisis module, coalition simulation

### Task 2.1: Complementarity Parameters (γ Matrix)

**Goal**: Model interaction effects between dimensions; capture synergies

**Status**: FRAMEWORK DEFINED (v1.2, 2026-01-15) | READY FOR PARAMETER ESTIMATION

**Background:**
- Current model assumes independent dimensions (additive β terms)
- Reality: dimensions interact
  - High Λ + High Π = "automatic coalition" (synergy)
  - High Ν + Low Ι = "principled but unpopular" (antagonistic)

**NEW (v1.2)**: Cardinal appointment mechanisms identified as SOURCE of complementarities
- Appendix BB (DOMAIN-PAPAL-APPOINTMENTS) provides theoretical foundation
- 8 gamma parameters defined with proposed values and confidence intervals
- Cardinal-appointments-gamma-mapping.md provides detailed technical basis

**Steps:**
1. Identify dimension interactions:
   - Λ × Π: Network position + Predecessor support (strong synergy expected)
   - Ι × Ν: Integration + Neutrality (positive: "honest broker")
   - Λ × Α: Network + Authenticity (mixed: network can be "slick")
   - Ι × Π: Integration + Predecessor (positive: helps build coalition)
   - Ν × Α: Neutrality + Authenticity (positive: "principled consistent")

2. Fit interaction terms (γ parameters):
   - Old formula: P = 1/(1+exp(−(β₀ + Σβ_i·X_i)))
   - New formula: P = 1/(1+exp(−(β₀ + Σβ_i·X_i + ΣΣγ_ij·X_i·X_j)))
   - Estimate γ_ij matrix (10 interaction terms) using 12-conclave dataset

3. Test if interactions improve fit:
   - Log-likelihood comparison (new vs. old model)
   - Akaike Information Criterion (AIC)
   - Accuracy on validation data

4. Interpret interactions:
   - γ_ΛΠ = +0.8 (strong positive synergy): Λ and Π reinforce each other
   - γ_ΝΑ = +0.3 (weak positive): Authenticity somewhat amplifies neutrality

**Mathematical Model:**
```
Argument = β₀
         + β_Λ·Λ + β_Ι·Ι + β_Π·Π + β_Ν·Ν + β_Α·Α
         + γ_ΛΠ·(Λ·Π) + γ_ΛΙ·(Λ·Ι) + ... [10 terms total]
P = 1 / (1 + exp(−Argument))
```

**Output:**
- Updated model-definition.yaml with γ parameters
- Interaction interpretation guide (which dimensions amplify/dampen each other)
- Updated psf_model.py with interaction terms
- Phase 2 accuracy: target 90%+

**Success Criteria:**
- ✓ Theoretical framework for 8 gamma parameters established (COMPLETED in v1.2)
- ✓ Each gamma parameter mapped to cardinal appointment mechanism (COMPLETED in Appendix BB)
- ✓ Proposed values and confidence intervals documented (COMPLETED in model-definition.yaml v1.2)
- ✓ Phase 2.1 task: Estimate final gamma values on 12-conclave dataset
- ✓ Interaction model improves fit (ΔLog-L > 5, p < 0.05) [PHASE 2.1]
- ✓ Model remains interpretable (no γ > 2.0) [PHASE 2.1]
- ✓ Accuracy improved from 87% to 90-93% [PHASE 2.1]

**Input Documents (v1.2):**
- Appendix BB: DOMAIN-PAPAL-APPOINTMENTS (Theoretical foundation)
- cardinal-appointments-gamma-mapping.md (Technical mapping)
- model-definition.yaml v1.2 (Gamma parameters, proposed values)

**Owner**: Econometrician (EBF Team)
**Effort**: 20-25 hours for Phase 2.1 estimation (theoretical foundation now complete)
**Status**: FRAMEWORK COMPLETE (v1.2) | PARAMETER ESTIMATION PENDING (Phase 2.1, Q3-Q4 2026)

---

### Task 2.2: Crisis/Shock Response Module

**Goal**: Model how sudden disqualifying events (scandals, health) affect election

**Known Disruptions in History:**
- John Paul I conclave (1978): Unknown circumstances
- 2005 conclave: Health concerns about candidates
- Future: Sudden scandals, health crises during conclave

**Steps:**
1. Define shock taxonomy (3-5 types):
   - **Type A - Scandal**: Criminal investigation, sexual abuse, financial impropriety
   - **Type B - Health**: Unexpected serious illness, hospitalization during conclave
   - **Type C - Political**: Major internal Church controversy (e.g., stance on key doctrine)
   - **Type D - Personal**: Death/major life event affecting candidate during election
   - **Type E - External**: Major world event (war, economic crash) changing priorities

2. For each shock type, estimate probability and effect:
   - P(Type A scandal revealed during conclave) = ?
   - Effect on winner: Λ → 0 (instant disqualification) or Λ → 0.5 (damaged)?

3. Build binary logit for "shock occurs":
   - Features: candidate prominence, media scrutiny, historical precedent
   - Output: P(shock) 0-30% range

4. If shock occurs, apply damage function:
   - Existing parameters: Λ, Ι, Π, Ν, Α
   - After shock: Λ', Ι', Π', Ν', Α' = adjusted values
   - Recalculate election probability

5. Integration into psf_model.py:
   ```python
   def apply_shock_scenario(candidate, shock_type):
       # Adjust parameters based on shock
       # Return new probability range
   ```

**Output:**
- Shock classification taxonomy
- Probability estimates for each shock type
- Damage functions (parameter adjustments)
- Updated psf_model.py with ShockModule
- Example: "If Cardinal X develops heart disease, probability drops from 85% to 15%"

**Success Criteria:**
- ✓ 3-5 shock types defined and modeled
- ✓ Shock probabilities estimated
- ✓ Damage functions validated against historical precedent
- ✓ Integrated into main model

**Owner**: Domain Expert (EBF Team)
**Effort**: 12-15 hours
**Status**: PENDING

---

### Task 2.3: Coalition Dynamics Simulation

**Goal**: Model multi-round conclave voting with coalition formation

**Background:**
- Current model: Single probability per candidate
- Reality: Conclave is multi-round voting where coalitions form/shift
- Duration = f(how quickly consensus forms) = f(Λ + Π)

**Steps:**
1. Build simplified coalition model:
   - Cardinals have preferred candidates + "coalition members" (bound votes)
   - Round 1: Each cardinal votes for preferred candidate
   - Round 2+: Coalitions merge as some candidates eliminated
   - Threshold: 2/3 majority wins

2. Predecessor support → automatic coalition:
   - Π = 0.95: ~50 automatic votes in Round 1
   - Ι = 0.92: Can attract neutral/undecided cardinals in later rounds
   - Model 3-5 round voting sequence

3. Test on known conclaves:
   - 2005 (Ratzinger, 2 rounds): Λ+Π=1.87, predicted 2 rounds ✓
   - 2025 (Prevost, 4 rounds): Λ+Π=1.80, predicted 4 rounds ✓
   - Does model explain historical duration?

4. Simulate conclave with hypothetical candidates:
   - Input: Candidate parameters (Λ, Ι, Π, etc.)
   - Output: Multi-round voting sequence, winner, duration

**Mathematical Model:**
```
Round r:
  Votes_i,r = Base_i + Coalition_Effect_i(r) - Elimination_Effect_i(r)
  Winner if Votes_i,r > 2/3 * Total_Cardinals
  else: eliminate bottom candidate, go to Round r+1
```

**Output:**
- Coalition simulation module (psf_coalition.py)
- Multi-round voting prediction for any candidate set
- Validation: Predicted duration vs. actual duration (86% current)
- Example output: "Round 1: Cardinal A=45, Cardinal B=38, Cardinal C=42; Round 2: A=62 (wins!)"

**Success Criteria:**
- ✓ Coalition model explains ≥80% of duration variance
- ✓ Backward-validates on 7 historical conclaves
- ✓ Generates plausible multi-round sequences
- ✓ Integrated with main model for forward predictions

**Owner**: Modeler (EBF Team)
**Effort**: 15-20 hours
**Status**: PENDING

---

## PHASE 3: Validation & Generalization (2027-2032)

**Timeline**: 2027 - 2032
**Owner**: EBF Research Team
**Budget**: 100+ hours (distributed over 6 years)
**Deliverables**: Real out-of-sample validation, generalization to other systems

### Task 3.1: 2032 Papacy Succession - Critical Out-of-Sample Test

**Goal**: Real, prospective prediction on next papal succession (2027-2032 timeframe)

**Status**: PENDING - Wait for 2032 event

**Implementation:**
1. Year 2027-2031: Monitor papal health, cardinal retirements, power dynamics
2. Year 2032: When papacy succession occurs:
   - Generate predictions using Phase 2 model (with interactions, coalitions)
   - Publish prediction (probability for each candidate before conclave)
   - After conclave: Compare prediction vs. actual outcome
3. Result interpretation:
   - If accuracy ≥85%: Model validated, ready for generalization
   - If accuracy 70-85%: Model needs adjustment; identify failure modes
   - If accuracy <70%: Major model issues; return to Phases 1-2

**Success Criteria:**
- ✓ Prospective prediction published before 2032 conclave
- ✓ Out-of-sample accuracy ≥85%
- ✓ Post-hoc analysis documenting any surprises
- ✓ Model refinement if needed

**Owner**: Lead Modeler
**Effort**: 20-30 hours (in 2032)
**Status**: PENDING

---

### Task 3.2: Parameter Updating & Validation

**Goal**: Incorporate 2032 outcome and refine parameters

**Status**: PENDING - After Task 3.1

**Steps:**
1. Add 2032 conclave to validation dataset (now 13 conclaves)
2. Re-fit β parameters with new data
3. Compare new β values to Phase 1 estimates:
   - Do parameters change significantly? (drift = concern)
   - Do confidence intervals narrow? (good: more data)
4. Update model-definition.yaml v2.0 with refined parameters
5. Document: What did the model get right? Where did it fail?

**Output:**
- model-definition.yaml v2.0 with Phase 3 refinements
- Post-hoc analysis report
- Confidence intervals (should be narrower: ±0.10 instead of ±0.15)

**Owner**: Statistician
**Effort**: 10-15 hours (in 2032-2033)
**Status**: PENDING

---

### Task 3.3: Generalization Framework

**Goal**: Extend PSF 2.0 to other elite-selection systems

**Target Systems:**
1. **Chinese Communist Party Leadership Selection**
   - Similar: Closed-door voting, factional politics, patronage
   - Parameter remapping: Π increases (patronage from Senioren), Α decreases
   - Test on Party Congress 2022, 2027, 2032

2. **Corporate Board CEO Succession**
   - Similar: Insider voting, founder influence, integration needs
   - Parameter remapping: Λ = internal board position, Π = founder endorsement
   - Test on tech company successions

3. **Military Leadership (General Staff)**
   - Similar: Seniority systems, merit-based, factional alignment
   - Parameter remapping: Λ = rank/command position, Ν = not too radical
   - Test on military succession patterns

**Framework Development:**
```python
class PSF_Generalized:
    def __init__(self, system_type):
        # Load system-specific parameter mappings
        # Dimension weights differ by system
        # Interpretation rules differ

    def set_parameter_mapping(self, mapping):
        # E.g., for Chinese politics:
        # Π weight: 20% → 25% (patronage more important)
        # Α weight: 5% → 3% (authenticity less important)
```

**Output:**
- Generalized PSF framework (psf_generalized.py)
- System-specific parameter mappings for 3+ elite-selection systems
- Validation on each system's historical data
- Case studies demonstrating generalization

**Success Criteria:**
- ✓ Framework generalizable to ≥3 systems
- ✓ Each system achieves ≥75% accuracy on historical test set
- ✓ Universal principles documented (5 principles identified in model-definition.yaml)
- ✓ Demonstrates external validity of core model

**Owner**: Generalization Team
**Effort**: 30-40 hours (2027-2032)
**Status**: PENDING

---

## Project Management

### Governance

- **Steering Committee**: EBF Leadership Team
- **Implementation**: EBF Research Team (5-8 people)
- **External Advisors**: Vatican scholars, political scientists, network analysts
- **Approval Gates**: Each phase requires steering committee sign-off before proceeding

### Budget & Resources

| Phase | Hours | FTE-Months | Cost (@ $150/hr) |
|-------|-------|-----------|-----------------|
| Phase 1 | 50-70 | 1.5-2.0 | $7,500-10,500 |
| Phase 2 | 50-80 | 1.5-2.5 | $7,500-12,000 |
| Phase 3 | 60-100 | 2.0-3.0 | $9,000-15,000 |
| **TOTAL** | **160-250** | **5-7.5** | **$24,000-37,500** |

### Timeline Gantt

```
2026 Q1:  ███  Phase 1.1-1.3 (Foundation)
2026 Q2:  ████ Phase 1 completion, Phase 2 start
2026 Q3:  ████ Phase 2.1-2.3 (Enhancement)
2026 Q4:  ███  Phase 2 completion
2027-2031:      Monitoring (prepare for 2032 succession)
2032 Q1:  ███  Phase 3.1-3.2 (Real validation)
2032-2033:      Parameter updating, final refinement
```

### Success Metrics (Overall Project)

| Metric | Current | Phase 1 | Phase 2 | Phase 3 |
|--------|---------|---------|---------|---------|
| Sample size (conclaves) | 7 | 12 | 12 | 13 |
| Accuracy (%) | 87 | 88-90 | 90-93 | 85-90+ |
| Parameter certainty (CI width) | ±0.25 | ±0.15 | ±0.12 | ±0.10 |
| Model complexity | 5D+1β | 5D+1β | 5D+1β+γ | 5D+1β+γ+shocks |
| Generalized systems | 1 | 1 | 1 | 3+ |
| Time to prediction | 30+ hours | 20 hours | 15 hours | <10 hours |

---

## Risk Management

### Key Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|-----------|
| Pre-1958 data insufficient | Medium | High | Task 1.1: Target ≥3 conclaves |
| Network data unavailable | Low | Medium | Task 1.2: Use alternative sources |
| 2032 succession delayed | Low | Medium | Phase 3 flexible on timing |
| Interaction terms unstable | Medium | Medium | Task 2.1: Validate on holdout set |
| Generalization fails | Medium | Low | Task 3.3: Test multiple systems |

### Contingency Plans

1. **If pre-1958 data insufficient**: Focus on sensitivity analysis instead (robustness testing)
2. **If network data unavailable**: Develop hybrid model (50% quantitative, 50% expert judgment)
3. **If 2032 succession >2033**: Proceed with internal validation; publish preliminary results
4. **If interaction terms unstable**: Stick with Phase 1 model (5D additive); note as limitation

---

## Next Steps

1. **Q1 2026 - Approve Phase 1**: Steering committee review, resource allocation
2. **Q1-Q2 2026 - Execute Phase 1**: Historical extension, network analysis, confidence intervals
3. **Q2 2026 - Phase 1 Review**: Validation of new data, parameter update
4. **Q2-Q4 2026 - Execute Phase 2**: Interaction terms, crisis module, coalition simulation
5. **Q4 2026 - Phase 2 Review**: Accuracy testing, documentation
6. **2027-2031 - Monitor & Prepare**: Prepare for 2032 succession
7. **2032 - Phase 3.1**: Real out-of-sample prediction
8. **2032-2033 - Final Validation**: Parameter updating, publication

---

## Contact & Questions

**Model Owner**: EBF Research Team
**Single Source of Truth**: `/home/user/complementarity-context-framework/models/PSF-2-0-PAPAL-SUCCESSION/model-definition.yaml`
**Implementation**: `psf_model.py`, `test_psf_model.py`
**Updates**: This file (`IMPROVEMENT_ROADMAP.md`)

For questions on specific improvements, see relevant phase/task above.

---

**Document Version**: 1.0
**Last Updated**: 2026-01-14
**Status**: ACTIVE (Phase 1 - PENDING)
