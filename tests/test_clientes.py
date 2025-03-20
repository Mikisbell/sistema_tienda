# app/test/clientes.py
from fastapi.testclient import TestClient
from app.main import app  # Importa app desde app.main
from app.config.settings import settings # Importa la configuración para acceder al prefijo

# Crea un cliente de prueba para interactuar con la aplicación
client = TestClient(app)

# Prueba para el endpoint de listar clientes
def test_listar_clientes():
    response = client.get(f"{settings.api_prefix}/clientes")
    assert response.status_code == 200
    assert response.json() == {"message": "Lista de clientes"}

# Prueba para el endpoint de crear cliente
def test_crear_cliente():
    response = client.post(f"{settings.api_prefix}/clientes", json={"nombre": "Juan", "email": "juan@example.com"})
    assert response.status_code == 200
    assert "Cliente creado" in response.json()["message"]