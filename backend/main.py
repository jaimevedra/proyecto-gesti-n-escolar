from fastapi import FastAPI
from database import Base, engine
from models import colegio, profesor, estudiante, materia, nota, asistencia
from routes import colegio as colegio_routes

# Crear las tablas si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Gestión Escolar",
    description="API para gestión de colegios rurales",
    version="1.0.0"
)

# Registrar rutas
app.include_router(colegio_routes.router)

@app.get("/")
def home():
    return {"mensaje": "Sistema de Gestión Escolar funcionando"}