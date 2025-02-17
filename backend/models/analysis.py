#models/analysis.py

import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import extract
from sqlalchemy import func
from backend.models.case import Case
from backend.models.norm import Norm
from datetime import datetime

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
        """Initialize the refined model with additional parameters."""
        self.normative_density = 0  # Number of new norms per day
        self.processing_rate = 0    # Number of norms processed per day
        self.backlog = 0            # Accumulated unprocessed norms
        self.temporal_gap = 0       # Average delay between norm creation & judicial processing

    async def calculate_daily_metrics(self, session: AsyncSession):
        """Calculate daily metrics for norms and cases."""
        async with session.begin():
            # Count norms created per day
            norms_per_day = await session.execute(
                select(extract("day", Norm.created_at), func.count(Norm.id))
                .filter(Norm.valid == True)
                .group_by(extract("day", Norm.created_at))
            )
            norms_per_day = dict(norms_per_day.fetchall())

            # Count cases resolved per day
            cases_per_day = await session.execute(
                select(extract("day", Case.resolved_at), func.count(Case.id))
                .filter(Case.status == "solved")
                .group_by(extract("day", Case.resolved_at))
            )
            cases_per_day = dict(cases_per_day.fetchall())

            return norms_per_day, cases_per_day

    async def update_metrics(self, session: AsyncSession):
        """Fetch and compute the refined normative inflation metrics safely."""
        norms_per_day, cases_per_day = await self.calculate_daily_metrics(session)

        # Remove None values from keys before computing max()
        valid_days = {day for day in norms_per_day.keys() | cases_per_day.keys() if day is not None}

        if valid_days:
            latest_day = max(valid_days)  # Ensure only valid days are considered
            self.normative_density = norms_per_day.get(latest_day, 0)
            self.processing_rate = cases_per_day.get(latest_day, 0)
        else:
            self.normative_density = 0
            self.processing_rate = 0

        # Update backlog: B_t = B_{t-1} + (ND_t - PR_t)
        self.backlog = max(0, self.backlog + (self.normative_density - self.processing_rate))

        # Compute Temporal Gap safely
        result = await session.execute(select(Case).filter(Case.status == "solved"))
        processed_cases = result.scalars().all()

        valid_cases = [case for case in processed_cases if case.resolved_at and case.created_at]

        if valid_cases:
            total_waiting_time = sum(
                (case.resolved_at - case.created_at).total_seconds() / 3600 for case in valid_cases
            )
            self.temporal_gap = round(total_waiting_time / len(valid_cases), 2)
        else:
            self.temporal_gap = 0

    async def calculate_inflation(self, session: AsyncSession):
        """Calculate and return inflation metrics with default values in case of failure."""
        try:
            await self.update_metrics(session)  # Refresh computations
            result = self.to_dict()

            # Ensure the API always returns a structured response
            if not result or not isinstance(result, dict):
                raise ValueError("Invalid result from to_dict() in NormativeInflationModel.")

            return result
        
        except Exception as e:
            logging.error(f"Error calculating normative inflation: {e}", exc_info=True)
            return {
                "normative_density": 0,
                "processing_rate": 0,
                "backlog": 0,
                "temporal_gap": "N/A"
            }

    def to_dict(self):
        """Return the refined metrics in a dictionary format for API responses."""
        return {
            "normative_density": round(self.normative_density, 2),
            "processing_rate": round(self.processing_rate, 2),
            "backlog": round(self.backlog, 2),
            "temporal_gap": f"{self.temporal_gap} hours"
        }