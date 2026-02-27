"""
HCM-1.0: Human Capital Model

A comprehensive model for analyzing human capital costs, productivity,
and workforce optimization.

Key Formulas:
- Total Cost per Employee = Salary + Benefits + Overhead + Training
- Revenue per Employee = Total Revenue / FTE
- Turnover Cost = (Separation + Vacancy + Replacement + Training) × Turnover Rate
- Human Capital ROI = (Revenue - (OpEx - Employee Costs)) / Employee Costs
- Productivity Index = Output / (Employee Count × Hours)

Dimensions:
- Cost structure (compensation, benefits, overhead)
- Productivity metrics (revenue/employee, output/hour)
- Turnover analysis (costs, retention strategies)
- Workforce planning (headcount, skills gap)

Version: 1.0.0
Date: 2026-01-16
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import math


@dataclass
class EmployeeCategory:
    """Represents an employee category/level."""
    name: str
    headcount: int
    avg_salary: float
    benefits_rate: float = 0.25  # Benefits as % of salary
    overhead_rate: float = 0.15  # Overhead as % of salary
    avg_tenure_years: float = 3.0
    annual_turnover_rate: float = 0.15
    training_cost_annual: float = 2000
    billable_rate: float = 0.0  # For professional services
    productivity_factor: float = 1.0  # Relative productivity


@dataclass
class Department:
    """Represents a department with its workforce."""
    name: str
    categories: List[EmployeeCategory]
    revenue_attribution: float = 0.0  # Revenue attributed to this dept
    is_revenue_generating: bool = False


# Industry benchmarks for HR metrics
INDUSTRY_HR_BENCHMARKS = {
    "technology": {
        "revenue_per_employee": 400000,
        "turnover_rate": 0.18,
        "benefits_rate": 0.28,
        "training_investment": 2500,
        "hr_to_employee_ratio": 1/80,
    },
    "manufacturing": {
        "revenue_per_employee": 250000,
        "turnover_rate": 0.12,
        "benefits_rate": 0.22,
        "training_investment": 1500,
        "hr_to_employee_ratio": 1/100,
    },
    "professional_services": {
        "revenue_per_employee": 200000,
        "turnover_rate": 0.20,
        "benefits_rate": 0.25,
        "training_investment": 3000,
        "hr_to_employee_ratio": 1/60,
    },
    "retail": {
        "revenue_per_employee": 150000,
        "turnover_rate": 0.40,
        "benefits_rate": 0.18,
        "training_investment": 800,
        "hr_to_employee_ratio": 1/150,
    },
    "healthcare": {
        "revenue_per_employee": 120000,
        "turnover_rate": 0.17,
        "benefits_rate": 0.30,
        "training_investment": 2000,
        "hr_to_employee_ratio": 1/70,
    },
    "financial_services": {
        "revenue_per_employee": 350000,
        "turnover_rate": 0.15,
        "benefits_rate": 0.30,
        "training_investment": 3500,
        "hr_to_employee_ratio": 1/50,
    },
}

# Turnover cost multipliers by role level
TURNOVER_COST_MULTIPLIERS = {
    "entry_level": 0.5,  # 50% of annual salary
    "individual_contributor": 1.0,  # 100% of annual salary
    "senior": 1.5,  # 150% of annual salary
    "manager": 2.0,  # 200% of annual salary
    "director": 2.5,  # 250% of annual salary
    "executive": 3.0,  # 300% of annual salary
}


def calculate_employee_costs(category: EmployeeCategory) -> dict:
    """
    Calculate total cost for an employee category.

    Total Cost = Salary + Benefits + Overhead + Training

    Args:
        category: EmployeeCategory with compensation data

    Returns:
        Dictionary with cost breakdown
    """
    salary = category.avg_salary
    benefits = salary * category.benefits_rate
    overhead = salary * category.overhead_rate
    training = category.training_cost_annual

    total_per_employee = salary + benefits + overhead + training
    total_category = total_per_employee * category.headcount

    return {
        "category": category.name,
        "headcount": category.headcount,
        "per_employee": {
            "salary": round(salary, 2),
            "benefits": round(benefits, 2),
            "overhead": round(overhead, 2),
            "training": round(training, 2),
            "total": round(total_per_employee, 2),
        },
        "category_total": {
            "salary": round(salary * category.headcount, 2),
            "benefits": round(benefits * category.headcount, 2),
            "overhead": round(overhead * category.headcount, 2),
            "training": round(training * category.headcount, 2),
            "total": round(total_category, 2),
        },
        "rates": {
            "benefits_rate_pct": round(category.benefits_rate * 100, 1),
            "overhead_rate_pct": round(category.overhead_rate * 100, 1),
            "fully_loaded_multiplier": round(total_per_employee / salary, 2),
        },
    }


def calculate_turnover_costs(
    category: EmployeeCategory,
    role_level: str = "individual_contributor",
    vacancy_days: float = 45,
    productivity_ramp_months: float = 6,
) -> dict:
    """
    Calculate turnover costs for an employee category.

    Turnover Cost Components:
    - Separation costs (exit interview, admin, severance)
    - Vacancy costs (lost productivity, overtime)
    - Replacement costs (recruiting, hiring)
    - Training/Onboarding costs

    Args:
        category: EmployeeCategory
        role_level: Level for cost multiplier
        vacancy_days: Average days position is vacant
        productivity_ramp_months: Months to full productivity

    Returns:
        Dictionary with turnover cost analysis
    """
    salary = category.avg_salary
    multiplier = TURNOVER_COST_MULTIPLIERS.get(role_level, 1.0)

    # Estimated cost components
    separation_cost = salary * 0.05  # Exit admin, potential severance
    vacancy_cost = (salary / 365) * vacancy_days  # Lost productivity during vacancy
    replacement_cost = salary * 0.30  # Recruiting, screening, interviewing
    onboarding_cost = salary * 0.25  # Training, reduced productivity

    total_turnover_cost = separation_cost + vacancy_cost + replacement_cost + onboarding_cost

    # Alternatively, use multiplier-based estimate
    multiplier_based_cost = salary * multiplier

    # Expected annual turnover count
    expected_turnover = category.headcount * category.annual_turnover_rate

    # Annual turnover cost for this category
    annual_turnover_cost = total_turnover_cost * expected_turnover

    return {
        "category": category.name,
        "role_level": role_level,
        "turnover_rate_pct": round(category.annual_turnover_rate * 100, 1),
        "headcount": category.headcount,
        "expected_annual_turnover": round(expected_turnover, 1),
        "cost_per_turnover": {
            "separation": round(separation_cost, 2),
            "vacancy": round(vacancy_cost, 2),
            "replacement": round(replacement_cost, 2),
            "onboarding": round(onboarding_cost, 2),
            "total_detailed": round(total_turnover_cost, 2),
            "total_multiplier_based": round(multiplier_based_cost, 2),
            "multiplier_used": multiplier,
        },
        "annual_turnover_cost": round(annual_turnover_cost, 2),
        "as_pct_of_payroll": round(
            annual_turnover_cost / (salary * category.headcount) * 100, 1
        ) if category.headcount > 0 else 0,
        "assumptions": {
            "vacancy_days": vacancy_days,
            "productivity_ramp_months": productivity_ramp_months,
        },
    }


def calculate_productivity_metrics(
    total_revenue: float,
    total_employees: int,
    total_labor_cost: float,
    operating_expenses: float,
    billable_employees: int = None,
    billable_hours: float = None,
    total_hours_worked: float = None,
) -> dict:
    """
    Calculate workforce productivity metrics.

    Key Metrics:
    - Revenue per Employee
    - Labor Cost as % of Revenue
    - Human Capital ROI = (Revenue - (OpEx - Labor Cost)) / Labor Cost

    Args:
        total_revenue: Total company revenue
        total_employees: Total FTE count
        total_labor_cost: Total employee costs
        operating_expenses: Total operating expenses
        billable_employees: Number of billable employees (services firms)
        billable_hours: Total billable hours (services firms)
        total_hours_worked: Total hours worked

    Returns:
        Productivity metrics dictionary
    """
    # Basic metrics
    revenue_per_employee = total_revenue / total_employees if total_employees > 0 else 0
    labor_cost_ratio = total_labor_cost / total_revenue if total_revenue > 0 else 0
    cost_per_employee = total_labor_cost / total_employees if total_employees > 0 else 0

    # Human Capital ROI
    # HC ROI = (Revenue - Non-Labor OpEx) / Labor Cost
    non_labor_opex = operating_expenses - total_labor_cost
    hc_value_add = total_revenue - non_labor_opex
    hc_roi = hc_value_add / total_labor_cost if total_labor_cost > 0 else 0

    # Profit per employee
    profit = total_revenue - operating_expenses
    profit_per_employee = profit / total_employees if total_employees > 0 else 0

    result = {
        "revenue_per_employee": round(revenue_per_employee, 2),
        "cost_per_employee": round(cost_per_employee, 2),
        "profit_per_employee": round(profit_per_employee, 2),
        "labor_cost_ratio_pct": round(labor_cost_ratio * 100, 1),
        "human_capital_roi": round(hc_roi, 2),
        "human_capital_roi_pct": round((hc_roi - 1) * 100, 1),  # ROI above cost
        "total_employees": total_employees,
        "total_revenue": total_revenue,
        "total_labor_cost": total_labor_cost,
    }

    # Utilization metrics (for services firms)
    if billable_employees and billable_hours:
        # Assuming 2080 available hours per year (40 hrs × 52 weeks)
        available_hours = billable_employees * 2080
        utilization = billable_hours / available_hours if available_hours > 0 else 0
        revenue_per_billable_hour = total_revenue / billable_hours if billable_hours > 0 else 0

        result["utilization"] = {
            "billable_employees": billable_employees,
            "billable_hours": billable_hours,
            "available_hours": available_hours,
            "utilization_rate_pct": round(utilization * 100, 1),
            "revenue_per_billable_hour": round(revenue_per_billable_hour, 2),
        }

    return result


def analyze_workforce_composition(departments: List[Department]) -> dict:
    """
    Analyze workforce composition across departments.

    Args:
        departments: List of Department objects

    Returns:
        Workforce composition analysis
    """
    total_headcount = 0
    total_cost = 0
    revenue_generating_headcount = 0
    department_analysis = []

    for dept in departments:
        dept_headcount = sum(cat.headcount for cat in dept.categories)
        dept_costs = sum(
            calculate_employee_costs(cat)["category_total"]["total"]
            for cat in dept.categories
        )
        avg_salary = sum(
            cat.avg_salary * cat.headcount for cat in dept.categories
        ) / dept_headcount if dept_headcount > 0 else 0

        total_headcount += dept_headcount
        total_cost += dept_costs

        if dept.is_revenue_generating:
            revenue_generating_headcount += dept_headcount

        # Weighted turnover rate
        weighted_turnover = sum(
            cat.annual_turnover_rate * cat.headcount
            for cat in dept.categories
        ) / dept_headcount if dept_headcount > 0 else 0

        department_analysis.append({
            "department": dept.name,
            "headcount": dept_headcount,
            "total_cost": round(dept_costs, 2),
            "avg_salary": round(avg_salary, 2),
            "avg_cost_per_employee": round(dept_costs / dept_headcount, 2) if dept_headcount > 0 else 0,
            "turnover_rate_pct": round(weighted_turnover * 100, 1),
            "is_revenue_generating": dept.is_revenue_generating,
            "revenue_attribution": dept.revenue_attribution,
            "categories": [
                {
                    "name": cat.name,
                    "headcount": cat.headcount,
                    "avg_salary": cat.avg_salary,
                }
                for cat in dept.categories
            ],
        })

    # Calculate shares
    for da in department_analysis:
        da["headcount_share_pct"] = round(da["headcount"] / total_headcount * 100, 1) if total_headcount > 0 else 0
        da["cost_share_pct"] = round(da["total_cost"] / total_cost * 100, 1) if total_cost > 0 else 0

    # G&A ratio (non-revenue-generating headcount)
    support_headcount = total_headcount - revenue_generating_headcount
    ga_ratio = support_headcount / revenue_generating_headcount if revenue_generating_headcount > 0 else 0

    return {
        "total_headcount": total_headcount,
        "total_cost": round(total_cost, 2),
        "avg_cost_per_employee": round(total_cost / total_headcount, 2) if total_headcount > 0 else 0,
        "revenue_generating_headcount": revenue_generating_headcount,
        "support_headcount": support_headcount,
        "support_ratio": round(ga_ratio, 2),
        "departments": department_analysis,
    }


def calculate_retention_roi(
    turnover_cost_per_employee: float,
    current_turnover_rate: float,
    target_turnover_rate: float,
    headcount: int,
    retention_program_cost: float,
) -> dict:
    """
    Calculate ROI of retention programs.

    Args:
        turnover_cost_per_employee: Cost to replace one employee
        current_turnover_rate: Current annual turnover rate
        target_turnover_rate: Target turnover rate after program
        headcount: Total employee count
        retention_program_cost: Annual cost of retention program

    Returns:
        Retention program ROI analysis
    """
    # Current turnover cost
    current_turnover = headcount * current_turnover_rate
    current_turnover_cost = current_turnover * turnover_cost_per_employee

    # Projected turnover cost
    target_turnover = headcount * target_turnover_rate
    target_turnover_cost = target_turnover * turnover_cost_per_employee

    # Savings
    turnover_reduction = current_turnover - target_turnover
    cost_savings = current_turnover_cost - target_turnover_cost

    # Net benefit and ROI
    net_benefit = cost_savings - retention_program_cost
    roi = net_benefit / retention_program_cost if retention_program_cost > 0 else 0

    # Payback period (months)
    monthly_savings = cost_savings / 12
    payback_months = retention_program_cost / monthly_savings if monthly_savings > 0 else float('inf')

    return {
        "current_state": {
            "turnover_rate_pct": round(current_turnover_rate * 100, 1),
            "expected_turnover": round(current_turnover, 1),
            "annual_turnover_cost": round(current_turnover_cost, 2),
        },
        "target_state": {
            "turnover_rate_pct": round(target_turnover_rate * 100, 1),
            "expected_turnover": round(target_turnover, 1),
            "annual_turnover_cost": round(target_turnover_cost, 2),
        },
        "program_impact": {
            "turnover_reduction": round(turnover_reduction, 1),
            "turnover_reduction_pct": round((current_turnover_rate - target_turnover_rate) / current_turnover_rate * 100, 1) if current_turnover_rate > 0 else 0,
            "cost_savings": round(cost_savings, 2),
        },
        "financials": {
            "retention_program_cost": retention_program_cost,
            "net_benefit": round(net_benefit, 2),
            "roi_pct": round(roi * 100, 1),
            "payback_months": round(payback_months, 1) if payback_months != float('inf') else None,
        },
        "recommendation": "Invest" if roi > 0.5 else "Review" if roi > 0 else "Do not invest",
    }


def project_workforce_needs(
    current_headcount: int,
    revenue_growth_rate: float,
    productivity_improvement_rate: float = 0.02,
    attrition_rate: float = 0.15,
    years: int = 5,
    revenue_per_employee: float = None,
) -> dict:
    """
    Project workforce needs based on growth plans.

    Headcount Growth = Revenue Growth - Productivity Improvement

    Args:
        current_headcount: Current employee count
        revenue_growth_rate: Annual revenue growth rate
        productivity_improvement_rate: Annual productivity improvement
        attrition_rate: Annual voluntary attrition rate
        years: Years to project
        revenue_per_employee: Current revenue per employee

    Returns:
        Workforce projection
    """
    projections = []
    headcount = current_headcount
    cumulative_hires = 0

    for year in range(1, years + 1):
        # Net headcount growth rate
        net_growth_rate = revenue_growth_rate - productivity_improvement_rate

        # Target headcount
        target_headcount = int(headcount * (1 + net_growth_rate))

        # Attrition (backfill needed)
        attrition = int(headcount * attrition_rate)

        # New positions (growth)
        new_positions = target_headcount - headcount

        # Total hires needed
        total_hires = attrition + new_positions
        cumulative_hires += total_hires

        # Revenue per employee (with productivity improvement)
        if revenue_per_employee:
            projected_rev_per_emp = revenue_per_employee * ((1 + productivity_improvement_rate) ** year)
        else:
            projected_rev_per_emp = None

        projections.append({
            "year": year,
            "start_headcount": headcount,
            "target_headcount": target_headcount,
            "attrition": attrition,
            "new_positions": new_positions,
            "total_hires_needed": total_hires,
            "cumulative_hires": cumulative_hires,
            "headcount_growth_pct": round(net_growth_rate * 100, 1),
            "projected_rev_per_employee": round(projected_rev_per_emp, 2) if projected_rev_per_emp else None,
        })

        headcount = target_headcount

    # Hiring velocity (monthly average)
    avg_monthly_hires = cumulative_hires / (years * 12)

    return {
        "current_headcount": current_headcount,
        "final_headcount": projections[-1]["target_headcount"],
        "total_growth": projections[-1]["target_headcount"] - current_headcount,
        "growth_pct": round(
            (projections[-1]["target_headcount"] / current_headcount - 1) * 100, 1
        ),
        "total_hires_needed": cumulative_hires,
        "avg_monthly_hires": round(avg_monthly_hires, 1),
        "projections": projections,
        "assumptions": {
            "revenue_growth_rate_pct": round(revenue_growth_rate * 100, 1),
            "productivity_improvement_pct": round(productivity_improvement_rate * 100, 1),
            "attrition_rate_pct": round(attrition_rate * 100, 1),
        },
    }


def calculate_training_roi(
    training_cost: float,
    participants: int,
    productivity_increase_pct: float,
    avg_salary: float,
    effect_duration_months: int = 12,
) -> dict:
    """
    Calculate ROI of training programs.

    Training ROI = (Productivity Gain Value - Training Cost) / Training Cost

    Args:
        training_cost: Total training program cost
        participants: Number of participants
        productivity_increase_pct: Expected productivity increase (0-1)
        avg_salary: Average salary of participants
        effect_duration_months: How long the effect lasts

    Returns:
        Training ROI analysis
    """
    # Cost per participant
    cost_per_participant = training_cost / participants if participants > 0 else 0

    # Value of productivity increase per employee per month
    # Assume productivity ≈ salary contribution
    monthly_productivity_value = avg_salary / 12
    productivity_gain_value = monthly_productivity_value * productivity_increase_pct

    # Total benefit over effect duration
    benefit_per_employee = productivity_gain_value * effect_duration_months
    total_benefit = benefit_per_employee * participants

    # Net benefit and ROI
    net_benefit = total_benefit - training_cost
    roi = net_benefit / training_cost if training_cost > 0 else 0

    # Break-even time
    monthly_benefit = productivity_gain_value * participants
    break_even_months = training_cost / monthly_benefit if monthly_benefit > 0 else float('inf')

    return {
        "investment": {
            "total_training_cost": training_cost,
            "participants": participants,
            "cost_per_participant": round(cost_per_participant, 2),
        },
        "expected_impact": {
            "productivity_increase_pct": round(productivity_increase_pct * 100, 1),
            "effect_duration_months": effect_duration_months,
            "benefit_per_employee": round(benefit_per_employee, 2),
            "total_benefit": round(total_benefit, 2),
        },
        "financials": {
            "net_benefit": round(net_benefit, 2),
            "roi_pct": round(roi * 100, 1),
            "break_even_months": round(break_even_months, 1) if break_even_months != float('inf') else None,
        },
        "recommendation": "Invest" if roi > 1.0 else "Consider" if roi > 0.5 else "Review",
    }


def benchmark_hr_metrics(
    revenue_per_employee: float,
    turnover_rate: float,
    benefits_rate: float,
    training_investment: float,
    industry: str = "technology",
) -> dict:
    """
    Benchmark HR metrics against industry standards.

    Args:
        revenue_per_employee: Revenue per employee
        turnover_rate: Annual turnover rate
        benefits_rate: Benefits as % of salary
        training_investment: Annual training spend per employee
        industry: Industry for benchmarking

    Returns:
        Benchmark comparison
    """
    benchmarks = INDUSTRY_HR_BENCHMARKS.get(industry, INDUSTRY_HR_BENCHMARKS["technology"])

    def get_rating(value, benchmark, higher_is_better=True):
        ratio = value / benchmark if benchmark > 0 else 0
        if higher_is_better:
            if ratio >= 1.2:
                return "excellent"
            elif ratio >= 0.9:
                return "good"
            elif ratio >= 0.7:
                return "acceptable"
            else:
                return "below_average"
        else:  # Lower is better
            if ratio <= 0.7:
                return "excellent"
            elif ratio <= 0.9:
                return "good"
            elif ratio <= 1.2:
                return "acceptable"
            else:
                return "above_average"

    return {
        "industry": industry,
        "metrics": {
            "revenue_per_employee": {
                "value": revenue_per_employee,
                "benchmark": benchmarks["revenue_per_employee"],
                "vs_benchmark_pct": round(
                    (revenue_per_employee / benchmarks["revenue_per_employee"] - 1) * 100, 1
                ),
                "rating": get_rating(revenue_per_employee, benchmarks["revenue_per_employee"], True),
            },
            "turnover_rate": {
                "value_pct": round(turnover_rate * 100, 1),
                "benchmark_pct": round(benchmarks["turnover_rate"] * 100, 1),
                "vs_benchmark_pp": round((turnover_rate - benchmarks["turnover_rate"]) * 100, 1),
                "rating": get_rating(turnover_rate, benchmarks["turnover_rate"], False),
            },
            "benefits_rate": {
                "value_pct": round(benefits_rate * 100, 1),
                "benchmark_pct": round(benchmarks["benefits_rate"] * 100, 1),
                "rating": get_rating(benefits_rate, benchmarks["benefits_rate"], False),
            },
            "training_investment": {
                "value": training_investment,
                "benchmark": benchmarks["training_investment"],
                "rating": get_rating(training_investment, benchmarks["training_investment"], True),
            },
        },
    }


def analyze_human_capital(
    employee_categories: List[EmployeeCategory],
    total_revenue: float,
    operating_expenses: float,
    industry: str = "technology",
    projection_years: int = 5,
    revenue_growth_rate: float = 0.10,
    run_projections: bool = True,
    run_benchmarks: bool = True,
    run_turnover_analysis: bool = True,
) -> dict:
    """
    Run comprehensive human capital analysis (HCM-1.0 main entry point).

    Args:
        employee_categories: List of EmployeeCategory objects
        total_revenue: Company total revenue
        operating_expenses: Total operating expenses
        industry: Industry for benchmarking
        projection_years: Years for workforce projection
        revenue_growth_rate: Expected revenue growth
        run_projections: Include workforce projections
        run_benchmarks: Include industry benchmarking
        run_turnover_analysis: Include turnover cost analysis

    Returns:
        Comprehensive human capital analysis
    """
    # Calculate costs for each category
    category_costs = [calculate_employee_costs(cat) for cat in employee_categories]

    # Totals
    total_headcount = sum(cat.headcount for cat in employee_categories)
    total_labor_cost = sum(cc["category_total"]["total"] for cc in category_costs)
    total_salary = sum(cc["category_total"]["salary"] for cc in category_costs)
    avg_salary = total_salary / total_headcount if total_headcount > 0 else 0
    avg_benefits_rate = sum(
        cat.benefits_rate * cat.headcount for cat in employee_categories
    ) / total_headcount if total_headcount > 0 else 0
    avg_training = sum(
        cat.training_cost_annual * cat.headcount for cat in employee_categories
    ) / total_headcount if total_headcount > 0 else 0

    # Productivity metrics
    productivity = calculate_productivity_metrics(
        total_revenue=total_revenue,
        total_employees=total_headcount,
        total_labor_cost=total_labor_cost,
        operating_expenses=operating_expenses,
    )

    result = {
        "model_id": "HCM-1.0",
        "model_name": "Human Capital Model",
        "summary": {
            "total_headcount": total_headcount,
            "total_labor_cost": round(total_labor_cost, 2),
            "avg_cost_per_employee": round(total_labor_cost / total_headcount, 2) if total_headcount > 0 else 0,
            "avg_salary": round(avg_salary, 2),
            "labor_cost_ratio_pct": productivity["labor_cost_ratio_pct"],
            "revenue_per_employee": productivity["revenue_per_employee"],
            "human_capital_roi": productivity["human_capital_roi"],
        },
        "cost_breakdown": {
            "total_salary": round(total_salary, 2),
            "total_benefits": round(sum(cc["category_total"]["benefits"] for cc in category_costs), 2),
            "total_overhead": round(sum(cc["category_total"]["overhead"] for cc in category_costs), 2),
            "total_training": round(sum(cc["category_total"]["training"] for cc in category_costs), 2),
        },
        "category_details": category_costs,
        "productivity_metrics": productivity,
    }

    # Turnover analysis
    if run_turnover_analysis:
        turnover_analysis = []
        total_turnover_cost = 0

        for cat in employee_categories:
            # Determine role level based on salary
            if cat.avg_salary >= 200000:
                role_level = "executive"
            elif cat.avg_salary >= 150000:
                role_level = "director"
            elif cat.avg_salary >= 100000:
                role_level = "manager"
            elif cat.avg_salary >= 70000:
                role_level = "senior"
            elif cat.avg_salary >= 50000:
                role_level = "individual_contributor"
            else:
                role_level = "entry_level"

            turnover = calculate_turnover_costs(cat, role_level=role_level)
            turnover_analysis.append(turnover)
            total_turnover_cost += turnover["annual_turnover_cost"]

        result["turnover_analysis"] = {
            "total_annual_turnover_cost": round(total_turnover_cost, 2),
            "turnover_cost_pct_of_payroll": round(total_turnover_cost / total_salary * 100, 1) if total_salary > 0 else 0,
            "by_category": turnover_analysis,
        }

        # Weighted average turnover rate
        avg_turnover = sum(
            cat.annual_turnover_rate * cat.headcount for cat in employee_categories
        ) / total_headcount if total_headcount > 0 else 0
        result["summary"]["avg_turnover_rate_pct"] = round(avg_turnover * 100, 1)

    # Workforce projections
    if run_projections:
        result["workforce_projection"] = project_workforce_needs(
            current_headcount=total_headcount,
            revenue_growth_rate=revenue_growth_rate,
            attrition_rate=avg_turnover if run_turnover_analysis else 0.15,
            years=projection_years,
            revenue_per_employee=productivity["revenue_per_employee"],
        )

    # Industry benchmarking
    if run_benchmarks:
        result["benchmark"] = benchmark_hr_metrics(
            revenue_per_employee=productivity["revenue_per_employee"],
            turnover_rate=avg_turnover if run_turnover_analysis else 0.15,
            benefits_rate=avg_benefits_rate,
            training_investment=avg_training,
            industry=industry,
        )

    return result


# Convenience alias
calculate_human_capital = analyze_human_capital


if __name__ == "__main__":
    # Example: Technology Company
    print("=" * 60)
    print("HCM-1.0: Human Capital Model")
    print("=" * 60)

    # Define employee categories
    categories = [
        EmployeeCategory(
            name="Engineering",
            headcount=150,
            avg_salary=120000,
            benefits_rate=0.28,
            annual_turnover_rate=0.15,
            training_cost_annual=3000,
        ),
        EmployeeCategory(
            name="Sales",
            headcount=50,
            avg_salary=90000,
            benefits_rate=0.25,
            annual_turnover_rate=0.25,
            training_cost_annual=2000,
        ),
        EmployeeCategory(
            name="Marketing",
            headcount=25,
            avg_salary=85000,
            benefits_rate=0.25,
            annual_turnover_rate=0.18,
            training_cost_annual=2500,
        ),
        EmployeeCategory(
            name="G&A",
            headcount=30,
            avg_salary=75000,
            benefits_rate=0.22,
            annual_turnover_rate=0.12,
            training_cost_annual=1500,
        ),
        EmployeeCategory(
            name="Executive",
            headcount=5,
            avg_salary=250000,
            benefits_rate=0.30,
            annual_turnover_rate=0.08,
            training_cost_annual=5000,
        ),
    ]

    result = analyze_human_capital(
        employee_categories=categories,
        total_revenue=100_000_000,  # $100M revenue
        operating_expenses=85_000_000,  # $85M OpEx
        industry="technology",
        revenue_growth_rate=0.15,
    )

    print(f"\nSummary:")
    print(f"  Total Headcount: {result['summary']['total_headcount']}")
    print(f"  Total Labor Cost: ${result['summary']['total_labor_cost']:,.0f}")
    print(f"  Avg Cost/Employee: ${result['summary']['avg_cost_per_employee']:,.0f}")
    print(f"  Revenue/Employee: ${result['summary']['revenue_per_employee']:,.0f}")
    print(f"  Labor Cost Ratio: {result['summary']['labor_cost_ratio_pct']}%")
    print(f"  Human Capital ROI: {result['summary']['human_capital_roi']:.2f}x")

    if "turnover_analysis" in result:
        print(f"\nTurnover:")
        print(f"  Avg Turnover Rate: {result['summary']['avg_turnover_rate_pct']}%")
        print(f"  Annual Turnover Cost: ${result['turnover_analysis']['total_annual_turnover_cost']:,.0f}")
        print(f"  As % of Payroll: {result['turnover_analysis']['turnover_cost_pct_of_payroll']}%")

    if "workforce_projection" in result:
        wp = result['workforce_projection']
        print(f"\nWorkforce Projection (5 years):")
        print(f"  Final Headcount: {wp['final_headcount']}")
        print(f"  Total Growth: {wp['total_growth']} ({wp['growth_pct']}%)")
        print(f"  Total Hires Needed: {wp['total_hires_needed']}")
        print(f"  Avg Monthly Hires: {wp['avg_monthly_hires']}")
