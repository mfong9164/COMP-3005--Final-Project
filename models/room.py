import sys
from pathlib import Path

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from app.base import Base
from sqlalchemy import *

class Room(Base):
    __tablename__ = "Room"
    room_id = Column(Integer, primary_key=True)

    ## Change to ENUM for options
    room_type = Column(String, nullable = False)

    capacity = Column(Integer, nullable = False) 
