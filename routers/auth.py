from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..auth import create_access_token, verify_password
from ..models import User

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login(correo: str, password: str, db: Session = Depends(get_db)):
    """
    Inicia sesión con correo y contraseña.
    """
    user = db.query(User).filter(User.correo == correo).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales incorrectas")
    
    token = create_access_token(data={"sub": user.correo})
    return {"access_token": token, "token_type": "bearer"}
