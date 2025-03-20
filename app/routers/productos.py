# app/routers/productos.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.productos import ProductoCreate, ProductoUpdate, Producto
from app.services.productos import ProductoService



router = APIRouter()

@router.get("/", response_model=list[Producto], summary="Listar productos", description="Obtiene una lista de todos los productos activos.")
def listar_productos(db: Session = Depends(get_db)):
    producto_service = ProductoService(db)
    return producto_service.obtener_productos()

@router.get("/{producto_id}", response_model=Producto, summary="Obtener producto", description="Obtiene un producto por su ID.")
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    producto_service = ProductoService(db)
    producto = producto_service.obtener_producto_por_id(producto_id)
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {producto_id} no encontrado",
        )
    return producto

@router.post("/", response_model=Producto, status_code=status.HTTP_201_CREATED, summary="Crear producto", description="Crea un nuevo producto.")
def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    producto_service = ProductoService(db)
    return producto_service.crear_producto(producto)

@router.put("/{producto_id}", response_model=Producto, summary="Actualizar producto", description="Actualiza un producto existente.")
def actualizar_producto(producto_id: int, producto: ProductoUpdate, db: Session = Depends(get_db)):
    producto_service = ProductoService(db)
    return producto_service.actualizar_producto(producto_id, producto)






@router.delete("/{producto_id}")
def marcar_producto_como_inactivo(producto_id: int, db: Session = Depends(get_db)):
    producto_service = ProductoService(db)
    producto_service.marcar_producto_como_inactivo(producto_id)
    return {"message": "Producto marcado como inactivo"}







@router.put("/{producto_id}/reactivar", response_model=Producto, summary="Reactivar producto", description="Reactivar un producto marcado como inactivo.")
def reactivar_producto(producto_id: int, db: Session = Depends(get_db)):
    producto_service = ProductoService(db)
    return producto_service.marcar_producto_como_activo(producto_id)