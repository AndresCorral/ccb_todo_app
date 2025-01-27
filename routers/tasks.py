from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlmodel import Session, select
from typing import List
from uuid import UUID
from ..database import get_db
from ..models import Task, TaskCreate, User, TaskUpdate
from ..crud import create_task, get_task, update_task, update_task_status, delete_task, get_tasks_by_user
from ..schemas import TaskResponse
from ..enums import TaskStatus
import logging

logger = logging.getLogger("tasks_logger")  # Nombre del logger específico para este archivo
logger.setLevel(logging.DEBUG)  # Cambia el nivel según sea necesario

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/user/{user_id}", response_model=List[TaskResponse])
def read_tasks_by_user(user_id: UUID, db: Session = Depends(get_db)):
    logger.info(f"Recibida solicitud para obtener tareas del usuario: {user_id}")
    tasks = get_tasks_by_user(db, user_id)
    if not tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron tareas para el usuario especificado"
        )
    return tasks
    logger.info(f"Recibida solicitud para obtener tareas del usuario: {user_id}")

    # Obtener las tareas desde la base de datos
    tasks = get_tasks_by_user(db, user_id)
    if not tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron tareas para el usuario especificado"
        )
    
    logger.info(f"Se encontraron {len(tasks)} tareas para el usuario: {user_id}")

    # Convertir a un JSON plano
    return [
        {
            "id": str(task.id),
            "task_name": task.task_name,
            "task_description": task.task_description,
            "task_status": task.task_status.value,  # Para convertir a un valor serializable
            "user_id": str(task.user_id),
        }
        for task in tasks
    ]


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_new_task(task: TaskCreate, db: Session = Depends(get_db)):
    """
    Crea una nueva tarea.
    """
    # Verifica si el usuario existe
    user = db.exec(select(User).where(User.id == task.user_id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario especificado no existe"
        )

    # Crea la tarea
    db_task = create_task(db, task)
    return db_task


@router.get("/{task_id}", response_model=Task)
def read_task(task_id: UUID, db: Session = Depends(get_db)):
    """
    Obtiene una tarea por su ID.
    """
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    return task

@router.patch("/{task_id}", response_model=Task)
def update_existing_task(task_id: UUID, updated_task: TaskUpdate, db: Session = Depends(get_db)):
    """
    Actualiza una tarea existente.
    """
    task = update_task(db, task_id, updated_task)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    return task

@router.patch("/{task_id}/status", response_model=Task)
def change_task_status(task_id: UUID, new_status: TaskStatus = Body(...), db: Session = Depends(get_db)):
    """
    Cambia el estado de una tarea.
    """
    task = update_task_status(db, task_id, new_status)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_task(task_id: UUID, db: Session = Depends(get_db)):
    """
    Elimina una tarea por su ID.
    """
    if not delete_task(db, task_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    return None