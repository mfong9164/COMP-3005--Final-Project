import sys
from pathlib import Path

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from app.base import Base
from sqlalchemy import *
from sqlalchemy.orm import relationship
from models.enums import RoomType

class Room(Base):
    __tablename__ = "Room"
    room_id = Column(
        Integer, 
        primary_key=True
    )

    room_type = Column(
        Enum(RoomType), 
        nullable = False
    )

    capacity = Column(
        Integer, 
        nullable = False
    ) 

    # One room can contain many equipment items
    equipment_items = relationship("Equipment", back_populates="room")

    # One room can host many personal training sessions
    personal_training_sessions = relationship(
        "PersonalTrainingSession",
        back_populates="room",
    )

    # One room can host many group fitness classes
    group_fitness_classes = relationship("GroupFitnessClass", back_populates="room")
