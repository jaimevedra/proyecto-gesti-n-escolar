from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Colegio(Base):
    __tablename__ = "colegios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    municipio = Column(String(100), nullable=False)
    departamento = Column(String(100), nullable=False)
    activo = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    profesores = relationship("Profesor", back_populates="colegio")
    estudiantes = relationship("Estudiante", back_populates="colegio")
    materias = relationship("Materia", back_populates="colegio")