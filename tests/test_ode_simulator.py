#!/usr/bin/env python3
"""
Tests for ODE Behavior Dynamics Simulator.

Tests cover:
1. YAML loading from customer data
2. Euler integration correctness
3. State variable bounds [0, 1]
4. Counterfactual analysis
5. Stage transitions
6. Zindel ZIN003 specific results
"""

import sys
import json
import unittest
from pathlib import Path
from unittest.mock import patch

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from ode_simulator import (
    ODEConfig, ODEState, UtilityParams, Complementarities,
    ProcessDynamics, ContextElasticities, InitialConditions,
    StageThresholds, SimulationResult,
    simulate, counterfactual, load_ode_config,
    _determine_stage, _zindel_hardcoded,
)


class TestODEState(unittest.TestCase):
    """Test ODEState data class."""

    def test_readiness_calculation(self):
        """Readiness is weighted average of A, H, 1-R, M, D."""
        state = ODEState(t=0, U=0.5, A=1.0, R=0.0, H=1.0, M=1.0, D=1.0)
        # 0.3*1 + 0.2*1 + 0.2*(1-0) + 0.15*1 + 0.15*1 = 1.0
        self.assertAlmostEqual(state.readiness(), 1.0, places=4)

    def test_readiness_zero(self):
        """All state at worst values -> low readiness."""
        state = ODEState(t=0, U=0, A=0, R=1.0, H=0, M=0, D=0)
        # 0.3*0 + 0.2*0 + 0.2*(1-1) + 0.15*0 + 0.15*0 = 0
        self.assertAlmostEqual(state.readiness(), 0.0, places=4)

    def test_to_dict(self):
        """State serializes correctly."""
        state = ODEState(t=1.0, U=0.5, A=0.1, R=0.6, H=0.0, M=0.1, D=0.3, stage="Kick-off")
        d = state.to_dict()
        self.assertEqual(d["t"], 1.0)
        self.assertEqual(d["stage"], "Kick-off")
        self.assertIn("readiness", d)


class TestStageTransitions(unittest.TestCase):
    """Test phase determination."""

    def test_kickoff(self):
        t = StageThresholds(theta_1=0.25, theta_2=0.55, theta_3=0.80)
        self.assertEqual(_determine_stage(0.10, t), "Kick-off")

    def test_umsetzung(self):
        t = StageThresholds(theta_1=0.25, theta_2=0.55, theta_3=0.80)
        self.assertEqual(_determine_stage(0.30, t), "Umsetzung")

    def test_stabilisierung(self):
        t = StageThresholds(theta_1=0.25, theta_2=0.55, theta_3=0.80)
        self.assertEqual(_determine_stage(0.60, t), "Stabilisierung")

    def test_transfer(self):
        t = StageThresholds(theta_1=0.25, theta_2=0.55, theta_3=0.80)
        self.assertEqual(_determine_stage(0.85, t), "Transfer")

    def test_boundary_exact(self):
        t = StageThresholds(theta_1=0.25, theta_2=0.55, theta_3=0.80)
        self.assertEqual(_determine_stage(0.25, t), "Umsetzung")
        self.assertEqual(_determine_stage(0.55, t), "Stabilisierung")
        self.assertEqual(_determine_stage(0.80, t), "Transfer")


class TestComplementarities(unittest.TestCase):
    """Test complementarity interaction computation."""

    def test_zero_inputs(self):
        comp = Complementarities(gamma_SX=0.35, gamma_DX=0.40)
        result = comp.total_interaction({"F": 0, "E": 0, "P": 0, "S": 0, "D": 0, "X": 0})
        self.assertAlmostEqual(result, 0.0, places=6)

    def test_positive_complementarity(self):
        comp = Complementarities(gamma_SX=0.35)
        result = comp.total_interaction({"F": 0, "E": 0, "P": 0, "S": 1.0, "D": 0, "X": 1.0})
        self.assertAlmostEqual(result, 0.35, places=4)

    def test_negative_crowding_out(self):
        """Financial x Social should be negative (crowding-out)."""
        comp = Complementarities(gamma_FS=-0.15)
        result = comp.total_interaction({"F": 1.0, "E": 0, "P": 0, "S": 1.0, "D": 0, "X": 0})
        self.assertAlmostEqual(result, -0.15, places=4)


class TestSimulation(unittest.TestCase):
    """Test ODE simulation core."""

    def setUp(self):
        """Use Zindel hardcoded config for tests."""
        self.config = _zindel_hardcoded()

    def test_simulation_runs(self):
        """Simulation completes without errors."""
        result = simulate(self.config, months=4, dt=0.1)
        self.assertIsInstance(result, SimulationResult)
        self.assertGreater(len(result.trajectory), 0)

    def test_state_bounds(self):
        """All state variables stay in [0, 1]."""
        result = simulate(self.config, months=12, dt=0.1)
        for state in result.trajectory:
            self.assertGreaterEqual(state.U, 0.0, f"U<0 at t={state.t}")
            self.assertLessEqual(state.U, 1.0, f"U>1 at t={state.t}")
            self.assertGreaterEqual(state.A, 0.0, f"A<0 at t={state.t}")
            self.assertLessEqual(state.A, 1.0, f"A>1 at t={state.t}")
            self.assertGreaterEqual(state.R, 0.0, f"R<0 at t={state.t}")
            self.assertLessEqual(state.R, 1.0, f"R>1 at t={state.t}")
            self.assertGreaterEqual(state.H, 0.0, f"H<0 at t={state.t}")
            self.assertLessEqual(state.H, 1.0, f"H>1 at t={state.t}")
            self.assertGreaterEqual(state.M, 0.0, f"M<0 at t={state.t}")
            self.assertLessEqual(state.M, 1.0, f"M>1 at t={state.t}")
            self.assertGreaterEqual(state.D, 0.0, f"D<0 at t={state.t}")
            self.assertLessEqual(state.D, 1.0, f"D>1 at t={state.t}")

    def test_adoption_grows(self):
        """Adoption should grow over 8 months."""
        result = simulate(self.config, months=8, dt=0.1)
        self.assertGreater(result.final_adoption, self.config.initial.Adoption_0)

    def test_resistance_decays(self):
        """Resistance should decrease over time."""
        result = simulate(self.config, months=8, dt=0.1)
        self.assertLess(result.final_resistance, self.config.initial.Resistance_0)

    def test_decision_capability_grows(self):
        """Decision capability should grow from initial 0.30."""
        result = simulate(self.config, months=8, dt=0.1)
        self.assertGreater(result.final_decision_capability, self.config.initial.Decision_0)

    def test_initial_state_correct(self):
        """First trajectory point matches initial conditions."""
        result = simulate(self.config, months=4, dt=0.1)
        first = result.trajectory[0]
        self.assertAlmostEqual(first.U, self.config.initial.U_0, places=4)
        self.assertAlmostEqual(first.A, self.config.initial.Adoption_0, places=4)
        self.assertAlmostEqual(first.R, self.config.initial.Resistance_0, places=4)

    def test_trajectory_length(self):
        """Trajectory has correct number of steps."""
        result = simulate(self.config, months=4, dt=0.1)
        expected = int(4 / 0.1) + 1  # 41 steps
        self.assertEqual(len(result.trajectory), expected)

    def test_to_dict_serializable(self):
        """Result serializes to valid JSON."""
        result = simulate(self.config, months=4, dt=0.1)
        d = result.to_dict()
        json_str = json.dumps(d)
        self.assertIsInstance(json_str, str)
        self.assertIn("summary", d)
        self.assertIn("trajectory_monthly", d)
        self.assertIn("provenance", d)
        self.assertEqual(d["provenance"]["layer"], 1)
        self.assertEqual(d["provenance"]["susceptibility"], 0.0)


class TestCounterfactual(unittest.TestCase):
    """Test counterfactual analysis."""

    def setUp(self):
        self.config = _zindel_hardcoded()

    def test_counterfactual_runs(self):
        """Counterfactual completes without errors."""
        cf = counterfactual(self.config, months=8, dt=0.1,
                            exclude=["INT-ZIN-007"])
        self.assertIn("baseline", cf)
        self.assertIn("counterfactual", cf)
        self.assertIn("delta", cf)

    def test_removing_int007_reduces_adoption(self):
        """Removing Entscheidungsarchitektur should reduce adoption."""
        cf = counterfactual(self.config, months=8, dt=0.1,
                            exclude=["INT-ZIN-007"])
        self.assertGreater(cf["delta"]["adoption_pp"], 0,
                           "Removing INT-ZIN-007 should reduce adoption")

    def test_removing_int007_reduces_decision_capability(self):
        """Removing Entscheidungsarchitektur should reduce D."""
        cf = counterfactual(self.config, months=8, dt=0.1,
                            exclude=["INT-ZIN-007"])
        self.assertGreater(cf["delta"]["decision_capability_pp"], 0,
                           "Removing INT-ZIN-007 should reduce decision capability")

    def test_counterfactual_provenance(self):
        """Counterfactual has correct provenance."""
        cf = counterfactual(self.config, months=8, dt=0.1,
                            exclude=["INT-ZIN-007"])
        self.assertEqual(cf["provenance"]["layer"], 1)
        self.assertEqual(cf["provenance"]["susceptibility"], 0.0)


class TestYAMLLoader(unittest.TestCase):
    """Test YAML parameter loading."""

    def test_load_zindel(self):
        """Load real Zindel ZIN003 parameters from YAML."""
        try:
            config = load_ode_config("zindel-united", "ZIN003")
        except FileNotFoundError:
            self.skipTest("Zindel YAML not available")

        self.assertEqual(config.model_id, "ZIN003-ODE-v1.0")
        self.assertAlmostEqual(config.utility.alpha_F, 0.10, places=2)
        self.assertAlmostEqual(config.utility.alpha_S, 0.15, places=2)
        self.assertAlmostEqual(config.complementarities.gamma_SX, 0.35, places=2)
        self.assertAlmostEqual(config.complementarities.gamma_FS, -0.15, places=2)
        self.assertAlmostEqual(config.initial.Resistance_0, 0.60, places=2)

    def test_load_nonexistent_raises(self):
        """Loading from nonexistent customer raises FileNotFoundError."""
        with self.assertRaises(FileNotFoundError):
            load_ode_config("nonexistent-customer", "XXX999")

    def test_yaml_vs_hardcoded_match(self):
        """YAML-loaded and hardcoded Zindel parameters should match."""
        try:
            yaml_config = load_ode_config("zindel-united", "ZIN003")
        except FileNotFoundError:
            self.skipTest("Zindel YAML not available")

        hc = _zindel_hardcoded()

        self.assertAlmostEqual(yaml_config.utility.alpha_F, hc.utility.alpha_F, places=2)
        self.assertAlmostEqual(yaml_config.utility.alpha_S, hc.utility.alpha_S, places=2)
        self.assertAlmostEqual(yaml_config.complementarities.gamma_SX,
                               hc.complementarities.gamma_SX, places=2)
        self.assertAlmostEqual(yaml_config.process.beta_adoption,
                               hc.process.beta_adoption, places=2)


class TestGeneralizedCounterfactual(unittest.TestCase):
    """Test generalized (YAML-driven) counterfactual analysis."""

    def test_custom_intervention_effects(self):
        """Custom intervention_effects work in counterfactual."""
        config = _zindel_hardcoded()
        # Add a custom intervention
        config.intervention_effects["INT-CUSTOM-001"] = {
            "name": "Custom Intervention",
            "effects_when_removed": {
                "beta_adoption_multiplier": 0.5,
            },
        }
        cf = counterfactual(config, months=8, dt=0.1,
                            exclude=["INT-CUSTOM-001"])
        self.assertGreater(cf["delta"]["adoption_pp"], 0,
                           "Removing custom intervention should reduce adoption")

    def test_removing_int008_reduces_decision(self):
        """Removing Lern-Loops (INT-ZIN-008) should reduce decision capability."""
        config = _zindel_hardcoded()
        cf = counterfactual(config, months=8, dt=0.1,
                            exclude=["INT-ZIN-008"])
        self.assertGreater(cf["delta"]["decision_capability_pp"], 0,
                           "Removing INT-ZIN-008 should reduce decision capability")

    def test_multiple_interventions_excluded(self):
        """Excluding multiple interventions has larger effect than one."""
        config = _zindel_hardcoded()
        cf_one = counterfactual(config, months=8, dt=0.1,
                                exclude=["INT-ZIN-007"])
        config2 = _zindel_hardcoded()
        cf_both = counterfactual(config2, months=8, dt=0.1,
                                 exclude=["INT-ZIN-007", "INT-ZIN-008"])
        self.assertGreater(cf_both["delta"]["decision_capability_pp"],
                           cf_one["delta"]["decision_capability_pp"],
                           "Excluding both should have larger effect")

    def test_unknown_intervention_no_effect(self):
        """Excluding an intervention not in effects dict has no impact."""
        config = _zindel_hardcoded()
        baseline = simulate(config, months=8, dt=0.1)
        config2 = _zindel_hardcoded()
        cf_result = simulate(config2, months=8, dt=0.1,
                             exclude_interventions=["INT-NONEXISTENT-999"])
        self.assertAlmostEqual(baseline.final_adoption, cf_result.final_adoption, places=6)

    def test_yaml_intervention_effects_loaded(self):
        """Intervention effects are loaded from YAML."""
        try:
            config = load_ode_config("zindel-united", "ZIN003")
        except FileNotFoundError:
            self.skipTest("Zindel YAML not available")
        self.assertIn("INT-ZIN-007", config.intervention_effects)
        self.assertIn("INT-ZIN-008", config.intervention_effects)
        effects_007 = config.intervention_effects["INT-ZIN-007"]
        self.assertAlmostEqual(
            effects_007["effects_when_removed"]["theta_learning_multiplier"], 0.3)
        self.assertAlmostEqual(
            effects_007["effects_when_removed"]["D_0_override"], 0.10)

    def test_rms_intervention_effects_loaded(self):
        """RMS intervention effects are loaded from YAML."""
        try:
            config = load_ode_config("ringier-medien-schweiz", "RMS001")
        except FileNotFoundError:
            self.skipTest("RMS YAML not available")
        self.assertIn("INT-RMS-001", config.intervention_effects)
        self.assertIn("INT-RMS-004", config.intervention_effects)
        effects_001 = config.intervention_effects["INT-RMS-001"]
        self.assertAlmostEqual(
            effects_001["effects_when_removed"]["alpha_D_multiplier"], 0.6)

    def test_rms_counterfactual_runs(self):
        """RMS counterfactual analysis completes without errors."""
        try:
            config = load_ode_config("ringier-medien-schweiz", "RMS001")
        except FileNotFoundError:
            self.skipTest("RMS YAML not available")
        cf = counterfactual(config, months=12, dt=0.1,
                            exclude=["INT-RMS-001"])
        self.assertIn("baseline", cf)
        self.assertIn("counterfactual", cf)
        self.assertGreater(cf["delta"]["adoption_pp"], 0,
                           "Removing INT-RMS-001 should reduce adoption")


class TestContextElasticities(unittest.TestCase):
    """Test context elasticity calculations."""

    def test_mean_elasticity(self):
        ctx = ContextElasticities(
            psi_I=0.8, psi_S=1.2, psi_C=0.6, psi_K=1.1,
            psi_E=0.7, psi_T=0.9, psi_M=0.85, psi_F=0.75
        )
        expected = (0.8 + 1.2 + 0.6 + 1.1 + 0.7 + 0.9 + 0.85 + 0.75) / 8
        self.assertAlmostEqual(ctx.mean_elasticity, expected, places=4)

    def test_zindel_social_strongest(self):
        """Zindel's social context elasticity should be the strongest."""
        ctx = ContextElasticities(
            psi_I=0.8, psi_S=1.2, psi_C=0.6, psi_K=1.1,
            psi_E=0.7, psi_T=0.9, psi_M=0.85, psi_F=0.75
        )
        vals = [ctx.psi_I, ctx.psi_S, ctx.psi_C, ctx.psi_K,
                ctx.psi_E, ctx.psi_T, ctx.psi_M, ctx.psi_F]
        self.assertEqual(max(vals), ctx.psi_S)


if __name__ == "__main__":
    unittest.main()
