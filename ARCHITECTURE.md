# System Architecture Overview

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                            │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Desktop    │  │    Tablet    │  │    Mobile    │          │
│  │   Browser    │  │   Browser    │  │   Browser    │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         │                  │                  │                  │
│         └──────────────────┼──────────────────┘                  │
│                            │                                     │
│                     HTTP/HTTPS (Port 5173)                       │
└────────────────────────────┼─────────────────────────────────────┘
                             │
┌────────────────────────────▼─────────────────────────────────────┐
│                    PRESENTATION LAYER                            │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              React Application (Vite)                     │  │
│  │                                                             │  │
│  │  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐    │  │
│  │  │   Pages     │  │  Components  │  │  API Client  │    │  │
│  │  │ ─────────── │  │ ──────────── │  │ ──────────── │    │  │
│  │  │ Customers   │  │ Cost         │  │ Typed        │    │  │
│  │  │ Materials   │  │ Breakdown    │  │ Fetch        │    │  │
│  │  │ Machines    │  │ Forms        │  │ Client       │    │  │
│  │  │ Parts       │  │ Tables       │  │ React Query  │    │  │
│  │  │ Quotes      │  │ Navigation   │  │ Cache        │    │  │
│  │  └─────────────┘  └──────────────┘  └──────────────┘    │  │
│  │                                                             │  │
│  │              Material-UI Components                        │  │
│  │              TypeScript Type Safety                        │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                   │
│                      REST API (JSON)                             │
└────────────────────────────┼─────────────────────────────────────┘
                             │
┌────────────────────────────▼─────────────────────────────────────┐
│                      API LAYER                                   │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              FastAPI Application (Uvicorn)                │  │
│  │                      Port 8000                             │  │
│  │                                                             │  │
│  │  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐    │  │
│  │  │  Routers    │  │  Services    │  │  Schemas     │    │  │
│  │  │ ─────────── │  │ ──────────── │  │ ──────────── │    │  │
│  │  │ /customers  │  │ Quoting      │  │ Pydantic     │    │  │
│  │  │ /materials  │  │ Calculation  │  │ Validation   │    │  │
│  │  │ /machines   │  │ Engine       │  │ Models       │    │  │
│  │  │ /parts      │  │              │  │              │    │  │
│  │  │ /quotes     │  │              │  │              │    │  │
│  │  └─────────────┘  └──────────────┘  └──────────────┘    │  │
│  │                                                             │  │
│  │  ┌───────────────────────────────────────────────────┐    │  │
│  │  │         OpenAPI/Swagger Documentation             │    │  │
│  │  │              Auto-generated at /docs              │    │  │
│  │  └───────────────────────────────────────────────────┘    │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                   │
│                    SQLAlchemy ORM                                │
└────────────────────────────┼─────────────────────────────────────┘
                             │
┌────────────────────────────▼─────────────────────────────────────┐
│                    DATA LAYER                                    │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │            PostgreSQL Database (Port 5432)                │  │
│  │                                                             │  │
│  │  ┌──────────────────────────────────────────────────────┐ │  │
│  │  │                   Tables                             │ │  │
│  │  │  ┌────────────┐ ┌────────────┐ ┌────────────┐      │ │  │
│  │  │  │ customers  │ │ materials  │ │  machines  │      │ │  │
│  │  │  └────────────┘ └────────────┘ └────────────┘      │ │  │
│  │  │  ┌────────────┐ ┌────────────┐ ┌────────────┐      │ │  │
│  │  │  │   parts    │ │ operations │ │   quotes   │      │ │  │
│  │  │  └────────────┘ └────────────┘ └────────────┘      │ │  │
│  │  │  ┌────────────┐                                     │ │  │
│  │  │  │quote_items │                                     │ │  │
│  │  │  └────────────┘                                     │ │  │
│  │  │                                                      │ │  │
│  │  │  Foreign Keys | Indexes | Constraints               │ │  │
│  │  └──────────────────────────────────────────────────────┘ │  │
│  └───────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Request Flow: Creating a Quote

```
┌──────────┐
│  User    │
│  Browser │
└────┬─────┘
     │
     │ 1. User fills quote form
     │    - Selects customer
     │    - Selects part
     │    - Enters quantity (e.g., 100)
     │    - Sets margin (e.g., 15%)
     │
     ▼
┌─────────────────────────────┐
│  React Component            │
│  (QuoteBuilder.tsx)         │
└────┬────────────────────────┘
     │
     │ 2. Form validation (React Hook Form)
     │    - Ensures required fields present
     │    - Validates data types
     │
     ▼
┌─────────────────────────────┐
│  API Client                 │
│  (React Query Mutation)     │
└────┬────────────────────────┘
     │
     │ 3. POST /api/quotes/calculate
     │    Body: { part_id: 1, quantity: 100, margin_pct: 0.15 }
     │
     ▼
┌─────────────────────────────────────────────────────┐
│  FastAPI Router                                     │
│  (quotes.py)                                        │
│                                                      │
│  @router.post("/calculate")                         │
│  def calculate(payload: CalculateRequest, ...)     │
└────┬────────────────────────────────────────────────┘
     │
     │ 4. Pydantic validation
     │    - Validates request schema
     │    - Converts types
     │
     ▼
┌─────────────────────────────────────────────────────┐
│  Database Query (SQLAlchemy)                        │
│                                                      │
│  - Fetch part with operations                       │
│  - Fetch material costs                             │
│  - Fetch machine rates                              │
└────┬────────────────────────────────────────────────┘
     │
     │ 5. Query execution
     │    SELECT * FROM parts WHERE id = 1
     │    JOIN operations, materials, machines
     │
     ▼
┌─────────────────────────────────────────────────────┐
│  Quoting Service                                    │
│  (services/quoting.py)                              │
│                                                      │
│  calc_unit_cost(                                    │
│    quantity=100,                                    │
│    stock_weight_lb=1.2,                             │
│    cost_per_lb=3.75,                                │
│    scrap_factor=0.05,                               │
│    ops=[...],                                       │
│    margin_pct=0.15                                  │
│  )                                                  │
└────┬────────────────────────────────────────────────┘
     │
     │ 6. Cost calculation
     │    Material = 1.2 × 3.75 × 1.05 = $4.73
     │
     │    For each operation:
     │      Setup per part = setup_time / quantity
     │      Allowance = cycle_time × allowance_pct
     │      Time = setup_per_part + cycle_time + allowance
     │      Machine cost += time × machine_rate
     │      Labor cost += time × labor_rate
     │
     │    Unit Cost = Material + Machine + Labor
     │    Unit Price = Unit Cost × (1 + margin)
     │
     ▼
┌─────────────────────────────────────────────────────┐
│  Response                                           │
│  {                                                  │
│    "material_unit": 4.73,                           │
│    "machine_unit": 31.45,                           │
│    "labor_unit": 12.95,                             │
│    "unit_cost": 49.13,                              │
│    "unit_price": 56.50,                             │
│    "total_time_hr": 0.37                            │
│  }                                                  │
└────┬────────────────────────────────────────────────┘
     │
     │ 7. JSON response sent to frontend
     │
     ▼
┌─────────────────────────────┐
│  React Query Cache          │
│  - Stores result            │
│  - Triggers re-render       │
└────┬────────────────────────┘
     │
     │ 8. Component re-renders with data
     │
     ▼
┌─────────────────────────────┐
│  CostBreakdown Component    │
│  - Displays material cost   │
│  - Displays machine cost    │
│  - Displays labor cost      │
│  - Shows unit cost/price    │
│  - Shows extended totals    │
└────┬────────────────────────┘
     │
     │ 9. User sees breakdown instantly
     │
     ▼
┌──────────┐
│  User    │
│  Browser │
└──────────┘
```

---

## Database Entity-Relationship Diagram

```
┌─────────────────┐
│   customers     │
│─────────────────│
│ id (PK)         │────┐
│ name            │    │
│ email           │    │
│ phone           │    │
│ created_at      │    │
└─────────────────┘    │
                       │
                       │ 1:N
                       │
┌──────────────────────▼─────┐
│   quotes                   │
│────────────────────────────│
│ id (PK)                    │────┐
│ customer_id (FK)           │    │
│ quote_number               │    │
│ status                     │    │
│ notes                      │    │
│ created_at                 │    │
└────────────────────────────┘    │
                                  │ 1:N
                                  │
┌─────────────────────────────────▼─────────────────┐
│   quote_items                                      │
│────────────────────────────────────────────────────│
│ id (PK)                                            │
│ quote_id (FK) ───────────────────────────────────┐│
│ part_id (FK) ────────────────┐                   ││
│ quantity                     │                   ││
│ margin_pct                   │                   ││
│ material_cost_unit (stored)  │                   ││
│ machine_cost_unit (stored)   │                   ││
│ labor_cost_unit (stored)     │                   ││
│ unit_cost (stored)           │                   ││
│ unit_price (stored)          │                   ││
└──────────────────────────────┼───────────────────┘│
                               │                    │
                               │                    │
                      ┌────────▼────────┐           │
                      │   parts         │           │
                      │─────────────────│           │
                      │ id (PK)         │───────────┘
                      │ part_number     │
                      │ description     │
                      │ material_id (FK)│────┐
                      │ stock_weight_lb │    │
                      │ scrap_factor    │    │
                      │ created_at      │    │
                      └────┬────────────┘    │
                           │                 │
                           │ 1:N             │ N:1
                           │                 │
              ┌────────────▼────────┐        │        ┌─────────────────┐
              │   operations        │        │        │   materials     │
              │─────────────────────│        │        │─────────────────│
              │ id (PK)             │        └────────│ id (PK)         │
              │ part_id (FK)        │                 │ name            │
              │ machine_id (FK)     │───┐             │ cost_per_lb     │
              │ name                │   │             │ density_lb_in3  │
              │ sequence            │   │             │ description     │
              │ setup_time_hr       │   │             └─────────────────┘
              │ cycle_time_hr       │   │
              │ allowance_pct       │   │ N:1
              └─────────────────────┘   │
                                        │
                                        │
                              ┌─────────▼───────┐
                              │   machines      │
                              │─────────────────│
                              │ id (PK)         │
                              │ name            │
                              │ machine_type    │
                              │ machine_rate_hr │
                              │ labor_rate_hr   │
                              │ description     │
                              └─────────────────┘
```

---

## Technology Stack Layers

```
┌────────────────────────────────────────────────────────────────┐
│                    FRONTEND STACK                              │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │   React 18   │  │  TypeScript  │  │ Material-UI  │        │
│  │ Component    │  │ Type Safety  │  │   Design     │        │
│  │   Model      │  │   & IDE      │  │   System     │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │ React Query  │  │ React Router │  │ React Hook   │        │
│  │   Caching    │  │  Navigation  │  │    Form      │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
│                                                                 │
│  ┌────────────────────────────────────────────────────┐        │
│  │              Vite (Build Tool)                     │        │
│  │  Hot Module Reload | Fast Builds | Tree Shaking   │        │
│  └────────────────────────────────────────────────────┘        │
│                                                                 │
└────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│                    BACKEND STACK                               │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌────────────────────────────────────────────────────┐        │
│  │                  FastAPI Framework                 │        │
│  │  Async | Auto Docs | Dependency Injection         │        │
│  └────────────────────────────────────────────────────┘        │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │  Pydantic    │  │ SQLAlchemy   │  │   Python     │        │
│  │ Validation   │  │  ORM 2.0     │  │    3.11+     │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
│                                                                 │
│  ┌────────────────────────────────────────────────────┐        │
│  │              Uvicorn (ASGI Server)                 │        │
│  │     High Performance | Production Ready            │        │
│  └────────────────────────────────────────────────────┘        │
│                                                                 │
└────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│                    DATABASE LAYER                              │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌────────────────────────────────────────────────────┐        │
│  │              PostgreSQL 16                         │        │
│  │  ACID Compliant | Foreign Keys | Indexes          │        │
│  └────────────────────────────────────────────────────┘        │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │  Connection  │  │   B-Tree     │  │  Constraint  │        │
│  │   Pooling    │  │   Indexes    │  │  Validation  │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
│                                                                 │
└────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│                    INFRASTRUCTURE                              │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌────────────────────────────────────────────────────┐        │
│  │              Docker + Docker Compose               │        │
│  │  Containerization | Service Orchestration          │        │
│  └────────────────────────────────────────────────────┘        │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │   Network    │  │   Volumes    │  │ Health       │        │
│  │   Isolation  │  │ Persistence  │  │   Checks     │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

## Deployment Architecture (Future Production)

```
┌────────────────────────────────────────────────────────────────┐
│                         INTERNET                               │
└────────────────────────┬───────────────────────────────────────┘
                         │
                    HTTPS/TLS
                         │
┌────────────────────────▼───────────────────────────────────────┐
│                    Load Balancer                               │
│                   (nginx / Cloud LB)                           │
└────────┬───────────────────────────────┬───────────────────────┘
         │                               │
         │                               │
    ┌────▼────┐                     ┌────▼────┐
    │ Frontend│                     │ Frontend│
    │ Server 1│                     │ Server 2│
    │ (React) │                     │ (React) │
    └────┬────┘                     └────┬────┘
         │                               │
         └───────────┬───────────────────┘
                     │ REST API
                     │
         ┌───────────▼───────────┐
         │   API Gateway         │
         │  (Authentication)     │
         └───────────┬───────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
    ┌────▼────┐             ┌────▼────┐
    │ Backend │             │ Backend │
    │ Server 1│             │ Server 2│
    │(FastAPI)│             │(FastAPI)│
    └────┬────┘             └────┬────┘
         │                       │
         └───────────┬───────────┘
                     │
         ┌───────────▼───────────┐
         │   Database Cluster    │
         │                       │
         │  ┌─────────────────┐  │
         │  │   Primary DB    │  │
         │  │  (Read/Write)   │  │
         │  └────────┬────────┘  │
         │           │           │
         │  ┌────────┴────────┐  │
         │  │                 │  │
         │  ▼                 ▼  │
         │ ┌────┐         ┌────┐│
         │ │Rep1│         │Rep2││
         │ │    │         │    ││
         │ └────┘         └────┘│
         │ (Read Only)  (Read  )│
         └───────────────────────┘

┌──────────────────────────────────┐
│     Monitoring & Logging         │
│  - Health checks                 │
│  - Performance metrics           │
│  - Error tracking                │
│  - Usage analytics               │
└──────────────────────────────────┘
```

---

## Security Architecture (Production)

```
┌────────────────────────────────────────────────────────────────┐
│                    SECURITY LAYERS                             │
└────────────────────────────────────────────────────────────────┘

Layer 1: Network Security
├─ HTTPS/TLS encryption (Let's Encrypt)
├─ Firewall rules (only expose 80/443)
├─ VPC isolation (database not public)
└─ Rate limiting (prevent abuse)

Layer 2: Application Security
├─ JWT authentication
├─ Role-based access control (RBAC)
├─ Input validation (Pydantic)
├─ SQL injection prevention (ORM parameterized queries)
├─ XSS prevention (React auto-escaping)
├─ CORS configuration
└─ Security headers (CSP, HSTS, etc.)

Layer 3: Data Security
├─ Encrypted connections (SSL/TLS to database)
├─ Password hashing (bcrypt)
├─ Encrypted backups
├─ Audit logging (who did what, when)
└─ Data retention policies

Layer 4: Operational Security
├─ Automated backups
├─ Disaster recovery plan
├─ Intrusion detection
├─ Security updates (automated)
└─ Penetration testing (annual)
```

---

## File Structure Overview

```
dtg_fabrication_automations/
│
├── backend/                        # Python FastAPI Backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                # FastAPI app entry point
│   │   ├── db.py                  # Database connection
│   │   ├── models.py              # SQLAlchemy models
│   │   ├── seed.py                # Demo data seeder
│   │   ├── routers/               # API endpoints
│   │   │   ├── customers.py       # Customer CRUD
│   │   │   ├── materials.py       # Material CRUD
│   │   │   ├── machines.py        # Machine CRUD
│   │   │   ├── parts.py           # Part + Operations CRUD
│   │   │   └── quotes.py          # Quote calculation & storage
│   │   └── services/              # Business logic
│   │       └── quoting.py         # Quote calculation engine
│   ├── requirements.txt           # Python dependencies
│   └── Dockerfile                 # Backend container
│
├── frontend/                       # React TypeScript Frontend
│   ├── src/
│   │   ├── main.tsx               # React entry point
│   │   ├── App.tsx                # Root component with routing
│   │   ├── api/
│   │   │   └── client.ts          # API client with types
│   │   ├── components/
│   │   │   └── CostBreakdown.tsx  # Reusable cost display
│   │   └── pages/
│   │       ├── Customers.tsx      # Customer list + create
│   │       ├── Materials.tsx      # Material list + create
│   │       ├── Machines.tsx       # Machine list + create
│   │       ├── Parts.tsx          # Part list
│   │       ├── QuoteBuilder.tsx   # New quote creation
│   │       ├── Quotes.tsx         # Quote list
│   │       └── QuoteView.tsx      # Quote detail view
│   ├── package.json               # Node dependencies
│   ├── vite.config.ts             # Vite configuration
│   └── Dockerfile                 # Frontend container
│
├── docker-compose.yml             # Multi-container orchestration
├── .gitignore                     # Git ignore rules
├── README.md                      # Full documentation
├── QUICKSTART.md                  # Demo setup guide
├── TECH_STACK_PRESENTATION.md     # Technical presentation
└── ARCHITECTURE.md                # This file
```

---

## Key Design Decisions

### 1. **Monorepo Structure**
- Single repository contains frontend + backend
- Easy to keep API contracts in sync
- Simplified deployment

### 2. **API-First Design**
- Backend is pure REST API
- Frontend is pure UI consumer
- Enables future integrations (mobile app, third-party tools)

### 3. **Type Safety End-to-End**
- TypeScript on frontend
- Pydantic on backend
- SQLAlchemy with type hints
- Reduces runtime errors significantly

### 4. **Separation of Concerns**
- **Routers**: Handle HTTP requests/responses
- **Services**: Contain business logic
- **Models**: Define data structure
- Makes testing and maintenance easier

### 5. **Stored Calculations**
- Quote calculations saved to database
- Provides audit trail
- Historical accuracy (even if rates change later)

### 6. **Real-Time Preview**
- Calculate endpoint doesn't save
- Allows user experimentation
- Save endpoint commits to database

---

## Scalability Considerations

### Current Capacity
- **Users**: 100+ concurrent
- **Quotes**: Millions
- **Parts**: Tens of thousands

### Scaling Strategy

**Vertical Scaling** (Easiest first step)
- Increase server CPU/RAM
- Upgrade database instance
- Cost: ~$100-500/month

**Horizontal Scaling** (Production growth)
- Multiple frontend servers (stateless)
- Multiple backend servers (stateless)
- Database read replicas
- Cost: ~$500-2000/month

**Microservices** (Enterprise scale)
- Quote service
- Customer service
- Notification service
- Cost: ~$2000+/month

---

This architecture is designed to be:
- ✅ **Maintainable**: Clear separation, standard patterns
- ✅ **Scalable**: Can grow from 10 to 10,000 users
- ✅ **Extensible**: Easy to add features
- ✅ **Reliable**: ACID transactions, type safety
- ✅ **Modern**: Industry-standard technologies
