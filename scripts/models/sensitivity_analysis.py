#!/usr/bin/env python3
"""
Sensitivity Analysis Model (SAM-1.0)
Systematic parameter sensitivity testing for strategic models.

Usage:
    from sensitivity_analysis import run_sensitivity_analysis
    result = run_sensitivity_analysis(config, base_results)

Model Version: 1.0.0
Implementation Date: 2026-01-16

FULLY GENERIC: All parameters from config, no hardcoded defaults.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Any, Callable
import yaml
import sys
from pathlib import Path
from copy import deepcopy


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


def extract_sensitivity_params(config: Dict) -> Dict:
    """
    Extract sensitivity analysis parameters from configuration.

    Expected config structure:
    ```yaml
    sensitivity_analysis:
      # Parameters to test
      parameters:
        - name: "europe_cagr"
          path: "strategic_assumptions.regional_growth_rates.europe.cagr"
          base_value: 2.5
          range_pct: 40  # ±40% of base value
          steps: 5  # number of test points

        - name: "apac_cagr"
          path: "strategic_assumptions.regional_growth_rates.apac.cagr"
          base_value: 8.5
          range_pct: 30
          steps: 5

        - name: "ebitda_margin"
          path: "pnl_model.ebitda_margin_percent"
          base_value: 12
          range_absolute: 4  # ±4pp absolute
          steps: 5

      # Output metrics to track
      output_metrics:
        - name: "revenue_2035"
          description: "Total Revenue in 2035 (€M)"
        - name: "ebitda_2035"
          description: "EBITDA in 2035 (€M)"
        - name: "net_income_2035"
          description: "Net Income in 2035 (€M)"

      # Scenario combinations (optional)
      scenarios:
        - name: "conservative"
          description: "All growth rates -20%"
          adjustments:
            europe_cagr: -20%
            apac_cagr: -20%

        - name: "aggressive"
          description: "All growth rates +20%"
          adjustments:
            europe_cagr: +20%
            apac_cagr: +20%
    ```
    """
    sens_config = config.get('sensitivity_analysis', {})

    params = {
        'parameters': sens_config.get('parameters', []),
        'output_metrics': sens_config.get('output_metrics', []),
        'scenarios': sens_config.get('scenarios', []),
        'default_range_pct': sens_config.get('default_range_pct', 20),
        'default_steps': sens_config.get('default_steps', 5)
    }

    return params


def get_nested_value(config: Dict, path: str) -> Any:
    """
    Get a value from nested config using dot notation path.

    Args:
        config: Configuration dictionary
        path: Dot-separated path (e.g., "strategic_assumptions.regional_growth_rates.europe.cagr")

    Returns:
        Value at the path, or None if not found
    """
    keys = path.split('.')
    value = config

    for key in keys:
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            return None

    return value


def set_nested_value(config: Dict, path: str, value: Any) -> Dict:
    """
    Set a value in nested config using dot notation path.

    Args:
        config: Configuration dictionary (will be modified in place)
        path: Dot-separated path
        value: Value to set

    Returns:
        Modified config
    """
    keys = path.split('.')
    current = config

    for key in keys[:-1]:
        if key not in current:
            current[key] = {}
        current = current[key]

    current[keys[-1]] = value
    return config


def generate_test_values(
    base_value: float,
    range_pct: Optional[float] = None,
    range_absolute: Optional[float] = None,
    steps: int = 5,
    min_value: Optional[float] = None,
    max_value: Optional[float] = None
) -> np.ndarray:
    """
    Generate test values for sensitivity analysis.

    Args:
        base_value: Base/center value
        range_pct: Percentage range (±range_pct% of base)
        range_absolute: Absolute range (±range_absolute)
        steps: Number of test points
        min_value: Minimum allowed value
        max_value: Maximum allowed value

    Returns:
        Array of test values
    """
    if range_absolute is not None:
        low = base_value - range_absolute
        high = base_value + range_absolute
    elif range_pct is not None:
        delta = base_value * (range_pct / 100)
        low = base_value - delta
        high = base_value + delta
    else:
        # Default: ±20%
        delta = base_value * 0.2
        low = base_value - delta
        high = base_value + delta

    # Apply bounds
    if min_value is not None:
        low = max(low, min_value)
    if max_value is not None:
        high = min(high, max_value)

    return np.linspace(low, high, steps)


def run_single_parameter_sensitivity(
    config: Dict,
    param_config: Dict,
    model_runner: Callable,
    output_extractor: Callable,
    default_range_pct: float = 20,
    default_steps: int = 5
) -> Dict:
    """
    Run sensitivity analysis for a single parameter.

    Args:
        config: Base configuration
        param_config: Parameter configuration
        model_runner: Function that runs models and returns results
        output_extractor: Function that extracts output metrics from results
        default_range_pct: Default percentage range
        default_steps: Default number of steps

    Returns:
        Dictionary with sensitivity results for this parameter
    """
    param_name = param_config.get('name', 'unknown')
    param_path = param_config.get('path', '')
    base_value = param_config.get('base_value')
    range_pct = param_config.get('range_pct', default_range_pct)
    range_absolute = param_config.get('range_absolute')
    steps = param_config.get('steps', default_steps)
    min_value = param_config.get('min_value')
    max_value = param_config.get('max_value')

    # Get base value from config if not specified
    if base_value is None:
        base_value = get_nested_value(config, param_path)
        if base_value is None:
            print(f"WARNING: Could not find base value for {param_name} at {param_path}")
            return None

    # Generate test values
    test_values = generate_test_values(
        base_value=float(base_value),
        range_pct=range_pct,
        range_absolute=range_absolute,
        steps=steps,
        min_value=min_value,
        max_value=max_value
    )

    # Run model for each test value
    results = []
    for test_value in test_values:
        # Create modified config
        test_config = deepcopy(config)
        set_nested_value(test_config, param_path, float(test_value))

        # Run model
        try:
            model_results = model_runner(test_config)
            outputs = output_extractor(model_results)
            results.append({
                'value': float(test_value),
                'pct_change': ((test_value - base_value) / base_value * 100) if base_value != 0 else 0,
                **outputs
            })
        except Exception as e:
            print(f"WARNING: Model run failed for {param_name}={test_value}: {e}")
            results.append({
                'value': float(test_value),
                'pct_change': ((test_value - base_value) / base_value * 100) if base_value != 0 else 0,
                'error': str(e)
            })

    # Calculate elasticities (sensitivity coefficients)
    df = pd.DataFrame(results)
    elasticities = {}

    # Get base results
    base_idx = len(results) // 2  # Middle value should be base
    if 'error' not in df.columns or pd.isna(df.loc[base_idx].get('error')):
        base_outputs = {k: v for k, v in results[base_idx].items()
                       if k not in ['value', 'pct_change', 'error']}

        for metric in base_outputs.keys():
            if metric in df.columns and df[metric].notna().sum() >= 2:
                # Elasticity = % change in output / % change in input
                valid_mask = df[metric].notna() & df['pct_change'].notna()
                if valid_mask.sum() >= 2:
                    # Use regression for elasticity
                    x = df.loc[valid_mask, 'pct_change'].values
                    y = ((df.loc[valid_mask, metric] - base_outputs[metric]) / base_outputs[metric] * 100).values
                    if len(x) > 1 and np.std(x) > 0:
                        elasticities[metric] = np.polyfit(x, y, 1)[0]

    return {
        'parameter': param_name,
        'path': param_path,
        'base_value': float(base_value),
        'test_values': test_values.tolist(),
        'results': results,
        'elasticities': elasticities,
        'df': df
    }


def run_tornado_analysis(
    config: Dict,
    sensitivity_results: List[Dict],
    target_metric: str
) -> pd.DataFrame:
    """
    Generate tornado diagram data showing parameter impact ranking.

    Args:
        config: Configuration
        sensitivity_results: Results from single parameter sensitivity
        target_metric: Metric to analyze

    Returns:
        DataFrame sorted by impact magnitude
    """
    tornado_data = []

    for param_result in sensitivity_results:
        if param_result is None:
            continue

        df = param_result['df']
        if target_metric not in df.columns:
            continue

        values = df[target_metric].dropna()
        if len(values) < 2:
            continue

        # Get min and max values
        min_val = values.min()
        max_val = values.max()
        base_val = values.iloc[len(values)//2]  # Middle value as base

        tornado_data.append({
            'parameter': param_result['parameter'],
            'low_value': min_val,
            'base_value': base_val,
            'high_value': max_val,
            'range': max_val - min_val,
            'elasticity': param_result['elasticities'].get(target_metric, 0)
        })

    # Sort by range (impact)
    tornado_df = pd.DataFrame(tornado_data)
    if not tornado_df.empty:
        tornado_df = tornado_df.sort_values('range', ascending=False)

    return tornado_df


def run_scenario_analysis(
    config: Dict,
    scenarios: List[Dict],
    parameters: List[Dict],
    model_runner: Callable,
    output_extractor: Callable
) -> List[Dict]:
    """
    Run predefined scenario combinations.

    Args:
        config: Base configuration
        scenarios: List of scenario definitions
        parameters: List of parameter definitions
        model_runner: Function that runs models
        output_extractor: Function that extracts outputs

    Returns:
        List of scenario results
    """
    # Build parameter lookup
    param_lookup = {p['name']: p for p in parameters}

    results = []

    for scenario in scenarios:
        scenario_name = scenario.get('name', 'unknown')
        description = scenario.get('description', '')
        adjustments = scenario.get('adjustments', {})

        # Apply adjustments
        scenario_config = deepcopy(config)

        for param_name, adjustment in adjustments.items():
            if param_name not in param_lookup:
                print(f"WARNING: Unknown parameter {param_name} in scenario {scenario_name}")
                continue

            param = param_lookup[param_name]
            base_value = param.get('base_value') or get_nested_value(config, param['path'])

            if base_value is None:
                continue

            # Parse adjustment
            if isinstance(adjustment, str):
                if adjustment.endswith('%'):
                    pct = float(adjustment[:-1])
                    new_value = base_value * (1 + pct/100)
                elif adjustment.endswith('pp'):
                    pp = float(adjustment[:-2])
                    new_value = base_value + pp
                else:
                    new_value = float(adjustment)
            else:
                new_value = adjustment

            set_nested_value(scenario_config, param['path'], new_value)

        # Run model
        try:
            model_results = model_runner(scenario_config)
            outputs = output_extractor(model_results)
            results.append({
                'scenario': scenario_name,
                'description': description,
                **outputs
            })
        except Exception as e:
            print(f"WARNING: Scenario {scenario_name} failed: {e}")
            results.append({
                'scenario': scenario_name,
                'description': description,
                'error': str(e)
            })

    return results


def run_sensitivity_analysis(
    config: Dict,
    model_runner: Callable,
    output_extractor: Callable,
    custom_parameters: Optional[List[Dict]] = None,
    custom_metrics: Optional[List[str]] = None
) -> Dict:
    """
    Main function: Run comprehensive sensitivity analysis.

    Args:
        config: Configuration dictionary (from YAML)
        model_runner: Function that takes config and returns model results
        output_extractor: Function that extracts metrics from model results
        custom_parameters: Override parameters from config
        custom_metrics: Override metrics to track

    Returns:
        Dictionary with:
        - single_parameter: Results for each parameter
        - tornado: Tornado diagram data for each metric
        - scenarios: Scenario analysis results
        - summary: Summary statistics
    """
    params = extract_sensitivity_params(config)

    parameters = custom_parameters or params['parameters']
    output_metrics = custom_metrics or [m['name'] for m in params['output_metrics']]
    scenarios = params['scenarios']

    if not parameters:
        print("WARNING: No sensitivity parameters defined in config")
        return {'error': 'No parameters defined'}

    # Run single parameter sensitivity
    print("Running single-parameter sensitivity analysis...")
    single_param_results = []
    for i, param_config in enumerate(parameters):
        print(f"  [{i+1}/{len(parameters)}] Testing {param_config.get('name', 'unknown')}...")
        result = run_single_parameter_sensitivity(
            config=config,
            param_config=param_config,
            model_runner=model_runner,
            output_extractor=output_extractor,
            default_range_pct=params['default_range_pct'],
            default_steps=params['default_steps']
        )
        if result:
            single_param_results.append(result)

    # Generate tornado diagrams
    print("Generating tornado analysis...")
    tornado_results = {}
    for metric in output_metrics:
        tornado_df = run_tornado_analysis(config, single_param_results, metric)
        if not tornado_df.empty:
            tornado_results[metric] = tornado_df

    # Run scenario analysis
    scenario_results = []
    if scenarios:
        print("Running scenario analysis...")
        scenario_results = run_scenario_analysis(
            config=config,
            scenarios=scenarios,
            parameters=parameters,
            model_runner=model_runner,
            output_extractor=output_extractor
        )

    # Summary
    summary = {
        'num_parameters': len(single_param_results),
        'num_scenarios': len(scenario_results),
        'metrics_analyzed': output_metrics,
        'top_drivers': {}
    }

    # Identify top 3 drivers for each metric
    for metric, tornado_df in tornado_results.items():
        if len(tornado_df) > 0:
            summary['top_drivers'][metric] = tornado_df.head(3)['parameter'].tolist()

    return {
        'single_parameter': single_param_results,
        'tornado': tornado_results,
        'scenarios': scenario_results,
        'summary': summary,
        'params': params
    }


def format_results(results: Dict) -> str:
    """Format sensitivity analysis results for display."""
    output = []
    output.append("\n" + "="*80)
    output.append("SENSITIVITY ANALYSIS MODEL (SAM-1.0) - RESULTS")
    output.append("="*80)

    summary = results.get('summary', {})

    output.append("\n[1] ANALYSIS SUMMARY")
    output.append("-" * 60)
    output.append(f"  Parameters Tested: {summary.get('num_parameters', 0)}")
    output.append(f"  Scenarios Analyzed: {summary.get('num_scenarios', 0)}")
    output.append(f"  Metrics Tracked: {', '.join(summary.get('metrics_analyzed', []))}")

    # Top Drivers
    output.append("\n[2] TOP SENSITIVITY DRIVERS")
    output.append("-" * 60)
    top_drivers = summary.get('top_drivers', {})
    for metric, drivers in top_drivers.items():
        output.append(f"\n  {metric}:")
        for i, driver in enumerate(drivers, 1):
            output.append(f"    {i}. {driver}")

    # Tornado Analysis
    output.append("\n[3] TORNADO ANALYSIS (by metric)")
    output.append("-" * 60)
    tornado = results.get('tornado', {})
    for metric, df in tornado.items():
        output.append(f"\n  {metric}:")
        if len(df) > 0:
            for _, row in df.head(5).iterrows():
                output.append(f"    {row['parameter']:20s} | Range: {row['range']:,.1f} | "
                            f"Low: {row['low_value']:,.1f} → High: {row['high_value']:,.1f}")

    # Scenario Results
    scenarios = results.get('scenarios', [])
    if scenarios:
        output.append("\n[4] SCENARIO ANALYSIS")
        output.append("-" * 60)
        for scenario in scenarios:
            output.append(f"\n  {scenario['scenario']}: {scenario.get('description', '')}")
            for key, value in scenario.items():
                if key not in ['scenario', 'description', 'error']:
                    if isinstance(value, (int, float)):
                        output.append(f"    {key}: {value:,.1f}")

    # Single Parameter Details (first 3)
    output.append("\n[5] PARAMETER SENSITIVITY DETAILS (top 3)")
    output.append("-" * 60)
    single_params = results.get('single_parameter', [])[:3]
    for param in single_params:
        output.append(f"\n  {param['parameter']}:")
        output.append(f"    Base Value: {param['base_value']:.2f}")
        output.append(f"    Test Range: [{min(param['test_values']):.2f} - {max(param['test_values']):.2f}]")
        if param['elasticities']:
            output.append("    Elasticities:")
            for metric, elast in param['elasticities'].items():
                output.append(f"      {metric}: {elast:.3f}")

    output.append("\n" + "="*80)
    return "\n".join(output)


# Default model runner and output extractor for standalone use
def default_model_runner(config: Dict) -> Dict:
    """
    Default model runner using the v1.5 model suite.
    """
    # Import models
    try:
        from revenue_projection import project_revenue
        from cost_structure import project_costs
        from profit_loss import project_pnl
    except ImportError:
        # Try relative import
        sys.path.insert(0, str(Path(__file__).parent))
        from revenue_projection import project_revenue
        from cost_structure import project_costs
        from profit_loss import project_pnl

    results = {}

    # Run revenue model
    try:
        revenue_df = project_revenue(config)
        results['revenue'] = revenue_df
    except Exception as e:
        results['revenue_error'] = str(e)

    # Run cost model
    try:
        cost_results = project_costs(config, results.get('revenue'))
        results['costs'] = cost_results
    except Exception as e:
        results['cost_error'] = str(e)

    # Run P&L model
    try:
        pnl_results = project_pnl(
            config,
            results.get('revenue'),
            results.get('costs', {}).get('cost_projection')
        )
        results['pnl'] = pnl_results
    except Exception as e:
        results['pnl_error'] = str(e)

    return results


def default_output_extractor(model_results: Dict) -> Dict:
    """
    Default output extractor for v1.5 model suite.
    """
    outputs = {}

    # Extract revenue metrics
    revenue_df = model_results.get('revenue')
    if revenue_df is not None and 'Total' in revenue_df.columns:
        final_row = revenue_df[revenue_df['Year'] == revenue_df['Year'].max()].iloc[0]
        outputs['revenue_2035'] = float(final_row['Total'])

    # Extract P&L metrics
    pnl = model_results.get('pnl', {})
    if pnl and 'pnl_projection' in pnl:
        pnl_df = pnl['pnl_projection']
        final_row = pnl_df[pnl_df['Year'] == pnl_df['Year'].max()].iloc[0]
        outputs['ebitda_2035'] = float(final_row.get('EBITDA', 0))
        outputs['net_income_2035'] = float(final_row.get('Net_Income', 0))
        outputs['ebitda_margin_2035'] = float(final_row.get('EBITDA_Margin_%', 0))

    return outputs


def main():
    """Main entry point for command-line execution."""
    if len(sys.argv) < 2:
        print("Usage: python sensitivity_analysis.py <config_file.yaml>")
        print("\nThe config file should contain a 'sensitivity_analysis' section with:")
        print("  - parameters: List of parameters to test")
        print("  - output_metrics: List of metrics to track")
        print("  - scenarios: Optional predefined scenarios")
        sys.exit(1)

    config_file = sys.argv[1]

    print(f"Loading configuration: {config_file}")
    config = load_configuration(config_file)

    print("Running sensitivity analysis...")
    results = run_sensitivity_analysis(
        config=config,
        model_runner=default_model_runner,
        output_extractor=default_output_extractor
    )

    print(format_results(results))


if __name__ == '__main__':
    main()
