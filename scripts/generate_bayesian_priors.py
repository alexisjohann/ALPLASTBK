#!/usr/bin/env python3
"""
Bayesian Prior Generation from Paper Robustness Scores
==============================================================================
Generates Bayesian prior distributions for 10C parameters weighted by
paper robustness scores. High-robustness papers (>85%) provide strong priors,
while low-robustness papers (<70%) are excluded from prior derivation.
==============================================================================
"""

import yaml
import numpy as np
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from scipy import stats
import datetime

# =============================================================================
# DATA STRUCTURES
# =============================================================================

@dataclass
class BayesianPrior:
    """Bayesian prior for a parameter"""
    parameter_name: str
    domain: str
    stage: str

    # Prior distribution (Normal)
    mean: float                    # μ
    std: float                     # σ

    # Credibility
    robustness_weight: float       # 0-1: how much to trust this prior
    contributing_papers: List[str] # Which papers contributed
    n_papers: int                  # How many papers

    # Beta (success rate)
    lower_bound: float
    upper_bound: float

@dataclass
class PriorDistribution:
    """Complete prior distribution for a domain/stage combination"""
    domain: str
    stage: str

    gamma: BayesianPrior           # Complementarity
    A_level: BayesianPrior         # Awareness
    W_level: BayesianPrior         # Willingness
    psi_dominant: Dict[str, float] # Context distribution (categorical)

    avg_robustness: float          # Average robustness of contributing papers
    n_contributing_papers: int     # How many papers contributed

# =============================================================================
# ROBUSTNESS LOADER
# =============================================================================

class RobustnessMetricsLoader:
    """Load robustness scores from validation reports"""

    @staticmethod
    def load_from_papers(paper_sources_path: str = 'data/paper-sources.yaml') -> Dict[str, Dict]:
        """
        Load papers and calculate robustness metrics on the fly
        Returns: {paper_id: {metrics}}
        """
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent))

        from validate_paper_robustness import (
            ClarityAnalyzer, LLMMCUncertaintyQuantifier
        )

        with open(paper_sources_path, 'r') as f:
            data = yaml.safe_load(f)
            papers = data.get('sources', [])

        clarity_analyzer = ClarityAnalyzer()
        results = {}

        for paper in papers:
            paper_id = paper.get('id', 'unknown')
            effect_size = paper.get('key_findings', [{}])[0].get('effect_size', 0.5)
            citations = paper.get('citations', 0)

            # Clarity score
            clarity_level = clarity_analyzer.classify_effect_size(effect_size)
            clarity_score = clarity_analyzer.calculate_clarity_score(effect_size)
            clarity_score *= clarity_analyzer.analyze_citation_count(citations)
            clarity_score = min(100, clarity_score)

            # Uncertainty quantification
            quantifier = LLMMCUncertaintyQuantifier(paper)
            uncertainties = quantifier.quantify()
            confidence = quantifier.confidence_level(uncertainties)

            # Overall robustness
            robustness_score = (clarity_score * 0.4) + (confidence * 0.6)

            # Get 10C coordinates
            coords = paper.get('9c_coordinates', [{}])[0]

            results[paper_id] = {
                'title': paper.get('title'),
                'authors': paper.get('authors', []),
                'year': paper.get('year'),
                'robustness_score': robustness_score,
                'clarity_score': clarity_score,
                'confidence': confidence,
                'effect_size': effect_size,
                'domain': coords.get('domain'),
                'stage': coords.get('stages', [])[0] if coords.get('stages') else None,
                'gamma': coords.get('gamma', 0.5),
                'A_level': coords.get('A_level', 0.5),
                'W_level': coords.get('W_level', 0.5),
                'psi_dominant': coords.get('psi_dominant'),
                'gamma_uncertainty': uncertainties.get('gamma', 0.15),
                'A_uncertainty': uncertainties.get('A_level', 0.20),
                'W_uncertainty': uncertainties.get('W_level', 0.18),
            }

        return results

# =============================================================================
# PRIOR GENERATOR
# =============================================================================

class BayesianPriorGenerator:
    """Generate Bayesian priors from robustness-weighted papers"""

    def __init__(self, metrics: Dict[str, Dict]):
        self.metrics = metrics
        self.high_robustness_threshold = 85
        self.low_robustness_threshold = 70

    def _weight_by_robustness(self, robustness_score: float) -> float:
        """
        Convert robustness score to weight (0-1)
        High robustness = high weight
        Low robustness = excluded (weight ≈ 0)
        """
        if robustness_score > self.high_robustness_threshold:
            return 1.0  # Full weight
        elif robustness_score > self.low_robustness_threshold:
            # Linear interpolation 0.3-1.0 between 70-85%
            return 0.3 + (robustness_score - self.low_robustness_threshold) / (
                self.high_robustness_threshold - self.low_robustness_threshold
            ) * 0.7
        else:
            return 0.0  # Exclude

    def generate_priors_for_domain_stage(self, domain: str, stage: str) -> Optional[PriorDistribution]:
        """
        Generate Bayesian priors for a specific domain/stage combination
        Only includes papers with adequate robustness
        """
        # Find papers matching domain/stage
        matching_papers = []
        for paper_id, metrics in self.metrics.items():
            if (metrics.get('domain') == domain and
                metrics.get('stage') == stage and
                self._weight_by_robustness(metrics['robustness_score']) > 0):

                weight = self._weight_by_robustness(metrics['robustness_score'])
                matching_papers.append((paper_id, metrics, weight))

        if not matching_papers:
            return None

        # Weighted aggregation
        total_weight = sum(w for _, _, w in matching_papers)
        weighted_gamma = sum(m['gamma'] * w for _, m, w in matching_papers) / total_weight
        weighted_A = sum(m['A_level'] * w for _, m, w in matching_papers) / total_weight
        weighted_W = sum(m['W_level'] * w for _, m, w in matching_papers) / total_weight

        # Uncertainty = inverse of average confidence (weighted)
        avg_confidence = sum(m['confidence'] * w for _, m, w in matching_papers) / total_weight
        avg_robustness = sum(m['robustness_score'] * w for _, m, w in matching_papers) / total_weight

        # Standard deviations (lower robustness = higher uncertainty)
        uncertainty_multiplier = 1.0 + (100 - avg_robustness) / 100  # Scale by robustness

        sigma_gamma = np.mean([m['gamma_uncertainty'] for _, m, _ in matching_papers]) * uncertainty_multiplier
        sigma_A = np.mean([m['A_uncertainty'] for _, m, _ in matching_papers]) * uncertainty_multiplier
        sigma_W = np.mean([m['W_uncertainty'] for _, m, _ in matching_papers]) * uncertainty_multiplier

        # Context distribution (categorical)
        psi_counts = {}
        for _, m, w in matching_papers:
            psi = m.get('psi_dominant')
            if psi:
                psi_counts[psi] = psi_counts.get(psi, 0) + w

        psi_dist = {k: v / total_weight for k, v in psi_counts.items()}

        # Create priors
        gamma_prior = BayesianPrior(
            parameter_name='gamma',
            domain=domain,
            stage=stage,
            mean=round(weighted_gamma, 3),
            std=round(sigma_gamma, 3),
            robustness_weight=round(avg_robustness / 100, 2),
            contributing_papers=[p for p, _, _ in matching_papers],
            n_papers=len(matching_papers),
            lower_bound=0.0,
            upper_bound=1.0
        )

        A_prior = BayesianPrior(
            parameter_name='A_level',
            domain=domain,
            stage=stage,
            mean=round(weighted_A, 3),
            std=round(sigma_A, 3),
            robustness_weight=round(avg_robustness / 100, 2),
            contributing_papers=[p for p, _, _ in matching_papers],
            n_papers=len(matching_papers),
            lower_bound=0.0,
            upper_bound=1.0
        )

        W_prior = BayesianPrior(
            parameter_name='W_level',
            domain=domain,
            stage=stage,
            mean=round(weighted_W, 3),
            std=round(sigma_W, 3),
            robustness_weight=round(avg_robustness / 100, 2),
            contributing_papers=[p for p, _, _ in matching_papers],
            n_papers=len(matching_papers),
            lower_bound=0.0,
            upper_bound=1.0
        )

        return PriorDistribution(
            domain=domain,
            stage=stage,
            gamma=gamma_prior,
            A_level=A_prior,
            W_level=W_prior,
            psi_dominant=psi_dist,
            avg_robustness=round(avg_robustness, 1),
            n_contributing_papers=len(matching_papers)
        )

    def generate_all_priors(self) -> Dict[Tuple[str, str], PriorDistribution]:
        """Generate priors for all domain/stage combinations in the data"""
        domains = set()
        stages = set()

        for metrics in self.metrics.values():
            domains.add(metrics['domain'])
            if metrics['stage']:
                stages.add(metrics['stage'])

        priors = {}
        for domain in sorted(domains):
            for stage in sorted(stages):
                prior = self.generate_priors_for_domain_stage(domain, stage)
                if prior:
                    priors[(domain, stage)] = prior

        return priors

# =============================================================================
# REPORT GENERATOR
# =============================================================================

class PriorReportGenerator:
    """Generate reports for Bayesian priors"""

    @staticmethod
    def generate_markdown(priors: Dict[Tuple[str, str], PriorDistribution]) -> str:
        """Generate markdown report"""
        today = datetime.datetime.now().strftime('%Y-%m-%d')

        report = f"""# Bayesian Priors Report - {today}

## Executive Summary

- **Total Domain-Stage Combinations**: {len(priors)}
- **Average Robustness**: {np.mean([p.avg_robustness for p in priors.values()]):.1f}%
- **Parameters Included**: γ (Complementarity), A (Awareness), W (Willingness)

## Priors by Domain-Stage

"""

        for (domain, stage), prior in sorted(priors.items()):
            report += f"\n### {domain.title()} - {stage.title()}\n"
            report += f"**Robustness**: {prior.avg_robustness:.0f}% | **Papers**: {prior.n_contributing_papers}\n\n"

            # Gamma
            report += f"**γ (Complementarity)**\n"
            report += f"- Mean: {prior.gamma.mean:.3f}\n"
            report += f"- σ: {prior.gamma.std:.3f}\n"
            report += f"- 95% CI: [{max(0, prior.gamma.mean - 1.96 * prior.gamma.std):.3f}, {min(1, prior.gamma.mean + 1.96 * prior.gamma.std):.3f}]\n\n"

            # A
            report += f"**A (Awareness)**\n"
            report += f"- Mean: {prior.A_level.mean:.3f}\n"
            report += f"- σ: {prior.A_level.std:.3f}\n"
            report += f"- 95% CI: [{max(0, prior.A_level.mean - 1.96 * prior.A_level.std):.3f}, {min(1, prior.A_level.mean + 1.96 * prior.A_level.std):.3f}]\n\n"

            # W
            report += f"**W (Willingness)**\n"
            report += f"- Mean: {prior.W_level.mean:.3f}\n"
            report += f"- σ: {prior.W_level.std:.3f}\n"
            report += f"- 95% CI: [{max(0, prior.W_level.mean - 1.96 * prior.W_level.std):.3f}, {min(1, prior.W_level.mean + 1.96 * prior.W_level.std):.3f}]\n\n"

            # Psi
            report += f"**Ψ (Context Distribution)**\n"
            for psi, prob in sorted(prior.psi_dominant.items(), key=lambda x: x[1], reverse=True):
                report += f"- {psi}: {prob:.0%}\n"

            report += f"\n**Contributing Papers**: {', '.join(prior.gamma.contributing_papers)}\n"

        return report

    @staticmethod
    def generate_yaml(priors: Dict[Tuple[str, str], PriorDistribution]) -> str:
        """Generate YAML format for use in model training"""
        data = {
            'bayesian_priors': {},
            'metadata': {
                'generated': datetime.datetime.now().isoformat(),
                'total_combinations': len(priors),
            }
        }

        for (domain, stage), prior in priors.items():
            key = f"{domain}:{stage}"
            data['bayesian_priors'][key] = {
                'domain': domain,
                'stage': stage,
                'robustness': prior.avg_robustness,
                'n_papers': prior.n_contributing_papers,
                'gamma': {
                    'mean': prior.gamma.mean,
                    'std': prior.gamma.std,
                    'lower': 0.0,
                    'upper': 1.0
                },
                'A_level': {
                    'mean': prior.A_level.mean,
                    'std': prior.A_level.std,
                    'lower': 0.0,
                    'upper': 1.0
                },
                'W_level': {
                    'mean': prior.W_level.mean,
                    'std': prior.W_level.std,
                    'lower': 0.0,
                    'upper': 1.0
                },
                'psi_dominant': prior.psi_dominant,
                'contributing_papers': prior.gamma.contributing_papers
            }

        return yaml.dump(data, default_flow_style=False, sort_keys=False)

# =============================================================================
# MAIN
# =============================================================================

def main():
    """Generate Bayesian priors"""

    print("=" * 80)
    print("BAYESIAN PRIOR GENERATION FROM ROBUSTNESS SCORES")
    print("=" * 80)
    print()

    # 1. Load robustness metrics
    print("[1/4] Loading robustness metrics from papers...")
    loader = RobustnessMetricsLoader()
    metrics = loader.load_from_papers()
    print(f"✅ Loaded metrics for {len(metrics)} papers")

    # Filter by quality
    high_robustness = {k: v for k, v in metrics.items() if v['robustness_score'] > 85}
    medium_robustness = {k: v for k, v in metrics.items()
                        if 70 < v['robustness_score'] <= 85}
    low_robustness = {k: v for k, v in metrics.items() if v['robustness_score'] <= 70}

    print(f"   ✅ {len(high_robustness)} papers > 85% (full weight)")
    print(f"   ⚠️  {len(medium_robustness)} papers 70-85% (partial weight)")
    print(f"   ❌ {len(low_robustness)} papers < 70% (excluded)")

    # 2. Generate priors
    print("\n[2/4] Generating Bayesian priors...")
    generator = BayesianPriorGenerator(metrics)
    priors = generator.generate_all_priors()
    print(f"✅ Generated {len(priors)} domain-stage prior combinations")

    # 3. Generate reports
    print("\n[3/4] Generating reports...")
    output_dir = Path('outputs/bayesian-priors')
    output_dir.mkdir(parents=True, exist_ok=True)

    # Markdown report
    md_report = PriorReportGenerator.generate_markdown(priors)
    md_path = output_dir / f"{datetime.datetime.now().strftime('%Y-%m-%d')}_priors.md"
    with open(md_path, 'w') as f:
        f.write(md_report)
    print(f"  ✓ Markdown report: {md_path}")

    # YAML report
    yaml_report = PriorReportGenerator.generate_yaml(priors)
    yaml_path = output_dir / 'bayesian_priors.yaml'
    with open(yaml_path, 'w') as f:
        f.write(yaml_report)
    print(f"  ✓ YAML priors: {yaml_path}")

    # 4. Summary
    print("\n[4/4] Summary...")
    print("\n" + "=" * 80)
    print("BAYESIAN PRIOR SUMMARY")
    print("=" * 80)

    # Show top priors
    sorted_priors = sorted(priors.items(),
                          key=lambda x: x[1].avg_robustness, reverse=True)

    print("\n✅ HIGH-ROBUSTNESS PRIORS (>85%):\n")
    for (domain, stage), prior in sorted_priors:
        if prior.avg_robustness > 85:
            print(f"  {domain.title()} / {stage.title()}")
            print(f"    γ ∼ N({prior.gamma.mean:.3f}, {prior.gamma.std:.3f})")
            print(f"    A ∼ N({prior.A_level.mean:.3f}, {prior.A_level.std:.3f})")
            print(f"    W ∼ N({prior.W_level.mean:.3f}, {prior.W_level.std:.3f})")
            print(f"    Papers: {', '.join(prior.gamma.contributing_papers)}")
            print()

    print("=" * 80)
    print(f"✅ Bayesian priors ready for model training")
    print(f"   → Use: outputs/bayesian-priors/bayesian_priors.yaml")
    print("=" * 80)

    return 0

if __name__ == '__main__':
    exit(main())
