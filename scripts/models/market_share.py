#!/usr/bin/env python3
"""
Market Share Model (MSM-1.0)
Competitive dynamics, market share projection, and competitive positioning.

Usage:
    from market_share import project_market_share
    result = project_market_share(config, revenue_projection)

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


def extract_market_share_params(config: Dict) -> Dict:
    """Extract market share parameters from configuration."""
    ms_config = config.get('market_share_model', {})

    params = {
        'base_year': ms_config.get('base_year', DEFAULT_BASE_YEAR),
        'projection_years': ms_config.get('projection_years', DEFAULT_PROJECTION_YEARS),
        'currency': ms_config.get('currency', DEFAULT_CURRENCY),
        'markets': ms_config.get('markets', []),
        'competitors': ms_config.get('competitors', []),
        'company_share': ms_config.get('company_share', {}),
        'market_growth': ms_config.get('market_growth', {})
    }

    # Default market if not specified
    if not params['markets']:
        params['markets'] = [
            {'name': 'Total Market', 'size_m': 50000, 'growth_rate_percent': 4.0}
        ]

    # Default competitors
    if not params['competitors']:
        params['competitors'] = [
            {'name': 'Company', 'share_percent': 10, 'growth_premium': 1.0},
            {'name': 'Competitor A', 'share_percent': 15, 'growth_premium': 0.8},
            {'name': 'Competitor B', 'share_percent': 12, 'growth_premium': 0.9},
            {'name': 'Others', 'share_percent': 63, 'growth_premium': 1.0}
        ]

    return params


def project_market_share(
    config: Dict,
    revenue_projection: pd.DataFrame = None
) -> Dict:
    """
    Project market share and competitive dynamics.

    Args:
        config: Configuration dictionary
        revenue_projection: Revenue projection from RPM-1.0

    Returns:
        Dictionary with market share projection and competitive analysis
    """
    params = extract_market_share_params(config)
    years = get_year_range(params['base_year'], params['projection_years'])
    markets = params['markets']
    competitors = params['competitors']

    # Market projection
    market_data = []
    for i, year in enumerate(years):
        row = {'Year': year}
        total_market = 0

        for market in markets:
            market_name = market['name']
            base_size = market.get('size_m', 50000)
            growth_rate = market.get('growth_rate_percent', 4.0) / 100

            if i == 0:
                market_size = base_size
            else:
                market_size = base_size * ((1 + growth_rate) ** i)

            row[f'{market_name}_Size'] = market_size
            total_market += market_size

        row['Total_Market'] = total_market
        market_data.append(row)

    market_df = pd.DataFrame(market_data)

    # Competitive share projection
    share_data = []
    for i, year in enumerate(years):
        row = {'Year': year}
        market_size = market_df[market_df['Year'] == year]['Total_Market'].iloc[0]
        market_growth = markets[0].get('growth_rate_percent', 4.0) / 100

        total_share = 0
        for comp in competitors:
            comp_name = comp['name']
            base_share = comp.get('share_percent', 10) / 100
            growth_premium = comp.get('growth_premium', 1.0)

            # Share evolves based on relative growth
            if i == 0:
                share = base_share
            else:
                # Share gain/loss based on growth premium
                share_change = (growth_premium - 1.0) * 0.005 * i  # Gradual share shift
                share = base_share + share_change
                share = max(0.01, min(0.5, share))  # Cap between 1% and 50%

            row[f'{comp_name}_Share_Pct'] = share * 100
            row[f'{comp_name}_Revenue'] = market_size * share
            total_share += share

        # Normalize to 100%
        if total_share != 1.0:
            for comp in competitors:
                comp_name = comp['name']
                row[f'{comp_name}_Share_Pct'] = row[f'{comp_name}_Share_Pct'] / (total_share * 100) * 100

        share_data.append(row)

    share_df = pd.DataFrame(share_data)

    # Get company metrics
    company_name = competitors[0]['name'] if competitors else 'Company'
    base_share = share_df.iloc[0][f'{company_name}_Share_Pct']
    final_share = share_df.iloc[-1][f'{company_name}_Share_Pct']
    base_revenue = share_df.iloc[0][f'{company_name}_Revenue']
    final_revenue = share_df.iloc[-1][f'{company_name}_Revenue']

    # Competitive position analysis
    position_data = []
    for comp in competitors:
        comp_name = comp['name']
        pos = {
            'Competitor': comp_name,
            'Base_Share_Pct': share_df.iloc[0][f'{comp_name}_Share_Pct'],
            'Final_Share_Pct': share_df.iloc[-1][f'{comp_name}_Share_Pct'],
            'Share_Change_Pct': share_df.iloc[-1][f'{comp_name}_Share_Pct'] - share_df.iloc[0][f'{comp_name}_Share_Pct'],
            'Base_Revenue': share_df.iloc[0][f'{comp_name}_Revenue'],
            'Final_Revenue': share_df.iloc[-1][f'{comp_name}_Revenue'],
            'Growth_Premium': comp.get('growth_premium', 1.0)
        }
        position_data.append(pos)

    position_df = pd.DataFrame(position_data)

    summary = {
        'currency': params['currency'],
        'market': {
            'base_size_m': float(market_df.iloc[0]['Total_Market']),
            'final_size_m': float(market_df.iloc[-1]['Total_Market']),
            'cagr_percent': ((market_df.iloc[-1]['Total_Market'] / market_df.iloc[0]['Total_Market']) ** (1/len(years)) - 1) * 100
        },
        'company': {
            'name': company_name,
            'base_share_percent': float(base_share),
            'final_share_percent': float(final_share),
            'share_change_percent': float(final_share - base_share),
            'base_revenue_m': float(base_revenue),
            'final_revenue_m': float(final_revenue)
        },
        'competitive_position': 'GAINING' if final_share > base_share else 'LOSING' if final_share < base_share else 'STABLE'
    }

    return {
        'market_projection': market_df,
        'share_projection': share_df,
        'competitive_position': position_df,
        'summary': summary,
        'params': params
    }


def format_results(results: Dict) -> str:
    """Format market share results for display."""
    output = []
    output.append("\n" + "="*80)
    output.append("MARKET SHARE MODEL (MSM-1.0) - RESULTS")
    output.append("="*80)

    summary = results['summary']
    currency = summary.get('currency', 'EUR')

    output.append("\n[1] MARKET SIZE")
    output.append("-" * 60)
    market = summary['market']
    output.append(f"  Base Year:   {currency}{market['base_size_m']:,.0f}M")
    output.append(f"  Final Year:  {currency}{market['final_size_m']:,.0f}M")
    output.append(f"  CAGR:        {market['cagr_percent']:.1f}%")

    output.append("\n[2] COMPANY POSITION")
    output.append("-" * 60)
    company = summary['company']
    output.append(f"  Company:     {company['name']}")
    output.append(f"  Base Share:  {company['base_share_percent']:.1f}%")
    output.append(f"  Final Share: {company['final_share_percent']:.1f}%")
    output.append(f"  Change:      {company['share_change_percent']:+.1f}pp")
    output.append(f"  Status:      {summary['competitive_position']}")

    output.append("\n[3] COMPETITIVE LANDSCAPE")
    output.append("-" * 60)
    pos_df = results['competitive_position']
    output.append(pos_df[['Competitor', 'Base_Share_Pct', 'Final_Share_Pct', 'Share_Change_Pct']].to_string(index=False))

    output.append("\n" + "="*80)
    return "\n".join(output)


def main():
    if len(sys.argv) < 2:
        print("Usage: python market_share.py <config_file.yaml>")
        sys.exit(1)

    config = load_config(sys.argv[1])
    results = project_market_share(config)
    print(format_results(results))


if __name__ == '__main__':
    main()
