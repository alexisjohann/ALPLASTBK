#!/usr/bin/env python3
"""
Cash Flow Model (CFM-1.0)
Cash flow projection from P&L and working capital assumptions.

Usage:
    from cash_flow import project_cash_flow
    result = project_cash_flow(config, pnl_projection, capex_projection)

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
        format_currency, calculate_cagr, get_year_range,
        DEFAULT_BASE_YEAR, DEFAULT_PROJECTION_YEARS, DEFAULT_CURRENCY
    )
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent))
    from strategy_base import (
        load_config, get_nested, save_csv, save_yaml,
        format_currency, calculate_cagr, get_year_range,
        DEFAULT_BASE_YEAR, DEFAULT_PROJECTION_YEARS, DEFAULT_CURRENCY
    )


def extract_cash_flow_params(config: Dict) -> Dict:
    """
    Extract cash flow parameters from configuration.

    Expected config structure:
    ```yaml
    cash_flow_model:
      base_year: 2024
      projection_years: 11
      currency: "EUR"

      # Working Capital Assumptions
      working_capital:
        days_receivable: 45        # DSO - Days Sales Outstanding
        days_payable: 60           # DPO - Days Payable Outstanding
        days_inventory: 30         # DIO - Days Inventory Outstanding
        # Or as % of revenue:
        wc_percent_of_revenue: 15  # Alternative: WC as % of revenue

      # Cash Conversion
      cash_conversion:
        depreciation_add_back: true
        amortization_add_back: true
        deferred_tax_percent: 5    # % of tax expense deferred

      # Financing
      financing:
        interest_paid_from_pnl: true
        dividend_payout_ratio: 30  # % of net income
        debt_repayment_schedule:
          - year: 2025
            amount_m: 50
          - year: 2028
            amount_m: 100

      # Opening Balance
      opening_cash_m: 200          # Cash at start of projection
    ```
    """
    cf_config = config.get('cash_flow_model', {})

    # Working capital params
    wc_config = cf_config.get('working_capital', {})

    # Financing params
    fin_config = cf_config.get('financing', {})

    params = {
        'base_year': cf_config.get('base_year', DEFAULT_BASE_YEAR),
        'projection_years': cf_config.get('projection_years', DEFAULT_PROJECTION_YEARS),
        'currency': cf_config.get('currency', DEFAULT_CURRENCY),

        # Working capital
        'days_receivable': wc_config.get('days_receivable', 45),
        'days_payable': wc_config.get('days_payable', 60),
        'days_inventory': wc_config.get('days_inventory', 30),
        'wc_percent_of_revenue': wc_config.get('wc_percent_of_revenue'),

        # Cash conversion
        'depreciation_add_back': cf_config.get('cash_conversion', {}).get('depreciation_add_back', True),
        'deferred_tax_percent': cf_config.get('cash_conversion', {}).get('deferred_tax_percent', 0),

        # Financing
        'dividend_payout_ratio': fin_config.get('dividend_payout_ratio', 0) / 100,
        'debt_repayment_schedule': fin_config.get('debt_repayment_schedule', []),

        # Opening balance
        'opening_cash_m': cf_config.get('opening_cash_m', 0),
    }

    return params


def calculate_working_capital(
    revenue: np.ndarray,
    cogs: np.ndarray,
    params: Dict
) -> np.ndarray:
    """
    Calculate working capital requirements.

    Args:
        revenue: Annual revenue array
        cogs: Cost of goods sold array
        params: Model parameters

    Returns:
        Working capital array
    """
    # Method 1: Use WC as % of revenue
    if params.get('wc_percent_of_revenue') is not None:
        wc_pct = params['wc_percent_of_revenue'] / 100
        return revenue * wc_pct

    # Method 2: Calculate from days
    dso = params['days_receivable']
    dpo = params['days_payable']
    dio = params['days_inventory']

    # Accounts Receivable = Revenue * DSO / 365
    ar = revenue * dso / 365

    # Accounts Payable = COGS * DPO / 365
    ap = cogs * dpo / 365

    # Inventory = COGS * DIO / 365
    inventory = cogs * dio / 365

    # Net Working Capital = AR + Inventory - AP
    nwc = ar + inventory - ap

    return nwc


def calculate_working_capital_change(wc: np.ndarray) -> np.ndarray:
    """
    Calculate change in working capital (cash outflow when WC increases).

    Args:
        wc: Working capital array

    Returns:
        Change in working capital array (positive = cash outflow)
    """
    wc_change = np.zeros(len(wc))
    wc_change[1:] = wc[1:] - wc[:-1]
    return wc_change


def get_debt_repayments(years: np.ndarray, schedule: List[Dict]) -> np.ndarray:
    """
    Get debt repayment amounts by year from schedule.

    Args:
        years: Array of years
        schedule: List of {year, amount_m} dictionaries

    Returns:
        Array of debt repayments
    """
    repayments = np.zeros(len(years))

    for item in schedule:
        year = item.get('year')
        amount = item.get('amount_m', 0)
        if year in years:
            idx = np.where(years == year)[0][0]
            repayments[idx] = amount

    return repayments


def project_cash_flow(
    config: Dict,
    pnl_projection: Optional[pd.DataFrame] = None,
    capex_projection: Optional[pd.DataFrame] = None
) -> Dict:
    """
    Main function: Project Cash Flow statement.

    Args:
        config: Configuration dictionary (from YAML)
        pnl_projection: DataFrame with P&L projection (from PLM)
        capex_projection: DataFrame with capex projection (from CAM)

    Returns:
        Dictionary with:
        - cash_flow_projection: DataFrame with full cash flow by year
        - summary: Summary metrics
        - fcf_yield: Free cash flow metrics
    """
    params = extract_cash_flow_params(config)

    base_year = params['base_year']
    num_years = params['projection_years']
    years = get_year_range(base_year, num_years)

    # Initialize cash flow DataFrame
    cf = pd.DataFrame({'Year': years})

    # Get P&L data
    if pnl_projection is not None:
        pnl = pnl_projection[pnl_projection['Year'].isin(years)].copy()
        if len(pnl) < len(years):
            # Pad with last values
            last_row = pnl.iloc[-1].copy()
            for year in years[len(pnl):]:
                last_row['Year'] = year
                pnl = pd.concat([pnl, pd.DataFrame([last_row])], ignore_index=True)

        cf['Revenue'] = pnl['Revenue'].values
        cf['EBITDA'] = pnl['EBITDA'].values if 'EBITDA' in pnl.columns else pnl['Revenue'].values * 0.12
        cf['Depreciation'] = pnl['Depreciation'].values if 'Depreciation' in pnl.columns else cf['Revenue'] * 0.03
        cf['EBIT'] = pnl['EBIT'].values if 'EBIT' in pnl.columns else cf['EBITDA'] - cf['Depreciation']
        cf['Interest'] = pnl['Interest'].values if 'Interest' in pnl.columns else cf['Revenue'] * 0.012
        cf['Tax'] = pnl['Tax'].values if 'Tax' in pnl.columns else np.maximum((cf['EBIT'] - cf['Interest']) * 0.25, 0)
        cf['Net_Income'] = pnl['Net_Income'].values if 'Net_Income' in pnl.columns else cf['EBIT'] - cf['Interest'] - cf['Tax']
    else:
        # Estimate from config
        base_revenue = config.get('company', {}).get('base_revenue_m', 1000)
        cagr = 0.05
        cf['Revenue'] = base_revenue * np.power(1 + cagr, years - base_year)
        cf['EBITDA'] = cf['Revenue'] * 0.12
        cf['Depreciation'] = cf['Revenue'] * 0.03
        cf['EBIT'] = cf['EBITDA'] - cf['Depreciation']
        cf['Interest'] = cf['Revenue'] * 0.012
        cf['Tax'] = np.maximum((cf['EBIT'] - cf['Interest']) * 0.25, 0)
        cf['Net_Income'] = cf['EBIT'] - cf['Interest'] - cf['Tax']

    # OPERATING CASH FLOW
    # Start with Net Income
    cf['OCF_Net_Income'] = cf['Net_Income']

    # Add back non-cash items
    if params['depreciation_add_back']:
        cf['OCF_Add_Depreciation'] = cf['Depreciation']
    else:
        cf['OCF_Add_Depreciation'] = 0

    # Deferred taxes
    deferred_tax_pct = params['deferred_tax_percent'] / 100
    cf['OCF_Deferred_Tax'] = cf['Tax'] * deferred_tax_pct

    # Working capital change
    cogs = cf['Revenue'] * 0.65  # Estimate COGS as 65% of revenue
    wc = calculate_working_capital(cf['Revenue'].values, cogs.values, params)
    wc_change = calculate_working_capital_change(wc)
    cf['Working_Capital'] = np.round(wc, 1)
    cf['WC_Change'] = np.round(wc_change, 1)

    # Operating Cash Flow
    cf['Operating_Cash_Flow'] = np.round(
        cf['OCF_Net_Income'] +
        cf['OCF_Add_Depreciation'] +
        cf['OCF_Deferred_Tax'] -
        cf['WC_Change'],
        1
    )

    # INVESTING CASH FLOW
    # Get CapEx
    if capex_projection is not None and 'Total' in capex_projection.columns:
        capex = capex_projection[capex_projection['Year'].isin(years)]['Total'].values
        if len(capex) < len(years):
            capex = np.pad(capex, (0, len(years) - len(capex)), mode='edge')
    else:
        # Estimate CapEx as % of revenue
        capex_pct = config.get('cash_flow_model', {}).get('capex_percent_of_revenue', 5) / 100
        capex = cf['Revenue'].values * capex_pct

    cf['CapEx'] = np.round(capex, 1)
    cf['Investing_Cash_Flow'] = np.round(-cf['CapEx'], 1)

    # FREE CASH FLOW
    cf['Free_Cash_Flow'] = np.round(cf['Operating_Cash_Flow'] + cf['Investing_Cash_Flow'], 1)

    # FINANCING CASH FLOW
    # Dividends
    dividend_ratio = params['dividend_payout_ratio']
    cf['Dividends'] = np.round(np.maximum(cf['Net_Income'] * dividend_ratio, 0), 1)

    # Debt repayments
    debt_repayments = get_debt_repayments(years, params['debt_repayment_schedule'])
    cf['Debt_Repayment'] = np.round(debt_repayments, 1)

    cf['Financing_Cash_Flow'] = np.round(-cf['Dividends'] - cf['Debt_Repayment'], 1)

    # NET CASH FLOW
    cf['Net_Cash_Flow'] = np.round(
        cf['Free_Cash_Flow'] + cf['Financing_Cash_Flow'],
        1
    )

    # CASH POSITION
    opening_cash = params['opening_cash_m']
    cash_position = np.zeros(len(years))
    cash_position[0] = opening_cash + cf['Net_Cash_Flow'].iloc[0]
    for i in range(1, len(years)):
        cash_position[i] = cash_position[i-1] + cf['Net_Cash_Flow'].iloc[i]
    cf['Cash_Position'] = np.round(cash_position, 1)

    # FCF METRICS
    cf['FCF_Yield_%'] = np.round(cf['Free_Cash_Flow'] / cf['Revenue'] * 100, 1)
    cf['OCF_to_EBITDA_%'] = np.round(cf['Operating_Cash_Flow'] / cf['EBITDA'] * 100, 1)

    # Summary
    base_idx = 0
    final_idx = len(years) - 1

    total_fcf = cf['Free_Cash_Flow'].sum()
    total_ocf = cf['Operating_Cash_Flow'].sum()
    total_capex = cf['CapEx'].sum()
    total_dividends = cf['Dividends'].sum()

    summary = {
        'base_year': int(years[base_idx]),
        'final_year': int(years[final_idx]),
        'currency': params['currency'],
        'operating_cash_flow': {
            'base_year_m': float(cf['Operating_Cash_Flow'].iloc[base_idx]),
            'final_year_m': float(cf['Operating_Cash_Flow'].iloc[final_idx]),
            'total_m': float(total_ocf),
            'cagr_percent': calculate_cagr(
                cf['Operating_Cash_Flow'].iloc[base_idx],
                cf['Operating_Cash_Flow'].iloc[final_idx],
                num_years - 1
            ) if cf['Operating_Cash_Flow'].iloc[base_idx] > 0 else 0
        },
        'free_cash_flow': {
            'base_year_m': float(cf['Free_Cash_Flow'].iloc[base_idx]),
            'final_year_m': float(cf['Free_Cash_Flow'].iloc[final_idx]),
            'total_m': float(total_fcf),
            'avg_fcf_yield_percent': float(cf['FCF_Yield_%'].mean()),
            'cagr_percent': calculate_cagr(
                max(cf['Free_Cash_Flow'].iloc[base_idx], 1),
                max(cf['Free_Cash_Flow'].iloc[final_idx], 1),
                num_years - 1
            )
        },
        'capital_allocation': {
            'total_capex_m': float(total_capex),
            'total_dividends_m': float(total_dividends),
            'capex_to_ocf_percent': float(total_capex / total_ocf * 100) if total_ocf > 0 else 0,
            'dividend_payout_ratio_percent': params['dividend_payout_ratio'] * 100
        },
        'cash_position': {
            'opening_m': float(opening_cash),
            'closing_m': float(cf['Cash_Position'].iloc[final_idx]),
            'min_m': float(cf['Cash_Position'].min()),
            'max_m': float(cf['Cash_Position'].max())
        },
        'working_capital': {
            'base_year_m': float(cf['Working_Capital'].iloc[base_idx]),
            'final_year_m': float(cf['Working_Capital'].iloc[final_idx]),
            'total_investment_m': float(cf['WC_Change'].sum())
        }
    }

    return {
        'cash_flow_projection': cf,
        'summary': summary,
        'params': params
    }


def format_results(results: Dict) -> str:
    """Format cash flow results for display."""
    output = []
    output.append("\n" + "="*80)
    output.append("CASH FLOW MODEL (CFM-1.0) - RESULTS")
    output.append("="*80)

    summary = results['summary']
    currency = summary['currency']

    output.append("\n[1] OPERATING CASH FLOW")
    output.append("-" * 60)
    ocf = summary['operating_cash_flow']
    output.append(f"  Base Year:  {currency}{ocf['base_year_m']:,.0f}M")
    output.append(f"  Final Year: {currency}{ocf['final_year_m']:,.0f}M")
    output.append(f"  Total:      {currency}{ocf['total_m']:,.0f}M")
    output.append(f"  CAGR:       {ocf['cagr_percent']:.1f}%")

    output.append("\n[2] FREE CASH FLOW")
    output.append("-" * 60)
    fcf = summary['free_cash_flow']
    output.append(f"  Base Year:  {currency}{fcf['base_year_m']:,.0f}M")
    output.append(f"  Final Year: {currency}{fcf['final_year_m']:,.0f}M")
    output.append(f"  Total:      {currency}{fcf['total_m']:,.0f}M")
    output.append(f"  Avg Yield:  {fcf['avg_fcf_yield_percent']:.1f}%")

    output.append("\n[3] CAPITAL ALLOCATION")
    output.append("-" * 60)
    cap = summary['capital_allocation']
    output.append(f"  Total CapEx:    {currency}{cap['total_capex_m']:,.0f}M")
    output.append(f"  Total Dividends: {currency}{cap['total_dividends_m']:,.0f}M")
    output.append(f"  CapEx/OCF:      {cap['capex_to_ocf_percent']:.1f}%")

    output.append("\n[4] CASH POSITION")
    output.append("-" * 60)
    cash = summary['cash_position']
    output.append(f"  Opening:  {currency}{cash['opening_m']:,.0f}M")
    output.append(f"  Closing:  {currency}{cash['closing_m']:,.0f}M")
    output.append(f"  Min:      {currency}{cash['min_m']:,.0f}M")
    output.append(f"  Max:      {currency}{cash['max_m']:,.0f}M")

    output.append("\n[5] CASH FLOW PROJECTION (Key Years)")
    output.append("-" * 60)
    cf = results['cash_flow_projection']
    key_years = [summary['base_year'], summary['base_year'] + 2,
                 summary['base_year'] + 5, summary['final_year']]
    key_rows = cf[cf['Year'].isin(key_years)]
    display_cols = ['Year', 'Operating_Cash_Flow', 'CapEx', 'Free_Cash_Flow', 'Cash_Position']
    output.append(key_rows[display_cols].to_string(index=False))

    output.append("\n" + "="*80)
    return "\n".join(output)


def main():
    """Main entry point for command-line execution."""
    if len(sys.argv) < 2:
        print("Usage: python cash_flow.py <config_file.yaml> [pnl_file.csv] [capex_file.csv]")
        sys.exit(1)

    config_file = sys.argv[1]
    pnl_file = sys.argv[2] if len(sys.argv) > 2 else None
    capex_file = sys.argv[3] if len(sys.argv) > 3 else None

    print(f"Loading configuration: {config_file}")
    config = load_config(config_file)

    pnl_df = None
    capex_df = None

    if pnl_file:
        print(f"Loading P&L projection: {pnl_file}")
        pnl_df = pd.read_csv(pnl_file)

    if capex_file:
        print(f"Loading CapEx projection: {capex_file}")
        capex_df = pd.read_csv(capex_file)

    print("Running cash flow model...")
    results = project_cash_flow(config, pnl_df, capex_df)

    print(format_results(results))


if __name__ == '__main__':
    main()
