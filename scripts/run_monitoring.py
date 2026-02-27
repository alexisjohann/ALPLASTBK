#!/usr/bin/env python3
"""
Cron Job: Hourly monitoring and alerting

Runs metrics collection and checks thresholds.
Designed to be executed hourly via cron:
  0 * * * * cd /path/to/repo && python3 scripts/run_monitoring.py

Usage:
    python3 scripts/run_monitoring.py
"""

import sys
from pathlib import Path
from datetime import datetime

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from metrics_collector import MetricsCollector
from audit_logger import AuditLogger


def main():
    """Run hourly monitoring"""
    print(f"[{datetime.now().isoformat()}] Starting monitoring job...")

    try:
        # Collect metrics
        collector = MetricsCollector()
        metrics = collector.collect_all_metrics()
        print(f"✓ Metrics collected")

        # Get health status
        health = collector.get_health_status()
        print(f"✓ System health: {health['overall_status']}")

        # Check for alerts
        alerts = check_thresholds(metrics)
        if alerts:
            print(f"⚠️  {len(alerts)} alerts triggered:")
            for alert in alerts:
                print(f"   - {alert['name']}: {alert['message']}")
                log_alert(alert)
        else:
            print(f"✓ All thresholds normal")

        # Log monitoring event
        logger = AuditLogger()
        logger.log_event(
            category="MONITORING",
            operation="MONITOR",
            target={"type": "SYSTEM", "path": "metrics"},
            execution={
                "status": "SUCCESS",
                "exit_code": 0
            },
            metadata={
                "overall_status": health["overall_status"],
                "alerts": len(alerts)
            }
        )

        print(f"✓ Monitoring job complete")
        return 0

    except Exception as e:
        print(f"✗ Monitoring error: {e}")
        logger = AuditLogger()
        logger.log_event(
            category="MONITORING",
            operation="MONITOR",
            target={"type": "SYSTEM", "path": "metrics"},
            execution={
                "status": "FAILURE",
                "exit_code": 1,
                "error": str(e)
            }
        )
        return 1


def check_thresholds(metrics):
    """
    Check metrics against thresholds.

    Returns:
        List of triggered alerts
    """
    alerts = []

    # Critical thresholds
    thresholds = [
        {
            "path": "integrity.index_consistency",
            "name": "Index Consistency",
            "condition": lambda v: v < 100,
            "message": "Index locations out of sync"
        },
        {
            "path": "integrity.code_conflict_count",
            "name": "Code Conflicts",
            "condition": lambda v: v > 0,
            "message": "Code conflicts detected"
        },
        {
            "path": "resources.audit_log_size_mb",
            "name": "Audit Log Size",
            "condition": lambda v: v > 1000,
            "message": "Audit log exceeds 1GB (cleanup recommended)"
        },
        {
            "path": "resources.backup_count",
            "name": "Backup Coverage",
            "condition": lambda v: v < 5,
            "message": "Insufficient backups"
        }
    ]

    for threshold in thresholds:
        value = get_metric(metrics, threshold["path"])
        if value is not None and threshold["condition"](value):
            alerts.append({
                "name": threshold["name"],
                "message": threshold["message"],
                "value": value,
                "path": threshold["path"],
                "severity": "HIGH"
            })

    return alerts


def get_metric(data, path):
    """Get metric from nested dict using dot notation"""
    keys = path.split(".")
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return None
    return current


def log_alert(alert):
    """Log alert to file"""
    alert_file = Path("data/monitoring/alerts.log")
    alert_file.parent.mkdir(parents=True, exist_ok=True)

    with open(alert_file, 'a') as f:
        timestamp = datetime.now().isoformat()
        f.write(f"{timestamp}: {alert['severity']} - "
               f"{alert['name']}: {alert['message']} "
               f"(value={alert['value']})\n")


if __name__ == "__main__":
    sys.exit(main())
