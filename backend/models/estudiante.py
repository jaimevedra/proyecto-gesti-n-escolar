from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Estudiante(Base):
    __tablename__ = "estudiantes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    colegio_id = Column(Integer, ForeignKey("colegios.id"), nullable=False)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    fecha_nacimiento = Column(Date)
    grado = Column(String(20), nullable=False)
    activo = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    colegio = relationship("Colegio", back_populates="estudiantes")
    notas = relationship("Nota", back_populates="estudiante")
    asistencias = relationship("Asistencia", back_populates="estudiante")