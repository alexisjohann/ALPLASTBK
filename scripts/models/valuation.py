"""
VAM-1.0: Valuation Model (Unternehmensbewertungsmodul)

Comprehensive Company Valuation Framework

This model provides multiple valuation approaches:
1. DCF (Discounted Cash Flow) - Entity & Equity Method
2. Multiple-Based Valuation (Trading & Transaction Comparables)
3. Sum-of-Parts Valuation

=============================================================================
DCF VALUATION (Ertragswertverfahren)
=============================================================================

Entity Value (Gesamtunternehmenswert):

    EV = Σ (FCF_t / (1 + WACC)^t) + TV / (1 + WACC)^n

Where:
    FCF_t = Free Cash Flow in year t
    WACC  = Weighted Average Cost of Capital
    TV    = Terminal Value
    n     = Projection period

Terminal Value Methods:
    1. Gordon Growth: TV = FCF_(n+1) / (WACC - g)
    2. Exit Multiple: TV = EBITDA_n × Multiple

Equity Value (Eigenkapitalwert):
    Equity Value = Entity Value - Net Debt

=============================================================================
MULTIPLE-BASED VALUATION (Multiplikatoren)
=============================================================================

Enterprise Value Multiples:
    EV/EBITDA  = Entity Value / EBITDA
    EV/EBIT    = Entity Value / EBIT
    EV/Sales   = Entity Value / Revenue

Equity Multiples:
    P/E        = Equity Value / Net Income
    P/B        = Equity Value / Book Value of Equity

=============================================================================
CONNECTION TO OTHER MODELS
=============================================================================

    FEM-1.0 (π = p·x - kv·x - Kf)
        ↓ EBIT
    PLM-1.0 (P&L Projection)
        ↓ Net Income, EBITDA
    CFM-1.0 (Cash Flow)
        ↓ Free Cash Flow
    BFM-1.0 (Beta Framework)
        ↓ β_E
    CMM-1.0 (Capital Markets)
        ↓ WACC
    VAM-1.0 (Valuation)
        → Entity Value, Equity Value, Implied Multiples

Author: Claude (Strategic Models Team)
Version: 1.0.0
Created: 2026-01-16
"""

import math
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from enum import Enum


class TerminalValueMethod(Enum):
    """Method for calculating terminal value."""
    GORDON_GROWTH = "gordon_growth"
    EXIT_MULTIPLE = "exit_multiple"


class ValuationApproach(Enum):
    """Valuation approach."""
    DCF = "dcf"
    TRADING_MULTIPLES = "trading_multiples"
    TRANSACTION_MULTIPLES = "transaction_multiples"
    SUM_OF_PARTS = "sum_of_parts"


@dataclass
class CashFlowProjection:
    """Projected cash flows for DCF."""
    year: int
    revenue: float
    ebitda: float
    ebit: float
    depreciation: float
    capex: float
    change_in_nwc: float  # Change in Net Working Capital
    tax_rate: float

    @property
    def nopat(self) -> float:
        """Net Operating Profit After Tax."""
        return self.ebit * (1 - self.tax_rate)

    @property
    def free_cash_flow(self) -> float:
        """Unlevered Free Cash Flow to Firm (FCFF)."""
        return (
            self.nopat +
            self.depreciation -
            self.capex -
            self.change_in_nwc
        )


# =============================================================================
# Industry Multiple Benchmarks
# =============================================================================

INDUSTRY_MULTIPLES = {
    "packaging_plastics": {
        "ev_ebitda": {"low": 6.0, "median": 8.0, "high": 10.0},
        "ev_ebit": {"low": 8.0, "median": 11.0, "high": 14.0},
        "ev_sales": {"low": 0.8, "median": 1.2, "high": 1.8},
        "pe": {"low": 12.0, "median": 16.0, "high": 22.0},
    },
    "manufacturing": {
        "ev_ebitda": {"low": 5.5, "median": 7.5, "high": 10.0},
        "ev_ebit": {"low": 7.5, "median": 10.0, "high": 13.0},
        "ev_sales": {"low": 0.6, "median": 1.0, "high": 1.5},
        "pe": {"low": 10.0, "median": 14.0, "high": 20.0},
    },
    "technology": {
        "ev_ebitda": {"low": 10.0, "median": 15.0, "high": 25.0},
        "ev_ebit": {"low": 15.0, "median": 22.0, "high": 35.0},
        "ev_sales": {"low": 2.0, "median": 4.0, "high": 8.0},
        "pe": {"low": 18.0, "median": 28.0, "high": 45.0},
    },
    "consumer_goods": {
        "ev_ebitda": {"low": 7.0, "median": 9.5, "high": 13.0},
        "ev_ebit": {"low": 9.0, "median": 12.5, "high": 17.0},
        "ev_sales": {"low": 0.8, "median": 1.3, "high": 2.0},
        "pe": {"low": 12.0, "median": 17.0, "high": 24.0},
    },
    "healthcare": {
        "ev_ebitda": {"low": 8.0, "median": 12.0, "high": 18.0},
        "ev_ebit": {"low": 10.0, "median": 15.0, "high": 22.0},
        "ev_sales": {"low": 1.5, "median": 2.5, "high": 4.0},
        "pe": {"low": 15.0, "median": 22.0, "high": 32.0},
    },
    "retail": {
        "ev_ebitda": {"low": 5.0, "median": 7.0, "high": 9.0},
        "ev_ebit": {"low": 7.0, "median": 9.5, "high": 12.0},
        "ev_sales": {"low": 0.4, "median": 0.7, "high": 1.0},
        "pe": {"low": 10.0, "median": 14.0, "high": 18.0},
    },
}


# =============================================================================
# DCF Valuation Functions
# =============================================================================

def calculate_dcf_valuation(
    cash_flows: List[CashFlowProjection],
    wacc: float,
    terminal_growth_rate: float = 0.02,
    terminal_method: TerminalValueMethod = TerminalValueMethod.GORDON_GROWTH,
    exit_multiple: float = None,
    net_debt: float = 0,
    minority_interests: float = 0,
    cash_and_equivalents: float = 0,
) -> Dict:
    """
    Calculate DCF valuation (Entity and Equity Value).

    Args:
        cash_flows: List of CashFlowProjection for each projection year
        wacc: Weighted Average Cost of Capital
        terminal_growth_rate: Long-term growth rate for Gordon Growth
        terminal_method: GORDON_GROWTH or EXIT_MULTIPLE
        exit_multiple: EV/EBITDA multiple for exit (if EXIT_MULTIPLE method)
        net_debt: Net Debt (Debt - Cash)
        minority_interests: Minority interests to deduct
        cash_and_equivalents: Additional cash to add

    Returns:
        Dict with DCF valuation results
    """
    if not cash_flows:
        return {"error": "No cash flows provided"}

    # Calculate present value of projection period FCFs
    pv_fcf = []
    cumulative_pv = 0

    for i, cf in enumerate(cash_flows):
        year = i + 1
        discount_factor = 1 / ((1 + wacc) ** year)
        pv = cf.free_cash_flow * discount_factor

        pv_fcf.append({
            "year": cf.year,
            "fcf": round(cf.free_cash_flow, 2),
            "discount_factor": round(discount_factor, 4),
            "present_value": round(pv, 2),
        })
        cumulative_pv += pv

    # Calculate Terminal Value
    last_cf = cash_flows[-1]
    n = len(cash_flows)

    if terminal_method == TerminalValueMethod.GORDON_GROWTH:
        # Gordon Growth Model: TV = FCF_(n+1) / (WACC - g)
        if wacc <= terminal_growth_rate:
            return {"error": "WACC must be greater than terminal growth rate"}

        terminal_fcf = last_cf.free_cash_flow * (1 + terminal_growth_rate)
        terminal_value = terminal_fcf / (wacc - terminal_growth_rate)
        tv_method_detail = f"FCF_(n+1) / (WACC - g) = {terminal_fcf:,.0f} / ({wacc*100:.1f}% - {terminal_growth_rate*100:.1f}%)"

    else:  # EXIT_MULTIPLE
        if exit_multiple is None:
            exit_multiple = 8.0  # Default EV/EBITDA
        terminal_value = last_cf.ebitda * exit_multiple
        tv_method_detail = f"EBITDA × Multiple = {last_cf.ebitda:,.0f} × {exit_multiple:.1f}x"

    # Discount Terminal Value to present
    tv_discount_factor = 1 / ((1 + wacc) ** n)
    pv_terminal_value = terminal_value * tv_discount_factor

    # Enterprise Value
    enterprise_value = cumulative_pv + pv_terminal_value

    # Equity Value = EV - Net Debt - Minority Interests + Excess Cash
    equity_value = enterprise_value - net_debt - minority_interests + cash_and_equivalents

    # Implied multiples
    current_ebitda = cash_flows[0].ebitda if cash_flows else 0
    current_ebit = cash_flows[0].ebit if cash_flows else 0
    current_revenue = cash_flows[0].revenue if cash_flows else 0

    implied_ev_ebitda = enterprise_value / current_ebitda if current_ebitda > 0 else 0
    implied_ev_ebit = enterprise_value / current_ebit if current_ebit > 0 else 0
    implied_ev_sales = enterprise_value / current_revenue if current_revenue > 0 else 0

    return {
        "method": "DCF",
        "wacc_percent": round(wacc * 100, 2),
        "projection_years": n,
        "cash_flow_projections": pv_fcf,
        "present_value_fcfs": round(cumulative_pv, 2),
        "terminal_value": {
            "method": terminal_method.value,
            "terminal_growth_rate": round(terminal_growth_rate * 100, 2) if terminal_method == TerminalValueMethod.GORDON_GROWTH else None,
            "exit_multiple": exit_multiple if terminal_method == TerminalValueMethod.EXIT_MULTIPLE else None,
            "undiscounted_tv": round(terminal_value, 2),
            "discount_factor": round(tv_discount_factor, 4),
            "present_value_tv": round(pv_terminal_value, 2),
            "tv_as_percent_of_ev": round(pv_terminal_value / enterprise_value * 100, 1) if enterprise_value > 0 else 0,
            "calculation": tv_method_detail,
        },
        "valuation_bridge": {
            "pv_projection_period": round(cumulative_pv, 2),
            "pv_terminal_value": round(pv_terminal_value, 2),
            "enterprise_value": round(enterprise_value, 2),
            "less_net_debt": round(-net_debt, 2),
            "less_minority_interests": round(-minority_interests, 2),
            "plus_excess_cash": round(cash_and_equivalents, 2),
            "equity_value": round(equity_value, 2),
        },
        "results": {
            "enterprise_value": round(enterprise_value, 2),
            "equity_value": round(equity_value, 2),
        },
        "implied_multiples": {
            "ev_ebitda": round(implied_ev_ebitda, 1),
            "ev_ebit": round(implied_ev_ebit, 1),
            "ev_sales": round(implied_ev_sales, 2),
        },
    }


# =============================================================================
# Multiple-Based Valuation Functions
# =============================================================================

def calculate_multiple_valuation(
    ebitda: float,
    ebit: float,
    revenue: float,
    net_income: float,
    book_equity: float,
    industry: str = "manufacturing",
    custom_multiples: Dict = None,
    net_debt: float = 0,
) -> Dict:
    """
    Calculate valuation using industry multiples.

    Args:
        ebitda: EBITDA
        ebit: EBIT
        revenue: Revenue
        net_income: Net Income
        book_equity: Book Value of Equity
        industry: Industry for benchmark multiples
        custom_multiples: Optional custom multiples dict
        net_debt: Net Debt for equity bridge

    Returns:
        Dict with multiple-based valuations
    """
    # Get industry multiples
    industry_lower = industry.lower().replace(" ", "_")
    multiples = INDUSTRY_MULTIPLES.get(industry_lower, INDUSTRY_MULTIPLES["manufacturing"])

    if custom_multiples:
        multiples = {**multiples, **custom_multiples}

    # Calculate EV using each multiple
    valuations = {}

    # EV/EBITDA
    ev_ebitda_low = ebitda * multiples["ev_ebitda"]["low"]
    ev_ebitda_med = ebitda * multiples["ev_ebitda"]["median"]
    ev_ebitda_high = ebitda * multiples["ev_ebitda"]["high"]

    valuations["ev_ebitda"] = {
        "metric": "EBITDA",
        "value": round(ebitda, 2),
        "multiples": multiples["ev_ebitda"],
        "enterprise_value": {
            "low": round(ev_ebitda_low, 2),
            "median": round(ev_ebitda_med, 2),
            "high": round(ev_ebitda_high, 2),
        },
        "equity_value": {
            "low": round(ev_ebitda_low - net_debt, 2),
            "median": round(ev_ebitda_med - net_debt, 2),
            "high": round(ev_ebitda_high - net_debt, 2),
        },
    }

    # EV/EBIT
    ev_ebit_low = ebit * multiples["ev_ebit"]["low"]
    ev_ebit_med = ebit * multiples["ev_ebit"]["median"]
    ev_ebit_high = ebit * multiples["ev_ebit"]["high"]

    valuations["ev_ebit"] = {
        "metric": "EBIT",
        "value": round(ebit, 2),
        "multiples": multiples["ev_ebit"],
        "enterprise_value": {
            "low": round(ev_ebit_low, 2),
            "median": round(ev_ebit_med, 2),
            "high": round(ev_ebit_high, 2),
        },
        "equity_value": {
            "low": round(ev_ebit_low - net_debt, 2),
            "median": round(ev_ebit_med - net_debt, 2),
            "high": round(ev_ebit_high - net_debt, 2),
        },
    }

    # EV/Sales
    ev_sales_low = revenue * multiples["ev_sales"]["low"]
    ev_sales_med = revenue * multiples["ev_sales"]["median"]
    ev_sales_high = revenue * multiples["ev_sales"]["high"]

    valuations["ev_sales"] = {
        "metric": "Revenue",
        "value": round(revenue, 2),
        "multiples": multiples["ev_sales"],
        "enterprise_value": {
            "low": round(ev_sales_low, 2),
            "median": round(ev_sales_med, 2),
            "high": round(ev_sales_high, 2),
        },
        "equity_value": {
            "low": round(ev_sales_low - net_debt, 2),
            "median": round(ev_sales_med - net_debt, 2),
            "high": round(ev_sales_high - net_debt, 2),
        },
    }

    # P/E (direct equity valuation)
    pe_low = net_income * multiples["pe"]["low"]
    pe_med = net_income * multiples["pe"]["median"]
    pe_high = net_income * multiples["pe"]["high"]

    valuations["pe"] = {
        "metric": "Net Income",
        "value": round(net_income, 2),
        "multiples": multiples["pe"],
        "equity_value": {
            "low": round(pe_low, 2),
            "median": round(pe_med, 2),
            "high": round(pe_high, 2),
        },
    }

    # Summary: Average of median valuations
    ev_median_avg = (ev_ebitda_med + ev_ebit_med + ev_sales_med) / 3
    equity_median_avg = (
        (ev_ebitda_med - net_debt) +
        (ev_ebit_med - net_debt) +
        (ev_sales_med - net_debt) +
        pe_med
    ) / 4

    return {
        "method": "Trading Multiples",
        "industry": industry,
        "valuations_by_multiple": valuations,
        "summary": {
            "enterprise_value_range": {
                "low": round(min(ev_ebitda_low, ev_ebit_low, ev_sales_low), 2),
                "median": round(ev_median_avg, 2),
                "high": round(max(ev_ebitda_high, ev_ebit_high, ev_sales_high), 2),
            },
            "equity_value_range": {
                "low": round(min(ev_ebitda_low, ev_ebit_low, ev_sales_low, pe_low) - net_debt, 2),
                "median": round(equity_median_avg, 2),
                "high": round(max(ev_ebitda_high, ev_ebit_high, ev_sales_high, pe_high), 2),
            },
        },
    }


# =============================================================================
# Football Field Chart Data
# =============================================================================

def create_football_field(
    dcf_result: Dict,
    multiple_result: Dict,
    additional_valuations: Dict = None,
) -> Dict:
    """
    Create data for football field valuation chart.

    Combines multiple valuation approaches into comparable ranges.
    """
    ranges = []

    # DCF
    if dcf_result and "results" in dcf_result:
        ev = dcf_result["results"]["enterprise_value"]
        # Assume +/- 15% for DCF range based on sensitivity
        ranges.append({
            "method": "DCF",
            "low": round(ev * 0.85, 2),
            "midpoint": round(ev, 2),
            "high": round(ev * 1.15, 2),
        })

    # Trading Multiples
    if multiple_result and "summary" in multiple_result:
        ev_range = multiple_result["summary"]["enterprise_value_range"]
        ranges.append({
            "method": "Trading Multiples",
            "low": ev_range["low"],
            "midpoint": ev_range["median"],
            "high": ev_range["high"],
        })

    # Additional valuations (e.g., transaction comps, LBO)
    if additional_valuations:
        for method, values in additional_valuations.items():
            ranges.append({
                "method": method,
                "low": values.get("low", values.get("midpoint", 0) * 0.9),
                "midpoint": values.get("midpoint", 0),
                "high": values.get("high", values.get("midpoint", 0) * 1.1),
            })

    # Calculate overall range
    all_lows = [r["low"] for r in ranges]
    all_highs = [r["high"] for r in ranges]
    all_mids = [r["midpoint"] for r in ranges]

    return {
        "valuation_ranges": ranges,
        "overall_range": {
            "minimum": round(min(all_lows), 2) if all_lows else 0,
            "weighted_average": round(sum(all_mids) / len(all_mids), 2) if all_mids else 0,
            "maximum": round(max(all_highs), 2) if all_highs else 0,
        },
        "chart_data": {
            "methods": [r["method"] for r in ranges],
            "low_values": [r["low"] for r in ranges],
            "mid_values": [r["midpoint"] for r in ranges],
            "high_values": [r["high"] for r in ranges],
        }
    }


# =============================================================================
# Main Function for Model Library
# =============================================================================

def run_valuation(
    # Financial metrics (current year)
    revenue: float,
    ebitda: float,
    ebit: float,
    net_income: float,
    depreciation: float,
    capex: float,
    change_in_nwc: float,

    # Capital structure
    net_debt: float = 0,
    book_equity: float = None,

    # Cost of capital
    wacc: float = 0.10,
    terminal_growth_rate: float = 0.02,

    # Growth assumptions
    revenue_growth_rates: List[float] = None,  # For each projection year
    ebitda_margin: float = None,  # Assumed constant if not provided per year
    projection_years: int = 5,

    # DCF settings
    terminal_method: str = "gordon_growth",
    exit_multiple: float = None,

    # Multiple settings
    industry: str = "manufacturing",
    custom_multiples: Dict = None,

    # Tax
    tax_rate: float = 0.25,
) -> Dict:
    """
    Main entry point for VAM-1.0: Valuation Model.

    Performs comprehensive company valuation using:
    1. DCF (Discounted Cash Flow)
    2. Trading Multiples

    Args:
        revenue: Current year revenue
        ebitda: Current year EBITDA
        ebit: Current year EBIT
        net_income: Current year Net Income
        depreciation: Current year Depreciation & Amortization
        capex: Current year Capital Expenditures
        change_in_nwc: Change in Net Working Capital

        net_debt: Net Debt (Debt - Cash)
        book_equity: Book Value of Equity

        wacc: Weighted Average Cost of Capital
        terminal_growth_rate: Long-term growth rate for Gordon Growth

        revenue_growth_rates: List of growth rates for projection years
        ebitda_margin: EBITDA margin (if constant)
        projection_years: Number of years to project

        terminal_method: "gordon_growth" or "exit_multiple"
        exit_multiple: Exit EV/EBITDA multiple (for exit_multiple method)

        industry: Industry for comparable multiples
        custom_multiples: Custom multiples override

        tax_rate: Corporate tax rate

    Returns:
        Complete valuation analysis with DCF and Multiples
    """
    # Default growth rates if not provided
    if revenue_growth_rates is None:
        revenue_growth_rates = [0.05] * projection_years  # 5% default

    # Default EBITDA margin from current year
    if ebitda_margin is None:
        ebitda_margin = ebitda / revenue if revenue > 0 else 0.15

    # Default book equity
    if book_equity is None:
        book_equity = revenue * 0.3  # Rough approximation

    # Build cash flow projections
    cash_flows = []
    current_revenue = revenue
    current_depreciation = depreciation
    current_capex = capex

    for i, growth_rate in enumerate(revenue_growth_rates[:projection_years]):
        year = 2026 + i  # Starting year

        proj_revenue = current_revenue * (1 + growth_rate)
        proj_ebitda = proj_revenue * ebitda_margin
        proj_depreciation = current_depreciation * (1 + growth_rate * 0.8)  # D&A grows slower
        proj_ebit = proj_ebitda - proj_depreciation
        proj_capex = current_capex * (1 + growth_rate * 1.1)  # CapEx grows faster
        proj_nwc_change = change_in_nwc * (1 + growth_rate)

        cf = CashFlowProjection(
            year=year,
            revenue=proj_revenue,
            ebitda=proj_ebitda,
            ebit=proj_ebit,
            depreciation=proj_depreciation,
            capex=proj_capex,
            change_in_nwc=proj_nwc_change,
            tax_rate=tax_rate,
        )
        cash_flows.append(cf)

        current_revenue = proj_revenue
        current_depreciation = proj_depreciation
        current_capex = proj_capex

    # Terminal method enum
    tv_method = (
        TerminalValueMethod.GORDON_GROWTH
        if terminal_method.lower() == "gordon_growth"
        else TerminalValueMethod.EXIT_MULTIPLE
    )

    # DCF Valuation
    dcf_result = calculate_dcf_valuation(
        cash_flows=cash_flows,
        wacc=wacc,
        terminal_growth_rate=terminal_growth_rate,
        terminal_method=tv_method,
        exit_multiple=exit_multiple,
        net_debt=net_debt,
    )

    # Multiple-Based Valuation
    multiple_result = calculate_multiple_valuation(
        ebitda=ebitda,
        ebit=ebit,
        revenue=revenue,
        net_income=net_income,
        book_equity=book_equity,
        industry=industry,
        custom_multiples=custom_multiples,
        net_debt=net_debt,
    )

    # Football Field
    football_field = create_football_field(dcf_result, multiple_result)

    # Build result
    result = {
        "model": "VAM-1.0",
        "model_name": "Valuation Model (Unternehmensbewertung)",
        "version": "1.0.0",
        "inputs": {
            "revenue": revenue,
            "ebitda": ebitda,
            "ebit": ebit,
            "net_income": net_income,
            "net_debt": net_debt,
            "wacc_percent": round(wacc * 100, 2),
            "terminal_growth_percent": round(terminal_growth_rate * 100, 2),
            "projection_years": projection_years,
            "industry": industry,
        },
        "dcf_valuation": dcf_result,
        "multiple_valuation": multiple_result,
        "football_field": football_field,
        "summary": {
            "enterprise_value": {
                "dcf": dcf_result.get("results", {}).get("enterprise_value", 0),
                "multiples_median": multiple_result.get("summary", {}).get("enterprise_value_range", {}).get("median", 0),
                "average": round(
                    (dcf_result.get("results", {}).get("enterprise_value", 0) +
                     multiple_result.get("summary", {}).get("enterprise_value_range", {}).get("median", 0)) / 2, 2
                ),
            },
            "equity_value": {
                "dcf": dcf_result.get("results", {}).get("equity_value", 0),
                "multiples_median": multiple_result.get("summary", {}).get("equity_value_range", {}).get("median", 0),
                "average": round(
                    (dcf_result.get("results", {}).get("equity_value", 0) +
                     multiple_result.get("summary", {}).get("equity_value_range", {}).get("median", 0)) / 2, 2
                ),
            },
            "implied_multiples_dcf": dcf_result.get("implied_multiples", {}),
        },
        "interpretation": {
            "enterprise_value_range": f"€{football_field['overall_range']['minimum']:,.0f} - €{football_field['overall_range']['maximum']:,.0f}",
            "midpoint": f"€{football_field['overall_range']['weighted_average']:,.0f}",
            "key_drivers": [
                f"WACC: {wacc*100:.1f}%",
                f"Terminal Growth: {terminal_growth_rate*100:.1f}%",
                f"EBITDA Margin: {ebitda_margin*100:.1f}%",
            ],
        },
    }

    return result


if __name__ == "__main__":
    print("=" * 70)
    print("VAM-1.0: Valuation Model - Demo")
    print("=" * 70)

    # Example: Manufacturing company
    result = run_valuation(
        revenue=100_000_000,
        ebitda=15_000_000,
        ebit=10_000_000,
        net_income=7_000_000,
        depreciation=5_000_000,
        capex=6_000_000,
        change_in_nwc=2_000_000,
        net_debt=20_000_000,
        wacc=0.09,
        terminal_growth_rate=0.02,
        projection_years=5,
        revenue_growth_rates=[0.06, 0.05, 0.04, 0.03, 0.02],
        industry="manufacturing",
    )

    print(f"\nModel: {result['model']} ({result['model_name']})")

    print(f"\n--- DCF VALUATION ---")
    dcf = result['dcf_valuation']
    print(f"  Enterprise Value: €{dcf['results']['enterprise_value']:,.0f}")
    print(f"  Equity Value: €{dcf['results']['equity_value']:,.0f}")
    print(f"  Terminal Value as % of EV: {dcf['terminal_value']['tv_as_percent_of_ev']:.1f}%")

    print(f"\n--- MULTIPLE VALUATION ---")
    mult = result['multiple_valuation']
    print(f"  EV Range: €{mult['summary']['enterprise_value_range']['low']:,.0f} - €{mult['summary']['enterprise_value_range']['high']:,.0f}")
    print(f"  EV Median: €{mult['summary']['enterprise_value_range']['median']:,.0f}")

    print(f"\n--- SUMMARY ---")
    summary = result['summary']
    print(f"  Average Enterprise Value: €{summary['enterprise_value']['average']:,.0f}")
    print(f"  Average Equity Value: €{summary['equity_value']['average']:,.0f}")

    print(f"\n--- IMPLIED MULTIPLES (DCF) ---")
    impl = result['dcf_valuation']['implied_multiples']
    print(f"  EV/EBITDA: {impl['ev_ebitda']:.1f}x")
    print(f"  EV/EBIT: {impl['ev_ebit']:.1f}x")
    print(f"  EV/Sales: {impl['ev_sales']:.2f}x")
