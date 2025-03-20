#app/routers/categorias.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.categorias import CategoriaCreate, CategoriaUpdate, Categoria
from app.services.categorias import categoria_service
from app.db.session import get_db

# Define el router con un prefijo y etiquetas para la documentación de Swagger
router = APIRouter(prefix="/api/v1/categorias", tags=["categorias"])

@router.post("/", response_model=Categoria, status_code=status.HTTP_201_CREATED)
def create_categoria(categoria_in: CategoriaCreate, db: Session = Depends(get_db)):
    """
    Crea una nueva categoría.
    """
    return categoria_service.create_categoria(categoria_in=categoria_in, db=db)

@router.get("/{categoria_id}", response_model=Categoria)
def read_categoria(categoria_id: int, db: Session = Depends(get_db)):
    """
    Obtiene una categoría por su ID.
    """
    return categoria_service.get_categoria(categoria_id=categoria_id, db=db)

@router.put("/{categoria_id}", response_model=Categoria)
def update_categoria(categoria_id: int, categoria_in: CategoriaUpdate, db: Session = Depends(get_db)):
    """
    Actualiza una categoría existente.
    """
    return categoria_service.update_categoria(categoria_id=categoria_id, categoria_in=categoria_in, db=db)

@router.delete("/{categoria_id}", response_model=Categoria)
def delete_categoria(categoria_id: int, db: Session = Depends(get_db)):
    """
    Elimina una categoría por su ID.
    """
    return categoria_service.delete_categoria(categoria_id=categoria_id, db=db)