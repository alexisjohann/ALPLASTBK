"""
Output Formatters for Stakeholder Simulation Results
Formats results as: Summary, Detailed, Matrix, Scenario Analysis

Version: 1.0.0
"""

import json
from typing import Dict, List, Optional, Tuple
from dataclasses import asdict
from stakeholder_simulator import StakeholderDecision, RiskZone

# ============================================================================
# OUTPUT FORMATTER - MAIN ORCHESTRATOR
# ============================================================================

class OutputFormatter:
    """Formats simulation results in different formats"""

    @staticmethod
    def format_summary(result: StakeholderDecision) -> str:
        """
        Format result as brief summary (default output)

        Output:
        APPROVAL PROBABILITY: 84.3% ✓ HIGH CONFIDENCE
        Key Drivers: WHERE +25.5%, WHEN +17.0%, ...
        Red Flags: NONE
        Timeline: 2 weeks to decision
        """
        output = []

        # Header
        output.append("╔═══════════════════════════════════════════════════════════════╗")
        output.append(f"║ {result.stakeholder_type.upper():60} ║")
        output.append(f"║ Decision: {result.decision_name:50} ║")
        output.append("╚═══════════════════════════════════════════════════════════════╝")
        output.append("")

        # Probability
        output.append(f"DECISION PROBABILITY: {result.probability:.1%} {result.risk_zone.value}")
        output.append(f"Confidence Level: {result.confidence_level.value}")
        output.append("")

        # Key Drivers
        output.append("Key Drivers (10C CORE):")
        sorted_drivers = sorted(result.key_drivers.items(), key=lambda x: abs(x[1]), reverse=True)
        for driver, value in sorted_drivers:
            sign = "+" if value > 0 else ""
            output.append(f"  {driver:20} {sign}{value:6.1f}%")
        output.append("")

        # Conditions Met
        if result.conditions_met:
            output.append("Conditions Met:")
            for condition in result.conditions_met:
                output.append(f"  {condition}")
            output.append("")

        # Red Flags
        if result.red_flags:
            output.append("Red Flags:")
            for flag in result.red_flags:
                output.append(f"  ⚠ {flag}")
            output.append("")
        else:
            output.append("Red Flags: NONE")
            output.append("")

        # Timeline
        output.append(f"Timeline to Decision: {result.timeline_to_decision}")
        output.append(f"Timeline to Execution: {result.timeline_to_execution}")

        return "\n".join(output)

    @staticmethod
    def format_detailed(result: StakeholderDecision) -> str:
        """
        Format result as detailed analysis

        Includes:
        - Full 10C dimensional breakdown
        - Historical comparison
        - Behavioral factors
        - Recommended interventions
        """
        output = []

        # Header
        output.append("╔═══════════════════════════════════════════════════════════════╗")
        output.append(f"║ DETAILED ANALYSIS: {result.stakeholder_type.upper():40} ║")
        output.append(f"║ {result.decision_name:60} ║")
        output.append("╚═══════════════════════════════════════════════════════════════╝")
        output.append("")

        # Probability with interpretation
        output.append(f"DECISION PROBABILITY: {result.probability:.1%}")
        output.append(f"Confidence Level: {result.confidence_level.value}")
        output.append(f"Risk Zone: {result.risk_zone.value}")
        output.append("")

        # Interpretation
        if result.probability >= 0.80:
            interpretation = "✓ GREEN LIGHT: High confidence; proceed as planned"
        elif result.probability >= 0.65:
            interpretation = "✓ YELLOW: On track; monitor closely for changes"
        elif result.probability >= 0.50:
            interpretation = "⚠ ORANGE: Needs attention; targeted engagement required"
        else:
            interpretation = "🔴 RED: High risk; immediate action needed"

        output.append(f"Interpretation: {interpretation}")
        output.append("")

        # 10C Dimensional Breakdown
        output.append("10C CORE Dimension Contributors:")
        output.append("┌─────────────────────┬────────────────┐")
        output.append("│ Dimension           │ Contribution   │")
        output.append("├─────────────────────┼────────────────┤")

        sorted_drivers = sorted(result.key_drivers.items(), key=lambda x: abs(x[1]), reverse=True)
        for driver, value in sorted_drivers:
            sign = "+" if value > 0 else ""
            output.append(f"│ {driver:19} │ {sign}{value:7.1f}%    │")

        output.append("└─────────────────────┴────────────────┘")
        output.append("")

        # Conditions Met & Red Flags
        output.append("Decision Analysis:")
        output.append(f"  Conditions Met: {len(result.conditions_met)}")
        for condition in result.conditions_met:
            output.append(f"    {condition}")

        output.append(f"  Red Flags: {len(result.red_flags)}")
        for flag in result.red_flags:
            output.append(f"    ⚠ {flag}")

        output.append("")

        # Timeline
        output.append("Timeline:")
        output.append(f"  To Decision: {result.timeline_to_decision}")
        output.append(f"  To Execution: {result.timeline_to_execution}")

        return "\n".join(output)

    @staticmethod
    def format_matrix(results: Dict[str, StakeholderDecision]) -> str:
        """
        Format all stakeholders as decision probability heatmap

        Output:
        ┌─────────────────────┬──────────────┬──────────────┬──────────────┐
        │ Stakeholder Type    │ Primary Decis.│ Probability  │ Confidence   │
        ├─────────────────────┼──────────────┼──────────────┼──────────────┤
        │ Board               │ Approve      │ 84% ✓✓       │ VERY HIGH    │
        ...
        """
        output = []

        # Header
        output.append("╔════════════════════════════════════════════════════════════════════╗")
        output.append("║ FULL STAKEHOLDER SIMULATION MATRIX - All 12 Types                 ║")
        output.append("╚════════════════════════════════════════════════════════════════════╝")
        output.append("")

        # Heatmap table
        output.append("DECISION PROBABILITY HEATMAP:")
        output.append("┌─────────────────────┬──────────────┬──────────────┬──────────────┐")
        output.append("│ Stakeholder Type    │ Primary Decis│ Probability  │ Confidence   │")
        output.append("├─────────────────────┼──────────────┼──────────────┼──────────────┤")

        # Sort by probability (highest first)
        sorted_results = sorted(results.items(), key=lambda x: x[1].probability, reverse=True)

        for stakeholder_type, result in sorted_results:
            name = stakeholder_type.replace("_", " ").title()[:19]
            decision = result.decision_name[:12]
            prob_str = f"{result.probability:.0%} {result.risk_zone.value}"
            conf = result.confidence_level.value[:8]

            output.append(f"│ {name:19} │ {decision:12} │ {prob_str:12} │ {conf:12} │")

        output.append("└─────────────────────┴──────────────┴──────────────┴──────────────┘")
        output.append("")

        # Risk Zone Summary
        green_count = sum(1 for r in results.values() if r.probability >= 0.80)
        yellow_count = sum(1 for r in results.values() if 0.65 <= r.probability < 0.80)
        orange_count = sum(1 for r in results.values() if 0.50 <= r.probability < 0.65)
        red_count = sum(1 for r in results.values() if r.probability < 0.50)

        output.append("RISK ZONE SUMMARY:")
        output.append(f"  ✓ GREEN (≥80%): {green_count} stakeholders - Execution likely")
        output.append(f"  ✓ YELLOW (65-80%): {yellow_count} stakeholders - On track, monitor")
        output.append(f"  ⚠ ORANGE (50-65%): {orange_count} stakeholders - Needs attention")
        output.append(f"  🔴 RED (<50%): {red_count} stakeholders - High risk, intervention needed")
        output.append("")

        # Critical Path Success Probability
        critical_path_prob = 1.0
        for stakeholder_type in ["board", "regional_pl", "capex_committee", "fpa"]:
            if stakeholder_type in results:
                critical_path_prob *= results[stakeholder_type].probability

        output.append(f"Critical Path Success Probability: {critical_path_prob:.0%}")
        output.append("  (Board × Regional P&L × Capex × FP&A approval)")
        output.append("")

        # Top risks
        output.append("TOP RISKS (Lowest Probabilities):")
        for i, (stakeholder_type, result) in enumerate(sorted_results[-3:], 1):
            name = stakeholder_type.replace("_", " ").title()
            output.append(f"  {i}. {name}: {result.probability:.0%}")
            if result.red_flags:
                for flag in result.red_flags[:2]:  # First 2 flags only
                    output.append(f"     → {flag}")

        return "\n".join(output)

    @staticmethod
    def format_scenario(baseline: StakeholderDecision,
                       scenario: StakeholderDecision,
                       scenario_name: str,
                       scenario_description: str) -> str:
        """
        Format scenario analysis: Baseline vs Scenario comparison

        Output:
        SCENARIO ANALYSIS: Price Increase +10%

        Baseline vs Scenario Comparison:
        │ Baseline  │ Scenario  │ Δ Impact
        Board      84%       82%       -2pp
        Customer   41%       28%       -13pp ⚠
        """
        output = []

        # Header
        output.append("╔═════════════════════════════════════════════════════════════════╗")
        output.append(f"║ SCENARIO ANALYSIS: {scenario_name.upper():50} ║")
        output.append(f"║ {scenario_description:60} ║")
        output.append("╚═════════════════════════════════════════════════════════════════╝")
        output.append("")

        # Single stakeholder impact
        output.append(f"STAKEHOLDER: {baseline.stakeholder_type.upper()}")
        output.append("")

        output.append("BASELINE vs SCENARIO IMPACT:")
        output.append("┌──────────────┬──────────┬──────────┬──────────┐")
        output.append("│ Aspect       │ Baseline │ Scenario │ Impact   │")
        output.append("├──────────────┼──────────┼──────────┼──────────┤")

        prob_delta = scenario.probability - baseline.probability
        delta_sign = "+" if prob_delta > 0 else ""
        delta_emoji = "↑" if prob_delta > 0 else "↓"

        output.append(f"│ Probability  │ {baseline.probability:6.0%}   │ {scenario.probability:6.0%}   │ {delta_sign}{prob_delta:6.0%} {delta_emoji} │")

        if scenario.confidence_level != baseline.confidence_level:
            output.append(f"│ Confidence   │ {baseline.confidence_level.value:8} │ {scenario.confidence_level.value:8} │ Changed  │")

        if scenario.risk_zone != baseline.risk_zone:
            output.append(f"│ Risk Zone    │ {baseline.risk_zone.value:8} │ {scenario.risk_zone.value:8} │ Changed  │")

        output.append("└──────────────┴──────────┴──────────┴──────────┘")
        output.append("")

        # Interpretation
        if abs(prob_delta) < 0.05:
            interpretation = "Minimal impact: Scenario doesn't significantly affect decision"
        elif prob_delta > 0:
            interpretation = f"Positive impact: Scenario improves decision probability by {prob_delta:.0%}pp"
        else:
            interpretation = f"Negative impact: Scenario reduces decision probability by {abs(prob_delta):.0%}pp"

        output.append(f"Interpretation: {interpretation}")
        output.append("")

        # Key Driver Changes
        output.append("Driver Sensitivity:")
        baseline_drivers = baseline.key_drivers
        scenario_drivers = scenario.key_drivers

        for driver in sorted(set(baseline_drivers.keys()) | set(scenario_drivers.keys())):
            baseline_val = baseline_drivers.get(driver, 0)
            scenario_val = scenario_drivers.get(driver, 0)
            driver_delta = scenario_val - baseline_val

            if abs(driver_delta) > 0.1:  # Only show meaningful changes
                sign = "+" if driver_delta > 0 else ""
                output.append(f"  {driver:20} {baseline_val:+6.1f}% → {scenario_val:+6.1f}% ({sign}{driver_delta:+.1f}%)")

        output.append("")

        # Recommendation
        output.append("Scenario Recommendation:")
        if prob_delta < -0.10:
            recommendation = "❌ AVOID: Negative impact on decision probability"
        elif prob_delta < -0.05:
            recommendation = "⚠ CAUTION: Negative impact; mitigate risks"
        elif prob_delta > 0.10:
            recommendation = "✅ RECOMMEND: Positive impact; accelerate"
        elif prob_delta > 0.05:
            recommendation = "✓ ACCEPTABLE: Minor positive impact"
        else:
            recommendation = "⚪ NEUTRAL: Scenario has minimal impact"

        output.append(f"  {recommendation}")

        return "\n".join(output)

    @staticmethod
    def format_json(result: StakeholderDecision) -> str:
        """Format result as JSON for programmatic access"""
        return json.dumps({
            "stakeholder_type": result.stakeholder_type,
            "decision_name": result.decision_name,
            "probability": round(result.probability, 4),
            "confidence_level": result.confidence_level.value,
            "risk_zone": result.risk_zone.value,
            "key_drivers": {k: round(v, 2) for k, v in result.key_drivers.items()},
            "red_flags": result.red_flags,
            "conditions_met": result.conditions_met,
            "timeline_to_decision": result.timeline_to_decision,
            "timeline_to_execution": result.timeline_to_execution,
        }, indent=2)

    @staticmethod
    def format_csv_row(result: StakeholderDecision) -> str:
        """Format result as CSV row"""
        return ",".join([
            result.stakeholder_type,
            result.decision_name,
            f"{result.probability:.2%}",
            result.confidence_level.value,
            result.risk_zone.value,
            str(len(result.red_flags)),
            str(len(result.conditions_met)),
        ])

# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Example output formatting (requires actual results)
    print("OUTPUT FORMATTER EXAMPLES")
    print("=" * 70)
    print("See /simulate-stakeholder skill for usage examples")
