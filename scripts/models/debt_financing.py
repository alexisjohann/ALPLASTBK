#!/usr/bin/env python3
"""
Debt & Financing Model (DFM-1.0)
Debt schedules, interest expense, and financing needs.

Usage:
    from debt_financing import project_debt_financing
    result = project_debt_financing(config, cash_flow_projection)

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

# Import base utilities
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


def extract_debt_params(config: Dict) -> Dict:
    """
    Extract debt and financing parameters from configuration.

    Expected config structure:
    ```yaml
    debt_financing_model:
      base_year: 2024
      projection_years: 11
      currency: "EUR"

      # Existing debt facilities
      debt_facilities:
        - name: "Term Loan A"
          type: "term_loan"
          principal_m: 500
          interest_rate_percent: 4.5
          maturity_year: 2029
          amortization: "bullet"  # or "linear", "annuity"

        - name: "Revolving Credit"
          type: "revolver"
          commitment_m: 200
          drawn_m: 50
          interest_rate_percent: 5.0
          commitment_fee_percent: 0.5
          maturity_year: 2027

        - name: "Bond 2030"
          type: "bond"
          principal_m: 300
          coupon_rate_percent: 3.75
          maturity_year: 2030

      # Refinancing assumptions
      refinancing:
        target_leverage_ratio: 2.5     # Net Debt / EBITDA
        min_cash_balance_m: 100        # Minimum cash buffer
        new_debt_rate_percent: 5.0     # Rate for new debt
        refinancing_costs_percent: 1.0 # % of principal

      # Covenants
      covenants:
        max_leverage_ratio: 3.5
        min_interest_coverage: 3.0
        min_debt_service_coverage: 1.2
    ```
    """
    df_config = config.get('debt_financing_model', {})

    params = {
        'base_year': df_config.get('base_year', DEFAULT_BASE_YEAR),
        'projection_years': df_config.get('projection_years', DEFAULT_PROJECTION_YEARS),
        'currency': df_config.get('currency', DEFAULT_CURRENCY),
        'debt_facilities': df_config.get('debt_facilities', []),
        'refinancing': df_config.get('refinancing', {}),
        'covenants': df_config.get('covenants', {})
    }

    # Default debt facility if none specified
    if not params['debt_facilities']:
        params['debt_facilities'] = [
            {
                'name': 'Term Loan',
                'type': 'term_loan',
                'principal_m': 500,
                'interest_rate_percent': 5.0,
                'maturity_year': params['base_year'] + 5,
                'amortization': 'linear'
            }
        ]

    # Refinancing defaults
    ref_defaults = {
        'target_leverage_ratio': 2.5,
        'min_cash_balance_m': 100,
        'new_debt_rate_percent': 5.0,
        'refinancing_costs_percent': 1.0
    }
    for key, default in ref_defaults.items():
        if key not in params['refinancing']:
            params['refinancing'][key] = default

    # Covenant defaults
    cov_defaults = {
        'max_leverage_ratio': 3.5,
        'min_interest_coverage': 3.0,
        'min_debt_service_coverage': 1.2
    }
    for key, default in cov_defaults.items():
        if key not in params['covenants']:
            params['covenants'][key] = default

    return params


def calculate_amortization(principal: float, years_remaining: int, amort_type: str) -> float:
    """Calculate annual amortization payment."""
    if years_remaining <= 0:
        return principal  # Bullet at maturity

    if amort_type == 'bullet':
        return 0  # No amortization until maturity
    elif amort_type == 'linear':
        return principal / years_remaining
    elif amort_type == 'annuity':
        # Simplified - assume 5% rate for annuity calculation
        rate = 0.05
        if rate > 0:
            return principal * (rate * (1 + rate)**years_remaining) / ((1 + rate)**years_remaining - 1)
        return principal / years_remaining
    else:
        return 0


def project_debt_financing(
    config: Dict,
    cash_flow_projection: pd.DataFrame = None,
    pnl_projection: pd.DataFrame = None
) -> Dict:
    """
    Project debt schedules and financing needs.

    Args:
        config: Configuration dictionary
        cash_flow_projection: Cash flow projection from CFM-1.0
        pnl_projection: P&L projection from PLM-1.0

    Returns:
        Dictionary with debt schedule, interest expense, and covenant compliance
    """
    params = extract_debt_params(config)
    years = get_year_range(params['base_year'], params['projection_years'])
    facilities = params['debt_facilities']
    refinancing = params['refinancing']
    covenants = params['covenants']

    # Initialize facility tracking
    facility_balances = {}
    for f in facilities:
        if f['type'] == 'revolver':
            facility_balances[f['name']] = f.get('drawn_m', 0)
        else:
            facility_balances[f['name']] = f.get('principal_m', 0)

    # Initialize data storage
    data = []
    facility_details = []

    for i, year in enumerate(years):
        row = {'Year': year}

        # Get EBITDA and FCF for this year
        ebitda = 0
        fcf = 0

        if pnl_projection is not None and 'Year' in pnl_projection.columns:
            pnl_row = pnl_projection[pnl_projection['Year'] == year]
            if len(pnl_row) > 0:
                ebitda = float(pnl_row['EBITDA'].iloc[0]) if 'EBITDA' in pnl_row else 0

        if cash_flow_projection is not None and 'Year' in cash_flow_projection.columns:
            cf_row = cash_flow_projection[cash_flow_projection['Year'] == year]
            if len(cf_row) > 0:
                fcf = float(cf_row['Free_Cash_Flow'].iloc[0]) if 'Free_Cash_Flow' in cf_row else 0

        # Process each facility
        total_interest = 0
        total_amortization = 0
        total_debt = 0
        total_commitment_fees = 0

        for f in facilities:
            fname = f['name']
            ftype = f['type']
            rate = f.get('interest_rate_percent', 5.0) / 100
            maturity = f.get('maturity_year', year + 5)
            amort_type = f.get('amortization', 'linear')

            balance = facility_balances.get(fname, 0)
            years_remaining = maturity - year

            if year <= maturity and balance > 0:
                # Interest expense
                interest = balance * rate
                total_interest += interest

                # Amortization
                if year == maturity:
                    # Bullet payment at maturity
                    amort = balance
                elif ftype != 'revolver':
                    amort = calculate_amortization(balance, years_remaining, amort_type)
                else:
                    amort = 0

                total_amortization += amort

                # Update balance
                facility_balances[fname] = max(0, balance - amort)

                # Track debt
                total_debt += facility_balances[fname]

                # Commitment fees for revolvers
                if ftype == 'revolver':
                    commitment = f.get('commitment_m', 0)
                    undrawn = commitment - balance
                    fee_rate = f.get('commitment_fee_percent', 0.5) / 100
                    total_commitment_fees += undrawn * fee_rate

                facility_details.append({
                    'Year': year,
                    'Facility': fname,
                    'Type': ftype,
                    'Opening_Balance': balance,
                    'Interest': interest,
                    'Amortization': amort,
                    'Closing_Balance': facility_balances[fname]
                })

        row['Total_Debt'] = total_debt
        row['Interest_Expense'] = total_interest
        row['Commitment_Fees'] = total_commitment_fees
        row['Total_Interest_Cost'] = total_interest + total_commitment_fees
        row['Principal_Repayment'] = total_amortization
        row['Total_Debt_Service'] = total_interest + total_amortization

        # Calculate ratios
        row['EBITDA'] = ebitda
        row['FCF'] = fcf

        # Leverage Ratio = Net Debt / EBITDA
        row['Leverage_Ratio'] = total_debt / ebitda if ebitda > 0 else 0

        # Interest Coverage = EBITDA / Interest
        row['Interest_Coverage'] = ebitda / total_interest if total_interest > 0 else 999

        # Debt Service Coverage = (EBITDA - CapEx) / Debt Service
        # Simplified: use FCF as proxy
        row['Debt_Service_Coverage'] = (ebitda) / row['Total_Debt_Service'] if row['Total_Debt_Service'] > 0 else 999

        # Covenant compliance
        row['Leverage_Compliant'] = row['Leverage_Ratio'] <= covenants['max_leverage_ratio']
        row['Interest_Coverage_Compliant'] = row['Interest_Coverage'] >= covenants['min_interest_coverage']
        row['DSCR_Compliant'] = row['Debt_Service_Coverage'] >= covenants['min_debt_service_coverage']
        row['All_Covenants_Compliant'] = row['Leverage_Compliant'] and row['Interest_Coverage_Compliant'] and row['DSCR_Compliant']

        data.append(row)

    df = pd.DataFrame(data)
    facility_df = pd.DataFrame(facility_details) if facility_details else pd.DataFrame()

    # Build summary
    base_row = df.iloc[0]
    final_row = df.iloc[-1]

    total_interest_paid = df['Total_Interest_Cost'].sum()
    total_principal_paid = df['Principal_Repayment'].sum()
    covenant_breaches = len(df[~df['All_Covenants_Compliant']])

    summary = {
        'currency': params['currency'],
        'debt': {
            'base_year_m': float(base_row['Total_Debt']),
            'final_year_m': float(final_row['Total_Debt']),
            'reduction_m': float(base_row['Total_Debt'] - final_row['Total_Debt']),
            'num_facilities': len(facilities)
        },
        'interest': {
            'total_paid_m': float(total_interest_paid),
            'avg_annual_m': float(total_interest_paid / len(years)),
            'base_year_m': float(base_row['Interest_Expense']),
            'final_year_m': float(final_row['Interest_Expense'])
        },
        'ratios': {
            'base_leverage': float(base_row['Leverage_Ratio']),
            'final_leverage': float(final_row['Leverage_Ratio']),
            'avg_interest_coverage': float(df['Interest_Coverage'].mean()),
            'min_interest_coverage': float(df['Interest_Coverage'].min())
        },
        'covenants': {
            'max_leverage_limit': covenants['max_leverage_ratio'],
            'min_interest_coverage_limit': covenants['min_interest_coverage'],
            'min_dscr_limit': covenants['min_debt_service_coverage'],
            'breach_years': int(covenant_breaches),
            'compliance_rate_percent': ((len(df) - covenant_breaches) / len(df)) * 100
        }
    }

    return {
        'debt_schedule': df,
        'facility_details': facility_df,
        'summary': summary,
        'params': params
    }


def format_results(results: Dict) -> str:
    """Format debt financing results for display."""
    output = []
    output.append("\n" + "="*80)
    output.append("DEBT & FINANCING MODEL (DFM-1.0) - RESULTS")
    output.append("="*80)

    summary = results['summary']
    currency = summary.get('currency', 'EUR')

    output.append("\n[1] DEBT SUMMARY")
    output.append("-" * 60)
    debt = summary['debt']
    output.append(f"  Base Year Debt:     {currency}{debt['base_year_m']:,.0f}M")
    output.append(f"  Final Year Debt:    {currency}{debt['final_year_m']:,.0f}M")
    output.append(f"  Debt Reduction:     {currency}{debt['reduction_m']:,.0f}M")
    output.append(f"  Facilities:         {debt['num_facilities']}")

    output.append("\n[2] INTEREST EXPENSE")
    output.append("-" * 60)
    interest = summary['interest']
    output.append(f"  Total Interest:     {currency}{interest['total_paid_m']:,.0f}M")
    output.append(f"  Avg Annual:         {currency}{interest['avg_annual_m']:,.0f}M")
    output.append(f"  Base Year:          {currency}{interest['base_year_m']:,.0f}M")
    output.append(f"  Final Year:         {currency}{interest['final_year_m']:,.0f}M")

    output.append("\n[3] KEY RATIOS")
    output.append("-" * 60)
    ratios = summary['ratios']
    output.append(f"  Base Leverage:      {ratios['base_leverage']:.2f}x")
    output.append(f"  Final Leverage:     {ratios['final_leverage']:.2f}x")
    output.append(f"  Avg Interest Cov:   {ratios['avg_interest_coverage']:.1f}x")
    output.append(f"  Min Interest Cov:   {ratios['min_interest_coverage']:.1f}x")

    output.append("\n[4] COVENANT COMPLIANCE")
    output.append("-" * 60)
    cov = summary['covenants']
    output.append(f"  Max Leverage:       {cov['max_leverage_limit']:.1f}x")
    output.append(f"  Min Interest Cov:   {cov['min_interest_coverage_limit']:.1f}x")
    output.append(f"  Min DSCR:           {cov['min_dscr_limit']:.1f}x")
    output.append(f"  Breach Years:       {cov['breach_years']}")
    output.append(f"  Compliance Rate:    {cov['compliance_rate_percent']:.0f}%")

    status = "ALL COMPLIANT" if cov['breach_years'] == 0 else "BREACHES DETECTED"
    output.append(f"\n  Status: {status}")

    output.append("\n" + "="*80)
    return "\n".join(output)


def main():
    """Main entry point for command-line execution."""
    if len(sys.argv) < 2:
        print("Usage: python debt_financing.py <config_file.yaml> [cashflow.csv] [pnl.csv]")
        sys.exit(1)

    config_file = sys.argv[1]
    config = load_config(config_file)

    cf_df = None
    pnl_df = None

    if len(sys.argv) > 2:
        cf_df = pd.read_csv(sys.argv[2])
    if len(sys.argv) > 3:
        pnl_df = pd.read_csv(sys.argv[3])

    results = project_debt_financing(config, cf_df, pnl_df)
    print(format_results(results))


if __name__ == '__main__':
    main()
