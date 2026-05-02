from sqlalchemy import Column, Integer, Boolean, TIMESTAMP, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Asistencia(Base):
    __tablename__ = "asistencia"

    id = Column(Integer, primary_key=True, autoincrement=True)
    estudiante_id = Column(Integer, ForeignKey("estudiantes.id"), nullable=False)
    materia_id = Column(Integer, ForeignKey("materias.id"), nullable=False)
    profesor_id = Column(Integer, ForeignKey("profesores.id"), nullable=False)
    fecha = Column(Date, nullable=False)
    presente = Column(Boolean, nullable=False)
    observacion = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())

    estudiante = relationship("Estudiante", back_populates="asistencias")
    materia = relationship("Materia", back_populates="asistencias")
    profesor = relationship("Profesor", back_populates="asistencias")