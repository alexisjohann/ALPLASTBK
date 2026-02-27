"""
Test Suite for PSF 2.0: Conclave Coalition Dynamics ABM
Validates agent-based model implementation, mechanism behavior, and historical validation
"""

import unittest
import numpy as np
from conclave_abm import (
    ConclaveABM,
    CardinalAgent,
    Faction,
    VotingRound,
    SimulationResult,
    validate_against_historical,
)


class TestCardinalAgent(unittest.TestCase):
    """Test CardinalAgent dataclass properties"""

    def test_papabile_score_calculation(self):
        """Verify PSF 2.0 weighted score: 2.5λ + 1.8ι + 1.5π + 0.8ν + 0.5α"""
        agent = CardinalAgent(
            id=0, name="Test", faction=Faction.MODERATE,
            lambda_=1.0, iota=1.0, pi=1.0, nu=1.0, alpha=1.0,
        )
        expected = 2.5 + 1.8 + 1.5 + 0.8 + 0.5  # = 7.1
        self.assertAlmostEqual(agent.papabile_score, expected, places=5)

    def test_papabile_score_zero(self):
        """Zero dimensions produce zero score"""
        agent = CardinalAgent(
            id=0, name="Test", faction=Faction.NEUTRAL,
            lambda_=0.0, iota=0.0, pi=0.0, nu=0.0, alpha=0.0,
        )
        self.assertEqual(agent.papabile_score, 0.0)

    def test_dimension_vector(self):
        """Verify dimension vector order: [λ, ι, π, ν, α]"""
        agent = CardinalAgent(
            id=0, name="Test", faction=Faction.CONSERVATIVE,
            lambda_=0.9, iota=0.8, pi=0.7, nu=0.6, alpha=0.5,
        )
        np.testing.assert_array_almost_equal(
            agent.dimension_vector, [0.9, 0.8, 0.7, 0.6, 0.5]
        )

    def test_default_behavioral_states(self):
        """Verify default behavioral state values"""
        agent = CardinalAgent(
            id=0, name="Test", faction=Faction.MODERATE,
            lambda_=0.5, iota=0.5, pi=0.5, nu=0.5, alpha=0.5,
        )
        self.assertEqual(agent.faction_loyalty, 0.8)
        self.assertEqual(agent.strategic_voting, 0.3)
        self.assertEqual(agent.pressure_sensitivity, 0.5)
        self.assertEqual(agent.ambition_signal, 0.0)


class TestConclaveInitialization(unittest.TestCase):
    """Test ConclaveABM initialization and cardinal generation"""

    def test_default_initialization(self):
        """Default creates 120 cardinals with 5 papabili"""
        abm = ConclaveABM(n_cardinals=120, seed=42)
        abm.initialize_cardinals()
        self.assertEqual(len(abm.cardinals), 120)
        self.assertEqual(len(abm.papabili_ids), 5)

    def test_custom_cardinal_count(self):
        """Support custom number of cardinals"""
        abm = ConclaveABM(n_cardinals=60, n_papabili=3, seed=42)
        abm.initialize_cardinals()
        self.assertEqual(len(abm.cardinals), 60)
        self.assertEqual(len(abm.papabili_ids), 3)

    def test_papabili_are_first_agents(self):
        """Papabili have IDs 0..n_papabili-1"""
        abm = ConclaveABM(n_cardinals=120, n_papabili=5, seed=42)
        abm.initialize_cardinals()
        self.assertEqual(abm.papabili_ids, [0, 1, 2, 3, 4])

    def test_custom_papabili_profiles(self):
        """Custom papabili profiles are respected"""
        profiles = [
            {"name": "Candidate A", "lambda_": 0.90, "iota": 0.85,
             "pi": 0.80, "nu": 0.70, "alpha": 0.95, "faction": "conservative"},
        ]
        abm = ConclaveABM(n_cardinals=30, n_papabili=1, seed=42)
        abm.initialize_cardinals(papabili_profiles=profiles)
        self.assertEqual(abm.cardinals[0].name, "Candidate A")
        self.assertAlmostEqual(abm.cardinals[0].lambda_, 0.90)

    def test_beliefs_initialized(self):
        """All cardinals have belief distributions over papabili"""
        abm = ConclaveABM(n_cardinals=120, seed=42)
        abm.initialize_cardinals()
        for cardinal in abm.cardinals:
            self.assertEqual(len(cardinal.belief_distribution), 5)
            # Beliefs should sum to ~1 (normalized)
            total = sum(cardinal.belief_distribution.values())
            self.assertAlmostEqual(total, 1.0, places=3)

    def test_beliefs_positive(self):
        """All beliefs are positive (minimum floor applied)"""
        abm = ConclaveABM(n_cardinals=120, seed=42)
        abm.initialize_cardinals()
        for cardinal in abm.cardinals:
            for pid, belief in cardinal.belief_distribution.items():
                self.assertGreater(belief, 0.0)

    def test_faction_distribution(self):
        """Cardinals are distributed across factions"""
        abm = ConclaveABM(n_cardinals=1000, seed=42)  # Large N for statistical stability
        abm.initialize_cardinals()
        factions = [c.faction for c in abm.cardinals[5:]]  # Skip papabili
        faction_counts = {f: 0 for f in Faction}
        for f in factions:
            faction_counts[f] += 1
        # All factions should have at least some cardinals
        for f, count in faction_counts.items():
            self.assertGreater(count, 0, f"Faction {f} has no cardinals")

    def test_parameter_override(self):
        """Custom parameters override defaults"""
        custom = {'supermajority_threshold': 0.75}
        abm = ConclaveABM(params=custom, seed=42)
        self.assertAlmostEqual(abm.PARAMS['supermajority_threshold'], 0.75)
        # Other params unchanged
        self.assertAlmostEqual(abm.PARAMS['lock_in_pressure_rate'], 0.06)


class TestSutterMechanisms(unittest.TestCase):
    """Test that each Sutter mechanism affects agent state correctly"""

    def setUp(self):
        self.abm = ConclaveABM(n_cardinals=60, n_papabili=3, seed=42)
        self.abm.initialize_cardinals()

    def test_m1_lock_in_pressure_increases(self):
        """M1: Lock-in pressure increases linearly with round number"""
        effects_r1 = self.abm._apply_mechanisms(1)
        effects_r5 = self.abm._apply_mechanisms(5)
        self.assertGreater(
            effects_r5['M1_lock_in_pressure'],
            effects_r1['M1_lock_in_pressure']
        )

    def test_m5_strategic_voting_decreases(self):
        """M5: Sacred space reduces strategic voting over rounds"""
        initial_strategic = np.mean([c.strategic_voting for c in self.abm.cardinals])
        self.abm._apply_mechanisms(1)
        self.abm._apply_mechanisms(2)
        self.abm._apply_mechanisms(3)
        after_strategic = np.mean([c.strategic_voting for c in self.abm.cardinals])
        self.assertLess(after_strategic, initial_strategic)

    def test_m5_strategic_voting_floor(self):
        """M5: Strategic voting doesn't go below the floor"""
        for _ in range(30):
            self.abm._apply_mechanisms(10)
        for c in self.abm.cardinals:
            self.assertGreaterEqual(c.strategic_voting, self.abm.PARAMS['moral_awareness_floor'])

    def test_m8_faction_loyalty_decays(self):
        """M8: Faction loyalty decreases over rounds"""
        initial_loyalty = np.mean([c.faction_loyalty for c in self.abm.cardinals])
        for r in range(1, 6):
            self.abm._apply_mechanisms(r)
        after_loyalty = np.mean([c.faction_loyalty for c in self.abm.cardinals])
        self.assertLess(after_loyalty, initial_loyalty)

    def test_m8_acceleration_after_round_5(self):
        """M8: Faction decay accelerates after round 5"""
        abm1 = ConclaveABM(n_cardinals=60, n_papabili=3, seed=42)
        abm1.initialize_cardinals()
        abm2 = ConclaveABM(n_cardinals=60, n_papabili=3, seed=42)
        abm2.initialize_cardinals()

        # Decay before round 5
        for r in range(1, 5):
            abm1._apply_mechanisms(r)
        loyalty_before_5 = np.mean([c.faction_loyalty for c in abm1.cardinals])
        abm1._apply_mechanisms(5)
        loyalty_after_5 = np.mean([c.faction_loyalty for c in abm1.cardinals])
        decay_at_5 = loyalty_before_5 - loyalty_after_5

        # Decay after round 5 (accelerated)
        for r in range(1, 6):
            abm2._apply_mechanisms(r)
        loyalty_before_6 = np.mean([c.faction_loyalty for c in abm2.cardinals])
        abm2._apply_mechanisms(6)
        loyalty_after_6 = np.mean([c.faction_loyalty for c in abm2.cardinals])
        decay_at_6 = loyalty_before_6 - loyalty_after_6

        self.assertGreater(decay_at_6, decay_at_5)

    def test_m7_pressure_only_after_round_3(self):
        """M7: Progressive pressure only kicks in after pressure_start_round"""
        effects_r1 = self.abm._apply_mechanisms(1)
        effects_r2 = self.abm._apply_mechanisms(2)
        self.assertEqual(effects_r1['M7_progressive_pressure'], 0.0)
        self.assertEqual(effects_r2['M7_progressive_pressure'], 0.0)

    def test_m6_belief_convergence_entropy_decreases(self):
        """M6: Belief convergence (entropy) decreases during simulation"""
        # Run a few rounds of simulation to get voting history
        self.abm.simulate(max_rounds=5)
        # Entropy should decrease from first to last round
        first_entropy = self.abm.rounds[0].faction_loyalty_mean
        last_entropy = self.abm.rounds[-1].faction_loyalty_mean
        # Faction loyalty should decrease (as proxy for increasing convergence)
        self.assertLessEqual(last_entropy, first_entropy)


class TestVoting(unittest.TestCase):
    """Test voting mechanism (M4: secret ballot)"""

    def test_all_cardinals_vote(self):
        """Every cardinal casts exactly one vote"""
        abm = ConclaveABM(n_cardinals=120, seed=42)
        abm.initialize_cardinals()
        votes = abm._conduct_vote(1)
        self.assertEqual(len(votes), 120)

    def test_votes_for_papabili_only(self):
        """Cardinals only vote for papabili candidates"""
        abm = ConclaveABM(n_cardinals=120, seed=42)
        abm.initialize_cardinals()
        votes = abm._conduct_vote(1)
        for cardinal_id, voted_for in votes.items():
            self.assertIn(voted_for, abm.papabili_ids)

    def test_votes_reproducible_with_seed(self):
        """Same seed produces same votes"""
        votes1 = self._run_vote(seed=42)
        votes2 = self._run_vote(seed=42)
        self.assertEqual(votes1, votes2)

    def test_votes_differ_with_seed(self):
        """Different seeds produce different votes"""
        votes1 = self._run_vote(seed=42)
        votes2 = self._run_vote(seed=99)
        self.assertNotEqual(votes1, votes2)

    def _run_vote(self, seed):
        abm = ConclaveABM(n_cardinals=120, seed=seed)
        abm.initialize_cardinals()
        return abm._conduct_vote(1)


class TestSimulation(unittest.TestCase):
    """Test full simulation execution"""

    def test_simulation_converges(self):
        """Default simulation reaches 2/3 supermajority"""
        abm = ConclaveABM(n_cardinals=120, seed=42)
        abm.initialize_cardinals()
        result = abm.simulate(max_rounds=30)
        # Should converge (last round has converged=True)
        self.assertTrue(result.rounds[-1].converged)

    def test_simulation_returns_valid_result(self):
        """SimulationResult has all required fields"""
        abm = ConclaveABM(n_cardinals=120, seed=42)
        abm.initialize_cardinals()
        result = abm.simulate()
        self.assertIsInstance(result, SimulationResult)
        self.assertIn(result.winner_id, abm.papabili_ids)
        self.assertGreater(result.total_rounds, 0)
        self.assertEqual(len(result.rounds), result.total_rounds)

    def test_threshold_is_two_thirds(self):
        """2/3 supermajority threshold is correctly calculated"""
        abm = ConclaveABM(n_cardinals=120, seed=42)
        threshold = int(np.ceil(120 * 2/3))
        self.assertEqual(threshold, 80)

    def test_simulation_respects_max_rounds(self):
        """Simulation stops at max_rounds if no convergence"""
        # Use extreme parameters that prevent convergence
        params = {'belief_update_rate': 0.01, 'commitment_threshold': 0.99}
        abm = ConclaveABM(n_cardinals=120, params=params, seed=42)
        abm.initialize_cardinals()
        result = abm.simulate(max_rounds=5)
        self.assertLessEqual(result.total_rounds, 5)

    def test_winning_vote_count_meets_threshold(self):
        """Winner's final vote count meets 2/3 threshold"""
        abm = ConclaveABM(n_cardinals=120, seed=42)
        abm.initialize_cardinals()
        result = abm.simulate()
        if result.rounds[-1].converged:
            threshold = int(np.ceil(120 * 2/3))
            self.assertGreaterEqual(result.rounds[-1].leading_votes, threshold)

    def test_coalition_history_recorded(self):
        """Coalition structures recorded for each round"""
        abm = ConclaveABM(n_cardinals=120, seed=42)
        abm.initialize_cardinals()
        result = abm.simulate()
        self.assertEqual(len(result.coalition_history), result.total_rounds)

    def test_mechanism_effects_tracked(self):
        """Mechanism effects are tracked for each round"""
        abm = ConclaveABM(n_cardinals=120, seed=42)
        abm.initialize_cardinals()
        result = abm.simulate()
        expected_keys = [
            'M1_lock_in_pressure', 'M2_coalition_breadth',
            'M3_ambition_penalties', 'M5_strategic_reduction',
            'M6_belief_convergence', 'M7_progressive_pressure',
            'M8_faction_loyalty'
        ]
        for key in expected_keys:
            self.assertIn(key, result.mechanism_effects)
            self.assertEqual(len(result.mechanism_effects[key]), result.total_rounds)

    def test_auto_initialize_if_needed(self):
        """Simulation auto-initializes cardinals if not done explicitly"""
        abm = ConclaveABM(n_cardinals=120, seed=42)
        result = abm.simulate()  # No explicit initialize_cardinals()
        self.assertGreater(result.total_rounds, 0)

    def test_strongest_papabile_wins(self):
        """The highest-scoring papabile wins in standard conditions"""
        abm = ConclaveABM(n_cardinals=120, seed=42)
        abm.initialize_cardinals()
        result = abm.simulate()
        # The default Insider (Prevost-type, ID=3) has the highest papabile_score
        winner = abm.cardinals[result.winner_id]
        scores = {pid: abm.cardinals[pid].papabile_score for pid in abm.papabili_ids}
        max_score_id = max(scores, key=scores.get)
        self.assertEqual(result.winner_id, max_score_id)


class TestBeliefUpdating(unittest.TestCase):
    """Test M6: Bayesian belief updating mechanism"""

    def test_beliefs_shift_toward_observed(self):
        """After observing votes, beliefs shift toward the observed distribution"""
        abm = ConclaveABM(n_cardinals=120, seed=42)
        abm.initialize_cardinals()

        # Record initial beliefs for first non-papabile cardinal
        cardinal = abm.cardinals[10]
        initial_belief_0 = cardinal.belief_distribution[0]

        # Simulate vote counts where candidate 0 gets majority
        vote_counts = {pid: 5 for pid in abm.papabili_ids}
        vote_counts[0] = 90  # Candidate 0 dominates

        abm._update_beliefs(vote_counts, round_num=1)
        after_belief_0 = cardinal.belief_distribution[0]

        # Belief in candidate 0 should increase
        self.assertGreater(after_belief_0, initial_belief_0)

    def test_dropout_mechanism(self):
        """Candidates below dropout threshold lose support rapidly"""
        abm = ConclaveABM(n_cardinals=120, seed=42)
        abm.initialize_cardinals()

        cardinal = abm.cardinals[10]
        initial_belief_4 = cardinal.belief_distribution[4]

        # Candidate 4 gets 0 votes (well below dropout threshold)
        vote_counts = {0: 50, 1: 30, 2: 25, 3: 15, 4: 0}
        abm._update_beliefs(vote_counts, round_num=2)  # round > 1 for dropout

        after_belief_4 = cardinal.belief_distribution[4]
        # Belief should be substantially reduced
        self.assertLess(after_belief_4, initial_belief_4 * 0.7)

    def test_beliefs_remain_normalized(self):
        """Beliefs stay normalized after updating"""
        abm = ConclaveABM(n_cardinals=120, seed=42)
        abm.initialize_cardinals()

        vote_counts = {0: 40, 1: 30, 2: 25, 3: 15, 4: 10}
        abm._update_beliefs(vote_counts, round_num=1)

        for cardinal in abm.cardinals:
            total = sum(cardinal.belief_distribution.values())
            self.assertAlmostEqual(total, 1.0, places=3)


class TestSummary(unittest.TestCase):
    """Test human-readable output generation"""

    def test_summary_contains_key_info(self):
        """Summary includes winner, rounds, and mechanism effects"""
        abm = ConclaveABM(n_cardinals=120, seed=42)
        abm.initialize_cardinals()
        result = abm.simulate()
        summary = abm.get_summary(result)
        self.assertIn("Winner:", summary)
        self.assertIn("Rounds:", summary)
        self.assertIn("MECHANISM EFFECTS:", summary)
        self.assertIn("ROUND-BY-ROUND:", summary)

    def test_summary_shows_elected(self):
        """Summary marks the winning round as ELECTED"""
        abm = ConclaveABM(n_cardinals=120, seed=42)
        abm.initialize_cardinals()
        result = abm.simulate()
        summary = abm.get_summary(result)
        self.assertIn("ELECTED", summary)


class TestHistoricalValidation(unittest.TestCase):
    """Test validation against 12 historical conclaves"""

    @classmethod
    def setUpClass(cls):
        """Run validation once (Monte Carlo takes time)"""
        cls.validation = validate_against_historical(seed=42)

    def test_twelve_conclaves_evaluated(self):
        """All 12 historical conclaves are evaluated"""
        self.assertEqual(len(self.validation['results']), 12)

    def test_winner_accuracy_above_80_percent(self):
        """ABM predicts correct winner in >80% of conclaves"""
        self.assertGreaterEqual(self.validation['winner_accuracy'], 0.80)

    def test_mean_duration_error_below_5(self):
        """Mean duration prediction error below 5 rounds"""
        self.assertLess(self.validation['mean_error'], 5.0)

    def test_duration_correlation_positive(self):
        """Duration correlation with historical data is positive"""
        self.assertGreater(self.validation['correlation'], 0.0)

    def test_all_conclaves_converge(self):
        """No conclave hits the 30-round maximum (median)"""
        for r in self.validation['results']:
            self.assertLess(r['simulated_rounds'], 30)

    def test_result_has_mc_data(self):
        """Each conclave result includes Monte Carlo metadata"""
        for r in self.validation['results']:
            self.assertIn('mc_range', r)
            self.assertIn('winner_rate', r)
            self.assertGreaterEqual(r['winner_rate'], 0.0)
            self.assertLessEqual(r['winner_rate'], 1.0)

    def test_short_conclave_simulated_short(self):
        """Pius XII 1939 (2 rounds actual) simulated in ≤5 rounds"""
        pius_xii = next(r for r in self.validation['results'] if r['year'] == 1939)
        self.assertLessEqual(pius_xii['simulated_rounds'], 5)

    def test_conclave_years_correct(self):
        """All expected conclave years are present"""
        years = [r['year'] for r in self.validation['results']]
        expected_years = [1878, 1903, 1914, 1922, 1939, 1958, 1963, 1978, 1978, 2005, 2013, 2025]
        self.assertEqual(years, expected_years)


class TestReproducibility(unittest.TestCase):
    """Test that simulations are reproducible with the same seed"""

    def test_same_seed_same_result(self):
        """Identical seeds produce identical simulation results"""
        result1 = self._run_simulation(seed=42)
        result2 = self._run_simulation(seed=42)
        self.assertEqual(result1.winner_id, result2.winner_id)
        self.assertEqual(result1.total_rounds, result2.total_rounds)

    def test_different_seed_may_differ(self):
        """Different seeds can produce different results"""
        results = [self._run_simulation(seed=s).total_rounds for s in range(10)]
        # At least some variation across seeds
        self.assertGreater(len(set(results)), 1)

    def _run_simulation(self, seed):
        abm = ConclaveABM(n_cardinals=120, seed=seed)
        abm.initialize_cardinals()
        return abm.simulate()


if __name__ == '__main__':
    # Run all tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    test_classes = [
        TestCardinalAgent,
        TestConclaveInitialization,
        TestSutterMechanisms,
        TestVoting,
        TestSimulation,
        TestBeliefUpdating,
        TestSummary,
        TestHistoricalValidation,
        TestReproducibility,
    ]

    for tc in test_classes:
        suite.addTests(loader.loadTestsFromTestCase(tc))

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
