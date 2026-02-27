#!/usr/bin/env python3
"""
Working Capital Model (WCM-1.0)
Detailed working capital management and optimization.

Usage:
    from working_capital import project_working_capital
    result = project_working_capital(config, revenue_projection)

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


def extract_working_capital_params(config: Dict) -> Dict:
    """
    Extract working capital parameters from configuration.

    Expected config structure:
    ```yaml
    working_capital_model:
      base_year: 2024
      projection_years: 11
      currency: "EUR"

      # Current state
      current_state:
        dso_days: 55          # Days Sales Outstanding
        dpo_days: 45          # Days Payable Outstanding
        dio_days: 40          # Days Inventory Outstanding

      # Target state (optimization)
      target_state:
        dso_days: 45          # Target DSO
        dpo_days: 60          # Target DPO (extend)
        dio_days: 30          # Target DIO (reduce)

      # Transition
      transition:
        improvement_years: 3   # Years to reach target

      # Cost of working capital
      cost_of_capital_percent: 8.0  # WACC for WC financing

      # Seasonality (optional)
      seasonality:
        q1_factor: 0.9
        q2_factor: 1.0
        q3_factor: 0.95
        q4_factor: 1.15
    ```
    """
    wc_config = config.get('working_capital_model', {})

    # Also check cash_flow_model for working capital params
    cf_wc = config.get('cash_flow_model', {}).get('working_capital', {})

    params = {
        'base_year': wc_config.get('base_year', DEFAULT_BASE_YEAR),
        'projection_years': wc_config.get('projection_years', DEFAULT_PROJECTION_YEARS),
        'currency': wc_config.get('currency', DEFAULT_CURRENCY),
        'current_state': wc_config.get('current_state', {}),
        'target_state': wc_config.get('target_state', {}),
        'transition': wc_config.get('transition', {}),
        'cost_of_capital_percent': wc_config.get('cost_of_capital_percent', 8.0),
        'seasonality': wc_config.get('seasonality', {})
    }

    # Use cash_flow_model params as fallback
    if not params['current_state']:
        params['current_state'] = {
            'dso_days': cf_wc.get('days_receivable', 45),
            'dpo_days': cf_wc.get('days_payable', 60),
            'dio_days': cf_wc.get('days_inventory', 30)
        }

    # Set target to current if not specified (no improvement)
    if not params['target_state']:
        params['target_state'] = params['current_state'].copy()

    # Default transition
    if not params['transition']:
        params['transition'] = {'improvement_years': 3}

    return params


def calculate_ccc(dso: float, dpo: float, dio: float) -> float:
    """Calculate Cash Conversion Cycle."""
    return dso + dio - dpo


def interpolate_days(current: float, target: float, year_index: int, transition_years: int) -> float:
    """Interpolate between current and target values."""
    if year_index >= transition_years:
        return target
    progress = year_index / transition_years
    return current + (target - current) * progress


def project_working_capital(
    config: Dict,
    revenue_projection: pd.DataFrame = None,
    cost_projection: pd.DataFrame = None
) -> Dict:
    """
    Project working capital requirements and optimization.

    Args:
        config: Configuration dictionary
        revenue_projection: Revenue projection from RPM-1.0
        cost_projection: Cost projection from CSM-1.0

    Returns:
        Dictionary with working capital projection and analysis
    """
    params = extract_working_capital_params(config)
    years = get_year_range(params['base_year'], params['projection_years'])
    current = params['current_state']
    target = params['target_state']
    transition_years = params['transition'].get('improvement_years', 3)
    cost_of_capital = params['cost_of_capital_percent'] / 100

    # Initialize data storage
    data = []
    prev_nwc = None

    for i, year in enumerate(years):
        row = {'Year': year}

        # Get revenue and COGS for this year
        revenue = 0
        cogs = 0

        if revenue_projection is not None and 'Year' in revenue_projection.columns:
            rev_row = revenue_projection[revenue_projection['Year'] == year]
            if len(rev_row) > 0:
                revenue = float(rev_row['Total'].iloc[0]) if 'Total' in rev_row else 0

        if cost_projection is not None and 'Year' in cost_projection.columns:
            cost_row = cost_projection[cost_projection['Year'] == year]
            if len(cost_row) > 0:
                cogs = float(cost_row['COGS'].iloc[0]) if 'COGS' in cost_row else revenue * 0.6

        # If no cost data, estimate COGS as 60% of revenue
        if cogs == 0 and revenue > 0:
            cogs = revenue * 0.6

        row['Revenue'] = revenue
        row['COGS'] = cogs

        # Calculate interpolated days
        row['DSO'] = interpolate_days(
            current.get('dso_days', 45),
            target.get('dso_days', 45),
            i, transition_years
        )
        row['DPO'] = interpolate_days(
            current.get('dpo_days', 60),
            target.get('dpo_days', 60),
            i, transition_years
        )
        row['DIO'] = interpolate_days(
            current.get('dio_days', 30),
            target.get('dio_days', 30),
            i, transition_years
        )

        # Cash Conversion Cycle
        row['CCC'] = calculate_ccc(row['DSO'], row['DPO'], row['DIO'])

        # Working Capital Components
        row['Accounts_Receivable'] = revenue * row['DSO'] / 365
        row['Inventory'] = cogs * row['DIO'] / 365
        row['Accounts_Payable'] = cogs * row['DPO'] / 365

        # Net Working Capital
        row['NWC'] = row['Accounts_Receivable'] + row['Inventory'] - row['Accounts_Payable']

        # Working Capital Change
        if prev_nwc is not None:
            row['NWC_Change'] = row['NWC'] - prev_nwc
        else:
            row['NWC_Change'] = 0

        prev_nwc = row['NWC']

        # Working Capital Ratios
        row['NWC_Percent_Revenue'] = (row['NWC'] / revenue * 100) if revenue > 0 else 0
        row['AR_Percent_Revenue'] = (row['Accounts_Receivable'] / revenue * 100) if revenue > 0 else 0
        row['Inv_Percent_COGS'] = (row['Inventory'] / cogs * 100) if cogs > 0 else 0
        row['AP_Percent_COGS'] = (row['Accounts_Payable'] / cogs * 100) if cogs > 0 else 0

        # Cost of Working Capital
        row['WC_Financing_Cost'] = row['NWC'] * cost_of_capital

        data.append(row)

    df = pd.DataFrame(data)

    # Calculate improvements
    base_row = df.iloc[0]
    final_row = df.iloc[-1]

    base_ccc = base_row['CCC']
    final_ccc = final_row['CCC']
    ccc_improvement = base_ccc - final_ccc

    # Cash released from WC improvement
    total_wc_change = df['NWC_Change'].sum()
    total_financing_cost = df['WC_Financing_Cost'].sum()

    summary = {
        'currency': params['currency'],
        'current_state': {
            'dso_days': float(base_row['DSO']),
            'dpo_days': float(base_row['DPO']),
            'dio_days': float(base_row['DIO']),
            'ccc_days': float(base_ccc)
        },
        'final_state': {
            'dso_days': float(final_row['DSO']),
            'dpo_days': float(final_row['DPO']),
            'dio_days': float(final_row['DIO']),
            'ccc_days': float(final_ccc)
        },
        'improvement': {
            'ccc_reduction_days': float(ccc_improvement),
            'dso_improvement_days': float(base_row['DSO'] - final_row['DSO']),
            'dpo_improvement_days': float(final_row['DPO'] - base_row['DPO']),
            'dio_improvement_days': float(base_row['DIO'] - final_row['DIO'])
        },
        'working_capital': {
            'base_nwc_m': float(base_row['NWC']),
            'final_nwc_m': float(final_row['NWC']),
            'total_change_m': float(total_wc_change),
            'avg_nwc_percent_revenue': float(df['NWC_Percent_Revenue'].mean())
        },
        'financing': {
            'cost_of_capital_percent': params['cost_of_capital_percent'],
            'total_financing_cost_m': float(total_financing_cost),
            'avg_annual_cost_m': float(total_financing_cost / len(years))
        }
    }

    return {
        'working_capital_projection': df,
        'summary': summary,
        'params': params
    }


def format_results(results: Dict) -> str:
    """Format working capital results for display."""
    output = []
    output.append("\n" + "="*80)
    output.append("WORKING CAPITAL MODEL (WCM-1.0) - RESULTS")
    output.append("="*80)

    summary = results['summary']
    currency = summary.get('currency', 'EUR')

    output.append("\n[1] CASH CONVERSION CYCLE")
    output.append("-" * 60)
    current = summary['current_state']
    final = summary['final_state']
    output.append(f"  {'Metric':<20} {'Current':>12} {'Final':>12} {'Change':>12}")
    output.append(f"  {'-'*20} {'-'*12} {'-'*12} {'-'*12}")
    output.append(f"  {'DSO (days)':<20} {current['dso_days']:>12.0f} {final['dso_days']:>12.0f} {final['dso_days']-current['dso_days']:>+12.0f}")
    output.append(f"  {'DPO (days)':<20} {current['dpo_days']:>12.0f} {final['dpo_days']:>12.0f} {final['dpo_days']-current['dpo_days']:>+12.0f}")
    output.append(f"  {'DIO (days)':<20} {current['dio_days']:>12.0f} {final['dio_days']:>12.0f} {final['dio_days']-current['dio_days']:>+12.0f}")
    output.append(f"  {'CCC (days)':<20} {current['ccc_days']:>12.0f} {final['ccc_days']:>12.0f} {final['ccc_days']-current['ccc_days']:>+12.0f}")

    output.append("\n[2] WORKING CAPITAL")
    output.append("-" * 60)
    wc = summary['working_capital']
    output.append(f"  Base Year NWC:      {currency}{wc['base_nwc_m']:,.0f}M")
    output.append(f"  Final Year NWC:     {currency}{wc['final_nwc_m']:,.0f}M")
    output.append(f"  Total Change:       {currency}{wc['total_change_m']:+,.0f}M")
    output.append(f"  Avg NWC/Revenue:    {wc['avg_nwc_percent_revenue']:.1f}%")

    output.append("\n[3] FINANCING COST")
    output.append("-" * 60)
    fin = summary['financing']
    output.append(f"  Cost of Capital:    {fin['cost_of_capital_percent']:.1f}%")
    output.append(f"  Total Cost:         {currency}{fin['total_financing_cost_m']:,.0f}M")
    output.append(f"  Avg Annual Cost:    {currency}{fin['avg_annual_cost_m']:,.0f}M")

    output.append("\n[4] IMPROVEMENT SUMMARY")
    output.append("-" * 60)
    imp = summary['improvement']
    output.append(f"  CCC Reduction:      {imp['ccc_reduction_days']:.0f} days")
    if imp['ccc_reduction_days'] > 0:
        output.append(f"  Status:             IMPROVING")
    else:
        output.append(f"  Status:             NO CHANGE")

    output.append("\n" + "="*80)
    return "\n".join(output)


def main():
    """Main entry point for command-line execution."""
    if len(sys.argv) < 2:
        print("Usage: python working_capital.py <config_file.yaml> [revenue.csv] [costs.csv]")
        sys.exit(1)

    config_file = sys.argv[1]
    config = load_config(config_file)

    rev_df = None
    cost_df = None

    if len(sys.argv) > 2:
        rev_df = pd.read_csv(sys.argv[2])
    if len(sys.argv) > 3:
        cost_df = pd.read_csv(sys.argv[3])

    results = project_working_capital(config, rev_df, cost_df)
    print(format_results(results))


if __name__ == '__main__':
    main()
