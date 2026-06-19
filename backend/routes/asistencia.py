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
        raise HTTPException(status_code=404, detail="Asignatura no encontrada")
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

# Endpoint para obtener asistencia de un estudiante por asignatura

@router.get("/estudiante/{estudiante_id}/materia/{materia_id}", response_model=List[AsistenciaRespuesta])
def obtener_asistencia(
    estudiante_id: int,
    materia_id: int,
    db: Session = Depends(get_db),
    profesor_actual: Profesor = Depends(obtener_profesor_actual)
):
    registros = db.query(Asistencia).filter(
        Asistencia.estudiante_id == estudiante_id,
        Asistencia.materia_id == materia_id
    ).all()
    return registros

# Endpoint para calcular resumen de asistencia

@router.get("/resumen/{estudiante_id}/{materia_id}", response_model=ResumenAsistencia)
def resumen_asistencia(
    estudiante_id: int,
    materia_id: int,
    db: Session = Depends(get_db),
    profesor_actual: Profesor = Depends(obtener_profesor_actual)
):
    total = db.query(Asistencia).filter(
        Asistencia.estudiante_id == estudiante_id,
        Asistencia.materia_id == materia_id
    ).count()

    asistidas = db.query(Asistencia).filter(
        Asistencia.estudiante_id == estudiante_id,
        Asistencia.materia_id == materia_id,
        Asistencia.presente == True
    ).count()

    if total == 0:
        raise HTTPException(status_code=404, detail="No hay registros de asistencia")

    porcentaje = round((asistidas / total) * 100, 2)

    return ResumenAsistencia(
        estudiante_id=estudiante_id,
        materia_id=materia_id,
        total_clases=total,
        clases_asistidas=asistidas,
        porcentaje_asistencia=porcentaje
    )