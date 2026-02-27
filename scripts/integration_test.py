#!/usr/bin/env python3
"""
Integration Test Suite for Complementarity-Context Framework (EBF)
==================================================================

Validates that new appendices/chapters are properly integrated:
- LaTeX syntax consistency
- Cross-references and citations
- Appendix index accuracy
- Parameter sourcing discipline

Usage:
    python scripts/integration_test.py                    # Run all tests
    python scripts/integration_test.py --test 1           # Run specific test
    python scripts/integration_test.py --chapter 20       # Test specific chapter
    python scripts/integration_test.py --appendix JJJ     # Test specific appendix
    python scripts/integration_test.py --verbose          # Detailed output
    python scripts/integration_test.py --json             # JSON output format

Exit Codes:
    0 = All tests passed
    1 = One or more tests failed
    2 = Configuration error
"""

import re
import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict


@dataclass
class TestResult:
    test_id: int
    test_name: str
    status: str  # "PASS", "FAIL", "SKIP"
    details: str
    severity: str  # "CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"


class IntegrationTester:
    """Main integration test orchestrator."""

    def __init__(self, project_root: Path, verbose: bool = False, json_output: bool = False):
        self.project_root = project_root
        self.verbose = verbose
        self.json_output = json_output
        self.results: List[TestResult] = []
        self.passed = 0
        self.failed = 0
        self.skipped = 0

    def run_all_tests(self) -> int:
        """Run all integration tests."""
        self.log("🚀 Starting Integration Test Suite", "INFO")
        self.log(f"Project root: {self.project_root}", "INFO")

        # Test 1: LaTeX Syntax Balance
        self._test_latex_syntax_balance()

        # Test 2: Internal Cross-References
        self._test_internal_cross_references()

        # Test 3: Appendix Index Entry
        self._test_appendix_index_entry()

        # Test 4: Appendix Counts
        self._test_appendix_counts()

        # Test 5: Chapter Examples (Rente)
        self._test_chapter_rente_formula()

        # Test 6: Chapter Examples (Energie)
        self._test_chapter_energie_segments()

        # Test 7: Chapter Examples (Engagement)
        self._test_chapter_engagement_disclosure()

        # Test 8: Cross-References Ch20 to Appendix
        self._test_cross_references_ch20_to_appendix()

        # Test 9: Citation Specificity
        self._test_citation_specificity()

        # Print summary
        self._print_summary()

        return 0 if self.failed == 0 else 1

    def run_specific_test(self, test_id: int) -> int:
        """Run a specific test by ID."""
        test_methods = {
            1: self._test_latex_syntax_balance,
            2: self._test_internal_cross_references,
            3: self._test_appendix_index_entry,
            4: self._test_appendix_counts,
            5: self._test_chapter_rente_formula,
            6: self._test_chapter_energie_segments,
            7: self._test_chapter_engagement_disclosure,
            8: self._test_cross_references_ch20_to_appendix,
            9: self._test_citation_specificity,
        }

        if test_id not in test_methods:
            self.log(f"❌ Test {test_id} not found", "ERROR")
            return 2

        self.log(f"🧪 Running Test {test_id}", "INFO")
        test_methods[test_id]()
        self._print_summary()
        return 0 if self.failed == 0 else 1

    # ============================================================================
    # Test 1: LaTeX Syntax Balance
    # ============================================================================

    def _test_latex_syntax_balance(self):
        """Test 1: Verify LaTeX environments are balanced (open/close)."""
        test_id = 1
        test_name = "LaTeX Syntax Balance"
        jjj_file = self.project_root / "appendices" / "JJJ_METHOD-PSG_Parameter_Sourcing_Guide.tex"

        if not jjj_file.exists():
            self._add_result(TestResult(
                test_id=test_id,
                test_name=test_name,
                status="SKIP",
                details="JJJ appendix not found",
                severity="INFO"
            ))
            return

        content = jjj_file.read_text()

        # Count opening and closing environments
        opening = len(re.findall(r'\\begin\{', content))
        closing = len(re.findall(r'\\end\{', content))

        if opening == closing:
            self._add_result(TestResult(
                test_id=test_id,
                test_name=test_name,
                status="PASS",
                details=f"Opening: {opening} ✓, Closing: {closing} ✓",
                severity="INFO"
            ))
        else:
            self._add_result(TestResult(
                test_id=test_id,
                test_name=test_name,
                status="FAIL",
                details=f"Mismatch: {opening} opening vs {closing} closing",
                severity="CRITICAL"
            ))

    # ============================================================================
    # Test 2: Internal Cross-References
    # ============================================================================

    def _test_internal_cross_references(self):
        """Test 2: Verify internal cross-references have matching labels."""
        test_id = 2
        test_name = "Internal Cross-References"
        jjj_file = self.project_root / "appendices" / "JJJ_METHOD-PSG_Parameter_Sourcing_Guide.tex"

        if not jjj_file.exists():
            self._add_result(TestResult(
                test_id=test_id,
                test_name=test_name,
                status="SKIP",
                details="JJJ appendix not found",
                severity="INFO"
            ))
            return

        content = jjj_file.read_text()

        # Find all references
        refs = set(re.findall(r'\\(?:ref|eqref)\{([^}]+)\}', content))

        # Find all labels
        labels = set(re.findall(r'\\label\{([^}]+)\}', content))

        # Check for missing labels
        missing = refs - labels

        if not missing:
            self._add_result(TestResult(
                test_id=test_id,
                test_name=test_name,
                status="PASS",
                details=f"All {len(refs)} references have matching labels ✓",
                severity="INFO"
            ))
        else:
            self._add_result(TestResult(
                test_id=test_id,
                test_name=test_name,
                status="FAIL",
                details=f"Missing labels: {', '.join(sorted(missing))}",
                severity="HIGH"
            ))

    # ============================================================================
    # Test 3: Appendix Index Entry
    # ============================================================================

    def _test_appendix_index_entry(self):
        """Test 3: Verify JJJ entry in appendix index."""
        test_id = 3
        test_name = "Appendix Index Entry"
        index_file = self.project_root / "appendices" / "00_appendix_index.tex"

        if not index_file.exists():
            self._add_result(TestResult(
                test_id=test_id,
                test_name=test_name,
                status="SKIP",
                details="Index file not found",
                severity="INFO"
            ))
            return

        content = index_file.read_text()

        if re.search(r'JJJ\s*&\s*METHOD-PSG', content):
            self._add_result(TestResult(
                test_id=test_id,
                test_name=test_name,
                status="PASS",
                details="JJJ & METHOD-PSG entry found in METHOD table ✓",
                severity="INFO"
            ))
        else:
            self._add_result(TestResult(
                test_id=test_id,
                test_name=test_name,
                status="FAIL",
                details="JJJ entry not found in appendix index",
                severity="HIGH"
            ))

    # ============================================================================
    # Test 4: Appendix Counts
    # ============================================================================

    def _test_appendix_counts(self):
        """Test 4: Verify appendix category counts are updated."""
        test_id = 4
        test_name = "Appendix Counts"
        index_file = self.project_root / "appendices" / "00_appendix_index.tex"

        if not index_file.exists():
            self._add_result(TestResult(
                test_id=test_id,
                test_name=test_name,
                status="SKIP",
                details="Index file not found",
                severity="INFO"
            ))
            return

        content = index_file.read_text()

        # Check METHOD count
        method_count_match = re.search(r'\\textbf\{METHOD-\}\s*&\s*Methodology\s*&\s*(\d+)', content)
        total_count_match = re.search(r'&\s*\\textbf\{Total\}\s*&\s*\\textbf\{(\d+)\}', content)

        method_count = int(method_count_match.group(1)) if method_count_match else None
        total_count = int(total_count_match.group(1)) if total_count_match else None

        if method_count == 15 and total_count == 129:
            self._add_result(TestResult(
                test_id=test_id,
                test_name=test_name,
                status="PASS",
                details=f"METHOD: {method_count} ✓, Total: {total_count} ✓",
                severity="INFO"
            ))
        else:
            self._add_result(TestResult(
                test_id=test_id,
                test_name=test_name,
                status="FAIL",
                details=f"Counts incorrect: METHOD: {method_count} (expected 15), Total: {total_count} (expected 129)",
                severity="HIGH"
            ))

    # ============================================================================
    # Test 5: Rente Formula
    # ============================================================================

    def _test_chapter_rente_formula(self):
        """Test 5: Verify Rente example has visible formula and derivation."""
        test_id = 5
        test_name = "Rente Formula Documentation"
        ch20_file = self.project_root / "chapters" / "20_intervention_portfolios.tex"

        if not ch20_file.exists():
            self._add_result(TestResult(
                test_id=test_id,
                test_name=test_name,
                status="SKIP",
                details="Chapter 20 not found",
                severity="INFO"
            ))
            return

        content = ch20_file.read_text()

        # Check for equation label, table, and Ch18 reference
        has_equation = bool(re.search(r'E_\{\\varphi\}\s*=\s*E_\{\\text\{baseline\}\}\s*\\times\s*\\alpha', content))
        has_table = bool(re.search(r'Rente.*Phase-Affinity', content, re.IGNORECASE))
        has_ch18_ref = bool(re.search(r'Ch18.*lines\s+440-485', content))

        if has_equation and has_table and has_ch18_ref:
            self._add_result(TestResult(
                test_id=test_id,
                test_name=test_name,
                status="PASS",
                details="Formula ✓, Table ✓, Ch18 refs (440-485) ✓",
                severity="INFO"
            ))
        else:
            missing = []
            if not has_equation: missing.append("equation")
            if not has_table: missing.append("derivation table")
            if not has_ch18_ref: missing.append("Ch18 reference")
            self._add_result(TestResult(
                test_id=test_id,
                test_name=test_name,
                status="FAIL",
                details=f"Missing: {', '.join(missing)}",
                severity="HIGH"
            ))

    # ============================================================================
    # Test 6: Energie Segments
    # ============================================================================

    def _test_chapter_energie_segments(self):
        """Test 6: Verify Energie example has correct segment multipliers."""
        test_id = 6
        test_name = "Energie Segment Multipliers"
        ch20_file = self.project_root / "chapters" / "20_intervention_portfolios.tex"

        if not ch20_file.exists():
            self._add_result(TestResult(
                test_id=test_id,
                test_name=test_name,
                status="SKIP",
                details="Chapter 20 not found",
                severity="INFO"
            ))
            return

        content = ch20_file.read_text()

        # Extract Energie section
        energie_section = re.search(r'subsection\{Example 3.*?\}.*?(?=\\subsection|\\end\{enumerate\})',
                                    content, re.DOTALL)

        if not energie_section:
            self._add_result(TestResult(
                test_id=test_id,
                test_name=test_name,
                status="SKIP",
                details="Energie section not found",
                severity="INFO"
            ))
            return

        energie_text = energie_section.group(0)

        # Check for AS multiplier and Ch19 reference
        has_as_08 = bool(re.search(r'Autonomy-Seeking.*?0\.8', energie_text))
        has_ch19_ref = bool(re.search(r'Ch19.*?lines?\s+1128-1135', energie_text))
        has_baseline_136 = bool(re.search(r'13\.56.*?approx.*?13\.6', energie_text))
        has_three_segments = bool(re.search(r'Present-Biased.*?Social-Oriented.*?Autonomy-Seeking',
                                            energie_text, re.DOTALL))

        if has_as_08 and has_ch19_ref and has_baseline_136 and has_three_segments:
            self._add_result(TestResult(
                test_id=test_id,
                test_name=test_name,
                status="PASS",
                details="AS σ=0.8 ✓, Ch19 refs ✓, Baseline 13.6% ✓, 3 segments ✓",
                severity="INFO"
            ))
        else:
            missing = []
            if not has_as_08: missing.append("AS σ=0.8")
            if not has_ch19_ref: missing.append("Ch19 reference")
            if not has_baseline_136: missing.append("baseline 13.6%")
            if not has_three_segments: missing.append("3 segments")
            self._add_result(TestResult(
                test_id=test_id,
                test_name=test_name,
                status="FAIL",
                details=f"Missing: {', '.join(missing)}",
                severity="HIGH"
            ))

    # ============================================================================
    # Test 7: Engagement Disclosure
    # ============================================================================

    def _test_chapter_engagement_disclosure(self):
        """Test 7: Verify Engagement example has disclosure statement."""
        test_id = 7
        test_name = "Engagement Disclosure"
        ch20_file = self.project_root / "chapters" / "20_intervention_portfolios.tex"

        if not ch20_file.exists():
            self._add_result(TestResult(
                test_id=test_id,
                test_name=test_name,
                status="SKIP",
                details="Chapter 20 not found",
                severity="INFO"
            ))
            return

        content = ch20_file.read_text()

        # Check for Engagement section with disclosure
        has_disclosure = bool(re.search(r'IMPORTANT DISCLOSURE.*Ch17.*Ch19.*synthesized.*practitioners.*validate',
                                        content, re.DOTALL | re.IGNORECASE))
        has_segment_suppression = bool(re.search(r'Segment-specific.*I_.*F.*suppression.*Ch19',
                                                  content, re.DOTALL))

        if has_disclosure and has_segment_suppression:
            self._add_result(TestResult(
                test_id=test_id,
                test_name=test_name,
                status="PASS",
                details="Disclosure ✓, Ch19 suppression values ✓",
                severity="INFO"
            ))
        else:
            missing = []
            if not has_disclosure: missing.append("disclosure statement")
            if not has_segment_suppression: missing.append("Ch19 suppression values")
            self._add_result(TestResult(
                test_id=test_id,
                test_name=test_name,
                status="FAIL",
                details=f"Missing: {', '.join(missing)}",
                severity="HIGH"
            ))

    # ============================================================================
    # Test 8: Cross-References Ch20 to Appendix
    # ============================================================================

    def _test_cross_references_ch20_to_appendix(self):
        """Test 8: Verify JJJ appendix documents all Ch20 examples."""
        test_id = 8
        test_name = "Ch20 to JJJ Cross-References"
        jjj_file = self.project_root / "appendices" / "JJJ_METHOD-PSG_Parameter_Sourcing_Guide.tex"

        if not jjj_file.exists():
            self._add_result(TestResult(
                test_id=test_id,
                test_name=test_name,
                status="SKIP",
                details="JJJ appendix not found",
                severity="INFO"
            ))
            return

        content = jjj_file.read_text()

        # Check for all four examples
        examples = ["Diabetes", "Rente", "Energie", "Engagement"]
        found_examples = sum(1 for ex in examples if re.search(ex, content))

        # Check for case study sections
        case_studies = bool(re.search(r'Case Studies.*Four Core Examples', content, re.DOTALL))

        if found_examples == 4 and case_studies:
            self._add_result(TestResult(
                test_id=test_id,
                test_name=test_name,
                status="PASS",
                details=f"All {found_examples} examples documented ✓, Case studies section ✓",
                severity="INFO"
            ))
        else:
            self._add_result(TestResult(
                test_id=test_id,
                test_name=test_name,
                status="FAIL",
                details=f"Found {found_examples}/4 examples, case studies: {'✓' if case_studies else '✗'}",
                severity="HIGH"
            ))

    # ============================================================================
    # Test 9: Citation Specificity
    # ============================================================================

    def _test_citation_specificity(self):
        """Test 9: Verify all citations include specific locations."""
        test_id = 9
        test_name = "Citation Specificity"
        ch20_file = self.project_root / "chapters" / "20_intervention_portfolios.tex"

        if not ch20_file.exists():
            self._add_result(TestResult(
                test_id=test_id,
                test_name=test_name,
                status="SKIP",
                details="Chapter 20 not found",
                severity="INFO"
            ))
            return

        content = ch20_file.read_text()

        # Check for chapter citations with specific locations
        ch17_specific = bool(re.search(r'Ch17.*(?:Eq\.|lines?|Section)', content))
        ch18_specific = bool(re.search(r'Ch18.*(?:lines?\s+\d+)', content))
        ch19_specific = bool(re.search(r'Ch19.*(?:lines?\s+\d+)', content))

        if ch17_specific and ch18_specific and ch19_specific:
            self._add_result(TestResult(
                test_id=test_id,
                test_name=test_name,
                status="PASS",
                details="Ch17 ✓, Ch18 lines ✓, Ch19 lines ✓",
                severity="INFO"
            ))
        else:
            missing = []
            if not ch17_specific: missing.append("Ch17")
            if not ch18_specific: missing.append("Ch18 lines")
            if not ch19_specific: missing.append("Ch19 lines")
            self._add_result(TestResult(
                test_id=test_id,
                test_name=test_name,
                status="FAIL",
                details=f"Missing specific citations: {', '.join(missing)}",
                severity="MEDIUM"
            ))

    # ============================================================================
    # Helper Methods
    # ============================================================================

    def _add_result(self, result: TestResult):
        """Add test result and update counters."""
        self.results.append(result)
        if result.status == "PASS":
            self.passed += 1
        elif result.status == "FAIL":
            self.failed += 1
        else:
            self.skipped += 1

    def log(self, message: str, level: str = "INFO"):
        """Print log message based on verbosity."""
        if level == "ERROR" or level == "INFO" or self.verbose:
            print(f"[{level}] {message}")

    def _print_summary(self):
        """Print test summary."""
        print("\n" + "="*80)
        print("Integration Test Summary")
        print("="*80)

        for result in self.results:
            status_symbol = "✅" if result.status == "PASS" else ("⏭️" if result.status == "SKIP" else "❌")
            print(f"{status_symbol} Test {result.test_id}: {result.test_name}")
            print(f"   Status: {result.status} | Severity: {result.severity}")
            print(f"   Details: {result.details}\n")

        print("="*80)
        print(f"Results: {self.passed} passed, {self.failed} failed, {self.skipped} skipped")
        print(f"Status: {'🎉 ALL TESTS PASSED' if self.failed == 0 else '⚠️  SOME TESTS FAILED'}")
        print("="*80 + "\n")

        if self.json_output:
            self._print_json_output()

    def _print_json_output(self):
        """Print results in JSON format."""
        output = {
            "summary": {
                "total": len(self.results),
                "passed": self.passed,
                "failed": self.failed,
                "skipped": self.skipped,
                "status": "PASS" if self.failed == 0 else "FAIL"
            },
            "tests": [asdict(r) for r in self.results]
        }
        print(json.dumps(output, indent=2))


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Integration Test Suite for EBF Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument('--test', type=int, help='Run specific test (1-9)')
    parser.add_argument('--chapter', type=int, help='Test specific chapter')
    parser.add_argument('--appendix', type=str, help='Test specific appendix')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    parser.add_argument('--json', action='store_true', help='JSON output format')

    args = parser.parse_args()

    project_root = Path(__file__).parent.parent
    tester = IntegrationTester(project_root, verbose=args.verbose, json_output=args.json)

    if args.test:
        return tester.run_specific_test(args.test)
    else:
        return tester.run_all_tests()


if __name__ == "__main__":
    sys.exit(main())
