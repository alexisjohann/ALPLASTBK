"""
ESG-1.0: Environmental, Social & Governance Scoring Model

A comprehensive model for measuring and analyzing ESG performance,
with alignment to major frameworks (GRI, SASB, TCFD, EU CSRD).

Key Components:
- Environmental: Carbon emissions, energy, water, waste, biodiversity
- Social: Workforce, health & safety, community, human rights, supply chain
- Governance: Board, ethics, transparency, risk management

Scoring:
- Individual metrics: 0-100 scale
- Pillar scores: Weighted average of metrics
- Overall ESG score: Weighted average of pillars (E:35%, S:35%, G:30%)

Version: 1.0.0
Date: 2026-01-16
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import math


@dataclass
class EnvironmentalMetrics:
    """Environmental performance metrics."""
    # Carbon & Emissions
    scope1_emissions_tco2: float = 0  # Direct emissions
    scope2_emissions_tco2: float = 0  # Indirect from energy
    scope3_emissions_tco2: float = 0  # Value chain emissions
    carbon_intensity: float = 0  # tCO2 per revenue unit
    emission_reduction_target_pct: float = 0  # Annual reduction target
    emission_reduction_achieved_pct: float = 0  # Actual reduction

    # Energy
    total_energy_mwh: float = 0
    renewable_energy_pct: float = 0
    energy_intensity: float = 0  # MWh per revenue unit

    # Water & Waste
    water_consumption_m3: float = 0
    water_recycled_pct: float = 0
    waste_generated_tons: float = 0
    waste_recycled_pct: float = 0
    hazardous_waste_pct: float = 0

    # Compliance
    environmental_fines: float = 0
    environmental_certifications: int = 0  # ISO 14001, etc.


@dataclass
class SocialMetrics:
    """Social performance metrics."""
    # Workforce
    total_employees: int = 0
    female_employees_pct: float = 0
    female_leadership_pct: float = 0
    minority_employees_pct: float = 0
    employee_turnover_pct: float = 0
    training_hours_per_employee: float = 0
    employee_satisfaction_score: float = 0  # 0-100

    # Health & Safety
    ltir: float = 0  # Lost Time Injury Rate
    trir: float = 0  # Total Recordable Incident Rate
    fatalities: int = 0
    safety_training_pct: float = 0

    # Labor Practices
    living_wage_pct: float = 0  # % employees at living wage
    collective_bargaining_pct: float = 0
    parental_leave_weeks: int = 0

    # Community
    community_investment: float = 0  # Annual investment
    volunteer_hours: float = 0
    local_hiring_pct: float = 0

    # Supply Chain
    supplier_code_of_conduct_pct: float = 0
    supplier_audits_pct: float = 0


@dataclass
class GovernanceMetrics:
    """Governance performance metrics."""
    # Board
    board_size: int = 0
    independent_directors_pct: float = 0
    female_board_pct: float = 0
    board_diversity_score: float = 0  # 0-100
    avg_board_tenure_years: float = 0
    board_meetings_per_year: int = 0
    ceo_chair_separation: bool = False

    # Ethics & Compliance
    ethics_hotline: bool = False
    whistleblower_cases: int = 0
    corruption_cases: int = 0
    ethics_training_pct: float = 0
    code_of_conduct_violations: int = 0

    # Transparency
    sustainability_report: bool = False
    integrated_report: bool = False
    external_assurance: bool = False
    tcfd_aligned: bool = False
    gri_aligned: bool = False

    # Risk Management
    esg_committee: bool = False
    climate_risk_assessment: bool = False
    cybersecurity_incidents: int = 0

    # Executive Compensation
    esg_linked_compensation_pct: float = 0
    ceo_pay_ratio: float = 0


# Industry benchmarks for ESG metrics
ESG_BENCHMARKS = {
    "manufacturing": {
        "scope1_2_intensity": 50,  # tCO2/M revenue
        "renewable_energy_pct": 30,
        "waste_recycled_pct": 60,
        "female_leadership_pct": 25,
        "ltir": 2.0,
        "independent_directors_pct": 60,
    },
    "technology": {
        "scope1_2_intensity": 10,
        "renewable_energy_pct": 50,
        "waste_recycled_pct": 70,
        "female_leadership_pct": 30,
        "ltir": 0.5,
        "independent_directors_pct": 70,
    },
    "financial_services": {
        "scope1_2_intensity": 5,
        "renewable_energy_pct": 40,
        "waste_recycled_pct": 80,
        "female_leadership_pct": 35,
        "ltir": 0.2,
        "independent_directors_pct": 75,
    },
    "retail": {
        "scope1_2_intensity": 20,
        "renewable_energy_pct": 25,
        "waste_recycled_pct": 50,
        "female_leadership_pct": 35,
        "ltir": 3.0,
        "independent_directors_pct": 60,
    },
    "energy": {
        "scope1_2_intensity": 200,
        "renewable_energy_pct": 20,
        "waste_recycled_pct": 40,
        "female_leadership_pct": 20,
        "ltir": 1.5,
        "independent_directors_pct": 65,
    },
    "healthcare": {
        "scope1_2_intensity": 15,
        "renewable_energy_pct": 30,
        "waste_recycled_pct": 45,
        "female_leadership_pct": 40,
        "ltir": 4.0,
        "independent_directors_pct": 70,
    },
}

# Weights for ESG scoring
DEFAULT_WEIGHTS = {
    "environmental": 0.35,
    "social": 0.35,
    "governance": 0.30,
}

# Sub-category weights
ENVIRONMENTAL_WEIGHTS = {
    "carbon": 0.40,
    "energy": 0.25,
    "waste_water": 0.20,
    "compliance": 0.15,
}

SOCIAL_WEIGHTS = {
    "workforce": 0.30,
    "health_safety": 0.25,
    "labor_practices": 0.20,
    "community": 0.15,
    "supply_chain": 0.10,
}

GOVERNANCE_WEIGHTS = {
    "board": 0.30,
    "ethics": 0.25,
    "transparency": 0.25,
    "risk_management": 0.20,
}


def score_environmental(
    metrics: EnvironmentalMetrics,
    revenue_millions: float,
    industry: str = "manufacturing",
) -> dict:
    """
    Calculate environmental pillar score.

    Args:
        metrics: EnvironmentalMetrics object
        revenue_millions: Annual revenue in millions
        industry: Industry for benchmarking

    Returns:
        Environmental score breakdown
    """
    benchmarks = ESG_BENCHMARKS.get(industry, ESG_BENCHMARKS["manufacturing"])

    # Carbon score (40% of environmental)
    total_scope1_2 = metrics.scope1_emissions_tco2 + metrics.scope2_emissions_tco2
    intensity = total_scope1_2 / revenue_millions if revenue_millions > 0 else 0
    intensity_benchmark = benchmarks["scope1_2_intensity"]

    if intensity <= intensity_benchmark * 0.5:
        carbon_intensity_score = 100
    elif intensity <= intensity_benchmark:
        carbon_intensity_score = 70 + 30 * (1 - intensity / intensity_benchmark)
    elif intensity <= intensity_benchmark * 1.5:
        carbon_intensity_score = 40 + 30 * (1.5 - intensity / intensity_benchmark)
    else:
        carbon_intensity_score = max(0, 40 * (2 - intensity / intensity_benchmark))

    # Reduction target score
    if metrics.emission_reduction_target_pct >= 5:
        reduction_target_score = min(100, 60 + metrics.emission_reduction_target_pct * 4)
    else:
        reduction_target_score = metrics.emission_reduction_target_pct * 12

    # Achievement score
    if metrics.emission_reduction_target_pct > 0:
        achievement_ratio = metrics.emission_reduction_achieved_pct / metrics.emission_reduction_target_pct
        achievement_score = min(100, achievement_ratio * 100)
    else:
        achievement_score = 50  # Neutral if no target

    carbon_score = (carbon_intensity_score * 0.5 + reduction_target_score * 0.25 + achievement_score * 0.25)

    # Energy score (25% of environmental)
    renewable_benchmark = benchmarks["renewable_energy_pct"]
    if metrics.renewable_energy_pct >= renewable_benchmark * 1.5:
        renewable_score = 100
    elif metrics.renewable_energy_pct >= renewable_benchmark:
        renewable_score = 70 + 30 * (metrics.renewable_energy_pct / renewable_benchmark - 1) / 0.5
    else:
        renewable_score = 70 * metrics.renewable_energy_pct / renewable_benchmark

    energy_score = renewable_score

    # Waste & Water score (20% of environmental)
    waste_benchmark = benchmarks["waste_recycled_pct"]
    if metrics.waste_recycled_pct >= waste_benchmark:
        waste_score = 70 + 30 * min(1, (metrics.waste_recycled_pct - waste_benchmark) / (100 - waste_benchmark))
    else:
        waste_score = 70 * metrics.waste_recycled_pct / waste_benchmark

    water_score = min(100, metrics.water_recycled_pct * 1.5)

    waste_water_score = waste_score * 0.6 + water_score * 0.4

    # Compliance score (15% of environmental)
    compliance_score = 100 if metrics.environmental_fines == 0 else max(0, 100 - metrics.environmental_fines / 10000)
    cert_score = min(100, metrics.environmental_certifications * 25)
    compliance_total = compliance_score * 0.7 + cert_score * 0.3

    # Overall environmental score
    environmental_score = (
        carbon_score * ENVIRONMENTAL_WEIGHTS["carbon"] +
        energy_score * ENVIRONMENTAL_WEIGHTS["energy"] +
        waste_water_score * ENVIRONMENTAL_WEIGHTS["waste_water"] +
        compliance_total * ENVIRONMENTAL_WEIGHTS["compliance"]
    )

    return {
        "pillar": "Environmental",
        "score": round(environmental_score, 1),
        "components": {
            "carbon": {
                "score": round(carbon_score, 1),
                "weight": ENVIRONMENTAL_WEIGHTS["carbon"],
                "metrics": {
                    "scope1_2_emissions": total_scope1_2,
                    "carbon_intensity": round(intensity, 2),
                    "benchmark_intensity": intensity_benchmark,
                    "reduction_target_pct": metrics.emission_reduction_target_pct,
                    "reduction_achieved_pct": metrics.emission_reduction_achieved_pct,
                },
            },
            "energy": {
                "score": round(energy_score, 1),
                "weight": ENVIRONMENTAL_WEIGHTS["energy"],
                "metrics": {
                    "total_energy_mwh": metrics.total_energy_mwh,
                    "renewable_pct": metrics.renewable_energy_pct,
                    "benchmark_renewable_pct": renewable_benchmark,
                },
            },
            "waste_water": {
                "score": round(waste_water_score, 1),
                "weight": ENVIRONMENTAL_WEIGHTS["waste_water"],
                "metrics": {
                    "waste_recycled_pct": metrics.waste_recycled_pct,
                    "water_recycled_pct": metrics.water_recycled_pct,
                },
            },
            "compliance": {
                "score": round(compliance_total, 1),
                "weight": ENVIRONMENTAL_WEIGHTS["compliance"],
                "metrics": {
                    "fines": metrics.environmental_fines,
                    "certifications": metrics.environmental_certifications,
                },
            },
        },
    }


def score_social(
    metrics: SocialMetrics,
    industry: str = "manufacturing",
) -> dict:
    """
    Calculate social pillar score.

    Args:
        metrics: SocialMetrics object
        industry: Industry for benchmarking

    Returns:
        Social score breakdown
    """
    benchmarks = ESG_BENCHMARKS.get(industry, ESG_BENCHMARKS["manufacturing"])

    # Workforce score (30% of social)
    diversity_benchmark = benchmarks["female_leadership_pct"]
    diversity_score = min(100, metrics.female_leadership_pct / diversity_benchmark * 70) if diversity_benchmark > 0 else 50

    if metrics.employee_turnover_pct <= 10:
        turnover_score = 100
    elif metrics.employee_turnover_pct <= 20:
        turnover_score = 100 - (metrics.employee_turnover_pct - 10) * 3
    else:
        turnover_score = max(0, 70 - (metrics.employee_turnover_pct - 20) * 2)

    training_score = min(100, metrics.training_hours_per_employee / 40 * 100)
    satisfaction_score = metrics.employee_satisfaction_score

    workforce_score = diversity_score * 0.3 + turnover_score * 0.25 + training_score * 0.2 + satisfaction_score * 0.25

    # Health & Safety score (25% of social)
    ltir_benchmark = benchmarks["ltir"]
    if metrics.ltir <= ltir_benchmark * 0.5:
        ltir_score = 100
    elif metrics.ltir <= ltir_benchmark:
        ltir_score = 70 + 30 * (1 - metrics.ltir / ltir_benchmark)
    else:
        ltir_score = max(0, 70 * (2 - metrics.ltir / ltir_benchmark))

    fatality_score = 100 if metrics.fatalities == 0 else max(0, 100 - metrics.fatalities * 50)
    safety_training_score = min(100, metrics.safety_training_pct * 1.2)

    health_safety_score = ltir_score * 0.4 + fatality_score * 0.4 + safety_training_score * 0.2

    # Labor Practices score (20% of social)
    living_wage_score = min(100, metrics.living_wage_pct * 1.1)
    parental_leave_score = min(100, metrics.parental_leave_weeks / 16 * 100)  # 16 weeks = 100

    labor_score = living_wage_score * 0.6 + parental_leave_score * 0.4

    # Community score (15% of social)
    community_score = min(100, metrics.local_hiring_pct * 1.2)

    # Supply Chain score (10% of social)
    supply_chain_score = (
        min(100, metrics.supplier_code_of_conduct_pct * 1.1) * 0.5 +
        min(100, metrics.supplier_audits_pct * 1.2) * 0.5
    )

    # Overall social score
    social_score = (
        workforce_score * SOCIAL_WEIGHTS["workforce"] +
        health_safety_score * SOCIAL_WEIGHTS["health_safety"] +
        labor_score * SOCIAL_WEIGHTS["labor_practices"] +
        community_score * SOCIAL_WEIGHTS["community"] +
        supply_chain_score * SOCIAL_WEIGHTS["supply_chain"]
    )

    return {
        "pillar": "Social",
        "score": round(social_score, 1),
        "components": {
            "workforce": {
                "score": round(workforce_score, 1),
                "weight": SOCIAL_WEIGHTS["workforce"],
                "metrics": {
                    "female_leadership_pct": metrics.female_leadership_pct,
                    "employee_turnover_pct": metrics.employee_turnover_pct,
                    "training_hours": metrics.training_hours_per_employee,
                    "satisfaction_score": metrics.employee_satisfaction_score,
                },
            },
            "health_safety": {
                "score": round(health_safety_score, 1),
                "weight": SOCIAL_WEIGHTS["health_safety"],
                "metrics": {
                    "ltir": metrics.ltir,
                    "benchmark_ltir": ltir_benchmark,
                    "fatalities": metrics.fatalities,
                    "safety_training_pct": metrics.safety_training_pct,
                },
            },
            "labor_practices": {
                "score": round(labor_score, 1),
                "weight": SOCIAL_WEIGHTS["labor_practices"],
                "metrics": {
                    "living_wage_pct": metrics.living_wage_pct,
                    "parental_leave_weeks": metrics.parental_leave_weeks,
                },
            },
            "community": {
                "score": round(community_score, 1),
                "weight": SOCIAL_WEIGHTS["community"],
                "metrics": {
                    "local_hiring_pct": metrics.local_hiring_pct,
                },
            },
            "supply_chain": {
                "score": round(supply_chain_score, 1),
                "weight": SOCIAL_WEIGHTS["supply_chain"],
                "metrics": {
                    "supplier_code_pct": metrics.supplier_code_of_conduct_pct,
                    "supplier_audits_pct": metrics.supplier_audits_pct,
                },
            },
        },
    }


def score_governance(
    metrics: GovernanceMetrics,
    industry: str = "manufacturing",
) -> dict:
    """
    Calculate governance pillar score.

    Args:
        metrics: GovernanceMetrics object
        industry: Industry for benchmarking

    Returns:
        Governance score breakdown
    """
    benchmarks = ESG_BENCHMARKS.get(industry, ESG_BENCHMARKS["manufacturing"])

    # Board score (30% of governance)
    independence_benchmark = benchmarks["independent_directors_pct"]
    if metrics.independent_directors_pct >= independence_benchmark:
        independence_score = 70 + 30 * min(1, (metrics.independent_directors_pct - independence_benchmark) / 30)
    else:
        independence_score = 70 * metrics.independent_directors_pct / independence_benchmark

    diversity_score = min(100, metrics.female_board_pct / 40 * 100)  # 40% = 100
    separation_score = 100 if metrics.ceo_chair_separation else 50
    meetings_score = min(100, metrics.board_meetings_per_year / 10 * 100)

    board_score = independence_score * 0.4 + diversity_score * 0.3 + separation_score * 0.15 + meetings_score * 0.15

    # Ethics score (25% of governance)
    hotline_score = 100 if metrics.ethics_hotline else 30
    corruption_score = 100 if metrics.corruption_cases == 0 else max(0, 100 - metrics.corruption_cases * 30)
    training_score = min(100, metrics.ethics_training_pct * 1.1)
    violations_score = 100 if metrics.code_of_conduct_violations == 0 else max(0, 100 - metrics.code_of_conduct_violations * 5)

    ethics_score = hotline_score * 0.2 + corruption_score * 0.3 + training_score * 0.25 + violations_score * 0.25

    # Transparency score (25% of governance)
    report_score = 0
    if metrics.sustainability_report:
        report_score += 30
    if metrics.integrated_report:
        report_score += 20
    if metrics.external_assurance:
        report_score += 20
    if metrics.tcfd_aligned:
        report_score += 15
    if metrics.gri_aligned:
        report_score += 15

    transparency_score = min(100, report_score)

    # Risk Management score (20% of governance)
    esg_committee_score = 100 if metrics.esg_committee else 40
    climate_risk_score = 100 if metrics.climate_risk_assessment else 30
    cyber_score = 100 if metrics.cybersecurity_incidents == 0 else max(0, 100 - metrics.cybersecurity_incidents * 20)
    compensation_score = min(100, metrics.esg_linked_compensation_pct * 2)  # 50% = 100

    risk_score = esg_committee_score * 0.3 + climate_risk_score * 0.3 + cyber_score * 0.2 + compensation_score * 0.2

    # Overall governance score
    governance_score = (
        board_score * GOVERNANCE_WEIGHTS["board"] +
        ethics_score * GOVERNANCE_WEIGHTS["ethics"] +
        transparency_score * GOVERNANCE_WEIGHTS["transparency"] +
        risk_score * GOVERNANCE_WEIGHTS["risk_management"]
    )

    return {
        "pillar": "Governance",
        "score": round(governance_score, 1),
        "components": {
            "board": {
                "score": round(board_score, 1),
                "weight": GOVERNANCE_WEIGHTS["board"],
                "metrics": {
                    "independent_directors_pct": metrics.independent_directors_pct,
                    "female_board_pct": metrics.female_board_pct,
                    "ceo_chair_separation": metrics.ceo_chair_separation,
                    "board_meetings": metrics.board_meetings_per_year,
                },
            },
            "ethics": {
                "score": round(ethics_score, 1),
                "weight": GOVERNANCE_WEIGHTS["ethics"],
                "metrics": {
                    "ethics_hotline": metrics.ethics_hotline,
                    "corruption_cases": metrics.corruption_cases,
                    "ethics_training_pct": metrics.ethics_training_pct,
                },
            },
            "transparency": {
                "score": round(transparency_score, 1),
                "weight": GOVERNANCE_WEIGHTS["transparency"],
                "metrics": {
                    "sustainability_report": metrics.sustainability_report,
                    "tcfd_aligned": metrics.tcfd_aligned,
                    "external_assurance": metrics.external_assurance,
                },
            },
            "risk_management": {
                "score": round(risk_score, 1),
                "weight": GOVERNANCE_WEIGHTS["risk_management"],
                "metrics": {
                    "esg_committee": metrics.esg_committee,
                    "climate_risk_assessment": metrics.climate_risk_assessment,
                    "esg_compensation_pct": metrics.esg_linked_compensation_pct,
                },
            },
        },
    }


def calculate_overall_esg_score(
    environmental_score: float,
    social_score: float,
    governance_score: float,
    weights: dict = None,
) -> dict:
    """
    Calculate overall ESG score from pillar scores.

    Args:
        environmental_score: Environmental pillar score
        social_score: Social pillar score
        governance_score: Governance pillar score
        weights: Optional custom weights

    Returns:
        Overall ESG score and rating
    """
    if weights is None:
        weights = DEFAULT_WEIGHTS

    overall_score = (
        environmental_score * weights["environmental"] +
        social_score * weights["social"] +
        governance_score * weights["governance"]
    )

    # Rating scale
    if overall_score >= 80:
        rating = "AAA"
        rating_description = "Leader - Best in class ESG performance"
    elif overall_score >= 70:
        rating = "AA"
        rating_description = "Strong - Above average ESG performance"
    elif overall_score >= 60:
        rating = "A"
        rating_description = "Good - Solid ESG performance"
    elif overall_score >= 50:
        rating = "BBB"
        rating_description = "Average - Adequate ESG performance"
    elif overall_score >= 40:
        rating = "BB"
        rating_description = "Below Average - Some ESG concerns"
    elif overall_score >= 30:
        rating = "B"
        rating_description = "Weak - Significant ESG gaps"
    else:
        rating = "CCC"
        rating_description = "Poor - Major ESG risks"

    return {
        "overall_score": round(overall_score, 1),
        "rating": rating,
        "rating_description": rating_description,
        "pillar_scores": {
            "environmental": round(environmental_score, 1),
            "social": round(social_score, 1),
            "governance": round(governance_score, 1),
        },
        "weights": weights,
    }


def identify_improvement_priorities(
    environmental_result: dict,
    social_result: dict,
    governance_result: dict,
    improvement_threshold: float = 60,
) -> dict:
    """
    Identify priority areas for ESG improvement.

    Args:
        environmental_result: Environmental scoring result
        social_result: Social scoring result
        governance_result: Governance scoring result
        improvement_threshold: Score below which improvement is needed

    Returns:
        Prioritized improvement recommendations
    """
    priorities = []

    # Check all components
    all_components = [
        ("Environmental", environmental_result),
        ("Social", social_result),
        ("Governance", governance_result),
    ]

    for pillar_name, result in all_components:
        for component_name, component_data in result["components"].items():
            if component_data["score"] < improvement_threshold:
                impact = component_data["weight"] * DEFAULT_WEIGHTS[pillar_name.lower()]
                priorities.append({
                    "pillar": pillar_name,
                    "component": component_name,
                    "current_score": component_data["score"],
                    "gap_to_threshold": round(improvement_threshold - component_data["score"], 1),
                    "weight": component_data["weight"],
                    "impact_factor": round(impact, 3),
                    "metrics": component_data["metrics"],
                })

    # Sort by impact (weight × gap)
    priorities.sort(key=lambda x: x["impact_factor"] * x["gap_to_threshold"], reverse=True)

    # Generate recommendations
    recommendations = []
    for p in priorities[:5]:  # Top 5 priorities
        if p["pillar"] == "Environmental":
            if p["component"] == "carbon":
                recommendations.append(f"Set science-based emission reduction targets (current gap: {p['gap_to_threshold']} pts)")
            elif p["component"] == "energy":
                recommendations.append(f"Increase renewable energy procurement (current gap: {p['gap_to_threshold']} pts)")
        elif p["pillar"] == "Social":
            if p["component"] == "workforce":
                recommendations.append(f"Improve diversity & inclusion programs (current gap: {p['gap_to_threshold']} pts)")
            elif p["component"] == "health_safety":
                recommendations.append(f"Strengthen safety programs and training (current gap: {p['gap_to_threshold']} pts)")
        elif p["pillar"] == "Governance":
            if p["component"] == "transparency":
                recommendations.append(f"Enhance ESG reporting and assurance (current gap: {p['gap_to_threshold']} pts)")
            elif p["component"] == "board":
                recommendations.append(f"Improve board independence and diversity (current gap: {p['gap_to_threshold']} pts)")

    return {
        "priorities": priorities,
        "recommendations": recommendations,
        "threshold_used": improvement_threshold,
    }


def project_esg_improvement(
    current_scores: dict,
    improvement_rates: dict = None,
    years: int = 5,
) -> dict:
    """
    Project ESG score improvement over time.

    Args:
        current_scores: Current pillar scores
        improvement_rates: Annual improvement rates per pillar
        years: Years to project

    Returns:
        ESG score projection
    """
    if improvement_rates is None:
        improvement_rates = {
            "environmental": 3.0,  # 3 points per year
            "social": 2.0,
            "governance": 2.5,
        }

    projections = []
    scores = current_scores.copy()

    for year in range(years + 1):
        overall = calculate_overall_esg_score(
            scores["environmental"],
            scores["social"],
            scores["governance"],
        )

        projections.append({
            "year": year,
            "environmental": round(scores["environmental"], 1),
            "social": round(scores["social"], 1),
            "governance": round(scores["governance"], 1),
            "overall": overall["overall_score"],
            "rating": overall["rating"],
        })

        # Apply improvement (capped at 95)
        scores["environmental"] = min(95, scores["environmental"] + improvement_rates["environmental"])
        scores["social"] = min(95, scores["social"] + improvement_rates["social"])
        scores["governance"] = min(95, scores["governance"] + improvement_rates["governance"])

    return {
        "projections": projections,
        "improvement_rates": improvement_rates,
        "final_rating": projections[-1]["rating"],
        "score_improvement": round(projections[-1]["overall"] - projections[0]["overall"], 1),
    }


def benchmark_esg(
    overall_score: float,
    environmental_score: float,
    social_score: float,
    governance_score: float,
    industry: str = "manufacturing",
) -> dict:
    """
    Benchmark ESG scores against industry peers.

    Args:
        overall_score: Overall ESG score
        environmental_score: Environmental score
        social_score: Social score
        governance_score: Governance score
        industry: Industry for benchmarking

    Returns:
        Benchmark comparison
    """
    # Simplified industry averages (would be more detailed in practice)
    industry_averages = {
        "manufacturing": {"overall": 52, "e": 48, "s": 55, "g": 54},
        "technology": {"overall": 62, "e": 65, "s": 58, "g": 63},
        "financial_services": {"overall": 58, "e": 52, "s": 60, "g": 62},
        "energy": {"overall": 45, "e": 40, "s": 50, "g": 48},
        "retail": {"overall": 50, "e": 48, "s": 52, "g": 50},
        "healthcare": {"overall": 55, "e": 50, "s": 60, "g": 55},
    }

    averages = industry_averages.get(industry, industry_averages["manufacturing"])

    def get_percentile(score, avg):
        # Simplified percentile estimation
        diff = score - avg
        if diff >= 20:
            return 95
        elif diff >= 10:
            return 80
        elif diff >= 0:
            return 60
        elif diff >= -10:
            return 40
        else:
            return 20

    return {
        "industry": industry,
        "overall": {
            "score": overall_score,
            "industry_avg": averages["overall"],
            "vs_avg": round(overall_score - averages["overall"], 1),
            "percentile": get_percentile(overall_score, averages["overall"]),
        },
        "environmental": {
            "score": environmental_score,
            "industry_avg": averages["e"],
            "vs_avg": round(environmental_score - averages["e"], 1),
        },
        "social": {
            "score": social_score,
            "industry_avg": averages["s"],
            "vs_avg": round(social_score - averages["s"], 1),
        },
        "governance": {
            "score": governance_score,
            "industry_avg": averages["g"],
            "vs_avg": round(governance_score - averages["g"], 1),
        },
    }


def analyze_esg(
    environmental: EnvironmentalMetrics,
    social: SocialMetrics,
    governance: GovernanceMetrics,
    revenue_millions: float,
    industry: str = "manufacturing",
    run_projections: bool = True,
    run_benchmarks: bool = True,
    identify_priorities: bool = True,
) -> dict:
    """
    Run comprehensive ESG analysis (ESG-1.0 main entry point).

    Args:
        environmental: EnvironmentalMetrics object
        social: SocialMetrics object
        governance: GovernanceMetrics object
        revenue_millions: Annual revenue in millions
        industry: Industry for benchmarking
        run_projections: Include 5-year projections
        run_benchmarks: Include industry benchmarking
        identify_priorities: Include improvement priorities

    Returns:
        Comprehensive ESG analysis
    """
    # Score each pillar
    env_result = score_environmental(environmental, revenue_millions, industry)
    soc_result = score_social(social, industry)
    gov_result = score_governance(governance, industry)

    # Calculate overall score
    overall = calculate_overall_esg_score(
        env_result["score"],
        soc_result["score"],
        gov_result["score"],
    )

    result = {
        "model_id": "ESG-1.0",
        "model_name": "ESG Scoring Model",
        "summary": {
            "overall_score": overall["overall_score"],
            "rating": overall["rating"],
            "rating_description": overall["rating_description"],
            "environmental_score": env_result["score"],
            "social_score": soc_result["score"],
            "governance_score": gov_result["score"],
        },
        "environmental": env_result,
        "social": soc_result,
        "governance": gov_result,
        "overall": overall,
    }

    # Improvement priorities
    if identify_priorities:
        result["improvement_priorities"] = identify_improvement_priorities(
            env_result, soc_result, gov_result
        )

    # Industry benchmarking
    if run_benchmarks:
        result["benchmark"] = benchmark_esg(
            overall["overall_score"],
            env_result["score"],
            soc_result["score"],
            gov_result["score"],
            industry,
        )

    # Projections
    if run_projections:
        result["projection"] = project_esg_improvement(
            {
                "environmental": env_result["score"],
                "social": soc_result["score"],
                "governance": gov_result["score"],
            }
        )

    return result


# Convenience alias
calculate_esg_score = analyze_esg


if __name__ == "__main__":
    # Example: Manufacturing Company
    print("=" * 60)
    print("ESG-1.0: ESG Scoring Model")
    print("=" * 60)

    # Define metrics
    env_metrics = EnvironmentalMetrics(
        scope1_emissions_tco2=25000,
        scope2_emissions_tco2=15000,
        emission_reduction_target_pct=5,
        emission_reduction_achieved_pct=4,
        total_energy_mwh=80000,
        renewable_energy_pct=35,
        waste_generated_tons=5000,
        waste_recycled_pct=65,
        water_recycled_pct=40,
        environmental_certifications=2,
    )

    soc_metrics = SocialMetrics(
        total_employees=5000,
        female_employees_pct=35,
        female_leadership_pct=28,
        employee_turnover_pct=12,
        training_hours_per_employee=32,
        employee_satisfaction_score=72,
        ltir=1.5,
        fatalities=0,
        safety_training_pct=95,
        living_wage_pct=100,
        parental_leave_weeks=12,
        local_hiring_pct=75,
        supplier_code_of_conduct_pct=85,
        supplier_audits_pct=60,
    )

    gov_metrics = GovernanceMetrics(
        board_size=9,
        independent_directors_pct=67,
        female_board_pct=33,
        ceo_chair_separation=True,
        board_meetings_per_year=8,
        ethics_hotline=True,
        corruption_cases=0,
        ethics_training_pct=98,
        code_of_conduct_violations=3,
        sustainability_report=True,
        external_assurance=True,
        tcfd_aligned=True,
        gri_aligned=True,
        esg_committee=True,
        climate_risk_assessment=True,
        esg_linked_compensation_pct=25,
    )

    result = analyze_esg(
        environmental=env_metrics,
        social=soc_metrics,
        governance=gov_metrics,
        revenue_millions=1000,
        industry="manufacturing",
    )

    print(f"\nOverall ESG:")
    print(f"  Score: {result['summary']['overall_score']}")
    print(f"  Rating: {result['summary']['rating']} - {result['summary']['rating_description']}")

    print(f"\nPillar Scores:")
    print(f"  Environmental: {result['summary']['environmental_score']}")
    print(f"  Social: {result['summary']['social_score']}")
    print(f"  Governance: {result['summary']['governance_score']}")

    if "benchmark" in result:
        print(f"\nIndustry Benchmark ({result['benchmark']['industry']}):")
        print(f"  vs Industry Avg: {result['benchmark']['overall']['vs_avg']:+.1f} pts")
        print(f"  Percentile: {result['benchmark']['overall']['percentile']}th")

    if "improvement_priorities" in result:
        print(f"\nTop Improvement Priorities:")
        for rec in result["improvement_priorities"]["recommendations"][:3]:
            print(f"  - {rec}")

    if "projection" in result:
        proj = result["projection"]
        print(f"\n5-Year Projection:")
        print(f"  Current Rating: {proj['projections'][0]['rating']}")
        print(f"  Projected Rating: {proj['final_rating']}")
        print(f"  Score Improvement: +{proj['score_improvement']} pts")
