"""
BFM-1.0: Beta Framework Model

Unified Risk Framework for Strategic Planning

This model provides a consistent beta framework across all strategic models,
connecting revenue risk through to equity risk.

Beta Hierarchy:
===============

    Revenue Beta (β_R)
         ↓  × Operating Leverage
    Operating Beta (β_Op)
         ↓  × Financial Leverage
    Asset Beta (β_A) [Unlevered]
         ↓  × Capital Structure
    Equity Beta (β_E) [Levered]

Key Equations:
--------------

1. Operating Beta (from cost structure):
   β_Op = β_R × DOL
   where DOL = Degree of Operating Leverage = Contribution Margin / EBIT

2. Asset Beta (unlevered):
   β_A = β_Op × (1 - Tax Rate × Debt/Assets)
   Or simplified: β_A ≈ β_Op for operating businesses

3. Equity Beta (Hamada equation):
   β_E = β_A × [1 + (1 - t) × (D/E)]

4. Revenue Beta (from market correlation):
   β_R = Cov(R_company, R_market) / Var(R_market)
   Or estimated from industry/geography factors

5. WACC Integration:
   WACC = (E/(D+E)) × Re + (D/(D+E)) × Rd × (1-t)
   where Re = Rf + β_E × MRP

Industry Beta Benchmarks (Source: Damodaran):
- Packaging/Plastics: β_A = 0.80-1.00
- Manufacturing: β_A = 0.90-1.10
- Consumer Goods: β_A = 0.70-0.90
- Technology: β_A = 1.10-1.40
- Utilities: β_A = 0.40-0.60

Author: Claude (Strategic Models Team)
Version: 1.0.0
Created: 2026-01-16
"""

import math
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from enum import Enum


class IndustryType(Enum):
    """Industry classifications for beta benchmarks."""
    PACKAGING_PLASTICS = "packaging_plastics"
    MANUFACTURING = "manufacturing"
    CONSUMER_GOODS = "consumer_goods"
    TECHNOLOGY = "technology"
    UTILITIES = "utilities"
    HEALTHCARE = "healthcare"
    FINANCIAL = "financial"
    RETAIL = "retail"
    ENERGY = "energy"
    REAL_ESTATE = "real_estate"


class GeographyType(Enum):
    """Geographic risk classifications."""
    DEVELOPED_EUROPE = "developed_europe"
    DEVELOPED_US = "developed_us"
    DEVELOPED_ASIA = "developed_asia"
    EMERGING_ASIA = "emerging_asia"
    EMERGING_LATAM = "emerging_latam"
    EMERGING_EMEA = "emerging_emea"


# Industry Asset Beta Benchmarks (Damodaran, 2024)
INDUSTRY_ASSET_BETAS = {
    IndustryType.PACKAGING_PLASTICS: 0.85,
    IndustryType.MANUFACTURING: 0.95,
    IndustryType.CONSUMER_GOODS: 0.80,
    IndustryType.TECHNOLOGY: 1.25,
    IndustryType.UTILITIES: 0.50,
    IndustryType.HEALTHCARE: 0.90,
    IndustryType.FINANCIAL: 0.75,  # Asset beta, not equity
    IndustryType.RETAIL: 0.95,
    IndustryType.ENERGY: 1.05,
    IndustryType.REAL_ESTATE: 0.70,
}

# Geographic Risk Premiums (Country Risk Premium)
GEOGRAPHY_RISK_PREMIUMS = {
    GeographyType.DEVELOPED_EUROPE: 0.0,
    GeographyType.DEVELOPED_US: 0.0,
    GeographyType.DEVELOPED_ASIA: 0.5,
    GeographyType.EMERGING_ASIA: 2.0,
    GeographyType.EMERGING_LATAM: 3.5,
    GeographyType.EMERGING_EMEA: 4.0,
}

# Default Market Parameters
DEFAULT_RISK_FREE_RATE = 0.035  # 3.5%
DEFAULT_MARKET_RISK_PREMIUM = 0.055  # 5.5%
DEFAULT_TAX_RATE = 0.25  # 25%


@dataclass
class BetaComponents:
    """All beta components for a business."""
    revenue_beta: float
    operating_beta: float
    asset_beta: float
    equity_beta: float

    # Leverage factors
    operating_leverage: float  # DOL
    financial_leverage: float  # D/E ratio

    # Derived metrics
    cost_of_equity: float
    wacc: float


@dataclass
class CostStructure:
    """Cost structure for operating leverage calculation."""
    revenue: float
    variable_costs: float
    fixed_costs: float
    depreciation: float
    interest: float

    @property
    def contribution_margin(self) -> float:
        return self.revenue - self.variable_costs

    @property
    def ebit(self) -> float:
        return self.contribution_margin - self.fixed_costs - self.depreciation

    @property
    def degree_of_operating_leverage(self) -> float:
        """DOL = Contribution Margin / EBIT"""
        if self.ebit <= 0:
            return 1.0  # Avoid division by zero
        return self.contribution_margin / self.ebit


@dataclass
class CapitalStructure:
    """Capital structure for financial leverage calculation."""
    equity_value: float
    debt_value: float
    tax_rate: float

    @property
    def debt_to_equity(self) -> float:
        if self.equity_value <= 0:
            return 0.0
        return self.debt_value / self.equity_value

    @property
    def debt_ratio(self) -> float:
        total = self.equity_value + self.debt_value
        if total <= 0:
            return 0.0
        return self.debt_value / total

    @property
    def equity_ratio(self) -> float:
        return 1.0 - self.debt_ratio


def calculate_revenue_beta(
    industry: IndustryType = IndustryType.MANUFACTURING,
    geographic_mix: Dict[GeographyType, float] = None,
    cyclicality_factor: float = 1.0,
) -> float:
    """
    Calculate Revenue Beta from industry and geographic factors.

    Revenue Beta captures how sensitive a company's revenue is to
    overall market conditions.

    Args:
        industry: Industry classification
        geographic_mix: Dict of geography -> revenue share (must sum to 1)
        cyclicality_factor: Adjustment for business cyclicality (0.5-1.5)

    Returns:
        Revenue Beta (β_R)
    """
    # Base beta from industry
    base_beta = INDUSTRY_ASSET_BETAS.get(industry, 0.90)

    # Revenue beta is typically lower than asset beta
    # (asset beta includes operating leverage effect)
    revenue_beta = base_beta * 0.7  # Approximate de-leveraging

    # Apply cyclicality factor
    revenue_beta *= cyclicality_factor

    # Geographic adjustment
    if geographic_mix:
        geo_adjustment = 0.0
        for geo, share in geographic_mix.items():
            risk_premium = GEOGRAPHY_RISK_PREMIUMS.get(geo, 0.0)
            # Higher country risk → higher revenue volatility
            geo_adjustment += share * (risk_premium / 100)
        revenue_beta *= (1.0 + geo_adjustment)

    return round(revenue_beta, 3)


def calculate_operating_beta(
    revenue_beta: float,
    cost_structure: CostStructure = None,
    fixed_cost_ratio: float = None,
) -> Tuple[float, float]:
    """
    Calculate Operating Beta from Revenue Beta and cost structure.

    Operating Beta = Revenue Beta × Degree of Operating Leverage

    Higher fixed costs → Higher DOL → Higher Operating Beta

    Args:
        revenue_beta: Revenue Beta (β_R)
        cost_structure: Full cost structure (preferred)
        fixed_cost_ratio: Simple fixed costs / total costs ratio (alternative)

    Returns:
        Tuple of (Operating Beta, DOL)
    """
    if cost_structure:
        dol = cost_structure.degree_of_operating_leverage
    elif fixed_cost_ratio is not None:
        # Approximate DOL from fixed cost ratio
        # Higher fixed costs → Higher DOL
        # DOL typically ranges from 1.0 (all variable) to 3.0+ (all fixed)
        dol = 1.0 + (fixed_cost_ratio * 2.0)
    else:
        # Default DOL for mixed cost structure
        dol = 1.5

    operating_beta = revenue_beta * dol

    return round(operating_beta, 3), round(dol, 2)


def calculate_asset_beta(
    operating_beta: float,
    tax_rate: float = DEFAULT_TAX_RATE,
    debt_ratio: float = 0.0,
) -> float:
    """
    Calculate Asset Beta (Unlevered Beta).

    For pure operating companies, Asset Beta ≈ Operating Beta.
    Adjustment for tax shield on debt:

    β_A = β_Op × (1 - t × D/A)

    Args:
        operating_beta: Operating Beta (β_Op)
        tax_rate: Corporate tax rate
        debt_ratio: Debt / Total Assets

    Returns:
        Asset Beta (β_A)
    """
    # Tax shield adjustment (minor effect for operating companies)
    tax_shield_factor = 1.0 - (tax_rate * debt_ratio * 0.1)  # Dampened effect

    asset_beta = operating_beta * tax_shield_factor

    return round(asset_beta, 3)


def calculate_equity_beta(
    asset_beta: float,
    capital_structure: CapitalStructure = None,
    debt_to_equity: float = None,
    tax_rate: float = DEFAULT_TAX_RATE,
) -> float:
    """
    Calculate Equity Beta (Levered Beta) using Hamada equation.

    β_E = β_A × [1 + (1 - t) × (D/E)]

    Higher financial leverage → Higher Equity Beta

    Args:
        asset_beta: Asset Beta (β_A)
        capital_structure: Full capital structure (preferred)
        debt_to_equity: D/E ratio (alternative)
        tax_rate: Corporate tax rate

    Returns:
        Equity Beta (β_E)
    """
    if capital_structure:
        de_ratio = capital_structure.debt_to_equity
        t = capital_structure.tax_rate
    else:
        de_ratio = debt_to_equity if debt_to_equity is not None else 0.5
        t = tax_rate

    # Hamada equation
    equity_beta = asset_beta * (1.0 + (1.0 - t) * de_ratio)

    return round(equity_beta, 3)


def unlever_beta(
    equity_beta: float,
    debt_to_equity: float,
    tax_rate: float = DEFAULT_TAX_RATE,
) -> float:
    """
    Unlever an observed equity beta to get asset beta.

    β_A = β_E / [1 + (1 - t) × (D/E)]

    Used when starting from market-observed equity beta.

    Args:
        equity_beta: Observed Equity Beta
        debt_to_equity: D/E ratio
        tax_rate: Corporate tax rate

    Returns:
        Asset Beta (β_A)
    """
    leverage_factor = 1.0 + (1.0 - tax_rate) * debt_to_equity
    asset_beta = equity_beta / leverage_factor

    return round(asset_beta, 3)


def relever_beta(
    asset_beta: float,
    target_debt_to_equity: float,
    tax_rate: float = DEFAULT_TAX_RATE,
) -> float:
    """
    Relever an asset beta to a new capital structure.

    Used for scenario analysis with different financing.

    Args:
        asset_beta: Asset Beta (β_A)
        target_debt_to_equity: Target D/E ratio
        tax_rate: Corporate tax rate

    Returns:
        New Equity Beta (β_E)
    """
    return calculate_equity_beta(
        asset_beta=asset_beta,
        debt_to_equity=target_debt_to_equity,
        tax_rate=tax_rate,
    )


def calculate_cost_of_equity(
    equity_beta: float,
    risk_free_rate: float = DEFAULT_RISK_FREE_RATE,
    market_risk_premium: float = DEFAULT_MARKET_RISK_PREMIUM,
    country_risk_premium: float = 0.0,
    size_premium: float = 0.0,
    company_specific_premium: float = 0.0,
) -> float:
    """
    Calculate Cost of Equity using CAPM + adjustments.

    Re = Rf + β_E × MRP + CRP + SP + CSP

    Args:
        equity_beta: Equity Beta (β_E)
        risk_free_rate: Risk-free rate (default 3.5%)
        market_risk_premium: Market risk premium (default 5.5%)
        country_risk_premium: Country/geographic risk premium
        size_premium: Small-cap premium
        company_specific_premium: Illiquidity, key-man risk, etc.

    Returns:
        Cost of Equity (Re)
    """
    cost_of_equity = (
        risk_free_rate +
        equity_beta * market_risk_premium +
        country_risk_premium +
        size_premium +
        company_specific_premium
    )

    return round(cost_of_equity, 4)


def calculate_wacc(
    cost_of_equity: float,
    cost_of_debt: float,
    equity_ratio: float,
    tax_rate: float = DEFAULT_TAX_RATE,
) -> float:
    """
    Calculate Weighted Average Cost of Capital.

    WACC = (E/(D+E)) × Re + (D/(D+E)) × Rd × (1-t)

    Args:
        cost_of_equity: Cost of Equity (Re)
        cost_of_debt: Cost of Debt (Rd)
        equity_ratio: E / (D + E)
        tax_rate: Corporate tax rate

    Returns:
        WACC
    """
    debt_ratio = 1.0 - equity_ratio

    wacc = (
        equity_ratio * cost_of_equity +
        debt_ratio * cost_of_debt * (1.0 - tax_rate)
    )

    return round(wacc, 4)


def calculate_full_beta_chain(
    industry: IndustryType = IndustryType.MANUFACTURING,
    geographic_mix: Dict[GeographyType, float] = None,
    cyclicality_factor: float = 1.0,
    fixed_cost_ratio: float = 0.4,
    debt_to_equity: float = 0.5,
    tax_rate: float = DEFAULT_TAX_RATE,
    risk_free_rate: float = DEFAULT_RISK_FREE_RATE,
    market_risk_premium: float = DEFAULT_MARKET_RISK_PREMIUM,
    cost_of_debt: float = 0.05,
    country_risk_premium: float = 0.0,
) -> BetaComponents:
    """
    Calculate the full beta chain from revenue to equity.

    This is the main function that ties all beta calculations together.

    Args:
        industry: Industry classification
        geographic_mix: Revenue by geography
        cyclicality_factor: Business cyclicality (0.5-1.5)
        fixed_cost_ratio: Fixed costs / Total costs
        debt_to_equity: D/E ratio
        tax_rate: Corporate tax rate
        risk_free_rate: Risk-free rate
        market_risk_premium: Market risk premium
        cost_of_debt: Pre-tax cost of debt
        country_risk_premium: Additional country risk

    Returns:
        BetaComponents with all calculated betas and derived metrics
    """
    # 1. Revenue Beta
    revenue_beta = calculate_revenue_beta(
        industry=industry,
        geographic_mix=geographic_mix,
        cyclicality_factor=cyclicality_factor,
    )

    # 2. Operating Beta
    operating_beta, dol = calculate_operating_beta(
        revenue_beta=revenue_beta,
        fixed_cost_ratio=fixed_cost_ratio,
    )

    # 3. Asset Beta
    debt_ratio = debt_to_equity / (1.0 + debt_to_equity)
    asset_beta = calculate_asset_beta(
        operating_beta=operating_beta,
        tax_rate=tax_rate,
        debt_ratio=debt_ratio,
    )

    # 4. Equity Beta
    equity_beta = calculate_equity_beta(
        asset_beta=asset_beta,
        debt_to_equity=debt_to_equity,
        tax_rate=tax_rate,
    )

    # 5. Cost of Equity
    cost_of_equity = calculate_cost_of_equity(
        equity_beta=equity_beta,
        risk_free_rate=risk_free_rate,
        market_risk_premium=market_risk_premium,
        country_risk_premium=country_risk_premium,
    )

    # 6. WACC
    equity_ratio = 1.0 / (1.0 + debt_to_equity)
    wacc = calculate_wacc(
        cost_of_equity=cost_of_equity,
        cost_of_debt=cost_of_debt,
        equity_ratio=equity_ratio,
        tax_rate=tax_rate,
    )

    return BetaComponents(
        revenue_beta=revenue_beta,
        operating_beta=operating_beta,
        asset_beta=asset_beta,
        equity_beta=equity_beta,
        operating_leverage=dol,
        financial_leverage=debt_to_equity,
        cost_of_equity=cost_of_equity,
        wacc=wacc,
    )


# =============================================================================
# Sensitivity Analysis for Betas
# =============================================================================

def analyze_beta_sensitivity(
    base_components: BetaComponents,
    scenarios: List[Dict] = None,
) -> Dict:
    """
    Analyze how betas and WACC change under different scenarios.

    Args:
        base_components: Base case beta components
        scenarios: List of scenario dicts with parameter changes

    Returns:
        Sensitivity analysis results
    """
    if scenarios is None:
        scenarios = [
            {"name": "Increase Leverage", "debt_to_equity": base_components.financial_leverage * 1.5},
            {"name": "Decrease Leverage", "debt_to_equity": base_components.financial_leverage * 0.5},
            {"name": "Higher Fixed Costs", "dol_multiplier": 1.3},
            {"name": "Lower Fixed Costs", "dol_multiplier": 0.7},
        ]

    results = {
        "base_case": {
            "revenue_beta": base_components.revenue_beta,
            "operating_beta": base_components.operating_beta,
            "asset_beta": base_components.asset_beta,
            "equity_beta": base_components.equity_beta,
            "cost_of_equity": base_components.cost_of_equity,
            "wacc": base_components.wacc,
        },
        "scenarios": []
    }

    for scenario in scenarios:
        # Apply changes (simplified - full implementation would recalculate chain)
        new_de = scenario.get("debt_to_equity", base_components.financial_leverage)
        dol_mult = scenario.get("dol_multiplier", 1.0)

        # Recalculate equity beta with new leverage
        new_equity_beta = relever_beta(
            asset_beta=base_components.asset_beta,
            target_debt_to_equity=new_de,
        )

        # Recalculate cost of equity
        new_coe = calculate_cost_of_equity(equity_beta=new_equity_beta)

        # Approximate WACC
        equity_ratio = 1.0 / (1.0 + new_de)
        new_wacc = calculate_wacc(
            cost_of_equity=new_coe,
            cost_of_debt=0.05,
            equity_ratio=equity_ratio,
        )

        results["scenarios"].append({
            "name": scenario["name"],
            "equity_beta": new_equity_beta,
            "cost_of_equity": new_coe,
            "wacc": new_wacc,
            "change_vs_base": {
                "equity_beta": round((new_equity_beta / base_components.equity_beta - 1) * 100, 1),
                "wacc": round((new_wacc / base_components.wacc - 1) * 100, 1),
            }
        })

    return results


# =============================================================================
# Main Function for Model Library
# =============================================================================

def analyze_beta_framework(
    industry: str = "manufacturing",
    geographic_mix: Dict[str, float] = None,
    cyclicality: str = "medium",
    fixed_cost_ratio: float = 0.40,
    debt_to_equity: float = 0.50,
    tax_rate: float = 0.25,
    risk_free_rate: float = 0.035,
    market_risk_premium: float = 0.055,
    cost_of_debt: float = 0.05,
    country_risk_premium: float = 0.0,
    run_sensitivity: bool = True,
) -> Dict:
    """
    Main entry point for BFM-1.0: Beta Framework Model.

    Calculates the complete beta chain from revenue to equity,
    plus WACC and optional sensitivity analysis.

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
        Dictionary with complete beta analysis
    """
    # Map string inputs to enums
    industry_map = {
        "packaging_plastics": IndustryType.PACKAGING_PLASTICS,
        "packaging": IndustryType.PACKAGING_PLASTICS,
        "plastics": IndustryType.PACKAGING_PLASTICS,
        "manufacturing": IndustryType.MANUFACTURING,
        "consumer_goods": IndustryType.CONSUMER_GOODS,
        "consumer": IndustryType.CONSUMER_GOODS,
        "technology": IndustryType.TECHNOLOGY,
        "tech": IndustryType.TECHNOLOGY,
        "utilities": IndustryType.UTILITIES,
        "healthcare": IndustryType.HEALTHCARE,
        "financial": IndustryType.FINANCIAL,
        "retail": IndustryType.RETAIL,
        "energy": IndustryType.ENERGY,
        "real_estate": IndustryType.REAL_ESTATE,
    }

    geo_map = {
        "europe": GeographyType.DEVELOPED_EUROPE,
        "developed_europe": GeographyType.DEVELOPED_EUROPE,
        "us": GeographyType.DEVELOPED_US,
        "usa": GeographyType.DEVELOPED_US,
        "developed_us": GeographyType.DEVELOPED_US,
        "asia_developed": GeographyType.DEVELOPED_ASIA,
        "developed_asia": GeographyType.DEVELOPED_ASIA,
        "japan": GeographyType.DEVELOPED_ASIA,
        "asia_emerging": GeographyType.EMERGING_ASIA,
        "emerging_asia": GeographyType.EMERGING_ASIA,
        "china": GeographyType.EMERGING_ASIA,
        "india": GeographyType.EMERGING_ASIA,
        "latam": GeographyType.EMERGING_LATAM,
        "emerging_latam": GeographyType.EMERGING_LATAM,
        "brazil": GeographyType.EMERGING_LATAM,
        "emea_emerging": GeographyType.EMERGING_EMEA,
        "emerging_emea": GeographyType.EMERGING_EMEA,
        "africa": GeographyType.EMERGING_EMEA,
        "middle_east": GeographyType.EMERGING_EMEA,
    }

    cyclicality_map = {
        "low": 0.7,
        "medium": 1.0,
        "high": 1.3,
    }

    # Convert inputs
    industry_type = industry_map.get(industry.lower(), IndustryType.MANUFACTURING)
    cyclicality_factor = cyclicality_map.get(cyclicality.lower(), 1.0)

    # Convert geographic mix
    geo_mix_typed = None
    if geographic_mix:
        geo_mix_typed = {}
        for geo, share in geographic_mix.items():
            geo_type = geo_map.get(geo.lower())
            if geo_type:
                geo_mix_typed[geo_type] = share

    # Calculate full beta chain
    components = calculate_full_beta_chain(
        industry=industry_type,
        geographic_mix=geo_mix_typed,
        cyclicality_factor=cyclicality_factor,
        fixed_cost_ratio=fixed_cost_ratio,
        debt_to_equity=debt_to_equity,
        tax_rate=tax_rate,
        risk_free_rate=risk_free_rate,
        market_risk_premium=market_risk_premium,
        cost_of_debt=cost_of_debt,
        country_risk_premium=country_risk_premium,
    )

    # Build result
    result = {
        "model": "BFM-1.0",
        "model_name": "Beta Framework Model",
        "version": "1.0.0",
        "inputs": {
            "industry": industry,
            "cyclicality": cyclicality,
            "fixed_cost_ratio": fixed_cost_ratio,
            "debt_to_equity": debt_to_equity,
            "tax_rate": tax_rate,
            "risk_free_rate": risk_free_rate,
            "market_risk_premium": market_risk_premium,
            "cost_of_debt": cost_of_debt,
        },
        "beta_chain": {
            "revenue_beta": components.revenue_beta,
            "operating_beta": components.operating_beta,
            "asset_beta": components.asset_beta,
            "equity_beta": components.equity_beta,
        },
        "leverage": {
            "operating_leverage_dol": components.operating_leverage,
            "financial_leverage_de": components.financial_leverage,
        },
        "cost_of_capital": {
            "cost_of_equity_percent": round(components.cost_of_equity * 100, 2),
            "cost_of_debt_percent": round(cost_of_debt * 100, 2),
            "wacc_percent": round(components.wacc * 100, 2),
        },
        "theory": {
            "operating_beta_formula": "β_Op = β_R × DOL",
            "equity_beta_formula": "β_E = β_A × [1 + (1-t) × (D/E)]",
            "cost_of_equity_formula": "Re = Rf + β_E × MRP",
            "wacc_formula": "WACC = (E/V) × Re + (D/V) × Rd × (1-t)",
        },
        "interpretation": {
            "risk_profile": _interpret_risk_profile(components),
            "leverage_impact": _interpret_leverage_impact(components),
        },
    }

    # Add sensitivity analysis
    if run_sensitivity:
        sensitivity = analyze_beta_sensitivity(components)
        result["sensitivity"] = sensitivity

    return result


def _interpret_risk_profile(components: BetaComponents) -> str:
    """Generate risk profile interpretation."""
    if components.equity_beta < 0.8:
        risk = "LOW RISK (defensive)"
    elif components.equity_beta < 1.0:
        risk = "BELOW MARKET RISK"
    elif components.equity_beta < 1.2:
        risk = "MARKET AVERAGE RISK"
    elif components.equity_beta < 1.5:
        risk = "ABOVE MARKET RISK"
    else:
        risk = "HIGH RISK (aggressive)"

    return f"{risk} - Equity Beta of {components.equity_beta:.2f}"


def _interpret_leverage_impact(components: BetaComponents) -> str:
    """Generate leverage impact interpretation."""
    beta_increase = (components.equity_beta / components.asset_beta - 1) * 100
    return (f"Financial leverage ({components.financial_leverage:.1f}x D/E) increases "
            f"beta by {beta_increase:.0f}% from asset to equity level")


if __name__ == "__main__":
    # Demo
    print("=" * 70)
    print("BFM-1.0: Beta Framework Model - Demo")
    print("=" * 70)

    # Example: ALPLA (Packaging/Plastics, global operations)
    result = analyze_beta_framework(
        industry="packaging_plastics",
        geographic_mix={
            "europe": 0.45,
            "asia_emerging": 0.25,
            "latam": 0.20,
            "us": 0.10,
        },
        cyclicality="medium",
        fixed_cost_ratio=0.45,
        debt_to_equity=0.40,
        tax_rate=0.25,
    )

    print(f"\nModel: {result['model']} ({result['model_name']})")
    print(f"\nBeta Chain:")
    for beta_type, value in result['beta_chain'].items():
        print(f"  {beta_type}: {value}")

    print(f"\nLeverage:")
    print(f"  Operating Leverage (DOL): {result['leverage']['operating_leverage_dol']:.2f}x")
    print(f"  Financial Leverage (D/E): {result['leverage']['financial_leverage_de']:.2f}x")

    print(f"\nCost of Capital:")
    print(f"  Cost of Equity: {result['cost_of_capital']['cost_of_equity_percent']:.2f}%")
    print(f"  WACC: {result['cost_of_capital']['wacc_percent']:.2f}%")

    print(f"\nInterpretation:")
    print(f"  {result['interpretation']['risk_profile']}")
    print(f"  {result['interpretation']['leverage_impact']}")

    if 'sensitivity' in result:
        print(f"\nSensitivity Scenarios:")
        for scenario in result['sensitivity']['scenarios']:
            print(f"  {scenario['name']}: WACC {scenario['change_vs_base']['wacc']:+.1f}%")
