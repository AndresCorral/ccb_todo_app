from sqlmodel import Session, select
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from uuid import UUID
from .models import User, Task, UserCreate, TaskCreate, TaskStatus, UserUpdate, TaskUpdate

# Operaciones CRUD para Usuarios

def create_user(db: Session, user: UserCreate):
    # Verificar si el correo ya existe
    stmt = select(User).where(User.correo == user.correo)
    result = db.exec(stmt).scalar_one_or_none()
    if result:
        raise ValueError(f"El correo {user.correo} ya está registrado.")

    # Crear un nuevo usuario si no existe
    db_user = User(**user.dict())
    db.add(db_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("Error al guardar el usuario. Revisa los datos proporcionados.")
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: UUID) -> Optional[User]:
    """
    Obtiene un usuario por su ID.
    """
    statement = select(User).where(User.id == user_id)
    return db.exec(statement).first()

def get_user_by_email(db: Session, correo: str) -> Optional[User]:
    """
    Obtiene un usuario por su correo electrónico.
    """
    statement = select(User).where(User.correo == correo)
    return db.exec(statement).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """
    Obtiene una lista de usuarios con paginación.
    """
    statement = select(User).offset(skip).limit(limit)
    return db.exec(statement).all()

def update_user(db: Session, user_id: UUID, updated_user: UserUpdate) -> Optional[User]:
    """
    Actualiza un usuario existente.
    """
    statement = select(User).where(User.id == user_id)
    user = db.exec(statement).first()
    if not user:
        return None

    # Actualizar solo los campos proporcionados
    for key, value in updated_user.model_dump(exclude_unset=True).items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: UUID) -> bool:
    """
    Elimina un usuario por su ID.
    """
    statement = select(User).where(User.id == user_id)
    user = db.exec(statement).first()
    if not user:
        return False

    db.delete(user)
    db.commit()
    return True

# Operaciones CRUD para Tareas

def create_task(db: Session, task: TaskCreate) -> Task:
    """
    Crea una nueva tarea en la base de datos.
    """
    db_task = Task(**task.model_dump())  # Usar model_dump() en lugar de dict()
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_task(db: Session, task_id: UUID) -> Optional[Task]:
    """
    Obtiene una tarea por su ID.
    """
    statement = select(Task).where(Task.id == task_id)
    return db.exec(statement).first()

def get_tasks(db: Session, skip: int = 0, limit: int = 100) -> List[Task]:
    """
    Obtiene una lista de tareas con paginación.
    """
    statement = select(Task).offset(skip).limit(limit)
    return db.exec(statement).all()

def get_tasks_by_user(db: Session, user_id: UUID) -> List[Task]:
    """
    Obtiene todas las tareas de un usuario específico.
    """
    statement = select(Task).where(Task.user_id == user_id)
    return db.exec(statement).all()

def update_task(db: Session, task_id: UUID, updated_task: TaskUpdate) -> Optional[Task]:
    """
    Actualiza una tarea existente.
    """
    statement = select(Task).where(Task.id == task_id)
    task = db.exec(statement).first()
    if not task:
        return None

    # Actualizar solo los campos proporcionados
    for key, value in updated_task.model_dump(exclude_unset=True).items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task

def update_task_status(db: Session, task_id: UUID, new_status: TaskStatus) -> Optional[Task]:
    """
    Cambia el estado de una tarea.
    """
    statement = select(Task).where(Task.id == task_id)
    task = db.exec(statement).first()
    if not task:
        return None

    task.task_status = new_status
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task_id: UUID) -> bool:
    """
    Elimina una tarea por su ID.
    """
    statement = select(Task).where(Task.id == task_id)
    task = db.exec(statement).first()
    if not task:
        return False

    db.delete(task)
    db.commit()
    return True