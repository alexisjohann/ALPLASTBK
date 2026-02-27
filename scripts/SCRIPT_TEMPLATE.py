#!/usr/bin/env python3
"""
MANDATORY TEMPLATE FOR ALL SCRIPTS IN EBF

Every script must follow this structure to comply with SOP-SCRIPT-01.
This template enforces:
- Precondition checks (SOP-SCRIPT-01, Phase 1)
- Backup creation before modifications (SOP-RECOVERY-04)
- Audit logging of all operations (SOP-AUDIT-05)
- Error handling and postconditions (SOP-SCRIPT-01, Phase 4)

Copy this file as your starting point for any new script:
    cp scripts/SCRIPT_TEMPLATE.py scripts/your_script_name.py

Then fill in:
    1. SCRIPT_METADATA below
    2. preconditions() function
    3. main() logic
    4. postconditions() function (optional, for verification)
"""

import sys
import logging
from pathlib import Path
from datetime import datetime

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from audit_logger import AuditLogger
from backup_manager import BackupManager

# ============================================================================
# SCRIPT_METADATA - REQUIRED BY SOP-SCRIPT-01
# ============================================================================
# Fill these in for your script

SCRIPT_METADATA = {
    "name": "your_script_name",           # e.g., "register_appendices"
    "version": "1.0.0",                   # Semantic versioning
    "purpose": "Your script purpose",     # Single sentence
    "phase": "IMPLEMENT",                 # DESIGN, IMPLEMENT, VALIDATE, EXECUTE
    "sop": "SOP-SCRIPT-01",               # Which SOP this implements
    "preconditions": [
        # e.g., "appendices/ directory exists",
        # e.g., "APPENDIX_CODE_REGISTRY.yaml is present"
    ],
    "postconditions": [
        # e.g., "All appendix codes validated",
        # e.g., "No code conflicts detected"
    ],
    "files_modified": [],                # Files this script changes
    "files_read": [],                    # Files this script reads
    "dependencies": [],                  # Other scripts that must run first
    "author": "Your Name",               # Author of script
    "contact": "you@example.com",        # Contact for issues
    "dry_run_capable": True,             # Can script run in --dry-run mode?
    "requires_backup": True,             # Does script need backup before running?
}


# ============================================================================
# SETUP LOGGING - MANDATORY BY SOP-AUDIT-05
# ============================================================================

def setup_logging():
    """Setup logging with both console and file output"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    script_name = SCRIPT_METADATA["name"]
    log_file = log_dir / f"{script_name}.log"

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


# ============================================================================
# PRECONDITIONS - MANDATORY BY SOP-SCRIPT-01, PHASE 1
# ============================================================================

def check_preconditions(logger):
    """
    Validate all preconditions before running script.

    Returns:
        (bool, str): (success, error_message)
    """
    logger.info(f"Checking preconditions for {SCRIPT_METADATA['name']}...")

    # EXAMPLE: Check required directories
    required_dirs = ["appendices", "chapters", "docs"]
    for dir_name in required_dirs:
        if not Path(dir_name).exists():
            return False, f"Required directory missing: {dir_name}"

    # EXAMPLE: Check required files
    required_files = ["appendices/00_appendix_index.tex"]
    for file_name in required_files:
        if not Path(file_name).exists():
            return False, f"Required file missing: {file_name}"

    logger.info("✓ All preconditions satisfied")
    return True, None


# ============================================================================
# POSTCONDITIONS - MANDATORY BY SOP-SCRIPT-01, PHASE 4
# ============================================================================

def verify_postconditions(logger):
    """
    Verify that script completed successfully.

    Returns:
        (bool, str): (success, error_message)
    """
    logger.info("Verifying postconditions...")

    # EXAMPLE: Verify expected files exist
    # EXAMPLE: Verify no code conflicts (check registry)
    # EXAMPLE: Verify index consistency across 4 locations

    logger.info("✓ All postconditions satisfied")
    return True, None


# ============================================================================
# BACKUP CREATION - MANDATORY BY SOP-RECOVERY-04
# ============================================================================

def create_backups(backup_manager, logger, dry_run=False):
    """
    Create backups of files that will be modified.
    Required by SOP-RECOVERY-04 before ANY modifications.

    Args:
        backup_manager: BackupManager instance
        logger: Logger instance
        dry_run: If True, only show what would be backed up

    Returns:
        dict: {"success": bool, "backups": [list of backup paths]}
    """
    logger.info("Creating backups before modifications...")

    backups = {
        "success": True,
        "backups": []
    }

    # EXAMPLE: Back up appendix index
    files_to_backup = [
        "appendices/00_appendix_index.tex",
        "docs/operations/APPENDIX_CODE_REGISTRY.yaml"
    ]

    for file_path in files_to_backup:
        if not Path(file_path).exists():
            continue

        if dry_run:
            logger.info(f"[DRY RUN] Would backup: {file_path}")
        else:
            try:
                backup_path = backup_manager.create_backup(file_path)
                backups["backups"].append(str(backup_path))
                logger.info(f"✓ Backed up: {file_path} → {backup_path}")
            except Exception as e:
                logger.error(f"✗ Backup failed for {file_path}: {e}")
                backups["success"] = False

    return backups


# ============================================================================
# MAIN SCRIPT LOGIC
# ============================================================================

def main(dry_run=False):
    """
    Main script logic.

    Structure (SOP-SCRIPT-01):
    1. Setup (logging, managers)
    2. Preconditions (validation)
    3. Execution (with backups)
    4. Postconditions (verification)
    5. Audit logging

    Args:
        dry_run: If True, simulate without making changes

    Returns:
        int: Exit code (0=success, 1=failure)
    """

    # Phase 0: Setup
    logger = setup_logging()
    audit_logger = AuditLogger()
    backup_manager = BackupManager()

    logger.info("=" * 70)
    logger.info(f"Starting: {SCRIPT_METADATA['name']} v{SCRIPT_METADATA['version']}")
    logger.info(f"Purpose: {SCRIPT_METADATA['purpose']}")
    if dry_run:
        logger.info("Mode: DRY RUN (no changes will be made)")
    logger.info("=" * 70)

    start_time = datetime.now()

    try:
        # Phase 1: Check preconditions (SOP-SCRIPT-01)
        success, error = check_preconditions(logger)
        if not success:
            logger.error(f"✗ Precondition check failed: {error}")
            audit_logger.log_event(
                category="SCRIPT",
                operation="EXECUTE",
                target={
                    "type": "SCRIPT",
                    "name": SCRIPT_METADATA["name"],
                    "version": SCRIPT_METADATA["version"]
                },
                execution={
                    "status": "FAILURE",
                    "exit_code": 1,
                    "phase": "PRECONDITIONS",
                    "error": error
                }
            )
            return 1

        # Phase 2: Create backups (SOP-RECOVERY-04)
        if SCRIPT_METADATA["requires_backup"] and not dry_run:
            backups = create_backups(backup_manager, logger, dry_run=False)
            if not backups["success"]:
                logger.error("✗ Backup creation failed, aborting")
                return 1

        # Phase 3: Execute main logic
        logger.info("Executing main logic...")
        # ====== INSERT YOUR MAIN LOGIC HERE ======
        # Example:
        # files_to_process = get_files_to_process()
        # for file in files_to_process:
        #     if dry_run:
        #         logger.info(f"[DRY RUN] Would process: {file}")
        #     else:
        #         process_file(file, logger)
        # ===========================================

        # Phase 4: Verify postconditions (SOP-SCRIPT-01)
        success, error = verify_postconditions(logger)
        if not success:
            logger.error(f"✗ Postcondition check failed: {error}")
            return 1

        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"✓ Script completed successfully ({duration:.1f}s)")

        # Phase 5: Log to audit trail (SOP-AUDIT-05)
        audit_logger.log_event(
            category="SCRIPT",
            operation="EXECUTE",
            target={
                "type": "SCRIPT",
                "name": SCRIPT_METADATA["name"],
                "version": SCRIPT_METADATA["version"]
            },
            execution={
                "status": "SUCCESS",
                "exit_code": 0,
                "duration_seconds": duration,
                "dry_run": dry_run
            },
            metadata={
                "purpose": SCRIPT_METADATA["purpose"],
                "phase": SCRIPT_METADATA["phase"]
            }
        )

        return 0

    except Exception as e:
        duration = (datetime.now() - start_time).total_seconds()
        logger.error(f"✗ Script failed with exception: {e}")
        import traceback
        traceback.print_exc()

        # Log failure to audit trail
        audit_logger.log_event(
            category="SCRIPT",
            operation="EXECUTE",
            target={
                "type": "SCRIPT",
                "name": SCRIPT_METADATA["name"],
                "version": SCRIPT_METADATA["version"]
            },
            execution={
                "status": "FAILURE",
                "exit_code": 1,
                "duration_seconds": duration,
                "error": str(e)
            }
        )

        return 1


# ============================================================================
# COMMAND LINE INTERFACE
# ============================================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description=SCRIPT_METADATA["purpose"],
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
SOP Reference: {SCRIPT_METADATA['sop']}
Author: {SCRIPT_METADATA['author']}

Examples:
  # Run script normally
  python3 {Path(__file__).name}

  # Run in dry-run mode (show what would change without making changes)
  python3 {Path(__file__).name} --dry-run

  # Show preconditions and postconditions
  python3 {Path(__file__).name} --show-checks
        """
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show changes without making them"
    )

    parser.add_argument(
        "--show-checks",
        action="store_true",
        help="Show preconditions and postconditions only"
    )

    args = parser.parse_args()

    if args.show_checks:
        print("\n=== PRECONDITIONS ===")
        for cond in SCRIPT_METADATA["preconditions"]:
            print(f"  ✓ {cond}")
        print("\n=== POSTCONDITIONS ===")
        for cond in SCRIPT_METADATA["postconditions"]:
            print(f"  ✓ {cond}")
        sys.exit(0)

    sys.exit(main(dry_run=args.dry_run))
