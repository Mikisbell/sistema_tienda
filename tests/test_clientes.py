from fastapi.testclient import TestClient
from app.main import app  # Importa app desde app.main

# Crea un cliente de prueba para interactuar con la aplicación
client = TestClient(app)

# Prueba para el endpoint de listar clientes
def test_listar_clientes():
    response = client.get("/clientes")
    assert response.status_code == 200
    assert response.json() == {"message": "Lista de clientes"}

# Prueba para el endpoint de crear cliente
def test_crear_cliente():
    response = client.post("/clientes", json={"nombre": "Juan", "email": "juan@example.com"})
    assert response.status_code == 200
    assert "Cliente creado" in response.json()["message"]