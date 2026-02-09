# 🚀 Quick Start Guide - CNC Quoting System

## For Client Presentation

### One-Command Demo Setup

1. **Open terminal in project folder**

2. **Start everything**:
```bash
docker-compose up --build
```

3. **Wait 30-60 seconds** for services to start (watch the logs)

4. **Open your browser to**:
   - **Main App**: http://localhost:3001
   - **API Docs**: http://localhost:8001/docs

That's it! The system is now running with demo data.

---

## 📱 Demo Flow for Client

### 1. Show the Dashboard (5 min)
- Open http://localhost:3001
- Walk through the navigation menu
- Show professional Material-UI design

### 2. View Existing Data (5 min)
- Click **Customers** → Show 3 pre-loaded customers
- Click **Materials** → Show material library with costs
- Click **Machines** → Show machine shop inventory with rates
- Click **Parts** → Show parts with operations routing

### 3. Create a Live Quote (10 min)
1. Click **New Quote** in sidebar
2. Select a customer (e.g., "Bayou Fabrication LLC")
3. Select a part (e.g., "BRKT-001 - Bracket")
4. Enter quantity: **100**
5. **Watch the cost breakdown calculate in real-time**
6. Adjust quantity to **50** → See costs recalculate instantly
7. Adjust margin to **20%** → See price change
8. Click **Save Quote**

### 4. View Saved Quote (3 min)
- System redirects to quote detail page
- Show complete breakdown:
  - Material costs
  - Machine time costs
  - Labor costs
  - Unit cost vs unit price
  - Extended totals
  - Profit margin

### 5. Show API Documentation (2 min)
- Open http://localhost:8001/docs
- Show auto-generated API documentation
- Demonstrate "Try it out" feature on any endpoint
- Explain this enables future integrations (mobile app, ERP, etc.)

---

## 🎯 Key Talking Points

### During Demo

**"This is a working prototype with real calculations..."**
- Not mockups or slides—actual functioning software
- Database-backed with audit trail
- Production-ready architecture

**"Watch how it calculates costs in real-time..."**
- Change quantity → instant recalculation
- Adjust margin → see profit impact
- All server-side for accuracy

**"Everything is stored for historical accuracy..."**
- Every quote saved with full breakdown
- Audit trail for who quoted what, when
- Can analyze pricing trends over time

**"Built on modern, proven technologies..."**
- React (used by Facebook, Netflix, Airbnb)
- Python/FastAPI (modern, fast, typed)
- PostgreSQL (bank-grade reliability)

**"Designed to scale with your business..."**
- Add unlimited customers, parts, materials
- Multi-user ready (add auth in Phase 2)
- API-first design for future integrations

---

## 💡 Questions They Might Ask

**Q: Can we customize this?**
A: Yes! Full source code ownership. Can add any features needed.

**Q: How accurate are the calculations?**
A: Based on the same formula spreadsheets use, but automated. You input:
   - Setup time, cycle time, allowances (from your CAM system)
   - Material costs, machine rates (from your accounting)
   - System does the math perfectly every time.

**Q: Can we import our existing parts?**
A: Yes. Can build an import tool for Excel/CSV data.

**Q: What about CAD files?**
A: Phase 2 feature. Can parse CAD to estimate material volume/weight.

**Q: How much does hosting cost?**
A: $100-300/month for typical shop. One-time setup, then low recurring costs.

**Q: How long to go live?**
A: Prototype is ready now. Production hardening (auth, security) is 4-6 weeks.

**Q: Can it integrate with our ERP?**
A: Yes. API-first design. Can push/pull data from QuickBooks, SAP, etc.

**Q: What if we want mobile access?**
A: The web app works on tablets now. Native mobile app is Phase 3.

---

## 🛠️ Troubleshooting (If Demo Hiccups)

### "Connection refused" or blank page
```bash
# Restart services
docker-compose down
docker-compose up --build
```

### Database not seeding
```bash
# Force re-seed
docker-compose down -v  # Delete volumes
docker-compose up --build
```

### Port already in use
```bash
# Stop conflicting services
docker ps  # See what's running
docker stop <container-id>
```

Or edit `docker-compose.yml` to use different ports:
- Frontend: Change `5173:5173` to `3000:5173`
- Backend: Change `8000:8000` to `9000:8000`

### Can't connect to database
```bash
# Check database is running
docker-compose ps

# View logs
docker-compose logs db
docker-compose logs backend
```

---

## 📋 Pre-Demo Checklist

- [ ] Docker Desktop installed and running
- [ ] Project downloaded/cloned
- [ ] Run `docker-compose up --build` successfully
- [ ] Can access http://localhost:5173 (frontend)
- [ ] Can access http://localhost:8001/docs (API)
- [ ] Demo data loaded (see 3 customers in UI)
- [ ] Created one test quote to verify workflow
- [ ] Browser bookmarks set for easy navigation
- [ ] Backup plan: Screenshots if internet/Docker fails

---

## 🎬 Presentation Flow (25 min total)

| Time | Section | Notes |
|------|---------|-------|
| 0-2 min | Introduction | "Built a working CNC quoting system prototype" |
| 2-7 min | Show dashboard | Navigate UI, show existing data |
| 7-17 min | Create quote | Live demo with real-time calculation |
| 17-20 min | Show saved quote | Full breakdown, audit trail |
| 20-22 min | API docs | Future-proof, extensible |
| 22-25 min | Q&A | Address specific needs |

---

## 💼 Leave-Behind Documents

Print/email these to the client:
1. `README.md` - Full documentation
2. `TECH_STACK_PRESENTATION.md` - Technical architecture
3. This `QUICKSTART.md` - They can run it themselves

---

## 🎯 Success Metrics for Demo

**Good demo if client says:**
- "This is exactly what we need"
- "How soon can we deploy this?"
- "Can you add [specific feature]?"
- "What's the next step?"

**Great demo if client:**
- Tries using it themselves during demo
- Asks detailed questions about customization
- Discusses rollout timeline
- Requests proposal/quote for completion

---

## 📞 After the Demo

### Next Steps to Propose:
1. **Phase 1 (2 weeks)**: Customize with their actual data (materials, machines, rates)
2. **Phase 2 (4 weeks)**: Add authentication, user roles, PDF quotes
3. **Phase 3 (4 weeks)**: Deployment to production cloud hosting
4. **Ongoing**: Support, maintenance, feature additions

### Pricing Guidance:
- **Development**: $8k-15k (depends on customizations)
- **Hosting**: $100-300/month
- **Support**: $500-1000/month (optional)

### Alternatives if Budget Limited:
- Start with just quote calculation module
- Self-hosted on their server (no cloud costs)
- Phased rollout (customers first, then parts, then quotes)

---

## 🏁 You're Ready!

This demo shows:
- ✅ Real working software (not vaporware)
- ✅ Professional UI (not a rough mockup)
- ✅ Accurate calculations (shop-floor ready)
- ✅ Production architecture (scales with growth)
- ✅ Your technical capability (win their confidence)

**Go get 'em!** 🎉
