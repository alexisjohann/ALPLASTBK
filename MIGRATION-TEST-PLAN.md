# Migration Test Plan - Subset Approach

**Date:** 2026-01-15
**Purpose:** Test migration on small subset before full rollout

---

## Test Subset: 10 Appendices (kein Duplikate)

Wir testen mit 10 Dateien die **KEINE Duplikate haben** und **KEINE References von anderen Appendices** erhalten.

### Test-Dateien (Saubere Auswahl ohne Duplikate):

1. **A_formal_derivations.tex** → DER (FORMAL-DERIVE)
   - Status: Single file, unique mapping
   - Risk: Low

2. **D_proofs.tex** → PRF (FORMAL-PROOF)
   - Status: Single file, unique mapping
   - Risk: Low

3. **E_operationalization.tex** → OPS (METHOD-OPS)
   - Status: Single file, unique mapping
   - Risk: Low

4. **F_worked_examples.tex** → EXM (REF-EXAMPLES)
   - Status: Single file, unique mapping
   - Risk: Low

5. **H_computational_history.tex** → HRC (REF-HISTORY)
   - Status: Single file, unique mapping
   - Risk: Low

6. **I_nobel_contributions.tex** → NOB (LIT-NOBEL)
   - Status: Single file, unique mapping
   - Risk: Low

7. **L_acemoglu_papers.tex** → ACE (LIT-ACEMOGLU)
   - Status: Single file, unique mapping
   - Risk: Low

8. **M_shleifer_papers.tex** → SHL (LIT-SHLEIFER)
   - Status: Single file, unique mapping
   - Risk: Low

9. **N_heckman_papers.tex** → HEC (LIT-HECKMAN)
   - Status: Single file, unique mapping
   - Risk: Low

10. **O_autor_papers.tex** → AUT (LIT-AUTOR)
    - Status: Single file, unique mapping
    - Risk: Low

---

## Test-Schritte

### Step 1: Prepare Test Environment
```bash
# Create test backup directory
mkdir -p migration-test/backups
cp migration-test/backups/appendices/*.tex migration-test/backups/

# Create list of test files
cat > migration-test/test-files.txt <<EOF
A_formal_derivations.tex → DER_formal_derivations.tex
D_proofs.tex → PRF_proofs.tex
E_operationalization.tex → OPS_operationalization.tex
F_worked_examples.tex → EXM_worked_examples.tex
H_computational_history.tex → HRC_computational_history.tex
I_nobel_contributions.tex → NOB_nobel_contributions.tex
L_acemoglu_papers.tex → ACE_acemoglu_papers.tex
M_shleifer_papers.tex → SHL_shleifer_papers.tex
N_heckman_papers.tex → HEC_heckman_papers.tex
O_autor_papers.tex → AUT_autor_papers.tex
EOF
```

### Step 2: Test File Renaming
```python
# For each test file:
# 1. Rename: A_*.tex → DER_*.tex
# 2. Verify file exists
# 3. Check checksum matches backup
```

**Expected Results:**
- ✅ All 10 files renamed successfully
- ✅ All checksums match
- ✅ No file corruption

### Step 3: Test Reference Updates in Chapters

```bash
# Search for references to test appendices in chapters/
grep -r "Appendix A\b" chapters/*.tex
grep -r "Appendix D\b" chapters/*.tex
grep -r "Appendix E\b" chapters/*.tex
# ... etc
```

**Expected Results:**
- ✅ Find exact references
- ✅ Update with correct new codes
- ✅ Verify references resolve

### Step 4: Test Reference Updates in Other Appendices

```bash
# Search for references within appendices to test files
grep -r "Appendix A\b" appendices/*.tex
grep -r "\\\\ref{app:A}" appendices/*.tex
```

**Expected Results:**
- ✅ Update all text references
- ✅ Update all LaTeX references
- ✅ Verify no "Appendix A" remains (unless in other context)

### Step 5: LaTeX Compilation Test

```bash
# Try to compile a chapter that references test appendices
latexmk -pdf outputs/chapter-with-test-refs.tex
```

**Expected Results:**
- ✅ PDF compiles without errors
- ✅ Cross-references resolve (no "???" in PDF)
- ✅ Appendix references link correctly

### Step 6: Validation

```bash
# Check that old codes are gone
ls appendices/A_* 2>&1 | grep "No such file"  # Should fail
ls appendices/D_* 2>&1 | grep "No such file"  # Should fail

# Check that new codes exist
ls appendices/DER_* | wc -l  # Should be 1
ls appendices/PRF_* | wc -l  # Should be 1
```

---

## If Test Passes ✅

1. Delete test files (restore from backup)
2. Create migration script for **duplicate codes** separately
3. Run full 120-file migration

## If Test Fails ❌

1. Restore from backup
2. Debug and fix issue
3. Create workaround or manual procedure
4. Re-test subset

---

## Duplicate Codes Resolution Strategy

After successful subset test, address the 7 remaining conflicts:

```
BHC   (2 files): AH_temporal + DOMAIN-CONSULTING
  → Keep BHC for DOMAIN-CONSULTING
  → Use BHC2 or CTM for temporal context

EQU   (2 files): BB_DOMAIN-PAPAL-APPOINTMENTS + BB_FORMAL-INTERVENTION
  → EQU for FORMAL (core math)
  → PAP for DOMAIN (papal)

FND   (3 files): X_FORMAL-FOUND + X_LIT-LOEWENSTEIN + X_milgrom
  → FND for FORMAL-FOUND
  → LOE for LIT-LOEWENSTEIN
  → MIL for DOMAIN-MILGROM-ROBERTS

MCD   (2 files): AZ_PAPAL + AZ_method_construct
  → MCD for METHOD-CONSTRUCT
  → CON for PAPAL (old code)

PAR   (2 files): AY_PAPAL + AY_paradigms
  → PAR for LIT-PARADIGMS
  → PAP for DOMAIN-PAPAL

TKT   (2 files): HHH_METHOD-TOOLKIT + HHH_REF-SEGMENTATION
  → TKT for METHOD-TOOLKIT
  → SEG for REF-SEGMENTATION-HEURISTICS

WHERE (2 files): BBB_estimation + BBB_parameter
  → WHERE for CORE-WHERE
  → EST for METHOD-ESTIMATION-METHODOLOGY
```

---

## Timeline

1. **Today:** Test subset (1-2 hours)
2. **Tomorrow:** Resolve duplicates + full migration (3-4 hours)
3. **Within 2 days:** Validation + verification

---

## Critical Success Factors

✅ No data loss (backups available)
✅ All references updateable (registry complete)
✅ No circular dependencies (pre-checked)
✅ All new codes unique (after duplicate resolution)
✅ LaTeX compiles (final validation)

---

**Status:** Ready to test with subset

