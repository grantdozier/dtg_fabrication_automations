# CNC Machining Quoting System

A professional, full-stack quoting application for CNC machining manufacturers. Built with React (frontend) and Python FastAPI (backend) with PostgreSQL database.

## 🎯 Features

### Core Quoting Engine
- **Accurate Cost Calculation** with breakdown of:
  - Material costs with scrap factor
  - Machine time costs (amortized setup + cycle time)
  - Labor costs
  - Configurable profit margins

### Multi-Entity Management
- **Customers** - Client database with contact information
- **Materials** - Material library with cost per pound and density
- **Machines** - Machine shop inventory with hourly rates
- **Parts** - Part definitions with operations routing
- **Quotes** - Complete quotes with line items and cost breakdowns

### Real-Time Quote Preview
- Live calculation as you adjust:
  - Quantity
  - Margin percentage
  - Part selection

### Audit Trail
- All quote calculations are stored for historical accuracy
- Quote versioning and status tracking

---

## 🏗️ Tech Stack

### Frontend
- **React 18** + **TypeScript**
- **Vite** - Lightning-fast build tool
- **Material-UI (MUI)** - Professional component library
- **React Query** - Server state management
- **React Router** - Client-side routing
- **React Hook Form + Zod** - Form handling with validation

### Backend
- **Python 3.11+**
- **FastAPI** - Modern, fast web framework
- **SQLAlchemy 2.0** - Powerful ORM with type hints
- **PostgreSQL** - Production-ready relational database
- **Pydantic** - Data validation with type annotations
- **Uvicorn** - ASGI server

### DevOps
- **Docker + Docker Compose** - One-command development environment
- **PostgreSQL 16** - Containerized database

---

## 🚀 Quick Start

### Prerequisites
- Docker Desktop installed
- Git

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd dtg_fabrication_automations
```

2. **Start the application**
```bash
docker-compose up --build
```

This single command will:
- Start PostgreSQL database
- Build and run the FastAPI backend on port 8000
- Build and run the React frontend on port 5173
- Automatically seed the database with demo data

3. **Access the application**
- Frontend UI: http://localhost:3001
- Backend API: http://localhost:8001
- API Documentation: http://localhost:8001/docs

### Demo Data
The system comes pre-loaded with:
- 3 Customers
- 4 Materials (Aluminum, Steel, Stainless, Delrin)
- 3 Machines (3-axis mill, 5-axis mill, CNC lathe)
- 3 Parts with operations

---

## 📊 Database Schema

### Core Tables
```
customers
  - id, name, email, phone

materials
  - id, name, cost_per_lb, density_lb_in3, description

machines
  - id, name, machine_type, machine_rate_per_hr, labor_rate_per_hr

parts
  - id, part_number, description, material_id
  - stock_weight_lb, scrap_factor

operations (routing steps per part)
  - id, part_id, machine_id, name, sequence
  - setup_time_hr, cycle_time_hr, allowance_pct

quotes
  - id, customer_id, quote_number, status, notes

quote_items
  - id, quote_id, part_id, quantity, margin_pct
  - material_cost_unit, machine_cost_unit, labor_cost_unit
  - unit_cost, unit_price (stored calculated values)
```

---

## 🔧 Development

### Backend Development

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server (needs PostgreSQL running)
uvicorn app.main:app --reload
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Run dev server
npm run dev
```

### Manual Database Seeding

```bash
cd backend
python -m app.seed
```

---

## 📐 Quoting Formula

The system uses industry-standard CNC quoting methodology:

### Time Calculation (per part)
```
Total Time = (Setup Time / Quantity) + Cycle Time + (Cycle Time × Allowance %)
```

### Cost Breakdown
```
Material Cost = Stock Weight × Cost/lb × (1 + Scrap Factor)
Machine Cost = Total Time × Machine Rate/hr
Labor Cost = Total Time × Labor Rate/hr
Unit Cost = Material + Machine + Labor
Unit Price = Unit Cost × (1 + Margin %)
```

### Key Variables
- **Setup Time**: One-time fixture/programming (amortized across quantity)
- **Cycle Time**: Machine runtime per part
- **Allowance %**: Non-cutting time (tool changes, inspection, handling)
- **Scrap Factor**: Material waste percentage
- **Margin %**: Profit margin (typically 15-30%)

---

## 🎨 User Interface

### Pages
1. **Quote Builder** - Create new quotes with real-time cost preview
2. **Quotes List** - View all quotes with status
3. **Quote View** - Detailed quote with full cost breakdown
4. **Customers** - Manage customer database
5. **Parts** - View parts with operations
6. **Materials** - Manage material library
7. **Machines** - Machine shop inventory

### Navigation
- Side drawer navigation
- Professional Material Design UI
- Responsive layout for desktop/tablet

---

## 🔌 API Endpoints

### Quotes
- `POST /api/quotes/calculate` - Real-time cost calculation (no save)
- `POST /api/quotes` - Create and save quote
- `GET /api/quotes` - List all quotes
- `GET /api/quotes/{id}` - Get quote details

### Customers
- `GET /api/customers` - List all
- `POST /api/customers` - Create new
- `GET /api/customers/{id}` - Get details

### Materials
- `GET /api/materials` - List all
- `POST /api/materials` - Create new

### Machines
- `GET /api/machines` - List all
- `POST /api/machines` - Create new

### Parts
- `GET /api/parts` - List all with operations
- `POST /api/parts` - Create with operations
- `GET /api/parts/{id}` - Get details

**Full API documentation available at:** http://localhost:8001/docs

---

## 📦 Project Structure

```
dtg_fabrication_automations/
├── backend/
│   ├── app/
│   │   ├── routers/          # API endpoints
│   │   │   ├── customers.py
│   │   │   ├── materials.py
│   │   │   ├── machines.py
│   │   │   ├── parts.py
│   │   │   └── quotes.py
│   │   ├── services/         # Business logic
│   │   │   └── quoting.py    # Quote calculation engine
│   │   ├── db.py             # Database connection
│   │   ├── models.py         # SQLAlchemy models
│   │   ├── main.py           # FastAPI app
│   │   └── seed.py           # Demo data seeder
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   └── client.ts     # API client with types
│   │   ├── components/
│   │   │   └── CostBreakdown.tsx
│   │   ├── pages/
│   │   │   ├── QuoteBuilder.tsx
│   │   │   ├── QuoteView.tsx
│   │   │   ├── Quotes.tsx
│   │   │   ├── Customers.tsx
│   │   │   ├── Materials.tsx
│   │   │   ├── Machines.tsx
│   │   │   └── Parts.tsx
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── vite.config.ts
│   └── Dockerfile
└── docker-compose.yml
```

---

## 🎯 Demo Workflow

1. **View existing parts** at `/parts` to see sample brackets and shafts
2. **Create a new quote** at `/quotes/new`:
   - Select a customer
   - Choose a part
   - Enter quantity (watch cost recalculate)
   - Adjust margin percentage
   - Save quote
3. **View saved quote** - See full cost breakdown and extended totals
4. **Add customers/materials** - Expand the database with your shop's data

---

## 🚀 Future Enhancements

### Phase 2 Features
- [ ] PDF quote generation
- [ ] User authentication & roles
- [ ] CAD file import for material estimation
- [ ] ERP integration
- [ ] Quote approval workflow
- [ ] Historical cost tracking & analytics
- [ ] Multi-currency support
- [ ] Email quote delivery

### Phase 3 Features
- [ ] Job tracking (quote → order → production)
- [ ] Inventory management
- [ ] Machine scheduling
- [ ] Customer portal
- [ ] Mobile app

---

## 📝 Client Presentation Points

### Value Proposition
1. **Accuracy**: Defendable quotes based on real machine times and costs
2. **Speed**: Real-time calculation eliminates spreadsheet errors
3. **Audit Trail**: All quotes stored with historical accuracy
4. **Scalability**: Add unlimited customers, parts, and materials
5. **Modern Stack**: Built with industry-standard technologies

### Competitive Advantages
- **Shop-floor accurate** time calculations with setup amortization
- **Live preview** - see costs change as you adjust parameters
- **Extensible** - easy to add new features (CAD import, ERP integration)
- **Professional UI** - impress customers with polished interface
- **Open architecture** - own your data, customize to your needs

### ROI Metrics
- Reduce quoting time from 30+ minutes to under 5 minutes
- Eliminate calculation errors that lead to unprofitable jobs
- Standardize pricing across estimators
- Build quote database for historical analysis
- Scale to handle 10x more quotes without adding staff

---

## 🤝 Contributing

This is a prototype system. For production deployment, consider:
- Adding authentication (Auth0, Cognito, or custom JWT)
- Rate limiting on API
- Input validation hardening
- Backup/restore procedures
- Monitoring and logging
- SSL/TLS certificates

---

## 📄 License

Proprietary - All rights reserved

---

## 📞 Support

For questions or support, contact: [your-email@company.com]

---

## 🏁 Getting Started Checklist

- [ ] Docker Desktop installed and running
- [ ] Run `docker-compose up --build`
- [ ] Open http://localhost:3001
- [ ] Explore demo data (3 customers, 4 materials, 3 machines, 3 parts)
- [ ] Create a test quote
- [ ] Review cost breakdown
- [ ] Check API docs at http://localhost:8001/docs
- [ ] Present to client!

**You're ready to demo!** 🎉
