#!/usr/bin/env python3
"""
ODE Behavior Dynamics Simulator (Layer 1)
==========================================

Simulates organizational behavior change using a 6-state ODE system:

    dU/dt  = Σ(α_i · I_i) - Σ(δ_i · U_i) + Σ(γ_ij · U_i · U_j)  [Utility]
    dA/dt  = β · U · A · (1-A) · D - (1-U) · A · 0.02              [Adoption]
    dR/dt  = -ρ · R · (M + 0.1) + r · setback_rate                  [Resistance]
    dH/dt  = η · A · (1-H) - 0.01 · (1-A) · H                      [Habit]
    dM/dt  = μ · A · U - friction · M                                [Momentum]
    dD/dt  = θ · learning_events · (1-D) - forgetting · D            [Decision Cap.]

Parameters are loaded from customer ODE parameter YAML files.

Usage:
    python ode_simulator.py --customer zindel-united --project ZIN003
    python ode_simulator.py --customer zindel-united --project ZIN003 --months 12
    python ode_simulator.py --customer zindel-united --project ZIN003 --counterfactual INT-ZIN-007
    python ode_simulator.py --customer zindel-united --project ZIN003 --json
    python ode_simulator.py --demo

Author: EBF Framework (Layer 1 - Formal Computation)
Date: 2026-02-16
Protocol: TLA Layer 1 (virus-susceptibility = 0.0)
"""

import json
import argparse
import sys
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. Install: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class UtilityParams:
    """Growth and decay rates for 6 FEPSDE utility dimensions."""
    alpha_F: float = 0.0   # Financial growth
    alpha_E: float = 0.0   # Emotional growth
    alpha_P: float = 0.0   # Physical/Effort growth
    alpha_S: float = 0.0   # Social growth
    alpha_D: float = 0.0   # Development growth
    alpha_X: float = 0.0   # Existential growth
    delta_F: float = 0.0   # Financial decay
    delta_E: float = 0.0   # Emotional decay
    delta_P: float = 0.0   # Physical decay
    delta_S: float = 0.0   # Social decay
    delta_D: float = 0.0   # Development decay
    delta_X: float = 0.0   # Existential decay

    @property
    def growth_rates(self) -> List[float]:
        return [self.alpha_F, self.alpha_E, self.alpha_P,
                self.alpha_S, self.alpha_D, self.alpha_X]

    @property
    def decay_rates(self) -> List[float]:
        return [self.delta_F, self.delta_E, self.delta_P,
                self.delta_S, self.delta_D, self.delta_X]


@dataclass
class Complementarities:
    """Pairwise interaction terms between utility dimensions."""
    gamma_SX: float = 0.0   # Social x Existential
    gamma_DX: float = 0.0   # Development x Existential
    gamma_FS: float = 0.0   # Financial x Social (often negative!)
    gamma_SD: float = 0.0   # Social x Development
    gamma_FP: float = 0.0   # Financial x Physical
    gamma_ED: float = 0.0   # Emotional x Development

    def total_interaction(self, u_dims: Dict[str, float]) -> float:
        """Compute total complementarity contribution."""
        F = u_dims.get("F", 0)
        E = u_dims.get("E", 0)
        P = u_dims.get("P", 0)
        S = u_dims.get("S", 0)
        D = u_dims.get("D", 0)
        X = u_dims.get("X", 0)
        return (self.gamma_SX * S * X +
                self.gamma_DX * D * X +
                self.gamma_FS * F * S +
                self.gamma_SD * S * D +
                self.gamma_FP * F * P +
                self.gamma_ED * E * D)


@dataclass
class ProcessDynamics:
    """Process parameters for adoption, resistance, habit, momentum."""
    beta_adoption: float = 0.5       # S-curve adoption rate
    rho_resistance_decay: float = 0.04  # Resistance decay
    r_setback_sensitivity: float = 0.15  # Setback rebound
    eta_habit_formation: float = 0.45   # Monthly habit formation
    mu_momentum: float = 0.08        # Momentum build-up
    friction: float = 0.05           # Momentum friction
    # Decision Capability (from Diagnosis v2)
    theta_learning: float = 0.15     # Learning rate for D
    d_forgetting: float = 0.03       # Forgetting rate for D


@dataclass
class ContextElasticities:
    """Psi-dimension elasticities that amplify utilities."""
    psi_I: float = 0.8   # Institutional
    psi_S: float = 1.2   # Social
    psi_C: float = 0.6   # Cognitive
    psi_K: float = 1.1   # Cultural
    psi_E: float = 0.7   # Economic
    psi_T: float = 0.9   # Temporal
    psi_M: float = 0.85  # Material
    psi_F: float = 0.75  # Physical

    @property
    def mean_elasticity(self) -> float:
        vals = [self.psi_I, self.psi_S, self.psi_C, self.psi_K,
                self.psi_E, self.psi_T, self.psi_M, self.psi_F]
        return sum(vals) / len(vals)


@dataclass
class InitialConditions:
    """Starting values for all 6 state variables."""
    U_0: float = 0.15          # Initial utility
    Adoption_0: float = 0.05   # Initial adoption
    Resistance_0: float = 0.60 # Initial resistance
    Habit_0: float = 0.0       # Initial habit
    Momentum_0: float = 0.10   # Initial momentum
    Decision_0: float = 0.30   # Initial decision capability


@dataclass
class StageThresholds:
    """Readiness thresholds for phase transitions."""
    theta_1: float = 0.25  # Kick-off -> Implementation
    theta_2: float = 0.55  # Implementation -> Stabilization
    theta_3: float = 0.80  # Stabilization -> Transfer


@dataclass
class ODEConfig:
    """Complete ODE configuration loaded from YAML."""
    model_id: str = ""
    model_name: str = ""
    utility: UtilityParams = field(default_factory=UtilityParams)
    complementarities: Complementarities = field(default_factory=Complementarities)
    process: ProcessDynamics = field(default_factory=ProcessDynamics)
    context: ContextElasticities = field(default_factory=ContextElasticities)
    initial: InitialConditions = field(default_factory=InitialConditions)
    thresholds: StageThresholds = field(default_factory=StageThresholds)
    # Intervention effects (which interventions are active)
    active_interventions: List[str] = field(default_factory=list)
    # Generalized intervention effects for counterfactual analysis
    # Each key is an intervention ID (e.g. "INT-ZIN-007"), value is a dict with:
    #   "name": human-readable name
    #   "effects_when_removed": dict of parameter adjustments when excluded
    #     - Keys ending in _multiplier: multiply the parameter (e.g. theta_learning_multiplier: 0.3)
    #     - Keys ending in _override: set the value directly (e.g. D_0_override: 0.10)
    #   "interpretation": text explanation
    intervention_effects: Dict[str, Dict] = field(default_factory=dict)


@dataclass
class ODEState:
    """State vector at a given time step."""
    t: float         # Time (months)
    U: float         # Total Utility
    A: float         # Adoption
    R: float         # Resistance
    H: float         # Habit Strength
    M: float         # Momentum
    D: float         # Decision Capability
    stage: str = ""  # Current phase

    def readiness(self) -> float:
        """Composite readiness = weighted average."""
        return 0.3 * self.A + 0.2 * self.H + 0.2 * (1 - self.R) + 0.15 * self.M + 0.15 * self.D

    def to_dict(self) -> Dict:
        return {
            "t": round(self.t, 1),
            "U": round(self.U, 4),
            "A": round(self.A, 4),
            "R": round(self.R, 4),
            "H": round(self.H, 4),
            "M": round(self.M, 4),
            "D": round(self.D, 4),
            "readiness": round(self.readiness(), 4),
            "stage": self.stage,
        }


@dataclass
class SimulationResult:
    """Complete simulation output."""
    config: ODEConfig
    trajectory: List[ODEState]
    months: int
    dt: float
    # Derived metrics
    final_adoption: float = 0.0
    final_resistance: float = 0.0
    final_decision_capability: float = 0.0
    max_momentum: float = 0.0
    stage_transitions: Dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        monthly = [s.to_dict() for s in self.trajectory
                   if s.t == int(s.t) or s.t == 0]
        return {
            "model_id": self.config.model_id,
            "model_name": self.config.model_name,
            "months": self.months,
            "dt": self.dt,
            "summary": {
                "final_adoption": round(self.final_adoption, 4),
                "final_resistance": round(self.final_resistance, 4),
                "final_decision_capability": round(self.final_decision_capability, 4),
                "max_momentum": round(self.max_momentum, 4),
                "stage_transitions": {k: round(v, 1) for k, v in self.stage_transitions.items()},
            },
            "trajectory_monthly": monthly,
            "active_interventions": self.config.active_interventions,
            "provenance": {
                "layer": 1,
                "script": "scripts/ode_simulator.py",
                "method": "Euler integration",
                "susceptibility": 0.0,
            },
        }


# =============================================================================
# YAML LOADER
# =============================================================================

def load_ode_config(customer: str, project: str,
                    base_path: Optional[Path] = None) -> ODEConfig:
    """Load ODE parameters from customer YAML file.

    Expects: data/customers/{customer}/kontextvektoren/{project}_ODE_parameters.yaml
    """
    if base_path is None:
        base_path = Path(__file__).parent.parent / "data" / "customers"

    yaml_path = base_path / customer / "kontextvektoren" / f"{project}_ODE_parameters.yaml"

    if not yaml_path.exists():
        raise FileNotFoundError(f"ODE parameters not found: {yaml_path}")

    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    config = ODEConfig()

    # Metadata
    meta = data.get("metadata", {})
    config.model_id = meta.get("model_id", "")
    config.model_name = meta.get("model_name", "")

    # Utility growth rates
    ugr = data.get("utility_growth_rates", {})
    config.utility = UtilityParams(
        alpha_F=ugr.get("alpha_F", {}).get("posterior_mean", 0),
        alpha_E=ugr.get("alpha_E", {}).get("posterior_mean", 0),
        alpha_P=ugr.get("alpha_P", {}).get("posterior_mean", 0),
        alpha_S=ugr.get("alpha_S", {}).get("posterior_mean", 0),
        alpha_D=ugr.get("alpha_D", {}).get("posterior_mean", 0),
        alpha_X=ugr.get("alpha_X", {}).get("posterior_mean", 0),
    )

    # Utility decay rates
    udr = data.get("utility_decay_rates", {})
    config.utility.delta_F = udr.get("delta_F", {}).get("posterior_mean", 0)
    config.utility.delta_E = udr.get("delta_E", {}).get("posterior_mean", 0)
    config.utility.delta_P = udr.get("delta_P", {}).get("posterior_mean", 0)
    config.utility.delta_S = udr.get("delta_S", {}).get("posterior_mean", 0)
    config.utility.delta_D = udr.get("delta_D", {}).get("posterior_mean", 0)
    config.utility.delta_X = udr.get("delta_X", {}).get("posterior_mean", 0)

    # Complementarities
    comp = data.get("complementarities", {})
    config.complementarities = Complementarities(
        gamma_SX=comp.get("gamma_SX", {}).get("posterior_mean", 0),
        gamma_DX=comp.get("gamma_DX", {}).get("posterior_mean", 0),
        gamma_FS=comp.get("gamma_FS", {}).get("posterior_mean", 0),
        gamma_SD=comp.get("gamma_SD", {}).get("posterior_mean", 0),
        gamma_FP=comp.get("gamma_FP", {}).get("posterior_mean", 0),
        gamma_ED=comp.get("gamma_ED", {}).get("posterior_mean", 0),
    )

    # Process dynamics
    proc = data.get("process_dynamics", {})
    config.process = ProcessDynamics(
        beta_adoption=proc.get("beta_adoption", {}).get("posterior_mean", 0.5),
        rho_resistance_decay=proc.get("rho_resistance_decay", {}).get("posterior_mean", 0.04),
        r_setback_sensitivity=proc.get("r_setback_sensitivity", {}).get("posterior_mean", 0.15),
        eta_habit_formation=proc.get("eta_habit_formation", {}).get("monthly_equivalent",
                                     proc.get("eta_habit_formation", {}).get("posterior_mean", 0.015) * 30),
        mu_momentum=proc.get("mu_momentum", {}).get("posterior_mean", 0.08),
        friction=proc.get("friction", {}).get("posterior_mean", 0.05),
        theta_learning=proc.get("theta_learning", {}).get("posterior_mean", 0.15),
        d_forgetting=proc.get("d_forgetting", {}).get("posterior_mean", 0.03),
    )

    # Context elasticities
    ctx = data.get("context_elasticities", {})
    config.context = ContextElasticities(
        psi_I=ctx.get("alpha_psi_I", {}).get("posterior_mean", 0.8),
        psi_S=ctx.get("alpha_psi_S", {}).get("posterior_mean", 1.2),
        psi_C=ctx.get("alpha_psi_C", {}).get("posterior_mean", 0.6),
        psi_K=ctx.get("alpha_psi_K", {}).get("posterior_mean", 1.1),
        psi_E=ctx.get("alpha_psi_E", {}).get("posterior_mean", 0.7),
        psi_T=ctx.get("alpha_psi_T", {}).get("posterior_mean", 0.9),
        psi_M=ctx.get("alpha_psi_M", {}).get("posterior_mean", 0.85),
        psi_F=ctx.get("alpha_psi_F", {}).get("posterior_mean", 0.75),
    )

    # Initial conditions
    ic = data.get("initial_conditions", {})
    config.initial = InitialConditions(
        U_0=ic.get("U_0", {}).get("posterior_mean", 0.15),
        Adoption_0=ic.get("Adoption_0", {}).get("posterior_mean", 0.05),
        Resistance_0=ic.get("Resistance_0", {}).get("posterior_mean", 0.60),
        Habit_0=ic.get("Habit_0", {}).get("posterior_mean", 0.0),
        Momentum_0=ic.get("Momentum_0", {}).get("posterior_mean", 0.10),
        Decision_0=ic.get("Decision_0", {}).get("posterior_mean", 0.30),
    )

    # Stage thresholds
    st = data.get("stage_thresholds", {})
    config.thresholds = StageThresholds(
        theta_1=st.get("theta_1", {}).get("posterior_mean", 0.25),
        theta_2=st.get("theta_2", {}).get("posterior_mean", 0.55),
        theta_3=st.get("theta_3", {}).get("posterior_mean", 0.80),
    )

    # Intervention effects (for generalized counterfactual analysis)
    ie = data.get("intervention_effects", {})
    for int_id, effect_data in ie.items():
        config.intervention_effects[int_id] = {
            "name": effect_data.get("name", int_id),
            "effects_when_removed": effect_data.get("effects_when_removed", {}),
            "interpretation": effect_data.get("interpretation", ""),
        }

    return config


# =============================================================================
# ODE INTEGRATION (EULER)
# =============================================================================

def _determine_stage(readiness: float, thresholds: StageThresholds) -> str:
    """Determine current phase from readiness score."""
    if readiness >= thresholds.theta_3:
        return "Transfer"
    elif readiness >= thresholds.theta_2:
        return "Stabilisierung"
    elif readiness >= thresholds.theta_1:
        return "Umsetzung"
    else:
        return "Kick-off"


def simulate(config: ODEConfig, months: int = 8, dt: float = 0.1,
             exclude_interventions: Optional[List[str]] = None) -> SimulationResult:
    """Run Euler integration of the 6-state ODE system.

    Args:
        config: ODE configuration with all parameters
        months: Simulation duration in months
        dt: Time step (months)
        exclude_interventions: List of intervention IDs to exclude (counterfactual)

    Returns:
        SimulationResult with full trajectory
    """
    excluded = set(exclude_interventions or [])

    # Initialize state
    U = config.initial.U_0
    A = config.initial.Adoption_0
    R = config.initial.Resistance_0
    H = config.initial.Habit_0
    M = config.initial.Momentum_0
    D = config.initial.Decision_0

    # Utility sub-dimensions (start equal)
    u_F = U / 6
    u_E = U / 6
    u_P = U / 6
    u_S = U / 6
    u_D = U / 6
    u_X = U / 6

    # Context amplification
    psi_amp = config.context.mean_elasticity

    # Parameters
    p = config.process
    ut = config.utility
    comp = config.complementarities

    # Generalized intervention effects (counterfactual support)
    # Apply effects_when_removed for each excluded intervention
    learning_events_mult = 1.0
    for int_id, effects in config.intervention_effects.items():
        if int_id in excluded:
            removal = effects.get("effects_when_removed", {})
            # Pre-simulation parameter multipliers
            if "theta_learning_multiplier" in removal:
                p.theta_learning *= removal["theta_learning_multiplier"]
            if "rho_resistance_multiplier" in removal:
                p.rho_resistance_decay *= removal["rho_resistance_multiplier"]
            if "beta_adoption_multiplier" in removal:
                p.beta_adoption *= removal["beta_adoption_multiplier"]
            if "mu_momentum_multiplier" in removal:
                p.mu_momentum *= removal["mu_momentum_multiplier"]
            if "alpha_S_multiplier" in removal:
                ut.alpha_S *= removal["alpha_S_multiplier"]
            if "alpha_D_multiplier" in removal:
                ut.alpha_D *= removal["alpha_D_multiplier"]
            if "alpha_E_multiplier" in removal:
                ut.alpha_E *= removal["alpha_E_multiplier"]
            # Pre-simulation value overrides
            if "D_0_override" in removal:
                D = removal["D_0_override"]
            if "A_0_override" in removal:
                A = removal["A_0_override"]
            if "R_0_override" in removal:
                R = removal["R_0_override"]
            # In-loop multipliers (accumulated across excluded interventions)
            if "learning_events_multiplier" in removal:
                learning_events_mult *= removal["learning_events_multiplier"]

    trajectory = []
    max_momentum = M
    stage_transitions = {}
    prev_stage = ""

    steps = int(months / dt) + 1
    for step in range(steps):
        t = step * dt

        # Determine stage
        state = ODEState(t=t, U=U, A=A, R=R, H=H, M=M, D=D)
        stage = _determine_stage(state.readiness(), config.thresholds)
        state.stage = stage

        # Track stage transitions
        if stage != prev_stage and prev_stage != "":
            stage_transitions[f"{prev_stage} -> {stage}"] = t
        prev_stage = stage

        trajectory.append(state)
        max_momentum = max(max_momentum, M)

        # --- ODE RIGHT-HAND SIDES ---

        # Utility sub-dimensions dynamics
        u_dims = {"F": u_F, "E": u_E, "P": u_P, "S": u_S, "D": u_D, "X": u_X}
        gamma_total = comp.total_interaction(u_dims)

        # Growth (intervention-driven, context-amplified)
        intervention_active = 1.0 if t > 0 else 0.5  # Ramp up
        net_growth = (
            ut.alpha_F * intervention_active +
            ut.alpha_E * intervention_active +
            ut.alpha_P * intervention_active * 0.5 +  # Effort grows slower
            ut.alpha_S * intervention_active +
            ut.alpha_D * intervention_active +
            ut.alpha_X * intervention_active
        ) * psi_amp

        # Decay
        net_decay = (
            ut.delta_F * u_F +
            ut.delta_E * u_E +
            ut.delta_P * u_P +
            ut.delta_S * u_S +
            ut.delta_D * u_D +
            ut.delta_X * u_X
        )

        # dU/dt
        dU = net_growth - net_decay + gamma_total * 0.1
        dU = dU * (1 - R * 0.5)  # Resistance dampens utility growth

        # dA/dt (S-curve with decision capability coupling)
        dA = p.beta_adoption * U * A * (1 - A) * D - (1 - U) * A * 0.02

        # dR/dt (resistance decay + setback rebounds)
        setback_rate = 0.02 if t < 2 else 0.01  # Fewer setbacks over time
        dR = -p.rho_resistance_decay * R * (M + 0.1) + p.r_setback_sensitivity * setback_rate

        # dH/dt (habit formation)
        dH = p.eta_habit_formation * A * (1 - H) * dt - 0.01 * (1 - A) * H

        # dM/dt (momentum)
        success_events = A * U * 0.5  # Success proportional to adoption x utility
        dM = p.mu_momentum * success_events - p.friction * M

        # dD/dt (decision capability)
        learning_events = 0.3 if t > 0 else 0.1  # Monthly learning events
        learning_events *= learning_events_mult   # Counterfactual adjustment
        dD = p.theta_learning * learning_events * (1 - D) - p.d_forgetting * D

        # --- EULER UPDATE ---
        U = max(0, min(1, U + dU * dt))
        A = max(0, min(1, A + dA * dt))
        R = max(0, min(1, R + dR * dt))
        H = max(0, min(1, H + dH * dt))
        M = max(0, min(1, M + dM * dt))
        D = max(0, min(1, D + dD * dt))

        # Update sub-dimensions proportionally
        if U > 0:
            total_alpha = sum(ut.growth_rates)
            if total_alpha > 0:
                u_F = U * ut.alpha_F / total_alpha
                u_E = U * ut.alpha_E / total_alpha
                u_P = U * ut.alpha_P / total_alpha
                u_S = U * ut.alpha_S / total_alpha
                u_D = U * ut.alpha_D / total_alpha
                u_X = U * ut.alpha_X / total_alpha

    # Build result
    result = SimulationResult(
        config=config,
        trajectory=trajectory,
        months=months,
        dt=dt,
        final_adoption=trajectory[-1].A,
        final_resistance=trajectory[-1].R,
        final_decision_capability=trajectory[-1].D,
        max_momentum=max_momentum,
        stage_transitions=stage_transitions,
    )

    return result


# =============================================================================
# COUNTERFACTUAL ANALYSIS
# =============================================================================

def counterfactual(config: ODEConfig, months: int = 8, dt: float = 0.1,
                   exclude: Optional[List[str]] = None) -> Dict:
    """Run baseline vs. counterfactual and compute deltas.

    Args:
        config: ODE configuration
        months: Simulation duration
        dt: Time step
        exclude: Interventions to exclude in counterfactual

    Returns:
        Dict with baseline, counterfactual, and deltas
    """
    # Baseline (all interventions active)
    baseline = simulate(config, months=months, dt=dt)

    # Counterfactual (excluded interventions removed)
    # Need fresh config since simulate modifies process params
    config_cf = load_ode_config_from_dict(config)
    cf = simulate(config_cf, months=months, dt=dt, exclude_interventions=exclude)

    delta_adoption = baseline.final_adoption - cf.final_adoption
    delta_resistance = cf.final_resistance - baseline.final_resistance
    delta_decision = baseline.final_decision_capability - cf.final_decision_capability

    return {
        "baseline": {
            "final_adoption": round(baseline.final_adoption, 4),
            "final_resistance": round(baseline.final_resistance, 4),
            "final_decision_capability": round(baseline.final_decision_capability, 4),
        },
        "counterfactual": {
            "excluded": exclude or [],
            "final_adoption": round(cf.final_adoption, 4),
            "final_resistance": round(cf.final_resistance, 4),
            "final_decision_capability": round(cf.final_decision_capability, 4),
        },
        "delta": {
            "adoption_pp": round(delta_adoption * 100, 1),
            "resistance_pp": round(delta_resistance * 100, 1),
            "decision_capability_pp": round(delta_decision * 100, 1),
        },
        "interpretation": (
            f"Removing {exclude} reduces adoption by {delta_adoption*100:.1f}pp "
            f"and decision capability by {delta_decision*100:.1f}pp."
        ),
        "provenance": {
            "layer": 1,
            "script": "scripts/ode_simulator.py",
            "method": "Euler counterfactual comparison",
            "susceptibility": 0.0,
        },
    }


def load_ode_config_from_dict(config: ODEConfig) -> ODEConfig:
    """Create a fresh copy of ODEConfig (since simulate may modify it)."""
    import copy
    return copy.deepcopy(config)


# =============================================================================
# DISPLAY
# =============================================================================

def print_trajectory_table(result: SimulationResult) -> None:
    """Print a human-readable trajectory table (monthly snapshots)."""
    print(f"\n{'='*85}")
    print(f"  ODE SIMULATION: {result.config.model_name}")
    print(f"  Model: {result.config.model_id} | Duration: {result.months} months | dt={result.dt}")
    print(f"{'='*85}")
    print(f"  {'Mo':>3} | {'U':>6} | {'A':>6} | {'R':>6} | {'H':>6} | {'M':>6} | {'D':>6} | {'Ready':>6} | Stage")
    print(f"  {'-'*3}-+-{'-'*6}-+-{'-'*6}-+-{'-'*6}-+-{'-'*6}-+-{'-'*6}-+-{'-'*6}-+-{'-'*6}-+--------")

    for state in result.trajectory:
        if state.t == int(state.t):
            t_int = int(state.t)
            print(f"  {t_int:3d} | {state.U:6.3f} | {state.A:6.3f} | {state.R:6.3f} | "
                  f"{state.H:6.3f} | {state.M:6.3f} | {state.D:6.3f} | "
                  f"{state.readiness():6.3f} | {state.stage}")

    print(f"{'='*85}")
    print(f"\n  KEY METRICS:")
    print(f"  Final Adoption:           {result.final_adoption*100:5.1f}%")
    print(f"  Final Resistance:         {result.final_resistance*100:5.1f}%")
    print(f"  Final Decision Cap.:      {result.final_decision_capability*100:5.1f}%")
    print(f"  Max Momentum:             {result.max_momentum:5.3f}")

    if result.stage_transitions:
        print(f"\n  STAGE TRANSITIONS:")
        for transition, time in result.stage_transitions.items():
            print(f"    {transition}: Month {time:.1f}")

    print()


def print_counterfactual(cf_result: Dict) -> None:
    """Print counterfactual comparison."""
    b = cf_result["baseline"]
    c = cf_result["counterfactual"]
    d = cf_result["delta"]

    print(f"\n{'='*70}")
    print(f"  COUNTERFACTUAL ANALYSIS")
    print(f"  Excluded: {c['excluded']}")
    print(f"{'='*70}")
    print(f"  {'Metric':<25} | {'Baseline':>10} | {'Without':>10} | {'Delta':>10}")
    print(f"  {'-'*25}-+-{'-'*10}-+-{'-'*10}-+-{'-'*10}")
    print(f"  {'Adoption':<25} | {b['final_adoption']*100:9.1f}% | {c['final_adoption']*100:9.1f}% | {d['adoption_pp']:+9.1f}pp")
    print(f"  {'Resistance':<25} | {b['final_resistance']*100:9.1f}% | {c['final_resistance']*100:9.1f}% | {d['resistance_pp']:+9.1f}pp")
    print(f"  {'Decision Capability':<25} | {b['final_decision_capability']*100:9.1f}% | {c['final_decision_capability']*100:9.1f}% | {d['decision_capability_pp']:+9.1f}pp")
    print(f"{'='*70}")
    print(f"\n  {cf_result['interpretation']}")
    print()


# =============================================================================
# DEMO (Zindel ZIN003)
# =============================================================================

def demo_zindel() -> SimulationResult:
    """Run the Zindel ZIN003 Kreislaufwirtschaft demo."""
    try:
        config = load_ode_config("zindel-united", "ZIN003")
    except FileNotFoundError:
        print("WARNING: Zindel YAML not found, using hardcoded demo parameters",
              file=sys.stderr)
        config = _zindel_hardcoded()

    print("\n  ZINDEL UNITED — ZIN003 Kreislaufwirtschaft")
    print("  8. Generation Bauunternehmen | 500 MA | CHF 160 Mio.")
    print("  Kern-Diagnose: Barriere = Entscheidungsfaehigkeit unter Unsicherheit")

    result = simulate(config, months=8, dt=0.1)
    print_trajectory_table(result)

    # Counterfactual: Without INT-ZIN-007
    config2 = load_ode_config_from_dict(config)
    cf = counterfactual(config2, months=8, dt=0.1, exclude=["INT-ZIN-007"])
    print_counterfactual(cf)

    return result


def _zindel_hardcoded() -> ODEConfig:
    """Hardcoded Zindel parameters (fallback if YAML not found)."""
    return ODEConfig(
        model_id="ZIN003-ODE-v1.0",
        model_name="Kreislaufwirtschaft Behavior Dynamics",
        utility=UtilityParams(
            alpha_F=0.10, alpha_E=0.15, alpha_P=0.04,
            alpha_S=0.15, alpha_D=0.10, alpha_X=0.10,
            delta_F=0.03, delta_E=0.08, delta_P=0.02,
            delta_S=0.06, delta_D=0.04, delta_X=0.02,
        ),
        complementarities=Complementarities(
            gamma_SX=0.35, gamma_DX=0.40, gamma_FS=-0.15,
            gamma_SD=0.25, gamma_FP=0.20, gamma_ED=0.30,
        ),
        process=ProcessDynamics(
            beta_adoption=0.50, rho_resistance_decay=0.04,
            r_setback_sensitivity=0.15, eta_habit_formation=0.45,
            mu_momentum=0.08, friction=0.05,
            theta_learning=0.15, d_forgetting=0.03,
        ),
        context=ContextElasticities(
            psi_I=0.80, psi_S=1.20, psi_C=0.60, psi_K=1.10,
            psi_E=0.70, psi_T=0.90, psi_M=0.85, psi_F=0.75,
        ),
        initial=InitialConditions(
            U_0=0.15, Adoption_0=0.05, Resistance_0=0.60,
            Habit_0=0.0, Momentum_0=0.10, Decision_0=0.30,
        ),
        thresholds=StageThresholds(theta_1=0.25, theta_2=0.55, theta_3=0.80),
        intervention_effects={
            "INT-ZIN-007": {
                "name": "Entscheidungsarchitektur",
                "effects_when_removed": {
                    "theta_learning_multiplier": 0.3,
                    "D_0_override": 0.10,
                },
                "interpretation": "Without structured decision framework, learning rate drops to 30% and decision capability starts much lower",
            },
            "INT-ZIN-008": {
                "name": "Lern-Loops & Reflexionszyklen",
                "effects_when_removed": {
                    "learning_events_multiplier": 0.5,
                },
                "interpretation": "Without reflection cycles, learning events are halved",
            },
        },
    )


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="ODE Behavior Dynamics Simulator (Layer 1)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python ode_simulator.py --demo
  python ode_simulator.py --customer zindel-united --project ZIN003
  python ode_simulator.py --customer zindel-united --project ZIN003 --months 12
  python ode_simulator.py --customer zindel-united --project ZIN003 --counterfactual INT-ZIN-007
  python ode_simulator.py --customer zindel-united --project ZIN003 --json
        """
    )
    parser.add_argument("--demo", action="store_true",
                        help="Run Zindel ZIN003 demo")
    parser.add_argument("--customer", type=str,
                        help="Customer directory name (e.g. zindel-united)")
    parser.add_argument("--project", type=str,
                        help="Project ID (e.g. ZIN003)")
    parser.add_argument("--months", type=int, default=8,
                        help="Simulation duration in months (default: 8)")
    parser.add_argument("--dt", type=float, default=0.1,
                        help="Time step in months (default: 0.1)")
    parser.add_argument("--counterfactual", type=str, nargs="+",
                        help="Intervention IDs to exclude (counterfactual analysis)")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON instead of table")

    args = parser.parse_args()

    if args.demo:
        result = demo_zindel()
        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        return

    if not args.customer or not args.project:
        parser.error("--customer and --project required (or use --demo)")

    config = load_ode_config(args.customer, args.project)

    if args.counterfactual:
        cf = counterfactual(config, months=args.months, dt=args.dt,
                            exclude=args.counterfactual)
        if args.json:
            print(json.dumps(cf, indent=2))
        else:
            # Run baseline for table display
            config2 = load_ode_config_from_dict(config)
            result = simulate(config2, months=args.months, dt=args.dt)
            print_trajectory_table(result)
            print_counterfactual(cf)
    else:
        result = simulate(config, months=args.months, dt=args.dt)
        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            print_trajectory_table(result)


if __name__ == "__main__":
    main()
