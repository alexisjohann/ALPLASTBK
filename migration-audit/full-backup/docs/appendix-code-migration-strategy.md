# Appendix Code Migration Strategy: Complete Methodology

**Date:** 2026-01-15
**Status:** DRAFT - Requires Review
**Scope:** Migrate from 1-3 letter codes to unique 3-letter codes
**Impact:** 98 appendices, 784 references, 50+ files

---

## Executive Summary

### Problem
- **24 duplicate codes** in the repository (e.g., AA used by both DOMAIN-LABOR and LIT-MULLAINATHAN)
- **~50+ files** with conflicting names in flat `appendices/` directory
- **784 references** across LaTeX, Markdown, and YAML files that would break
- **No audit trail** of what references what

### Solution: Unique 3-Letter Code System
```
OLD: AA_labor_economics.tex + AA_LIT-mullainathan.tex (conflict!)
NEW: LAB_labor_economics.tex + MUL_LIT-mullainathan.tex (unique!)
```

**Strategy:**
1. Create complete mapping: old code → unique 3-letter code
2. Scan and document ALL references (audit trail)
3. Rename files with version control
4. Update all references systematically
5. Validate completeness (no broken links)
6. Create permanent audit log

---

## Phase 1: Planning & Mapping (Weeks 1-2)

### Step 1.1: Create Mapping Document
**File:** `docs/frameworks/code-migration-mapping.yaml`

Define mapping for all 98 appendices:
- **CORE:** 9 codes (WHO, WAT, HOW, WEN, WHERE, AWA, REA, STA, HIE)
- **FORMAL:** 11 codes (DER, PRF, SEG, EQU, PBB, EIH, LET, MEP, MEQ, GTC, FND, MDL)
- **DOMAIN:** 21 codes (LAB, MAT, IOO, EVO, MEC, CHO, CMX, CON, SCP, EPS, INF, MIL, CAP, GRW, DFN, EBF, CAT, CHI, BNK, COR, GEN, PAP)
- **METHOD:** 13 codes (LLM, SRL, OPS, EVL, CON, DTP, DSN, REG, CFG, TKT, CMP, RSH, CAL)
- **PREDICT:** 7 codes (PRM, P01, P02, P03, P04, P05, P06)
- **LIT:** 30 codes (MUL, LIS, DOL, SPC, FAL, MAL, SHA, NOB, REC, FEH, ACE, SHL, HEC, AUT, DUF, BLM, THL, SUN, CAM, ARI, LOE, CIA, HAI, KTH, MTA, PAR, HST, CRT, THM, FRM)
- **CONTEXT:** 3 codes (CTM, CTS, CTW)
- **REF:** 5 codes (EXM, GLS, HST, MTA, DTP)

**Conflict Resolution:** See mapping document for all 24 conflict resolutions

### Step 1.2: Create Migration Tools
**Files:**
- `scripts/migrate-appendix-codes.py` - Main migration script
- `migration-audit/` - Audit trail directory

**Capabilities:**
- `--scan`: Find all references (784 expected)
- `--validate`: Check mapping consistency
- `--list-files`: Show all files to rename
- `--plan`: Generate migration plan
- `--summary`: Print migration overview

### Step 1.3: Review & Approval
- Review mapping for correctness
- Validate no new duplicates in 3-letter codes
- Get stakeholder approval
- **Status:** ✅ READY

---

## Phase 2: Reference Scanning (Week 2)

### Step 2.1: Scan All References
```bash
python scripts/migrate-appendix-codes.py --scan
# Generates: migration-audit/reference-scan-report.json
```

**Output:**
- List of ALL 784 references
- File paths and line numbers
- Context for each reference

**Validation Criteria:**
- All code occurrences found
- No false positives
- Complete coverage

### Step 2.2: Generate Audit Trail
```bash
python scripts/migrate-appendix-codes.py --list-files
# Generates: migration-audit/files-to-rename.json
```

**Output:**
- Mapping of old filename → new filename
- Full path information
- Size of each file

### Step 2.3: Create Migration Plan
```bash
python scripts/migrate-appendix-codes.py --plan
# Generates: migration-audit/migration-plan.json
```

**5-Phase Plan:**
1. Backup all files
2. Rename appendix files
3. Update references (automated)
4. Update index
5. Verify & validate

**Status:** ✅ READY

---

## Phase 3: Backup & Version Control (Week 3)

### Step 3.1: Create Complete Backup
```bash
# Automated in migration script
mkdir -p migration-audit/backups/
cp -r appendices/ migration-audit/backups/appendices-backup-2026-01-15/
cp -r docs/ migration-audit/backups/docs-backup-2026-01-15/
cp -r models/ migration-audit/backups/models-backup-2026-01-15/
```

**Backup Contents:**
- All `.tex` files from `appendices/`
- All `.md` files from `docs/`
- All `.md` files from `models/`
- Size: ~200-300 MB

### Step 3.2: Create Git Commit Checkpoint
```bash
git add migration-audit/backups/
git commit -m "chore(migration): Create backup before appendix code migration"
git push origin claude/cardinal-appointments-article-AfQe9
```

**Purpose:** Safe restore point if anything goes wrong

### Step 3.3: Create Rollback Plan
```
If migration fails at ANY point:
1. git reset --hard (to before migration commit)
2. Copy from migration-audit/backups/
3. Investigate failure
4. Fix mapping/script
5. Retry

This ensures ZERO data loss.
```

**Status:** ⏳ READY (after backup)

---

## Phase 4: Execute Migration (Week 4)

### Step 4.1: Rename All Appendix Files

**Script handles:**
```python
# Before
appendices/AA_labor_economics.tex
appendices/AB_matching_repugnant.tex
appendices/AC_industrial_organization.tex
...

# After
appendices/LAB_labor_economics.tex
appendices/MAT_matching_repugnant.tex
appendices/IOO_industrial_organization.tex
...
```

**50+ files renamed in one operation**

### Step 4.2: Update All References in TeX Files

**Pattern matching:**
```
Appendix MUL1 → Appendix LAB
ef{app:MUL1} → \ref{app:LAB}
\label{app:aa-*} → \label{app:lab-*}
appendix{AA} → appendix{LAB}
```

**Examples:**
```latex
% Before
See Appendix MUL1 for labor market applications
\item Appendix WHO (CORE-WHO): Levels $L$ on which dimensions operate

% After
See Appendix LAB for labor market applications
\item Appendix WHO (CORE-WHO): Levels $L$ on which dimensions operate
```

### Step 4.3: Update All References in Markdown Files

**Pattern matching:**
```
Appendix MUL1 → Appendix LAB
[Appendix MUL1](../appendices/AA_labor.tex) → [Appendix LAB](../appendices/LAB_labor.tex)
```

### Step 4.4: Update Appendix Index

**File:** `appendices/00_appendix_index.tex`

Update 3 locations:
1. **DOMAIN section table** (~line 481)
2. **Complete appendix map** (~line 704)
3. **Category counts** (~line 68)

**Example:**
```latex
% Before
AA & DOMAIN-LABOR & Labor Economics & Multi-level labor market analysis \\

% After
LAB & DOMAIN-LABOR & Labor Economics & Multi-level labor market analysis \\
```

### Step 4.5: Generate Validation Reports

```bash
# Check for any remaining old codes
grep -r "Appendix [A-Z][A-Z]" appendices/ docs/ models/ | wc -l
# Expected: ~20 (only CORE/FORMAL like "Appendix WAT", "Appendix HOW" which are intentional)

# Check new code consistency
python scripts/validate-codes.py
# Expected: 0 errors, 98 unique codes
```

**Status:** ⏳ READY (after execution)

---

## Phase 5: Validation & Audit (Week 5)

### Step 5.1: Verify All References Updated

```bash
python scripts/migrate-appendix-codes.py --scan
# Compare with reference-scan-report.json from Phase 2
# Expected: 0 old codes found in new report
```

### Step 5.2: Test LaTeX Compilation

```bash
cd outputs/
latexmk -pdf 00_master_documentation_framework.tex
# Expected: No errors, PDF compiles successfully
```

### Step 5.3: Cross-Reference Validation

```bash
python scripts/validate-cross-references.py
# Expected: All 784 references valid and pointing to correct files
```

### Step 5.4: Generate Audit Report

```bash
python scripts/migrate-appendix-codes.py --audit
# Generates: migration-audit/final-audit-report.md
```

**Report includes:**
- Before/After statistics
- All files renamed
- All references updated
- Any issues/warnings
- Complete change log

### Step 5.5: Create Git Commit

```bash
git add appendices/ docs/ models/ appendices/00_appendix_index.tex
git commit -m "refactor(appendices): Migrate all codes to unique 3-letter system

- Rename 50+ appendix files (AA→LAB, AB→MAT, etc.)
- Update 784 references across TeX, Markdown, YAML files
- Resolve all 24 code conflicts
- Create audit trail in migration-audit/
- Validate completeness with 5-step verification

MIGRATION COMPLETE:
- Old codes: ~60 (1-3 letters)
- New codes: 98 (unique 3 letters)
- Files renamed: 50+
- References updated: 784
- Zero data loss verified
- Audit trail: migration-audit/final-audit-report.md"

git push origin claude/cardinal-appointments-article-AfQe9
```

**Status:** ⏳ READY (after validation)

---

## Phase 6: Documentation & Handoff (Week 6)

### Step 6.1: Update Mapping Documentation

**File:** `docs/frameworks/code-migration-mapping.yaml`

Update status:
```yaml
migration:
  status: COMPLETED
  date: 2026-01-15
  executed_by: claude
  duration: 2 weeks
  files_renamed: 50
  references_updated: 784
  success: true
```

### Step 6.2: Create Migration Guide

**File:** `docs/frameworks/HOW-TO-USE-NEW-CODES.md`

Guide for future work:
- How to find an appendix by code
- How to reference an appendix
- How to create new appendices with 3-letter codes
- Mapping table for reference

### Step 6.3: Archive Audit Trail

**Permanent record:**
```
migration-audit/
├── reference-scan-report.json         # All 784 references found
├── files-to-rename.json               # All 50+ files mapped
├── migration-plan.json                # 5-phase execution plan
├── final-audit-report.md              # Complete audit
├── backups/                           # Full backup (for rollback)
│   ├── appendices-backup-2026-01-15/
│   ├── docs-backup-2026-01-15/
│   └── models-backup-2026-01-15/
└── MIGRATION_COMPLETED.txt            # Success marker
```

**Status:** ✅ READY

---

## Timeline & Effort Estimate

| Phase | Duration | Key Deliverable | Status |
|-------|----------|-----------------|--------|
| 1: Planning | Week 1-2 | Mapping + Tools | ✅ DONE |
| 2: Scanning | Week 2 | Reference Report (784 items) | ⏳ READY |
| 3: Backup | Week 3 | Backup + Commit | ⏳ READY |
| 4: Execute | Week 4 | All files renamed + refs updated | ⏳ READY |
| 5: Validate | Week 5 | Audit Report + Verification | ⏳ READY |
| 6: Handoff | Week 6 | Documentation + Archive | ⏳ READY |

**Total:** 6 weeks (with parallelization, could be 3-4 weeks)

---

## Success Criteria

### Before Migration
- ✅ 24 duplicate codes identified
- ✅ 784 references found
- ✅ ~50+ files with conflicts

### After Migration
- ✅ 0 duplicate codes (98 unique 3-letter codes)
- ✅ All 784 references updated
- ✅ LaTeX compilation successful
- ✅ All cross-references valid
- ✅ Complete audit trail created
- ✅ Zero data loss
- ✅ Version control clean history

---

## Risk Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|-----------|
| References missed | Low | High | 2 independent scans before + after |
| File rename fails | Low | High | Backup + rollback ready |
| LaTeX breaks | Medium | Medium | Compile test before/after |
| Conflicts in merge | Low | High | Clean git history on feature branch |
| Approval delays | Medium | Low | Document everything upfront |

---

## Next Steps

### Immediate (Today)
1. ✅ Review `code-migration-mapping.yaml` for correctness
2. ✅ Review `migrate-appendix-codes.py` for logic
3. ✅ Get stakeholder approval on strategy

### Week 1
1. Run `--scan` to verify all 784 references found
2. Run `--validate` to check mapping consistency
3. Run `--list-files` to review all files to rename
4. Create git checkpoint (current state)

### Week 2-3
1. Execute Phase 3: Create backups
2. Execute Phase 4: Rename files & update references
3. Execute Phase 5: Validation

### Week 4+
1. Documentation & archive
2. Communicate completion to team
3. Begin creating NEW appendices with 3-letter codes (e.g., BF, BG, etc.)

---

## Questions & Clarifications

**Q: What if the mapping is wrong?**
A: Rollback from backup, fix mapping, retry. Audit trail shows exactly what happened.

**Q: What about existing cross-project references to "Appendix MUL1"?**
A: All external docs that reference this repo would need updates. A "redirect" guide can help.

**Q: Can we do this incrementally (not all at once)?**
A: Technically yes, but risky. All-at-once with clean rollback is safer.

**Q: What about GitHub links to files?**
A: GitHub redirects will handle file renames automatically.

---

**Document Version:** 1.0
**Status:** DRAFT - AWAITING APPROVAL
**Owner:** Claude (working on cardinal-appointments-article-AfQe9 branch)
**Next Review:** After stakeholder feedback
