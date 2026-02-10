from sqlalchemy import String, Integer, Float, ForeignKey, DateTime, func, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from datetime import datetime
from .db import Base

class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(200))
    phone: Mapped[Optional[str]] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    quotes: Mapped[list["Quote"]] = relationship("Quote", back_populates="customer")

class Material(Base):
    __tablename__ = "materials"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    cost_per_lb: Mapped[float] = mapped_column(Float, nullable=False)
    density_lb_in3: Mapped[float] = mapped_column(Float, nullable=False, default=0.283)  # steel default
    description: Mapped[Optional[str]] = mapped_column(String(400))

    parts: Mapped[list["Part"]] = relationship("Part", back_populates="material")

class Machine(Base):
    __tablename__ = "machines"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    machine_type: Mapped[str] = mapped_column(String(50), nullable=False, default="mill")  # mill, lathe, etc.
    machine_rate_per_hr: Mapped[float] = mapped_column(Float, nullable=False)
    labor_rate_per_hr: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(400))

    operations: Mapped[list["Operation"]] = relationship("Operation", back_populates="machine")

class Part(Base):
    __tablename__ = "parts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    part_number: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(String(400))
    material_id: Mapped[int] = mapped_column(ForeignKey("materials.id"), nullable=False)

    # Material estimation inputs
    stock_weight_lb: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    scrap_factor: Mapped[float] = mapped_column(Float, nullable=False, default=0.05)  # 5%

    # Enhanced cost tracking (Rule 2, 3)
    programming_time_hr: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)  # CAM/programming time
    programming_rate_per_hr: Mapped[float] = mapped_column(Float, nullable=False, default=75.0)  # Programming labor rate
    first_article_inspection_hr: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)  # One-time FAI
    overhead_rate_pct: Mapped[float] = mapped_column(Float, nullable=False, default=1.5)  # 150% overhead multiplier

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    material: Mapped["Material"] = relationship("Material", back_populates="parts")
    operations: Mapped[list["Operation"]] = relationship("Operation", back_populates="part", cascade="all, delete-orphan")
    quote_items: Mapped[list["QuoteItem"]] = relationship("QuoteItem", back_populates="part")

class Operation(Base):
    __tablename__ = "operations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    part_id: Mapped[int] = mapped_column(ForeignKey("parts.id"), nullable=False)
    machine_id: Mapped[int] = mapped_column(ForeignKey("machines.id"), nullable=False)

    name: Mapped[str] = mapped_column(String(120), nullable=False)
    sequence: Mapped[int] = mapped_column(Integer, nullable=False, default=10)  # op 10, 20, 30...
    setup_time_hr: Mapped[float] = mapped_column(Float, nullable=False, default=0.5)   # one-time
    cycle_time_hr: Mapped[float] = mapped_column(Float, nullable=False, default=0.25)  # per part
    allowance_pct: Mapped[float] = mapped_column(Float, nullable=False, default=0.10)  # 10%

    # Enhanced operation tracking (Rule 2, 3)
    operation_type: Mapped[str] = mapped_column(String(20), nullable=False, default="machining")  # roughing, finishing, inspection, deburr
    tool_cost_per_part: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)  # Tooling cost allocation
    tool_change_time_min: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)  # Tool change time
    inspection_time_min: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)  # In-process inspection
    consumables_cost_per_part: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)  # Coolant, abrasives

    part: Mapped["Part"] = relationship("Part", back_populates="operations")
    machine: Mapped["Machine"] = relationship("Machine", back_populates="operations")

class Quote(Base):
    __tablename__ = "quotes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False)
    quote_number: Mapped[Optional[str]] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="draft")  # draft, sent, approved
    notes: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    customer: Mapped["Customer"] = relationship("Customer", back_populates="quotes")
    items: Mapped[list["QuoteItem"]] = relationship("QuoteItem", back_populates="quote", cascade="all, delete-orphan")

class QuoteItem(Base):
    __tablename__ = "quote_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quote_id: Mapped[int] = mapped_column(ForeignKey("quotes.id"), nullable=False)
    part_id: Mapped[int] = mapped_column(ForeignKey("parts.id"), nullable=False)

    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    margin_pct: Mapped[float] = mapped_column(Float, nullable=False, default=0.15)

    # Stored computed results (for audit/historical accuracy)
    material_cost_unit: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    machine_cost_unit: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    labor_cost_unit: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    unit_cost: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    unit_price: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    # Enhanced breakdown fields (Rule 2, 3, 4)
    tooling_cost_unit: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    programming_cost_unit: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    inspection_cost_unit: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    consumables_cost_unit: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    overhead_cost_unit: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    # Time breakdown fields (Rule 2)
    setup_time_per_part: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    cycle_time_per_part: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    allowance_time_per_part: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    total_time_per_part: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    quote: Mapped["Quote"] = relationship("Quote", back_populates="items")
    part: Mapped["Part"] = relationship("Part", back_populates="quote_items")
