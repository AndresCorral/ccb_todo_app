from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from .enums import TaskStatus

class TaskResponse(BaseModel):
    id: UUID
    task_name: str
    task_description: Optional[str]
    task_status: TaskStatus
    user_id: UUID

    class Config:
        from_attributes=True

class UserResponse(BaseModel):
    id: UUID
    name: str
    correo: str

    class Config:
        from_attributes=True