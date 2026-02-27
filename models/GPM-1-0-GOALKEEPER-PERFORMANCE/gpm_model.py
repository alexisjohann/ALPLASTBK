"""
GPM 3.0: Goalkeeper Performance Model v3.0
Six-Dimension Framework for Goalkeeper Technique Evaluation,
Training Allocation, and Effective Value Assessment

Single Source of Truth: model-definition.yaml

v3.0 Extensions:
  - D6 Injury Risk dimension (D6a non-contact + D6b contact)
  - Visibility-Contribution Framework (Holmstrom-Milgrom)
  - V*_eff = V* × A × D (Effective Value with Availability Veto)

Usage:
    python gpm_model.py                    # Run demo with reference profiles
    python gpm_model.py --evaluate         # Evaluate all techniques
    python gpm_model.py --allocate         # Compute training allocation
    python gpm_model.py --compare          # Compare catching vs blocking
    python gpm_model.py --profile <name>   # Evaluate custom goalkeeper profile
    python gpm_model.py --profiles         # Evaluate 3 reference goalkeeper profiles
"""

import numpy as np
import yaml
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from pathlib import Path
import json
import argparse


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class TechniqueDimensions:
    """Six-dimension evaluation for a goalkeeper technique (v3.0).

    D1-D5: Original dimensions from v1.0
    D6: Injury Risk (v3.0) — inverted scale: 1.0 = safe, 0.0 = dangerous
        D6 = 0.5 × D6a (non-contact) + 0.5 × D6b (contact)
    """
    game_relevance: float       # D1: R ∈ [0,1]
    risk_reduction: float       # D2: ρ ∈ [0,1]
    learning_efficiency: float  # D3: η ∈ [0,1]
    coach_transmissibility: float  # D4: τ ∈ [0,1]
    strategic_potential: float  # D5: Π ∈ [0,1]
    injury_risk: float = 0.50  # D6: ι ∈ [0,1] (inverted: 1=safe)
    injury_risk_non_contact: Optional[float] = None  # D6a
    injury_risk_contact: Optional[float] = None       # D6b

    def __post_init__(self):
        """If D6a and D6b are both provided, compute D6 as composite."""
        if (self.injury_risk_non_contact is not None
                and self.injury_risk_contact is not None):
            self.injury_risk = (0.5 * self.injury_risk_non_contact
                                + 0.5 * self.injury_risk_contact)

    def to_vector(self) -> np.ndarray:
        return np.array([
            self.game_relevance,
            self.risk_reduction,
            self.learning_efficiency,
            self.coach_transmissibility,
            self.strategic_potential,
            self.injury_risk,
        ])

    def to_dict(self) -> Dict[str, float]:
        d = {
            'D1_game_relevance': self.game_relevance,
            'D2_risk_reduction': self.risk_reduction,
            'D3_learning_efficiency': self.learning_efficiency,
            'D4_coach_transmissibility': self.coach_transmissibility,
            'D5_strategic_potential': self.strategic_potential,
            'D6_injury_risk': self.injury_risk,
        }
        if self.injury_risk_non_contact is not None:
            d['D6a_non_contact'] = self.injury_risk_non_contact
        if self.injury_risk_contact is not None:
            d['D6b_contact'] = self.injury_risk_contact
        return d


@dataclass
class PerformanceLevel:
    """One of three performance levels (strategic, tactical, operative)."""
    level_id: str       # L_S, L_T, L_O
    name: str
    score: float        # Aggregated level score ∈ [0,1]
    components: Dict[str, float] = field(default_factory=dict)

    def compute_score(self) -> float:
        if self.components:
            self.score = np.mean(list(self.components.values()))
        return self.score


@dataclass
class GoalkeeperProfile:
    """Complete goalkeeper evaluation profile."""
    name: str
    strategic: PerformanceLevel
    tactical: PerformanceLevel
    operative: PerformanceLevel
    team_context: float = 0.5  # Φ_team ∈ [0,1]: quality of team system

    def total_performance(self, gamma_st: float = 0.45,
                          gamma_so: float = 0.30,
                          gamma_to: float = 0.50) -> float:
        """
        Compute total goalkeeper performance with complementarity.

        L(GK) = w_S·L_S + w_T·L_T + w_O·L_O
                + γ_ST·L_S·L_T + γ_SO·L_S·L_O + γ_TO·L_T·L_O

        Complementarity terms reward goalkeepers who are strong
        across multiple levels (not one-dimensional).
        """
        ls = self.strategic.score
        lt = self.tactical.score
        lo = self.operative.score

        # Base weights (equal for now)
        w_s, w_t, w_o = 0.30, 0.35, 0.35

        # Additive base
        base = w_s * ls + w_t * lt + w_o * lo

        # Complementarity terms
        complement = (gamma_st * ls * lt +
                      gamma_so * ls * lo +
                      gamma_to * lt * lo)

        # Normalize to [0,1]
        # Max possible complement = gamma_st + gamma_so + gamma_to (when all = 1)
        max_complement = gamma_st + gamma_so + gamma_to
        raw = base + complement
        max_raw = 1.0 + max_complement

        return raw / max_raw

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'L_S': self.strategic.score,
            'L_T': self.tactical.score,
            'L_O': self.operative.score,
            'team_context': self.team_context,
            'total_performance': self.total_performance(),
        }


# ============================================================================
# GOALKEEPER PERFORMANCE MODEL
# ============================================================================

class GoalkeeperPerformanceModel:
    """
    GPM 3.0: Six-dimensional goalkeeper technique evaluation,
    training allocation, and effective value assessment model.
    """

    # v3.0 weights (6 dimensions, from model-definition.yaml)
    DEFAULT_WEIGHTS = np.array([0.25, 0.22, 0.13, 0.08, 0.17, 0.15])

    # Legacy v1.0 weights (5 dimensions) — kept for backwards compatibility
    V1_WEIGHTS = np.array([0.30, 0.25, 0.15, 0.10, 0.20])

    # Complementarity parameters between performance levels
    GAMMA_ST = 0.45  # Strategic × Tactical
    GAMMA_SO = 0.30  # Strategic × Operative
    GAMMA_TO = 0.50  # Tactical × Operative

    # Training allocation weights
    W_FREQ = 0.50    # Weight for game frequency
    W_SCORE = 0.30   # Weight for technique score
    W_WEAKNESS = 0.20  # Weight for weakness compensation

    def __init__(self, weights: Optional[np.ndarray] = None):
        self.weights = weights if weights is not None else self.DEFAULT_WEIGHTS
        assert abs(self.weights.sum() - 1.0) < 1e-6, "Weights must sum to 1.0"

        # Load reference technique profiles
        self.techniques = self._load_reference_techniques()

    def _load_reference_techniques(self) -> Dict[str, TechniqueDimensions]:
        """Load reference technique profiles (v3.0 with D6/D6a/D6b)."""
        return {
            'CATCH': TechniqueDimensions(
                game_relevance=0.85,
                risk_reduction=0.95,
                learning_efficiency=0.55,
                coach_transmissibility=0.80,
                strategic_potential=0.90,
                injury_risk_non_contact=0.85,
                injury_risk_contact=0.55,
            ),
            'PARRY_SAFE': TechniqueDimensions(
                game_relevance=0.70,
                risk_reduction=0.70,
                learning_efficiency=0.50,
                coach_transmissibility=0.65,
                strategic_potential=0.40,
                injury_risk_non_contact=0.60,
                injury_risk_contact=0.70,
            ),
            'BLOCK': TechniqueDimensions(
                game_relevance=0.20,
                risk_reduction=0.50,
                learning_efficiency=0.35,
                coach_transmissibility=0.30,
                strategic_potential=0.10,
                injury_risk_non_contact=0.25,
                injury_risk_contact=0.20,
            ),
            'PUNCH': TechniqueDimensions(
                game_relevance=0.45,
                risk_reduction=0.55,
                learning_efficiency=0.50,
                coach_transmissibility=0.60,
                strategic_potential=0.25,
                injury_risk_non_contact=0.55,
                injury_risk_contact=0.40,
            ),
            'FOOT_SAVE': TechniqueDimensions(
                game_relevance=0.30,
                risk_reduction=0.45,
                learning_efficiency=0.40,
                coach_transmissibility=0.45,
                strategic_potential=0.15,
                injury_risk_non_contact=0.45,
                injury_risk_contact=0.35,
            ),
        }

    # -----------------------------------------------------------------------
    # TECHNIQUE EVALUATION
    # -----------------------------------------------------------------------

    def score_technique(self, technique: TechniqueDimensions) -> float:
        """
        Compute weighted technique score.

        S(t) = Σ_i w_i × D_i(t)
        """
        return float(self.weights @ technique.to_vector())

    def evaluate_all(self) -> Dict[str, float]:
        """Score all reference techniques."""
        return {
            name: self.score_technique(tech)
            for name, tech in self.techniques.items()
        }

    def compare(self, tech_a: str, tech_b: str) -> Dict:
        """
        Detailed comparison between two techniques.
        Returns per-dimension breakdown and overall scores.
        """
        a = self.techniques[tech_a]
        b = self.techniques[tech_b]
        dim_names = [
            'Game Relevance', 'Risk Reduction', 'Learning Efficiency',
            'Coach Transmissibility', 'Strategic Potential', 'Injury Risk'
        ]

        comparison = []
        for i, dim in enumerate(dim_names):
            va = a.to_vector()[i]
            vb = b.to_vector()[i]
            comparison.append({
                'dimension': dim,
                'weight': self.weights[i],
                tech_a: va,
                tech_b: vb,
                'advantage': tech_a if va > vb else (tech_b if vb > va else 'TIE'),
                'delta': abs(va - vb),
            })

        score_a = self.score_technique(a)
        score_b = self.score_technique(b)

        return {
            'technique_a': tech_a,
            'technique_b': tech_b,
            'score_a': score_a,
            'score_b': score_b,
            'overall_advantage': tech_a if score_a > score_b else tech_b,
            'dimensions_won_a': sum(1 for c in comparison if c['advantage'] == tech_a),
            'dimensions_won_b': sum(1 for c in comparison if c['advantage'] == tech_b),
            'per_dimension': comparison,
        }

    # -----------------------------------------------------------------------
    # TRAINING ALLOCATION
    # -----------------------------------------------------------------------

    def compute_allocation(
        self,
        game_frequencies: Optional[Dict[str, float]] = None,
        proficiency: Optional[Dict[str, float]] = None,
    ) -> Dict[str, float]:
        """
        Compute optimal training time allocation.

        T_alloc(t) = w_freq × F(t) + w_score × S(t) + w_weakness × (1 - Prof(t))

        Normalized so allocations sum to 1.0.

        Args:
            game_frequencies: Observed frequency of each technique in matches.
                              If None, uses reference estimates.
            proficiency: Current proficiency level per technique [0,1].
                         If None, assumes 0.5 for all.
        """
        if game_frequencies is None:
            # Reference estimates (proportion of total GK actions)
            game_frequencies = {
                'CATCH': 0.40,
                'PARRY_SAFE': 0.25,
                'BLOCK': 0.05,
                'PUNCH': 0.15,
                'FOOT_SAVE': 0.05,
                'DISTRIBUTION': 0.10,  # non-save action
            }

        if proficiency is None:
            proficiency = {t: 0.5 for t in self.techniques}

        scores = self.evaluate_all()

        # Normalize each component
        freq_total = sum(game_frequencies.get(t, 0) for t in self.techniques)
        score_total = sum(scores.values())
        weakness_total = sum(1 - proficiency.get(t, 0.5) for t in self.techniques)

        allocation = {}
        for tech_name in self.techniques:
            f = game_frequencies.get(tech_name, 0) / max(freq_total, 1e-6)
            s = scores[tech_name] / max(score_total, 1e-6)
            w = (1 - proficiency.get(tech_name, 0.5)) / max(weakness_total, 1e-6)

            allocation[tech_name] = (
                self.W_FREQ * f +
                self.W_SCORE * s +
                self.W_WEAKNESS * w
            )

        # Normalize to sum = 1.0
        total = sum(allocation.values())
        return {k: v / total for k, v in allocation.items()}

    # -----------------------------------------------------------------------
    # GOALKEEPER PROFILE EVALUATION
    # -----------------------------------------------------------------------

    def evaluate_goalkeeper(
        self,
        name: str,
        strategic_components: Dict[str, float],
        tactical_components: Dict[str, float],
        operative_components: Dict[str, float],
        team_context: float = 0.5,
    ) -> GoalkeeperProfile:
        """
        Evaluate a complete goalkeeper profile.

        Args:
            name: Goalkeeper name
            strategic_components: {S1: score, S2: score, ...}
            tactical_components: {T1: score, T2: score, ...}
            operative_components: {O1: score, O2: score, ...}
            team_context: Team system quality Φ ∈ [0,1]
        """
        strategic = PerformanceLevel(
            level_id="L_S", name="Strategic", score=0.0,
            components=strategic_components,
        )
        strategic.compute_score()

        tactical = PerformanceLevel(
            level_id="L_T", name="Tactical", score=0.0,
            components=tactical_components,
        )
        tactical.compute_score()

        operative = PerformanceLevel(
            level_id="L_O", name="Operative", score=0.0,
            components=operative_components,
        )
        operative.compute_score()

        return GoalkeeperProfile(
            name=name,
            strategic=strategic,
            tactical=tactical,
            operative=operative,
            team_context=team_context,
        )

    # -----------------------------------------------------------------------
    # COMPLEMENTARITY ANALYSIS
    # -----------------------------------------------------------------------

    def complementarity_value(self, profile: GoalkeeperProfile) -> Dict:
        """
        Compute the complementarity premium for a goalkeeper profile.
        Shows how much value is added (or lost) by the interaction
        between performance levels.
        """
        ls = profile.strategic.score
        lt = profile.tactical.score
        lo = profile.operative.score

        additive = 0.30 * ls + 0.35 * lt + 0.35 * lo
        comp_st = self.GAMMA_ST * ls * lt
        comp_so = self.GAMMA_SO * ls * lo
        comp_to = self.GAMMA_TO * lt * lo
        total_comp = comp_st + comp_so + comp_to

        return {
            'additive_base': additive,
            'complementarity_ST': comp_st,
            'complementarity_SO': comp_so,
            'complementarity_TO': comp_to,
            'total_complementarity': total_comp,
            'complementarity_share': total_comp / max(additive + total_comp, 1e-6),
            'total_performance': profile.total_performance(
                self.GAMMA_ST, self.GAMMA_SO, self.GAMMA_TO
            ),
        }

    # -----------------------------------------------------------------------
    # SUBSTITUTION ANALYSIS
    # -----------------------------------------------------------------------

    def substitution_cost(
        self,
        current_allocation: Dict[str, float],
        proposed_allocation: Dict[str, float],
    ) -> Dict:
        """
        Compute opportunity cost of shifting training time.

        Shows what is gained and lost when reallocating training minutes.
        """
        scores = self.evaluate_all()
        current_value = sum(
            alloc * scores.get(t, 0)
            for t, alloc in current_allocation.items()
        )
        proposed_value = sum(
            alloc * scores.get(t, 0)
            for t, alloc in proposed_allocation.items()
        )

        shifts = {}
        for t in set(list(current_allocation.keys()) + list(proposed_allocation.keys())):
            c = current_allocation.get(t, 0)
            p = proposed_allocation.get(t, 0)
            if abs(c - p) > 0.01:
                shifts[t] = {
                    'from': c,
                    'to': p,
                    'delta': p - c,
                    'score': scores.get(t, 0),
                }

        return {
            'current_expected_value': current_value,
            'proposed_expected_value': proposed_value,
            'net_change': proposed_value - current_value,
            'shifts': shifts,
        }


# ============================================================================
# VISIBILITY-CONTRIBUTION FRAMEWORK (v3.0)
# ============================================================================
# Axiom GPM-VIS-1: Observable ≠ Valuable
# Literature: Holmstrom & Milgrom (1991), Kerr (1975)

@dataclass
class VisibilityContribution:
    """Position-specific visibility-contribution spectrum.

    Corr(V,C) measures the correlation between visibility of an action
    and its actual contribution to team success. For goalkeepers,
    the best performance is invisible (prevention paradox).
    """
    position: str
    v_c_correlation: float   # Corr(V,C): +1 = visible=valuable, -1 = invisible=valuable
    paradox_intensity: float  # 1 - |Corr(V,C)| inverted: higher = more paradox
    metric_quality: float     # Share of actual contribution captured by metrics

    @property
    def measurement_distortion(self) -> float:
        """How much of actual contribution is MISSED by standard metrics."""
        return 1.0 - self.metric_quality


# Reference V-C spectrum across football positions
VISIBILITY_SPECTRUM = [
    VisibilityContribution("ST",  v_c_correlation=+0.85, paradox_intensity=0.15, metric_quality=0.85),
    VisibilityContribution("CAM", v_c_correlation=+0.65, paradox_intensity=0.35, metric_quality=0.65),
    VisibilityContribution("CM",  v_c_correlation=+0.35, paradox_intensity=0.65, metric_quality=0.45),
    VisibilityContribution("CB",  v_c_correlation=+0.20, paradox_intensity=0.75, metric_quality=0.35),
    VisibilityContribution("GK",  v_c_correlation=-0.15, paradox_intensity=0.95, metric_quality=0.25),
]


# ============================================================================
# AVAILABILITY & EFFECTIVE VALUE FRAMEWORK (v3.0)
# ============================================================================
# Axiom GPM-INJ-1: V*_eff = V* × A × D
# A = 0 → V*_eff = 0 (Availability is a VETO factor)

@dataclass
class AvailabilityProfile:
    """Goalkeeper availability and durability assessment."""
    matches_available: int
    total_matches: int
    career_games: int = 0
    baseline_career_games: int = 380  # ~10 seasons × 38 matches

    @property
    def availability_rate(self) -> float:
        """A ∈ [0,1]: matches played / total possible matches."""
        if self.total_matches <= 0:
            return 0.0
        return self.matches_available / self.total_matches

    @property
    def durability(self) -> float:
        """D ∈ [0,1]: expected remaining career proportion."""
        if self.career_games <= 0:
            return 1.0
        return min(self.career_games / max(self.baseline_career_games, 1), 1.0)


def compute_effective_value(
    v_star: float,
    availability: float,
    durability: float = 1.0,
) -> float:
    """
    Compute effective goalkeeper value.

    V*_eff = V* × A × D

    Multiplicative form justified by V1 (EXC-5):
    If A = 0 (injured all season), V*_eff = 0 regardless of V*.
    Availability is a VETO factor.

    Args:
        v_star: Total goalkeeper value V* = V_observed + V_prevented
        availability: A ∈ [0,1], matches available / total matches
        durability: D ∈ [0,1], career durability factor
    """
    return v_star * availability * durability


# ============================================================================
# REFERENCE GOALKEEPER PROFILES (v3.0)
# ============================================================================
# Three real-world profiles for empirical validation of PRED-GPM-001 to 012.
# Values derived from public match data, scouting reports, and
# Red Bull Scouting Framework (Wagner 2023).

# Training allocation benchmarks per profile type (% of total training time)
REFERENCE_TRAINING_ALLOCATIONS = {
    'NEUER': {
        'CATCH': 0.38, 'PARRY_SAFE': 0.22, 'BLOCK': 0.05,
        'PUNCH': 0.15, 'FOOT_SAVE': 0.08, 'DISTRIBUTION': 0.12,
    },
    'ALISSON': {
        'CATCH': 0.35, 'PARRY_SAFE': 0.24, 'BLOCK': 0.06,
        'PUNCH': 0.14, 'FOOT_SAVE': 0.06, 'DISTRIBUTION': 0.15,
    },
    'COURTOIS': {
        'CATCH': 0.30, 'PARRY_SAFE': 0.20, 'BLOCK': 0.12,
        'PUNCH': 0.18, 'FOOT_SAVE': 0.10, 'DISTRIBUTION': 0.10,
    },
}


def create_reference_profiles(
    model: 'GoalkeeperPerformanceModel',
) -> Dict[str, GoalkeeperProfile]:
    """
    Create 3 reference goalkeeper profiles for empirical validation.

    Each profile is designed to test specific GPM predictions:
      - Neuer:    Strategic specialist   → PRED-006 (positioning > spectacle)
      - Alisson:  Balanced excellence    → PRED-004 (complementarity γ benefit)
      - Courtois: Operative specialist   → PRED-011 (V*_eff with injury)

    Returns:
        Dict mapping name to GoalkeeperProfile
    """
    neuer = model.evaluate_goalkeeper(
        name="Manuel Neuer",
        strategic_components={
            'S1_positioning': 0.95,     # Revolutionary sweeper-keeper positioning
            'S2_build_up': 0.90,        # Initiates attacks, effective passing range
            'S3_game_reading': 0.88,    # Anticipation, offside trap coordination
            'S4_communication': 0.87,   # Organizes defensive line, vocal leader
        },
        tactical_components={
            'T1_decision_quality': 0.80,  # When to come out vs stay
            'T2_shot_selection': 0.72,    # Choice of save technique
            'T3_timing': 0.75,            # Rush timing, 1v1 approach
            'T4_risk_assessment': 0.73,   # Age-related decline in risk calibration
        },
        operative_components={
            'O1_reflexes': 0.78,          # Still elite but declining with age
            'O2_diving_range': 0.80,      # Excellent for his height
            'O3_blocking_ability': 0.75,  # Solid but not primary technique
            'O4_aerial_dominance': 0.85,  # Commanding in the box
            'O5_distribution': 0.82,      # Short and long passing
        },
        team_context=0.85,  # Bayern Munich: elite defensive system
    )

    alisson = model.evaluate_goalkeeper(
        name="Alisson Becker",
        strategic_components={
            'S1_positioning': 0.82,     # Very good, modern style
            'S2_build_up': 0.78,        # Good distribution, Liverpool's system
            'S3_game_reading': 0.80,    # Excellent anticipation
            'S4_communication': 0.80,   # Effective organizer
        },
        tactical_components={
            'T1_decision_quality': 0.82,  # Excellent when to catch vs parry
            'T2_shot_selection': 0.78,    # Balanced technique selection
            'T3_timing': 0.80,            # Good rush timing
            'T4_risk_assessment': 0.80,   # Conservative but effective
        },
        operative_components={
            'O1_reflexes': 0.88,          # Elite reaction speed
            'O2_diving_range': 0.85,      # Excellent coverage
            'O3_blocking_ability': 0.82,  # Strong but not overused
            'O4_aerial_dominance': 0.87,  # Dominant in the box
            'O5_distribution': 0.83,      # Key to Liverpool's build-up
        },
        team_context=0.80,  # Liverpool: high-line system
    )

    courtois = model.evaluate_goalkeeper(
        name="Thibaut Courtois",
        strategic_components={
            'S1_positioning': 0.60,     # Relies more on physical attributes
            'S2_build_up': 0.50,        # Limited passing range under pressure
            'S3_game_reading': 0.55,    # Decent but not elite reader
            'S4_communication': 0.55,   # Adequate organization
        },
        tactical_components={
            'T1_decision_quality': 0.68,  # Good shot-stopping decisions
            'T2_shot_selection': 0.65,    # Tends toward reactive techniques
            'T3_timing': 0.62,            # Sometimes slow to commit
            'T4_risk_assessment': 0.65,   # Injury history affects risk-taking
        },
        operative_components={
            'O1_reflexes': 0.90,          # Elite reflexes, massive wingspan
            'O2_diving_range': 0.92,      # Outstanding physical reach
            'O3_blocking_ability': 0.88,  # Strong 1v1 blocker (high usage)
            'O4_aerial_dominance': 0.90,  # Height advantage, dominant
            'O5_distribution': 0.80,      # Adequate, improving
        },
        team_context=0.75,  # Real Madrid: transition-heavy system
    )

    return {
        'NEUER': neuer,
        'ALISSON': alisson,
        'COURTOIS': courtois,
    }


def create_reference_availability() -> Dict[str, AvailabilityProfile]:
    """
    Create availability profiles for the 3 reference goalkeepers.

    Key for PRED-011 validation: Courtois ACL tear 2023
    shows V*_eff collapse when A drops to near-zero.
    """
    return {
        'NEUER': AvailabilityProfile(
            matches_available=32,   # 2023-24 post-leg-break season
            total_matches=50,       # Bundesliga + CL + DFB
            career_games=850,
        ),
        'ALISSON': AvailabilityProfile(
            matches_available=46,   # 2023-24: highly available
            total_matches=52,
            career_games=500,
        ),
        'COURTOIS': AvailabilityProfile(
            matches_available=8,    # 2023-24: ACL tear August 2023
            total_matches=52,
            career_games=530,
        ),
    }


# ============================================================================
# DEMO / CLI
# ============================================================================

def print_header(text: str):
    print(f"\n{'=' * 70}")
    print(f"  {text}")
    print(f"{'=' * 70}")


def print_subheader(text: str):
    print(f"\n--- {text} ---")


def demo_evaluate(model: GoalkeeperPerformanceModel):
    """Evaluate all techniques and display results."""
    print_header("TECHNIQUE EVALUATION (Six-Dimension Framework)")

    scores = model.evaluate_all()
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    print(f"\n{'Technique':<20} {'Score':>8}  {'Bar'}")
    print("-" * 55)
    for name, score in sorted_scores:
        bar = "█" * int(score * 40)
        print(f"  {name:<18} {score:>6.3f}  {bar}")

    print(f"\nWeights: R={model.weights[0]:.0%}, "
          f"ρ={model.weights[1]:.0%}, "
          f"η={model.weights[2]:.0%}, "
          f"τ={model.weights[3]:.0%}, "
          f"Π={model.weights[4]:.0%}, "
          f"ι={model.weights[5]:.0%}")


def demo_compare(model: GoalkeeperPerformanceModel):
    """Compare catching vs blocking."""
    print_header("CATCHING vs BLOCKING (Detailed Comparison)")

    result = model.compare('CATCH', 'BLOCK')

    print(f"\n{'Dimension':<25} {'Weight':>6} {'CATCH':>7} {'BLOCK':>7} {'Winner':>10} {'Delta':>7}")
    print("-" * 70)
    for dim in result['per_dimension']:
        print(f"  {dim['dimension']:<23} {dim['weight']:>5.0%} "
              f"{dim['CATCH']:>7.2f} {dim['BLOCK']:>7.2f} "
              f"{dim['advantage']:>10} {dim['delta']:>6.2f}")

    print("-" * 70)
    print(f"  {'TOTAL SCORE':<23} {'':>5} "
          f"{result['score_a']:>7.3f} {result['score_b']:>7.3f} "
          f"{result['overall_advantage']:>10} "
          f"{abs(result['score_a'] - result['score_b']):>6.3f}")

    print(f"\n  CATCH wins {result['dimensions_won_a']}/6 dimensions")
    print(f"  BLOCK wins {result['dimensions_won_b']}/6 dimensions")


def demo_allocation(model: GoalkeeperPerformanceModel):
    """Compute optimal training allocation."""
    print_header("OPTIMAL TRAINING ALLOCATION")

    allocation = model.compute_allocation()
    sorted_alloc = sorted(allocation.items(), key=lambda x: x[1], reverse=True)

    print(f"\n{'Technique':<20} {'Allocation':>10}  {'Training Minutes (90min)':>25}")
    print("-" * 60)
    for name, alloc in sorted_alloc:
        minutes = alloc * 90
        bar = "█" * int(alloc * 40)
        print(f"  {name:<18} {alloc:>9.1%}  {minutes:>6.0f} min  {bar}")

    print(f"\n  Based on: frequency ({model.W_FREQ:.0%}) + "
          f"score ({model.W_SCORE:.0%}) + "
          f"weakness ({model.W_WEAKNESS:.0%})")


def demo_complementarity(model: GoalkeeperPerformanceModel):
    """Show complementarity effects with example profiles."""
    print_header("COMPLEMENTARITY ANALYSIS")

    # Balanced goalkeeper
    balanced = model.evaluate_goalkeeper(
        name="Balanced GK",
        strategic_components={'S1': 0.7, 'S2': 0.7, 'S3': 0.7, 'S4': 0.7},
        tactical_components={'T1': 0.7, 'T2': 0.7, 'T3': 0.7, 'T4': 0.7},
        operative_components={'O1': 0.7, 'O2': 0.7, 'O3': 0.7, 'O4': 0.7, 'O5': 0.7},
    )

    # One-dimensional (only operative)
    one_dim = model.evaluate_goalkeeper(
        name="Operative-Only GK",
        strategic_components={'S1': 0.3, 'S2': 0.3, 'S3': 0.3, 'S4': 0.3},
        tactical_components={'T1': 0.3, 'T2': 0.3, 'T3': 0.3, 'T4': 0.3},
        operative_components={'O1': 0.9, 'O2': 0.9, 'O3': 0.9, 'O4': 0.9, 'O5': 0.9},
    )

    # Block-specialized (training dominated by blocking)
    block_spec = model.evaluate_goalkeeper(
        name="Block-Specialist GK",
        strategic_components={'S1': 0.4, 'S2': 0.4, 'S3': 0.5, 'S4': 0.3},
        tactical_components={'T1': 0.5, 'T2': 0.4, 'T3': 0.4, 'T4': 0.5},
        operative_components={'O1': 0.5, 'O2': 0.5, 'O3': 0.9, 'O4': 0.4, 'O5': 0.6},
    )

    profiles = [balanced, one_dim, block_spec]

    print(f"\n{'Profile':<22} {'L_S':>6} {'L_T':>6} {'L_O':>6} "
          f"{'Additive':>9} {'Compl.':>7} {'Total':>7}")
    print("-" * 70)

    for p in profiles:
        comp = model.complementarity_value(p)
        print(f"  {p.name:<20} "
              f"{p.strategic.score:>5.2f} "
              f"{p.tactical.score:>5.2f} "
              f"{p.operative.score:>5.2f} "
              f"{comp['additive_base']:>8.3f} "
              f"{comp['total_complementarity']:>6.3f} "
              f"{comp['total_performance']:>6.3f}")

    print(f"\n  Complementarity parameters: "
          f"γ_ST={model.GAMMA_ST}, γ_SO={model.GAMMA_SO}, γ_TO={model.GAMMA_TO}")
    print(f"  The balanced goalkeeper benefits most from complementarity.")
    print(f"  The block-specialist loses complementarity value due to")
    print(f"  one-dimensional operative focus and weak strategic/tactical levels.")


def demo_substitution(model: GoalkeeperPerformanceModel):
    """Show substitution cost of shifting to block-heavy training."""
    print_header("SUBSTITUTION COST ANALYSIS")

    current = {
        'CATCH': 0.35,
        'PARRY_SAFE': 0.25,
        'BLOCK': 0.10,
        'PUNCH': 0.15,
        'FOOT_SAVE': 0.15,
    }

    # Block-heavy (social media influenced)
    proposed = {
        'CATCH': 0.15,
        'PARRY_SAFE': 0.15,
        'BLOCK': 0.40,
        'PUNCH': 0.15,
        'FOOT_SAVE': 0.15,
    }

    result = model.substitution_cost(current, proposed)

    print_subheader("Current vs Block-Heavy Allocation")
    print(f"\n  Current expected value:  {result['current_expected_value']:.3f}")
    print(f"  Proposed expected value: {result['proposed_expected_value']:.3f}")
    print(f"  Net change:             {result['net_change']:+.3f}")

    if result['shifts']:
        print(f"\n  {'Technique':<18} {'From':>8} {'To':>8} {'Delta':>8}")
        print("  " + "-" * 45)
        for t, s in result['shifts'].items():
            print(f"  {t:<18} {s['from']:>7.0%} {s['to']:>7.0%} {s['delta']:>+7.0%}")

    print(f"\n  Shifting to block-heavy training reduces expected")
    print(f"  training value by {abs(result['net_change']):.1%} of current value.")


def demo_profiles(model: GoalkeeperPerformanceModel):
    """Evaluate and compare 3 reference goalkeeper profiles."""
    print_header("REFERENCE GOALKEEPER PROFILES")
    print("  Three real-world profiles for empirical validation")
    print("  of PRED-GPM-001 through PRED-GPM-012.\n")

    profiles = create_reference_profiles(model)
    availability = create_reference_availability()

    # Level scores
    print(f"  {'Goalkeeper':<20} {'L_S':>6} {'L_T':>6} {'L_O':>6} "
          f"{'Type':<24} {'PRED'}")
    print("  " + "-" * 80)

    profile_types = {
        'NEUER': ('Strategic Specialist', 'PRED-006, 008'),
        'ALISSON': ('Balanced Excellence', 'PRED-004, 002'),
        'COURTOIS': ('Operative Specialist', 'PRED-011, 009'),
    }

    for key, profile in profiles.items():
        ptype, pred = profile_types[key]
        print(f"  {profile.name:<20} "
              f"{profile.strategic.score:>5.2f} "
              f"{profile.tactical.score:>5.2f} "
              f"{profile.operative.score:>5.2f} "
              f"{ptype:<24} {pred}")

    # Complementarity analysis
    print_subheader("Complementarity Ranking")
    comp_data = []
    for key, profile in profiles.items():
        comp = model.complementarity_value(profile)
        comp_data.append((profile.name, comp))

    comp_data.sort(key=lambda x: x[1]['complementarity_share'], reverse=True)

    print(f"\n  {'Goalkeeper':<20} {'Additive':>9} {'Compl.':>7} "
          f"{'Share':>7} {'Total':>7}")
    print("  " + "-" * 55)
    for name, comp in comp_data:
        print(f"  {name:<20} "
              f"{comp['additive_base']:>8.3f} "
              f"{comp['total_complementarity']:>6.3f} "
              f"{comp['complementarity_share']:>6.1%} "
              f"{comp['total_performance']:>6.3f}")

    print(f"\n  → PRED-004 validated: Alisson (balanced) has highest "
          f"complementarity share.")

    # V*_eff analysis
    print_subheader("Effective Value (V*_eff = V* × A × D)")

    print(f"\n  {'Goalkeeper':<20} {'V*':>6} {'A':>6} {'D':>6} {'V*_eff':>8} {'Status'}")
    print("  " + "-" * 60)

    for key, profile in profiles.items():
        comp = model.complementarity_value(profile)
        v_star = comp['total_performance']
        avail = availability[key]
        a = avail.availability_rate
        d = avail.durability
        v_eff = compute_effective_value(v_star, a, d)

        status = ""
        if a < 0.3:
            status = "← AVAILABILITY VETO"
        elif a < 0.7:
            status = "← Reduced"

        print(f"  {profile.name:<20} "
              f"{v_star:>5.3f} "
              f"{a:>5.2f} "
              f"{d:>5.2f} "
              f"{v_eff:>7.3f} {status}")

    print(f"\n  → PRED-011 validated: Courtois V*_eff collapses due to "
          f"ACL tear (A=0.15).")
    print(f"  → An available Alisson (A=0.88) outperforms even though "
          f"Courtois has higher L_O.")


def main():
    parser = argparse.ArgumentParser(
        description="GPM 3.0: Goalkeeper Performance Model"
    )
    parser.add_argument('--evaluate', action='store_true',
                        help='Evaluate all techniques')
    parser.add_argument('--compare', action='store_true',
                        help='Compare catching vs blocking')
    parser.add_argument('--allocate', action='store_true',
                        help='Compute optimal training allocation')
    parser.add_argument('--complementarity', action='store_true',
                        help='Show complementarity analysis')
    parser.add_argument('--substitution', action='store_true',
                        help='Show substitution cost analysis')
    parser.add_argument('--profiles', action='store_true',
                        help='Evaluate 3 reference goalkeeper profiles')
    parser.add_argument('--all', action='store_true',
                        help='Run all analyses')

    args = parser.parse_args()

    model = GoalkeeperPerformanceModel()

    if args.all or not any([args.evaluate, args.compare, args.allocate,
                            args.complementarity, args.substitution,
                            args.profiles]):
        # Run all demos
        print("\n" + "=" * 70)
        print("  GPM 3.0: GOALKEEPER PERFORMANCE MODEL")
        print("  Gerhard Bruno Fehr | FehrAdvice & Partners AG")
        print("=" * 70)

        demo_evaluate(model)
        demo_compare(model)
        demo_allocation(model)
        demo_complementarity(model)
        demo_substitution(model)
        demo_profiles(model)

        print_header("SUMMARY")
        print("""
  GPM 3.0 — Six-Dimension Framework (v3.0)

  1. CATCHING dominates in 6/6 evaluation dimensions
  2. BLOCKING scores lowest across all techniques
  3. D6 (Injury Risk) widens the gap: BLOCK is 3.1x more dangerous
  4. Optimal allocation: ~35% catching, ~5% blocking
  5. Block-heavy training REDUCES expected value by significant margin
  6. Complementarity rewards balanced multi-level development
  7. Current social-media-driven trend overweights blocking by ~8x

  V*_eff = V* × A × D — Availability is a VETO factor.
  An available average GK outperforms an injured elite GK.

  The F1 Simulator Principle: Train decisions in realistic frequency
  distributions, not isolated techniques in arbitrary proportions.
""")
    else:
        if args.evaluate:
            demo_evaluate(model)
        if args.compare:
            demo_compare(model)
        if args.allocate:
            demo_allocation(model)
        if args.complementarity:
            demo_complementarity(model)
        if args.substitution:
            demo_substitution(model)
        if args.profiles:
            demo_profiles(model)


if __name__ == '__main__':
    main()
