# schema/productos.py
# Description: Pydantic schemas for productos
#from pydantic import BaseModel, ConfigDict
#import pytest
#from pydantic import ValidationError
#from app.schemas.productos import ProductoBase
from pydantic import BaseModel, Field, ConfigDict
from pydantic import BaseModel


class ProductoBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre del producto")
    precio: float = Field(..., gt=0, description="Precio del producto (debe ser mayor que 0)")
    stock: int = Field(..., ge=0, description="Stock del producto (no puede ser negativo)")
    categoria_id: int = Field(..., description="ID de la categoría del producto")

class ProductoCreate(ProductoBase):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "nombre": "Laptop HP",
                "precio": 1300.00,
                "stock": 5,
                "categoria_id": 1,
            }
        },
    )
    
class ProductoUpdate(ProductoBase):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "nombre": "Laptop HP Actualizada",
                "precio": 1200.00,
                "stock": 10,
                "categoria_id": 1,
            }
        },
    )

class Producto(ProductoBase):
    id: int
    model_config = ConfigDict(from_attributes=True)