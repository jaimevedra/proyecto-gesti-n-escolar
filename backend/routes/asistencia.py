from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models.asistencia import Asistencia
from models.estudiante import Estudiante
from models.materia import Materia
from models.profesor import Profesor
from schemas.asistencia import AsistenciaCrear, AsistenciaRespuesta, ResumenAsistencia
from typing import List
from auth import obtener_profesor_actual
from models.profesor import Profesor

router = APIRouter(
    prefix="/asistencia",
    tags=["Asistencia"]
)

# Endpoint para registrar asistencia
@router.post("/", response_model=AsistenciaRespuesta)
def registrar_asistencia(
    asistencia: AsistenciaCrear,
    db: Session = Depends(get_db),
    profesor_actual: Profesor = Depends(obtener_profesor_actual)
):
    if not db.query(Estudiante).filter(Estudiante.id == asistencia.estudiante_id).first():
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    if not db.query(Materia).filter(Materia.id == asistencia.materia_id).first():
        raise HTTPException(status_code=404, detail="Materia no encontrada")
    if not db.query(Profesor).filter(Profesor.id == asistencia.profesor_id).first():
        raise HTTPException(status_code=404, detail="Profesor no encontrado")

    nuevo_registro = Asistencia(
        estudiante_id=asistencia.estudiante_id,
        materia_id=asistencia.materia_id,
        profesor_id=asistencia.profesor_id,
        fecha=asistencia.fecha,
        presente=asistencia.presente,
        observacion=asistencia.observacion
    )
    db.add(nuevo_registro)
    db.commit()
    db.refresh(nuevo_registro)
    return nuevo_registro