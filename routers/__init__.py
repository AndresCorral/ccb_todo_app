from .tasks import router as tasks_router
from .users import router as users_router
from .auth import router as auth_router

# Lista de routers para incluir en la aplicación principal
routers = [
    tasks_router,
    users_router,
    auth_router,
]