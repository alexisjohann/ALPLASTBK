#!/usr/bin/env python3
"""
Cron Job: Daily backup of entire scope (TIER 2)

Creates daily checkpoint snapshot of appendices, chapters, and data.
Designed to be executed daily via cron:
  0 2 * * * cd /path/to/repo && python3 scripts/run_daily_backup.py

Usage:
    python3 scripts/run_daily_backup.py
"""

import sys
from pathlib import Path
from datetime import datetime

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from backup_manager import BackupManager
from audit_logger import AuditLogger


def main():
    """Run daily backup"""
    print(f"[{datetime.now().isoformat()}] Starting daily backup...")

    try:
        manager = BackupManager()

        # Create scope backup (TIER 2)
        scope_dirs = ['appendices', 'chapters', 'data']
        backup_path = manager.create_scope_backup(scope_dirs)
        print(f"✓ Scope backup created: {backup_path}")

        # Get backup stats
        stats = manager.get_backup_stats()
        print(f"✓ Backup stats:")
        print(f"   TIER 1: {stats['tier1_count']} files, {stats['tier1_size_mb']:.1f} MB")
        print(f"   TIER 2: {stats['tier2_count']} files, {stats['tier2_size_mb']:.1f} MB")
        print(f"   Total: {stats['total_size_mb']:.1f} MB")

        # Cleanup old TIER 1 backups (keep 7 days)
        manager.cleanup_old_backups(max_age_days=7)
        print(f"✓ Cleaned up old TIER 1 backups")

        # Log backup event
        logger = AuditLogger()
        logger.log_event(
            category="BACKUP",
            operation="CREATE",
            target={
                "type": "SCOPE_BACKUP",
                "path": str(backup_path),
                "scope": scope_dirs
            },
            execution={
                "status": "SUCCESS",
                "exit_code": 0,
                "duration_seconds": 0  # Would be actual duration
            },
            metadata={
                "backup_size_mb": stats['total_size_mb'],
                "tier": 2,
                "retention_days": 30
            }
        )

        print(f"✓ Daily backup complete")
        return 0

    except Exception as e:
        print(f"✗ Backup error: {e}")

        logger = AuditLogger()
        logger.log_event(
            category="BACKUP",
            operation="CREATE",
            target={"type": "SCOPE_BACKUP", "path": "unknown"},
            execution={
                "status": "FAILURE",
                "exit_code": 1,
                "error": str(e)
            }
        )

        return 1


if __name__ == "__main__":
    sys.exit(main())
