"""
CAC-1.0: Customer Acquisition Cost Model

A comprehensive model for analyzing customer acquisition costs across channels,
optimizing marketing spend, and calculating marketing ROI.

Key Formulas:
- CAC = Total Acquisition Cost / New Customers Acquired
- Blended CAC = Σ(channel_spend) / Σ(channel_customers)
- CAC Payback = CAC / (ARPU × Gross Margin)
- Marketing ROI = (CLV - CAC) / CAC
- Channel Efficiency = Customers Acquired / Channel Spend

Dimensions:
- Channel analysis (paid, organic, referral, sales)
- Funnel metrics (impressions → leads → customers)
- Attribution models (first-touch, last-touch, linear)

Version: 1.0.0
Date: 2026-01-16
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import math


@dataclass
class AcquisitionChannel:
    """Represents an acquisition channel."""
    name: str
    monthly_spend: float
    impressions: int = 0
    clicks: int = 0
    leads: int = 0
    opportunities: int = 0
    customers_acquired: int = 0
    setup_costs: float = 0.0  # One-time setup costs
    overhead_allocation: float = 0.0  # Allocated overhead


@dataclass
class FunnelStage:
    """Represents a funnel stage with conversion metrics."""
    name: str
    volume: int
    conversion_rate_to_next: float = 0.0
    cost_per_unit: float = 0.0
    time_in_stage_days: float = 0.0


# Industry CAC benchmarks
INDUSTRY_CAC_BENCHMARKS = {
    "saas_enterprise": {
        "cac_range": (5000, 25000),
        "cac_payback_months": 18,
        "organic_share": 0.30,
        "sales_cycle_days": 90,
    },
    "saas_smb": {
        "cac_range": (200, 2000),
        "cac_payback_months": 12,
        "organic_share": 0.40,
        "sales_cycle_days": 30,
    },
    "saas_plg": {  # Product-Led Growth
        "cac_range": (50, 500),
        "cac_payback_months": 6,
        "organic_share": 0.60,
        "sales_cycle_days": 14,
    },
    "ecommerce": {
        "cac_range": (10, 100),
        "cac_payback_months": 3,
        "organic_share": 0.35,
        "sales_cycle_days": 1,
    },
    "b2b_services": {
        "cac_range": (1000, 10000),
        "cac_payback_months": 15,
        "organic_share": 0.25,
        "sales_cycle_days": 60,
    },
    "manufacturing": {
        "cac_range": (2000, 20000),
        "cac_payback_months": 24,
        "organic_share": 0.20,
        "sales_cycle_days": 120,
    },
    "financial_services": {
        "cac_range": (100, 5000),
        "cac_payback_months": 12,
        "organic_share": 0.30,
        "sales_cycle_days": 45,
    },
}

# Channel benchmarks (CPM, CTR, conversion rates)
CHANNEL_BENCHMARKS = {
    "google_search": {
        "cpm": 30.0,  # Cost per 1000 impressions
        "ctr": 0.03,  # Click-through rate
        "landing_to_lead": 0.05,  # Landing page to lead
        "lead_to_customer": 0.10,
        "typical_share": 0.25,
    },
    "google_display": {
        "cpm": 3.0,
        "ctr": 0.005,
        "landing_to_lead": 0.02,
        "lead_to_customer": 0.05,
        "typical_share": 0.10,
    },
    "facebook_ads": {
        "cpm": 10.0,
        "ctr": 0.01,
        "landing_to_lead": 0.03,
        "lead_to_customer": 0.08,
        "typical_share": 0.15,
    },
    "linkedin_ads": {
        "cpm": 35.0,
        "ctr": 0.008,
        "landing_to_lead": 0.06,
        "lead_to_customer": 0.15,
        "typical_share": 0.10,
    },
    "content_seo": {
        "cpm": 0.0,  # Organic
        "ctr": 0.02,
        "landing_to_lead": 0.04,
        "lead_to_customer": 0.12,
        "typical_share": 0.20,
    },
    "referral": {
        "cpm": 0.0,
        "ctr": 0.0,
        "landing_to_lead": 0.20,
        "lead_to_customer": 0.25,
        "typical_share": 0.10,
    },
    "direct_sales": {
        "cpm": 0.0,
        "ctr": 0.0,
        "landing_to_lead": 0.0,
        "lead_to_customer": 0.20,
        "typical_share": 0.10,
    },
}


def calculate_channel_cac(channel: AcquisitionChannel) -> dict:
    """
    Calculate CAC metrics for a single acquisition channel.

    Args:
        channel: AcquisitionChannel with spend and acquisition data

    Returns:
        Dictionary with channel CAC metrics
    """
    # Total cost including overhead
    total_cost = channel.monthly_spend + channel.overhead_allocation
    amortized_setup = channel.setup_costs / 12  # Amortize over a year
    total_cost += amortized_setup

    # CAC calculation
    if channel.customers_acquired > 0:
        cac = total_cost / channel.customers_acquired
        cost_per_lead = total_cost / channel.leads if channel.leads > 0 else 0
        cost_per_click = total_cost / channel.clicks if channel.clicks > 0 else 0
    else:
        cac = float('inf')
        cost_per_lead = float('inf') if channel.leads == 0 else total_cost / channel.leads
        cost_per_click = float('inf') if channel.clicks == 0 else total_cost / channel.clicks

    # Funnel metrics
    ctr = channel.clicks / channel.impressions if channel.impressions > 0 else 0
    click_to_lead = channel.leads / channel.clicks if channel.clicks > 0 else 0
    lead_to_opp = channel.opportunities / channel.leads if channel.leads > 0 else 0
    opp_to_customer = channel.customers_acquired / channel.opportunities if channel.opportunities > 0 else 0
    lead_to_customer = channel.customers_acquired / channel.leads if channel.leads > 0 else 0

    return {
        "channel": channel.name,
        "monthly_spend": channel.monthly_spend,
        "total_cost": round(total_cost, 2),
        "customers_acquired": channel.customers_acquired,
        "cac": round(cac, 2) if cac != float('inf') else None,
        "cost_per_lead": round(cost_per_lead, 2) if cost_per_lead != float('inf') else None,
        "cost_per_click": round(cost_per_click, 2) if cost_per_click != float('inf') else None,
        "funnel_metrics": {
            "impressions": channel.impressions,
            "clicks": channel.clicks,
            "leads": channel.leads,
            "opportunities": channel.opportunities,
            "customers": channel.customers_acquired,
            "ctr_pct": round(ctr * 100, 2),
            "click_to_lead_pct": round(click_to_lead * 100, 2),
            "lead_to_opp_pct": round(lead_to_opp * 100, 2),
            "opp_to_customer_pct": round(opp_to_customer * 100, 2),
            "lead_to_customer_pct": round(lead_to_customer * 100, 2),
        },
    }


def calculate_blended_cac(channels: List[AcquisitionChannel], include_organic: bool = True) -> dict:
    """
    Calculate blended CAC across all channels.

    Args:
        channels: List of AcquisitionChannel objects
        include_organic: Include organic/referral channels in calculation

    Returns:
        Dictionary with blended CAC analysis
    """
    channel_results = []
    total_spend = 0
    total_customers = 0
    total_leads = 0
    paid_spend = 0
    paid_customers = 0

    for channel in channels:
        result = calculate_channel_cac(channel)
        channel_results.append(result)

        # Track totals
        total_spend += result["total_cost"]
        total_customers += channel.customers_acquired
        total_leads += channel.leads

        # Track paid vs organic
        if channel.monthly_spend > 0:
            paid_spend += result["total_cost"]
            paid_customers += channel.customers_acquired

    # Blended CAC
    blended_cac = total_spend / total_customers if total_customers > 0 else 0
    paid_cac = paid_spend / paid_customers if paid_customers > 0 else 0
    organic_customers = total_customers - paid_customers
    organic_ratio = organic_customers / total_customers if total_customers > 0 else 0

    # Channel efficiency ranking
    channel_results.sort(key=lambda x: x["cac"] if x["cac"] else float('inf'))

    # Calculate channel contribution
    for cr in channel_results:
        cr["customer_share_pct"] = round(
            cr["customers_acquired"] / total_customers * 100, 1
        ) if total_customers > 0 else 0
        cr["spend_share_pct"] = round(
            cr["total_cost"] / total_spend * 100, 1
        ) if total_spend > 0 else 0

    return {
        "blended_cac": round(blended_cac, 2),
        "paid_cac": round(paid_cac, 2),
        "organic_ratio_pct": round(organic_ratio * 100, 1),
        "total_spend": round(total_spend, 2),
        "total_customers": total_customers,
        "total_leads": total_leads,
        "overall_lead_to_customer": round(total_customers / total_leads * 100, 1) if total_leads > 0 else 0,
        "channels": channel_results,
        "most_efficient_channel": channel_results[0]["channel"] if channel_results else None,
        "least_efficient_channel": channel_results[-1]["channel"] if channel_results else None,
    }


def analyze_funnel(stages: List[FunnelStage]) -> dict:
    """
    Analyze full acquisition funnel from awareness to customer.

    Args:
        stages: List of FunnelStage objects in order

    Returns:
        Funnel analysis dictionary
    """
    funnel_analysis = []
    cumulative_conversion = 1.0

    for i, stage in enumerate(stages):
        cumulative_conversion *= stage.conversion_rate_to_next if i > 0 else 1.0

        stage_cost = stage.volume * stage.cost_per_unit if stage.cost_per_unit > 0 else 0

        funnel_analysis.append({
            "stage": stage.name,
            "volume": stage.volume,
            "conversion_to_next_pct": round(stage.conversion_rate_to_next * 100, 2),
            "cumulative_conversion_pct": round(cumulative_conversion * 100, 4),
            "cost_per_unit": stage.cost_per_unit,
            "stage_total_cost": round(stage_cost, 2),
            "time_in_stage_days": stage.time_in_stage_days,
        })

    # Calculate bottlenecks (lowest conversion rates)
    conversion_rates = [(s.name, s.conversion_rate_to_next) for s in stages[:-1]]
    conversion_rates.sort(key=lambda x: x[1])
    bottlenecks = conversion_rates[:2]  # Top 2 bottlenecks

    # Total funnel time
    total_time = sum(s.time_in_stage_days for s in stages)

    # Cost per final conversion
    final_stage = stages[-1] if stages else None
    total_funnel_cost = sum(s.volume * s.cost_per_unit for s in stages if s.cost_per_unit > 0)
    cost_per_customer = total_funnel_cost / final_stage.volume if final_stage and final_stage.volume > 0 else 0

    return {
        "stages": funnel_analysis,
        "total_stages": len(stages),
        "top_of_funnel": stages[0].volume if stages else 0,
        "bottom_of_funnel": stages[-1].volume if stages else 0,
        "overall_conversion_pct": round(
            (stages[-1].volume / stages[0].volume * 100), 4
        ) if stages and stages[0].volume > 0 else 0,
        "total_funnel_cost": round(total_funnel_cost, 2),
        "cost_per_customer": round(cost_per_customer, 2),
        "total_funnel_time_days": round(total_time, 1),
        "bottlenecks": [{"stage": b[0], "conversion_pct": round(b[1] * 100, 2)} for b in bottlenecks],
    }


def calculate_marketing_roi(
    total_marketing_spend: float,
    customers_acquired: int,
    clv: float,
    gross_margin: float = 0.60,
    attribution_model: str = "last_touch",
) -> dict:
    """
    Calculate marketing ROI metrics.

    Args:
        total_marketing_spend: Total marketing spend
        customers_acquired: New customers acquired
        clv: Customer Lifetime Value
        gross_margin: Gross margin for payback calculation
        attribution_model: Attribution model used

    Returns:
        Marketing ROI metrics
    """
    # CAC
    cac = total_marketing_spend / customers_acquired if customers_acquired > 0 else 0

    # LTV:CAC ratio
    ltv_cac_ratio = clv / cac if cac > 0 else 0

    # Marketing ROI
    total_customer_value = clv * customers_acquired
    marketing_roi = (total_customer_value - total_marketing_spend) / total_marketing_spend if total_marketing_spend > 0 else 0

    # Profit per customer
    profit_per_customer = clv - cac

    # Payback period (assuming monthly revenue)
    # Simplified: assume monthly_revenue = clv / 36 (3-year lifetime)
    monthly_revenue_per_customer = clv / 36
    monthly_contribution = monthly_revenue_per_customer * gross_margin
    payback_months = cac / monthly_contribution if monthly_contribution > 0 else float('inf')

    # ROAS (Return on Ad Spend) - first-year revenue
    first_year_revenue = monthly_revenue_per_customer * 12 * customers_acquired
    roas = first_year_revenue / total_marketing_spend if total_marketing_spend > 0 else 0

    return {
        "cac": round(cac, 2),
        "ltv_cac_ratio": round(ltv_cac_ratio, 2),
        "marketing_roi_pct": round(marketing_roi * 100, 1),
        "total_investment": total_marketing_spend,
        "total_customer_value": round(total_customer_value, 2),
        "net_profit": round(total_customer_value - total_marketing_spend, 2),
        "profit_per_customer": round(profit_per_customer, 2),
        "payback_months": round(payback_months, 1) if payback_months != float('inf') else None,
        "roas": round(roas, 2),
        "attribution_model": attribution_model,
        "interpretation": _interpret_marketing_roi(ltv_cac_ratio, marketing_roi, payback_months),
    }


def _interpret_marketing_roi(ltv_cac: float, roi: float, payback: float) -> dict:
    """Interpret marketing ROI metrics."""
    if ltv_cac >= 5:
        ltv_cac_interpretation = "Excellent - consider increasing marketing investment"
    elif ltv_cac >= 3:
        ltv_cac_interpretation = "Good - healthy unit economics"
    elif ltv_cac >= 2:
        ltv_cac_interpretation = "Acceptable - monitor and optimize"
    elif ltv_cac >= 1:
        ltv_cac_interpretation = "Marginal - needs improvement"
    else:
        ltv_cac_interpretation = "Poor - losing money per customer"

    if roi >= 3:
        roi_interpretation = "Excellent ROI - scale investment"
    elif roi >= 1:
        roi_interpretation = "Good ROI - positive returns"
    elif roi >= 0:
        roi_interpretation = "Break-even - optimize before scaling"
    else:
        roi_interpretation = "Negative ROI - reduce spend or improve efficiency"

    return {
        "ltv_cac": ltv_cac_interpretation,
        "roi": roi_interpretation,
        "overall": "healthy" if ltv_cac >= 3 and roi >= 1 else "needs_attention",
    }


def optimize_channel_mix(
    channels: List[AcquisitionChannel],
    budget_constraint: float,
    target_customers: int = None,
    min_channel_spend: float = 0,
    max_channel_share: float = 0.50,
) -> dict:
    """
    Optimize marketing spend across channels.

    Simple optimization: allocate more budget to lower-CAC channels.

    Args:
        channels: List of channels with current performance
        budget_constraint: Total marketing budget
        target_customers: Target customer acquisition (optional)
        min_channel_spend: Minimum spend per active channel
        max_channel_share: Maximum share for any single channel

    Returns:
        Optimized channel allocation
    """
    # Calculate CAC for each channel
    channel_metrics = []
    for ch in channels:
        metrics = calculate_channel_cac(ch)
        if metrics["cac"] and metrics["cac"] > 0:
            # Estimate capacity (can acquire more at same CAC)
            capacity_multiplier = 1.5  # Assume 50% more capacity
            max_customers = int(ch.customers_acquired * capacity_multiplier)
            channel_metrics.append({
                "channel": ch.name,
                "current_spend": ch.monthly_spend,
                "current_cac": metrics["cac"],
                "current_customers": ch.customers_acquired,
                "max_customers": max_customers,
                "efficiency_score": 1 / metrics["cac"],  # Higher is better
            })

    # Sort by efficiency (lowest CAC first)
    channel_metrics.sort(key=lambda x: x["current_cac"])

    # Allocate budget proportionally to efficiency
    total_efficiency = sum(cm["efficiency_score"] for cm in channel_metrics)

    optimized_allocation = []
    remaining_budget = budget_constraint
    total_expected_customers = 0

    for cm in channel_metrics:
        # Ideal allocation based on efficiency
        ideal_share = cm["efficiency_score"] / total_efficiency if total_efficiency > 0 else 1/len(channel_metrics)

        # Apply constraints
        allocation = budget_constraint * min(ideal_share, max_channel_share)
        allocation = max(allocation, min_channel_spend)
        allocation = min(allocation, remaining_budget)

        # Expected customers at this allocation
        if cm["current_spend"] > 0:
            spend_multiplier = allocation / cm["current_spend"]
            # Diminishing returns - square root scaling
            effective_multiplier = math.sqrt(spend_multiplier) if spend_multiplier > 1 else spend_multiplier
            expected_customers = int(cm["current_customers"] * effective_multiplier)
        else:
            expected_customers = 0

        expected_cac = allocation / expected_customers if expected_customers > 0 else None

        optimized_allocation.append({
            "channel": cm["channel"],
            "current_spend": cm["current_spend"],
            "optimized_spend": round(allocation, 2),
            "spend_change_pct": round((allocation / cm["current_spend"] - 1) * 100, 1) if cm["current_spend"] > 0 else None,
            "current_customers": cm["current_customers"],
            "expected_customers": expected_customers,
            "current_cac": cm["current_cac"],
            "expected_cac": round(expected_cac, 2) if expected_cac else None,
        })

        remaining_budget -= allocation
        total_expected_customers += expected_customers

    # Calculate totals
    current_spend = sum(cm["current_spend"] for cm in channel_metrics)
    current_customers = sum(cm["current_customers"] for cm in channel_metrics)
    current_blended_cac = current_spend / current_customers if current_customers > 0 else 0

    optimized_spend = sum(oa["optimized_spend"] for oa in optimized_allocation)
    optimized_blended_cac = optimized_spend / total_expected_customers if total_expected_customers > 0 else 0

    return {
        "current_state": {
            "total_spend": round(current_spend, 2),
            "total_customers": current_customers,
            "blended_cac": round(current_blended_cac, 2),
        },
        "optimized_state": {
            "total_spend": round(optimized_spend, 2),
            "expected_customers": total_expected_customers,
            "blended_cac": round(optimized_blended_cac, 2),
        },
        "improvement": {
            "customer_increase": total_expected_customers - current_customers,
            "customer_increase_pct": round((total_expected_customers / current_customers - 1) * 100, 1) if current_customers > 0 else 0,
            "cac_reduction": round(current_blended_cac - optimized_blended_cac, 2),
            "cac_reduction_pct": round((1 - optimized_blended_cac / current_blended_cac) * 100, 1) if current_blended_cac > 0 else 0,
        },
        "channel_allocation": optimized_allocation,
        "budget_constraint": budget_constraint,
        "unallocated_budget": round(remaining_budget, 2),
    }


def project_cac_trend(
    historical_cac: List[float],
    months_to_project: int = 12,
    market_saturation_factor: float = 0.02,  # CAC increase due to market saturation
    efficiency_improvement_rate: float = 0.01,  # Annual improvement
) -> dict:
    """
    Project CAC trend over time.

    CAC typically increases due to market saturation but can be offset by efficiency gains.

    Args:
        historical_cac: List of historical CAC values
        months_to_project: Months to project forward
        market_saturation_factor: Monthly CAC increase rate
        efficiency_improvement_rate: Monthly efficiency improvement rate

    Returns:
        CAC trend projection
    """
    if not historical_cac:
        return {"error": "No historical data provided"}

    # Calculate historical trend
    n = len(historical_cac)
    if n >= 2:
        historical_growth = (historical_cac[-1] / historical_cac[0]) ** (1 / (n - 1)) - 1 if historical_cac[0] > 0 else 0
    else:
        historical_growth = 0

    # Net monthly change
    net_monthly_change = market_saturation_factor - efficiency_improvement_rate

    # Project forward
    current_cac = historical_cac[-1]
    projection = []

    for month in range(1, months_to_project + 1):
        projected_cac = current_cac * ((1 + net_monthly_change) ** month)
        projection.append({
            "month": month,
            "projected_cac": round(projected_cac, 2),
            "change_from_current_pct": round((projected_cac / current_cac - 1) * 100, 1),
        })

    return {
        "current_cac": current_cac,
        "historical_monthly_growth_pct": round(historical_growth * 100, 2),
        "market_saturation_factor_pct": round(market_saturation_factor * 100, 2),
        "efficiency_improvement_pct": round(efficiency_improvement_rate * 100, 2),
        "net_monthly_change_pct": round(net_monthly_change * 100, 2),
        "projection": projection,
        "projected_cac_12m": projection[-1]["projected_cac"] if projection else current_cac,
        "projected_change_12m_pct": projection[-1]["change_from_current_pct"] if projection else 0,
    }


def benchmark_cac(
    cac: float,
    industry: str,
    company_stage: str = "growth",  # startup, growth, mature
    go_to_market: str = "hybrid",  # plg, sales-led, marketing-led, hybrid
) -> dict:
    """
    Benchmark CAC against industry standards.

    Args:
        cac: Current CAC
        industry: Industry for benchmark
        company_stage: Company stage
        go_to_market: Go-to-market motion

    Returns:
        Benchmark comparison
    """
    benchmarks = INDUSTRY_CAC_BENCHMARKS.get(industry, INDUSTRY_CAC_BENCHMARKS["b2b_services"])

    cac_min, cac_max = benchmarks["cac_range"]
    cac_mid = (cac_min + cac_max) / 2

    # Adjust for company stage
    stage_multipliers = {"startup": 1.3, "growth": 1.0, "mature": 0.8}
    stage_mult = stage_multipliers.get(company_stage, 1.0)
    adjusted_mid = cac_mid * stage_mult

    # Adjust for GTM
    gtm_multipliers = {"plg": 0.5, "marketing-led": 0.8, "hybrid": 1.0, "sales-led": 1.5}
    gtm_mult = gtm_multipliers.get(go_to_market, 1.0)
    adjusted_mid *= gtm_mult

    # Rating
    if cac <= cac_min:
        rating = "excellent"
    elif cac <= adjusted_mid:
        rating = "good"
    elif cac <= cac_max:
        rating = "acceptable"
    else:
        rating = "high"

    return {
        "your_cac": cac,
        "industry": industry,
        "company_stage": company_stage,
        "go_to_market": go_to_market,
        "benchmark": {
            "range_min": cac_min,
            "range_max": cac_max,
            "adjusted_target": round(adjusted_mid, 2),
        },
        "rating": rating,
        "vs_target_pct": round((cac / adjusted_mid - 1) * 100, 1),
        "typical_payback_months": benchmarks["cac_payback_months"],
        "typical_organic_share_pct": round(benchmarks["organic_share"] * 100, 1),
    }


def analyze_customer_acquisition(
    channels: List[AcquisitionChannel],
    clv: float = None,
    gross_margin: float = 0.60,
    industry: str = "b2b_services",
    budget_constraint: float = None,
    run_optimization: bool = True,
    run_benchmarks: bool = True,
) -> dict:
    """
    Run comprehensive customer acquisition analysis (CAC-1.0 main entry point).

    Args:
        channels: List of AcquisitionChannel objects
        clv: Customer Lifetime Value (for ROI calculations)
        gross_margin: Gross margin percentage
        industry: Industry for benchmarking
        budget_constraint: Budget for optimization
        run_optimization: Run channel optimization
        run_benchmarks: Run industry benchmarking

    Returns:
        Comprehensive CAC analysis dictionary
    """
    # Blended CAC analysis
    blended_analysis = calculate_blended_cac(channels)

    # Total customers and spend
    total_spend = blended_analysis["total_spend"]
    total_customers = blended_analysis["total_customers"]
    blended_cac = blended_analysis["blended_cac"]

    result = {
        "model_id": "CAC-1.0",
        "model_name": "Customer Acquisition Cost Model",
        "summary": {
            "blended_cac": blended_cac,
            "paid_cac": blended_analysis["paid_cac"],
            "organic_ratio_pct": blended_analysis["organic_ratio_pct"],
            "total_marketing_spend": total_spend,
            "total_customers_acquired": total_customers,
            "most_efficient_channel": blended_analysis["most_efficient_channel"],
        },
        "channel_analysis": blended_analysis,
    }

    # Marketing ROI (if CLV provided)
    if clv:
        result["marketing_roi"] = calculate_marketing_roi(
            total_marketing_spend=total_spend,
            customers_acquired=total_customers,
            clv=clv,
            gross_margin=gross_margin,
        )
        result["summary"]["ltv_cac_ratio"] = result["marketing_roi"]["ltv_cac_ratio"]
        result["summary"]["marketing_roi_pct"] = result["marketing_roi"]["marketing_roi_pct"]

    # Channel optimization
    if run_optimization and budget_constraint:
        result["optimization"] = optimize_channel_mix(
            channels=channels,
            budget_constraint=budget_constraint,
        )

    # Industry benchmarking
    if run_benchmarks:
        result["benchmark"] = benchmark_cac(
            cac=blended_cac,
            industry=industry,
        )

    return result


# Convenience alias
calculate_cac = analyze_customer_acquisition


if __name__ == "__main__":
    # Example: B2B SaaS Company
    print("=" * 60)
    print("CAC-1.0: Customer Acquisition Cost Model")
    print("=" * 60)

    # Define acquisition channels
    channels = [
        AcquisitionChannel(
            name="Google Search",
            monthly_spend=50000,
            impressions=500000,
            clicks=15000,
            leads=750,
            opportunities=150,
            customers_acquired=45,
        ),
        AcquisitionChannel(
            name="LinkedIn Ads",
            monthly_spend=30000,
            impressions=200000,
            clicks=1600,
            leads=96,
            opportunities=48,
            customers_acquired=20,
        ),
        AcquisitionChannel(
            name="Content/SEO",
            monthly_spend=10000,  # Content creation costs
            impressions=300000,
            clicks=6000,
            leads=240,
            opportunities=72,
            customers_acquired=35,
        ),
        AcquisitionChannel(
            name="Referral",
            monthly_spend=5000,  # Referral incentives
            impressions=0,
            clicks=0,
            leads=100,
            opportunities=50,
            customers_acquired=25,
        ),
    ]

    result = analyze_customer_acquisition(
        channels=channels,
        clv=5000,  # $5,000 CLV
        gross_margin=0.75,
        industry="saas_smb",
        budget_constraint=100000,
    )

    print(f"\nSummary:")
    print(f"  Blended CAC: ${result['summary']['blended_cac']:,.2f}")
    print(f"  Paid CAC: ${result['summary']['paid_cac']:,.2f}")
    print(f"  Organic Ratio: {result['summary']['organic_ratio_pct']}%")
    print(f"  Total Spend: ${result['summary']['total_marketing_spend']:,.2f}")
    print(f"  Customers Acquired: {result['summary']['total_customers_acquired']}")
    print(f"  Most Efficient: {result['summary']['most_efficient_channel']}")

    if "marketing_roi" in result:
        print(f"\nMarketing ROI:")
        print(f"  LTV:CAC Ratio: {result['summary']['ltv_cac_ratio']:.1f}x")
        print(f"  Marketing ROI: {result['summary']['marketing_roi_pct']}%")
        print(f"  Payback: {result['marketing_roi']['payback_months']} months")

    print(f"\nBenchmark ({result['benchmark']['industry']}):")
    print(f"  Rating: {result['benchmark']['rating']}")
    print(f"  vs Target: {result['benchmark']['vs_target_pct']:+.1f}%")
