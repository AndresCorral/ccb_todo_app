from fastapi import FastAPI
from database import create_tables
from routers import routers
import os
print("Current working directory:", os.getcwd())

# Crear la aplicación FastAPI
app = FastAPI(
    title="API de TODO",
    description="Una API simple para gestionar tareas y usuarios.",
    version="1.0.0",
)

# Crear tablas en la base de datos al iniciar
create_tables()

# Incluir todos los routers dinámicamente
for router in routers:
    app.include_router(router)

# Ruta de inicio
@app.get("/", tags=["Inicio"])
def read_root():
    return {
        "message": "Bienvenido a la API de TODO",
        "endpoints": {
            "tasks": "/tasks",
            "users": "/users",
        },
    }