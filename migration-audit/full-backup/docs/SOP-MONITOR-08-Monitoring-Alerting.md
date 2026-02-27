# SOP-MONITOR-08: Monitoring & Alerting System

> **Version:** 1.0 | **Protocol:** HHH-MONITOR-1 | **Date:** 2026-01-15
>
> **Purpose:** Real-time system monitoring and incident alerting

---

## 1. Monitoring Architecture

### What We Monitor

```
┌─────────────────────────────────────────────────────┐
│ CATEGORY 1: Operational Health                      │
│ • Script execution success rates                    │
│ • Average execution time                            │
│ • Failed validations                                │
│ • Backup creation and verification                  │
│ • Audit log integrity                               │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ CATEGORY 2: Data Integrity                          │
│ • Index consistency (4-location sync)               │
│ • Code conflict detection                           │
│ • Orphaned/ghost file detection                     │
│ • Cross-reference validity                          │
│ • Duplicate entry detection                         │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ CATEGORY 3: Resource Utilization                    │
│ • Disk space (audit logs, backups)                  │
│ • Memory usage during script execution              │
│ • File count growth (risk assessment)               │
│ • Database size                                     │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ CATEGORY 4: Security & Compliance                   │
│ • Unauthorized file access attempts                 │
│ • Audit log tampering detection                     │
│ • SOP compliance violations                         │
│ • Cryptographic verification failures               │
│ • Missing pre/post-condition validations            │
└─────────────────────────────────────────────────────┘
```

---

## 2. Metrics Definition

### Operational Metrics

```yaml
metrics:

  # Execution metrics
  script_execution_success_rate:
    unit: "percentage (0-100%)"
    calculation: "successful_executions / total_executions * 100"
    alert_threshold: "< 95%"
    description: "Percentage of scripts that complete successfully"
    sop_reference: "SOP-SCRIPT-01"

  script_execution_duration:
    unit: "seconds"
    calculation: "median(execution_times) per script"
    alert_threshold: "> 2x baseline"
    description: "How long scripts take to execute"
    trend: "should be stable; increase indicates performance degradation"

  validation_failure_rate:
    unit: "percentage"
    calculation: "failed_validations / total_validations * 100"
    alert_threshold: "> 5%"
    description: "Rate of validation rule failures"
    sop_reference: "SOP-VALID-07"

  # Data integrity metrics
  index_consistency_score:
    unit: "percentage (0-100%)"
    calculation: "1.0 if (loc1==loc2==loc3==loc4) else 0.0"
    alert_threshold: "< 100%"
    description: "Whether all 4 index locations are synchronized"
    sop_reference: "SOP-INDEX-03"
    critical: true

  code_conflict_count:
    unit: "count"
    calculation: "number of codes assigned 2+ times"
    alert_threshold: "> 0"
    description: "Number of code conflicts detected"
    sop_reference: "SOP-APPEND-02"
    critical: true

  orphaned_file_count:
    unit: "count"
    calculation: "files_in_filesystem - files_in_index"
    alert_threshold: "> 0"
    description: "Number of orphaned files"
    sop_reference: "SOP-INDEX-03"
    critical: true

  # Resource metrics
  audit_log_size:
    unit: "megabytes"
    calculation: "size(data/audit/events.jsonl)"
    alert_threshold: "> 1000 MB (needs cleanup)"
    description: "Size of real-time audit log"
    action_when_triggered: "Run SOP-AUDIT-05 cleanup"

  backup_coverage:
    unit: "days"
    calculation: "number of backup slots filled / total slots * 100"
    alert_threshold: "< 95%"
    description: "Percentage of backup slots that have data"
    sop_reference: "SOP-RECOVERY-04"
    critical: true

  # Compliance metrics
  appendix_compliance_score:
    unit: "percentage (0-100%)"
    calculation: "average compliance score across all appendices"
    alert_threshold: "< 85%"
    description: "Template compliance for all appendices"
    sop_reference: "SOP-APPEND-02"

  chapter_compliance_score:
    unit: "percentage (0-100%)"
    calculation: "average compliance score across all chapters"
    alert_threshold: "< 85%"
    description: "Template compliance for all chapters"
    sop_reference: "CLAUDE.md"

  sop_compliance_violations:
    unit: "count"
    calculation: "number of operations not following SOP pattern"
    alert_threshold: "> 0"
    description: "SOP violations detected"
```

---

## 3. MetricsCollector Implementation

```python
#!/usr/bin/env python3
"""
MetricsCollector: Gather operational metrics
"""

import json
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict

class MetricsCollector:
    """Collect and store operational metrics"""

    def __init__(self, metrics_dir="data/metrics"):
        self.metrics_dir = Path(metrics_dir)
        self.metrics_dir.mkdir(parents=True, exist_ok=True)
        self.current_metrics = {}

    def collect_all_metrics(self):
        """Gather all metrics from system"""
        self.current_metrics = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "operational": self._collect_operational_metrics(),
            "integrity": self._collect_integrity_metrics(),
            "resources": self._collect_resource_metrics(),
            "compliance": self._collect_compliance_metrics()
        }

        # Save metrics snapshot
        self._save_metrics_snapshot()

        return self.current_metrics

    def _collect_operational_metrics(self):
        """Collect script execution and validation metrics"""
        from audit_logger import AuditLogger

        logger = AuditLogger()
        today = datetime.now(timezone.utc).date()

        # Query today's script executions
        events = logger.query_events(
            category="SCRIPT",
            date_from=str(today),
            limit=1000
        )

        if not events:
            return {
                "script_success_rate": None,
                "avg_execution_time": None,
                "scripts_executed_today": 0
            }

        successful = sum(1 for e in events
                        if e["execution"]["status"] == "SUCCESS")
        total = len(events)
        avg_duration = sum(e["execution"].get("duration_seconds", 0)
                          for e in events) / len(events) if events else 0

        return {
            "script_success_rate": (successful / total * 100) if total > 0 else 0,
            "avg_execution_time": avg_duration,
            "scripts_executed_today": total,
            "successful": successful,
            "failed": total - successful
        }

    def _collect_integrity_metrics(self):
        """Collect data integrity metrics"""
        from audit_logger import AuditLogger

        metrics = {}

        # Index consistency
        try:
            from appendix_index_manager import AppendixIndexManager
            manager = AppendixIndexManager()
            manager.validate_all_locations()
            metrics["index_consistency"] = 100
        except:
            metrics["index_consistency"] = 0

        # Code conflicts
        try:
            import yaml
            registry = yaml.safe_load(
                open("APPENDIX_CODE_REGISTRY.yaml"))
            conflicts = [c for c in registry["code_registry"].values()
                        if c.get("status") == "CONFLICT"]
            metrics["code_conflict_count"] = len(conflicts)
        except:
            metrics["code_conflict_count"] = None

        # Orphaned files
        try:
            files = set(Path("appendices").glob("*.tex"))
            # Would need to parse index
            metrics["orphaned_file_count"] = 0  # Placeholder
        except:
            metrics["orphaned_file_count"] = None

        return metrics

    def _collect_resource_metrics(self):
        """Collect resource utilization metrics"""
        metrics = {}

        # Audit log size
        audit_log = Path("data/audit/events.jsonl")
        metrics["audit_log_size_mb"] = (
            audit_log.stat().st_size / (1024 * 1024)
            if audit_log.exists() else 0
        )

        # Backup coverage
        backup_dir = Path("data/backups")
        if backup_dir.exists():
            backups = list(backup_dir.glob("*.BACKUP.*"))
            metrics["backup_count"] = len(backups)
        else:
            metrics["backup_count"] = 0

        # Total file count
        metrics["appendix_file_count"] = len(
            list(Path("appendices").glob("*.tex")))
        metrics["chapter_file_count"] = len(
            list(Path("chapters").glob("*.tex")))

        return metrics

    def _collect_compliance_metrics(self):
        """Collect compliance metrics"""
        from pathlib import Path
        import subprocess

        metrics = {}

        # Appendix compliance
        try:
            result = subprocess.run(
                ["python", "scripts/check_template_compliance.py",
                 "appendices/", "--batch"],
                capture_output=True, text=True
            )
            # Parse output to get average score
            metrics["appendix_compliance_avg"] = 87.5  # Placeholder
        except:
            metrics["appendix_compliance_avg"] = None

        # SOP compliance
        metrics["sop_violations"] = 0  # Would be tracked by validation

        return metrics

    def _save_metrics_snapshot(self):
        """Save metrics snapshot for history"""
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        snapshot_file = self.metrics_dir / f"{timestamp}-metrics.json"

        with open(snapshot_file, 'w') as f:
            json.dump(self.current_metrics, f, indent=2)

    def get_metric_trend(self, metric_name, days=30):
        """Get trend for a metric over N days"""
        snapshots = sorted(self.metrics_dir.glob("*-metrics.json"))[-days:]
        values = []

        for snapshot in snapshots:
            with open(snapshot, 'r') as f:
                data = json.load(f)
                # Navigate to metric value
                value = self._extract_metric(data, metric_name)
                if value is not None:
                    values.append({
                        "date": snapshot.stem.split("-")[0],
                        "value": value
                    })

        return values

    def _extract_metric(self, data, metric_name):
        """Navigate nested dict to find metric value"""
        keys = metric_name.split(".")
        current = data
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return None
        return current
```

---

## 4. AlertingSystem Implementation

```python
#!/usr/bin/env python3
"""
AlertingSystem: Trigger alerts based on metrics
"""

import smtplib
from email.mime.text import MIMEText
from datetime import datetime

class AlertingSystem:
    """Generate and send alerts based on metrics"""

    def __init__(self, config_file="data/monitoring/ALERT_CONFIG.yaml"):
        import yaml
        with open(config_file, 'r') as f:
            self.config = yaml.safe_load(f)

    def check_metrics(self, metrics):
        """
        Check metrics against thresholds and generate alerts.

        Args:
            metrics: dict from MetricsCollector.collect_all_metrics()

        Returns:
            list of Alert objects
        """
        alerts = []

        # Define threshold checks
        checks = {
            "script_success_rate": {
                "path": "operational.script_success_rate",
                "threshold": 95,
                "operator": "<",
                "severity": "HIGH",
                "message": "Script success rate below 95%"
            },
            "index_consistency": {
                "path": "integrity.index_consistency",
                "threshold": 100,
                "operator": "<",
                "severity": "CRITICAL",
                "message": "Index locations are out of sync!"
            },
            "code_conflicts": {
                "path": "integrity.code_conflict_count",
                "threshold": 0,
                "operator": ">",
                "severity": "CRITICAL",
                "message": "Code conflicts detected"
            },
            "orphaned_files": {
                "path": "integrity.orphaned_file_count",
                "threshold": 0,
                "operator": ">",
                "severity": "HIGH",
                "message": "Orphaned files detected"
            },
            "audit_log_size": {
                "path": "resources.audit_log_size_mb",
                "threshold": 1000,
                "operator": ">",
                "severity": "MEDIUM",
                "message": "Audit log too large, cleanup recommended"
            },
            "backup_coverage": {
                "path": "resources.backup_count",
                "threshold": 5,
                "operator": "<",
                "severity": "HIGH",
                "message": "Insufficient backup coverage"
            }
        }

        # Check each threshold
        for check_name, check in checks.items():
            value = self._extract_value(metrics, check["path"])

            if value is not None:
                triggered = self._evaluate(value, check["operator"],
                                           check["threshold"])

                if triggered:
                    alert = Alert(
                        check_name=check_name,
                        severity=check["severity"],
                        message=check["message"],
                        value=value,
                        threshold=check["threshold"],
                        timestamp=datetime.now()
                    )
                    alerts.append(alert)

        return alerts

    def _extract_value(self, data, path):
        """Navigate nested dict using dot notation"""
        keys = path.split(".")
        current = data
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return None
        return current

    def _evaluate(self, value, operator, threshold):
        """Evaluate if threshold is triggered"""
        if operator == "<":
            return value < threshold
        elif operator == ">":
            return value > threshold
        elif operator == "==":
            return value == threshold
        else:
            return False

    def send_alerts(self, alerts):
        """Send alerts via configured channels"""
        for alert in alerts:
            # Log to audit trail
            from audit_logger import AuditLogger
            logger = AuditLogger()
            logger.log_event(
                category="MONITORING",
                operation="ALERT",
                target={"type": "METRIC", "path": alert.check_name},
                metadata={
                    "severity": alert.severity,
                    "value": alert.value,
                    "threshold": alert.threshold
                }
            )

            # Send notifications
            if alert.severity == "CRITICAL":
                self._send_email(alert)
                self._send_slack(alert)
                self._write_alert_log(alert)
            elif alert.severity == "HIGH":
                self._write_alert_log(alert)
                self._send_slack(alert)
            else:
                self._write_alert_log(alert)

    def _send_email(self, alert):
        """Send email alert"""
        smtp = smtplib.SMTP(self.config["smtp"]["server"],
                           self.config["smtp"]["port"])

        msg = MIMEText(alert.format_message())
        msg["Subject"] = f"[{alert.severity}] System Alert: {alert.check_name}"
        msg["From"] = self.config["email"]["from"]
        msg["To"] = self.config["email"]["to"]

        smtp.send_message(msg)
        smtp.quit()

    def _send_slack(self, alert):
        """Send Slack notification"""
        import requests

        color = {
            "CRITICAL": "danger",
            "HIGH": "warning",
            "MEDIUM": "good"
        }.get(alert.severity, "good")

        payload = {
            "attachments": [{
                "color": color,
                "title": f"{alert.severity}: {alert.check_name}",
                "text": alert.format_message(),
                "ts": int(alert.timestamp.timestamp())
            }]
        }

        requests.post(self.config["slack"]["webhook"], json=payload)

    def _write_alert_log(self, alert):
        """Write alert to log file"""
        log_file = Path("data/monitoring/alerts.log")
        log_file.parent.mkdir(parents=True, exist_ok=True)

        with open(log_file, 'a') as f:
            f.write(f"{alert.timestamp.isoformat()}: {alert.severity} - "
                   f"{alert.check_name}: {alert.message} (value={alert.value})\n")


class Alert:
    """Alert object"""

    def __init__(self, check_name, severity, message, value, threshold,
                 timestamp):
        self.check_name = check_name
        self.severity = severity
        self.message = message
        self.value = value
        self.threshold = threshold
        self.timestamp = timestamp

    def format_message(self):
        """Format alert message for notifications"""
        return f"""
        Alert: {self.check_name}
        Severity: {self.severity}
        Message: {self.message}
        Current Value: {self.value}
        Threshold: {self.threshold}
        Timestamp: {self.timestamp.isoformat()}
        """
```

---

## 5. Dashboard Implementation

### HTML Dashboard

**File:** `outputs/system-dashboard.html` (generated hourly)

```html
<!DOCTYPE html>
<html>
<head>
    <title>EBF System Dashboard</title>
    <style>
        body { font-family: monospace; background: #1e1e1e; color: #fff; }
        .metric-box { border: 1px solid #444; padding: 10px; margin: 5px; }
        .healthy { background: #2d7d2d; }
        .warning { background: #8d7d2d; }
        .critical { background: #8d2d2d; }
        .chart { width: 100%; height: 300px; }
    </style>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <h1>EBF System Dashboard</h1>
    <p>Generated: <span id="generated-time"></span></p>

    <h2>Operational Health</h2>
    <div class="metric-box healthy" id="success-rate"></div>
    <div class="metric-box" id="execution-time"></div>

    <h2>Data Integrity</h2>
    <div class="metric-box" id="index-consistency"></div>
    <div class="metric-box" id="code-conflicts"></div>

    <h2>Active Alerts</h2>
    <div id="alerts-list"></div>

    <h2>Trends (30 days)</h2>
    <canvas class="chart" id="trends-chart"></canvas>

    <script>
        // Load metrics and render dashboard
        fetch('/api/metrics')
            .then(r => r.json())
            .then(metrics => {
                document.getElementById('generated-time').textContent =
                    new Date().toISOString();

                // Render metrics boxes
                renderMetrics(metrics);

                // Render alerts
                renderAlerts(metrics.alerts);

                // Render trends
                renderTrends(metrics.trends);
            });
    </script>
</body>
</html>
```

---

## 6. Monitoring Schedule

### Cron Jobs

```bash
# /etc/cron.d/monitoring-schedule

# Collect metrics every hour
0  * * * * root python3 /scripts/collect_metrics.py

# Check alerts every 30 minutes
*/30 * * * * root python3 /scripts/check_alerts.py

# Generate dashboard hourly
5  * * * * root python3 /scripts/generate_dashboard.py

# Daily summary report
0  8 * * * root python3 /scripts/generate_daily_report.py

# Weekly deep analysis
0  9 * * 1 root python3 /scripts/generate_weekly_analysis.py
```

---

## 7. Incident Response Integration

When alert triggers:

```python
# SOP-MONITOR-08 → SOP-RECOVERY-04 (if needed)

alert = Alert(..., severity="CRITICAL", check_name="index_consistency")

if alert.check_name == "index_consistency":
    # This is a data integrity issue
    # Trigger SOP-RECOVERY-04 recovery
    from backup_manager import BackupManager

    manager = BackupManager()
    manager.restore("appendices/00_appendix_index.tex")

    # Log incident
    logger.log_event(
        category="INCIDENT_RESPONSE",
        operation="RECOVER",
        target={"type": "FILE", "path": "appendices/00_appendix_index.tex"},
        metadata={"triggered_by_alert": alert.check_name}
    )
```

---

## 8. Checklist: Monitoring System

```
☐ MetricsCollector class implemented
☐ Metric definitions documented (YAML)
☐ AlertingSystem class implemented
☐ Alert thresholds configured
☐ Email/Slack integration active
☐ HTML dashboard generation working
☐ Cron jobs scheduled
☐ Alert log file created
☐ Incident response integration
☐ Trend analysis working
☐ Monthly health reports generated
```

---

*SOP-MONITOR-08: Monitoring & Alerting | Version: 1.0 | Date: 2026-01-15 | Protocol: HHH-MONITOR-1*
