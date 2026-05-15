from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models.nota import Nota
from models.estudiante import Estudiante
from models.materia import Materia
from models.profesor import Profesor
from auth import obtener_profesor_actual
from pydantic import BaseModel
from typing import List
import httpx
import json

router = APIRouter(
    prefix="/ia",
    tags=["Inteligencia Artificial"]
)

# Schema para la respuesta del análisis
class EstudianteEnRiesgo(BaseModel):
    estudiante_id: int
    nombre: str
    apellido: str
    grado: str
    promedio: float
    total_notas: int

class ConsultaIA(BaseModel):
    pregunta: str
    estudiante_id: int

# Endpoint para obtener estudiantes con bajo rendimiento
@router.get("/estudiantes-en-riesgo/{colegio_id}/{periodo}", response_model=List[EstudianteEnRiesgo])
def obtener_estudiantes_en_riesgo(
    colegio_id: int,
    periodo: int,
    umbral: float = 3.0,
    db: Session = Depends(get_db),
    profesor_actual: Profesor = Depends(obtener_profesor_actual)
):
    resultados = db.query(
        Estudiante.id,
        Estudiante.nombre,
        Estudiante.apellido,
        Estudiante.grado,
        func.avg(Nota.nota).label("promedio"),
        func.count(Nota.id).label("total_notas")
    ).join(Nota, Nota.estudiante_id == Estudiante.id)\
     .filter(
        Estudiante.colegio_id == colegio_id,
        Nota.periodo == periodo
    ).group_by(
        Estudiante.id,
        Estudiante.nombre,
        Estudiante.apellido,
        Estudiante.grado
    ).having(
        func.avg(Nota.nota) < umbral
    ).all()

    return [
        EstudianteEnRiesgo(
            estudiante_id=r.id,
            nombre=r.nombre,
            apellido=r.apellido,
            grado=r.grado,
            promedio=round(float(r.promedio), 2),
            total_notas=r.total_notas
        )
        for r in resultados
    ]

# Endpoint para consultar la IA sobre un estudiante
@router.post("/consultar")
async def consultar_ia(
    consulta: ConsultaIA,
    db: Session = Depends(get_db),
    profesor_actual: Profesor = Depends(obtener_profesor_actual)
):
    estudiante = db.query(Estudiante).filter(Estudiante.id == consulta.estudiante_id).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    notas = db.query(Nota).filter(Nota.estudiante_id == consulta.estudiante_id).all()

    resumen_notas = []
    for n in notas:
        materia = db.query(Materia).filter(Materia.id == n.materia_id).first()
        resumen_notas.append({
            "materia": materia.nombre if materia else "Desconocida",
            "nota": float(n.nota),
            "periodo": n.periodo
        })

    contexto = f"""
Eres un asistente educativo. Un profesor necesita ayuda con un estudiante.

Estudiante: {estudiante.nombre} {estudiante.apellido}, grado {estudiante.grado}
Notas: {json.dumps(resumen_notas, ensure_ascii=False)}

Pregunta: {consulta.pregunta}

Da recomendaciones prácticas y cortas para mejorar el rendimiento del estudiante.
"""

    async with httpx.AsyncClient() as client:
        respuesta = await client.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "tinyllama",
                "prompt": contexto,
                "stream": False
            },
            timeout=60.0
        )

    if respuesta.status_code != 200:
        raise HTTPException(status_code=500, detail="Error al consultar la IA")

    datos = respuesta.json()
    texto_respuesta = datos["response"]

    return {
        "estudiante": f"{estudiante.nombre} {estudiante.apellido}",
        "respuesta_ia": texto_respuesta
    }