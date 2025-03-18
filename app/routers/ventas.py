#Endpoint de ventas
from fastapi import APIRouter

router = APIRouter()

@router.get("/ventas")
def listar_ventas():
    return {"message": "Lista de solo ventas"}