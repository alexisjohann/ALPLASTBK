#!/usr/bin/env python3
# =============================================================================
# ARCHETYPE DISCOVERY: Learning Recurring Patterns Across Projects
# =============================================================================
#
# Purpose: Discover and formalize new strategic archetypes from observed outcomes
#
# Key Insight:
#   After 3+ strategic planning projects, patterns emerge in:
#     (Ψ, WHAT, HOW, WHERE) → Predicted outcomes vs Actual outcomes
#
#   When we observe that projects with similar (Ψ, γ, FEPSDE weights) have
#   similar characteristics, we create a NEW ARCHETYPE in FFF registry.
#
# Example Archetype Discovery:
#
#   OBSERVED PATTERN: "Tech Companies in APAC"
#     Companies: TechCo1, TechCo2, TechCo3
#     Shared characteristics:
#       - Ψ₇ (Technological) = 0.9 (high)
#       - Ψ₁ (Economic) = 0.8 (high growth market)
#       - WHAT: ω_D=0.4, ω_X=0.3 (Innovation + Purpose focused)
#       - HOW: γ_avg = 0.72 (high synergy potential)
#
#     Observed outcomes:
#       - CAGR higher: 7.2% vs 6.0% (sector baseline)
#       - Headcount elasticity tighter: 0.75 vs 0.65
#       - Capex intensity higher: 4.2% vs 3.5% (R&D investment)
#       - ROI better: 2.1x vs 1.8x (complementarity pays off)
#
#   ARCHIVED ARCHETYPE: FFF-TECH-APAC
#     → Used to seed parameters for NEW tech companies in APAC
#     → Faster convergence (starts with better priors)
#     → More accurate confidence intervals
#
# Single Source of Truth:
#   - /data/intervention-registry.yaml (project outcomes)
#   - /data/models/registry/model_registry.yaml (parameter metadata)
#   - /data/case-registry.yaml (10C-indexed cases)
#
# Version: 1.0
# Date: 2026-01-16
# Status: DRAFT

import yaml
import json
from pathlib import Path
from typing import Dict, List, Tuple, Set
from datetime import datetime
from dataclasses import dataclass
import statistics


@dataclass
class Archetype:
    """Represents a discovered archetype."""
    name: str
    code: str  # e.g., "FFF-TECH-APAC"
    companies: List[str]
    characteristics: Dict
    observed_parameters: Dict
    recommendations: Dict
    confidence: float  # 0-1, based on sample size
    last_updated: str


class ArchetypeDiscovery:
    """
    Discovers and formalizes strategic archetypes from observed outcomes.

    Workflow:
    1. Load all projects with measurements (intervention-registry.yaml)
    2. Extract (Ψ, WHAT, HOW, WHERE) context for each
    3. Calculate similarity between projects
    4. Cluster similar projects
    5. Formalize cluster as ARCHETYPE
    6. Generate recommendations based on cluster
    7. Save to archetype registry
    """

    def __init__(self):
        self.data_dir = Path(__file__).parent.parent.parent / "data"
        self.intervention_registry_file = self.data_dir / "intervention-registry.yaml"
        self.case_registry_file = self.data_dir / "case-registry.yaml"
        self.archetype_registry_file = self.data_dir / "archetype-registry.yaml"

    def load_completed_projects(self) -> List[Dict]:
        """Load projects with completed measurements (not just predictions)."""

        if not self.intervention_registry_file.exists():
            return []

        with open(self.intervention_registry_file) as f:
            registry = yaml.safe_load(f)

        # Filter for projects with "execution_complete" status
        completed = []
        for project_key, project_data in registry.get("projects", {}).items():
            if project_data.get("status") == "COMPLETED":
                completed.append({
                    "key": project_key,
                    "data": project_data
                })

        return completed

    def extract_context_vector(self, project: Dict) -> Dict:
        """
        Extract (Ψ, WHAT, HOW, WHERE) context from a completed project.

        Returns a normalized vector for similarity comparison.
        """

        data = project["data"]

        context = {
            "company": data.get("company_name", ""),

            # WHEN: Context dimensions (Ψ)
            "psi_economic": data.get("context", {}).get("psi_1_economic", 0.5),
            "psi_technological": data.get("context", {}).get("psi_7_technological", 0.5),
            "psi_institutional": data.get("context", {}).get("psi_5_institutional", 0.5),
            "psi_environmental": data.get("context", {}).get("psi_8_environmental", 0.5),
            "psi_cultural": data.get("context", {}).get("psi_6_cultural", 0.5),

            # WHAT: Utility dimension weights
            "weight_f_financial": data.get("strategy", {}).get("dimension_weights", {}).get("F", 0.5),
            "weight_d_development": data.get("strategy", {}).get("dimension_weights", {}).get("D", 0.5),
            "weight_s_social": data.get("strategy", {}).get("dimension_weights", {}).get("S", 0.5),
            "weight_x_existential": data.get("strategy", {}).get("dimension_weights", {}).get("X", 0.5),

            # HOW: Complementarity
            "gamma_avg": data.get("strategy", {}).get("complementarity_avg", 0.6),

            # WHERE: Parameter characteristics
            "revenue_size_eur_m": data.get("execution_results", {}).get("actual_revenue_eur_m", 0),
            "headcount_size": data.get("execution_results", {}).get("actual_headcount", 0),

            # Outcome metrics
            "revenue_mape": data.get("execution_results", {}).get("revenue_mape", 0),
            "headcount_elasticity_observed": data.get("execution_results", {}).get("headcount_elasticity", 0),
            "cagr_observed": data.get("execution_results", {}).get("cagr_observed", 0),
        }

        return context

    def calculate_similarity(self, ctx1: Dict, ctx2: Dict) -> float:
        """
        Calculate similarity between two context vectors.

        Uses normalized Euclidean distance in context space.
        Returns: 0-1 (1 = identical, 0 = completely different)
        """

        # Relevant dimensions for clustering
        dimensions = [
            "psi_economic",
            "psi_technological",
            "weight_f_financial",
            "weight_d_development",
            "gamma_avg",
        ]

        # Normalize and calculate
        sum_squared_diff = 0
        for dim in dimensions:
            v1 = ctx1.get(dim, 0.5)
            v2 = ctx2.get(dim, 0.5)
            diff = (v1 - v2) / max(abs(v1), abs(v2), 1)  # Normalized difference
            sum_squared_diff += diff ** 2

        euclidean_dist = (sum_squared_diff) ** 0.5
        # Convert distance to similarity (0-1)
        similarity = 1 / (1 + euclidean_dist)

        return min(1.0, max(0.0, similarity))

    def cluster_projects(self, projects: List[Dict], similarity_threshold: float = 0.75) -> List[List[Dict]]:
        """
        Cluster similar projects using hierarchical clustering.

        Args:
            projects: List of completed projects
            similarity_threshold: Minimum similarity to form a cluster (0-1)

        Returns:
            List of clusters (each cluster is a list of projects)
        """

        if not projects:
            return []

        # Extract context vectors
        contexts = [self.extract_context_vector(p) for p in projects]

        clusters = []
        used_indices = set()

        # Greedy clustering: start with first unused project
        for i, ctx_i in enumerate(contexts):
            if i in used_indices:
                continue

            # Start new cluster
            cluster = [projects[i]]
            used_indices.add(i)

            # Add similar projects to cluster
            for j, ctx_j in enumerate(contexts):
                if j in used_indices:
                    continue

                similarity = self.calculate_similarity(ctx_i, ctx_j)
                if similarity >= similarity_threshold:
                    cluster.append(projects[j])
                    used_indices.add(j)

            # Keep cluster if size >= 2
            if len(cluster) >= 2:
                clusters.append(cluster)

        return clusters

    def formalize_archetype(self, cluster: List[Dict]) -> Archetype:
        """
        Convert a cluster into a formal archetype.

        Extracts:
        - Common characteristics (Ψ, WHAT, HOW)
        - Observed outcomes (CAGR, elasticity, ROI)
        - Recommendations for new projects with same profile
        """

        contexts = [self.extract_context_vector(p) for p in cluster]
        companies = [ctx["company"] for ctx in contexts]

        # Calculate cluster centroid
        centroid = {}
        for key in contexts[0].keys():
            values = [ctx.get(key, 0) for ctx in contexts]
            if all(isinstance(v, (int, float)) for v in values):
                centroid[key] = statistics.mean(values)

        # Extract characteristics
        characteristics = {
            "industry_cluster": self._infer_industry(companies),
            "geographic_pattern": self._infer_geography(companies),
            "context_profile": {
                "psi_economic": f"{centroid['psi_economic']:.2f}",
                "psi_technological": f"{centroid['psi_technological']:.2f}",
                "psi_institutional": f"{centroid.get('psi_institutional', 0.5):.2f}",
            },
            "strategy_profile": {
                "financial_focus": f"{centroid['weight_f_financial']:.2f}",
                "development_focus": f"{centroid['weight_d_development']:.2f}",
                "social_focus": f"{centroid['weight_s_social']:.2f}",
                "existential_focus": f"{centroid['weight_x_existential']:.2f}",
            },
            "complementarity_level": f"{centroid['gamma_avg']:.2f}",
        }

        # Observed outcomes (average across cluster)
        observed_parameters = {
            "cagr_observed": f"{statistics.mean([ctx['cagr_observed'] for ctx in contexts if ctx['cagr_observed'] > 0]):.1%}",
            "headcount_elasticity": f"{statistics.mean([ctx['headcount_elasticity_observed'] for ctx in contexts if ctx['headcount_elasticity_observed'] > 0]):.2f}",
            "revenue_forecast_accuracy": f"{(1 - statistics.mean([ctx['revenue_mape'] for ctx in contexts])):.1%}",
        }

        # Generate recommendations
        recommendations = self._generate_recommendations(
            centroid, observed_parameters, len(cluster)
        )

        # Generate archetype code
        code = self._generate_archetype_code(characteristics, companies)

        archetype = Archetype(
            name=f"{code} Archetype ({len(cluster)} companies)",
            code=code,
            companies=companies,
            characteristics=characteristics,
            observed_parameters=observed_parameters,
            recommendations=recommendations,
            confidence=min(0.99, 0.6 + len(cluster) * 0.1),  # Confidence = f(sample size)
            last_updated=datetime.now().isoformat()
        )

        return archetype

    def _infer_industry(self, companies: List[str]) -> str:
        """Infer industry from company names (simple heuristic)."""
        # This would integrate with company metadata in practice
        return "MIXED"  # Default

    def _infer_geography(self, companies: List[str]) -> str:
        """Infer geography from company names (simple heuristic)."""
        return "GLOBAL"  # Default

    def _generate_archetype_code(self, characteristics: Dict, companies: List[str]) -> str:
        """Generate unique archetype code."""
        # Format: FFF-DESCRIPTOR-DESCRIPTOR
        # Example: FFF-TECH-APAC, FFF-MANU-SCALE
        return f"FFF-{len(companies)}-CLUSTER"  # Placeholder

    def _generate_recommendations(self, centroid: Dict, outcomes: Dict, cluster_size: int) -> Dict:
        """Generate recommendations for new projects with this archetype."""

        psi_tech = centroid.get("psi_technological", 0.5)
        weight_d = centroid.get("weight_d_development", 0.5)
        gamma = centroid.get("gamma_avg", 0.6)

        recommendations = {
            "parameter_seeding": {
                "recommended_cagr": outcomes.get("cagr_observed", "TBD"),
                "recommended_headcount_elasticity": outcomes.get("headcount_elasticity", "0.65"),
                "confidence_boost": f"E(θ) shrinks ±20% faster (n_prior = {cluster_size})"
            },
            "execution_strategy": [],
            "risk_mitigation": []
        }

        # Context-specific recommendations
        if psi_tech > 0.7:
            recommendations["execution_strategy"].append(
                "HIGH TECH INTENSITY: Allocate 5%+ capex to digital transformation"
            )

        if weight_d > 0.35:
            recommendations["execution_strategy"].append(
                "INNOVATION FOCUS: Invest heavily in R&D pipeline and talent development"
            )

        if gamma > 0.70:
            recommendations["execution_strategy"].append(
                "SYNERGY POTENTIAL: Coordinate across revenue/headcount/capex (high γ)"
            )

        return recommendations

    def save_archetypes(self, archetypes: List[Archetype]) -> str:
        """Save discovered archetypes to archetype registry."""

        # Load existing registry
        if self.archetype_registry_file.exists():
            with open(self.archetype_registry_file) as f:
                registry = yaml.safe_load(f)
        else:
            registry = {"archetypes": {}}

        # Add new archetypes
        for arch in archetypes:
            registry["archetypes"][arch.code] = {
                "name": arch.name,
                "companies": arch.companies,
                "characteristics": arch.characteristics,
                "observed_parameters": arch.observed_parameters,
                "recommendations": arch.recommendations,
                "confidence": arch.confidence,
                "created_date": arch.last_updated,
                "sample_size": len(arch.companies),
            }

        # Save registry
        self.archetype_registry_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.archetype_registry_file, "w") as f:
            yaml.dump(registry, f, default_flow_style=False, sort_keys=False)

        return str(self.archetype_registry_file)

    def generate_discovery_report(self, archetypes: List[Archetype]) -> Dict:
        """Generate human-readable discovery report."""

        report = {
            "timestamp": datetime.now().isoformat(),
            "archetypes_discovered": len(archetypes),
            "total_companies_clustered": sum(len(a.companies) for a in archetypes),
            "archetypes": [
                {
                    "code": a.code,
                    "name": a.name,
                    "companies": ", ".join(a.companies),
                    "sample_size": len(a.companies),
                    "confidence": f"{a.confidence:.1%}",
                    "key_characteristics": {
                        k: v for k, v in a.characteristics.items()
                        if k not in ["industry_cluster", "geographic_pattern"]
                    },
                    "observed_outcomes": a.observed_parameters,
                    "top_recommendations": a.recommendations["execution_strategy"][:2],
                }
                for a in archetypes
            ],
            "next_steps": [
                "Validate archetypes with domain experts",
                f"Use FFF archetype registry to seed {len(archetypes)} new customer profiles",
                "Monitor cluster drift as new projects complete",
                "Refine archetype definitions quarterly"
            ]
        }

        return report

    def run(self, min_cluster_size: int = 2) -> Dict:
        """
        Run archetype discovery pipeline.

        Args:
            min_cluster_size: Minimum projects per cluster to formalize

        Returns:
            Dictionary with archetypes and report
        """

        print(f"\n{'='*70}")
        print(f"ARCHETYPE DISCOVERY PIPELINE")
        print(f"{'='*70}\n")

        # Load completed projects
        print("Loading completed projects...")
        projects = self.load_completed_projects()
        print(f"  Found {len(projects)} completed projects\n")

        if len(projects) < min_cluster_size:
            print(f"⚠️  Not enough projects ({len(projects)} < {min_cluster_size})")
            return {}

        # Cluster similar projects
        print("Clustering similar projects...")
        clusters = self.cluster_projects(projects, similarity_threshold=0.75)
        print(f"  Found {len(clusters)} clusters\n")

        # Formalize archetypes
        print("Formalizing archetypes...")
        archetypes = []
        for i, cluster in enumerate(clusters, 1):
            arch = self.formalize_archetype(cluster)
            archetypes.append(arch)
            print(f"  ✓ Archetype {i}: {arch.code} ({len(arch.companies)} companies)")

        # Save archetypes
        print(f"\nSaving archetype registry...")
        registry_file = self.save_archetypes(archetypes)

        # Generate report
        report = self.generate_discovery_report(archetypes)

        print(f"✅ Registry saved: {registry_file}\n")
        print("DISCOVERY SUMMARY:")
        for arch in archetypes:
            print(f"  {arch.code}: {', '.join(arch.companies)} → {arch.confidence:.0%} confidence")

        return {
            "archetypes": archetypes,
            "report": report,
            "registry_file": registry_file
        }


if __name__ == "__main__":
    print("""
    ARCHETYPE DISCOVERY v1.0

    This script discovers recurring patterns across strategic projects.

    When 3+ projects have similar (Ψ, WHAT, HOW) profile and similar outcomes,
    we formalize them as an ARCHETYPE in FFF registry.

    Benefits:
    - New customers with same profile get better parameter seeding
    - E(θ) shrinks faster (start with informed prior)
    - More accurate confidence intervals
    - Reduces customer onboarding time

    Workflow:
    1. Load all completed projects (intervention-registry)
    2. Extract (Ψ, WHAT, HOW, WHERE) context for each
    3. Cluster similar projects (similarity threshold = 0.75)
    4. Formalize clusters as archetypes
    5. Generate recommendations for new projects
    6. Save to FFF archetype registry
    """)
