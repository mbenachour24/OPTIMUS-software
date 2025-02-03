import asyncio
import logging
from models import db  # Import shared db instance from models/__init__.py
from .notification_manager import NotificationManager

logging.basicConfig(level=logging.DEBUG, format="%(message)s")

class Norm(db.Model):
    __tablename__ = "norms"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String(255), nullable=False)
    valid = db.Column(db.Boolean, default=True)
    complexity = db.Column(db.Integer, nullable=False, default=1)
    constitutional = db.Column(db.Boolean, default=False)

    # Define the relationship before Case references it
    cases = db.relationship("Case", backref="norm", lazy=True)

    def __init__(self, text, valid=True, complexity=1, constitutional=False):
        self.text = text
        self.valid = valid
        self.complexity = complexity
        self.constitutional = constitutional

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "valid": self.valid,
            "complexity": self.complexity,
            "constitutional": self.constitutional,
        }

    def invalidate(self):
        self.valid = False
        db.session.commit()

        try:
            asyncio.run(NotificationManager().broadcast_update({
                "type": "norm_update",
                "norm_id": self.id,
                "valid": self.valid
            }))
        except RuntimeError:
            logging.warning("Async operation ignored (not in an async context).")

        logging.info(f"Norm {self.id}: Invalidated")

# Legacy Norm class for in-memory usage (optional, if needed)
class LegacyNorm:
    """This class retains the original in-memory functionality, if required for compatibility."""

    def __init__(self, norm_id, text, valid=True, complexity=1):
        """Initialize a LegacyNorm instance."""
        self.id = norm_d
        self.text = text
        self.valid = valid
        self.complexity = complexity
        self.log_event(f"Initialized with complexity {complexity} and validity {valid}")

    def invalidate(self):
        """Mark the norm as invalid (unconstitutional)."""
        self.valid = False
        self.log_event("Invalidated")
        asyncio.create_task(NotificationManager().broadcast_update({
            'type': 'norm_update',
            'norm_id': self.id,
            'valid': self.valid
        }))

    def log_event(self, message):
        """Log an event for this norm."""
        log_message = f"LegacyNorm {self.id}: {message}"
        logging.info(log_message)
        print(log_message)
