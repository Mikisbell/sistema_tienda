# test_productos.py
import pytest
from fastapi import HTTPException, status
from app.models.productos import Producto
from app.services.productos import ProductoService
from pydantic import ValidationError
from app.schemas.productos import ProductoCreate
from fastapi.testclient import TestClient
from app.main import app
from typing import Generator
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from app.db.base import SessionLocal as BaseSessionLocal, get_db, Base  # Importa Base aquí
#from app.db.base import Base



@pytest.fixture
def client():
    with TestClient(app=app) as client:
        yield client


def test_reactivar_producto_existente(db):
    """Test para verificar la reactivación de un producto existente."""
    # Crear un producto inactivo en la base de datos
    producto_inactivo = Producto(
        nombre="Laptop HP",
        precio=1300.00,
        stock=5,
        categoria_id=1,
        activo=False,
    )
    db.add(producto_inactivo)
    db.commit()
    db.refresh(producto_inactivo)

    # Reactivar el producto
    producto_service = ProductoService(db)
    producto_reactivado = producto_service.marcar_producto_como_activo(producto_inactivo.id)

    # Verificar que el producto está activo
    assert producto_reactivado.activo is True




def test_reactivar_producto_inexistente(db):
    """Test para verificar el manejo de la reactivación de un producto inexistente."""
    producto_service = ProductoService(db)

    # Intentar reactivar un producto con un ID que no existe
    with pytest.raises(HTTPException) as exc_info:
        producto_service.marcar_producto_como_activo(999)  # ID que no existe

    # Verificar que se lanza una excepción HTTP 404
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == "Producto con ID 999 no encontrado"







def test_producto_reactivado_en_lista_activos(db):
    """Test para verificar que un producto reactivado aparece en la lista de activos."""
    # Crear un producto inactivo en la base de datos
    producto_inactivo = Producto(
        nombre="Laptop HP",
        precio=1300.00,
        stock=5,
        categoria_id=1,
        activo=False,
    )
    db.add(producto_inactivo)
    db.commit()
    db.refresh(producto_inactivo)

    # Reactivar el producto
    producto_service = ProductoService(db)
    producto_reactivado = producto_service.marcar_producto_como_activo(producto_inactivo.id)

    # Obtener la lista de productos activos
    productos_activos = db.query(Producto).filter(Producto.activo == True).all()

    # Verificar que el producto reactivado está en la lista de productos activos
    assert producto_reactivado in productos_activos

def test_crear_producto_con_precio_negativo():
    """Test para verificar la validación de precio negativo al crear un producto."""
    with pytest.raises(ValidationError):
        ProductoCreate(nombre="Producto Inválido", precio=-10.0, stock=10, categoria_id=1)

def test_crear_producto_con_stock_negativo():
    """Test para verificar la validación de stock negativo al crear un producto."""
    with pytest.raises(ValidationError):
        ProductoCreate(nombre="Producto Inválido", precio=10.0, stock=-1, categoria_id=1)






def test_reactivar_producto_ya_activo(client, db):
    """Test para verificar el manejo de la reactivación de un producto ya activo."""
    # Crear un producto activo en la base de datos para la prueba
    producto_activo = Producto(
        nombre="Producto Activo",
        precio=20.00,
        stock=2,
        categoria_id=2,
        activo=True,
    )
    db.add(producto_activo)
    db.commit()
    db.refresh(producto_activo)  # Añade esta línea

    # Intentar reactivar el producto ya activo
    response = client.put(f"/productos/{producto_activo.id}/reactivar")

    if response.status_code != status.HTTP_400_BAD_REQUEST:
        print(f"\n--- Respuesta inesperada ({response.status_code}): {response.json()} ---")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "El producto ya está activo"}







def test_import_product_create():
    """Test para verificar la importación del schema ProductoCreate."""
    from app.schemas.productos import ProductoCreate
    assert ProductoCreate is not None







def test_listar_productos(client, db):
    """Test para verificar la lista de productos, enfocándose en los creados en este test."""
    # No necesitas sobreescribir la dependencia aquí, ya que la fixture 'db' ya usa la base de datos de prueba
    # app.dependency_overrides[get_db] = override_get_db

    # Crear algunos productos en la base de datos con nombres específicos
    producto1_data = {"nombre": "Producto de Prueba 1", "precio": 10.0, "stock": 5, "categoria_id": 1, "activo": True}
    producto2_data = {"nombre": "Producto de Prueba 2", "precio": 20.0, "stock": 10, "categoria_id": 1, "activo": True}

    producto1 = Producto(**producto1_data)
    producto2 = Producto(**producto2_data)

    db.add(producto1)
    db.add(producto2)
    db.commit()
    db.refresh(producto1)
    db.refresh(producto2)

    # Llamar al endpoint para listar productos
    response = client.get("/productos")
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    print(f"Respuesta de la API: {response_data}")

    # Verificar que los productos que creaste están en la respuesta
    nombres_en_respuesta = {producto["nombre"] for producto in response_data}
    assert producto1.nombre in nombres_en_respuesta
    assert producto2.nombre in nombres_en_respuesta

    # No necesitas limpiar la sobreescritura aquí ya que la fixture 'create_test_database' se encarga de la configuración para toda la sesión
    # del app.dependency_overrides[get_db]


def test_crear_producto_con_datos_invalidos(client):
    """Test para verificar el manejo de datos inválidos al crear un producto."""
    # Intentar crear un producto con precio negativo
    response = client.post("/productos", json={
        "nombre": "Producto Inválido",
        "precio": -10.0,
        "stock": 5,
        "categoria_id": 1,
    })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_actualizar_producto(client, db):
    """Test para verificar la actualización de un producto existente."""
    # Crear un producto en la base de datos
    producto = Producto(nombre="Producto Original", precio=10.0, stock=5, categoria_id=1, activo=True)
    db.add(producto)
    db.commit()
    db.refresh(producto)

    # Actualizar el producto
    response = client.put(f"/productos/{producto.id}", json={
        "nombre": "Producto Actualizado",
        "precio": 20.0,
        "stock": 10,
        "categoria_id": 1,
    })
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["nombre"] == "Producto Actualizado"
    assert response.json()["precio"] == 20.0







def test_eliminar_producto(client, db):
    """Test para verificar la eliminación (marcado como inactivo) de un producto."""
    # Crear un producto en la base de datos
    producto = Producto(nombre="Producto a Eliminar", precio=10.0, stock=5, categoria_id=1, activo=True)
    db.add(producto)
    db.commit()
    db.refresh(producto)

    # Verificar que el producto está activo antes de eliminarlo
    assert producto.activo is True

    # Obtener una instancia del servicio con la sesión actual
    producto_service = ProductoService(db)

    # Eliminar el producto usando el servicio directamente
    producto_service.marcar_producto_como_inactivo(producto.id)

    # Obtener el producto directamente de la base de datos después de la eliminación
    producto_en_db = db.query(Producto).filter(Producto.id == producto.id).first()

    # Verificar que el producto está inactivo
    assert producto_en_db.activo is False, f"El producto con ID {producto.id} no se marcó como inactivo"