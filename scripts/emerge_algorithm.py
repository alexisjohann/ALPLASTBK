#!/usr/bin/env python3
"""
EMERGE Algorithm Implementation (EIT-EMP-2/3)
=============================================

Computes optimal intervention profiles for AWARE changes based on:
- Context vector Ψ
- Baseline complementarities γ₀ (from literature)
- Budget and complexity constraints
- Scope level hierarchy (EIT-EMP-3)

Usage:
    python scripts/emerge_algorithm.py --context "econ=0.3,social=0.7,temporal=0.5"
    python scripts/emerge_algorithm.py --context "econ=0.3" --scope strategic
    python scripts/emerge_algorithm.py --scope systemic --stage action
    python scripts/emerge_algorithm.py --demo
    python scripts/emerge_algorithm.py --interactive

Scope Levels (EIT-EMP-3):
    instant     L4  Seconds-Minutes  Reflex/Habit
    operative   L3  Hours-Days       Routine
    tactical    L2  Days-Weeks       Deliberate (default)
    strategic   L1  Weeks-Months     Planned
    systemic    L0  Months-Years     Transformational

Based on: Appendix IE, EIT-EMP-1/2/3
"""

import argparse
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
import yaml

# =============================================================================
# BASELINE PARAMETERS (γ₀) - From EIT-EMP-1
# =============================================================================

# Category 1: Referent Complementarity
GAMMA_REFERENT = {
    ('Self', 'Comm'): -0.30,  # Egocentric Bias (AWX-A34)
}

# Category 2: Utility-Type Complementarity
GAMMA_UTILITY = {
    ('INU', 'KNU'): +0.25,  # AWX-A38
    ('INU', 'IDN'): +0.40,  # AWX-A39
    ('KNU', 'IDN'): +0.35,  # AWX-A40
}

# Category 3: Domain Complementarity (FEPSDE)
GAMMA_DOMAIN = {
    ('F', 'E'): +0.15,
    ('F', 'P'): +0.20,
    ('F', 'S'): -0.25,  # CROWDING-OUT (sign fixed by EIT-T9)
    ('F', 'D'): +0.30,
    ('F', 'Ex'): +0.10,
    ('E', 'P'): +0.35,
    ('E', 'S'): +0.40,
    ('E', 'D'): +0.25,
    ('E', 'Ex'): +0.45,
    ('P', 'S'): +0.20,
    ('P', 'D'): +0.15,
    ('P', 'Ex'): +0.10,
    ('S', 'D'): +0.35,
    ('S', 'Ex'): +0.50,  # STRONGEST positive synergy
    ('D', 'Ex'): +0.40,
}

# Category 4: Valence Complementarity
GAMMA_VALENCE = {
    ('pos', 'neg'): -0.50,  # Loss Aversion asymmetry
}

# Context sensitivity coefficients (β) - Initial estimates
BETA_SOCIAL_ON_FS = 0.15  # Strong social norms weaken F+S crowding-out

# =============================================================================
# 80D DIMENSION DEFINITIONS
# =============================================================================

# Block A: Other 10C (8 dimensions)
BLOCK_A = ['WHO', 'WHAT', 'HOW', 'WHEN', 'WHERE', 'READY', 'STAGE', 'HIER']

# Block B: AWARE Detail (72 dimensions)
REFERENTS = ['Self', 'Comm']
UTILITY_TYPES = ['INU', 'KNU', 'IDN']
DOMAINS = ['F', 'E', 'P', 'S', 'D', 'Ex']
VALENCES = ['pos', 'neg']

def generate_aware_dimensions() -> List[str]:
    """Generate all 72 AWARE-detail dimension names."""
    dims = []
    for ref in REFERENTS:
        for util in UTILITY_TYPES:
            for dom in DOMAINS:
                for val in VALENCES:
                    dims.append(f"{ref}_{util}_{dom}_{val}")
    return dims

BLOCK_B = generate_aware_dimensions()
ALL_DIMENSIONS = BLOCK_A + BLOCK_B  # 80 total

# =============================================================================
# BASELINE WEIGHTS (w_i) - Effectiveness by dimension
# =============================================================================

BASELINE_WEIGHTS = {
    # Block A: 10C dimensions
    'WHO': 0.5,
    'WHAT': 0.6,
    'HOW': 0.5,
    'WHEN': 0.7,
    'WHERE': 0.4,
    'READY': 0.6,
    'STAGE': 0.5,
    'HIER': 0.4,
}

# Block B: AWARE-detail weights (pattern-based)
def compute_aware_weight(dim: str) -> float:
    """Compute baseline weight for an AWARE-detail dimension."""
    parts = dim.split('_')
    ref, util, dom, val = parts[0], parts[1], parts[2], parts[3]

    # Base weight
    w = 0.5

    # Self is generally more effective than Community
    if ref == 'Self':
        w += 0.1

    # KNU (Known Not Used) has highest impact potential
    if util == 'KNU':
        w += 0.15
    elif util == 'IDN':
        w += 0.10

    # Domain adjustments
    domain_bonus = {'F': 0.10, 'E': 0.05, 'S': 0.05, 'Ex': 0.05, 'D': 0.0, 'P': 0.0}
    w += domain_bonus.get(dom, 0)

    # Positive valence slightly more effective
    if val == 'pos':
        w += 0.05

    return min(w, 1.0)

# Populate weights for all dimensions
for dim in BLOCK_B:
    BASELINE_WEIGHTS[dim] = compute_aware_weight(dim)

# =============================================================================
# CONTEXT ENCODING
# =============================================================================

@dataclass
class Context:
    """Context vector Ψ ∈ [0,1]^8"""
    economic: float = 0.5      # 0=recession, 1=boom
    social: float = 0.5        # 0=weak norms, 1=strong norms
    temporal: float = 0.5      # 0=short horizon, 1=long horizon
    spatial: float = 0.5       # 0=local, 1=global
    institutional: float = 0.5 # 0=weak institutions, 1=strong
    cultural: float = 0.5      # 0=individualist, 1=collectivist
    technological: float = 0.5 # 0=low tech, 1=high tech
    environmental: float = 0.5 # 0=stable, 1=crisis

    def to_vector(self) -> np.ndarray:
        return np.array([
            self.economic, self.social, self.temporal, self.spatial,
            self.institutional, self.cultural, self.technological, self.environmental
        ])

    @classmethod
    def from_dict(cls, d: Dict[str, float]) -> 'Context':
        return cls(
            economic=d.get('econ', d.get('economic', 0.5)),
            social=d.get('social', 0.5),
            temporal=d.get('temporal', d.get('temp', 0.5)),
            spatial=d.get('spatial', 0.5),
            institutional=d.get('institutional', d.get('inst', 0.5)),
            cultural=d.get('cultural', d.get('cult', 0.5)),
            technological=d.get('technological', d.get('tech', 0.5)),
            environmental=d.get('environmental', d.get('env', 0.5)),
        )

# =============================================================================
# GAMMA COMPUTATION (EIT-EMP-1)
# =============================================================================

def get_gamma_baseline(dim_i: str, dim_j: str) -> float:
    """Get baseline γ₀ for a pair of dimensions."""
    if dim_i == dim_j:
        return 0.0

    # Block A × Block A: Use 10C matrix
    if dim_i in BLOCK_A and dim_j in BLOCK_A:
        # Simplified: return 0 for most, known values for specific pairs
        return 0.0

    # Block A × Block B: Cross-block (simplified)
    if (dim_i in BLOCK_A) != (dim_j in BLOCK_A):
        return 0.1  # Small positive synergy

    # Block B × Block B: Compute from factors
    if dim_i in BLOCK_B and dim_j in BLOCK_B:
        return compute_detail_gamma(dim_i, dim_j)

    return 0.0

def compute_detail_gamma(dim_i: str, dim_j: str) -> float:
    """
    Compute γ for two AWARE-detail dimensions using factor decomposition.
    γ(Di, Dj) = 1/4 [γ_ref + γ_util + γ_dom + γ_val]
    """
    parts_i = dim_i.split('_')
    parts_j = dim_j.split('_')

    ref_i, util_i, dom_i, val_i = parts_i
    ref_j, util_j, dom_j, val_j = parts_j

    # Get factor-level gammas
    gamma_ref = GAMMA_REFERENT.get((ref_i, ref_j), GAMMA_REFERENT.get((ref_j, ref_i), 0.0))
    gamma_util = GAMMA_UTILITY.get((util_i, util_j), GAMMA_UTILITY.get((util_j, util_i), 0.0))
    gamma_dom = GAMMA_DOMAIN.get((dom_i, dom_j), GAMMA_DOMAIN.get((dom_j, dom_i), 0.0))
    gamma_val = GAMMA_VALENCE.get((val_i, val_j), GAMMA_VALENCE.get((val_j, val_i), 0.0))

    return 0.25 * (gamma_ref + gamma_util + gamma_dom + gamma_val)

def compute_gamma_context(dim_i: str, dim_j: str, context: Context) -> float:
    """
    Compute context-dependent γ(Ψ) = γ₀ + Σ β·Ψ
    """
    gamma_0 = get_gamma_baseline(dim_i, dim_j)

    # Apply context modulation
    # Example: Strong social norms weaken F+S crowding-out
    if 'F' in dim_i and 'S' in dim_j or 'S' in dim_i and 'F' in dim_j:
        gamma_0 += BETA_SOCIAL_ON_FS * context.social

    # Ensure sign preservation for F+S (Theorem EIT-T13)
    if ('_F_' in dim_i and '_S_' in dim_j) or ('_S_' in dim_i and '_F_' in dim_j):
        gamma_0 = min(gamma_0, -0.05)  # Never positive

    return gamma_0

# =============================================================================
# K-OPTIMAL COMPUTATION (Dynamic Portfolio Size)
# =============================================================================

# BCJ Stage adjustments for K
BCJ_STAGE_ADJUSTMENT = {
    'pre_contemplation': -2,
    'contemplation': -1,
    'preparation': 0,
    'action': +1,
    'maintenance': 0,
}

# =============================================================================
# SCOPE LEVEL HIERARCHY (EIT-EMP-3)
# =============================================================================

# Scope levels from EIT-EMP-3-D1
SCOPE_LEVELS = {
    'instant': {'level': 4, 'I_HIER': 0.0, 'duration': 'Seconds-Minutes', 'type': 'Reflex/Habit'},
    'operative': {'level': 3, 'I_HIER': 0.25, 'duration': 'Hours-Days', 'type': 'Routine'},
    'tactical': {'level': 2, 'I_HIER': 0.50, 'duration': 'Days-Weeks', 'type': 'Deliberate'},
    'strategic': {'level': 1, 'I_HIER': 0.75, 'duration': 'Weeks-Months', 'type': 'Planned'},
    'systemic': {'level': 0, 'I_HIER': 1.0, 'duration': 'Months-Years', 'type': 'Transformational'},
}

# Scope adjustment for K (EIT-EMP-3-D3)
SCOPE_K_ADJUSTMENT = {
    'instant': -2,      # L4: Single intervention only
    'operative': -1,    # L3: Few interventions
    'tactical': 0,      # L2: Standard (baseline)
    'strategic': +1,    # L1: More comprehensive
    'systemic': +2,     # L0: Multi-level portfolio
}

# =============================================================================
# SCOPE-MECHANISM AFFINITY MATRIX (EIT-EMP-3-D2)
# =============================================================================
# Maps intervention mechanisms to their appropriate scope levels
# Affinity α ∈ [0,1]: 0 = not appropriate, 1 = highly appropriate

SCOPE_MECHANISM_AFFINITY = {
    # === INSTANT (L4): Reflex/Habit - Seconds to Minutes ===
    'instant': {
        # High affinity: Simple, automatic, no deliberation required
        'Default Setting': 1.0,
        'Point-of-Decision Prompt': 0.9,
        'Simplification': 0.9,
        'Choice Architecture': 0.8,
        'Reminder/Salience': 0.7,
        'Loss Salience': 0.7,
        'Social Proof Reminder': 0.6,
        # Low affinity: Requires deliberation
        'Pre-Commitment Device': 0.1,
        'Goal Setting': 0.1,
        'Future Self Visualization': 0.2,
        'Implementation Intentions': 0.2,
        'Identity Priming': 0.3,
    },

    # === OPERATIVE (L3): Routine - Hours to Days ===
    'operative': {
        # High affinity: Daily routines, short feedback loops
        'Reminder/Salience': 1.0,
        'Progress Tracking': 0.9,
        'Daily Cost Calculator': 0.9,
        'Point-of-Decision Prompt': 0.8,
        'Deadline/Urgency': 0.8,
        'Default Setting': 0.7,
        'Social Proof Reminder': 0.7,
        'Peer Comparison': 0.7,
        # Medium affinity
        'Goal Proximity Display': 0.6,
        'Emotional Memory Activation': 0.5,
        # Lower affinity: Too long-term
        'Future Self Visualization': 0.3,
        'Pre-Commitment Device': 0.3,
    },

    # === TACTICAL (L2): Deliberate - Days to Weeks ===
    'tactical': {
        # High affinity: Planned actions, medium-term tracking
        'Goal Setting': 1.0,
        'Implementation Intentions': 0.9,
        'Progress Tracking': 0.9,
        'Milestone Celebrations': 0.9,
        'Stage-Matched Messaging': 0.8,
        'Timing Optimization': 0.8,
        'Barrier Reduction': 0.8,
        'Self-Efficacy Building': 0.7,
        'Peer Comparison': 0.7,
        'Leaderboard': 0.7,
        # Medium affinity
        'Pre-Commitment Device': 0.6,
        'Default Setting': 0.5,
        'Community Challenges': 0.6,
    },

    # === STRATEGIC (L1): Planned - Weeks to Months ===
    'strategic': {
        # High affinity: Long-term planning, identity change
        'Pre-Commitment Device': 1.0,
        'Future Self Visualization': 1.0,
        'Identity Priming': 0.9,
        'Role Assignment': 0.9,
        'Compound Interest Demonstration': 0.9,
        'Goal Setting': 0.8,
        'Journey Acceleration': 0.8,
        'Multi-Domain Bundling': 0.8,
        'Domain Reframing': 0.7,
        'Self-Efficacy Building': 0.7,
        # Medium affinity
        'Progress Tracking': 0.6,
        'Community Challenges': 0.6,
        # Lower for instant mechanisms
        'Default Setting': 0.4,
        'Reminder/Salience': 0.4,
    },

    # === SYSTEMIC (L0): Transformational - Months to Years ===
    'systemic': {
        # High affinity: Culture change, institutional redesign
        'Level Shifting': 1.0,
        'Environmental Restructuring': 1.0,
        'Role Assignment': 0.9,
        'Identity Priming': 0.9,
        'Multi-Domain Bundling': 0.9,
        'Community Norms': 0.9,
        'Collective Benefit Information': 0.8,
        'Community Dashboard': 0.8,
        'Social Capital Reminder': 0.8,
        'Future Self Visualization': 0.7,
        'Pre-Commitment Device': 0.7,
        # Lower for short-term mechanisms
        'Reminder/Salience': 0.2,
        'Default Setting': 0.3,
        'Daily Cost Calculator': 0.2,
        'Deadline/Urgency': 0.3,
    },
}

def get_mechanism_affinity(mechanism_name: str, scope_level: str) -> float:
    """
    Get affinity score for a mechanism at a given scope level.
    Returns α ∈ [0,1], default 0.5 if not explicitly defined.
    """
    scope_affinities = SCOPE_MECHANISM_AFFINITY.get(scope_level, {})
    return scope_affinities.get(mechanism_name, 0.5)  # Default moderate affinity

def compute_k_optimal(
    context: Context,
    budget: float = 100.0,
    stage: str = 'preparation',
    psi_education: float = 0.5,
    crowding_risk: float = 0.0,
    scope_level: str = 'tactical',
    verbose: bool = False
) -> Tuple[int, Dict[str, any]]:
    """
    Compute optimal portfolio size K* based on context.

    K*(Ψ) = K_base + δ_budget + δ_complexity + δ_stage + δ_crowding + δ_scope

    Based on:
    - Michie et al. (2013): 3-7 BCTs optimal
    - Miller (1956): 7±2 working memory limit
    - Gabaix (2019): Behavioral inattention

    Returns:
        Tuple of (K_optimal, rationale_dict)
    """
    K_BASE = 4  # Empirical sweet spot
    K_MIN = 2
    K_MAX = 9
    B_REF = 50.0  # Reference budget

    factors = {}

    # 1. Budget factor: δ_budget = floor(log2(B / B_ref))
    if budget > B_REF:
        delta_budget = int(np.floor(np.log2(budget / B_REF)))
    elif budget < B_REF / 2:
        delta_budget = -1
    else:
        delta_budget = 0
    delta_budget = max(-2, min(3, delta_budget))
    factors['budget'] = {'delta': delta_budget, 'value': budget, 'ref': B_REF}

    # 2. Complexity/Education factor: δ_complexity = round(2 · (ψ_edu - 0.5))
    delta_complexity = round(2 * (psi_education - 0.5))
    delta_complexity = max(-1, min(1, delta_complexity))
    factors['complexity'] = {'delta': delta_complexity, 'psi_education': psi_education}

    # 3. Stage factor
    delta_stage = BCJ_STAGE_ADJUSTMENT.get(stage, 0)
    factors['stage'] = {'delta': delta_stage, 'stage': stage}

    # 4. Crowding-out risk factor
    delta_crowding = -1 if crowding_risk > 0.3 else 0
    factors['crowding'] = {'delta': delta_crowding, 'risk': crowding_risk}

    # 5. Scope factor (EIT-EMP-3)
    delta_scope = SCOPE_K_ADJUSTMENT.get(scope_level, 0)
    scope_info = SCOPE_LEVELS.get(scope_level, SCOPE_LEVELS['tactical'])
    factors['scope'] = {
        'delta': delta_scope,
        'level': scope_level,
        'L': scope_info['level'],
        'duration': scope_info['duration'],
        'type': scope_info['type']
    }

    # Compute K*
    K_raw = K_BASE + delta_budget + delta_complexity + delta_stage + delta_crowding + delta_scope
    K_optimal = max(K_MIN, min(K_MAX, K_raw))

    rationale = {
        'K_base': K_BASE,
        'factors': factors,
        'K_raw': K_raw,
        'K_optimal': K_optimal,
        'scope_level': scope_level,
        'formula': f"K* = {K_BASE} + ({delta_budget}) + ({delta_complexity}) + ({delta_stage}) + ({delta_crowding}) + ({delta_scope}) = {K_raw} → {K_optimal}"
    }

    if verbose:
        print(f"\n--- K-Optimal Computation ---")
        print(f"K_base = {K_BASE}")
        print(f"δ_budget = {delta_budget} (Budget={budget}, Ref={B_REF})")
        print(f"δ_complexity = {delta_complexity} (ψ_education={psi_education})")
        print(f"δ_stage = {delta_stage} (Stage={stage})")
        print(f"δ_crowding = {delta_crowding} (Risk={crowding_risk:.2f})")
        print(f"δ_scope = {delta_scope} (Scope={scope_level}, L{scope_info['level']}, {scope_info['duration']})")
        print(f"K* = max({K_MIN}, min({K_MAX}, {K_raw})) = {K_optimal}")

    return K_optimal, rationale


# =============================================================================
# EMERGE ALGORITHM (EIT-EMP-2)
# =============================================================================

@dataclass
class InterventionResult:
    """Result of EMERGE algorithm."""
    profile: Dict[str, float]  # Dimension -> Intensity
    effectiveness: float
    active_dimensions: List[str]
    avoided_pairs: List[Tuple[str, str]]
    context: Context
    k_rationale: Optional[Dict] = None  # K-optimal computation rationale
    scope_level: str = 'tactical'  # Scope level (EIT-EMP-3)

def emerge(
    context: Context,
    target: str = "AWARE",
    budget: float = 100.0,
    complexity_limit: Optional[int] = None,  # None = compute dynamically
    crowding_threshold: float = 0.15,
    stage: str = 'preparation',
    psi_education: float = 0.5,
    scope_level: str = 'tactical',  # Scope level (EIT-EMP-3)
    verbose: bool = False
) -> InterventionResult:
    """
    EMERGE Algorithm: Compute optimal intervention profile.

    Args:
        context: Context vector Ψ
        target: Target outcome (e.g., "AWARE", "Self_KNU_F")
        budget: Total budget B
        complexity_limit: Maximum active dimensions K (None = compute dynamically)
        crowding_threshold: θ for crowding-out avoidance
        stage: BCJ stage for K computation
        psi_education: Education/complexity level for K computation
        scope_level: Scope level (instant/operative/tactical/strategic/systemic)
        verbose: Print progress

    Returns:
        InterventionResult with optimal profile
    """

    # Validate scope_level
    if scope_level not in SCOPE_LEVELS:
        raise ValueError(f"Invalid scope_level '{scope_level}'. Valid: {list(SCOPE_LEVELS.keys())}")

    # Compute K* dynamically if not provided
    k_rationale = None
    if complexity_limit is None:
        complexity_limit, k_rationale = compute_k_optimal(
            context=context,
            budget=budget,
            stage=stage,
            psi_education=psi_education,
            crowding_risk=0.0,  # Will be updated after first pass
            scope_level=scope_level,
            verbose=verbose
        )

    scope_info = SCOPE_LEVELS[scope_level]
    if verbose:
        print(f"\n{'='*60}")
        print("EMERGE Algorithm - Emergent Intervention Selection")
        print(f"{'='*60}")
        print(f"Context: econ={context.economic:.1f}, social={context.social:.1f}, "
              f"temporal={context.temporal:.1f}")
        print(f"Target: {target}, Budget: {budget}, K*: {complexity_limit}"
              f"{' (computed)' if k_rationale else ' (fixed)'}")
        print(f"Scope: {scope_level} (L{scope_info['level']}, {scope_info['duration']}, {scope_info['type']})")

    # Phase 1: Identify candidate dimensions
    if verbose:
        print(f"\n--- Phase 1: Identify Candidates ---")

    candidates = []
    for dim in ALL_DIMENSIONS:
        # Filter by target
        if target == "AWARE":
            if dim in BLOCK_B or dim == 'AWARE':
                candidates.append(dim)
        elif target in dim:
            candidates.append(dim)
        elif dim in BLOCK_A:
            candidates.append(dim)  # Include 10C for synergy

    # Rank by baseline weight
    candidates = sorted(candidates, key=lambda d: BASELINE_WEIGHTS.get(d, 0.5), reverse=True)
    candidates = candidates[:2 * complexity_limit]  # Top 2K

    if verbose:
        print(f"Top candidates: {candidates[:5]}...")

    # Phase 2: Greedy synergy selection
    if verbose:
        print(f"\n--- Phase 2: Greedy Selection ---")

    active = []
    avoided = []
    profile = {d: 0.0 for d in ALL_DIMENSIONS}
    remaining_budget = budget
    cost_per_dim = budget / complexity_limit  # Simplified uniform cost

    for _ in range(complexity_limit):
        if remaining_budget < cost_per_dim:
            break

        best_dim = None
        best_efficiency = -np.inf

        for dim in candidates:
            if dim in active:
                continue

            # Compute marginal gain
            w = BASELINE_WEIGHTS.get(dim, 0.5)
            synergy = sum(compute_gamma_context(dim, a, context) for a in active)
            marginal_gain = w + synergy
            efficiency = marginal_gain / cost_per_dim

            # Check crowding-out
            crowding_out = False
            for a in active:
                gamma = compute_gamma_context(dim, a, context)
                if gamma < -crowding_threshold:
                    crowding_out = True
                    avoided.append((dim, a))
                    break

            if crowding_out:
                continue

            if efficiency > best_efficiency:
                best_efficiency = efficiency
                best_dim = dim

        if best_dim is None:
            break

        active.append(best_dim)
        profile[best_dim] = 1.0
        remaining_budget -= cost_per_dim

        if verbose:
            print(f"  Selected: {best_dim} (w={BASELINE_WEIGHTS.get(best_dim, 0.5):.2f}, "
                  f"efficiency={best_efficiency:.3f})")

    # Phase 3: Intensity optimization (simplified)
    if verbose:
        print(f"\n--- Phase 3: Intensity Optimization ---")

    # For now, use heuristic: higher weight = higher intensity
    total_w = sum(BASELINE_WEIGHTS.get(d, 0.5) for d in active)
    for dim in active:
        w = BASELINE_WEIGHTS.get(dim, 0.5)
        profile[dim] = w / total_w if total_w > 0 else 1.0 / len(active)

    # Normalize to [0, 1]
    max_intensity = max(profile.values()) if profile else 1.0
    for dim in active:
        profile[dim] = profile[dim] / max_intensity if max_intensity > 0 else profile[dim]

    # Compute total effectiveness
    effectiveness = sum(BASELINE_WEIGHTS.get(d, 0.5) * profile[d] for d in active)
    for i, d1 in enumerate(active):
        for d2 in active[i+1:]:
            gamma = compute_gamma_context(d1, d2, context)
            effectiveness += gamma * profile[d1] * profile[d2]

    if verbose:
        print(f"\n--- Result ---")
        print(f"Active dimensions: {len(active)}")
        print(f"Total effectiveness: {effectiveness:.3f}")
        print(f"Avoided pairs: {len(avoided)}")

    return InterventionResult(
        profile={d: v for d, v in profile.items() if v > 0},
        effectiveness=effectiveness,
        active_dimensions=active,
        avoided_pairs=avoided,
        context=context,
        k_rationale=k_rationale,
        scope_level=scope_level
    )

# =============================================================================
# OUTPUT FORMATTING
# =============================================================================

# =============================================================================
# INTERVENTION SPECIFICATIONS - Full Scope Definition
# =============================================================================
# Each mechanism has: Ziel, In-Scope, Out-of-Scope, Lieferobjekte

@dataclass
class InterventionSpec:
    """Full specification for an intervention mechanism."""
    name: str
    description: str
    ziel: str                    # Objective/Goal
    in_scope: List[str]          # What's included
    out_of_scope: List[str]      # What's excluded
    lieferobjekte: List[str]     # Deliverables
    scope_levels: List[str]      # Optimal scope levels (L0-L4)
    primary_10c: str             # Primary 10C dimension

INTERVENTION_SPECS: Dict[str, InterventionSpec] = {
    # === NUDGE/CHOICE ARCHITECTURE ===
    'Default Setting': InterventionSpec(
        name='Default Setting',
        description='Setze vorteilhafte Standardoption',
        ziel='Automatische Wahl der optimalen Option ohne aktive Entscheidung',
        in_scope=[
            'Opt-out statt Opt-in Design',
            'Pre-selected beneficial options',
            'Smart defaults basierend auf Segment',
        ],
        out_of_scope=[
            'Zwang oder Mandatierung',
            'Versteckte oder irreführende Defaults',
            'Defaults ohne Opt-out Möglichkeit',
        ],
        lieferobjekte=[
            'Default-Konfiguration je Segment',
            'A/B Test Design für Default-Varianten',
            'Opt-out Rate Monitoring Dashboard',
        ],
        scope_levels=['instant', 'operative'],
        primary_10c='WHEN',
    ),
    'Choice Architecture': InterventionSpec(
        name='Choice Architecture',
        description='Strukturiere Entscheidungsumgebung',
        ziel='Vereinfachung komplexer Entscheidungen durch strukturierte Präsentation',
        in_scope=[
            'Option-Ordering (beste zuerst)',
            'Kategorisierung von Alternativen',
            'Progressive Disclosure (schrittweise)',
            'Eliminierung überflüssiger Optionen',
        ],
        out_of_scope=[
            'Manipulation oder Täuschung',
            'Entfernung relevanter Optionen',
            'Künstliche Verknappung',
        ],
        lieferobjekte=[
            'Choice Architecture Blueprint',
            'Wireframes/Mockups der Entscheidungsumgebung',
            'Usability Test Protokoll',
        ],
        scope_levels=['instant', 'tactical'],
        primary_10c='WHEN',
    ),

    # === AWARENESS/FEEDBACK ===
    'Reminder/Salience': InterventionSpec(
        name='Reminder/Salience',
        description='Push-Notification oder kontextuelle Erinnerung',
        ziel='Bekannte Information im richtigen Moment aktivieren',
        in_scope=[
            'Timing-optimierte Push-Notifications',
            'Kontextuelle In-App Reminders',
            'Email-Nudges mit personalisierten Daten',
        ],
        out_of_scope=[
            'Spam oder excessive Frequenz',
            'Generische Massenmailings',
            'Reminder ohne Handlungsoption',
        ],
        lieferobjekte=[
            'Notification-Timing-Matrix',
            'Message Templates (personalisiert)',
            'Frequenz-Optimierungs-Algorithmus',
            'Opt-out Management System',
        ],
        scope_levels=['operative', 'instant'],
        primary_10c='AWARE',
    ),
    'Progress Tracking': InterventionSpec(
        name='Progress Tracking',
        description='Visualisierung des Fortschritts zu Ziel',
        ziel='Motivation durch sichtbaren Fortschritt verstärken',
        in_scope=[
            'Fortschrittsbalken mit Prozentanzeige',
            'Milestone-Visualisierung',
            'Vergleich mit persönlichem Benchmark',
            'Streak-Counter für Konsistenz',
        ],
        out_of_scope=[
            'Unrealistische Zielprojektion',
            'Demotivierende Vergleiche',
            'Tracking ohne Feedback-Loop',
        ],
        lieferobjekte=[
            'Progress Dashboard Design',
            'Milestone-Definition je Segment',
            'Gamification-Elemente (Badges, Levels)',
            'Export/Sharing Funktion',
        ],
        scope_levels=['operative', 'tactical', 'strategic'],
        primary_10c='AWARE',
    ),
    'Future Self Visualization': InterventionSpec(
        name='Future Self Visualization',
        description='Verbindung zum zukünftigen Selbst herstellen',
        ziel='Emotionale Verbindung zu langfristigen Konsequenzen aufbauen',
        in_scope=[
            'Aging-Simulation (Foto-App)',
            'Brief an zukünftiges Selbst',
            'VR/AR Zukunfts-Simulation',
            'Personalisierte Szenario-Projektion',
        ],
        out_of_scope=[
            'Angstmachende Szenarien',
            'Unrealistische Versprechungen',
            'Manipulation durch Schockbilder',
        ],
        lieferobjekte=[
            'Future Self App/Tool',
            'Personalisierungs-Algorithmus',
            'Szenario-Templates (positiv/negativ)',
            'Emotional Impact Assessment',
        ],
        scope_levels=['strategic', 'systemic'],
        primary_10c='AWARE',
    ),

    # === GOAL-ORIENTED ===
    'Goal Setting': InterventionSpec(
        name='Goal Setting',
        description='SMART-Ziele mit Feedback definieren',
        ziel='Klare, erreichbare Ziele mit Commitment etablieren',
        in_scope=[
            'SMART-Ziel Formulierung',
            'Ziel-Commitment-Mechanismus',
            'Regelmäßige Ziel-Reviews',
            'Anpassbare Sub-Goals',
        ],
        out_of_scope=[
            'Unrealistische Ziele setzen',
            'Ziele ohne Review-Mechanismus',
            'Starre Ziele ohne Anpassung',
        ],
        lieferobjekte=[
            'Goal-Setting Workshop Design',
            'SMART-Goal Template',
            'Review-Cadence Kalender',
            'Goal-Tracking Integration',
        ],
        scope_levels=['tactical', 'strategic'],
        primary_10c='HOW',
    ),
    'Pre-Commitment Device': InterventionSpec(
        name='Pre-Commitment Device',
        description='Bindung an zukünftiges Verhalten',
        ziel='Selbstkontrolle durch vorherige Bindung stärken',
        in_scope=[
            'Commitment-Verträge (mit sich selbst)',
            'Automatische Transfers/Sperren',
            'Soziale Commitment-Mechanismen',
            'Penalty-basierte Commitment',
        ],
        out_of_scope=[
            'Unflexible Bindungen ohne Exit',
            'Excessive Penalties',
            'Commitment ohne Autonomie',
        ],
        lieferobjekte=[
            'Commitment Contract Template',
            'Auto-Escalation Mechanismus',
            'Cooling-Off Period Design',
            'Social Accountability System',
        ],
        scope_levels=['strategic', 'systemic'],
        primary_10c='HOW',
    ),
    'Implementation Intentions': InterventionSpec(
        name='Implementation Intentions',
        description='Wenn-Dann Pläne für automatisches Handeln',
        ziel='Handlungsabsicht in konkrete Situationen übersetzen',
        in_scope=[
            'Wenn-Dann Formulierung',
            'Situative Trigger definieren',
            'Habit Stacking (an bestehende Gewohnheit)',
            'Environment Design für Trigger',
        ],
        out_of_scope=[
            'Vage Absichtserklärungen',
            'Zu viele gleichzeitige Intentions',
            'Intentions ohne Monitoring',
        ],
        lieferobjekte=[
            'Implementation Intention Worksheet',
            'Trigger-Mapping Template',
            'Habit Stack Designer',
            'Weekly Check-in Protokoll',
        ],
        scope_levels=['tactical'],
        primary_10c='HOW',
    ),

    # === SOCIAL ===
    'Social Proof Reminder': InterventionSpec(
        name='Social Proof Reminder',
        description='Zeige was ähnliche Andere tun',
        ziel='Soziale Norm aktivieren um Verhalten zu legitimieren',
        in_scope=[
            'Descriptive Norms ("73% tun X")',
            'Peer Comparison (ähnliche Personen)',
            'Community-Aktivitäts-Feed',
            'Testimonials von Peers',
        ],
        out_of_scope=[
            'Manipulierte Statistiken',
            'Beschämende Vergleiche',
            'Irrelevante Vergleichsgruppen',
        ],
        lieferobjekte=[
            'Social Proof Message Library',
            'Peer Group Segmentierung',
            'Real-Time Norm Display',
            'A/B Test für Norm-Framing',
        ],
        scope_levels=['operative', 'tactical'],
        primary_10c='AWARE',
    ),
    'Community Norms': InterventionSpec(
        name='Community Norms',
        description='Etabliere und verstärke Gemeinschaftsnormen',
        ziel='Langfristige Verhaltensänderung durch Kulturwandel',
        in_scope=[
            'Norm-Setting durch Leadership',
            'Community Rituale und Events',
            'Shared Values Communication',
            'Norm Violation Feedback',
        ],
        out_of_scope=[
            'Zwangskonformität',
            'Ausgrenzung von Abweichlern',
            'Artifizielle Normen ohne Basis',
        ],
        lieferobjekte=[
            'Community Guidelines',
            'Norm Reinforcement Programm',
            'Leadership Talking Points',
            'Culture Assessment Survey',
        ],
        scope_levels=['systemic'],
        primary_10c='AWARE',
    ),

    # === IDENTITY/STRATEGIC ===
    'Identity Priming': InterventionSpec(
        name='Identity Priming',
        description='Aktiviere relevante Identität vor Entscheidung',
        ziel='Selbstkonzept als Motivator für konsistentes Verhalten nutzen',
        in_scope=[
            'Identitäts-Labels ("Sie als Sparer")',
            'Role Model Stories',
            'Identity-Consistent Framing',
            'Self-Affirmation Exercises',
        ],
        out_of_scope=[
            'Identitäts-Manipulation',
            'Beschämende Labels',
            'Inkonsistente Identitätsbotschaften',
        ],
        lieferobjekte=[
            'Identity Priming Message Set',
            'Persona-Segment Mapping',
            'Priming Timing Protocol',
            'Identity Consistency Check',
        ],
        scope_levels=['strategic', 'systemic'],
        primary_10c='WHO',
    ),
    'Environmental Restructuring': InterventionSpec(
        name='Environmental Restructuring',
        description='Physische oder digitale Umgebung umgestalten',
        ziel='Verhalten durch Umgebungsdesign erleichtern/erschweren',
        in_scope=[
            'Physical Space Redesign',
            'Digital Environment Changes',
            'Accessibility Optimization',
            'Friction/Ease Engineering',
        ],
        out_of_scope=[
            'Irreversible Änderungen ohne Test',
            'Umgebung ohne User Input',
            'Rein ästhetische Änderungen',
        ],
        lieferobjekte=[
            'Environment Audit Checklist',
            'Friction Map (aktuell vs. gewünscht)',
            'Redesign Blueprint',
            'Pilot Test Protocol',
        ],
        scope_levels=['systemic'],
        primary_10c='WHERE',
    ),
}

def get_intervention_spec(mechanism_name: str) -> Optional[InterventionSpec]:
    """Get full specification for a mechanism, or None if not found."""
    return INTERVENTION_SPECS.get(mechanism_name)

# =============================================================================
# INTERVENTION CATALOG - Concrete Mechanisms (Simplified)
# =============================================================================

INTERVENTION_CATALOG = {
    # Block A: 10C
    'WHO': [
        ("Identity Priming", "Aktiviere relevante Identität vor Entscheidung"),
        ("Role Assignment", "Weise explizite Rolle zu"),
        ("Level Shifting", "Verschiebe Perspektive (L0→L1→L2)"),
    ],
    'WHAT': [
        ("Domain Reframing", "Reframe in anderer FEPSDE-Dimension"),
        ("Multi-Domain Bundling", "Verknüpfe mehrere Utility-Dimensionen"),
    ],
    'HOW': [
        ("Pre-Commitment Device", "Bindung an zukünftiges Verhalten"),
        ("Goal Setting", "SMART-Ziele mit Feedback"),
        ("Implementation Intentions", "Wenn-Dann Pläne"),
    ],
    'WHEN': [
        ("Default Setting", "Setze vorteilhafte Standardoption"),
        ("Choice Architecture", "Strukturiere Entscheidungsumgebung"),
        ("Timing Optimization", "Fresh Start Effect nutzen"),
        ("Deadline/Urgency", "Zeitliche Begrenzung setzen"),
    ],
    'WHERE': [
        ("Point-of-Decision Prompt", "Erinnerung am Entscheidungsort"),
        ("Environmental Restructuring", "Physische Umgebung ändern"),
    ],
    'READY': [
        ("Self-Efficacy Building", "Stärke Überzeugung, es zu schaffen"),
        ("Barrier Reduction", "Reduziere wahrgenommene Hürden"),
    ],
    'STAGE': [
        ("Stage-Matched Messaging", "Botschaft an BCJ-Phase anpassen"),
        ("Journey Acceleration", "Beschleunige zur nächsten Phase"),
    ],
    'HIER': [
        ("Simplification", "Reduziere kognitive Komplexität"),
    ],

    # Block B: AWARE-Detail (Selection)
    'Self_INU_F_pos': [
        ("Hidden Benefits Revelation", "Zeige versteckte finanzielle Vorteile"),
        ("Personalized Projection", "Individualisierte finanzielle Prognose"),
        ("Compound Interest Calculator", "Interaktiver Zinseszins-Rechner"),
    ],
    'Self_INU_F_neg': [
        ("Cost Revelation", "Zeige versteckte Kosten"),
        ("Loss Preview", "Simuliere potenzielle Verluste"),
        ("Opportunity Cost Display", "Zeige Opportunitätskosten"),
    ],
    'Self_INU_E_pos': [
        ("Emotional Benefit Framing", "Betone emotionale Vorteile"),
        ("Testimonial Stories", "Erfahrungsberichte über emotionale Gewinne"),
        ("Peace of Mind Messaging", "Ruhe und Sicherheit betonen"),
    ],
    'Self_INU_E_neg': [
        ("Anticipated Regret", "Aktiviere erwartete Reue"),
        ("Stress/Anxiety Preview", "Zeige emotionale Kosten"),
    ],
    'Self_KNU_F_pos': [
        ("Future Self Visualization", "Gealterte Foto-App / Brief an zukünftiges Selbst"),
        ("Compound Interest Demonstration", "Animierter Wachstumsgraph"),
        ("Progress Tracking", "Spar-Fortschrittsbalken"),
        ("Reminder/Salience", "Push-Notification: 'Ihr Sparziel wartet'"),
        ("Goal Proximity Display", "'Nur noch CHF X bis Ziel'"),
    ],
    'Self_KNU_F_neg': [
        ("Loss Salience", "Tägliche statt jährliche Kosten zeigen"),
        ("Regret Anticipation", "Vergangene Reue aktivieren"),
        ("Daily Cost Calculator", "'Sie verlieren CHF X pro Tag'"),
    ],
    'Self_KNU_E_pos': [
        ("Emotional Memory Activation", "Positive Erinnerungen aktivieren"),
        ("Success Visualization", "Erfolgsmomente zeigen"),
    ],
    'Self_KNU_S_pos': [
        ("Social Proof Reminder", "'73% Ihrer Nachbarn sparen bereits'"),
        ("Peer Comparison", "Vergleich mit ähnlichen Personen"),
        ("Leaderboard", "Rangliste"),
        ("Recognition/Badges", "Achievement System"),
    ],
    'Self_KNU_Ex_pos': [
        ("Experience Reminder", "Fotos von positiven Erlebnissen"),
        ("Simulation Preview", "VR-Vorschau auf Zukunft"),
    ],
    'Self_IDN_F_pos': [
        ("Progress Tracking", "Zeige Fortschritt zu Ziel"),
        ("Milestone Celebrations", "Feiere Etappenziele"),
        ("Endowed Progress Effect", "Fortschritt 'schenken'"),
    ],
    'Comm_INU_F_pos': [
        ("Collective Benefit Information", "Zeige Nutzen für Gemeinschaft"),
        ("Community Dashboard", "Aggregierte Ersparnisse zeigen"),
    ],
    'Comm_KNU_S_pos': [
        ("Community Norms", "Zeige was andere tun"),
        ("Community Challenges", "Gemeinsame Herausforderungen"),
        ("Social Capital Reminder", "Netzwerk-Wert betonen"),
    ],
}

def get_mechanisms_for_dimension(
    dim: str,
    scope_level: str = 'tactical',
    min_affinity: float = 0.3
) -> List[Tuple[str, str, float]]:
    """
    Get concrete intervention mechanisms for a dimension, filtered by scope affinity.

    Args:
        dim: Dimension name (e.g., 'Self_KNU_F_pos', 'WHO')
        scope_level: Scope level for affinity filtering
        min_affinity: Minimum affinity threshold (default 0.3)

    Returns:
        List of (name, description, affinity) tuples, sorted by affinity descending
    """
    raw_mechanisms = []

    # Direct match
    if dim in INTERVENTION_CATALOG:
        raw_mechanisms = INTERVENTION_CATALOG[dim]
    else:
        # Pattern matching for AWARE-detail dimensions
        for pattern, mechanisms in INTERVENTION_CATALOG.items():
            if pattern in dim:
                raw_mechanisms = mechanisms
                break

    # Default fallback based on dimension components
    if not raw_mechanisms and '_' in dim:
        parts = dim.split('_')
        ref, util, dom, val = parts[0], parts[1], parts[2], parts[3]

        if util == 'INU':
            raw_mechanisms.append(("Information Provision", f"Informiere über {dom}-Effekte"))
        elif util == 'KNU':
            raw_mechanisms.append(("Salience/Reminder", f"Erinnere an bekannte {dom}-Effekte"))
        elif util == 'IDN':
            raw_mechanisms.append(("Progress Tracking", f"Zeige Fortschritt bei {dom}"))

        if val == 'pos':
            raw_mechanisms.append(("Benefit Framing", "Betone positive Aspekte"))
        else:
            raw_mechanisms.append(("Loss Framing", "Betone zu vermeidende Verluste"))

    if not raw_mechanisms:
        raw_mechanisms = [("Generic Intervention", "Kontextspezifische Maßnahme entwickeln")]

    # Add affinity scores and filter
    mechanisms_with_affinity = []
    for name, desc in raw_mechanisms:
        affinity = get_mechanism_affinity(name, scope_level)
        if affinity >= min_affinity:
            mechanisms_with_affinity.append((name, desc, affinity))

    # Sort by affinity descending
    mechanisms_with_affinity.sort(key=lambda x: x[2], reverse=True)

    # If all filtered out, return at least one with lowest threshold
    if not mechanisms_with_affinity and raw_mechanisms:
        name, desc = raw_mechanisms[0]
        affinity = get_mechanism_affinity(name, scope_level)
        mechanisms_with_affinity = [(name, desc, affinity)]

    return mechanisms_with_affinity


def format_result(result: InterventionResult) -> str:
    """Format EMERGE result as readable output."""
    lines = []
    lines.append("\n" + "="*70)
    lines.append("EMERGENT INTERVENTION PROFILE")
    lines.append("="*70)

    # Scope information (EIT-EMP-3)
    scope_info = SCOPE_LEVELS.get(result.scope_level, SCOPE_LEVELS['tactical'])
    lines.append(f"\nScope Level: {result.scope_level.upper()} (L{scope_info['level']})")
    lines.append(f"  Duration:  {scope_info['duration']}")
    lines.append(f"  Type:      {scope_info['type']}")

    lines.append(f"\nContext Ψ:")
    lines.append(f"  Economic:      {result.context.economic:.2f} {'(recession)' if result.context.economic < 0.3 else '(boom)' if result.context.economic > 0.7 else ''}")
    lines.append(f"  Social Norms:  {result.context.social:.2f} {'(weak)' if result.context.social < 0.3 else '(strong)' if result.context.social > 0.7 else ''}")
    lines.append(f"  Temporal:      {result.context.temporal:.2f}")

    lines.append(f"\nOptimal Intervention Profile (I⃗*):")
    lines.append("-"*50)

    sorted_profile = sorted(result.profile.items(), key=lambda x: x[1], reverse=True)
    for dim, intensity in sorted_profile:
        bar = "█" * int(intensity * 20)
        lines.append(f"  {dim:30s} I={intensity:.2f} {bar}")

    lines.append(f"\nTotal Effectiveness E*: {result.effectiveness:.3f}")

    # Show K rationale if available
    if result.k_rationale:
        lines.append(f"\nK-Optimal Berechnung:")
        lines.append(f"  {result.k_rationale['formula']}")

    if result.avoided_pairs:
        lines.append(f"\nAvoided Combinations (crowding-out risk):")
        for d1, d2 in result.avoided_pairs[:5]:
            gamma = compute_gamma_context(d1, d2, result.context)
            lines.append(f"  {d1} + {d2}: γ={gamma:.2f}")

    lines.append("\n" + "="*70)
    lines.append(f"KONKRETE INTERVENTIONEN für {result.scope_level.upper()}")
    lines.append(f"(Mechanismen gefiltert nach Scope-Affinity α ≥ 0.3)")
    lines.append("="*70)

    def affinity_stars(alpha: float) -> str:
        """Convert affinity to star rating."""
        if alpha >= 0.9: return "★★★"
        if alpha >= 0.7: return "★★☆"
        if alpha >= 0.5: return "★☆☆"
        return "☆☆☆"

    total_mechanisms = 0
    high_affinity_count = 0
    specs_shown = []  # Track which specs to show in detail

    for dim, intensity in sorted_profile:
        mechanisms = get_mechanisms_for_dimension(dim, scope_level=result.scope_level)
        lines.append(f"\n▶ {dim} (I={intensity:.2f})")
        lines.append("-" * 50)
        for name, desc, affinity in mechanisms:
            stars = affinity_stars(affinity)
            lines.append(f"   {stars} {name} (α={affinity:.1f})")
            lines.append(f"       → {desc}")
            total_mechanisms += 1
            if affinity >= 0.7:
                high_affinity_count += 1
                # Collect high-affinity mechanisms for detailed specs
                spec = get_intervention_spec(name)
                if spec and name not in [s.name for s in specs_shown]:
                    specs_shown.append(spec)

    lines.append(f"\n{'─'*70}")
    lines.append(f"TOTAL: {len(sorted_profile)} Dimensionen × {total_mechanisms} Mechanismen")
    lines.append(f"       {high_affinity_count} mit hoher Scope-Affinity (α ≥ 0.7)")
    lines.append(f"{'─'*70}")

    # Show detailed specifications for high-affinity mechanisms
    if specs_shown:
        lines.append("\n" + "="*70)
        lines.append("DETAILLIERTE SPEZIFIKATIONEN (Top-Mechanismen)")
        lines.append("="*70)

        for spec in specs_shown[:3]:  # Show top 3 detailed specs
            lines.append(f"\n┌{'─'*68}┐")
            lines.append(f"│ {spec.name:66s} │")
            lines.append(f"├{'─'*68}┤")
            lines.append(f"│ ZIEL: {spec.ziel[:60]:60s} │")
            lines.append(f"├{'─'*68}┤")
            lines.append(f"│ IN-SCOPE:{'':58s} │")
            for item in spec.in_scope[:3]:
                lines.append(f"│   ✓ {item[:62]:62s} │")
            lines.append(f"├{'─'*68}┤")
            lines.append(f"│ OUT-OF-SCOPE:{'':54s} │")
            for item in spec.out_of_scope[:2]:
                lines.append(f"│   ✗ {item[:62]:62s} │")
            lines.append(f"├{'─'*68}┤")
            lines.append(f"│ LIEFEROBJEKTE:{'':53s} │")
            for item in spec.lieferobjekte[:3]:
                lines.append(f"│   □ {item[:62]:62s} │")
            lines.append(f"└{'─'*68}┘")

    lines.append("\n" + "="*70)
    lines.append("INTERPRETATION")
    lines.append("="*70)

    # Generate interpretation
    primary = sorted_profile[0] if sorted_profile else None
    if primary:
        dim_name = primary[0]
        if '_' in dim_name:
            parts = dim_name.split('_')
            ref = "eigene" if parts[0] == "Self" else "gemeinschaftliche"
            util = {"INU": "Unbekannte", "KNU": "Bekannte-Nicht-Genutzte", "IDN": "Identifizierte"}[parts[1]]
            dom = {"F": "finanzielle", "E": "emotionale", "P": "physische", "S": "soziale", "D": "development", "Ex": "Erfahrungs-"}[parts[2]]
            val = "positive" if parts[3] == "pos" else "negative"
            lines.append(f"\nPrimäre Intervention: Stärke Awareness für {val} {dom}")
            lines.append(f"                      Effekte auf {ref} {util} Utility")

    lines.append("\n" + "="*70)

    return "\n".join(lines)

# =============================================================================
# DEMO SCENARIOS
# =============================================================================

def run_demo():
    """Run demonstration scenarios."""
    print("\n" + "="*70)
    print("EMERGE ALGORITHM DEMONSTRATION")
    print("="*70)

    scenarios = [
        {
            "name": "Retirement Savings (Strategic)",
            "context": Context(economic=0.3, social=0.8, temporal=0.7),
            "target": "Self_KNU_F",
            "scope": "strategic",
            "stage": "contemplation",
        },
        {
            "name": "Smoking Cessation (Tactical)",
            "context": Context(economic=0.5, social=0.5, temporal=0.3),
            "target": "Self_INU",
            "scope": "tactical",
            "stage": "action",
        },
        {
            "name": "ERP Adoption (Systemic)",
            "context": Context(economic=0.6, social=0.9, temporal=0.8, institutional=0.7),
            "target": "Comm",
            "scope": "systemic",
            "stage": "preparation",
        },
    ]

    for scenario in scenarios:
        print(f"\n\n{'#'*70}")
        print(f"SCENARIO: {scenario['name']}")
        print(f"{'#'*70}")

        result = emerge(
            context=scenario["context"],
            target=scenario["target"],
            scope_level=scenario.get("scope", "tactical"),
            stage=scenario.get("stage", "preparation"),
            verbose=True
        )

        print(format_result(result))

# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="EMERGE Algorithm - Compute optimal intervention profiles"
    )
    parser.add_argument("--demo", action="store_true", help="Run demonstration scenarios")
    parser.add_argument("--context", type=str, help="Context as key=value pairs (e.g., 'econ=0.3,social=0.7')")
    parser.add_argument("--target", type=str, default="AWARE", help="Target outcome")
    parser.add_argument("--budget", type=float, default=100.0, help="Budget constraint")
    parser.add_argument("--k", type=int, default=None, help="Complexity limit (max active dimensions, computed if omitted)")
    parser.add_argument("--scope", type=str, default="tactical",
                       choices=["instant", "operative", "tactical", "strategic", "systemic"],
                       help="Scope level (EIT-EMP-3): instant/operative/tactical/strategic/systemic")
    parser.add_argument("--stage", type=str, default="preparation",
                       choices=["pre_contemplation", "contemplation", "preparation", "action", "maintenance"],
                       help="BCJ stage for K computation")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    if args.demo:
        run_demo()
        return

    if args.context:
        # Parse context string
        context_dict = {}
        for pair in args.context.split(','):
            key, value = pair.split('=')
            context_dict[key.strip()] = float(value.strip())
        context = Context.from_dict(context_dict)
    else:
        # Default context
        context = Context()

    result = emerge(
        context=context,
        target=args.target,
        budget=args.budget,
        complexity_limit=args.k,
        scope_level=args.scope,
        stage=args.stage,
        verbose=args.verbose
    )

    print(format_result(result))

if __name__ == "__main__":
    main()
