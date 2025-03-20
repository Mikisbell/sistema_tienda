# app/models/categorias.py
from sqlalchemy import Column, Integer, String

from app.db.base import Base
from sqlalchemy.orm import relationship

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True, nullable=False)
    descripcion = Column(String, nullable=True)
    cantidad_productos = Column(Integer, default=0)  # Añade esta línea

    productos = relationship("Producto", back_populates="categoria")


