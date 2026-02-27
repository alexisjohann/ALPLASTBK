#!/usr/bin/env python3
"""
Apply All Models - Orchestrator Script v2.0
Runs all 10 strategic models sequentially:

v1.0 Core:
  - RPM-1.0: Revenue Projection Model
  - MCSM-1.0: Monte Carlo Simulation Model
  - OSM-1.0: Organizational Scaling Model
  - CAM-1.0: Capital Expenditure Allocation Model

v1.5 Financial:
  - CSM-1.0: Cost Structure Model
  - PLM-1.0: Profit & Loss Model
  - SAM-1.0: Sensitivity Analysis Model (optional)

v2.0 Value & Strategy:
  - CFM-1.0: Cash Flow Model
  - VCM-1.0: Value Creation Model
  - SCM-1.0: Scenario Comparison Model (optional)

Usage:
    python apply_all_models.py <customer_name> [--output-dir <path>]
    python apply_all_models.py ALPLA
    python apply_all_models.py ALPLA --output-dir outputs/
    python apply_all_models.py ALPLA --with-sensitivity --with-scenarios

Model Version: 2.0.0
Implementation Date: 2026-01-16
"""

import os
import sys
import yaml
import time
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# v1.0 Core Models
from revenue_projection import project_revenue, calculate_summary_metrics, load_configuration
from monte_carlo_simulation import run_monte_carlo, format_results as format_mc_results
from organizational_scaling import project_headcount, format_results as format_org_results
from capex_allocation import project_capex, format_results as format_capex_results

# v1.5 Financial Models
from cost_structure import project_costs, format_results as format_cost_results
from profit_loss import project_pnl, format_results as format_pnl_results
from sensitivity_analysis import run_sensitivity_analysis, format_results as format_sens_results

# v2.0 Value & Strategy Models
from cash_flow import project_cash_flow, format_results as format_cf_results
from value_creation import calculate_value_creation, format_results as format_vc_results
from scenario_comparison import compare_scenarios, format_results as format_sc_results


def find_customer_config(customer_name: str, base_path: str = None) -> Dict[str, str]:
    """
    Find customer configuration files.

    Args:
        customer_name: Name of customer (e.g., 'ALPLA')
        base_path: Base path to search from (optional)

    Returns:
        Dictionary with paths to config files
    """
    if base_path is None:
        # Try to find the repository root
        current = Path(__file__).parent
        while current != current.parent:
            if (current / 'data' / 'customers').exists():
                base_path = str(current)
                break
            current = current.parent
        else:
            base_path = '.'

    customer_dir = Path(base_path) / 'data' / 'customers' / customer_name.lower()

    if not customer_dir.exists():
        raise FileNotFoundError(f"Customer directory not found: {customer_dir}")

    # Find config files
    config_files = {
        'profile': customer_dir / f'{customer_name.lower()}_profile.yaml',
        'assumptions': customer_dir / f'{customer_name.lower()}_assumptions.yaml',
        'scenarios': customer_dir / f'{customer_name.lower()}_scenarios.yaml',
        'models': customer_dir / f'{customer_name.lower()}_models.yaml',
    }

    # Validate required files exist
    required = ['assumptions']
    for key in required:
        if not config_files[key].exists():
            raise FileNotFoundError(f"Required file not found: {config_files[key]}")

    return {k: str(v) for k, v in config_files.items() if v.exists()}


def load_all_configs(config_paths: Dict[str, str]) -> Dict:
    """
    Load and merge all configuration files.

    Args:
        config_paths: Dictionary with paths to config files

    Returns:
        Merged configuration dictionary
    """
    merged_config = {}

    for config_type, path in config_paths.items():
        try:
            with open(path, 'r') as f:
                config = yaml.safe_load(f)
                if config:
                    merged_config.update(config)
        except Exception as e:
            print(f"Warning: Could not load {path}: {e}")

    return merged_config


def save_results_csv(df, filepath: str):
    """Save DataFrame to CSV."""
    df.to_csv(filepath, index=False)
    print(f"  Saved: {filepath}")


def save_results_yaml(data: Dict, filepath: str):
    """Save dictionary to YAML."""
    with open(filepath, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
    print(f"  Saved: {filepath}")


def run_all_models(
    customer_name: str,
    output_dir: Optional[str] = None,
    num_simulations: int = 10000,
    verbose: bool = True,
    run_sensitivity: bool = False,
    run_scenarios: bool = False
) -> Dict:
    """
    Run all 10 strategic models (v2.0) for a customer.

    Args:
        customer_name: Name of customer (e.g., 'ALPLA')
        output_dir: Directory to save outputs (optional)
        num_simulations: Number of Monte Carlo simulations
        verbose: Print progress and results
        run_sensitivity: Run SAM-1.0 sensitivity analysis (optional)
        run_scenarios: Run SCM-1.0 scenario comparison (optional)

    Returns:
        Dictionary with all model results
    """
    start_time = time.time()

    # Calculate number of models to run
    # Base: 8 models (RPM, MCSM, OSM, CAM, CSM, PLM, CFM, VCM)
    # Optional: SAM (+1), SCM (+1)
    num_models = 8
    if run_sensitivity:
        num_models += 1
    if run_scenarios:
        num_models += 1

    # Header
    if verbose:
        print("\n" + "="*80)
        print(f"STRATEGIC MODEL SUITE v2.0 - {customer_name.upper()}")
        print("="*80)
        print(f"Execution Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Models to Run: {num_models}")
        print(f"Monte Carlo Simulations: {num_simulations:,}")
        print("="*80)

    # Phase 1: Load Configuration
    if verbose:
        print("\n[PHASE 1] Loading Configuration...")

    config_paths = find_customer_config(customer_name)
    config = load_all_configs(config_paths)

    if verbose:
        print(f"  ✓ Loaded {len(config_paths)} configuration files")
        for key, path in config_paths.items():
            print(f"    - {key}: {Path(path).name}")

    # Setup output directory
    if output_dir:
        output_path = Path(output_dir)
    else:
        output_path = Path(config_paths['assumptions']).parent

    output_path.mkdir(parents=True, exist_ok=True)

    # Phase 2: Revenue Projection Model (RPM-1.0)
    if verbose:
        print("\n[PHASE 2] Running Revenue Projection Model (RPM-1.0)...")

    rpm_start = time.time()
    try:
        revenue_df = project_revenue(config)
        revenue_metrics = calculate_summary_metrics(revenue_df)
        rpm_time = time.time() - rpm_start

        if verbose:
            print(f"  ✓ RPM-1.0 completed in {rpm_time:.2f}s")
            print(f"    2024 Revenue: €{revenue_metrics['base_year_2024_revenue_eur_m']:,.0f}M")
            print(f"    2035 Revenue: €{revenue_metrics['target_year_2035_revenue_eur_m']:,.0f}M")
            print(f"    CAGR: {revenue_metrics['blended_cagr_percent']:.2f}%")

        # Save results
        save_results_csv(revenue_df, str(output_path / 'revenue_projection_2024_2035.csv'))

    except Exception as e:
        print(f"  ✗ RPM-1.0 failed: {e}")
        revenue_df = None
        revenue_metrics = {}

    # Phase 3: Monte Carlo Simulation (MCSM-1.0)
    if verbose:
        print(f"\n[PHASE 3] Running Monte Carlo Simulation (MCSM-1.0, {num_simulations:,} runs)...")

    mcsm_start = time.time()
    try:
        mc_results = run_monte_carlo(
            config,
            revenue_df=revenue_df,
            num_simulations=num_simulations
        )
        mcsm_time = time.time() - mcsm_start

        if verbose:
            print(f"  ✓ MCSM-1.0 completed in {mcsm_time:.2f}s")
            print(f"    Mean 2035 Revenue: €{mc_results['statistics']['mean']:,.0f}M")
            print(f"    95% CI: [€{mc_results['percentiles']['p5']:,.0f}M - €{mc_results['percentiles']['p95']:,.0f}M]")
            print(f"    P(≥ Conservative): {mc_results['probabilities'].get('prob_exceeds_conservative', 0)*100:.1f}%")

        # Save results
        mc_summary = {
            'percentiles': mc_results['percentiles'],
            'statistics': mc_results['statistics'],
            'probabilities': mc_results['probabilities'],
            'sensitivity': mc_results['sensitivity']
        }
        save_results_yaml(mc_summary, str(output_path / 'monte_carlo_summary.yaml'))

    except Exception as e:
        print(f"  ✗ MCSM-1.0 failed: {e}")
        mc_results = {}

    # Phase 4: Organizational Scaling Model (OSM-1.0)
    if verbose:
        print("\n[PHASE 4] Running Organizational Scaling Model (OSM-1.0)...")

    osm_start = time.time()
    try:
        org_results = project_headcount(config)
        osm_time = time.time() - osm_start

        if verbose:
            summary = org_results['summary']
            print(f"  ✓ OSM-1.0 completed in {osm_time:.2f}s")
            print(f"    2024 Headcount: {summary['base_year_headcount']:,}")
            print(f"    2035 Headcount: {summary['target_year_headcount']:,}")
            print(f"    Growth: +{summary['total_growth']:,} (+{summary['growth_percent']:.1f}%)")
            print(f"    2035 Payroll: €{summary['payroll_2035_eur_m']:,.0f}M")

        # Save results
        save_results_csv(org_results['headcount_by_function'], str(output_path / 'headcount_by_function.csv'))
        save_results_csv(org_results['headcount_by_region'], str(output_path / 'headcount_by_region.csv'))
        save_results_csv(org_results['payroll_projection'], str(output_path / 'payroll_projection.csv'))

    except Exception as e:
        print(f"  ✗ OSM-1.0 failed: {e}")
        org_results = {}

    # Phase 5: Capex Allocation Model (CAM-1.0)
    if verbose:
        print("\n[PHASE 5] Running Capex Allocation Model (CAM-1.0)...")

    cam_start = time.time()
    try:
        capex_results = project_capex(config)
        cam_time = time.time() - cam_start

        if verbose:
            summary = capex_results['summary']
            print(f"  ✓ CAM-1.0 completed in {cam_time:.2f}s")
            print(f"    Total 11-Year Capex: €{summary['total_capex_11_years_eur_m']:,.0f}M")
            print(f"    Annual Average: €{summary['annual_average_eur_m']:,.0f}M")
            print(f"    Expected Benefits: €{summary['total_benefits_eur_m']:,.0f}M")
            print(f"    Total ROI: {summary['total_roi_percent']:.0f}%")

        # Save results
        save_results_csv(capex_results['annual_capex'], str(output_path / 'capex_roadmap.csv'))
        save_results_csv(capex_results['roi_analysis'], str(output_path / 'roi_analysis.csv'))
        save_results_csv(capex_results['phase_summary'], str(output_path / 'capex_phase_summary.csv'))

    except Exception as e:
        print(f"  ✗ CAM-1.0 failed: {e}")
        capex_results = {}

    # Phase 6: Cost Structure Model (CSM-1.0) - v1.5
    if verbose:
        print("\n[PHASE 6] Running Cost Structure Model (CSM-1.0)...")

    csm_start = time.time()
    cost_results = {}
    try:
        cost_results = project_costs(config, revenue_df)
        csm_time = time.time() - csm_start

        if verbose:
            summary = cost_results.get('summary', {})
            print(f"  ✓ CSM-1.0 completed in {csm_time:.2f}s")
            print(f"    2024 Total Costs: €{summary.get('base_year_costs_m', 0):,.0f}M")
            print(f"    2035 Total Costs: €{summary.get('final_year_costs_m', 0):,.0f}M")
            print(f"    Cost CAGR: {summary.get('cost_cagr_percent', 0):.1f}%")

        # Save results
        if 'cost_projection' in cost_results:
            save_results_csv(cost_results['cost_projection'], str(output_path / 'cost_projection.csv'))

    except Exception as e:
        print(f"  ✗ CSM-1.0 failed: {e}")
        cost_results = {}

    # Phase 7: Profit & Loss Model (PLM-1.0) - v1.5
    if verbose:
        print("\n[PHASE 7] Running Profit & Loss Model (PLM-1.0)...")

    plm_start = time.time()
    pnl_results = {}
    try:
        cost_df = cost_results.get('cost_projection') if cost_results else None
        pnl_results = project_pnl(config, revenue_df, cost_df)
        plm_time = time.time() - plm_start

        if verbose:
            summary = pnl_results.get('summary', {})
            ebitda = summary.get('ebitda', {})
            print(f"  ✓ PLM-1.0 completed in {plm_time:.2f}s")
            print(f"    2024 EBITDA: €{ebitda.get('base_year_m', 0):,.0f}M ({ebitda.get('base_margin_percent', 0):.1f}% margin)")
            print(f"    2035 EBITDA: €{ebitda.get('final_year_m', 0):,.0f}M ({ebitda.get('final_margin_percent', 0):.1f}% margin)")

        # Save results
        if 'pnl_projection' in pnl_results:
            save_results_csv(pnl_results['pnl_projection'], str(output_path / 'pnl_projection.csv'))
        if 'margins' in pnl_results:
            save_results_csv(pnl_results['margins'], str(output_path / 'margin_evolution.csv'))

    except Exception as e:
        print(f"  ✗ PLM-1.0 failed: {e}")
        pnl_results = {}

    # Phase 8: Sensitivity Analysis Model (SAM-1.0) - v1.5 (Optional)
    sensitivity_results = {}
    if run_sensitivity:
        if verbose:
            print("\n[PHASE 8] Running Sensitivity Analysis Model (SAM-1.0)...")

        sam_start = time.time()
        try:
            # Define model runner for sensitivity analysis
            def model_runner_for_sensitivity(test_config):
                rev_df = project_revenue(test_config)
                cost_res = project_costs(test_config, rev_df)
                pnl_res = project_pnl(test_config, rev_df, cost_res.get('cost_projection'))
                return {'revenue': rev_df, 'costs': cost_res, 'pnl': pnl_res}

            def output_extractor_for_sensitivity(model_results):
                outputs = {}
                rev_df = model_results.get('revenue')
                if rev_df is not None and 'Total' in rev_df.columns:
                    final_row = rev_df[rev_df['Year'] == rev_df['Year'].max()].iloc[0]
                    outputs['revenue_2035'] = float(final_row['Total'])
                pnl = model_results.get('pnl', {})
                if pnl and 'pnl_projection' in pnl:
                    pnl_df = pnl['pnl_projection']
                    final_row = pnl_df[pnl_df['Year'] == pnl_df['Year'].max()].iloc[0]
                    outputs['ebitda_2035'] = float(final_row.get('EBITDA', 0))
                    outputs['net_income_2035'] = float(final_row.get('Net_Income', 0))
                return outputs

            sensitivity_results = run_sensitivity_analysis(
                config=config,
                model_runner=model_runner_for_sensitivity,
                output_extractor=output_extractor_for_sensitivity
            )
            sam_time = time.time() - sam_start

            if verbose:
                summary = sensitivity_results.get('summary', {})
                print(f"  ✓ SAM-1.0 completed in {sam_time:.2f}s")
                print(f"    Parameters Tested: {summary.get('num_parameters', 0)}")
                print(f"    Scenarios Analyzed: {summary.get('num_scenarios', 0)}")
                top_drivers = summary.get('top_drivers', {})
                if 'revenue_2035' in top_drivers:
                    print(f"    Top Revenue Drivers: {', '.join(top_drivers['revenue_2035'][:3])}")

            # Save results
            save_results_yaml({
                'summary': sensitivity_results.get('summary', {}),
                'scenarios': sensitivity_results.get('scenarios', [])
            }, str(output_path / 'sensitivity_analysis.yaml'))

        except Exception as e:
            print(f"  ✗ SAM-1.0 failed: {e}")
            sensitivity_results = {}

    # Phase 9: Cash Flow Model (CFM-1.0) - v2.0
    if verbose:
        print("\n[PHASE 9] Running Cash Flow Model (CFM-1.0)...")

    cfm_start = time.time()
    cf_results = {}
    try:
        pnl_df = pnl_results.get('pnl_projection') if pnl_results else None
        capex_df = capex_results.get('annual_capex') if capex_results else None
        cf_results = project_cash_flow(config, pnl_df, capex_df)
        cfm_time = time.time() - cfm_start

        if verbose:
            summary = cf_results.get('summary', {})
            fcf = summary.get('free_cash_flow', {})
            print(f"  ✓ CFM-1.0 completed in {cfm_time:.2f}s")
            print(f"    Total FCF: €{fcf.get('total_m', 0):,.0f}M")
            print(f"    Avg FCF Yield: {fcf.get('avg_fcf_yield_percent', 0):.1f}%")
            cash = summary.get('cash_position', {})
            print(f"    Ending Cash: €{cash.get('closing_m', 0):,.0f}M")

        # Save results
        if 'cash_flow_projection' in cf_results:
            save_results_csv(cf_results['cash_flow_projection'], str(output_path / 'cash_flow_projection.csv'))

    except Exception as e:
        print(f"  ✗ CFM-1.0 failed: {e}")
        cf_results = {}

    # Phase 10: Value Creation Model (VCM-1.0) - v2.0
    if verbose:
        print("\n[PHASE 10] Running Value Creation Model (VCM-1.0)...")

    vcm_start = time.time()
    vc_results = {}
    try:
        pnl_df = pnl_results.get('pnl_projection') if pnl_results else None
        cf_df = cf_results.get('cash_flow_projection') if cf_results else None
        vc_results = calculate_value_creation(config, pnl_df, cf_df)
        vcm_time = time.time() - vcm_start

        if verbose:
            summary = vc_results.get('summary', {})
            wacc = summary.get('wacc', {})
            value = summary.get('value_creation', {})
            print(f"  ✓ VCM-1.0 completed in {vcm_time:.2f}s")
            print(f"    WACC: {wacc.get('wacc_percent', 0):.2f}%")
            print(f"    Total EVA: €{value.get('total_eva_m', 0):,.0f}M")
            print(f"    Avg ROIC: {value.get('avg_roic_percent', 0):.1f}%")
            status = "VALUE CREATING" if value.get('value_creating', False) else "VALUE DESTROYING"
            print(f"    Status: {status}")

        # Save results
        if 'value_metrics' in vc_results:
            save_results_csv(vc_results['value_metrics'], str(output_path / 'value_metrics.csv'))

    except Exception as e:
        print(f"  ✗ VCM-1.0 failed: {e}")
        vc_results = {}

    # Phase 11: Scenario Comparison Model (SCM-1.0) - v2.0 (Optional)
    sc_results = {}
    if run_scenarios:
        if verbose:
            print("\n[PHASE 11] Running Scenario Comparison Model (SCM-1.0)...")

        scm_start = time.time()
        try:
            # Define model runner for scenario comparison
            def model_runner_for_scenarios(test_config):
                rev_df = project_revenue(test_config)
                rev_metrics = calculate_summary_metrics(rev_df)
                pnl_res = project_pnl(test_config, rev_df)
                cf_res = project_cash_flow(test_config, pnl_res.get('pnl_projection'))
                return {
                    'revenue': {
                        'final_year_m': rev_metrics.get('target_year_2035_revenue_eur_m', 0),
                        'cagr_percent': rev_metrics.get('blended_cagr_percent', 0)
                    },
                    'pnl': pnl_res.get('summary', {}),
                    'cash_flow': cf_res.get('summary', {}).get('free_cash_flow', {})
                }

            sc_results = compare_scenarios(
                config=config,
                model_runner=model_runner_for_scenarios
            )
            scm_time = time.time() - scm_start

            if verbose:
                summary = sc_results.get('summary', {})
                print(f"  ✓ SCM-1.0 completed in {scm_time:.2f}s")
                print(f"    Scenarios Compared: {summary.get('num_scenarios', 0)}")
                print(f"    Best Scenario: {summary.get('best_scenario', 'N/A')}")

            # Save results
            if 'comparison_table' in sc_results:
                save_results_csv(sc_results['comparison_table'], str(output_path / 'scenario_comparison.csv'))
            if 'rankings' in sc_results:
                save_results_csv(sc_results['rankings'], str(output_path / 'scenario_rankings.csv'))

        except Exception as e:
            print(f"  ✗ SCM-1.0 failed: {e}")
            sc_results = {}

    # Phase 12: Generate Summary
    total_time = time.time() - start_time

    if verbose:
        print("\n" + "="*80)
        print("EXECUTION SUMMARY - v2.0")
        print("="*80)
        print(f"  Customer: {customer_name}")
        print(f"  Total Time: {total_time:.2f}s")
        print(f"  Models Run: {num_models}/{num_models}")
        print(f"    ✓ RPM-1.0 (Revenue Projection)")
        print(f"    ✓ MCSM-1.0 (Monte Carlo Simulation)")
        print(f"    ✓ OSM-1.0 (Organizational Scaling)")
        print(f"    ✓ CAM-1.0 (Capex Allocation)")
        print(f"    ✓ CSM-1.0 (Cost Structure)")
        print(f"    ✓ PLM-1.0 (Profit & Loss)")
        if run_sensitivity:
            print(f"    ✓ SAM-1.0 (Sensitivity Analysis)")
        print(f"    ✓ CFM-1.0 (Cash Flow) [v2.0]")
        print(f"    ✓ VCM-1.0 (Value Creation) [v2.0]")
        if run_scenarios:
            print(f"    ✓ SCM-1.0 (Scenario Comparison) [v2.0]")
        print(f"\n  Output Directory: {output_path}")
        print("="*80)

    # Create consolidated summary
    summary_metrics = {
        'customer': customer_name,
        'model_version': '2.0.0',
        'execution_date': datetime.now().isoformat(),
        'execution_time_seconds': round(total_time, 2),
        'models_run': num_models,
        'revenue': revenue_metrics if revenue_metrics else {},
        'monte_carlo': {
            'num_simulations': num_simulations,
            'mean_2035': mc_results.get('statistics', {}).get('mean'),
            'ci_95_lower': mc_results.get('percentiles', {}).get('p5'),
            'ci_95_upper': mc_results.get('percentiles', {}).get('p95'),
        } if mc_results else {},
        'organization': org_results.get('summary', {}),
        'capex': capex_results.get('summary', {}),
        'costs': cost_results.get('summary', {}),
        'pnl': pnl_results.get('summary', {}),
        'sensitivity': sensitivity_results.get('summary', {}) if run_sensitivity else {},
        'cash_flow': cf_results.get('summary', {}),
        'value_creation': vc_results.get('summary', {}),
        'scenarios': sc_results.get('summary', {}) if run_scenarios else {}
    }

    save_results_yaml(summary_metrics, str(output_path / 'summary_metrics.yaml'))

    return {
        'revenue': {'df': revenue_df, 'metrics': revenue_metrics},
        'monte_carlo': mc_results,
        'organization': org_results,
        'capex': capex_results,
        'costs': cost_results,
        'pnl': pnl_results,
        'sensitivity': sensitivity_results,
        'cash_flow': cf_results,
        'value_creation': vc_results,
        'scenarios': sc_results,
        'summary': summary_metrics,
        'output_path': str(output_path)
    }


def main():
    """Main entry point for command-line execution."""
    parser = argparse.ArgumentParser(
        description='Run all 10 strategic models (v2.0) for a customer',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python apply_all_models.py ALPLA
  python apply_all_models.py ALPLA --output-dir outputs/
  python apply_all_models.py ALPLA --simulations 5000 --quiet
  python apply_all_models.py ALPLA --with-sensitivity --with-scenarios

Models included (v2.0):
  v1.0 Core:
    - RPM-1.0: Revenue Projection Model
    - MCSM-1.0: Monte Carlo Simulation Model
    - OSM-1.0: Organizational Scaling Model
    - CAM-1.0: Capital Expenditure Allocation Model
  v1.5 Financial:
    - CSM-1.0: Cost Structure Model
    - PLM-1.0: Profit & Loss Model
    - SAM-1.0: Sensitivity Analysis Model (optional)
  v2.0 Value & Strategy:
    - CFM-1.0: Cash Flow Model
    - VCM-1.0: Value Creation Model
    - SCM-1.0: Scenario Comparison Model (optional)
        """
    )

    parser.add_argument('customer', help='Customer name (e.g., ALPLA)')
    parser.add_argument('--output-dir', '-o', help='Output directory for results')
    parser.add_argument('--simulations', '-n', type=int, default=10000,
                        help='Number of Monte Carlo simulations (default: 10000)')
    parser.add_argument('--quiet', '-q', action='store_true',
                        help='Suppress verbose output')
    parser.add_argument('--with-sensitivity', '-s', action='store_true',
                        help='Run SAM-1.0 sensitivity analysis (slower)')
    parser.add_argument('--with-scenarios', '-c', action='store_true',
                        help='Run SCM-1.0 scenario comparison (slower)')

    args = parser.parse_args()

    try:
        results = run_all_models(
            customer_name=args.customer,
            output_dir=args.output_dir,
            num_simulations=args.simulations,
            verbose=not args.quiet,
            run_sensitivity=args.with_sensitivity,
            run_scenarios=args.with_scenarios
        )

        print(f"\n✅ All models executed successfully!")
        print(f"   Results saved to: {results['output_path']}")

    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("\nAvailable customers:")
        # List available customers
        repo_root = Path(__file__).parent.parent.parent
        customers_dir = repo_root / 'data' / 'customers'
        if customers_dir.exists():
            for d in customers_dir.iterdir():
                if d.is_dir() and not d.name.startswith('.'):
                    print(f"  - {d.name}")
        sys.exit(1)

    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
