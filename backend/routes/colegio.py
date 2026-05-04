from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.colegio import Colegio
from schemas.colegio import ColegioCrear, ColegioRespuesta
from typing import List

router = APIRouter(
    prefix="/colegios",
    tags=["Colegios"]
)

# Endpoint para crear un colegio
@router.post("/", response_model=ColegioRespuesta)
def crear_colegio(colegio: ColegioCrear, db: Session = Depends(get_db)):
    nuevo_colegio = Colegio(
        nombre=colegio.nombre,
        municipio=colegio.municipio,
        departamento=colegio.departamento
    )
    db.add(nuevo_colegio)
    db.commit()
    db.refresh(nuevo_colegio)
    return nuevo_colegio

# Endpoint para consultar todos los colegios
@router.get("/", response_model=List[ColegioRespuesta])
def obtener_colegios(db: Session = Depends(get_db)):
    colegios = db.query(Colegio).filter(Colegio.activo == True).all()
    return colegios