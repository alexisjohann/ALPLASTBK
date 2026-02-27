"""
ICM-1.0: Iteration Convergence Model

Generic Theory for Optimal Iteration Count in Strategic Planning

Mathematical Framework:
-----------------------
The convergence of top-down targets and bottom-up capacity follows
an exponential decay pattern where each iteration reduces the gap
by a characteristic factor.

Key Equation:
    G(n) = G₀ · λⁿ

Where:
    G(n) = Gap after n iterations
    G₀   = Initial gap (top-down - bottom-up)
    λ    = Convergence rate (0 < λ < 1)
    n    = Number of iterations

Optimal Iteration Count:
    n* = ⌈log(ε/G₀) / log(λ)⌉

Where:
    ε = Acceptable gap threshold (e.g., 5%)
    n* = Optimal number of iterations

Factors Affecting λ (Convergence Rate):
1. Data Quality (DQ): Better data → faster convergence
2. Model Complexity (MC): More complex → slower convergence
3. Organizational Alignment (OA): Better alignment → faster convergence
4. Market Volatility (MV): Higher volatility → slower convergence
5. Planning Horizon (PH): Longer horizon → slower convergence

λ = λ_base · f(DQ) · f(MC) · f(OA) · f(MV) · f(PH)

Author: Claude (Strategic Models Team)
Version: 1.0.0
Created: 2026-01-16
"""

import math
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from enum import Enum


class ConvergenceFactorLevel(Enum):
    """Levels for convergence factors."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class ConvergenceFactor:
    """A factor affecting convergence rate."""
    name: str
    level: ConvergenceFactorLevel
    multiplier: float
    description: str


@dataclass
class IterationResult:
    """Result of a single iteration."""
    iteration: int
    gap_before: float
    gap_after: float
    gap_reduction: float
    cumulative_effort: float
    marginal_benefit: float


@dataclass
class ConvergenceAnalysis:
    """Complete convergence analysis result."""
    initial_gap: float
    target_gap: float
    convergence_rate: float
    optimal_iterations: int
    iterations: List[IterationResult]
    total_effort: float
    efficiency_ratio: float
    recommendation: str
    factors: Dict[str, ConvergenceFactor]


# Factor multiplier tables
FACTOR_MULTIPLIERS = {
    "data_quality": {
        ConvergenceFactorLevel.LOW: 0.7,    # Poor data → slower convergence
        ConvergenceFactorLevel.MEDIUM: 1.0,
        ConvergenceFactorLevel.HIGH: 1.3,   # Excellent data → faster convergence
    },
    "model_complexity": {
        ConvergenceFactorLevel.LOW: 1.2,    # Simple models → faster convergence
        ConvergenceFactorLevel.MEDIUM: 1.0,
        ConvergenceFactorLevel.HIGH: 0.8,   # Complex models → slower convergence
    },
    "organizational_alignment": {
        ConvergenceFactorLevel.LOW: 0.6,    # Poor alignment → slower convergence
        ConvergenceFactorLevel.MEDIUM: 1.0,
        ConvergenceFactorLevel.HIGH: 1.4,   # Strong alignment → faster convergence
    },
    "market_volatility": {
        ConvergenceFactorLevel.LOW: 1.2,    # Stable market → faster convergence
        ConvergenceFactorLevel.MEDIUM: 1.0,
        ConvergenceFactorLevel.HIGH: 0.7,   # Volatile market → slower convergence
    },
    "planning_horizon": {
        ConvergenceFactorLevel.LOW: 1.3,    # Short horizon (1-2y) → faster
        ConvergenceFactorLevel.MEDIUM: 1.0, # Medium horizon (3-5y)
        ConvergenceFactorLevel.HIGH: 0.8,   # Long horizon (5-10y) → slower
    },
}

# Base convergence rate (empirically derived from typical planning cycles)
BASE_CONVERGENCE_RATE = 0.5  # Each iteration typically closes 50% of remaining gap


def calculate_convergence_rate(
    data_quality: ConvergenceFactorLevel = ConvergenceFactorLevel.MEDIUM,
    model_complexity: ConvergenceFactorLevel = ConvergenceFactorLevel.MEDIUM,
    organizational_alignment: ConvergenceFactorLevel = ConvergenceFactorLevel.MEDIUM,
    market_volatility: ConvergenceFactorLevel = ConvergenceFactorLevel.MEDIUM,
    planning_horizon: ConvergenceFactorLevel = ConvergenceFactorLevel.MEDIUM,
) -> Tuple[float, Dict[str, ConvergenceFactor]]:
    """
    Calculate the convergence rate λ based on organizational factors.

    The convergence rate determines how quickly the gap between
    top-down targets and bottom-up capacity closes with each iteration.

    Args:
        data_quality: Quality of planning data (LOW/MEDIUM/HIGH)
        model_complexity: Complexity of business models (LOW/MEDIUM/HIGH)
        organizational_alignment: Cross-functional alignment (LOW/MEDIUM/HIGH)
        market_volatility: Market uncertainty level (LOW/MEDIUM/HIGH)
        planning_horizon: Planning time horizon (LOW=1-2y, MEDIUM=3-5y, HIGH=5-10y)

    Returns:
        Tuple of (convergence_rate, factors_dict)
    """
    factors = {}

    # Data Quality Factor
    dq_mult = FACTOR_MULTIPLIERS["data_quality"][data_quality]
    factors["data_quality"] = ConvergenceFactor(
        name="Data Quality",
        level=data_quality,
        multiplier=dq_mult,
        description="Quality and availability of planning data"
    )

    # Model Complexity Factor
    mc_mult = FACTOR_MULTIPLIERS["model_complexity"][model_complexity]
    factors["model_complexity"] = ConvergenceFactor(
        name="Model Complexity",
        level=model_complexity,
        multiplier=mc_mult,
        description="Complexity of business and financial models"
    )

    # Organizational Alignment Factor
    oa_mult = FACTOR_MULTIPLIERS["organizational_alignment"][organizational_alignment]
    factors["organizational_alignment"] = ConvergenceFactor(
        name="Organizational Alignment",
        level=organizational_alignment,
        multiplier=oa_mult,
        description="Cross-functional coordination and buy-in"
    )

    # Market Volatility Factor
    mv_mult = FACTOR_MULTIPLIERS["market_volatility"][market_volatility]
    factors["market_volatility"] = ConvergenceFactor(
        name="Market Volatility",
        level=market_volatility,
        multiplier=mv_mult,
        description="Uncertainty in market conditions"
    )

    # Planning Horizon Factor
    ph_mult = FACTOR_MULTIPLIERS["planning_horizon"][planning_horizon]
    factors["planning_horizon"] = ConvergenceFactor(
        name="Planning Horizon",
        level=planning_horizon,
        multiplier=ph_mult,
        description="Time horizon of strategic plan"
    )

    # Calculate adjusted convergence rate
    # Higher rate = faster convergence (gap closes faster)
    combined_multiplier = dq_mult * mc_mult * oa_mult * mv_mult * ph_mult

    # λ is the gap RETENTION rate (how much gap remains after iteration)
    # Lower λ = faster convergence
    # We invert the multiplier effect: better factors → lower λ → faster convergence
    lambda_rate = BASE_CONVERGENCE_RATE / combined_multiplier

    # Bound λ between 0.2 and 0.8
    lambda_rate = max(0.2, min(0.8, lambda_rate))

    return lambda_rate, factors


def calculate_optimal_iterations(
    initial_gap: float,
    target_gap: float,
    convergence_rate: float,
) -> int:
    """
    Calculate the optimal number of iterations using the convergence formula.

    Formula: n* = ⌈log(ε/G₀) / log(λ)⌉

    Args:
        initial_gap: Initial gap G₀ (as decimal, e.g., 0.25 for 25%)
        target_gap: Acceptable gap threshold ε (as decimal, e.g., 0.05 for 5%)
        convergence_rate: Convergence rate λ (0 < λ < 1)

    Returns:
        Optimal number of iterations n*
    """
    if initial_gap <= target_gap:
        return 0

    if convergence_rate <= 0 or convergence_rate >= 1:
        raise ValueError("Convergence rate must be between 0 and 1")

    # n* = log(ε/G₀) / log(λ)
    n_star = math.log(target_gap / initial_gap) / math.log(convergence_rate)

    # Round up to nearest integer
    return math.ceil(n_star)


def simulate_iterations(
    initial_gap: float,
    convergence_rate: float,
    max_iterations: int = 10,
    effort_per_iteration: float = 1.0,
) -> List[IterationResult]:
    """
    Simulate the iteration process and calculate metrics for each round.

    Args:
        initial_gap: Initial gap G₀
        convergence_rate: Convergence rate λ
        max_iterations: Maximum iterations to simulate
        effort_per_iteration: Relative effort per iteration (can increase with n)

    Returns:
        List of IterationResult for each iteration
    """
    results = []
    current_gap = initial_gap
    cumulative_effort = 0.0

    for n in range(1, max_iterations + 1):
        gap_before = current_gap
        gap_after = current_gap * convergence_rate
        gap_reduction = gap_before - gap_after

        # Effort increases slightly with each iteration (diminishing returns on easy fixes)
        iteration_effort = effort_per_iteration * (1 + 0.1 * (n - 1))
        cumulative_effort += iteration_effort

        # Marginal benefit = gap reduction / effort
        marginal_benefit = gap_reduction / iteration_effort if iteration_effort > 0 else 0

        results.append(IterationResult(
            iteration=n,
            gap_before=gap_before,
            gap_after=gap_after,
            gap_reduction=gap_reduction,
            cumulative_effort=cumulative_effort,
            marginal_benefit=marginal_benefit,
        ))

        current_gap = gap_after

    return results


def analyze_convergence(
    initial_gap: float = 0.25,
    target_gap: float = 0.05,
    data_quality: ConvergenceFactorLevel = ConvergenceFactorLevel.MEDIUM,
    model_complexity: ConvergenceFactorLevel = ConvergenceFactorLevel.MEDIUM,
    organizational_alignment: ConvergenceFactorLevel = ConvergenceFactorLevel.MEDIUM,
    market_volatility: ConvergenceFactorLevel = ConvergenceFactorLevel.MEDIUM,
    planning_horizon: ConvergenceFactorLevel = ConvergenceFactorLevel.MEDIUM,
) -> ConvergenceAnalysis:
    """
    Complete convergence analysis for strategic planning iterations.

    This is the main entry point for the ICM-1.0 model.

    Args:
        initial_gap: Initial gap between top-down and bottom-up (default 25%)
        target_gap: Acceptable gap threshold (default 5%)
        data_quality: Quality of planning data
        model_complexity: Complexity of business models
        organizational_alignment: Cross-functional alignment
        market_volatility: Market uncertainty level
        planning_horizon: Planning time horizon

    Returns:
        ConvergenceAnalysis with complete results and recommendation
    """
    # Calculate convergence rate based on factors
    convergence_rate, factors = calculate_convergence_rate(
        data_quality=data_quality,
        model_complexity=model_complexity,
        organizational_alignment=organizational_alignment,
        market_volatility=market_volatility,
        planning_horizon=planning_horizon,
    )

    # Calculate optimal iterations
    optimal_n = calculate_optimal_iterations(initial_gap, target_gap, convergence_rate)

    # Simulate all iterations up to optimal + 2 (for comparison)
    iterations = simulate_iterations(
        initial_gap=initial_gap,
        convergence_rate=convergence_rate,
        max_iterations=min(optimal_n + 2, 10),
    )

    # Calculate total effort at optimal iteration
    total_effort = iterations[optimal_n - 1].cumulative_effort if optimal_n > 0 else 0

    # Efficiency ratio = gap closed / effort
    gap_closed = initial_gap - (iterations[optimal_n - 1].gap_after if optimal_n > 0 else initial_gap)
    efficiency_ratio = gap_closed / total_effort if total_effort > 0 else 0

    # Generate recommendation
    recommendation = _generate_recommendation(
        optimal_n=optimal_n,
        convergence_rate=convergence_rate,
        factors=factors,
    )

    return ConvergenceAnalysis(
        initial_gap=initial_gap,
        target_gap=target_gap,
        convergence_rate=convergence_rate,
        optimal_iterations=optimal_n,
        iterations=iterations,
        total_effort=total_effort,
        efficiency_ratio=efficiency_ratio,
        recommendation=recommendation,
        factors=factors,
    )


def _generate_recommendation(
    optimal_n: int,
    convergence_rate: float,
    factors: Dict[str, ConvergenceFactor],
) -> str:
    """Generate a recommendation based on analysis results."""

    # Identify bottleneck factors (those slowing convergence)
    bottlenecks = []
    accelerators = []

    for name, factor in factors.items():
        if factor.multiplier < 1.0:
            bottlenecks.append(factor.name)
        elif factor.multiplier > 1.0:
            accelerators.append(factor.name)

    # Build recommendation
    parts = []

    if optimal_n <= 2:
        parts.append(f"Fast convergence expected ({optimal_n} iterations).")
    elif optimal_n <= 4:
        parts.append(f"Standard convergence ({optimal_n} iterations).")
    else:
        parts.append(f"Slow convergence expected ({optimal_n} iterations).")

    if bottlenecks:
        parts.append(f"Bottlenecks: {', '.join(bottlenecks)}.")

    if accelerators:
        parts.append(f"Strengths: {', '.join(accelerators)}.")

    # Specific improvement suggestions
    if "Organizational Alignment" in bottlenecks:
        parts.append("Consider: Cross-functional planning workshops before iterations.")

    if "Data Quality" in bottlenecks:
        parts.append("Consider: Data validation sprint before planning cycle.")

    if "Market Volatility" in bottlenecks:
        parts.append("Consider: Scenario-based planning with wider tolerance bands.")

    return " ".join(parts)


# =============================================================================
# Extended Theory: Cost-Benefit Optimization
# =============================================================================

@dataclass
class CostBenefitAnalysis:
    """Cost-benefit analysis for iteration count decision."""
    optimal_n_pure: int          # Optimal n based on gap alone
    optimal_n_economic: int      # Optimal n considering costs
    cost_per_iteration: float    # Estimated cost per iteration
    benefit_per_percent: float   # Value of 1% gap reduction
    net_benefits: List[float]    # Net benefit at each iteration
    break_even_iteration: int    # Where marginal cost = marginal benefit
    recommendation: str


def analyze_cost_benefit(
    convergence_analysis: ConvergenceAnalysis,
    cost_per_iteration: float = 50000.0,  # Default: 50k CHF per iteration
    benefit_per_percent_gap: float = 100000.0,  # Default: 100k CHF value per 1% gap reduction
) -> CostBenefitAnalysis:
    """
    Economic optimization of iteration count.

    This extends the pure convergence analysis with cost-benefit considerations.

    The economic optimum occurs where:
        Marginal Benefit = Marginal Cost

    Or equivalently:
        dB/dn = dC/dn

    Where:
        B(n) = Total benefit from gap reduction
        C(n) = Total cost of iterations

    Args:
        convergence_analysis: Results from analyze_convergence()
        cost_per_iteration: Cost of one planning iteration (CHF)
        benefit_per_percent_gap: Value of reducing gap by 1% (CHF)

    Returns:
        CostBenefitAnalysis with economic optimization
    """
    iterations = convergence_analysis.iterations
    initial_gap = convergence_analysis.initial_gap

    net_benefits = []
    break_even = 0

    for i, iteration in enumerate(iterations):
        # Total benefit = gap closed * value per percent
        gap_closed_percent = (initial_gap - iteration.gap_after) * 100
        total_benefit = gap_closed_percent * benefit_per_percent_gap

        # Total cost = iterations * cost
        total_cost = (i + 1) * cost_per_iteration * (1 + 0.1 * i)  # Increasing cost

        # Net benefit
        net_benefit = total_benefit - total_cost
        net_benefits.append(net_benefit)

        # Find break-even (where adding another iteration isn't worth it)
        if i > 0:
            marginal_benefit = (gap_closed_percent -
                              (initial_gap - iterations[i-1].gap_after) * 100) * benefit_per_percent_gap
            marginal_cost = cost_per_iteration * (1 + 0.1 * i)

            if marginal_benefit < marginal_cost and break_even == 0:
                break_even = i  # Previous iteration was optimal

    # Find economically optimal n (max net benefit)
    optimal_economic = net_benefits.index(max(net_benefits)) + 1

    # Generate recommendation
    if optimal_economic < convergence_analysis.optimal_iterations:
        rec = (f"Economic optimum ({optimal_economic}) is less than convergence optimum "
               f"({convergence_analysis.optimal_iterations}). "
               f"Consider accepting higher gap tolerance to save costs.")
    elif optimal_economic > convergence_analysis.optimal_iterations:
        rec = (f"Gap target is achieved before economic optimum. "
               f"Consider tighter gap tolerance for additional value.")
    else:
        rec = f"Economic and convergence optima align at {optimal_economic} iterations."

    return CostBenefitAnalysis(
        optimal_n_pure=convergence_analysis.optimal_iterations,
        optimal_n_economic=optimal_economic,
        cost_per_iteration=cost_per_iteration,
        benefit_per_percent=benefit_per_percent_gap,
        net_benefits=net_benefits,
        break_even_iteration=break_even if break_even > 0 else optimal_economic,
        recommendation=rec,
    )


# =============================================================================
# Stopping Rule Theory
# =============================================================================

@dataclass
class StoppingRule:
    """A rule for determining when to stop iterating."""
    name: str
    description: str
    check_function: str  # Name of check function
    threshold: float


STOPPING_RULES = [
    StoppingRule(
        name="Gap Threshold",
        description="Stop when gap falls below threshold",
        check_function="gap_below_threshold",
        threshold=0.05,
    ),
    StoppingRule(
        name="Marginal Improvement",
        description="Stop when improvement < 1% of previous",
        check_function="marginal_improvement_low",
        threshold=0.01,
    ),
    StoppingRule(
        name="Economic Break-Even",
        description="Stop when marginal cost > marginal benefit",
        check_function="economic_break_even",
        threshold=1.0,  # Ratio of marginal benefit to cost
    ),
    StoppingRule(
        name="Time Constraint",
        description="Stop after maximum iterations",
        check_function="max_iterations",
        threshold=4.0,
    ),
    StoppingRule(
        name="Consensus Reached",
        description="Stop when all stakeholders approve",
        check_function="consensus_approval",
        threshold=0.8,  # 80% approval rate
    ),
]


def recommend_stopping_rule(
    time_pressure: ConvergenceFactorLevel = ConvergenceFactorLevel.MEDIUM,
    precision_requirement: ConvergenceFactorLevel = ConvergenceFactorLevel.MEDIUM,
    budget_constraint: ConvergenceFactorLevel = ConvergenceFactorLevel.MEDIUM,
) -> List[StoppingRule]:
    """
    Recommend stopping rules based on organizational context.

    Args:
        time_pressure: How urgent is the planning deadline
        precision_requirement: How precise must the plan be
        budget_constraint: How tight is the planning budget

    Returns:
        Ordered list of recommended stopping rules
    """
    rules = []

    # High time pressure → prioritize time constraint
    if time_pressure == ConvergenceFactorLevel.HIGH:
        rules.append(STOPPING_RULES[3])  # Time Constraint first

    # High precision → prioritize gap threshold
    if precision_requirement == ConvergenceFactorLevel.HIGH:
        rules.append(STOPPING_RULES[0])  # Gap Threshold
        rules.append(STOPPING_RULES[1])  # Marginal Improvement

    # High budget constraint → prioritize economic break-even
    if budget_constraint == ConvergenceFactorLevel.HIGH:
        rules.append(STOPPING_RULES[2])  # Economic Break-Even

    # Add remaining rules in standard order
    for rule in STOPPING_RULES:
        if rule not in rules:
            rules.append(rule)

    return rules


# =============================================================================
# Main Function for Model Library
# =============================================================================

def analyze_iteration_convergence(
    initial_gap_percent: float = 25.0,
    target_gap_percent: float = 5.0,
    data_quality: str = "medium",
    model_complexity: str = "medium",
    organizational_alignment: str = "medium",
    market_volatility: str = "medium",
    planning_horizon: str = "medium",
    cost_per_iteration: Optional[float] = None,
    benefit_per_percent: Optional[float] = None,
) -> Dict:
    """
    Main entry point for ICM-1.0: Iteration Convergence Model.

    Determines the optimal number of planning iterations based on
    convergence theory and organizational factors.

    Args:
        initial_gap_percent: Initial gap (default 25%)
        target_gap_percent: Target gap (default 5%)
        data_quality: "low", "medium", or "high"
        model_complexity: "low", "medium", or "high"
        organizational_alignment: "low", "medium", or "high"
        market_volatility: "low", "medium", or "high"
        planning_horizon: "low" (1-2y), "medium" (3-5y), "high" (5-10y)
        cost_per_iteration: Optional cost per iteration for economic analysis
        benefit_per_percent: Optional benefit per 1% gap reduction

    Returns:
        Dictionary with complete analysis results
    """
    # Convert string levels to enum
    level_map = {
        "low": ConvergenceFactorLevel.LOW,
        "medium": ConvergenceFactorLevel.MEDIUM,
        "high": ConvergenceFactorLevel.HIGH,
    }

    # Run convergence analysis
    analysis = analyze_convergence(
        initial_gap=initial_gap_percent / 100,
        target_gap=target_gap_percent / 100,
        data_quality=level_map.get(data_quality.lower(), ConvergenceFactorLevel.MEDIUM),
        model_complexity=level_map.get(model_complexity.lower(), ConvergenceFactorLevel.MEDIUM),
        organizational_alignment=level_map.get(organizational_alignment.lower(), ConvergenceFactorLevel.MEDIUM),
        market_volatility=level_map.get(market_volatility.lower(), ConvergenceFactorLevel.MEDIUM),
        planning_horizon=level_map.get(planning_horizon.lower(), ConvergenceFactorLevel.MEDIUM),
    )

    # Prepare base result
    result = {
        "model": "ICM-1.0",
        "model_name": "Iteration Convergence Model",
        "version": "1.0.0",
        "convergence_analysis": {
            "initial_gap_percent": initial_gap_percent,
            "target_gap_percent": target_gap_percent,
            "convergence_rate": round(analysis.convergence_rate, 3),
            "optimal_iterations": analysis.optimal_iterations,
            "efficiency_ratio": round(analysis.efficiency_ratio, 4),
        },
        "iteration_trajectory": [
            {
                "iteration": it.iteration,
                "gap_before_percent": round(it.gap_before * 100, 2),
                "gap_after_percent": round(it.gap_after * 100, 2),
                "gap_reduction_percent": round(it.gap_reduction * 100, 2),
                "marginal_benefit": round(it.marginal_benefit, 4),
            }
            for it in analysis.iterations
        ],
        "factors": {
            name: {
                "level": factor.level.value,
                "multiplier": factor.multiplier,
                "description": factor.description,
            }
            for name, factor in analysis.factors.items()
        },
        "recommendation": analysis.recommendation,
        "theory": {
            "formula": "G(n) = G₀ · λⁿ",
            "optimal_formula": "n* = ⌈log(ε/G₀) / log(λ)⌉",
            "interpretation": (
                f"With λ={analysis.convergence_rate:.3f}, each iteration retains "
                f"{analysis.convergence_rate*100:.1f}% of the remaining gap "
                f"(closes {(1-analysis.convergence_rate)*100:.1f}%)."
            ),
        },
    }

    # Add economic analysis if cost/benefit provided
    if cost_per_iteration is not None and benefit_per_percent is not None:
        cost_benefit = analyze_cost_benefit(
            analysis,
            cost_per_iteration=cost_per_iteration,
            benefit_per_percent_gap=benefit_per_percent,
        )
        result["economic_analysis"] = {
            "optimal_n_pure": cost_benefit.optimal_n_pure,
            "optimal_n_economic": cost_benefit.optimal_n_economic,
            "cost_per_iteration": cost_benefit.cost_per_iteration,
            "benefit_per_percent": cost_benefit.benefit_per_percent,
            "break_even_iteration": cost_benefit.break_even_iteration,
            "net_benefits": [round(nb, 0) for nb in cost_benefit.net_benefits],
            "recommendation": cost_benefit.recommendation,
        }

    return result


if __name__ == "__main__":
    # Demo: Analyze convergence for a typical enterprise planning scenario
    print("=" * 70)
    print("ICM-1.0: Iteration Convergence Model - Demo")
    print("=" * 70)

    # Scenario 1: Typical medium-complexity organization
    print("\n--- Scenario 1: Typical Organization ---")
    result = analyze_iteration_convergence(
        initial_gap_percent=25.0,
        target_gap_percent=5.0,
    )
    print(f"Optimal Iterations: {result['convergence_analysis']['optimal_iterations']}")
    print(f"Convergence Rate (λ): {result['convergence_analysis']['convergence_rate']}")
    print(f"Recommendation: {result['recommendation']}")

    # Scenario 2: High volatility, poor alignment
    print("\n--- Scenario 2: Challenging Environment ---")
    result = analyze_iteration_convergence(
        initial_gap_percent=30.0,
        target_gap_percent=5.0,
        market_volatility="high",
        organizational_alignment="low",
    )
    print(f"Optimal Iterations: {result['convergence_analysis']['optimal_iterations']}")
    print(f"Convergence Rate (λ): {result['convergence_analysis']['convergence_rate']}")
    print(f"Recommendation: {result['recommendation']}")

    # Scenario 3: Well-prepared organization
    print("\n--- Scenario 3: Well-Prepared Organization ---")
    result = analyze_iteration_convergence(
        initial_gap_percent=20.0,
        target_gap_percent=5.0,
        data_quality="high",
        organizational_alignment="high",
        market_volatility="low",
    )
    print(f"Optimal Iterations: {result['convergence_analysis']['optimal_iterations']}")
    print(f"Convergence Rate (λ): {result['convergence_analysis']['convergence_rate']}")
    print(f"Recommendation: {result['recommendation']}")

    # Scenario 4: With economic analysis
    print("\n--- Scenario 4: Economic Optimization ---")
    result = analyze_iteration_convergence(
        initial_gap_percent=25.0,
        target_gap_percent=5.0,
        cost_per_iteration=50000,
        benefit_per_percent=100000,
    )
    print(f"Pure Optimal: {result['economic_analysis']['optimal_n_pure']} iterations")
    print(f"Economic Optimal: {result['economic_analysis']['optimal_n_economic']} iterations")
    print(f"Economic Recommendation: {result['economic_analysis']['recommendation']}")

    print("\n" + "=" * 70)
    print("Trajectory for Scenario 1:")
    print("-" * 70)
    for it in result["iteration_trajectory"]:
        print(f"  Iteration {it['iteration']}: Gap {it['gap_before_percent']:.1f}% → {it['gap_after_percent']:.1f}%")
