import sys
from pathlib import Path

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from app.base import Base
from sqlalchemy import Column, String, ForeignKey, Enum, Integer
from enums import GoalType


class FitnessGoal(Base):
    __tablename__ = "FitnessGoal"

    member_email = Column(
        String,
        ForeignKey("Member.email"), 
        primary_key=True
    )

    Goaltype = Column(
        Enum(GoalType), 
        primary_key=True
    )

    amount = Column(
        Integer,
        nullable=False
    )