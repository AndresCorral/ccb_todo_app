# CCB TODO App

Esta es una aplicación backend para gestionar usuarios y tareas, desarrollada con **FastAPI** y **PostgreSQL** (Neon como servicio de base de datos).

## Requisitos Previos

Asegúrate de tener instalado:

- **Python 3.11 o superior**
- **Git**
- Un cliente de PostgreSQL o conexión a Neon

## Cómo Configurar el Proyecto

### 1. Clona el Repositorio

```bash
git clone https://github.com/tu-usuario/tu-repositorio.git
cd tu-repositorio
```

### 2. Crea y Activa un Entorno Virtual

```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

### 3. Instala las Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configura las Variables de Entorno

Crea un archivo `.env` en el directorio raíz y añade la URL de tu base de datos PostgreSQL (proporcionada por Neon):

```env
DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<database>?sslmode=require
```

### 5. Realiza las Migraciones

Aplica las migraciones para crear las tablas en tu base de datos:

```bash
alembic upgrade head
```

### 6. Inicia el Servidor

Ejecuta el servidor de desarrollo:

```bash
uvicorn main:app --reload
```

Visita http://127.0.0.1:8000/docs para ver la documentación interactiva.

## Pruebas

### 1. Endpoints

Puedes probar los endpoints de la API directamente desde la documentación Swagger en `/docs`.

### 2. Pruebas Manuales

Usa herramientas como **Postman** o **cURL** para realizar solicitudes a la API.

## Despliegue

### Railway

1. Crea un nuevo proyecto en Railway
2. Configura las variables de entorno, incluyendo `DATABASE_URL`
3. Configura el comando de inicio:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

4. Despliega el proyecto y accede a la URL proporcionada por Railway

## Estructura del Proyecto

```plaintext
📦 ccb_todo_app
├── alembic/            # Configuración y scripts de migración
├── routers/            # Rutas de la API
│   ├── tasks.py
│   └── users.py
├── models.py           # Modelos de SQLModel
├── database.py         # Configuración de la base de datos
├── main.py            # Entrada principal de la aplicación
├── requirements.txt    # Dependencias del proyecto
├── README.md          # Documentación del proyecto
└── .env.example       # Ejemplo de configuración de variables de entorno
```

## Contribuciones

¡Las contribuciones son bienvenidas! Si quieres colaborar:

1. Haz un fork del repositorio
2. Crea una rama para tu funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. Envía un pull request

## Licencia

Este proyecto está bajo la licencia MIT.
