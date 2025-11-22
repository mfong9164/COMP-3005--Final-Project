import sys
from pathlib import Path

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from app.base import Base
from sqlalchemy import *
from sqlalchemy.orm import relationship

class Room(Base):
    __tablename__ = "Room"
    __table_args__ = (
        CheckConstraint('capacity > 0', name='check_capacity_positive'),
    )
    
    room_id = Column(Integer, primary_key=True, autoincrement=True)

    ## Change to ENUM for options
    room_type = Column(String(50), nullable = False)

    capacity = Column(Integer, nullable = False) 

    # One room can contain many equipment items
    equipment_items = relationship("Equipment", back_populates="room")

    # One room can host many personal training sessions
    personal_training_sessions = relationship(
        "PersonalTrainingSession",
        back_populates="room",
    )

    # One room can host many group fitness classes
    group_fitness_classes = relationship("GroupFitnessClass", back_populates="room")
