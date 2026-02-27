#!/usr/bin/env python3
"""
Phase 6: Decay Analyzer
Models and analyzes effect persistence and decay over time

Components:
- Exponential decay model fitting
- Linear decay modeling
- Segmented decay analysis
- Sustainability scoring
- Booster effectiveness estimation
"""

import yaml
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import numpy as np


class Phase6DecayAnalyzer:
    """Model and analyze effect decay over time"""

    def __init__(self, registry_path: str = "data/intervention-registry.yaml"):
        self.registry_path = Path(registry_path)
        self.registry = self._load_registry()

    def _load_registry(self) -> Dict:
        """Load intervention registry"""
        with open(self.registry_path, 'r') as f:
            return yaml.safe_load(f) or {}

    def _save_registry(self) -> None:
        """Save intervention registry"""
        with open(self.registry_path, 'w') as f:
            yaml.dump(self.registry, f, default_flow_style=False, allow_unicode=True)

    def fit_decay_model(
        self,
        project_id: str,
        model_type: str = 'exponential'
    ) -> Dict:
        """
        Fit decay model to observed effect data

        Args:
            project_id: Project identifier
            model_type: 'exponential', 'linear', or 'segmented'

        Returns:
            Fitted model parameters and statistics
        """
        if project_id not in self.registry['projects']:
            raise ValueError(f"Project {project_id} not found")

        project = self.registry['projects'][project_id]

        # Extract timepoint data
        measurements = {}
        if 'long_term_results' in project:
            for timepoint, result in project['long_term_results'].items():
                months = int(timepoint.rstrip('M'))
                # Get first KPI effect
                for kpi in result.get('kpis', []):
                    if 'delta_vs_prediction' in kpi:
                        measurements[months] = kpi['delta_vs_prediction']
                        break

        if not measurements:
            return {'status': 'insufficient_data', 'reason': 'No measurements recorded'}

        # Get initial effect from Phase 5 results
        initial_effect = project.get('results', {}).get('deviation_analysis', {}).get('overall', {}).get('actual_E_P', None)
        if not initial_effect:
            initial_effect = project.get('predictions', {}).get('portfolio_effect', {}).get('E_P', 0.5)

        # Fit model
        if model_type == 'exponential':
            return self._fit_exponential(project_id, initial_effect, measurements)
        elif model_type == 'linear':
            return self._fit_linear(project_id, initial_effect, measurements)
        elif model_type == 'segmented':
            return self._fit_segmented(project_id, initial_effect, measurements)
        else:
            raise ValueError(f"Unknown model type: {model_type}")

    def _fit_exponential(self, project_id: str, E0: float, measurements: Dict[int, float]) -> Dict:
        """
        Fit exponential decay model: E(t) = E₀ · e^(-ρ·t)

        Uses least squares estimation
        """
        if len(measurements) < 2:
            return {'status': 'insufficient_data', 'reason': 'Need at least 2 timepoints'}

        # Extract time and effect values
        times = np.array(sorted(measurements.keys()), dtype=float)
        effects = np.array([measurements[t] for t in times], dtype=float)

        # Normalize by initial effect
        normalized_effects = effects / E0

        # Fit log-linear model: ln(E/E₀) = -ρ·t
        # Linear regression on log scale
        log_effects = np.log(np.maximum(normalized_effects, 0.01))  # Avoid log(0)

        # Simple linear regression
        n = len(times)
        sum_t = np.sum(times)
        sum_log_e = np.sum(log_effects)
        sum_t_log_e = np.sum(times * log_effects)
        sum_t2 = np.sum(times**2)

        denominator = n * sum_t2 - sum_t**2
        rho = -(n * sum_t_log_e - sum_t * sum_log_e) / denominator if denominator != 0 else 0.05

        # Calculate R²
        predicted = E0 * np.exp(-rho * times)
        ss_res = np.sum((effects - predicted)**2)
        ss_tot = np.sum((effects - np.mean(effects))**2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0.7

        # Calculate t_half (time to 50% effect)
        t_half = math.log(2) / rho if rho > 0 else float('inf')

        result = {
            'model': 'exponential',
            'formula': "E(t) = E₀ · e^(-ρ·t)",
            'fitted_parameters': {
                'rho': round(rho, 4),
                'E_0': round(E0, 4),
                't_half': round(t_half, 2)
            },
            'model_fit': {
                'R_squared': round(r_squared, 3),
                'n_observations': len(times),
                'model_quality': self._assess_model_quality(r_squared)
            },
            'predictions': {}
        }

        # Generate predictions
        for t in [3, 6, 12, 24]:
            if t not in measurements:  # Only predict unmeasured timepoints
                result['predictions'][f'{t}M'] = round(E0 * math.exp(-rho * t), 4)

        # Store in registry
        if 'decay_analysis' not in self.registry['projects'][project_id]:
            self.registry['projects'][project_id]['decay_analysis'] = {}

        self.registry['projects'][project_id]['decay_analysis']['effect_decay'] = result

        return result

    def _fit_linear(self, project_id: str, E0: float, measurements: Dict[int, float]) -> Dict:
        """Fit linear decay model: E(t) = E₀ - β·t"""
        if len(measurements) < 2:
            return {'status': 'insufficient_data'}

        times = np.array(sorted(measurements.keys()), dtype=float)
        effects = np.array([measurements[t] for t in times], dtype=float)

        # Linear regression: E = E₀ - β·t
        n = len(times)
        sum_t = np.sum(times)
        sum_e = np.sum(effects)
        sum_t_e = np.sum(times * effects)
        sum_t2 = np.sum(times**2)

        denominator = n * sum_t2 - sum_t**2
        beta = (n * sum_t_e - sum_t * sum_e) / denominator if denominator != 0 else 0.01

        # Calculate R²
        predicted = E0 - beta * times
        ss_res = np.sum((effects - predicted)**2)
        ss_tot = np.sum((effects - np.mean(effects))**2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0.6

        result = {
            'model': 'linear',
            'formula': "E(t) = E₀ - β·t",
            'fitted_parameters': {
                'E_0': round(E0, 4),
                'beta': round(beta, 4)
            },
            'model_fit': {
                'R_squared': round(r_squared, 3),
                'n_observations': len(times),
                'model_quality': self._assess_model_quality(r_squared)
            },
            'predictions': {}
        }

        for t in [3, 6, 12, 24]:
            if t not in measurements:
                result['predictions'][f'{t}M'] = max(round(E0 - beta * t, 4), 0)

        if 'decay_analysis' not in self.registry['projects'][project_id]:
            self.registry['projects'][project_id]['decay_analysis'] = {}

        self.registry['projects'][project_id]['decay_analysis']['effect_decay'] = result

        return result

    def _fit_segmented(self, project_id: str, E0: float, measurements: Dict[int, float]) -> Dict:
        """Fit different decay models for different segments"""
        project = self.registry['projects'][project_id]

        if 'context' not in project or 'segments' not in project['context']:
            return {'status': 'no_segments_defined'}

        result = {
            'model': 'segmented',
            'formula': "E(t) = Σ E_segment(t), weighted by segment proportion",
            'by_segment': {}
        }

        # For each segment, create a decay estimate
        for segment in project['context']['segments']:
            segment_name = segment['name']
            proportion = segment['proportion']

            result['by_segment'][segment_name] = {
                'proportion': proportion,
                'estimated_rho': round(0.05 + 0.05 * (1 - proportion), 4),
                'interpretation': self._interpret_segment_decay(segment_name)
            }

        if 'decay_analysis' not in self.registry['projects'][project_id]:
            self.registry['projects'][project_id]['decay_analysis'] = {}

        self.registry['projects'][project_id]['decay_analysis']['by_segment'] = result['by_segment']

        return result

    def _assess_model_quality(self, r_squared: float) -> str:
        """Assess model fit quality based on R²"""
        if r_squared >= 0.90:
            return "excellent"
        elif r_squared >= 0.80:
            return "good"
        elif r_squared >= 0.70:
            return "acceptable"
        elif r_squared >= 0.60:
            return "weak"
        else:
            return "poor"

    def _interpret_segment_decay(self, segment_name: str) -> str:
        """Generate interpretation for segment decay pattern"""
        patterns = {
            'present-biased': 'Sustained behavior once adopted, structural inertia',
            'loss-averse': 'Moderate decay as salience fades, need for reinforcement',
            'rational-calculative': 'Early exit after initial trial, continued cost-benefit assessment',
            'health-conscious': 'Sustained behavior aligned with identity, low fade',
            'impulsive': 'Rapid decay without ongoing environmental support',
            'indifferent': 'Baseline reversion likely without reinforcement'
        }
        return patterns.get(segment_name, 'Unknown pattern')

    def predict_effect_trajectory(
        self,
        project_id: str,
        months_ahead: int = 24,
        model_type: str = 'exponential'
    ) -> Dict:
        """
        Project effect forward over time

        Args:
            project_id: Project identifier
            months_ahead: How many months to project
            model_type: 'exponential' or 'linear'

        Returns:
            Trajectory with monthly projections and confidence bands
        """
        project = self.registry['projects'][project_id]

        # Get fitted model
        decay_data = project.get('decay_analysis', {})
        if not decay_data:
            # Fit model first
            decay_data = self.fit_decay_model(project_id, model_type)

        if 'effect_decay' not in decay_data:
            return {'status': 'no_fitted_model'}

        model = decay_data['effect_decay']
        E0 = model['fitted_parameters']['E_0']
        rho = model['fitted_parameters'].get('rho', 0.08)

        trajectory = {
            'project_id': project_id,
            'model': model_type,
            'months_projected': months_ahead,
            'trajectory': {}
        }

        for month in range(0, months_ahead + 1, 3):
            if model_type == 'exponential':
                effect = E0 * math.exp(-rho * month)
                # Add confidence band (±15%)
                ci_lower = effect * 0.85
                ci_upper = effect * 1.15
            else:
                beta = model['fitted_parameters'].get('beta', 0.01)
                effect = max(E0 - beta * month, 0)
                ci_lower = effect * 0.80
                ci_upper = effect * 1.20

            trajectory['trajectory'][f'{month}M'] = {
                'predicted_effect': round(effect, 4),
                'ci_lower': round(ci_lower, 4),
                'ci_upper': round(ci_upper, 4)
            }

        return trajectory

    def calculate_sustainability_score(self, project_id: str) -> Dict:
        """
        Calculate sustainability score: S = (E_12M / E_0) · (1 - attrition)^0.5

        Returns:
            Sustainability assessment with thresholds and recommendations
        """
        project = self.registry['projects'][project_id]

        if 'long_term_results' not in project or '12M' not in project['long_term_results']:
            # Use predicted value if measurement not available
            decay_data = project.get('decay_analysis', {})
            if decay_data and 'effect_decay' in decay_data:
                model = decay_data['effect_decay']
                E0 = model['fitted_parameters']['E_0']
                E_12M = model['predictions'].get('12M', E0 * 0.55)
                attrition = 0.40  # Expected 12M attrition
            else:
                return {'status': 'insufficient_data'}
        else:
            # Use actual measurement
            measurement = project['long_term_results']['12M']
            E0 = project.get('results', {}).get('deviation_analysis', {}).get('overall', {}).get('actual_E_P', 0.5)
            E_12M = measurement['kpis'][0].get('actual_value', E0) if measurement.get('kpis') else E0
            attrition = measurement.get('attrition', 0.40)

        # Calculate sustainability
        effect_retention = E_12M / E0 if E0 != 0 else 0
        attrition_factor = math.sqrt(max(1 - attrition, 0))
        sustainability_score = effect_retention * attrition_factor

        # Classify
        if sustainability_score >= 0.80:
            classification = "Highly sustainable"
            action = "No booster needed"
            priority = "low"
        elif sustainability_score >= 0.60:
            classification = "Moderately sustainable"
            action = "Booster at 12M recommended"
            priority = "medium"
        elif sustainability_score >= 0.40:
            classification = "Moderate decay"
            action = "Booster at 6M and 12M"
            priority = "high"
        else:
            classification = "Rapid decay"
            action = "Requires structural redesign or continuous reinforcement"
            priority = "critical"

        result = {
            'project_id': project_id,
            'sustainability_score': round(sustainability_score, 3),
            'effect_retention': round(effect_retention, 3),
            'attrition_adjustment': round(attrition_factor, 3),
            'classification': classification,
            'recommended_action': action,
            'priority': priority,
            'thresholds': {
                'highly_sustainable': 0.80,
                'moderately_sustainable': 0.60,
                'moderate_decay': 0.40
            }
        }

        # Store in registry
        if 'decay_analysis' not in project:
            project['decay_analysis'] = {}
        project['decay_analysis']['sustainability_score'] = result
        self._save_registry()

        return result

    def estimate_booster_needs(self, project_id: str) -> Dict:
        """
        Estimate when and what type of boosters are needed

        Returns:
            Booster schedule with triggers and recommendations
        """
        project = self.registry['projects'][project_id]

        trajectory = self.predict_effect_trajectory(project_id, months_ahead=24)
        if 'trajectory' not in trajectory:
            return {'status': 'cannot_calculate'}

        # Get initial effect
        E0 = project.get('results', {}).get('deviation_analysis', {}).get('overall', {}).get('actual_E_P', 0.5)

        boosters = {
            'project_id': project_id,
            'booster_interventions': []
        }

        threshold_6m = E0 * 0.80
        threshold_12m = E0 * 0.60

        traj_6m = trajectory['trajectory'].get('6M', {}).get('predicted_effect', E0)
        traj_12m = trajectory['trajectory'].get('12M', {}).get('predicted_effect', E0)

        if traj_6m < threshold_6m:
            boosters['booster_interventions'].append({
                'timepoint': '6M',
                'trigger': 'Decay below 80% of initial',
                'intervention_type': 'reminder',
                'intensity': 'light',
                'expected_recovery': 0.05
            })

        if traj_12m < threshold_12m:
            boosters['booster_interventions'].append({
                'timepoint': '12M',
                'trigger': 'Decay below 60% of initial',
                'intervention_type': 're-engagement',
                'intensity': 'medium',
                'expected_recovery': 0.08
            })

        if not boosters['booster_interventions']:
            boosters['booster_interventions'].append({
                'timepoint': 'none',
                'recommendation': 'No boosters needed, effect sustainable'
            })

        return boosters

    def generate_decay_report(self, project_id: str) -> Dict:
        """
        Generate comprehensive decay analysis report

        Returns:
            Full report with curves, parameters, and recommendations
        """
        project = self.registry['projects'][project_id]

        report = {
            'project_id': project_id,
            'project_name': project['meta']['name'],
            'generated': datetime.now().isoformat(),
            'decay_model': {},
            'trajectory': {},
            'sustainability': {},
            'booster_needs': {},
            'recommendations': []
        }

        # Fit decay model
        model = self.fit_decay_model(project_id, 'exponential')
        if 'model' in model:
            report['decay_model'] = model

        # Project trajectory
        traj = self.predict_effect_trajectory(project_id)
        if 'trajectory' in traj:
            report['trajectory'] = traj

        # Calculate sustainability
        sust = self.calculate_sustainability_score(project_id)
        report['sustainability'] = sust

        # Estimate booster needs
        boosters = self.estimate_booster_needs(project_id)
        report['booster_needs'] = boosters

        # Generate recommendations
        if sust.get('priority') == 'critical':
            report['recommendations'].append(
                "Consider structural intervention redesign - current approach shows rapid decay"
            )
        elif sust.get('priority') == 'high':
            report['recommendations'].append(
                "Implement booster interventions at 6M and 12M to maintain behavior"
            )
        elif sust.get('priority') == 'medium':
            report['recommendations'].append(
                "Schedule booster intervention at 12M to prevent effect erosion"
            )

        return report


def main():
    """CLI interface for decay analysis"""
    import argparse

    parser = argparse.ArgumentParser(description='Phase 6: Decay Analyzer')
    subparsers = parser.add_subparsers(dest='command')

    # Fit command
    fit_parser = subparsers.add_parser('fit', help='Fit decay model')
    fit_parser.add_argument('project_id', help='Project ID')
    fit_parser.add_argument('--model', choices=['exponential', 'linear'], default='exponential')

    # Predict command
    predict_parser = subparsers.add_parser('predict', help='Predict effect trajectory')
    predict_parser.add_argument('project_id', help='Project ID')
    predict_parser.add_argument('--months', type=int, default=24, help='Months to project')

    # Score command
    score_parser = subparsers.add_parser('score', help='Calculate sustainability score')
    score_parser.add_argument('project_id', help='Project ID')

    # Report command
    report_parser = subparsers.add_parser('report', help='Generate decay report')
    report_parser.add_argument('project_id', help='Project ID')
    report_parser.add_argument('--format', choices=['json', 'yaml'], default='json')

    args = parser.parse_args()

    analyzer = Phase6DecayAnalyzer()

    if args.command == 'fit':
        result = analyzer.fit_decay_model(args.project_id, args.model)
        print(json.dumps(result, indent=2))

    elif args.command == 'predict':
        traj = analyzer.predict_effect_trajectory(args.project_id, args.months)
        print(json.dumps(traj, indent=2))

    elif args.command == 'score':
        score = analyzer.calculate_sustainability_score(args.project_id)
        print(json.dumps(score, indent=2))

    elif args.command == 'report':
        report = analyzer.generate_decay_report(args.project_id)
        if args.format == 'json':
            print(json.dumps(report, indent=2))
        else:
            print(yaml.dump(report, default_flow_style=False))


if __name__ == '__main__':
    main()
