"""
Strategic Bank Decision-Making System (SBDMS) v1.0
Framework for hierarchical strategic decision modeling in global financial institutions

Supports three decision types:
  1. Market Entry Decisions
  2. Credit/Risk Classification Decisions
  3. Capital Allocation & M&A Decisions

Single Source of Truth: models/SBDMS-1-0-BANK-STRATEGY/model-definition.yaml
"""

import numpy as np
import yaml
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path


class DecisionLevel(Enum):
    """Organizational hierarchy levels"""
    BOARD = "board"
    DIVISION = "division"
    OPERATIONAL = "operational"


class DecisionType(Enum):
    """Strategic decision types"""
    MARKET_ENTRY = "market_entry"
    CREDIT_CLASSIFICATION = "credit_classification"
    CAPITAL_ALLOCATION = "capital_allocation"


class ContextEnvironment(Enum):
    """Economic/market contexts"""
    NORMAL = "normal"
    GROWTH = "growth"
    CRISIS = "crisis"


@dataclass
class DecisionContext:
    """Environmental context that modulates decision weights"""
    market_volatility: float  # VIX-like metric (10-80)
    regulatory_tightness: float  # 0 (loose) to 1 (tight)
    capital_position: float  # 0 (deficit) to 1 (surplus)
    management_risk_appetite: float  # 0 (conservative) to 1 (aggressive)
    economic_cycle: str  # "expansion", "normal", "contraction"

    def environment_classification(self) -> ContextEnvironment:
        """Classify context into environment type"""
        if self.market_volatility > 40 or self.regulatory_tightness > 0.7:
            return ContextEnvironment.CRISIS
        elif self.economic_cycle == "expansion" and self.capital_position > 0.6:
            return ContextEnvironment.GROWTH
        else:
            return ContextEnvironment.NORMAL


@dataclass
class StrategicDecision:
    """Core strategic decision dimensions"""
    name: str
    decision_type: DecisionType
    organization_level: DecisionLevel

    # Six core dimensions (0-1 scale)
    financial: float  # F: ROI, NPV, profit impact
    strategic: float  # S: Strategic alignment, competitive fit
    risk: float  # R: Net risk exposure (note: inverted, high=bad)
    practical: float  # P: Operational feasibility
    emotional: float  # E: Management conviction
    regulatory: float  # Reg: Regulatory approval probability

    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary for analysis"""
        return {
            'financial': self.financial,
            'strategic': self.strategic,
            'risk': self.risk,
            'practical': self.practical,
            'emotional': self.emotional,
            'regulatory': self.regulatory
        }

    def validate(self) -> bool:
        """Validate all dimensions in [0,1]"""
        for dim_name, dim_value in self.to_dict().items():
            if not (0.0 <= dim_value <= 1.0):
                raise ValueError(f"{dim_name} must be in [0,1], got {dim_value}")
        return True


@dataclass
class DecisionScore:
    """Result of decision scoring"""
    decision_name: str
    decision_type: DecisionType
    organization_level: DecisionLevel

    utility_score: float  # Raw utility (-∞ to +∞)
    approval_probability: float  # Logistic transformed (0-1)
    ranking: int  # For comparison across decisions
    decision_recommendation: str  # "GO", "CONDITIONAL", "NO-GO"

    # Dimension contributions
    dimension_scores: Dict[str, float]
    complementarity_effects: Dict[str, float]

    # Context information
    context_environment: str


class StrategicBankDecisionModel:
    """
    Main decision-making model with hierarchical structure
    """

    def __init__(self, model_yaml_path: str):
        """
        Initialize model from YAML definition

        Args:
            model_yaml_path: Path to model-definition.yaml
        """
        self.model_path = Path(model_yaml_path)
        with open(self.model_path, 'r') as f:
            self.model_spec = yaml.safe_load(f)

        self.model_id = self.model_spec['model_id']
        self.status = self.model_spec['metadata']['status']
        self.confidence = self.model_spec['metadata']['confidence']

        # Load parameters per level
        self._load_parameters()

    def _load_parameters(self):
        """Load hierarchical parameters from YAML"""
        self.parameters = {}
        for level_spec in self.model_spec['hierarchical_parameters']:
            level_name = level_spec['level']
            self.parameters[level_name] = {
                'intercept': level_spec['intercept'],
                'weights': level_spec['weights'],
                'risk_appetite_constraint': level_spec.get('risk_appetite_constraint', 1.0)
            }

        # Load complementarity matrix
        self.complementarity_matrix = {}
        for comp in self.model_spec.get('complementarity_parameters', []):
            key = comp['parameter']
            self.complementarity_matrix[key] = {
                'symbols': comp['symbols'],
                'value': comp['value'],
                'interpretation': comp['interpretation']
            }

    def calculate_utility(
        self,
        decision: StrategicDecision,
        context: DecisionContext
    ) -> float:
        """
        Calculate utility score for a strategic decision

        Formula:
        U = β₀ + Σβᵢ·Cᵢ + Σγᵢⱼ·Cᵢ·Cⱼ + β_Ψ·Ψ

        Args:
            decision: StrategicDecision with all dimensions
            context: DecisionContext environmental factors

        Returns:
            Utility score (unbounded)
        """
        decision.validate()

        level = decision.organization_level.value
        params = self.parameters[level]

        # Intercept
        utility = params['intercept']

        # Linear dimension contributions
        dimensions = decision.to_dict()
        weights = params['weights']
        for dim_name, dim_value in dimensions.items():
            if dim_name in weights:
                utility += weights[dim_name] * dim_value

        # Complementarity interactions
        utility += self._apply_complementarities(decision)

        # Context modulation
        utility += self._apply_context_modulation(decision, context)

        return utility

    def _apply_complementarities(self, decision: StrategicDecision) -> float:
        """
        Calculate complementarity (γ) interaction effects

        Main complementarities:
        - γ(F,S) = +0.15: Financial + Strategic synergy
        - γ(F,R) = -0.20: Financial-Risk trade-off
        - γ(R,P) = -0.15: Risk + Practical complexity
        - γ(S,E) = +0.12: Strategic + Emotional conviction
        - γ(Reg,P) = +0.10: Regulatory + Practical feasibility
        """
        dims = decision.to_dict()

        complementarity_contribution = 0.0

        # Define all complementarity pairs
        complementarities = {
            ('financial', 'strategic'): 0.15,
            ('financial', 'risk'): -0.20,
            ('risk', 'practical'): -0.15,
            ('strategic', 'emotional'): 0.12,
            ('regulatory', 'practical'): 0.10,
            ('financial', 'emotional'): 0.08,
            ('strategic', 'risk'): -0.10
        }

        for (dim1, dim2), gamma_value in complementarities.items():
            if dim1 in dims and dim2 in dims:
                complementarity_contribution += gamma_value * dims[dim1] * dims[dim2]

        return complementarity_contribution

    def _apply_context_modulation(
        self,
        decision: StrategicDecision,
        context: DecisionContext
    ) -> float:
        """
        Apply context-dependent modulation to utility

        Context effects:
        - Crisis: Increase risk weight, decrease strategic weight
        - Growth: Increase strategic weight, decrease risk aversion
        - Normal: Baseline weights
        """
        env = context.environment_classification()

        modulation = 0.0

        if env == ContextEnvironment.CRISIS:
            # In crisis, risk aversion increases
            modulation -= 0.30 * (1.0 - context.management_risk_appetite)

        elif env == ContextEnvironment.GROWTH:
            # In growth mode, strategic ambition increases
            modulation += 0.20 * context.management_risk_appetite

        # Capital constraint: shortage reduces willingness to take on new decisions
        if context.capital_position < 0.5:
            modulation -= 0.15 * (0.5 - context.capital_position)

        return modulation

    def approve_probability(self, utility_score: float) -> float:
        """
        Convert utility score to approval probability via logistic function

        P(Approve) = 1 / (1 + exp(-U))

        Args:
            utility_score: Raw utility score

        Returns:
            Probability in [0, 1]
        """
        return 1.0 / (1.0 + np.exp(-utility_score))

    def score_market_entry(
        self,
        decision: StrategicDecision,
        context: DecisionContext
    ) -> DecisionScore:
        """
        Score a market entry decision

        Special logic for market entry decisions
        """
        decision.decision_type = DecisionType.MARKET_ENTRY
        decision.validate()

        utility = self.calculate_utility(decision, context)
        prob = self.approve_probability(utility)

        # Market entry recommendation thresholds
        if prob > 0.70:
            recommendation = "GO"
        elif prob > 0.50:
            recommendation = "CONDITIONAL"
        else:
            recommendation = "NO-GO"

        return DecisionScore(
            decision_name=decision.name,
            decision_type=decision.decision_type,
            organization_level=decision.organization_level,
            utility_score=utility,
            approval_probability=prob,
            ranking=0,  # Will be set after sorting
            decision_recommendation=recommendation,
            dimension_scores=decision.to_dict(),
            complementarity_effects=self._get_complementarity_breakdown(decision),
            context_environment=context.environment_classification().value
        )

    def score_credit_decision(
        self,
        decision: StrategicDecision,
        context: DecisionContext
    ) -> DecisionScore:
        """
        Score a credit/risk classification decision

        Special logic for credit decisions
        """
        decision.decision_type = DecisionType.CREDIT_CLASSIFICATION
        decision.validate()

        utility = self.calculate_utility(decision, context)
        prob = self.approve_probability(utility)

        # Credit approval thresholds
        if prob > 0.80:
            recommendation = "APPROVE"
        elif prob > 0.60:
            recommendation = "APPROVE_WITH_CONDITIONS"
        elif prob > 0.40:
            recommendation = "COMMITTEE_REVIEW"
        else:
            recommendation = "REJECT"

        return DecisionScore(
            decision_name=decision.name,
            decision_type=decision.decision_type,
            organization_level=decision.organization_level,
            utility_score=utility,
            approval_probability=prob,
            ranking=0,
            decision_recommendation=recommendation,
            dimension_scores=decision.to_dict(),
            complementarity_effects=self._get_complementarity_breakdown(decision),
            context_environment=context.environment_classification().value
        )

    def score_capital_allocation(
        self,
        decision: StrategicDecision,
        context: DecisionContext
    ) -> DecisionScore:
        """
        Score a capital allocation / M&A decision

        Special logic for capital allocation decisions
        """
        decision.decision_type = DecisionType.CAPITAL_ALLOCATION
        decision.validate()

        utility = self.calculate_utility(decision, context)
        prob = self.approve_probability(utility)

        # M&A approval thresholds
        if prob > 0.75:
            recommendation = "GO"
        elif prob > 0.50:
            recommendation = "CONDITIONAL"
        else:
            recommendation = "NO-GO"

        return DecisionScore(
            decision_name=decision.name,
            decision_type=decision.decision_type,
            organization_level=decision.organization_level,
            utility_score=utility,
            approval_probability=prob,
            ranking=0,
            decision_recommendation=recommendation,
            dimension_scores=decision.to_dict(),
            complementarity_effects=self._get_complementarity_breakdown(decision),
            context_environment=context.environment_classification().value
        )

    def _get_complementarity_breakdown(self, decision: StrategicDecision) -> Dict[str, float]:
        """Get detailed complementarity effects breakdown"""
        dims = decision.to_dict()
        effects = {}

        complementarities = {
            'F×S': (('financial', 'strategic'), 0.15),
            'F×R': (('financial', 'risk'), -0.20),
            'R×P': (('risk', 'practical'), -0.15),
            'S×E': (('strategic', 'emotional'), 0.12),
            'Reg×P': (('regulatory', 'practical'), 0.10),
            'F×E': (('financial', 'emotional'), 0.08),
            'S×R': (('strategic', 'risk'), -0.10)
        }

        for label, ((dim1, dim2), gamma) in complementarities.items():
            if dim1 in dims and dim2 in dims:
                effects[label] = gamma * dims[dim1] * dims[dim2]

        return effects

    def apply_hierarchy_constraint(
        self,
        l2_decision: DecisionScore,
        l1_risk_appetite: float
    ) -> DecisionScore:
        """
        Apply Level 1 (Board) constraint to Level 2 (Division) decision

        Board sets max acceptable risk; Division cannot exceed it

        Args:
            l2_decision: Decision score at Division level
            l1_risk_appetite: Board's max acceptable risk (0-1)

        Returns:
            Constrained decision score
        """
        if l2_decision.dimension_scores['risk'] > (1.0 - l1_risk_appetite):
            # Decision violates risk constraint; adjust recommendation
            l2_decision.decision_recommendation = "VIOLATES_RISK_CONSTRAINT"
            # Reduce approval probability to reflect constraint violation
            l2_decision.approval_probability *= 0.5
            return l2_decision

        return l2_decision

    def get_model_summary(self) -> str:
        """Return human-readable model summary"""
        return f"""
╔════════════════════════════════════════════════════════╗
║   Strategic Bank Decision-Making System (SBDMS) 1.0  ║
╚════════════════════════════════════════════════════════╝

Model ID: {self.model_id}
Status: {self.status}
Confidence: {self.confidence}

THREE DECISION TYPES:
  1. Market Entry Decisions
     - Determine whether to enter new market/product/segment
     - Horizon: 3-5 years
     - Approval threshold: P > 0.70

  2. Credit/Risk Classification
     - Approve customer, set risk rating, determine conditions
     - Horizon: Days-weeks
     - Approval threshold: P > 0.80

  3. Capital Allocation / M&A
     - Decide whether to acquire or invest
     - Horizon: 3-5 years
     - Approval threshold: P > 0.75

HIERARCHICAL STRUCTURE:
  Board (L1)    → Sets risk appetite (0-1 constraint)
    ↓
  Division (L2) → Implements tactic (allocates risk budget)
    ↓
  Operations (L3) → Makes deal-by-deal decisions

CORE DIMENSIONS:
  Financial (F):     ROI, NPV, profit impact [0-1]
  Strategic (S):     Strategic alignment, competitive fit [0-1]
  Risk (R):          Net risk exposure, inverted [0-1]
  Practical (P):     Operational feasibility [0-1]
  Emotional (E):     Management conviction [0-1]
  Regulatory (Reg):  Regulatory approval probability [0-1]

COMPLEMENTARITY MATRIX:
  γ(F,S) = +0.15   Financial + Strategic = Synergy
  γ(F,R) = -0.20   Financial vs Risk = Trade-off
  γ(R,P) = -0.15   Risk + Complexity = Problem
  γ(S,E) = +0.12   Strategy + Conviction = Execution
  γ(Reg,P) = +0.10 Compliance + Feasibility = Efficiency

CONTEXT MODULATION:
  Normal: Baseline weights
  Crisis: Risk weight ↑ 50%, Strategic weight ↓ 30%
  Growth: Strategic weight ↑ 40%, Risk aversion ↓ 20%
"""


# ============================================================================
# USAGE EXAMPLE
# ============================================================================

if __name__ == "__main__":
    # Initialize model
    model = StrategicBankDecisionModel("model-definition.yaml")
    print(model.get_model_summary())

    # Define context
    normal_context = DecisionContext(
        market_volatility=20.0,
        regulatory_tightness=0.4,
        capital_position=0.7,
        management_risk_appetite=0.6,
        economic_cycle="normal"
    )

    crisis_context = DecisionContext(
        market_volatility=55.0,
        regulatory_tightness=0.75,
        capital_position=0.3,
        management_risk_appetite=0.3,
        economic_cycle="contraction"
    )

    # Example 1: Market Entry Decision
    print("\n" + "="*60)
    print("EXAMPLE 1: Market Entry Decision")
    print("="*60)

    market_entry = StrategicDecision(
        name="Enter Singapore Wealth Management",
        decision_type=DecisionType.MARKET_ENTRY,
        organization_level=DecisionLevel.DIVISION,
        financial=0.80,
        strategic=0.75,
        risk=0.40,
        practical=0.70,
        emotional=0.65,
        regulatory=0.85
    )

    entry_score = model.score_market_entry(market_entry, normal_context)
    print(f"Decision: {entry_score.decision_name}")
    print(f"Recommendation: {entry_score.decision_recommendation}")
    print(f"Approval Probability: {entry_score.approval_probability:.1%}")
    print(f"Utility Score: {entry_score.utility_score:.3f}")
    print(f"Dimension Scores: {entry_score.dimension_scores}")

    # Example 2: Credit Decision
    print("\n" + "="*60)
    print("EXAMPLE 2: Credit Classification Decision")
    print("="*60)

    credit_decision = StrategicDecision(
        name="Approve Fortune 500 Technology Company",
        decision_type=DecisionType.CREDIT_CLASSIFICATION,
        organization_level=DecisionLevel.OPERATIONAL,
        financial=0.85,
        strategic=0.70,
        risk=0.25,  # Low risk (good credit)
        practical=0.90,
        emotional=0.80,
        regulatory=0.95
    )

    credit_score = model.score_credit_decision(credit_decision, normal_context)
    print(f"Decision: {credit_score.decision_name}")
    print(f"Recommendation: {credit_score.decision_recommendation}")
    print(f"Approval Probability: {credit_score.approval_probability:.1%}")
    print(f"Utility Score: {credit_score.utility_score:.3f}")

    # Example 3: Crisis Context
    print("\n" + "="*60)
    print("EXAMPLE 3: Market Entry in CRISIS Context")
    print("="*60)

    entry_crisis = model.score_market_entry(market_entry, crisis_context)
    print(f"Decision: {entry_crisis.decision_name}")
    print(f"Recommendation: {entry_crisis.decision_recommendation}")
    print(f"Approval Probability: {entry_crisis.approval_probability:.1%}")
    print(f"Crisis Context Impact: {entry_score.approval_probability - entry_crisis.approval_probability:.1%} reduction")

    # Example 4: Capital Allocation
    print("\n" + "="*60)
    print("EXAMPLE 4: M&A Decision – Acquire Regional Bank")
    print("="*60)

    ma_decision = StrategicDecision(
        name="Acquire Regional Wealth Manager",
        decision_type=DecisionType.CAPITAL_ALLOCATION,
        organization_level=DecisionLevel.BOARD,
        financial=0.75,
        strategic=0.85,
        risk=0.50,  # Integration risk
        practical=0.55,  # Complex integration
        emotional=0.70,
        regulatory=0.80
    )

    ma_score = model.score_capital_allocation(ma_decision, normal_context)
    print(f"Decision: {ma_score.decision_name}")
    print(f"Recommendation: {ma_score.decision_recommendation}")
    print(f"Approval Probability: {ma_score.approval_probability:.1%}")
    print(f"Utility Score: {ma_score.utility_score:.3f}")
    print(f"Risk-Practical Complementarity: {ma_score.complementarity_effects.get('R×P', 0):.3f}")
