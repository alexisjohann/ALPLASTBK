#!/usr/bin/env python3
"""
EBF CORE Framework Migration Script: 10C → 10C

This script automates the migration from the 10C CORE Framework to 10C,
adding CORE-EIT as the 10th CORE dimension.

Usage:
    python scripts/migrate_9c_to_10c.py                    # Dry-run (default)
    python scripts/migrate_9c_to_10c.py --dry-run         # Explicit dry-run
    python scripts/migrate_9c_to_10c.py --execute         # Actually make changes
    python scripts/migrate_9c_to_10c.py --verbose         # Detailed output
    python scripts/migrate_9c_to_10c.py --report-only     # Only show what would change

Author: Claude Code
Date: 2026-01-20
Version: 1.0
"""

import os
import re
import sys
import yaml
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# =============================================================================
# CONFIGURATION
# =============================================================================

# The new 10th CORE definition (EIT - Emergent Intervention Theory)
NEW_CORE_EIT = {
    'number': 10,
    'code': 'EIT',
    'appendix_code': 'IE',
    'full_name': 'CORE-EIT',
    'title': 'Emergent Intervention Theory',
    'question_de': 'Wie emergieren Interventionen aus dem 10C-System?',
    'question_en': 'How do interventions emerge from the 10C system?',
    'output': 'Intervention Vector I⃗, E-modes, T1-T8 Types',
    'primary_symbol': 'I⃗, E-Full, E-Partial, E-None',
    'chapter_reference': 17,
    'file': 'appendices/IE_CORE-EIT.tex',
    'key_concepts': [
        '10C Emergence Classification (Fundamental/Semi-Emergent/Fully Emergent)',
        'E-Full: Dimensions + Values entirely determined by prior COREs',
        'E-Partial: Dimensions determined, values require configuration',
        'E-None: Neither dimensions nor values determined',
        'T1-T8 Intervention Primitives',
        'Phase-Type Affinity Matrix α_BCJ',
        'Segment Multiplier Matrix β_BCS',
        'P_eff = σ(WEC × α_BCJ × β_BCS)'
    ]
}

# Files to update with version change
FILES_TO_UPDATE = [
    'README.md',
    'CLAUDE.md',
    'docs/EBF-INTRODUCTION.md',
    'docs/frameworks/appendix-category-definitions.md',
    'docs/frameworks/core-framework-extension-guide.md',
    'appendices/README.md',
    'appendices/00_appendix_index.tex',
]

# Patterns to search for and update
PATTERNS = {
    # Simple version references (uppercase)
    r'\b9C\b': '10C',
    r'\b9C CORE\b': '10C CORE',
    r'10C Framework': '10C Framework',
    r'10C-Dimensionen': '10C-Dimensionen',
    r'10 COREs': '10 COREs',
    r'10 CORE': '10 CORE',

    # YAML/config values
    r'count: 10\b': 'count: 10',
    r'version: "10C"': 'version: "10C"',
    r'"10C"': '"10C"',
    r"'10C'": "'10C'",

    # LaTeX labels (lowercase 9c)
    r'sec:10c-': 'sec:10c-',
    r'tab:10c-': 'tab:10c-',
    r'def:10c-': 'def:10c-',
    r'\\ref\{sec:10c-': '\\ref{sec:10c-',
    r'\\ref\{tab:10c-': '\\ref{tab:10c-',
    r'\\ref\{def:10c-': '\\ref{def:10c-',

    # Python dict keys and variables
    r"'10c_integration'": "'10c_integration'",
    r'"10c_integration"': '"10c_integration"',
    r'10c_integration': '10c_integration',
}

# Files to rename (old_name -> new_name)
FILES_TO_RENAME = {
    'chapters/01b_10c_core_architecture.tex': 'chapters/01b_10c_core_architecture.tex',
}

# References to renamed files that need updating
FILE_REFERENCE_PATTERNS = {
    r'01b_10c_core_architecture': '01b_10c_core_architecture',
}

# Files/directories to exclude from search
EXCLUDE_PATTERNS = [
    'migration-audit/',
    '.git/',
    '__pycache__/',
    'outputs/',
    '.pyc',
    'node_modules/',
    'venv/',
]

# File extensions to process
INCLUDE_EXTENSIONS = [
    '.md', '.yaml', '.yml', '.tex', '.py', '.json', '.txt'
]

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def should_process_file(filepath: str) -> bool:
    """Check if file should be processed based on exclusion rules."""
    for pattern in EXCLUDE_PATTERNS:
        if pattern in filepath:
            return False

    ext = os.path.splitext(filepath)[1].lower()
    if ext not in INCLUDE_EXTENSIONS:
        return False

    return True


def find_all_9c_references(root_dir: str) -> Dict[str, List[Tuple[int, str, str]]]:
    """
    Find all files containing 10C references.

    Returns:
        Dict mapping filepath to list of (line_number, original_line, pattern_matched)
    """
    results = {}

    for root, dirs, files in os.walk(root_dir):
        # Filter out excluded directories
        dirs[:] = [d for d in dirs if not any(excl.rstrip('/') == d for excl in EXCLUDE_PATTERNS)]

        for filename in files:
            filepath = os.path.join(root, filename)
            rel_path = os.path.relpath(filepath, root_dir)

            if not should_process_file(rel_path):
                continue

            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()

                file_matches = []
                for i, line in enumerate(lines, 1):
                    for pattern in PATTERNS.keys():
                        if re.search(pattern, line):
                            file_matches.append((i, line.rstrip(), pattern))

                if file_matches:
                    results[rel_path] = file_matches

            except Exception as e:
                print(f"  Warning: Could not read {rel_path}: {e}")

    return results


def update_ssot(ssot_path: str, dry_run: bool = True, verbose: bool = False) -> Tuple[bool, str]:
    """
    Update the Single Source of Truth YAML file.

    Returns:
        Tuple of (success, message)
    """
    try:
        with open(ssot_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse YAML
        data = yaml.safe_load(content)

        # Check current version
        current_version = data.get('framework', {}).get('version', 'unknown')
        if current_version == '10C':
            return True, f"SSOT already at 10C - skipping SSOT update"
        if current_version != '10C':
            return False, f"SSOT is not at 10C (found: {current_version})"

        if dry_run:
            return True, "Would update SSOT: version 10C → 10C, count 9 → 10, add CORE-EIT"

        # Update framework section
        # We need to do string replacement to preserve YAML formatting and comments

        # Update version
        content = re.sub(r'version:\s*"10C"', 'version: "10C"', content)

        # Update count
        content = re.sub(r'count:\s*9\b', 'count: 10', content)

        # Find where to insert new CORE (after HIERARCHY)
        # Look for the pattern after CORE 9: HIERARCHY section
        hierarchy_pattern = r'(# CORE 9: HIERARCHY.*?key_concepts:.*?\n(?:      - "[^"]+"\n)+)'

        new_core_yaml = '''
  # --------------------------------------------------------------------------
  # CORE 10: EIT - Emergent Intervention Theory
  # --------------------------------------------------------------------------
  - number: 10
    code: "EIT"
    appendix_code: "IE"
    full_name: "CORE-EIT"
    title: "Emergent Intervention Theory"
    question_de: "Wie emergieren Interventionen aus dem 10C-System?"
    question_en: "How do interventions emerge from the 10C system?"
    output: "Intervention Vector I⃗, E-modes, T1-T8 Types"
    primary_symbol: "I⃗, E-Full, E-Partial, E-None"
    chapter_reference: 17
    file: "appendices/IE_CORE-EIT.tex"
    key_concepts:
      - "10C Emergence Classification (Fundamental/Semi-Emergent/Fully Emergent)"
      - "E-Full: Dimensions + Values entirely determined by prior COREs"
      - "E-Partial: Dimensions determined, values require configuration"
      - "E-None: Neither dimensions nor values determined"
      - "T1-T8 Intervention Primitives"
      - "Phase-Type Affinity Matrix α_BCJ"
      - "Segment Multiplier Matrix β_BCS"
      - "P_eff = σ(WEC × α_BCJ × β_BCS)"
'''

        # Find insertion point (after last key_concept of HIERARCHY)
        # Look for the extension_rules section
        extension_marker = "# ============================================================================\n# ERWEITERUNGSREGELN"
        if extension_marker in content:
            content = content.replace(
                extension_marker,
                new_core_yaml + "\n" + extension_marker
            )

        # Write updated content
        with open(ssot_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return True, "SSOT updated successfully"

    except Exception as e:
        return False, f"Error updating SSOT: {e}"


def update_file_content(filepath: str, dry_run: bool = True, verbose: bool = False) -> Tuple[int, List[str]]:
    """
    Update 10C references to 10C in a file.

    Returns:
        Tuple of (changes_count, list_of_changes)
    """
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        original_content = content
        changes = []

        for pattern, replacement in PATTERNS.items():
            matches = list(re.finditer(pattern, content))
            if matches:
                for match in matches:
                    changes.append(f"  Line ~{content[:match.start()].count(chr(10))+1}: '{match.group()}' → '{replacement}'")
                content = re.sub(pattern, replacement, content)

        if content != original_content:
            if not dry_run:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
            return len(changes), changes

        return 0, []

    except Exception as e:
        return 0, [f"Error: {e}"]


def update_dependencies_section(ssot_path: str, dry_run: bool = True) -> Tuple[bool, str]:
    """Add EIT to dependencies section in SSOT."""
    if dry_run:
        return True, "Would add EIT dependencies"

    try:
        with open(ssot_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Add EIT dependency after HIERARCHY
        hierarchy_dep = "HIERARCHY: [HOW, READY, STAGE]"
        intervene_dep = "HIERARCHY: [HOW, READY, STAGE]\n  EIT: [STAGE, HIERARCHY, WHERE]  # Intervention design needs BCJ, decision levels, parameters"

        content = content.replace(hierarchy_dep, intervene_dep)

        with open(ssot_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return True, "Dependencies updated"
    except Exception as e:
        return False, f"Error: {e}"


def update_glossary_terms(ssot_path: str, dry_run: bool = True) -> Tuple[bool, str]:
    """Add EIT glossary terms to SSOT."""
    if dry_run:
        return True, "Would add EIT glossary terms"

    glossary_addition = '''
  EIT:
    - term: "Intervention Type (T1-T8)"
      definition: "Die 8 primitiven Interventionstypen basierend auf W_eff Zerlegung"
      symbol: "T ∈ {T1, T2, ..., T8}"
    - term: "Phase-Type Affinity (α)"
      definition: "Effektivität eines Interventionstyps in einer BCJ-Phase"
      symbol: "α(T, φ) ∈ [0,1]"
    - term: "Intervention Portfolio"
      definition: "Kombination mehrerer Interventionen mit Complementarity-Effekten"
      symbol: "I_H = {I_1, ..., I_n}"
'''

    try:
        with open(ssot_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find glossary_terms section and add after HIERARCHY
        hierarchy_glossary = '  HIERARCHY:\n    - term: "Decision Level (L0-L3)"'
        if hierarchy_glossary in content:
            insert_point = content.find(hierarchy_glossary)
            # Find end of HIERARCHY glossary section (next double newline or next section)
            end_search = content.find('\n\n# ', insert_point)
            if end_search == -1:
                end_search = len(content)

            # Find the last entry of HIERARCHY
            hierarchy_end = content.rfind('symbol:', insert_point, end_search)
            if hierarchy_end != -1:
                # Find end of that line
                line_end = content.find('\n', hierarchy_end)
                content = content[:line_end+1] + glossary_addition + content[line_end+1:]

        with open(ssot_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return True, "Glossary terms added"
    except Exception as e:
        return False, f"Error: {e}"


def update_chapter_mapping(ssot_path: str, dry_run: bool = True) -> Tuple[bool, str]:
    """Add EIT chapter mapping to SSOT."""
    if dry_run:
        return True, "Would add EIT chapter mapping"

    chapter_mapping = '''
  - core: EIT
    primary_chapter: 17
    title: "Intervention Architecture"
    supporting_chapters: [18, 19, 20]
'''

    try:
        with open(ssot_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find chapter_mapping section and add after HIERARCHY
        hierarchy_mapping = "primary_chapter: 15\n    title: \"Decision Hierarchy & Strategic Coherence\""
        if hierarchy_mapping in content:
            # Find end of HIERARCHY mapping
            insert_point = content.find(hierarchy_mapping)
            # Find the supporting_chapters line after this
            supp_start = content.find("supporting_chapters:", insert_point)
            if supp_start != -1:
                line_end = content.find('\n', supp_start)
                content = content[:line_end+1] + chapter_mapping + content[line_end+1:]

        with open(ssot_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return True, "Chapter mapping added"
    except Exception as e:
        return False, f"Error: {e}"


def rename_files(root_dir: str, dry_run: bool = True) -> List[Tuple[str, str, bool]]:
    """
    Rename files according to FILES_TO_RENAME mapping.

    Returns:
        List of (old_path, new_path, success) tuples
    """
    results = []

    for old_name, new_name in FILES_TO_RENAME.items():
        old_path = os.path.join(root_dir, old_name)
        new_path = os.path.join(root_dir, new_name)

        if os.path.exists(old_path):
            if dry_run:
                results.append((old_name, new_name, True))
            else:
                try:
                    os.rename(old_path, new_path)
                    results.append((old_name, new_name, True))
                except Exception as e:
                    results.append((old_name, new_name, False))
        else:
            # File might already be renamed
            if os.path.exists(new_path):
                results.append((old_name, f"{new_name} (already exists)", True))
            else:
                results.append((old_name, f"{new_name} (source not found)", False))

    return results


def update_file_references(root_dir: str, dry_run: bool = True) -> Tuple[int, List[str]]:
    """
    Update references to renamed files across the codebase.

    Returns:
        Tuple of (changes_count, list_of_changes)
    """
    total_changes = 0
    all_changes = []

    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if not any(excl.rstrip('/') == d for excl in EXCLUDE_PATTERNS)]

        for filename in files:
            filepath = os.path.join(root, filename)
            rel_path = os.path.relpath(filepath, root_dir)

            if not should_process_file(rel_path):
                continue

            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                original_content = content
                file_changes = []

                for pattern, replacement in FILE_REFERENCE_PATTERNS.items():
                    if re.search(pattern, content):
                        file_changes.append(f"  {rel_path}: '{pattern}' → '{replacement}'")
                        content = re.sub(pattern, replacement, content)

                if content != original_content:
                    total_changes += len(file_changes)
                    all_changes.extend(file_changes)
                    if not dry_run:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(content)

            except Exception as e:
                pass

    return total_changes, all_changes


def run_validation(root_dir: str) -> Tuple[bool, str]:
    """Run the validation script to check consistency."""
    import subprocess

    try:
        result = subprocess.run(
            ['python', 'scripts/validate_core_framework.py'],
            cwd=root_dir,
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stdout + result.stderr

    except Exception as e:
        return False, f"Validation error: {e}"


# =============================================================================
# MAIN FUNCTIONS
# =============================================================================

def generate_report(root_dir: str) -> str:
    """Generate a detailed report of what would change."""
    report = []
    report.append("=" * 70)
    report.append("10C → 10C MIGRATION REPORT")
    report.append("=" * 70)
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")

    # Find all 10C references
    references = find_all_9c_references(root_dir)

    report.append(f"Files with 10C references: {len(references)}")
    total_changes = sum(len(matches) for matches in references.values())
    report.append(f"Total references to update: {total_changes}")
    report.append("")

    # Group by directory
    by_directory = {}
    for filepath, matches in references.items():
        directory = os.path.dirname(filepath) or '.'
        if directory not in by_directory:
            by_directory[directory] = []
        by_directory[directory].append((filepath, len(matches)))

    report.append("-" * 70)
    report.append("FILES BY DIRECTORY:")
    report.append("-" * 70)

    for directory in sorted(by_directory.keys()):
        files = by_directory[directory]
        report.append(f"\n{directory}/ ({sum(c for _, c in files)} references)")
        for filepath, count in sorted(files):
            report.append(f"  {os.path.basename(filepath)}: {count} references")

    report.append("")
    report.append("-" * 70)
    report.append("NEW CORE TO ADD:")
    report.append("-" * 70)
    report.append("")
    report.append("CORE 10: EIT")
    report.append(f"  Question (DE): {NEW_CORE_EIT['question_de']}")
    report.append(f"  Question (EN): {NEW_CORE_EIT['question_en']}")
    report.append(f"  Output: {NEW_CORE_EIT['output']}")
    report.append(f"  Symbol: {NEW_CORE_EIT['primary_symbol']}")
    report.append(f"  Chapter: {NEW_CORE_EIT['chapter_reference']}")
    report.append(f"  Appendix: {NEW_CORE_EIT['file']}")
    report.append(f"  Key Concepts:")
    for concept in NEW_CORE_EIT['key_concepts']:
        report.append(f"    - {concept}")

    report.append("")
    report.append("-" * 70)
    report.append("SSOT CHANGES:")
    report.append("-" * 70)
    report.append("  1. framework.version: '10C' → '10C'")
    report.append("  2. framework.count: 10 → 10")
    report.append("  3. Add CORE 10: EIT entry")
    report.append("  4. Add EIT to dependencies")
    report.append("  5. Add EIT glossary terms")
    report.append("  6. Add EIT chapter mapping")

    report.append("")
    report.append("-" * 70)
    report.append("POST-MIGRATION TASKS:")
    report.append("-" * 70)
    report.append("")
    report.append("The following directories are EXCLUDED from migration (by design):")
    report.append("")
    report.append("  1. migration-audit/ (69 files with 10C)")
    report.append("     → Historical backup from 8C→10C migration")
    report.append("     → Action: KEEP AS-IS (do not modify)")
    report.append("")
    report.append("  2. outputs/ (18 files with 10C)")
    report.append("     → Generated outputs (reports, papers, simulations)")
    report.append("     → Action: REGENERATE after migration using source files")
    report.append("     → Files to regenerate:")
    report.append("       - UBS-FIN-SB-001_* (simulation outputs)")
    report.append("       - *-PAPER-DATABASE-*.md (paper reports)")
    report.append("       - Chapter_*_Paper.tex (generated papers)")
    report.append("       - fehr-*-papers-*.md, kahneman-*-papers-*.md")
    report.append("")
    report.append("  3. .git/, __pycache__/, node_modules/, venv/")
    report.append("     → Technical directories (no text content)")
    report.append("     → Action: NONE")
    report.append("")
    report.append("VALIDATION STEPS (after --execute):")
    report.append("  1. Run: python scripts/validate_core_framework.py")
    report.append("  2. Run: python scripts/check_template_compliance.py --all")
    report.append("  3. Regenerate outputs: python scripts/generate_paper.py ...")
    report.append("")
    report.append("=" * 70)

    return "\n".join(report)


def execute_migration(root_dir: str, dry_run: bool = True, verbose: bool = False) -> bool:
    """Execute the full migration."""

    print("=" * 70)
    if dry_run:
        print("10C → 10C MIGRATION (DRY RUN)")
        print("No changes will be made. Use --execute to apply changes.")
    else:
        print("10C → 10C MIGRATION (EXECUTING)")
        print("Changes will be applied to files.")
    print("=" * 70)
    print()

    ssot_path = os.path.join(root_dir, 'docs/frameworks/core-framework-definition.yaml')

    # Step 1: Update SSOT
    print("Step 1: Update Single Source of Truth (SSOT)")
    print("-" * 50)

    success, message = update_ssot(ssot_path, dry_run, verbose)
    print(f"  {'[DRY-RUN]' if dry_run else '[DONE]'} {message}")

    if not dry_run:
        success, message = update_dependencies_section(ssot_path, dry_run)
        print(f"  [DONE] {message}")

        success, message = update_glossary_terms(ssot_path, dry_run)
        print(f"  [DONE] {message}")

        success, message = update_chapter_mapping(ssot_path, dry_run)
        print(f"  [DONE] {message}")
    else:
        print(f"  [DRY-RUN] Would add EIT dependencies")
        print(f"  [DRY-RUN] Would add EIT glossary terms")
        print(f"  [DRY-RUN] Would add EIT chapter mapping")

    print()

    # Step 2: Find and update all 10C references
    print("Step 2: Update 10C → 10C references in all files")
    print("-" * 50)

    references = find_all_9c_references(root_dir)
    total_files = len(references)
    total_changes = 0

    for filepath, matches in sorted(references.items()):
        full_path = os.path.join(root_dir, filepath)
        changes_count, changes = update_file_content(full_path, dry_run, verbose)
        total_changes += changes_count

        status = '[DRY-RUN]' if dry_run else '[UPDATED]'
        print(f"  {status} {filepath}: {changes_count} changes")

        if verbose and changes:
            for change in changes[:5]:  # Show first 5 changes
                print(f"    {change}")
            if len(changes) > 5:
                print(f"    ... and {len(changes) - 5} more")

    print()
    print(f"Total: {total_files} files, {total_changes} changes")
    print()

    # Step 3: Rename files
    print("Step 3: Rename files")
    print("-" * 50)

    rename_results = rename_files(root_dir, dry_run)
    for old_name, new_name, success in rename_results:
        status = '[DRY-RUN]' if dry_run else ('[RENAMED]' if success else '[FAILED]')
        print(f"  {status} {old_name} → {new_name}")

    print()

    # Step 4: Update file references
    print("Step 4: Update file references")
    print("-" * 50)

    ref_changes, ref_details = update_file_references(root_dir, dry_run)
    if ref_changes > 0:
        status = '[DRY-RUN]' if dry_run else '[UPDATED]'
        print(f"  {status} {ref_changes} file reference(s) updated")
        if verbose:
            for detail in ref_details[:10]:
                print(f"    {detail}")
            if len(ref_details) > 10:
                print(f"    ... and {len(ref_details) - 10} more")
    else:
        print("  No file references to update")

    print()

    # Step 5: Run validation (only if not dry-run)
    print("Step 5: Validation")
    print("-" * 50)

    if dry_run:
        print("  [SKIPPED] Validation skipped in dry-run mode")
        print("  Run with --execute to perform actual migration and validation")
    else:
        success, output = run_validation(root_dir)
        if success:
            print("  [PASSED] Validation successful!")
        else:
            print("  [FAILED] Validation found issues:")
            for line in output.split('\n')[:20]:
                print(f"    {line}")

    print()
    print("=" * 70)
    if dry_run:
        print("DRY RUN COMPLETE - No changes were made")
        print("Run with --execute to apply the migration")
    else:
        print("MIGRATION COMPLETE")
        print("")
        print("NEXT STEPS:")
        print("  1. Commit the changes:")
        print("     git add -A")
        print('     git commit -m "feat(CORE): Migrate 10C → 10C, add CORE-EIT"')
        print("")
        print("  2. Regenerate outputs (these were excluded from migration):")
        print("     - outputs/UBS-FIN-SB-001_* files")
        print("     - outputs/*-PAPER-DATABASE-*.md reports")
        print("     - outputs/fehr-*-papers-*.md, kahneman-*-papers-*.md")
        print("")
        print("  3. Verify migration:")
        print("     python scripts/validate_core_framework.py")
        print("")
        print("  NOTE: migration-audit/ was preserved as historical backup (8C→10C)")
    print("=" * 70)

    return True


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Migrate EBF CORE Framework from 10C to 10C',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python scripts/migrate_9c_to_10c.py                    # Dry-run (default)
  python scripts/migrate_9c_to_10c.py --report-only     # Show detailed report
  python scripts/migrate_9c_to_10c.py --execute         # Apply changes
  python scripts/migrate_9c_to_10c.py --execute -v      # Apply with verbose output
        '''
    )

    parser.add_argument(
        '--dry-run', '-d',
        action='store_true',
        default=True,
        help='Show what would change without making changes (default)'
    )

    parser.add_argument(
        '--execute', '-x',
        action='store_true',
        help='Actually execute the migration'
    )

    parser.add_argument(
        '--report-only', '-r',
        action='store_true',
        help='Only generate and show the migration report'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed output'
    )

    parser.add_argument(
        '--root', '-p',
        default='.',
        help='Root directory of the repository (default: current directory)'
    )

    args = parser.parse_args()

    # Resolve root directory
    root_dir = os.path.abspath(args.root)

    # Check if we're in the right directory
    ssot_path = os.path.join(root_dir, 'docs/frameworks/core-framework-definition.yaml')
    if not os.path.exists(ssot_path):
        print(f"Error: SSOT not found at {ssot_path}")
        print("Make sure you're running from the repository root or use --root")
        sys.exit(1)

    # Execute based on mode
    if args.report_only:
        print(generate_report(root_dir))
    else:
        dry_run = not args.execute
        execute_migration(root_dir, dry_run=dry_run, verbose=args.verbose)


if __name__ == '__main__':
    main()
