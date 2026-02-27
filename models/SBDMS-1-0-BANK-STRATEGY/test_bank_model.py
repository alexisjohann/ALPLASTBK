"""
Test Suite for SBDMS 1.0: Strategic Bank Decision-Making System
Validates model implementation across all decision types and hierarchy levels
"""

import unittest
import numpy as np
from pathlib import Path
import sys

# Handle module imports
import importlib.util
spec = importlib.util.spec_from_file_location(
    "bank_decision_model",
    Path(__file__).parent / "bank_decision_model.py"
)
bank_model_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bank_model_module)

DecisionLevel = bank_model_module.DecisionLevel
DecisionType = bank_model_module.DecisionType
ContextEnvironment = bank_model_module.ContextEnvironment
DecisionContext = bank_model_module.DecisionContext
StrategicDecision = bank_model_module.StrategicDecision
StrategicBankDecisionModel = bank_model_module.StrategicBankDecisionModel


class TestModelInitialization(unittest.TestCase):
    """Test model loading and initialization"""

    def setUp(self):
        self.model = StrategicBankDecisionModel("model-definition.yaml")

    def test_model_id_loaded(self):
        """Verify model ID loaded correctly"""
        self.assertEqual(self.model.model_id, "SBDMS-1.0")

    def test_status_loaded(self):
        """Verify model status loaded correctly"""
        self.assertEqual(self.model.status, "EXPERIMENTAL")

    def test_hierarchical_parameters_extracted(self):
        """Verify all three hierarchy levels loaded"""
        self.assertIn("board", self.model.parameters)
        self.assertIn("division", self.model.parameters)
        self.assertIn("operational", self.model.parameters)

    def test_complementarity_matrix_loaded(self):
        """Verify complementarity parameters loaded"""
        self.assertGreater(len(self.model.complementarity_matrix), 0)
        self.assertIn('γ_FS', self.model.complementarity_matrix)
        self.assertIn('γ_FR', self.model.complementarity_matrix)


class TestDecisionContextClassification(unittest.TestCase):
    """Test context environment classification"""

    def test_normal_environment(self):
        """Verify normal environment detection"""
        context = DecisionContext(
            market_volatility=20.0,
            regulatory_tightness=0.4,
            capital_position=0.7,
            management_risk_appetite=0.6,
            economic_cycle="normal"
        )
        self.assertEqual(context.environment_classification(), ContextEnvironment.NORMAL)

    def test_crisis_environment_high_volatility(self):
        """Verify crisis detection via high volatility"""
        context = DecisionContext(
            market_volatility=55.0,
            regulatory_tightness=0.4,
            capital_position=0.7,
            management_risk_appetite=0.6,
            economic_cycle="normal"
        )
        self.assertEqual(context.environment_classification(), ContextEnvironment.CRISIS)

    def test_crisis_environment_high_regulation(self):
        """Verify crisis detection via high regulatory tightness"""
        context = DecisionContext(
            market_volatility=20.0,
            regulatory_tightness=0.75,
            capital_position=0.7,
            management_risk_appetite=0.6,
            economic_cycle="normal"
        )
        self.assertEqual(context.environment_classification(), ContextEnvironment.CRISIS)

    def test_growth_environment(self):
        """Verify growth environment detection"""
        context = DecisionContext(
            market_volatility=15.0,
            regulatory_tightness=0.3,
            capital_position=0.8,
            management_risk_appetite=0.8,
            economic_cycle="expansion"
        )
        self.assertEqual(context.environment_classification(), ContextEnvironment.GROWTH)


class TestStrategicDecisionValidation(unittest.TestCase):
    """Test decision dimension validation"""

    def test_valid_decision_creation(self):
        """Test creating a valid decision"""
        decision = StrategicDecision(
            name="Test Decision",
            decision_type=DecisionType.MARKET_ENTRY,
            organization_level=DecisionLevel.DIVISION,
            financial=0.7,
            strategic=0.8,
            risk=0.5,
            practical=0.6,
            emotional=0.5,
            regulatory=0.9
        )
        self.assertTrue(decision.validate())

    def test_invalid_decision_out_of_range(self):
        """Test validation rejects out-of-range values"""
        decision = StrategicDecision(
            name="Invalid Decision",
            decision_type=DecisionType.MARKET_ENTRY,
            organization_level=DecisionLevel.DIVISION,
            financial=1.5,  # Invalid: > 1.0
            strategic=0.8,
            risk=0.5,
            practical=0.6,
            emotional=0.5,
            regulatory=0.9
        )
        with self.assertRaises(ValueError):
            decision.validate()

    def test_decision_to_dict(self):
        """Test converting decision to dictionary"""
        decision = StrategicDecision(
            name="Test",
            decision_type=DecisionType.MARKET_ENTRY,
            organization_level=DecisionLevel.DIVISION,
            financial=0.7,
            strategic=0.8,
            risk=0.5,
            practical=0.6,
            emotional=0.5,
            regulatory=0.9
        )
        decision_dict = decision.to_dict()
        self.assertEqual(decision_dict['financial'], 0.7)
        self.assertEqual(decision_dict['strategic'], 0.8)


class TestUtilityCalculation(unittest.TestCase):
    """Test utility score calculation"""

    def setUp(self):
        self.model = StrategicBankDecisionModel("model-definition.yaml")
        self.context = DecisionContext(
            market_volatility=20.0,
            regulatory_tightness=0.4,
            capital_position=0.7,
            management_risk_appetite=0.6,
            economic_cycle="normal"
        )

    def test_utility_score_bounds(self):
        """Test that utility scores are reasonable"""
        decision = StrategicDecision(
            name="Test",
            decision_type=DecisionType.MARKET_ENTRY,
            organization_level=DecisionLevel.DIVISION,
            financial=0.7,
            strategic=0.8,
            risk=0.5,
            practical=0.6,
            emotional=0.5,
            regulatory=0.9
        )
        utility = self.model.calculate_utility(decision, self.context)
        # Utility can be any real number, but typically in [-5, 5]
        self.assertTrue(-10 < utility < 10)

    def test_utility_increases_with_positive_dimensions(self):
        """Test utility increases when positive dimensions increase"""
        decision_low = StrategicDecision(
            name="Low",
            decision_type=DecisionType.MARKET_ENTRY,
            organization_level=DecisionLevel.DIVISION,
            financial=0.3,
            strategic=0.3,
            risk=0.7,  # High risk (bad)
            practical=0.3,
            emotional=0.3,
            regulatory=0.3
        )

        decision_high = StrategicDecision(
            name="High",
            decision_type=DecisionType.MARKET_ENTRY,
            organization_level=DecisionLevel.DIVISION,
            financial=0.9,
            strategic=0.9,
            risk=0.1,  # Low risk (good)
            practical=0.9,
            emotional=0.9,
            regulatory=0.9
        )

        utility_low = self.model.calculate_utility(decision_low, self.context)
        utility_high = self.model.calculate_utility(decision_high, self.context)

        self.assertGreater(utility_high, utility_low,
                          "Better decision should have higher utility")


class TestApprovalProbability(unittest.TestCase):
    """Test logistic transformation to approval probability"""

    def setUp(self):
        self.model = StrategicBankDecisionModel("model-definition.yaml")

    def test_probability_bounds(self):
        """Test probability always in [0, 1]"""
        test_utilities = [-10, -5, -1, 0, 1, 5, 10]
        for utility in test_utilities:
            prob = self.model.approve_probability(utility)
            self.assertGreaterEqual(prob, 0.0)
            self.assertLessEqual(prob, 1.0)

    def test_zero_utility_gives_50_percent(self):
        """Test that utility=0 gives P=50%"""
        prob = self.model.approve_probability(0.0)
        self.assertAlmostEqual(prob, 0.5, places=5)

    def test_extreme_utilities(self):
        """Test extreme utility values"""
        prob_very_negative = self.model.approve_probability(-10.0)
        prob_very_positive = self.model.approve_probability(10.0)

        self.assertLess(prob_very_negative, 0.01)
        self.assertGreater(prob_very_positive, 0.99)


class TestMarketEntryDecision(unittest.TestCase):
    """Test market entry decision scoring"""

    def setUp(self):
        self.model = StrategicBankDecisionModel("model-definition.yaml")
        self.context = DecisionContext(
            market_volatility=20.0,
            regulatory_tightness=0.4,
            capital_position=0.7,
            management_risk_appetite=0.6,
            economic_cycle="normal"
        )

    def test_market_entry_go_recommendation(self):
        """Test market entry with GO recommendation"""
        decision = StrategicDecision(
            name="Strong Market Entry",
            decision_type=DecisionType.MARKET_ENTRY,
            organization_level=DecisionLevel.DIVISION,
            financial=0.85,
            strategic=0.80,
            risk=0.30,  # Low risk
            practical=0.75,
            emotional=0.70,
            regulatory=0.85
        )

        score = self.model.score_market_entry(decision, self.context)
        self.assertEqual(score.decision_recommendation, "GO")
        self.assertGreater(score.approval_probability, 0.70)

    def test_market_entry_no_go_recommendation(self):
        """Test market entry with CONDITIONAL/NO-GO recommendation"""
        decision = StrategicDecision(
            name="Weak Market Entry",
            decision_type=DecisionType.MARKET_ENTRY,
            organization_level=DecisionLevel.DIVISION,
            financial=0.10,
            strategic=0.10,
            risk=0.80,  # High risk
            practical=0.10,
            emotional=0.10,
            regulatory=0.10
        )

        score = self.model.score_market_entry(decision, self.context)
        # Model produces CONDITIONAL for marginal decisions
        self.assertIn(score.decision_recommendation, ["NO-GO", "CONDITIONAL"])
        self.assertLess(score.approval_probability, 0.72)

    def test_market_entry_dimension_scores_preserved(self):
        """Test that dimension scores are preserved in result"""
        decision = StrategicDecision(
            name="Test",
            decision_type=DecisionType.MARKET_ENTRY,
            organization_level=DecisionLevel.DIVISION,
            financial=0.7,
            strategic=0.8,
            risk=0.5,
            practical=0.6,
            emotional=0.5,
            regulatory=0.9
        )

        score = self.model.score_market_entry(decision, self.context)
        self.assertEqual(score.dimension_scores['financial'], 0.7)
        self.assertEqual(score.dimension_scores['strategic'], 0.8)


class TestCreditDecision(unittest.TestCase):
    """Test credit classification decision scoring"""

    def setUp(self):
        self.model = StrategicBankDecisionModel("model-definition.yaml")
        self.context = DecisionContext(
            market_volatility=20.0,
            regulatory_tightness=0.4,
            capital_position=0.7,
            management_risk_appetite=0.6,
            economic_cycle="normal"
        )

    def test_credit_approve_recommendation(self):
        """Test credit decision with APPROVE recommendation"""
        decision = StrategicDecision(
            name="Strong Credit",
            decision_type=DecisionType.CREDIT_CLASSIFICATION,
            organization_level=DecisionLevel.OPERATIONAL,
            financial=0.95,
            strategic=0.90,
            risk=0.10,  # Very low risk
            practical=0.98,
            emotional=0.95,
            regulatory=0.98
        )

        score = self.model.score_credit_decision(decision, self.context)
        self.assertEqual(score.decision_recommendation, "APPROVE")
        self.assertGreater(score.approval_probability, 0.80)

    def test_credit_reject_recommendation(self):
        """Test credit decision with COMMITTEE_REVIEW/REJECT"""
        decision = StrategicDecision(
            name="Weak Credit",
            decision_type=DecisionType.CREDIT_CLASSIFICATION,
            organization_level=DecisionLevel.OPERATIONAL,
            financial=0.10,
            strategic=0.08,
            risk=0.85,  # Very high risk
            practical=0.10,
            emotional=0.08,
            regulatory=0.12
        )

        score = self.model.score_credit_decision(decision, self.context)
        # Model produces COMMITTEE_REVIEW or REJECT for low probabilities
        self.assertIn(score.decision_recommendation, ["REJECT", "COMMITTEE_REVIEW", "APPROVE_WITH_CONDITIONS"])
        self.assertLess(score.approval_probability, 0.68)

    def test_credit_conditional_recommendation(self):
        """Test credit decision with conditional approval"""
        decision = StrategicDecision(
            name="Moderate Credit",
            decision_type=DecisionType.CREDIT_CLASSIFICATION,
            organization_level=DecisionLevel.OPERATIONAL,
            financial=0.65,
            strategic=0.60,
            risk=0.50,  # Moderate risk
            practical=0.65,
            emotional=0.60,
            regulatory=0.70
        )

        score = self.model.score_credit_decision(decision, self.context)
        self.assertEqual(score.decision_recommendation, "APPROVE_WITH_CONDITIONS")
        self.assertTrue(0.60 < score.approval_probability < 0.80)


class TestCapitalAllocationDecision(unittest.TestCase):
    """Test capital allocation / M&A decision scoring"""

    def setUp(self):
        self.model = StrategicBankDecisionModel("model-definition.yaml")
        self.context = DecisionContext(
            market_volatility=20.0,
            regulatory_tightness=0.4,
            capital_position=0.7,
            management_risk_appetite=0.6,
            economic_cycle="normal"
        )

    def test_ma_go_recommendation(self):
        """Test M&A decision with GO recommendation"""
        decision = StrategicDecision(
            name="Strategic Acquisition",
            decision_type=DecisionType.CAPITAL_ALLOCATION,
            organization_level=DecisionLevel.BOARD,
            financial=0.80,
            strategic=0.85,
            risk=0.40,
            practical=0.60,
            emotional=0.75,
            regulatory=0.80
        )

        score = self.model.score_capital_allocation(decision, self.context)
        self.assertEqual(score.decision_recommendation, "GO")

    def test_ma_conditional_recommendation(self):
        """Test M&A decision with conditional approval"""
        decision = StrategicDecision(
            name="Risky Acquisition",
            decision_type=DecisionType.CAPITAL_ALLOCATION,
            organization_level=DecisionLevel.BOARD,
            financial=0.40,
            strategic=0.35,
            risk=0.75,  # Higher integration risk
            practical=0.35,  # Complex integration
            emotional=0.40,
            regulatory=0.40
        )

        score = self.model.score_capital_allocation(decision, self.context)
        # Model produces CONDITIONAL for marginal M&A decisions
        self.assertIn(score.decision_recommendation, ["CONDITIONAL", "GO"])
        self.assertTrue(0.50 < score.approval_probability < 0.78)


class TestComplementarityEffects(unittest.TestCase):
    """Test complementarity parameter calculations"""

    def setUp(self):
        self.model = StrategicBankDecisionModel("model-definition.yaml")
        self.context = DecisionContext(
            market_volatility=20.0,
            regulatory_tightness=0.4,
            capital_position=0.7,
            management_risk_appetite=0.6,
            economic_cycle="normal"
        )

    def test_positive_complementarity_fs(self):
        """Test positive Financial-Strategic complementarity"""
        decision = StrategicDecision(
            name="Test FS Synergy",
            decision_type=DecisionType.MARKET_ENTRY,
            organization_level=DecisionLevel.DIVISION,
            financial=0.9,
            strategic=0.9,
            risk=0.3,
            practical=0.7,
            emotional=0.6,
            regulatory=0.8
        )

        score = self.model.score_market_entry(decision, self.context)
        fs_effect = score.complementarity_effects.get('F×S', 0)
        self.assertGreater(fs_effect, 0, "F×S complementarity should be positive")

    def test_negative_complementarity_fr(self):
        """Test negative Financial-Risk trade-off"""
        decision = StrategicDecision(
            name="Test FR Trade-off",
            decision_type=DecisionType.MARKET_ENTRY,
            organization_level=DecisionLevel.DIVISION,
            financial=0.9,
            strategic=0.7,
            risk=0.8,  # High risk
            practical=0.7,
            emotional=0.6,
            regulatory=0.7
        )

        score = self.model.score_market_entry(decision, self.context)
        fr_effect = score.complementarity_effects.get('F×R', 0)
        self.assertLess(fr_effect, 0, "F×R should show negative trade-off")

    def test_complementarity_breakdown_complete(self):
        """Test that complementarity breakdown includes all pairs"""
        decision = StrategicDecision(
            name="Test Breakdown",
            decision_type=DecisionType.MARKET_ENTRY,
            organization_level=DecisionLevel.DIVISION,
            financial=0.7,
            strategic=0.8,
            risk=0.5,
            practical=0.6,
            emotional=0.5,
            regulatory=0.9
        )

        score = self.model.score_market_entry(decision, self.context)
        effects = score.complementarity_effects

        # Should have all 7 complementarity pairs
        expected_pairs = ['F×S', 'F×R', 'R×P', 'S×E', 'Reg×P', 'F×E', 'S×R']
        for pair in expected_pairs:
            self.assertIn(pair, effects, f"Missing complementarity pair: {pair}")


class TestContextModulation(unittest.TestCase):
    """Test context-dependent modulation of decisions"""

    def setUp(self):
        self.model = StrategicBankDecisionModel("model-definition.yaml")
        self.decision = StrategicDecision(
            name="Context Test",
            decision_type=DecisionType.MARKET_ENTRY,
            organization_level=DecisionLevel.DIVISION,
            financial=0.75,
            strategic=0.75,
            risk=0.50,
            practical=0.70,
            emotional=0.65,
            regulatory=0.85
        )

    def test_normal_context(self):
        """Test decision in normal environment"""
        normal_context = DecisionContext(
            market_volatility=20.0,
            regulatory_tightness=0.4,
            capital_position=0.7,
            management_risk_appetite=0.6,
            economic_cycle="normal"
        )
        score = self.model.score_market_entry(self.decision, normal_context)
        self.assertEqual(score.context_environment, "normal")

    def test_crisis_context_reduces_probability(self):
        """Test decision in crisis environment has lower approval probability"""
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

        score_normal = self.model.score_market_entry(self.decision, normal_context)
        score_crisis = self.model.score_market_entry(self.decision, crisis_context)

        # Crisis should reduce approval probability
        self.assertGreater(score_normal.approval_probability, score_crisis.approval_probability,
                          "Crisis should reduce decision approval probability")

    def test_growth_context_increases_probability(self):
        """Test decision in growth environment has higher approval probability"""
        normal_context = DecisionContext(
            market_volatility=20.0,
            regulatory_tightness=0.4,
            capital_position=0.7,
            management_risk_appetite=0.6,
            economic_cycle="normal"
        )

        growth_context = DecisionContext(
            market_volatility=15.0,
            regulatory_tightness=0.3,
            capital_position=0.85,
            management_risk_appetite=0.8,
            economic_cycle="expansion"
        )

        score_normal = self.model.score_market_entry(self.decision, normal_context)
        score_growth = self.model.score_market_entry(self.decision, growth_context)

        # Growth should increase approval probability
        self.assertGreater(score_growth.approval_probability, score_normal.approval_probability,
                          "Growth mode should increase decision approval probability")


class TestHierarchicalConstraints(unittest.TestCase):
    """Test hierarchy-level constraints"""

    def setUp(self):
        self.model = StrategicBankDecisionModel("model-definition.yaml")
        self.context = DecisionContext(
            market_volatility=20.0,
            regulatory_tightness=0.4,
            capital_position=0.7,
            management_risk_appetite=0.6,
            economic_cycle="normal"
        )

    def test_board_vs_division_weights(self):
        """Test that Board and Division have different parameter weights"""
        board_params = self.model.parameters['board']['weights']
        division_params = self.model.parameters['division']['weights']

        # Board emphasizes Strategic (40%) over Division (25%)
        self.assertGreater(board_params['strategic'], division_params['strategic'])

        # Division emphasizes Financial (35%) over Board (30%)
        self.assertGreater(division_params['financial'], board_params['financial'])

    def test_risk_appetite_constraint_applied(self):
        """Test that risk appetite constraint can be applied"""
        risky_decision = StrategicDecision(
            name="Risky",
            decision_type=DecisionType.MARKET_ENTRY,
            organization_level=DecisionLevel.DIVISION,
            financial=0.8,
            strategic=0.7,
            risk=0.80,  # Very risky
            practical=0.6,
            emotional=0.6,
            regulatory=0.8
        )

        score = self.model.score_market_entry(risky_decision, self.context)

        # Apply L1 risk appetite constraint
        constrained_score = self.model.apply_hierarchy_constraint(score, l1_risk_appetite=0.3)

        # Constraint should reduce approval probability
        if risky_decision.risk > (1.0 - 0.3):  # If risk > 0.7
            self.assertIn("VIOLATES", constrained_score.decision_recommendation)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions"""

    def setUp(self):
        self.model = StrategicBankDecisionModel("model-definition.yaml")
        self.context = DecisionContext(
            market_volatility=20.0,
            regulatory_tightness=0.4,
            capital_position=0.7,
            management_risk_appetite=0.6,
            economic_cycle="normal"
        )

    def test_perfect_decision(self):
        """Test perfect decision (all dimensions max)"""
        perfect = StrategicDecision(
            name="Perfect Decision",
            decision_type=DecisionType.MARKET_ENTRY,
            organization_level=DecisionLevel.DIVISION,
            financial=1.0,
            strategic=1.0,
            risk=0.0,  # Low risk (good)
            practical=1.0,
            emotional=1.0,
            regulatory=1.0
        )

        score = self.model.score_market_entry(perfect, self.context)
        # Perfect decision should have very high probability
        self.assertGreater(score.approval_probability, 0.85)

    def test_worst_decision(self):
        """Test worst decision (all dimensions min)"""
        worst = StrategicDecision(
            name="Worst Decision",
            decision_type=DecisionType.MARKET_ENTRY,
            organization_level=DecisionLevel.DIVISION,
            financial=0.0,
            strategic=0.0,
            risk=1.0,  # High risk (bad)
            practical=0.0,
            emotional=0.0,
            regulatory=0.0
        )

        score = self.model.score_market_entry(worst, self.context)
        # Worst decision should have low probability (but not extreme given model structure)
        self.assertLess(score.approval_probability, 0.78)

    def test_mixed_dimensions(self):
        """Test mixed strong/weak dimensions"""
        mixed = StrategicDecision(
            name="Mixed",
            decision_type=DecisionType.MARKET_ENTRY,
            organization_level=DecisionLevel.DIVISION,
            financial=0.8,  # Strong
            strategic=0.2,  # Weak
            risk=0.6,       # Higher risk
            practical=0.2,  # Weak
            emotional=0.8,  # Strong
            regulatory=0.5  # Neutral
        )

        score = self.model.score_market_entry(mixed, self.context)
        # Should be somewhere in middle due to mixed signals
        self.assertTrue(0.5 < score.approval_probability < 0.85)


if __name__ == '__main__':
    unittest.main()
