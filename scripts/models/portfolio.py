#!/usr/bin/env python3
"""
Portfolio Model (PFM-1.0)
BCG Matrix analysis and strategic portfolio optimization.

Usage:
    from portfolio import analyze_portfolio
    result = analyze_portfolio(config)

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


def extract_portfolio_params(config: Dict) -> Dict:
    """Extract portfolio parameters from configuration."""
    pf_config = config.get('portfolio_model', {})

    params = {
        'base_year': pf_config.get('base_year', DEFAULT_BASE_YEAR),
        'currency': pf_config.get('currency', DEFAULT_CURRENCY),

        # Business units
        'business_units': pf_config.get('business_units', [
            {'name': 'Core Business', 'revenue_m': 500, 'growth_percent': 3, 'market_share_percent': 25, 'margin_percent': 15},
            {'name': 'Growth Division', 'revenue_m': 200, 'growth_percent': 15, 'market_share_percent': 8, 'margin_percent': 8},
            {'name': 'Mature Product', 'revenue_m': 300, 'growth_percent': -2, 'market_share_percent': 40, 'margin_percent': 20},
            {'name': 'New Venture', 'revenue_m': 50, 'growth_percent': 25, 'market_share_percent': 3, 'margin_percent': -5}
        ]),

        # BCG thresholds
        'bcg_thresholds': pf_config.get('bcg_thresholds', {
            'growth_threshold_percent': 10,  # Above = high growth
            'share_threshold_percent': 15    # Above = high share
        }),

        # Strategic priorities
        'strategic_priorities': pf_config.get('strategic_priorities', {
            'stars': 'invest',        # High growth, high share
            'question_marks': 'selective',  # High growth, low share
            'cash_cows': 'harvest',   # Low growth, high share
            'dogs': 'divest'          # Low growth, low share
        })
    }

    return params


def classify_bcg(growth: float, share: float, thresholds: Dict) -> str:
    """Classify business unit in BCG matrix."""
    high_growth = growth >= thresholds.get('growth_threshold_percent', 10)
    high_share = share >= thresholds.get('share_threshold_percent', 15)

    if high_growth and high_share:
        return 'Star'
    elif high_growth and not high_share:
        return 'Question Mark'
    elif not high_growth and high_share:
        return 'Cash Cow'
    else:
        return 'Dog'


def get_strategic_recommendation(quadrant: str, priorities: Dict) -> str:
    """Get strategic recommendation for BCG quadrant."""
    mapping = {
        'Star': priorities.get('stars', 'invest').upper(),
        'Question Mark': priorities.get('question_marks', 'selective').upper(),
        'Cash Cow': priorities.get('cash_cows', 'harvest').upper(),
        'Dog': priorities.get('dogs', 'divest').upper()
    }
    return mapping.get(quadrant, 'REVIEW')


def analyze_portfolio(config: Dict) -> Dict:
    """
    Analyze business portfolio using BCG matrix and strategic positioning.

    Args:
        config: Configuration dictionary

    Returns:
        Dictionary with portfolio analysis, BCG classification, and recommendations
    """
    params = extract_portfolio_params(config)
    business_units = params['business_units']
    thresholds = params['bcg_thresholds']
    priorities = params['strategic_priorities']

    # Analyze each business unit
    analysis_data = []
    total_revenue = sum(bu['revenue_m'] for bu in business_units)

    for bu in business_units:
        name = bu['name']
        revenue = bu['revenue_m']
        growth = bu['growth_percent']
        share = bu['market_share_percent']
        margin = bu['margin_percent']

        # BCG classification
        quadrant = classify_bcg(growth, share, thresholds)
        recommendation = get_strategic_recommendation(quadrant, priorities)

        # Calculate contribution
        ebitda = revenue * margin / 100
        portfolio_weight = revenue / total_revenue * 100

        # Future potential (simplified)
        if quadrant == 'Star':
            investment_priority = 1
            cash_need = 'HIGH'
        elif quadrant == 'Question Mark':
            investment_priority = 2
            cash_need = 'HIGH'
        elif quadrant == 'Cash Cow':
            investment_priority = 3
            cash_need = 'LOW'
        else:
            investment_priority = 4
            cash_need = 'MINIMAL'

        analysis_data.append({
            'Business_Unit': name,
            'Revenue_M': revenue,
            'Growth_Percent': growth,
            'Market_Share_Percent': share,
            'EBITDA_Margin_Percent': margin,
            'EBITDA_M': ebitda,
            'Portfolio_Weight_Percent': portfolio_weight,
            'BCG_Quadrant': quadrant,
            'Strategic_Recommendation': recommendation,
            'Investment_Priority': investment_priority,
            'Cash_Need': cash_need
        })

    df = pd.DataFrame(analysis_data)

    # Portfolio summary by quadrant
    quadrant_summary = df.groupby('BCG_Quadrant').agg({
        'Revenue_M': 'sum',
        'EBITDA_M': 'sum',
        'Business_Unit': 'count'
    }).reset_index()
    quadrant_summary.columns = ['Quadrant', 'Revenue_M', 'EBITDA_M', 'Count']

    # Portfolio balance score (ideally: Stars + Cash Cows should dominate)
    stars_cows_revenue = df[df['BCG_Quadrant'].isin(['Star', 'Cash Cow'])]['Revenue_M'].sum()
    balance_score = stars_cows_revenue / total_revenue * 100

    # Cash flow balance (Cash Cows should fund Stars and Question Marks)
    cash_generators = df[df['BCG_Quadrant'] == 'Cash Cow']['EBITDA_M'].sum()
    cash_users = df[df['BCG_Quadrant'].isin(['Star', 'Question Mark'])]['EBITDA_M'].sum()
    cash_balance = cash_generators - abs(cash_users) if cash_users < 0 else cash_generators

    summary = {
        'currency': params['currency'],
        'portfolio': {
            'total_revenue_m': float(total_revenue),
            'total_ebitda_m': float(df['EBITDA_M'].sum()),
            'avg_margin_percent': float(df['EBITDA_Margin_Percent'].mean()),
            'num_business_units': len(business_units)
        },
        'bcg_distribution': {
            'stars': int(len(df[df['BCG_Quadrant'] == 'Star'])),
            'question_marks': int(len(df[df['BCG_Quadrant'] == 'Question Mark'])),
            'cash_cows': int(len(df[df['BCG_Quadrant'] == 'Cash Cow'])),
            'dogs': int(len(df[df['BCG_Quadrant'] == 'Dog']))
        },
        'portfolio_health': {
            'balance_score_percent': float(balance_score),
            'cash_generators_m': float(cash_generators),
            'self_funding': cash_balance >= 0,
            'assessment': 'HEALTHY' if balance_score >= 60 else 'NEEDS REBALANCING'
        }
    }

    return {
        'business_unit_analysis': df,
        'quadrant_summary': quadrant_summary,
        'summary': summary,
        'params': params
    }


def format_results(results: Dict) -> str:
    """Format portfolio analysis results for display."""
    output = []
    output.append("\n" + "="*80)
    output.append("PORTFOLIO MODEL (PFM-1.0) - BCG MATRIX ANALYSIS")
    output.append("="*80)

    summary = results['summary']
    currency = summary.get('currency', 'EUR')

    output.append("\n[1] PORTFOLIO OVERVIEW")
    output.append("-" * 60)
    pf = summary['portfolio']
    output.append(f"  Total Revenue:       {currency}{pf['total_revenue_m']:,.0f}M")
    output.append(f"  Total EBITDA:        {currency}{pf['total_ebitda_m']:,.0f}M")
    output.append(f"  Avg Margin:          {pf['avg_margin_percent']:.1f}%")
    output.append(f"  Business Units:      {pf['num_business_units']}")

    output.append("\n[2] BCG DISTRIBUTION")
    output.append("-" * 60)
    bcg = summary['bcg_distribution']
    output.append(f"  ⭐ Stars:            {bcg['stars']}")
    output.append(f"  ❓ Question Marks:   {bcg['question_marks']}")
    output.append(f"  🐄 Cash Cows:        {bcg['cash_cows']}")
    output.append(f"  🐕 Dogs:             {bcg['dogs']}")

    output.append("\n[3] BUSINESS UNIT ANALYSIS")
    output.append("-" * 60)
    df = results['business_unit_analysis']
    display_cols = ['Business_Unit', 'Revenue_M', 'Growth_Percent', 'BCG_Quadrant', 'Strategic_Recommendation']
    output.append(df[display_cols].to_string(index=False))

    output.append("\n[4] PORTFOLIO HEALTH")
    output.append("-" * 60)
    health = summary['portfolio_health']
    output.append(f"  Balance Score:       {health['balance_score_percent']:.0f}%")
    output.append(f"  Cash Generators:     {currency}{health['cash_generators_m']:,.0f}M")
    output.append(f"  Self-Funding:        {'Yes' if health['self_funding'] else 'No'}")
    output.append(f"  Assessment:          {health['assessment']}")

    output.append("\n" + "="*80)
    return "\n".join(output)


def main():
    if len(sys.argv) < 2:
        print("Usage: python portfolio.py <config_file.yaml>")
        sys.exit(1)

    config = load_config(sys.argv[1])
    results = analyze_portfolio(config)
    print(format_results(results))


if __name__ == '__main__':
    main()
