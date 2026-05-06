from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal

# Schema para crear una nota
class NotaCrear(BaseModel):
    estudiante_id: int
    materia_id: int
    profesor_id: int
    periodo: int
    nota: Decimal
    observacion: Optional[str] = None

# Schema para mostrar una nota
class NotaRespuesta(BaseModel):
    id: int
    estudiante_id: int
    materia_id: int
    profesor_id: int
    periodo: int
    nota: Decimal
    observacion: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

# Schema para mostrar el promedio de un estudiante
class PromedioRespuesta(BaseModel):
    estudiante_id: int
    materia_id: int
    periodo: int
    promedio: Decimal
    total_notas: int