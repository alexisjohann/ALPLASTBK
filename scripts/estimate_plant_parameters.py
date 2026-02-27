#!/usr/bin/env python3
"""
ALPLA Plant Parameter Estimation using LLMMC
=============================================

Reads priors from data/alpla-pci-priors.yaml and generates
parameter estimates with confidence intervals.

Methodology: LLMMC (LLM Monte Carlo) - Appendix AN
Reference: docs/methods/ALPLA_Plant_Comparability_Index_PCI.md

Usage:
    python scripts/estimate_plant_parameters.py
    python scripts/estimate_plant_parameters.py --output csv
    python scripts/estimate_plant_parameters.py --validate-only

Output:
    data/alpla-pci-estimates.csv
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import numpy as np

# Try to import yaml, provide helpful error if missing
try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)


class LLMMCEstimator:
    """
    LLM Monte Carlo Parameter Estimator

    Generates parameter estimates with uncertainty quantification
    using constrained Monte Carlo simulation.
    """

    def __init__(self, priors_path: str, n_simulations: int = 1000):
        self.priors_path = Path(priors_path)
        self.n_simulations = n_simulations
        self.priors = self._load_priors()
        self.rng = np.random.default_rng(42)  # Reproducible

    def _load_priors(self) -> Dict:
        """Load priors from YAML file."""
        if not self.priors_path.exists():
            raise FileNotFoundError(f"Priors file not found: {self.priors_path}")

        with open(self.priors_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def _sample_lognormal(self, median: float, sigma: float,
                          min_val: float, max_val: float,
                          n: int = 1) -> np.ndarray:
        """
        Sample from truncated lognormal distribution.

        Args:
            median: Median of distribution (exp(mu))
            sigma: Standard deviation of log
            min_val: Minimum allowed value
            max_val: Maximum allowed value
            n: Number of samples
        """
        mu = np.log(median)
        samples = self.rng.lognormal(mu, sigma, n)

        # Truncate to bounds
        samples = np.clip(samples, min_val, max_val)
        return samples

    def _get_plant_prior(self, plant_id: str) -> Dict:
        """Get prior distribution for a specific plant."""
        plant = self.priors['plants'].get(plant_id, {})
        plant_type = plant.get('type', 'standalone')
        type_prior = self.priors['plant_type_priors'].get(plant_type, {})

        # Check for plant-specific override
        override = plant.get('prior_override')
        if override and override.get('median'):
            return {
                'median': override['median'],
                'sigma': type_prior.get('sigma', 0.4),
                'min': override.get('min', type_prior.get('min', 50)),
                'max': override.get('max', type_prior.get('max', 500))
            }

        return {
            'median': type_prior.get('median', 150),
            'sigma': type_prior.get('sigma', 0.4),
            'min': type_prior.get('min', 50),
            'max': type_prior.get('max', 500)
        }

    def estimate_S2_employees(self) -> Dict[str, Dict]:
        """
        Estimate S2 (employee count) for all plants using LLMMC.

        Returns dict with plant_id -> {median, p10, p90, confidence}
        """
        results = {}
        all_samples = {}

        # Get target constraint
        constraints = self.priors['global_constraints']['north_america_region']
        target = constraints['usa_employees_target']
        tolerance_pct = constraints['usa_employees_tolerance_pct']
        min_total = target * (1 - tolerance_pct/100)
        max_total = target * (1 + tolerance_pct/100)

        # Phase 1: Generate unconstrained samples
        plant_ids = list(self.priors['plants'].keys())

        for plant_id in plant_ids:
            prior = self._get_plant_prior(plant_id)
            samples = self._sample_lognormal(
                prior['median'], prior['sigma'],
                prior['min'], prior['max'],
                self.n_simulations
            )
            all_samples[plant_id] = samples

        # Phase 2: Constraint satisfaction via rejection sampling
        valid_indices = []
        for i in range(self.n_simulations):
            total = sum(all_samples[pid][i] for pid in plant_ids)
            if min_total <= total <= max_total:
                valid_indices.append(i)

        # If not enough valid samples, use scaling
        if len(valid_indices) < 100:
            print(f"Warning: Only {len(valid_indices)} valid samples. Using scaling.")
            # Scale all samples to meet constraint
            for i in range(self.n_simulations):
                total = sum(all_samples[pid][i] for pid in plant_ids)
                scale = target / total
                for pid in plant_ids:
                    all_samples[pid][i] *= scale
            valid_indices = list(range(self.n_simulations))

        # Phase 3: Compute statistics from valid samples
        for plant_id in plant_ids:
            valid_samples = all_samples[plant_id][valid_indices]
            plant_info = self.priors['plants'].get(plant_id, {})

            results[plant_id] = {
                'name': plant_info.get('name', plant_id),
                'type': plant_info.get('type', 'standalone'),
                'S2_median': int(np.median(valid_samples)),
                'S2_p10': int(np.percentile(valid_samples, 10)),
                'S2_p90': int(np.percentile(valid_samples, 90)),
                'S2_std': int(np.std(valid_samples)),
                'confidence': plant_info.get('confidence', 'medium'),
                'n_valid_samples': len(valid_indices)
            }

        # Validation
        total_median = sum(r['S2_median'] for r in results.values())
        print(f"\nValidation: Total S2 median = {total_median}")
        print(f"Target range: {int(min_total)} - {int(max_total)}")
        print(f"Valid samples: {len(valid_indices)}/{self.n_simulations}")

        return results

    def estimate_other_parameters(self, S2_results: Dict) -> Dict[str, Dict]:
        """
        Estimate other parameters (S3-S6, O1-O5, P1-P4) based on S2 and priors.
        """
        other_priors = self.priors.get('other_parameters', {})
        results = {}

        for plant_id, s2_data in S2_results.items():
            plant = self.priors['plants'].get(plant_id, {})
            plant_type = plant.get('type', 'standalone')
            S2 = s2_data['S2_median']

            # S3: Plant Age (known from facts)
            known_years = {
                'US-002': 2017, 'US-003': 2003, 'US-006': 2010,
                'US-008': 2022, 'US-009': 2013, 'US-010': 2020,
                'US-013': 2006, 'US-014': 2019, 'US-015': 2018,
                'US-016': 2001, 'US-017': 2017
            }
            opening_year = known_years.get(plant_id, 2010)  # Default
            S3 = 2026 - opening_year

            # S4: Technology Complexity
            s4_prior = other_priors.get('S4_technology_complexity', {}).get('prior', {})
            s4_type_prior = s4_prior.get(plant_type, {'median': 2.0, 'sigma': 0.3})
            S4 = round(self.rng.normal(s4_type_prior['median'], s4_type_prior['sigma']), 1)
            S4 = np.clip(S4, 1.0, 3.0)

            # S5: Automation (newer plants higher)
            if opening_year >= 2018:
                S5 = int(self.rng.normal(65, 10))
            else:
                S5 = int(self.rng.normal(45, 15))
            S5 = np.clip(S5, 20, 90)

            # S6: Shift Model (based on size and type)
            if plant_type == 'in_house':
                S6 = 3  # Usually 3-shift for customer demand
            elif S2 > 200:
                S6 = 4  # Continuous for large plants
            elif S2 < 150:
                S6 = 2  # 2-shift for small
            else:
                S6 = 3  # 3-shift default

            # O1: Customer Concentration
            o1_prior = other_priors.get('O1_customer_concentration', {}).get('prior', {})
            o1_type = o1_prior.get(plant_type, {'median': 35, 'min': 15, 'max': 60})
            O1 = int(self.rng.uniform(o1_type.get('min', 15), o1_type.get('max', 60)))
            if plant_type == 'in_house':
                O1 = int(self.rng.uniform(85, 100))
            elif plant_type == 'near_customer':
                O1 = int(self.rng.uniform(50, 90))

            # O2: Plant Manager Tenure
            O2 = round(self.rng.exponential(4.5), 1)
            O2 = min(O2, 15)  # Cap at 15 years

            # O3: HR On-Site (based on size)
            O3 = 1 if S2 >= 150 else 0

            # O4: Union Status (state-based)
            state_union_prob = {
                'KY': 0.10, 'OH': 0.25, 'MO': 0.15,
                'PA': 0.20, 'GA': 0.08, 'TX': 0.05,
                'IA': 0.12, 'UT': 0.05, 'WI': 0.15
            }
            # Extract state from name
            name = s2_data['name']
            state = name.split()[-1] if len(name.split()) > 1 else 'GA'
            prob = state_union_prob.get(state, 0.10)
            O4 = 1 if self.rng.random() < prob else 0

            # O5: Training Hours
            O5 = int(self.rng.normal(24, 8))
            O5 = np.clip(O5, 8, 48)

            # =========================================================
            # BLUE COLLAR / WHITE COLLAR SPLIT
            # =========================================================
            workforce_comp = self.priors.get('workforce_composition', {}).get('by_plant_type', {})
            type_comp = workforce_comp.get(plant_type, {'blue_collar_pct': 80, 'white_collar_pct': 20})

            BC_pct = type_comp.get('blue_collar_pct', 80)
            WC_pct = type_comp.get('white_collar_pct', 20)

            # Calculate absolute numbers
            BC_count = int(round(S2 * BC_pct / 100))
            WC_count = S2 - BC_count  # Ensure sum = S2

            # =========================================================
            # CHURN RATES BY COLLAR TYPE
            # =========================================================
            churn_priors = self.priors.get('workforce_composition', {}).get('churn_rates_prior', {})

            # Blue Collar Churn
            bc_churn_prior = churn_priors.get('blue_collar', {})
            P1_BC = round(self.rng.normal(
                bc_churn_prior.get('alpla_estimated_median', 22),
                bc_churn_prior.get('alpla_estimated_sigma', 6)
            ), 1)
            P1_BC = np.clip(P1_BC, bc_churn_prior.get('min', 10), bc_churn_prior.get('max', 45))

            # White Collar Churn
            wc_churn_prior = churn_priors.get('white_collar', {})
            P1_WC = round(self.rng.normal(
                wc_churn_prior.get('alpla_estimated_median', 10),
                wc_churn_prior.get('alpla_estimated_sigma', 3)
            ), 1)
            P1_WC = np.clip(P1_WC, wc_churn_prior.get('min', 4), wc_churn_prior.get('max', 20))

            # Overall weighted churn
            P1 = round((P1_BC * BC_pct + P1_WC * WC_pct) / 100, 1)

            # P2: Absence Rate
            P2 = round(self.rng.normal(3.5, 1.2), 1)
            P2 = np.clip(P2, 1, 8)

            # P3: TRIR
            P3 = round(self.rng.normal(2.5, 0.8), 1)
            P3 = np.clip(P3, 0.5, 6)

            # P4: Productivity Index
            base_productivity = 100 + (S5 - 50) * 0.4  # Correlation with automation
            P4 = int(self.rng.normal(base_productivity, 15))
            P4 = np.clip(P4, 60, 140)

            results[plant_id] = {
                'S3': S3, 'S4': float(S4), 'S5': int(S5), 'S6': S6,
                'O1': O1, 'O2': float(O2), 'O3': O3, 'O4': O4, 'O5': int(O5),
                'BC_pct': BC_pct, 'WC_pct': WC_pct,
                'BC_count': BC_count, 'WC_count': WC_count,
                'P1_BC': float(P1_BC), 'P1_WC': float(P1_WC), 'P1_total': float(P1),
                'P2': float(P2), 'P3': float(P3), 'P4': int(P4)
            }

        return results

    def generate_full_estimates(self) -> List[Dict]:
        """Generate complete parameter estimates for all plants."""
        print("=" * 60)
        print("ALPLA Plant Parameter Estimation (LLMMC)")
        print("=" * 60)

        # Step 1: Estimate S2 with constraints
        print("\n[1/3] Estimating S2 (Employee Count)...")
        s2_results = self.estimate_S2_employees()

        # Step 2: Estimate other parameters
        print("\n[2/3] Estimating S3-S6, O1-O5, P1-P4...")
        other_results = self.estimate_other_parameters(s2_results)

        # Step 3: Combine results
        print("\n[3/3] Combining results...")
        combined = []
        for plant_id in s2_results:
            row = {
                'plant_id': plant_id,
                'plant_name': s2_results[plant_id]['name'],
                'plant_type': s2_results[plant_id]['type'],
                'S2_employees': s2_results[plant_id]['S2_median'],
                'S2_p10': s2_results[plant_id]['S2_p10'],
                'S2_p90': s2_results[plant_id]['S2_p90'],
                'S2_confidence': s2_results[plant_id]['confidence'],
                **other_results[plant_id]
            }
            combined.append(row)

        return combined

    def export_csv(self, results: List[Dict], output_path: str):
        """Export results to CSV."""
        import csv

        fieldnames = list(results[0].keys())

        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            # Header comment
            f.write("# ALPLA PCI Parameter Estimates (LLMMC)\n")
            f.write(f"# Generated: 2026-01-19\n")
            f.write(f"# Simulations: {self.n_simulations}\n")
            f.write(f"# Priors: {self.priors_path}\n")
            f.write("#\n")

            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

        print(f"\nExported to: {output_path}")

    def print_summary(self, results: List[Dict]):
        """Print summary table."""
        print("\n" + "=" * 100)
        print("ESTIMATION RESULTS (with Blue Collar / White Collar Split)")
        print("=" * 100)
        print(f"{'Plant':<25} {'Type':<12} {'S2':>5} {'BC':>5} {'WC':>4} {'BC%':>4} {'Churn_BC':>8} {'Churn_WC':>8} {'Churn_Tot':>9}")
        print("-" * 100)

        total_s2 = 0
        total_bc = 0
        total_wc = 0
        for r in results:
            name = r['plant_name'][:23]
            ptype = r['plant_type'][:10]
            s2 = r['S2_employees']
            bc = r.get('BC_count', int(s2 * 0.8))
            wc = r.get('WC_count', s2 - bc)
            bc_pct = r.get('BC_pct', 80)
            p1_bc = r.get('P1_BC', 22.0)
            p1_wc = r.get('P1_WC', 10.0)
            p1_tot = r.get('P1_total', 18.0)
            print(f"{name:<25} {ptype:<12} {s2:>5} {bc:>5} {wc:>4} {bc_pct:>3}% {p1_bc:>7.1f}% {p1_wc:>7.1f}% {p1_tot:>8.1f}%")
            total_s2 += s2
            total_bc += bc
            total_wc += wc

        print("-" * 100)
        avg_bc_pct = round(total_bc / total_s2 * 100, 1) if total_s2 > 0 else 0
        print(f"{'TOTAL':<25} {'':<12} {total_s2:>5} {total_bc:>5} {total_wc:>4} {avg_bc_pct:>3}%")
        print("=" * 100)

        # Additional summary
        print(f"\nWorkforce Composition Summary:")
        print(f"  Blue Collar:  {total_bc:,} ({avg_bc_pct}%)")
        print(f"  White Collar: {total_wc:,} ({100-avg_bc_pct:.1f}%)")


def main():
    parser = argparse.ArgumentParser(description='ALPLA Plant Parameter Estimation')
    parser.add_argument('--priors', default='data/alpla-pci-priors.yaml',
                        help='Path to priors YAML file')
    parser.add_argument('--output', default='data/alpla-pci-estimates.csv',
                        help='Output CSV path')
    parser.add_argument('--simulations', type=int, default=1000,
                        help='Number of Monte Carlo simulations')
    parser.add_argument('--validate-only', action='store_true',
                        help='Only validate priors, do not estimate')

    args = parser.parse_args()

    # Find project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    priors_path = project_root / args.priors
    output_path = project_root / args.output

    try:
        estimator = LLMMCEstimator(str(priors_path), args.simulations)

        if args.validate_only:
            print("Priors loaded successfully.")
            print(f"Plants: {len(estimator.priors.get('plants', {}))}")
            return

        results = estimator.generate_full_estimates()
        estimator.print_summary(results)
        estimator.export_csv(results, str(output_path))

        print("\nDone! Review estimates and adjust priors if needed.")

    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}")
        raise


if __name__ == '__main__':
    main()
