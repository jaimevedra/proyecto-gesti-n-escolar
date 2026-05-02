from sqlalchemy import Column, Integer, Boolean, TIMESTAMP, Text, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Nota(Base):
    __tablename__ = "notas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    estudiante_id = Column(Integer, ForeignKey("estudiantes.id"), nullable=False)
    materia_id = Column(Integer, ForeignKey("materias.id"), nullable=False)
    profesor_id = Column(Integer, ForeignKey("profesores.id"), nullable=False)
    periodo = Column(Integer, nullable=False)
    nota = Column(DECIMAL(4, 2), nullable=False)
    observacion = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())

    estudiante = relationship("Estudiante", back_populates="notas")
    materia = relationship("Materia", back_populates="notas")
    profesor = relationship("Profesor", back_populates="notas")