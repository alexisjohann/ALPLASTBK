#!/usr/bin/env python3
# ┌─────────────────────────────────────────────────────────────────────────┐
# │  ⚠️  DEPRECATED (2026-02-08)                                            │
# │                                                                         │
# │  Paper-to-Cases Extractor (uses old paper-sources.yaml format)         │
# │  Kept for reference only.                                              │
# │                                                                         │
# │  SSOT: data/paper-references/PAP-*.yaml + bibliography/bcm_master.bib │
# │  Neue Papers: /integrate-paper Workflow                                │
# └─────────────────────────────────────────────────────────────────────────┘
# =============================================================================
# PAPER-TO-CASES EXTRACTOR - 10C Extraction from Behavioral Econ Papers
# =============================================================================
#
# Automatische Case-Generierung aus verhaltensökonomischen Papieren.
# Nutzt LLM-basierte 10C-Koordinaten-Extraktion.
#
# Workflow:
# 1. Paper-Metadaten laden (paper-sources.yaml)
# 2. Findings & Mechanismen extrahieren
# 3. 10C-Dimensionen inferieren (rule-based + LLM)
# 4. Cases aus Findings generieren
# 5. In case-registry.yaml speichern
#
# Usage:
#   python scripts/extract_cases_from_papers.py              # All papers
#   python scripts/extract_cases_from_papers.py --paper thaler2008nudge
#   python scripts/extract_cases_from_papers.py --dry-run
#
# =============================================================================

import yaml
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import argparse
import sys

sys.path.insert(0, str(Path(__file__).parent))

# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class PaperFinding:
    """A key finding from a paper"""
    finding_text: str
    domain: str
    stage: Optional[str]
    primary_intervention: Optional[str]
    effect_size: Optional[float]
    population: Optional[str]

@dataclass
class NineCCoordinates:
    """Extracted 10C coordinates from paper findings"""
    domain: str
    stages: List[str]
    primary_dimension: str
    psi_dominant: str
    gamma: float
    A_level: float
    W_level: float
    awareness_type: str
    key_insight: str

# =============================================================================
# CONFIGURATION LOADER
# =============================================================================

class PaperConfigLoader:
    """Load paper-sources.yaml configuration"""

    def __init__(self, config_path: str = "data/paper-sources.yaml"):
        self.config_path = Path(config_path)
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        """Load YAML configuration"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config not found: {self.config_path}")

        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)

    def get_sources(self) -> List[Dict]:
        """Get all paper sources"""
        return self.config.get('sources', [])

    def get_extraction_rules(self) -> Dict:
        """Get extraction rules"""
        return self.config.get('ingestion', {}).get('extraction_rules', [])

    def get_quality_filters(self) -> Dict:
        """Get quality filters"""
        return self.config.get('ingestion', {}).get('quality_filters', {})

# =============================================================================
# RULE-BASED 10C EXTRACTOR
# =============================================================================

class RuleBasedExtractor:
    """Extract 10C coordinates using rule-based mapping"""

    def __init__(self, config: PaperConfigLoader):
        self.config = config
        self.rules = config.get_extraction_rules()
        self.build_mappings()

    def build_mappings(self):
        """Build regex mappings from extraction rules"""
        self.domain_mapping = {}
        self.stage_mapping = {}
        self.dimension_mapping = {}
        self.psi_mapping = {}

        for rule in self.rules:
            if rule['rule_id'] == 'finding_to_domain':
                self.domain_mapping = rule['mapping']
            elif rule['rule_id'] == 'intervention_to_stage':
                self.stage_mapping = rule['mapping']
            elif rule['rule_id'] == 'mechanism_to_dimension':
                self.dimension_mapping = rule['mapping']
            elif rule['rule_id'] == 'context_to_psi':
                self.psi_mapping = rule['mapping']

    def extract_domain(self, text: str) -> Optional[str]:
        """Extract domain from text using regex"""
        text_lower = text.lower()

        for domain, keywords in self.domain_mapping.items():
            # keywords is a pipe-separated string like "energy|electricity|consumption"
            keyword_list = [kw.strip() for kw in keywords.split('|')]
            for keyword in keyword_list:
                if keyword in text_lower:
                    return domain

        return None

    def extract_stage(self, text: str) -> Optional[str]:
        """Extract stage from intervention description"""
        text_lower = text.lower()

        for stage, keywords in self.stage_mapping.items():
            keyword_list = [kw.strip() for kw in keywords.split('|')]
            for keyword in keyword_list:
                if keyword in text_lower:
                    return stage

        return None

    def extract_dimension(self, text: str) -> Optional[str]:
        """Extract primary FEPSDE dimension"""
        text_lower = text.lower()

        for dim, keywords in self.dimension_mapping.items():
            keyword_list = [kw.strip() for kw in keywords.split('|')]
            for keyword in keyword_list:
                if keyword in text_lower:
                    return dim

        return None

    def extract_psi(self, text: str) -> Optional[str]:
        """Extract dominant context dimension"""
        text_lower = text.lower()

        for psi, keywords in self.psi_mapping.items():
            keyword_list = [kw.strip() for kw in keywords.split('|')]
            for keyword in keyword_list:
                if keyword in text_lower:
                    return psi

        return None

    def infer_gamma(self, paper_data: Dict, finding: Dict) -> float:
        """Infer gamma (complementarity) from paper data"""
        # If explicitly provided, use it
        if 'gamma' in finding:
            return finding['gamma']

        # Otherwise infer from intervention complexity
        intervention = finding.get('primary_intervention', '')
        findings_str = ' '.join([str(f) for f in paper_data.get('key_findings', [])]) if isinstance(paper_data.get('key_findings'), list) else str(paper_data.get('key_findings', ''))
        text_lower = (paper_data.get('title', '') + ' ' + findings_str).lower()

        # High complementarity: multiple dimensions interact
        if 'social norm' in intervention or 'choice architecture' in intervention:
            return 0.6
        elif 'incentive' in intervention or 'commitment' in intervention:
            return 0.5
        else:
            return 0.3

    def infer_awareness(self, finding: Dict) -> Tuple[float, str]:
        """Infer awareness level and type"""
        if 'awareness_type' in finding:
            awareness_type = finding['awareness_type']
            # Map type to level
            if awareness_type == 'explicit':
                return 0.7, awareness_type
            elif awareness_type == 'implicit':
                return 0.3, awareness_type
            else:
                return 0.5, 'mixed'

        return 0.4, 'implicit'  # Default

    def infer_willingness(self, finding: Dict) -> float:
        """Infer willingness from effect size and stage"""
        stage = finding.get('stage')
        effect_size = finding.get('effect_size', 0.3)

        # Higher willingness if intervention is in action stage
        if stage == 'action':
            willingness = 0.7 + effect_size * 0.2
        elif stage == 'preparation':
            willingness = 0.5 + effect_size * 0.2
        elif stage == 'contemplation':
            willingness = 0.4
        else:  # precontemplation
            willingness = 0.2

        return max(0, min(1, willingness))

# =============================================================================
# PAPER PROCESSOR
# =============================================================================

class PaperProcessor:
    """Process paper data and extract cases"""

    def __init__(self, config: PaperConfigLoader):
        self.config = config
        self.extractor = RuleBasedExtractor(config)

    def process_paper(self, paper_data: Dict) -> List[Tuple[NineCCoordinates, Dict]]:
        """Process a single paper and extract 10C coordinates + case info"""
        cases = []

        # Check if paper has pre-extracted 10C coordinates
        if '9c_coordinates' in paper_data:
            # Use pre-extracted coordinates (faster path)
            pre_extracted = paper_data.get('9c_coordinates', [])
            findings = paper_data.get('key_findings', [])

            for i, coords_data in enumerate(pre_extracted):
                finding = findings[i] if i < len(findings) else {}

                coords = NineCCoordinates(
                    domain=coords_data.get('domain'),
                    stages=coords_data.get('stages', ['action']),
                    primary_dimension=finding.get('primary_dimension', 'F'),
                    psi_dominant=coords_data.get('psi_dominant', 'institutional'),
                    gamma=coords_data.get('gamma', 0.4),
                    A_level=coords_data.get('A_level', 0.5),
                    W_level=coords_data.get('W_level', 0.5),
                    awareness_type=coords_data.get('awareness_type', 'mixed'),
                    key_insight=coords_data.get('key_insight', finding.get('finding', ''))
                )

                case_info = {
                    'paper_id': paper_data.get('id'),
                    'authors': paper_data.get('authors', []),
                    'year': paper_data.get('year'),
                    'title': paper_data.get('title'),
                    'finding': finding.get('finding', ''),
                    'effect_size': finding.get('effect_size'),
                    'population': finding.get('population')
                }

                cases.append((coords, case_info))

            return cases

        # Otherwise extract findings
        findings = paper_data.get('key_findings', [])

        for finding in findings:
            # Extract basic info
            finding_text = finding.get('finding', '')
            domain = finding.get('domain') or self.extractor.extract_domain(finding_text)
            stage = finding.get('stage') or self.extractor.extract_stage(finding_text)
            dimension = finding.get('primary_dimension') or self.extractor.extract_dimension(finding_text) or 'F'  # Default to Financial
            psi = finding.get('psi_dominant') or self.extractor.extract_psi(finding_text) or 'institutional'  # Default context

            # Skip if critical info missing
            if not domain:
                continue

            # Infer missing values
            A_level, awareness_type = self.extractor.infer_awareness(finding)
            W_level = self.extractor.infer_willingness(finding)
            gamma = self.extractor.infer_gamma(paper_data, finding)
            psi = psi or 'institutional'  # Default

            # Build 10C coordinates
            coords = NineCCoordinates(
                domain=domain,
                stages=[stage] if stage else ['action'],
                primary_dimension=dimension,
                psi_dominant=psi,
                gamma=gamma,
                A_level=round(A_level, 2),
                W_level=round(W_level, 2),
                awareness_type=awareness_type,
                key_insight=finding_text
            )

            # Prepare case info
            case_info = {
                'paper_id': paper_data.get('id'),
                'authors': paper_data.get('authors', []),
                'year': paper_data.get('year'),
                'title': paper_data.get('title'),
                'finding': finding_text,
                'effect_size': finding.get('effect_size'),
                'population': finding.get('population')
            }

            cases.append((coords, case_info))

        return cases

    def generate_case_name(self, coords: NineCCoordinates, paper_title: str) -> str:
        """Generate human-readable case name"""
        stage_str = coords.stages[0].capitalize() if coords.stages else 'Action'
        domain_str = coords.domain.capitalize()

        return f"{domain_str} ({paper_title[:30]}...) - {stage_str}"

# =============================================================================
# CASE GENERATOR FROM PAPERS
# =============================================================================

class PaperCaseGenerator:
    """Generate complete YAML case entries from paper findings"""

    def __init__(self):
        pass

    def generate_case(
        self,
        coords: NineCCoordinates,
        case_info: Dict,
        case_id: str
    ) -> Dict:
        """Generate a complete case dictionary"""

        # Generate superkey
        superkey = self._generate_superkey(coords, case_info)

        # Generate case name
        paper_title = case_info.get('title', 'Unknown')
        case_name = f"{coords.domain.capitalize()} - {paper_title[:50]}"

        case = {
            'superkey': superkey,
            'name': case_name,
            'description': case_info.get('finding', 'Paper-derived case'),

            '10C': {
                'WHO': {
                    'levels': ['individual'],
                    'heterogeneity': 'mixed',
                    'segments': [case_info.get('population', 'general')]
                },
                'WHAT': {
                    'dimensions': [coords.primary_dimension],
                    'primary': coords.primary_dimension
                },
                'HOW': {
                    'gamma_avg': coords.gamma,
                    'interaction': self._gamma_to_interaction(coords.gamma)
                },
                'WHEN': {
                    'psi_dominant': coords.psi_dominant,
                    'temporal': 'experimental'
                },
                'WHERE': {
                    'source': 'empirical',
                    'confidence': 'high'
                },
                'AWARE': {
                    'A_level': coords.A_level,
                    'awareness_type': coords.awareness_type
                },
                'READY': {
                    'W_level': coords.W_level,
                    'theta': max(0, min(1, coords.W_level - 0.2))
                },
                'STAGE': {
                    'phase': coords.stages[0] if coords.stages else 'action',
                    'stability': 'medium'
                },
                'HIERARCHY': {
                    'primary_level': 'L2',
                    'N_L2': 1
                }
            },

            'domain': [coords.domain],
            'tags': ['paper-derived', coords.domain, coords.primary_dimension.lower(), case_info.get('year')],

            'insight': coords.key_insight,
            'implication': f"Study by {', '.join(case_info.get('authors', ['Unknown'])[:2])} ({case_info.get('year')}) demonstrates intervention effectiveness.",

            'formulas': [],
            'references': {
                'appendices': [],
                'chapters': [],
                'cases': [],
                'literature': [case_info.get('paper_id')]
            }
        }

        return case

    def _generate_superkey(self, coords: NineCCoordinates, case_info: Dict) -> str:
        """Generate unique superkey"""
        domain = coords.domain[0] if coords.domain else 'x'
        year = str(case_info.get('year', '0000'))[-2:]
        dimension = coords.primary_dimension.lower()
        psi = coords.psi_dominant[:3].lower()

        return f"{domain}:{year}:{dimension}:{psi}:{coords.W_level:.1f}"

    def _gamma_to_interaction(self, gamma: float) -> str:
        """Convert gamma to interaction type"""
        if gamma > 0.3:
            return 'complementary'
        elif gamma < 0:
            return 'substitutive'
        else:
            return 'additive'

# =============================================================================
# REGISTRY WRITER (reuse from generate_cases_auto.py)
# =============================================================================

class RegistryWriter:
    """Write validated cases to case-registry.yaml"""

    def __init__(self, registry_path: str):
        self.registry_path = Path(registry_path)
        self.data = self._load_registry()

    def _load_registry(self) -> Dict:
        """Load existing case registry"""
        if not self.registry_path.exists():
            return {'cases': {}}

        with open(self.registry_path, 'r') as f:
            return yaml.safe_load(f) or {'cases': {}}

    def add_case(self, case_id: str, case: Dict) -> bool:
        """Add case to registry"""
        if case_id in self.data.get('cases', {}):
            return False  # Already exists

        if 'cases' not in self.data:
            self.data['cases'] = {}

        self.data['cases'][case_id] = case
        return True

    def save(self) -> bool:
        """Save registry to file"""
        try:
            with open(self.registry_path, 'w') as f:
                yaml.dump(self.data, f, default_flow_style=False, sort_keys=False)
            return True
        except Exception as e:
            print(f"Error writing registry: {e}")
            return False

    def get_next_case_id(self) -> str:
        """Get next available case ID"""
        existing_ids = [int(cid.split('-')[1]) for cid in self.data.get('cases', {}).keys() if cid.startswith('CASE-')]
        next_id = max(existing_ids, default=0) + 1
        return f"CASE-{next_id:03d}"

# =============================================================================
# REPORT GENERATOR
# =============================================================================

class PaperReportGenerator:
    """Generate report of paper-to-case extraction"""

    def __init__(self, output_dir: str = "outputs/paper-to-cases-reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate(
        self,
        papers_processed: List[str],
        cases_generated: List[Tuple[str, Dict]],
        extraction_stats: Dict
    ) -> str:
        """Generate markdown report"""
        from datetime import datetime
        today = datetime.now().strftime('%Y-%m-%d')
        report_path = self.output_dir / f"{today}_papers.md"

        report = f"""# Paper-to-Cases Extraction Report - {today}

## Summary
- **Papers Processed**: {len(papers_processed)}
- **Cases Generated**: {len(cases_generated)}
- **Average Cases per Paper**: {len(cases_generated) / max(1, len(papers_processed)):.2f}

## Papers Processed
"""

        for paper_id in papers_processed:
            report += f"- {paper_id}\n"

        report += f"\n## Generated Cases\n"

        for case_id, case in cases_generated:
            report += f"\n### {case_id}: {case.get('name')}\n"
            report += f"- Domain: {', '.join(case.get('domain', []))}\n"
            report += f"- Insight: {case.get('insight', 'N/A')}\n"
            report += f"- Literature: {case.get('references', {}).get('literature', ['N/A'])[0]}\n"

        report += f"\n## Extraction Statistics\n"
        for stat, value in extraction_stats.items():
            report += f"- {stat}: {value}\n"

        try:
            with open(report_path, 'w') as f:
                f.write(report)
            return str(report_path)
        except Exception as e:
            print(f"Error writing report: {e}")
            return None

# =============================================================================
# MAIN ORCHESTRATOR
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="Paper-to-Cases Extractor")
    parser.add_argument('--paper', default=None, help="Specific paper ID to process")
    parser.add_argument('--dry-run', action='store_true', help="Preview only")
    parser.add_argument('--config', default='data/paper-sources.yaml')

    args = parser.parse_args()

    print("=" * 70)
    print("PAPER-TO-CASES EXTRACTION - Behavioral Economics Pipeline")
    print("=" * 70)

    # 1. Load configuration
    print("\n[1/4] Loading paper sources...")
    try:
        config = PaperConfigLoader(args.config)
        sources = config.get_sources()
        print(f"✅ Loaded {len(sources)} paper sources")
    except Exception as e:
        print(f"❌ Config load failed: {e}")
        return 1

    # 2. Process papers
    print(f"\n[2/4] Processing papers...")
    processor = PaperProcessor(config)
    case_generator = PaperCaseGenerator()
    writer = RegistryWriter('data/case-registry.yaml')

    generated_cases = []
    papers_processed = []
    total_findings = 0

    for source in sources:
        paper_id = source.get('id')

        # Filter by paper ID if specified
        if args.paper and args.paper != paper_id:
            continue

        papers_processed.append(paper_id)
        print(f"\n  Processing: {paper_id}")

        # Process paper
        case_list = processor.process_paper(source)
        print(f"    Extracted {len(case_list)} findings")

        for coords, case_info in case_list:
            total_findings += 1

            # Generate case
            case_id = writer.get_next_case_id()
            case = case_generator.generate_case(coords, case_info, case_id)

            generated_cases.append((case_id, case))
            print(f"    ✅ Generated {case_id}: {case.get('name')[:50]}...")

            if not args.dry_run:
                writer.add_case(case_id, case)

    # 3. Save
    print(f"\n[3/4] Saving cases...")
    if not args.dry_run:
        if writer.save():
            print("✅ Case registry updated")
        else:
            print("❌ Failed to save registry")

    # 4. Report
    print(f"\n[4/4] Generating report...")
    report_gen = PaperReportGenerator()
    stats = {
        'total_findings': total_findings,
        'cases_per_paper': len(generated_cases) / max(1, len(papers_processed)),
        'papers_processed': len(papers_processed)
    }
    report_path = report_gen.generate(papers_processed, generated_cases, stats)
    if report_path:
        print(f"✅ Report generated: {report_path}")

    print("\n" + "=" * 70)
    print(f"DONE: {len(generated_cases)} cases generated from {len(papers_processed)} papers")
    print("=" * 70)

    return 0

if __name__ == '__main__':
    exit(main())
