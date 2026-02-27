"""
Behavior Matrix Dashboard - Phase 6 Week 3
Monthly stakeholder health scorecard + probability tracking

Exports to CSV/JSON for reporting and trending
Integrates with quarterly learning loop for probability updates

Version: 1.0.0
"""

import json
import csv
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import asdict
from stakeholder_simulator import StakeholderDecision, RiskZone

# ============================================================================
# MONTHLY HEALTH SCORECARD
# ============================================================================

class MonthlyHealthScorecard:
    """Generate monthly stakeholder health report"""

    @staticmethod
    def create_scorecard(customer_name: str,
                        results: Dict[str, StakeholderDecision],
                        previous_results: Optional[Dict[str, StakeholderDecision]] = None) -> Dict:
        """
        Create comprehensive monthly health scorecard

        Args:
            customer_name: Customer/project name
            results: Current month's stakeholder decisions
            previous_results: Previous month's results (for trending)

        Returns:
            Dictionary with scorecard data
        """
        current_date = datetime.now()

        # Calculate summary metrics
        green_count = sum(1 for r in results.values() if r.probability >= 0.80)
        yellow_count = sum(1 for r in results.values() if 0.65 <= r.probability < 0.80)
        orange_count = sum(1 for r in results.values() if 0.50 <= r.probability < 0.65)
        red_count = sum(1 for r in results.values() if r.probability < 0.50)

        # Calculate critical path
        critical_path_prob = MonthlyHealthScorecard._calculate_critical_path(results)

        # Risk assessment
        risk_level = MonthlyHealthScorecard._assess_risk_level(
            green_count, yellow_count, orange_count, red_count, critical_path_prob
        )

        # Trend analysis
        trends = {}
        if previous_results:
            trends = MonthlyHealthScorecard._calculate_trends(results, previous_results)

        # Identify action items
        action_items = MonthlyHealthScorecard._identify_action_items(results)

        return {
            "report_date": current_date.isoformat(),
            "customer": customer_name,
            "summary": {
                "total_stakeholders": len(results),
                "green": green_count,
                "yellow": yellow_count,
                "orange": orange_count,
                "red": red_count,
                "critical_path_success": round(critical_path_prob, 2),
                "overall_risk": risk_level,
            },
            "stakeholder_details": {
                k: {
                    "probability": round(v.probability, 4),
                    "confidence": v.confidence_level.value,
                    "risk_zone": v.risk_zone.value,
                    "red_flags": v.red_flags,
                    "conditions_met": len(v.conditions_met),
                    "trend": trends.get(k, "stable"),
                }
                for k, v in results.items()
            },
            "trends": trends,
            "action_items": action_items,
            "recommendations": MonthlyHealthScorecard._generate_recommendations(results, risk_level),
        }

    @staticmethod
    def _calculate_critical_path(results: Dict[str, StakeholderDecision]) -> float:
        """Calculate critical path success probability"""
        critical_stakeholders = ["board", "regional_pl", "capex_committee", "fpa"]
        critical_path_prob = 1.0

        for stakeholder in critical_stakeholders:
            if stakeholder in results:
                critical_path_prob *= results[stakeholder].probability

        return critical_path_prob

    @staticmethod
    def _assess_risk_level(green: int, yellow: int, orange: int, red: int, critical_path: float) -> str:
        """Assess overall risk level"""
        # RED: If any critical stakeholder < 70% OR critical path < 40%
        if red > 0 or critical_path < 0.40:
            return "CRITICAL"

        # ORANGE: If orange > 3 OR critical path < 50%
        if orange > 3 or critical_path < 0.50:
            return "HIGH"

        # YELLOW: If any critical stakeholder < 65% OR orange ≤ 3
        if yellow > 2 or (orange > 0 and critical_path < 0.60):
            return "MEDIUM"

        # GREEN: All good
        return "LOW"

    @staticmethod
    def _calculate_trends(results: Dict[str, StakeholderDecision],
                         previous: Dict[str, StakeholderDecision]) -> Dict[str, str]:
        """Calculate month-over-month trends"""
        trends = {}

        for stakeholder_type, current in results.items():
            if stakeholder_type not in previous:
                trends[stakeholder_type] = "new"
                continue

            previous_prob = previous[stakeholder_type].probability
            current_prob = current.probability
            delta = current_prob - previous_prob

            if abs(delta) < 0.03:
                trends[stakeholder_type] = "stable"
            elif delta > 0.05:
                trends[stakeholder_type] = "improving ↑"
            elif delta < -0.05:
                trends[stakeholder_type] = "declining ↓"
            else:
                trends[stakeholder_type] = "slight change"

        return trends

    @staticmethod
    def _identify_action_items(results: Dict[str, StakeholderDecision]) -> List[Dict]:
        """Identify priority action items"""
        action_items = []

        for stakeholder_type, result in results.items():
            # Priority 1: RED zone stakeholders
            if result.probability < 0.50:
                action_items.append({
                    "priority": "CRITICAL",
                    "stakeholder": stakeholder_type,
                    "issue": f"LOW approval probability ({result.probability:.0%})",
                    "action": MonthlyHealthScorecard._get_intervention(stakeholder_type, result),
                    "timeline": "This week",
                })

            # Priority 2: RED flags identified
            elif result.red_flags:
                for flag in result.red_flags[:2]:  # First 2 flags
                    action_items.append({
                        "priority": "HIGH",
                        "stakeholder": stakeholder_type,
                        "issue": flag,
                        "action": f"Address concern with {stakeholder_type}",
                        "timeline": "Next 1-2 weeks",
                    })

            # Priority 3: ORANGE zone
            elif 0.50 <= result.probability < 0.65:
                action_items.append({
                    "priority": "MEDIUM",
                    "stakeholder": stakeholder_type,
                    "issue": f"Moderate approval risk ({result.probability:.0%})",
                    "action": "Targeted engagement + additional information",
                    "timeline": "Next 2-3 weeks",
                })

        # Sort by priority
        priority_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
        action_items.sort(key=lambda x: priority_order[x["priority"]])

        return action_items[:5]  # Top 5 actions

    @staticmethod
    def _get_intervention(stakeholder_type: str, result: StakeholderDecision) -> str:
        """Get specific intervention recommendation"""
        interventions = {
            "customer": "Reduce switching barriers: Risk-free trial + case studies + customization",
            "employee": "Increase engagement: Manager briefings + transparent communication + career path",
            "competitor": "Monitor response: Set escalation triggers if they act within 3 months",
            "regional_pl": "Regional coaching: Data intelligence + incentive alignment + monthly check-ins",
            "supplier": "Relationship review: Discuss volume commitment + pricing + innovation partnership",
            "board": "Additional materials: Governance clarity + parameter confidence documentation",
            "c_suite": "Risk assessment: Monthly monitoring gates + CFO weekly reviews",
            "fpa": "Parameter validation: Data quality assessment + confidence intervals review",
        }
        return interventions.get(stakeholder_type, "Conduct stakeholder engagement meeting")

    @staticmethod
    def _generate_recommendations(results: Dict[str, StakeholderDecision], risk_level: str) -> List[str]:
        """Generate strategic recommendations"""
        recommendations = []

        if risk_level == "CRITICAL":
            recommendations.append("⚠ ESCALATE: Immediate executive review required")
            recommendations.append("→ Consider delaying execution until critical path improves")
            recommendations.append("→ Implement weekly stakeholder tracking")

        elif risk_level == "HIGH":
            recommendations.append("⚠ ELEVATED RISK: Increase monitoring frequency")
            recommendations.append("→ Execute targeted interventions for orange-zone stakeholders")
            recommendations.append("→ Monthly board updates required")

        elif risk_level == "MEDIUM":
            recommendations.append("✓ ON TRACK: Continue standard monitoring")
            recommendations.append("→ Maintain regular stakeholder engagement")
            recommendations.append("→ Quarterly board updates")

        else:  # LOW
            recommendations.append("✓ LOW RISK: Proceed as planned")
            recommendations.append("→ Standard monthly tracking")
            recommendations.append("→ Focus on sustainability + loyalty building")

        # Add specific metrics recommendations
        avg_prob = sum(r.probability for r in results.values()) / len(results) if results else 0
        if avg_prob < 0.65:
            recommendations.append("→ Focus on WHERE (parameter confidence) improvement")
        if any(r.probability < 0.50 for r in results.values()):
            recommendations.append("→ Identify and mitigate behavioral blockers (loss aversion, status quo bias)")

        return recommendations

# ============================================================================
# EXPORT FUNCTIONS
# ============================================================================

class DashboardExporter:
    """Export stakeholder results to various formats"""

    @staticmethod
    def export_to_csv(results: Dict[str, StakeholderDecision], filename: str):
        """Export results to CSV"""
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)

            # Header
            writer.writerow([
                "Stakeholder Type",
                "Decision",
                "Probability",
                "Confidence",
                "Risk Zone",
                "Red Flags Count",
                "Conditions Met",
                "Timeline to Decision",
            ])

            # Rows
            for stakeholder_type, result in sorted(results.items()):
                writer.writerow([
                    stakeholder_type,
                    result.decision_name,
                    f"{result.probability:.1%}",
                    result.confidence_level.value,
                    result.risk_zone.value,
                    len(result.red_flags),
                    len(result.conditions_met),
                    result.timeline_to_decision,
                ])

        print(f"✓ Exported to CSV: {filename}")

    @staticmethod
    def export_to_json(results: Dict[str, StakeholderDecision], filename: str):
        """Export results to JSON"""
        export_data = {
            "export_date": datetime.now().isoformat(),
            "stakeholders": {
                k: {
                    "probability": v.probability,
                    "confidence": v.confidence_level.value,
                    "risk_zone": v.risk_zone.value,
                    "key_drivers": {dk: round(dv, 2) for dk, dv in v.key_drivers.items()},
                    "red_flags": v.red_flags,
                    "conditions_met": v.conditions_met,
                    "timeline_to_decision": v.timeline_to_decision,
                    "timeline_to_execution": v.timeline_to_execution,
                }
                for k, v in results.items()
            }
        }

        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)

        print(f"✓ Exported to JSON: {filename}")

    @staticmethod
    def export_scorecard_to_json(scorecard: Dict, filename: str):
        """Export health scorecard to JSON"""
        with open(filename, 'w') as f:
            json.dump(scorecard, f, indent=2, default=str)

        print(f"✓ Exported scorecard to JSON: {filename}")

    @staticmethod
    def generate_html_report(customer_name: str,
                           results: Dict[str, StakeholderDecision],
                           scorecard: Dict,
                           filename: str):
        """Generate HTML report for browser viewing"""
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Stakeholder Behavior Report - {customer_name}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #333; }}
        .summary {{ background: #f0f0f0; padding: 15px; margin: 20px 0; border-radius: 5px; }}
        .green {{ color: green; font-weight: bold; }}
        .yellow {{ color: orange; font-weight: bold; }}
        .orange {{ color: #ff8c00; font-weight: bold; }}
        .red {{ color: red; font-weight: bold; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background-color: #4CAF50; color: white; }}
        tr:nth-child(even) {{ background-color: #f9f9f9; }}
    </style>
</head>
<body>
    <h1>Stakeholder Behavior Report: {customer_name}</h1>
    <p>Report Date: {scorecard['report_date']}</p>

    <h2>Summary</h2>
    <div class="summary">
        <p>Total Stakeholders: {scorecard['summary']['total_stakeholders']}</p>
        <p><span class="green">GREEN (≥80%): {scorecard['summary']['green']}</span></p>
        <p><span class="yellow">YELLOW (65-80%): {scorecard['summary']['yellow']}</span></p>
        <p><span class="orange">ORANGE (50-65%): {scorecard['summary']['orange']}</span></p>
        <p><span class="red">RED (<50%): {scorecard['summary']['red']}</span></p>
        <p>Critical Path Success: {scorecard['summary']['critical_path_success']:.0%}</p>
        <p>Overall Risk: {scorecard['summary']['overall_risk']}</p>
    </div>

    <h2>Stakeholder Details</h2>
    <table>
        <tr>
            <th>Stakeholder</th>
            <th>Probability</th>
            <th>Confidence</th>
            <th>Risk Zone</th>
            <th>Red Flags</th>
            <th>Trend</th>
        </tr>
"""

        for stakeholder, details in scorecard['stakeholder_details'].items():
            risk_class = details['risk_zone'].lower().split()[1] if len(details['risk_zone'].split()) > 1 else 'green'
            html += f"""
        <tr>
            <td>{stakeholder}</td>
            <td><span class="{risk_class}">{details['probability']:.0%}</span></td>
            <td>{details['confidence']}</td>
            <td>{details['risk_zone']}</td>
            <td>{len(details['red_flags'])}</td>
            <td>{details.get('trend', 'N/A')}</td>
        </tr>
"""

        html += """
    </table>

    <h2>Action Items</h2>
    <ol>
"""
        for item in scorecard['action_items']:
            html += f"<li><strong>{item['priority']}</strong>: {item['stakeholder']} - {item['issue']}<br/>"
            html += f"Action: {item['action']} (Timeline: {item['timeline']})</li>"

        html += """
    </ol>

    <h2>Recommendations</h2>
    <ul>
"""
        for rec in scorecard['recommendations']:
            html += f"<li>{rec}</li>"

        html += """
    </ul>
</body>
</html>
"""

        with open(filename, 'w') as f:
            f.write(html)

        print(f"✓ Generated HTML report: {filename}")

# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("BEHAVIOR MATRIX DASHBOARD")
    print("=" * 70)
    print("See simulate_stakeholder_cli.py for integration examples")
