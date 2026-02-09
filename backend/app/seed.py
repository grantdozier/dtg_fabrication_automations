"""
Seed database with realistic mock data for demo/testing
"""

from sqlalchemy.orm import Session
from . import models

def seed_database(db: Session):
    """Populate database with demo data"""

    # Check if already seeded
    if db.query(models.Customer).count() > 0:
        print("Database already seeded, skipping...")
        return

    print("Seeding database with mock data...")

    # Customers
    customers = [
        models.Customer(name="Bayou Fabrication LLC", email="ops@bayoufab.com", phone="555-0100"),
        models.Customer(name="Delta Manufacturing", email="quotes@deltamfg.com", phone="555-0101"),
        models.Customer(name="Gulf Coast Machining", email="purchasing@gulfcoast.com", phone="555-0102"),
    ]

    # Materials
    materials = [
        models.Material(
            name="6061-T6 Aluminum",
            cost_per_lb=3.75,
            density_lb_in3=0.0975,
            description="General purpose aluminum alloy, excellent machinability"
        ),
        models.Material(
            name="1018 Steel",
            cost_per_lb=1.20,
            density_lb_in3=0.283,
            description="Low carbon steel, good for general machining"
        ),
        models.Material(
            name="304 Stainless Steel",
            cost_per_lb=4.50,
            density_lb_in3=0.290,
            description="Corrosion resistant, more difficult to machine"
        ),
        models.Material(
            name="Delrin (Acetal)",
            cost_per_lb=6.80,
            density_lb_in3=0.051,
            description="Engineering plastic, excellent dimensional stability"
        ),
    ]

    # Machines
    machines = [
        models.Machine(
            name="Haas VF-2 (3-axis Mill)",
            machine_type="mill",
            machine_rate_per_hr=85.00,
            labor_rate_per_hr=35.00,
            description="40x20x25 work envelope, 8100 RPM spindle"
        ),
        models.Machine(
            name="DMG Mori NHX5000 (5-axis)",
            machine_type="mill",
            machine_rate_per_hr=145.00,
            labor_rate_per_hr=45.00,
            description="High-precision 5-axis machining center"
        ),
        models.Machine(
            name="Doosan Puma 2100 Lathe",
            machine_type="lathe",
            machine_rate_per_hr=95.00,
            labor_rate_per_hr=38.00,
            description="CNC turning center with live tooling"
        ),
    ]

    db.add_all(customers + materials + machines)
    db.flush()

    # Parts with operations
    # Part 1: Simple bracket
    part1 = models.Part(
        part_number="BRKT-001",
        description="Aluminum mounting bracket with 4x holes",
        material_id=materials[0].id,  # 6061 Aluminum
        stock_weight_lb=1.2,
        scrap_factor=0.05
    )
    part1.operations = [
        models.Operation(
            name="Mill Op 10 - Face & Rough",
            sequence=10,
            machine_id=machines[0].id,  # Haas VF-2
            setup_time_hr=2.0,
            cycle_time_hr=0.30,
            allowance_pct=0.10
        ),
        models.Operation(
            name="Mill Op 20 - Finish & Drill",
            sequence=20,
            machine_id=machines[0].id,
            setup_time_hr=0.5,
            cycle_time_hr=0.15,
            allowance_pct=0.08
        ),
        models.Operation(
            name="Deburr & Inspect",
            sequence=30,
            machine_id=machines[0].id,
            setup_time_hr=0.25,
            cycle_time_hr=0.08,
            allowance_pct=0.05
        ),
    ]

    # Part 2: Precision shaft
    part2 = models.Part(
        part_number="SHAFT-100",
        description="Turned shaft with tight tolerances",
        material_id=materials[1].id,  # 1018 Steel
        stock_weight_lb=2.5,
        scrap_factor=0.08
    )
    part2.operations = [
        models.Operation(
            name="Lathe Op 10 - Rough Turn",
            sequence=10,
            machine_id=machines[2].id,  # Doosan Lathe
            setup_time_hr=1.5,
            cycle_time_hr=0.25,
            allowance_pct=0.12
        ),
        models.Operation(
            name="Lathe Op 20 - Finish Turn",
            sequence=20,
            machine_id=machines[2].id,
            setup_time_hr=0.25,
            cycle_time_hr=0.18,
            allowance_pct=0.08
        ),
    ]

    # Part 3: Complex housing (5-axis)
    part3 = models.Part(
        part_number="HOUSING-250",
        description="Complex aluminum housing with internal features",
        material_id=materials[0].id,  # 6061 Aluminum
        stock_weight_lb=8.5,
        scrap_factor=0.12
    )
    part3.operations = [
        models.Operation(
            name="5-Axis Op 10 - Rough & Semi-finish",
            sequence=10,
            machine_id=machines[1].id,  # 5-axis
            setup_time_hr=4.0,
            cycle_time_hr=1.5,
            allowance_pct=0.15
        ),
        models.Operation(
            name="5-Axis Op 20 - Finish",
            sequence=20,
            machine_id=machines[1].id,
            setup_time_hr=0.5,
            cycle_time_hr=0.75,
            allowance_pct=0.10
        ),
    ]

    db.add_all([part1, part2, part3])
    db.commit()

    print("✓ Database seeded successfully!")
    print(f"  - {len(customers)} customers")
    print(f"  - {len(materials)} materials")
    print(f"  - {len(machines)} machines")
    print(f"  - 3 parts with operations")

if __name__ == "__main__":
    from .db import SessionLocal
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
