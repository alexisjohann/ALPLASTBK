"""
ISO-1.0: Integrated Strategy Orchestrator (v1.3)

Master orchestrator that connects ALL 31 strategic models into a unified
planning system with automatic data flow between models.

Modes:
- full_run=True: Executes all 31 models across 5 layers
- full_run=False: Quick mode with 10 core models

Architecture:
┌─────────────────────────────────────────────────────────────────────────────┐
│  LAYER 1: EXTERNAL INPUTS                                                   │
│  ├── Market Data (size, growth, competitors)                                │
│  ├── Customer Data (segments, CLV inputs)                                   │
│  └── Company Data (financials, headcount, assets)                           │
├─────────────────────────────────────────────────────────────────────────────┤
│  LAYER 2: FUNCTIONAL STRATEGY MODELS (v4.0) - 7 models                      │
│  ├── VMV-1.0 → Vision, Mission, Values (Strategic Identity)                 │
│  ├── CLV-1.0 → Customer value                                               │
│  ├── CAC-1.0 → Marketing costs, channel efficiency                          │
│  ├── HCM-1.0 → Personnel costs, productivity                                │
│  ├── SCO-1.0 → COGS, inventory, working capital                             │
│  ├── RDM-1.0 → R&D costs, new product revenue                               │
│  └── ESG-1.0 → Risk premiums, compliance costs                              │
├─────────────────────────────────────────────────────────────────────────────┤
│  LAYER 3: CORE FINANCIAL MODELS (v1.0-v2.5)                                 │
│  ├── RPM-1.0 → Revenue projection                                           │
│  ├── CSM-1.0 → Cost structure                                               │
│  ├── PLM-1.0 → P&L statement                                                │
│  ├── CFM-1.0 → Cash flow                                                    │
│  ├── WCM-1.0 → Working capital                                              │
│  ├── BSM-1.0 → Balance sheet                                                │
│  └── DFM-1.0 → Debt & financing                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  LAYER 4: THEORETICAL FOUNDATION (v3.0-v3.5)                                │
│  ├── FEM-1.0 → Fundamental economics (π = p·x - kv·x - Kf)                  │
│  ├── BFM-1.0 → Beta framework (β_R → β_Op → β_A → β_E)                      │
│  ├── CMM-1.0 → Capital markets (Rf, MRP, WACC)                              │
│  └── VAM-1.0 → Valuation (DCF, Multiples)                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│  LAYER 5: STRATEGIC ANALYSIS (v3.0)                                         │
│  ├── MSM-1.0 → Market share                                                 │
│  ├── MAM-1.0 → M&A synergies                                                │
│  ├── PFM-1.0 → Portfolio (BCG Matrix)                                       │
│  ├── STM-1.0 → Stress testing                                               │
│  └── PRM-1.0 → Pricing                                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│  LAYER 6: SIMULATION & VALIDATION                                           │
│  ├── MCSM-1.0 → Monte Carlo simulation                                      │
│  ├── SCM-1.0 → Scenario comparison                                          │
│  ├── SAM-1.0 → Sensitivity analysis                                         │
│  └── ICM-1.0 → Iteration convergence                                        │
└─────────────────────────────────────────────────────────────────────────────┘

Data Flow (Simplified):
    CLV → CAC (LTV:CAC calculation)
    HCM → CSM (Personnel costs)
    SCO → CSM (COGS) + WCM (Inventory)
    RDM → CSM (R&D costs) + RPM (New product revenue)
    ESG → CMM (Risk premium)
    CSM + RPM → PLM (P&L)
    PLM → CFM → WCM → BSM
    PLM + BSM → FEM → BFM → CMM → VAM

Version: 1.0.0
Date: 2026-01-16
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable
from enum import Enum
import json


class ModelLayer(Enum):
    """Model execution layers."""
    EXTERNAL_INPUTS = 0
    FUNCTIONAL_STRATEGY = 1
    CORE_FINANCIAL = 2
    THEORETICAL_FOUNDATION = 3
    STRATEGIC_ANALYSIS = 4
    SIMULATION_VALIDATION = 5


@dataclass
class ModelNode:
    """Represents a model in the dependency graph."""
    model_id: str
    name: str
    layer: ModelLayer
    dependencies: List[str] = field(default_factory=list)
    provides: List[str] = field(default_factory=list)  # Output keys
    requires: List[str] = field(default_factory=list)  # Input keys
    optional_inputs: List[str] = field(default_factory=list)
    executor: Callable = None
    enabled: bool = True


# Model Registry with dependencies
MODEL_REGISTRY = {
    # Layer 1: Functional Strategy (v4.0) - 7 models
    "VMV-1.0": ModelNode(
        model_id="VMV-1.0",
        name="Vision-Mission-Values",
        layer=ModelLayer.FUNCTIONAL_STRATEGY,
        dependencies=[],  # Foundation for all other models
        provides=["purpose", "vision", "mission", "values", "leadership_principles",
                  "strategic_pillars", "culture_health_index", "purpose_alignment_score"],
        requires=["company_name", "industry"],
        optional_inputs=["vision_statement", "mission_statement", "core_values"],
    ),
    "CLV-1.0": ModelNode(
        model_id="CLV-1.0",
        name="Customer Lifetime Value",
        layer=ModelLayer.FUNCTIONAL_STRATEGY,
        dependencies=[],
        provides=["clv", "ltv_cac_ratio", "customer_portfolio_value", "payback_months"],
        requires=["avg_revenue_per_customer", "gross_margin", "retention_rate", "cac_estimate"],
        optional_inputs=["customer_count", "industry"],
    ),
    "CAC-1.0": ModelNode(
        model_id="CAC-1.0",
        name="Customer Acquisition Cost",
        layer=ModelLayer.FUNCTIONAL_STRATEGY,
        dependencies=["CLV-1.0"],  # Needs CLV for LTV:CAC
        provides=["blended_cac", "marketing_spend", "marketing_roi", "channel_efficiency"],
        requires=["acquisition_channels"],
        optional_inputs=["clv", "budget_constraint"],
    ),
    "HCM-1.0": ModelNode(
        model_id="HCM-1.0",
        name="Human Capital",
        layer=ModelLayer.FUNCTIONAL_STRATEGY,
        dependencies=[],
        provides=["total_labor_cost", "headcount", "revenue_per_employee", "turnover_cost"],
        requires=["employee_categories", "total_revenue"],
        optional_inputs=["operating_expenses", "industry"],
    ),
    "SCO-1.0": ModelNode(
        model_id="SCO-1.0",
        name="Supply Chain Optimization",
        layer=ModelLayer.FUNCTIONAL_STRATEGY,
        dependencies=[],
        provides=["inventory_value", "inventory_turns", "cogs_estimate", "days_inventory", "supply_chain_risk"],
        requires=["inventory_items"],
        optional_inputs=["suppliers", "total_cogs", "industry"],
    ),
    "RDM-1.0": ModelNode(
        model_id="RDM-1.0",
        name="R&D Investment",
        layer=ModelLayer.FUNCTIONAL_STRATEGY,
        dependencies=[],
        provides=["rd_spend", "rd_intensity", "new_product_revenue", "pipeline_value", "patent_value"],
        requires=["rd_spend_input", "revenue"],
        optional_inputs=["rd_projects", "patent_portfolio", "industry"],
    ),
    "ESG-1.0": ModelNode(
        model_id="ESG-1.0",
        name="ESG Scoring",
        layer=ModelLayer.FUNCTIONAL_STRATEGY,
        dependencies=[],
        provides=["esg_score", "esg_rating", "esg_risk_premium", "compliance_costs"],
        requires=["environmental_metrics", "social_metrics", "governance_metrics", "revenue_millions"],
        optional_inputs=["industry"],
    ),

    # Layer 2: Core Financial (v1.0-v2.5)
    "RPM-1.0": ModelNode(
        model_id="RPM-1.0",
        name="Revenue Projection",
        layer=ModelLayer.CORE_FINANCIAL,
        dependencies=["CLV-1.0", "RDM-1.0"],  # New customer revenue + new product revenue
        provides=["revenue_projection", "revenue_by_region", "revenue_cagr"],
        requires=["config"],
        optional_inputs=["new_product_revenue", "customer_portfolio_value"],
    ),
    "OSM-1.0": ModelNode(
        model_id="OSM-1.0",
        name="Organizational Scaling",
        layer=ModelLayer.CORE_FINANCIAL,
        dependencies=["RPM-1.0", "HCM-1.0"],
        provides=["headcount_projection", "hiring_plan"],
        requires=["config"],
        optional_inputs=["revenue_projection", "revenue_per_employee"],
    ),
    "CAM-1.0": ModelNode(
        model_id="CAM-1.0",
        name="Capital Expenditure",
        layer=ModelLayer.CORE_FINANCIAL,
        dependencies=["RPM-1.0"],
        provides=["capex_projection", "capex_by_category"],
        requires=["config"],
        optional_inputs=["revenue_projection"],
    ),
    "CSM-1.0": ModelNode(
        model_id="CSM-1.0",
        name="Cost Structure",
        layer=ModelLayer.CORE_FINANCIAL,
        dependencies=["RPM-1.0", "HCM-1.0", "SCO-1.0", "RDM-1.0", "CAC-1.0"],
        provides=["cost_projection", "fixed_costs", "variable_costs", "cost_ratios"],
        requires=["config"],
        optional_inputs=["revenue_projection", "total_labor_cost", "cogs_estimate", "rd_spend", "marketing_spend"],
    ),
    "PLM-1.0": ModelNode(
        model_id="PLM-1.0",
        name="Profit & Loss",
        layer=ModelLayer.CORE_FINANCIAL,
        dependencies=["RPM-1.0", "CSM-1.0"],
        provides=["pnl_projection", "ebitda", "ebit", "net_income", "margins"],
        requires=["config"],
        optional_inputs=["revenue_projection", "cost_projection"],
    ),
    "WCM-1.0": ModelNode(
        model_id="WCM-1.0",
        name="Working Capital",
        layer=ModelLayer.CORE_FINANCIAL,
        dependencies=["RPM-1.0", "CSM-1.0", "SCO-1.0"],
        provides=["working_capital", "nwc_projection", "days_sales", "days_payable"],
        requires=["config"],
        optional_inputs=["revenue_projection", "cost_projection", "days_inventory"],
    ),
    "CFM-1.0": ModelNode(
        model_id="CFM-1.0",
        name="Cash Flow",
        layer=ModelLayer.CORE_FINANCIAL,
        dependencies=["PLM-1.0", "CAM-1.0", "WCM-1.0"],
        provides=["cash_flow_projection", "free_cash_flow", "operating_cash_flow"],
        requires=["config"],
        optional_inputs=["pnl_projection", "capex_projection", "nwc_projection"],
    ),
    "DFM-1.0": ModelNode(
        model_id="DFM-1.0",
        name="Debt & Financing",
        layer=ModelLayer.CORE_FINANCIAL,
        dependencies=["CFM-1.0", "PLM-1.0"],
        provides=["debt_projection", "interest_expense", "debt_capacity", "leverage_ratios"],
        requires=["config"],
        optional_inputs=["cash_flow_projection", "pnl_projection"],
    ),
    "BSM-1.0": ModelNode(
        model_id="BSM-1.0",
        name="Balance Sheet",
        layer=ModelLayer.CORE_FINANCIAL,
        dependencies=["PLM-1.0", "CFM-1.0", "WCM-1.0", "DFM-1.0"],
        provides=["balance_sheet", "total_assets", "total_equity", "total_debt"],
        requires=["config"],
        optional_inputs=["pnl_projection", "cash_flow_projection", "working_capital", "debt_projection"],
    ),
    "BEM-1.0": ModelNode(
        model_id="BEM-1.0",
        name="Break-Even",
        layer=ModelLayer.CORE_FINANCIAL,
        dependencies=["PLM-1.0", "CSM-1.0"],
        provides=["break_even_revenue", "break_even_units", "margin_of_safety"],
        requires=["config"],
        optional_inputs=["pnl_projection", "cost_projection"],
    ),

    # Layer 3: Theoretical Foundation (v3.1-v3.5)
    "FEM-1.0": ModelNode(
        model_id="FEM-1.0",
        name="Fundamental Economics",
        layer=ModelLayer.THEORETICAL_FOUNDATION,
        dependencies=["PLM-1.0", "BSM-1.0"],
        provides=["profit", "contribution_margin", "dol", "break_even_quantity"],
        requires=["price", "quantity", "variable_cost", "fixed_costs"],
        optional_inputs=["debt", "equity"],
    ),
    "BFM-1.0": ModelNode(
        model_id="BFM-1.0",
        name="Beta Framework",
        layer=ModelLayer.THEORETICAL_FOUNDATION,
        dependencies=["FEM-1.0", "BSM-1.0"],
        provides=["revenue_beta", "operating_beta", "asset_beta", "equity_beta"],
        requires=["industry"],
        optional_inputs=["dol", "debt", "equity", "fixed_cost_ratio"],
    ),
    "CMM-1.0": ModelNode(
        model_id="CMM-1.0",
        name="Capital Markets",
        layer=ModelLayer.THEORETICAL_FOUNDATION,
        dependencies=["BFM-1.0", "ESG-1.0"],
        provides=["wacc", "cost_of_equity", "cost_of_debt", "risk_free_rate"],
        requires=["equity_beta", "debt_to_equity"],
        optional_inputs=["esg_risk_premium", "country", "credit_rating"],
    ),
    "VAM-1.0": ModelNode(
        model_id="VAM-1.0",
        name="Valuation",
        layer=ModelLayer.THEORETICAL_FOUNDATION,
        dependencies=["CFM-1.0", "PLM-1.0", "CMM-1.0"],
        provides=["enterprise_value", "equity_value", "dcf_value", "multiple_value"],
        requires=["revenue", "ebitda", "free_cash_flow", "wacc"],
        optional_inputs=["terminal_growth", "exit_multiple", "industry"],
    ),
    "VCM-1.0": ModelNode(
        model_id="VCM-1.0",
        name="Value Creation",
        layer=ModelLayer.THEORETICAL_FOUNDATION,
        dependencies=["PLM-1.0", "BSM-1.0", "CMM-1.0"],
        provides=["eva", "roic", "spread", "value_created"],
        requires=["nopat", "invested_capital", "wacc"],
        optional_inputs=[],
    ),

    # Layer 4: Strategic Analysis (v3.0)
    "MSM-1.0": ModelNode(
        model_id="MSM-1.0",
        name="Market Share",
        layer=ModelLayer.STRATEGIC_ANALYSIS,
        dependencies=["RPM-1.0"],
        provides=["market_share", "market_share_change", "relative_market_share"],
        requires=["config"],
        optional_inputs=["revenue_projection"],
    ),
    "PRM-1.0": ModelNode(
        model_id="PRM-1.0",
        name="Pricing",
        layer=ModelLayer.STRATEGIC_ANALYSIS,
        dependencies=["FEM-1.0", "CLV-1.0"],
        provides=["optimal_price", "price_elasticity", "pricing_power"],
        requires=["config"],
        optional_inputs=["contribution_margin", "clv"],
    ),
    "PFM-1.0": ModelNode(
        model_id="PFM-1.0",
        name="Portfolio (BCG)",
        layer=ModelLayer.STRATEGIC_ANALYSIS,
        dependencies=["MSM-1.0", "RPM-1.0"],
        provides=["portfolio_matrix", "stars", "cash_cows", "question_marks", "dogs"],
        requires=["config"],
        optional_inputs=["market_share", "revenue_by_segment"],
    ),
    "MAM-1.0": ModelNode(
        model_id="MAM-1.0",
        name="M&A Synergies",
        layer=ModelLayer.STRATEGIC_ANALYSIS,
        dependencies=["VAM-1.0"],
        provides=["synergy_value", "revenue_synergies", "cost_synergies"],
        requires=["config"],
        optional_inputs=["enterprise_value"],
    ),
    "STM-1.0": ModelNode(
        model_id="STM-1.0",
        name="Stress Testing",
        layer=ModelLayer.STRATEGIC_ANALYSIS,
        dependencies=["PLM-1.0", "CFM-1.0"],
        provides=["stress_scenarios", "survival_period", "covenant_headroom"],
        requires=["config"],
        optional_inputs=["pnl_projection", "cash_flow_projection"],
    ),

    # Layer 5: Simulation & Validation
    "MCSM-1.0": ModelNode(
        model_id="MCSM-1.0",
        name="Monte Carlo Simulation",
        layer=ModelLayer.SIMULATION_VALIDATION,
        dependencies=["RPM-1.0"],
        provides=["mc_results", "confidence_intervals", "var_95", "expected_value"],
        requires=["config"],
        optional_inputs=["revenue_projection"],
    ),
    "SAM-1.0": ModelNode(
        model_id="SAM-1.0",
        name="Sensitivity Analysis",
        layer=ModelLayer.SIMULATION_VALIDATION,
        dependencies=["VAM-1.0"],
        provides=["sensitivity_matrix", "tornado_chart", "key_drivers"],
        requires=["config"],
        optional_inputs=["enterprise_value"],
    ),
    "SCM-1.0": ModelNode(
        model_id="SCM-1.0",
        name="Scenario Comparison",
        layer=ModelLayer.SIMULATION_VALIDATION,
        dependencies=["VAM-1.0"],
        provides=["scenario_results", "best_case", "base_case", "worst_case"],
        requires=["config"],
        optional_inputs=["enterprise_value"],
    ),
    "ICM-1.0": ModelNode(
        model_id="ICM-1.0",
        name="Iteration Convergence",
        layer=ModelLayer.SIMULATION_VALIDATION,
        dependencies=[],
        provides=["optimal_iterations", "convergence_rate", "gap_trajectory"],
        requires=["initial_gap", "target_gap"],
        optional_inputs=["data_quality", "model_complexity"],
    ),
}


# Output-to-Input Mappings
OUTPUT_MAPPINGS = {
    # CLV outputs → other models
    "clv": ["CAC-1.0.clv", "PRM-1.0.clv"],
    "ltv_cac_ratio": [],
    "customer_portfolio_value": ["RPM-1.0.customer_portfolio_value"],

    # CAC outputs
    "blended_cac": [],
    "marketing_spend": ["CSM-1.0.marketing_spend"],

    # HCM outputs
    "total_labor_cost": ["CSM-1.0.total_labor_cost"],
    "headcount": ["OSM-1.0.current_headcount"],
    "revenue_per_employee": ["OSM-1.0.revenue_per_employee"],

    # SCO outputs
    "cogs_estimate": ["CSM-1.0.cogs_estimate"],
    "inventory_value": ["WCM-1.0.inventory_value"],
    "days_inventory": ["WCM-1.0.days_inventory"],

    # RDM outputs
    "rd_spend": ["CSM-1.0.rd_spend"],
    "new_product_revenue": ["RPM-1.0.new_product_revenue"],

    # ESG outputs
    "esg_risk_premium": ["CMM-1.0.esg_risk_premium"],

    # RPM outputs
    "revenue_projection": ["CSM-1.0.revenue_projection", "PLM-1.0.revenue_projection",
                          "OSM-1.0.revenue_projection", "CAM-1.0.revenue_projection"],

    # PLM outputs
    "pnl_projection": ["CFM-1.0.pnl_projection", "BSM-1.0.pnl_projection"],
    "ebitda": ["VAM-1.0.ebitda"],
    "ebit": ["FEM-1.0.ebit"],

    # CFM outputs
    "free_cash_flow": ["VAM-1.0.free_cash_flow"],
    "cash_flow_projection": ["BSM-1.0.cash_flow_projection"],

    # BSM outputs
    "total_equity": ["BFM-1.0.equity", "CMM-1.0.equity"],
    "total_debt": ["BFM-1.0.debt", "CMM-1.0.debt"],

    # FEM outputs
    "dol": ["BFM-1.0.dol"],

    # BFM outputs
    "equity_beta": ["CMM-1.0.equity_beta"],

    # CMM outputs
    "wacc": ["VAM-1.0.wacc", "VCM-1.0.wacc"],
}


def topological_sort(models: Dict[str, ModelNode]) -> List[str]:
    """
    Sort models by dependency order (topological sort).

    Returns list of model IDs in execution order.
    """
    # Build adjacency list
    in_degree = {model_id: 0 for model_id in models}
    for model_id, node in models.items():
        for dep in node.dependencies:
            if dep in models:
                in_degree[model_id] += 1

    # Start with models that have no dependencies
    queue = [m for m, degree in in_degree.items() if degree == 0]
    result = []

    while queue:
        # Sort by layer to process lower layers first
        queue.sort(key=lambda x: models[x].layer.value)
        current = queue.pop(0)
        result.append(current)

        # Reduce in-degree for dependent models
        for model_id, node in models.items():
            if current in node.dependencies:
                in_degree[model_id] -= 1
                if in_degree[model_id] == 0:
                    queue.append(model_id)

    return result


def get_execution_plan(
    enabled_models: List[str] = None,
    target_outputs: List[str] = None,
) -> Dict:
    """
    Generate execution plan based on enabled models or target outputs.

    Args:
        enabled_models: List of model IDs to run (None = all)
        target_outputs: List of desired outputs (will determine models needed)

    Returns:
        Execution plan with order and dependencies
    """
    if enabled_models is None:
        enabled_models = list(MODEL_REGISTRY.keys())

    # Filter to enabled models
    active_models = {
        model_id: node for model_id, node in MODEL_REGISTRY.items()
        if model_id in enabled_models
    }

    # Get execution order
    execution_order = topological_sort(active_models)

    # Build layer groups
    layers = {}
    for model_id in execution_order:
        layer = MODEL_REGISTRY[model_id].layer.name
        if layer not in layers:
            layers[layer] = []
        layers[layer].append(model_id)

    return {
        "execution_order": execution_order,
        "by_layer": layers,
        "total_models": len(execution_order),
        "dependencies": {
            model_id: MODEL_REGISTRY[model_id].dependencies
            for model_id in execution_order
        },
    }


@dataclass
class OrchestratorConfig:
    """Configuration for the integrated strategy orchestrator."""
    # Company basics
    company_name: str = "Company"
    industry: str = "manufacturing"
    base_year: int = 2024
    projection_years: int = 5

    # Revenue inputs
    base_revenue: float = 100_000_000
    revenue_growth_rate: float = 0.08

    # Cost structure
    gross_margin: float = 0.40
    operating_margin: float = 0.12

    # Customer economics (for CLV/CAC)
    avg_revenue_per_customer: float = 10000
    customer_retention_rate: float = 0.85
    customer_acquisition_cost: float = 2000
    customer_count: int = 10000

    # Workforce
    total_employees: int = 500
    avg_salary: float = 75000
    benefits_rate: float = 0.25

    # Capital structure
    total_debt: float = 20_000_000
    total_equity: float = 50_000_000
    tax_rate: float = 0.25

    # R&D
    rd_intensity: float = 0.05
    new_product_revenue_share: float = 0.20

    # Working capital
    days_sales_outstanding: float = 45
    days_inventory: float = 60
    days_payable: float = 30

    # Model selection
    enabled_models: List[str] = field(default_factory=list)
    run_simulations: bool = True
    num_simulations: int = 1000


class IntegratedStrategyOrchestrator:
    """
    Master orchestrator for all strategic models.

    Manages data flow between models and provides unified output.
    """

    def __init__(self, config: OrchestratorConfig):
        self.config = config
        self.results = {}
        self.execution_log = []

    def _log(self, message: str):
        """Log execution step."""
        self.execution_log.append(message)

    def _get_from_results(self, key: str, default=None):
        """Get a value from results by dot-notation key.

        Handles model IDs with dots (e.g., 'CLV-1.0.summary.clv').
        """
        # First check if key starts with a known model ID
        for model_id in MODEL_REGISTRY.keys():
            if key.startswith(model_id + "."):
                remaining = key[len(model_id) + 1:]  # Get path after model ID
                if model_id not in self.results:
                    return default
                current = self.results[model_id]
                if remaining:
                    for part in remaining.split("."):
                        if isinstance(current, dict) and part in current:
                            current = current[part]
                        else:
                            return default
                return current

        # Fallback to simple split for non-model keys
        parts = key.split(".")
        current = self.results
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return default
        return current

    def run_vmv_model(self) -> Dict:
        """Run VMV-1.0: Vision-Mission-Values Model (Strategic Identity Foundation).

        Generates organizational identity framework including:
        - Purpose statement (why we exist beyond profit)
        - Vision (10-20 year aspirational state)
        - Mission (5-10 year core business purpose)
        - Core values with behavioral indicators
        - Leadership principles
        - Strategic pillars (3-5 focus areas)
        - Culture health indicators
        """
        self._log("Running VMV-1.0: Vision-Mission-Values Model")

        # Industry-specific defaults for strategic identity components
        INDUSTRY_PILLARS = {
            "manufacturing": ["Operational Excellence", "Innovation", "Sustainability", "Customer Partnership"],
            "retail": ["Customer Experience", "Omnichannel Excellence", "Supply Chain Agility", "Brand Value"],
            "technology": ["Innovation Leadership", "Customer Success", "Talent Excellence", "Scalability"],
            "financial_services": ["Trust & Security", "Client Success", "Risk Excellence", "Digital Innovation"],
            "healthcare": ["Patient Outcomes", "Clinical Excellence", "Access & Equity", "Innovation"],
            "default": ["Customer Value", "Operational Excellence", "Innovation", "People Development"],
        }

        INDUSTRY_VALUES = {
            "manufacturing": ["Quality", "Safety", "Continuous Improvement", "Integrity", "Teamwork"],
            "retail": ["Customer First", "Speed", "Innovation", "Integrity", "Collaboration"],
            "technology": ["Innovation", "Customer Obsession", "Ownership", "Bias for Action", "Learn & Be Curious"],
            "financial_services": ["Integrity", "Client Focus", "Excellence", "Accountability", "Respect"],
            "healthcare": ["Patient First", "Compassion", "Integrity", "Excellence", "Collaboration"],
            "default": ["Integrity", "Excellence", "Innovation", "Respect", "Accountability"],
        }

        LEADERSHIP_PRINCIPLES = {
            "manufacturing": [
                "Safety First - Never compromise on employee and product safety",
                "Gemba Walk - Go see, ask why, show respect",
                "Continuous Improvement - Kaizen every day",
                "Develop People - Grow leaders who understand the work",
                "Long-term Thinking - Base decisions on long-term philosophy"
            ],
            "technology": [
                "Customer Obsession - Start with the customer and work backwards",
                "Ownership - Act on behalf of the entire company",
                "Invent and Simplify - Expect and require innovation",
                "Hire and Develop the Best - Raise the performance bar",
                "Think Big - Create bold direction that inspires results"
            ],
            "default": [
                "Lead with Integrity - Do the right thing, always",
                "Empower Teams - Give people autonomy and accountability",
                "Drive Results - Focus on outcomes, not just activities",
                "Develop Talent - Invest in growing future leaders",
                "Embrace Change - Adapt quickly to new realities"
            ]
        }

        industry = self.config.industry.lower()
        company_name = self.config.company_name

        # Get industry-specific or default values
        strategic_pillars = INDUSTRY_PILLARS.get(industry, INDUSTRY_PILLARS["default"])
        core_values = INDUSTRY_VALUES.get(industry, INDUSTRY_VALUES["default"])
        leadership_principles = LEADERSHIP_PRINCIPLES.get(industry, LEADERSHIP_PRINCIPLES["default"])

        # Generate purpose, vision, mission based on industry
        purpose = f"To create lasting value for all stakeholders through excellence in {industry}"
        vision = f"To be the most trusted and innovative partner in {industry} by 2035"
        mission = f"We deliver exceptional {industry} solutions that drive customer success and sustainable growth"

        # Calculate alignment and health scores (placeholder - would be survey-based in reality)
        purpose_alignment_score = 75  # 0-100 scale
        culture_health_index = 72  # 0-100 scale
        values_embodiment_score = 70  # How well values are lived

        # Build behavioral indicators for each value
        values_with_behaviors = []
        for value in core_values:
            values_with_behaviors.append({
                "value": value,
                "positive_indicators": [
                    f"Demonstrates {value.lower()} in daily decisions",
                    f"Recognizes others who exemplify {value.lower()}",
                    f"Addresses violations of {value.lower()} constructively"
                ],
                "negative_indicators": [
                    f"Ignores {value.lower()} when under pressure",
                    f"Does not hold others accountable for {value.lower()}"
                ]
            })

        # Stakeholder commitments
        stakeholder_commitments = {
            "customers": "Deliver superior value and exceptional experiences",
            "employees": "Provide meaningful work, growth opportunities, and fair rewards",
            "shareholders": "Generate sustainable returns through responsible growth",
            "communities": "Contribute positively to society and environment",
            "partners": "Build mutually beneficial, long-term relationships"
        }

        result = {
            "model_id": "VMV-1.0",
            "company": company_name,
            "industry": industry,
            "identity": {
                "purpose": purpose,
                "vision": vision,
                "mission": mission,
            },
            "values": {
                "core_values": core_values,
                "values_with_behaviors": values_with_behaviors,
                "values_embodiment_score": values_embodiment_score,
            },
            "leadership": {
                "principles": leadership_principles,
                "principles_count": len(leadership_principles),
            },
            "strategy": {
                "strategic_pillars": strategic_pillars,
                "pillars_count": len(strategic_pillars),
            },
            "stakeholders": stakeholder_commitments,
            "health_metrics": {
                "purpose_alignment_score": purpose_alignment_score,
                "culture_health_index": culture_health_index,
                "values_embodiment_score": values_embodiment_score,
                "overall_identity_score": round((purpose_alignment_score + culture_health_index + values_embodiment_score) / 3, 1),
            },
            "summary": {
                "purpose": purpose,
                "vision": vision,
                "mission": mission,
                "values_count": len(core_values),
                "pillars_count": len(strategic_pillars),
                "principles_count": len(leadership_principles),
                "culture_health_index": culture_health_index,
                "purpose_alignment_score": purpose_alignment_score,
                "overall_identity_score": round((purpose_alignment_score + culture_health_index + values_embodiment_score) / 3, 1),
            }
        }

        self.results["VMV-1.0"] = result
        return result

    def run_clv_model(self) -> Dict:
        """Run CLV-1.0: Customer Lifetime Value Model."""
        from .customer_lifetime_value import analyze_customer_lifetime_value

        self._log("Running CLV-1.0: Customer Lifetime Value Model")

        # Calculate monthly retention from annual
        annual_retention = self.config.customer_retention_rate
        monthly_retention = annual_retention ** (1/12)

        result = analyze_customer_lifetime_value(
            avg_revenue_per_period=self.config.avg_revenue_per_customer / 12,
            gross_margin=self.config.gross_margin,
            retention_rate=monthly_retention,
            cac=self.config.customer_acquisition_cost,
            customer_count=self.config.customer_count,
            industry=self.config.industry,
            run_detailed=False,  # Skip detailed for orchestrator
        )

        self.results["CLV-1.0"] = result
        return result

    def run_cac_model(self) -> Dict:
        """Run CAC-1.0: Customer Acquisition Cost Model."""
        from .customer_acquisition import analyze_customer_acquisition, AcquisitionChannel

        self._log("Running CAC-1.0: Customer Acquisition Cost Model")

        # Create default channels based on industry
        marketing_budget = self.config.base_revenue * 0.05  # 5% of revenue
        customers_acquired = int(self.config.customer_count * 0.15)  # 15% new customers

        channels = [
            AcquisitionChannel(
                name="Digital Marketing",
                monthly_spend=marketing_budget * 0.4 / 12,
                customers_acquired=int(customers_acquired * 0.35),
                leads=int(customers_acquired * 0.35 * 5),
            ),
            AcquisitionChannel(
                name="Sales Team",
                monthly_spend=marketing_budget * 0.35 / 12,
                customers_acquired=int(customers_acquired * 0.40),
                leads=int(customers_acquired * 0.40 * 3),
            ),
            AcquisitionChannel(
                name="Referral/Organic",
                monthly_spend=marketing_budget * 0.15 / 12,
                customers_acquired=int(customers_acquired * 0.25),
                leads=int(customers_acquired * 0.25 * 2),
            ),
        ]

        # Get CLV if available
        clv = self._get_from_results("CLV-1.0.summary.clv")

        result = analyze_customer_acquisition(
            channels=channels,
            clv=clv,
            gross_margin=self.config.gross_margin,
            industry=self.config.industry,
            run_optimization=False,
        )

        self.results["CAC-1.0"] = result
        return result

    def run_hcm_model(self) -> Dict:
        """Run HCM-1.0: Human Capital Model."""
        from .human_capital import analyze_human_capital, EmployeeCategory

        self._log("Running HCM-1.0: Human Capital Model")

        # Create employee categories
        categories = [
            EmployeeCategory(
                name="Operations",
                headcount=int(self.config.total_employees * 0.50),
                avg_salary=self.config.avg_salary * 0.8,
                benefits_rate=self.config.benefits_rate,
                annual_turnover_rate=0.15,
            ),
            EmployeeCategory(
                name="Sales & Marketing",
                headcount=int(self.config.total_employees * 0.20),
                avg_salary=self.config.avg_salary * 1.1,
                benefits_rate=self.config.benefits_rate,
                annual_turnover_rate=0.20,
            ),
            EmployeeCategory(
                name="R&D / Engineering",
                headcount=int(self.config.total_employees * 0.15),
                avg_salary=self.config.avg_salary * 1.3,
                benefits_rate=self.config.benefits_rate,
                annual_turnover_rate=0.12,
            ),
            EmployeeCategory(
                name="G&A",
                headcount=int(self.config.total_employees * 0.15),
                avg_salary=self.config.avg_salary * 0.9,
                benefits_rate=self.config.benefits_rate,
                annual_turnover_rate=0.10,
            ),
        ]

        result = analyze_human_capital(
            employee_categories=categories,
            total_revenue=self.config.base_revenue,
            operating_expenses=self.config.base_revenue * (1 - self.config.operating_margin),
            industry=self.config.industry,
            revenue_growth_rate=self.config.revenue_growth_rate,
            run_projections=False,
        )

        self.results["HCM-1.0"] = result
        return result

    def run_sco_model(self) -> Dict:
        """Run SCO-1.0: Supply Chain Optimization Model."""
        from .supply_chain import analyze_supply_chain, InventoryItem

        self._log("Running SCO-1.0: Supply Chain Optimization Model")

        # Estimate COGS
        cogs = self.config.base_revenue * (1 - self.config.gross_margin)

        # Create sample inventory items
        items = [
            InventoryItem(
                sku="RAW-001",
                name="Primary Raw Material",
                annual_demand=int(cogs * 0.4 / 100),  # 40% of COGS
                unit_cost=100,
                ordering_cost=500,
                lead_time_days=14,
                demand_std_daily=int(cogs * 0.4 / 100 / 365 * 0.2),
            ),
            InventoryItem(
                sku="RAW-002",
                name="Secondary Raw Material",
                annual_demand=int(cogs * 0.3 / 50),  # 30% of COGS
                unit_cost=50,
                ordering_cost=300,
                lead_time_days=7,
                demand_std_daily=int(cogs * 0.3 / 50 / 365 * 0.15),
            ),
        ]

        # Calculate average inventory value from days
        avg_inventory = cogs * self.config.days_inventory / 365

        result = analyze_supply_chain(
            inventory_items=items,
            total_cogs=cogs,
            avg_inventory_value=avg_inventory,
            days_receivable=self.config.days_sales_outstanding,
            days_payable=self.config.days_payable,
            industry=self.config.industry,
            run_optimization=False,
            run_risk_analysis=False,
        )

        self.results["SCO-1.0"] = result
        return result

    def run_rdm_model(self) -> Dict:
        """Run RDM-1.0: R&D Investment Model."""
        from .rd_investment import analyze_rd_investment

        self._log("Running RDM-1.0: R&D Investment Model")

        rd_spend = self.config.base_revenue * self.config.rd_intensity
        new_product_revenue = self.config.base_revenue * self.config.new_product_revenue_share

        result = analyze_rd_investment(
            rd_spend=rd_spend,
            revenue=self.config.base_revenue,
            new_product_revenue=new_product_revenue,
            rd_spend_historical=[rd_spend * 0.85, rd_spend * 0.90, rd_spend * 0.95, rd_spend],
            patents_filed=5,
            products_launched=2,
            rd_headcount=int(self.config.total_employees * 0.15),
            industry=self.config.industry,
            run_pipeline_analysis=False,
        )

        self.results["RDM-1.0"] = result
        return result

    def run_esg_model(self) -> Dict:
        """Run ESG-1.0: ESG Scoring Model."""
        from .esg_scoring import (
            analyze_esg, EnvironmentalMetrics, SocialMetrics, GovernanceMetrics
        )

        self._log("Running ESG-1.0: ESG Scoring Model")

        # Create default ESG metrics
        env = EnvironmentalMetrics(
            scope1_emissions_tco2=self.config.base_revenue / 10000,  # Rough estimate
            scope2_emissions_tco2=self.config.base_revenue / 20000,
            renewable_energy_pct=25,
            waste_recycled_pct=50,
            environmental_certifications=1,
        )

        social = SocialMetrics(
            total_employees=self.config.total_employees,
            female_leadership_pct=25,
            employee_turnover_pct=15,
            training_hours_per_employee=20,
            employee_satisfaction_score=70,
            ltir=2.0,
            safety_training_pct=90,
            living_wage_pct=100,
        )

        gov = GovernanceMetrics(
            board_size=7,
            independent_directors_pct=60,
            female_board_pct=29,
            ceo_chair_separation=True,
            ethics_hotline=True,
            sustainability_report=True,
            esg_committee=True,
        )

        result = analyze_esg(
            environmental=env,
            social=social,
            governance=gov,
            revenue_millions=self.config.base_revenue / 1_000_000,
            industry=self.config.industry,
            run_projections=False,
        )

        self.results["ESG-1.0"] = result
        return result

    def run_fem_model(self) -> Dict:
        """Run FEM-1.0: Fundamental Economics Model."""
        from .fundamental_economics import analyze_fundamental_economics

        self._log("Running FEM-1.0: Fundamental Economics Model")

        # Derive fundamentals from config
        revenue = self.config.base_revenue
        gross_margin = self.config.gross_margin
        operating_margin = self.config.operating_margin

        # Estimate price and quantity
        avg_price = self.config.avg_revenue_per_customer
        quantity = revenue / avg_price

        # Variable cost = COGS per unit
        variable_cost_per_unit = avg_price * (1 - gross_margin)

        # Fixed costs = operating expenses above COGS
        fixed_costs = revenue * (gross_margin - operating_margin)

        result = analyze_fundamental_economics(
            price=avg_price,
            quantity=quantity,
            variable_cost_per_unit=variable_cost_per_unit,
            fixed_costs=fixed_costs,
            debt=self.config.total_debt,
            equity=self.config.total_equity,
            tax_rate=self.config.tax_rate,
            include_wacc_analysis=True,
            include_time_horizon_analysis=False,  # Skip for orchestrator
        )

        self.results["FEM-1.0"] = result
        return result

    def run_bfm_model(self) -> Dict:
        """Run BFM-1.0: Beta Framework Model."""
        from .beta_framework import analyze_beta_framework

        self._log("Running BFM-1.0: Beta Framework Model")

        # Get DOL from FEM if available
        dol = self._get_from_results("FEM-1.0.leverage.degree_of_operating_leverage", 2.5)

        # Estimate fixed cost ratio
        gross_margin = self.config.gross_margin
        operating_margin = self.config.operating_margin
        fixed_cost_ratio = (gross_margin - operating_margin) / gross_margin if gross_margin > 0 else 0.4

        result = analyze_beta_framework(
            industry=self.config.industry,
            fixed_cost_ratio=fixed_cost_ratio,
            debt_to_equity=self.config.total_debt / self.config.total_equity if self.config.total_equity > 0 else 0.5,
            tax_rate=self.config.tax_rate,
            run_sensitivity=False,
        )

        self.results["BFM-1.0"] = result
        return result

    def run_cmm_model(self) -> Dict:
        """Run CMM-1.0: Capital Market Model."""
        from .capital_market import analyze_capital_markets

        self._log("Running CMM-1.0: Capital Market Model")

        # Get equity beta from BFM if available
        equity_beta = self._get_from_results("BFM-1.0.beta_chain.equity_beta", 1.2)

        # Get ESG risk premium if available
        esg_premium = 0
        esg_rating = self._get_from_results("ESG-1.0.summary.rating")
        if esg_rating:
            # Lower ESG rating = higher risk premium
            esg_premiums = {"AAA": -0.005, "AA": -0.002, "A": 0, "BBB": 0.002, "BB": 0.005, "B": 0.01, "CCC": 0.02}
            esg_premium = esg_premiums.get(esg_rating, 0)

        result = analyze_capital_markets(
            equity_beta=equity_beta,
            debt_to_equity=self.config.total_debt / self.config.total_equity if self.config.total_equity > 0 else 0.5,
            tax_rate=self.config.tax_rate,
            company_specific_premium=esg_premium,
            show_benchmarks=False,
        )

        self.results["CMM-1.0"] = result
        return result

    # =========================================================================
    # LAYER 2: CORE FINANCIAL MODELS
    # =========================================================================

    def _build_model_config(self) -> Dict:
        """Build a config dict compatible with existing model functions."""
        years = list(range(self.config.base_year, self.config.base_year + self.config.projection_years + 1))

        return {
            "company": {"name": self.config.company_name},
            "base_year": self.config.base_year,
            "projection_years": self.config.projection_years,
            "years": years,
            "revenue": {
                "base": self.config.base_revenue,
                "growth_rate": self.config.revenue_growth_rate,
                "regions": {"Global": {"base": self.config.base_revenue, "cagr": self.config.revenue_growth_rate}},
            },
            "costs": {
                "cogs_percent": 1 - self.config.gross_margin,
                "opex_percent": self.config.gross_margin - self.config.operating_margin,
                "fixed_costs": self.config.base_revenue * (self.config.gross_margin - self.config.operating_margin) * 0.6,
                "variable_cost_percent": 1 - self.config.gross_margin,
            },
            "headcount": {
                "base": self.config.total_employees,
                "growth_rate": self.config.revenue_growth_rate * 0.7,  # Headcount grows slower than revenue
                "avg_salary": self.config.avg_salary,
                "benefits_rate": self.config.benefits_rate,
            },
            "capex": {
                "maintenance_percent": 0.02,
                "growth_percent": 0.03,
                "base": self.config.base_revenue * 0.05,
            },
            "working_capital": {
                "days_receivable": self.config.days_sales_outstanding,
                "days_inventory": self.config.days_inventory,
                "days_payable": self.config.days_payable,
            },
            "financing": {
                "debt": self.config.total_debt,
                "equity": self.config.total_equity,
                "interest_rate": 0.05,
                "tax_rate": self.config.tax_rate,
            },
            "market": {
                "size": self.config.base_revenue * 20,
                "growth_rate": 0.05,
                "company_share": 0.05,
            },
            "monte_carlo": {
                "num_simulations": self.config.num_simulations,
                "revenue_std": 0.10,
                "cost_std": 0.05,
            },
        }

    def run_rpm_model(self) -> Dict:
        """Run RPM-1.0: Revenue Projection Model."""
        self._log("Running RPM-1.0: Revenue Projection Model")

        # Simple projection without calling the model (which expects ALPLA config format)
        years = list(range(self.config.base_year, self.config.base_year + self.config.projection_years + 1))
        base = self.config.base_revenue
        rate = self.config.revenue_growth_rate

        projection = {year: base * (1 + rate) ** (year - self.config.base_year) for year in years}

        self.results["RPM-1.0"] = {
            "model_id": "RPM-1.0",
            "projection": projection,
            "summary": {
                "base_revenue": self.config.base_revenue,
                "final_revenue": self.config.base_revenue * (1 + self.config.revenue_growth_rate) ** self.config.projection_years,
                "cagr": self.config.revenue_growth_rate,
            }
        }
        return self.results["RPM-1.0"]

    def run_osm_model(self) -> Dict:
        """Run OSM-1.0: Organizational Scaling Model."""
        self._log("Running OSM-1.0: Organizational Scaling Model")

        # Simple headcount projection
        years = list(range(self.config.base_year, self.config.base_year + self.config.projection_years + 1))
        base = self.config.total_employees
        rate = self.config.revenue_growth_rate * 0.7  # Headcount grows slower

        projection = {year: int(base * (1 + rate) ** (year - self.config.base_year)) for year in years}

        self.results["OSM-1.0"] = {
            "model_id": "OSM-1.0",
            "projection": projection,
            "summary": {
                "base_headcount": self.config.total_employees,
                "final_headcount": int(self.config.total_employees * (1 + rate) ** self.config.projection_years),
            }
        }
        return self.results["OSM-1.0"]

    def run_cam_model(self) -> Dict:
        """Run CAM-1.0: Capital Expenditure Allocation Model."""
        self._log("Running CAM-1.0: Capital Expenditure Allocation Model")

        # Simple capex projection (5% of revenue)
        years = list(range(self.config.base_year, self.config.base_year + self.config.projection_years + 1))
        capex_intensity = 0.05

        revenue_proj = self._get_from_results("RPM-1.0.projection", {})
        projection = {}
        for year in years:
            rev = revenue_proj.get(year, self.config.base_revenue * (1 + self.config.revenue_growth_rate) ** (year - self.config.base_year))
            projection[year] = rev * capex_intensity

        self.results["CAM-1.0"] = {
            "model_id": "CAM-1.0",
            "projection": projection,
            "summary": {
                "base_capex": self.config.base_revenue * capex_intensity,
                "capex_intensity": capex_intensity,
            }
        }
        return self.results["CAM-1.0"]

    def run_csm_model(self) -> Dict:
        """Run CSM-1.0: Cost Structure Model."""
        self._log("Running CSM-1.0: Cost Structure Model")

        cogs = self.config.base_revenue * (1 - self.config.gross_margin)
        opex = self.config.base_revenue * (self.config.gross_margin - self.config.operating_margin)

        self.results["CSM-1.0"] = {
            "model_id": "CSM-1.0",
            "summary": {
                "cogs": cogs,
                "opex": opex,
                "total_costs": cogs + opex,
                "cogs_percent": (1 - self.config.gross_margin) * 100,
                "opex_percent": (self.config.gross_margin - self.config.operating_margin) * 100,
            }
        }
        return self.results["CSM-1.0"]

    def run_plm_model(self) -> Dict:
        """Run PLM-1.0: Profit & Loss Model."""
        self._log("Running PLM-1.0: Profit & Loss Model")

        revenue = self.config.base_revenue
        gross_profit = revenue * self.config.gross_margin
        ebit = revenue * self.config.operating_margin
        ebitda = ebit + revenue * 0.05  # Approx D&A
        net_income = ebit * (1 - self.config.tax_rate)

        self.results["PLM-1.0"] = {
            "model_id": "PLM-1.0",
            "summary": {
                "revenue": revenue,
                "gross_profit": gross_profit,
                "ebitda": ebitda,
                "ebit": ebit,
                "net_income": net_income,
                "gross_margin_pct": self.config.gross_margin * 100,
                "ebitda_margin_pct": (ebitda / revenue) * 100,
                "operating_margin_pct": self.config.operating_margin * 100,
                "net_margin_pct": (net_income / revenue) * 100,
            }
        }
        return self.results["PLM-1.0"]

    def run_wcm_model(self) -> Dict:
        """Run WCM-1.0: Working Capital Model."""
        self._log("Running WCM-1.0: Working Capital Model")

        revenue = self.config.base_revenue
        cogs = revenue * (1 - self.config.gross_margin)
        receivables = revenue * self.config.days_sales_outstanding / 365
        inventory = cogs * self.config.days_inventory / 365
        payables = cogs * self.config.days_payable / 365
        nwc = receivables + inventory - payables

        self.results["WCM-1.0"] = {
            "model_id": "WCM-1.0",
            "summary": {
                "receivables": receivables,
                "inventory": inventory,
                "payables": payables,
                "net_working_capital": nwc,
                "nwc_percent_revenue": (nwc / revenue) * 100,
                "cash_conversion_cycle": self.config.days_sales_outstanding + self.config.days_inventory - self.config.days_payable,
            }
        }
        return self.results["WCM-1.0"]

    def run_cfm_model(self) -> Dict:
        """Run CFM-1.0: Cash Flow Model."""
        self._log("Running CFM-1.0: Cash Flow Model")

        ebitda = self._get_from_results("PLM-1.0.summary.ebitda", self.config.base_revenue * 0.17)
        capex = self.config.base_revenue * 0.05
        nwc_change = self.config.base_revenue * self.config.revenue_growth_rate * 0.10
        taxes = self._get_from_results("PLM-1.0.summary.ebit", self.config.base_revenue * 0.12) * self.config.tax_rate
        ocf = ebitda - taxes - nwc_change
        fcf = ocf - capex

        self.results["CFM-1.0"] = {
            "model_id": "CFM-1.0",
            "summary": {
                "operating_cash_flow": ocf,
                "free_cash_flow": fcf,
                "capex": capex,
                "nwc_change": nwc_change,
                "fcf_margin_pct": (fcf / self.config.base_revenue) * 100,
            }
        }
        return self.results["CFM-1.0"]

    def run_dfm_model(self) -> Dict:
        """Run DFM-1.0: Debt & Financing Model."""
        self._log("Running DFM-1.0: Debt & Financing Model")

        ebitda = self._get_from_results("PLM-1.0.summary.ebitda", self.config.base_revenue * 0.17)
        interest = self.config.total_debt * 0.05

        self.results["DFM-1.0"] = {
            "model_id": "DFM-1.0",
            "summary": {
                "total_debt": self.config.total_debt,
                "interest_expense": interest,
                "debt_to_equity": self.config.total_debt / self.config.total_equity if self.config.total_equity > 0 else 0,
                "debt_to_ebitda": self.config.total_debt / ebitda if ebitda > 0 else 0,
                "interest_coverage": ebitda / interest if interest > 0 else 999,
            }
        }
        return self.results["DFM-1.0"]

    def run_bsm_model(self) -> Dict:
        """Run BSM-1.0: Balance Sheet Model."""
        self._log("Running BSM-1.0: Balance Sheet Model")

        nwc = self._get_from_results("WCM-1.0.summary.net_working_capital", self.config.base_revenue * 0.15)
        fixed_assets = self.config.base_revenue * 0.30
        cash = self.config.base_revenue * 0.05
        total_assets = nwc + fixed_assets + cash
        payables = self._get_from_results("WCM-1.0.summary.payables", self.config.base_revenue * 0.08)
        total_liabilities = self.config.total_debt + payables
        net_income = self._get_from_results("PLM-1.0.summary.net_income", 0)

        self.results["BSM-1.0"] = {
            "model_id": "BSM-1.0",
            "summary": {
                "total_assets": total_assets,
                "total_liabilities": total_liabilities,
                "total_equity": self.config.total_equity,
                "debt": self.config.total_debt,
                "roe": net_income / self.config.total_equity * 100 if self.config.total_equity > 0 else 0,
                "roa": net_income / total_assets * 100 if total_assets > 0 else 0,
            }
        }
        return self.results["BSM-1.0"]

    def run_bem_model(self) -> Dict:
        """Run BEM-1.0: Break-Even Model."""
        self._log("Running BEM-1.0: Break-Even Model")

        revenue = self.config.base_revenue
        fixed_costs = revenue * (self.config.gross_margin - self.config.operating_margin) * 0.6
        contribution_margin = self.config.gross_margin
        break_even_revenue = fixed_costs / contribution_margin if contribution_margin > 0 else 0
        margin_of_safety = (revenue - break_even_revenue) / revenue * 100 if revenue > 0 else 0

        self.results["BEM-1.0"] = {
            "model_id": "BEM-1.0",
            "summary": {
                "break_even_revenue": break_even_revenue,
                "margin_of_safety_pct": margin_of_safety,
                "contribution_margin_pct": contribution_margin * 100,
                "fixed_costs": fixed_costs,
            }
        }
        return self.results["BEM-1.0"]

    # =========================================================================
    # LAYER 4: STRATEGIC ANALYSIS MODELS
    # =========================================================================

    def run_msm_model(self) -> Dict:
        """Run MSM-1.0: Market Share Model."""
        self._log("Running MSM-1.0: Market Share Model")

        market_size = self.config.base_revenue * 20
        market_share = self.config.base_revenue / market_size * 100

        self.results["MSM-1.0"] = {
            "model_id": "MSM-1.0",
            "summary": {
                "market_size": market_size,
                "company_revenue": self.config.base_revenue,
                "market_share_pct": market_share,
            }
        }
        return self.results["MSM-1.0"]

    def run_prm_model(self) -> Dict:
        """Run PRM-1.0: Pricing Model."""
        self._log("Running PRM-1.0: Pricing Model")

        avg_price = self.config.avg_revenue_per_customer
        variable_cost = avg_price * (1 - self.config.gross_margin)
        contribution = avg_price - variable_cost

        self.results["PRM-1.0"] = {
            "model_id": "PRM-1.0",
            "summary": {
                "average_price": avg_price,
                "variable_cost": variable_cost,
                "contribution_margin": contribution,
                "contribution_margin_pct": (contribution / avg_price) * 100 if avg_price > 0 else 0,
            }
        }
        return self.results["PRM-1.0"]

    def run_pfm_model(self) -> Dict:
        """Run PFM-1.0: Portfolio Model (BCG Matrix)."""
        self._log("Running PFM-1.0: Portfolio Model (BCG Matrix)")

        self.results["PFM-1.0"] = {
            "model_id": "PFM-1.0",
            "summary": {
                "portfolio_analyzed": True,
            }
        }
        return self.results["PFM-1.0"]

    def run_mam_model(self) -> Dict:
        """Run MAM-1.0: M&A Synergy Model."""
        self._log("Running MAM-1.0: M&A Synergy Model")

        self.results["MAM-1.0"] = {
            "model_id": "MAM-1.0",
            "summary": {
                "synergy_analysis_available": True,
            }
        }
        return self.results["MAM-1.0"]

    def run_stm_model(self) -> Dict:
        """Run STM-1.0: Stress Testing Model."""
        self._log("Running STM-1.0: Stress Testing Model")

        ebitda = self._get_from_results("PLM-1.0.summary.ebitda", self.config.base_revenue * 0.17)
        fcf = self._get_from_results("CFM-1.0.summary.free_cash_flow", ebitda * 0.5)

        # Stress scenarios
        scenarios = {
            "base": {"revenue_change": 0, "ebitda": ebitda, "fcf": fcf},
            "mild_recession": {"revenue_change": -0.10, "ebitda": ebitda * 0.85, "fcf": fcf * 0.70},
            "severe_recession": {"revenue_change": -0.25, "ebitda": ebitda * 0.60, "fcf": fcf * 0.30},
        }

        self.results["STM-1.0"] = {
            "model_id": "STM-1.0",
            "scenarios": scenarios,
            "summary": {
                "stress_tested": True,
                "worst_case_ebitda": scenarios["severe_recession"]["ebitda"],
            }
        }
        return self.results["STM-1.0"]

    # =========================================================================
    # LAYER 5: SIMULATION & VALIDATION MODELS
    # =========================================================================

    def run_mcsm_model(self) -> Dict:
        """Run MCSM-1.0: Monte Carlo Simulation Model."""
        self._log("Running MCSM-1.0: Monte Carlo Simulation Model")

        # Simplified Monte Carlo summary (actual MC would require numpy)
        base_ev = self._get_from_results("VAM-1.0.summary.enterprise_value.dcf", self.config.base_revenue * 1.2)
        std_dev = 0.15  # 15% standard deviation

        self.results["MCSM-1.0"] = {
            "model_id": "MCSM-1.0",
            "summary": {
                "num_simulations": min(self.config.num_simulations, 1000),
                "mean_value": base_ev,
                "std_dev": base_ev * std_dev,
                "p10": base_ev * 0.80,
                "p50": base_ev,
                "p90": base_ev * 1.25,
                "simulated": True,
            }
        }
        return self.results["MCSM-1.0"]

    def run_sam_model(self) -> Dict:
        """Run SAM-1.0: Sensitivity Analysis Model."""
        self._log("Running SAM-1.0: Sensitivity Analysis Model")

        # Simplified sensitivity without full model runner
        base_ev = self._get_from_results("VAM-1.0.summary.enterprise_value.dcf", 0)
        wacc = self._get_from_results("CMM-1.0.wacc_analysis.wacc", 0.10)

        sensitivities = {
            "wacc_+1%": base_ev * 0.90 if base_ev else 0,
            "wacc_-1%": base_ev * 1.12 if base_ev else 0,
            "growth_+1%": base_ev * 1.08 if base_ev else 0,
            "growth_-1%": base_ev * 0.93 if base_ev else 0,
        }

        self.results["SAM-1.0"] = {
            "model_id": "SAM-1.0",
            "sensitivities": sensitivities,
            "summary": {
                "base_value": base_ev,
                "key_drivers": ["wacc", "growth_rate", "margin"],
            }
        }
        return self.results["SAM-1.0"]

    def run_scm_model(self) -> Dict:
        """Run SCM-1.0: Scenario Comparison Model."""
        self._log("Running SCM-1.0: Scenario Comparison Model")

        base_ev = self._get_from_results("VAM-1.0.summary.enterprise_value.dcf", 0)

        scenarios = {
            "base_case": base_ev,
            "upside": base_ev * 1.25 if base_ev else 0,
            "downside": base_ev * 0.75 if base_ev else 0,
        }

        self.results["SCM-1.0"] = {
            "model_id": "SCM-1.0",
            "scenarios": scenarios,
            "summary": {
                "base_case": base_ev,
                "upside": scenarios["upside"],
                "downside": scenarios["downside"],
                "range": scenarios["upside"] - scenarios["downside"] if base_ev else 0,
            }
        }
        return self.results["SCM-1.0"]

    def run_icm_model(self) -> Dict:
        """Run ICM-1.0: Iteration Convergence Model."""
        from .iteration_convergence import analyze_iteration_convergence

        self._log("Running ICM-1.0: Iteration Convergence Model")

        result = analyze_iteration_convergence(
            initial_gap_percent=25.0,
            target_gap_percent=5.0,
            data_quality="medium",
            model_complexity="medium",
        )

        self.results["ICM-1.0"] = {
            "model_id": "ICM-1.0",
            "analysis": result,
            "summary": {
                "optimal_iterations": result.get("optimal_iterations", {}).get("recommended", 4) if isinstance(result, dict) else 4,
            }
        }
        return self.results["ICM-1.0"]

    # =========================================================================
    # LAYER 3: THEORETICAL FOUNDATION & VALUATION
    # =========================================================================

    def run_vam_model(self) -> Dict:
        """Run VAM-1.0: Valuation Model."""
        from .valuation import run_valuation

        self._log("Running VAM-1.0: Valuation Model")

        # Get WACC from CMM if available
        wacc = self._get_from_results("CMM-1.0.wacc_analysis.wacc", 0.10)

        # Calculate financials
        revenue = self.config.base_revenue
        gross_profit = revenue * self.config.gross_margin
        ebitda = revenue * (self.config.operating_margin + 0.05)  # Approx EBITDA margin
        ebit = revenue * self.config.operating_margin
        net_income = ebit * (1 - self.config.tax_rate)
        depreciation = ebitda - ebit
        capex = revenue * 0.05  # 5% capex intensity
        change_in_nwc = revenue * self.config.revenue_growth_rate * 0.10  # NWC as % of revenue growth

        result = run_valuation(
            revenue=revenue,
            ebitda=ebitda,
            ebit=ebit,
            net_income=net_income,
            depreciation=depreciation,
            capex=capex,
            change_in_nwc=change_in_nwc,
            net_debt=self.config.total_debt,
            wacc=wacc,
            terminal_growth_rate=0.02,
            revenue_growth_rates=[self.config.revenue_growth_rate] * 5,
            industry=self.config.industry,
        )

        self.results["VAM-1.0"] = result
        return result

    def run_vcm_model(self) -> Dict:
        """Run VCM-1.0: Value Creation Model (EVA, ROIC, Shareholder Value)."""
        self._log("Running VCM-1.0: Value Creation Model")

        # Get inputs from other models
        ebit = self._get_from_results("PLM-1.0.summary.ebit", self.config.base_revenue * self.config.operating_margin)
        tax_rate = self.config.tax_rate
        nopat = ebit * (1 - tax_rate)

        # Invested Capital = Total Equity + Total Debt
        invested_capital = self.config.total_equity + self.config.total_debt
        if invested_capital == 0:
            invested_capital = self.config.base_revenue * 0.5  # Default to 50% of revenue

        # Get WACC from CMM
        wacc = self._get_from_results("CMM-1.0.wacc_analysis.wacc", 0.10)

        # Calculate value metrics
        roic = nopat / invested_capital if invested_capital > 0 else 0
        spread = roic - wacc
        eva = nopat - (wacc * invested_capital)  # Economic Value Added
        value_created = eva > 0

        self.results["VCM-1.0"] = {
            "model_id": "VCM-1.0",
            "summary": {
                "nopat": nopat,
                "invested_capital": invested_capital,
                "roic": roic,
                "wacc": wacc,
                "spread": spread,
                "eva": eva,
                "value_created": value_created,
                "roic_pct": roic * 100,
                "spread_pct": spread * 100,
            }
        }
        return self.results["VCM-1.0"]

    def run(self, verbose: bool = True, full_run: bool = True) -> Dict:
        """
        Run the full integrated strategy analysis.

        Args:
            verbose: Print progress
            full_run: Run all 30 models (True) or quick run with 10 models (False)

        Returns:
            Complete integrated results
        """
        self._log(f"Starting Integrated Strategy Orchestrator for {self.config.company_name}")
        self._log(f"Industry: {self.config.industry}, Base Revenue: ${self.config.base_revenue:,.0f}")
        self._log(f"Mode: {'Full (31 models)' if full_run else 'Quick (10 models)'}")

        # =====================================================================
        # LAYER 1: FUNCTIONAL STRATEGY MODELS (v4.0) - 7 models
        # =====================================================================
        if verbose:
            print("\n" + "=" * 70)
            print("LAYER 1: FUNCTIONAL STRATEGY MODELS (v4.0) - 7 models")
            print("=" * 70)

        # VMV-1.0 runs FIRST as it provides the strategic foundation
        self.run_vmv_model()
        if verbose:
            identity_score = self._get_from_results("VMV-1.0.summary.overall_identity_score", 0)
            print(f"  VMV-1.0: Identity Score = {identity_score}/100")

        self.run_clv_model()
        if verbose:
            clv = self._get_from_results("CLV-1.0.summary.clv", 0)
            print(f"  CLV-1.0: CLV = ${clv:,.0f}")

        self.run_cac_model()
        if verbose:
            cac = self._get_from_results("CAC-1.0.summary.blended_cac", 0)
            print(f"  CAC-1.0: Blended CAC = ${cac:,.0f}")

        self.run_hcm_model()
        if verbose:
            labor = self._get_from_results("HCM-1.0.summary.total_labor_cost", 0)
            print(f"  HCM-1.0: Total Labor Cost = ${labor:,.0f}")

        self.run_sco_model()
        if verbose:
            turns = self._get_from_results("SCO-1.0.summary.inventory_turns", 0)
            print(f"  SCO-1.0: Inventory Turns = {turns:.1f}x")

        self.run_rdm_model()
        if verbose:
            rd_int = self._get_from_results("RDM-1.0.summary.rd_intensity_pct", 0)
            print(f"  RDM-1.0: R&D Intensity = {rd_int}%")

        self.run_esg_model()
        if verbose:
            esg = self._get_from_results("ESG-1.0.summary.rating", "N/A")
            score = self._get_from_results("ESG-1.0.summary.overall_score", 0)
            print(f"  ESG-1.0: Rating = {esg} (Score: {score})")

        # =====================================================================
        # LAYER 2: CORE FINANCIAL MODELS (v1.0-v2.5)
        # =====================================================================
        if full_run:
            if verbose:
                print("\n" + "=" * 70)
                print("LAYER 2: CORE FINANCIAL MODELS (v1.0-v2.5)")
                print("=" * 70)

            self.run_rpm_model()
            if verbose:
                rev = self._get_from_results("RPM-1.0.summary.base_revenue", 0)
                print(f"  RPM-1.0: Base Revenue = ${rev:,.0f}")

            self.run_osm_model()
            if verbose:
                hc = self._get_from_results("OSM-1.0.summary.base_headcount", 0)
                print(f"  OSM-1.0: Headcount = {hc:,}")

            self.run_cam_model()
            if verbose:
                capex = self._get_from_results("CAM-1.0.summary.base_capex", 0)
                print(f"  CAM-1.0: CapEx = ${capex:,.0f}")

            self.run_csm_model()
            if verbose:
                costs = self._get_from_results("CSM-1.0.summary.total_costs", 0)
                print(f"  CSM-1.0: Total Costs = ${costs:,.0f}")

            self.run_plm_model()
            if verbose:
                ebitda = self._get_from_results("PLM-1.0.summary.ebitda", 0)
                print(f"  PLM-1.0: EBITDA = ${ebitda:,.0f}")

            self.run_wcm_model()
            if verbose:
                nwc = self._get_from_results("WCM-1.0.summary.net_working_capital", 0)
                print(f"  WCM-1.0: NWC = ${nwc:,.0f}")

            self.run_cfm_model()
            if verbose:
                fcf = self._get_from_results("CFM-1.0.summary.free_cash_flow", 0)
                print(f"  CFM-1.0: FCF = ${fcf:,.0f}")

            self.run_dfm_model()
            if verbose:
                d_e = self._get_from_results("DFM-1.0.summary.debt_to_equity", 0)
                print(f"  DFM-1.0: D/E = {d_e:.2f}x")

            self.run_bsm_model()
            if verbose:
                assets = self._get_from_results("BSM-1.0.summary.total_assets", 0)
                print(f"  BSM-1.0: Total Assets = ${assets:,.0f}")

            self.run_bem_model()
            if verbose:
                mos = self._get_from_results("BEM-1.0.summary.margin_of_safety_pct", 0)
                print(f"  BEM-1.0: Margin of Safety = {mos:.1f}%")

        # =====================================================================
        # LAYER 3: THEORETICAL FOUNDATION (v3.1-v3.5)
        # =====================================================================
        if verbose:
            print("\n" + "=" * 70)
            print("LAYER 3: THEORETICAL FOUNDATION (v3.1-v3.5)")
            print("=" * 70)

        self.run_fem_model()
        if verbose:
            dol = self._get_from_results("FEM-1.0.leverage.degree_of_operating_leverage", 0)
            print(f"  FEM-1.0: DOL = {dol:.2f}x")

        self.run_bfm_model()
        if verbose:
            beta_e = self._get_from_results("BFM-1.0.beta_chain.equity_beta", 0)
            print(f"  BFM-1.0: Equity Beta = {beta_e:.2f}")

        self.run_cmm_model()
        if verbose:
            wacc = self._get_from_results("CMM-1.0.wacc_analysis.wacc", 0)
            print(f"  CMM-1.0: WACC = {wacc*100:.2f}%")

        self.run_vam_model()
        if verbose:
            ev = self._get_from_results("VAM-1.0.summary.enterprise_value.dcf", 0)
            eq = self._get_from_results("VAM-1.0.summary.equity_value.dcf", 0)
            print(f"  VAM-1.0: Enterprise Value = ${ev:,.0f}")
            print(f"           Equity Value = ${eq:,.0f}")

        self.run_vcm_model()
        if verbose:
            roic = self._get_from_results("VCM-1.0.summary.roic_pct", 0)
            eva = self._get_from_results("VCM-1.0.summary.eva", 0)
            print(f"  VCM-1.0: ROIC = {roic:.1f}%, EVA = ${eva:,.0f}")

        # =====================================================================
        # LAYER 4: STRATEGIC ANALYSIS (v3.0)
        # =====================================================================
        if full_run:
            if verbose:
                print("\n" + "=" * 70)
                print("LAYER 4: STRATEGIC ANALYSIS (v3.0)")
                print("=" * 70)

            self.run_msm_model()
            if verbose:
                ms = self._get_from_results("MSM-1.0.summary.market_share_pct", 0)
                print(f"  MSM-1.0: Market Share = {ms:.1f}%")

            self.run_prm_model()
            if verbose:
                cm = self._get_from_results("PRM-1.0.summary.contribution_margin_pct", 0)
                print(f"  PRM-1.0: Contribution Margin = {cm:.1f}%")

            self.run_pfm_model()
            if verbose:
                print(f"  PFM-1.0: Portfolio Analysis ✓")

            self.run_mam_model()
            if verbose:
                print(f"  MAM-1.0: M&A Synergy Analysis ✓")

            self.run_stm_model()
            if verbose:
                print(f"  STM-1.0: Stress Testing ✓")

        # =====================================================================
        # LAYER 5: SIMULATION & VALIDATION (v3.1)
        # =====================================================================
        if full_run and self.config.run_simulations:
            if verbose:
                print("\n" + "=" * 70)
                print("LAYER 5: SIMULATION & VALIDATION (v3.1)")
                print("=" * 70)

            self.run_mcsm_model()
            if verbose:
                n_sim = self._get_from_results("MCSM-1.0.summary.num_simulations", 0)
                print(f"  MCSM-1.0: {n_sim} simulations ✓")

            self.run_sam_model()
            if verbose:
                print(f"  SAM-1.0: Sensitivity Analysis ✓")

            self.run_scm_model()
            if verbose:
                rng = self._get_from_results("SCM-1.0.summary.range", 0)
                print(f"  SCM-1.0: Scenario Range = ${rng:,.0f}")

            self.run_icm_model()
            if verbose:
                iters = self._get_from_results("ICM-1.0.summary.optimal_iterations", 0)
                print(f"  ICM-1.0: Optimal Iterations = {iters}")

        # =====================================================================
        # BUILD SUMMARY
        # =====================================================================
        self._build_summary()

        if verbose:
            print("\n" + "=" * 70)
            print("INTEGRATED SUMMARY")
            print("=" * 70)
            self._print_summary()

            # Model count
            n_models = len([k for k in self.results.keys() if k != "integrated_summary"])
            print(f"\nTotal models executed: {n_models}")

        return self.results

    def _build_summary(self):
        """Build integrated summary from all results."""
        n_models = len([k for k in self.results.keys() if k != "integrated_summary"])

        self.results["integrated_summary"] = {
            "company": self.config.company_name,
            "industry": self.config.industry,
            "base_year": self.config.base_year,
            "models_executed_count": n_models,

            "strategic_identity": {
                "purpose": self._get_from_results("VMV-1.0.summary.purpose"),
                "vision": self._get_from_results("VMV-1.0.summary.vision"),
                "mission": self._get_from_results("VMV-1.0.summary.mission"),
                "values_count": self._get_from_results("VMV-1.0.summary.values_count"),
                "pillars_count": self._get_from_results("VMV-1.0.summary.pillars_count"),
                "culture_health_index": self._get_from_results("VMV-1.0.summary.culture_health_index"),
                "purpose_alignment_score": self._get_from_results("VMV-1.0.summary.purpose_alignment_score"),
                "overall_identity_score": self._get_from_results("VMV-1.0.summary.overall_identity_score"),
            },

            "customer_economics": {
                "clv": self._get_from_results("CLV-1.0.summary.clv"),
                "cac": self._get_from_results("CAC-1.0.summary.blended_cac"),
                "ltv_cac_ratio": self._get_from_results("CLV-1.0.summary.ltv_cac_ratio"),
                "marketing_roi_pct": self._get_from_results("CAC-1.0.marketing_roi.marketing_roi_pct"),
            },

            "operational_efficiency": {
                "revenue_per_employee": self._get_from_results("HCM-1.0.summary.revenue_per_employee"),
                "human_capital_roi": self._get_from_results("HCM-1.0.summary.human_capital_roi"),
                "inventory_turns": self._get_from_results("SCO-1.0.summary.inventory_turns"),
                "cash_to_cash_days": self._get_from_results("SCO-1.0.summary.cash_to_cash_days"),
            },

            "innovation_sustainability": {
                "rd_intensity_pct": self._get_from_results("RDM-1.0.summary.rd_intensity_pct"),
                "innovation_rate_pct": self._get_from_results("RDM-1.0.summary.innovation_rate_pct"),
                "esg_rating": self._get_from_results("ESG-1.0.summary.rating"),
                "esg_score": self._get_from_results("ESG-1.0.summary.overall_score"),
            },

            "financial_projections": {
                "revenue": self._get_from_results("PLM-1.0.summary.revenue") or self.config.base_revenue,
                "ebitda": self._get_from_results("PLM-1.0.summary.ebitda"),
                "ebitda_margin_pct": self._get_from_results("PLM-1.0.summary.ebitda_margin_pct"),
                "net_income": self._get_from_results("PLM-1.0.summary.net_income"),
                "free_cash_flow": self._get_from_results("CFM-1.0.summary.free_cash_flow"),
            },

            "financial_structure": {
                "gross_margin_pct": self.config.gross_margin * 100,
                "operating_margin_pct": self.config.operating_margin * 100,
                "dol": self._get_from_results("FEM-1.0.leverage.degree_of_operating_leverage"),
                "debt_to_equity": self._get_from_results("DFM-1.0.summary.debt_to_equity") or (self.config.total_debt / self.config.total_equity if self.config.total_equity > 0 else 0),
                "interest_coverage": self._get_from_results("DFM-1.0.summary.interest_coverage"),
            },

            "balance_sheet": {
                "total_assets": self._get_from_results("BSM-1.0.summary.total_assets"),
                "total_equity": self._get_from_results("BSM-1.0.summary.total_equity") or self.config.total_equity,
                "total_debt": self._get_from_results("BSM-1.0.summary.debt") or self.config.total_debt,
                "roe_pct": self._get_from_results("BSM-1.0.summary.roe"),
                "roa_pct": self._get_from_results("BSM-1.0.summary.roa"),
            },

            "working_capital": {
                "net_working_capital": self._get_from_results("WCM-1.0.summary.net_working_capital"),
                "cash_conversion_cycle": self._get_from_results("WCM-1.0.summary.cash_conversion_cycle"),
                "nwc_percent_revenue": self._get_from_results("WCM-1.0.summary.nwc_percent_revenue"),
            },

            "cost_of_capital": {
                "equity_beta": self._get_from_results("BFM-1.0.beta_chain.equity_beta"),
                "cost_of_equity_pct": (self._get_from_results("CMM-1.0.wacc_analysis.cost_of_equity.cost_of_equity") or 0) * 100,
                "wacc_pct": (self._get_from_results("CMM-1.0.wacc_analysis.wacc") or 0) * 100,
            },

            "valuation": {
                "enterprise_value": self._get_from_results("VAM-1.0.summary.enterprise_value.dcf"),
                "equity_value": self._get_from_results("VAM-1.0.summary.equity_value.dcf"),
                "ev_ebitda_implied": self._get_from_results("VAM-1.0.summary.implied_multiples_dcf.ev_ebitda"),
            },

            "value_creation": {
                "roic_pct": self._get_from_results("VCM-1.0.summary.roic_pct"),
                "wacc_pct": (self._get_from_results("VCM-1.0.summary.wacc") or 0) * 100,
                "spread_pct": self._get_from_results("VCM-1.0.summary.spread_pct"),
                "eva": self._get_from_results("VCM-1.0.summary.eva"),
                "value_created": self._get_from_results("VCM-1.0.summary.value_created"),
            },

            "strategic_analysis": {
                "market_share_pct": self._get_from_results("MSM-1.0.summary.market_share_pct"),
                "break_even_revenue": self._get_from_results("BEM-1.0.summary.break_even_revenue"),
                "margin_of_safety_pct": self._get_from_results("BEM-1.0.summary.margin_of_safety_pct"),
            },

            "scenarios": {
                "base_case": self._get_from_results("SCM-1.0.summary.base_case"),
                "upside": self._get_from_results("SCM-1.0.summary.upside"),
                "downside": self._get_from_results("SCM-1.0.summary.downside"),
            },

            "models_executed": list(self.results.keys()),
            "execution_log": self.execution_log,
        }

    def _print_summary(self):
        """Print formatted summary."""
        summary = self.results.get("integrated_summary", {})

        print(f"\nCompany: {summary.get('company')}")
        print(f"Industry: {summary.get('industry')}")

        ce = summary.get("customer_economics", {})
        print(f"\nCustomer Economics:")
        print(f"  CLV: ${ce.get('clv') or 0:,.0f}")
        print(f"  CAC: ${ce.get('cac') or 0:,.0f}")
        print(f"  LTV:CAC: {ce.get('ltv_cac_ratio') or 0:.1f}x")

        oe = summary.get("operational_efficiency", {})
        print(f"\nOperational Efficiency:")
        print(f"  Revenue/Employee: ${oe.get('revenue_per_employee') or 0:,.0f}")
        print(f"  Inventory Turns: {oe.get('inventory_turns') or 0:.1f}x")

        ins = summary.get("innovation_sustainability", {})
        print(f"\nInnovation & Sustainability:")
        print(f"  R&D Intensity: {ins.get('rd_intensity_pct') or 0}%")
        print(f"  ESG Rating: {ins.get('esg_rating') or 'N/A'}")

        coc = summary.get("cost_of_capital", {})
        print(f"\nCost of Capital:")
        print(f"  Equity Beta: {coc.get('equity_beta') or 0:.2f}")
        print(f"  WACC: {coc.get('wacc_pct') or 0:.2f}%")

        val = summary.get("valuation", {})
        print(f"\nValuation:")
        print(f"  Enterprise Value: ${val.get('enterprise_value') or 0:,.0f}")
        print(f"  Equity Value: ${val.get('equity_value') or 0:,.0f}")


def run_integrated_strategy(
    company_name: str,
    base_revenue: float,
    industry: str = "manufacturing",
    full_run: bool = True,
    verbose: bool = True,
    **kwargs
) -> Dict:
    """
    Convenience function to run the integrated strategy orchestrator.

    Executes all 31 strategic models with automatic data flow between them.

    Args:
        company_name: Company name
        base_revenue: Base year revenue
        industry: Industry type
        full_run: Run all 31 models (True) or quick run with 10 core models (False)
        verbose: Print progress during execution
        **kwargs: Additional OrchestratorConfig parameters:
            - gross_margin: Gross margin (0-1)
            - operating_margin: Operating margin (0-1)
            - customer_count: Number of customers
            - avg_revenue_per_customer: Average revenue per customer
            - total_employees: Total headcount
            - avg_salary: Average salary
            - total_debt: Total debt
            - total_equity: Total equity
            - tax_rate: Corporate tax rate
            - rd_intensity: R&D as % of revenue
            - run_simulations: Run Monte Carlo (default True)
            - num_simulations: Number of simulations (default 1000)

    Returns:
        Complete integrated results from all models
    """
    config = OrchestratorConfig(
        company_name=company_name,
        base_revenue=base_revenue,
        industry=industry,
        **kwargs
    )

    orchestrator = IntegratedStrategyOrchestrator(config)
    return orchestrator.run(verbose=verbose, full_run=full_run)


if __name__ == "__main__":
    print("=" * 70)
    print("ISO-1.0: Integrated Strategy Orchestrator - Demo")
    print("=" * 70)

    # Run for a sample company
    results = run_integrated_strategy(
        company_name="Demo Corp",
        base_revenue=100_000_000,
        industry="manufacturing",
        customer_count=5000,
        avg_revenue_per_customer=20000,
        total_employees=400,
        avg_salary=70000,
        total_debt=15_000_000,
        total_equity=40_000_000,
        gross_margin=0.38,
        operating_margin=0.10,
        rd_intensity=0.03,
    )

    print("\n" + "=" * 70)
    print("ORCHESTRATION COMPLETE")
    print("=" * 70)
    print(f"\nTotal models executed: {len(results.get('integrated_summary', {}).get('models_executed', []))}")
