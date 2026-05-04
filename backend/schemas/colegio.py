from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Schema para crear un colegio (datos que llegan a la API)
class ColegioCrear(BaseModel):
    nombre: str
    municipio: str
    departamento: str

# Schema para mostrar un colegio (datos que devuelve la API)
class ColegioRespuesta(BaseModel):
    id: int
    nombre: str
    municipio: str
    departamento: str
    activo: bool
    created_at: datetime

    class Config:
        from_attributes = True