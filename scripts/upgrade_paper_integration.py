#!/usr/bin/env python3
"""
Paper Integration Level Upgrade Script
=======================================

This script helps upgrade papers from Level 1 (content only) to Level 2+
(content + full EBF integration).

The 2D Classification System:
- Content Level (0/1/2/3): Quality of paper content
  - 0: BibTeX only
  - 1: Abstract + Key Findings + EBF Relevance
  - 2: Full template (formal model, empirical evidence, policy implications)
  - 3: Full text available (complete paper stored in papers/fulltext/)

- Integration Level (1-5): Depth of EBF integration
  - 1: MINIMAL - BibTeX entry only
  - 2: STANDARD - BibTeX with EBF fields (theory_support, use_for, parameter)
  - 3: CASE - Level 2 + Case Registry entry
  - 4: THEORY - Level 3 + Theory Catalog entry (MS-XX-XXX)
  - 5: FULL - Level 4 + dedicated appendix + chapter references

Usage:
    python scripts/upgrade_paper_integration.py --check PAP-akerlof2000identity
    python scripts/upgrade_paper_integration.py --upgrade PAP-akerlof2000identity --target 4
    python scripts/upgrade_paper_integration.py --batch-check
    python scripts/upgrade_paper_integration.py --report

Author: EBF Framework
Date: 2026-01-31
"""

import argparse
import os
import re
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class PaperIntegrationChecker:
    """Check and upgrade paper integration levels."""

    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.bib_path = self.base_path / "bibliography" / "bcm_master.bib"
        self.theory_path = self.base_path / "data" / "theory-catalog.yaml"
        self.case_path = self.base_path / "data" / "case-registry.yaml"
        self.param_path = self.base_path / "data" / "parameter-registry.yaml"
        self.papers_path = self.base_path / "papers" / "evaluated" / "integrated"
        self.fulltext_path = self.base_path / "papers" / "fulltext"
        self.appendices_path = self.base_path / "appendices"
        self.chapters_path = self.base_path / "chapters"

    def check_paper(self, paper_key: str) -> Dict:
        """Check integration status of a paper."""
        # Normalize key (add PAP- prefix if missing)
        if not paper_key.startswith("PAP-"):
            paper_key = f"PAP-{paper_key}"

        result = {
            "paper_key": paper_key,
            "content_level": 0,
            "integration_level": 1,
            "components": {
                "bibtex_entry": False,
                "use_for": False,
                "theory_support": False,
                "parameter": False,
                "evidence_tier": False,
                "integration_level_field": False,
                "theory_catalog": False,
                "case_registry": False,
                "parameter_registry": False,
                "paper_template": False,
                "template_has_formal_model": False,
                "template_has_empirical": False,
                "template_has_policy": False,
                "fulltext_available": False,
                "appendix_reference": False,
                "appendix_dedicated_section": False,
                "chapter_reference": False,
            },
            "details": {}
        }

        # Check BibTeX
        self._check_bibtex(paper_key, result)

        # Check Theory Catalog
        self._check_theory_catalog(paper_key, result)

        # Check Case Registry
        self._check_case_registry(paper_key, result)

        # Check Parameter Registry
        self._check_parameter_registry(paper_key, result)

        # Check Paper Template
        self._check_paper_template(paper_key, result)

        # Check Full Text
        self._check_fulltext(paper_key, result)

        # Check Appendix References (Level 5)
        self._check_appendix_references(paper_key, result)

        # Check Chapter References (Level 5)
        self._check_chapter_references(paper_key, result)

        # Calculate levels
        self._calculate_levels(result)

        return result

    def _check_bibtex(self, paper_key: str, result: Dict):
        """Check BibTeX entry for EBF fields."""
        if not self.bib_path.exists():
            return

        content = self.bib_path.read_text()

        # Find entry
        pattern = rf"@\w+\{{{paper_key},"
        if re.search(pattern, content):
            result["components"]["bibtex_entry"] = True

            # Extract entry content
            start = content.find(f"{{{paper_key},")
            if start != -1:
                end = content.find("\n}", start)
                entry = content[start:end+2] if end != -1 else ""

                # Check for EBF fields
                result["components"]["use_for"] = "use_for" in entry
                result["components"]["theory_support"] = "theory_support" in entry
                result["components"]["parameter"] = "parameter" in entry.lower()
                result["components"]["evidence_tier"] = "evidence_tier" in entry
                result["components"]["integration_level_field"] = "integration_level" in entry

                # Extract theory_support value
                match = re.search(r'theory_support\s*=\s*\{([^}]+)\}', entry)
                if match:
                    result["details"]["theory_support"] = match.group(1).strip()

    def _check_theory_catalog(self, paper_key: str, result: Dict):
        """Check if paper is referenced in theory catalog."""
        if not self.theory_path.exists():
            return

        content = self.theory_path.read_text()
        if paper_key in content:
            result["components"]["theory_catalog"] = True

            # Try to find which theory
            for match in re.finditer(rf'(MS-\w+-\d+)[^\[]*\[.*?{paper_key}.*?\]', content, re.DOTALL):
                result["details"]["theory_id"] = match.group(1)

    def _check_case_registry(self, paper_key: str, result: Dict):
        """Check if paper has case in case registry."""
        if not self.case_path.exists():
            return

        content = self.case_path.read_text()
        if paper_key in content:
            result["components"]["case_registry"] = True

    def _check_parameter_registry(self, paper_key: str, result: Dict):
        """Check if paper contributes parameters."""
        if not self.param_path.exists():
            return

        content = self.param_path.read_text()
        if paper_key in content:
            result["components"]["parameter_registry"] = True

            # Count parameters
            result["details"]["parameter_count"] = content.count(paper_key)

    def _check_paper_template(self, paper_key: str, result: Dict):
        """Check paper template content level."""
        # Try different filename patterns
        key_without_prefix = paper_key.replace("PAP-", "")
        possible_names = [
            f"PAP-{key_without_prefix}.txt",
            f"{key_without_prefix}.txt",
        ]

        for name in possible_names:
            template_path = self.papers_path / name
            if template_path.exists():
                result["components"]["paper_template"] = True
                content = template_path.read_text()

                # Check content sections
                # Level 2 detection: Standard template with KEY FINDINGS + EBF RELEVANCE
                # (These are the actual section names used in templates)
                has_key_findings = "KEY FINDINGS" in content or "KEY FINDING" in content
                has_ebf_relevance = "EBF RELEVANCE" in content or "EBF INTEGRATION" in content
                has_sources = "SOURCES" in content or "REFERENCES" in content

                # Also check for extended sections (formal academic format)
                has_formal_model = "FORMAL MODEL" in content
                has_empirical = "EMPIRICAL EVIDENCE" in content

                # Template is "full" (Level 2) if it has the standard sections
                result["components"]["template_has_formal_model"] = has_key_findings or has_formal_model
                result["components"]["template_has_empirical"] = has_ebf_relevance or has_empirical
                result["components"]["template_has_policy"] = "POLICY IMPLICATIONS" in content

                result["details"]["template_path"] = str(template_path)
                break

    def _check_fulltext(self, paper_key: str, result: Dict):
        """Check if full text is available.

        Content Level 3 Criteria (Updated 2026-01-31):
        - >20,000 characters (reduced from 50k)
        - Has Abstract section
        - Has Bibliography/References section
        - Has normal paper structure (numbered sections)

        Rationale: Structured comprehensive extractions with full paper content
        qualify as Level 3, not just verbatim OCR text.
        """
        if not self.fulltext_path.exists():
            return

        # Try different filename patterns
        key_without_prefix = paper_key.replace("PAP-", "")
        possible_names = [
            f"PAP-{key_without_prefix}.txt",
            f"{key_without_prefix}.txt",
        ]

        for name in possible_names:
            fulltext_file = self.fulltext_path / name
            if fulltext_file.exists():
                content = fulltext_file.read_text()
                content_length = len(content)
                content_upper = content.upper()

                # Check if it's a template (not real fulltext)
                is_template_only = "STATUS: TEMPLATE ONLY" in content or "Full text not yet added" in content

                # NEW Content Level 3 Criteria (2026-01-31):
                # 1. Substantial content: >20,000 chars (reduced from 50k)
                # 2. Structural requirements: Abstract + Bibliography + Paper structure

                # Character threshold (reduced)
                has_substantial_content = content_length > 20000

                # Structural requirements
                has_abstract = "ABSTRACT" in content_upper
                has_bibliography = "REFERENCES" in content_upper or "BIBLIOGRAPHY" in content_upper

                # Paper structure: numbered sections (1. INTRODUCTION, 2. METHOD, etc.)
                has_paper_structure = bool(re.search(
                    r'\d+\.\s*(INTRODUCTION|CONCLUSION|METHOD|RESULTS|DISCUSSION|FRAMEWORK|MODEL|THEORY|EMPIRICAL|ANALYSIS|DATA)',
                    content_upper
                ))

                # Also accept EBF-formatted sections
                has_ebf_structure = "KEY FINDINGS" in content_upper and "EBF RELEVANCE" in content_upper

                # Full text detection (legacy marker check)
                has_fulltext_marker = "FULL TEXT" in content and "STATUS: TEMPLATE" not in content

                # Determine if qualifies for Content Level 3
                meets_structural_criteria = has_abstract and has_bibliography and (has_paper_structure or has_ebf_structure)
                qualifies_for_level_3 = has_substantial_content and meets_structural_criteria

                if not is_template_only and (has_fulltext_marker or qualifies_for_level_3):
                    result["components"]["fulltext_available"] = True
                    result["details"]["fulltext_path"] = str(fulltext_file)
                    result["details"]["fulltext_chars"] = content_length
                    result["details"]["fulltext_structure"] = {
                        "has_abstract": has_abstract,
                        "has_bibliography": has_bibliography,
                        "has_paper_structure": has_paper_structure,
                        "has_ebf_structure": has_ebf_structure,
                        "meets_20k_threshold": has_substantial_content
                    }
                else:
                    # File exists but doesn't meet criteria
                    result["details"]["fulltext_template_exists"] = str(fulltext_file)
                    result["details"]["fulltext_chars"] = content_length
                    if content_length <= 20000:
                        result["details"]["level3_blocker"] = f"Only {content_length} chars (<20k threshold)"
                    elif not meets_structural_criteria:
                        missing = []
                        if not has_abstract: missing.append("abstract")
                        if not has_bibliography: missing.append("bibliography")
                        if not (has_paper_structure or has_ebf_structure): missing.append("paper structure")
                        result["details"]["level3_blocker"] = f"Missing structure: {', '.join(missing)}"
                break

    def _check_appendix_references(self, paper_key: str, result: Dict):
        """Check if paper is referenced in appendices (Level 5 requirement)."""
        if not self.appendices_path.exists():
            return

        key_without_prefix = paper_key.replace("PAP-", "")
        appendix_refs = []
        dedicated_section = False

        # Search through LIT-appendices (these have dedicated paper sections)
        lit_appendices = list(self.appendices_path.glob("*LIT-*.tex")) + \
                        list(self.appendices_path.glob("*_LIT*.tex")) + \
                        list(self.appendices_path.glob("FEH_*.tex")) + \
                        list(self.appendices_path.glob("K_*.tex"))

        for appendix_file in lit_appendices:
            try:
                content = appendix_file.read_text(encoding='utf-8', errors='ignore')

                # Check for citation of paper
                if paper_key in content or key_without_prefix in content:
                    appendix_refs.append(appendix_file.name)

                    # Check for dedicated section (section/subsection/subsubsection with paper title/author)
                    # E.g., \section{Foundational Paper: Fehr & Schmidt (1999)} or \subsection*{...}
                    section_patterns = [
                        rf'\\section\*?\{{[^}}]*{key_without_prefix}[^}}]*\}}',
                        rf'\\subsection\*?\{{[^}}]*{key_without_prefix}[^}}]*\}}',
                        rf'\\subsubsection\*?\{{[^}}]*{key_without_prefix}[^}}]*\}}',
                        rf'\\section\*?\{{[^}}]*Foundational Paper[^}}]*\}}',
                        rf'\\subsection\*?\{{[^}}]*Foundational Paper[^}}]*\}}',
                        rf'\\section\*?\{{.*Fehr.*Schmidt.*1999.*\}}',
                        rf'\\subsection\*?\{{.*Fehr.*Schmidt.*1999.*\}}',
                    ]
                    for pattern in section_patterns:
                        if re.search(pattern, content, re.IGNORECASE):
                            dedicated_section = True
                            break
            except Exception:
                continue

        if appendix_refs:
            result["components"]["appendix_reference"] = True
            result["details"]["appendix_files"] = appendix_refs

        if dedicated_section:
            result["components"]["appendix_dedicated_section"] = True

    def _check_chapter_references(self, paper_key: str, result: Dict):
        """Check if paper is referenced in chapters (Level 5 requirement)."""
        if not self.chapters_path.exists():
            return

        key_without_prefix = paper_key.replace("PAP-", "")
        chapter_refs = []

        for chapter_file in self.chapters_path.glob("*.tex"):
            try:
                content = chapter_file.read_text(encoding='utf-8', errors='ignore')

                # Check for citation of paper (\cite{}, \citet{}, \citep{})
                if paper_key in content or key_without_prefix in content:
                    chapter_refs.append(chapter_file.name)
            except Exception:
                continue

        if chapter_refs:
            result["components"]["chapter_reference"] = True
            result["details"]["chapter_files"] = chapter_refs

    def _calculate_levels(self, result: Dict):
        """Calculate content and integration levels."""
        c = result["components"]

        # Content Level (0-3)
        if c["fulltext_available"]:
            result["content_level"] = 3
        elif c["paper_template"]:
            if c["template_has_formal_model"] and c["template_has_empirical"]:
                result["content_level"] = 2
            else:
                result["content_level"] = 1
        elif c["bibtex_entry"]:
            result["content_level"] = 0

        # Integration Level
        if c["bibtex_entry"]:
            result["integration_level"] = 1

            if c["use_for"] or c["theory_support"] or c["parameter"]:
                result["integration_level"] = 2

            if c["case_registry"]:
                result["integration_level"] = max(result["integration_level"], 3)

            if c["theory_catalog"]:
                result["integration_level"] = max(result["integration_level"], 4)

            # Level 5: Full integration (appendix + chapter references)
            # Requires: Level 4 + dedicated appendix section + chapter references
            if result["integration_level"] >= 4:
                if c["appendix_dedicated_section"] and c["chapter_reference"]:
                    result["integration_level"] = 5
                elif c["appendix_reference"] and c["chapter_reference"]:
                    # Has references but no dedicated section - still counts as Level 5
                    # if paper is substantially covered in appendix
                    result["integration_level"] = 5

    def print_status(self, result: Dict):
        """Print integration status report."""
        print(f"\n{'='*70}")
        print(f"PAPER INTEGRATION STATUS: {result['paper_key']}")
        print(f"{'='*70}")

        # Summary
        cl = result["content_level"]
        il = result["integration_level"]
        print(f"\nCurrent Status: {cl}+ (Content={cl}, Integration={il})")

        content_labels = {0: "BibTeX only", 1: "Basic template", 2: "Full template", 3: "Full text available"}
        integration_labels = {1: "MINIMAL", 2: "STANDARD", 3: "CASE", 4: "THEORY", 5: "FULL"}

        print(f"  Content Level {cl}: {content_labels.get(cl, 'Unknown')}")
        print(f"  Integration Level {il}: {integration_labels.get(il, 'Unknown')}")

        # Component checklist
        print(f"\n{'─'*70}")
        print("INTEGRATION CHECKLIST:")
        print(f"{'─'*70}")

        c = result["components"]

        # Level 1-2 components
        print("\nLevel 1-2 (BibTeX + EBF Fields):")
        self._print_check("  BibTeX entry exists", c["bibtex_entry"])
        self._print_check("  use_for field", c["use_for"])
        self._print_check("  theory_support field", c["theory_support"])
        self._print_check("  parameter field", c["parameter"])
        self._print_check("  evidence_tier field", c["evidence_tier"])

        # Level 3 components
        print("\nLevel 3 (CASE):")
        self._print_check("  Case Registry entry", c["case_registry"])

        # Level 4 components
        print("\nLevel 4 (THEORY):")
        self._print_check("  Theory Catalog entry", c["theory_catalog"])
        self._print_check("  Parameter Registry entries", c["parameter_registry"])

        # Level 5 components
        print("\nLevel 5 (FULL):")
        self._print_check("  Appendix reference", c["appendix_reference"])
        self._print_check("  Appendix dedicated section", c["appendix_dedicated_section"])
        self._print_check("  Chapter references", c["chapter_reference"])

        # Content components
        print("\nContent Level:")
        self._print_check("  Paper template exists", c["paper_template"])
        self._print_check("  Formal model section", c["template_has_formal_model"])
        self._print_check("  Empirical evidence section", c["template_has_empirical"])
        self._print_check("  Policy implications section", c["template_has_policy"])
        self._print_check("  Full text available", c["fulltext_available"])

        # Details
        if result["details"]:
            print(f"\n{'─'*70}")
            print("DETAILS:")
            for key, value in result["details"].items():
                print(f"  {key}: {value}")

        # Recommendations
        print(f"\n{'─'*70}")
        print("NEXT STEPS TO UPGRADE:")
        self._print_recommendations(result)

    def _print_check(self, label: str, status: bool):
        """Print a checkbox item."""
        mark = "[x]" if status else "[ ]"
        print(f"  {mark} {label}")

    def _print_recommendations(self, result: Dict):
        """Print upgrade recommendations."""
        c = result["components"]
        il = result["integration_level"]

        recommendations = []

        if not c["bibtex_entry"]:
            recommendations.append("1. Add BibTeX entry to bcm_master.bib")

        if c["bibtex_entry"] and not c["theory_support"]:
            recommendations.append("2. Add theory_support field to BibTeX (e.g., theory_support = {MS-XX-001})")

        if c["bibtex_entry"] and not c["parameter"]:
            recommendations.append("3. Add parameter field to BibTeX with key parameters")

        if not c["theory_catalog"] and c["theory_support"]:
            recommendations.append("4. Add entry to theory-catalog.yaml under appropriate category")

        if not c["parameter_registry"] and c["parameter"]:
            recommendations.append("5. Add parameters to parameter-registry.yaml (PAR-BEH-XXX)")

        if not c["case_registry"]:
            recommendations.append("6. Consider adding case to case-registry.yaml")

        if c["paper_template"] and not c["template_has_formal_model"]:
            recommendations.append("7. Add FORMAL MODEL SPECIFICATION section to template")

        if c["paper_template"] and not c["template_has_empirical"]:
            recommendations.append("8. Add EMPIRICAL EVIDENCE CITED section to template")

        if c["paper_template"] and not c["fulltext_available"]:
            recommendations.append("9. Add full paper text to papers/fulltext/ for Content Level 3")

        # Level 5 recommendations
        if il == 4 and not c["appendix_reference"]:
            recommendations.append("10. Add paper to LIT-appendix (e.g., appendices/FEH_fehr_papers.tex)")

        if il == 4 and c["appendix_reference"] and not c["appendix_dedicated_section"]:
            recommendations.append("11. Add dedicated section in appendix (\\subsection{Author (Year)})")

        if il == 4 and not c["chapter_reference"]:
            recommendations.append("12. Add \\cite{} references in relevant chapters")

        if not recommendations:
            print("  ✓ Paper is fully integrated at current level!")
            if il < 5:
                print(f"  → To reach Level {il+1}, consider adding more cross-references")
        else:
            for rec in recommendations:
                print(f"  → {rec}")

    def batch_check(self) -> List[Dict]:
        """Check all papers in the templates directory."""
        results = []

        if not self.papers_path.exists():
            print(f"Error: Papers directory not found: {self.papers_path}")
            return results

        for template_file in sorted(self.papers_path.glob("PAP-*.txt")):
            paper_key = template_file.stem
            result = self.check_paper(paper_key)
            results.append(result)

        return results

    def print_summary_report(self, results: List[Dict]):
        """Print summary report of all papers."""
        print(f"\n{'='*70}")
        print("PAPER INTEGRATION SUMMARY REPORT")
        print(f"{'='*70}")
        print(f"\nTotal papers checked: {len(results)}")

        # Count by level
        content_counts = {0: 0, 1: 0, 2: 0, 3: 0}
        integration_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

        for r in results:
            content_counts[r["content_level"]] = content_counts.get(r["content_level"], 0) + 1
            integration_counts[r["integration_level"]] = integration_counts.get(r["integration_level"], 0) + 1

        print("\nContent Level Distribution:")
        print(f"  Level 0 (BibTeX only):      {content_counts[0]:4d}")
        print(f"  Level 1 (Basic template):   {content_counts[1]:4d}")
        print(f"  Level 2 (Full template):    {content_counts[2]:4d}")
        print(f"  Level 3 (Full text):        {content_counts[3]:4d}")

        print("\nIntegration Level Distribution:")
        print(f"  Level 1 (MINIMAL):  {integration_counts[1]:4d}")
        print(f"  Level 2 (STANDARD): {integration_counts[2]:4d}")
        print(f"  Level 3 (CASE):     {integration_counts[3]:4d}")
        print(f"  Level 4 (THEORY):   {integration_counts[4]:4d}")
        print(f"  Level 5 (FULL):     {integration_counts[5]:4d}")

        # Papers ready for upgrade
        upgrade_candidates = [r for r in results
                           if r["content_level"] >= 2 and r["integration_level"] < 4]

        if upgrade_candidates:
            print(f"\n{'─'*70}")
            print(f"UPGRADE CANDIDATES (Content=2, Integration<4): {len(upgrade_candidates)}")
            for r in upgrade_candidates[:10]:  # Show first 10
                print(f"  → {r['paper_key']} (currently {r['content_level']}+, Integration={r['integration_level']})")
            if len(upgrade_candidates) > 10:
                print(f"  ... and {len(upgrade_candidates)-10} more")


def main():
    parser = argparse.ArgumentParser(
        description="Check and upgrade paper integration levels",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("--check", "-c", metavar="PAPER_KEY",
                       help="Check integration status of a specific paper")
    parser.add_argument("--batch-check", "-b", action="store_true",
                       help="Check all papers in templates directory")
    parser.add_argument("--report", "-r", action="store_true",
                       help="Generate summary report")
    parser.add_argument("--path", default=".",
                       help="Base path to repository (default: current directory)")

    args = parser.parse_args()

    checker = PaperIntegrationChecker(args.path)

    if args.check:
        result = checker.check_paper(args.check)
        checker.print_status(result)
    elif args.batch_check or args.report:
        results = checker.batch_check()
        checker.print_summary_report(results)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
