"""
CMM-1.0: Capital Market Model (Kapitalmarkt-Modul)

Capital Market Parameters for Strategic Planning

This model provides all capital market parameters needed for
WACC calculation and valuation models.

=============================================================================
KAPITALMARKT-PARAMETER
=============================================================================

Cost of Equity Components:
    Re = Rf + β_E × MRP + CRP + SP + IP + CSP

Where:
    Rf  = Risk-Free Rate (Risikofreier Zins)
    MRP = Market Risk Premium (Marktrisikoprämie)
    CRP = Country Risk Premium (Länderrisikoprämie)
    SP  = Size Premium (Größenprämie)
    IP  = Illiquidity Premium (Illiquiditätsprämie)
    CSP = Company-Specific Premium (Unternehmensspezifische Prämie)

Cost of Debt Components:
    Rd = Rf + Credit Spread + Country Spread

=============================================================================
DATA SOURCES
=============================================================================

Risk-Free Rate (Rf):
    - Germany: 10Y Bund yield
    - US: 10Y Treasury yield
    - Switzerland: 10Y Confederation bond

Market Risk Premium (MRP):
    - Historical: Long-term equity premium over bonds
    - Implied: From current market valuations
    - Survey: Analyst expectations

Country Risk Premium (CRP):
    - Damodaran country risk data
    - Based on sovereign ratings and CDS spreads

Size Premium (SP):
    - Based on market cap deciles
    - Duff & Phelps / Ibbotson data

Credit Spreads:
    - By credit rating (AAA to CCC)
    - Corporate bond yields over government

Author: Claude (Strategic Models Team)
Version: 1.0.0
Created: 2026-01-16
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from enum import Enum
from datetime import date


class Currency(Enum):
    """Supported currencies for capital market data."""
    EUR = "EUR"
    USD = "USD"
    CHF = "CHF"
    GBP = "GBP"


class CreditRating(Enum):
    """Credit rating categories."""
    AAA = "AAA"
    AA = "AA"
    A = "A"
    BBB = "BBB"
    BB = "BB"
    B = "B"
    CCC = "CCC"


class CompanySize(Enum):
    """Company size categories for size premium."""
    MEGA_CAP = "mega_cap"      # > €50B
    LARGE_CAP = "large_cap"    # €10B - €50B
    MID_CAP = "mid_cap"        # €2B - €10B
    SMALL_CAP = "small_cap"    # €300M - €2B
    MICRO_CAP = "micro_cap"    # < €300M
    PRIVATE = "private"        # Not publicly traded


class Region(Enum):
    """Geographic regions for market parameters."""
    EUROPE_DEVELOPED = "europe_developed"
    EUROPE_EMERGING = "europe_emerging"
    US = "us"
    ASIA_DEVELOPED = "asia_developed"
    ASIA_EMERGING = "asia_emerging"
    LATAM = "latam"
    MIDDLE_EAST = "middle_east"
    AFRICA = "africa"


# =============================================================================
# Market Data (as of Q1 2026 - Update periodically)
# =============================================================================

# Risk-Free Rates by Currency (10Y Government Bonds)
RISK_FREE_RATES = {
    Currency.EUR: 0.025,   # 2.5% - German Bund
    Currency.USD: 0.040,   # 4.0% - US Treasury
    Currency.CHF: 0.010,   # 1.0% - Swiss Confederation
    Currency.GBP: 0.035,   # 3.5% - UK Gilt
}

# Market Risk Premium (Equity Risk Premium)
# Source: Damodaran, Duff & Phelps
MARKET_RISK_PREMIUM = {
    "historical_geometric": 0.045,   # 4.5% - Long-term geometric average
    "historical_arithmetic": 0.060,  # 6.0% - Long-term arithmetic average
    "implied_current": 0.055,        # 5.5% - Current implied from market
    "survey_consensus": 0.055,       # 5.5% - Analyst survey consensus
    "recommended": 0.055,            # 5.5% - Recommended for planning
}

# Country Risk Premiums by Region
# Source: Damodaran Country Risk Data
COUNTRY_RISK_PREMIUMS = {
    Region.EUROPE_DEVELOPED: 0.00,    # 0.0% - Germany, France, Netherlands, etc.
    Region.EUROPE_EMERGING: 0.025,    # 2.5% - Poland, Czech, Hungary
    Region.US: 0.00,                  # 0.0% - United States
    Region.ASIA_DEVELOPED: 0.005,     # 0.5% - Japan, Singapore, Australia
    Region.ASIA_EMERGING: 0.020,      # 2.0% - China, India, Indonesia
    Region.LATAM: 0.035,              # 3.5% - Brazil, Mexico, Argentina
    Region.MIDDLE_EAST: 0.025,        # 2.5% - UAE, Saudi Arabia
    Region.AFRICA: 0.045,             # 4.5% - South Africa, Nigeria
}

# Specific Country Risk Premiums (selected countries)
COUNTRY_SPECIFIC_PREMIUMS = {
    # Europe Developed
    "germany": 0.00, "austria": 0.00, "switzerland": 0.00,
    "netherlands": 0.00, "france": 0.005, "uk": 0.005,
    "spain": 0.010, "italy": 0.015, "portugal": 0.015,
    # Europe Emerging
    "poland": 0.015, "czech": 0.010, "hungary": 0.025,
    "romania": 0.030, "turkey": 0.045, "russia": 0.060,
    # Americas
    "usa": 0.00, "canada": 0.00,
    "mexico": 0.025, "brazil": 0.035, "argentina": 0.055,
    # Asia
    "japan": 0.005, "australia": 0.00, "singapore": 0.00,
    "china": 0.015, "india": 0.020, "indonesia": 0.025,
    "vietnam": 0.030, "thailand": 0.015,
    # Middle East & Africa
    "uae": 0.010, "saudi": 0.015,
    "south_africa": 0.030, "nigeria": 0.050,
}

# Size Premium by Company Size
# Source: Duff & Phelps Risk Premium Report
SIZE_PREMIUMS = {
    CompanySize.MEGA_CAP: 0.00,     # 0.0% - No size premium
    CompanySize.LARGE_CAP: 0.005,   # 0.5%
    CompanySize.MID_CAP: 0.015,     # 1.5%
    CompanySize.SMALL_CAP: 0.030,   # 3.0%
    CompanySize.MICRO_CAP: 0.045,   # 4.5%
    CompanySize.PRIVATE: 0.050,     # 5.0% - Private company premium
}

# Illiquidity Premium
ILLIQUIDITY_PREMIUMS = {
    "public_liquid": 0.00,         # 0.0% - Listed, liquid shares
    "public_illiquid": 0.010,      # 1.0% - Listed, low volume
    "private_strategic": 0.020,    # 2.0% - Private, strategic buyer exists
    "private_pe_backed": 0.025,    # 2.5% - Private, PE-backed
    "private_family": 0.035,       # 3.5% - Private family business
    "private_distressed": 0.050,   # 5.0% - Private, distressed
}

# Credit Spreads by Rating (over risk-free)
# Source: Corporate bond indices
CREDIT_SPREADS = {
    CreditRating.AAA: 0.005,   # 0.5%
    CreditRating.AA: 0.008,    # 0.8%
    CreditRating.A: 0.012,     # 1.2%
    CreditRating.BBB: 0.018,   # 1.8%
    CreditRating.BB: 0.035,    # 3.5%
    CreditRating.B: 0.055,     # 5.5%
    CreditRating.CCC: 0.090,   # 9.0%
}


@dataclass
class CapitalMarketParameters:
    """Complete set of capital market parameters."""
    # Base rates
    risk_free_rate: float
    market_risk_premium: float

    # Premiums
    country_risk_premium: float
    size_premium: float
    illiquidity_premium: float
    company_specific_premium: float

    # Debt parameters
    credit_spread: float
    cost_of_debt_pretax: float

    # Derived values
    base_cost_of_equity: float  # Rf + MRP (before beta)
    total_equity_premium: float  # CRP + SP + IP + CSP


def get_risk_free_rate(currency: Currency = Currency.EUR) -> float:
    """Get current risk-free rate for currency."""
    return RISK_FREE_RATES.get(currency, RISK_FREE_RATES[Currency.EUR])


def get_market_risk_premium(method: str = "recommended") -> float:
    """Get market risk premium by estimation method."""
    return MARKET_RISK_PREMIUM.get(method, MARKET_RISK_PREMIUM["recommended"])


def get_country_risk_premium(
    country: str = None,
    region: Region = None,
) -> float:
    """Get country risk premium."""
    if country:
        country_lower = country.lower().replace(" ", "_")
        if country_lower in COUNTRY_SPECIFIC_PREMIUMS:
            return COUNTRY_SPECIFIC_PREMIUMS[country_lower]

    if region:
        return COUNTRY_RISK_PREMIUMS.get(region, 0.0)

    return 0.0


def get_size_premium(
    market_cap: float = None,
    size_category: CompanySize = None,
) -> float:
    """Get size premium based on market cap or category."""
    if size_category:
        return SIZE_PREMIUMS.get(size_category, 0.0)

    if market_cap is not None:
        # Market cap in millions
        if market_cap >= 50000:
            return SIZE_PREMIUMS[CompanySize.MEGA_CAP]
        elif market_cap >= 10000:
            return SIZE_PREMIUMS[CompanySize.LARGE_CAP]
        elif market_cap >= 2000:
            return SIZE_PREMIUMS[CompanySize.MID_CAP]
        elif market_cap >= 300:
            return SIZE_PREMIUMS[CompanySize.SMALL_CAP]
        else:
            return SIZE_PREMIUMS[CompanySize.MICRO_CAP]

    return 0.0


def get_illiquidity_premium(liquidity_status: str = "public_liquid") -> float:
    """Get illiquidity premium."""
    return ILLIQUIDITY_PREMIUMS.get(liquidity_status, 0.0)


def get_credit_spread(rating: CreditRating = CreditRating.BBB) -> float:
    """Get credit spread for rating."""
    return CREDIT_SPREADS.get(rating, CREDIT_SPREADS[CreditRating.BBB])


def calculate_cost_of_equity(
    equity_beta: float,
    risk_free_rate: float,
    market_risk_premium: float,
    country_risk_premium: float = 0.0,
    size_premium: float = 0.0,
    illiquidity_premium: float = 0.0,
    company_specific_premium: float = 0.0,
) -> Dict:
    """
    Calculate Cost of Equity with all components.

    Re = Rf + β_E × MRP + CRP + SP + IP + CSP

    Returns detailed breakdown.
    """
    # CAPM component
    capm_premium = equity_beta * market_risk_premium

    # Total additional premiums
    total_additional = (
        country_risk_premium +
        size_premium +
        illiquidity_premium +
        company_specific_premium
    )

    # Total cost of equity
    cost_of_equity = risk_free_rate + capm_premium + total_additional

    return {
        "cost_of_equity": round(cost_of_equity, 4),
        "cost_of_equity_percent": round(cost_of_equity * 100, 2),
        "components": {
            "risk_free_rate": round(risk_free_rate * 100, 2),
            "capm_premium": round(capm_premium * 100, 2),
            "country_risk_premium": round(country_risk_premium * 100, 2),
            "size_premium": round(size_premium * 100, 2),
            "illiquidity_premium": round(illiquidity_premium * 100, 2),
            "company_specific_premium": round(company_specific_premium * 100, 2),
        },
        "formula": "Re = Rf + β×MRP + CRP + SP + IP + CSP",
        "calculation": (
            f"Re = {risk_free_rate*100:.1f}% + {equity_beta:.2f}×{market_risk_premium*100:.1f}% + "
            f"{country_risk_premium*100:.1f}% + {size_premium*100:.1f}% + "
            f"{illiquidity_premium*100:.1f}% + {company_specific_premium*100:.1f}%"
        ),
    }


def calculate_cost_of_debt(
    risk_free_rate: float,
    credit_rating: CreditRating = CreditRating.BBB,
    country_spread: float = 0.0,
    company_spread: float = 0.0,
) -> Dict:
    """
    Calculate pre-tax Cost of Debt.

    Rd = Rf + Credit Spread + Country Spread + Company Spread
    """
    credit_spread = get_credit_spread(credit_rating)

    cost_of_debt = risk_free_rate + credit_spread + country_spread + company_spread

    return {
        "cost_of_debt_pretax": round(cost_of_debt, 4),
        "cost_of_debt_percent": round(cost_of_debt * 100, 2),
        "components": {
            "risk_free_rate": round(risk_free_rate * 100, 2),
            "credit_spread": round(credit_spread * 100, 2),
            "country_spread": round(country_spread * 100, 2),
            "company_spread": round(company_spread * 100, 2),
        },
        "credit_rating": credit_rating.value,
        "formula": "Rd = Rf + Credit Spread + Country Spread",
    }


def calculate_wacc_from_market_data(
    equity_beta: float,
    debt_to_equity: float,
    tax_rate: float = 0.25,
    currency: Currency = Currency.EUR,
    country: str = None,
    region: Region = None,
    company_size: CompanySize = None,
    market_cap: float = None,
    liquidity_status: str = "public_liquid",
    credit_rating: CreditRating = CreditRating.BBB,
    company_specific_premium: float = 0.0,
) -> Dict:
    """
    Calculate WACC using current market data.

    This is the main function that assembles all capital market
    parameters and calculates WACC.
    """
    # Get base rates
    rf = get_risk_free_rate(currency)
    mrp = get_market_risk_premium("recommended")

    # Get premiums
    crp = get_country_risk_premium(country, region)
    sp = get_size_premium(market_cap, company_size)
    ip = get_illiquidity_premium(liquidity_status)

    # Calculate cost of equity
    coe_result = calculate_cost_of_equity(
        equity_beta=equity_beta,
        risk_free_rate=rf,
        market_risk_premium=mrp,
        country_risk_premium=crp,
        size_premium=sp,
        illiquidity_premium=ip,
        company_specific_premium=company_specific_premium,
    )

    # Calculate cost of debt
    cod_result = calculate_cost_of_debt(
        risk_free_rate=rf,
        credit_rating=credit_rating,
        country_spread=crp * 0.5,  # Debt country spread typically lower
    )

    # Capital structure weights
    equity_weight = 1 / (1 + debt_to_equity)
    debt_weight = debt_to_equity / (1 + debt_to_equity)

    # WACC
    cost_of_equity = coe_result["cost_of_equity"]
    cost_of_debt = cod_result["cost_of_debt_pretax"]

    wacc = (
        equity_weight * cost_of_equity +
        debt_weight * cost_of_debt * (1 - tax_rate)
    )

    return {
        "wacc": round(wacc, 4),
        "wacc_percent": round(wacc * 100, 2),
        "cost_of_equity": coe_result,
        "cost_of_debt": cod_result,
        "capital_structure": {
            "debt_to_equity": debt_to_equity,
            "equity_weight_percent": round(equity_weight * 100, 1),
            "debt_weight_percent": round(debt_weight * 100, 1),
        },
        "tax_rate_percent": round(tax_rate * 100, 1),
        "wacc_formula": "WACC = (E/V)×Re + (D/V)×Rd×(1-t)",
        "wacc_calculation": (
            f"WACC = {equity_weight*100:.1f}%×{cost_of_equity*100:.1f}% + "
            f"{debt_weight*100:.1f}%×{cost_of_debt*100:.1f}%×(1-{tax_rate*100:.0f}%)"
        ),
    }


# =============================================================================
# Main Function for Model Library
# =============================================================================

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
) -> Dict:
    """
    Main entry point for CMM-1.0: Capital Market Model.

    Provides all capital market parameters for WACC calculation.

    Args:
        equity_beta: Equity beta (β_E)
        debt_to_equity: D/E ratio
        tax_rate: Corporate tax rate
        currency: "EUR", "USD", "CHF", "GBP"
        country: Country name (e.g., "germany", "brazil")
        region: Region if country not specified
        company_size: "mega_cap", "large_cap", "mid_cap", "small_cap", "micro_cap", "private"
        market_cap_millions: Market cap in millions (alternative to company_size)
        is_public: Is company publicly traded?
        is_liquid: Are shares liquid?
        credit_rating: "AAA", "AA", "A", "BBB", "BB", "B", "CCC"
        company_specific_premium: Additional company-specific risk (0.0-0.10)
        show_benchmarks: Include market benchmarks in output

    Returns:
        Complete capital market analysis with WACC
    """
    # Map string inputs to enums
    currency_map = {
        "EUR": Currency.EUR, "USD": Currency.USD,
        "CHF": Currency.CHF, "GBP": Currency.GBP,
    }

    region_map = {
        "europe": Region.EUROPE_DEVELOPED,
        "europe_developed": Region.EUROPE_DEVELOPED,
        "europe_emerging": Region.EUROPE_EMERGING,
        "us": Region.US, "usa": Region.US,
        "asia": Region.ASIA_DEVELOPED,
        "asia_developed": Region.ASIA_DEVELOPED,
        "asia_emerging": Region.ASIA_EMERGING,
        "latam": Region.LATAM,
        "middle_east": Region.MIDDLE_EAST,
        "africa": Region.AFRICA,
    }

    size_map = {
        "mega_cap": CompanySize.MEGA_CAP,
        "large_cap": CompanySize.LARGE_CAP,
        "mid_cap": CompanySize.MID_CAP,
        "small_cap": CompanySize.SMALL_CAP,
        "micro_cap": CompanySize.MICRO_CAP,
        "private": CompanySize.PRIVATE,
    }

    rating_map = {
        "AAA": CreditRating.AAA, "AA": CreditRating.AA,
        "A": CreditRating.A, "BBB": CreditRating.BBB,
        "BB": CreditRating.BB, "B": CreditRating.B,
        "CCC": CreditRating.CCC,
    }

    # Convert inputs
    curr = currency_map.get(currency.upper(), Currency.EUR)
    reg = region_map.get(region.lower()) if region else None
    size = size_map.get(company_size.lower()) if company_size else None
    rating = rating_map.get(credit_rating.upper(), CreditRating.BBB)

    # Determine liquidity status
    if not is_public:
        liquidity = "private_family"
    elif not is_liquid:
        liquidity = "public_illiquid"
    else:
        liquidity = "public_liquid"

    # Calculate WACC
    wacc_result = calculate_wacc_from_market_data(
        equity_beta=equity_beta,
        debt_to_equity=debt_to_equity,
        tax_rate=tax_rate,
        currency=curr,
        country=country,
        region=reg,
        company_size=size,
        market_cap=market_cap_millions,
        liquidity_status=liquidity,
        credit_rating=rating,
        company_specific_premium=company_specific_premium,
    )

    # Build result
    result = {
        "model": "CMM-1.0",
        "model_name": "Capital Market Model (Kapitalmarkt-Modul)",
        "version": "1.0.0",
        "data_date": "Q1 2026",
        "inputs": {
            "equity_beta": equity_beta,
            "debt_to_equity": debt_to_equity,
            "tax_rate_percent": tax_rate * 100,
            "currency": currency,
            "country": country,
            "region": region,
            "company_size": company_size,
            "credit_rating": credit_rating,
            "is_public": is_public,
            "is_liquid": is_liquid,
        },
        "wacc_analysis": wacc_result,
    }

    # Add benchmarks
    if show_benchmarks:
        result["market_benchmarks"] = {
            "risk_free_rates": {
                "EUR_10Y_Bund": f"{RISK_FREE_RATES[Currency.EUR]*100:.1f}%",
                "USD_10Y_Treasury": f"{RISK_FREE_RATES[Currency.USD]*100:.1f}%",
                "CHF_10Y_Confed": f"{RISK_FREE_RATES[Currency.CHF]*100:.1f}%",
            },
            "market_risk_premium": {
                "historical_geometric": f"{MARKET_RISK_PREMIUM['historical_geometric']*100:.1f}%",
                "implied_current": f"{MARKET_RISK_PREMIUM['implied_current']*100:.1f}%",
                "recommended": f"{MARKET_RISK_PREMIUM['recommended']*100:.1f}%",
            },
            "country_risk_examples": {
                "germany": "0.0%",
                "poland": "1.5%",
                "brazil": "3.5%",
                "china": "1.5%",
                "india": "2.0%",
            },
            "size_premiums": {
                "large_cap": "0.5%",
                "mid_cap": "1.5%",
                "small_cap": "3.0%",
                "private": "5.0%",
            },
            "credit_spreads": {
                "AAA": "0.5%",
                "A": "1.2%",
                "BBB": "1.8%",
                "BB": "3.5%",
            },
        }

    return result


if __name__ == "__main__":
    print("=" * 70)
    print("CMM-1.0: Capital Market Model - Demo")
    print("=" * 70)

    # Example: German mid-cap company
    result = analyze_capital_markets(
        equity_beta=1.2,
        debt_to_equity=0.5,
        tax_rate=0.25,
        currency="EUR",
        country="germany",
        company_size="mid_cap",
        is_public=True,
        is_liquid=True,
        credit_rating="BBB",
    )

    print(f"\nModel: {result['model']} ({result['model_name']})")

    wacc = result['wacc_analysis']
    print(f"\n--- WACC RESULT ---")
    print(f"  WACC: {wacc['wacc_percent']}%")

    print(f"\n--- COST OF EQUITY ---")
    coe = wacc['cost_of_equity']
    print(f"  Cost of Equity: {coe['cost_of_equity_percent']}%")
    for comp, val in coe['components'].items():
        if val > 0:
            print(f"    {comp}: {val}%")

    print(f"\n--- COST OF DEBT ---")
    cod = wacc['cost_of_debt']
    print(f"  Cost of Debt (pre-tax): {cod['cost_of_debt_percent']}%")
    print(f"  Credit Rating: {cod['credit_rating']}")

    print(f"\n--- CAPITAL STRUCTURE ---")
    cs = wacc['capital_structure']
    print(f"  D/E Ratio: {cs['debt_to_equity']}")
    print(f"  Equity Weight: {cs['equity_weight_percent']}%")
    print(f"  Debt Weight: {cs['debt_weight_percent']}%")

    print(f"\n--- WACC CALCULATION ---")
    print(f"  {wacc['wacc_calculation']}")
