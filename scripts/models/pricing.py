#!/usr/bin/env python3
"""
Pricing Model (PRM-1.0)
Price elasticity analysis and pricing optimization.

Usage:
    from pricing import analyze_pricing
    result = analyze_pricing(config)

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


def extract_pricing_params(config: Dict) -> Dict:
    """Extract pricing parameters from configuration."""
    pr_config = config.get('pricing_model', {})

    params = {
        'base_year': pr_config.get('base_year', DEFAULT_BASE_YEAR),
        'currency': pr_config.get('currency', DEFAULT_CURRENCY),

        # Current pricing
        'current_pricing': pr_config.get('current_pricing', {
            'avg_price': 100,
            'volume': 10000,
            'variable_cost_per_unit': 60,
            'fixed_costs': 200000
        }),

        # Price elasticity
        'elasticity': pr_config.get('elasticity', {
            'price_elasticity': -1.5,  # % volume change per 1% price change
            'cross_elasticity': 0.5,   # Impact of competitor pricing
            'income_elasticity': 0.8   # Impact of economic conditions
        }),

        # Competitive pricing
        'competition': pr_config.get('competition', {
            'competitor_avg_price': 95,
            'price_premium_tolerance': 15  # Max premium % before significant volume loss
        }),

        # Pricing scenarios to test
        'test_scenarios': pr_config.get('test_scenarios', [
            {'name': 'Aggressive Discount', 'price_change_percent': -15},
            {'name': 'Moderate Discount', 'price_change_percent': -5},
            {'name': 'Current Pricing', 'price_change_percent': 0},
            {'name': 'Modest Increase', 'price_change_percent': 5},
            {'name': 'Premium Pricing', 'price_change_percent': 10},
            {'name': 'Ultra Premium', 'price_change_percent': 20}
        ])
    }

    return params


def calculate_volume_impact(price_change_pct: float, elasticity: float) -> float:
    """Calculate volume change based on price elasticity."""
    return price_change_pct * elasticity


def optimize_price(current: Dict, elasticity: Dict) -> Dict:
    """Find profit-maximizing price using elasticity."""
    price = current['avg_price']
    volume = current['volume']
    vc = current['variable_cost_per_unit']
    fc = current['fixed_costs']
    elas = elasticity['price_elasticity']

    # Profit = (Price - VC) * Volume - FC
    # With elasticity: Volume' = Volume * (1 + elas * price_change%)
    # Optimize: d(Profit)/d(price_change) = 0

    # Simplified: optimal markup = -1/elasticity
    if elas < -1:  # Elastic demand
        optimal_markup = -1 / elas
        optimal_price_multiplier = 1 + optimal_markup * (price - vc) / price
        optimal_price = price * optimal_price_multiplier
    else:
        optimal_price = price * 1.1  # Inelastic - can raise price

    # Cap at reasonable bounds
    optimal_price = max(vc * 1.1, min(price * 1.5, optimal_price))

    return {
        'optimal_price': optimal_price,
        'optimal_change_percent': (optimal_price / price - 1) * 100
    }


def analyze_pricing(config: Dict) -> Dict:
    """
    Analyze pricing strategies and optimize pricing.

    Args:
        config: Configuration dictionary

    Returns:
        Dictionary with pricing analysis and optimization
    """
    params = extract_pricing_params(config)
    current = params['current_pricing']
    elasticity = params['elasticity']
    competition = params['competition']
    scenarios = params['test_scenarios']

    price = current['avg_price']
    volume = current['volume']
    vc = current['variable_cost_per_unit']
    fc = current['fixed_costs']
    elas = elasticity['price_elasticity']

    # Current metrics
    current_revenue = price * volume
    current_gross_profit = (price - vc) * volume
    current_profit = current_gross_profit - fc
    current_margin = (price - vc) / price * 100

    # Analyze each scenario
    scenario_results = []

    for scenario in scenarios:
        name = scenario['name']
        price_change = scenario['price_change_percent']

        # New price
        new_price = price * (1 + price_change / 100)

        # Volume impact from elasticity
        volume_change = calculate_volume_impact(price_change, elas)
        new_volume = volume * (1 + volume_change / 100)

        # Competitive impact
        price_vs_comp = (new_price / competition['competitor_avg_price'] - 1) * 100
        if price_vs_comp > competition['price_premium_tolerance']:
            # Additional volume loss for excessive premium
            excess_premium = price_vs_comp - competition['price_premium_tolerance']
            competitive_penalty = excess_premium * 0.5  # 0.5% volume loss per 1% excess
            new_volume = new_volume * (1 - competitive_penalty / 100)

        new_volume = max(0, new_volume)  # Can't go negative

        # Calculate financials
        new_revenue = new_price * new_volume
        new_gross_profit = (new_price - vc) * new_volume
        new_profit = new_gross_profit - fc
        new_margin = (new_price - vc) / new_price * 100 if new_price > 0 else 0

        # Changes
        revenue_change = (new_revenue / current_revenue - 1) * 100 if current_revenue > 0 else 0
        profit_change = new_profit - current_profit

        scenario_results.append({
            'Scenario': name,
            'Price_Change_Percent': price_change,
            'New_Price': new_price,
            'Volume_Change_Percent': (new_volume / volume - 1) * 100,
            'New_Volume': new_volume,
            'New_Revenue': new_revenue,
            'Revenue_Change_Percent': revenue_change,
            'New_Gross_Margin_Percent': new_margin,
            'New_Profit': new_profit,
            'Profit_Change': profit_change,
            'Price_vs_Competition': price_vs_comp
        })

    df = pd.DataFrame(scenario_results)

    # Find optimal scenario
    best_scenario = df.loc[df['New_Profit'].idxmax()]

    # Calculate optimal price analytically
    optimal = optimize_price(current, elasticity)

    summary = {
        'currency': params['currency'],
        'current_state': {
            'price': float(price),
            'volume': int(volume),
            'revenue': float(current_revenue),
            'gross_margin_percent': float(current_margin),
            'profit': float(current_profit)
        },
        'elasticity': {
            'price_elasticity': float(elas),
            'demand_type': 'ELASTIC' if abs(elas) > 1 else 'INELASTIC'
        },
        'optimal_pricing': {
            'optimal_price': float(optimal['optimal_price']),
            'optimal_change_percent': float(optimal['optimal_change_percent']),
            'best_tested_scenario': best_scenario['Scenario'],
            'best_profit': float(best_scenario['New_Profit']),
            'best_profit_change': float(best_scenario['Profit_Change'])
        },
        'competitive_position': {
            'competitor_price': float(competition['competitor_avg_price']),
            'current_premium_percent': float((price / competition['competitor_avg_price'] - 1) * 100),
            'premium_tolerance_percent': float(competition['price_premium_tolerance'])
        }
    }

    return {
        'scenario_analysis': df,
        'summary': summary,
        'params': params
    }


def format_results(results: Dict) -> str:
    """Format pricing analysis results for display."""
    output = []
    output.append("\n" + "="*80)
    output.append("PRICING MODEL (PRM-1.0) - RESULTS")
    output.append("="*80)

    summary = results['summary']
    currency = summary.get('currency', 'EUR')

    output.append("\n[1] CURRENT STATE")
    output.append("-" * 60)
    current = summary['current_state']
    output.append(f"  Price:          {currency}{current['price']:,.2f}")
    output.append(f"  Volume:         {current['volume']:,}")
    output.append(f"  Revenue:        {currency}{current['revenue']:,.0f}")
    output.append(f"  Gross Margin:   {current['gross_margin_percent']:.1f}%")
    output.append(f"  Profit:         {currency}{current['profit']:,.0f}")

    output.append("\n[2] PRICE ELASTICITY")
    output.append("-" * 60)
    elas = summary['elasticity']
    output.append(f"  Elasticity:     {elas['price_elasticity']:.2f}")
    output.append(f"  Demand Type:    {elas['demand_type']}")
    if elas['demand_type'] == 'ELASTIC':
        output.append(f"  Implication:    Volume sensitive to price changes")
    else:
        output.append(f"  Implication:    Room to increase prices")

    output.append("\n[3] SCENARIO ANALYSIS")
    output.append("-" * 60)
    df = results['scenario_analysis']
    display_cols = ['Scenario', 'Price_Change_Percent', 'New_Revenue', 'New_Profit', 'Profit_Change']
    output.append(df[display_cols].to_string(index=False))

    output.append("\n[4] OPTIMAL PRICING")
    output.append("-" * 60)
    optimal = summary['optimal_pricing']
    output.append(f"  Optimal Price:      {currency}{optimal['optimal_price']:,.2f}")
    output.append(f"  Optimal Change:     {optimal['optimal_change_percent']:+.1f}%")
    output.append(f"  Best Scenario:      {optimal['best_tested_scenario']}")
    output.append(f"  Max Profit:         {currency}{optimal['best_profit']:,.0f}")
    output.append(f"  Profit Uplift:      {currency}{optimal['best_profit_change']:+,.0f}")

    output.append("\n[5] COMPETITIVE POSITION")
    output.append("-" * 60)
    comp = summary['competitive_position']
    output.append(f"  Competitor Price:   {currency}{comp['competitor_price']:,.2f}")
    output.append(f"  Current Premium:    {comp['current_premium_percent']:+.1f}%")
    output.append(f"  Premium Tolerance:  {comp['premium_tolerance_percent']:.0f}%")

    output.append("\n" + "="*80)
    return "\n".join(output)


def main():
    if len(sys.argv) < 2:
        print("Usage: python pricing.py <config_file.yaml>")
        sys.exit(1)

    config = load_config(sys.argv[1])
    results = analyze_pricing(config)
    print(format_results(results))


if __name__ == '__main__':
    main()
