from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.materia import Materia
from models.colegio import Colegio
from schemas.materia import MateriaCrear, MateriaRespuesta
from typing import List

router = APIRouter(
    prefix="/materias",
    tags=["Materias"]
)

# Endpoint para crear una materia
@router.post("/", response_model=MateriaRespuesta)
def crear_materia(materia: MateriaCrear, db: Session = Depends(get_db)):
    colegio = db.query(Colegio).filter(Colegio.id == materia.colegio_id).first()
    if not colegio:
        raise HTTPException(status_code=404, detail="Colegio no encontrado")

    nueva_materia = Materia(
        colegio_id=materia.colegio_id,
        nombre=materia.nombre,
        descripcion=materia.descripcion
    )
    db.add(nueva_materia)
    db.commit()
    db.refresh(nueva_materia)
    return nueva_materia

# Endpoint para obtener materias por colegio
@router.get("/colegio/{colegio_id}", response_model=List[MateriaRespuesta])
def obtener_materias_por_colegio(colegio_id: int, db: Session = Depends(get_db)):
    materias = db.query(Materia).filter(
        Materia.colegio_id == colegio_id,
        Materia.activo == True
    ).all()
    return materias