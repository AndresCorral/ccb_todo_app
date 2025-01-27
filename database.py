from sqlmodel import SQLModel, create_engine, Session
from typing import Generator

# Configuración de la base de datos
DATABASE_URL = "sqlite:///todo.db"  # SQLite en el mismo directorio

# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL, echo=True)  # echo=True para ver logs de SQL

# Crear tablas en la base de datos
def create_tables():
    """
    Crea todas las tablas definidas en los modelos SQLModel.
    """
    SQLModel.metadata.create_all(engine)

# Dependencia para obtener una sesión de la base de datos
def get_db() -> Generator[Session, None, None]:
    """
    Proporciona una sesión de la base de datos para cada solicitud.
    Cierra la sesión automáticamente después de su uso.
    """
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()