from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from uuid import UUID, uuid4
from enum import Enum
from pydantic import EmailStr

# Enumeración para los estados de las tareas
class TaskStatus(str, Enum):
    PENDIENTE = "Pendiente"
    TERMINADA = "Terminada"
    CANCELADA = "Cancelada"

# Esquema de entrada para User (sin el campo id)
class UserCreate(SQLModel):
    name: str
    correo: EmailStr
    password: str

# Esquema de actualización para User (todos los campos son opcionales)
class UserUpdate(SQLModel):
    name: Optional[str] = None
    correo: Optional[EmailStr] = None
    password: Optional[str] = None

# Modelo de base de datos para User
class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    correo: str = Field(index=True, unique=True)
    password: str

    # Relación con las tareas
    tasks: List["Task"] = Relationship(back_populates="user")

# Esquema de entrada para Task (sin el campo id)
class TaskCreate(SQLModel):
    task_name: str
    task_description: Optional[str] = None
    task_status: TaskStatus = Field(default=TaskStatus.PENDIENTE)
    user_id: UUID

# Esquema de actualización para Task (todos los campos son opcionales)
class TaskUpdate(SQLModel):
    task_name: Optional[str] = None
    task_description: Optional[str] = None
    task_status: Optional[TaskStatus] = None
    user_id: Optional[UUID] = None

# Modelo de base de datos para Task
class Task(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    task_name: str
    task_description: Optional[str] = None
    task_status: TaskStatus = Field(default=TaskStatus.PENDIENTE)

    # Clave foránea para el usuario
    user_id: UUID = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="tasks")