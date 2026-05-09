from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from models.profesor import Profesor
from auth import encriptar_password, verificar_password, crear_token
from pydantic import BaseModel

router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"]
)

# Schema para registrar profesor con password
class ProfesorRegistro(BaseModel):
    colegio_id: int
    nombre: str
    apellido: str
    email: str
    password: str

# Endpoint para registrar un profesor con password
@router.post("/registro")
def registrar_profesor(datos: ProfesorRegistro, db: Session = Depends(get_db)):
    profesor_existe = db.query(Profesor).filter(Profesor.email == datos.email).first()
    if profesor_existe:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    nuevo_profesor = Profesor(
        colegio_id=datos.colegio_id,
        nombre=datos.nombre,
        apellido=datos.apellido,
        email=datos.email,
        password=encriptar_password(datos.password)
    )
    db.add(nuevo_profesor)
    db.commit()
    db.refresh(nuevo_profesor)
    return {"mensaje": "Profesor registrado correctamente", "id": nuevo_profesor.id}

# Endpoint para iniciar sesión
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    profesor = db.query(Profesor).filter(Profesor.email == form_data.username).first()
    if not profesor:
        raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")
    if not verificar_password(form_data.password, profesor.password):
        raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")

    token = crear_token({"sub": profesor.email})
    return {
        "access_token": token,
        "token_type": "bearer",
        "nombre": profesor.nombre,
        "apellido": profesor.apellido
    }