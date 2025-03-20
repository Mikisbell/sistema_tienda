# app/repositories/categorias.py
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.categorias import Categoria
from app.schemas.categorias import CategoriaCreate, CategoriaUpdate
# Assuming ModelType is defined somewhere, if not, remove it from the import

class CategoriaRepository:
    def __init__(self, model: type[Categoria]):
        self.model = model

    def get(self, db: Session, id: int) -> Optional[Categoria]:
        """
        Obtiene una categoría por su ID.
        """
        return db.query(self.model).filter(self.model.id == id).first()

    def create(self, db: Session, *, obj_in: CategoriaCreate) -> Categoria:
        """
        Crea una nueva categoría.
        """
        db_obj = self.model(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: Categoria, obj_in: CategoriaUpdate) -> Categoria:
        """
        Actualiza una categoría existente.
        """
        obj_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            setattr(db_obj, field, obj_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, id: int) -> Categoria:
            """
            Elimina una categoría por su ID.
            """
            obj = db.get(self.model, id)
            db.delete(obj)
            db.commit()
            return obj

# Instancia del repositorio para ser utilizada en las rutas
categoria = CategoriaRepository(Categoria)