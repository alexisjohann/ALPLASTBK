#!/usr/bin/env python3
"""
Paper Integration Classifier
=============================

Automatically determines the integration level required for a new paper
in the EBF framework and updates BibTeX entries with integration protocol.

Usage:
    python scripts/classify_paper_integration.py --title "Paper Title" --abstract "..."
    python scripts/classify_paper_integration.py --doi "10.xxxx/xxxxx"
    python scripts/classify_paper_integration.py --interactive

    # Update BibTeX with integration protocol:
    python scripts/classify_paper_integration.py --update-bib --bib-key PAP-smith2026example \\
        --title "..." --abstract "..." --components "bibliography,case_registry:CAS-123"

Output:
    - Integration level (1-5)
    - Required components checklist
    - Estimated time
    - Suggested workflow
    - Updated BibTeX entry (with --update-bib)

Integration Levels:
    1. MINIMAL:     BibTeX only (replication, minor contribution)
    2. STANDARD:    BibTeX + theory_support + optional parameters
    3. CASE:        BibTeX + Case Registry entry
    4. THEORY:      BibTeX + new MS-XX-XXX entry in existing category
    5. FULL:        Complete theory integration (new category/domain)

Author: EBF Team
Version: 2.0
Date: January 2026
"""

import argparse
import yaml
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import date

# =============================================================================
# CLASSIFICATION CRITERIA
# =============================================================================

CLASSIFICATION_CRITERIA = {
    "new_theory_category": {
        "weight": 5,
        "indicators": [
            "new framework",
            "novel theory",
            "new model of",
            "unified theory",
            "general theory",
            "foundational",
            "paradigm",
        ],
        "questions": [
            "Does it introduce a fundamentally new way of thinking about behavior?",
            "Does it unify previously separate phenomena?",
            "Is it cited as foundational by other papers?",
        ]
    },
    "extends_existing_theory": {
        "weight": 3,
        "indicators": [
            "extends",
            "builds on",
            "generalizes",
            "application of",
            "test of",
            "replication",
        ],
        "questions": [
            "Does it extend an existing theory in the catalog?",
            "Does it apply a known theory to a new domain?",
        ]
    },
    "new_domain": {
        "weight": 4,
        "indicators": [
            "first study",
            "novel application",
            "new market",
            "emerging",
            "digital platform",
            "cryptocurrency",
            "AI",
            "machine learning",
        ],
        "questions": [
            "Does it open a new application domain not covered in EBF?",
            "Is this the first behavioral study in this area?",
        ]
    },
    "empirical_parameters": {
        "weight": 2,
        "indicators": [
            "we estimate",
            "we find that",
            "coefficient",
            "parameter",
            "effect size",
            "elasticity",
            "λ =",
            "β =",
            "γ =",
        ],
        "questions": [
            "Does it provide new parameter estimates?",
            "Are the parameters generalizable beyond this study?",
        ]
    },
    "policy_implications": {
        "weight": 2,
        "indicators": [
            "policy",
            "regulation",
            "intervention",
            "nudge",
            "welfare",
            "antitrust",
            "FTC",
            "government",
        ],
        "questions": [
            "Does it have direct policy implications?",
            "Could it inform regulatory decisions?",
        ]
    },
    "field_experiment": {
        "weight": 2,
        "indicators": [
            "field experiment",
            "RCT",
            "randomized controlled",
            "natural experiment",
            "quasi-experiment",
        ],
        "questions": [
            "Is it based on a field experiment?",
            "Does it provide causal identification?",
        ]
    },
    "case_study_worthy": {
        "weight": 1,
        "indicators": [
            "case study",
            "real-world",
            "applied",
            "practical",
            "implementation",
        ],
        "questions": [
            "Would this make a good worked example?",
            "Is it a memorable illustration of a theory?",
        ]
    },
}

# =============================================================================
# INTEGRATION LEVELS
# =============================================================================

INTEGRATION_LEVELS = {
    1: {
        "name": "MINIMAL",
        "description": "BibTeX entry only",
        "components": ["bibliography"],
        "time_estimate": "5 min",
        "triggers": "Replication, minor contribution, tangential relevance",
    },
    2: {
        "name": "STANDARD",
        "description": "BibTeX + theory link + optional parameters",
        "components": ["bibliography", "theory_support"],
        "optional": ["parameter_registry"],
        "time_estimate": "10-15 min",
        "triggers": "Extends existing theory, provides new parameters",
    },
    3: {
        "name": "CASE",
        "description": "BibTeX + Case Registry entry",
        "components": ["bibliography", "theory_support", "case_registry"],
        "optional": ["parameter_registry"],
        "time_estimate": "15-20 min",
        "triggers": "Good worked example, memorable case study",
    },
    4: {
        "name": "THEORY",
        "description": "BibTeX + new theory entry in existing category",
        "components": ["bibliography", "theory_catalog", "parameter_registry"],
        "optional": ["case_registry", "model_registry"],
        "time_estimate": "20-30 min",
        "triggers": "New theory variant, significant extension",
    },
    5: {
        "name": "FULL",
        "description": "Complete theory integration",
        "components": [
            "bibliography",
            "theory_catalog (new category)",
            "model_registry",
            "parameter_registry",
            "case_registry",
            "latex_appendix",
            "chapter_mapping",
            "formal_proofs (DER)",
        ],
        "time_estimate": "60-90 min",
        "triggers": "New theory category, new domain, foundational paper",
    },
}

# =============================================================================
# CLASSIFIER CLASS
# =============================================================================

class PaperIntegrationClassifier:
    """Classifies papers and determines required integration level."""

    def __init__(self, theory_catalog_path: str = None, bib_path: str = None):
        self.theory_catalog = self._load_theory_catalog(theory_catalog_path)
        self.existing_theories = self._extract_theory_names()
        self.existing_categories = self._extract_category_names()

    def _load_theory_catalog(self, path: str = None) -> dict:
        """Load the theory catalog YAML."""
        if path is None:
            path = Path(__file__).parent.parent / "data" / "theory-catalog.yaml"
        try:
            with open(path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            return {"categories": []}

    def _extract_theory_names(self) -> List[str]:
        """Extract all theory names from catalog."""
        names = []
        for cat in self.theory_catalog.get("categories", []):
            for theory in cat.get("theories", []):
                names.append(theory.get("name", "").lower())
        return names

    def _extract_category_names(self) -> List[str]:
        """Extract all category names from catalog."""
        return [cat.get("name", "").lower()
                for cat in self.theory_catalog.get("categories", [])]

    def classify(self, title: str, abstract: str,
                 answers: Dict[str, bool] = None) -> Tuple[int, dict]:
        """
        Classify a paper and return integration level.

        Args:
            title: Paper title
            abstract: Paper abstract
            answers: Optional dict of yes/no answers to classification questions

        Returns:
            Tuple of (integration_level, details_dict)
        """
        text = f"{title} {abstract}".lower()
        scores = {}
        triggers = []

        # Score each criterion
        for criterion, config in CLASSIFICATION_CRITERIA.items():
            score = 0

            # Check text indicators
            for indicator in config["indicators"]:
                if indicator.lower() in text:
                    score += 1
                    triggers.append(f"{criterion}: found '{indicator}'")

            # Check manual answers if provided
            if answers:
                for q in config["questions"]:
                    q_key = q[:50]  # Use truncated question as key
                    if answers.get(q_key, False):
                        score += 2
                        triggers.append(f"{criterion}: confirmed by user")

            scores[criterion] = score * config["weight"]

        # Determine integration level
        total_score = sum(scores.values())

        # Check for specific high-impact triggers
        is_new_category = scores["new_theory_category"] >= 10
        is_new_domain = scores["new_domain"] >= 8
        has_parameters = scores["empirical_parameters"] >= 4
        is_case_worthy = scores["case_study_worthy"] >= 2
        extends_theory = scores["extends_existing_theory"] >= 6

        # Determine level
        if is_new_category or (is_new_domain and has_parameters):
            level = 5  # FULL
        elif extends_theory and has_parameters and not self._theory_exists(title):
            level = 4  # THEORY
        elif is_case_worthy or (has_parameters and scores["field_experiment"] >= 4):
            level = 3  # CASE
        elif extends_theory or has_parameters:
            level = 2  # STANDARD
        else:
            level = 1  # MINIMAL

        details = {
            "level": level,
            "level_name": INTEGRATION_LEVELS[level]["name"],
            "scores": scores,
            "total_score": total_score,
            "triggers": triggers,
            "components": INTEGRATION_LEVELS[level]["components"],
            "optional": INTEGRATION_LEVELS[level].get("optional", []),
            "time_estimate": INTEGRATION_LEVELS[level]["time_estimate"],
            "rationale": INTEGRATION_LEVELS[level]["triggers"],
        }

        return level, details

    def _theory_exists(self, title: str) -> bool:
        """Check if a similar theory already exists."""
        title_words = set(title.lower().split())
        for theory in self.existing_theories:
            theory_words = set(theory.split())
            if len(title_words & theory_words) >= 2:
                return True
        return False

    def get_questions(self) -> List[str]:
        """Get all classification questions for interactive mode."""
        questions = []
        for criterion, config in CLASSIFICATION_CRITERIA.items():
            for q in config["questions"]:
                questions.append((criterion, q))
        return questions

    def generate_checklist(self, level: int, details: dict) -> str:
        """Generate a checklist for the integration workflow."""
        lines = [
            f"# Paper Integration Checklist",
            f"## Level {level}: {INTEGRATION_LEVELS[level]['name']}",
            f"",
            f"**Estimated Time:** {details['time_estimate']}",
            f"**Rationale:** {details['rationale']}",
            f"",
            f"## Required Components",
        ]

        for comp in details["components"]:
            lines.append(f"- [ ] {comp}")

        if details.get("optional"):
            lines.append("")
            lines.append("## Optional Components")
            for comp in details["optional"]:
                lines.append(f"- [ ] {comp}")

        lines.append("")
        lines.append("## Classification Triggers")
        for trigger in details["triggers"][:10]:  # Limit to top 10
            lines.append(f"- {trigger}")

        return "\n".join(lines)


# =============================================================================
# BIBTEX UPDATE FUNCTIONALITY
# =============================================================================

class BibTeXUpdater:
    """Updates BibTeX entries with integration protocol fields."""

    def __init__(self, bib_path: str = None):
        if bib_path is None:
            bib_path = Path(__file__).parent.parent / "bibliography" / "bcm_master.bib"
        self.bib_path = Path(bib_path)
        self.content = None

    def load(self) -> str:
        """Load BibTeX file content."""
        with open(self.bib_path, 'r', encoding='utf-8') as f:
            self.content = f.read()
        return self.content

    def save(self) -> None:
        """Save BibTeX file content."""
        with open(self.bib_path, 'w', encoding='utf-8') as f:
            f.write(self.content)

    def find_entry(self, bib_key: str) -> Tuple[int, int]:
        """
        Find the start and end position of a BibTeX entry.

        Returns:
            Tuple of (start_pos, end_pos) or (-1, -1) if not found
        """
        if self.content is None:
            self.load()

        # Find the entry start
        pattern = rf'@\w+\{{{bib_key}\s*,'
        match = re.search(pattern, self.content)
        if not match:
            return (-1, -1)

        start_pos = match.start()

        # Find the matching closing brace
        brace_count = 0
        end_pos = start_pos
        in_entry = False

        for i, char in enumerate(self.content[start_pos:], start=start_pos):
            if char == '{':
                brace_count += 1
                in_entry = True
            elif char == '}':
                brace_count -= 1
                if in_entry and brace_count == 0:
                    end_pos = i + 1
                    break

        return (start_pos, end_pos)

    def get_entry(self, bib_key: str) -> Optional[str]:
        """Get a BibTeX entry by key."""
        start, end = self.find_entry(bib_key)
        if start == -1:
            return None
        return self.content[start:end]

    def has_field(self, bib_key: str, field_name: str) -> bool:
        """Check if entry has a specific field."""
        entry = self.get_entry(bib_key)
        if entry is None:
            return False
        pattern = rf'^\s*{field_name}\s*=\s*'
        return bool(re.search(pattern, entry, re.MULTILINE))

    def update_entry_with_protocol(
        self,
        bib_key: str,
        level: int,
        score: int,
        components: str,
        triggers: List[str] = None
    ) -> bool:
        """
        Add/update integration protocol fields in a BibTeX entry.

        Fields added:
            - integration_level
            - integration_score
            - integration_date
            - integration_components
            - integration_triggers (optional)

        Returns:
            True if successful, False otherwise
        """
        if self.content is None:
            self.load()

        start, end = self.find_entry(bib_key)
        if start == -1:
            print(f"ERROR: BibTeX entry '{bib_key}' not found")
            return False

        entry = self.content[start:end]
        today = date.today().isoformat()

        # Build the new fields
        new_fields = f"""  % === INTEGRATION PROTOCOL (auto-generated) ===
  integration_level = {{{level}}},
  integration_score = {{{score}}},
  integration_date = {{{today}}},
  integration_components = {{{components}}},"""

        if triggers:
            # Take top 3 triggers, escape special chars
            top_triggers = "; ".join(triggers[:3]).replace("{", "").replace("}", "")
            new_fields += f"""
  integration_triggers = {{{top_triggers}}},"""

        # Find where to insert (before the closing brace, after last field)
        # Look for the last field line (ends with },)
        lines = entry.split('\n')
        insert_line_idx = len(lines) - 1

        # Find the last line with actual content before closing brace
        for i in range(len(lines) - 1, -1, -1):
            line = lines[i].strip()
            if line and line != '}':
                insert_line_idx = i + 1
                break

        # Check if protocol fields already exist
        if 'integration_level' in entry:
            # Update existing fields instead of adding
            entry = re.sub(
                r'integration_level\s*=\s*\{[^}]*\}',
                f'integration_level = {{{level}}}',
                entry
            )
            entry = re.sub(
                r'integration_score\s*=\s*\{[^}]*\}',
                f'integration_score = {{{score}}}',
                entry
            )
            entry = re.sub(
                r'integration_date\s*=\s*\{[^}]*\}',
                f'integration_date = {{{today}}}',
                entry
            )
            entry = re.sub(
                r'integration_components\s*=\s*\{[^}]*\}',
                f'integration_components = {{{components}}}',
                entry
            )
            if triggers:
                top_triggers = "; ".join(triggers[:3]).replace("{", "").replace("}", "")
                if 'integration_triggers' in entry:
                    entry = re.sub(
                        r'integration_triggers\s*=\s*\{[^}]*\}',
                        f'integration_triggers = {{{top_triggers}}}',
                        entry
                    )
                else:
                    # Add triggers field after integration_components
                    entry = re.sub(
                        r'(integration_components\s*=\s*\{[^}]*\}),',
                        f'\\1,\n  integration_triggers = {{{top_triggers}}},',
                        entry
                    )
        else:
            # Insert new fields
            lines.insert(insert_line_idx, new_fields)
            entry = '\n'.join(lines)

        # Replace the entry in content
        self.content = self.content[:start] + entry + self.content[end:]
        return True

    def update_and_save(
        self,
        bib_key: str,
        level: int,
        score: int,
        components: str,
        triggers: List[str] = None
    ) -> bool:
        """Update entry and save file."""
        success = self.update_entry_with_protocol(
            bib_key, level, score, components, triggers
        )
        if success:
            self.save()
            print(f"✅ Updated {bib_key} with integration protocol")
            print(f"   Level: {level}, Score: {score}")
            print(f"   Components: {components}")
        return success


# =============================================================================
# CLI INTERFACE
# =============================================================================

def interactive_classify(classifier: PaperIntegrationClassifier):
    """Interactive classification mode."""
    print("\n" + "="*70)
    print("  PAPER INTEGRATION CLASSIFIER - Interactive Mode")
    print("="*70 + "\n")

    title = input("Paper Title: ").strip()
    print("\nPaste Abstract (end with empty line):")
    abstract_lines = []
    while True:
        line = input()
        if line == "":
            break
        abstract_lines.append(line)
    abstract = " ".join(abstract_lines)

    # Quick classification first
    level, details = classifier.classify(title, abstract)

    print(f"\n📊 Initial Classification: Level {level} ({details['level_name']})")
    print(f"   Score: {details['total_score']}")

    # Ask follow-up questions for borderline cases
    if 2 <= level <= 4:
        print("\n📝 Please answer a few questions to refine classification:")
        answers = {}
        questions = classifier.get_questions()

        for criterion, question in questions[:5]:  # Ask top 5 questions
            response = input(f"   {question} (y/n): ").strip().lower()
            answers[question[:50]] = response in ['y', 'yes', 'ja', '1']

        # Re-classify with answers
        level, details = classifier.classify(title, abstract, answers)

    # Print final result
    print("\n" + "="*70)
    print(f"  FINAL CLASSIFICATION: Level {level} - {details['level_name']}")
    print("="*70)
    print(f"\n⏱️  Estimated Time: {details['time_estimate']}")
    print(f"📋 Components Required:")
    for comp in details["components"]:
        print(f"   • {comp}")
    if details.get("optional"):
        print(f"\n📋 Optional Components:")
        for comp in details["optional"]:
            print(f"   • {comp}")

    print("\n" + "-"*70)
    print("TRIGGERS:")
    for trigger in details["triggers"][:5]:
        print(f"   → {trigger}")

    # Generate checklist
    checklist = classifier.generate_checklist(level, details)
    print("\n" + "-"*70)
    print("CHECKLIST:")
    print(checklist)

    return level, details


def main():
    parser = argparse.ArgumentParser(
        description="Classify paper integration level for EBF"
    )
    parser.add_argument("--title", "-t", help="Paper title")
    parser.add_argument("--abstract", "-a", help="Paper abstract")
    parser.add_argument("--doi", "-d", help="Paper DOI (for fetching metadata)")
    parser.add_argument("--interactive", "-i", action="store_true",
                       help="Interactive mode")
    parser.add_argument("--json", action="store_true",
                       help="Output as JSON")

    # BibTeX update arguments
    parser.add_argument("--update-bib", action="store_true",
                       help="Update BibTeX entry with integration protocol")
    parser.add_argument("--bib-key", "-k",
                       help="BibTeX entry key (e.g., PAP-smith2026example)")
    parser.add_argument("--components", "-c",
                       help="Completed components (e.g., 'bibliography,case_registry:CAS-123')")
    parser.add_argument("--bib-path",
                       help="Path to BibTeX file (default: bibliography/bcm_master.bib)")

    args = parser.parse_args()

    classifier = PaperIntegrationClassifier()

    if args.interactive:
        level, details = interactive_classify(classifier)

        # After interactive classification, offer to update BibTeX
        if level and details:
            update = input("\n📝 Update BibTeX entry with protocol? (y/n): ").strip().lower()
            if update in ['y', 'yes', 'ja']:
                bib_key = input("   BibTeX key (e.g., PAP-author2026title): ").strip()
                components = input("   Completed components (e.g., bibliography,case_registry:CAS-123): ").strip()
                if bib_key and components:
                    updater = BibTeXUpdater(args.bib_path)
                    updater.update_and_save(
                        bib_key,
                        level,
                        details['total_score'],
                        components,
                        details.get('triggers', [])
                    )

    elif args.update_bib:
        # Update BibTeX mode
        if not args.bib_key:
            print("ERROR: --bib-key required with --update-bib")
            sys.exit(1)
        if not args.components:
            print("ERROR: --components required with --update-bib")
            sys.exit(1)
        if not args.title or not args.abstract:
            print("ERROR: --title and --abstract required with --update-bib")
            sys.exit(1)

        # Classify the paper
        level, details = classifier.classify(args.title, args.abstract)

        # Update BibTeX
        updater = BibTeXUpdater(args.bib_path)
        success = updater.update_and_save(
            args.bib_key,
            level,
            details['total_score'],
            args.components,
            details.get('triggers', [])
        )

        if success:
            print(f"\n📊 Classification: Level {level} ({details['level_name']})")
        else:
            sys.exit(1)

    elif args.title and args.abstract:
        level, details = classifier.classify(args.title, args.abstract)

        if args.json:
            import json
            print(json.dumps(details, indent=2))
        else:
            print(f"Level: {level} ({details['level_name']})")
            print(f"Time: {details['time_estimate']}")
            print(f"Components: {', '.join(details['components'])}")

            # Show update command hint
            print(f"\n💡 To update BibTeX, run:")
            print(f"   python scripts/classify_paper_integration.py --update-bib \\")
            print(f"       --bib-key PAP-author2026title \\")
            print(f"       --title \"{args.title[:30]}...\" \\")
            print(f"       --abstract \"...\" \\")
            print(f"       --components \"bibliography,...\"")
    else:
        parser.print_help()
        print("\n💡 Tip: Use --interactive for guided classification")
        print("💡 Tip: Use --update-bib to add integration protocol to BibTeX entry")


if __name__ == "__main__":
    main()
