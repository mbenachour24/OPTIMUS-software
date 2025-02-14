#society.py

import asyncio
import logging
from sqlalchemy.ext.asyncio import AsyncSession

class Society:
    def __init__(self):
        self.parliament = None  # Placeholder for PoliticalSystem
        self.judicial_system = None  # Placeholder for JudicialSystem
        self.citizen_pressure = None  # Placeholder for CitizenPressure
        self.iteration = 0

    def initialize_systems(self, session: AsyncSession):
        """Initialize system components with an async session."""
        from .political_system import PoliticalSystem
        from .judicial_system import JudicialSystem
        from .citizen_pressure import CitizenPressure

        self.parliament = PoliticalSystem()
        self.judicial_system = JudicialSystem()
        self.citizen_pressure = CitizenPressure(self.judicial_system, self.parliament)
        logging.info("✅ Systems initialized: Parliament, Judicial System, Citizen Pressure")

    async def simulate(self, session: AsyncSession, simulation_days=100):
        """Simulate society for a given number of days."""
        while self.iteration < simulation_days:
            self.iteration += 1
            norm = await self.parliament.create_norm(session)  # Create a new norm
            await self.judicial_system.check_constitutionality(norm)  # Check its constitutionality
            await self.citizen_pressure.generate_daily_cases(session)  # Generate citizen pressure cases
            await asyncio.sleep(1)  # Pause for 1 second to simulate a day
