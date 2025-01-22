import asyncio
from .political_system import PoliticalSystem
from .judicial_system import JudicialSystem
from .citizen_pressure import CitizenPressure

class Society:
    def __init__(self):
        self.parliament = PoliticalSystem()
        self.judicial_system = JudicialSystem()
        self.citizen_pressure = CitizenPressure(self.judicial_system, self.parliament)
        self.iteration = 0

    async def simulate(self, simulation_days=100):
        while self.iteration < simulation_days:
            self.iteration += 1
            norm = self.parliament.create_norm()
            self.judicial_system.check_constitutionality(norm)
            self.citizen_pressure.generate_daily_cases()
            await asyncio.sleep(1)