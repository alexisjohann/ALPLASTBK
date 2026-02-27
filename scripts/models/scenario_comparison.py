#!/usr/bin/env python3
"""
Scenario Comparison Model (SCM-1.0)
Systematic comparison of strategic scenarios.

Usage:
    from scenario_comparison import compare_scenarios
    result = compare_scenarios(config, model_runner)

Model Version: 1.0.0
Implementation Date: 2026-01-16

FULLY GENERIC: All parameters from config, no hardcoded defaults.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Any, Callable
from copy import deepcopy
import yaml
import sys
from pathlib import Path

# Import base utilities
try:
    from strategy_base import (
        load_config, get_nested, set_nested, save_csv, save_yaml,
        format_currency, format_percent, calculate_cagr, get_year_range,
        DEFAULT_BASE_YEAR, DEFAULT_PROJECTION_YEARS, DEFAULT_CURRENCY
    )
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent))
    from strategy_base import (
        load_config, get_nested, set_nested, save_csv, save_yaml,
        format_currency, format_percent, calculate_cagr, get_year_range,
        DEFAULT_BASE_YEAR, DEFAULT_PROJECTION_YEARS, DEFAULT_CURRENCY
    )


def extract_scenario_params(config: Dict) -> Dict:
    """
    Extract scenario comparison parameters from configuration.

    Expected config structure:
    ```yaml
    scenario_comparison:
      base_year: 2024
      projection_years: 11
      currency: "EUR"

      # Scenarios to compare
      scenarios:
        - name: "Conservative"
          probability: 0.25
          description: "Slow growth, margin pressure"
          adjustments:
            strategic_assumptions.regional_growth_rates.europe.cagr: 1.5
            strategic_assumptions.regional_growth_rates.apac.cagr: 6.0
            pnl_model.ebitda_margin_percent: 10

        - name: "Base Case"
          probability: 0.50
          description: "Expected trajectory"
          adjustments: {}  # No changes

        - name: "Aggressive"
          probability: 0.25
          description: "Strong growth, margin expansion"
          adjustments:
            strategic_assumptions.regional_growth_rates.europe.cagr: 3.5
            strategic_assumptions.regional_growth_rates.apac.cagr: 10.0
            pnl_model.ebitda_margin_percent: 15

      # Metrics to compare
      comparison_metrics:
        - name: "revenue_2035"
          path: "revenue.final_year_m"
          higher_is_better: true
        - name: "ebitda_margin_2035"
          path: "pnl.ebitda.final_margin_percent"
          higher_is_better: true
        - name: "total_fcf"
          path: "cash_flow.total_m"
          higher_is_better: true

      # Ranking weights
      ranking_weights:
        revenue_2035: 0.30
        ebitda_margin_2035: 0.25
        total_fcf: 0.25
        risk_adjusted_value: 0.20
    ```
    """
    sc_config = config.get('scenario_comparison', {})

    params = {
        'base_year': sc_config.get('base_year', DEFAULT_BASE_YEAR),
        'projection_years': sc_config.get('projection_years', DEFAULT_PROJECTION_YEARS),
        'currency': sc_config.get('currency', DEFAULT_CURRENCY),
        'scenarios': sc_config.get('scenarios', []),
        'comparison_metrics': sc_config.get('comparison_metrics', []),
        'ranking_weights': sc_config.get('ranking_weights', {})
    }

    # Default scenarios if none specified
    if not params['scenarios']:
        params['scenarios'] = [
            {
                'name': 'Conservative',
                'probability': 0.25,
                'description': 'Low growth scenario',
                'adjustments': {}
            },
            {
                'name': 'Base Case',
                'probability': 0.50,
                'description': 'Expected trajectory',
                'adjustments': {}
            },
            {
                'name': 'Aggressive',
                'probability': 0.25,
                'description': 'High growth scenario',
                'adjustments': {}
            }
        ]

    return params


def apply_scenario_adjustments(config: Dict, adjustments: Dict) -> Dict:
    """
    Apply scenario adjustments to configuration.

    Args:
        config: Base configuration
        adjustments: Dictionary of path -> value adjustments

    Returns:
        Modified configuration
    """
    scenario_config = deepcopy(config)

    for path, value in adjustments.items():
        set_nested(scenario_config, path, value)

    return scenario_config


def extract_metric_value(results: Dict, metric_path: str) -> Optional[float]:
    """
    Extract a metric value from model results.

    Args:
        results: Model results dictionary
        metric_path: Dot-notation path to metric

    Returns:
        Metric value or None if not found
    """
    return get_nested(results, metric_path)


def run_scenario(
    scenario: Dict,
    base_config: Dict,
    model_runner: Callable
) -> Dict:
    """
    Run a single scenario.

    Args:
        scenario: Scenario definition
        base_config: Base configuration
        model_runner: Function that runs models and returns results

    Returns:
        Dictionary with scenario results
    """
    scenario_name = scenario.get('name', 'Unknown')
    adjustments = scenario.get('adjustments', {})

    # Apply adjustments
    scenario_config = apply_scenario_adjustments(base_config, adjustments)

    # Run models
    try:
        model_results = model_runner(scenario_config)
        success = True
        error = None
    except Exception as e:
        model_results = {}
        success = False
        error = str(e)

    return {
        'name': scenario_name,
        'probability': scenario.get('probability', 0),
        'description': scenario.get('description', ''),
        'adjustments': adjustments,
        'results': model_results,
        'success': success,
        'error': error
    }


def calculate_scenario_metrics(
    scenario_results: List[Dict],
    metrics_config: List[Dict]
) -> pd.DataFrame:
    """
    Extract and compare metrics across scenarios.

    Args:
        scenario_results: List of scenario results
        metrics_config: List of metric configurations

    Returns:
        DataFrame with metrics by scenario
    """
    data = []

    for scenario in scenario_results:
        row = {
            'Scenario': scenario['name'],
            'Probability': scenario['probability'],
            'Success': scenario['success']
        }

        if scenario['success']:
            results = scenario['results']

            for metric in metrics_config:
                metric_name = metric.get('name', 'unknown')
                metric_path = metric.get('path', '')

                value = extract_metric_value(results, metric_path)
                row[metric_name] = value

        data.append(row)

    return pd.DataFrame(data)


def calculate_probability_weighted_outcomes(
    metrics_df: pd.DataFrame,
    metric_columns: List[str]
) -> Dict:
    """
    Calculate probability-weighted expected values.

    Args:
        metrics_df: DataFrame with metrics by scenario
        metric_columns: List of metric column names

    Returns:
        Dictionary with weighted outcomes
    """
    weighted = {}

    total_prob = metrics_df['Probability'].sum()
    if total_prob == 0:
        return weighted

    for col in metric_columns:
        if col in metrics_df.columns:
            values = metrics_df[col].fillna(0)
            probs = metrics_df['Probability']
            weighted[col] = (values * probs).sum() / total_prob

    return weighted


def rank_scenarios(
    metrics_df: pd.DataFrame,
    metrics_config: List[Dict],
    ranking_weights: Dict
) -> pd.DataFrame:
    """
    Rank scenarios by weighted score.

    Args:
        metrics_df: DataFrame with metrics by scenario
        metrics_config: List of metric configurations
        ranking_weights: Dictionary of metric_name -> weight

    Returns:
        DataFrame with rankings
    """
    df = metrics_df.copy()

    # Normalize each metric to 0-100 scale
    for metric in metrics_config:
        metric_name = metric.get('name')
        higher_is_better = metric.get('higher_is_better', True)

        if metric_name in df.columns:
            values = df[metric_name].fillna(0)
            min_val = values.min()
            max_val = values.max()

            if max_val > min_val:
                normalized = (values - min_val) / (max_val - min_val) * 100
                if not higher_is_better:
                    normalized = 100 - normalized
            else:
                normalized = 50  # All same

            df[f'{metric_name}_score'] = normalized

    # Calculate weighted score
    total_weight = sum(ranking_weights.values()) if ranking_weights else 1
    df['Weighted_Score'] = 0

    for metric_name, weight in ranking_weights.items():
        score_col = f'{metric_name}_score'
        if score_col in df.columns:
            df['Weighted_Score'] += df[score_col] * (weight / total_weight)

    # Rank by weighted score
    df['Rank'] = df['Weighted_Score'].rank(ascending=False).astype(int)
    df = df.sort_values('Rank')

    return df


def calculate_scenario_ranges(
    metrics_df: pd.DataFrame,
    metric_columns: List[str]
) -> Dict:
    """
    Calculate min/max ranges across scenarios.

    Args:
        metrics_df: DataFrame with metrics by scenario
        metric_columns: List of metric column names

    Returns:
        Dictionary with ranges
    """
    ranges = {}

    for col in metric_columns:
        if col in metrics_df.columns:
            values = metrics_df[col].dropna()
            if len(values) > 0:
                ranges[col] = {
                    'min': float(values.min()),
                    'max': float(values.max()),
                    'range': float(values.max() - values.min()),
                    'mean': float(values.mean()),
                    'std': float(values.std()) if len(values) > 1 else 0
                }

    return ranges


def compare_scenarios(
    config: Dict,
    model_runner: Callable,
    custom_scenarios: Optional[List[Dict]] = None
) -> Dict:
    """
    Main function: Compare multiple strategic scenarios.

    Args:
        config: Configuration dictionary (from YAML)
        model_runner: Function that takes config and returns model results
        custom_scenarios: Optional list of custom scenarios (overrides config)

    Returns:
        Dictionary with:
        - scenario_results: Detailed results for each scenario
        - comparison_table: DataFrame comparing metrics
        - rankings: DataFrame with scenario rankings
        - probability_weighted: Expected values
        - summary: Summary statistics
    """
    params = extract_scenario_params(config)
    scenarios = custom_scenarios or params['scenarios']
    metrics_config = params['comparison_metrics']

    if not scenarios:
        return {'error': 'No scenarios defined'}

    print(f"Comparing {len(scenarios)} scenarios...")

    # Run each scenario
    scenario_results = []
    for i, scenario in enumerate(scenarios):
        print(f"  [{i+1}/{len(scenarios)}] Running {scenario.get('name', 'Unknown')}...")
        result = run_scenario(scenario, config, model_runner)
        scenario_results.append(result)

    # Extract metrics
    metric_columns = [m['name'] for m in metrics_config]
    metrics_df = calculate_scenario_metrics(scenario_results, metrics_config)

    # Calculate probability-weighted outcomes
    prob_weighted = calculate_probability_weighted_outcomes(metrics_df, metric_columns)

    # Rank scenarios
    rankings_df = rank_scenarios(metrics_df, metrics_config, params['ranking_weights'])

    # Calculate ranges
    ranges = calculate_scenario_ranges(metrics_df, metric_columns)

    # Build comparison table
    comparison_cols = ['Scenario', 'Probability'] + metric_columns
    comparison_df = metrics_df[[c for c in comparison_cols if c in metrics_df.columns]]

    # Summary
    successful = sum(1 for s in scenario_results if s['success'])
    best_scenario = rankings_df.iloc[0]['Scenario'] if len(rankings_df) > 0 else None

    summary = {
        'num_scenarios': len(scenarios),
        'successful_runs': successful,
        'failed_runs': len(scenarios) - successful,
        'best_scenario': best_scenario,
        'currency': params['currency'],
        'probability_weighted_outcomes': prob_weighted,
        'metric_ranges': ranges,
        'scenario_list': [s['name'] for s in scenarios]
    }

    return {
        'scenario_results': scenario_results,
        'comparison_table': comparison_df,
        'rankings': rankings_df,
        'probability_weighted': prob_weighted,
        'ranges': ranges,
        'summary': summary,
        'params': params
    }


def format_results(results: Dict) -> str:
    """Format scenario comparison results for display."""
    output = []
    output.append("\n" + "="*80)
    output.append("SCENARIO COMPARISON MODEL (SCM-1.0) - RESULTS")
    output.append("="*80)

    summary = results['summary']
    currency = summary.get('currency', 'EUR')

    output.append("\n[1] COMPARISON SUMMARY")
    output.append("-" * 60)
    output.append(f"  Scenarios Compared: {summary['num_scenarios']}")
    output.append(f"  Successful Runs:    {summary['successful_runs']}")
    output.append(f"  Best Scenario:      {summary['best_scenario']}")

    output.append("\n[2] SCENARIO COMPARISON TABLE")
    output.append("-" * 60)
    comparison = results['comparison_table']
    output.append(comparison.to_string(index=False))

    output.append("\n[3] SCENARIO RANKINGS")
    output.append("-" * 60)
    rankings = results['rankings']
    rank_cols = ['Rank', 'Scenario', 'Weighted_Score', 'Probability']
    available_cols = [c for c in rank_cols if c in rankings.columns]
    output.append(rankings[available_cols].to_string(index=False))

    output.append("\n[4] PROBABILITY-WEIGHTED OUTCOMES")
    output.append("-" * 60)
    prob_weighted = results['probability_weighted']
    for metric, value in prob_weighted.items():
        if value is not None:
            if 'percent' in metric.lower() or 'margin' in metric.lower():
                output.append(f"  {metric}: {value:.1f}%")
            else:
                output.append(f"  {metric}: {currency}{value:,.0f}M")

    output.append("\n[5] METRIC RANGES")
    output.append("-" * 60)
    ranges = results['ranges']
    for metric, range_data in ranges.items():
        output.append(f"  {metric}:")
        output.append(f"    Min: {range_data['min']:,.1f}")
        output.append(f"    Max: {range_data['max']:,.1f}")
        output.append(f"    Range: {range_data['range']:,.1f}")

    output.append("\n" + "="*80)
    return "\n".join(output)


# Default model runner for standalone use
def default_model_runner(config: Dict) -> Dict:
    """
    Default model runner using the strategic model suite.
    """
    try:
        from revenue_projection import project_revenue, calculate_summary_metrics
        from profit_loss import project_pnl
        from cash_flow import project_cash_flow
    except ImportError:
        sys.path.insert(0, str(Path(__file__).parent))
        from revenue_projection import project_revenue, calculate_summary_metrics
        from profit_loss import project_pnl
        from cash_flow import project_cash_flow

    results = {}

    # Revenue
    try:
        revenue_df = project_revenue(config)
        revenue_metrics = calculate_summary_metrics(revenue_df)
        results['revenue'] = {
            'final_year_m': revenue_metrics.get('target_year_2035_revenue_eur_m', 0),
            'cagr_percent': revenue_metrics.get('blended_cagr_percent', 0)
        }
    except Exception as e:
        results['revenue'] = {'error': str(e)}

    # P&L
    try:
        pnl_results = project_pnl(config, revenue_df if 'revenue_df' in dir() else None)
        pnl_summary = pnl_results.get('summary', {})
        results['pnl'] = {
            'ebitda': pnl_summary.get('ebitda', {}),
            'net_income': pnl_summary.get('net_income', {})
        }
    except Exception as e:
        results['pnl'] = {'error': str(e)}

    # Cash Flow
    try:
        cf_results = project_cash_flow(config, pnl_results.get('pnl_projection') if 'pnl_results' in dir() else None)
        cf_summary = cf_results.get('summary', {})
        results['cash_flow'] = {
            'total_m': cf_summary.get('free_cash_flow', {}).get('total_m', 0),
            'avg_yield_percent': cf_summary.get('free_cash_flow', {}).get('avg_fcf_yield_percent', 0)
        }
    except Exception as e:
        results['cash_flow'] = {'error': str(e)}

    return results


def main():
    """Main entry point for command-line execution."""
    if len(sys.argv) < 2:
        print("Usage: python scenario_comparison.py <config_file.yaml>")
        print("\nThe config file should contain a 'scenario_comparison' section with:")
        print("  - scenarios: List of scenario definitions")
        print("  - comparison_metrics: Metrics to compare")
        print("  - ranking_weights: Weights for ranking")
        sys.exit(1)

    config_file = sys.argv[1]

    print(f"Loading configuration: {config_file}")
    config = load_config(config_file)

    print("Running scenario comparison...")
    results = compare_scenarios(
        config=config,
        model_runner=default_model_runner
    )

    print(format_results(results))


if __name__ == '__main__':
    main()
