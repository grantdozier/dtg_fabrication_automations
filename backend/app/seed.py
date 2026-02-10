"""
Seed database with extensive realistic mock data for demo/testing
"""

from sqlalchemy.orm import Session
from . import models
from .services.quoting import calc_unit_cost

def seed_database(db: Session):
    """Populate database with comprehensive demo data"""

    # Check if already seeded
    if db.query(models.Customer).count() > 0:
        print("Database already seeded, skipping...")
        return

    print("Seeding database with comprehensive mock data...")

    # ==================== CUSTOMERS ====================
    customers = [
        models.Customer(name="Bayou Fabrication LLC", email="ops@bayoufab.com", phone="225-555-0100"),
        models.Customer(name="Delta Manufacturing Co", email="quotes@deltamfg.com", phone="504-555-0101"),
        models.Customer(name="Gulf Coast Machining", email="purchasing@gulfcoast.com", phone="337-555-0102"),
        models.Customer(name="Pelican Precision Parts", email="orders@pelicanparts.com", phone="985-555-0103"),
        models.Customer(name="Crescent City Components", email="sourcing@crescentcity.com", phone="504-555-0104"),
        models.Customer(name="Magnolia Machine Works", email="procurement@magnoliamachine.com", phone="225-555-0105"),
        models.Customer(name="Cajun Custom Fabrication", email="sales@cajuncustom.com", phone="337-555-0106"),
        models.Customer(name="River Bend Industries", email="buyers@riverbend.com", phone="985-555-0107"),
        models.Customer(name="Acadia Aerospace", email="supply@acadiaaero.com", phone="337-555-0108"),
        models.Customer(name="Pontchartrain Prototypes", email="rapid@pontproto.com", phone="504-555-0109"),
        models.Customer(name="Baton Rouge Machining", email="rfq@brmachining.com", phone="225-555-0110"),
        models.Customer(name="Atchafalaya Automation", email="parts@atchauto.com", phone="337-555-0111"),
        models.Customer(name="Vermilion Valve Company", email="orders@vermilionvalve.com", phone="337-555-0112"),
        models.Customer(name="Teche Tool & Die", email="contact@techetool.com", phone="337-555-0113"),
        models.Customer(name="Lafourche Logistics", email="materials@lafourchelogistics.com", phone="985-555-0114"),
    ]

    # ==================== MATERIALS ====================
    materials = [
        models.Material(
            name="6061-T6 Aluminum",
            cost_per_lb=3.75,
            density_lb_in3=0.0975,
            description="General purpose aluminum alloy, excellent machinability and corrosion resistance"
        ),
        models.Material(
            name="7075-T6 Aluminum",
            cost_per_lb=5.20,
            density_lb_in3=0.101,
            description="High-strength aluminum, aerospace applications"
        ),
        models.Material(
            name="1018 Mild Steel",
            cost_per_lb=1.20,
            density_lb_in3=0.283,
            description="Low carbon steel, good for general machining and welding"
        ),
        models.Material(
            name="4140 Alloy Steel",
            cost_per_lb=2.15,
            density_lb_in3=0.283,
            description="Heat treatable steel, high strength and toughness"
        ),
        models.Material(
            name="304 Stainless Steel",
            cost_per_lb=4.50,
            density_lb_in3=0.290,
            description="Corrosion resistant, food grade, more difficult to machine"
        ),
        models.Material(
            name="316 Stainless Steel",
            cost_per_lb=6.25,
            density_lb_in3=0.290,
            description="Marine grade stainless, superior corrosion resistance"
        ),
        models.Material(
            name="Brass (C360)",
            cost_per_lb=7.50,
            density_lb_in3=0.307,
            description="Free-machining brass, excellent for high-volume production"
        ),
        models.Material(
            name="Delrin (Acetal)",
            cost_per_lb=6.80,
            density_lb_in3=0.051,
            description="Engineering plastic, excellent dimensional stability and low friction"
        ),
        models.Material(
            name="UHMW Polyethylene",
            cost_per_lb=5.40,
            density_lb_in3=0.034,
            description="Ultra-high molecular weight plastic, wear resistant"
        ),
        models.Material(
            name="Titanium (Grade 5)",
            cost_per_lb=28.50,
            density_lb_in3=0.163,
            description="High strength-to-weight ratio, aerospace and medical applications"
        ),
    ]

    # ==================== MACHINES ====================
    machines = [
        models.Machine(
            name="Haas VF-2 (3-axis Mill)",
            machine_type="mill",
            machine_rate_per_hr=85.00,
            labor_rate_per_hr=35.00,
            description="40x20x25 work envelope, 8100 RPM spindle, workhorse 3-axis mill"
        ),
        models.Machine(
            name="Haas VF-4 (3-axis Mill)",
            machine_type="mill",
            machine_rate_per_hr=95.00,
            labor_rate_per_hr=35.00,
            description="50x20x25 work envelope, larger capacity"
        ),
        models.Machine(
            name="DMG Mori NHX5000 (5-axis)",
            machine_type="mill",
            machine_rate_per_hr=145.00,
            labor_rate_per_hr=45.00,
            description="High-precision 5-axis machining center, complex geometries"
        ),
        models.Machine(
            name="Doosan Puma 2100 Lathe",
            machine_type="lathe",
            machine_rate_per_hr=95.00,
            labor_rate_per_hr=38.00,
            description="CNC turning center with live tooling, 8-inch chuck"
        ),
        models.Machine(
            name="Mazak Quick Turn 250",
            machine_type="lathe",
            machine_rate_per_hr=105.00,
            labor_rate_per_hr=38.00,
            description="High-speed turning center with sub-spindle"
        ),
        models.Machine(
            name="Haas ST-10 Lathe",
            machine_type="lathe",
            machine_rate_per_hr=75.00,
            labor_rate_per_hr=32.00,
            description="Entry-level CNC lathe, great for simple turned parts"
        ),
    ]

    db.add_all(customers + materials + machines)
    db.flush()

    # ==================== PARTS WITH OPERATIONS ====================
    parts_list = []

    # Part 1: Simple aluminum bracket (with enhanced cost tracking)
    part1 = models.Part(
        part_number="BRKT-001",
        description="Aluminum mounting bracket with 4x thru holes",
        material_id=materials[0].id,  # 6061 Aluminum
        stock_weight_lb=1.2,
        scrap_factor=0.05,
        programming_time_hr=2.5,  # CAM programming time
        programming_rate_per_hr=75.0,  # Programming rate
        first_article_inspection_hr=0.75,  # First article inspection
        overhead_rate_pct=1.5  # 150% overhead
    )
    part1.operations = [
        models.Operation(
            name="Mill Op 10 - Face & Rough",
            sequence=10,
            machine_id=machines[0].id,
            operation_type="roughing",
            setup_time_hr=1.5,
            cycle_time_hr=0.25,
            allowance_pct=0.10,
            tool_change_time_min=3.0,
            inspection_time_min=2.0,
            tool_cost_per_part=0.85,  # Tool wear cost
            consumables_cost_per_part=0.50  # Coolant, etc
        ),
        models.Operation(
            name="Mill Op 20 - Finish & Drill",
            sequence=20,
            machine_id=machines[0].id,
            operation_type="finishing",
            setup_time_hr=0.5,
            cycle_time_hr=0.15,
            allowance_pct=0.08,
            tool_change_time_min=2.0,
            inspection_time_min=3.0,
            tool_cost_per_part=0.65,
            consumables_cost_per_part=0.35
        ),
        models.Operation(
            name="Deburr & Inspect",
            sequence=30,
            machine_id=machines[0].id,
            operation_type="deburr",
            setup_time_hr=0.25,
            cycle_time_hr=0.08,
            allowance_pct=0.05,
            tool_change_time_min=0.0,
            inspection_time_min=5.0,  # Final inspection
            tool_cost_per_part=0.15,  # Deburring tools
            consumables_cost_per_part=0.25  # Abrasives
        ),
    ]
    parts_list.append(part1)

    # Part 2: Precision shaft
    part2 = models.Part(
        part_number="SHAFT-100",
        description="Precision turned shaft, +/- 0.001 tolerance",
        material_id=materials[2].id,  # 1018 Steel
        stock_weight_lb=2.5,
        scrap_factor=0.08,
        programming_time_hr=1.5,
        programming_rate_per_hr=75.0,
        first_article_inspection_hr=0.5,
        overhead_rate_pct=1.5
    )
    part2.operations = [
        models.Operation(name="Lathe Op 10 - Rough Turn", sequence=10, machine_id=machines[3].id,
                        operation_type="roughing",
                        setup_time_hr=1.5, cycle_time_hr=0.25, allowance_pct=0.12,
                        tool_change_time_min=2.5, inspection_time_min=1.5,
                        tool_cost_per_part=0.65, consumables_cost_per_part=0.40),
        models.Operation(name="Lathe Op 20 - Finish Turn", sequence=20, machine_id=machines[3].id,
                        operation_type="finishing",
                        setup_time_hr=0.25, cycle_time_hr=0.18, allowance_pct=0.08,
                        tool_change_time_min=2.0, inspection_time_min=4.0,
                        tool_cost_per_part=0.55, consumables_cost_per_part=0.30),
    ]
    parts_list.append(part2)

    # Part 3: Complex housing (5-axis)
    part3 = models.Part(
        part_number="HOUSING-250",
        description="Complex aluminum housing with internal features",
        material_id=materials[0].id,  # 6061 Aluminum
        stock_weight_lb=8.5,
        scrap_factor=0.12,
        programming_time_hr=8.0,  # Complex 5-axis programming
        programming_rate_per_hr=85.0,  # Senior programmer
        first_article_inspection_hr=1.5,
        overhead_rate_pct=1.6
    )
    part3.operations = [
        models.Operation(name="5-Axis Op 10 - Rough & Semi-finish", sequence=10, machine_id=machines[2].id,
                        operation_type="roughing",
                        setup_time_hr=4.0, cycle_time_hr=1.5, allowance_pct=0.15,
                        tool_change_time_min=5.0, inspection_time_min=3.0,
                        tool_cost_per_part=2.50, consumables_cost_per_part=1.20),
        models.Operation(name="5-Axis Op 20 - Finish", sequence=20, machine_id=machines[2].id,
                        operation_type="finishing",
                        setup_time_hr=0.5, cycle_time_hr=0.75, allowance_pct=0.10,
                        tool_change_time_min=3.0, inspection_time_min=5.0,
                        tool_cost_per_part=1.80, consumables_cost_per_part=0.85),
    ]
    parts_list.append(part3)

    # Part 4: Stainless steel flange
    part4 = models.Part(
        part_number="FLANGE-304",
        description="6-inch 304SS pipe flange with bolt circle",
        material_id=materials[4].id,  # 304 Stainless
        stock_weight_lb=12.0,
        scrap_factor=0.10,
        programming_time_hr=3.0,
        programming_rate_per_hr=75.0,
        first_article_inspection_hr=1.0,
        overhead_rate_pct=1.5
    )
    part4.operations = [
        models.Operation(name="Mill Op 10 - Face & Bore", sequence=10, machine_id=machines[1].id,
                        operation_type="machining",
                        setup_time_hr=2.0, cycle_time_hr=0.85, allowance_pct=0.12,
                        tool_change_time_min=4.0, inspection_time_min=2.5,
                        tool_cost_per_part=1.25, consumables_cost_per_part=0.75),
        models.Operation(name="Mill Op 20 - Drill Bolt Circle", sequence=20, machine_id=machines[1].id,
                        operation_type="machining",
                        setup_time_hr=0.75, cycle_time_hr=0.35, allowance_pct=0.08,
                        tool_change_time_min=2.0, inspection_time_min=3.5,
                        tool_cost_per_part=0.95, consumables_cost_per_part=0.55),
    ]
    parts_list.append(part4)

    # Part 5: Brass bushing
    part5 = models.Part(
        part_number="BUSHING-BR-050",
        description="Brass sleeve bushing, 0.500 ID x 0.750 OD",
        material_id=materials[6].id,  # Brass
        stock_weight_lb=0.35,
        scrap_factor=0.05,
        programming_time_hr=0.5,  # Simple part
        programming_rate_per_hr=75.0,
        first_article_inspection_hr=0.25,
        overhead_rate_pct=1.5
    )
    part5.operations = [
        models.Operation(name="Lathe Op 10 - Turn & Bore", sequence=10, machine_id=machines[5].id,
                        operation_type="machining",
                        setup_time_hr=0.75, cycle_time_hr=0.08, allowance_pct=0.08,
                        tool_change_time_min=1.5, inspection_time_min=2.0,
                        tool_cost_per_part=0.25, consumables_cost_per_part=0.20),
    ]
    parts_list.append(part5)

    # Part 6: Large steel plate
    part6 = models.Part(
        part_number="PLATE-STL-001",
        description="Steel base plate 12x12x1 with pattern of holes",
        material_id=materials[3].id,  # 4140 Steel
        stock_weight_lb=42.0,
        scrap_factor=0.08,
        programming_time_hr=2.0,
        programming_rate_per_hr=75.0,
        first_article_inspection_hr=0.75,
        overhead_rate_pct=1.5
    )
    part6.operations = [
        models.Operation(name="Mill Op 10 - Face Both Sides", sequence=10, machine_id=machines[1].id,
                        operation_type="machining",
                        setup_time_hr=2.5, cycle_time_hr=1.2, allowance_pct=0.10,
                        tool_change_time_min=3.5, inspection_time_min=2.0,
                        tool_cost_per_part=1.40, consumables_cost_per_part=0.80),
        models.Operation(name="Mill Op 20 - Drill & Tap Holes", sequence=20, machine_id=machines[1].id,
                        operation_type="machining",
                        setup_time_hr=1.0, cycle_time_hr=0.65, allowance_pct=0.12,
                        tool_change_time_min=2.5, inspection_time_min=4.0,
                        tool_cost_per_part=1.10, consumables_cost_per_part=0.60),
    ]
    parts_list.append(part6)

    # Part 7: Delrin spacer
    part7 = models.Part(
        part_number="SPACER-DELRIN-025",
        description="Delrin spacer, simple turned part",
        material_id=materials[7].id,  # Delrin
        stock_weight_lb=0.15,
        scrap_factor=0.03,
        programming_time_hr=0.25,  # Very simple
        programming_rate_per_hr=75.0,
        first_article_inspection_hr=0.15,
        overhead_rate_pct=1.4
    )
    part7.operations = [
        models.Operation(name="Lathe Op 10 - Turn", sequence=10, machine_id=machines[5].id,
                        operation_type="machining",
                        setup_time_hr=0.5, cycle_time_hr=0.05, allowance_pct=0.05,
                        tool_change_time_min=1.0, inspection_time_min=1.0,
                        tool_cost_per_part=0.15, consumables_cost_per_part=0.10),
    ]
    parts_list.append(part7)

    # Part 8: Aerospace bracket (7075)
    part8 = models.Part(
        part_number="BRKT-AERO-7075",
        description="High-strength 7075 aircraft bracket",
        material_id=materials[1].id,  # 7075 Aluminum
        stock_weight_lb=3.2,
        scrap_factor=0.10,
        programming_time_hr=6.0,  # Aerospace complexity
        programming_rate_per_hr=85.0,
        first_article_inspection_hr=2.0,  # AS9100 requirements
        overhead_rate_pct=1.7  # Higher overhead for aerospace
    )
    part8.operations = [
        models.Operation(name="5-Axis Op 10 - Rough", sequence=10, machine_id=machines[2].id,
                        operation_type="roughing",
                        setup_time_hr=3.0, cycle_time_hr=0.95, allowance_pct=0.15,
                        tool_change_time_min=4.0, inspection_time_min=2.5,
                        tool_cost_per_part=2.10, consumables_cost_per_part=1.10),
        models.Operation(name="5-Axis Op 20 - Finish", sequence=20, machine_id=machines[2].id,
                        operation_type="finishing",
                        setup_time_hr=0.5, cycle_time_hr=0.55, allowance_pct=0.10,
                        tool_change_time_min=3.0, inspection_time_min=4.0,
                        tool_cost_per_part=1.65, consumables_cost_per_part=0.75),
        models.Operation(name="Deburr", sequence=30, machine_id=machines[0].id,
                        operation_type="deburr",
                        setup_time_hr=0.25, cycle_time_hr=0.15, allowance_pct=0.05,
                        tool_change_time_min=0.0, inspection_time_min=3.0,
                        tool_cost_per_part=0.20, consumables_cost_per_part=0.30),
    ]
    parts_list.append(part8)

    # Part 9: Steel shaft with keyway
    part9 = models.Part(
        part_number="SHAFT-KEY-200",
        description="Steel shaft 2-inch diameter with keyway",
        material_id=materials[3].id,  # 4140 Steel
        stock_weight_lb=8.5,
        scrap_factor=0.08,
        programming_time_hr=1.75,
        programming_rate_per_hr=75.0,
        first_article_inspection_hr=0.5,
        overhead_rate_pct=1.5
    )
    part9.operations = [
        models.Operation(name="Lathe Op 10 - Rough Turn", sequence=10, machine_id=machines[4].id,
                        operation_type="roughing",
                        setup_time_hr=1.75, cycle_time_hr=0.45, allowance_pct=0.10,
                        tool_change_time_min=3.0, inspection_time_min=1.5,
                        tool_cost_per_part=0.95, consumables_cost_per_part=0.55),
        models.Operation(name="Lathe Op 20 - Finish Turn", sequence=20, machine_id=machines[4].id,
                        operation_type="finishing",
                        setup_time_hr=0.25, cycle_time_hr=0.30, allowance_pct=0.08,
                        tool_change_time_min=2.0, inspection_time_min=3.5,
                        tool_cost_per_part=0.75, consumables_cost_per_part=0.40),
        models.Operation(name="Mill Op 30 - Cut Keyway", sequence=30, machine_id=machines[0].id,
                        operation_type="machining",
                        setup_time_hr=1.0, cycle_time_hr=0.20, allowance_pct=0.08,
                        tool_change_time_min=2.0, inspection_time_min=2.5,
                        tool_cost_per_part=0.60, consumables_cost_per_part=0.35),
    ]
    parts_list.append(part9)

    # Part 10: Marine stainless cover
    part10 = models.Part(
        part_number="COVER-316SS",
        description="316 stainless marine cover plate",
        material_id=materials[5].id,  # 316 Stainless
        stock_weight_lb=5.8,
        scrap_factor=0.10,
        programming_time_hr=3.5,
        programming_rate_per_hr=75.0,
        first_article_inspection_hr=0.75,
        overhead_rate_pct=1.5
    )
    part10.operations = [
        models.Operation(name="Mill Op 10 - Contour & Pocket", sequence=10, machine_id=machines[1].id,
                        operation_type="machining",
                        setup_time_hr=2.5, cycle_time_hr=1.1, allowance_pct=0.12,
                        tool_change_time_min=4.5, inspection_time_min=2.5,
                        tool_cost_per_part=1.55, consumables_cost_per_part=0.90),
        models.Operation(name="Mill Op 20 - Drill & Tap", sequence=20, machine_id=machines[0].id,
                        operation_type="machining",
                        setup_time_hr=0.75, cycle_time_hr=0.35, allowance_pct=0.08,
                        tool_change_time_min=2.0, inspection_time_min=3.0,
                        tool_cost_per_part=0.85, consumables_cost_per_part=0.50),
    ]
    parts_list.append(part10)

    # Part 11: Simple aluminum disc
    part11 = models.Part(
        part_number="DISC-AL-100",
        description="Simple aluminum disc, 4-inch diameter",
        material_id=materials[0].id,  # 6061 Aluminum
        stock_weight_lb=1.5,
        scrap_factor=0.05,
        programming_time_hr=0.5,
        programming_rate_per_hr=75.0,
        first_article_inspection_hr=0.25,
        overhead_rate_pct=1.4
    )
    part11.operations = [
        models.Operation(name="Lathe Op 10 - Face & Turn", sequence=10, machine_id=machines[5].id,
                        operation_type="machining",
                        setup_time_hr=0.75, cycle_time_hr=0.12, allowance_pct=0.08,
                        tool_change_time_min=1.5, inspection_time_min=2.0,
                        tool_cost_per_part=0.35, consumables_cost_per_part=0.25),
    ]
    parts_list.append(part11)

    # Part 12: UHMW wear pad
    part12 = models.Part(
        part_number="PAD-UHMW-001",
        description="UHMW wear pad for conveyor",
        material_id=materials[8].id,  # UHMW
        stock_weight_lb=0.85,
        scrap_factor=0.05,
        programming_time_hr=0.75,
        programming_rate_per_hr=75.0,
        first_article_inspection_hr=0.25,
        overhead_rate_pct=1.4
    )
    part12.operations = [
        models.Operation(name="Mill Op 10 - Contour Cut", sequence=10, machine_id=machines[0].id,
                        operation_type="machining",
                        setup_time_hr=1.0, cycle_time_hr=0.18, allowance_pct=0.08,
                        tool_change_time_min=1.5, inspection_time_min=2.0,
                        tool_cost_per_part=0.40, consumables_cost_per_part=0.20),
    ]
    parts_list.append(part12)

    # Part 13: Titanium medical component
    part13 = models.Part(
        part_number="IMPLANT-TI-001",
        description="Titanium medical component (prototype)",
        material_id=materials[9].id,  # Titanium
        stock_weight_lb=0.45,
        scrap_factor=0.15,
        programming_time_hr=12.0,  # Complex medical component
        programming_rate_per_hr=95.0,  # Senior programmer
        first_article_inspection_hr=3.0,  # ISO 13485 requirements
        overhead_rate_pct=2.0  # Higher overhead for medical
    )
    part13.operations = [
        models.Operation(name="5-Axis Op 10 - Complex Contour", sequence=10, machine_id=machines[2].id,
                        operation_type="roughing",
                        setup_time_hr=5.0, cycle_time_hr=2.5, allowance_pct=0.18,
                        tool_change_time_min=6.0, inspection_time_min=5.0,
                        tool_cost_per_part=4.50, consumables_cost_per_part=2.00),
        models.Operation(name="5-Axis Op 20 - Fine Finish", sequence=20, machine_id=machines[2].id,
                        operation_type="finishing",
                        setup_time_hr=1.0, cycle_time_hr=1.2, allowance_pct=0.12,
                        tool_change_time_min=4.0, inspection_time_min=8.0,
                        tool_cost_per_part=3.25, consumables_cost_per_part=1.50),
    ]
    parts_list.append(part13)

    # Part 14: Steel coupling
    part14 = models.Part(
        part_number="COUPLING-STL-150",
        description="Steel flexible coupling, 1.5-inch bore",
        material_id=materials[2].id,  # 1018 Steel
        stock_weight_lb=4.2,
        scrap_factor=0.08,
        programming_time_hr=2.0,
        programming_rate_per_hr=75.0,
        first_article_inspection_hr=0.5,
        overhead_rate_pct=1.5
    )
    part14.operations = [
        models.Operation(name="Lathe Op 10 - Turn OD & Face", sequence=10, machine_id=machines[3].id,
                        operation_type="machining",
                        setup_time_hr=1.5, cycle_time_hr=0.35, allowance_pct=0.10,
                        tool_change_time_min=2.5, inspection_time_min=2.0,
                        tool_cost_per_part=0.70, consumables_cost_per_part=0.45),
        models.Operation(name="Lathe Op 20 - Bore & Groove", sequence=20, machine_id=machines[3].id,
                        operation_type="machining",
                        setup_time_hr=0.5, cycle_time_hr=0.28, allowance_pct=0.08,
                        tool_change_time_min=2.0, inspection_time_min=2.5,
                        tool_cost_per_part=0.55, consumables_cost_per_part=0.35),
        models.Operation(name="Mill Op 30 - Drill Bolt Holes", sequence=30, machine_id=machines[0].id,
                        operation_type="machining",
                        setup_time_hr=0.75, cycle_time_hr=0.15, allowance_pct=0.08,
                        tool_change_time_min=1.5, inspection_time_min=2.0,
                        tool_cost_per_part=0.45, consumables_cost_per_part=0.30),
    ]
    parts_list.append(part14)

    # Part 15: Aluminum heat sink
    part15 = models.Part(
        part_number="HEATSINK-AL-001",
        description="Aluminum heat sink with fin array",
        material_id=materials[0].id,  # 6061 Aluminum
        stock_weight_lb=2.8,
        scrap_factor=0.10,
        programming_time_hr=4.0,
        programming_rate_per_hr=75.0,
        first_article_inspection_hr=0.5,
        overhead_rate_pct=1.5
    )
    part15.operations = [
        models.Operation(name="Mill Op 10 - Rough Fins", sequence=10, machine_id=machines[1].id,
                        operation_type="roughing",
                        setup_time_hr=2.0, cycle_time_hr=0.95, allowance_pct=0.12,
                        tool_change_time_min=3.5, inspection_time_min=2.0,
                        tool_cost_per_part=1.30, consumables_cost_per_part=0.70),
        models.Operation(name="Mill Op 20 - Finish & Drill", sequence=20, machine_id=machines[0].id,
                        operation_type="finishing",
                        setup_time_hr=0.75, cycle_time_hr=0.45, allowance_pct=0.08,
                        tool_change_time_min=2.0, inspection_time_min=3.0,
                        tool_cost_per_part=0.90, consumables_cost_per_part=0.50),
    ]
    parts_list.append(part15)

    # Part 16: Brass valve body
    part16 = models.Part(
        part_number="VALVE-BR-075",
        description="Brass valve body, 3/4 inch NPT",
        material_id=materials[6].id,  # Brass
        stock_weight_lb=1.8,
        scrap_factor=0.08,
        programming_time_hr=2.5,
        programming_rate_per_hr=75.0,
        first_article_inspection_hr=0.75,
        overhead_rate_pct=1.5
    )
    part16.operations = [
        models.Operation(name="Mill Op 10 - Machine Body", sequence=10, machine_id=machines[0].id,
                        operation_type="machining",
                        setup_time_hr=2.0, cycle_time_hr=0.55, allowance_pct=0.10,
                        tool_change_time_min=3.0, inspection_time_min=2.5,
                        tool_cost_per_part=0.95, consumables_cost_per_part=0.55),
        models.Operation(name="Mill Op 20 - Drill & Tap Ports", sequence=20, machine_id=machines[0].id,
                        operation_type="machining",
                        setup_time_hr=1.0, cycle_time_hr=0.40, allowance_pct=0.10,
                        tool_change_time_min=2.0, inspection_time_min=3.5,
                        tool_cost_per_part=0.75, consumables_cost_per_part=0.45),
    ]
    parts_list.append(part16)

    # Part 17: Large steel gear blank
    part17 = models.Part(
        part_number="GEAR-BLANK-400",
        description="4-inch steel gear blank (no teeth cut)",
        material_id=materials[3].id,  # 4140 Steel
        stock_weight_lb=15.5,
        scrap_factor=0.10,
        programming_time_hr=2.0,
        programming_rate_per_hr=75.0,
        first_article_inspection_hr=0.75,
        overhead_rate_pct=1.5
    )
    part17.operations = [
        models.Operation(name="Lathe Op 10 - Turn OD & Bore", sequence=10, machine_id=machines[4].id,
                        operation_type="machining",
                        setup_time_hr=2.0, cycle_time_hr=0.75, allowance_pct=0.10,
                        tool_change_time_min=3.5, inspection_time_min=2.5,
                        tool_cost_per_part=1.20, consumables_cost_per_part=0.65),
        models.Operation(name="Lathe Op 20 - Face & Keyway", sequence=20, machine_id=machines[4].id,
                        operation_type="machining",
                        setup_time_hr=0.5, cycle_time_hr=0.35, allowance_pct=0.08,
                        tool_change_time_min=2.0, inspection_time_min=3.0,
                        tool_cost_per_part=0.85, consumables_cost_per_part=0.45),
    ]
    parts_list.append(part17)

    # Part 18: Delrin guide block
    part18 = models.Part(
        part_number="GUIDE-DELRIN-200",
        description="Delrin guide block with slots",
        material_id=materials[7].id,  # Delrin
        stock_weight_lb=0.95,
        scrap_factor=0.05,
        programming_time_hr=1.0,
        programming_rate_per_hr=75.0,
        first_article_inspection_hr=0.25,
        overhead_rate_pct=1.4
    )
    part18.operations = [
        models.Operation(name="Mill Op 10 - Machine Slots", sequence=10, machine_id=machines[0].id,
                        operation_type="machining",
                        setup_time_hr=1.25, cycle_time_hr=0.30, allowance_pct=0.08,
                        tool_change_time_min=2.0, inspection_time_min=2.5,
                        tool_cost_per_part=0.50, consumables_cost_per_part=0.30),
    ]
    parts_list.append(part18)

    # Part 19: Stainless tube adapter
    part19 = models.Part(
        part_number="ADAPTER-304-100",
        description="304SS tube adapter fitting",
        material_id=materials[4].id,  # 304 Stainless
        stock_weight_lb=1.2,
        scrap_factor=0.08,
        programming_time_hr=1.25,
        programming_rate_per_hr=75.0,
        first_article_inspection_hr=0.5,
        overhead_rate_pct=1.5
    )
    part19.operations = [
        models.Operation(name="Lathe Op 10 - Turn & Thread", sequence=10, machine_id=machines[3].id,
                        operation_type="machining",
                        setup_time_hr=1.5, cycle_time_hr=0.28, allowance_pct=0.10,
                        tool_change_time_min=2.5, inspection_time_min=2.0,
                        tool_cost_per_part=0.70, consumables_cost_per_part=0.40),
        models.Operation(name="Lathe Op 20 - Bore & Finish", sequence=20, machine_id=machines[3].id,
                        operation_type="finishing",
                        setup_time_hr=0.25, cycle_time_hr=0.18, allowance_pct=0.08,
                        tool_change_time_min=1.5, inspection_time_min=3.0,
                        tool_cost_per_part=0.55, consumables_cost_per_part=0.30),
    ]
    parts_list.append(part19)

    # Part 20: Aluminum prototype enclosure
    part20 = models.Part(
        part_number="ENCLOSURE-AL-001",
        description="Custom aluminum electronics enclosure",
        material_id=materials[0].id,  # 6061 Aluminum
        stock_weight_lb=6.5,
        scrap_factor=0.12,
        programming_time_hr=5.5,
        programming_rate_per_hr=75.0,
        first_article_inspection_hr=1.0,
        overhead_rate_pct=1.6
    )
    part20.operations = [
        models.Operation(name="Mill Op 10 - Rough Pocket", sequence=10, machine_id=machines[1].id,
                        operation_type="roughing",
                        setup_time_hr=3.0, cycle_time_hr=1.8, allowance_pct=0.12,
                        tool_change_time_min=4.0, inspection_time_min=2.5,
                        tool_cost_per_part=1.85, consumables_cost_per_part=1.00),
        models.Operation(name="Mill Op 20 - Finish & Drill", sequence=20, machine_id=machines[1].id,
                        operation_type="finishing",
                        setup_time_hr=0.75, cycle_time_hr=0.95, allowance_pct=0.10,
                        tool_change_time_min=2.5, inspection_time_min=3.5,
                        tool_cost_per_part=1.30, consumables_cost_per_part=0.70),
        models.Operation(name="Deburr & Polish", sequence=30, machine_id=machines[0].id,
                        operation_type="deburr",
                        setup_time_hr=0.5, cycle_time_hr=0.25, allowance_pct=0.05,
                        tool_change_time_min=0.0, inspection_time_min=4.0,
                        tool_cost_per_part=0.30, consumables_cost_per_part=0.45),
    ]
    parts_list.append(part20)

    db.add_all(parts_list)
    db.flush()

    # ==================== PRE-CREATED QUOTES ====================
    quotes_list = []

    # Quote 1: Bayou Fab - Simple bracket order
    quote1 = models.Quote(
        customer_id=customers[0].id,
        quote_number="Q-00001",
        status="sent",
        notes="100 piece production run, requested lead time 2 weeks"
    )
    breakdown1 = calc_unit_cost(
        quantity=100,
        stock_weight_lb=part1.stock_weight_lb,
        cost_per_lb=materials[0].cost_per_lb,
        scrap_factor=part1.scrap_factor,
        ops=[{
            "setup_time_hr": op.setup_time_hr,
            "cycle_time_hr": op.cycle_time_hr,
            "allowance_pct": op.allowance_pct,
            "machine_rate_per_hr": machines[0].machine_rate_per_hr,
            "labor_rate_per_hr": machines[0].labor_rate_per_hr,
        } for op in part1.operations],
        margin_pct=0.15
    )
    quote1.items = [models.QuoteItem(
        part_id=part1.id,
        quantity=100,
        margin_pct=0.15,
        material_cost_unit=breakdown1.material_unit,
        machine_cost_unit=breakdown1.machine_unit,
        labor_cost_unit=breakdown1.labor_unit,
        unit_cost=breakdown1.unit_cost,
        unit_price=breakdown1.unit_price
    )]
    quotes_list.append(quote1)

    # Quote 2: Delta Mfg - Multiple parts
    quote2 = models.Quote(
        customer_id=customers[1].id,
        quote_number="Q-00002",
        status="draft",
        notes="Prototype quote for 3 different parts, customer wants budget pricing"
    )
    # Add BRKT-001
    breakdown2a = calc_unit_cost(
        quantity=25,
        stock_weight_lb=part1.stock_weight_lb,
        cost_per_lb=materials[0].cost_per_lb,
        scrap_factor=part1.scrap_factor,
        ops=[{
            "setup_time_hr": op.setup_time_hr,
            "cycle_time_hr": op.cycle_time_hr,
            "allowance_pct": op.allowance_pct,
            "machine_rate_per_hr": machines[0].machine_rate_per_hr,
            "labor_rate_per_hr": machines[0].labor_rate_per_hr,
        } for op in part1.operations],
        margin_pct=0.20
    )
    # Add SHAFT-100
    breakdown2b = calc_unit_cost(
        quantity=50,
        stock_weight_lb=part2.stock_weight_lb,
        cost_per_lb=materials[2].cost_per_lb,
        scrap_factor=part2.scrap_factor,
        ops=[{
            "setup_time_hr": op.setup_time_hr,
            "cycle_time_hr": op.cycle_time_hr,
            "allowance_pct": op.allowance_pct,
            "machine_rate_per_hr": machines[3].machine_rate_per_hr,
            "labor_rate_per_hr": machines[3].labor_rate_per_hr,
        } for op in part2.operations],
        margin_pct=0.20
    )
    quote2.items = [
        models.QuoteItem(
            part_id=part1.id, quantity=25, margin_pct=0.20,
            material_cost_unit=breakdown2a.material_unit,
            machine_cost_unit=breakdown2a.machine_unit,
            labor_cost_unit=breakdown2a.labor_unit,
            unit_cost=breakdown2a.unit_cost,
            unit_price=breakdown2a.unit_price
        ),
        models.QuoteItem(
            part_id=part2.id, quantity=50, margin_pct=0.20,
            material_cost_unit=breakdown2b.material_unit,
            machine_cost_unit=breakdown2b.machine_unit,
            labor_cost_unit=breakdown2b.labor_unit,
            unit_cost=breakdown2b.unit_cost,
            unit_price=breakdown2b.unit_price
        )
    ]
    quotes_list.append(quote2)

    # Quote 3: Acadia Aerospace - High-value 5-axis part
    quote3 = models.Quote(
        customer_id=customers[8].id,
        quote_number="Q-00003",
        status="approved",
        notes="Aerospace bracket, AS9100 quality requirements, material cert required"
    )
    breakdown3 = calc_unit_cost(
        quantity=50,
        stock_weight_lb=part8.stock_weight_lb,
        cost_per_lb=materials[1].cost_per_lb,
        scrap_factor=part8.scrap_factor,
        ops=[{
            "setup_time_hr": op.setup_time_hr,
            "cycle_time_hr": op.cycle_time_hr,
            "allowance_pct": op.allowance_pct,
            "machine_rate_per_hr": machines[2].machine_rate_per_hr if op.sequence < 30 else machines[0].machine_rate_per_hr,
            "labor_rate_per_hr": machines[2].labor_rate_per_hr if op.sequence < 30 else machines[0].labor_rate_per_hr,
        } for op in part8.operations],
        margin_pct=0.25
    )
    quote3.items = [models.QuoteItem(
        part_id=part8.id,
        quantity=50,
        margin_pct=0.25,
        material_cost_unit=breakdown3.material_unit,
        machine_cost_unit=breakdown3.machine_unit,
        labor_cost_unit=breakdown3.labor_unit,
        unit_cost=breakdown3.unit_cost,
        unit_price=breakdown3.unit_price
    )]
    quotes_list.append(quote3)

    # Quote 4: Gulf Coast - Stainless flanges
    quote4 = models.Quote(
        customer_id=customers[2].id,
        quote_number="Q-00004",
        status="sent",
        notes="Repeat customer, marine application, need by end of month"
    )
    breakdown4 = calc_unit_cost(
        quantity=20,
        stock_weight_lb=part4.stock_weight_lb,
        cost_per_lb=materials[4].cost_per_lb,
        scrap_factor=part4.scrap_factor,
        ops=[{
            "setup_time_hr": op.setup_time_hr,
            "cycle_time_hr": op.cycle_time_hr,
            "allowance_pct": op.allowance_pct,
            "machine_rate_per_hr": machines[1].machine_rate_per_hr,
            "labor_rate_per_hr": machines[1].labor_rate_per_hr,
        } for op in part4.operations],
        margin_pct=0.18
    )
    quote4.items = [models.QuoteItem(
        part_id=part4.id,
        quantity=20,
        margin_pct=0.18,
        material_cost_unit=breakdown4.material_unit,
        machine_cost_unit=breakdown4.machine_unit,
        labor_cost_unit=breakdown4.labor_unit,
        unit_cost=breakdown4.unit_cost,
        unit_price=breakdown4.unit_price
    )]
    quotes_list.append(quote4)

    # Quote 5: Pelican Parts - High volume brass bushings
    quote5 = models.Quote(
        customer_id=customers[3].id,
        quote_number="Q-00005",
        status="sent",
        notes="High volume quote, customer is price shopping"
    )
    breakdown5 = calc_unit_cost(
        quantity=500,
        stock_weight_lb=part5.stock_weight_lb,
        cost_per_lb=materials[6].cost_per_lb,
        scrap_factor=part5.scrap_factor,
        ops=[{
            "setup_time_hr": op.setup_time_hr,
            "cycle_time_hr": op.cycle_time_hr,
            "allowance_pct": op.allowance_pct,
            "machine_rate_per_hr": machines[5].machine_rate_per_hr,
            "labor_rate_per_hr": machines[5].labor_rate_per_hr,
        } for op in part5.operations],
        margin_pct=0.12
    )
    quote5.items = [models.QuoteItem(
        part_id=part5.id,
        quantity=500,
        margin_pct=0.12,
        material_cost_unit=breakdown5.material_unit,
        machine_cost_unit=breakdown5.machine_unit,
        labor_cost_unit=breakdown5.labor_unit,
        unit_cost=breakdown5.unit_cost,
        unit_price=breakdown5.unit_price
    )]
    quotes_list.append(quote5)

    # Quote 6: Pontchartrain Prototypes - Titanium medical part
    quote6 = models.Quote(
        customer_id=customers[9].id,
        quote_number="Q-00006",
        status="draft",
        notes="Medical prototype, extremely tight tolerances, ISO 13485 quality system"
    )
    breakdown6 = calc_unit_cost(
        quantity=10,
        stock_weight_lb=part13.stock_weight_lb,
        cost_per_lb=materials[9].cost_per_lb,
        scrap_factor=part13.scrap_factor,
        ops=[{
            "setup_time_hr": op.setup_time_hr,
            "cycle_time_hr": op.cycle_time_hr,
            "allowance_pct": op.allowance_pct,
            "machine_rate_per_hr": machines[2].machine_rate_per_hr,
            "labor_rate_per_hr": machines[2].labor_rate_per_hr,
        } for op in part13.operations],
        margin_pct=0.30
    )
    quote6.items = [models.QuoteItem(
        part_id=part13.id,
        quantity=10,
        margin_pct=0.30,
        material_cost_unit=breakdown6.material_unit,
        machine_cost_unit=breakdown6.machine_unit,
        labor_cost_unit=breakdown6.labor_unit,
        unit_cost=breakdown6.unit_cost,
        unit_price=breakdown6.unit_price
    )]
    quotes_list.append(quote6)

    # Quote 7: Vermilion Valve - Multiple valve bodies
    quote7 = models.Quote(
        customer_id=customers[12].id,
        quote_number="Q-00007",
        status="approved",
        notes="Production order for brass valve bodies, need COC and material certs"
    )
    breakdown7 = calc_unit_cost(
        quantity=200,
        stock_weight_lb=part16.stock_weight_lb,
        cost_per_lb=materials[6].cost_per_lb,
        scrap_factor=part16.scrap_factor,
        ops=[{
            "setup_time_hr": op.setup_time_hr,
            "cycle_time_hr": op.cycle_time_hr,
            "allowance_pct": op.allowance_pct,
            "machine_rate_per_hr": machines[0].machine_rate_per_hr,
            "labor_rate_per_hr": machines[0].labor_rate_per_hr,
        } for op in part16.operations],
        margin_pct=0.15
    )
    quote7.items = [models.QuoteItem(
        part_id=part16.id,
        quantity=200,
        margin_pct=0.15,
        material_cost_unit=breakdown7.material_unit,
        machine_cost_unit=breakdown7.machine_unit,
        labor_cost_unit=breakdown7.labor_unit,
        unit_cost=breakdown7.unit_cost,
        unit_price=breakdown7.unit_price
    )]
    quotes_list.append(quote7)

    db.add_all(quotes_list)
    db.commit()

    print("✓ Database seeded successfully with comprehensive demo data!")
    print(f"  - {len(customers)} customers")
    print(f"  - {len(materials)} materials")
    print(f"  - {len(machines)} machines")
    print(f"  - {len(parts_list)} parts with operations")
    print(f"  - {len(quotes_list)} pre-created quotes")

if __name__ == "__main__":
    from .db import SessionLocal
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
