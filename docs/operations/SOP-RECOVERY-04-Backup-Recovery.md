# SOP-RECOVERY-04: Backup, Recovery & Rollback Protocol

> **Purpose:** Establish comprehensive backup and disaster recovery procedures for repository integrity
> **Version:** 1.0
> **Date:** 2026-01-15
> **Owner:** Recovery & Disaster Management Team
> **Review Cycle:** Annually
> **Related:** SOP-SCRIPT-01, SOP-APPEND-02, SOP-INDEX-03

---

## 1. Scope

This SOP covers:
- Automated backup creation (BEFORE every operation)
- Backup versioning and retention
- Recovery procedures (partial and full)
- Rollback strategies (git + filesystem)
- Disaster recovery planning

**In-Scope:**
- Critical files (index, chapters, appendices)
- Databases (papers, cases, interventions)
- Generated outputs (PDFs, CSVs, reports)

**Out-of-Scope:**
- Local development branches
- Cache/temporary files
- Build artifacts

---

## 2. Backup Strategy: 3-Tier System

```
TIER 1: OPERATION-LEVEL BACKUPS (Immediate)
├─ Before every script execution
├─ Before every appendix modification
├─ Before every index update
├─ Retention: 7 days (automatic cleanup)
└─ Format: timestamp backups in /backups/

TIER 2: CHECKPOINT BACKUPS (Daily)
├─ Daily snapshot at midnight (UTC)
├─ Covers entire /appendices and /chapters
├─ Retention: 30 days
├─ Format: daily snapshots /backups/checkpoint/

TIER 3: ARCHIVE BACKUPS (Weekly + Monthly)
├─ Full repository backup
├─ Includes git history
├─ Retention: 3 months for monthly, 4 weeks for weekly
├─ Format: compressed archives /backups/archive/
└─ Storage: Separate from primary repository
```

---

## 3. Automated Backup Creation

### 3.1 Before Script Execution

**Every Python script MUST create backup:**

```python
#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime
import shutil
import logging

class BackupManager:
    """Handles automatic backup creation and management."""

    def __init__(self, scope="appendices"):
        """
        scope: "single" (one file), "appendices", "full"
        """
        self.scope = scope
        self.backup_dir = Path("backups") / scope
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.timestamp = datetime.now().isoformat()

    def create_backup(self, filepath):
        """Create timestamped backup of single file."""
        backup_path = self.backup_dir / f"{filepath.stem}.BACKUP.{self.timestamp}{filepath.suffix}"

        shutil.copy(filepath, backup_path)
        logging.info(f"✅ Backup created: {backup_path}")
        return backup_path

    def create_scope_backup(self):
        """Create backup of entire scope (e.g., appendices/)."""
        if self.scope == "appendices":
            source = Path("appendices")
            archive_name = f"appendices.BACKUP.{self.timestamp}"

        elif self.scope == "chapters":
            source = Path("chapters")
            archive_name = f"chapters.BACKUP.{self.timestamp}"

        elif self.scope == "full":
            source = Path(".")
            archive_name = f"full_repo.BACKUP.{self.timestamp}"

        archive_path = self.backup_dir / archive_name
        shutil.make_archive(str(archive_path), 'tar.gz', source)

        logging.info(f"✅ Scope backup created: {archive_path}.tar.gz")
        return archive_path

    def cleanup_old_backups(self, max_age_days=7):
        """Remove backups older than max_age_days."""
        import glob
        from datetime import timedelta

        now = datetime.now()
        cutoff = now - timedelta(days=max_age_days)

        deleted_count = 0
        for backup_file in self.backup_dir.glob("*"):
            # Extract timestamp from filename
            try:
                timestamp_str = backup_file.name.split("BACKUP.")[1].split(".")[0]
                backup_time = datetime.fromisoformat(timestamp_str)

                if backup_time < cutoff:
                    backup_file.unlink()
                    logging.info(f"🗑️  Deleted old backup: {backup_file}")
                    deleted_count += 1
            except (IndexError, ValueError):
                # Couldn't parse timestamp, skip
                pass

        logging.info(f"✅ Cleanup complete: Deleted {deleted_count} old backups")

# Usage in any script:
backup_mgr = BackupManager(scope="appendices")

# Before modifying files
backup_mgr.create_backup(Path("appendices/00_appendix_index.tex"))

# Optional: Backup entire scope
backup_mgr.create_scope_backup()

# ... do modifications ...

# After successful completion, cleanup old backups
backup_mgr.cleanup_old_backups(max_age_days=7)
```

### 3.2 Daily Checkpoint Backup (Cron Job)

```bash
#!/bin/bash
# Daily checkpoint backup (run at 00:00 UTC)

BACKUP_DIR="backups/checkpoint"
TIMESTAMP=$(date +%Y-%m-%d)
ARCHIVE="$BACKUP_DIR/checkpoint_$TIMESTAMP.tar.gz"

mkdir -p "$BACKUP_DIR"

# Backup appendices and chapters (the critical content)
tar -czf "$ARCHIVE" \
    --exclude='*.BACKUP.*' \
    --exclude='*.tmp' \
    appendices/ \
    chapters/ \
    data/ \
    quality/

echo "✅ Daily checkpoint created: $ARCHIVE"

# Cleanup old checkpoints (keep 30 days)
find "$BACKUP_DIR" -name "checkpoint_*.tar.gz" -mtime +30 -delete

echo "✅ Cleanup complete: Removed checkpoints older than 30 days"
```

**Register in crontab:**

```bash
# Add to crontab -e:
0 0 * * * /home/user/complementarity-context-framework/backups/daily_checkpoint.sh >> /var/log/ebf_backup.log 2>&1
```

### 3.3 Weekly/Monthly Archives

```bash
#!/bin/bash
# Weekly (Friday) and Monthly (1st) archival

BACKUP_DIR="backups/archive"
DAY_OF_WEEK=$(date +%u)
DAY_OF_MONTH=$(date +%d)

mkdir -p "$BACKUP_DIR"

# Weekly backup (Friday = 5)
if [ $DAY_OF_WEEK -eq 5 ]; then
    WEEK=$(date +%Y-W%V)
    ARCHIVE="$BACKUP_DIR/weekly_$WEEK.tar.gz"
    tar -czf "$ARCHIVE" --exclude-caches .
    echo "✅ Weekly archive created: $ARCHIVE"
fi

# Monthly backup (1st of month)
if [ $DAY_OF_MONTH -eq 1 ]; then
    MONTH=$(date +%Y-%m)
    ARCHIVE="$BACKUP_DIR/monthly_$MONTH.tar.gz"
    tar -czf "$ARCHIVE" --exclude-caches .
    echo "✅ Monthly archive created: $ARCHIVE"

    # Include git history
    git bundle create "$BACKUP_DIR/git_$MONTH.bundle" --all
    echo "✅ Git bundle created: $BACKUP_DIR/git_$MONTH.bundle"
fi

# Cleanup old archives (3 months for monthly, 4 weeks for weekly)
find "$BACKUP_DIR/weekly_*.tar.gz" -mtime +28 -delete
find "$BACKUP_DIR/monthly_*.tar.gz" -mtime +90 -delete
find "$BACKUP_DIR/git_*.bundle" -mtime +90 -delete

echo "✅ Archive cleanup complete"
```

---

## 4. Recovery Procedures

### 4.1 Scenario 1: Accidental File Modification (Single File)

**If you accidentally modified `appendices/00_appendix_index.tex`:**

```bash
# Step 1: Identify latest backup
ls -lrt backups/appendices/*BACKUP* | tail -1

# Output: backups/appendices/00_appendix_index.BACKUP.2026-01-15T14:32:45.123456.tex

# Step 2: Restore
cp backups/appendices/00_appendix_index.BACKUP.2026-01-15T14:32:45.123456.tex \
   appendices/00_appendix_index.tex

# Step 3: Verify
python scripts/validate_integrity.py

# Step 4: If validation passes
git status  # Should show only this file modified
git diff appendices/00_appendix_index.tex  # Review the change

# Step 5: Commit the recovery
git add appendices/00_appendix_index.tex
git commit -m "chore: recover appendix index from accidental modification"
```

### 4.2 Scenario 2: Script Execution Failed Partway (Partial Rollback)

**If a script started writing but failed halfway through:**

```bash
# Step 1: Identify what was affected
ls -lrt backups/appendices/*BACKUP* | tail -5  # Show last 5 backups

# Step 2: Restore all affected files to their pre-execution state
for backup in backups/appendices/*BACKUP*2026-01-15T14:32*; do
    ORIGINAL=$(echo $backup | sed 's/.BACKUP.*//g')
    cp "$backup" "$ORIGINAL"
    echo "✅ Restored: $ORIGINAL"
done

# Step 3: Verify system integrity
python scripts/validate_integrity.py

# Step 4: Investigate root cause
cat logs/script_execution_*.log | grep "❌"

# Step 5: Fix script and retry with dry-run
python scripts/problematic_script.py --dry-run
```

### 4.3 Scenario 3: Major Corruption (Checkpoint Recovery)

**If multiple files are corrupted and you need to roll back to last good state:**

```bash
# Step 1: Identify latest good checkpoint
ls -lrt backups/checkpoint/ | tail -1

# Output: checkpoint_2026-01-14.tar.gz (Yesterday's backup)

# Step 2: Verify checkpoint integrity
tar -tzf backups/checkpoint/checkpoint_2026-01-14.tar.gz | head -20

# Step 3: If checkpoint looks good, extract to temporary location
mkdir -p /tmp/recovery
tar -xzf backups/checkpoint/checkpoint_2026-01-14.tar.gz -C /tmp/recovery

# Step 4: Review what's in the recovery
diff -r appendices /tmp/recovery/appendices | head -20

# Step 5: If happy with recovery, restore
cp -r /tmp/recovery/appendices/* appendices/
cp -r /tmp/recovery/chapters/* chapters/
cp -r /tmp/recovery/data/* data/

# Step 6: Verify
python scripts/validate_integrity.py

# Step 7: Commit the recovery
git add .
git commit -m "chore: recover from corruption using checkpoint 2026-01-14"

# Step 8: Notify team
echo "📢 Recovery completed from checkpoint 2026-01-14. Recovered files committed."
```

### 4.4 Scenario 4: Total Disaster (Full Repository Recovery)

**If the entire repository is corrupted:**

```bash
# Step 1: Preserve current state (just in case)
mv complementarity-context-framework complementarity-context-framework.CORRUPTED.$(date +%s)

# Step 2: Restore from git
git clone https://github.com/FehrAdvice-Partners-AG/complementarity-context-framework.git complementarity-context-framework

# Step 3: Check if that helps
cd complementarity-context-framework
git log --oneline | head -10

# Step 4: If git is also corrupted, restore from archive backup
cd ..
tar -xzf backups/archive/monthly_2026-01.tar.gz

# Step 5: Verify recovery
python scripts/validate_integrity.py

# Step 6: If successful, cleanup corrupted copy
rm -rf complementarity-context-framework.CORRUPTED.*
```

---

## 5. Rollback Strategies

### 5.1 Git-Based Rollback (Recommended)

```bash
# Option 1: Undo single commit
git revert <commit_hash>

# Option 2: Reset to previous state (be careful!)
git reset --hard <commit_hash>

# Option 3: Revert specific file to specific commit
git checkout <commit_hash> -- appendices/00_appendix_index.tex

# Always verify after rollback
python scripts/validate_integrity.py
git diff HEAD
```

### 5.2 Backup-Based Rollback

```bash
# If git rollback isn't sufficient (e.g., git history corrupted)

# Step 1: Find closest recent backup before the problem
ls -lrt backups/checkpoint/ | grep "2026-01-14"

# Step 2: Extract to temp location and review
tar -xzf backups/checkpoint/checkpoint_2026-01-14.tar.gz -C /tmp/review

# Step 3: Selectively restore files
cp /tmp/review/appendices/00_appendix_index.tex appendices/

# Step 4: Verify and commit
python scripts/validate_integrity.py
git add appendices/00_appendix_index.tex
git commit -m "chore: rollback appendix index to 2026-01-14 state"
```

---

## 6. Backup Verification & Testing

### 6.1 Monthly Backup Test

```bash
#!/bin/bash
# Test that backups are actually recoverable (run monthly)

echo "🔍 BACKUP VERIFICATION TEST"
echo "============================"

# Test 1: Can we extract the latest checkpoint?
echo ""
echo "Test 1: Checkpoint extraction..."
LATEST_CHECKPOINT=$(ls -rt backups/checkpoint/*.tar.gz | tail -1)

if tar -tzf "$LATEST_CHECKPOINT" >/dev/null 2>&1; then
    echo "  ✅ Checkpoint is valid"
else
    echo "  ❌ Checkpoint is CORRUPTED!"
    exit 1
fi

# Test 2: Can we extract the latest monthly archive?
echo ""
echo "Test 2: Monthly archive extraction..."
LATEST_MONTHLY=$(ls -rt backups/archive/monthly_*.tar.gz | tail -1)

if tar -tzf "$LATEST_MONTHLY" >/dev/null 2>&1; then
    echo "  ✅ Monthly archive is valid"
else
    echo "  ❌ Monthly archive is CORRUPTED!"
    exit 1
fi

# Test 3: Can we restore git history?
echo ""
echo "Test 3: Git bundle validity..."
LATEST_BUNDLE=$(ls -rt backups/archive/git_*.bundle | tail -1)

if git bundle verify "$LATEST_BUNDLE" >/dev/null 2>&1; then
    echo "  ✅ Git bundle is valid"
else
    echo "  ❌ Git bundle is CORRUPTED!"
    exit 1
fi

# Test 4: Do critical files exist in backups?
echo ""
echo "Test 4: Critical file coverage..."
TEMP_DIR="/tmp/backup_test_$$"
mkdir -p "$TEMP_DIR"

tar -xzf "$LATEST_CHECKPOINT" -C "$TEMP_DIR"

MISSING=0
for file in appendices/00_appendix_index.tex chapters/00_chapter_template.tex data/case-registry.yaml; do
    if [ -f "$TEMP_DIR/$file" ]; then
        echo "  ✅ $file found in backup"
    else
        echo "  ❌ $file MISSING from backup!"
        ((MISSING++))
    fi
done

rm -rf "$TEMP_DIR"

if [ $MISSING -gt 0 ]; then
    exit 1
fi

echo ""
echo "============================"
echo "✅ ALL BACKUP TESTS PASSED"
echo "Backups are recoverable"
```

**Register in crontab (monthly):**

```bash
# Run on 15th of each month at 02:00 UTC
0 2 15 * * /home/user/complementarity-context-framework/backups/verify_backups.sh >> /var/log/ebf_backup_verify.log 2>&1
```

---

## 7. Backup Inventory & Retention Policy

```yaml
backup_policy:
  tier_1_operation:
    retention_days: 7
    frequency: every_script_execution
    storage: backups/[scope]/
    purpose: "Undo single operation"

  tier_2_checkpoint:
    retention_days: 30
    frequency: daily_0000_utc
    storage: backups/checkpoint/
    purpose: "Rollback to recent good state"

  tier_3_weekly:
    retention_weeks: 4
    frequency: every_friday
    storage: backups/archive/
    purpose: "Multi-week recovery"

  tier_3_monthly:
    retention_months: 3
    frequency: 1st_of_month
    storage: backups/archive/ + offsite
    purpose: "Long-term recovery"

  git_bundle:
    retention_months: 3
    frequency: 1st_of_month
    storage: backups/archive/
    purpose: "Restore git history if repo corrupted"
```

---

## 8. Disaster Recovery Plan (DRP)

### 8.1 Incident Response Flowchart

```
PROBLEM DETECTED
      ↓
Is it a single file? → YES → Scenario 1: Single File Recovery
      ↓ NO
Is script partially executed? → YES → Scenario 2: Partial Rollback
      ↓ NO
Are multiple files corrupted? → YES → Scenario 3: Checkpoint Recovery
      ↓ NO
Is everything corrupted? → YES → Scenario 4: Total Repository Recovery
      ↓ NO
Unknown problem → CALL DRP COORDINATOR
```

### 8.2 DRP Coordinator Checklist

```markdown
# Disaster Recovery Plan Activation

**Incident Time:** _______________
**Discovered By:** _______________
**Incident Type:** _______________

## Immediate Actions (0-5 min)
- [ ] Stop any ongoing operations
- [ ] Document current state with screenshots
- [ ] Notify team members
- [ ] Open incident log: `quality/incidents/incident_YYYYMMDD_HHMMSS.md`

## Assessment (5-15 min)
- [ ] Scope: How many files affected?
- [ ] Severity: Is production broken? Is data lost?
- [ ] Root Cause: What happened? (script error, user mistake, corruption?)
- [ ] Recovery Options: Which scenario applies?

## Recovery Execution (15+ min)
- [ ] Execute appropriate recovery scenario (SOP-RECOVERY-04)
- [ ] Verify system integrity: `python scripts/validate_integrity.py`
- [ ] Test critical functions
- [ ] If successful: Commit recovery, document lessons learned
- [ ] If unsuccessful: Escalate to backup DRP coordinator

## Post-Incident (After recovery)
- [ ] Root cause analysis: How do we prevent this?
- [ ] Process improvement: Update relevant SOP
- [ ] Communication: Brief team on what happened & how we recovered
- [ ] Testing: Verify backups are working
```

---

## 9. SOP Version & Change Log

| Version | Date | Changes | Status |
|---------|------|---------|--------|
| 1.0 | 2026-01-15 | Initial release - 4 recovery scenarios + verification protocol | ACTIVE |

---

*SOP-RECOVERY-04 | Version 1.0 | Owner: Recovery & Disaster Management Team*
