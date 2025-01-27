from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..auth import create_access_token, verify_password
from ..models import User

router = APIRouter(prefix="/auth", tags=["auth"])

# Modelo Pydantic para los datos de inicio de sesión
class LoginRequest(BaseModel):
    correo: str
    password: str

@router.post("/login")
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    """
    Inicia sesión con correo y contraseña.
    """
    # Busca al usuario en la base de datos
    user = db.query(User).filter(User.correo == credentials.correo).first()
    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )
    
    # Genera el token de acceso
    token = create_access_token(data={"sub": user.correo})
    
    # Retorna el token y el id del usuario
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": str(user.id)  # Convertir UUID a string
    }