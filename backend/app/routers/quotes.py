from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from pydantic import BaseModel
from ..db import get_db
from .. import models
from ..services.quoting import calc_unit_cost

router = APIRouter(prefix="/api/quotes", tags=["quotes"])

class CalculateRequest(BaseModel):
    part_id: int
    quantity: int
    margin_pct: float = 0.15

class CalculateResponse(BaseModel):
    material_unit: float
    machine_unit: float
    labor_unit: float
    unit_cost: float
    unit_price: float
    total_time_hr: float

class QuoteItemCreate(BaseModel):
    part_id: int
    quantity: int
    margin_pct: float = 0.15

class QuoteCreate(BaseModel):
    customer_id: int
    notes: str | None = None
    items: List[QuoteItemCreate]

class QuoteItemResponse(BaseModel):
    id: int
    part_id: int
    quantity: int
    margin_pct: float
    material_cost_unit: float
    machine_cost_unit: float
    labor_cost_unit: float
    unit_cost: float
    unit_price: float

    class Config:
        from_attributes = True

class QuoteResponse(BaseModel):
    id: int
    customer_id: int
    quote_number: str | None
    status: str
    notes: str | None
    items: List[QuoteItemResponse] = []

    class Config:
        from_attributes = True

@router.post("/calculate", response_model=CalculateResponse)
def calculate(payload: CalculateRequest, db: Session = Depends(get_db)):
    """
    Calculate cost breakdown for a part without saving.
    Used for real-time quote preview.
    """
    part = db.query(models.Part).options(
        joinedload(models.Part.operations).joinedload(models.Operation.machine),
        joinedload(models.Part.material)
    ).filter(models.Part.id == payload.part_id).first()

    if not part:
        raise HTTPException(status_code=404, detail="Part not found")

    ops = []
    for op in part.operations:
        ops.append({
            "setup_time_hr": op.setup_time_hr,
            "cycle_time_hr": op.cycle_time_hr,
            "allowance_pct": op.allowance_pct,
            "machine_rate_per_hr": op.machine.machine_rate_per_hr,
            "labor_rate_per_hr": op.machine.labor_rate_per_hr,
        })

    breakdown = calc_unit_cost(
        quantity=payload.quantity,
        stock_weight_lb=part.stock_weight_lb,
        cost_per_lb=part.material.cost_per_lb,
        scrap_factor=part.scrap_factor,
        ops=ops,
        margin_pct=payload.margin_pct,
    )

    return breakdown.to_dict()

@router.post("", response_model=QuoteResponse)
def create_quote(payload: QuoteCreate, db: Session = Depends(get_db)):
    """
    Create and save a complete quote with calculated pricing.
    """

    # Verify customer exists
    customer = db.get(models.Customer, payload.customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Create quote
    quote = models.Quote(
        customer_id=payload.customer_id,
        notes=payload.notes,
        status="draft"
    )
    db.add(quote)
    db.flush()

    # Generate quote number
    quote.quote_number = f"Q-{quote.id:05d}"

    # Process each line item
    for item_data in payload.items:
        part = db.query(models.Part).options(
            joinedload(models.Part.operations).joinedload(models.Operation.machine),
            joinedload(models.Part.material)
        ).filter(models.Part.id == item_data.part_id).first()

        if not part:
            raise HTTPException(status_code=404, detail=f"Part {item_data.part_id} not found")

        # Calculate costs
        ops = [{
            "setup_time_hr": op.setup_time_hr,
            "cycle_time_hr": op.cycle_time_hr,
            "allowance_pct": op.allowance_pct,
            "machine_rate_per_hr": op.machine.machine_rate_per_hr,
            "labor_rate_per_hr": op.machine.labor_rate_per_hr,
        } for op in part.operations]

        breakdown = calc_unit_cost(
            quantity=item_data.quantity,
            stock_weight_lb=part.stock_weight_lb,
            cost_per_lb=part.material.cost_per_lb,
            scrap_factor=part.scrap_factor,
            ops=ops,
            margin_pct=item_data.margin_pct,
        )

        # Create quote item with calculated values
        quote_item = models.QuoteItem(
            quote_id=quote.id,
            part_id=part.id,
            quantity=item_data.quantity,
            margin_pct=item_data.margin_pct,
            material_cost_unit=breakdown.material_unit,
            machine_cost_unit=breakdown.machine_unit,
            labor_cost_unit=breakdown.labor_unit,
            unit_cost=breakdown.unit_cost,
            unit_price=breakdown.unit_price,
        )
        db.add(quote_item)

    db.commit()
    db.refresh(quote)
    return quote

@router.get("", response_model=List[QuoteResponse])
def list_quotes(db: Session = Depends(get_db)):
    """Get all quotes"""
    return db.query(models.Quote).options(joinedload(models.Quote.items)).all()

@router.get("/{quote_id}", response_model=QuoteResponse)
def get_quote(quote_id: int, db: Session = Depends(get_db)):
    """Get a specific quote with all line items"""
    quote = db.query(models.Quote).options(joinedload(models.Quote.items)).filter(models.Quote.id == quote_id).first()
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    return quote
