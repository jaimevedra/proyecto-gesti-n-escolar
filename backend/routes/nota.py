from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models.nota import Nota
from models.estudiante import Estudiante
from models.materia import Materia
from models.profesor import Profesor
from schemas.nota import NotaCrear, NotaRespuesta, PromedioRespuesta
from typing import List
from auth import obtener_profesor_actual
from models.profesor import Profesor

router = APIRouter(
    prefix="/notas",
    tags=["Notas"]
)

# Endpoint para registrar una nota
@router.post("/", response_model=NotaRespuesta)
def crear_nota(
    nota: NotaCrear,
    db: Session = Depends(get_db),
    profesor_actual: Profesor = Depends(obtener_profesor_actual)
):
    if not db.query(Estudiante).filter(Estudiante.id == nota.estudiante_id).first():
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    if not db.query(Materia).filter(Materia.id == nota.materia_id).first():
        raise HTTPException(status_code=404, detail="Materia no encontrada")
    if not db.query(Profesor).filter(Profesor.id == nota.profesor_id).first():
        raise HTTPException(status_code=404, detail="Profesor no encontrado")

    nueva_nota = Nota(
        estudiante_id=nota.estudiante_id,
        materia_id=nota.materia_id,
        profesor_id=nota.profesor_id,
        periodo=nota.periodo,
        nota=nota.nota,
        observacion=nota.observacion
    )
    db.add(nueva_nota)
    db.commit()
    db.refresh(nueva_nota)
    return nueva_nota