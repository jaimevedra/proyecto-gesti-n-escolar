from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

# Schema para crear un estudiante
class EstudianteCrear(BaseModel):
    colegio_id: int
    nombre: str
    apellido: str
    fecha_nacimiento: Optional[date] = None
    grado: str

# Schema para mostrar un estudiante
class EstudianteRespuesta(BaseModel):
    id: int
    colegio_id: int
    nombre: str
    apellido: str
    fecha_nacimiento: Optional[date]
    grado: str
    activo: bool
    created_at: datetime

    class Config:
        from_attributes = True