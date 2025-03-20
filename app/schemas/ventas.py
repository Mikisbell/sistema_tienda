# app/schemas/ventas.py
from typing import Optional
from datetime import datetime

from pydantic import BaseModel

class VentaBase(BaseModel):
    cliente_id: Optional[int] = None
    total: float

class VentaCreate(VentaBase):
    pass

class VentaUpdate(VentaBase):
    id: int
    cliente_id: Optional[int] = None # Permitir actualizar el cliente si es necesario
    total: Optional[float] = None     # Permitir actualizar el total si es necesario
    necesita_actualizacion: Optional[bool] = None # Permitir actualizar este flag

class VentaInDBBase(VentaBase):
    id: int
    fecha_venta: datetime
    necesita_actualizacion: bool

    class Config:
        orm_mode = True

class Venta(VentaInDBBase):
    pass