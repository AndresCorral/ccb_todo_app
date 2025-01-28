import logging
from fastapi import FastAPI, Request
import time
from .routers import routers
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# Configura el logger
logging.basicConfig(
    level=logging.DEBUG,  # Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Formato del mensaje
    handlers=[
        logging.StreamHandler()  # Los logs se imprimen en la consola
    ],
)

logger = logging.getLogger(__name__)  # Crea un logger para este módulo

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
    allow_origins=["https://ccbtodofront.netlify.app, http://localhost:8000, https://todoapp-register.flutterflow.app"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

# Ruta de inicio
@app.get("/", tags=["Inicio"])
def read_root():
    return {
        "message": "Bienvenido a la API de ToDo",
        "endpoints": {
            "tasks": "/tasks",
            "users": "/users",
        },
    }

# Middleware para loggear solicitudes
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    try:
        response = await call_next(request)
    except Exception as e:
        logger.error(f"Error en la solicitud: {e}", exc_info=True)
        raise

    process_time = time.time() - start_time
    logger.info(
        f"{request.method} {request.url} - {response.status_code} - {process_time:.2f}s"
    )
    return response