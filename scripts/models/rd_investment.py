"""
RDM-1.0: R&D Investment Model

A comprehensive model for analyzing R&D investments, innovation pipeline,
and research productivity.

Key Formulas:
- R&D Intensity = R&D Spend / Revenue
- R&D ROI = (Revenue from New Products - R&D Cost) / R&D Cost
- Pipeline Value = Σ(Project NPV × Success Probability)
- Innovation Rate = New Product Revenue / Total Revenue
- Patent Value = Σ(Future Royalties × Discount Factor)

Dimensions:
- Investment allocation (basic, applied, development)
- Pipeline analysis (stage-gate, success rates)
- Productivity metrics (patents, papers, products)
- Portfolio management (risk, return, timing)

Version: 1.0.0
Date: 2026-01-16
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import math


@dataclass
class RDProject:
    """Represents an R&D project."""
    project_id: str
    name: str
    stage: str  # discovery, concept, development, validation, launch
    total_budget: float
    spent_to_date: float
    expected_completion_years: float
    success_probability: float  # 0-1
    expected_npv_if_successful: float
    annual_revenue_potential: float = 0
    patent_potential: int = 0
    risk_level: str = "medium"  # low, medium, high
    strategic_priority: str = "medium"  # low, medium, high, critical


@dataclass
class PatentPortfolio:
    """Represents a patent portfolio."""
    total_patents: int = 0
    pending_applications: int = 0
    patents_by_category: Dict[str, int] = field(default_factory=dict)
    avg_remaining_life_years: float = 10
    annual_licensing_revenue: float = 0
    annual_maintenance_cost: float = 0
    key_patents: int = 0  # Patents essential to core products


# Stage-gate success probabilities by industry
STAGE_SUCCESS_RATES = {
    "pharma": {
        "discovery": 0.10,
        "preclinical": 0.25,
        "phase1": 0.65,
        "phase2": 0.35,
        "phase3": 0.60,
        "approval": 0.85,
    },
    "technology": {
        "discovery": 0.30,
        "concept": 0.50,
        "development": 0.70,
        "validation": 0.80,
        "launch": 0.90,
    },
    "manufacturing": {
        "discovery": 0.25,
        "concept": 0.45,
        "development": 0.65,
        "validation": 0.75,
        "launch": 0.85,
    },
    "consumer_goods": {
        "discovery": 0.35,
        "concept": 0.55,
        "development": 0.70,
        "validation": 0.80,
        "launch": 0.85,
    },
}

# R&D benchmarks by industry
RD_BENCHMARKS = {
    "pharma": {
        "rd_intensity": 0.18,  # 18% of revenue
        "patent_per_100m": 5,
        "innovation_rate": 0.25,
        "time_to_market_years": 10,
    },
    "technology": {
        "rd_intensity": 0.15,
        "patent_per_100m": 3,
        "innovation_rate": 0.35,
        "time_to_market_years": 2,
    },
    "automotive": {
        "rd_intensity": 0.06,
        "patent_per_100m": 2,
        "innovation_rate": 0.20,
        "time_to_market_years": 4,
    },
    "manufacturing": {
        "rd_intensity": 0.03,
        "patent_per_100m": 1,
        "innovation_rate": 0.15,
        "time_to_market_years": 3,
    },
    "consumer_goods": {
        "rd_intensity": 0.02,
        "patent_per_100m": 0.5,
        "innovation_rate": 0.20,
        "time_to_market_years": 1.5,
    },
}


def calculate_rd_intensity(
    rd_spend: float,
    revenue: float,
    employee_count: int = None,
) -> dict:
    """
    Calculate R&D intensity metrics.

    Args:
        rd_spend: Annual R&D spend
        revenue: Annual revenue
        employee_count: Total employees (optional)

    Returns:
        R&D intensity metrics
    """
    rd_intensity = rd_spend / revenue if revenue > 0 else 0
    rd_per_employee = rd_spend / employee_count if employee_count else None

    return {
        "rd_spend": rd_spend,
        "revenue": revenue,
        "rd_intensity_pct": round(rd_intensity * 100, 2),
        "rd_per_employee": round(rd_per_employee, 2) if rd_per_employee else None,
    }


def analyze_project(
    project: RDProject,
    discount_rate: float = 0.12,
) -> dict:
    """
    Analyze a single R&D project.

    Args:
        project: RDProject object
        discount_rate: Discount rate for NPV calculations

    Returns:
        Project analysis
    """
    # Expected value
    expected_npv = project.expected_npv_if_successful * project.success_probability

    # Risk-adjusted return
    remaining_investment = project.total_budget - project.spent_to_date
    total_investment_pv = project.spent_to_date + remaining_investment / (
        (1 + discount_rate) ** (project.expected_completion_years / 2)
    )

    # Sunk cost consideration
    sunk_cost = project.spent_to_date

    # Go/No-Go value
    # Value of continuing = E[NPV] - remaining investment
    # Value of stopping = -sunk_cost (already spent)
    value_if_continue = expected_npv - remaining_investment
    go_no_go = "continue" if value_if_continue > 0 else "review"

    # Real option value (simplified)
    # Option to abandon adds value under uncertainty
    option_value = max(0, -value_if_continue * 0.2) if value_if_continue < 0 else 0

    return {
        "project_id": project.project_id,
        "name": project.name,
        "stage": project.stage,
        "financials": {
            "total_budget": project.total_budget,
            "spent_to_date": project.spent_to_date,
            "remaining_investment": round(remaining_investment, 2),
            "completion_pct": round(project.spent_to_date / project.total_budget * 100, 1),
        },
        "expected_value": {
            "success_probability": round(project.success_probability * 100, 1),
            "npv_if_successful": project.expected_npv_if_successful,
            "expected_npv": round(expected_npv, 2),
            "expected_revenue": round(project.annual_revenue_potential * project.success_probability, 2),
        },
        "decision": {
            "value_if_continue": round(value_if_continue, 2),
            "recommendation": go_no_go,
            "option_value": round(option_value, 2),
        },
        "attributes": {
            "risk_level": project.risk_level,
            "strategic_priority": project.strategic_priority,
            "patent_potential": project.patent_potential,
            "time_to_completion_years": project.expected_completion_years,
        },
    }


def analyze_pipeline(
    projects: List[RDProject],
    discount_rate: float = 0.12,
    industry: str = "technology",
) -> dict:
    """
    Analyze the full R&D pipeline.

    Args:
        projects: List of RDProject objects
        discount_rate: Discount rate for NPV
        industry: Industry for stage-gate benchmarks

    Returns:
        Pipeline analysis
    """
    success_rates = STAGE_SUCCESS_RATES.get(industry, STAGE_SUCCESS_RATES["technology"])

    project_analyses = []
    total_budget = 0
    total_spent = 0
    total_expected_npv = 0
    total_expected_revenue = 0

    # Stage distribution
    stage_counts = {}
    stage_budgets = {}

    for project in projects:
        analysis = analyze_project(project, discount_rate)
        project_analyses.append(analysis)

        total_budget += project.total_budget
        total_spent += project.spent_to_date
        total_expected_npv += analysis["expected_value"]["expected_npv"]
        total_expected_revenue += analysis["expected_value"]["expected_revenue"]

        # Stage tracking
        stage = project.stage
        stage_counts[stage] = stage_counts.get(stage, 0) + 1
        stage_budgets[stage] = stage_budgets.get(stage, 0) + project.total_budget

    # Pipeline value
    pipeline_value = total_expected_npv

    # Pipeline health indicators
    projects_to_continue = sum(1 for a in project_analyses if a["decision"]["recommendation"] == "continue")
    projects_to_review = len(projects) - projects_to_continue

    # Risk distribution
    risk_distribution = {}
    for project in projects:
        risk_distribution[project.risk_level] = risk_distribution.get(project.risk_level, 0) + 1

    # Priority distribution
    priority_distribution = {}
    for project in projects:
        priority_distribution[project.strategic_priority] = priority_distribution.get(project.strategic_priority, 0) + 1

    # Average success probability
    avg_success_prob = sum(p.success_probability for p in projects) / len(projects) if projects else 0

    # Pipeline efficiency
    efficiency = total_expected_npv / total_budget if total_budget > 0 else 0

    return {
        "summary": {
            "total_projects": len(projects),
            "total_budget": round(total_budget, 2),
            "total_spent": round(total_spent, 2),
            "remaining_investment": round(total_budget - total_spent, 2),
            "pipeline_value": round(pipeline_value, 2),
            "expected_annual_revenue": round(total_expected_revenue, 2),
            "avg_success_probability": round(avg_success_prob * 100, 1),
            "pipeline_efficiency": round(efficiency, 2),
        },
        "stage_distribution": {
            "counts": stage_counts,
            "budgets": {k: round(v, 2) for k, v in stage_budgets.items()},
            "benchmark_success_rates": success_rates,
        },
        "risk_distribution": risk_distribution,
        "priority_distribution": priority_distribution,
        "decision_summary": {
            "continue": projects_to_continue,
            "review": projects_to_review,
        },
        "projects": project_analyses,
    }


def calculate_rd_roi(
    rd_spend_historical: List[float],  # Last 3-5 years
    new_product_revenue: float,
    revenue_from_products_under_n_years: float = None,
    n_years: int = 3,
    time_lag_years: int = 2,
) -> dict:
    """
    Calculate R&D Return on Investment.

    R&D ROI = (Revenue from New Products - R&D Cost) / R&D Cost

    Args:
        rd_spend_historical: R&D spend for last several years
        new_product_revenue: Revenue from new products
        revenue_from_products_under_n_years: Revenue from products launched in last n years
        n_years: Years to consider for "new" products
        time_lag_years: Typical R&D to revenue time lag

    Returns:
        R&D ROI analysis
    """
    # Average R&D spend (considering time lag)
    lagged_rd_spend = rd_spend_historical[:-time_lag_years] if len(rd_spend_historical) > time_lag_years else rd_spend_historical
    avg_rd_spend = sum(lagged_rd_spend) / len(lagged_rd_spend) if lagged_rd_spend else 0

    # Simple ROI
    simple_roi = (new_product_revenue - avg_rd_spend) / avg_rd_spend if avg_rd_spend > 0 else 0

    # Revenue multiple
    revenue_multiple = new_product_revenue / avg_rd_spend if avg_rd_spend > 0 else 0

    # R&D productivity (revenue per R&D dollar)
    total_rd_spend = sum(rd_spend_historical)
    productivity = new_product_revenue / total_rd_spend if total_rd_spend > 0 else 0

    return {
        "rd_spend_analyzed": rd_spend_historical,
        "avg_rd_spend_lagged": round(avg_rd_spend, 2),
        "new_product_revenue": new_product_revenue,
        "simple_roi_pct": round(simple_roi * 100, 1),
        "revenue_multiple": round(revenue_multiple, 2),
        "rd_productivity": round(productivity, 2),
        "time_lag_years": time_lag_years,
        "interpretation": _interpret_rd_roi(simple_roi, revenue_multiple),
    }


def _interpret_rd_roi(roi: float, multiple: float) -> str:
    """Interpret R&D ROI."""
    if roi >= 2.0:  # 200%+ ROI
        return "Excellent - R&D investments generating strong returns"
    elif roi >= 1.0:  # 100%+ ROI
        return "Good - R&D investments are profitable"
    elif roi >= 0.5:  # 50%+ ROI
        return "Acceptable - Moderate returns on R&D"
    elif roi >= 0:
        return "Low - R&D barely covering costs"
    else:
        return "Negative - R&D investments not generating positive returns"


def analyze_patent_portfolio(
    portfolio: PatentPortfolio,
    revenue: float,
    discount_rate: float = 0.10,
) -> dict:
    """
    Analyze patent portfolio value and metrics.

    Args:
        portfolio: PatentPortfolio object
        revenue: Annual revenue
        discount_rate: Discount rate for valuation

    Returns:
        Patent portfolio analysis
    """
    # Licensing yield
    licensing_yield = portfolio.annual_licensing_revenue / revenue if revenue > 0 else 0

    # Net licensing income
    net_licensing = portfolio.annual_licensing_revenue - portfolio.annual_maintenance_cost

    # Patent value estimation (simplified DCF of licensing revenue)
    if portfolio.annual_licensing_revenue > 0:
        years = portfolio.avg_remaining_life_years
        # PV of annuity
        if discount_rate > 0:
            annuity_factor = (1 - (1 + discount_rate) ** -years) / discount_rate
        else:
            annuity_factor = years
        licensing_value = net_licensing * annuity_factor
    else:
        licensing_value = 0

    # Strategic value (key patents)
    strategic_value_per_key_patent = revenue * 0.02  # Assume 2% revenue dependency per key patent
    strategic_value = portfolio.key_patents * strategic_value_per_key_patent

    # Total portfolio value
    total_value = licensing_value + strategic_value

    # Value per patent
    value_per_patent = total_value / portfolio.total_patents if portfolio.total_patents > 0 else 0

    return {
        "portfolio_size": {
            "total_patents": portfolio.total_patents,
            "pending_applications": portfolio.pending_applications,
            "key_patents": portfolio.key_patents,
            "by_category": portfolio.patents_by_category,
        },
        "financials": {
            "annual_licensing_revenue": portfolio.annual_licensing_revenue,
            "annual_maintenance_cost": portfolio.annual_maintenance_cost,
            "net_licensing_income": round(net_licensing, 2),
            "licensing_yield_pct": round(licensing_yield * 100, 3),
        },
        "valuation": {
            "licensing_value": round(licensing_value, 2),
            "strategic_value": round(strategic_value, 2),
            "total_portfolio_value": round(total_value, 2),
            "value_per_patent": round(value_per_patent, 2),
            "avg_remaining_life_years": portfolio.avg_remaining_life_years,
        },
    }


def calculate_innovation_metrics(
    total_revenue: float,
    new_product_revenue: float,  # Products launched in last 3 years
    rd_spend: float,
    patents_filed: int,
    products_launched: int,
    rd_headcount: int = None,
    papers_published: int = 0,
) -> dict:
    """
    Calculate key innovation metrics.

    Args:
        total_revenue: Total annual revenue
        new_product_revenue: Revenue from new products
        rd_spend: Annual R&D spend
        patents_filed: Patents filed in year
        products_launched: New products launched
        rd_headcount: R&D employee count
        papers_published: Scientific papers published

    Returns:
        Innovation metrics
    """
    # Innovation rate (Vitality Index)
    innovation_rate = new_product_revenue / total_revenue if total_revenue > 0 else 0

    # Patents per $M R&D spend
    patents_per_million = patents_filed / (rd_spend / 1_000_000) if rd_spend > 0 else 0

    # Products per $M R&D spend
    products_per_million = products_launched / (rd_spend / 1_000_000) if rd_spend > 0 else 0

    # Revenue per R&D dollar
    revenue_per_rd_dollar = new_product_revenue / rd_spend if rd_spend > 0 else 0

    result = {
        "innovation_rate_pct": round(innovation_rate * 100, 1),
        "new_product_revenue": new_product_revenue,
        "patents_filed": patents_filed,
        "products_launched": products_launched,
        "efficiency": {
            "patents_per_million_rd": round(patents_per_million, 2),
            "products_per_million_rd": round(products_per_million, 2),
            "revenue_per_rd_dollar": round(revenue_per_rd_dollar, 2),
        },
    }

    if rd_headcount:
        result["per_researcher"] = {
            "patents_per_researcher": round(patents_filed / rd_headcount, 2),
            "rd_spend_per_researcher": round(rd_spend / rd_headcount, 2),
            "papers_per_researcher": round(papers_published / rd_headcount, 2) if papers_published else None,
        }

    return result


def allocate_rd_budget(
    total_budget: float,
    strategic_priorities: dict,
    risk_tolerance: str = "moderate",
    industry: str = "technology",
) -> dict:
    """
    Recommend R&D budget allocation.

    Args:
        total_budget: Total R&D budget
        strategic_priorities: Dict of priority areas with importance weights
        risk_tolerance: "conservative", "moderate", "aggressive"
        industry: Industry type

    Returns:
        Budget allocation recommendation
    """
    # Base allocation by R&D type
    type_allocations = {
        "conservative": {"basic": 0.10, "applied": 0.35, "development": 0.55},
        "moderate": {"basic": 0.15, "applied": 0.35, "development": 0.50},
        "aggressive": {"basic": 0.25, "applied": 0.35, "development": 0.40},
    }

    base_allocation = type_allocations.get(risk_tolerance, type_allocations["moderate"])

    # Allocate within development based on priorities
    total_priority_weight = sum(strategic_priorities.values())
    priority_allocation = {}

    for priority, weight in strategic_priorities.items():
        share = weight / total_priority_weight if total_priority_weight > 0 else 1 / len(strategic_priorities)
        priority_allocation[priority] = round(total_budget * base_allocation["development"] * share, 2)

    # Time horizon allocation
    horizon_allocation = {
        "short_term_1_2yr": round(total_budget * 0.40, 2),
        "medium_term_3_5yr": round(total_budget * 0.35, 2),
        "long_term_5plus_yr": round(total_budget * 0.25, 2),
    }

    return {
        "total_budget": total_budget,
        "risk_tolerance": risk_tolerance,
        "by_type": {
            "basic_research": round(total_budget * base_allocation["basic"], 2),
            "applied_research": round(total_budget * base_allocation["applied"], 2),
            "development": round(total_budget * base_allocation["development"], 2),
        },
        "by_priority": priority_allocation,
        "by_time_horizon": horizon_allocation,
        "recommendations": [
            f"Allocate {base_allocation['basic']*100:.0f}% to basic research for long-term innovation",
            f"Focus development budget on top strategic priorities",
            f"Maintain balanced portfolio across time horizons",
        ],
    }


def benchmark_rd(
    rd_intensity: float,
    patents_per_100m: float,
    innovation_rate: float,
    time_to_market_years: float,
    industry: str = "technology",
) -> dict:
    """
    Benchmark R&D metrics against industry.

    Args:
        rd_intensity: R&D spend as % of revenue
        patents_per_100m: Patents per $100M revenue
        innovation_rate: New product revenue / total revenue
        time_to_market_years: Average time to market
        industry: Industry for benchmarking

    Returns:
        Benchmark comparison
    """
    benchmarks = RD_BENCHMARKS.get(industry, RD_BENCHMARKS["technology"])

    def get_rating(value, benchmark, higher_is_better=True):
        ratio = value / benchmark if benchmark > 0 else 0
        if higher_is_better:
            if ratio >= 1.3:
                return "excellent"
            elif ratio >= 0.9:
                return "good"
            elif ratio >= 0.6:
                return "acceptable"
            else:
                return "below_average"
        else:
            if ratio <= 0.7:
                return "excellent"
            elif ratio <= 0.9:
                return "good"
            elif ratio <= 1.3:
                return "acceptable"
            else:
                return "below_average"

    return {
        "industry": industry,
        "metrics": {
            "rd_intensity": {
                "value_pct": round(rd_intensity * 100, 2),
                "benchmark_pct": round(benchmarks["rd_intensity"] * 100, 2),
                "rating": get_rating(rd_intensity, benchmarks["rd_intensity"], True),
            },
            "patents_per_100m": {
                "value": patents_per_100m,
                "benchmark": benchmarks["patent_per_100m"],
                "rating": get_rating(patents_per_100m, benchmarks["patent_per_100m"], True),
            },
            "innovation_rate": {
                "value_pct": round(innovation_rate * 100, 1),
                "benchmark_pct": round(benchmarks["innovation_rate"] * 100, 1),
                "rating": get_rating(innovation_rate, benchmarks["innovation_rate"], True),
            },
            "time_to_market": {
                "value_years": time_to_market_years,
                "benchmark_years": benchmarks["time_to_market_years"],
                "rating": get_rating(time_to_market_years, benchmarks["time_to_market_years"], False),
            },
        },
    }


def analyze_rd_investment(
    rd_spend: float,
    revenue: float,
    projects: List[RDProject] = None,
    patent_portfolio: PatentPortfolio = None,
    new_product_revenue: float = None,
    rd_spend_historical: List[float] = None,
    patents_filed: int = 0,
    products_launched: int = 0,
    rd_headcount: int = None,
    industry: str = "technology",
    run_pipeline_analysis: bool = True,
    run_roi_analysis: bool = True,
    run_benchmarks: bool = True,
) -> dict:
    """
    Run comprehensive R&D investment analysis (RDM-1.0 main entry point).

    Args:
        rd_spend: Current year R&D spend
        revenue: Current year revenue
        projects: List of RDProject objects
        patent_portfolio: PatentPortfolio object
        new_product_revenue: Revenue from new products
        rd_spend_historical: Historical R&D spend
        patents_filed: Patents filed this year
        products_launched: Products launched this year
        rd_headcount: R&D employee count
        industry: Industry for benchmarking
        run_pipeline_analysis: Include pipeline analysis
        run_roi_analysis: Include ROI analysis
        run_benchmarks: Include benchmarking

    Returns:
        Comprehensive R&D analysis
    """
    # R&D intensity
    intensity = calculate_rd_intensity(rd_spend, revenue, rd_headcount)

    result = {
        "model_id": "RDM-1.0",
        "model_name": "R&D Investment Model",
        "summary": {
            "rd_spend": rd_spend,
            "revenue": revenue,
            "rd_intensity_pct": intensity["rd_intensity_pct"],
            "rd_per_employee": intensity["rd_per_employee"],
        },
        "intensity_metrics": intensity,
    }

    # Innovation metrics
    if new_product_revenue:
        innovation = calculate_innovation_metrics(
            total_revenue=revenue,
            new_product_revenue=new_product_revenue,
            rd_spend=rd_spend,
            patents_filed=patents_filed,
            products_launched=products_launched,
            rd_headcount=rd_headcount,
        )
        result["innovation_metrics"] = innovation
        result["summary"]["innovation_rate_pct"] = innovation["innovation_rate_pct"]
        result["summary"]["patents_filed"] = patents_filed

    # Pipeline analysis
    if projects and run_pipeline_analysis:
        pipeline = analyze_pipeline(projects, industry=industry)
        result["pipeline_analysis"] = pipeline
        result["summary"]["total_projects"] = pipeline["summary"]["total_projects"]
        result["summary"]["pipeline_value"] = pipeline["summary"]["pipeline_value"]

    # Patent portfolio
    if patent_portfolio:
        patents = analyze_patent_portfolio(patent_portfolio, revenue)
        result["patent_analysis"] = patents
        result["summary"]["total_patents"] = patents["portfolio_size"]["total_patents"]
        result["summary"]["patent_portfolio_value"] = patents["valuation"]["total_portfolio_value"]

    # R&D ROI
    if rd_spend_historical and new_product_revenue and run_roi_analysis:
        roi = calculate_rd_roi(rd_spend_historical, new_product_revenue)
        result["roi_analysis"] = roi
        result["summary"]["rd_roi_pct"] = roi["simple_roi_pct"]

    # Benchmarking
    if run_benchmarks:
        patents_per_100m = patents_filed / (revenue / 100_000_000) if revenue > 0 else 0
        innovation_rate = new_product_revenue / revenue if new_product_revenue and revenue > 0 else 0

        result["benchmark"] = benchmark_rd(
            rd_intensity=intensity["rd_intensity_pct"] / 100,
            patents_per_100m=patents_per_100m,
            innovation_rate=innovation_rate,
            time_to_market_years=2.5,  # Would come from actual data
            industry=industry,
        )

    return result


# Convenience alias
calculate_rd = analyze_rd_investment


if __name__ == "__main__":
    # Example: Technology Company
    print("=" * 60)
    print("RDM-1.0: R&D Investment Model")
    print("=" * 60)

    # Define R&D projects
    projects = [
        RDProject(
            project_id="P001",
            name="Next-Gen Platform",
            stage="development",
            total_budget=5_000_000,
            spent_to_date=3_000_000,
            expected_completion_years=1.5,
            success_probability=0.75,
            expected_npv_if_successful=25_000_000,
            annual_revenue_potential=10_000_000,
            patent_potential=3,
            risk_level="medium",
            strategic_priority="critical",
        ),
        RDProject(
            project_id="P002",
            name="AI Features",
            stage="concept",
            total_budget=2_000_000,
            spent_to_date=500_000,
            expected_completion_years=2.5,
            success_probability=0.50,
            expected_npv_if_successful=15_000_000,
            annual_revenue_potential=5_000_000,
            patent_potential=2,
            risk_level="high",
            strategic_priority="high",
        ),
        RDProject(
            project_id="P003",
            name="UX Improvements",
            stage="validation",
            total_budget=1_000_000,
            spent_to_date=800_000,
            expected_completion_years=0.5,
            success_probability=0.90,
            expected_npv_if_successful=3_000_000,
            annual_revenue_potential=2_000_000,
            patent_potential=0,
            risk_level="low",
            strategic_priority="medium",
        ),
    ]

    # Define patent portfolio
    patent_portfolio = PatentPortfolio(
        total_patents=45,
        pending_applications=12,
        patents_by_category={"software": 30, "hardware": 10, "design": 5},
        avg_remaining_life_years=12,
        annual_licensing_revenue=500_000,
        annual_maintenance_cost=100_000,
        key_patents=8,
    )

    result = analyze_rd_investment(
        rd_spend=15_000_000,
        revenue=100_000_000,
        projects=projects,
        patent_portfolio=patent_portfolio,
        new_product_revenue=35_000_000,
        rd_spend_historical=[12_000_000, 13_000_000, 14_000_000, 15_000_000],
        patents_filed=8,
        products_launched=3,
        rd_headcount=120,
        industry="technology",
    )

    print(f"\nSummary:")
    print(f"  R&D Spend: ${result['summary']['rd_spend']:,.0f}")
    print(f"  R&D Intensity: {result['summary']['rd_intensity_pct']}%")
    print(f"  R&D per Employee: ${result['summary']['rd_per_employee']:,.0f}")
    print(f"  Innovation Rate: {result['summary']['innovation_rate_pct']}%")

    if "pipeline_analysis" in result:
        pipe = result["pipeline_analysis"]["summary"]
        print(f"\nR&D Pipeline:")
        print(f"  Total Projects: {pipe['total_projects']}")
        print(f"  Pipeline Value: ${pipe['pipeline_value']:,.0f}")
        print(f"  Avg Success Probability: {pipe['avg_success_probability']}%")

    if "patent_analysis" in result:
        pat = result["patent_analysis"]
        print(f"\nPatent Portfolio:")
        print(f"  Total Patents: {pat['portfolio_size']['total_patents']}")
        print(f"  Portfolio Value: ${pat['valuation']['total_portfolio_value']:,.0f}")
        print(f"  Net Licensing Income: ${pat['financials']['net_licensing_income']:,.0f}")

    if "roi_analysis" in result:
        print(f"\nR&D ROI:")
        print(f"  Simple ROI: {result['summary']['rd_roi_pct']}%")
        print(f"  Interpretation: {result['roi_analysis']['interpretation']}")
