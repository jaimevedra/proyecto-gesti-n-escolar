from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Profesor(Base):
    __tablename__ = "profesores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    colegio_id = Column(Integer, ForeignKey("colegios.id"), nullable=False)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    password = Column(String(255))
    rol = Column(String(20), default="profesor")
    grado_asignado = Column(String(20))
    materia_asignada_id = Column(Integer, ForeignKey("materias.id"), nullable=True)
    celular = Column(String(20))
    foto_url = Column(Text)
    activo = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    colegio = relationship("Colegio", back_populates="profesores")
    notas = relationship("Nota", back_populates="profesor")
    asistencias = relationship("Asistencia", back_populates="profesor")