#!/usr/bin/env python3
"""
Case Deduplication & Semantic Similarity Detection
==============================================================================
Identifies and flags duplicate/similar cases to prevent redundancy in registry
Uses 10C coordinates + semantic similarity to detect duplicates
==============================================================================
"""

import yaml
import json
import numpy as np
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
import difflib
import datetime

# =============================================================================
# DATA STRUCTURES
# =============================================================================

@dataclass
class CaseSimilarity:
    """Similarity metrics between two cases"""
    case_id_1: str
    case_id_2: str
    coordinate_similarity: float      # 0-1: 10C dimension overlap
    semantic_similarity: float         # 0-1: text similarity
    overall_similarity: float          # 0-1: weighted average
    is_duplicate: bool                 # True if > 85% similar
    explanation: str                   # Why are they similar?

# =============================================================================
# COORDINATE SIMILARITY ANALYZER
# =============================================================================

class CoordinateSimilarityAnalyzer:
    """Analyzes 10C coordinate overlap"""

    @staticmethod
    def calculate_domain_similarity(domain1: str, domain2: str) -> float:
        """Exact domain match"""
        return 1.0 if domain1 == domain2 else 0.0

    @staticmethod
    def calculate_stage_similarity(case1: Dict, case2: Dict) -> float:
        """Check if same BCJ stage"""
        stage1 = case1.get('10C', {}).get('STAGE', {}).get('phase')
        stage2 = case2.get('10C', {}).get('STAGE', {}).get('phase')

        if not stage1 or not stage2:
            return 0.0

        return 1.0 if stage1 == stage2 else 0.5

    @staticmethod
    def calculate_dimension_similarity(case1: Dict, case2: Dict) -> float:
        """Check if same primary dimension"""
        dim1 = case1.get('10C', {}).get('WHAT', {}).get('primary')
        dim2 = case2.get('10C', {}).get('WHAT', {}).get('primary')

        if not dim1 or not dim2:
            return 0.0

        return 1.0 if dim1 == dim2 else 0.5

    @staticmethod
    def calculate_context_similarity(case1: Dict, case2: Dict) -> float:
        """Check if same dominant context (Ψ)"""
        psi1 = case1.get('10C', {}).get('WHEN', {}).get('psi_dominant')
        psi2 = case2.get('10C', {}).get('WHEN', {}).get('psi_dominant')

        if not psi1 or not psi2:
            return 0.0

        return 1.0 if psi1 == psi2 else 0.5

    @staticmethod
    def calculate_parameter_distance(case1: Dict, case2: Dict) -> float:
        """
        Euclidean distance in 10C parameter space
        Returns normalized distance (0-1): 0 = identical, 1 = very different
        """
        params = ['gamma_avg', 'A_level', 'W_level']

        distances = []
        for param_path in [
            ('10C', 'HOW', 'gamma_avg'),
            ('10C', 'AWARE', 'A_level'),
            ('10C', 'READY', 'W_level')
        ]:
            val1 = case1
            val2 = case2

            for key in param_path:
                val1 = val1.get(key, {}) if isinstance(val1, dict) else None
                val2 = val2.get(key, {}) if isinstance(val2, dict) else None

                if val1 is None or val2 is None:
                    break

            if val1 is not None and val2 is not None:
                distances.append(abs(float(val1) - float(val2)))

        if not distances:
            return 0.5  # Default if params missing

        # Normalize distance to 0-1 range (max distance = 1)
        avg_distance = np.mean(distances)
        normalized = min(1.0, avg_distance / 1.0)

        return normalized

    @classmethod
    def analyze(cls, case1: Dict, case2: Dict) -> float:
        """
        Calculate overall coordinate similarity (0-1)
        Higher = more similar
        """
        domain = cls.calculate_domain_similarity(
            case1.get('domain', [''])[0],
            case2.get('domain', [''])[0]
        )

        stage = cls.calculate_stage_similarity(case1, case2)
        dimension = cls.calculate_dimension_similarity(case1, case2)
        context = cls.calculate_context_similarity(case1, case2)

        # Parameter similarity (inverse of distance)
        param_distance = cls.calculate_parameter_distance(case1, case2)
        param_similarity = 1.0 - param_distance

        # Weighted average
        # Domain match is critical (40%), stage/dimension/context (15% each), params (15%)
        similarity = (
            domain * 0.40 +
            stage * 0.15 +
            dimension * 0.15 +
            context * 0.15 +
            param_similarity * 0.15
        )

        return round(similarity, 3)

# =============================================================================
# SEMANTIC SIMILARITY ANALYZER
# =============================================================================

class SemanticSimilarityAnalyzer:
    """Analyzes text similarity using SequenceMatcher"""

    @staticmethod
    def extract_text_features(case: Dict) -> str:
        """Extract all text from a case"""
        texts = []

        # Name and description
        texts.append(case.get('name', '').lower())
        texts.append(case.get('description', '').lower())
        texts.append(case.get('insight', '').lower())
        texts.append(case.get('implication', '').lower())

        # Tags
        for tag in case.get('tags', []):
            texts.append(str(tag).lower())

        return ' '.join(texts)

    @staticmethod
    def calculate_text_similarity(text1: str, text2: str) -> float:
        """Calculate text similarity using SequenceMatcher"""
        matcher = difflib.SequenceMatcher(None, text1, text2)
        return round(matcher.ratio(), 3)

    @classmethod
    def analyze(cls, case1: Dict, case2: Dict) -> float:
        """Calculate semantic similarity (0-1)"""
        text1 = cls.extract_text_features(case1)
        text2 = cls.extract_text_features(case2)

        return cls.calculate_text_similarity(text1, text2)

# =============================================================================
# DEDUPLICATION ENGINE
# =============================================================================

class DeduplicationEngine:
    """Main deduplication system"""

    def __init__(self, registry_path: str = 'data/case-registry.yaml'):
        self.registry_path = registry_path
        self.cases = {}
        self.load_registry()

    def load_registry(self):
        """Load case registry"""
        try:
            with open(self.registry_path, 'r') as f:
                data = yaml.safe_load(f)
                self.cases = data.get('cases', {})
        except Exception as e:
            print(f"Error loading registry: {e}")
            self.cases = {}

    def find_duplicates(self,
                       coordinate_threshold: float = 0.75,
                       semantic_threshold: float = 0.70) -> List[CaseSimilarity]:
        """
        Find potential duplicate cases

        Args:
            coordinate_threshold: Cases > this similarity in 10C space are flagged
            semantic_threshold: Cases > this similarity in text are flagged
        """
        duplicates = []
        case_ids = list(self.cases.keys())

        # Compare all pairs
        for i in range(len(case_ids)):
            for j in range(i + 1, len(case_ids)):
                case_id_1 = case_ids[i]
                case_id_2 = case_ids[j]

                case1 = self.cases[case_id_1]
                case2 = self.cases[case_id_2]

                # Calculate similarities
                coord_sim = CoordinateSimilarityAnalyzer.analyze(case1, case2)
                sem_sim = SemanticSimilarityAnalyzer.analyze(case1, case2)

                # Weighted overall similarity
                overall_sim = (coord_sim * 0.60) + (sem_sim * 0.40)

                # Check thresholds
                is_dup = (overall_sim > 0.85) or \
                        (coord_sim > coordinate_threshold and sem_sim > semantic_threshold)

                if is_dup or overall_sim > 0.70:  # Flag even moderate similarities
                    # Generate explanation
                    explanation = self._generate_explanation(
                        case1, case2, coord_sim, sem_sim
                    )

                    duplicates.append(CaseSimilarity(
                        case_id_1=case_id_1,
                        case_id_2=case_id_2,
                        coordinate_similarity=coord_sim,
                        semantic_similarity=sem_sim,
                        overall_similarity=round(overall_sim, 3),
                        is_duplicate=(overall_sim > 0.85),
                        explanation=explanation
                    ))

        # Sort by similarity (highest first)
        return sorted(duplicates, key=lambda x: x.overall_similarity, reverse=True)

    @staticmethod
    def _generate_explanation(case1: Dict, case2: Dict,
                             coord_sim: float, sem_sim: float) -> str:
        """Generate human-readable explanation"""
        reasons = []

        # Domain/stage match
        domain1 = case1.get('domain', [''])[0]
        domain2 = case2.get('domain', [''])[0]

        if domain1 == domain2:
            stage1 = case1.get('10C', {}).get('STAGE', {}).get('phase', '')
            stage2 = case2.get('10C', {}).get('STAGE', {}).get('phase', '')
            if stage1 == stage2:
                reasons.append(f"Same domain ({domain1}) & stage ({stage1})")

        # Dimension match
        dim1 = case1.get('10C', {}).get('WHAT', {}).get('primary')
        dim2 = case2.get('10C', {}).get('WHAT', {}).get('primary')
        if dim1 == dim2:
            reasons.append(f"Same primary dimension ({dim1})")

        # Context match
        psi1 = case1.get('10C', {}).get('WHEN', {}).get('psi_dominant')
        psi2 = case2.get('10C', {}).get('WHEN', {}).get('psi_dominant')
        if psi1 == psi2:
            reasons.append(f"Same context (Ψ={psi1})")

        # Textual similarity
        if sem_sim > 0.70:
            reasons.append(f"High text similarity ({sem_sim:.0%})")

        if not reasons:
            reasons.append("Similar 10C coordinates")

        return "; ".join(reasons)

    def generate_report(self, duplicates: List[CaseSimilarity]) -> str:
        """Generate deduplication report"""
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        report = f"""# Case Deduplication Report - {today}

## Executive Summary

- **Total Cases Analyzed**: {len(self.cases)}
- **Potential Duplicates Found**: {len([d for d in duplicates if d.is_duplicate])}
- **Similar Cases (70-85%)**: {len([d for d in duplicates if not d.is_duplicate and d.overall_similarity > 0.70])}

## Duplicate Pairs (>85% similarity)

"""

        duplicates_only = [d for d in duplicates if d.is_duplicate]
        if duplicates_only:
            for dup in duplicates_only:
                report += f"\n### {dup.case_id_1} ↔ {dup.case_id_2}\n"
                report += f"- **Overall Similarity**: {dup.overall_similarity:.0%}\n"
                report += f"- **10C Coordinates**: {dup.coordinate_similarity:.0%}\n"
                report += f"- **Text Semantics**: {dup.semantic_similarity:.0%}\n"
                report += f"- **Reason**: {dup.explanation}\n"
                report += f"- **Recommendation**: Merge or delete one case\n"
        else:
            report += "*No true duplicates detected (>85% similarity)*\n"

        # Similar cases section
        report += f"\n## Similar Cases (70-85% similarity)\n"
        similar = [d for d in duplicates if not d.is_duplicate and d.overall_similarity > 0.70]

        if similar:
            for sim in similar[:10]:  # Show top 10
                report += f"\n### {sim.case_id_1} ~ {sim.case_id_2} ({sim.overall_similarity:.0%})\n"
                report += f"- {sim.explanation}\n"
        else:
            report += "*No similar cases detected*\n"

        return report

# =============================================================================
# MAIN
# =============================================================================

def main():
    """Run deduplication analysis"""

    print("=" * 80)
    print("CASE DEDUPLICATION & SIMILARITY DETECTION")
    print("=" * 80)
    print()

    # 1. Load registry
    print("[1/3] Loading case registry...")
    engine = DeduplicationEngine()
    print(f"✅ Loaded {len(engine.cases)} cases")

    # 2. Find duplicates
    print("\n[2/3] Analyzing for duplicates and similar cases...")
    duplicates = engine.find_duplicates(
        coordinate_threshold=0.75,
        semantic_threshold=0.70
    )
    print(f"✅ Found {len(duplicates)} similar pair(s)")

    # 3. Generate report
    print("\n[3/3] Generating report...")
    report = engine.generate_report(duplicates)

    # Save report
    output_dir = Path('outputs/deduplication-reports')
    output_dir.mkdir(parents=True, exist_ok=True)

    report_path = output_dir / f"{datetime.datetime.now().strftime('%Y-%m-%d')}_deduplication.md"
    with open(report_path, 'w') as f:
        f.write(report)

    print(f"✅ Report saved: {report_path}")

    # Summary
    print("\n" + "=" * 80)
    print("DEDUPLICATION SUMMARY")
    print("=" * 80)

    true_dups = [d for d in duplicates if d.is_duplicate]
    similar_only = [d for d in duplicates if not d.is_duplicate and d.overall_similarity > 0.70]

    print(f"✅ True Duplicates (>85%): {len(true_dups)}")
    for dup in true_dups[:5]:
        print(f"   - {dup.case_id_1} ↔ {dup.case_id_2} ({dup.overall_similarity:.0%})")

    print(f"\n⚠️  Similar Cases (70-85%): {len(similar_only)}")
    for sim in similar_only[:5]:
        print(f"   - {sim.case_id_1} ~ {sim.case_id_2} ({sim.overall_similarity:.0%})")

    print(f"\n✅ Registry Health: {100 * (1 - len(true_dups) / len(engine.cases)):.1f}% unique")

    print("\n" + "=" * 80)
    return 0

if __name__ == '__main__':
    exit(main())
