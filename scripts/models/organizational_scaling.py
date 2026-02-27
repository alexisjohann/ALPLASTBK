#!/usr/bin/env python3
"""
Organizational Scaling Model (OSM-1.0)
Workforce planning and organizational evolution projection.

Usage:
    from organizational_scaling import project_headcount, calculate_payroll
    result = project_headcount(config)
    payroll_df = result['payroll_projection']

Model Version: 1.0.0
Implementation Date: 2026-01-15
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
import yaml
import sys
from pathlib import Path


# Default function parameters
DEFAULT_FUNCTIONS = {
    'operations': {
        'name': 'Operations & Manufacturing',
        'base_headcount': 11000,
        'percentage': 45.2,
        'avg_cost_eur_k': 45,
        'escalation_rate': 3.0
    },
    'sales_customer_service': {
        'name': 'Sales & Customer Service',
        'base_headcount': 2500,
        'percentage': 10.3,
        'avg_cost_eur_k': 55,
        'escalation_rate': 3.5
    },
    'quality_compliance': {
        'name': 'Quality & Compliance',
        'base_headcount': 1200,
        'percentage': 4.9,
        'avg_cost_eur_k': 50,
        'escalation_rate': 3.0
    },
    'research_development': {
        'name': 'R&D & Innovation',
        'base_headcount': 850,
        'percentage': 3.5,
        'avg_cost_eur_k': 70,
        'escalation_rate': 4.0
    },
    'supply_chain': {
        'name': 'Supply Chain & Logistics',
        'base_headcount': 1100,
        'percentage': 4.5,
        'avg_cost_eur_k': 60,
        'escalation_rate': 3.5
    },
    'finance_admin': {
        'name': 'Finance & Administration',
        'base_headcount': 1500,
        'percentage': 6.2,
        'avg_cost_eur_k': 55,
        'escalation_rate': 3.0
    },
    'it_digital': {
        'name': 'IT & Digital',
        'base_headcount': 400,
        'percentage': 1.6,
        'avg_cost_eur_k': 85,
        'escalation_rate': 5.0
    },
    'sustainability': {
        'name': 'Sustainability & Compliance',
        'base_headcount': 800,
        'percentage': 3.3,
        'avg_cost_eur_k': 65,
        'escalation_rate': 4.0
    },
    'executive_management': {
        'name': 'Executive Management',
        'base_headcount': 150,
        'percentage': 0.6,
        'avg_cost_eur_k': 250,
        'escalation_rate': 2.0
    },
    'other': {
        'name': 'Other',
        'base_headcount': 2250,
        'percentage': 9.2,
        'avg_cost_eur_k': 45,
        'escalation_rate': 2.5
    }
}

# Default regional distribution
DEFAULT_REGIONS = {
    'europe': {
        'headcount_2024': 12000,
        'percent': 49.3,
        'avg_cost_eur_k': 65,
        'target_2035': 14500
    },
    'south_america': {
        'headcount_2024': 3500,
        'percent': 14.4,
        'avg_cost_eur_k': 42,
        'target_2035': 5200
    },
    'north_america': {
        'headcount_2024': 2000,
        'percent': 8.2,
        'avg_cost_eur_k': 75,
        'target_2035': 3000
    },
    'asia_pacific': {
        'headcount_2024': 3850,
        'percent': 15.8,
        'avg_cost_eur_k': 35,
        'target_2035': 8050
    },
    'africa_middle_east': {
        'headcount_2024': 700,
        'percent': 2.9,
        'avg_cost_eur_k': 38,
        'target_2035': 4000
    },
    'global_support': {
        'headcount_2024': 1300,
        'percent': 5.3,
        'avg_cost_eur_k': 70,
        'target_2035': 3750
    }
}

# Default phase-based hiring
DEFAULT_PHASES = {
    'phase_1': {
        'name': 'Foundation & Acceleration',
        'start_year': 2025,
        'end_year': 2026,
        'total_hires': 3050
    },
    'phase_2': {
        'name': 'Expansion & Scaling',
        'start_year': 2027,
        'end_year': 2029,
        'total_hires': 5100
    },
    'phase_3': {
        'name': 'Optimization & Maturation',
        'start_year': 2030,
        'end_year': 2035,
        'total_hires': 6000
    }
}


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


def extract_org_params(config: Dict) -> Tuple[Dict, Dict, Dict, int]:
    """
    Extract organizational parameters from configuration.

    Args:
        config: Configuration dictionary

    Returns:
        Tuple of (functions, regions, phases, base_headcount)
    """
    assumptions = config.get('strategic_assumptions', {})

    # Extract base headcount
    org_data = config.get('customer', {}).get('organization', {})
    base_headcount = org_data.get('total_employees', 24350)

    # Extract functions (use defaults if not specified)
    functions = DEFAULT_FUNCTIONS.copy()

    headcount_costs = assumptions.get('headcount_costs_by_region', {})
    escalation = assumptions.get('headcount_escalation_by_function', {})

    # Update from config if available
    for func_key, func_data in escalation.items():
        if func_key in functions:
            if isinstance(func_data, dict):
                functions[func_key]['avg_cost_eur_k'] = func_data.get('base_avg_cost_eur_k', functions[func_key]['avg_cost_eur_k'])
                functions[func_key]['escalation_rate'] = func_data.get('escalation_percent_per_year', functions[func_key]['escalation_rate'])

    # Extract regional data
    regions = DEFAULT_REGIONS.copy()

    for region_key, region_data in headcount_costs.items():
        if region_key in regions and isinstance(region_data, dict):
            regions[region_key]['avg_cost_eur_k'] = region_data.get('avg_cost_per_employee_eur_k', regions[region_key]['avg_cost_eur_k'])

    # Extract phases (use defaults)
    phases = DEFAULT_PHASES.copy()

    return functions, regions, phases, base_headcount


def calculate_function_headcount_trajectory(
    functions: Dict,
    base_headcount: int,
    phases: Dict,
    years: np.ndarray
) -> pd.DataFrame:
    """
    Calculate headcount trajectory by function over time.

    Args:
        functions: Function parameters dictionary
        base_headcount: Total base headcount (2024)
        phases: Phase definitions
        years: Array of years [2024, 2025, ..., 2035]

    Returns:
        DataFrame with headcount by function and year
    """
    # Calculate total growth
    total_hires = sum(p['total_hires'] for p in phases.values())
    target_headcount = base_headcount + total_hires

    # Create growth trajectory (smooth S-curve approximation)
    growth_rate = (target_headcount / base_headcount) ** (1 / 11) - 1

    data = {'Year': years}

    for func_key, func_params in functions.items():
        func_base = func_params['base_headcount']
        func_pct = func_params['percentage'] / 100

        # Project function headcount maintaining relative proportions
        # with slight adjustments for strategic functions (IT grows faster)
        if func_key == 'it_digital':
            func_growth_multiplier = 1.5  # IT grows 50% faster than average
        elif func_key in ['research_development', 'sustainability']:
            func_growth_multiplier = 1.3  # R&D and sustainability grow 30% faster
        elif func_key == 'executive_management':
            func_growth_multiplier = 0.5  # Executive grows slower (leverage)
        else:
            func_growth_multiplier = 1.0

        func_cagr = growth_rate * func_growth_multiplier
        func_trajectory = func_base * np.power(1 + func_cagr, years - 2024)
        data[func_key] = np.round(func_trajectory).astype(int)

    df = pd.DataFrame(data)

    # Add total column
    func_cols = [c for c in df.columns if c != 'Year']
    df['Total'] = df[func_cols].sum(axis=1)

    # Calculate YoY growth
    df['YoY%'] = df['Total'].pct_change() * 100

    return df


def calculate_regional_headcount_trajectory(
    regions: Dict,
    base_headcount: int,
    phases: Dict,
    years: np.ndarray
) -> pd.DataFrame:
    """
    Calculate headcount trajectory by region over time.

    Args:
        regions: Regional parameters dictionary
        base_headcount: Total base headcount (2024)
        phases: Phase definitions
        years: Array of years [2024, 2025, ..., 2035]

    Returns:
        DataFrame with headcount by region and year
    """
    data = {'Year': years}

    for region_key, region_params in regions.items():
        base_hc = region_params['headcount_2024']
        target_hc = region_params['target_2035']

        # Calculate region-specific CAGR
        if base_hc > 0:
            region_cagr = (target_hc / base_hc) ** (1 / 11) - 1
        else:
            region_cagr = 0

        trajectory = base_hc * np.power(1 + region_cagr, years - 2024)
        data[region_key] = np.round(trajectory).astype(int)

    df = pd.DataFrame(data)

    # Add total column
    region_cols = [c for c in df.columns if c != 'Year']
    df['Total'] = df[region_cols].sum(axis=1)

    return df


def calculate_payroll_projection(
    headcount_df: pd.DataFrame,
    functions: Dict,
    years: np.ndarray
) -> pd.DataFrame:
    """
    Calculate payroll cost projection based on headcount.

    Args:
        headcount_df: Headcount projection DataFrame
        functions: Function parameters with cost data
        years: Array of years

    Returns:
        DataFrame with annual payroll projection
    """
    payroll_data = []

    for year in years:
        year_row = headcount_df[headcount_df['Year'] == year]
        if year_row.empty:
            continue

        years_from_base = year - 2024
        total_payroll = 0

        for func_key, func_params in functions.items():
            if func_key in year_row.columns:
                hc = year_row[func_key].values[0]
                base_cost = func_params['avg_cost_eur_k']
                escalation = func_params['escalation_rate'] / 100

                # Calculate escalated cost
                cost_per_employee = base_cost * ((1 + escalation) ** years_from_base)
                func_payroll = hc * cost_per_employee / 1000  # Convert to millions

                total_payroll += func_payroll

        total_hc = year_row['Total'].values[0]
        avg_cost = (total_payroll * 1000 / total_hc) if total_hc > 0 else 0

        payroll_data.append({
            'Year': year,
            'Headcount': total_hc,
            'Payroll_EUR_M': round(total_payroll, 1),
            'Avg_Cost_EUR_K': round(avg_cost, 1)
        })

    return pd.DataFrame(payroll_data)


def calculate_hiring_plan(
    phases: Dict,
    functions: Dict,
    base_headcount: int
) -> pd.DataFrame:
    """
    Calculate phase-based hiring plan.

    Args:
        phases: Phase definitions
        functions: Function parameters
        base_headcount: Base headcount (2024)

    Returns:
        DataFrame with hiring plan by phase
    """
    plan_data = []

    for phase_key, phase_params in phases.items():
        total_hires = phase_params['total_hires']
        duration_years = phase_params['end_year'] - phase_params['start_year'] + 1

        # Distribute hires across functions (based on strategic priorities)
        function_hires = {}
        for func_key, func_params in functions.items():
            if func_key == 'it_digital':
                func_share = 0.08  # IT gets more hires (8%)
            elif func_key == 'research_development':
                func_share = 0.06  # R&D gets 6%
            elif func_key == 'operations':
                func_share = 0.45  # Operations gets bulk (45%)
            elif func_key == 'sales_customer_service':
                func_share = 0.15  # Sales 15%
            else:
                func_share = func_params['percentage'] / 100

            function_hires[func_key] = round(total_hires * func_share)

        plan_data.append({
            'Phase': phase_params['name'],
            'Period': f"{phase_params['start_year']}-{phase_params['end_year']}",
            'Total_Hires': total_hires,
            'Annual_Average': round(total_hires / duration_years),
            **{f'Hires_{k}': v for k, v in function_hires.items()}
        })

    return pd.DataFrame(plan_data)


def project_headcount(config: Dict) -> Dict:
    """
    Main function: Project organizational headcount and costs.

    Args:
        config: Configuration dictionary (from YAML)

    Returns:
        Dictionary with:
        - headcount_by_function: DataFrame with headcount by function
        - headcount_by_region: DataFrame with headcount by region
        - payroll_projection: DataFrame with payroll costs
        - hiring_plan: DataFrame with phase-based hiring plan
        - summary: Summary metrics dictionary
    """
    # Extract parameters
    functions, regions, phases, base_headcount = extract_org_params(config)

    # Generate years array
    years = np.arange(2024, 2036)

    # Calculate trajectories
    headcount_by_function = calculate_function_headcount_trajectory(
        functions, base_headcount, phases, years
    )

    headcount_by_region = calculate_regional_headcount_trajectory(
        regions, base_headcount, phases, years
    )

    # Calculate payroll
    payroll_projection = calculate_payroll_projection(
        headcount_by_function, functions, years
    )

    # Calculate hiring plan
    hiring_plan = calculate_hiring_plan(phases, functions, base_headcount)

    # Calculate summary metrics
    hc_2024 = headcount_by_function[headcount_by_function['Year'] == 2024]['Total'].values[0]
    hc_2035 = headcount_by_function[headcount_by_function['Year'] == 2035]['Total'].values[0]
    payroll_2024 = payroll_projection[payroll_projection['Year'] == 2024]['Payroll_EUR_M'].values[0]
    payroll_2035 = payroll_projection[payroll_projection['Year'] == 2035]['Payroll_EUR_M'].values[0]

    summary = {
        'base_year_headcount': int(hc_2024),
        'target_year_headcount': int(hc_2035),
        'total_growth': int(hc_2035 - hc_2024),
        'growth_percent': round((hc_2035 / hc_2024 - 1) * 100, 1),
        'headcount_cagr_percent': round(((hc_2035 / hc_2024) ** (1/11) - 1) * 100, 2),
        'payroll_2024_eur_m': payroll_2024,
        'payroll_2035_eur_m': payroll_2035,
        'payroll_cagr_percent': round(((payroll_2035 / payroll_2024) ** (1/11) - 1) * 100, 2),
        'avg_cost_2024_eur_k': payroll_projection[payroll_projection['Year'] == 2024]['Avg_Cost_EUR_K'].values[0],
        'avg_cost_2035_eur_k': payroll_projection[payroll_projection['Year'] == 2035]['Avg_Cost_EUR_K'].values[0]
    }

    return {
        'headcount_by_function': headcount_by_function,
        'headcount_by_region': headcount_by_region,
        'payroll_projection': payroll_projection,
        'hiring_plan': hiring_plan,
        'summary': summary,
        'functions': functions,
        'regions': regions,
        'phases': phases
    }


def format_results(results: Dict) -> str:
    """
    Format organizational scaling results for display.

    Args:
        results: Results dictionary from project_headcount

    Returns:
        Formatted string
    """
    output = []
    output.append("\n" + "="*80)
    output.append("ORGANIZATIONAL SCALING MODEL (OSM-1.0) - RESULTS")
    output.append("="*80)

    summary = results['summary']

    output.append("\n[1] SUMMARY METRICS")
    output.append("-" * 60)
    output.append(f"  2024 Headcount:      {summary['base_year_headcount']:,}")
    output.append(f"  2035 Headcount:      {summary['target_year_headcount']:,}")
    output.append(f"  Total Growth:        +{summary['total_growth']:,} (+{summary['growth_percent']:.1f}%)")
    output.append(f"  Headcount CAGR:      {summary['headcount_cagr_percent']:.2f}%")
    output.append(f"  2024 Payroll:        €{summary['payroll_2024_eur_m']:,.0f}M")
    output.append(f"  2035 Payroll:        €{summary['payroll_2035_eur_m']:,.0f}M")
    output.append(f"  Payroll CAGR:        {summary['payroll_cagr_percent']:.2f}%")
    output.append(f"  Avg Cost 2024:       €{summary['avg_cost_2024_eur_k']:.0f}K")
    output.append(f"  Avg Cost 2035:       €{summary['avg_cost_2035_eur_k']:.0f}K")

    output.append("\n[2] HEADCOUNT BY FUNCTION (Key Years)")
    output.append("-" * 60)
    hc_df = results['headcount_by_function']
    key_years = [2024, 2026, 2029, 2035]
    key_rows = hc_df[hc_df['Year'].isin(key_years)]
    output.append(key_rows.to_string(index=False))

    output.append("\n[3] HEADCOUNT BY REGION (Key Years)")
    output.append("-" * 60)
    region_df = results['headcount_by_region']
    key_rows = region_df[region_df['Year'].isin(key_years)]
    output.append(key_rows.to_string(index=False))

    output.append("\n[4] PAYROLL PROJECTION")
    output.append("-" * 60)
    payroll_df = results['payroll_projection']
    key_rows = payroll_df[payroll_df['Year'].isin(key_years)]
    output.append(key_rows.to_string(index=False))

    output.append("\n[5] HIRING PLAN BY PHASE")
    output.append("-" * 60)
    plan_df = results['hiring_plan'][['Phase', 'Period', 'Total_Hires', 'Annual_Average']]
    output.append(plan_df.to_string(index=False))

    output.append("\n" + "="*80)
    return "\n".join(output)


def main():
    """Main entry point for command-line execution."""
    if len(sys.argv) < 2:
        print("Usage: python organizational_scaling.py <config_file.yaml>")
        sys.exit(1)

    config_file = sys.argv[1]

    print(f"Loading configuration: {config_file}")
    config = load_configuration(config_file)

    print("Running organizational scaling model...")
    results = project_headcount(config)

    print(format_results(results))


if __name__ == '__main__':
    main()
