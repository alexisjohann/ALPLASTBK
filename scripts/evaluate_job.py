#!/usr/bin/env python3
"""
CLI Wrapper for Job Analysis Engine
Evaluates job design complexity, automation risk, engagement impact

Usage:
    python scripts/evaluate_job.py ALPLA "Machine Operator" --detail
    python scripts/evaluate_job.py ALPLA "Machine Operator" --impact-on-hr
    python scripts/evaluate_job.py ALPLA "Machine Operator" --scenario "increase_troubleshooting_20pct"

Version: 1.0.0
"""

import sys
import argparse
import json
from pathlib import Path

# Add job_analysis module to path
sys.path.insert(0, str(Path(__file__).parent / "job_analysis"))

from job_analyzer import JobAnalyzer, JobProfile, Task, TaskType

# ============================================================================
# PREDEFINED JOB PROFILES
# ============================================================================

JOB_LIBRARY = {
    "ALPLA_machine_operator": JobProfile(
        company="ALPLA",
        job_title="Machine Operator - Injection Molding",
        location="Salzburg",
        current_wage=13.0,
        tasks=[
            Task(
                task_id="1a",
                name="Feed raw material into hopper",
                time_allocation_pct=20,
                cognitive_load=1,
                motor_skill=2,
                decision_making=0,
                automation_risk=95,
                training_time_days=1,
                skill_level_required=1,
                frequency_per_shift="Every 2 hours",
            ),
            Task(
                task_id="1b",
                name="Remove finished parts from mold",
                time_allocation_pct=20,
                cognitive_load=2,
                motor_skill=3,
                decision_making=1,
                automation_risk=80,
                training_time_days=3,
                skill_level_required=2,
                frequency_per_shift="Every 15 minutes",
            ),
            Task(
                task_id="2a",
                name="Record production metrics",
                time_allocation_pct=10,
                cognitive_load=2,
                motor_skill=1,
                decision_making=0,
                automation_risk=99,
                training_time_days=1,
                skill_level_required=1,
                frequency_per_shift="Hourly",
            ),
            Task(
                task_id="2b",
                name="Visual quality inspection",
                time_allocation_pct=10,
                cognitive_load=3,
                motor_skill=2,
                decision_making=2,
                automation_risk=70,
                training_time_days=7,
                skill_level_required=2,
                frequency_per_shift="Every 30 parts",
            ),
            Task(
                task_id="3a",
                name="Troubleshoot machine jams",
                time_allocation_pct=20,
                cognitive_load=4,
                motor_skill=2,
                decision_making=4,
                automation_risk=15,
                training_time_days=60,
                skill_level_required=3,
                frequency_per_shift="2-3x per shift",
            ),
            Task(
                task_id="3b",
                name="Optimize cycle time parameters",
                time_allocation_pct=5,
                cognitive_load=5,
                motor_skill=1,
                decision_making=5,
                automation_risk=20,
                training_time_days=90,
                skill_level_required=4,
                frequency_per_shift="1-2x per week",
            ),
            Task(
                task_id="4",
                name="Preventive maintenance",
                time_allocation_pct=15,
                cognitive_load=2,
                motor_skill=4,
                decision_making=2,
                automation_risk=25,
                training_time_days=14,
                skill_level_required=3,
                frequency_per_shift="Daily + weekly",
            ),
        ],
    ),
}

# ============================================================================
# OUTPUT FORMATTERS
# ============================================================================

class JobReportFormatter:
    """Format job analysis reports for display"""

    @staticmethod
    def format_summary(report: dict) -> str:
        """Format report as brief summary"""
        output = []

        output.append("╔════════════════════════════════════════════════════════════════════╗")
        output.append(f"║ JOB ANALYSIS REPORT: {report['job_profile']['job_title']:<45} ║")
        output.append(f"║ Company: {report['job_profile']['company']:<59} ║")
        output.append("╚════════════════════════════════════════════════════════════════════╝")
        output.append("")

        # Complexity
        complexity = report['complexity_analysis']['overall_complexity_score']
        output.append(f"COMPLEXITY SCORE: {complexity}/5.0")
        output.append(f"  → {report['complexity_analysis']['interpretation']}")
        output.append("")

        # Automation Risk
        automation = report['automation_risk']['overall_automation_risk_pct']
        output.append(f"AUTOMATION RISK: {automation}%")
        output.append(f"  → {report['automation_risk']['interpretation']}")
        if report['automation_risk']['automatable_tasks_5yr']:
            output.append("  High-risk tasks:")
            for task in report['automation_risk']['automatable_tasks_5yr'][:3]:
                output.append(f"    • {task['task_name']}: {task['automation_risk']}% ({task['time_allocation_pct']}% time)")
        output.append("")

        # Engagement
        engagement = report['engagement_analysis']['overall_engagement_score']
        output.append(f"ENGAGEMENT SCORE: {engagement}/10")
        output.append(f"  → {report['engagement_analysis']['interpretation']}")
        output.append(f"  Breakdown:")
        for factor, score in report['engagement_analysis']['breakdown'].items():
            output.append(f"    • {factor.capitalize()}: {score}/10")
        output.append("")

        # Wage
        output.append(f"WAGE ANALYSIS:")
        output.append(f"  Current wage: €{report['wage_analysis']['current_wage']:.2f}/hr")
        fair_low, fair_high = report['wage_analysis']['fair_wage_range']
        output.append(f"  Fair range: €{fair_low:.2f} - €{fair_high:.2f}/hr")
        output.append(f"  Assessment: {report['wage_analysis']['fairness_assessment']}")
        output.append("")

        # Retention
        output.append(f"RETENTION IMPACT:")
        output.append(f"  Base retention (Phase 6): 58%")
        output.append(f"  Adjusted (job design): {report['retention_impact']['adjusted_retention_pct']}%")
        output.append(f"  Change: {report['retention_impact']['retention_change_pct']:+.1f}pp")
        output.append("")

        # Summary
        output.append(f"JOB QUALITY RATING: {report['summary']['job_quality']}")
        output.append("PRIMARY RISKS:")
        for risk in report['summary']['primary_risks']:
            output.append(f"  • {risk}")
        output.append("")

        # Improvements
        output.append("IMPROVEMENT OPPORTUNITIES:")
        for i, improvement in enumerate(report['summary']['improvement_opportunities'], 1):
            output.append(f"  {i}. {improvement['action']}")
            if 'target' in improvement:
                output.append(f"     Target: {improvement['target']}")
            if 'timeline' in improvement:
                output.append(f"     Timeline: {improvement['timeline']}")

        return "\n".join(output)

    @staticmethod
    def format_detailed(report: dict) -> str:
        """Format report as detailed analysis"""
        output = []

        output.append("╔════════════════════════════════════════════════════════════════════╗")
        output.append(f"║ DETAILED JOB ANALYSIS: {report['job_profile']['job_title']:<42} ║")
        output.append("╚════════════════════════════════════════════════════════════════════╝")
        output.append("")

        # Task Inventory
        output.append("TASK INVENTORY:")
        output.append(f"  Total distinct tasks: {report['task_inventory']['total_tasks']}")
        for i, task_name in enumerate(report['task_inventory']['task_names'], 1):
            output.append(f"  {i}. {task_name}")
        output.append("")

        # Task Composition
        output.append("TASK COMPOSITION (Autor Framework):")
        for task_type, pct in report['task_composition'].items():
            output.append(f"  {task_type}: {pct:.0f}%")
        output.append("")

        # Full Report as JSON
        output.append("FULL ANALYSIS DATA (JSON):")
        output.append(json.dumps(report, indent=2, default=str))

        return "\n".join(output)

    @staticmethod
    def format_impact_on_hr(report: dict) -> str:
        """Format report showing impact on Phase 6 HR decision"""
        output = []

        output.append("╔════════════════════════════════════════════════════════════════════╗")
        output.append("║ IMPACT ON PHASE 6 HR HIRING DECISION                              ║")
        output.append("╚════════════════════════════════════════════════════════════════════╝")
        output.append("")

        output.append("PHASE 6 BASELINE:")
        output.append(f"  P(HR approves hiring) = 84% (based on revenue forecast + capability)")
        output.append("")

        # Calculate adjustments based on job design
        automation = report['automation_risk']['overall_automation_risk_pct']
        complexity = report['complexity_analysis']['overall_complexity_score']
        engagement = report['engagement_analysis']['overall_engagement_score']
        wage_fairness = report['wage_analysis']['fairness_assessment']
        retention = report['retention_impact']['adjusted_retention_pct']

        # Adjustments
        adjustments = 0
        output.append("JOB DESIGN ADJUSTMENTS:")

        # Automation risk adjustment
        if automation > 60:
            adj = -3
            output.append(f"  • High automation risk ({automation}%): {adj:+.0f}pp")
            adjustments += adj

        # Complexity adjustment
        if complexity < 2.5:
            adj = -2
            output.append(f"  • Low complexity ({complexity}/5): {adj:+.0f}pp")
            adjustments += adj
        elif complexity >= 3.5:
            adj = +1
            output.append(f"  • Good complexity ({complexity}/5): {adj:+.0f}pp")
            adjustments += adj

        # Engagement adjustment
        if engagement < 4:
            adj = -2
            output.append(f"  • Low engagement ({engagement}/10): {adj:+.0f}pp")
            adjustments += adj

        # Wage fairness adjustment
        if wage_fairness == "UNDERPAID":
            adj = -2
            output.append(f"  • Wage underpaid vs market: {adj:+.0f}pp")
            adjustments += adj

        # Retention impact
        retention_adj = retention - 58
        if retention_adj != 0:
            output.append(f"  • Retention impact ({retention}%): {retention_adj/10:+.1f}pp")
            adjustments += retention_adj / 10

        output.append("")

        # Final calculation
        baseline = 84
        adjusted = baseline + adjustments
        adjusted = max(50, min(95, adjusted))  # Cap between 50-95%

        output.append(f"PHASE 6.5 ADJUSTED PROBABILITY:")
        output.append(f"  Baseline: {baseline}%")
        output.append(f"  Adjustments: {adjustments:+.1f}pp")
        output.append(f"  ADJUSTED: {adjusted:.0f}%")
        output.append("")

        if adjusted < baseline - 5:
            output.append(f"⚠ WARNING: Job design creates hiring risk")
        elif adjusted > baseline + 5:
            output.append(f"✓ JOB DESIGN SUPPORTS hiring approval")
        else:
            output.append(f"✓ Job design impact is neutral")

        return "\n".join(output)

    @staticmethod
    def format_phase6_integration(report: dict) -> str:
        """Format report showing job design impact on Phase 6 stakeholder simulation"""
        output = []

        output.append("╔════════════════════════════════════════════════════════════════════╗")
        output.append("║ PHASE 6 INTEGRATION: Job Design Impact on Stakeholder Decisions   ║")
        output.append("╚════════════════════════════════════════════════════════════════════╝")
        output.append("")

        # Job design metrics summary
        complexity = report['complexity_analysis']['overall_complexity_score']
        automation = report['automation_risk']['overall_automation_risk_pct']
        engagement = report['engagement_analysis']['overall_engagement_score']
        wage_assessment = report['wage_analysis']['fairness_assessment']

        output.append("JOB DESIGN PROFILE:")
        output.append(f"  Complexity Score: {complexity}/5.0")
        output.append(f"  Automation Risk: {automation}%")
        output.append(f"  Engagement Score: {engagement}/10")
        output.append(f"  Wage Assessment: {wage_assessment}")
        output.append("")

        # HR decision impact (with job metrics)
        output.append("HR DECISION IMPACT (with Job Design):")
        output.append(f"  Phase 6 baseline (without job design): 84%")
        output.append("")

        # Job design factor adjustments (simplified version)
        hr_adjustment = 0
        factors = []

        if complexity < 2.5:
            adj = -2.0
            factors.append(f"  • Low complexity (<2.5): {adj:+.1f}pp (boredom/turnover risk)")
            hr_adjustment += adj
        elif complexity > 3.5:
            adj = 1.0
            factors.append(f"  • High complexity (>3.5): {adj:+.1f}pp (good engagement)")
            hr_adjustment += adj

        if automation > 70:
            adj = -1.0
            factors.append(f"  • High automation (>70%): {adj:+.1f}pp (job security concern)")
            hr_adjustment += adj
        elif automation < 30:
            adj = 0.5
            factors.append(f"  • Low automation (<30%): {adj:+.1f}pp (stable job)")
            hr_adjustment += adj

        if engagement < 5:
            adj = -1.0
            factors.append(f"  • Low engagement (<5): {adj:+.1f}pp (satisfaction risk)")
            hr_adjustment += adj
        elif engagement > 7:
            adj = 0.5
            factors.append(f"  • High engagement (>7): {adj:+.1f}pp (good retention)")
            hr_adjustment += adj

        if wage_assessment == "UNDERPAID":
            adj = -0.5
            factors.append(f"  • Wage fairness (underpaid): {adj:+.1f}pp")
            hr_adjustment += adj

        if factors:
            output.append("Job Design Adjustments:")
            for factor in factors:
                output.append(factor)
        else:
            output.append("  (No major job design adjustments)")

        output.append("")

        # Final HR probability
        final_hr_prob = max(50, min(95, 84 + hr_adjustment))
        output.append(f"ADJUSTED HR DECISION PROBABILITY:")
        output.append(f"  Base: 84%")
        output.append(f"  Job Design Adjustment: {hr_adjustment:+.1f}pp")
        output.append(f"  Adjusted: {final_hr_prob:.0f}%")
        output.append("")

        # Employee stakeholder impact
        output.append("EMPLOYEE STAKEHOLDER IMPACT:")
        output.append("  Job design affects employee 'READY' (readiness) dimension:")
        if engagement > 7:
            output.append(f"  • High engagement ({engagement}/10) → Higher willingness θ_will")
            output.append(f"  • Employee more likely to support org decisions")
        else:
            output.append(f"  • Moderate engagement ({engagement}/10) → Baseline willingness")
        output.append("")

        # Integration summary
        output.append("INTEGRATION FLOW:")
        output.append(f"  Job Analysis → Job Metrics ({complexity:.1f}/5, {automation:.0f}%, {engagement:.1f}/10)")
        output.append(f"  ↓")
        output.append(f"  HR Decision Function (with job design) → {final_hr_prob:.0f}% approval probability")
        output.append(f"  ↓")
        output.append(f"  Employee Stakeholder Simulation → Engagement factors affect readiness")
        output.append(f"  ↓")
        output.append(f"  Retention Impact ({report['retention_impact']['adjusted_retention_pct']:.1f}%) → Phase 6.5 feedback")
        output.append("")

        output.append("KEY INSIGHT:")
        if abs(hr_adjustment) <= 1.0:
            output.append(f"  Job design has NEUTRAL impact on HR approval (±0.5pp range)")
        elif hr_adjustment > 0:
            output.append(f"  Job design has POSITIVE impact on HR approval (+{hr_adjustment:.1f}pp)")
            output.append(f"  → Recommend: Replicate this job design for similar roles")
        else:
            output.append(f"  Job design has NEGATIVE impact on HR approval ({hr_adjustment:.1f}pp)")
            output.append(f"  → Recommend: Upskill tasks, increase complexity, or improve engagement")

        return "\n".join(output)


# ============================================================================
# MAIN CLI LOGIC
# ============================================================================

def get_job(company: str, job_title: str) -> JobProfile:
    """Get job profile from library"""
    key = f"{company.upper()}_{job_title.replace(' ', '_').lower()}"

    if key in JOB_LIBRARY:
        return JOB_LIBRARY[key]

    raise ValueError(f"Unknown job: {key}. Available: {list(JOB_LIBRARY.keys())}")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Analyze job design complexity, automation risk, engagement",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze ALPLA machine operator
  %(prog)s ALPLA "Machine Operator"

  # Detailed analysis
  %(prog)s ALPLA "Machine Operator" --detail

  # Impact on Phase 6 HR decision
  %(prog)s ALPLA "Machine Operator" --impact-on-hr

  # Phase 6 integration (job design → stakeholder simulation)
  %(prog)s ALPLA "Machine Operator" --phase6-integration

  # Export to JSON
  %(prog)s ALPLA "Machine Operator" --json

  # List available jobs
  %(prog)s --list
        """
    )

    parser.add_argument("company", nargs="?", help="Company name (e.g., ALPLA)")
    parser.add_argument("job_title", nargs="?", help="Job title (e.g., 'Machine Operator')")
    parser.add_argument("--detail", action="store_true", help="Show detailed analysis")
    parser.add_argument("--impact-on-hr", action="store_true", help="Show HR decision impact")
    parser.add_argument("--phase6-integration", action="store_true", help="Show Phase 6 stakeholder integration")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--list", action="store_true", help="List available jobs")

    args = parser.parse_args()

    # List available jobs
    if args.list:
        print("\nAVAILABLE JOBS IN LIBRARY:")
        print("=" * 70)
        for key in JOB_LIBRARY.keys():
            job = JOB_LIBRARY[key]
            print(f"\n{job.company} - {job.job_title}")
            print(f"  Location: {job.location}")
            print(f"  Wage: €{job.current_wage}/hr")
        return

    # Check arguments
    if not args.company or not args.job_title:
        parser.print_help()
        return

    # Get job
    try:
        job = get_job(args.company, args.job_title)
    except ValueError as e:
        print(f"Error: {e}")
        print(f"\nRun with --list to see available jobs")
        sys.exit(1)

    # Analyze
    analyzer = JobAnalyzer(job)
    report = analyzer.generate_report()

    # Format output
    if args.json:
        print(json.dumps(report, indent=2, default=str))
    elif args.phase6_integration:
        print(JobReportFormatter.format_phase6_integration(report))
    elif args.impact_on_hr:
        print(JobReportFormatter.format_impact_on_hr(report))
    elif args.detail:
        print(JobReportFormatter.format_detailed(report))
    else:
        print(JobReportFormatter.format_summary(report))


if __name__ == "__main__":
    main()
