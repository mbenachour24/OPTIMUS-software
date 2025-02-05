#political_system.py

import logging
import random
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.norm import Norm
from models import Base

logging.basicConfig(level=logging.DEBUG, format="%(message)s")

class PoliticalSystem:
    def __init__(self):
        self.norm_counter = 0  # Internal counter for norms

    async def create_norm(self, session: AsyncSession):
        """Create a new norm and save it to the database asynchronously."""
        self.norm_counter += 1
        try:
            # Create a new norm instance
            norm = Norm(
                text=f'Law {self.norm_counter}',
                valid=True,
                complexity=random.randint(1, 10)
            )

            # Add the norm to the database
            session.add(norm)
            await session.commit()  # Save changes to the database
            await session.refresh(norm)  # Ensure we get the updated ID

            logging.info(
                f"✅ Created Norm #{norm.id} - {norm.text} (Valid: {norm.valid}, Complexity: {norm.complexity})"
            )
            return norm.to_dict()  # Return as a dictionary

        except Exception as e:
            await session.rollback()
            logging.error(f"❌ Error creating norm in the database: {e}")
            return None
