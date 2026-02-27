"""
Test Suite for PSF 2.0: Papal Succession Framework
Validates model implementation against historical data and mathematical properties
"""

import unittest
import numpy as np
from psf_model import (
    PapalSuccessionFramework,
    CandidateParameters,
    ModelResults
)


class TestModelInitialization(unittest.TestCase):
    """Test model loading and initialization"""

    def setUp(self):
        self.model = PapalSuccessionFramework("model-definition.yaml")

    def test_config_loaded(self):
        """Verify configuration file loaded correctly"""
        self.assertIsNotNone(self.model.config)
        self.assertEqual(self.model.config['metadata']['version'], "1.0.0")

    def test_beta_parameters_extracted(self):
        """Verify beta parameters extracted correctly"""
        self.assertEqual(self.model.beta_params['intercept'], -4.0)
        self.assertEqual(self.model.beta_params['lambda'], 2.5)
        self.assertEqual(self.model.beta_params['iota'], 1.8)
        self.assertEqual(self.model.beta_params['pi'], 1.5)
        self.assertEqual(self.model.beta_params['nu'], 0.8)
        self.assertEqual(self.model.beta_params['alpha'], 0.5)

    def test_dimensions_extracted(self):
        """Verify dimensions extracted correctly"""
        self.assertIn('Λ', self.model.dimensions)
        self.assertIn('Ι', self.model.dimensions)
        self.assertIn('Π', self.model.dimensions)
        self.assertIn('Ν', self.model.dimensions)
        self.assertIn('Α', self.model.dimensions)


class TestLogisticFunction(unittest.TestCase):
    """Test logistic regression calculation"""

    def setUp(self):
        self.model = PapalSuccessionFramework("model-definition.yaml")

    def test_probability_bounds(self):
        """Verify probabilities are always in [0, 1]"""
        # Test extreme values
        extreme_low = CandidateParameters(
            name="Extreme Low",
            lambda_=0.0, iota=0.0, pi=0.0, nu=0.0, alpha=0.0
        )
        extreme_high = CandidateParameters(
            name="Extreme High",
            lambda_=1.0, iota=1.0, pi=1.0, nu=1.0, alpha=1.0
        )

        prob_low = self.model.calculate_individual_probability(extreme_low)
        prob_high = self.model.calculate_individual_probability(extreme_high)

        self.assertGreaterEqual(prob_low, 0.0)
        self.assertLessEqual(prob_low, 1.0)
        self.assertGreaterEqual(prob_high, 0.0)
        self.assertLessEqual(prob_high, 1.0)

    def test_probability_monotonicity(self):
        """Verify probability increases with increasing scores"""
        # Base candidate
        base = CandidateParameters(
            name="Base",
            lambda_=0.5, iota=0.5, pi=0.5, nu=0.5, alpha=0.5
        )
        base_prob = self.model.calculate_individual_probability(base)

        # Higher lambda
        higher_lambda = CandidateParameters(
            name="Higher Lambda",
            lambda_=0.7, iota=0.5, pi=0.5, nu=0.5, alpha=0.5
        )
        higher_lambda_prob = self.model.calculate_individual_probability(higher_lambda)

        self.assertGreater(higher_lambda_prob, base_prob,
                          "Increasing network centrality should increase probability")

    def test_leo_xiv_calculation(self):
        """Verify known candidate (Leo XIV) produces correct probability"""
        # Leo XIV (Robert Francis Prevost) from 2025 conclave
        leo_xiv = CandidateParameters(
            name="Robert Francis Prevost (Leo XIV)",
            lambda_=0.85,
            iota=0.92,
            pi=0.95,
            nu=0.80,
            alpha=0.93
        )

        prob = self.model.calculate_individual_probability(leo_xiv)
        expected_prob = 0.91  # From model definition

        # Allow 5% tolerance due to rounding
        self.assertAlmostEqual(prob, expected_prob, delta=0.05,
                              msg=f"Leo XIV probability should be ~{expected_prob}, got {prob}")


class TestDimensionContributions(unittest.TestCase):
    """Test dimension contribution analysis"""

    def setUp(self):
        self.model = PapalSuccessionFramework("model-definition.yaml")

    def test_contributions_calculated(self):
        """Verify contributions are calculated for all dimensions"""
        candidate = CandidateParameters(
            name="Test",
            lambda_=0.8, iota=0.7, pi=0.6, nu=0.5, alpha=0.4
        )

        contributions = self.model.get_dimension_contributions(candidate)

        self.assertIn('intercept', contributions)
        self.assertIn('lambda', contributions)
        self.assertIn('iota', contributions)
        self.assertIn('pi', contributions)
        self.assertIn('nu', contributions)
        self.assertIn('alpha', contributions)

    def test_contributions_proportional_to_scores(self):
        """Verify contributions scale with dimension scores"""
        candidate1 = CandidateParameters(
            name="Test1", lambda_=0.5, iota=0.5, pi=0.5, nu=0.5, alpha=0.5
        )
        candidate2 = CandidateParameters(
            name="Test2", lambda_=1.0, iota=0.5, pi=0.5, nu=0.5, alpha=0.5
        )

        contrib1 = self.model.get_dimension_contributions(candidate1)
        contrib2 = self.model.get_dimension_contributions(candidate2)

        # Lambda contribution should be doubled when lambda doubled
        ratio = contrib2['lambda'] / (contrib1['lambda'] + 1e-6)
        self.assertAlmostEqual(ratio, 2.0, places=5)


class TestConclaveEvaluation(unittest.TestCase):
    """Test multi-candidate conclave evaluation"""

    def setUp(self):
        self.model = PapalSuccessionFramework("model-definition.yaml")

    def test_normalization_sums_to_one(self):
        """Verify competitive probabilities sum to 1.0"""
        candidates = [
            CandidateParameters(
                name="Candidate A", lambda_=0.8, iota=0.7, pi=0.6, nu=0.5, alpha=0.4
            ),
            CandidateParameters(
                name="Candidate B", lambda_=0.7, iota=0.8, pi=0.7, nu=0.6, alpha=0.5
            ),
            CandidateParameters(
                name="Candidate C", lambda_=0.6, iota=0.6, pi=0.8, nu=0.7, alpha=0.6
            ),
        ]

        results = self.model.evaluate_conclave(candidates)
        total_prob = sum(r.competitive_probability for r in results)

        self.assertAlmostEqual(total_prob, 1.0, places=10,
                              msg="Competitive probabilities should sum to 1.0")

    def test_ranking_order(self):
        """Verify candidates ranked correctly by probability"""
        candidates = [
            CandidateParameters(
                name="High", lambda_=0.9, iota=0.9, pi=0.9, nu=0.9, alpha=0.9
            ),
            CandidateParameters(
                name="Medium", lambda_=0.5, iota=0.5, pi=0.5, nu=0.5, alpha=0.5
            ),
            CandidateParameters(
                name="Low", lambda_=0.1, iota=0.1, pi=0.1, nu=0.1, alpha=0.1
            ),
        ]

        results = self.model.evaluate_conclave(candidates)

        self.assertEqual(results[0].candidate_name, "High")
        self.assertEqual(results[1].candidate_name, "Medium")
        self.assertEqual(results[2].candidate_name, "Low")


class TestHistoricalValidation(unittest.TestCase):
    """Test model validation against historical data"""

    def setUp(self):
        self.model = PapalSuccessionFramework("model-definition.yaml")

    def test_validation_returns_metrics(self):
        """Verify validation returns complete metrics"""
        validation = self.model.validate_against_historical_data()

        self.assertIn('total_conclaves', validation)
        self.assertIn('correct_predictions', validation)
        self.assertIn('accuracy', validation)
        self.assertIn('average_duration_error', validation)
        self.assertIn('results_per_conclave', validation)

    def test_historical_accuracy(self):
        """Verify model achieves documented accuracy on historical data"""
        validation = self.model.validate_against_historical_data()

        # Model should achieve at least 87% accuracy (7/8 or better)
        self.assertGreaterEqual(validation['accuracy'], 0.87,
                               msg="Model should achieve ≥87% accuracy on historical data")

    def test_conclave_predictions_correct(self):
        """Verify all 7 papal conclaves predicted correctly"""
        validation = self.model.validate_against_historical_data()

        # All 7 known conclaves should be predicted correctly
        for result in validation['results_per_conclave']:
            self.assertTrue(result['prediction_correct'],
                           msg=f"Failed to correctly predict {result['year']} "
                               f"conclave winner ({result['winner']})")

    def test_duration_estimates_reasonable(self):
        """Verify duration estimates are within reasonable bounds"""
        validation = self.model.validate_against_historical_data()

        # Average error should be small (within 1 round)
        self.assertLess(validation['average_duration_error'], 1.0,
                       msg="Average duration error should be < 1 round")


class TestSensitivityAnalysis(unittest.TestCase):
    """Test parameter sensitivity analysis"""

    def setUp(self):
        self.model = PapalSuccessionFramework("model-definition.yaml")

    def test_sensitivity_calculated(self):
        """Verify sensitivity analysis produces output for all dimensions"""
        candidate = CandidateParameters(
            name="Test", lambda_=0.5, iota=0.5, pi=0.5, nu=0.5, alpha=0.5
        )

        sensitivity = self.model.sensitivity_analysis(candidate)

        self.assertIn('lambda_', sensitivity)
        self.assertIn('iota', sensitivity)
        self.assertIn('pi', sensitivity)
        self.assertIn('nu', sensitivity)
        self.assertIn('alpha', sensitivity)

    def test_network_centrality_most_sensitive(self):
        """Verify network centrality has highest sensitivity"""
        candidate = CandidateParameters(
            name="Test", lambda_=0.5, iota=0.5, pi=0.5, nu=0.5, alpha=0.5
        )

        sensitivity = self.model.sensitivity_analysis(candidate)

        sensitivities = {k: v['sensitivity'] for k, v in sensitivity.items()}

        # Lambda should have highest sensitivity (coefficient 2.5)
        lambda_sens = sensitivities['lambda_']
        iota_sens = sensitivities['iota']
        alpha_sens = sensitivities['alpha']

        self.assertGreater(lambda_sens, iota_sens,
                          msg="Network centrality should be more sensitive than integration")
        self.assertGreater(lambda_sens, alpha_sens,
                          msg="Network centrality should be more sensitive than authenticity")


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions"""

    def setUp(self):
        self.model = PapalSuccessionFramework("model-definition.yaml")

    def test_single_candidate_conclave(self):
        """Test conclave with only one candidate"""
        candidates = [
            CandidateParameters(
                name="Only Candidate", lambda_=0.5, iota=0.5, pi=0.5, nu=0.5, alpha=0.5
            )
        ]

        results = self.model.evaluate_conclave(candidates)

        self.assertEqual(len(results), 1)
        self.assertAlmostEqual(results[0].competitive_probability, 1.0, places=10)

    def test_identical_candidates(self):
        """Test conclave with identical candidates"""
        candidates = [
            CandidateParameters(
                name="Candidate A", lambda_=0.5, iota=0.5, pi=0.5, nu=0.5, alpha=0.5
            ),
            CandidateParameters(
                name="Candidate B", lambda_=0.5, iota=0.5, pi=0.5, nu=0.5, alpha=0.5
            ),
        ]

        results = self.model.evaluate_conclave(candidates)

        # Should have equal competitive probabilities
        self.assertAlmostEqual(results[0].competitive_probability,
                              results[1].competitive_probability, places=10)
        self.assertAlmostEqual(results[0].competitive_probability, 0.5, places=10)


class TestConclaveDurationEstimate(unittest.TestCase):
    """Test conclave duration prediction"""

    def setUp(self):
        self.model = PapalSuccessionFramework("model-definition.yaml")

    def test_duration_high_network_high_predecessor(self):
        """Verify high network + high predecessor = short conclave"""
        # Benedict XVI: Λ=0.95, Π=0.92 → 2 rounds (fastest)
        candidate = CandidateParameters(
            name="High Network High Pred",
            lambda_=0.95, iota=0.5, pi=0.92, nu=0.5, alpha=0.5
        )

        duration = self.model._estimate_conclave_duration(candidate)

        # Should predict short conclave (2-3 rounds)
        self.assertLessEqual(duration, 3,
                            msg="High network + high predecessor should predict short conclave")

    def test_duration_low_network_low_predecessor(self):
        """Verify low network + low predecessor = long conclave"""
        candidate = CandidateParameters(
            name="Low Network Low Pred",
            lambda_=0.3, iota=0.5, pi=0.2, nu=0.5, alpha=0.5
        )

        duration = self.model._estimate_conclave_duration(candidate)

        # Should predict longer conclave (5-10 rounds)
        self.assertGreaterEqual(duration, 5,
                               msg="Low network + low predecessor should predict longer conclave")


class TestIntegration(unittest.TestCase):
    """Integration tests combining multiple components"""

    def setUp(self):
        self.model = PapalSuccessionFramework("model-definition.yaml")

    def test_full_workflow(self):
        """Test complete workflow: validate + evaluate + export"""
        # 1. Validate against historical data
        validation = self.model.validate_against_historical_data()
        self.assertGreater(validation['accuracy'], 0.8)

        # 2. Evaluate hypothetical conclave
        candidates = [
            CandidateParameters(
                name="Cardinal Alpha", lambda_=0.8, iota=0.7, pi=0.6, nu=0.7, alpha=0.8
            ),
            CandidateParameters(
                name="Cardinal Beta", lambda_=0.7, iota=0.8, pi=0.7, nu=0.8, alpha=0.9
            ),
        ]
        results = self.model.evaluate_conclave(candidates)

        # 3. Verify results structure
        self.assertEqual(len(results), 2)
        total_prob = sum(r.competitive_probability for r in results)
        self.assertAlmostEqual(total_prob, 1.0, places=10)

        # 4. Export results
        self.model.export_results(results, "/tmp/test_results.json")

    def test_model_summary_generation(self):
        """Test that model summary can be generated without errors"""
        summary = self.model.get_model_summary()

        self.assertIn("PSF 2.0", summary)
        self.assertIn("Network Centrality", summary)
        self.assertIn("Integration Capacity", summary)
        self.assertIn("87%", summary)


def run_test_suite():
    """Run complete test suite and report results"""
    print("\n" + "=" * 80)
    print("PSF 2.0 TEST SUITE")
    print("=" * 80 + "\n")

    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestModelInitialization))
    suite.addTests(loader.loadTestsFromTestCase(TestLogisticFunction))
    suite.addTests(loader.loadTestsFromTestCase(TestDimensionContributions))
    suite.addTests(loader.loadTestsFromTestCase(TestConclaveEvaluation))
    suite.addTests(loader.loadTestsFromTestCase(TestHistoricalValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestSensitivityAnalysis))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestConclaveDurationEstimate))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("=" * 80 + "\n")

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_test_suite()
    exit(0 if success else 1)
