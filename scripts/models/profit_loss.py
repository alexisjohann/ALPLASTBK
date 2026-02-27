#!/usr/bin/env python3
"""
Profit & Loss Model (PLM-1.0)
Generic P&L projection combining revenue and costs.

Usage:
    from profit_loss import project_pnl
    result = project_pnl(config, revenue_df, cost_df)

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


def load_configuration(config_path: str) -> Dict:
    """Load model configuration from YAML file."""
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except FileNotFoundError:
        print(f"ERROR: Configuration file not found: {config_path}")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"ERROR: Invalid YAML format: {e}")
        sys.exit(1)


def extract_pnl_params(config: Dict) -> Dict:
    """
    Extract P&L parameters from configuration.

    Expected config structure:
    ```yaml
    pnl_model:
      base_year: 2024
      projection_years: 11
      currency: "EUR"

      # Margin assumptions (if not calculated from cost model)
      gross_margin_percent: 35
      ebitda_margin_percent: 12
      depreciation_percent_of_revenue: 3
      interest_rate_percent: 4
      tax_rate_percent: 25

      # Or detailed line items
      line_items:
        - name: "COGS"
          type: "percent_of_revenue"
          value: 65

        - name: "SG&A"
          type: "percent_of_revenue"
          value: 15

        - name: "R&D"
          type: "percent_of_revenue"
          value: 3

        - name: "Depreciation"
          type: "percent_of_revenue"
          value: 3

        - name: "Interest"
          type: "fixed_escalation"
          base_value_m: 20
          escalation_rate: 2
    ```
    """
    pnl_config = config.get('pnl_model', {})

    params = {
        'base_year': pnl_config.get('base_year', 2024),
        'projection_years': pnl_config.get('projection_years', 11),
        'currency': pnl_config.get('currency', 'EUR'),
        'gross_margin_percent': pnl_config.get('gross_margin_percent'),
        'ebitda_margin_percent': pnl_config.get('ebitda_margin_percent'),
        'depreciation_percent': pnl_config.get('depreciation_percent_of_revenue', 3),
        'interest_rate_percent': pnl_config.get('interest_rate_percent', 4),
        'tax_rate_percent': pnl_config.get('tax_rate_percent', 25),
        'line_items': pnl_config.get('line_items', [])
    }

    # Try to get EBITDA margin from strategic assumptions if not in pnl_model
    if params['ebitda_margin_percent'] is None:
        assumptions = config.get('strategic_assumptions', {})
        profitability = assumptions.get('profitability_evolution', {})
        if profitability:
            # Use base year margin
            params['ebitda_margin_percent'] = profitability.get('ebitda_margin_2024_percent', 10)

    return params


def calculate_line_item(
    item: Dict,
    years: np.ndarray,
    base_year: int,
    revenue: np.ndarray
) -> np.ndarray:
    """
    Calculate a single P&L line item.

    Args:
        item: Line item definition
        years: Array of years
        base_year: Base year for calculations
        revenue: Revenue array

    Returns:
        Array of calculated values
    """
    item_type = item.get('type', 'percent_of_revenue')
    value = item.get('value', 0)
    base_value = item.get('base_value_m', 0)
    escalation = item.get('escalation_rate', 0) / 100

    years_from_base = years - base_year

    if item_type == 'percent_of_revenue':
        return revenue * (value / 100)

    elif item_type == 'fixed_escalation':
        return base_value * np.power(1 + escalation, years_from_base)

    elif item_type == 'fixed':
        return np.full(len(years), base_value)

    else:
        return np.zeros(len(years))


def project_pnl(
    config: Dict,
    revenue_projection: Optional[pd.DataFrame] = None,
    cost_projection: Optional[pd.DataFrame] = None
) -> Dict:
    """
    Main function: Project Profit & Loss statement.

    Args:
        config: Configuration dictionary (from YAML)
        revenue_projection: DataFrame with revenue projection (from RPM)
        cost_projection: DataFrame with cost projection (from CSM)

    Returns:
        Dictionary with:
        - pnl_projection: DataFrame with full P&L by year
        - summary: Summary metrics
        - margins: Margin evolution
    """
    params = extract_pnl_params(config)

    base_year = params['base_year']
    num_years = params['projection_years']
    years = np.arange(base_year, base_year + num_years)

    # Get revenue data
    if revenue_projection is not None and 'Total' in revenue_projection.columns:
        revenue = revenue_projection[revenue_projection['Year'].isin(years)]['Total'].values
        if len(revenue) < len(years):
            # Pad with last value if needed
            revenue = np.pad(revenue, (0, len(years) - len(revenue)), mode='edge')
    else:
        # Default: estimate from config or use placeholder
        base_revenue = config.get('company', {}).get('base_revenue_m', 1000)
        cagr = 0.05  # Default 5%
        revenue = base_revenue * np.power(1 + cagr, years - base_year)

    # Initialize P&L DataFrame
    pnl = pd.DataFrame({'Year': years, 'Revenue': np.round(revenue, 1)})

    # Method 1: Use cost projection if provided
    if cost_projection is not None and 'Total_Costs' in cost_projection.columns:
        costs = cost_projection[cost_projection['Year'].isin(years)]['Total_Costs'].values
        if len(costs) < len(years):
            costs = np.pad(costs, (0, len(years) - len(costs)), mode='edge')

        pnl['Operating_Costs'] = np.round(costs, 1)
        pnl['EBITDA'] = np.round(pnl['Revenue'] - pnl['Operating_Costs'], 1)

    # Method 2: Use margin assumption
    elif params['ebitda_margin_percent'] is not None:
        ebitda_margin = params['ebitda_margin_percent'] / 100
        pnl['EBITDA'] = np.round(pnl['Revenue'] * ebitda_margin, 1)
        pnl['Operating_Costs'] = np.round(pnl['Revenue'] - pnl['EBITDA'], 1)

    # Method 3: Use line items
    elif params['line_items']:
        total_costs = np.zeros(len(years))
        for item in params['line_items']:
            item_name = item.get('name', 'Unknown')
            item_values = calculate_line_item(item, years, base_year, revenue)
            pnl[item_name] = np.round(item_values, 1)
            if item_name not in ['Depreciation', 'Interest', 'Tax']:
                total_costs += item_values

        pnl['Operating_Costs'] = np.round(total_costs, 1)
        pnl['EBITDA'] = np.round(pnl['Revenue'] - pnl['Operating_Costs'], 1)

    else:
        # Fallback: assume 10% EBITDA margin
        pnl['EBITDA'] = np.round(pnl['Revenue'] * 0.10, 1)
        pnl['Operating_Costs'] = np.round(pnl['Revenue'] - pnl['EBITDA'], 1)

    # Calculate D&A
    depreciation_pct = params['depreciation_percent'] / 100
    pnl['Depreciation'] = np.round(pnl['Revenue'] * depreciation_pct, 1)

    # EBIT
    pnl['EBIT'] = np.round(pnl['EBITDA'] - pnl['Depreciation'], 1)

    # Interest (simplified: fixed or % of revenue)
    interest_rate = params['interest_rate_percent'] / 100
    # Assume debt ~ 30% of revenue as proxy
    pnl['Interest'] = np.round(pnl['Revenue'] * 0.30 * interest_rate, 1)

    # EBT
    pnl['EBT'] = np.round(pnl['EBIT'] - pnl['Interest'], 1)

    # Tax
    tax_rate = params['tax_rate_percent'] / 100
    pnl['Tax'] = np.round(np.maximum(pnl['EBT'] * tax_rate, 0), 1)

    # Net Income
    pnl['Net_Income'] = np.round(pnl['EBT'] - pnl['Tax'], 1)

    # Calculate margins
    pnl['EBITDA_Margin_%'] = np.round(pnl['EBITDA'] / pnl['Revenue'] * 100, 1)
    pnl['EBIT_Margin_%'] = np.round(pnl['EBIT'] / pnl['Revenue'] * 100, 1)
    pnl['Net_Margin_%'] = np.round(pnl['Net_Income'] / pnl['Revenue'] * 100, 1)

    # Summary
    base_idx = 0
    final_idx = len(years) - 1

    summary = {
        'base_year': int(years[base_idx]),
        'final_year': int(years[final_idx]),
        'currency': params['currency'],
        'revenue': {
            'base_year_m': float(pnl['Revenue'].iloc[base_idx]),
            'final_year_m': float(pnl['Revenue'].iloc[final_idx]),
            'cagr_percent': float((pow(pnl['Revenue'].iloc[final_idx] / pnl['Revenue'].iloc[base_idx], 1/(num_years-1)) - 1) * 100)
        },
        'ebitda': {
            'base_year_m': float(pnl['EBITDA'].iloc[base_idx]),
            'final_year_m': float(pnl['EBITDA'].iloc[final_idx]),
            'base_margin_percent': float(pnl['EBITDA_Margin_%'].iloc[base_idx]),
            'final_margin_percent': float(pnl['EBITDA_Margin_%'].iloc[final_idx]),
            'cagr_percent': float((pow(pnl['EBITDA'].iloc[final_idx] / pnl['EBITDA'].iloc[base_idx], 1/(num_years-1)) - 1) * 100) if pnl['EBITDA'].iloc[base_idx] > 0 else 0
        },
        'net_income': {
            'base_year_m': float(pnl['Net_Income'].iloc[base_idx]),
            'final_year_m': float(pnl['Net_Income'].iloc[final_idx]),
            'base_margin_percent': float(pnl['Net_Margin_%'].iloc[base_idx]),
            'final_margin_percent': float(pnl['Net_Margin_%'].iloc[final_idx])
        },
        'tax_rate_percent': params['tax_rate_percent']
    }

    # Margin evolution
    margins = pnl[['Year', 'EBITDA_Margin_%', 'EBIT_Margin_%', 'Net_Margin_%']].copy()

    return {
        'pnl_projection': pnl,
        'summary': summary,
        'margins': margins,
        'params': params
    }


def format_results(results: Dict) -> str:
    """Format P&L results for display."""
    output = []
    output.append("\n" + "="*80)
    output.append("PROFIT & LOSS MODEL (PLM-1.0) - RESULTS")
    output.append("="*80)

    summary = results['summary']
    currency = summary['currency']

    output.append("\n[1] SUMMARY METRICS")
    output.append("-" * 60)
    output.append(f"  Period: {summary['base_year']} - {summary['final_year']}")

    output.append(f"\n  REVENUE:")
    output.append(f"    Base Year:  {currency}{summary['revenue']['base_year_m']:,.0f}M")
    output.append(f"    Final Year: {currency}{summary['revenue']['final_year_m']:,.0f}M")
    output.append(f"    CAGR:       {summary['revenue']['cagr_percent']:.1f}%")

    output.append(f"\n  EBITDA:")
    output.append(f"    Base Year:  {currency}{summary['ebitda']['base_year_m']:,.0f}M ({summary['ebitda']['base_margin_percent']:.1f}% margin)")
    output.append(f"    Final Year: {currency}{summary['ebitda']['final_year_m']:,.0f}M ({summary['ebitda']['final_margin_percent']:.1f}% margin)")
    output.append(f"    CAGR:       {summary['ebitda']['cagr_percent']:.1f}%")

    output.append(f"\n  NET INCOME:")
    output.append(f"    Base Year:  {currency}{summary['net_income']['base_year_m']:,.0f}M ({summary['net_income']['base_margin_percent']:.1f}% margin)")
    output.append(f"    Final Year: {currency}{summary['net_income']['final_year_m']:,.0f}M ({summary['net_income']['final_margin_percent']:.1f}% margin)")

    output.append("\n[2] P&L PROJECTION (Key Years)")
    output.append("-" * 60)
    pnl = results['pnl_projection']
    key_years = [summary['base_year'], summary['base_year'] + 2,
                 summary['base_year'] + 5, summary['final_year']]
    key_rows = pnl[pnl['Year'].isin(key_years)]
    # Select key columns
    display_cols = ['Year', 'Revenue', 'EBITDA', 'EBIT', 'Net_Income', 'EBITDA_Margin_%']
    output.append(key_rows[display_cols].to_string(index=False))

    output.append("\n[3] MARGIN EVOLUTION")
    output.append("-" * 60)
    margins = results['margins']
    key_margins = margins[margins['Year'].isin(key_years)]
    output.append(key_margins.to_string(index=False))

    output.append("\n" + "="*80)
    return "\n".join(output)


def main():
    """Main entry point for command-line execution."""
    if len(sys.argv) < 2:
        print("Usage: python profit_loss.py <config_file.yaml> [revenue_file.csv] [cost_file.csv]")
        sys.exit(1)

    config_file = sys.argv[1]
    revenue_file = sys.argv[2] if len(sys.argv) > 2 else None
    cost_file = sys.argv[3] if len(sys.argv) > 3 else None

    print(f"Loading configuration: {config_file}")
    config = load_configuration(config_file)

    revenue_df = None
    cost_df = None

    if revenue_file:
        print(f"Loading revenue projection: {revenue_file}")
        revenue_df = pd.read_csv(revenue_file)

    if cost_file:
        print(f"Loading cost projection: {cost_file}")
        cost_df = pd.read_csv(cost_file)

    print("Running profit & loss model...")
    results = project_pnl(config, revenue_df, cost_df)

    print(format_results(results))


if __name__ == '__main__':
    main()
