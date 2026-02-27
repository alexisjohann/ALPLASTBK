#!/usr/bin/env python3
"""
Phase 6: Learnings Extractor
Extracts meta-learnings from long-term outcome tracking data

Components:
- Sustainability pattern analysis
- Decay parameter updates for Appendix BBB
- Booster effectiveness analysis
- Behavioral pattern extraction
- Cross-project meta-analysis
"""

import yaml
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from collections import defaultdict


class Phase6LearningsExtractor:
    """Extract insights from long-term tracking data"""

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

    def extract_sustainability_patterns(
        self,
        domain: Optional[str] = None,
        intervention_type: Optional[str] = None
    ) -> Dict:
        """
        Extract sustainability patterns across projects

        Args:
            domain: Filter by domain (finance, health, energy, workplace)
            intervention_type: Filter by intervention type (nudge, social, information, etc.)

        Returns:
            Pattern analysis with generalizable insights
        """
        patterns = {
            'domain': domain,
            'intervention_type': intervention_type,
            'projects_analyzed': [],
            'sustainability_by_intervention': defaultdict(list),
            'sustainability_by_domain': defaultdict(list),
            'key_patterns': []
        }

        for project_id, project in self.registry.get('projects', {}).items():
            # Filter by domain
            if domain and project['meta'].get('domain') != domain:
                continue

            # Check if project has long-term results
            if 'long_term_results' not in project or '12M' not in project['long_term_results']:
                continue

            patterns['projects_analyzed'].append(project_id)

            # Extract sustainability for each intervention
            for intervention in project.get('intervention_mix', []):
                int_type = intervention.get('type')
                if intervention_type and int_type != intervention_type:
                    continue

                # Get effect retention
                measurement = project['long_term_results']['12M']
                effect_retention = measurement['kpis'][0].get('delta_vs_prediction', 0) if measurement.get('kpis') else 0

                patterns['sustainability_by_intervention'][int_type].append({
                    'project_id': project_id,
                    'effect_retention_12M': effect_retention,
                    'description': intervention.get('description', '')
                })

            # Track by domain
            domain_key = project['meta'].get('domain', 'unknown')
            patterns['sustainability_by_domain'][domain_key].append({
                'project_id': project_id,
                'sustainability_score': (
                    project.get('decay_analysis', {}).get('sustainability_score', {}).get('sustainability_score', 0)
                )
            })

        # Generate insights
        patterns['key_patterns'] = self._synthesize_patterns(patterns)

        return patterns

    def _synthesize_patterns(self, patterns: Dict) -> List[Dict]:
        """Synthesize key patterns from data"""
        insights = []

        # Analyze by intervention type
        for int_type, data in patterns['sustainability_by_intervention'].items():
            if data:
                avg_retention = sum(d['effect_retention_12M'] for d in data) / len(data)
                insights.append({
                    'pattern': f'{int_type.upper()} interventions',
                    'average_effect_retention_12M': round(avg_retention, 3),
                    'n_projects': len(data),
                    'assessment': self._assess_retention(avg_retention)
                })

        # Analyze by domain
        for domain_key, data in patterns['sustainability_by_domain'].items():
            if data:
                avg_score = sum(d['sustainability_score'] for d in data) / len(data)
                insights.append({
                    'pattern': f'{domain_key.upper()} domain',
                    'average_sustainability_score': round(avg_score, 3),
                    'n_projects': len(data),
                    'assessment': self._assess_sustainability(avg_score)
                })

        return insights

    def _assess_retention(self, retention: float) -> str:
        """Assess effect retention level"""
        if retention >= 0.85:
            return "Excellent - effect sustained"
        elif retention >= 0.70:
            return "Good - minor decay"
        elif retention >= 0.50:
            return "Moderate - noticeable decay"
        else:
            return "Poor - significant decay"

    def _assess_sustainability(self, score: float) -> str:
        """Assess sustainability score"""
        if score >= 0.80:
            return "Highly sustainable"
        elif score >= 0.60:
            return "Moderately sustainable"
        elif score >= 0.40:
            return "Moderate decay"
        else:
            return "Rapid decay"

    def update_decay_parameters(self, project_id: str) -> Dict:
        """
        Update decay rate parameters (ρ) in Appendix BBB

        Args:
            project_id: Project with new long-term data

        Returns:
            Parameter updates with evidence basis
        """
        if project_id not in self.registry['projects']:
            raise ValueError(f"Project {project_id} not found")

        project = self.registry['projects'][project_id]

        if 'decay_analysis' not in project or 'effect_decay' not in project['decay_analysis']:
            return {'status': 'no_decay_model'}

        model = project['decay_analysis']['effect_decay']
        rho = model['fitted_parameters'].get('rho', None)

        if not rho:
            return {'status': 'cannot_extract_rho'}

        updates = {
            'project_id': project_id,
            'parameter_updates': [],
            'evidence_basis': f"Long-term tracking for {project['meta']['name']}"
        }

        # Update by intervention type
        for intervention in project.get('intervention_mix', []):
            int_type = intervention.get('type')
            updates['parameter_updates'].append({
                'parameter': f'ρ (decay rate) for {int_type}',
                'new_value': rho,
                'confidence': model['model_fit'].get('model_quality', 'medium'),
                'basis': f"{project_id} - {project['meta']['domain']} domain",
                'n_observations': model['model_fit'].get('n_observations', 1)
            })

        # Store update recommendations
        if 'long_term_learnings' not in project:
            project['long_term_learnings'] = {}

        project['long_term_learnings']['parameter_updates'] = updates['parameter_updates']
        self._save_registry()

        return updates

    def identify_booster_effectiveness(self, project_id: str) -> Dict:
        """
        Analyze effectiveness of booster interventions

        Args:
            project_id: Project with booster data

        Returns:
            Assessment of booster impact
        """
        if project_id not in self.registry['projects']:
            raise ValueError(f"Project {project_id} not found")

        project = self.registry['projects'][project_id]

        analysis = {
            'project_id': project_id,
            'boosters_implemented': [],
            'effectiveness_analysis': []
        }

        # Check if boosters were scheduled
        schedule = project.get('follow_up_schedule', {})
        booster_points = schedule.get('booster_intervention_points', [])

        if not booster_points:
            analysis['status'] = 'no_boosters_scheduled'
            return analysis

        # Analyze each booster
        for booster in booster_points:
            timepoint = booster.get('timepoint')
            trigger = booster.get('trigger_condition')
            intervention_type = booster.get('intervention_type')

            effectiveness_entry = {
                'timepoint': timepoint,
                'intervention_type': intervention_type,
                'trigger': trigger
            }

            # Check if measurement exists post-booster
            measurements = project.get('long_term_results', {})
            if timepoint in measurements:
                measurement = measurements[timepoint]
                effectiveness_entry['effect_recovery'] = (
                    measurement['kpis'][0].get('delta_vs_prediction', 0) if measurement.get('kpis') else 0
                )
                effectiveness_entry['assessment'] = 'measured'
            else:
                effectiveness_entry['assessment'] = 'pending_measurement'

            analysis['boosters_implemented'].append({
                'type': intervention_type,
                'timepoint': timepoint
            })
            analysis['effectiveness_analysis'].append(effectiveness_entry)

        return analysis

    def extract_behavioral_patterns(
        self,
        project_id: str,
        segment: Optional[str] = None
    ) -> Dict:
        """
        Extract behavioral patterns by segment over time

        Args:
            project_id: Project to analyze
            segment: Optional segment name filter

        Returns:
            Behavioral trajectories by segment
        """
        if project_id not in self.registry['projects']:
            raise ValueError(f"Project {project_id} not found")

        project = self.registry['projects'][project_id]

        patterns = {
            'project_id': project_id,
            'segments_analyzed': [],
            'behavioral_trajectories': {}
        }

        segments = project.get('context', {}).get('segments', [])
        if not segments:
            return {'status': 'no_segments_defined'}

        # Analyze each segment
        for seg in segments:
            seg_name = seg['name']
            if segment and seg_name != segment:
                continue

            patterns['segments_analyzed'].append(seg_name)

            trajectory = {
                'segment_name': seg_name,
                'proportion': seg.get('proportion', 0),
                'heterogeneity_sigma': seg.get('sigma', 0),
                'response_timeline': []
            }

            # Collect response data by timepoint
            predictions = project.get('predictions', {})
            if 'kpis' in predictions:
                trajectory['response_timeline'].append({
                    'timepoint': '0M (prediction)',
                    'predicted_response': predictions['kpis'][0].get('predicted_delta_pct', 0)
                })

            # Add actual measurements
            for timepoint in ['3M', '6M', '12M', '24M']:
                if timepoint in project.get('long_term_results', {}):
                    measurement = project['long_term_results'][timepoint]
                    # Try to extract segment-specific response
                    decay_data = project.get('decay_analysis', {})
                    segment_decay = decay_data.get('by_segment', {}).get(seg_name, {})

                    trajectory['response_timeline'].append({
                        'timepoint': timepoint,
                        'actual_measurement': measurement.get('measurement_date'),
                        'estimated_decay_rate': segment_decay.get('rho', 0.08)
                    })

            patterns['behavioral_trajectories'][seg_name] = trajectory

        return patterns

    def generate_meta_analysis(
        self,
        domains: Optional[List[str]] = None,
        years: Optional[int] = None
    ) -> Dict:
        """
        Generate cross-project meta-analysis

        Args:
            domains: Filter by domains (health, finance, energy, workplace)
            years: Minimum years of data per project

        Returns:
            Cross-project synthesis with generalizable insights
        """
        meta = {
            'analysis_date': datetime.now().isoformat(),
            'domains_included': domains,
            'minimum_years_data': years,
            'projects_in_analysis': [],
            'aggregate_findings': {},
            'generalizable_patterns': []
        }

        # Collect data from all relevant projects
        project_data = []

        for project_id, project in self.registry.get('projects', {}).items():
            # Filter by domain
            proj_domain = project['meta'].get('domain')
            if domains and proj_domain not in domains:
                continue

            # Check long-term data availability
            if 'long_term_results' not in project:
                continue

            meta['projects_in_analysis'].append(project_id)
            project_data.append({
                'project_id': project_id,
                'domain': proj_domain,
                'sustainability': project.get('decay_analysis', {}).get('sustainability_score', {}).get('sustainability_score', 0),
                'avg_prediction_accuracy': 0  # Would calculate from deviation analysis
            })

        # Generate aggregate findings
        if project_data:
            avg_sustainability = sum(p['sustainability'] for p in project_data) / len(project_data)
            domains_represented = set(p['domain'] for p in project_data)

            meta['aggregate_findings'] = {
                'n_projects': len(project_data),
                'domains_represented': list(domains_represented),
                'average_sustainability_score': round(avg_sustainability, 3),
                'sustainability_assessment': self._assess_sustainability(avg_sustainability)
            }

            # Extract generalizable patterns
            if avg_sustainability >= 0.70:
                meta['generalizable_patterns'].append({
                    'pattern': 'Strong intervention-based behavior change sustainability',
                    'generalizability': 'across domains',
                    'confidence': 'high' if len(project_data) >= 5 else 'medium'
                })

            if len(domains_represented) > 1:
                meta['generalizable_patterns'].append({
                    'pattern': 'Sustainability patterns consistent across domains',
                    'domains': list(domains_represented),
                    'confidence': 'medium' if len(project_data) >= 3 else 'low'
                })

        return meta

    def recommend_maintenance_strategies(self, project_id: str) -> Dict:
        """
        Recommend maintenance and sustainability strategies

        Args:
            project_id: Project to analyze

        Returns:
            Tailored maintenance recommendations
        """
        if project_id not in self.registry['projects']:
            raise ValueError(f"Project {project_id} not found")

        project = self.registry['projects'][project_id]

        recommendations = {
            'project_id': project_id,
            'analysis_date': datetime.now().isoformat(),
            'sustainability_assessment': {},
            'maintenance_strategies': []
        }

        # Get sustainability score
        sustainability = project.get('decay_analysis', {}).get('sustainability_score', {})
        if sustainability:
            recommendations['sustainability_assessment'] = {
                'score': sustainability.get('sustainability_score', 0),
                'classification': sustainability.get('classification', 'unknown'),
                'current_status': sustainability.get('recommended_action', '')
            }

        # Analyze decay model
        decay_model = project.get('decay_analysis', {}).get('effect_decay', {})
        if decay_model:
            rho = decay_model['fitted_parameters'].get('rho', 0.08)

            if rho < 0.05:
                recommendations['maintenance_strategies'].append({
                    'strategy': 'Structural Maintenance',
                    'description': 'Effect very sustainable (slow decay). Ensure structural changes persist.',
                    'actions': [
                        'Maintain default/choice architecture',
                        'Monitor for policy changes',
                        'Annual check-in'
                    ],
                    'cost': 'low',
                    'frequency': 'annual'
                })
            elif rho < 0.10:
                recommendations['maintenance_strategies'].append({
                    'strategy': 'Light Reinforcement',
                    'description': 'Moderate sustainability. Light reminders help maintain behavior.',
                    'actions': [
                        'Annual reminder campaign',
                        'Celebrate continued participation',
                        'Update materials if needed'
                    ],
                    'cost': 'low',
                    'frequency': 'annual'
                })
            else:
                recommendations['maintenance_strategies'].append({
                    'strategy': 'Regular Booster Cycle',
                    'description': 'Significant decay detected. Regular boosters needed.',
                    'actions': [
                        'Implement booster at 6M intervals',
                        'Vary booster type to prevent habituation',
                        'Increase social reinforcement'
                    ],
                    'cost': 'medium',
                    'frequency': 'semi-annual'
                })

        # Segment-specific recommendations
        segments = project.get('context', {}).get('segments', [])
        if segments:
            recommendations['segment_specific_strategies'] = {}

            for segment in segments:
                seg_name = segment['name']
                seg_decay = project.get('decay_analysis', {}).get('by_segment', {}).get(seg_name, {})

                if seg_decay.get('rho', 0.08) > 0.12:
                    recommendations['segment_specific_strategies'][seg_name] = {
                        'concern': 'Higher decay rate',
                        'recommendation': f'Prioritize {seg_name} for booster interventions',
                        'intervention_focus': 'Re-engagement and social reinforcement'
                    }

        return recommendations

    def generate_learnings_report(self, project_id: Optional[str] = None) -> Dict:
        """
        Generate comprehensive learnings report

        Args:
            project_id: Single project or None for cross-project

        Returns:
            Full learnings report
        """
        report = {
            'generated': datetime.now().isoformat(),
            'report_type': 'single_project' if project_id else 'cross_project',
            'key_findings': [],
            'parameter_updates': [],
            'recommendations': []
        }

        if project_id:
            # Single project report
            patterns = self.extract_sustainability_patterns()
            effectiveness = self.identify_booster_effectiveness(project_id)
            maintenance = self.recommend_maintenance_strategies(project_id)

            report['project_id'] = project_id
            report['sustainability_patterns'] = patterns
            report['booster_effectiveness'] = effectiveness
            report['maintenance_recommendations'] = maintenance
        else:
            # Cross-project report
            meta = self.generate_meta_analysis()
            report['meta_analysis'] = meta

        return report


def main():
    """CLI interface for learnings extraction"""
    import argparse

    parser = argparse.ArgumentParser(description='Phase 6: Learnings Extractor')
    subparsers = parser.add_subparsers(dest='command')

    # Patterns command
    patterns_parser = subparsers.add_parser('patterns', help='Extract sustainability patterns')
    patterns_parser.add_argument('--domain', help='Filter by domain')
    patterns_parser.add_argument('--intervention-type', help='Filter by intervention type')

    # Update command
    update_parser = subparsers.add_parser('update', help='Update decay parameters')
    update_parser.add_argument('project_id', help='Project ID')

    # Booster command
    booster_parser = subparsers.add_parser('booster', help='Analyze booster effectiveness')
    booster_parser.add_argument('project_id', help='Project ID')

    # Behavior command
    behavior_parser = subparsers.add_parser('behavior', help='Extract behavioral patterns')
    behavior_parser.add_argument('project_id', help='Project ID')
    behavior_parser.add_argument('--segment', help='Filter by segment')

    # Meta command
    meta_parser = subparsers.add_parser('meta', help='Generate meta-analysis')
    meta_parser.add_argument('--domains', nargs='+', help='Domains to include')

    # Maintenance command
    maint_parser = subparsers.add_parser('maintenance', help='Get maintenance recommendations')
    maint_parser.add_argument('project_id', help='Project ID')

    # Report command
    report_parser = subparsers.add_parser('report', help='Generate learnings report')
    report_parser.add_argument('--project-id', help='Optional single project')
    report_parser.add_argument('--format', choices=['json', 'yaml'], default='json')

    args = parser.parse_args()

    extractor = Phase6LearningsExtractor()

    if args.command == 'patterns':
        result = extractor.extract_sustainability_patterns(args.domain, args.intervention_type)
        print(json.dumps(result, indent=2, default=str))

    elif args.command == 'update':
        result = extractor.update_decay_parameters(args.project_id)
        print(json.dumps(result, indent=2))

    elif args.command == 'booster':
        result = extractor.identify_booster_effectiveness(args.project_id)
        print(json.dumps(result, indent=2))

    elif args.command == 'behavior':
        result = extractor.extract_behavioral_patterns(args.project_id, args.segment)
        print(json.dumps(result, indent=2))

    elif args.command == 'meta':
        result = extractor.generate_meta_analysis(args.domains)
        print(json.dumps(result, indent=2))

    elif args.command == 'maintenance':
        result = extractor.recommend_maintenance_strategies(args.project_id)
        print(json.dumps(result, indent=2))

    elif args.command == 'report':
        result = extractor.generate_learnings_report(args.project_id)
        if args.format == 'json':
            print(json.dumps(result, indent=2, default=str))
        else:
            print(yaml.dump(result, default_flow_style=False))


if __name__ == '__main__':
    main()
