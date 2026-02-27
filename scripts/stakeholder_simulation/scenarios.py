"""
Scenario Engine for Stakeholder Simulation
What-if analysis: How do stakeholder probabilities change with parameter modifications?

Version: 1.0.0
"""

from dataclasses import dataclass
from typing import Dict, Optional
from enum import Enum

# ============================================================================
# SCENARIO DEFINITIONS
# ============================================================================

class ScenarioCategory(Enum):
    """Scenario classification"""
    ECONOMIC = "Economic / Market"
    EXECUTION = "Execution / Operations"
    STRATEGIC = "Strategic / Leadership"
    LEARNING = "Learning Loop / Data"

@dataclass
class Scenario:
    """Definition of a what-if scenario"""
    name: str
    description: str
    category: ScenarioCategory
    adjustments: Dict[str, float]  # 10C adjustments: where_adjustment, when_adjustment, etc.
    financial_impact: Optional[str] = None  # e.g., "-€20M revenue"
    recommendation: Optional[str] = None  # Should we execute or avoid?

# ============================================================================
# SCENARIO LIBRARY: 15+ Scenarios
# ============================================================================

class ScenarioLibrary:
    """Complete library of what-if scenarios"""

    # ====================================================================
    # ECONOMIC / MARKET CHANGES (5 scenarios)
    # ====================================================================

    GDP_SLOWDOWN_1PP = Scenario(
        name="gdp_slowdown_1pp",
        description="GDP growth slows: 2.8% → 1.8%",
        category=ScenarioCategory.ECONOMIC,
        adjustments={
            "when_adjustment": 0.15,  # Context risk increases
            "where_adjustment": -0.10,  # Revenue forecast confidence decreases
            "ready_adjustment": -0.05,  # Org becomes more risk-averse
        },
        financial_impact="€50-100M revenue impact (volume decline)",
        recommendation="Monitor monthly; may trigger capex delay"
    )

    RECESSION = Scenario(
        name="recession",
        description="Economic recession: GDP 2.8% → -0.5%",
        category=ScenarioCategory.ECONOMIC,
        adjustments={
            "when_adjustment": 0.35,  # Major context shock
            "where_adjustment": -0.25,  # Forecast confidence erodes
            "ready_adjustment": -0.15,  # Org very risk-averse
            "aware_adjustment": -0.10,  # Distraction from recession news
        },
        financial_impact="-€200-300M revenue",
        recommendation="Likely to trigger capex delay & board re-evaluation"
    )

    MARKET_EXPANSION_2X = Scenario(
        name="market_expansion_2x",
        description="TAM grows 2x: €10B → €20B opportunity",
        category=ScenarioCategory.ECONOMIC,
        adjustments={
            "when_adjustment": -0.15,  # Favorable market timing
            "what_adjustment": 0.20,  # Strategic alignment improves
            "ready_adjustment": 0.10,  # Org more willing to invest
        },
        financial_impact="+€100-150M revenue opportunity",
        recommendation="Accelerate execution; increase investments"
    )

    COMPETITOR_PRICE_WAR = Scenario(
        name="competitor_price_war",
        description="Competitor initiates aggressive pricing",
        category=ScenarioCategory.ECONOMIC,
        adjustments={
            "when_adjustment": 0.20,  # Market disruption
            "what_adjustment": -0.10,  # Our offering looks less attractive
            "aware_adjustment": -0.05,  # Customer confusion
        },
        financial_impact="-€30-50M if we match; -€80M if we don't",
        recommendation="Avoid price war; differentiate on value"
    )

    COMMODITY_PRICE_SHOCK = Scenario(
        name="commodity_price_shock",
        description="Raw material costs up 20%",
        category=ScenarioCategory.ECONOMIC,
        adjustments={
            "when_adjustment": 0.25,  # Supply chain shock
            "where_adjustment": -0.15,  # Cost structure uncertainty
        },
        financial_impact="-€40-60M EBITDA if absorbed",
        recommendation="May require price increase; negotiate with suppliers"
    )

    # ====================================================================
    # EXECUTION / OPERATIONS CHANGES (5 scenarios)
    # ====================================================================

    CAPEX_DELAY_6MO = Scenario(
        name="capex_delay_6mo",
        description="Phase 1 capex delayed 6 months",
        category=ScenarioCategory.EXECUTION,
        adjustments={
            "when_adjustment": 0.20,  # Timeline risk
            "how_adjustment": -0.15,  # Org capability execution delayed
            "where_adjustment": -0.08,  # CAGR timing assumptions broken
        },
        financial_impact="-€100-150M revenue delay",
        recommendation="Reassess board approval; may need phase gate re-approval"
    )

    ORG_RESTRUCTURE = Scenario(
        name="org_restructure",
        description="Major organizational restructuring",
        category=ScenarioCategory.EXECUTION,
        adjustments={
            "when_adjustment": 0.25,  # Disruption during restructure
            "how_adjustment": -0.20,  # Org capability degraded
            "aware_adjustment": -0.15,  # Employees confused about new structure
            "ready_adjustment": -0.20,  # Willingness to execute decreases
        },
        financial_impact="-€200-300M (productivity loss + turnover)",
        recommendation="Critical: Align restructure with strategy timeline"
    )

    KEY_PERSON_LEAVES = Scenario(
        name="key_person_leaves",
        description="CEO or CFO departure",
        category=ScenarioCategory.EXECUTION,
        adjustments={
            "how_adjustment": -0.25,  # Org capability severely degraded
            "aware_adjustment": -0.20,  # Leadership vacuum; unclear direction
            "ready_adjustment": -0.25,  # Org paralyzed during transition
            "hierarchy_adjustment": -0.30,  # Decision-making authority unclear
        },
        financial_impact="-€100-200M (strategic uncertainty)",
        recommendation="Announce interim/permanent successor immediately"
    )

    QUALITY_ISSUE = Scenario(
        name="quality_issue",
        description="Product quality defect discovered",
        category=ScenarioCategory.EXECUTION,
        adjustments={
            "what_adjustment": -0.30,  # Product doesn't meet quality requirements
            "where_adjustment": -0.20,  # Confidence in quality erodes
            "aware_adjustment": -0.15,  # Negative publicity
        },
        financial_impact="-€50-100M (recalls, lost sales)",
        recommendation="Rapid quality fix required; communicate transparently"
    )

    SUPPLY_CHAIN_DISRUPTION = Scenario(
        name="supply_chain_disruption",
        description="Critical supplier capacity unavailable",
        category=ScenarioCategory.EXECUTION,
        adjustments={
            "when_adjustment": 0.30,  # Supply risk
            "how_adjustment": -0.25,  # Cannot deliver at planned volumes
            "where_adjustment": -0.15,  # Revenue forecast at risk
        },
        financial_impact="-€75-125M revenue if cannot fulfill",
        recommendation="Diversify suppliers; secure alternative capacity"
    )

    # ====================================================================
    # STRATEGIC / LEADERSHIP CHANGES (3 scenarios)
    # ====================================================================

    PRICE_INCREASE_10PCT = Scenario(
        name="price_increase_10pct",
        description="Increase prices by 10%",
        category=ScenarioCategory.STRATEGIC,
        adjustments={
            "what_adjustment": -0.10,  # Lower perceived value
            "ready_adjustment": -0.08,  # Customer willingness decreases
            # For customers specifically: Additional -30% loss aversion penalty
        },
        financial_impact="+€50M price, -€70M volume = -€20M net",
        recommendation="DON'T increase: Demand too elastic (-1.3% elasticity)"
    )

    PRICE_DECREASE_10PCT = Scenario(
        name="price_decrease_10pct",
        description="Decrease prices by 10%",
        category=ScenarioCategory.STRATEGIC,
        adjustments={
            "what_adjustment": 0.15,  # Higher perceived value
            "ready_adjustment": 0.12,  # Customer willingness increases
        },
        financial_impact="-€50M price, +€120M volume = +€70M net",
        recommendation="CONSIDER: Gains market share; increases customer probability"
    )

    MERGE_WITH_COMPETITOR = Scenario(
        name="merge_with_competitor",
        description="Strategic M&A with competitor",
        category=ScenarioCategory.STRATEGIC,
        adjustments={
            "how_adjustment": 0.25,  # Org capability increases significantly
            "what_adjustment": 0.20,  # Combined offering stronger
            "when_adjustment": -0.20,  # Strategic timing excellent
            "aware_adjustment": -0.10,  # M&A disruption/integration
            "hierarchy_adjustment": -0.25,  # Governance complexity increases
        },
        financial_impact="+€300-500M (synergies) net of -€200M (integration costs)",
        recommendation="Requires board approval & clear integration plan"
    )

    # ====================================================================
    # LEARNING LOOP / DATA CHANGES (2 scenarios)
    # ====================================================================

    Q1_ACTUAL_MISS_10PCT = Scenario(
        name="q1_actual_miss_10pct",
        description="Q1 actual misses forecast by 10% (€285B → €256B)",
        category=ScenarioCategory.LEARNING,
        adjustments={
            "where_adjustment": -0.15,  # Parameter confidence erodes
            "ready_adjustment": -0.10,  # C-Suite/Board confidence decreases
            "aware_adjustment": -0.08,  # Negative news impacts stakeholders
        },
        financial_impact="-€29M Q1 miss (can be caught up later)",
        recommendation="Implement corrective actions; monthly tracking increases"
    )

    E_THETA_SHRINKS_CONFIDENCE = Scenario(
        name="confidence_tightens",
        description="E(θ) shrinks after 2 quarters: ±0.8pp → ±0.6pp",
        category=ScenarioCategory.LEARNING,
        adjustments={
            "where_adjustment": 0.08,  # Parameter confidence INCREASES
            "aware_adjustment": 0.10,  # Greater certainty improves briefing
            "ready_adjustment": 0.05,  # More confidence to approve
        },
        financial_impact="None (non-financial benefit)",
        recommendation="Positive: Board approval probability increases 5-8pp"
    )

    REGIME_CHANGE_DETECTED = Scenario(
        name="regime_change_detected",
        description="Major context shift detected: ΔΨ > 2.0σ",
        category=ScenarioCategory.LEARNING,
        adjustments={
            "when_adjustment": 0.35,  # Major context shock
            "where_adjustment": -0.20,  # Old parameters no longer valid
            "aware_adjustment": 0.00,  # New reality; may improve over time
            "ready_adjustment": -0.15,  # Org uncertain about new environment
        },
        financial_impact="Highly variable depending on nature of change",
        recommendation="Trigger emergency board review; reforecast required"
    )

# ============================================================================
# SCENARIO MANAGER
# ============================================================================

class ScenarioManager:
    """Manage scenarios: lookup, execute, compare"""

    # Full scenario library
    ALL_SCENARIOS = {
        "gdp_slowdown_1pp": ScenarioLibrary.GDP_SLOWDOWN_1PP,
        "recession": ScenarioLibrary.RECESSION,
        "market_expansion_2x": ScenarioLibrary.MARKET_EXPANSION_2X,
        "competitor_price_war": ScenarioLibrary.COMPETITOR_PRICE_WAR,
        "commodity_price_shock": ScenarioLibrary.COMMODITY_PRICE_SHOCK,
        "capex_delay_6mo": ScenarioLibrary.CAPEX_DELAY_6MO,
        "org_restructure": ScenarioLibrary.ORG_RESTRUCTURE,
        "key_person_leaves": ScenarioLibrary.KEY_PERSON_LEAVES,
        "quality_issue": ScenarioLibrary.QUALITY_ISSUE,
        "supply_chain_disruption": ScenarioLibrary.SUPPLY_CHAIN_DISRUPTION,
        "price_increase_10pct": ScenarioLibrary.PRICE_INCREASE_10PCT,
        "price_decrease_10pct": ScenarioLibrary.PRICE_DECREASE_10PCT,
        "merge_with_competitor": ScenarioLibrary.MERGE_WITH_COMPETITOR,
        "q1_actual_miss_10pct": ScenarioLibrary.Q1_ACTUAL_MISS_10PCT,
        "confidence_tightens": ScenarioLibrary.E_THETA_SHRINKS_CONFIDENCE,
        "regime_change_detected": ScenarioLibrary.REGIME_CHANGE_DETECTED,
    }

    @staticmethod
    def get_scenario(scenario_name: str) -> Scenario:
        """Get scenario definition by name"""
        if scenario_name not in ScenarioManager.ALL_SCENARIOS:
            raise ValueError(f"Unknown scenario: {scenario_name}. Available: {list(ScenarioManager.ALL_SCENARIOS.keys())}")
        return ScenarioManager.ALL_SCENARIOS[scenario_name]

    @staticmethod
    def list_scenarios(category: Optional[ScenarioCategory] = None) -> Dict[str, Scenario]:
        """List all scenarios, optionally filtered by category"""
        if category is None:
            return ScenarioManager.ALL_SCENARIOS

        return {
            name: scenario
            for name, scenario in ScenarioManager.ALL_SCENARIOS.items()
            if scenario.category == category
        }

    @staticmethod
    def get_scenario_adjustments(scenario_name: str) -> Dict[str, float]:
        """Get 10C adjustments for a scenario"""
        scenario = ScenarioManager.get_scenario(scenario_name)
        return scenario.adjustments

    @staticmethod
    def get_scenario_description(scenario_name: str) -> str:
        """Get human-readable description"""
        scenario = ScenarioManager.get_scenario(scenario_name)
        return f"{scenario.description}\n{scenario.financial_impact}\n→ {scenario.recommendation}"

# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("SCENARIO LIBRARY")
    print("=" * 70)

    # List all economic scenarios
    print("\nECONOMIC SCENARIOS:")
    for name, scenario in ScenarioManager.list_scenarios(ScenarioCategory.ECONOMIC).items():
        print(f"  {name}: {scenario.description}")

    print("\nEXECUTION SCENARIOS:")
    for name, scenario in ScenarioManager.list_scenarios(ScenarioCategory.EXECUTION).items():
        print(f"  {name}: {scenario.description}")

    print("\nSTRATEGIC SCENARIOS:")
    for name, scenario in ScenarioManager.list_scenarios(ScenarioCategory.STRATEGIC).items():
        print(f"  {name}: {scenario.description}")

    print("\nLEARNING LOOP SCENARIOS:")
    for name, scenario in ScenarioManager.list_scenarios(ScenarioCategory.LEARNING).items():
        print(f"  {name}: {scenario.description}")

    # Example: Get adjustments for price increase scenario
    print("\n" + "=" * 70)
    print("EXAMPLE: Price Increase +10% Scenario")
    scenario = ScenarioManager.get_scenario("price_increase_10pct")
    print(f"Description: {scenario.description}")
    print(f"Financial Impact: {scenario.financial_impact}")
    print(f"Adjustments: {scenario.adjustments}")
    print(f"Recommendation: {scenario.recommendation}")
