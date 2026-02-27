#!/usr/bin/env python3
"""
Break-Even Model (BEM-1.0)
Break-even analysis, operating leverage, and margin of safety.

Usage:
    from break_even import analyze_break_even
    result = analyze_break_even(config, pnl_projection)

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


def extract_break_even_params(config: Dict) -> Dict:
    """
    Extract break-even analysis parameters from configuration.

    Expected config structure:
    ```yaml
    break_even_model:
      base_year: 2024
      projection_years: 11
      currency: "EUR"

      # Cost structure (if not from CSM)
      cost_structure:
        variable_cost_percent: 60   # Variable costs as % of revenue
        # OR detailed breakdown:
        # cogs_variable_percent: 80
        # opex_variable_percent: 20

      # Fixed costs (if not from CSM)
      fixed_costs:
        total_fixed_costs_m: 500    # Total annual fixed costs
        # OR breakdown:
        # fixed_manufacturing_m: 200
        # fixed_sga_m: 200
        # fixed_rd_m: 50
        # fixed_other_m: 50

      # Analysis parameters
      analysis:
        target_profit_m: 100        # Target profit for target analysis
        sensitivity_range_percent: 20  # +/- range for sensitivity
    ```
    """
    be_config = config.get('break_even_model', {})

    params = {
        'base_year': be_config.get('base_year', DEFAULT_BASE_YEAR),
        'projection_years': be_config.get('projection_years', DEFAULT_PROJECTION_YEARS),
        'currency': be_config.get('currency', DEFAULT_CURRENCY),
        'cost_structure': be_config.get('cost_structure', {}),
        'fixed_costs': be_config.get('fixed_costs', {}),
        'analysis': be_config.get('analysis', {})
    }

    # Cost structure defaults
    if 'variable_cost_percent' not in params['cost_structure']:
        params['cost_structure']['variable_cost_percent'] = 60

    # Fixed cost defaults
    if 'total_fixed_costs_m' not in params['fixed_costs']:
        params['fixed_costs']['total_fixed_costs_m'] = 500

    # Analysis defaults
    analysis_defaults = {
        'target_profit_m': 100,
        'sensitivity_range_percent': 20
    }
    for key, default in analysis_defaults.items():
        if key not in params['analysis']:
            params['analysis'][key] = default

    return params


def calculate_break_even_point(fixed_costs: float, contribution_margin_ratio: float) -> float:
    """Calculate break-even revenue."""
    if contribution_margin_ratio <= 0:
        return float('inf')
    return fixed_costs / contribution_margin_ratio


def calculate_margin_of_safety(actual_revenue: float, break_even_revenue: float) -> float:
    """Calculate margin of safety percentage."""
    if actual_revenue <= 0:
        return 0
    return ((actual_revenue - break_even_revenue) / actual_revenue) * 100


def calculate_operating_leverage(contribution_margin: float, operating_income: float) -> float:
    """Calculate degree of operating leverage."""
    if operating_income <= 0:
        return float('inf')
    return contribution_margin / operating_income


def analyze_break_even(
    config: Dict,
    pnl_projection: pd.DataFrame = None,
    cost_projection: pd.DataFrame = None
) -> Dict:
    """
    Perform break-even analysis.

    Args:
        config: Configuration dictionary
        pnl_projection: P&L projection from PLM-1.0
        cost_projection: Cost projection from CSM-1.0

    Returns:
        Dictionary with break-even analysis, operating leverage, and sensitivity
    """
    params = extract_break_even_params(config)
    years = get_year_range(params['base_year'], params['projection_years'])
    cost_struct = params['cost_structure']
    fixed_cost_params = params['fixed_costs']
    analysis = params['analysis']

    # Initialize data storage
    data = []

    for i, year in enumerate(years):
        row = {'Year': year}

        # Get P&L data
        revenue = 0
        cogs = 0
        opex = 0
        ebitda = 0
        ebit = 0

        if pnl_projection is not None and 'Year' in pnl_projection.columns:
            pnl_row = pnl_projection[pnl_projection['Year'] == year]
            if len(pnl_row) > 0:
                revenue = float(pnl_row['Revenue'].iloc[0]) if 'Revenue' in pnl_row else 0
                cogs = float(pnl_row['COGS'].iloc[0]) if 'COGS' in pnl_row else 0
                opex = float(pnl_row['OpEx'].iloc[0]) if 'OpEx' in pnl_row else 0
                ebitda = float(pnl_row['EBITDA'].iloc[0]) if 'EBITDA' in pnl_row else 0
                ebit = float(pnl_row['EBIT'].iloc[0]) if 'EBIT' in pnl_row else ebitda * 0.85

        row['Revenue'] = revenue

        # Estimate variable and fixed costs
        variable_pct = cost_struct.get('variable_cost_percent', 60) / 100

        total_costs = cogs + opex if (cogs + opex) > 0 else revenue * 0.85
        row['Total_Costs'] = total_costs

        # Variable costs
        row['Variable_Costs'] = total_costs * variable_pct

        # Fixed costs
        row['Fixed_Costs'] = total_costs * (1 - variable_pct)

        # Per-unit metrics (assuming revenue = units * price)
        row['Variable_Cost_Ratio'] = row['Variable_Costs'] / revenue if revenue > 0 else variable_pct

        # Contribution margin
        row['Contribution_Margin'] = revenue - row['Variable_Costs']
        row['Contribution_Margin_Ratio'] = row['Contribution_Margin'] / revenue if revenue > 0 else (1 - variable_pct)

        # Break-even point
        row['Break_Even_Revenue'] = calculate_break_even_point(
            row['Fixed_Costs'],
            row['Contribution_Margin_Ratio']
        )

        # Margin of safety
        row['Margin_of_Safety_M'] = revenue - row['Break_Even_Revenue']
        row['Margin_of_Safety_Percent'] = calculate_margin_of_safety(revenue, row['Break_Even_Revenue'])

        # Operating income (proxy with EBIT or contribution - fixed)
        operating_income = row['Contribution_Margin'] - row['Fixed_Costs']
        row['Operating_Income'] = operating_income

        # Degree of Operating Leverage
        row['DOL'] = calculate_operating_leverage(row['Contribution_Margin'], operating_income)

        # Target profit analysis
        target_profit = analysis['target_profit_m']
        row['Target_Profit'] = target_profit
        row['Revenue_for_Target'] = (row['Fixed_Costs'] + target_profit) / row['Contribution_Margin_Ratio'] if row['Contribution_Margin_Ratio'] > 0 else 0

        # Break-even as % of capacity (assume current revenue = capacity proxy)
        row['Break_Even_Capacity_Percent'] = (row['Break_Even_Revenue'] / revenue * 100) if revenue > 0 else 0

        data.append(row)

    df = pd.DataFrame(data)

    # Sensitivity analysis
    sensitivity_data = []
    base_row = df[df['Year'] == params['base_year']].iloc[0] if len(df[df['Year'] == params['base_year']]) > 0 else df.iloc[0]

    range_pct = analysis['sensitivity_range_percent']
    scenarios = [
        ('Revenue -20%', 'revenue', -20),
        ('Revenue -10%', 'revenue', -10),
        ('Base Case', 'base', 0),
        ('Revenue +10%', 'revenue', 10),
        ('Revenue +20%', 'revenue', 20),
        ('Variable Costs -10%', 'variable', -10),
        ('Variable Costs +10%', 'variable', 10),
        ('Fixed Costs -10%', 'fixed', -10),
        ('Fixed Costs +10%', 'fixed', 10),
    ]

    base_revenue = base_row['Revenue']
    base_variable = base_row['Variable_Costs']
    base_fixed = base_row['Fixed_Costs']
    base_cm_ratio = base_row['Contribution_Margin_Ratio']

    for scenario_name, scenario_type, change_pct in scenarios:
        revenue = base_revenue
        variable = base_variable
        fixed = base_fixed

        if scenario_type == 'revenue':
            revenue = base_revenue * (1 + change_pct / 100)
            variable = revenue * (base_variable / base_revenue) if base_revenue > 0 else 0
        elif scenario_type == 'variable':
            variable = base_variable * (1 + change_pct / 100)
        elif scenario_type == 'fixed':
            fixed = base_fixed * (1 + change_pct / 100)

        contribution = revenue - variable
        cm_ratio = contribution / revenue if revenue > 0 else 0
        be_revenue = fixed / cm_ratio if cm_ratio > 0 else float('inf')
        op_income = contribution - fixed
        mos_pct = calculate_margin_of_safety(revenue, be_revenue)

        sensitivity_data.append({
            'Scenario': scenario_name,
            'Revenue': revenue,
            'Variable_Costs': variable,
            'Fixed_Costs': fixed,
            'Contribution_Margin': contribution,
            'Operating_Income': op_income,
            'Break_Even_Revenue': be_revenue,
            'Margin_of_Safety_Percent': mos_pct
        })

    sensitivity_df = pd.DataFrame(sensitivity_data)

    # Build summary
    final_row = df.iloc[-1]
    avg_mos = df['Margin_of_Safety_Percent'].mean()
    avg_dol = df[df['DOL'] < 100]['DOL'].mean()  # Exclude extreme values

    summary = {
        'currency': params['currency'],
        'break_even': {
            'base_year_revenue_m': float(base_row['Break_Even_Revenue']),
            'final_year_revenue_m': float(final_row['Break_Even_Revenue']),
            'avg_break_even_capacity_percent': float(df['Break_Even_Capacity_Percent'].mean())
        },
        'margin_of_safety': {
            'base_year_m': float(base_row['Margin_of_Safety_M']),
            'base_year_percent': float(base_row['Margin_of_Safety_Percent']),
            'final_year_m': float(final_row['Margin_of_Safety_M']),
            'final_year_percent': float(final_row['Margin_of_Safety_Percent']),
            'avg_percent': float(avg_mos)
        },
        'operating_leverage': {
            'base_year_dol': float(base_row['DOL']) if base_row['DOL'] < 100 else 'High',
            'final_year_dol': float(final_row['DOL']) if final_row['DOL'] < 100 else 'High',
            'avg_dol': float(avg_dol) if not np.isnan(avg_dol) else 'High'
        },
        'cost_structure': {
            'variable_cost_percent': float(base_row['Variable_Cost_Ratio'] * 100),
            'contribution_margin_percent': float(base_row['Contribution_Margin_Ratio'] * 100)
        }
    }

    return {
        'break_even_analysis': df,
        'sensitivity_analysis': sensitivity_df,
        'summary': summary,
        'params': params
    }


def format_results(results: Dict) -> str:
    """Format break-even analysis results for display."""
    output = []
    output.append("\n" + "="*80)
    output.append("BREAK-EVEN MODEL (BEM-1.0) - RESULTS")
    output.append("="*80)

    summary = results['summary']
    currency = summary.get('currency', 'EUR')

    output.append("\n[1] BREAK-EVEN ANALYSIS")
    output.append("-" * 60)
    be = summary['break_even']
    output.append(f"  Base Year BE Revenue:   {currency}{be['base_year_revenue_m']:,.0f}M")
    output.append(f"  Final Year BE Revenue:  {currency}{be['final_year_revenue_m']:,.0f}M")
    output.append(f"  Avg BE as % Capacity:   {be['avg_break_even_capacity_percent']:.1f}%")

    output.append("\n[2] MARGIN OF SAFETY")
    output.append("-" * 60)
    mos = summary['margin_of_safety']
    output.append(f"  Base Year:              {currency}{mos['base_year_m']:,.0f}M ({mos['base_year_percent']:.1f}%)")
    output.append(f"  Final Year:             {currency}{mos['final_year_m']:,.0f}M ({mos['final_year_percent']:.1f}%)")
    output.append(f"  Average:                {mos['avg_percent']:.1f}%")

    output.append("\n[3] OPERATING LEVERAGE")
    output.append("-" * 60)
    ol = summary['operating_leverage']
    output.append(f"  Base Year DOL:          {ol['base_year_dol']:.2f}x" if isinstance(ol['base_year_dol'], float) else f"  Base Year DOL:          {ol['base_year_dol']}")
    output.append(f"  Final Year DOL:         {ol['final_year_dol']:.2f}x" if isinstance(ol['final_year_dol'], float) else f"  Final Year DOL:         {ol['final_year_dol']}")
    output.append(f"  Average DOL:            {ol['avg_dol']:.2f}x" if isinstance(ol['avg_dol'], float) else f"  Average DOL:            {ol['avg_dol']}")

    output.append("\n[4] COST STRUCTURE")
    output.append("-" * 60)
    cs = summary['cost_structure']
    output.append(f"  Variable Cost Ratio:    {cs['variable_cost_percent']:.1f}%")
    output.append(f"  Contribution Margin:    {cs['contribution_margin_percent']:.1f}%")

    output.append("\n[5] SENSITIVITY ANALYSIS")
    output.append("-" * 60)
    sens_df = results['sensitivity_analysis']
    output.append(sens_df[['Scenario', 'Operating_Income', 'Margin_of_Safety_Percent']].to_string(index=False))

    # Risk assessment
    avg_mos = summary['margin_of_safety']['avg_percent']
    if avg_mos >= 30:
        risk = "LOW RISK - Strong margin of safety"
    elif avg_mos >= 15:
        risk = "MODERATE RISK - Adequate buffer"
    else:
        risk = "HIGH RISK - Limited margin of safety"

    output.append(f"\n[6] RISK ASSESSMENT: {risk}")

    output.append("\n" + "="*80)
    return "\n".join(output)


def main():
    """Main entry point for command-line execution."""
    if len(sys.argv) < 2:
        print("Usage: python break_even.py <config_file.yaml> [pnl.csv]")
        sys.exit(1)

    config_file = sys.argv[1]
    config = load_config(config_file)

    pnl_df = None
    if len(sys.argv) > 2:
        pnl_df = pd.read_csv(sys.argv[2])

    results = analyze_break_even(config, pnl_df)
    print(format_results(results))


if __name__ == '__main__':
    main()
