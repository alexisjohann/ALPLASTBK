#!/usr/bin/env python3
"""
deprecate_migration_scripts.py — Add DEPRECATED headers to one-time migration scripts.

This script itself is a one-time tool. After running, it can be deleted.

Usage:
    python scripts/deprecate_migration_scripts.py --dry-run   # Preview changes
    python scripts/deprecate_migration_scripts.py              # Apply changes
"""

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
SCRIPTS_DIR = ROOT / "scripts"

# ──────────────────────────────────────────────────────────────
# Scripts to deprecate, grouped by category
# ──────────────────────────────────────────────────────────────

DEPRECATED_SCRIPTS = {
    # Bulk add scripts (one-time data entry, papers already in BIB)
    "add_50_behavioral_econ_papers.py": "Einmalige Bulk-Datenerfassung: 50 Behavioral Econ Papers",
    "add_50_falk_papers.py": "Einmalige Bulk-Datenerfassung: 50 Falk Papers",
    "add_50_list_papers.py": "Einmalige Bulk-Datenerfassung: 50 List Papers",
    "add_50_malmendier_papers.py": "Einmalige Bulk-Datenerfassung: 50 Malmendier Papers",
    "add_50_shafir_papers.py": "Einmalige Bulk-Datenerfassung: 25 Shafir Papers",
    "add_ariely_papers_20.py": "Einmalige Bulk-Datenerfassung: 20 Ariely Papers",
    "add_autor_papers_20.py": "Einmalige Bulk-Datenerfassung: 20 Autor Papers",
    "add_camerer_papers_20.py": "Einmalige Bulk-Datenerfassung: 20 Camerer Papers",
    "add_fehr_final_6.py": "Einmalige Bulk-Datenerfassung: 6 Fehr Papers",
    "add_fehr_final_6_more.py": "Einmalige Bulk-Datenerfassung: 6 weitere Fehr Papers",
    "add_fehr_papers_100.py": "Einmalige Bulk-Datenerfassung: 100 Fehr Papers",
    "add_fehr_papers_50_more.py": "Einmalige Bulk-Datenerfassung: 50 weitere Fehr Papers",
    "add_gaechter_papers.py": "Einmalige Bulk-Datenerfassung: 20 Gaechter Papers",
    "add_kahneman_final_18.py": "Einmalige Bulk-Datenerfassung: 18 Kahneman Papers",
    "add_kahneman_papers_50.py": "Einmalige Bulk-Datenerfassung: 50 Kahneman Papers",
    "add_loewenstein_papers_20.py": "Einmalige Bulk-Datenerfassung: 20 Loewenstein Papers",
    "add_sunstein_papers_20.py": "Einmalige Bulk-Datenerfassung: 20 Sunstein Papers",
    "add_thaler_papers_20.py": "Einmalige Bulk-Datenerfassung: 20 Thaler Papers",
    "add_doi_urls.py": "Einmalige DOI/URL-Ergaenzung (Phase 3)",
    # LIT appendix generation (one-time)
    "generate_6_lit_appendices.py": "Einmalige LIT-Appendix-Generierung (Y, Z, AA, AB, AC, AD)",
    "generate_lit_appendices.py": "Einmalige LIT-Appendix-Generierung",
    "generate_lit_falk.py": "Einmalige LIT-FALK-Generierung (AE)",
    "generate_lit_malmendier.py": "Einmalige LIT-MALMENDIER-Generierung (AF)",
    "generate_lit_shafir.py": "Einmalige LIT-SHAFIR-Generierung (AG)",
    "regenerate_lit_aa.py": "Einmalige LIT-AA-Regenerierung",
    "update_lit_list.py": "Einmalige LIT-LIST-Aktualisierung (AB)",
    # Expansion / mining (one-time)
    "expand_mullainathan_papers.py": "Einmalige Mullainathan-Erweiterung",
    "expand_paper_database.py": "Einmalige Paper-DB-Erweiterung auf 50+",
    "complete_paper_database_50.py": "Einmalige Paper-DB-Vervollstaendigung",
    "mine_journal_papers.py": "Einmaliges Knowledge-Mining aus LLM-Training",
    # DOI population (one-time)
    "populate_dois_comprehensive.py": "Einmalige DOI-Ergaenzung (comprehensive)",
    "populate_top100_dois.py": "Einmalige DOI-Ergaenzung (Top 100)",
    "phase3_complete_journal_mapping.py": "Einmaliges Journal-DOI-Mapping (Phase 3)",
    "phase3_massive_doi_expansion.py": "Einmalige DOI-Expansion (Phase 3)",
    # Migration scripts
    "migrate_paper_sources.py": "Einmalige Migration paper-sources.yaml zu PAP-*.yaml (TL-001)",
    "cleanup_stub_papers.py": "Einmalige Stub-Paper-Bereinigung",
    "analyze_paper_lit_mapping.py": "Einmalige Analyse Paper-LIT-Zuordnung",
    "paper_lit_matcher.py": "Einmalige lit_appendix-Zuweisung",
    "classify_evidence_tiers.py": "Einmalige Evidence-Tier-Klassifikation (ersetzt durch add_evidence_tier.py)",
}

# These scripts are NOT deprecated (still useful):
# - generate_bayesian_priors.py (used by /bayesian-priors skill)
# - extract_cases_from_papers.py (used by GitHub Actions)
# - case_paper_linker.py (reusable for new papers)
# - phase4_case_paper_linker.py (reusable)
# - phase5_intervention_analyzer.py (active pipeline)
# - phase5_intervention_design.py (active pipeline)
# - phase5_learnings_extractor.py (active pipeline)
# - phase6_decay_analyzer.py (active pipeline)
# - phase6_learnings_extractor.py (active pipeline)
# - phase6_longterm_tracker.py (active pipeline)

HEADER_TEMPLATE = """# ┌─────────────────────────────────────────────────────────────────────────┐
# │  ⚠️  DEPRECATED (2026-02-08)                                            │
# │                                                                         │
# │  {reason:<69s} │
# │  Kept for reference only.                                              │
# │                                                                         │
# │  SSOT: data/paper-references/PAP-*.yaml + bibliography/bcm_master.bib │
# │  Neue Papers: /integrate-paper Workflow                                │
# └─────────────────────────────────────────────────────────────────────────┘
"""


def add_deprecated_header(filepath, reason, dry_run=False):
    """Add DEPRECATED header to a Python script."""
    content = filepath.read_text(encoding="utf-8")

    # Skip if already deprecated
    if "DEPRECATED" in content[:500]:
        return "already_deprecated"

    lines = content.split("\n")
    header = HEADER_TEMPLATE.format(reason=reason)

    # Find insertion point: after shebang, before docstring
    insert_idx = 0
    if lines and lines[0].startswith("#!"):
        insert_idx = 1

    new_content = "\n".join(lines[:insert_idx]) + "\n" + header + "\n".join(lines[insert_idx:])

    # Also add DEPRECATED note to docstring if present
    docstring_match = re.search(r'("""[^\n]*\n)', new_content)
    if docstring_match:
        pos = docstring_match.end()
        new_content = (
            new_content[:pos]
            + "\n⚠️  DEPRECATED (2026-02-08) — See header for details.\n"
            + new_content[pos:]
        )

    if not dry_run:
        filepath.write_text(new_content, encoding="utf-8")
    return "updated"


def main():
    parser = argparse.ArgumentParser(description="Deprecate migration scripts")
    parser.add_argument("--dry-run", action="store_true", help="Preview only")
    args = parser.parse_args()

    updated = 0
    skipped = 0
    missing = 0

    prefix = "[DRY RUN] " if args.dry_run else ""

    for filename, reason in sorted(DEPRECATED_SCRIPTS.items()):
        filepath = SCRIPTS_DIR / filename
        if not filepath.exists():
            print(f"  ⚠️  {filename}: NOT FOUND (may have been renamed/deleted)")
            missing += 1
            continue

        status = add_deprecated_header(filepath, reason, dry_run=args.dry_run)
        if status == "already_deprecated":
            print(f"  ⏭️  {filename}: already deprecated")
            skipped += 1
        else:
            print(f"  ✅ {filename}: {reason[:50]}")
            updated += 1

    print(f"\n{prefix}Results:")
    print(f"  Updated:  {updated}")
    print(f"  Skipped:  {skipped} (already deprecated)")
    print(f"  Missing:  {missing}")
    print(f"  Total:    {updated + skipped + missing}")


if __name__ == "__main__":
    main()
