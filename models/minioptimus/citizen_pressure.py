import random
import logging

logging.basicConfig(level=logging.DEBUG, format='%(message)s')

class CitizenPressure:
    def __init__(self, judicial_system, political_system):
        self.judicial_system = judicial_system
        self.political_system = political_system
        self.daily_case_count = 5
        self.case_types = [
            "Environmental Concern",
            "Civil Rights Issue",
            "Labor Dispute",
            "Consumer Protection",
            "Luhmann's theory Public Safety Concern",
            "Mohamed got funds and it's not fair",
            "Alien invasion",
            "Zombie outbreak",
        ]

    def generate_daily_cases(self):
        generated_cases = []
        valid_norms = [norm for norm in self.political_system.norms if norm.valid]
        
        if not valid_norms:
            print("No valid norm to generate case.")
            return "No valid norm to generate case."

        for _ in range(self.daily_case_count):
            norm = random.choice(valid_norms)
            case_type = random.choice(self.case_types)
            case = self.judicial_system.create_case_from_pressure(
                norm=norm,
                pressure_text=f"Citizen Petition: {case_type} regarding {norm.text}"
            )
            if case:
                generated_cases.append(case)
                
        return generated_cases