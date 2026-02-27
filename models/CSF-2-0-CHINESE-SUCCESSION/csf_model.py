"""
CSF 2.0: China Succession Framework v1.0
Factionalist-consensus model of Chinese Communist Party leadership succession
Implementation: Python operational model for candidate evaluation and prediction

Single Source of Truth: model-definition.yaml
"""

import numpy as np
import yaml
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
import json
from pathlib import Path


@dataclass
class CandidateProfile:
    """Candidate dimension scores (0-1 scale) for CCP succession"""
    name: str
    age: int
    c_fraktion: float         # Factional alignment
    c_legitimitat: float      # Track record
    c_seniority: float        # Tenure & generational position
    c_kompetenz: float        # Technical competence
    c_intl: float             # International relations

    def to_dict(self) -> Dict[str, float]:
        return {
            'c_fraktion': self.c_fraktion,
            'c_legitimitat': self.c_legitimitat,
            'c_seniority': self.c_seniority,
            'c_kompetenz': self.c_kompetenz,
            'c_intl': self.c_intl
        }


@dataclass
class SuccessionResults:
    """Results from succession model evaluation"""
    candidate_name: str
    individual_probability: float
    consensus_probability: float  # After factional negotiations
    competitive_probability: float  # In 5-candidate field
    dimension_scores: Dict[str, float]
    contribution_by_dimension: Dict[str, float]
    ranking: int
    pbsc_advancement_estimate: int  # Years until PBSC (if not there already)
    generalsekretaer_readiness: str  # "Ready", "Preparing", "Too Young", "Too Old"


class ChinaSuccessionFramework:
    """CSF 2.0: Factionalist-consensus model of Chinese succession"""

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

        # Extract parameters
        self._load_dimensions()
        self._load_complementarity_matrix()

    def _load_dimensions(self):
        """Load dimension weights and beta coefficients"""
        self.dimensions = {}
        self.weights = {}

        for dim in self.model_spec['dimensions']:
            symbol = dim['symbol']
            name = dim['name']
            weight = dim['weight']

            self.dimensions[symbol] = {
                'name': name,
                'weight': weight,
                'description': dim['description']
            }
            self.weights[symbol] = weight

        # Validate weights sum to ~1.0
        total_weight = sum(self.weights.values())
        assert 0.95 < total_weight < 1.05, f"Dimension weights must sum to 1.0, got {total_weight}"

    def _load_complementarity_matrix(self):
        """Load gamma complementarity parameters"""
        self.gamma_matrix = {}

        for param in self.model_spec['complementarity_matrix']:
            key = param['parameter']
            self.gamma_matrix[key] = {
                'symbol': param['symbol'],
                'value': param['value'],
                'interpretation': param['interpretation']
            }

    def calculate_individual_probability(self, candidate: CandidateProfile) -> float:
        """
        Calculate probability that candidate becomes General Secretary
        Using logistic regression with beta coefficients

        P(General Secretary) = 1 / (1 + exp(-(β₀ + Σβᵢ·Xᵢ)))

        Args:
            candidate: CandidateProfile with dimension scores

        Returns:
            Probability (0-1)
        """
        # Beta coefficients from model (matched to PSF 2.0 structure)
        beta_0 = -3.5  # Baseline (most candidates not papabile)
        beta_fraktion = 2.2
        beta_legitimitat = 1.6
        beta_seniority = 1.4
        beta_kompetenz = 0.9
        beta_intl = 0.6

        # Linear predictor
        argument = (
            beta_0 +
            beta_fraktion * candidate.c_fraktion +
            beta_legitimitat * candidate.c_legitimitat +
            beta_seniority * candidate.c_seniority +
            beta_kompetenz * candidate.c_kompetenz +
            beta_intl * candidate.c_intl
        )

        # Logistic transformation
        p_individual = 1.0 / (1.0 + np.exp(-argument))

        return float(p_individual)

    def evaluate_conclave(self, candidates: List[CandidateProfile]) -> List[SuccessionResults]:
        """
        Evaluate multiple candidates and normalize probabilities

        In Chinese succession:
        1. Individual probabilities reflect personal qualifications
        2. Normalization shows competitive field
        3. Factional negotiations may further modify

        Args:
            candidates: List of CandidateProfile objects

        Returns:
            List of SuccessionResults, sorted by probability
        """
        results = []

        # Calculate individual probabilities
        individual_probs = []
        for candidate in candidates:
            p_ind = self.calculate_individual_probability(candidate)
            individual_probs.append(p_ind)

        # Normalize to competition field (divide by sum)
        total_prob = sum(individual_probs)
        competitive_probs = [p / total_prob for p in individual_probs]

        # Estimate dimension contributions
        for i, candidate in enumerate(candidates):
            dim_contrib = self._calculate_dimension_contributions(candidate)

            # Estimate PBSC advancement timeline
            if candidate.c_seniority < 0.6:
                pbsc_years = 5
            elif candidate.c_seniority < 0.75:
                pbsc_years = 3
            else:
                pbsc_years = 0

            # Generalsekretär readiness assessment
            if candidate.age < 50:
                readiness = "Too Young (building experience)"
            elif candidate.age < 55:
                readiness = "Preparing (early candidacy)"
            elif candidate.age < 68:
                readiness = "Ready (optimal window)"
            else:
                readiness = "Too Old (unless extraordinary)"

            result = SuccessionResults(
                candidate_name=candidate.name,
                individual_probability=individual_probs[i],
                consensus_probability=individual_probs[i] * 0.85,  # Negotiations reduce some
                competitive_probability=competitive_probs[i],
                dimension_scores=candidate.to_dict(),
                contribution_by_dimension=dim_contrib,
                ranking=0,  # Will be set after sorting
                pbsc_advancement_estimate=pbsc_years,
                generalsekretaer_readiness=readiness
            )
            results.append(result)

        # Sort by probability and assign rankings
        results.sort(key=lambda r: r.competitive_probability, reverse=True)
        for i, result in enumerate(results, 1):
            result.ranking = i

        return results

    def _calculate_dimension_contributions(self, candidate: CandidateProfile) -> Dict[str, float]:
        """Calculate contribution of each dimension to overall probability"""
        scores = candidate.to_dict()

        # Contribution = dimension_score × dimension_weight
        contributions = {}
        for dim_symbol, dim_info in self.dimensions.items():
            weight = dim_info['weight']
            score = scores.get(dim_symbol.lower(), 0.5)  # Default to 0.5
            contributions[dim_symbol] = score * weight

        return contributions

    def estimate_succession_timeline(self, candidate: CandidateProfile) -> Tuple[str, int]:
        """
        Estimate when candidate will reach General Secretary (if ever)

        Args:
            candidate: CandidateProfile

        Returns:
            Tuple: (timeline_description, years_until_generalsekretaer)
        """
        # Simple heuristic based on age and seniority
        if candidate.age < 45:
            return ("Early Career - 12+ years minimum", 12)
        elif candidate.age < 55:
            return ("Provincial/Politburo track - 5-10 years", 7)
        elif candidate.age < 60:
            return ("PBSC candidate - 2-5 years", 3)
        elif candidate.age < 68:
            return ("Ready for succession - 0-3 years", 1)
        else:
            return ("Age limit approaching - unlikely", 999)

    def factional_consensus_probability(self, candidate: CandidateProfile) -> float:
        """
        Estimate likelihood of factional consensus
        (All major factions accept this candidate)

        Key insight: Even strong candidates can be blocked by consensus requirement
        Chinese system requires ~3/5 major factions accepting candidate

        Args:
            candidate: CandidateProfile

        Returns:
            Probability that major factions accept (0-1)
        """
        # High factional alignment → easier consensus
        # Consensus gets harder with extreme ideology
        c_frak = candidate.c_fraktion

        if c_frak > 0.85:
            # Ultra-aligned: hard to block, ~80% consensus chance
            return 0.80
        elif c_frak > 0.75:
            # Well-connected: ~70% consensus
            return 0.70
        elif c_frak > 0.60:
            # Moderate: ~60% consensus
            return 0.60
        elif c_frak > 0.50:
            # Weak: ~40% consensus (likely blocked)
            return 0.40
        else:
            # Very weak: ~10% consensus (only if no alternatives)
            return 0.10

    def apply_complementarity_effects(self, candidate: CandidateProfile) -> Dict[str, float]:
        """
        Calculate synergy effects between dimensions (complementarity γ)

        Example: Strong c_fraktion + strong c_legitimitat → multiplicative advantage

        Args:
            candidate: CandidateProfile

        Returns:
            Dictionary of gamma effects
        """
        effects = {}

        # γ_FraktionLegitimität: High both → powerful
        fl_synergy = (candidate.c_fraktion * candidate.c_legitimitat) * 0.75
        effects['gamma_fraktion_legitimitat'] = fl_synergy

        # γ_FraktionSeniority: Long-serving loyalists
        fs_synergy = (candidate.c_fraktion * candidate.c_seniority) * 0.70
        effects['gamma_fraktion_seniority'] = fs_synergy

        # γ_LegitimitätKompetenz: Results + technical skill
        lk_synergy = (candidate.c_legitimitat * candidate.c_kompetenz) * 0.55
        effects['gamma_legitimitat_kompetenz'] = lk_synergy

        # γ_SeniorityKompetenz (ANTI-synergy): Older = less tech-savvy
        sk_antisyn = (candidate.c_seniority * candidate.c_kompetenz) * (-0.30)
        effects['gamma_seniority_kompetenz_anti'] = sk_antisyn

        # γ_CompetitionEffect: If multiple candidates strong → stalemate
        effects['competition_blockade_risk'] = -0.15

        return effects

    def get_model_summary(self) -> str:
        """Return human-readable model summary"""
        return f"""
╔════════════════════════════════════════════════════════╗
║   China Succession Framework (CSF) 2.0 Summary         ║
╚════════════════════════════════════════════════════════╝

Model ID: {self.model_id}
Status: {self.status}
Confidence: {self.confidence}

CORE DIMENSIONS (5):
  Λ (C_Fraktion):      Factional alignment [40% weight]
  Ι (C_Legitimität):   Track record [25% weight]
  Π (C_Seniority):     Tenure/generational [20% weight]
  Ν (C_Kompetenz):     Technical competence [12% weight]
  Α (C_Intl):          International relations [8% weight]

GOVERNANCE TIERS:
  Tier 1: Senioren-Patriarchen (3-5 ultra-elders)
  Tier 2: PBSC Standing Committee (7 persons)
  Tier 3: Politburo (24-25 persons)
  Tier 4: Provincial Governors (31 provinces)

KEY INSIGHT:
  Chinese succession = FACTIONALIST CONSENSUS
  NOT: Democratic election
  NOT: Simple meritocracy
  BUT: Negotiated consensus among competing power networks

NEXT SUCCESSION POINT: 2027 Party Congress (5-year cycle)
OUT-OF-SAMPLE TEST: 2032 succession prediction
"""

    @staticmethod
    def create_test_candidate(name: str, profile_dict: Dict) -> CandidateProfile:
        """Helper to create candidate from dictionary"""
        return CandidateProfile(
            name=name,
            age=profile_dict.get('age', 55),
            c_fraktion=profile_dict.get('c_fraktion', 0.5),
            c_legitimitat=profile_dict.get('c_legitimitat', 0.5),
            c_seniority=profile_dict.get('c_seniority', 0.5),
            c_kompetenz=profile_dict.get('c_kompetenz', 0.5),
            c_intl=profile_dict.get('c_intl', 0.3)
        )


# ============================================================================
# USAGE EXAMPLE
# ============================================================================

if __name__ == "__main__":
    # Initialize model
    model = ChinaSuccessionFramework("model-definition.yaml")
    print(model.get_model_summary())

    # Define candidates
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

    unknown_candidate = CandidateProfile(
        name="Unknown Rising Star",
        age=58,
        c_fraktion=0.60,
        c_legitimitat=0.80,
        c_seniority=0.72,
        c_kompetenz=0.75,
        c_intl=0.25
    )

    candidates = [li_qiang, ding_xuexiang, unknown_candidate]

    # Evaluate
    results = model.evaluate_conclave(candidates)

    print("\n╔════════════════════════════════════════════════════════╗")
    print("║   2032 Succession Probability Ranking                 ║")
    print("╚════════════════════════════════════════════════════════╝\n")

    for result in results:
        print(f"Rank {result.ranking}: {result.candidate_name}")
        print(f"  Individual Probability: {result.individual_probability:.1%}")
        print(f"  Competitive Probability: {result.competitive_probability:.1%}")
        print(f"  Readiness: {result.generalsekretaer_readiness}")
        print(f"  Factional Consensus Chance: {model.factional_consensus_probability(candidates[result.ranking-1]):.1%}")
        print()
