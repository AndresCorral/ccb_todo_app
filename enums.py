from enum import Enum

class TaskStatus(str, Enum):
    PENDIENTE = "Pendiente"
    TERMINADA = "Terminada"
    CANCELADA = "Cancelada"
   