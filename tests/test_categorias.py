from typing import Dict, Generator

import pytest
from fastapi import FastAPI, APIRouter
from fastapi.testclient import TestClient

from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine

from app.config.settings import settings
from app.db.session import SessionLocal, engine
from app import models
from app.schemas import categorias as categoria_schemas
from app.schemas.categorias import CategoriaCreate, CategoriaUpdate, Categoria  # Importa CategoriaUpdate
from app.routers import categorias as categorias_router, productos as productos_router # Importa también otros routers si los usas en las pruebas
from app.db.base import Base


from sqlalchemy.orm import Session


from app.config.settings import settings

import time
import uuid

@pytest.fixture(scope="module")
def db():
    print(f"sqlite:///:memory: {settings.database_url}") # Añade esta línea
    engine_test = create_engine(settings.database_url) # Crea un motor para la base de datos de prueba
    Base.metadata.create_all(bind=engine_test) # Crea las tablas en la base de datos de prueba
    SessionLocalTest = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)
    database = SessionLocalTest()
    try:
        yield database
    finally:
        database.close()
        Base.metadata.drop_all(bind=engine_test) # Opcional: Elimina las tablas después de las pruebas


@pytest.fixture
def app_test():
    app = FastAPI(
        title="Sistema de Tienda API Test",
        description="API para gestionar productos, categorías, ventas y clientes.",
        version="0.1.0",
    )
    app.include_router(categorias_router.router, tags=["categorias"])
    app.include_router(productos_router.router, prefix=settings.api_prefix + "/productos", tags=["productos"]) # Mantén el prefijo para otros routers si es necesario
    return app

@pytest.fixture
def client(app_test):
    with TestClient(app=app_test) as client:
        yield client



def test_create_categoria(client: TestClient, db: Session) -> None:
    nombre_unico = f"Electrónica - Test Create - {uuid.uuid4()}"  # Generar un nombre único
    data = {"nombre": nombre_unico, "descripcion": "Productos electrónicos"}
    response = client.post(f"{settings.api_prefix}/categorias/", json=data)
    assert response.status_code == 201
        # ... other assertions ...





import time

def test_read_categoria(client: TestClient, db: Session) -> None:
    timestamp = int(time.time())
    unique_name = f"Libros - Test Read - {timestamp}"
    data = {"nombre": unique_name, "descripcion": "Todo tipo de libros"}
    response = client.post(f"{settings.api_prefix}/categorias/", json=data)
    assert response.status_code == 201
    categoria = response.json()
    categoria_id = categoria["id"]
    # ... resto de la prueba ...

def test_update_categoria(client: TestClient, db: Session) -> None:
    timestamp = int(time.time())
    initial_name = f"Ropa - Test Update - Initial - {timestamp}"
    create_data = {"nombre": initial_name, "descripcion": "Todo tipo de ropa"}
    create_response = client.post(f"{settings.api_prefix}/categorias/", json=create_data)
    assert create_response.status_code == 201
    categoria_created = create_response.json()
    categoria_id = categoria_created["id"]
    # ... resto de la prueba ...







def test_delete_categoria(client: TestClient, db: Session) -> None:
    # Primero creamos una categoría
    data = {"nombre": "Zapatos", "descripcion": "Todo tipo de calzado"}
    response = client.post(f"{settings.api_prefix}/categorias/", json=data)
    assert response.status_code == 201
    categoria_id = response.json()["id"]

    # Luego eliminamos la categoría
    response = client.delete(f"{settings.api_prefix}/categorias/{categoria_id}")
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == categoria_id

    # Intentamos leerla y debería dar 404
    response = client.get(f"{settings.api_prefix}/categorias/{categoria_id}")
    assert response.status_code == 404