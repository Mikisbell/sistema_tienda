# app/schemas/categorias.py
from typing import Optional

from pydantic import BaseModel, ConfigDict

class CategoriaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    cantidad_productos: Optional[int] = 0

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaUpdate(CategoriaBase):
    id: int

class CategoriaInDBBase(CategoriaBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class Categoria(CategoriaInDBBase):
    pass