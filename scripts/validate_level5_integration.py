#!/usr/bin/env python3
"""
validate_level5_integration.py - Validate Level 5 Paper Integration

Prüft alle 13 Komponenten einer Level 5 (FULL) Paper-Integration:

1. BibTeX Entry - Paper in bcm_master.bib mit EBF-Feldern
2. Paper-YAML - SSOT in data/paper-references/PAP-{key}.yaml
3. Case Registry - Case in data/case-registry.yaml
4. Theory Catalog - Theorie in data/theory-catalog.yaml
5. Parameter Registry - Parameter in data/parameter-registry.yaml
6. LIT-Appendix - Integration in LIT-Appendix
7. BCM2 Context - Kontext-Faktoren in BCM2
8. Chapter-Appendix Mapping - Mapping aktualisiert
9. CORE Extensions - 6-Factor Framework angewendet
10. Full-Text Archive - Volltext in data/paper-texts/
11. Cross-References - Bidirektionale Verweise
12. Chapter Relevance - high_relevance Kapitel mit status: completed
13. Cross-DB Consistency - theory_id/case_id über alle Datenbanken konsistent

ATOMIC ID RULE:
  Paper-YAML ist die Single Source of Truth (SSOT) für alle IDs.
  Alle anderen Registries MÜSSEN von Paper-YAML ableiten.
  Check 13 validiert diese Konsistenz automatisch.

Usage:
    python scripts/validate_level5_integration.py PAP-benabou_2022_hurts_ask
    python scripts/validate_level5_integration.py --all
    python scripts/validate_level5_integration.py --list

Author: EBF Framework Team
Version: 1.1.0
Date: 2026-02-05
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import yaml

# Paths relative to repository root
REPO_ROOT = Path(__file__).parent.parent
BIB_PATH = REPO_ROOT / "bibliography" / "bcm_master.bib"
PAPER_REFS_PATH = REPO_ROOT / "data" / "paper-references"
PAPER_TEXTS_PATH = REPO_ROOT / "data" / "paper-texts"
CASE_REGISTRY_PATH = REPO_ROOT / "data" / "case-registry.yaml"
THEORY_CATALOG_PATH = REPO_ROOT / "data" / "theory-catalog.yaml"
PARAM_REGISTRY_PATH = REPO_ROOT / "data" / "parameter-registry.yaml"
CHAPTER_MAPPING_PATH = REPO_ROOT / "docs" / "frameworks" / "chapter-appendix-mapping.yaml"
BCM2_CONTEXT_PATH = REPO_ROOT / "data" / "dr-datareq" / "sources" / "context"
APPENDICES_PATH = REPO_ROOT / "appendices"


class Level5Validator:
    """Validates Level 5 Paper Integration completeness."""

    def __init__(self, paper_key: str):
        """
        Initialize validator with paper key.

        Args:
            paper_key: Paper identifier (e.g., 'benabou_2022_hurts_ask' or 'PAP-benabou_2022_hurts_ask')
        """
        # Normalize key (remove PAP- prefix if present)
        self.paper_key = paper_key.replace("PAP-", "")
        self.full_key = f"PAP-{self.paper_key}"

        # Results storage
        self.results: Dict[str, Dict] = {}
        self.paper_yaml: Optional[Dict] = None

    def load_paper_yaml(self) -> bool:
        """Load the Paper-YAML file."""
        yaml_path = PAPER_REFS_PATH / f"{self.full_key}.yaml"
        if not yaml_path.exists():
            self.results["paper_yaml"] = {
                "status": "FAIL",
                "message": f"Paper-YAML not found: {yaml_path}"
            }
            return False

        try:
            with open(yaml_path, 'r', encoding='utf-8') as f:
                self.paper_yaml = yaml.safe_load(f)
            return True
        except Exception as e:
            self.results["paper_yaml"] = {
                "status": "FAIL",
                "message": f"Error loading Paper-YAML: {e}"
            }
            return False

    def check_bibtex(self) -> Tuple[str, str]:
        """Check BibTeX entry exists with EBF fields."""
        if not BIB_PATH.exists():
            return "FAIL", f"BibTeX file not found: {BIB_PATH}"

        with open(BIB_PATH, 'r', encoding='utf-8') as f:
            bib_content = f.read()

        # Check for entry
        pattern = rf'@\w+\{{{self.paper_key},'
        entry_start = re.search(pattern, bib_content)
        if not entry_start:
            return "FAIL", f"BibTeX entry '{self.paper_key}' not found"

        # Extract entry by counting braces (BibTeX entries have nested {})
        start_pos = entry_start.start()
        brace_count = 0
        end_pos = start_pos
        for i, char in enumerate(bib_content[start_pos:]):
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    end_pos = start_pos + i + 1
                    break

        entry = bib_content[start_pos:end_pos]

        # Check for EBF fields (case-insensitive search in full entry)
        required_fields = ['use_for', 'theory_support', 'evidence_tier']
        missing = [f for f in required_fields if f not in entry.lower()]
        if missing:
            return "WARN", f"Missing EBF fields: {missing}"

        return "PASS", "BibTeX entry found with EBF fields"

    def check_paper_yaml(self) -> Tuple[str, str]:
        """Check Paper-YAML exists and has required sections."""
        yaml_path = PAPER_REFS_PATH / f"{self.full_key}.yaml"
        if not yaml_path.exists():
            return "FAIL", f"Paper-YAML not found: {yaml_path}"

        if not self.paper_yaml:
            if not self.load_paper_yaml():
                return "FAIL", "Could not load Paper-YAML"

        # Check required sections
        required = ['superkey', 'structural_characteristics', 'ebf_integration',
                   'ten_c_mapping', 'chapter_relevance']
        missing = [s for s in required if s not in self.paper_yaml]

        if missing:
            return "WARN", f"Missing sections: {missing}"

        return "PASS", "Paper-YAML complete"

    def check_case_registry(self) -> Tuple[str, str]:
        """Check case exists in case registry."""
        if not self.paper_yaml:
            return "SKIP", "Paper-YAML not loaded"

        # Get case_id from Paper-YAML
        case_integration = self.paper_yaml.get('case_integration', {})
        case_id = case_integration.get('case_id')

        if not case_id:
            return "FAIL", "No case_id in Paper-YAML case_integration"

        if not CASE_REGISTRY_PATH.exists():
            return "FAIL", f"Case registry not found: {CASE_REGISTRY_PATH}"

        with open(CASE_REGISTRY_PATH, 'r', encoding='utf-8') as f:
            content = f.read()

        if case_id in content:
            return "PASS", f"Case {case_id} found in registry"

        return "FAIL", f"Case {case_id} not found in case-registry.yaml"

    def check_theory_catalog(self) -> Tuple[str, str]:
        """Check theory exists in theory catalog."""
        if not self.paper_yaml:
            return "SKIP", "Paper-YAML not loaded"

        theory_integration = self.paper_yaml.get('theory_integration', {})
        theory_id = theory_integration.get('theory_id')

        if not theory_id:
            return "FAIL", "No theory_id in Paper-YAML theory_integration"

        if not THEORY_CATALOG_PATH.exists():
            return "FAIL", f"Theory catalog not found: {THEORY_CATALOG_PATH}"

        with open(THEORY_CATALOG_PATH, 'r', encoding='utf-8') as f:
            content = f.read()

        if theory_id in content:
            return "PASS", f"Theory {theory_id} found in catalog"

        return "FAIL", f"Theory {theory_id} not found in theory-catalog.yaml"

    def check_parameter_registry(self) -> Tuple[str, str]:
        """Check parameters exist in parameter registry."""
        if not self.paper_yaml:
            return "SKIP", "Paper-YAML not loaded"

        param_integration = self.paper_yaml.get('parameter_integration', [])

        if not param_integration:
            return "FAIL", "No parameters in Paper-YAML parameter_integration"

        if not PARAM_REGISTRY_PATH.exists():
            return "FAIL", f"Parameter registry not found: {PARAM_REGISTRY_PATH}"

        with open(PARAM_REGISTRY_PATH, 'r', encoding='utf-8') as f:
            content = f.read()

        found = []
        missing = []
        for param_id in param_integration:
            if param_id in content:
                found.append(param_id)
            else:
                missing.append(param_id)

        if missing:
            return "FAIL", f"Missing parameters: {missing}"

        return "PASS", f"All {len(found)} parameters found in registry"

    def check_lit_appendix(self) -> Tuple[str, str]:
        """Check LIT-Appendix integration."""
        if not self.paper_yaml:
            return "SKIP", "Paper-YAML not loaded"

        appendix_integration = self.paper_yaml.get('appendix_integration', {})
        primary_appendix = appendix_integration.get('primary_appendix')

        if not primary_appendix:
            return "FAIL", "No primary_appendix in Paper-YAML"

        # Search for appendix file
        appendix_files = list(APPENDICES_PATH.glob(f"{primary_appendix}*.tex"))
        if not appendix_files:
            return "FAIL", f"LIT-Appendix {primary_appendix} not found"

        # Check if paper is referenced in appendix
        appendix_file = appendix_files[0]
        with open(appendix_file, 'r', encoding='utf-8') as f:
            content = f.read()

        if self.paper_key in content or self.paper_key.replace('_', '') in content:
            return "PASS", f"Paper referenced in {appendix_file.name}"

        return "WARN", f"Paper may not be referenced in {appendix_file.name}"

    def check_bcm2_context(self) -> Tuple[str, str]:
        """Check BCM2 context factors."""
        if not self.paper_yaml:
            return "SKIP", "Paper-YAML not loaded"

        context_integration = self.paper_yaml.get('context_integration', {})
        bcm2_factors = context_integration.get('bcm2_factors', [])

        if not bcm2_factors:
            return "WARN", "No bcm2_factors in Paper-YAML context_integration"

        # Check if referenced BCM2 file exists
        bcm2_file = context_integration.get('bcm2_file')
        if bcm2_file:
            bcm2_path = REPO_ROOT / bcm2_file
            if bcm2_path.exists():
                # Check for factor IDs in file
                with open(bcm2_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                found_factors = []
                for factor in bcm2_factors:
                    factor_id = factor.get('id', '')
                    if factor_id in content:
                        found_factors.append(factor_id)

                if len(found_factors) == len(bcm2_factors):
                    return "PASS", f"All {len(found_factors)} BCM2 factors found"
                else:
                    return "WARN", f"Only {len(found_factors)}/{len(bcm2_factors)} factors found"

        return "WARN", "BCM2 file not specified or not found"

    def check_chapter_mapping(self) -> Tuple[str, str]:
        """Check chapter-appendix mapping."""
        if not CHAPTER_MAPPING_PATH.exists():
            return "FAIL", f"Chapter mapping not found: {CHAPTER_MAPPING_PATH}"

        with open(CHAPTER_MAPPING_PATH, 'r', encoding='utf-8') as f:
            content = f.read()

        if self.paper_key in content:
            return "PASS", "Paper referenced in chapter-appendix-mapping.yaml"

        return "FAIL", "Paper not in chapter-appendix-mapping.yaml"

    def check_core_extensions(self) -> Tuple[str, str]:
        """Check CORE extensions (6-Factor Framework)."""
        if not self.paper_yaml:
            return "SKIP", "Paper-YAML not loaded"

        appendix_integration = self.paper_yaml.get('appendix_integration', {})
        core_integrations = appendix_integration.get('core_appendix_integrations', [])

        if not core_integrations:
            return "WARN", "No core_appendix_integrations in Paper-YAML"

        completed_count = 0
        cross_ref_count = 0

        # Check for axioms in CORE appendices or chapters
        for core in core_integrations:
            appendix = core.get('appendix')
            axiom = core.get('axiom')
            status = core.get('status', 'cross_reference')
            chapter = core.get('chapter')  # Check if axiom is in a chapter instead

            # Only verify axiom location for completed integrations
            if status == 'completed' and axiom:
                if chapter:
                    # Axiom is in chapter, not appendix
                    chapters_path = REPO_ROOT / "chapters"
                    chapter_files = list(chapters_path.glob(f"{chapter:02d}_*.tex")) if isinstance(chapter, int) else list(chapters_path.glob(f"{chapter}_*.tex"))
                    if chapter_files:
                        with open(chapter_files[0], 'r', encoding='utf-8') as f:
                            content = f.read()
                        if axiom in content:
                            completed_count += 1
                        else:
                            return "WARN", f"Axiom {axiom} not found in Chapter {chapter}"
                    else:
                        return "WARN", f"Chapter {chapter} file not found"
                elif appendix:
                    # Axiom is in appendix
                    appendix_files = list(APPENDICES_PATH.glob(f"{appendix}*.tex"))
                    if appendix_files:
                        with open(appendix_files[0], 'r', encoding='utf-8') as f:
                            content = f.read()
                        if axiom in content:
                            completed_count += 1
                        else:
                            return "WARN", f"Axiom {axiom} not found in {appendix}"
            elif status == 'cross_reference':
                cross_ref_count += 1

        total = completed_count + cross_ref_count
        if total == 0:
            return "WARN", "No CORE integrations verified"

        return "PASS", f"CORE extensions: {completed_count} completed, {cross_ref_count} cross-refs"

    def check_fulltext_archive(self) -> Tuple[str, str]:
        """Check full-text archive."""
        fulltext_path = PAPER_TEXTS_PATH / f"{self.full_key}.md"

        if not fulltext_path.exists():
            return "FAIL", f"Full-text not found: {fulltext_path}"

        # Check file has content
        file_size = fulltext_path.stat().st_size
        if file_size < 1000:  # Less than 1KB is suspicious
            return "WARN", f"Full-text file seems too small ({file_size} bytes)"

        return "PASS", f"Full-text archived ({file_size:,} bytes)"

    def check_cross_references(self) -> Tuple[str, str]:
        """Check bidirectional cross-references."""
        issues = []
        checks_passed = 0

        # Check Paper-YAML references Case
        if self.paper_yaml:
            case_id = self.paper_yaml.get('case_integration', {}).get('case_id')
            if case_id:
                # Check Case references Paper
                if CASE_REGISTRY_PATH.exists():
                    with open(CASE_REGISTRY_PATH, 'r', encoding='utf-8') as f:
                        case_content = f.read()
                    if self.paper_key in case_content:
                        checks_passed += 1
                    else:
                        issues.append(f"Case {case_id} doesn't reference paper")

            # Check Theory references Paper
            theory_id = self.paper_yaml.get('theory_integration', {}).get('theory_id')
            if theory_id:
                if THEORY_CATALOG_PATH.exists():
                    with open(THEORY_CATALOG_PATH, 'r', encoding='utf-8') as f:
                        theory_content = f.read()
                    if self.paper_key in theory_content:
                        checks_passed += 1
                    else:
                        issues.append(f"Theory {theory_id} doesn't reference paper")

        if issues:
            return "WARN", f"Cross-ref issues: {'; '.join(issues)}"

        if checks_passed > 0:
            return "PASS", f"{checks_passed} bidirectional references verified"

        return "SKIP", "No cross-references to verify"

    def check_chapter_relevance(self) -> Tuple[str, str]:
        """Check all high_relevance chapters have status: completed."""
        if not self.paper_yaml:
            return "SKIP", "Paper-YAML not loaded"

        chapter_relevance = self.paper_yaml.get('chapter_relevance', {})
        high_relevance = chapter_relevance.get('high_relevance', [])

        if not high_relevance:
            return "SKIP", "No high_relevance chapters defined"

        completed = []
        pending = []

        for chapter_info in high_relevance:
            chapter_num = chapter_info.get('chapter')
            status = chapter_info.get('status', 'pending')
            action = chapter_info.get('action', 'unknown')

            if status == 'completed':
                completed.append(chapter_num)
            else:
                pending.append(f"Ch{chapter_num}: {action}")

        if pending:
            return "FAIL", f"Pending chapters: {'; '.join(pending)}"

        return "PASS", f"All {len(completed)} high-relevance chapters completed"

    def check_cross_db_consistency(self) -> Tuple[str, str]:
        """
        Check 13: Cross-Database ID Consistency

        Verifies that IDs (theory_id, case_id) in Paper-YAML match
        the corresponding entries in Case Registry and Theory Catalog.

        ATOMIC ID RULE: Paper-YAML superkey is the Single Source of Truth.
        All other registries MUST derive IDs from Paper-YAML.

        Uses regex-based extraction instead of full YAML parsing for robustness.
        """
        if not self.paper_yaml:
            return "SKIP", "Paper-YAML not loaded"

        mismatches = []
        verified = []

        # Get IDs from Paper-YAML (SSOT)
        paper_theory_id = self.paper_yaml.get('theory_integration', {}).get('theory_id')
        paper_case_id = self.paper_yaml.get('case_integration', {}).get('case_id')

        # Verify Case Registry consistency using regex (more robust than YAML parsing)
        if paper_case_id and CASE_REGISTRY_PATH.exists():
            try:
                with open(CASE_REGISTRY_PATH, 'r', encoding='utf-8') as f:
                    case_content = f.read()

                # Find the case block using regex
                # Pattern: Find case_id, then look for theory_id nearby
                case_pattern = rf'id:\s*{re.escape(paper_case_id)}.*?(?=\n  - id:|\n- id:|\Z)'
                case_match = re.search(case_pattern, case_content, re.DOTALL)

                if case_match:
                    case_block = case_match.group(0)

                    # Extract theory_id from case block
                    theory_match = re.search(r'theory_id:\s*(MS-[A-Z]{2}-\d{3})', case_block)
                    if theory_match:
                        case_theory_id = theory_match.group(1)
                        if paper_theory_id:
                            if case_theory_id != paper_theory_id:
                                mismatches.append(
                                    f"theory_id: Paper-YAML={paper_theory_id}, "
                                    f"Case({paper_case_id})={case_theory_id}"
                                )
                            else:
                                verified.append(f"theory_id in {paper_case_id}")

                    # Check paper reference in case
                    paper_match = re.search(r'paper_key:\s*(\S+)', case_block)
                    if paper_match:
                        case_paper = paper_match.group(1)
                        if case_paper != self.paper_key:
                            mismatches.append(
                                f"paper_key: Paper-YAML={self.paper_key}, "
                                f"Case={case_paper}"
                            )
            except Exception as e:
                return "WARN", f"Could not read Case Registry: {e}"

        # Verify Theory Catalog consistency
        if paper_theory_id and THEORY_CATALOG_PATH.exists():
            try:
                with open(THEORY_CATALOG_PATH, 'r', encoding='utf-8') as f:
                    theory_content = f.read()

                # Check if theory exists and paper is referenced
                if paper_theory_id in theory_content:
                    if self.paper_key in theory_content:
                        verified.append(f"paper in {paper_theory_id}")
                    else:
                        # This is acceptable - theory may predate paper
                        pass
            except Exception as e:
                return "WARN", f"Could not parse Theory Catalog: {e}"

        if mismatches:
            return "FAIL", f"ID mismatches found: {'; '.join(mismatches)}"

        if verified:
            return "PASS", f"Cross-DB consistent: {', '.join(verified)}"

        return "SKIP", "No cross-database IDs to verify"

    def validate_all(self) -> Dict[str, Dict]:
        """Run all validation checks."""
        # Load Paper-YAML first (needed by other checks)
        self.load_paper_yaml()

        checks = [
            ("1. BibTeX Entry", self.check_bibtex),
            ("2. Paper-YAML", self.check_paper_yaml),
            ("3. Case Registry", self.check_case_registry),
            ("4. Theory Catalog", self.check_theory_catalog),
            ("5. Parameter Registry", self.check_parameter_registry),
            ("6. LIT-Appendix", self.check_lit_appendix),
            ("7. BCM2 Context", self.check_bcm2_context),
            ("8. Chapter-Appendix Mapping", self.check_chapter_mapping),
            ("9. CORE Extensions", self.check_core_extensions),
            ("10. Full-Text Archive", self.check_fulltext_archive),
            ("11. Cross-References", self.check_cross_references),
            ("12. Chapter Relevance", self.check_chapter_relevance),
            ("13. Cross-DB Consistency", self.check_cross_db_consistency),
        ]

        for name, check_func in checks:
            status, message = check_func()
            self.results[name] = {"status": status, "message": message}

        return self.results

    def get_summary(self) -> Dict:
        """Get validation summary."""
        passed = sum(1 for r in self.results.values() if r["status"] == "PASS")
        warned = sum(1 for r in self.results.values() if r["status"] == "WARN")
        failed = sum(1 for r in self.results.values() if r["status"] == "FAIL")
        skipped = sum(1 for r in self.results.values() if r["status"] == "SKIP")

        total = len(self.results)
        compliance = (passed / total * 100) if total > 0 else 0

        return {
            "paper_key": self.paper_key,
            "passed": passed,
            "warned": warned,
            "failed": failed,
            "skipped": skipped,
            "total": total,
            "compliance": compliance,
            "is_complete": failed == 0
        }


def print_results(validator: Level5Validator):
    """Print validation results in formatted output."""
    results = validator.results
    summary = validator.get_summary()

    print(f"\n{'='*70}")
    print(f"  LEVEL 5 INTEGRATION VALIDATION: {validator.full_key}")
    print(f"{'='*70}\n")

    # Status symbols
    symbols = {"PASS": "✅", "WARN": "⚠️", "FAIL": "❌", "SKIP": "⏭️"}

    for name, result in results.items():
        symbol = symbols.get(result["status"], "?")
        print(f"  {symbol} {name}")
        print(f"     {result['message']}\n")

    print(f"{'─'*70}")
    print(f"  SUMMARY:")
    print(f"  ├── Passed:  {summary['passed']:2d} / {summary['total']}")
    print(f"  ├── Warned:  {summary['warned']:2d} / {summary['total']}")
    print(f"  ├── Failed:  {summary['failed']:2d} / {summary['total']}")
    print(f"  ├── Skipped: {summary['skipped']:2d} / {summary['total']}")
    print(f"  └── Compliance: {summary['compliance']:.1f}%")
    print(f"{'─'*70}")

    if summary['is_complete']:
        print(f"  ✅ LEVEL 5 INTEGRATION COMPLETE")
    else:
        print(f"  ❌ LEVEL 5 INTEGRATION INCOMPLETE - {summary['failed']} components missing")

    print(f"{'='*70}\n")


def list_level5_papers() -> List[str]:
    """List all papers with Paper-YAML files."""
    papers = []
    for yaml_file in PAPER_REFS_PATH.glob("PAP-*.yaml"):
        papers.append(yaml_file.stem)
    return sorted(papers)


def main():
    parser = argparse.ArgumentParser(
        description="Validate Level 5 Paper Integration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python scripts/validate_level5_integration.py PAP-benabou_2022_hurts_ask
    python scripts/validate_level5_integration.py benabou_2022_hurts_ask
    python scripts/validate_level5_integration.py --all
    python scripts/validate_level5_integration.py --list
        """
    )

    parser.add_argument(
        "paper_key",
        nargs="?",
        help="Paper key (e.g., PAP-benabou_2022_hurts_ask)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Validate all papers with Paper-YAML files"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all papers with Paper-YAML files"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as failures"
    )

    args = parser.parse_args()

    if args.list:
        papers = list_level5_papers()
        print(f"\nFound {len(papers)} papers with Paper-YAML files:\n")
        for paper in papers:
            print(f"  - {paper}")
        print()
        return 0

    if args.all:
        papers = list_level5_papers()
        all_summaries = []

        for paper in papers:
            validator = Level5Validator(paper)
            validator.validate_all()
            summary = validator.get_summary()
            all_summaries.append(summary)

            if not args.json:
                print_results(validator)

        if args.json:
            import json
            print(json.dumps(all_summaries, indent=2))

        # Overall summary
        complete = sum(1 for s in all_summaries if s['is_complete'])
        print(f"\n{'='*70}")
        print(f"  OVERALL: {complete}/{len(all_summaries)} papers with complete Level 5 integration")
        print(f"{'='*70}\n")

        return 0 if complete == len(all_summaries) else 1

    if not args.paper_key:
        parser.print_help()
        return 1

    validator = Level5Validator(args.paper_key)
    results = validator.validate_all()
    summary = validator.get_summary()

    if args.json:
        import json
        output = {
            "paper_key": validator.paper_key,
            "results": results,
            "summary": summary
        }
        print(json.dumps(output, indent=2))
    else:
        print_results(validator)

    # Exit code based on validation result
    if args.strict:
        return 0 if summary['failed'] == 0 and summary['warned'] == 0 else 1
    else:
        return 0 if summary['failed'] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
