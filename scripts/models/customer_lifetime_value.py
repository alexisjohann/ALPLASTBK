"""
CLV-1.0: Customer Lifetime Value Model

A comprehensive model for calculating and analyzing customer lifetime value,
providing the foundation for marketing strategy decisions.

Key Formulas:
- CLV = Σ(margin × retention_rate^t / (1+discount_rate)^t)
- Simple CLV = margin × (retention_rate / (1 + discount_rate - retention_rate))
- LTV:CAC Ratio = CLV / CAC
- Payback Period = CAC / (margin × gross_margin)

Dimensions:
- Customer segments (by value, behavior, acquisition channel)
- Cohort analysis (retention curves)
- Unit economics (contribution margin, variable costs)

Version: 1.0.0
Date: 2026-01-16
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import math


@dataclass
class CustomerSegment:
    """Represents a customer segment with its characteristics."""
    name: str
    avg_revenue_per_period: float  # ARPU
    avg_gross_margin: float  # as decimal (e.g., 0.60 = 60%)
    retention_rate: float  # as decimal (e.g., 0.85 = 85%)
    avg_customer_lifetime_periods: float  # in periods (months/years)
    customer_count: int
    acquisition_cost: float  # CAC per customer
    variable_cost_per_period: float = 0.0  # Service/support costs


@dataclass
class CohortData:
    """Cohort analysis data."""
    cohort_name: str
    start_customers: int
    retention_by_period: List[float]  # Retention rates for each period
    revenue_by_period: List[float]  # Revenue for each period


# Industry benchmarks for CLV metrics
INDUSTRY_BENCHMARKS = {
    "saas": {
        "ltv_cac_ratio": {"excellent": 5.0, "good": 3.0, "acceptable": 2.0, "poor": 1.0},
        "retention_rate": {"excellent": 0.95, "good": 0.90, "acceptable": 0.85, "poor": 0.75},
        "payback_months": {"excellent": 6, "good": 12, "acceptable": 18, "poor": 24},
        "gross_margin": 0.80,
    },
    "ecommerce": {
        "ltv_cac_ratio": {"excellent": 4.0, "good": 2.5, "acceptable": 1.5, "poor": 1.0},
        "retention_rate": {"excellent": 0.60, "good": 0.45, "acceptable": 0.35, "poor": 0.20},
        "payback_months": {"excellent": 3, "good": 6, "acceptable": 12, "poor": 18},
        "gross_margin": 0.40,
    },
    "b2b_services": {
        "ltv_cac_ratio": {"excellent": 6.0, "good": 4.0, "acceptable": 2.5, "poor": 1.5},
        "retention_rate": {"excellent": 0.92, "good": 0.85, "acceptable": 0.78, "poor": 0.65},
        "payback_months": {"excellent": 12, "good": 18, "acceptable": 24, "poor": 36},
        "gross_margin": 0.65,
    },
    "manufacturing": {
        "ltv_cac_ratio": {"excellent": 5.0, "good": 3.5, "acceptable": 2.0, "poor": 1.2},
        "retention_rate": {"excellent": 0.90, "good": 0.82, "acceptable": 0.72, "poor": 0.60},
        "payback_months": {"excellent": 12, "good": 24, "acceptable": 36, "poor": 48},
        "gross_margin": 0.35,
    },
    "retail": {
        "ltv_cac_ratio": {"excellent": 3.5, "good": 2.5, "acceptable": 1.5, "poor": 0.8},
        "retention_rate": {"excellent": 0.55, "good": 0.40, "acceptable": 0.30, "poor": 0.18},
        "payback_months": {"excellent": 2, "good": 4, "acceptable": 8, "poor": 12},
        "gross_margin": 0.30,
    },
    "financial_services": {
        "ltv_cac_ratio": {"excellent": 8.0, "good": 5.0, "acceptable": 3.0, "poor": 1.5},
        "retention_rate": {"excellent": 0.95, "good": 0.88, "acceptable": 0.80, "poor": 0.70},
        "payback_months": {"excellent": 18, "good": 24, "acceptable": 36, "poor": 48},
        "gross_margin": 0.70,
    },
}

# Default industry
DEFAULT_INDUSTRY = "b2b_services"


def calculate_simple_clv(
    margin_per_period: float,
    retention_rate: float,
    discount_rate: float = 0.10,
    periods_per_year: int = 12,
) -> dict:
    """
    Calculate simple CLV using the perpetuity formula.

    CLV = m × (r / (1 + d - r))

    Where:
    - m = margin per period
    - r = retention rate per period
    - d = discount rate per period

    Args:
        margin_per_period: Contribution margin per period
        retention_rate: Retention rate per period (0-1)
        discount_rate: Annual discount rate
        periods_per_year: Number of periods per year (12=monthly, 4=quarterly, 1=annual)

    Returns:
        Dictionary with CLV calculation details
    """
    # Convert annual discount rate to per-period
    d = (1 + discount_rate) ** (1 / periods_per_year) - 1
    r = retention_rate
    m = margin_per_period

    # CLV formula: m × (r / (1 + d - r))
    # Guard against division by zero
    denominator = 1 + d - r
    if denominator <= 0:
        # If retention is very high, use finite horizon approximation
        clv = m * min(100, 1 / (1 - r + 0.01))  # Cap at 100 periods
    else:
        clv = m * (r / denominator)

    # Expected lifetime in periods
    if r >= 1:
        expected_lifetime = 100  # Cap
    else:
        expected_lifetime = 1 / (1 - r)

    return {
        "clv": round(clv, 2),
        "margin_per_period": margin_per_period,
        "retention_rate": retention_rate,
        "discount_rate_annual": discount_rate,
        "discount_rate_period": round(d, 6),
        "expected_lifetime_periods": round(expected_lifetime, 1),
        "expected_lifetime_years": round(expected_lifetime / periods_per_year, 1),
        "total_expected_margin": round(m * expected_lifetime, 2),
    }


def calculate_clv_detailed(
    margin_per_period: float,
    retention_rate: float,
    discount_rate: float = 0.10,
    periods: int = 60,  # 5 years monthly
    periods_per_year: int = 12,
    initial_margin_growth: float = 0.0,  # Margin growth rate
) -> dict:
    """
    Calculate detailed CLV with period-by-period projection.

    CLV = Σ(m_t × r^t / (1+d)^t) for t = 1 to T

    Args:
        margin_per_period: Initial contribution margin per period
        retention_rate: Retention rate per period (0-1)
        discount_rate: Annual discount rate
        periods: Number of periods to project
        periods_per_year: Periods per year
        initial_margin_growth: Annual margin growth rate

    Returns:
        Dictionary with detailed CLV analysis
    """
    # Convert rates to per-period
    d = (1 + discount_rate) ** (1 / periods_per_year) - 1
    g = (1 + initial_margin_growth) ** (1 / periods_per_year) - 1
    r = retention_rate

    period_data = []
    cumulative_clv = 0

    for t in range(1, periods + 1):
        # Survival probability (cumulative retention)
        survival_prob = r ** t

        # Margin in period t (with growth)
        margin_t = margin_per_period * ((1 + g) ** t)

        # Expected margin (margin × survival probability)
        expected_margin = margin_t * survival_prob

        # Present value
        discount_factor = 1 / ((1 + d) ** t)
        pv_margin = expected_margin * discount_factor

        cumulative_clv += pv_margin

        period_data.append({
            "period": t,
            "year": round(t / periods_per_year, 2),
            "survival_probability": round(survival_prob, 4),
            "margin": round(margin_t, 2),
            "expected_margin": round(expected_margin, 2),
            "discount_factor": round(discount_factor, 4),
            "pv_margin": round(pv_margin, 2),
            "cumulative_clv": round(cumulative_clv, 2),
        })

    # Find when 50%, 80%, 90% of CLV is realized
    clv_50 = None
    clv_80 = None
    clv_90 = None

    for p in period_data:
        if clv_50 is None and p["cumulative_clv"] >= cumulative_clv * 0.5:
            clv_50 = p["period"]
        if clv_80 is None and p["cumulative_clv"] >= cumulative_clv * 0.8:
            clv_80 = p["period"]
        if clv_90 is None and p["cumulative_clv"] >= cumulative_clv * 0.9:
            clv_90 = p["period"]

    return {
        "clv": round(cumulative_clv, 2),
        "clv_by_year": {
            1: round(sum(p["pv_margin"] for p in period_data[:periods_per_year]), 2),
            2: round(sum(p["pv_margin"] for p in period_data[periods_per_year:2*periods_per_year]), 2),
            3: round(sum(p["pv_margin"] for p in period_data[2*periods_per_year:3*periods_per_year]), 2),
            4: round(sum(p["pv_margin"] for p in period_data[3*periods_per_year:4*periods_per_year]), 2),
            5: round(sum(p["pv_margin"] for p in period_data[4*periods_per_year:5*periods_per_year]), 2),
        },
        "periods_to_50_pct_clv": clv_50,
        "periods_to_80_pct_clv": clv_80,
        "periods_to_90_pct_clv": clv_90,
        "period_data": period_data[:24],  # First 2 years for brevity
        "parameters": {
            "margin_per_period": margin_per_period,
            "retention_rate": retention_rate,
            "discount_rate": discount_rate,
            "margin_growth_rate": initial_margin_growth,
            "periods": periods,
        },
    }


def calculate_ltv_cac_metrics(
    clv: float,
    cac: float,
    margin_per_period: float,
    gross_margin: float = 0.60,
    periods_per_year: int = 12,
) -> dict:
    """
    Calculate LTV:CAC ratio and related unit economics.

    Key Metrics:
    - LTV:CAC Ratio = CLV / CAC
    - Payback Period = CAC / (margin × gross_margin)
    - ROI = (CLV - CAC) / CAC

    Args:
        clv: Customer Lifetime Value
        cac: Customer Acquisition Cost
        margin_per_period: Revenue/margin per period
        gross_margin: Gross margin percentage
        periods_per_year: Periods per year

    Returns:
        Dictionary with unit economics metrics
    """
    # LTV:CAC ratio
    ltv_cac_ratio = clv / cac if cac > 0 else float('inf')

    # Payback period (in periods)
    contribution_per_period = margin_per_period * gross_margin
    payback_periods = cac / contribution_per_period if contribution_per_period > 0 else float('inf')
    payback_months = payback_periods if periods_per_year == 12 else payback_periods * (12 / periods_per_year)

    # ROI
    customer_roi = (clv - cac) / cac if cac > 0 else float('inf')

    # Profit per customer
    profit_per_customer = clv - cac

    return {
        "ltv_cac_ratio": round(ltv_cac_ratio, 2),
        "payback_periods": round(payback_periods, 1),
        "payback_months": round(payback_months, 1),
        "customer_roi_percent": round(customer_roi * 100, 1),
        "profit_per_customer": round(profit_per_customer, 2),
        "cac": cac,
        "clv": clv,
        "interpretation": _interpret_ltv_cac(ltv_cac_ratio, payback_months),
    }


def _interpret_ltv_cac(ratio: float, payback_months: float) -> dict:
    """Interpret LTV:CAC metrics."""
    if ratio >= 5.0:
        ratio_assessment = "Excellent - potential underinvestment in growth"
    elif ratio >= 3.0:
        ratio_assessment = "Good - healthy unit economics"
    elif ratio >= 2.0:
        ratio_assessment = "Acceptable - monitor closely"
    elif ratio >= 1.0:
        ratio_assessment = "Poor - barely profitable"
    else:
        ratio_assessment = "Critical - losing money per customer"

    if payback_months <= 6:
        payback_assessment = "Excellent - rapid capital recovery"
    elif payback_months <= 12:
        payback_assessment = "Good - reasonable payback"
    elif payback_months <= 18:
        payback_assessment = "Acceptable - longer capital cycle"
    elif payback_months <= 24:
        payback_assessment = "Poor - significant working capital needs"
    else:
        payback_assessment = "Critical - very long capital cycle"

    return {
        "ltv_cac_assessment": ratio_assessment,
        "payback_assessment": payback_assessment,
        "overall_health": "healthy" if ratio >= 3.0 and payback_months <= 12 else
                          "acceptable" if ratio >= 2.0 and payback_months <= 18 else "concerning",
    }


def analyze_cohort(
    cohort: CohortData,
    margin_per_customer: float,
    discount_rate: float = 0.10,
) -> dict:
    """
    Analyze a customer cohort over time.

    Args:
        cohort: CohortData with retention and revenue by period
        margin_per_customer: Average margin per customer per period
        discount_rate: Annual discount rate

    Returns:
        Cohort analysis dictionary
    """
    periods = len(cohort.retention_by_period)

    analysis = []
    cumulative_revenue = 0
    cumulative_margin = 0

    for t, retention in enumerate(cohort.retention_by_period):
        active_customers = int(cohort.start_customers * retention)
        period_revenue = cohort.revenue_by_period[t] if t < len(cohort.revenue_by_period) else 0
        period_margin = margin_per_customer * active_customers

        # Discount factor (assuming monthly)
        discount_factor = 1 / ((1 + discount_rate / 12) ** t)
        pv_margin = period_margin * discount_factor

        cumulative_revenue += period_revenue
        cumulative_margin += pv_margin

        analysis.append({
            "period": t,
            "retention_rate": round(retention, 4),
            "active_customers": active_customers,
            "churned_customers": cohort.start_customers - active_customers,
            "period_revenue": round(period_revenue, 2),
            "period_margin": round(period_margin, 2),
            "pv_margin": round(pv_margin, 2),
            "cumulative_revenue": round(cumulative_revenue, 2),
            "cumulative_margin": round(cumulative_margin, 2),
        })

    # Calculate cohort CLV
    cohort_clv = cumulative_margin / cohort.start_customers if cohort.start_customers > 0 else 0

    return {
        "cohort_name": cohort.name,
        "start_customers": cohort.start_customers,
        "end_customers": analysis[-1]["active_customers"] if analysis else 0,
        "total_churn_rate": round(1 - analysis[-1]["retention_rate"], 4) if analysis else 0,
        "cohort_clv": round(cohort_clv, 2),
        "total_revenue": round(cumulative_revenue, 2),
        "total_margin_pv": round(cumulative_margin, 2),
        "analysis_by_period": analysis[:12],  # First year
    }


def segment_customers_by_value(
    segments: List[CustomerSegment],
    discount_rate: float = 0.10,
    periods_per_year: int = 12,
) -> dict:
    """
    Analyze customer segments by value contribution.

    Args:
        segments: List of CustomerSegment objects
        discount_rate: Annual discount rate
        periods_per_year: Periods per year

    Returns:
        Segment analysis with value distribution
    """
    segment_analysis = []
    total_customers = sum(s.customer_count for s in segments)
    total_clv = 0

    for seg in segments:
        # Calculate CLV for this segment
        margin = seg.avg_revenue_per_period * seg.avg_gross_margin - seg.variable_cost_per_period
        clv_result = calculate_simple_clv(
            margin_per_period=margin,
            retention_rate=seg.retention_rate,
            discount_rate=discount_rate,
            periods_per_year=periods_per_year,
        )

        segment_clv = clv_result["clv"]
        segment_total_value = segment_clv * seg.customer_count
        total_clv += segment_total_value

        # LTV:CAC
        ltv_cac = segment_clv / seg.acquisition_cost if seg.acquisition_cost > 0 else float('inf')

        segment_analysis.append({
            "segment": seg.name,
            "customer_count": seg.customer_count,
            "customer_share_pct": round(seg.customer_count / total_customers * 100, 1) if total_customers > 0 else 0,
            "avg_revenue": seg.avg_revenue_per_period,
            "gross_margin": round(seg.avg_gross_margin * 100, 1),
            "retention_rate": round(seg.retention_rate * 100, 1),
            "clv": segment_clv,
            "cac": seg.acquisition_cost,
            "ltv_cac_ratio": round(ltv_cac, 2),
            "total_segment_value": round(segment_total_value, 2),
            "expected_lifetime_years": clv_result["expected_lifetime_years"],
        })

    # Calculate value share
    for sa in segment_analysis:
        sa["value_share_pct"] = round(sa["total_segment_value"] / total_clv * 100, 1) if total_clv > 0 else 0

    # Sort by CLV descending
    segment_analysis.sort(key=lambda x: x["clv"], reverse=True)

    # 80/20 analysis
    cumulative_value = 0
    customers_for_80_pct = 0
    for sa in segment_analysis:
        cumulative_value += sa["total_segment_value"]
        customers_for_80_pct += sa["customer_count"]
        if cumulative_value >= total_clv * 0.8:
            break

    return {
        "total_customers": total_customers,
        "total_portfolio_value": round(total_clv, 2),
        "avg_clv": round(total_clv / total_customers, 2) if total_customers > 0 else 0,
        "segments": segment_analysis,
        "pareto_analysis": {
            "customers_for_80_pct_value": customers_for_80_pct,
            "customer_pct_for_80_value": round(customers_for_80_pct / total_customers * 100, 1) if total_customers > 0 else 0,
        },
        "recommendations": _generate_segment_recommendations(segment_analysis),
    }


def _generate_segment_recommendations(segments: List[dict]) -> List[str]:
    """Generate strategic recommendations based on segment analysis."""
    recommendations = []

    # Find high-value, low-acquisition cost segments
    for seg in segments:
        if seg["ltv_cac_ratio"] >= 5.0:
            recommendations.append(
                f"Increase acquisition investment in '{seg['segment']}' - excellent LTV:CAC of {seg['ltv_cac_ratio']}x"
            )
        elif seg["ltv_cac_ratio"] < 2.0 and seg["value_share_pct"] < 20:
            recommendations.append(
                f"Review acquisition strategy for '{seg['segment']}' - marginal LTV:CAC of {seg['ltv_cac_ratio']}x"
            )

        if seg["retention_rate"] < 75 and seg["clv"] > 500:
            recommendations.append(
                f"Focus retention efforts on '{seg['segment']}' - high CLV but {seg['retention_rate']}% retention"
            )

    # General recommendations
    if len(segments) >= 3:
        top_segment = segments[0]
        if top_segment["value_share_pct"] > 50:
            recommendations.append(
                f"High concentration risk: '{top_segment['segment']}' represents {top_segment['value_share_pct']}% of value"
            )

    return recommendations


def calculate_clv_drivers(
    base_clv: float,
    retention_rate: float,
    margin_per_period: float,
    improvement_scenarios: dict = None,
) -> dict:
    """
    Analyze sensitivity of CLV to key drivers.

    Args:
        base_clv: Current CLV
        retention_rate: Current retention rate
        margin_per_period: Current margin per period
        improvement_scenarios: Custom scenarios to test

    Returns:
        CLV driver analysis
    """
    if improvement_scenarios is None:
        improvement_scenarios = {
            "retention_+5pp": {"retention_delta": 0.05},
            "retention_+10pp": {"retention_delta": 0.10},
            "margin_+10%": {"margin_multiplier": 1.10},
            "margin_+20%": {"margin_multiplier": 1.20},
            "combined_5_10": {"retention_delta": 0.05, "margin_multiplier": 1.10},
        }

    scenarios = []

    for name, params in improvement_scenarios.items():
        new_retention = min(0.99, retention_rate + params.get("retention_delta", 0))
        new_margin = margin_per_period * params.get("margin_multiplier", 1.0)

        new_clv_result = calculate_simple_clv(
            margin_per_period=new_margin,
            retention_rate=new_retention,
            discount_rate=0.10,
        )
        new_clv = new_clv_result["clv"]

        clv_increase = new_clv - base_clv
        clv_increase_pct = (clv_increase / base_clv * 100) if base_clv > 0 else 0

        scenarios.append({
            "scenario": name,
            "new_retention": round(new_retention * 100, 1),
            "new_margin": round(new_margin, 2),
            "new_clv": round(new_clv, 2),
            "clv_increase": round(clv_increase, 2),
            "clv_increase_pct": round(clv_increase_pct, 1),
        })

    # Calculate marginal value of 1pp retention improvement
    retention_plus_1pp = calculate_simple_clv(
        margin_per_period=margin_per_period,
        retention_rate=min(0.99, retention_rate + 0.01),
        discount_rate=0.10,
    )["clv"]
    marginal_value_1pp_retention = retention_plus_1pp - base_clv

    return {
        "base_clv": base_clv,
        "base_retention_pct": round(retention_rate * 100, 1),
        "base_margin": margin_per_period,
        "scenarios": scenarios,
        "marginal_value_1pp_retention": round(marginal_value_1pp_retention, 2),
        "key_insight": f"Each 1pp retention improvement adds ${round(marginal_value_1pp_retention, 2)} to CLV",
    }


def benchmark_against_industry(
    clv: float,
    cac: float,
    retention_rate: float,
    payback_months: float,
    industry: str = DEFAULT_INDUSTRY,
) -> dict:
    """
    Benchmark CLV metrics against industry standards.

    Args:
        clv: Customer Lifetime Value
        cac: Customer Acquisition Cost
        retention_rate: Retention rate (0-1)
        payback_months: Payback period in months
        industry: Industry for benchmarking

    Returns:
        Benchmark comparison
    """
    benchmarks = INDUSTRY_BENCHMARKS.get(industry, INDUSTRY_BENCHMARKS[DEFAULT_INDUSTRY])

    ltv_cac = clv / cac if cac > 0 else 0

    def get_rating(value, metric_benchmarks, higher_is_better=True):
        if higher_is_better:
            if value >= metric_benchmarks["excellent"]:
                return "excellent"
            elif value >= metric_benchmarks["good"]:
                return "good"
            elif value >= metric_benchmarks["acceptable"]:
                return "acceptable"
            else:
                return "poor"
        else:  # Lower is better (like payback)
            if value <= metric_benchmarks["excellent"]:
                return "excellent"
            elif value <= metric_benchmarks["good"]:
                return "good"
            elif value <= metric_benchmarks["acceptable"]:
                return "acceptable"
            else:
                return "poor"

    ltv_cac_rating = get_rating(ltv_cac, benchmarks["ltv_cac_ratio"], True)
    retention_rating = get_rating(retention_rate, benchmarks["retention_rate"], True)
    payback_rating = get_rating(payback_months, benchmarks["payback_months"], False)

    return {
        "industry": industry,
        "metrics": {
            "ltv_cac_ratio": {
                "value": round(ltv_cac, 2),
                "rating": ltv_cac_rating,
                "benchmark_good": benchmarks["ltv_cac_ratio"]["good"],
                "benchmark_excellent": benchmarks["ltv_cac_ratio"]["excellent"],
            },
            "retention_rate": {
                "value": round(retention_rate * 100, 1),
                "rating": retention_rating,
                "benchmark_good_pct": round(benchmarks["retention_rate"]["good"] * 100, 1),
                "benchmark_excellent_pct": round(benchmarks["retention_rate"]["excellent"] * 100, 1),
            },
            "payback_months": {
                "value": round(payback_months, 1),
                "rating": payback_rating,
                "benchmark_good": benchmarks["payback_months"]["good"],
                "benchmark_excellent": benchmarks["payback_months"]["excellent"],
            },
        },
        "overall_score": _calculate_overall_score(ltv_cac_rating, retention_rating, payback_rating),
    }


def _calculate_overall_score(ltv_cac_rating: str, retention_rating: str, payback_rating: str) -> dict:
    """Calculate overall score from individual ratings."""
    rating_scores = {"excellent": 4, "good": 3, "acceptable": 2, "poor": 1}

    scores = [
        rating_scores.get(ltv_cac_rating, 1),
        rating_scores.get(retention_rating, 1),
        rating_scores.get(payback_rating, 1),
    ]

    avg_score = sum(scores) / len(scores)

    if avg_score >= 3.5:
        overall = "excellent"
    elif avg_score >= 2.5:
        overall = "good"
    elif avg_score >= 1.5:
        overall = "acceptable"
    else:
        overall = "poor"

    return {
        "rating": overall,
        "score": round(avg_score, 1),
        "max_score": 4,
    }


def analyze_customer_lifetime_value(
    avg_revenue_per_period: float,
    gross_margin: float,
    retention_rate: float,
    cac: float,
    customer_count: int = 1000,
    periods_per_year: int = 12,
    discount_rate: float = 0.10,
    industry: str = DEFAULT_INDUSTRY,
    variable_cost_per_period: float = 0.0,
    run_detailed: bool = True,
    run_benchmarks: bool = True,
    run_drivers: bool = True,
) -> dict:
    """
    Run comprehensive CLV analysis (CLV-1.0 main entry point).

    Args:
        avg_revenue_per_period: Average revenue per customer per period
        gross_margin: Gross margin (0-1)
        retention_rate: Retention rate per period (0-1)
        cac: Customer Acquisition Cost
        customer_count: Total customers for portfolio value
        periods_per_year: Periods per year (12=monthly)
        discount_rate: Annual discount rate
        industry: Industry for benchmarking
        variable_cost_per_period: Variable service cost per period
        run_detailed: Include detailed period analysis
        run_benchmarks: Include industry benchmarking
        run_drivers: Include CLV driver analysis

    Returns:
        Comprehensive CLV analysis dictionary
    """
    # Calculate margin per period
    margin_per_period = avg_revenue_per_period * gross_margin - variable_cost_per_period

    # Simple CLV
    simple_clv = calculate_simple_clv(
        margin_per_period=margin_per_period,
        retention_rate=retention_rate,
        discount_rate=discount_rate,
        periods_per_year=periods_per_year,
    )

    # LTV:CAC metrics
    ltv_cac_metrics = calculate_ltv_cac_metrics(
        clv=simple_clv["clv"],
        cac=cac,
        margin_per_period=avg_revenue_per_period,
        gross_margin=gross_margin,
        periods_per_year=periods_per_year,
    )

    result = {
        "model_id": "CLV-1.0",
        "model_name": "Customer Lifetime Value Model",
        "summary": {
            "clv": simple_clv["clv"],
            "cac": cac,
            "ltv_cac_ratio": ltv_cac_metrics["ltv_cac_ratio"],
            "payback_months": ltv_cac_metrics["payback_months"],
            "profit_per_customer": ltv_cac_metrics["profit_per_customer"],
            "expected_lifetime_years": simple_clv["expected_lifetime_years"],
            "portfolio_value": round(simple_clv["clv"] * customer_count, 2),
        },
        "unit_economics": {
            "revenue_per_period": avg_revenue_per_period,
            "gross_margin_pct": round(gross_margin * 100, 1),
            "margin_per_period": round(margin_per_period, 2),
            "retention_rate_pct": round(retention_rate * 100, 1),
            "annual_churn_rate_pct": round((1 - retention_rate ** periods_per_year) * 100, 1),
        },
        "clv_calculation": simple_clv,
        "ltv_cac_analysis": ltv_cac_metrics,
    }

    # Detailed period analysis
    if run_detailed:
        result["detailed_projection"] = calculate_clv_detailed(
            margin_per_period=margin_per_period,
            retention_rate=retention_rate,
            discount_rate=discount_rate,
            periods=60,
            periods_per_year=periods_per_year,
        )

    # Industry benchmarking
    if run_benchmarks:
        result["industry_benchmark"] = benchmark_against_industry(
            clv=simple_clv["clv"],
            cac=cac,
            retention_rate=retention_rate,
            payback_months=ltv_cac_metrics["payback_months"],
            industry=industry,
        )

    # CLV drivers
    if run_drivers:
        result["clv_drivers"] = calculate_clv_drivers(
            base_clv=simple_clv["clv"],
            retention_rate=retention_rate,
            margin_per_period=margin_per_period,
        )

    return result


# Convenience alias
calculate_clv = analyze_customer_lifetime_value


if __name__ == "__main__":
    # Example: B2B SaaS Company
    print("=" * 60)
    print("CLV-1.0: Customer Lifetime Value Model")
    print("=" * 60)

    result = analyze_customer_lifetime_value(
        avg_revenue_per_period=500,  # $500/month ARPU
        gross_margin=0.75,  # 75% gross margin
        retention_rate=0.97,  # 97% monthly retention (~70% annual)
        cac=2000,  # $2000 CAC
        customer_count=5000,
        industry="saas",
    )

    print(f"\nSummary:")
    print(f"  CLV: ${result['summary']['clv']:,.2f}")
    print(f"  CAC: ${result['summary']['cac']:,.2f}")
    print(f"  LTV:CAC Ratio: {result['summary']['ltv_cac_ratio']:.1f}x")
    print(f"  Payback Period: {result['summary']['payback_months']:.1f} months")
    print(f"  Profit/Customer: ${result['summary']['profit_per_customer']:,.2f}")
    print(f"  Expected Lifetime: {result['summary']['expected_lifetime_years']:.1f} years")
    print(f"  Portfolio Value: ${result['summary']['portfolio_value']:,.0f}")

    print(f"\nUnit Economics:")
    ue = result['unit_economics']
    print(f"  Revenue/Month: ${ue['revenue_per_period']}")
    print(f"  Gross Margin: {ue['gross_margin_pct']}%")
    print(f"  Margin/Month: ${ue['margin_per_period']}")
    print(f"  Monthly Retention: {ue['retention_rate_pct']}%")
    print(f"  Annual Churn: {ue['annual_churn_rate_pct']}%")

    print(f"\nIndustry Benchmark ({result['industry_benchmark']['industry']}):")
    for metric, data in result['industry_benchmark']['metrics'].items():
        print(f"  {metric}: {data['value']} ({data['rating']})")

    print(f"\nCLV Driver Analysis:")
    print(f"  {result['clv_drivers']['key_insight']}")
