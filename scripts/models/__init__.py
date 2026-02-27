"""
Strategic Model Library v4.0

A parametric, config-first model library for strategic planning.

Models included (32 total):

v1.0 Core:
- RPM-1.0: Revenue Projection Model
- MCSM-1.0: Monte Carlo Simulation Model
- OSM-1.0: Organizational Scaling Model
- CAM-1.0: Capital Expenditure Allocation Model

v1.5 Financial:
- CSM-1.0: Cost Structure Model
- PLM-1.0: Profit & Loss Model
- SAM-1.0: Sensitivity Analysis Model

v2.0 Value & Strategy:
- CFM-1.0: Cash Flow Model
- VCM-1.0: Value Creation Model (EVA, ROIC)
- SCM-1.0: Scenario Comparison Model

v2.5 Financial Extended:
- BSM-1.0: Balance Sheet Model
- WCM-1.0: Working Capital Model
- DFM-1.0: Debt & Financing Model
- BEM-1.0: Break-Even Model

v3.0 Strategic:
- MSM-1.0: Market Share Model
- MAM-1.0: M&A Synergy Model
- PFM-1.0: Portfolio Model (BCG Matrix)
- STM-1.0: Stress Testing Model
- PRM-1.0: Pricing Model

v3.1 Planning Process:
- ICM-1.0: Iteration Convergence Model (Optimal Iteration Theory)

v3.2 Risk Framework:
- BFM-1.0: Beta Framework Model (Revenue → Operating → Asset → Equity Beta)

v3.3 Theoretical Foundation:
- FEM-1.0: Fundamental Economics Model (π = p·x - kv·x - Kf + Time Horizons)

v3.4 Capital Markets:
- CMM-1.0: Capital Market Model (Rf, MRP, CRP, Size Premium, WACC)

v3.5 Valuation:
- VAM-1.0: Valuation Model (DCF, Multiples, Football Field)

v4.0 Functional Strategy:
- CLV-1.0: Customer Lifetime Value Model (LTV:CAC, Cohorts, Segmentation)
- CAC-1.0: Customer Acquisition Cost Model (Channels, Funnel, Marketing ROI)
- HCM-1.0: Human Capital Model (Costs, Productivity, Turnover)
- SCO-1.0: Supply Chain Optimization Model (EOQ, Inventory, Suppliers)
- ESG-1.0: ESG Scoring Model (Environmental, Social, Governance)
- RDM-1.0: R&D Investment Model (Pipeline, Patents, Innovation)

Orchestrators:
- STCM-2.0: Strategy Cascade Model
- ISO-1.0: Integrated Strategy Orchestrator (connects all 31 models)

Usage:
    from scripts.models import run_all_models
    results = run_all_models('ALPLA', num_simulations=10000)

    # Or individual models:
    from scripts.models import project_revenue, project_cash_flow
    from scripts.models import load_config

    config = load_config('path/to/config.yaml')
    revenue_df = project_revenue(config)

Version: 4.0.0
Date: 2026-01-16
"""

__version__ = "4.1.0"
__author__ = "FehrAdvice Partners AG"

# Base module exports
from .strategy_base import (
    # Constants
    DEFAULT_BASE_YEAR,
    DEFAULT_PROJECTION_YEARS,
    DEFAULT_CURRENCY,
    MODEL_IDS,

    # Data classes
    ModelConfig,
    ModelResult,

    # Config utilities
    load_config,
    merge_configs,
    get_nested,
    set_nested,
    validate_config,

    # Output utilities
    save_csv,
    save_yaml,
    format_currency,
    format_percent,
    format_number,

    # Calculation utilities
    calculate_cagr,
    project_with_cagr,
    project_with_escalation,
    weighted_average,

    # Time utilities
    get_year_range,
    year_index,
    years_between,

    # Base classes
    StrategyModel,
    ModelRegistry,

    # Formatting
    format_model_header,
    format_section,
    format_key_value,
    format_summary_table,
)

# Model functions (lazy imports to avoid circular dependencies)
def project_revenue(config, **kwargs):
    """Run Revenue Projection Model (RPM-1.0)."""
    from .revenue_projection import project_revenue as _project_revenue
    return _project_revenue(config, **kwargs)


def run_monte_carlo(config, revenue_df=None, num_simulations=10000, **kwargs):
    """Run Monte Carlo Simulation Model (MCSM-1.0)."""
    from .monte_carlo_simulation import run_monte_carlo as _run_monte_carlo
    return _run_monte_carlo(config, revenue_df, num_simulations, **kwargs)


def project_headcount(config, **kwargs):
    """Run Organizational Scaling Model (OSM-1.0)."""
    from .organizational_scaling import project_headcount as _project_headcount
    return _project_headcount(config, **kwargs)


def project_capex(config, **kwargs):
    """Run Capital Expenditure Allocation Model (CAM-1.0)."""
    from .capex_allocation import project_capex as _project_capex
    return _project_capex(config, **kwargs)


def project_costs(config, revenue_projection=None, **kwargs):
    """Run Cost Structure Model (CSM-1.0)."""
    from .cost_structure import project_costs as _project_costs
    return _project_costs(config, revenue_projection, **kwargs)


def project_pnl(config, revenue_projection=None, cost_projection=None, **kwargs):
    """Run Profit & Loss Model (PLM-1.0)."""
    from .profit_loss import project_pnl as _project_pnl
    return _project_pnl(config, revenue_projection, cost_projection, **kwargs)


def run_sensitivity_analysis(config, model_runner=None, output_extractor=None, **kwargs):
    """Run Sensitivity Analysis Model (SAM-1.0)."""
    from .sensitivity_analysis import run_sensitivity_analysis as _run_sensitivity_analysis
    return _run_sensitivity_analysis(config, model_runner, output_extractor, **kwargs)


# v2.0 Models
def project_cash_flow(config, pnl_projection=None, capex_projection=None, **kwargs):
    """Run Cash Flow Model (CFM-1.0)."""
    from .cash_flow import project_cash_flow as _project_cash_flow
    return _project_cash_flow(config, pnl_projection, capex_projection, **kwargs)


def calculate_value_creation(config, pnl_projection=None, cash_flow_projection=None, **kwargs):
    """Run Value Creation Model (VCM-1.0)."""
    from .value_creation import calculate_value_creation as _calculate_value_creation
    return _calculate_value_creation(config, pnl_projection, cash_flow_projection, **kwargs)


def compare_scenarios(config, model_runner=None, custom_scenarios=None, **kwargs):
    """Run Scenario Comparison Model (SCM-1.0)."""
    from .scenario_comparison import compare_scenarios as _compare_scenarios
    return _compare_scenarios(config, model_runner, custom_scenarios, **kwargs)


# v2.5 Financial Extended Models
def project_balance_sheet(config, pnl_projection=None, cash_flow_projection=None, **kwargs):
    """Run Balance Sheet Model (BSM-1.0)."""
    from .balance_sheet import project_balance_sheet as _project_balance_sheet
    return _project_balance_sheet(config, pnl_projection, cash_flow_projection, **kwargs)


def project_working_capital(config, revenue_projection=None, cost_projection=None, **kwargs):
    """Run Working Capital Model (WCM-1.0)."""
    from .working_capital import project_working_capital as _project_working_capital
    return _project_working_capital(config, revenue_projection, cost_projection, **kwargs)


def project_debt_financing(config, cash_flow_projection=None, pnl_projection=None, **kwargs):
    """Run Debt & Financing Model (DFM-1.0)."""
    from .debt_financing import project_debt_financing as _project_debt_financing
    return _project_debt_financing(config, cash_flow_projection, pnl_projection, **kwargs)


def analyze_break_even(config, pnl_projection=None, cost_projection=None, **kwargs):
    """Run Break-Even Model (BEM-1.0)."""
    from .break_even import analyze_break_even as _analyze_break_even
    return _analyze_break_even(config, pnl_projection, cost_projection, **kwargs)


# v3.0 Strategic Models
def project_market_share(config, revenue_projection=None, **kwargs):
    """Run Market Share Model (MSM-1.0)."""
    from .market_share import project_market_share as _project_market_share
    return _project_market_share(config, revenue_projection, **kwargs)


def analyze_ma_synergies(config, **kwargs):
    """Run M&A Synergy Model (MAM-1.0)."""
    from .ma_synergy import analyze_ma_synergies as _analyze_ma_synergies
    return _analyze_ma_synergies(config, **kwargs)


def analyze_portfolio(config, **kwargs):
    """Run Portfolio Model (PFM-1.0) - BCG Matrix Analysis."""
    from .portfolio import analyze_portfolio as _analyze_portfolio
    return _analyze_portfolio(config, **kwargs)


def run_stress_tests(config, pnl_projection=None, **kwargs):
    """Run Stress Testing Model (STM-1.0)."""
    from .stress_testing import run_stress_tests as _run_stress_tests
    return _run_stress_tests(config, pnl_projection, **kwargs)


def analyze_pricing(config, **kwargs):
    """Run Pricing Model (PRM-1.0)."""
    from .pricing import analyze_pricing as _analyze_pricing
    return _analyze_pricing(config, **kwargs)


# v3.1 Planning Process Models
def analyze_iteration_convergence(
    initial_gap_percent: float = 25.0,
    target_gap_percent: float = 5.0,
    data_quality: str = "medium",
    model_complexity: str = "medium",
    organizational_alignment: str = "medium",
    market_volatility: str = "medium",
    planning_horizon: str = "medium",
    cost_per_iteration: float = None,
    benefit_per_percent: float = None,
):
    """
    Run Iteration Convergence Model (ICM-1.0).

    Determines optimal number of planning iterations based on convergence theory.

    Key Formula: G(n) = G₀ · λⁿ
    Optimal: n* = ⌈log(ε/G₀) / log(λ)⌉

    Args:
        initial_gap_percent: Initial gap between top-down and bottom-up (default 25%)
        target_gap_percent: Acceptable gap threshold (default 5%)
        data_quality: "low", "medium", or "high"
        model_complexity: "low", "medium", or "high"
        organizational_alignment: "low", "medium", or "high"
        market_volatility: "low", "medium", or "high"
        planning_horizon: "low" (1-2y), "medium" (3-5y), "high" (5-10y)
        cost_per_iteration: Optional cost per iteration for economic analysis
        benefit_per_percent: Optional benefit per 1% gap reduction

    Returns:
        Dictionary with convergence analysis, optimal iterations, and recommendations
    """
    from .iteration_convergence import analyze_iteration_convergence as _analyze
    return _analyze(
        initial_gap_percent=initial_gap_percent,
        target_gap_percent=target_gap_percent,
        data_quality=data_quality,
        model_complexity=model_complexity,
        organizational_alignment=organizational_alignment,
        market_volatility=market_volatility,
        planning_horizon=planning_horizon,
        cost_per_iteration=cost_per_iteration,
        benefit_per_percent=benefit_per_percent,
    )


# v3.2 Risk Framework Models
def analyze_beta_framework(
    industry: str = "manufacturing",
    geographic_mix: dict = None,
    cyclicality: str = "medium",
    fixed_cost_ratio: float = 0.40,
    debt_to_equity: float = 0.50,
    tax_rate: float = 0.25,
    risk_free_rate: float = 0.035,
    market_risk_premium: float = 0.055,
    cost_of_debt: float = 0.05,
    country_risk_premium: float = 0.0,
    run_sensitivity: bool = True,
):
    """
    Run Beta Framework Model (BFM-1.0).

    Calculates complete beta chain from revenue to equity:
    Revenue Beta → Operating Beta → Asset Beta → Equity Beta

    Key Formulas:
    - Operating Beta: β_Op = β_R × DOL
    - Equity Beta (Hamada): β_E = β_A × [1 + (1-t) × (D/E)]
    - Cost of Equity: Re = Rf + β_E × MRP
    - WACC: (E/V) × Re + (D/V) × Rd × (1-t)

    Args:
        industry: Industry type (packaging_plastics, manufacturing, etc.)
        geographic_mix: Dict of geography -> revenue share
        cyclicality: "low", "medium", or "high"
        fixed_cost_ratio: Fixed costs / Total costs (0-1)
        debt_to_equity: D/E ratio
        tax_rate: Corporate tax rate
        risk_free_rate: Risk-free rate
        market_risk_premium: Market risk premium
        cost_of_debt: Pre-tax cost of debt
        country_risk_premium: Additional country risk
        run_sensitivity: Run sensitivity scenarios

    Returns:
        Dictionary with beta chain, cost of capital, and sensitivity analysis
    """
    from .beta_framework import analyze_beta_framework as _analyze
    return _analyze(
        industry=industry,
        geographic_mix=geographic_mix,
        cyclicality=cyclicality,
        fixed_cost_ratio=fixed_cost_ratio,
        debt_to_equity=debt_to_equity,
        tax_rate=tax_rate,
        risk_free_rate=risk_free_rate,
        market_risk_premium=market_risk_premium,
        cost_of_debt=cost_of_debt,
        country_risk_premium=country_risk_premium,
        run_sensitivity=run_sensitivity,
    )


# v3.3 Theoretical Foundation Models
def analyze_fundamental_economics(
    price: float,
    quantity: float,
    variable_cost_per_unit: float,
    fixed_costs: float,
    debt: float = 0,
    equity: float = 0,
    invested_capital: float = None,
    tax_rate: float = 0.25,
    revenue_beta: float = 0.8,
    risk_free_rate: float = 0.035,
    market_risk_premium: float = 0.055,
    cost_of_debt: float = 0.05,
    include_beta_analysis: bool = True,
    include_wacc_analysis: bool = True,
    include_leverage_scenarios: bool = True,
    include_time_horizon_analysis: bool = True,
    scale_elasticity: float = 0.85,
):
    """
    Run Fundamental Economics Model (FEM-1.0).

    Core equation: π = p·x - kv·x - Kf

    Includes:
    - Time horizons: instant/short/medium/long-term
    - Beta chain: β_R → β_Op → β_A → β_E
    - WACC (Kapitalkosten): (E/V)×Re + (D/V)×Rd×(1-t)
    - Value Creation: ROIC, EVA, Spread

    Args:
        price: Price per unit (p)
        quantity: Quantity sold (x)
        variable_cost_per_unit: Variable cost per unit (kv)
        fixed_costs: Total fixed costs (Kf)
        debt: Total debt / Fremdkapital (D)
        equity: Total equity / Eigenkapital (E)
        invested_capital: Invested capital (if None, uses D + E)
        tax_rate: Corporate tax rate (t)
        revenue_beta: Base revenue beta (β_R)
        risk_free_rate: Risk-free rate (Rf)
        market_risk_premium: Market risk premium (MRP)
        cost_of_debt: Pre-tax cost of debt (Rd)
        include_beta_analysis: Calculate beta chain from DOL
        include_wacc_analysis: Calculate WACC and value creation
        include_leverage_scenarios: Calculate leverage scenarios
        include_time_horizon_analysis: Calculate by time horizon
        scale_elasticity: Long-run scale elasticity (< 1 = economies of scale)

    Returns:
        Complete fundamental economics analysis with WACC and EVA
    """
    from .fundamental_economics import analyze_fundamental_economics as _analyze
    return _analyze(
        price=price,
        quantity=quantity,
        variable_cost_per_unit=variable_cost_per_unit,
        fixed_costs=fixed_costs,
        debt=debt,
        equity=equity,
        invested_capital=invested_capital,
        tax_rate=tax_rate,
        revenue_beta=revenue_beta,
        risk_free_rate=risk_free_rate,
        market_risk_premium=market_risk_premium,
        cost_of_debt=cost_of_debt,
        include_beta_analysis=include_beta_analysis,
        include_wacc_analysis=include_wacc_analysis,
        include_leverage_scenarios=include_leverage_scenarios,
        include_time_horizon_analysis=include_time_horizon_analysis,
        scale_elasticity=scale_elasticity,
    )


# v3.4 Capital Markets Models
def analyze_capital_markets(
    equity_beta: float = 1.0,
    debt_to_equity: float = 0.5,
    tax_rate: float = 0.25,
    currency: str = "EUR",
    country: str = None,
    region: str = None,
    company_size: str = None,
    market_cap_millions: float = None,
    is_public: bool = True,
    is_liquid: bool = True,
    credit_rating: str = "BBB",
    company_specific_premium: float = 0.0,
    show_benchmarks: bool = True,
):
    """
    Run Capital Market Model (CMM-1.0) - Kapitalmarkt-Modul.

    Provides all capital market parameters for WACC calculation:
    - Risk-Free Rate (Rf) by currency
    - Market Risk Premium (MRP)
    - Country Risk Premium (CRP)
    - Size Premium (SP)
    - Illiquidity Premium (IP)
    - Credit Spreads by rating

    Cost of Equity: Re = Rf + β×MRP + CRP + SP + IP + CSP
    Cost of Debt: Rd = Rf + Credit Spread
    WACC: (E/V)×Re + (D/V)×Rd×(1-t)

    Args:
        equity_beta: Equity beta (β_E)
        debt_to_equity: D/E ratio
        tax_rate: Corporate tax rate
        currency: "EUR", "USD", "CHF", "GBP"
        country: Country name (e.g., "germany", "brazil")
        region: Region if country not specified
        company_size: "mega_cap" to "private"
        market_cap_millions: Market cap in millions
        is_public: Is company publicly traded?
        is_liquid: Are shares liquid?
        credit_rating: "AAA" to "CCC"
        company_specific_premium: Additional risk premium
        show_benchmarks: Include market benchmarks

    Returns:
        Complete capital market analysis with WACC
    """
    from .capital_market import analyze_capital_markets as _analyze
    return _analyze(
        equity_beta=equity_beta,
        debt_to_equity=debt_to_equity,
        tax_rate=tax_rate,
        currency=currency,
        country=country,
        region=region,
        company_size=company_size,
        market_cap_millions=market_cap_millions,
        is_public=is_public,
        is_liquid=is_liquid,
        credit_rating=credit_rating,
        company_specific_premium=company_specific_premium,
        show_benchmarks=show_benchmarks,
    )


# v3.5 Valuation Models
def run_valuation(
    revenue: float,
    ebitda: float,
    ebit: float,
    net_income: float,
    depreciation: float,
    capex: float,
    change_in_nwc: float,
    net_debt: float = 0,
    book_equity: float = None,
    wacc: float = 0.10,
    terminal_growth_rate: float = 0.02,
    revenue_growth_rates: list = None,
    ebitda_margin: float = None,
    projection_years: int = 5,
    terminal_method: str = "gordon_growth",
    exit_multiple: float = None,
    industry: str = "manufacturing",
    custom_multiples: dict = None,
    tax_rate: float = 0.25,
):
    """
    Run Valuation Model (VAM-1.0) - Unternehmensbewertung.

    Comprehensive company valuation using:
    1. DCF (Discounted Cash Flow) - Gordon Growth or Exit Multiple
    2. Trading Multiples (EV/EBITDA, EV/EBIT, EV/Sales, P/E)
    3. Football Field chart data

    DCF Formula:
        EV = Σ(FCF_t / (1+WACC)^t) + TV / (1+WACC)^n
        Equity = EV - Net Debt

    Args:
        revenue: Current year revenue
        ebitda: Current year EBITDA
        ebit: Current year EBIT
        net_income: Current year Net Income
        depreciation: Depreciation & Amortization
        capex: Capital Expenditures
        change_in_nwc: Change in Net Working Capital
        net_debt: Net Debt (Debt - Cash)
        book_equity: Book Value of Equity
        wacc: Weighted Average Cost of Capital
        terminal_growth_rate: Long-term growth rate
        revenue_growth_rates: Growth rates per year
        ebitda_margin: EBITDA margin
        projection_years: Number of projection years
        terminal_method: "gordon_growth" or "exit_multiple"
        exit_multiple: Exit EV/EBITDA multiple
        industry: Industry for benchmark multiples
        custom_multiples: Custom multiples override
        tax_rate: Corporate tax rate

    Returns:
        Complete valuation with DCF, Multiples, and Football Field
    """
    from .valuation import run_valuation as _run_valuation
    return _run_valuation(
        revenue=revenue,
        ebitda=ebitda,
        ebit=ebit,
        net_income=net_income,
        depreciation=depreciation,
        capex=capex,
        change_in_nwc=change_in_nwc,
        net_debt=net_debt,
        book_equity=book_equity,
        wacc=wacc,
        terminal_growth_rate=terminal_growth_rate,
        revenue_growth_rates=revenue_growth_rates,
        ebitda_margin=ebitda_margin,
        projection_years=projection_years,
        terminal_method=terminal_method,
        exit_multiple=exit_multiple,
        industry=industry,
        custom_multiples=custom_multiples,
        tax_rate=tax_rate,
    )


# v4.0 Functional Strategy Models
def analyze_customer_lifetime_value(
    avg_revenue_per_period: float,
    gross_margin: float,
    retention_rate: float,
    cac: float,
    customer_count: int = 1000,
    periods_per_year: int = 12,
    discount_rate: float = 0.10,
    industry: str = "b2b_services",
    variable_cost_per_period: float = 0.0,
    run_detailed: bool = True,
    run_benchmarks: bool = True,
    run_drivers: bool = True,
):
    """
    Run Customer Lifetime Value Model (CLV-1.0).

    Calculates CLV, LTV:CAC ratio, cohort analysis, and customer segmentation.

    Key Formulas:
    - CLV = Σ(margin × retention_rate^t / (1+discount_rate)^t)
    - LTV:CAC Ratio = CLV / CAC
    - Payback Period = CAC / (margin × gross_margin)

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
    from .customer_lifetime_value import analyze_customer_lifetime_value as _analyze
    return _analyze(
        avg_revenue_per_period=avg_revenue_per_period,
        gross_margin=gross_margin,
        retention_rate=retention_rate,
        cac=cac,
        customer_count=customer_count,
        periods_per_year=periods_per_year,
        discount_rate=discount_rate,
        industry=industry,
        variable_cost_per_period=variable_cost_per_period,
        run_detailed=run_detailed,
        run_benchmarks=run_benchmarks,
        run_drivers=run_drivers,
    )


def analyze_customer_acquisition(
    channels,
    clv: float = None,
    gross_margin: float = 0.60,
    industry: str = "b2b_services",
    budget_constraint: float = None,
    run_optimization: bool = True,
    run_benchmarks: bool = True,
):
    """
    Run Customer Acquisition Cost Model (CAC-1.0).

    Analyzes acquisition costs across channels, funnel metrics, and marketing ROI.

    Key Formulas:
    - CAC = Total Acquisition Cost / New Customers Acquired
    - Blended CAC = Σ(channel_spend) / Σ(channel_customers)
    - Marketing ROI = (CLV - CAC) / CAC

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
    from .customer_acquisition import analyze_customer_acquisition as _analyze
    return _analyze(
        channels=channels,
        clv=clv,
        gross_margin=gross_margin,
        industry=industry,
        budget_constraint=budget_constraint,
        run_optimization=run_optimization,
        run_benchmarks=run_benchmarks,
    )


def analyze_human_capital(
    employee_categories,
    total_revenue: float,
    operating_expenses: float,
    industry: str = "technology",
    projection_years: int = 5,
    revenue_growth_rate: float = 0.10,
    run_projections: bool = True,
    run_benchmarks: bool = True,
    run_turnover_analysis: bool = True,
):
    """
    Run Human Capital Model (HCM-1.0).

    Analyzes workforce costs, productivity, turnover, and workforce planning.

    Key Formulas:
    - Total Cost per Employee = Salary + Benefits + Overhead + Training
    - Revenue per Employee = Total Revenue / FTE
    - Turnover Cost = (Separation + Vacancy + Replacement + Training) × Turnover Rate
    - Human Capital ROI = (Revenue - (OpEx - Employee Costs)) / Employee Costs

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
    from .human_capital import analyze_human_capital as _analyze
    return _analyze(
        employee_categories=employee_categories,
        total_revenue=total_revenue,
        operating_expenses=operating_expenses,
        industry=industry,
        projection_years=projection_years,
        revenue_growth_rate=revenue_growth_rate,
        run_projections=run_projections,
        run_benchmarks=run_benchmarks,
        run_turnover_analysis=run_turnover_analysis,
    )


def analyze_supply_chain(
    inventory_items=None,
    suppliers=None,
    total_cogs: float = None,
    avg_inventory_value: float = None,
    total_orders: int = None,
    perfect_orders: int = None,
    fill_rate: float = None,
    days_receivable: float = 45,
    days_payable: float = 30,
    industry: str = "manufacturing",
    capital_constraint: float = None,
    run_optimization: bool = True,
    run_benchmarks: bool = True,
    run_risk_analysis: bool = True,
):
    """
    Run Supply Chain Optimization Model (SCO-1.0).

    Analyzes inventory, suppliers, and supply chain efficiency.

    Key Formulas:
    - EOQ = √(2×D×S / H)
    - Safety Stock = z × σ_d × √L
    - Inventory Turns = COGS / Avg Inventory
    - Cash-to-Cash = Days Inventory + Days Receivable - Days Payable

    Args:
        inventory_items: List of InventoryItem objects
        suppliers: List of Supplier objects
        total_cogs: Total cost of goods sold
        avg_inventory_value: Average inventory value
        total_orders: Total orders
        perfect_orders: Perfect orders
        fill_rate: Fill rate (if order lines not available)
        days_receivable: Days sales outstanding
        days_payable: Days payable outstanding
        industry: Industry for benchmarking
        capital_constraint: Working capital constraint
        run_optimization: Run inventory optimization
        run_benchmarks: Run industry benchmarking
        run_risk_analysis: Run risk analysis

    Returns:
        Comprehensive supply chain analysis
    """
    from .supply_chain import analyze_supply_chain as _analyze
    return _analyze(
        inventory_items=inventory_items,
        suppliers=suppliers,
        total_cogs=total_cogs,
        avg_inventory_value=avg_inventory_value,
        total_orders=total_orders,
        perfect_orders=perfect_orders,
        fill_rate=fill_rate,
        days_receivable=days_receivable,
        days_payable=days_payable,
        industry=industry,
        capital_constraint=capital_constraint,
        run_optimization=run_optimization,
        run_benchmarks=run_benchmarks,
        run_risk_analysis=run_risk_analysis,
    )


def analyze_esg(
    environmental,
    social,
    governance,
    revenue_millions: float,
    industry: str = "manufacturing",
    run_projections: bool = True,
    run_benchmarks: bool = True,
    identify_priorities: bool = True,
):
    """
    Run ESG Scoring Model (ESG-1.0).

    Calculates Environmental, Social, and Governance scores with industry benchmarking.

    Scoring:
    - Individual metrics: 0-100 scale
    - Pillar scores: Weighted average of metrics
    - Overall ESG score: E:35% + S:35% + G:30%
    - Rating: AAA to CCC

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
    from .esg_scoring import analyze_esg as _analyze
    return _analyze(
        environmental=environmental,
        social=social,
        governance=governance,
        revenue_millions=revenue_millions,
        industry=industry,
        run_projections=run_projections,
        run_benchmarks=run_benchmarks,
        identify_priorities=identify_priorities,
    )


def analyze_rd_investment(
    rd_spend: float,
    revenue: float,
    projects=None,
    patent_portfolio=None,
    new_product_revenue: float = None,
    rd_spend_historical=None,
    patents_filed: int = 0,
    products_launched: int = 0,
    rd_headcount: int = None,
    industry: str = "technology",
    run_pipeline_analysis: bool = True,
    run_roi_analysis: bool = True,
    run_benchmarks: bool = True,
):
    """
    Run R&D Investment Model (RDM-1.0).

    Analyzes R&D investments, innovation pipeline, and research productivity.

    Key Formulas:
    - R&D Intensity = R&D Spend / Revenue
    - R&D ROI = (Revenue from New Products - R&D Cost) / R&D Cost
    - Pipeline Value = Σ(Project NPV × Success Probability)
    - Innovation Rate = New Product Revenue / Total Revenue

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
    from .rd_investment import analyze_rd_investment as _analyze
    return _analyze(
        rd_spend=rd_spend,
        revenue=revenue,
        projects=projects,
        patent_portfolio=patent_portfolio,
        new_product_revenue=new_product_revenue,
        rd_spend_historical=rd_spend_historical,
        patents_filed=patents_filed,
        products_launched=products_launched,
        rd_headcount=rd_headcount,
        industry=industry,
        run_pipeline_analysis=run_pipeline_analysis,
        run_roi_analysis=run_roi_analysis,
        run_benchmarks=run_benchmarks,
    )


def run_strategy_cascade(config, scenario=None, strategic_override=None,
                         cascade_mode='full', num_simulations=10000, verbose=True):
    """
    Run Strategy Cascade Model (STCM-1.0) with top-down planning.

    Args:
        config: Configuration dictionary
        scenario: Scenario name ('conservative', 'base_case', 'aggressive')
        strategic_override: Optional strategic overrides dict
        cascade_mode: 'full' (all 7 levels) or 'quick' (skip Level 7)
        num_simulations: Monte Carlo simulations for Level 7
        verbose: Print progress

    Returns:
        Dictionary with cascade results, dependencies, and validation
    """
    from .strategy_cascade import run_strategy_cascade as _run_strategy_cascade
    return _run_strategy_cascade(
        config=config,
        scenario=scenario,
        strategic_override=strategic_override,
        cascade_mode=cascade_mode,
        num_simulations=num_simulations,
        verbose=verbose
    )


def run_all_models(customer_name, output_dir=None, num_simulations=10000,
                   verbose=True, run_sensitivity=False, run_scenarios=False):
    """
    Run all 10 strategic models (v2.0) for a customer.

    Args:
        customer_name: Name of customer (e.g., 'ALPLA')
        output_dir: Directory to save outputs (optional)
        num_simulations: Number of Monte Carlo simulations
        verbose: Print progress and results
        run_sensitivity: Run SAM-1.0 sensitivity analysis (optional)
        run_scenarios: Run SCM-1.0 scenario comparison (optional)

    Returns:
        Dictionary with all model results
    """
    from .apply_all_models import run_all_models as _run_all_models
    return _run_all_models(
        customer_name=customer_name,
        output_dir=output_dir,
        num_simulations=num_simulations,
        verbose=verbose,
        run_sensitivity=run_sensitivity,
        run_scenarios=run_scenarios
    )


# ISO-1.0: Integrated Strategy Orchestrator
def run_integrated_strategy(
    company_name: str,
    base_revenue: float,
    industry: str = "manufacturing",
    **kwargs
):
    """
    Run Integrated Strategy Orchestrator (ISO-1.0).

    Connects all 31 strategic models with automatic data flow:

    Layer 1 (Functional Strategy):
    - CLV-1.0, CAC-1.0, HCM-1.0, SCO-1.0, RDM-1.0, ESG-1.0

    Layer 2 (Theoretical Foundation):
    - FEM-1.0, BFM-1.0, CMM-1.0

    Layer 3 (Valuation):
    - VAM-1.0

    Data Flow:
        CLV → CAC (LTV:CAC calculation)
        HCM → CSM (Personnel costs)
        SCO → WCM (Inventory)
        ESG → CMM (Risk premium)
        BFM → CMM → VAM (Beta → WACC → Valuation)

    Args:
        company_name: Company name
        base_revenue: Base year revenue
        industry: Industry type (manufacturing, technology, etc.)
        **kwargs: Additional OrchestratorConfig parameters:
            - gross_margin: Gross margin (0-1)
            - operating_margin: Operating margin (0-1)
            - customer_count: Number of customers
            - avg_revenue_per_customer: Average revenue per customer
            - total_employees: Total employee count
            - avg_salary: Average salary
            - total_debt: Total debt
            - total_equity: Total equity
            - tax_rate: Corporate tax rate
            - rd_intensity: R&D as % of revenue

    Returns:
        Dictionary with integrated results from all models:
        - Customer economics (CLV, CAC, LTV:CAC)
        - Operational efficiency (revenue/employee, inventory turns)
        - Innovation & sustainability (R&D intensity, ESG rating)
        - Cost of capital (beta, WACC)
        - Valuation (enterprise value, equity value)
    """
    from .integrated_strategy_orchestrator import run_integrated_strategy as _run
    return _run(
        company_name=company_name,
        base_revenue=base_revenue,
        industry=industry,
        **kwargs
    )


# All public exports
__all__ = [
    # Version info
    '__version__',
    '__author__',

    # Base module
    'DEFAULT_BASE_YEAR',
    'DEFAULT_PROJECTION_YEARS',
    'DEFAULT_CURRENCY',
    'MODEL_IDS',
    'ModelConfig',
    'ModelResult',
    'load_config',
    'merge_configs',
    'get_nested',
    'set_nested',
    'validate_config',
    'save_csv',
    'save_yaml',
    'format_currency',
    'format_percent',
    'format_number',
    'calculate_cagr',
    'project_with_cagr',
    'project_with_escalation',
    'weighted_average',
    'get_year_range',
    'year_index',
    'years_between',
    'StrategyModel',
    'ModelRegistry',
    'format_model_header',
    'format_section',
    'format_key_value',
    'format_summary_table',

    # Model functions (v1.0-v1.5)
    'project_revenue',
    'run_monte_carlo',
    'project_headcount',
    'project_capex',
    'project_costs',
    'project_pnl',
    'run_sensitivity_analysis',

    # Model functions (v2.0)
    'project_cash_flow',
    'calculate_value_creation',
    'compare_scenarios',

    # Model functions (v2.5 Financial Extended)
    'project_balance_sheet',
    'project_working_capital',
    'project_debt_financing',
    'analyze_break_even',

    # Model functions (v3.0 Strategic)
    'project_market_share',
    'analyze_ma_synergies',
    'analyze_portfolio',
    'run_stress_tests',
    'analyze_pricing',

    # Model functions (v3.1 Planning Process)
    'analyze_iteration_convergence',

    # Model functions (v3.2 Risk Framework)
    'analyze_beta_framework',

    # Model functions (v3.3 Theoretical Foundation)
    'analyze_fundamental_economics',

    # Model functions (v3.4 Capital Markets)
    'analyze_capital_markets',

    # Model functions (v3.5 Valuation)
    'run_valuation',

    # Model functions (v4.0 Functional Strategy)
    'analyze_customer_lifetime_value',
    'analyze_customer_acquisition',
    'analyze_human_capital',
    'analyze_supply_chain',
    'analyze_esg',
    'analyze_rd_investment',

    # Strategy Cascade (STCM-2.0)
    'run_strategy_cascade',

    # Orchestrators
    'run_all_models',
    'run_integrated_strategy',
]
