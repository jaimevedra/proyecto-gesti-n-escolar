from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Schema para crear una materia
class MateriaCrear(BaseModel):
    colegio_id: int
    nombre: str
    descripcion: Optional[str] = None

# Schema para mostrar una materia
class MateriaRespuesta(BaseModel):
    id: int
    colegio_id: int
    nombre: str
    descripcion: Optional[str]
    activo: bool
    created_at: datetime

    class Config:
        from_attributes = True