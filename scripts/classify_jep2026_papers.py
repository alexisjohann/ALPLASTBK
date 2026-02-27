#!/usr/bin/env python3
"""Apply 10C classification to JEP Winter 2026 papers.

Updates both YAML (data/paper-references/) and BibTeX (bcm_master.bib)
with 10C dimensions, use_for, theory_support, and parameters.

Usage:
    python scripts/classify_jep2026_papers.py            # dry-run
    python scripts/classify_jep2026_papers.py --execute   # apply
"""

import argparse
import os
import re

REFS_DIR = "data/paper-references"
BIB_FILE = "bibliography/bcm_master.bib"

CLASSIFICATIONS = {
    'berger2026labor': {
        'use_for': ['LIT-O', 'DOMAIN-LABOR', 'CORE-HOW', 'CORE-WHERE'],
        'theory_support': 'MS-LM-001, MS-SP-001, MS-IF-006',
        'parameter': 'monopsony_wage_markdown=0.70-0.80, labor_HHI, welfare_loss_pct=7.6, wage_gain_concentrated_markets=30pct',
        'identification': 'structural_estimation, granular_firm_model, cross_market_variation',
        'external_validity': 'US labor markets; generalizable to concentrated employer markets globally',
        'evidence_tier': 1,
        '10c_dimensions': ['WHAT', 'HOW', 'WHEN', 'WHERE', 'HIERARCHY'],
    },
    'geruso2026likelihood': {
        'use_for': ['LIT-O', 'DOMAIN-DEMOGRAPHY', 'CORE-WHAT', 'CORE-STAGE'],
        'theory_support': 'MS-DV-001, MS-PP-001',
        'parameter': 'TFR_global_2025=2.06, TFR_1950=4.85, fertility_persistence_tau',
        'identification': 'demographic_projections, cross_country_data, UN_WPP_2024',
        'external_validity': 'Global; 200+ countries; longitudinal 1950-2100',
        'evidence_tier': 1,
        '10c_dimensions': ['WHAT', 'STAGE', 'HIERARCHY', 'WHERE'],
    },
    'gobbi2026family': {
        'use_for': ['LIT-O', 'DOMAIN-FAMILY', 'CORE-WHAT', 'CORE-WHEN'],
        'theory_support': 'MS-DV-003, MS-IF-014, MS-IF-003',
        'parameter': 'alpha_inheritance, gamma_gender_role, beta_institution, rho_econ_conditional',
        'identification': 'cross_country_institutional_variation, historical_ethnographic_data',
        'external_validity': 'Global; historical and contemporary; cross-cultural',
        'evidence_tier': 1,
        '10c_dimensions': ['WHAT', 'WHEN', 'HIERARCHY', 'STAGE'],
    },
    'johnson2026occupational': {
        'use_for': ['LIT-O', 'DOMAIN-LABOR', 'CORE-WHAT', 'CORE-WHERE'],
        'theory_support': 'MS-IF-006, MS-IF-001, MS-NU-002',
        'parameter': 'licensure_prevalence_US=0.30, wage_premium_license=0.15-0.20, mobility_friction_psi',
        'identification': 'state_variation_licensing, labor_force_surveys, quasi_experimental',
        'external_validity': 'US; state-level variation; 30pct of workforce',
        'evidence_tier': 1,
        '10c_dimensions': ['WHAT', 'WHEN', 'HIERARCHY', 'WHERE'],
    },
    'khanna2026asia': {
        'use_for': ['LIT-O', 'DOMAIN-LABOR', 'DOMAIN-MIGRATION', 'CORE-WHO', 'CORE-HOW'],
        'theory_support': 'MS-LM-002, MS-LM-003, MS-IN-005',
        'parameter': 'high_skill_share_india=0.78, high_skill_share_china=0.63, sector_software=0.38, visa_H1B_elasticity',
        'identification': 'immigration_administrative_data, visa_lottery, sector_composition',
        'external_validity': 'US immigration; Asian-origin; skill-intensive sectors',
        'evidence_tier': 1,
        '10c_dimensions': ['WHO', 'HOW', 'WHEN', 'WHERE'],
    },
    'postel2026asian': {
        'use_for': ['LIT-O', 'DOMAIN-MIGRATION', 'CORE-WHO', 'CORE-WHEN'],
        'theory_support': 'MS-LM-004, MS-SF-001',
        'parameter': 'population_growth_1960_2019=2700pct, policy_leverage_1965_act',
        'identification': 'historical_analysis, census_data, policy_discontinuity',
        'external_validity': 'US; Asian immigration 1850-2020; policy-driven variation',
        'evidence_tier': 1,
        '10c_dimensions': ['WHO', 'WHEN', 'WHERE', 'HIERARCHY'],
    },
    'prager2026antitrust': {
        'use_for': ['LIT-O', 'DOMAIN-ANTITRUST', 'CORE-HOW', 'CORE-WHERE'],
        'theory_support': 'MS-SP-001, MS-IF-006, MS-CM-001',
        'parameter': 'enforcement_intensity_2010=1_to_2020=7, labor_HHI_threshold, gamma_monopsony',
        'identification': 'enforcement_data, merger_analysis, labor_market_outcomes',
        'external_validity': 'US antitrust enforcement; labor markets',
        'evidence_tier': 1,
        '10c_dimensions': ['WHAT', 'HOW', 'WHERE', 'HIERARCHY'],
    },
    'pritchett2026global': {
        'use_for': ['LIT-O', 'DOMAIN-MIGRATION', 'CORE-WHEN', 'CORE-HIERARCHY'],
        'theory_support': 'MS-DV-001, MS-LM-001, MS-PP-002',
        'parameter': 'TFR_rich_below_1.5, TFR_africa_above_3.5, dependency_ratio_shift, mobility_gains_trillions',
        'identification': 'demographic_projections, cross_country_comparison, labor_force_forecasts',
        'external_validity': 'Global; rich vs developing countries; 2025-2100 projections',
        'evidence_tier': 1,
        '10c_dimensions': ['WHO', 'WHEN', 'STAGE', 'HIERARCHY', 'WHERE'],
    },
    'starr2026economics': {
        'use_for': ['LIT-O', 'DOMAIN-LABOR', 'CORE-HOW', 'CORE-WHAT'],
        'theory_support': 'MS-IF-006, MS-IF-007, MS-CM-001, MS-RD-002',
        'parameter': 'beta_noncompete_wage=-0.08_to_-0.15, california_ban_innovation_multiplier, exit_option_delta',
        'identification': 'state_variation_enforceability, quasi_experimental, survey_data',
        'external_validity': 'US; state-level enforceability variation; multiple industries',
        'evidence_tier': 1,
        '10c_dimensions': ['WHAT', 'HOW', 'WHEN', 'WHERE'],
    },
    'taylor2026recommendations': {
        'use_for': ['LIT-O'],
        'theory_support': '',
        'parameter': '',
        'identification': 'review_article',
        'external_validity': 'JEP reading recommendations; meta-level',
        'evidence_tier': 2,
        '10c_dimensions': [],
    },
    'weil2026continued': {
        'use_for': ['LIT-O', 'DOMAIN-DEMOGRAPHY', 'CORE-WHAT', 'CORE-STAGE'],
        'theory_support': 'MS-DV-001, MS-DV-004, MS-PP-001',
        'parameter': 'TFR_US_2023=1.62, consumption_impact_TFR1.0=-8.7pct, transition_benefit_decades=4',
        'identification': 'calibrated_OLG_model, demographic_accounting, scenario_analysis',
        'external_validity': 'US; scalable to other low-fertility developed economies',
        'evidence_tier': 1,
        '10c_dimensions': ['WHAT', 'STAGE', 'HIERARCHY', 'WHERE'],
    },
}


def update_yaml(key, cls, execute=False):
    """Update YAML file with classification."""
    yaml_path = os.path.join(REFS_DIR, f"PAP-{key}.yaml")
    if not os.path.exists(yaml_path):
        print(f"  SKIP {key}: no YAML file")
        return False

    with open(yaml_path, 'r') as f:
        content = f.read()

    # Update ebf_integration section
    use_for_yaml = '\n'.join(f'  - {u}' for u in cls['use_for'])
    theory_val = cls['theory_support'] if cls['theory_support'] else 'null'
    param_val = cls['parameter'] if cls['parameter'] else 'null'
    ident_val = cls['identification'] if cls['identification'] else 'null'
    ext_val = cls['external_validity'] if cls['external_validity'] else 'null'

    new_ebf = (
        f"ebf_integration:\n"
        f"  evidence_tier: {cls['evidence_tier']}\n"
        f"  use_for:\n{use_for_yaml}\n"
        f"  theory_support: {theory_val}\n"
        f"  parameter: {param_val}\n"
        f"  identification: {ident_val}\n"
        f"  external_validity: {ext_val}\n"
    )

    # Replace existing ebf_integration block
    content = re.sub(
        r'ebf_integration:\n(?:  .*\n)*',
        new_ebf,
        content
    )

    # Update integration level based on richness
    if len(cls['use_for']) > 2 and cls['theory_support']:
        new_level = 'I2'
    else:
        new_level = 'I1'
    content = re.sub(r'integration_level: I\d', f'integration_level: {new_level}', content)

    if execute:
        with open(yaml_path, 'w') as f:
            f.write(content)
    return True


def update_bibtex(key, cls, execute=False):
    """Update BibTeX entry with classification."""
    with open(BIB_FILE, 'r') as f:
        content = f.read()

    use_for_str = ', '.join(cls['use_for'])
    theory_str = cls['theory_support']
    param_str = cls['parameter']
    ident_str = cls['identification']
    ext_str = cls['external_validity']

    # Find and replace use_for field
    pattern = rf'(@article\{{{key},.*?use_for = \{{)(.*?)(\}})'
    content = re.sub(pattern, rf'\g<1>{use_for_str}\3', content, flags=re.DOTALL)

    # Replace theory_support
    pattern = rf'(@article\{{{key},.*?theory_support = \{{)(.*?)(\}})'
    content = re.sub(pattern, rf'\g<1>{theory_str}\3', content, flags=re.DOTALL)

    # Replace parameter
    pattern = rf'(@article\{{{key},.*?parameter = \{{)(.*?)(\}})'
    content = re.sub(pattern, rf'\g<1>{param_str}\3', content, flags=re.DOTALL)

    # Replace identification
    pattern = rf'(@article\{{{key},.*?identification = \{{)(.*?)(\}})'
    content = re.sub(pattern, rf'\g<1>{ident_str}\3', content, flags=re.DOTALL)

    # Replace external_validity
    pattern = rf'(@article\{{{key},.*?external_validity = \{{)(.*?)(\}})'
    content = re.sub(pattern, rf'\g<1>{ext_str}\3', content, flags=re.DOTALL)

    if execute:
        with open(BIB_FILE, 'w') as f:
            f.write(content)
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--execute', action='store_true')
    parser.add_argument('--key', type=str)
    args = parser.parse_args()

    papers = CLASSIFICATIONS
    if args.key:
        papers = {args.key: papers[args.key]}

    for key, cls in papers.items():
        dims = ', '.join(cls['10c_dimensions']) if cls['10c_dimensions'] else '(none)'
        uses = ', '.join(cls['use_for'])

        if args.execute:
            update_yaml(key, cls, execute=True)
            print(f"  UPDATE {key}: 10C=[{dims}] use_for=[{uses}]")
        else:
            print(f"  [DRY-RUN] {key}: 10C=[{dims}] use_for=[{uses}]")

    # Update BibTeX all at once (reads/writes full file)
    if args.execute:
        with open(BIB_FILE, 'r') as f:
            content = f.read()

        for key, cls in papers.items():
            use_for_str = ', '.join(cls['use_for'])
            theory_str = cls['theory_support']
            param_str = cls['parameter']
            ident_str = cls['identification']
            ext_str = cls['external_validity']

            content = re.sub(
                rf'(@article\{{{key},.*?use_for = \{{)(.*?)(\}})',
                rf'\g<1>{use_for_str}\3', content, flags=re.DOTALL)
            content = re.sub(
                rf'(@article\{{{key},.*?theory_support = \{{)(.*?)(\}})',
                rf'\g<1>{theory_str}\3', content, flags=re.DOTALL)
            content = re.sub(
                rf'(@article\{{{key},.*?parameter = \{{)(.*?)(\}})',
                rf'\g<1>{param_str}\3', content, flags=re.DOTALL)
            content = re.sub(
                rf'(@article\{{{key},.*?identification = \{{)(.*?)(\}})',
                rf'\g<1>{ident_str}\3', content, flags=re.DOTALL)
            content = re.sub(
                rf'(@article\{{{key},.*?external_validity = \{{)(.*?)(\}})',
                rf'\g<1>{ext_str}\3', content, flags=re.DOTALL)

        with open(BIB_FILE, 'w') as f:
            f.write(content)
        print(f"\n  BibTeX updated for {len(papers)} entries.")

    if not args.execute:
        print(f"\nDry run. Use --execute to apply 10C classifications.")


if __name__ == '__main__':
    main()
