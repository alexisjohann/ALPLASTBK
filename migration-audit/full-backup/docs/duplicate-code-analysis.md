# Duplicate Appendix Code Analysis

**Date:** 2026-01-15
**Severity:** CRITICAL - 24 codes have 50+ files with duplicates
**Status:** Documented & requires cleanup

---

## 1. Duplicate Code Inventory

### Critical Duplicates (Same Code, Different Categories)

#### **AA Code** (2 files)
- `AA_labor_economics.tex` (DOMAIN-LABOR)
- `AA_LIT-AA_mullainathan_research.tex` (LIT-MULLAINATHAN)

#### **AB Code** (2 files)
- `AB_matching_repugnant.tex` (DOMAIN-MATCH)
- `AB_LIT-AB_list_research.tex` (LIT-LIST)

#### **AC Code** (2 files)
- `AC_industrial_organization.tex` (DOMAIN-IO)
- `AC_LIT-AC_dolan_research.tex` (LIT-DOLAN)

#### **AD Code** (2 files)
- `AD_evolutionary_behavioral_gt.tex` (DOMAIN-EVO)
- `AD_LIT-AD_specialists_research.tex` (LIT-SPECIALISTS)

#### **AE Code** (2 files)
- `AE_mechanism_design.tex` (DOMAIN-MECH)
- `AE_LIT-AE_falk_research.tex` (LIT-FALK)

#### **AF Code** (2 files)
- `AF_social_choice.tex` (DOMAIN-CHOICE)
- `AF_LIT-AF_malmendier_research.tex` (LIT-MALMENDIER)

#### **AG Code** (2 files)
- `AG_complexity_economics.tex` (DOMAIN-COMPLEX)
- `AG_LIT-AG_shafir_research.tex` (LIT-SHAFIR)

#### **AN Code** (2 files)
- `AN_llm_monte_carlo.tex` (METHOD-LLMMC)
- `AN_llm_monte_carlo_final.tex` (METHOD-LLMMC - duplicate/updated)

#### **AY Code** (2 files)
- `AY_paradigms.tex` (LIT-PARADIGMS)
- `AY_PAPAL-SUCCESSION-FRAMEWORK.tex` (DOMAIN-PAPAL)

#### **AZ Code** (2 files)
- `AZ_method_construct.tex` (METHOD-CONSTRUCT)
- `AZ_PAPAL-HISTORICAL-ANALYSIS.tex` (DOMAIN-PAPAL)

#### **BA Code** (2 files)
- `BA_FORMAL-SEGMENTATION_genesis.tex` (FORMAL-SEGMENT)
- `BA_DOMAIN-PAPAL-EXTENDED-1878-1939.tex` (DOMAIN-PAPAL)

#### **BB Code** (2 files)
- `BB_FORMAL-INTERVENTION-EQUILIBRIA.tex` (FORMAL-EQUILIBRIA)
- `BB_DOMAIN-PAPAL-APPOINTMENTS.tex` (DOMAIN-PAPAL)

#### **BBB Code** (2 files)
- `BBB_estimation_methodology.tex` (CORE-WHERE or METHOD variant)
- `BBB_parameter_estimation.tex` (duplicate/updated)

#### **HHH Code** (2 files)
- `HHH_METHOD-TOOLKIT.tex` (METHOD-TOOLKIT)
- `HHH_REF-SEGMENTATION-HEURISTICS.tex` (REF variant)

#### **III Code** (2 files)
- `III_METHOD-LLMMC_calibration_pipeline.tex` (METHOD-LLMMC-CAL)
- `III_THEORY-EIH_efficient_intervention_hypothesis.tex` (FORMAL-EIH)

#### **R Code** (2 files)
- `R_evaluation_protocol.tex` (METHOD-EVAL)
- `R_LIT-THALER_thaler_research.tex` (LIT-THALER)

#### **S Code** (2 files)
- `S_falsifiable_predictions.tex` (PREDICT-MASTER)
- `S_LIT-SUNSTEIN_sunstein_research.tex` (LIT-SUNSTEIN)

#### **T Code** (2 files)
- `T_metatheory.tex` (REF-META)
- `T_LIT-CAMERER_camerer_research.tex` (LIT-CAMERER)

#### **V Code** (2 files)
- `V_psi_dimensions.tex` (CORE-WHEN)
- `V_THEORY-MEP_minimum_effective_portfolio.tex` (FORMAL-MEP)

#### **VVV Code** (7 files) ⚠️ MOST DUPLICATED
- `VVV_0_technology_landscape.tex`
- `VVV_1_technological_roadmap.tex`
- `VVV_2_strategic_positioning.tex`
- `VVV_3_product_options.tex`
- `VVV_4_productizing_journey.tex`
- `VVV_business_model.tex`
- `VVV_README.md`

#### **W Code** (2 files)
- `W_information_economics.tex` (DOMAIN-INFO)
- `W_LIT-ARIELY_ariely_research.tex` (LIT-ARIELY)

#### **X Code** (3 files)
- `X_milgrom_roberts.tex` (DOMAIN-COMPLEMENT)
- `X_FORMAL-FOUND_mathematical_foundations_complementarity.tex` (FORMAL-FOUND)
- `X_LIT-LOEWENSTEIN_loewenstein_research.tex` (LIT-LOEWENSTEIN)

#### **Y Code** (2 files)
- `Y_capital_markets.tex` (DOMAIN-CAPITAL)
- `Y_LIT-Y_cialdini_research.tex` (LIT-CIALDINI)

#### **Z Code** (2 files)
- `Z_growth_theory.tex` (DOMAIN-GROWTH)
- `Z_LIT-Z_haidt_research.tex` (LIT-HAIDT)

---

## 2. Root Cause

The appendix naming system has a **fundamental conflict:**

### Problem
- **DOMAIN codes** (AA–AG, W, X, Y, Z) are assigned in index section 451–484
- **LIT codes** (AA, AB, AC, AD, AE, AF, AG, R, S, T, W, X, Y, Z) are assigned in index section 572–619
- **Same codes used for different categories** = files can't coexist in one directory

### Why This Happened
The system evolved with:
1. DOMAIN appendices created first (AA = labor, AB = matching, etc.)
2. LIT appendices added later using the SAME codes (AA = Mullainathan, AB = List, etc.)
3. Both were indexed separately but with file naming conflicts
4. Directory structure is `appendices/` (flat, not categorized)

---

## 3. Resolution Options

### Option A: Rename All LIT Codes (Recommended)
**Action:** Use different code range for LIT appendices
- Current: LIT uses AA, AB, AC, AD, AE, AF, AG, R, S, T, W, X, Y, Z
- New: LIT uses BK, BL, BM, BN, BO, BP, BQ, BR, BS, BT, BU, BV, BW, BX

**Advantages:**
- No conflicts with DOMAIN codes
- Preserves existing DOMAIN files
- Clean, systematic

**Disadvantages:**
- Requires updating 30 LIT appendix files
- Requires updating index (2 locations)
- Many cross-references to update

### Option B: Rename All DOMAIN Codes (Complex)
**Action:** Use different code range for DOMAIN appendices
- Current: DOMAIN uses AA–AG, W, X, Y, Z
- New: DOMAIN uses CK, CL, CM, CN, CO, CP, CQ, CR, CS, CT, CU, CV, CW, CX

**Disadvantages:**
- Updates 17 DOMAIN files
- Breaks many existing references
- Less intuitive (AA usually means "first alphabetical")

### Option C: Rename Some Categories (Surgical)
**Action:** Consolidate duplicates by function
- Keep either LIT or DOMAIN version
- Rename the other

**Example:** Keep DOMAIN-AA (labor), rename LIT-AA → LIT-MULLAINATHAN-1

**Disadvantages:**
- Creates inconsistent naming scheme
- Requires decisions on which version to keep

---

## 4. Recommended Action Plan

### Step 1: Decide Policy
Choose one option above. **Recommendation: Option A** (rename LIT codes to BK–BX range)

### Step 2: Create Migration Mapping
| Old Code | New Code | Category | Name |
|----------|----------|----------|------|
| AA (LIT) | BK | LIT-MULLAINATHAN | Sendhil Mullainathan Research |
| AB (LIT) | BL | LIT-LIST | John List Research |
| ... | ... | ... | ... |

### Step 3: Execute Renames
- Rename all LIT appendix files
- Update appendix index (2 locations)
- Update cross-references in other appendices

### Step 4: Verify
- Check no duplicate codes remain
- Verify LaTeX compilation
- Test cross-references

---

## 5. Impact on Current Work (Cardinal Appointments)

**Good news:** The current recommendation **BF** and **BG** codes are **still available** and **don't conflict** with any existing duplicates.

**Current status:**
- BF = AVAILABLE (recommended for DOMAIN-GENERALIZATION)
- BG = AVAILABLE (recommended for FORMAL-LEARNING)

**However:** Before creating major new appendices, the duplicate issue should be resolved to avoid future naming conflicts.

---

## 6. Files Affected by Duplicates

**Summary:**
- **24 codes with duplicates**
- **Total files with duplicated codes: ~50+**
- **VVV is most problematic** (7 files, unclear hierarchy)
- **Appendix index has 3 places** listing conflicting assignments

---

## Recommendation

**Immediate action:** Don't create new appendices until duplicate codes are resolved.

**Timeline:**
1. Choose Option A/B/C (Decision needed from project lead)
2. If Option A: Allocate BK–BX (14 free codes) for renamed LIT appendices
3. Execute renames systematically
4. Then proceed with BF/BG creation for cardinal appointments work

**Alternative:** Create BF and BG now (they don't conflict), but note that full index cleanup will be needed before major expansion.

---

**Document Version:** 1.0
**Status:** Analysis Complete, Action Pending
