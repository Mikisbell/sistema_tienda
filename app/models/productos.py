# app/models/productos.py
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    precio = Column(Float)
    stock = Column(Integer)
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    activo = Column(Boolean, default=True)

    categoria = relationship("Categoria", back_populates="productos")
