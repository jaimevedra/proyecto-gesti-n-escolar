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

router = APIRouter(
    prefix="/notas",
    tags=["Notas"]
)

# Endpoint para registrar una nota
@router.post("/", response_model=NotaRespuesta)
def crear_nota(nota: NotaCrear, db: Session = Depends(get_db)):
    # Verificar que existen el estudiante, materia y profesor
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

# Endpoint para obtener notas de un estudiante
@router.get("/estudiante/{estudiante_id}", response_model=List[NotaRespuesta])
def obtener_notas_estudiante(estudiante_id: int, db: Session = Depends(get_db)):
    notas = db.query(Nota).filter(Nota.estudiante_id == estudiante_id).all()
    return notas

# Endpoint para calcular el promedio de un estudiante por materia y periodo
@router.get("/promedio/{estudiante_id}/{materia_id}/{periodo}", response_model=PromedioRespuesta)
def obtener_promedio(estudiante_id: int, materia_id: int, periodo: int, db: Session = Depends(get_db)):
    resultado = db.query(
        func.avg(Nota.nota).label("promedio"),
        func.count(Nota.id).label("total_notas")
    ).filter(
        Nota.estudiante_id == estudiante_id,
        Nota.materia_id == materia_id,
        Nota.periodo == periodo
    ).first()

    if not resultado.promedio:
        raise HTTPException(status_code=404, detail="No hay notas registradas")

    return PromedioRespuesta(
        estudiante_id=estudiante_id,
        materia_id=materia_id,
        periodo=periodo,
        promedio=round(resultado.promedio, 2),
        total_notas=resultado.total_notas
    )