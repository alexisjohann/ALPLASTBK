# SOP-APPEND-02: Appendix Code & Naming Management

> **Purpose:** Standardized protocol for assigning, validating, and managing appendix codes to prevent conflicts
> **Version:** 1.0
> **Date:** 2026-01-15
> **Owner:** Appendix Management Team
> **Review Cycle:** Quarterly
> **Related:** SOP-SCRIPT-01, SOP-INDEX-03, SOP-RECOVERY-04

---

## 1. Scope

This SOP prevents the **25-code-conflict bug** that occurred with register_lit_appendices.py.

**Applies to:**
- Assigning new appendix codes (AA-ZZ range + special codes)
- Naming appendix files
- Registering appendices in index
- Detecting conflicts BEFORE execution
- Managing code lifecycle (active, deprecated, reserved)

---

## 2. The 8 Appendix Categories (Reference)

```
CORE-:      Core Theory (9 codes: AAA, C, B, V, BBB, AU, AV, AW, HI)
FORMAL-:    Formalization (11 codes: A, D, BA, BB, BC, BJ, etc.)
DOMAIN-:    Applications (17 codes: AA-AG, AJ, AK, W-Z, etc.)
CONTEXT-:   Context factors (3 codes: AH, AI, V overlap with CORE)
METHOD-:    Methodology (12 codes: AN, AL, E, R, AZ, etc.)
PREDICT-:   Predictions (7 codes: S, AO-AT)
LIT-:       Literature (30 codes: I-Q, U, R, S, T, W, X, AM, AX, AY, etc.)
REF-:       Reference (5 codes: F, G, H, T, DDD)
```

**Problem:** Multiple codes overlap! (e.g., V used by both CORE and CONTEXT)

---

## 3. Code Availability System

### 3.1 Available Single-Letter Codes

```
RESERVED (Never use):
  ├─ A, B, C, D → FORMAL/CORE foundation
  ├─ E, F, G, H → METHOD/REF foundation
  ├─ I-Q → LIT foundation (14 codes)
  └─ R, S, T, U, V, W, X → Multi-use (overlap problem!)

AVAILABLE (Use for new LIT/CUSTOM):
  ├─ Y, Z (only 2 left!)
  └─ !! ALMOST FULL !!
```

**WARNING:** Single-letter space nearly exhausted!

### 3.2 Available Two-Letter Codes (Primary)

```
PRIMARY RANGE (Recommended for all NEW appendices):

✅ BF-BZ (22 slots, AVAILABLE):
   BF ← DOMAIN-GENERALIZATION
   BG ← FORMAL-LEARNING
   BH-BZ ← 19 unused slots

✅ CA-CZ (26 slots, AVAILABLE)

✅ DA-DZ (26 slots, AVAILABLE)

... and so on until ZZ
```

**Best Practice:** Use two-letter codes for all NEW appendices (never go back to single-letter!)

### 3.3 The Master Code Registry

**Location:** `docs/operations/APPENDIX_CODE_REGISTRY.yaml`

```yaml
code_registry:
  version: "1.0"
  last_updated: "2026-01-15"
  total_assigned: 93
  total_available: 400+

  assigned_codes:
    AAA:
      category: CORE-WHO
      status: ACTIVE
      created: "2024-01-01"
      file: appendices/AAA_core_who.tex
      updated: "2026-01-15"

    C:
      category: CORE-WHAT
      status: ACTIVE
      created: "2024-01-01"
      file: appendices/C_core_what.tex
      note: "Single-letter (legacy) - don't create new"

    BF:
      category: DOMAIN-GENERALIZATION
      status: ACTIVE
      created: "2026-01-15"
      file: appendices/BF_DOMAIN-GENERALIZATION.tex
      note: "Two-letter (new standard)"

    V:
      category: CORE-WHEN / CONTEXT-MASTER / FORMAL-MEP
      status: CONFLICT ⚠️
      severity: HIGH
      note: "Used by 3 categories! Must resolve."
      action: "Deprecated CONTEXT-MASTER → use AI instead"

    X:
      category: CORE-WHO / FORMAL-FOUND / LIT-LOEWENSTEIN
      status: CONFLICT ⚠️
      severity: CRITICAL
      note: "Used by 3 categories! Triple conflict!"

    VVV:
      category: UNDOCUMENTED-PROJECT
      status: ORPHAN
      created: "2025-11-20"
      note: "7 files, not in index"
      action: "Integrate or remove"

  available_ranges:
    single_letter:
      total: 26
      used: 24
      available: 2  # Y, Z only
      note: "EXHAUSTED - Don't use for new!"

    two_letter_BF_BZ:
      total: 22
      used: 2  # BF, BG
      available: 20
      recommended: YES

    two_letter_CA_DZ:
      total: 78
      used: 0
      available: 78
      recommended: YES
```

---

## 4. Before Assigning a Code: 5-Point Checklist

**MANDATORY - DO THIS FIRST:**

### Step 1: Check Code Availability

```bash
#!/bin/bash
# Check if code is available

CODE="$1"  # e.g., "BF"

# Method 1: Search index
grep "^$CODE " docs/operations/APPENDIX_CODE_REGISTRY.yaml && \
  echo "❌ Code $CODE is ALREADY USED" || \
  echo "✅ Code $CODE is AVAILABLE"

# Method 2: Search all appendices
grep -l "^\\\\section{\\\\label{app:$CODE}" appendices/*.tex && \
  echo "❌ Code $CODE found in files" || \
  echo "✅ Code $CODE not in files"

# Method 3: Sanity check index
grep -E "($CODE &|$CODE \\\\)" appendices/00_appendix_index.tex && \
  echo "❌ Code $CODE in index" || \
  echo "✅ Code $CODE not in index"
```

### Step 2: Identify Category Constraints

```markdown
My new appendix is about: [TOPIC]

Category mapping:
  ├─ Is it core theory (WHO/WHAT/HOW)?       → CORE-
  ├─ Is it mathematical?                     → FORMAL-
  ├─ Is it application/domain-specific?      → DOMAIN-
  ├─ Is it about context (Ψ)?                → CONTEXT-
  ├─ Is it methodology/measurement?          → METHOD-
  ├─ Is it predictions/tests?                → PREDICT-
  ├─ Is it literature review by author?      → LIT-
  └─ Is it reference/utility?                → REF-

Selected category: [CATEGORY]
```

### Step 3: Check for Conflicts

```python
# Python utility to check conflicts
def check_code_conflicts(code):
    """Check if code is used in multiple categories."""

    with open('docs/operations/APPENDIX_CODE_REGISTRY.yaml') as f:
        registry = yaml.load(f)

    conflicts = registry['code_registry']['assigned_codes'][code]
    if 'status' in conflicts and conflicts['status'] == 'CONFLICT':
        print(f"⚠️ WARNING: Code {code} has conflicts!")
        print(f"   Used by: {conflicts['category']}")
        return False
    else:
        return True

# Usage
check_code_conflicts('V')  # ⚠️ WARNING: Used by 3 categories
check_code_conflicts('BF') # ✅ OK
check_code_conflicts('BZ') # ✅ AVAILABLE
```

### Step 4: Plan Filename

```
NAMING CONVENTION:
  [CODE]_[CATEGORY]-[NAME]_[description].tex

EXAMPLES:
  ✅ GOOD:
     BF_DOMAIN-GENERALIZATION_Elite-Selection.tex
     BG_FORMAL-LEARNING_Theorems.tex

  ❌ WRONG:
     LIT-THALER.tex                    (missing code!)
     R_LIT-THALER.tex                  (code R already used!)
     appendix_thaler.tex               (no convention!)
```

### Step 5: Create Registry Entry

```yaml
# BEFORE creating any file, add to registry:

new_code:
  XY:                                    # Code you want to use
    category: DOMAIN-YOUR-CATEGORY
    status: RESERVED                     # Reserved (not ACTIVE yet)
    created: "2026-01-15"
    creator: "YOUR_NAME"
    file: appendices/XY_DOMAIN-...tex
    planned: YES
    note: "Planning new appendix on [topic]"
```

---

## 5. The 3-Phase Appendix Lifecycle

### Phase 1: Planning (Status = RESERVED)

```markdown
# Before you write anything:

1. ✅ Code checked for conflicts        [SOP-APPEND-02 Section 4]
2. ✅ Category confirmed                [Ask: CORE/FORMAL/DOMAIN/etc?]
3. ✅ Filename planned                  [Format: CODE_CATEGORY-NAME.tex]
4. ✅ Registry entry created (RESERVED) [docs/operations/APPENDIX_CODE_REGISTRY.yaml]
5. ✅ Template copied                   [cp 00_appendix_template.tex NEW_FILE.tex]

→ Only then: Start writing content
```

### Phase 2: Development (Status = DRAFT)

```markdown
# While writing:

1. ✅ Content follows template           [appendices/00_appendix_template.tex]
2. ✅ Compliance score ≥ 85%             [python scripts/check_template_compliance.py]
3. ✅ Cross-references added             [Link to related appendices]
4. ✅ Glossary updated                   [Appendix G entries for new terms]
5. ✅ Registry updated (DRAFT)           [Add draft date, content description]

→ Ready for review
```

### Phase 3: Registration (Status = ACTIVE)

```markdown
# When file is finalized:

1. ✅ File compliance 100%               [All checks pass]
2. ✅ Index updated (all 4 locations)    [SOP-INDEX-03]
3. ✅ Cross-references bidirectional     [A→B and B→A both work]
4. ✅ Registry marked ACTIVE             [Not DRAFT, not RESERVED]
5. ✅ Committed to git                   [With clear commit message]

→ Now in production
```

---

## 6. Registration Procedure (The Bug Fix)

**What register_lit_appendices.py did WRONG:**

```python
# ❌ BUG: No conflict checking!
new_appendices = [
    {'code': 'R', ...},  # ❌ Already used by METHOD-EVAL!
    {'code': 'S', ...},  # ❌ Already used by PREDICT-MASTER!
    {'code': 'T', ...},  # ❌ Already used by REF-META!
    {'code': 'W', ...},  # ❌ Already used by DOMAIN!
    {'code': 'X', ...},  # ❌ Already used by 3 categories!
]
```

**Correct procedure (using available codes):**

```python
# ✅ CORRECT: Check availability first!

def validate_codes_before_registration(new_appendices):
    """
    MANDATORY: Validate all codes BEFORE any index modification.
    """

    # 1. Load registry
    with open('docs/operations/APPENDIX_CODE_REGISTRY.yaml') as f:
        registry = yaml.load(f)

    used_codes = set(registry['code_registry']['assigned_codes'].keys())
    requested_codes = [app['code'] for app in new_appendices]

    # 2. Check for conflicts
    conflicts = set(requested_codes) & used_codes
    if conflicts:
        raise ValueError(
            f"❌ CODE CONFLICTS DETECTED: {conflicts}\n"
            f"Available two-letter codes: BF-BZ, CA-DZ\n"
            f"Use: python scripts/find_available_codes.py"
        )

    # 3. Check format
    for app in new_appendices:
        if not re.match(r'^[A-Z]{2}$', app['code']):
            raise ValueError(
                f"❌ INVALID CODE FORMAT: {app['code']}\n"
                f"Must be two letters (e.g., BF, BG, CA)\n"
                f"Single-letter codes (A-Z) are EXHAUSTED!"
            )

    # 4. Update registry (BEFORE modifying index!)
    for app in new_appendices:
        registry['code_registry']['assigned_codes'][app['code']] = {
            'category': app['category'],
            'status': 'RESERVED',
            'created': datetime.now().isoformat(),
            'file': f"appendices/{app['code']}_...tex"
        }

    with open('docs/operations/APPENDIX_CODE_REGISTRY.yaml', 'w') as f:
        yaml.dump(registry, f)

    print(f"✅ Validation passed: {len(new_appendices)} codes verified")
    return True

# Usage:
new_lit_appendices = [
    {'code': 'BF', 'category': 'LIT-THALER', ...},
    {'code': 'BG', 'category': 'LIT-SUNSTEIN', ...},
    {'code': 'BH', 'category': 'LIT-CAMERER', ...},
    # ... etc (using BF-BZ range, not exhausted S/T/W/X!)
]

validate_codes_before_registration(new_lit_appendices)
```

---

## 7. Common Conflicts & Resolution

### 7.1 Current Known Conflicts

| Code | Used By | Status | Action |
|------|---------|--------|--------|
| **V** | CORE-WHEN + CONTEXT + FORMAL-MEP | CRITICAL | Consolidate to CORE-WHEN |
| **X** | CORE-WHO + FORMAL-FOUND + LIT-LOEWENSTEIN | CRITICAL | Rename LIT to BJ |
| **W** | DOMAIN-COMPLEMENTARITIES + LIT-ARIELY | HIGH | Rename LIT to BI |
| **AA-AG, W-Z** | DOMAIN + LIT overlaps | HIGH | Migrate LIT to BF-BZ range |

### 7.2 Conflict Resolution SOP

```markdown
# If you find a conflict:

1. Document it:
   Code: X
   Conflict: Used by CORE-WHO AND LIT-LOEWENSTEIN
   Severity: CRITICAL

2. Report it:
   - Add to quality/known_issues.md
   - Create GitHub issue
   - Add to APPENDIX_CODE_REGISTRY.yaml with status: CONFLICT

3. Plan resolution:
   Option A: Rename conflicting category to available code
   Option B: Consolidate categories
   Option C: Reserve code for highest-priority category

4. Execute resolution:
   - Use SOP-RECOVER-04 for safe renaming
   - Update all files and indices
   - Test integrity

5. Validate:
   - Run python scripts/validate_appendix_integrity.py
   - All 4 index locations updated
   - All cross-references work
```

---

## 8. Best Practices

### DO ✅
- Use two-letter codes for NEW appendices (BF-BZ and beyond)
- Check availability BEFORE writing content
- Update registry BEFORE modifying index
- Run dry-run BEFORE production execution
- Document every decision (why this code? why this category?)

### DON'T ❌
- Don't use single-letter codes (A-Z are exhausted)
- Don't assume a code is available (check first!)
- Don't modify index without checking registry
- Don't create files without planning filename first
- Don't register code without 85%+ compliance check

---

## 9. Tools & Scripts

### 9.1 Available Code Finder

```bash
#!/bin/bash
# Find available codes

echo "Single-letter (A-Z): Mostly exhausted, only Y, Z available"
echo ""
echo "Two-letter ranges:"
echo "  BF-BZ:  $(grep -c '^B[F-Z]' docs/operations/APPENDIX_CODE_REGISTRY.yaml) used, $(( 22 - $(grep -c '^B[F-Z]' docs/operations/APPENDIX_CODE_REGISTRY.yaml) )) available"
echo "  CA-CZ:  $(grep -c '^C[A-Z]' docs/operations/APPENDIX_CODE_REGISTRY.yaml) used, $(( 26 - $(grep -c '^C[A-Z]' docs/operations/APPENDIX_CODE_REGISTRY.yaml) )) available"
echo ""
echo "Recommended: Use BF-BZ range first (22 slots)"
echo ""

# List available codes in BF-BZ
echo "Available in BF-BZ:"
for i in {66..90}; do  # ASCII B=66 to Z=90
    CODE=$(printf "\\$(printf '%03o' $i)")
    grep -q "^${CODE}" docs/operations/APPENDIX_CODE_REGISTRY.yaml || echo "  ✅ ${CODE}"
done
```

### 9.2 Conflict Detector

```python
#!/usr/bin/env python3
"""Detect code conflicts in appendix system."""

def find_conflicts():
    import re
    import glob
    from pathlib import Path

    # Extract codes from files
    file_codes = {}
    for filepath in glob.glob('appendices/*_*.tex'):
        match = re.match(r'appendices/([A-Z]+)_', Path(filepath).name)
        if match:
            code = match.group(1)
            file_codes[code] = filepath

    # Extract codes from index
    index_codes = {}
    with open('appendices/00_appendix_index.tex') as f:
        for line in f:
            match = re.match(r'^([A-Z]+)\s+&', line)
            if match:
                code = match.group(1)
                index_codes[code] = line.strip()

    # Check for mismatches
    file_only = set(file_codes.keys()) - set(index_codes.keys())
    index_only = set(index_codes.keys()) - set(file_codes.keys())

    print(f"Files without index entry: {file_only}")
    print(f"Index without file: {index_only}")
    print(f"Total files: {len(file_codes)}")
    print(f"Total index entries: {len(index_codes)}")

    if file_only or index_only:
        return False  # Conflicts exist
    return True  # No conflicts

find_conflicts()
```

---

## 10. SOP Version & Change Log

| Version | Date | Changes | Status |
|---------|------|---------|--------|
| 1.0 | 2026-01-15 | Initial release - addresses 25-code-conflict bug | ACTIVE |

---

*SOP-APPEND-02 | Version 1.0 | Owner: Appendix Management Team*
