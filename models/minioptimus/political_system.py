import random
import logging
from .norm import Norm

logging.basicConfig(level=logging.DEBUG, format='%(message)s')

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
            complexity=random.randint(1, 10)
        )
        self.norms.append(norm)
        logging.info(f"Debug: Created Norm #{self.norm_counter} with ID {norm.id}")
        return norm