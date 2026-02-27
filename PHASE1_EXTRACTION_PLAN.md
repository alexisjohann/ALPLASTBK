# Phase 1: EXTRACTION PLAN für Option B Refactoring
## Ch20 → Ch20 (static) + Ch21 (dynamic) + KKK (formal)

**Status:** Planning Complete | Date: 2026-01-21
**Total Ch20 Current:** 4,577 lines
**Target Distribution:** Ch20 (3,200) + Ch21 (2,000) + KKK (900)

---

## PART A: WHAT STAYS IN CH20 (STATISCH - 3,200 lines)

### Section 1: Meta-Framework: From Mathematics to Heuristics
**Lines:** 170-362
**Size:** 192 lines
**Keep:** ✅ ENTIRE
**Reason:** Foundation for A1-A8 heuristics (statisch, nicht dynamisch)
**Content:**
- Why heuristics?
- Five levels of abstraction
- Error taxonomy (E1-E6)

---

### Section 2: Portfolio of Heuristic Frameworks: Six Equally Valid Derivations
**Lines:** 361-872
**Size:** 511 lines
**Keep:** ✅ ENTIRE
**Reason:** The six frameworks (Component, Behavioral, Temporal, Segment, Outcome, Context) are STATIC design tools
**Content:**
- Framework 1: Component-Based Clustering (A1-A8)
- Framework 2: Behavioral Architecture
- Framework 3: Temporal Staging
- Framework 4: Segment-First Design
- Framework 5: Outcome-First Design
- Framework 6: Context-Adaptive Meta
- Framework Comparison Table

---

### Section 3: Theoretische Grundlagen: Warum Portfolios?
**Lines:** 872-952
**Size:** 80 lines
**Keep:** ✅ ENTIRE
**Reason:** Single Intervention Ceiling Theorem + Superadditivity Principle = static analysis
**Content:**
- Limitations of Single Interventions Theorem (line 923-931)
- Superadditivity Principle (line 940-950)

---

### Section 4: Die Complementarity Matrix γ_ij
**Lines:** 973-1102
**Size:** 129 lines
**Keep:** ✅ ENTIRE
**Reason:** Definition of γ values (STATIC, not dynamic update mechanism)
**Content:**
- Definition und Interpretation
- The Matrix with empirical estimates
- Known Crowding-Out effects

---

### Section 5: Portfolio Coherence Criteria
**Lines:** 1103-1177
**Size:** 74 lines
**Keep:** ✅ ENTIRE
**Reason:** C1-C4 Coherence Criteria are static validation rules
**Content:**
- Four Coherence Criteria
- Coherence Score
- Coherence Diagnosis Matrix

---

### Section 6: Error Detection and Validation: Six Sanity Checks
**Lines:** 1178-1452
**Size:** 274 lines
**Keep:** ✅ ENTIRE
**Reason:** All 6 checks (Aggregation Reversibility, Segment Representativeness, Context Sensitivity, Complementarity Audit, Phase Coverage, Emergence-Mode Alignment) are STATIC validation tools
**Content:**
- Check 1-6 detailed
- Sanity Check Summary
- Decision Tree: Which Abstraction Level
- Consistency Audit Ch17-20 Integration

---

### Section 7: Portfolio Optimization Through Heuristic Lenses
**Lines:** 1514-1731
**Size:** 217 lines
**Keep:** ✅ ENTIRE
**Reason:** Static optimization algorithms given S_0
**Content:**
- Optimization Spaces
- Framework-Specific Constraints
- Three-Dimensional Optimization (I × Phase × Segment)
- Practical Algorithms
- Trade-Offs
- Decision Rule

---

### Section 8: Formal Portfolio Optimization: Mathematical Foundations
**Lines:** 1732-2038
**Size:** 306 lines
**Keep:** ✅ ENTIRE
**Reason:** Static optimization theory
**Content:**
- The optimization problem (Eq. at line 1738)
- Solution algorithms (line 1750-1776)
- Portfolio Archetypes: Seven Predefined Optimization Goals (line 1777-2038)
  - Quick Wins
  - Optimal
  - Eco
  - Safe
  - Deep
  - Blended
  - Adaptive

---

### Section 9: FEPSDE-KPI-Framework: Messung über alle Utility-Dimensionen
**Lines:** 2039-2197
**Size:** 158 lines
**Keep:** ✅ ENTIRE
**Reason:** Static KPI measurement framework
**Content:**
- F (Financial), E (Emotional), P (Physical), S (Social), D (Decision), X (eXecutive)
- KPI-Zuordnung nach Interventionstyp
- KPI-Messprotokoll

---

### Section 10: Operational Deployment: From Theory to Practice
**Lines:** 2198-2427
**Size:** 229 lines
**Keep:** ✅ ENTIRE
**Reason:** Static deployment procedures (Pre-Deployment Checklist, Rollout Strategy, Monitoring Dashboard)
**Content:**
- Pre-Deployment Checklist
- Deployment Phases
- Real-Time Monitoring Dashboard
- Adaptive Adjustment Rules (NOTE: This is ADAPTIVE during single deployment, not learning loop)
- End-of-Deployment Report
- Success Criteria

---

### Section 11: Multi-Level Implementation
**Lines:** 2428-2479
**Size:** 51 lines
**Keep:** ✅ ENTIRE
**Reason:** Static level analysis (Individual → Household → Org → Region → Nation → Global)
**Content:**
- The Six Implementation Levels
- Level-specific Portfolio Principles
- Cross-Level Coherence

---

### Section 12: Der Vollständige Interventions-Design-Workflow
**Lines:** 3065-3754
**Size:** 689 lines
**Keep:** ✅ ENTIRE
**Reason:** Complete STATIC design workflow from scratch to portfolio
**Content:**
- Drei Emergenz-Modi (E-Full, E-Partial, E-None)
- Phase 0: Status-Quo Diagnose
- Phase 1-7: Design Workflow
- Worked Example Pfad A & B

---

### Section 13: Error Analysis: Four Core Examples (STATIC ANALYSIS ONLY)
**Lines:** 3754-4160
**Size:** 406 lines
**Keep:** ✅ PARTLY - Only the worked examples for SINGLE TIME-POINT analysis

**Subsection 13a: Example 1: Diabetes** (Lines 3781-3895)
**Keep:** ✅ YES
**Reason:** Single time-point portfolio design (t=0)
**Content:** Diabetes portfolio at t=0 (PreAware phase)

**Subsection 13b: Example 2: Rente** (Lines 3896-4002)
**Keep:** ✅ YES
**Reason:** Single time-point phase-specific analysis
**Content:** Rente portfolio analysis across phases (but still static at each φ)

**Subsection 13c: Example 3: Energie** (Lines 4003-4116)
**Keep:** ✅ YES
**Reason:** Single time-point segment analysis
**Content:** Energie portfolio for three segments (PS, SO, AS)

**Subsection 13d: Example 4: Engagement** (Lines 4117-4196)
**Keep:** ✅ YES
**Reason:** Single time-point multi-segment design
**Content:** Engagement portfolio across segments

**Subsection 13e: Framework Selection Summary** (Lines 4197-4236)
**Keep:** ✅ YES
**Reason:** Static framework comparison

---

### Section 14: Summary
**Lines:** 4237-4498
**Size:** 261 lines
**Keep:** ✅ ENTIRE (but update for new Ch21 reference)
**Reason:** Synthesis of static design principles
**Content:**
- Phase 7: Comprehensive Synthesis
- Final Consistency Audit
- Meta-Decision Tree
- Integration Loop Ch17-20
- When to Re-Evaluate
- Summary of Summary

---

## TOTAL STAYING IN CH20: ~3,600 lines
**ACTION:** Need to TRIM ~400 lines from Summary/Workflow to reach target 3,200

---

## PART B: WHAT MOVES TO CH21 (DYNAMISCH - 1,000+ lines)

### Section 1: Simulation und Prediction → PARTIALLY MOVE
**Lines:** 2480-2651
**Size:** 171 lines
**Decision:** EXTRACT ONLY the DYNAMIC parts
**What moves (lines ~2480-2644):**
- 10C-basierte Vorhersage der Verhaltensänderung (2486-2610) → This is FORWARD-LOOKING, belongs in Ch21
- Der Simulations-Workflow (2610-2642) → This describes MULTI-PERIOD simulation, belongs in Ch21

**What stays in Ch20 (lines ~2645-2651):**
- Risiko-Metriken (2652) → Could be static metric, but marginal

**Action:** MOVE lines 2486-2642 to Ch21 Section 1: "Prediction & Simulation: Why Status Quo Changes"

---

### Section 2: Evaluation und Organizational Learning → MOVE ENTIRE
**Lines:** 2652-2827
**Size:** 175 lines
**MOVE:** ✅ ENTIRE to Ch21
**Reason:** The Learning Loop (Design → Implement → Evaluate → Update → Redesign) is INHERENTLY DYNAMIC
**Content:**
- Der Drei-Schritt Evaluations-Prozess (2658-2681)
  - Measurement
  - Attribution
  - Repository-Update (Bayesian: line 2677)
- Der Learning Loop (2683-2699) [THE DIAGRAM]
- Organizational Learning Metriken (2701-2708)
- 10C Delta Measurement: Der vollständige Learning Loop (2709-2810)
  - Der 10C Delta Vektor
  - Dimensions-spezifische Messung
  - Quantifizierung des Δ-Vektors
  - Erfolgs-Kriterien

**Action:** MOVE lines 2652-2827 entirely to Ch21 Section 2-3: "Learning Loop & Parameter Updates"

---

## PART C: WHAT MOVES TO KKK (FORMAL-DYNAMIC - 900 lines)

### These are FORMAL MATHEMATICAL MODELS needed to understand Ch21

**New Appendix KKK: METHOD-DYNAMIC**
**Category:** METHOD-DYNAMIC (new subcategory under METHOD)
**Code:** KKK (next available code in K-series)

### Content Structure (to be created from scratch):

#### Section 1: Formal Setup (~100 lines)
- Time-indexed state vector: S_t = (L, d, γ_current, Ψ_t, Θ_t, A_t, W_t, φ_t, Scope)
- Portfolio trajectory: P_t = {I_1^t, ..., I_n^t}
- Effectiveness trajectory: E_t = E(P_t | S_t)
- Behavior change trajectory: BC_t = BC(P_t | S_t)

#### Section 2: Phase-Progression Dynamics (~150 lines)
- Continuous model: dφ/dt = v(A_t, W_t, α_t,φ) [ODE]
- Discrete model: φ_{t+1} = φ_t + Δφ_t [Markov]
- Boundary conditions and saturation
- Examples: Diabetes, Rente phase velocities

#### Section 3: Context-Evolution Dynamics (~100 lines)
- Linear approximation: Ψ_{t+1} = Ψ_t + η(I_t, shocks_t)
- Nonlinear S-curves and thresholds
- External shock modeling (policy changes, crises)
- Reversibility vs irreversibility

#### Section 4: Bayesian Parameter Learning (~150 lines)
- Prior: Θ_0 from literature (Appendix BBB)
- Likelihood: P(observed_BC_t | Θ)
- Posterior update: Θ_t = Θ_{t-1} + Δ Θ_t
- Convergence criteria: ||Θ_t - Θ_{t-1}|| < ε
- Relation to γ-update equation (line 2677)

#### Section 5: Portfolio Redesign Rules (~150 lines)
- Decision tree: WHEN to redesign?
  - Trigger: Δφ > threshold?
  - Trigger: E_t declining?
  - Trigger: ΔΨ shock?
- Optimization: max E_t(P_t) subject to switching costs
- Cost function: C_redesign(P_{t-1} → P_t)

#### Section 6: Convergence Analysis (~150 lines)
- Fixed point analysis: S_∞ = limit(S_t) as t→∞
- Sufficient conditions for convergence
- Rate of convergence (exponential, polynomial, etc.)
- Cases of divergence or cycling

#### Section 7: Worked Examples (Formal Derivations) (~100 lines)
- Diabetes: Full φ(t) evolution with numerical values
- Rente: Phase-specific parameter updates
- Energie: Context shock response dynamics

---

## PART D: INDEX UPDATES REQUIRED

### appendices/00_appendix_index.tex

1. **Add KKK to METHOD Table** (around line ~430)
   ```
   KKK & METHOD-DYNAMIC & Portfolio Evolution Dynamics & ... \\
   ```

2. **Update METHOD Count** (around line ~68)
   ```
   METHOD- & ... & 15 → 16 (now includes KKK)
   ```

3. **Update Total Appendix Count** (around line ~68)
   ```
   Total & ... & 129 → 130
   ```

4. **Add KKK to Status Table** (around line ~612)
   ```
   KKK & METHOD-DYNAMIC: Portfolio Evolution & Method & NEW \\
   ```

5. **Add KKK to Reading Path** (around line ~898)
   ```
   KKK & METHOD-DYNAMIC & HHH, KKK & Ch. 21 \\
   ```

### chapters/20_intervention_portfolios.tex Header

**Update metadata (lines 1-21):**
```
Old: Leads to: Chapter 21 (Limitations)
New: Leads to: Chapter 21 (Dynamic Portfolio Evolution)
```

**Update appendix references (line 15-16):**
```
Old: Primary Appendix: HHH - METHOD-TOOLKIT
New: Primary Appendix: HHH - METHOD-TOOLKIT; KKK - METHOD-DYNAMIC (for Ch21 reference)
```

---

## PART E: DECISIONS STILL NEEDED (before Phase 2)

### Decision 1: What EXACT lines to trim from Ch20?
**Current:** 3,600 estimated
**Target:** 3,200
**Gap:** ~400 lines to cut

**Options:**
- A) Cut from Summary/Workflow (less critical)
- B) Consolidate some framework sections (reduce redundancy)
- C) Move some worked examples to appendix (keep only 1-2 worked examples in Ch20)

**Recommendation:** Option C - keep only Diabetes + Rente in Ch20 as "quick portfolio design examples", move Energie + Engagement to Ch21 as "multi-period portfolio redesign examples"

**If we do this:**
- Remove Example 3 (Energie, ~114 lines)
- Remove Example 4 (Engagement, ~80 lines)
- Total cut: 194 lines
- New Ch20 size: 3,406 lines
- Need additional ~206 lines to trim

### Decision 2: Structure of Ch21 sections?
**Option A:**
- Ch21 Sec 1: Prediction & Simulation basics
- Ch21 Sec 2: Learning Loop & Bayesian Updates
- Ch21 Sec 3: Multi-period Worked Examples (Diabetes, Rente with redesigns)
- Ch21 Sec 4: Context Shocks & Convergence Criteria

**Option B:**
- Ch21 Sec 1: Why Status Quo Changes (motivation)
- Ch21 Sec 2: Phase-Progression Dynamics (with Diabetes example)
- Ch21 Sec 3: Context-Evolution & Learning Loop (with Rente + Energie examples)
- Ch21 Sec 4: Convergence & When to Stop (with Engagement example)
- Ch21 Sec 5: Synthesis: Linking to KKK formal models

**Recommendation:** Option B (more pedagogical structure)

### Decision 3: KKK formality level?
**Option A:** Highly formal (proofs, full equations)
- Target audience: PhD students, researchers
- Time to write: 4-5 hours

**Option B:** Medium formal (key equations, intuitions)
- Target audience: practitioners wanting deeper understanding
- Time to write: 2-3 hours

**Recommendation:** Option B (makes KKK accessible, not intimidating)

---

## PART F: CHECKLIST FOR PHASE 1 COMPLETION

```
☐ Extraction plan documented (THIS FILE) ✓
☐ All line numbers verified in actual file
☐ Section assignments clear (Ch20 stay / Ch21 move / KKK new)
☐ Index updates identified
☐ Trim target decisions made (which 400 lines to cut?)
☐ Ch21 section structure chosen
☐ KKK formality level decided
☐ Ready for Phase 2 (Clean Ch20)
```

---

## NEXT STEPS

**Phase 1 ✓ DONE:** Extraction plan complete
**Phase 2 (2h):** Clean Ch20
- Delete identified lines
- Trim 400 lines
- Update metadata
- Rename chapter

**Phase 3 (3h):** Create Appendix KKK
- 900 lines new content
- Sections 1-7 as outlined
- Cross-references to Ch20 & Ch21

**Phase 4 (4h):** Rewrite Ch21
- 2,000 lines new content
- Sections as per Decision 2 (Option B)
- Multi-period examples
- Convergence criteria

**Phase 5 (1.5h):** Integration testing
- All cross-references valid
- Index counts correct
- LaTeX compiles

**Phase 6 (1h):** Commit & push

---

**Estimated Total Time:** 11-12 hours
**Start Date:** Ready when you say GO
