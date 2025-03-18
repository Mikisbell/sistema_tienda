#endpoint de categorias 
from fastapi import APIRouter

router = APIRouter()

@router.get("/categorias")
def listar_categorias():
    return {"message": "Lista de categorias"}