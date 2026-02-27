"""
Stakeholder Simulation Engine - Phase 6
Predict stakeholder decisions using 10C CORE framework + behavioral economics

Phase: 6 (Stakeholder Behavior Simulation)
Status: ACTIVE
Version: 1.0.0
Created: 2026-01-16

Key Components:
- stakeholder_simulator.py: Core decision engine (12 stakeholder types)
- scenarios.py: What-if scenario library (15+ scenarios)
- output_formatters.py: Output formatting (summary/detailed/matrix/scenario)

Usage:
    from stakeholder_simulation import StakeholderSimulator, ScenarioManager, OutputFormatter
    from stakeholder_simulation import NineCAdjustments

    # Initialize
    simulator = StakeholderSimulator()

    # Create adjustments
    adjustments = NineCAdjustments(
        WHERE_confidence=0.82,
        WHEN_context_risk=0.25,
        HOW_capability=0.85,
        WHAT_alignment=0.80,
        HIERARCHY_clarity=0.90,
        AWARE_briefing=0.95,
        READY_willingness=0.88,
    )

    # Single decision
    result = simulator.simulate("board", adjustments)
    print(OutputFormatter.format_summary(result))

    # What-if scenario
    scenario = ScenarioManager.get_scenario("price_increase_10pct")
    result_scenario = simulator.simulate("customer", adjustments, scenario.adjustments)
    print(OutputFormatter.format_scenario(result, result_scenario, "Price +10%", "..."))

    # All stakeholders
    all_results = simulator.simulate_all_stakeholders(adjustments)
    print(OutputFormatter.format_matrix(all_results))
"""

from stakeholder_simulator import (
    StakeholderSimulator,
    DecisionFunctions,
    NineCAdjustments,
    StakeholderDecision,
    ConfidenceLevel,
    RiskZone,
)

from scenarios import (
    Scenario,
    ScenarioLibrary,
    ScenarioManager,
    ScenarioCategory,
)

from output_formatters import (
    OutputFormatter,
)

from change_journey import (
    ChangeJourneyManager,
    JourneyProgress,
    JourneyStage,
)

from behavior_dashboard import (
    MonthlyHealthScorecard,
    DashboardExporter,
)

__all__ = [
    # Main simulator
    "StakeholderSimulator",
    "DecisionFunctions",

    # Data classes
    "NineCAdjustments",
    "StakeholderDecision",
    "ConfidenceLevel",
    "RiskZone",

    # Scenarios
    "Scenario",
    "ScenarioLibrary",
    "ScenarioManager",
    "ScenarioCategory",

    # Formatters
    "OutputFormatter",

    # Change Journey
    "ChangeJourneyManager",
    "JourneyProgress",
    "JourneyStage",

    # Dashboard
    "MonthlyHealthScorecard",
    "DashboardExporter",
]

__version__ = "1.0.0"
__author__ = "Complementarity Context Framework"
