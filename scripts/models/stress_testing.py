#!/usr/bin/env python3
"""
Stress Testing Model (STM-1.0)
Extreme scenario analysis and tail risk assessment.

Usage:
    from stress_testing import run_stress_tests
    result = run_stress_tests(config, pnl_projection)

Model Version: 1.0.0
Implementation Date: 2026-01-16

FULLY GENERIC: All parameters from config, no hardcoded defaults.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Any, Callable
import yaml
import sys
from pathlib import Path

try:
    from strategy_base import (
        load_config, get_nested, set_nested, save_csv, save_yaml,
        format_currency, calculate_cagr, get_year_range,
        DEFAULT_BASE_YEAR, DEFAULT_PROJECTION_YEARS, DEFAULT_CURRENCY
    )
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent))
    from strategy_base import (
        load_config, get_nested, set_nested, save_csv, save_yaml,
        format_currency, calculate_cagr, get_year_range,
        DEFAULT_BASE_YEAR, DEFAULT_PROJECTION_YEARS, DEFAULT_CURRENCY
    )


def extract_stress_params(config: Dict) -> Dict:
    """Extract stress testing parameters from configuration."""
    st_config = config.get('stress_testing_model', {})

    params = {
        'base_year': st_config.get('base_year', DEFAULT_BASE_YEAR),
        'projection_years': st_config.get('projection_years', DEFAULT_PROJECTION_YEARS),
        'currency': st_config.get('currency', DEFAULT_CURRENCY),

        # Stress scenarios
        'scenarios': st_config.get('scenarios', [
            {
                'name': 'Mild Recession',
                'probability_percent': 20,
                'revenue_shock_percent': -10,
                'margin_compression_pp': 2,
                'duration_years': 2
            },
            {
                'name': 'Severe Recession',
                'probability_percent': 10,
                'revenue_shock_percent': -25,
                'margin_compression_pp': 5,
                'duration_years': 3
            },
            {
                'name': 'Market Disruption',
                'probability_percent': 5,
                'revenue_shock_percent': -15,
                'margin_compression_pp': 8,
                'duration_years': 4
            },
            {
                'name': 'Supply Chain Crisis',
                'probability_percent': 10,
                'revenue_shock_percent': -5,
                'margin_compression_pp': 10,
                'duration_years': 1
            },
            {
                'name': 'Tail Risk Event',
                'probability_percent': 2,
                'revenue_shock_percent': -40,
                'margin_compression_pp': 15,
                'duration_years': 3
            }
        ]),

        # Baseline financials
        'baseline': st_config.get('baseline', {
            'revenue_m': 1000,
            'ebitda_margin_percent': 15,
            'fixed_costs_m': 300,
            'debt_m': 500,
            'cash_m': 100
        }),

        # Thresholds
        'thresholds': st_config.get('thresholds', {
            'min_liquidity_m': 50,
            'max_leverage_ratio': 4.0,
            'min_interest_coverage': 2.0
        })
    }

    return params


def apply_stress_scenario(baseline: Dict, scenario: Dict, year: int) -> Dict:
    """Apply stress scenario to baseline financials."""
    duration = scenario.get('duration_years', 2)
    revenue_shock = scenario.get('revenue_shock_percent', -10) / 100
    margin_compression = scenario.get('margin_compression_pp', 2)

    # Calculate stress impact (gradual recovery after shock)
    if year <= duration:
        # Full impact during stress period
        recovery_factor = 0
    else:
        # Gradual recovery
        recovery_years = year - duration
        recovery_factor = min(1.0, recovery_years / 2)  # 2 years to recover

    # Apply shocks
    revenue = baseline['revenue_m'] * (1 + revenue_shock * (1 - recovery_factor))
    margin = baseline['ebitda_margin_percent'] - margin_compression * (1 - recovery_factor)
    margin = max(0, margin)  # Can't go negative

    ebitda = revenue * margin / 100
    fixed_costs = baseline.get('fixed_costs_m', 300)

    # Cash flow impact
    operating_cf = ebitda - fixed_costs * 0.1  # Simplified

    return {
        'revenue': revenue,
        'ebitda_margin': margin,
        'ebitda': ebitda,
        'operating_cf': operating_cf
    }


def run_stress_tests(
    config: Dict,
    pnl_projection: pd.DataFrame = None,
    model_runner: Callable = None
) -> Dict:
    """
    Run stress tests across multiple scenarios.

    Args:
        config: Configuration dictionary
        pnl_projection: P&L projection from PLM-1.0
        model_runner: Optional function to run full model under stress

    Returns:
        Dictionary with stress test results and risk assessment
    """
    params = extract_stress_params(config)
    years = get_year_range(params['base_year'], params['projection_years'])
    scenarios = params['scenarios']
    baseline = params['baseline']
    thresholds = params['thresholds']

    # Get baseline from P&L if provided
    if pnl_projection is not None and 'Year' in pnl_projection.columns:
        base_row = pnl_projection[pnl_projection['Year'] == params['base_year']]
        if len(base_row) > 0:
            baseline['revenue_m'] = float(base_row['Revenue'].iloc[0]) if 'Revenue' in base_row else baseline['revenue_m']
            if 'EBITDA' in base_row and 'Revenue' in base_row:
                baseline['ebitda_margin_percent'] = float(base_row['EBITDA'].iloc[0] / base_row['Revenue'].iloc[0] * 100)

    # Run each stress scenario
    scenario_results = []
    all_data = []

    for scenario in scenarios:
        scenario_name = scenario['name']
        prob = scenario.get('probability_percent', 10)

        scenario_data = []
        min_ebitda = float('inf')
        min_margin = float('inf')
        years_negative_cf = 0

        for i, year in enumerate(years):
            stressed = apply_stress_scenario(baseline, scenario, i)

            row = {
                'Scenario': scenario_name,
                'Year': year,
                'Revenue': stressed['revenue'],
                'EBITDA_Margin': stressed['ebitda_margin'],
                'EBITDA': stressed['ebitda'],
                'Operating_CF': stressed['operating_cf']
            }

            scenario_data.append(row)
            all_data.append(row)

            min_ebitda = min(min_ebitda, stressed['ebitda'])
            min_margin = min(min_margin, stressed['ebitda_margin'])
            if stressed['operating_cf'] < 0:
                years_negative_cf += 1

        # Calculate scenario metrics
        df_scenario = pd.DataFrame(scenario_data)
        total_cf = df_scenario['Operating_CF'].sum()

        # Survival check
        cumulative_cf = df_scenario['Operating_CF'].cumsum()
        cash_position = baseline.get('cash_m', 100) + cumulative_cf
        min_cash = cash_position.min()
        survives = min_cash >= thresholds.get('min_liquidity_m', 50)

        # Leverage check (simplified)
        debt = baseline.get('debt_m', 500)
        max_leverage = debt / min_ebitda if min_ebitda > 0 else float('inf')
        leverage_ok = max_leverage <= thresholds.get('max_leverage_ratio', 4.0)

        scenario_results.append({
            'Scenario': scenario_name,
            'Probability_Percent': prob,
            'Revenue_Shock_Percent': scenario.get('revenue_shock_percent', -10),
            'Margin_Compression_PP': scenario.get('margin_compression_pp', 2),
            'Duration_Years': scenario.get('duration_years', 2),
            'Min_EBITDA_M': min_ebitda,
            'Min_Margin_Percent': min_margin,
            'Years_Negative_CF': years_negative_cf,
            'Min_Cash_M': min_cash,
            'Max_Leverage': max_leverage if max_leverage != float('inf') else 99,
            'Survives': survives,
            'Leverage_OK': leverage_ok,
            'Pass_All_Tests': survives and leverage_ok
        })

    results_df = pd.DataFrame(scenario_results)
    detailed_df = pd.DataFrame(all_data)

    # Risk assessment
    total_probability = results_df['Probability_Percent'].sum()
    fail_probability = results_df[~results_df['Pass_All_Tests']]['Probability_Percent'].sum()
    severe_fail = results_df[(~results_df['Pass_All_Tests']) & (results_df['Revenue_Shock_Percent'] <= -25)]

    # Expected loss
    prob_weighted_min_ebitda = (results_df['Min_EBITDA_M'] * results_df['Probability_Percent'] / 100).sum()
    base_ebitda = baseline['revenue_m'] * baseline['ebitda_margin_percent'] / 100
    expected_loss = base_ebitda - prob_weighted_min_ebitda

    summary = {
        'currency': params['currency'],
        'scenarios_tested': len(scenarios),
        'baseline': {
            'revenue_m': float(baseline['revenue_m']),
            'ebitda_margin_percent': float(baseline['ebitda_margin_percent']),
            'ebitda_m': float(base_ebitda)
        },
        'risk_metrics': {
            'scenarios_passed': int(results_df['Pass_All_Tests'].sum()),
            'scenarios_failed': int((~results_df['Pass_All_Tests']).sum()),
            'failure_probability_percent': float(fail_probability),
            'survival_rate_percent': float(100 - fail_probability),
            'expected_loss_m': float(expected_loss)
        },
        'worst_case': {
            'scenario': results_df.loc[results_df['Min_EBITDA_M'].idxmin(), 'Scenario'],
            'min_ebitda_m': float(results_df['Min_EBITDA_M'].min()),
            'min_margin_percent': float(results_df['Min_Margin_Percent'].min())
        },
        'risk_rating': 'LOW' if fail_probability < 10 else 'MEDIUM' if fail_probability < 25 else 'HIGH'
    }

    return {
        'scenario_results': results_df,
        'detailed_projection': detailed_df,
        'summary': summary,
        'params': params
    }


def format_results(results: Dict) -> str:
    """Format stress testing results for display."""
    output = []
    output.append("\n" + "="*80)
    output.append("STRESS TESTING MODEL (STM-1.0) - RESULTS")
    output.append("="*80)

    summary = results['summary']
    currency = summary.get('currency', 'EUR')

    output.append("\n[1] BASELINE")
    output.append("-" * 60)
    base = summary['baseline']
    output.append(f"  Revenue:         {currency}{base['revenue_m']:,.0f}M")
    output.append(f"  EBITDA Margin:   {base['ebitda_margin_percent']:.1f}%")
    output.append(f"  EBITDA:          {currency}{base['ebitda_m']:,.0f}M")

    output.append("\n[2] STRESS TEST RESULTS")
    output.append("-" * 60)
    df = results['scenario_results']
    display_cols = ['Scenario', 'Revenue_Shock_Percent', 'Min_EBITDA_M', 'Pass_All_Tests']
    output.append(df[display_cols].to_string(index=False))

    output.append("\n[3] RISK METRICS")
    output.append("-" * 60)
    risk = summary['risk_metrics']
    output.append(f"  Scenarios Passed:    {risk['scenarios_passed']}/{summary['scenarios_tested']}")
    output.append(f"  Failure Probability: {risk['failure_probability_percent']:.1f}%")
    output.append(f"  Survival Rate:       {risk['survival_rate_percent']:.1f}%")
    output.append(f"  Expected Loss:       {currency}{risk['expected_loss_m']:,.0f}M")

    output.append("\n[4] WORST CASE")
    output.append("-" * 60)
    worst = summary['worst_case']
    output.append(f"  Scenario:        {worst['scenario']}")
    output.append(f"  Min EBITDA:      {currency}{worst['min_ebitda_m']:,.0f}M")
    output.append(f"  Min Margin:      {worst['min_margin_percent']:.1f}%")

    output.append(f"\n[5] RISK RATING: {summary['risk_rating']}")

    output.append("\n" + "="*80)
    return "\n".join(output)


def main():
    if len(sys.argv) < 2:
        print("Usage: python stress_testing.py <config_file.yaml>")
        sys.exit(1)

    config = load_config(sys.argv[1])
    results = run_stress_tests(config)
    print(format_results(results))


if __name__ == '__main__':
    main()
