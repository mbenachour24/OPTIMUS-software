# This file is part of the OPTMUS project.
# Licensed under CC BY-NC 4.0. Non-commercial use only.
# For more details, see the LICENSE file in the repository.

import asyncio
import random
import logging

# Setup enhanced logging
logging.basicConfig(level=logging.DEBUG, filename='mini_optimu4.log', filemode='a', format='%(message)s')

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
        self.log_event("A new case is brought to the Courts")

    def log_event(self, message):
        log_message = f"Case {self.id}: {message}"
        logging.info(log_message)
        print(log_message)

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
        self.cases = []

    def check_constitutionality(self, norm):
        log_message = f"Judicial System: Checking constitutionality of norm {norm.id} with complexity {norm.complexity}"
        logging.info(log_message)
        print(log_message)
        
        if norm.complexity > 5:
            norm.invalidate()
        
        # Log message indicating constitutionality check is complete
        log_message = f"Judicial System: Norm {norm.id} has been checked for constitutionality. Valid status: {norm.valid}"
        logging.info(log_message)
        print(log_message)

    def create_case(self, norm):
        if not norm.valid:
            log_message = f"Judicial System: Cannot create case based on invalid norm {norm.id}"
            logging.info(log_message)
            print(log_message)
            return None

        self.case_counter += 1
        case = Case(
            case_id=self.case_counter,
            text=f'Case {self.case_counter} referencing {norm.text}',
            norm=norm
        )
        self.cases.append(case)
        return case

class Society:
    def __init__(self):
        self.parliament = PoliticalSystem()
        self.judicial_system = JudicialSystem()
        self.iteration = 0

    async def simulate(self):
        while self.iteration < SIMULATION_DAYS:
            self.iteration += 1
            log_message = f"\n\n{'='*20} START OF DAY {self.iteration} {'='*20}\n"
            logging.info(log_message)
            print(log_message)

            # Political system creates a norm
            norm = self.parliament.create_norm()
            log_message = f"Political System produced: {norm.text}"
            logging.info(log_message)
            print(log_message)

            # Judicial system checks constitutionality
            self.judicial_system.check_constitutionality(norm)

            # Judicial system creates a case
            case = self.judicial_system.create_case(norm)
            if case:
                log_message = f"Judicial System produced: {case.text}"
                logging.info(log_message)
                print(log_message)

            log_message = f"\n{'='*20} END OF DAY {self.iteration} {'='*20}\n"
            logging.info(log_message)
            print(log_message)
            
            await asyncio.sleep(1)  # Simulate the passage of time

        logging.info("Simulation completed.")

async def main():
    society = Society()
    await society.simulate()

if __name__ == "__main__":
    asyncio.run(main())
