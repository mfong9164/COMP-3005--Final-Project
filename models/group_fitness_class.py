import sys
from pathlib import Path

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from app.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float, CheckConstraint
from sqlalchemy.dialects.postgresql import TSRANGE
from sqlalchemy.orm import relationship

class GroupFitnessClass(Base):
    __tablename__ = "GroupFitnessClass"
    __table_args__ = (
        CheckConstraint('price >= 0', name='check_price_non_negative'),
        CheckConstraint('capacity > 0', name='check_capacity_positive'),
    )

    id = Column(
        Integer, 
        primary_key=True,
        autoincrement=True
    )

    trainer_email = Column(
        String(255),
        ForeignKey("Trainer.trainer_email"),
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

    # Many classes are taught by one trainer
    trainer = relationship("Trainer", back_populates="group_fitness_classes")

    # Many classes are held in one room
    room = relationship("Room", back_populates="group_fitness_classes")

    # One class can have many participation records
    participants = relationship("ParticipatesIn",back_populates="fitness_class")

    # One class can be linked to many bills via GroupFitnessBill
    group_fitness_bills = relationship("GroupFitnessBill", back_populates="fitness_class")