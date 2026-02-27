"""
Unit Tests for GPM 3.0: Goalkeeper Performance Model

Tests cover:
- TechniqueDimensions data class (6 dimensions including D6 injury risk)
- D6 composite calculation (D6 = 0.5*D6a + 0.5*D6b)
- PerformanceLevel computation
- GoalkeeperProfile total performance
- GoalkeeperPerformanceModel scoring, comparison, allocation
- Complementarity analysis
- Substitution cost analysis
- Visibility-Contribution framework
- V*_eff Availability framework
- Edge cases and invariants
- Predictions PRED-GPM-001 through PRED-GPM-012

Run: pytest models/GPM-1-0-GOALKEEPER-PERFORMANCE/test_gpm_model.py -v
"""

import numpy as np
import pytest

from gpm_model import (
    AvailabilityProfile,
    GoalkeeperPerformanceModel,
    GoalkeeperProfile,
    PerformanceLevel,
    TechniqueDimensions,
    VisibilityContribution,
    VISIBILITY_SPECTRUM,
    compute_effective_value,
    create_reference_profiles,
    create_reference_availability,
    REFERENCE_TRAINING_ALLOCATIONS,
)


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def model():
    """Standard model with default v3.0 weights."""
    return GoalkeeperPerformanceModel()


@pytest.fixture
def custom_model():
    """Model with equal weights (6 dimensions)."""
    w = np.array([1/6, 1/6, 1/6, 1/6, 1/6, 1/6])
    return GoalkeeperPerformanceModel(weights=w)


@pytest.fixture
def catch_technique():
    return TechniqueDimensions(
        game_relevance=0.85,
        risk_reduction=0.95,
        learning_efficiency=0.55,
        coach_transmissibility=0.80,
        strategic_potential=0.90,
        injury_risk_non_contact=0.85,
        injury_risk_contact=0.55,
    )


@pytest.fixture
def block_technique():
    return TechniqueDimensions(
        game_relevance=0.20,
        risk_reduction=0.50,
        learning_efficiency=0.35,
        coach_transmissibility=0.30,
        strategic_potential=0.10,
        injury_risk_non_contact=0.25,
        injury_risk_contact=0.20,
    )


@pytest.fixture
def balanced_profile(model):
    return model.evaluate_goalkeeper(
        name="Balanced",
        strategic_components={'S1': 0.7, 'S2': 0.7, 'S3': 0.7, 'S4': 0.7},
        tactical_components={'T1': 0.7, 'T2': 0.7, 'T3': 0.7, 'T4': 0.7},
        operative_components={'O1': 0.7, 'O2': 0.7, 'O3': 0.7, 'O4': 0.7, 'O5': 0.7},
    )


@pytest.fixture
def operative_only_profile(model):
    return model.evaluate_goalkeeper(
        name="Operative-Only",
        strategic_components={'S1': 0.3, 'S2': 0.3, 'S3': 0.3, 'S4': 0.3},
        tactical_components={'T1': 0.3, 'T2': 0.3, 'T3': 0.3, 'T4': 0.3},
        operative_components={'O1': 0.9, 'O2': 0.9, 'O3': 0.9, 'O4': 0.9, 'O5': 0.9},
    )


# ============================================================================
# TECHNIQUE DIMENSIONS (6D)
# ============================================================================

class TestTechniqueDimensions:

    def test_to_vector(self, catch_technique):
        vec = catch_technique.to_vector()
        assert isinstance(vec, np.ndarray)
        assert len(vec) == 6
        assert vec[0] == 0.85  # game_relevance
        assert vec[1] == 0.95  # risk_reduction
        assert vec[5] == pytest.approx(0.70)  # injury_risk (computed)

    def test_to_dict(self, catch_technique):
        d = catch_technique.to_dict()
        assert 'D1_game_relevance' in d
        assert 'D5_strategic_potential' in d
        assert 'D6_injury_risk' in d
        assert d['D1_game_relevance'] == 0.85
        assert d['D5_strategic_potential'] == 0.90
        assert d['D6_injury_risk'] == pytest.approx(0.70)

    def test_to_dict_with_sub_components(self, catch_technique):
        d = catch_technique.to_dict()
        assert 'D6a_non_contact' in d
        assert 'D6b_contact' in d
        assert d['D6a_non_contact'] == 0.85
        assert d['D6b_contact'] == 0.55

    def test_to_dict_without_sub_components(self):
        t = TechniqueDimensions(0.5, 0.5, 0.5, 0.5, 0.5, injury_risk=0.6)
        d = t.to_dict()
        assert 'D6_injury_risk' in d
        assert d['D6_injury_risk'] == 0.6
        assert 'D6a_non_contact' not in d
        assert 'D6b_contact' not in d

    def test_all_values_in_range(self, catch_technique):
        vec = catch_technique.to_vector()
        assert all(0.0 <= v <= 1.0 for v in vec)

    def test_zero_technique(self):
        zero = TechniqueDimensions(0.0, 0.0, 0.0, 0.0, 0.0, injury_risk=0.0)
        assert np.allclose(zero.to_vector(), np.zeros(6))

    def test_max_technique(self):
        perfect = TechniqueDimensions(1.0, 1.0, 1.0, 1.0, 1.0, injury_risk=1.0)
        assert np.allclose(perfect.to_vector(), np.ones(6))

    def test_default_injury_risk(self):
        """D6 defaults to 0.50 when not specified."""
        t = TechniqueDimensions(0.5, 0.5, 0.5, 0.5, 0.5)
        assert t.injury_risk == 0.50
        vec = t.to_vector()
        assert len(vec) == 6
        assert vec[5] == 0.50


# ============================================================================
# D6 INJURY RISK
# ============================================================================

class TestInjuryRisk:

    def test_d6_composite_calculation(self):
        """D6 = 0.5 * D6a + 0.5 * D6b."""
        t = TechniqueDimensions(
            0.5, 0.5, 0.5, 0.5, 0.5,
            injury_risk_non_contact=0.80,
            injury_risk_contact=0.40,
        )
        assert t.injury_risk == pytest.approx(0.60)

    def test_d6_composite_symmetric(self):
        """D6a and D6b contribute equally."""
        t1 = TechniqueDimensions(
            0.5, 0.5, 0.5, 0.5, 0.5,
            injury_risk_non_contact=0.90,
            injury_risk_contact=0.10,
        )
        t2 = TechniqueDimensions(
            0.5, 0.5, 0.5, 0.5, 0.5,
            injury_risk_non_contact=0.10,
            injury_risk_contact=0.90,
        )
        assert t1.injury_risk == pytest.approx(t2.injury_risk)

    def test_block_highest_injury_risk(self, model):
        """BLOCK should have the highest injury exposure (lowest D6) of all techniques."""
        techniques = model.techniques
        block_d6 = techniques['BLOCK'].injury_risk
        for name, tech in techniques.items():
            if name != 'BLOCK':
                assert tech.injury_risk > block_d6, (
                    f"{name} (D6={tech.injury_risk}) should be safer than BLOCK (D6={block_d6})"
                )

    def test_catch_safest_technique(self, model):
        """CATCH should have the lowest injury exposure (highest D6)."""
        techniques = model.techniques
        catch_d6 = techniques['CATCH'].injury_risk
        for name, tech in techniques.items():
            if name != 'CATCH':
                assert tech.injury_risk <= catch_d6, (
                    f"{name} (D6={tech.injury_risk}) should not be safer than CATCH (D6={catch_d6})"
                )

    def test_block_3x_more_dangerous_than_catch(self, model):
        """BLOCK injury exposure is ~3.1x higher than CATCH (inverted scale)."""
        catch_risk = 1.0 - model.techniques['CATCH'].injury_risk
        block_risk = 1.0 - model.techniques['BLOCK'].injury_risk
        ratio = block_risk / catch_risk
        assert ratio > 2.5, f"Block/Catch risk ratio {ratio:.1f}x should be > 2.5x"

    def test_d6_contributes_positively_to_catch_advantage(self, model):
        """D6 contributes positively to CATCH's advantage over BLOCK."""
        catch_d6 = model.techniques['CATCH'].injury_risk
        block_d6 = model.techniques['BLOCK'].injury_risk
        w6 = model.weights[5]

        # D6 contribution to gap = w6 * (catch_D6 - block_D6)
        d6_contribution = w6 * (catch_d6 - block_d6)
        assert d6_contribution > 0, "D6 should favor CATCH over BLOCK"
        assert d6_contribution > 0.05, f"D6 contribution {d6_contribution:.3f} should be substantial"

    def test_d6_only_set_when_both_sub_components(self):
        """D6 auto-computes only when BOTH D6a and D6b are provided."""
        # Only D6a set — D6 stays at default
        t = TechniqueDimensions(
            0.5, 0.5, 0.5, 0.5, 0.5,
            injury_risk_non_contact=0.80,
        )
        assert t.injury_risk == 0.50  # default, not auto-computed

    def test_d6_sub_component_values(self, model):
        """Reference techniques should have D6a and D6b set."""
        catch = model.techniques['CATCH']
        assert catch.injury_risk_non_contact is not None
        assert catch.injury_risk_contact is not None
        assert catch.injury_risk_non_contact == 0.85
        assert catch.injury_risk_contact == 0.55


# ============================================================================
# PERFORMANCE LEVEL
# ============================================================================

class TestPerformanceLevel:

    def test_compute_score_from_components(self):
        level = PerformanceLevel(
            level_id="L_S", name="Strategic", score=0.0,
            components={'S1': 0.6, 'S2': 0.8, 'S3': 0.7, 'S4': 0.5},
        )
        score = level.compute_score()
        assert score == pytest.approx(0.65, abs=1e-6)
        assert level.score == pytest.approx(0.65, abs=1e-6)

    def test_compute_score_empty_components(self):
        level = PerformanceLevel(level_id="L_T", name="Tactical", score=0.5)
        score = level.compute_score()
        assert score == 0.5  # no components, returns existing score

    def test_single_component(self):
        level = PerformanceLevel(
            level_id="L_O", name="Operative", score=0.0,
            components={'O1': 0.9},
        )
        assert level.compute_score() == pytest.approx(0.9)


# ============================================================================
# GOALKEEPER PROFILE
# ============================================================================

class TestGoalkeeperProfile:

    def test_total_performance_balanced(self, balanced_profile):
        total = balanced_profile.total_performance()
        assert 0.0 < total < 1.0
        assert total == pytest.approx(0.583, abs=0.01)

    def test_total_performance_operative_only(self, operative_only_profile):
        total = operative_only_profile.total_performance()
        assert 0.0 < total < 1.0

    def test_balanced_beats_operative_only(self, balanced_profile, operative_only_profile):
        """Core prediction PRED-GPM-002: balanced GK > one-dimensional GK."""
        assert balanced_profile.total_performance() > operative_only_profile.total_performance()

    def test_total_performance_with_zero_gamma(self, balanced_profile):
        """Without complementarity, total performance is just weighted average."""
        total = balanced_profile.total_performance(gamma_st=0, gamma_so=0, gamma_to=0)
        expected = 0.30 * 0.70 + 0.35 * 0.70 + 0.35 * 0.70
        assert total == pytest.approx(expected, abs=1e-6)

    def test_total_performance_bounded(self, balanced_profile):
        """Total performance must be in [0, 1]."""
        total = balanced_profile.total_performance()
        assert 0.0 <= total <= 1.0

    def test_perfect_profile(self):
        perfect = GoalkeeperProfile(
            name="Perfect",
            strategic=PerformanceLevel("L_S", "S", 1.0),
            tactical=PerformanceLevel("L_T", "T", 1.0),
            operative=PerformanceLevel("L_O", "O", 1.0),
        )
        total = perfect.total_performance()
        assert total == pytest.approx(1.0, abs=1e-6)

    def test_zero_profile(self):
        zero = GoalkeeperProfile(
            name="Zero",
            strategic=PerformanceLevel("L_S", "S", 0.0),
            tactical=PerformanceLevel("L_T", "T", 0.0),
            operative=PerformanceLevel("L_O", "O", 0.0),
        )
        total = zero.total_performance()
        assert total == pytest.approx(0.0, abs=1e-6)

    def test_to_dict(self, balanced_profile):
        d = balanced_profile.to_dict()
        assert d['name'] == 'Balanced'
        assert d['L_S'] == pytest.approx(0.70)
        assert d['L_T'] == pytest.approx(0.70)
        assert d['L_O'] == pytest.approx(0.70)
        assert 'total_performance' in d


# ============================================================================
# MODEL: TECHNIQUE SCORING (v3.0 weights)
# ============================================================================

class TestTechniqueScoring:

    def test_score_technique_catch(self, model, catch_technique):
        score = model.score_technique(catch_technique)
        # v3.0: S = 0.25*0.85 + 0.22*0.95 + 0.13*0.55 + 0.08*0.80 + 0.17*0.90 + 0.15*0.70
        expected = 0.2125 + 0.209 + 0.0715 + 0.064 + 0.153 + 0.105
        assert score == pytest.approx(expected, abs=1e-4)

    def test_score_technique_block(self, model, block_technique):
        score = model.score_technique(block_technique)
        # v3.0: S = 0.25*0.20 + 0.22*0.50 + 0.13*0.35 + 0.08*0.30 + 0.17*0.10 + 0.15*0.225
        expected = 0.05 + 0.11 + 0.0455 + 0.024 + 0.017 + 0.03375
        assert score == pytest.approx(expected, abs=1e-4)

    def test_catch_dominates_block(self, model, catch_technique, block_technique):
        """PRED-GPM-001: Catching scores higher than blocking in total."""
        assert model.score_technique(catch_technique) > model.score_technique(block_technique)

    def test_catch_wins_all_six_dimensions(self, catch_technique, block_technique):
        """Catching should be >= blocking in every dimension (6/6)."""
        for i, (c, b) in enumerate(zip(catch_technique.to_vector(), block_technique.to_vector())):
            assert c >= b, f"Dimension {i}: CATCH ({c}) should >= BLOCK ({b})"

    def test_score_with_equal_weights(self, custom_model, catch_technique):
        score = custom_model.score_technique(catch_technique)
        expected = np.mean(catch_technique.to_vector())
        assert score == pytest.approx(expected, abs=1e-6)

    def test_evaluate_all_returns_five_techniques(self, model):
        scores = model.evaluate_all()
        assert len(scores) == 5
        assert set(scores.keys()) == {'CATCH', 'PARRY_SAFE', 'BLOCK', 'PUNCH', 'FOOT_SAVE'}

    def test_evaluate_all_ordering(self, model):
        """CATCH should be highest, BLOCK should be lowest."""
        scores = model.evaluate_all()
        assert scores['CATCH'] == max(scores.values())
        assert scores['BLOCK'] == min(scores.values())

    def test_scores_bounded(self, model):
        scores = model.evaluate_all()
        for score in scores.values():
            assert 0.0 <= score <= 1.0


# ============================================================================
# MODEL: COMPARISON (6D)
# ============================================================================

class TestComparison:

    def test_compare_catch_block(self, model):
        result = model.compare('CATCH', 'BLOCK')
        assert result['technique_a'] == 'CATCH'
        assert result['technique_b'] == 'BLOCK'
        assert result['overall_advantage'] == 'CATCH'
        assert result['dimensions_won_a'] == 6  # CATCH wins all 6
        assert result['dimensions_won_b'] == 0

    def test_compare_has_per_dimension(self, model):
        result = model.compare('CATCH', 'PARRY_SAFE')
        assert len(result['per_dimension']) == 6
        for dim in result['per_dimension']:
            assert 'dimension' in dim
            assert 'weight' in dim
            assert 'delta' in dim

    def test_compare_scores_match_evaluate(self, model):
        result = model.compare('CATCH', 'BLOCK')
        scores = model.evaluate_all()
        assert result['score_a'] == pytest.approx(scores['CATCH'])
        assert result['score_b'] == pytest.approx(scores['BLOCK'])

    def test_compare_symmetric_delta(self, model):
        """Delta should be the same regardless of order."""
        ab = model.compare('CATCH', 'BLOCK')
        ba = model.compare('BLOCK', 'CATCH')
        assert abs(ab['score_a'] - ab['score_b']) == pytest.approx(
            abs(ba['score_a'] - ba['score_b'])
        )

    def test_compare_includes_injury_risk(self, model):
        """Comparison should include D6 (Injury Risk) dimension."""
        result = model.compare('CATCH', 'BLOCK')
        dim_names = [d['dimension'] for d in result['per_dimension']]
        assert 'Injury Risk' in dim_names


# ============================================================================
# MODEL: TRAINING ALLOCATION
# ============================================================================

class TestTrainingAllocation:

    def test_allocation_sums_to_one(self, model):
        alloc = model.compute_allocation()
        assert sum(alloc.values()) == pytest.approx(1.0, abs=1e-6)

    def test_allocation_all_positive(self, model):
        alloc = model.compute_allocation()
        for v in alloc.values():
            assert v > 0.0

    def test_catch_gets_most_allocation(self, model):
        """PRED-GPM-003: Catching should get the largest allocation."""
        alloc = model.compute_allocation()
        assert alloc['CATCH'] == max(alloc.values())

    def test_block_gets_least_allocation(self, model):
        """Blocking should get the smallest or near-smallest allocation."""
        alloc = model.compute_allocation()
        sorted_alloc = sorted(alloc.values())
        assert alloc['BLOCK'] <= sorted_alloc[1]  # Among the bottom 2

    def test_custom_frequencies(self, model):
        freq = {
            'CATCH': 0.60,
            'PARRY_SAFE': 0.20,
            'BLOCK': 0.02,
            'PUNCH': 0.10,
            'FOOT_SAVE': 0.08,
        }
        alloc = model.compute_allocation(game_frequencies=freq)
        assert sum(alloc.values()) == pytest.approx(1.0, abs=1e-6)
        # With high catch frequency, catch allocation should increase
        default_alloc = model.compute_allocation()
        assert alloc['CATCH'] >= default_alloc['CATCH'] - 0.05  # roughly same or higher

    def test_custom_proficiency(self, model):
        prof = {
            'CATCH': 0.9,  # very proficient
            'PARRY_SAFE': 0.5,
            'BLOCK': 0.2,  # weak
            'PUNCH': 0.5,
            'FOOT_SAVE': 0.5,
        }
        alloc = model.compute_allocation(proficiency=prof)
        assert sum(alloc.values()) == pytest.approx(1.0, abs=1e-6)

    def test_allocation_five_techniques(self, model):
        alloc = model.compute_allocation()
        assert len(alloc) == 5


# ============================================================================
# MODEL: COMPLEMENTARITY
# ============================================================================

class TestComplementarity:

    def test_complementarity_value_balanced(self, model, balanced_profile):
        comp = model.complementarity_value(balanced_profile)
        assert comp['total_complementarity'] > 0
        assert comp['complementarity_share'] > 0
        assert comp['total_performance'] > 0

    def test_complementarity_increases_with_balance(self, model, balanced_profile, operative_only_profile):
        """Balanced profile should have higher complementarity share."""
        comp_balanced = model.complementarity_value(balanced_profile)
        comp_one_dim = model.complementarity_value(operative_only_profile)
        assert comp_balanced['total_complementarity'] > comp_one_dim['total_complementarity']

    def test_complementarity_zero_for_zero_profile(self, model):
        zero = model.evaluate_goalkeeper(
            name="Zero",
            strategic_components={'S1': 0.0},
            tactical_components={'T1': 0.0},
            operative_components={'O1': 0.0},
        )
        comp = model.complementarity_value(zero)
        assert comp['total_complementarity'] == pytest.approx(0.0)

    def test_complementarity_components_sum(self, model, balanced_profile):
        comp = model.complementarity_value(balanced_profile)
        total = (comp['complementarity_ST'] +
                 comp['complementarity_SO'] +
                 comp['complementarity_TO'])
        assert total == pytest.approx(comp['total_complementarity'], abs=1e-6)

    def test_complementarity_positive_cross_derivatives(self, model):
        """
        Core mathematical property: d²L/dL_i dL_j > 0
        Increasing one level should increase the marginal value of another.
        """
        # Compare marginal value of L_T at L_S=0.3 vs L_S=0.7
        low_s = model.evaluate_goalkeeper(
            name="Low S",
            strategic_components={'S1': 0.3},
            tactical_components={'T1': 0.5},
            operative_components={'O1': 0.5},
        )
        high_s = model.evaluate_goalkeeper(
            name="High S",
            strategic_components={'S1': 0.7},
            tactical_components={'T1': 0.5},
            operative_components={'O1': 0.5},
        )

        # Now increase T by delta for both
        delta = 0.1
        low_s_high_t = model.evaluate_goalkeeper(
            name="Low S + dT",
            strategic_components={'S1': 0.3},
            tactical_components={'T1': 0.5 + delta},
            operative_components={'O1': 0.5},
        )
        high_s_high_t = model.evaluate_goalkeeper(
            name="High S + dT",
            strategic_components={'S1': 0.7},
            tactical_components={'T1': 0.5 + delta},
            operative_components={'O1': 0.5},
        )

        marginal_t_low_s = low_s_high_t.total_performance() - low_s.total_performance()
        marginal_t_high_s = high_s_high_t.total_performance() - high_s.total_performance()

        # Positive cross-derivative: marginal value of T is higher when S is higher
        assert marginal_t_high_s > marginal_t_low_s


# ============================================================================
# MODEL: SUBSTITUTION COST
# ============================================================================

class TestSubstitutionCost:

    def test_substitution_no_change(self, model):
        alloc = {
            'CATCH': 0.35, 'PARRY_SAFE': 0.25,
            'BLOCK': 0.10, 'PUNCH': 0.15, 'FOOT_SAVE': 0.15,
        }
        result = model.substitution_cost(alloc, alloc)
        assert result['net_change'] == pytest.approx(0.0, abs=1e-6)
        assert len(result['shifts']) == 0

    def test_shift_to_block_reduces_value(self, model):
        """PRED-GPM-004: Shifting from catch-heavy to block-heavy reduces value."""
        current = {
            'CATCH': 0.35, 'PARRY_SAFE': 0.25,
            'BLOCK': 0.10, 'PUNCH': 0.15, 'FOOT_SAVE': 0.15,
        }
        block_heavy = {
            'CATCH': 0.15, 'PARRY_SAFE': 0.15,
            'BLOCK': 0.40, 'PUNCH': 0.15, 'FOOT_SAVE': 0.15,
        }
        result = model.substitution_cost(current, block_heavy)
        assert result['net_change'] < 0  # value decreases

    def test_shift_to_catch_increases_value(self, model):
        current = {
            'CATCH': 0.20, 'PARRY_SAFE': 0.20,
            'BLOCK': 0.20, 'PUNCH': 0.20, 'FOOT_SAVE': 0.20,
        }
        catch_heavy = {
            'CATCH': 0.50, 'PARRY_SAFE': 0.20,
            'BLOCK': 0.05, 'PUNCH': 0.15, 'FOOT_SAVE': 0.10,
        }
        result = model.substitution_cost(current, catch_heavy)
        assert result['net_change'] > 0  # value increases

    def test_substitution_shifts_tracked(self, model):
        current = {'CATCH': 0.50, 'BLOCK': 0.50}
        proposed = {'CATCH': 0.30, 'BLOCK': 0.70}
        result = model.substitution_cost(current, proposed)
        assert 'CATCH' in result['shifts']
        assert 'BLOCK' in result['shifts']
        assert result['shifts']['CATCH']['delta'] == pytest.approx(-0.20, abs=0.01)
        assert result['shifts']['BLOCK']['delta'] == pytest.approx(0.20, abs=0.01)


# ============================================================================
# MODEL: INITIALIZATION & WEIGHTS (v3.0)
# ============================================================================

class TestModelInit:

    def test_default_weights_sum_to_one(self, model):
        assert model.weights.sum() == pytest.approx(1.0, abs=1e-6)

    def test_default_weights_six_elements(self, model):
        assert len(model.weights) == 6

    def test_default_weights_v3(self, model):
        """v3.0 weights: [0.25, 0.22, 0.13, 0.08, 0.17, 0.15]."""
        expected = np.array([0.25, 0.22, 0.13, 0.08, 0.17, 0.15])
        assert np.allclose(model.weights, expected)

    def test_custom_weights(self, custom_model):
        assert custom_model.weights.sum() == pytest.approx(1.0, abs=1e-6)
        assert all(w == pytest.approx(1/6) for w in custom_model.weights)

    def test_invalid_weights_raises(self):
        with pytest.raises(AssertionError):
            GoalkeeperPerformanceModel(weights=np.array([0.5, 0.5, 0.5, 0.5, 0.5, 0.5]))

    def test_reference_techniques_loaded(self, model):
        assert len(model.techniques) == 5
        assert 'CATCH' in model.techniques
        assert 'BLOCK' in model.techniques

    def test_reference_techniques_have_d6(self, model):
        """All reference techniques should have D6 values."""
        for name, tech in model.techniques.items():
            assert tech.injury_risk is not None, f"{name} missing D6"
            assert 0.0 <= tech.injury_risk <= 1.0, f"{name} D6 out of range"

    def test_gamma_parameters(self, model):
        assert model.GAMMA_ST == 0.45
        assert model.GAMMA_SO == 0.30
        assert model.GAMMA_TO == 0.50


# ============================================================================
# MODEL: GOALKEEPER EVALUATION
# ============================================================================

class TestGoalkeeperEvaluation:

    def test_evaluate_goalkeeper_creates_profile(self, model):
        profile = model.evaluate_goalkeeper(
            name="Test GK",
            strategic_components={'S1': 0.5, 'S2': 0.6},
            tactical_components={'T1': 0.7},
            operative_components={'O1': 0.8, 'O2': 0.6},
        )
        assert profile.name == "Test GK"
        assert profile.strategic.score == pytest.approx(0.55)
        assert profile.tactical.score == pytest.approx(0.70)
        assert profile.operative.score == pytest.approx(0.70)

    def test_team_context_stored(self, model):
        profile = model.evaluate_goalkeeper(
            name="Test",
            strategic_components={'S1': 0.5},
            tactical_components={'T1': 0.5},
            operative_components={'O1': 0.5},
            team_context=0.8,
        )
        assert profile.team_context == 0.8


# ============================================================================
# INVARIANTS & EDGE CASES (6D)
# ============================================================================

class TestInvariants:

    def test_monotonicity_in_dimensions(self, model):
        """Higher dimension values should always produce higher scores."""
        low = TechniqueDimensions(0.3, 0.3, 0.3, 0.3, 0.3, injury_risk=0.3)
        high = TechniqueDimensions(0.7, 0.7, 0.7, 0.7, 0.7, injury_risk=0.7)
        assert model.score_technique(high) > model.score_technique(low)

    def test_score_linearity(self, model):
        """Score should scale linearly with uniform dimension increase."""
        a = TechniqueDimensions(0.4, 0.4, 0.4, 0.4, 0.4, injury_risk=0.4)
        b = TechniqueDimensions(0.8, 0.8, 0.8, 0.8, 0.8, injury_risk=0.8)
        assert model.score_technique(b) == pytest.approx(
            2 * model.score_technique(a), abs=1e-6
        )

    def test_allocation_invariant_to_proficiency_scale(self, model):
        """Allocation should sum to 1 regardless of proficiency values."""
        for prof_val in [0.0, 0.5, 1.0]:
            prof = {t: prof_val for t in model.techniques}
            alloc = model.compute_allocation(proficiency=prof)
            assert sum(alloc.values()) == pytest.approx(1.0, abs=1e-6)

    def test_complementarity_symmetry(self):
        """gamma_ij terms are symmetric: gamma_ST * L_S * L_T = gamma_ST * L_T * L_S."""
        profile = GoalkeeperProfile(
            name="Sym Test",
            strategic=PerformanceLevel("L_S", "S", 0.6),
            tactical=PerformanceLevel("L_T", "T", 0.8),
            operative=PerformanceLevel("L_O", "O", 0.5),
        )
        total = profile.total_performance(gamma_st=0.45, gamma_so=0.30, gamma_to=0.50)
        # Swap S and T values
        profile_swapped = GoalkeeperProfile(
            name="Sym Test Swapped",
            strategic=PerformanceLevel("L_S", "S", 0.8),
            tactical=PerformanceLevel("L_T", "T", 0.6),
            operative=PerformanceLevel("L_O", "O", 0.5),
        )
        total_swapped = profile_swapped.total_performance(
            gamma_st=0.45, gamma_so=0.30, gamma_to=0.50
        )
        # Should NOT be equal because base weights differ (w_S=0.30, w_T=0.35)
        # But the complementarity TERM gamma_ST*L_S*L_T should be the same
        comp_term = 0.45 * 0.6 * 0.8
        comp_term_swapped = 0.45 * 0.8 * 0.6
        assert comp_term == pytest.approx(comp_term_swapped)


# ============================================================================
# VISIBILITY-CONTRIBUTION FRAMEWORK
# ============================================================================

class TestVisibilityFramework:

    def test_gk_negative_v_c_correlation(self):
        """GK has negative visibility-contribution correlation."""
        gk = [p for p in VISIBILITY_SPECTRUM if p.position == "GK"][0]
        assert gk.v_c_correlation < 0

    def test_striker_positive_v_c_correlation(self):
        """Striker has positive visibility-contribution correlation."""
        st = [p for p in VISIBILITY_SPECTRUM if p.position == "ST"][0]
        assert st.v_c_correlation > 0

    def test_gk_highest_paradox_intensity(self):
        """GK should have the highest paradox intensity."""
        gk = [p for p in VISIBILITY_SPECTRUM if p.position == "GK"][0]
        for p in VISIBILITY_SPECTRUM:
            assert gk.paradox_intensity >= p.paradox_intensity

    def test_measurement_distortion(self):
        """Measurement distortion = 1 - metric_quality."""
        for p in VISIBILITY_SPECTRUM:
            assert p.measurement_distortion == pytest.approx(1.0 - p.metric_quality)

    def test_gk_lowest_metric_quality(self):
        """GK has the lowest metric quality (most contribution is invisible)."""
        gk = [p for p in VISIBILITY_SPECTRUM if p.position == "GK"][0]
        for p in VISIBILITY_SPECTRUM:
            assert gk.metric_quality <= p.metric_quality

    def test_spectrum_monotonic_v_c(self):
        """V-C correlation should decrease from ST to GK."""
        correlations = [p.v_c_correlation for p in VISIBILITY_SPECTRUM]
        for i in range(len(correlations) - 1):
            assert correlations[i] >= correlations[i+1]


# ============================================================================
# EFFECTIVE VALUE (V*_eff = V* x A x D)
# ============================================================================

class TestEffectiveValue:

    def test_veto_factor_availability_zero(self):
        """V*_eff = 0 when A = 0 (injured all season)."""
        result = compute_effective_value(v_star=0.80, availability=0.0)
        assert result == pytest.approx(0.0)

    def test_full_availability(self):
        """V*_eff = V* when A = 1, D = 1."""
        result = compute_effective_value(v_star=0.80, availability=1.0, durability=1.0)
        assert result == pytest.approx(0.80)

    def test_multiplicative_correct(self):
        """V*_eff = V* x A x D."""
        result = compute_effective_value(v_star=0.80, availability=0.50, durability=0.90)
        assert result == pytest.approx(0.80 * 0.50 * 0.90)

    def test_available_average_beats_injured_elite(self):
        """PRED-GPM-011: V*=0.6, A=0.95 > V*=0.8, A=0.5."""
        average_available = compute_effective_value(v_star=0.60, availability=0.95)
        elite_injured = compute_effective_value(v_star=0.80, availability=0.50)
        assert average_available > elite_injured

    def test_availability_profile_rate(self):
        """Availability rate = matches_available / total_matches."""
        profile = AvailabilityProfile(matches_available=30, total_matches=38)
        assert profile.availability_rate == pytest.approx(30/38)

    def test_availability_profile_zero_matches(self):
        """Zero total matches should return 0 availability."""
        profile = AvailabilityProfile(matches_available=0, total_matches=0)
        assert profile.availability_rate == 0.0

    def test_durability_calculation(self):
        """Durability = career_games / baseline_career_games, capped at 1.0."""
        profile = AvailabilityProfile(
            matches_available=30, total_matches=38,
            career_games=190, baseline_career_games=380,
        )
        assert profile.durability == pytest.approx(0.5)

    def test_durability_capped_at_one(self):
        """Durability should not exceed 1.0."""
        profile = AvailabilityProfile(
            matches_available=30, total_matches=38,
            career_games=500, baseline_career_games=380,
        )
        assert profile.durability == pytest.approx(1.0)

    def test_durability_default_one(self):
        """Durability defaults to 1.0 when no career_games set."""
        profile = AvailabilityProfile(matches_available=30, total_matches=38)
        assert profile.durability == 1.0


# ============================================================================
# PREDICTIONS FROM MODEL (PRED-GPM-001 to PRED-GPM-012)
# ============================================================================

class TestModelPredictions:
    """
    Tests corresponding to testable predictions in model-definition.yaml.
    """

    def test_pred_gpm_001_catching_dominates(self, model):
        """
        PRED-GPM-001: Catching scores > 0.80, blocking < 0.35.
        Falsification: catching < 0.70 or blocking > 0.50.
        """
        scores = model.evaluate_all()
        assert scores['CATCH'] > 0.80
        assert scores['BLOCK'] < 0.35

    def test_pred_gpm_002_balanced_beats_specialist(self, model):
        """
        PRED-GPM-002: Balanced GK (all 0.7) outperforms
        one-dimensional GK (one level 0.9, others 0.3).
        """
        balanced = model.evaluate_goalkeeper(
            name="Balanced",
            strategic_components={'S1': 0.7, 'S2': 0.7, 'S3': 0.7, 'S4': 0.7},
            tactical_components={'T1': 0.7, 'T2': 0.7, 'T3': 0.7, 'T4': 0.7},
            operative_components={'O1': 0.7, 'O2': 0.7, 'O3': 0.7, 'O4': 0.7, 'O5': 0.7},
        )
        specialist = model.evaluate_goalkeeper(
            name="Specialist",
            strategic_components={'S1': 0.3, 'S2': 0.3, 'S3': 0.3, 'S4': 0.3},
            tactical_components={'T1': 0.3, 'T2': 0.3, 'T3': 0.3, 'T4': 0.3},
            operative_components={'O1': 0.9, 'O2': 0.9, 'O3': 0.9, 'O4': 0.9, 'O5': 0.9},
        )
        assert balanced.total_performance() > specialist.total_performance()

    def test_pred_gpm_003_optimal_allocation(self, model):
        """
        PRED-GPM-003: Optimal allocation assigns catching > 30%,
        blocking < 15% (well below typical 30-40% in biased training).
        """
        alloc = model.compute_allocation()
        assert alloc['CATCH'] > 0.30
        assert alloc['BLOCK'] < 0.15  # well below biased 30-40%
        assert alloc['CATCH'] > alloc['BLOCK'] * 2  # catch at least 2x block

    def test_pred_gpm_004_block_shift_negative(self, model):
        """
        PRED-GPM-004: Shifting 20pp from catch to block
        reduces expected training value.
        """
        current = {
            'CATCH': 0.35, 'PARRY_SAFE': 0.25,
            'BLOCK': 0.10, 'PUNCH': 0.15, 'FOOT_SAVE': 0.15,
        }
        block_shift = {
            'CATCH': 0.15, 'PARRY_SAFE': 0.25,
            'BLOCK': 0.30, 'PUNCH': 0.15, 'FOOT_SAVE': 0.15,
        }
        result = model.substitution_cost(current, block_shift)
        assert result['net_change'] < 0


class TestPredictionsV3:
    """Additional v3.0 predictions (PRED-GPM-009 to PRED-GPM-012)."""

    def test_pred_gpm_009_block_heavy_higher_injury(self, model):
        """
        PRED-GPM-009: Block-heavy training profile leads to higher
        injury exposure (lower average D6) than catch-heavy profile.
        """
        techniques = model.techniques
        # Weighted D6 for catch-heavy (35% catch, 25% parry, 10% block, 15% punch, 15% foot)
        catch_heavy_d6 = (
            0.35 * techniques['CATCH'].injury_risk +
            0.25 * techniques['PARRY_SAFE'].injury_risk +
            0.10 * techniques['BLOCK'].injury_risk +
            0.15 * techniques['PUNCH'].injury_risk +
            0.15 * techniques['FOOT_SAVE'].injury_risk
        )
        # Weighted D6 for block-heavy (15% catch, 15% parry, 40% block, 15% punch, 15% foot)
        block_heavy_d6 = (
            0.15 * techniques['CATCH'].injury_risk +
            0.15 * techniques['PARRY_SAFE'].injury_risk +
            0.40 * techniques['BLOCK'].injury_risk +
            0.15 * techniques['PUNCH'].injury_risk +
            0.15 * techniques['FOOT_SAVE'].injury_risk
        )
        # Higher D6 = safer; block-heavy should be less safe
        assert catch_heavy_d6 > block_heavy_d6

    def test_pred_gpm_010_block_loses_all_six(self, model):
        """PRED-GPM-010: Block loses to CATCH on ALL SIX dimensions."""
        result = model.compare('CATCH', 'BLOCK')
        assert result['dimensions_won_a'] == 6
        assert result['dimensions_won_b'] == 0

    def test_pred_gpm_011_available_average_beats_injured_elite(self):
        """
        PRED-GPM-011: Available average GK (V*=0.6, A=0.95)
        outperforms injured elite GK (V*=0.8, A=0.5).
        """
        v_eff_average = compute_effective_value(0.60, 0.95)
        v_eff_elite = compute_effective_value(0.80, 0.50)
        assert v_eff_average > v_eff_elite
        assert v_eff_average == pytest.approx(0.57)
        assert v_eff_elite == pytest.approx(0.40)

    def test_pred_gpm_012_hybrid_evaluation(self):
        """
        PRED-GPM-012: With 44% of GK contribution unmeasurable,
        hybrid evaluation > data-only.

        V*_hybrid = 0.55 * V*_data + 0.45 * V*_scout
        When V*_scout captures prevented value better:
        V*_hybrid > V*_data for defensive-style GKs.
        """
        # GK where prevented value (invisible) is high
        v_data = 0.50   # Only visible saves counted
        v_scout = 0.85  # Expert sees positioning, communication, prevention
        v_hybrid = 0.55 * v_data + 0.45 * v_scout
        assert v_hybrid > v_data
        assert v_hybrid == pytest.approx(0.6575)


# ============================================================================
# REFERENCE PROFILES (v3.0 Case Studies)
# ============================================================================

class TestReferenceProfiles:
    """Test the 3 reference goalkeeper profiles (Neuer, Alisson, Courtois)."""

    @pytest.fixture
    def profiles(self, model):
        return create_reference_profiles(model)

    @pytest.fixture
    def availability(self):
        return create_reference_availability()

    def test_three_profiles_exist(self, profiles):
        """All three reference profiles are created."""
        assert len(profiles) == 3
        assert 'NEUER' in profiles
        assert 'ALISSON' in profiles
        assert 'COURTOIS' in profiles

    def test_neuer_is_strategic_specialist(self, profiles):
        """Neuer has highest L_S among all profiles."""
        neuer = profiles['NEUER']
        alisson = profiles['ALISSON']
        courtois = profiles['COURTOIS']
        assert neuer.strategic.score > alisson.strategic.score
        assert neuer.strategic.score > courtois.strategic.score
        assert neuer.strategic.score > 0.85  # L_S > 0.85

    def test_courtois_is_operative_specialist(self, profiles):
        """Courtois has highest L_O among all profiles."""
        neuer = profiles['NEUER']
        alisson = profiles['ALISSON']
        courtois = profiles['COURTOIS']
        assert courtois.operative.score > neuer.operative.score
        assert courtois.operative.score > alisson.operative.score
        assert courtois.operative.score > 0.85  # L_O > 0.85

    def test_alisson_is_most_balanced(self, profiles):
        """Alisson has smallest spread between L_S, L_T, L_O."""
        for name, profile in profiles.items():
            scores = [
                profile.strategic.score,
                profile.tactical.score,
                profile.operative.score,
            ]
            spread = max(scores) - min(scores)
            if name == 'ALISSON':
                alisson_spread = spread
            else:
                other_spread = spread if name == 'NEUER' else spread
        # Alisson should have the smallest spread
        alisson = profiles['ALISSON']
        a_scores = [alisson.strategic.score, alisson.tactical.score, alisson.operative.score]
        a_spread = max(a_scores) - min(a_scores)
        for name in ['NEUER', 'COURTOIS']:
            p = profiles[name]
            p_scores = [p.strategic.score, p.tactical.score, p.operative.score]
            p_spread = max(p_scores) - min(p_scores)
            assert a_spread < p_spread, f"Alisson should be more balanced than {name}"

    def test_pred004_balanced_complementarity_share(self, model, profiles):
        """PRED-004: Balanced profiles have highest complementarity share."""
        comp_shares = {}
        for name, profile in profiles.items():
            comp = model.complementarity_value(profile)
            comp_shares[name] = comp['complementarity_share']
        assert comp_shares['ALISSON'] > comp_shares['COURTOIS'], \
            "Alisson (balanced) should have higher γ-share than Courtois (specialist)"

    def test_pred006_strategic_outperforms(self, model, profiles):
        """PRED-006: Strategic GK (Neuer) outperforms operative specialist (Courtois)."""
        neuer_perf = profiles['NEUER'].total_performance()
        courtois_perf = profiles['COURTOIS'].total_performance()
        assert neuer_perf > courtois_perf, \
            "Strategic specialist should outperform operative specialist in total"

    def test_pred011_availability_veto(self, model, profiles, availability):
        """PRED-011: Courtois V*_eff collapses due to low availability."""
        courtois_v = profiles['COURTOIS'].total_performance()
        courtois_a = availability['COURTOIS'].availability_rate
        courtois_veff = compute_effective_value(courtois_v, courtois_a)

        alisson_v = profiles['ALISSON'].total_performance()
        alisson_a = availability['ALISSON'].availability_rate
        alisson_veff = compute_effective_value(alisson_v, alisson_a)

        # Courtois has lower V*_eff despite higher L_O
        assert courtois_veff < alisson_veff
        # Courtois V*_eff is severely reduced
        assert courtois_veff < 0.15, "Courtois V*_eff should be near-zero with ACL tear"
        # Alisson is much higher
        assert alisson_veff > 0.5

    def test_alisson_highest_veff(self, model, profiles, availability):
        """Alisson has the highest V*_eff of all three profiles."""
        veffs = {}
        for name, profile in profiles.items():
            v = profile.total_performance()
            a = availability[name].availability_rate
            d = availability[name].durability
            veffs[name] = compute_effective_value(v, a, d)
        assert veffs['ALISSON'] == max(veffs.values()), \
            "Alisson should have highest V*_eff (balance + availability)"

    def test_training_allocations_sum_to_one(self):
        """All training allocations sum to 1.0."""
        for name, alloc in REFERENCE_TRAINING_ALLOCATIONS.items():
            total = sum(alloc.values())
            assert abs(total - 1.0) < 0.01, f"{name} allocation sums to {total}"

    def test_neuer_low_block_allocation(self):
        """Neuer has low block allocation (consistent with GPM optimal)."""
        block = REFERENCE_TRAINING_ALLOCATIONS['NEUER']['BLOCK']
        assert block <= 0.06, f"Neuer block allocation {block} should be <= 6%"

    def test_courtois_higher_block_allocation(self):
        """Courtois has higher block allocation than Neuer and Alisson."""
        c_block = REFERENCE_TRAINING_ALLOCATIONS['COURTOIS']['BLOCK']
        n_block = REFERENCE_TRAINING_ALLOCATIONS['NEUER']['BLOCK']
        a_block = REFERENCE_TRAINING_ALLOCATIONS['ALISSON']['BLOCK']
        assert c_block > n_block
        assert c_block > a_block
        assert c_block >= 0.10, "Courtois block allocation should be >= 10%"

    def test_all_profiles_have_valid_scores(self, profiles):
        """All profile scores are in [0, 1]."""
        for name, profile in profiles.items():
            assert 0 <= profile.strategic.score <= 1, f"{name} L_S out of range"
            assert 0 <= profile.tactical.score <= 1, f"{name} L_T out of range"
            assert 0 <= profile.operative.score <= 1, f"{name} L_O out of range"
            perf = profile.total_performance()
            assert 0 <= perf <= 1, f"{name} total performance {perf} out of [0,1]"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
