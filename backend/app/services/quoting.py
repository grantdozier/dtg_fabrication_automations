"""
CNC Quoting Calculation Engine

This module implements the core quoting logic for CNC machining.
It calculates accurate per-unit costs considering:
- Material cost with scrap factor
- Machine time and rates
- Labor time and rates
- Setup time amortization
- Process allowances
"""

from dataclasses import dataclass
from typing import List, Dict

@dataclass
class QuoteBreakdown:
    """Detailed cost breakdown for a quoted part"""
    material_unit: float
    machine_unit: float
    labor_unit: float
    unit_cost: float
    unit_price: float
    total_time_hr: float

    def to_dict(self) -> dict:
        return {
            "material_unit": round(self.material_unit, 2),
            "machine_unit": round(self.machine_unit, 2),
            "labor_unit": round(self.labor_unit, 2),
            "unit_cost": round(self.unit_cost, 2),
            "unit_price": round(self.unit_price, 2),
            "total_time_hr": round(self.total_time_hr, 4),
        }

def calc_unit_cost(
    *,
    quantity: int,
    stock_weight_lb: float,
    cost_per_lb: float,
    scrap_factor: float,
    ops: List[Dict],
    margin_pct: float = 0.15,
) -> QuoteBreakdown:
    """
    Calculate per-unit cost and price for a CNC machined part.

    Args:
        quantity: Number of parts to produce
        stock_weight_lb: Raw material weight per part in pounds
        cost_per_lb: Material cost per pound
        scrap_factor: Scrap percentage (0.05 = 5%)
        ops: List of operations, each containing:
            - setup_time_hr: One-time setup hours
            - cycle_time_hr: Per-part cycle hours
            - allowance_pct: Non-cut time allowance (0.10 = 10%)
            - machine_rate_per_hr: Machine hourly rate
            - labor_rate_per_hr: Labor hourly rate
        margin_pct: Profit margin (0.15 = 15%)

    Returns:
        QuoteBreakdown with detailed cost analysis
    """

    # Material Cost Calculation
    # Includes raw stock cost + scrap factor
    material_unit = (stock_weight_lb * cost_per_lb) * (1.0 + scrap_factor)

    # Time and Cost Accumulation
    machine_unit = 0.0
    labor_unit = 0.0
    total_time_hr = 0.0

    for op in ops:
        # Setup time is amortized across the quantity
        setup_per_part = op["setup_time_hr"] / max(quantity, 1)

        # Allowance accounts for non-cutting time (tool changes, inspection, etc.)
        allowance = op["cycle_time_hr"] * op["allowance_pct"]

        # Total time per part for this operation
        t_part = setup_per_part + op["cycle_time_hr"] + allowance

        # Cost accumulation
        machine_unit += t_part * op["machine_rate_per_hr"]
        labor_unit += t_part * op["labor_rate_per_hr"]
        total_time_hr += t_part

    # Total Cost (at cost)
    unit_cost = material_unit + machine_unit + labor_unit

    # Selling Price (cost + margin)
    unit_price = unit_cost * (1.0 + margin_pct)

    return QuoteBreakdown(
        material_unit=material_unit,
        machine_unit=machine_unit,
        labor_unit=labor_unit,
        unit_cost=unit_cost,
        unit_price=unit_price,
        total_time_hr=total_time_hr,
    )
