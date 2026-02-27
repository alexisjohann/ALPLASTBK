# Operations & Infrastructure Handbook

> **Layer 2: Operational SOPs for EBF Script & Appendix Management**
>
> Version: 1.0 | Date: 2026-01-15 | Protocol: OPS-L2-001

---

## Purpose

This directory contains **Standard Operating Procedures (SOPs)** for managing scripts, appendices, and infrastructure in the complementarity-context-framework repository.

**Why Layer 2 exists:**
The EBF repository contains 75+ executable Python scripts, 400+ LaTeX appendices, and 19 chapters. Without operational discipline, these components become:
- Inconsistent (scripts with different error handling patterns)
- Undocumented (no audit trails, no dry-run validation)
- Fragile (index out of sync, orphaned files, code conflicts)
- Unrecoverable (no backup procedures, no rollback capability)

**Layer 2 Solution:** 4 foundational SOPs that enforce operational discipline across the entire repository.

---

## The 4 Operations SOPs

### 1️⃣ SOP-SCRIPT-01: General Script Management & Execution Protocol

**When to use:** Before executing, modifying, or creating ANY Python script in `/scripts/` directory.

**Key concepts:**
- **4-Phase Lifecycle**: Design → Development → Validation → Execution
- **Precondition Checking**: Every script verifies assumptions BEFORE running
- **Dry-Run Mode**: All transformations support `--dry-run` flag to preview changes
- **PostCondition Validation**: After execution, verify output meets expected criteria
- **Audit Logging**: Every run is logged with timestamp, parameters, results, and any errors

**File reference:** `SOP-SCRIPT-01-Script-Management.md` (8,000+ lines, 25 checklists)

**Core code pattern** all scripts must follow:
```python
#!/usr/bin/env python3
"""
Script Purpose: [Exact description]
Inputs: [Data structures]
Outputs: [Generated artifacts]
Preconditions: [What must be true before running]
PostConditions: [What is guaranteed after running]
"""

def check_preconditions():
    """Verify all assumptions are met. Raise exception if not."""

def execute_transformation(data, dry_run=False):
    """Core business logic. Support --dry-run to preview without changes."""

def validate_output(output):
    """Verify output meets expected criteria. Return bool."""

def save_output(output, filepath, backup_existing=True):
    """Write output with safety checks and optional backup."""

if __name__ == "__main__":
    try:
        check_preconditions()
        output = execute_transformation(data, dry_run=args.dry_run)
        if validate_output(output):
            save_output(output, filepath)
            log_success(output)
    except Exception as e:
        log_error(e)
        raise
```

**Most common use:** When you have a script that modifies files (e.g., `register_lit_appendices.py`), verify it follows the 4-phase lifecycle and includes dry-run capability.

---

### 2️⃣ SOP-APPEND-02: Appendix Code & Naming Management

**When to use:** Before assigning a code to a NEW appendix or registering appendix changes.

**Key concepts:**
- **Code Availability Crisis**: Single-letter codes (A-Z) are EXHAUSTED. Only Y, Z remain free.
- **Solution**: Use two-letter codes (BF-BZ range provides 22 new slots; CA-DZ provides 78 more)
- **5-Point Checklist BEFORE assigning code**:
  1. Search for code conflicts (python utility provided)
  2. Verify code isn't in APPENDIX_CODE_REGISTRY.yaml
  3. Check category constraints (CORE codes differ from DOMAIN codes)
  4. Plan filename: `[CODE]_[CATEGORY]-[NAME].tex`
  5. Create RESERVED entry in registry (prevents others from using same code)
- **3-Phase Lifecycle**: RESERVED (code protected) → DRAFT (file exists, not complete) → ACTIVE (published)

**File reference:** `SOP-APPEND-02-Appendix-Naming.md` (6,500+ lines)

**Critical validation function** (always use this):
```python
def validate_codes_before_registration(new_appendices):
    """MANDATORY: Check for conflicts BEFORE modifying index"""
    registry = load_appendix_code_registry()
    used_codes = set(registry['assigned_codes'].keys())
    requested = set([app['code'] for app in new_appendices])
    conflicts = requested & used_codes
    if conflicts:
        raise ValueError(f"CODE CONFLICTS: {conflicts}")
```

**Root cause it prevents:** The bug that created 25 code conflicts (codes R, S, T, W, X assigned twice simultaneously).

**Most common use:** When creating a new appendix or integrating appendix changes from elsewhere.

---

### 3️⃣ SOP-INDEX-03: Appendix Index Integrity & Validation

**When to use:** Whenever appendices are added/removed or when index consistency is questioned.

**Key concepts:**
- **The 4 Critical Locations** in `appendices/00_appendix_index.tex` that MUST stay synchronized:
  1. **Location 1** (line ~430): Appendix Summary Table (code, category, title, lines)
  2. **Location 2** (line ~68): Category Counts (CORE: 9, FORMAL: 11, DOMAIN: 17, etc.)
  3. **Location 3** (line ~612): Status & Progress Table (completion %, DRAFT/ACTIVE/DEPRECATED)
  4. **Location 4** (line ~898): Reading Paths Table (cross-references to chapters)
- **The Bug**: `register_lit_appendices.py` updated Locations 1, 2, 3 but FORGOT Location 4 → orphaned reading paths
- **The Solution**: Use `AppendixIndexManager` class that validates all 4 locations BEFORE and AFTER modifications

**File reference:** `SOP-INDEX-03-Index-Integrity.md` (5,500+ lines)

**Core class** (use for all index modifications):
```python
class AppendixIndexManager:
    def add_appendix(self, code, category, title, lines, chapter_refs):
        """Add appendix to ALL 4 index locations. Raises exception if any fail."""
        self._update_location_1_summary(code, category, title, lines)
        self._update_location_2_counts(category)
        self._update_location_3_status(code, 'DRAFT')
        self._update_location_4_reading_paths(code, chapter_refs)
        self._validate_all_locations()  # Sanity check
        return True
```

**Quarterly Audit Protocol:**
- Count files vs index entries
- Detect orphaned files (in filesystem but not in index)
- Detect ghost entries (in index but no physical file)
- Verify cross-references are bidirectional

**Most common use:** After running a script that modifies appendices, verify index consistency.

---

### 4️⃣ SOP-RECOVERY-04: Backup, Recovery & Rollback Protocol

**When to use:** Before executing ANY script that modifies files, and after failures occur.

**Key concepts:**
- **3-Tier Backup System**:
  - **TIER 1 (Operation-Level)**: Automatic backup before each script execution, retention 7 days
  - **TIER 2 (Daily Checkpoint)**: Automated snapshot every 24h at 00:00 UTC, retention 30 days
  - **TIER 3 (Archive)**: Weekly (Friday) + Monthly (1st of month), retention 4 weeks + 3 months
- **Backup Naming Convention**: `FILENAME.BACKUP.2026-01-15T14:32:45.123456.EXT`
- **4 Recovery Scenarios**:
  1. Single file corruption → restore from BACKUP (TIER 1)
  2. Multiple file partial failure → restore from pre-execution backups
  3. Widespread corruption → restore from daily checkpoint (TIER 2)
  4. Total disaster → restore from monthly archive (TIER 3) or git bundle

**File reference:** `SOP-RECOVERY-04-Backup-Recovery.md` (5,000+ lines)

**Core backup class** (automatically used by all scripts):
```python
class BackupManager:
    def create_backup(self, filepath):
        """Backup single file: FILENAME.BACKUP.TIMESTAMP.EXT"""

    def create_scope_backup(self, scope='appendices,chapters,data'):
        """Backup entire scope as tar.gz with timestamp"""

    def cleanup_old_backups(self, max_age_days=7):
        """Auto-delete backups older than threshold"""

    def restore(self, original_filepath, backup_timestamp=None):
        """Restore specific version or latest backup"""
```

**Disaster Recovery Checklist:**
- [ ] Incident classification (severity level 1-4)
- [ ] Backup selection (TIER 1, 2, or 3)
- [ ] Extraction testing (verify backup is readable before restoring)
- [ ] Selective restoration (restore only affected files)
- [ ] Post-recovery validation (verify restored files are intact)
- [ ] Incident log (document what happened, how it was fixed, prevention)

**Most common use:** Automatic (scripts create backups before modifications). Manual: if something goes wrong, follow the 4 recovery scenarios.

---

## Quick Decision Tree

```
I need to...

├─ Create/modify a Python script
│  └─ Read: SOP-SCRIPT-01
│     → Use 4-phase lifecycle (Design → Dev → Validate → Execute)
│     → Include preconditions, postconditions, dry-run mode
│     → Create audit log

├─ Add a new appendix
│  └─ Read: SOP-APPEND-02
│     → Check code availability (5-point checklist)
│     → Update APPENDIX_CODE_REGISTRY.yaml
│     → Use BF-BZ or CA-DZ range (not exhausted A-Z)

├─ Register appendix changes in index
│  └─ Read: SOP-INDEX-03
│     → Use AppendixIndexManager class
│     → Update ALL 4 critical locations
│     → Run quarterly audit protocol

├─ Back up files or recover from failure
│  └─ Read: SOP-RECOVERY-04
│     → TIER 1: Last 7 days of operation backups
│     → TIER 2: Last 30 days of daily snapshots
│     → TIER 3: Archives (4 weeks + 3 months)

└─ I'm not sure which SOP applies
   └─ Most likely: SOP-SCRIPT-01 (covers 80% of operations)
```

---

## Registry Files

Two central registries document ALL operations:

### 1. SCRIPT_REGISTRY.yaml
**Purpose:** Inventory of all 75+ executable scripts

**Location:** `/docs/operations/SCRIPT_REGISTRY.yaml`

**Schema:**
```yaml
scripts:
  - name: "register_lit_appendices.py"
    category: "Appendix Management"
    description: "Register literature-based appendices with validation"
    sop_reference: "SOP-SCRIPT-01, SOP-APPEND-02, SOP-INDEX-03"
    preconditions:
      - "Appendix files exist in appendices/"
      - "APPENDIX_CODE_REGISTRY.yaml loaded"
    postconditions:
      - "All 4 index locations synchronized"
      - "Backup created"
    affected_systems:
      - "appendices/00_appendix_index.tex"
      - "APPENDIX_CODE_REGISTRY.yaml"
    status: "DEPRECATED (v1.0 had bugs)"
    version: "1.0"
    last_run: "2026-01-13T14:32:00"
    next_scheduled: null
```

**Status values:** ACTIVE, DEPRECATED, MAINTENANCE, ARCHIVED

**When to use:**
- Before executing any script, check SCRIPT_REGISTRY to understand its purpose and preconditions
- After creating new script, register it immediately (prevents duplicate script creation)
- To audit which scripts touch which files

---

### 2. APPENDIX_CODE_REGISTRY.yaml
**Purpose:** Master list of all 400+ possible appendix codes and their status

**Location:** `/docs/operations/APPENDIX_CODE_REGISTRY.yaml`

**Schema:**
```yaml
metadata:
  version: "1.0"
  last_updated: "2026-01-15T21:56:00"
  total_codes: 702  # 26 (A-Z) + 26×26 (AA-ZZ) - already assigned

code_registry:
  A:
    status: "ACTIVE"
    category: "FORMAL"
    title: "Formal Foundations: Axioms"
    assigned_date: "2025-10-15"
    appendix_file: "A_FORMAL-Axioms.tex"

  R:
    status: "CONFLICT"
    conflict_with: ["METHOD-EVAL", "PREDICT-MASTER"]
    notes: "Bug from register_lit_appendices v1.0 - see SOP-APPEND-02"

  BF:
    status: "AVAILABLE"
    recommended_for: "DOMAIN category (suggested)"
    next_available: true

assignment_rules:
  single_letter_available: ["Y", "Z"]  # Only 2 left!
  two_letter_ranges:
    BF-BZ: 22 slots (11/22 remaining)
    CA-CZ: 26 slots (all available)
    DA-DZ: 26 slots (all available)
    EA-EZ: 26 slots (all available)
```

**Status values:**
- `ACTIVE`: Assigned to published appendix
- `DRAFT`: Assigned but appendix not yet complete
- `RESERVED`: Code protected for upcoming appendix (prevents conflicts)
- `CONFLICT`: Code assigned 2+ times (bug!)
- `ORPHAN`: In index but no physical file
- `AVAILABLE`: Free for assignment

**When to use:**
- BEFORE assigning code to new appendix (mandatory 5-point checklist in SOP-APPEND-02)
- To find available codes (avoid single-letter A-Z; use BF-BZ or CA-DZ instead)
- To detect conflicts (SOP-APPEND-02 validation uses this)

---

## Implementation Roadmap

### ✅ Phase 1: Operations SOPs Created (2026-01-15)
- [x] SOP-SCRIPT-01: Script Management (8.0K lines, 25 checklists)
- [x] SOP-APPEND-02: Appendix Naming (6.5K lines, code validation)
- [x] SOP-INDEX-03: Index Integrity (5.5K lines, 4-location sync)
- [x] SOP-RECOVERY-04: Backup & Recovery (5.0K lines, 3-tier system)

### ⏳ Phase 2: Registry Files & Integration (2026-01-15 ongoing)
- [ ] Create SCRIPT_REGISTRY.yaml (inventory all 75+ scripts)
- [ ] Create APPENDIX_CODE_REGISTRY.yaml (status of all codes)
- [ ] Create INTEGRATION_GUIDE.md (link Layer 2 to CLAUDE.md)
- [ ] Update CLAUDE.md with SOP cross-references

### ⏳ Phase 3: Bug Fixes Using Layer 2
- [ ] Create register_lit_appendices_v2.py (fixes 25 code conflicts)
- [ ] Implement AppendixIndexManager class from SOP-INDEX-03
- [ ] Execute with BackupManager from SOP-RECOVERY-04
- [ ] Run quarterly audit to validate fix

### ⏳ Phase 4: Layer 3 Infrastructure
- [ ] Audit Logging System (git-integrated, immutable)
- [ ] Dependency Management (track script dependencies)
- [ ] Automated Validation Framework
- [ ] Monitoring & Alerting

---

## Using Layer 2 in Practice

### Example 1: I need to create a new script

**Step 1:** Read SOP-SCRIPT-01, Section 3 (Design Phase)
```
→ Create Specification Document
→ Define Inputs, Outputs, Preconditions, PostConditions
→ Choose dry-run mode capability
→ Plan backup and rollback strategy
```

**Step 2:** Implement using 4-phase code pattern
```python
#!/usr/bin/env python3
"""
Purpose: [Your purpose]
Inputs: [Your inputs]
Outputs: [Your outputs]
Preconditions: [Your preconditions]
PostConditions: [Your postconditions]
"""

def check_preconditions():
    """Verify all assumptions"""
    # Your validation code

def execute_transformation(data, dry_run=False):
    """Business logic with dry-run support"""
    # Your logic here

def validate_output(output):
    """Verify output quality"""
    # Your validation

def save_output(output, filepath):
    """Save with backup"""
    # Your save logic

if __name__ == "__main__":
    # Follow 4-phase execution
```

**Step 3:** Register in SCRIPT_REGISTRY.yaml
```yaml
- name: "my_new_script.py"
  category: "Your Category"
  status: "ACTIVE"
  sop_reference: "SOP-SCRIPT-01"
```

**Step 4:** Run with SOP-SCRIPT-01 validation checklist

---

### Example 2: I discovered an appendix code conflict

**Step 1:** Read SOP-APPEND-02, Section 5 (Conflict Resolution)

**Step 2:** Check APPENDIX_CODE_REGISTRY.yaml status
```
→ Find conflicting code (e.g., "R")
→ Identify which appendices incorrectly use "R"
→ Choose replacement codes from BF-BZ range
```

**Step 3:** Create backup per SOP-RECOVERY-04
```bash
BackupManager.create_scope_backup('appendices')
```

**Step 4:** Update appendix files and index using SOP-INDEX-03
```python
AppendixIndexManager.rename_code('R', 'BF')  # Update all 4 locations
```

**Step 5:** Run SOP-INDEX-03 quarterly audit to verify

---

### Example 3: A script failed mid-execution

**Step 1:** Read SOP-RECOVERY-04, Section 4 (Recovery Scenarios)

**Step 2:** Classify severity (Scenario 1-4)
```
→ Single file corruption? → Restore from BACKUP (TIER 1)
→ Multi-file partial failure? → Restore multiple from pre-execution
→ Widespread corruption? → Restore from checkpoint (TIER 2)
→ Total disaster? → Restore from archive (TIER 3)
```

**Step 3:** Follow recovery checklist
```
☐ Incident classification
☐ Backup selection
☐ Extraction testing (verify backup works!)
☐ Selective restoration
☐ Post-recovery validation
☐ Incident log (prevent recurrence)
```

**Step 4:** Improve script per SOP-SCRIPT-01
```
→ Was precondition validation missing?
→ Was dry-run mode available?
→ Was backup created automatically?
→ Update script to prevent recurrence
```

---

## FAQ

**Q: Which SOP should I read first?**
A: SOP-SCRIPT-01 (covers 80% of operations). Others are specialty SOPs.

**Q: Can I skip the dry-run phase?**
A: No. Every script that modifies files must support `--dry-run`. See SOP-SCRIPT-01 Section 3 for template.

**Q: What if a script doesn't match the 4-phase pattern?**
A: It's non-compliant. See SOP-SCRIPT-01 compliance checklist. All scripts must follow the pattern.

**Q: How do I find an available appendix code?**
A: Check APPENDIX_CODE_REGISTRY.yaml for status='AVAILABLE'. Use BF-BZ or CA-DZ (two-letter) codes; single-letter is exhausted.

**Q: What if backup restoration fails?**
A: See SOP-RECOVERY-04, Section 5 (Advanced Recovery). Follow DRP Coordinator Checklist.

**Q: I found a bug in one of the SOPs. What do I do?**
A: This is expected! SOPs are v1.0 and will evolve. Document in `/quality/lessons_learned.md` with recommended fix.

---

## Related Documentation

**User-Facing Documentation (Layer 1):**
- `/CLAUDE.md` - Main project instructions (references Layer 2)
- `/docs/frameworks/appendix-category-definitions.md` - Appendix categories

**Operations Handbook (Layer 2 - You Are Here):**
- `SOP-SCRIPT-01-Script-Management.md` - Script lifecycle
- `SOP-APPEND-02-Appendix-Naming.md` - Code assignment
- `SOP-INDEX-03-Index-Integrity.md` - Index synchronization
- `SOP-RECOVERY-04-Backup-Recovery.md` - Disaster recovery

**Infrastructure Layer (Layer 3 - Coming Soon):**
- Audit Logging System
- Dependency Management
- Validation Framework
- Monitoring & Alerting

---

## Contact & Support

**Questions about Layer 2?**
- SOP-SCRIPT-01 issues → See scripting compliance checklist
- Code conflicts → See SOP-APPEND-02 5-point validation
- Index out of sync → See SOP-INDEX-03 4-location sync protocol
- Recovery needed → See SOP-RECOVERY-04 4 scenarios

**Reporting bugs:**
1. Document in `/quality/lessons_learned.md`
2. Reference the affected SOP
3. Include steps to reproduce
4. Suggest improvement

---

*Layer 2 Handbook v1.0 | 2026-01-15 | Protocol: OPS-L2-001*
