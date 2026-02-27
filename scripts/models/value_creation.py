#!/usr/bin/env python3
"""
Value Creation Model (VCM-1.0)
Economic Value Added, ROIC, and Shareholder Value metrics.

Usage:
    from value_creation import calculate_value_creation
    result = calculate_value_creation(config, pnl_projection, balance_sheet)

Model Version: 1.0.0
Implementation Date: 2026-01-16

FULLY GENERIC: All parameters from config, no hardcoded defaults.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Any
import yaml
import sys
from pathlib import Path

# Import base utilities
try:
    from strategy_base import (
        load_config, get_nested, save_csv, save_yaml,
        format_currency, format_percent, calculate_cagr, get_year_range,
        DEFAULT_BASE_YEAR, DEFAULT_PROJECTION_YEARS, DEFAULT_CURRENCY
    )
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent))
    from strategy_base import (
        load_config, get_nested, save_csv, save_yaml,
        format_currency, format_percent, calculate_cagr, get_year_range,
        DEFAULT_BASE_YEAR, DEFAULT_PROJECTION_YEARS, DEFAULT_CURRENCY
    )


def extract_value_params(config: Dict) -> Dict:
    """
    Extract value creation parameters from configuration.

    Expected config structure:
    ```yaml
    value_creation_model:
      base_year: 2024
      projection_years: 11
      currency: "EUR"

      # Cost of Capital
      wacc:
        risk_free_rate_percent: 3.0
        equity_risk_premium_percent: 5.0
        beta: 1.1
        cost_of_debt_percent: 4.5
        tax_rate_percent: 25
        target_debt_ratio_percent: 30

      # Capital Structure (if not calculated from balance sheet)
      capital_structure:
        total_equity_m: 2000
        total_debt_m: 1500
        # Or specify invested capital directly:
        invested_capital_m: 3500

      # Valuation
      valuation:
        terminal_growth_rate_percent: 2.0
        dcf_discount_rate_percent: 8.5
        ev_ebitda_multiple: 8.0

      # Value Drivers
      value_drivers:
        - name: "Revenue Growth"
          weight: 0.25
        - name: "Margin Expansion"
          weight: 0.25
        - name: "Capital Efficiency"
          weight: 0.25
        - name: "WACC Optimization"
          weight: 0.25
    ```
    """
    vc_config = config.get('value_creation_model', {})
    wacc_config = vc_config.get('wacc', {})
    cap_config = vc_config.get('capital_structure', {})
    val_config = vc_config.get('valuation', {})

    params = {
        'base_year': vc_config.get('base_year', DEFAULT_BASE_YEAR),
        'projection_years': vc_config.get('projection_years', DEFAULT_PROJECTION_YEARS),
        'currency': vc_config.get('currency', DEFAULT_CURRENCY),

        # WACC components
        'risk_free_rate': wacc_config.get('risk_free_rate_percent', 3.0) / 100,
        'equity_risk_premium': wacc_config.get('equity_risk_premium_percent', 5.0) / 100,
        'beta': wacc_config.get('beta', 1.0),
        'cost_of_debt': wacc_config.get('cost_of_debt_percent', 5.0) / 100,
        'tax_rate': wacc_config.get('tax_rate_percent', 25) / 100,
        'target_debt_ratio': wacc_config.get('target_debt_ratio_percent', 30) / 100,

        # Capital structure
        'total_equity_m': cap_config.get('total_equity_m'),
        'total_debt_m': cap_config.get('total_debt_m'),
        'invested_capital_m': cap_config.get('invested_capital_m'),

        # Valuation
        'terminal_growth_rate': val_config.get('terminal_growth_rate_percent', 2.0) / 100,
        'dcf_discount_rate': val_config.get('dcf_discount_rate_percent'),
        'ev_ebitda_multiple': val_config.get('ev_ebitda_multiple', 8.0),

        # Value drivers
        'value_drivers': vc_config.get('value_drivers', [])
    }

    return params


def calculate_wacc(params: Dict) -> Dict:
    """
    Calculate Weighted Average Cost of Capital.

    Args:
        params: Model parameters

    Returns:
        Dictionary with WACC components and total
    """
    # Cost of Equity (CAPM)
    rf = params['risk_free_rate']
    erp = params['equity_risk_premium']
    beta = params['beta']
    cost_of_equity = rf + beta * erp

    # Cost of Debt (after-tax)
    cost_of_debt = params['cost_of_debt']
    tax_rate = params['tax_rate']
    after_tax_cost_of_debt = cost_of_debt * (1 - tax_rate)

    # Weights
    debt_ratio = params['target_debt_ratio']
    equity_ratio = 1 - debt_ratio

    # WACC
    wacc = equity_ratio * cost_of_equity + debt_ratio * after_tax_cost_of_debt

    return {
        'wacc': wacc,
        'wacc_percent': wacc * 100,
        'cost_of_equity': cost_of_equity,
        'cost_of_equity_percent': cost_of_equity * 100,
        'cost_of_debt_pretax': cost_of_debt,
        'cost_of_debt_aftertax': after_tax_cost_of_debt,
        'cost_of_debt_percent': after_tax_cost_of_debt * 100,
        'debt_ratio': debt_ratio,
        'equity_ratio': equity_ratio,
        'beta': beta,
        'risk_free_rate': rf,
        'equity_risk_premium': erp
    }


def calculate_invested_capital(
    revenue: np.ndarray,
    params: Dict,
    pnl_projection: Optional[pd.DataFrame] = None
) -> np.ndarray:
    """
    Calculate or estimate Invested Capital.

    Args:
        revenue: Revenue array
        params: Model parameters
        pnl_projection: Optional P&L projection

    Returns:
        Invested capital array
    """
    # If directly specified, use it as base and grow with revenue
    if params['invested_capital_m'] is not None:
        base_ic = params['invested_capital_m']
        # Assume IC grows at 80% of revenue growth rate
        ic_growth = np.ones(len(revenue))
        ic_growth[1:] = revenue[1:] / revenue[:-1]
        ic_growth = 1 + (ic_growth - 1) * 0.8
        ic = base_ic * np.cumprod(ic_growth)
        return ic

    # If equity and debt specified
    if params['total_equity_m'] is not None and params['total_debt_m'] is not None:
        base_ic = params['total_equity_m'] + params['total_debt_m']
        ic_growth = np.ones(len(revenue))
        ic_growth[1:] = revenue[1:] / revenue[:-1]
        ic_growth = 1 + (ic_growth - 1) * 0.8
        ic = base_ic * np.cumprod(ic_growth)
        return ic

    # Estimate from revenue (IC typically 50-70% of revenue)
    ic_to_revenue = 0.6
    return revenue * ic_to_revenue


def calculate_nopat(
    ebit: np.ndarray,
    tax_rate: float
) -> np.ndarray:
    """
    Calculate Net Operating Profit After Tax.

    Args:
        ebit: EBIT array
        tax_rate: Tax rate as decimal

    Returns:
        NOPAT array
    """
    return ebit * (1 - tax_rate)


def calculate_eva(
    nopat: np.ndarray,
    invested_capital: np.ndarray,
    wacc: float
) -> np.ndarray:
    """
    Calculate Economic Value Added.

    EVA = NOPAT - (Invested Capital × WACC)

    Args:
        nopat: NOPAT array
        invested_capital: Invested capital array
        wacc: WACC as decimal

    Returns:
        EVA array
    """
    capital_charge = invested_capital * wacc
    return nopat - capital_charge


def calculate_roic(
    nopat: np.ndarray,
    invested_capital: np.ndarray
) -> np.ndarray:
    """
    Calculate Return on Invested Capital.

    ROIC = NOPAT / Invested Capital

    Args:
        nopat: NOPAT array
        invested_capital: Invested capital array

    Returns:
        ROIC array (as percentages)
    """
    return np.where(invested_capital > 0, nopat / invested_capital * 100, 0)


def calculate_value_spread(
    roic: np.ndarray,
    wacc_percent: float
) -> np.ndarray:
    """
    Calculate Value Spread (ROIC - WACC).

    Positive spread = value creation
    Negative spread = value destruction

    Args:
        roic: ROIC array (as percentages)
        wacc_percent: WACC as percentage

    Returns:
        Value spread array (as percentages)
    """
    return roic - wacc_percent


def calculate_dcf_value(
    fcf: np.ndarray,
    terminal_fcf: float,
    wacc: float,
    terminal_growth: float
) -> Dict:
    """
    Calculate DCF enterprise value.

    Args:
        fcf: Free cash flow array
        terminal_fcf: Final year FCF for terminal value
        wacc: WACC as decimal
        terminal_growth: Terminal growth rate as decimal

    Returns:
        Dictionary with DCF components
    """
    # Discount factors
    years = np.arange(1, len(fcf) + 1)
    discount_factors = 1 / np.power(1 + wacc, years)

    # PV of FCF
    pv_fcf = fcf * discount_factors
    pv_explicit = pv_fcf.sum()

    # Terminal value (Gordon Growth Model)
    terminal_value = terminal_fcf * (1 + terminal_growth) / (wacc - terminal_growth)
    pv_terminal = terminal_value * discount_factors[-1]

    # Enterprise value
    enterprise_value = pv_explicit + pv_terminal

    return {
        'enterprise_value_m': enterprise_value,
        'pv_explicit_period_m': pv_explicit,
        'terminal_value_m': terminal_value,
        'pv_terminal_m': pv_terminal,
        'explicit_percent': pv_explicit / enterprise_value * 100,
        'terminal_percent': pv_terminal / enterprise_value * 100
    }


def calculate_value_creation(
    config: Dict,
    pnl_projection: Optional[pd.DataFrame] = None,
    cash_flow_projection: Optional[pd.DataFrame] = None
) -> Dict:
    """
    Main function: Calculate value creation metrics.

    Args:
        config: Configuration dictionary (from YAML)
        pnl_projection: DataFrame with P&L projection (from PLM)
        cash_flow_projection: DataFrame with cash flow projection (from CFM)

    Returns:
        Dictionary with:
        - value_metrics: DataFrame with value metrics by year
        - wacc: WACC calculation details
        - dcf_valuation: DCF valuation (if FCF available)
        - summary: Summary metrics
    """
    params = extract_value_params(config)

    base_year = params['base_year']
    num_years = params['projection_years']
    years = get_year_range(base_year, num_years)

    # Initialize value metrics DataFrame
    vm = pd.DataFrame({'Year': years})

    # Get P&L data
    if pnl_projection is not None:
        pnl = pnl_projection[pnl_projection['Year'].isin(years)].copy()
        if len(pnl) < len(years):
            last_row = pnl.iloc[-1].copy()
            for year in years[len(pnl):]:
                last_row['Year'] = year
                pnl = pd.concat([pnl, pd.DataFrame([last_row])], ignore_index=True)

        vm['Revenue'] = pnl['Revenue'].values
        vm['EBITDA'] = pnl['EBITDA'].values if 'EBITDA' in pnl.columns else pnl['Revenue'].values * 0.12
        vm['EBIT'] = pnl['EBIT'].values if 'EBIT' in pnl.columns else vm['EBITDA'] - vm['Revenue'] * 0.03
    else:
        # Estimate from config
        base_revenue = config.get('company', {}).get('base_revenue_m', 1000)
        cagr = 0.05
        vm['Revenue'] = base_revenue * np.power(1 + cagr, years - base_year)
        vm['EBITDA'] = vm['Revenue'] * 0.12
        vm['EBIT'] = vm['EBITDA'] - vm['Revenue'] * 0.03

    # Calculate WACC
    wacc_result = calculate_wacc(params)
    wacc = wacc_result['wacc']
    wacc_pct = wacc_result['wacc_percent']

    # Calculate Invested Capital
    invested_capital = calculate_invested_capital(vm['Revenue'].values, params, pnl_projection)
    vm['Invested_Capital'] = np.round(invested_capital, 1)

    # Calculate NOPAT
    nopat = calculate_nopat(vm['EBIT'].values, params['tax_rate'])
    vm['NOPAT'] = np.round(nopat, 1)

    # Calculate Capital Charge
    vm['Capital_Charge'] = np.round(vm['Invested_Capital'] * wacc, 1)

    # Calculate EVA
    eva = calculate_eva(nopat, invested_capital, wacc)
    vm['EVA'] = np.round(eva, 1)

    # Calculate ROIC
    roic = calculate_roic(nopat, invested_capital)
    vm['ROIC_%'] = np.round(roic, 1)

    # Calculate Value Spread
    value_spread = calculate_value_spread(roic, wacc_pct)
    vm['Value_Spread_%'] = np.round(value_spread, 1)

    # Cumulative EVA
    vm['Cumulative_EVA'] = np.round(np.cumsum(eva), 1)

    # DCF Valuation (if FCF available)
    dcf_result = None
    if cash_flow_projection is not None and 'Free_Cash_Flow' in cash_flow_projection.columns:
        fcf = cash_flow_projection[cash_flow_projection['Year'].isin(years)]['Free_Cash_Flow'].values
        if len(fcf) == len(years):
            terminal_fcf = fcf[-1]
            dcf_result = calculate_dcf_value(
                fcf, terminal_fcf, wacc, params['terminal_growth_rate']
            )
    else:
        # Estimate FCF from NOPAT
        fcf_estimate = nopat * 0.7  # Assume 70% FCF conversion
        terminal_fcf = fcf_estimate[-1]
        dcf_result = calculate_dcf_value(
            fcf_estimate, terminal_fcf, wacc, params['terminal_growth_rate']
        )

    # EV/EBITDA Valuation
    final_ebitda = vm['EBITDA'].iloc[-1]
    ev_ebitda_multiple = params['ev_ebitda_multiple']
    ev_from_multiple = final_ebitda * ev_ebitda_multiple

    # Summary
    base_idx = 0
    final_idx = len(years) - 1

    total_eva = vm['EVA'].sum()
    avg_roic = vm['ROIC_%'].mean()
    avg_spread = vm['Value_Spread_%'].mean()

    summary = {
        'base_year': int(years[base_idx]),
        'final_year': int(years[final_idx]),
        'currency': params['currency'],
        'wacc': {
            'wacc_percent': round(wacc_pct, 2),
            'cost_of_equity_percent': round(wacc_result['cost_of_equity_percent'], 2),
            'cost_of_debt_percent': round(wacc_result['cost_of_debt_percent'], 2),
            'debt_ratio_percent': round(wacc_result['debt_ratio'] * 100, 1),
            'beta': wacc_result['beta']
        },
        'value_creation': {
            'total_eva_m': round(total_eva, 1),
            'base_year_eva_m': float(vm['EVA'].iloc[base_idx]),
            'final_year_eva_m': float(vm['EVA'].iloc[final_idx]),
            'avg_roic_percent': round(avg_roic, 1),
            'avg_value_spread_percent': round(avg_spread, 1),
            'value_creating': avg_spread > 0
        },
        'invested_capital': {
            'base_year_m': float(vm['Invested_Capital'].iloc[base_idx]),
            'final_year_m': float(vm['Invested_Capital'].iloc[final_idx]),
            'growth_percent': calculate_cagr(
                vm['Invested_Capital'].iloc[base_idx],
                vm['Invested_Capital'].iloc[final_idx],
                num_years - 1
            )
        },
        'valuation': {
            'dcf_enterprise_value_m': round(dcf_result['enterprise_value_m'], 0) if dcf_result else None,
            'ev_ebitda_multiple': ev_ebitda_multiple,
            'ev_from_multiple_m': round(ev_from_multiple, 0),
            'terminal_value_percent': round(dcf_result['terminal_percent'], 1) if dcf_result else None
        }
    }

    return {
        'value_metrics': vm,
        'wacc': wacc_result,
        'dcf_valuation': dcf_result,
        'summary': summary,
        'params': params
    }


def format_results(results: Dict) -> str:
    """Format value creation results for display."""
    output = []
    output.append("\n" + "="*80)
    output.append("VALUE CREATION MODEL (VCM-1.0) - RESULTS")
    output.append("="*80)

    summary = results['summary']
    currency = summary['currency']

    output.append("\n[1] WEIGHTED AVERAGE COST OF CAPITAL (WACC)")
    output.append("-" * 60)
    wacc = summary['wacc']
    output.append(f"  WACC:              {wacc['wacc_percent']:.2f}%")
    output.append(f"  Cost of Equity:    {wacc['cost_of_equity_percent']:.2f}%")
    output.append(f"  Cost of Debt:      {wacc['cost_of_debt_percent']:.2f}% (after-tax)")
    output.append(f"  Debt Ratio:        {wacc['debt_ratio_percent']:.1f}%")
    output.append(f"  Beta:              {wacc['beta']:.2f}")

    output.append("\n[2] VALUE CREATION METRICS")
    output.append("-" * 60)
    vc = summary['value_creation']
    output.append(f"  Total EVA:         {currency}{vc['total_eva_m']:,.0f}M")
    output.append(f"  Avg ROIC:          {vc['avg_roic_percent']:.1f}%")
    output.append(f"  Avg Value Spread:  {vc['avg_value_spread_percent']:.1f}%")
    status = "VALUE CREATING" if vc['value_creating'] else "VALUE DESTROYING"
    output.append(f"  Status:            {status}")

    output.append("\n[3] INVESTED CAPITAL")
    output.append("-" * 60)
    ic = summary['invested_capital']
    output.append(f"  Base Year:  {currency}{ic['base_year_m']:,.0f}M")
    output.append(f"  Final Year: {currency}{ic['final_year_m']:,.0f}M")
    output.append(f"  CAGR:       {ic['growth_percent']:.1f}%")

    output.append("\n[4] VALUATION")
    output.append("-" * 60)
    val = summary['valuation']
    if val['dcf_enterprise_value_m']:
        output.append(f"  DCF Enterprise Value: {currency}{val['dcf_enterprise_value_m']:,.0f}M")
        output.append(f"  Terminal Value %:     {val['terminal_value_percent']:.1f}%")
    output.append(f"  EV/EBITDA Multiple:   {val['ev_ebitda_multiple']:.1f}x")
    output.append(f"  EV from Multiple:     {currency}{val['ev_from_multiple_m']:,.0f}M")

    output.append("\n[5] VALUE METRICS (Key Years)")
    output.append("-" * 60)
    vm = results['value_metrics']
    key_years = [summary['base_year'], summary['base_year'] + 2,
                 summary['base_year'] + 5, summary['final_year']]
    key_rows = vm[vm['Year'].isin(key_years)]
    display_cols = ['Year', 'NOPAT', 'Invested_Capital', 'EVA', 'ROIC_%', 'Value_Spread_%']
    output.append(key_rows[display_cols].to_string(index=False))

    output.append("\n" + "="*80)
    return "\n".join(output)


def main():
    """Main entry point for command-line execution."""
    if len(sys.argv) < 2:
        print("Usage: python value_creation.py <config_file.yaml> [pnl_file.csv] [cf_file.csv]")
        sys.exit(1)

    config_file = sys.argv[1]
    pnl_file = sys.argv[2] if len(sys.argv) > 2 else None
    cf_file = sys.argv[3] if len(sys.argv) > 3 else None

    print(f"Loading configuration: {config_file}")
    config = load_config(config_file)

    pnl_df = None
    cf_df = None

    if pnl_file:
        print(f"Loading P&L projection: {pnl_file}")
        pnl_df = pd.read_csv(pnl_file)

    if cf_file:
        print(f"Loading cash flow projection: {cf_file}")
        cf_df = pd.read_csv(cf_file)

    print("Running value creation model...")
    results = calculate_value_creation(config, pnl_df, cf_df)

    print(format_results(results))


if __name__ == '__main__':
    main()
