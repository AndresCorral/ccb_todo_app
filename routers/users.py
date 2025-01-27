from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from uuid import UUID
from ..database import get_db
from ..models import User, UserCreate, UserUpdate
from ..crud import create_user, get_user, get_users, update_user, delete_user

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo usuario.
    """
    try:
        return create_user(db, user)
    except IntegrityError as e:
        db.rollback()  # Revertir la transacción si ocurre un error
        # Verificar si el error es por correo duplicado
        if "ix_user_correo" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El correo {user.correo} ya está registrado."
            )
        # Para otros errores de integridad, relanzar un error genérico
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear el usuario. Por favor, inténtalo nuevamente."
        )

@router.get("/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Obtiene una lista de usuarios.
    """
    return get_users(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=User)
def read_user(user_id: UUID, db: Session = Depends(get_db)):
    """
    Obtiene un usuario por su ID.
    """
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return user

@router.patch("/{user_id}", response_model=User)
def update_existing_user(user_id: UUID, updated_user: UserUpdate, db: Session = Depends(get_db)):
    """
    Actualiza un usuario existente.
    """
    user = update_user(db, user_id, updated_user)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_user(user_id: UUID, db: Session = Depends(get_db)):
    """
    Elimina un usuario por su ID, pero verifica si tiene tareas asociadas.
    """
    try:
        if not delete_user(db, user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user cannot be deleted because they have associated tasks. Please delete all tasks before removing the user."
        )