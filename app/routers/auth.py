#endpoint de autenticación
from fastapi import APIRouter

router = APIRouter()

@router.get("/auth")
def listar_categorias():
    return {"message": "Esta es la autenticación"}