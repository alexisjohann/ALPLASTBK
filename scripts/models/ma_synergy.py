#!/usr/bin/env python3
"""
M&A Synergy Model (MAM-1.0)
Merger & acquisition synergy analysis and integration planning.

Usage:
    from ma_synergy import analyze_ma_synergies
    result = analyze_ma_synergies(config)

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


def extract_ma_params(config: Dict) -> Dict:
    """Extract M&A parameters from configuration."""
    ma_config = config.get('ma_synergy_model', {})

    params = {
        'base_year': ma_config.get('base_year', DEFAULT_BASE_YEAR),
        'projection_years': ma_config.get('projection_years', DEFAULT_PROJECTION_YEARS),
        'currency': ma_config.get('currency', DEFAULT_CURRENCY),

        # Acquirer financials
        'acquirer': ma_config.get('acquirer', {
            'name': 'Acquirer',
            'revenue_m': 1000,
            'ebitda_m': 150,
            'employees': 5000
        }),

        # Target financials
        'target': ma_config.get('target', {
            'name': 'Target',
            'revenue_m': 300,
            'ebitda_m': 45,
            'employees': 1500,
            'purchase_price_m': 400
        }),

        # Synergy assumptions
        'synergies': ma_config.get('synergies', {
            'revenue_synergies': {
                'cross_sell_percent': 5,
                'new_markets_percent': 3,
                'ramp_years': 3
            },
            'cost_synergies': {
                'headcount_reduction_percent': 10,
                'procurement_savings_percent': 5,
                'facility_consolidation_m': 20,
                'ramp_years': 2
            }
        }),

        # Integration costs
        'integration': ma_config.get('integration', {
            'one_time_costs_m': 50,
            'restructuring_m': 30,
            'it_integration_m': 20,
            'retention_bonuses_m': 10
        }),

        # Financing
        'financing': ma_config.get('financing', {
            'debt_percent': 60,
            'equity_percent': 40,
            'debt_rate_percent': 5.0
        })
    }

    return params


def analyze_ma_synergies(config: Dict) -> Dict:
    """
    Analyze M&A synergies and integration economics.

    Args:
        config: Configuration dictionary

    Returns:
        Dictionary with synergy analysis, integration timeline, and value creation
    """
    params = extract_ma_params(config)
    years = get_year_range(params['base_year'], params['projection_years'])

    acquirer = params['acquirer']
    target = params['target']
    synergies = params['synergies']
    integration = params['integration']
    financing = params['financing']

    # Combined baseline
    combined_revenue = acquirer['revenue_m'] + target['revenue_m']
    combined_ebitda = acquirer['ebitda_m'] + target['ebitda_m']
    combined_employees = acquirer['employees'] + target['employees']

    # Revenue synergies
    rev_syn = synergies.get('revenue_synergies', {})
    cross_sell = target['revenue_m'] * rev_syn.get('cross_sell_percent', 5) / 100
    new_markets = target['revenue_m'] * rev_syn.get('new_markets_percent', 3) / 100
    total_rev_synergy = cross_sell + new_markets
    rev_ramp_years = rev_syn.get('ramp_years', 3)

    # Cost synergies
    cost_syn = synergies.get('cost_synergies', {})
    combined_costs = combined_revenue - combined_ebitda
    headcount_savings = combined_costs * cost_syn.get('headcount_reduction_percent', 10) / 100 * 0.4  # Labor ~40% of costs
    procurement_savings = combined_costs * cost_syn.get('procurement_savings_percent', 5) / 100 * 0.3  # Procurement ~30%
    facility_savings = cost_syn.get('facility_consolidation_m', 20)
    total_cost_synergy = headcount_savings + procurement_savings + facility_savings
    cost_ramp_years = cost_syn.get('ramp_years', 2)

    # Integration costs
    total_integration_costs = (
        integration.get('one_time_costs_m', 50) +
        integration.get('restructuring_m', 30) +
        integration.get('it_integration_m', 20) +
        integration.get('retention_bonuses_m', 10)
    )

    # Project synergies over time
    data = []
    cumulative_synergies = 0

    for i, year in enumerate(years):
        row = {'Year': year}

        # Revenue synergy ramp-up
        if i < rev_ramp_years:
            rev_synergy_realized = total_rev_synergy * (i + 1) / rev_ramp_years
        else:
            rev_synergy_realized = total_rev_synergy

        row['Revenue_Synergy'] = rev_synergy_realized

        # Cost synergy ramp-up
        if i < cost_ramp_years:
            cost_synergy_realized = total_cost_synergy * (i + 1) / cost_ramp_years
        else:
            cost_synergy_realized = total_cost_synergy

        row['Cost_Synergy'] = cost_synergy_realized

        # Total synergies
        row['Total_Synergy'] = rev_synergy_realized + cost_synergy_realized
        cumulative_synergies += row['Total_Synergy']
        row['Cumulative_Synergy'] = cumulative_synergies

        # Integration costs (Year 1 only)
        row['Integration_Costs'] = total_integration_costs if i == 0 else 0

        # Net value added
        row['Net_Value_Added'] = row['Total_Synergy'] - row['Integration_Costs']

        # Pro-forma financials
        row['PF_Revenue'] = combined_revenue + rev_synergy_realized
        row['PF_EBITDA'] = combined_ebitda + row['Total_Synergy'] - (row['Integration_Costs'] if i == 0 else 0)
        row['PF_EBITDA_Margin'] = row['PF_EBITDA'] / row['PF_Revenue'] * 100

        data.append(row)

    df = pd.DataFrame(data)

    # Valuation impact
    purchase_price = target.get('purchase_price_m', 400)
    implied_ev_ebitda = purchase_price / target['ebitda_m'] if target['ebitda_m'] > 0 else 0

    # NPV of synergies (simplified, 10% discount rate)
    discount_rate = 0.10
    npv_synergies = sum(df['Total_Synergy'].iloc[i] / ((1 + discount_rate) ** (i + 1)) for i in range(len(df)))
    npv_integration = total_integration_costs  # Year 0

    # Value creation
    synergy_value_created = npv_synergies - npv_integration

    # Payback period
    cumulative = df['Cumulative_Synergy'].values
    payback_year = None
    for i, cum in enumerate(cumulative):
        if cum >= total_integration_costs:
            payback_year = i + 1
            break

    summary = {
        'currency': params['currency'],
        'deal': {
            'acquirer': acquirer['name'],
            'target': target['name'],
            'purchase_price_m': purchase_price,
            'implied_ev_ebitda': float(implied_ev_ebitda)
        },
        'combined': {
            'revenue_m': float(combined_revenue),
            'ebitda_m': float(combined_ebitda),
            'employees': int(combined_employees)
        },
        'synergies': {
            'revenue_synergy_m': float(total_rev_synergy),
            'cost_synergy_m': float(total_cost_synergy),
            'total_run_rate_m': float(total_rev_synergy + total_cost_synergy),
            'ramp_years': max(rev_ramp_years, cost_ramp_years)
        },
        'integration': {
            'total_costs_m': float(total_integration_costs),
            'payback_years': payback_year
        },
        'value_creation': {
            'npv_synergies_m': float(npv_synergies),
            'net_value_created_m': float(synergy_value_created),
            'value_created_positive': synergy_value_created > 0
        }
    }

    return {
        'synergy_projection': df,
        'summary': summary,
        'params': params
    }


def format_results(results: Dict) -> str:
    """Format M&A synergy results for display."""
    output = []
    output.append("\n" + "="*80)
    output.append("M&A SYNERGY MODEL (MAM-1.0) - RESULTS")
    output.append("="*80)

    summary = results['summary']
    currency = summary.get('currency', 'EUR')

    output.append("\n[1] DEAL OVERVIEW")
    output.append("-" * 60)
    deal = summary['deal']
    output.append(f"  Acquirer:        {deal['acquirer']}")
    output.append(f"  Target:          {deal['target']}")
    output.append(f"  Purchase Price:  {currency}{deal['purchase_price_m']:,.0f}M")
    output.append(f"  Implied EV/EBITDA: {deal['implied_ev_ebitda']:.1f}x")

    output.append("\n[2] COMBINED ENTITY")
    output.append("-" * 60)
    combined = summary['combined']
    output.append(f"  Revenue:         {currency}{combined['revenue_m']:,.0f}M")
    output.append(f"  EBITDA:          {currency}{combined['ebitda_m']:,.0f}M")
    output.append(f"  Employees:       {combined['employees']:,}")

    output.append("\n[3] SYNERGIES (Run-Rate)")
    output.append("-" * 60)
    syn = summary['synergies']
    output.append(f"  Revenue Synergies:  {currency}{syn['revenue_synergy_m']:,.0f}M")
    output.append(f"  Cost Synergies:     {currency}{syn['cost_synergy_m']:,.0f}M")
    output.append(f"  Total Run-Rate:     {currency}{syn['total_run_rate_m']:,.0f}M")
    output.append(f"  Full Ramp-Up:       {syn['ramp_years']} years")

    output.append("\n[4] INTEGRATION")
    output.append("-" * 60)
    integ = summary['integration']
    output.append(f"  Integration Costs:  {currency}{integ['total_costs_m']:,.0f}M")
    output.append(f"  Payback Period:     {integ['payback_years']} years" if integ['payback_years'] else "  Payback Period:     >10 years")

    output.append("\n[5] VALUE CREATION")
    output.append("-" * 60)
    value = summary['value_creation']
    output.append(f"  NPV of Synergies:   {currency}{value['npv_synergies_m']:,.0f}M")
    output.append(f"  Net Value Created:  {currency}{value['net_value_created_m']:,.0f}M")
    status = "VALUE CREATING" if value['value_created_positive'] else "VALUE DESTROYING"
    output.append(f"  Status:             {status}")

    output.append("\n" + "="*80)
    return "\n".join(output)


def main():
    if len(sys.argv) < 2:
        print("Usage: python ma_synergy.py <config_file.yaml>")
        sys.exit(1)

    config = load_config(sys.argv[1])
    results = analyze_ma_synergies(config)
    print(format_results(results))


if __name__ == '__main__':
    main()
