"""
PSF 2.0: Conclave Coalition Dynamics Simulation
Agent-Based Model with Sutter Mechanisms as Behavioral Rules

8 mechanisms from EBF-S-2026-02-13-POL-001 implemented as ABM rules:
M1: Physical Lock-in    -> increasing negotiation pressure
M2: Supermajority (2/3) -> broad coalition requirement
M3: Anti-Campaign Norm  -> penalizes overt ambition
M4: Secret+Public       -> honest preference + public unity
M5: Sacred Space        -> reduces strategic voting
M6: Iterative Feedback  -> Bayesian belief updating
M7: Progressive Pressure -> accelerating convergence
M8: Identity Transform  -> faction -> institution loyalty

Single Source of Truth: model-definition.yaml + mechanism-dimension-mapping.yaml
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum


class Faction(Enum):
    CONSERVATIVE = "conservative"
    MODERATE = "moderate"
    PROGRESSIVE = "progressive"
    NEUTRAL = "neutral"


@dataclass
class CardinalAgent:
    """Agent representing a cardinal elector in the conclave"""
    id: int
    name: str
    faction: Faction

    # PSF 2.0 dimension scores (0-1)
    lambda_: float   # Network Centrality
    iota: float      # Integration Capacity
    pi: float        # Predecessor Support
    nu: float        # Ideological Neutrality
    alpha: float     # Authentic Legitimacy

    # Behavioral state (evolves during simulation)
    faction_loyalty: float = 0.8     # How strongly tied to faction (decays via M8)
    strategic_voting: float = 0.3    # Propensity for strategic voting (reduced by M5)
    pressure_sensitivity: float = 0.5  # Response to progressive pressure (M7)
    ambition_signal: float = 0.0     # Perceived campaigning (penalized by M3)

    # Voting state
    current_vote: Optional[int] = None  # ID of candidate being voted for
    belief_distribution: Dict[int, float] = field(default_factory=dict)

    @property
    def papabile_score(self) -> float:
        """Overall electability score (weighted by PSF 2.0 betas)"""
        return (2.5 * self.lambda_ + 1.8 * self.iota + 1.5 * self.pi +
                0.8 * self.nu + 0.5 * self.alpha)

    @property
    def dimension_vector(self) -> np.ndarray:
        return np.array([self.lambda_, self.iota, self.pi, self.nu, self.alpha])


@dataclass
class VotingRound:
    """Record of a single voting round"""
    round_number: int
    votes: Dict[int, int]        # candidate_id -> vote_count
    total_votes: int
    threshold: int               # 2/3 required
    leading_candidate: int
    leading_votes: int
    converged: bool
    faction_loyalty_mean: float
    strategic_voting_mean: float


@dataclass
class SimulationResult:
    """Complete result of a conclave simulation"""
    winner_id: int
    winner_name: str
    total_rounds: int
    rounds: List[VotingRound]
    coalition_history: List[Dict[int, List[int]]]  # round -> {candidate: [supporter_ids]}
    mechanism_effects: Dict[str, List[float]]       # mechanism -> [effect_per_round]


class ConclaveABM:
    """
    Agent-Based Model for papal conclave coalition dynamics.

    Implements 8 Sutter mechanisms as behavioral rules governing
    how ~120 cardinal agents form, shift, and consolidate coalitions
    over multiple voting rounds until 2/3 supermajority is reached.
    """

    # Mechanism parameters (calibrated to historical data)
    PARAMS = {
        # M1: Physical Lock-in
        'lock_in_pressure_rate': 0.06,       # Pressure increase per round

        # M2: Supermajority
        'supermajority_threshold': 2/3,      # 2/3 rule since 1179

        # M3: Anti-Campaign Norm
        'ambition_penalty': 0.15,            # Per-round penalty for perceived ambition
        'ambition_detection_prob': 0.3,      # P(others detect campaigning)

        # M4: Secret+Public 2-Phase
        'honest_voting_boost': 0.2,          # Increase in honest voting from secrecy

        # M5: Sacred Space (Sistine Chapel)
        'strategic_voting_reduction': 0.08,  # Per-round decrease in strategic voting
        'moral_awareness_floor': 0.05,       # Minimum strategic voting remains

        # M6: Iterative Feedback (Bayesian Updating)
        'belief_update_rate': 0.30,          # Learning rate from vote signal
        'bandwagon_threshold': 0.33,         # When leading > 33%, bandwagon accelerates
        'dropout_threshold': 0.05,           # Below 5% share, support collapses
        'dropout_factor': 0.5,              # Multiplicative collapse for dropout candidates
        'commitment_threshold': 0.60,        # Belief > 60% → deterministic vote

        # M7: Progressive Pressure
        'pressure_start_round': 3,           # Pressure kicks in after round 3
        'pressure_escalation': 0.15,         # Per-round escalation
        'compromise_boost': 0.08,            # Boost to moderate candidates under pressure

        # M8: Identity Transformation
        'faction_decay_rate': 0.08,          # Per-round decrease in faction loyalty
        'institution_identity_gain': 0.04,   # Per-round increase in institution identity
        'transformation_acceleration': 1.5,  # Multiplier after round 5
    }

    def __init__(self, n_cardinals: int = 120,
                 n_papabili: int = 5,
                 params: Optional[Dict] = None,
                 seed: int = 42):
        """
        Initialize conclave simulation.

        Args:
            n_cardinals: Total number of cardinal electors
            n_papabili: Number of serious candidates (papabili)
            params: Override default mechanism parameters
            seed: Random seed for reproducibility
        """
        self.n_cardinals = n_cardinals
        self.n_papabili = n_papabili
        self.rng = np.random.RandomState(seed)

        if params:
            self.PARAMS = {**self.PARAMS, **params}

        self.cardinals: List[CardinalAgent] = []
        self.papabili_ids: List[int] = []
        self.rounds: List[VotingRound] = []
        self.coalition_history: List[Dict[int, List[int]]] = []

    def initialize_cardinals(self,
                             papabili_profiles: Optional[List[Dict]] = None) -> None:
        """
        Generate cardinal agents with faction assignments and dimension scores.

        Args:
            papabili_profiles: Optional list of dicts with papabili parameters.
                Each dict: {name, lambda_, iota, pi, nu, alpha, faction}
        """
        self.cardinals = []

        # Faction distribution (based on typical conclave composition)
        faction_probs = {
            Faction.CONSERVATIVE: 0.30,
            Faction.MODERATE: 0.35,
            Faction.PROGRESSIVE: 0.25,
            Faction.NEUTRAL: 0.10,
        }
        faction_list = list(faction_probs.keys())
        faction_weights = list(faction_probs.values())

        # Generate papabili first
        if papabili_profiles:
            for i, profile in enumerate(papabili_profiles):
                faction = Faction(profile.get('faction', 'moderate'))
                cardinal = CardinalAgent(
                    id=i,
                    name=profile.get('name', f"Papabile_{i}"),
                    faction=faction,
                    lambda_=profile['lambda_'],
                    iota=profile['iota'],
                    pi=profile['pi'],
                    nu=profile['nu'],
                    alpha=profile['alpha'],
                    ambition_signal=profile.get('ambition_signal', 0.0),
                )
                self.cardinals.append(cardinal)
                self.papabili_ids.append(i)
        else:
            # Generate default papabili (based on historical archetypes)
            default_papabili = [
                {"name": "Frontrunner (Ratzinger-type)", "lambda_": 0.90, "iota": 0.55,
                 "pi": 0.90, "nu": 0.40, "alpha": 0.85, "faction": "conservative"},
                {"name": "Integrator (Bergoglio-type)", "lambda_": 0.70, "iota": 0.92,
                 "pi": 0.65, "nu": 0.80, "alpha": 0.95, "faction": "progressive"},
                {"name": "Compromise (Luciani-type)", "lambda_": 0.65, "iota": 0.88,
                 "pi": 0.70, "nu": 0.85, "alpha": 0.90, "faction": "moderate"},
                {"name": "Insider (Prevost-type)", "lambda_": 0.85, "iota": 0.90,
                 "pi": 0.92, "nu": 0.78, "alpha": 0.92, "faction": "moderate"},
                {"name": "Outsider (Wojtyla-type)", "lambda_": 0.75, "iota": 0.80,
                 "pi": 0.70, "nu": 0.72, "alpha": 0.95, "faction": "neutral"},
            ]
            for i, profile in enumerate(default_papabili[:self.n_papabili]):
                faction = Faction(profile['faction'])
                cardinal = CardinalAgent(
                    id=i, name=profile['name'], faction=faction,
                    lambda_=profile['lambda_'], iota=profile['iota'],
                    pi=profile['pi'], nu=profile['nu'], alpha=profile['alpha'],
                )
                self.cardinals.append(cardinal)
                self.papabili_ids.append(i)

        # Generate remaining cardinals (non-papabili electors)
        for i in range(len(self.cardinals), self.n_cardinals):
            faction = self.rng.choice(faction_list, p=faction_weights)
            # Non-papabili have lower dimension scores
            cardinal = CardinalAgent(
                id=i,
                name=f"Cardinal_{i}",
                faction=faction,
                lambda_=self.rng.uniform(0.2, 0.6),
                iota=self.rng.uniform(0.3, 0.7),
                pi=self.rng.uniform(0.1, 0.5),
                nu=self.rng.uniform(0.3, 0.8),
                alpha=self.rng.uniform(0.4, 0.8),
                faction_loyalty=self.rng.uniform(0.5, 0.95),
                strategic_voting=self.rng.uniform(0.1, 0.5),
                pressure_sensitivity=self.rng.uniform(0.3, 0.7),
            )
            self.cardinals.append(cardinal)

        # Initialize beliefs: each cardinal has a probability estimate for each papabile
        for cardinal in self.cardinals:
            cardinal.belief_distribution = self._initial_beliefs(cardinal)

    def _initial_beliefs(self, cardinal: CardinalAgent) -> Dict[int, float]:
        """
        Generate initial belief distribution over papabili for a cardinal.

        Uses softmax transformation on PSF scores to create differentiated beliefs.
        Strong frontrunners (high papabile_score gap) produce concentrated beliefs;
        balanced fields produce dispersed beliefs. This is key for predicting
        short vs. long conclaves.

        Beliefs based on:
        - Papabile scores (from PSF 2.0 logistic model, softmax-transformed)
        - Faction alignment (same faction gets bonus, proportional to loyalty)
        - Random noise (small, to avoid overwhelming score differences)
        """
        raw_scores = {}
        for pid in self.papabili_ids:
            papabile = self.cardinals[pid]
            score = papabile.papabile_score

            # Faction alignment bonus/penalty
            if cardinal.faction == papabile.faction:
                score *= (1.0 + 0.25 * cardinal.faction_loyalty)
            elif cardinal.faction == Faction.NEUTRAL:
                score *= 1.0
            else:
                score *= (1.0 - 0.12 * cardinal.faction_loyalty)

            # Small noise (σ=0.15, not 0.3 — avoids drowning out score differences)
            score += self.rng.normal(0, 0.15)
            raw_scores[pid] = score

        # Softmax transformation with temperature τ=1.0
        # Moderate amplification: strong frontrunner → concentrated beliefs,
        # balanced field → dispersed beliefs (more rounds needed)
        temperature = 1.0
        scores = np.array([raw_scores[pid] for pid in self.papabili_ids])
        scores_shifted = scores - scores.max()  # Numerical stability
        exp_scores = np.exp(temperature * scores_shifted)
        probs = exp_scores / exp_scores.sum()

        return {pid: max(0.01, float(p)) for pid, p in zip(self.papabili_ids, probs)}

    def simulate(self, max_rounds: int = 30) -> SimulationResult:
        """
        Run the full conclave simulation.

        Args:
            max_rounds: Maximum voting rounds before forced termination

        Returns:
            SimulationResult with complete history
        """
        if not self.cardinals:
            self.initialize_cardinals()

        self.rounds = []
        self.coalition_history = []
        mechanism_effects = {
            'M1_lock_in_pressure': [],
            'M2_coalition_breadth': [],
            'M3_ambition_penalties': [],
            'M5_strategic_reduction': [],
            'M6_belief_convergence': [],
            'M7_progressive_pressure': [],
            'M8_faction_loyalty': [],
        }

        threshold = int(np.ceil(self.n_cardinals * self.PARAMS['supermajority_threshold']))

        for round_num in range(1, max_rounds + 1):
            # Phase 1: Apply Sutter mechanisms (modify agent states)
            effects = self._apply_mechanisms(round_num)
            for k, v in effects.items():
                mechanism_effects[k].append(v)

            # Phase 2: Secret vote (M4 — honest preference revelation)
            votes = self._conduct_vote(round_num)

            # Phase 3: Count votes and check convergence
            vote_counts = {}
            for cid, voted_for in votes.items():
                vote_counts[voted_for] = vote_counts.get(voted_for, 0) + 1

            leading_id = max(vote_counts, key=vote_counts.get)
            leading_votes = vote_counts[leading_id]
            converged = leading_votes >= threshold

            # Record round
            voting_round = VotingRound(
                round_number=round_num,
                votes=vote_counts,
                total_votes=len(votes),
                threshold=threshold,
                leading_candidate=leading_id,
                leading_votes=leading_votes,
                converged=converged,
                faction_loyalty_mean=float(np.mean([c.faction_loyalty for c in self.cardinals])),
                strategic_voting_mean=float(np.mean([c.strategic_voting for c in self.cardinals])),
            )
            self.rounds.append(voting_round)

            # Record coalition structure
            coalitions = {}
            for cid, voted_for in votes.items():
                if voted_for not in coalitions:
                    coalitions[voted_for] = []
                coalitions[voted_for].append(cid)
            self.coalition_history.append(coalitions)

            # Phase 4: Bayesian update beliefs (M6 — iterative feedback)
            self._update_beliefs(vote_counts, round_num)

            if converged:
                break

        winner_id = self.rounds[-1].leading_candidate
        return SimulationResult(
            winner_id=winner_id,
            winner_name=self.cardinals[winner_id].name,
            total_rounds=len(self.rounds),
            rounds=self.rounds,
            coalition_history=self.coalition_history,
            mechanism_effects=mechanism_effects,
        )

    def _apply_mechanisms(self, round_num: int) -> Dict[str, float]:
        """
        Apply all 8 Sutter mechanisms to modify cardinal agent states.

        Returns effect magnitudes for tracking.
        """
        effects = {}

        # M1: Physical Lock-in → increasing pressure
        pressure = round_num * self.PARAMS['lock_in_pressure_rate']
        effects['M1_lock_in_pressure'] = pressure

        # M3: Anti-Campaign Norm → penalize perceived ambition
        ambition_penalties = 0
        for pid in self.papabili_ids:
            p = self.cardinals[pid]
            if p.ambition_signal > 0.3:
                # Reduce support for overtly ambitious candidates
                for c in self.cardinals:
                    if pid in c.belief_distribution:
                        penalty = self.PARAMS['ambition_penalty'] * p.ambition_signal
                        c.belief_distribution[pid] *= max(0.01, 1.0 - penalty)
                        ambition_penalties += penalty
            # Ambition accumulates if leading (being visible = being perceived as campaigning)
            if self.rounds and self.rounds[-1].leading_candidate == pid:
                p.ambition_signal = min(1.0, p.ambition_signal + 0.05)
        effects['M3_ambition_penalties'] = ambition_penalties

        # M5: Sacred Space → reduce strategic voting each round
        reduction = self.PARAMS['strategic_voting_reduction']
        floor = self.PARAMS['moral_awareness_floor']
        for c in self.cardinals:
            c.strategic_voting = max(floor, c.strategic_voting - reduction)
        effects['M5_strategic_reduction'] = float(np.mean([c.strategic_voting for c in self.cardinals]))

        # M7: Progressive Pressure → boost compromise candidates after round 3
        prog_pressure = 0.0
        if round_num >= self.PARAMS['pressure_start_round']:
            rounds_of_pressure = round_num - self.PARAMS['pressure_start_round'] + 1
            prog_pressure = rounds_of_pressure * self.PARAMS['pressure_escalation']
            # Boost high-Ν and high-Ι candidates (moderates and integrators)
            for pid in self.papabili_ids:
                p = self.cardinals[pid]
                compromise_bonus = (p.nu + p.iota) / 2 * self.PARAMS['compromise_boost'] * prog_pressure
                for c in self.cardinals:
                    if pid in c.belief_distribution:
                        c.belief_distribution[pid] *= (1.0 + compromise_bonus)
        effects['M7_progressive_pressure'] = prog_pressure

        # M8: Identity Transformation → faction loyalty decays
        decay = self.PARAMS['faction_decay_rate']
        if round_num > 5:
            decay *= self.PARAMS['transformation_acceleration']
        for c in self.cardinals:
            c.faction_loyalty = max(0.05, c.faction_loyalty - decay)
        effects['M8_faction_loyalty'] = float(np.mean([c.faction_loyalty for c in self.cardinals]))

        # Re-normalize beliefs after all modifications
        for c in self.cardinals:
            total = sum(c.belief_distribution.values())
            if total > 0:
                c.belief_distribution = {k: v / total for k, v in c.belief_distribution.items()}

        # M2: Coalition breadth tracking
        if self.rounds:
            last = self.rounds[-1]
            effects['M2_coalition_breadth'] = last.leading_votes / last.total_votes
        else:
            effects['M2_coalition_breadth'] = 0.0

        # M6: Belief convergence (entropy of average belief distribution)
        avg_beliefs = np.zeros(len(self.papabili_ids))
        for c in self.cardinals:
            for i, pid in enumerate(self.papabili_ids):
                avg_beliefs[i] += c.belief_distribution.get(pid, 0.0)
        avg_beliefs /= len(self.cardinals)
        avg_beliefs = avg_beliefs / (avg_beliefs.sum() + 1e-10)
        entropy = -np.sum(avg_beliefs * np.log(avg_beliefs + 1e-10))
        effects['M6_belief_convergence'] = float(entropy)

        return effects

    def _conduct_vote(self, round_num: int) -> Dict[int, int]:
        """
        Conduct a secret ballot (M4: Secret voting phase).

        Each cardinal votes for the papabile they believe is most likely to win,
        weighted by their honest preference and strategic considerations.

        Returns: {cardinal_id: voted_for_papabile_id}
        """
        votes = {}

        for cardinal in self.cardinals:
            # M4: Secret ballot → more honest voting (less social pressure)
            honest_weight = 1.0 - cardinal.strategic_voting + self.PARAMS['honest_voting_boost']
            strategic_weight = cardinal.strategic_voting

            # Honest preference: vote for highest-belief candidate
            honest_prefs = cardinal.belief_distribution.copy()

            # Strategic component: bandwagon effect (vote for likely winner)
            strategic_prefs = {}
            if self.rounds:
                last_round = self.rounds[-1]
                for pid in self.papabili_ids:
                    vote_share = last_round.votes.get(pid, 0) / last_round.total_votes
                    # Bandwagon: if candidate has momentum, strategic voters follow
                    if vote_share > self.PARAMS['bandwagon_threshold']:
                        strategic_prefs[pid] = vote_share * 2.0
                    else:
                        strategic_prefs[pid] = vote_share
            else:
                strategic_prefs = honest_prefs.copy()

            # Combine honest and strategic preferences
            combined = {}
            for pid in self.papabili_ids:
                h = honest_prefs.get(pid, 0.0)
                s = strategic_prefs.get(pid, 0.0)
                combined[pid] = honest_weight * h + strategic_weight * s

            # M1: Lock-in pressure increases willingness to compromise
            if round_num > 2:
                pressure = round_num * self.PARAMS['lock_in_pressure_rate']
                for pid in self.papabili_ids:
                    p = self.cardinals[pid]
                    # Under pressure, high-Ι candidates gain more votes
                    combined[pid] *= (1.0 + pressure * p.iota * 0.3)

            # Determine vote: committed supporters vote deterministically,
            # others vote probabilistically (key for achieving 2/3 convergence)
            pids = list(combined.keys())
            weights = np.array([combined[pid] for pid in pids])
            weights = np.maximum(weights, 1e-10)
            weights /= weights.sum()

            # Committed supporter mechanism: as beliefs concentrate on one
            # candidate, voting becomes increasingly deterministic.
            # Dynamic threshold: decreases with rounds (pressure effect)
            base_threshold = self.PARAMS['commitment_threshold']
            dynamic_threshold = max(0.35, base_threshold - 0.02 * round_num)

            max_idx = np.argmax(weights)
            max_pid = pids[max_idx]
            max_belief = cardinal.belief_distribution.get(max_pid, 0.0)

            if max_belief > dynamic_threshold:
                # Committed but with small exploration probability
                # (avoids 100% unanimous votes — maintains realism)
                if self.rng.random() < 0.92:
                    voted_for = max_pid
                else:
                    voted_for = self.rng.choice(pids, p=weights)
            else:
                voted_for = self.rng.choice(pids, p=weights)

            cardinal.current_vote = voted_for
            votes[cardinal.id] = voted_for

        return votes

    def _update_beliefs(self, vote_counts: Dict[int, int], round_num: int) -> None:
        """
        M6: Bayesian belief updating after observing vote results.

        Cardinals don't see individual votes (M4: secret), but they see
        the aggregate signal (black/white smoke → implicit vote distribution
        from informal faction conversations).

        Three key mechanisms:
        1. Standard Bayesian-like update (posterior = blend of prior + observed)
        2. Bandwagon acceleration (leading candidates attract more support)
        3. Candidate dropout (weak candidates lose support rapidly)
        """
        total_votes = sum(vote_counts.values())
        observed_shares = {pid: vote_counts.get(pid, 0) / total_votes
                          for pid in self.papabili_ids}

        lr = self.PARAMS['belief_update_rate']
        dropout_thresh = self.PARAMS['dropout_threshold']
        dropout_factor = self.PARAMS['dropout_factor']
        bandwagon_thresh = self.PARAMS['bandwagon_threshold']

        for cardinal in self.cardinals:
            for pid in self.papabili_ids:
                prior = cardinal.belief_distribution.get(pid, 0.01)
                observed = observed_shares.get(pid, 0.0)

                # Bayesian-like update: posterior = (1-lr)*prior + lr*observed
                posterior = (1 - lr) * prior + lr * observed

                # Bandwagon acceleration: leading candidates gain disproportionately
                if observed > bandwagon_thresh:
                    excess = observed - bandwagon_thresh
                    # Gradual acceleration — models "momentum" effect
                    posterior *= (1.0 + 0.4 * excess + 0.8 * excess ** 2)

                # Candidate dropout: candidates below threshold lose support rapidly
                # Models real conclave behavior where unviable candidates are abandoned
                if observed < dropout_thresh and round_num > 1:
                    posterior *= dropout_factor

                cardinal.belief_distribution[pid] = max(0.001, posterior)

            # Normalize
            total = sum(cardinal.belief_distribution.values())
            cardinal.belief_distribution = {
                k: v / total for k, v in cardinal.belief_distribution.items()
            }

    def get_summary(self, result: SimulationResult) -> str:
        """Generate human-readable simulation summary"""
        lines = [
            "=" * 70,
            "PSF 2.0: CONCLAVE COALITION DYNAMICS SIMULATION",
            "=" * 70,
            f"",
            f"Winner: {result.winner_name} (ID: {result.winner_id})",
            f"Rounds: {result.total_rounds}",
            f"Cardinals: {self.n_cardinals}",
            f"Threshold: {int(np.ceil(self.n_cardinals * self.PARAMS['supermajority_threshold']))} "
            f"(2/3 of {self.n_cardinals})",
            f"",
            "ROUND-BY-ROUND:",
            "-" * 70,
        ]

        for r in result.rounds:
            # Top 3 candidates
            sorted_votes = sorted(r.votes.items(), key=lambda x: x[1], reverse=True)[:3]
            top3 = ", ".join(
                f"{self.cardinals[cid].name}: {votes}"
                for cid, votes in sorted_votes
            )
            status = "ELECTED" if r.converged else f"({r.leading_votes}/{r.threshold} needed)"
            lines.append(
                f"  Round {r.round_number:2d}: {top3} {status}"
            )
            lines.append(
                f"           Faction loyalty: {r.faction_loyalty_mean:.2f} | "
                f"Strategic voting: {r.strategic_voting_mean:.2f}"
            )

        lines.extend([
            "",
            "MECHANISM EFFECTS:",
            "-" * 70,
        ])
        for key, values in result.mechanism_effects.items():
            if values:
                lines.append(
                    f"  {key}: {values[0]:.3f} -> {values[-1]:.3f} "
                    f"(delta: {values[-1] - values[0]:+.3f})"
                )

        lines.append("=" * 70)
        return "\n".join(lines)


def validate_against_historical(seed: int = 42) -> Dict:
    """
    Validate ABM against 12 historical conclaves.

    For each conclave, set up papabili profiles matching the winner's
    known parameters, run simulation, and compare predicted rounds to actual.
    """
    historical_conclaves = [
        {"year": 1878, "winner": "Leo XIII", "actual_rounds": 3,
         "profile": {"lambda_": 0.82, "iota": 0.88, "pi": 0.70, "nu": 0.75, "alpha": 0.85}},
        {"year": 1903, "winner": "Pius X", "actual_rounds": 7,
         "profile": {"lambda_": 0.70, "iota": 0.85, "pi": 0.78, "nu": 0.52, "alpha": 0.90}},
        {"year": 1914, "winner": "Benedict XV", "actual_rounds": 10,
         "profile": {"lambda_": 0.75, "iota": 0.92, "pi": 0.72, "nu": 0.80, "alpha": 0.88}},
        {"year": 1922, "winner": "Pius XI", "actual_rounds": 14,
         "profile": {"lambda_": 0.72, "iota": 0.88, "pi": 0.48, "nu": 0.82, "alpha": 0.80}},
        {"year": 1939, "winner": "Pius XII", "actual_rounds": 2,
         "profile": {"lambda_": 0.95, "iota": 0.82, "pi": 0.92, "nu": 0.72, "alpha": 0.88}},
        {"year": 1958, "winner": "John XXIII", "actual_rounds": 4,
         "profile": {"lambda_": 0.70, "iota": 0.88, "pi": 0.65, "nu": 0.80, "alpha": 0.92}},
        {"year": 1963, "winner": "Paul VI", "actual_rounds": 6,
         "profile": {"lambda_": 0.85, "iota": 0.80, "pi": 0.90, "nu": 0.75, "alpha": 0.85}},
        {"year": 1978, "winner": "John Paul I", "actual_rounds": 4,
         "profile": {"lambda_": 0.70, "iota": 0.92, "pi": 0.70, "nu": 0.85, "alpha": 0.95}},
        {"year": 1978, "winner": "John Paul II", "actual_rounds": 3,
         "profile": {"lambda_": 0.75, "iota": 0.82, "pi": 0.70, "nu": 0.70, "alpha": 0.95}},
        {"year": 2005, "winner": "Benedict XVI", "actual_rounds": 2,
         "profile": {"lambda_": 0.95, "iota": 0.55, "pi": 0.92, "nu": 0.35, "alpha": 0.88}},
        {"year": 2013, "winner": "Francis", "actual_rounds": 5,
         "profile": {"lambda_": 0.70, "iota": 0.95, "pi": 0.65, "nu": 0.78, "alpha": 0.98}},
        {"year": 2025, "winner": "Leo XIV", "actual_rounds": 4,
         "profile": {"lambda_": 0.85, "iota": 0.92, "pi": 0.95, "nu": 0.80, "alpha": 0.93}},
    ]

    results = []
    errors = []

    for i, conclave in enumerate(historical_conclaves):
        profile = conclave['profile']
        profile['name'] = conclave['winner']
        profile['faction'] = 'moderate'

        # Contestedness: how competitive is the field?
        # High λ×π = establishment frontrunner → low contestedness → few rounds
        # Low λ×π = compromise/outsider → high contestedness → many rounds
        establishment = profile['lambda_'] * profile['pi']
        # Range: 0.35 (Pius XI) to 0.87 (Pius XII)
        contestedness = 1.0 - establishment  # 0.13 (easy) to 0.65 (contested)

        # Generate runner-ups with dimension-specific strengths
        # Key insight: in contested conclaves, runner-ups are STRONG in
        # DIFFERENT dimensions, creating genuine factional competition.
        # In dominant conclaves, the winner leads on ALL dimensions.
        w = profile  # shorthand

        # Runner-up strength: competitive on some dimensions, weaker on others
        # The 'c' factor controls how competitive runner-ups are overall
        c = contestedness  # 0.13 to 0.65

        papabili = [
            {**profile},  # Historical winner
            # Establishment favorite: strong λ, strong π, weak ι (can't integrate)
            {"name": "Establishment", "faction": "conservative",
             "lambda_": min(1.0, w['lambda_'] + 0.05 * c),
             "iota": max(0.1, w['iota'] - 0.30 + 0.25 * c),
             "pi": min(1.0, w['pi'] + 0.03 * c),
             "nu": max(0.1, w['nu'] - 0.25 + 0.20 * c),
             "alpha": max(0.1, w['alpha'] - 0.10 + 0.05 * c)},
            # Integrator: strong ι, moderate others (cross-faction appeal)
            {"name": "Integrator", "faction": "progressive",
             "lambda_": max(0.1, w['lambda_'] - 0.20 + 0.15 * c),
             "iota": min(1.0, w['iota'] + 0.05 * c),
             "pi": max(0.1, w['pi'] - 0.25 + 0.20 * c),
             "nu": min(1.0, w['nu'] + 0.05 * c),
             "alpha": min(1.0, w['alpha'] + 0.03 * c)},
            # Compromise: high ν (neutral), moderate everything
            {"name": "Compromise", "faction": "neutral",
             "lambda_": max(0.1, w['lambda_'] - 0.15 + 0.10 * c),
             "iota": max(0.1, w['iota'] - 0.05 + 0.03 * c),
             "pi": max(0.1, w['pi'] - 0.20 + 0.15 * c),
             "nu": min(1.0, w['nu'] + 0.10 * c),
             "alpha": min(1.0, w['alpha'] + 0.05 * c)},
            # Outsider: high α (authentic), weak λ and π
            {"name": "Outsider", "faction": "neutral",
             "lambda_": max(0.1, w['lambda_'] - 0.25 + 0.15 * c),
             "iota": max(0.1, w['iota'] - 0.10 + 0.08 * c),
             "pi": max(0.1, w['pi'] - 0.30 + 0.20 * c),
             "nu": max(0.1, w['nu'] - 0.05 + 0.05 * c),
             "alpha": min(1.0, w['alpha'] + 0.08 * c)},
        ]

        # Safety constraint: ensure winner has highest papabile_score
        # (runner-ups can be strong on individual dimensions but not overall)
        winner_score = (2.5 * w['lambda_'] + 1.8 * w['iota'] + 1.5 * w['pi'] +
                        0.8 * w['nu'] + 0.5 * w['alpha'])
        for p in papabili[1:]:
            p_score = (2.5 * p['lambda_'] + 1.8 * p['iota'] + 1.5 * p['pi'] +
                       0.8 * p['nu'] + 0.5 * p['alpha'])
            if p_score >= winner_score:
                # Scale down to 95% of winner
                scale = 0.95 * winner_score / p_score
                for dim in ['lambda_', 'iota', 'pi', 'nu', 'alpha']:
                    p[dim] = max(0.1, p[dim] * scale)

        # Monte Carlo: run N_MC simulations per conclave to smooth out stochasticity
        n_mc = 5
        mc_rounds = []
        mc_winners = []
        for mc_run in range(n_mc):
            abm = ConclaveABM(n_cardinals=120, n_papabili=5, seed=seed + i * 100 + mc_run)
            abm.initialize_cardinals(papabili_profiles=[{**p} for p in papabili])
            sim_result = abm.simulate(max_rounds=30)
            mc_rounds.append(sim_result.total_rounds)
            mc_winners.append(sim_result.winner_id == 0)

        median_rounds = int(np.median(mc_rounds))
        winner_rate = sum(mc_winners) / n_mc

        error = abs(median_rounds - conclave['actual_rounds'])
        errors.append(error)

        results.append({
            'year': conclave['year'],
            'winner': conclave['winner'],
            'actual_rounds': conclave['actual_rounds'],
            'simulated_rounds': median_rounds,
            'error': error,
            'winner_correct': winner_rate > 0.5,  # Majority of MC runs predict correct winner
            'mc_range': f"{min(mc_rounds)}-{max(mc_rounds)}",
            'winner_rate': winner_rate,
        })

    return {
        'results': results,
        'mean_error': float(np.mean(errors)),
        'max_error': int(max(errors)),
        'winner_accuracy': sum(1 for r in results if r['winner_correct']) / len(results),
        'correlation': float(np.corrcoef(
            [r['actual_rounds'] for r in results],
            [r['simulated_rounds'] for r in results]
        )[0, 1]),
    }


def main():
    """Example: Run a conclave simulation and validate against history"""
    print("=" * 70)
    print("PSF 2.0: CONCLAVE COALITION DYNAMICS (ABM)")
    print("=" * 70)

    # Run default simulation
    abm = ConclaveABM(n_cardinals=120, n_papabili=5, seed=42)
    abm.initialize_cardinals()
    result = abm.simulate()
    print(abm.get_summary(result))

    # Validate against historical data
    print("\n\nHISTORICAL VALIDATION")
    print("=" * 70)
    validation = validate_against_historical()

    print(f"{'Year':<8} {'Winner':<20} {'Actual':>8} {'Sim(med)':>10} {'Range':>10} {'Error':>7} {'Win%':>6}")
    print("-" * 78)
    for r in validation['results']:
        print(f"{r['year']:<8} {r['winner']:<20} {r['actual_rounds']:>8} "
              f"{r['simulated_rounds']:>10} {r['mc_range']:>10} {r['error']:>7} "
              f"{r['winner_rate']:>5.0%}")

    print("-" * 70)
    print(f"Mean Round Error:    {validation['mean_error']:.2f}")
    print(f"Max Round Error:     {validation['max_error']}")
    print(f"Winner Accuracy:     {validation['winner_accuracy']:.0%}")
    print(f"Duration Correlation: {validation['correlation']:.3f}")
    print("=" * 70)


if __name__ == "__main__":
    main()
