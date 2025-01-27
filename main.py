from fastapi import FastAPI
import logging
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
    allow_origins=["https://ccbtodofront.netlify.app"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
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
# Configuración del logger
logging.basicConfig(
    level=logging.DEBUG,  # Cambia a DEBUG para obtener más detalles
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()  # Los logs van a la consola, visibles en Railway
    ],
)

logger = logging.getLogger("fastapi_app")


