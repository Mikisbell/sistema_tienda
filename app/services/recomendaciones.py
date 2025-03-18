from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.recomendaciones import RecomendacionService

router = APIRouter()

@router.get("/recomendaciones/{cliente_id}")
def obtener_recomendaciones(cliente_id: int, db: Session = Depends(get_db)):
    recomendacion_service = RecomendacionService(db)
    recomendaciones = recomendacion_service.obtener_recomendaciones(cliente_id)
    
    if not recomendaciones:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron recomendaciones para el cliente"
        )
    
    return {"recomendaciones": recomendaciones}
