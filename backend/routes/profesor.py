from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.profesor import Profesor
from models.colegio import Colegio
from schemas.profesor import ProfesorCrear, ProfesorRespuesta
from typing import List

router = APIRouter(
    prefix="/profesores",
    tags=["Profesores"]
)

# Endpoint para crear un profesor
@router.post("/", response_model=ProfesorRespuesta)
def crear_profesor(profesor: ProfesorCrear, db: Session = Depends(get_db)):
    colegio = db.query(Colegio).filter(Colegio.id == profesor.colegio_id).first()
    if not colegio:
        raise HTTPException(status_code=404, detail="Colegio no encontrado")
    
    nuevo_profesor = Profesor(
        colegio_id=profesor.colegio_id,
        nombre=profesor.nombre,
        apellido=profesor.apellido,
        email=profesor.email
    )
    db.add(nuevo_profesor)
    db.commit()
    db.refresh(nuevo_profesor)
    return nuevo_profesor

# Endpoint para obtener todos los profesores
@router.get("/", response_model=List[ProfesorRespuesta])
def obtener_profesores(db: Session = Depends(get_db)):
    profesores = db.query(Profesor).filter(Profesor.activo == True).all()
    return profesores

# Endpoint para obtener profesores por colegio
@router.get("/colegio/{colegio_id}", response_model=List[ProfesorRespuesta])
def obtener_profesores_por_colegio(colegio_id: int, db: Session = Depends(get_db)):
    profesores = db.query(Profesor).filter(
        Profesor.colegio_id == colegio_id,
        Profesor.activo == True
    ).all()
    return profesores