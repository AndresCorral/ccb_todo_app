from fastapi import FastAPI
from .database import get_db
from .routers import routers
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware


# Cargar las variables de entorno
load_dotenv()

# Crear la aplicación FastAPI
app = FastAPI(
    title="API de TODO",
    description="Una API simple para gestionar tareas y usuarios.",
    version="1.0.0",
)

# Incluir todos los routers dinámicamente
for router in routers:
    app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://moonlit-bombolone-d444fb.netlify.app"],  # Cambia "*" por la lista de dominios permitidos (por ejemplo: ["http://localhost:3000"])
    allow_credentials=True,
    allow_methods=["*"],  # Métodos permitidos: GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],  # Encabezados permitidos: Authorization, Content-Type, etc.
)

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
