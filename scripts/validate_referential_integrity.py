#!/usr/bin/env python3
"""
=============================================================================
REFERENTIAL INTEGRITY VALIDATOR
=============================================================================
Validates foreign key relationships across EBF YAML databases.

Checks:
1. model-registry → model-building-session (session_id exists)
2. model-registry → theory-catalog (theory_id exists)
3. model-registry → bcm_master.bib (bib_key exists)
4. case-registry → appendices (appendix exists)
5. case-registry → chapters (chapter exists)
6. intervention-registry → model-registry (model_id exists)
7. intervention-registry → case-registry (case_id exists)
8. theory-catalog → bcm_master.bib (bib_key exists)
9. concept-registry → bcm_master.bib (paper references exist)

Usage:
    python scripts/validate_referential_integrity.py
    python scripts/validate_referential_integrity.py --fix  # Auto-fix where possible
    python scripts/validate_referential_integrity.py --verbose

Version: 1.0
Date: January 2026
=============================================================================
"""

import os
import sys
import re
import yaml
import glob
import argparse
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass, field

# =============================================================================
# DATA STRUCTURES
# =============================================================================

@dataclass
class ValidationError:
    """Single validation error"""
    source_file: str
    source_id: str
    target_file: str
    target_id: str
    error_type: str
    severity: str  # 'critical', 'warning', 'info'
    message: str
    auto_fixable: bool = False


@dataclass
class ValidationResult:
    """Complete validation result"""
    errors: List[ValidationError] = field(default_factory=list)
    warnings: List[ValidationError] = field(default_factory=list)
    info: List[ValidationError] = field(default_factory=list)
    checks_passed: int = 0
    checks_failed: int = 0

    @property
    def score(self) -> float:
        total = self.checks_passed + self.checks_failed
        if total == 0:
            return 100.0
        return (self.checks_passed / total) * 100


# =============================================================================
# FILE LOADERS
# =============================================================================

def load_yaml(path: str) -> Optional[dict]:
    """Load YAML file safely with detailed error reporting"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as e:
        # Provide more context for YAML parsing errors
        if hasattr(e, 'problem_mark'):
            mark = e.problem_mark
            print(f"Warning: YAML parsing error in {path} at line {mark.line + 1}, column {mark.column + 1}")
            print(f"  Problem: {e.problem}")
            if hasattr(e, 'context') and e.context:
                print(f"  Context: {e.context}")
        else:
            print(f"Warning: Could not load {path}: {e}")
        return None
    except FileNotFoundError:
        print(f"Warning: File not found: {path}")
        return None
    except Exception as e:
        print(f"Warning: Could not load {path}: {type(e).__name__}: {e}")
        return None


def load_bibtex_keys(bib_path: str) -> Set[str]:
    """Extract all BibTeX keys from .bib file"""
    keys = set()
    try:
        with open(bib_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # Match @type{key,
        pattern = r'@\w+\{([^,]+),'
        keys = set(re.findall(pattern, content))
    except Exception as e:
        print(f"Warning: Could not load {bib_path}: {e}")
    return keys


def get_existing_appendices(appendix_dir: str) -> Set[str]:
    """Get all appendix codes from filenames"""
    codes = set()
    for f in glob.glob(os.path.join(appendix_dir, '*.tex')):
        basename = os.path.basename(f)
        # Extract code from filename patterns like "AAA_*.tex", "B_*.tex"
        match = re.match(r'^([A-Z]+)[-_]', basename)
        if match:
            codes.add(match.group(1))
        # Also match single letter codes like "V_context.tex"
        match = re.match(r'^([A-Z])_', basename)
        if match:
            codes.add(match.group(1))
    return codes


def get_existing_chapters(chapter_dir: str) -> Set[int]:
    """Get all chapter numbers from filenames"""
    chapters = set()
    for f in glob.glob(os.path.join(chapter_dir, '*.tex')):
        basename = os.path.basename(f)
        # Match chapter number at start: "03_utility.tex"
        match = re.match(r'^(\d+)_', basename)
        if match:
            chapters.add(int(match.group(1)))
    return chapters


# =============================================================================
# VALIDATORS
# =============================================================================

class ReferentialIntegrityValidator:
    def __init__(self, base_path: str, verbose: bool = False):
        self.base_path = Path(base_path)
        self.verbose = verbose
        self.result = ValidationResult()

        # Load all data sources
        self._load_data_sources()

    def _load_data_sources(self):
        """Load all YAML databases and reference data"""
        data_path = self.base_path / 'data'

        # Core registries
        self.model_registry = load_yaml(data_path / 'model-registry.yaml') or {}
        self.theory_catalog = load_yaml(data_path / 'theory-catalog.yaml') or {}
        self.case_registry = load_yaml(data_path / 'case-registry.yaml') or {}
        self.intervention_registry = load_yaml(data_path / 'intervention-registry.yaml') or {}
        self.session_registry = load_yaml(data_path / 'model-building-session.yaml') or {}
        self.concept_registry = load_yaml(data_path / 'concept-registry.yaml') or {}
        self.parameter_registry = load_yaml(data_path / 'parameter-registry.yaml') or {}

        # BibTeX keys
        self.bib_keys = load_bibtex_keys(self.base_path / 'bibliography' / 'bcm_master.bib')

        # File-based references
        self.appendix_codes = get_existing_appendices(self.base_path / 'appendices')
        self.chapter_numbers = get_existing_chapters(self.base_path / 'chapters')

        if self.verbose:
            print(f"Loaded: {len(self.bib_keys)} BibTeX keys")
            print(f"Loaded: {len(self.appendix_codes)} appendix codes")
            print(f"Loaded: {len(self.chapter_numbers)} chapter numbers")

    def _add_error(self, error: ValidationError):
        """Add error to appropriate category"""
        if error.severity == 'critical':
            self.result.errors.append(error)
            self.result.checks_failed += 1
        elif error.severity == 'warning':
            self.result.warnings.append(error)
            self.result.checks_failed += 1
        else:
            self.result.info.append(error)
            self.result.checks_passed += 1

    def _check_passed(self):
        """Record a passed check"""
        self.result.checks_passed += 1

    # -------------------------------------------------------------------------
    # CHECK 1: model-registry → session
    # -------------------------------------------------------------------------
    def validate_model_sessions(self):
        """Validate that model sessions exist"""
        if self.verbose:
            print("\n[1/9] Checking model-registry → session references...")

        models = self.model_registry.get('models', [])
        sessions = self.session_registry.get('sessions', [])
        session_ids = {s.get('session_id') for s in sessions if s}

        for model in models:
            if not model:
                continue
            model_id = model.get('id', 'UNKNOWN')

            # Check created_in_session
            created_session = model.get('created_in_session')
            if created_session and created_session != 'null':
                if created_session not in session_ids:
                    self._add_error(ValidationError(
                        source_file='model-registry.yaml',
                        source_id=model_id,
                        target_file='model-building-session.yaml',
                        target_id=created_session,
                        error_type='missing_session',
                        severity='warning',
                        message=f"Model {model_id} references non-existent session: {created_session}"
                    ))
                else:
                    self._check_passed()

            # Check evolved_in_sessions
            evolved_sessions = model.get('evolved_in_sessions', [])
            for session_id in evolved_sessions:
                if session_id and session_id not in session_ids:
                    self._add_error(ValidationError(
                        source_file='model-registry.yaml',
                        source_id=model_id,
                        target_file='model-building-session.yaml',
                        target_id=session_id,
                        error_type='missing_session',
                        severity='warning',
                        message=f"Model {model_id} references non-existent evolved session: {session_id}"
                    ))
                else:
                    self._check_passed()

    # -------------------------------------------------------------------------
    # CHECK 2: model-registry → theory-catalog
    # -------------------------------------------------------------------------
    def validate_model_theories(self):
        """Validate that referenced theories exist"""
        if self.verbose:
            print("[2/9] Checking model-registry → theory-catalog references...")

        models = self.model_registry.get('models', [])

        # Build theory ID set
        theory_ids = set()
        categories = self.theory_catalog.get('categories', [])
        for cat in categories:
            if not cat:
                continue
            for theory in cat.get('theories', []):
                if theory:
                    theory_ids.add(theory.get('id'))

        for model in models:
            if not model:
                continue
            model_id = model.get('id', 'UNKNOWN')

            # Check theory_basis
            theory_basis = model.get('theory_basis', {})
            for section in ['primary', 'secondary']:
                theories = theory_basis.get(section, [])
                for theory_ref in theories:
                    if not theory_ref:
                        continue
                    theory_id = theory_ref.get('theory_id')
                    if theory_id and theory_id not in theory_ids:
                        self._add_error(ValidationError(
                            source_file='model-registry.yaml',
                            source_id=model_id,
                            target_file='theory-catalog.yaml',
                            target_id=theory_id,
                            error_type='missing_theory',
                            severity='warning',
                            message=f"Model {model_id} references non-existent theory: {theory_id}"
                        ))
                    else:
                        self._check_passed()

    # -------------------------------------------------------------------------
    # CHECK 3: model-registry → bcm_master.bib
    # -------------------------------------------------------------------------
    def validate_model_papers(self):
        """Validate that referenced papers exist in bibliography"""
        if self.verbose:
            print("[3/9] Checking model-registry → bcm_master.bib references...")

        models = self.model_registry.get('models', [])

        for model in models:
            if not model:
                continue
            model_id = model.get('id', 'UNKNOWN')

            # Check data_sources key_papers
            data_sources = model.get('data_sources', [])
            for source in data_sources:
                if not source:
                    continue
                key_papers = source.get('key_papers', [])
                for paper_key in key_papers:
                    if paper_key and paper_key not in self.bib_keys:
                        self._add_error(ValidationError(
                            source_file='model-registry.yaml',
                            source_id=model_id,
                            target_file='bcm_master.bib',
                            target_id=paper_key,
                            error_type='missing_paper',
                            severity='critical',
                            message=f"Model {model_id} references non-existent paper: {paper_key}"
                        ))
                    else:
                        self._check_passed()

    # -------------------------------------------------------------------------
    # CHECK 4: case-registry → appendices
    # -------------------------------------------------------------------------
    def validate_case_appendices(self):
        """Validate that case appendix references exist"""
        if self.verbose:
            print("[4/9] Checking case-registry → appendices references...")

        cases = self.case_registry.get('cases', {})

        for case_id, case_data in cases.items():
            if not case_data:
                continue

            refs = case_data.get('references', {})
            appendices = refs.get('appendices', [])

            for appendix_code in appendices:
                if appendix_code and appendix_code not in self.appendix_codes:
                    self._add_error(ValidationError(
                        source_file='case-registry.yaml',
                        source_id=case_id,
                        target_file='appendices/',
                        target_id=appendix_code,
                        error_type='missing_appendix',
                        severity='warning',
                        message=f"Case {case_id} references non-existent appendix: {appendix_code}"
                    ))
                else:
                    self._check_passed()

    # -------------------------------------------------------------------------
    # CHECK 5: case-registry → chapters
    # -------------------------------------------------------------------------
    def validate_case_chapters(self):
        """Validate that case chapter references exist"""
        if self.verbose:
            print("[5/9] Checking case-registry → chapters references...")

        cases = self.case_registry.get('cases', {})

        for case_id, case_data in cases.items():
            if not case_data:
                continue

            refs = case_data.get('references', {})
            chapters = refs.get('chapters', [])

            for chapter_num in chapters:
                if chapter_num and chapter_num not in self.chapter_numbers:
                    self._add_error(ValidationError(
                        source_file='case-registry.yaml',
                        source_id=case_id,
                        target_file='chapters/',
                        target_id=str(chapter_num),
                        error_type='missing_chapter',
                        severity='warning',
                        message=f"Case {case_id} references non-existent chapter: {chapter_num}"
                    ))
                else:
                    self._check_passed()

    # -------------------------------------------------------------------------
    # CHECK 6: case-registry → bcm_master.bib
    # -------------------------------------------------------------------------
    def validate_case_papers(self):
        """Validate that case literature references exist"""
        if self.verbose:
            print("[6/9] Checking case-registry → bcm_master.bib references...")

        cases = self.case_registry.get('cases', {})

        for case_id, case_data in cases.items():
            if not case_data:
                continue

            refs = case_data.get('references', {})
            literature = refs.get('literature', [])

            for paper_key in literature:
                if paper_key and paper_key not in self.bib_keys:
                    self._add_error(ValidationError(
                        source_file='case-registry.yaml',
                        source_id=case_id,
                        target_file='bcm_master.bib',
                        target_id=paper_key,
                        error_type='missing_paper',
                        severity='critical',
                        message=f"Case {case_id} references non-existent paper: {paper_key}"
                    ))
                else:
                    self._check_passed()

    # -------------------------------------------------------------------------
    # CHECK 7: theory-catalog → bcm_master.bib
    # -------------------------------------------------------------------------
    def validate_theory_papers(self):
        """Validate that theory bib_keys exist"""
        if self.verbose:
            print("[7/9] Checking theory-catalog → bcm_master.bib references...")

        categories = self.theory_catalog.get('categories', [])

        for cat in categories:
            if not cat:
                continue
            for theory in cat.get('theories', []):
                if not theory:
                    continue
                theory_id = theory.get('id', 'UNKNOWN')
                bib_keys = theory.get('bib_keys', [])

                for bib_key in bib_keys:
                    if bib_key and bib_key not in self.bib_keys:
                        self._add_error(ValidationError(
                            source_file='theory-catalog.yaml',
                            source_id=theory_id,
                            target_file='bcm_master.bib',
                            target_id=bib_key,
                            error_type='missing_paper',
                            severity='critical',
                            message=f"Theory {theory_id} references non-existent paper: {bib_key}"
                        ))
                    else:
                        self._check_passed()

    # -------------------------------------------------------------------------
    # CHECK 8: intervention-registry → model/case
    # -------------------------------------------------------------------------
    def validate_intervention_refs(self):
        """Validate intervention references to models and cases"""
        if self.verbose:
            print("[8/9] Checking intervention-registry references...")

        # Get model IDs
        model_ids = {m.get('id') for m in self.model_registry.get('models', []) if m}

        # Get case IDs
        case_ids = set(self.case_registry.get('cases', {}).keys())

        # Handle both dict and list structures for projects
        projects_data = self.intervention_registry.get('projects', {})

        # If projects is a dict (PRJ-001: {...}), iterate over items
        if isinstance(projects_data, dict):
            projects_iter = projects_data.items()
        else:
            # If it's a list, convert to compatible format
            projects_iter = [(p.get('id', f'UNKNOWN-{i}'), p) for i, p in enumerate(projects_data) if p]

        for project_id, project_data in projects_iter:
            if not project_data:
                continue

            # Check model references (could be in different locations)
            model_ref = project_data.get('model_used') or project_data.get('meta', {}).get('model_used')
            if model_ref and model_ref not in model_ids:
                self._add_error(ValidationError(
                    source_file='intervention-registry.yaml',
                    source_id=project_id,
                    target_file='model-registry.yaml',
                    target_id=model_ref,
                    error_type='missing_model',
                    severity='warning',
                    message=f"Project {project_id} references non-existent model: {model_ref}"
                ))
            elif model_ref:
                self._check_passed()

            # Check case references (could be in different locations)
            case_refs = project_data.get('related_cases', []) or project_data.get('meta', {}).get('related_cases', [])
            for case_ref in case_refs:
                if case_ref and case_ref not in case_ids:
                    self._add_error(ValidationError(
                        source_file='intervention-registry.yaml',
                        source_id=project_id,
                        target_file='case-registry.yaml',
                        target_id=case_ref,
                        error_type='missing_case',
                        severity='warning',
                        message=f"Project {project_id} references non-existent case: {case_ref}"
                    ))
                elif case_ref:
                    self._check_passed()

    # -------------------------------------------------------------------------
    # CHECK 9: concept-registry → bcm_master.bib
    # -------------------------------------------------------------------------
    def validate_concept_papers(self):
        """Validate concept evidence paper references"""
        if self.verbose:
            print("[9/9] Checking concept-registry → bcm_master.bib references...")

        concepts = self.concept_registry.get('concepts', [])

        for concept in concepts:
            if not concept:
                continue
            concept_id = concept.get('concept_id', 'UNKNOWN')

            # Check pro_evidence
            for evidence in concept.get('pro_evidence', []):
                if not evidence:
                    continue
                paper_key = evidence.get('paper_key')
                if paper_key and paper_key not in self.bib_keys:
                    self._add_error(ValidationError(
                        source_file='concept-registry.yaml',
                        source_id=concept_id,
                        target_file='bcm_master.bib',
                        target_id=paper_key,
                        error_type='missing_paper',
                        severity='critical',
                        message=f"Concept {concept_id} pro-evidence references non-existent paper: {paper_key}"
                    ))
                else:
                    self._check_passed()

            # Check contra_evidence
            for evidence in concept.get('contra_evidence', []):
                if not evidence:
                    continue
                paper_key = evidence.get('paper_key')
                if paper_key and paper_key not in self.bib_keys:
                    self._add_error(ValidationError(
                        source_file='concept-registry.yaml',
                        source_id=concept_id,
                        target_file='bcm_master.bib',
                        target_id=paper_key,
                        error_type='missing_paper',
                        severity='warning',
                        message=f"Concept {concept_id} contra-evidence references non-existent paper: {paper_key}"
                    ))
                else:
                    self._check_passed()

    # -------------------------------------------------------------------------
    # MAIN VALIDATION
    # -------------------------------------------------------------------------
    def validate_all(self) -> ValidationResult:
        """Run all validation checks"""
        print("=" * 70)
        print("REFERENTIAL INTEGRITY VALIDATION")
        print("=" * 70)

        # Run all checks
        self.validate_model_sessions()
        self.validate_model_theories()
        self.validate_model_papers()
        self.validate_case_appendices()
        self.validate_case_chapters()
        self.validate_case_papers()
        self.validate_theory_papers()
        self.validate_intervention_refs()
        self.validate_concept_papers()

        return self.result


# =============================================================================
# OUTPUT
# =============================================================================

def print_results(result: ValidationResult, verbose: bool = False):
    """Print validation results"""
    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)

    print(f"\nScore: {result.score:.1f}%")
    print(f"Checks Passed: {result.checks_passed}")
    print(f"Checks Failed: {result.checks_failed}")
    print(f"  - Critical Errors: {len(result.errors)}")
    print(f"  - Warnings: {len(result.warnings)}")

    if result.errors:
        print("\n" + "-" * 70)
        print("CRITICAL ERRORS (must fix)")
        print("-" * 70)
        for err in result.errors:
            print(f"\n  [{err.error_type}] {err.message}")
            print(f"    Source: {err.source_file}:{err.source_id}")
            print(f"    Target: {err.target_file}:{err.target_id}")

    if result.warnings and verbose:
        print("\n" + "-" * 70)
        print("WARNINGS")
        print("-" * 70)
        for warn in result.warnings:
            print(f"\n  [{warn.error_type}] {warn.message}")
            print(f"    Source: {warn.source_file}:{warn.source_id}")
            print(f"    Target: {warn.target_file}:{warn.target_id}")

    print("\n" + "=" * 70)

    if result.score >= 85:
        print("✅ PASSED: Referential integrity score >= 85%")
        return 0
    else:
        print("❌ FAILED: Referential integrity score < 85%")
        return 1


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description='Validate referential integrity across EBF databases')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed output')
    parser.add_argument('--fix', action='store_true', help='Attempt to auto-fix issues')
    parser.add_argument('--path', default='.', help='Base path to repository')
    args = parser.parse_args()

    # Find repository root
    base_path = Path(args.path).resolve()
    if not (base_path / 'data').exists():
        print(f"Error: Cannot find data/ directory in {base_path}")
        sys.exit(1)

    validator = ReferentialIntegrityValidator(base_path, verbose=args.verbose)
    result = validator.validate_all()

    exit_code = print_results(result, verbose=args.verbose)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
