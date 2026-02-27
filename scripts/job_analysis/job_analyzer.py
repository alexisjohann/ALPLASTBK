"""
Job Analysis Engine - Phase 6.5
Evaluates job design complexity, automation risk, engagement impact
Based on David Autor's task typology framework

Version: 1.0.0
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
import statistics

# ============================================================================
# ENUMS & CONSTANTS
# ============================================================================

class TaskType(Enum):
    """Autor task typology"""
    ROUTINE_COGNITIVE = "Routine Cognitive"
    ROUTINE_MANUAL = "Routine Manual"
    NON_ROUTINE_COGNITIVE = "Non-Routine Cognitive"
    NON_ROUTINE_MANUAL = "Non-Routine Manual"

class ComplexityLevel(Enum):
    """Complexity classification"""
    TRIVIAL = (1, "Trivial")
    SIMPLE = (2, "Simple")
    ROUTINE_COGNITIVE = (3, "Routine Cognitive")
    COMPLEX_COGNITIVE = (4, "Complex Cognitive")
    HIGHLY_COMPLEX = (5, "Highly Complex")

    def __init__(self, score: int, label: str):
        self.score = score
        self.label = label

# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class Task:
    """Individual task within a job"""
    task_id: str  # Unique identifier
    name: str  # Task name
    time_allocation_pct: float  # % of work week spent on this task
    cognitive_load: int  # 0-5 scale
    motor_skill: int  # 0-5 scale
    decision_making: int  # 0-5 scale (0=none, 5=critical)
    automation_risk: float  # 0-100% probability can be automated
    training_time_days: int  # Days to train someone on this task
    skill_level_required: int  # 1-5 (1=entry-level, 5=expert)
    frequency_per_shift: Optional[str] = None  # "hourly", "2-3x", "daily", etc.

    def calculate_complexity(self) -> float:
        """
        Calculate task complexity score (0-5)
        Average of cognitive load, decision-making, skill required
        """
        return (self.cognitive_load + self.decision_making + self.skill_level_required) / 3.0

    def calculate_task_type(self) -> TaskType:
        """Classify task using Autor framework"""
        is_routine = self.decision_making <= 2
        is_cognitive = self.cognitive_load >= 3

        if is_routine and is_cognitive:
            return TaskType.ROUTINE_COGNITIVE
        elif is_routine and not is_cognitive:
            return TaskType.ROUTINE_MANUAL
        elif not is_routine and is_cognitive:
            return TaskType.NON_ROUTINE_COGNITIVE
        else:
            return TaskType.NON_ROUTINE_MANUAL

@dataclass
class JobProfile:
    """Complete job profile"""
    company: str
    job_title: str
    location: str
    current_wage: float  # EUR/hour
    tasks: List[Task] = field(default_factory=list)

    # Optional context
    employment_type: str = "Full-time"
    hours_per_week: int = 40
    experience_required_years: int = 0

# ============================================================================
# JOB ANALYZER ENGINE
# ============================================================================

class JobAnalyzer:
    """Analyze job design complexity, automation risk, engagement impact"""

    def __init__(self, job: JobProfile):
        self.job = job
        self.validate_job()

    def validate_job(self):
        """Validate job profile data"""
        if not self.job.tasks:
            raise ValueError(f"Job '{self.job.job_title}' has no tasks")

        # Check time allocation sums to ~100%
        total_time = sum(t.time_allocation_pct for t in self.job.tasks)
        if abs(total_time - 100) > 5:
            print(f"Warning: Task time allocation sums to {total_time}% (should be ~100%)")

        # Check all values are in valid ranges
        for task in self.job.tasks:
            assert 0 <= task.time_allocation_pct <= 100, f"Task {task.task_id}: Invalid time allocation"
            assert 0 <= task.cognitive_load <= 5, f"Task {task.task_id}: Invalid cognitive load"
            assert 0 <= task.automation_risk <= 100, f"Task {task.task_id}: Invalid automation risk"

    def calculate_job_complexity_score(self) -> float:
        """
        Calculate overall job complexity (0-5)
        Weighted average of task complexities
        """
        weighted_sum = 0
        for task in self.job.tasks:
            task_complexity = task.calculate_complexity()
            weighted_sum += task_complexity * (task.time_allocation_pct / 100)

        return round(weighted_sum, 2)

    def calculate_automation_risk(self) -> float:
        """
        Calculate % of job automatable in 5 years
        Weighted by time allocation
        """
        weighted_risk = 0
        for task in self.job.tasks:
            weighted_risk += task.automation_risk * (task.time_allocation_pct / 100)

        return round(weighted_risk, 1)

    def calculate_task_composition(self) -> Dict[TaskType, float]:
        """
        Calculate % of time spent on each Autor task type
        """
        composition = {task_type: 0 for task_type in TaskType}

        for task in self.job.tasks:
            task_type = task.calculate_task_type()
            composition[task_type] += task.time_allocation_pct

        return composition

    def calculate_engagement_score(self) -> Tuple[float, Dict[str, float]]:
        """
        Calculate engagement score (0-10) based on job design
        Model: Engagement = f(complexity, variety, autonomy, skill_utilization)
        """
        # Factor 1: Complexity (0-10)
        complexity_score = self.calculate_job_complexity_score()
        complexity_engagement = min(10, complexity_score * 2)  # 2.9 → 5.8

        # Factor 2: Variety (count of distinct tasks, 0-10)
        task_variety = min(10, len(self.job.tasks) * 1.5)  # 6 tasks → 9

        # Factor 3: Autonomy (assumed based on decision-making)
        avg_decision_making = statistics.mean(t.decision_making for t in self.job.tasks)
        autonomy_score = min(10, avg_decision_making * 2)  # 0-5 → 0-10

        # Factor 4: Skill Utilization
        avg_skill_required = statistics.mean(t.skill_level_required for t in self.job.tasks)
        skill_utilization = min(10, avg_skill_required * 2)  # 0-5 → 0-10

        # Average all factors
        overall_engagement = (complexity_engagement + task_variety + autonomy_score + skill_utilization) / 4

        return round(overall_engagement, 1), {
            "complexity": round(complexity_engagement, 1),
            "variety": round(task_variety, 1),
            "autonomy": round(autonomy_score, 1),
            "skill_utilization": round(skill_utilization, 1),
        }

    def calculate_fair_wage_range(self) -> Tuple[float, float]:
        """
        Calculate fair wage range based on task complexity & skill required
        Uses market data: base €10/hr + premiums
        """
        base_wage = 10.0

        # Complexity premium
        complexity = self.calculate_job_complexity_score()
        complexity_premium = (complexity / 5.0) * 5.0  # 0-5 → 0-5 EUR

        # Skill premium
        avg_skill = statistics.mean(t.skill_level_required for t in self.job.tasks)
        skill_premium = (avg_skill / 5.0) * 3.0  # 0-5 → 0-3 EUR

        # Training investment premium
        avg_training = statistics.mean(t.training_time_days for t in self.job.tasks)
        training_premium = min(1.5, avg_training / 30)  # 30 days → 1 EUR

        midpoint = base_wage + complexity_premium + skill_premium + training_premium
        range_margin = 1.0  # ±1 EUR range

        return (
            round(midpoint - range_margin, 2),
            round(midpoint + range_margin, 2),
        )

    def assess_wage_fairness(self) -> str:
        """Compare current wage to fair wage range"""
        low, high = self.calculate_fair_wage_range()

        if self.job.current_wage < low - 0.5:
            return "UNDERPAID"
        elif self.job.current_wage > high + 0.5:
            return "OVERPAID"
        else:
            return "FAIR"

    def estimate_retention_impact(self, base_retention_pct: float = 58.0) -> float:
        """
        Estimate how job design affects employee retention
        Base: 58% (Phase 6 model)
        Adjustments: +/- based on engagement, complexity, automation risk
        """
        engagement, _ = self.calculate_engagement_score()
        automation_risk = self.calculate_automation_risk()

        # Engagement impact: +0.3% per point (0-10 scale)
        engagement_impact = (engagement - 5.0) * 0.3

        # Automation risk impact: -0.1% per point (0-100 scale)
        automation_impact = -(automation_risk - 50) / 500

        # Complexity impact: jobs with 3.5+ complexity have +2% retention
        complexity = self.calculate_job_complexity_score()
        complexity_impact = 2.0 if complexity >= 3.5 else -1.0

        adjusted_retention = base_retention_pct + engagement_impact + automation_impact + complexity_impact
        return round(max(20, min(95, adjusted_retention)), 1)

    def generate_report(self) -> Dict:
        """Generate complete job analysis report"""
        complexity = self.calculate_job_complexity_score()
        automation = self.calculate_automation_risk()
        composition = self.calculate_task_composition()
        engagement, engagement_breakdown = self.calculate_engagement_score()
        fair_wage_low, fair_wage_high = self.calculate_fair_wage_range()
        wage_fairness = self.assess_wage_fairness()
        retention = self.estimate_retention_impact()

        return {
            "job_profile": {
                "company": self.job.company,
                "job_title": self.job.job_title,
                "location": self.job.location,
                "current_wage": self.job.current_wage,
            },
            "task_inventory": {
                "total_tasks": len(self.job.tasks),
                "task_names": [t.name for t in self.job.tasks],
            },
            "complexity_analysis": {
                "overall_complexity_score": complexity,
                "interpretation": self._interpret_complexity(complexity),
                "average_cognitive_load": round(statistics.mean(t.cognitive_load for t in self.job.tasks), 1),
                "average_skill_required": round(statistics.mean(t.skill_level_required for t in self.job.tasks), 1),
            },
            "task_composition": {
                str(k.value): round(v, 1) for k, v in composition.items()
            },
            "automation_risk": {
                "overall_automation_risk_pct": automation,
                "automatable_tasks_5yr": self._identify_high_risk_tasks(),
                "interpretation": self._interpret_automation_risk(automation),
            },
            "engagement_analysis": {
                "overall_engagement_score": engagement,
                "breakdown": engagement_breakdown,
                "interpretation": self._interpret_engagement(engagement),
            },
            "wage_analysis": {
                "current_wage": self.job.current_wage,
                "fair_wage_range": [fair_wage_low, fair_wage_high],
                "fairness_assessment": wage_fairness,
                "wage_premium_vs_base": round(self.job.current_wage - 10, 2),
            },
            "retention_impact": {
                "base_retention_pct": 58.0,
                "adjusted_retention_pct": retention,
                "retention_change_pct": round(retention - 58.0, 1),
            },
            "summary": {
                "job_quality": self._rate_job_quality(complexity, automation, engagement),
                "primary_risks": self._identify_primary_risks(complexity, automation, engagement),
                "improvement_opportunities": self._identify_improvements(),
            }
        }

    # Helper methods for interpretation

    def _interpret_complexity(self, score: float) -> str:
        """Interpret complexity score"""
        if score < 1.5:
            return "TRIVIAL - Minimal skill required"
        elif score < 2.5:
            return "SIMPLE - Basic operational skills"
        elif score < 3.5:
            return "ROUTINE-COGNITIVE - Some problem-solving"
        elif score < 4.5:
            return "COMPLEX-COGNITIVE - Significant technical knowledge"
        else:
            return "HIGHLY COMPLEX - Expert-level skills required"

    def _interpret_automation_risk(self, risk: float) -> str:
        """Interpret automation risk"""
        if risk < 30:
            return "LOW RISK - Core tasks hard to automate"
        elif risk < 50:
            return "MODERATE RISK - Mix of routine and complex tasks"
        elif risk < 70:
            return "HIGH RISK - Majority of tasks automatable"
        else:
            return "VERY HIGH RISK - Job highly exposed to automation"

    def _interpret_engagement(self, score: float) -> str:
        """Interpret engagement score"""
        if score < 3:
            return "LOW - Monotonous, repetitive work"
        elif score < 5:
            return "MODERATE - Some variety and skill use"
        elif score < 7:
            return "GOOD - Engaging mix of tasks"
        else:
            return "EXCELLENT - Highly engaging work"

    def _rate_job_quality(self, complexity: float, automation: float, engagement: float) -> str:
        """Overall job quality rating"""
        score = 0
        if complexity >= 3: score += 1
        if automation <= 50: score += 1
        if engagement >= 5: score += 1

        if score == 3:
            return "EXCELLENT"
        elif score == 2:
            return "GOOD"
        elif score == 1:
            return "FAIR"
        else:
            return "POOR"

    def _identify_high_risk_tasks(self) -> List[Dict]:
        """Identify tasks with >60% automation risk"""
        high_risk = [
            {
                "task_name": t.name,
                "automation_risk": t.automation_risk,
                "time_allocation_pct": t.time_allocation_pct,
            }
            for t in self.job.tasks
            if t.automation_risk > 60
        ]
        return sorted(high_risk, key=lambda x: x["automation_risk"], reverse=True)

    def _identify_primary_risks(self, complexity: float, automation: float, engagement: float) -> List[str]:
        """Identify main job design risks"""
        risks = []

        if complexity < 2.5:
            risks.append("Low complexity → boring work, high turnover risk")

        if automation > 60:
            risks.append(f"High automation risk ({automation}%) → job security concerns")

        if engagement < 4:
            risks.append("Low engagement → retention risk, quality issues")

        if automation > 60 and complexity < 3:
            risks.append("CRITICAL: Low-skilled, highly automatable job → strategic risk")

        return risks if risks else ["No major risks identified"]

    def _identify_improvements(self) -> List[Dict]:
        """Suggest job design improvements"""
        improvements = []

        # High automation risk tasks
        high_risk_tasks = self._identify_high_risk_tasks()
        if high_risk_tasks:
            improvements.append({
                "action": "Upskill in complex tasks",
                "target_tasks": [t["task_name"] for t in high_risk_tasks[:2]],
                "benefit": "Reduce automatable portion",
                "timeline": "3-6 months",
            })

        # Low engagement
        engagement, breakdown = self.calculate_engagement_score()
        if engagement < 5:
            if breakdown["variety"] < 5:
                improvements.append({
                    "action": "Add task variety",
                    "benefit": "Increase engagement",
                    "timeline": "Immediate",
                })

            if breakdown["autonomy"] < 5:
                improvements.append({
                    "action": "Increase decision-making authority",
                    "benefit": "Boost engagement and retention",
                    "timeline": "1-2 months",
                })

        # Career progression
        complexity = self.calculate_job_complexity_score()
        if complexity >= 3:
            improvements.append({
                "action": "Create career path",
                "target": "Operator → Senior Operator → Technician",
                "wage_progression": "€13 → €15 → €18/hr",
                "benefit": "Improve retention",
                "timeline": "6-12 months",
            })

        return improvements

# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Example: ALPLA Machine Operator
    print("=" * 70)
    print("JOB ANALYSIS ENGINE - EXAMPLE: ALPLA Machine Operator")
    print("=" * 70)

    alpla_operator = JobProfile(
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
            ),
        ],
    )

    analyzer = JobAnalyzer(alpla_operator)
    report = analyzer.generate_report()

    # Pretty print results
    import json
    print("\nJOB ANALYSIS REPORT:\n")
    print(json.dumps(report, indent=2))

    print("\n" + "=" * 70)
    print("KEY FINDINGS:")
    print(f"Complexity Score: {report['complexity_analysis']['overall_complexity_score']}/5 - {report['complexity_analysis']['interpretation']}")
    print(f"Automation Risk: {report['automation_risk']['overall_automation_risk_pct']}% - {report['automation_risk']['interpretation']}")
    print(f"Engagement Score: {report['engagement_analysis']['overall_engagement_score']}/10 - {report['engagement_analysis']['interpretation']}")
    print(f"Wage Fairness: {report['wage_analysis']['fairness_assessment']} (€{report['wage_analysis']['current_wage']}/hr vs fair range €{report['wage_analysis']['fair_wage_range'][0]}-€{report['wage_analysis']['fair_wage_range'][1]}/hr)")
    print(f"Retention Impact: {report['retention_impact']['adjusted_retention_pct']}% (vs baseline 58%) - {report['retention_impact']['retention_change_ppt']:.1f}pp change")
    print(f"Job Quality: {report['summary']['job_quality']}")
    print("=" * 70)
