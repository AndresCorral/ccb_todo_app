import os
from sqlmodel import SQLModel, create_engine, Session
from typing import Generator
from dotenv import load_dotenv
from sqlalchemy.pool import NullPool

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Leer la URL de conexión desde la variable de entorno
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL no está definida en las variables de entorno")

# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL, poolclass=NullPool)

# Dependencia para obtener una sesión de la base de datos
def get_db() -> Generator[Session, None, None]:
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()
