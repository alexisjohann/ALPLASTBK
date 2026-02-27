# Appendix Code Migration: Quick Reference

**Status:** ✅ Dry-run validated and successful
**Ready to execute:** Yes
**Risk level:** Minimal (full backups available)

---

## What Will Change

### 1. Appendix Filenames (122 files)

**Old naming:** Single/double letter prefixes
```
A_formal_derivations.tex
AA_labor_economics.tex
AAA_aggregation_levels.tex
AU_bcm_axiom_formalization.tex
G_glossary.tex
BBB_parameter_estimation.tex
```

**New naming:** Unique 3-letter semantic codes
```
DER_formal_derivations.tex
MUL_labor_economics.tex
WHO_aggregation_levels.tex
AWA_bcm_axiom_formalization.tex
GLS_glossary.tex
WHERE_parameter_estimation.tex
```

### 2. References in All Files (1,573 updates)

**Text references:**
```latex
% BEFORE
See Appendix AU for formalization
See Appendix G for definitions

% AFTER
See Appendix AWA for formalization
See Appendix GLS for definitions
```

**LaTeX citations:**
```latex
% BEFORE
\ref{app:AU}
\label{app:G}

% AFTER
\ref{app:AWA}
\label{app:GLS}
```

**Axiom/Theorem references:**
```latex
% BEFORE
AU-1 (Awareness Axiom 1)
HHH-T5 (Toolkit Theorem 5)

% AFTER
AWA-1 (Awareness Axiom 1)
TKT-T5 (Toolkit Theorem 5)
```

---

## Core Code Mappings

### CORE Framework (9 codes)
| Old | New | Meaning | Appendix |
|-----|-----|---------|----------|
| AAA | WHO | Welfare Hierarchy | `WHO_aggregation_levels.tex` |
| C | WAT | Welfare Dimensions | `WAT_fepsde_matrix.tex` |
| B | HOW | Interaction Structure | `HOW_complementarity_levels.tex` |
| V | WEN | Context Framework | `WEN_psi_dimensions.tex` |
| BBB | WHERE | Parameter Estimation | `WHERE_parameter_estimation.tex` |
| AU | AWA | Awareness Function | `AWA_bcm_axiom_formalization.tex` |
| AV | REA | Willingness Function | `REA_willingness_formalization.tex` |
| AW | STA | Behavioral Journey | `STA_behavioral_change_journey.tex` |
| HI | HIE | Decision Hierarchy | `HIE_decision_hierarchy.tex` |

### Most-Used Appendices (⚠️ High impact)
| Old | New | References | File |
|-----|-----|------------|------|
| G | GLS | 58+ | Glossary |
| V | WEN | 39+ | Psi Dimensions |
| B | HOW | 38+ | Complementarity |
| BBB | WHERE | 29+ | Parameters |
| AAA | WHO | 24+ | Hierarchy |

---

## Migration Timeline

### Execution Steps
1. **Pre-checks** (~30 sec)
   - Validate mapping consistency
   - Detect any circular dependencies
   - Verify file access

2. **Create Backups** (~2 min)
   - Copy all 330 files to backup directory
   - Generate MD5 checksums for integrity

3. **Rename Files** (~5 min)
   - Rename 122 appendix files from old to new codes
   - Update index references

4. **Update References** (~90 min)
   - Text replacements in 300+ files
   - LaTeX reference updates
   - Axiom/theorem reference updates

5. **Post-Migration Validation** (~30 min)
   - Verify old codes are completely gone
   - Check new codes exist
   - Validate checksums

6. **Generate Report** (~5 min)
   - Create detailed execution log
   - Document all changes made

**Total Expected Time:** 2-3 hours

---

## Files Most Affected

### Highest Reference Counts
1. **HHH_METHOD-TOOLKIT.tex** → TKT_METHOD-TOOLKIT.tex
   - Contains 50+ references to other appendices
   - Will be updated with new codes throughout

2. **AAA_aggregation_levels.tex** → WHO_aggregation_levels.tex
   - References 40+ CORE and METHOD appendices
   - Critical for framework structure

3. **C_fepsde_matrix.tex** → WAT_fepsde_matrix.tex
   - Multi-dimensional welfare reference
   - Referenced from chapters 01-21

4. **EEE_METHOD-DESIGN_model_design_workflow.tex** → DSN_METHOD-DESIGN_model_design_workflow.tex
   - References FFF, GGG, AN, B, C, V, BBB
   - Core methodology document

### All 23 Chapters Affected
Every chapter currently references at least one appendix. All references will be updated:
- Chapter 01: 13 appendix references
- Chapter 10: 8 appendix references
- Chapter 17: 10 appendix references
- ...and so on across all 23 chapters

---

## Rollback Procedure

If anything goes wrong, **instant rollback is available**:

```bash
# Restore everything from checksum-verified backups
python scripts/execute-complete-migration.py --rollback

# Time: ~2 minutes
# Result: Complete restoration to pre-migration state
```

---

## Verification Steps (After Execution)

Run these to verify success:

```bash
# 1. Check that all new codes exist
ls appendices/DER_* appendices/WHO_* appendices/WAT_* ...

# 2. Check that old codes are gone
ls appendices/A_* appendices/AA_* ...  # Should show: No such file

# 3. Verify LaTeX compilation
cd /home/user/complementarity-context-framework
latexmk -pdf outputs/main.tex

# 4. Check for undefined references
grep -r "??" outputs/main.pdf  # Should be empty
```

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Data loss | ✅ Full checksummed backups |
| Incomplete updates | ✅ All 1,573 references tracked and validated |
| Circular dependencies | ✅ Pre-checks detect and report |
| Partial migration failure | ✅ Automatic rollback on error |
| LaTeX compilation errors | ✅ Post-migration validation before final commit |

---

## Commands to Execute Migration

### Safe (Recommended First)
```bash
# See what would change (NO actual changes made)
python scripts/execute-complete-migration.py --dry-run
```

### Execute Full Migration
```bash
# Actually perform the migration
python scripts/execute-complete-migration.py --execute
# Will prompt for confirmation: "Type 'yes' to proceed"
```

### Rollback if Needed
```bash
# Restore from backups instantly
python scripts/execute-complete-migration.py --rollback
```

### Validate Existing Migration
```bash
# Check if migration is complete and consistent
python scripts/execute-complete-migration.py --validate
```

---

## Expected Output During Execution

```
================================================================================
APPENDIX CODE MIGRATION SYSTEM
================================================================================
Mode: EXECUTE
Execution ID: execution-20260115-HHMMSS

PHASE 1: PRE-MIGRATION CHECKS
✅ 82 unique codes, no duplicates
✅ No circular dependencies detected
✅ 122 appendix files found, 85 codes present
✅ File system access verified

PHASE 2: CREATE BACKUPS
✅ Backed up to migration-audit/execution-20260115-HHMMSS/backups/appendices
✅ Backed up to migration-audit/execution-20260115-HHMMSS/backups/chapters
✅ Backed up to migration-audit/execution-20260115-HHMMSS/backups/docs
✅ Backed up to migration-audit/execution-20260115-HHMMSS/backups/models
✅ Total files backed up: 330

PHASE 3: DRY-RUN SIMULATION
✅ Simulating 122 file renames
✅ Simulating 1,573 reference updates
✅ Dry-run: 1,573 references would be updated

PHASE 4: EXECUTE MIGRATION
[Actual file renames and updates happening...]
✅ Renamed 122 files
✅ Updated 1,573 references

PHASE 5: POST-MIGRATION VALIDATION
✅ Verified old codes are gone
✅ Verified new codes exist
✅ Verified reference integrity

PHASE 6: GENERATE REPORT
✅ Migration completed successfully
```

---

## Key Dates & Versions

| Version | Date | Status |
|---------|------|--------|
| 1.0 | 2026-01-15 | ✅ Dry-run validated |
| Ready for | 2026-01-15 | ✅ Execution-ready |

---

## Support & Questions

If issues arise:

1. Check migration.log in execution directory
2. Review dry-run results in MIGRATION-VALIDATION-SUMMARY.md
3. Rollback instantly if needed: `--rollback` mode
4. Run diagnostic: `--validate` mode

---

**Status: ✅ READY FOR EXECUTION**

Execute when approved:
```bash
python scripts/execute-complete-migration.py --execute
```

---

*Generated: 2026-01-15*
*Validation ID: execution-20260115-174730*
