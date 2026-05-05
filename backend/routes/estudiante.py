from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.estudiante import Estudiante
from models.colegio import Colegio
from schemas.estudiante import EstudianteCrear, EstudianteRespuesta
from typing import List

router = APIRouter(
    prefix="/estudiantes",
    tags=["Estudiantes"]
)

# Endpoint para crear un estudiante
@router.post("/", response_model=EstudianteRespuesta)
def crear_estudiante(estudiante: EstudianteCrear, db: Session = Depends(get_db)):
    colegio = db.query(Colegio).filter(Colegio.id == estudiante.colegio_id).first()
    if not colegio:
        raise HTTPException(status_code=404, detail="Colegio no encontrado")

    nuevo_estudiante = Estudiante(
        colegio_id=estudiante.colegio_id,
        nombre=estudiante.nombre,
        apellido=estudiante.apellido,
        fecha_nacimiento=estudiante.fecha_nacimiento,
        grado=estudiante.grado
    )
    db.add(nuevo_estudiante)
    db.commit()
    db.refresh(nuevo_estudiante)
    return nuevo_estudiante

# Endpoint para obtener todos los estudiantes
@router.get("/", response_model=List[EstudianteRespuesta])
def obtener_estudiantes(db: Session = Depends(get_db)):
    estudiantes = db.query(Estudiante).filter(Estudiante.activo == True).all()
    return estudiantes

# Endpoint para obtener estudiantes por colegio
@router.get("/colegio/{colegio_id}", response_model=List[EstudianteRespuesta])
def obtener_estudiantes_por_colegio(colegio_id: int, db: Session = Depends(get_db)):
    estudiantes = db.query(Estudiante).filter(
        Estudiante.colegio_id == colegio_id,
        Estudiante.activo == True
    ).all()
    return estudiantes

# Endpoint para obtener estudiantes por grado
@router.get("/colegio/{colegio_id}/grado/{grado}", response_model=List[EstudianteRespuesta])
def obtener_estudiantes_por_grado(colegio_id: int, grado: str, db: Session = Depends(get_db)):
    estudiantes = db.query(Estudiante).filter(
        Estudiante.colegio_id == colegio_id,
        Estudiante.grado == grado,
        Estudiante.activo == True
    ).all()
    return estudiantes