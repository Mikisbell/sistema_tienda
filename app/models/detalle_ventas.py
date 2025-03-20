#app/models/detalle_ventas.py
from sqlalchemy import Column, Integer, ForeignKey, Numeric, Integer as IntegerType
from sqlalchemy.orm import relationship
from app.db.base import Base

class DetalleVenta(Base):
    __tablename__ = "detalle_ventas"

    id = Column(Integer, primary_key=True, index=True)
    venta_id = Column(Integer, ForeignKey("ventas.id", ondelete="CASCADE"))
    producto_id = Column(Integer, ForeignKey("productos.id", ondelete="CASCADE"))
    cantidad = Column(IntegerType, nullable=False)
    precio_unitario = Column(Numeric(8, 2), nullable=False)
    subtotal = Column(Numeric(10, 2))

    venta = relationship("Venta", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalles_venta")