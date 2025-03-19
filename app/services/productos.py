# service/productos.py
from fastapi import HTTPException, status
from app.repositories.productos import ProductoRepository
from app.schemas.productos import ProductoCreate, ProductoUpdate, Producto  # Importa el esquema Producto
from app.models.productos import Producto as ProductoModelo # Importa el modelo con un alias
from typing import List

class ProductoService:
    def __init__(self, db):
        """
        Inicializa el servicio de productos.

        Args:
            db: Sesión de la base de datos.
        """
        self.repo = ProductoRepository(db)
        self.db = db

    def obtener_productos(self) -> List[Producto]:
        """
        Obtiene todos los productos activos.

        Returns:
            List[Producto]: Lista de productos activos.
        """
        return self.db.query(ProductoModelo).filter(ProductoModelo.activo == True).all()

    def obtener_producto_por_id(self, producto_id: int):
        """
        Obtiene un producto por su ID.

        Args:
            producto_id (int): ID del producto.

        Returns:
            Producto: El producto encontrado.

        Raises:
            HTTPException: Si el producto no existe.
        """
        producto = self.repo.obtener_producto_por_id(producto_id)
        if not producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID {producto_id} no encontrado",
            )
        return producto

    def crear_producto(self, producto: ProductoCreate):
        """
        Crea un nuevo producto.

        Args:
            producto (ProductoCreate): Datos del producto a crear.

        Returns:
            Producto: El producto creado.
        """
        # Validar que el precio y el stock no sean negativos
        if producto.precio < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El precio no puede ser negativo",
            )
        if producto.stock < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El stock no puede ser negativo",
            )
        return self.repo.crear_producto(producto)

    def actualizar_producto(self, producto_id: int, producto: ProductoUpdate):
        """
        Actualiza un producto existente.

        Args:
            producto_id (int): ID del producto a actualizar.
            producto (ProductoUpdate): Datos actualizados del producto.

        Returns:
            Producto: El producto actualizado.

        Raises:
            HTTPException: Si el producto no existe.
        """
        db_producto = self.repo.obtener_producto_por_id(producto_id)
        if not db_producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID {producto_id} no encontrado",
            )
        return self.repo.actualizar_producto(producto_id, producto)
    





    def marcar_producto_como_inactivo(self, producto_id: int):
        db_producto = self.repo.obtener_producto_por_id(producto_id)
        if not db_producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID {producto_id} no encontrado",
            )
        db_producto.activo = False
        self.repo.guardar_cambios()  # Asegúrate de que los cambios se guarden
        self.db.refresh(db_producto)
        return db_producto
    









    def marcar_producto_como_activo(self, producto_id: int):
        """
        Marca un producto como activo.

        Args:
            producto_id (int): ID del producto a marcar como activo.

        Returns:
            Producto: El producto marcado como activo.

        Raises:
            HTTPException: Si el producto no existe o ya está activo.
        """
        db_producto = self.repo.obtener_producto_por_id(producto_id)
        if not db_producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID {producto_id} no encontrado",
            )
        if db_producto.activo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El producto ya está activo",
            )
        db_producto.activo = True
        self.repo.guardar_cambios()
        return db_producto