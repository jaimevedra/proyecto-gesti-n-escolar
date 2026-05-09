from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from models.profesor import Profesor

# Configuración de seguridad
SECRET_KEY = "sge_escolar_clave_secreta_2026"
ALGORITHM = "HS256"
TIEMPO_EXPIRACION = 60  # minutos

# Configuración de encriptación
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Funciones de contraseña
def encriptar_password(password: str) -> str:
    return pwd_context.hash(password)

def verificar_password(password: str, hash: str) -> bool:
    return pwd_context.verify(password, hash)

# Funciones de token
def crear_token(data: dict) -> str:
    datos = data.copy()
    expiracion = datetime.utcnow() + timedelta(minutes=TIEMPO_EXPIRACION)
    datos.update({"exp": expiracion})
    return jwt.encode(datos, SECRET_KEY, algorithm=ALGORITHM)

def obtener_profesor_actual(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    excepcion = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise excepcion
    except JWTError:
        raise excepcion

    profesor = db.query(Profesor).filter(Profesor.email == email).first()
    if profesor is None:
        raise excepcion
    return profesor