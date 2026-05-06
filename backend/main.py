from fastapi import FastAPI
from database import Base, engine
from models import colegio, profesor, estudiante, materia, nota, asistencia
from routes import colegio as colegio_routes
from routes import profesor as profesor_routes
from routes import estudiante as estudiante_routes
from routes import nota as nota_routes
from routes import asistencia as asistencia_routes
from routes import materia as materia_routes

# Crear las tablas si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Gestión Escolar",
    description="API para gestión de colegios rurales",
    version="1.0.0"
)

# Registrar rutas
app.include_router(colegio_routes.router)
app.include_router(profesor_routes.router)
app.include_router(estudiante_routes.router)
app.include_router(materia_routes.router)
app.include_router(nota_routes.router)
app.include_router(asistencia_routes.router)

@app.get("/")
def home():
    return {"mensaje": "Sistema de Gestión Escolar funcionando"}