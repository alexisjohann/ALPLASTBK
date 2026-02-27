#!/usr/bin/env python3
# =============================================================================
# RANDOMIZED CASE GENERATION - LLMMC-Based Auto-Producer
# =============================================================================
#
# Automated Case Generation mit validiertem Zufallssampling
# Ref: Appendix AN (METHOD-LLMMC), data/case-generation-sources.yaml
#
# Usage:
#   python scripts/generate_cases_auto.py              # Use config defaults
#   python scripts/generate_cases_auto.py --max 5      # Max 5 cases
#   python scripts/generate_cases_auto.py --dry-run    # Preview only
#
# =============================================================================

import yaml
import json
import random
import hashlib
import datetime
import argparse
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import sys

# Add scripts to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# =============================================================================
# DATA CLASSES
# =============================================================================

class Stage(Enum):
    """Behavioral Change Journey Stages"""
    PRECONTEMPLATION = "precontemplation"
    CONTEMPLATION = "contemplation"
    PREPARATION = "preparation"
    ACTION = "action"
    MAINTENANCE = "maintenance"

class HierarchyLevel(Enum):
    """Decision Hierarchy Levels"""
    L0 = "L0"
    L1 = "L1"
    L2 = "L2"
    L3 = "L3"

@dataclass
class RandomCoordinates:
    """Randomly sampled 10C coordinates"""
    domain: str
    stage: Stage
    hierarchy_level: HierarchyLevel
    gamma: float
    psi_dominant: str
    A_level: float
    W_level: float
    primary_dimension: str
    heterogeneity: str
    awareness_type: str
    segments: List[str]

# =============================================================================
# CONFIGURATION LOADER
# =============================================================================

class ConfigLoader:
    """Load and validate case-generation-sources.yaml"""

    def __init__(self, config_path: str):
        self.config_path = Path(config_path)
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        """Load YAML configuration"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config not found: {self.config_path}")

        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)

    def get_generation_strategy(self) -> Dict:
        """Get generation strategy parameters"""
        return self.config.get('generation_strategy', {})

    def get_sampling_config(self) -> Dict:
        """Get LLMMC sampling configuration"""
        return self.get_generation_strategy().get('sampling', {})

    def get_validation_rules(self) -> Dict:
        """Get validation rules"""
        return self.get_generation_strategy().get('validation', {})

    def get_schedule(self) -> Dict:
        """Get automation schedule"""
        return self.config.get('schedule', {})

# =============================================================================
# RANDOM COORDINATE SAMPLER (LLMMC-based)
# =============================================================================

class LLMMCRandomSampler:
    """Sample random 10C coordinates using LLMMC strategy"""

    def __init__(self, config: ConfigLoader):
        self.config = config
        self.sampling_cfg = config.get_sampling_config()
        self.existing_superkeys = self._load_existing_superkeys()

    def _load_existing_superkeys(self) -> set:
        """Load existing superkeys to prevent duplicates"""
        registry_path = Path(__file__).parent.parent / "data" / "case-registry.yaml"
        if not registry_path.exists():
            return set()

        with open(registry_path, 'r') as f:
            data = yaml.safe_load(f)

        superkeys = set()
        for case_id, case_data in data.get('cases', {}).items():
            if 'superkey' in case_data:
                superkeys.add(case_data['superkey'])

        return superkeys

    def sample_domain(self) -> str:
        """Sample domain with weighted distribution"""
        domains_cfg = self.sampling_cfg.get('domains', [])
        domains = [d['name'] for d in domains_cfg]
        weights = [d['weight'] for d in domains_cfg]
        return random.choices(domains, weights=weights, k=1)[0]

    def sample_stage(self) -> Stage:
        """Sample stage with weighted distribution"""
        stages_cfg = self.sampling_cfg.get('stages', {})
        stages = [Stage(k) for k in stages_cfg.keys()]
        weights = [stages_cfg[s.value]['weight'] for s in stages]
        return random.choices(stages, weights=weights, k=1)[0]

    def sample_hierarchy_level(self) -> HierarchyLevel:
        """Sample hierarchy level with weighted distribution"""
        levels_cfg = self.sampling_cfg.get('hierarchy_levels', {})
        levels = [HierarchyLevel[k] for k in levels_cfg.keys()]
        weights = [levels_cfg[l.name]['weight'] for l in levels]
        return random.choices(levels, weights=weights, k=1)[0]

    def sample_gamma(self) -> float:
        """Sample γ (complementarity) from normal distribution"""
        cfg = self.sampling_cfg.get('9c_distributions', {}).get('HOW', {})
        mean = cfg.get('gamma_mean', 0.4)
        std = cfg.get('gamma_std', 0.25)
        min_val = cfg.get('gamma_min', -0.5)
        max_val = cfg.get('gamma_max', 0.9)

        gamma = random.gauss(mean, std)
        return max(min_val, min(max_val, gamma))

    def sample_psi_dominant(self) -> str:
        """Sample dominant context dimension"""
        dims = self.sampling_cfg.get('9c_distributions', {}).get('WHEN', {}).get('psi_dimensions', [])
        return random.choice(dims)

    def sample_awareness_level(self) -> float:
        """Sample A(·) awareness level"""
        cfg = self.sampling_cfg.get('9c_distributions', {}).get('AWARE', {})
        return max(0, min(1, random.gauss(cfg.get('A_mean', 0.5), cfg.get('A_std', 0.25))))

    def sample_willingness_level(self) -> float:
        """Sample W(·) willingness level"""
        cfg = self.sampling_cfg.get('9c_distributions', {}).get('READY', {})
        return max(0, min(1, random.gauss(cfg.get('W_mean', 0.5), cfg.get('W_std', 0.25))))

    def sample_primary_dimension(self) -> str:
        """Sample primary utility dimension (FEPSDE)"""
        cfg = self.sampling_cfg.get('9c_distributions', {}).get('WHAT', {})
        dist = cfg.get('primary_distribution', {})
        dims = list(dist.keys())
        weights = list(dist.values())
        return random.choices(dims, weights=weights, k=1)[0]

    def sample_heterogeneity(self) -> str:
        """Sample heterogeneity level"""
        return random.choice(['low', 'medium', 'high'])

    def sample_awareness_type(self) -> str:
        """Sample awareness type"""
        cfg = self.sampling_cfg.get('9c_distributions', {}).get('AWARE', {})
        return random.choice(cfg.get('awareness_types', ['explicit', 'implicit', 'mixed']))

    def apply_constraints(self, coords: RandomCoordinates) -> bool:
        """Check if coordinates satisfy logical constraints"""
        constraints = self.config.get_generation_strategy().get('constraints', {})
        if not constraints.get('enabled', True):
            return True

        # Constraint 1: Precontemplation → Low A
        if coords.stage == Stage.PRECONTEMPLATION and coords.A_level > 0.4:
            return False

        # Constraint 2: Action → High W
        if coords.stage == Stage.ACTION and coords.W_level < 0.5:
            return False

        # Constraint 3: Hierarchy-Domain affinity
        scope_req = constraints.get('rules', [{}])[-1].get('scope_requirements', {})
        if coords.hierarchy_level.value in scope_req:
            if coords.domain not in scope_req[coords.hierarchy_level.value]:
                return False

        return True

    def generate_superkey(self, coords: RandomCoordinates) -> str:
        """Generate superkey: {domain}:{stage}:{hierarchy}:{psi}:{primary_dim}"""
        superkey = f"{coords.domain[0]}:{coords.stage.value}:{coords.hierarchy_level.value}:{coords.psi_dominant}:{coords.primary_dimension.lower()}"

        # Check uniqueness
        if superkey in self.existing_superkeys:
            return None  # Duplicate

        return superkey

    def sample(self) -> Optional[RandomCoordinates]:
        """Sample random 10C coordinates (with constraint checking)"""
        max_attempts = 5

        for attempt in range(max_attempts):
            domain = self.sample_domain()
            coords = RandomCoordinates(
                domain=domain,
                stage=self.sample_stage(),
                hierarchy_level=self.sample_hierarchy_level(),
                gamma=self.sample_gamma(),
                psi_dominant=self.sample_psi_dominant(),
                A_level=self.sample_awareness_level(),
                W_level=self.sample_willingness_level(),
                primary_dimension=self.sample_primary_dimension(),
                heterogeneity=self.sample_heterogeneity(),
                awareness_type=self.sample_awareness_type(),
                segments=[domain]  # Placeholder
            )

            # Check constraints
            if not self.apply_constraints(coords):
                continue

            # Generate superkey (with uniqueness check)
            superkey = self.generate_superkey(coords)
            if superkey is None:
                continue

            # Success
            return coords

        return None  # Failed after max attempts

# =============================================================================
# CASE GENERATOR (with Claude)
# =============================================================================

class CaseGenerator:
    """Generate full case from random coordinates"""

    def __init__(self, config: ConfigLoader):
        self.config = config
        self.generation_cfg = config.get_generation_strategy().get('generation', {})

    def generate_case_from_coordinates(self, coords: RandomCoordinates, case_id: str) -> Optional[Dict]:
        """
        Generate a complete case from random coordinates.
        In production: Uses Claude API. For demo: Returns template.
        """

        # For now: Return template structure
        # In production: Call Claude API with prompt from generation_cfg

        superkey = f"{coords.domain}:{coords.stage.value}:{coords.hierarchy_level.value}:{coords.psi_dominant}"

        case = {
            'superkey': superkey,
            'name': f"{coords.domain.capitalize()} - {coords.stage.value.capitalize()} ({coords.primary_dimension})",
            'description': f"Auto-generated case from random 10C sampling. Domain: {coords.domain}, Stage: {coords.stage.value}, γ: {coords.gamma:.2f}",

            '10C': {
                'WHO': {
                    'levels': ['individual'],
                    'heterogeneity': coords.heterogeneity,
                    'segments': coords.segments
                },
                'WHAT': {
                    'dimensions': [coords.primary_dimension],
                    'primary': coords.primary_dimension
                },
                'HOW': {
                    'gamma_avg': round(coords.gamma, 2),
                    'interaction': 'complementary' if coords.gamma > 0.3 else ('substitutive' if coords.gamma < 0 else 'additive')
                },
                'WHEN': {
                    'psi_dominant': coords.psi_dominant,
                    'temporal': 'dynamic'
                },
                'WHERE': {
                    'source': random.choice(['literature', 'empirical', 'hybrid']),
                    'confidence': random.choice(['low', 'medium', 'high'])
                },
                'AWARE': {
                    'A_level': round(coords.A_level, 2),
                    'awareness_type': coords.awareness_type
                },
                'READY': {
                    'W_level': round(coords.W_level, 2),
                    'theta': round(random.gauss(0.5, 0.2), 2)
                },
                'STAGE': {
                    'phase': coords.stage.value,
                    'stability': random.choice(['low', 'medium', 'high'])
                },
                'HIERARCHY': {
                    'primary_level': coords.hierarchy_level.value,
                    'N_L2': round(random.gauss(1.5, 0.5), 1)
                }
            },

            'domain': [coords.domain],
            'tags': [coords.domain, coords.stage.value, coords.primary_dimension.lower(), 'auto-generated'],
            'insight': f"Randomly generated case exploring {coords.domain} in {coords.stage.value} phase with {coords.primary_dimension} focus.",
            'implication': f"This case highlights the importance of context (ψ={coords.psi_dominant}) and complementarity (γ={coords.gamma:.2f}) in {coords.domain}.",

            'formulas': [],
            'references': {
                'appendices': [],
                'chapters': [],
                'cases': [],
                'literature': []
            }
        }

        return case

# =============================================================================
# CASE VALIDATOR
# =============================================================================

class CaseValidator:
    """Validate generated cases"""

    def __init__(self, config: ConfigLoader):
        self.config = config
        self.validation_cfg = config.get_generation_strategy().get('validation', {})

    def validate(self, case: Dict, case_id: str) -> Tuple[bool, List[str]]:
        """Validate case and return (is_valid, errors)"""
        errors = []

        # Check 1: Superkey uniqueness
        if not self._check_superkey_uniqueness(case.get('superkey')):
            errors.append("Superkey duplicate or missing")

        # Check 2: 10C completeness
        if not self._check_9c_completeness(case.get('10C', {})):
            errors.append("Incomplete 10C dimensions")

        # Check 3: Consistency
        consistency_errs = self._check_consistency(case)
        errors.extend(consistency_errs)

        # Check 4: Insight quality
        if not self._check_insight_quality(case.get('insight', '')):
            errors.append("Insight quality too low")

        is_valid = len(errors) == 0
        return is_valid, errors

    def _check_superkey_uniqueness(self, superkey: str) -> bool:
        """Check if superkey is unique"""
        if not superkey:
            return False
        # In production: Check against case-registry
        return True

    def _check_9c_completeness(self, nine_c: Dict) -> bool:
        """Check if all 10C dimensions present"""
        required = ['WHO', 'WHAT', 'HOW', 'WHEN', 'WHERE', 'AWARE', 'READY', 'STAGE', 'HIERARCHY']
        return all(dim in nine_c for dim in required)

    def _check_consistency(self, case: Dict) -> List[str]:
        """Check logical consistency"""
        errors = []
        stage = case.get('10C', {}).get('STAGE', {}).get('phase')
        A_level = case.get('10C', {}).get('AWARE', {}).get('A_level', 0.5)
        W_level = case.get('10C', {}).get('READY', {}).get('W_level', 0.5)

        if stage == 'precontemplation' and A_level > 0.4:
            errors.append("Inconsistency: precontemplation with high awareness")

        if stage == 'action' and W_level < 0.5:
            errors.append("Inconsistency: action phase with low willingness")

        return errors

    def _check_insight_quality(self, insight: str) -> bool:
        """Check insight is reasonable length and not trivial"""
        return 10 < len(insight) < 250

# =============================================================================
# CASE REGISTRY WRITER
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

class ReportGenerator:
    """Generate daily report of case generation"""

    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, generated_cases: List[Tuple[str, Dict]], validation_results: Dict) -> str:
        """Generate markdown report"""
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        report_path = self.output_dir / f"{today}.md"

        # Count metrics
        total_generated = len(generated_cases)
        accepted = sum(1 for _, valid in validation_results.items() if valid)
        rejected = total_generated - accepted
        acceptance_rate = (accepted / total_generated * 100) if total_generated > 0 else 0

        report = f"""# Case Generation Report - {today}

## Summary
- **Total Generated**: {total_generated}
- **Accepted**: {accepted}
- **Rejected**: {rejected}
- **Acceptance Rate**: {acceptance_rate:.1f}%

## Generated Cases
"""

        for case_id, case in generated_cases:
            is_valid = validation_results.get(case_id, False)
            status = "✅ VALID" if is_valid else "❌ REJECTED"
            report += f"\n### {case_id}: {case.get('name')} {status}\n"
            report += f"- Domain: {', '.join(case.get('domain', []))}\n"
            report += f"- Stage: {case.get('10C', {}).get('STAGE', {}).get('phase')}\n"
            report += f"- Insight: {case.get('insight', 'N/A')}\n"

        # Write report
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
    parser = argparse.ArgumentParser(description="Randomized Case Generator")
    parser.add_argument('--max', type=int, default=10, help="Max cases to generate")
    parser.add_argument('--dry-run', action='store_true', help="Preview only, don't commit")
    parser.add_argument('--config', default='data/case-generation-sources.yaml')

    args = parser.parse_args()

    print("=" * 70)
    print("RANDOMIZED CASE GENERATION - LLMMC Pipeline")
    print("=" * 70)

    # 1. Load configuration
    print("\n[1/5] Loading configuration...")
    try:
        config = ConfigLoader(args.config)
        print(f"✅ Config loaded from {args.config}")
    except Exception as e:
        print(f"❌ Config load failed: {e}")
        return 1

    # 2. Sample coordinates
    print(f"\n[2/5] Sampling {args.max} random 10C coordinates...")
    sampler = LLMMCRandomSampler(config)
    sampled_coords = []
    for i in range(args.max):
        coords = sampler.sample()
        if coords:
            sampled_coords.append(coords)
            print(f"  ✅ Sample {i+1}: {coords.domain} / {coords.stage.value} / {coords.hierarchy_level.value}")
        else:
            print(f"  ⚠️ Sample {i+1}: Failed (constraint violation)")

    print(f"Generated: {len(sampled_coords)} valid coordinate sets")

    # 3. Generate cases
    print(f"\n[3/5] Generating cases from coordinates...")
    generator = CaseGenerator(config)
    writer = RegistryWriter('data/case-registry.yaml')
    generated_cases = []

    # Pre-calculate all case IDs to avoid duplicate ID issue
    existing_ids = [int(cid.split('-')[1]) for cid in writer.data.get('cases', {}).keys() if cid.startswith('CASE-')]
    next_id = max(existing_ids, default=0) + 1

    for coords in sampled_coords:
        case_id = f"CASE-{next_id:03d}"
        case = generator.generate_case_from_coordinates(coords, case_id)
        generated_cases.append((case_id, case))
        print(f"  ✅ {case_id}: {case.get('name')}")
        next_id += 1

    # 4. Validate cases
    print(f"\n[4/5] Validating {len(generated_cases)} cases...")
    validator = CaseValidator(config)
    validation_results = {}
    accepted_count = 0

    for case_id, case in generated_cases:
        is_valid, errors = validator.validate(case, case_id)
        validation_results[case_id] = is_valid

        if is_valid:
            print(f"  ✅ {case_id}: Valid")
            accepted_count += 1
            if not args.dry_run:
                writer.add_case(case_id, case)
        else:
            print(f"  ❌ {case_id}: {', '.join(errors)}")

    acceptance_rate = (accepted_count / len(generated_cases) * 100) if generated_cases else 0
    print(f"\nAcceptance Rate: {acceptance_rate:.1f}%")

    # 5. Save and report
    print(f"\n[5/5] Saving and reporting...")
    if not args.dry_run:
        if writer.save():
            print("✅ Case registry updated")
        else:
            print("❌ Failed to save registry")

    report_gen = ReportGenerator('outputs/case-generation-reports')
    report_path = report_gen.generate(generated_cases, validation_results)
    if report_path:
        print(f"✅ Report generated: {report_path}")

    print("\n" + "=" * 70)
    print(f"DONE: {accepted_count}/{len(generated_cases)} cases accepted")
    print("=" * 70)

    return 0

if __name__ == '__main__':
    exit(main())
