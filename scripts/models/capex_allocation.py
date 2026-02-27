#!/usr/bin/env python3
"""
Capex Allocation Model (CAM-1.0)
Capital expenditure planning and ROI analysis.

Usage:
    from capex_allocation import project_capex
    result = project_capex(config)
    roadmap_df = result['annual_capex']

Model Version: 1.0.0
Implementation Date: 2026-01-15
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
import yaml
import sys
from pathlib import Path


# Default initiative parameters
DEFAULT_INITIATIVES = {
    'erp_transformation': {
        'name': 'ERP Transformation (SAP S/4HANA)',
        'total_budget_eur_m': 35,
        'phase_allocation': {'phase_1': 40, 'phase_2': 40, 'phase_3': 20},
        'expected_benefits_eur_m': 150,
        'payback_years': 4,
        'description': 'Global ERP platform deployment across 240 plants'
    },
    'iot_deployment': {
        'name': 'IoT & Predictive Maintenance',
        'total_budget_eur_m': 25,
        'phase_allocation': {'phase_1': 20, 'phase_2': 40, 'phase_3': 40},
        'expected_benefits_eur_m': 80,
        'payback_years': 3,
        'description': 'IoT sensors and predictive maintenance'
    },
    'data_platform': {
        'name': 'Data Platform & Analytics',
        'total_budget_eur_m': 15,
        'phase_allocation': {'phase_1': 50, 'phase_2': 30, 'phase_3': 20},
        'expected_benefits_eur_m': 100,
        'payback_years': 3,
        'description': 'Snowflake data warehouse + ML models'
    },
    'cybersecurity': {
        'name': 'Cybersecurity & Compliance',
        'total_budget_eur_m': 20,
        'phase_allocation': {'phase_1': 30, 'phase_2': 40, 'phase_3': 30},
        'expected_benefits_eur_m': 0,  # Risk mitigation, not quantified
        'payback_years': None,
        'description': 'Zero-trust architecture, compliance automation'
    },
    'recycling_expansion': {
        'name': 'Recycling Capacity Expansion',
        'total_budget_eur_m': 60,
        'phase_allocation': {'phase_1': 10, 'phase_2': 60, 'phase_3': 30},
        'expected_benefits_eur_m': 200,
        'payback_years': 5,
        'description': 'Scale recycling from 350K to 700K tonnes/year'
    },
    'geographic_expansion': {
        'name': 'Geographic Expansion (APAC, AMET)',
        'total_budget_eur_m': 60,
        'phase_allocation': {'phase_1': 10, 'phase_2': 50, 'phase_3': 40},
        'expected_benefits_eur_m': 350,
        'payback_years': 6,
        'description': 'New plant capex (Thailand, Vietnam, India, Egypt)'
    },
    'maintenance': {
        'name': 'Maintenance Capex',
        'total_budget_eur_m': 335,
        'phase_allocation': {'phase_1': 30, 'phase_2': 35, 'phase_3': 35},
        'expected_benefits_eur_m': 100,
        'payback_years': 4,
        'description': 'Ongoing capex for existing 200 plants'
    }
}

# Phase definitions
DEFAULT_PHASES = {
    'phase_1': {
        'name': 'Foundation & Acceleration',
        'start_year': 2025,
        'end_year': 2026,
        'years': 2
    },
    'phase_2': {
        'name': 'Expansion & Scaling',
        'start_year': 2027,
        'end_year': 2029,
        'years': 3
    },
    'phase_3': {
        'name': 'Optimization & Maturation',
        'start_year': 2030,
        'end_year': 2035,
        'years': 6
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


def extract_capex_params(config: Dict) -> Tuple[Dict, Dict, float]:
    """
    Extract capex parameters from configuration.

    Args:
        config: Configuration dictionary

    Returns:
        Tuple of (initiatives, phases, total_capex)
    """
    assumptions = config.get('strategic_assumptions', {})
    capex_framework = assumptions.get('capex_framework', {})

    # Extract total capex
    total_capex = capex_framework.get('total_strategic_capex_11_years_eur_m', 550)

    # Extract initiatives (use defaults if not specified)
    initiatives = DEFAULT_INITIATIVES.copy()

    distribution = capex_framework.get('distribution_by_initiative', {})
    for init_key, init_data in distribution.items():
        if init_key in initiatives and isinstance(init_data, dict):
            initiatives[init_key]['total_budget_eur_m'] = init_data.get('total_eur_m', initiatives[init_key]['total_budget_eur_m'])
            if 'expected_benefits_eur_m' in init_data:
                initiatives[init_key]['expected_benefits_eur_m'] = init_data['expected_benefits_eur_m']
            if 'payback_years' in init_data:
                initiatives[init_key]['payback_years'] = init_data['payback_years']

    # Extract phases (use defaults)
    phases = DEFAULT_PHASES.copy()

    return initiatives, phases, total_capex


def calculate_annual_capex(
    initiatives: Dict,
    phases: Dict,
    years: np.ndarray
) -> pd.DataFrame:
    """
    Calculate annual capex by initiative.

    Args:
        initiatives: Initiative parameters dictionary
        phases: Phase definitions
        years: Array of years [2024, 2025, ..., 2035]

    Returns:
        DataFrame with annual capex by initiative
    """
    data = {'Year': years}

    for init_key, init_params in initiatives.items():
        total_budget = init_params['total_budget_eur_m']
        phase_alloc = init_params['phase_allocation']

        annual_capex = np.zeros(len(years))

        for phase_key, phase_pct in phase_alloc.items():
            if phase_key in phases:
                phase_info = phases[phase_key]
                phase_budget = total_budget * phase_pct / 100
                phase_years = phase_info['years']

                # Distribute evenly within phase
                annual_amount = phase_budget / phase_years

                # Find years in this phase
                for i, year in enumerate(years):
                    if phase_info['start_year'] <= year <= phase_info['end_year']:
                        annual_capex[i] += annual_amount

        data[init_key] = np.round(annual_capex, 1)

    df = pd.DataFrame(data)

    # Add total column
    init_cols = [c for c in df.columns if c != 'Year']
    df['Total'] = df[init_cols].sum(axis=1).round(1)

    # Add phase column
    def get_phase(year):
        for phase_key, phase_info in phases.items():
            if phase_info['start_year'] <= year <= phase_info['end_year']:
                return phase_info['name']
        return 'Pre-Phase'

    df['Phase'] = df['Year'].apply(get_phase)

    return df


def calculate_phase_summary(
    initiatives: Dict,
    phases: Dict
) -> pd.DataFrame:
    """
    Calculate capex summary by phase.

    Args:
        initiatives: Initiative parameters dictionary
        phases: Phase definitions

    Returns:
        DataFrame with phase-based capex summary
    """
    phase_data = []

    for phase_key, phase_info in phases.items():
        phase_total = 0
        strategic_total = 0
        maintenance_total = 0

        for init_key, init_params in initiatives.items():
            phase_pct = init_params['phase_allocation'].get(phase_key, 0)
            phase_budget = init_params['total_budget_eur_m'] * phase_pct / 100
            phase_total += phase_budget

            if init_key == 'maintenance':
                maintenance_total += phase_budget
            else:
                strategic_total += phase_budget

        phase_data.append({
            'Phase': phase_info['name'],
            'Period': f"{phase_info['start_year']}-{phase_info['end_year']}",
            'Years': phase_info['years'],
            'Total_Capex_EUR_M': round(phase_total, 1),
            'Annual_Average_EUR_M': round(phase_total / phase_info['years'], 1),
            'Strategic_EUR_M': round(strategic_total, 1),
            'Maintenance_EUR_M': round(maintenance_total, 1),
            'Strategic_Pct': round(strategic_total / phase_total * 100, 1) if phase_total > 0 else 0
        })

    return pd.DataFrame(phase_data)


def calculate_roi_analysis(initiatives: Dict) -> pd.DataFrame:
    """
    Calculate ROI analysis for each initiative.

    Args:
        initiatives: Initiative parameters dictionary

    Returns:
        DataFrame with ROI analysis
    """
    roi_data = []

    for init_key, init_params in initiatives.items():
        budget = init_params['total_budget_eur_m']
        benefits = init_params['expected_benefits_eur_m']
        payback = init_params['payback_years']

        # Handle non-numeric benefits (e.g., "Risk mitigation")
        if isinstance(benefits, str) or benefits is None:
            benefits_num = 0
        else:
            benefits_num = benefits

        if budget > 0 and benefits_num > 0:
            roi = (benefits_num - budget) / budget * 100
        else:
            roi = None

        roi_data.append({
            'Initiative': init_params['name'],
            'Budget_EUR_M': budget,
            'Benefits_EUR_M': benefits if isinstance(benefits, (int, float)) else 'N/A',
            'Net_Value_EUR_M': benefits_num - budget if benefits_num else None,
            'ROI_Pct': round(roi, 0) if roi else 'N/A',
            'Payback_Years': payback if payback else 'N/A'
        })

    df = pd.DataFrame(roi_data)

    # Add total row (only sum numeric benefits)
    total_budget = sum(init_params['total_budget_eur_m'] for init_params in initiatives.values())
    total_benefits = sum(
        init_params['expected_benefits_eur_m']
        for init_params in initiatives.values()
        if isinstance(init_params['expected_benefits_eur_m'], (int, float))
    )
    total_roi = (total_benefits - total_budget) / total_budget * 100 if total_budget > 0 else 0

    # Calculate weighted average payback
    weighted_payback_sum = 0
    weighted_budget = 0
    for init_params in initiatives.values():
        payback = init_params['payback_years']
        if isinstance(payback, (int, float)) and payback > 0:
            weighted_payback_sum += init_params['total_budget_eur_m'] * payback
            weighted_budget += init_params['total_budget_eur_m']
    avg_payback = weighted_payback_sum / weighted_budget if weighted_budget > 0 else None

    total_row = pd.DataFrame([{
        'Initiative': 'TOTAL',
        'Budget_EUR_M': total_budget,
        'Benefits_EUR_M': total_benefits,
        'Net_Value_EUR_M': total_benefits - total_budget,
        'ROI_Pct': round(total_roi, 0),
        'Payback_Years': round(avg_payback, 1) if avg_payback else 'N/A'
    }])

    df = pd.concat([df, total_row], ignore_index=True)

    return df


def calculate_quarterly_capex(annual_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate quarterly capex pace from annual data.

    Args:
        annual_df: Annual capex DataFrame

    Returns:
        DataFrame with quarterly capex
    """
    quarterly_data = []

    for _, row in annual_df.iterrows():
        year = row['Year']
        if year < 2025:
            continue

        for q in range(1, 5):
            quarterly_data.append({
                'Year': year,
                'Quarter': f'Q{q}',
                'Period': f'{year}-Q{q}',
                'Quarterly_Capex_EUR_M': round(row['Total'] / 4, 2),
                'Phase': row['Phase']
            })

    return pd.DataFrame(quarterly_data)


def project_capex(config: Dict) -> Dict:
    """
    Main function: Project capex allocation and ROI.

    Args:
        config: Configuration dictionary (from YAML)

    Returns:
        Dictionary with:
        - annual_capex: DataFrame with annual capex by initiative
        - phase_summary: DataFrame with phase-based summary
        - roi_analysis: DataFrame with ROI by initiative
        - quarterly_capex: DataFrame with quarterly capex pace
        - summary: Summary metrics dictionary
    """
    # Extract parameters
    initiatives, phases, total_capex = extract_capex_params(config)

    # Generate years array
    years = np.arange(2024, 2036)

    # Calculate annual capex
    annual_capex = calculate_annual_capex(initiatives, phases, years)

    # Calculate phase summary
    phase_summary = calculate_phase_summary(initiatives, phases)

    # Calculate ROI analysis
    roi_analysis = calculate_roi_analysis(initiatives)

    # Calculate quarterly capex
    quarterly_capex = calculate_quarterly_capex(annual_capex)

    # Calculate summary metrics
    total_budget = sum(init['total_budget_eur_m'] for init in initiatives.values())
    total_benefits = sum(
        init['expected_benefits_eur_m']
        for init in initiatives.values()
        if isinstance(init['expected_benefits_eur_m'], (int, float))
    )
    strategic_budget = sum(init['total_budget_eur_m'] for key, init in initiatives.items() if key != 'maintenance')

    summary = {
        'total_capex_11_years_eur_m': round(total_budget, 1),
        'annual_average_eur_m': round(total_budget / 11, 1),
        'total_benefits_eur_m': total_benefits,
        'net_value_eur_m': total_benefits - total_budget,
        'total_roi_percent': round((total_benefits - total_budget) / total_budget * 100, 1) if total_budget > 0 else 0,
        'strategic_capex_eur_m': round(strategic_budget, 1),
        'maintenance_capex_eur_m': round(initiatives['maintenance']['total_budget_eur_m'], 1),
        'strategic_percent': round(strategic_budget / total_budget * 100, 1) if total_budget > 0 else 0,
        'num_initiatives': len(initiatives)
    }

    return {
        'annual_capex': annual_capex,
        'phase_summary': phase_summary,
        'roi_analysis': roi_analysis,
        'quarterly_capex': quarterly_capex,
        'summary': summary,
        'initiatives': initiatives,
        'phases': phases
    }


def format_results(results: Dict) -> str:
    """
    Format capex allocation results for display.

    Args:
        results: Results dictionary from project_capex

    Returns:
        Formatted string
    """
    output = []
    output.append("\n" + "="*80)
    output.append("CAPEX ALLOCATION MODEL (CAM-1.0) - RESULTS")
    output.append("="*80)

    summary = results['summary']

    output.append("\n[1] SUMMARY METRICS")
    output.append("-" * 60)
    output.append(f"  Total 11-Year Capex:    €{summary['total_capex_11_years_eur_m']:,.0f}M")
    output.append(f"  Annual Average:         €{summary['annual_average_eur_m']:,.0f}M")
    output.append(f"  Strategic Capex:        €{summary['strategic_capex_eur_m']:,.0f}M ({summary['strategic_percent']:.0f}%)")
    output.append(f"  Maintenance Capex:      €{summary['maintenance_capex_eur_m']:,.0f}M")
    output.append(f"  Expected Benefits:      €{summary['total_benefits_eur_m']:,.0f}M")
    output.append(f"  Net Value:              €{summary['net_value_eur_m']:,.0f}M")
    output.append(f"  Total ROI:              {summary['total_roi_percent']:.0f}%")

    output.append("\n[2] PHASE SUMMARY")
    output.append("-" * 60)
    phase_df = results['phase_summary']
    output.append(phase_df.to_string(index=False))

    output.append("\n[3] ROI ANALYSIS BY INITIATIVE")
    output.append("-" * 60)
    roi_df = results['roi_analysis']
    output.append(roi_df.to_string(index=False))

    output.append("\n[4] ANNUAL CAPEX ROADMAP (Key Years)")
    output.append("-" * 60)
    annual_df = results['annual_capex']
    key_years = [2025, 2026, 2027, 2029, 2032, 2035]
    key_rows = annual_df[annual_df['Year'].isin(key_years)]
    # Select only important columns for display
    display_cols = ['Year', 'Phase', 'erp_transformation', 'recycling_expansion',
                    'geographic_expansion', 'maintenance', 'Total']
    available_cols = [c for c in display_cols if c in key_rows.columns]
    output.append(key_rows[available_cols].to_string(index=False))

    output.append("\n" + "="*80)
    return "\n".join(output)


def main():
    """Main entry point for command-line execution."""
    if len(sys.argv) < 2:
        print("Usage: python capex_allocation.py <config_file.yaml>")
        sys.exit(1)

    config_file = sys.argv[1]

    print(f"Loading configuration: {config_file}")
    config = load_configuration(config_file)

    print("Running capex allocation model...")
    results = project_capex(config)

    print(format_results(results))


if __name__ == '__main__':
    main()
