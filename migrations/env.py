#migration/env.py

import asyncio
from logging.config import fileConfig
from sqlalchemy import create_engine
from alembic import context
from database import DATABASE_URL
from backend.models import Base  # Vérifie que cet import est correct

# Charger la configuration Alembic
config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Configurer les logs
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata  # Assure-toi que Base est bien défini


def do_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True
    )
    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    """Exécute les migrations en mode 'online'."""
    connectable = create_engine(DATABASE_URL.replace("postgresql+asyncpg", "postgresql"), echo=True)

    with connectable.begin() as connection:
        do_migrations(connection)


def run_migrations_offline():
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata
    )

    with context.begin_transaction():
        context.run_migrations()


async def main():
    """Exécute les migrations en fonction du mode."""
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        await run_migrations_online()


asyncio.run(main())
