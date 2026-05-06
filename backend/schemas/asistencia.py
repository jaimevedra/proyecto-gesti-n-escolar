from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

# Schema para crear asistencia
class AsistenciaCrear(BaseModel):
    estudiante_id: int
    materia_id: int
    profesor_id: int
    fecha: date
    presente: bool
    observacion: Optional[str] = None

# Schema para mostrar asistencia
class AsistenciaRespuesta(BaseModel):
    id: int
    estudiante_id: int
    materia_id: int
    profesor_id: int
    fecha: date
    presente: bool
    observacion: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

# Schema para mostrar resumen de asistencia
class ResumenAsistencia(BaseModel):
    estudiante_id: int
    materia_id: int
    total_clases: int
    clases_asistidas: int
    porcentaje_asistencia: float