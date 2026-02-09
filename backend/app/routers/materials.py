from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from ..db import get_db
from .. import models

router = APIRouter(prefix="/api/materials", tags=["materials"])

class MaterialCreate(BaseModel):
    name: str
    cost_per_lb: float
    density_lb_in3: float = 0.283
    description: str | None = None

class MaterialResponse(BaseModel):
    id: int
    name: str
    cost_per_lb: float
    density_lb_in3: float
    description: str | None

    class Config:
        from_attributes = True

@router.get("", response_model=List[MaterialResponse])
def list_materials(db: Session = Depends(get_db)):
    """Get all materials"""
    return db.query(models.Material).all()

@router.post("", response_model=MaterialResponse)
def create_material(payload: MaterialCreate, db: Session = Depends(get_db)):
    """Create a new material"""
    material = models.Material(**payload.model_dump())
    db.add(material)
    db.commit()
    db.refresh(material)
    return material

@router.get("/{material_id}", response_model=MaterialResponse)
def get_material(material_id: int, db: Session = Depends(get_db)):
    """Get a specific material"""
    material = db.get(models.Material, material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    return material
