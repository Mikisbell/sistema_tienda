# app/main.py
# Importa FastAPI para crear la aplicación
from fastapi import FastAPI
# Importa engine y Base desde app.db.session para manejar la base de datos
from app.db.session import engine, Base
# Importa los routers de productos y clientes
from app.routers import productos, clientes
from app.routers import categorias
from app.routers import ventas
from app.routers import auth

# Crea una instancia de la aplicación FastAPI
app = FastAPI()

# Incluye los routers
# Incluye el router de productos en la aplicación
app.include_router(productos.router)
app.include_router(categorias.router)
app.include_router(ventas.router)
# Incluye el router de clientes en la aplicación
app.include_router(clientes.router)
app.include_router(auth.router)


# Crear las tablas en la base de datos (solo para desarrollo)
Base.metadata.create_all(bind=engine)

# Define una ruta para el endpoint raíz
@app.get("/")
def read_root():
    """
    Endpoint raíz que devuelve un mensaje de bienvenida.
    """
    return {"message": "¡Hola, mundo!"}