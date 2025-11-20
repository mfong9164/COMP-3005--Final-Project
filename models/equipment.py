import sys
from pathlib import Path

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from app.base import Base
from sqlalchemy import *


class Equipment(Base):
    __tablename__ = "Equipment"
    equipment_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    room_id = Column(Integer, ForeignKey("Room.room_id"), nullable = False)
    status = Column(String, nullable = False)