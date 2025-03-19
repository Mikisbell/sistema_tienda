# app/main.py
from fastapi import FastAPI
from app.db.session import engine, Base
from app.routers import productos, clientes, categorias, ventas, auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Sistema de Tienda API",
    description="API para gestionar productos, categorías, ventas y clientes.",
    version="0.1.0",
)

app.include_router(productos.router)
app.include_router(categorias.router)
app.include_router(ventas.router)
app.include_router(clientes.router)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "¡Hola, mundo!"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    database_url: str
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()

# Create the tables only if the script is run directly
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
