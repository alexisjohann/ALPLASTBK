#!/usr/bin/env python3
# ┌─────────────────────────────────────────────────────────────────────────┐
# │  ⚠️  DEPRECATED (2026-02-08)                                            │
# │                                                                         │
# │  Paper Robustness Validation (uses old paper-sources.yaml format)      │
# │  Kept for reference only.                                              │
# │                                                                         │
# │  SSOT: data/paper-references/PAP-*.yaml + bibliography/bcm_master.bib │
# │  Neue Papers: /integrate-paper Workflow                                │
# └─────────────────────────────────────────────────────────────────────────┘
"""
Paper Robustness Validation System
==============================================================================
Validates robustness of behavioral economics papers using:
1. Effect Size Clarity scoring
2. LLMMC-based parameter uncertainty quantification
3. Cross-paper consistency analysis
==============================================================================
"""

import yaml
import json
import numpy as np
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from enum import Enum
import datetime

# =============================================================================
# DATA STRUCTURES
# =============================================================================

class ClarityLevel(Enum):
    """Effect size clarity classification"""
    CLEAR = "🟢 Clear"      # Effect size > 1.0
    AMBIGUOUS = "🟡 Ambiguous"  # 0.5 < Effect size < 1.0
    WEAK = "🔴 Weak"        # Effect size < 0.5

@dataclass
class PaperMetrics:
    """Robustness metrics for a paper"""
    paper_id: str
    title: str
    year: int
    citations: int
    authors: List[str]

    # Clarity metrics
    effect_size: float
    clarity_level: ClarityLevel
    clarity_score: float  # 0-100

    # LLMMC metrics
    parameter_uncertainty: Dict[str, float]  # sigma for each param
    confidence_level: float  # 0-100 (95% CI coverage)
    robustness_score: float  # Combined score

    # Domain metrics
    domain: str
    stage: str
    gamma: float
    A_level: float
    W_level: float
    psi_dominant: str

    # Recommendation
    recommendation: str
    needs_replication: bool

# =============================================================================
# CLARITY ANALYSIS
# =============================================================================

class ClarityAnalyzer:
    """Analyzes effect size clarity"""

    @staticmethod
    def classify_effect_size(effect_size: float) -> ClarityLevel:
        """Classify effect size into clarity levels"""
        if effect_size > 1.0:
            return ClarityLevel.CLEAR
        elif effect_size > 0.5:
            return ClarityLevel.AMBIGUOUS
        else:
            return ClarityLevel.WEAK

    @staticmethod
    def calculate_clarity_score(effect_size: float) -> float:
        """
        Calculate clarity score 0-100
        Based on effect size strength
        """
        # Normalize effect size to 0-100 scale
        # Effect size of 2.0 = 100% clear
        clarity = min(100, (effect_size / 2.0) * 100)
        return clarity

    @staticmethod
    def analyze_citation_count(citations: int) -> float:
        """Adjust clarity score based on citation count (community validation)"""
        # More citations = more peer validation
        # 1000+ citations = max boost (+10%)
        if citations > 5000:
            return 1.10
        elif citations > 2000:
            return 1.05
        elif citations > 1000:
            return 1.03
        else:
            return 1.0

# =============================================================================
# LLMMC UNCERTAINTY QUANTIFICATION
# =============================================================================

class LLMMCUncertaintyQuantifier:
    """
    Estimates parameter uncertainty using LLMMC principles
    Without access to actual data, we infer uncertainty from:
    - Effect size (larger effects = lower uncertainty)
    - Study design (published, citations = lower uncertainty)
    - Parameter type (some are inherently more uncertain)
    """

    def __init__(self, paper: Dict):
        self.paper = paper
        self.effect_size = self._get_effect_size()
        self.citations = paper.get('citations', 500)
        self.status = paper.get('status', 'published')

    def _get_effect_size(self) -> float:
        """Extract primary effect size"""
        findings = self.paper.get('key_findings', [])
        if findings:
            return findings[0].get('effect_size', 0.5)
        return 0.5

    def _base_uncertainty(self, param_name: str) -> float:
        """Base uncertainty by parameter type (0-1 scale)"""
        # Some parameters are inherently more uncertain
        uncertainties = {
            'gamma': 0.15,          # Complementarity is somewhat uncertain
            'A_level': 0.20,        # Awareness is hard to measure precisely
            'W_level': 0.18,        # Willingness is context-dependent
            'psi_dominant': 0.25,   # Context classification has ambiguity
        }
        return uncertainties.get(param_name, 0.15)

    def _effect_size_adjustment(self) -> float:
        """Larger effects = lower uncertainty"""
        # Effect size 2.0+ reduces uncertainty by 30%
        # Effect size 0.5 increases uncertainty by 30%
        if self.effect_size > 1.5:
            return 0.70  # 30% reduction
        elif self.effect_size > 1.0:
            return 0.85  # 15% reduction
        elif self.effect_size > 0.5:
            return 1.0   # No change
        else:
            return 1.30  # 30% increase

    def _publication_adjustment(self) -> float:
        """Published, cited papers have lower uncertainty"""
        if self.status == 'seminal':
            return 0.60  # 40% reduction for seminal papers
        elif self.citations > 5000:
            return 0.70  # 30% reduction for highly cited
        elif self.citations > 2000:
            return 0.85  # 15% reduction
        else:
            return 1.0   # No change

    def quantify(self) -> Dict[str, float]:
        """Estimate uncertainty for each parameter"""
        effect_adj = self._effect_size_adjustment()
        pub_adj = self._publication_adjustment()

        params = ['gamma', 'A_level', 'W_level', 'psi_dominant']
        uncertainties = {}

        for param in params:
            base = self._base_uncertainty(param)
            sigma = base * effect_adj * pub_adj
            uncertainties[param] = round(sigma, 3)

        return uncertainties

    def confidence_level(self, uncertainties: Dict[str, float]) -> float:
        """
        Calculate overall confidence level (0-100)
        Based on parameter uncertainties
        Higher uncertainty = lower confidence
        """
        # Average uncertainty across parameters
        avg_uncertainty = np.mean(list(uncertainties.values()))

        # Convert to confidence: uncertainty 0.1 = 90% confidence
        confidence = (1 - avg_uncertainty) * 100

        # Boost by citation count
        citation_boost = min(10, self.citations / 500)
        confidence = min(100, confidence + citation_boost)

        return round(confidence, 1)

# =============================================================================
# CROSS-PAPER CONSISTENCY ANALYSIS
# =============================================================================

class CrossPaperAnalyzer:
    """Analyzes consistency across papers"""

    def __init__(self, papers: List[Dict]):
        self.papers = papers

    def find_related_papers(self, target_paper: Dict) -> List[Tuple[str, float]]:
        """
        Find papers with similar domain/stage/dimensions
        Returns list of (paper_id, similarity_score)
        """
        target_domain = target_paper.get('9c_coordinates', [{}])[0].get('domain')
        target_stages = target_paper.get('9c_coordinates', [{}])[0].get('stages', [])

        related = []

        for paper in self.papers:
            if paper.get('id') == target_paper.get('id'):
                continue

            coords = paper.get('9c_coordinates', [{}])[0]
            paper_domain = coords.get('domain')
            paper_stages = coords.get('stages', [])

            # Calculate similarity
            domain_match = 1.0 if paper_domain == target_domain else 0.0
            stage_overlap = len(set(target_stages) & set(paper_stages)) / max(len(target_stages), len(paper_stages))

            similarity = (domain_match * 0.6 + stage_overlap * 0.4)

            if similarity > 0.4:  # Only include reasonably similar papers
                related.append((paper.get('id'), round(similarity, 2)))

        return sorted(related, key=lambda x: x[1], reverse=True)

    def check_consistency(self, paper_id: str, related_papers: List[Tuple[str, float]]) -> Tuple[bool, str]:
        """
        Check if paper findings are consistent with related papers
        Returns (is_consistent, explanation)
        """
        if len(related_papers) == 0:
            return True, "No related papers for comparison"

        # Find the papers
        target = next((p for p in self.papers if p.get('id') == paper_id), None)
        related = [next((p for p in self.papers if p.get('id') == rid), None) for rid, _ in related_papers[:2]]
        related = [p for p in related if p is not None]

        if not related:
            return True, "Could not load related papers"

        # Compare findings direction (all positive effects?)
        target_effect = target.get('key_findings', [{}])[0].get('effect_size', 0)
        related_effects = [p.get('key_findings', [{}])[0].get('effect_size', 0) for p in related]

        # Check consistency
        target_positive = target_effect > 0
        related_positive = [e > 0 for e in related_effects]

        consistency_ratio = sum(1 for rp in related_positive if rp == target_positive) / len(related_positive)

        if consistency_ratio >= 0.66:
            return True, f"Consistent with {int(consistency_ratio*100)}% of related papers"
        else:
            return False, f"Mixed/inconsistent results with related papers ({int(consistency_ratio*100)}% alignment)"

# =============================================================================
# ROBUSTNESS REPORT GENERATOR
# =============================================================================

class RobustnessReportGenerator:
    """Generates validation reports"""

    def __init__(self, output_dir: str = 'outputs/paper-robustness-reports'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, metrics_list: List[PaperMetrics]) -> str:
        """Generate markdown report"""
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        report_path = self.output_dir / f"{today}_robustness.md"

        # Sort by robustness score descending
        sorted_metrics = sorted(metrics_list, key=lambda m: m.robustness_score, reverse=True)

        # Build report
        report = f"""# Paper Robustness Validation Report - {today}

## Executive Summary

- **Papers Analyzed**: {len(metrics_list)}
- **Average Robustness Score**: {np.mean([m.robustness_score for m in metrics_list]):.1f}%
- **Papers Flagged for Replication**: {sum(1 for m in metrics_list if m.needs_replication)}
- **Highly Robust Papers (>85%)**: {sum(1 for m in metrics_list if m.robustness_score > 85)}

## Robustness Rankings

"""

        for i, metric in enumerate(sorted_metrics, 1):
            status = "✅ Robust" if metric.robustness_score > 85 else ("⚠️ Caution" if metric.robustness_score > 70 else "❌ Questionable")
            report += f"\n### {i}. {metric.paper_id} {status}\n"
            report += f"- **Title**: {metric.title}\n"
            report += f"- **Authors**: {', '.join(metric.authors)}\n"
            report += f"- **Year**: {metric.year} | **Citations**: {metric.citations}\n"
            report += f"- **Effect Size**: {metric.effect_size} {metric.clarity_level.value}\n"
            report += f"- **Clarity Score**: {metric.clarity_score:.0f}%\n"
            report += f"- **Confidence Level**: {metric.confidence_level:.1f}%\n"
            report += f"- **Robustness Score**: {metric.robustness_score:.1f}%\n"
            report += f"- **Domain**: {metric.domain} | **Stage**: {metric.stage}\n"
            report += f"- **Recommendation**: {metric.recommendation}\n"
            report += f"- **Parameter Uncertainties**:\n"
            for param, uncertainty in metric.parameter_uncertainty.items():
                report += f"  - {param}: ±{uncertainty:.1%}\n"

        # Write report
        try:
            with open(report_path, 'w') as f:
                f.write(report)
            return str(report_path)
        except Exception as e:
            print(f"Error writing report: {e}")
            return ""

    def generate_matrix(self, metrics_list: List[PaperMetrics]) -> str:
        """Generate comparison matrix"""
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        matrix_path = self.output_dir / f"{today}_robustness_matrix.csv"

        try:
            with open(matrix_path, 'w') as f:
                # Header
                f.write("Paper ID,Title,Year,Citations,Effect Size,Clarity,Confidence,Robustness,Recommendation\n")

                for metric in sorted(metrics_list, key=lambda m: m.robustness_score, reverse=True):
                    f.write(f"\"{metric.paper_id}\",\"{metric.title}\",{metric.year},{metric.citations},"
                           f"{metric.effect_size:.2f},{metric.clarity_score:.0f},{metric.confidence_level:.1f},"
                           f"{metric.robustness_score:.1f},\"{metric.recommendation}\"\n")

            return str(matrix_path)
        except Exception as e:
            print(f"Error writing matrix: {e}")
            return ""

# =============================================================================
# MAIN VALIDATION PIPELINE
# =============================================================================

def main():
    """Run paper robustness validation"""

    print("=" * 80)
    print("PAPER ROBUSTNESS VALIDATION SYSTEM")
    print("=" * 80)
    print()

    # 1. Load papers
    print("[1/5] Loading papers...")
    try:
        with open('data/paper-sources.yaml', 'r') as f:
            data = yaml.safe_load(f)
            papers = data.get('sources', [])
        print(f"✅ Loaded {len(papers)} papers")
    except Exception as e:
        print(f"❌ Error loading papers: {e}")
        return 1

    clarity_analyzer = ClarityAnalyzer()
    cross_analyzer = CrossPaperAnalyzer(papers)
    metrics_list = []

    # 2. Analyze clarity
    print("\n[2/5] Analyzing effect size clarity...")

    for paper in papers:
        paper_id = paper.get('id', 'unknown')
        title = paper.get('title', '')
        year = paper.get('year', 0)
        citations = paper.get('citations', 0)
        authors = paper.get('authors', [])

        # Get effect size
        effect_size = paper.get('key_findings', [{}])[0].get('effect_size', 0.5)

        # Analyze clarity
        clarity_level = clarity_analyzer.classify_effect_size(effect_size)
        clarity_score = clarity_analyzer.calculate_clarity_score(effect_size)
        clarity_score *= clarity_analyzer.analyze_citation_count(citations)
        clarity_score = min(100, clarity_score)

        # Get 10C coordinates
        coords = paper.get('9c_coordinates', [{}])[0]
        domain = coords.get('domain', 'unknown')
        stages = coords.get('stages', [])
        stage = stages[0] if stages else 'unknown'
        gamma = coords.get('gamma', 0.5)
        A_level = coords.get('A_level', 0.5)
        W_level = coords.get('W_level', 0.5)
        psi_dominant = coords.get('psi_dominant', 'unknown')

        print(f"  ✓ {paper_id}: {clarity_level.value} (effect={effect_size}, clarity={clarity_score:.0f}%)")

    # 3. Quantify uncertainty
    print("\n[3/5] Quantifying parameter uncertainty (LLMMC)...")

    for paper in papers:
        paper_id = paper.get('id', 'unknown')

        # Quantify uncertainty
        quantifier = LLMMCUncertaintyQuantifier(paper)
        uncertainties = quantifier.quantify()
        confidence = quantifier.confidence_level(uncertainties)

        print(f"  ✓ {paper_id}: confidence={confidence:.1f}% (γ±{uncertainties['gamma']:.1%}, A±{uncertainties['A_level']:.1%})")

    # 4. Check cross-paper consistency
    print("\n[4/5] Analyzing cross-paper consistency...")

    for paper in papers:
        paper_id = paper.get('id', 'unknown')
        related = cross_analyzer.find_related_papers(paper)
        consistent, explanation = cross_analyzer.check_consistency(paper_id, related)

        status = "✓" if consistent else "⚠"
        print(f"  {status} {paper_id}: {explanation}")

    # 5. Compile metrics and generate reports
    print("\n[5/5] Compiling metrics and generating reports...")

    for paper in papers:
        paper_id = paper.get('id', 'unknown')
        title = paper.get('title', '')
        year = paper.get('year', 0)
        citations = paper.get('citations', 0)
        authors = paper.get('authors', [])
        effect_size = paper.get('key_findings', [{}])[0].get('effect_size', 0.5)

        coords = paper.get('9c_coordinates', [{}])[0]
        domain = coords.get('domain', 'unknown')
        stages = coords.get('stages', [])
        stage = stages[0] if stages else 'unknown'
        gamma = coords.get('gamma', 0.5)
        A_level = coords.get('A_level', 0.5)
        W_level = coords.get('W_level', 0.5)
        psi_dominant = coords.get('psi_dominant', 'unknown')

        # Calculate metrics
        clarity_level = clarity_analyzer.classify_effect_size(effect_size)
        clarity_score = clarity_analyzer.calculate_clarity_score(effect_size)
        clarity_score *= clarity_analyzer.analyze_citation_count(citations)
        clarity_score = min(100, clarity_score)

        quantifier = LLMMCUncertaintyQuantifier(paper)
        uncertainties = quantifier.quantify()
        confidence = quantifier.confidence_level(uncertainties)

        # Calculate robustness score (weighted combination)
        robustness_score = (clarity_score * 0.4) + (confidence * 0.6)

        # Determine recommendation
        if robustness_score > 85:
            recommendation = "✅ Use as-is for model training"
            needs_replication = False
        elif robustness_score > 70:
            recommendation = "⚠️ Use with caution; verify key parameters"
            needs_replication = True
        else:
            recommendation = "❌ Insufficient robustness; recommend replication before use"
            needs_replication = True

        metrics = PaperMetrics(
            paper_id=paper_id,
            title=title,
            year=year,
            citations=citations,
            authors=authors,
            effect_size=effect_size,
            clarity_level=clarity_level,
            clarity_score=clarity_score,
            parameter_uncertainty=uncertainties,
            confidence_level=confidence,
            robustness_score=robustness_score,
            domain=domain,
            stage=stage,
            gamma=gamma,
            A_level=A_level,
            W_level=W_level,
            psi_dominant=psi_dominant,
            recommendation=recommendation,
            needs_replication=needs_replication
        )

        metrics_list.append(metrics)

    # Generate reports
    report_gen = RobustnessReportGenerator()
    report_path = report_gen.generate(metrics_list)
    matrix_path = report_gen.generate_matrix(metrics_list)

    if report_path:
        print(f"  ✓ Report generated: {report_path}")
    if matrix_path:
        print(f"  ✓ Matrix generated: {matrix_path}")

    # Print summary
    print("\n" + "=" * 80)
    print("ROBUSTNESS VALIDATION SUMMARY")
    print("=" * 80)

    sorted_metrics = sorted(metrics_list, key=lambda m: m.robustness_score, reverse=True)
    for i, m in enumerate(sorted_metrics[:3], 1):
        status = "✅" if m.robustness_score > 85 else "⚠️"
        print(f"{i}. {m.paper_id}: {m.robustness_score:.0f}% {status}")

    print(f"\n📊 Overall Statistics:")
    print(f"   Average Robustness: {np.mean([m.robustness_score for m in metrics_list]):.1f}%")
    print(f"   Highly Robust (>85%): {sum(1 for m in metrics_list if m.robustness_score > 85)}/{len(metrics_list)}")
    print(f"   Need Replication: {sum(1 for m in metrics_list if m.needs_replication)}/{len(metrics_list)}")

    print("\n" + "=" * 80)
    print("✅ Robustness validation complete")
    print("=" * 80)

    return 0

if __name__ == '__main__':
    exit(main())
