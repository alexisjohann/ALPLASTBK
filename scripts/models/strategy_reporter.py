#!/usr/bin/env python3
"""
Strategy Reporter - Generate reports and visualizations from ISO-1.0 results.

Produces:
- Executive Summary (text)
- Model Results Table (CSV)
- Key Metrics Dashboard (markdown/HTML)
- Optional: Charts (if matplotlib available)

Version: 1.0.0
Author: EBF Strategic Model Library
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from datetime import datetime
import json
import csv
import os


@dataclass
class ReportConfig:
    """Configuration for report generation."""
    company_name: str
    output_dir: str = "outputs/reports"
    include_charts: bool = True
    format: str = "markdown"  # markdown, html, text
    language: str = "en"  # en, de


class StrategyReporter:
    """Generate reports from ISO-1.0 orchestrator results."""

    def __init__(self, results: Dict, config: ReportConfig):
        """
        Initialize reporter with ISO-1.0 results.

        Args:
            results: Output from IntegratedStrategyOrchestrator.run()
            config: Report configuration
        """
        self.results = results
        self.config = config
        self.summary = results.get("summary", {})
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    def generate_executive_summary(self) -> str:
        """Generate text executive summary."""
        company = self.config.company_name

        # Extract key metrics
        clv = self._safe_get("CLV-1.0.summary.clv", 0)
        cac = self._safe_get("CAC-1.0.summary.cac", 0)
        clv_cac_ratio = clv / cac if cac > 0 else 0

        revenue_base = self._safe_get("RPM-1.0.summary.base_revenue", 0)
        revenue_final = self._safe_get("RPM-1.0.summary.final_revenue", 0)
        revenue_cagr = self._safe_get("RPM-1.0.summary.cagr", 0)

        headcount_2024 = self._safe_get("HCM-1.0.summary.total_headcount", 1)  # Avoid div by zero
        headcount_2035 = self._safe_get("OSM-1.0.summary.final_headcount", headcount_2024)

        enterprise_value = self._safe_get("VAM-1.0.summary.enterprise_value", 0)
        esg_score = self._safe_get("ESG-1.0.summary.total_score", 0)

        mc_mean = self._safe_get("MCSM-1.0.summary.mean", revenue_final)
        mc_ci_low = self._safe_get("MCSM-1.0.summary.ci_95_low", mc_mean * 0.85)
        mc_ci_high = self._safe_get("MCSM-1.0.summary.ci_95_high", mc_mean * 1.15)

        summary = f"""
================================================================================
EXECUTIVE SUMMARY: {company}
Generated: {self.timestamp}
================================================================================

1. STRATEGIC OVERVIEW
---------------------
{company} is projected to grow from EUR {revenue_base/1e6:.0f}M to
EUR {revenue_final/1e6:.0f}M by 2035, representing a {revenue_cagr*100:.1f}% CAGR.

2. KEY FINANCIAL METRICS
------------------------
  Revenue 2024:        EUR {revenue_base/1e6:,.0f}M
  Revenue 2035:        EUR {revenue_final/1e6:,.0f}M
  Revenue CAGR:        {revenue_cagr*100:.1f}%
  Enterprise Value:    EUR {enterprise_value/1e9:.2f}B

3. CUSTOMER ECONOMICS
---------------------
  Customer Lifetime Value (CLV):  EUR {clv:,.0f}
  Customer Acquisition Cost (CAC): EUR {cac:,.0f}
  CLV/CAC Ratio:                   {clv_cac_ratio:.1f}x

  {"HEALTHY" if clv_cac_ratio >= 3 else "NEEDS IMPROVEMENT"}:
  {"Excellent customer economics" if clv_cac_ratio >= 3 else "Target CLV/CAC > 3.0x"}

4. ORGANIZATIONAL GROWTH
------------------------
  Headcount 2024:      {headcount_2024:,.0f}
  Headcount 2035:      {headcount_2035:,.0f}
  Growth:              +{headcount_2035 - headcount_2024:,.0f} ({(headcount_2035/headcount_2024-1)*100:.0f}%)

5. SUSTAINABILITY (ESG)
-----------------------
  Overall ESG Score:   {esg_score:.0f}/100
  {"STRONG" if esg_score >= 70 else "MODERATE" if esg_score >= 50 else "NEEDS ATTENTION"}

6. MONTE CARLO CONFIDENCE
-------------------------
  Base Case (Mean):    EUR {mc_mean/1e6:,.0f}M
  95% Confidence:      EUR {mc_ci_low/1e6:,.0f}M - EUR {mc_ci_high/1e6:,.0f}M
  Downside Risk:       {self._safe_pct(mc_mean - mc_ci_low, mc_mean):.1f}%
  Upside Potential:    {self._safe_pct(mc_ci_high - mc_mean, mc_mean):.1f}%

================================================================================
Models Executed: {self.summary.get('models_run', 31)}
Execution Time: {self.summary.get('execution_time', 'N/A')}
================================================================================
"""
        return summary.strip()

    def generate_metrics_table(self) -> List[Dict]:
        """Generate structured metrics for CSV/table output."""
        metrics = []

        # Layer 1: Functional Strategy
        metrics.append({"Layer": "Functional", "Model": "CLV-1.0", "Metric": "Customer Lifetime Value", "Value": self._safe_get("CLV-1.0.summary.clv", 0), "Unit": "EUR"})
        metrics.append({"Layer": "Functional", "Model": "CAC-1.0", "Metric": "Customer Acquisition Cost", "Value": self._safe_get("CAC-1.0.summary.cac", 0), "Unit": "EUR"})
        metrics.append({"Layer": "Functional", "Model": "HCM-1.0", "Metric": "Total Headcount", "Value": self._safe_get("HCM-1.0.summary.total_headcount", 0), "Unit": "FTE"})
        metrics.append({"Layer": "Functional", "Model": "SCO-1.0", "Metric": "Supply Chain Efficiency", "Value": self._safe_get("SCO-1.0.summary.efficiency", 0), "Unit": "%"})
        metrics.append({"Layer": "Functional", "Model": "RDM-1.0", "Metric": "R&D Investment", "Value": self._safe_get("RDM-1.0.summary.total_investment", 0), "Unit": "EUR"})
        metrics.append({"Layer": "Functional", "Model": "ESG-1.0", "Metric": "ESG Score", "Value": self._safe_get("ESG-1.0.summary.total_score", 0), "Unit": "Score"})

        # Layer 2: Core Financial
        metrics.append({"Layer": "Financial", "Model": "RPM-1.0", "Metric": "Revenue 2035", "Value": self._safe_get("RPM-1.0.summary.final_revenue", 0), "Unit": "EUR"})
        metrics.append({"Layer": "Financial", "Model": "OSM-1.0", "Metric": "Headcount 2035", "Value": self._safe_get("OSM-1.0.summary.final_headcount", 0), "Unit": "FTE"})
        metrics.append({"Layer": "Financial", "Model": "CAM-1.0", "Metric": "Total Capex", "Value": self._safe_get("CAM-1.0.summary.total_capex", 0), "Unit": "EUR"})
        metrics.append({"Layer": "Financial", "Model": "PLM-1.0", "Metric": "Net Profit 2035", "Value": self._safe_get("PLM-1.0.summary.final_net_profit", 0), "Unit": "EUR"})
        metrics.append({"Layer": "Financial", "Model": "CFM-1.0", "Metric": "Free Cash Flow 2035", "Value": self._safe_get("CFM-1.0.summary.final_fcf", 0), "Unit": "EUR"})

        # Layer 3: Theoretical
        metrics.append({"Layer": "Theoretical", "Model": "VAM-1.0", "Metric": "Enterprise Value", "Value": self._safe_get("VAM-1.0.summary.enterprise_value", 0), "Unit": "EUR"})
        metrics.append({"Layer": "Theoretical", "Model": "CMM-1.0", "Metric": "WACC", "Value": self._safe_get("CMM-1.0.summary.wacc", 0), "Unit": "%"})

        # Layer 5: Simulation
        metrics.append({"Layer": "Simulation", "Model": "MCSM-1.0", "Metric": "Monte Carlo Mean", "Value": self._safe_get("MCSM-1.0.summary.mean", 0), "Unit": "EUR"})
        metrics.append({"Layer": "Simulation", "Model": "MCSM-1.0", "Metric": "95% CI Low", "Value": self._safe_get("MCSM-1.0.summary.ci_95_low", 0), "Unit": "EUR"})
        metrics.append({"Layer": "Simulation", "Model": "MCSM-1.0", "Metric": "95% CI High", "Value": self._safe_get("MCSM-1.0.summary.ci_95_high", 0), "Unit": "EUR"})

        return metrics

    def generate_markdown_dashboard(self) -> str:
        """Generate markdown dashboard."""
        company = self.config.company_name

        # Key metrics
        revenue_base = self._safe_get("RPM-1.0.summary.base_revenue", 1)  # Avoid div by zero
        revenue_final = self._safe_get("RPM-1.0.summary.final_revenue", revenue_base)
        revenue_cagr = self._safe_get("RPM-1.0.summary.cagr", 0)
        enterprise_value = self._safe_get("VAM-1.0.summary.enterprise_value", 0)
        clv = self._safe_get("CLV-1.0.summary.clv", 0)
        cac = self._safe_get("CAC-1.0.summary.cac", 0)
        clv_cac = clv / cac if cac > 0 else 0
        esg = self._safe_get("ESG-1.0.summary.total_score", 0)

        dashboard = f"""# {company} - Strategic Dashboard

**Generated:** {self.timestamp}
**Models Executed:** {self.summary.get('models_run', 29)}

---

## Key Performance Indicators

| Metric | 2024 | 2035 | Change |
|--------|------|------|--------|
| Revenue | EUR {revenue_base/1e6:,.0f}M | EUR {revenue_final/1e6:,.0f}M | +{(revenue_final/revenue_base-1)*100:.0f}% |
| Enterprise Value | - | EUR {enterprise_value/1e9:.2f}B | - |
| ESG Score | - | {esg:.0f}/100 | - |

---

## Customer Economics

| Metric | Value | Status |
|--------|-------|--------|
| CLV | EUR {clv:,.0f} | - |
| CAC | EUR {cac:,.0f} | - |
| CLV/CAC Ratio | {clv_cac:.1f}x | {"Good" if clv_cac >= 3 else "Needs Work"} |

---

## Monte Carlo Simulation

```
                    95% Confidence Interval
                    |<---------------->|
    [P5]           [Mean]            [P95]
     |---------------|-----------------|
   {self._safe_get("MCSM-1.0.summary.ci_95_low", 0)/1e6:.0f}M          {self._safe_get("MCSM-1.0.summary.mean", 0)/1e6:.0f}M           {self._safe_get("MCSM-1.0.summary.ci_95_high", 0)/1e6:.0f}M
```

---

## Model Execution Summary

| Layer | Models | Status |
|-------|--------|--------|
| Functional Strategy | CLV, CAC, HCM, SCO, RDM, ESG | Complete |
| Core Financial | RPM, OSM, CAM, CSM, PLM, WCM, CFM, DFM, BSM, BEM | Complete |
| Theoretical | FEM, BFM, CMM, VAM | Complete |
| Strategic Analysis | MSM, MAM, PFM, STM, PRM | Complete |
| Simulation | MCSM, SAM, SCM, ICM | Complete |

---

*Report generated by EBF Strategy Reporter v1.0.0*
"""
        return dashboard

    def save_reports(self) -> Dict[str, str]:
        """Save all reports to output directory."""
        os.makedirs(self.config.output_dir, exist_ok=True)
        company_slug = self.config.company_name.lower().replace(" ", "_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")

        saved_files = {}

        # Executive Summary (text)
        summary_path = os.path.join(
            self.config.output_dir,
            f"{company_slug}_executive_summary_{timestamp}.txt"
        )
        with open(summary_path, "w") as f:
            f.write(self.generate_executive_summary())
        saved_files["executive_summary"] = summary_path

        # Metrics Table (CSV)
        csv_path = os.path.join(
            self.config.output_dir,
            f"{company_slug}_metrics_{timestamp}.csv"
        )
        metrics = self.generate_metrics_table()
        with open(csv_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["Layer", "Model", "Metric", "Value", "Unit"])
            writer.writeheader()
            writer.writerows(metrics)
        saved_files["metrics_csv"] = csv_path

        # Dashboard (Markdown)
        md_path = os.path.join(
            self.config.output_dir,
            f"{company_slug}_dashboard_{timestamp}.md"
        )
        with open(md_path, "w") as f:
            f.write(self.generate_markdown_dashboard())
        saved_files["dashboard_md"] = md_path

        # Raw results (JSON)
        json_path = os.path.join(
            self.config.output_dir,
            f"{company_slug}_raw_results_{timestamp}.json"
        )
        with open(json_path, "w") as f:
            json.dump(self.results, f, indent=2, default=str)
        saved_files["raw_json"] = json_path

        return saved_files

    def _safe_pct(self, numerator: float, denominator: float) -> float:
        """Calculate percentage safely, avoiding division by zero."""
        if denominator == 0:
            return 0.0
        return (numerator / denominator) * 100

    def _safe_get(self, path: str, default: Any = None) -> Any:
        """Safely get nested value from results using dot notation.

        Handles model IDs with dots like 'CLV-1.0.summary.clv'
        """
        # Try to match model ID pattern (e.g., "CLV-1.0")
        # Model IDs have format: XXX-N.N where N.N is version
        import re

        current = self.results

        # First, try to extract model ID (pattern like "XXX-1.0")
        model_pattern = r'^([A-Z]+-\d+\.\d+)\.(.*)$'
        match = re.match(model_pattern, path)

        if match:
            model_id = match.group(1)  # e.g., "CLV-1.0"
            rest_path = match.group(2)  # e.g., "summary.clv"

            if model_id in current:
                current = current[model_id]
                parts = rest_path.split(".")
            else:
                return default
        else:
            parts = path.split(".")

        for part in parts:
            if isinstance(current, dict):
                if part in current:
                    current = current[part]
                else:
                    return default
            else:
                return default

        return current if current is not None else default


def generate_strategy_report(
    results: Dict,
    company_name: str,
    output_dir: str = "outputs/reports",
    format: str = "all"
) -> Dict[str, str]:
    """
    Convenience function to generate strategy reports.

    Args:
        results: Output from IntegratedStrategyOrchestrator.run()
        company_name: Name of the company
        output_dir: Directory for output files
        format: "all", "summary", "csv", "markdown", "json"

    Returns:
        Dict with paths to generated files
    """
    config = ReportConfig(
        company_name=company_name,
        output_dir=output_dir
    )
    reporter = StrategyReporter(results, config)

    if format == "all":
        return reporter.save_reports()
    elif format == "summary":
        print(reporter.generate_executive_summary())
        return {"printed": "executive_summary"}
    elif format == "markdown":
        print(reporter.generate_markdown_dashboard())
        return {"printed": "dashboard"}
    else:
        return reporter.save_reports()


if __name__ == "__main__":
    # Test with mock data
    mock_results = {
        "CLV-1.0": {"summary": {"clv": 15000}},
        "CAC-1.0": {"summary": {"cac": 3000}},
        "HCM-1.0": {"summary": {"total_headcount": 5000}},
        "RPM-1.0": {"summary": {"base_revenue": 1_500_000_000, "final_revenue": 2_850_000_000, "cagr": 0.06}},
        "OSM-1.0": {"summary": {"final_headcount": 8000}},
        "ESG-1.0": {"summary": {"total_score": 72}},
        "VAM-1.0": {"summary": {"enterprise_value": 5_000_000_000}},
        "MCSM-1.0": {"summary": {"mean": 2_850_000_000, "ci_95_low": 2_400_000_000, "ci_95_high": 3_300_000_000}},
        "summary": {"models_run": 29, "execution_time": "5.2s"}
    }

    files = generate_strategy_report(mock_results, "TestCompany", format="all")
    print(f"\nGenerated files:")
    for name, path in files.items():
        print(f"  {name}: {path}")
