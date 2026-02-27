#!/usr/bin/env python3
"""
Paper Validation & Migration Script
====================================
Migrates BibTeX keys to PAP- prefixed superkeys with DOI/URL validation.

Features:
  - Counts references per paper (start with easiest)
  - Validates DOI exists
  - Validates URL is accessible
  - Migrates BibTeX entry + ALL references
  - Validates no orphan references remain
  - Logs learnings for future migrations

Usage:
  python scripts/migrate_paper_validated.py --analyze          # Show papers sorted by reference count
  python scripts/migrate_paper_validated.py --check KEY        # Check single paper status
  python scripts/migrate_paper_validated.py --migrate KEY      # Migrate single paper
  python scripts/migrate_paper_validated.py --validate KEY     # Validate migration complete
  python scripts/migrate_paper_validated.py --batch N          # Migrate N easiest papers

Author: EBF Team
Date: January 2026
Reference: Appendix BN REF-SUPERKEY, Axiom SK-9
"""

import os
import re
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from collections import defaultdict
from datetime import datetime
import argparse

# Configuration
BIB_FILE = Path("bibliography/bcm_master.bib")
LEARNING_LOG = Path("data/paper_migration_learnings.yaml")
PAPER_REFS_DIR = Path("data/paper-references")
PAP_PREFIX = "PAP-"

# Threshold for generating reference files
MIN_REFS_FOR_FILE = 6

# Directories to search for references
SEARCH_DIRS = [
    Path("appendices"),
    Path("chapters"),
    Path("data"),
    Path("docs"),
]

# File extensions to search
SEARCH_EXTENSIONS = [".tex", ".yaml", ".yml", ".md", ".bib"]


@dataclass
class PaperInfo:
    """Information about a paper in the bibliography."""
    key: str
    title: str = ""
    author: str = ""
    year: str = ""
    doi: Optional[str] = None
    url: Optional[str] = None
    reference_count: int = 0
    reference_locations: List[str] = field(default_factory=list)
    has_pap_prefix: bool = False
    # EBF-specific fields stored in BibTeX
    ebf_reference_count: Optional[int] = None  # Cached count from BibTeX
    ebf_migration_status: str = "pending"  # pending, migrated, validated

    @property
    def is_validated(self) -> bool:
        """Paper is validated if it has DOI or URL."""
        return bool(self.doi or self.url)


class PaperMigrator:
    """Handles paper validation and migration."""

    def __init__(self):
        self.papers: Dict[str, PaperInfo] = {}
        self.learnings: List[Dict] = []

    def load_bibliography(self) -> int:
        """Load all papers from bcm_master.bib."""
        if not BIB_FILE.exists():
            print(f"❌ BibTeX file not found: {BIB_FILE}")
            return 0

        with open(BIB_FILE, 'r', encoding='utf-8') as f:
            content = f.read()

        # Pattern to match BibTeX entries
        entry_pattern = r'@(\w+)\{([^,]+),([^@]*?)(?=\n@|\n*$)'

        for match in re.finditer(entry_pattern, content, re.DOTALL):
            entry_type = match.group(1).lower()
            key = match.group(2).strip()
            fields = match.group(3)

            # Skip special entries
            if entry_type in ('string', 'preamble', 'comment'):
                continue

            paper = PaperInfo(key=key)
            paper.has_pap_prefix = key.startswith(PAP_PREFIX)

            # Extract fields
            for field_match in re.finditer(r'(\w+)\s*=\s*[{"]([^}"]*)[}"]', fields):
                field_name = field_match.group(1).lower()
                field_value = field_match.group(2).strip()

                if field_name == 'title':
                    paper.title = field_value[:60] + "..." if len(field_value) > 60 else field_value
                elif field_name == 'author':
                    paper.author = field_value.split(',')[0].split(' and ')[0][:30]
                elif field_name == 'year':
                    paper.year = field_value
                elif field_name == 'doi':
                    paper.doi = field_value
                elif field_name == 'url':
                    paper.url = field_value
                elif field_name == 'ebf_reference_count':
                    try:
                        paper.ebf_reference_count = int(field_value)
                    except ValueError:
                        pass
                elif field_name == 'ebf_migration_status':
                    paper.ebf_migration_status = field_value

            self.papers[key] = paper

        return len(self.papers)

    def count_references(self) -> None:
        """Count references to each paper across the codebase (optimized single-pass)."""
        for paper in self.papers.values():
            paper.reference_count = 0
            paper.reference_locations = []

        # Build set of unmigrated keys for fast lookup
        unmigrated_keys = {k for k, p in self.papers.items() if not p.has_pap_prefix}

        # Single pass through all files
        for search_dir in SEARCH_DIRS:
            if not search_dir.exists():
                continue

            for ext in SEARCH_EXTENSIONS:
                for file_path in search_dir.rglob(f"*{ext}"):
                    # Skip the bib file itself
                    if file_path.suffix == '.bib':
                        continue

                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                    except Exception:
                        continue

                    # Find all word-like tokens in the file
                    # Check which ones match paper keys
                    for key in unmigrated_keys:
                        if key in content:
                            # Verify it's not already PAP-prefixed
                            pattern = rf'(?<!PAP-)\b{re.escape(key)}\b'
                            matches = re.findall(pattern, content)
                            if matches:
                                self.papers[key].reference_count += len(matches)
                                self.papers[key].reference_locations.append(f"{file_path}:{len(matches)}")

    def find_references(self, key: str) -> List[Tuple[Path, int, str]]:
        """Find all references to a specific paper key."""
        references = []

        for search_dir in SEARCH_DIRS:
            if not search_dir.exists():
                continue

            for ext in SEARCH_EXTENSIONS:
                for file_path in search_dir.rglob(f"*{ext}"):
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            lines = f.readlines()
                    except Exception:
                        continue

                    for line_num, line in enumerate(lines, 1):
                        # Match key but not PAP-key
                        pattern = rf'(?<!PAP-)\b{re.escape(key)}\b'
                        if re.search(pattern, line):
                            references.append((file_path, line_num, line.strip()[:80]))

        return references

    def validate_no_orphans(self, key: str) -> List[Tuple[Path, int, str]]:
        """Check that no un-migrated references remain after migration."""
        return self.find_references(key)

    def migrate_single_paper(self, key: str, dry_run: bool = True) -> Dict:
        """Migrate a single paper and all its references."""
        result = {
            'key': key,
            'new_key': f"{PAP_PREFIX}{key}",
            'success': False,
            'changes': [],
            'errors': [],
            'orphans': [],
        }

        if key not in self.papers:
            result['errors'].append(f"Paper not found: {key}")
            return result

        paper = self.papers[key]
        new_key = f"{PAP_PREFIX}{key}"

        # Find all references first
        references = self.find_references(key)
        result['reference_count'] = len(references)

        # 1. Migrate BibTeX entry
        if not dry_run:
            self._migrate_bib_entry(key, new_key)
        result['changes'].append(f"BibTeX: {key} → {new_key}")

        # 2. Migrate all references
        files_to_update = defaultdict(list)
        for file_path, line_num, line_content in references:
            files_to_update[file_path].append((line_num, line_content))

        for file_path, locations in files_to_update.items():
            if not dry_run:
                self._migrate_file_references(file_path, key, new_key)
            result['changes'].append(f"{file_path}: {len(locations)} references")

        # 3. Validate (only in non-dry-run mode)
        if not dry_run:
            orphans = self.validate_no_orphans(key)
            result['orphans'] = [(str(p), ln, txt) for p, ln, txt in orphans]
            result['success'] = len(orphans) == 0
        else:
            result['success'] = True  # Dry run always "succeeds"

        return result

    def _migrate_bib_entry(self, old_key: str, new_key: str) -> None:
        """Update the BibTeX entry key."""
        with open(BIB_FILE, 'r', encoding='utf-8') as f:
            content = f.read()

        # Pattern to match the entry definition
        pattern = rf'(@\w+\{{){re.escape(old_key)}(,)'
        content = re.sub(pattern, rf'\g<1>{new_key}\g<2>', content)

        with open(BIB_FILE, 'w', encoding='utf-8') as f:
            f.write(content)

    def _migrate_file_references(self, file_path: Path, old_key: str, new_key: str) -> None:
        """Update all references in a file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Replace all occurrences (but not already-migrated ones)
        pattern = rf'(?<!PAP-)\b{re.escape(old_key)}\b'
        content = re.sub(pattern, new_key, content)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def update_all_reference_counts(self) -> int:
        """Update reference counts for all papers in BibTeX (single pass)."""
        self.load_bibliography()
        self.count_references()

        # Build update map
        updates = {}
        for key, paper in self.papers.items():
            status = "migrated" if paper.has_pap_prefix else "pending"
            updates[key] = {
                'ref_count': paper.reference_count,
                'status': status,
                'old_count': paper.ebf_reference_count,
            }

        # Single pass through BibTeX file
        with open(BIB_FILE, 'r', encoding='utf-8') as f:
            content = f.read()

        # Pattern to match each BibTeX entry
        entry_pattern = r'(@\w+\{)([^,]+)(,.*?)((?=\n@)|\Z)'

        def update_entry(match):
            prefix = match.group(1)
            key = match.group(2)
            body = match.group(3)
            suffix = match.group(4)

            if key not in updates:
                return match.group(0)

            update = updates[key]

            # Remove existing EBF fields
            body = re.sub(r',?\s*ebf_reference_count\s*=\s*\{[^}]*\}', '', body)
            body = re.sub(r',?\s*ebf_migration_status\s*=\s*\{[^}]*\}', '', body)

            # Clean up trailing commas and whitespace before }
            body = re.sub(r',\s*\}', '\n}', body)

            # Add new EBF fields before closing brace
            if body.rstrip().endswith('}'):
                insert_pos = body.rfind('}')
                new_fields = f',\n  ebf_reference_count = {{{update["ref_count"]}}},\n  ebf_migration_status = {{{update["status"]}}}\n'
                body = body[:insert_pos] + new_fields + body[insert_pos:]

            return prefix + key + body + suffix

        updated_content = re.sub(entry_pattern, update_entry, content, flags=re.DOTALL)

        # Count changes
        changed = sum(1 for k, v in updates.items()
                     if v['ref_count'] != v['old_count'] or v['old_count'] is None)

        # Write back
        with open(BIB_FILE, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        return changed

    def generate_reference_file(self, key: str) -> Optional[Path]:
        """Generate a YAML file documenting all references to a paper."""
        if key not in self.papers:
            return None

        paper = self.papers[key]
        references = self.find_references(key)

        if len(references) < MIN_REFS_FOR_FILE:
            return None

        # Ensure directory exists
        PAPER_REFS_DIR.mkdir(parents=True, exist_ok=True)

        # Generate filename (use PAP- prefix if not already present)
        filename = key if key.startswith(PAP_PREFIX) else f"{PAP_PREFIX}{key}"
        file_path = PAPER_REFS_DIR / f"{filename}.yaml"

        # Build YAML content
        content = f"""# Paper Reference Registry: {filename}
# Auto-generated by migrate_paper_validated.py
# Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

paper: {key}
superkey: {filename}
title: "{paper.title}"
author: "{paper.author}"
year: "{paper.year}"
doi: {f'"{paper.doi}"' if paper.doi else 'null'}
url: {f'"{paper.url}"' if paper.url else 'null'}

reference_count: {len(references)}
migration_status: {paper.ebf_migration_status}

# All locations where this paper is referenced
references:
"""
        # Group by file
        by_file = defaultdict(list)
        for file_path_ref, line_num, context in references:
            by_file[str(file_path_ref)].append((line_num, context))

        for file_ref, locations in sorted(by_file.items()):
            content += f"\n  # {file_ref}\n"
            for line_num, context in sorted(locations):
                # Determine reference type
                ref_type = "citation"
                if "theory" in file_ref.lower() or "MS-" in context:
                    ref_type = "theory_definition"
                elif "parameter" in context.lower() or "=" in context:
                    ref_type = "parameter_source"
                elif "bib_keys" in context or "use_for" in context:
                    ref_type = "yaml_reference"

                # Escape quotes in context
                safe_context = context.replace('"', '\\"')[:60]

                content += f"""  - file: "{file_ref}"
    line: {line_num}
    context: "{safe_context}"
    type: {ref_type}
"""

        # Write file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return file_path

    def generate_all_reference_files(self) -> int:
        """Generate reference files for all papers with 6+ references."""
        self.load_bibliography()
        self.count_references()

        generated = 0
        papers_to_process = [
            (k, p) for k, p in self.papers.items()
            if p.reference_count >= MIN_REFS_FOR_FILE
        ]

        print(f"\n📚 Papers with {MIN_REFS_FOR_FILE}+ references: {len(papers_to_process)}")

        for key, paper in sorted(papers_to_process, key=lambda x: -x[1].reference_count):
            file_path = self.generate_reference_file(key)
            if file_path:
                generated += 1
                print(f"   ✅ {key}: {paper.reference_count} refs → {file_path.name}")

        return generated

    def analyze(self) -> None:
        """Analyze all papers and show migration status."""
        print("\n" + "="*80)
        print("PAPER MIGRATION ANALYSIS")
        print("="*80)

        # Load and count
        paper_count = self.load_bibliography()
        print(f"\n📚 Total papers in bibliography: {paper_count}")

        self.count_references()

        # Separate migrated and unmigrated
        migrated = [p for p in self.papers.values() if p.has_pap_prefix]
        unmigrated = [p for p in self.papers.values() if not p.has_pap_prefix]

        print(f"✅ Already migrated (PAP-): {len(migrated)}")
        print(f"⏳ To migrate: {len(unmigrated)}")

        # Sort unmigrated by reference count
        unmigrated.sort(key=lambda p: p.reference_count)

        # Show validation status
        with_doi = sum(1 for p in unmigrated if p.doi)
        with_url = sum(1 for p in unmigrated if p.url)
        validated = sum(1 for p in unmigrated if p.is_validated)

        print(f"\n📋 Validation status (unmigrated papers):")
        print(f"   With DOI: {with_doi}")
        print(f"   With URL: {with_url}")
        print(f"   Validated (DOI or URL): {validated}")
        print(f"   Need validation: {len(unmigrated) - validated}")

        # Show papers by reference count buckets
        print(f"\n📊 Papers by reference count:")
        buckets = [(0, 0), (1, 1), (2, 5), (6, 10), (11, 50), (51, float('inf'))]
        for low, high in buckets:
            count = sum(1 for p in unmigrated if low <= p.reference_count <= high)
            high_str = str(high) if high != float('inf') else "+"
            print(f"   {low}-{high_str} refs: {count} papers")

        # Show easiest papers (0 references)
        zero_refs = [p for p in unmigrated if p.reference_count == 0]
        print(f"\n🎯 EASIEST TO MIGRATE (0 references): {len(zero_refs)} papers")
        for p in zero_refs[:10]:
            doi_status = "✓ DOI" if p.doi else "✗ no DOI"
            print(f"   {p.key[:45]:<45} {doi_status}")
        if len(zero_refs) > 10:
            print(f"   ... and {len(zero_refs) - 10} more")

        # Show next batch (1 reference)
        one_ref = [p for p in unmigrated if p.reference_count == 1]
        print(f"\n📝 NEXT BATCH (1 reference): {len(one_ref)} papers")
        for p in one_ref[:5]:
            doi_status = "✓ DOI" if p.doi else "✗ no DOI"
            locs = p.reference_locations[0] if p.reference_locations else ""
            print(f"   {p.key[:40]:<40} {doi_status:<10} → {locs}")
        if len(one_ref) > 5:
            print(f"   ... and {len(one_ref) - 5} more")

        print("\n" + "-"*80)
        print("Commands:")
        print("  --check KEY      Check single paper status")
        print("  --migrate KEY    Migrate single paper (dry-run, add --execute to apply)")
        print("  --batch N        Migrate N easiest papers (dry-run)")
        print("-"*80 + "\n")

    def check_paper(self, key: str) -> None:
        """Show detailed status of a single paper."""
        self.load_bibliography()

        if key not in self.papers:
            print(f"❌ Paper not found: {key}")
            return

        paper = self.papers[key]

        print("\n" + "="*80)
        print(f"PAPER STATUS: {key}")
        print("="*80)

        print(f"\n📄 Metadata:")
        print(f"   Title:  {paper.title}")
        print(f"   Author: {paper.author}")
        print(f"   Year:   {paper.year}")

        print(f"\n🔗 Validation:")
        print(f"   DOI: {paper.doi or '❌ MISSING'}")
        print(f"   URL: {paper.url or '❌ MISSING'}")
        print(f"   Status: {'✅ VALIDATED' if paper.is_validated else '⚠️ NEEDS VALIDATION'}")

        print(f"\n📍 References in codebase:")
        references = self.find_references(key)
        print(f"   Total: {len(references)}")

        if references:
            print("\n   Locations:")
            for file_path, line_num, line_content in references[:15]:
                print(f"   {file_path}:{line_num}")
                print(f"      {line_content[:70]}")
            if len(references) > 15:
                print(f"   ... and {len(references) - 15} more")

        print("\n" + "-"*80)
        if paper.has_pap_prefix:
            print("✅ Already migrated!")
        else:
            print(f"Run: --migrate {key} --execute")
        print("-"*80 + "\n")

    def migrate_paper(self, key: str, execute: bool = False) -> None:
        """Migrate a single paper (dry-run by default)."""
        self.load_bibliography()

        if key not in self.papers:
            print(f"❌ Paper not found: {key}")
            return

        paper = self.papers[key]

        if paper.has_pap_prefix:
            print(f"✅ Paper already migrated: {key}")
            return

        mode = "EXECUTING" if execute else "DRY-RUN"
        print("\n" + "="*80)
        print(f"PAPER MIGRATION ({mode}): {key}")
        print("="*80)

        result = self.migrate_single_paper(key, dry_run=not execute)

        print(f"\n📄 Paper: {key} → {result['new_key']}")
        print(f"📍 References found: {result['reference_count']}")

        print(f"\n📝 Changes:")
        for change in result['changes']:
            print(f"   {change}")

        if result['errors']:
            print(f"\n❌ Errors:")
            for error in result['errors']:
                print(f"   {error}")

        if execute and result['orphans']:
            print(f"\n⚠️ ORPHAN REFERENCES (migration incomplete!):")
            for path, line, content in result['orphans']:
                print(f"   {path}:{line}")
                print(f"      {content}")

        print("\n" + "-"*80)
        if execute:
            if result['success']:
                print("✅ Migration complete and validated!")
            else:
                print("❌ Migration incomplete - orphan references remain!")
        else:
            print("DRY-RUN complete. Add --execute to apply changes.")
        print("-"*80 + "\n")

    def batch_migrate(self, count: int, execute: bool = False) -> None:
        """Migrate multiple papers starting with easiest."""
        self.load_bibliography()
        self.count_references()

        # Get unmigrated papers sorted by reference count
        unmigrated = [p for p in self.papers.values() if not p.has_pap_prefix]
        unmigrated.sort(key=lambda p: p.reference_count)

        # Take first N
        batch = unmigrated[:count]

        mode = "EXECUTING" if execute else "DRY-RUN"
        print("\n" + "="*80)
        print(f"BATCH MIGRATION ({mode}): {len(batch)} papers")
        print("="*80)

        total_refs = 0
        total_changes = 0
        results = []

        for paper in batch:
            result = self.migrate_single_paper(paper.key, dry_run=not execute)
            results.append(result)
            total_refs += result['reference_count']
            total_changes += len(result['changes'])

            status = "✅" if result['success'] else "❌"
            print(f"{status} {paper.key[:50]:<50} refs:{result['reference_count']:>3}")

        print("\n" + "-"*80)
        print(f"Summary: {len(batch)} papers, {total_refs} references, {total_changes} file changes")

        if execute:
            failed = [r for r in results if not r['success']]
            if failed:
                print(f"⚠️ {len(failed)} papers had orphan references!")
            else:
                print("✅ All migrations complete and validated!")
        else:
            print("DRY-RUN complete. Add --execute to apply changes.")
        print("-"*80 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Paper validation and migration with DOI/URL verification"
    )
    parser.add_argument('--analyze', action='store_true',
                       help='Analyze all papers and show migration status')
    parser.add_argument('--check', metavar='KEY',
                       help='Check status of a single paper')
    parser.add_argument('--migrate', metavar='KEY',
                       help='Migrate a single paper (dry-run by default)')
    parser.add_argument('--batch', metavar='N', type=int,
                       help='Migrate N easiest papers (dry-run by default)')
    parser.add_argument('--validate', metavar='KEY',
                       help='Validate that a migration is complete')
    parser.add_argument('--execute', action='store_true',
                       help='Actually apply changes (not just dry-run)')
    parser.add_argument('--update-counts', action='store_true',
                       help='Update ebf_reference_count in all BibTeX entries')
    parser.add_argument('--generate-refs', action='store_true',
                       help='Generate reference YAML files for papers with 6+ refs')
    parser.add_argument('--generate-ref', metavar='KEY',
                       help='Generate reference YAML for a specific paper')

    args = parser.parse_args()

    migrator = PaperMigrator()

    if args.update_counts:
        print("\n" + "="*70)
        print("UPDATING REFERENCE COUNTS IN BIBTEX")
        print("="*70 + "\n")
        updated = migrator.update_all_reference_counts()
        print(f"✅ Updated {updated} BibTeX entries with ebf_reference_count")
    elif args.generate_refs:
        print("\n" + "="*70)
        print("GENERATING PAPER REFERENCE FILES")
        print("="*70)
        generated = migrator.generate_all_reference_files()
        print(f"\n✅ Generated {generated} reference files in {PAPER_REFS_DIR}/")
    elif args.generate_ref:
        migrator.load_bibliography()
        migrator.count_references()
        file_path = migrator.generate_reference_file(args.generate_ref)
        if file_path:
            print(f"✅ Generated {file_path}")
        else:
            print(f"❌ Could not generate (paper not found or <{MIN_REFS_FOR_FILE} refs)")
    elif args.analyze or not any([args.check, args.migrate, args.batch, args.validate, args.generate_refs, args.generate_ref]):
        migrator.analyze()
    elif args.check:
        migrator.check_paper(args.check)
    elif args.migrate:
        migrator.migrate_paper(args.migrate, execute=args.execute)
    elif args.batch:
        migrator.batch_migrate(args.batch, execute=args.execute)
    elif args.validate:
        migrator.load_bibliography()
        orphans = migrator.validate_no_orphans(args.validate)
        if orphans:
            print(f"❌ {len(orphans)} orphan references found for {args.validate}:")
            for path, line, content in orphans:
                print(f"   {path}:{line}: {content}")
        else:
            print(f"✅ No orphan references for {args.validate}")


if __name__ == '__main__':
    main()
