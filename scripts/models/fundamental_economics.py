"""
FEM-1.0: Fundamental Economics Model

Core Economic Relationships for Strategic Planning

This model formalizes the fundamental economic equations that underlie
ALL other strategic models. Every model in the library derives from
these basic relationships.

=============================================================================
TIME HORIZONS (Zeithorizonte)
=============================================================================

                    Instant      Short-Term   Medium-Term   Long-Term
                    (Sofort)     (Kurzfristig) (Mittelfristig) (Langfristig)
                    < 1 Month    1-12 Months   1-5 Years     > 5 Years
    ──────────────────────────────────────────────────────────────────────
    Price (p)       Variable     Variable      Variable      Variable
    Quantity (x)    Fixed¹       Variable      Variable      Variable
    Variable Cost   Fixed        Variable      Variable      Variable
    (kv)
    Fixed Costs     Fixed        Fixed         Step-Variable All Variable
    (Kf)
    Capacity        Fixed        Fixed         Adjustable    Fully Flexible
    Technology      Fixed        Fixed         Fixed         Variable

    ¹ Inventory adjustment possible

Key Implications:
- INSTANT: Only p can change → Price elasticity matters most
- SHORT-TERM: Standard π = p·x - kv·x - Kf equation applies
- MEDIUM-TERM: Kf becomes "stepped" → Capacity decisions matter
- LONG-TERM: All costs variable → Scale economies dominate

Beta Implications by Horizon:
- SHORT-TERM: High DOL (fixed costs locked) → High β_Op
- LONG-TERM: All costs adjust → DOL → 1 → β_Op ≈ β_R

=============================================================================
FUNDAMENTAL EQUATION
=============================================================================

    π = p·x - kv·x - Kf

Where:
    π   = Profit (Gewinn)
    p   = Price per unit (Preis)
    x   = Quantity sold (Menge)
    kv  = Variable cost per unit (variable Stückkosten)
    Kf  = Total fixed costs (Fixkosten)

Equivalent forms:
    π = (p - kv)·x - Kf           [Contribution Margin form]
    π = CM·x - Kf                  [where CM = Contribution Margin per unit]
    π = Revenue - VC - FC          [Accounting form]

=============================================================================
DERIVED RELATIONSHIPS
=============================================================================

1. BREAK-EVEN (BEM-1.0):
   π = 0 → x_BE = Kf / (p - kv) = Kf / CM

2. MARGIN OF SAFETY:
   MoS = (x - x_BE) / x = 1 - (Kf / CM·x)

3. OPERATING LEVERAGE (DOL):
   DOL = CM·x / π = (p - kv)·x / [(p - kv)·x - Kf]

   At break-even: DOL → ∞
   As x → ∞: DOL → 1

4. CONTRIBUTION MARGIN RATIO:
   CMR = CM / p = (p - kv) / p = 1 - (kv / p)

5. SENSITIVITY ANALYSIS:
   ∂π/∂p = x                    [Price sensitivity]
   ∂π/∂x = p - kv = CM          [Volume sensitivity]
   ∂π/∂kv = -x                  [Variable cost sensitivity]
   ∂π/∂Kf = -1                  [Fixed cost sensitivity]

=============================================================================
KAPITALKOSTEN (WACC) - Cost of Capital
=============================================================================

WACC = Weighted Average Cost of Capital = Kapitalkosten

    WACC = (E/V) × Re + (D/V) × Rd × (1-t)

Where:
    E   = Equity (Eigenkapital)
    D   = Debt (Fremdkapital)
    V   = E + D (Gesamtkapital)
    Re  = Cost of Equity (Eigenkapitalkosten) = Rf + β_E × MRP
    Rd  = Cost of Debt (Fremdkapitalkosten)
    t   = Tax Rate (Steuersatz)

Value Creation Test:
    ROIC > WACC  →  Wertschaffend (Value Creating)
    ROIC < WACC  →  Wertvernichtend (Value Destroying)

    EVA = NOPAT - WACC × Invested Capital
    EVA > 0  →  Economic Value Added (Mehrwert)

Connection to Fundamental Equation:
    π (EBIT) → NOPAT = EBIT × (1-t)
    ROIC = NOPAT / Invested Capital
    Value Created = (ROIC - WACC) × Invested Capital

=============================================================================
BETA CONNECTIONS
=============================================================================

Revenue Beta (β_R):
    Measures sensitivity of revenue (p·x) to market conditions
    β_R = Cov(R, R_m) / Var(R_m)

Operating Beta (β_Op):
    β_Op = β_R × DOL
    Higher fixed costs (Kf) → Higher DOL → Higher β_Op

Asset Beta (β_A):
    β_A ≈ β_Op for operating businesses

Equity Beta (β_E):
    β_E = β_A × [1 + (1-t) × (D/E)]
    Financial leverage amplifies operating risk

Cost of Equity (Re):
    Re = Rf + β_E × MRP
    Higher β_E → Higher Re → Higher WACC

=============================================================================
MODEL CONNECTIONS
=============================================================================

FEM-1.0 provides the foundation for:

┌─────────────────────────────────────────────────────────────────────────┐
│  FEM-1.0: π = p·x - kv·x - Kf                                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  RPM-1.0 (Revenue)     → R = p·x (aggregated across regions/products)  │
│  CSM-1.0 (Costs)       → TC = kv·x + Kf (by category)                  │
│  PLM-1.0 (P&L)         → π = R - TC                                    │
│  BEM-1.0 (Break-Even)  → x_BE = Kf / CM                                │
│  PRM-1.0 (Pricing)     → Optimize p given elasticity ε                 │
│  BFM-1.0 (Beta)        → DOL = CM·x / π → β_Op = β_R × DOL            │
│  VCM-1.0 (Value)       → EVA = NOPAT - WACC × Capital                  │
│  MCSM-1.0 (Monte Carlo)→ Simulate p, x, kv, Kf with uncertainty        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

Author: Claude (Strategic Models Team)
Version: 1.0.0
Created: 2026-01-16
"""

import math
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import numpy as np


@dataclass
class FundamentalInputs:
    """Core economic inputs."""
    price: float              # p: Price per unit
    quantity: float           # x: Quantity sold
    variable_cost: float      # kv: Variable cost per unit
    fixed_costs: float        # Kf: Total fixed costs

    # Optional for extended analysis
    tax_rate: float = 0.25    # t: Corporate tax rate
    debt: float = 0.0         # D: Total debt
    equity: float = 0.0       # E: Total equity
    invested_capital: float = 0.0  # IC: Invested capital


@dataclass
class FundamentalOutputs:
    """All derived economic metrics."""
    # Core P&L
    revenue: float
    variable_costs_total: float
    contribution_margin_total: float
    profit: float  # π = EBIT

    # Unit economics
    contribution_margin_unit: float  # CM = p - kv
    contribution_margin_ratio: float  # CMR = CM / p

    # Break-even
    break_even_quantity: float  # x_BE
    break_even_revenue: float  # R_BE
    margin_of_safety_percent: float  # MoS

    # Leverage
    degree_of_operating_leverage: float  # DOL
    degree_of_financial_leverage: float  # DFL (if applicable)
    degree_of_total_leverage: float  # DTL = DOL × DFL

    # Sensitivities (elasticities)
    profit_sensitivity_price: float  # ∂π/∂p
    profit_sensitivity_volume: float  # ∂π/∂x
    profit_sensitivity_variable_cost: float  # ∂π/∂kv
    profit_sensitivity_fixed_cost: float  # ∂π/∂Kf


def calculate_fundamentals(inputs: FundamentalInputs) -> FundamentalOutputs:
    """
    Calculate all fundamental economic metrics from core inputs.

    This is the CORE calculation that underlies all strategic models.

    Args:
        inputs: FundamentalInputs with p, x, kv, Kf

    Returns:
        FundamentalOutputs with all derived metrics
    """
    p = inputs.price
    x = inputs.quantity
    kv = inputs.variable_cost
    Kf = inputs.fixed_costs

    # === Core P&L ===
    revenue = p * x
    variable_costs_total = kv * x
    contribution_margin_total = revenue - variable_costs_total  # CM·x
    profit = contribution_margin_total - Kf  # π = EBIT

    # === Unit Economics ===
    contribution_margin_unit = p - kv  # CM per unit
    contribution_margin_ratio = contribution_margin_unit / p if p > 0 else 0  # CMR

    # === Break-Even ===
    if contribution_margin_unit > 0:
        break_even_quantity = Kf / contribution_margin_unit
        break_even_revenue = break_even_quantity * p
    else:
        break_even_quantity = float('inf')
        break_even_revenue = float('inf')

    # Margin of Safety
    if x > 0:
        margin_of_safety = (x - break_even_quantity) / x * 100
    else:
        margin_of_safety = 0

    # === Operating Leverage ===
    # DOL = CM·x / π = Contribution Margin / EBIT
    if profit > 0:
        degree_of_operating_leverage = contribution_margin_total / profit
    elif profit < 0:
        # Negative profit: DOL is technically negative (losses amplified)
        degree_of_operating_leverage = contribution_margin_total / profit
    else:
        # At break-even: DOL → ∞
        degree_of_operating_leverage = float('inf')

    # === Financial Leverage ===
    # DFL = EBIT / EBT = EBIT / (EBIT - Interest)
    # For now, assume no interest (will be calculated in DFM-1.0)
    degree_of_financial_leverage = 1.0

    if inputs.debt > 0 and inputs.equity > 0:
        # Approximate DFL from capital structure
        # DFL ≈ 1 + D/E for typical interest coverage
        degree_of_financial_leverage = 1.0 + (inputs.debt / inputs.equity) * 0.3  # Dampened

    # Total Leverage
    degree_of_total_leverage = degree_of_operating_leverage * degree_of_financial_leverage

    # === Sensitivities ===
    # These are the partial derivatives ∂π/∂variable
    profit_sensitivity_price = x  # ∂π/∂p = x
    profit_sensitivity_volume = contribution_margin_unit  # ∂π/∂x = CM
    profit_sensitivity_variable_cost = -x  # ∂π/∂kv = -x
    profit_sensitivity_fixed_cost = -1  # ∂π/∂Kf = -1

    return FundamentalOutputs(
        revenue=revenue,
        variable_costs_total=variable_costs_total,
        contribution_margin_total=contribution_margin_total,
        profit=profit,
        contribution_margin_unit=contribution_margin_unit,
        contribution_margin_ratio=contribution_margin_ratio,
        break_even_quantity=break_even_quantity,
        break_even_revenue=break_even_revenue,
        margin_of_safety_percent=margin_of_safety,
        degree_of_operating_leverage=degree_of_operating_leverage,
        degree_of_financial_leverage=degree_of_financial_leverage,
        degree_of_total_leverage=degree_of_total_leverage,
        profit_sensitivity_price=profit_sensitivity_price,
        profit_sensitivity_volume=profit_sensitivity_volume,
        profit_sensitivity_variable_cost=profit_sensitivity_variable_cost,
        profit_sensitivity_fixed_cost=profit_sensitivity_fixed_cost,
    )


# =============================================================================
# Time Horizon Analysis
# =============================================================================

from enum import Enum


class TimeHorizon(Enum):
    """Economic time horizons affecting cost behavior."""
    INSTANT = "instant"           # < 1 month: Only price adjusts
    SHORT_TERM = "short_term"     # 1-12 months: Standard variable/fixed
    MEDIUM_TERM = "medium_term"   # 1-5 years: Step costs, capacity changes
    LONG_TERM = "long_term"       # > 5 years: All costs variable


@dataclass
class TimeHorizonParameters:
    """Cost behavior parameters for different time horizons."""
    horizon: TimeHorizon
    price_elasticity: float = -1.5  # ε: % quantity change per % price change
    capacity_utilization: float = 0.80  # Current utilization
    capacity_max: float = 1.0  # Max capacity
    step_cost_threshold: float = 0.1  # Capacity change triggering step cost
    step_cost_amount: float = 0.0  # Additional fixed cost per step
    scale_elasticity: float = 0.85  # Long-run: 1% volume → 0.85% cost increase


def analyze_by_time_horizon(
    inputs: FundamentalInputs,
    horizon: TimeHorizon,
    horizon_params: TimeHorizonParameters = None,
) -> Dict:
    """
    Analyze economics adjusted for specific time horizon.

    Different horizons imply different cost behaviors:
    - INSTANT: All costs fixed except price
    - SHORT_TERM: Standard variable/fixed split
    - MEDIUM_TERM: Fixed costs can step up/down
    - LONG_TERM: All costs become variable (scale effects)

    Args:
        inputs: Base FundamentalInputs
        horizon: TimeHorizon enum
        horizon_params: Optional TimeHorizonParameters

    Returns:
        Dict with horizon-adjusted analysis
    """
    if horizon_params is None:
        horizon_params = TimeHorizonParameters(horizon=horizon)

    base_outputs = calculate_fundamentals(inputs)

    result = {
        "horizon": horizon.value,
        "base_case": {
            "revenue": base_outputs.revenue,
            "profit": base_outputs.profit,
            "dol": base_outputs.degree_of_operating_leverage,
        }
    }

    if horizon == TimeHorizon.INSTANT:
        # INSTANT: Only price can change, all else fixed
        # Relevant question: What if we change price?
        # Quantity responds via elasticity: Δx/x = ε × Δp/p

        scenarios = []
        for price_change in [-10, -5, 0, 5, 10]:
            # Quantity response via elasticity
            quantity_response = horizon_params.price_elasticity * price_change
            new_price = inputs.price * (1 + price_change / 100)
            new_quantity = inputs.quantity * (1 + quantity_response / 100)

            # But in instant, we can't actually change quantity (capacity fixed)
            # So only revenue from existing inventory changes
            # π_instant = p_new × x_fixed - kv × x_fixed - Kf
            new_revenue = new_price * inputs.quantity  # Fixed quantity
            new_profit = new_revenue - inputs.variable_cost * inputs.quantity - inputs.fixed_costs

            scenarios.append({
                "price_change_percent": price_change,
                "theoretical_quantity_response": round(quantity_response, 1),
                "actual_quantity_change": 0,  # Fixed in instant
                "new_revenue": round(new_revenue, 2),
                "new_profit": round(new_profit, 2),
                "profit_change_percent": round((new_profit - base_outputs.profit) / base_outputs.profit * 100 if base_outputs.profit != 0 else 0, 1),
            })

        result["instant_analysis"] = {
            "description": "INSTANT: Only price adjusts, quantity and costs fixed",
            "key_insight": "Short-term pricing power matters most",
            "scenarios": scenarios,
        }

    elif horizon == TimeHorizon.SHORT_TERM:
        # SHORT-TERM: Standard equation π = p·x - kv·x - Kf
        # DOL is high because Kf is locked
        result["short_term_analysis"] = {
            "description": "SHORT-TERM: Variable costs adjust, fixed costs locked",
            "dol": round(base_outputs.degree_of_operating_leverage, 2) if base_outputs.degree_of_operating_leverage != float('inf') else "∞",
            "key_insight": f"High DOL ({base_outputs.degree_of_operating_leverage:.1f}x) amplifies revenue changes",
            "break_even_quantity": base_outputs.break_even_quantity,
            "margin_of_safety": round(base_outputs.margin_of_safety_percent, 1),
        }

    elif horizon == TimeHorizon.MEDIUM_TERM:
        # MEDIUM-TERM: Fixed costs can step up/down with capacity
        # Kf becomes Kf(capacity_level)

        capacity_levels = [0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2]  # 60% to 120%
        step_scenarios = []

        base_capacity = horizon_params.capacity_utilization
        for cap in capacity_levels:
            # How many steps from base capacity?
            steps = int(abs(cap - base_capacity) / horizon_params.step_cost_threshold)

            # Adjusted fixed costs
            if cap > base_capacity:
                # Expansion: Add step costs
                adjusted_kf = inputs.fixed_costs + steps * horizon_params.step_cost_amount
            else:
                # Contraction: Can reduce some fixed costs (but not all)
                reduction = min(steps * horizon_params.step_cost_amount * 0.5, inputs.fixed_costs * 0.3)
                adjusted_kf = inputs.fixed_costs - reduction

            # Quantity at this capacity
            max_quantity = inputs.quantity / base_capacity  # Derive max from current
            new_quantity = max_quantity * cap

            # New profit
            new_revenue = inputs.price * new_quantity
            new_vc = inputs.variable_cost * new_quantity
            new_profit = new_revenue - new_vc - adjusted_kf

            step_scenarios.append({
                "capacity_utilization": cap,
                "capacity_percent": round(cap * 100),
                "quantity": round(new_quantity),
                "step_cost_adjustment": round(adjusted_kf - inputs.fixed_costs, 2),
                "fixed_costs": round(adjusted_kf, 2),
                "profit": round(new_profit, 2),
            })

        result["medium_term_analysis"] = {
            "description": "MEDIUM-TERM: Fixed costs step with capacity changes",
            "key_insight": "Capacity decisions trigger step costs",
            "step_cost_threshold": f"{horizon_params.step_cost_threshold * 100:.0f}% capacity change",
            "scenarios": step_scenarios,
        }

    elif horizon == TimeHorizon.LONG_TERM:
        # LONG-RUN: All costs become variable → Economies of scale
        # TC = f(x) with scale elasticity < 1 (economies of scale)
        # DOL → 1 as Kf → 0 (all costs adjust)

        scale_elasticity = horizon_params.scale_elasticity
        scale_scenarios = []

        for volume_mult in [0.5, 0.75, 1.0, 1.25, 1.5, 2.0]:
            new_quantity = inputs.quantity * volume_mult

            # Long-run cost function: TC = TC_base × (x/x_base)^scale_elasticity
            base_total_cost = inputs.variable_cost * inputs.quantity + inputs.fixed_costs
            new_total_cost = base_total_cost * (volume_mult ** scale_elasticity)

            # Effective cost per unit
            cost_per_unit = new_total_cost / new_quantity if new_quantity > 0 else 0
            base_cpu = base_total_cost / inputs.quantity

            new_revenue = inputs.price * new_quantity
            new_profit = new_revenue - new_total_cost

            # Long-run DOL approaches 1 (no fixed/variable distinction)
            long_run_dol = 1.0 / scale_elasticity  # Approximation

            scale_scenarios.append({
                "volume_multiplier": volume_mult,
                "quantity": round(new_quantity),
                "total_cost": round(new_total_cost, 2),
                "cost_per_unit": round(cost_per_unit, 2),
                "cost_per_unit_change_percent": round((cost_per_unit - base_cpu) / base_cpu * 100, 1),
                "profit": round(new_profit, 2),
                "profit_margin_percent": round(new_profit / new_revenue * 100 if new_revenue > 0 else 0, 1),
            })

        result["long_term_analysis"] = {
            "description": "LONG-TERM: All costs variable, scale effects dominate",
            "scale_elasticity": scale_elasticity,
            "key_insight": f"Scale elasticity {scale_elasticity:.2f} means 10% volume growth → {scale_elasticity * 10:.1f}% cost growth",
            "long_run_dol": round(1.0 / scale_elasticity, 2),
            "scenarios": scale_scenarios,
        }

    return result


def calculate_comprehensive_time_analysis(inputs: FundamentalInputs) -> Dict:
    """
    Run analysis across all time horizons.

    Shows how the same business looks different depending on planning horizon.
    """
    results = {
        "instant": analyze_by_time_horizon(inputs, TimeHorizon.INSTANT),
        "short_term": analyze_by_time_horizon(inputs, TimeHorizon.SHORT_TERM),
        "medium_term": analyze_by_time_horizon(
            inputs,
            TimeHorizon.MEDIUM_TERM,
            TimeHorizonParameters(
                horizon=TimeHorizon.MEDIUM_TERM,
                step_cost_threshold=0.1,
                step_cost_amount=inputs.fixed_costs * 0.15,  # 15% of Kf per step
            )
        ),
        "long_term": analyze_by_time_horizon(
            inputs,
            TimeHorizon.LONG_TERM,
            TimeHorizonParameters(
                horizon=TimeHorizon.LONG_TERM,
                scale_elasticity=0.85,
            )
        ),
    }

    # Summary comparison
    base = calculate_fundamentals(inputs)
    short_term_dol = base.degree_of_operating_leverage

    results["summary"] = {
        "key_differences": {
            "instant": "Only price adjusts → Price elasticity critical",
            "short_term": f"Standard DOL = {short_term_dol:.1f}x → Leverage risk",
            "medium_term": "Step costs → Capacity planning critical",
            "long_term": "All variable → Scale economics dominate",
        },
        "beta_implications": {
            "short_term_beta_op": round(0.8 * short_term_dol, 2) if short_term_dol != float('inf') else "∞",
            "long_term_beta_op": round(0.8 * (1.0 / 0.85), 2),  # β_R × long-run DOL
            "interpretation": "Short-term β higher due to fixed cost leverage; long-term β lower as costs adjust"
        }
    }

    return results


# =============================================================================
# Extended Analysis Functions
# =============================================================================

def calculate_profit_impact(
    base_outputs: FundamentalOutputs,
    price_change_percent: float = 0,
    volume_change_percent: float = 0,
    variable_cost_change_percent: float = 0,
    fixed_cost_change_percent: float = 0,
) -> Dict:
    """
    Calculate profit impact of parameter changes.

    Uses the fundamental sensitivities to estimate profit changes.

    Args:
        base_outputs: Base case FundamentalOutputs
        price_change_percent: % change in price
        volume_change_percent: % change in volume
        variable_cost_change_percent: % change in variable costs
        fixed_cost_change_percent: % change in fixed costs

    Returns:
        Dict with profit impacts by driver
    """
    base_profit = base_outputs.profit
    base_revenue = base_outputs.revenue
    base_cm = base_outputs.contribution_margin_total
    base_vc = base_outputs.variable_costs_total

    # Calculate impacts using sensitivities
    # Δπ ≈ (∂π/∂p)·Δp + (∂π/∂x)·Δx + (∂π/∂kv)·Δkv + (∂π/∂Kf)·ΔKf

    # Price impact: Δπ_p = x · Δp = x · (p · change%)
    price_impact = base_outputs.profit_sensitivity_price * (base_revenue / base_outputs.profit_sensitivity_price * price_change_percent / 100) if base_outputs.profit_sensitivity_price > 0 else 0

    # Volume impact: Δπ_x = CM · Δx
    volume_impact = base_outputs.profit_sensitivity_volume * (base_outputs.profit_sensitivity_price * volume_change_percent / 100)

    # Variable cost impact: Δπ_kv = -x · Δkv
    vc_impact = base_outputs.profit_sensitivity_variable_cost * (base_vc / abs(base_outputs.profit_sensitivity_variable_cost) * variable_cost_change_percent / 100) if base_outputs.profit_sensitivity_variable_cost != 0 else 0

    # Fixed cost impact: Δπ_Kf = -1 · ΔKf
    fc_impact = base_outputs.profit_sensitivity_fixed_cost * ((base_revenue - base_cm) * fixed_cost_change_percent / 100) if base_outputs.contribution_margin_total != base_revenue else 0

    total_impact = price_impact + volume_impact + vc_impact + fc_impact

    return {
        "base_profit": base_profit,
        "impacts": {
            "price": round(price_impact, 2),
            "volume": round(volume_impact, 2),
            "variable_costs": round(vc_impact, 2),
            "fixed_costs": round(fc_impact, 2),
        },
        "total_impact": round(total_impact, 2),
        "new_profit": round(base_profit + total_impact, 2),
        "profit_change_percent": round(total_impact / base_profit * 100 if base_profit != 0 else 0, 1),
    }


def calculate_operating_leverage_scenarios(
    base_inputs: FundamentalInputs,
    revenue_changes: List[float] = None,
) -> Dict:
    """
    Show how operating leverage amplifies revenue changes.

    This demonstrates DOL in action:
    - Revenue ↑ 10% → Profit ↑ (10% × DOL)

    Args:
        base_inputs: Base case inputs
        revenue_changes: List of revenue change percentages to simulate

    Returns:
        Dict with leverage scenarios
    """
    if revenue_changes is None:
        revenue_changes = [-20, -10, -5, 0, 5, 10, 20]

    base_outputs = calculate_fundamentals(base_inputs)
    dol = base_outputs.degree_of_operating_leverage

    scenarios = []
    for rev_change in revenue_changes:
        # Revenue change affects quantity (assuming constant price)
        new_quantity = base_inputs.quantity * (1 + rev_change / 100)

        new_inputs = FundamentalInputs(
            price=base_inputs.price,
            quantity=new_quantity,
            variable_cost=base_inputs.variable_cost,
            fixed_costs=base_inputs.fixed_costs,
        )
        new_outputs = calculate_fundamentals(new_inputs)

        profit_change = (new_outputs.profit - base_outputs.profit) / base_outputs.profit * 100 if base_outputs.profit != 0 else 0

        scenarios.append({
            "revenue_change_percent": rev_change,
            "expected_profit_change": round(rev_change * dol, 1),  # Theoretical
            "actual_profit_change": round(profit_change, 1),  # Calculated
            "new_profit": round(new_outputs.profit, 2),
            "new_margin_of_safety": round(new_outputs.margin_of_safety_percent, 1),
        })

    return {
        "base_case": {
            "revenue": base_outputs.revenue,
            "profit": base_outputs.profit,
            "dol": round(dol, 2) if dol != float('inf') else "∞",
            "margin_of_safety": round(base_outputs.margin_of_safety_percent, 1),
        },
        "scenarios": scenarios,
        "interpretation": _interpret_leverage(dol),
    }


def _interpret_leverage(dol: float) -> str:
    """Interpret the DOL value."""
    if dol == float('inf'):
        return "AT BREAK-EVEN: Infinite leverage - any volume change causes swing to profit/loss"
    elif dol > 3:
        return f"HIGH LEVERAGE (DOL={dol:.1f}): 1% revenue change → {dol:.1f}% profit change. High fixed costs."
    elif dol > 2:
        return f"MODERATE LEVERAGE (DOL={dol:.1f}): Mixed cost structure."
    elif dol > 1:
        return f"LOW LEVERAGE (DOL={dol:.1f}): Mostly variable costs, stable profits."
    else:
        return f"LOSS SITUATION (DOL={dol:.1f}): Below break-even."


def calculate_wacc_and_value(
    profit_ebit: float,
    invested_capital: float,
    equity: float,
    debt: float,
    equity_beta: float,
    tax_rate: float = 0.25,
    risk_free_rate: float = 0.035,
    market_risk_premium: float = 0.055,
    cost_of_debt: float = 0.05,
) -> Dict:
    """
    Calculate WACC (Kapitalkosten) and Value Creation metrics.

    WACC = (E/V) × Re + (D/V) × Rd × (1-t)

    Args:
        profit_ebit: EBIT from fundamental equation (π)
        invested_capital: Total invested capital
        equity: Equity value (E)
        debt: Debt value (D)
        equity_beta: Equity beta (β_E) from beta chain
        tax_rate: Corporate tax rate (t)
        risk_free_rate: Risk-free rate (Rf)
        market_risk_premium: Market risk premium (MRP)
        cost_of_debt: Pre-tax cost of debt (Rd)

    Returns:
        Dict with WACC, ROIC, EVA, and value creation assessment
    """
    # Total value
    total_value = equity + debt
    if total_value <= 0:
        return {"error": "Total value must be positive"}

    # Capital structure weights
    equity_weight = equity / total_value
    debt_weight = debt / total_value

    # Cost of Equity: Re = Rf + β_E × MRP
    cost_of_equity = risk_free_rate + equity_beta * market_risk_premium

    # WACC = (E/V) × Re + (D/V) × Rd × (1-t)
    wacc = equity_weight * cost_of_equity + debt_weight * cost_of_debt * (1 - tax_rate)

    # NOPAT = EBIT × (1 - t)
    nopat = profit_ebit * (1 - tax_rate)

    # ROIC = NOPAT / Invested Capital
    roic = nopat / invested_capital if invested_capital > 0 else 0

    # EVA = NOPAT - WACC × Invested Capital
    capital_charge = wacc * invested_capital
    eva = nopat - capital_charge

    # Spread = ROIC - WACC
    spread = roic - wacc

    # Value creation assessment
    if spread > 0.02:  # > 2% spread
        value_status = "STARK WERTSCHAFFEND (Strong Value Creation)"
    elif spread > 0:
        value_status = "WERTSCHAFFEND (Value Creating)"
    elif spread > -0.02:
        value_status = "GRENZWERTIG (Marginal)"
    else:
        value_status = "WERTVERNICHTEND (Value Destroying)"

    return {
        "kapitalstruktur": {
            "eigenkapital_e": equity,
            "fremdkapital_d": debt,
            "gesamtkapital_v": total_value,
            "eigenkapitalquote": round(equity_weight * 100, 1),
            "fremdkapitalquote": round(debt_weight * 100, 1),
        },
        "kapitalkosten": {
            "eigenkapitalkosten_re_percent": round(cost_of_equity * 100, 2),
            "fremdkapitalkosten_rd_percent": round(cost_of_debt * 100, 2),
            "wacc_percent": round(wacc * 100, 2),
            "formula": "WACC = (E/V) × Re + (D/V) × Rd × (1-t)",
        },
        "wertschaffung": {
            "ebit": profit_ebit,
            "nopat": round(nopat, 2),
            "invested_capital": invested_capital,
            "roic_percent": round(roic * 100, 2),
            "capital_charge": round(capital_charge, 2),
            "eva": round(eva, 2),
            "spread_percent": round(spread * 100, 2),
            "status": value_status,
        },
        "interpretation": {
            "roic_vs_wacc": f"ROIC ({roic*100:.1f}%) {'>' if roic > wacc else '<'} WACC ({wacc*100:.1f}%)",
            "eva_bedeutung": f"EVA = €{eva:,.0f} = NOPAT - Kapitalkosten",
            "spread_bedeutung": f"Spread = {spread*100:.1f}pp bedeutet {'Wertschaffung' if spread > 0 else 'Wertvernichtung'} pro € investiertem Kapital",
        }
    }


def calculate_beta_from_fundamentals(
    base_outputs: FundamentalOutputs,
    revenue_beta: float = 0.8,
    debt_to_equity: float = 0.5,
    tax_rate: float = 0.25,
) -> Dict:
    """
    Calculate beta chain starting from fundamental DOL.

    This connects FEM-1.0 directly to BFM-1.0.

    β_Op = β_R × DOL
    β_E = β_A × [1 + (1-t) × (D/E)]

    Args:
        base_outputs: FundamentalOutputs with DOL
        revenue_beta: Base revenue beta
        debt_to_equity: D/E ratio
        tax_rate: Corporate tax rate

    Returns:
        Dict with full beta chain
    """
    dol = base_outputs.degree_of_operating_leverage

    # Handle infinite DOL
    if dol == float('inf'):
        return {
            "warning": "At break-even, DOL is infinite. Beta calculation not meaningful.",
            "recommendation": "Move above break-even before calculating systematic risk."
        }

    # Operating Beta
    operating_beta = revenue_beta * dol

    # Asset Beta (≈ Operating Beta for operating businesses)
    asset_beta = operating_beta

    # Equity Beta (Hamada)
    equity_beta = asset_beta * (1 + (1 - tax_rate) * debt_to_equity)

    # Cost of Equity (CAPM)
    risk_free = 0.035
    market_premium = 0.055
    cost_of_equity = risk_free + equity_beta * market_premium

    return {
        "beta_chain": {
            "revenue_beta": round(revenue_beta, 3),
            "operating_beta": round(operating_beta, 3),
            "asset_beta": round(asset_beta, 3),
            "equity_beta": round(equity_beta, 3),
        },
        "leverage_factors": {
            "operating_leverage_dol": round(dol, 2),
            "financial_leverage_de": debt_to_equity,
        },
        "cost_of_equity_percent": round(cost_of_equity * 100, 2),
        "interpretation": f"DOL of {dol:.1f}x amplifies β_R ({revenue_beta:.2f}) to β_Op ({operating_beta:.2f}). Financial leverage further amplifies to β_E ({equity_beta:.2f})."
    }


# =============================================================================
# Main Function for Model Library
# =============================================================================

def analyze_fundamental_economics(
    price: float,
    quantity: float,
    variable_cost_per_unit: float,
    fixed_costs: float,
    debt: float = 0,
    equity: float = 0,
    invested_capital: float = None,  # If None, uses debt + equity
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
) -> Dict:
    """
    Main entry point for FEM-1.0: Fundamental Economics Model.

    Calculates all metrics derived from the fundamental equation:

        π = p·x - kv·x - Kf

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
        include_beta_analysis: Calculate beta chain
        include_wacc_analysis: Calculate WACC and value creation
        include_leverage_scenarios: Calculate leverage scenarios
        include_time_horizon_analysis: Calculate analysis by time horizon
        scale_elasticity: Long-run scale elasticity (< 1 = economies of scale)

    Returns:
        Complete fundamental economics analysis including:
        - Core P&L from π = p·x - kv·x - Kf
        - Break-even analysis
        - Operating leverage (DOL)
        - Sensitivities
        - Beta chain: β_R → β_Op → β_A → β_E (optional)
        - WACC and Value Creation: ROIC, EVA, Spread (optional)
        - Leverage scenarios (optional)
        - Time horizon analysis (optional): instant/short/medium/long-term
    """
    # Build inputs
    inputs = FundamentalInputs(
        price=price,
        quantity=quantity,
        variable_cost=variable_cost_per_unit,
        fixed_costs=fixed_costs,
        tax_rate=tax_rate,
        debt=debt,
        equity=equity,
    )

    # Core calculations
    outputs = calculate_fundamentals(inputs)

    # Build result
    result = {
        "model": "FEM-1.0",
        "model_name": "Fundamental Economics Model",
        "version": "1.0.0",
        "fundamental_equation": {
            "formula": "π = p·x - kv·x - Kf",
            "components": {
                "p_price": price,
                "x_quantity": quantity,
                "kv_variable_cost": variable_cost_per_unit,
                "Kf_fixed_costs": fixed_costs,
            }
        },
        "pnl": {
            "revenue": round(outputs.revenue, 2),
            "variable_costs": round(outputs.variable_costs_total, 2),
            "contribution_margin": round(outputs.contribution_margin_total, 2),
            "fixed_costs": fixed_costs,
            "profit_ebit": round(outputs.profit, 2),
        },
        "unit_economics": {
            "contribution_margin_per_unit": round(outputs.contribution_margin_unit, 2),
            "contribution_margin_ratio_percent": round(outputs.contribution_margin_ratio * 100, 1),
        },
        "break_even": {
            "break_even_quantity": round(outputs.break_even_quantity, 0) if outputs.break_even_quantity != float('inf') else "N/A",
            "break_even_revenue": round(outputs.break_even_revenue, 2) if outputs.break_even_revenue != float('inf') else "N/A",
            "margin_of_safety_percent": round(outputs.margin_of_safety_percent, 1),
        },
        "leverage": {
            "degree_of_operating_leverage": round(outputs.degree_of_operating_leverage, 2) if outputs.degree_of_operating_leverage != float('inf') else "∞",
            "degree_of_financial_leverage": round(outputs.degree_of_financial_leverage, 2),
            "degree_of_total_leverage": round(outputs.degree_of_total_leverage, 2) if outputs.degree_of_total_leverage != float('inf') else "∞",
        },
        "sensitivities": {
            "profit_per_1pct_price_change": round(outputs.profit_sensitivity_price * price * 0.01, 2),
            "profit_per_1pct_volume_change": round(outputs.profit_sensitivity_volume * quantity * 0.01, 2),
            "profit_per_1pct_variable_cost_change": round(outputs.profit_sensitivity_variable_cost * variable_cost_per_unit * 0.01, 2),
            "profit_per_1pct_fixed_cost_change": round(outputs.profit_sensitivity_fixed_cost * fixed_costs * 0.01, 2),
        },
        "formulas": {
            "break_even": "x_BE = Kf / (p - kv)",
            "dol": "DOL = (p-kv)·x / π",
            "margin_of_safety": "MoS = (x - x_BE) / x",
            "sensitivities": "∂π/∂p = x, ∂π/∂x = CM, ∂π/∂kv = -x, ∂π/∂Kf = -1",
        }
    }

    # Add beta analysis
    if include_beta_analysis:
        de_ratio = debt / equity if equity > 0 else 0.5
        beta_analysis = calculate_beta_from_fundamentals(
            outputs,
            revenue_beta=revenue_beta,
            debt_to_equity=de_ratio,
            tax_rate=tax_rate,
        )
        result["beta_analysis"] = beta_analysis

        # Add WACC and value creation analysis
        if include_wacc_analysis and debt > 0 and equity > 0:
            # Get equity beta from beta analysis
            equity_beta = beta_analysis.get("beta_chain", {}).get("equity_beta", 1.0)

            # Use invested capital or default to D + E
            ic = invested_capital if invested_capital is not None else (debt + equity)

            wacc_analysis = calculate_wacc_and_value(
                profit_ebit=outputs.profit,
                invested_capital=ic,
                equity=equity,
                debt=debt,
                equity_beta=equity_beta,
                tax_rate=tax_rate,
                risk_free_rate=risk_free_rate,
                market_risk_premium=market_risk_premium,
                cost_of_debt=cost_of_debt,
            )
            result["wacc_value_creation"] = wacc_analysis

    # Add leverage scenarios
    if include_leverage_scenarios:
        leverage_scenarios = calculate_operating_leverage_scenarios(inputs)
        result["leverage_scenarios"] = leverage_scenarios

    # Add time horizon analysis
    if include_time_horizon_analysis:
        # Create horizon params with user's scale elasticity
        medium_params = TimeHorizonParameters(
            horizon=TimeHorizon.MEDIUM_TERM,
            step_cost_threshold=0.1,
            step_cost_amount=fixed_costs * 0.15,
        )
        long_params = TimeHorizonParameters(
            horizon=TimeHorizon.LONG_TERM,
            scale_elasticity=scale_elasticity,
        )

        result["time_horizon_analysis"] = {
            "instant": analyze_by_time_horizon(inputs, TimeHorizon.INSTANT),
            "short_term": analyze_by_time_horizon(inputs, TimeHorizon.SHORT_TERM),
            "medium_term": analyze_by_time_horizon(inputs, TimeHorizon.MEDIUM_TERM, medium_params),
            "long_term": analyze_by_time_horizon(inputs, TimeHorizon.LONG_TERM, long_params),
            "summary": {
                "cost_behavior_by_horizon": {
                    "instant": "All costs fixed, only price adjusts",
                    "short_term": "Variable costs adjust, fixed costs locked → High DOL",
                    "medium_term": "Fixed costs step with capacity changes",
                    "long_term": "All costs variable, scale economics dominate",
                },
                "dol_by_horizon": {
                    "short_term": round(outputs.degree_of_operating_leverage, 2) if outputs.degree_of_operating_leverage != float('inf') else "∞",
                    "long_term": round(1.0 / scale_elasticity, 2),
                    "interpretation": f"DOL falls from {outputs.degree_of_operating_leverage:.1f}x (short) to {1.0/scale_elasticity:.1f}x (long) as costs become variable"
                },
                "strategic_implications": {
                    "pricing": "Short-term: Price changes fully impact profit. Long-term: Competition erodes pricing power.",
                    "capacity": "Medium-term: Capacity decisions trigger step costs. Plan expansions carefully.",
                    "scale": f"Long-term: Scale elasticity {scale_elasticity:.2f} means economies of scale exist. Growth is profitable.",
                }
            }
        }

    return result


if __name__ == "__main__":
    print("=" * 70)
    print("FEM-1.0: Fundamental Economics Model - Demo")
    print("=" * 70)

    # Example: Manufacturing company
    # Revenue €100M, 50% variable costs, €30M fixed costs
    result = analyze_fundamental_economics(
        price=100,           # €100 per unit
        quantity=1_000_000,  # 1M units → €100M revenue
        variable_cost_per_unit=50,  # €50 variable cost → 50% of price
        fixed_costs=30_000_000,     # €30M fixed costs
        debt=40_000_000,     # €40M debt
        equity=60_000_000,   # €60M equity
        revenue_beta=0.7,    # Low cyclicality
    )

    print(f"\nModel: {result['model']} ({result['model_name']})")

    print(f"\n--- FUNDAMENTAL EQUATION ---")
    print(f"  π = p·x - kv·x - Kf")
    print(f"  π = {result['fundamental_equation']['components']['p_price']}·{result['fundamental_equation']['components']['x_quantity']:,} - {result['fundamental_equation']['components']['kv_variable_cost']}·{result['fundamental_equation']['components']['x_quantity']:,} - {result['fundamental_equation']['components']['Kf_fixed_costs']:,}")

    print(f"\n--- P&L ---")
    print(f"  Revenue:      €{result['pnl']['revenue']:,.0f}")
    print(f"  Variable:     €{result['pnl']['variable_costs']:,.0f}")
    print(f"  Contribution: €{result['pnl']['contribution_margin']:,.0f}")
    print(f"  Fixed:        €{result['pnl']['fixed_costs']:,.0f}")
    print(f"  EBIT:         €{result['pnl']['profit_ebit']:,.0f}")

    print(f"\n--- UNIT ECONOMICS ---")
    print(f"  CM per unit: €{result['unit_economics']['contribution_margin_per_unit']}")
    print(f"  CM ratio:    {result['unit_economics']['contribution_margin_ratio_percent']}%")

    print(f"\n--- BREAK-EVEN ---")
    print(f"  BE Quantity: {result['break_even']['break_even_quantity']:,} units")
    print(f"  BE Revenue:  €{result['break_even']['break_even_revenue']:,.0f}")
    print(f"  Margin of Safety: {result['break_even']['margin_of_safety_percent']}%")

    print(f"\n--- LEVERAGE ---")
    print(f"  DOL: {result['leverage']['degree_of_operating_leverage']}x")
    print(f"  DFL: {result['leverage']['degree_of_financial_leverage']}x")
    print(f"  DTL: {result['leverage']['degree_of_total_leverage']}x")

    print(f"\n--- SENSITIVITIES (per 1% change) ---")
    print(f"  Price +1%:    €{result['sensitivities']['profit_per_1pct_price_change']:+,.0f}")
    print(f"  Volume +1%:   €{result['sensitivities']['profit_per_1pct_volume_change']:+,.0f}")
    print(f"  Var Cost +1%: €{result['sensitivities']['profit_per_1pct_variable_cost_change']:+,.0f}")
    print(f"  Fix Cost +1%: €{result['sensitivities']['profit_per_1pct_fixed_cost_change']:+,.0f}")

    if 'beta_analysis' in result and 'beta_chain' in result['beta_analysis']:
        print(f"\n--- BETA CHAIN (from DOL) ---")
        beta = result['beta_analysis']['beta_chain']
        print(f"  β_R (Revenue):   {beta['revenue_beta']}")
        print(f"  β_Op (Operating): {beta['operating_beta']}")
        print(f"  β_A (Asset):      {beta['asset_beta']}")
        print(f"  β_E (Equity):     {beta['equity_beta']}")
        print(f"  Cost of Equity:   {result['beta_analysis']['cost_of_equity_percent']}%")

    print(f"\n--- LEVERAGE SCENARIOS ---")
    scenarios = result['leverage_scenarios']['scenarios']
    for s in scenarios:
        print(f"  Revenue {s['revenue_change_percent']:+3}% → Profit {s['actual_profit_change']:+.1f}% (MoS: {s['new_margin_of_safety']:.1f}%)")
