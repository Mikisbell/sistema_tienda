from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.productos import ProductoCreate, ProductoUpdate, Producto
from app.services.productos import ProductoService

router = APIRouter()

# Listar todos los productos
@router.get("/productos", response_model=list[Producto])
def listar_productos(db: Session = Depends(get_db)):
    producto_service = ProductoService(db)
    return producto_service.obtener_productos()

# Obtener un producto por ID
@router.get("/productos/{producto_id}", response_model=Producto)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    producto_service = ProductoService(db)
    producto = producto_service.obtener_producto_por_id(producto_id)
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado",
        )
    return producto

# Crear un nuevo producto
@router.post("/productos", response_model=Producto, status_code=status.HTTP_201_CREATED)
def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    producto_service = ProductoService(db)
    return producto_service.crear_producto(producto)

# Actualizar un producto existente
@router.put("/productos/{producto_id}", response_model=Producto)
def actualizar_producto(producto_id: int, producto: ProductoUpdate, db: Session = Depends(get_db)):
    producto_service = ProductoService(db)
    return producto_service.actualizar_producto(producto_id, producto)

# Eliminar un producto
@router.delete("/productos/{producto_id}")
def marcar_producto_como_inactivo(producto_id: int, db: Session = Depends(get_db)):
    producto_service = ProductoService(db)
    producto_service.marcar_producto_como_inactivo(producto_id)
    return {"message": "Producto marcado como inactivo"}