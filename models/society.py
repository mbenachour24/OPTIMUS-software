import asyncio

class Society:
    def __init__(self):
        self.parliament = None  # Placeholder for PoliticalSystem
        self.judicial_system = None  # Placeholder for JudicialSystem
        self.citizen_pressure = None  # Placeholder for CitizenPressure
        self.iteration = 0

        # Initialize components after the instance is created
        self.initialize_systems()

    def initialize_systems(self):
        from .political_system import PoliticalSystem
        from .judicial_system import JudicialSystem
        from .citizen_pressure import CitizenPressure

        self.parliament = PoliticalSystem()
        self.judicial_system = JudicialSystem()
        self.citizen_pressure = CitizenPressure(self.judicial_system, self.parliament)

    async def simulate(self, simulation_days=100):
        """Simulate society for a given number of days."""
        while self.iteration < simulation_days:
            self.iteration += 1
            norm = self.parliament.create_norm()  # Create a new norm
            self.judicial_system.check_constitutionality(norm)  # Check its constitutionality
            self.citizen_pressure.generate_daily_cases()  # Generate citizen pressure cases
            await asyncio.sleep(1)  # Pause for 1 second to simulate a day
