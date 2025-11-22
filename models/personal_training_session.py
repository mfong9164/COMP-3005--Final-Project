import sys
from pathlib import Path

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from app.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float, CheckConstraint
from sqlalchemy.dialects.postgresql import TSRANGE
from sqlalchemy.orm import relationship

class PersonalTrainingSession(Base):
    __tablename__ = "PersonalTrainingSession"
    __table_args__ = (
        CheckConstraint('price >= 0', name='check_price_non_negative'),
    )

    id = Column(
        Integer, 
        primary_key=True,
        autoincrement=True
    )

    trainer_email = Column(
        String(255),
        ForeignKey("Trainer.email"),
        nullable=False
    )

    member_email = Column(
        String(255),
        ForeignKey("Member.email"),
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

    # Many sessions belong to one trainer
    trainer = relationship("Trainer", back_populates="personal_training_sessions")

    # Many sessions belong to one member
    member = relationship("Member", back_populates="personal_training_sessions")

    # Many sessions take place in one room
    room = relationship("Room", back_populates="personal_training_sessions")

    # One session can be linked to many bills via PersonalTrainingBill
    personal_training_bills = relationship("PersonalTrainingBill", back_populates="session")