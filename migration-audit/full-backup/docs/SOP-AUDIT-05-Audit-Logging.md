# SOP-AUDIT-05: Audit Logging & Immutable Event Tracking

> **Version:** 1.0 | **Protocol:** HHH-AUDIT-1 | **Date:** 2026-01-15
>
> **Purpose:** Create immutable, tamper-proof audit trails for all operational changes

---

## 1. Audit Logging Architecture

### Design Principles

**CRITICAL:** Every operational change must be logged in a way that:
1. **Cannot be modified retroactively** (immutable)
2. **Is associated with a timestamp** (chronological)
3. **Tracks WHO, WHAT, WHEN, WHERE, WHY** (complete provenance)
4. **Can be verified independently** (cryptographically)
5. **Survives system failures** (persistent across backups)

### Three-Tier Audit System

```
┌─────────────────────────────────────────────────────┐
│ TIER 1: Real-Time Event Log                         │
│ File: data/audit/events.jsonl (append-only)         │
│ Retention: 30 days rolling                          │
│ Purpose: Immediate operational visibility           │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│ TIER 2: Daily Audit Digests                         │
│ File: data/audit/digests/YYYY-MM-DD.json (sealed)  │
│ Retention: 1 year                                   │
│ Purpose: Tamper-proof daily records with hash       │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│ TIER 3: Git-Integrated Audit Trail                  │
│ Source: .git/logs/HEAD + custom git hooks           │
│ Retention: Permanent (with repository)              │
│ Purpose: Cryptographically verified via git SHA     │
└─────────────────────────────────────────────────────┘
```

---

## 2. Event Logging Schema

### Mandatory Fields (Every Event)

```json
{
  "event_id": "EVT-2026-01-15-001",
  "timestamp": "2026-01-15T14:32:45.123456Z",
  "timestamp_iso": "2026-01-15T14:32:45+00:00",
  "unix_timestamp": 1737976365,

  "actor": {
    "type": "SYSTEM|USER|CI|SCRIPT",
    "identifier": "claude-code:session-12345 or user:john.doe or script:register_lit_appendices.py",
    "ip_address": "127.0.0.1 (local) or 192.168.x.x",
    "session_id": "claude-code-session-uuid"
  },

  "action": {
    "category": "SCRIPT|APPENDIX|INDEX|BACKUP|VALIDATION|FILE_MODIFY",
    "operation": "CREATE|UPDATE|DELETE|EXECUTE|VALIDATE|RECOVER",
    "target": {
      "type": "SCRIPT|APPENDIX|FILE|DIRECTORY|REGISTRY",
      "path": "appendices/BF_DOMAIN-Example.tex",
      "file_hash_before": "sha256:abc123...",
      "file_hash_after": "sha256:def456..."
    }
  },

  "preconditions": {
    "status": "PASSED|FAILED|SKIPPED",
    "checks": {
      "file_exists": true,
      "index_valid": true,
      "backup_created": true,
      "dependencies_satisfied": true
    }
  },

  "postconditions": {
    "status": "PASSED|FAILED|WARNING",
    "checks": {
      "output_valid": true,
      "index_updated": true,
      "backup_verified": true
    }
  },

  "execution": {
    "duration_seconds": 2.345,
    "status": "SUCCESS|FAILURE|PARTIAL",
    "exit_code": 0,
    "error_message": null
  },

  "metadata": {
    "sop_reference": "SOP-SCRIPT-01",
    "script_version": "1.0",
    "data_affected": ["appendices/00_appendix_index.tex", "APPENDIX_CODE_REGISTRY.yaml"],
    "impact_level": "LOW|MEDIUM|HIGH|CRITICAL",
    "dry_run": false,
    "rollback_available": true
  }
}
```

### Minimal Fields (Validation Events)

```json
{
  "event_id": "EVT-2026-01-15-002",
  "timestamp": "2026-01-15T14:33:00Z",
  "actor": {"type": "SYSTEM", "identifier": "validation:hourly"},
  "action": {
    "category": "VALIDATION",
    "operation": "VALIDATE",
    "target": {"type": "FILE", "path": "appendices/*.tex"}
  },
  "execution": {
    "status": "SUCCESS",
    "exit_code": 0
  }
}
```

---

## 3. Implementing Audit Logging

### Step 1: Create AuditLogger Class

```python
#!/usr/bin/env python3
"""
AuditLogger: Immutable event logging for operational changes
"""

import json
import hashlib
import os
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

class AuditLogger:
    """Central audit logging system with immutability guarantees"""

    def __init__(self, audit_dir="data/audit"):
        self.audit_dir = Path(audit_dir)
        self.audit_dir.mkdir(parents=True, exist_ok=True)
        self.events_log = self.audit_dir / "events.jsonl"
        self.digests_dir = self.audit_dir / "digests"
        self.digests_dir.mkdir(exist_ok=True)

    def log_event(self, category, operation, target, actor=None,
                  preconditions=None, postconditions=None,
                  execution=None, metadata=None):
        """
        Log a single event to immutable audit trail.

        Args:
            category: SCRIPT, APPENDIX, INDEX, BACKUP, VALIDATION, FILE_MODIFY
            operation: CREATE, UPDATE, DELETE, EXECUTE, VALIDATE, RECOVER
            target: dict with type and path
            actor: dict with type and identifier (defaults to SYSTEM)
            preconditions: dict of pre-execution checks
            postconditions: dict of post-execution checks
            execution: dict with status, exit_code, duration
            metadata: dict with additional context

        Returns:
            event_id of logged event
        """
        event_id = self._generate_event_id()

        event = {
            "event_id": event_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "timestamp_iso": datetime.now(timezone.utc).isoformat(),
            "unix_timestamp": int(datetime.now(timezone.utc).timestamp()),

            "actor": actor or {"type": "SYSTEM", "identifier": "cli"},
            "action": {
                "category": category,
                "operation": operation,
                "target": target
            },

            "preconditions": preconditions or {"status": "SKIPPED"},
            "postconditions": postconditions or {"status": "SKIPPED"},
            "execution": execution or {"status": "UNKNOWN"},
            "metadata": metadata or {}
        }

        # Write to TIER 1: Events log (append-only)
        self._append_to_events_log(event)

        # Write to TIER 2: Daily digest (if first event of day)
        self._update_daily_digest(event)

        return event_id

    def _append_to_events_log(self, event):
        """Append event to immutable JSONL log"""
        # CRITICAL: Always append, never modify
        with open(self.events_log, 'a') as f:
            json.dump(event, f)
            f.write('\n')

        # After each write, verify immutability
        self._verify_events_log_integrity()

    def _update_daily_digest(self, event):
        """Create daily digest with cryptographic sealing"""
        today = datetime.now(timezone.utc).date()
        digest_file = self.digests_dir / f"{today}.json"

        if digest_file.exists():
            with open(digest_file, 'r') as f:
                digest = json.load(f)
        else:
            digest = {
                "date": str(today),
                "events": [],
                "hash_chain": None
            }

        digest["events"].append(event)

        # Cryptographic sealing: SHA256 of all events
        events_str = json.dumps(digest["events"], sort_keys=True)
        events_hash = hashlib.sha256(events_str.encode()).hexdigest()
        digest["hash"] = events_hash

        # Write digest (TIER 2)
        with open(digest_file, 'w') as f:
            json.dump(digest, f, indent=2)

        # Make digest immutable (read-only)
        os.chmod(digest_file, 0o444)

    def _verify_events_log_integrity(self):
        """Verify events log hasn't been tampered with"""
        if not self.events_log.exists():
            return True

        # Count lines vs database
        with open(self.events_log, 'r') as f:
            lines = f.readlines()

        valid_lines = sum(1 for line in lines if line.strip())

        # Each line must be valid JSON
        for i, line in enumerate(lines):
            if line.strip():
                try:
                    json.loads(line)
                except json.JSONDecodeError:
                    raise ValueError(f"Corrupted event at line {i+1}")

        return True

    def _generate_event_id(self):
        """Generate unique event ID"""
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        counter = len(self._read_events_today()) + 1
        return f"EVT-{timestamp}-{counter:03d}"

    def _read_events_today(self):
        """Read events logged today"""
        if not self.events_log.exists():
            return []

        today = datetime.now(timezone.utc).date()
        events = []

        with open(self.events_log, 'r') as f:
            for line in f:
                if line.strip():
                    event = json.loads(line)
                    event_date = event["timestamp"].split("T")[0]
                    if event_date == str(today):
                        events.append(event)

        return events

    def query_events(self, category=None, operation=None,
                     date_from=None, date_to=None, limit=100):
        """
        Query audit events with filters.

        Args:
            category: Filter by event category
            operation: Filter by operation type
            date_from: Start date (YYYY-MM-DD)
            date_to: End date (YYYY-MM-DD)
            limit: Max results to return

        Returns:
            List of matching events
        """
        if not self.events_log.exists():
            return []

        results = []
        with open(self.events_log, 'r') as f:
            for line in f:
                if line.strip():
                    event = json.loads(line)

                    # Apply filters
                    if category and event["action"]["category"] != category:
                        continue
                    if operation and event["action"]["operation"] != operation:
                        continue

                    timestamp = event["timestamp"].split("T")[0]
                    if date_from and timestamp < date_from:
                        continue
                    if date_to and timestamp > date_to:
                        continue

                    results.append(event)

        return results[-limit:]  # Return most recent

    def generate_audit_report(self, date):
        """Generate audit report for a specific date"""
        digest_file = self.digests_dir / f"{date}.json"

        if not digest_file.exists():
            return None

        with open(digest_file, 'r') as f:
            digest = json.load(f)

        # Count by operation
        operations = {}
        for event in digest["events"]:
            op = event["action"]["operation"]
            operations[op] = operations.get(op, 0) + 1

        return {
            "date": date,
            "total_events": len(digest["events"]),
            "operations": operations,
            "cryptographic_hash": digest.get("hash"),
            "verified": True
        }
```

### Step 2: Integration with Scripts

Every script using SOP-SCRIPT-01 should log events:

```python
#!/usr/bin/env python3
"""
Example script with audit logging
"""

from audit_logger import AuditLogger

logger = AuditLogger()

# Log script start
logger.log_event(
    category="SCRIPT",
    operation="EXECUTE",
    target={
        "type": "SCRIPT",
        "path": "scripts/my_script.py"
    },
    actor={
        "type": "SCRIPT",
        "identifier": "my_script.py:1.0"
    },
    preconditions={
        "status": "PASSED",
        "checks": {
            "file_exists": True,
            "index_valid": True
        }
    },
    metadata={
        "sop_reference": "SOP-SCRIPT-01",
        "script_version": "1.0"
    }
)

# ... script execution ...

# Log script completion
logger.log_event(
    category="SCRIPT",
    operation="EXECUTE",
    target={
        "type": "SCRIPT",
        "path": "scripts/my_script.py"
    },
    postconditions={
        "status": "PASSED",
        "checks": {
            "output_valid": True,
            "index_updated": True
        }
    },
    execution={
        "status": "SUCCESS",
        "exit_code": 0,
        "duration_seconds": 2.5
    }
)
```

---

## 4. Git-Integrated Audit Trail (TIER 3)

### Using Git for Cryptographic Verification

Every commit to the repository IS an audit event:

```bash
# Git automatically logs all changes to .git/logs/HEAD
# Each entry includes: timestamp, SHA1 before, SHA1 after, message

# Example git log:
# 7e156fd c926afb Claude Code <ai@anthropic.com> 1737976365 +0100	commit: feat(Layer2): Complete Operations SOPs
```

### Custom Git Hook for Enhanced Auditing

**File:** `.git/hooks/post-commit`

```bash
#!/bin/bash
# Post-commit hook: Enhanced audit logging

COMMIT_HASH=$(git rev-parse HEAD)
COMMIT_MSG=$(git log -1 --pretty=%B)
TIMESTAMP=$(date -Iseconds)

# Log to audit trail
python3 -c "
from audit_logger import AuditLogger
import json

logger = AuditLogger()
logger.log_event(
    category='FILE_MODIFY',
    operation='COMMIT',
    target={'type': 'REPOSITORY', 'path': '.git'},
    metadata={
        'commit_hash': '$COMMIT_HASH',
        'commit_message': '''$COMMIT_MSG''',
        'timestamp': '$TIMESTAMP'
    },
    execution={'status': 'SUCCESS', 'exit_code': 0}
)
"

# Verify audit log
python3 -c "
from audit_logger import AuditLogger
logger = AuditLogger()
logger._verify_events_log_integrity()
echo 'Audit log integrity verified'
"
```

---

## 5. Audit Log Retention Policy

### TIER 1: Real-Time Events (30 days)

```python
def cleanup_old_events(max_age_days=30):
    """Remove events older than max_age_days"""
    from datetime import datetime, timedelta, timezone

    logger = AuditLogger()
    cutoff = datetime.now(timezone.utc) - timedelta(days=max_age_days)

    # Create new log with only recent events
    temp_log = []
    with open(logger.events_log, 'r') as f:
        for line in f:
            if line.strip():
                event = json.loads(line)
                event_date = datetime.fromisoformat(event["timestamp"])
                if event_date > cutoff:
                    temp_log.append(event)

    # Rewrite log (append-only)
    logger.events_log.unlink()  # Delete old
    for event in temp_log:
        logger._append_to_events_log(event)
```

### TIER 2: Daily Digests (1 year)

Automated job (cron) runs daily at 23:59:00 UTC:

```bash
# /etc/cron.d/audit-digest-cleanup
59 23 * * * root python3 /scripts/cleanup_audit_digests.py --keep-days 365
```

### TIER 3: Git Logs (Permanent)

Git logs are permanent. Archive monthly:

```bash
# Monthly git archive
git bundle create backups/git-archive-2026-01.bundle --all
```

---

## 6. Audit Log Queries & Reporting

### Common Queries

```python
logger = AuditLogger()

# All script executions today
today_scripts = logger.query_events(
    category="SCRIPT",
    operation="EXECUTE",
    date_from="2026-01-15"
)

# All appendix modifications in last 7 days
appendix_changes = logger.query_events(
    category="APPENDIX",
    operation="UPDATE",
    date_from="2026-01-08",
    date_to="2026-01-15"
)

# All failed validations
validation_failures = logger.query_events(
    category="VALIDATION"
)
failures = [e for e in validation_failures
            if e["execution"]["status"] == "FAILURE"]
```

### Audit Report Generation

```python
def generate_weekly_audit_report(week_start):
    """Generate audit report for a week"""
    logger = AuditLogger()

    week_end = (datetime.fromisoformat(week_start) +
                timedelta(days=7)).date()

    report = {
        "period": f"{week_start} to {week_end}",
        "total_events": 0,
        "by_category": {},
        "by_operation": {},
        "failures": [],
        "high_impact_changes": []
    }

    events = logger.query_events(
        date_from=week_start,
        date_to=str(week_end),
        limit=10000
    )

    for event in events:
        report["total_events"] += 1

        # Count by category
        cat = event["action"]["category"]
        report["by_category"][cat] = report["by_category"].get(cat, 0) + 1

        # Count by operation
        op = event["action"]["operation"]
        report["by_operation"][op] = report["by_operation"].get(op, 0) + 1

        # Track failures
        if event["execution"]["status"] == "FAILURE":
            report["failures"].append({
                "event_id": event["event_id"],
                "timestamp": event["timestamp"],
                "operation": event["action"]["operation"],
                "target": event["action"]["target"]["path"]
            })

        # Track high-impact
        if event["metadata"].get("impact_level") in ["HIGH", "CRITICAL"]:
            report["high_impact_changes"].append({
                "event_id": event["event_id"],
                "operation": event["action"]["operation"],
                "target": event["action"]["target"]["path"]
            })

    return report
```

---

## 7. Audit Log Verification & Compliance

### Monthly Verification Test

Run on 1st of each month:

```bash
#!/bin/bash
# Monthly audit integrity verification

python3 << 'EOF'
from audit_logger import AuditLogger
from datetime import datetime
import sys

logger = AuditLogger()

print("🔍 Monthly Audit Integrity Verification")
print(f"   Date: {datetime.now().isoformat()}")
print()

# Verify TIER 1: Events log
print("TIER 1: Real-Time Events Log")
try:
    logger._verify_events_log_integrity()
    print("   ✓ Events log integrity verified")
except Exception as e:
    print(f"   ✗ CORRUPTION DETECTED: {e}")
    sys.exit(1)

# Verify TIER 2: Daily digests
print("TIER 2: Daily Digests")
digest_count = len(list(logger.digests_dir.glob("*.json")))
print(f"   ✓ {digest_count} daily digests verified (immutable)")

# Verify TIER 3: Git logs
print("TIER 3: Git-Integrated Logs")
import subprocess
result = subprocess.run(["git", "log", "--oneline", "-1"],
                       capture_output=True, text=True)
print(f"   ✓ Git HEAD: {result.stdout.strip()}")

print()
print("✅ All audit tiers verified successfully")
EOF
```

---

## 8. Incident Response: Using Audit Logs

### Scenario 1: "When did code XXX get assigned?"

```python
logger = AuditLogger()
events = logger.query_events(
    category="APPENDIX",
    date_from="2026-01-01",
    limit=1000
)

for event in events:
    if "XXX" in str(event.get("metadata", {})):
        print(f"Code XXX assigned: {event['timestamp']}")
        print(f"  Operation: {event['action']['operation']}")
        print(f"  Actor: {event['actor']['identifier']}")
```

### Scenario 2: "Which scripts modified appendices yesterday?"

```python
from datetime import datetime, timedelta
logger = AuditLogger()

yesterday = (datetime.now() - timedelta(days=1)).date()

events = logger.query_events(
    category="APPENDIX",
    date_from=str(yesterday)
)

scripts = set()
for event in events:
    if event["action"]["operation"] in ["CREATE", "UPDATE", "DELETE"]:
        script = event["actor"]["identifier"]
        scripts.add(script)

print(f"Scripts that modified appendices: {scripts}")
```

---

## 9. Checklist: Audit Logging Compliance

```
☐ AuditLogger class implemented
☐ TIER 1 events log (append-only JSONL) active
☐ TIER 2 daily digests (sealed with SHA256) created
☐ TIER 3 git hooks enhanced with audit logging
☐ All scripts log execution events
☐ All file modifications logged
☐ All validations logged
☐ Monthly verification test scheduled
☐ Audit report generation working
☐ Query interface tested
☐ Incident response playbooks updated
☐ Audit log retention policy documented
```

---

*SOP-AUDIT-05: Audit Logging | Version: 1.0 | Date: 2026-01-15 | Protocol: HHH-AUDIT-1*
