import datetime
import logging
from .case import Case

logging.basicConfig(level=logging.DEBUG, format='%(message)s')

class JudicialSystem:
    def __init__(self):
        self.case_counter = 0
        self.pending_cases = []
        self.solved_cases = []

    def check_constitutionality(self, norm):
        log_message = f"Checking constitutionality of norm {norm.id} with complexity {norm.complexity}"
        logging.info(log_message)

    def create_case(self, norm):
        if norm.valid:
            self.case_counter += 1
            case = Case(self.case_counter, f'Case {self.case_counter}', norm)
            self.pending_cases.append(case)
            return case
        return None

    def create_case_from_pressure(self, norm, pressure_text):
        if norm.valid:
            self.case_counter += 1
            case = Case(self.case_counter, pressure_text, norm)
            self.pending_cases.append(case)
            return case
        return None

    def solve_case(self, case_id):
        case = next((case for case in self.pending_cases if case.id == case_id), None)
        if case:
            self.pending_cases.remove(case)
            self.solved_cases.append(case)
            case.resolved_at = datetime.now().isoformat()
            return case
        return None