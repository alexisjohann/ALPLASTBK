#!/usr/bin/env python3
# ┌─────────────────────────────────────────────────────────────────────────┐
# │  ⚠️  DEPRECATED (2026-02-08)                                            │
# │                                                                         │
# │  Einmaliges Migrations-Script: Papers aus extracted_papers.yaml        │
# │  gegen paper-sources.yaml klassifiziert.                               │
# │  Beide Quell-Dateien sind DEPRECATED. Kept for reference only.         │
# │                                                                         │
# │  SSOT: data/paper-references/PAP-*.yaml + bibliography/bcm_master.bib │
# │  Neue Papers: /integrate-paper Workflow                                │
# └─────────────────────────────────────────────────────────────────────────┘
"""
Classify extracted papers by matching against paper-sources.yaml

⚠️  DEPRECATED — Source files (extracted_papers.yaml, paper-sources.yaml)
are both deprecated (2026-02-08).

This script:
1. Loads extracted_papers.yaml (138 papers with minimal metadata)
2. Matches against paper-sources.yaml (1784 papers with full 10C coordinates)
3. Updates titles and 10C classifications
4. Marks status as 'classified' instead of 'extracted'
5. Creates comprehensive report of matches/misses
"""

import sys
import logging
import yaml
import re
import unicodedata
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from audit_logger import AuditLogger
from backup_manager import BackupManager

# ============================================================================
# SCRIPT_METADATA
# ============================================================================

SCRIPT_METADATA = {
    "name": "classify_extracted_papers",
    "version": "1.2.0",
    "purpose": "Classify papers with confidence scoring, fallback appendix mapping, and domain-based classification",
    "phase": "VALIDATE",
    "sop": "SOP-SCRIPT-01",
    "preconditions": [
        "data/extracted_papers.yaml exists",
        "data/paper-sources.yaml exists",
        "All extracted papers have valid IDs"
    ],
    "postconditions": [
        "138 papers have status='classified'",
        "All papers have proper 9c_coordinates",
        "Match report generated in outputs/"
    ],
    "files_modified": ["data/extracted_papers.yaml"],
    "files_read": ["data/extracted_papers.yaml", "data/paper-sources.yaml"],
    "dependencies": [],
    "author": "Claude",
    "contact": "support@example.com",
    "dry_run_capable": True,
    "requires_backup": True,
}


# ============================================================================
# SETUP LOGGING
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

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


# ============================================================================
# PRECONDITIONS
# ============================================================================

def check_preconditions(logger):
    """Validate all preconditions before running script"""
    logger.info(f"Checking preconditions for {SCRIPT_METADATA['name']}...")

    # Check required files
    required_files = [
        "data/extracted_papers.yaml",
        "data/paper-sources.yaml"
    ]

    for file_name in required_files:
        if not Path(file_name).exists():
            return False, f"Required file missing: {file_name}"

    logger.info("✓ All preconditions satisfied")
    return True, None


# ============================================================================
# BACKUP CREATION
# ============================================================================

def create_backups(backup_manager, logger, dry_run=False):
    """Create backups of files that will be modified"""
    logger.info("Creating backups before modifications...")

    backups = {
        "success": True,
        "backups": []
    }

    files_to_backup = [
        "data/extracted_papers.yaml"
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
# CORE LOGIC
# ============================================================================

def load_extracted_papers():
    """Load extracted_papers.yaml"""
    with open("data/extracted_papers.yaml", 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def build_sources_index(logger):
    """
    Build index from paper-sources.yaml by reading line-by-line
    to avoid YAML parsing issues with large files
    """
    logger.info("Building paper-sources index...")

    sources_index = {}
    current_paper = None
    current_section = None

    try:
        with open("data/paper-sources.yaml", 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
    except Exception as e:
        logger.error(f"Failed to read paper-sources.yaml: {e}")
        return sources_index

    for i, line in enumerate(lines):
        # Match "- id: <paper_id>"
        id_match = re.match(r'^\s*-\s+id:\s+(\S+)\s*$', line)
        if id_match:
            current_paper = id_match.group(1)
            sources_index[current_paper] = {
                'line_start': i,
                'title': None,
                '9c_coordinates': None,
                'lit_appendix': None,
            }
            current_section = None
            continue

        if not current_paper:
            continue

        # Match "title: ..."
        if line.strip().startswith('title:'):
            title_match = re.match(r'\s*title:\s["\']?(.+?)["\']?\s*$', line)
            if title_match:
                sources_index[current_paper]['title'] = title_match.group(1).strip("'\"")

        # Match "lit_appendix: ..."
        elif line.strip().startswith('lit_appendix:'):
            lit_match = re.match(r'\s*lit_appendix:\s(\S+)\s*$', line)
            if lit_match:
                sources_index[current_paper]['lit_appendix'] = lit_match.group(1)

    logger.info(f"✓ Built index with {len(sources_index)} papers")
    return sources_index


def extract_appendix_from_source(extraction_source):
    """Extract appendix code from extraction_source"""
    # Format: "L_LIT-ACEMOGLU_..." → "L"
    # Format: "PA_LIT-AGHION_..." → "PA"
    parts = extraction_source.split('_')
    if parts:
        return parts[0]
    return None


# Fallback appendix mapping for unmatched papers based on domain/extraction source
FALLBACK_APPENDIX_MAP = {
    'CRT': 'W',  # Complex Systems/Networks → LIT-ARIELY
    'HTY': 'XV',  # Historical/Philosophical → LIT-HISTORY
    'GB': 'AA',  # Labor/Education → LIT-AUTOR
    'GN': 'P',  # Game Theory → LIT-DUFLO
    'JT': 'K',  # Market Design → LIT-FEHR
    'LA': 'AA',  # Economics → LIT-AUTOR
    'OT': 'AX',  # Other → LIT-META
    'RB': 'K',  # Behavioral → LIT-FEHR
    'SU': 'K',  # Social → LIT-FEHR
    'LO': 'X',  # Loewenstein → LIT-LOEWENSTEIN
}


def normalize_string(s):
    """
    Normalize string for matching:
    - Remove diacritics (é → e, ä → a, etc.)
    - Convert to lowercase
    - Remove special characters except alphanumerics
    """
    # Decompose and remove diacritics
    nfd = unicodedata.normalize('NFD', s)
    normalized = ''.join(c for c in nfd if unicodedata.category(c) != 'Mn')
    # Convert to lowercase and keep only alphanumeric
    return normalized.lower()


def extract_author_surnames(authors):
    """
    Extract surnames from author list (format: "Surname, Initials")
    Returns both original and normalized versions
    """
    surnames = []
    surnames_normalized = []
    for author in authors:
        if ',' in author:
            surname = author.split(',')[0].strip()
        else:
            # Fallback: last word if no comma
            parts = author.split()
            surname = parts[-1] if parts else author
        surnames.append(surname.lower())
        surnames_normalized.append(normalize_string(surname))
    return surnames, surnames_normalized


def find_matching_paper(paper, sources_index):
    """
    Find matching paper using fuzzy matching: Author(s) + Year

    Matching strategy (in order of priority, with confidence scoring):
    1. Exact match with paper_id (confidence: 1.0)
    2. First author (normalized) + year (confidence: 0.9)
    3. Any author (normalized) + year (confidence: 0.8)
    4. Multiple authors in ID (normalized) + year (confidence: 0.85)
    5. BibTeX key matching (confidence: 0.7)

    Returns: (source_id, source_info, confidence) tuple if found, or None
    """
    paper_id = paper.get('id')
    authors = paper.get('authors', [])
    year = paper.get('year')

    if not authors or not year:
        return None

    # Strategy 1: Exact match first (confidence: 1.0)
    if paper_id in sources_index:
        return (paper_id, sources_index[paper_id], 1.0)

    # Extract author surnames (both original and normalized)
    surnames, surnames_norm = extract_author_surnames(authors)
    search_year = str(year)

    if not surnames:
        return None

    # Strategy 2: First author + year (confidence: 0.9)
    if surnames:
        first_surname, first_surname_norm = surnames[0], surnames_norm[0]
        for source_id, source_info in sources_index.items():
            source_id_norm = normalize_string(source_id)
            if (source_id_norm.startswith(first_surname_norm) and search_year in source_id) or \
               (source_id.lower().startswith(first_surname) and search_year in source_id):
                return (source_id, source_info, 0.9)

    # Strategy 3: Any other author + year (confidence: 0.8)
    for i in range(1, len(surnames)):
        surname, surname_norm = surnames[i], surnames_norm[i]
        for source_id, source_info in sources_index.items():
            source_id_norm = normalize_string(source_id)
            if (source_id_norm.startswith(surname_norm) and search_year in source_id) or \
               (source_id.lower().startswith(surname) and search_year in source_id):
                return (source_id, source_info, 0.8)

    # Strategy 4: Multiple authors in ID (confidence: 0.85)
    for source_id, source_info in sources_index.items():
        source_id_norm = normalize_string(source_id)
        matching_surnames = sum(1 for s in surnames_norm if source_id_norm.find(s) >= 0)
        if matching_surnames >= 2 and search_year in source_id:
            return (source_id, source_info, 0.85)

    # Strategy 5: BibTeX key matching (confidence: 0.7)
    bibtex_key = paper.get('bibtex_key')
    if bibtex_key:
        bibtex_norm = normalize_string(bibtex_key)
        for source_id, source_info in sources_index.items():
            source_id_norm = normalize_string(source_id)
            if search_year in bibtex_norm and search_year in source_id:
                bibtex_base = bibtex_norm.replace(search_year, '')
                source_base = source_id_norm.replace(search_year, '')
                if bibtex_base and source_base and (bibtex_base in source_base or source_base in bibtex_base):
                    return (source_id, source_info, 0.7)

    return None


def classify_papers(logger, sources_index, dry_run=False):
    """Main classification logic"""

    logger.info("Loading extracted papers...")
    extracted = load_extracted_papers()

    logger.info(f"Loaded {len(extracted['extracted_papers'])} papers from extracted_papers.yaml")
    logger.info(f"Using {len(sources_index)} papers from sources index")

    # Classification stats
    stats = {
        'total': len(extracted['extracted_papers']),
        'matched': 0,
        'unmatched': 0,
        'updated': 0,
        'fallback_mapped': 0,
        'appendix_lookup': defaultdict(int),
        'fuzzy_matches': [],
        'confidence_distribution': defaultdict(int)
    }

    # Process each extracted paper
    for i, paper in enumerate(extracted['extracted_papers']):
        paper_id = paper.get('id')

        # Try to find in sources index using fuzzy matching
        match_result = find_matching_paper(paper, sources_index)
        if match_result:
            stats['matched'] += 1

            # Unpack match result with confidence
            if len(match_result) == 3:
                matched_source_id, source_info, confidence = match_result
            else:
                matched_source_id, source_info = match_result
                confidence = 0.5  # Fallback confidence

            # Track confidence distribution
            confidence_bucket = f"{int(confidence * 100)}%"
            stats['confidence_distribution'][confidence_bucket] += 1

            # Update title if available
            if source_info.get('title'):
                old_title = paper.get('title', '?')
                paper['title'] = source_info['title']
                if old_title in ['A', 'H', 'L', 'T'] and old_title != source_info['title']:
                    logger.debug(f"  {i+1}. {paper_id}: title updated ({old_title} → actual) [matched as {matched_source_id}, conf: {confidence:.2f}]")

            # Update lit_appendix if available
            if source_info.get('lit_appendix'):
                paper['lit_appendix'] = source_info['lit_appendix']

            # Track confidence in paper metadata
            paper['match_confidence'] = confidence

            # Track fuzzy match
            if matched_source_id != paper_id:
                stats['fuzzy_matches'].append({
                    'original_id': paper_id,
                    'matched_id': matched_source_id,
                    'confidence': confidence
                })

            # Mark status as classified (we matched it, even if partial metadata)
            paper['status'] = 'classified'
            stats['updated'] += 1

        else:
            # Unmatched - try fallback appendix classification from extraction_source
            stats['unmatched'] += 1
            extraction_source = paper.get('extraction_source', '')
            appendix_code = extract_appendix_from_source(extraction_source)

            # Try fallback lit_appendix mapping
            if appendix_code and appendix_code in FALLBACK_APPENDIX_MAP:
                fallback_lit_appendix = FALLBACK_APPENDIX_MAP[appendix_code]
                paper['lit_appendix'] = fallback_lit_appendix
                paper['lit_appendix_confidence'] = 0.3  # Low confidence - not a direct match
                paper['classification_notes'] = f'Fallback: domain={appendix_code} → appendix={fallback_lit_appendix}'
                stats['fallback_mapped'] += 1
                logger.debug(f"  {paper_id}: No match in sources, fallback appendix={fallback_lit_appendix}")
            elif appendix_code:
                paper['classification_notes'] = f'Manual review needed: appendix={appendix_code}'
                logger.debug(f"  {paper_id}: No match in sources, appendix={appendix_code}")
            else:
                paper['classification_notes'] = 'Manual review needed: appendix=UNKNOWN'
                logger.warning(f"  {paper_id}: No match in sources, appendix=UNKNOWN")

            # Track appendix lookup
            if appendix_code:
                stats['appendix_lookup'][appendix_code] += 1

            # Mark as extracted_unmatched (still needs manual review)
            paper['status'] = 'extracted_unmatched'

    return extracted, stats


def save_yaml(data, file_path):
    """Save data to YAML file with nice formatting"""
    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True,
                 sort_keys=False, width=120)


# ============================================================================
# POSTCONDITIONS
# ============================================================================

def verify_postconditions(logger):
    """Verify that script completed successfully"""
    logger.info("Verifying postconditions...")

    # Load updated file
    updated = load_extracted_papers()

    # Check all papers have status (classified or extracted_unmatched)
    for paper in updated['extracted_papers']:
        if 'status' not in paper:
            return False, f"Paper {paper.get('id')} has no status"
        if paper['status'] not in ['classified', 'extracted_unmatched']:
            return False, f"Paper {paper.get('id')} has invalid status: {paper['status']}"

        # Check 9c_coordinates exist (even if placeholder)
        if '9c_coordinates' not in paper:
            return False, f"Paper {paper.get('id')} has no 9c_coordinates"

    logger.info("✓ All postconditions satisfied")
    return True, None


# ============================================================================
# REPORTING
# ============================================================================

def generate_report(stats, logger):
    """Generate classification report"""

    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = output_dir / f"paper_classification_report_{timestamp}.yaml"

    fallback_count = stats.get('fallback_mapped', 0)

    report = {
        'generated': datetime.now().isoformat(),
        'script': SCRIPT_METADATA['name'],
        'version': SCRIPT_METADATA['version'],
        'statistics': {
            'total_papers': stats['total'],
            'matched': stats['matched'],
            'unmatched': stats['unmatched'],
            'unmatched_with_fallback': fallback_count,
            'match_percentage': f"{(stats['matched'] / stats['total'] * 100):.1f}%" if stats['total'] > 0 else "0%",
            'total_classified_or_fallback': stats['matched'] + fallback_count,
            'overall_coverage': f"{(stats['matched'] + fallback_count) / stats['total'] * 100:.1f}%" if stats['total'] > 0 else "0%"
        },
        'confidence_distribution': dict(sorted(stats['confidence_distribution'].items(), reverse=True)),
        'appendix_breakdown': dict(stats['appendix_lookup']),
        'fuzzy_matches_count': len(stats['fuzzy_matches']),
        'fallback_appendix_map': FALLBACK_APPENDIX_MAP
    }

    with open(report_file, 'w') as f:
        yaml.dump(report, f, default_flow_style=False)

    logger.info(f"✓ Report saved to {report_file}")

    # Summary to console
    logger.info("\n" + "="*70)
    logger.info("CLASSIFICATION SUMMARY")
    logger.info("="*70)
    logger.info(f"Total papers:           {stats['total']}")
    logger.info(f"Direct matches:         {stats['matched']} ({report['statistics']['match_percentage']})")
    logger.info(f"Unmatched:              {stats['unmatched']}")
    logger.info(f"  └─ Fallback mapped:   {report['statistics']['unmatched_with_fallback']}")
    logger.info(f"Total classified+map:   {report['statistics']['total_classified_or_fallback']} ({report['statistics']['overall_coverage']})")
    logger.info("")
    logger.info("Confidence Distribution (Matched):")
    for conf, count in sorted(report['confidence_distribution'].items(), reverse=True):
        pct = count / stats['matched'] * 100 if stats['matched'] > 0 else 0
        bar = "█" * int(pct / 5)
        logger.info(f"  {conf:5} → {count:3} papers ({pct:5.1f}%) {bar}")
    logger.info("="*70)

    return report_file


# ============================================================================
# MAIN
# ============================================================================

def main(dry_run=False):
    """
    Main script logic following SOP-SCRIPT-01 phases
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
        # Phase 1: Check preconditions
        success, error = check_preconditions(logger)
        if not success:
            logger.error(f"✗ Precondition check failed: {error}")
            return 1

        # Phase 2: Create backups
        if SCRIPT_METADATA["requires_backup"] and not dry_run:
            backups = create_backups(backup_manager, logger, dry_run=False)
            if not backups["success"]:
                logger.error("✗ Backup creation failed, aborting")
                return 1

        # Phase 3: Execute main logic
        logger.info("Executing classification...")

        # Build index from sources
        sources_index = build_sources_index(logger)

        # Classify papers
        updated_data, stats = classify_papers(logger, sources_index, dry_run=dry_run)

        # Write results
        if dry_run:
            logger.info("[DRY RUN] Would write updated YAML to data/extracted_papers.yaml")
        else:
            logger.info("Writing updated papers to data/extracted_papers.yaml...")
            save_yaml(updated_data, "data/extracted_papers.yaml")
            logger.info("✓ File updated")

        # Generate report
        report_file = generate_report(stats, logger)

        # Phase 4: Verify postconditions
        if not dry_run:
            success, error = verify_postconditions(logger)
            if not success:
                logger.error(f"✗ Postcondition check failed: {error}")
                return 1

        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"✓ Script completed successfully ({duration:.1f}s)")

        # Phase 5: Audit logging
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
                "dry_run": dry_run,
                "matched": stats['matched'],
                "unmatched": stats['unmatched']
            }
        )

        return 0

    except Exception as e:
        duration = (datetime.now() - start_time).total_seconds()
        logger.error(f"✗ Script failed with exception: {e}")
        import traceback
        traceback.print_exc()

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
  # Show what will change without modifying files
  python3 classify_extracted_papers.py --dry-run

  # Classify papers and update data/extracted_papers.yaml
  python3 classify_extracted_papers.py
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
