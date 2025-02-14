#judicial_system.py

import logging
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.case import Case

logging.basicConfig(level=logging.DEBUG, format="%(message)s")

class JudicialSystem:
    def __init__(self):
        self.case_counter = 0  # Removed local lists (DB will handle it)

    async def check_constitutionality(self, norm):
        """Log norm constitutionality check (async-compatible)."""
        log_message = f"Checking constitutionality of norm {norm.id} with complexity {norm.complexity}"
        logging.info(log_message)

    async def create_case(self, session: AsyncSession, norm):
        """Create a new case and store it in the database."""
        if norm.valid:
            self.case_counter += 1
            case = Case(
                text=f"Case {self.case_counter}",
                norm_id=norm.id
            )
            session.add(case)
            await session.commit()
            await session.refresh(case)

            logging.info(f"✅ Created Case #{case.id} linked to Norm #{norm.id}")
            return case.to_dict()
        return None

    async def create_case_from_pressure(self, session: AsyncSession, norm, pressure_text):
        """Create a case from citizen pressure (async)."""
        if norm.valid:
            self.case_counter += 1
            case = Case(
                text=pressure_text,
                norm_id=norm.id
            )
            session.add(case)
            await session.commit()
            await session.refresh(case)

            logging.info(f"✅ Created Pressure Case #{case.id} for Norm #{norm.id}")
            return case.to_dict()
        return None

    async def solve_case(self, session: AsyncSession, case_id):
        """Resolve a case asynchronously."""
        result = await session.execute(select(Case).where(Case.id == case_id))
        case = result.scalars().first()

        if case:
            case.resolved_at = datetime.utcnow()
            case.status = "solved"
            await session.commit()

            logging.info(f"✅ Case {case.id} resolved at {case.resolved_at}")
            return case.to_dict()
        return None
