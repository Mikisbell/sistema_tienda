

# app/main.py
from fastapi import FastAPI
from app.db.session import engine, Base
from app.routers import productos

app = FastAPI()

# Incluye los routers
app.include_router(productos.router)

# Crear las tablas en la base de datos (solo para desarrollo)
Base.metadata.create_all(bind=engine)