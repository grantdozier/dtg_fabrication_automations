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

class OperationResponse(BaseModel):
    id: int
    machine_id: int
    name: str
    sequence: int
    setup_time_hr: float
    cycle_time_hr: float
    allowance_pct: float

    class Config:
        from_attributes = True

class PartCreate(BaseModel):
    part_number: str
    description: str | None = None
    material_id: int
    stock_weight_lb: float = 1.0
    scrap_factor: float = 0.05
    operations: List[OperationCreate] = []

class PartResponse(BaseModel):
    id: int
    part_number: str
    description: str | None
    material_id: int
    stock_weight_lb: float
    scrap_factor: float
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
