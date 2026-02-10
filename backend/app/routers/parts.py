from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from pydantic import BaseModel
from ..db import get_db
from .. import models

router = APIRouter(prefix="/api/parts", tags=["parts"])

class OperationCreate(BaseModel):
    machine_id: int
    name: str
    sequence: int = 10
    setup_time_hr: float = 0.5
    cycle_time_hr: float = 0.25
    allowance_pct: float = 0.10
    # Enhanced fields
    operation_type: str = "machining"
    tool_cost_per_part: float = 0.0
    tool_change_time_min: float = 0.0
    inspection_time_min: float = 0.0
    consumables_cost_per_part: float = 0.0

class OperationResponse(BaseModel):
    id: int
    machine_id: int
    name: str
    sequence: int
    setup_time_hr: float
    cycle_time_hr: float
    allowance_pct: float
    operation_type: str
    tool_cost_per_part: float
    tool_change_time_min: float
    inspection_time_min: float
    consumables_cost_per_part: float

    class Config:
        from_attributes = True

class PartCreate(BaseModel):
    part_number: str
    description: str | None = None
    material_id: int
    stock_weight_lb: float = 1.0
    scrap_factor: float = 0.05
    # Enhanced fields
    programming_time_hr: float = 0.0
    programming_rate_per_hr: float = 75.0
    first_article_inspection_hr: float = 0.0
    overhead_rate_pct: float = 1.5
    operations: List[OperationCreate] = []

class PartUpdate(BaseModel):
    part_number: str | None = None
    description: str | None = None
    material_id: int | None = None
    stock_weight_lb: float | None = None
    scrap_factor: float | None = None
    programming_time_hr: float | None = None
    programming_rate_per_hr: float | None = None
    first_article_inspection_hr: float | None = None
    overhead_rate_pct: float | None = None

class PartResponse(BaseModel):
    id: int
    part_number: str
    description: str | None
    material_id: int
    stock_weight_lb: float
    scrap_factor: float
    programming_time_hr: float
    programming_rate_per_hr: float
    first_article_inspection_hr: float
    overhead_rate_pct: float
    operations: List[OperationResponse] = []

    class Config:
        from_attributes = True

@router.get("", response_model=List[PartResponse])
def list_parts(db: Session = Depends(get_db)):
    """Get all parts with operations"""
    return db.query(models.Part).options(joinedload(models.Part.operations)).all()

@router.post("", response_model=PartResponse)
def create_part(payload: PartCreate, db: Session = Depends(get_db)):
    """Create a new part with operations"""

    # Check if part number already exists
    existing = db.query(models.Part).filter(models.Part.part_number == payload.part_number).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Part number {payload.part_number} already exists")

    # Create part
    part_data = payload.model_dump(exclude={"operations"})
    part = models.Part(**part_data)
    db.add(part)
    db.flush()

    # Create operations
    for op_data in payload.operations:
        operation = models.Operation(part_id=part.id, **op_data.model_dump())
        db.add(operation)

    db.commit()
    db.refresh(part)
    return part

@router.get("/{part_id}", response_model=PartResponse)
def get_part(part_id: int, db: Session = Depends(get_db)):
    """Get a specific part with operations"""
    part = db.query(models.Part).options(joinedload(models.Part.operations)).filter(models.Part.id == part_id).first()
    if not part:
        raise HTTPException(status_code=404, detail="Part not found")
    return part

@router.put("/{part_id}", response_model=PartResponse)
def update_part(part_id: int, payload: PartUpdate, db: Session = Depends(get_db)):
    """Update an existing part"""
    part = db.query(models.Part).filter(models.Part.id == part_id).first()
    if not part:
        raise HTTPException(status_code=404, detail="Part not found")

    # Update only provided fields
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(part, field, value)

    db.commit()
    db.refresh(part)
    return part

@router.put("/{part_id}/operations/{operation_id}")
def update_operation(part_id: int, operation_id: int, payload: OperationCreate, db: Session = Depends(get_db)):
    """Update an existing operation"""
    operation = db.query(models.Operation).filter(
        models.Operation.id == operation_id,
        models.Operation.part_id == part_id
    ).first()

    if not operation:
        raise HTTPException(status_code=404, detail="Operation not found")

    # Update all fields
    update_data = payload.model_dump()
    for field, value in update_data.items():
        setattr(operation, field, value)

    db.commit()
    db.refresh(operation)
    return operation
