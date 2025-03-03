#case.py

import logging
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.models import Base
from sqlalchemy import Enum as SQLAEnum
from enum import Enum

logging.basicConfig(level=logging.DEBUG, format="%(message)s")

class DecisionEnum(str, Enum): # 
    ACCEPTED = "Accepted"
    REJECTED = "Rejected"

class Case(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String(255), nullable=False)
    norm_id = Column(Integer, ForeignKey("norms.id"), nullable=False)
    constitutional = Column(Boolean, nullable=False, default=True)
    status = Column(String(20), nullable=False, default="pending")
    created_at = Column(DateTime, default=func.now())  # Auto-add timestamp on creation
    resolved_at = Column(DateTime, nullable=True)
    decision = Column(SQLAEnum(DecisionEnum, name="decision_enum"), nullable=True)

    norm = relationship("Norm", back_populates="cases", lazy="selectin")

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "norm_id": self.norm_id,
            "constitutional": self.constitutional,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
            "status": self.status,
            "decision": self.decision.value if self.decision else None  
        }

    @classmethod
    async def get_all(cls, session: AsyncSession):
        async with session.begin():
            result = await session.execute(select(cls))
            return result.scalars().all()

    async def resolve(self, session: AsyncSession, decision: bool):
        """Resolve the case asynchronously."""
        self.constitutional = decision
        self.resolved_at = datetime.utcnow()
        self.status = "solved"
        await session.commit()
        logging.info(f"Case {self.id}: Resolved with decision {'Constitutional' if decision else 'Unconstitutional'}")

