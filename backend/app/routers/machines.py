from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from ..db import get_db
from .. import models

router = APIRouter(prefix="/api/machines", tags=["machines"])

class MachineCreate(BaseModel):
    name: str
    machine_type: str = "mill"
    machine_rate_per_hr: float
    labor_rate_per_hr: float
    description: str | None = None

class MachineResponse(BaseModel):
    id: int
    name: str
    machine_type: str
    machine_rate_per_hr: float
    labor_rate_per_hr: float
    description: str | None

    class Config:
        from_attributes = True

@router.get("", response_model=List[MachineResponse])
def list_machines(db: Session = Depends(get_db)):
    """Get all machines"""
    return db.query(models.Machine).all()

@router.post("", response_model=MachineResponse)
def create_machine(payload: MachineCreate, db: Session = Depends(get_db)):
    """Create a new machine"""
    machine = models.Machine(**payload.model_dump())
    db.add(machine)
    db.commit()
    db.refresh(machine)
    return machine

@router.get("/{machine_id}", response_model=MachineResponse)
def get_machine(machine_id: int, db: Session = Depends(get_db)):
    """Get a specific machine"""
    machine = db.get(models.Machine, machine_id)
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    return machine
