#!/usr/bin/env python3
"""
Phase 6: Long-Term Outcomes Tracker
Manages follow-up measurement scheduling and data collection

Components:
- Follow-up schedule creation
- Measurement recording
- Attrition tracking
- Decay threshold detection
"""

import yaml
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class Phase6LongTermTracker:
    """Manage long-term outcome tracking and follow-up measurements"""

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

    def schedule_follow_up(
        self,
        project_id: str,
        timepoints: Optional[List[Dict]] = None
    ) -> Dict:
        """
        Schedule follow-up measurements for a project

        Args:
            project_id: Project identifier (e.g., 'PRJ-001')
            timepoints: List of timepoint dicts with 'timepoint', 'measurement_type',
                       'target_metrics', 'sample_size_pct', 'priority'

        Returns:
            Schedule document with measurement dates and details
        """
        if project_id not in self.registry['projects']:
            raise ValueError(f"Project {project_id} not found")

        project = self.registry['projects'][project_id]

        if timepoints is None:
            # Default schedule: 3M, 6M, 12M, 24M
            timepoints = self._get_default_schedule()

        # Calculate measurement dates based on intervention end date
        end_date = datetime.fromisoformat(project['meta']['end_date'])
        schedule = {
            'created': datetime.now().isoformat(),
            'measurement_points': []
        }

        for tp in timepoints:
            months_offset = int(tp['timepoint'].rstrip('M'))
            measurement_date = end_date + timedelta(days=30*months_offset)

            schedule['measurement_points'].append({
                'timepoint': tp['timepoint'],
                'scheduled_date': measurement_date.isoformat(),
                'measurement_type': tp.get('measurement_type', 'survey'),
                'target_metrics': tp.get('target_metrics', []),
                'sample_size_pct': tp.get('sample_size_pct', 1.0),
                'priority': tp.get('priority', 'medium'),
                'status': 'pending'
            })

        # Store in registry
        if 'follow_up_schedule' not in project:
            project['follow_up_schedule'] = {}

        project['follow_up_schedule']['measurement_points'] = schedule['measurement_points']
        self._save_registry()

        return schedule

    def _get_default_schedule(self) -> List[Dict]:
        """Get default follow-up schedule"""
        return [
            {
                'timepoint': '3M',
                'measurement_type': 'survey',
                'target_metrics': ['participation_rate', 'satisfaction', 'behavior_frequency'],
                'sample_size_pct': 0.8,
                'priority': 'high'
            },
            {
                'timepoint': '6M',
                'measurement_type': 'administrative',
                'target_metrics': ['participation_rate', 'usage_frequency'],
                'sample_size_pct': 1.0,
                'priority': 'high'
            },
            {
                'timepoint': '12M',
                'measurement_type': 'survey',
                'target_metrics': ['participation_rate', 'satisfaction', 'relapse_likelihood'],
                'sample_size_pct': 0.6,
                'priority': 'medium'
            },
            {
                'timepoint': '24M',
                'measurement_type': 'survey',
                'target_metrics': ['participation_rate', 'behavior_naturalization', 'recommendations'],
                'sample_size_pct': 0.4,
                'priority': 'low'
            }
        ]

    def record_measurement(
        self,
        project_id: str,
        timepoint: str,
        kpis: Dict,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Record measurement data at a specific timepoint

        Args:
            project_id: Project identifier
            timepoint: '3M', '6M', '12M', or '24M'
            kpis: Dict of KPI names to actual values
            metadata: Optional metadata (sample_size, coverage, attrition, etc.)

        Returns:
            Recorded measurement with metadata
        """
        if project_id not in self.registry['projects']:
            raise ValueError(f"Project {project_id} not found")

        project = self.registry['projects'][project_id]

        if 'long_term_results' not in project:
            project['long_term_results'] = {}

        # Format measurement
        measurement = {
            'measurement_date': datetime.now().isoformat().split('T')[0],
            'sample_size': metadata.get('sample_size', None) if metadata else None,
            'coverage': metadata.get('coverage', 1.0) if metadata else 1.0,
            'attrition': metadata.get('attrition', 0.0) if metadata else 0.0,
            'kpis': []
        }

        # Process KPIs
        for kpi_name, actual_value in kpis.items():
            kpi_record = {
                'name': kpi_name,
                'actual_value': actual_value
            }

            # Calculate delta vs prediction if available
            if 'predictions' in project and 'kpis' in project['predictions']:
                for pred_kpi in project['predictions']['kpis']:
                    if pred_kpi['name'] == kpi_name:
                        kpi_record['delta_vs_prediction'] = (
                            actual_value - pred_kpi.get('predicted_value', actual_value)
                        )
                        break

            measurement['kpis'].append(kpi_record)

        # Store measurement
        project['long_term_results'][timepoint] = measurement

        # Update schedule status
        if 'follow_up_schedule' in project:
            for mp in project['follow_up_schedule'].get('measurement_points', []):
                if mp['timepoint'] == timepoint:
                    mp['status'] = 'completed'
                    break

        self._save_registry()

        return measurement

    def detect_attrition(
        self,
        project_id: str,
        timepoint: str,
        actual_sample: int
    ) -> Tuple[bool, str]:
        """
        Detect unexpected attrition patterns

        Args:
            project_id: Project identifier
            timepoint: Measurement timepoint
            actual_sample: Actual sample size achieved

        Returns:
            Tuple of (is_unexpected, explanation)
        """
        project = self.registry['projects'][project_id]
        baseline_sample = project['context']['sample_size']

        # Expected attrition by timepoint
        expected_attrition = {
            '3M': 0.20,
            '6M': 0.00,
            '12M': 0.40,
            '24M': 0.60
        }

        attrition_rate = 1 - (actual_sample / baseline_sample)
        expected_attrition_rate = expected_attrition.get(timepoint, 0.30)

        # Flag if actual attrition is 10pp higher than expected
        is_unexpected = attrition_rate > (expected_attrition_rate + 0.10)

        explanation = (
            f"Baseline: {baseline_sample}, Actual: {actual_sample}, "
            f"Attrition: {attrition_rate:.1%} (expected: {expected_attrition_rate:.1%})"
        )

        if is_unexpected:
            explanation += " ⚠ Higher than expected attrition"

        return is_unexpected, explanation

    def check_decay_threshold(
        self,
        project_id: str,
        timepoint: str
    ) -> Dict:
        """
        Evaluate if decay triggers booster intervention

        Args:
            project_id: Project identifier
            timepoint: Current timepoint

        Returns:
            Assessment with booster recommendation
        """
        project = self.registry['projects'][project_id]

        if 'long_term_results' not in project or timepoint not in project['long_term_results']:
            return {'status': 'no_measurement_yet'}

        measurement = project['long_term_results'][timepoint]
        initial_effect = project.get('results', {}).get('deviation_analysis', {}).get('overall', {}).get('actual_E_P', None)

        if not initial_effect:
            return {'status': 'insufficient_data'}

        # Get current effect from KPIs
        current_effect = None
        for kpi in measurement['kpis']:
            if 'delta_vs_prediction' in kpi:
                current_effect = kpi['delta_vs_prediction']
                break

        if not current_effect:
            return {'status': 'cannot_calculate_effect'}

        effect_retention_pct = current_effect / initial_effect if initial_effect != 0 else 0

        # Booster thresholds
        booster_recommendation = {
            'timepoint': timepoint,
            'effect_retention_pct': effect_retention_pct,
            'trigger_booster': False,
            'booster_type': None,
            'urgency': 'none'
        }

        if effect_retention_pct < 0.60:
            booster_recommendation['trigger_booster'] = True
            booster_recommendation['booster_type'] = 're-engagement'
            booster_recommendation['urgency'] = 'high'
        elif effect_retention_pct < 0.80:
            booster_recommendation['trigger_booster'] = True
            booster_recommendation['booster_type'] = 'reminder'
            booster_recommendation['urgency'] = 'medium'

        return booster_recommendation

    def generate_follow_up_report(self, project_id: str) -> Dict:
        """
        Generate summary of follow-up measurements vs predictions

        Returns:
            Report with all measurements, deviations, and recommendations
        """
        if project_id not in self.registry['projects']:
            raise ValueError(f"Project {project_id} not found")

        project = self.registry['projects'][project_id]

        report = {
            'project_id': project_id,
            'project_name': project['meta']['name'],
            'generated': datetime.now().isoformat(),
            'summary': {},
            'measurements': {},
            'attrition_analysis': {},
            'booster_recommendations': []
        }

        if 'long_term_results' not in project:
            report['summary']['status'] = 'No measurements recorded'
            return report

        # Compile measurements
        for timepoint, measurement in project['long_term_results'].items():
            report['measurements'][timepoint] = measurement

            # Check attrition
            if measurement.get('sample_size'):
                is_unexpected, explanation = self.detect_attrition(
                    project_id, timepoint, measurement['sample_size']
                )
                report['attrition_analysis'][timepoint] = {
                    'unexpected': is_unexpected,
                    'explanation': explanation
                }

            # Check decay
            decay_check = self.check_decay_threshold(project_id, timepoint)
            if decay_check.get('trigger_booster'):
                report['booster_recommendations'].append(
                    {
                        'timepoint': timepoint,
                        'type': decay_check['booster_type'],
                        'urgency': decay_check['urgency']
                    }
                )

        report['summary']['measurements_recorded'] = len(report['measurements'])
        report['summary']['boosters_needed'] = len(report['booster_recommendations'])

        return report

    def get_pending_measurements(self) -> List[Dict]:
        """
        Get all pending measurements across all projects

        Returns:
            List of pending measurements with due dates
        """
        pending = []

        for project_id, project in self.registry.get('projects', {}).items():
            if 'follow_up_schedule' not in project:
                continue

            for mp in project['follow_up_schedule'].get('measurement_points', []):
                if mp['status'] == 'pending':
                    pending.append({
                        'project_id': project_id,
                        'project_name': project['meta']['name'],
                        'timepoint': mp['timepoint'],
                        'scheduled_date': mp['scheduled_date'],
                        'priority': mp['priority'],
                        'target_metrics': mp['target_metrics']
                    })

        # Sort by date
        pending.sort(key=lambda x: x['scheduled_date'])
        return pending


def main():
    """CLI interface for Phase 6 outcomes tracking"""
    import argparse

    parser = argparse.ArgumentParser(description='Phase 6: Long-Term Outcomes Tracker')
    subparsers = parser.add_subparsers(dest='command')

    # Schedule command
    schedule_parser = subparsers.add_parser('schedule', help='Schedule follow-up measurements')
    schedule_parser.add_argument('project_id', help='Project ID (e.g., PRJ-001)')
    schedule_parser.add_argument('--custom', type=str, help='Custom schedule JSON file')

    # Record command
    record_parser = subparsers.add_parser('record', help='Record measurement data')
    record_parser.add_argument('project_id', help='Project ID')
    record_parser.add_argument('timepoint', help='Timepoint (3M, 6M, 12M, 24M)')
    record_parser.add_argument('--file', type=str, help='JSON file with KPI data')
    record_parser.add_argument('--sample-size', type=int, help='Sample size achieved')

    # Report command
    report_parser = subparsers.add_parser('report', help='Generate follow-up report')
    report_parser.add_argument('project_id', help='Project ID')
    report_parser.add_argument('--format', choices=['json', 'yaml'], default='json')

    # Pending command
    pending_parser = subparsers.add_parser('pending', help='List pending measurements')

    args = parser.parse_args()

    tracker = Phase6LongTermTracker()

    if args.command == 'schedule':
        print(f"Scheduling follow-ups for {args.project_id}...")
        schedule = tracker.schedule_follow_up(args.project_id)
        print(json.dumps(schedule, indent=2))

    elif args.command == 'record':
        print(f"Recording measurement for {args.project_id} at {args.timepoint}...")
        # Load KPI data from file or stdin
        if args.file:
            with open(args.file) as f:
                kpis = json.load(f)
        else:
            kpis = json.loads(input("Enter KPI data (JSON): "))

        metadata = {}
        if args.sample_size:
            metadata['sample_size'] = args.sample_size

        result = tracker.record_measurement(args.project_id, args.timepoint, kpis, metadata)
        print(json.dumps(result, indent=2))

    elif args.command == 'report':
        report = tracker.generate_follow_up_report(args.project_id)
        if args.format == 'json':
            print(json.dumps(report, indent=2))
        else:
            print(yaml.dump(report, default_flow_style=False))

    elif args.command == 'pending':
        pending = tracker.get_pending_measurements()
        print(f"Found {len(pending)} pending measurements:\n")
        for p in pending:
            print(f"  {p['project_id']:10} {p['timepoint']:3} {p['scheduled_date'][:10]} "
                  f"({p['priority']}) - {p['project_name'][:30]}")


if __name__ == '__main__':
    main()
