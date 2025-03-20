# app/services/categorias.py
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.categorias import CategoriaCreate, CategoriaUpdate, Categoria
from app.repositories.categorias import categoria
from app.db.session import get_db

class CategoriaService:
    def __init__(self, categoria_repo):
        self.categoria_repo = categoria_repo

    def create_categoria(self, categoria_in: CategoriaCreate, db: Session):
        return self.categoria_repo.create(db=db, obj_in=categoria_in)

    def get_categoria(self, categoria_id: int, db: Session):
        db_categoria = self.categoria_repo.get(db, id=categoria_id)
        if db_categoria is None:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
        return db_categoria

    def update_categoria(self, categoria_id: int, categoria_in: CategoriaUpdate, db: Session):
        db_categoria = self.categoria_repo.get(db, id=categoria_id)
        if db_categoria is None:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
        return self.categoria_repo.update(db=db, db_obj=db_categoria, obj_in=categoria_in)

    def delete_categoria(self, categoria_id: int, db: Session):
        db_categoria = self.categoria_repo.get(db, id=categoria_id)
        if db_categoria is None:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
        return self.categoria_repo.remove(db=db, id=categoria_id)

# Instancia del servicio para ser utilizada en las rutas
categoria_service = CategoriaService(categoria)