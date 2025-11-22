import sys
from pathlib import Path

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from app.base import Base
from sqlalchemy import *
from models.enums import EquipmentStatus
from sqlalchemy.orm import relationship


class Equipment(Base):
    __tablename__ = "Equipment"
    
    equipment_id = Column(
        Integer, 
        primary_key=True
    )

    name = Column(
        String, 
        nullable=False
    )

    room_id = Column(
        Integer, 
        ForeignKey("Room.room_id"), 
        nullable = False
    )
    
    status = Column(
        Enum(EquipmentStatus), 
        nullable=False, 
        default=EquipmentStatus.IN_SERVICE
    )

    # Many equipment items belong to one room
    room = relationship("Room", back_populates="equipment_items")

    # One equipment item can have many maintenance tickets
    maintenance_tickets = relationship("MaintenanceTicket", back_populates="equipment")