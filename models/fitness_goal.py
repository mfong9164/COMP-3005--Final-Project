import sys
from pathlib import Path

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from app.base import Base
from sqlalchemy import *
import enum

class Type(enum.Enum):
    WEIGHT = 0
    BODY_FAT_PERCENTAGE = 1
    CARDIO = 2

class FitnessGoal(Base):
    __tablename__ = "FitnessGoal"

    member_email = Column(
        String,
        ForeignKey("Member.email"), 
        primary_key=True
    )

    type = Column(
        Enum(Type), 
        primary_key=True
    )

    amount = Column(
        Integer
    )