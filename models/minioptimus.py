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
            # Create a case automatically for invalidated norms
            self.create_case(norm)

        log_message = f"Judicial System: Norm {norm.id} has been checked for constitutionality. Valid status: {norm.valid}"
        logging.info(log_message)
        print(log_message)

    def create_case(self, norm):
        if not norm.valid:  # Only create cases for invalid norms
            self.case_counter += 1
            case = Case(
                case_id=self.case_counter,
                text=f'Case {self.case_counter} referencing {norm.text}',
                norm=norm
            )
            self.cases.append(case)
            case.log_event("Case created and added to JudicialSystem.")
            return case
        else:
            log_message = f"Cannot create a case for a valid norm (Norm #{norm.id})"
            logging.info(log_message)
            print(log_message)
            return None

        # Log case creation
        log_message = f"Case created: ID {case.id}, Text: {case.text}, Constitutional: {case.constitutional}"
        logging.info(log_message)
        print(log_message)
        
        return case

        # Debugging: Log the case creation
        log_message = f"Case created: ID {case.id}, Text: {case.text}, Constitutional: {case.constitutional}"
        logging.info(log_message)
        print(log_message)

        # Debugging: Log the current list of cases
        log_message = f"Current cases: {[c.text for c in self.cases]}"
        logging.info(log_message)
        print(log_message)

        print(f"Debug: Cases in JudicialSystem after creation: {[case.text for case in self.cases]}")
     
        return case

class Society:
    def __init__(self):
        self.parliament = PoliticalSystem()
        self.judicial_system = JudicialSystem()
        self.iteration = 0

    async def simulate(self):
        while self.iteration < SIMULATION_DAYS:
            self.iteration += 1
            print(f"Debug: Starting Day {self.iteration}")

            # Political system creates a norm
            norm = self.parliament.create_norm()
            print(f"Debug: Created Norm: {norm.text}, Valid: {norm.valid}")

            # Judicial system checks constitutionality (and creates a case)
            self.judicial_system.check_constitutionality(norm)

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