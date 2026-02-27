#!/usr/bin/env python3
"""
Board Presentation Generator - Generate 10-slide strategic presentations from ISO-1.0 results.

Takes ISO-1.0 orchestrator output and generates board-ready presentations.

Output formats:
- Markdown (.md) - Text-based slides
- LaTeX (.tex) - For PDF compilation
- JSON (.json) - Structured data for PPTX generation

Version: 1.0.0
Author: EBF Strategic Model Library
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from datetime import datetime
import json
import os
import re


@dataclass
class PresentationConfig:
    """Configuration for presentation generation."""
    company_name: str
    output_dir: str = "outputs/presentations"
    style: str = "professional"  # professional, minimal, detailed
    language: str = "en"  # en, de
    include_appendix: bool = False


class BoardPresentationGenerator:
    """Generate board presentations from ISO-1.0 results."""

    def __init__(self, results: Dict, config: PresentationConfig):
        """
        Initialize generator with ISO-1.0 results.

        Args:
            results: Output from IntegratedStrategyOrchestrator.run()
            config: Presentation configuration
        """
        self.results = results
        self.config = config
        self.summary = results.get("integrated_summary", {})
        self.timestamp = datetime.now().strftime("%Y-%m-%d")
        self.slides = []

    def _safe_get(self, path: str, default: Any = None) -> Any:
        """Safely get nested value from results."""
        model_pattern = r'^([A-Z]+-\d+\.\d+)\.(.*)$'
        match = re.match(model_pattern, path)
        current = self.results

        if match:
            model_id = match.group(1)
            rest_path = match.group(2)
            if model_id in current:
                current = current[model_id]
                parts = rest_path.split(".")
            else:
                return default
        else:
            parts = path.split(".")

        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return default
        return current if current is not None else default

    def _fmt_eur(self, value: float, unit: str = "M") -> str:
        """Format EUR value."""
        if value >= 1e9:
            return f"€{value/1e9:.1f}B"
        elif value >= 1e6:
            return f"€{value/1e6:.0f}M"
        else:
            return f"€{value:,.0f}"

    def _fmt_pct(self, value: float) -> str:
        """Format percentage."""
        return f"{value:.1f}%"

    def generate_slide_1_executive_summary(self) -> Dict:
        """SLIDE 1: Executive Summary."""
        revenue_2024 = self._safe_get("RPM-1.0.summary.base_revenue", 0)
        revenue_2035 = self._safe_get("RPM-1.0.summary.final_revenue", revenue_2024)
        cagr = self._safe_get("RPM-1.0.summary.cagr", 0)
        ev = self._safe_get("VAM-1.0.summary.enterprise_value.dcf", 0)
        headcount_2024 = self._safe_get("HCM-1.0.summary.total_headcount", 0)
        headcount_2035 = self._safe_get("OSM-1.0.summary.final_headcount", headcount_2024)

        return {
            "slide_number": 1,
            "title": f"Strategic Outlook 2035 | {self.config.company_name}",
            "subtitle": f"Board Presentation | {self.timestamp}",
            "content": {
                "key_metrics": [
                    {"label": "Revenue 2024", "value": self._fmt_eur(revenue_2024)},
                    {"label": "Revenue 2035", "value": self._fmt_eur(revenue_2035)},
                    {"label": "CAGR", "value": self._fmt_pct(cagr * 100)},
                    {"label": "Enterprise Value", "value": self._fmt_eur(ev)},
                ],
                "growth_summary": f"+{self._fmt_pct((revenue_2035/revenue_2024-1)*100 if revenue_2024 > 0 else 0)} growth over 11 years",
                "headcount": f"{headcount_2024:,.0f} → {headcount_2035:,.0f} employees",
            },
            "visual": "4-box KPI dashboard",
        }

    def generate_slide_2_scenarios(self) -> Dict:
        """SLIDE 2: 3 Strategic Scenarios."""
        base_revenue = self._safe_get("RPM-1.0.summary.final_revenue", 0)
        base_cagr = self._safe_get("RPM-1.0.summary.cagr", 0)

        # Calculate conservative and optimistic (±1.5pp CAGR adjustment)
        revenue_2024 = self._safe_get("RPM-1.0.summary.base_revenue", 0)
        years = 11

        conservative_cagr = max(0, base_cagr - 0.015)
        optimistic_cagr = base_cagr + 0.015

        conservative_2035 = revenue_2024 * (1 + conservative_cagr) ** years
        optimistic_2035 = revenue_2024 * (1 + optimistic_cagr) ** years

        return {
            "slide_number": 2,
            "title": "Revenue Scenarios 2024-2035",
            "content": {
                "scenarios": [
                    {
                        "name": "Conservative",
                        "revenue_2024": self._fmt_eur(revenue_2024),
                        "revenue_2035": self._fmt_eur(conservative_2035),
                        "cagr": self._fmt_pct(conservative_cagr * 100),
                        "status": "Achievable",
                    },
                    {
                        "name": "Base Case",
                        "revenue_2024": self._fmt_eur(revenue_2024),
                        "revenue_2035": self._fmt_eur(base_revenue),
                        "cagr": self._fmt_pct(base_cagr * 100),
                        "status": "RECOMMENDED",
                        "highlight": True,
                    },
                    {
                        "name": "Optimistic",
                        "revenue_2024": self._fmt_eur(revenue_2024),
                        "revenue_2035": self._fmt_eur(optimistic_2035),
                        "cagr": self._fmt_pct(optimistic_cagr * 100),
                        "status": "Stretch Target",
                    },
                ],
            },
            "visual": "3-line trajectory chart",
        }

    def generate_slide_3_monte_carlo(self) -> Dict:
        """SLIDE 3: Monte Carlo Confidence Metrics."""
        mc_mean = self._safe_get("MCSM-1.0.summary.mean_value", 0)
        mc_p10 = self._safe_get("MCSM-1.0.summary.p10", mc_mean * 0.80)
        mc_p50 = self._safe_get("MCSM-1.0.summary.p50", mc_mean)
        mc_p90 = self._safe_get("MCSM-1.0.summary.p90", mc_mean * 1.20)
        num_sims = self._safe_get("MCSM-1.0.summary.num_simulations", 1000)

        return {
            "slide_number": 3,
            "title": f"Risk Quantification ({num_sims:,} Simulations)",
            "content": {
                "percentiles": [
                    {"percentile": "10%", "value": self._fmt_eur(mc_p10), "interpretation": "Downside risk"},
                    {"percentile": "50%", "value": self._fmt_eur(mc_p50), "interpretation": "Median outcome"},
                    {"percentile": "90%", "value": self._fmt_eur(mc_p90), "interpretation": "Upside potential"},
                ],
                "confidence_statement": f"90% confidence interval: {self._fmt_eur(mc_p10)} - {self._fmt_eur(mc_p90)}",
                "base_case_probability": "50% probability of achieving base case",
            },
            "visual": "Histogram with percentile markers",
        }

    def generate_slide_4_regional_growth(self) -> Dict:
        """SLIDE 4: Regional Growth Drivers."""
        # Use summary data or defaults
        revenue_2024 = self._safe_get("RPM-1.0.summary.base_revenue", 0)

        regions = [
            {"name": "Europe", "share": 0.45, "cagr": 0.03},
            {"name": "APAC", "share": 0.25, "cagr": 0.08},
            {"name": "Americas", "share": 0.20, "cagr": 0.05},
            {"name": "MEA", "share": 0.10, "cagr": 0.06},
        ]

        regional_data = []
        for r in regions:
            rev_2024 = revenue_2024 * r["share"]
            rev_2035 = rev_2024 * (1 + r["cagr"]) ** 11
            regional_data.append({
                "region": r["name"],
                "revenue_2024": self._fmt_eur(rev_2024),
                "revenue_2035": self._fmt_eur(rev_2035),
                "cagr": self._fmt_pct(r["cagr"] * 100),
                "share": self._fmt_pct(r["share"] * 100),
            })

        return {
            "slide_number": 4,
            "title": "Regional Revenue Breakdown & Growth Rates",
            "content": {"regions": regional_data},
            "visual": "Stacked bar chart by region",
        }

    def generate_slide_5_customer_economics(self) -> Dict:
        """SLIDE 5: Customer Economics (CLV/CAC)."""
        clv = self._safe_get("CLV-1.0.summary.clv", 0)
        cac = self._safe_get("CAC-1.0.summary.blended_cac", 0)
        ltv_cac = clv / cac if cac > 0 else 0
        retention = self._safe_get("CLV-1.0.summary.retention_rate", 0.85)

        health = "EXCELLENT" if ltv_cac >= 3 else "GOOD" if ltv_cac >= 2 else "NEEDS IMPROVEMENT"

        return {
            "slide_number": 5,
            "title": "Customer Economics",
            "content": {
                "metrics": [
                    {"label": "Customer Lifetime Value (CLV)", "value": f"€{clv:,.0f}"},
                    {"label": "Customer Acquisition Cost (CAC)", "value": f"€{cac:,.0f}"},
                    {"label": "LTV:CAC Ratio", "value": f"{ltv_cac:.1f}x"},
                    {"label": "Customer Retention Rate", "value": self._fmt_pct(retention * 100)},
                ],
                "health_status": health,
                "benchmark": "Target LTV:CAC > 3.0x",
            },
            "visual": "Funnel diagram with CLV breakdown",
        }

    def generate_slide_6_organizational(self) -> Dict:
        """SLIDE 6: Organizational Growth & Headcount."""
        hc_2024 = self._safe_get("HCM-1.0.summary.total_headcount", 0)
        hc_2035 = self._safe_get("OSM-1.0.summary.final_headcount", hc_2024)
        labor_cost = self._safe_get("HCM-1.0.summary.total_labor_cost", 0)
        rev_per_emp = self._safe_get("HCM-1.0.summary.revenue_per_employee", 0)

        return {
            "slide_number": 6,
            "title": "Organizational Growth & Human Capital",
            "content": {
                "headcount": {
                    "2024": f"{hc_2024:,.0f}",
                    "2035": f"{hc_2035:,.0f}",
                    "growth": f"+{hc_2035 - hc_2024:,.0f} ({(hc_2035/hc_2024-1)*100:.0f}%)" if hc_2024 > 0 else "N/A",
                },
                "efficiency": {
                    "revenue_per_employee": self._fmt_eur(rev_per_emp),
                    "total_labor_cost": self._fmt_eur(labor_cost),
                },
            },
            "visual": "Headcount waterfall chart",
        }

    def generate_slide_7_capex(self) -> Dict:
        """SLIDE 7: Capital Investment Roadmap."""
        total_capex = self._safe_get("CAM-1.0.summary.total_capex", 0)
        annual_avg = total_capex / 11 if total_capex > 0 else 0

        return {
            "slide_number": 7,
            "title": "Capital Investment Roadmap (2025-2035)",
            "content": {
                "total_capex": self._fmt_eur(total_capex),
                "annual_average": self._fmt_eur(annual_avg),
                "categories": [
                    {"name": "Production/Equipment", "share": "40%"},
                    {"name": "Digital/IT", "share": "20%"},
                    {"name": "Expansion", "share": "20%"},
                    {"name": "Maintenance", "share": "15%"},
                    {"name": "Sustainability", "share": "5%"},
                ],
            },
            "visual": "Capex waterfall by year and category",
        }

    def generate_slide_8_valuation(self) -> Dict:
        """SLIDE 8: Valuation & Value Creation."""
        ev_dcf = self._safe_get("VAM-1.0.summary.enterprise_value.dcf", 0)
        eq_dcf = self._safe_get("VAM-1.0.summary.equity_value.dcf", 0)
        wacc = self._safe_get("CMM-1.0.wacc_analysis.wacc", 0.10)
        roic = self._safe_get("VCM-1.0.summary.roic_pct", 0)
        eva = self._safe_get("VCM-1.0.summary.eva", 0)
        spread = self._safe_get("VCM-1.0.summary.spread_pct", 0)

        value_created = spread > 0

        return {
            "slide_number": 8,
            "title": "Valuation & Value Creation",
            "content": {
                "valuation": {
                    "enterprise_value": self._fmt_eur(ev_dcf),
                    "equity_value": self._fmt_eur(eq_dcf),
                    "methodology": "DCF (10-year projection + terminal value)",
                },
                "value_creation": {
                    "roic": self._fmt_pct(roic),
                    "wacc": self._fmt_pct(wacc * 100),
                    "spread": self._fmt_pct(spread),
                    "eva": self._fmt_eur(eva),
                    "status": "VALUE CREATED" if value_created else "VALUE DESTROYED",
                },
            },
            "visual": "DCF bridge chart + ROIC vs WACC comparison",
        }

    def generate_slide_9_esg(self) -> Dict:
        """SLIDE 9: ESG & Sustainability."""
        esg_score = self._safe_get("ESG-1.0.summary.overall_score", 0)
        rating = self._safe_get("ESG-1.0.summary.rating", "N/A")
        env = self._safe_get("ESG-1.0.environmental.score", esg_score * 0.33)
        soc = self._safe_get("ESG-1.0.social.score", esg_score * 0.33)
        gov = self._safe_get("ESG-1.0.governance.score", esg_score * 0.34)

        return {
            "slide_number": 9,
            "title": "ESG & Sustainability Positioning",
            "content": {
                "overall": {
                    "score": f"{esg_score:.0f}/100",
                    "rating": rating,
                },
                "breakdown": [
                    {"pillar": "Environmental", "score": f"{env:.0f}"},
                    {"pillar": "Social", "score": f"{soc:.0f}"},
                    {"pillar": "Governance", "score": f"{gov:.0f}"},
                ],
                "key_initiatives": [
                    "Carbon neutrality roadmap",
                    "Supply chain sustainability",
                    "Diversity & inclusion targets",
                ],
            },
            "visual": "ESG radar chart",
        }

    def generate_slide_10_recommendation(self) -> Dict:
        """SLIDE 10: Strategic Recommendation & Next Steps."""
        revenue_2035 = self._safe_get("RPM-1.0.summary.final_revenue", 0)
        cagr = self._safe_get("RPM-1.0.summary.cagr", 0)
        total_capex = self._safe_get("CAM-1.0.summary.total_capex", 0)

        return {
            "slide_number": 10,
            "title": "Strategic Recommendation & Board Decision",
            "content": {
                "recommendation": {
                    "strategy": "Base Case Strategy",
                    "target": self._fmt_eur(revenue_2035),
                    "cagr": self._fmt_pct(cagr * 100),
                    "capex_required": self._fmt_eur(total_capex),
                },
                "key_benefits": [
                    "Balanced growth across regions",
                    "Achievable with disciplined execution",
                    "Positions company for market leadership",
                ],
                "implementation_phases": [
                    {"phase": "Phase 1 (2025-26)", "focus": "Foundation & acceleration"},
                    {"phase": "Phase 2 (2027-29)", "focus": "Expansion & scaling"},
                    {"phase": "Phase 3 (2030-35)", "focus": "Optimization & maturation"},
                ],
                "board_actions": [
                    "Approve base case strategy",
                    "Authorize Phase 1 capex",
                    "Establish quarterly review process",
                ],
            },
            "visual": "Implementation timeline",
        }

    def generate_all_slides(self) -> List[Dict]:
        """Generate all 10 slides."""
        self.slides = [
            self.generate_slide_1_executive_summary(),
            self.generate_slide_2_scenarios(),
            self.generate_slide_3_monte_carlo(),
            self.generate_slide_4_regional_growth(),
            self.generate_slide_5_customer_economics(),
            self.generate_slide_6_organizational(),
            self.generate_slide_7_capex(),
            self.generate_slide_8_valuation(),
            self.generate_slide_9_esg(),
            self.generate_slide_10_recommendation(),
        ]
        return self.slides

    def to_markdown(self) -> str:
        """Export presentation to Markdown format."""
        if not self.slides:
            self.generate_all_slides()

        md = f"""# {self.config.company_name} - Strategic Board Presentation
**Generated:** {self.timestamp} | **Models:** ISO-1.0 (31 models)

---

"""
        for slide in self.slides:
            md += f"## Slide {slide['slide_number']}: {slide['title']}\n\n"

            if "subtitle" in slide:
                md += f"*{slide['subtitle']}*\n\n"

            content = slide.get("content", {})

            # Handle different content types
            if "key_metrics" in content:
                md += "| Metric | Value |\n|--------|-------|\n"
                for m in content["key_metrics"]:
                    md += f"| {m['label']} | **{m['value']}** |\n"
                md += "\n"
                if "growth_summary" in content:
                    md += f"**Growth:** {content['growth_summary']}\n\n"

            if "scenarios" in content:
                md += "| Scenario | 2024 | 2035 | CAGR | Status |\n"
                md += "|----------|------|------|------|--------|\n"
                for s in content["scenarios"]:
                    highlight = "**" if s.get("highlight") else ""
                    md += f"| {highlight}{s['name']}{highlight} | {s['revenue_2024']} | {s['revenue_2035']} | {s['cagr']} | {s['status']} |\n"
                md += "\n"

            if "percentiles" in content:
                md += "| Percentile | Value | Interpretation |\n"
                md += "|------------|-------|----------------|\n"
                for p in content["percentiles"]:
                    md += f"| {p['percentile']} | {p['value']} | {p['interpretation']} |\n"
                md += "\n"
                if "confidence_statement" in content:
                    md += f"**{content['confidence_statement']}**\n\n"

            if "regions" in content:
                md += "| Region | 2024 | 2035 | CAGR | Share |\n"
                md += "|--------|------|------|------|-------|\n"
                for r in content["regions"]:
                    md += f"| {r['region']} | {r['revenue_2024']} | {r['revenue_2035']} | {r['cagr']} | {r['share']} |\n"
                md += "\n"

            if "metrics" in content:
                md += "| Metric | Value |\n|--------|-------|\n"
                for m in content["metrics"]:
                    md += f"| {m['label']} | **{m['value']}** |\n"
                if "health_status" in content:
                    md += f"\n**Status:** {content['health_status']}\n"
                md += "\n"

            if "headcount" in content and isinstance(content["headcount"], dict):
                hc = content["headcount"]
                if "2024" in hc and "2035" in hc:
                    md += f"**Headcount:** {hc['2024']} → {hc['2035']} ({hc.get('growth', 'N/A')})\n\n"

            if "valuation" in content:
                v = content["valuation"]
                md += f"**Enterprise Value:** {v['enterprise_value']} | **Equity Value:** {v['equity_value']}\n\n"
                if "value_creation" in content:
                    vc = content["value_creation"]
                    md += f"**ROIC:** {vc['roic']} | **WACC:** {vc['wacc']} | **Spread:** {vc['spread']}\n"
                    md += f"**EVA:** {vc['eva']} → **{vc['status']}**\n\n"

            if "overall" in content:
                o = content["overall"]
                md += f"**ESG Score:** {o['score']} | **Rating:** {o['rating']}\n\n"

            if "recommendation" in content:
                rec = content["recommendation"]
                md += f"### RECOMMENDATION: {rec['strategy']}\n"
                md += f"- **Target:** {rec['target']} by 2035\n"
                md += f"- **CAGR:** {rec['cagr']}\n"
                md += f"- **Capex Required:** {rec['capex_required']}\n\n"

            if "board_actions" in content:
                md += "### Board Actions Requested:\n"
                for action in content["board_actions"]:
                    md += f"- [ ] {action}\n"
                md += "\n"

            if "visual" in slide:
                md += f"*[Visual: {slide['visual']}]*\n\n"

            md += "---\n\n"

        md += f"\n*Generated by ISO-1.0 Board Presentation Generator v1.0.0*\n"
        return md

    def to_json(self) -> Dict:
        """Export presentation to JSON format."""
        if not self.slides:
            self.generate_all_slides()

        return {
            "metadata": {
                "company": self.config.company_name,
                "generated": self.timestamp,
                "generator": "ISO-1.0 Board Presentation Generator v1.0.0",
                "num_slides": len(self.slides),
            },
            "slides": self.slides,
        }

    def save(self, formats: List[str] = None) -> Dict[str, str]:
        """Save presentation in specified formats."""
        if formats is None:
            formats = ["markdown", "json"]

        os.makedirs(self.config.output_dir, exist_ok=True)
        company_slug = self.config.company_name.lower().replace(" ", "_")
        timestamp = datetime.now().strftime("%Y%m%d")

        saved_files = {}

        if "markdown" in formats:
            md_path = os.path.join(
                self.config.output_dir,
                f"{company_slug}_board_presentation_{timestamp}.md"
            )
            with open(md_path, "w") as f:
                f.write(self.to_markdown())
            saved_files["markdown"] = md_path

        if "json" in formats:
            json_path = os.path.join(
                self.config.output_dir,
                f"{company_slug}_board_presentation_{timestamp}.json"
            )
            with open(json_path, "w") as f:
                json.dump(self.to_json(), f, indent=2)
            saved_files["json"] = json_path

        return saved_files


def generate_board_presentation(
    results: Dict,
    company_name: str,
    output_dir: str = "outputs/presentations",
    formats: List[str] = None
) -> Dict[str, str]:
    """
    Convenience function to generate board presentation from ISO-1.0 results.

    Args:
        results: Output from IntegratedStrategyOrchestrator.run()
        company_name: Name of the company
        output_dir: Directory for output files
        formats: List of formats ["markdown", "json"]

    Returns:
        Dict with paths to generated files
    """
    config = PresentationConfig(
        company_name=company_name,
        output_dir=output_dir
    )
    generator = BoardPresentationGenerator(results, config)
    return generator.save(formats)


if __name__ == "__main__":
    # Test with ISO-1.0 results
    from integrated_strategy_orchestrator import run_integrated_strategy

    print("Running ISO-1.0 to generate test data...")
    results = run_integrated_strategy("TestCompany", 1_500_000_000, full_run=True, verbose=False)

    print("\nGenerating board presentation...")
    files = generate_board_presentation(results, "TestCompany")

    print(f"\nGenerated files:")
    for fmt, path in files.items():
        print(f"  {fmt}: {path}")

    # Print markdown preview
    config = PresentationConfig(company_name="TestCompany")
    generator = BoardPresentationGenerator(results, config)
    print("\n" + "=" * 70)
    print("MARKDOWN PREVIEW (first 2000 chars):")
    print("=" * 70)
    print(generator.to_markdown()[:2000])
