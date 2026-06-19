from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.profesor import Profesor
from models.colegio import Colegio
from schemas.profesor import ProfesorCrear, ProfesorRespuesta
from typing import List, Optional
from pydantic import BaseModel
from auth import obtener_profesor_actual, encriptar_password

router = APIRouter(
    prefix="/profesores",
    tags=["Profesores"]
)

# Schema para editar perfil propio
class PerfilEditar(BaseModel):
    celular: Optional[str] = None
    password: Optional[str] = None
    foto_url: Optional[str] = None

# Schema para que el rector edite rol/asignacion
class AsignacionEditar(BaseModel):
    rol: Optional[str] = None
    grado_asignado: Optional[str] = None
    materia_asignada_id: Optional[int] = None

# Endpoint para crear un profesor (usa /auth/registro normalmente, este queda para casos internos)
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

# Endpoint para obtener todos los profesores (solo el rector)
@router.get("/", response_model=List[ProfesorRespuesta])
def obtener_profesores(
    db: Session = Depends(get_db),
    profesor_actual: Profesor = Depends(obtener_profesor_actual)
):
    if profesor_actual.rol != "rector":
        raise HTTPException(status_code=403, detail="Solo el rector puede ver todos los profesores")
    return db.query(Profesor).filter(Profesor.activo == True).all()

# Endpoint para obtener profesores por colegio (solo el rector)
@router.get("/colegio/{colegio_id}", response_model=List[ProfesorRespuesta])
def obtener_profesores_por_colegio(
    colegio_id: int,
    db: Session = Depends(get_db),
    profesor_actual: Profesor = Depends(obtener_profesor_actual)
):
    if profesor_actual.rol != "rector":
        raise HTTPException(status_code=403, detail="Solo el rector puede ver los profesores del colegio")
    return db.query(Profesor).filter(
        Profesor.colegio_id == colegio_id,
        Profesor.activo == True
    ).all()

# Endpoint para editar el perfil propio (cualquier profesor autenticado)
@router.patch("/perfil")
def editar_perfil_propio(
    datos: PerfilEditar,
    db: Session = Depends(get_db),
    profesor_actual: Profesor = Depends(obtener_profesor_actual)
):
    if datos.celular is not None:
        profesor_actual.celular = datos.celular
    if datos.foto_url is not None:
        profesor_actual.foto_url = datos.foto_url
    if datos.password:
        profesor_actual.password = encriptar_password(datos.password)

    db.commit()
    return {"mensaje": "Perfil actualizado correctamente"}

# Endpoint para que el rector edite la asignacion de un profesor
@router.patch("/{profesor_id}/asignacion")
def editar_asignacion(
    profesor_id: int,
    datos: AsignacionEditar,
    db: Session = Depends(get_db),
    profesor_actual: Profesor = Depends(obtener_profesor_actual)
):
    if profesor_actual.rol != "rector":
        raise HTTPException(status_code=403, detail="Solo el rector puede reasignar profesores")

    profesor = db.query(Profesor).filter(Profesor.id == profesor_id).first()
    if not profesor:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")

    if datos.rol is not None:
        profesor.rol = datos.rol
    if datos.grado_asignado is not None:
        profesor.grado_asignado = datos.grado_asignado
    if datos.materia_asignada_id is not None:
        profesor.materia_asignada_id = datos.materia_asignada_id

    db.commit()
    return {"mensaje": "Asignación actualizada correctamente"}