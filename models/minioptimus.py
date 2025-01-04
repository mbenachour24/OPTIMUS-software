# This file is part of the OPTMUS project.
# Licensed under CC BY-NC 4.0. Non-commercial use only.
# For more details, see the LICENSE file in the repository.

import asyncio
import random
import logging
from datetime import datetime

# Setup enhanced logging
logging.basicConfig(level=logging.DEBUG, format='%(message)s')

# Constants
COMPLEXITY_MIN = 1
COMPLEXITY_MAX = 10
SIMULATION_DAYS = 100

class Norm:
    def __init__(self, norm_id, text, valid=True, complexity=1):
        self.id = norm_id
        self.text = text
        self.valid = valid
        self.complexity = complexity
        self.log_event(f"Initialized with complexity {complexity} and validity {valid}")

    def invalidate(self):
        self.valid = False
        self.log_event("Invalidated")

    def log_event(self, message):
        log_message = f"Norm {self.id}: {message}"
        logging.info(log_message)
        print(log_message)

class Case:
    def __init__(self, case_id, text, norm):
        self.id = case_id
        self.text = text
        self.norm = norm
        self.constitutional = norm.valid
        self.resolved_at = None  # New field for resolution timestamp
        self.log_event("A new case is brought to the Courts")

    def log_event(self, message):
        log_message = f"Case {self.id}: {message}"
        logging.info(log_message)
        print(log_message)

class CitizenPressure:
    def __init__(self, judicial_system, parliament):
        self.judicial_system = judicial_system
        self.parliament = parliament
        self.daily_case_count = 5
        self.case_types = [
            "Environmental Concern",
            "Civil Rights Issue",
            "Labor Dispute",
            "Consumer Protection",
            "Luhmann's Public Safety Concern",
            "Mohamed got funds and it's not fair",
            "Alien invasion",
            "Zombie outbreak",
        ]

    def generate_daily_cases(self):
        generated_cases = []
        for _ in range(self.daily_case_count):
            # Get a random existing norm to challenge
            if not self.parliament.norms:
                # Create a norm if none exist
                norm = self.parliament.create_norm()
            else:
                norm = random.choice(self.parliament.norms)
            
            # Force the norm to be invalid (simulating citizen challenge)
            norm.valid = False
            
            # Create a case
            case_type = random.choice(self.case_types)
            case = self.judicial_system.create_case_from_pressure(
                norm=norm,
                pressure_text=f"Citizen Petition: {case_type} regarding {norm.text}"
            )
            if case:
                generated_cases.append(case)
                
        return generated_cases

class PoliticalSystem:
    def __init__(self):
        self.norm_counter = 0
        self.norms = []

    def create_norm(self):
        self.norm_counter += 1
        norm = Norm(
            norm_id=self.norm_counter,
            text=f'Law {self.norm_counter}',
            valid=True,
            complexity=random.randint(COMPLEXITY_MIN, COMPLEXITY_MAX)
        )
        self.norms.append(norm)
        return norm

class JudicialSystem:
    def __init__(self):
        self.case_counter = 0
        self.pending_cases = []  # New pool for pending cases
        self.solved_cases = []   # New pool for solved cases

    def check_constitutionality(self, norm):
        log_message = f"Judicial System: Checking constitutionality of norm {norm.id} with complexity {norm.complexity}"
        logging.info(log_message)
        print(log_message)

        if norm.complexity > 5:
            norm.invalidate()
            # Create a case automatically for invalidated norms
            self.create_case(norm)

        log_message = f"Judicial System: Norm {norm.id} has been checked for constitutionality. Valid status: {norm.valid}"
        logging.info(log_message)
        print(log_message)

    def create_case(self, norm):
        if not norm.valid:
            self.case_counter += 1
            case = Case(
                case_id=self.case_counter,
                text=f'Case {self.case_counter} referencing {norm.text}',
                norm=norm
            )
            self.pending_cases.append(case)  # Add to pending instead of cases
            case.log_event("Case created and added to pending cases.")
            return case
        else:
            log_message = f"Cannot create a case for a valid norm (Norm #{norm.id})"
            logging.info(log_message)
            print(log_message)
            return None

    def create_case_from_pressure(self, norm, pressure_text):
        """Create a case from citizen pressure, regardless of norm validity"""
        self.case_counter += 1
        case = Case(
            case_id=self.case_counter,
            text=pressure_text,
            norm=norm
        )
        self.pending_cases.append(case)  # Add to pending cases
        case.log_event("Case created from citizen pressure and added to pending cases.")
        
        log_message = f"Citizen Pressure Case created: ID {case.id}, Text: {case.text}"
        logging.info(log_message)
        print(log_message)
        
        return case

    def solve_case(self, case_id):
        """Solve a pending case and move it to solved cases"""
        # Find the case in pending cases
        case = next((case for case in self.pending_cases if case.id == case_id), None)
        if not case:
            raise ValueError(f"No pending case found with ID {case_id}")

        # Remove from pending and add to solved
        self.pending_cases.remove(case)
        self.solved_cases.append(case)
        
        # Add resolution timestamp and log
        case.resolved_at = datetime.now().isoformat()
        case.log_event("Case has been resolved by the Judicial System")
        
        return case

class Society:
    def __init__(self):
        self.parliament = PoliticalSystem()
        self.judicial_system = JudicialSystem()
        self.citizen_pressure = CitizenPressure(self.judicial_system, self.parliament)
        self.iteration = 0

    async def simulate(self):
        while self.iteration < SIMULATION_DAYS:
            self.iteration += 1
            print(f"Debug: Starting Day {self.iteration}")

            # Political system creates a norm
            norm = self.parliament.create_norm()
            print(f"Debug: Created Norm: {norm.text}, Valid: {norm.valid}")

            # Judicial system checks constitutionality
            self.judicial_system.check_constitutionality(norm)

            # Generate citizen pressure cases
            generated_cases = self.citizen_pressure.generate_daily_cases()
            print(f"Debug: Generated {len(generated_cases)} citizen pressure cases")

            # Debugging: Log the current state of cases
            print("Debug: Current cases in JudicialSystem:")
            for case in self.judicial_system.cases:
                print(f"Case ID: {case.id}, Text: {case.text}, Constitutional: {case.constitutional}")

            print(f"Debug: Ending Day {self.iteration}")
            await asyncio.sleep(1)

async def main():
    society = Society()
    await society.simulate()

if __name__ == "__main__":
    asyncio.run(main())