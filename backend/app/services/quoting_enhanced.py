"""
Enhanced CNC Quoting Calculation Engine

Implements industry-standard machine shop quoting with comprehensive
cost breakdowns satisfying Rules 2, 3, and 4.
"""

from dataclasses import dataclass
from typing import List, Dict

@dataclass
class TimeBreakdown:
    """Detailed time breakdown per part (Rule 2)"""
    setup_time_per_part: float
    cycle_time: float
    allowance_time: float
    tool_change_time: float
    inspection_time: float
    total_time_per_part: float

    def to_dict(self) -> dict:
        return {
            "setup_time_per_part": round(self.setup_time_per_part, 4),
            "cycle_time": round(self.cycle_time, 4),
            "allowance_time": round(self.allowance_time, 4),
            "tool_change_time": round(self.tool_change_time, 4),
            "inspection_time": round(self.inspection_time, 4),
            "total_time_per_part": round(self.total_time_per_part, 4),
        }

@dataclass
class CostBreakdown:
    """Detailed cost breakdown per part (Rule 3)"""
    # Material costs
    material_base: float
    material_scrap: float
    material_total: float

    # Time-based costs
    machine_cost: float
    labor_cost: float

    # Additional costs
    tooling_cost: float
    programming_cost: float
    inspection_cost: float
    consumables_cost: float
    overhead_cost: float

    # Totals
    subtotal_cost: float
    unit_cost: float
    margin_amount: float
    unit_price: float

    def to_dict(self) -> dict:
        return {
            "material": {
                "base": round(self.material_base, 2),
                "scrap": round(self.material_scrap, 2),
                "total": round(self.material_total, 2),
            },
            "machine_cost": round(self.machine_cost, 2),
            "labor_cost": round(self.labor_cost, 2),
            "tooling_cost": round(self.tooling_cost, 2),
            "programming_cost": round(self.programming_cost, 2),
            "inspection_cost": round(self.inspection_cost, 2),
            "consumables_cost": round(self.consumables_cost, 2),
            "overhead_cost": round(self.overhead_cost, 2),
            "subtotal_cost": round(self.subtotal_cost, 2),
            "unit_cost": round(self.unit_cost, 2),
            "margin_amount": round(self.margin_amount, 2),
            "unit_price": round(self.unit_price, 2),
        }

@dataclass
class OperationBreakdown:
    """Per-operation cost and time breakdown"""
    operation_name: str
    operation_type: str
    sequence: int

    # Time components
    setup_time_per_part: float
    cycle_time: float
    allowance_time: float
    tool_change_time: float
    inspection_time: float
    total_time: float

    # Cost components
    machine_cost: float
    labor_cost: float
    tooling_cost: float
    consumables_cost: float
    total_cost: float

    def to_dict(self) -> dict:
        return {
            "operation_name": self.operation_name,
            "operation_type": self.operation_type,
            "sequence": self.sequence,
            "time": {
                "setup_per_part": round(self.setup_time_per_part, 4),
                "cycle": round(self.cycle_time, 4),
                "allowance": round(self.allowance_time, 4),
                "tool_change": round(self.tool_change_time, 4),
                "inspection": round(self.inspection_time, 4),
                "total": round(self.total_time, 4),
            },
            "cost": {
                "machine": round(self.machine_cost, 2),
                "labor": round(self.labor_cost, 2),
                "tooling": round(self.tooling_cost, 2),
                "consumables": round(self.consumables_cost, 2),
                "total": round(self.total_cost, 2),
            }
        }

@dataclass
class DetailedQuoteBreakdown:
    """Complete detailed quote breakdown (Rules 2, 3, 4)"""
    time_breakdown: TimeBreakdown
    cost_breakdown: CostBreakdown
    operations_breakdown: List[OperationBreakdown]

    # Summary
    quantity: int
    unit_cost: float
    unit_price: float
    margin_pct: float
    extended_cost: float
    extended_price: float
    profit_amount: float

    def to_dict(self) -> dict:
        return {
            "time_breakdown": self.time_breakdown.to_dict(),
            "cost_breakdown": self.cost_breakdown.to_dict(),
            "operations": [op.to_dict() for op in self.operations_breakdown],
            "summary": {
                "quantity": self.quantity,
                "unit_cost": round(self.unit_cost, 2),
                "unit_price": round(self.unit_price, 2),
                "margin_pct": round(self.margin_pct * 100, 1),
                "extended_cost": round(self.extended_cost, 2),
                "extended_price": round(self.extended_price, 2),
                "profit_amount": round(self.profit_amount, 2),
            }
        }


def calc_operation_breakdown(
    operation: Dict,
    quantity: int,
    machine_rate: float,
    labor_rate: float
) -> OperationBreakdown:
    """
    Calculate detailed breakdown for a single operation.

    Args:
        operation: Operation dictionary with all parameters
        quantity: Total quantity being quoted
        machine_rate: Machine hourly rate
        labor_rate: Labor hourly rate

    Returns:
        OperationBreakdown with detailed time and cost analysis
    """

    # Time calculations
    setup_per_part = operation["setup_time_hr"] / max(quantity, 1)
    cycle_time = operation["cycle_time_hr"]
    allowance_time = cycle_time * operation["allowance_pct"]
    tool_change_time = operation.get("tool_change_time_min", 0.0) / 60.0  # Convert minutes to hours
    inspection_time = operation.get("inspection_time_min", 0.0) / 60.0  # Convert minutes to hours

    total_time = setup_per_part + cycle_time + allowance_time + tool_change_time + inspection_time

    # Cost calculations
    machine_cost = total_time * machine_rate
    labor_cost = total_time * labor_rate
    tooling_cost = operation.get("tool_cost_per_part", 0.0)
    consumables_cost = operation.get("consumables_cost_per_part", 0.0)

    total_cost = machine_cost + labor_cost + tooling_cost + consumables_cost

    return OperationBreakdown(
        operation_name=operation["name"],
        operation_type=operation.get("operation_type", "machining"),
        sequence=operation["sequence"],
        setup_time_per_part=setup_per_part,
        cycle_time=cycle_time,
        allowance_time=allowance_time,
        tool_change_time=tool_change_time,
        inspection_time=inspection_time,
        total_time=total_time,
        machine_cost=machine_cost,
        labor_cost=labor_cost,
        tooling_cost=tooling_cost,
        consumables_cost=consumables_cost,
        total_cost=total_cost,
    )


def calc_detailed_quote(
    *,
    quantity: int,
    stock_weight_lb: float,
    cost_per_lb: float,
    scrap_factor: float,
    ops: List[Dict],
    programming_time_hr: float = 0.0,
    programming_rate_per_hr: float = 75.0,
    first_article_inspection_hr: float = 0.0,
    overhead_rate_pct: float = 1.5,
    margin_pct: float = 0.15,
) -> DetailedQuoteBreakdown:
    """
    Calculate comprehensive detailed quote breakdown.

    Implements industry-standard machine shop quoting methodology
    with complete itemization per Rules 2, 3, and 4.

    Args:
        quantity: Number of parts to produce
        stock_weight_lb: Raw material weight per part
        cost_per_lb: Material cost per pound
        scrap_factor: Scrap percentage (0.05 = 5%)
        ops: List of operations with all parameters
        programming_time_hr: CAM/programming time (amortized)
        programming_rate_per_hr: Programming labor rate
        first_article_inspection_hr: First article inspection time (amortized)
        overhead_rate_pct: Overhead multiplier (1.5 = 150%)
        margin_pct: Profit margin (0.15 = 15%)

    Returns:
        DetailedQuoteBreakdown with complete cost and time analysis
    """

    # ==================== MATERIAL COST ====================
    material_base = stock_weight_lb * cost_per_lb
    material_scrap = material_base * scrap_factor
    material_total = material_base + material_scrap

    # ==================== OPERATIONS BREAKDOWN ====================
    operations_breakdown = []
    total_machine_cost = 0.0
    total_labor_cost = 0.0
    total_tooling_cost = 0.0
    total_consumables_cost = 0.0
    total_time = 0.0

    # Time accumulators
    total_setup_time = 0.0
    total_cycle_time = 0.0
    total_allowance_time = 0.0
    total_tool_change_time = 0.0
    total_inspection_time = 0.0

    for op in ops:
        op_breakdown = calc_operation_breakdown(
            operation=op,
            quantity=quantity,
            machine_rate=op["machine_rate_per_hr"],
            labor_rate=op["labor_rate_per_hr"]
        )

        operations_breakdown.append(op_breakdown)

        # Accumulate costs
        total_machine_cost += op_breakdown.machine_cost
        total_labor_cost += op_breakdown.labor_cost
        total_tooling_cost += op_breakdown.tooling_cost
        total_consumables_cost += op_breakdown.consumables_cost
        total_time += op_breakdown.total_time

        # Accumulate time components
        total_setup_time += op_breakdown.setup_time_per_part
        total_cycle_time += op_breakdown.cycle_time
        total_allowance_time += op_breakdown.allowance_time
        total_tool_change_time += op_breakdown.tool_change_time
        total_inspection_time += op_breakdown.inspection_time

    # ==================== PROGRAMMING COST ====================
    programming_cost = 0.0
    if programming_time_hr > 0:
        programming_cost = (programming_time_hr * programming_rate_per_hr) / quantity

    # ==================== INSPECTION COST ====================
    inspection_cost = 0.0
    if first_article_inspection_hr > 0:
        # First article is one-time cost amortized over quantity
        # Assume inspection at programming rate
        inspection_cost = (first_article_inspection_hr * programming_rate_per_hr) / quantity

    # ==================== OVERHEAD ALLOCATION ====================
    # Overhead applied to direct labor as per industry standard
    direct_costs = total_machine_cost + total_labor_cost
    overhead_cost = direct_costs * (overhead_rate_pct - 1.0)  # Subtract 1 since rates already include base

    # ==================== TOTAL COST ====================
    subtotal_cost = (
        material_total +
        total_machine_cost +
        total_labor_cost +
        total_tooling_cost +
        programming_cost +
        inspection_cost +
        total_consumables_cost
    )

    unit_cost = subtotal_cost + overhead_cost

    # ==================== MARGIN & PRICE ====================
    margin_amount = unit_cost * margin_pct
    unit_price = unit_cost + margin_amount

    # Extended totals
    extended_cost = unit_cost * quantity
    extended_price = unit_price * quantity
    profit_amount = extended_price - extended_cost

    # ==================== BUILD BREAKDOWN OBJECTS ====================
    time_breakdown = TimeBreakdown(
        setup_time_per_part=total_setup_time,
        cycle_time=total_cycle_time,
        allowance_time=total_allowance_time,
        tool_change_time=total_tool_change_time,
        inspection_time=total_inspection_time,
        total_time_per_part=total_time,
    )

    cost_breakdown = CostBreakdown(
        material_base=material_base,
        material_scrap=material_scrap,
        material_total=material_total,
        machine_cost=total_machine_cost,
        labor_cost=total_labor_cost,
        tooling_cost=total_tooling_cost,
        programming_cost=programming_cost,
        inspection_cost=inspection_cost,
        consumables_cost=total_consumables_cost,
        overhead_cost=overhead_cost,
        subtotal_cost=subtotal_cost,
        unit_cost=unit_cost,
        margin_amount=margin_amount,
        unit_price=unit_price,
    )

    return DetailedQuoteBreakdown(
        time_breakdown=time_breakdown,
        cost_breakdown=cost_breakdown,
        operations_breakdown=operations_breakdown,
        quantity=quantity,
        unit_cost=unit_cost,
        unit_price=unit_price,
        margin_pct=margin_pct,
        extended_cost=extended_cost,
        extended_price=extended_price,
        profit_amount=profit_amount,
    )
