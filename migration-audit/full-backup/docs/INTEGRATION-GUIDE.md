# Layer 2 ↔ CLAUDE.md Integration Guide

> **How Operations SOPs Connect to Main Project Instructions**
>
> Version: 1.0 | Date: 2026-01-15 | Integration: L2 → Main

---

## Purpose

This guide shows WHERE in CLAUDE.md to reference Layer 2 Operations SOPs, and when users should switch from user-facing instructions to operational procedures.

**Key Insight:** CLAUDE.md is USER-CENTRIC (what to do), while Layer 2 SOPs are OPERATIONS-CENTRIC (how to do it reliably at scale).

---

## Architecture: Three Layers

```
┌─────────────────────────────────────────────────────────┐
│ LAYER 1: User Instructions                              │
│ File: CLAUDE.md                                         │
│ Purpose: What users can do (PFLICHT-Workflows)          │
│ Audience: Claude AI, Engineers, Researchers             │
└──────────────────┬──────────────────────────────────────┘
                   │ "See Layer 2 for operational details"
                   ↓
┌─────────────────────────────────────────────────────────┐
│ LAYER 2: Operations SOPs (You Are Here)                 │
│ Directory: /docs/operations/                            │
│ Purpose: HOW to do things reliably (SOP-SCRIPT-01, etc) │
│ Audience: CI/CD systems, operational staff              │
└──────────────────┬──────────────────────────────────────┘
                   │ "See Layer 3 for infrastructure"
                   ↓
┌─────────────────────────────────────────────────────────┐
│ LAYER 3: Infrastructure (Coming Q1 2026)                │
│ Directory: /docs/infrastructure/ (planned)              │
│ Purpose: Audit trails, dependency mgmt, monitoring      │
│ Audience: DevOps, System Administrators                 │
└─────────────────────────────────────────────────────────┘
```

---

## Cross-Reference Map: CLAUDE.md → Layer 2 SOPs

### Section: "PFLICHT-Workflows"

#### In CLAUDE.md:
```
### Neues Kapitel erstellen (PFLICHT-Workflow)
```

**Should reference:**
- SOP-SCRIPT-01: General Script Management (if using scripts for chapter generation)
- SOP-RECOVERY-04: Backup before modifying chapters

**New text to add:**
```
📋 For operational requirements on script execution, see:
   → /docs/operations/README.md (operations handbook overview)
   → /docs/operations/SOP-SCRIPT-01-Script-Management.md (script lifecycle)
```

---

#### In CLAUDE.md:
```
### Neuen Appendix erstellen (PFLICHT-Workflow)
```

**Should reference:**
- SOP-APPEND-02: Appendix Code & Naming Management (CRITICAL)
- SOP-INDEX-03: Appendix Index Integrity & Validation (CRITICAL)
- SOP-RECOVERY-04: Backup before modifications

**New text to add:**
```
⚠️ CRITICAL OPERATIONAL REQUIREMENTS:
   Before assigning ANY code to a new appendix:
   → Read: /docs/operations/SOP-APPEND-02-Appendix-Naming.md (Section 5: 5-Point Checklist)
   → Check: /docs/operations/APPENDIX_CODE_REGISTRY.yaml (code availability)
   → Validate: Use python script to detect conflicts (SOP-APPEND-02, Section 7)

   After registration:
   → Read: /docs/operations/SOP-INDEX-03-Index-Integrity.md (4-Location Sync)
   → Update ALL 4 locations in appendices/00_appendix_index.tex
```

---

#### In CLAUDE.md:
```
### Qualitätscheck durchführen (PFLICHT-Workflow)
```

**Should reference:**
- SOP-SCRIPT-01: Pre/post-condition validation pattern
- SOP-RECOVERY-04: Backup before compliance checks

**Addition:**
```
🔍 Operational Requirements:
   Before running compliance checks:
   → Create backup per SOP-RECOVERY-04 (BackupManager class)
   → Document changes per SOP-SCRIPT-01 audit logging
```

---

### Section: "Slash Commands"

#### `/compile` command
**Should reference:** SOP-SCRIPT-01 (script execution pattern)

```yaml
- command: "/compile"
  sop_reference: "SOP-SCRIPT-01, Section 4 (Validation & Dry-Run)"
  preconditions: "LaTeX files exist, texlive installed"
  postconditions: "PDF generated, audit log created"
```

#### `/validate` command
**Should reference:** SOP-SCRIPT-01 (validation pattern)

```yaml
- command: "/validate"
  sop_reference: "SOP-SCRIPT-01, Section 4 (PostCondition Validation)"
  affected_systems:
    - "chapters/*.tex"
    - "appendices/*.tex"
  note: "Creates backup before validation (SOP-RECOVERY-04)"
```

#### `/new-appendix` command
**Should reference:** SOP-APPEND-02 + SOP-INDEX-03

```yaml
- command: "/new-appendix"
  sop_reference: ["SOP-APPEND-02", "SOP-INDEX-03"]
  critical_requirement: "Validate code availability BEFORE creation (SOP-APPEND-02 5-point checklist)"
  backup_requirement: "SOP-RECOVERY-04 BackupManager"
```

---

### Section: "Datenbank-Skills"

#### `/case` command
**Should reference:** SOP-SCRIPT-01 (query execution)

```yaml
- command: "/case"
  sop_reference: "SOP-SCRIPT-01, Section 2 (Preconditions)"
  precondition: "data/case-registry.yaml exists and is current"
```

#### `/intervention` command
**Should reference:** SOP-SCRIPT-01 + SOP-RECOVERY-04

```yaml
- command: "/intervention"
  sop_reference: ["SOP-SCRIPT-01", "SOP-RECOVERY-04"]
  precondition: "data/intervention-registry.yaml exists"
  backup: "Automatic per SOP-RECOVERY-04 TIER 1"
```

---

## Change Mapping: Where to Add SOP References

### In CLAUDE.md "Neues Dokument erstellen" Section:

**Current text:**
```
### Neues Dokument erstellen (PFLICHT-Workflow: 8D-Algorithmus)
```

**Add after 8D description:**
```
🔧 **Operational Requirements (Layer 2):**
   All document generation must follow SOP-SCRIPT-01 pattern:
   - Define preconditions and postconditions
   - Support --dry-run mode for preview before writing
   - Create automatic backup (SOP-RECOVERY-04)
   - Log all generation steps

   See: /docs/operations/SOP-SCRIPT-01-Script-Management.md
```

---

### In CLAUDE.md "Verhaltensmodell designen" Section:

**Current text:**
```
### Verhaltensmodell designen (PFLICHT-Workflow: EEE Workflow)
```

**Add before step descriptions:**
```
📋 **Pre-Workflow Checklist (Layer 2):**
   [ ] Read SOP-SCRIPT-01 for design documentation pattern
   [ ] SOP-RECOVERY-04: Create backup of current /data/models
   [ ] SOP-SCRIPT-01: Document preconditions & postconditions

   See: /docs/operations/SOP-SCRIPT-01-Script-Management.md (Design Phase)
```

---

## File Organization Changes

### In CLAUDE.md: Add New Section

After "Quick Links" section, add:

```markdown
---

## 📚 Layer 2: Operations Standard Operating Procedures

**Critical Note:** Layer 2 SOPs are MANDATORY for:
- Script creation and execution
- Appendix management (code assignment, index updates)
- Disaster recovery and backup
- Operational compliance and auditing

**Entry Point:** Read `/docs/operations/README.md` first

**Quick Links:**
- [SOP-SCRIPT-01: Script Management](docs/operations/SOP-SCRIPT-01-Script-Management.md)
- [SOP-APPEND-02: Appendix Naming](docs/operations/SOP-APPEND-02-Appendix-Naming.md)
- [SOP-INDEX-03: Index Integrity](docs/operations/SOP-INDEX-03-Index-Integrity.md)
- [SOP-RECOVERY-04: Backup & Recovery](docs/operations/SOP-RECOVERY-04-Backup-Recovery.md)
- [Script Registry](docs/operations/SCRIPT_REGISTRY.yaml)
- [Appendix Code Registry](docs/operations/APPENDIX_CODE_REGISTRY.yaml)

---
```

---

## When to Reference Layer 2 in CLAUDE.md

| Scenario | Reference |
|----------|-----------|
| **User creates new script** | SOP-SCRIPT-01: Design → Dev → Validate → Execute |
| **User creates new appendix** | SOP-APPEND-02: 5-point code validation checklist |
| **User registers appendices** | SOP-INDEX-03: 4-location sync protocol |
| **User modifies files** | SOP-RECOVERY-04: Create backup first |
| **User runs validation** | SOP-SCRIPT-01: Precondition validation pattern |
| **User checks compliance** | SOP-SCRIPT-01: PostCondition validation pattern |
| **User fixes a bug** | SOP-RECOVERY-04: Follow recovery scenarios |
| **User executes `--dry-run`** | SOP-SCRIPT-01: Dry-run validation mode |

---

## Integration Examples

### Example 1: CLAUDE.md Section "Neuen Appendix erstellen"

**Before (User-Centric Only):**
```markdown
### Neuen Appendix erstellen (PFLICHT-Workflow)

#### Phase 1: Vorbereitung
1. **Kategorie bestimmen** (Entscheidungsbaum oben)
2. **Code zuweisen** - prüfen mit: `grep -E "^[A-Z]+ & " appendices/00_appendix_index.tex`
```

**After (With Layer 2 References):**
```markdown
### Neuen Appendix erstellen (PFLICHT-Workflow)

⚠️ **Operational Requirements (SOP-APPEND-02):**
   Before assigning ANY code, complete the 5-point checklist in
   `/docs/operations/SOP-APPEND-02-Appendix-Naming.md` (Section 5)

   Critical steps:
   1. Check code availability in APPENDIX_CODE_REGISTRY.yaml
   2. Validate no conflicts exist (python utility provided)
   3. Create RESERVED registry entry (prevents others from using same code)
   4. Then proceed with appendix creation

#### Phase 1: Vorbereitung
1. **Kategorie bestimmen** (Entscheidungsbaum oben)
2. **Code zuweisen** - MUST use SOP-APPEND-02 5-point validation
   - Check: /docs/operations/APPENDIX_CODE_REGISTRY.yaml
   - Validate: python check_code_conflicts.py --code YOUR_CODE
3. **Create RESERVED entry** (prevents concurrent assignment)
```

---

### Example 2: CLAUDE.md Section "Slash Commands"

**Before:**
```markdown
| Command | Beschreibung | Beispiel |
|---------|--------------|----------|
| `/compile` | LaTeX → PDF kompilieren | `/compile outputs/paper.tex` |
```

**After:**
```markdown
| Command | Beschreibung | Beispiel | Operational Ref |
|---------|--------------|----------|-----------------|
| `/compile` | LaTeX → PDF kompilieren | `/compile outputs/paper.tex` | SOP-SCRIPT-01 (Script Lifecycle) |
| `/new-appendix` | Neuen Appendix erstellen | `/new-appendix AX DOMAIN "Title"` | SOP-APPEND-02 (Code Validation) |
| `/validate` | Alle Validierungen ausführen | `/validate` | SOP-SCRIPT-01 (PostConditions) |
```

---

## Maintenance Schedule

### When Adding New Sections to CLAUDE.md:
1. **Check** if section involves scripts → Add SOP-SCRIPT-01 reference
2. **Check** if section involves appendices → Add SOP-APPEND-02/SOP-INDEX-03 references
3. **Check** if section modifies files → Add SOP-RECOVERY-04 reference
4. **Update** this integration guide with new mapping

### Quarterly Review:
- Verify all CLAUDE.md sections have Layer 2 cross-references
- Ensure no new PFLICHT-Workflows bypass operational requirements
- Document lessons in `/quality/lessons_learned.md`

---

## Key Integration Points

### CLAUDE.md PFLICHT-Workflow Checklist

Every PFLICHT-Workflow in CLAUDE.md should now include:

```markdown
### Your Workflow Name

**Layer 2 Operational Requirements:**
☐ SOP-SCRIPT-01 applies? (script execution)
☐ SOP-APPEND-02 applies? (code assignment)
☐ SOP-INDEX-03 applies? (index modifications)
☐ SOP-RECOVERY-04 applies? (backup needed)
☐ Cross-references added to doc

**See:** /docs/operations/README.md for decision tree
```

---

## Transition Timeline

### ✅ Complete (2026-01-15)
- Layer 2 SOPs written (SOP-SCRIPT-01, SOP-APPEND-02, SOP-INDEX-03, SOP-RECOVERY-04)
- Supporting registries created (SCRIPT_REGISTRY.yaml, APPENDIX_CODE_REGISTRY.yaml)
- Operations README created (/docs/operations/README.md)

### ⏳ In Progress (2026-01-15 → 2026-01-20)
- Integration guide created (this file)
- CLAUDE.md updated with Layer 2 cross-references
- Pre-commit hooks updated to enforce Layer 2 compliance

### ⏳ Planned (2026-01-20 → 2026-02-15)
- Layer 3: Infrastructure SOPs (Audit Logging, Dependency Management, Monitoring)
- Bug fix using Layer 2: register_lit_appendices_v2.py
- Quarterly audit execution

---

## FAQ

**Q: Do I need to read all 4 SOPs?**
A: No. Read SOP-SCRIPT-01 first (covers 80% of operations). Others are specialty SOPs for specific tasks.

**Q: Where should I add new SOP references in CLAUDE.md?**
A: Look for PFLICHT-Workflows that involve:
- Script creation/execution → Add SOP-SCRIPT-01
- Appendix creation → Add SOP-APPEND-02 + SOP-INDEX-03
- File modifications → Add SOP-RECOVERY-04

**Q: What if CLAUDE.md and Layer 2 SOPs conflict?**
A: Layer 2 SOPs are the SOURCE OF TRUTH for operational procedures. CLAUDE.md should reference them, not duplicate them.

**Q: Should Layer 2 references be in every CLAUDE.md section?**
A: No, only in sections that involve:
- Executing scripts
- Creating appendices
- Modifying files
- Running validation

**Q: How do I know if my task needs Layer 2?**
A: Use the decision tree in `/docs/operations/README.md` (Quick Decision Tree section)

---

## Template: How to Add SOP References to CLAUDE.md

When you identify a section that needs Layer 2 references, use this template:

```markdown
### [Existing Section Title]

**⚠️ Operational Requirements (Layer 2 SOP):**

[Mandatory Operational Requirements Box]

[Existing CLAUDE.md Content Here]

[Additional operational notes if needed]

**Operational Reference:**
- See: /docs/operations/SOP-[NUMBER]-[NAME].md for detailed procedures
- Decision tree: /docs/operations/README.md (Quick Decision Tree section)
```

---

## Next Steps for CLAUDE.md Integration

1. **Search & Replace:**
   ```bash
   grep -n "Neuen.*erstellen\|Neues.*erstellen\|PFLICHT-Workflow" CLAUDE.md
   ```
   This finds all PFLICHT-Workflow sections that need Layer 2 references

2. **For Each Section Found:**
   - Determine which SOPs apply (use decision tree)
   - Add cross-reference box
   - Update examples with --dry-run, backup references
   - Document in this integration guide

3. **Add New Section to CLAUDE.md:**
   - Link to /docs/operations/README.md
   - Brief explanation of what Layer 2 is
   - Quick links to 4 SOPs

4. **Update PreCommit Hook:**
   - Check that CLAUDE.md has Layer 2 references for PFLICHT-Workflows
   - Warn if new PFLICHT-Workflow added without SOP reference

---

## Success Metrics

✅ **Integration is complete when:**
- [ ] All PFLICHT-Workflows in CLAUDE.md reference appropriate Layer 2 SOPs
- [ ] Slash commands documented with SOP references
- [ ] No PFLICHT-Workflow bypasses Layer 2 requirements
- [ ] Pre-commit hook enforces Layer 2 compliance
- [ ] Users report successful Layer 2 → CLAUDE.md navigation
- [ ] Quality checklist includes Layer 2 reference verification

---

*Layer 2 Integration Guide v1.0 | 2026-01-15 | Integration Protocol: L2-MAIN-001*
