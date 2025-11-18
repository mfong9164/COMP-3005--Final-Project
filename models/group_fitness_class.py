import sys
from pathlib import Path

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from app.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.dialects.postgresql import TSRANGE

class GroupFitnessClass(Base):
    __tablename__ = "GroupFitnessClass"

    id = Column(
        Integer, 
        primary_key=True
    )

    trainer_email = Column(
        String,
        ForeignKey("Trainer.email"),
        nullable=False
    )

    room_id = Column(
        Integer,
        ForeignKey("Room.room_id"),
        nullable=False
    )

    time_stamp_range = Column(
        TSRANGE,
        nullable=False
    )

    price = Column(
        Float,
        nullable=False
    )

    capacity = Column(
        Integer,
        nullable=False,
    )