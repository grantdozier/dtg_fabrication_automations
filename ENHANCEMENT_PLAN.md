# CNC Quoting System Enhancement Plan

## Based on Professional Machine Shop Research

### Current State (What We Have)
✅ Basic quoting functionality
✅ Material, machine, labor costs
✅ Setup time amortization
✅ Simple margin calculation

### Target State (Industry Standard)
🎯 Detailed time breakdown with all components
🎯 Complete cost itemization
🎯 Professional quote presentation
🎯 Volume pricing tiers
🎯 Rush charge calculator
🎯 Tool cost per part
🎯 Inspection time tracking

---

## Phase 1: Enhanced Data Model (Database)

### 1.1 Operation Enhancements
```python
class Operation:
    # EXISTING
    setup_time_hr
    cycle_time_hr
    allowance_pct

    # NEW FIELDS
    operation_type: enum['roughing', 'finishing', 'inspection', 'deburr']
    tool_cost_per_part: float  # Tooling cost allocation
    programming_time_hr: float  # CAM/programming time
    tool_change_time_min: float  # Tool change time
    inspection_time_min: float  # In-process inspection
```

### 1.2 Part Enhancements
```python
class Part:
    # NEW FIELDS
    first_article_inspection_hr: float  # One-time FAI
    cam_programming_hr: float  # Programming labor
    fixture_cost: float  # Custom fixture cost
    fixture_life_parts: int  # Amortize over N parts
```

### 1.3 Quote Item Enhancements
```python
class QuoteItem:
    # NEW BREAKDOWN FIELDS
    tool_cost_unit: float
    programming_cost_unit: float
    inspection_cost_unit: float
    consumables_cost_unit: float
    fixture_cost_unit: float
    overhead_cost_unit: float

    # TIME BREAKDOWN
    total_setup_time_hr: float
    total_cycle_time_hr: float
    total_allowance_time_hr: float
    total_inspection_time_hr: float
```

### 1.4 Volume Pricing
```python
class VolumePriceTier:
    part_id: int
    min_quantity: int
    max_quantity: int
    unit_price: float
    notes: str
```

### 1.5 Rush Charges
```python
class QuoteModifier:
    quote_id: int
    modifier_type: enum['rush', 'expedite', 'overtime']
    multiplier: float  # 1.5x, 2.0x, etc.
    flat_fee: float  # or fixed amount
    description: str
```

---

## Phase 2: Enhanced Calculation Engine

### 2.1 Detailed Time Calculation
```python
def calc_detailed_time_breakdown(operation, quantity):
    """
    Returns:
    {
        'setup_per_part': float,
        'cycle_time': float,
        'allowance_time': float,
        'tool_change_time': float,
        'inspection_time': float,
        'total_time_per_part': float
    }
    """
```

### 2.2 Complete Cost Breakdown
```python
def calc_comprehensive_cost(part, quantity, margin_pct):
    """
    Returns detailed breakdown:
    - Material (stock + scrap + cutoff waste)
    - Machine time by operation
    - Labor by operation
    - Tooling cost per part
    - Programming (amortized)
    - Inspection (first article + in-process)
    - Consumables (coolant, abrasives)
    - Fixtures (NRE or amortized)
    - Overhead
    - Total cost
    - Margin
    - Final price
    """
```

### 2.3 Volume Pricing Calculator
```python
def calc_volume_pricing(part, quantities=[1, 10, 50, 100, 250, 500]):
    """
    Calculate prices at different quantity breaks
    Show how setup amortization affects unit cost
    """
```

---

## Phase 3: UI Enhancements

### 3.1 Detailed Cost Breakdown Component
```
┌─────────────────────────────────────────────────────────────┐
│ QUOTE BREAKDOWN - Part: BRKT-001 | Qty: 100                │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│ TIME BREAKDOWN                                                │
│   Setup (amortized):      0.025 hr/pc   $ 1.88/pc          │
│   Cycle time:             0.300 hr/pc   $22.50/pc          │
│   Allowance (10%):        0.030 hr/pc   $ 2.25/pc          │
│   Tool changes:           0.015 hr/pc   $ 1.13/pc          │
│   Inspection:             0.080 hr/pc   $ 6.00/pc          │
│   ─────────────────────────────────────────────────────      │
│   Total machine time:     0.450 hr/pc   $33.76/pc          │
│                                                               │
│ COST BREAKDOWN                                                │
│   Material:                             $ 4.73/pc           │
│     └─ Stock: 1.2 lb @ $3.75/lb = $4.50                    │
│     └─ Scrap factor (5%): $0.23                             │
│                                                               │
│   Machining:                            $33.76/pc           │
│     └─ OP10: Mill - Rough   $18.50/pc                      │
│     └─ OP20: Mill - Finish  $15.26/pc                      │
│                                                               │
│   Labor:                                $12.95/pc           │
│     └─ Operator: 0.37 hr @ $35/hr                          │
│                                                               │
│   Tooling:                              $ 1.80/pc           │
│     └─ Carbide inserts, end mills                           │
│                                                               │
│   Programming (NRE):                    $ 0.50/pc           │
│     └─ 3 hrs @ $75/hr ÷ 100 pcs                            │
│                                                               │
│   Inspection:                           $ 2.25/pc           │
│     └─ First article: $125 ÷ 100                            │
│     └─ In-process: 3 min/pc                                 │
│                                                               │
│   Consumables:                          $ 1.50/pc           │
│     └─ Coolant, deburring, marking                          │
│                                                               │
│   Overhead (150%):                      $16.20/pc           │
│     └─ Shop burden, utilities, admin                        │
│   ─────────────────────────────────────────────────────      │
│                                                               │
│   UNIT COST (at cost):                  $73.69/pc           │
│   Margin (15%):                         $11.05/pc           │
│   ═════════════════════════════════════════════════════      │
│   UNIT PRICE:                           $84.74/pc           │
│                                                               │
│   EXTENDED TOTAL (100 pcs):             $8,474.00           │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Volume Pricing Table Component
```
┌─────────────────────────────────────────────────┐
│ VOLUME PRICING - Part: BRKT-001                │
├─────────────────────────────────────────────────┤
│                                                   │
│  Quantity      Unit Price    Extended Total     │
│  ────────      ──────────    ──────────────     │
│  1-10 pcs      $142.50       $1,425.00         │
│  11-50 pcs     $ 98.25       $4,912.50         │
│  51-100 pcs    $ 84.74       $8,474.00  ← Current│
│  101-250 pcs   $ 76.20       $19,050.00        │
│  251-500 pcs   $ 72.15       $36,075.00        │
│  501+ pcs      Call for quote                   │
│                                                   │
│  💡 Save 49% by ordering 500 vs 10!             │
└─────────────────────────────────────────────────┘
```

### 3.3 What-If Calculator
```
┌─────────────────────────────────────────────────┐
│ WHAT-IF CALCULATOR                               │
├─────────────────────────────────────────────────┤
│                                                   │
│  Quantity: [____100____] ⚡ Update              │
│  Margin %: [____15_____] ⚡ Update              │
│  Rush?:    [_No_▼______]                        │
│                                                   │
│  ➜ Unit Price: $84.74                           │
│  ➜ Total: $8,474.00                             │
│  ➜ Lead Time: 2 weeks                           │
│                                                   │
│  🔄 Compare Scenarios:                          │
│  - Current (100 pcs, 2 weeks): $8,474          │
│  - Rushed (100 pcs, 1 week): $12,711 (+50%)    │
│  - Higher qty (250 pcs): $19,050 (save 24%)    │
└─────────────────────────────────────────────────┘
```

### 3.4 Quote Presentation Modes
```
┌─────────────────────────────────────────────────┐
│ QUOTE VIEW MODES                                 │
├─────────────────────────────────────────────────┤
│                                                   │
│  📄 Customer View (Simple)                      │
│     ├─ Part number, quantity                    │
│     ├─ Unit price                                │
│     ├─ Extended total                            │
│     └─ Lead time                                 │
│                                                   │
│  📊 Itemized View (Transparent)                 │
│     ├─ Material cost                             │
│     ├─ Machining cost                            │
│     ├─ Labor cost                                │
│     ├─ Subtotal + margin                         │
│     └─ Final price                               │
│                                                   │
│  🔬 Detailed Internal View (Operations)         │
│     ├─ Every operation breakdown                 │
│     ├─ Time per operation                        │
│     ├─ Cost per operation                        │
│     ├─ Tooling, programming, inspection          │
│     └─ Complete audit trail                      │
│                                                   │
└─────────────────────────────────────────────────┘
```

---

## Phase 4: New API Endpoints

### 4.1 Enhanced Quote Calculation
```
POST /api/quotes/calculate-detailed
{
  "part_id": 1,
  "quantity": 100,
  "margin_pct": 0.15,
  "rush": false,
  "include_nre": true
}

Response:
{
  "time_breakdown": {...},
  "cost_breakdown": {...},
  "unit_cost": 73.69,
  "unit_price": 84.74,
  "extended_total": 8474.00,
  "nre_charges": {...},
  "lead_time_days": 14
}
```

### 4.2 Volume Pricing
```
POST /api/quotes/volume-pricing
{
  "part_id": 1,
  "quantities": [1, 10, 50, 100, 250, 500]
}

Response:
{
  "tiers": [
    {"qty": 1, "unit_price": 142.50, "total": 142.50},
    {"qty": 10, "unit_price": 142.50, "total": 1425.00},
    ...
  ]
}
```

### 4.3 Rush Quote Calculator
```
POST /api/quotes/calculate-rush
{
  "quote_id": 1,
  "rush_level": "expedite"  // standard, rush, expedite, emergency
}

Response:
{
  "standard_price": 8474.00,
  "rush_price": 12711.00,
  "multiplier": 1.5,
  "lead_time_standard": 14,
  "lead_time_rush": 7
}
```

---

## Implementation Priority

### HIGH PRIORITY (Must Have)
1. ✅ Detailed cost breakdown display (Rules 2, 3, 4)
2. ✅ Time breakdown component
3. ✅ Enhanced calculation engine
4. ✅ Database model enhancements

### MEDIUM PRIORITY (Should Have)
5. Volume pricing calculator
6. What-if scenario tool
7. Rush charge calculator
8. Tool cost tracking

### LOW PRIORITY (Nice to Have)
9. Programming time tracking
10. Fixture cost amortization
11. Quote presentation mode toggle
12. PDF quote generation

---

## Success Criteria

✅ **Rule 2 Satisfied**: Detailed time breakdown showing setup, cycle, allowance, tool changes, inspection
✅ **Rule 3 Satisfied**: Complete cost itemization including material, machine, labor, tooling, consumables, overhead
✅ **Rule 4 Satisfied**: Clear display of cost vs price with margin percentage and breakdown

---

## Next Steps

1. Create enhanced database models
2. Build comprehensive calculation engine
3. Design and implement UI components
4. Test with real machine shop data
5. Get client feedback on presentation format

