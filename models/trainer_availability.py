import sys
from pathlib import Path

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from app.base import Base
from sqlalchemy import Column, String, ForeignKey, Enum, text
from sqlalchemy.dialects.postgresql import TSRANGE, ExcludeConstraint
from sqlalchemy.orm import relationship
from models.enums import AvailabilityType

class TrainerAvailability(Base):
    __tablename__ = "TrainerAvailability"
    trainer_email = Column(String(255), ForeignKey("Trainer.email"), primary_key=True)
    time_stamp_range = Column(TSRANGE, primary_key=True)
    availability_type = Column(Enum(AvailabilityType), nullable = False)

    # Many availability entries belong to one trainer
    trainer = relationship("Trainer", back_populates="availabilities")

    # Prevent overlapping Adhoc Time Ranges for the same Trainer
    __table_args__ = (
        ExcludeConstraint(
            ("trainer_email", "="),
            ("time_stamp_range", "&&"),
            where=(text("availability_type = 'ADHOC'")),
            name="no_overlapping_adhoc_availability",
            using="gist",
        ),
    )