from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Materia(Base):
    __tablename__ = "materias"

    id = Column(Integer, primary_key=True, autoincrement=True)
    colegio_id = Column(Integer, ForeignKey("colegios.id"), nullable=False)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    activo = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    colegio = relationship("Colegio", back_populates="materias")
    notas = relationship("Nota", back_populates="materia")
    asistencias = relationship("Asistencia", back_populates="materia")