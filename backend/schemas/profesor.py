from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Schema para crear un profesor
class ProfesorCrear(BaseModel):
    colegio_id: int
    nombre: str
    apellido: str
    email: Optional[str] = None

# Schema para mostrar un profesor
class ProfesorRespuesta(BaseModel):
    id: int
    colegio_id: int
    nombre: str
    apellido: str
    email: Optional[str]
    rol: Optional[str]
    grado_asignado: Optional[str]
    materia_asignada_id: Optional[int]
    celular: Optional[str]
    foto_url: Optional[str]
    activo: bool
    created_at: datetime

    class Config:
        from_attributes = True