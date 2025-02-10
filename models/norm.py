import logging
import datetime
from sqlalchemy import Column, Integer, String, Boolean, select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from sqlalchemy.types import DateTime  # Import DateTime from SQLAlchemy
from models import Base
from .notification_manager import NotificationManager

logging.basicConfig(level=logging.DEBUG, format="%(message)s")

class Norm(Base):
    __tablename__ = "norms"

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String(255), nullable=False)
    valid = Column(Boolean, default=True)
    complexity = Column(Integer, nullable=False, default=1)
    constitutional = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())  # Use DateTime from SQLAlchemy

    # Define relationship before Case references it
    cases = relationship("Case", back_populates="norm", lazy="selectin")

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "valid": self.valid,
            "complexity": self.complexity,
            "constitutional": self.constitutional,
        }

    @classmethod
    async def get_all(cls, session: AsyncSession):
        async with session.begin():
            result = await session.execute(select(cls))
            return result.scalars().all()

    async def invalidate(self, session: AsyncSession):
        """Invalidate a norm and commit changes asynchronously."""
        self.valid = False
        await session.commit()

        try:
            await NotificationManager().broadcast_update({
                "type": "norm_update",
                "norm_id": self.id,
                "valid": self.valid
            })
        except RuntimeError:
            logging.warning("Async operation ignored (not in an async context).")

        logging.info(f"Norm {self.id}: Invalidated")

# Legacy Norm class for in-memory usage (optional, if needed)
class LegacyNorm:
    """This class retains the original in-memory functionality, if required for compatibility."""

    def __init__(self, norm_id, text, valid=True, complexity=1):
        """Initialize a LegacyNorm instance."""
        self.id = norm_id
        self.text = text
        self.valid = valid
        self.complexity = complexity
        self.log_event(f"Initialized with complexity {complexity} and validity {valid}")

    async def invalidate(self):
        """Mark the norm as invalid (unconstitutional)."""
        self.valid = False
        self.log_event("Invalidated")
        await NotificationManager().broadcast_update({
            'type': 'norm_update',
            'norm_id': self.id,
            'valid': self.valid
        })

    def log_event(self, message):
        """Log an event for this norm."""
        log_message = f"LegacyNorm {self.id}: {message}"
        logging.info(log_message)
        print(log_message)
