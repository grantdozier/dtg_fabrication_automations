from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from ..db import get_db
from .. import models

router = APIRouter(prefix="/api/customers", tags=["customers"])

class CustomerCreate(BaseModel):
    name: str
    email: str | None = None
    phone: str | None = None

class CustomerResponse(BaseModel):
    id: int
    name: str
    email: str | None
    phone: str | None

    class Config:
        from_attributes = True

@router.get("", response_model=List[CustomerResponse])
def list_customers(db: Session = Depends(get_db)):
    """Get all customers"""
    return db.query(models.Customer).all()

@router.post("", response_model=CustomerResponse)
def create_customer(payload: CustomerCreate, db: Session = Depends(get_db)):
    """Create a new customer"""
    customer = models.Customer(**payload.model_dump())
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer

@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    """Get a specific customer"""
    customer = db.get(models.Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer
