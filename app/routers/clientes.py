# app/routers/clientes.py
from fastapi import APIRouter

# Crea un router para los endpoints de clientes
router = APIRouter()

# Endpoint para listar clientes
@router.get("/")
def listar_clientes():
    """
    Devuelve una lista de clientes.
    """
    return {"message": "Lista de clientes"}

# Endpoint para crear un nuevo cliente
@router.post("/")
def crear_cliente():
    """
    Crea un nuevo cliente.
    """
    return {"message": "Cliente creado"}

# Endpoint para obtener los detalles de un cliente específico
@router.get("/{cliente_id}")
def obtener_cliente(cliente_id: int):
    """
    Devuelve los detalles de un cliente específico.

    Parámetros:
    - cliente_id (int): El ID del cliente que se desea obtener.
    """
    return {"message": f"Detalles del cliente {cliente_id}"}