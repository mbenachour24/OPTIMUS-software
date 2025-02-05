#env.py

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool, create_engine
from alembic import context
from models import Base, register_models
from database import DATABASE_URL

# Convert asyncpg URL to synchronous URL
sync_database_url = DATABASE_URL.replace("postgresql+asyncpg", "postgresql")
config = context.config
config.set_main_option("sqlalchemy.url", sync_database_url)

# Configure logging
fileConfig(config.config_file_name)

# Target metadata for migrations
target_metadata = Base.metadata

# Register models so Alembic knows about them
sync_engine = create_engine(sync_database_url, echo=True)
register_models(sync_engine)

def run_migrations_online():
    """Run migrations in 'online' mode using a synchronous engine."""
    # Use the synchronous engine to connect
    with sync_engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True
        )

        # Run migrations
        with context.begin_transaction():
            context.run_migrations()

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=sync_database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

# Check if the context is offline or online
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
