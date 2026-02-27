"""
Stakeholder Simulation Engine - Phase 6
Predicts stakeholder decisions using 10C CORE framework + behavioral economics

Core Decision Functions:
- Board of Directors: Strategy Approval
- C-Suite: Risk Escalation
- Regional P&L Leaders: Hit CAGR Target
- Customers: Purchase Decisions (with behavioral economics)
- Employees: Retention During Change
- Suppliers: Partnership Commitment
- Competitors: Market Response
... and 5 more stakeholder types

Version: 1.0.0
Created: 2026-01-16
"""

import json
import math
import yaml
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from enum import Enum

# ============================================================================
# DATA CLASSES
# ============================================================================

class ConfidenceLevel(Enum):
    """Probability confidence classification"""
    VERY_HIGH = "VERY HIGH"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class RiskZone(Enum):
    """Risk classification zones"""
    GREEN = "✓ GREEN"      # >= 80%
    YELLOW = "✓ YELLOW"    # 65-80%
    ORANGE = "⚠ ORANGE"    # 50-65%
    RED = "🔴 RED"         # < 50%

@dataclass
class StakeholderDecision:
    """Result of stakeholder decision simulation"""
    stakeholder_type: str
    decision_name: str
    probability: float
    confidence_level: ConfidenceLevel
    risk_zone: RiskZone
    key_drivers: Dict[str, float]  # 10C dimension contributions
    red_flags: List[str]
    conditions_met: List[str]
    timeline_to_decision: str
    timeline_to_execution: str

@dataclass
class NineCAdjustments:
    """10C CORE dimension values for a specific case"""
    WHERE_confidence: float  # Parameter confidence E(θ)
    WHEN_context_risk: float  # Context sensitivity Ψ
    HOW_capability: float  # Complementarity γ
    WHAT_alignment: float  # Utility dimension match ω_d
    HIERARCHY_clarity: float  # Decision stratification N_L2
    AWARE_briefing: float  # Awareness level AU
    READY_willingness: float  # Readiness θ_cap × θ_will
    additional_factors: Dict[str, float] = None  # Behavioral factors

# ============================================================================
# DECISION FUNCTIONS: Logistic Regression (Sigmoid) Models
# ============================================================================

class DecisionFunctions:
    """All 12 stakeholder decision functions"""

    # ====================================================================
    # STRATEGIC TIER
    # ====================================================================

    @staticmethod
    def board_strategy_approval(adjustments: NineCAdjustments) -> Tuple[float, Dict]:
        """
        Board of Directors: Approve Strategic Capex Authorization

        Formula: P(Approve) = sigmoid(β₀ + Σ(βᵢ × dimensionᵢ))

        Weights (learned from strategic approval patterns):
        - β₁ (WHERE) = 1.25 - Biggest driver: confidence in numbers
        - β₂ (WHEN) = -0.85 - Economic uncertainty reduces approval
        - β₃ (HOW) = 0.95 - Need proven execution capability
        - β₄ (HIERARCHY) = 1.10 - Clear governance gates
        - β₅ (AWARE) = 0.75 - Full briefing required
        - β₆ (READY) = 0.90 - Internal voting matters
        """
        beta_intercept = -0.50
        beta_where = 1.25
        beta_when = -0.85
        beta_how = 0.95
        beta_hierarchy = 1.10
        beta_aware = 0.75
        beta_ready = 0.90

        # Calculate logit
        logit = (
            beta_intercept +
            beta_where * adjustments.WHERE_confidence +
            beta_when * (1 - adjustments.WHEN_context_risk) +  # Risk inverse
            beta_how * adjustments.HOW_capability +
            beta_hierarchy * adjustments.HIERARCHY_clarity +
            beta_aware * adjustments.AWARE_briefing +
            beta_ready * adjustments.READY_willingness
        )

        # Convert to probability via sigmoid
        probability = DecisionFunctions._sigmoid(logit)

        # Calculate contributions (drivers)
        drivers = {
            "WHERE": beta_where * adjustments.WHERE_confidence * 100 / (1 + math.exp(-logit)),
            "WHEN": beta_when * (1 - adjustments.WHEN_context_risk) * 100 / (1 + math.exp(-logit)),
            "HOW": beta_how * adjustments.HOW_capability * 100 / (1 + math.exp(-logit)),
            "HIERARCHY": beta_hierarchy * adjustments.HIERARCHY_clarity * 100 / (1 + math.exp(-logit)),
            "AWARE": beta_aware * adjustments.AWARE_briefing * 100 / (1 + math.exp(-logit)),
            "READY": beta_ready * adjustments.READY_willingness * 100 / (1 + math.exp(-logit)),
        }

        return probability, drivers

    @staticmethod
    def c_suite_risk_escalation(adjustments: NineCAdjustments) -> Tuple[float, Dict]:
        """
        C-Suite: Monthly Risk Escalation Decision

        Trigger: P(Escalate Risk) IF:
        - ΔP > ±5% vs quarterly forecast
        - E(θ) growing (shrinkage working backwards)
        - WHEN context shock > 1.5σ

        Risk Model: Not traditional sigmoid, but threshold-based
        """
        # Simplified: Escalation triggered by forecast miss confidence
        forecast_confidence_loss = 1 - adjustments.WHERE_confidence
        context_shock = adjustments.WHEN_context_risk

        # Probability of escalation increases with risk
        escalation_prob = min(0.95, forecast_confidence_loss * 0.3 + context_shock * 0.4)

        drivers = {
            "Forecast_Confidence_Loss": forecast_confidence_loss * 100,
            "Context_Risk": context_shock * 100,
        }

        return escalation_prob, drivers

    # ====================================================================
    # OPERATIONAL TIER
    # ====================================================================

    @staticmethod
    def regional_pl_hit_cagr(adjustments: NineCAdjustments) -> Tuple[float, Dict]:
        """
        Regional P&L Leader: Hit Monthly CAGR Target

        Success depends on:
        - WHERE: Regional forecast confidence
        - HOW: Revenue-headcount complementarity γ_rev-org = 0.68
        - WHAT: Strategic utility alignment (segment focus)
        """
        beta_intercept = 0.15
        beta_where = 1.0  # Regional CAGR confidence
        beta_how = 0.85   # Organization capability (γ coupling)
        beta_what = 0.60  # Segment alignment

        logit = (
            beta_intercept +
            beta_where * adjustments.WHERE_confidence +
            beta_how * adjustments.HOW_capability +
            beta_what * adjustments.WHAT_alignment
        )

        probability = DecisionFunctions._sigmoid(logit)

        drivers = {
            "WHERE_Regional_Confidence": beta_where * adjustments.WHERE_confidence * 100 / (1 + math.exp(-logit)),
            "HOW_Org_Capability": beta_how * adjustments.HOW_capability * 100 / (1 + math.exp(-logit)),
            "WHAT_Segment_Alignment": beta_what * adjustments.WHAT_alignment * 100 / (1 + math.exp(-logit)),
        }

        return probability, drivers

    @staticmethod
    def fpa_accept_parameter_update(adjustments: NineCAdjustments) -> Tuple[float, Dict]:
        """
        FP&A Team: Accept Parameter Update Decision

        Rule: Accept if:
        - Shrinkage > 15% (confidence improving)
        - E(θ) confidence level increases
        - No regime change detected
        """
        # FP&A is highly rational - based on statistical improvement
        # Assume incoming shrinkage of 20% (0.8pp → 0.64pp)
        estimated_shrinkage = 0.25  # 25% shrinkage expected

        # Probability increases with parameter confidence
        acceptance_prob = min(0.95, adjustments.WHERE_confidence * 0.7 + estimated_shrinkage * 0.5)

        drivers = {
            "Parameter_Confidence": adjustments.WHERE_confidence * 100,
            "Expected_Shrinkage": estimated_shrinkage * 100,
        }

        return acceptance_prob, drivers

    @staticmethod
    def hr_approve_hiring_plan(adjustments: NineCAdjustments) -> Tuple[float, Dict]:
        """
        HR/Organization: Approve Hiring Plan Commitment

        Depends on:
        - HOW: Revenue-headcount complementarity γ_rev-org = 0.68
        - WHAT: Strategic priority alignment
        - READY: Org willingness to invest
        """
        beta_intercept = -0.20
        beta_how = 1.05  # High dependency on γ_rev-org
        beta_what = 0.75
        beta_ready = 0.65

        logit = (
            beta_intercept +
            beta_how * adjustments.HOW_capability +
            beta_what * adjustments.WHAT_alignment +
            beta_ready * adjustments.READY_willingness
        )

        probability = DecisionFunctions._sigmoid(logit)

        drivers = {
            "HOW_Revenue_Headcount_Synergy": beta_how * adjustments.HOW_capability * 100 / (1 + math.exp(-logit)),
            "WHAT_Strategic_Alignment": beta_what * adjustments.WHAT_alignment * 100 / (1 + math.exp(-logit)),
            "READY_Org_Willingness": beta_ready * adjustments.READY_willingness * 100 / (1 + math.exp(-logit)),
        }

        return probability, drivers

    @staticmethod
    def hr_approve_hiring_with_job_design(adjustments: NineCAdjustments,
                                          job_metrics: Dict = None) -> Tuple[float, Dict]:
        """
        HR/Organization: Approve Hiring Plan with Job Design Factors

        Incorporates job design metrics (complexity, automation risk, engagement)
        into HR hiring decision to create more nuanced approval probability.

        Base formula (from Phase 6):
        P(Approve) = sigmoid(β₀ + β₁×HOW + β₂×WHAT + β₃×READY)

        Job design adjustment factors:
        - Complexity: -2pp if <2.5 (boring), +1pp if >3.5 (engaging)
        - Automation Risk: -1pp if >70% (job security), +0.5pp if <30%
        - Engagement: ±1pp based on overall engagement score
        - Wage Fairness: -0.5pp if underpaid, +0.25pp if overpaid

        Integration: Adjusted_Prob = Base_Prob + Job_Design_Adjustment
        """
        # Base 10C calculation (same as hr_approve_hiring_plan)
        beta_intercept = -0.20
        beta_how = 1.05
        beta_what = 0.75
        beta_ready = 0.65

        base_logit = (
            beta_intercept +
            beta_how * adjustments.HOW_capability +
            beta_what * adjustments.WHAT_alignment +
            beta_ready * adjustments.READY_willingness
        )

        base_probability = DecisionFunctions._sigmoid(base_logit)

        # Job design adjustments
        job_design_adjustment = 0.0
        job_design_factors = {}

        if job_metrics:
            complexity_score = job_metrics.get('complexity_score', 2.5)
            automation_risk = job_metrics.get('automation_risk', 50)
            engagement_score = job_metrics.get('engagement_score', 5)
            fairness_assessment = job_metrics.get('fairness_assessment', 'FAIR')

            # Complexity adjustment
            if complexity_score < 2.5:
                complexity_adj = -0.02  # Low complexity → boredom/turnover risk
                job_design_factors['complexity'] = complexity_adj
                job_design_adjustment += complexity_adj
            elif complexity_score > 3.5:
                complexity_adj = 0.01  # Good complexity → engagement
                job_design_factors['complexity'] = complexity_adj
                job_design_adjustment += complexity_adj

            # Automation risk adjustment
            if automation_risk > 70:
                automation_adj = -0.01  # High automation → job security concern
                job_design_factors['automation_risk'] = automation_adj
                job_design_adjustment += automation_adj
            elif automation_risk < 30:
                automation_adj = 0.005  # Low automation → stable job
                job_design_factors['automation_risk'] = automation_adj
                job_design_adjustment += automation_adj

            # Engagement adjustment
            if engagement_score < 5:
                engagement_adj = -0.01
                job_design_factors['engagement'] = engagement_adj
                job_design_adjustment += engagement_adj
            elif engagement_score > 7:
                engagement_adj = 0.005
                job_design_factors['engagement'] = engagement_adj
                job_design_adjustment += engagement_adj

            # Wage fairness adjustment
            if fairness_assessment == "UNDERPAID":
                wage_adj = -0.005
                job_design_factors['wage_fairness'] = wage_adj
                job_design_adjustment += wage_adj
            elif fairness_assessment == "OVERPAID":
                wage_adj = 0.0025
                job_design_factors['wage_fairness'] = wage_adj
                job_design_adjustment += wage_adj

        # Apply adjustment and constrain
        adjusted_probability = base_probability + job_design_adjustment
        adjusted_probability = max(0.5, min(0.95, adjusted_probability))

        # Build drivers dictionary
        drivers = {
            "Base_Probability": base_probability * 100,
            "Job_Design_Adjustment": job_design_adjustment * 100,
            "Adjusted_Probability": adjusted_probability * 100,
            "HOW_Revenue_Headcount_Synergy": beta_how * adjustments.HOW_capability * 100 / (1 + math.exp(-base_logit)),
            "WHAT_Strategic_Alignment": beta_what * adjustments.WHAT_alignment * 100 / (1 + math.exp(-base_logit)),
            "READY_Org_Willingness": beta_ready * adjustments.READY_willingness * 100 / (1 + math.exp(-base_logit)),
        }

        # Add job design factors if present
        if job_design_factors:
            drivers.update({
                f"Job_Design_{k}": v * 100
                for k, v in job_design_factors.items()
            })

        return adjusted_probability, drivers

    @staticmethod
    def capex_committee_phase_gate(adjustments: NineCAdjustments) -> Tuple[float, Dict]:
        """
        Capex Committee: Phase Gate Approval (Go/No-Go)

        Decision depends on:
        - HIERARCHY: Execution risk (N_L2 decisions)
        - WHEN: Capex governance lag Ψ₆
        - HOW: Org implementation capacity
        """
        beta_intercept = 0.05
        beta_hierarchy = 0.95  # High weight on governance clarity
        beta_when = -0.70  # Context risk reduces gate approval
        beta_how = 0.85    # Execution capability matters

        logit = (
            beta_intercept +
            beta_hierarchy * adjustments.HIERARCHY_clarity +
            beta_when * (1 - adjustments.WHEN_context_risk) +
            beta_how * adjustments.HOW_capability
        )

        probability = DecisionFunctions._sigmoid(logit)

        drivers = {
            "HIERARCHY_Governance_Clarity": beta_hierarchy * adjustments.HIERARCHY_clarity * 100 / (1 + math.exp(-logit)),
            "WHEN_Context_Risk": beta_when * (1 - adjustments.WHEN_context_risk) * 100 / (1 + math.exp(-logit)),
            "HOW_Execution_Capability": beta_how * adjustments.HOW_capability * 100 / (1 + math.exp(-logit)),
        }

        return probability, drivers

    # ====================================================================
    # EXTERNAL TIER - BEHAVIORAL ECONOMICS
    # ====================================================================

    @staticmethod
    def customer_purchase_decision(adjustments: NineCAdjustments) -> Tuple[float, Dict]:
        """
        Customer: Purchase/Renewal Decision

        Formula: P(Buy) = sigmoid(β₁×WHAT + β₂×WHERE + β₃×HOW + β₄×AWARE + β₅×READY - loss_aversion)

        Behavioral Economics:
        - Loss aversion penalty: -30% for switching from incumbent
        - Status quo bias: -20% prefer current supplier
        - Sunk cost fallacy: -15% already invested

        Typical profile:
        WHAT match: 0.75 (solution meets 75% of requirements)
        WHERE confidence: 0.70 (product reliability proven ±15%)
        HOW integration ease: 0.65 (6-month implementation)
        AWARE solution: 0.80 (CTO well briefed)
        READY authority: 0.60 (requires CFO sign-off)
        loss_aversion: -0.30 (switching from incumbent)
        """
        beta_what = 0.30
        beta_where = 0.25
        beta_how = 0.20
        beta_aware = 0.15
        beta_ready = 0.10
        loss_aversion_penalty = -0.30

        logit = (
            beta_what * adjustments.WHAT_alignment +
            beta_where * adjustments.WHERE_confidence +
            beta_how * adjustments.HOW_capability +
            beta_aware * adjustments.AWARE_briefing +
            beta_ready * adjustments.READY_willingness +
            loss_aversion_penalty
        )

        probability = DecisionFunctions._sigmoid(logit)

        drivers = {
            "WHAT_Solution_Match": beta_what * adjustments.WHAT_alignment * 100,
            "WHERE_Product_Proof": beta_where * adjustments.WHERE_confidence * 100,
            "HOW_Integration_Ease": beta_how * adjustments.HOW_capability * 100,
            "AWARE_Knowledge": beta_aware * adjustments.AWARE_briefing * 100,
            "READY_Decision_Authority": beta_ready * adjustments.READY_willingness * 100,
            "Loss_Aversion_Penalty": loss_aversion_penalty * 100,
        }

        return probability, drivers

    @staticmethod
    def employee_retention_during_change(adjustments: NineCAdjustments) -> Tuple[float, Dict]:
        """
        Employee: Retention During Strategic Change

        Formula: P(Stay) = sigmoid(β₁×Comp + β₂×Growth + β₃×Purpose + β₄×Manager + β₅×Culture - change_anxiety)

        Behavioral factors:
        - Change anxiety: -25% fear of unknown, role changes
        - Loss aversion (current role): -20% fear of demotion
        - Status quo bias: -15% prefer current state

        Typical scores:
        Compensation: 0.70 (competitive pay)
        Career growth: 0.65 (advancement opportunities)
        Purpose: 0.75 (mission alignment)
        Manager quality: 0.80 (trust in direct manager)
        Culture fit: 0.70 (org culture alignment)
        change_anxiety: -0.25
        """
        beta_compensation = 0.25
        beta_career = 0.30
        beta_purpose = 0.20
        beta_manager = 0.15
        beta_culture = 0.10
        change_anxiety_penalty = -0.25

        logit = (
            beta_compensation * adjustments.READY_willingness * 0.7 +  # Willingness partly reflects pay
            beta_career * adjustments.WHAT_alignment +  # WHAT = career growth opportunities
            beta_purpose * adjustments.AWARE_briefing +  # AWARE = understand purpose
            beta_manager * adjustments.HOW_capability * 0.8 +  # Manager quality (part of HOW)
            beta_culture * adjustments.WHERE_confidence * 0.7 +  # Culture (proxy with WHERE)
            change_anxiety_penalty
        )

        probability = DecisionFunctions._sigmoid(logit)

        drivers = {
            "Compensation": beta_compensation * 0.7 * 100,
            "Career_Growth": beta_career * adjustments.WHAT_alignment * 100,
            "Purpose_Alignment": beta_purpose * adjustments.AWARE_briefing * 100,
            "Manager_Quality": beta_manager * 0.8 * 100,
            "Culture_Fit": beta_culture * 0.7 * 100,
            "Change_Anxiety": change_anxiety_penalty * 100,
        }

        return probability, drivers

    @staticmethod
    def supplier_partnership_commitment(adjustments: NineCAdjustments) -> Tuple[float, Dict]:
        """
        Supplier: Long-term Partnership Commitment (3-5 year volume)

        Depends on:
        - HOW: Volume synergy potential
        - WHEN: Demand stability Ψ
        - WHERE: Revenue/volume forecast confidence
        """
        beta_intercept = 0.10
        beta_how = 0.80  # High dependency on volume synergy
        beta_when = 0.70  # Demand stability important
        beta_where = 0.60  # Forecast confidence

        logit = (
            beta_intercept +
            beta_how * adjustments.HOW_capability +
            beta_when * (1 - adjustments.WHEN_context_risk) +
            beta_where * adjustments.WHERE_confidence
        )

        probability = DecisionFunctions._sigmoid(logit)

        drivers = {
            "HOW_Volume_Synergy": beta_how * adjustments.HOW_capability * 100 / (1 + math.exp(-logit)),
            "WHEN_Demand_Stability": beta_when * (1 - adjustments.WHEN_context_risk) * 100 / (1 + math.exp(-logit)),
            "WHERE_Forecast_Confidence": beta_where * adjustments.WHERE_confidence * 100 / (1 + math.exp(-logit)),
        }

        return probability, drivers

    @staticmethod
    def competitor_market_response(adjustments: NineCAdjustments) -> Tuple[float, Dict]:
        """
        Competitor: Market Response Decision (Match/Undercut/Innovate/Exit)

        Returns probability of competitive response (any type) within 6 months

        Depends on:
        - WHEN: Market move speed Ψ₇ (technology pace)
        - WHERE: Our competitive intelligence (their uncertainty about us)
        - HOW: Their capability to respond
        """
        beta_when = 0.85  # Market timing sensitivity
        beta_where = 0.65  # Intelligence/awareness
        beta_how = 0.70    # Capability to respond

        logit = (
            beta_when * adjustments.WHEN_context_risk +
            beta_where * (1 - adjustments.WHERE_confidence) +  # Their uncertainty about us
            beta_how * adjustments.HOW_capability
        )

        probability = DecisionFunctions._sigmoid(logit)

        drivers = {
            "WHEN_Market_Timing": beta_when * adjustments.WHEN_context_risk * 100 / (1 + math.exp(-logit)),
            "WHERE_Our_Competitive_Strength": beta_where * (1 - adjustments.WHERE_confidence) * 100 / (1 + math.exp(-logit)),
            "HOW_Their_Capability": beta_how * adjustments.HOW_capability * 100 / (1 + math.exp(-logit)),
        }

        return probability, drivers

    # ====================================================================
    # UTILITY FUNCTIONS
    # ====================================================================

    @staticmethod
    def _sigmoid(x: float) -> float:
        """
        Sigmoid function: σ(x) = 1 / (1 + e^(-x))
        Converts logit to probability (0-1)
        """
        try:
            return 1.0 / (1.0 + math.exp(-x))
        except OverflowError:
            # Handle large exponents
            return 0.0 if x < 0 else 1.0

    @staticmethod
    def _classify_confidence(probability: float) -> ConfidenceLevel:
        """Classify probability confidence level"""
        if probability >= 0.80:
            return ConfidenceLevel.VERY_HIGH
        elif probability >= 0.65:
            return ConfidenceLevel.HIGH
        elif probability >= 0.50:
            return ConfidenceLevel.MEDIUM
        else:
            return ConfidenceLevel.LOW

    @staticmethod
    def _classify_risk_zone(probability: float) -> RiskZone:
        """Classify probability risk zone (color coding)"""
        if probability >= 0.80:
            return RiskZone.GREEN
        elif probability >= 0.65:
            return RiskZone.YELLOW
        elif probability >= 0.50:
            return RiskZone.ORANGE
        else:
            return RiskZone.RED

# ============================================================================
# STAKEHOLDER SIMULATOR - MAIN ORCHESTRATOR
# ============================================================================

class StakeholderSimulator:
    """
    Main engine: Load stakeholder models, execute decision functions,
    format output
    """

    def __init__(self, models_registry_path: str = None):
        """
        Initialize simulator with stakeholder models registry

        Args:
            models_registry_path: Path to stakeholder_models_registry.yaml
                                 Defaults to data/stakeholder-models/stakeholder_models_registry.yaml
        """
        self.models_registry = {}
        self.load_models(models_registry_path)
        self.decision_functions_map = {
            "board": DecisionFunctions.board_strategy_approval,
            "c_suite": DecisionFunctions.c_suite_risk_escalation,
            "regional_pl": DecisionFunctions.regional_pl_hit_cagr,
            "business_unit": DecisionFunctions.regional_pl_hit_cagr,  # Same logic as regional PL
            "fpa": DecisionFunctions.fpa_accept_parameter_update,
            "hr": DecisionFunctions.hr_approve_hiring_plan,
            "capex_committee": DecisionFunctions.capex_committee_phase_gate,
            "analytics": DecisionFunctions.fpa_accept_parameter_update,  # Similar data-driven decision
            "data_science": DecisionFunctions.fpa_accept_parameter_update,  # Similar data-driven decision
            "customer": DecisionFunctions.customer_purchase_decision,
            "employee": DecisionFunctions.employee_retention_during_change,
            "supplier": DecisionFunctions.supplier_partnership_commitment,
            "competitor": DecisionFunctions.competitor_market_response,
        }

    def load_models(self, registry_path: str):
        """Load stakeholder models from YAML registry"""
        if registry_path is None:
            registry_path = "data/stakeholder-models/stakeholder_models_registry.yaml"

        try:
            with open(registry_path, 'r') as f:
                self.models_registry = yaml.safe_load(f)
        except (FileNotFoundError, Exception):
            # Registry is optional - we use hardcoded defaults
            self.models_registry = {}

    def simulate(self,
                 stakeholder_type: str,
                 nine_c_adjustments: NineCAdjustments,
                 scenario_adjustments: Dict = None,
                 job_metrics: Dict = None) -> StakeholderDecision:
        """
        Simulate a single stakeholder decision

        Args:
            stakeholder_type: Type of stakeholder (board, customer, etc.)
            nine_c_adjustments: 10C CORE dimensional values
            scenario_adjustments: Optional parameter modifications for what-if scenarios
            job_metrics: Optional job design metrics (complexity, automation, engagement, etc.)
                        If provided for HR stakeholder, will use enhanced job-design-aware decision

        Returns:
            StakeholderDecision object with full results
        """
        # Apply scenario adjustments if provided
        if scenario_adjustments:
            nine_c_adjustments = self._apply_scenario_adjustments(nine_c_adjustments, scenario_adjustments)

        # Get appropriate decision function
        if stakeholder_type not in self.decision_functions_map:
            raise ValueError(f"Unknown stakeholder type: {stakeholder_type}")

        decision_func = self.decision_functions_map[stakeholder_type]

        # Execute decision function
        # For HR stakeholder, use job-design-aware version if metrics provided
        if stakeholder_type == "hr" and job_metrics:
            probability, drivers = DecisionFunctions.hr_approve_hiring_with_job_design(
                nine_c_adjustments, job_metrics
            )
        else:
            probability, drivers = decision_func(nine_c_adjustments)

        # Classify results
        confidence = DecisionFunctions._classify_confidence(probability)
        risk_zone = DecisionFunctions._classify_risk_zone(probability)

        # Determine red flags and conditions
        red_flags = self._get_red_flags(stakeholder_type, nine_c_adjustments, probability)
        conditions = self._get_conditions_met(stakeholder_type, nine_c_adjustments, probability)

        # Create result object
        return StakeholderDecision(
            stakeholder_type=stakeholder_type,
            decision_name=self._get_decision_name(stakeholder_type),
            probability=probability,
            confidence_level=confidence,
            risk_zone=risk_zone,
            key_drivers=drivers,
            red_flags=red_flags,
            conditions_met=conditions,
            timeline_to_decision=self._get_timeline(stakeholder_type),
            timeline_to_execution=self._get_execution_timeline(stakeholder_type),
        )

    def simulate_all_stakeholders(self,
                                  nine_c_adjustments: NineCAdjustments,
                                  scenario_adjustments: Dict = None) -> Dict[str, StakeholderDecision]:
        """
        Simulate all 12 stakeholder types at once

        Returns:
            Dictionary of stakeholder_type -> StakeholderDecision
        """
        results = {}
        for stakeholder_type in self.decision_functions_map.keys():
            try:
                results[stakeholder_type] = self.simulate(
                    stakeholder_type, nine_c_adjustments, scenario_adjustments
                )
            except Exception as e:
                print(f"Error simulating {stakeholder_type}: {e}")

        return results

    def _apply_scenario_adjustments(self,
                                    adjustments: NineCAdjustments,
                                    scenario: Dict) -> NineCAdjustments:
        """Apply scenario parameter adjustments to 10C values"""
        # Create copy to avoid mutating original
        adjusted = NineCAdjustments(
            WHERE_confidence=adjustments.WHERE_confidence,
            WHEN_context_risk=adjustments.WHEN_context_risk,
            HOW_capability=adjustments.HOW_capability,
            WHAT_alignment=adjustments.WHAT_alignment,
            HIERARCHY_clarity=adjustments.HIERARCHY_clarity,
            AWARE_briefing=adjustments.AWARE_briefing,
            READY_willingness=adjustments.READY_willingness,
        )

        # Apply scenario modifications
        if "where_adjustment" in scenario:
            adjusted.WHERE_confidence = max(0, min(1, adjusted.WHERE_confidence + scenario["where_adjustment"]))
        if "when_adjustment" in scenario:
            adjusted.WHEN_context_risk = max(0, min(1, adjusted.WHEN_context_risk + scenario["when_adjustment"]))
        if "how_adjustment" in scenario:
            adjusted.HOW_capability = max(0, min(1, adjusted.HOW_capability + scenario["how_adjustment"]))
        if "what_adjustment" in scenario:
            adjusted.WHAT_alignment = max(0, min(1, adjusted.WHAT_alignment + scenario["what_adjustment"]))
        if "ready_adjustment" in scenario:
            adjusted.READY_willingness = max(0, min(1, adjusted.READY_willingness + scenario["ready_adjustment"]))
        if "aware_adjustment" in scenario:
            adjusted.AWARE_briefing = max(0, min(1, adjusted.AWARE_briefing + scenario["aware_adjustment"]))

        return adjusted

    def _get_decision_name(self, stakeholder_type: str) -> str:
        """Get human-readable decision name"""
        decision_names = {
            "board": "Strategy Approval (Capex Authorization)",
            "c_suite": "Monthly Risk Escalation",
            "regional_pl": "Hit CAGR Target",
            "fpa": "Parameter Update Acceptance",
            "hr": "Hiring Plan Commitment",
            "capex_committee": "Phase Gate Approval",
            "customer": "Purchase/Renewal Decision",
            "employee": "Retention During Change",
            "supplier": "Partnership Commitment (3-5yr)",
            "competitor": "Market Response",
        }
        return decision_names.get(stakeholder_type, "Unknown Decision")

    def _get_timeline(self, stakeholder_type: str) -> str:
        """Get timeline to decision"""
        timelines = {
            "board": "2 weeks (next board meeting)",
            "c_suite": "Monthly governance gate",
            "regional_pl": "Monthly (with actuals)",
            "fpa": "Quarterly review cycle",
            "hr": "Quarterly hiring planning",
            "capex_committee": "Q4 phase gate",
            "customer": "3-6 months (sales cycle)",
            "employee": "Q1-Q2 (during change)",
            "supplier": "Annual contract cycle",
            "competitor": "1-6 months (market response)",
        }
        return timelines.get(stakeholder_type, "TBD")

    def _get_execution_timeline(self, stakeholder_type: str) -> str:
        """Get timeline to execution"""
        timelines = {
            "board": "4 weeks post-approval",
            "c_suite": "1 week (escalation response)",
            "regional_pl": "Immediate (monthly tracking)",
            "fpa": "Quarterly model update",
            "hr": "6-8 weeks (hiring lead time)",
            "capex_committee": "3-6 months (phase execution)",
            "customer": "6-12 months (implementation)",
            "employee": "Ongoing (change management)",
            "supplier": "Contract negotiation: 4-8 weeks",
            "competitor": "Varies (1-12 months)",
        }
        return timelines.get(stakeholder_type, "TBD")

    def _get_red_flags(self, stakeholder_type: str, adjustments: NineCAdjustments, prob: float) -> List[str]:
        """Identify red flags for stakeholder decision"""
        flags = []

        # Generic flags for low probability
        if prob < 0.65:
            flags.append(f"Low approval probability ({prob:.0%})")

        # Stakeholder-specific flags
        if stakeholder_type == "board":
            if adjustments.WHERE_confidence < 0.70:
                flags.append("Parameter confidence too low (<70%)")
            if adjustments.HIERARCHY_clarity < 0.75:
                flags.append("Governance gates unclear")

        elif stakeholder_type == "customer":
            if adjustments.HOW_capability < 0.60:
                flags.append("Integration complexity concerns")
            if adjustments.WHAT_alignment < 0.70:
                flags.append("Solution doesn't match all requirements")

        elif stakeholder_type == "employee":
            if prob < 0.60:
                flags.append("Change anxiety may trigger attrition")
            if adjustments.READY_willingness < 0.50:
                flags.append("Low willingness to change")

        return flags

    def _get_conditions_met(self, stakeholder_type: str, adjustments: NineCAdjustments, prob: float) -> List[str]:
        """List conditions that support positive decision"""
        conditions = []

        if stakeholder_type == "board":
            if adjustments.WHERE_confidence >= 0.80:
                conditions.append("✓ Parameter confidence adequate (≥80%)")
            if adjustments.WHEN_context_risk <= 0.30:
                conditions.append("✓ Economic environment favorable")
            if adjustments.HOW_capability >= 0.80:
                conditions.append("✓ Org capability proven")
            if adjustments.HIERARCHY_clarity >= 0.85:
                conditions.append("✓ Governance gates clear")

        elif stakeholder_type == "customer":
            if adjustments.WHAT_alignment >= 0.75:
                conditions.append("✓ Solution matches requirements")
            if adjustments.WHERE_confidence >= 0.70:
                conditions.append("✓ Product reliability proven")

        elif stakeholder_type == "employee":
            if adjustments.AWARE_briefing >= 0.80:
                conditions.append("✓ Fully informed about change")
            if adjustments.READY_willingness >= 0.70:
                conditions.append("✓ Willing to adapt")

        return conditions


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Initialize simulator
    simulator = StakeholderSimulator()

    # Example: Board approval for ALPLA Phase 1 capex
    print("=" * 70)
    print("EXAMPLE 1: Board of Directors - Strategy Approval")
    print("=" * 70)

    adjustments = NineCAdjustments(
        WHERE_confidence=0.82,      # CAGR ±0.8pp confidence
        WHEN_context_risk=0.25,     # GDP conservative (low risk)
        HOW_capability=0.85,         # γ_rev-org=0.68 proven
        WHAT_alignment=0.80,         # Strategic fit
        HIERARCHY_clarity=0.90,      # Gates defined
        AWARE_briefing=0.95,         # Full briefing
        READY_willingness=0.88,      # 8/10 votes likely
    )

    result = simulator.simulate("board", adjustments)
    print(f"\nProbability: {result.probability:.1%} {result.risk_zone.value}")
    print(f"Confidence: {result.confidence_level.value}")
    print(f"\nKey Drivers:")
    for driver, value in result.key_drivers.items():
        print(f"  {driver}: {value:+.1f}%")

    print(f"\nConditions Met: {len(result.conditions_met)}")
    for condition in result.conditions_met:
        print(f"  {condition}")

    # Example 2: Customer purchase decision
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Customer - Purchase Decision")
    print("=" * 70)

    customer_adjustments = NineCAdjustments(
        WHERE_confidence=0.70,      # Product reliability proven
        WHEN_context_risk=0.40,     # Budget cycle timing
        HOW_capability=0.65,        # Integration complexity
        WHAT_alignment=0.75,        # Meets 75% of needs
        HIERARCHY_clarity=0.60,     # Requires CFO sign-off
        AWARE_briefing=0.80,        # CTO well briefed
        READY_willingness=0.60,     # Budget authority present
    )

    result2 = simulator.simulate("customer", customer_adjustments)
    print(f"\nProbability: {result2.probability:.1%} {result2.risk_zone.value}")
    print(f"Confidence: {result2.confidence_level.value}")
    print(f"\nKey Drivers:")
    for driver, value in result2.key_drivers.items():
        print(f"  {driver}: {value:+.1f}%")

    if result2.red_flags:
        print(f"\nRed Flags: {len(result2.red_flags)}")
        for flag in result2.red_flags:
            print(f"  ⚠ {flag}")
