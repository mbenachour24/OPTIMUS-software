import os
import asyncio
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from models import Base, register_models  # Import the register_models function

# Load environment variables
load_dotenv()

# Retrieve database URL
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL is not set! Check your .env file or environment variables.")

print(f"DEBUG: DATABASE_URL = {DATABASE_URL}")

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Register models so Alembic knows about them
register_models(engine)  # Pass the engine to register models

# Create an async session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base model for SQLAlchemy
Base = declarative_base()

# Dependency for database session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# Function to initialize database and create tables
async def init_db():
    # Create tables with AsyncEngine
    async with engine.begin() as conn:
        # Use run_sync for async engine
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database tables created successfully!")

# Run database initialization if executed directly
if __name__ == "__main__":
    asyncio.run(init_db())
