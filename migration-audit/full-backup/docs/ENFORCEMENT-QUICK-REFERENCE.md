# SOP Enforcement: Quick Reference Card

**Print this page and post it at your desk!**

---

## The 5 Enforcement Points (ALWAYS!!!)

```
╔════════════════════════════════════════════════════════════════╗
║                    SOP ENFORCEMENT PYRAMID                     ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  📄 Level 5: DOCUMENTATION (Guidelines & Reference)           ║
║     ├─ CLAUDE.md (enforcement overview)                       ║
║     ├─ SOP-ENFORCEMENT-INTEGRATION.md (this guide)            ║
║     └─ Individual SOP documents (SOP-SCRIPT-01, etc.)         ║
║                                                                ║
║  🔧 Level 4: SCRIPT TEMPLATES (Code-Level Enforcement)        ║
║     └─ scripts/SCRIPT_TEMPLATE.py ← COPY THIS FOR NEW SCRIPTS  ║
║        Enforces: Preconditions, backup, logging, error-handle ║
║                                                                ║
║  ⏰ Level 3: CRON JOBS (Automated Hourly/Daily/Monthly)        ║
║     ├─ Hourly: run_monitoring.py (metrics + alerts)           ║
║     ├─ Daily 2AM: run_daily_backup.py (TIER 2 snapshots)     ║
║     └─ Monthly: validate_tier4.py (all 47+ rules)             ║
║                                                                ║
║  🚫 Level 2: GIT HOOKS (Prevents Non-Compliant Commits)       ║
║     └─ .claude/hooks/pre-commit.sh                            ║
║        Blocks: Low compliance, code conflicts, index out-sync  ║
║                                                                ║
║  ⚙️  Level 1: CONFIGURATION (Single Source of Truth)           ║
║     └─ data/config/SOP_ENFORCEMENT.yaml                       ║
║        Defines: All enforcement rules & thresholds             ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

---

## When You Create Something...

### 🔨 Creating a New Script?

```
STEP 1: Copy the template
$ cp scripts/SCRIPT_TEMPLATE.py scripts/my_script.py

STEP 2: Fill in SCRIPT_METADATA
✓ name, version, purpose, phase, sop
✓ preconditions, postconditions
✓ files_modified, files_read
✓ dependencies, requires_backup

STEP 3: Implement your logic
✓ Fill in check_preconditions()
✓ Fill in main()
✓ Fill in verify_postconditions()

STEP 4: Test with --dry-run
$ python3 scripts/my_script.py --dry-run

STEP 5: Test normally
$ python3 scripts/my_script.py

STEP 6: Commit (pre-commit.sh will validate)
$ git add scripts/my_script.py
$ git commit -m "feat(script): Add my_script"
  ✓ pre-commit.sh checks:
    - SCRIPT_METADATA present?
    - Error handling?
    - SOP reference?
  ✓ If all pass → COMMIT ALLOWED

STEP 7: Cron will run it
→ Next hourly/daily/weekly trigger
→ Metrics collected
→ Audit trail recorded
```

**What's automatically enforced:**
- ✅ Precondition checking (SOP-SCRIPT-01)
- ✅ Backup creation (SOP-RECOVERY-04)
- ✅ Error handling
- ✅ Audit logging (SOP-AUDIT-05)
- ✅ Postcondition verification (SOP-SCRIPT-01)

---

### 📚 Adding a New Appendix?

```
STEP 1: Determine category
→ Use decision tree in CLAUDE.md
→ Pick from: CORE-, FORMAL-, DOMAIN-, CONTEXT-, METHOD-,
             PREDICT-, LIT-, REF-

STEP 2: Find available code
→ Check: docs/operations/APPENDIX_CODE_REGISTRY.yaml
→ Available ranges: CA-CZ, DA-DZ, etc.
→ Copy recommended code (e.g., "CA")

STEP 3: Copy appendix template
$ cp appendices/00_appendix_template.tex appendices/CA_your_title.tex

STEP 4: Commit (pre-commit.sh will validate)
$ git add appendices/CA_your_title.tex
$ git commit -m "docs(Appendix): Add CA CATEGORY-Title"
  ✓ pre-commit.sh checks:
    - Code not already used?
    - Appendix template ≥ 85% complete?
    - Category counts updated?
    - 4-location index sync?
  ✓ If all pass → COMMIT ALLOWED

STEP 5: Code automatically registered
→ Monthly cron job validates
→ Audit trail records creation
```

**What's automatically enforced:**
- ✅ Code conflict detection (SOP-APPEND-02)
- ✅ Template compliance ≥ 85% (SOP-VALID-07)
- ✅ Index sync across 4 locations (SOP-INDEX-03)

---

### 📝 Modifying Appendix Index?

```
⚠️  CRITICAL: Must update ALL 4 LOCATIONS atomically!

Location 1: Main summary table (~line 430)
  pattern: CODE & CATEGORY & TITLE & ...

Location 2: Category counts (~line 68)
  pattern: CATEGORY & ... & COUNT

Location 3: Status table (~line 612)
  pattern: CODE & CATEGORY & TITLE & DOMAIN & PRIORITY

Location 4: Reading paths (~line 898)
  pattern: CODE & CATEGORY & RELATED_CODE & CHAPTERS

STEP 1: Update all 4 locations in appendices/00_appendix_index.tex

STEP 2: Commit (pre-commit.sh will validate)
$ git add appendices/00_appendix_index.tex
$ git commit -m "docs(Index): Update 4-location sync for CODE"
  ✓ pre-commit.sh checks:
    - Location 1 updated?
    - Location 2 updated?
    - Location 3 updated?
    - Location 4 updated?
    - All consistent?
  ✓ If all 4 pass → COMMIT ALLOWED
  ✗ If any missing → COMMIT BLOCKED

⛔ CANNOT commit partial index update!
→ Must update all 4 locations or none
```

**What's automatically enforced:**
- ✅ Atomic 4-location sync (SOP-INDEX-03)
- ✅ Code conflict detection (SOP-APPEND-02)

---

## When Something Goes Wrong...

### 🔴 Pre-Commit Hook Blocked My Commit?

```
Error: ❌ FAILED: chapters/05.tex (Score: 72% < 85%)
       ⛔ Commit blocked: Some files have compliance < 85%

REASON: LaTeX file doesn't meet template requirements
SOLUTION:
  1. Read which elements are missing
  2. Add missing elements to file
  3. Test: python scripts/check_chapter_compliance.py chapters/05.tex
  4. Try commit again

Options:
  - FIX the file (recommended)
  - Use --no-verify to bypass (NOT recommended, violates SOPs)
    $ git commit --no-verify
```

### 🔴 Code Conflict Detected?

```
Error: ❌ FAILED: Code conflict detected: "AB" already assigned

REASON: Code "AB" is already used by another appendix
SOLUTION (per SOP-APPEND-02):
  1. Check docs/operations/APPENDIX_CODE_REGISTRY.yaml
  2. Pick another code from available range (CA-DZ recommended)
  3. Update your appendix filename: AB_... → CA_...
  4. Update appendix index with new code
  5. Try commit again

NEVER reuse codes, always pick from available range!
```

### 🔴 Index Out of Sync?

```
Error: ❌ FAILED: Index locations out of sync
       Location 1: Code "AB" present
       Location 2: Category count not updated
       Location 3: Code missing
       Location 4: Reading path missing

REASON: Updated only some of 4 index locations
SOLUTION (per SOP-INDEX-03):
  1. Update Location 1: Summary table
  2. Update Location 2: Category counts
  3. Update Location 3: Status table
  4. Update Location 4: Reading paths
  5. Ensure ALL consistent
  6. Try commit again

ALL 4 LOCATIONS must be updated together!
```

---

## SOP Quick Reference

### SOP-SCRIPT-01: Script Management
**When**: Creating new scripts
**Rule**: All scripts must have SCRIPT_METADATA + 4-phase lifecycle
**Enforced By**: SCRIPT_TEMPLATE.py + pre-commit.sh
**Severity**: STRICT (blocks non-compliant scripts)

### SOP-APPEND-02: Appendix Code Management
**When**: Adding/modifying appendices
**Rule**: No code conflicts, 5-point validation checklist
**Enforced By**: pre-commit.sh + run_monitoring.py (hourly)
**Severity**: STRICT (blocks conflicts immediately)

### SOP-INDEX-03: Index Integrity
**When**: Modifying appendix index
**Rule**: All 4 locations must sync atomically
**Enforced By**: pre-commit.sh + run_monitoring.py (daily)
**Severity**: STRICT (blocks partial updates)

### SOP-RECOVERY-04: Backup Management
**When**: Running any script that modifies files
**Rule**: Backup BEFORE modify, 3-tier retention
**Enforced By**: SCRIPT_TEMPLATE.py + run_daily_backup.py
**Severity**: STRICT (cannot modify without backup)

### SOP-AUDIT-05: Audit Logging
**When**: Every operation
**Rule**: Log with complete schema (WHO/WHAT/WHEN/WHERE/WHY/HOW)
**Enforced By**: audit_logger.py + all scripts
**Severity**: STRICT (every operation logged)

### SOP-DEPEND-06: Dependency Management
**When**: Running multiple scripts
**Rule**: Execute in dependency order (topological sort)
**Enforced By**: dependency_graph.py
**Severity**: WARNING (checked but allows override)

### SOP-VALID-07: Validation Framework
**When**: Committing + monthly validation
**Rule**: All 47+ validation rules must pass
**Enforced By**: pre-commit.sh + validate_tier4.py
**Severity**: STRICT (blocks non-compliant code)

### SOP-MONITOR-08: Monitoring & Alerting
**When**: Continuously (hourly + daily + monthly)
**Rule**: Check thresholds, generate alerts
**Enforced By**: run_monitoring.py (cron)
**Severity**: WARNING (alerts but allows operation)

---

## Enforcement Timeline

```
REAL-TIME (As you type)
  └─ Nothing yet (enforcement happens at commit)

AT COMMIT TIME (git commit)
  ├─ pre-commit.sh runs automatically
  ├─ Validates: LaTeX, Python, codes, index
  ├─ Blocks if compliance < 85% or conflicts found
  └─ [REQUIRED] You must fix before commit succeeds

HOURLY (every hour on the hour)
  ├─ run_monitoring.py executes via cron
  ├─ Collects metrics + checks thresholds
  ├─ Generates alerts if thresholds breached
  └─ Logs to data/monitoring/alerts.log

DAILY (2 AM UTC)
  ├─ run_daily_backup.py executes via cron
  ├─ Creates TIER 2 scope backup
  ├─ Cleans up old TIER 1 backups
  └─ Logs to audit trail

WEEKLY (Saturday 4 AM UTC)
  ├─ Backup verification runs
  ├─ Tests all backups readable
  └─ Generates report

MONTHLY (1st of month, 5 AM UTC)
  ├─ validate_tier4.py executes via cron
  ├─ Runs all 47+ validation rules
  ├─ Generates compliance report
  └─ Alerts on violations [IMMEDIATE if found]
```

---

## The Golden Rules

1. **Always use templates**
   - New scripts → copy SCRIPT_TEMPLATE.py
   - New appendices → copy 00_appendix_template.tex

2. **Pre-commit.sh is your friend**
   - It blocks bad code BEFORE it enters repo
   - Fix errors it reports (don't bypass with --no-verify)

3. **Never modify index partially**
   - Always update all 4 locations together
   - One location out-of-sync = broken

4. **Backup before you modify**
   - SCRIPT_TEMPLATE.py does this automatically
   - Never comment it out!

5. **Trust the cron jobs**
   - They run while you sleep
   - They catch issues automatically
   - They log everything for audit trails

6. **When in doubt, check SOP_ENFORCEMENT.yaml**
   - It's the single source of truth
   - All enforcement rules live there
   - If enforcement isn't working → check here

---

## Cheat Sheet Commands

```bash
# Create new script (enforced)
cp scripts/SCRIPT_TEMPLATE.py scripts/my_script.py
# ... edit SCRIPT_METADATA ...
python3 scripts/my_script.py --dry-run
python3 scripts/my_script.py

# Show what script does
python3 scripts/my_script.py --show-checks

# Check if you can commit (run this before git commit)
python3 scripts/check_chapter_compliance.py chapters/XX.tex
python3 scripts/check_template_compliance.py appendices/YY_title.tex

# View latest scripts
ls -ltr scripts/

# View code availability
grep "Code Availability" docs/operations/APPENDIX_CODE_REGISTRY.yaml

# View enforcement config
cat data/config/SOP_ENFORCEMENT.yaml | head -100

# View recent alerts
tail -20 data/monitoring/alerts.log

# View recent audit events
tail -20 data/audit/events.jsonl

# Check backup status
ls -lh data/backups/tier*/

# Test monitoring script manually
python3 scripts/run_monitoring.py

# Test validation manually
python3 scripts/validate_tier4.py
```

---

**Enforcement Pyramid Summary:**
- 🔴 **STRICT** enforcement on critical operations (pre-commit, templates)
- 🟡 **WARNING** on continuous monitoring (alerts but allows)
- 🟢 **INFO** on detailed metrics (logged but not blocking)

**Remember: The 5 integration points work TOGETHER to ensure SOPs are ALWAYS!!! followed.**

---

*Last Updated: 2026-01-15*
*Print & Post This Page*
