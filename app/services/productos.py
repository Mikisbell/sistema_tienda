from fastapi import HTTPException, status
from app.repositories.productos import ProductoRepository
from app.schemas.productos import ProductoCreate, ProductoUpdate

class ProductoService:
    def __init__(self, db):
        self.repo = ProductoRepository(db)

    def obtener_productos(self):
        return self.repo.obtener_productos()

    def obtener_producto_por_id(self, producto_id: int):
        producto = self.repo.obtener_producto_por_id(producto_id)
        if not producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado",
            )
        return producto

    def crear_producto(self, producto: ProductoCreate):
        return self.repo.crear_producto(producto)

    def actualizar_producto(self, producto_id: int, producto: ProductoUpdate):
        return self.repo.actualizar_producto(producto_id, producto)

    def marcar_producto_como_inactivo(self, producto_id: int):
            db_producto = self.repo.obtener_producto_por_id(producto_id)
            if not db_producto:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Producto no encontrado",
                )
            db_producto.activo = False  # Marcar el producto como inactivo
            self.repo.guardar_cambios()
            return db_producto