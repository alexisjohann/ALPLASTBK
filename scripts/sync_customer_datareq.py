#!/usr/bin/env python3
"""
Sync Customer Data from dr-datareq to data/customers/

This script synchronizes customer data between:
- Source: data/dr-datareq/sources/clients/<customer>/
- Target: data/customers/<customer>/

Usage:
    python scripts/sync_customer_datareq.py                    # Sync all customers
    python scripts/sync_customer_datareq.py --customer bfe     # Sync specific customer
    python scripts/sync_customer_datareq.py --check            # Check sync status
    python scripts/sync_customer_datareq.py --create <name>    # Create new customer link

Features:
- Creates symlinks for automatic updates
- Validates link integrity
- Reports new customers in dr-datareq not yet in customers/
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime

# Paths
BASE_DIR = Path(__file__).parent.parent
DATAREQ_CLIENTS = BASE_DIR / "data" / "dr-datareq" / "sources" / "clients"
CUSTOMERS_DIR = BASE_DIR / "data" / "customers"

# Mapping: source file pattern -> target name
FILE_MAPPINGS = {
    "external/BCM2_INDIV_{}_behavioral.yaml": "{}_behavioral_parameters.yaml",
    "external/BCM2_MIKRO_{}_context.yaml": "{}_context_mikro.yaml",
    "learnings/{}_context_enrichments.yaml": "{}_learnings.yaml",
}


def get_datareq_customers():
    """Get list of customers in dr-datareq/sources/clients/"""
    if not DATAREQ_CLIENTS.exists():
        return []
    return [d.name for d in DATAREQ_CLIENTS.iterdir() if d.is_dir()]


def get_linked_customers():
    """Get list of customers in data/customers/ with dr-datareq links"""
    linked = []
    if not CUSTOMERS_DIR.exists():
        return linked

    for d in CUSTOMERS_DIR.iterdir():
        if d.is_dir():
            # Check if it has symlinks to dr-datareq
            for item in d.iterdir():
                if item.is_symlink():
                    target = os.readlink(item)
                    if "dr-datareq" in target:
                        linked.append(d.name)
                        break
    return linked


def check_sync_status():
    """Check which customers need syncing"""
    datareq = set(get_datareq_customers())
    linked = set(get_linked_customers())

    not_linked = datareq - linked
    orphaned = linked - datareq

    print("=" * 60)
    print("CUSTOMER SYNC STATUS")
    print("=" * 60)
    print(f"\nIn dr-datareq/sources/clients/: {len(datareq)}")
    for c in sorted(datareq):
        status = "✅" if c in linked else "❌ NOT LINKED"
        print(f"  {c}: {status}")

    if not_linked:
        print(f"\n⚠️  Not yet linked ({len(not_linked)}):")
        for c in sorted(not_linked):
            print(f"  - {c}")
        print("\nRun: python scripts/sync_customer_datareq.py --create <name>")

    if orphaned:
        print(f"\n⚠️  Orphaned links ({len(orphaned)}):")
        for c in sorted(orphaned):
            print(f"  - {c}")

    return not_linked


def create_customer_link(customer_name: str):
    """Create customer folder with symlinks to dr-datareq"""
    customer_upper = customer_name.upper()
    source_dir = DATAREQ_CLIENTS / customer_name
    target_dir = CUSTOMERS_DIR / customer_name

    if not source_dir.exists():
        print(f"❌ Source not found: {source_dir}")
        return False

    # Create target directory
    target_dir.mkdir(parents=True, exist_ok=True)

    # Calculate relative path from target to source
    rel_path = os.path.relpath(source_dir, target_dir)

    print(f"\n📁 Creating links for: {customer_name}")
    print(f"   Source: {source_dir}")
    print(f"   Target: {target_dir}")
    print(f"   Relative: {rel_path}")

    # Create symlinks for specific files
    links_created = []

    for source_pattern, target_pattern in FILE_MAPPINGS.items():
        source_file = source_dir / source_pattern.format(customer_upper)
        target_file = target_dir / target_pattern.format(customer_name)

        if source_file.exists():
            rel_source = os.path.relpath(source_file, target_dir)
            if target_file.exists() or target_file.is_symlink():
                target_file.unlink()
            os.symlink(rel_source, target_file)
            links_created.append(target_file.name)
            print(f"   ✅ {target_file.name} -> {rel_source}")

    # Link projects directory
    projects_source = source_dir / "projects"
    projects_target = target_dir / "projects"
    if projects_source.exists():
        rel_projects = os.path.relpath(projects_source, target_dir)
        if projects_target.exists() or projects_target.is_symlink():
            if projects_target.is_symlink():
                projects_target.unlink()
            elif projects_target.is_dir():
                import shutil
                shutil.rmtree(projects_target)
        os.symlink(rel_projects, projects_target)
        links_created.append("projects/")
        print(f"   ✅ projects/ -> {rel_projects}")

    # Create profile if it doesn't exist
    profile_file = target_dir / f"{customer_name}_profile.yaml"
    if not profile_file.exists():
        create_profile_template(customer_name, profile_file)
        print(f"   ✅ {profile_file.name} (created)")

    print(f"\n✅ Created {len(links_created)} links for {customer_name}")
    return True


def create_profile_template(customer_name: str, profile_path: Path):
    """Create a basic profile template"""
    template = f'''# {customer_name.upper()} Customer Profile
# Version: 1.0
# Created: {datetime.now().strftime("%Y-%m-%d")}
# CVA Level: SCHNELL (to be expanded)

metadata:
  customer_id: "{customer_name.upper()}"
  customer_name: "{customer_name.title()}"
  cva_level: "SCHNELL"
  created: "{datetime.now().strftime("%Y-%m-%d")}"
  updated: "{datetime.now().strftime("%Y-%m-%d")}"

  source_sync:
    enabled: true
    source_path: "data/dr-datareq/sources/clients/{customer_name}"
    sync_direction: "bidirectional"
    last_sync: "{datetime.now().strftime("%Y-%m-%d")}"

profile:
  name: "{customer_name.title()}"
  # TODO: Fill in customer details

relationship:
  status: "active"
  # TODO: Add project history

notes: |
  Profile auto-generated. Please expand with customer details.
'''
    profile_path.write_text(template)


def sync_all():
    """Sync all customers from dr-datareq"""
    not_linked = check_sync_status()

    if not_linked:
        print("\n" + "=" * 60)
        print("CREATING MISSING LINKS")
        print("=" * 60)
        for customer in sorted(not_linked):
            create_customer_link(customer)

    print("\n✅ Sync complete")


def main():
    parser = argparse.ArgumentParser(description="Sync customer data from dr-datareq")
    parser.add_argument("--customer", "-c", help="Sync specific customer")
    parser.add_argument("--check", action="store_true", help="Check sync status only")
    parser.add_argument("--create", help="Create link for new customer")
    parser.add_argument("--all", action="store_true", help="Sync all missing customers")

    args = parser.parse_args()

    if args.check:
        check_sync_status()
    elif args.create:
        create_customer_link(args.create)
    elif args.customer:
        create_customer_link(args.customer)
    elif args.all:
        sync_all()
    else:
        check_sync_status()


if __name__ == "__main__":
    main()
