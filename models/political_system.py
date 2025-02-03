import logging  # Keep logging at the top

logging.basicConfig(level=logging.DEBUG, format='%(message)s')

class PoliticalSystem:
    def __init__(self):
        self.norm_counter = 0  # Internal counter for norms

def create_norm(self):
    """Create a new norm and save it to the database."""
    import random  # ✅ Fix: Import random inside function to avoid scope issues
    from models.norm import Norm, db  # ✅ Fix: Avoid circular imports

    self.norm_counter += 1
    try:
        # Create a new norm instance
        norm = Norm(
            text=f'Law {self.norm_counter}',
            valid=True,
            complexity=random.randint(1, 10)
        )

        # Add the norm to the database
        db.session.add(norm)
        db.session.commit()  # Save changes to the database

        logging.info(
            f"✅ Created Norm #{norm.id} - {norm.text} (Valid: {norm.valid}, Complexity: {norm.complexity})"
        )
        return norm.to_dict()  # ✅ FIX: Return as a dictionary

    except Exception as e:
        db.session.rollback()
        logging.error(f"❌ Error creating norm in the database: {e}")
        return None
