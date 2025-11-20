import sys
from pathlib import Path

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from app.base import Base
from sqlalchemy import Column, Integer, ForeignKey, String, Enum
from models.enums import EquipmentStatus

class Equipment(Base):
    __tablename__ = "Equipment"

    id = Column(
        Integer,
        primary_key=True
    )

    room_id = Column(
        Integer, 
        ForeignKey("Room.id")
    )

    name = Column(
        String,
        nullable=False
    )

    status = Column(
        Enum(EquipmentStatus),
        nullable=False,
        default=EquipmentStatus.IN_SERVICE
    )