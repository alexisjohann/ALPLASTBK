# SOP-SCRIPT-01: General Script Management & Execution Protocol

> **Purpose:** Standardized protocol for developing, validating, and executing Python scripts in the EBF repository
> **Version:** 1.0
> **Date:** 2026-01-15
> **Owner:** Operations Team
> **Review Cycle:** Quarterly

---

## 1. Scope & Applicability

This SOP applies to **all Python scripts** in `/scripts/` directory that:
- Modify repository state (appendices, index, databases)
- Generate outputs or derivatives
- Require manual execution or CI/CD integration
- Impact multiple systems (cross-references, indexing, etc.)

**Out of Scope:**
- One-time data migration scripts
- Individual analysis/exploration scripts
- Development prototypes

---

## 2. The 4-Phase Script Lifecycle

```
┌────────────────────────────────────────────────────────┐
│ PHASE 1: DESIGN                                        │
├────────────────────────────────────────────────────────┤
│ Input: Feature request or bug fix                      │
│ Output: Script specification + validation plan         │
│ Owner: Developer                                       │
└────────────┬───────────────────────────────────────────┘
             ↓
┌────────────────────────────────────────────────────────┐
│ PHASE 2: DEVELOPMENT                                   │
├────────────────────────────────────────────────────────┤
│ Input: Specification                                   │
│ Output: Code + pre-execution checklist + SOP draft     │
│ Owner: Developer                                       │
└────────────┬───────────────────────────────────────────┘
             ↓
┌────────────────────────────────────────────────────────┐
│ PHASE 3: VALIDATION & DRY-RUN                          │
├────────────────────────────────────────────────────────┤
│ Input: Code + checklist                                │
│ Output: Validated script + frozen SOP                  │
│ Owner: Operations Review                               │
└────────────┬───────────────────────────────────────────┘
             ↓
┌────────────────────────────────────────────────────────┐
│ PHASE 4: EXECUTION & VERIFICATION                      │
├────────────────────────────────────────────────────────┤
│ Input: Validated script                                │
│ Output: Execution log + post-verification report       │
│ Owner: Operations Executor                             │
└────────────────────────────────────────────────────────┘
```

---

## 3. PHASE 1: Design

### 3.1 Script Specification Document

**Create BEFORE writing any code:**

```markdown
# Script Specification: [SCRIPT_NAME]

## Purpose
[What problem does this solve?]

## Inputs
- Input 1: [Description, format, location]
- Input 2: ...

## Outputs
- Output 1: [Description, format, location]
- Output 2: ...

## Preconditions (What must be true BEFORE running?)
- [ ] Condition 1
- [ ] Condition 2
- [ ] Condition 3

## Postconditions (What will be true AFTER running?)
- [ ] Condition 1
- [ ] Condition 2

## Edge Cases & Error Handling
- If [condition], then [action]
- If [error], then [recovery]

## Affected Systems
- [ ] Appendix index?
- [ ] Paper database?
- [ ] Cross-references?
- [ ] Generated outputs?

## Dependencies
- External libraries: [list]
- Files required: [list]
- Other scripts: [list]

## Undo Strategy
- How to rollback if script fails?
- How to recover corrupted state?
```

---

## 4. PHASE 2: Development

### 4.1 Code Structure

**Every script must include:**

```python
#!/usr/bin/env python3
"""
Script Name: [NAME]
Purpose: [PURPOSE]
Version: 1.0
Date: YYYY-MM-DD

Execution:
    python script_name.py [--dry-run] [--verbose]

Safety Features:
    - Dry-run mode (no writes by default)
    - Backup creation
    - Validation checks
    - Logging
    - Rollback capability
"""

import logging
import argparse
from pathlib import Path
from datetime import datetime

# ============================================================================
# CONFIGURATION
# ============================================================================

DRY_RUN = False
VERBOSE = False
BACKUP_DIR = Path("backups")
LOG_FILE = f"logs/script_execution_{datetime.now().isoformat()}.log"

# ============================================================================
# LOGGING SETUP
# ============================================================================

def setup_logging():
    """Configure logging for this execution."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()

# ============================================================================
# PRECONDITION CHECKS
# ============================================================================

def check_preconditions():
    """Verify all preconditions before executing."""
    logger.info("Checking preconditions...")

    checks = {
        "Input file exists": Path("data/input.yaml").exists(),
        "Write permissions": Path(".").is_writable(),
        "Backup directory": BACKUP_DIR.exists(),
    }

    for check_name, result in checks.items():
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"  {check_name}: {status}")
        if not result:
            raise RuntimeError(f"Precondition failed: {check_name}")

    logger.info("✅ All preconditions passed")

# ============================================================================
# MAIN LOGIC
# ============================================================================

def create_backup(filepath):
    """Create timestamped backup of file before modification."""
    backup_path = BACKUP_DIR / f"{filepath.stem}.BACKUP.{datetime.now().isoformat()}.{filepath.suffix}"
    if not DRY_RUN:
        shutil.copy(filepath, backup_path)
        logger.info(f"✅ Backup created: {backup_path}")
    else:
        logger.info(f"[DRY-RUN] Would create backup: {backup_path}")
    return backup_path

def execute_transformation(data):
    """Perform the core transformation."""
    logger.info("Executing transformation...")

    # Your logic here
    transformed = do_something(data)

    logger.info(f"✅ Transformation complete: {len(transformed)} items")
    return transformed

def validate_output(output):
    """Verify output meets expected criteria."""
    logger.info("Validating output...")

    checks = {
        "Output not empty": len(output) > 0,
        "No duplicates": len(output) == len(set(output)),
        "Valid schema": all(validate_item(item) for item in output),
    }

    for check_name, result in checks.items():
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"  {check_name}: {status}")
        if not result:
            raise ValueError(f"Validation failed: {check_name}")

    logger.info("✅ All validations passed")
    return True

def save_output(output, filepath):
    """Write output to file with safety checks."""
    logger.info(f"Saving output to {filepath}...")

    if not DRY_RUN:
        with open(filepath, 'w') as f:
            json.dump(output, f, indent=2)
        logger.info(f"✅ Output saved: {filepath}")
    else:
        logger.info(f"[DRY-RUN] Would save {len(output)} items to {filepath}")

# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main execution flow."""
    logger.info("=" * 80)
    logger.info(f"STARTING: {__doc__.split(chr(10))[1]}")
    logger.info(f"Dry-run: {DRY_RUN}")
    logger.info("=" * 80)

    try:
        # Phase 1: Preconditions
        check_preconditions()

        # Phase 2: Load input
        input_data = load_input()
        backup_path = create_backup(Path("data/input.yaml"))

        # Phase 3: Transform
        output_data = execute_transformation(input_data)

        # Phase 4: Validate
        validate_output(output_data)

        # Phase 5: Save
        save_output(output_data, Path("outputs/result.json"))

        logger.info("=" * 80)
        logger.info("✅ EXECUTION COMPLETE - All phases succeeded")
        logger.info("=" * 80)

    except Exception as e:
        logger.error(f"❌ EXECUTION FAILED: {str(e)}")
        logger.error(f"Backup available at: {backup_path}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    parser.add_argument("--verbose", action="store_true", help="Verbose logging")
    args = parser.parse_args()

    DRY_RUN = args.dry_run
    VERBOSE = args.verbose

    main()
```

### 4.2 Pre-Execution Checklist

**Every script must have:**

```markdown
# Pre-Execution Checklist for [SCRIPT_NAME]

## Code Quality
- [ ] Docstring complete (purpose, inputs, outputs)
- [ ] All functions documented
- [ ] Logging added throughout
- [ ] Error handling for all file I/O
- [ ] No hardcoded paths (use Path objects)
- [ ] No print() statements (use logging)

## Safety Features
- [ ] Dry-run mode implemented (--dry-run flag)
- [ ] Backup creation before modifications
- [ ] Precondition checks implemented
- [ ] Postcondition validation implemented
- [ ] Rollback strategy documented
- [ ] Audit trail logging added

## Dependencies
- [ ] All imports documented
- [ ] External packages listed in requirements
- [ ] No circular dependencies
- [ ] Compatible with Python 3.8+

## Testing
- [ ] Unit tests for core functions
- [ ] Dry-run test successful
- [ ] Edge cases tested
- [ ] Error conditions tested

## Documentation
- [ ] SOP draft written
- [ ] Inputs/outputs documented
- [ ] Preconditions documented
- [ ] Affected systems documented
- [ ] Rollback procedure documented
```

### 4.3 SOP Draft

**Create alongside code:**

```markdown
# SOP-CUSTOM-XX: [Script Name] Execution

## When to Use This Script
[Describe the problem and solution]

## Prerequisites
- [ ] Precondition 1
- [ ] Precondition 2

## How to Execute

### Step 1: Dry-Run (NO CHANGES)
```bash
python scripts/script_name.py --dry-run --verbose
```

Review output. If OK, proceed to Step 2.

### Step 2: Create Manual Backup
```bash
cp appendices/00_appendix_index.tex appendices/00_appendix_index.BACKUP.$(date +%s)
```

### Step 3: Execute
```bash
python scripts/script_name.py
```

Watch output for ✅ or ❌ markers.

### Step 4: Validate
```bash
python scripts/validate_integrity.py
```

All checks should pass.

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| Error 1 | Cause | Run rollback command |
| Error 2 | Cause | Manual fix |

## Rollback Procedure
```bash
cp appendices/00_appendix_index.BACKUP.XXX appendices/00_appendix_index.tex
git status  # Verify state restored
```
```

---

## 5. PHASE 3: Validation & Dry-Run

### 5.1 Operations Review Checklist

**Before any production execution:**

```markdown
# Operations Review: [SCRIPT_NAME]

Reviewer: _______________  Date: _______________

## Code Review
- [ ] Preconditions checked
- [ ] Postconditions validated
- [ ] Error handling complete
- [ ] Logging sufficient
- [ ] Dry-run mode works correctly
- [ ] Backup strategy sound
- [ ] No hardcoded values

## Safety Review
- [ ] Dry-run executed successfully
- [ ] All test cases passed
- [ ] Edge cases handled
- [ ] Rollback tested
- [ ] Performance acceptable (no N² bugs)
- [ ] Memory usage reasonable

## Documentation Review
- [ ] SOP is complete
- [ ] All preconditions documented
- [ ] All affected systems identified
- [ ] Rollback procedure clear
- [ ] Example execution shown

## Affected Systems Impact Analysis
- [ ] Appendix index: [ ] Not affected / [ ] Modified / [ ] Risk
- [ ] Paper database: [ ] Not affected / [ ] Modified / [ ] Risk
- [ ] Cross-references: [ ] Not affected / [ ] Modified / [ ] Risk
- [ ] Generated outputs: [ ] Not affected / [ ] Modified / [ ] Risk

## Risk Assessment

**Risk Level:** [ ] Low / [ ] Medium / [ ] High

**Justification:**
[Explain risk level and mitigations]

## Sign-Off

**Approved for Production:** [ ] YES / [ ] NO

**Comments:**
[Any additional notes]

---
Reviewed by: _______________ Date: _______________
```

### 5.2 Dry-Run Protocol

```bash
# Step 1: Code review complete ✅

# Step 2: Run dry-run
python scripts/script_name.py --dry-run --verbose 2>&1 | tee dry-run.log

# Step 3: Inspect output
cat dry-run.log
# Should show all changes without writing

# Step 4: Verify preconditions reported
grep "✅ PASS\|❌ FAIL" dry-run.log

# Step 5: Verify postconditions
grep "Validation" dry-run.log

# Step 6: If all green ✅ → Proceed to Phase 4
# If any red ❌ → Stop, fix code, repeat
```

---

## 6. PHASE 4: Execution & Verification

### 6.1 Execution Procedure

```bash
#!/bin/bash
# Safe execution wrapper for scripts

SCRIPT_NAME="$1"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_DIR="logs"
BACKUP_DIR="backups"

mkdir -p "$LOG_DIR" "$BACKUP_DIR"

# Step 1: Final dry-run
echo "🔍 Running final dry-run..."
python "scripts/$SCRIPT_NAME.py" --dry-run > "$LOG_DIR/$SCRIPT_NAME.dry-run.$TIMESTAMP.log" 2>&1

if [ $? -ne 0 ]; then
    echo "❌ Dry-run failed! Aborting."
    exit 1
fi
echo "✅ Dry-run passed"

# Step 2: Manual approval
echo ""
echo "Review dry-run output above. Continue? (y/n)"
read -r APPROVAL

if [ "$APPROVAL" != "y" ]; then
    echo "❌ Aborted by user"
    exit 1
fi

# Step 3: Create backup
echo "💾 Creating backup..."
# (backend-specific backup logic)
echo "✅ Backup created"

# Step 4: Execute
echo ""
echo "🚀 Executing script..."
python "scripts/$SCRIPT_NAME.py" > "$LOG_DIR/$SCRIPT_NAME.execution.$TIMESTAMP.log" 2>&1

RESULT=$?

# Step 5: Verify
echo ""
echo "✔️ Verifying execution..."
python "scripts/validate_integrity.py" > "$LOG_DIR/$SCRIPT_NAME.validation.$TIMESTAMP.log" 2>&1

VALIDATION=$?

# Step 6: Report
echo ""
echo "=" * 80
if [ $RESULT -eq 0 ] && [ $VALIDATION -eq 0 ]; then
    echo "✅ EXECUTION SUCCESSFUL"
    echo "Log: $LOG_DIR/$SCRIPT_NAME.execution.$TIMESTAMP.log"
else
    echo "❌ EXECUTION FAILED"
    echo "Execution log: $LOG_DIR/$SCRIPT_NAME.execution.$TIMESTAMP.log"
    echo "Validation log: $LOG_DIR/$SCRIPT_NAME.validation.$TIMESTAMP.log"
fi
echo "=" * 80
```

### 6.2 Post-Execution Checklist

```markdown
# Post-Execution Verification: [SCRIPT_NAME]

Executor: _______________ Date: _______________ Time: _______________

## Execution Status
- [ ] Script executed without errors
- [ ] All log messages show ✅ completion markers
- [ ] No warnings or errors in logs

## Validation Status
- [ ] Validation script passed all checks
- [ ] No new conflicts introduced
- [ ] No orphan entries created
- [ ] All cross-references valid
- [ ] File integrity verified

## State Verification
- [ ] Expected files modified (list):
  - [ ] File 1: ✅ Modified
  - [ ] File 2: ✅ Modified

- [ ] Unexpected files NOT modified:
  - [ ] File 1: ✅ Untouched
  - [ ] File 2: ✅ Untouched

## Final Sign-Off
- [ ] All checks passed
- [ ] Ready to commit
- [ ] SOP archived with version number

## Execution Summary
- Start time: _______________
- End time: _______________
- Duration: _______________
- Items processed: _______________
- Success rate: _______________

## Artifacts
- Execution log: `logs/script_name.execution.[timestamp].log`
- Validation log: `logs/script_name.validation.[timestamp].log`
- Backup location: `backups/[backup_name]`

---
Verified by: _______________ Date: _______________
```

---

## 7. Script Registry

**Maintain in `/docs/operations/SCRIPT_REGISTRY.yaml`:**

```yaml
scripts:
  - name: register_lit_appendices.py
    version: 1.0
    purpose: "Register new literature appendices in index"
    status: "DEPRECATED - Use SOP-APPEND-02"

  - name: new_script.py
    version: 1.0
    purpose: "Clear description"
    sop: "SOP-CUSTOM-XX: New Script Execution"
    preconditions:
      - "Input file exists"
      - "Write permissions granted"
    affected_systems:
      - "Appendix index"
      - "Paper database"
    execution_frequency: "Monthly"
    owner: "Operations Team"
    last_run: "2026-01-15"
    next_run: "2026-02-15"
    status: "ACTIVE"
```

---

## 8. Troubleshooting & Rollback

### 8.1 Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `FileNotFoundError` | Precondition check failed | Run precondition checks again |
| `ValidationError` | Output doesn't match schema | Review output format |
| `PermissionError` | Write permissions insufficient | Check directory ownership |

### 8.2 Rollback Procedure

**If script fails DURING execution:**

```bash
# 1. Stop execution (Ctrl+C)

# 2. Check backup location (shown in logs)
cat logs/script_name.execution.TIMESTAMP.log | grep "Backup"

# 3. Restore from backup
cp backups/00_appendix_index.BACKUP.XXX appendices/00_appendix_index.tex

# 4. Verify restoration
python scripts/validate_integrity.py

# 5. Investigate root cause
# (don't re-run until bug fixed)
```

---

## 9. SOP Version & Change Log

| Version | Date | Changes | Status |
|---------|------|---------|--------|
| 1.0 | 2026-01-15 | Initial release | ACTIVE |

---

*SOP-SCRIPT-01 | Version 1.0 | Owner: Operations Team*
