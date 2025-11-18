import sys
from pathlib import Path
import enum

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from app.base import Base
from sqlalchemy import *
from sqlalchemy.dialects.postgresql import TSRANGE
from models.enums import AvailabilityType

class TrainerAvailability(Base):
    __tablename__ = "TrainerAvailability"
    email = Column(String, primary_key=True)
    time_stamp_range = Column(TSRANGE, primary_key=True)
    availability_type = Column(Enum(AvailabilityType))