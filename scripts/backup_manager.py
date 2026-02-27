#!/usr/bin/env python3
"""
BackupManager: Backup and recovery system

Implements SOP-RECOVERY-04: Backup, Recovery & Rollback Protocol
- TIER 1: Operation-level backups (7-day retention)
- TIER 2: Daily checkpoint (30-day retention)
- TIER 3: Archive (4 weeks + 3 months)

Usage:
    manager = BackupManager()

    # Create backup before modification
    backup_path = manager.create_backup("appendices/00_appendix_index.tex")

    # Later, restore if needed
    manager.restore("appendices/00_appendix_index.tex", backup_path)
"""

import shutil
import tarfile
import gzip
import os
from pathlib import Path
from datetime import datetime, timezone, timedelta


class BackupManager:
    """Manage backups across 3-tier system"""

    def __init__(self, backup_dir="data/backups"):
        """Initialize backup system"""
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)

        # Create tier directories
        self.tier1_dir = self.backup_dir / "tier1"
        self.tier2_dir = self.backup_dir / "tier2"
        self.tier3_dir = self.backup_dir / "tier3"

        for d in [self.tier1_dir, self.tier2_dir, self.tier3_dir]:
            d.mkdir(exist_ok=True)

        self.timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")

    def create_backup(self, filepath):
        """
        Create backup of single file (TIER 1: Operation-level).

        Args:
            filepath: Path to file to backup

        Returns:
            Path to backup file
        """
        filepath = Path(filepath)

        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")

        # Naming: FILENAME.BACKUP.TIMESTAMP.EXT
        backup_name = (f"{filepath.stem}.BACKUP."
                      f"{self.timestamp}.{filepath.suffix}")
        backup_path = self.tier1_dir / backup_name

        # Copy file
        shutil.copy2(filepath, backup_path)

        # Verify backup
        if not backup_path.exists():
            raise IOError(f"Backup failed: {backup_path}")

        return backup_path

    def create_scope_backup(self, scope_dirs=None):
        """
        Create backup of entire scope (TIER 2: Daily checkpoint).

        Args:
            scope_dirs: List of directories to backup (default: ['appendices', 'chapters', 'data'])

        Returns:
            Path to backup tar.gz file
        """
        if scope_dirs is None:
            scope_dirs = ['appendices', 'chapters', 'data']

        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        backup_name = f"scope-backup-{today}.tar.gz"
        backup_path = self.tier2_dir / backup_name

        # Create tar.gz
        with tarfile.open(backup_path, "w:gz") as tar:
            for dir_name in scope_dirs:
                dir_path = Path(dir_name)
                if dir_path.exists():
                    tar.add(dir_path, arcname=dir_path.name)

        # Verify backup
        if not backup_path.exists():
            raise IOError(f"Scope backup failed: {backup_path}")

        return backup_path

    def restore(self, original_filepath, backup_filepath=None):
        """
        Restore file from backup.

        Args:
            original_filepath: Path to file to restore
            backup_filepath: Specific backup to restore from (default: latest)

        Returns:
            True if successful
        """
        original_path = Path(original_filepath)

        # Find latest backup if not specified
        if backup_filepath is None:
            backups = sorted(self.tier1_dir.glob(
                f"{original_path.stem}.BACKUP.*.{original_path.suffix}"))
            if not backups:
                raise FileNotFoundError(f"No backups found for {original_filepath}")
            backup_filepath = backups[-1]
        else:
            backup_filepath = Path(backup_filepath)

        if not backup_filepath.exists():
            raise FileNotFoundError(f"Backup not found: {backup_filepath}")

        # Restore
        shutil.copy2(backup_filepath, original_path)

        # Verify
        if not original_path.exists():
            raise IOError(f"Restore failed: {original_path}")

        return True

    def cleanup_old_backups(self, max_age_days=7):
        """
        Remove TIER 1 backups older than max_age_days.

        Args:
            max_age_days: Maximum age in days
        """
        cutoff = datetime.now(timezone.utc) - timedelta(days=max_age_days)

        for backup_file in self.tier1_dir.glob("*.BACKUP.*"):
            # Extract timestamp from filename
            try:
                timestamp_str = backup_file.stem.split(".BACKUP.")[1]
                backup_time = datetime.strptime(timestamp_str, "%Y%m%d-%H%M%S")
                backup_time = backup_time.replace(tzinfo=timezone.utc)

                if backup_time < cutoff:
                    backup_file.unlink()
            except:
                pass

    def verify_backup(self, backup_filepath):
        """
        Verify backup file is readable and valid.

        Args:
            backup_filepath: Path to backup to verify

        Returns:
            True if valid, False if corrupted
        """
        backup_path = Path(backup_filepath)

        if not backup_path.exists():
            return False

        try:
            # Try to read file to verify integrity
            with open(backup_path, 'rb') as f:
                f.read(1024)  # Read first 1KB
            return True
        except:
            return False

    def get_backup_stats(self):
        """Get statistics about backup system"""
        tier1_size = sum(f.stat().st_size for f in self.tier1_dir.glob("*"))
        tier2_size = sum(f.stat().st_size for f in self.tier2_dir.glob("*"))
        tier3_size = sum(f.stat().st_size for f in self.tier3_dir.glob("*"))

        return {
            "tier1_count": len(list(self.tier1_dir.glob("*"))),
            "tier1_size_mb": tier1_size / (1024 * 1024),
            "tier2_count": len(list(self.tier2_dir.glob("*"))),
            "tier2_size_mb": tier2_size / (1024 * 1024),
            "tier3_count": len(list(self.tier3_dir.glob("*"))),
            "tier3_size_mb": tier3_size / (1024 * 1024),
            "total_size_mb": (tier1_size + tier2_size + tier3_size) / (1024 * 1024)
        }


if __name__ == "__main__":
    # Test backup system
    manager = BackupManager()

    # Test: Create a test file
    test_file = Path("test_backup.txt")
    test_file.write_text("Test content")

    try:
        # Create backup
        backup = manager.create_backup("test_backup.txt")
        print(f"✓ Backup created: {backup}")

        # Modify original
        test_file.write_text("Modified content")

        # Restore
        manager.restore("test_backup.txt", backup)
        restored_content = test_file.read_text()
        print(f"✓ Restored: {restored_content}")

        # Stats
        stats = manager.get_backup_stats()
        print(f"✓ Backup stats: {stats}")

    finally:
        # Cleanup
        test_file.unlink(missing_ok=True)
