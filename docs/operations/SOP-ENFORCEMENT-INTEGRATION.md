# SOP Enforcement Integration Guide
> **Wo müssen die SOPs implementiert werden, damit sie immer!!! berücksichtigst werden**
> (Where must SOPs be implemented so they are ALWAYS!!! considered/enforced)

**Document**: SOP Enforcement Integration
**Version**: 1.0.0
**Date**: 2026-01-15
**Status**: ACTIVE
**Reference**: `data/config/SOP_ENFORCEMENT.yaml`

---

## Overview: The 5 Critical Integration Points

To ensure SOPs are **ALWAYS** followed (not just recommended), they must be integrated into these **5 critical enforcement points**:

```
┌──────────────────────────────────────────────────────────────────┐
│  ENFORCEMENT PYRAMID (Bottom = Most Enforced)                    │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  5. DOCUMENTATION (CLAUDE.md, SOPs)                              │
│     ↑ References, guidelines, best practices                    │
│                                                                  │
│  4. SCRIPT TEMPLATES (SCRIPT_TEMPLATE.py)                       │
│     ↑ Every script must inherit from this                       │
│                                                                  │
│  3. CRON JOBS (CRON-JOBS-SETUP.sh)                             │
│     ↑ Automated enforcement via scheduled tasks                │
│                                                                  │
│  2. GIT HOOKS (pre-commit.sh, pre-push.sh)                     │
│     ↑ Blocks commits that violate SOPs                         │
│                                                                  │
│  1. CONFIGURATION (SOP_ENFORCEMENT.yaml) ← SINGLE SOURCE OF TRUTH
│     ↑ All enforcement rules defined here                        │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Integration Point #1: Configuration (LEVEL 5 - MOST ENFORCED)

### Location: `data/config/SOP_ENFORCEMENT.yaml`

This is the **single source of truth** for all SOP enforcement rules.

**What it defines:**
- Enforcement levels (STRICT, WARNING, INFO, OFF)
- For each SOP: enabled/disabled, validation rules, severity
- Threshold values (compliance score ≥85%, code conflicts >0, etc.)
- 4-tier validation system specification
- Alert thresholds and metrics

**How it works:**
```
SOP_ENFORCEMENT.yaml (SOURCE OF TRUTH)
    ↓
    ├─→ pre-commit.sh reads rules → validates commits
    ├─→ SCRIPT_TEMPLATE.py reads rules → enforces structure
    ├─→ run_monitoring.py reads rules → checks alerts
    ├─→ validate_tier4.py reads rules → comprehensive check
    └─→ infrastructure_init.py reads rules → setup
```

**Used by these scripts:**
- `.claude/hooks/pre-commit.sh` - Reads enforcement levels
- `scripts/run_monitoring.py` - Reads alert thresholds
- `scripts/validate_tier4.py` - Reads all rules
- `scripts/infrastructure_init.py` - Reads tier configuration

**Key Rules Enforced:**

| Rule | Enforcement | Where | Severity |
|------|-------------|-------|----------|
| Scripts must have SCRIPT_METADATA | STRICT | pre-commit.sh | BLOCKS |
| LaTeX compliance ≥ 85% | STRICT | pre-commit.sh | BLOCKS |
| Code conflicts detection | STRICT | pre-commit.sh | BLOCKS |
| Backup before modify | STRICT | SCRIPT_TEMPLATE.py | BLOCKS |
| Audit logging | STRICT | audit_logger.py | ENFORCED |
| 4-location index sync | STRICT | AppendixIndexManager | BLOCKS |

**Maintenance:**
- Update when SOP rules change
- Version control all changes
- Commit message: `chore: Update SOP enforcement rules in config`

---

## Integration Point #2: Git Hooks (LEVEL 4 - ENFORCED AT COMMIT)

### Locations: `.claude/hooks/pre-commit.sh` and `.claude/hooks/pre-push.sh`

**Pre-Commit Hook** runs BEFORE allowing `git commit`:

```bash
.claude/hooks/pre-commit.sh
├─ Read SOP_ENFORCEMENT.yaml
├─ For each .tex file staged:
│  ├─ Run compliance check (SCRIPT_TEMPLATE + LaTeX)
│  └─ If score < 85%: BLOCK COMMIT
├─ For each .py file staged:
│  ├─ Check SCRIPT_METADATA present
│  ├─ Check SOP reference present
│  └─ If missing: BLOCK COMMIT
├─ Check appendix codes:
│  ├─ Read APPENDIX_CODE_REGISTRY.yaml
│  ├─ Detect conflicts
│  └─ If conflicts found: BLOCK COMMIT
└─ Check index sync:
   ├─ Verify 4 locations updated
   └─ If out of sync: BLOCK COMMIT
```

**What it validates:**

1. **LaTeX Files** (`*.tex`)
   - Must have compliance score ≥ 85%
   - Enforces: CHAPTER STRUCTURE + APPENDIX TEMPLATE requirements
   - Scripts: `scripts/check_chapter_compliance.py`, `scripts/check_template_compliance.py`

2. **Python Scripts** (`scripts/*.py`)
   - Must have SCRIPT_METADATA block
   - Must reference SOP in docstring
   - Must include error handling
   - Enforces: SOP-SCRIPT-01 compliance

3. **Appendix Codes** (all `.tex` files)
   - Must not have code conflicts
   - Must be in APPENDIX_CODE_REGISTRY.yaml
   - Enforces: SOP-APPEND-02 compliance

4. **Index Consistency**
   - All 4 critical locations must be synchronized:
     1. Summary table
     2. Category counts
     3. Status table
     4. Reading paths
   - Enforces: SOP-INDEX-03 compliance

**Installation:**
```bash
# Git automatically runs hooks from .claude/hooks/ (if properly configured)
# Or manually install:
mkdir -p .git/hooks
cp .claude/hooks/pre-commit.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

**Bypass (Not Recommended):**
```bash
git commit --no-verify    # Skip hook (violates SOP enforcement)
```

---

## Integration Point #3: Cron Jobs (LEVEL 3 - ENFORCED AUTOMATICALLY)

### Locations: `docs/operations/CRON-JOBS-SETUP.sh` and individual scripts

**Automated Enforcement Schedule:**

```
HOURLY (0 * * * *)
  └─→ scripts/run_monitoring.py
      ├─ Collect metrics (operational, integrity, resources)
      ├─ Check thresholds (read from SOP_ENFORCEMENT.yaml)
      ├─ Generate alerts (CRITICAL/HIGH/MEDIUM)
      └─ Log to audit trail (SOP-AUDIT-05)

DAILY 2 AM (0 2 * * *)
  └─→ scripts/run_daily_backup.py
      ├─ Create TIER 2 scope backup
      ├─ Cleanup old TIER 1 backups
      └─ Log to audit trail (SOP-AUDIT-05)

WEEKLY (0 4 * * 6)
  └─→ Backup verification
      ├─ Verify all backups readable
      ├─ Check retention policies
      └─ Generate report (SOP-RECOVER-04)

MONTHLY (0 5 1 * *)
  └─→ scripts/validate_tier4.py
      ├─ Run all 47+ validation rules
      ├─ Check index integrity (4-location sync)
      ├─ Scan for code conflicts
      ├─ Generate compliance report
      └─ Alert on violations
```

**Installation:**
```bash
bash docs/operations/CRON-JOBS-SETUP.sh
# Then: crontab -e
# Paste the contents of /tmp/ebf-cron-jobs.txt
```

**What gets enforced:**

| Cron Job | Enforces | Frequency | Blocks Operations? |
|----------|----------|-----------|-------------------|
| run_monitoring.py | SOP-MONITOR-08 | Hourly | NO (warning only) |
| run_daily_backup.py | SOP-RECOVERY-04 | Daily | NO (automated) |
| Backup verification | SOP-RECOVERY-04 | Weekly | NO (report only) |
| validate_tier4.py | All 47+ rules | Monthly | NO (report only) |

---

## Integration Point #4: Script Templates (LEVEL 2 - ENFORCED IN EVERY SCRIPT)

### Location: `scripts/SCRIPT_TEMPLATE.py`

Every script must use this template. It enforces SOPs automatically:

**Structure enforced by template:**

```python
#!/usr/bin/env python3
"""
[1] SOP Reference in docstring (MANDATORY)
    - Which SOP(s) does this implement?
"""

# [2] SCRIPT_METADATA - Mandatory by SOP-SCRIPT-01
SCRIPT_METADATA = {
    "name": "...",           # Identifier
    "version": "1.0.0",      # Semantic versioning
    "purpose": "...",        # One sentence
    "phase": "IMPLEMENT",    # DESIGN/IMPLEMENT/VALIDATE/EXECUTE
    "sop": "SOP-SCRIPT-01",  # Which SOP enforces this?
    "preconditions": [...],  # What must be true before running?
    "postconditions": [...], # What must be true after?
    "files_modified": [...], # What does this change?
    "files_read": [...],     # What does this read?
    "dependencies": [...],   # What scripts must run first?
    "requires_backup": True  # SOP-RECOVERY-04
}

def main(dry_run=False):
    # [3] Setup phase - enforced by SOP-SCRIPT-01, PHASE 1
    logger = setup_logging()
    audit_logger = AuditLogger()      # SOP-AUDIT-05
    backup_manager = BackupManager()  # SOP-RECOVERY-04

    # [4] Precondition checking - SOP-SCRIPT-01, PHASE 2
    success, error = check_preconditions(logger)
    if not success:
        audit_logger.log_event(...)   # Log failure
        return 1

    # [5] Backup creation - SOP-RECOVERY-04, MANDATORY
    if SCRIPT_METADATA["requires_backup"]:
        backups = create_backups(backup_manager, logger)
        if not backups["success"]:
            return 1

    # [6] Main execution - Your logic here
    # (with error handling)

    # [7] Postcondition verification - SOP-SCRIPT-01, PHASE 4
    success, error = verify_postconditions(logger)
    if not success:
        return 1

    # [8] Audit logging - SOP-AUDIT-05, MANDATORY
    audit_logger.log_event(
        category="SCRIPT",
        operation="EXECUTE",
        target={...},
        execution={...}
    )

    return 0
```

**How to create a new script:**

```bash
# 1. Copy template
cp scripts/SCRIPT_TEMPLATE.py scripts/my_script.py

# 2. Fill in SCRIPT_METADATA
# 3. Implement check_preconditions()
# 4. Implement main() logic
# 5. Implement verify_postconditions()
# 6. Test with --dry-run
python3 scripts/my_script.py --dry-run

# 7. Test normally
python3 scripts/my_script.py

# 8. Git will validate via pre-commit.sh before allowing commit
git add scripts/my_script.py
git commit -m "feat(script): Add my_script"
```

**What the template enforces:**

- ✅ SCRIPT_METADATA presence (SOP-SCRIPT-01)
- ✅ Error handling (try/except)
- ✅ Precondition checking (SOP-SCRIPT-01)
- ✅ Backup creation before modifications (SOP-RECOVERY-04)
- ✅ Audit logging of all operations (SOP-AUDIT-05)
- ✅ Postcondition verification (SOP-SCRIPT-01)
- ✅ Dry-run capability (--dry-run flag)
- ✅ Proper exit codes (0=success, 1=failure)

---

## Integration Point #5: Documentation (LEVEL 1 - REFERENCE & GUIDANCE)

### Locations: `CLAUDE.md`, SOPs, this guide

**CLAUDE.md Integration:**

The main project file should reference ALL enforcement points:

```markdown
## Where SOPs are Enforced (ALWAYS)

SOPs are not just documentation - they are **ENFORCED** at these 5 critical points:

### 1. Configuration: `data/config/SOP_ENFORCEMENT.yaml`
   - Single source of truth for all SOP rules
   - Specifies enforcement levels (STRICT/WARNING/INFO)
   - Used by all enforcement points below

### 2. Git Hooks: `.claude/hooks/pre-commit.sh`
   - Runs before every commit
   - Validates LaTeX compliance ≥85%
   - Checks code conflicts
   - Verifies index sync (4 locations)
   - BLOCKS commits that violate SOPs

### 3. Cron Jobs: Automated hourly/daily/weekly/monthly
   - `run_monitoring.py` - Hourly metrics + alerts
   - `run_daily_backup.py` - Daily scope backups
   - `validate_tier4.py` - Monthly comprehensive check
   - Enforces SOP compliance continuously

### 4. Script Templates: `scripts/SCRIPT_TEMPLATE.py`
   - Every script must inherit from this
   - Enforces SOP-SCRIPT-01 (4-phase lifecycle)
   - Enforces backup/logging/error-handling
   - CANNOT create non-compliant scripts

### 5. Documentation: This guide + INTEGRATION-GUIDE.md
   - Explains WHAT each SOP requires
   - Shows WHEN each SOP is enforced
   - References WHERE to find rules

## Quick Decision Tree

**"Do I need to check the SOPs?"**

→ Creating a new script?
  ✓ Use SCRIPT_TEMPLATE.py (enforces SOP-SCRIPT-01)

→ Adding an appendix?
  ✓ pre-commit.sh will validate (enforces SOP-APPEND-02, SOP-INDEX-03)

→ Modifying appendix index?
  ✓ pre-commit.sh will check 4-location sync (enforces SOP-INDEX-03)

→ Making a LaTeX file?
  ✓ pre-commit.sh will score compliance (enforces template requirement)

→ Running a script manually?
  ✓ Script will enforce preconditions + backup + logging (enforces SOP-SCRIPT-01/04/05)

→ Worried about missing something?
  ✓ Monthly cron job validates everything (enforces all SOPs)
```

---

## The Enforcement Workflow (How It Works)

### Scenario 1: Creating a New Script

```
1. Developer: cp scripts/SCRIPT_TEMPLATE.py scripts/new_feature.py
   ↓
2. Developer: Fills in SCRIPT_METADATA (preconditions, postconditions, etc.)
   ↓
3. Developer: python3 scripts/new_feature.py --show-checks
   ↓
4. Developer: python3 scripts/new_feature.py --dry-run
   ✓ Script enforces: precondition checking, error handling, logging
   ↓
5. Developer: python3 scripts/new_feature.py
   ✓ Script enforces: backup creation, audit logging, postcondition check
   ↓
6. Developer: git add scripts/new_feature.py
   git commit -m "feat: Add new feature"
   ↓
7. Git Hook (pre-commit.sh):
   - Read SOP_ENFORCEMENT.yaml
   - Check SCRIPT_METADATA present ✓
   - Check error handling ✓
   - Check SOP reference ✓
   ✓ COMMIT ALLOWED
   ↓
8. Every hour (cron):
   - run_monitoring.py executes (including this script if needed)
   - Metrics collected
   - Audit trail updated
   ↓
9. Monthly (cron):
   - validate_tier4.py runs
   - Checks all 47+ rules
   - Reports compliance ✓
```

### Scenario 2: Modifying Appendix Index

```
1. Developer: Edits appendices/00_appendix_index.tex (Location 1)
   ↓
2. Developer: git add appendices/00_appendix_index.tex
   git commit -m "docs: Add new appendix code"
   ↓
3. Git Hook (pre-commit.sh):
   - Check code conflicts? SOP_ENFORCEMENT.yaml says STRICT
   - Check APPENDIX_CODE_REGISTRY.yaml
   - Code "AB" already exists? ✗ BLOCK
   ↓
4. Developer: Uses SOP-APPEND-02 to resolve
   - Checks available codes: "CA-DZ" range
   - Updates APPENDIX_CODE_REGISTRY.yaml
   - Updates all 4 index locations (SOP-INDEX-03)
   ↓
5. Developer: git add appendices/00_appendix_index.tex docs/operations/APPENDIX_CODE_REGISTRY.yaml
   git commit -m "docs(Appendix): Add new code with full sync"
   ↓
6. Git Hook (pre-commit.sh):
   - Check Location 1: ✓ New code present
   - Check Location 2: ✓ Category count updated
   - Check Location 3: ✓ Status table updated
   - Check Location 4: ✓ Reading paths updated
   - Check registry: ✓ Code marked ACTIVE
   ✓ COMMIT ALLOWED
```

### Scenario 3: Automated Enforcement (Cron)

```
Every Hour at :00:
  ↓
  run_monitoring.py
  ├─ Read SOP_ENFORCEMENT.yaml
  ├─ Read alert thresholds:
  │   - Index consistency < 100? CRITICAL
  │   - Code conflicts > 0? CRITICAL
  │   - Audit log > 1GB? HIGH
  ├─ Collect metrics:
  │   - Index consistency: Check all 4 locations
  │   - Code conflicts: Scan APPENDIX_CODE_REGISTRY
  │   - Audit log size: Check data/audit/ directory
  ├─ If threshold breached → Generate ALERT
  └─ Log to data/monitoring/alerts.log + audit trail

Daily 2 AM:
  ↓
  run_daily_backup.py
  ├─ Read SOP_ENFORCEMENT.yaml for backup config
  ├─ Create TIER 2 backup (appendices + chapters + data)
  ├─ Cleanup old TIER 1 backups (7-day retention)
  └─ Log to audit trail

Monthly on 1st at 5 AM:
  ↓
  validate_tier4.py
  ├─ Read SOP_ENFORCEMENT.yaml (all 47+ rules)
  ├─ Validate:
  │   ├─ Index integrity (4-location sync)
  │   ├─ Code conflicts (uniqueness)
  │   ├─ Orphaned entries (bidirectional consistency)
  │   ├─ LaTeX compliance (all ≥85%?)
  │   ├─ Script METADATA (all present?)
  │   └─ ... and 41+ more rules
  ├─ Generate compliance report
  ├─ Alert on violations
  └─ Log to audit trail
```

---

## Quick Reference: What's Enforced Where?

| SOP | Enforced By | When | Severity |
|-----|-------------|------|----------|
| **SOP-SCRIPT-01** (Script Management) | SCRIPT_TEMPLATE.py + pre-commit.sh | At creation, at commit, at execution | STRICT |
| **SOP-APPEND-02** (Code Management) | pre-commit.sh + run_monitoring.py | At commit, hourly check | STRICT |
| **SOP-INDEX-03** (Index Integrity) | pre-commit.sh + run_monitoring.py | At commit, daily check | STRICT |
| **SOP-RECOVERY-04** (Backup System) | SCRIPT_TEMPLATE.py + run_daily_backup.py | Before every modification, daily | STRICT |
| **SOP-AUDIT-05** (Audit Logging) | SCRIPT_TEMPLATE.py + audit_logger.py | Every operation | STRICT |
| **SOP-DEPEND-06** (Dependency Management) | dependency_graph.py | Before execution order determined | WARNING |
| **SOP-VALID-07** (Validation) | pre-commit.sh + validate_tier4.py | At commit, monthly | STRICT |
| **SOP-MONITOR-08** (Monitoring) | run_monitoring.py | Hourly + alerts | WARNING |

---

## Summary: How to Ensure SOPs Are "ALWAYS!!!" Followed

**The 5 Integration Points (in order of enforcement strength):**

1. **Configuration** (SOP_ENFORCEMENT.yaml)
   - Single source of truth
   - All other systems read from this

2. **Git Hooks** (pre-commit.sh)
   - Validates BEFORE commit is allowed
   - Cannot commit non-compliant code

3. **Script Templates** (SCRIPT_TEMPLATE.py)
   - Every script inherits enforcement
   - Preconditions + backup + logging automatic

4. **Cron Jobs** (Automated hourly/daily/monthly)
   - Continuous enforcement even when developers sleep
   - Catches issues immediately

5. **Documentation** (This guide + SOPs)
   - Explains WHY and WHEN
   - Reference for understanding enforcement

**To make SOPs "always!!!" followed:**

- ✅ Use pre-commit hook → blocks non-compliant commits
- ✅ Use SCRIPT_TEMPLATE → every new script is compliant
- ✅ Setup cron jobs → automated continuous enforcement
- ✅ Update SOP_ENFORCEMENT.yaml → change enforcement globally
- ✅ Reference in CLAUDE.md → makes enforcement visible

**Maintenance:**
- When SOP rules change → update SOP_ENFORCEMENT.yaml first
- When adding new scripts → must use SCRIPT_TEMPLATE.py
- When adding new processes → integrate into cron schedule
- When enforcement isn't working → check SOP_ENFORCEMENT.yaml

---

## Next Steps

1. ✅ Configuration created: `data/config/SOP_ENFORCEMENT.yaml`
2. ✅ Template created: `scripts/SCRIPT_TEMPLATE.py`
3. ✅ This guide created: `SOP-ENFORCEMENT-INTEGRATION.md`
4. ⏳ Update CLAUDE.md to reference these 5 enforcement points
5. ⏳ Setup git hooks: `.git/hooks/pre-commit` (copy from `.claude/hooks/`)
6. ⏳ Setup cron jobs: `bash docs/operations/CRON-JOBS-SETUP.sh`
7. ⏳ Test enforcement: Create test script using SCRIPT_TEMPLATE.py

---

**Version**: 1.0.0
**Last Updated**: 2026-01-15
**Author**: Claude Code
**Status**: ACTIVE
**Enforcement Level**: STRICT (all 5 integration points)
