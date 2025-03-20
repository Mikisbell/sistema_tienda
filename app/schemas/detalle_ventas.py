# app/schemas/detalle_ventas.py
from typing import Optional

from pydantic import BaseModel

class DetalleVentaBase(BaseModel):
    venta_id: Optional[int] = None
    producto_id: Optional[int] = None
    cantidad: int
    precio_unitario: float
    subtotal: Optional[float] = None

class DetalleVentaCreate(DetalleVentaBase):
    pass

class DetalleVentaUpdate(DetalleVentaBase):
    id: int
    venta_id: Optional[int] = None
    producto_id: Optional[int] = None
    cantidad: Optional[int] = None
    precio_unitario: Optional[float] = None
    subtotal: Optional[float] = None

class DetalleVentaInDBBase(DetalleVentaBase):
    id: int

    class Config:
        orm_mode = True

class DetalleVenta(DetalleVentaInDBBase):
    pass