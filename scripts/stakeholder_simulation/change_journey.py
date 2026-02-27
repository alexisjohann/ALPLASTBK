"""
Change Journey Tracker - Phase 6 Week 3
Maps stakeholder progress through 8-stage behavioral change model
(Awareness → Consideration → Decision → Action → Loyalty)

Version: 1.0.0
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum
from datetime import datetime

# ============================================================================
# CHANGE JOURNEY MODEL
# ============================================================================

class JourneyStage(Enum):
    """8-stage behavioral change journey"""
    STAGE_1_AWARENESS = (1, "Awareness", "Do they know change is coming?", 0)
    STAGE_2_UNDERSTANDING = (2, "Understanding", "Do they grasp the what/why/how?", 1)
    STAGE_3_CONSIDERATION = (3, "Consideration", "Does this align with my interests?", 2)
    STAGE_4_ACCEPTANCE = (4, "Acceptance", "Can I mentally accept this?", 3)
    STAGE_5_DECISION = (5, "Decision", "Will I commit to support?", 4)
    STAGE_6_PREPARATION = (6, "Preparation", "Am I ready to act?", 5)
    STAGE_7_ACTION = (7, "Action", "Am I executing?", 6)
    STAGE_8_LOYALTY = (8, "Loyalty", "Am I sustained + advocating?", 7)

    def __init__(self, stage_num: int, name: str, question: str, index: int):
        self.stage_num = stage_num
        self.stage_name = name
        self.fundamental_question = question
        self.index = index

@dataclass
class JourneyProgress:
    """Track individual stakeholder progress through journey"""
    stakeholder_type: str
    stakeholder_name: str  # e.g., "Board of Directors", "Regional Leader - APAC"
    current_stage: int  # 1-8
    progress_percentage: float  # 0-100% within stage
    stage_entry_date: datetime
    expected_completion_date: Optional[datetime] = None
    blockers: List[str] = None
    accelerators: List[str] = None
    last_update: datetime = None

    def __post_init__(self):
        if self.blockers is None:
            self.blockers = []
        if self.accelerators is None:
            self.accelerators = []
        if self.last_update is None:
            self.last_update = datetime.now()

# ============================================================================
# STAGE DEFINITIONS WITH ACTIONS & BLOCKERS
# ============================================================================

JOURNEY_STAGE_DEFINITIONS = {
    1: {
        "name": "Awareness",
        "question": "Do they know change is coming?",
        "activity": "Initial communication about strategic initiative",
        "success_criteria": "AU ≥ 20% (basic awareness)",
        "timeline": "1-2 weeks before communication",
        "key_actions": [
            "Announce strategic initiative",
            "Share overview of what's changing",
            "Explain business rationale",
        ],
        "common_blockers": [
            "No communication yet",
            "Initiative not visible",
            "Competing news/priorities",
        ],
        "accelerators": [
            "CEO announcement",
            "Email from direct manager",
            "All-hands meeting",
        ],
    },
    2: {
        "name": "Understanding",
        "question": "Do they grasp the what/why/how?",
        "activity": "Education sessions, model walkthrough, FAQ",
        "success_criteria": "AU ≥ 50% (understands implications)",
        "timeline": "2-4 weeks (ongoing learning)",
        "key_actions": [
            "Detailed briefing sessions",
            "Q&A forums",
            "Share supporting materials",
            "Clarify impacts on their role",
        ],
        "common_blockers": [
            "Complexity/jargon",
            "Conflicting information",
            "Insufficient communication",
            "Fear/uncertainty",
        ],
        "accelerators": [
            "Clear, simple explanations",
            "Peer testimonials",
            "FAQ addressing concerns",
            "Manager 1-on-1s",
        ],
    },
    3: {
        "name": "Consideration",
        "question": "Does this align with my interests/utility?",
        "activity": "Evaluate options, compare current vs proposed",
        "success_criteria": "WHAT alignment ≥ 0.65 (strategic fit evident)",
        "timeline": "1-2 weeks (internal evaluation)",
        "key_actions": [
            "Highlight personal benefits",
            "Address concerns directly",
            "Provide comparison: current state vs future",
            "Share success stories",
        ],
        "common_blockers": [
            "Loss aversion (don't want to lose current situation)",
            "Status quo bias (prefer things as-is)",
            "Switching costs too high",
            "Unclear personal benefit",
        ],
        "accelerators": [
            "Clear value proposition",
            "Case studies/proof points",
            "Trial period/pilot",
            "Low-risk ways to experiment",
        ],
    },
    4: {
        "name": "Acceptance",
        "question": "Can I mentally accept this as inevitable/beneficial?",
        "activity": "Reduce psychological resistance",
        "success_criteria": "Psychological resistance < 30%",
        "timeline": "2-4 weeks (emotional adjustment)",
        "key_actions": [
            "Acknowledge concerns/fears",
            "Provide emotional support",
            "Share success stories",
            "Build community/support network",
        ],
        "common_blockers": [
            "Status quo bias (prefer familiar)",
            "Sunk cost fallacy (invested in old way)",
            "Identity threat (new role different)",
            "Grief/loss feelings",
        ],
        "accelerators": [
            "Leadership role modeling",
            "Peer acceptance",
            "Early wins/successes",
            "Community events",
        ],
    },
    5: {
        "name": "Decision",
        "question": "Will I commit to support/implementation?",
        "activity": "Formal voting/approval, budget commitment",
        "success_criteria": "READY (θ_cap × θ_will) ≥ 0.65 (commitment secured)",
        "timeline": "1-2 weeks (formal decision)",
        "key_actions": [
            "Request formal commitment",
            "Secure budget/resources",
            "Get approvals/sign-offs",
            "Build accountability",
        ],
        "common_blockers": [
            "Authority gaps (no decision power)",
            "Competing priorities",
            "Incentive misalignment",
            "Latent doubts",
        ],
        "accelerators": [
            "Clear decision process",
            "Leadership pressure (positive)",
            "Aligned incentives",
            "Public commitment",
        ],
    },
    6: {
        "name": "Preparation",
        "question": "Do I have resources/skills/authority to execute?",
        "activity": "Assemble team, secure budget, train staff",
        "success_criteria": "θ_capability ≥ 0.70 (ready to execute)",
        "timeline": "2-8 weeks (pre-launch preparation)",
        "key_actions": [
            "Assign teams/resources",
            "Provide training",
            "Build tools/systems",
            "Clarify roles/responsibilities",
        ],
        "common_blockers": [
            "Resource constraints",
            "Skill gaps",
            "System/tool delays",
            "Unclear responsibilities",
        ],
        "accelerators": [
            "Early resource allocation",
            "Proactive training",
            "Clear role definitions",
            "Executive sponsorship",
        ],
    },
    7: {
        "name": "Action",
        "question": "Am I actively executing the plan?",
        "activity": "Day 1 execution: new process, decisions, behaviors",
        "success_criteria": "Execution compliance ≥ 85%",
        "timeline": "First 30-90 days (critical execution)",
        "key_actions": [
            "Start using new process",
            "Make new decisions",
            "Adopt new behaviors",
            "Provide support/coaching",
        ],
        "common_blockers": [
            "Old habits (default to old way)",
            "System friction (new tools don't work)",
            "Unclear processes",
            "Lack of support",
        ],
        "accelerators": [
            "Quick wins",
            "Visible leadership adoption",
            "Support available 24/7",
            "Regular feedback",
        ],
    },
    8: {
        "name": "Loyalty",
        "question": "Am I sustained + advocating to others?",
        "activity": "Routine adoption, positive word-of-mouth",
        "success_criteria": "NPS ≥ 7/10, Continued use, Positive advocacy",
        "timeline": "6+ months (embedded in culture)",
        "key_actions": [
            "Reinforce new behaviors",
            "Celebrate success",
            "Solicit feedback",
            "Support peer adoption",
        ],
        "common_blockers": [
            "Backsliding to old habits",
            "New issues/bugs",
            "Fatigue/complacency",
            "Competing new initiatives",
        ],
        "accelerators": [
            "Regular success stories",
            "Peer recognition",
            "Continuous improvement",
            "Integration with incentives",
        ],
    },
}

# ============================================================================
# JOURNEY MANAGER
# ============================================================================

class ChangeJourneyManager:
    """Track and manage stakeholder progress through change journey"""

    @staticmethod
    def get_stage_info(stage_num: int) -> Dict:
        """Get detailed information about a journey stage"""
        if stage_num not in JOURNEY_STAGE_DEFINITIONS:
            raise ValueError(f"Invalid stage: {stage_num}")
        return JOURNEY_STAGE_DEFINITIONS[stage_num]

    @staticmethod
    def advance_stage(current_stage: int, progress: float = 100.0) -> int:
        """
        Advance stakeholder to next stage when progress hits threshold

        Args:
            current_stage: Current stage (1-8)
            progress: Progress percentage in current stage (0-100)

        Returns:
            New stage number (max 8)
        """
        if progress >= 100 and current_stage < 8:
            return current_stage + 1
        return current_stage

    @staticmethod
    def calculate_progress_percentage(stage_num: int, time_in_stage_days: float, stage_duration_days: float) -> float:
        """
        Calculate progress percentage within a stage

        Args:
            stage_num: Current stage (1-8)
            time_in_stage_days: Days spent in current stage
            stage_duration_days: Expected duration of stage

        Returns:
            Progress percentage (0-100)
        """
        if stage_duration_days <= 0:
            return 0.0

        progress = min(100.0, (time_in_stage_days / stage_duration_days) * 100)
        return progress

    @staticmethod
    def estimate_completion_date(current_stage: int, stage_entry_date: datetime) -> Optional[datetime]:
        """
        Estimate when stakeholder will reach Stage 8 (Loyalty)

        Args:
            current_stage: Current stage (1-8)
            stage_entry_date: Date when entered current stage

        Returns:
            Estimated completion date
        """
        from datetime import timedelta

        # Typical duration per stage (days)
        stage_durations = {
            1: 14,   # Awareness: 2 weeks
            2: 21,   # Understanding: 3 weeks
            3: 14,   # Consideration: 2 weeks
            4: 21,   # Acceptance: 3 weeks
            5: 14,   # Decision: 2 weeks
            6: 42,   # Preparation: 6 weeks
            7: 60,   # Action: 8-12 weeks
            8: 180,  # Loyalty: 6+ months
        }

        # Sum remaining stages
        remaining_days = sum(stage_durations[s] for s in range(current_stage, 9))
        estimated_completion = stage_entry_date + timedelta(days=remaining_days)

        return estimated_completion

    @staticmethod
    def get_stage_blockers(stage_num: int) -> List[str]:
        """Get common blockers for a stage"""
        stage_info = ChangeJourneyManager.get_stage_info(stage_num)
        return stage_info.get("common_blockers", [])

    @staticmethod
    def get_stage_accelerators(stage_num: int) -> List[str]:
        """Get actions that accelerate progress through a stage"""
        stage_info = ChangeJourneyManager.get_stage_info(stage_num)
        return stage_info.get("accelerators", [])

    @staticmethod
    def recommend_actions(stage_num: int, blockers: List[str] = None) -> List[str]:
        """
        Recommend specific actions to accelerate progress

        Args:
            stage_num: Current stage (1-8)
            blockers: List of identified blockers

        Returns:
            Prioritized action recommendations
        """
        stage_info = ChangeJourneyManager.get_stage_info(stage_num)
        actions = stage_info.get("key_actions", [])
        accelerators = stage_info.get("accelerators", [])

        # Prioritize actions that address blockers
        if blockers:
            accelerators_for_blockers = []
            for blocker in blockers:
                if "communication" in blocker.lower():
                    accelerators_for_blockers.append("Increase communication frequency")
                elif "fear" in blocker.lower() or "uncertainty" in blocker.lower():
                    accelerators_for_blockers.append("Address concerns directly with leadership support")
                elif "resource" in blocker.lower():
                    accelerators_for_blockers.append("Secure additional budget/resources")
                elif "skill" in blocker.lower():
                    accelerators_for_blockers.append("Provide targeted training")

            return accelerators_for_blockers + actions

        return actions + accelerators

    @staticmethod
    def calculate_overall_progress(journey_progresses: Dict[str, JourneyProgress]) -> Dict:
        """
        Calculate overall organization change progress

        Args:
            journey_progresses: Dict of stakeholder_type -> JourneyProgress

        Returns:
            Overall progress metrics
        """
        if not journey_progresses:
            return {
                "total_stakeholders": 0,
                "average_stage": 0,
                "percentage_at_stage_5_plus": 0,
                "percentage_at_stage_8": 0,
            }

        stages = [p.current_stage for p in journey_progresses.values()]
        stage_5_plus = sum(1 for s in stages if s >= 5)
        stage_8 = sum(1 for s in stages if s == 8)
        total = len(stages)

        return {
            "total_stakeholders": total,
            "average_stage": sum(stages) / total if total > 0 else 0,
            "percentage_at_stage_5_plus": (stage_5_plus / total * 100) if total > 0 else 0,
            "percentage_at_stage_8": (stage_8 / total * 100) if total > 0 else 0,
            "stage_distribution": {
                i: sum(1 for s in stages if s == i)
                for i in range(1, 9)
            },
        }

# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    from datetime import datetime, timedelta

    print("CHANGE JOURNEY MAPPING")
    print("=" * 70)

    # Example: Board progress
    print("\nExample: Board of Directors Journey")
    print("-" * 70)

    stage_info = ChangeJourneyManager.get_stage_info(5)
    print(f"Current Stage: {stage_info['name']}")
    print(f"Question: {stage_info['question']}")
    print(f"Activity: {stage_info['activity']}")
    print(f"Key Actions:")
    for action in stage_info["key_actions"]:
        print(f"  • {action}")

    # Calculate progress
    entry_date = datetime.now() - timedelta(days=7)
    stage_duration = 14
    progress = ChangeJourneyManager.calculate_progress_percentage(5, 7, stage_duration)
    estimated_completion = ChangeJourneyManager.estimate_completion_date(5, entry_date)

    print(f"\nProgress: {progress:.0f}%")
    print(f"Estimated Completion: {estimated_completion.strftime('%Y-%m-%d')}")

    # Recommendations
    blockers = ["Competing priorities", "Budget approval delays"]
    recommendations = ChangeJourneyManager.recommend_actions(5, blockers)
    print(f"\nRecommended Actions:")
    for i, action in enumerate(recommendations, 1):
        print(f"  {i}. {action}")

    # Overall progress
    print("\n" + "=" * 70)
    print("Overall Organization Progress (12 Stakeholders)")
    progresses = {
        "board": JourneyProgress("board", "Board", stage=5, progress_percentage=70, stage_entry_date=entry_date),
        "regional_pl": JourneyProgress("regional_pl", "Regional P&L", stage=6, progress_percentage=50, stage_entry_date=entry_date - timedelta(days=14)),
        "customer": JourneyProgress("customer", "Customer", stage=3, progress_percentage=40, stage_entry_date=entry_date - timedelta(days=30)),
    }

    overall = ChangeJourneyManager.calculate_overall_progress({p.stakeholder_type: p for p in progresses.values()})
    print(f"Average Stage: {overall['average_stage']:.1f}/8")
    print(f"At Stage 5+ (Decision+): {overall['percentage_at_stage_5_plus']:.0f}%")
    print(f"At Stage 8 (Loyalty): {overall['percentage_at_stage_8']:.0f}%")
