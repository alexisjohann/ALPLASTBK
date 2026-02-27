#!/usr/bin/env python3
"""
Cost Structure Model (CSM-1.0)
Generic operating cost projection by cost block.

Usage:
    from cost_structure import project_costs
    result = project_costs(config)

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


def extract_cost_params(config: Dict) -> Dict:
    """
    Extract cost structure parameters from configuration.

    Expected config structure:
    ```yaml
    cost_model:
      base_year: 2024
      projection_years: 11
      currency: "EUR"

      cost_blocks:
        - name: "Personnel"
          type: "variable"  # or "fixed" or "semi_variable"
          base_value_m: 500
          percent_of_revenue: 25  # for variable costs
          escalation_rate: 3.0

        - name: "Materials"
          type: "variable"
          percent_of_revenue: 40
          escalation_rate: 2.0

        - name: "Rent & Facilities"
          type: "fixed"
          base_value_m: 50
          escalation_rate: 2.5
    ```
    """
    cost_config = config.get('cost_model', {})

    params = {
        'base_year': cost_config.get('base_year', 2024),
        'projection_years': cost_config.get('projection_years', 11),
        'currency': cost_config.get('currency', 'EUR'),
        'cost_blocks': cost_config.get('cost_blocks', [])
    }

    # If no cost_blocks defined, try to infer from strategic_assumptions
    if not params['cost_blocks']:
        assumptions = config.get('strategic_assumptions', {})

        # Try to build cost blocks from payroll data
        payroll = assumptions.get('total_payroll_evolution', {})
        if payroll:
            base_payroll = payroll.get('year_2024_eur_m', 0)
            payroll_cagr = payroll.get('cagr_percent', 3.0)
            if base_payroll > 0:
                params['cost_blocks'].append({
                    'name': 'Personnel',
                    'type': 'semi_variable',
                    'base_value_m': base_payroll,
                    'escalation_rate': payroll_cagr
                })

    return params


def project_cost_block(
    block: Dict,
    years: np.ndarray,
    base_year: int,
    revenue_projection: Optional[pd.DataFrame] = None
) -> np.ndarray:
    """
    Project a single cost block over time.

    Args:
        block: Cost block parameters
        years: Array of years to project
        base_year: Base year for calculations
        revenue_projection: Optional revenue projection for variable costs

    Returns:
        Array of projected costs
    """
    cost_type = block.get('type', 'fixed')
    base_value = block.get('base_value_m', 0)
    escalation = block.get('escalation_rate', 0) / 100
    pct_of_revenue = block.get('percent_of_revenue', 0) / 100

    years_from_base = years - base_year

    if cost_type == 'variable' and revenue_projection is not None and pct_of_revenue > 0:
        # Variable cost: % of revenue
        if 'Total' in revenue_projection.columns:
            revenues = revenue_projection['Total'].values
            costs = revenues * pct_of_revenue
        else:
            # Fallback to base value with escalation
            costs = base_value * np.power(1 + escalation, years_from_base)

    elif cost_type == 'semi_variable' and revenue_projection is not None and pct_of_revenue > 0:
        # Semi-variable: base + % of revenue growth
        if 'Total' in revenue_projection.columns:
            revenues = revenue_projection['Total'].values
            base_revenue = revenues[0] if len(revenues) > 0 else 1
            revenue_growth = revenues / base_revenue
            costs = base_value * np.power(1 + escalation, years_from_base) * np.sqrt(revenue_growth)
        else:
            costs = base_value * np.power(1 + escalation, years_from_base)

    else:
        # Fixed cost: base value with escalation
        costs = base_value * np.power(1 + escalation, years_from_base)

    return costs


def project_costs(
    config: Dict,
    revenue_projection: Optional[pd.DataFrame] = None
) -> Dict:
    """
    Main function: Project cost structure over planning horizon.

    Args:
        config: Configuration dictionary (from YAML)
        revenue_projection: Optional DataFrame with revenue projection (for variable costs)

    Returns:
        Dictionary with:
        - cost_projection: DataFrame with costs by block and year
        - summary: Summary metrics
        - cost_blocks: Original cost block definitions
    """
    params = extract_cost_params(config)

    base_year = params['base_year']
    num_years = params['projection_years']
    years = np.arange(base_year, base_year + num_years)

    # Align revenue projection if provided
    if revenue_projection is not None and 'Year' in revenue_projection.columns:
        # Filter to matching years
        revenue_projection = revenue_projection[
            revenue_projection['Year'].isin(years)
        ].reset_index(drop=True)

    # Project each cost block
    data = {'Year': years}

    for block in params['cost_blocks']:
        block_name = block.get('name', 'Unknown')
        costs = project_cost_block(block, years, base_year, revenue_projection)
        data[block_name] = np.round(costs, 1)

    df = pd.DataFrame(data)

    # Add total column
    cost_cols = [c for c in df.columns if c != 'Year']
    if cost_cols:
        df['Total_Costs'] = df[cost_cols].sum(axis=1).round(1)
    else:
        df['Total_Costs'] = 0

    # Calculate YoY growth
    df['YoY%'] = df['Total_Costs'].pct_change() * 100

    # Add cost as % of revenue if revenue provided
    if revenue_projection is not None and 'Total' in revenue_projection.columns:
        df['Revenue'] = revenue_projection['Total'].values[:len(df)]
        df['Cost_Pct_Revenue'] = (df['Total_Costs'] / df['Revenue'] * 100).round(1)

    # Calculate summary
    base_costs = df[df['Year'] == base_year]['Total_Costs'].values[0] if len(df) > 0 else 0
    final_costs = df[df['Year'] == base_year + num_years - 1]['Total_Costs'].values[0] if len(df) > 0 else 0

    summary = {
        'base_year': base_year,
        'base_year_costs_m': float(base_costs),
        'final_year': base_year + num_years - 1,
        'final_year_costs_m': float(final_costs),
        'total_growth_m': float(final_costs - base_costs),
        'growth_percent': float((final_costs / base_costs - 1) * 100) if base_costs > 0 else 0,
        'cagr_percent': float((pow(final_costs / base_costs, 1 / (num_years - 1)) - 1) * 100) if base_costs > 0 else 0,
        'num_cost_blocks': len(params['cost_blocks']),
        'currency': params['currency']
    }

    # Add cost breakdown for final year
    if cost_cols:
        final_row = df[df['Year'] == base_year + num_years - 1]
        if not final_row.empty:
            summary['cost_breakdown'] = {
                col: float(final_row[col].values[0])
                for col in cost_cols
            }

    return {
        'cost_projection': df,
        'summary': summary,
        'cost_blocks': params['cost_blocks'],
        'params': params
    }


def format_results(results: Dict) -> str:
    """Format cost structure results for display."""
    output = []
    output.append("\n" + "="*80)
    output.append("COST STRUCTURE MODEL (CSM-1.0) - RESULTS")
    output.append("="*80)

    summary = results['summary']

    output.append("\n[1] SUMMARY METRICS")
    output.append("-" * 60)
    output.append(f"  Base Year ({summary['base_year']}) Costs:  {summary['currency']}{summary['base_year_costs_m']:,.0f}M")
    output.append(f"  Final Year ({summary['final_year']}) Costs: {summary['currency']}{summary['final_year_costs_m']:,.0f}M")
    output.append(f"  Total Growth:              {summary['currency']}{summary['total_growth_m']:,.0f}M (+{summary['growth_percent']:.1f}%)")
    output.append(f"  Cost CAGR:                 {summary['cagr_percent']:.2f}%")
    output.append(f"  Cost Blocks:               {summary['num_cost_blocks']}")

    if 'cost_breakdown' in summary:
        output.append("\n[2] COST BREAKDOWN (Final Year)")
        output.append("-" * 60)
        for block, value in summary['cost_breakdown'].items():
            output.append(f"  {block}: {summary['currency']}{value:,.0f}M")

    output.append("\n[3] COST PROJECTION")
    output.append("-" * 60)
    df = results['cost_projection']
    # Show key years
    key_years = [summary['base_year'], summary['base_year'] + 2,
                 summary['base_year'] + 5, summary['final_year']]
    key_rows = df[df['Year'].isin(key_years)]
    output.append(key_rows.to_string(index=False))

    output.append("\n" + "="*80)
    return "\n".join(output)


def main():
    """Main entry point for command-line execution."""
    if len(sys.argv) < 2:
        print("Usage: python cost_structure.py <config_file.yaml> [revenue_file.csv]")
        sys.exit(1)

    config_file = sys.argv[1]
    revenue_file = sys.argv[2] if len(sys.argv) > 2 else None

    print(f"Loading configuration: {config_file}")
    config = load_configuration(config_file)

    revenue_df = None
    if revenue_file:
        print(f"Loading revenue projection: {revenue_file}")
        revenue_df = pd.read_csv(revenue_file)

    print("Running cost structure model...")
    results = project_costs(config, revenue_df)

    print(format_results(results))


if __name__ == '__main__':
    main()
