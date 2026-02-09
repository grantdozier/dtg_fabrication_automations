# Port Configuration - No Collision Setup

## Overview
The CNC Quoting System has been configured with non-standard ports to avoid conflicts with other local projects.

---

## 🔌 Port Mapping

| Service | External Port | Internal Port | Access URL |
|---------|---------------|---------------|------------|
| **Frontend** | 3001 | 5173 | http://localhost:3001 |
| **Backend API** | 8001 | 8000 | http://localhost:8001 |
| **API Docs** | 8001 | 8000 | http://localhost:8001/docs |
| **PostgreSQL** | 5433 | 5432 | localhost:5433 |

### What This Means

- **External Port**: The port you use on your host machine (your computer)
- **Internal Port**: The port the service uses inside the Docker container
- **Access URL**: Where you open the app in your browser

---

## 🐳 Container Names

All containers have unique names to prevent collisions:

| Service | Container Name |
|---------|----------------|
| Database | `cnc_quoting_db` |
| Backend | `cnc_quoting_backend` |
| Frontend | `cnc_quoting_frontend` |

### Why Named Containers?

- Prevents conflicts with other Docker projects
- Easy to identify in `docker ps` output
- Simple to reference in commands (e.g., `docker logs cnc_quoting_backend`)

---

## 📦 Volume Name

- **Volume Name**: `cnc_quoting_postgres_data`
- **Purpose**: Stores PostgreSQL database data
- **Uniqueness**: Won't conflict with other project volumes

---

## 🚀 Quick Start

### Start the Application
```bash
docker-compose up --build
```

### Access the Application
- **Main UI**: http://localhost:3001
- **API Documentation**: http://localhost:8001/docs
- **API Endpoints**: http://localhost:8001/api/...

### Stop the Application
```bash
docker-compose down
```

### Stop and Remove Data
```bash
docker-compose down -v
```

---

## 🔧 Customizing Ports Further

If you still have port conflicts, edit `docker-compose.yml`:

### Change Frontend Port
```yaml
frontend:
  ports:
    - "3002:5173"  # Changed from 3001 to 3002
```

### Change Backend Port
```yaml
backend:
  ports:
    - "8002:8000"  # Changed from 8001 to 8002
```

**Important**: If you change the backend port, also update:
1. Frontend environment variable in `docker-compose.yml`:
   ```yaml
   frontend:
     environment:
       - VITE_API_BASE=http://localhost:8002  # Match new port
   ```

2. CORS settings in `backend/app/main.py`:
   ```python
   allow_origins=[
       "http://localhost:3001",  # Or your new frontend port
       "http://localhost:3002",  # Add additional ports as needed
   ]
   ```

### Change Database Port
```yaml
db:
  ports:
    - "5434:5432"  # Changed from 5433 to 5434
```

---

## 🛠️ Troubleshooting

### Check What Ports Are In Use

**Windows:**
```bash
netstat -ano | findstr :3001
netstat -ano | findstr :8001
netstat -ano | findstr :5433
```

**Mac/Linux:**
```bash
lsof -i :3001
lsof -i :8001
lsof -i :5433
```

### Port Still In Use?

**Stop conflicting container:**
```bash
docker ps  # Find the container ID
docker stop <container-id>
```

**Or kill the process:**
```bash
# Windows (run as Administrator)
netstat -ano | findstr :<PORT>
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:<PORT> | xargs kill -9
```

---

## 📊 Comparison with Defaults

| Service | Default Port | CNC Quoting Port | Reason for Change |
|---------|--------------|------------------|-------------------|
| Vite Dev Server | 5173 | 3001 | Avoid conflicts with other Vite projects |
| FastAPI | 8000 | 8001 | Common port often in use |
| PostgreSQL | 5432 | 5433 | May conflict with local Postgres install |

---

## 🔒 CORS Configuration

The backend is configured to accept requests from multiple frontend ports:

```python
allow_origins=[
    "http://localhost:3001",  # CNC Quoting Frontend (current)
    "http://localhost:5173",  # Vite default
    "http://localhost:3000",  # React default
]
```

This allows flexibility during development.

---

## 🎯 Benefits of This Setup

✅ **No Port Collisions** - Uses non-standard ports
✅ **Named Containers** - Easy to identify and manage
✅ **Isolated Volumes** - Data won't mix with other projects
✅ **Flexible CORS** - Works with multiple frontend configurations
✅ **Easy Customization** - Simple to change ports if needed

---

## 📝 Quick Reference Card

Print or save this for easy reference:

```
┌─────────────────────────────────────┐
│   CNC QUOTING SYSTEM - PORT CARD   │
├─────────────────────────────────────┤
│                                     │
│  Frontend:  http://localhost:3001  │
│  API:       http://localhost:8001  │
│  API Docs:  /docs                   │
│  Database:  localhost:5433          │
│                                     │
│  Containers:                        │
│    - cnc_quoting_frontend           │
│    - cnc_quoting_backend            │
│    - cnc_quoting_db                 │
│                                     │
│  Commands:                          │
│    Start:  docker-compose up        │
│    Stop:   docker-compose down      │
│    Logs:   docker-compose logs      │
│                                     │
└─────────────────────────────────────┘
```

---

## 🔗 Related Documentation

- `README.md` - Full project documentation
- `QUICKSTART.md` - Demo and presentation guide
- `docker-compose.yml` - Service configuration
- `backend/app/main.py` - CORS settings

---

## ✅ Configuration Checklist

- [x] Unique container names set
- [x] Non-standard ports configured
- [x] CORS updated for new frontend port
- [x] Volume name made unique
- [x] Documentation updated with new ports
- [x] Environment variables updated

**Your system is now configured to run alongside other projects without conflicts!** 🎉
