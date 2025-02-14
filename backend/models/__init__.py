# models/__init__.py

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine
import asyncio

Base = declarative_base()

def register_models(engine):
    from models.norm import Norm
    from models.case import Case
    from models.judicial_system import JudicialSystem
    from models.political_system import PoliticalSystem
    from models.citizen_pressure import CitizenPressure
    from models.society import Society
    from models.analysis import Counter, NormativeInflationModel

    # Ensure models are added to Base.metadata
    if isinstance(engine, AsyncEngine):
        # Async engine - can't use directly with Alembic
        print("Using Async Engine, cannot apply migrations directly with Alembic.")
    else:
        # Synchronous engine - used with Alembic
        print("Using Sync Engine, applying migrations directly.")
        Base.metadata.create_all(bind=engine)

    return Base.metadata
