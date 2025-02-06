#analysis.py

import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from models.case import Case
from models.norm import Norm

logging.basicConfig(level=logging.DEBUG, format="%(message)s")

class Counter:
    def __init__(self):
        """Initialize counters with default values."""
        self.total_cases = 0
        self.solved_cases = 0
        self.pending_cases = 0
        self.total_norms = 0
        self.valid_norms = 0
        self.invalid_norms = 0

    async def update_counts(self, session: AsyncSession):
        """Fetch and update the latest counts from the database asynchronously."""
        async with session.begin():
            self.total_cases = await session.scalar(select(func.count(Case.id)))
            self.solved_cases = await session.scalar(select(func.count(Case.id)).filter_by(status="solved"))
            self.pending_cases = await session.scalar(select(func.count(Case.id)).filter_by(status="pending"))

            self.total_norms = await session.scalar(select(func.count(Norm.id)))
            self.valid_norms = await session.scalar(select(func.count(Norm.id)).filter_by(valid=True))
            self.invalid_norms = await session.scalar(select(func.count(Norm.id)).filter_by(valid=False))

    def to_dict(self):
        """Return a dictionary of all counts for API responses."""
        return {
            "total_cases": self.total_cases,
            "solved_cases": self.solved_cases,
            "pending_cases": self.pending_cases,
            "total_norms": self.total_norms,
            "valid_norms": self.valid_norms,
            "invalid_norms": self.invalid_norms,
            "resolution_rate": round((self.solved_cases / self.total_cases * 100) if self.total_cases else 0, 1),
        }


class NormativeInflationModel:
    def __init__(self):
        """Initialize the model with default values."""
        self.normative_density = 0  # Number of new norms per cycle
        self.processing_rate = 0    # Number of norms processed by the judiciary per cycle
        self.temporal_gap = 0       # Average delay (in cycles) between norm creation & judicial interpretation
        self.backlog = 0            # Number of norms waiting for judicial processing

    async def update_metrics(self, session: AsyncSession):
        """Fetch and compute the real-time normative inflation metrics from the database asynchronously."""
        async with session.begin():
            # ✅ Normative Density (ND): Count new norms created
            self.normative_density = await session.scalar(select(func.count(Norm.id)))

            # ✅ Processing Rate (PR): Count norms processed by the judiciary
            self.processing_rate = await session.scalar(select(func.count(Case.id)).filter(Case.status == "solved"))

            # ✅ Backlog (B_t): Compute unprocessed norms (ND - PR)
            self.backlog = max(0, self.normative_density - self.processing_rate)

            # ✅ Temporal Gap (TG) in HOURS instead of DAYS
            result = await session.execute(select(Case).filter(Case.status == "solved"))
            processed_cases = result.scalars().all()

            valid_cases = [
                case for case in processed_cases 
                if case.resolved_at and case.created_at  # ✅ Ensure both timestamps exist
            ]

            if valid_cases:
                total_waiting_time = sum(
                    (case.resolved_at - case.created_at).total_seconds() / 3600 for case in valid_cases  # ✅ Convert to hours
                )
                self.temporal_gap = round(total_waiting_time / len(valid_cases), 2)  # ✅ Rounded for readability
            else:
                self.temporal_gap = 0  # No valid cases means no delay

    async def calculate_inflation(self, session: AsyncSession):
        """Calculate and return inflation metrics."""
        await self.update_metrics(session)  # Reuse the existing logic
        return self.to_dict()  # Return the results as a dictionary

    def to_dict(self):
        """Return the metrics in a dictionary format for the API."""
        return {
            "normative_density": self.normative_density,
            "processing_rate": self.processing_rate,
            "backlog": self.backlog,
            "temporal_gap": f"{self.temporal_gap} hours"  # ✅ Updated to show hours
        }
