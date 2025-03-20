# conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.config.settings import settings as app_settings
from app.models.productos import Producto

TEST_DATABASE_URL = "sqlite:///:memory:"  # Use an in-memory database

@pytest.fixture(scope="session")
def settings():
    app_settings.database_url = TEST_DATABASE_URL
    return app_settings

@pytest.fixture(scope="session")
def engine(settings):
    return create_engine(settings.database_url)

@pytest.fixture(scope="session")
def SessionLocal(engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db(SessionLocal, engine):
    """Fixture para proporcionar una sesión de base de datos con rollback para cada test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)
    try:
        print("\n--- Antes del test ---")
        Base.metadata.drop_all(bind=engine)  # Elimina las tablas existentes
        Base.metadata.create_all(bind=engine)  # Crea las tablas de nuevo
        print("--- Base de datos recreada ---")
        count_before = session.query(Producto).count()
        print(f"Número de productos antes del test: {count_before}")
        yield session
        print("\n--- Después del test ---")
        count_after = session.query(Producto).count()
        print(f"Número de productos después del test (antes del rollback): {count_after}")
    finally:
        session.close()
        transaction.rollback()
        connection.close()
        print("--- Rollback realizado ---")
        connection_after_rollback = engine.connect()
        session_after_rollback = SessionLocal(bind=connection_after_rollback)
        count_after_rollback = session_after_rollback.query(Producto).count()
        print(f"Número de productos después del rollback: {count_after_rollback}")
        session_after_rollback.close()
        connection_after_rollback.close()

@pytest.fixture(scope="function")
def client(db):  # Inject the 'db' fixture here
    from fastapi.testclient import TestClient
    from fastapi import FastAPI
    from app.routers import productos, categorias, ventas, clientes, auth
    from app.db.base import get_db

    def create_app():
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

        def override_get_db():
            yield db  # Use the 'db' fixture's session

        app.dependency_overrides[get_db] = override_get_db
        return app

    app = create_app()
    with TestClient(app) as client:
        yield client

@pytest.fixture(scope="session", autouse=True)
def create_test_database(engine):
    # Ya no necesitamos crear las tablas aquí, lo haremos en el fixture 'db'
    print("\n--- Configuración inicial de la base de datos de prueba ---")
    yield
    # Opcional: Si quieres eliminar las tablas después de cada sesión de tests
    # Base.metadata.drop_all(bind=engine)