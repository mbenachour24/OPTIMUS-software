#citizen_pressure.py

import random
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.case import Case

logging.basicConfig(level=logging.DEBUG, format="%(message)s")

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
            "Public Safety Concern"
        ]

    async def generate_daily_cases(self, session: AsyncSession):
        """
        Generate a fixed number of daily cases from valid norms.
        Ensure cases are committed to the database and added to pending cases.
        """
        generated_cases = []
        valid_norms = await self.political_system.get_valid_norms(session)

        if not valid_norms:
            logging.info("No valid norm to generate case.")
            return []

        for _ in range(self.daily_case_count):
            norm = random.choice(valid_norms)
            case_type = random.choice(self.case_types)

            case = Case(
                text=f"Citizen Petition: {case_type} regarding norm {norm.text}",
                norm_id=norm.id
            )

            session.add(case)  # Persist to database
            self.judicial_system.pending_cases.append(case)  # Ensure added to pending cases
            generated_cases.append(case)

        await session.commit()  # Commit all cases at once
        logging.info(f"✅ Generated {len(generated_cases)} citizen pressure cases.")
        return generated_cases

    async def generate_cases_from_norms(self, session: AsyncSession, valid_norms):
        """Generates and saves cases based on the provided valid norms."""
        generated_cases = []

        if not valid_norms:
            logging.info("No valid norm to generate case.")
            return []

        for _ in range(self.daily_case_count):
            norm = random.choice(valid_norms)
            case_type = random.choice(self.case_types)
            case = Case(
                text=f"Citizen Petition: {case_type} regarding norm {norm.text}",
                norm_id=norm.id,
                constitutional=True
            )
            session.add(case)  # ✅ Ensure case is added to session
            generated_cases.append(case)

        await session.commit()  # ✅ Commit all cases at once
        return generated_cases
