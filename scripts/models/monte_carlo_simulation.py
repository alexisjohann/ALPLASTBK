#!/usr/bin/env python3
"""
Monte Carlo Simulation Model (MCSM-1.0)
Stochastic validation of revenue projections across uncertainty.

Usage:
    from monte_carlo_simulation import run_monte_carlo
    results = run_monte_carlo(config, revenue_df, num_simulations=10000)

Model Version: 1.0.0
Implementation Date: 2026-01-15
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from scipy import stats
import yaml
import sys
from pathlib import Path


# Default regional distribution parameters
DEFAULT_REGIONAL_PARAMS = {
    'europe': {
        'base_cagr': 2.5,
        'std_dev_percent': 15,
        'min_cagr': 0.5,
        'max_cagr': 5.0
    },
    'asia_pacific': {
        'base_cagr': 8.5,
        'std_dev_percent': 20,
        'min_cagr': 3.0,
        'max_cagr': 14.0
    },
    'south_america': {
        'base_cagr': 6.5,
        'std_dev_percent': 18,
        'min_cagr': 2.0,
        'max_cagr': 12.0
    },
    'north_america': {
        'base_cagr': 4.5,
        'std_dev_percent': 16,
        'min_cagr': 1.0,
        'max_cagr': 8.0
    },
    'africa_middle_east': {
        'base_cagr': 8.0,
        'std_dev_percent': 22,
        'min_cagr': 1.0,
        'max_cagr': 16.0
    }
}

# Default correlation matrix (Europe, APAC, SA, NA, AMET)
DEFAULT_CORRELATION_MATRIX = np.array([
    [1.00, 0.45, 0.60, 0.70, 0.20],
    [0.45, 1.00, 0.50, 0.40, 0.65],
    [0.60, 0.50, 1.00, 0.55, 0.40],
    [0.70, 0.40, 0.55, 1.00, 0.30],
    [0.20, 0.65, 0.40, 0.30, 1.00]
])


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


def extract_regional_params(config: Dict) -> Dict:
    """
    Extract regional CAGR parameters from configuration.

    Args:
        config: Configuration dictionary

    Returns:
        Dictionary with regional parameters
    """
    regional_params = {}

    assumptions = config.get('strategic_assumptions', {})
    regional_growth = assumptions.get('regional_growth_rates', {}).get('period_2024_2035_cagr_percent', {})

    # Map config keys to standard keys
    key_mapping = {
        'europe': 'europe',
        'asia_pacific': 'asia_pacific',
        'south_america': 'south_america',
        'north_america': 'north_america',
        'africa_middle_east': 'africa_middle_east'
    }

    for config_key, standard_key in key_mapping.items():
        if config_key in regional_growth:
            data = regional_growth[config_key]
            if isinstance(data, dict):
                regional_params[standard_key] = {
                    'base_cagr': data.get('cagr', DEFAULT_REGIONAL_PARAMS.get(standard_key, {}).get('base_cagr', 5.0)),
                    'base_revenue': data.get('revenue_2024_eur_m', 1000),
                    'std_dev_percent': DEFAULT_REGIONAL_PARAMS.get(standard_key, {}).get('std_dev_percent', 15),
                    'min_cagr': DEFAULT_REGIONAL_PARAMS.get(standard_key, {}).get('min_cagr', 0),
                    'max_cagr': DEFAULT_REGIONAL_PARAMS.get(standard_key, {}).get('max_cagr', 15)
                }
        elif standard_key in DEFAULT_REGIONAL_PARAMS:
            regional_params[standard_key] = DEFAULT_REGIONAL_PARAMS[standard_key].copy()
            regional_params[standard_key]['base_revenue'] = 1000  # Default

    return regional_params


def generate_correlated_cagrs(
    regional_params: Dict,
    correlation_matrix: np.ndarray,
    num_simulations: int,
    random_seed: Optional[int] = 42
) -> pd.DataFrame:
    """
    Generate correlated random CAGR samples using Cholesky decomposition.

    Args:
        regional_params: Dictionary with regional CAGR parameters
        correlation_matrix: Correlation matrix between regions
        num_simulations: Number of Monte Carlo simulations
        random_seed: Random seed for reproducibility

    Returns:
        DataFrame with simulated CAGRs for each region
    """
    if random_seed is not None:
        np.random.seed(random_seed)

    regions = list(regional_params.keys())
    n_regions = len(regions)

    # Ensure correlation matrix matches number of regions
    if correlation_matrix.shape[0] != n_regions:
        # Use identity matrix if mismatch
        correlation_matrix = np.eye(n_regions)

    # Cholesky decomposition for correlated samples
    try:
        cholesky = np.linalg.cholesky(correlation_matrix)
    except np.linalg.LinAlgError:
        # If matrix not positive definite, use identity
        cholesky = np.eye(n_regions)

    # Generate uncorrelated standard normal samples
    uncorrelated = np.random.standard_normal((num_simulations, n_regions))

    # Apply correlation structure
    correlated = uncorrelated @ cholesky.T

    # Transform to actual CAGR distributions
    cagr_samples = {}
    for i, region in enumerate(regions):
        params = regional_params[region]
        base = params['base_cagr']
        std_pct = params.get('std_dev_percent', 15)
        min_cagr = params.get('min_cagr', base - 3)
        max_cagr = params.get('max_cagr', base + 5)

        # Convert std_dev_percent to absolute
        std_dev = base * std_pct / 100

        # Generate samples centered on base case
        samples = base + correlated[:, i] * std_dev

        # Clip to bounds
        samples = np.clip(samples, min_cagr, max_cagr)

        cagr_samples[region] = samples

    return pd.DataFrame(cagr_samples)


def simulate_revenue(
    base_revenues: Dict[str, float],
    cagr_samples: pd.DataFrame,
    projection_years: int = 11
) -> np.ndarray:
    """
    Simulate total revenue for each Monte Carlo run.

    Args:
        base_revenues: Base year (2024) revenue by region
        cagr_samples: DataFrame with CAGR samples for each region
        projection_years: Number of years to project (default: 11 for 2024-2035)

    Returns:
        Array of simulated 2035 revenues
    """
    num_simulations = len(cagr_samples)
    total_revenues_2035 = np.zeros(num_simulations)

    for region in cagr_samples.columns:
        if region in base_revenues:
            base_rev = base_revenues[region]
            cagrs = cagr_samples[region].values / 100  # Convert % to decimal

            # Revenue in 2035 = Base * (1 + CAGR)^11
            regional_rev_2035 = base_rev * np.power(1 + cagrs, projection_years)
            total_revenues_2035 += regional_rev_2035

    return total_revenues_2035


def calculate_percentiles(revenues: np.ndarray) -> Dict[str, float]:
    """
    Calculate percentile distribution from simulated revenues.

    Args:
        revenues: Array of simulated revenues

    Returns:
        Dictionary with percentile values
    """
    percentiles = {
        'p1': np.percentile(revenues, 1),
        'p5': np.percentile(revenues, 5),
        'p10': np.percentile(revenues, 10),
        'p25': np.percentile(revenues, 25),
        'p50': np.percentile(revenues, 50),
        'p75': np.percentile(revenues, 75),
        'p90': np.percentile(revenues, 90),
        'p95': np.percentile(revenues, 95),
        'p99': np.percentile(revenues, 99)
    }
    return percentiles


def calculate_probability_metrics(
    revenues: np.ndarray,
    base_case: float,
    conservative: Optional[float] = None,
    optimistic: Optional[float] = None
) -> Dict[str, float]:
    """
    Calculate probability metrics from simulated revenues.

    Args:
        revenues: Array of simulated revenues
        base_case: Base case revenue target
        conservative: Conservative scenario target (optional)
        optimistic: Optimistic scenario target (optional)

    Returns:
        Dictionary with probability metrics
    """
    n = len(revenues)

    metrics = {
        'prob_exceeds_base_case': np.sum(revenues >= base_case) / n,
        'prob_below_base_case': np.sum(revenues < base_case) / n,
    }

    if conservative is not None:
        metrics['prob_exceeds_conservative'] = np.sum(revenues >= conservative) / n
        metrics['prob_below_conservative'] = np.sum(revenues < conservative) / n

    if optimistic is not None:
        metrics['prob_exceeds_optimistic'] = np.sum(revenues >= optimistic) / n

    # Additional thresholds
    metrics['prob_exceeds_10b'] = np.sum(revenues >= 10000) / n
    metrics['prob_below_8b'] = np.sum(revenues < 8000) / n

    return metrics


def calculate_sensitivity(
    regional_params: Dict,
    base_revenues: Dict[str, float],
    perturbation_pp: float = 1.0
) -> Dict[str, float]:
    """
    Calculate regional sensitivity (elasticity per 1pp CAGR change).

    Args:
        regional_params: Regional CAGR parameters
        base_revenues: Base year revenues by region
        perturbation_pp: Perturbation in percentage points

    Returns:
        Dictionary with sensitivity per region
    """
    sensitivity = {}

    for region, params in regional_params.items():
        if region in base_revenues:
            base_rev = base_revenues[region]
            base_cagr = params['base_cagr'] / 100

            # Revenue change for +1pp CAGR change
            rev_base = base_rev * np.power(1 + base_cagr, 11)
            rev_up = base_rev * np.power(1 + base_cagr + perturbation_pp/100, 11)

            sensitivity[region] = (rev_up - rev_base)

    return sensitivity


def run_monte_carlo(
    config: Dict,
    revenue_df: Optional[pd.DataFrame] = None,
    num_simulations: int = 10000,
    confidence_level: float = 0.95,
    random_seed: int = 42
) -> Dict:
    """
    Main function: Run Monte Carlo simulation for revenue projections.

    Args:
        config: Configuration dictionary (from YAML)
        revenue_df: Optional DataFrame with base revenue projections
        num_simulations: Number of Monte Carlo simulations (default: 10,000)
        confidence_level: Confidence level for intervals (default: 95%)
        random_seed: Random seed for reproducibility

    Returns:
        Dictionary with simulation results:
        - percentiles: Percentile distribution
        - statistics: Summary statistics (mean, std, etc.)
        - probabilities: Probability metrics
        - sensitivity: Regional sensitivity analysis
        - simulations: Raw simulation results (optional)
    """

    # Extract regional parameters
    regional_params = extract_regional_params(config)

    # Extract base revenues
    base_revenues = {}
    for region, params in regional_params.items():
        base_revenues[region] = params.get('base_revenue', 1000)

    # If revenue_df provided, update base revenues from it
    if revenue_df is not None and 'Year' in revenue_df.columns:
        base_row = revenue_df[revenue_df['Year'] == 2024]
        if not base_row.empty:
            for col in revenue_df.columns:
                if col not in ['Year', 'Total', 'YoY%']:
                    # Map column name to regional key
                    key_map = {
                        'europe': 'europe',
                        'asia_pacific': 'asia_pacific',
                        'south_america': 'south_america',
                        'north_america': 'north_america',
                        'africa_middle_east': 'africa_middle_east'
                    }
                    for key, standard_key in key_map.items():
                        if key in col.lower().replace(' ', '_').replace('-', '_'):
                            base_revenues[standard_key] = base_row[col].values[0]

    # Calculate base case total
    base_case_total = sum(base_revenues.values())

    # Determine correlation matrix size
    n_regions = len(regional_params)
    if n_regions <= 5:
        correlation_matrix = DEFAULT_CORRELATION_MATRIX[:n_regions, :n_regions]
    else:
        correlation_matrix = np.eye(n_regions)

    # Generate correlated CAGR samples
    cagr_samples = generate_correlated_cagrs(
        regional_params,
        correlation_matrix,
        num_simulations,
        random_seed
    )

    # Simulate revenues
    simulated_revenues = simulate_revenue(
        base_revenues,
        cagr_samples,
        projection_years=11
    )

    # Calculate percentiles
    percentiles = calculate_percentiles(simulated_revenues)

    # Calculate statistics
    statistics = {
        'mean': np.mean(simulated_revenues),
        'median': np.median(simulated_revenues),
        'std_dev': np.std(simulated_revenues),
        'coefficient_of_variation': np.std(simulated_revenues) / np.mean(simulated_revenues),
        'min': np.min(simulated_revenues),
        'max': np.max(simulated_revenues),
        'confidence_interval_lower': percentiles[f'p{int((1-confidence_level)*100/2)}'] if f'p{int((1-confidence_level)*100/2)}' in percentiles else percentiles['p5'],
        'confidence_interval_upper': percentiles[f'p{int(100 - (1-confidence_level)*100/2)}'] if f'p{int(100 - (1-confidence_level)*100/2)}' in percentiles else percentiles['p95'],
    }

    # Calculate scenario targets (Base ± 15%)
    conservative_target = statistics['mean'] * 0.88  # ~5th percentile
    optimistic_target = statistics['mean'] * 1.12   # ~95th percentile

    # Calculate probabilities
    probabilities = calculate_probability_metrics(
        simulated_revenues,
        base_case=statistics['mean'],
        conservative=conservative_target,
        optimistic=optimistic_target
    )

    # Calculate sensitivity
    sensitivity = calculate_sensitivity(
        regional_params,
        base_revenues,
        perturbation_pp=1.0
    )

    return {
        'percentiles': percentiles,
        'statistics': statistics,
        'probabilities': probabilities,
        'sensitivity': sensitivity,
        'num_simulations': num_simulations,
        'confidence_level': confidence_level,
        'base_revenues': base_revenues,
        'regional_params': regional_params,
        'simulations': simulated_revenues  # Raw data for plotting
    }


def format_results(results: Dict) -> str:
    """
    Format Monte Carlo results for display.

    Args:
        results: Results dictionary from run_monte_carlo

    Returns:
        Formatted string
    """
    output = []
    output.append("\n" + "="*80)
    output.append("MONTE CARLO SIMULATION MODEL (MCSM-1.0) - RESULTS")
    output.append("="*80)

    output.append(f"\nSimulations: {results['num_simulations']:,}")
    output.append(f"Confidence Level: {results['confidence_level']*100:.0f}%")

    output.append("\n[1] PERCENTILE DISTRIBUTION (2035 Revenue)")
    output.append("-" * 60)
    for p, v in results['percentiles'].items():
        label = p.replace('p', '').rjust(3) + '%'
        output.append(f"  {label}: €{v:,.0f}M")

    output.append("\n[2] SUMMARY STATISTICS")
    output.append("-" * 60)
    stats = results['statistics']
    output.append(f"  Mean:      €{stats['mean']:,.0f}M")
    output.append(f"  Median:    €{stats['median']:,.0f}M")
    output.append(f"  Std Dev:   €{stats['std_dev']:,.0f}M")
    output.append(f"  CV:        {stats['coefficient_of_variation']:.3f}")
    output.append(f"  95% CI:    [€{stats['confidence_interval_lower']:,.0f}M - €{stats['confidence_interval_upper']:,.0f}M]")

    output.append("\n[3] PROBABILITY METRICS")
    output.append("-" * 60)
    probs = results['probabilities']
    output.append(f"  P(≥ Base Case):     {probs['prob_exceeds_base_case']*100:.1f}%")
    output.append(f"  P(≥ Conservative):  {probs.get('prob_exceeds_conservative', 0)*100:.1f}%")
    output.append(f"  P(≥ €10B):          {probs['prob_exceeds_10b']*100:.1f}%")
    output.append(f"  P(< €8B):           {probs['prob_below_8b']*100:.1f}%")

    output.append("\n[4] REGIONAL SENSITIVITY (per 1pp CAGR change)")
    output.append("-" * 60)
    for region, impact in results['sensitivity'].items():
        output.append(f"  {region.replace('_', ' ').title()}: €{impact:,.0f}M")

    output.append("\n" + "="*80)
    return "\n".join(output)


def main():
    """Main entry point for command-line execution."""
    if len(sys.argv) < 2:
        print("Usage: python monte_carlo_simulation.py <config_file.yaml> [num_simulations]")
        sys.exit(1)

    config_file = sys.argv[1]
    num_simulations = int(sys.argv[2]) if len(sys.argv) > 2 else 10000

    print(f"Loading configuration: {config_file}")
    config = load_configuration(config_file)

    print(f"Running Monte Carlo simulation ({num_simulations:,} simulations)...")
    results = run_monte_carlo(config, num_simulations=num_simulations)

    print(format_results(results))


if __name__ == '__main__':
    main()
