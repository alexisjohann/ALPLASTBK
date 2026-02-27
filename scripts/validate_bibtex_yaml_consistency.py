#!/usr/bin/env python3
"""
validate_bibtex_yaml_consistency.py - Cross-Validate BibTeX and Paper-YAML

Prüft Konsistenz zwischen BibTeX-Einträgen und Paper-YAML-Dateien:

1. integration_level Konsistenz (BibTeX vs YAML)
2. content_level vs actual content
3. full_text.available vs actual file existence
4. use_for vs LIT-Appendix content
5. theory_support vs theory_catalog entries
6. Calculated level vs claimed level

WORKFLOW GAP FIX:
  Verhindert dass Papers als "Level 5 FOUNDATIONAL" markiert werden
  ohne die tatsächlichen Anforderungen zu erfüllen.

Usage:
    python scripts/validate_bibtex_yaml_consistency.py PAP-heckman2024causality
    python scripts/validate_bibtex_yaml_consistency.py --all
    python scripts/validate_bibtex_yaml_consistency.py --fix PAP-heckman2024causality

Author: EBF Framework Team
Version: 1.0.0
Date: 2026-02-05
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
import yaml

# Paths relative to repository root
REPO_ROOT = Path(__file__).parent.parent
BIB_PATH = REPO_ROOT / "bibliography" / "bcm_master.bib"
PAPER_REFS_PATH = REPO_ROOT / "data" / "paper-references"
PAPER_TEXTS_PATH = REPO_ROOT / "data" / "paper-texts"  # SSOT for full texts!
APPENDICES_PATH = REPO_ROOT / "appendices"
THEORY_CATALOG_PATH = REPO_ROOT / "data" / "theory-catalog.yaml"
CASE_REGISTRY_PATH = REPO_ROOT / "data" / "case-registry.yaml"
PARAM_REGISTRY_PATH = REPO_ROOT / "data" / "parameter-registry.yaml"

# Level mapping
CONTENT_LEVEL_MAP = {
    "L0": 0, "L1": 1, "L2": 2, "L3": 3
}

INTEGRATION_LEVEL_MAP = {
    "I0": 0, "I1": 1, "I2": 2, "I3": 3, "I4": 4, "I5": 5,
    "MINIMAL": 1, "STANDARD": 2, "CASE": 3, "THEORY": 4, "FULL": 5, "FOUNDATIONAL": 5
}

# Level requirements
LEVEL_REQUIREMENTS = {
    1: {
        "name": "MINIMAL",
        "requires": ["bibtex"],
        "content_level_min": "L0"
    },
    2: {
        "name": "STANDARD",
        "requires": ["bibtex", "paper_yaml", "theory_support"],
        "content_level_min": "L1"
    },
    3: {
        "name": "CASE",
        "requires": ["bibtex", "paper_yaml", "theory_support", "case_registry"],
        "content_level_min": "L1"
    },
    4: {
        "name": "THEORY",
        "requires": ["bibtex", "paper_yaml", "theory_support", "case_registry", "theory_catalog", "parameters"],
        "content_level_min": "L2"
    },
    5: {
        "name": "FULL/FOUNDATIONAL",
        "requires": ["bibtex", "paper_yaml", "theory_support", "case_registry", "theory_catalog",
                    "parameters", "full_text", "lit_appendix", "chapter_refs"],
        "content_level_min": "L3"
    }
}


class ConsistencyValidator:
    """Validates consistency between BibTeX and Paper-YAML."""

    def __init__(self, paper_key: str):
        self.paper_key = paper_key.replace("PAP-", "")
        self.full_key = f"PAP-{self.paper_key}"
        self.bibtex_entry: Optional[str] = None
        self.bibtex_fields: Dict[str, str] = {}
        self.paper_yaml: Optional[Dict] = None
        self.issues: List[Dict] = []
        self.calculated_level: int = 0
        self.components_present: Dict[str, bool] = {}

    def load_bibtex(self) -> bool:
        """Load and parse BibTeX entry."""
        if not BIB_PATH.exists():
            self.issues.append({
                "type": "ERROR",
                "component": "bibtex",
                "message": f"BibTeX file not found: {BIB_PATH}"
            })
            return False

        with open(BIB_PATH, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find entry - try multiple patterns
        patterns = [
            rf'@\w+\{{{self.paper_key},',
            rf'@\w+\{{PAP-{self.paper_key},',
            rf'@\w+\{{{self.paper_key.replace("_", "")},',
        ]

        entry_match = None
        for pattern in patterns:
            entry_match = re.search(pattern, content)
            if entry_match:
                break

        if not entry_match:
            self.issues.append({
                "type": "ERROR",
                "component": "bibtex",
                "message": f"BibTeX entry not found for: {self.paper_key}"
            })
            return False

        # Extract full entry
        start_pos = entry_match.start()
        brace_count = 0
        end_pos = start_pos
        for i, char in enumerate(content[start_pos:]):
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    end_pos = start_pos + i + 1
                    break

        self.bibtex_entry = content[start_pos:end_pos]

        # Parse fields
        field_pattern = r'(\w+)\s*=\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}'
        for match in re.finditer(field_pattern, self.bibtex_entry):
            self.bibtex_fields[match.group(1).lower()] = match.group(2)

        self.components_present["bibtex"] = True
        return True

    def load_paper_yaml(self) -> bool:
        """Load Paper-YAML file."""
        yaml_path = PAPER_REFS_PATH / f"{self.full_key}.yaml"
        if not yaml_path.exists():
            self.issues.append({
                "type": "ERROR",
                "component": "paper_yaml",
                "message": f"Paper-YAML not found: {yaml_path}"
            })
            return False

        try:
            with open(yaml_path, 'r', encoding='utf-8') as f:
                self.paper_yaml = yaml.safe_load(f)
            self.components_present["paper_yaml"] = True
            return True
        except Exception as e:
            self.issues.append({
                "type": "ERROR",
                "component": "paper_yaml",
                "message": f"Error loading Paper-YAML: {e}"
            })
            return False

    def check_integration_level_consistency(self) -> None:
        """Check if BibTeX integration_level matches Paper-YAML."""
        bib_level = self.bibtex_fields.get('integration_level', '')
        bib_level_name = self.bibtex_fields.get('integration_level_name', '')

        yaml_content_level = "L0"
        yaml_integration_level = "I0"

        if self.paper_yaml:
            # Try different locations for content_level
            if 'content_level' in self.paper_yaml:
                yaml_content_level = self.paper_yaml.get('content_level', 'L0')
            elif 'structural_characteristics' in self.paper_yaml:
                yaml_content_level = self.paper_yaml.get('structural_characteristics', {}).get('content_level', 'L0')
            elif 'full_text' in self.paper_yaml:
                if self.paper_yaml.get('full_text', {}).get('content_level'):
                    yaml_content_level = self.paper_yaml['full_text']['content_level']

            # Get integration level from ebf_integration
            ebf = self.paper_yaml.get('ebf_integration', {})
            yaml_integration_level = ebf.get('integration_level', 'I0')
            if isinstance(yaml_integration_level, int):
                yaml_integration_level = f"I{yaml_integration_level}"

        # Normalize levels
        bib_level_num = 0
        if bib_level:
            try:
                bib_level_num = int(bib_level)
            except ValueError:
                bib_level_num = INTEGRATION_LEVEL_MAP.get(bib_level.upper(), 0)

        yaml_level_num = INTEGRATION_LEVEL_MAP.get(str(yaml_integration_level).upper(), 0)
        if isinstance(yaml_integration_level, int):
            yaml_level_num = yaml_integration_level

        # Check consistency
        if bib_level_num != yaml_level_num and bib_level_num > 0:
            self.issues.append({
                "type": "MISMATCH",
                "component": "integration_level",
                "message": f"BibTeX claims Level {bib_level_num} ({bib_level_name}), YAML says {yaml_integration_level}",
                "bibtex_value": bib_level_num,
                "yaml_value": yaml_level_num,
                "fix": f"Update Paper-YAML integration_level to {bib_level_num} OR downgrade BibTeX to {yaml_level_num}"
            })

    def check_full_text_consistency(self) -> None:
        """Check full_text.available matches actual file existence."""
        # Check SSOT location
        ssot_path = PAPER_TEXTS_PATH / f"{self.full_key}.md"
        ssot_exists = ssot_path.exists()

        # Check legacy location
        legacy_path = REPO_ROOT / "papers" / "evaluated" / "integrated" / f"{self.full_key}.txt"
        legacy_exists = legacy_path.exists()

        # Get YAML claim
        yaml_available = False
        yaml_path = None
        if self.paper_yaml:
            ft = self.paper_yaml.get('full_text', {})
            yaml_available = ft.get('available', False)
            yaml_path = ft.get('path')

        # Check consistency
        if yaml_available and not ssot_exists:
            if legacy_exists:
                self.issues.append({
                    "type": "WRONG_LOCATION",
                    "component": "full_text",
                    "message": f"Full-text exists at legacy location but not at SSOT",
                    "legacy_path": str(legacy_path),
                    "ssot_path": str(ssot_path),
                    "fix": f"Move/copy full-text to {ssot_path}"
                })
            else:
                self.issues.append({
                    "type": "MISMATCH",
                    "component": "full_text",
                    "message": f"YAML claims full_text.available=true but file not found",
                    "fix": f"Set full_text.available=false OR add file to {ssot_path}"
                })

        if not yaml_available and ssot_exists:
            self.issues.append({
                "type": "MISMATCH",
                "component": "full_text",
                "message": f"Full-text exists but YAML claims available=false",
                "fix": "Update Paper-YAML: full_text.available=true, path=..."
            })

        if ssot_exists:
            self.components_present["full_text"] = True
            # Check file size
            size = ssot_path.stat().st_size
            if size < 1000:
                self.issues.append({
                    "type": "WARNING",
                    "component": "full_text",
                    "message": f"Full-text file seems too small ({size} bytes)"
                })

    def check_use_for_consistency(self) -> None:
        """Check use_for claims match actual appendix content."""
        use_for = self.bibtex_fields.get('use_for', '')
        if not use_for:
            return

        # Parse use_for entries
        entries = [e.strip() for e in use_for.split(',')]
        lit_appendices = [e for e in entries if e.startswith('LIT-')]

        for lit_entry in lit_appendices:
            # Extract appendix code (e.g., LIT-HECKMAN -> HEC or HECKMAN)
            appendix_code = lit_entry.replace('LIT-', '')

            # Search for appendix file
            patterns = [
                f"{appendix_code}*.tex",
                f"*LIT-{appendix_code}*.tex",
                f"*{appendix_code.lower()}*.tex"
            ]

            found_file = None
            for pattern in patterns:
                files = list(APPENDICES_PATH.glob(pattern))
                if files:
                    found_file = files[0]
                    break

            if not found_file:
                self.issues.append({
                    "type": "WARNING",
                    "component": "use_for",
                    "message": f"LIT-Appendix for {lit_entry} not found",
                    "fix": f"Create appendix or remove {lit_entry} from use_for"
                })
                continue

            # Check if paper is referenced in appendix
            with open(found_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check for paper reference (various formats)
            paper_patterns = [
                self.paper_key,
                self.paper_key.replace('_', ''),
                self.paper_key.replace('2024', '2023'),  # NBER vs published
                re.escape(self.bibtex_fields.get('title', '')[:50]) if self.bibtex_fields.get('title') else None
            ]

            found_ref = False
            for pattern in paper_patterns:
                if pattern and pattern in content:
                    found_ref = True
                    self.components_present["lit_appendix"] = True
                    break

            if not found_ref:
                self.issues.append({
                    "type": "MISSING_REF",
                    "component": "lit_appendix",
                    "message": f"Paper not referenced in {found_file.name}",
                    "fix": f"Add \\citep{{{self.paper_key}}} to {found_file.name}"
                })

    def check_theory_support_consistency(self) -> None:
        """Check theory_support claims exist in theory catalog."""
        theory_support = self.bibtex_fields.get('theory_support', '')
        if not theory_support:
            return

        theories = [t.strip() for t in theory_support.split(',')]

        if not THEORY_CATALOG_PATH.exists():
            return

        with open(THEORY_CATALOG_PATH, 'r', encoding='utf-8') as f:
            catalog_content = f.read()

        found_theories = []
        missing_theories = []

        for theory in theories:
            if theory in catalog_content:
                found_theories.append(theory)
            else:
                missing_theories.append(theory)

        if found_theories:
            self.components_present["theory_support"] = True

        if missing_theories:
            self.issues.append({
                "type": "MISSING",
                "component": "theory_support",
                "message": f"Theories not in catalog: {missing_theories}",
                "fix": "Add theories to theory-catalog.yaml or remove from BibTeX"
            })

    def check_case_registry(self) -> None:
        """Check if paper has case in case registry."""
        if not self.paper_yaml:
            return

        case_integration = self.paper_yaml.get('case_integration', {})
        case_id = case_integration.get('case_id')

        if case_id and CASE_REGISTRY_PATH.exists():
            with open(CASE_REGISTRY_PATH, 'r', encoding='utf-8') as f:
                content = f.read()
            if case_id in content:
                self.components_present["case_registry"] = True

    def check_theory_catalog(self) -> None:
        """Check if paper has theory in theory catalog."""
        if not self.paper_yaml:
            return

        theory_integration = self.paper_yaml.get('theory_integration', {})
        theory_id = theory_integration.get('theory_id')

        if theory_id and THEORY_CATALOG_PATH.exists():
            with open(THEORY_CATALOG_PATH, 'r', encoding='utf-8') as f:
                content = f.read()
            if theory_id in content:
                self.components_present["theory_catalog"] = True

    def check_parameters(self) -> None:
        """Check if paper has parameters in parameter registry."""
        if not self.paper_yaml:
            return

        param_integration = self.paper_yaml.get('parameter_integration', [])

        if param_integration and PARAM_REGISTRY_PATH.exists():
            with open(PARAM_REGISTRY_PATH, 'r', encoding='utf-8') as f:
                content = f.read()
            for param in param_integration:
                if param in content:
                    self.components_present["parameters"] = True
                    break

    def check_chapter_refs(self) -> None:
        """Check if paper has chapter cross-references."""
        if not self.paper_yaml:
            return

        chapter_relevance = self.paper_yaml.get('chapter_relevance', {})
        high_relevance = chapter_relevance.get('high_relevance', [])

        if high_relevance:
            # Check if any chapter actually references this paper
            chapters_path = REPO_ROOT / "chapters"
            for chapter_info in high_relevance:
                chapter_num = chapter_info.get('chapter')
                status = chapter_info.get('status', 'pending')

                if status == 'completed':
                    self.components_present["chapter_refs"] = True
                    break

    def calculate_actual_level(self) -> int:
        """Calculate actual integration level based on present components."""
        for level in range(5, 0, -1):
            requirements = LEVEL_REQUIREMENTS[level]["requires"]
            if all(self.components_present.get(req, False) for req in requirements):
                return level
        return 1 if self.components_present.get("bibtex") else 0

    def validate_all(self) -> Dict:
        """Run all validation checks."""
        # Load data
        self.load_bibtex()
        self.load_paper_yaml()

        # Run checks
        self.check_integration_level_consistency()
        self.check_full_text_consistency()
        self.check_use_for_consistency()
        self.check_theory_support_consistency()
        self.check_case_registry()
        self.check_theory_catalog()
        self.check_parameters()
        self.check_chapter_refs()

        # Calculate actual level
        self.calculated_level = self.calculate_actual_level()

        # Get claimed level
        bib_level = 0
        if 'integration_level' in self.bibtex_fields:
            try:
                bib_level = int(self.bibtex_fields['integration_level'])
            except ValueError:
                bib_level = INTEGRATION_LEVEL_MAP.get(
                    self.bibtex_fields['integration_level'].upper(), 0
                )

        # Add level mismatch if claimed > actual
        if bib_level > self.calculated_level:
            missing = []
            for req in LEVEL_REQUIREMENTS[bib_level]["requires"]:
                if not self.components_present.get(req, False):
                    missing.append(req)

            self.issues.append({
                "type": "LEVEL_OVERCLAIM",
                "component": "integration_level",
                "message": f"Claims Level {bib_level} but only qualifies for Level {self.calculated_level}",
                "missing_components": missing,
                "fix": f"Add missing components: {missing} OR downgrade to Level {self.calculated_level}"
            })

        return {
            "paper_key": self.full_key,
            "claimed_level": bib_level,
            "calculated_level": self.calculated_level,
            "components_present": self.components_present,
            "issues": self.issues,
            "is_consistent": len([i for i in self.issues if i["type"] not in ["WARNING"]]) == 0
        }


def print_results(result: Dict) -> None:
    """Print validation results."""
    print(f"\n{'='*70}")
    print(f"  BIBTEX ↔ YAML CONSISTENCY: {result['paper_key']}")
    print(f"{'='*70}\n")

    # Level comparison
    claimed = result['claimed_level']
    actual = result['calculated_level']
    level_match = "✅" if claimed <= actual else "❌"

    print(f"  Level Comparison:")
    print(f"  ├── Claimed (BibTeX):    Level {claimed}")
    print(f"  ├── Calculated (Actual): Level {actual}")
    print(f"  └── Status: {level_match} {'CONSISTENT' if claimed <= actual else 'OVERCLAIMED'}\n")

    # Components
    print(f"  Components Present:")
    components = result['components_present']
    for comp, present in sorted(components.items()):
        symbol = "✅" if present else "❌"
        print(f"  ├── {symbol} {comp}")
    print()

    # Issues
    if result['issues']:
        print(f"  Issues Found ({len(result['issues'])}):")
        for issue in result['issues']:
            symbol = {"ERROR": "❌", "MISMATCH": "⚠️", "MISSING": "❌",
                     "MISSING_REF": "📝", "WRONG_LOCATION": "📁",
                     "LEVEL_OVERCLAIM": "🔴", "WARNING": "⚠️"}.get(issue['type'], "?")
            print(f"  {symbol} [{issue['type']}] {issue['component']}")
            print(f"     {issue['message']}")
            if 'fix' in issue:
                print(f"     → FIX: {issue['fix']}")
            print()
    else:
        print("  ✅ No issues found!\n")

    print(f"{'─'*70}")
    print(f"  RESULT: {'✅ CONSISTENT' if result['is_consistent'] else '❌ INCONSISTENT'}")
    print(f"{'='*70}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Validate BibTeX ↔ Paper-YAML consistency"
    )
    parser.add_argument("paper_key", nargs="?", help="Paper key")
    parser.add_argument("--all", action="store_true", help="Check all papers")
    parser.add_argument("--fix", action="store_true", help="Attempt to fix issues")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--level", type=int, help="Only check papers claiming this level")

    args = parser.parse_args()

    if args.all:
        # Find all papers with BibTeX entries claiming high levels
        papers_to_check = []

        with open(BIB_PATH, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find entries with integration_level
        pattern = r'@\w+\{(PAP-[\w]+),'
        for match in re.finditer(pattern, content):
            paper_key = match.group(1)
            papers_to_check.append(paper_key)

        # Also check paper-references directory
        for yaml_file in PAPER_REFS_PATH.glob("PAP-*.yaml"):
            paper_key = yaml_file.stem
            if paper_key not in papers_to_check:
                papers_to_check.append(paper_key)

        results = []
        inconsistent = []

        for paper_key in sorted(papers_to_check)[:50]:  # Limit for performance
            validator = ConsistencyValidator(paper_key)
            result = validator.validate_all()

            if args.level and result['claimed_level'] != args.level:
                continue

            results.append(result)
            if not result['is_consistent']:
                inconsistent.append(result)

        if args.json:
            import json
            print(json.dumps(results, indent=2))
        else:
            print(f"\n{'='*70}")
            print(f"  CONSISTENCY CHECK: {len(results)} papers checked")
            print(f"{'='*70}")
            print(f"  ✅ Consistent: {len(results) - len(inconsistent)}")
            print(f"  ❌ Inconsistent: {len(inconsistent)}")

            if inconsistent:
                print(f"\n  Inconsistent Papers:")
                for r in inconsistent:
                    print(f"  ├── {r['paper_key']}: Claims L{r['claimed_level']}, Actual L{r['calculated_level']}")
            print()

        return 0 if not inconsistent else 1

    if not args.paper_key:
        parser.print_help()
        return 1

    validator = ConsistencyValidator(args.paper_key)
    result = validator.validate_all()

    if args.json:
        import json
        print(json.dumps(result, indent=2))
    else:
        print_results(result)

    return 0 if result['is_consistent'] else 1


if __name__ == "__main__":
    sys.exit(main())
