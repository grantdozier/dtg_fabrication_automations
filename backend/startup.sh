#!/bin/sh
set -e

echo "Starting CNC Quoting Backend..."

# Create tables and seed database
python -c "
from app.db import Base, engine, SessionLocal
from app.seed import seed_database

print('Creating database tables...')
Base.metadata.create_all(bind=engine)

print('Seeding database...')
db = SessionLocal()
try:
    seed_database(db)
finally:
    db.close()
"

# Start FastAPI server
echo "Starting FastAPI server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
