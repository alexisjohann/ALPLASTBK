# Layer 3: Infrastructure & System Observability

> **Complete EBF Operations Stack**
>
> Version: 1.0 | Date: 2026-01-15 | Framework: L1+L2+L3

---

## What is Layer 3?

**Layer 1 (CLAUDE.md):** User-facing instructions
**Layer 2 (SOP-SCRIPT-01 through SOP-RECOVERY-04):** Operational procedures
**Layer 3 (This):** Infrastructure-level observability & governance

Layer 3 adds:
1. **Immutable audit trails** (SOP-AUDIT-05)
2. **Dependency tracking** (SOP-DEPEND-06)
3. **Automated validation** (SOP-VALID-07)
4. **Real-time monitoring** (SOP-MONITOR-08)

---

## The 4 Infrastructure SOPs

### SOP-AUDIT-05: Audit Logging & Immutable Event Tracking

**Problem Solved:** "What happened? When? Who did it? Why?"

**Key Features:**
- **3-Tier Audit System:**
  - TIER 1: Real-time JSONL events (30-day retention)
  - TIER 2: Daily sealed digests with SHA256 (1-year retention)
  - TIER 3: Git-integrated logs (permanent)
- **Complete Event Schema:** WHO, WHAT, WHEN, WHERE, WHY, HOW
- **Immutable:** Events cannot be modified retroactively
- **Queryable:** Find events by category, date, actor, operation
- **Cryptographically Verified:** SHA256 hashing prevents tampering

**File:** `SOP-AUDIT-05-Audit-Logging.md`

**When to Use:**
- Every script should log its execution
- Every file modification creates audit entry
- Every validation creates audit entry
- Every failure must be logged for incident analysis

---

### SOP-DEPEND-06: Dependency Management & Script Relations

**Problem Solved:** "Which scripts depend on which? In what order? What breaks if I change this?"

**Key Features:**
- **Dependency Graph:** Maps all 69 scripts' relationships
- **Topological Sorting:** Computes correct execution order
- **Critical Path Analysis:** Identifies slowest execution path
- **Impact Analysis:** Shows what breaks if file changes
- **Conflict Detection:** Prevents concurrent execution of conflicting scripts
- **Parallel Execution:** Identifies which scripts can run simultaneously

**File:** `SOP-DEPEND-06-Dependency-Management.md`

**When to Use:**
- Before scheduling script executions
- When adding new scripts (document their dependencies)
- When modifying a file (understand impact)
- To optimize execution speed (parallelize where possible)

---

### SOP-VALID-07: Automated Validation Framework

**Problem Solved:** "Is everything still working? What's broken?"

**Key Features:**
- **4-Tier Validation:**
  - TIER 1: Pre-execution validation (SOP-SCRIPT-01)
  - TIER 2: Post-execution validation (SOP-SCRIPT-01)
  - TIER 3: Continuous scheduled validation
  - TIER 4: On-demand full system audit
- **47+ Validation Rules:** Template compliance, index integrity, dependency graphs, etc.
- **HTML Reporting:** Generate compliance scorecards
- **Failure Response:** Automatic rollback on critical failures

**File:** `SOP-VALID-07-Validation-Framework.md`

**When to Use:**
- Every script automatically runs TIER 1 & 2
- Hourly automation checks TIER 3
- Monthly full audit via `/validate` command
- After system changes to verify integrity

---

### SOP-MONITOR-08: Monitoring & Alerting System

**Problem Solved:** "Is something wrong? Notify me immediately. Show me trends."

**Key Features:**
- **Real-Time Metrics:**
  - Operational: script success rates, execution time
  - Integrity: index sync, code conflicts, orphaned files
  - Resources: disk space, backup coverage, file counts
  - Compliance: template scores, SOP violations
- **Smart Alerting:**
  - CRITICAL: Email + Slack + Alert log
  - HIGH: Slack + Alert log
  - MEDIUM: Alert log only
- **Trend Analysis:** Track metrics over 30 days
- **HTML Dashboard:** Real-time system health visualization

**File:** `SOP-MONITOR-08-Monitoring-Alerting.md`

**When to Use:**
- System runs monitoring continuously
- Alerts trigger when thresholds crossed
- Dashboard shows overall health
- Trends reveal performance issues

---

## Complete Operational Stack

```
┌──────────────────────────────────────────────────────────────┐
│ USER REQUEST (Layer 1: CLAUDE.md)                            │
│ "Create a new appendix"                                      │
└────────────────────────┬─────────────────────────────────────┘
                         ↓
┌──────────────────────────────────────────────────────────────┐
│ OPERATIONAL PROCEDURE (Layer 2: SOP-SCRIPT-01)               │
│ 1. Check preconditions (dependencies, inputs)               │
│    → SOP-DEPEND-06: Validate no conflicts                   │
│ 2. Execute (generate appendix file)                         │
│ 3. Validate postconditions                                  │
│    → SOP-VALID-07: TIER 2 validation                        │
│ 4. Create backup                                            │
│    → SOP-RECOVERY-04: BackupManager                         │
└────────────────────────┬─────────────────────────────────────┘
                         ↓
┌──────────────────────────────────────────────────────────────┐
│ INFRASTRUCTURE OBSERVABILITY (Layer 3)                       │
│ • Log event to audit trail                                  │
│   → SOP-AUDIT-05: AuditLogger                               │
│ • Collect metrics                                           │
│   → SOP-MONITOR-08: MetricsCollector                        │
│ • Check for issues                                          │
│   → SOP-VALID-07: Continuous validation (TIER 3)            │
│ • If problem detected, alert team                           │
│   → SOP-MONITOR-08: AlertingSystem                          │
└──────────────────────────────────────────────────────────────┘
```

---

## Integration with Layer 2

Each Layer 2 SOP triggers Layer 3 automatically:

| Layer 2 SOP | Triggers | Layer 3 SOP |
|------------|----------|------------|
| **SOP-SCRIPT-01** | Pre/post-execution validation | SOP-VALID-07 (TIER 1, 2) |
| **SOP-SCRIPT-01** | All operations logged | SOP-AUDIT-05 (AuditLogger) |
| **SOP-APPEND-02** | Code conflict detection | SOP-DEPEND-06 + SOP-MONITOR-08 |
| **SOP-INDEX-03** | Index sync verification | SOP-VALID-07 (TIER 2) |
| **SOP-RECOVERY-04** | Backup monitoring | SOP-MONITOR-08 (metrics) |

---

## Getting Started with Layer 3

### Step 1: Review the SOPs (30 min)

Read in this order:
1. SOP-AUDIT-05 (understand what's being logged)
2. SOP-DEPEND-06 (understand script relationships)
3. SOP-VALID-07 (understand validation rules)
4. SOP-MONITOR-08 (understand monitoring)

### Step 2: Enable Audit Logging (15 min)

```bash
# Create audit infrastructure
mkdir -p data/audit/digests
python3 -c "from audit_logger import AuditLogger; AuditLogger().log_event(...)"
```

### Step 3: Map Dependencies (1 hour)

```bash
# Document script dependencies in DEPENDENCY_GRAPH.yaml
# For each of 69 scripts, add:
#   - inputs (files it reads)
#   - outputs (files it writes)
#   - dependencies (scripts that must complete first)
#   - estimated duration
```

### Step 4: Enable Validation (30 min)

```bash
# Create validation rules in VALIDATION_RULES.yaml
# Activate pre-commit hook for TIER 2 validation
chmod +x .git/hooks/pre-commit
```

### Step 5: Enable Monitoring (30 min)

```bash
# Schedule cron jobs for metrics collection
# Configure alerting (email, Slack)
# Generate dashboard
```

---

## Key Metrics to Watch

### Critical (Alert immediately if triggered)

```
❌ index_consistency < 100%
   → Index locations out of sync (SOP-INDEX-03 failure)
   → Action: Run SOP-RECOVERY-04 restore

❌ code_conflict_count > 0
   → Duplicate code assignments detected (SOP-APPEND-02 failure)
   → Action: Run code conflict resolution

❌ orphaned_file_count > 0
   → Files exist but not in index (data corruption)
   → Action: Run SOP-RECOVERY-04 restore

❌ backup_coverage < 95%
   → Insufficient backups exist (disaster recovery risk)
   → Action: Check SOP-RECOVERY-04 backup system
```

### Important (Monitor and trend)

```
⚠️  script_success_rate < 95%
   → Too many script failures
   → Action: Review audit logs (SOP-AUDIT-05)

⚠️  validation_failure_rate > 5%
   → Too many validations failing (SOP-VALID-07)
   → Action: Fix underlying issues

⚠️  appendix_compliance_avg < 85%
   → Templates not being followed
   → Action: Run compliance correction
```

---

## Incident Response Examples

### Scenario 1: "Index consistency alert triggered"

```
1. Alert from SOP-MONITOR-08 → Index locations out of sync
2. Check SOP-AUDIT-05 logs → What changed?
3. Check SOP-DEPEND-06 → What scripts ran?
4. Run SOP-VALID-07 TIER 4 → Full validation audit
5. If data corrupted → Use SOP-RECOVERY-04 restore
6. Document in audit log (SOP-AUDIT-05)
```

### Scenario 2: "Script X suddenly slow (10x normal)"

```
1. Check SOP-MONITOR-08 metrics → Execution time trending up
2. Check SOP-DEPEND-06 → Did dependencies change?
3. Check SOP-AUDIT-05 → Did input file size grow?
4. Check system resources → Disk space? Memory?
5. Optimize or scale as needed
```

### Scenario 3: "Suspicious operation detected"

```
1. Check SOP-AUDIT-05 logs → Who, when, what?
2. Verify SOP-DEPEND-06 → Was this operation expected?
3. Check SOP-MONITOR-08 metrics → Anything abnormal?
4. Check SOP-VALID-07 rules → Did it violate SOP?
5. Take corrective action (rollback via SOP-RECOVERY-04)
```

---

## Configuration Files

Layer 3 uses several YAML configuration files:

| File | Purpose | Created By |
|------|---------|------------|
| `data/audit/events.jsonl` | Real-time audit events (append-only) | SOP-AUDIT-05 |
| `data/audit/digests/*.json` | Daily sealed digests | SOP-AUDIT-05 |
| `data/dependencies/DEPENDENCY_GRAPH.yaml` | Script relationships | SOP-DEPEND-06 |
| `data/validation/VALIDATION_RULES.yaml` | 47+ validation rules | SOP-VALID-07 |
| `data/monitoring/ALERT_CONFIG.yaml` | Alert thresholds | SOP-MONITOR-08 |
| `data/metrics/YYYY-MM-DD-metrics.json` | Daily metric snapshots | SOP-MONITOR-08 |

---

## Automation & Scheduling

### Automated Processes

| Process | Frequency | SOP | Trigger |
|---------|-----------|-----|---------|
| Audit event logging | Real-time | SOP-AUDIT-05 | Every script execution |
| Dependency validation | On-demand | SOP-DEPEND-06 | Before script execution |
| Pre/post-execution validation | On-demand | SOP-VALID-07 | SOP-SCRIPT-01 |
| Continuous validation (TIER 3) | Hourly/daily/weekly | SOP-VALID-07 | Cron scheduler |
| Metrics collection | Hourly | SOP-MONITOR-08 | Cron scheduler |
| Alert checking | Every 30 min | SOP-MONITOR-08 | Cron scheduler |
| Dashboard generation | Hourly | SOP-MONITOR-08 | Cron scheduler |
| Audit log cleanup | Weekly | SOP-AUDIT-05 | Cron scheduler |
| Backup cleanup | Weekly | SOP-RECOVERY-04 | Cron scheduler |

---

## Compliance & Governance

### Quarterly Review Checklist

```
☐ Review all 4 Layer 3 SOPs for updates needed
☐ Audit operational metrics (success rates, error rates)
☐ Validate dependency graph accuracy
☐ Run full system validation (SOP-VALID-07 TIER 4)
☐ Analyze audit log for patterns/anomalies
☐ Update monitoring rules and thresholds
☐ Generate compliance report
☐ Document lessons learned
☐ Plan improvements for next quarter
```

### Annual Review

- Full audit of all 3 layers
- Performance analysis (throughput, reliability)
- Capacity planning (growth trajectory)
- Security review (audit log integrity)
- Disaster recovery drill

---

## Success Metrics

**Layer 3 is working when:**

✅ Scripts log every execution (SOP-AUDIT-05)
✅ Audit logs show complete history of changes
✅ Dependencies tracked and validated automatically
✅ Validation rules catch 95%+ of issues before they impact users
✅ Alerts notify team within 5 minutes of critical issues
✅ System recovers from failures automatically (SOP-RECOVERY-04)
✅ Trends show stable/improving operational metrics
✅ Zero unplanned downtime due to data corruption

---

## Next Steps

1. **Immediate (Week 1):**
   - [ ] Review all 4 SOPs
   - [ ] Create audit infrastructure
   - [ ] Enable pre-commit validation

2. **Short-term (Week 2-3):**
   - [ ] Document all 69 scripts' dependencies
   - [ ] Create validation rules
   - [ ] Schedule monitoring cron jobs

3. **Medium-term (Month 1-2):**
   - [ ] Accumulate audit trail data
   - [ ] Build trend analysis
   - [ ] Refine alert thresholds based on data

4. **Ongoing:**
   - [ ] Monitor metrics daily
   - [ ] Respond to alerts immediately
   - [ ] Review logs weekly
   - [ ] Quarterly compliance review

---

## FAQ

**Q: Do I need to implement all of Layer 3 at once?**
A: No. Start with SOP-AUDIT-05 (logging), then SOP-VALID-07 (validation), then the others. But eventually all 4 are needed for complete observability.

**Q: How much overhead does Layer 3 add?**
A: ~5% performance impact from logging and validation. Small price for complete visibility.

**Q: What if I find an issue in the middle of an operation?**
A: SOP-VALID-07 catches it (TIER 2 post-execution validation), SOP-RECOVER-04 restores from backup.

**Q: How long do I keep audit logs?**
A: 30 days (real-time), 1 year (daily digests), permanent (git).

---

*Layer 3: Infrastructure SOP | Version 1.0 | 2026-01-15*
*Complete EBF Operations Stack: Layer 1 (User) + Layer 2 (Ops) + Layer 3 (Infrastructure) = Fully Observable, Self-Healing System*
