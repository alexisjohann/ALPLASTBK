"""
Test Suite for CSF 2.0: China Succession Framework
Validates model implementation for CCP leadership succession prediction
"""

import unittest
import numpy as np
import sys
from pathlib import Path

# Handle dashed directory names in import
import importlib.util
spec = importlib.util.spec_from_file_location(
    "csf_model",
    Path(__file__).parent / "csf_model.py"
)
csf_model_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(csf_model_module)

CandidateProfile = csf_model_module.CandidateProfile
ChinaSuccessionFramework = csf_model_module.ChinaSuccessionFramework
SuccessionResults = csf_model_module.SuccessionResults


class TestModelInitialization(unittest.TestCase):
    """Test model loading and initialization"""

    def setUp(self):
        self.model = ChinaSuccessionFramework("model-definition.yaml")

    def test_model_id_loaded(self):
        """Verify model ID loaded correctly"""
        self.assertEqual(self.model.model_id, "CSF-2.0")

    def test_status_loaded(self):
        """Verify model status loaded correctly"""
        self.assertEqual(self.model.status, "BETA")

    def test_dimensions_extracted(self):
        """Verify all 5 dimensions extracted correctly"""
        expected_symbols = {'C_Fraktion', 'C_Legitimität', 'C_Seniority', 'C_Kompetenz_Tech', 'C_IntlBez'}
        actual_symbols = set(self.model.dimensions.keys())
        self.assertEqual(actual_symbols, expected_symbols)

    def test_dimension_weights_sum_to_one(self):
        """Verify dimension weights sum to 1.0"""
        total_weight = sum(self.model.weights.values())
        self.assertAlmostEqual(total_weight, 1.0, places=5,
                              msg=f"Weights sum to {total_weight}, expected ~1.0")

    def test_dimension_weights_correct(self):
        """Verify individual dimension weights"""
        self.assertAlmostEqual(self.model.weights['C_Fraktion'], 0.35, places=2)
        self.assertAlmostEqual(self.model.weights['C_Legitimität'], 0.25, places=2)
        self.assertAlmostEqual(self.model.weights['C_Seniority'], 0.20, places=2)
        self.assertAlmostEqual(self.model.weights['C_Kompetenz_Tech'], 0.12, places=2)
        self.assertAlmostEqual(self.model.weights['C_IntlBez'], 0.08, places=2)

    def test_gamma_matrix_loaded(self):
        """Verify complementarity matrix loaded"""
        self.assertGreater(len(self.model.gamma_matrix), 0,
                          msg="Gamma matrix should contain complementarity parameters")


class TestLogisticProbabilityCalculation(unittest.TestCase):
    """Test logistic regression probability calculation"""

    def setUp(self):
        self.model = ChinaSuccessionFramework("model-definition.yaml")

    def test_probability_bounds(self):
        """Verify probabilities are always in [0, 1]"""
        # Test extreme values
        extreme_low = CandidateProfile(
            name="Extreme Low",
            age=55,
            c_fraktion=0.0, c_legitimitat=0.0, c_seniority=0.0,
            c_kompetenz=0.0, c_intl=0.0
        )
        extreme_high = CandidateProfile(
            name="Extreme High",
            age=55,
            c_fraktion=1.0, c_legitimitat=1.0, c_seniority=1.0,
            c_kompetenz=1.0, c_intl=1.0
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
        base = CandidateProfile(
            name="Base",
            age=55,
            c_fraktion=0.5, c_legitimitat=0.5, c_seniority=0.5,
            c_kompetenz=0.5, c_intl=0.5
        )
        base_prob = self.model.calculate_individual_probability(base)

        # Higher fraktion (most important dimension)
        higher_fraktion = CandidateProfile(
            name="Higher Fraktion",
            age=55,
            c_fraktion=0.8, c_legitimitat=0.5, c_seniority=0.5,
            c_kompetenz=0.5, c_intl=0.5
        )
        higher_fraktion_prob = self.model.calculate_individual_probability(higher_fraktion)

        self.assertGreater(higher_fraktion_prob, base_prob,
                          "Increasing factional alignment should increase probability")

    def test_li_qiang_calculation(self):
        """Verify known candidate (Li Qiang) produces reasonable probability"""
        # Li Qiang - Xi's chosen successor
        li_qiang = CandidateProfile(
            name="Li Qiang",
            age=63,
            c_fraktion=0.80,
            c_legitimitat=0.85,
            c_seniority=0.78,
            c_kompetenz=0.65,
            c_intl=0.30
        )

        prob = self.model.calculate_individual_probability(li_qiang)

        # Li Qiang should have relatively high probability
        self.assertGreater(prob, 0.3,
                          "Li Qiang should have notable probability (>30%)")
        self.assertLess(prob, 1.0,
                       "Probability should be less than 100%")

    def test_probability_scale_with_dimensions(self):
        """Verify probability scales appropriately with each dimension"""
        base = CandidateProfile(
            name="Base", age=55,
            c_fraktion=0.5, c_legitimitat=0.5, c_seniority=0.5,
            c_kompetenz=0.5, c_intl=0.5
        )
        base_prob = self.model.calculate_individual_probability(base)

        # Test each dimension independently
        for dim_name, dim_attr in [
            ("fraktion", "c_fraktion"),
            ("legitimitat", "c_legitimitat"),
            ("seniority", "c_seniority"),
        ]:
            improved = CandidateProfile(
                name=f"High {dim_name}", age=55,
                c_fraktion=0.5, c_legitimitat=0.5, c_seniority=0.5,
                c_kompetenz=0.5, c_intl=0.5
            )
            setattr(improved, dim_attr, 0.8)

            improved_prob = self.model.calculate_individual_probability(improved)
            self.assertGreater(improved_prob, base_prob,
                             f"Increasing {dim_name} should increase probability")


class TestCandidateProfileDataclass(unittest.TestCase):
    """Test CandidateProfile dataclass"""

    def test_profile_creation(self):
        """Verify candidate profile can be created"""
        profile = CandidateProfile(
            name="Test Candidate",
            age=60,
            c_fraktion=0.7,
            c_legitimitat=0.8,
            c_seniority=0.75,
            c_kompetenz=0.6,
            c_intl=0.4
        )

        self.assertEqual(profile.name, "Test Candidate")
        self.assertEqual(profile.age, 60)

    def test_profile_to_dict(self):
        """Verify profile can be converted to dictionary"""
        profile = CandidateProfile(
            name="Test",
            age=60,
            c_fraktion=0.7,
            c_legitimitat=0.8,
            c_seniority=0.75,
            c_kompetenz=0.6,
            c_intl=0.4
        )

        profile_dict = profile.to_dict()

        self.assertIn('c_fraktion', profile_dict)
        self.assertIn('c_legitimitat', profile_dict)
        self.assertAlmostEqual(profile_dict['c_fraktion'], 0.7)


class TestConclaveEvaluation(unittest.TestCase):
    """Test multi-candidate conclave evaluation"""

    def setUp(self):
        self.model = ChinaSuccessionFramework("model-definition.yaml")

    def test_normalization_sums_to_one(self):
        """Verify competitive probabilities sum to 1.0"""
        candidates = [
            CandidateProfile(
                name="Candidate A", age=63,
                c_fraktion=0.80, c_legitimitat=0.85, c_seniority=0.78,
                c_kompetenz=0.65, c_intl=0.30
            ),
            CandidateProfile(
                name="Candidate B", age=60,
                c_fraktion=0.85, c_legitimitat=0.75, c_seniority=0.70,
                c_kompetenz=0.70, c_intl=0.35
            ),
            CandidateProfile(
                name="Candidate C", age=58,
                c_fraktion=0.60, c_legitimitat=0.80, c_seniority=0.72,
                c_kompetenz=0.75, c_intl=0.25
            ),
        ]

        results = self.model.evaluate_conclave(candidates)
        total_prob = sum(r.competitive_probability for r in results)

        self.assertAlmostEqual(total_prob, 1.0, places=10,
                              msg="Competitive probabilities should sum to 1.0")

    def test_ranking_order_by_probability(self):
        """Verify candidates ranked correctly by probability"""
        candidates = [
            CandidateProfile(
                name="Strong", age=60,
                c_fraktion=0.9, c_legitimitat=0.9, c_seniority=0.9,
                c_kompetenz=0.9, c_intl=0.8
            ),
            CandidateProfile(
                name="Medium", age=60,
                c_fraktion=0.5, c_legitimitat=0.5, c_seniority=0.5,
                c_kompetenz=0.5, c_intl=0.5
            ),
            CandidateProfile(
                name="Weak", age=60,
                c_fraktion=0.2, c_legitimitat=0.2, c_seniority=0.3,
                c_kompetenz=0.2, c_intl=0.1
            ),
        ]

        results = self.model.evaluate_conclave(candidates)

        self.assertEqual(results[0].candidate_name, "Strong")
        self.assertEqual(results[1].candidate_name, "Medium")
        self.assertEqual(results[2].candidate_name, "Weak")
        self.assertEqual(results[0].ranking, 1)
        self.assertEqual(results[1].ranking, 2)
        self.assertEqual(results[2].ranking, 3)

    def test_results_dataclass_structure(self):
        """Verify SuccessionResults has all required fields"""
        candidates = [
            CandidateProfile(
                name="Test", age=60,
                c_fraktion=0.6, c_legitimitat=0.7, c_seniority=0.65,
                c_kompetenz=0.6, c_intl=0.3
            )
        ]

        results = self.model.evaluate_conclave(candidates)

        self.assertEqual(len(results), 1)
        result = results[0]

        self.assertIsNotNone(result.candidate_name)
        self.assertIsNotNone(result.individual_probability)
        self.assertIsNotNone(result.consensus_probability)
        self.assertIsNotNone(result.competitive_probability)
        self.assertIsNotNone(result.dimension_scores)
        self.assertIsNotNone(result.contribution_by_dimension)
        self.assertIsNotNone(result.ranking)
        self.assertIsNotNone(result.pbsc_advancement_estimate)
        self.assertIsNotNone(result.generalsekretaer_readiness)

    def test_single_candidate_conclave(self):
        """Test conclave with only one candidate"""
        candidates = [
            CandidateProfile(
                name="Only Candidate", age=60,
                c_fraktion=0.5, c_legitimitat=0.5, c_seniority=0.5,
                c_kompetenz=0.5, c_intl=0.5
            )
        ]

        results = self.model.evaluate_conclave(candidates)

        self.assertEqual(len(results), 1)
        self.assertAlmostEqual(results[0].competitive_probability, 1.0, places=10)


class TestFactionalConsensusCalculation(unittest.TestCase):
    """Test factional consensus probability calculation"""

    def setUp(self):
        self.model = ChinaSuccessionFramework("model-definition.yaml")

    def test_high_fraktion_high_consensus(self):
        """Verify ultra-aligned candidate has high consensus chance"""
        ultra_aligned = CandidateProfile(
            name="Ultra-Aligned",
            age=60,
            c_fraktion=0.90,
            c_legitimitat=0.8,
            c_seniority=0.7,
            c_kompetenz=0.6,
            c_intl=0.3
        )

        consensus_prob = self.model.factional_consensus_probability(ultra_aligned)

        self.assertGreater(consensus_prob, 0.7,
                          "Ultra-aligned candidate should have high consensus (>70%)")

    def test_weak_fraktion_low_consensus(self):
        """Verify weakly-aligned candidate has low consensus chance"""
        weak_aligned = CandidateProfile(
            name="Weak-Aligned",
            age=60,
            c_fraktion=0.30,
            c_legitimitat=0.8,
            c_seniority=0.7,
            c_kompetenz=0.6,
            c_intl=0.3
        )

        consensus_prob = self.model.factional_consensus_probability(weak_aligned)

        self.assertLess(consensus_prob, 0.3,
                       "Weakly-aligned candidate should have low consensus (<30%)")

    def test_consensus_bounds(self):
        """Verify consensus probability is in [0, 1]"""
        candidates = [
            CandidateProfile("Low", 55, 0.1, 0.5, 0.5, 0.5, 0.3),
            CandidateProfile("Mid", 60, 0.5, 0.5, 0.5, 0.5, 0.3),
            CandidateProfile("High", 65, 0.95, 0.8, 0.8, 0.7, 0.4),
        ]

        for candidate in candidates:
            consensus = self.model.factional_consensus_probability(candidate)
            self.assertGreaterEqual(consensus, 0.0)
            self.assertLessEqual(consensus, 1.0)


class TestComplementarityEffects(unittest.TestCase):
    """Test complementarity (γ) parameter calculations"""

    def setUp(self):
        self.model = ChinaSuccessionFramework("model-definition.yaml")

    def test_complementarity_effects_calculated(self):
        """Verify complementarity effects are calculated"""
        candidate = CandidateProfile(
            name="Test",
            age=60,
            c_fraktion=0.7,
            c_legitimitat=0.8,
            c_seniority=0.75,
            c_kompetenz=0.6,
            c_intl=0.4
        )

        effects = self.model.apply_complementarity_effects(candidate)

        self.assertIsNotNone(effects)
        self.assertGreater(len(effects), 0,
                          "Complementarity effects should be calculated")

    def test_fraktion_legitimitat_synergy(self):
        """Verify fraktion-legitimität complementarity is positive"""
        high_both = CandidateProfile(
            name="High Both",
            age=60,
            c_fraktion=0.9,
            c_legitimitat=0.9,
            c_seniority=0.5,
            c_kompetenz=0.5,
            c_intl=0.3
        )

        effects = self.model.apply_complementarity_effects(high_both)

        self.assertIn('gamma_fraktion_legitimitat', effects)
        self.assertGreater(effects['gamma_fraktion_legitimitat'], 0.5,
                          "High fraktion + legitimität should show strong synergy")

    def test_low_complementarity(self):
        """Verify complementarity effects are lower for weak candidates"""
        weak = CandidateProfile(
            name="Weak",
            age=60,
            c_fraktion=0.2,
            c_legitimitat=0.2,
            c_seniority=0.3,
            c_kompetenz=0.2,
            c_intl=0.1
        )

        strong = CandidateProfile(
            name="Strong",
            age=60,
            c_fraktion=0.8,
            c_legitimitat=0.8,
            c_seniority=0.8,
            c_kompetenz=0.7,
            c_intl=0.5
        )

        effects_weak = self.model.apply_complementarity_effects(weak)
        effects_strong = self.model.apply_complementarity_effects(strong)

        weak_synergy = effects_weak['gamma_fraktion_legitimitat']
        strong_synergy = effects_strong['gamma_fraktion_legitimitat']

        self.assertLess(weak_synergy, strong_synergy,
                       "Strong candidates should show more synergy than weak candidates")


class TestSuccessionTimeline(unittest.TestCase):
    """Test succession timeline estimation"""

    def setUp(self):
        self.model = ChinaSuccessionFramework("model-definition.yaml")

    def test_young_candidate_long_timeline(self):
        """Verify young candidates have long timelines"""
        young = CandidateProfile(
            name="Young", age=45,
            c_fraktion=0.7, c_legitimitat=0.7, c_seniority=0.4,
            c_kompetenz=0.7, c_intl=0.3
        )

        timeline, years = self.model.estimate_succession_timeline(young)

        self.assertGreaterEqual(years, 7,
                          "Young candidate should need 7+ years to reach General Secretary")

    def test_mid_career_moderate_timeline(self):
        """Verify mid-career candidates have moderate timelines"""
        mid = CandidateProfile(
            name="Mid", age=55,
            c_fraktion=0.7, c_legitimitat=0.7, c_seniority=0.65,
            c_kompetenz=0.7, c_intl=0.3
        )

        timeline, years = self.model.estimate_succession_timeline(mid)

        self.assertGreaterEqual(years, 3)
        self.assertLess(years, 12,
                       "Mid-career should be 3-12 years")

    def test_senior_candidate_short_timeline(self):
        """Verify senior candidates have short timelines"""
        senior = CandidateProfile(
            name="Senior", age=65,
            c_fraktion=0.8, c_legitimitat=0.8, c_seniority=0.85,
            c_kompetenz=0.7, c_intl=0.4
        )

        timeline, years = self.model.estimate_succession_timeline(senior)

        self.assertLess(years, 5,
                       "Senior candidate ready for succession (0-3 years)")


class TestGeneralSekretaerReadiness(unittest.TestCase):
    """Test General Secretary readiness assessment"""

    def setUp(self):
        self.model = ChinaSuccessionFramework("model-definition.yaml")

    def test_readiness_age_classification(self):
        """Verify readiness classification based on age"""
        candidates = [
            (40, "Too Young"),
            (52, "Preparing"),
            (62, "Ready"),
            (72, "Too Old"),
        ]

        for age, expected_readiness_type in candidates:
            candidate = CandidateProfile(
                name=f"Age {age}",
                age=age,
                c_fraktion=0.7,
                c_legitimitat=0.7,
                c_seniority=0.5 + (age - 40) * 0.01,
                c_kompetenz=0.7,
                c_intl=0.3
            )

            results = self.model.evaluate_conclave([candidate])
            readiness = results[0].generalsekretaer_readiness

            self.assertIn(expected_readiness_type, readiness,
                         f"Age {age} should have readiness containing '{expected_readiness_type}'")


class TestDimensionContributions(unittest.TestCase):
    """Test dimension contribution analysis"""

    def setUp(self):
        self.model = ChinaSuccessionFramework("model-definition.yaml")

    def test_contributions_calculated_for_all_dimensions(self):
        """Verify contributions calculated for all dimensions"""
        candidate = CandidateProfile(
            name="Test",
            age=60,
            c_fraktion=0.8,
            c_legitimitat=0.7,
            c_seniority=0.6,
            c_kompetenz=0.5,
            c_intl=0.4
        )

        contributions = self.model._calculate_dimension_contributions(candidate)

        self.assertIn('C_Fraktion', contributions)
        self.assertIn('C_Legitimität', contributions)
        self.assertIn('C_Seniority', contributions)
        self.assertIn('C_Kompetenz_Tech', contributions)
        self.assertIn('C_IntlBez', contributions)

    def test_fraktion_has_highest_weight(self):
        """Verify fraktion dimension has highest contribution due to weight"""
        candidate = CandidateProfile(
            name="Equal Scores",
            age=60,
            c_fraktion=0.5,
            c_legitimitat=0.5,
            c_seniority=0.5,
            c_kompetenz=0.5,
            c_intl=0.5
        )

        contrib = self.model._calculate_dimension_contributions(candidate)

        fraktion_contrib = contrib['C_Fraktion']
        intl_contrib = contrib['C_IntlBez']

        self.assertGreater(fraktion_contrib, intl_contrib,
                          "Fraktion should contribute more than international (35% > 8%)")


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions"""

    def setUp(self):
        self.model = ChinaSuccessionFramework("model-definition.yaml")

    def test_all_zeros_profile(self):
        """Test candidate with all dimension scores at zero"""
        profile = CandidateProfile(
            name="No Qualifications",
            age=55,
            c_fraktion=0.0,
            c_legitimitat=0.0,
            c_seniority=0.0,
            c_kompetenz=0.0,
            c_intl=0.0
        )

        prob = self.model.calculate_individual_probability(profile)

        self.assertGreaterEqual(prob, 0.0)
        self.assertLessEqual(prob, 1.0)
        self.assertLess(prob, 0.05,
                       "Profile with all zeros should have very low probability")

    def test_all_ones_profile(self):
        """Test candidate with all dimension scores at maximum"""
        profile = CandidateProfile(
            name="Perfect Candidate",
            age=55,
            c_fraktion=1.0,
            c_legitimitat=1.0,
            c_seniority=1.0,
            c_kompetenz=1.0,
            c_intl=1.0
        )

        prob = self.model.calculate_individual_probability(profile)

        self.assertGreaterEqual(prob, 0.0)
        self.assertLessEqual(prob, 1.0)
        self.assertGreater(prob, 0.8,
                          "Profile with all ones should have very high probability")

    def test_identical_candidates(self):
        """Test conclave with identical candidates"""
        identical_candidate_spec = {
            'age': 60,
            'c_fraktion': 0.6,
            'c_legitimitat': 0.7,
            'c_seniority': 0.65,
            'c_kompetenz': 0.6,
            'c_intl': 0.3
        }

        candidates = [
            CandidateProfile(name="Candidate A", **identical_candidate_spec),
            CandidateProfile(name="Candidate B", **identical_candidate_spec),
            CandidateProfile(name="Candidate C", **identical_candidate_spec),
        ]

        results = self.model.evaluate_conclave(candidates)

        # Each should have ~33% chance
        for result in results:
            self.assertAlmostEqual(result.competitive_probability, 1.0/3, places=3,
                                  msg=f"{result.candidate_name} should have ~33.3% probability")

    def test_extreme_age_candidates(self):
        """Test candidates at age extremes"""
        very_young = CandidateProfile(
            name="Very Young", age=35,
            c_fraktion=0.8, c_legitimitat=0.8, c_seniority=0.3,
            c_kompetenz=0.8, c_intl=0.7
        )

        very_old = CandidateProfile(
            name="Very Old", age=80,
            c_fraktion=0.8, c_legitimitat=0.8, c_seniority=0.95,
            c_kompetenz=0.6, c_intl=0.4
        )

        prob_young = self.model.calculate_individual_probability(very_young)
        prob_old = self.model.calculate_individual_probability(very_old)

        self.assertGreaterEqual(prob_young, 0.0)
        self.assertLessEqual(prob_young, 1.0)
        self.assertGreaterEqual(prob_old, 0.0)
        self.assertLessEqual(prob_old, 1.0)


class TestModelSummary(unittest.TestCase):
    """Test model summary output"""

    def setUp(self):
        self.model = ChinaSuccessionFramework("model-definition.yaml")

    def test_get_model_summary(self):
        """Verify model summary can be generated"""
        summary = self.model.get_model_summary()

        self.assertIsNotNone(summary)
        self.assertIn("China Succession Framework", summary)
        self.assertIn("CSF", summary)
        self.assertIn("Fraktion", summary)
        self.assertIn("PBSC", summary)


class TestKnownCandidates(unittest.TestCase):
    """Test with known real-world candidates"""

    def setUp(self):
        self.model = ChinaSuccessionFramework("model-definition.yaml")

    def test_li_qiang_vs_others(self):
        """Verify Li Qiang ranks highest among current PBSC"""
        li_qiang = CandidateProfile(
            name="Li Qiang",
            age=63,
            c_fraktion=0.80,
            c_legitimitat=0.85,
            c_seniority=0.78,
            c_kompetenz=0.65,
            c_intl=0.30
        )

        ding_xuexiang = CandidateProfile(
            name="Ding Xuexiang",
            age=60,
            c_fraktion=0.85,
            c_legitimitat=0.75,
            c_seniority=0.70,
            c_kompetenz=0.70,
            c_intl=0.35
        )

        candidates = [li_qiang, ding_xuexiang]
        results = self.model.evaluate_conclave(candidates)

        # Li Qiang should rank #1 (most probable successor)
        self.assertEqual(results[0].candidate_name, "Li Qiang",
                        "Li Qiang should rank as most probable successor")


if __name__ == '__main__':
    unittest.main()
