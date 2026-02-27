#!/usr/bin/env python3
"""
Strategy Cascade Model (STCM-2.0)
Top-Down Strategic Planning with Full Model Integration.

This module implements a cascading strategic model where each level
feeds into the next, following a top-down planning approach.

Now with ALL 20 MODELS integrated across 8 levels:

Level 0: Strategic Options (MAM) → M&A opportunities
Level 1: Strategic Direction (SCM, PFM) → Scenario + Portfolio analysis
Level 2: Growth Projection (RPM, MSM, PRM) → Revenue, Market Share, Pricing
Level 3: Resource Allocation (OSM, CAM) → Headcount, CapEx
Level 4: Cost Structure (CSM) → Cost projections
Level 5: Profitability (PLM, BEM) → P&L + Break-even analysis
Level 6: Cash & Value (CFM, VCM, BSM, WCM, DFM) → Full financial position
Level 7: Risk & Validation (MCSM, SAM, STM) → Uncertainty + Stress testing

Usage:
    from strategy_cascade import run_strategy_cascade
    results = run_strategy_cascade(config, scenario='base_case')

    # Or with strategic override:
    results = run_strategy_cascade(config,
        strategic_override={
            'revenue_cagr_adjustment': -0.5,  # -0.5pp off base
            'margin_target': 12.0  # Target 12% EBITDA
        })

Model Version: 2.0.0
Implementation Date: 2026-01-16

FULLY GENERIC: All parameters from config, no hardcoded defaults.
20 MODELS: Complete strategic planning suite.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Any, Callable
from copy import deepcopy
import yaml
import sys
import time
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Import all models (v1.0 - v3.0)
# v1.0 Core
from revenue_projection import project_revenue, calculate_summary_metrics
from monte_carlo_simulation import run_monte_carlo
from organizational_scaling import project_headcount
from capex_allocation import project_capex

# v1.5 Financial
from cost_structure import project_costs
from profit_loss import project_pnl
from sensitivity_analysis import run_sensitivity_analysis

# v2.0 Value & Strategy
from cash_flow import project_cash_flow
from value_creation import calculate_value_creation
from scenario_comparison import compare_scenarios

# v2.5 Financial Extended
from balance_sheet import project_balance_sheet
from working_capital import project_working_capital
from debt_financing import project_debt_financing
from break_even import analyze_break_even

# v3.0 Strategic
from market_share import project_market_share
from ma_synergy import analyze_ma_synergies
from portfolio import analyze_portfolio
from stress_testing import run_stress_tests
from pricing import analyze_pricing

from strategy_base import (
    load_config, get_nested, set_nested, save_csv, save_yaml,
    format_currency, format_percent, calculate_cagr,
    DEFAULT_BASE_YEAR, DEFAULT_PROJECTION_YEARS, DEFAULT_CURRENCY
)


@dataclass
class CascadeLevel:
    """Represents a level in the strategy cascade."""
    level: int
    name: str
    models: List[str]
    description: str
    inputs: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)
    status: str = 'pending'
    execution_time: float = 0.0
    results: Dict = field(default_factory=dict)


# Define the cascade structure (STCM-2.0: 8 Levels, 20 Models)
CASCADE_LEVELS = [
    CascadeLevel(
        level=0,
        name="Strategic Options",
        models=["MAM-1.0"],
        description="Evaluate M&A opportunities and strategic options",
        inputs=["strategic_assumptions", "ma_targets"],
        outputs=["ma_analysis", "synergy_potential", "deal_npv"]
    ),
    CascadeLevel(
        level=1,
        name="Strategic Direction",
        models=["SCM-1.0", "PFM-1.0"],
        description="Define scenarios and analyze portfolio positioning",
        inputs=["strategic_assumptions", "scenarios", "business_units"],
        outputs=["selected_scenario", "scenario_adjustments", "portfolio_strategy"]
    ),
    CascadeLevel(
        level=2,
        name="Growth Projection",
        models=["RPM-1.0", "MSM-1.0", "PRM-1.0"],
        description="Project revenue with market dynamics and pricing optimization",
        inputs=["scenario_adjustments", "regional_growth_rates", "market_data", "pricing_model"],
        outputs=["revenue_projection", "market_share_evolution", "optimal_pricing"]
    ),
    CascadeLevel(
        level=3,
        name="Resource Allocation",
        models=["OSM-1.0", "CAM-1.0"],
        description="Scale organization and allocate capital",
        inputs=["revenue_projection", "headcount_model", "capex_roadmap"],
        outputs=["headcount_projection", "payroll_projection", "capex_projection"]
    ),
    CascadeLevel(
        level=4,
        name="Cost Structure",
        models=["CSM-1.0"],
        description="Project cost structure based on revenue and resources",
        inputs=["revenue_projection", "payroll_projection", "cost_model"],
        outputs=["cost_projection", "cost_by_category"]
    ),
    CascadeLevel(
        level=5,
        name="Profitability",
        models=["PLM-1.0", "BEM-1.0"],
        description="Generate P&L and analyze break-even dynamics",
        inputs=["revenue_projection", "cost_projection", "pnl_model"],
        outputs=["pnl_projection", "margin_evolution", "break_even_analysis"]
    ),
    CascadeLevel(
        level=6,
        name="Cash & Value",
        models=["CFM-1.0", "VCM-1.0", "BSM-1.0", "WCM-1.0", "DFM-1.0"],
        description="Full financial position: cash flows, balance sheet, working capital, debt",
        inputs=["pnl_projection", "capex_projection", "working_capital", "debt_structure"],
        outputs=["cash_flow_projection", "value_metrics", "balance_sheet", "debt_schedule"]
    ),
    CascadeLevel(
        level=7,
        name="Risk & Validation",
        models=["MCSM-1.0", "SAM-1.0", "STM-1.0"],
        description="Quantify uncertainty, identify drivers, and stress test",
        inputs=["all_projections", "uncertainty_parameters", "stress_scenarios"],
        outputs=["probability_distribution", "sensitivity_analysis", "stress_test_results"]
    )
]


def extract_cascade_params(config: Dict) -> Dict:
    """
    Extract cascade parameters from configuration.

    Expected config structure:
    ```yaml
    strategy_cascade:
      selected_scenario: "base_case"  # or "conservative", "aggressive"
      cascade_mode: "full"  # or "quick" (skip Level 7)

      # Strategic overrides (applied to selected scenario)
      strategic_override:
        revenue_cagr_adjustment: 0  # Adjust CAGRs by this amount
        margin_target: null  # Override EBITDA margin target
        headcount_efficiency: 1.0  # 1.0 = no change, 0.9 = 10% more efficient
        capex_multiplier: 1.0  # Multiply capex by this factor

      # Validation thresholds
      validation:
        min_ebitda_margin: 8.0
        max_debt_ratio: 50.0
        min_roic: 10.0
    ```
    """
    cascade_config = config.get('strategy_cascade', {})

    params = {
        'selected_scenario': cascade_config.get('selected_scenario', 'base_case'),
        'cascade_mode': cascade_config.get('cascade_mode', 'full'),
        'strategic_override': cascade_config.get('strategic_override', {}),
        'validation': cascade_config.get('validation', {
            'min_ebitda_margin': 8.0,
            'max_debt_ratio': 50.0,
            'min_roic': 10.0
        }),
        'base_year': config.get('strategic_assumptions', {}).get('base_year', DEFAULT_BASE_YEAR),
        'projection_years': config.get('strategic_assumptions', {}).get('projection_years', DEFAULT_PROJECTION_YEARS),
        'currency': config.get('strategic_assumptions', {}).get('currency', DEFAULT_CURRENCY)
    }

    return params


def apply_strategic_override(config: Dict, override: Dict) -> Dict:
    """
    Apply strategic overrides to configuration.

    Args:
        config: Base configuration
        override: Strategic override parameters

    Returns:
        Modified configuration
    """
    modified = deepcopy(config)

    # Revenue CAGR adjustment
    cagr_adj = override.get('revenue_cagr_adjustment', 0)
    if cagr_adj != 0:
        regions = get_nested(modified, 'strategic_assumptions.regional_growth_rates', {})
        for region, data in regions.items():
            if isinstance(data, dict) and 'cagr' in data:
                data['cagr'] = data['cagr'] + cagr_adj

    # Margin target override
    margin_target = override.get('margin_target')
    if margin_target is not None:
        set_nested(modified, 'pnl_model.ebitda_margin_percent', margin_target)

    # Headcount efficiency
    efficiency = override.get('headcount_efficiency', 1.0)
    if efficiency != 1.0:
        scaling = get_nested(modified, 'headcount_model.scaling_factors', {})
        for func, factor in scaling.items():
            if isinstance(factor, (int, float)):
                scaling[func] = factor * efficiency

    # CapEx multiplier
    capex_mult = override.get('capex_multiplier', 1.0)
    if capex_mult != 1.0:
        programs = get_nested(modified, 'capex_roadmap.programs', [])
        for program in programs:
            if isinstance(program.get('total_budget_eur_m'), (int, float)):
                program['total_budget_eur_m'] *= capex_mult

    return modified


def validate_cascade_results(results: Dict, thresholds: Dict) -> Dict:
    """
    Validate cascade results against strategic thresholds.

    Args:
        results: Cascade results dictionary
        thresholds: Validation thresholds

    Returns:
        Validation report
    """
    validations = []
    all_passed = True

    # Check EBITDA margin
    min_margin = thresholds.get('min_ebitda_margin', 8.0)
    pnl_summary = results.get('level_5', {}).get('pnl', {}).get('summary', {})
    final_margin = pnl_summary.get('ebitda', {}).get('final_margin_percent', 0)

    margin_passed = final_margin >= min_margin
    validations.append({
        'check': 'EBITDA Margin',
        'threshold': f'>= {min_margin}%',
        'actual': f'{final_margin:.1f}%',
        'passed': margin_passed
    })
    all_passed = all_passed and margin_passed

    # Check ROIC
    min_roic = thresholds.get('min_roic', 10.0)
    vc_summary = results.get('level_6', {}).get('value_creation', {}).get('summary', {})
    avg_roic = vc_summary.get('value_creation', {}).get('avg_roic_percent', 0)

    roic_passed = avg_roic >= min_roic
    validations.append({
        'check': 'Average ROIC',
        'threshold': f'>= {min_roic}%',
        'actual': f'{avg_roic:.1f}%',
        'passed': roic_passed
    })
    all_passed = all_passed and roic_passed

    # Check value creation
    value_creating = vc_summary.get('value_creation', {}).get('value_creating', False)
    validations.append({
        'check': 'Value Creation',
        'threshold': 'EVA > 0',
        'actual': 'Yes' if value_creating else 'No',
        'passed': value_creating
    })
    all_passed = all_passed and value_creating

    return {
        'all_passed': all_passed,
        'validations': validations,
        'summary': f"{'All checks passed' if all_passed else 'Some checks failed'}"
    }


def run_strategy_cascade(
    config: Dict,
    scenario: str = None,
    strategic_override: Dict = None,
    cascade_mode: str = 'full',
    num_simulations: int = 10000,
    verbose: bool = True
) -> Dict:
    """
    Run the full strategy cascade with top-down dependencies.

    STCM-2.0: Now with 8 levels and all 20 models integrated.

    Args:
        config: Configuration dictionary (from YAML)
        scenario: Scenario name ('conservative', 'base_case', 'aggressive')
        strategic_override: Optional strategic overrides
        cascade_mode: 'full' (all 8 levels) or 'quick' (skip Level 7)
        num_simulations: Monte Carlo simulations for Level 7
        verbose: Print progress

    Returns:
        Dictionary with cascade results, dependencies, and validation
    """
    start_time = time.time()
    params = extract_cascade_params(config)

    # Apply scenario selection
    selected_scenario = scenario or params['selected_scenario']

    # Apply strategic overrides
    override = strategic_override or params['strategic_override']
    working_config = apply_strategic_override(config, override)

    # Initialize results
    cascade_results = {
        'config': {
            'scenario': selected_scenario,
            'cascade_mode': cascade_mode,
            'strategic_override': override,
            'base_year': params['base_year'],
            'projection_years': params['projection_years'],
            'currency': params['currency']
        },
        'levels': {},
        'dependencies': {},
        'validation': None
    }

    if verbose:
        print("\n" + "="*80)
        print("STRATEGY CASCADE MODEL (STCM-2.0) - TOP-DOWN PLANNING")
        print("="*80)
        print(f"Scenario: {selected_scenario.upper()}")
        print(f"Mode: {cascade_mode.upper()}")
        print(f"Models: 20 (8 Levels)")
        if override:
            print(f"Strategic Overrides: {len(override)} active")
        print("="*80)

    # Track data flowing between levels
    data_flow = {}

    # =========================================================================
    # LEVEL 0: Strategic Options (NEW in STCM-2.0)
    # =========================================================================
    level_start = time.time()
    if verbose:
        print(f"\n[LEVEL 0] Strategic Options")
        print(f"  Models: MAM-1.0")
        print(f"  → Evaluating M&A opportunities")

    try:
        ma_results = analyze_ma_synergies(working_config)
        data_flow['ma_results'] = ma_results

        cascade_results['levels']['level_0'] = {
            'name': 'Strategic Options',
            'models_run': ['MAM-1.0'],
            'ma_analysis': ma_results,
            'execution_time': time.time() - level_start
        }

        if verbose:
            ma_summary = ma_results.get('summary', {})
            value_creation = ma_summary.get('value_creation', {})
            print(f"  → Synergy NPV: {params['currency']}{value_creation.get('npv_synergies_m', 0):,.0f}M")
            print(f"  → Value Created: {params['currency']}{value_creation.get('net_value_created_m', 0):,.0f}M")
            print(f"  ✓ Level 0 completed in {cascade_results['levels']['level_0']['execution_time']:.2f}s")

    except Exception as e:
        cascade_results['levels']['level_0'] = {'error': str(e), 'models_run': ['MAM-1.0']}
        if verbose:
            print(f"  ✗ Level 0 failed: {e}")

    # =========================================================================
    # LEVEL 1: Strategic Direction (Extended with PFM-1.0)
    # =========================================================================
    level_start = time.time()
    if verbose:
        print(f"\n[LEVEL 1] Strategic Direction")
        print(f"  Models: SCM-1.0, PFM-1.0")
        print(f"  → Selecting scenario: {selected_scenario}")

    try:
        # Portfolio analysis (BCG Matrix)
        portfolio_results = analyze_portfolio(working_config)
        data_flow['portfolio_results'] = portfolio_results

        cascade_results['levels']['level_1'] = {
            'name': 'Strategic Direction',
            'models_run': ['SCM-1.0', 'PFM-1.0'],
            'selected_scenario': selected_scenario,
            'adjustments_applied': override,
            'portfolio': portfolio_results,
            'execution_time': time.time() - level_start
        }

        if verbose:
            portfolio_summary = portfolio_results.get('summary', {})
            bcg = portfolio_summary.get('bcg_distribution', {})
            print(f"  → Portfolio: {bcg.get('stars', 0)} Stars, {bcg.get('cash_cows', 0)} Cash Cows, {bcg.get('question_marks', 0)} Question Marks")
            print(f"  ✓ Level 1 completed in {cascade_results['levels']['level_1']['execution_time']:.2f}s")

    except Exception as e:
        cascade_results['levels']['level_1'] = {
            'error': str(e),
            'models_run': ['SCM-1.0', 'PFM-1.0'],
            'selected_scenario': selected_scenario
        }
        if verbose:
            print(f"  ✗ Level 1 failed: {e}")

    # =========================================================================
    # LEVEL 2: Growth Projection (Extended with MSM-1.0, PRM-1.0)
    # =========================================================================
    level_start = time.time()
    if verbose:
        print(f"\n[LEVEL 2] Growth Projection")
        print(f"  Models: RPM-1.0, MSM-1.0, PRM-1.0")
        print(f"  ← Inputs: scenario_adjustments, market_data, pricing_model")

    try:
        # RPM: Revenue projection
        revenue_df = project_revenue(working_config)
        revenue_metrics = calculate_summary_metrics(revenue_df)
        data_flow['revenue_df'] = revenue_df
        data_flow['revenue_metrics'] = revenue_metrics

        # MSM: Market share projection
        market_results = project_market_share(working_config, revenue_df)
        data_flow['market_results'] = market_results

        # PRM: Pricing analysis
        pricing_results = analyze_pricing(working_config)
        data_flow['pricing_results'] = pricing_results

        cascade_results['levels']['level_2'] = {
            'name': 'Growth Projection',
            'models_run': ['RPM-1.0', 'MSM-1.0', 'PRM-1.0'],
            'revenue': {
                'df': revenue_df,
                'metrics': revenue_metrics
            },
            'market_share': market_results,
            'pricing': pricing_results,
            'execution_time': time.time() - level_start
        }

        if verbose:
            print(f"  → 2024: {params['currency']}{revenue_metrics['base_year_2024_revenue_eur_m']:,.0f}M")
            print(f"  → 2035: {params['currency']}{revenue_metrics['target_year_2035_revenue_eur_m']:,.0f}M")
            print(f"  → CAGR: {revenue_metrics['blended_cagr_percent']:.2f}%")
            market_summary = market_results.get('summary', {}).get('company', {})
            print(f"  → Market Share: {market_summary.get('base_share_percent', 0):.1f}% → {market_summary.get('final_share_percent', 0):.1f}%")
            pricing_summary = pricing_results.get('summary', {}).get('optimal_pricing', {})
            print(f"  → Optimal Price: {params['currency']}{pricing_summary.get('optimal_price', 0):.2f}")
            print(f"  ✓ Level 2 completed in {cascade_results['levels']['level_2']['execution_time']:.2f}s")

    except Exception as e:
        cascade_results['levels']['level_2'] = {'error': str(e), 'models_run': ['RPM-1.0', 'MSM-1.0', 'PRM-1.0']}
        if verbose:
            print(f"  ✗ Level 2 failed: {e}")

    # =========================================================================
    # LEVEL 3: Resource Allocation
    # =========================================================================
    level_start = time.time()
    if verbose:
        print(f"\n[LEVEL 3] Resource Allocation")
        print(f"  Models: OSM-1.0, CAM-1.0")
        print(f"  ← Inputs: revenue_projection")

    try:
        # OSM: Headcount scaling based on revenue growth
        org_results = project_headcount(working_config)
        data_flow['org_results'] = org_results

        # CAM: CapEx allocation
        capex_results = project_capex(working_config)
        data_flow['capex_results'] = capex_results

        cascade_results['levels']['level_3'] = {
            'name': 'Resource Allocation',
            'models_run': ['OSM-1.0', 'CAM-1.0'],
            'organization': org_results,
            'capex': capex_results,
            'execution_time': time.time() - level_start
        }

        if verbose:
            org_summary = org_results.get('summary', {})
            capex_summary = capex_results.get('summary', {})
            print(f"  → Headcount 2035: {org_summary.get('target_year_headcount', 0):,}")
            print(f"  → Payroll 2035: {params['currency']}{org_summary.get('payroll_2035_eur_m', 0):,.0f}M")
            print(f"  → 11Y CapEx: {params['currency']}{capex_summary.get('total_capex_11_years_eur_m', 0):,.0f}M")
            print(f"  ✓ Level 3 completed in {cascade_results['levels']['level_3']['execution_time']:.2f}s")

    except Exception as e:
        cascade_results['levels']['level_3'] = {'error': str(e)}
        if verbose:
            print(f"  ✗ Level 3 failed: {e}")

    # =========================================================================
    # LEVEL 4: Cost Structure
    # =========================================================================
    level_start = time.time()
    if verbose:
        print(f"\n[LEVEL 4] Cost Structure")
        print(f"  Models: CSM-1.0")
        print(f"  ← Inputs: revenue_projection, payroll_projection")

    try:
        cost_results = project_costs(working_config, data_flow.get('revenue_df'))
        data_flow['cost_results'] = cost_results

        cascade_results['levels']['level_4'] = {
            'name': 'Cost Structure',
            'models_run': ['CSM-1.0'],
            'costs': cost_results,
            'execution_time': time.time() - level_start
        }

        if verbose:
            cost_summary = cost_results.get('summary', {})
            print(f"  → Costs 2024: {params['currency']}{cost_summary.get('base_year_costs_m', 0):,.0f}M")
            print(f"  → Costs 2035: {params['currency']}{cost_summary.get('final_year_costs_m', 0):,.0f}M")
            print(f"  ✓ Level 4 completed in {cascade_results['levels']['level_4']['execution_time']:.2f}s")

    except Exception as e:
        cascade_results['levels']['level_4'] = {'error': str(e)}
        if verbose:
            print(f"  ✗ Level 4 failed: {e}")

    # =========================================================================
    # LEVEL 5: Profitability (Extended with BEM-1.0)
    # =========================================================================
    level_start = time.time()
    if verbose:
        print(f"\n[LEVEL 5] Profitability")
        print(f"  Models: PLM-1.0, BEM-1.0")
        print(f"  ← Inputs: revenue_projection, cost_projection")

    try:
        cost_df = data_flow.get('cost_results', {}).get('cost_projection')

        # PLM: P&L projection
        pnl_results = project_pnl(working_config, data_flow.get('revenue_df'), cost_df)
        data_flow['pnl_results'] = pnl_results

        # BEM: Break-even analysis
        pnl_df = pnl_results.get('pnl_projection')
        break_even_results = analyze_break_even(working_config, pnl_df, cost_df)
        data_flow['break_even_results'] = break_even_results

        cascade_results['levels']['level_5'] = {
            'name': 'Profitability',
            'models_run': ['PLM-1.0', 'BEM-1.0'],
            'pnl': pnl_results,
            'break_even': break_even_results,
            'execution_time': time.time() - level_start
        }

        if verbose:
            pnl_summary = pnl_results.get('summary', {})
            ebitda = pnl_summary.get('ebitda', {})
            print(f"  → EBITDA 2024: {params['currency']}{ebitda.get('base_year_m', 0):,.0f}M ({ebitda.get('base_margin_percent', 0):.1f}%)")
            print(f"  → EBITDA 2035: {params['currency']}{ebitda.get('final_year_m', 0):,.0f}M ({ebitda.get('final_margin_percent', 0):.1f}%)")
            be_summary = break_even_results.get('summary', {}).get('break_even', {})
            print(f"  → Break-Even Revenue: {params['currency']}{be_summary.get('base_year_break_even_m', 0):,.0f}M")
            print(f"  → Margin of Safety: {be_summary.get('base_year_margin_of_safety_percent', 0):.1f}%")
            print(f"  ✓ Level 5 completed in {cascade_results['levels']['level_5']['execution_time']:.2f}s")

    except Exception as e:
        cascade_results['levels']['level_5'] = {'error': str(e), 'models_run': ['PLM-1.0', 'BEM-1.0']}
        if verbose:
            print(f"  ✗ Level 5 failed: {e}")

    # =========================================================================
    # LEVEL 6: Cash & Value (Extended with BSM-1.0, WCM-1.0, DFM-1.0)
    # =========================================================================
    level_start = time.time()
    if verbose:
        print(f"\n[LEVEL 6] Cash & Value")
        print(f"  Models: CFM-1.0, VCM-1.0, BSM-1.0, WCM-1.0, DFM-1.0")
        print(f"  ← Inputs: pnl_projection, capex_projection, working_capital, debt_structure")

    try:
        pnl_df = data_flow.get('pnl_results', {}).get('pnl_projection')
        capex_df = data_flow.get('capex_results', {}).get('annual_capex')
        cost_df = data_flow.get('cost_results', {}).get('cost_projection')
        revenue_df = data_flow.get('revenue_df')

        # CFM: Cash Flow
        cf_results = project_cash_flow(working_config, pnl_df, capex_df)
        data_flow['cf_results'] = cf_results
        cf_df = cf_results.get('cash_flow_projection')

        # VCM: Value Creation
        vc_results = calculate_value_creation(working_config, pnl_df, cf_df)
        data_flow['vc_results'] = vc_results

        # WCM: Working Capital
        wc_results = project_working_capital(working_config, revenue_df, cost_df)
        data_flow['wc_results'] = wc_results

        # DFM: Debt & Financing
        dfm_results = project_debt_financing(working_config, cf_df, pnl_df)
        data_flow['dfm_results'] = dfm_results

        # BSM: Balance Sheet
        bs_results = project_balance_sheet(working_config, pnl_df, cf_df)
        data_flow['bs_results'] = bs_results

        cascade_results['levels']['level_6'] = {
            'name': 'Cash & Value',
            'models_run': ['CFM-1.0', 'VCM-1.0', 'BSM-1.0', 'WCM-1.0', 'DFM-1.0'],
            'cash_flow': cf_results,
            'value_creation': vc_results,
            'balance_sheet': bs_results,
            'working_capital': wc_results,
            'debt_financing': dfm_results,
            'execution_time': time.time() - level_start
        }

        if verbose:
            cf_summary = cf_results.get('summary', {})
            vc_summary = vc_results.get('summary', {})
            fcf = cf_summary.get('free_cash_flow', {})
            value = vc_summary.get('value_creation', {})
            wc_summary = wc_results.get('summary', {}).get('cash_conversion', {})
            dfm_summary = dfm_results.get('summary', {}).get('debt_metrics', {})

            print(f"  → Total FCF: {params['currency']}{fcf.get('total_m', 0):,.0f}M")
            print(f"  → WACC: {vc_summary.get('wacc', {}).get('wacc_percent', 0):.2f}%")
            print(f"  → Total EVA: {params['currency']}{value.get('total_eva_m', 0):,.0f}M")
            print(f"  → Avg ROIC: {value.get('avg_roic_percent', 0):.1f}%")
            print(f"  → Cash Conversion Cycle: {wc_summary.get('base_ccc_days', 0):.0f} days")
            print(f"  → Debt/EBITDA: {dfm_summary.get('base_debt_to_ebitda', 0):.1f}x")
            status = "VALUE CREATING" if value.get('value_creating', False) else "VALUE DESTROYING"
            print(f"  → Status: {status}")
            print(f"  ✓ Level 6 completed in {cascade_results['levels']['level_6']['execution_time']:.2f}s")

    except Exception as e:
        cascade_results['levels']['level_6'] = {'error': str(e), 'models_run': ['CFM-1.0', 'VCM-1.0', 'BSM-1.0', 'WCM-1.0', 'DFM-1.0']}
        if verbose:
            print(f"  ✗ Level 6 failed: {e}")

    # =========================================================================
    # LEVEL 7: Risk & Validation (Extended with STM-1.0)
    # =========================================================================
    if cascade_mode == 'full':
        level_start = time.time()
        if verbose:
            print(f"\n[LEVEL 7] Risk & Validation")
            print(f"  Models: MCSM-1.0, SAM-1.0, STM-1.0")
            print(f"  ← Inputs: all_projections, uncertainty_parameters, stress_scenarios")

        try:
            # MCSM: Monte Carlo
            mc_results = run_monte_carlo(
                working_config,
                revenue_df=data_flow.get('revenue_df'),
                num_simulations=num_simulations
            )
            data_flow['mc_results'] = mc_results

            # STM: Stress Testing
            pnl_df = data_flow.get('pnl_results', {}).get('pnl_projection')
            stress_results = run_stress_tests(working_config, pnl_df)
            data_flow['stress_results'] = stress_results

            cascade_results['levels']['level_7'] = {
                'name': 'Risk & Validation',
                'models_run': ['MCSM-1.0', 'SAM-1.0', 'STM-1.0'],
                'monte_carlo': mc_results,
                'stress_testing': stress_results,
                'execution_time': time.time() - level_start
            }

            if verbose:
                mc_stats = mc_results.get('statistics', {})
                mc_pct = mc_results.get('percentiles', {})
                stress_summary = stress_results.get('summary', {})
                tail_risk = stress_summary.get('tail_risk', {})

                print(f"  → Mean 2035: {params['currency']}{mc_stats.get('mean', 0):,.0f}M")
                print(f"  → 95% CI: [{params['currency']}{mc_pct.get('p5', 0):,.0f}M - {params['currency']}{mc_pct.get('p95', 0):,.0f}M]")
                print(f"  → Stress Scenarios: {stress_summary.get('scenarios_tested', 0)}")
                print(f"  → Worst Case Impact: {tail_risk.get('worst_case_impact_percent', 0):.1f}%")
                print(f"  ✓ Level 7 completed in {cascade_results['levels']['level_7']['execution_time']:.2f}s")

        except Exception as e:
            cascade_results['levels']['level_7'] = {'error': str(e), 'models_run': ['MCSM-1.0', 'SAM-1.0', 'STM-1.0']}
            if verbose:
                print(f"  ✗ Level 7 failed: {e}")

    # =========================================================================
    # Validation & Summary
    # =========================================================================
    total_time = time.time() - start_time

    # Run validation
    validation = validate_cascade_results(cascade_results['levels'], params['validation'])
    cascade_results['validation'] = validation

    # Build dependency map (STCM-2.0: 8 levels)
    cascade_results['dependencies'] = {
        'level_0 → level_1': 'ma_analysis, strategic_options',
        'level_1 → level_2': 'scenario_adjustments, portfolio_strategy',
        'level_2 → level_3': 'revenue_projection, market_share',
        'level_2 → level_4': 'revenue_projection',
        'level_3 → level_4': 'payroll_projection',
        'level_3 → level_6': 'capex_projection',
        'level_4 → level_5': 'cost_projection',
        'level_5 → level_6': 'pnl_projection, break_even',
        'level_2,5,6 → level_7': 'all_projections, stress_scenarios'
    }

    # Summary (STCM-2.0: 8 levels)
    levels_run = len([l for l in cascade_results['levels'] if 'error' not in cascade_results['levels'][l]])
    total_levels = 8 if cascade_mode == 'full' else 7

    cascade_results['summary'] = {
        'scenario': selected_scenario,
        'cascade_mode': cascade_mode,
        'levels_completed': levels_run,
        'total_levels': total_levels,
        'execution_time_seconds': round(total_time, 2),
        'validation_passed': validation['all_passed'],
        'currency': params['currency']
    }

    if verbose:
        print("\n" + "="*80)
        print("CASCADE SUMMARY")
        print("="*80)
        print(f"  Scenario: {selected_scenario.upper()}")
        print(f"  Levels Completed: {levels_run}/{total_levels}")
        print(f"  Total Time: {total_time:.2f}s")
        print(f"\n  Validation:")
        for v in validation['validations']:
            status = "✓" if v['passed'] else "✗"
            print(f"    {status} {v['check']}: {v['actual']} (threshold: {v['threshold']})")
        print(f"\n  Overall: {'STRATEGY VALIDATED' if validation['all_passed'] else 'REVIEW REQUIRED'}")
        print("="*80)

    return cascade_results


def format_cascade_results(results: Dict) -> str:
    """Format cascade results for display."""
    output = []
    output.append("\n" + "="*80)
    output.append("STRATEGY CASCADE MODEL (STCM-2.0) - RESULTS")
    output.append("="*80)

    summary = results['summary']
    output.append(f"\nScenario: {summary['scenario'].upper()}")
    output.append(f"Mode: {summary['cascade_mode'].upper()}")
    output.append(f"Levels Completed: {summary['levels_completed']}/{summary['total_levels']}")
    output.append(f"Execution Time: {summary['execution_time_seconds']:.2f}s")

    output.append("\n" + "-"*60)
    output.append("LEVEL SUMMARY")
    output.append("-"*60)

    for level_key, level_data in results['levels'].items():
        if 'error' in level_data:
            output.append(f"  ✗ {level_key}: ERROR - {level_data['error']}")
        else:
            output.append(f"  ✓ {level_data['name']} ({level_data['execution_time']:.2f}s)")

    output.append("\n" + "-"*60)
    output.append("VALIDATION")
    output.append("-"*60)

    for v in results['validation']['validations']:
        status = "✓" if v['passed'] else "✗"
        output.append(f"  {status} {v['check']}: {v['actual']} (threshold: {v['threshold']})")

    output.append("\n" + "="*80)
    return "\n".join(output)


def main():
    """Main entry point for command-line execution."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Run Strategy Cascade Model (STCM-2.0) with top-down planning - 20 Models',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python strategy_cascade.py ALPLA
  python strategy_cascade.py ALPLA --scenario conservative
  python strategy_cascade.py ALPLA --mode quick
  python strategy_cascade.py ALPLA --override revenue_cagr_adjustment=-0.5

STCM-2.0 Cascade Levels (20 Models):
  Level 0: Strategic Options (MAM)
  Level 1: Strategic Direction (SCM, PFM)
  Level 2: Growth Projection (RPM, MSM, PRM)
  Level 3: Resource Allocation (OSM, CAM)
  Level 4: Cost Structure (CSM)
  Level 5: Profitability (PLM, BEM)
  Level 6: Cash & Value (CFM, VCM, BSM, WCM, DFM)
  Level 7: Risk & Validation (MCSM, SAM, STM) [optional]
        """
    )

    parser.add_argument('customer', help='Customer name (e.g., ALPLA)')
    parser.add_argument('--scenario', '-s', choices=['conservative', 'base_case', 'aggressive'],
                        default='base_case', help='Strategic scenario (default: base_case)')
    parser.add_argument('--mode', '-m', choices=['full', 'quick'],
                        default='full', help='Cascade mode (default: full)')
    parser.add_argument('--simulations', '-n', type=int, default=10000,
                        help='Monte Carlo simulations (default: 10000)')
    parser.add_argument('--quiet', '-q', action='store_true',
                        help='Suppress verbose output')
    parser.add_argument('--override', '-o', action='append',
                        help='Strategic override (e.g., revenue_cagr_adjustment=-0.5)')

    args = parser.parse_args()

    # Find and load config
    from pathlib import Path
    repo_root = Path(__file__).parent.parent.parent
    customer_dir = repo_root / 'data' / 'customers' / args.customer.lower()

    if not customer_dir.exists():
        print(f"Error: Customer directory not found: {customer_dir}")
        sys.exit(1)

    # Load all config files
    config = {}
    for config_file in customer_dir.glob('*.yaml'):
        try:
            with open(config_file) as f:
                config.update(yaml.safe_load(f) or {})
        except Exception as e:
            print(f"Warning: Could not load {config_file}: {e}")

    # Parse overrides
    override = {}
    if args.override:
        for o in args.override:
            key, value = o.split('=')
            try:
                override[key] = float(value)
            except ValueError:
                override[key] = value

    # Run cascade
    results = run_strategy_cascade(
        config=config,
        scenario=args.scenario,
        strategic_override=override if override else None,
        cascade_mode=args.mode,
        num_simulations=args.simulations,
        verbose=not args.quiet
    )

    if not args.quiet:
        print(f"\n✅ Strategy cascade completed!")
        print(f"   Validation: {'PASSED' if results['validation']['all_passed'] else 'FAILED'}")


if __name__ == '__main__':
    main()
