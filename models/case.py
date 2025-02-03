import logging
from datetime import datetime
from models import db  # Import shared db instance from models/__init__.py

logging.basicConfig(level=logging.DEBUG, format='%(message)s')

class Case(db.Model):
    __tablename__ = "cases"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String(255), nullable=False)
    norm_id = db.Column(db.Integer, db.ForeignKey("norms.id"), nullable=False)
    constitutional = db.Column(db.Boolean, nullable=False, default=True)
    status = db.Column(db.String(20), nullable=False, default="pending")
    resolved_at = db.Column(db.DateTime, nullable=True)

    def __init__(self, text, norm_id, constitutional=True):
        self.text = text
        self.norm_id = norm_id
        self.constitutional = constitutional
        self.status = "pending"  # ✅ Default status is pending

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "norm_id": self.norm_id,
            "constitutional": self.constitutional,
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
            "status": self.status,  # ✅ Include status in serialization
        }

    def resolve(self, decision):
        self.constitutional = decision
        self.resolved_at = datetime.utcnow()
        self.status = "solved"  # ✅ Mark as solved
        db.session.commit()
        logging.info(f"Case {self.id}: Resolved with decision {'Constitutional' if decision else 'Unconstitutional'}")

# Import Norm **after** defining Case to resolve circular dependency
from .norm import Norm
