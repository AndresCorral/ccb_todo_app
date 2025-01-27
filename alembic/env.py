import os
from models import SQLModel
import sqlmodel  # Importa sqlmodel explícitamente

from sqlmodel import SQLModel
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool
from alembic import context

# Cargar las variables de entorno
load_dotenv()

# Leer la URL desde la variable de entorno o usar un valor predeterminado
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://neondb_owner:npg_JyfblGh8ak6D@ep-yellow-star-a4ycf2vp-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require")

config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Importar metadatos de modelos
from models import SQLModel
target_metadata = SQLModel.metadata

def run_migrations_offline():
    context.configure(url=DATABASE_URL, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
