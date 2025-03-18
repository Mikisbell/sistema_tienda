from sqlalchemy.orm import Session
from app.models.productos import Producto
from app.schemas.productos import ProductoCreate, ProductoUpdate

class ProductoRepository:
    def __init__(self, db: Session):
        self.db = db

    def obtener_productos(self):
        return self.db.query(Producto).all()

    def obtener_producto_por_id(self, producto_id: int):
        return self.db.query(Producto).filter(Producto.id == producto_id).first()

    def crear_producto(self, producto: ProductoCreate):
        db_producto = Producto(**producto.dict())
        self.db.add(db_producto)
        self.db.commit()
        self.db.refresh(db_producto)
        return db_producto

    def actualizar_producto(self, producto_id: int, producto: ProductoUpdate):
        db_producto = self.obtener_producto_por_id(producto_id)
        if db_producto:
            for key, value in producto.dict().items():
                setattr(db_producto, key, value)
            self.db.commit()
            self.db.refresh(db_producto)
        return db_producto

    def eliminar_producto(self, producto_id: int):
        db_producto = self.obtener_producto_por_id(producto_id)
        if db_producto:
            self.db.delete(db_producto)
            self.db.commit()
        return db_producto
    
    def guardar_cambios(self):
        self.db.commit()
    
       