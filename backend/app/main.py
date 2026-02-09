from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import Base, engine
from .routers import customers, materials, machines, parts, quotes

app = FastAPI(
    title="CNC Quoting System",
    description="Professional CNC machining quoting engine with accurate cost calculation",
    version="1.0.0"
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3001",  # CNC Quoting Frontend
        "http://localhost:5173",  # Vite default
        "http://localhost:3000",  # React default
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables on startup
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(customers.router)
app.include_router(materials.router)
app.include_router(machines.router)
app.include_router(parts.router)
app.include_router(quotes.router)

@app.get("/")
def root():
    return {
        "service": "CNC Quoting System API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health():
    return {"status": "healthy", "service": "cnc-quoting-api"}
