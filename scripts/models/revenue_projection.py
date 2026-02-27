#!/usr/bin/env python3
"""
Revenue Projection Model - Parametric Implementation
Reusable across customers with parameter substitution.

Usage:
    config = load_yaml('alpla_assumptions.yaml')
    df = project_revenue(config)

Model Version: 1.0.0
Implementation Date: 2026-01-15
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import yaml
import sys
from pathlib import Path


def load_configuration(config_path: str) -> Dict:
    """
    Load model configuration from YAML file.

    Args:
        config_path: Path to YAML configuration file

    Returns:
        Dictionary with model parameters

    Raises:
        FileNotFoundError: If config file not found
        yaml.YAMLError: If YAML parsing fails
    """
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


def validate_parameters(config: Dict) -> Tuple[bool, List[str]]:
    """
    Validate model parameters against business rules.

    Args:
        config: Configuration dictionary

    Returns:
        Tuple of (is_valid: bool, error_messages: List[str])
    """
    errors = []

    # Extract assumptions section
    assumptions = config.get('strategic_assumptions', {})
    regional_cagr = assumptions.get('regional_growth_rates', {}).get('period_2024_2035_cagr_percent', {})
    regional_allocation = assumptions.get('regional_growth_rates', {}).get('period_2024_2035_cagr_percent', {})

    # Validation rule 1: Regional CAGR within reasonable bounds
    for region, data in regional_cagr.items():
        if isinstance(data, dict):
            cagr = data.get('cagr', 0)
            if cagr < -5 or cagr > 20:
                errors.append(f"Region {region}: CAGR {cagr}% outside reasonable bounds [-5%, 20%]")

    # Validation rule 2: All regions have CAGR defined
    if not regional_cagr:
        errors.append("ERROR: No regional CAGR data found in assumptions")

    return len(errors) == 0, errors


def initialize_regional_data(config: Dict) -> Dict[str, Dict]:
    """
    Initialize regional revenue data from base year.

    Args:
        config: Configuration dictionary

    Returns:
        Dictionary with regional base revenues
    """
    assumptions = config.get('strategic_assumptions', {})
    regional_growth = assumptions.get('regional_growth_rates', {}).get('period_2024_2035_cagr_percent', {})

    base_revenue_eur_m = 4900  # Default: ALPLA base case

    # Extract from config if available
    if 'alpla_profile' in config:
        profile = config['alpla_profile']
        if 'financial_2024' in profile:
            base_revenue_eur_m = profile['financial_2024'].get('revenue_eur_m', 4900)

    regional_data = {}

    for region, data in regional_growth.items():
        if isinstance(data, dict) and 'revenue_2024_eur_m' in data:
            regional_data[region] = {
                'base_revenue': data['revenue_2024_eur_m'],
                'cagr': data.get('cagr', 0) / 100.0,  # Convert % to decimal
                'revenue_2035': data.get('revenue_2035_eur_m', 0),
            }

    return regional_data


def project_region_revenue(
    base_revenue: float,
    cagr: float,
    years: np.ndarray
) -> np.ndarray:
    """
    Project revenue for single region using CAGR formula.

    Formula: Revenue(t) = Revenue(t0) * (1 + CAGR)^(t - t0)

    Args:
        base_revenue: Base year revenue (2024)
        cagr: Compound annual growth rate (as decimal, e.g., 0.069 for 6.9%)
        years: Array of years to project [2024, 2025, ..., 2035]

    Returns:
        Array of projected revenues
    """
    years_from_base = years - 2024
    projected_revenue = base_revenue * np.power(1 + cagr, years_from_base)
    return projected_revenue


def project_revenue(config: Dict) -> pd.DataFrame:
    """
    Main function: Project company revenue 2024-2035 by region.

    Args:
        config: Model configuration dictionary (from YAML)

    Returns:
        DataFrame with columns: Year, Region1, Region2, ..., Total, YoY%

    Example:
        >>> config = load_yaml('alpla_assumptions.yaml')
        >>> df = project_revenue(config)
        >>> print(df)
    """

    # Validate configuration
    is_valid, errors = validate_parameters(config)
    if not is_valid:
        print("Configuration validation failed:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)

    # Initialize
    years = np.arange(2024, 2036)  # 2024-2035 inclusive
    regional_data = initialize_regional_data(config)

    # Project each region
    projections = {}
    for region, data in regional_data.items():
        base = data['base_revenue']
        cagr = data['cagr']
        projections[region] = project_region_revenue(base, cagr, years)

    # Create DataFrame
    df = pd.DataFrame({'Year': years})

    for region, revenues in projections.items():
        df[region] = revenues

    # Calculate total
    revenue_columns = list(projections.keys())
    df['Total'] = df[revenue_columns].sum(axis=1)

    # Calculate YoY growth %
    df['YoY%'] = df['Total'].pct_change() * 100

    return df


def calculate_summary_metrics(df: pd.DataFrame) -> Dict:
    """
    Calculate summary metrics from revenue projection.

    Args:
        df: Revenue projection DataFrame

    Returns:
        Dictionary with summary metrics
    """
    metrics = {
        'base_year_2024_revenue_eur_m': df[df['Year'] == 2024]['Total'].values[0],
        'target_year_2035_revenue_eur_m': df[df['Year'] == 2035]['Total'].values[0],
        'absolute_growth_eur_m': df[df['Year'] == 2035]['Total'].values[0] - df[df['Year'] == 2024]['Total'].values[0],
        'growth_percent': ((df[df['Year'] == 2035]['Total'].values[0] / df[df['Year'] == 2024]['Total'].values[0]) - 1) * 100,
    }

    # Calculate blended CAGR
    r_2024 = metrics['base_year_2024_revenue_eur_m']
    r_2035 = metrics['target_year_2035_revenue_eur_m']
    cagr_blended = (pow(r_2035 / r_2024, 1/11) - 1) * 100
    metrics['blended_cagr_percent'] = cagr_blended

    return metrics


def sensitivity_analysis(config: Dict, perturbation_pct: float = 1.0) -> pd.DataFrame:
    """
    Sensitivity analysis: Impact of ±{perturbation_pct} change in regional CAGRs.

    Args:
        config: Model configuration
        perturbation_pct: Percentage point change to test (default: 1.0pp)

    Returns:
        DataFrame with sensitivity results
    """
    # Base case
    df_base = project_revenue(config)
    base_2035 = df_base[df_base['Year'] == 2035]['Total'].values[0]

    sensitivity_results = []

    # Test each region
    assumptions = config.get('strategic_assumptions', {})
    regional_growth = assumptions.get('regional_growth_rates', {}).get('period_2024_2035_cagr_percent', {})

    for region in regional_growth.keys():
        # Decrease CAGR
        config_down = yaml.safe_load(yaml.dump(config))  # Deep copy
        if 'strategic_assumptions' in config_down:
            if 'regional_growth_rates' in config_down['strategic_assumptions']:
                if 'period_2024_2035_cagr_percent' in config_down['strategic_assumptions']['regional_growth_rates']:
                    if region in config_down['strategic_assumptions']['regional_growth_rates']['period_2024_2035_cagr_percent']:
                        cagr_down = config_down['strategic_assumptions']['regional_growth_rates']['period_2024_2035_cagr_percent'][region].get('cagr', 0)
                        config_down['strategic_assumptions']['regional_growth_rates']['period_2024_2035_cagr_percent'][region]['cagr'] = cagr_down - perturbation_pct

        df_down = project_revenue(config_down)
        revenue_down = df_down[df_down['Year'] == 2035]['Total'].values[0]

        # Increase CAGR
        config_up = yaml.safe_load(yaml.dump(config))  # Deep copy
        if 'strategic_assumptions' in config_up:
            if 'regional_growth_rates' in config_up['strategic_assumptions']:
                if 'period_2024_2035_cagr_percent' in config_up['strategic_assumptions']['regional_growth_rates']:
                    if region in config_up['strategic_assumptions']['regional_growth_rates']['period_2024_2035_cagr_percent']:
                        cagr_up = config_up['strategic_assumptions']['regional_growth_rates']['period_2024_2035_cagr_percent'][region].get('cagr', 0)
                        config_up['strategic_assumptions']['regional_growth_rates']['period_2024_2035_cagr_percent'][region]['cagr'] = cagr_up + perturbation_pct

        df_up = project_revenue(config_up)
        revenue_up = df_up[df_up['Year'] == 2035]['Total'].values[0]

        sensitivity_results.append({
            'region': region,
            'cagr_change_pp': f"-{perturbation_pct}pp to +{perturbation_pct}pp",
            'revenue_down_eur_m': revenue_down,
            'revenue_base_eur_m': base_2035,
            'revenue_up_eur_m': revenue_up,
            'impact_range_eur_m': revenue_up - revenue_down,
            'elasticity_per_1pp': (revenue_up - revenue_down) / (2 * perturbation_pct),
        })

    df_sensitivity = pd.DataFrame(sensitivity_results)
    return df_sensitivity


def format_output(df: pd.DataFrame, metrics: Dict) -> str:
    """
    Format output for display.

    Args:
        df: Projection DataFrame
        metrics: Summary metrics dictionary

    Returns:
        Formatted string for display
    """
    output = []
    output.append("\n" + "="*80)
    output.append("REVENUE PROJECTION MODEL - RESULTS")
    output.append("="*80)

    output.append("\n[1] ANNUAL REVENUE PROJECTION (2024-2035)")
    output.append("-" * 80)
    output.append(df.to_string(index=False))

    output.append("\n[2] SUMMARY METRICS")
    output.append("-" * 80)
    output.append(f"  Base Year (2024) Revenue:    €{metrics['base_year_2024_revenue_eur_m']:,.0f}M")
    output.append(f"  Target Year (2035) Revenue: €{metrics['target_year_2035_revenue_eur_m']:,.0f}M")
    output.append(f"  Absolute Growth:            €{metrics['absolute_growth_eur_m']:,.0f}M")
    output.append(f"  Growth %:                   {metrics['growth_percent']:.1f}%")
    output.append(f"  Blended CAGR (2024-2035):   {metrics['blended_cagr_percent']:.2f}%")

    output.append("\n" + "="*80)
    return "\n".join(output)


def main():
    """
    Main entry point for command-line execution.

    Usage:
        python revenue_projection.py alpla_assumptions.yaml
    """
    if len(sys.argv) < 2:
        print("Usage: python revenue_projection.py <config_file.yaml> [output_file.csv]")
        sys.exit(1)

    config_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    print(f"Loading configuration: {config_file}")
    config = load_configuration(config_file)

    print("Running revenue projection model...")
    df = project_revenue(config)

    metrics = calculate_summary_metrics(df)

    print(format_output(df, metrics))

    # Sensitivity analysis
    print("\n[3] SENSITIVITY ANALYSIS (±1pp CAGR change)")
    print("-" * 80)
    df_sensitivity = sensitivity_analysis(config, perturbation_pct=1.0)
    print(df_sensitivity.to_string(index=False))

    # Optional: Save to CSV
    if output_file:
        df.to_csv(output_file, index=False)
        print(f"\nResults saved to: {output_file}")


if __name__ == '__main__':
    main()
