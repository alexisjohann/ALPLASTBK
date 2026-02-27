#!/usr/bin/env python3
"""
migrate_bibtex_to_yaml.py - Migrate EBF fields from BibTeX to YAML (SSOT)

This script implements the SSOT (Single Source of Truth) architecture by:
1. Reading EBF fields from bcm_master.bib
2. Updating corresponding YAML files in data/paper-references/
3. Computing and storing Prior Scores

SSOT Architecture:
- PRIMÄR: data/paper-references/PAP-{key}.yaml (all metadata)
- FULL-TEXT: data/paper-texts/PAP-{key}.md (full text content)
- GENERATED: bibliography/bcm_master.bib (for LaTeX, generated from YAML)

Usage:
    python scripts/migrate_bibtex_to_yaml.py --dry-run          # Preview changes
    python scripts/migrate_bibtex_to_yaml.py --migrate          # Execute migration
    python scripts/migrate_bibtex_to_yaml.py --paper PAP-xxx    # Single paper
    python scripts/migrate_bibtex_to_yaml.py --stats            # Show statistics
"""

import os
import sys
import re
import yaml
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
BIBTEX_PATH = PROJECT_ROOT / "bibliography" / "bcm_master.bib"
YAML_DIR = PROJECT_ROOT / "data" / "paper-references"
PAPER_TEXTS_DIR = PROJECT_ROOT / "data" / "paper-texts"

# EBF fields to migrate from BibTeX to YAML
EBF_FIELDS = [
    'evidence_tier',
    'use_for',
    'theory_support',
    'parameter',
    'identification',
    'external_validity',
    'ebf_reference_count',
    'ebf_migration_status',
    'session_ref',
    'notes'
]

# BibTeX standard fields (already in YAML, for reference)
STANDARD_FIELDS = [
    'title', 'author', 'year', 'journal', 'volume', 'number',
    'pages', 'doi', 'publisher', 'booktitle', 'editor', 'url'
]


def parse_bibtex_file(bib_path: Path) -> Dict[str, Dict]:
    """Parse BibTeX file and extract all entries with their fields."""
    entries = {}
    
    with open(bib_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    # Match BibTeX entries: @type{key, ... }
    entry_pattern = r'@(\w+)\{([^,]+),([^@]*?)(?=\n@|\Z)'
    matches = re.findall(entry_pattern, content, re.DOTALL)
    
    for entry_type, key, fields_str in matches:
        key = key.strip()
        entry = {
            'entry_type': entry_type.lower(),
            'key': key,
            'fields': {}
        }
        
        # Parse fields
        # Match field = {value} or field = value
        field_pattern = r'(\w+)\s*=\s*(?:\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}|(\d+))'
        for match in re.finditer(field_pattern, fields_str):
            field_name = match.group(1).lower()
            field_value = match.group(2) if match.group(2) else match.group(3)
            if field_value:
                entry['fields'][field_name] = field_value.strip()
        
        entries[key] = entry
    
    return entries


def load_yaml_file_fallback(yaml_path: Path) -> Optional[Dict]:
    """Load YAML file with fallback parsing for files with escape characters."""
    with open(yaml_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    # Extract core fields using regex (for files with escape character issues)
    data = {}

    # Extract simple fields: field: value or field: "value"
    simple_patterns = [
        (r'^paper:\s*(\S+)', 'paper'),
        (r'^superkey:\s*(\S+)', 'superkey'),
        (r'^title:\s*["\']?([^"\'\n]+)', 'title'),
        (r'^author:\s*["\']?([^"\'\n]+)', 'author'),
        (r'^year:\s*["\']?(\d{4})', 'year'),
        (r'^doi:\s*["\']?([^"\'\n]+)', 'doi'),
        (r'^publication_type:\s*(\S+)', 'publication_type'),
        (r'^migration_status:\s*(\S+)', 'migration_status'),
        (r'^reference_count:\s*(\d+)', 'reference_count'),
    ]

    for pattern, field in simple_patterns:
        match = re.search(pattern, content, re.MULTILINE)
        if match:
            data[field] = match.group(1).strip().strip('"\'')

    # Try to get abstract (multiline)
    abstract_match = re.search(r'abstract:\s*["\']?([^"\']+)', content, re.DOTALL)
    if abstract_match:
        data['abstract'] = abstract_match.group(1).strip()[:500]  # First 500 chars

    return data if data else None


def load_yaml_file(yaml_path: Path) -> Optional[Dict]:
    """Load YAML file with error handling and fallback."""
    if not yaml_path.exists():
        return None

    try:
        with open(yaml_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as e:
        # Try fallback parsing
        fallback_data = load_yaml_file_fallback(yaml_path)
        if fallback_data:
            return fallback_data
        print(f"  Warning: YAML parse error in {yaml_path.name}: {e}")
        return None


def save_yaml_file(yaml_path: Path, data: Dict, preserve_comments: bool = True):
    """Save YAML file with proper formatting."""
    # Custom representer for multiline strings
    def str_representer(dumper, data):
        if '\n' in data:
            return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
        return dumper.represent_scalar('tag:yaml.org,2002:str', data)
    
    yaml.add_representer(str, str_representer)
    
    with open(yaml_path, 'w', encoding='utf-8') as f:
        # Write header
        f.write(f"# Paper Reference Registry: {data.get('superkey', 'Unknown')}\n")
        f.write(f"# SSOT Architecture - All paper data centralized here\n")
        f.write(f"# Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Write YAML content
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def extract_ebf_fields(bib_entry: Dict) -> Dict[str, Any]:
    """Extract EBF-specific fields from a BibTeX entry."""
    fields = bib_entry.get('fields', {})
    ebf_data = {}
    
    for field in EBF_FIELDS:
        if field in fields:
            value = fields[field]
            
            # Parse special fields
            if field == 'evidence_tier':
                try:
                    ebf_data[field] = int(value)
                except ValueError:
                    ebf_data[field] = value
            
            elif field == 'use_for':
                # Split comma-separated values
                ebf_data[field] = [v.strip() for v in value.split(',')]
            
            elif field == 'ebf_reference_count':
                try:
                    ebf_data[field] = int(value)
                except ValueError:
                    ebf_data[field] = 0
            
            else:
                ebf_data[field] = value
    
    return ebf_data


def check_full_text_exists(paper_key: str) -> Dict[str, Any]:
    """Check if full-text file exists and return metadata."""
    # Normalize key for file lookup
    if not paper_key.startswith('PAP-'):
        file_key = f"PAP-{paper_key}"
    else:
        file_key = paper_key
    
    full_text_path = PAPER_TEXTS_DIR / f"{file_key}.md"
    
    if full_text_path.exists():
        stat = full_text_path.stat()
        char_count = stat.st_size
        
        # Determine content level based on size
        if char_count >= 50000:
            content_level = "L3"
        elif char_count >= 10000:
            content_level = "L2"
        elif char_count >= 2000:
            content_level = "L1"
        else:
            content_level = "L0"
        
        return {
            'available': True,
            'path': f"data/paper-texts/{file_key}.md",
            'format': 'markdown',
            'content_level': content_level,
            'character_count': char_count,
            'archived_date': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d')
        }
    
    return {
        'available': False,
        'path': None,
        'content_level': 'L0'
    }


def compute_prior_score_simple(yaml_data: Dict, ebf_fields: Dict) -> Dict[str, Any]:
    """Compute a simplified Prior Score for the paper."""
    # Get evidence tier (default 3 = lowest)
    evidence_tier = ebf_fields.get('evidence_tier', 3)
    tau_map = {1: 1.0, 2: 0.8, 3: 0.5}
    tau = tau_map.get(evidence_tier, 0.5)
    
    # Get content level
    full_text = yaml_data.get('full_text', {})
    content_level = full_text.get('content_level', 'L0')
    rho_map = {'L0': 0.6, 'L1': 0.8, 'L2': 0.95, 'L3': 1.0}
    rho = rho_map.get(content_level, 0.6)
    
    # Estimate supply based on available fields
    use_for = ebf_fields.get('use_for', [])
    theory_support = ebf_fields.get('theory_support', '')
    parameter = ebf_fields.get('parameter', '')
    
    # Supply vector estimation (simplified)
    s_theory = 1.0 if theory_support and 'MS-' in theory_support.upper() else 0.3
    s_param = 1.0 if parameter else 0.2
    s_lit = 1.0 if any('LIT-' in u.upper() for u in use_for) else 0.3
    s_10c = 1.0 if any('CORE-' in u.upper() for u in use_for) else 0.3
    
    # Gap vector (constant for now - would be computed from EBF state)
    g_theory = 0.8
    g_param = 0.9
    g_lit = 0.7
    g_10c = 0.6
    
    # Weights
    w = {'theory': 0.3, 'param': 0.25, 'lit': 0.25, '10c': 0.2}
    
    # Compute prior score
    prior_score = (
        w['theory'] * g_theory * s_theory +
        w['param'] * g_param * s_param +
        w['lit'] * g_lit * s_lit +
        w['10c'] * g_10c * s_10c
    ) * tau * rho
    
    # Classification
    if prior_score >= 0.5:
        classification = "STANDARD"
    elif prior_score >= 0.3:
        classification = "MINIMAL"
    elif prior_score >= 0.2:
        classification = "PENDING"
    else:
        classification = "REJECT"
    
    return {
        'prior_score': round(prior_score, 4),
        'classification': classification,
        'confidence_multiplier': rho,
        'evidence_quality': tau,
        'content_level': content_level,
        'computed_date': datetime.now().strftime('%Y-%m-%d')
    }


def migrate_paper(paper_key: str, bib_entries: Dict, dry_run: bool = True) -> Tuple[bool, str]:
    """Migrate a single paper from BibTeX to YAML."""
    # Normalize key
    bib_key = paper_key.replace('PAP-', '')
    yaml_key = f"PAP-{bib_key}" if not paper_key.startswith('PAP-') else paper_key
    
    # Find BibTeX entry
    bib_entry = None
    for key, entry in bib_entries.items():
        if bib_key in key or key in bib_key:
            bib_entry = entry
            break
    
    if not bib_entry:
        return False, f"BibTeX entry not found for {paper_key}"
    
    # Load YAML file
    yaml_path = YAML_DIR / f"{yaml_key}.yaml"
    yaml_data = load_yaml_file(yaml_path)
    
    if not yaml_data:
        return False, f"YAML file not found: {yaml_path.name}"
    
    # Extract EBF fields from BibTeX
    ebf_fields = extract_ebf_fields(bib_entry)
    
    if not ebf_fields:
        return False, f"No EBF fields found in BibTeX for {paper_key}"
    
    # Check for full-text
    full_text_info = check_full_text_exists(bib_key)
    
    # Compute prior score
    yaml_data['full_text'] = full_text_info
    prior_score_data = compute_prior_score_simple(yaml_data, ebf_fields)
    
    # Build update summary
    changes = []
    
    # Add EBF fields section
    if 'ebf_integration' not in yaml_data:
        yaml_data['ebf_integration'] = {}
        changes.append("+ ebf_integration section")
    
    for field, value in ebf_fields.items():
        old_value = yaml_data['ebf_integration'].get(field)
        if old_value != value:
            yaml_data['ebf_integration'][field] = value
            changes.append(f"+ {field}: {value}")
    
    # Add prior score
    yaml_data['prior_score'] = prior_score_data
    changes.append(f"+ prior_score: {prior_score_data['prior_score']} ({prior_score_data['classification']})")
    
    # Add full-text info
    if full_text_info['available']:
        changes.append(f"+ full_text: {full_text_info['content_level']}")
    
    # Update migration status
    yaml_data['migration_status'] = 'ssot_migrated'
    yaml_data['ssot_migration_date'] = datetime.now().strftime('%Y-%m-%d')
    
    if dry_run:
        return True, f"Would update with {len(changes)} changes: {', '.join(changes[:3])}..."
    else:
        save_yaml_file(yaml_path, yaml_data)
        return True, f"Updated with {len(changes)} changes"


def get_yaml_files() -> List[Path]:
    """Get all YAML files in paper-references directory."""
    if not YAML_DIR.exists():
        return []
    return list(YAML_DIR.glob("PAP-*.yaml"))


def main():
    parser = argparse.ArgumentParser(
        description='Migrate EBF fields from BibTeX to YAML (SSOT Architecture)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python scripts/migrate_bibtex_to_yaml.py --dry-run
    python scripts/migrate_bibtex_to_yaml.py --migrate
    python scripts/migrate_bibtex_to_yaml.py --paper PAP-fehr1999theory
    python scripts/migrate_bibtex_to_yaml.py --stats
        """
    )
    
    parser.add_argument('--dry-run', action='store_true',
                        help='Preview changes without modifying files')
    parser.add_argument('--migrate', action='store_true',
                        help='Execute the migration')
    parser.add_argument('--paper', type=str,
                        help='Migrate a single paper by key (e.g., PAP-fehr1999theory)')
    parser.add_argument('--stats', action='store_true',
                        help='Show statistics about migration status')
    parser.add_argument('--limit', type=int, default=0,
                        help='Limit number of papers to process (0 = all)')
    
    args = parser.parse_args()
    
    if not any([args.dry_run, args.migrate, args.paper, args.stats]):
        parser.print_help()
        return
    
    print("=" * 70)
    print("SSOT Migration: BibTeX → YAML")
    print("=" * 70)
    
    # Parse BibTeX
    print(f"\nLoading BibTeX from {BIBTEX_PATH}...")
    bib_entries = parse_bibtex_file(BIBTEX_PATH)
    print(f"  Found {len(bib_entries)} BibTeX entries")
    
    # Get YAML files
    yaml_files = get_yaml_files()
    print(f"  Found {len(yaml_files)} YAML files")
    
    if args.stats:
        # Show statistics
        print("\n" + "=" * 70)
        print("MIGRATION STATISTICS")
        print("=" * 70)
        
        migrated = 0
        pending = 0
        with_ebf_fields = 0
        with_full_text = 0
        
        for yaml_path in yaml_files:
            yaml_data = load_yaml_file(yaml_path)
            if yaml_data:
                status = yaml_data.get('migration_status', 'pending')
                if status == 'ssot_migrated':
                    migrated += 1
                else:
                    pending += 1
                
                if yaml_data.get('ebf_integration'):
                    with_ebf_fields += 1
                
                full_text = yaml_data.get('full_text', {})
                if full_text.get('available'):
                    with_full_text += 1
        
        print(f"\nYAML Files: {len(yaml_files)}")
        print(f"  - SSOT Migrated:    {migrated}")
        print(f"  - Pending:          {pending}")
        print(f"  - With EBF fields:  {with_ebf_fields}")
        print(f"  - With Full-Text:   {with_full_text}")
        
        # BibTeX stats
        with_ebf = sum(1 for e in bib_entries.values() 
                       if any(f in e.get('fields', {}) for f in EBF_FIELDS))
        print(f"\nBibTeX Entries: {len(bib_entries)}")
        print(f"  - With EBF fields:  {with_ebf}")
        
        return
    
    if args.paper:
        # Single paper migration
        print(f"\nMigrating single paper: {args.paper}")
        success, message = migrate_paper(args.paper, bib_entries, dry_run=not args.migrate)
        status = "✓" if success else "✗"
        print(f"  {status} {args.paper}: {message}")
        return
    
    # Batch migration
    dry_run = args.dry_run or not args.migrate
    mode = "DRY RUN" if dry_run else "MIGRATING"
    
    print(f"\n{mode} all papers...")
    
    success_count = 0
    skip_count = 0
    error_count = 0
    
    files_to_process = yaml_files[:args.limit] if args.limit > 0 else yaml_files
    
    for i, yaml_path in enumerate(files_to_process):
        paper_key = yaml_path.stem
        success, message = migrate_paper(paper_key, bib_entries, dry_run=dry_run)
        
        if success:
            if "No EBF fields" in message or "not found" in message.lower():
                skip_count += 1
            else:
                success_count += 1
                if not dry_run:
                    print(f"  ✓ {paper_key}")
        else:
            error_count += 1
        
        # Progress
        if (i + 1) % 100 == 0:
            print(f"  Progress: {i + 1}/{len(files_to_process)}")
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Processed:  {len(files_to_process)}")
    print(f"  Updated:    {success_count}")
    print(f"  Skipped:    {skip_count} (no EBF fields in BibTeX)")
    print(f"  Errors:     {error_count}")
    
    if dry_run:
        print("\n  This was a DRY RUN. Use --migrate to execute changes.")


if __name__ == '__main__':
    main()
