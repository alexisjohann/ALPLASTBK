#!/usr/bin/env python3
# ============================================================================
# EBF Database Initialization Script
# ============================================================================
# Runs at session-start to load and validate all 5 EBF databases
# Provides quick overview of available data
#
# Usage: python3 scripts/init-databases.py [--verbose]
# ============================================================================

import os
import sys
import yaml
import json
from pathlib import Path
from typing import Dict, List, Tuple

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def load_yaml(filepath: str) -> Dict:
    """Load a YAML file safely."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        print(f"{Colors.FAIL}✗ Error loading {filepath}: {e}{Colors.ENDC}", file=sys.stderr)
        return {}

def load_json(filepath: str) -> Dict:
    """Load a JSON file safely."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f) or {}
    except Exception as e:
        print(f"{Colors.FAIL}✗ Error loading {filepath}: {e}{Colors.ENDC}", file=sys.stderr)
        return {}

def get_database_stats() -> Tuple[Dict, List[str]]:
    """Load all 5 databases and return statistics."""
    project_root = Path(__file__).parent.parent
    stats = {}
    warnings = []

    # Database definitions
    databases = {
        "📚 Paper References": {
            "path": project_root / "data" / "paper-references",
            "key": "_directory_count",
            "description": "Scientific papers (SSOT: individual PAP-*.yaml files)"
        },
        "📋 Case Registry": {
            "path": project_root / "data" / "case-registry.yaml",
            "key": "cases",
            "description": "Real-world case studies with 10C specifications"
        },
        "🚀 Intervention Registry": {
            "path": project_root / "data" / "intervention-registry.yaml",
            "key": "projects",
            "description": "Behavior change projects with predictions & results"
        },
        "🧮 Model Registry": {
            "path": project_root / "models" / "models.registry.yaml",
            "key": "models",
            "description": "Validated behavioral models (seed library)"
        },
        "👥 Stakeholder Models": {
            "path": project_root / "data" / "stakeholder-models" / "stakeholder_models_registry.yaml",
            "key": "companies",
            "description": "Customer/company-specific models with simulations"
        }
    }

    for db_name, db_info in databases.items():
        filepath = str(db_info["path"])

        if not db_info["path"].exists():
            stats[db_name] = {
                "count": 0,
                "status": "⚠️  MISSING",
                "description": db_info["description"]
            }
            warnings.append(f"Missing database: {filepath}")
            continue

        # Handle directory-based databases (paper-references/)
        if db_info["key"] == "_directory_count":
            count = len(list(db_info["path"].glob("PAP-*.yaml")))
        else:
            # Load YAML database
            data = load_yaml(filepath)
            entries = data.get(db_info["key"], {})

            if isinstance(entries, dict):
                count = len(entries)
            elif isinstance(entries, list):
                count = len(entries)
            else:
                count = 0

        status = "✅" if count > 0 else "⚠️  EMPTY"
        stats[db_name] = {
            "count": count,
            "status": status,
            "description": db_info["description"]
        }

    return stats, warnings

def print_database_status(stats: Dict, warnings: List[str], verbose: bool = False):
    """Print database status in a formatted way."""

    print(f"\n{Colors.BOLD}{Colors.OKCYAN}{'=' * 50}")
    print("EBF DATABASE STATUS".center(50))
    print(f"{'=' * 50}{Colors.ENDC}\n")

    total_entries = 0
    all_ok = True

    for db_name, info in stats.items():
        count = info["count"]
        status = info["status"]
        description = info["description"]
        total_entries += count

        # Determine color based on status
        if "✅" in status:
            color = Colors.OKGREEN
        elif "⚠️" in status:
            color = Colors.WARNING
            all_ok = False
        else:
            color = Colors.FAIL
            all_ok = False

        # Print database info
        print(f"{color}{db_name:30} {status:12} {count:6} entries{Colors.ENDC}")

        if verbose:
            print(f"  └─ {description}")

    print(f"\n{Colors.BOLD}Total Entries:{Colors.ENDC} {total_entries:,}")

    # Print warnings if any
    if warnings:
        print(f"\n{Colors.WARNING}{Colors.BOLD}⚠️  WARNINGS:{Colors.ENDC}")
        for warning in warnings:
            print(f"  • {warning}")

    # Print quick tips
    print(f"\n{Colors.OKCYAN}{Colors.BOLD}💡 QUICK TIPS:{Colors.ENDC}")
    print("  /case --domain health              Find similar cases")
    print("  /design-model --mode schnell       Design model in 10 min")
    print("  /new-customer \"Company\" 1500      Create customer model")
    print("  /intervention-manage new           Track a project")
    print("  /sensitivity-analysis Company      What-if analysis")

    # Print summary
    if all_ok and total_entries > 0:
        print(f"\n{Colors.OKGREEN}{Colors.BOLD}✅ All databases loaded successfully!{Colors.ENDC}\n")
    else:
        print(f"\n{Colors.WARNING}{Colors.BOLD}⚠️  Some databases may need attention{Colors.ENDC}\n")

    return all_ok

def validate_database_schemas(project_root: Path) -> List[str]:
    """Check if schema files exist for all databases."""
    issues = []

    schemas = {
        "Paper References": project_root / "data" / "paper-references",  # Directory-based, no schema file
        "Case Registry": project_root / "data" / "case-registry.schema.yaml",
        "Intervention": project_root / "data" / "intervention-registry.schema.yaml",
        "Model Registry": project_root / "models" / "models.schema.yaml",
        "Stakeholder Models": project_root / "data" / "stakeholder-models" / "stakeholder-models.schema.yaml"
    }

    for schema_name, schema_path in schemas.items():
        if schema_path.is_dir():
            continue  # Directory-based databases validated via check_paper_consistency.py
        if not schema_path.exists():
            issues.append(f"Missing schema: {schema_name}")

    return issues

def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="EBF Database Initialization")
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    args = parser.parse_args()

    # Get database statistics
    stats, warnings = get_database_stats()

    # Check schemas
    project_root = Path(__file__).parent.parent
    schema_issues = validate_database_schemas(project_root)
    warnings.extend(schema_issues)

    # Print status
    all_ok = print_database_status(stats, warnings, args.verbose)

    # Return appropriate exit code
    sys.exit(0 if all_ok else 1)

if __name__ == "__main__":
    main()
