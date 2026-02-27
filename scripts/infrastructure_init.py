#!/usr/bin/env python3
"""
Infrastructure initialization script

Initializes all Layer 2/3 infrastructure:
- Creates required directories
- Initializes audit logging system
- Creates backup manager
- Sets up dependency graph
- Initializes metrics system
- Tests all components

Usage:
    python3 scripts/infrastructure_init.py
"""

import sys
from pathlib import Path
from datetime import datetime

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from audit_logger import AuditLogger
from backup_manager import BackupManager
from dependency_graph import DependencyGraph
from metrics_collector import MetricsCollector


def main():
    """Initialize infrastructure"""
    print("=" * 70)
    print("EBF Infrastructure Initialization")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()

    try:
        # Step 1: Create directories
        print("📁 Creating directories...")
        directories = [
            "data/audit",
            "data/audit/digests",
            "data/backups",
            "data/backups/tier1",
            "data/backups/tier2",
            "data/backups/tier3",
            "data/metrics",
            "data/monitoring",
            "data/dependencies",
            "data/validation",
            "logs"
        ]

        for dir_name in directories:
            path = Path(dir_name)
            path.mkdir(parents=True, exist_ok=True)
        print(f"   ✓ Created {len(directories)} directories")

        # Step 2: Initialize audit logging
        print()
        print("📝 Initializing audit logging (SOP-AUDIT-05)...")
        logger = AuditLogger()

        init_event = logger.log_event(
            category="INFRASTRUCTURE",
            operation="INIT",
            target={"type": "SYSTEM", "path": "audit_logging"},
            actor={"type": "SYSTEM", "identifier": "infrastructure_init"},
            execution={"status": "SUCCESS", "exit_code": 0}
        )
        print(f"   ✓ Audit logger initialized (event: {init_event})")

        # Step 3: Initialize backup manager
        print()
        print("💾 Initializing backup system (SOP-RECOVERY-04)...")
        backup_mgr = BackupManager()
        stats = backup_mgr.get_backup_stats()
        print(f"   ✓ Backup manager initialized")
        print(f"     TIER 1: {stats['tier1_count']} backups, {stats['tier1_size_mb']:.1f}MB")
        print(f"     TIER 2: {stats['tier2_count']} backups, {stats['tier2_size_mb']:.1f}MB")
        print(f"     TIER 3: {stats['tier3_count']} backups, {stats['tier3_size_mb']:.1f}MB")

        # Step 4: Initialize dependency graph
        print()
        print("🔗 Initializing dependency graph (SOP-DEPEND-06)...")
        dep_graph = DependencyGraph()

        # Check if graph exists
        if dep_graph.graph_file.exists():
            script_count = len(dep_graph.scripts)
            print(f"   ✓ Dependency graph loaded ({script_count} scripts)")

            # Validate
            issues = dep_graph.validate_dependencies()
            if not issues:
                print(f"   ✓ All dependencies valid")
            else:
                print(f"   ⚠️  {len(issues)} dependency issues found:")
                for issue in issues[:3]:  # Show first 3
                    print(f"      - {issue}")
        else:
            print(f"   ℹ️  Dependency graph not yet created")
            print(f"      See: docs/operations/SOP-DEPEND-06.md")

        # Step 5: Initialize metrics
        print()
        print("📊 Initializing metrics system (SOP-MONITOR-08)...")
        collector = MetricsCollector()
        metrics = collector.collect_all_metrics()
        health = collector.get_health_status()

        print(f"   ✓ Metrics collected")
        print(f"     Overall status: {health['overall_status']}")
        print(f"     Components checked: {len(health['components'])}")

        # Step 6: Summary
        print()
        print("=" * 70)
        print("✅ Infrastructure Initialization Complete!")
        print("=" * 70)
        print()
        print("📚 Next Steps:")
        print("  1. Review the SOPs in: docs/operations/")
        print("  2. Create dependency graph: docs/operations/SOP-DEPEND-06.md")
        print("  3. Setup cron jobs: bash docs/operations/CRON-JOBS-SETUP.sh")
        print("  4. Integrate with CLAUDE.md: docs/operations/INTEGRATION-GUIDE.md")
        print()
        print("🎯 Key Features:")
        print("  • Immutable audit trails (SOP-AUDIT-05)")
        print("  • 3-tier backup system (SOP-RECOVERY-04)")
        print("  • Dependency validation (SOP-DEPEND-06)")
        print("  • Real-time monitoring (SOP-MONITOR-08)")
        print()
        print("📖 Documentation:")
        print("  • Layer 2 Handbook: docs/operations/README.md")
        print("  • Layer 3 Handbook: docs/operations/LAYER3-README.md")
        print("  • Complete Summary: docs/operations/00-OPERATIONAL-FRAMEWORK-COMPLETE.md")
        print()

        return 0

    except Exception as e:
        print(f"✗ Initialization error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
