# app.main.py
from fastapi import FastAPI
from app.config.settings import settings
from app.routers import productos, clientes, categorias, ventas, auth
from fastapi.middleware.cors import CORSMiddleware
from app.models.categorias import Base

app = FastAPI(
    title="Sistema de Tienda API",
    description="API para gestionar productos, categorías, ventas y clientes.",
    version="0.1.0",)

app.include_router(productos.router, prefix=settings.api_prefix + "/productos", tags=["productos"])
app.include_router(categorias.router, prefix=settings.api_prefix + "/categorias", tags=["categorias"])
app.include_router(ventas.router, prefix=settings.api_prefix + "/ventas", tags=["ventas"])
app.include_router(clientes.router, prefix=settings.api_prefix + "/clientes", tags=["clientes"])
app.include_router(auth.router, prefix=settings.api_prefix + "/auth", tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "¡Hola, mundo!"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)

# Crear las tablas solo si el script se ejecuta directamente
if __name__ == "__main__":
    from app.db.session import engine, Base
    Base.metadata.create_all(bind=engine)# Listar todas las rutas para depuración
for route in app.routes:
    print(f"Ruta: {route.path} - Métodos: {route.methods}")