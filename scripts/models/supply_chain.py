"""
SCO-1.0: Supply Chain Optimization Model

A comprehensive model for analyzing and optimizing supply chain operations,
including inventory management, supplier performance, and cost optimization.

Key Formulas:
- EOQ = √(2×D×S / H)  (Economic Order Quantity)
- Safety Stock = z × σ_d × √L  (Service level based)
- Inventory Turns = COGS / Avg Inventory
- Perfect Order Rate = (On-time × In-full × Damage-free × Correct docs) / Total Orders
- Total Cost of Ownership = Purchase Price + Ordering + Holding + Shortage + Quality

Dimensions:
- Inventory management (EOQ, reorder point, safety stock)
- Supplier performance (lead time, quality, reliability)
- Cost analysis (procurement, holding, shortage)
- Efficiency metrics (turns, fill rate, cycle time)

Version: 1.0.0
Date: 2026-01-16
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import math


@dataclass
class InventoryItem:
    """Represents an inventory item/SKU."""
    sku: str
    name: str
    annual_demand: float  # Units per year
    unit_cost: float  # Purchase price per unit
    ordering_cost: float  # Cost per order (fixed)
    holding_cost_rate: float = 0.25  # As % of unit cost per year
    lead_time_days: float = 14  # Average lead time
    lead_time_std_days: float = 3  # Lead time standard deviation
    demand_std_daily: float = 0  # Daily demand standard deviation
    current_inventory: float = 0
    service_level: float = 0.95  # Target service level


@dataclass
class Supplier:
    """Represents a supplier."""
    name: str
    items_supplied: List[str]  # SKU list
    lead_time_days: float
    lead_time_reliability: float = 0.90  # On-time delivery rate
    quality_rate: float = 0.98  # % of items without defects
    price_competitiveness: float = 1.0  # 1.0 = market average
    payment_terms_days: int = 30
    min_order_value: float = 0
    volume_discount_threshold: float = 0  # Order value for discount
    volume_discount_rate: float = 0  # Discount rate


# Industry benchmarks for supply chain metrics
SUPPLY_CHAIN_BENCHMARKS = {
    "manufacturing": {
        "inventory_turns": 8,
        "fill_rate": 0.95,
        "perfect_order_rate": 0.90,
        "on_time_delivery": 0.92,
        "days_inventory": 45,
        "cash_to_cash_days": 60,
    },
    "retail": {
        "inventory_turns": 12,
        "fill_rate": 0.97,
        "perfect_order_rate": 0.93,
        "on_time_delivery": 0.95,
        "days_inventory": 30,
        "cash_to_cash_days": 45,
    },
    "distribution": {
        "inventory_turns": 15,
        "fill_rate": 0.98,
        "perfect_order_rate": 0.95,
        "on_time_delivery": 0.97,
        "days_inventory": 24,
        "cash_to_cash_days": 35,
    },
    "high_tech": {
        "inventory_turns": 6,
        "fill_rate": 0.92,
        "perfect_order_rate": 0.88,
        "on_time_delivery": 0.90,
        "days_inventory": 60,
        "cash_to_cash_days": 75,
    },
    "consumer_goods": {
        "inventory_turns": 10,
        "fill_rate": 0.96,
        "perfect_order_rate": 0.92,
        "on_time_delivery": 0.94,
        "days_inventory": 36,
        "cash_to_cash_days": 50,
    },
}

# Z-scores for service levels
SERVICE_LEVEL_Z = {
    0.90: 1.28,
    0.95: 1.65,
    0.97: 1.88,
    0.98: 2.05,
    0.99: 2.33,
    0.995: 2.58,
    0.999: 3.09,
}


def get_z_score(service_level: float) -> float:
    """Get z-score for a given service level."""
    # Find closest service level
    levels = sorted(SERVICE_LEVEL_Z.keys())
    for i, level in enumerate(levels):
        if service_level <= level:
            return SERVICE_LEVEL_Z[level]
    return SERVICE_LEVEL_Z[levels[-1]]


def calculate_eoq(
    annual_demand: float,
    ordering_cost: float,
    unit_cost: float,
    holding_cost_rate: float,
) -> dict:
    """
    Calculate Economic Order Quantity (EOQ).

    EOQ = √(2 × D × S / H)

    Where:
    - D = Annual demand
    - S = Ordering cost per order
    - H = Holding cost per unit per year

    Args:
        annual_demand: Annual demand in units
        ordering_cost: Fixed cost per order
        unit_cost: Cost per unit
        holding_cost_rate: Holding cost as % of unit cost

    Returns:
        Dictionary with EOQ analysis
    """
    D = annual_demand
    S = ordering_cost
    H = unit_cost * holding_cost_rate

    # EOQ formula
    if H > 0 and D > 0:
        eoq = math.sqrt(2 * D * S / H)
    else:
        eoq = 0

    # Number of orders per year
    orders_per_year = D / eoq if eoq > 0 else 0

    # Total annual costs at EOQ
    ordering_cost_annual = orders_per_year * S
    holding_cost_annual = (eoq / 2) * H  # Average inventory × holding cost
    total_cost = ordering_cost_annual + holding_cost_annual

    # Time between orders (days)
    order_cycle_days = 365 / orders_per_year if orders_per_year > 0 else 0

    return {
        "eoq_units": round(eoq, 0),
        "orders_per_year": round(orders_per_year, 1),
        "order_cycle_days": round(order_cycle_days, 1),
        "costs": {
            "annual_ordering_cost": round(ordering_cost_annual, 2),
            "annual_holding_cost": round(holding_cost_annual, 2),
            "total_annual_cost": round(total_cost, 2),
            "cost_per_unit": round(total_cost / D, 4) if D > 0 else 0,
        },
        "parameters": {
            "annual_demand": annual_demand,
            "ordering_cost": ordering_cost,
            "unit_cost": unit_cost,
            "holding_cost_rate": holding_cost_rate,
        },
    }


def calculate_safety_stock(
    service_level: float,
    lead_time_days: float,
    demand_std_daily: float,
    lead_time_std_days: float = 0,
    avg_daily_demand: float = 0,
) -> dict:
    """
    Calculate safety stock for a given service level.

    Safety Stock = z × √(L × σ_d² + d² × σ_L²)

    Where:
    - z = z-score for service level
    - L = Lead time
    - σ_d = Demand standard deviation
    - d = Average daily demand
    - σ_L = Lead time standard deviation

    Args:
        service_level: Target service level (e.g., 0.95)
        lead_time_days: Average lead time in days
        demand_std_daily: Daily demand standard deviation
        lead_time_std_days: Lead time standard deviation (optional)
        avg_daily_demand: Average daily demand (for lead time variability)

    Returns:
        Dictionary with safety stock calculation
    """
    z = get_z_score(service_level)

    # Combined uncertainty
    demand_variance = lead_time_days * (demand_std_daily ** 2)
    lead_time_variance = (avg_daily_demand ** 2) * (lead_time_std_days ** 2) if lead_time_std_days > 0 else 0
    combined_std = math.sqrt(demand_variance + lead_time_variance)

    safety_stock = z * combined_std

    return {
        "safety_stock_units": round(safety_stock, 0),
        "service_level": service_level,
        "z_score": round(z, 2),
        "demand_uncertainty": round(math.sqrt(demand_variance), 2),
        "lead_time_uncertainty": round(math.sqrt(lead_time_variance), 2),
        "combined_uncertainty": round(combined_std, 2),
    }


def calculate_reorder_point(
    avg_daily_demand: float,
    lead_time_days: float,
    safety_stock: float,
) -> dict:
    """
    Calculate reorder point.

    ROP = (d × L) + SS

    Where:
    - d = Average daily demand
    - L = Lead time in days
    - SS = Safety stock

    Args:
        avg_daily_demand: Average daily demand
        lead_time_days: Lead time in days
        safety_stock: Safety stock units

    Returns:
        Reorder point calculation
    """
    demand_during_lead_time = avg_daily_demand * lead_time_days
    reorder_point = demand_during_lead_time + safety_stock

    return {
        "reorder_point_units": round(reorder_point, 0),
        "demand_during_lead_time": round(demand_during_lead_time, 0),
        "safety_stock": round(safety_stock, 0),
        "avg_daily_demand": avg_daily_demand,
        "lead_time_days": lead_time_days,
    }


def analyze_inventory_item(item: InventoryItem) -> dict:
    """
    Comprehensive inventory analysis for a single item.

    Args:
        item: InventoryItem to analyze

    Returns:
        Complete inventory analysis
    """
    avg_daily_demand = item.annual_demand / 365

    # EOQ calculation
    eoq = calculate_eoq(
        annual_demand=item.annual_demand,
        ordering_cost=item.ordering_cost,
        unit_cost=item.unit_cost,
        holding_cost_rate=item.holding_cost_rate,
    )

    # Safety stock calculation
    safety = calculate_safety_stock(
        service_level=item.service_level,
        lead_time_days=item.lead_time_days,
        demand_std_daily=item.demand_std_daily if item.demand_std_daily > 0 else avg_daily_demand * 0.2,
        lead_time_std_days=item.lead_time_std_days,
        avg_daily_demand=avg_daily_demand,
    )

    # Reorder point
    rop = calculate_reorder_point(
        avg_daily_demand=avg_daily_demand,
        lead_time_days=item.lead_time_days,
        safety_stock=safety["safety_stock_units"],
    )

    # Inventory levels
    avg_inventory = (eoq["eoq_units"] / 2) + safety["safety_stock_units"]
    max_inventory = eoq["eoq_units"] + safety["safety_stock_units"]

    # Inventory value
    avg_inventory_value = avg_inventory * item.unit_cost
    annual_holding_cost = avg_inventory_value * item.holding_cost_rate

    # Inventory turns
    cogs = item.annual_demand * item.unit_cost
    inventory_turns = cogs / avg_inventory_value if avg_inventory_value > 0 else 0

    # Days of inventory
    days_inventory = 365 / inventory_turns if inventory_turns > 0 else 0

    return {
        "sku": item.sku,
        "name": item.name,
        "eoq_analysis": eoq,
        "safety_stock": safety,
        "reorder_point": rop,
        "inventory_levels": {
            "avg_inventory_units": round(avg_inventory, 0),
            "max_inventory_units": round(max_inventory, 0),
            "safety_stock_units": safety["safety_stock_units"],
            "avg_inventory_value": round(avg_inventory_value, 2),
            "annual_holding_cost": round(annual_holding_cost, 2),
        },
        "performance": {
            "inventory_turns": round(inventory_turns, 1),
            "days_inventory": round(days_inventory, 1),
            "service_level": item.service_level,
        },
        "current_status": {
            "current_inventory": item.current_inventory,
            "vs_avg": round(item.current_inventory - avg_inventory, 0),
            "weeks_of_stock": round(item.current_inventory / (avg_daily_demand * 7), 1) if avg_daily_demand > 0 else 0,
            "below_rop": item.current_inventory < rop["reorder_point_units"],
        },
    }


def analyze_supplier(
    supplier: Supplier,
    annual_spend: float,
    orders_per_year: int,
) -> dict:
    """
    Analyze supplier performance and total cost of ownership.

    Args:
        supplier: Supplier object
        annual_spend: Annual spend with supplier
        orders_per_year: Number of orders placed per year

    Returns:
        Supplier analysis
    """
    # Quality cost (defect rate × cost)
    defect_rate = 1 - supplier.quality_rate
    quality_cost = annual_spend * defect_rate * 0.5  # Assume 50% cost for defects

    # Delivery reliability cost (late deliveries cause expediting costs)
    late_rate = 1 - supplier.lead_time_reliability
    late_delivery_cost = annual_spend * late_rate * 0.02  # 2% of late order value

    # Working capital cost (payment terms)
    # Compare to 30-day baseline
    wc_impact = annual_spend * (supplier.payment_terms_days - 30) / 365 * 0.08  # 8% cost of capital

    # Volume discount opportunity
    order_value = annual_spend / orders_per_year if orders_per_year > 0 else 0
    qualifies_for_discount = order_value >= supplier.volume_discount_threshold if supplier.volume_discount_threshold > 0 else False
    discount_value = annual_spend * supplier.volume_discount_rate if qualifies_for_discount else 0

    # Total Cost of Ownership
    base_cost = annual_spend
    tco = base_cost + quality_cost + late_delivery_cost - wc_impact - discount_value

    # Supplier score (0-100)
    quality_score = supplier.quality_rate * 30
    delivery_score = supplier.lead_time_reliability * 30
    price_score = max(0, (2 - supplier.price_competitiveness)) * 20  # 1.0 = 20 pts, 0.8 = 24 pts
    terms_score = min(20, supplier.payment_terms_days / 3)  # Longer terms = better

    total_score = quality_score + delivery_score + price_score + terms_score

    return {
        "supplier": supplier.name,
        "items_supplied": supplier.items_supplied,
        "annual_spend": annual_spend,
        "performance": {
            "quality_rate_pct": round(supplier.quality_rate * 100, 1),
            "on_time_delivery_pct": round(supplier.lead_time_reliability * 100, 1),
            "lead_time_days": supplier.lead_time_days,
            "payment_terms_days": supplier.payment_terms_days,
        },
        "total_cost_of_ownership": {
            "base_cost": round(base_cost, 2),
            "quality_cost": round(quality_cost, 2),
            "late_delivery_cost": round(late_delivery_cost, 2),
            "working_capital_impact": round(wc_impact, 2),
            "volume_discount": round(discount_value, 2),
            "total_tco": round(tco, 2),
            "tco_premium_pct": round((tco / base_cost - 1) * 100, 2),
        },
        "supplier_score": {
            "quality": round(quality_score, 1),
            "delivery": round(delivery_score, 1),
            "price": round(price_score, 1),
            "terms": round(terms_score, 1),
            "total": round(total_score, 1),
            "rating": "A" if total_score >= 80 else "B" if total_score >= 65 else "C" if total_score >= 50 else "D",
        },
    }


def calculate_inventory_metrics(
    total_cogs: float,
    avg_inventory_value: float,
    total_orders: int,
    perfect_orders: int,
    total_order_lines: int,
    filled_order_lines: int,
    days_payable: float,
    days_receivable: float,
) -> dict:
    """
    Calculate key supply chain metrics.

    Args:
        total_cogs: Cost of goods sold
        avg_inventory_value: Average inventory value
        total_orders: Total orders shipped
        perfect_orders: Orders with no issues
        total_order_lines: Total order lines
        filled_order_lines: Order lines filled completely
        days_payable: Days payable outstanding
        days_receivable: Days sales outstanding

    Returns:
        Supply chain metrics
    """
    # Inventory turns
    inventory_turns = total_cogs / avg_inventory_value if avg_inventory_value > 0 else 0

    # Days of inventory
    days_inventory = 365 / inventory_turns if inventory_turns > 0 else 0

    # Perfect order rate
    perfect_order_rate = perfect_orders / total_orders if total_orders > 0 else 0

    # Fill rate
    fill_rate = filled_order_lines / total_order_lines if total_order_lines > 0 else 0

    # Cash-to-cash cycle
    cash_to_cash = days_inventory + days_receivable - days_payable

    return {
        "inventory_turns": round(inventory_turns, 1),
        "days_inventory": round(days_inventory, 1),
        "perfect_order_rate_pct": round(perfect_order_rate * 100, 1),
        "fill_rate_pct": round(fill_rate * 100, 1),
        "cash_cycle": {
            "days_inventory": round(days_inventory, 1),
            "days_receivable": days_receivable,
            "days_payable": days_payable,
            "cash_to_cash_days": round(cash_to_cash, 1),
        },
    }


def optimize_inventory_policy(
    items: List[InventoryItem],
    target_service_level: float = 0.95,
    capital_constraint: float = None,
) -> dict:
    """
    Optimize inventory policy across multiple items.

    Args:
        items: List of InventoryItem objects
        target_service_level: Target service level for all items
        capital_constraint: Optional working capital constraint

    Returns:
        Optimized inventory policy
    """
    item_analyses = []
    total_inventory_value = 0
    total_annual_cost = 0

    for item in items:
        item.service_level = target_service_level
        analysis = analyze_inventory_item(item)
        item_analyses.append(analysis)
        total_inventory_value += analysis["inventory_levels"]["avg_inventory_value"]
        total_annual_cost += (
            analysis["eoq_analysis"]["costs"]["total_annual_cost"] +
            analysis["inventory_levels"]["annual_holding_cost"]
        )

    # ABC classification by value
    item_analyses.sort(
        key=lambda x: x["eoq_analysis"]["parameters"]["annual_demand"] *
                     x["eoq_analysis"]["parameters"]["unit_cost"],
        reverse=True
    )

    # Calculate cumulative value share
    total_value = sum(
        a["eoq_analysis"]["parameters"]["annual_demand"] *
        a["eoq_analysis"]["parameters"]["unit_cost"]
        for a in item_analyses
    )

    cumulative_value = 0
    for i, analysis in enumerate(item_analyses):
        item_value = (
            analysis["eoq_analysis"]["parameters"]["annual_demand"] *
            analysis["eoq_analysis"]["parameters"]["unit_cost"]
        )
        cumulative_value += item_value
        cumulative_pct = cumulative_value / total_value

        # ABC classification
        if cumulative_pct <= 0.80:
            analysis["abc_class"] = "A"
        elif cumulative_pct <= 0.95:
            analysis["abc_class"] = "B"
        else:
            analysis["abc_class"] = "C"

        analysis["value_rank"] = i + 1
        analysis["value_share_pct"] = round(item_value / total_value * 100, 2)
        analysis["cumulative_value_pct"] = round(cumulative_pct * 100, 2)

    # Summary by class
    class_summary = {}
    for cls in ["A", "B", "C"]:
        class_items = [a for a in item_analyses if a["abc_class"] == cls]
        class_summary[cls] = {
            "item_count": len(class_items),
            "item_share_pct": round(len(class_items) / len(item_analyses) * 100, 1),
            "value_share_pct": round(sum(a["value_share_pct"] for a in class_items), 1),
            "avg_turns": round(
                sum(a["performance"]["inventory_turns"] for a in class_items) / len(class_items), 1
            ) if class_items else 0,
        }

    result = {
        "total_items": len(items),
        "target_service_level": target_service_level,
        "total_inventory_value": round(total_inventory_value, 2),
        "total_annual_inventory_cost": round(total_annual_cost, 2),
        "abc_analysis": class_summary,
        "item_details": item_analyses,
    }

    # Check capital constraint
    if capital_constraint and total_inventory_value > capital_constraint:
        result["constraint_violation"] = {
            "required": total_inventory_value,
            "available": capital_constraint,
            "shortfall": round(total_inventory_value - capital_constraint, 2),
            "recommendation": "Reduce service level or prioritize A-class items",
        }

    return result


def analyze_supply_chain_risk(
    suppliers: List[Supplier],
    single_source_items: List[str],
    critical_items: List[str],
    lead_time_buffer_days: float = 0,
) -> dict:
    """
    Analyze supply chain risk.

    Args:
        suppliers: List of Supplier objects
        single_source_items: Items with only one supplier
        critical_items: Business-critical items
        lead_time_buffer_days: Current lead time buffer

    Returns:
        Risk analysis
    """
    risks = []
    risk_score = 0

    # Single source risk
    single_source_critical = [
        item for item in single_source_items if item in critical_items
    ]
    if single_source_critical:
        risks.append({
            "risk": "Single-source critical items",
            "severity": "high",
            "items": single_source_critical,
            "mitigation": "Develop alternative suppliers",
        })
        risk_score += 30

    # Supplier concentration risk
    total_items = sum(len(s.items_supplied) for s in suppliers)
    for supplier in suppliers:
        share = len(supplier.items_supplied) / total_items if total_items > 0 else 0
        if share > 0.5:
            risks.append({
                "risk": f"High supplier concentration: {supplier.name}",
                "severity": "medium",
                "share_pct": round(share * 100, 1),
                "mitigation": "Diversify supplier base",
            })
            risk_score += 20

    # Quality risk
    low_quality_suppliers = [s for s in suppliers if s.quality_rate < 0.95]
    if low_quality_suppliers:
        risks.append({
            "risk": "Suppliers with quality issues",
            "severity": "medium",
            "suppliers": [s.name for s in low_quality_suppliers],
            "mitigation": "Implement quality improvement programs",
        })
        risk_score += 15

    # Delivery risk
    unreliable_suppliers = [s for s in suppliers if s.lead_time_reliability < 0.90]
    if unreliable_suppliers:
        risks.append({
            "risk": "Suppliers with delivery issues",
            "severity": "medium",
            "suppliers": [s.name for s in unreliable_suppliers],
            "mitigation": "Increase safety stock or find alternatives",
        })
        risk_score += 15

    # Lead time buffer risk
    max_lead_time = max(s.lead_time_days for s in suppliers) if suppliers else 0
    if lead_time_buffer_days < max_lead_time * 0.2:
        risks.append({
            "risk": "Insufficient lead time buffer",
            "severity": "low",
            "current_buffer_days": lead_time_buffer_days,
            "recommended_buffer_days": round(max_lead_time * 0.2, 1),
            "mitigation": "Increase safety stock",
        })
        risk_score += 10

    # Overall risk rating
    if risk_score >= 50:
        overall_rating = "high"
    elif risk_score >= 25:
        overall_rating = "medium"
    else:
        overall_rating = "low"

    return {
        "risk_score": risk_score,
        "max_score": 100,
        "overall_rating": overall_rating,
        "identified_risks": risks,
        "single_source_items": single_source_items,
        "critical_items": critical_items,
        "recommendations": [r["mitigation"] for r in risks],
    }


def benchmark_supply_chain(
    inventory_turns: float,
    fill_rate: float,
    perfect_order_rate: float,
    on_time_delivery: float,
    days_inventory: float,
    cash_to_cash_days: float,
    industry: str = "manufacturing",
) -> dict:
    """
    Benchmark supply chain metrics against industry standards.

    Args:
        inventory_turns: Annual inventory turns
        fill_rate: Order fill rate
        perfect_order_rate: Perfect order rate
        on_time_delivery: On-time delivery rate
        days_inventory: Days of inventory
        cash_to_cash_days: Cash-to-cash cycle days
        industry: Industry for benchmarking

    Returns:
        Benchmark comparison
    """
    benchmarks = SUPPLY_CHAIN_BENCHMARKS.get(industry, SUPPLY_CHAIN_BENCHMARKS["manufacturing"])

    def get_rating(value, benchmark, higher_is_better=True):
        ratio = value / benchmark if benchmark > 0 else 0
        if higher_is_better:
            if ratio >= 1.2:
                return "excellent"
            elif ratio >= 0.9:
                return "good"
            elif ratio >= 0.7:
                return "acceptable"
            else:
                return "needs_improvement"
        else:
            if ratio <= 0.7:
                return "excellent"
            elif ratio <= 0.9:
                return "good"
            elif ratio <= 1.2:
                return "acceptable"
            else:
                return "needs_improvement"

    return {
        "industry": industry,
        "metrics": {
            "inventory_turns": {
                "value": inventory_turns,
                "benchmark": benchmarks["inventory_turns"],
                "rating": get_rating(inventory_turns, benchmarks["inventory_turns"], True),
            },
            "fill_rate": {
                "value_pct": round(fill_rate * 100, 1),
                "benchmark_pct": round(benchmarks["fill_rate"] * 100, 1),
                "rating": get_rating(fill_rate, benchmarks["fill_rate"], True),
            },
            "perfect_order_rate": {
                "value_pct": round(perfect_order_rate * 100, 1),
                "benchmark_pct": round(benchmarks["perfect_order_rate"] * 100, 1),
                "rating": get_rating(perfect_order_rate, benchmarks["perfect_order_rate"], True),
            },
            "on_time_delivery": {
                "value_pct": round(on_time_delivery * 100, 1),
                "benchmark_pct": round(benchmarks["on_time_delivery"] * 100, 1),
                "rating": get_rating(on_time_delivery, benchmarks["on_time_delivery"], True),
            },
            "days_inventory": {
                "value": days_inventory,
                "benchmark": benchmarks["days_inventory"],
                "rating": get_rating(days_inventory, benchmarks["days_inventory"], False),
            },
            "cash_to_cash": {
                "value": cash_to_cash_days,
                "benchmark": benchmarks["cash_to_cash_days"],
                "rating": get_rating(cash_to_cash_days, benchmarks["cash_to_cash_days"], False),
            },
        },
    }


def analyze_supply_chain(
    inventory_items: List[InventoryItem] = None,
    suppliers: List[Supplier] = None,
    total_cogs: float = None,
    avg_inventory_value: float = None,
    total_orders: int = None,
    perfect_orders: int = None,
    fill_rate: float = None,
    days_receivable: float = 45,
    days_payable: float = 30,
    industry: str = "manufacturing",
    capital_constraint: float = None,
    run_optimization: bool = True,
    run_benchmarks: bool = True,
    run_risk_analysis: bool = True,
) -> dict:
    """
    Run comprehensive supply chain analysis (SCO-1.0 main entry point).

    Args:
        inventory_items: List of InventoryItem objects
        suppliers: List of Supplier objects
        total_cogs: Total cost of goods sold
        avg_inventory_value: Average inventory value
        total_orders: Total orders
        perfect_orders: Perfect orders
        fill_rate: Fill rate (if order lines not available)
        days_receivable: Days sales outstanding
        days_payable: Days payable outstanding
        industry: Industry for benchmarking
        capital_constraint: Working capital constraint
        run_optimization: Run inventory optimization
        run_benchmarks: Run industry benchmarking
        run_risk_analysis: Run risk analysis

    Returns:
        Comprehensive supply chain analysis
    """
    result = {
        "model_id": "SCO-1.0",
        "model_name": "Supply Chain Optimization Model",
    }

    # Inventory analysis
    if inventory_items:
        if run_optimization:
            optimization = optimize_inventory_policy(
                items=inventory_items,
                target_service_level=0.95,
                capital_constraint=capital_constraint,
            )
            result["inventory_optimization"] = optimization
            result["summary"] = {
                "total_items": optimization["total_items"],
                "total_inventory_value": optimization["total_inventory_value"],
                "total_annual_cost": optimization["total_annual_inventory_cost"],
                "abc_a_items": optimization["abc_analysis"]["A"]["item_count"],
                "abc_a_value_pct": optimization["abc_analysis"]["A"]["value_share_pct"],
            }

    # Supplier analysis
    if suppliers:
        supplier_analyses = []
        total_spend = 0
        for supplier in suppliers:
            # Estimate spend (simplified)
            spend = 100000  # Default, should be passed in
            analysis = analyze_supplier(supplier, spend, 24)
            supplier_analyses.append(analysis)
            total_spend += spend

        result["supplier_analysis"] = {
            "total_suppliers": len(suppliers),
            "total_spend": total_spend,
            "suppliers": supplier_analyses,
            "avg_quality_rate": round(
                sum(s.quality_rate for s in suppliers) / len(suppliers) * 100, 1
            ),
            "avg_on_time_delivery": round(
                sum(s.lead_time_reliability for s in suppliers) / len(suppliers) * 100, 1
            ),
        }

    # Supply chain metrics
    if total_cogs and avg_inventory_value:
        inventory_turns = total_cogs / avg_inventory_value
        days_inventory = 365 / inventory_turns if inventory_turns > 0 else 0
        perfect_order_rate = perfect_orders / total_orders if total_orders and perfect_orders else 0.90

        metrics = {
            "inventory_turns": round(inventory_turns, 1),
            "days_inventory": round(days_inventory, 1),
            "perfect_order_rate_pct": round(perfect_order_rate * 100, 1),
            "fill_rate_pct": round(fill_rate * 100, 1) if fill_rate else 95.0,
            "cash_to_cash_days": round(days_inventory + days_receivable - days_payable, 1),
        }
        result["metrics"] = metrics

        if "summary" not in result:
            result["summary"] = {}
        result["summary"]["inventory_turns"] = metrics["inventory_turns"]
        result["summary"]["days_inventory"] = metrics["days_inventory"]
        result["summary"]["cash_to_cash_days"] = metrics["cash_to_cash_days"]

        # Benchmarking
        if run_benchmarks:
            result["benchmark"] = benchmark_supply_chain(
                inventory_turns=inventory_turns,
                fill_rate=fill_rate or 0.95,
                perfect_order_rate=perfect_order_rate,
                on_time_delivery=0.92,  # Default
                days_inventory=days_inventory,
                cash_to_cash_days=metrics["cash_to_cash_days"],
                industry=industry,
            )

    # Risk analysis
    if run_risk_analysis and suppliers and inventory_items:
        # Identify single-source and critical items
        item_suppliers = {}
        for supplier in suppliers:
            for item in supplier.items_supplied:
                if item not in item_suppliers:
                    item_suppliers[item] = []
                item_suppliers[item].append(supplier.name)

        single_source = [item for item, sups in item_suppliers.items() if len(sups) == 1]
        # Top 20% by value are critical
        critical = [a["sku"] for a in result.get("inventory_optimization", {}).get("item_details", [])[:3]]

        result["risk_analysis"] = analyze_supply_chain_risk(
            suppliers=suppliers,
            single_source_items=single_source,
            critical_items=critical,
        )

    return result


# Convenience alias
optimize_supply_chain = analyze_supply_chain


if __name__ == "__main__":
    # Example: Manufacturing Company
    print("=" * 60)
    print("SCO-1.0: Supply Chain Optimization Model")
    print("=" * 60)

    # Define inventory items
    items = [
        InventoryItem(
            sku="RAW-001",
            name="Steel Sheets",
            annual_demand=50000,
            unit_cost=25.00,
            ordering_cost=150,
            holding_cost_rate=0.25,
            lead_time_days=14,
            demand_std_daily=20,
            current_inventory=3000,
        ),
        InventoryItem(
            sku="RAW-002",
            name="Plastic Pellets",
            annual_demand=100000,
            unit_cost=2.50,
            ordering_cost=100,
            holding_cost_rate=0.20,
            lead_time_days=7,
            demand_std_daily=50,
            current_inventory=15000,
        ),
        InventoryItem(
            sku="COMP-001",
            name="Electronic Components",
            annual_demand=25000,
            unit_cost=15.00,
            ordering_cost=200,
            holding_cost_rate=0.30,
            lead_time_days=21,
            demand_std_daily=10,
            current_inventory=2500,
        ),
    ]

    # Define suppliers
    suppliers = [
        Supplier(
            name="SteelCo",
            items_supplied=["RAW-001"],
            lead_time_days=14,
            lead_time_reliability=0.92,
            quality_rate=0.98,
            payment_terms_days=45,
        ),
        Supplier(
            name="PlastiChem",
            items_supplied=["RAW-002"],
            lead_time_days=7,
            lead_time_reliability=0.95,
            quality_rate=0.99,
            payment_terms_days=30,
        ),
        Supplier(
            name="ElectroSupply",
            items_supplied=["COMP-001"],
            lead_time_days=21,
            lead_time_reliability=0.88,
            quality_rate=0.96,
            payment_terms_days=30,
        ),
    ]

    result = analyze_supply_chain(
        inventory_items=items,
        suppliers=suppliers,
        total_cogs=5_000_000,
        avg_inventory_value=500_000,
        total_orders=10000,
        perfect_orders=9000,
        fill_rate=0.96,
        industry="manufacturing",
    )

    print(f"\nSummary:")
    print(f"  Total Items: {result['summary']['total_items']}")
    print(f"  Total Inventory Value: ${result['summary']['total_inventory_value']:,.0f}")
    print(f"  A-Class Items: {result['summary']['abc_a_items']} ({result['summary']['abc_a_value_pct']}% of value)")
    print(f"  Inventory Turns: {result['summary']['inventory_turns']}")
    print(f"  Days Inventory: {result['summary']['days_inventory']}")
    print(f"  Cash-to-Cash: {result['summary']['cash_to_cash_days']} days")

    print(f"\nSupplier Performance:")
    print(f"  Avg Quality Rate: {result['supplier_analysis']['avg_quality_rate']}%")
    print(f"  Avg On-Time Delivery: {result['supplier_analysis']['avg_on_time_delivery']}%")

    if "risk_analysis" in result:
        print(f"\nRisk Analysis:")
        print(f"  Risk Score: {result['risk_analysis']['risk_score']}/100")
        print(f"  Overall Rating: {result['risk_analysis']['overall_rating']}")
        print(f"  Identified Risks: {len(result['risk_analysis']['identified_risks'])}")
